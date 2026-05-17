from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_INCLUDES = ["*.md", "*.csv", "*.json", "*.txt"]
MOJIBAKE_TOKENS = [
    "â€“", "â€”", "â€¦", "â€˜", "â€™", "â€œ", "â€\x9d", "Ã¢â‚¬", "Ã¢â‚¬â€œ", "Ã¢â‚¬â€”", "Ã¢â‚¬Â", "Â", "�",
]
SOURCE_SECTION_HINTS = ["examples", "source-local examples", "donor examples", "extracted text", "source snippet"]
SOURCE_DERIVED_HINTS = [
    "source-local", "source_local", "donor", "retained", "rejected import", "doctrine escalation", "queue",
    "example", "packet_id", "construct", "rationale", "reviewer_notes", "conversion_notes", "text", "notes",
]
SOURCE_JSON_KEYS = {
    "donor_construct", "text", "rationale", "notes", "example", "examples", "source_local", "source-local",
    "retained construct", "rejected import", "doctrine escalation", "queue action", "canon candidate",
    "reviewer_notes", "conversion_notes",
}


def has_mojibake(s: str) -> str | None:
    for t in MOJIBAKE_TOKENS:
        if t in s:
            return t
    return None


def _is_source_section_heading(line: str) -> bool:
    l = line.strip().lower().lstrip("#").strip()
    return any(h in l for h in SOURCE_SECTION_HINTS)


def _is_generated_md_line(line: str) -> bool:
    l = line.strip().lower()
    if l.startswith("#"):
        return True
    if l.startswith("|") and ("---" in l or "status" in l or "count" in l):
        return True
    markers = ["confidence range", "packets total", "result status counts", "lawful outcome counts", "run summary", "report metadata"]
    return any(m in l for m in markers)


def _is_source_derived_line(line: str) -> bool:
    l = line.lower()
    return any(h in l for h in SOURCE_DERIVED_HINTS)


def _collect_files(path: Path, patterns: list[str]) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted([p for p in path.rglob("*") if p.is_file() and any(fnmatch.fnmatch(p.name, pat) for pat in patterns)])


def _classify_md_txt(lines: list[str], allow_source_examples: bool):
    out = []
    in_source = False
    for i, line in enumerate(lines, 1):
        tok = has_mojibake(line)
        if not tok:
            if line.strip().startswith("#"):
                in_source = _is_source_section_heading(line)
            continue
        if _is_generated_md_line(line):
            cls = "generated_scaffold_mojibake"
        elif in_source or (allow_source_examples and _is_source_derived_line(line)):
            cls = "likely_source_text_mojibake"
        else:
            cls = "ambiguous_mojibake"
        out.append((i, tok, cls, line[:240]))
    return out


def _classify_json(path: Path, allow_source_examples: bool):
    out = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    # key-level scan from raw lines
    for i, line in enumerate(text.splitlines(), 1):
        tok = has_mojibake(line)
        if not tok:
            continue
        stripped = line.strip()
        if stripped.startswith('"') and ':' in stripped:
            key = stripped.split(':', 1)[0].strip().strip('"').lower()
            if has_mojibake(key):
                cls = "generated_scaffold_mojibake"
            elif allow_source_examples and key in SOURCE_JSON_KEYS:
                cls = "likely_source_text_mojibake"
            else:
                cls = "ambiguous_mojibake"
        else:
            cls = "likely_source_text_mojibake" if (allow_source_examples and _is_source_derived_line(stripped)) else "ambiguous_mojibake"
        out.append((i, tok, cls, line[:240]))
    return out


def _classify_csv(path: Path, allow_source_examples: bool):
    out = []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    if not lines:
        return out
    headers = next(csv.reader([lines[0]]))
    for h in headers:
        tok = has_mojibake(h)
        if tok:
            out.append((1, tok, "generated_scaffold_mojibake", lines[0][:240]))
    for idx, line in enumerate(lines[1:], 2):
        tok = has_mojibake(line)
        if not tok:
            continue
        cls = "likely_source_text_mojibake" if allow_source_examples else "ambiguous_mojibake"
        out.append((idx, tok, cls, line[:240]))
    return out


def scan(target: Path, strict: bool, include: list[str], allow_source_examples: bool) -> dict[str, Any]:
    files = _collect_files(target, include or DEFAULT_INCLUDES)
    findings = []
    errors = []
    warnings = []

    for f in files:
        if f.suffix.lower() in {".md", ".txt"}:
            classified = _classify_md_txt(f.read_text(encoding="utf-8", errors="ignore").splitlines(), allow_source_examples)
        elif f.suffix.lower() == ".json":
            classified = _classify_json(f, allow_source_examples)
        elif f.suffix.lower() == ".csv":
            classified = _classify_csv(f, allow_source_examples)
        else:
            classified = []

        for line_no, tok, cls, preview in classified:
            findings.append({"file": str(f), "line": line_no, "token": tok, "classification": cls, "line_preview": preview})
            if strict:
                if cls == "generated_scaffold_mojibake":
                    errors.append(f"generated_scaffold_mojibake:{f}:{line_no}:{tok}")
                elif cls == "likely_source_text_mojibake":
                    if allow_source_examples:
                        warnings.append(f"likely_source_text_mojibake:{f}:{line_no}:{tok}")
                    else:
                        errors.append(f"likely_source_text_mojibake:{f}:{line_no}:{tok}")
                else:
                    errors.append(f"ambiguous_mojibake:{f}:{line_no}:{tok}")

    return {
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
