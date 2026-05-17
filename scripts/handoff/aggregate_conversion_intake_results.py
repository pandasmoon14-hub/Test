from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

LAWFUL_OUTCOMES = (
    "direct Astra mapping",
    "normalized Astra mapping",
    "source-local retained construct",
    "quarantined construct pending later doctrine",
    "escalated doctrine problem",
)

CONSTRUCT_FAMILY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("extraction_provenance_and_handoff", ("manifest", "audit", "page truth", "extraction", "ocr", "packet", "source unit", "handoff")),
    ("player_chassis_and_character_creation", ("character creation", "character record", "player character", "chassis", "build", "priority", "archetype", "class package")),
    ("origin_kinform_culture_background", ("ancestry", "lineage", "heritage", "race", "species", "origin", "culture", "background", "metatype", "kinform")),
    ("competency_skill_profession", ("skill", "competency", "profession", "trigger", "trait", "proficiency", "expertise", "career", "lifepath")),
    ("ability_power_spell_technique", ("spell", "power", "technique", "maneuver", "ability", "cypher", "focus", "feat", "talent", "discipline", "magic", "psionic")),
    ("resource_cost_recharge_backlash", ("resource", "cost", "recharge", "cooldown", "drain", "stress", "strain", "backlash", "edge", "fate point", "plot point", "resolve")),
    ("progression_advancement_growth", ("progression", "advancement", "level", "rank", "license", "xp", "milestone", "growth", "evolution")),
    ("damage_condition_effect_survivability", ("damage", "condition", "status", "effect", "injury", "death", "healing", "recovery", "resistance", "armor", "soak")),
    ("gear_item_crafting_loot_economy", ("gear", "item", "equipment", "weapon", "armor", "loot", "treasure", "craft", "salvage", "wealth", "currency", "price", "requisition")),
    ("vehicle_platform_starship_mech", ("vehicle", "starship", "spacecraft", "ship", "mech", "frame", "mount", "platform", "drone", "robot", "installable")),
    ("creature_npc_bestiary_companion", ("creature", "monster", "npc", "bestiary", "enemy", "antagonist", "companion", "summon", "familiar")),
    ("scene_mission_adventure_scenario", ("mission", "scenario", "adventure", "quest", "encounter", "scene", "dungeon", "job", "campaign", "arc")),
    ("world_region_faction_setting", ("setting", "world", "region", "realm", "planet", "plane", "faction", "organization", "pantheon", "god", "cosmology", "lore")),
    ("hazard_environment_exploration_travel", ("hazard", "environment", "travel", "exploration", "weather", "terrain", "navigation", "journey", "wilderness", "trap")),
    ("social_reputation_institution", ("social", "reputation", "contact", "patron", "lifestyle", "status", "faction status", "institution", "relationship")),
    ("narrative_tag_aspect_meta_currency", ("aspect", "tag", "theme", "descriptor", "distinction", "asset", "complication", "clock", "move", "narrative")),
    ("random_table_generator_or_index", ("random table", "generator", "roll table", "d100", "index", "appendix", "backmatter")),
    ("safety_sensitive_content", ("safety", "content warning", "consent", "sensitive", "discrimination", "sexual", "torture", "slavery", "bigotry")),
    ("live_play_or_gm_procedure", ("gm", "game master", "referee", "mc", "arbiter", "running", "adjudication", "session", "downtime")),
)

