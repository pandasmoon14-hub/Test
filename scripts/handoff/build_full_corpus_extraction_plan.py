from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _parse_overlay(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    current = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("- pattern_id:"):
            if current:
                out.append(current)
            current = {"pattern_id": s.split(":", 1)[1].strip()}
        elif current and s.startswith("match_terms:"):
            v = s.split(":", 1)[1].strip().strip("[]")
            current["match_terms"] = [x.strip() for x in v.split(",") if x.strip()]
        elif current and s.startswith("suggested_donor_family_candidates:"):
            v = s.split(":", 1)[1].strip().strip("[]")
            current["suggested_donor_family_candidates"] = [x.strip() for x in v.split(",") if x.strip()]
    if current:
        out.append(current)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run-dir", required=True)
    ap.add_argument("--preflight-review-dir", required=True)
    ap.add_argument("--readiness-gate-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--output-json")
    ap.add_argument("--pilot-size", type=int, default=24)
    ap.add_argument("--template-batch-size", type=int, default=96)
    ap.add_argument("--mixed-batch-size", type=int, default=240)
    ap.add_argument("--use-routing-overlay", action="store_true")
    ap.add_argument("--require-readiness-valid", action="store_true")
    ap.add_argument("--allow-ready-with-warnings", action="store_true")
    args = ap.parse_args()

    dry = Path(args.dry_run_dir)
    pre = Path(args.preflight_review_dir)
    gate = Path(args.readiness_gate_dir)
    out = Path(args.output_dir)
    strict = bool(args.strict)

    errors: list[str] = []
    warnings: list[str] = []
    output_files: list[str] = []

    files_total = planned_files = review_queue_count = overlay_applied_count = 0
    lane_counts: Counter[str] = Counter()
    wave_counts: Counter[str] = Counter()

    try:
        if not dry.exists(): errors.append("missing_dry_run_dir")
        if not pre.exists(): errors.append("missing_preflight_review_dir")
        if not gate.exists(): errors.append("missing_readiness_gate_dir")

        dry_req = [
            "full_corpus_dry_run_manifest.json",
            "full_corpus_dry_run_manifest.csv",
            "full_corpus_preflight_issues.csv",
            "full_corpus_donor_family_estimates.csv",
            "full_corpus_dry_run_report.md",
        ]
        pre_req = [
            "full_corpus_preflight_review_summary.json",
            "full_corpus_preflight_review_report.md",
            "full_corpus_issue_triage.csv",
            "full_corpus_unclassified_clusters.csv",
        ]
        gate_req = [
            "full_corpus_readiness_gate_summary.json",
            "full_corpus_readiness_gate_report.md",
            "full_corpus_readiness_gate_checks.csv",
            "full_corpus_next_action_plan.md",
        ]
        for fn in dry_req:
            if not (dry / fn).exists(): errors.append(f"missing_required_file:{fn}")
        for fn in pre_req:
            if not (pre / fn).exists(): errors.append(f"missing_required_file:{fn}")
        for fn in gate_req:
            if not (gate / fn).exists(): errors.append(f"missing_required_file:{fn}")

        if errors and strict:
            raise RuntimeError("missing required files")

        manifest = _read_json(dry / "full_corpus_dry_run_manifest.json")
        manifest_csv = _read_csv(dry / "full_corpus_dry_run_manifest.csv")
        issues_csv = _read_csv(dry / "full_corpus_preflight_issues.csv")
        family_csv = _read_csv(dry / "full_corpus_donor_family_estimates.csv")
        gate_summary = _read_json(gate / "full_corpus_readiness_gate_summary.json")

        if args.require_readiness_valid and not bool(gate_summary.get("valid")):
            errors.append("readiness_gate_not_valid")
        rs = gate_summary.get("readiness_status", "blocked")
        if rs == "ready_with_warnings" and not args.allow_ready_with_warnings:
            errors.append("ready_with_warnings_not_allowed")

        issue_by_path = defaultdict(set)
        for r in issues_csv:
            issue_by_path[r.get("path", "")].add(r.get("issue_code", ""))
        family_map = {r.get("relative_path", ""): r for r in family_csv}

        overlay = []
        overlay_path = pre / "donor_family_routing_overlay_proposal.yaml"
        if args.use_routing_overlay and overlay_path.exists():
            overlay = _parse_overlay(overlay_path)

        supported_paths = {r.get("relative_path", "") for r in manifest_csv if str(r.get("supported", "")).lower() in {"true", "1"}}
        plan_rows = []
        review_rows = []

        for idx, f in enumerate(manifest.get("files", []), start=1):
            rel = f.get("relative_path", "")
            if rel not in supported_paths:
                continue
            planned_files += 1
            fam = family_map.get(rel, {})
            donor = fam.get("donor_family_candidates", "unclassified_or_mixed_donor_family")
            confidence = fam.get("confidence", fam.get("donor_family_confidence", "low"))
            repair = fam.get("repair_queue_candidates", "")
            issue_codes = sorted(c for c in issue_by_path.get(rel, set()) if c)
            overlay_applied = False
            overlay_pattern_ids = []
            review_required = False

            if args.use_routing_overlay and overlay:
                for o in overlay:
                    terms = [t.lower() for t in o.get("match_terms", [])]
                    if any(t and t in rel.lower() for t in terms):
                        if "unclassified_or_mixed_donor_family" in donor:
                            sug = o.get("suggested_donor_family_candidates", [])
                            if sug:
                                donor = "|".join(sug)
                                overlay_applied = True
                                overlay_pattern_ids.append(o.get("pattern_id", "unknown"))
                                review_required = True
                        break

            donor_l = donor.lower()
            repair_l = repair.lower()
            lane = "lane_a_standard_native_candidate"
            if "very_long_path" in issue_codes or "suspicious_temporary_fragment" in issue_codes:
                lane = "lane_e_manual_review_hold"
            elif "unusually_large_file" in issue_codes:
                lane = "lane_b_large_or_layout_risk"
            elif any(x in repair_l for x in ["scanned_or_image_only", "low_confidence_extraction", "map_diagram_review"]):
                lane = "lane_c_visual_map_or_scan_review"
            elif any(x in donor_l for x in ["random_table_loot", "bestiary_statblock_heavy", "gear_item_catalog", "magic_spell_power_compendium"]):
                lane = "lane_d_table_statblock_catalog_risk"

            if lane == "lane_e_manual_review_hold":
                wave = "wave_00_manual_triage"
            elif idx <= args.pilot_size:
                wave = "wave_01_pilot_review_batch"
            elif idx <= args.pilot_size + args.template_batch_size:
                wave = "wave_02_donor_family_template_batch"
            elif idx <= args.pilot_size + args.template_batch_size + args.mixed_batch_size:
                wave = "wave_03_mixed_pressure_batch"
            else:
                wave = "wave_04_full_corpus_orchestrated_run"

            if "unclassified_or_mixed_donor_family" in donor or confidence == "low" or overlay_applied or "unusually_large_file" in issue_codes or "very_long_path" in issue_codes or "suspicious_temporary_fragment" in issue_codes or any(x in repair_l for x in ["scan", "image", "map"]):
                review_required = True

            notes = "planning-only metadata"
            row = {
                "plan_id": f"plan_{idx:05d}",
                "relative_path": rel,
                "absolute_path": f.get("absolute_path", ""),
                "file_name": f.get("file_name", Path(rel).name),
                "extension": f.get("extension", Path(rel).suffix.lower()),
                "size_bytes": f.get("size_bytes", 0),
                "donor_family_candidates": donor,
                "confidence": confidence,
                "repair_queue_candidates": repair,
                "issue_codes": "|".join(issue_codes),
                "overlay_candidate_applied": str(overlay_applied),
                "overlay_pattern_ids": "|".join(overlay_pattern_ids),
                "extraction_lane": lane,
                "extraction_wave": wave,
                "review_required": str(review_required),
                "planning_notes": notes,
            }
            plan_rows.append(row)
            lane_counts[lane] += 1
            wave_counts[wave] += 1
            if overlay_applied:
                overlay_applied_count += 1
            if review_required:
                review_queue_count += 1
                review_rows.append({
                    "plan_id": row["plan_id"],
                    "relative_path": rel,
                    "reason": "|".join(filter(None, [
                        "unclassified" if "unclassified_or_mixed_donor_family" in donor else "",
                        "low_confidence" if confidence == "low" else "",
                        "overlay_applied" if overlay_applied else "",
                        "large_file" if "unusually_large_file" in issue_codes else "",
                        "very_long_path" if "very_long_path" in issue_codes else "",
                        "suspicious_fragment" if "suspicious_temporary_fragment" in issue_codes else "",
                        "scan_map_risk" if any(x in repair_l for x in ["scan", "image", "map"]) else "",
                        "non_ascii_path" if "non_ascii_path" in issue_codes else "",
                    ])),
                })

        files_total = len(manifest.get("files", []))

        out.mkdir(parents=True, exist_ok=True)
        manifest_json = out / "full_corpus_extraction_plan_manifest.json"
        manifest_csv_out = out / "full_corpus_extraction_plan_manifest.csv"
        batches_csv = out / "full_corpus_extraction_batches.csv"
        lane_csv = out / "full_corpus_extraction_lane_summary.csv"
        review_csv = out / "full_corpus_extraction_review_queue.csv"
        report_md = out / "full_corpus_extraction_plan_report.md"
        summary_json = out / "full_corpus_extraction_plan_summary.json"

        manifest_json.write_text(json.dumps({"records": plan_rows}, indent=2, ensure_ascii=True), encoding="utf-8")
        output_files.append(str(manifest_json))
        _write_csv(manifest_csv_out, plan_rows, list(plan_rows[0].keys()) if plan_rows else [
            "plan_id","relative_path","absolute_path","file_name","extension","size_bytes","donor_family_candidates","confidence","repair_queue_candidates","issue_codes","overlay_candidate_applied","overlay_pattern_ids","extraction_lane","extraction_wave","review_required","planning_notes"
        ])
        output_files.append(str(manifest_csv_out))

        batch_rows = [{"extraction_wave": k, "count": v} for k, v in sorted(wave_counts.items())]
        _write_csv(batches_csv, batch_rows, ["extraction_wave", "count"])
        output_files.append(str(batches_csv))

        lane_rows = [{"extraction_lane": k, "count": v} for k, v in sorted(lane_counts.items())]
        _write_csv(lane_csv, lane_rows, ["extraction_lane", "count"])
        output_files.append(str(lane_csv))

        _write_csv(review_csv, review_rows, ["plan_id", "relative_path", "reason"])
        output_files.append(str(review_csv))

        manual_hold = [r for r in plan_rows if r["extraction_lane"] == "lane_e_manual_review_hold"][:20]
        large = sorted(plan_rows, key=lambda x: int(x.get("size_bytes", 0)), reverse=True)[:20]
        unclassified = [r for r in plan_rows if "unclassified_or_mixed_donor_family" in r["donor_family_candidates"]][:20]

        report_lines = [
            "# Full Corpus Extraction Plan Report",
            "",
            "## Plan Summary",
            f"- files_total: {files_total}",
            f"- planned_files: {planned_files}",
            f"- readiness_status: {rs}",
            f"- overlay_applied_count: {overlay_applied_count}",
            f"- review_queue_count: {review_queue_count}",
            "",
            "## Input Paths",
            f"- dry_run_dir: {dry}",
            f"- preflight_review_dir: {pre}",
            f"- readiness_gate_dir: {gate}",
            "",
            "## Lane Counts",
        ]
        report_lines += [f"- {k}: {v}" for k, v in sorted(lane_counts.items())] or ["- none"]
        report_lines += ["", "## Wave Counts"]
        report_lines += [f"- {k}: {v}" for k, v in sorted(wave_counts.items())] or ["- none"]
        report_lines += ["", "## Top Manual Hold Examples"]
        report_lines += [f"- {r['relative_path']}" for r in manual_hold] or ["- none"]
        report_lines += ["", "## Top Large-File Examples"]
        report_lines += [f"- {r['relative_path']} ({r['size_bytes']} bytes)" for r in large] or ["- none"]
        report_lines += ["", "## Top Unclassified Examples"]
        report_lines += [f"- {r['relative_path']}" for r in unclassified] or ["- none"]
        report_lines += [
            "",
            "## Recommended Next Actions",
            "- Review manual-hold and review-queue entries before extraction starts.",
            "- Refine routing overlay where unclassified/low-confidence remains high.",
            "- Confirm lane and wave sequencing in operations runbook.",
            "",
            "This plan does not extract, OCR, convert, or canonize.",
            "Dry-run routing metadata is not extraction truth.",
            "Extraction planning is not extraction truth.",
            "Extraction truth is not conversion permission.",
            "Conversion permission is not canon permission.",
        ]
        report_md.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        output_files.append(str(report_md))

        summary = {
            "valid": len(errors) == 0,
            "strict": strict,
            "dry_run_dir": str(dry),
            "preflight_review_dir": str(pre),
            "readiness_gate_dir": str(gate),
            "output_dir": str(out),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "files_total": files_total,
            "planned_files": planned_files,
            "lane_counts": dict(lane_counts),
            "wave_counts": dict(wave_counts),
            "review_queue_count": review_queue_count,
            "overlay_applied_count": overlay_applied_count,
            "output_files": output_files,
            "errors": errors,
            "warnings": warnings,
            "summary": {
                "readiness_status": rs,
                "planning_only_note": "No extraction, OCR, packet building, LLM calls, or conversion are performed.",
            },
        }
        summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=True), encoding="utf-8")
        output_files.append(str(summary_json))

    except Exception as exc:
        summary = {
            "valid": False,
            "strict": strict,
            "dry_run_dir": str(dry),
            "preflight_review_dir": str(pre),
            "readiness_gate_dir": str(gate),
            "output_dir": str(out),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "files_total": files_total,
            "planned_files": planned_files,
            "lane_counts": dict(lane_counts),
            "wave_counts": dict(wave_counts),
            "review_queue_count": review_queue_count,
            "overlay_applied_count": overlay_applied_count,
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
