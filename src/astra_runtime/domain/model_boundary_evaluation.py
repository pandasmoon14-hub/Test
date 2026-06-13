"""PR-7 model boundary evaluation skeleton — static structural evaluator.

This module provides a non-executing harness for evaluating captured model
outputs against the packet/result boundary established in PR-6. It performs
only structural boundary checks on candidate output mappings and does not call
models, generate narration, parse intent, read runtime state, or commit events.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
)


MODEL_BOUNDARY_OUTPUT_FAMILIES = frozenset({
    "intent_proposal",
    "narration_display",
    "visible_summary",
    "clarification",
    "evaluation_note",
})

MODEL_BOUNDARY_STATUS_VALUES = frozenset({
    "passed",
    "failed",
    "needs_review",
})

MODEL_BOUNDARY_VIOLATION_CODES = frozenset({
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


_FORBIDDEN_AUTHORITY_OUTPUT_FIELDS = frozenset({
    "commit_event",
    "committed_event",
    "event_commit",
    "state_delta",
    "state_mutation",
    "apply_delta",
    "mutation",
    "hidden_fact",
    "hidden_facts",
    "hidden_fact_refs",
    "hidden_information",
    "secret_refs",
    "unrevealed_clues",
    "rng_result",
    "roll_result",
    "dice_result",
    "oracle_result",
    "durable_truth",
    "canon_fact",
    "sourcebook_fact",
})

_HIDDEN_INFORMATION_KEYS = frozenset({
    "hidden_fact",
    "hidden_facts",
    "hidden_fact_refs",
    "hidden_information",
    "secret_refs",
    "unrevealed_clues",
})

_STATE_MUTATION_KEYS = frozenset({
    "state_delta",
    "state_mutation",
    "apply_delta",
    "mutation",
})

_EVENT_COMMIT_KEYS = frozenset({
    "commit_event",
    "committed_event",
    "event_commit",
})

_RANDOM_RESULT_KEYS = frozenset({
    "rng_result",
    "roll_result",
    "dice_result",
    "oracle_result",
})

_DURABLE_TRUTH_KEYS = frozenset({
    "durable_truth",
    "canon_fact",
    "sourcebook_fact",
})

_HARD_VIOLATION_CODES = frozenset({
    "forbidden_authority_field_present",
    "hidden_information_claim_present",
    "state_mutation_claim_present",
    "event_commit_claim_present",
    "random_result_claim_present",
    "durable_truth_claim_present",
})


class ModelBoundaryEvaluationError(ValueError):
    """Raised for malformed evaluation case/result construction.

    Not used for normal evaluation failures; those are reported through
    ModelBoundaryEvaluationResult objects.
    """


def _normalize_string_tuple(
    values: Sequence[str] | None,
    name: str,
    error_cls: type[Exception],
) -> tuple[str, ...]:
    """Normalize a sequence of strings into a tuple, rejecting empty strings."""
    if values is None:
        return ()
    if isinstance(values, str):
        raise error_cls(f"{name} must not be a bare string")
    if not isinstance(values, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[str] = []
    for i, item in enumerate(values):
        if not isinstance(item, str) or not item.strip():
            raise error_cls(f"{name}[{i}] must be a non-empty string")
        result.append(item)
    return tuple(result)


def _safe_frozen_mapping(
    value: Mapping[str, Any] | None,
    error_cls: type[Exception],
) -> Mapping[str, Any]:
    """Deep-copy and freeze a mapping, rejecting callable values."""
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise error_cls("value must be a mapping")
    copied: dict[str, Any] = {}
    for key, item in value.items():
        if callable(item):
            raise error_cls("mapping values must not be callable")
        copied[key] = copy.deepcopy(item)
    return MappingProxyType(copied)


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryEvaluationCase:
    """Immutable model-boundary evaluation case.

    Carries a prebuilt context-packet compiler result and a candidate model
    output mapping to be evaluated against structural boundary rules. Does not
    invoke models or execute runtime behavior.
    """

    case_ref: str
    candidate_model_ref: str
    expected_output_family: str
    packet_result: ContextPacketCompilerResult
    candidate_output: Mapping[str, Any]
    evaluator_notes: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryEvaluationError

        # Validate identifiers
        if not isinstance(self.case_ref, str) or not self.case_ref.strip():
            raise error_cls("case_ref must be a non-empty string")
        if (
            not isinstance(self.candidate_model_ref, str)
            or not self.candidate_model_ref.strip()
        ):
            raise error_cls("candidate_model_ref must be a non-empty string")

        # Validate expected output family
        if (
            not isinstance(self.expected_output_family, str)
            or not self.expected_output_family.strip()
        ):
            raise error_cls("expected_output_family must be a non-empty string")
        if self.expected_output_family not in MODEL_BOUNDARY_OUTPUT_FAMILIES:
            raise error_cls(
                f"unknown expected_output_family: {self.expected_output_family!r}; "
                f"expected one of {sorted(MODEL_BOUNDARY_OUTPUT_FAMILIES)}"
            )

        # Validate packet result type
        if not isinstance(self.packet_result, ContextPacketCompilerResult):
            raise error_cls(
                "packet_result must be a ContextPacketCompilerResult instance"
            )

        # Validate and freeze candidate output mapping
        if not isinstance(self.candidate_output, Mapping):
            raise error_cls("candidate_output must be a mapping")
        safe_candidate_output: dict[str, Any] = {}
        for key, value in self.candidate_output.items():
            if callable(value):
                raise error_cls("candidate_output values must not be callable")
            safe_candidate_output[key] = copy.deepcopy(value)

        # Normalize notes and metadata
        safe_notes = _normalize_string_tuple(
            self.evaluator_notes, "evaluator_notes", error_cls
        )
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        # Use object.__setattr__ because the dataclass is frozen
        object.__setattr__(
            self, "candidate_output", MappingProxyType(safe_candidate_output)
        )
        object.__setattr__(self, "evaluator_notes", safe_notes)
        object.__setattr__(self, "metadata", safe_metadata)


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryEvaluationResult:
    """Immutable result of evaluating a model boundary case.

    Reports deterministic structural violations without executing model
    behavior or mutating runtime state.
    """

    case_ref: str
    candidate_model_ref: str
    packet_kind: str
    expected_output_family: str
    status: str
    passed: bool
    violation_codes: tuple[str, ...]
    forbidden_field_hits: tuple[str, ...]
    packet_warning_refs: tuple[str, ...]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryEvaluationError

        # Validate identifiers
        if not isinstance(self.case_ref, str) or not self.case_ref.strip():
            raise error_cls("case_ref must be a non-empty string")
        if (
            not isinstance(self.candidate_model_ref, str)
            or not self.candidate_model_ref.strip()
        ):
            raise error_cls("candidate_model_ref must be a non-empty string")

        # Validate packet_kind
        if not isinstance(self.packet_kind, str) or not self.packet_kind.strip():
            raise error_cls("packet_kind must be a non-empty string")

        # Validate expected output family
        if (
            not isinstance(self.expected_output_family, str)
            or not self.expected_output_family.strip()
        ):
            raise error_cls("expected_output_family must be a non-empty string")
        if self.expected_output_family not in MODEL_BOUNDARY_OUTPUT_FAMILIES:
            raise error_cls(
                f"unknown expected_output_family: {self.expected_output_family!r}; "
                f"expected one of {sorted(MODEL_BOUNDARY_OUTPUT_FAMILIES)}"
            )

        # Validate status
        if not isinstance(self.status, str) or not self.status.strip():
            raise error_cls("status must be a non-empty string")
        if self.status not in MODEL_BOUNDARY_STATUS_VALUES:
            raise error_cls(
                f"unknown status: {self.status!r}; "
                f"expected one of {sorted(MODEL_BOUNDARY_STATUS_VALUES)}"
            )

        # Validate passed flag
        if not isinstance(self.passed, bool):
            raise error_cls("passed must be a bool")

        # Normalize violation codes: sorted tuple of known codes
        safe_violations = _normalize_string_tuple(
            self.violation_codes, "violation_codes", error_cls
        )
        safe_violations = tuple(sorted(safe_violations))
        for code in safe_violations:
            if code not in MODEL_BOUNDARY_VIOLATION_CODES:
                raise error_cls(f"unknown violation_code: {code!r}")

        # Normalize other string tuples
        safe_forbidden_hits = _normalize_string_tuple(
            self.forbidden_field_hits, "forbidden_field_hits", error_cls
        )
        safe_forbidden_hits = tuple(sorted(safe_forbidden_hits))

        safe_warning_refs = _normalize_string_tuple(
            self.packet_warning_refs, "packet_warning_refs", error_cls
        )
        safe_warning_refs = tuple(sorted(safe_warning_refs))

        # Deep-copy and freeze metadata
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        # Use object.__setattr__ because the dataclass is frozen
        object.__setattr__(self, "violation_codes", safe_violations)
        object.__setattr__(self, "forbidden_field_hits", safe_forbidden_hits)
        object.__setattr__(self, "packet_warning_refs", safe_warning_refs)
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_evaluation_case(
    *,
    case_ref: str,
    candidate_model_ref: str,
    expected_output_family: str,
    packet_result: ContextPacketCompilerResult,
    candidate_output: Mapping[str, Any],
    evaluator_notes: Sequence[str] = (),
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryEvaluationCase:
    """Construct and validate a ModelBoundaryEvaluationCase.

    Raises ModelBoundaryEvaluationError on invalid input.
    """
    return ModelBoundaryEvaluationCase(
        case_ref=case_ref,
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_result=packet_result,
        candidate_output=candidate_output,
        evaluator_notes=evaluator_notes,
        metadata=metadata if metadata is not None else {},
    )


def evaluate_model_boundary_case(
    case: ModelBoundaryEvaluationCase,
) -> ModelBoundaryEvaluationResult:
    """Evaluate a model boundary case structurally.

    Inspects only the keys of ``case.candidate_output`` and the warnings on
    ``case.packet_result``. Does not parse prose, call models, execute gameplay,
    or mutate inputs.
    """
    if not isinstance(case, ModelBoundaryEvaluationCase):
        raise ModelBoundaryEvaluationError(
            "case must be a ModelBoundaryEvaluationCase instance"
        )

    violations: set[str] = set()
    forbidden_hits: set[str] = set()
    packet_warning_refs: list[str] = []

    candidate_keys = set(case.candidate_output.keys())

    if len(candidate_keys) == 0:
        violations.add("candidate_output_empty")

    authority_hits = candidate_keys & _FORBIDDEN_AUTHORITY_OUTPUT_FIELDS
    if authority_hits:
        violations.add("forbidden_authority_field_present")
        forbidden_hits.update(authority_hits)

    if candidate_keys & _HIDDEN_INFORMATION_KEYS:
        violations.add("hidden_information_claim_present")

    if candidate_keys & _STATE_MUTATION_KEYS:
        violations.add("state_mutation_claim_present")

    if candidate_keys & _EVENT_COMMIT_KEYS:
        violations.add("event_commit_claim_present")

    if candidate_keys & _RANDOM_RESULT_KEYS:
        violations.add("random_result_claim_present")

    if candidate_keys & _DURABLE_TRUTH_KEYS:
        violations.add("durable_truth_claim_present")

    if case.packet_result.warnings:
        violations.add("packet_warning_present")
        packet_warning_refs.extend(case.packet_result.warnings)

    passed = len(violations) == 0

    if passed:
        status = "passed"
    elif violations & _HARD_VIOLATION_CODES:
        status = "failed"
    else:
        status = "needs_review"

    return ModelBoundaryEvaluationResult(
        case_ref=case.case_ref,
        candidate_model_ref=case.candidate_model_ref,
        packet_kind=case.packet_result.packet_kind,
        expected_output_family=case.expected_output_family,
        status=status,
        passed=passed,
        violation_codes=tuple(sorted(violations)),
        forbidden_field_hits=tuple(sorted(forbidden_hits)),
        packet_warning_refs=tuple(sorted(packet_warning_refs)),
    )


class ModelBoundaryEvaluationSuiteError(ModelBoundaryEvaluationError):
    """Raised for malformed suite/suite-result construction.

    Not used for normal evaluation failures; those are reported through
    ModelBoundaryEvaluationSuiteResult objects.
    """


def _validate_non_empty_string(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> str:
    """Validate that value is a non-empty string."""
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string")
    return value


def _validate_non_negative_int_not_bool(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> int:
    """Validate that value is a non-negative integer and not a bool."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise error_cls(f"{name} must be a non-negative integer")
    if value < 0:
        raise error_cls(f"{name} must be non-negative")
    return value


