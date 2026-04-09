#!/usr/bin/env python3
"""
Regression suite for Aether Forge quality checks.

Creates synthetic markdown fixtures that mimic TTRPG failure modes and validates
core quality tooling behaviors without requiring heavyweight model inference.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import tempfile
import types
from dataclasses import dataclass, asdict
from pathlib import Path

from table_fixer import apply_fixes
from quality_harness import (
    heading_sequence_score,
    table_integrity_score,
    statblock_integrity_score,
    reading_order_score,
    parse_page_markers,
    page_score,
)
from mechanics_vocab import best_family, statblock_density, mechanics_hits


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
    divider_like = any(" ---" in ln and "|" in ln for ln in fixed.splitlines())
    passed = divider_like and stats["separators_added"] >= 1
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
    return TestResult("statblock_bad", val < 0.8, f"score={val:.3f}")


def test_vocab_whog() -> TestResult:
    fam = best_family(fixture_whog_statblock())
    dens = statblock_density(fixture_whog_statblock())
    return TestResult("vocab_whog", fam.family == "whog" and dens > 0.3, f"family={fam.family}, density={dens:.3f}")


def test_vocab_shadowrun() -> TestResult:
    fam = best_family(fixture_shadowrun_statblock())
    return TestResult("vocab_shadowrun", fam.family == "shadowrun", f"family={fam.family}")


def test_vocab_anima_hits() -> TestResult:
    text = "Zeon Ki MA Multiple Life Points Attack Ability"
    hits = mechanics_hits(text)
    return TestResult("vocab_anima_hits", hits.get("anima", 0) > 0, f"anima_hits={hits.get('anima', 0)}")


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
    divider_rows = sum(1 for ln in fixed.splitlines() if "---" in ln and "|" in ln)
    passed = divider_rows >= 2 and stats["tables_seen"] >= 2
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


def test_interface_schemas_present() -> TestResult:
    candidates = [Path(__file__).parent / "schemas", Path(__file__).parent]
    expected = [
        "manifest.schema.json",
        "page_metadata.schema.json",
        "table_sidecar.schema.json",
        "repair_queue.schema.json",
        "quality_report.schema.json",
    ]
    schema_dir = next((cand for cand in candidates if all((cand / name).exists() for name in expected)), candidates[0])
    missing = [name for name in expected if not (schema_dir / name).exists()]
    if missing:
        return TestResult("interface_schemas_present", False, f"missing={missing}")
    for name in expected:
        try:
            json.loads((schema_dir / name).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return TestResult("interface_schemas_present", False, f"invalid_json={name}:{exc}")
    return TestResult("interface_schemas_present", True, "all schemas present and valid json")


def test_stat_block_with_table() -> TestResult:
    text = """
