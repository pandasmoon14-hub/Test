#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def normalize_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]

    normalized: list[str] = []
    blank_run = 0
    for line in lines:
        if not line.strip():
            blank_run += 1
            if blank_run <= 2:
                normalized.append("")
            continue
        blank_run = 0
        normalized.append(line)

    return "\n".join(normalized).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize markdown sourcebooks for Astra pipeline input.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8", errors="ignore")
    args.output.write_text(normalize_markdown(text), encoding="utf-8")


if __name__ == "__main__":
    main()