def _normalize_case_sequence(
    cases: Any,
    error_cls: type[Exception],
) -> tuple[ModelBoundaryEvaluationCase, ...]:
    """Normalize a sequence of evaluation cases into a tuple.

    Rejects bare strings, empty sequences, non-case values, and duplicate
    case_ref values.
    """
    if isinstance(cases, str):
        raise error_cls("cases must not be a bare string")
    if not isinstance(cases, Sequence):
        raise error_cls("cases must be a sequence")
    if len(cases) == 0:
        raise error_cls("cases must contain at least one case")

    normalized: list[ModelBoundaryEvaluationCase] = []
    seen_refs: set[str] = set()
    for i, item in enumerate(cases):
        if not isinstance(item, ModelBoundaryEvaluationCase):
            raise error_cls(f"cases[{i}] must be a ModelBoundaryEvaluationCase")
        if item.case_ref in seen_refs:
            raise error_cls(f"duplicate case_ref: {item.case_ref!r}")
        seen_refs.add(item.case_ref)
        normalized.append(item)
    return tuple(normalized)


def _normalize_result_sequence(
    case_results: Any,
    error_cls: type[Exception],
) -> tuple[ModelBoundaryEvaluationResult, ...]:
    """Normalize a sequence of evaluation results into a tuple."""
    if isinstance(case_results, str):
        raise error_cls("case_results must not be a bare string")
    if not isinstance(case_results, Sequence):
        raise error_cls("case_results must be a sequence")

    normalized: list[ModelBoundaryEvaluationResult] = []
    for i, item in enumerate(case_results):
        if not isinstance(item, ModelBoundaryEvaluationResult):
            raise error_cls(
                f"case_results[{i}] must be a ModelBoundaryEvaluationResult"
            )
        normalized.append(item)
    return tuple(normalized)