DONOR_FAMILY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("universal_toolkit_or_generic_engine", ("basic roleplaying", "cypher", "cortex", "fate", "besm", "generic", "universal")),
    ("d20_fantasy_or_science_fantasy", ("dungeons", "dragons", "pathfinder", "starfinder", "5e", "theros", "galaxium", "phantasy star", "labyrinth")),
    ("traveller_lifepath_trade_starship", ("traveller", "2300ad", "high guard", "central supply", "robot handbook")),
    ("cyberpunk_biotech_transhuman", ("shadowrun", "cyberpunk", "otherscape", "eclipse phase", "newedo", "augment")),
    ("mech_vehicle_tactical_platform", ("lancer", "mech", "battletech", "armored", "vehicle")),
    ("wuxia_cultivation_martial", ("wuxia", "ogre gate", "wandering heroes", "exalted", "anima", "ki", "cultivation")),
    ("osr_survival_sandbox", ("into the odd", "without number", "mothership", "old-school", "osr", "sandbox")),
    ("solo_progress_or_oracle", ("ironsworn", "starforged", "solo", "oracle")),
    ("horror_investigation", ("cthulhu", "horror", "vaesen", "delta green", "alien")),
    ("jrpg_heroic_fantasy", ("fabula", "cloudbreaker", "final fantasy", "jrpg")),
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_space(value: Any) -> str:
    text = str(value or "")
    text = text.replace("\\_", "_")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def item_to_text(item: Any) -> str:
    if item is None:
        return ""
    if isinstance(item, str):
        return normalize_space(item)
    if isinstance(item, dict):
        if "text" in item:
            return normalize_space(item.get("text"))
        preferred = [
            "construct", "donor_construct", "term", "canonical_term", "action", "queue_action",
            "issue", "rationale", "recommendation", "note", "description", "owner", "status",
        ]
        parts: list[str] = []
        for key in preferred:
            if key in item and item[key] not in (None, "", []):
                parts.append(f"{key}: {normalize_space(item[key])}")
        if parts:
            return "; ".join(parts)
        return normalize_space(json.dumps(item, ensure_ascii=False, sort_keys=True))
    return normalize_space(item)


def compact_example(value: Any, limit: int = 220) -> str:
    text = item_to_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def classify_by_rules(text: str, rules: tuple[tuple[str, tuple[str, ...]], ...], fallback: str) -> str:
    haystack = text.lower()
    for label, needles in rules:
        if any(needle in haystack for needle in needles):
            return label
    return fallback


def classify_construct_family(mapping: dict[str, Any]) -> str:
    text = " ".join(
        normalize_space(mapping.get(key))
        for key in ("astra_target_family", "donor_construct", "rationale", "doctrine_owner")
    )
    return classify_by_rules(text, CONSTRUCT_FAMILY_RULES, "unclassified_or_mixed")


def classify_donor_family(result: dict[str, Any]) -> str:
    text = " ".join(normalize_space(result.get(key)) for key in ("book_id", "packet_id", "source_packet_dir"))
    return classify_by_rules(text, DONOR_FAMILY_RULES, "unclassified_or_mixed_donor_family")


def result_paths(run_dir: Path) -> list[Path]:
    results_dir = run_dir / "results"
    if not results_dir.exists():
        raise FileNotFoundError(f"Missing results directory: {results_dir}")
    return sorted(p for p in results_dir.glob("*_conversion_result.json") if p.is_file())


def counter_to_dict(counter: Counter) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def append_limited(bucket: list[Any], value: Any, limit: int) -> None:
    if len(bucket) < limit:
        bucket.append(value)


