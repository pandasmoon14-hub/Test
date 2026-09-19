# Executable validation for PR2-TEST initial activation.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"

CONTRACT = (
    ROOT
    / "docs/doctrine/control/"
    "myravant_post_r2_acceptance_evaluation_contract.md"
)

MIG_CLOSURE_TEST = (
    ROOT
    / "tests/test_pr2_mig_b_post_merge_closure.py"
)

BASE = "02d63b38e83000099e2654d74db0d0454bf97346"
TREE = "031d38ec2ec973cb5812dde11824b4e838cf752e"
AUTH = "owner_directive_2026-09-18_pr2_test_activation"
EFFECT = "post_r2_acceptance_evaluation_only"
ACCEPTED_MERGE = "0b3720ffdabd68744cec31e9b0da3aae50913972"

FAMILIES = [
    "source_governance",
    "originality_and_information_barrier",
    "deterministic_topology_equivalence",
    "persistence_replay_and_recovery",
    "fidelity_aggregation_and_reconstitution",
    "overload_backpressure_and_lawful_degradation",
    "failure_isolation_and_authority_ambiguity",
]

OWNED = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/control/"
    "myravant_post_r2_acceptance_evaluation_contract.md",
    "docs/doctrine/control/post_r2a_transition_manifest.yaml",
    "docs/doctrine/control/post_r2a_transition_program.md",
    "tests/test_post_r2a_transition_program.py",
    "tests/test_pr2_mig_b_post_merge_closure.py",
    "tests/test_pr2_test_acceptance_evaluation_contract.py",
}


def read_at(ref, path):
    return subprocess.check_output(
        [
            "git",
            "show",
            f"{ref}:{path.relative_to(ROOT).as_posix()}",
        ],
        cwd=ROOT,
        text=True,
    )


def load_at(ref, path):
    return json.loads(read_at(ref, path))


def load_manifest():
    return load_at(ACCEPTED_MERGE, MAN)


def rows(data):
    return {
        row["workstream_id"]: row
        for row in data["workstreams"]
    }


def flat_contract():
    return " ".join(
        read_at(
            ACCEPTED_MERGE,
            CONTRACT,
        ).split()
    )


def test_pr2_test_is_only_active_post_r2_workstream():
    data = load_manifest()
    by = rows(data)
    test = by["PR2-TEST"]

    assert data["artifact_version"] == "0.4.59"

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == {"PR2-TEST"}

    assert test["status"] == "active"
    assert test["authorization_reference"] == AUTH
    assert test["authority_effect"] == EFFECT
    assert test["starting_baseline"] == BASE

    assert test["control_artifact"] == (
        "docs/doctrine/control/"
        "myravant_post_r2_acceptance_evaluation_contract.md"
    )

    assert (
        test["completion_state"]
        == "active_evaluation_expansion"
    )

    assert test["evaluation_families"] == FAMILIES
    assert set(test["owned_paths"]) == OWNED

    assert test["pull_request"] is None
    assert test["branch_head"] is None
    assert test["merge_commit"] is None


def test_all_pr2_test_dependencies_are_terminal_merged():
    data = load_manifest()
    by = rows(data)
    test = by["PR2-TEST"]

    assert set(
        test["dependencies"]
    ) == {
        "PR2-CONC",
        "PR2-FID",
        "PR2-EVENT",
        "PR2-PERSIST",
        "PR2-BP",
    }

    for dependency in test["dependencies"]:
        assert by[dependency]["status"] == "merged"


