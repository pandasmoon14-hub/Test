# Executable validation for PR2-TEST terminal completion closure.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = (
    ROOT
    / "docs/doctrine/control/"
    "post_r2a_transition_manifest.yaml"
)

PROG = (
    ROOT
    / "docs/doctrine/control/"
    "post_r2a_transition_program.md"
)

DEC = ROOT / "docs/decisions/current_decisions_log.md"

REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_test_seven_family_completion_assessment.yaml"
)

ASSESSMENT_TEST = (
    ROOT
    / "tests/"
    "test_pr2_test_seven_family_completion_assessment.py"
)

PR = 423

HEAD = (
    "6781782bda0405648d658ec07bccce68f68e4ff7"
)

MERGE = (
    "54cb6c459585011dfbee11ad0510c24cb2d0fe3f"
)

TREE = (
    "c0f40093e399e94efcaa402442cbfae1168d83ec"
)

CI_RUN = 246
CI_RUN_ID = 35456472681

AUTH = (
    "owner_directive_2026-09-19_"
    "pr2_test_completion_post_merge_closure"
)

EFFECT = (
    "post_r2_test_completion_post_merge_"
    "lifecycle_reconciliation_only"
)

HANDOFF_IDS = [
    "PR2-TEST-HANDOFF-TOPOLOGY-001",
    "PR2-TEST-HANDOFF-PERSIST-001",
    "PR2-TEST-HANDOFF-FIDELITY-001",
    "PR2-TEST-HANDOFF-BP-001",
    "PR2-TEST-HANDOFF-FAILURE-001",
]


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


def test_pr2_test_is_terminal_at_accepted_assessment_merge():
    data = load(MAN)
    test = rows(data)["PR2-TEST"]

    assert data["artifact_version"] == "0.4.62"

    assert test["status"] == "merged"

    assert (
        test["completion_state"]
        == "merged_complete_with_future_implementation_handoffs"
    )

    assert test["pull_request"] == PR
    assert test["branch_head"] == HEAD
    assert test["merge_commit"] == MERGE

    assert test["completion_assessment_pull_request"] == PR
    assert test["completion_assessment_branch_head"] == HEAD
    assert test["completion_assessment_merge_commit"] == MERGE
    assert test["completion_assessment_merge_tree"] == TREE


def test_terminal_closure_metadata_is_exact():
    data = load(MAN)
    test = rows(data)["PR2-TEST"]

    assert (
        test["completion_post_merge_closure_authorization_reference"]
        == AUTH
    )

    assert (
        test["completion_post_merge_closure_authority_effect"]
        == EFFECT
    )

    assert (
        test["completion_post_merge_closure_recorded_from"]
        == MERGE
    )

    assert (
        test["completion_post_merge_closure_tree"]
        == TREE
    )

    assert (
        test["completion_post_merge_closure_ci_run"]
        == CI_RUN
    )

    assert (
        test["completion_post_merge_closure_ci_run_id"]
        == CI_RUN_ID
    )

    assert (
        f"PR2-TEST completion assessment "
        f"GitHub Actions CI #{CI_RUN}:success"
        in test["validation_evidence"]
    )


def test_five_future_implementation_handoffs_are_preserved():
    data = load(MAN)
    test = rows(data)["PR2-TEST"]

    assert test["residual_gaps"] == HANDOFF_IDS

    handoffs = test["future_implementation_handoffs"]

    assert [
        row["handoff_id"]
        for row in handoffs
    ] == HANDOFF_IDS

    assert all(
        row["route"] == "PR2-IMPL"
        for row in handoffs
    )

    assert all(
        row["gap_class"] == "future_implementation"
        for row in handoffs
    )

    assert all(
        row["pr2_test_blocking"] is False
        for row in handoffs
    )


def test_pr2_impl_is_ready_but_not_authorized():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    assert impl["status"] == "ready_pending_authorization"
    assert impl["authorization_reference"] is None
    assert impl["starting_baseline"] is None

    assert impl["readiness_source"] == "PR2-TEST"
    assert impl["readiness_recorded_from"] == MERGE
    assert impl["readiness_handoff_ids"] == HANDOFF_IDS

    assert impl["implementation_handoff_authorized"] is False


def test_r4_and_runtime_authority_remain_closed():
    data = load(MAN)
    by = rows(data)

    test = by["PR2-TEST"]

    assert test["runtime_implementation_authorized"] is False
    assert test["production_schema_authorized"] is False
    assert test["pr2_impl_authorized"] is False
    assert test["r4_b_authorized"] is False
    assert test["runtime_promotion_authorized"] is False

    r4 = data["r4_native_substrate_design_target"]

    assert r4["r4_b_ready_pending_authorization"] is False
    assert r4["r4_b_authorized"] is False
    assert r4["r4_activation_authorized"] is False
    assert r4["implementation_authorized"] is False
    assert r4["runtime_promotion_clear"] is False

    assert data["r2_gate_state"]["R4-R6"] == "blocked"

    assert (
        data["r3_conformance_target"]["runtime_promotion_clear"]
        is False
    )


