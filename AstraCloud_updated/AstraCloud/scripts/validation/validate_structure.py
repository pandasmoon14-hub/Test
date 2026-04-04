#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def validate_structure(source_text: str, converted_text: str) -> dict[str, object]:
    source_headings = re.findall(r"^#{1,6}\s+.+$", source_text, flags=re.M)
    converted_headings = re.findall(r"^#{1,6}\s+.+$", converted_text, flags=re.M)
    source_tables = len(re.findall(r"^\s*\|.+\|\s*$", source_text, flags=re.M))
    converted_tables = len(re.findall(r"^\s*\|.+\|\s*$", converted_text, flags=re.M))

    heading_ratio = 1.0 if not source_headings else min(len(converted_headings) / len(source_headings), 1.0)
    table_ratio = 1.0 if source_tables == 0 else min(converted_tables / source_tables, 1.0)
    passed = heading_ratio >= 0.5 and table_ratio >= 0.5

    return {
        "passed": passed,
        "source_heading_count": len(source_headings),
        "converted_heading_count": len(converted_headings),
        "source_table_row_count": source_tables,
        "converted_table_row_count": converted_tables,
        "heading_ratio": round(heading_ratio, 3),
        "table_ratio": round(table_ratio, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate structural preservation between source and converted markdown.")
    parser.add_argument("source", type=Path)
    parser.add_argument("converted", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    source_text = args.source.read_text(encoding="utf-8", errors="ignore")
    converted_text = args.converted.read_text(encoding="utf-8", errors="ignore")
    result = validate_structure(source_text, converted_text)
    args.output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
