#!/usr/bin/env python3
"""Shared mechanics vocabulary utilities for TTRPG extraction."""

from __future__ import annotations

import re
from dataclasses import dataclass


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
    "generic": ("difficulty", "target number", "critical", "success", "failure", "cooldown", "resource"),
}


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
