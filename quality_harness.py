#!/usr/bin/env python3
"""
Quality harness for Aether Forge corpus validation.

Runs offline checks against extracted markdown directories and manifests:
- page coverage consistency
- heading continuity
- table integrity
- stat-block integrity
- repeated header/footer leakage
- glyph corruption and soft-hyphen splits
- lane-level and donor-family metrics

The harness outputs a detailed JSON report for regression tracking.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from mechanics_vocab import best_family, statblock_density as vocab_statblock_density


@dataclass
class PageCheck:
    page: int
    chars: int
    issues: list[str]
    score: float


@dataclass
class BookCheck:
    book_id: str
    markdown_path: str
    manifest_path: str
    pages: int
    page_checks: list[PageCheck]
    issues: list[str]
    score: float
    lane: str
    donor_family: str


def parse_page_markers(markdown: str) -> dict[int, str]:
    marker_re = re.compile(r"\s*<!--\s*PAGE:(\d+)\s*-->")
    if not marker_re.search(markdown):
        return {}
    pages: dict[int, list[str]] = {}
    current: int | None = None
    for line in markdown.splitlines():
        m = marker_re.match(line)
        if m:
            current = int(m.group(1))
            pages.setdefault(current, [])
            continue
        if current is not None:
            pages.setdefault(current, []).append(line)
    return {p: "\n".join(lines).strip() for p, lines in pages.items()}


def heading_sequence_score(text: str) -> float:
    headings = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+", line.strip())
        if m:
            headings.append(len(m.group(1)))
    if len(headings) < 2:
        return 1.0
    jumps = 0
    for a, b in zip(headings, headings[1:]):
        if b - a > 1:
            jumps += 1
    return max(0.0, 1.0 - (jumps / len(headings)))


def table_integrity_score(text: str) -> float:
    lines = [line for line in text.splitlines() if "|" in line]
    if not lines:
        return 0.5
    divider = sum(1 for line in lines if re.search(r"\|\s*[-:]{3,}\s*\|", line))
    row_quality = sum(1 for line in lines if line.count("|") >= 2) / max(1, len(lines))
    divider_quality = min(1.0, divider / max(1, len(lines) * 0.25))
    return min(1.0, 0.65 * row_quality + 0.35 * divider_quality)


STATBLOCK_FIELDS: dict[str, list[str]] = {
    "cypher": ["motive:", "environment:", "health:", "damage inflicted:", "combat:", "interaction:", "use:", "gm intrusion:"],
    "d20": ["armor class", "hit points", "speed", "saving throws", "skills", "challenge"],
}


def statblock_integrity_score(text: str, donor_family: str = "") -> float:
    density = vocab_statblock_density(text)
    if density < 0.08:
        return 0.5
    family = donor_family or best_family(text).family
    fields = STATBLOCK_FIELDS.get(family, [])
    if not fields:
        fields = STATBLOCK_FIELDS.get(best_family(text).family, [])
    if not fields:
        return min(1.0, density + 0.3)
    low = text.lower()
    hits = sum(1 for field in fields if field in low)
    ordered = sum(1 for a, b in zip(fields, fields[1:]) if low.find(a) != -1 and low.find(b) != -1 and low.find(a) < low.find(b))
    return min(1.0, (hits * 0.7 + ordered * 0.3) / max(1, len(fields) * 0.6))


def reading_order_score(text: str) -> float:
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    if len(lines) < 5:
        return 1.0
    bad = 0
    for i in range(1, len(lines)):
        if lines[i].startswith("#") and len(lines[i - 1]) < 15 and not lines[i - 1].startswith("#"):
            bad += 1
    return max(0.0, 1.0 - bad / max(1, len(lines) / 12))


def header_footer_penalty(page_texts: dict[int, str]) -> float:
    firsts: dict[str, int] = {}
    lasts: dict[str, int] = {}
    for _, text in page_texts.items():
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        if not lines:
            continue
        firsts[lines[0]] = firsts.get(lines[0], 0) + 1
        lasts[lines[-1]] = lasts.get(lines[-1], 0) + 1

    total_pages = max(1, len(page_texts))
    worst = 0.0
    for count in list(firsts.values()) + list(lasts.values()):
        worst = max(worst, count / total_pages)
    if worst <= 0.4:
        return 0.0
    return min(0.4, worst - 0.4)


def glyph_penalty(text: str) -> float:
    penalties = 0.0
    if "\ufffd" in text:
        penalties += 0.2
    if re.search(r"archdev[^\w]?ils|conse[^\w]?quences", text, flags=re.IGNORECASE):
        penalties += 0.15
    controls = len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text))
    if controls > 0:
        penalties += min(0.2, controls / 200)
    return min(0.4, penalties)


def page_score(text: str, donor_family: str = "") -> tuple[float, list[str]]:
    issues = []

    chars = len(text)
    if chars < 120:
        issues.append("thin_output")

    hs = heading_sequence_score(text)
    if hs < 0.65:
        issues.append("heading_jump")

    ts = table_integrity_score(text)
    if ts < 0.5:
        issues.append("table_integrity")

    ss = statblock_integrity_score(text, donor_family=donor_family)
    if ss < 0.45:
        issues.append("statblock_integrity")

    ro = reading_order_score(text)
    if ro < 0.6:
        issues.append("reading_order")

    gp = glyph_penalty(text)
    if gp > 0.0:
        issues.append("glyph_issue")

    score = 1.0
    score -= (1.0 - hs) * 0.15
    score -= (1.0 - ts) * 0.25
    score -= (1.0 - ss) * 0.20
    score -= (1.0 - ro) * 0.25
    score -= gp
    if chars < 120:
        score -= 0.15

    return max(0.0, score), issues


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    if not manifest_path.exists():
        return {}
    with open(manifest_path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_book(markdown_path: Path, manifest_path: Path, pdf_path: Path | None = None) -> BookCheck:
    text = markdown_path.read_text(encoding="utf-8", errors="replace")
    pages = parse_page_markers(text)
    manifest = load_manifest(manifest_path)
    if manifest:
        try:
            import jsonschema  # type: ignore
            schema_dir = Path(__file__).parent / "schemas"
            manifest_schema = json.loads((schema_dir / "manifest.schema.json").read_text(encoding="utf-8"))
            jsonschema.validate(manifest, manifest_schema)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            manifest.setdefault("audit_signatures", [])
            manifest["audit_signatures"].append(f"schema_violation:{str(exc)[:80]}")
    page_metadata = []
    page_meta_path = Path(manifest.get("page_metadata_path", "")) if manifest else Path("")
    if page_meta_path and page_meta_path.exists():
        try:
            page_metadata = json.loads(page_meta_path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            page_metadata = []

    page_checks: list[PageCheck] = []
    for page_num in sorted(pages):
        score, issues = page_score(pages[page_num], donor_family=manifest.get("donor_family", ""))
        page_checks.append(PageCheck(page=page_num, chars=len(pages[page_num]), issues=issues, score=score))

    issues: list[str] = []
    if not pages:
        issues.append("missing_pages")
        issues.append("missing_page_truth")
        score = 0.0

    hfp = header_footer_penalty(pages)
    if hfp > 0.15:
        issues.append("header_footer_repeat")

    page_scores = [p.score for p in page_checks] or [0.0]
    score = max(0.0, statistics.mean(page_scores) - hfp)

    if score < 0.55:
        issues.append("book_quality_low")

    manifest_issues = manifest.get("audit_signatures", []) if manifest else []
    if manifest_issues:
        issues.extend([f"manifest:{x}" for x in manifest_issues])

    table_miss_pages = []
    for pm in page_metadata:
        page_num = int(pm.get("page", 0) or 0)
        if page_num <= 0:
            continue
        src_table_signal = float(pm.get("detected_tables", 0.0) or 0.0)
        md_page = pages.get(page_num, "")
        pipe_rows = sum(1 for ln in md_page.splitlines() if ln.count("|") >= 2)
        if src_table_signal > 0.15 and pipe_rows < 2:
            table_miss_pages.append(page_num)
    if table_miss_pages:
        issues.append("vector_table_miss")
    form_routed_as_prose = []
    rotated_without_normalization = []
    complex_missing_sidecar = []
    for pm in page_metadata:
        page_num = int(pm.get("page", 0) or 0)
        modality = str(pm.get("modality", ""))
        repair_path = str(pm.get("repair_path", ""))
        if modality == "form" and "form" not in repair_path:
            form_routed_as_prose.append(page_num)
        if str(pm.get("orientation", "")) in {"rotated", "landscape"} and str(pm.get("normalization_applied", "none")) == "none":
            rotated_without_normalization.append(page_num)
        if modality == "table" and pm.get("table_complex_detected") and not pm.get("table_sidecar_refs"):
            complex_missing_sidecar.append(page_num)
    if form_routed_as_prose:
        issues.append("form_routed_through_prose")
    if rotated_without_normalization:
        issues.append("rotation_not_normalized")
    if complex_missing_sidecar:
        issues.append("complex_table_missing_sidecar")
    if pdf_path and pdf_path.exists():
        try:
            import fitz
            from orchestrator import vector_table_density
            by_page = {pc.page: pc for pc in page_checks}
            with fitz.open(pdf_path) as doc:
                for page_num in sorted(pages):
                    if 0 <= page_num - 1 < len(doc):
                        vt = vector_table_density(doc[page_num - 1])
                        pipe_rows = sum(1 for ln in pages[page_num].splitlines() if ln.count("|") >= 2)
                        if vt > 0.3 and pipe_rows < 2:
                            issues.append("vector_table_miss")
                            if page_num in by_page:
                                by_page[page_num].issues.append("vector_table_miss")
        except Exception:
            pass
    page_marker_mode = str(manifest.get("page_marker_mode", ""))
    if page_marker_mode in {"chunk_fallback", "native_or_fallback"}:
        score = 0.0
        issues.append("untrusted_page_truth")
    elif page_marker_mode and any(x in page_marker_mode.lower() for x in ("fallback", "synthetic", "untrusted")):
        score = 0.0
        issues.append("untrusted_page_truth")

    return BookCheck(
        book_id=markdown_path.stem,
        markdown_path=str(markdown_path),
        manifest_path=str(manifest_path),
        pages=len(pages),
        page_checks=page_checks,
        issues=sorted(set(issues)),
        score=round(score, 4),
        lane=manifest.get("lane", "unknown") if manifest else "unknown",
        donor_family=manifest.get("donor_family", "unknown") if manifest else "unknown",
    )


def aggregate(books: list[BookCheck]) -> dict[str, Any]:
    if not books:
        return {
            "books": 0,
            "avg_score": 0.0,
            "p50_score": 0.0,
            "p90_score": 0.0,
            "books_below_0_6": 0,
            "lane_distribution": {},
            "donor_distribution": {},
            "issue_counts": {},
        }

    scores = sorted([b.score for b in books])
    issue_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    donor_counts: dict[str, int] = {}

    for b in books:
        lane_counts[b.lane] = lane_counts.get(b.lane, 0) + 1
        donor_counts[b.donor_family] = donor_counts.get(b.donor_family, 0) + 1
        for issue in b.issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1

    def percentile(values: list[float], pct: float) -> float:
        if not values:
            return 0.0
        idx = int((len(values) - 1) * pct)
        return values[idx]

    return {
        "books": len(books),
        "avg_score": round(statistics.mean(scores), 4),
        "p50_score": round(percentile(scores, 0.5), 4),
        "p90_score": round(percentile(scores, 0.9), 4),
        "books_below_0_6": sum(1 for s in scores if s < 0.6),
        "lane_distribution": lane_counts,
        "donor_distribution": donor_counts,
        "issue_counts": issue_counts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aether Forge quality harness")
    parser.add_argument("--markdown_root", required=True)
    parser.add_argument("--manifest_root", required=True)
    parser.add_argument("--glob", default="**/*.md")
    parser.add_argument("--report", required=True)
    parser.add_argument("--fail_below", type=float, default=0.55)
    parser.add_argument("--max_books", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    md_root = Path(args.markdown_root)
    manifest_root = Path(args.manifest_root)

    markdown_files = [
        p for p in sorted(md_root.glob(args.glob))
        if p.is_file() and "_chunk_" not in p.name and "_dchunk_" not in p.name and not p.name.endswith(".repair.tmp.md")
    ]
    if args.max_books > 0:
        markdown_files = markdown_files[: args.max_books]

    books: list[BookCheck] = []
    for md in markdown_files:
        manifest = manifest_root / f"{md.stem}.manifest.json"
        books.append(check_book(md, manifest))

    summary = aggregate(books)
    payload = {
        "summary": summary,
        "books": [
            {
                **asdict(b),
                "page_checks": [asdict(p) for p in b.page_checks],
            }
            for b in books
        ],
    }

    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    fail_count = sum(1 for b in books if b.score < args.fail_below)
    print(json.dumps({"report": str(report), "books": len(books), "below_threshold": fail_count}, indent=2))

    if fail_count > 0:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
