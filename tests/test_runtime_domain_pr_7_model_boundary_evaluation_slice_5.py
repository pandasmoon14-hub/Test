"""Tests for PR-7 Slice 5 — Captured Fixture Assertion Runner."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    ModelBoundaryCapturedFixtureAssertionError,
    ModelBoundaryCapturedFixtureAssertionResult,
    ModelBoundaryCapturedOutputFixture,
    ModelBoundaryEvaluationCase,
    ModelBoundaryEvaluationError,
    ModelBoundaryEvaluationResult,
    assert_model_boundary_captured_output_fixture,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_captured_output_fixture,
    create_model_boundary_expected_case_outcome,
    evaluate_model_boundary_case,
)
from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
)
from astra_runtime.domain.model_boundary_evaluation import (
    MODEL_BOUNDARY_OUTPUT_FAMILIES,
    ModelBoundaryCaseAssertionResult,
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


def _make_fixture(
    *,
    fixture_ref: str = "fixture-1",
    capture_ref: str = "capture-1",
    candidate_model_ref: str = "model-1",
    expected_output_family: str = "narration_display",
    packet_result: ContextPacketCompilerResult | None = None,
    candidate_output: dict[str, Any] | None = None,
    raw_captured_text: str | None = "The knight moves forward.",
    evaluator_notes: tuple[str, ...] = ("note-1",),
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedOutputFixture:
    """Build a valid ModelBoundaryCapturedOutputFixture."""
    return create_model_boundary_captured_output_fixture(
        fixture_ref=fixture_ref,
        capture_ref=capture_ref,
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_result=packet_result if packet_result is not None else _make_packet_result(),
        candidate_output=candidate_output if candidate_output is not None else {"display": "The knight moves forward."},
        raw_captured_text=raw_captured_text,
        evaluator_notes=evaluator_notes,
        metadata=metadata if metadata is not None else {"source": "manual"},
    )


def _make_expectation(
    *,
    expectation_ref: str = "exp-1",
    expected_status: str = "passed",
    expected_passed: bool = True,
    expected_violation_codes: tuple[str, ...] = (),
    expected_forbidden_field_hits: tuple[str, ...] = (),
    expected_packet_warning_refs: tuple[str, ...] = (),
    metadata: dict[str, Any] | None = None,
) -> Any:
    """Build a valid ModelBoundaryExpectedCaseOutcome."""
    return create_model_boundary_expected_case_outcome(
        expectation_ref=expectation_ref,
        expected_status=expected_status,
        expected_passed=expected_passed,
        expected_violation_codes=expected_violation_codes,
        expected_forbidden_field_hits=expected_forbidden_field_hits,
        expected_packet_warning_refs=expected_packet_warning_refs,
        metadata=metadata if metadata is not None else {},
    )


def _make_valid_evaluation_result(
    *,
    case_ref: str = "case-1",
    candidate_model_ref: str = "model-1",
    expected_output_family: str = "narration_display",
) -> ModelBoundaryEvaluationResult:
    """Build a valid ModelBoundaryEvaluationResult."""
    fixture = _make_fixture(
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
    )
    case = ModelBoundaryEvaluationCase(
        case_ref=case_ref,
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_result=fixture.packet_result,
        candidate_output=fixture.candidate_output,
    )
    return evaluate_model_boundary_case(case)


def _make_valid_assertion_result(
    *,
    expectation_ref: str = "exp-1",
    case_ref: str = "case-1",
    assertion_passed: bool = True,
) -> ModelBoundaryCaseAssertionResult:
    """Build a valid ModelBoundaryCaseAssertionResult."""
    return ModelBoundaryCaseAssertionResult(
        expectation_ref=expectation_ref,
        case_ref=case_ref,
        assertion_passed=assertion_passed,
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


def _make_valid_result(
    *,
    fixture_ref: str = "fixture-1",
    capture_ref: str = "capture-1",
    case_ref: str = "case-1",
    expectation_ref: str = "exp-1",
    candidate_model_ref: str = "model-1",
    expected_output_family: str = "narration_display",
    assertion_passed: bool = True,
    has_raw_captured_text: bool = True,
    evaluator_notes: tuple[str, ...] = ("note-1",),
    metadata: dict[str, Any] | None = None,
    evaluation_result: ModelBoundaryEvaluationResult | None = None,
    assertion_result: ModelBoundaryCaseAssertionResult | None = None,
) -> ModelBoundaryCapturedFixtureAssertionResult:
    """Build a valid captured-fixture assertion result."""
    if evaluation_result is None:
        evaluation_result = _make_valid_evaluation_result(
            case_ref=case_ref,
            candidate_model_ref=candidate_model_ref,
            expected_output_family=expected_output_family,
        )
    if assertion_result is None:
        assertion_result = _make_valid_assertion_result(
            expectation_ref=expectation_ref,
            case_ref=case_ref,
            assertion_passed=assertion_passed,
        )
    return ModelBoundaryCapturedFixtureAssertionResult(
        fixture_ref=fixture_ref,
        capture_ref=capture_ref,
        case_ref=case_ref,
        expectation_ref=expectation_ref,
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        assertion_passed=assertion_passed,
        evaluation_result=evaluation_result,
        assertion_result=assertion_result,
        has_raw_captured_text=has_raw_captured_text,
        evaluator_notes=evaluator_notes,
        metadata=metadata if metadata is not None else {},
    )


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------

def test_package_exports() -> None:
    """All PR-7 Slice 5 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        ModelBoundaryCapturedFixtureAssertionError,
        ModelBoundaryCapturedFixtureAssertionResult,
        assert_model_boundary_captured_output_fixture,
    )

    assert issubclass(ModelBoundaryCapturedFixtureAssertionError, ModelBoundaryEvaluationError)
    assert ModelBoundaryCapturedFixtureAssertionResult is not None
    assert callable(assert_model_boundary_captured_output_fixture)


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedFixtureAssertionError
# ---------------------------------------------------------------------------

