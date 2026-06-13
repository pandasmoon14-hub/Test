"""Tests for PR-7 Slice 3 — Expected Boundary Assertion Layer."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    MODEL_BOUNDARY_STATUS_VALUES,
    MODEL_BOUNDARY_VIOLATION_CODES,
    ModelBoundaryAssertionError,
    ModelBoundaryCaseAssertionResult,
    ModelBoundaryEvaluationError,
    ModelBoundaryEvaluationResult,
    ModelBoundaryEvaluationSuite,
    ModelBoundaryEvaluationSuiteResult,
    ModelBoundaryExpectedCaseOutcome,
    ModelBoundaryExpectedSuiteOutcome,
    ModelBoundarySuiteAssertionResult,
    assert_model_boundary_case_result,
    assert_model_boundary_suite_result,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_evaluation_case,
    create_model_boundary_evaluation_suite,
    create_model_boundary_expected_case_outcome,
    create_model_boundary_expected_suite_outcome,
    evaluate_model_boundary_case,
    evaluate_model_boundary_suite,
)
from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
)


def _make_packet_result(warnings: tuple[str, ...] = ()) -> ContextPacketCompilerResult:
    """Build a valid ContextPacketCompilerResult through the PR-6 route."""
    request = create_context_packet_assembly_request(
        request_ref="req-1",
        packet_kind="single_event_narration",
        packet_payload={
            "event_ref": "evt-1",
            "event_kind": "move",
            "visible_fact_refs": ["fact-1"],
        },
        assembly_timestamp="2026-06-13T12:00:00Z",
    )
    result = compile_context_packet_from_request(request)
    if warnings:
        return ContextPacketCompilerResult(
            request_ref=result.request_ref,
            packet_kind=result.packet_kind,
            serialized_packet=dict(result.serialized_packet),
            audit_report=result.audit_report,
            assembly_succeeded=result.assembly_succeeded,
            serialization_succeeded=result.serialization_succeeded,
            audit_succeeded=result.audit_succeeded,
            hidden_information_excluded=result.hidden_information_excluded,
            non_authority_seal_present=result.non_authority_seal_present,
            warnings=warnings,
        )
    return result


def _make_case(
    case_ref: str,
    candidate_output: dict[str, Any],
    expected_output_family: str = "narration_display",
    warnings: tuple[str, ...] = (),
) -> ModelBoundaryEvaluationCase:
    """Build a valid ModelBoundaryEvaluationCase around a candidate output."""
    return create_model_boundary_evaluation_case(
        case_ref=case_ref,
        candidate_model_ref="model-1",
        expected_output_family=expected_output_family,
        packet_result=_make_packet_result(warnings=warnings),
        candidate_output=candidate_output,
    )


def _make_actual_case_result(
    candidate_output: dict[str, Any],
    warnings: tuple[str, ...] = (),
) -> ModelBoundaryEvaluationResult:
    """Build an actual ModelBoundaryEvaluationResult through the PR-7 route."""
    case = _make_case("case-1", candidate_output, warnings=warnings)
    return evaluate_model_boundary_case(case)


def _make_actual_suite_result(
    cases: list[ModelBoundaryEvaluationCase],
) -> ModelBoundaryEvaluationSuiteResult:
    """Build an actual ModelBoundaryEvaluationSuiteResult through the PR-7 route."""
    suite = create_model_boundary_evaluation_suite(
        suite_ref="suite-1",
        suite_label="Test Suite",
        cases=cases,
    )
    return evaluate_model_boundary_suite(suite)


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------

def test_package_exports() -> None:
    """All PR-7 Slice 3 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        ModelBoundaryAssertionError,
        ModelBoundaryCaseAssertionResult,
        ModelBoundaryExpectedCaseOutcome,
        ModelBoundaryExpectedSuiteOutcome,
        ModelBoundarySuiteAssertionResult,
        assert_model_boundary_case_result,
        assert_model_boundary_suite_result,
        create_model_boundary_expected_case_outcome,
        create_model_boundary_expected_suite_outcome,
    )

    assert issubclass(ModelBoundaryAssertionError, ModelBoundaryEvaluationError)
    assert ModelBoundaryExpectedCaseOutcome is not None
    assert ModelBoundaryCaseAssertionResult is not None
    assert ModelBoundaryExpectedSuiteOutcome is not None
    assert ModelBoundarySuiteAssertionResult is not None
    assert callable(create_model_boundary_expected_case_outcome)
    assert callable(assert_model_boundary_case_result)
    assert callable(create_model_boundary_expected_suite_outcome)
    assert callable(assert_model_boundary_suite_result)