def aggregate_run(run_dir: Path, output_dir: Path | None = None, confidence_review_threshold: float = 0.67, max_examples: int = 8) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    output_dir = (output_dir or (run_dir / "reports" / "aggregation")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = result_paths(run_dir)
    if not paths:
        raise FileNotFoundError(f"No *_conversion_result.json files found under: {run_dir / 'results'}")

    result_status_counts: Counter[str] = Counter()
    lawful_outcome_counts: Counter[str] = Counter()
    canon_permission_counts: Counter[str] = Counter()
    doctrine_owner_counts: Counter[str] = Counter()
    donor_family_counts: Counter[str] = Counter()
    construct_family_counts: Counter[str] = Counter()
    construct_family_outcomes: dict[str, Counter[str]] = defaultdict(Counter)
    construct_family_target_families: dict[str, Counter[str]] = defaultdict(Counter)
    outcome_by_target_family: dict[str, Counter[str]] = defaultdict(Counter)
    outcome_by_doctrine_owner: dict[str, Counter[str]] = defaultdict(Counter)

    packet_rows: list[dict[str, Any]] = []
    construct_family_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    target_family_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)

    doctrine_escalations: list[dict[str, Any]] = []
    source_local_retentions: list[dict[str, Any]] = []
    rejected_imports: list[dict[str, Any]] = []
    queue_actions: list[dict[str, Any]] = []
    lexicon_delta: list[dict[str, Any]] = []
    quarantined_mapping_entries: list[dict[str, Any]] = []
    escalated_mapping_entries: list[dict[str, Any]] = []
    source_local_mapping_entries: list[dict[str, Any]] = []
    canon_candidate_packets: list[dict[str, Any]] = []
    human_review_queue: list[dict[str, Any]] = []

    confidence_values: list[float] = []

    for path in paths:
        result = load_json(path)
        packet_id = normalize_space(result.get("packet_id"))
        book_id = normalize_space(result.get("book_id"))
        status = normalize_space(result.get("result_status") or "unknown")
        confidence = float(result.get("confidence") or 0.0)
        page_range = result.get("page_range") or {}
        donor_family = classify_donor_family(result)

        result_status_counts[status] += 1
        donor_family_counts[donor_family] += 1
        confidence_values.append(confidence)

        packet_outcomes: Counter[str] = Counter()
        packet_construct_families: Counter[str] = Counter()
        packet_doctrine_owners: Counter[str] = Counter()

        for mapping in result.get("mapping_ledger", []) or []:
            outcome = normalize_space(mapping.get("lawful_outcome") or "unknown")
            target_family = normalize_space(mapping.get("astra_target_family") or "unknown")
            doctrine_owner = normalize_space(mapping.get("doctrine_owner") or "unassigned") or "unassigned"
            canon_permission = normalize_space(mapping.get("canon_candidate_permission") or "unknown")
            construct_family = classify_construct_family(mapping)

            lawful_outcome_counts[outcome] += 1
            packet_outcomes[outcome] += 1
            canon_permission_counts[canon_permission] += 1
            doctrine_owner_counts[doctrine_owner] += 1
            packet_doctrine_owners[doctrine_owner] += 1
            construct_family_counts[construct_family] += 1
            packet_construct_families[construct_family] += 1
            construct_family_outcomes[construct_family][outcome] += 1
            construct_family_target_families[construct_family][target_family] += 1
            outcome_by_target_family[target_family][outcome] += 1
            outcome_by_doctrine_owner[doctrine_owner][outcome] += 1

            example = {
                "packet_id": packet_id,
                "book_id": book_id,
                "donor_family": donor_family,
                "donor_construct": compact_example(mapping.get("donor_construct")),
                "astra_target_family": target_family,
                "lawful_outcome": outcome,
                "doctrine_owner": doctrine_owner,
                "canon_candidate_permission": canon_permission,
                "confidence": mapping.get("confidence"),
            }
            append_limited(construct_family_examples[construct_family], example, max_examples)
            append_limited(target_family_examples[target_family], example, max_examples)

            if outcome == "quarantined construct pending later doctrine":
                quarantined_mapping_entries.append(example | {"rationale": compact_example(mapping.get("rationale"), 320)})
            elif outcome == "escalated doctrine problem":
                escalated_mapping_entries.append(example | {"rationale": compact_example(mapping.get("rationale"), 320)})
            elif outcome == "source-local retained construct":
                source_local_mapping_entries.append(example | {"rationale": compact_example(mapping.get("rationale"), 320)})

        def collect_list(name: str, target: list[dict[str, Any]]) -> None:
            for index, item in enumerate(result.get(name, []) or [], start=1):
                text = item_to_text(item)
                if text:
                    target.append({
                        "packet_id": packet_id,
                        "book_id": book_id,
                        "donor_family": donor_family,
                        "index": index,
                        "text": text,
                    })

        collect_list("doctrine_escalations", doctrine_escalations)
        collect_list("source_local_retentions", source_local_retentions)
        collect_list("rejected_imports", rejected_imports)
        collect_list("queue_actions", queue_actions)
        collect_list("lexicon_delta", lexicon_delta)

        canon_notes = normalize_space(result.get("canon_candidate_notes"))
        if canon_notes and not canon_notes.lower().startswith("no canon candidates"):
            canon_candidate_packets.append({
                "packet_id": packet_id,
                "book_id": book_id,
                "donor_family": donor_family,
                "canon_candidate_notes": canon_notes,
            })

        review_reasons: list[str] = []
        if status not in {"drafted", "reviewed"}:
            review_reasons.append(f"status={status}")
        if confidence < confidence_review_threshold:
            review_reasons.append(f"confidence<{confidence_review_threshold}")
        if packet_outcomes.get("quarantined construct pending later doctrine", 0):
            review_reasons.append("has_quarantined_constructs")
        if packet_outcomes.get("escalated doctrine problem", 0):
            review_reasons.append("has_escalated_doctrine_problems")
        if result.get("doctrine_escalations"):
            review_reasons.append("has_doctrine_escalation_notes")
        if review_reasons:
            human_review_queue.append({
                "packet_id": packet_id,
                "book_id": book_id,
                "donor_family": donor_family,
                "confidence": confidence,
                "review_reasons": review_reasons,
                "quarantined_count": packet_outcomes.get("quarantined construct pending later doctrine", 0),
                "escalated_count": packet_outcomes.get("escalated doctrine problem", 0),
                "doctrine_escalation_note_count": len(result.get("doctrine_escalations", []) or []),
            })

        packet_rows.append({
            "packet_id": packet_id,
            "book_id": book_id,
            "donor_family": donor_family,
            "page_start": page_range.get("start_page"),
            "page_end": page_range.get("end_page"),
            "result_status": status,
            "confidence": confidence,
            "mapping_count": sum(packet_outcomes.values()),
            "outcomes": dict(packet_outcomes),
            "construct_families": dict(packet_construct_families),
            "doctrine_owners": dict(packet_doctrine_owners),
            "doctrine_escalation_count": len(result.get("doctrine_escalations", []) or []),
            "source_local_retention_count": len(result.get("source_local_retentions", []) or []),
            "rejected_import_count": len(result.get("rejected_imports", []) or []),
            "queue_action_count": len(result.get("queue_actions", []) or []),
            "lexicon_delta_count": len(result.get("lexicon_delta", []) or []),
        })

    construct_family_summary = []
    for family in sorted(construct_family_counts):
        construct_family_summary.append({
            "construct_family": family,
            "mapping_count": construct_family_counts[family],
            "outcome_counts": counter_to_dict(construct_family_outcomes[family]),
            "top_target_families": dict(construct_family_target_families[family].most_common(10)),
            "examples": construct_family_examples[family],
        })

    target_family_summary = []
    for target_family in sorted(outcome_by_target_family):
        target_family_summary.append({
            "astra_target_family": target_family,
            "mapping_count": sum(outcome_by_target_family[target_family].values()),
            "outcome_counts": counter_to_dict(outcome_by_target_family[target_family]),
            "examples": target_family_examples[target_family],
        })

    aggregation = {
        "run_dir": str(run_dir),
        "output_dir": str(output_dir),
        "packets_total": len(paths),
        "result_status_counts": counter_to_dict(result_status_counts),
        "lawful_outcome_counts": counter_to_dict(lawful_outcome_counts),
        "canon_permission_counts": counter_to_dict(canon_permission_counts),
        "doctrine_owner_counts": counter_to_dict(doctrine_owner_counts),
        "donor_family_counts": counter_to_dict(donor_family_counts),
        "confidence": {
            "avg": sum(confidence_values) / len(confidence_values),
            "min": min(confidence_values),
            "max": max(confidence_values),
            "review_threshold": confidence_review_threshold,
        },
        "packet_rows": packet_rows,
        "construct_family_summary": construct_family_summary,
        "target_family_summary": target_family_summary,
        "doctrine_pressure": {
            "doctrine_escalation_notes": doctrine_escalations,
            "escalated_mapping_entries": escalated_mapping_entries,
            "quarantined_mapping_entries": quarantined_mapping_entries,
            "outcome_by_doctrine_owner": {k: counter_to_dict(v) for k, v in sorted(outcome_by_doctrine_owner.items())},
        },
        "source_local_retention": {
            "source_local_retention_notes": source_local_retentions,
            "source_local_mapping_entries": source_local_mapping_entries,
            "rejected_imports": rejected_imports,
        },
        "queue_actions": queue_actions,
        "lexicon_delta": lexicon_delta,
        "canon_candidate_packets": canon_candidate_packets,
        "human_review_queue": human_review_queue,
    }

    write_json(output_dir / "batch_001_aggregation_report.json", aggregation)
    write_markdown_reports(output_dir, aggregation)
    write_csv_reports(output_dir, aggregation)
    return aggregation


