"""
doctrine_validator.py

Validates converted output against batchA_15 conversion invariants.

Five checks per batchA_15:
1. Classification check  — output classified into an Astra doctrine job
2. Split check           — multi-job constructs declared as split
3. Output state check    — lawful output state marker present (high-risk chunks)
4. Ability invariant     — batchA_07 minimum fields present for ability output
5. Donor assumption      — no donor-framing phrases imported as Astra doctrine
"""
from __future__ import annotations

import re

from astra_cloud.schemas.route import ChunkType
from astra_cloud.schemas.runlog import ValidatorOutcome, ValidatorResult


# ---------------------------------------------------------------------------
# Astra doctrine job families (batchA_05 through batchA_10)
# ---------------------------------------------------------------------------
_JOB_SIGNALS: dict[str, list[str]] = {
    "capability":  ["capability", "competency", "skill", "proficiency", "expertise",
                    "knowledge area", "trade", "practiced", "non-activated"],
    "access":      ["access tag", "access gate", "proficiency gate", "domain",
                    "training tag", "license", "attunement", "tradition", "school of",
                    "requires training", "prerequisite", "qualified to"],
    "ability":     ["technique", "spell", "power", "maneuver", "invocation", "stance",
                    "working", "module", "activated", "cast", "activate", "cast time",
                    "use action", "ability object"],
    "resource":    ["cost", "recharge", "charge", "slot", "mana", "stamina", "psi",
                    "essence", "aether", "backlash", "exhaustion", "heat", "fuel",
                    "resource pool", "per rest", "per day", "cooldown", "expenditure"],
    "condition":   ["condition", "status effect", "buff", "debuff", "poisoned",
                    "stunned", "blinded", "frightened", "charmed", "paralyzed",
                    "burning", "bleeding", "ongoing effect", "duration"],
    "damage":      ["damage type", "damage family", "resistance", "vulnerability",
                    "immunity", "fire damage", "cold damage", "necrotic", "radiant",
                    "piercing", "slashing", "bludgeoning", "absorb damage"],
    "progression": ["level up", "gain level", "advancement", "progression", "experience",
                    "rank up", "cultivation", "stage advancement", "milestone", "degree",
                    "class level", "tier advancement"],
}

# Chunk types that need classification verification
_CLASSIFY_CHECK_TYPES = {
    ChunkType.CLASS_FEATURE,
    ChunkType.SPELL_OR_POWER,
    ChunkType.RULES_TEXT,
    ChunkType.NPC_OR_BESTIARY,
    ChunkType.MIXED_DENSE,
}

# Chunk types exempt from classification check (structural/nav content)
_CLASSIFY_EXEMPT_TYPES = {
    ChunkType.FRONTMATTER, ChunkType.TOC, ChunkType.INDEX_OR_GLOSSARY,
    ChunkType.JUNK_OR_ARTIFACT, ChunkType.APPENDIX_REFERENCE,
    ChunkType.TABLE_LIGHT, ChunkType.TABLE_HEAVY,
}

# High-complexity types that should carry explicit output state markers
_OUTPUT_STATE_REQUIRED = {
    ChunkType.CLASS_FEATURE,
    ChunkType.SPELL_OR_POWER,
    ChunkType.NPC_OR_BESTIARY,
}

# batchA_07 minimum core record fields
_ABILITY_REQUIRED = {"identity", "classification", "activation", "scope",
                     "payload", "resolution", "persistence"}

# Regex patterns
_SPLIT_SIGNAL = re.compile(
    r"\b(split|separate|decompos|broken into|divided into|two records|"
    r"two entries|split record|sub-record)\b",
    re.I,
)
_MULTI_JOB_SIGNAL = re.compile(
    r"\b(also|additionally|furthermore|it also|combined|multi-purpose|"
    r"dual-purpose|functions as|serves as|acts as|doubles as)\b",
    re.I,
)
_OUTPUT_STATE_SIGNAL = re.compile(
    r"\[(?:source-local|quarantine|escalate|direct-map|normalized-map|"
    r"cosmology-local)\]|output_state\s*:\s*\w",
    re.I,
)
_YAML_FIELD = re.compile(r"^\s*(\w[\w_-]*):\s", re.M)
_DONOR_ASSUMPTION = re.compile(
    r"\b(in this system|in [A-Z][a-z]+ rules|as per [A-Z]|"
    r"following [A-Z][a-z]+ convention|according to the source|"
    r"as written in the donor|donor-native)\b",
    re.I,
)


