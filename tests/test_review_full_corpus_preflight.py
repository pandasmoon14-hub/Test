import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/handoff/review_full_corpus_preflight.py")


def _mk_dry_run(tmp_path: Path):
    d = tmp_path / "dry"
    d.mkdir()
    files = [
        {"relative_path": "Level Up - Advanced 5th Edition - Gate Pass Gazette.pdf"},
        {"relative_path": "Traveller Merchant Fleet.pdf"},
        {"relative_path": "weird_unknown_book.pdf"},
    ]
    (d / "full_corpus_dry_run_manifest.json").write_text(json.dumps({"files": files}), encoding="utf-8")
    (d / "full_corpus_dry_run_manifest.csv").write_text("relative_path,supported\na.pdf,True\nb.pdf,True\nc.pdf,True\n", encoding="utf-8")
    (d / "full_corpus_preflight_issues.csv").write_text("issue_code,path,detail,severity\nnon_ascii_path,a,na,warning\nunusually_large_file,b,123,warning\n", encoding="utf-8")
    (d / "full_corpus_donor_family_estimates.csv").write_text(
        "relative_path,donor_family_candidates,confidence,repair_queue_candidates\n"
        "Level Up - Advanced 5th Edition - Gate Pass Gazette.pdf,unclassified_or_mixed_donor_family,low,manual_review_required\n"
        "Traveller Merchant Fleet.pdf,unclassified_or_mixed_donor_family,low,manual_review_required\n"
        "weird_unknown_book.pdf,unclassified_or_mixed_donor_family,low,manual_review_required\n",
        encoding="utf-8",
    )
    (d / "full_corpus_dry_run_report.md").write_text("# report\n", encoding="utf-8")
    return d


def _run(dry: Path, out: Path, strict=True, extra=None):
    cmd = [sys.executable, str(SCRIPT), "--dry-run-dir", str(dry), "--output-dir", str(out)]
    if strict:
        cmd.append("--strict")
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p, json.loads(p.stdout)


def test_minimal_valid_dry_run_review(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    p, r = _run(dry, tmp_path / "out")
    assert p.returncode == 0
    assert r["valid"] is True


def test_missing_dry_run_file_fails_strict(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    (dry / "full_corpus_dry_run_manifest.json").unlink()
    p, r = _run(dry, tmp_path / "out")
    assert p.returncode != 0
    assert any("missing_required_file" in e for e in r["errors"])


def test_malformed_csv_fails_strict(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    (dry / "full_corpus_preflight_issues.csv").write_text("\x00\x00", encoding="utf-8")
    p, r = _run(dry, tmp_path / "out")
    assert p.returncode != 0
    assert r["valid"] is False


def test_issue_triage_groups_issue_code(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    _, r = _run(dry, tmp_path / "out")
    tri = Path(tmp_path / "out" / "full_corpus_issue_triage.csv").read_text(encoding="utf-8")
    assert "non_ascii_path" in tri


def test_unclassified_rows_are_clustered(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    _, r = _run(dry, tmp_path / "out", extra=["--min-cluster-size", "1"])
    assert r["cluster_count"] >= 1


def test_known_series_tokens_produce_clusters(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    _, _ = _run(dry, tmp_path / "out", extra=["--min-cluster-size", "1"])
    text = Path(tmp_path / "out" / "full_corpus_unclassified_clusters.csv").read_text(encoding="utf-8").lower()
    assert "level_up_a5e_gate_pass" in text or "traveller" in text


def test_overlay_writes_yaml_when_requested(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    _, r = _run(dry, tmp_path / "out", extra=["--write-routing-overlay-proposal", "--min-cluster-size", "1"])
    assert Path(tmp_path / "out" / "donor_family_routing_overlay_proposal.yaml").exists()


def test_output_files_are_written(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    _, r = _run(dry, tmp_path / "out")
    for p in r["output_files"]:
        assert Path(p).exists()


def test_report_contains_separation_reminders(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    _, _ = _run(dry, tmp_path / "out")
    rep = Path(tmp_path / "out" / "full_corpus_preflight_review_report.md").read_text(encoding="utf-8")
    assert "Dry-run routing metadata is not extraction truth." in rep
    assert "Extraction truth is not conversion permission." in rep
    assert "Conversion permission is not canon permission." in rep


def test_no_canon_permission_language_introduced(tmp_path: Path):
    dry = _mk_dry_run(tmp_path)
    _, _ = _run(dry, tmp_path / "out", extra=["--write-routing-overlay-proposal", "--min-cluster-size", "1"])
    txt = Path(tmp_path / "out" / "full_corpus_preflight_review_report.md").read_text(encoding="utf-8").lower()
    assert "canon permission granted" not in txt
