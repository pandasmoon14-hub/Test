# Executable validation for PR2-IMPL terminal completion closure.
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

ASSESSMENT = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_impl_completion_assessment.yaml"
)

PACKAGE = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_b_persistent_world_entity_location_implementation_package.yaml"
)

ASSESSMENT_TEST = (
    ROOT
    / "tests/"
    "test_pr2_impl_completion_assessment.py"
)

PR = 427
HEAD = "6ba3c28b2b7805958e2d01018ff4828f7307be56"
MERGE = "98b8bcec284f4a233af76ae7cb2ba88614df8b97"
TREE = "d1953e09d1d0bfa55659e98934bcff8b84946307"
ACCEPTED_MERGE = "a7d7f912254abeab5716d23d3dc2f7fc5d6c4e59"

CI_RUN = 254
CI_RUN_ID = 35487544104

AUTH = "owner_directive_2026-09-19_pr2_impl_completion_post_merge_closure"
EFFECT = "bounded_implementation_handoff_completion_post_merge_lifecycle_reconciliation_only"

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
        read_at(
            ACCEPTED_MERGE,
            path,
        )
    )


def rows(data):
    return {
        row["workstream_id"]: row
        for row in data["workstreams"]
    }


def test_pr2_impl_is_terminal_and_merge_metadata_is_exact():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    assert data["artifact_version"] == "0.4.66"

    assert impl["status"] == "merged"

    assert (
        impl["completion_state"]
        == "merged_complete_r4_b_ready_pending_authorization"
    )

    assert impl["pull_request"] == PR
    assert impl["branch_head"] == HEAD
    assert impl["merge_commit"] == MERGE

    assert impl["completion_assessment_pull_request"] == PR
    assert impl["completion_assessment_branch_head"] == HEAD
    assert impl["completion_assessment_merge_commit"] == MERGE
    assert impl["completion_assessment_merge_tree"] == TREE


def test_completion_closure_metadata_is_exact():
    impl = rows(load(MAN))["PR2-IMPL"]

    assert (
        impl["completion_post_merge_closure_authorization_reference"]
        == AUTH
    )

    assert (
        impl["completion_post_merge_closure_authority_effect"]
        == EFFECT
    )

    assert (
        impl["completion_post_merge_closure_recorded_from"]
        == MERGE
    )

    assert impl["completion_post_merge_closure_tree"] == TREE
    assert impl["completion_post_merge_closure_ci_run"] == CI_RUN
    assert impl["completion_post_merge_closure_ci_run_id"] == CI_RUN_ID

    assert (
        f"PR2-IMPL completion assessment "
        f"GitHub Actions CI #{CI_RUN}:success"
        in impl["validation_evidence"]
    )


def test_five_future_implementation_handoffs_remain_preserved():
    impl = rows(load(MAN))["PR2-IMPL"]

    assert (
        impl["carried_future_implementation_handoffs"]
        == HANDOFF_IDS
    )

    assert impl["carried_handoff_blocker_count_for_r4_b"] == 0

    assert (
        impl["package_rules"][
            "all_carried_handoffs_are_automatic_prerequisites"
        ]
        is False
    )


def test_r4_b_is_ready_but_not_authorized():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    candidate = impl["first_playable_candidate"]

    assert candidate["package"] == "R4-B"
    assert candidate["package_definition_complete"] is True
    assert candidate["ready_pending_authorization"] is True
    assert candidate["ready_after_completion_post_merge_closure"] is True
    assert candidate["readiness_recorded_from"] == MERGE
    assert candidate["authorized"] is False

    target = data["r4_native_substrate_design_target"]

    assert target["r4_b_package_defined"] is True
    assert target["r4_b_ready_pending_authorization"] is True
    assert target["r4_b_readiness_source"] == "PR2-IMPL"
    assert target["r4_b_readiness_recorded_from"] == MERGE
    assert target["r4_b_authorized"] is False


def test_runtime_r4_and_promotion_authority_remain_closed():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]
    target = data["r4_native_substrate_design_target"]

    assert impl["runtime_implementation_authorized"] is False
    assert impl["production_schema_authorized"] is False
    assert impl["content_implementation_authorized"] is False
    assert impl["live_play_authorized"] is False
    assert impl["canon_promotion_authorized"] is False
    assert impl["r4_b_authorized"] is False
    assert impl["r4_activation_authorized"] is False
    assert impl["runtime_promotion_authorized"] is False

    assert target["runtime_edits_authorized"] is False
    assert target["schema_edits_authorized"] is False
    assert target["implementation_authorized"] is False
    assert target["r4_activation_authorized"] is False
    assert target["runtime_promotion_clear"] is False

    assert data["r2_gate_state"]["R4-R6"] == "blocked"


