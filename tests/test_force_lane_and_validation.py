from __future__ import annotations

import json
from pathlib import Path

import pytest

fitz = pytest.importorskip("fitz")

import orchestrator
import validate_outputs


def _pdf(path: Path, text: str = "hello") -> None:
    doc = fitz.open()
    p = doc.new_page()
    if text:
        p.insert_text((72, 72), text * 40)
    doc.save(path)


def test_force_lane_a_avoids_marker_docling(monkeypatch, tmp_path: Path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    in_dir.mkdir(); out_dir.mkdir()
    pdf = in_dir / "single_column_prose.pdf"
    _pdf(pdf, "native text")

    monkeypatch.setenv("INPUT_DIR", str(in_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(out_dir))
    monkeypatch.setenv("FORCE_LANE", "A")
    monkeypatch.setenv("OCR_MODE", "skip")
    monkeypatch.setenv("CONTINUE_ON_ERROR", "0")

    def _boom(*_a, **_kw):
        raise AssertionError("external runner should not be called for FORCE_LANE=A native text")

    monkeypatch.setattr(orchestrator, "run_marker", _boom)
    monkeypatch.setattr(orchestrator, "run_docling", _boom)

    cfg = orchestrator.apply_layout_calibration(orchestrator.RuntimeConfig.from_env(Path(orchestrator.__file__).parent))
    orchestrator.ensure_dirs(cfg)
    m = orchestrator.process_book(cfg, pdf, {})
    assert m.lane == "A"
    assert m.pages_ok == 1
    assert m.pages_ocr_needed == 0


def test_validate_outputs_writes_summary(tmp_path: Path, capsys):
    out = tmp_path / "out"
    (out / "manifests").mkdir(parents=True)
    sample = {
        "pages_ok": 1,
        "pages_empty": 0,
        "pages_image_only": 0,
        "pages_ocr_needed": 0,
        "pages_ocr_done": 0,
        "pages_queued": 0,
        "pages_failed": 0,
        "total_pages": 1,
        "reason_code_counts": {"native_text_extracted": 1},
    }
    (out / "manifests" / "book.manifest.json").write_text(json.dumps(sample), encoding="utf-8")

    import sys
    argv = sys.argv
    sys.argv = ["validate_outputs.py", "--output-dir", str(out), "--strict"]
    try:
        validate_outputs.main()
    finally:
        sys.argv = argv

    written = out / "corpus_validation_summary.json"
    assert written.exists()
    printed = capsys.readouterr().out.strip()
    assert json.loads(printed) == json.loads(written.read_text(encoding="utf-8"))


def test_auto_missing_external_dependency_falls_back_to_lane_a(monkeypatch, tmp_path: Path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    in_dir.mkdir(); out_dir.mkdir()
    pdf = in_dir / "book.pdf"
    _pdf(pdf, "native text")

    monkeypatch.setenv("INPUT_DIR", str(in_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(out_dir))
    monkeypatch.setenv("FORCE_LANE", "AUTO")
    monkeypatch.setenv("OCR_MODE", "skip")
    monkeypatch.setenv("CONTINUE_ON_ERROR", "0")
    monkeypatch.setenv("AUTO_FALLBACK_TO_LANE_A_ON_MISSING_EXTERNAL", "1")
    monkeypatch.setattr(orchestrator, "choose_lane", lambda *_a, **_kw: ("B", {"A": 0.1, "B": 0.9, "B2": 0.2}))

    def _missing(*_a, **_kw):
        raise RuntimeError("missing_external_dependency: marker_python path not found: /missing")
    monkeypatch.setattr(orchestrator, "run_marker", _missing)

    cfg = orchestrator.apply_layout_calibration(orchestrator.RuntimeConfig.from_env(Path(orchestrator.__file__).parent))
    orchestrator.ensure_dirs(cfg)
    m = orchestrator.process_book(cfg, pdf, {})
    assert m.lane == "A"
    assert m.fallback_used is True
    assert m.intended_lane == "B"
    assert m.actual_lane == "A"
    handoff = json.loads((Path(cfg.output_dir) / "book" / "astra_handoff_manifest.json").read_text(encoding="utf-8"))
    assert handoff["fallback_used"] is True
    assert handoff["intended_extraction_lane"] == "B"
    assert handoff["actual_extraction_lane"] == "A"


def test_auto_missing_external_dependency_fallback_disabled_fails(monkeypatch, tmp_path: Path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    in_dir.mkdir(); out_dir.mkdir()
    pdf = in_dir / "book.pdf"
    _pdf(pdf, "native text")
    monkeypatch.setenv("INPUT_DIR", str(in_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(out_dir))
    monkeypatch.setenv("FORCE_LANE", "AUTO")
    monkeypatch.setenv("AUTO_FALLBACK_TO_LANE_A_ON_MISSING_EXTERNAL", "0")
    monkeypatch.setattr(orchestrator, "choose_lane", lambda *_a, **_kw: ("B", {"A": 0.1, "B": 0.9, "B2": 0.2}))
    monkeypatch.setattr(orchestrator, "run_marker", lambda *_a, **_kw: (_ for _ in ()).throw(RuntimeError("missing_external_dependency: marker_python path not found: /missing")))
    cfg = orchestrator.apply_layout_calibration(orchestrator.RuntimeConfig.from_env(Path(orchestrator.__file__).parent))
    orchestrator.ensure_dirs(cfg)
    with pytest.raises(RuntimeError, match="missing_external_dependency"):
        orchestrator.process_book(cfg, pdf, {})


def test_force_lane_b_missing_dependency_fails_without_fallback(monkeypatch, tmp_path: Path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    in_dir.mkdir(); out_dir.mkdir()
    pdf = in_dir / "book.pdf"
    _pdf(pdf, "native text")
    monkeypatch.setenv("INPUT_DIR", str(in_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(out_dir))
    monkeypatch.setenv("FORCE_LANE", "B")
    monkeypatch.setenv("AUTO_FALLBACK_TO_LANE_A_ON_MISSING_EXTERNAL", "1")
    monkeypatch.setattr(orchestrator, "run_marker", lambda *_a, **_kw: (_ for _ in ()).throw(RuntimeError("missing_external_dependency: marker_python path not found: /missing")))
    cfg = orchestrator.apply_layout_calibration(orchestrator.RuntimeConfig.from_env(Path(orchestrator.__file__).parent))
    orchestrator.ensure_dirs(cfg)
    with pytest.raises(RuntimeError, match="missing_external_dependency"):
        orchestrator.process_book(cfg, pdf, {})


def test_ocr_force_missing_dependency_writes_run_summary_and_failed_records(monkeypatch, tmp_path: Path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    in_dir.mkdir(); out_dir.mkdir()
    _pdf(in_dir / "one.pdf", "a")
    _pdf(in_dir / "two.pdf", "b")
    monkeypatch.setenv("INPUT_DIR", str(in_dir))
    monkeypatch.setenv("OUTPUT_DIR", str(out_dir))
    monkeypatch.setenv("OCR_MODE", "force")
    monkeypatch.setenv("OCRMYPDF_BIN", "/definitely/missing/ocrmypdf")
    monkeypatch.setenv("CONTINUE_ON_ERROR", "1")
    import sys
    argv = sys.argv
    sys.argv = ["orchestrator.py"]
    try:
        orchestrator.main()
    finally:
        sys.argv = argv
    rs = json.loads((out_dir / "run_summary.json").read_text(encoding="utf-8"))
    assert rs["books_total"] == 2
    assert rs["books_failed_extraction"] == 2
    assert len(list((out_dir / "failed_books").glob("*.failure.json"))) == 2


def test_validate_outputs_uses_run_summary_when_no_artifacts(tmp_path: Path):
    out = tmp_path / "out"
    (out / "manifests").mkdir(parents=True)
    (out / "run_summary.json").write_text(json.dumps({
        "books_total": 2,
        "books_failed_extraction": 2,
        "failure_reason_counts": {"missing_external_dependency": 2},
    }), encoding="utf-8")
    import sys
    argv = sys.argv
    sys.argv = ["validate_outputs.py", "--output-dir", str(out), "--strict"]
    try:
        validate_outputs.main()
    finally:
        sys.argv = argv
    s = json.loads((out / "corpus_validation_summary.json").read_text(encoding="utf-8"))
    assert s["total_books"] == 2
    assert s["books_failed_extraction"] == 2
    assert "missing_external_dependency" in s["top_error_codes"]


def test_top_error_codes_excludes_ocr_applied(tmp_path: Path, capsys):
    out = tmp_path / "out"
    (out / "manifests").mkdir(parents=True)
    (out / "book").mkdir(parents=True)
    (out / "manifests" / "book.manifest.json").write_text(json.dumps({"page_count": 2}), encoding="utf-8")
    (out / "book" / "strict_audit.json").write_text(json.dumps({"strict_audit_status": "pass", "unaccounted_page_count": 0, "status_counts": {"ocr_done": 2}}), encoding="utf-8")
    (out / "book" / "astra_handoff_manifest.json").write_text(json.dumps({"pages_ocr_done": 2}), encoding="utf-8")
    (out / "book" / "book.page_truth.jsonl").write_text(
        json.dumps({"book_id": "book", "page": 1, "page_status": "ocr_done", "reason_code": "ocr_applied"}) + "\n" +
        json.dumps({"book_id": "book", "page": 2, "page_status": "ocr_done", "reason_code": "image_only_ocr_required"}) + "\n",
        encoding="utf-8",
    )
    import sys
    argv = sys.argv
    sys.argv = ["validate_outputs.py", "--output-dir", str(out), "--strict"]
    try:
        validate_outputs.main()
    finally:
        sys.argv = argv
    s = json.loads((out / "corpus_validation_summary.json").read_text(encoding="utf-8"))
    assert "ocr_applied" not in s["top_error_codes"]
    assert "image_only_ocr_required" not in s["top_error_codes"]
