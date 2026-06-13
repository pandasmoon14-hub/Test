"""Tests for PR-7 Slice 7 — Captured Fixture Assertion Report Snapshot."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    ModelBoundaryCapturedFixtureAssertionReportError,
    ModelBoundaryCapturedFixtureAssertionReportSnapshot,
    ModelBoundaryCapturedFixtureAssertionSuite,
    ModelBoundaryCapturedFixtureAssertionSuiteResult,
    ModelBoundaryCapturedOutputFixture,
    ModelBoundaryEvaluationError,
    assert_model_boundary_captured_fixture_assertion_suite,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_captured_fixture_assertion_report_snapshot,
    create_model_boundary_captured_fixture_assertion_spec,
    create_model_boundary_captured_fixture_assertion_suite,
    create_model_boundary_captured_output_fixture,
    create_model_boundary_expected_case_outcome,
    serialize_model_boundary_captured_fixture_assertion_report_snapshot,
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
        candidate_output=candidate_output
        if candidate_output is not None
        else {"display": "The knight moves forward."},
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
) -> Any:
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
    specs: list[Any] | None = None,
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


def _make_suite_result(
    *,
    suite_ref: str = "suite-1",
    suite_label: str = "Suite One",
    specs: list[Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionSuiteResult:
    """Build a valid ModelBoundaryCapturedFixtureAssertionSuiteResult."""
    suite = _make_suite(
        suite_ref=suite_ref, suite_label=suite_label, specs=specs, metadata=metadata
    )
    return assert_model_boundary_captured_fixture_assertion_suite(suite)


def _make_valid_snapshot(
    *,
    report_ref: str = "report-1",
    suite_result: ModelBoundaryCapturedFixtureAssertionSuiteResult | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionReportSnapshot:
    """Build a valid report snapshot through the factory."""
    if suite_result is None:
        suite_result = _make_suite_result()
    return create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref=report_ref,
        suite_result=suite_result,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------


def test_package_exports() -> None:
    """All PR-7 Slice 7 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        ModelBoundaryCapturedFixtureAssertionReportError,
        ModelBoundaryCapturedFixtureAssertionReportSnapshot,
        create_model_boundary_captured_fixture_assertion_report_snapshot,
        serialize_model_boundary_captured_fixture_assertion_report_snapshot,
    )

    assert ModelBoundaryCapturedFixtureAssertionReportError is not None
    assert ModelBoundaryCapturedFixtureAssertionReportSnapshot is not None
    assert create_model_boundary_captured_fixture_assertion_report_snapshot is not None
    assert serialize_model_boundary_captured_fixture_assertion_report_snapshot is not None


# ---------------------------------------------------------------------------
# Error class
# ---------------------------------------------------------------------------


def test_report_error_subclasses_model_boundary_evaluation_error() -> None:
    """Report error is a subclass of ModelBoundaryEvaluationError."""
    assert issubclass(
        ModelBoundaryCapturedFixtureAssertionReportError, ModelBoundaryEvaluationError
    )


# ---------------------------------------------------------------------------
# Report snapshot immutability and normalization
# ---------------------------------------------------------------------------


def test_report_snapshot_is_frozen() -> None:
    """Report snapshot dataclass is frozen."""
    snapshot = _make_valid_snapshot()
    with pytest.raises(FrozenInstanceError):
        snapshot.report_ref = "other"  # type: ignore[misc]


