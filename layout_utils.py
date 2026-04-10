#!/usr/bin/env python3
"""Shared layout heuristics used by orchestrator and calibration tools."""

from __future__ import annotations

import re
import statistics

import fitz

from mechanics_vocab import statblock_density as vocab_statblock_density


def detect_multicolumn(blocks: list[tuple]) -> bool:
    text_blocks = [b for b in blocks if len(b) >= 5 and str(b[4]).strip()]
    if len(text_blocks) < 8:
        return False
    xs = []
    for b in text_blocks:
        txt = str(b[4]).strip()
        width = max(1.0, float(b[2]) - float(b[0]))
        if len(txt) < 10 and width < 120:
            continue
        xs.append(float(b[0]))
    if len(xs) < 8:
        return False
    xs = sorted(xs)
    mid = statistics.median(xs)
    left = [x for x in xs if x < mid]
    right = [x for x in xs if x >= mid]
    if len(left) < 3 or len(right) < 3:
        return False
    return (statistics.mean(right) - statistics.mean(left)) > 90


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
