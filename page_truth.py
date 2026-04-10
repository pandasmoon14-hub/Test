#!/usr/bin/env python3
"""Page-truth sidecar helpers.

Stores page metadata derived from source PDF geometry/metadata only.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class PageTruthRecord:
    page: int
    chars: int
    blocks: int
    detected_tables: float = 0.0
    lane: str = "A"
    page_marker_mode: str = "heuristic"
    trusted_page_truth: bool = True


def write_page_truth_jsonl(pdf_path: Path, output_path: Path | list[PageTruthRecord], records: list[PageTruthRecord] | None = None):
    """Compatibility writer.

    Supports both call styles:
    - write_page_truth_jsonl(pdf_path, output_path, records)
    - write_page_truth_jsonl(output_path, records)
    """
    if records is None:
        records = output_path  # type: ignore[assignment]
        output_path = pdf_path  # type: ignore[assignment]
    output_path = Path(output_path)  # type: ignore[arg-type]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [{
        "page": r.page,
        "chars": r.chars,
        "blocks": r.blocks,
        "detected_tables": r.detected_tables,
        "lane": r.lane,
        "page_marker_mode": r.page_marker_mode,
        "trusted_page_truth": r.trusted_page_truth
    } for r in records or []]
    output_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    book_id: str
    page: int
    width: float
    height: float
    rotation: int
    text_chars: int
    image_count: int
    drawing_count: int
    trusted_page_truth: bool = True
    orientation: str = "portrait"
    modality: str = "mixed"
    region_metadata_path: str | None = None
    producer: str = ""
    creator: str = ""
    encrypted: bool = False
    file_size: int = 0


def write_page_truth_jsonl(path: Path, rows: Iterable[PageTruthRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")
