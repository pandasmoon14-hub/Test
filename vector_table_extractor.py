#!/usr/bin/env python3
"""Minimal vector table extraction scaffold."""
from __future__ import annotations
from typing import Any

try:
    import fitz
except Exception:  # pragma: no cover
    fitz = Any  # type: ignore

def extract_vector_tables(page: fitz.Page) -> list[fitz.Rect]:
    tables = []
    try:
        found = page.find_tables()
        for t in getattr(found, "tables", []):
            if getattr(t, "bbox", None):
                tables.append(fitz.Rect(t.bbox))
    except Exception:
        return []
    return tables
