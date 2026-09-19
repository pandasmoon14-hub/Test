# Executable validation for PR2-TEST seven-family completion assessment.
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAN = ROOT / "docs/doctrine/control/post_r2a_transition_manifest.yaml"
PROG = ROOT / "docs/doctrine/control/post_r2a_transition_program.md"
DEC = ROOT / "docs/decisions/current_decisions_log.md"

REVIEW = (
    ROOT
    / "docs/doctrine/reviews/"
    "pr2_test_seven_family_completion_assessment.yaml"
)

CLOSURE_TEST = (
    ROOT
    / "tests/test_pr2_test_post_merge_closure.py"
)

BASE = "da5bc37dc61a31fb199ab9b62332a7063d4b7d04"
ACCEPTED_MERGE = "54cb6c459585011dfbee11ad0510c24cb2d0fe3f"


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


def test_all_seven_families_are_assessed():
    review = load(REVIEW)

    assert review["status"] == "validated_complete"
    assert (
        review["review_result"]
        == "complete_with_future_implementation_handoffs"
    )

    families = {
        row["family"]: row
        for row in review["family_assessments"]
    }

    assert set(families) == {
        "source_governance",
        "originality_and_information_barrier",
        "deterministic_topology_equivalence",
        "persistence_replay_and_recovery",
        "fidelity_aggregation_and_reconstitution",
        "overload_backpressure_and_lawful_degradation",
        "failure_isolation_and_authority_ambiguity",
    }

    expected = {
        "source_governance": (55, 0),
        "originality_and_information_barrier": (37, 0),
        "deterministic_topology_equivalence": (22, 0),
        "persistence_replay_and_recovery": (169, 1),
        "fidelity_aggregation_and_reconstitution": (14, 0),
        "overload_backpressure_and_lawful_degradation": (15, 0),
        "failure_isolation_and_authority_ambiguity": (76, 1),
    }

    for family, result in expected.items():
        assert (
            families[family]["passed"],
            families[family]["skipped"],
        ) == result

        assert families[family]["pr2_test_blocking"] is False


def test_future_implementation_handoffs_are_bounded():
    review = load(REVIEW)
    handoffs = review["future_implementation_handoffs"]

    assert len(handoffs) == 5

    assert {
        row["handoff_id"]
        for row in handoffs
    } == {
        "PR2-TEST-HANDOFF-TOPOLOGY-001",
        "PR2-TEST-HANDOFF-PERSIST-001",
        "PR2-TEST-HANDOFF-FIDELITY-001",
        "PR2-TEST-HANDOFF-BP-001",
        "PR2-TEST-HANDOFF-FAILURE-001",
    }

    assert all(
        row["route"] == "PR2-IMPL"
        for row in handoffs
    )

    assert all(
        row["pr2_test_blocking"] is False
        for row in handoffs
    )


def test_completion_is_satisfied_without_inventing_implementation():
    review = load(REVIEW)
    summary = review["summary"]
    method = review["method"]

    assert summary["evaluation_family_count"] == 7
    assert summary["passing_family_count"] == 7
    assert summary["family_failure_count"] == 0
    assert summary["evaluation_owned_repair_count"] == 0
    assert summary["pr2_test_blocking_finding_count"] == 0
    assert summary["future_implementation_handoff_count"] == 5
    assert summary["completion_condition_satisfied"] is True
    assert summary["pr2_test_completion_recommended"] is True

    assert method["repository_mutation_during_sweep"] is False
    assert method["new_runtime_implementation_created"] is False
    assert method["new_production_schema_created"] is False
    assert method["missing_mechanics_implemented"] is False


def test_manifest_records_validated_nonterminal_state():
    data = load(MAN)
    by = rows(data)

    test = by["PR2-TEST"]

    assert data["artifact_version"] == "0.4.61"

    assert {
        row["workstream_id"]
        for row in data["workstreams"]
        if row["status"] == "active"
    } == set()

    assert test["status"] == "validated"

    assert (
        test["completion_state"]
        == "validated_complete_with_future_implementation_handoffs"
    )

    assert test["completion_condition_satisfied"] is True
    assert test["completion_recommended"] is True
    assert test["future_implementation_handoff_count"] == 5


