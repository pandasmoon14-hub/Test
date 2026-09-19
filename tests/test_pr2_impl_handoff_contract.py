# Executable validation for PR2-IMPL activation.
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"

CONTRACT = (
    ROOT
    / "docs/doctrine/control/"
    "myravant_pr2_implementation_handoff_contract.md"
)

R4_REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_a_myravant_native_substrate_design.yaml"
)

CLOSURE = (
    ROOT
    / "tests/"
    "test_pr2_test_completion_post_merge_closure.py"
)

BASE = "a429b4a65e7118a5b102ef9357a83bf236d4b1cd"
AUTH = "owner_directive_2026-09-19_pr2_impl_activation"
EFFECT = "bounded_implementation_handoff_definition_only"

HANDOFF_IDS = ['PR2-TEST-HANDOFF-TOPOLOGY-001', 'PR2-TEST-HANDOFF-PERSIST-001', 'PR2-TEST-HANDOFF-FIDELITY-001', 'PR2-TEST-HANDOFF-BP-001', 'PR2-TEST-HANDOFF-FAILURE-001']


def load(path):
    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def rows(data):
    return {
        row["workstream_id"]: row
        for row in data["workstreams"]
    }


def flat_contract():
    return " ".join(
        CONTRACT.read_text(
            encoding="utf-8",
        ).split()
    )


def test_pr2_impl_is_only_active_post_r2_workstream():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    assert data["artifact_version"] == "0.4.63"

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == {"PR2-IMPL"}

    assert impl["status"] == "active"
    assert impl["authorization_reference"] == AUTH
    assert impl["authority_effect"] == EFFECT
    assert impl["starting_baseline"] == BASE

    assert (
        impl["completion_state"]
        == "active_bounded_implementation_handoff_definition"
    )


def test_dependencies_are_terminal():
    data = load(MAN)
    by = rows(data)

    impl = by["PR2-IMPL"]

    assert set(impl["dependencies"]) == {
        "PR2-R2C",
        "PR2-MIG",
        "PR2-TEST",
    }

    for dependency in impl["dependencies"]:
        assert by[dependency]["status"] == "merged"


def test_five_handoffs_are_preserved():
    impl = rows(load(MAN))["PR2-IMPL"]

    assert impl["readiness_handoff_ids"] == HANDOFF_IDS
    assert (
        impl["carried_future_implementation_handoffs"]
        == HANDOFF_IDS
    )

    assert (
        impl["package_rules"][
            "all_carried_handoffs_are_automatic_prerequisites"
        ]
        is False
    )


def test_gate_authority_does_not_become_implementation_authority():
    impl = rows(load(MAN))["PR2-IMPL"]

    assert impl["implementation_handoff_authorized"] is True
    assert impl["handoff_definition_authorized"] is True

    assert impl["runtime_implementation_authorized"] is False
    assert impl["production_schema_authorized"] is False
    assert impl["content_implementation_authorized"] is False
    assert impl["live_play_authorized"] is False
    assert impl["canon_promotion_authorized"] is False
    assert impl["r4_b_authorized"] is False
    assert impl["r4_activation_authorized"] is False
    assert impl["runtime_promotion_authorized"] is False


def test_r4_b_is_first_playable_candidate_but_remains_closed():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]
    r4 = data["r4_native_substrate_design_target"]

    candidate = impl["first_playable_candidate"]

    assert candidate["package"] == "R4-B"

    assert candidate["name"] == (
        "persistent_world_entity_location_"
        "representation_implementation"
    )

    assert candidate["ready_pending_authorization"] is False
    assert candidate["authorized"] is False

    assert r4["r4_b_ready_pending_authorization"] is False
    assert r4["r4_b_authorized"] is False
    assert r4["implementation_authorized"] is False
    assert r4["runtime_promotion_clear"] is False

    review = load(R4_REVIEW)

    assert (
        review["implementation_handoff"]["candidate_package"]
        == "R4-B"
    )

    assert (
        review["implementation_handoff"]["authorized"]
        is False
    )


def test_contract_is_game_led_and_bounded():
    flat = flat_contract()

    for token in (
        "playable need -> bounded capability -> executable evidence -> sustained play",
        "No carried handoff becomes a prerequisite merely because it exists.",
        "PR2-IMPL does not itself implement runtime mechanics.",
        "R4-B remains unauthorized.",
        "AFQR-18",
        "no universal world-state manager",
    ):
        assert token in flat


def test_program_and_decision_record_activation():
    program = PROG.read_text(
        encoding="utf-8",
    )

    decisions = DEC.read_text(
        encoding="utf-8",
    )

    assert "**Artifact version:** `0.4.63`" in program

    assert (
        "### 5.59 PR2-IMPL bounded implementation "
        "handoff activation"
        in program
    )

    assert "PR2-IMPL-ACTIVATION-001" in decisions

    for token in (
        "**PR2-IMPL status:** `active`",
        "**Carried future-implementation handoffs:** `5`",
        "**First playable candidate:** `R4-B`",
        "**R4-B authorized:** `false`",
        "**Runtime implementation authorized:** `false`",
        "**Production schema authorized:** `false`",
    ):
        assert token in decisions


def test_pr2_test_closure_is_snapshot_frozen():
    text = CLOSURE.read_text(
        encoding="utf-8",
    )

    assert f'ACCEPTED_MERGE = "{BASE}"' in text
    assert "read_at(" in text



def test_activation_validation_evidence_is_exact():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    required = {
        "PR2-IMPL activation focused certification:51 passed",
        "PR2-IMPL activation broader PR2 regression:388 passed",
        (
            "PR2-IMPL activation full local repository suite:"
            "9319 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        (
            "PR2-IMPL activation focused post-suite regression:"
            "51 passed"
        ),
        "PR2-IMPL activation git diff --check:clean",
        "PR2-IMPL activation exact seven-file footprint:PASS",
        "PR2-IMPL activation runtime/schema noninterference:PASS",
    }

    assert required.issubset(
        set(impl["validation_evidence"])
    )

    certification = impl["activation_validation"]

    assert certification["focused_certification"] == {
        "passed": 51,
        "result": "pass",
    }

    assert certification["broader_pr2_regression"] == {
        "passed": 388,
        "result": "pass",
    }

    assert certification["full_repository_suite"] == {
        "passed": 9319,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "result": "pass",
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
    }

    assert certification["focused_post_suite_regression"] == {
        "passed": 51,
        "result": "pass",
    }

    assert certification["git_diff_check"] == "clean"
    assert certification["changed_path_count"] == 7
    assert certification["runtime_implementation_path_count"] == 0
    assert certification["production_schema_path_count"] == 0