class DoctrineValidator:
    """Validates converted chunks against batchA_15 conversion invariants."""

    def validate(
        self,
        chunk_id: str,
        chunk_type: ChunkType,
        converted_text: str,
    ) -> ValidatorResult:
        issues: list[str] = []
        warnings: list[str] = []
        text_lower = converted_text.lower()

        # ------------------------------------------------------------------
        # 1. Classification check
        # ------------------------------------------------------------------
        if chunk_type in _CLASSIFY_CHECK_TYPES:
            matched = [
                job for job, sigs in _JOB_SIGNALS.items()
                if any(s in text_lower for s in sigs)
            ]
            if not matched:
                issues.append(
                    "classification_missing: no Astra doctrine job family detected; "
                    "conversion may have bypassed batchA_15 classification discipline"
                )
            elif len(matched) >= 3 and not _SPLIT_SIGNAL.search(converted_text):
                warnings.append(
                    f"layer_collapse_risk: {len(matched)} job families detected "
                    f"({', '.join(matched[:3])}) without split declaration; "
                    "verify batchA_15 split-vs-merge discipline was applied"
                )

        # ------------------------------------------------------------------
        # 2. Split check
        # ------------------------------------------------------------------
        if _MULTI_JOB_SIGNAL.search(converted_text) and not _SPLIT_SIGNAL.search(converted_text):
            warnings.append(
                "multi_job_unsplit: multi-purpose language present without split "
                "declaration — verify against batchA_15 split-vs-merge rule"
            )

        # ------------------------------------------------------------------
        # 3. Output state check (soft — warn only for high-complexity types)
        # ------------------------------------------------------------------
        if (
            chunk_type in _OUTPUT_STATE_REQUIRED
            and not _OUTPUT_STATE_SIGNAL.search(converted_text)
        ):
            warnings.append(
                "output_state_undeclared: high-complexity chunk lacks explicit output "
                "state marker ([source-local], [quarantine], etc.); "
                "add annotation for conversion traceability"
            )

        # ------------------------------------------------------------------
        # 4. Ability invariant (batchA_07 minimum record)
        # ------------------------------------------------------------------
        if chunk_type in {ChunkType.SPELL_OR_POWER, ChunkType.CLASS_FEATURE}:
            found = {m.group(1).lower() for m in _YAML_FIELD.finditer(converted_text)}
            missing = [f for f in _ABILITY_REQUIRED if not any(f in ff for ff in found)]
            if missing:
                warnings.append(
                    f"ability_record_incomplete: batchA_07 minimum fields not found: "
                    f"{missing}"
                )

        # ------------------------------------------------------------------
        # 5. Donor assumption import
        # ------------------------------------------------------------------
        donor_hits = _DONOR_ASSUMPTION.findall(converted_text)
        if donor_hits:
            issues.append(
                f"donor_assumption_imported: {len(donor_hits)} phrase(s) reference "
                "donor framing directly — verify not treated as Astra doctrine"
            )

        # Outcome
        if issues:
            outcome = ValidatorOutcome.FAIL
            msg = "; ".join(issues[:2])
        elif warnings:
            outcome = ValidatorOutcome.WARN
            msg = "; ".join(warnings[:2])
        else:
            outcome = ValidatorOutcome.PASS
            msg = "doctrine invariants satisfied"

        return ValidatorResult(
            name="doctrine_validator",
            outcome=outcome,
            message=msg,
            score=max(0.0, 1.0 - len(issues) * 0.25),
            details={
                "issues": issues,
                "warnings": warnings,
                "matched_job_families": [
                    job for job, sigs in _JOB_SIGNALS.items()
                    if any(s in text_lower for s in sigs)
                ],
            },
        )
