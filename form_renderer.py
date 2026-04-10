#!/usr/bin/env python3
"""Minimal renderer for form/worksheet-like pages."""
from __future__ import annotations

def render_form_like(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines()]
    return "\n".join(lines)
