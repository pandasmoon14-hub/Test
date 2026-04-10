#!/usr/bin/env python3
"""Thin typed-region scaffold for page content."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Region:
    kind: str
    text: str
    bbox: tuple[float, float, float, float] | None = None

def segment_regions(text: str) -> list[Region]:
    regions: list[Region] = []
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    total = max(1, len(blocks))
    for idx, block in enumerate(blocks):
        kind = "body"
        if "|" in block:
            kind = "table"
        elif ":" in block and len(block.splitlines()) > 2:
            kind = "statblock"
        elif "___" in block:
            kind = "form"
        elif block.startswith(">"):
            kind = "sidebar/callout"
        bbox = (0.0, idx / total, 1.0, (idx + 1) / total)
        regions.append(Region(kind=kind, text=block, bbox=bbox))
    return regions
