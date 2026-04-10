#!/usr/bin/env python3
"""Shared layout heuristics used by orchestrator and calibration tools."""

from __future__ import annotations

import re

import fitz

from mechanics_vocab import statblock_density as vocab_statblock_density


def detect_multicolumn(blocks: list[tuple], page_width: float | None = None) -> bool:
    text_blocks: list[tuple[float, float, float, float]] = []
    for b in blocks:
        if len(b) < 5:
            continue
        txt = str(b[4]).strip()
        if not txt:
            continue
        x0, y0, x1, y1 = map(float, b[:4])
        width = x1 - x0
        if len(txt) < 12 and width < 120:
            continue
        text_blocks.append((x0, y0, x1, y1))
    if len(text_blocks) < 6:
        return False

    if page_width is None:
        page_width = max(x1 for _, _, x1, _ in text_blocks)

    centers = [((x0 + x1) / 2.0, y0, y1) for x0, y0, x1, y1 in text_blocks]
    left = [(c, y0, y1) for c, y0, y1 in centers if c < page_width * 0.45]
    right = [(c, y0, y1) for c, y0, y1 in centers if c > page_width * 0.55]
    if len(left) < 3 or len(right) < 3:
        return False

    left_band = (min(y0 for _, y0, _ in left), max(y1 for _, _, y1 in left))
    right_band = (min(y0 for _, y0, _ in right), max(y1 for _, _, y1 in right))
    overlap = min(left_band[1], right_band[1]) - max(left_band[0], right_band[0])
    return overlap > 120


def detect_table_density(text: str) -> float:
    lines = text.splitlines()
    if not lines:
        return 0.0
    tableish = sum(1 for line in lines if line.count("|") >= 2 or re.search(r"\b\d+\s{2,}\d+\b", line))
    return tableish / len(lines)


def vector_table_density(page: fitz.Page) -> float:
    drawings = page.get_drawings()
    if not drawings:
        return 0.0
    horizontals = 0
    verticals = 0
    for draw in drawings:
        rect = draw.get("rect")
        if rect is None:
            continue
        if rect.width > page.rect.width * 0.2 and rect.height <= 2.0:
            horizontals += 1
        if rect.height > page.rect.height * 0.08 and rect.width <= 2.0:
            verticals += 1
    return min(1.0, (horizontals + verticals) / 20.0)


def detect_statblock_density(text: str) -> float:
    return vocab_statblock_density(text)