# Orc
| Key | Value |
| --- | --- |
| Armor Class | 13 |
| Hit Points | 15 |
""".strip()
    val = statblock_integrity_score(text)
    return TestResult("stat_block_with_table", val > 0.45, f"score={val:.3f}")


def test_image_only_signature_detection() -> TestResult:
    try:
        if "fitz" not in sys.modules:
            sys.modules["fitz"] = types.ModuleType("fitz")
        is_image_only_signature = importlib.import_module("orchestrator").is_image_only_signature
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return TestResult("image_only_signature_detection", False, f"import_error={exc}")
    passed = is_image_only_signature(1.0, 0.0) and not is_image_only_signature(0.8, 0.0)
    return TestResult("image_only_signature_detection", passed, "threshold check")


def test_donor_family_image_only() -> TestResult:
    try:
        if "fitz" not in sys.modules:
            sys.modules["fitz"] = types.ModuleType("fitz")
        choose_donor_family_from_text = importlib.import_module("orchestrator").choose_donor_family_from_text
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return TestResult("donor_family_image_only", False, f"import_error={exc}")
    passed = (
        choose_donor_family_from_text("Adobe Photoshop 25.0") == "image_only"
        and choose_donor_family_from_text("Image Conversion Pipeline") == "image_only"
    )
    return TestResult("donor_family_image_only", passed, "photoshop marker")


def test_donor_family_ignores_indesign_noise() -> TestResult:
    try:
        if "fitz" not in sys.modules:
            sys.modules["fitz"] = types.ModuleType("fitz")
        choose_donor_family_from_text = importlib.import_module("orchestrator").choose_donor_family_from_text
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return TestResult("donor_family_ignores_indesign_noise", False, f"import_error={exc}")
    fam = choose_donor_family_from_text("Adobe InDesign 19.0 Numenera Ninth World Bestiary GM Intrusion Damage Inflicted")
    return TestResult("donor_family_ignores_indesign_noise", fam != "dnd5e", f"family={fam}")


def test_surgeon_prompt_fallback() -> TestResult:
    try:
        if "fitz" not in sys.modules:
            sys.modules["fitz"] = types.ModuleType("fitz")
        if "PIL" not in sys.modules:
            pil_mod = types.ModuleType("PIL")
            pil_image_mod = types.ModuleType("PIL.Image")
            pil_mod.Image = pil_image_mod
            sys.modules["PIL"] = pil_mod
            sys.modules["PIL.Image"] = pil_image_mod
        prompt_for_layout = importlib.import_module("surgeon").prompt_for_layout
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return TestResult("surgeon_prompt_fallback", False, f"import_error={exc}")
    prompt = prompt_for_layout({"table_density": 0.0, "statblock_density": 0.0, "sidebar_density": 0.0, "image_coverage": 0.8})
    passed = "If you see ANY tables" in prompt and "stat blocks" in prompt
    return TestResult("surgeon_prompt_fallback", passed, "fallback prompt check")


def test_layout_detect_multicolumn_fixture() -> TestResult:
    from layout_utils import detect_multicolumn

    blocks = [
        (50, 80, 250, 120, "Left col text line one", 0, 0),
        (55, 130, 255, 170, "Left col text line two", 1, 0),
        (60, 180, 260, 220, "Left col text line three", 2, 0),
        (350, 85, 560, 125, "Right col text line one", 3, 0),
        (355, 135, 565, 175, "Right col text line two", 4, 0),
        (360, 185, 570, 225, "Right col text line three", 5, 0),
    ]
    passed = detect_multicolumn(blocks, page_width=620.0)
    return TestResult("layout_detect_multicolumn_fixture", passed, "two-column synthetic blocks")


def test_runner_page_map_requires_markers() -> TestResult:
    try:
        marker_pages = importlib.import_module("marker_runner")._parse_page_markers("No page markers here")
        docling_pages = importlib.import_module("docling_runner")._parse_page_markers("Still no page markers")
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return TestResult("runner_page_map_requires_markers", False, f"import_error={exc}")
    passed = marker_pages == {} and docling_pages == {}
    return TestResult("runner_page_map_requires_markers", passed, "empty page map without markers")


def test_cypher_profile_not_lane_a() -> TestResult:
    try:
        if "fitz" not in sys.modules:
            sys.modules["fitz"] = types.ModuleType("fitz")
        orchestrator = importlib.import_module("orchestrator")
        cfg = orchestrator.RuntimeConfig.from_env(Path("."))
        profile = orchestrator.PdfProfile(
            total_pages=24,
            average_chars_per_page=1200.0,
            weird_ratio=0.01,
            scanned_ratio=0.02,
            multicolumn_ratio=0.6,
            table_page_ratio=0.3,
            sidebar_page_ratio=0.2,
            statblock_page_ratio=0.6,
            image_dominant_ratio=0.1,
            is_image_only=False,
            donor_family="cypher",
            samples=[0, 1, 2],
            page_features=[],
        )
        lane, scores = orchestrator.choose_lane(profile, cfg)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return TestResult("cypher_profile_not_lane_a", False, f"import_error={exc}")
    passed = lane != "A" and scores["A"] < max(scores["B"], scores["B2"])
    return TestResult("cypher_profile_not_lane_a", passed, f"lane={lane}, scores={scores}")


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
        test_vocab_anima_hits(),
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
        test_interface_schemas_present(),
        test_stat_block_with_table(),
        test_image_only_signature_detection(),
        test_donor_family_image_only(),
        test_donor_family_ignores_indesign_noise(),
        test_surgeon_prompt_fallback(),
        test_layout_detect_multicolumn_fixture(),
        test_runner_page_map_requires_markers(),
        test_cypher_profile_not_lane_a(),
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
