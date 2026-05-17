import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/handoff/validate_conversion_run_integrity.py")


def _mk_run(tmp_path: Path) -> Path:
    run = tmp_path / "run"
    for d in ["packets", "prompts", "results", "validation", "reports/aggregation"]:
        (run / d).mkdir(parents=True, exist_ok=True)
    idx = [
        {"packet_id": "packet_001"},
        {"packet_id": "packet_002"},
    ]
    (run / "packet_index.json").write_text(json.dumps(idx), encoding="utf-8")
    for pid in ["packet_001", "packet_002"]:
        (run / "packets" / pid).mkdir(exist_ok=True)
        (run / "prompts" / f"{pid}_conversion_prompt.md").write_text("# prompt", encoding="utf-8")
        obj = {
            "packet_id": pid,
            "result_status": "drafted",
            "mapping_ledger": [{"donor_construct": "x", "lawful_outcome": "normalized Astra mapping"}],
            "confidence": 0.7,
            "doctrine_escalations": [],
            "source_local_retentions": [],
            "rejected_imports": [],
            "canon_candidate_notes": [],
            "reviewer_notes": ["review required"],
        }
        (run / "results" / f"{pid}_conversion_result.json").write_text(json.dumps(obj), encoding="utf-8")
        (run / "results" / f"{pid}_conversion_result.md").write_text("not canon", encoding="utf-8")
    agg = {
        "packets_total": 2,
        "result_status_counts": {"drafted": 2},
        "lawful_outcome_counts": {"normalized Astra mapping": 2},
        "human_review_queue_count": 0,
        "output_dir": str(run / "reports" / "aggregation"),
    }
    (run / "reports" / "aggregation" / "batch_001_aggregation_report.json").write_text(json.dumps(agg), encoding="utf-8")
    for fn in [
        "batch_001_aggregation_report.md",
        "batch_001_doctrine_pressure_report.md",
        "batch_001_source_local_retention_report.md",
        "batch_001_quarantine_escalation_queue.csv",
        "batch_001_human_review_queue.csv",
        "batch_001_construct_family_summary.csv",
        "batch_001_packet_aggregation_table.csv",
    ]:
        (run / "reports" / "aggregation" / fn).write_text("ok", encoding="utf-8")
    return run


def _run(run: Path, strict: bool = True):
    cmd = [sys.executable, str(SCRIPT), "--run-dir", str(run)]
    if strict:
        cmd.append("--strict")
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p, json.loads(p.stdout)


def test_minimal_valid_synthetic_run(tmp_path: Path):
    run = _mk_run(tmp_path)
    p, rep = _run(run, strict=True)
    assert p.returncode == 0
    assert rep["valid"] is True


def test_duplicate_packet_id_failure(tmp_path: Path):
    run = _mk_run(tmp_path)
    (run / "packet_index.json").write_text(json.dumps([{"packet_id": "packet_001"}, {"packet_id": "packet_001"}]))
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("duplicate_packet_id" in e for e in rep["errors"])


def test_missing_result_failure(tmp_path: Path):
    run = _mk_run(tmp_path)
    (run / "results" / "packet_002_conversion_result.json").unlink()
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("result_json_count_not_one:packet_002:0" in e for e in rep["errors"])


def test_stale_backup_artifact_failure(tmp_path: Path):
    run = _mk_run(tmp_path)
    (run / "results" / "foo.bak_before_2026").write_text("x")
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("stale_backup_artifact" in e for e in rep["errors"])


def test_invalid_lawful_outcome_failure(tmp_path: Path):
    run = _mk_run(tmp_path)
    j = json.loads((run / "results" / "packet_001_conversion_result.json").read_text())
    j["mapping_ledger"][0]["lawful_outcome"] = "bad outcome"
    (run / "results" / "packet_001_conversion_result.json").write_text(json.dumps(j))
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("invalid_lawful_outcome" in e for e in rep["errors"])


def test_placeholder_status_failure_in_strict_mode(tmp_path: Path):
    run = _mk_run(tmp_path)
    j = json.loads((run / "results" / "packet_001_conversion_result.json").read_text())
    j["result_status"] = "placeholder"
    (run / "results" / "packet_001_conversion_result.json").write_text(json.dumps(j))
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("placeholder_status_in_strict" in e for e in rep["errors"])


def test_unresolved_variable_leakage_failure(tmp_path: Path):
    run = _mk_run(tmp_path)
    (run / "reports" / "note.md").write_text("$batchRoot", encoding="utf-8")
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("unresolved_placeholder" in e for e in rep["errors"])


def test_canon_leakage_failure(tmp_path: Path):
    run = _mk_run(tmp_path)
    j = json.loads((run / "results" / "packet_001_conversion_result.json").read_text())
    j["reviewer_notes"] = ["approved canon"]
    j["canon_candidate_notes"] = []
    (run / "results" / "packet_001_conversion_result.json").write_text(json.dumps(j))
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("canon_leakage_phrase" in e for e in rep["errors"])


def test_aggregation_summary_consistency_test(tmp_path: Path):
    run = _mk_run(tmp_path)
    agg = json.loads((run / "reports" / "aggregation" / "batch_001_aggregation_report.json").read_text())
    agg["packets_total"] = 3
    (run / "reports" / "aggregation" / "batch_001_aggregation_report.json").write_text(json.dumps(agg))
    p, rep = _run(run)
    assert p.returncode != 0
    assert any("aggregation_packets_total_mismatch" in e for e in rep["errors"])