def test_assessment_artifact_is_unchanged_by_terminal_closure():
    current = load(REVIEW)

    accepted = json.loads(
        read_at(
            MERGE,
            REVIEW,
        )
    )

    assert current == accepted


def test_assessment_regression_is_frozen_at_accepted_merge():
    text = ASSESSMENT_TEST.read_text(
        encoding="utf-8",
    )

    assert (
        f'ACCEPTED_MERGE = "{MERGE}"'
        in text
    )

    assert "def read_at(" in text

    assert (
        "read_at(\n"
        "            ACCEPTED_MERGE,"
        in text
    )


def test_program_and_decision_record_terminal_closure():
    program = PROG.read_text(
        encoding="utf-8",
    )

    decisions = DEC.read_text(
        encoding="utf-8",
    )

    assert "**Artifact version:** `0.4.62`" in program

    assert (
        "### 5.58 PR2-TEST terminal completion "
        "post-merge closure"
        in program
    )

    for token in (
        AUTH,
        EFFECT,
        f"`#{PR}`",
        HEAD,
        MERGE,
        TREE,
        f"`#{CI_RUN}`",
        f"`{CI_RUN_ID}`",
        "PR2-TEST is terminal.",
        "PR2-IMPL now becomes `ready_pending_authorization`.",
        "R4-B remains not ready pending authorization",
        "Runtime promotion remains uncleared.",
    ):
        assert token in program

    assert (
        "PR2-TEST-COMPLETION-POST-MERGE-CLOSURE-001"
        in decisions
    )

    for token in (
        "**PR2-TEST status:** `merged`",
        (
            "**PR2-TEST completion state:** "
            "`merged_complete_with_future_implementation_handoffs`"
        ),
        "**Future implementation handoffs preserved:** `5`",
        "**PR2-IMPL status:** `ready_pending_authorization`",
        "**PR2-IMPL authorized:** `false`",
        "**R4-B ready pending authorization:** `false`",
        "**R4-B authorized:** `false`",
        "**Runtime promotion authorized:** `false`",
    ):
        assert token in decisions


def test_previous_initial_activation_closure_is_preserved():
    data = load(MAN)
    test = rows(data)["PR2-TEST"]

    assert (
        test["post_merge_closure_recorded_from"]
        == "0b3720ffdabd68744cec31e9b0da3aae50913972"
    )

    assert (
        test["post_merge_closure_tree"]
        == "2a9b783ce64110c89197702c5d4e08bd069fdb72"
    )

def test_terminal_closure_validation_evidence_is_exact():
    data = load(MAN)
    test = rows(data)["PR2-TEST"]

    required = {
        "PR2-TEST terminal completion closure focused pre-certification:58 passed",
        "PR2-TEST terminal completion closure broader PR2 regression:379 passed",
        (
            "PR2-TEST terminal completion closure full local repository suite:"
            "9310 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        "PR2-TEST terminal completion closure focused post-suite regression:58 passed",
        "PR2-TEST terminal completion closure git diff --check:clean",
        "PR2-TEST terminal completion closure exact six-file footprint:PASS",
        "PR2-TEST terminal completion closure runtime/schema noninterference:PASS",
    }

    assert required.issubset(
        set(test["validation_evidence"])
    )

    certification = test[
        "completion_post_merge_closure_validation"
    ]

    assert certification["focused_pre_certification"] == {
        "passed": 58,
        "result": "pass",
    }

    assert certification["broader_pr2_regression"] == {
        "passed": 379,
        "result": "pass",
    }

    assert certification["full_repository_suite"] == {
        "passed": 9310,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "result": "pass",
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
    }

    assert certification["focused_post_suite_regression"] == {
        "passed": 58,
        "result": "pass",
    }

    assert certification["git_diff_check"] == "clean"
    assert certification["changed_path_count"] == 6
    assert certification["runtime_implementation_path_count"] == 0
    assert certification["production_schema_path_count"] == 0

    program = PROG.read_text(
        encoding="utf-8",
    )

    decisions = DEC.read_text(
        encoding="utf-8",
    )

    assert (
        "#### PR2-TEST terminal completion post-merge "
        "closure validation evidence"
        in program
    )

    assert (
        "PR2-TEST-COMPLETION-POST-MERGE-"
        "CLOSURE-VALIDATION-002"
        in decisions
    )