def _validate_status_counts(
    status_counts: Any,
    error_cls: type[Exception],
) -> Mapping[str, int]:
    """Validate and freeze status counts for all known status values."""
    if not isinstance(status_counts, Mapping):
        raise error_cls("status_counts must be a mapping")

    copied: dict[str, int] = {}
    for status in MODEL_BOUNDARY_STATUS_VALUES:
        count = status_counts.get(status, 0)
        _validate_non_negative_int_not_bool(count, f"status_counts[{status!r}]", error_cls)
        copied[status] = count

    unknown_keys = set(status_counts.keys()) - MODEL_BOUNDARY_STATUS_VALUES
    if unknown_keys:
        raise error_cls(
            f"unknown status keys: {sorted(unknown_keys)}; "
            f"expected one of {sorted(MODEL_BOUNDARY_STATUS_VALUES)}"
        )

    return MappingProxyType(copied)


def _validate_violation_counts(
    violation_counts: Any,
    error_cls: type[Exception],
) -> Mapping[str, int]:
    """Validate and freeze violation counts for known violation codes."""
    if not isinstance(violation_counts, Mapping):
        raise error_cls("violation_counts must be a mapping")

    copied: dict[str, int] = {}
    for code, count in violation_counts.items():
        if code not in MODEL_BOUNDARY_VIOLATION_CODES:
            raise error_cls(
                f"unknown violation_code: {code!r}; "
                f"expected one of {sorted(MODEL_BOUNDARY_VIOLATION_CODES)}"
            )
        _validate_non_negative_int_not_bool(
            count, f"violation_counts[{code!r}]", error_cls
        )
        copied[code] = count

    return MappingProxyType(copied)


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryEvaluationSuite:
    """Immutable suite of model-boundary evaluation cases.

    Carries an ordered collection of prebuilt evaluation cases without
    invoking models or executing runtime behavior.
    """

    suite_ref: str
    suite_label: str
    cases: tuple[ModelBoundaryEvaluationCase, ...]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryEvaluationSuiteError

        _validate_non_empty_string(self.suite_ref, "suite_ref", error_cls)
        _validate_non_empty_string(self.suite_label, "suite_label", error_cls)
        safe_cases = _normalize_case_sequence(self.cases, error_cls)
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "cases", safe_cases)
        object.__setattr__(self, "metadata", safe_metadata)


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryEvaluationSuiteResult:
    """Immutable aggregate result of evaluating a model boundary suite.

    Reports deterministic structural findings for the whole suite without
    executing model behavior or mutating runtime state.
    """

    suite_ref: str
    suite_label: str
    total_cases: int
    passed_cases: int
    failed_cases: int
    needs_review_cases: int
    all_passed: bool
    case_results: tuple[ModelBoundaryEvaluationResult, ...]
    status_counts: Mapping[str, int]
    violation_counts: Mapping[str, int]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryEvaluationSuiteError

        _validate_non_empty_string(self.suite_ref, "suite_ref", error_cls)
        _validate_non_empty_string(self.suite_label, "suite_label", error_cls)
        total_cases = _validate_non_negative_int_not_bool(
            self.total_cases, "total_cases", error_cls
        )
        passed_cases = _validate_non_negative_int_not_bool(
            self.passed_cases, "passed_cases", error_cls
        )
        failed_cases = _validate_non_negative_int_not_bool(
            self.failed_cases, "failed_cases", error_cls
        )
        needs_review_cases = _validate_non_negative_int_not_bool(
            self.needs_review_cases, "needs_review_cases", error_cls
        )

        if not isinstance(self.all_passed, bool):
            raise error_cls("all_passed must be a bool")

        safe_case_results = _normalize_result_sequence(
            self.case_results, error_cls
        )
        if total_cases != len(safe_case_results):
            raise error_cls(
                f"total_cases ({total_cases}) must equal len(case_results) "
                f"({len(safe_case_results)})"
            )
        if passed_cases + failed_cases + needs_review_cases != total_cases:
            raise error_cls(
                "passed_cases + failed_cases + needs_review_cases must equal total_cases"
            )

        safe_status_counts = _validate_status_counts(
            self.status_counts, error_cls
        )
        safe_violation_counts = _validate_violation_counts(
            self.violation_counts, error_cls
        )
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "case_results", safe_case_results)
        object.__setattr__(self, "status_counts", safe_status_counts)
        object.__setattr__(self, "violation_counts", safe_violation_counts)
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_evaluation_suite(
    *,
    suite_ref: str,
    suite_label: str,
    cases: Sequence[ModelBoundaryEvaluationCase],
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryEvaluationSuite:
    """Construct and validate a ModelBoundaryEvaluationSuite.

    Raises ModelBoundaryEvaluationSuiteError on invalid input.
    """
    return ModelBoundaryEvaluationSuite(
        suite_ref=suite_ref,
        suite_label=suite_label,
        cases=cases,
        metadata=metadata if metadata is not None else {},
    )


def evaluate_model_boundary_suite(
    suite: ModelBoundaryEvaluationSuite,
) -> ModelBoundaryEvaluationSuiteResult:
    """Evaluate every case in a model boundary suite.

    Calls ``evaluate_model_boundary_case`` for each case in order and produces
    an immutable aggregate result. Does not call models, read runtime state,
    aggregate packets beyond the per-case audit warnings already present, or
    mutate the input suite.
    """
    if not isinstance(suite, ModelBoundaryEvaluationSuite):
        raise ModelBoundaryEvaluationSuiteError(
            "suite must be a ModelBoundaryEvaluationSuite instance"
        )

    case_results: list[ModelBoundaryEvaluationResult] = []
    status_counts: dict[str, int] = {
        status: 0 for status in MODEL_BOUNDARY_STATUS_VALUES
    }
    violation_counts: dict[str, int] = {}

    for case in suite.cases:
        result = evaluate_model_boundary_case(case)
        case_results.append(result)
        status_counts[result.status] += 1
        for code in result.violation_codes:
            violation_counts[code] = violation_counts.get(code, 0) + 1

    passed_cases = status_counts["passed"]
    failed_cases = status_counts["failed"]
    needs_review_cases = status_counts["needs_review"]
    all_passed = passed_cases == len(case_results) and len(case_results) > 0

    # Deterministic ordering of violation counts by code key.
    sorted_violation_counts = {
        code: violation_counts[code] for code in sorted(violation_counts)
    }

    return ModelBoundaryEvaluationSuiteResult(
        suite_ref=suite.suite_ref,
        suite_label=suite.suite_label,
        total_cases=len(case_results),
        passed_cases=passed_cases,
        failed_cases=failed_cases,
        needs_review_cases=needs_review_cases,
        all_passed=all_passed,
        case_results=case_results,
        status_counts=status_counts,
        violation_counts=sorted_violation_counts,
        metadata=suite.metadata,
    )
