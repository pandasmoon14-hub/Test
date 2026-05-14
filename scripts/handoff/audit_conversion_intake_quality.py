#!/usr/bin/env python3
"""Audit scaffolded Astra conversion-intake results for under-parsed outputs.

This is a quality gate helper. It does not validate the JSON schema; the existing
validate_conversion_intake_results.py script owns schema/contract validation.

This script answers a different question:
"Did a drafted result parse richly enough to be useful?"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _as_count(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return len(value)
    if value is None:
        return 0
    return 1


def _escaped_heading_count(markdown: str) -> int:
    return len(re.findall(r"(?m)^\s*#{0,6}\s*\d+\\\.\s+", markdown))


def _plain_required_heading_count(markdown: str) -> int:
    required = [
        "Extraction Readiness Assessment",
        "Donor Construct Inventory",
        "Astra Mapping Ledger",
        "Queue and Quarantine Actions",
        "Lexicon Delta",
        "Doctrine Escalations",
        "Source-Local Retentions",
        "Rejected Imports",
        "Canon Candidate Notes",
        "Conversion Notes",
        "Confidence and Reviewer Notes",
    ]
    count = 0
    for idx, title in enumerate(required, start=1):
        pattern = re.compile(
            rf"(?mi)^\s*#{{0,6}}\s*{idx}\s*(?:\\\.)?\.\s+{re.escape(title)}\s*$"
        )
        if pattern.search(markdown):
            count += 1
    return count


def _is_placeholder_markdown(markdown: str) -> bool:
    lower = markdown.lower()
    return (
        "paste or write the conversion-intake memo here" in lower
        or "status: placeholder" in lower
    )


def _is_low_value_backmatter(markdown: str, obj: dict[str, Any]) -> bool:
    haystack = markdown.lower()
    for key in (
        "donor_construct_inventory",
        "mapping_ledger",
        "source_local_retentions",
        "rejected_imports",
        "conversion_notes",
    ):
        value = obj.get(key)
        if value is not None:
            haystack += "\n" + json.dumps(value, ensure_ascii=False).lower()

    markers = [
        "credits/backmatter",
        "non-convertible backmatter",
        "backer",
        "supporter",
        "kickstarter",
        "credits-layout",
        "false-positive",
        "publication metadata",
    ]
    return any(marker in haystack for marker in markers)


def audit_result(json_path: Path) -> dict[str, Any]:
    obj = _read_json(json_path)
    packet_id = obj.get("packet_id") or json_path.name.replace("_conversion_result.json", "")
    md_path = json_path.with_name(f"{packet_id}_conversion_result.md")
    markdown = _read_text(md_path)

    mapping_count = _as_count(obj.get("mapping_ledger"))
    inventory_count = _as_count(obj.get("donor_construct_inventory"))
    doctrine_escalation_count = _as_count(obj.get("doctrine_escalations"))
    source_local_count = _as_count(obj.get("source_local_retentions"))
    rejected_count = _as_count(obj.get("rejected_imports"))
    canon_candidate_count = _as_count(obj.get("canon_candidate_notes"))

    status = obj.get("result_status", "unknown")
    confidence = obj.get("confidence", None)
    markdown_length = len(markdown)
    escaped_headings = _escaped_heading_count(markdown)
    required_headings = _plain_required_heading_count(markdown)
    placeholder_markdown = _is_placeholder_markdown(markdown)
    low_value_backmatter = _is_low_value_backmatter(markdown, obj)

    issues: list[dict[str, str]] = []

    if status != "drafted":
        issues.append({
            "severity": "error",
            "code": "status_not_drafted",
            "message": f"Expected result_status drafted, found {status!r}.",
        })

    if placeholder_markdown:
        issues.append({
            "severity": "error",
            "code": "placeholder_markdown",
            "message": "Markdown result still appears to contain placeholder text.",
        })

    if mapping_count <= 1 and not low_value_backmatter:
        issues.append({
            "severity": "error",
            "code": "underparsed_mapping_ledger",
            "message": "Drafted packet has <= 1 mapping ledger entry and is not marked as low-value backmatter.",
        })

    if inventory_count == 0 and not low_value_backmatter:
        issues.append({
            "severity": "error",
            "code": "missing_construct_inventory",
            "message": "Drafted packet has no donor construct inventory entries.",
        })

    if markdown_length > 5000 and mapping_count <= 1 and inventory_count <= 1 and not low_value_backmatter:
        issues.append({
            "severity": "error",
            "code": "rich_markdown_fallback_json",
            "message": "Markdown is substantial but scaffolded JSON looks fallback-level.",
        })

    if source_local_count == 0 and not low_value_backmatter:
        issues.append({
            "severity": "warning",
            "code": "missing_source_local_retentions",
            "message": "No source-local retentions were parsed; review whether donor-specific content was captured.",
        })

    if rejected_count == 0 and not low_value_backmatter:
        issues.append({
            "severity": "warning",
            "code": "missing_rejected_imports",
            "message": "No rejected imports were parsed; review whether donor canon leakage was explicitly blocked.",
        })

    if escaped_headings > 0:
        issues.append({
            "severity": "warning",
            "code": "escaped_numbered_headings",
            "message": f"Markdown contains {escaped_headings} escaped numbered heading(s). Parser should tolerate this, but cleanup is recommended.",
        })

    if markdown and required_headings < 8:
        issues.append({
            "severity": "warning",
            "code": "low_required_heading_count",
            "message": f"Only {required_headings}/11 required headings were detected in Markdown.",
        })

    return {
        "packet_id": packet_id,
        "json_path": str(json_path),
        "markdown_path": str(md_path) if md_path.exists() else None,
        "status": status,
        "confidence": confidence,
        "markdown_length": markdown_length,
        "required_heading_count": required_headings,
        "escaped_heading_count": escaped_headings,
        "low_value_backmatter": low_value_backmatter,
        "counts": {
            "mapping_ledger": mapping_count,
            "donor_construct_inventory": inventory_count,
            "doctrine_escalations": doctrine_escalation_count,
            "source_local_retentions": source_local_count,
            "rejected_imports": rejected_count,
            "canon_candidate_notes": canon_candidate_count,
        },
        "issues": issues,
    }


def audit_run(run_dir: Path) -> dict[str, Any]:
    results_dir = run_dir / "results"
    json_files = sorted(results_dir.glob("*_conversion_result.json"))

    packet_results = [audit_result(path) for path in json_files]
    issue_counter = Counter()
    severity_counter = Counter()
    status_counter = Counter()

    for result in packet_results:
        status_counter[result["status"]] += 1
        for issue in result["issues"]:
            issue_counter[issue["code"]] += 1
            severity_counter[issue["severity"]] += 1

    packets_with_errors = [
        result["packet_id"]
        for result in packet_results
        if any(issue["severity"] == "error" for issue in result["issues"])
    ]
    packets_with_warnings = [
        result["packet_id"]
        for result in packet_results
        if any(issue["severity"] == "warning" for issue in result["issues"])
    ]

    return {
        "run_dir": str(run_dir),
        "valid_quality_gate": not packets_with_errors,
        "packets_total": len(packet_results),
        "status_counts": dict(status_counter),
        "issue_counts": dict(issue_counter),
        "severity_counts": dict(severity_counter),
        "packets_with_errors": packets_with_errors,
        "packets_with_warnings": packets_with_warnings,
        "packet_results": packet_results,
    }


def write_reports(run_dir: Path, report: dict[str, Any]) -> tuple[Path, Path]:
    reports_dir = run_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    json_path = reports_dir / "conversion_intake_quality_audit.json"
    md_path = reports_dir / "conversion_intake_quality_audit.md"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Conversion Intake Quality Audit",
        "",
        f"Run directory: `{report['run_dir']}`",
        "",
        f"- valid_quality_gate: `{str(report['valid_quality_gate']).lower()}`",
        f"- packets_total: {report['packets_total']}",
        f"- status_counts: `{json.dumps(report['status_counts'], sort_keys=True)}`",
        f"- severity_counts: `{json.dumps(report['severity_counts'], sort_keys=True)}`",
        f"- issue_counts: `{json.dumps(report['issue_counts'], sort_keys=True)}`",
        "",
        "## Packets with errors",
        "",
    ]

    if report["packets_with_errors"]:
        lines.extend(f"- `{packet_id}`" for packet_id in report["packets_with_errors"])
    else:
        lines.append("- None")

    lines.extend(["", "## Packets with warnings", ""])

    if report["packets_with_warnings"]:
        lines.extend(f"- `{packet_id}`" for packet_id in report["packets_with_warnings"])
    else:
        lines.append("- None")

    lines.extend(["", "## Packet details", ""])

    for result in report["packet_results"]:
        lines.append(f"### {result['packet_id']}")
        lines.append("")
        lines.append(f"- status: `{result['status']}`")
        lines.append(f"- confidence: `{result['confidence']}`")
        lines.append(f"- low_value_backmatter: `{str(result['low_value_backmatter']).lower()}`")
        lines.append(f"- required_heading_count: {result['required_heading_count']}/11")
        lines.append(f"- escaped_heading_count: {result['escaped_heading_count']}")
        lines.append(f"- counts: `{json.dumps(result['counts'], sort_keys=True)}`")
        if result["issues"]:
            lines.append("- issues:")
            for issue in result["issues"]:
                lines.append(f"  - `{issue['severity']}` `{issue['code']}` — {issue['message']}")
        else:
            lines.append("- issues: none")
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, help="Conversion intake run directory")
    parser.add_argument(
        "--fail-on-errors",
        "--strict",
        action="store_true",
        dest="fail_on_errors",
        help="Exit nonzero if any quality-gate errors are found",
    )
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir)
    report = audit_run(run_dir)
    json_path, md_path = write_reports(run_dir, report)

    print(json.dumps({
        "valid_quality_gate": report["valid_quality_gate"],
        "packets_total": report["packets_total"],
        "status_counts": report["status_counts"],
        "severity_counts": report["severity_counts"],
        "issue_counts": report["issue_counts"],
        "packets_with_errors": report["packets_with_errors"],
        "packets_with_warnings": report["packets_with_warnings"],
        "report_json": str(json_path),
        "report_md": str(md_path),
    }, indent=2))

    if args.fail_on_errors and not report["valid_quality_gate"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
