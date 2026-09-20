# Executable validation for PR2-IMPL completion assessment.
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

PACKAGE = (
    ROOT
    / "docs/doctrine/reviews/"
    "r4_b_persistent_world_entity_location_implementation_package.yaml"
)

ASSESSMENT = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_impl_completion_assessment.yaml"
)

CLOSURE_TEST = (
    ROOT
    / "tests/"
    "test_pr2_impl_post_merge_closure.py"
)

BASE = "058beb0577ee5942ab9fb9c526d675b689b3e829"
ACCEPTED_MERGE = "98b8bcec284f4a233af76ae7cb2ba88614df8b97"

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


def test_completion_assessment_satisfies_all_seven_requirements():
    review = load(ASSESSMENT)

    assert review["status"] == "validated_complete"

    assert (
        review["review_result"]
        == "complete_r4_b_package_defined_pending_post_merge_closure"
    )

    requirements = review["completion_requirement_assessment"]

    assert len(requirements) == 7
    assert all(
        row["satisfied"] is True
        for row in requirements
    )

    summary = review["summary"]

    assert summary["completion_requirement_count"] == 7
    assert summary["satisfied_requirement_count"] == 7
    assert summary["blocking_finding_count"] == 0
    assert summary["completion_condition_satisfied"] is True
    assert summary["pr2_impl_completion_recommended"] is True


def test_manifest_records_validated_nonterminal_completion_state():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    assert data["artifact_version"] == "0.4.65"

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == set()

    assert impl["status"] == "validated"

    assert (
        impl["completion_state"]
        == (
            "validated_complete_r4_b_package_defined_"
            "pending_post_merge_closure"
        )
    )

    assert impl["completion_condition_satisfied"] is True
    assert impl["completion_recommended"] is True
    assert impl["r4_b_package_definition_complete"] is True


def test_r4_b_is_defined_but_still_closed():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]

    candidate = impl["first_playable_candidate"]

    assert candidate["package"] == "R4-B"
    assert candidate["package_definition_complete"] is True

    assert (
        candidate["ready_pending_authorization"]
        is False
    )

    assert (
        candidate[
            "ready_after_completion_post_merge_closure"
        ]
        is True
    )

    assert candidate["authorized"] is False

    assert impl["r4_b_authorized"] is False
    assert impl["runtime_implementation_authorized"] is False
    assert impl["production_schema_authorized"] is False
    assert impl["r4_activation_authorized"] is False
    assert impl["runtime_promotion_authorized"] is False

    target = data["r4_native_substrate_design_target"]

    assert target["r4_b_package_defined"] is True

    assert (
        target[
            "r4_b_ready_after_pr2_impl_post_merge_closure"
        ]
        is True
    )

    assert target["r4_b_ready_pending_authorization"] is False
    assert target["r4_b_authorized"] is False
    assert target["implementation_authorized"] is False
    assert target["runtime_promotion_clear"] is False


def test_all_five_future_handoffs_remain_preserved_and_nonblocking():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]
    package = load(PACKAGE)

    assert (
        impl["carried_future_implementation_handoffs"]
        == HANDOFF_IDS
    )

    assert impl["carried_handoff_blocker_count_for_r4_b"] == 0

    dependency_rows = package["dependencies"][
        "carried_handoff_dependency_assessment"
    ]

    assert [
        row["handoff_id"]
        for row in dependency_rows
    ] == HANDOFF_IDS

    assert all(
        row["blocks_r4_b"] is False
        for row in dependency_rows
    )


def test_completion_assessment_implements_no_runtime_or_schema_code():
    review = load(ASSESSMENT)
    method = review["method"]

    assert method["runtime_implementation_created"] is False
    assert method["production_schema_created"] is False
    assert method["r4_b_implementation_authorized"] is False
    assert method["r4_activation_authorized"] is False
    assert method["runtime_promotion_authorized"] is False

    package = load(PACKAGE)

    assert package["implementation_authorized"] is False
    assert package["edit_allowlist"]["production_schema_paths"] == []


