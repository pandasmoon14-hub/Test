from __future__ import annotations
import json
from pathlib import Path
import pytest

fitz = pytest.importorskip("fitz")

import orchestrator
import validate_outputs


def make_pdf(path: Path, pages: int = 50):
    doc = fitz.open()
    for i in range(pages):
        p = doc.new_page()
        p.insert_text((72, 72), f"Page {i+1} native text " * 30)
    doc.save(path)


def test_lane_a_finalizes_page_truth_and_artifacts(monkeypatch, tmp_path: Path):
    in_dir = tmp_path / "in"; out_dir = tmp_path / "out"
    in_dir.mkdir(); out_dir.mkdir()
    pdf = in_dir / "fifty.pdf"
    make_pdf(pdf, 50)

    monkeypatch.setenv("INPUT_DIR", str(in_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(out_dir))
    monkeypatch.setenv("FORCE_LANE", "A")
    monkeypatch.setenv("OCR_MODE", "skip")

    cfg = orchestrator.apply_layout_calibration(orchestrator.RuntimeConfig.from_env(Path(orchestrator.__file__).parent))
    orchestrator.ensure_dirs(cfg)
    m = orchestrator.process_book(cfg, pdf, {})
    assert m.pages_ok == 50

    book_dir = out_dir / "fifty"
    pt = book_dir / "fifty.page_truth.jsonl"
    rows = [json.loads(x) for x in pt.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 50
    assert all(r.get("page_status") == "ok" for r in rows)
    assert all(r.get("reason_code") == "native_text_extracted" for r in rows)
    assert (book_dir / "strict_audit.json").exists()
    assert (book_dir / "astra_handoff_manifest.json").exists()
    audit = json.loads((book_dir / "strict_audit.json").read_text(encoding="utf-8"))
    assert audit["page_count"] == 50
    assert audit["final_page_truth_count"] == 50
    assert audit["markdown_page_marker_count"] == 50
    assert sum(audit["status_counts"].values()) == 50
    assert audit["unaccounted_page_count"] == 0
    assert audit["strict_audit_status"] == "pass"
    handoff = json.loads((book_dir / "astra_handoff_manifest.json").read_text(encoding="utf-8"))
    for key in ["source_sha256", "final_page_truth_count", "markdown_page_marker_count", "pages_ok", "unaccounted_page_count", "artifact_paths"]:
        assert key in handoff


def test_validate_outputs_strict_rejects_missing_artifacts(tmp_path: Path, monkeypatch):
    out = tmp_path / "o"
    (out / "manifests").mkdir(parents=True)
    (out / "book").mkdir(parents=True)
    (out / "manifests" / "book.manifest.json").write_text(json.dumps({"total_pages": 1}), encoding="utf-8")
    (out / "book" / "book.page_truth.jsonl").write_text(json.dumps({"book_id": "book", "page": 1}) + "\n", encoding="utf-8")

    import sys
    old = sys.argv
    sys.argv = ["validate_outputs.py", "--output-dir", str(out), "--strict"]
    try:
        validate_outputs.main()
    finally:
        sys.argv = old

    s = json.loads((out / "corpus_validation_summary.json").read_text(encoding="utf-8"))
    assert s["books_artifact_invalid"] == 1


def test_validate_outputs_strict_detects_659_vs_60_regression(tmp_path: Path):
    out = tmp_path / "r"
    (out / "manifests").mkdir(parents=True)
    book = out / "exalted"; book.mkdir(parents=True)
    (out / "manifests" / "exalted.manifest.json").write_text(json.dumps({"total_pages": 659}), encoding="utf-8")
    (book / "strict_audit.json").write_text(json.dumps({"strict_audit_status": "fail", "unaccounted_page_count": 599}), encoding="utf-8")
    (book / "astra_handoff_manifest.json").write_text(json.dumps({"book_id": "exalted"}), encoding="utf-8")
    rows = [{"book_id": "exalted", "page": i + 1, "page_status": "ok", "reason_code": "native_text_extracted"} for i in range(60)]
    (book / "exalted.page_truth.jsonl").write_text("\\n".join(json.dumps(r) for r in rows) + "\\n", encoding="utf-8")
    import sys
    old = sys.argv
    sys.argv = ["validate_outputs.py", "--output-dir", str(out), "--strict"]
    try:
        validate_outputs.main()
    finally:
        sys.argv = old
    s = json.loads((out / "corpus_validation_summary.json").read_text(encoding="utf-8"))
    assert s["books_artifact_invalid"] == 1
    assert "strict_audit_failed" in s["top_error_codes"] or "unaccounted_pages_present" in s["top_error_codes"]
