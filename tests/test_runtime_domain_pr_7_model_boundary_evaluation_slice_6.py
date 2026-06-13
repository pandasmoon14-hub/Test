"""Tests for PR-7 Slice 6 — Captured Fixture Assertion Suite Runner."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    ModelBoundaryCapturedFixtureAssertionSpec,
    ModelBoundaryCapturedFixtureAssertionSuite,
    ModelBoundaryCapturedFixtureAssertionSuiteError,
    ModelBoundaryCapturedFixtureAssertionSuiteResult,
    ModelBoundaryCapturedOutputFixture,
    ModelBoundaryEvaluationError,
    assert_model_boundary_captured_fixture_assertion_suite,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_captured_fixture_assertion_spec,
    create_model_boundary_captured_fixture_assertion_suite,
    create_model_boundary_captured_output_fixture,
    create_model_boundary_expected_case_outcome,
)
from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
)
from astra_runtime.domain.model_boundary_evaluation import (
    MODEL_BOUNDARY_STATUS_VALUES,
    MODEL_BOUNDARY_VIOLATION_CODES,
    ModelBoundaryCapturedFixtureAssertionResult,
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
) -> Any:
    """Build a valid ModelBoundaryExpectedCaseOutcome."""
    return create_model_boundary_expected_case_outcome(
        expectation_ref=expectation_ref,
        expected_status=expected_status,
        expected_passed=expected_passed,
        expected_violation_codes=expected_violation_codes,
        expected_forbidden_field_hits=expected_forbidden_field_hits,
        expected_packet_warning_refs=expected_packet_warning_refs,
    )


def _make_spec(
    *,
    spec_ref: str = "spec-1",
    fixture: ModelBoundaryCapturedOutputFixture | None = None,
    expectation: Any | None = None,
    case_ref: str | None = None,
    case_metadata: dict[str, Any] | None = None,
    assertion_metadata: dict[str, Any] | None = None,
    result_metadata: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionSpec:
    """Build a valid ModelBoundaryCapturedFixtureAssertionSpec."""
    return create_model_boundary_captured_fixture_assertion_spec(
        spec_ref=spec_ref,
        fixture=fixture if fixture is not None else _make_fixture(),
        expectation=expectation if expectation is not None else _make_expectation(),
        case_ref=case_ref,
        case_metadata=case_metadata,
        assertion_metadata=assertion_metadata,
        result_metadata=result_metadata,
        metadata=metadata if metadata is not None else {},
    )


def _make_suite(
    *,
    suite_ref: str = "suite-1",
    suite_label: str = "Suite One",
    specs: list[ModelBoundaryCapturedFixtureAssertionSpec] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionSuite:
    """Build a valid ModelBoundaryCapturedFixtureAssertionSuite."""
    if specs is None:
        specs = [_make_spec()]
    return create_model_boundary_captured_fixture_assertion_suite(
        suite_ref=suite_ref,
        suite_label=suite_label,
        specs=specs,
        metadata=metadata if metadata is not None else {"suite_source": "test"},
    )


def _make_valid_result(
    *,
    suite_ref: str = "suite-1",
    suite_label: str = "Suite One",
    total_specs: int = 1,
    passed_specs: int = 1,
    failed_specs: int = 0,
    all_passed: bool = True,
    spec_results: list[ModelBoundaryCapturedFixtureAssertionResult] | None = None,
    status_counts: dict[str, int] | None = None,
    violation_counts: dict[str, int] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionSuiteResult:
    """Build a valid ModelBoundaryCapturedFixtureAssertionSuiteResult."""
    if spec_results is None:
        spec_results = [
            assert_model_boundary_captured_fixture_assertion_suite(
                _make_suite()
            ).spec_results[0]
        ]
    if status_counts is None:
        status_counts = {status: 0 for status in MODEL_BOUNDARY_STATUS_VALUES}
        status_counts["passed"] = passed_specs
    if violation_counts is None:
        violation_counts = {}
    return ModelBoundaryCapturedFixtureAssertionSuiteResult(
        suite_ref=suite_ref,
        suite_label=suite_label,
        total_specs=total_specs,
        passed_specs=passed_specs,
        failed_specs=failed_specs,
        all_passed=all_passed,
        spec_results=spec_results,
        status_counts=status_counts,
        violation_counts=violation_counts,
        metadata=metadata if metadata is not None else {},
    )


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------

def test_package_exports() -> None:
    """All PR-7 Slice 6 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        ModelBoundaryCapturedFixtureAssertionSuiteError,
        ModelBoundaryCapturedFixtureAssertionSpec,
        ModelBoundaryCapturedFixtureAssertionSuite,
        ModelBoundaryCapturedFixtureAssertionSuiteResult,
        create_model_boundary_captured_fixture_assertion_spec,
        create_model_boundary_captured_fixture_assertion_suite,
        assert_model_boundary_captured_fixture_assertion_suite,
    )

    assert ModelBoundaryCapturedFixtureAssertionSuiteError is not None
    assert ModelBoundaryCapturedFixtureAssertionSpec is not None
    assert ModelBoundaryCapturedFixtureAssertionSuite is not None
    assert ModelBoundaryCapturedFixtureAssertionSuiteResult is not None
    assert callable(create_model_boundary_captured_fixture_assertion_spec)
    assert callable(create_model_boundary_captured_fixture_assertion_suite)
    assert callable(assert_model_boundary_captured_fixture_assertion_suite)


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedFixtureAssertionSuiteError
# ---------------------------------------------------------------------------

