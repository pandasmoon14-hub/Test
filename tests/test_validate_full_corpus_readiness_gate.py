from pathlib import Path
from tests.conftest import ROOT
import json
import subprocess
import sys

SCRIPT = ROOT / "scripts/handoff/validate_full_corpus_readiness_gate.py"


def _mk_inputs(tmp_path: Path, with_overlay=True):
    dry = tmp_path / "dry"
    pre = tmp_path / "pre"
    dry.mkdir(); pre.mkdir()
    (dry / "full_corpus_dry_run_manifest.json").write_text(json.dumps({"files": [{"id": 1}, {"id": 2}]}), encoding="utf-8")
    (dry / "full_corpus_dry_run_manifest.csv").write_text("relative_path,supported\na.pdf,True\nb.pdf,True\n", encoding="utf-8")
    (dry / "full_corpus_preflight_issues.csv").write_text("issue_code,path,detail,severity\nnon_ascii_path,a,x,warning\n", encoding="utf-8")
    (dry / "full_corpus_donor_family_estimates.csv").write_text(
        "relative_path,donor_family_candidates,confidence,repair_queue_candidates\n"
        "a.pdf,unclassified_or_mixed_donor_family,low,manual_review_required\n"
        "b.pdf,d20_class_level_fantasy,medium,\n", encoding="utf-8")
    (dry / "full_corpus_dry_run_report.md").write_text("Dry-run routing metadata is not extraction truth.\n", encoding="utf-8")

    (pre / "full_corpus_preflight_review_summary.json").write_text(json.dumps({"files_total": 2, "issue_count": 1, "unclassified_count": 1, "cluster_count": 1, "overlay_records": 1}), encoding="utf-8")
    (pre / "full_corpus_preflight_review_report.md").write_text(
        "Dry-run routing metadata is not extraction truth.\nExtraction truth is not conversion permission.\nConversion permission is not canon permission.\n", encoding="utf-8")
    (pre / "full_corpus_issue_triage.csv").write_text("issue_code,severity,count\nnon_ascii_path,warning,1\n", encoding="utf-8")
    (pre / "full_corpus_unclassified_clusters.csv").write_text("cluster_id,match_terms,count,sample_files\ntraveller,traveller,1,a.pdf\n", encoding="utf-8")
    if with_overlay:
        (pre / "donor_family_routing_overlay_proposal.yaml").write_text("overlay_patterns:\n  - pattern_id: traveller\n", encoding="utf-8")
    return dry, pre


def _run(dry: Path, pre: Path, out: Path, strict=True, extra=None):
    cmd = [sys.executable, str(SCRIPT), "--dry-run-dir", str(dry), "--preflight-review-dir", str(pre), "--output-dir", str(out)]
    if strict:
        cmd.append("--strict")
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p, json.loads(p.stdout)


def test_minimal_valid_readiness_gate(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path)
    p, r = _run(dry, pre, tmp_path / "out")
    assert p.returncode == 0
    assert r["valid"] is True


def test_missing_dry_run_dir_fails_strict_mode(tmp_path: Path):
    _, pre = _mk_inputs(tmp_path)
    p, r = _run(tmp_path / "missing", pre, tmp_path / "out")
    assert p.returncode != 0


def test_missing_preflight_review_dir_fails_strict_mode(tmp_path: Path):
    dry, _ = _mk_inputs(tmp_path)
    p, r = _run(dry, tmp_path / "missing", tmp_path / "out")
    assert p.returncode != 0


def test_missing_required_file_fails_strict_mode(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path)
    (dry / "full_corpus_dry_run_manifest.csv").unlink()
    p, r = _run(dry, pre, tmp_path / "out")
    assert p.returncode != 0


def test_inconsistent_file_counts_produces_warning(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path)
    (pre / "full_corpus_preflight_review_summary.json").write_text(json.dumps({"files_total": 999, "issue_count": 1, "unclassified_count": 1, "cluster_count": 1, "overlay_records": 1}), encoding="utf-8")
    _, r = _run(dry, pre, tmp_path / "out")
    assert any("files_total_mismatch" in w for w in r["warnings"])


def test_unclassified_threshold_can_fail_strict_mode(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path)
    p, r = _run(dry, pre, tmp_path / "out", extra=["--allow-unclassified-threshold", "0"])
    assert p.returncode != 0


def test_routing_overlay_required_flag_fails_when_missing(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path, with_overlay=False)
    p, r = _run(dry, pre, tmp_path / "out", extra=["--require-routing-overlay"])
    assert p.returncode != 0


def test_report_contains_separation_reminders(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path)
    _, r = _run(dry, pre, tmp_path / "out")
    rep = Path(tmp_path / "out" / "full_corpus_readiness_gate_report.md").read_text(encoding="utf-8")
    assert "Dry-run routing metadata is not extraction truth." in rep
    assert "Extraction truth is not conversion permission." in rep
    assert "Conversion permission is not canon permission." in rep


def test_no_canon_permission_language_is_introduced(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path)
    _, _ = _run(dry, pre, tmp_path / "out")
    rep = Path(tmp_path / "out" / "full_corpus_readiness_gate_report.md").read_text(encoding="utf-8").lower()
    assert "canon permission granted" not in rep


def test_output_files_are_written(tmp_path: Path):
    dry, pre = _mk_inputs(tmp_path)
    _, r = _run(dry, pre, tmp_path / "out")
    for p in r["output_files"]:
        assert Path(p).exists()
