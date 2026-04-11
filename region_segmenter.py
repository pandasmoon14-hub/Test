#!/usr/bin/env python3
"""Typed region segmentation for mixed page content."""
from __future__ import annotations
from dataclasses import dataclass
import re


@dataclass
class Region:
    kind: str
    text: str
    bbox: tuple[float, float, float, float] | None = None
    page: int | None = None
    region_id: str | None = None


def _kind_for_block(block: str) -> str:
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    joined = "\n".join(lines)
    if not lines:
        return "body"
    if joined.startswith(">") or any(x in joined.lower() for x in ["sidebar", "callout", "note:"]):
        return "sidebar/callout"
    if any("|" in ln for ln in lines) and len(lines) >= 2:
        return "table"
    if sum(1 for ln in lines if re.search(r"\b[^:]{2,}:\s*\S", ln)) >= 3:
        return "statblock"
    if sum(1 for ln in lines if re.search(r"_{3,}|\.{3,}\s*$", ln)) >= 2:
        return "form"
    if len(lines) <= 2 and any(re.match(r"^#+\s+", ln) for ln in lines):
        return "sidebar/callout"
    return "body"


def segment_regions(text: str, page: int | None = None) -> list[Region]:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    total = max(1, len(blocks))
    regions: list[Region] = []
    for idx, block in enumerate(blocks):
        kind = _kind_for_block(block)
        y0 = round(idx / total, 4)
        y1 = round((idx + 1) / total, 4)
        regions.append(
            Region(
                kind=kind,
                text=block,
                bbox=(0.0, y0, 1.0, y1),
                page=page,
                region_id=f"p{page or 0}_r{idx}_{kind.replace('/', '_')}",
            )
        )
    return regions