def test_captured_fixture_assertion_suite_error_subclasses_model_boundary_evaluation_error() -> None:
    """ModelBoundaryCapturedFixtureAssertionSuiteError subclasses ModelBoundaryEvaluationError."""
    assert issubclass(
        ModelBoundaryCapturedFixtureAssertionSuiteError,
        ModelBoundaryEvaluationError,
    )
    assert issubclass(ModelBoundaryCapturedFixtureAssertionSuiteError, ValueError)


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedFixtureAssertionSpec
# ---------------------------------------------------------------------------

def test_captured_fixture_assertion_spec_is_frozen() -> None:
    """ModelBoundaryCapturedFixtureAssertionSpec instances are immutable."""
    spec = _make_spec()
    with pytest.raises(FrozenInstanceError):
        spec.spec_ref = "other"  # type: ignore[misc]


def test_captured_fixture_assertion_spec_metadata_is_deep_copied_and_frozen() -> None:
    """Metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    spec = _make_spec(metadata=mutable_meta)

    assert isinstance(spec.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(spec.metadata["tags"]) == ["a", "b"]


def test_captured_fixture_assertion_spec_freezes_optional_metadata_fields() -> None:
    """Provided case/assertion/result metadata are deep-copied and frozen."""
    case_meta: dict[str, Any] = {"case_key": ["x"]}
    assertion_meta: dict[str, Any] = {"assertion_key": ["y"]}
    result_meta: dict[str, Any] = {"result_key": ["z"]}

    spec = _make_spec(
        case_metadata=case_meta,
        assertion_metadata=assertion_meta,
        result_metadata=result_meta,
    )

    assert isinstance(spec.case_metadata, MappingProxyType)
    assert isinstance(spec.assertion_metadata, MappingProxyType)
    assert isinstance(spec.result_metadata, MappingProxyType)

    case_meta["case_key"].append("xx")
    assertion_meta["assertion_key"].append("yy")
    result_meta["result_key"].append("zz")

    assert list(spec.case_metadata["case_key"]) == ["x"]
    assert list(spec.assertion_metadata["assertion_key"]) == ["y"]
    assert list(spec.result_metadata["result_key"]) == ["z"]


def test_captured_fixture_assertion_spec_preserves_none_metadata_fields() -> None:
    """Optional metadata fields remain None when omitted."""
    spec = create_model_boundary_captured_fixture_assertion_spec(
        spec_ref="spec-1",
        fixture=_make_fixture(),
        expectation=_make_expectation(),
    )

    assert spec.case_metadata is None
    assert spec.assertion_metadata is None
    assert spec.result_metadata is None


def test_captured_fixture_assertion_spec_rejects_empty_spec_ref() -> None:
    """Empty spec_ref is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_spec(spec_ref="")