def test_implementation_and_r4_boundaries_remain_closed():
    data = load_manifest()
    by = rows(data)
    test = by["PR2-TEST"]

    assert (
        test["runtime_implementation_authorized"]
        is False
    )
    assert (
        test["production_schema_authorized"]
        is False
    )
    assert test["pr2_impl_authorized"] is False
    assert test["r4_b_authorized"] is False
    assert test["runtime_promotion_authorized"] is False

    assert by["PR2-IMPL"]["status"] == "blocked"
    assert (
        by["PR2-IMPL"]["authorization_reference"]
        is None
    )

    assert data["r2_gate_state"]["R4-R6"] == "blocked"
    assert (
        data["r3_conformance_target"][
            "runtime_promotion_clear"
        ]
        is False
    )

    r4 = data["r4_native_substrate_design_target"]

    assert (
        r4["r4_b_ready_pending_authorization"]
        is False
    )
    assert r4["r4_b_authorized"] is False
    assert r4["implementation_authorized"] is False
    assert r4["runtime_promotion_clear"] is False


def test_migration_remains_terminal_and_exhausted():
    data = load_manifest()
    by = rows(data)
    mig = by["PR2-MIG"]

    assert mig["status"] == "merged"
    assert mig["migration_execution_authorized"] is False
    assert mig["migration_execution_scope"] == []
    assert mig["remaining_candidate_ids"] == []

    target = data["pr2_audit_completion_target"]

    assert target["current_migration_required_count"] == 0
    assert target["migration_required_candidate_ids"] == []


def test_contract_preserves_evaluation_nonauthority_law():
    flat = flat_contract()

    for required in (
        "Evaluation may demonstrate, falsify, or expose compliance; "
        "it may not create the authority, mechanic, world fact, or "
        "semantic rule being evaluated.",
        "Tests do not invent missing doctrine.",
        "Benchmark results do not create authority.",
        "Test-count growth is not an objective.",
        "No arbitrary test-count quota defines completion.",
        "It evaluates accepted owners; "
        "it does not absorb their semantic authority.",
    ):
        assert required in flat


def test_contract_covers_all_seven_pressure_families():
    text = CONTRACT.read_text(
        encoding="utf-8",
    )

    for family in FAMILIES:
        assert f"`{family}`" in text

    for required in (
        "worker-count independence",
        "partition migration",
        "committed-randomness preservation",
        "repeated fidelity cycles",
        "retry storms",
        "split-brain authority risk",
        "Authority ambiguity must fail closed or remain explicitly unsupported.",
    ):
        assert required in text


def test_player_freedom_and_persistent_world_pressure_are_preserved():
    flat = flat_contract()

    for required in (
        "fictionally coherent unusual actions",
        "closed verb menu",
        "Failure to represent an unusual action "
        "should expose a real capability gap",
        "protagonist-independent continuity",
        "lawful off-screen state",
        "PR2-TEST does not implement missing "
        "persistent-world mechanics.",
    ):
        assert required in flat


def test_program_and_decisions_record_bounded_activation():
    program = read_at(
        ACCEPTED_MERGE,
        PROG,
    )
    decisions = read_at(
        ACCEPTED_MERGE,
        DEC,
    )

    assert (
        "**Artifact version:** `0.4.59`"
        in program
    )

    assert (
        "### 5.55 PR2-TEST post-R2 acceptance and evaluation activation"
        in program
    )

    for value in (
        AUTH,
        EFFECT,
        BASE,
    ):
        assert value in program
        assert value in decisions

    assert (
        "docs/doctrine/control/"
        "myravant_post_r2_acceptance_evaluation_contract.md"
        in program
    )

    assert "PR2-TEST is now `active`" in program
    assert (
        "PR2-IMPL remains `blocked` and unauthorized."
        in program
    )

    assert (
        "PR2-TEST-ACTIVATION-001"
        in decisions
    )

    assert TREE in decisions


def test_historical_pr2_mig_b_closure_is_snapshot_frozen():
    text = read_at(
        ACCEPTED_MERGE,
        MIG_CLOSURE_TEST,
    )

    assert (
        'CLOSURE_MERGE = '
        '"02d63b38e83000099e2654d74db0d0454bf97346"'
        in text
    )

    assert (
        'CLOSURE_TREE = '
        '"031d38ec2ec973cb5812dde11824b4e838cf752e"'
        in text
    )

    assert "closure_manifest()" in text
    assert "read_at(" in text
    assert "CLOSURE_MERGE" in text