def test_captured_fixture_assertion_error_subclasses_model_boundary_evaluation_error() -> None:
    """ModelBoundaryCapturedFixtureAssertionError subclasses ModelBoundaryEvaluationError."""
    assert issubclass(ModelBoundaryCapturedFixtureAssertionError, ModelBoundaryEvaluationError)
    assert issubclass(ModelBoundaryCapturedFixtureAssertionError, ValueError)


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedFixtureAssertionResult
# ---------------------------------------------------------------------------

def test_captured_fixture_assertion_result_is_frozen() -> None:
    """ModelBoundaryCapturedFixtureAssertionResult instances are immutable."""
    result = _make_valid_result()
    with pytest.raises(FrozenInstanceError):
        result.fixture_ref = "other"  # type: ignore[misc]


def test_captured_fixture_assertion_result_metadata_is_deep_copied_and_frozen() -> None:
    """Metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    result = _make_valid_result(metadata=mutable_meta)

    assert isinstance(result.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(result.metadata["tags"]) == ["a", "b"]


def test_captured_fixture_assertion_result_normalizes_evaluator_notes_to_tuple() -> None:
    """Evaluator notes are normalized to a tuple of strings."""
    result = _make_valid_result(evaluator_notes=["note-a", "note-b"])
    assert result.evaluator_notes == ("note-a", "note-b")


def test_captured_fixture_assertion_result_rejects_empty_fixture_ref() -> None:
    """Empty fixture_ref is rejected."""
    base = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref="",
            capture_ref=base.capture_ref,
            case_ref=base.case_ref,
            expectation_ref=base.expectation_ref,
            candidate_model_ref=base.candidate_model_ref,
            expected_output_family=base.expected_output_family,
            assertion_passed=True,
            evaluation_result=base.evaluation_result,
            assertion_result=base.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_empty_capture_ref() -> None:
    """Empty capture_ref is rejected."""
    base = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=base.fixture_ref,
            capture_ref="",
            case_ref=base.case_ref,
            expectation_ref=base.expectation_ref,
            candidate_model_ref=base.candidate_model_ref,
            expected_output_family=base.expected_output_family,
            assertion_passed=True,
            evaluation_result=base.evaluation_result,
            assertion_result=base.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_empty_case_ref() -> None:
    """Empty case_ref is rejected."""
    base = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=base.fixture_ref,
            capture_ref=base.capture_ref,
            case_ref="",
            expectation_ref=base.expectation_ref,
            candidate_model_ref=base.candidate_model_ref,
            expected_output_family=base.expected_output_family,
            assertion_passed=True,
            evaluation_result=base.evaluation_result,
            assertion_result=base.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_empty_expectation_ref() -> None:
    """Empty expectation_ref is rejected."""
    base = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=base.fixture_ref,
            capture_ref=base.capture_ref,
            case_ref=base.case_ref,
            expectation_ref="",
            candidate_model_ref=base.candidate_model_ref,
            expected_output_family=base.expected_output_family,
            assertion_passed=True,
            evaluation_result=base.evaluation_result,
            assertion_result=base.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_empty_candidate_model_ref() -> None:
    """Empty candidate_model_ref is rejected."""
    base = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=base.fixture_ref,
            capture_ref=base.capture_ref,
            case_ref=base.case_ref,
            expectation_ref=base.expectation_ref,
            candidate_model_ref="",
            expected_output_family=base.expected_output_family,
            assertion_passed=True,
            evaluation_result=base.evaluation_result,
            assertion_result=base.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_unknown_output_family() -> None:
    """Unknown expected_output_family is rejected."""
    base = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=base.fixture_ref,
            capture_ref=base.capture_ref,
            case_ref=base.case_ref,
            expectation_ref=base.expectation_ref,
            candidate_model_ref=base.candidate_model_ref,
            expected_output_family="not_a_family",
            assertion_passed=True,
            evaluation_result=base.evaluation_result,
            assertion_result=base.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_non_bool_assertion_passed() -> None:
    """Non-bool assertion_passed is rejected."""
    base = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=base.fixture_ref,
            capture_ref=base.capture_ref,
            case_ref=base.case_ref,
            expectation_ref=base.expectation_ref,
            candidate_model_ref=base.candidate_model_ref,
            expected_output_family=base.expected_output_family,
            assertion_passed="yes",  # type: ignore[arg-type]
            evaluation_result=base.evaluation_result,
            assertion_result=base.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_non_evaluation_result() -> None:
    """Non-ModelBoundaryEvaluationResult evaluation_result is rejected."""
    result = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=result.fixture_ref,
            capture_ref=result.capture_ref,
            case_ref=result.case_ref,
            expectation_ref=result.expectation_ref,
            candidate_model_ref=result.candidate_model_ref,
            expected_output_family=result.expected_output_family,
            assertion_passed=True,
            evaluation_result="not-a-result",  # type: ignore[arg-type]
            assertion_result=result.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_non_assertion_result() -> None:
    """Non-ModelBoundaryCaseAssertionResult assertion_result is rejected."""
    result = _make_valid_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=result.fixture_ref,
            capture_ref=result.capture_ref,
            case_ref=result.case_ref,
            expectation_ref=result.expectation_ref,
            candidate_model_ref=result.candidate_model_ref,
            expected_output_family=result.expected_output_family,
            assertion_passed=True,
            evaluation_result=result.evaluation_result,
            assertion_result="not-a-result",  # type: ignore[arg-type]
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_assertion_passed_mismatch() -> None:
    """assertion_passed must equal assertion_result.assertion_passed."""
    result = _make_valid_result(assertion_passed=True)
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=result.fixture_ref,
            capture_ref=result.capture_ref,
            case_ref=result.case_ref,
            expectation_ref=result.expectation_ref,
            candidate_model_ref=result.candidate_model_ref,
            expected_output_family=result.expected_output_family,
            assertion_passed=False,
            evaluation_result=result.evaluation_result,
            assertion_result=result.assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_case_ref_mismatch() -> None:
    """case_ref must equal evaluation_result.case_ref."""
    evaluation_result = _make_valid_evaluation_result(case_ref="case-2")
    assertion_result = _make_valid_assertion_result(case_ref="case-2")
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref="fixture-1",
            capture_ref="capture-1",
            case_ref="case-1",
            expectation_ref="exp-1",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            assertion_passed=True,
            evaluation_result=evaluation_result,
            assertion_result=assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_expectation_ref_mismatch() -> None:
    """expectation_ref must equal assertion_result.expectation_ref."""
    result = _make_valid_result(expectation_ref="exp-1")
    assertion_result = ModelBoundaryCaseAssertionResult(
        expectation_ref="exp-2",
        case_ref=result.case_ref,
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
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=result.fixture_ref,
            capture_ref=result.capture_ref,
            case_ref=result.case_ref,
            expectation_ref="exp-1",
            candidate_model_ref=result.candidate_model_ref,
            expected_output_family=result.expected_output_family,
            assertion_passed=True,
            evaluation_result=result.evaluation_result,
            assertion_result=assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_candidate_model_ref_mismatch() -> None:
    """candidate_model_ref must equal evaluation_result.candidate_model_ref."""
    fixture = _make_fixture(candidate_model_ref="model-1")
    case = ModelBoundaryEvaluationCase(
        case_ref="case-1",
        candidate_model_ref="model-2",
        expected_output_family=fixture.expected_output_family,
        packet_result=fixture.packet_result,
        candidate_output=fixture.candidate_output,
    )
    evaluation_result = evaluate_model_boundary_case(case)
    assertion_result = ModelBoundaryCaseAssertionResult(
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
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=fixture.fixture_ref,
            capture_ref=fixture.capture_ref,
            case_ref="case-1",
            expectation_ref="exp-1",
            candidate_model_ref="model-1",
            expected_output_family=fixture.expected_output_family,
            assertion_passed=True,
            evaluation_result=evaluation_result,
            assertion_result=assertion_result,
            has_raw_captured_text=True,
        )


def test_captured_fixture_assertion_result_rejects_expected_output_family_mismatch() -> None:
    """expected_output_family must equal evaluation_result.expected_output_family."""
    fixture = _make_fixture(expected_output_family="narration_display")
    case = ModelBoundaryEvaluationCase(
        case_ref="case-1",
        candidate_model_ref=fixture.candidate_model_ref,
        expected_output_family="visible_summary",
        packet_result=fixture.packet_result,
        candidate_output=fixture.candidate_output,
    )
    evaluation_result = evaluate_model_boundary_case(case)
    assertion_result = ModelBoundaryCaseAssertionResult(
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
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        ModelBoundaryCapturedFixtureAssertionResult(
            fixture_ref=fixture.fixture_ref,
            capture_ref=fixture.capture_ref,
            case_ref="case-1",
            expectation_ref="exp-1",
            candidate_model_ref=fixture.candidate_model_ref,
            expected_output_family="narration_display",
            assertion_passed=True,
            evaluation_result=evaluation_result,
            assertion_result=assertion_result,
            has_raw_captured_text=True,
        )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def test_runner_rejects_non_fixture_input() -> None:
    """Runner rejects input that is not a ModelBoundaryCapturedOutputFixture."""
    expectation = _make_expectation()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        assert_model_boundary_captured_output_fixture(
            fixture="not-a-fixture",  # type: ignore[arg-type]
            expectation=expectation,
        )


def test_runner_rejects_non_expectation_input() -> None:
    """Runner rejects input that is not a ModelBoundaryExpectedCaseOutcome."""
    fixture = _make_fixture()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        assert_model_boundary_captured_output_fixture(
            fixture=fixture,
            expectation="not-an-expectation",  # type: ignore[arg-type]
        )


def test_runner_rejects_blank_explicit_case_ref() -> None:
    """Runner rejects a blank explicit case_ref."""
    fixture = _make_fixture()
    expectation = _make_expectation()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionError):
        assert_model_boundary_captured_output_fixture(
            fixture=fixture,
            expectation=expectation,
            case_ref="",
        )


def test_runner_creates_case_from_fixture() -> None:
    """Runner derives a ModelBoundaryEvaluationCase from the fixture."""
    fixture = _make_fixture(fixture_ref="fixture-1")
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.case_ref == "fixture-1"
    assert isinstance(result.evaluation_result, ModelBoundaryEvaluationResult)


def test_runner_evaluates_the_case() -> None:
    """Runner evaluates the derived case structurally."""
    fixture = _make_fixture()
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.evaluation_result.status == "passed"
    assert result.evaluation_result.passed is True


def test_runner_asserts_actual_result_against_expected_outcome() -> None:
    """Runner asserts the evaluation result against the expected outcome."""
    fixture = _make_fixture()
    expectation = _make_expectation(expected_status="passed", expected_passed=True)
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.assertion_result.assertion_passed is True
    assert result.assertion_result.expected_status == "passed"
    assert result.assertion_result.actual_status == "passed"


def test_runner_returns_passing_combined_result_for_matching_expectation() -> None:
    """Runner returns a passing combined result when expectation matches."""
    fixture = _make_fixture()
    expectation = _make_expectation(expected_status="passed", expected_passed=True)
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert isinstance(result, ModelBoundaryCapturedFixtureAssertionResult)
    assert result.assertion_passed is True


def test_runner_returns_failing_combined_result_for_mismatching_expectation_without_raising() -> None:
    """Runner returns a failing result for mismatched expectation without raising."""
    fixture = _make_fixture()
    expectation = _make_expectation(expected_status="failed", expected_passed=False)
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.assertion_passed is False
    assert "status_mismatch" in result.assertion_result.mismatch_codes


def test_runner_preserves_fixture_ref_and_capture_ref() -> None:
    """Runner preserves fixture_ref and capture_ref from the fixture."""
    fixture = _make_fixture(fixture_ref="fx-1", capture_ref="cap-1")
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.fixture_ref == "fx-1"
    assert result.capture_ref == "cap-1"


def test_runner_preserves_candidate_model_ref() -> None:
    """Runner preserves candidate_model_ref from the fixture."""
    fixture = _make_fixture(candidate_model_ref="model-alpha")
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.candidate_model_ref == "model-alpha"
    assert result.evaluation_result.candidate_model_ref == "model-alpha"


def test_runner_preserves_expected_output_family() -> None:
    """Runner preserves expected_output_family from the fixture."""
    fixture = _make_fixture(expected_output_family="visible_summary")
    expectation = _make_expectation(expected_status="passed", expected_passed=True)
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.expected_output_family == "visible_summary"
    assert result.evaluation_result.expected_output_family == "visible_summary"


def test_runner_preserves_evaluator_notes() -> None:
    """Runner preserves evaluator notes from the fixture."""
    fixture = _make_fixture(evaluator_notes=["note-a", "note-b"])
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.evaluator_notes == ("note-a", "note-b")


def test_runner_sets_has_raw_captured_text_true_when_raw_text_exists() -> None:
    """has_raw_captured_text is True when fixture has raw captured text."""
    fixture = _make_fixture(raw_captured_text="raw text")
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.has_raw_captured_text is True


def test_runner_sets_has_raw_captured_text_false_when_raw_text_is_absent() -> None:
    """has_raw_captured_text is False when fixture has no raw captured text."""
    fixture = _make_fixture(raw_captured_text=None)
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    assert result.has_raw_captured_text is False


def test_runner_default_metadata_includes_identity_and_raw_text_presence() -> None:
    """Default result metadata includes fixture identity and has_raw_captured_text."""
    fixture = _make_fixture(
        fixture_ref="fx-1",
        capture_ref="cap-1",
        raw_captured_text="raw text",
        metadata={"source": "manual"},
    )
    expectation = _make_expectation(expectation_ref="exp-1")
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
        case_ref="case-1",
    )

    assert result.metadata["fixture_ref"] == "fx-1"
    assert result.metadata["capture_ref"] == "cap-1"
    assert result.metadata["case_ref"] == "case-1"
    assert result.metadata["expectation_ref"] == "exp-1"
    assert result.metadata["has_raw_captured_text"] is True
    assert result.metadata["source"] == "manual"


def test_runner_uses_result_metadata_override_when_supplied() -> None:
    """Runner uses caller-supplied result_metadata instead of the default."""
    fixture = _make_fixture(metadata={"source": "manual"})
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
        result_metadata={"override": True},
    )

    assert dict(result.metadata) == {"override": True}
    assert "fixture_ref" not in result.metadata


def test_runner_does_not_include_raw_captured_text_in_result_metadata() -> None:
    """Raw captured text is never copied into result metadata."""
    fixture = _make_fixture(raw_captured_text="sensitive raw text")
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
    )

    for value in result.metadata.values():
        assert value != "sensitive raw text"
    assert "raw_captured_text" not in result.metadata


def test_runner_passes_case_metadata_to_generated_case() -> None:
    """Runner passes case_metadata to the generated case."""
    fixture = _make_fixture()
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
        case_metadata={"case_tag": "value"},
    )

    # case_metadata is accepted and the runner produces a valid combined result;
    # the generated case itself is not exposed, but the call path succeeds.
    assert isinstance(result, ModelBoundaryCapturedFixtureAssertionResult)
    assert result.assertion_passed is True


def test_runner_passes_assertion_metadata_to_assertion_helper() -> None:
    """Runner passes assertion_metadata to the assertion helper."""
    fixture = _make_fixture()
    expectation = _make_expectation()
    result = assert_model_boundary_captured_output_fixture(
        fixture=fixture,
        expectation=expectation,
        assertion_metadata={"assertion_tag": "value"},
    )

    assert result.assertion_result.metadata["assertion_tag"] == "value"


# ---------------------------------------------------------------------------
# Source scan
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
    "json.loads",
    "ast.literal_eval",
    "re.search",
    "re.match",
)


def test_module_source_does_not_import_or_call_forbidden_systems() -> None:
    """Module source contains no forbidden runtime/model/prose-parsing imports or calls."""
    import pathlib

    source = pathlib.Path("src/astra_runtime/domain/model_boundary_evaluation.py").read_text()
    for pattern in _FORBIDDEN_PATTERNS:
        assert pattern not in source, f"forbidden pattern found: {pattern!r}"
