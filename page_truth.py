#!/usr/bin/env python3
"""Page truth manifest generator for Aether Forge."""

from dataclasses import dataclass
from pathlib import Path
import json


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
