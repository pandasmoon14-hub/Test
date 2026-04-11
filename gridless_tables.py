#!/usr/bin/env python3
"""Aligned-column detection for gridless tables."""
from __future__ import annotations

import re
from table_model import TableCell, TableRow, TableSidecar


def detect_gridless_rows(text: str) -> list[str]:
    rows = []
    for ln in text.splitlines():
        if len(re.findall(r"\s{2,}", ln)) >= 2 and re.search(r"\S\s{2,}\S", ln):
            rows.append(ln.rstrip())
    return rows


def _split_aligned_row(row: str) -> list[str]:
    return [part.strip() for part in re.split(r"\s{2,}", row.strip())]


def extract_gridless_table(text: str, page_num: int | None = None) -> TableSidecar | None:
    rows = detect_gridless_rows(text)
    if len(rows) < 2:
        return None
    split_rows = [_split_aligned_row(r) for r in rows]
    widths = [len(r) for r in split_rows]
    if max(widths) < 2:
        return None
    width = max(widths)
    norm_rows: list[TableRow] = []
    for row in split_rows:
        padded = row + [""] * (width - len(row))
        norm_rows.append(TableRow(cells=[TableCell(text=cell) for cell in padded]))
    confidence = 0.8 if len(set(widths)) <= 2 else 0.55
    return TableSidecar(page=page_num, bbox=None, rows=norm_rows, render_mode="markdown", confidence=confidence)
