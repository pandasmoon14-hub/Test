from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ChunkType(StrEnum):
    FRONTMATTER = "frontmatter"
    TOC = "toc"
    PROSE_LORE = "prose_lore"
    RULES_TEXT = "rules_text"
    CLASS_FEATURE = "class_feature"
    SPELL_OR_POWER = "spell_or_power"
    ITEM_BLOCK = "item_block"
    NPC_OR_BESTIARY = "npc_or_bestiary"
    STATBLOCK = "statblock"
    TABLE_LIGHT = "table_light"
    TABLE_HEAVY = "table_heavy"
    MIXED_DENSE = "mixed_dense"
    APPENDIX_REFERENCE = "appendix_reference"
    INDEX_OR_GLOSSARY = "index_or_glossary"
    JUNK_OR_ARTIFACT = "junk_or_artifact"


class RouteName(StrEnum):
    SKIP = "skip"
    PRESERVE_RAW = "preserve_raw"
    DETERMINISTIC_TRANSFORM = "deterministic_transform"
    ONE_PASS_CONVERT = "one_pass_convert"
    TWO_PASS_CONVERT = "two_pass_convert"
    GUARDED_STATBLOCK_CONVERT = "guarded_statblock_convert"
    GUARDED_TABLE_CONVERT = "guarded_table_convert"
    ESCALATE_REVIEW = "escalate_review"


class ChunkSizeClass(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    OVERSIZE = "oversize"


class FinalStatus(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ESCALATED = "escalated"
    SKIPPED = "skipped"


@dataclass(slots=True)
class ChunkFeatures:
    chunk_id: str
    sourcebook_id: str
    chunk_type: ChunkType
    chunk_size_class: ChunkSizeClass
    char_count: int
    is_empty: bool = False
    artifact_score: float = 0.0
    ambiguity_score: float = 0.0
    predicted_validator_risk: float = 0.0
    mechanics_density: float = 0.0
    contains_patterns: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RouteOverrideMatch:
    name: str
    priority: int
    matched: bool
    resulting_route: RouteName | None = None
    rationale: str = ""


@dataclass(slots=True)
class RouteDecision:
    chunk_id: str
    sourcebook_id: str
    chunk_type: ChunkType
    chunk_size_class: ChunkSizeClass
    assigned_route: RouteName
    final_route: RouteName
    override_name: str | None = None
    rationale: str = ""
    validator_names: list[str] = field(default_factory=list)
    retry_policy: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
