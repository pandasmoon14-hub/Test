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
