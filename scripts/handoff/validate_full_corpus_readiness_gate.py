from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DRY_REQUIRED = [
    "full_corpus_dry_run_manifest.json",
    "full_corpus_dry_run_manifest.csv",
    "full_corpus_preflight_issues.csv",
    "full_corpus_donor_family_estimates.csv",
    "full_corpus_dry_run_report.md",
]
REVIEW_REQUIRED = [
    "full_corpus_preflight_review_summary.json",
    "full_corpus_preflight_review_report.md",
    "full_corpus_issue_triage.csv",
    "full_corpus_unclassified_clusters.csv",
]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _check(name: str, state: str, detail: str) -> dict[str, str]:
    return {"check_name": name, "state": state, "detail": detail}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run-dir", required=True)
    ap.add_argument("--preflight-review-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--output-json")
    ap.add_argument("--allow-unclassified-threshold", type=int)
    ap.add_argument("--require-routing-overlay", action="store_true")
    ap.add_argument("--require-no-errors", action="store_true")
    ap.add_argument("--require-tests-manifest")
    args = ap.parse_args()

    strict = bool(args.strict)
    dry = Path(args.dry_run_dir)
    pre = Path(args.preflight_review_dir)
    out = Path(args.output_dir)

    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, str]] = []
    output_files: list[str] = []

    files_total = issue_count = unclassified_count = cluster_count = overlay_records = 0

    try:
        if not dry.exists():
            errors.append("missing_dry_run_dir")
        if not pre.exists():
            errors.append("missing_preflight_review_dir")

        for fn in DRY_REQUIRED:
            if not (dry / fn).exists():
                errors.append(f"missing_required_file:{fn}")
        for fn in REVIEW_REQUIRED:
            if not (pre / fn).exists():
                errors.append(f"missing_required_file:{fn}")

        if errors and strict:
            raise RuntimeError("required inputs missing")

        dry_manifest = _read_json(dry / "full_corpus_dry_run_manifest.json")
        dry_manifest_csv = _read_csv(dry / "full_corpus_dry_run_manifest.csv")
        dry_issues_csv = _read_csv(dry / "full_corpus_preflight_issues.csv")
        dry_family_csv = _read_csv(dry / "full_corpus_donor_family_estimates.csv")
        dry_report_text = (dry / "full_corpus_dry_run_report.md").read_text(encoding="utf-8")

        review_summary = _read_json(pre / "full_corpus_preflight_review_summary.json")
        review_report_text = (pre / "full_corpus_preflight_review_report.md").read_text(encoding="utf-8")
        issue_triage_csv = _read_csv(pre / "full_corpus_issue_triage.csv")
        cluster_csv = _read_csv(pre / "full_corpus_unclassified_clusters.csv")

        overlay_path = pre / "donor_family_routing_overlay_proposal.yaml"
        overlay_exists = overlay_path.exists()
        overlay_line_count = 0
        if overlay_exists:
            overlay_line_count = sum(1 for ln in overlay_path.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("- pattern_id:") or ln.strip().startswith("pattern_id:"))

        files_total = len(dry_manifest.get("files", []))
        supported_files = sum(1 for r in dry_manifest_csv if str(r.get("supported", "")).lower() in {"true", "1"})
        issue_count = len(dry_issues_csv)
        unclassified_count = sum(1 for r in dry_family_csv if "unclassified_or_mixed_donor_family" in (r.get("donor_family_candidates") or ""))
        cluster_count = len(cluster_csv)
        overlay_records = int(review_summary.get("overlay_records", 0))

        if int(review_summary.get("files_total", files_total)) != files_total:
            warnings.append("files_total_mismatch_between_dry_run_and_review")
        if int(review_summary.get("issue_count", issue_count)) != issue_count:
            warnings.append("issue_count_mismatch_between_dry_run_and_review")
        if int(review_summary.get("unclassified_count", unclassified_count)) != unclassified_count:
            warnings.append("unclassified_count_mismatch_between_dry_run_and_review")
        if overlay_exists and overlay_records and overlay_line_count and overlay_records != overlay_line_count:
            warnings.append("overlay_record_count_mismatch")

        checks.append(_check("dry_run_valid", "pass", "dry-run inputs parsed"))
        checks.append(_check("preflight_review_valid", "pass", "preflight review inputs parsed"))
        checks.append(_check("no_strict_errors", "pass" if not errors else "fail", f"errors={len(errors)}"))
        checks.append(_check("supported_files_nonzero", "pass" if supported_files > 0 else "fail", f"supported_files={supported_files}"))
        checks.append(_check("issue_count_reviewed", "pass" if issue_triage_csv else "fail", f"triage_rows={len(issue_triage_csv)}"))
        repair_present = any((r.get("repair_queue_candidates") or "").strip() for r in dry_family_csv)
        checks.append(_check("repair_queue_estimates_present", "pass" if repair_present else "warn", f"repair_present={repair_present}"))
        checks.append(_check("unclassified_clusters_reported", "pass" if cluster_count > 0 else "warn", f"clusters={cluster_count}"))
        routing_state = "pass" if overlay_exists else ("fail" if args.require_routing_overlay else "warn")
        checks.append(_check("routing_overlay_present", routing_state, f"overlay_exists={overlay_exists}"))
        if args.require_routing_overlay and not overlay_exists:
            errors.append("required_routing_overlay_missing")

        sep_ok = all(s in review_report_text for s in [
            "Dry-run routing metadata is not extraction truth.",
            "Extraction truth is not conversion permission.",
            "Conversion permission is not canon permission.",
        ])
        checks.append(_check("separation_reminders_present", "pass" if sep_ok else "fail", f"present={sep_ok}"))

        text_blob = (dry_report_text + "\n" + review_report_text).lower()
        forbidden = ["canon permission granted", "approved canon", "canonized"]
        canon_ok = not any(x in text_blob for x in forbidden)
        checks.append(_check("no_canon_permission_language", "pass" if canon_ok else "fail", f"canon_ok={canon_ok}"))
        checks.append(_check("no_extraction_started_by_gate", "pass", "gate is reporting-only"))

        if args.allow_unclassified_threshold is not None and unclassified_count > args.allow_unclassified_threshold:
            errors.append("unclassified_threshold_exceeded")

        if args.require_no_errors and errors:
            errors.append("require_no_errors_failed")

        if args.require_tests_manifest:
            p = Path(args.require_tests_manifest)
            if not p.exists():
                errors.append("missing_required_tests_manifest")

        out.mkdir(parents=True, exist_ok=True)
        checks_csv = out / "full_corpus_readiness_gate_checks.csv"
        with checks_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["check_name", "state", "detail"])
            w.writeheader(); w.writerows(checks)
        output_files.append(str(checks_csv))

        check_counts = Counter(c["state"] for c in checks)
        readiness_status = "blocked" if errors or check_counts.get("fail", 0) > 0 else ("ready_with_warnings" if warnings or check_counts.get("warn", 0) > 0 or unclassified_count > 0 else "ready")

        report_md = out / "full_corpus_readiness_gate_report.md"
        report_md.write_text("\n".join([
            "# Full Corpus Readiness Gate Report",
            "",
            "## Final readiness summary",
            f"- readiness_status: {readiness_status}",
            f"- files_total: {files_total}",
            f"- issue_count: {issue_count}",
            f"- unclassified_count: {unclassified_count}",
            f"- cluster_count: {cluster_count}",
            f"- overlay_records: {overlay_records}",
            "",
            "## Input paths",
            f"- dry_run_dir: {dry}",
            f"- preflight_review_dir: {pre}",
            "",
            "## Pass/Warn/Fail checks",
            *[f"- {c['check_name']}: {c['state']} ({c['detail']})" for c in checks],
            "",
            "## Blocking issues",
            *([f"- {e}" for e in errors] if errors else ["- none"]),
            "",
            "## Warnings",
            *([f"- {w}" for w in warnings] if warnings else ["- none"]),
            "",
            "## Recommended next actions",
            "- Proceed to extraction planning only after reviewing top unclassified clusters and overlay proposal.",
            "- Keep routing overlay refinement active while unclassified_count remains high.",
            "",
            "This gate does not extract, OCR, convert, or canonize.",
            "Dry-run routing metadata is not extraction truth.",
            "Extraction truth is not conversion permission.",
            "Conversion permission is not canon permission.",
        ]) + "\n", encoding="utf-8")
        output_files.append(str(report_md))

        next_plan = out / "full_corpus_next_action_plan.md"
        next_plan.write_text("\n".join([
            "# Full Corpus Next Action Plan",
            "- Review overlay proposals and cluster samples.",
            "- Resolve blocking issues if any.",
            "- Proceed with extraction packet planning with warnings tracked.",
        ]) + "\n", encoding="utf-8")
        output_files.append(str(next_plan))

        summary = {
            "valid": len(errors) == 0,
            "strict": strict,
            "readiness_status": readiness_status,
            "dry_run_dir": str(dry),
            "preflight_review_dir": str(pre),
            "output_dir": str(out),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "files_total": files_total,
            "issue_count": issue_count,
            "unclassified_count": unclassified_count,
            "cluster_count": cluster_count,
            "overlay_records": overlay_records,
            "check_counts": dict(check_counts),
            "output_files": output_files,
            "errors": errors,
            "warnings": warnings,
            "summary": {
                "can_proceed_note": "Extraction planning can proceed when blocked=0; overlay refinement still recommended for high unclassified counts.",
                "separation_note": "Dry-run metadata is not extraction truth; extraction truth is not conversion permission; conversion permission is not canon permission.",
            },
        }

        summary_path = out / "full_corpus_readiness_gate_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=True), encoding="utf-8")
        output_files.append(str(summary_path))

    except Exception as exc:
        summary = {
            "valid": False,
            "strict": strict,
            "readiness_status": "blocked",
            "dry_run_dir": str(dry),
            "preflight_review_dir": str(pre),
            "output_dir": str(out),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "files_total": files_total,
            "issue_count": issue_count,
            "unclassified_count": unclassified_count,
            "cluster_count": cluster_count,
            "overlay_records": overlay_records,
            "check_counts": {},
            "output_files": output_files,
            "errors": errors + [f"unexpected_exception:{exc}"],
            "warnings": warnings,
            "summary": {},
        }

    payload = json.dumps(summary, indent=2, ensure_ascii=True)
    print(payload)
    if args.output_json:
        Path(args.output_json).write_text(payload + "\n", encoding="utf-8")

    if strict and not summary["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
