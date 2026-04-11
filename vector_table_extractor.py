#!/usr/bin/env python3
"""Vector table extraction into structured table models."""
from __future__ import annotations
from typing import Any

from table_model import TableCell, TableRow, TableSidecar

try:
    import fitz
except Exception:  # pragma: no cover
    fitz = Any  # type: ignore


def _table_from_cells(cells: list[list[str]], page_num: int | None, bbox: list[float] | None, confidence: float = 0.8) -> TableSidecar:
    rows = [TableRow(cells=[TableCell(text=str(cell).strip()) for cell in row]) for row in cells if row]
    return TableSidecar(page=page_num, bbox=bbox, rows=rows, render_mode="markdown", confidence=confidence)


def extract_vector_tables(page: Any, page_num: int | None = None) -> list[TableSidecar]:
    """Extract candidate vector tables and return TableSidecar models.

    Supports either real fitz.Page.find_tables() output or test doubles containing
    table-like dicts with keys: bbox, cells/rows.
    """
    tables: list[TableSidecar] = []
    try:
        found = page.find_tables()
        raw_tables = getattr(found, "tables", found)
    except Exception:
        raw_tables = []

    for raw in raw_tables or []:
        bbox = None
        if getattr(raw, "bbox", None):
            bbox = [float(v) for v in raw.bbox]
        elif isinstance(raw, dict) and raw.get("bbox"):
            bbox = [float(v) for v in raw["bbox"]]

        cells: list[list[str]] | None = None
        if hasattr(raw, "extract"):
            try:
                cells = raw.extract()
            except Exception:
                cells = None
        if cells is None and hasattr(raw, "rows"):
            cells = getattr(raw, "rows")
        if cells is None and isinstance(raw, dict):
            cells = raw.get("cells") or raw.get("rows")

        if cells:
            tables.append(_table_from_cells(cells, page_num=page_num, bbox=bbox, confidence=0.85))
        elif bbox:
            degraded = TableSidecar(page=page_num, bbox=bbox, rows=[TableRow(cells=[TableCell(text="[vector-table-unparsed]")])], render_mode="html", confidence=0.2)
            tables.append(degraded)
    return tables
