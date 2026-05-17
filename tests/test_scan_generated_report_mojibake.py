import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/handoff/scan_generated_report_mojibake.py")


def _run(path: Path, strict: bool = True, allow_source_examples: bool = False, extra=None):
    cmd = [sys.executable, str(SCRIPT), "--path", str(path)]
    if strict:
        cmd.append("--strict")
    if allow_source_examples:
        cmd.append("--allow-source-examples")
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p, json.loads(p.stdout)


def test_clean_generated_report_passes(tmp_path: Path):
    d = tmp_path / "reports"
    d.mkdir()
    (d / "a.md").write_text("# Report\n- count: 1\n", encoding="utf-8")
    p, r = _run(d)
    assert p.returncode == 0
    assert r["valid"] is True


def test_generated_heading_mojibake_fails_strict_mode(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("# Aggregation â€” Report\n", encoding="utf-8")
    p, r = _run(f)
    assert p.returncode != 0


def test_confidence_range_mojibake_fails_strict_mode(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("Confidence range: 0.5 â€“ 0.8\n", encoding="utf-8")
    p, r = _run(f)
    assert p.returncode != 0


def test_json_source_derived_value_warns_with_allow_source_examples(tmp_path: Path):
    f = tmp_path / "r.json"
    f.write_text('{"donor_construct": "Sword â€” of test"}\n', encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0
    assert r["warning_count"] >= 1
    assert r["error_count"] == 0


def test_json_key_mojibake_still_fails(tmp_path: Path):
    f = tmp_path / "r.json"
    f.write_text('{"Âkey": "ok"}\n', encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode != 0


def test_markdown_source_example_bullet_warns_with_allow_source_examples(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("- packet_id: p1 donor construct example: Ã¢â‚¬â€œ text\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0
    assert r["warning_count"] >= 1


def test_csv_data_row_mojibake_warns_with_allow_source_examples(tmp_path: Path):
    f = tmp_path / "r.csv"
    f.write_text("packet_id,example\np1,quoted Ã¢â‚¬â€œ text\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0
    assert r["warning_count"] >= 1


def test_csv_header_mojibake_fails(tmp_path: Path):
    f = tmp_path / "r.csv"
    f.write_text("packet_id,examâ€”ple\np1,ok\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode != 0


def test_ambiguous_mojibake_fails_strict_mode(tmp_path: Path):
    f = tmp_path / "r.txt"
    f.write_text("random Ã¢â‚¬ text\n", encoding="utf-8")
    p, r = _run(f)
    assert p.returncode != 0
    assert any("ambiguous_mojibake" in e for e in r["errors"])


def test_scanner_handles_single_file_path(tmp_path: Path):
    f = tmp_path / "r.json"
    f.write_text('{"ok": true}', encoding="utf-8")
    p, r = _run(f)
    assert p.returncode == 0
    assert r["files_scanned"] == 1


def test_scanner_handles_directory_recursion(tmp_path: Path):
    d = tmp_path / "reports"
    (d / "x").mkdir(parents=True)
    (d / "x" / "a.md").write_text("# A\n", encoding="utf-8")
    (d / "x" / "b.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    p, r = _run(d)
    assert p.returncode == 0
    assert r["files_scanned"] == 2


def test_output_json_writes_valid_json(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("# Clean\n", encoding="utf-8")
    out = tmp_path / "out.json"
    p, _ = _run(f, extra=["--output-json", str(out)])
    assert p.returncode == 0
    obj = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(obj, dict)
    assert "valid" in obj
