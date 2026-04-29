from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

ALLOWED_STATUSES = {"ok", "empty", "image_only", "ocr_needed", "ocr_done", "queued", "failed", "repaired", "skipped"}


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
    summary = {
        "total_books": len(manifests), "books_artifact_valid": 0, "books_artifact_invalid": 0,
        "books_conversion_ready": 0, "books_ready_with_warnings": 0, "books_needing_repair": 0, "books_failed_extraction": 0,
        "total_pages": 0, "pages_ok": 0, "pages_empty": 0, "pages_image_only": 0, "pages_ocr_needed": 0, "pages_ocr_done": 0, "pages_queued": 0, "pages_failed": 0,
        "invalid_artifact_count": 0, "missing_artifact_count": 0, "top_error_codes": []
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
        required = [book_dir / "strict_audit.json", book_dir / "astra_handoff_manifest.json", book_dir / f"{book_id}.page_truth.jsonl"]
        missing = [p for p in required if not p.exists()]

        strict_errors = []
        if args.strict and missing:
            strict_errors.append("missing_required_artifact")
            summary["missing_artifact_count"] += len(missing)

        rows = _load_jsonl(book_dir / f"{book_id}.page_truth.jsonl") if (book_dir / f"{book_id}.page_truth.jsonl").exists() else None
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
                if rows is not None and sum(status_counts.values()) != len(rows):
                    strict_errors.append("status_count_mismatch")

        if strict_errors:
            summary["books_artifact_invalid"] += 1
            summary["invalid_artifact_count"] += 1
            error_codes.update(strict_errors)
            continue

        summary["books_artifact_valid"] += 1
        for k in ["pages_ok", "pages_empty", "pages_image_only", "pages_ocr_needed", "pages_ocr_done", "pages_queued", "pages_failed", "total_pages"]:
            summary[k] += int(m.get(k, 0))

        rc = m.get("reason_code_counts", {}) or {}
        error_codes.update([k for k, v in rc.items() if k != "native_text_extracted" for _ in range(int(v))])
        if m.get("pages_ocr_needed", 0) or m.get("pages_queued", 0) or m.get("pages_failed", 0) or m.get("pages_image_only", 0):
            summary["books_needing_repair"] += 1
        elif m.get("pages_empty", 0):
            summary["books_ready_with_warnings"] += 1
        else:
            summary["books_conversion_ready"] += 1

    summary["top_error_codes"] = [k for k, _ in error_codes.most_common(10)]
    rendered = json.dumps(summary, indent=2)
    (out / "corpus_validation_summary.json").write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
