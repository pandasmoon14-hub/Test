#!/usr/bin/env python3
"""Data-driven acceptance scanner for Aether Forge markdown outputs."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from mechanics_vocab import best_family, mechanics_hits, statblock_density


@dataclass(frozen=True)
class RuleDef:
    rule_id: str
    label: str
    weight: float


@dataclass
class RuleResult:
    rule: str
    passed: bool
    value: float
    threshold: float
    detail: str
    weight: float


BASE_RULES: tuple[RuleDef, ...] = (
    RuleDef("page_markers", "page markers present", 1.2),
    RuleDef("glyph_clean", "glyph cleanliness", 1.0),
    RuleDef("reading_order", "reading-order continuity", 1.1),
    RuleDef("heading_flow", "heading hierarchy continuity", 0.9),
    RuleDef("table_signal", "table retention signal", 1.0),
    RuleDef("table_structure", "table structural integrity", 1.1),
    RuleDef("statblock_signal", "stat-block signal", 1.2),
    RuleDef("content_density", "content density", 0.8),
    RuleDef("list_continuity", "list continuity", 0.7),
    RuleDef("duplicate_para", "duplicate paragraph leakage", 0.7),
)

ASTRA_TERMS = ("dao", "tier", "astra-well", "heartbeat", "friction", "epiphany", "dao-vein")


def parse_pages(markdown: str) -> dict[int, str]:
    pages: dict[int, list[str]] = {}
    current = 1
    for line in markdown.splitlines():
        marker = re.match(r"\s*<!--\s*PAGE:(\d+)\s*-->", line)
        if marker:
            current = int(marker.group(1))
            pages.setdefault(current, [])
            continue
        pages.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in pages.items()}


def score_page_markers(text: str) -> tuple[float, float, str]:
    count = len(re.findall(r"<!--\s*PAGE:\d+\s*-->", text))
    if count > 0:
        return 1.0, 1.0, f"markers={count}"
    return 0.0, 1.0, "no page markers"


def score_glyph_clean(text: str) -> tuple[float, float, str]:
    bad = len(re.findall(r"\ufffd|[\x00-\x08\x0b\x0c\x0e-\x1f]", text))
    score = max(0.0, 1.0 - (bad / max(1, len(text) / 1200)))
    return score, 0.9, f"bad_chars={bad}"


def score_reading_order(text: str) -> tuple[float, float, str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    jumps = 0
    for a, b in zip(lines, lines[1:]):
        if b.startswith("#") and not a.startswith("#") and len(a) < 18:
            jumps += 1
    score = max(0.0, 1.0 - jumps / max(1, len(lines) / 8))
    return score, 0.62, f"heading_jumps={jumps}"


def score_heading_flow(text: str) -> tuple[float, float, str]:
    levels = [len(m.group(1)) for line in text.splitlines() if (m := re.match(r"^(#{1,6})\s+", line.strip()))]
    if len(levels) < 2:
        return 0.7, 0.4, "insufficient headings"
    bad = sum(1 for a, b in zip(levels, levels[1:]) if b - a > 1)
    score = max(0.0, 1.0 - bad / len(levels))
    return score, 0.6, f"level_jumps={bad}"


def score_table_signal(text: str) -> tuple[float, float, str]:
    pipes = sum(1 for ln in text.splitlines() if ln.count("|") >= 2)
    spaced_cols = len(re.findall(r"\S\s{3,}\S", text))
    score = min(1.0, (pipes / 8.0) + (spaced_cols / 20.0))
    return score, 0.2, f"pipe_rows={pipes}, spaced_cols={spaced_cols}"


def score_table_structure(text: str) -> tuple[float, float, str]:
    rows = [ln for ln in text.splitlines() if "|" in ln]
    if not rows:
        return 0.5, 0.25, "no explicit table rows"
    valid = sum(1 for ln in rows if ln.count("|") >= 2)
    dividers = sum(1 for ln in rows if re.search(r"\|\s*[-:]{3,}\s*\|", ln))
    score = min(1.0, (valid / len(rows)) * 0.7 + min(1.0, dividers / max(1, len(rows) * 0.25)) * 0.3)
    return score, 0.45, f"valid={valid}, dividers={dividers}, total={len(rows)}"


def score_statblock_signal(text: str) -> tuple[float, float, str]:
    density = statblock_density(text)
    family = best_family(text)
    astra_hits = sum(1 for t in ASTRA_TERMS if t in text.lower())
    score = min(1.0, density + min(0.3, astra_hits * 0.05))
    return score, 0.25, f"density={density:.3f}, family={family.family}:{family.hits}, astra_hits={astra_hits}"


def score_content_density(text: str) -> tuple[float, float, str]:
    blocks = [b for b in re.split(r"\n\n+", text) if b.strip()]
    long_blocks = sum(1 for b in blocks if len(b) > 140)
    score = long_blocks / max(1, len(blocks))
    return score, 0.2, f"long_blocks={long_blocks}/{len(blocks)}"


def score_list_continuity(text: str) -> tuple[float, float, str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullets = [ln for ln in lines if re.match(r"^[-*]\s+", ln)]
    if not bullets:
        return 0.6, 0.3, "no bullet lists"
    broken = sum(1 for ln in bullets if len(ln.split()) < 2)
    score = max(0.0, 1.0 - broken / max(1, len(bullets)))
    return score, 0.75, f"broken_bullets={broken}/{len(bullets)}"


def score_duplicate_para(text: str) -> tuple[float, float, str]:
    blocks = [re.sub(r"\s+", " ", b.strip()) for b in re.split(r"\n\n+", text) if len(b.strip()) > 80]
    seen = set()
    dup = 0
    for b in blocks:
        if b in seen:
            dup += 1
        seen.add(b)
    score = max(0.0, 1.0 - dup / max(1, len(blocks)))
    return score, 0.85, f"duplicates={dup}/{len(blocks)}"


SCORERS = {
    "page_markers": score_page_markers,
    "glyph_clean": score_glyph_clean,
    "reading_order": score_reading_order,
    "heading_flow": score_heading_flow,
    "table_signal": score_table_signal,
    "table_structure": score_table_structure,
    "statblock_signal": score_statblock_signal,
    "content_density": score_content_density,
    "list_continuity": score_list_continuity,
    "duplicate_para": score_duplicate_para,
}


def evaluate_text(text: str) -> tuple[float, list[RuleResult]]:
    results: list[RuleResult] = []
    total_weight = 0.0
    achieved = 0.0

    for rule in BASE_RULES:
        value, threshold, detail = SCORERS[rule.rule_id](text)
        passed = value >= threshold
        results.append(RuleResult(rule.rule_id, passed, round(value, 4), threshold, detail, rule.weight))
        total_weight += rule.weight
        achieved += rule.weight * max(0.0, min(1.0, value))

    score = achieved / max(1e-6, total_weight)
    return round(score, 4), results


def scan_file(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    weighted_score, rules = evaluate_text(text)
    pages = parse_pages(text)
    failed = [r.rule for r in rules if not r.passed]
    family = best_family(text).family
    family_hits = mechanics_hits(text)
    return {
        "file": str(path),
        "pages": len(pages),
        "weighted_score": weighted_score,
        "failed_rule_ids": failed,
        "top_family": family,
        "family_hits": family_hits,
        "rules": [asdict(r) for r in rules],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data-driven acceptance scanner")
    parser.add_argument("--input", required=True, help="Markdown file or directory")
    parser.add_argument("--glob", default="**/*.md")
    parser.add_argument("--report", default="")
    parser.add_argument("--fail_below", type=float, default=0.62)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inp = Path(args.input)
    targets = [inp] if inp.is_file() else [p for p in sorted(inp.glob(args.glob)) if p.is_file() and "_chunk_" not in p.name and "_dchunk_" not in p.name]

    scanned = [scan_file(path) for path in targets]
    avg = round(sum(item["weighted_score"] for item in scanned) / max(1, len(scanned)), 4)
    below = [item for item in scanned if item["weighted_score"] < args.fail_below]

    payload = {
        "summary": {
            "files": len(scanned),
            "avg_weighted_score": avg,
            "below_threshold": len(below),
            "threshold": args.fail_below,
        },
        "files": scanned,
    }

    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(payload["summary"], indent=2))
    if below:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
