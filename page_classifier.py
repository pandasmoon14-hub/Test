#!/usr/bin/env python3
"""Deterministic page modality classifier with stronger routing signals."""
from __future__ import annotations


def classify_page(char_count: int, table_density: float, statblock_density: float, form_density: float, image_coverage: float) -> str:
    if image_coverage > 0.9 and char_count < 80:
        return "scan"
    if char_count < 70 and table_density < 0.04 and form_density < 0.05 and statblock_density < 0.08:
        return "divider"

    strong_table = table_density >= 0.22
    strong_form = form_density >= 0.28
    strong_stat = statblock_density >= 0.3

    mixed_signals = sum(1 for cond in [table_density > 0.08, form_density > 0.12, statblock_density > 0.12] if cond)

    if strong_form and not strong_table:
        return "form"
    if strong_stat and not strong_table and not strong_form:
        return "statblock"
    if strong_table and not strong_form and not strong_stat:
        return "table"
    if mixed_signals >= 2:
        return "mixed"
    return "prose"
