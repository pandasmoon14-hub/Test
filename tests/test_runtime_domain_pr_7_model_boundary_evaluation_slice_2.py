"""Tests for PR-7 Slice 2 — Model Boundary Evaluation Suite and Summary Runner."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    MODEL_BOUNDARY_STATUS_VALUES,
    MODEL_BOUNDARY_VIOLATION_CODES,
    ContextPacketAssemblyRequest,
    ModelBoundaryEvaluationCase,
    ModelBoundaryEvaluationError,
    ModelBoundaryEvaluationResult,
    ModelBoundaryEvaluationSuite,
    ModelBoundaryEvaluationSuiteError,
    ModelBoundaryEvaluationSuiteResult,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_evaluation_case,
    create_model_boundary_evaluation_suite,
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


def _make_suite(
    cases: list[ModelBoundaryEvaluationCase] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryEvaluationSuite:
    """Build a valid ModelBoundaryEvaluationSuite."""
    if cases is None:
        cases = [_make_case("case-1", {"visible_text": "safe"})]
    return create_model_boundary_evaluation_suite(
        suite_ref="suite-1",
        suite_label="Test Suite",
        cases=cases,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------

def test_package_exports() -> None:
    """All PR-7 Slice 2 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        ModelBoundaryEvaluationSuite,
        ModelBoundaryEvaluationSuiteError,
        ModelBoundaryEvaluationSuiteResult,
        create_model_boundary_evaluation_suite,
        evaluate_model_boundary_suite,
    )

    assert ModelBoundaryEvaluationSuite is not None
    assert issubclass(ModelBoundaryEvaluationSuiteError, ModelBoundaryEvaluationError)
    assert ModelBoundaryEvaluationSuiteResult is not None
    assert callable(create_model_boundary_evaluation_suite)
    assert callable(evaluate_model_boundary_suite)


# ---------------------------------------------------------------------------
# ModelBoundaryEvaluationSuiteError
# ---------------------------------------------------------------------------

def test_suite_error_subclasses_model_boundary_evaluation_error() -> None:
    """ModelBoundaryEvaluationSuiteError subclasses ModelBoundaryEvaluationError."""
    assert issubclass(ModelBoundaryEvaluationSuiteError, ModelBoundaryEvaluationError)
    assert issubclass(ModelBoundaryEvaluationSuiteError, ValueError)


# ---------------------------------------------------------------------------
# ModelBoundaryEvaluationSuite construction and immutability
# ---------------------------------------------------------------------------

def test_suite_is_frozen() -> None:
    """ModelBoundaryEvaluationSuite instances are immutable."""
    suite = _make_suite()
    with pytest.raises(FrozenInstanceError):
        suite.suite_ref = "mutated"  # type: ignore[misc]


