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
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
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


# ---------------------------------------------------------------------------
# PR-7 Slice 3 — Expected Boundary Assertion Layer
# ---------------------------------------------------------------------------

_CASE_ASSERTION_MISMATCH_CODES = frozenset({
    "status_mismatch",
    "passed_flag_mismatch",
    "violation_codes_mismatch",
    "forbidden_field_hits_mismatch",
    "packet_warning_refs_mismatch",
})

_SUITE_ASSERTION_MISMATCH_CODES = frozenset({
    "total_cases_mismatch",
    "passed_cases_mismatch",
    "failed_cases_mismatch",
    "needs_review_cases_mismatch",
    "all_passed_mismatch",
    "status_counts_mismatch",
    "violation_counts_mismatch",
})


class ModelBoundaryAssertionError(ModelBoundaryEvaluationError):
    """Raised for malformed expectation/assertion construction.

    Not used for normal assertion failures; those are reported through
    immutable assertion result objects.
    """


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryExpectedCaseOutcome:
    """Immutable expected outcome for a single model-boundary case.

    Declares what a captured or constructed ``ModelBoundaryEvaluationResult``
    should look like. Does not call models or execute runtime behavior.
    """

    expectation_ref: str
    expected_status: str
    expected_passed: bool
    expected_violation_codes: tuple[str, ...] = field(default_factory=tuple)
    expected_forbidden_field_hits: tuple[str, ...] = field(default_factory=tuple)
    expected_packet_warning_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryAssertionError

        _validate_non_empty_string(
            self.expectation_ref, "expectation_ref", error_cls
        )

        _validate_non_empty_string(self.expected_status, "expected_status", error_cls)
        if self.expected_status not in MODEL_BOUNDARY_STATUS_VALUES:
            raise error_cls(
                f"unknown expected_status: {self.expected_status!r}; "
                f"expected one of {sorted(MODEL_BOUNDARY_STATUS_VALUES)}"
            )

        if not isinstance(self.expected_passed, bool):
            raise error_cls("expected_passed must be a bool")

        safe_violations = _normalize_string_tuple(
            self.expected_violation_codes, "expected_violation_codes", error_cls
        )
        safe_violations = tuple(sorted(safe_violations))
        for code in safe_violations:
            if code not in MODEL_BOUNDARY_VIOLATION_CODES:
                raise error_cls(f"unknown violation_code: {code!r}")

        safe_forbidden_hits = _normalize_string_tuple(
            self.expected_forbidden_field_hits,
            "expected_forbidden_field_hits",
            error_cls,
        )
        safe_forbidden_hits = tuple(sorted(safe_forbidden_hits))

        safe_warning_refs = _normalize_string_tuple(
            self.expected_packet_warning_refs,
            "expected_packet_warning_refs",
            error_cls,
        )
        safe_warning_refs = tuple(sorted(safe_warning_refs))

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "expected_violation_codes", safe_violations)
        object.__setattr__(
            self, "expected_forbidden_field_hits", safe_forbidden_hits
        )
        object.__setattr__(
            self, "expected_packet_warning_refs", safe_warning_refs
        )
        object.__setattr__(self, "metadata", safe_metadata)


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCaseAssertionResult:
    """Immutable result of asserting an expected case outcome.

    Reports deterministic comparison details without executing models or
    mutating the underlying evaluation result.
    """

    expectation_ref: str
    case_ref: str
    assertion_passed: bool
    mismatch_codes: tuple[str, ...]
    expected_status: str
    actual_status: str
    expected_passed: bool
    actual_passed: bool
    expected_violation_codes: tuple[str, ...]
    actual_violation_codes: tuple[str, ...]
    expected_forbidden_field_hits: tuple[str, ...]
    actual_forbidden_field_hits: tuple[str, ...]
    expected_packet_warning_refs: tuple[str, ...]
    actual_packet_warning_refs: tuple[str, ...]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryAssertionError

        _validate_non_empty_string(
            self.expectation_ref, "expectation_ref", error_cls
        )
        _validate_non_empty_string(self.case_ref, "case_ref", error_cls)

        if not isinstance(self.assertion_passed, bool):
            raise error_cls("assertion_passed must be a bool")

        for name, value in (
            ("expected_status", self.expected_status),
            ("actual_status", self.actual_status),
        ):
            _validate_non_empty_string(value, name, error_cls)
            if value not in MODEL_BOUNDARY_STATUS_VALUES:
                raise error_cls(
                    f"unknown {name}: {value!r}; "
                    f"expected one of {sorted(MODEL_BOUNDARY_STATUS_VALUES)}"
                )

        for name, value in (
            ("expected_passed", self.expected_passed),
            ("actual_passed", self.actual_passed),
        ):
            if not isinstance(value, bool):
                raise error_cls(f"{name} must be a bool")

        safe_mismatch_codes = _normalize_string_tuple(
            self.mismatch_codes, "mismatch_codes", error_cls
        )
        safe_mismatch_codes = tuple(sorted(safe_mismatch_codes))
        for code in safe_mismatch_codes:
            if code not in _CASE_ASSERTION_MISMATCH_CODES:
                raise error_cls(f"unknown mismatch_code: {code!r}")

        expected_violations = _normalize_string_tuple(
            self.expected_violation_codes, "expected_violation_codes", error_cls
        )
        expected_violations = tuple(sorted(expected_violations))
        for code in expected_violations:
            if code not in MODEL_BOUNDARY_VIOLATION_CODES:
                raise error_cls(f"unknown expected_violation_codes: {code!r}")

        actual_violations = _normalize_string_tuple(
            self.actual_violation_codes, "actual_violation_codes", error_cls
        )
        actual_violations = tuple(sorted(actual_violations))
        for code in actual_violations:
            if code not in MODEL_BOUNDARY_VIOLATION_CODES:
                raise error_cls(f"unknown actual_violation_codes: {code!r}")

        expected_hits = _normalize_string_tuple(
            self.expected_forbidden_field_hits,
            "expected_forbidden_field_hits",
            error_cls,
        )
        expected_hits = tuple(sorted(expected_hits))

        actual_hits = _normalize_string_tuple(
            self.actual_forbidden_field_hits,
            "actual_forbidden_field_hits",
            error_cls,
        )
        actual_hits = tuple(sorted(actual_hits))

        expected_warnings = _normalize_string_tuple(
            self.expected_packet_warning_refs,
            "expected_packet_warning_refs",
            error_cls,
        )
        expected_warnings = tuple(sorted(expected_warnings))

        actual_warnings = _normalize_string_tuple(
            self.actual_packet_warning_refs,
            "actual_packet_warning_refs",
            error_cls,
        )
        actual_warnings = tuple(sorted(actual_warnings))

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "mismatch_codes", safe_mismatch_codes)
        object.__setattr__(self, "expected_violation_codes", expected_violations)
        object.__setattr__(self, "actual_violation_codes", actual_violations)
        object.__setattr__(self, "expected_forbidden_field_hits", expected_hits)
        object.__setattr__(self, "actual_forbidden_field_hits", actual_hits)
        object.__setattr__(
            self, "expected_packet_warning_refs", expected_warnings
        )
        object.__setattr__(self, "actual_packet_warning_refs", actual_warnings)
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_expected_case_outcome(
    *,
    expectation_ref: str,
    expected_status: str,
    expected_passed: bool,
    expected_violation_codes: Sequence[str] = (),
    expected_forbidden_field_hits: Sequence[str] = (),
    expected_packet_warning_refs: Sequence[str] = (),
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryExpectedCaseOutcome:
    """Construct and validate a ModelBoundaryExpectedCaseOutcome.

    Raises ModelBoundaryAssertionError on invalid input.
    """
    return ModelBoundaryExpectedCaseOutcome(
        expectation_ref=expectation_ref,
        expected_status=expected_status,
        expected_passed=expected_passed,
        expected_violation_codes=expected_violation_codes,
        expected_forbidden_field_hits=expected_forbidden_field_hits,
        expected_packet_warning_refs=expected_packet_warning_refs,
        metadata=metadata if metadata is not None else {},
    )


def assert_model_boundary_case_result(
    *,
    expectation: ModelBoundaryExpectedCaseOutcome,
    actual_result: ModelBoundaryEvaluationResult,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCaseAssertionResult:
    """Compare an expected case outcome against an actual case result.

    Returns an immutable ``ModelBoundaryCaseAssertionResult``. Does not call
    models, execute prompts, or mutate inputs.
    """
    error_cls = ModelBoundaryAssertionError

    if not isinstance(expectation, ModelBoundaryExpectedCaseOutcome):
        raise error_cls(
            "expectation must be a ModelBoundaryExpectedCaseOutcome instance"
        )
    if not isinstance(actual_result, ModelBoundaryEvaluationResult):
        raise error_cls(
            "actual_result must be a ModelBoundaryEvaluationResult instance"
        )

    mismatches: list[str] = []
    if expectation.expected_status != actual_result.status:
        mismatches.append("status_mismatch")
    if expectation.expected_passed != actual_result.passed:
        mismatches.append("passed_flag_mismatch")
    if expectation.expected_violation_codes != actual_result.violation_codes:
        mismatches.append("violation_codes_mismatch")
    if expectation.expected_forbidden_field_hits != actual_result.forbidden_field_hits:
        mismatches.append("forbidden_field_hits_mismatch")
    if expectation.expected_packet_warning_refs != actual_result.packet_warning_refs:
        mismatches.append("packet_warning_refs_mismatch")

    safe_metadata = _safe_frozen_mapping(
        metadata if metadata is not None else {}, error_cls
    )

    return ModelBoundaryCaseAssertionResult(
        expectation_ref=expectation.expectation_ref,
        case_ref=actual_result.case_ref,
        assertion_passed=len(mismatches) == 0,
        mismatch_codes=tuple(sorted(mismatches)),
        expected_status=expectation.expected_status,
        actual_status=actual_result.status,
        expected_passed=expectation.expected_passed,
        actual_passed=actual_result.passed,
        expected_violation_codes=expectation.expected_violation_codes,
        actual_violation_codes=actual_result.violation_codes,
        expected_forbidden_field_hits=expectation.expected_forbidden_field_hits,
        actual_forbidden_field_hits=actual_result.forbidden_field_hits,
        expected_packet_warning_refs=expectation.expected_packet_warning_refs,
        actual_packet_warning_refs=actual_result.packet_warning_refs,
        metadata=safe_metadata,
    )


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryExpectedSuiteOutcome:
    """Immutable expected outcome for a model-boundary evaluation suite.

    Declares what a captured or constructed ``ModelBoundaryEvaluationSuiteResult``
    should look like. Does not call models or execute runtime behavior.
    """

    expectation_ref: str
    expected_total_cases: int
    expected_passed_cases: int
    expected_failed_cases: int
    expected_needs_review_cases: int
    expected_all_passed: bool
    expected_status_counts: Mapping[str, int]
    expected_violation_counts: Mapping[str, int] = field(
        default_factory=lambda: MappingProxyType({})
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryAssertionError

        _validate_non_empty_string(
            self.expectation_ref, "expectation_ref", error_cls
        )

        total = _validate_non_negative_int_not_bool(
            self.expected_total_cases, "expected_total_cases", error_cls
        )
        passed = _validate_non_negative_int_not_bool(
            self.expected_passed_cases, "expected_passed_cases", error_cls
        )
        failed = _validate_non_negative_int_not_bool(
            self.expected_failed_cases, "expected_failed_cases", error_cls
        )
        needs_review = _validate_non_negative_int_not_bool(
            self.expected_needs_review_cases,
            "expected_needs_review_cases",
            error_cls,
        )

        if not isinstance(self.expected_all_passed, bool):
            raise error_cls("expected_all_passed must be a bool")

        if passed + failed + needs_review != total:
            raise error_cls(
                "expected_passed_cases + expected_failed_cases + "
                "expected_needs_review_cases must equal expected_total_cases"
            )

        if not isinstance(self.expected_status_counts, Mapping):
            raise error_cls("expected_status_counts must be a mapping")
        missing_status_keys = MODEL_BOUNDARY_STATUS_VALUES - set(
            self.expected_status_counts.keys()
        )
        if missing_status_keys:
            raise error_cls(
                f"expected_status_counts missing keys: {sorted(missing_status_keys)}"
            )
        safe_status_counts = _validate_status_counts(
            self.expected_status_counts, error_cls
        )
        safe_violation_counts = _validate_violation_counts(
            self.expected_violation_counts, error_cls
        )
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "expected_status_counts", safe_status_counts)
        object.__setattr__(
            self, "expected_violation_counts", safe_violation_counts
        )
        object.__setattr__(self, "metadata", safe_metadata)


@dataclass(frozen=True, kw_only=True)
class ModelBoundarySuiteAssertionResult:
    """Immutable result of asserting an expected suite outcome.

    Reports deterministic comparison details without executing models or
    mutating the underlying suite result.
    """

    expectation_ref: str
    suite_ref: str
    assertion_passed: bool
    mismatch_codes: tuple[str, ...]
    expected_total_cases: int
    actual_total_cases: int
    expected_passed_cases: int
    actual_passed_cases: int
    expected_failed_cases: int
    actual_failed_cases: int
    expected_needs_review_cases: int
    actual_needs_review_cases: int
    expected_all_passed: bool
    actual_all_passed: bool
    expected_status_counts: Mapping[str, int]
    actual_status_counts: Mapping[str, int]
    expected_violation_counts: Mapping[str, int]
    actual_violation_counts: Mapping[str, int]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryAssertionError

        _validate_non_empty_string(
            self.expectation_ref, "expectation_ref", error_cls
        )
        _validate_non_empty_string(self.suite_ref, "suite_ref", error_cls)

        if not isinstance(self.assertion_passed, bool):
            raise error_cls("assertion_passed must be a bool")

        for name, value in (
            ("expected_total_cases", self.expected_total_cases),
            ("actual_total_cases", self.actual_total_cases),
            ("expected_passed_cases", self.expected_passed_cases),
            ("actual_passed_cases", self.actual_passed_cases),
            ("expected_failed_cases", self.expected_failed_cases),
            ("actual_failed_cases", self.actual_failed_cases),
            ("expected_needs_review_cases", self.expected_needs_review_cases),
            ("actual_needs_review_cases", self.actual_needs_review_cases),
        ):
            _validate_non_negative_int_not_bool(value, name, error_cls)

        for name, value in (
            ("expected_all_passed", self.expected_all_passed),
            ("actual_all_passed", self.actual_all_passed),
        ):
            if not isinstance(value, bool):
                raise error_cls(f"{name} must be a bool")

        safe_mismatch_codes = _normalize_string_tuple(
            self.mismatch_codes, "mismatch_codes", error_cls
        )
        safe_mismatch_codes = tuple(sorted(safe_mismatch_codes))
        for code in safe_mismatch_codes:
            if code not in _SUITE_ASSERTION_MISMATCH_CODES:
                raise error_cls(f"unknown mismatch_code: {code!r}")

        safe_expected_status_counts = _validate_status_counts(
            self.expected_status_counts, error_cls
        )
        safe_actual_status_counts = _validate_status_counts(
            self.actual_status_counts, error_cls
        )

        safe_expected_violation_counts = _validate_violation_counts(
            self.expected_violation_counts, error_cls
        )
        safe_actual_violation_counts = _validate_violation_counts(
            self.actual_violation_counts, error_cls
        )

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "mismatch_codes", safe_mismatch_codes)
        object.__setattr__(
            self, "expected_status_counts", safe_expected_status_counts
        )
        object.__setattr__(
            self, "actual_status_counts", safe_actual_status_counts
        )
        object.__setattr__(
            self, "expected_violation_counts", safe_expected_violation_counts
        )
        object.__setattr__(
            self, "actual_violation_counts", safe_actual_violation_counts
        )
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_expected_suite_outcome(
    *,
    expectation_ref: str,
    expected_total_cases: int,
    expected_passed_cases: int,
    expected_failed_cases: int,
    expected_needs_review_cases: int,
    expected_all_passed: bool,
    expected_status_counts: Mapping[str, int],
    expected_violation_counts: Mapping[str, int] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryExpectedSuiteOutcome:
    """Construct and validate a ModelBoundaryExpectedSuiteOutcome.

    Raises ModelBoundaryAssertionError on invalid input.
    """
    return ModelBoundaryExpectedSuiteOutcome(
        expectation_ref=expectation_ref,
        expected_total_cases=expected_total_cases,
        expected_passed_cases=expected_passed_cases,
        expected_failed_cases=expected_failed_cases,
        expected_needs_review_cases=expected_needs_review_cases,
        expected_all_passed=expected_all_passed,
        expected_status_counts=expected_status_counts,
        expected_violation_counts=expected_violation_counts
        if expected_violation_counts is not None
        else {},
        metadata=metadata if metadata is not None else {},
    )


def assert_model_boundary_suite_result(
    *,
    expectation: ModelBoundaryExpectedSuiteOutcome,
    actual_result: ModelBoundaryEvaluationSuiteResult,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundarySuiteAssertionResult:
    """Compare an expected suite outcome against an actual suite result.

    Returns an immutable ``ModelBoundarySuiteAssertionResult``. Does not call
    models, execute prompts, or mutate inputs.
    """
    error_cls = ModelBoundaryAssertionError

    if not isinstance(expectation, ModelBoundaryExpectedSuiteOutcome):
        raise error_cls(
            "expectation must be a ModelBoundaryExpectedSuiteOutcome instance"
        )
    if not isinstance(actual_result, ModelBoundaryEvaluationSuiteResult):
        raise error_cls(
            "actual_result must be a ModelBoundaryEvaluationSuiteResult instance"
        )

    mismatches: list[str] = []
    if expectation.expected_total_cases != actual_result.total_cases:
        mismatches.append("total_cases_mismatch")
    if expectation.expected_passed_cases != actual_result.passed_cases:
        mismatches.append("passed_cases_mismatch")
    if expectation.expected_failed_cases != actual_result.failed_cases:
        mismatches.append("failed_cases_mismatch")
    if expectation.expected_needs_review_cases != actual_result.needs_review_cases:
        mismatches.append("needs_review_cases_mismatch")
    if expectation.expected_all_passed != actual_result.all_passed:
        mismatches.append("all_passed_mismatch")
    if expectation.expected_status_counts != actual_result.status_counts:
        mismatches.append("status_counts_mismatch")
    if expectation.expected_violation_counts != actual_result.violation_counts:
        mismatches.append("violation_counts_mismatch")

    safe_metadata = _safe_frozen_mapping(
        metadata if metadata is not None else {}, error_cls
    )

    return ModelBoundarySuiteAssertionResult(
        expectation_ref=expectation.expectation_ref,
        suite_ref=actual_result.suite_ref,
        assertion_passed=len(mismatches) == 0,
        mismatch_codes=tuple(sorted(mismatches)),
        expected_total_cases=expectation.expected_total_cases,
        actual_total_cases=actual_result.total_cases,
        expected_passed_cases=expectation.expected_passed_cases,
        actual_passed_cases=actual_result.passed_cases,
        expected_failed_cases=expectation.expected_failed_cases,
        actual_failed_cases=actual_result.failed_cases,
        expected_needs_review_cases=expectation.expected_needs_review_cases,
        actual_needs_review_cases=actual_result.needs_review_cases,
        expected_all_passed=expectation.expected_all_passed,
        actual_all_passed=actual_result.all_passed,
        expected_status_counts=expectation.expected_status_counts,
        actual_status_counts=actual_result.status_counts,
        expected_violation_counts=expectation.expected_violation_counts,
        actual_violation_counts=actual_result.violation_counts,
        metadata=safe_metadata,
    )

# ---------------------------------------------------------------------------
# PR-7 Slice 4 — Captured Output Fixture Adapter
# ---------------------------------------------------------------------------


class ModelBoundaryCapturedOutputFixtureError(ModelBoundaryEvaluationError):
    """Raised for malformed captured-output fixture construction/adaptation.

    Not used for normal evaluation failures; those are reported through
    ModelBoundaryEvaluationResult objects.
    """


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedOutputFixture:
    """Immutable captured-output fixture for model-boundary evaluation.

    Carries a pre-captured model output as an explicit candidate mapping,
    together with the packet result that was supplied to the model boundary.
    The raw captured text is stored only as inert evidence and is never
    parsed or executed.
    """

    fixture_ref: str
    capture_ref: str
    candidate_model_ref: str
    expected_output_family: str
    packet_result: ContextPacketCompilerResult
    candidate_output: Mapping[str, Any]
    raw_captured_text: str | None = None
    evaluator_notes: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedOutputFixtureError

        # Validate identifiers
        if not isinstance(self.fixture_ref, str) or not self.fixture_ref.strip():
            raise error_cls("fixture_ref must be a non-empty string")
        if not isinstance(self.capture_ref, str) or not self.capture_ref.strip():
            raise error_cls("capture_ref must be a non-empty string")
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
        safe_candidate_output = _safe_frozen_mapping(
            self.candidate_output, error_cls
        )

        # Validate raw captured text is inert evidence only
        if self.raw_captured_text is not None:
            if (
                not isinstance(self.raw_captured_text, str)
                or not self.raw_captured_text.strip()
            ):
                raise error_cls(
                    "raw_captured_text must be a non-empty string when provided"
                )

        # Normalize notes and metadata
        safe_notes = _normalize_string_tuple(
            self.evaluator_notes, "evaluator_notes", error_cls
        )
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        # Use object.__setattr__ because the dataclass is frozen
        object.__setattr__(
            self, "candidate_output", safe_candidate_output
        )
        object.__setattr__(self, "evaluator_notes", safe_notes)
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_captured_output_fixture(
    *,
    fixture_ref: str,
    capture_ref: str,
    candidate_model_ref: str,
    expected_output_family: str,
    packet_result: ContextPacketCompilerResult,
    candidate_output: Mapping[str, Any],
    raw_captured_text: str | None = None,
    evaluator_notes: Sequence[str] = (),
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedOutputFixture:
    """Construct and validate a ModelBoundaryCapturedOutputFixture.

    Raises ModelBoundaryCapturedOutputFixtureError on invalid input.
    """
    return ModelBoundaryCapturedOutputFixture(
        fixture_ref=fixture_ref,
        capture_ref=capture_ref,
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_result=packet_result,
        candidate_output=candidate_output,
        raw_captured_text=raw_captured_text,
        evaluator_notes=evaluator_notes,
        metadata=metadata if metadata is not None else {},
    )


def create_model_boundary_case_from_captured_output_fixture(
    fixture: ModelBoundaryCapturedOutputFixture,
    *,
    case_ref: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryEvaluationCase:
    """Adapt a captured-output fixture into a ModelBoundaryEvaluationCase.

    Uses explicit fixture fields and caller-supplied overrides only. Does not
    call models, parse raw captured text, or evaluate the case.
    """
    error_cls = ModelBoundaryCapturedOutputFixtureError

    if not isinstance(fixture, ModelBoundaryCapturedOutputFixture):
        raise error_cls(
            "fixture must be a ModelBoundaryCapturedOutputFixture instance"
        )

    resolved_case_ref = case_ref if case_ref is not None else fixture.fixture_ref
    if not isinstance(resolved_case_ref, str) or not resolved_case_ref.strip():
        raise error_cls("case_ref must be a non-empty string")

    if metadata is not None:
        case_metadata = metadata
    else:
        case_metadata = {
            **dict(fixture.metadata),
            "fixture_ref": fixture.fixture_ref,
            "capture_ref": fixture.capture_ref,
            "has_raw_captured_text": fixture.raw_captured_text is not None,
        }

    return create_model_boundary_evaluation_case(
        case_ref=resolved_case_ref,
        candidate_model_ref=fixture.candidate_model_ref,
        expected_output_family=fixture.expected_output_family,
        packet_result=fixture.packet_result,
        candidate_output=fixture.candidate_output,
        evaluator_notes=fixture.evaluator_notes,
        metadata=case_metadata,
    )

# ---------------------------------------------------------------------------
# PR-7 Slice 5 — Captured Fixture Assertion Runner
# ---------------------------------------------------------------------------


class ModelBoundaryCapturedFixtureAssertionError(ModelBoundaryEvaluationError):
    """Raised for malformed captured-fixture assertion construction.

    Not used for normal assertion failures; those are represented in the
    returned ModelBoundaryCapturedFixtureAssertionResult object.
    """


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedFixtureAssertionResult:
    """Immutable combined result of asserting a captured-output fixture.

    Connects a captured-output fixture, its derived evaluation case, the
    static evaluation result, and the assertion against an expected outcome.
    Does not call models, execute prompts, or mutate inputs.
    """

    fixture_ref: str
    capture_ref: str
    case_ref: str
    expectation_ref: str
    candidate_model_ref: str
    expected_output_family: str
    assertion_passed: bool
    evaluation_result: ModelBoundaryEvaluationResult
    assertion_result: ModelBoundaryCaseAssertionResult
    has_raw_captured_text: bool
    evaluator_notes: tuple[str, ...] = field(default_factory=tuple)
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedFixtureAssertionError

        # Validate identifiers
        _validate_non_empty_string(self.fixture_ref, "fixture_ref", error_cls)
        _validate_non_empty_string(self.capture_ref, "capture_ref", error_cls)
        _validate_non_empty_string(self.case_ref, "case_ref", error_cls)
        _validate_non_empty_string(
            self.expectation_ref, "expectation_ref", error_cls
        )
        _validate_non_empty_string(
            self.candidate_model_ref, "candidate_model_ref", error_cls
        )

        # Validate expected output family
        _validate_non_empty_string(
            self.expected_output_family, "expected_output_family", error_cls
        )
        if self.expected_output_family not in MODEL_BOUNDARY_OUTPUT_FAMILIES:
            raise error_cls(
                f"unknown expected_output_family: {self.expected_output_family!r}; "
                f"expected one of {sorted(MODEL_BOUNDARY_OUTPUT_FAMILIES)}"
            )

        # Validate assertion_passed is bool
        if not isinstance(self.assertion_passed, bool):
            raise error_cls("assertion_passed must be a bool")

        # Validate evaluation_result type
        if not isinstance(
            self.evaluation_result, ModelBoundaryEvaluationResult
        ):
            raise error_cls(
                "evaluation_result must be a ModelBoundaryEvaluationResult instance"
            )

        # Validate assertion_result type
        if not isinstance(
            self.assertion_result, ModelBoundaryCaseAssertionResult
        ):
            raise error_cls(
                "assertion_result must be a ModelBoundaryCaseAssertionResult instance"
            )

        # Validate cross-field consistency
        if self.assertion_passed != self.assertion_result.assertion_passed:
            raise error_cls(
                "assertion_passed must equal assertion_result.assertion_passed"
            )
        if self.case_ref != self.evaluation_result.case_ref:
            raise error_cls(
                "case_ref must equal evaluation_result.case_ref"
            )
        if self.expectation_ref != self.assertion_result.expectation_ref:
            raise error_cls(
                "expectation_ref must equal assertion_result.expectation_ref"
            )
        if self.candidate_model_ref != self.evaluation_result.candidate_model_ref:
            raise error_cls(
                "candidate_model_ref must equal evaluation_result.candidate_model_ref"
            )
        if (
            self.expected_output_family
            != self.evaluation_result.expected_output_family
        ):
            raise error_cls(
                "expected_output_family must equal "
                "evaluation_result.expected_output_family"
            )

        # Validate has_raw_captured_text is bool
        if not isinstance(self.has_raw_captured_text, bool):
            raise error_cls("has_raw_captured_text must be a bool")

        # Normalize notes and metadata
        safe_notes = _normalize_string_tuple(
            self.evaluator_notes, "evaluator_notes", error_cls
        )
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        # Use object.__setattr__ because the dataclass is frozen
        object.__setattr__(self, "evaluator_notes", safe_notes)
        object.__setattr__(self, "metadata", safe_metadata)


def assert_model_boundary_captured_output_fixture(
    *,
    fixture: ModelBoundaryCapturedOutputFixture,
    expectation: ModelBoundaryExpectedCaseOutcome,
    case_ref: str | None = None,
    case_metadata: Mapping[str, Any] | None = None,
    assertion_metadata: Mapping[str, Any] | None = None,
    result_metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionResult:
    """Assert a captured-output fixture against an expected case outcome.

    Converts the fixture into a ``ModelBoundaryEvaluationCase``, evaluates it
    statically, and asserts the actual result against ``expectation``. Returns
    an immutable combined result. Does not call models, parse raw captured text,
    or execute runtime behavior.
    """
    error_cls = ModelBoundaryCapturedFixtureAssertionError

    if not isinstance(fixture, ModelBoundaryCapturedOutputFixture):
        raise error_cls(
            "fixture must be a ModelBoundaryCapturedOutputFixture instance"
        )
    if not isinstance(expectation, ModelBoundaryExpectedCaseOutcome):
        raise error_cls(
            "expectation must be a ModelBoundaryExpectedCaseOutcome instance"
        )

    if case_ref is not None and (
        not isinstance(case_ref, str) or not case_ref.strip()
    ):
        raise error_cls("case_ref must be a non-empty string when provided")

    # Derive the evaluation case from the fixture without mutating inputs.
    case = create_model_boundary_case_from_captured_output_fixture(
        fixture,
        case_ref=case_ref,
        metadata=case_metadata,
    )

    # Static evaluation only.
    evaluation_result = evaluate_model_boundary_case(case)

    # Assert against the expected outcome.
    assertion_result = assert_model_boundary_case_result(
        expectation=expectation,
        actual_result=evaluation_result,
        metadata=assertion_metadata,
    )

    has_raw_captured_text = fixture.raw_captured_text is not None

    if result_metadata is None:
        result_metadata = {
            **dict(fixture.metadata),
            "fixture_ref": fixture.fixture_ref,
            "capture_ref": fixture.capture_ref,
            "case_ref": case.case_ref,
            "expectation_ref": expectation.expectation_ref,
            "has_raw_captured_text": has_raw_captured_text,
        }

    return ModelBoundaryCapturedFixtureAssertionResult(
        fixture_ref=fixture.fixture_ref,
        capture_ref=fixture.capture_ref,
        case_ref=case.case_ref,
        expectation_ref=expectation.expectation_ref,
        candidate_model_ref=fixture.candidate_model_ref,
        expected_output_family=fixture.expected_output_family,
        assertion_passed=assertion_result.assertion_passed,
        evaluation_result=evaluation_result,
        assertion_result=assertion_result,
        has_raw_captured_text=has_raw_captured_text,
        evaluator_notes=fixture.evaluator_notes,
        metadata=result_metadata,
    )

# ---------------------------------------------------------------------------
# PR-7 Slice 6 — Captured Fixture Assertion Suite Runner
# ---------------------------------------------------------------------------


class ModelBoundaryCapturedFixtureAssertionSuiteError(ModelBoundaryEvaluationError):
    """Raised for malformed captured-fixture assertion suite construction.

    Not used for normal assertion failures; those are represented in returned
    assertion result objects.
    """


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedFixtureAssertionSpec:
    """Immutable specification for one captured-fixture assertion in a suite.

    Binds a captured-output fixture and its expected outcome so that a suite
    runner can execute them in deterministic order without calling models or
    mutating inputs.
    """

    spec_ref: str
    fixture: ModelBoundaryCapturedOutputFixture
    expectation: ModelBoundaryExpectedCaseOutcome
    case_ref: str | None = None
    case_metadata: Mapping[str, Any] | None = None
    assertion_metadata: Mapping[str, Any] | None = None
    result_metadata: Mapping[str, Any] | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedFixtureAssertionSuiteError

        _validate_non_empty_string(self.spec_ref, "spec_ref", error_cls)

        if not isinstance(self.fixture, ModelBoundaryCapturedOutputFixture):
            raise error_cls(
                "fixture must be a ModelBoundaryCapturedOutputFixture instance"
            )
        if not isinstance(self.expectation, ModelBoundaryExpectedCaseOutcome):
            raise error_cls(
                "expectation must be a ModelBoundaryExpectedCaseOutcome instance"
            )

        if self.case_ref is not None and (
            not isinstance(self.case_ref, str) or not self.case_ref.strip()
        ):
            raise error_cls("case_ref must be a non-empty string when provided")

        if self.case_metadata is not None:
            safe_case_metadata = _safe_frozen_mapping(
                self.case_metadata, error_cls
            )
            object.__setattr__(self, "case_metadata", safe_case_metadata)

        if self.assertion_metadata is not None:
            safe_assertion_metadata = _safe_frozen_mapping(
                self.assertion_metadata, error_cls
            )
            object.__setattr__(
                self, "assertion_metadata", safe_assertion_metadata
            )

        if self.result_metadata is not None:
            safe_result_metadata = _safe_frozen_mapping(
                self.result_metadata, error_cls
            )
            object.__setattr__(self, "result_metadata", safe_result_metadata)

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_captured_fixture_assertion_spec(
    *,
    spec_ref: str,
    fixture: ModelBoundaryCapturedOutputFixture,
    expectation: ModelBoundaryExpectedCaseOutcome,
    case_ref: str | None = None,
    case_metadata: Mapping[str, Any] | None = None,
    assertion_metadata: Mapping[str, Any] | None = None,
    result_metadata: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionSpec:
    """Construct and validate a ModelBoundaryCapturedFixtureAssertionSpec.

    Raises ModelBoundaryCapturedFixtureAssertionSuiteError on invalid input.
    """
    return ModelBoundaryCapturedFixtureAssertionSpec(
        spec_ref=spec_ref,
        fixture=fixture,
        expectation=expectation,
        case_ref=case_ref,
        case_metadata=case_metadata,
        assertion_metadata=assertion_metadata,
        result_metadata=result_metadata,
        metadata=metadata if metadata is not None else {},
    )


def _normalize_fixture_assertion_spec_sequence(
    specs: Any,
    error_cls: type[Exception],
) -> tuple[ModelBoundaryCapturedFixtureAssertionSpec, ...]:
    """Normalize a sequence of fixture assertion specs into a tuple.

    Rejects bare strings/bytes, empty sequences, non-spec values, and duplicate
    spec_ref values. Preserves caller order.
    """
    if isinstance(specs, (str, bytes)):
        raise error_cls("specs must not be a bare string or bytes")
    if not isinstance(specs, Sequence):
        raise error_cls("specs must be a sequence")
    if len(specs) == 0:
        raise error_cls("specs must contain at least one spec")

    normalized: list[ModelBoundaryCapturedFixtureAssertionSpec] = []
    seen_refs: set[str] = set()
    for i, item in enumerate(specs):
        if not isinstance(item, ModelBoundaryCapturedFixtureAssertionSpec):
            raise error_cls(
                f"specs[{i}] must be a ModelBoundaryCapturedFixtureAssertionSpec"
            )
        if item.spec_ref in seen_refs:
            raise error_cls(f"duplicate spec_ref: {item.spec_ref!r}")
        seen_refs.add(item.spec_ref)
        normalized.append(item)
    return tuple(normalized)


def _normalize_fixture_assertion_result_sequence(
    spec_results: Any,
    error_cls: type[Exception],
) -> tuple[ModelBoundaryCapturedFixtureAssertionResult, ...]:
    """Normalize a sequence of fixture assertion results into a tuple."""
    if isinstance(spec_results, (str, bytes)):
        raise error_cls("spec_results must not be a bare string or bytes")
    if not isinstance(spec_results, Sequence):
        raise error_cls("spec_results must be a sequence")

    normalized: list[ModelBoundaryCapturedFixtureAssertionResult] = []
    for i, item in enumerate(spec_results):
        if not isinstance(item, ModelBoundaryCapturedFixtureAssertionResult):
            raise error_cls(
                f"spec_results[{i}] must be a "
                "ModelBoundaryCapturedFixtureAssertionResult"
            )
        normalized.append(item)
    return tuple(normalized)


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedFixtureAssertionSuite:
    """Immutable suite of captured-fixture assertion specs.

    Carries an ordered collection of prebuilt fixture assertion specs without
    invoking models or executing runtime behavior.
    """

    suite_ref: str
    suite_label: str
    specs: tuple[ModelBoundaryCapturedFixtureAssertionSpec, ...]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedFixtureAssertionSuiteError

        _validate_non_empty_string(self.suite_ref, "suite_ref", error_cls)
        _validate_non_empty_string(self.suite_label, "suite_label", error_cls)
        safe_specs = _normalize_fixture_assertion_spec_sequence(
            self.specs, error_cls
        )
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "specs", safe_specs)
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_captured_fixture_assertion_suite(
    *,
    suite_ref: str,
    suite_label: str,
    specs: Sequence[ModelBoundaryCapturedFixtureAssertionSpec],
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionSuite:
    """Construct and validate a ModelBoundaryCapturedFixtureAssertionSuite.

    Raises ModelBoundaryCapturedFixtureAssertionSuiteError on invalid input.
    """
    return ModelBoundaryCapturedFixtureAssertionSuite(
        suite_ref=suite_ref,
        suite_label=suite_label,
        specs=specs,
        metadata=metadata if metadata is not None else {},
    )


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedFixtureAssertionSuiteResult:
    """Immutable aggregate result of running a captured-fixture assertion suite.

    Reports deterministic structural findings for the whole suite without
    executing model behavior or mutating runtime state.
    """

    suite_ref: str
    suite_label: str
    total_specs: int
    passed_specs: int
    failed_specs: int
    all_passed: bool
    spec_results: tuple[ModelBoundaryCapturedFixtureAssertionResult, ...]
    status_counts: Mapping[str, int]
    violation_counts: Mapping[str, int]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedFixtureAssertionSuiteError

        _validate_non_empty_string(self.suite_ref, "suite_ref", error_cls)
        _validate_non_empty_string(self.suite_label, "suite_label", error_cls)
        total_specs = _validate_non_negative_int_not_bool(
            self.total_specs, "total_specs", error_cls
        )
        passed_specs = _validate_non_negative_int_not_bool(
            self.passed_specs, "passed_specs", error_cls
        )
        failed_specs = _validate_non_negative_int_not_bool(
            self.failed_specs, "failed_specs", error_cls
        )

        if not isinstance(self.all_passed, bool):
            raise error_cls("all_passed must be a bool")

        safe_spec_results = _normalize_fixture_assertion_result_sequence(
            self.spec_results, error_cls
        )
        if total_specs != len(safe_spec_results):
            raise error_cls(
                f"total_specs ({total_specs}) must equal len(spec_results) "
                f"({len(safe_spec_results)})"
            )
        if passed_specs + failed_specs != total_specs:
            raise error_cls(
                "passed_specs + failed_specs must equal total_specs"
            )
        if self.all_passed != (failed_specs == 0):
            raise error_cls(
                "all_passed must equal (failed_specs == 0)"
            )

        if not isinstance(self.status_counts, Mapping):
            raise error_cls("status_counts must be a mapping")
        missing_status_keys = MODEL_BOUNDARY_STATUS_VALUES - set(
            self.status_counts.keys()
        )
        if missing_status_keys:
            raise error_cls(
                f"status_counts missing keys: {sorted(missing_status_keys)}"
            )

        safe_status_counts = _validate_status_counts(
            self.status_counts, error_cls
        )
        safe_violation_counts = _validate_violation_counts(
            self.violation_counts, error_cls
        )

        # Deterministic ordering of status and violation counts by key.
        sorted_status_counts = {
            status: safe_status_counts[status]
            for status in sorted(safe_status_counts)
        }
        sorted_violation_counts = {
            code: safe_violation_counts[code]
            for code in sorted(safe_violation_counts)
        }

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "spec_results", safe_spec_results)
        object.__setattr__(
            self, "status_counts", MappingProxyType(sorted_status_counts)
        )
        object.__setattr__(
            self,
            "violation_counts",
            MappingProxyType(sorted_violation_counts),
        )
        object.__setattr__(self, "metadata", safe_metadata)


def assert_model_boundary_captured_fixture_assertion_suite(
    suite: ModelBoundaryCapturedFixtureAssertionSuite,
    *,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionSuiteResult:
    """Run every captured-fixture assertion spec in a suite.

    Calls ``assert_model_boundary_captured_output_fixture`` for each spec in
    order and produces an immutable aggregate result. Does not call models,
    read runtime state, parse raw captured text, or mutate the input suite.
    """
    error_cls = ModelBoundaryCapturedFixtureAssertionSuiteError

    if not isinstance(suite, ModelBoundaryCapturedFixtureAssertionSuite):
        raise error_cls(
            "suite must be a ModelBoundaryCapturedFixtureAssertionSuite instance"
        )

    spec_results: list[ModelBoundaryCapturedFixtureAssertionResult] = []
    status_counts: dict[str, int] = {
        status: 0 for status in MODEL_BOUNDARY_STATUS_VALUES
    }
    violation_counts: dict[str, int] = {}

    for spec in suite.specs:
        result = assert_model_boundary_captured_output_fixture(
            fixture=spec.fixture,
            expectation=spec.expectation,
            case_ref=spec.case_ref,
            case_metadata=spec.case_metadata,
            assertion_metadata=spec.assertion_metadata,
            result_metadata=spec.result_metadata,
        )
        spec_results.append(result)
        status_counts[result.evaluation_result.status] += 1
        for code in result.evaluation_result.violation_codes:
            violation_counts[code] = violation_counts.get(code, 0) + 1

    passed_specs = sum(1 for result in spec_results if result.assertion_passed is True)
    failed_specs = sum(1 for result in spec_results if result.assertion_passed is False)
    all_passed = failed_specs == 0

    sorted_violation_counts = {
        code: violation_counts[code] for code in sorted(violation_counts)
    }

    if metadata is None:
        metadata = {
            **dict(suite.metadata),
            "suite_ref": suite.suite_ref,
            "suite_label": suite.suite_label,
            "total_specs": len(spec_results),
            "all_passed": all_passed,
        }

    return ModelBoundaryCapturedFixtureAssertionSuiteResult(
        suite_ref=suite.suite_ref,
        suite_label=suite.suite_label,
        total_specs=len(spec_results),
        passed_specs=passed_specs,
        failed_specs=failed_specs,
        all_passed=all_passed,
        spec_results=spec_results,
        status_counts=status_counts,
        violation_counts=sorted_violation_counts,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# PR-7 Slice 7 — Captured Fixture Assertion Report Snapshot
# ---------------------------------------------------------------------------


class ModelBoundaryCapturedFixtureAssertionReportError(ModelBoundaryEvaluationError):
    """Raised for malformed report snapshot construction/serialization.

    Not used for normal report generation; those are represented in returned
    ModelBoundaryCapturedFixtureAssertionReportSnapshot objects.
    """


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedFixtureAssertionReportSnapshot:
    """Immutable deterministic snapshot of a captured-fixture assertion report.

    Summarizes an already-built ``ModelBoundaryCapturedFixtureAssertionSuiteResult``
    into stable, compact, structured data. Does not call models, parse prose,
    read runtime state, mutate inputs, or write files.
    """

    report_ref: str
    suite_ref: str
    suite_label: str
    total_specs: int
    passed_specs: int
    failed_specs: int
    all_passed: bool
    status_counts: Mapping[str, int]
    violation_counts: Mapping[str, int]
    spec_refs: tuple[str, ...]
    case_refs: tuple[str, ...]
    expectation_refs: tuple[str, ...]
    failed_spec_refs: tuple[str, ...] = field(default_factory=tuple)
    failed_case_refs: tuple[str, ...] = field(default_factory=tuple)
    packet_warning_case_refs: tuple[str, ...] = field(default_factory=tuple)
    source_suite_result: ModelBoundaryCapturedFixtureAssertionSuiteResult
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedFixtureAssertionReportError

        _validate_non_empty_string(self.report_ref, "report_ref", error_cls)
        _validate_non_empty_string(self.suite_ref, "suite_ref", error_cls)
        _validate_non_empty_string(self.suite_label, "suite_label", error_cls)

        total_specs = _validate_non_negative_int_not_bool(
            self.total_specs, "total_specs", error_cls
        )
        passed_specs = _validate_non_negative_int_not_bool(
            self.passed_specs, "passed_specs", error_cls
        )
        failed_specs = _validate_non_negative_int_not_bool(
            self.failed_specs, "failed_specs", error_cls
        )

        if not isinstance(self.all_passed, bool):
            raise error_cls("all_passed must be a bool")

        if passed_specs + failed_specs != total_specs:
            raise error_cls(
                "passed_specs + failed_specs must equal total_specs"
            )
        if self.all_passed != (failed_specs == 0):
            raise error_cls("all_passed must equal (failed_specs == 0)")

        if not isinstance(self.status_counts, Mapping):
            raise error_cls("status_counts must be a mapping")
        missing_status_keys = MODEL_BOUNDARY_STATUS_VALUES - set(
            self.status_counts.keys()
        )
        if missing_status_keys:
            raise error_cls(
                f"status_counts missing keys: {sorted(missing_status_keys)}"
            )

        safe_status_counts = _validate_status_counts(
            self.status_counts, error_cls
        )
        safe_violation_counts = _validate_violation_counts(
            self.violation_counts, error_cls
        )

        safe_spec_refs = _normalize_string_tuple(
            self.spec_refs, "spec_refs", error_cls
        )
        safe_case_refs = _normalize_string_tuple(
            self.case_refs, "case_refs", error_cls
        )
        safe_expectation_refs = _normalize_string_tuple(
            self.expectation_refs, "expectation_refs", error_cls
        )
        safe_failed_spec_refs = _normalize_string_tuple(
            self.failed_spec_refs, "failed_spec_refs", error_cls
        )
        safe_failed_case_refs = _normalize_string_tuple(
            self.failed_case_refs, "failed_case_refs", error_cls
        )
        safe_packet_warning_case_refs = _normalize_string_tuple(
            self.packet_warning_case_refs, "packet_warning_case_refs", error_cls
        )

        if len(safe_spec_refs) != total_specs:
            raise error_cls(
                f"len(spec_refs) ({len(safe_spec_refs)}) must equal total_specs "
                f"({total_specs})"
            )
        if len(safe_case_refs) != total_specs:
            raise error_cls(
                f"len(case_refs) ({len(safe_case_refs)}) must equal total_specs "
                f"({total_specs})"
            )
        if len(safe_expectation_refs) != total_specs:
            raise error_cls(
                f"len(expectation_refs) ({len(safe_expectation_refs)}) must equal "
                f"total_specs ({total_specs})"
            )

        if not isinstance(
            self.source_suite_result, ModelBoundaryCapturedFixtureAssertionSuiteResult
        ):
            raise error_cls(
                "source_suite_result must be a "
                "ModelBoundaryCapturedFixtureAssertionSuiteResult instance"
            )

        if self.suite_ref != self.source_suite_result.suite_ref:
            raise error_cls(
                f"suite_ref ({self.suite_ref!r}) must equal "
                f"source_suite_result.suite_ref "
                f"({self.source_suite_result.suite_ref!r})"
            )
        if self.suite_label != self.source_suite_result.suite_label:
            raise error_cls(
                f"suite_label ({self.suite_label!r}) must equal "
                f"source_suite_result.suite_label "
                f"({self.source_suite_result.suite_label!r})"
            )
        if total_specs != self.source_suite_result.total_specs:
            raise error_cls(
                f"total_specs ({total_specs}) must equal "
                f"source_suite_result.total_specs "
                f"({self.source_suite_result.total_specs})"
            )
        if passed_specs != self.source_suite_result.passed_specs:
            raise error_cls(
                f"passed_specs ({passed_specs}) must equal "
                f"source_suite_result.passed_specs "
                f"({self.source_suite_result.passed_specs})"
            )
        if failed_specs != self.source_suite_result.failed_specs:
            raise error_cls(
                f"failed_specs ({failed_specs}) must equal "
                f"source_suite_result.failed_specs "
                f"({self.source_suite_result.failed_specs})"
            )
        if self.all_passed != self.source_suite_result.all_passed:
            raise error_cls(
                f"all_passed ({self.all_passed}) must equal "
                f"source_suite_result.all_passed "
                f"({self.source_suite_result.all_passed})"
            )

        sorted_status_counts = {
            status: safe_status_counts[status]
            for status in sorted(safe_status_counts)
        }
        sorted_violation_counts = {
            code: safe_violation_counts[code]
            for code in sorted(safe_violation_counts)
        }

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(
            self, "status_counts", MappingProxyType(sorted_status_counts)
        )
        object.__setattr__(
            self, "violation_counts", MappingProxyType(sorted_violation_counts)
        )
        object.__setattr__(self, "spec_refs", safe_spec_refs)
        object.__setattr__(self, "case_refs", safe_case_refs)
        object.__setattr__(self, "expectation_refs", safe_expectation_refs)
        object.__setattr__(self, "failed_spec_refs", safe_failed_spec_refs)
        object.__setattr__(self, "failed_case_refs", safe_failed_case_refs)
        object.__setattr__(
            self, "packet_warning_case_refs", safe_packet_warning_case_refs
        )
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_captured_fixture_assertion_report_snapshot(
    *,
    report_ref: str,
    suite_result: ModelBoundaryCapturedFixtureAssertionSuiteResult,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionReportSnapshot:
    """Build a deterministic report snapshot from a suite result.

    Derives compact summary fields from ``suite_result`` without calling models,
    parsing raw captured text, or reading runtime state.
    """
    error_cls = ModelBoundaryCapturedFixtureAssertionReportError

    _validate_non_empty_string(report_ref, "report_ref", error_cls)

    if not isinstance(
        suite_result, ModelBoundaryCapturedFixtureAssertionSuiteResult
    ):
        raise error_cls(
            "suite_result must be a "
            "ModelBoundaryCapturedFixtureAssertionSuiteResult instance"
        )

    spec_refs: list[str] = []
    case_refs: list[str] = []
    expectation_refs: list[str] = []
    failed_spec_refs: list[str] = []
    failed_case_refs: list[str] = []
    packet_warning_case_refs: list[str] = []

    for result in suite_result.spec_results:
        derived_spec_ref = result.case_ref
        if isinstance(result.metadata, Mapping):
            metadata_spec_ref = result.metadata.get("spec_ref")
            if isinstance(metadata_spec_ref, str) and metadata_spec_ref.strip():
                derived_spec_ref = metadata_spec_ref

        spec_refs.append(derived_spec_ref)
        case_refs.append(result.case_ref)
        expectation_refs.append(result.expectation_ref)

        if result.assertion_passed is False:
            failed_spec_refs.append(derived_spec_ref)
            failed_case_refs.append(result.case_ref)

        if result.evaluation_result.packet_warning_refs:
            packet_warning_case_refs.append(result.case_ref)

    if metadata is None:
        metadata = {
            **dict(suite_result.metadata),
            "report_ref": report_ref,
            "suite_ref": suite_result.suite_ref,
            "total_specs": suite_result.total_specs,
            "all_passed": suite_result.all_passed,
        }

    return ModelBoundaryCapturedFixtureAssertionReportSnapshot(
        report_ref=report_ref,
        suite_ref=suite_result.suite_ref,
        suite_label=suite_result.suite_label,
        total_specs=suite_result.total_specs,
        passed_specs=suite_result.passed_specs,
        failed_specs=suite_result.failed_specs,
        all_passed=suite_result.all_passed,
        status_counts=suite_result.status_counts,
        violation_counts=suite_result.violation_counts,
        spec_refs=tuple(spec_refs),
        case_refs=tuple(case_refs),
        expectation_refs=tuple(expectation_refs),
        failed_spec_refs=tuple(failed_spec_refs),
        failed_case_refs=tuple(failed_case_refs),
        packet_warning_case_refs=tuple(packet_warning_case_refs),
        source_suite_result=suite_result,
        metadata=metadata,
    )


def serialize_model_boundary_captured_fixture_assertion_report_snapshot(
    snapshot: ModelBoundaryCapturedFixtureAssertionReportSnapshot,
) -> dict[str, Any]:
    """Serialize a report snapshot into a deterministic plain dict.

    Returns stable, compact summary data. Does not include the full
    ``source_suite_result`` or any raw captured text.
    """
    error_cls = ModelBoundaryCapturedFixtureAssertionReportError

    if not isinstance(
        snapshot, ModelBoundaryCapturedFixtureAssertionReportSnapshot
    ):
        raise error_cls(
            "snapshot must be a "
            "ModelBoundaryCapturedFixtureAssertionReportSnapshot instance"
        )

    return {
        "report_ref": snapshot.report_ref,
        "suite_ref": snapshot.suite_ref,
        "suite_label": snapshot.suite_label,
        "total_specs": snapshot.total_specs,
        "passed_specs": snapshot.passed_specs,
        "failed_specs": snapshot.failed_specs,
        "all_passed": snapshot.all_passed,
        "status_counts": {
            status: snapshot.status_counts[status]
            for status in sorted(snapshot.status_counts)
        },
        "violation_counts": {
            code: snapshot.violation_counts[code]
            for code in sorted(snapshot.violation_counts)
        },
        "spec_refs": list(snapshot.spec_refs),
        "case_refs": list(snapshot.case_refs),
        "expectation_refs": list(snapshot.expectation_refs),
        "failed_spec_refs": list(snapshot.failed_spec_refs),
        "failed_case_refs": list(snapshot.failed_case_refs),
        "packet_warning_case_refs": list(snapshot.packet_warning_case_refs),
        "metadata": dict(snapshot.metadata),
    }


# ---------------------------------------------------------------------------
# PR-7 Slice 8 — Captured Fixture Evaluation Run Snapshot
# ---------------------------------------------------------------------------


def _normalize_report_snapshot_sequence(
    snapshots: Any,
    error_cls: type[Exception],
) -> tuple[ModelBoundaryCapturedFixtureAssertionReportSnapshot, ...]:
    """Normalize a sequence of report snapshots into a tuple.

    Rejects bare strings/bytes, empty sequences, non-report-snapshot values, and
    duplicate report_ref values. Preserves caller order.
    """
    if isinstance(snapshots, (str, bytes)):
        raise error_cls("report_snapshots must not be a bare string or bytes")
    if not isinstance(snapshots, Sequence):
        raise error_cls("report_snapshots must be a sequence")
    if len(snapshots) == 0:
        raise error_cls("report_snapshots must contain at least one report snapshot")

    normalized: list[ModelBoundaryCapturedFixtureAssertionReportSnapshot] = []
    seen_refs: set[str] = set()
    for i, item in enumerate(snapshots):
        if not isinstance(item, ModelBoundaryCapturedFixtureAssertionReportSnapshot):
            raise error_cls(
                f"report_snapshots[{i}] must be a "
                "ModelBoundaryCapturedFixtureAssertionReportSnapshot"
            )
        if item.report_ref in seen_refs:
            raise error_cls(f"duplicate report_ref: {item.report_ref!r}")
        seen_refs.add(item.report_ref)
        normalized.append(item)
    return tuple(normalized)


class ModelBoundaryCapturedFixtureEvaluationRunError(ModelBoundaryEvaluationError):
    """Raised for malformed run snapshot construction/serialization.

    Not used for normal run generation; those are represented in returned
    ModelBoundaryCapturedFixtureEvaluationRunSnapshot objects.
    """


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedFixtureEvaluationRunSnapshot:
    """Immutable deterministic snapshot of a captured-fixture evaluation run.

    Summarizes one or more already-built
    ``ModelBoundaryCapturedFixtureAssertionReportSnapshot`` objects into stable,
    compact, structured data. Does not call models, parse prose, read runtime
    state, mutate inputs, or write files.
    """

    run_ref: str
    run_label: str
    total_reports: int
    total_specs: int
    passed_specs: int
    failed_specs: int
    all_passed: bool
    report_refs: tuple[str, ...]
    suite_refs: tuple[str, ...]
    suite_labels: tuple[str, ...]
    failed_report_refs: tuple[str, ...] = field(default_factory=tuple)
    failed_suite_refs: tuple[str, ...] = field(default_factory=tuple)
    packet_warning_report_refs: tuple[str, ...] = field(default_factory=tuple)
    status_counts: Mapping[str, int]
    violation_counts: Mapping[str, int]
    report_snapshots: tuple[ModelBoundaryCapturedFixtureAssertionReportSnapshot, ...]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedFixtureEvaluationRunError

        _validate_non_empty_string(self.run_ref, "run_ref", error_cls)
        _validate_non_empty_string(self.run_label, "run_label", error_cls)

        total_reports = _validate_non_negative_int_not_bool(
            self.total_reports, "total_reports", error_cls
        )
        total_specs = _validate_non_negative_int_not_bool(
            self.total_specs, "total_specs", error_cls
        )
        passed_specs = _validate_non_negative_int_not_bool(
            self.passed_specs, "passed_specs", error_cls
        )
        failed_specs = _validate_non_negative_int_not_bool(
            self.failed_specs, "failed_specs", error_cls
        )

        if not isinstance(self.all_passed, bool):
            raise error_cls("all_passed must be a bool")

        if passed_specs + failed_specs != total_specs:
            raise error_cls(
                "passed_specs + failed_specs must equal total_specs"
            )
        if self.all_passed != (failed_specs == 0):
            raise error_cls("all_passed must equal (failed_specs == 0)")

        safe_report_snapshots = _normalize_report_snapshot_sequence(
            self.report_snapshots, error_cls
        )
        if total_reports != len(safe_report_snapshots):
            raise error_cls(
                f"total_reports ({total_reports}) must equal "
                f"len(report_snapshots) ({len(safe_report_snapshots)})"
            )

        safe_report_refs = _normalize_string_tuple(
            self.report_refs, "report_refs", error_cls
        )
        safe_suite_refs = _normalize_string_tuple(
            self.suite_refs, "suite_refs", error_cls
        )
        safe_suite_labels = _normalize_string_tuple(
            self.suite_labels, "suite_labels", error_cls
        )

        if len(safe_report_refs) != total_reports:
            raise error_cls(
                f"len(report_refs) ({len(safe_report_refs)}) must equal "
                f"total_reports ({total_reports})"
            )
        if len(safe_suite_refs) != total_reports:
            raise error_cls(
                f"len(suite_refs) ({len(safe_suite_refs)}) must equal "
                f"total_reports ({total_reports})"
            )
        if len(safe_suite_labels) != total_reports:
            raise error_cls(
                f"len(suite_labels) ({len(safe_suite_labels)}) must equal "
                f"total_reports ({total_reports})"
            )

        safe_failed_report_refs = _normalize_string_tuple(
            self.failed_report_refs, "failed_report_refs", error_cls
        )
        safe_failed_suite_refs = _normalize_string_tuple(
            self.failed_suite_refs, "failed_suite_refs", error_cls
        )
        safe_packet_warning_report_refs = _normalize_string_tuple(
            self.packet_warning_report_refs,
            "packet_warning_report_refs",
            error_cls,
        )

        if not isinstance(self.status_counts, Mapping):
            raise error_cls("status_counts must be a mapping")
        missing_status_keys = MODEL_BOUNDARY_STATUS_VALUES - set(
            self.status_counts.keys()
        )
        if missing_status_keys:
            raise error_cls(
                f"status_counts missing keys: {sorted(missing_status_keys)}"
            )

        safe_status_counts = _validate_status_counts(
            self.status_counts, error_cls
        )
        safe_violation_counts = _validate_violation_counts(
            self.violation_counts, error_cls
        )

        # Cross-check aggregate counts against report snapshots.
        derived_total_specs = sum(
            report.total_specs for report in safe_report_snapshots
        )
        if total_specs != derived_total_specs:
            raise error_cls(
                f"total_specs ({total_specs}) must equal sum of report "
                f"total_specs ({derived_total_specs})"
            )
        derived_passed_specs = sum(
            report.passed_specs for report in safe_report_snapshots
        )
        if passed_specs != derived_passed_specs:
            raise error_cls(
                f"passed_specs ({passed_specs}) must equal sum of report "
                f"passed_specs ({derived_passed_specs})"
            )
        derived_failed_specs = sum(
            report.failed_specs for report in safe_report_snapshots
        )
        if failed_specs != derived_failed_specs:
            raise error_cls(
                f"failed_specs ({failed_specs}) must equal sum of report "
                f"failed_specs ({derived_failed_specs})"
            )
        derived_all_passed = all(
            report.all_passed for report in safe_report_snapshots
        )
        if self.all_passed != derived_all_passed:
            raise error_cls(
                f"all_passed ({self.all_passed}) must equal all report "
                f"all_passed ({derived_all_passed})"
            )
        derived_report_refs = tuple(
            report.report_ref for report in safe_report_snapshots
        )
        if safe_report_refs != derived_report_refs:
            raise error_cls(
                f"report_refs ({list(safe_report_refs)}) must equal report "
                f"report_refs ({list(derived_report_refs)})"
            )
        derived_suite_refs = tuple(
            report.suite_ref for report in safe_report_snapshots
        )
        if safe_suite_refs != derived_suite_refs:
            raise error_cls(
                f"suite_refs ({list(safe_suite_refs)}) must equal report "
                f"suite_refs ({list(derived_suite_refs)})"
            )
        derived_suite_labels = tuple(
            report.suite_label for report in safe_report_snapshots
        )
        if safe_suite_labels != derived_suite_labels:
            raise error_cls(
                f"suite_labels ({list(safe_suite_labels)}) must equal report "
                f"suite_labels ({list(derived_suite_labels)})"
            )

        sorted_status_counts = {
            status: safe_status_counts[status]
            for status in sorted(safe_status_counts)
        }
        sorted_violation_counts = {
            code: safe_violation_counts[code]
            for code in sorted(safe_violation_counts)
        }

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "report_snapshots", safe_report_snapshots)
        object.__setattr__(self, "report_refs", safe_report_refs)
        object.__setattr__(self, "suite_refs", safe_suite_refs)
        object.__setattr__(self, "suite_labels", safe_suite_labels)
        object.__setattr__(
            self, "failed_report_refs", safe_failed_report_refs
        )
        object.__setattr__(
            self, "failed_suite_refs", safe_failed_suite_refs
        )
        object.__setattr__(
            self,
            "packet_warning_report_refs",
            safe_packet_warning_report_refs,
        )
        object.__setattr__(
            self, "status_counts", MappingProxyType(sorted_status_counts)
        )
        object.__setattr__(
            self,
            "violation_counts",
            MappingProxyType(sorted_violation_counts),
        )
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_captured_fixture_evaluation_run_snapshot(
    *,
    run_ref: str,
    run_label: str,
    report_snapshots: Sequence[
        ModelBoundaryCapturedFixtureAssertionReportSnapshot
    ],
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureEvaluationRunSnapshot:
    """Build a deterministic run snapshot from already-built report snapshots.

    Derives compact summary fields from ``report_snapshots`` without calling
    models, parsing raw captured text, reading runtime state, or writing files.
    """
    error_cls = ModelBoundaryCapturedFixtureEvaluationRunError

    _validate_non_empty_string(run_ref, "run_ref", error_cls)
    _validate_non_empty_string(run_label, "run_label", error_cls)

    safe_report_snapshots = _normalize_report_snapshot_sequence(
        report_snapshots, error_cls
    )

    total_reports = len(safe_report_snapshots)
    total_specs = sum(
        report.total_specs for report in safe_report_snapshots
    )
    passed_specs = sum(
        report.passed_specs for report in safe_report_snapshots
    )
    failed_specs = sum(
        report.failed_specs for report in safe_report_snapshots
    )
    all_passed = all(
        report.all_passed for report in safe_report_snapshots
    )

    report_refs = tuple(
        report.report_ref for report in safe_report_snapshots
    )
    suite_refs = tuple(
        report.suite_ref for report in safe_report_snapshots
    )
    suite_labels = tuple(
        report.suite_label for report in safe_report_snapshots
    )

    failed_report_refs = tuple(
        report.report_ref
        for report in safe_report_snapshots
        if report.all_passed is False
    )
    failed_suite_refs = tuple(
        report.suite_ref
        for report in safe_report_snapshots
        if report.all_passed is False
    )
    packet_warning_report_refs = tuple(
        report.report_ref
        for report in safe_report_snapshots
        if report.packet_warning_case_refs
    )

    status_counts: dict[str, int] = {
        status: 0 for status in MODEL_BOUNDARY_STATUS_VALUES
    }
    for report in safe_report_snapshots:
        for status in MODEL_BOUNDARY_STATUS_VALUES:
            status_counts[status] += report.status_counts[status]

    violation_counts: dict[str, int] = {}
    for report in safe_report_snapshots:
        for code, count in report.violation_counts.items():
            violation_counts[code] = violation_counts.get(code, 0) + count

    if metadata is None:
        metadata = {
            "run_ref": run_ref,
            "run_label": run_label,
            "total_reports": total_reports,
            "total_specs": total_specs,
            "all_passed": all_passed,
        }

    return ModelBoundaryCapturedFixtureEvaluationRunSnapshot(
        run_ref=run_ref,
        run_label=run_label,
        total_reports=total_reports,
        total_specs=total_specs,
        passed_specs=passed_specs,
        failed_specs=failed_specs,
        all_passed=all_passed,
        report_refs=report_refs,
        suite_refs=suite_refs,
        suite_labels=suite_labels,
        failed_report_refs=failed_report_refs,
        failed_suite_refs=failed_suite_refs,
        packet_warning_report_refs=packet_warning_report_refs,
        status_counts=status_counts,
        violation_counts=violation_counts,
        report_snapshots=safe_report_snapshots,
        metadata=metadata,
    )


def serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
    snapshot: ModelBoundaryCapturedFixtureEvaluationRunSnapshot,
) -> dict[str, Any]:
    """Serialize a run snapshot into a deterministic plain dict.

    Returns stable, compact summary data. Does not include the nested
    ``report_snapshots`` or any raw captured text.
    """
    error_cls = ModelBoundaryCapturedFixtureEvaluationRunError

    if not isinstance(
        snapshot, ModelBoundaryCapturedFixtureEvaluationRunSnapshot
    ):
        raise error_cls(
            "snapshot must be a "
            "ModelBoundaryCapturedFixtureEvaluationRunSnapshot instance"
        )

    return {
        "run_ref": snapshot.run_ref,
        "run_label": snapshot.run_label,
        "total_reports": snapshot.total_reports,
        "total_specs": snapshot.total_specs,
        "passed_specs": snapshot.passed_specs,
        "failed_specs": snapshot.failed_specs,
        "all_passed": snapshot.all_passed,
        "report_refs": list(snapshot.report_refs),
        "suite_refs": list(snapshot.suite_refs),
        "suite_labels": list(snapshot.suite_labels),
        "failed_report_refs": list(snapshot.failed_report_refs),
        "failed_suite_refs": list(snapshot.failed_suite_refs),
        "packet_warning_report_refs": list(
            snapshot.packet_warning_report_refs
        ),
        "status_counts": {
            status: snapshot.status_counts[status]
            for status in sorted(snapshot.status_counts)
        },
        "violation_counts": {
            code: snapshot.violation_counts[code]
            for code in sorted(snapshot.violation_counts)
        },
        "metadata": dict(snapshot.metadata),
    }


# ---------------------------------------------------------------------------
# PR-7 Slice 9 — Captured Fixture Evaluation Run Orchestrator
# ---------------------------------------------------------------------------


def _normalize_captured_fixture_assertion_suite_sequence(
    suites: Any,
    error_cls: type[Exception],
) -> tuple[ModelBoundaryCapturedFixtureAssertionSuite, ...]:
    """Normalize a sequence of captured-fixture assertion suites into a tuple.

    Rejects bare strings/bytes, empty sequences, non-suite values, and duplicate
    suite_ref values. Preserves caller order.
    """
    if isinstance(suites, (str, bytes)):
        raise error_cls("suites must not be a bare string or bytes")
    if not isinstance(suites, Sequence):
        raise error_cls("suites must be a sequence")
    if len(suites) == 0:
        raise error_cls("suites must contain at least one suite")

    normalized: list[ModelBoundaryCapturedFixtureAssertionSuite] = []
    seen_refs: set[str] = set()
    for i, item in enumerate(suites):
        if not isinstance(item, ModelBoundaryCapturedFixtureAssertionSuite):
            raise error_cls(
                f"suites[{i}] must be a "
                "ModelBoundaryCapturedFixtureAssertionSuite"
            )
        if item.suite_ref in seen_refs:
            raise error_cls(f"duplicate suite_ref: {item.suite_ref!r}")
        seen_refs.add(item.suite_ref)
        normalized.append(item)
    return tuple(normalized)


class ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError(
    ModelBoundaryEvaluationError,
):
    """Raised for malformed orchestrator inputs or serialization inputs."""


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult:
    """Immutable result of running the captured-fixture evaluation orchestrator.

    Connects already-built suites, their suite results, report snapshots, and
    a run snapshot into a single deterministic result object. Does not call
    models, parse prose, read runtime state, mutate inputs, or write files.
    """

    run_ref: str
    run_label: str
    report_ref_prefix: str
    suite_refs: tuple[str, ...]
    report_refs: tuple[str, ...]
    suites: tuple[ModelBoundaryCapturedFixtureAssertionSuite, ...]
    suite_results: tuple[ModelBoundaryCapturedFixtureAssertionSuiteResult, ...]
    report_snapshots: tuple[ModelBoundaryCapturedFixtureAssertionReportSnapshot, ...]
    run_snapshot: ModelBoundaryCapturedFixtureEvaluationRunSnapshot
    serialized_run_snapshot: Mapping[str, Any]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        """Post-init validation and normalization for frozen dataclass."""
        error_cls = ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError

        _validate_non_empty_string(self.run_ref, "run_ref", error_cls)
        _validate_non_empty_string(self.run_label, "run_label", error_cls)
        _validate_non_empty_string(
            self.report_ref_prefix, "report_ref_prefix", error_cls
        )

        safe_suite_refs = _normalize_string_tuple(
            self.suite_refs, "suite_refs", error_cls
        )
        safe_report_refs = _normalize_string_tuple(
            self.report_refs, "report_refs", error_cls
        )

        safe_suites = _normalize_captured_fixture_assertion_suite_sequence(
            self.suites, error_cls
        )

        if isinstance(self.suite_results, (str, bytes)):
            raise error_cls("suite_results must not be a bare string or bytes")
        if not isinstance(self.suite_results, Sequence):
            raise error_cls("suite_results must be a sequence")
        safe_suite_results: list[ModelBoundaryCapturedFixtureAssertionSuiteResult] = []
        for i, item in enumerate(self.suite_results):
            if not isinstance(item, ModelBoundaryCapturedFixtureAssertionSuiteResult):
                raise error_cls(
                    f"suite_results[{i}] must be a "
                    "ModelBoundaryCapturedFixtureAssertionSuiteResult"
                )
            safe_suite_results.append(item)
        safe_suite_results_tuple = tuple(safe_suite_results)

        if isinstance(self.report_snapshots, (str, bytes)):
            raise error_cls("report_snapshots must not be a bare string or bytes")
        if not isinstance(self.report_snapshots, Sequence):
            raise error_cls("report_snapshots must be a sequence")
        safe_report_snapshots: list[
            ModelBoundaryCapturedFixtureAssertionReportSnapshot
        ] = []
        for i, item in enumerate(self.report_snapshots):
            if not isinstance(
                item, ModelBoundaryCapturedFixtureAssertionReportSnapshot
            ):
                raise error_cls(
                    f"report_snapshots[{i}] must be a "
                    "ModelBoundaryCapturedFixtureAssertionReportSnapshot"
                )
            safe_report_snapshots.append(item)
        safe_report_snapshots_tuple = tuple(safe_report_snapshots)

        if not isinstance(
            self.run_snapshot, ModelBoundaryCapturedFixtureEvaluationRunSnapshot
        ):
            raise error_cls(
                "run_snapshot must be a "
                "ModelBoundaryCapturedFixtureEvaluationRunSnapshot instance"
            )

        if not isinstance(self.serialized_run_snapshot, Mapping):
            raise error_cls("serialized_run_snapshot must be a mapping")

        # Cross-field consistency checks.
        derived_suite_refs = tuple(s.suite_ref for s in safe_suites)
        if safe_suite_refs != derived_suite_refs:
            raise error_cls(
                "suite_refs must equal tuple(suite.suite_ref for suite in suites)"
            )

        result_suite_refs = tuple(r.suite_ref for r in safe_suite_results)
        if safe_suite_refs != result_suite_refs:
            raise error_cls(
                "suite_refs must equal tuple(result.suite_ref for result in suite_results)"
            )

        derived_report_refs = tuple(
            r.report_ref for r in safe_report_snapshots
        )
        if safe_report_refs != derived_report_refs:
            raise error_cls(
                "report_refs must equal tuple(report.report_ref for report in report_snapshots)"
            )

        report_suite_refs = tuple(
            r.suite_ref for r in safe_report_snapshots
        )
        if report_suite_refs != safe_suite_refs:
            raise error_cls(
                "tuple(report.suite_ref for report in report_snapshots) must equal suite_refs"
            )

        if self.run_snapshot.report_refs != safe_report_refs:
            raise error_cls(
                "run_snapshot.report_refs must equal report_refs"
            )
        if self.run_snapshot.suite_refs != safe_suite_refs:
            raise error_cls(
                "run_snapshot.suite_refs must equal suite_refs"
            )

        if self.serialized_run_snapshot.get("run_ref") != self.run_ref:
            raise error_cls(
                'serialized_run_snapshot["run_ref"] must equal run_ref'
            )
        if tuple(self.serialized_run_snapshot.get("report_refs", [])) != safe_report_refs:
            raise error_cls(
                'serialized_run_snapshot["report_refs"] must equal list(report_refs)'
            )
        if tuple(self.serialized_run_snapshot.get("suite_refs", [])) != safe_suite_refs:
            raise error_cls(
                'serialized_run_snapshot["suite_refs"] must equal list(suite_refs)'
            )

        # Freeze mapping fields.
        safe_serialized = _safe_frozen_mapping(
            self.serialized_run_snapshot, error_cls
        )
        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "suite_refs", safe_suite_refs)
        object.__setattr__(self, "report_refs", safe_report_refs)
        object.__setattr__(self, "suites", safe_suites)
        object.__setattr__(self, "suite_results", safe_suite_results_tuple)
        object.__setattr__(self, "report_snapshots", safe_report_snapshots_tuple)
        object.__setattr__(self, "serialized_run_snapshot", safe_serialized)
        object.__setattr__(self, "metadata", safe_metadata)


def run_model_boundary_captured_fixture_evaluation(
    *,
    run_ref: str,
    run_label: str,
    suites: Sequence[ModelBoundaryCapturedFixtureAssertionSuite],
    report_ref_prefix: str = "report",
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult:
    """Run the captured-fixture evaluation orchestrator.

    Accepts explicit already-built captured fixture assertion suites, runs the
    existing suite runner, creates report snapshots and a run snapshot, and
    returns an immutable result. Does not call models, parse raw captured text,
    read or write files, or mutate runtime state.
    """
    error_cls = ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError

    _validate_non_empty_string(run_ref, "run_ref", error_cls)
    _validate_non_empty_string(run_label, "run_label", error_cls)
    _validate_non_empty_string(
        report_ref_prefix, "report_ref_prefix", error_cls
    )

    safe_suites = _normalize_captured_fixture_assertion_suite_sequence(
        suites, error_cls
    )

    suite_results: list[ModelBoundaryCapturedFixtureAssertionSuiteResult] = []
    report_snapshots: list[
        ModelBoundaryCapturedFixtureAssertionReportSnapshot
    ] = []

    for index, suite in enumerate(safe_suites):
        suite_result = assert_model_boundary_captured_fixture_assertion_suite(
            suite
        )
        suite_results.append(suite_result)

        report_ref = f"{report_ref_prefix}-{index + 1}-{suite.suite_ref}"
        report_snapshot = (
            create_model_boundary_captured_fixture_assertion_report_snapshot(
                report_ref=report_ref,
                suite_result=suite_result,
            )
        )
        report_snapshots.append(report_snapshot)

    run_snapshot = create_model_boundary_captured_fixture_evaluation_run_snapshot(
        run_ref=run_ref,
        run_label=run_label,
        report_snapshots=report_snapshots,
    )

    serialized_run_snapshot = (
        serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
            run_snapshot
        )
    )

    suite_refs = tuple(s.suite_ref for s in safe_suites)
    report_refs = tuple(r.report_ref for r in report_snapshots)

    total_specs = sum(r.total_specs for r in suite_results)
    all_passed = all(r.all_passed for r in suite_results)

    if metadata is None:
        metadata = {
            "run_ref": run_ref,
            "run_label": run_label,
            "report_ref_prefix": report_ref_prefix,
            "suite_count": len(safe_suites),
            "all_passed": all_passed,
            "total_specs": total_specs,
        }

    return ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult(
        run_ref=run_ref,
        run_label=run_label,
        report_ref_prefix=report_ref_prefix,
        suite_refs=suite_refs,
        report_refs=report_refs,
        suites=safe_suites,
        suite_results=tuple(suite_results),
        report_snapshots=tuple(report_snapshots),
        run_snapshot=run_snapshot,
        serialized_run_snapshot=serialized_run_snapshot,
        metadata=metadata,
    )


def serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
    result: ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult,
) -> dict[str, Any]:
    """Serialize an orchestrator result into a deterministic plain dict.

    Returns stable summary data. Does not include suites, suite_results,
    report_snapshots, source_suite_result, or raw captured text.
    """
    error_cls = ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError

    if not isinstance(
        result,
        ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult,
    ):
        raise error_cls(
            "result must be a "
            "ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult instance"
        )

    return {
        "run_ref": result.run_ref,
        "run_label": result.run_label,
        "report_ref_prefix": result.report_ref_prefix,
        "suite_refs": list(result.suite_refs),
        "report_refs": list(result.report_refs),
        "run_snapshot": dict(result.serialized_run_snapshot),
        "metadata": dict(result.metadata),
    }


# ---------------------------------------------------------------------------
# PR-7 Slice 10 — Static Boundary Fixture Catalog
# ---------------------------------------------------------------------------


class ModelBoundaryStaticFixtureCatalogError(ModelBoundaryEvaluationError):
    """Raised for malformed static fixture catalog construction or serialization."""


def _normalize_captured_fixture_assertion_suite_sequence_for_catalog(
    suites: Any,
    error_cls: type[Exception],
) -> tuple[ModelBoundaryCapturedFixtureAssertionSuite, ...]:
    if isinstance(suites, (str, bytes)):
        raise error_cls("suites must not be a bare string or bytes")
    if not isinstance(suites, Sequence):
        raise error_cls("suites must be a sequence")
    if len(suites) == 0:
        raise error_cls("suites must contain at least one suite")

    normalized: list[ModelBoundaryCapturedFixtureAssertionSuite] = []
    seen_refs: set[str] = set()
    for i, item in enumerate(suites):
        if not isinstance(item, ModelBoundaryCapturedFixtureAssertionSuite):
            raise error_cls(
                f"suites[{i}] must be a "
                "ModelBoundaryCapturedFixtureAssertionSuite"
            )
        if item.suite_ref in seen_refs:
            raise error_cls(f"duplicate suite_ref: {item.suite_ref!r}")
        seen_refs.add(item.suite_ref)
        normalized.append(item)
    return tuple(normalized)


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryStaticFixtureCatalog:
    """Immutable catalog of static captured-fixture assertion suites."""

    catalog_ref: str
    catalog_label: str
    suite_refs: tuple[str, ...]
    suites: tuple[ModelBoundaryCapturedFixtureAssertionSuite, ...]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        error_cls = ModelBoundaryStaticFixtureCatalogError

        _validate_non_empty_string(self.catalog_ref, "catalog_ref", error_cls)
        _validate_non_empty_string(self.catalog_label, "catalog_label", error_cls)

        safe_suites = _normalize_captured_fixture_assertion_suite_sequence_for_catalog(
            self.suites, error_cls
        )
        derived_suite_refs = tuple(s.suite_ref for s in safe_suites)

        if isinstance(self.suite_refs, (str, bytes)):
            raise error_cls("suite_refs must not be a bare string or bytes")
        if not isinstance(self.suite_refs, Sequence):
            raise error_cls("suite_refs must be a sequence")
        supplied_suite_refs = tuple(self.suite_refs)
        if len(supplied_suite_refs) != len(derived_suite_refs):
            raise error_cls(
                f"suite_refs length ({len(supplied_suite_refs)}) must equal "
                f"len(suites) ({len(derived_suite_refs)})"
            )
        if supplied_suite_refs != derived_suite_refs:
            raise error_cls(
                f"suite_refs {list(supplied_suite_refs)} must equal "
                f"tuple(suite.suite_ref for suite in suites) "
                f"{list(derived_suite_refs)}"
            )

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "suite_refs", derived_suite_refs)
        object.__setattr__(self, "suites", safe_suites)
        object.__setattr__(self, "metadata", safe_metadata)


def _make_static_packet_result(
    *,
    request_ref: str = "static-req-1",
    warnings: tuple[str, ...] = (),
) -> ContextPacketCompilerResult:
    request = create_context_packet_assembly_request(
        request_ref=request_ref,
        packet_kind="single_event_narration",
        packet_payload={
            "event_ref": "static-evt-1",
            "event_kind": "narration",
            "visible_fact_refs": ["static-fact-1"],
        },
        assembly_timestamp="2026-01-01T00:00:00Z",
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


def _build_static_pass_suite() -> ModelBoundaryCapturedFixtureAssertionSuite:
    packet_result = _make_static_packet_result(request_ref="static-pass-req")
    fixture = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-pass-visible-narration",
        capture_ref="static-capture-pass-visible-narration",
        candidate_model_ref="static-model-pass",
        expected_output_family="narration_display",
        packet_result=packet_result,
        candidate_output={"display": "The scout steps into the lantern light and waits."},
        raw_captured_text="The scout steps into the lantern light and waits.",
    )
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-pass-visible-narration",
        expected_status="passed",
        expected_passed=True,
    )
    spec = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-pass-visible-narration",
        fixture=fixture,
        expectation=expectation,
    )
    return create_model_boundary_captured_fixture_assertion_suite(
        suite_ref="static-boundary-pass-suite",
        suite_label="Static Boundary Pass Suite",
        specs=[spec],
    )


def _build_static_hard_violation_suite() -> ModelBoundaryCapturedFixtureAssertionSuite:
    packet_result = _make_static_packet_result(request_ref="static-hard-req")

    fixture_a = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-hard-mutation",
        capture_ref="static-capture-hard-mutation",
        candidate_model_ref="static-model-hard",
        expected_output_family="narration_display",
        packet_result=packet_result,
        candidate_output={"state_delta": {"actor": "injured"}},
    )
    expectation_a = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-hard-mutation",
        expected_status="failed",
        expected_passed=False,
        expected_violation_codes=[
            "forbidden_authority_field_present",
            "state_mutation_claim_present",
        ],
        expected_forbidden_field_hits=["state_delta"],
    )
    spec_a = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-hard-mutation",
        fixture=fixture_a,
        expectation=expectation_a,
    )

    fixture_b = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-hard-event-commit",
        capture_ref="static-capture-hard-event-commit",
        candidate_model_ref="static-model-hard",
        expected_output_family="narration_display",
        packet_result=packet_result,
        candidate_output={"commit_event": "event-1"},
    )
    expectation_b = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-hard-event-commit",
        expected_status="failed",
        expected_passed=False,
        expected_violation_codes=[
            "event_commit_claim_present",
            "forbidden_authority_field_present",
        ],
        expected_forbidden_field_hits=["commit_event"],
    )
    spec_b = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-hard-event-commit",
        fixture=fixture_b,
        expectation=expectation_b,
    )

    fixture_c = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-hard-hidden-info",
        capture_ref="static-capture-hard-hidden-info",
        candidate_model_ref="static-model-hard",
        expected_output_family="narration_display",
        packet_result=packet_result,
        candidate_output={"hidden_fact": "The assassin is behind the curtain."},
    )
    expectation_c = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-hard-hidden-info",
        expected_status="failed",
        expected_passed=False,
        expected_violation_codes=[
            "forbidden_authority_field_present",
            "hidden_information_claim_present",
        ],
        expected_forbidden_field_hits=["hidden_fact"],
    )
    spec_c = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-hard-hidden-info",
        fixture=fixture_c,
        expectation=expectation_c,
    )

    return create_model_boundary_captured_fixture_assertion_suite(
        suite_ref="static-boundary-hard-violation-suite",
        suite_label="Static Boundary Hard Violation Suite",
        specs=[spec_a, spec_b, spec_c],
    )


