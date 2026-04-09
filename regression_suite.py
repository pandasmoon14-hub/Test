#!/usr/bin/env python3
"""
Regression suite for Aether Forge quality checks.

Creates synthetic markdown fixtures that mimic TTRPG failure modes and validates
core quality tooling behaviors without requiring heavyweight model inference.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path

from table_fixer import apply_fixes
from quality_harness import (
    heading_sequence_score,
    table_integrity_score,
    statblock_integrity_score,
    reading_order_score,
    parse_page_markers,
)
from mechanics_vocab import best_family, statblock_density


@dataclass
class TestResult:
    name: str
    passed: bool
    detail: str


def fixture_good_table() -> str:
    return """
<!-- PAGE:1 -->
# Monster Stats
| Name | AC | HP |
| --- | --- | --- |
| Goblin | 15 | 7 |
| Ogre | 11 | 59 |
""".strip()


def fixture_broken_table_no_divider() -> str:
    return """
<!-- PAGE:1 -->
# Monster Stats
| Name | AC | HP |
| Goblin | 15 | 7 |
| Ogre | 11 | 59 |
""".strip()


def fixture_pseudo_table() -> str:
    return """
<!-- PAGE:1 -->
Name    AC    HP
Goblin  15    7
Ogre    11    59
""".strip()


def fixture_heading_jump() -> str:
    return """
<!-- PAGE:1 -->
# Chapter 1
Some intro.
#### Deep Heading Too Early
Content.
""".strip()


def fixture_reading_order_issue() -> str:
    return """
<!-- PAGE:1 -->
paragraph
# heading
text
# heading2
text
""".strip()


def fixture_stat_block_good() -> str:
    return """
<!-- PAGE:1 -->
# Goblin
- Armor Class: 15
- Hit Points: 7
- Speed: 30 ft.
- Actions: Scimitar.
""".strip()


def fixture_stat_block_bad() -> str:
    return """
<!-- PAGE:1 -->
# Goblin
Armor Class 15 Hit Points 7 Speed 30 Actions Scimitar
""".strip()


def fixture_whog_statblock() -> str:
    return """
<!-- PAGE:1 -->
# Iron Disciple
Defenses: Hardiness 5, Evade 6, Parry 6
Qi: 2
Max Wounds: 5
Key Techniques: Biting Blade
""".strip()


def fixture_shadowrun_statblock() -> str:
    return """
<!-- PAGE:1 -->
# Street Samurai
Dice Pool: 12
Edge: 3
Initiative Score: 10+2d6
Condition Monitor: 10
""".strip()


def fixture_page_markers() -> str:
    return """
<!-- PAGE:1 -->
Alpha
<!-- PAGE:2 -->
Beta
<!-- PAGE:3 -->
Gamma
""".strip()


def test_table_integrity_good() -> TestResult:
    val = table_integrity_score(fixture_good_table())
    return TestResult("table_integrity_good", val > 0.8, f"score={val:.3f}")


def test_table_integrity_bad() -> TestResult:
    val = table_integrity_score(fixture_broken_table_no_divider())
    return TestResult("table_integrity_bad", val < 0.8, f"score={val:.3f}")


def test_table_fixer_adds_divider() -> TestResult:
    fixed, stats = apply_fixes(fixture_broken_table_no_divider())
    passed = "| --- | --- | --- |" in fixed and stats["separators_added"] >= 1
    return TestResult("table_fixer_adds_divider", passed, json.dumps(stats))


def test_table_fixer_promotes_pseudo() -> TestResult:
    fixed, stats = apply_fixes(fixture_pseudo_table())
    passed = fixed.count("|") > 6 and stats["pseudo_tables_promoted"] >= 2
    return TestResult("table_fixer_promotes_pseudo", passed, json.dumps(stats))


def test_heading_sequence_jump() -> TestResult:
    val = heading_sequence_score(fixture_heading_jump())
    return TestResult("heading_sequence_jump", val < 0.8, f"score={val:.3f}")


def test_reading_order_signal() -> TestResult:
    val = reading_order_score(fixture_reading_order_issue())
    return TestResult("reading_order_signal", val < 0.9, f"score={val:.3f}")


def test_statblock_good() -> TestResult:
    val = statblock_integrity_score(fixture_stat_block_good())
    return TestResult("statblock_good", val > 0.45, f"score={val:.3f}")


def test_statblock_bad() -> TestResult:
    val = statblock_integrity_score(fixture_stat_block_bad())
    return TestResult("statblock_bad", val < 0.7, f"score={val:.3f}")


def test_vocab_whog() -> TestResult:
    fam = best_family(fixture_whog_statblock())
    dens = statblock_density(fixture_whog_statblock())
    return TestResult("vocab_whog", fam.family == "whog" and dens > 0.3, f"family={fam.family}, density={dens:.3f}")


def test_vocab_shadowrun() -> TestResult:
    fam = best_family(fixture_shadowrun_statblock())
    return TestResult("vocab_shadowrun", fam.family == "shadowrun", f"family={fam.family}")


def test_page_marker_parser() -> TestResult:
    pages = parse_page_markers(fixture_page_markers())
    passed = sorted(pages.keys()) == [1, 2, 3] and pages[2].strip() == "Beta"
    return TestResult("page_marker_parser", passed, f"keys={sorted(pages.keys())}")


def test_table_fixer_idempotent() -> TestResult:
    text = fixture_good_table()
    fixed, _ = apply_fixes(text)
    fixed2, _ = apply_fixes(fixed)
    return TestResult("table_fixer_idempotent", fixed == fixed2, "idempotent check")


def test_table_fixer_padding() -> TestResult:
    text = """
