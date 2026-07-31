"""Deterministic validation for the bounded, nonauthoritative R2A-1 contract."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "9382958197c9d5dee9d29cb5f9d051147237c64d"
REVIEWS = ROOT / "docs/doctrine/reviews"
CONTRACT_PATH = REVIEWS / "afqr_r2a_inventory_contract.yaml"
PARTITIONS_PATH = REVIEWS / "afqr_r2a_partition_manifest.yaml"
CLUSTERS_PATH = REVIEWS / "afqr_r2a_controlled_search_clusters.yaml"
FILE_MANIFEST_PATH = REVIEWS / "afqr_r2_doctrine_drift_file_manifest.yaml"
PLAN_PATH = ROOT / "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md"
AUTHORIZED = {
    "docs/doctrine/reviews/afqr_r2a_inventory_contract.yaml",
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "docs/doctrine/reviews/afqr_r2a_controlled_search_clusters.yaml",
    "docs/doctrine/reviews/afqr_r2_doctrine_drift_file_manifest.yaml",
    "docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md",
    "tests/test_afqr_r2a_inventory_contract.py",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def changed_paths() -> set[str]:
    committed = subprocess.check_output(
        ["git", "diff", "--name-only", f"{BASE}...HEAD"], cwd=ROOT, text=True
    ).splitlines()
    worktree = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=ROOT, text=True
    ).splitlines()
    return set(committed) | {row[3:] for row in worktree if row[:2].strip()}


def test_exact_base_and_authorized_change_boundary():
    assert subprocess.check_output(["git", "merge-base", BASE, "HEAD"], cwd=ROOT, text=True).strip() == BASE
    assert load(CONTRACT_PATH)["inspected_base_commit"] == BASE
    assert changed_paths() == AUTHORIZED
    assert not any(path.startswith(("src/", "schemas/", "tests/runtime/")) for path in changed_paths())


def test_record_contracts_have_purpose_fields_controls_rules_and_prohibitions():
    contract = load(CONTRACT_PATH)
    expected = set(contract["controlled_values"]["record_types"])
    assert expected == set(contract["record_types"])
    for name, record in contract["record_types"].items():
        assert record["purpose"] and record["required_fields"]
        assert record["field_controls"] and record["validation_rules"] and record["prohibited_uses"], name
    assert contract["status"] in contract["controlled_values"]["statuses"]
    outcomes = contract["controlled_values"]["assessment_outcomes"]
    assert len(outcomes) == len(set(outcomes)) == 7
    for name in ("claim_assessment", "unresolved_question_assessment", "package_assessment", "module_assessment"):
        assert contract["record_types"][name]["field_controls"]["assessment_outcome"] == "controlled_values.assessment_outcomes"


def test_surface_locator_and_candidate_disposition_controls_are_substantive():
    contract = load(CONTRACT_PATH)
    surface = contract["record_types"]["semantic_authority_surface"]
    assert surface["field_controls"]["line_start"] == "positive_integer"
    assert "greater_than_or_equal_to_line_start" in surface["field_controls"]["line_end"]
    assert surface["field_controls"]["excerpt_sha256"] == "lowercase_sha256_64_hex"
    assert "keyword match is insufficient" in " ".join(surface["validation_rules"])
    candidate = contract["record_types"]["candidate_file_disposition"]
    rules = " ".join(candidate["validation_rules"] + candidate["prohibited_uses"])
    assert "Exactly one disposition" in rules
    assert "One committed record per raw occurrence is prohibited" in rules
    assert "Generic dismissal" in rules and "no mapped surface" in rules


def test_claim_evidence_and_positive_links_are_typed_and_reciprocal():
    contract = load(CONTRACT_PATH)
    evidence = set(contract["claim_evidence_fields"]["required"])
    assert evidence == {
        "surface_ids", "relevant_current_normative_surface_ids",
        "relevant_current_control_surface_ids", "relevant_schema_runtime_test_surface_ids",
        "relevant_historical_or_source_local_surface_ids", "negative_or_absence_evidence_surface_ids",
    }
    links = contract["positive_link_fields"]
    assert set(links["required"]) == {"surface_id", "relevance_type", "semantic_role", "exact_relevance", "owner_boundary_effect"}
    assert links["controls"]["relevance_type"] == "controlled_values.relevance_types"
    claim_rules = " ".join(contract["record_types"]["claim_assessment"]["validation_rules"])
    assert "structured evidence" in claim_rules and "reciprocal" in claim_rules and "claim-specific" in claim_rules


def test_search_clusters_and_receipt_algorithm_are_deterministic_without_counts():
    clusters = load(CLUSTERS_PATH)
    expected = {
        "commitment_and_transition", "identity_and_continuity", "time_and_causality",
        "evidence_and_provenance", "dependency_and_revalidation",
        "truth_knowledge_belief_projection", "correction_retcon_supersession",
        "branch_fork_merge_replay", "reservation_settlement_conservation",
        "action_conflict_targeting", "sensing_contact_visibility", "embodiment_injury_recovery",
        "environmental_state_process", "canon_conversion_cross_phase", "runtime_storage_serialization",
    }
    assert {row["cluster_id"] for row in clusters["clusters"]} == expected
    for row in clusters["clusters"]:
        assert row["terms"] and row["term_matching"] and row["expected_false_positive_families"] and row["owner_families_to_inspect"]
    assert clusters["rules"]["occurrence_tuple"] == ["path", "line_number", "normalized_term", "cluster_id"]
    assert "not doctrine" in clusters["rules"]["authority"]
    algorithm = load(CONTRACT_PATH)["canonical_scan_receipt_algorithm"]
    assert algorithm["tuple_fields"] == clusters["rules"]["occurrence_tuple"]
    assert algorithm["encoding"] == "UTF-8" and algorithm["delimiter"] == "\\t" and algorithm["record_terminator"] == "\\n"
    assert algorithm["digest"].startswith("SHA-256")
    forbidden_count_keys = {"total_occurrence_count", "total_candidate_file_count", "count_by_term", "count_by_cluster", "sha256"}
    assert not forbidden_count_keys.intersection(load(CLUSTERS_PATH))


def test_partition_dependencies_gates_precedence_and_coordination_boundaries():
    manifest = load(PARTITIONS_PATH)
    rows = manifest["partitions"]
    assert manifest["partition_count"] == len(rows) == 8
    assert [row["partition_id"] for row in rows] == [f"R2A-{number}" for number in range(1, 9)]
    for row in rows:
        assert row["dependency_partitions"] and row["gate_effect"] and row["completion_condition"] and row["prohibited_work"]
    precedence = manifest["ownership_rules"]["disposition_precedence"]
    assert [entry.split()[0] for entry in precedence] == ["R2A-4", "R2A-5", "R2A-6"]
    assert "first matching" in manifest["ownership_rules"]["overlap_resolution"]
    disposition_rows = {row["partition_id"]: row for row in rows[3:6]}
    assert "files already owned by R2A-4" in disposition_rows["R2A-5"]["excluded_path_families"]
    assert set(disposition_rows["R2A-6"]["excluded_path_families"]) == {"files owned by R2A-4", "files owned by R2A-5"}
    assert manifest["ownership_rules"]["coordination_domain_ownership"] == []
    assert set(load(CONTRACT_PATH)["responsibility_ownership"]["coordination_must_not_own"]) == set(manifest["ownership_rules"]["coordination_must_not_own"])


def test_cross_file_sequence_registration_and_lawful_gate_posture():
    file_manifest = load(FILE_MANIFEST_PATH)
    sequence = file_manifest["r2a_reconstruction_sequence"]
    assert [row["partition_id"] for row in sequence] == [f"R2A-{number}" for number in range(1, 9)]
    assert sequence[0]["status"] == "active_incomplete"
    assert {row["status"] for row in sequence[1:]} == {"planned_not_present"}
    registered = {row["path"]: row for row in file_manifest["artifacts"]}
    for path in (CONTRACT_PATH, PARTITIONS_PATH, CLUSTERS_PATH):
        assert registered[str(path.relative_to(ROOT))]["current_status"] == "active_incomplete"
    planned = [row for row in file_manifest["artifacts"] if row.get("phase", "").startswith("R2A-") and row["phase"] != "R2A-1"]
    assert len(planned) == 7 and all(row["status"] == "planned_not_present" for row in planned)
    posture = load(CONTRACT_PATH)["project_posture"]
    assert posture == {"R1": "complete", "R2": "active_incomplete", "R2-0": "complete", "R2A": "active_incomplete", "R2B": "blocked", "R2C": "blocked", "R3-R6": "blocked", "RT-002G": "unauthorized", "temporary_evidence_deletion": "unauthorized"}
    plan = PLAN_PATH.read_text(encoding="utf-8")
    for marker in ("`R2A=active_incomplete`", "`R2B=blocked`", "`R2C=blocked`", "`R3–R6=blocked`", "`RT-002G=unauthorized`", "`temporary_evidence_deletion=unauthorized`"):
        assert marker in plan
    assert "PR #342 was closed without merge" in plan and "isolated local commit is repository authority" in plan
    assert load(CONTRACT_PATH)["status"] != "complete"
    assert all(row["status"] != "complete" for row in sequence)


def test_changed_files_have_no_deletions_binary_content_or_limit_violations():
    assert not subprocess.check_output(
        ["git", "diff", "--name-status", "--diff-filter=D", BASE], cwd=ROOT, text=True
    ).strip()
    for relative in changed_paths():
        raw = (ROOT / relative).read_bytes()
        assert b"\0" not in raw
        assert len(raw) <= 300 * 1024
        assert max(map(len, raw.splitlines()), default=0) <= 1000
    numstat = subprocess.check_output(["git", "diff", "--numstat", BASE], cwd=ROOT, text=True)
    assert "-\t-\t" not in numstat
    assert len(changed_paths()) <= 7
    assert sum(int(row.split("\t")[0]) for row in numstat.splitlines() if row) <= 2500
