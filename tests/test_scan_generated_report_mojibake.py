from pathlib import Path
from tests.helpers import ROOT
import json
import subprocess
import sys

SCRIPT = ROOT / "scripts/handoff/scan_generated_report_mojibake.py"


def _run(path: Path, strict: bool = True, allow_source_examples: bool = False, extra=None):
    cmd = [sys.executable, str(SCRIPT), "--path", str(path)]
    if strict:
        cmd.append("--strict")
    if allow_source_examples:
        cmd.append("--allow-source-examples")
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return p, json.loads(p.stdout)


def test_clean_generated_report_passes(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("# Report\n- count: 1\n", encoding="utf-8")
    p, r = _run(f)
    assert p.returncode == 0 and r["valid"]


def test_heading_mojibake_fails(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("# Batch 001 â€” Report\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode != 0
    assert any("generated_scaffold_mojibake" in e for e in r["errors"])


def test_confidence_range_mojibake_fails(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("Confidence range: 0.5 â€“ 0.8\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode != 0


def test_json_value_warns_with_allow(tmp_path: Path):
    f = tmp_path / "r.json"
    f.write_text('{"donor_construct": "x Ã¢â‚¬â€œ y"}\n', encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0
    assert r["warning_count"] >= 1 and r["error_count"] == 0


def test_json_key_mojibake_fails(tmp_path: Path):
    f = tmp_path / "r.json"
    f.write_text('{"Âkey": "ok"}\n', encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode != 0


def test_markdown_packet_row_warns(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("- `packet_001` - normalized Astra mapping - donor Ã¢â‚¬â€œ text\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0
    assert r["warning_count"] >= 1


def test_markdown_indented_packet_row_warns(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("  - `packet_001` - source-local retained construct - donor Ã¢â‚¬â€œ text\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0


def test_doctrine_pressure_row_warns(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("- `packet_009` - doctrine escalation rationale Ã¢â‚¬â€œ sample\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0


def test_source_local_retention_row_warns(tmp_path: Path):
    f = tmp_path / "r.md"
    f.write_text("- `packet_011` - source-local retained construct Ã¢â‚¬â€œ sample\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0


def test_csv_data_row_warns(tmp_path: Path):
    f = tmp_path / "r.csv"
    f.write_text("packet_id,example\np1,quoted Ã¢â‚¬â€œ text\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode == 0 and r["warning_count"] >= 1


def test_csv_header_fails(tmp_path: Path):
    f = tmp_path / "r.csv"
    f.write_text("packet_id,exaÂmple\np1,ok\n", encoding="utf-8")
    p, r = _run(f, allow_source_examples=True)
    assert p.returncode != 0


def test_single_file_and_output_json_handles_control(tmp_path: Path):
    f = tmp_path / "r.txt"
    f.write_text("source text � \u0001\n", encoding="utf-8", errors="ignore")
    out = tmp_path / "out.json"
    p, r = _run(f, allow_source_examples=True, extra=["--output-json", str(out)])
    assert isinstance(r, dict)
    assert json.loads(out.read_text(encoding="utf-8"))["path"]