<!-- PAGE:1 -->
| A | B | C |
| --- | --- | --- |
| 1 | 2 |
""".strip()
    fixed, stats = apply_fixes(text)
    passed = "| 1 | 2 |  |" in fixed and stats["rows_padded"] >= 1
    return TestResult("table_fixer_padding", passed, json.dumps(stats))


def test_table_fixer_leading_trailing_pipe() -> TestResult:
    text = """
<!-- PAGE:1 -->
A | B | C
1 | 2 | 3
""".strip()
    fixed, _ = apply_fixes(text)
    passed = "| A | B | C |" in fixed
    return TestResult("table_fixer_leading_trailing_pipe", passed, "normalized")


def test_table_fixer_escape_pipes() -> TestResult:
    text = """
<!-- PAGE:1 -->
| Name | Effect |
| --- | --- |
| Wand | fire|ice |
""".strip()
    fixed, _ = apply_fixes(text)
    passed = "Wand" in fixed and "Effect" in fixed
    return TestResult("table_fixer_escape_pipes", passed, "escape check")


def test_markers_survive_fix() -> TestResult:
    text = fixture_broken_table_no_divider()
    fixed, _ = apply_fixes(text)
    passed = "<!-- PAGE:1 -->" in fixed
    return TestResult("markers_survive_fix", passed, "marker retained")


def test_multi_block_table_fix() -> TestResult:
    text = """
<!-- PAGE:1 -->
| A | B |
| 1 | 2 |

text

| X | Y |
| alpha | beta |
""".strip()
    fixed, stats = apply_fixes(text)
    passed = fixed.count("| --- |") >= 2 and stats["tables_seen"] >= 2
    return TestResult("multi_block_table_fix", passed, json.dumps(stats))


def test_empty_input() -> TestResult:
    fixed, stats = apply_fixes("")
    passed = fixed == "" and stats["tables_seen"] == 0
    return TestResult("empty_input", passed, json.dumps(stats))


def test_single_line_non_table() -> TestResult:
    fixed, stats = apply_fixes("hello world")
    passed = fixed == "hello world" and stats["tables_seen"] == 0
    return TestResult("single_line_non_table", passed, json.dumps(stats))


def test_whitespace_columns_detection() -> TestResult:
    text = "A   B   C\n1   2   3"
    fixed, stats = apply_fixes(text)
    passed = stats["pseudo_tables_promoted"] >= 2
    return TestResult("whitespace_columns_detection", passed, json.dumps(stats))


def test_long_table() -> TestResult:
    rows = ["| col1 | col2 | col3 |"]
    for i in range(20):
        rows.append(f"| a{i} | b{i} | c{i} |")
    text = "\n".join(rows)
    fixed, stats = apply_fixes(text)
    passed = stats["tables_seen"] >= 1 and "| --- | --- | --- |" in fixed
    return TestResult("long_table", passed, json.dumps(stats))


def test_mixed_content() -> TestResult:
    text = """
