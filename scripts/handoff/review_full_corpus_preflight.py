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

REQUIRED_FILES = [
    "full_corpus_dry_run_manifest.json",
    "full_corpus_dry_run_manifest.csv",
    "full_corpus_preflight_issues.csv",
    "full_corpus_donor_family_estimates.csv",
]

SERIES_HINTS = {
    "level_up_a5e_gate_pass": ["level up", "advanced 5th", "gate pass gazette"],
    "fading_suns": ["fading suns"],
    "exalted": ["exalted"],
    "numenera_cypher": ["numenera", "cypher"],
    "age_blue_rose": ["fantasy age", "blue rose", "age system"],
    "fate_worlds_of_adventure": ["fate worlds", "worlds of adventure", "fate"],
    "pathfinder_companion_ap": ["pathfinder player companion", "adventure path", "pathfinder"],
    "starfinder": ["starfinder"],
    "shadowrun": ["shadowrun"],
    "traveller": ["traveller"],
    "without_number": ["worlds without number", "stars without number", "cities without number"],
    "anima_beyond_fantasy": ["anima beyond fantasy", "anima"],
    "dnd_5e_dmsguild": ["5e", "dnd", "d&d", "dungeon masters guild"],
    "mcdm_flee_mortals": ["mcdm", "flee mortals"],
    "warhammer_wfrp_zweihander": ["warhammer", "zweihander", "wfrp"],
    "vampire_wod_chronicles": ["vampire", "world of darkness", "chronicles of darkness"],
    "lancer": ["lancer"],
    "ironsworn_starforged": ["ironsworn", "starforged"],
}

SUGGESTED_FAMILY = {
    "level_up_a5e_gate_pass": ["d20_class_level_fantasy"],
    "fading_suns": ["d20_scifi_science_fantasy", "lifepath_trade_starship"],
    "exalted": ["magic_spell_power_compendium", "narrative_tag_aspect"],
    "numenera_cypher": ["universal_toolkit_or_generic_engine", "d20_scifi_science_fantasy"],
    "age_blue_rose": ["d20_class_level_fantasy", "narrative_tag_aspect"],
    "fate_worlds_of_adventure": ["narrative_tag_aspect"],
    "pathfinder_companion_ap": ["adventure_path_scenario", "d20_class_level_fantasy"],
    "starfinder": ["d20_scifi_science_fantasy"],
    "shadowrun": ["cyberpunk_biotech_transhuman"],
    "traveller": ["lifepath_trade_starship"],
    "without_number": ["osr_survival_sandbox"],
    "anima_beyond_fantasy": ["d20_class_level_fantasy", "magic_spell_power_compendium"],
    "dnd_5e_dmsguild": ["d20_class_level_fantasy"],
    "mcdm_flee_mortals": ["bestiary_statblock_heavy", "d20_class_level_fantasy"],
    "warhammer_wfrp_zweihander": ["mass_battle_war_campaign", "horror_investigation_social"],
    "vampire_wod_chronicles": ["horror_investigation_social", "narrative_tag_aspect"],
    "lancer": ["tactical_mech_vehicle_platform"],
    "ironsworn_starforged": ["forged_pbta_clock_playbook", "solo_procedure_heavy"],
}