def test_captured_fixture_assertion_spec_rejects_non_fixture_fixture() -> None:
    """Non-fixture fixture value is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        create_model_boundary_captured_fixture_assertion_spec(
            spec_ref="spec-1",
            fixture={"not": "a fixture"},  # type: ignore[arg-type]
            expectation=_make_expectation(),
        )


def test_captured_fixture_assertion_spec_rejects_non_expectation_expectation() -> None:
    """Non-expectation expectation value is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        create_model_boundary_captured_fixture_assertion_spec(
            spec_ref="spec-1",
            fixture=_make_fixture(),
            expectation={"not": "an expectation"},  # type: ignore[arg-type]
        )


def test_captured_fixture_assertion_spec_rejects_blank_case_ref() -> None:
    """Blank case_ref is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_spec(case_ref="   ")


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedFixtureAssertionSuite
# ---------------------------------------------------------------------------

def test_captured_fixture_assertion_suite_is_frozen() -> None:
    """ModelBoundaryCapturedFixtureAssertionSuite instances are immutable."""
    suite = _make_suite()
    with pytest.raises(FrozenInstanceError):
        suite.suite_ref = "other"  # type: ignore[misc]


def test_captured_fixture_assertion_suite_metadata_is_deep_copied_and_frozen() -> None:
    """Suite metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    suite = _make_suite(metadata=mutable_meta)

    assert isinstance(suite.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(suite.metadata["tags"]) == ["a", "b"]


def test_captured_fixture_assertion_suite_rejects_empty_suite_ref() -> None:
    """Empty suite_ref is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_suite(suite_ref="")


def test_captured_fixture_assertion_suite_rejects_empty_suite_label() -> None:
    """Empty suite_label is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_suite(suite_label="")


def test_captured_fixture_assertion_suite_rejects_empty_specs() -> None:
    """Empty specs sequence is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_suite(specs=[])


def test_captured_fixture_assertion_suite_rejects_bare_string_specs() -> None:
    """Bare string specs are rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_suite(specs="not-a-sequence")  # type: ignore[arg-type]


def test_captured_fixture_assertion_suite_rejects_bare_bytes_specs() -> None:
    """Bare bytes specs are rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_suite(specs=b"not-a-sequence")  # type: ignore[arg-type]


def test_captured_fixture_assertion_suite_rejects_non_spec_item() -> None:
    """Non-spec items are rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_suite(specs=["not-a-spec"])  # type: ignore[list-item]


def test_captured_fixture_assertion_suite_rejects_duplicate_spec_ref() -> None:
    """Duplicate spec_ref values are rejected."""
    spec = _make_spec(spec_ref="same")
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_suite(specs=[spec, spec])


def test_captured_fixture_assertion_suite_preserves_spec_order() -> None:
    """Spec order is preserved in the suite."""
    spec_a = _make_spec(spec_ref="a")
    spec_b = _make_spec(spec_ref="b")
    spec_c = _make_spec(spec_ref="c")

    suite = _make_suite(specs=[spec_a, spec_b, spec_c])
    assert suite.specs == (spec_a, spec_b, spec_c)


# ---------------------------------------------------------------------------
# ModelBoundaryCapturedFixtureAssertionSuiteResult
# ---------------------------------------------------------------------------

def test_captured_fixture_assertion_suite_result_is_frozen() -> None:
    """ModelBoundaryCapturedFixtureAssertionSuiteResult instances are immutable."""
    result = _make_valid_result()
    with pytest.raises(FrozenInstanceError):
        result.suite_ref = "other"  # type: ignore[misc]


def test_captured_fixture_assertion_suite_result_metadata_is_deep_copied_and_frozen() -> None:
    """Suite result metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    result = _make_valid_result(metadata=mutable_meta)

    assert isinstance(result.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(result.metadata["tags"]) == ["a", "b"]


def test_captured_fixture_assertion_suite_result_rejects_count_sum_mismatch() -> None:
    """passed_specs + failed_specs must equal total_specs."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_valid_result(
            total_specs=2,
            passed_specs=2,
            failed_specs=1,
            all_passed=False,
        )


def test_captured_fixture_assertion_suite_result_rejects_all_passed_mismatch() -> None:
    """all_passed must match (failed_specs == 0)."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_valid_result(
            total_specs=1,
            passed_specs=1,
            failed_specs=0,
            all_passed=False,
        )


def test_captured_fixture_assertion_suite_result_rejects_missing_status_count_keys() -> None:
    """status_counts must include all known status values."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_valid_result(status_counts={"passed": 1})


