#!/usr/bin/env python3
"""Corpus-scale layout analyzer for calibrating Aether Forge routing heuristics.

Designed for 500-600+ PDF corpora. Produces a calibration JSON that can be fed
into orchestrator via LAYOUT_PROFILE_PATH.
"""

from __future__ import annotations

import argparse
import json
import sys
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path

import fitz

from layout_utils import detect_multicolumn, detect_statblock_density, detect_table_density, vector_table_density


@dataclass
class BookLayout:
    file: str
    pages: int
    sampled_pages: int
    multicol_ratio: float
    table_ratio: float
    stat_ratio: float
    scanned_ratio: float


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    arr = sorted(values)
    idx = max(0, min(len(arr) - 1, int((len(arr) - 1) * q)))
    return float(arr[idx])


def analyze_pdf(pdf: Path, sample_interval: int) -> BookLayout:
    try:
        with fitz.open(pdf) as doc:
            total = len(doc)
            sample_idxs = list(range(0, total, max(1, sample_interval))) or [0]

            multicol = 0
            tableish = 0
            statish = 0
            scanned = 0

            for idx in sample_idxs:
                page = doc[idx]
                text = page.get_text("text")
                blocks = page.get_text("blocks")
                if detect_multicolumn(blocks):
                    multicol += 1
                if max(detect_table_density(text), vector_table_density(page)) >= 0.15:
                    tableish += 1
                if detect_statblock_density(text) >= 0.30:
                    statish += 1
                if len(text.strip()) < 50:
                    scanned += 1
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(f"Error analyzing {pdf}: {exc}", file=sys.stderr)
        return BookLayout(str(pdf), 0, 0, 0.0, 0.0, 0.0, 0.0)

    n = max(1, len(sample_idxs))
    return BookLayout(
        file=str(pdf),
        pages=total,
        sampled_pages=len(sample_idxs),
        multicol_ratio=round(multicol / n, 4),
        table_ratio=round(tableish / n, 4),
        stat_ratio=round(statish / n, 4),
        scanned_ratio=round(scanned / n, 4),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze corpus layout profile for orchestrator calibration")
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--glob", default="*.pdf")
    parser.add_argument("--max_books", type=int, default=0)
    parser.add_argument("--sample_interval", type=int, default=8)
    parser.add_argument("--report", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    pdfs = [p for p in sorted(input_dir.glob(args.glob)) if p.is_file()]
    if args.max_books > 0:
        pdfs = pdfs[: args.max_books]

    books = [analyze_pdf(pdf, args.sample_interval) for pdf in pdfs]

    multicol = [b.multicol_ratio for b in books]
    tables = [b.table_ratio for b in books]
    stats = [b.stat_ratio for b in books]

    recommended = {
        "lane_a_multicol_penalty": round(2.2 if percentile(multicol, 0.75) > 0.45 else 1.8, 3),
        "lane_a_hard_exclusion_multicol": round(max(0.45, percentile(multicol, 0.8) if multicol else 0.5), 3),
        "table_ratio_threshold": round(max(0.10, percentile(tables, 0.25)), 3),
        "stat_ratio_threshold": round(max(0.20, percentile(stats, 0.25)), 3),
    }

    summary = {
        "books": len(books),
        "pages_total": int(sum(b.pages for b in books)),
        "multicol_ratio_p50": round(percentile(multicol, 0.5), 4),
        "multicol_ratio_p90": round(percentile(multicol, 0.9), 4),
        "table_ratio_p50": round(percentile(tables, 0.5), 4),
        "stat_ratio_p50": round(percentile(stats, 0.5), 4),
        "recommended": recommended,
    }

    payload = {
        "summary": summary,
        "recommended": recommended,
        "books": [asdict(b) for b in books],
    }

    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