# ---------------------------------------------------------------------------
# ModelBoundaryAssertionError
# ---------------------------------------------------------------------------

def test_assertion_error_subclasses_model_boundary_evaluation_error() -> None:
    """ModelBoundaryAssertionError subclasses ModelBoundaryEvaluationError."""
    assert issubclass(ModelBoundaryAssertionError, ModelBoundaryEvaluationError)
    assert issubclass(ModelBoundaryAssertionError, ValueError)


# ---------------------------------------------------------------------------
# ModelBoundaryExpectedCaseOutcome
# ---------------------------------------------------------------------------

def test_expected_case_outcome_is_frozen() -> None:
    """ModelBoundaryExpectedCaseOutcome instances are immutable."""
    outcome = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-1",
        expected_status="passed",
        expected_passed=True,
    )
    with pytest.raises(FrozenInstanceError):
        outcome.expected_status = "failed"  # type: ignore[misc]


def test_expected_case_outcome_freezes_metadata() -> None:
    """Expected case outcome metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    outcome = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-1",
        expected_status="passed",
        expected_passed=True,
        metadata=mutable_meta,
    )

    assert isinstance(outcome.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(outcome.metadata["tags"]) == ["a", "b"]


def test_expected_case_outcome_normalizes_and_sorts_fields() -> None:
    """Violation codes, forbidden hits, and warning refs are normalized and sorted."""
    outcome = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-1",
        expected_status="failed",
        expected_passed=False,
        expected_violation_codes=[
            "forbidden_authority_field_present",
            "candidate_output_empty",
        ],
        expected_forbidden_field_hits=["state_delta", "apply_delta"],
        expected_packet_warning_refs=["warn-b", "warn-a"],
    )

    assert outcome.expected_violation_codes == (
        "candidate_output_empty",
        "forbidden_authority_field_present",
    )
    assert outcome.expected_forbidden_field_hits == ("apply_delta", "state_delta")
    assert outcome.expected_packet_warning_refs == ("warn-a", "warn-b")


def test_expected_case_outcome_rejects_unknown_expected_status() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_case_outcome(
            expectation_ref="exp-1",
            expected_status="unknown",
            expected_passed=True,
        )


def test_expected_case_outcome_rejects_non_bool_expected_passed() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_case_outcome(
            expectation_ref="exp-1",
            expected_status="passed",
            expected_passed="yes",  # type: ignore[arg-type]
        )


def test_expected_case_outcome_rejects_unknown_violation_code() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_case_outcome(
            expectation_ref="exp-1",
            expected_status="failed",
            expected_passed=False,
            expected_violation_codes=["not_a_real_code"],
        )


# ---------------------------------------------------------------------------
# ModelBoundaryCaseAssertionResult
# ---------------------------------------------------------------------------

def test_case_assertion_result_is_frozen() -> None:
    """ModelBoundaryCaseAssertionResult instances are immutable."""
    result = ModelBoundaryCaseAssertionResult(
        expectation_ref="exp-1",
        case_ref="case-1",
        assertion_passed=True,
        mismatch_codes=(),
        expected_status="passed",
        actual_status="passed",
        expected_passed=True,
        actual_passed=True,
        expected_violation_codes=(),
        actual_violation_codes=(),
        expected_forbidden_field_hits=(),
        actual_forbidden_field_hits=(),
        expected_packet_warning_refs=(),
        actual_packet_warning_refs=(),
    )
    with pytest.raises(FrozenInstanceError):
        result.assertion_passed = False  # type: ignore[misc]


def test_case_assertion_passes_when_actual_matches_expected() -> None:
    actual = _make_actual_case_result({"visible_text": "safe"})
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-pass",
        expected_status="passed",
        expected_passed=True,
    )

    result = assert_model_boundary_case_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is True
    assert result.mismatch_codes == ()
    assert result.case_ref == "case-1"
    assert result.expectation_ref == "exp-pass"


def test_case_assertion_reports_status_mismatch() -> None:
    actual = _make_actual_case_result({"visible_text": "safe"})
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-status",
        expected_status="failed",
        expected_passed=False,
    )

    result = assert_model_boundary_case_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "status_mismatch" in result.mismatch_codes


def test_case_assertion_reports_passed_flag_mismatch() -> None:
    actual = _make_actual_case_result({"visible_text": "safe"})
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-passed",
        expected_status="passed",
        expected_passed=False,
    )

    result = assert_model_boundary_case_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "passed_flag_mismatch" in result.mismatch_codes


def test_case_assertion_reports_violation_codes_mismatch() -> None:
    actual = _make_actual_case_result({"state_delta": {"hp": -5}})
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-violations",
        expected_status="failed",
        expected_passed=False,
        expected_violation_codes=["candidate_output_empty"],
    )

    result = assert_model_boundary_case_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "violation_codes_mismatch" in result.mismatch_codes


def test_case_assertion_reports_forbidden_field_hits_mismatch() -> None:
    actual = _make_actual_case_result({"state_delta": {"hp": -5}})
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-hits",
        expected_status="failed",
        expected_passed=False,
        expected_violation_codes=[
            "forbidden_authority_field_present",
            "state_mutation_claim_present",
        ],
        expected_forbidden_field_hits=["apply_delta"],
    )

    result = assert_model_boundary_case_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "forbidden_field_hits_mismatch" in result.mismatch_codes


def test_case_assertion_reports_packet_warning_refs_mismatch() -> None:
    actual = _make_actual_case_result(
        {"visible_text": "safe"},
        warnings=("warn-a",),
    )
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-warnings",
        expected_status="needs_review",
        expected_passed=False,
        expected_violation_codes=["packet_warning_present"],
        expected_packet_warning_refs=["warn-b"],
    )

    result = assert_model_boundary_case_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "packet_warning_refs_mismatch" in result.mismatch_codes


def test_case_assertion_rejects_invalid_expectation_object() -> None:
    actual = _make_actual_case_result({"visible_text": "safe"})
    with pytest.raises(ModelBoundaryAssertionError):
        assert_model_boundary_case_result(
            expectation="not-an-expectation",  # type: ignore[arg-type]
            actual_result=actual,
        )


def test_case_assertion_rejects_invalid_actual_result_object() -> None:
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-1",
        expected_status="passed",
        expected_passed=True,
    )
    with pytest.raises(ModelBoundaryAssertionError):
        assert_model_boundary_case_result(
            expectation=expectation,
            actual_result="not-a-result",  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# ModelBoundaryExpectedSuiteOutcome
# ---------------------------------------------------------------------------

def test_expected_suite_outcome_is_frozen() -> None:
    """ModelBoundaryExpectedSuiteOutcome instances are immutable."""
    outcome = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-1",
        expected_total_cases=1,
        expected_passed_cases=1,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
    )
    with pytest.raises(FrozenInstanceError):
        outcome.expected_all_passed = False  # type: ignore[misc]


def test_expected_suite_outcome_freezes_counts_and_metadata() -> None:
    """Status counts, violation counts, and metadata are frozen."""
    mutable_status_counts: dict[str, int] = {
        "passed": 1,
        "failed": 0,
        "needs_review": 0,
    }
    mutable_violation_counts: dict[str, int] = {"candidate_output_empty": 1}
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}

    outcome = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-1",
        expected_total_cases=1,
        expected_passed_cases=1,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts=mutable_status_counts,
        expected_violation_counts=mutable_violation_counts,
        metadata=mutable_meta,
    )

    assert isinstance(outcome.expected_status_counts, MappingProxyType)
    assert isinstance(outcome.expected_violation_counts, MappingProxyType)
    assert isinstance(outcome.metadata, MappingProxyType)

    mutable_status_counts["passed"] = 99
    mutable_violation_counts["candidate_output_empty"] = 99
    mutable_meta["tags"].append("c")

    assert outcome.expected_status_counts["passed"] == 1
    assert outcome.expected_violation_counts["candidate_output_empty"] == 1
    assert list(outcome.metadata["tags"]) == ["a", "b"]


def test_expected_suite_outcome_rejects_negative_counts() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_suite_outcome(
            expectation_ref="exp-suite-1",
            expected_total_cases=-1,
            expected_passed_cases=0,
            expected_failed_cases=0,
            expected_needs_review_cases=0,
            expected_all_passed=True,
            expected_status_counts={"passed": 0, "failed": 0, "needs_review": 0},
        )


def test_expected_suite_outcome_rejects_bool_counts() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_suite_outcome(
            expectation_ref="exp-suite-1",
            expected_total_cases=True,  # type: ignore[arg-type]
            expected_passed_cases=1,
            expected_failed_cases=0,
            expected_needs_review_cases=0,
            expected_all_passed=True,
            expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
        )


def test_expected_suite_outcome_rejects_count_sum_mismatch() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_suite_outcome(
            expectation_ref="exp-suite-1",
            expected_total_cases=2,
            expected_passed_cases=1,
            expected_failed_cases=1,
            expected_needs_review_cases=1,
            expected_all_passed=False,
            expected_status_counts={"passed": 1, "failed": 1, "needs_review": 1},
        )


def test_expected_suite_outcome_rejects_missing_status_count_key() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_suite_outcome(
            expectation_ref="exp-suite-1",
            expected_total_cases=1,
            expected_passed_cases=1,
            expected_failed_cases=0,
            expected_needs_review_cases=0,
            expected_all_passed=True,
            expected_status_counts={"passed": 1, "failed": 0},  # type: ignore[typeddict-item]
        )


def test_expected_suite_outcome_rejects_unknown_status_count_key() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_suite_outcome(
            expectation_ref="exp-suite-1",
            expected_total_cases=1,
            expected_passed_cases=1,
            expected_failed_cases=0,
            expected_needs_review_cases=0,
            expected_all_passed=True,
            expected_status_counts={
                "passed": 1,
                "failed": 0,
                "needs_review": 0,
                "unknown": 0,
            },
        )


def test_expected_suite_outcome_rejects_unknown_violation_count_key() -> None:
    with pytest.raises(ModelBoundaryAssertionError):
        create_model_boundary_expected_suite_outcome(
            expectation_ref="exp-suite-1",
            expected_total_cases=1,
            expected_passed_cases=1,
            expected_failed_cases=0,
            expected_needs_review_cases=0,
            expected_all_passed=True,
            expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
            expected_violation_counts={"not_a_code": 1},
        )


# ---------------------------------------------------------------------------
# ModelBoundarySuiteAssertionResult
# ---------------------------------------------------------------------------

def test_suite_assertion_result_is_frozen() -> None:
    """ModelBoundarySuiteAssertionResult instances are immutable."""
    result = ModelBoundarySuiteAssertionResult(
        expectation_ref="exp-1",
        suite_ref="suite-1",
        assertion_passed=True,
        mismatch_codes=(),
        expected_total_cases=1,
        actual_total_cases=1,
        expected_passed_cases=1,
        actual_passed_cases=1,
        expected_failed_cases=0,
        actual_failed_cases=0,
        expected_needs_review_cases=0,
        actual_needs_review_cases=0,
        expected_all_passed=True,
        actual_all_passed=True,
        expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
        actual_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
        expected_violation_counts={},
        actual_violation_counts={},
    )
    with pytest.raises(FrozenInstanceError):
        result.assertion_passed = False  # type: ignore[misc]


def test_suite_assertion_passes_when_actual_matches_expected() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"visible_text": "safe"}),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-pass",
        expected_total_cases=1,
        expected_passed_cases=1,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
        expected_violation_counts={},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is True
    assert result.mismatch_codes == ()
    assert result.suite_ref == "suite-1"
    assert result.expectation_ref == "exp-suite-pass"


def test_suite_assertion_reports_total_cases_mismatch() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"visible_text": "safe"}),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-total",
        expected_total_cases=2,
        expected_passed_cases=2,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 2, "failed": 0, "needs_review": 0},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "total_cases_mismatch" in result.mismatch_codes


def test_suite_assertion_reports_passed_cases_mismatch() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"visible_text": "safe"}),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-passed",
        expected_total_cases=1,
        expected_passed_cases=0,
        expected_failed_cases=0,
        expected_needs_review_cases=1,
        expected_all_passed=False,
        expected_status_counts={"passed": 0, "failed": 0, "needs_review": 1},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "passed_cases_mismatch" in result.mismatch_codes


def test_suite_assertion_reports_failed_cases_mismatch() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"state_delta": {"hp": -5}}),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-failed",
        expected_total_cases=1,
        expected_passed_cases=1,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "failed_cases_mismatch" in result.mismatch_codes


def test_suite_assertion_reports_needs_review_cases_mismatch() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {}, warnings=("warn-1",)),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-review",
        expected_total_cases=1,
        expected_passed_cases=1,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "needs_review_cases_mismatch" in result.mismatch_codes


def test_suite_assertion_reports_all_passed_mismatch() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"state_delta": {"hp": -5}}),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-all-passed",
        expected_total_cases=1,
        expected_passed_cases=0,
        expected_failed_cases=1,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 0, "failed": 1, "needs_review": 0},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "all_passed_mismatch" in result.mismatch_codes


def test_suite_assertion_reports_status_counts_mismatch() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"visible_text": "safe"}),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-status",
        expected_total_cases=1,
        expected_passed_cases=1,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 0, "failed": 0, "needs_review": 1},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "status_counts_mismatch" in result.mismatch_codes


def test_suite_assertion_reports_violation_counts_mismatch() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"state_delta": {"hp": -5}}),
    ])
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-violations",
        expected_total_cases=1,
        expected_passed_cases=0,
        expected_failed_cases=1,
        expected_needs_review_cases=0,
        expected_all_passed=False,
        expected_status_counts={"passed": 0, "failed": 1, "needs_review": 0},
        expected_violation_counts={},
    )

    result = assert_model_boundary_suite_result(
        expectation=expectation,
        actual_result=actual,
    )

    assert result.assertion_passed is False
    assert "violation_counts_mismatch" in result.mismatch_codes


def test_suite_assertion_rejects_invalid_expectation_object() -> None:
    actual = _make_actual_suite_result([
        _make_case("case-1", {"visible_text": "safe"}),
    ])
    with pytest.raises(ModelBoundaryAssertionError):
        assert_model_boundary_suite_result(
            expectation="not-an-expectation",  # type: ignore[arg-type]
            actual_result=actual,
        )


def test_suite_assertion_rejects_invalid_actual_result_object() -> None:
    expectation = create_model_boundary_expected_suite_outcome(
        expectation_ref="exp-suite-1",
        expected_total_cases=1,
        expected_passed_cases=1,
        expected_failed_cases=0,
        expected_needs_review_cases=0,
        expected_all_passed=True,
        expected_status_counts={"passed": 1, "failed": 0, "needs_review": 0},
    )
    with pytest.raises(ModelBoundaryAssertionError):
        assert_model_boundary_suite_result(
            expectation=expectation,
            actual_result="not-a-result",  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# Source scan — confirm no forbidden runtime/model authority dependencies
# ---------------------------------------------------------------------------

_FORBIDDEN_PATTERNS = (
    "roll_dice",
    "commit_event(",
    "apply_delta(",
    "mutate_state",
    "persist_state",
    "replay_event",
    "state_store.get",
    "event_ledger.get",
    "generate_narration",
    "call_model",
    "invoke_model",
    "openai",
    "anthropic",
)


def test_source_scan_for_forbidden_authority_usage() -> None:
    """The new module does not import or call forbidden runtime authority systems."""
    import pathlib

    module_path = pathlib.Path("src/astra_runtime/domain/model_boundary_evaluation.py")
    source = module_path.read_text(encoding="utf-8")

    for pattern in _FORBIDDEN_PATTERNS:
        assert pattern not in source, f"forbidden pattern found: {pattern!r}"
