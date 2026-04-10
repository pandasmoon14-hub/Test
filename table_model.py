#!/usr/bin/env python3
"""Structured table model for sidecar-first rendering."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class TableCell:
    text: str
    colspan: int = 1
    rowspan: int = 1

@dataclass
class TableRow:
    cells: list[TableCell]

@dataclass
class TableSidecar:
    page: int | None
    bbox: list[float] | None
    rows: list[TableRow]
    render_mode: str = "markdown"
    confidence: float = 0.5
    continuation: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
