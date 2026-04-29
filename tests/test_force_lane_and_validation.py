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