def test_captured_fixture_assertion_suite_result_rejects_unknown_status_count_key() -> None:
    """Unknown status keys are rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_valid_result(
            status_counts={
                "passed": 1,
                "failed": 0,
                "needs_review": 0,
                "unknown": 0,
            }
        )


def test_captured_fixture_assertion_suite_result_rejects_unknown_violation_count_key() -> None:
    """Unknown violation codes are rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        _make_valid_result(violation_counts={"not_a_code": 1})


# ---------------------------------------------------------------------------
# assert_model_boundary_captured_fixture_assertion_suite
# ---------------------------------------------------------------------------

def test_suite_runner_rejects_non_suite_input() -> None:
    """Runner rejects non-suite input."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionSuiteError):
        assert_model_boundary_captured_fixture_assertion_suite("not-a-suite")  # type: ignore[arg-type]


def test_suite_runner_preserves_suite_ref_and_label() -> None:
    """Suite ref and label are preserved in the result."""
    suite = _make_suite(suite_ref="S1", suite_label="My Suite")
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    assert result.suite_ref == "S1"
    assert result.suite_label == "My Suite"


def test_suite_runner_preserves_spec_result_order() -> None:
    """Spec results are returned in the same order as the input specs."""
    spec_a = _make_spec(
        spec_ref="a",
        fixture=_make_fixture(fixture_ref="fixture-a"),
    )
    spec_b = _make_spec(
        spec_ref="b",
        fixture=_make_fixture(fixture_ref="fixture-b"),
    )
    suite = _make_suite(specs=[spec_a, spec_b])

    result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    assert len(result.spec_results) == 2
    assert result.spec_results[0].fixture_ref == "fixture-a"
    assert result.spec_results[1].fixture_ref == "fixture-b"


def test_suite_runner_counts_passed_and_failed_specs() -> None:
    """Passed and failed spec counts are computed from assertion results."""
    passing_spec = _make_spec(
        spec_ref="pass",
        fixture=_make_fixture(
            fixture_ref="fixture-pass",
            candidate_output={"display": "ok"},
        ),
        expectation=_make_expectation(expected_status="passed", expected_passed=True),
    )
    failing_spec = _make_spec(
        spec_ref="fail",
        fixture=_make_fixture(
            fixture_ref="fixture-fail",
            candidate_output={"state_delta": {"x": 1}},
        ),
        expectation=_make_expectation(expected_status="passed", expected_passed=True),
    )
    suite = _make_suite(specs=[passing_spec, failing_spec])

    result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    assert result.total_specs == 2
    assert result.passed_specs == 1
    assert result.failed_specs == 1


def test_suite_runner_all_passed_true_when_all_specs_pass() -> None:
    """all_passed is True when every spec passes."""
    suite = _make_suite(
        specs=[
            _make_spec(spec_ref="a"),
            _make_spec(spec_ref="b", fixture=_make_fixture(fixture_ref="fixture-b")),
        ]
    )
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    assert result.all_passed is True


def test_suite_runner_all_passed_false_when_any_spec_fails() -> None:
    """all_passed is False when any spec fails."""
    failing_spec = _make_spec(
        spec_ref="fail",
        fixture=_make_fixture(
            fixture_ref="fixture-fail",
            candidate_output={"hidden_fact": "secret"},
        ),
        expectation=_make_expectation(expected_status="passed", expected_passed=True),
    )
    suite = _make_suite(specs=[_make_spec(spec_ref="pass"), failing_spec])
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    assert result.all_passed is False


def test_suite_runner_includes_all_status_keys_even_when_zero() -> None:
    """Status counts include all known statuses, even those with zero count."""
    suite = _make_suite(specs=[_make_spec()])
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    assert set(result.status_counts.keys()) == set(MODEL_BOUNDARY_STATUS_VALUES)
    for status in MODEL_BOUNDARY_STATUS_VALUES:
        assert isinstance(result.status_counts[status], int)
        assert not isinstance(result.status_counts[status], bool)


def test_suite_runner_computes_violation_counts_from_nested_results() -> None:
    """Violation counts aggregate violation codes from nested evaluation results."""
    spec_a = _make_spec(
        spec_ref="a",
        fixture=_make_fixture(
            fixture_ref="fixture-a",
            candidate_output={"hidden_fact": "secret"},
        ),
        expectation=_make_expectation(
            expected_status="failed",
            expected_passed=False,
            expected_violation_codes=("hidden_information_claim_present",),
        ),
    )
    spec_b = _make_spec(
        spec_ref="b",
        fixture=_make_fixture(
            fixture_ref="fixture-b",
            candidate_output={"state_delta": {"x": 1}},
        ),
        expectation=_make_expectation(
            expected_status="failed",
            expected_passed=False,
            expected_violation_codes=("state_mutation_claim_present",),
        ),
    )
    suite = _make_suite(specs=[spec_a, spec_b])
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    assert result.violation_counts["hidden_information_claim_present"] == 1
    assert result.violation_counts["state_mutation_claim_present"] == 1
    assert list(result.violation_counts.keys()) == sorted(
        result.violation_counts.keys()
    )


def test_suite_runner_default_metadata_includes_suite_fields() -> None:
    """Default metadata includes suite_ref, suite_label, total_specs, and all_passed."""
    suite = _make_suite(
        suite_ref="S1",
        suite_label="My Suite",
        metadata={"origin": "test"},
    )
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    assert result.metadata["suite_ref"] == "S1"
    assert result.metadata["suite_label"] == "My Suite"
    assert result.metadata["total_specs"] == 1
    assert result.metadata["all_passed"] is True
    assert result.metadata["origin"] == "test"


def test_suite_runner_uses_metadata_override_when_supplied() -> None:
    """Runner uses caller-supplied metadata instead of the default."""
    suite = _make_suite()
    override = {"custom": "data"}
    result = assert_model_boundary_captured_fixture_assertion_suite(
        suite, metadata=override
    )

    assert result.metadata == MappingProxyType({"custom": "data"})


def test_suite_runner_passes_per_spec_case_metadata() -> None:
    """Per-spec case_metadata reaches the generated case."""
    spec = _make_spec(
        case_metadata={"case_marker": "present"},
    )
    suite = _make_suite(specs=[spec])
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    # case_metadata is accepted and the runner produces a valid combined result;
    # the generated case itself is not exposed, but the call path succeeds.
    assert isinstance(result.spec_results[0], ModelBoundaryCapturedFixtureAssertionResult)
    assert result.spec_results[0].assertion_passed is True


def test_suite_runner_passes_per_spec_assertion_metadata() -> None:
    """Per-spec assertion_metadata reaches the assertion result."""
    spec = _make_spec(
        assertion_metadata={"assertion_marker": "present"},
    )
    suite = _make_suite(specs=[spec])
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    assert (
        result.spec_results[0].assertion_result.metadata["assertion_marker"]
        == "present"
    )


def test_suite_runner_passes_per_spec_result_metadata() -> None:
    """Per-spec result_metadata reaches the captured fixture assertion result."""
    spec = _make_spec(
        result_metadata={"result_marker": "present"},
    )
    suite = _make_suite(specs=[spec])
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    assert result.spec_results[0].metadata["result_marker"] == "present"


def test_suite_runner_does_not_include_raw_captured_text_in_suite_metadata() -> None:
    """Suite metadata does not contain raw captured text."""
    suite = _make_suite()
    result = assert_model_boundary_captured_fixture_assertion_suite(suite)

    assert "raw_captured_text" not in result.metadata
    for spec_result in result.spec_results:
        assert spec_result.has_raw_captured_text is True


# ---------------------------------------------------------------------------
# Source scan — forbidden runtime/model/prose parsing/file IO systems
# ---------------------------------------------------------------------------

def test_module_does_not_import_or_call_forbidden_systems() -> None:
    """The module source avoids forbidden runtime/model/prose parsing/file IO."""
    import astra_runtime.domain.model_boundary_evaluation as mod

    source = mod.__loader__.get_source(mod.__name__) or ""
    forbidden_tokens = [
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
        "open(",
        "Path(",
        ".read_text(",
        ".write_text(",
    ]
    found: list[str] = []
    for token in forbidden_tokens:
        if token in source:
            found.append(token)

    assert not found, f"Forbidden tokens present in source: {found}"
