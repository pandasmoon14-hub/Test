#!/usr/bin/env python3
"""Authoritative page-truth model and JSONL writer for Aether Forge v13."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Literal

PageStatus = Literal["ok", "empty", "image_only", "repaired", "queued", "failed", "skipped"]


@dataclass
class PageTruthRecord:
    book_id: str
    source_path: str
    source_sha256: str
    page_index_zero_based: int
    page_number_one_based: int
    width: float
    height: float
    rotation: int
    text_chars: int
    extracted_chars: int
    blocks: int
    image_count: int
    drawing_count: int
    table_count: int = 0
    has_native_text: bool = False
    is_image_only: bool = False
    ocr_required: bool = False
    ocr_attempted: bool = False
    ocr_applied: bool = False
    extraction_backend: str = "unknown"
    extraction_lane: str = "unknown"
    page_status: PageStatus = "ok"
    trust_level: float = 1.0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    run_id: str = ""



def write_page_truth_jsonl(path: Path, rows: Iterable[PageTruthRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(asdict(row), ensure_ascii=False, sort_keys=True) + "\n")
