# Executable validation for PR2-PART authority partitioning/migration governance.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/doctrine/control/myravant_authority_partitioning_migration_contract.md"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
SCALE_CLOSURE_TEST = ROOT / "tests/test_pr2_scale_post_merge_closure.py"

BASE = "26e0d5ea870ab8aac23fd0aeb0e200cd3a4bf965"
AUTH = "owner_directive_2026-09-14_pr2_part_activation"
EFFECT = "runtime_partitioning_contract_only"
CONTROL = "docs/doctrine/control/myravant_authority_partitioning_migration_contract.md"
OWNED = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/control/myravant_authority_partitioning_migration_contract.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_part_authority_partitioning_contract.py",
    "tests/test_pr2_scale_post_merge_closure.py",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def test_contract_declares_bounded_partitioning_authority():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "artifact_id: PR2-PART-AUTHORITY-PARTITIONING-MIGRATION-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASE}" in text
    for token in (
        "runtime_implementation_authority: none",
        "production_schema_authority: none",
        "concurrency_semantics_authority: none",
        "event_delivery_semantics_authority: none",
        "persistence_recovery_semantics_authority: none",
        "fidelity_semantics_authority: none",
        "performance_budget_authority: none",
    ):
        assert token in text


def test_partition_is_runtime_boundary_not_semantic_owner():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Core partition nonownership law",
        "coordination and execution-responsibility",
        "a semantic owner;",
        "a gameplay owner;",
        "a truth owner;",
        "Partitioning does not create new semantics",
    ):
        assert token in text


def test_logical_partition_identity_is_separate_from_placement_and_continuity():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Logical partition identity is not physical placement",
        "!= process identity",
        "!= host identity",
        "Partition identity is not timeline or branch identity",
        "Partition identity is not entity identity",
    ):
        assert token in text


def test_partition_model_is_not_spatial_or_technology_mandate():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "No universal partition dimension" in text
    for token in (
        "map region;",
        "planet or star system;",
        "database table;",
        "spatial, nonspatial, hybrid",
        "sharding algorithms or shard-key formulas;",
        "replication or consensus protocols;",
        "database, message-bus, or cloud-provider choice;",
    ):
        assert token in text


def test_migration_preserves_semantics_and_has_attributable_cutover():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Migration is responsibility transfer, not semantic-owner transfer",
        "Migration must have an attributable cutover basis",
        "the pre-migration responsible execution assignment;",
        "the intended post-migration assignment;",
        "the boundary at which new authoritative responsibility takes effect;",
        "No ambiguous authoritative responsibility",
    ):
        assert token in text


def test_overlap_precomputation_and_split_brain_do_not_gain_authority():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Overlap is not automatically dual authority",
        "Precomputed work does not gain commitment by migration",
        "Split-brain is an authority-risk condition, not a new game state",
        "prevent authoritative divergence",
        "PR2-PART does not prescribe a consensus mechanism.",
    ):
        assert token in text


def test_cross_partition_interactions_preserve_existing_semantics():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Cross-partition interaction law" in text
    for token in (
        "legality checks;",
        "commitment qualification;",
        "causal ordering;",
        "identity continuity;",
        "version applicability;",
        "randomness identity;",
        "hidden-information restrictions.",
    ):
        assert token in text
    assert "Partitioning does not authorize fidelity loss." in text


def test_downstream_owners_are_explicitly_preserved():
    text = CONTRACT.read_text(encoding="utf-8")
    for wid in ("PR2-CONC", "PR2-EVENT", "PR2-PERSIST", "PR2-FID", "PR2-BP"):
        assert f"PR2-PART does not activate {wid}." in text
    assert "PR2-PART does not execute R3" in text
    assert "change the frozen" in text


def test_manifest_activates_only_part_and_preserves_r3():
    manifest = load(MAN)
    by = rows(manifest)
    part = by["PR2-PART"]

    assert manifest["artifact_version"] == "0.4.29"
    assert part["status"] == "active"
    assert part["authorization_reference"] == AUTH
    assert part["authority_effect"] == EFFECT
    assert part["starting_baseline"] == BASE
    assert part["control_artifact"] == CONTROL
    assert set(part["owned_paths"]) == OWNED
    assert part["pull_request"] is None
    assert part["branch_head"] is None
    assert part["merge_commit"] is None

    active = {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    }
    assert active == {"PR2-PART"}
    assert by["PR2-SCALE"]["status"] == "merged"

    for wid in (
        "PR2-CONC", "PR2-EVENT", "PR2-PERSIST", "PR2-FID", "PR2-BP",
        "PR2-AUDIT", "PR2-MIG", "PR2-TEST", "PR2-IMPL",
    ):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_scale_closure_is_frozen_as_historical_snapshot():
    text = SCALE_CLOSURE_TEST.read_text(encoding="utf-8")
    assert f'CLOSURE_SNAPSHOT = "{BASE}"' in text
    assert text.count("load_at(CLOSURE_SNAPSHOT, MAN)") == 2
    assert "read_at(CLOSURE_SNAPSHOT, PROG)" in text
    assert "read_at(CLOSURE_SNAPSHOT, DEC)" in text
    assert "read_at(CLOSURE_SNAPSHOT, ACTIVATION_TEST)" in text
    assert "read_at(MERGE, CONTRACT)" in text


def test_program_and_decisions_record_part_only_activation():
    program = PROG.read_text(encoding="utf-8")
    decisions = DEC.read_text(encoding="utf-8")

    assert "**Artifact version:** `0.4.29`" in program
    assert "### 5.26 PR2-PART authority partitioning and migration activation" in program
    assert AUTH in program
    assert BASE in program
    assert CONTROL in program
    assert "PR2-PART is the only active successor workstream." in program
    assert "No downstream runtime workstream is activated by this decision." in program
    assert "PART -> CONC -> EVENT -> PERSIST -> FID -> BP -> R3" in program

    assert "PR2-PART-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions
    assert "does not create or transfer" in decisions
    assert "gameplay ownership" in decisions
    assert "semantic ownership" in decisions
    assert "does not activate PR2-CONC" in decisions
