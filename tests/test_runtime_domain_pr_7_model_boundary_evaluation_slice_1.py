"""Tests for PR-7 Slice 1 — Model Boundary Evaluation Case and Result Skeleton."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    MODEL_BOUNDARY_OUTPUT_FAMILIES,
    MODEL_BOUNDARY_STATUS_VALUES,
    MODEL_BOUNDARY_VIOLATION_CODES,
    ModelBoundaryEvaluationCase,
    ModelBoundaryEvaluationError,
    ModelBoundaryEvaluationResult,
    create_context_packet_assembly_request,
    compile_context_packet_from_request,
    create_model_boundary_evaluation_case,
    evaluate_model_boundary_case,
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
        # Reconstruct result with injected warnings for test scenarios.
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
    candidate_output: dict[str, Any],
    expected_output_family: str = "narration_display",
    warnings: tuple[str, ...] = (),
) -> ModelBoundaryEvaluationCase:
    """Build a valid ModelBoundaryEvaluationCase around a candidate output."""
    return create_model_boundary_evaluation_case(
        case_ref="case-1",
        candidate_model_ref="model-1",
        expected_output_family=expected_output_family,
        packet_result=_make_packet_result(warnings=warnings),
        candidate_output=candidate_output,
    )


# ---------------------------------------------------------------------------
# Package exports and constants
# ---------------------------------------------------------------------------

def test_package_exports() -> None:
    """All PR-7 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        MODEL_BOUNDARY_OUTPUT_FAMILIES,
        MODEL_BOUNDARY_STATUS_VALUES,
        MODEL_BOUNDARY_VIOLATION_CODES,
        ModelBoundaryEvaluationCase,
        ModelBoundaryEvaluationError,
        ModelBoundaryEvaluationResult,
        create_model_boundary_evaluation_case,
        evaluate_model_boundary_case,
    )

    assert isinstance(MODEL_BOUNDARY_OUTPUT_FAMILIES, frozenset)
    assert isinstance(MODEL_BOUNDARY_STATUS_VALUES, frozenset)
    assert isinstance(MODEL_BOUNDARY_VIOLATION_CODES, frozenset)
    assert issubclass(ModelBoundaryEvaluationError, ValueError)
    assert ModelBoundaryEvaluationCase is not None
    assert ModelBoundaryEvaluationResult is not None
    assert callable(create_model_boundary_evaluation_case)
    assert callable(evaluate_model_boundary_case)


def test_constants_are_frozensets_with_expected_values() -> None:
    """Constants match the PR-7 specification exactly."""
    assert MODEL_BOUNDARY_OUTPUT_FAMILIES == frozenset({
        "intent_proposal",
        "narration_display",
        "visible_summary",
        "clarification",
        "evaluation_note",
    })
    assert MODEL_BOUNDARY_STATUS_VALUES == frozenset({
        "passed",
        "failed",
        "needs_review",
    })
    expected_violations = frozenset({
        "candidate_output_not_mapping",
        "candidate_output_empty",
        "forbidden_authority_field_present",
        "hidden_information_claim_present",
        "state_mutation_claim_present",
        "event_commit_claim_present",
        "random_result_claim_present",
        "durable_truth_claim_present",
        "packet_warning_present",
    })
    assert MODEL_BOUNDARY_VIOLATION_CODES == expected_violations


def test_error_subclasses_value_error() -> None:
    """ModelBoundaryEvaluationError is a ValueError subclass."""
    assert issubclass(ModelBoundaryEvaluationError, ValueError)


# ---------------------------------------------------------------------------
# ModelBoundaryEvaluationCase construction and immutability
# ---------------------------------------------------------------------------

def test_case_is_frozen() -> None:
    """ModelBoundaryEvaluationCase instances are immutable."""
    case = _make_case({"visible_text": "hello"})
    with pytest.raises(FrozenInstanceError):
        case.case_ref = "mutated"  # type: ignore[misc]


def test_case_freezes_and_deep_copies_candidate_output() -> None:
    """candidate_output is deep-copied and wrapped in MappingProxyType."""
    mutable: dict[str, Any] = {"nested": {"key": "value"}, "items": [1, 2]}
    case = _make_case(mutable)

    assert isinstance(case.candidate_output, MappingProxyType)
    # Mutating original should not affect frozen case.
    mutable["nested"]["key"] = "changed"
    mutable["items"].append(3)
    assert case.candidate_output["nested"]["key"] == "value"
    assert list(case.candidate_output["items"]) == [1, 2]


