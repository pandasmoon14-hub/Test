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
    pages: dict[int, list[str]] = {}
    current = 1
    for line in markdown.splitlines():
        m = re.match(r"\s*<!--\s*PAGE:(\d+)\s*-->", line)
        if m:
            current = int(m.group(1))
            pages.setdefault(current, [])
            continue
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
        return 1.0
    divider = sum(1 for line in lines if re.search(r"\|\s*[-:]{3,}\s*\|", line))
    row_quality = sum(1 for line in lines if line.count("|") >= 2) / max(1, len(lines))
    divider_quality = min(1.0, divider / max(1, len(lines) * 0.25))
    return min(1.0, 0.65 * row_quality + 0.35 * divider_quality)


def statblock_integrity_score(text: str) -> float:
    keys = [
        "armor class",
        "hit points",
        "speed",
        "saving throws",
        "skills",
        "actions",
        "bonus actions",
        "spell slots",
        "dc",
    ]
    low = text.lower()
    hits = sum(1 for k in keys if k in low)
    if hits == 0:
        return 1.0
    separators = text.count("|") + len(re.findall(r"\n\s*[-*]\s+", text))
    return min(1.0, separators / max(1, hits * 2))


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


def page_score(text: str) -> tuple[float, list[str]]:
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

    ss = statblock_integrity_score(text)
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


def check_book(markdown_path: Path, manifest_path: Path) -> BookCheck:
    text = markdown_path.read_text(encoding="utf-8", errors="replace")
    pages = parse_page_markers(text)
    manifest = load_manifest(manifest_path)

    page_checks: list[PageCheck] = []
    for page_num in sorted(pages):
        score, issues = page_score(pages[page_num])
        page_checks.append(PageCheck(page=page_num, chars=len(pages[page_num]), issues=issues, score=score))

    issues: list[str] = []
    if not pages:
        issues.append("missing_pages")

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

    markdown_files = [p for p in sorted(md_root.glob(args.glob)) if p.is_file()]
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