# Chapter
Some prose.
A   B   C
1   2   3
More prose.
""".strip()
    fixed, stats = apply_fixes(text)
    passed = "| A | B | C |" in fixed and "More prose." in fixed
    return TestResult("mixed_content", passed, json.dumps(stats))


def test_heading_preservation() -> TestResult:
    text = """
# Heading
| A | B |
| 1 | 2 |
""".strip()
    fixed, _ = apply_fixes(text)
    passed = fixed.splitlines()[0].startswith("# Heading")
    return TestResult("heading_preservation", passed, "header intact")


def test_utf8_preservation() -> TestResult:
    text = """
| Name | Effect |
| --- | --- |
| Æther | brûlée |
""".strip()
    fixed, _ = apply_fixes(text)
    passed = "Æther" in fixed and "brûlée" in fixed
    return TestResult("utf8_preservation", passed, "utf8 intact")


def test_marker_multpage() -> TestResult:
    text = """
<!-- PAGE:1 -->
| A | B |
| 1 | 2 |
<!-- PAGE:2 -->
| X | Y |
| 3 | 4 |
""".strip()
    fixed, _ = apply_fixes(text)
    pages = parse_page_markers(fixed)
    passed = 1 in pages and 2 in pages
    return TestResult("marker_multpage", passed, f"pages={sorted(pages.keys())}")


def test_score_functions_stability() -> TestResult:
    text = fixture_good_table()
    vals = [
        heading_sequence_score(text),
        table_integrity_score(text),
        statblock_integrity_score(text),
        reading_order_score(text),
    ]
    passed = all(0.0 <= v <= 1.0 for v in vals)
    return TestResult("score_functions_stability", passed, f"vals={vals}")


def test_stat_block_with_table() -> TestResult:
    text = """
# Orc
| Key | Value |
| --- | --- |
| Armor Class | 13 |
| Hit Points | 15 |
""".strip()
    val = statblock_integrity_score(text)
    return TestResult("stat_block_with_table", val > 0.7, f"score={val:.3f}")


def test_regression_snapshot(tmp: Path) -> TestResult:
    text = fixture_broken_table_no_divider()
    fixed, _ = apply_fixes(text)
    snap = tmp / "snapshot.md"
    snap.write_text(fixed, encoding="utf-8")
    loaded = snap.read_text(encoding="utf-8")
    return TestResult("regression_snapshot", loaded == fixed, "roundtrip")


def run_all(tmp: Path) -> list[TestResult]:
    results = [
        test_table_integrity_good(),
        test_table_integrity_bad(),
        test_table_fixer_adds_divider(),
        test_table_fixer_promotes_pseudo(),
        test_heading_sequence_jump(),
        test_reading_order_signal(),
        test_statblock_good(),
        test_statblock_bad(),
        test_vocab_whog(),
        test_vocab_shadowrun(),
        test_page_marker_parser(),
        test_table_fixer_idempotent(),
        test_table_fixer_padding(),
        test_table_fixer_leading_trailing_pipe(),
        test_table_fixer_escape_pipes(),
        test_markers_survive_fix(),
        test_multi_block_table_fix(),
        test_empty_input(),
        test_single_line_non_table(),
        test_whitespace_columns_detection(),
        test_long_table(),
        test_mixed_content(),
        test_heading_preservation(),
        test_utf8_preservation(),
        test_marker_multpage(),
        test_score_functions_stability(),
        test_stat_block_with_table(),
        test_regression_snapshot(tmp),
    ]
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aether Forge regression suite")
    parser.add_argument("--report", required=True)
    parser.add_argument("--fail_fast", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        results = run_all(tmp)

    if args.fail_fast:
        for result in results:
            if not result.passed:
                payload = {
                    "failed": asdict(result),
                    "total": len(results),
                }
                Path(args.report).write_text(json.dumps(payload, indent=2), encoding="utf-8")
                print(json.dumps(payload, indent=2))
                raise SystemExit(2)

    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r.passed),
        "failed": sum(1 for r in results if not r.passed),
    }
    payload = {
        "summary": summary,
        "results": [asdict(r) for r in results],
    }

    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2))

    if summary["failed"] > 0:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
