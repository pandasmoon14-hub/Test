import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/handoff/build_full_corpus_extraction_plan.py")


def _mk_inputs(tmp_path: Path, gate_valid=True, gate_status="ready_with_warnings", with_overlay=True):
    dry = tmp_path / "dry"; pre = tmp_path / "pre"; gate = tmp_path / "gate"
    dry.mkdir(); pre.mkdir(); gate.mkdir()
    files = [
        {"relative_path": "a.pdf", "absolute_path": "/a.pdf", "file_name": "a.pdf", "extension": ".pdf", "size_bytes": 1234},
        {"relative_path": "b.pdf", "absolute_path": "/b.pdf", "file_name": "b.pdf", "extension": ".pdf", "size_bytes": 999999999},
    ]
    (dry / "full_corpus_dry_run_manifest.json").write_text(json.dumps({"files": files}), encoding="utf-8")
    (dry / "full_corpus_dry_run_manifest.csv").write_text("relative_path,supported\na.pdf,True\nb.pdf,True\n", encoding="utf-8")
    (dry / "full_corpus_preflight_issues.csv").write_text("issue_code,path,detail,severity\nunusually_large_file,b.pdf,x,warning\n", encoding="utf-8")
    (dry / "full_corpus_donor_family_estimates.csv").write_text(
        "relative_path,donor_family_candidates,confidence,repair_queue_candidates\n"
        "a.pdf,unclassified_or_mixed_donor_family,low,manual_review_required\n"
        "b.pdf,magic_spell_power_compendium,medium,\n", encoding="utf-8")
    (dry / "full_corpus_dry_run_report.md").write_text("ok", encoding="utf-8")

    (pre / "full_corpus_preflight_review_summary.json").write_text(json.dumps({"ok": True}), encoding="utf-8")
    (pre / "full_corpus_preflight_review_report.md").write_text("ok", encoding="utf-8")
    (pre / "full_corpus_issue_triage.csv").write_text("issue_code,severity,count\nunusually_large_file,warning,1\n", encoding="utf-8")
    (pre / "full_corpus_unclassified_clusters.csv").write_text("cluster_id,match_terms,count,sample_files\ntraveller,traveller,1,a.pdf\n", encoding="utf-8")
    if with_overlay:
        (pre / "donor_family_routing_overlay_proposal.yaml").write_text(
            "overlay_patterns:\n  - pattern_id: traveller\n    match_terms: [a]\n    suggested_donor_family_candidates: [lifepath_trade_starship]\n", encoding="utf-8")

    (gate / "full_corpus_readiness_gate_summary.json").write_text(json.dumps({"valid": gate_valid, "readiness_status": gate_status}), encoding="utf-8")
    (gate / "full_corpus_readiness_gate_report.md").write_text("ok", encoding="utf-8")
    (gate / "full_corpus_readiness_gate_checks.csv").write_text("check_name,state,detail\na,pass,b\n", encoding="utf-8")
    (gate / "full_corpus_next_action_plan.md").write_text("ok", encoding="utf-8")
    return dry, pre, gate


def _run(dry: Path, pre: Path, gate: Path, out: Path, strict=True, extra=None):
    cmd = [sys.executable, str(SCRIPT), "--dry-run-dir", str(dry), "--preflight-review-dir", str(pre), "--readiness-gate-dir", str(gate), "--output-dir", str(out)]
    if strict:
        cmd.append("--strict")
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p, json.loads(p.stdout)


def test_minimal_valid_extraction_plan(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path)
    p, r = _run(dry, pre, gate, tmp_path / "out", extra=["--allow-ready-with-warnings"])
    assert p.returncode == 0 and r["valid"]


def test_missing_dirs_fail_strict(tmp_path: Path):
    p, _ = _run(tmp_path / "d", tmp_path / "p", tmp_path / "g", tmp_path / "out")
    assert p.returncode != 0


def test_invalid_readiness_gate_fails_when_required(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path, gate_valid=False)
    p, _ = _run(dry, pre, gate, tmp_path / "out", extra=["--require-readiness-valid", "--allow-ready-with-warnings"])
    assert p.returncode != 0


def test_ready_with_warnings_accepted_when_allowed(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path, gate_status="ready_with_warnings")
    p, r = _run(dry, pre, gate, tmp_path / "out", extra=["--allow-ready-with-warnings"])
    assert p.returncode == 0


def test_issue_based_lane_assignment(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path)
    _, _ = _run(dry, pre, gate, tmp_path / "out", extra=["--allow-ready-with-warnings"])
    rows = Path(tmp_path / "out" / "full_corpus_extraction_plan_manifest.csv").read_text(encoding="utf-8")
    assert "lane_b_large_or_layout_risk" in rows


def test_repair_queue_based_lane_assignment(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path)
    (dry / "full_corpus_donor_family_estimates.csv").write_text(
        "relative_path,donor_family_candidates,confidence,repair_queue_candidates\n"
        "a.pdf,unclassified_or_mixed_donor_family,low,map_diagram_review\n"
        "b.pdf,magic_spell_power_compendium,medium,\n", encoding="utf-8")
    _, _ = _run(dry, pre, gate, tmp_path / "out", extra=["--allow-ready-with-warnings"])
    rows = Path(tmp_path / "out" / "full_corpus_extraction_plan_manifest.csv").read_text(encoding="utf-8")
    assert "lane_c_visual_map_or_scan_review" in rows


def test_unclassified_enters_review_queue(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path)
    _, r = _run(dry, pre, gate, tmp_path / "out", extra=["--allow-ready-with-warnings"])
    q = Path(tmp_path / "out" / "full_corpus_extraction_review_queue.csv").read_text(encoding="utf-8")
    assert "unclassified" in q


def test_overlay_applies_only_to_unclassified(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path)
    _, _ = _run(dry, pre, gate, tmp_path / "out", extra=["--use-routing-overlay", "--allow-ready-with-warnings"])
    rows = Path(tmp_path / "out" / "full_corpus_extraction_plan_manifest.csv").read_text(encoding="utf-8")
    assert "lifepath_trade_starship" in rows


def test_output_files_written_and_report_reminders(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path)
    _, r = _run(dry, pre, gate, tmp_path / "out", extra=["--allow-ready-with-warnings"])
    for p in r["output_files"]:
        assert Path(p).exists()
    rep = Path(tmp_path / "out" / "full_corpus_extraction_plan_report.md").read_text(encoding="utf-8")
    assert "Dry-run routing metadata is not extraction truth." in rep
    assert "Extraction planning is not extraction truth." in rep
    assert "Conversion permission is not canon permission." in rep
    assert "canon permission granted" not in rep.lower()


def test_no_extraction_artifacts_created(tmp_path: Path):
    dry, pre, gate = _mk_inputs(tmp_path)
    _, _ = _run(dry, pre, gate, tmp_path / "out", extra=["--allow-ready-with-warnings"])
    out_files = {p.name for p in (tmp_path / "out").iterdir()}
    assert "packets" not in out_files
