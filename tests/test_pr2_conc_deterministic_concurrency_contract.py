# Executable validation for PR2-CONC deterministic concurrency governance.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/doctrine/control/myravant_deterministic_concurrency_scheduling_contract.md"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
PART_CLOSURE_TEST = ROOT / "tests/test_pr2_part_post_merge_closure.py"

BASE = "0c24b4dad5e2f8e35b93cfb38632c5d3fb92b96a"
MERGE = "5752de38f432c59f9e603ffd1ef38384e621a407"
AUTH = "owner_directive_2026-09-14_pr2_conc_activation"
EFFECT = "runtime_concurrency_contract_only"
CONTROL = "docs/doctrine/control/myravant_deterministic_concurrency_scheduling_contract.md"
OWNED = {
    "docs/decisions/current_decisions_log.md",
    CONTROL,
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_conc_deterministic_concurrency_contract.py",
    "tests/test_pr2_part_post_merge_closure.py",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_at(ref, path):
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    )


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def test_contract_declares_bounded_concurrency_authority():
    text = read_at(MERGE, CONTRACT)
    assert "artifact_id: PR2-CONC-DETERMINISTIC-CONCURRENCY-SCHEDULING-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASE}" in text
    for token in (
        "runtime_implementation_authority: none",
        "production_schema_authority: none",
        "semantic_commitment_owner_authority: none",
        "command_identity_authority: none",
        "logical_time_authority: none",
        "event_delivery_semantics_authority: none",
        "persistence_recovery_semantics_authority: none",
        "fidelity_semantics_authority: none",
        "performance_budget_authority: none",
    ):
        assert token in text


def test_existing_semantic_owners_are_preserved():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "AFQR-01 retains qualified state/write ownership",
        "commitment, recovery, replay",
        "AFQR-02 retains command identity",
        "retry identity",
        "AFQR-04 retains logical time",
        "simultaneity, scheduling",
        "deterministic resolution groups",
        "It does not become the semantic commitment",
    ):
        assert token in text


def test_scheduler_and_physical_order_are_nonauthoritative():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "Core concurrency nonauthority law",
        "physical concurrency",
        "!= semantic simultaneity",
        "physical completion order",
        "!= authoritative order",
        "Scheduler nonauthority",
        "Message arrival nonauthority",
        "Wall-clock nonauthority",
    ):
        assert token in text


def test_determinism_does_not_erase_lawful_randomness_or_choice():
    text = read_at(MERGE, CONTRACT)
    assert "Determinism means runtime-authority determinism" in text
    for token in (
        "dice, cards",
        "explicit player choice",
        "GM-authorized choice",
        "Concurrency must not become a hidden randomizer.",
        "Recompute cannot reroll committed randomness",
    ):
        assert token in text


def test_independence_conflict_and_commitment_are_bounded():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "Independently computable work",
        "Independence is not permanent commutativity",
        "Candidate computation is not commitment",
        "Concurrency conflict classification",
        "Missing conflict doctrine fails closed",
        "Commitment remains owner-qualified",
        "One concurrent attempt must not manufacture duplicate commitment",
    ):
        assert token in text


def test_logical_time_and_simultaneous_groups_are_not_reowned():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "Semantic simultaneity may execute sequentially",
        "Physical concurrency may represent semantic sequence",
        "Ordered work must preserve authoritative order",
        "Simultaneous groups require group-law preservation",
        "PR2-CONC does not define stale-command semantics.",
    ):
        assert token in text


def test_cross_partition_concurrency_consumes_part_without_technology_mandate():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "Cross-partition concurrency consumes PR2-PART",
        "Cross-partition interaction still requires one lawful outcome",
        "distributed transactions, two-phase commit, consensus",
        "These are possible implementation techniques, not doctrine.",
        "Split-brain cannot be resolved by fastest response",
    ):
        assert token in text


def test_downstream_owners_remain_separate():
    text = read_at(MERGE, CONTRACT)
    for wid in ("PR2-EVENT", "PR2-PERSIST", "PR2-FID", "PR2-BP"):
        assert f"PR2-CONC does not activate {wid}." in text
    assert "PR2-CONC does not:" in text
    assert "execute R3;" in text
    assert "change the record count;" in text


def test_manifest_activates_only_conc_and_preserves_r3():
    manifest = load_at(MERGE, MAN)
    by = rows(manifest)
    conc = by["PR2-CONC"]

    assert manifest["artifact_version"] == "0.4.31"
    assert by["PR2-PART"]["status"] == "merged"
    assert conc["status"] == "active"
    assert conc["authorization_reference"] == AUTH
    assert conc["authority_effect"] == EFFECT
    assert conc["starting_baseline"] == BASE
    assert conc["control_artifact"] == CONTROL
    assert set(conc["owned_paths"]) == OWNED
    assert conc["downstream_handoff"] == ["PR2-EVENT"]
    assert conc["pull_request"] is None
    assert conc["branch_head"] is None
    assert conc["merge_commit"] is None

    active = {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    }
    assert active == {"PR2-CONC"}

    for wid in (
        "PR2-EVENT", "PR2-PERSIST", "PR2-FID", "PR2-BP",
        "PR2-AUDIT", "PR2-MIG", "PR2-TEST", "PR2-IMPL",
    ):
        assert by[wid]["status"] == "blocked"
        assert by[wid]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_part_closure_is_frozen_as_historical_snapshot():
    text = read_at(MERGE, PART_CLOSURE_TEST)
    assert f'CLOSURE_SNAPSHOT = "{BASE}"' in text
    assert text.count("load_at(CLOSURE_SNAPSHOT, MAN)") == 2
    assert "read_at(CLOSURE_SNAPSHOT, CONTRACT)" in text
    assert "read_at(CLOSURE_SNAPSHOT, ACTIVATION_TEST)" in text
    assert "read_at(CLOSURE_SNAPSHOT, PROG)" in text
    assert "read_at(CLOSURE_SNAPSHOT, DEC)" in text


def test_program_and_decisions_record_conc_only_activation():
    program = read_at(MERGE, PROG)
    decisions = read_at(MERGE, DEC)

    assert "**Artifact version:** `0.4.31`" in program
    assert "### 5.28 PR2-CONC deterministic concurrency and scheduling activation" in program
    assert AUTH in program
    assert BASE in program
    assert CONTROL in program
    assert "PR2-CONC is the only active successor workstream." in program
    assert "PR2-EVENT remains `blocked` and unauthorized." in program
    assert "PART -> CONC -> EVENT -> PERSIST -> FID -> BP -> R3" in program

    assert "PR2-CONC-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions
    assert "Scheduler timing does not" in decisions
    assert "does not redefine AFQR-01 commitment" in decisions
    assert "does not activate PR2-EVENT" in decisions
