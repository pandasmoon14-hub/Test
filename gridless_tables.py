#!/usr/bin/env python3
"""Minimal aligned-column detection for gridless tables."""
from __future__ import annotations
import re

def detect_gridless_rows(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if len(re.findall(r"\s{3,}", ln)) >= 2]