def write_markdown_reports(output_dir: Path, aggregation: dict[str, Any]) -> None:
    lines: list[str] = []
    lines.append("# Batch 001 Conversion-Intake Aggregation Report")
    lines.append("")
    lines.append("This report aggregates conversion-intake results only. It does not promote donor material to Astra canon.")
    lines.append("")
    lines.append("## Run Summary")
    lines.append("")
    lines.append(f"- Run directory: `{aggregation['run_dir']}`")
    lines.append(f"- Packets total: {aggregation['packets_total']}")
    lines.append(f"- Result status counts: `{json.dumps(aggregation['result_status_counts'], ensure_ascii=False)}`")
    lines.append(f"- Lawful outcome counts: `{json.dumps(aggregation['lawful_outcome_counts'], ensure_ascii=False)}`")
    conf = aggregation["confidence"]
    lines.append(f"- Confidence average: {conf['avg']:.4f}")
    lines.append(f"- Confidence range: {conf['min']:.4f}-{conf['max']:.4f}")
    lines.append("")

    lines.append("## Donor-Family Pressure")
    lines.append("")
    for family, count in sorted(aggregation["donor_family_counts"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {family}: {count}")
    lines.append("")

    lines.append("## Construct-Family Summary")
    lines.append("")
    for entry in sorted(aggregation["construct_family_summary"], key=lambda e: (-e["mapping_count"], e["construct_family"])):
        lines.append(f"### {entry['construct_family']}")
        lines.append("")
        lines.append(f"- Mapping count: {entry['mapping_count']}")
        lines.append(f"- Outcome counts: `{json.dumps(entry['outcome_counts'], ensure_ascii=False)}`")
        if entry["top_target_families"]:
            lines.append(f"- Top Astra target families: `{json.dumps(entry['top_target_families'], ensure_ascii=False)}`")
        if entry["examples"]:
            lines.append("- Examples:")
            for ex in entry["examples"][:5]:
                lines.append(f"  - `{ex['packet_id']}` - {ex['lawful_outcome']} - {ex['donor_construct']}")
        lines.append("")

    doctrine = aggregation["doctrine_pressure"]
    lines.append("## Doctrine Pressure Queue")
    lines.append("")
    lines.append(f"- Doctrine escalation notes: {len(doctrine['doctrine_escalation_notes'])}")
    lines.append(f"- Escalated mapping entries: {len(doctrine['escalated_mapping_entries'])}")
    lines.append(f"- Quarantined mapping entries: {len(doctrine['quarantined_mapping_entries'])}")
    lines.append(f"- Human review queue packets: {len(aggregation['human_review_queue'])}")
    lines.append("")
    for item in aggregation["human_review_queue"][:20]:
        lines.append(f"- `{item['packet_id']}` - confidence {item['confidence']} - {', '.join(item['review_reasons'])}")
    lines.append("")

    retention = aggregation["source_local_retention"]
    lines.append("## Source-Local and Rejected Imports")
    lines.append("")
    lines.append(f"- Source-local retention notes: {len(retention['source_local_retention_notes'])}")
    lines.append(f"- Source-local mapping entries: {len(retention['source_local_mapping_entries'])}")
    lines.append(f"- Rejected import notes: {len(retention['rejected_imports'])}")
    lines.append("")

    lines.append("## Next Actions")
    lines.append("")
    lines.append("1. Review the human-review queue before any canon promotion.")
    lines.append("2. Cluster repeated doctrine escalations into candidate doctrine-work tickets.")
    lines.append("3. Keep source-local retentions and rejected imports outside canon/sourcebook layers unless later promoted by review.")
    lines.append("4. Use the construct-family summary to seed reusable donor-family templates for later batches.")
    lines.append("")
    (output_dir / "batch_001_aggregation_report.md").write_text("\n".join(lines), encoding="utf-8")

    doctrine_lines = [
        "# Batch 001 Doctrine Pressure Report",
        "",
        "Conversion-intake doctrine pressure only. This is not canon promotion.",
        "",
        f"- Doctrine escalation notes: {len(doctrine['doctrine_escalation_notes'])}",
        f"- Escalated mapping entries: {len(doctrine['escalated_mapping_entries'])}",
        f"- Quarantined mapping entries: {len(doctrine['quarantined_mapping_entries'])}",
        "",
        "## Escalated Mapping Entries",
        "",
    ]
    for item in doctrine["escalated_mapping_entries"]:
        doctrine_lines.append(f"- `{item['packet_id']}` - {item['donor_construct']} - {item.get('rationale', '')}")
    doctrine_lines.extend(["", "## Quarantined Mapping Entries", ""])
    for item in doctrine["quarantined_mapping_entries"]:
        doctrine_lines.append(f"- `{item['packet_id']}` - {item['donor_construct']} - {item.get('rationale', '')}")
    doctrine_lines.extend(["", "## Doctrine Escalation Notes", ""])
    for item in doctrine["doctrine_escalation_notes"]:
        doctrine_lines.append(f"- `{item['packet_id']}` - {item['text']}")
    (output_dir / "batch_001_doctrine_pressure_report.md").write_text("\n".join(doctrine_lines), encoding="utf-8")

    retention_lines = [
        "# Batch 001 Source-Local Retention Report",
        "",
        "Source-local retentions and rejected imports are not Astra canon.",
        "",
        "## Source-Local Mapping Entries",
        "",
    ]
    for item in retention["source_local_mapping_entries"]:
        retention_lines.append(f"- `{item['packet_id']}` - {item['donor_construct']} - {item.get('rationale', '')}")
    retention_lines.extend(["", "## Source-Local Retention Notes", ""])
    for item in retention["source_local_retention_notes"]:
        retention_lines.append(f"- `{item['packet_id']}` - {item['text']}")
    retention_lines.extend(["", "## Rejected Imports", ""])
    for item in retention["rejected_imports"]:
        retention_lines.append(f"- `{item['packet_id']}` - {item['text']}")
    (output_dir / "batch_001_source_local_retention_report.md").write_text("\n".join(retention_lines), encoding="utf-8")


def write_csv_reports(output_dir: Path, aggregation: dict[str, Any]) -> None:
    def write_rows(name: str, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
        with (output_dir / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                flat = dict(row)
                for key, value in list(flat.items()):
                    if isinstance(value, (dict, list)):
                        flat[key] = json.dumps(value, ensure_ascii=False)
                writer.writerow(flat)

    write_rows(
        "batch_001_packet_aggregation_table.csv",
        aggregation["packet_rows"],
        [
            "packet_id", "book_id", "donor_family", "page_start", "page_end", "result_status", "confidence",
            "mapping_count", "outcomes", "construct_families", "doctrine_owners", "doctrine_escalation_count",
            "source_local_retention_count", "rejected_import_count", "queue_action_count", "lexicon_delta_count",
        ],
    )
    write_rows(
        "batch_001_construct_family_summary.csv",
        aggregation["construct_family_summary"],
        ["construct_family", "mapping_count", "outcome_counts", "top_target_families", "examples"],
    )
    write_rows(
        "batch_001_human_review_queue.csv",
        aggregation["human_review_queue"],
        ["packet_id", "book_id", "donor_family", "confidence", "review_reasons", "quarantined_count", "escalated_count", "doctrine_escalation_note_count"],
    )
    write_rows(
        "batch_001_quarantine_escalation_queue.csv",
        aggregation["doctrine_pressure"]["quarantined_mapping_entries"] + aggregation["doctrine_pressure"]["escalated_mapping_entries"],
        ["packet_id", "book_id", "donor_family", "donor_construct", "astra_target_family", "lawful_outcome", "doctrine_owner", "canon_candidate_permission", "confidence", "rationale"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate Astra conversion-intake result JSON files into Batch-level review reports.")
    parser.add_argument("--run-dir", required=True, help="Path to conversion_intake_run directory.")
    parser.add_argument("--output-dir", default=None, help="Optional output directory. Defaults to <run-dir>/reports/aggregation.")
    parser.add_argument("--confidence-review-threshold", type=float, default=0.67)
    parser.add_argument("--max-examples", type=int, default=8)
    args = parser.parse_args()

    aggregation = aggregate_run(
        run_dir=Path(args.run_dir),
        output_dir=Path(args.output_dir) if args.output_dir else None,
        confidence_review_threshold=args.confidence_review_threshold,
        max_examples=args.max_examples,
    )
    print(json.dumps({
        "packets_total": aggregation["packets_total"],
        "result_status_counts": aggregation["result_status_counts"],
        "lawful_outcome_counts": aggregation["lawful_outcome_counts"],
        "human_review_queue_count": len(aggregation["human_review_queue"]),
        "output_dir": aggregation["output_dir"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