def test_suite_metadata_is_deep_copied_and_frozen() -> None:
    """Suite metadata is deep-copied and wrapped in MappingProxyType."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    suite = _make_suite(metadata=mutable_meta)

    assert isinstance(suite.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(suite.metadata["tags"]) == ["a", "b"]


def test_suite_cases_normalize_to_tuple() -> None:
    """Suite cases are normalized to a tuple."""
    case_list = [
        _make_case("case-1", {"visible_text": "one"}),
        _make_case("case-2", {"visible_text": "two"}),
    ]
    suite = _make_suite(cases=case_list)

    assert isinstance(suite.cases, tuple)
    assert len(suite.cases) == 2
    assert suite.cases[0].case_ref == "case-1"
    assert suite.cases[1].case_ref == "case-2"


def test_suite_rejects_empty_suite_ref() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        create_model_boundary_evaluation_suite(
            suite_ref="",
            suite_label="Test Suite",
            cases=[_make_case("case-1", {"visible_text": "safe"})],
        )


def test_suite_rejects_empty_suite_label() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        create_model_boundary_evaluation_suite(
            suite_ref="suite-1",
            suite_label="",
            cases=[_make_case("case-1", {"visible_text": "safe"})],
        )


def test_suite_rejects_empty_cases() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        create_model_boundary_evaluation_suite(
            suite_ref="suite-1",
            suite_label="Test Suite",
            cases=[],
        )


def test_suite_rejects_non_case_values_in_cases() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        create_model_boundary_evaluation_suite(
            suite_ref="suite-1",
            suite_label="Test Suite",
            cases=["not-a-case"],  # type: ignore[list-item]
        )


def test_suite_rejects_duplicate_case_ref() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        create_model_boundary_evaluation_suite(
            suite_ref="suite-1",
            suite_label="Test Suite",
            cases=[
                _make_case("case-1", {"visible_text": "one"}),
                _make_case("case-1", {"visible_text": "two"}),
            ],
        )


# ---------------------------------------------------------------------------
# ModelBoundaryEvaluationSuiteResult construction and immutability
# ---------------------------------------------------------------------------

def _make_result(**overrides: Any) -> ModelBoundaryEvaluationSuiteResult:
    """Build a minimal valid suite result, allowing overrides."""
    defaults: dict[str, Any] = {
        "suite_ref": "suite-1",
        "suite_label": "Test Suite",
        "total_cases": 1,
        "passed_cases": 1,
        "failed_cases": 0,
        "needs_review_cases": 0,
        "all_passed": True,
        "case_results": [
            ModelBoundaryEvaluationResult(
                case_ref="case-1",
                candidate_model_ref="model-1",
                packet_kind="single_event_narration",
                expected_output_family="narration_display",
                status="passed",
                passed=True,
                violation_codes=(),
                forbidden_field_hits=(),
                packet_warning_refs=(),
            )
        ],
        "status_counts": {"passed": 1, "failed": 0, "needs_review": 0},
        "violation_counts": {},
    }
    defaults.update(overrides)
    return ModelBoundaryEvaluationSuiteResult(**defaults)


def test_suite_result_is_frozen() -> None:
    """ModelBoundaryEvaluationSuiteResult instances are immutable."""
    result = _make_result()
    with pytest.raises(FrozenInstanceError):
        result.all_passed = False  # type: ignore[misc]


def test_suite_result_freezes_status_counts() -> None:
    """Suite result status_counts are frozen with MappingProxyType."""
    mutable_counts: dict[str, int] = {"passed": 1, "failed": 0, "needs_review": 0}
    result = _make_result(status_counts=mutable_counts)

    assert isinstance(result.status_counts, MappingProxyType)
    mutable_counts["passed"] = 99
    assert result.status_counts["passed"] == 1


def test_suite_result_freezes_violation_counts() -> None:
    """Suite result violation_counts are frozen with MappingProxyType."""
    mutable_counts: dict[str, int] = {"candidate_output_empty": 1}
    result = _make_result(violation_counts=mutable_counts)

    assert isinstance(result.violation_counts, MappingProxyType)
    mutable_counts["candidate_output_empty"] = 99
    assert result.violation_counts["candidate_output_empty"] == 1


def test_suite_result_freezes_metadata() -> None:
    """Suite result metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    result = _make_result(metadata=mutable_meta)

    assert isinstance(result.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(result.metadata["tags"]) == ["a", "b"]


def test_suite_result_rejects_negative_counts() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        _make_result(total_cases=-1)


def test_suite_result_rejects_bool_counts() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        _make_result(total_cases=True)  # type: ignore[arg-type]


def test_suite_result_rejects_unknown_status_key() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        _make_result(status_counts={"passed": 1, "unknown": 0})


def test_suite_result_rejects_unknown_violation_key() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        _make_result(violation_counts={"not_a_code": 1})


def test_suite_result_rejects_total_cases_mismatch() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        _make_result(total_cases=2, passed_cases=1)


def test_suite_result_rejects_count_sum_mismatch() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        _make_result(
            total_cases=2,
            passed_cases=1,
            failed_cases=1,
            needs_review_cases=1,
            case_results=[
                ModelBoundaryEvaluationResult(
                    case_ref="case-1",
                    candidate_model_ref="model-1",
                    packet_kind="single_event_narration",
                    expected_output_family="narration_display",
                    status="passed",
                    passed=True,
                    violation_codes=(),
                    forbidden_field_hits=(),
                    packet_warning_refs=(),
                ),
                ModelBoundaryEvaluationResult(
                    case_ref="case-2",
                    candidate_model_ref="model-1",
                    packet_kind="single_event_narration",
                    expected_output_family="narration_display",
                    status="failed",
                    passed=False,
                    violation_codes=("candidate_output_empty",),
                    forbidden_field_hits=(),
                    packet_warning_refs=(),
                ),
            ],
        )


# ---------------------------------------------------------------------------
# Factory and evaluator behavior
# ---------------------------------------------------------------------------

def test_factory_creates_valid_suite() -> None:
    case = _make_case("case-1", {"visible_text": "safe"})
    suite = create_model_boundary_evaluation_suite(
        suite_ref="suite-factory",
        suite_label="Factory Suite",
        cases=[case],
        metadata={"source": "test"},
    )

    assert suite.suite_ref == "suite-factory"
    assert suite.suite_label == "Factory Suite"
    assert suite.cases == (case,)
    assert isinstance(suite.metadata, MappingProxyType)


def test_evaluator_rejects_non_suite_input() -> None:
    with pytest.raises(ModelBoundaryEvaluationSuiteError):
        evaluate_model_boundary_suite("not a suite")  # type: ignore[arg-type]


def test_evaluator_passes_suite_with_all_safe_candidate_outputs() -> None:
    suite = create_model_boundary_evaluation_suite(
        suite_ref="suite-safe",
        suite_label="All Safe",
        cases=[
            _make_case("case-1", {"visible_text": "one"}),
            _make_case("case-2", {"visible_text": "two"}),
        ],
    )
    result = evaluate_model_boundary_suite(suite)

    assert result.suite_ref == "suite-safe"
    assert result.suite_label == "All Safe"
    assert result.total_cases == 2
    assert result.passed_cases == 2
    assert result.failed_cases == 0
    assert result.needs_review_cases == 0
    assert result.all_passed is True


def test_evaluator_preserves_case_result_order() -> None:
    cases = [
        _make_case("case-a", {"visible_text": "a"}),
        _make_case("case-b", {"state_delta": {"hp": -5}}),
        _make_case("case-c", {"visible_text": "c"}),
    ]
    suite = _make_suite(cases=cases)
    result = evaluate_model_boundary_suite(suite)

    refs = [r.case_ref for r in result.case_results]
    assert refs == ["case-a", "case-b", "case-c"]


def test_evaluator_counts_passed_failed_needs_review() -> None:
    suite = _make_suite(cases=[
        _make_case("case-pass", {"visible_text": "safe"}),
        _make_case("case-fail", {"state_delta": {"hp": -5}}),
        _make_case("case-review", {}, warnings=("audit_warning",)),
    ])
    result = evaluate_model_boundary_suite(suite)

    assert result.total_cases == 3
    assert result.passed_cases == 1
    assert result.failed_cases == 1
    assert result.needs_review_cases == 1
    assert result.all_passed is False


def test_evaluator_produces_status_counts_with_all_status_keys() -> None:
    suite = _make_suite(cases=[
        _make_case("case-pass", {"visible_text": "safe"}),
    ])
    result = evaluate_model_boundary_suite(suite)

    assert set(result.status_counts.keys()) == MODEL_BOUNDARY_STATUS_VALUES
    assert result.status_counts["passed"] == 1
    assert result.status_counts["failed"] == 0
    assert result.status_counts["needs_review"] == 0


def test_evaluator_produces_deterministic_violation_counts() -> None:
    suite = _make_suite(cases=[
        _make_case("case-1", {"state_delta": {"hp": -5}, "hidden_fact": "x"}),
        _make_case("case-2", {"state_delta": {"hp": -3}}),
        _make_case("case-3", {"dice_result": 4}),
    ])
    result = evaluate_model_boundary_suite(suite)

    assert list(result.violation_counts.keys()) == sorted(
        result.violation_counts.keys()
    )
    assert result.violation_counts["state_mutation_claim_present"] == 2
    assert result.violation_counts["hidden_information_claim_present"] == 1
    assert result.violation_counts["random_result_claim_present"] == 1
    assert result.violation_counts["forbidden_authority_field_present"] == 3


def test_evaluator_handles_packet_warning_only_cases_as_needs_review() -> None:
    suite = _make_suite(cases=[
        _make_case("case-1", {"visible_text": "safe"}, warnings=("warn-1",)),
    ])
    result = evaluate_model_boundary_suite(suite)

    assert result.needs_review_cases == 1
    assert result.status_counts["needs_review"] == 1
    case_result = result.case_results[0]
    assert case_result.status == "needs_review"
    assert "packet_warning_present" in case_result.violation_codes


def test_evaluator_handles_hard_violations_as_failed() -> None:
    suite = _make_suite(cases=[
        _make_case("case-1", {"state_delta": {"hp": -5}}),
    ])
    result = evaluate_model_boundary_suite(suite)

    assert result.failed_cases == 1
    assert result.status_counts["failed"] == 1
    assert result.all_passed is False


def test_evaluator_sets_all_passed_false_if_any_case_fails_or_needs_review() -> None:
    suite = _make_suite(cases=[
        _make_case("case-pass", {"visible_text": "safe"}),
        _make_case("case-fail", {"state_delta": {"hp": -5}}),
        _make_case("case-review", {}, warnings=("warn-1",)),
    ])
    result = evaluate_model_boundary_suite(suite)

    assert result.all_passed is False


def test_evaluator_does_not_mutate_suite_cases_or_candidate_outputs() -> None:
    candidate: dict[str, Any] = {"visible_text": "safe"}
    case = _make_case("case-1", candidate)
    original_candidate_id = id(case.candidate_output)
    suite = _make_suite(cases=[case])
    original_cases_id = id(suite.cases)

    result = evaluate_model_boundary_suite(suite)

    assert id(suite.cases) == original_cases_id
    assert id(case.candidate_output) == original_candidate_id
    assert case.candidate_output["visible_text"] == "safe"
    assert candidate == {"visible_text": "safe"}
    assert result.case_results[0].case_ref == case.case_ref


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