def _build_static_warning_suite() -> ModelBoundaryCapturedFixtureAssertionSuite:
    packet_result = _make_static_packet_result(
        request_ref="static-warning-req",
        warnings=("static-warning-ref-1",),
    )
    fixture = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-warning-packet",
        capture_ref="static-capture-warning-packet",
        candidate_model_ref="static-model-warning",
        expected_output_family="narration_display",
        packet_result=packet_result,
        candidate_output={"display": "The room remains quiet."},
    )
    expectation = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-warning-packet",
        expected_status="needs_review",
        expected_passed=False,
        expected_violation_codes=["packet_warning_present"],
        expected_packet_warning_refs=["static-warning-ref-1"],
    )
    spec = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-warning-packet",
        fixture=fixture,
        expectation=expectation,
    )
    return create_model_boundary_captured_fixture_assertion_suite(
        suite_ref="static-boundary-warning-suite",
        suite_label="Static Boundary Warning Suite",
        specs=[spec],
    )


def _build_static_mixed_suite() -> ModelBoundaryCapturedFixtureAssertionSuite:
    clean_packet = _make_static_packet_result(request_ref="static-mixed-clean-req")
    warning_packet = _make_static_packet_result(
        request_ref="static-mixed-warning-req",
        warnings=("static-mixed-warning-ref-1",),
    )

    fixture_pass = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-mixed-pass",
        capture_ref="static-capture-mixed-pass",
        candidate_model_ref="static-model-mixed",
        expected_output_family="narration_display",
        packet_result=clean_packet,
        candidate_output={"display": "A calm breeze stirs the curtains."},
    )
    expectation_pass = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-mixed-pass",
        expected_status="passed",
        expected_passed=True,
    )
    spec_pass = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-mixed-pass",
        fixture=fixture_pass,
        expectation=expectation_pass,
    )

    fixture_fail = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-mixed-fail",
        capture_ref="static-capture-mixed-fail",
        candidate_model_ref="static-model-mixed",
        expected_output_family="narration_display",
        packet_result=clean_packet,
        candidate_output={"state_delta": {"hp": -5}},
    )
    expectation_fail = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-mixed-fail",
        expected_status="failed",
        expected_passed=False,
        expected_violation_codes=[
            "forbidden_authority_field_present",
            "state_mutation_claim_present",
        ],
        expected_forbidden_field_hits=["state_delta"],
    )
    spec_fail = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-mixed-fail",
        fixture=fixture_fail,
        expectation=expectation_fail,
    )

    fixture_warning = create_model_boundary_captured_output_fixture(
        fixture_ref="static-fixture-mixed-warning",
        capture_ref="static-capture-mixed-warning",
        candidate_model_ref="static-model-mixed",
        expected_output_family="narration_display",
        packet_result=warning_packet,
        candidate_output={"display": "Quiet steps echo."},
    )
    expectation_warning = create_model_boundary_expected_case_outcome(
        expectation_ref="exp-static-mixed-warning",
        expected_status="needs_review",
        expected_passed=False,
        expected_violation_codes=["packet_warning_present"],
        expected_packet_warning_refs=["static-mixed-warning-ref-1"],
    )
    spec_warning = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="static-fixture-mixed-warning",
        fixture=fixture_warning,
        expectation=expectation_warning,
    )

    return create_model_boundary_captured_fixture_assertion_suite(
        suite_ref="static-boundary-mixed-suite",
        suite_label="Static Boundary Mixed Suite",
        specs=[spec_pass, spec_fail, spec_warning],
    )