def test_report_snapshot_metadata_is_deep_copied_and_frozen() -> None:
    """Report snapshot metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    snapshot = _make_valid_snapshot(metadata=mutable_meta)
    assert isinstance(snapshot.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(snapshot.metadata["tags"]) == ["a", "b"]


def test_report_snapshot_status_counts_are_frozen() -> None:
    """status_counts is frozen inside the snapshot."""
    snapshot = _make_valid_snapshot()
    assert isinstance(snapshot.status_counts, MappingProxyType)


def test_report_snapshot_violation_counts_are_frozen() -> None:
    """violation_counts is frozen inside the snapshot."""
    snapshot = _make_valid_snapshot()
    assert isinstance(snapshot.violation_counts, MappingProxyType)


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def test_serializer_returns_keys_in_exact_required_order() -> None:
    """Serialized dict keys follow the exact required order."""
    snapshot = _make_valid_snapshot()
    payload = serialize_model_boundary_captured_fixture_assertion_report_snapshot(
        snapshot
    )
    expected_keys = [
        "report_ref",
        "suite_ref",
        "suite_label",
        "total_specs",
        "passed_specs",
        "failed_specs",
        "all_passed",
        "status_counts",
        "violation_counts",
        "spec_refs",
        "case_refs",
        "expectation_refs",
        "failed_spec_refs",
        "failed_case_refs",
        "packet_warning_case_refs",
        "metadata",
    ]
    assert list(payload.keys()) == expected_keys


def test_status_counts_and_violation_counts_serialize_as_plain_dicts() -> None:
    """Status and violation counts are plain dicts with sorted keys."""
    snapshot = _make_valid_snapshot()
    payload = serialize_model_boundary_captured_fixture_assertion_report_snapshot(
        snapshot
    )
    assert isinstance(payload["status_counts"], dict)
    assert list(payload["status_counts"].keys()) == sorted(
        MODEL_BOUNDARY_STATUS_VALUES
    )
    assert isinstance(payload["violation_counts"], dict)


def test_tuple_fields_serialize_as_lists() -> None:
    """Tuple fields serialize as lists."""
    snapshot = _make_valid_snapshot()
    payload = serialize_model_boundary_captured_fixture_assertion_report_snapshot(
        snapshot
    )
    for key in (
        "spec_refs",
        "case_refs",
        "expectation_refs",
        "failed_spec_refs",
        "failed_case_refs",
        "packet_warning_case_refs",
    ):
        assert isinstance(payload[key], list)


def test_source_suite_result_is_retained_but_not_serialized() -> None:
    """Snapshot retains source_suite_result but serializer omits it."""
    snapshot = _make_valid_snapshot()
    assert isinstance(
        snapshot.source_suite_result, ModelBoundaryCapturedFixtureAssertionSuiteResult
    )
    payload = serialize_model_boundary_captured_fixture_assertion_report_snapshot(
        snapshot
    )
    assert "source_suite_result" not in payload


def test_serializer_does_not_include_raw_captured_text() -> None:
    """Serialized payload does not include raw captured text."""
    snapshot = _make_valid_snapshot()
    payload = serialize_model_boundary_captured_fixture_assertion_report_snapshot(
        snapshot
    )
    assert "raw_captured_text" not in payload
    for value in _flatten_values(payload):
        assert "The knight moves forward." not in str(value)


def _flatten_values(value: Any) -> list[Any]:
    """Flatten a nested structure into leaf values for scanning."""
    items: list[Any] = []
    if isinstance(value, dict):
        for v in value.values():
            items.extend(_flatten_values(v))
    elif isinstance(value, (list, tuple)):
        for v in value:
            items.extend(_flatten_values(v))
    else:
        items.append(value)
    return items


# ---------------------------------------------------------------------------
# Snapshot validation
# ---------------------------------------------------------------------------


def test_snapshot_rejects_empty_report_ref() -> None:
    """Empty report_ref is rejected."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_empty_suite_ref() -> None:
    """Empty suite_ref is rejected."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref="",
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_empty_suite_label() -> None:
    """Empty suite_label is rejected."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label="   ",
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_count_sum_mismatch() -> None:
    """passed_specs + failed_specs must equal total_specs."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs + 1,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_all_passed_mismatch() -> None:
    """all_passed must equal (failed_specs == 0)."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=not suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_missing_status_count_keys() -> None:
    """status_counts must include all known status values."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts={"passed": 1},
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_unknown_status_count_key() -> None:
    """Unknown status count keys are rejected."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts={**dict(suite_result.status_counts), "unknown": 0},
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_unknown_violation_count_key() -> None:
    """Unknown violation count keys are rejected."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts={"unknown_violation": 1},
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_non_suite_result_source_suite_result() -> None:
    """source_suite_result must be a ModelBoundaryCapturedFixtureAssertionSuiteResult."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result="not-a-result",  # type: ignore[arg-type]
        )


