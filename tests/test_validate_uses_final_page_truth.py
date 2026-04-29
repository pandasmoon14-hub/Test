from __future__ import annotations
import json, sys
from pathlib import Path
import validate_outputs


def _write_jsonl(path: Path, rows):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def test_validator_uses_final_page_truth_not_stale_manifest(tmp_path: Path):
    out = tmp_path / "o"; (out / "manifests").mkdir(parents=True); (out / "exalted").mkdir(parents=True)
    (out / "manifests" / "exalted.manifest.json").write_text(json.dumps({"page_count": 659, "pages_ok": 58, "pages_ocr_needed": 2}), encoding="utf-8")
    rows = ([{"book_id": "exalted", "page": i+1, "page_status": "ok", "reason_code": "native_text_extracted"} for i in range(644)] +
            [{"book_id": "exalted", "page": 645+i, "page_status": "ocr_needed", "reason_code": "image_only_no_ocr"} for i in range(13)] +
            [{"book_id": "exalted", "page": 658+i, "page_status": "queued", "reason_code": "backend_extraction_empty"} for i in range(2)])
    _write_jsonl(out / "exalted" / "exalted.page_truth.jsonl", rows)
    (out / "exalted" / "strict_audit.json").write_text(json.dumps({"strict_audit_status": "pass", "status_counts": {"ok": 644, "ocr_needed": 13, "queued": 2}, "unaccounted_page_count": 0}), encoding="utf-8")
    (out / "exalted" / "astra_handoff_manifest.json").write_text(json.dumps({"pages_ok": 644, "pages_ocr_needed": 13, "pages_queued": 2}), encoding="utf-8")

    old = sys.argv; sys.argv = ["validate_outputs.py", "--output-dir", str(out), "--strict"]
    try: validate_outputs.main()
    finally: sys.argv = old
    s = json.loads((out / "corpus_validation_summary.json").read_text())
    assert s["pages_ok"] == 644
    assert s["pages_ocr_needed"] == 13
    assert s["pages_queued"] == 2


def test_validator_fails_on_strict_audit_mismatch(tmp_path: Path):
    out = tmp_path / "o2"; (out / "manifests").mkdir(parents=True); (out / "exalted").mkdir(parents=True)
    (out / "manifests" / "exalted.manifest.json").write_text(json.dumps({"page_count": 659}), encoding="utf-8")
    rows = [{"book_id": "exalted", "page": i+1, "page_status": "ok", "reason_code": "native_text_extracted"} for i in range(659)]
    _write_jsonl(out / "exalted" / "exalted.page_truth.jsonl", rows)
    (out / "exalted" / "strict_audit.json").write_text(json.dumps({"strict_audit_status": "fail", "status_counts": {"ok": 60}, "unaccounted_page_count": 599}), encoding="utf-8")
    (out / "exalted" / "astra_handoff_manifest.json").write_text(json.dumps({"pages_ok": 60}), encoding="utf-8")

    old = sys.argv; sys.argv = ["validate_outputs.py", "--output-dir", str(out), "--strict"]
    try: validate_outputs.main()
    finally: sys.argv = old
    s = json.loads((out / "corpus_validation_summary.json").read_text())
    assert s["books_artifact_invalid"] == 1
    assert "strict_audit_disposition_mismatch" in s["top_error_codes"] or "strict_audit_failed" in s["top_error_codes"]