def _read_csv(path: Path, required_headers: list[str] | None = None) -> list[dict[str, str]]:
    raw = path.read_text(encoding="utf-8")
    if "\x00" in raw:
        raise ValueError(f"malformed_csv_null_byte:{path}")
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if required_headers:
            headers = reader.fieldnames or []
            for h in required_headers:
                if h not in headers:
                    raise ValueError(f"malformed_csv_missing_header:{path}:{h}")
        return list(reader)


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _cluster_unclassified(paths: list[str], min_cluster_size: int) -> list[dict[str, Any]]:
    clusters = []
    for cid, terms in SERIES_HINTS.items():
        matched = [p for p in paths if any(t in p.lower() for t in terms)]
        if len(matched) >= min_cluster_size:
            clusters.append({
                "cluster_id": cid,
                "match_terms": "|".join(terms),
                "count": len(matched),
                "sample_files": matched[:10],
            })

    # fallback token clusters
    token_counts = Counter()
    token_examples = defaultdict(list)
    for p in paths:
        for t in re.findall(r"[a-zA-Z0-9]+", p.lower()):
            if len(t) >= 5:
                token_counts[t] += 1
                if len(token_examples[t]) < 5:
                    token_examples[t].append(p)
    for tok, c in token_counts.most_common(50):
        if c >= min_cluster_size and not any(tok in cl["match_terms"] for cl in clusters):
            clusters.append({"cluster_id": f"token_{tok}", "match_terms": tok, "count": c, "sample_files": token_examples[tok]})
    return sorted(clusters, key=lambda x: x["count"], reverse=True)


