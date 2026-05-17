from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_INCLUDES = ["*.md", "*.csv", "*.json", "*.txt"]
MOJIBAKE_TOKENS = [
    "â€“",
    "â€”",
    "â€¦",
    "â€˜",
    "â€™",
    "â€œ",
    "â€\x9d",
    "Ã¢â‚¬",
    "Ã¢â‚¬â€œ",
    "Ã¢â‚¬â€”",
    "Ã¢â‚¬Â",
    "Â",
    "�",
]
SOURCE_SECTION_HINTS = [
    "examples",
    "source-local examples",
    "donor examples",
    "extracted text",
    "source snippet",
]


def _looks_generated_zone(line: str) -> bool:
    l = line.strip().lower()
    if not l:
        return False
    if l.startswith("#"):
        return True
    if l.startswith("- ") or l.startswith("* "):
        return True
    if "|" in l and ("---" in l or "count" in l or "status" in l):
        return True
    markers = [
        "confidence",
        "status",
        "count",
        "summary",
        "report",
        "generated",
        "packets_total",
        "result_status_counts",
        "lawful_outcome_counts",
    ]
    return any(m in l for m in markers)


def _is_source_section_heading(line: str) -> bool:
    l = line.strip().lower().lstrip("#").strip()
    return any(h in l for h in SOURCE_SECTION_HINTS)


def _collect_files(path: Path, patterns: list[str]) -> list[Path]:
    if path.is_file():
        return [path]
    out: list[Path] = []
    for p in path.rglob("*"):
        if p.is_file() and any(fnmatch.fnmatch(p.name, pat) for pat in patterns):
            out.append(p)
    return sorted(out)


def scan(target: Path, strict: bool, include: list[str], allow_source_examples: bool) -> dict[str, Any]:
    findings = []
    errors = []
    warnings = []

    files = _collect_files(target, include or DEFAULT_INCLUDES)

    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        in_source_zone = False
        for i, line in enumerate(lines, start=1):
            if _is_source_section_heading(line):
                in_source_zone = True
            if line.strip().startswith("#") and not _is_source_section_heading(line):
                in_source_zone = False

            for tok in MOJIBAKE_TOKENS:
                if tok in line:
                    if _looks_generated_zone(line):
                        cls = "generated_scaffold_mojibake"
                    elif in_source_zone:
                        cls = "likely_source_text_mojibake"
                    else:
                        cls = "ambiguous_mojibake"

                    rec = {
                        "file": str(f),
                        "line": i,
                        "token": tok,
                        "classification": cls,
                        "line_preview": line[:240],
                    }
                    findings.append(rec)

                    if strict:
                        if cls == "generated_scaffold_mojibake":
                            errors.append(f"generated_scaffold_mojibake:{f}:{i}:{tok}")
                        elif cls == "likely_source_text_mojibake":
                            if allow_source_examples:
                                warnings.append(f"likely_source_text_mojibake:{f}:{i}:{tok}")
                            else:
                                errors.append(f"likely_source_text_mojibake:{f}:{i}:{tok}")
                        else:  # ambiguous
                            if allow_source_examples and in_source_zone:
                                warnings.append(f"ambiguous_mojibake_source_zone:{f}:{i}:{tok}")
                            else:
                                errors.append(f"ambiguous_mojibake:{f}:{i}:{tok}")

    report = {
        "valid": len(errors) == 0,
        "strict": strict,
        "path": str(target),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "files_scanned": len(files),
        "finding_count": len(findings),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "findings": findings,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "includes": include or DEFAULT_INCLUDES,
            "allow_source_examples": allow_source_examples,
            "classification_counts": {
                "generated_scaffold_mojibake": sum(1 for f in findings if f["classification"] == "generated_scaffold_mojibake"),
                "likely_source_text_mojibake": sum(1 for f in findings if f["classification"] == "likely_source_text_mojibake"),
                "ambiguous_mojibake": sum(1 for f in findings if f["classification"] == "ambiguous_mojibake"),
            },
        },
    }
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--output-json")
    ap.add_argument("--include", nargs="*")
    ap.add_argument("--allow-source-examples", action="store_true")
    args = ap.parse_args()

    report = scan(Path(args.path), bool(args.strict), args.include or DEFAULT_INCLUDES, bool(args.allow_source_examples))
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    print(payload)
    if args.output_json:
        Path(args.output_json).write_text(payload + "\n", encoding="utf-8")

    if args.strict and not report["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
