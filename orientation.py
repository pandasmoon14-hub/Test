#!/usr/bin/env python3
"""Orientation helpers."""
from __future__ import annotations
import fitz

def orientation_from_page(page: fitz.Page) -> str:
    rot = int(getattr(page, "rotation", 0) or 0) % 360
    if rot in (90, 270):
        return "rotated"
    return "landscape" if page.rect.width > page.rect.height else "portrait"


def normalization_action(page: fitz.Page) -> str:
    mode = orientation_from_page(page)
    if mode == "rotated":
        return "rotate_to_upright"
    if mode == "landscape":
        return "rotate_landscape_to_portrait"
    return "none"
