from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VALID_RESULT_STATUSES = {"placeholder", "drafted", "final"}
VALID_LAWFUL_OUTCOMES = {
    "direct Astra mapping",
    "normalized Astra mapping",
    "source-local retained construct",
    "quarantined construct pending later doctrine",
    "escalated doctrine problem",
}
REQUIRED_RUN_DIRS = ["packets", "prompts", "results", "validation", "reports"]
REQUIRED_AGGREGATION_FILES = [
    "batch_001_aggregation_report.json",
    "batch_001_aggregation_report.md",
    "batch_001_doctrine_pressure_report.md",
    "batch_001_source_local_retention_report.md",
    "batch_001_quarantine_escalation_queue.csv",
    "batch_001_human_review_queue.csv",
    "batch_001_construct_family_summary.csv",
    "batch_001_packet_aggregation_table.csv",
]

DISALLOWED_CANON_PHRASES = [
    "final canon promotion",
    "canonical adoption",
    "canonized",
    "approved canon",
    "live-play authority",
    "sourcebook merge",
]
ALLOWLIST_CANON_PHRASES = [
    "not canon",
    "review required",
    "canon permission: review_required",
    "conversion permission is not canon permission",
]

UNRESOLVED_PATTERNS = [
    "$batchRoot",
    "$batchRun",
    "$zipPath",
    "$stamp",
    "ConvertTo-Json",
    "@{",
    "<TODO>",
    "TODO placeholder",
    "FIXME",
]


class Collector:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def _safe_load_json(path: Path, c: Collector) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        c.err(f"json_parse_error:{path}:{exc}")
        return None


def _contains_unresolved_placeholder(text: str) -> str | None:
    for token in UNRESOLVED_PATTERNS:
        if token in text:
            return token
    if re.search(r"\{\{[^}]+\}\}", text):
        return "{{...}}"
    if re.search(r"\$\{[^}]+\}", text):
        return "${...}"
    return None


