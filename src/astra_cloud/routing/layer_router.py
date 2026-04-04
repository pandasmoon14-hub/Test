"""
layer_router.py

Routes classified chunks to specific Astra doctrine layers (batchA_05–batchA_12)
and detects multi-job constructs that require splitting per batchA_15.

This sits AFTER classify_chunk() and BEFORE the conversion prompt is applied.
Its job is to answer: which doctrine file(s) govern this chunk's conversion?
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum

from astra_cloud.schemas.route import ChunkType


class AstraLayer(StrEnum):
    LEXICON     = "batchA_01"
    CHASSIS     = "batchA_02"
    RESOLUTION  = "batchA_03"
    ATTRIBUTES  = "batchA_04"
    CAPABILITY  = "batchA_05"
    ACCESS      = "batchA_06"
    ABILITY     = "batchA_07"
    RESOURCE    = "batchA_07b"
    CONDITION   = "batchA_08"
    DAMAGE      = "batchA_09"
    PROGRESSION = "batchA_10"
    ORIGIN      = "batchA_11"
    PATH        = "batchA_12"
    LOADOUT     = "batchA_14"
    UNKNOWN     = "unknown"


@dataclass
class LayerRouteDecision:
    chunk_id: str
    primary_layer: AstraLayer
    secondary_layers: list[AstraLayer] = field(default_factory=list)
    split_required: bool = False
    split_rationale: str = ""
    escalate: bool = False
    escalate_reason: str = ""
    confidence: float = 1.0
    rationale: str = ""


# ---------------------------------------------------------------------------
# Signal vocabulary per layer
# Minimum 2 hits required to count a layer as "detected".
# ---------------------------------------------------------------------------
_SIGNALS: dict[AstraLayer, list[str]] = {
    AstraLayer.CAPABILITY: [
        "skill", "proficiency", "expertise", "competency", "knowledge area",
        "trade", "tool use", "trained in", "lore", "craft", "discipline",
        "practical capacity", "non-activated", "passive ability", "background skill",
    ],
    AstraLayer.ACCESS: [
        "domain", "license", "training requirement", "access tag", "permission",
        "eligibility", "proficiency gate", "attunement", "tradition", "school of",
        "armor proficiency", "weapon proficiency", "implant clearance",
        "relic access", "qualified to", "requires training", "prerequisite",
    ],
    AstraLayer.ABILITY: [
        "spell", "power", "technique", "maneuver", "invocation", "stance",
        "ability", "working", "module", "activated", "cast", "activate",
        "trigger", "use action", "bonus action", "cast time", "ability object",
    ],
    AstraLayer.RESOURCE: [
        "cost", "recharge", "charge", "slot", "mana", "stamina", "psi",
        "essence", "aether", "backlash", "exhaustion", "heat", "fuel",
        "resource pool", "expenditure", "replenish", "per rest", "per day",
        "cooldown", "recover resource", "resource economy",
    ],
    AstraLayer.CONDITION: [
        "condition", "status effect", "buff", "debuff", "poisoned", "stunned",
        "blinded", "frightened", "charmed", "paralyzed", "incapacitated",
        "burning", "bleeding", "ongoing effect", "duration", "end of turn",
        "remove condition", "suppress condition",
    ],
    AstraLayer.DAMAGE: [
        "damage type", "damage family", "fire damage", "cold damage", "acid",
        "lightning", "necrotic", "radiant", "piercing", "slashing", "bludgeoning",
        "resistance", "vulnerability", "immunity", "absorb damage",
        "damage reduction", "damage conversion",
    ],
    AstraLayer.PROGRESSION: [
        "level up", "gain level", "advancement", "progression", "experience",
        "rank up", "cultivation", "stage advancement", "milestone", "degree",
        "class level", "proficiency bonus increase", "tier advancement",
        "xp", "exp gain", "level progression",
    ],
    AstraLayer.ATTRIBUTES: [
        "strength", "dexterity", "constitution", "intelligence", "wisdom",
        "charisma", "ability score", "attribute", "modifier", "stat bonus",
        "derived stat", "hit points", "armor class", "saving throw bonus",
        "primary attribute", "secondary stat",
    ],
    AstraLayer.RESOLUTION: [
        "roll", "check", "test", "contest", "difficulty class", " dc ",
        "opposed check", "saving throw", "skill check", "attack roll",
        "threshold", "result band", "success", "failure", "critical",
    ],
    AstraLayer.LOADOUT: [
        "starting equipment", "starting gear", "kit", "loadout", "equipment package",
        "starting wealth", "starting items", "initial loadout", "gear package",
    ],
    AstraLayer.ORIGIN: [
        "race", "species", "ancestry", "heritage", "background", "kinform",
        "lineage", "origin", "culture", "upbringing", "homeland", "biology",
    ],
    AstraLayer.PATH: [
        "class", "subclass", "archetype", "path", "profession", "vocation",
        "class feature", "subclass feature", "path ability", "class option",
    ],
    AstraLayer.LEXICON: [
        "glossary", "defined term", "terminology", "definition", "term entry",
        "lexicon entry", "see also", "refer to",
    ],
}

# Chunk types that naturally carry multiple families (no split alarm)
_MULTI_FAMILY_EXEMPT = {
    ChunkType.STATBLOCK,
    ChunkType.NPC_OR_BESTIARY,
    ChunkType.MIXED_DENSE,
    ChunkType.TABLE_HEAVY,
}

# Chunk-type → expected primary layer (fallback if signal detection is weak)
_TYPE_DEFAULT: dict[ChunkType, AstraLayer] = {
    ChunkType.SPELL_OR_POWER:  AstraLayer.ABILITY,
    ChunkType.CLASS_FEATURE:   AstraLayer.PATH,
    ChunkType.ITEM_BLOCK:      AstraLayer.LOADOUT,
    ChunkType.RULES_TEXT:      AstraLayer.RESOLUTION,
    ChunkType.NPC_OR_BESTIARY: AstraLayer.ABILITY,
    ChunkType.STATBLOCK:       AstraLayer.ABILITY,
    ChunkType.PROSE_LORE:      AstraLayer.ORIGIN,
    ChunkType.INDEX_OR_GLOSSARY: AstraLayer.LEXICON,
}

_SPLIT_SIG = re.compile(
    r"\b(split|separate|decompos|broken into|divided into|"
    r"two records|two entries|split record)\b",
    re.I,
)

_MIN_HITS = 2  # minimum signal count to consider a layer "detected"


def _score_layers(text: str) -> list[tuple[AstraLayer, int]]:
    tl = text.lower()
    scores = [
        (layer, sum(1 for sig in sigs if sig in tl))
        for layer, sigs in _SIGNALS.items()
    ]
    return sorted(
        [(l, s) for l, s in scores if s >= _MIN_HITS],
        key=lambda x: x[1],
        reverse=True,
    )


def route_to_doctrine_layer(
    chunk_id: str,
    chunk_type: ChunkType,
    text: str,
) -> LayerRouteDecision:
    """
    Determine which Astra doctrine layer(s) govern this chunk and whether
    a batchA_15 split is required.
    """
    scored = _score_layers(text)
    fallback = _TYPE_DEFAULT.get(chunk_type, AstraLayer.UNKNOWN)

    if not scored:
        return LayerRouteDecision(
            chunk_id=chunk_id,
            primary_layer=fallback,
            confidence=0.4,
            rationale=f"no_signal; chunk_type_default={fallback}",
        )

    primary_layer, primary_hits = scored[0]
    secondary = [l for l, _ in scored[1:4]]

    # Split required? 3+ distinct job families in a non-exempt chunk type.
    split_required = (
        len(scored) >= 3
        and chunk_type not in _MULTI_FAMILY_EXEMPT
    )
    split_rationale = (
        f"batchA_15_split_required: {len(scored)} doctrine families detected "
        f"({', '.join(l.value for l, _ in scored[:3])}); "
        "evaluate whether construct should be decomposed into separate records"
        if split_required else ""
    )

    # Escalate if we genuinely cannot determine the layer
    escalate = primary_layer == AstraLayer.UNKNOWN
    escalate_reason = "no_doctrine_layer_determinable" if escalate else ""

    # Confidence: fraction of that layer's signals hit, capped at 1.0
    max_possible = len(_SIGNALS.get(primary_layer, []))
    confidence = round(min(1.0, primary_hits / max(max_possible, 1)), 3)

    return LayerRouteDecision(
        chunk_id=chunk_id,
        primary_layer=primary_layer,
        secondary_layers=secondary,
        split_required=split_required,
        split_rationale=split_rationale,
        escalate=escalate,
        escalate_reason=escalate_reason,
        confidence=confidence,
        rationale=(
            f"primary={primary_layer}({primary_hits} hits); "
            f"total_layers={len(scored)}; chunk_type={chunk_type}"
        ),
    )