def _write_overlay(path: Path, clusters: list[dict[str, Any]], max_samples: int) -> int:
    lines = ["overlay_patterns:"]
    n = 0
    for c in clusters:
        pid = c["cluster_id"]
        sugg = SUGGESTED_FAMILY.get(pid, ["unclassified_or_mixed_donor_family"])
        conf = "medium" if pid in SUGGESTED_FAMILY else "low"
        lines.append(f"  - pattern_id: {pid}")
        lines.append(f"    match_terms: [{', '.join(c['match_terms'].split('|'))}]")
        lines.append(f"    suggested_donor_family_candidates: [{', '.join(sugg)}]")
        lines.append(f"    confidence: {conf}")
        lines.append("    rationale: Filename/path recurring cluster from dry-run unclassified set.")
        samples = c["sample_files"][:max_samples]
        lines.append(f"    sample_files: [{', '.join(samples)}]")
        lines.append("    review_required: true")
        n += 1
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--output-json")
    ap.add_argument("--max-samples", type=int, default=10)
    ap.add_argument("--write-routing-overlay-proposal", action="store_true")
    ap.add_argument("--min-cluster-size", type=int, default=3)
    args = ap.parse_args()

    strict = bool(args.strict)
    dry = Path(args.dry_run_dir)
    out = Path(args.output_dir)
    errors: list[str] = []
    warnings: list[str] = []
    output_files: list[str] = []

    files_total = 0
    unclassified_count = 0
    issue_count = 0
    cluster_count = 0
    overlay_records = 0

    try:
        for req in REQUIRED_FILES:
            if not (dry / req).exists():
                errors.append(f"missing_required_file:{req}")

        if errors and strict:
            raise RuntimeError("missing required dry-run files")

        manifest = json.loads((dry / "full_corpus_dry_run_manifest.json").read_text(encoding="utf-8"))
        man_csv = _read_csv(dry / "full_corpus_dry_run_manifest.csv", ["relative_path", "supported"])
        issues_csv = _read_csv(dry / "full_corpus_preflight_issues.csv", ["issue_code", "path", "severity"])
        fam_csv = _read_csv(dry / "full_corpus_donor_family_estimates.csv", ["relative_path", "donor_family_candidates", "confidence", "repair_queue_candidates"])

        files_total = len(manifest.get("files", []))
        supported_count = sum(1 for r in man_csv if str(r.get("supported", "")).lower() in {"true", "1"})
        if supported_count and supported_count != len(fam_csv):
            warnings.append(f"supported_count_mismatch:manifest_csv={supported_count}:family_csv={len(fam_csv)}")

        issue_count = len(issues_csv)
        triage_counts = Counter((r.get("issue_code") or r.get("issue") or "unknown") for r in issues_csv)
        triage_rows = []
        for code, count in sorted(triage_counts.items()):
            triage_rows.append({"issue_code": code, "severity": "warning", "count": count})

        unclassified_rows = [r for r in fam_csv if "unclassified_or_mixed_donor_family" in (r.get("donor_family_candidates") or "")]
        unclassified_count = len(unclassified_rows)
        unclassified_paths = [r.get("relative_path", "") for r in unclassified_rows if r.get("relative_path")]
        clusters = _cluster_unclassified(unclassified_paths, args.min_cluster_size)
        cluster_count = len(clusters)

        out.mkdir(parents=True, exist_ok=True)

        triage_path = out / "full_corpus_issue_triage.csv"
        _write_csv(triage_path, triage_rows, ["issue_code", "severity", "count"])
        output_files.append(str(triage_path))

        cluster_rows = []
        for c in clusters:
            cluster_rows.append({
                "cluster_id": c["cluster_id"],
                "match_terms": c["match_terms"],
                "count": c["count"],
                "sample_files": "|".join(c["sample_files"][: args.max_samples]),
            })
        cluster_path = out / "full_corpus_unclassified_clusters.csv"
        _write_csv(cluster_path, cluster_rows, ["cluster_id", "match_terms", "count", "sample_files"])
        output_files.append(str(cluster_path))

        overlay_path = out / "donor_family_routing_overlay_proposal.yaml"
        if args.write_routing_overlay_proposal:
            overlay_records = _write_overlay(overlay_path, clusters, args.max_samples)
            output_files.append(str(overlay_path))

        report_path = out / "full_corpus_preflight_review_report.md"
        report_lines = [
            "# Full Corpus Preflight Review Report",
            "",
            "## Run Summary",
            f"- files_total: {files_total}",
            f"- issue_count: {issue_count}",
            f"- unclassified_count: {unclassified_count}",
            f"- cluster_count: {cluster_count}",
            f"- overlay_records: {overlay_records}",
            "",
            "## Issue Triage",
        ]
        report_lines += [f"- {r['issue_code']}: {r['count']}" for r in triage_rows] or ["- none"]
        report_lines += ["", "## Largest Unclassified Clusters"]
        report_lines += [f"- {c['cluster_id']}: {c['count']}" for c in clusters[:20]] or ["- none"]
        report_lines += ["", "## Proposed Overlay Summary", f"- records: {overlay_records}"]
        report_lines += ["", "## Samples for Manual Review"]
        for c in clusters[: min(10, len(clusters))]:
            report_lines.append(f"- {c['cluster_id']}: {', '.join(c['sample_files'][:3])}")
        report_lines += [
            "",
            "## Extraction Planning Readiness Recommendation",
            "- Ready for extraction planning after manual review of top clusters and issue triage groups.",
            "",
            "Dry-run routing metadata is not extraction truth.",
            "Extraction truth is not conversion permission.",
            "Conversion permission is not canon permission.",
        ]
        report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        output_files.append(str(report_path))

        summary_obj = {
            "files_total": files_total,
            "issue_count": issue_count,
            "unclassified_count": unclassified_count,
            "cluster_count": cluster_count,
            "overlay_records": overlay_records,
            "triage_counts": dict(triage_counts),
        }
        summary_path = out / "full_corpus_preflight_review_summary.json"
        summary_path.write_text(json.dumps(summary_obj, indent=2, ensure_ascii=True), encoding="utf-8")
        output_files.append(str(summary_path))

        valid = len(errors) == 0

    except Exception as exc:
        if not errors:
            errors.append(f"unexpected_exception:{exc}")
        valid = False

    result = {
        "valid": valid,
        "strict": strict,
        "dry_run_dir": str(dry),
        "output_dir": str(out),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "files_total": files_total,
        "unclassified_count": unclassified_count,
        "issue_count": issue_count,
        "cluster_count": cluster_count,
        "overlay_records": overlay_records,
        "output_files": output_files,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "review_note": "Preflight review output is routing/refinement proposal data only.",
            "separation_note": "Dry-run metadata is not extraction truth, conversion permission, or canon permission.",
        },
    }

    payload = json.dumps(result, indent=2, ensure_ascii=True)
    print(payload)
    if args.output_json:
        Path(args.output_json).write_text(payload + "\n", encoding="utf-8")

    if strict and not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
