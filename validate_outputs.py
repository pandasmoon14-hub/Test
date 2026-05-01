from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

ALLOWED_STATUSES = {"ok", "empty", "image_only", "ocr_needed", "ocr_done", "queued", "failed", "repaired", "skipped"}
NON_ERROR_REASON_CODES = {"native_text_extracted", "ocr_applied", "image_only_ocr_required"}


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_jsonl(path: Path):
    rows = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    except Exception:
        return None
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    out = Path(args.output_dir)
    manifests = list((out / "manifests").glob("*.manifest.json"))
    run_summary = _load_json(out / "run_summary.json")
    summary = {
        "total_books": int((run_summary or {}).get("books_total", len(manifests))), "books_artifact_valid": 0, "books_artifact_invalid": 0,
        "books_conversion_ready": 0, "books_ready_with_warnings": 0, "books_needing_repair": 0, "books_failed_extraction": 0,
        "books_with_lane_fallback": 0, "fallback_reason_counts": {}, "lane_fallback_counts": {},
        "total_pages": 0, "pages_ok": 0, "pages_empty": 0, "pages_image_only": 0, "pages_ocr_needed": 0, "pages_ocr_done": 0, "pages_repaired": 0, "pages_skipped": 0, "pages_queued": 0, "pages_failed": 0,
        "unaccounted_page_count": 0, "invalid_artifact_count": 0, "missing_artifact_count": 0, "reason_code_counts": {}, "failure_reason_counts": {}, "top_error_codes": []
    }
    error_codes = Counter()

    for mf in manifests:
        m = _load_json(mf)
        if not m:
            summary["books_artifact_invalid"] += 1
            summary["invalid_artifact_count"] += 1
            continue

        book_id = mf.stem.replace(".manifest", "")
        book_dir = out / book_id
        strict_audit_path = book_dir / "strict_audit.json"
        handoff_path = book_dir / "astra_handoff_manifest.json"
        pt_path = book_dir / f"{book_id}.page_truth.jsonl"
        required = [strict_audit_path, handoff_path, pt_path]
        missing = [p for p in required if not p.exists()]

        strict_errors = []
        if args.strict and missing:
            strict_errors.append("missing_required_artifact")
            summary["missing_artifact_count"] += len(missing)

        strict_audit = _load_json(strict_audit_path) if strict_audit_path.exists() else None
        handoff = _load_json(handoff_path) if handoff_path.exists() else None
        rows = _load_jsonl(pt_path) if pt_path.exists() else None
        row_status_counts = Counter()
        row_reason_counts = Counter()
        if args.strict:
            if rows is None:
                strict_errors.append("invalid_page_truth_jsonl")
            else:
                status_counts = Counter()
                for r in rows:
                    if not r.get("page_status") or not r.get("reason_code"):
                        strict_errors.append("incomplete_page_truth_fields")
                        break
                    if not (r.get("page") or r.get("page_number_one_based")) or not (r.get("book_id") or r.get("source_sha256")):
                        strict_errors.append("missing_identity_fields")
                        break
                    st = str(r.get("page_status"))
                    if st not in ALLOWED_STATUSES:
                        strict_errors.append("unknown_page_status")
                        break
                    status_counts[st] += 1
                    row_status_counts[st] += 1
                    row_reason_counts[str(r.get("reason_code"))] += 1
                if rows is not None and sum(status_counts.values()) != len(rows):
                    strict_errors.append("status_count_mismatch")
                expected_pages = int(m.get("page_count", m.get("total_pages", len(rows))))
                if rows is not None and len(rows) != expected_pages:
                    strict_errors.append("final_page_truth_count_mismatch")
                if rows is not None and sum(status_counts.values()) != expected_pages:
                    strict_errors.append("unaccounted_pages_present")
                if strict_audit and int(strict_audit.get("unaccounted_page_count", 0)) > 0:
                    strict_errors.append("unaccounted_pages_present")
                if strict_audit and strict_audit.get("strict_audit_status") != "pass":
                    strict_errors.append("strict_audit_failed")
                if strict_audit and dict(strict_audit.get("status_counts", {})) != dict(row_status_counts):
                    strict_errors.append("strict_audit_disposition_mismatch")
                if handoff:
                    handoff_counts = {
                        "ok": int(handoff.get("pages_ok", 0)),
                        "empty": int(handoff.get("pages_empty", 0)),
                        "image_only": int(handoff.get("pages_image_only", 0)),
                        "ocr_needed": int(handoff.get("pages_ocr_needed", 0)),
                        "ocr_done": int(handoff.get("pages_ocr_done", 0)),
                        "repaired": int(handoff.get("pages_repaired", 0)),
                        "queued": int(handoff.get("pages_queued", 0)),
                        "failed": int(handoff.get("pages_failed", 0)),
                        "skipped": int(handoff.get("pages_skipped", 0)),
                    }
                    if any(int(row_status_counts.get(k, 0)) != v for k, v in handoff_counts.items()):
                        strict_errors.append("manifest_disposition_mismatch")

        if strict_errors:
            summary["books_artifact_invalid"] += 1
            summary["invalid_artifact_count"] += 1
            error_codes.update(strict_errors)
            continue

        summary["books_artifact_valid"] += 1
        if handoff and bool(handoff.get("fallback_used", False)):
            summary["books_with_lane_fallback"] += 1
            fb_reason = str(handoff.get("fallback_reason") or "unknown")
            summary["fallback_reason_counts"] = dict(Counter(summary["fallback_reason_counts"]) + Counter({fb_reason: 1}))
            route = f"{handoff.get('intended_extraction_lane', 'unknown')}->{handoff.get('actual_extraction_lane', 'unknown')}"
            summary["lane_fallback_counts"] = dict(Counter(summary["lane_fallback_counts"]) + Counter({route: 1}))
        if rows is not None:
            row_status_counts = Counter(str(r.get("page_status")) for r in rows if r.get("page_status"))
            row_reason_counts = Counter(str(r.get("reason_code")) for r in rows if r.get("reason_code"))
        page_count = int(m.get("page_count", m.get("total_pages", len(rows or []))))
        summary["total_pages"] += page_count
        summary["pages_ok"] += int(row_status_counts.get("ok", 0))
        summary["pages_empty"] += int(row_status_counts.get("empty", 0))
        summary["pages_image_only"] += int(row_status_counts.get("image_only", 0))
        summary["pages_ocr_needed"] += int(row_status_counts.get("ocr_needed", 0))
        summary["pages_ocr_done"] += int(row_status_counts.get("ocr_done", 0))
        summary["pages_repaired"] += int(row_status_counts.get("repaired", 0))
        summary["pages_skipped"] += int(row_status_counts.get("skipped", 0))
        summary["pages_queued"] += int(row_status_counts.get("queued", 0))
        summary["pages_failed"] += int(row_status_counts.get("failed", 0))
        unaccounted = max(0, page_count - sum(row_status_counts.values()))
        summary["unaccounted_page_count"] += unaccounted

        summary["reason_code_counts"] = dict(Counter(summary["reason_code_counts"]) + row_reason_counts)
        error_codes.update([k for k, v in row_reason_counts.items() if k not in NON_ERROR_REASON_CODES for _ in range(int(v))])
        if row_status_counts.get("ocr_needed", 0) or row_status_counts.get("queued", 0) or row_status_counts.get("failed", 0) or row_status_counts.get("image_only", 0):
            summary["books_needing_repair"] += 1
        elif row_status_counts.get("empty", 0):
            summary["books_ready_with_warnings"] += 1
        else:
            summary["books_conversion_ready"] += 1

    summary["top_error_codes"] = [k for k, _ in error_codes.most_common(10)]
    if run_summary:
        summary["books_failed_extraction"] = max(int(summary.get("books_failed_extraction", 0)), int(run_summary.get("books_failed_extraction", 0)))
        summary["failure_reason_counts"] = dict(run_summary.get("failure_reason_counts", {}))
        error_codes.update(summary["failure_reason_counts"])
        summary["top_error_codes"] = [k for k, _ in error_codes.most_common(10)]
    rendered = json.dumps(summary, indent=2)
    (out / "corpus_validation_summary.json").write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
