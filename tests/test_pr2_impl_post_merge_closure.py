# Executable validation for PR2-IMPL activation post-merge closure.
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
    "myravant_pr2_implementation_handoff_contract.md"
)

ACTIVATION_TEST = (
    ROOT
    / "tests/"
    "test_pr2_impl_handoff_contract.py"
)

PR = 425
HEAD = "070daa79b9507c577424d1a9b8c4769db746753e"
MERGE = "0609657c81193cbc7b5905d38fb9efeddcb11d1d"
TREE = "a652378b901dce055dde3957d5cea5cb3663ba57"

CI_RUN = 250
CI_RUN_ID = 35469059294

AUTH = "owner_directive_2026-09-19_pr2_impl_post_merge_closure"
EFFECT = "bounded_implementation_handoff_post_merge_lifecycle_reconciliation_only"

HANDOFF_IDS = ['PR2-TEST-HANDOFF-TOPOLOGY-001', 'PR2-TEST-HANDOFF-PERSIST-001', 'PR2-TEST-HANDOFF-FIDELITY-001', 'PR2-TEST-HANDOFF-BP-001', 'PR2-TEST-HANDOFF-FAILURE-001']


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


def test_activation_merge_is_reconciled_without_completion():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    assert data["artifact_version"] == "0.4.64"

    assert impl["status"] == "active"

    assert (
        impl["completion_state"]
        == "active_bounded_implementation_handoff_definition"
    )

    assert impl["pull_request"] == PR
    assert impl["branch_head"] == HEAD
    assert impl["merge_commit"] == MERGE

    assert (
        impl["post_merge_closure_authorization_reference"]
        == AUTH
    )

    assert (
        impl["post_merge_closure_authority_effect"]
        == EFFECT
    )

    assert (
        impl["post_merge_closure_recorded_from"]
        == MERGE
    )

    assert impl["post_merge_closure_tree"] == TREE
    assert impl["post_merge_closure_ci_run"] == CI_RUN
    assert impl["post_merge_closure_ci_run_id"] == CI_RUN_ID

    assert (
        f"PR2-IMPL GitHub Actions CI #{CI_RUN}:success"
        in impl["validation_evidence"]
    )


def test_pr2_impl_remains_only_active_post_r2_workstream():
    data = load(MAN)

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == {"PR2-IMPL"}


def test_five_handoffs_remain_preserved():
    impl = rows(load(MAN))["PR2-IMPL"]

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


def test_closure_preserves_downstream_authority_boundaries():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

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

    candidate = impl["first_playable_candidate"]

    assert candidate["package"] == "R4-B"
    assert candidate["ready_pending_authorization"] is False
    assert candidate["authorized"] is False

    r4 = data["r4_native_substrate_design_target"]

    assert r4["r4_b_ready_pending_authorization"] is False
    assert r4["r4_b_authorized"] is False
    assert r4["implementation_authorized"] is False
    assert r4["runtime_promotion_clear"] is False


def test_activation_contract_is_unchanged_by_closure():
    assert (
        CONTRACT.read_text(
            encoding="utf-8",
        )
        == read_at(
            MERGE,
            CONTRACT,
        )
    )


def test_activation_regression_is_frozen_at_accepted_merge():
    text = ACTIVATION_TEST.read_text(
        encoding="utf-8",
    )

    assert (
        f'ACCEPTED_MERGE = "{MERGE}"'
        in text
    )

    assert "def read_at(" in text
    assert "read_at(" in text
    assert "ACCEPTED_MERGE" in text


def test_program_and_decision_record_bounded_closure():
    program = PROG.read_text(
        encoding="utf-8",
    )

    decisions = DEC.read_text(
        encoding="utf-8",
    )

    assert "**Artifact version:** `0.4.64`" in program

    assert (
        "### 5.60 PR2-IMPL activation "
        "post-merge closure recording"
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
        "PR2-IMPL remains `active`.",
        "active_bounded_implementation_handoff_definition",
        "R4-B remains not ready pending authorization",
        "PR2-IMPL must still satisfy its bounded completion condition",
    ):
        assert token in program

    assert (
        "PR2-IMPL-ACTIVATION-POST-MERGE-CLOSURE-001"
        in decisions
    )

    for token in (
        "**PR2-IMPL state:** `active`",
        (
            "**PR2-IMPL completion state:** "
            "`active_bounded_implementation_handoff_definition`"
        ),
        "**Future implementation handoffs preserved:** `5`",
        "**R4-B ready pending authorization:** `false`",
        "**R4-B authorized:** `false`",
        "**Runtime implementation authorized:** `false`",
        "**Production schema authorized:** `false`",
        "**R4 activation authorized:** `false`",
        "**Runtime promotion authorized:** `false`",
    ):
        assert token in decisions


def test_closure_does_not_redefine_handoff_authority():
    flat = " ".join(
        CONTRACT.read_text(
            encoding="utf-8",
        ).split()
    )

    for token in (
        "PR2-IMPL does not itself implement runtime mechanics.",
        "R4-B remains unauthorized.",
        (
            "No carried handoff becomes a prerequisite "
            "merely because it exists."
        ),
        "model-generated identity authority",
        "model-generated relation authority",
        "no universal world-state manager",
    ):
        assert token in flat



def test_closure_validation_evidence_is_exact():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    required = {
        (
            "PR2-IMPL post-merge closure "
            "focused pre-certification:43 passed"
        ),
        (
            "PR2-IMPL post-merge closure "
            "broader PR2 regression:397 passed"
        ),
        (
            "PR2-IMPL post-merge closure full local repository suite:"
            "9328 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        (
            "PR2-IMPL post-merge closure "
            "focused post-suite regression:43 passed"
        ),
        (
            "PR2-IMPL post-merge closure "
            "git diff --check:clean"
        ),
        (
            "PR2-IMPL post-merge closure "
            "exact six-file footprint:PASS"
        ),
        (
            "PR2-IMPL post-merge closure "
            "runtime/schema noninterference:PASS"
        ),
    }

    assert required.issubset(
        set(impl["validation_evidence"])
    )

    certification = impl["post_merge_closure_validation"]

    assert certification["focused_pre_certification"] == {
        "passed": 43,
        "result": "pass",
    }

    assert certification["broader_pr2_regression"] == {
        "passed": 397,
        "result": "pass",
    }

    assert certification["full_repository_suite"] == {
        "passed": 9328,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "result": "pass",
    }

    assert certification["focused_post_suite_regression"] == {
        "passed": 43,
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
        "#### PR2-IMPL activation post-merge "
        "closure validation evidence"
        in program
    )

    assert (
        "PR2-IMPL-ACTIVATION-POST-MERGE-"
        "CLOSURE-VALIDATION-002"
        in decisions
    )

    for token in (
        "397 passed",
        "9328 passed, 10 skipped, 2 xfailed, 1 warning",
        "**Changed paths:** `6`",
        "**PR2-IMPL status:** `active`",
        "**R4-B authorized:** `false`",
        "**Runtime implementation authorized:** `false`",
        "**Production schema authorized:** `false`",
        "**Runtime promotion authorized:** `false`",
    ):
        assert token in decisions
