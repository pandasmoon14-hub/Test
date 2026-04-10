#!/usr/bin/env python3
"""Minimal page modality classifier."""
from __future__ import annotations

def classify_page(char_count: int, table_density: float, statblock_density: float, form_density: float, image_coverage: float) -> str:
    if image_coverage > 0.85 and char_count < 50:
        return "scan"
    if form_density > 0.5:
        return "form"
    if table_density > 0.2:
        return "table"
    if statblock_density > 0.3:
        return "statblock"
    if char_count < 80:
        return "divider"
    if table_density > 0.05 or statblock_density > 0.1:
        return "mixed"
    return "prose"
