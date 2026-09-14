# Executable validation for PR2-SCALE runtime scalability governance.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/doctrine/control/myravant_runtime_scalability_execution_topology_contract.md"
MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"
SIMEX_CLOSURE_TEST = ROOT / "tests/test_pr2_simex_post_merge_closure.py"

BASE = "5268f85135b9ad5d67719b37305b204554729bed"
MERGE = "862ee41369ec8cba5768cb13aa59ecd853a7f8c4"
AUTH = "owner_directive_2026-09-14_pr2_scale_activation"
EFFECT = "runtime_architecture_contract_only"
CONTROL = "docs/doctrine/control/myravant_runtime_scalability_execution_topology_contract.md"
OWNED = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/control/myravant_runtime_scalability_execution_topology_contract.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_scale_runtime_scalability_contract.py",
    "tests/test_pr2_simex_post_merge_closure.py",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(manifest):
    return {row["workstream_id"]: row for row in manifest["workstreams"]}


def read_at(ref, path):
    return subprocess.check_output(
        ["git", "show", f"{ref}:{path.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    )


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def test_contract_declares_bounded_runtime_architecture_authority():
    text = read_at(MERGE, CONTRACT)
    assert "artifact_id: PR2-SCALE-RUNTIME-SCALABILITY-EXECUTION-TOPOLOGY-001" in text
    assert f"authority_reference: {AUTH}" in text
    assert f"authority_effect: {EFFECT}" in text
    assert f"starting_baseline: {BASE}" in text
    for token in (
        "runtime_implementation_authority: none",
        "distributed_runtime_implementation_authority: none",
        "production_schema_authority: none",
        "partitioning_semantics_authority: none",
        "concurrency_semantics_authority: none",
        "fidelity_semantics_authority: none",
        "event_delivery_semantics_authority: none",
        "persistence_recovery_semantics_authority: none",
        "performance_budget_authority: none",
    ):
        assert token in text


def test_topology_independence_and_nontransfer_are_explicit():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "Logical simulation semantics must remain independent of physical execution topology.",
        "A physical execution boundary does not create semantic authority.",
        "No semantic owner transfers merely because data or computation moves.",
        "No worker-count semantics",
        "No machine-count semantics",
        "Physical ordering is not authoritative ordering",
    ):
        assert token in text


def test_reference_execution_is_role_not_technology_mandate():
    text = read_at(MERGE, CONTRACT)
    assert "reference-execution role" in text
    assert "semantic/evaluation role, not a permanent technology mandate" in text
    assert "PR2-SCALE does not claim that a complete conforming reference runtime already exists." in text
    for token in (
        "fastest;",
        "most scalable;",
        "distributed;",
        "the final data layout;",
        "the final scheduling model.",
    ):
        assert token in text


def test_scale_claims_require_context():
    text = read_at(MERGE, CONTRACT)
    assert "Scale is multidimensional" in text
    assert "Workload-envelope law" in text
    assert "one million dormant records" in text
    assert "one million actively interacting actors" in text
    assert '"supports one million entities"' in text
    assert '"supports MMO scale"' in text


def test_technology_choices_are_not_mandated():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "microservices;",
        "Entity Component Systems;",
        "actor systems;",
        "event sourcing;",
        "database choice;",
        "message-bus choice;",
        "cloud-provider choice;",
        "GPU or accelerator mandates;",
    ):
        assert token in text
    assert "No distributed-by-default law" in text
    assert "No architecture-fashion voting" in text


def test_downstream_runtime_owners_remain_separate():
    text = read_at(MERGE, CONTRACT)
    for workstream_id in (
        "PR2-PART",
        "PR2-CONC",
        "PR2-FID",
        "PR2-EVENT",
        "PR2-PERSIST",
        "PR2-BP",
    ):
        assert f"PR2-SCALE does not activate {workstream_id}." in text
    assert "PR2-SCALE must not manufacture certainty before downstream contracts exist." in text


def test_equivalence_can_fail_closed():
    text = read_at(MERGE, CONTRACT)
    for token in (
        "`equivalent_within_declared_envelope`",
        "`equivalent_with_declared_constraints`",
        "`not_equivalent`",
        "`inconclusive_missing_downstream_contract`",
        "`inconclusive_missing_evidence`",
        "`unsupported_topology`",
    ):
        assert token in text
    assert "Unsupported topology is lawful" in text
    assert "prefer an explicit unsupported boundary over false equivalence" in text


def test_manifest_activates_only_scale_and_preserves_downstream_blocks():
    manifest = load_at(MERGE, MAN)
    by = rows(manifest)
    scale = by["PR2-SCALE"]

    assert manifest["artifact_version"] == "0.4.27"
    assert scale["status"] == "active"
    assert scale["authorization_reference"] == AUTH
    assert scale["authority_effect"] == EFFECT
    assert scale["starting_baseline"] == BASE
    assert scale["control_artifact"] == CONTROL
    assert set(scale["owned_paths"]) == OWNED
    assert scale["pull_request"] is None
    assert scale["branch_head"] is None
    assert scale["merge_commit"] is None

    active = {
        row["workstream_id"]
        for row in manifest["workstreams"]
        if row["status"] == "active"
    }
    assert active == {"PR2-SCALE"}

    assert by["PR2-SIMEX"]["status"] == "merged"

    for workstream_id in (
        "PR2-PART",
        "PR2-CONC",
        "PR2-FID",
        "PR2-EVENT",
        "PR2-PERSIST",
        "PR2-BP",
        "PR2-AUDIT",
        "PR2-MIG",
        "PR2-TEST",
        "PR2-IMPL",
    ):
        assert by[workstream_id]["status"] == "blocked"
        assert by[workstream_id]["authorization_reference"] is None

    assert manifest["r2_gate_state"]["R3"] == "ready_pending_authorization"
    assert manifest["r3_conformance_target"]["candidate_count"] == 34
    assert manifest["r3_conformance_target"]["execution_authorized"] is False


def test_simex_closure_is_frozen_as_historical_snapshot():
    text = read_at(MERGE, SIMEX_CLOSURE_TEST)
    assert f'CLOSURE_SNAPSHOT = "{BASE}"' in text
    assert text.count("load_at(CLOSURE_SNAPSHOT, MAN)") == 2
    assert "read_at(CLOSURE_SNAPSHOT, PROG)" in text
    assert "read_at(CLOSURE_SNAPSHOT, DEC)" in text


def test_program_and_decision_record_activation_without_implementation_authority():
    program = read_at(MERGE, PROG)
    decisions = read_at(MERGE, DEC)

    assert "**Artifact version:** `0.4.27`" in program
    assert "### 5.24 PR2-SCALE runtime scalability and execution-topology activation" in program
    assert AUTH in program
    assert BASE in program
    assert CONTROL in program
    assert "PR2-SCALE is the only active successor workstream." in program
    assert "No downstream runtime workstream is activated by this decision." in program

    assert "PR2-SCALE-ACTIVATION-001" in decisions
    assert AUTH in decisions
    assert EFFECT in decisions
    assert BASE in decisions
    assert "does not authorize distributed runtime implementation" in decisions
    assert "does not activate PR2-PART" in decisions