def validate(run_dir: Path, strict: bool) -> dict[str, Any]:
    c = Collector()
    summary: dict[str, Any] = {}

    for d in REQUIRED_RUN_DIRS:
        if not (run_dir / d).exists():
            c.err(f"missing_required_directory:{d}")

    idx_path = run_dir / "packet_index.json"
    indexed_ids: list[str] = []
    idx: list[dict[str, Any]] = []
    if idx_path.exists():
        loaded = _safe_load_json(idx_path, c)
        if isinstance(loaded, list):
            idx = loaded
        else:
            c.err("packet_index_not_list")
        seen = set()
        for row in idx:
            pid = row.get("packet_id")
            if not isinstance(pid, str) or not pid:
                c.err("invalid_packet_id_type")
                continue
            if "/" in pid or "\\" in pid:
                c.err(f"packet_id_has_path_separator:{pid}")
            if pid in seen:
                c.err(f"duplicate_packet_id:{pid}")
            seen.add(pid)
            indexed_ids.append(pid)
        packet_dirs = [p.name for p in (run_dir / "packets").iterdir()] if (run_dir / "packets").exists() else []
        if packet_dirs and len(packet_dirs) != len(indexed_ids):
            c.warn(f"packet_count_mismatch:index={len(indexed_ids)}:discovered={len(packet_dirs)}")
    else:
        c.warn("packet_index_missing_optional")

    results_dir = run_dir / "results"
    prompts_dir = run_dir / "prompts"

    result_json_by_pid: dict[str, list[Path]] = {}
    result_md_by_pid: dict[str, list[Path]] = {}
    status_counts: Counter[str] = Counter()

    for p in results_dir.glob("*.bak_before_*"):
        c.err(f"stale_backup_artifact:{p.name}")

    for p in results_dir.glob("*_conversion_result.json"):
        pid = p.name.removesuffix("_conversion_result.json")
        result_json_by_pid.setdefault(pid, []).append(p)
    for p in results_dir.glob("*_conversion_result.md"):
        pid = p.name.removesuffix("_conversion_result.md")
        result_md_by_pid.setdefault(pid, []).append(p)

    for pid in indexed_ids:
        prompt = prompts_dir / f"{pid}_conversion_prompt.md"
        prompt_bundle = prompts_dir / pid
        if not prompt.exists() and not prompt_bundle.exists():
            c.err(f"missing_prompt_or_bundle:{pid}")

        j = result_json_by_pid.get(pid, [])
        m = result_md_by_pid.get(pid, [])
        if len(j) != 1:
            c.err(f"result_json_count_not_one:{pid}:{len(j)}")
        if m and len(m) != 1:
            c.err(f"result_md_count_not_one:{pid}:{len(m)}")

    for pid in result_json_by_pid:
        if indexed_ids and pid not in indexed_ids:
            c.err(f"non_index_result_json:{pid}")

    for pid in indexed_ids:
        paths = result_json_by_pid.get(pid, [])
        if len(paths) != 1:
            continue
        obj = _safe_load_json(paths[0], c)
        if not isinstance(obj, dict):
            c.err(f"result_json_not_object:{pid}")
            continue

        for field in ["packet_id", "result_status", "mapping_ledger"]:
            if field not in obj:
                c.err(f"missing_required_result_field:{pid}:{field}")

        st = obj.get("result_status")
        if st not in VALID_RESULT_STATUSES:
            c.err(f"invalid_result_status:{pid}:{st}")
        else:
            status_counts[st] += 1
            if strict and st == "placeholder":
                c.err(f"placeholder_status_in_strict:{pid}")

        ml = obj.get("mapping_ledger", [])
        if not isinstance(ml, list):
            c.err(f"mapping_ledger_not_list:{pid}")
            ml = []
        for i, entry in enumerate(ml):
            if not isinstance(entry, dict):
                c.err(f"mapping_entry_not_object:{pid}:{i}")
                continue
            if entry.get("donor_construct"):
                lo = entry.get("lawful_outcome")
                if lo not in VALID_LAWFUL_OUTCOMES:
                    c.err(f"invalid_lawful_outcome:{pid}:{i}:{lo}")

        conf = obj.get("confidence")
        if conf is not None and not (isinstance(conf, (int, float)) and 0.0 <= float(conf) <= 1.0):
            c.err(f"invalid_confidence:{pid}:{conf}")

        for arr_field in [
            "doctrine_escalations",
            "source_local_retentions",
            "rejected_imports",
            "canon_candidate_notes",
            "reviewer_notes",
        ]:
            if arr_field in obj and not isinstance(obj.get(arr_field), list):
                c.err(f"field_not_list:{pid}:{arr_field}")

        blob = json.dumps(obj, ensure_ascii=False).lower()
        if not any(p in blob for p in ALLOWLIST_CANON_PHRASES):
            for phrase in DISALLOWED_CANON_PHRASES:
                if phrase in blob:
                    c.err(f"canon_leakage_phrase:{pid}:{phrase}")

    scan_dirs = [run_dir / "reports", run_dir / "validation"]
    for base in scan_dirs:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in {".md", ".json", ".txt", ".csv"}:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            token = _contains_unresolved_placeholder(text)
            if token:
                c.err(f"unresolved_placeholder:{p.relative_to(run_dir)}:{token}")

    agg_dir = run_dir / "reports" / "aggregation"
    if agg_dir.exists():
        for fname in REQUIRED_AGGREGATION_FILES:
            if not (agg_dir / fname).exists():
                c.err(f"missing_aggregation_report:{fname}")

        agg_json_path = agg_dir / "batch_001_aggregation_report.json"
        if agg_json_path.exists():
            agg = _safe_load_json(agg_json_path, c)
            if isinstance(agg, dict):
                packets_total = agg.get("packets_total")
                rsc = agg.get("result_status_counts")
                if isinstance(packets_total, int) and isinstance(rsc, dict):
                    total = sum(v for v in rsc.values() if isinstance(v, int))
                    if packets_total != total:
                        c.err(f"aggregation_packets_total_mismatch:{packets_total}:{total}")
                outcomes = agg.get("lawful_outcome_counts", {})
                if isinstance(outcomes, dict):
                    for k, v in outcomes.items():
                        if not isinstance(v, int) or v < 0:
                            c.err(f"invalid_lawful_outcome_count:{k}:{v}")
                hq = agg.get("human_review_queue_count")
                if hq is not None and (not isinstance(hq, int) or hq < 0):
                    c.err(f"invalid_human_review_queue_count:{hq}")
                out_dir = agg.get("output_dir")
                if out_dir and not Path(out_dir).exists():
                    c.err(f"aggregation_output_dir_missing:{out_dir}")

    summary["indexed_packets"] = len(indexed_ids)
    summary["result_status_counts"] = dict(status_counts)
    summary["step8_mojibake_note"] = "Generated-report mojibake scanning is reserved for Step 8."

    return {
        "valid": len(c.errors) == 0,
        "strict": strict,
        "run_dir": str(run_dir),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "error_count": len(c.errors),
        "warning_count": len(c.warnings),
        "errors": c.errors,
        "warnings": c.warnings,
        "summary": summary,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--output-json")
    args = ap.parse_args()

    report = validate(Path(args.run_dir), strict=bool(args.strict))
    output = json.dumps(report, indent=2, ensure_ascii=False)
    print(output)
    if args.output_json:
        Path(args.output_json).write_text(output + "\n", encoding="utf-8")

    if args.strict and not report["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