def test_assessment_and_package_are_unchanged_by_closure():
    accepted_assessment = read_at(
        ACCEPTED_MERGE,
        ASSESSMENT,
    )

    accepted_package = read_at(
        ACCEPTED_MERGE,
        PACKAGE,
    )

    assert accepted_assessment == read_at(
        MERGE,
        ASSESSMENT,
    )

    assert accepted_package == read_at(
        MERGE,
        PACKAGE,
    )


def test_completion_assessment_regression_is_snapshot_frozen():
    text = ASSESSMENT_TEST.read_text(
        encoding="utf-8",
    )

    assert (
        f'ACCEPTED_MERGE = "{MERGE}"'
        in text
    )

    assert "import subprocess" in text
    assert "def read_at(" in text

    assert (
        "read_at(\n"
        "            ACCEPTED_MERGE,"
        in text
    )


def test_program_and_decision_record_terminal_closure():
    program = read_at(
        ACCEPTED_MERGE,
        PROG,
    )

    decisions = read_at(
        ACCEPTED_MERGE,
        DEC,
    )

    assert "**Artifact version:** `0.4.66`" in program

    assert (
        "### 5.62 PR2-IMPL completion "
        "post-merge closure"
        in program
    )

    normalized = " ".join(
        program.split()
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
        "PR2-IMPL is now terminal with status:",
        "merged_complete_r4_b_ready_pending_authorization",
        "R4-B now becomes `ready_pending_authorization`.",
        "R4-B remains unauthorized.",
        "Runtime promotion remains uncleared.",
    ):
        assert token in normalized

    assert (
        "PR2-IMPL-COMPLETION-POST-MERGE-CLOSURE-001"
        in decisions
    )

    for token in (
        "**PR2-IMPL status:** `merged`",
        (
            "**PR2-IMPL completion state:** "
            "`merged_complete_r4_b_ready_pending_authorization`"
        ),
        "**Future implementation handoffs preserved:** `5`",
        "**Carried handoffs blocking R4-B:** `0`",
        "**R4-B ready pending authorization:** `true`",
        "**R4-B authorized:** `false`",
        "**Runtime implementation authorized:** `false`",
        "**Production schema authorized:** `false`",
        "**R4 activation authorized:** `false`",
        "**Runtime promotion authorized:** `false`",
    ):
        assert token in decisions



def test_terminal_closure_validation_evidence_is_exact():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    required = {
        'PR2-IMPL terminal completion closure focused pre-certification:63 passed',
        'PR2-IMPL terminal completion closure broader PR2 regression:414 passed',
        'PR2-IMPL terminal completion closure full local repository suite:9352 passed, 10 skipped, 2 xfailed, 1 warning',
        'PR2-IMPL terminal completion closure focused post-suite regression:63 passed',
        'PR2-IMPL terminal completion closure git diff --check:clean',
        'PR2-IMPL terminal completion closure exact six-file footprint:PASS',
        'PR2-IMPL terminal completion closure runtime/schema noninterference:PASS',
    }

    assert required.issubset(
        set(impl["validation_evidence"])
    )

    expected = {'focused_pre_certification': {'passed': 63, 'result': 'pass'}, 'broader_pr2_regression': {'passed': 414, 'result': 'pass'}, 'full_repository_suite': {'passed': 9352, 'skipped': 10, 'xfailed': 2, 'warnings': 1, 'result': 'pass', 'warning_class': 'PytestRemovedIn10Warning', 'warning_disposition': 'existing_nonblocking_deprecation'}, 'focused_post_suite_regression': {'passed': 63, 'result': 'pass'}, 'git_diff_check': 'clean', 'changed_path_count': 6, 'runtime_implementation_path_count': 0, 'production_schema_path_count': 0}

    assert (
        impl["completion_post_merge_closure_validation"]
        == expected
    )

    program = read_at(
        ACCEPTED_MERGE,
        PROG,
    )

    decisions = read_at(
        ACCEPTED_MERGE,
        DEC,
    )

    assert (
        "#### PR2-IMPL terminal completion "
        "post-merge closure validation evidence"
        in program
    )

    assert (
        "PR2-IMPL-COMPLETION-POST-MERGE-"
        "CLOSURE-VALIDATION-002"
        in decisions
    )

    for token in (
        '63 passed',
        '414 passed',
        '9352 passed, 10 skipped, 2 xfailed, 1 warning',
        '63 passed',
        "**Changed paths:** `6`",
        "**PR2-IMPL status:** `merged`",
        (
            "**PR2-IMPL completion state:** "
            "`merged_complete_r4_b_ready_pending_authorization`"
        ),
        "**R4-B ready pending authorization:** `true`",
        "**R4-B authorized:** `false`",
        "**Runtime implementation authorized:** `false`",
        "**Production schema authorized:** `false`",
        "**R4 activation authorized:** `false`",
        "**Runtime promotion authorized:** `false`",
    ):
        assert token in decisions