def test_downstream_authority_remains_closed():
    data = load(MAN)
    by = rows(data)

    test = by["PR2-TEST"]
    impl = by["PR2-IMPL"]

    assert impl["status"] == "blocked"
    assert impl["authorization_reference"] is None

    assert test["runtime_implementation_authorized"] is False
    assert test["production_schema_authorized"] is False
    assert test["pr2_impl_authorized"] is False
    assert test["r4_b_authorized"] is False
    assert test["runtime_promotion_authorized"] is False

    r4 = data["r4_native_substrate_design_target"]

    assert r4["r4_b_ready_pending_authorization"] is False
    assert r4["r4_b_authorized"] is False
    assert r4["implementation_authorized"] is False
    assert r4["runtime_promotion_clear"] is False


def test_previous_closure_is_snapshot_frozen():
    text = read_at(
        ACCEPTED_MERGE,
        CLOSURE_TEST,
    )

    assert (
        f'ACCEPTED_MERGE = "{BASE}"'
        in text
    )

    assert "load_at(" in text
    assert "ACCEPTED_MERGE" in text


def test_program_and_decision_record_assessment():
    program = read_at(
        ACCEPTED_MERGE,
        PROG,
    )
    decisions = read_at(
        ACCEPTED_MERGE,
        DEC,
    )

    assert "**Artifact version:** `0.4.61`" in program

    assert (
        "### 5.57 PR2-TEST seven-family executable "
        "completion assessment"
        in program
    )

    for token in (
        "55 passed",
        "37 passed",
        "22 passed",
        "169 passed, 1 skipped",
        "14 passed",
        "15 passed",
        "76 passed, 1 skipped",
        "Five future-implementation handoffs",
        "zero PR2-TEST-owned",
        "PR2-IMPL remains `blocked` and unauthorized.",
        "R4-B remains unauthorized.",
    ):
        assert token in program

    assert (
        "PR2-TEST-SEVEN-FAMILY-"
        "COMPLETION-ASSESSMENT-001"
        in decisions
    )

    for token in (
        "**Evaluation families assessed:** `7`",
        "**Passing families:** `7`",
        "**PR2-TEST blocking findings:** `0`",
        "**Evaluation-owned repairs required:** `0`",
        "**Future implementation handoffs:** `5`",
        "**Completion condition satisfied:** `true`",
        "**PR2-TEST status:** `validated`",
        "**PR2-IMPL authorized:** `false`",
        "**R4-B authorized:** `false`",
    ):
        assert token in decisions

def test_recorded_certification_evidence_is_exact():
    data = load(MAN)
    test = rows(data)["PR2-TEST"]
    review = load(REVIEW)

    required = {
        "PR2-TEST completion assessment focused constructor regression:153 passed",
        "PR2-TEST completion assessment broader PR2 regression:369 passed",
        (
            "PR2-TEST completion assessment full local repository suite:"
            "9300 passed, 10 skipped, 2 xfailed, 1 warning"
        ),
        "PR2-TEST completion assessment focused post-suite regression:153 passed",
        "PR2-TEST completion assessment git diff --check:clean",
        "PR2-TEST completion assessment exact seven-file footprint:PASS",
        "PR2-TEST completion assessment runtime/schema noninterference:PASS",
    }

    assert required.issubset(
        set(test["validation_evidence"])
    )

    assert required.issubset(
        set(review["evidence"])
    )

    certification = review["certification"]

    assert certification["focused_constructor_regression"] == {
        "passed": 153,
        "result": "pass",
    }

    assert certification["broader_pr2_regression"] == {
        "passed": 369,
        "result": "pass",
    }

    assert certification["full_repository_suite"] == {
        "passed": 9300,
        "skipped": 10,
        "xfailed": 2,
        "warnings": 1,
        "result": "pass",
        "warning_class": "PytestRemovedIn10Warning",
        "warning_disposition": "existing_nonblocking_deprecation",
    }

    assert certification["focused_post_suite_regression"] == {
        "passed": 153,
        "result": "pass",
    }

    assert certification["git_diff_check"] == "clean"
    assert certification["changed_path_count"] == 7
    assert certification["runtime_implementation_path_count"] == 0
    assert certification["production_schema_path_count"] == 0

    program = read_at(
        ACCEPTED_MERGE,
        PROG,
    )
    decisions = read_at(
        ACCEPTED_MERGE,
        DEC,
    )

    assert (
        "#### PR2-TEST seven-family completion "
        "assessment validation evidence"
        in program
    )

    assert (
        "PR2-TEST-SEVEN-FAMILY-COMPLETION-"
        "ASSESSMENT-VALIDATION-002"
        in decisions
    )