def test_snapshot_rejects_source_suite_ref_mismatch() -> None:
    """suite_ref must match source_suite_result.suite_ref."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref="other-suite",
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_source_suite_label_mismatch() -> None:
    """suite_label must match source_suite_result.suite_label."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label="Other Suite",
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_source_total_specs_mismatch() -> None:
    """total_specs must match source_suite_result.total_specs."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs + 1,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_source_passed_specs_mismatch() -> None:
    """passed_specs must match source_suite_result.passed_specs."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs + 1,
            failed_specs=suite_result.failed_specs,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_source_failed_specs_mismatch() -> None:
    """failed_specs must match source_suite_result.failed_specs."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs + 1,
            all_passed=suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


def test_snapshot_rejects_source_all_passed_mismatch() -> None:
    """all_passed must match source_suite_result.all_passed."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        ModelBoundaryCapturedFixtureAssertionReportSnapshot(
            report_ref="report-1",
            suite_ref=suite_result.suite_ref,
            suite_label=suite_result.suite_label,
            total_specs=suite_result.total_specs,
            passed_specs=suite_result.passed_specs,
            failed_specs=suite_result.failed_specs,
            all_passed=not suite_result.all_passed,
            status_counts=dict(suite_result.status_counts),
            violation_counts=dict(suite_result.violation_counts),
            spec_refs=tuple(result.case_ref for result in suite_result.spec_results),
            case_refs=tuple(result.case_ref for result in suite_result.spec_results),
            expectation_refs=tuple(
                result.expectation_ref for result in suite_result.spec_results
            ),
            source_suite_result=suite_result,
        )


# ---------------------------------------------------------------------------
# Factory behavior
# ---------------------------------------------------------------------------