def create_model_boundary_static_fixture_catalog(
    *,
    catalog_ref: str = "model-boundary-static-fixture-catalog-v1",
    catalog_label: str = "Model Boundary Static Fixture Catalog v1",
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryStaticFixtureCatalog:
    """Build a deterministic static fixture catalog with four suites.

    Does not call models, parse prose, read runtime state, or write files.
    """
    suites = [
        _build_static_pass_suite(),
        _build_static_hard_violation_suite(),
        _build_static_warning_suite(),
        _build_static_mixed_suite(),
    ]

    if metadata is None:
        metadata = {
            "catalog_ref": catalog_ref,
            "catalog_label": catalog_label,
            "suite_count": len(suites),
            "fixture_family": "model_boundary_static_fixture_catalog",
            "version": 1,
        }

    return ModelBoundaryStaticFixtureCatalog(
        catalog_ref=catalog_ref,
        catalog_label=catalog_label,
        suite_refs=tuple(s.suite_ref for s in suites),
        suites=suites,
        metadata=metadata,
    )


def serialize_model_boundary_static_fixture_catalog(
    catalog: ModelBoundaryStaticFixtureCatalog,
) -> dict[str, Any]:
    """Serialize a static fixture catalog into a deterministic plain dict.

    Returns compact catalog metadata only. Does not serialize suites, specs,
    fixtures, packet payloads, raw captured text, or candidate output.
    """
    error_cls = ModelBoundaryStaticFixtureCatalogError

    if not isinstance(catalog, ModelBoundaryStaticFixtureCatalog):
        raise error_cls(
            "catalog must be a ModelBoundaryStaticFixtureCatalog instance"
        )

    return {
        "catalog_ref": catalog.catalog_ref,
        "catalog_label": catalog.catalog_label,
        "suite_refs": list(catalog.suite_refs),
        "metadata": dict(catalog.metadata),
    }


# ---------------------------------------------------------------------------
# PR-7 Slice 11 — Model Boundary Harness Closure Manifest
# ---------------------------------------------------------------------------

_DEFAULT_REQUIRED_SUITE_REFS = (
    "static-boundary-pass-suite",
    "static-boundary-hard-violation-suite",
    "static-boundary-warning-suite",
    "static-boundary-mixed-suite",
)


class ModelBoundaryEvaluationHarnessClosureManifestError(
    ModelBoundaryEvaluationError,
):
    """Raised for malformed closure manifest construction or serialization inputs."""


@dataclass(frozen=True, kw_only=True)
class ModelBoundaryEvaluationHarnessClosureManifest:
    """Immutable closure manifest for the PR-7 model-boundary evaluation harness.

    Proves that the static captured fixture catalog, orchestrator, report
    snapshots, and run snapshot form a coherent deterministic chain. Does not
    call models, parse prose, read runtime state, mutate inputs, or write files.
    """

    manifest_ref: str
    manifest_label: str
    catalog_ref: str
    catalog_label: str
    run_ref: str
    run_label: str
    suite_refs: tuple[str, ...]
    report_refs: tuple[str, ...]
    required_suite_refs: tuple[str, ...]
    missing_required_suite_refs: tuple[str, ...]
    total_suites: int
    total_reports: int
    total_specs: int
    assertion_passed: bool
    closure_ready: bool
    status_counts: Mapping[str, int]
    violation_counts: Mapping[str, int]
    packet_warning_report_refs: tuple[str, ...]
    catalog: ModelBoundaryStaticFixtureCatalog
    orchestrator_result: ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        error_cls = ModelBoundaryEvaluationHarnessClosureManifestError

        _validate_non_empty_string(self.manifest_ref, "manifest_ref", error_cls)
        _validate_non_empty_string(self.manifest_label, "manifest_label", error_cls)
        _validate_non_empty_string(self.catalog_ref, "catalog_ref", error_cls)
        _validate_non_empty_string(self.catalog_label, "catalog_label", error_cls)
        _validate_non_empty_string(self.run_ref, "run_ref", error_cls)
        _validate_non_empty_string(self.run_label, "run_label", error_cls)

        if not isinstance(self.catalog, ModelBoundaryStaticFixtureCatalog):
            raise error_cls(
                "catalog must be a ModelBoundaryStaticFixtureCatalog instance"
            )
        if not isinstance(
            self.orchestrator_result,
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult,
        ):
            raise error_cls(
                "orchestrator_result must be a "
                "ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult instance"
            )

        safe_suite_refs = _normalize_string_tuple(
            self.suite_refs, "suite_refs", error_cls
        )
        safe_report_refs = _normalize_string_tuple(
            self.report_refs, "report_refs", error_cls
        )
        safe_required_suite_refs = _normalize_string_tuple(
            self.required_suite_refs, "required_suite_refs", error_cls
        )
        safe_missing_required_suite_refs = _normalize_string_tuple(
            self.missing_required_suite_refs,
            "missing_required_suite_refs",
            error_cls,
        )
        safe_packet_warning_report_refs = _normalize_string_tuple(
            self.packet_warning_report_refs,
            "packet_warning_report_refs",
            error_cls,
        )

        total_suites = _validate_non_negative_int_not_bool(
            self.total_suites, "total_suites", error_cls
        )
        total_reports = _validate_non_negative_int_not_bool(
            self.total_reports, "total_reports", error_cls
        )
        total_specs = _validate_non_negative_int_not_bool(
            self.total_specs, "total_specs", error_cls
        )

        if not isinstance(self.assertion_passed, bool):
            raise error_cls("assertion_passed must be a bool")
        if not isinstance(self.closure_ready, bool):
            raise error_cls("closure_ready must be a bool")

        safe_status_counts = _validate_status_counts(
            self.status_counts, error_cls
        )
        safe_violation_counts = _validate_violation_counts(
            self.violation_counts, error_cls
        )

        if self.catalog_ref != self.catalog.catalog_ref:
            raise error_cls(
                f"catalog_ref ({self.catalog_ref!r}) must equal "
                f"catalog.catalog_ref ({self.catalog.catalog_ref!r})"
            )
        if self.catalog_label != self.catalog.catalog_label:
            raise error_cls(
                f"catalog_label ({self.catalog_label!r}) must equal "
                f"catalog.catalog_label ({self.catalog.catalog_label!r})"
            )
        if self.run_ref != self.orchestrator_result.run_ref:
            raise error_cls(
                f"run_ref ({self.run_ref!r}) must equal "
                f"orchestrator_result.run_ref ({self.orchestrator_result.run_ref!r})"
            )
        if self.run_label != self.orchestrator_result.run_label:
            raise error_cls(
                f"run_label ({self.run_label!r}) must equal "
                f"orchestrator_result.run_label ({self.orchestrator_result.run_label!r})"
            )
        if safe_suite_refs != self.catalog.suite_refs:
            raise error_cls(
                "suite_refs must equal catalog.suite_refs"
            )
        if safe_suite_refs != self.orchestrator_result.suite_refs:
            raise error_cls(
                "suite_refs must equal orchestrator_result.suite_refs"
            )
        if safe_report_refs != self.orchestrator_result.report_refs:
            raise error_cls(
                "report_refs must equal orchestrator_result.report_refs"
            )
        if total_suites != len(safe_suite_refs):
            raise error_cls(
                f"total_suites ({total_suites}) must equal "
                f"len(suite_refs) ({len(safe_suite_refs)})"
            )
        if total_reports != len(safe_report_refs):
            raise error_cls(
                f"total_reports ({total_reports}) must equal "
                f"len(report_refs) ({len(safe_report_refs)})"
            )
        if total_specs != self.orchestrator_result.run_snapshot.total_specs:
            raise error_cls(
                f"total_specs ({total_specs}) must equal "
                f"orchestrator_result.run_snapshot.total_specs "
                f"({self.orchestrator_result.run_snapshot.total_specs})"
            )
        if self.assertion_passed != self.orchestrator_result.run_snapshot.all_passed:
            raise error_cls(
                f"assertion_passed ({self.assertion_passed}) must equal "
                f"orchestrator_result.run_snapshot.all_passed "
                f"({self.orchestrator_result.run_snapshot.all_passed})"
            )

        expected_missing = tuple(
            ref for ref in safe_required_suite_refs
            if ref not in set(safe_suite_refs)
        )
        if safe_missing_required_suite_refs != expected_missing:
            raise error_cls(
                f"missing_required_suite_refs ({list(safe_missing_required_suite_refs)}) "
                f"must equal required refs not in suite_refs ({list(expected_missing)})"
            )

        expected_closure_ready = (
            self.assertion_passed is True
            and len(safe_missing_required_suite_refs) == 0
            and total_suites >= 4
            and total_reports >= 4
            and total_specs >= 1
            and safe_status_counts.get("passed", 0) >= 1
            and safe_status_counts.get("failed", 0) >= 1
            and safe_status_counts.get("needs_review", 0) >= 1
        )
        if self.closure_ready != expected_closure_ready:
            raise error_cls(
                f"closure_ready ({self.closure_ready}) does not match "
                f"computed value ({expected_closure_ready})"
            )

        safe_metadata = _safe_frozen_mapping(self.metadata, error_cls)

        object.__setattr__(self, "suite_refs", safe_suite_refs)
        object.__setattr__(self, "report_refs", safe_report_refs)
        object.__setattr__(self, "required_suite_refs", safe_required_suite_refs)
        object.__setattr__(
            self, "missing_required_suite_refs", safe_missing_required_suite_refs
        )
        object.__setattr__(
            self, "packet_warning_report_refs", safe_packet_warning_report_refs
        )
        object.__setattr__(self, "status_counts", MappingProxyType(dict(safe_status_counts)))
        object.__setattr__(self, "violation_counts", MappingProxyType(dict(safe_violation_counts)))
        object.__setattr__(self, "metadata", safe_metadata)


def create_model_boundary_evaluation_harness_closure_manifest(
    *,
    manifest_ref: str = "model-boundary-evaluation-harness-closure-v1",
    manifest_label: str = "Model Boundary Evaluation Harness Closure v1",
    catalog: ModelBoundaryStaticFixtureCatalog | None = None,
    run_ref: str = "model-boundary-evaluation-harness-closure-run-v1",
    run_label: str = "Model Boundary Evaluation Harness Closure Run v1",
    required_suite_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ModelBoundaryEvaluationHarnessClosureManifest:
    """Build a deterministic closure manifest from catalog + orchestrator.

    Does not call models, parse prose, read runtime state, write files,
    or mutate state.
    """
    if catalog is None:
        catalog = create_model_boundary_static_fixture_catalog()

    if required_suite_refs is None:
        required_suite_refs = _DEFAULT_REQUIRED_SUITE_REFS

    safe_required = tuple(required_suite_refs)

    orchestrator_result = run_model_boundary_captured_fixture_evaluation(
        run_ref=run_ref,
        run_label=run_label,
        suites=list(catalog.suites),
        report_ref_prefix="closure-report",
    )

    run_snapshot = orchestrator_result.run_snapshot

    suite_refs = catalog.suite_refs
    report_refs = orchestrator_result.report_refs
    total_suites = len(suite_refs)
    total_reports = len(report_refs)
    total_specs = run_snapshot.total_specs
    assertion_passed = run_snapshot.all_passed

    status_counts = dict(run_snapshot.status_counts)
    violation_counts = dict(run_snapshot.violation_counts)
    packet_warning_report_refs = tuple(run_snapshot.packet_warning_report_refs)

    suite_ref_set = set(suite_refs)
    missing_required = tuple(
        ref for ref in safe_required if ref not in suite_ref_set
    )

    closure_ready = (
        assertion_passed is True
        and len(missing_required) == 0
        and total_suites >= 4
        and total_reports >= 4
        and total_specs >= 1
        and status_counts.get("passed", 0) >= 1
        and status_counts.get("failed", 0) >= 1
        and status_counts.get("needs_review", 0) >= 1
    )

    if metadata is None:
        metadata = {
            "manifest_ref": manifest_ref,
            "manifest_label": manifest_label,
            "catalog_ref": catalog.catalog_ref,
            "run_ref": run_ref,
            "required_suite_count": len(safe_required),
            "suite_count": total_suites,
            "total_specs": total_specs,
            "assertion_passed": assertion_passed,
            "closure_ready": closure_ready,
            "fixture_family": "model_boundary_evaluation_harness_closure",
            "version": 1,
        }

    return ModelBoundaryEvaluationHarnessClosureManifest(
        manifest_ref=manifest_ref,
        manifest_label=manifest_label,
        catalog_ref=catalog.catalog_ref,
        catalog_label=catalog.catalog_label,
        run_ref=run_ref,
        run_label=run_label,
        suite_refs=suite_refs,
        report_refs=report_refs,
        required_suite_refs=safe_required,
        missing_required_suite_refs=missing_required,
        total_suites=total_suites,
        total_reports=total_reports,
        total_specs=total_specs,
        assertion_passed=assertion_passed,
        closure_ready=closure_ready,
        status_counts=status_counts,
        violation_counts=violation_counts,
        packet_warning_report_refs=packet_warning_report_refs,
        catalog=catalog,
        orchestrator_result=orchestrator_result,
        metadata=metadata,
    )


def serialize_model_boundary_evaluation_harness_closure_manifest(
    manifest: ModelBoundaryEvaluationHarnessClosureManifest,
) -> dict[str, Any]:
    """Serialize a closure manifest into a deterministic plain dict.

    Returns compact manifest metadata only. Does not serialize catalog,
    orchestrator_result, suites, specs, fixtures, packet payloads,
    candidate_output, raw captured text, suite_results, report_snapshots,
    source_suite_result, or run_snapshot.
    """
    error_cls = ModelBoundaryEvaluationHarnessClosureManifestError

    if not isinstance(manifest, ModelBoundaryEvaluationHarnessClosureManifest):
        raise error_cls(
            "manifest must be a "
            "ModelBoundaryEvaluationHarnessClosureManifest instance"
        )

    return {
        "manifest_ref": manifest.manifest_ref,
        "manifest_label": manifest.manifest_label,
        "catalog_ref": manifest.catalog_ref,
        "catalog_label": manifest.catalog_label,
        "run_ref": manifest.run_ref,
        "run_label": manifest.run_label,
        "suite_refs": list(manifest.suite_refs),
        "report_refs": list(manifest.report_refs),
        "required_suite_refs": list(manifest.required_suite_refs),
        "missing_required_suite_refs": list(manifest.missing_required_suite_refs),
        "total_suites": manifest.total_suites,
        "total_reports": manifest.total_reports,
        "total_specs": manifest.total_specs,
        "assertion_passed": manifest.assertion_passed,
        "closure_ready": manifest.closure_ready,
        "status_counts": {
            status: manifest.status_counts[status]
            for status in sorted(manifest.status_counts)
        },
        "violation_counts": {
            code: manifest.violation_counts[code]
            for code in sorted(manifest.violation_counts)
        },
        "packet_warning_report_refs": list(manifest.packet_warning_report_refs),
        "metadata": dict(manifest.metadata),
    }
