from __future__ import annotations

import re
from dataclasses import dataclass

from astra_cloud.schemas.route import ChunkFeatures, ChunkSizeClass, ChunkType


FRONTMATTER_PATTERNS = re.compile(
    r"copyright|all rights reserved|isbn|credits|published by|open game license",
    re.I,
)
TOC_PATTERNS = re.compile(r"^#*\s*(table of contents|contents)\b", re.I | re.M)
INDEX_PATTERNS = re.compile(r"^#*\s*(index|glossary|appendix)\b", re.I | re.M)
STATBLOCK_PATTERNS = re.compile(r"\b(AC|HP|Hit Points|Speed|STR|DEX|CON|INT|WIS|CHA|Initiative)\b")
SPELL_PATTERNS = re.compile(r"\b(range|duration|casting time|components?|save|spell level|power cost)\b", re.I)
ITEM_PATTERNS = re.compile(r"\b(cost|price|bulk|damage|armor|weapon|item level|credits?)\b", re.I)
RULES_PATTERNS = re.compile(r"\b(when you|if you|must|can|check|roll|saving throw|action|turn)\b", re.I)
LORE_PATTERNS = re.compile(r"\b(history|culture|faction|world|legend|society|region|empire)\b", re.I)
GIBBERISH_PATTERNS = re.compile(r"[�]{2,}|(?:\b[a-z]{1,2}\b\s*){10,}")


@dataclass(slots=True)
class ClassificationResult:
    chunk_type: ChunkType
    size_class: ChunkSizeClass
    mechanics_density: float
    artifact_score: float
    ambiguity_score: float


def _normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def detect_size_class(char_count: int) -> ChunkSizeClass:
    if char_count <= 2500:
        return ChunkSizeClass.SMALL
    if char_count <= 7000:
        return ChunkSizeClass.MEDIUM
    if char_count <= 12000:
        return ChunkSizeClass.LARGE
    return ChunkSizeClass.OVERSIZE


def _table_density(text: str) -> float:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return 0.0
    tableish = sum(1 for line in lines if line.count("|") >= 2 or "\t" in line)
    return tableish / max(len(lines), 1)


def _mechanics_density(text: str) -> float:
    hits = 0
    for pattern in (STATBLOCK_PATTERNS, SPELL_PATTERNS, ITEM_PATTERNS, RULES_PATTERNS):
        hits += len(pattern.findall(text))
    return min(hits / max(len(text.split()), 1), 1.0)


def classify_text(text: str) -> ClassificationResult:
    text = _normalize_text(text)
    char_count = len(text)
    size_class = detect_size_class(char_count)
    if not text:
        return ClassificationResult(ChunkType.JUNK_OR_ARTIFACT, size_class, 0.0, 1.0, 0.0)

    table_density = _table_density(text)
    mechanics_density = _mechanics_density(text)
    artifact_score = 1.0 if GIBBERISH_PATTERNS.search(text) else 0.0

    if FRONTMATTER_PATTERNS.search(text[:1200]):
        chunk_type = ChunkType.FRONTMATTER
    elif TOC_PATTERNS.search(text[:3000]):
        chunk_type = ChunkType.TOC
    elif artifact_score >= 1.0:
        chunk_type = ChunkType.JUNK_OR_ARTIFACT
    elif table_density >= 0.55:
        chunk_type = ChunkType.TABLE_HEAVY
    elif table_density >= 0.18:
        chunk_type = ChunkType.TABLE_LIGHT
    elif STATBLOCK_PATTERNS.search(text) and mechanics_density >= 0.08:
        chunk_type = ChunkType.STATBLOCK
    elif SPELL_PATTERNS.search(text):
        chunk_type = ChunkType.SPELL_OR_POWER
    elif ITEM_PATTERNS.search(text):
        chunk_type = ChunkType.ITEM_BLOCK
    elif INDEX_PATTERNS.search(text[:1500]):
        chunk_type = ChunkType.INDEX_OR_GLOSSARY
    elif RULES_PATTERNS.search(text) and LORE_PATTERNS.search(text):
        chunk_type = ChunkType.MIXED_DENSE
    elif RULES_PATTERNS.search(text):
        chunk_type = ChunkType.RULES_TEXT
    elif LORE_PATTERNS.search(text):
        chunk_type = ChunkType.PROSE_LORE
    else:
        chunk_type = ChunkType.MIXED_DENSE

    ambiguity_score = 0.7 if chunk_type == ChunkType.MIXED_DENSE else 0.2
    if chunk_type in {ChunkType.TABLE_LIGHT, ChunkType.TABLE_HEAVY} and STATBLOCK_PATTERNS.search(text):
        ambiguity_score = 0.8

    return ClassificationResult(
        chunk_type=chunk_type,
        size_class=size_class,
        mechanics_density=mechanics_density,
        artifact_score=artifact_score,
        ambiguity_score=ambiguity_score,
    )


def classify_chunk(chunk_id: str, sourcebook_id: str, text: str) -> ChunkFeatures:
    result = classify_text(text)
    normalized = _normalize_text(text)
    return ChunkFeatures(
        chunk_id=chunk_id,
        sourcebook_id=sourcebook_id,
        chunk_type=result.chunk_type,
        chunk_size_class=result.size_class,
        char_count=len(normalized),
        is_empty=not bool(normalized),
        artifact_score=result.artifact_score,
        ambiguity_score=result.ambiguity_score,
        predicted_validator_risk=0.65
        if result.chunk_type in {ChunkType.MIXED_DENSE, ChunkType.TABLE_HEAVY, ChunkType.STATBLOCK}
        else 0.25,
        mechanics_density=result.mechanics_density,
    )