def test_case_freezes_and_deep_copies_metadata() -> None:
    """metadata is deep-copied and wrapped in MappingProxyType."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    case = create_model_boundary_evaluation_case(
        case_ref="case-meta",
        candidate_model_ref="model-1",
        expected_output_family="narration_display",
        packet_result=_make_packet_result(),
        candidate_output={"text": "hello"},
        metadata=mutable_meta,
    )

    assert isinstance(case.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(case.metadata["tags"]) == ["a", "b"]


def test_case_normalizes_evaluator_notes_to_tuple() -> None:
    """evaluator_notes are normalized to a tuple of strings."""
    case = create_model_boundary_evaluation_case(
        case_ref="case-notes",
        candidate_model_ref="model-1",
        expected_output_family="narration_display",
        packet_result=_make_packet_result(),
        candidate_output={"text": "hello"},
        evaluator_notes=["note-1", "note-2"],
    )

    assert isinstance(case.evaluator_notes, tuple)
    assert case.evaluator_notes == ("note-1", "note-2")


def test_case_rejects_empty_case_ref() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        create_model_boundary_evaluation_case(
            case_ref="",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            packet_result=_make_packet_result(),
            candidate_output={"text": "hello"},
        )


def test_case_rejects_empty_candidate_model_ref() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        create_model_boundary_evaluation_case(
            case_ref="case-1",
            candidate_model_ref="",
            expected_output_family="narration_display",
            packet_result=_make_packet_result(),
            candidate_output={"text": "hello"},
        )


def test_case_rejects_unknown_expected_output_family() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        create_model_boundary_evaluation_case(
            case_ref="case-1",
            candidate_model_ref="model-1",
            expected_output_family="unknown_family",
            packet_result=_make_packet_result(),
            candidate_output={"text": "hello"},
        )


def test_case_rejects_non_packet_result() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        create_model_boundary_evaluation_case(
            case_ref="case-1",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            packet_result={"not": "a result"},  # type: ignore[arg-type]
            candidate_output={"text": "hello"},
        )


def test_case_rejects_non_mapping_candidate_output() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        create_model_boundary_evaluation_case(
            case_ref="case-1",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            packet_result=_make_packet_result(),
            candidate_output=["not", "a", "mapping"],  # type: ignore[arg-type]
        )


def test_case_rejects_callable_candidate_output_values() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        create_model_boundary_evaluation_case(
            case_ref="case-1",
            candidate_model_ref="model-1",
            expected_output_family="narration_display",
            packet_result=_make_packet_result(),
            candidate_output={"handler": lambda: None},  # type: ignore[dict-item]
        )


# ---------------------------------------------------------------------------
# ModelBoundaryEvaluationResult construction and normalization
# ---------------------------------------------------------------------------

def test_result_is_frozen() -> None:
    """ModelBoundaryEvaluationResult instances are immutable."""
    result = ModelBoundaryEvaluationResult(
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
    with pytest.raises(FrozenInstanceError):
        result.status = "failed"  # type: ignore[misc]


def test_result_normalizes_sorted_tuples() -> None:
    """violation codes, forbidden hits, and warning refs are sorted tuples."""
    result = ModelBoundaryEvaluationResult(
        case_ref="case-1",
        candidate_model_ref="model-1",
        packet_kind="single_event_narration",
        expected_output_family="narration_display",
        status="failed",
        passed=False,
        violation_codes=["candidate_output_empty", "forbidden_authority_field_present"],
        forbidden_field_hits=["state_delta", "apply_delta"],
        packet_warning_refs=["warn-b", "warn-a"],
    )

    assert result.violation_codes == (
        "candidate_output_empty",
        "forbidden_authority_field_present",
    )
    assert result.forbidden_field_hits == ("apply_delta", "state_delta")
    assert result.packet_warning_refs == ("warn-a", "warn-b")


def test_result_rejects_unknown_status() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        ModelBoundaryEvaluationResult(
            case_ref="case-1",
            candidate_model_ref="model-1",
            packet_kind="single_event_narration",
            expected_output_family="narration_display",
            status="unknown",
            passed=False,
            violation_codes=(),
            forbidden_field_hits=(),
            packet_warning_refs=(),
        )


def test_result_rejects_non_bool_passed() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        ModelBoundaryEvaluationResult(
            case_ref="case-1",
            candidate_model_ref="model-1",
            packet_kind="single_event_narration",
            expected_output_family="narration_display",
            status="failed",
            passed="no",  # type: ignore[arg-type]
            violation_codes=(),
            forbidden_field_hits=(),
            packet_warning_refs=(),
        )


def test_result_rejects_unknown_violation_code() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        ModelBoundaryEvaluationResult(
            case_ref="case-1",
            candidate_model_ref="model-1",
            packet_kind="single_event_narration",
            expected_output_family="narration_display",
            status="failed",
            passed=False,
            violation_codes=("not_a_real_code",),
            forbidden_field_hits=(),
            packet_warning_refs=(),
        )


# ---------------------------------------------------------------------------
# Factory and evaluator behavior
# ---------------------------------------------------------------------------

def test_factory_creates_valid_case() -> None:
    case = create_model_boundary_evaluation_case(
        case_ref="case-factory",
        candidate_model_ref="model-factory",
        expected_output_family="visible_summary",
        packet_result=_make_packet_result(),
        candidate_output={"summary": "safe"},
        evaluator_notes=["factory note"],
        metadata={"source": "test"},
    )
    assert case.case_ref == "case-factory"
    assert case.candidate_model_ref == "model-factory"
    assert case.expected_output_family == "visible_summary"
    assert isinstance(case.packet_result, ContextPacketCompilerResult)
    assert isinstance(case.candidate_output, MappingProxyType)
    assert case.evaluator_notes == ("factory note",)
    assert isinstance(case.metadata, MappingProxyType)


def test_evaluator_rejects_non_case_input() -> None:
    with pytest.raises(ModelBoundaryEvaluationError):
        evaluate_model_boundary_case("not a case")  # type: ignore[arg-type]


def test_evaluator_passes_safe_candidate_output() -> None:
    case = _make_case({
        "output_family": "narration_display",
        "visible_text": "The visible scene remains unchanged.",
        "uncertainty_flags": [],
    })
    result = evaluate_model_boundary_case(case)

    assert result.status == "passed"
    assert result.passed is True
    assert result.violation_codes == ()
    assert result.forbidden_field_hits == ()
    assert result.packet_warning_refs == ()


def test_evaluator_flags_empty_candidate_output_as_needs_review() -> None:
    case = _make_case({})
    result = evaluate_model_boundary_case(case)

    assert result.status == "needs_review"
    assert result.passed is False
    assert result.violation_codes == ("candidate_output_empty",)


def test_evaluator_flags_forbidden_authority_fields_as_failed() -> None:
    case = _make_case({
        "state_delta": {"hp": -5},
        "mutation": True,
        "visible_text": "safe",
    })
    result = evaluate_model_boundary_case(case)

    assert result.status == "failed"
    assert result.passed is False
    assert "forbidden_authority_field_present" in result.violation_codes
    assert "state_mutation_claim_present" in result.violation_codes
    assert result.forbidden_field_hits == ("mutation", "state_delta")


def test_evaluator_flags_hidden_information_keys_as_failed() -> None:
    case = _make_case({"hidden_fact": "the butler did it"})
    result = evaluate_model_boundary_case(case)

    assert result.status == "failed"
    assert "hidden_information_claim_present" in result.violation_codes
    assert "forbidden_authority_field_present" in result.violation_codes


def test_evaluator_flags_state_mutation_keys_as_failed() -> None:
    case = _make_case({"apply_delta": {"inventory": []}})
    result = evaluate_model_boundary_case(case)

    assert result.status == "failed"
    assert "state_mutation_claim_present" in result.violation_codes
    assert "forbidden_authority_field_present" in result.violation_codes


def test_evaluator_flags_event_commit_keys_as_failed() -> None:
    case = _make_case({"commit_event": "evt-2"})
    result = evaluate_model_boundary_case(case)

    assert result.status == "failed"
    assert "event_commit_claim_present" in result.violation_codes
    assert "forbidden_authority_field_present" in result.violation_codes


def test_evaluator_flags_random_result_keys_as_failed() -> None:
    case = _make_case({"dice_result": 17})
    result = evaluate_model_boundary_case(case)

    assert result.status == "failed"
    assert "random_result_claim_present" in result.violation_codes
    assert "forbidden_authority_field_present" in result.violation_codes


def test_evaluator_flags_durable_truth_keys_as_failed() -> None:
    case = _make_case({"canon_fact": "earth is round"})
    result = evaluate_model_boundary_case(case)

    assert result.status == "failed"
    assert "durable_truth_claim_present" in result.violation_codes
    assert "forbidden_authority_field_present" in result.violation_codes


def test_evaluator_flags_packet_warnings_as_needs_review_when_alone() -> None:
    case = _make_case(
        {"visible_text": "safe"},
        warnings=("audit_warning",),
    )
    result = evaluate_model_boundary_case(case)

    assert result.status == "needs_review"
    assert result.passed is False
    assert result.violation_codes == ("packet_warning_present",)
    assert result.packet_warning_refs == ("audit_warning",)


def test_evaluator_chooses_failed_when_warnings_and_hard_violations_present() -> None:
    case = _make_case(
        {"state_delta": {"hp": -5}},
        warnings=("audit_warning",),
    )
    result = evaluate_model_boundary_case(case)

    assert result.status == "failed"
    assert result.passed is False
    assert "state_mutation_claim_present" in result.violation_codes
    assert "forbidden_authority_field_present" in result.violation_codes
    assert "packet_warning_present" in result.violation_codes
    assert result.packet_warning_refs == ("audit_warning",)


def test_evaluator_does_not_mutate_case_or_candidate_output() -> None:
    candidate: dict[str, Any] = {"visible_text": "safe"}
    case = _make_case(candidate)
    original_candidate_id = id(case.candidate_output)

    result = evaluate_model_boundary_case(case)

    assert id(case.candidate_output) == original_candidate_id
    assert case.candidate_output["visible_text"] == "safe"
    assert candidate == {"visible_text": "safe"}
    assert result.case_ref == case.case_ref


# ---------------------------------------------------------------------------
# Source scan — confirm no forbidden runtime authority dependencies
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
