#!/usr/bin/env python3
"""Shared mechanics vocabulary utilities for TTRPG extraction."""

from __future__ import annotations

import re
import os
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VocabMatch:
    hits: int
    family: str


VOCAB_FAMILIES: dict[str, tuple[str, ...]] = {
    "d20": (
        "armor class", "hit points", "saving throw", "proficiency", "spell slots", "challenge rating", "initiative", "ability score",
    ),
    "year_zero": ("agility", "wits", "empathy", "strength", "stress", "trauma", "critical injury"),
    "whog": ("hardiness", "parry", "evade", "qi", "max wounds", "resolve", "quickness", "movement speed"),
    "wod": ("willpower", "humanity", "hunger", "auspex", "discipline", "paradox", "quintessence"),
    "shadowrun": ("dice pool", "edge", "initiative score", "matrix", "condition monitor", "essence", "drain"),
    "gurps": ("advantages", "disadvantages", "point cost", "skill level", "basic speed", "hit location"),
    "savage_worlds": ("pace", "parry", "toughness", "wild die", "raise", "edges", "hindrances"),
    "pbta": ("moves", "on a 10+", "on a 7-9", "on a miss", "hold", "forward"),
    "astra": ("dao", "tier", "astra-well", "heartbeat", "friction", "epiphany", "dao-vein"),
    "cypher": ("effort", "might pool", "speed pool", "intellect pool", "cypher limit", "artifact", "recovery roll"),
    "l5r": ("strife", "opportunity", "void points", "honor", "glory", "composure", "endurance", "focus"),
    "genesys": ("triumph", "despair", "advantage", "threat", "setback die", "boost die", "proficiency die"),
    "rolemaster": ("offensive bonus", "defensive bonus", "maneuver points", "critical strike", "fumble", "moving maneuver"),
    "hero_system": ("stun", "body", "endurance", "speed", "ocv", "dcv", "ego combat value"),
    "symbaroum": ("corruption", "shadow", "toughness", "resolute", "vigilant", "discreet", "persuasive"),
    "mothership": ("stress", "panic check", "wounds", "sanity", "body save", "fear save", "armor save"),
    "anima": (
        "zeon", "ki", "ma multiple", "magic accumulation", "psychic points",
        "attack ability", "defense ability", "life points", "life point multiple",
        "development points", "psychic projection", "magic projection", "accumulation multiple",
        "supernatural ability",
    ),
    "tri_stat": (
        "body", "mind", "soul", "attack combat value", "defense combat value",
        "health points", "energy points", "shock value",
    ),
    "cortex": ("distinction", "stress die", "complications", "plot points", "asset"),
    "fantasy_age": ("health", "defense", "speed", "stunt points", "ability focus"),
    "scion": ("legend", "epic attributes", "boons", "birthrights", "fatebinding", "purviews"),
    "warhammer": (
        "wounds", "ballistic skill", "weapon skill", "toughness", "fellowship",
        "fate points", "corruption points", "influence",
    ),
    "osr": ("thac0", "morale", "treasure type", "reaction roll", "saving throw", "armor class", "experience points"),
    "generic": ("difficulty", "target number", "critical", "success", "failure", "cooldown", "resource"),
}


def load_custom_vocab(path: str | None = None) -> None:
    if not path:
        return
    candidate = Path(path)
    if not candidate.exists():
        return
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    for family, keywords in payload.items():
        if isinstance(family, str) and isinstance(keywords, list):
            cleaned = tuple(str(k).strip().lower() for k in keywords if str(k).strip())
            if cleaned:
                VOCAB_FAMILIES[family] = cleaned


load_custom_vocab(os.getenv("MECHANICS_VOCAB_EXTRA"))


def mechanics_hits(text: str) -> dict[str, int]:
    low = text.lower()
    out: dict[str, int] = {}
    for family, keys in VOCAB_FAMILIES.items():
        out[family] = sum(1 for key in keys if key in low)
    return out


def best_family(text: str) -> VocabMatch:
    scores = mechanics_hits(text)
    family, hits = max(scores.items(), key=lambda item: item[1])
    return VocabMatch(hits=hits, family=family)


def statblock_density(text: str) -> float:
    low = text.lower()
    kv = len(re.findall(r"\b[a-z][a-z\s]{2,30}:\s*[^\n]+", low))
    vocab = sum(mechanics_hits(text).values())
    bullet = len(re.findall(r"^\s*[-*]\s+", text, flags=re.MULTILINE))
    raw = (vocab * 1.2) + (kv * 0.8) + (bullet * 0.15)
    return min(1.0, raw / 10.0)