def test_previous_post_merge_closure_is_snapshot_frozen():
    text = CLOSURE_TEST.read_text(
        encoding="utf-8",
    )

    assert (
        f'ACCEPTED_MERGE = "{BASE}"'
        in text
    )

    assert "read_at(" in text
    assert "ACCEPTED_MERGE" in text


def test_program_and_decision_record_completion_assessment():
    program = read_at(
        ACCEPTED_MERGE,
        PROG,
    )

    decisions = read_at(
        ACCEPTED_MERGE,
        DEC,
    )

    normalized_program = " ".join(
        program.split()
    )

    assert "**Artifact version:** `0.4.65`" in program

    assert (
        "### 5.61 PR2-IMPL R4-B package definition "
        "and completion assessment"
        in program
    )

    for token in (
        "all seven PR2-IMPL completion requirements satisfied",
        "None is a concrete blocker for this representation-only slice.",
        "PR2-IMPL candidate state is now `validated`",
        "R4-B remains unauthorized.",
    ):
        assert token in normalized_program

    assert (
        "PR2-IMPL-COMPLETION-ASSESSMENT-001"
        in decisions
    )

    for token in (
        "**PR2-IMPL completion requirements assessed:** `7`",
        "**PR2-IMPL completion requirements satisfied:** `7`",
        "**Blocking findings:** `0`",
        "**Carried PR2-TEST handoffs preserved:** `5`",
        "**Carried handoffs blocking R4-B:** `0`",
        "**PR2-IMPL status:** `validated`",
        "**PR2-IMPL completion condition satisfied:** `true`",
        "**R4-B ready pending authorization:** `false`",
        "**R4-B authorized:** `false`",
        "**Runtime implementation authorized:** `false`",
        "**Production schema authorized:** `false`",
    ):
        assert token in decisions



def test_completion_assessment_validation_evidence_is_exact():
    data = load(MAN)
    impl = rows(data)["PR2-IMPL"]
    review = load(ASSESSMENT)

    required = {
        'PR2-IMPL completion assessment focused pre-certification:54 passed',
        'PR2-IMPL completion assessment broader PR2 regression:405 passed',
        'PR2-IMPL completion assessment full local repository suite:9343 passed, 10 skipped, 2 xfailed, 1 warning',
        'PR2-IMPL completion assessment focused post-suite regression:54 passed',
        'PR2-IMPL completion assessment git diff --check:clean',
        'PR2-IMPL completion assessment exact nine-file footprint:PASS',
        'PR2-IMPL completion assessment runtime/schema noninterference:PASS',
    }

    assert required.issubset(
        set(impl["validation_evidence"])
    )

    assert set(review["evidence"]) == required

    expected = {'focused_pre_certification': {'passed': 54, 'result': 'pass'}, 'broader_pr2_regression': {'passed': 405, 'result': 'pass'}, 'full_repository_suite': {'passed': 9343, 'skipped': 10, 'xfailed': 2, 'warnings': 1, 'result': 'pass'}, 'focused_post_suite_regression': {'passed': 54, 'result': 'pass'}, 'git_diff_check': 'clean', 'changed_path_count': 9, 'runtime_implementation_path_count': 0, 'production_schema_path_count': 0}

    assert (
        impl["completion_assessment_validation"]
        == expected
    )

    assert review["certification"] == expected

    program = read_at(
        ACCEPTED_MERGE,
        PROG,
    )

    decisions = read_at(
        ACCEPTED_MERGE,
        DEC,
    )

    assert (
        "#### PR2-IMPL completion assessment "
        "validation evidence"
        in program
    )

    assert (
        "PR2-IMPL-COMPLETION-ASSESSMENT-"
        "VALIDATION-002"
        in decisions
    )

    for token in (
        '54 passed',
        '405 passed',
        '9343 passed, 10 skipped, 2 xfailed, 1 warning',
        '54 passed',
        "**Changed paths:** `9`",
        "**PR2-IMPL status:** `validated`",
        "**R4-B ready pending authorization:** `false`",
        "**R4-B authorized:** `false`",
        "**Runtime implementation authorized:** `false`",
        "**Production schema authorized:** `false`",
        "**Runtime promotion authorized:** `false`",
    ):
        assert token in decisions
