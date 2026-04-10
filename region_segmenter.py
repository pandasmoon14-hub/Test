#!/usr/bin/env python3
"""Thin typed-region scaffold for page content."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Region:
    kind: str
    text: str

def segment_regions(text: str) -> list[Region]:
    regions: list[Region] = []
    for block in [b.strip() for b in text.split("\n\n") if b.strip()]:
        kind = "body"
        if "|" in block:
            kind = "table"
        elif ":" in block and len(block.splitlines()) > 2:
            kind = "statblock"
        elif "___" in block:
            kind = "form"
        elif block.startswith(">"):
            kind = "sidebar"
        regions.append(Region(kind=kind, text=block))
    return regions