def test_factory_rejects_non_suite_result_input() -> None:
    """Factory rejects non-suite-result input."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        create_model_boundary_captured_fixture_assertion_report_snapshot(
            report_ref="report-1",
            suite_result="not-a-result",  # type: ignore[arg-type]
        )


def test_factory_rejects_empty_report_ref() -> None:
    """Factory rejects empty report_ref."""
    suite_result = _make_suite_result()
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        create_model_boundary_captured_fixture_assertion_report_snapshot(
            report_ref="",
            suite_result=suite_result,
        )


def test_factory_derives_spec_refs_in_order() -> None:
    """Factory derives spec_refs in order, falling back to case_ref."""
    suite = _make_suite(
        specs=[
            _make_spec(spec_ref="spec-a", case_ref="case-a"),
            _make_spec(spec_ref="spec-b", case_ref="case-b"),
        ]
    )
    suite_result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    # By default result_metadata does not include spec_ref, so fallback to case_ref.
    assert snapshot.spec_refs == ("case-a", "case-b")


def test_factory_uses_metadata_spec_ref_when_available() -> None:
    """Factory uses spec_ref from nested result metadata when available."""
    suite = _make_suite(
        specs=[
            _make_spec(
                spec_ref="spec-a",
                case_ref="case-a",
                result_metadata={"spec_ref": "metadata-spec-a"},
            ),
            _make_spec(spec_ref="spec-b", case_ref="case-b"),
        ]
    )
    suite_result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    assert snapshot.spec_refs == ("metadata-spec-a", "case-b")


def test_factory_derives_case_refs_in_order() -> None:
    """Factory derives case_refs in order."""
    suite = _make_suite(
        specs=[
            _make_spec(spec_ref="spec-a", case_ref="case-a"),
            _make_spec(spec_ref="spec-b", case_ref="case-b"),
        ]
    )
    suite_result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    assert snapshot.case_refs == ("case-a", "case-b")


def test_factory_derives_expectation_refs_in_order() -> None:
    """Factory derives expectation_refs in order."""
    suite = _make_suite(
        specs=[
            _make_spec(
                spec_ref="spec-a",
                expectation=_make_expectation(expectation_ref="exp-a"),
            ),
            _make_spec(
                spec_ref="spec-b",
                expectation=_make_expectation(expectation_ref="exp-b"),
            ),
        ]
    )
    suite_result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    assert snapshot.expectation_refs == ("exp-a", "exp-b")


def test_factory_derives_failed_spec_refs_from_assertion_failures() -> None:
    """Failed spec refs come from assertion failures."""
    suite = _make_suite(
        specs=[
            _make_spec(
                spec_ref="spec-pass",
                case_ref="case-pass",
                fixture=_make_fixture(candidate_output={"display": "ok"}),
                expectation=_make_expectation(expected_status="passed"),
            ),
            _make_spec(
                spec_ref="spec-fail",
                case_ref="case-fail",
                fixture=_make_fixture(
                    candidate_output={"commit_event": "bad"}
                ),
                expectation=_make_expectation(expected_status="passed"),
            ),
        ]
    )
    suite_result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    assert snapshot.failed_spec_refs == ("case-fail",)
    assert snapshot.failed_case_refs == ("case-fail",)


def test_factory_derives_packet_warning_case_refs_from_nested_warnings() -> None:
    """Packet warning case refs come from nested evaluation_result packet warnings."""
    packet_result = _make_packet_result(warnings=("warn-1",))
    suite = _make_suite(
        specs=[
            _make_spec(
                spec_ref="spec-warn",
                case_ref="case-warn",
                fixture=_make_fixture(packet_result=packet_result),
                expectation=_make_expectation(
                    expected_status="needs_review",
                    expected_violation_codes=("packet_warning_present",),
                ),
            ),
            _make_spec(
                spec_ref="spec-clean",
                case_ref="case-clean",
                expectation=_make_expectation(expected_status="passed"),
            ),
        ]
    )
    suite_result = assert_model_boundary_captured_fixture_assertion_suite(suite)
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    assert snapshot.packet_warning_case_refs == ("case-warn",)


def test_factory_default_metadata_includes_required_fields() -> None:
    """Default metadata includes report_ref, suite_ref, total_specs, and all_passed."""
    suite_result = _make_suite_result(
        metadata={"suite_source": "test"},
    )
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    assert snapshot.metadata["report_ref"] == "report-1"
    assert snapshot.metadata["suite_ref"] == suite_result.suite_ref
    assert snapshot.metadata["total_specs"] == suite_result.total_specs
    assert snapshot.metadata["all_passed"] == suite_result.all_passed
    assert snapshot.metadata["suite_source"] == "test"


def test_factory_uses_metadata_override_when_supplied() -> None:
    """Supplied metadata replaces the default metadata entirely."""
    suite_result = _make_suite_result()
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1",
        suite_result=suite_result,
        metadata={"custom": "only"},
    )
    assert dict(snapshot.metadata) == {"custom": "only"}


def test_factory_does_not_include_raw_captured_text_in_metadata() -> None:
    """Factory default metadata does not include raw captured text."""
    suite_result = _make_suite_result()
    snapshot = create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref="report-1", suite_result=suite_result
    )
    assert "raw_captured_text" not in snapshot.metadata
    for value in _flatten_values(dict(snapshot.metadata)):
        assert "The knight moves forward." not in str(value)


# ---------------------------------------------------------------------------
# Serializer validation
# ---------------------------------------------------------------------------


def test_serializer_rejects_non_snapshot_input() -> None:
    """Serializer rejects non-snapshot input."""
    with pytest.raises(ModelBoundaryCapturedFixtureAssertionReportError):
        serialize_model_boundary_captured_fixture_assertion_report_snapshot(
            "not-a-snapshot"  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# Source scan — forbidden runtime/model/prose parsing/file IO systems
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
    "open(",
    "Path(",
    ".read_text(",
    ".write_text(",
)


def test_source_module_does_not_import_or_call_forbidden_systems() -> None:
    """The implementation module contains no forbidden runtime integrations."""
    module_path = Path("src/astra_runtime/domain/model_boundary_evaluation.py")
    source = module_path.read_text(encoding="utf-8")
    for pattern in _FORBIDDEN_PATTERNS:
        assert pattern not in source, f"forbidden pattern found: {pattern!r}"

