"""Tests for PR-7 Slice 8 — Captured Fixture Evaluation Run Snapshot."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    ModelBoundaryCapturedFixtureAssertionReportSnapshot,
    ModelBoundaryCapturedFixtureAssertionSuite,
    ModelBoundaryCapturedFixtureAssertionSuiteResult,
    ModelBoundaryCapturedFixtureEvaluationRunError,
    ModelBoundaryCapturedFixtureEvaluationRunSnapshot,
    ModelBoundaryCapturedOutputFixture,
    ModelBoundaryEvaluationError,
    assert_model_boundary_captured_fixture_assertion_suite,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_captured_fixture_assertion_report_snapshot,
    create_model_boundary_captured_fixture_assertion_spec,
    create_model_boundary_captured_fixture_assertion_suite,
    create_model_boundary_captured_fixture_evaluation_run_snapshot,
    create_model_boundary_captured_output_fixture,
    create_model_boundary_expected_case_outcome,
    serialize_model_boundary_captured_fixture_evaluation_run_snapshot,
)
from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
)
from astra_runtime.domain.model_boundary_evaluation import (
    MODEL_BOUNDARY_STATUS_VALUES,
    MODEL_BOUNDARY_VIOLATION_CODES,
)


def _make_packet_result(
    warnings: tuple[str, ...] = (),
) -> ContextPacketCompilerResult:
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


def _make_report_snapshot(
    *,
    report_ref: str = "report-1",
    suite_result: ModelBoundaryCapturedFixtureAssertionSuiteResult | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureAssertionReportSnapshot:
    """Build a valid report snapshot through the PR-7 Slice 7 factory."""
    if suite_result is None:
        suite_result = _make_suite_result()
    return create_model_boundary_captured_fixture_assertion_report_snapshot(
        report_ref=report_ref,
        suite_result=suite_result,
        metadata=metadata,
    )


def _make_passing_suite_result(
    suite_ref: str = "suite-pass",
    suite_label: str = "Passing Suite",
) -> ModelBoundaryCapturedFixtureAssertionSuiteResult:
    """Build a suite result where every spec passes."""
    return _make_suite_result(suite_ref=suite_ref, suite_label=suite_label)


def _make_failing_suite_result(
    suite_ref: str = "suite-fail",
    suite_label: str = "Failing Suite",
) -> ModelBoundaryCapturedFixtureAssertionSuiteResult:
    """Build a suite result with one passing and one failing spec."""
    pass_spec = _make_spec(
        spec_ref="spec-pass",
        case_ref="case-pass",
        fixture=_make_fixture(
            fixture_ref="fixture-pass",
            candidate_output={"display": "ok"},
        ),
        expectation=_make_expectation(expected_status="passed"),
    )
    fail_spec = _make_spec(
        spec_ref="spec-fail",
        case_ref="case-fail",
        fixture=_make_fixture(
            fixture_ref="fixture-fail",
            candidate_output={"commit_event": "bad"},
        ),
        expectation=_make_expectation(expected_status="passed"),
    )
    return _make_suite_result(
        suite_ref=suite_ref,
        suite_label=suite_label,
        specs=[pass_spec, fail_spec],
    )


def _make_warning_suite_result(
    suite_ref: str = "suite-warn",
    suite_label: str = "Warning Suite",
) -> ModelBoundaryCapturedFixtureAssertionSuiteResult:
    """Build a suite result with one spec that carries packet warnings."""
    packet_result = _make_packet_result(warnings=("warn-1",))
    warn_spec = _make_spec(
        spec_ref="spec-warn",
        case_ref="case-warn",
        fixture=_make_fixture(
            fixture_ref="fixture-warn",
            packet_result=packet_result,
            candidate_output={"display": "ok"},
        ),
        expectation=_make_expectation(
            expected_status="needs_review",
            expected_violation_codes=("packet_warning_present",),
        ),
    )
    return _make_suite_result(
        suite_ref=suite_ref,
        suite_label=suite_label,
        specs=[warn_spec],
    )


def _make_valid_run_snapshot(
    *,
    run_ref: str = "run-1",
    run_label: str = "Run One",
    reports: list[ModelBoundaryCapturedFixtureAssertionReportSnapshot] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ModelBoundaryCapturedFixtureEvaluationRunSnapshot:
    """Build a valid run snapshot through the factory."""
    if reports is None:
        reports = [
            _make_report_snapshot(
                report_ref="report-1",
                suite_result=_make_passing_suite_result(),
            )
        ]
    return create_model_boundary_captured_fixture_evaluation_run_snapshot(
        run_ref=run_ref,
        run_label=run_label,
        report_snapshots=reports,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------


def test_package_exports() -> None:
    """All PR-7 Slice 8 public symbols are exported from astra_runtime.domain."""
    from astra_runtime.domain import (
        ModelBoundaryCapturedFixtureEvaluationRunError,
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot,
        create_model_boundary_captured_fixture_evaluation_run_snapshot,
        serialize_model_boundary_captured_fixture_evaluation_run_snapshot,
    )

    assert ModelBoundaryCapturedFixtureEvaluationRunError is not None
    assert ModelBoundaryCapturedFixtureEvaluationRunSnapshot is not None
    assert create_model_boundary_captured_fixture_evaluation_run_snapshot is not None
    assert serialize_model_boundary_captured_fixture_evaluation_run_snapshot is not None


# ---------------------------------------------------------------------------
# Error class
# ---------------------------------------------------------------------------


def test_run_error_subclasses_model_boundary_evaluation_error() -> None:
    """Run error is a subclass of ModelBoundaryEvaluationError."""
    assert issubclass(
        ModelBoundaryCapturedFixtureEvaluationRunError, ModelBoundaryEvaluationError
    )


# ---------------------------------------------------------------------------
# Run snapshot immutability and normalization
# ---------------------------------------------------------------------------


def test_run_snapshot_is_frozen() -> None:
    """Run snapshot dataclass is frozen."""
    snapshot = _make_valid_run_snapshot()
    with pytest.raises(FrozenInstanceError):
        snapshot.run_ref = "other"  # type: ignore[misc]


def test_run_snapshot_metadata_is_deep_copied_and_frozen() -> None:
    """Run snapshot metadata is deep-copied and frozen."""
    mutable_meta: dict[str, Any] = {"tags": ["a", "b"]}
    snapshot = _make_valid_run_snapshot(metadata=mutable_meta)
    assert isinstance(snapshot.metadata, MappingProxyType)
    mutable_meta["tags"].append("c")
    assert list(snapshot.metadata["tags"]) == ["a", "b"]


def test_report_snapshots_is_stored_as_tuple() -> None:
    """report_snapshots is stored as a tuple."""
    snapshot = _make_valid_run_snapshot()
    assert isinstance(snapshot.report_snapshots, tuple)
    for item in snapshot.report_snapshots:
        assert isinstance(item, ModelBoundaryCapturedFixtureAssertionReportSnapshot)


def test_run_snapshot_status_counts_are_frozen() -> None:
    """status_counts is frozen inside the run snapshot."""
    snapshot = _make_valid_run_snapshot()
    assert isinstance(snapshot.status_counts, MappingProxyType)


def test_run_snapshot_violation_counts_are_frozen() -> None:
    """violation_counts is frozen inside the run snapshot."""
    snapshot = _make_valid_run_snapshot()
    assert isinstance(snapshot.violation_counts, MappingProxyType)


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def test_serializer_returns_keys_in_exact_required_order() -> None:
    """Serialized dict keys follow the exact required order."""
    snapshot = _make_valid_run_snapshot()
    payload = serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
        snapshot
    )
    expected_keys = [
        "run_ref",
        "run_label",
        "total_reports",
        "total_specs",
        "passed_specs",
        "failed_specs",
        "all_passed",
        "report_refs",
        "suite_refs",
        "suite_labels",
        "failed_report_refs",
        "failed_suite_refs",
        "packet_warning_report_refs",
        "status_counts",
        "violation_counts",
        "metadata",
    ]
    assert list(payload.keys()) == expected_keys


def test_serializer_returns_tuple_fields_as_lists() -> None:
    """Tuple fields serialize as lists."""
    snapshot = _make_valid_run_snapshot()
    payload = serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
        snapshot
    )
    for key in (
        "report_refs",
        "suite_refs",
        "suite_labels",
        "failed_report_refs",
        "failed_suite_refs",
        "packet_warning_report_refs",
    ):
        assert isinstance(payload[key], list)


def test_serializer_returns_status_counts_and_violation_counts_as_plain_dicts() -> None:
    """Status and violation counts are plain dicts with sorted keys."""
    snapshot = _make_valid_run_snapshot()
    payload = serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
        snapshot
    )
    assert isinstance(payload["status_counts"], dict)
    assert list(payload["status_counts"].keys()) == sorted(MODEL_BOUNDARY_STATUS_VALUES)
    assert isinstance(payload["violation_counts"], dict)


def test_serializer_does_not_include_report_snapshots() -> None:
    """Serialized payload does not include the nested report_snapshots."""
    snapshot = _make_valid_run_snapshot()
    payload = serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
        snapshot
    )
    assert "report_snapshots" not in payload


def test_serializer_does_not_include_source_suite_result() -> None:
    """Serialized payload does not include source_suite_result."""
    snapshot = _make_valid_run_snapshot()
    payload = serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
        snapshot
    )
    assert "source_suite_result" not in payload


def test_serializer_does_not_include_raw_captured_text() -> None:
    """Serialized payload does not include raw captured text."""
    snapshot = _make_valid_run_snapshot()
    payload = serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
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
# Run snapshot validation
# ---------------------------------------------------------------------------


def _valid_status_counts(total: int = 1) -> dict[str, int]:
    """Return a valid status_counts mapping summing to total."""
    return {"passed": total, "failed": 0, "needs_review": 0}


def _base_run_snapshot_kwargs(
    report: ModelBoundaryCapturedFixtureAssertionReportSnapshot,
) -> dict[str, Any]:
    """Return kwargs for a minimal valid direct run snapshot."""
    return {
        "run_ref": "run-1",
        "run_label": "Run One",
        "total_reports": 1,
        "total_specs": report.total_specs,
        "passed_specs": report.passed_specs,
        "failed_specs": report.failed_specs,
        "all_passed": report.all_passed,
        "report_refs": (report.report_ref,),
        "suite_refs": (report.suite_ref,),
        "suite_labels": (report.suite_label,),
        "failed_report_refs": report.failed_spec_refs,
        "failed_suite_refs": report.failed_case_refs,
        "packet_warning_report_refs": report.packet_warning_case_refs,
        "status_counts": dict(report.status_counts),
        "violation_counts": dict(report.violation_counts),
        "report_snapshots": (report,),
    }


def test_snapshot_rejects_empty_run_ref() -> None:
    """Empty run_ref is rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["run_ref"] = ""
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_empty_run_label() -> None:
    """Empty run_label is rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["run_label"] = "   "
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_negative_total_reports() -> None:
    """Negative total_reports is rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["total_reports"] = -1
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_bool_count_fields() -> None:
    """Bool count fields are rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["total_specs"] = True  # type: ignore[dict-item]
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_count_sum_mismatch() -> None:
    """passed_specs + failed_specs must equal total_specs."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["passed_specs"] = kwargs["passed_specs"] + 1
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_all_passed_mismatch() -> None:
    """all_passed must equal (failed_specs == 0)."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["all_passed"] = not kwargs["all_passed"]
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_empty_report_snapshots() -> None:
    """Empty report_snapshots is rejected."""
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(
            run_ref="run-1",
            run_label="Run One",
            total_reports=0,
            total_specs=0,
            passed_specs=0,
            failed_specs=0,
            all_passed=True,
            report_refs=(),
            suite_refs=(),
            suite_labels=(),
            status_counts={status: 0 for status in MODEL_BOUNDARY_STATUS_VALUES},
            violation_counts={},
            report_snapshots=[],
        )


def test_snapshot_rejects_bare_string_report_snapshots() -> None:
    """Bare string report_snapshots is rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["report_snapshots"] = "not-a-sequence"  # type: ignore[dict-item]
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_non_report_snapshot_item() -> None:
    """Non-report-snapshot items are rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["report_snapshots"] = [report, "not-a-snapshot"]  # type: ignore[dict-item]
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_duplicate_report_ref() -> None:
    """Duplicate report_ref values are rejected."""
    report = _make_report_snapshot(report_ref="report-dup")
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["total_reports"] = 2
    kwargs["total_specs"] = report.total_specs * 2
    kwargs["passed_specs"] = report.passed_specs * 2
    kwargs["report_refs"] = ("report-dup", "report-dup")
    kwargs["suite_refs"] = (report.suite_ref, report.suite_ref)
    kwargs["suite_labels"] = (report.suite_label, report.suite_label)
    kwargs["report_snapshots"] = [report, report]
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_total_reports_mismatch() -> None:
    """total_reports must equal len(report_snapshots)."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["total_reports"] = 2
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_total_specs_mismatch_against_reports() -> None:
    """total_specs must equal sum of report total_specs."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["total_specs"] = kwargs["total_specs"] + 1
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_passed_specs_mismatch_against_reports() -> None:
    """passed_specs must equal sum of report passed_specs."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["passed_specs"] = kwargs["passed_specs"] + 1
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_failed_specs_mismatch_against_reports() -> None:
    """failed_specs must equal sum of report failed_specs."""
    failing_report = _make_report_snapshot(
        report_ref="report-fail",
        suite_result=_make_failing_suite_result(),
    )
    kwargs = _base_run_snapshot_kwargs(failing_report)
    kwargs["failed_specs"] = kwargs["failed_specs"] + 1
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_all_passed_mismatch_against_reports() -> None:
    """all_passed must equal all(report.all_passed)."""
    failing_report = _make_report_snapshot(
        report_ref="report-fail",
        suite_result=_make_failing_suite_result(),
    )
    kwargs = _base_run_snapshot_kwargs(failing_report)
    kwargs["all_passed"] = True
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_report_refs_mismatch_against_reports() -> None:
    """report_refs must match report report_refs."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["report_refs"] = ("wrong-report",)
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_suite_refs_mismatch_against_reports() -> None:
    """suite_refs must match report suite_refs."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["suite_refs"] = ("wrong-suite",)
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_suite_labels_mismatch_against_reports() -> None:
    """suite_labels must match report suite_labels."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["suite_labels"] = ("Wrong Suite",)
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_missing_status_count_keys() -> None:
    """status_counts must include all known status values."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["status_counts"] = {"passed": 1}
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_unknown_status_count_key() -> None:
    """Unknown status count keys are rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["status_counts"] = {**dict(report.status_counts), "unknown": 0}
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


def test_snapshot_rejects_unknown_violation_count_key() -> None:
    """Unknown violation count keys are rejected."""
    report = _make_report_snapshot()
    kwargs = _base_run_snapshot_kwargs(report)
    kwargs["violation_counts"] = {"unknown_violation": 1}
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        ModelBoundaryCapturedFixtureEvaluationRunSnapshot(**kwargs)


# ---------------------------------------------------------------------------
# Factory behavior
# ---------------------------------------------------------------------------


def test_factory_rejects_non_sequence_report_snapshots() -> None:
    """Factory rejects non-sequence report_snapshots."""
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        create_model_boundary_captured_fixture_evaluation_run_snapshot(
            run_ref="run-1",
            run_label="Run One",
            report_snapshots=123,  # type: ignore[arg-type]
        )


def test_factory_derives_total_reports() -> None:
    """Factory derives total_reports from report_snapshots."""
    reports = [
        _make_report_snapshot(
            report_ref="report-1",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-2",
            suite_result=_make_failing_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.total_reports == 2


def test_factory_derives_total_specs() -> None:
    """Factory derives total_specs as sum of report total_specs."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-fail",
            suite_result=_make_failing_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.total_specs == 1 + 2


def test_factory_derives_passed_specs_and_failed_specs() -> None:
    """Factory derives passed_specs and failed_specs."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-fail",
            suite_result=_make_failing_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.passed_specs == 2
    assert snapshot.failed_specs == 1


def test_factory_derives_all_passed_true_when_all_reports_pass() -> None:
    """Factory derives all_passed True when every report passes."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass-1",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-pass-2",
            suite_result=_make_passing_suite_result(
                suite_ref="suite-pass-2", suite_label="Passing Suite 2"
            ),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.all_passed is True


def test_factory_derives_all_passed_false_when_any_report_fails() -> None:
    """Factory derives all_passed False when any report fails."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-fail",
            suite_result=_make_failing_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.all_passed is False


def test_factory_derives_report_refs_in_order() -> None:
    """Factory derives report_refs in caller order."""
    reports = [
        _make_report_snapshot(
            report_ref="report-a",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-b",
            suite_result=_make_passing_suite_result(
                suite_ref="suite-b", suite_label="Suite B"
            ),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.report_refs == ("report-a", "report-b")


def test_factory_derives_suite_refs_in_order() -> None:
    """Factory derives suite_refs in caller order."""
    reports = [
        _make_report_snapshot(
            report_ref="report-a",
            suite_result=_make_passing_suite_result(suite_ref="suite-a"),
        ),
        _make_report_snapshot(
            report_ref="report-b",
            suite_result=_make_passing_suite_result(suite_ref="suite-b"),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.suite_refs == ("suite-a", "suite-b")


def test_factory_derives_suite_labels_in_order() -> None:
    """Factory derives suite_labels in caller order."""
    reports = [
        _make_report_snapshot(
            report_ref="report-a",
            suite_result=_make_passing_suite_result(suite_label="Suite A"),
        ),
        _make_report_snapshot(
            report_ref="report-b",
            suite_result=_make_passing_suite_result(suite_label="Suite B"),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.suite_labels == ("Suite A", "Suite B")


def test_factory_derives_failed_report_refs() -> None:
    """Factory derives failed_report_refs from reports that did not pass."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-fail",
            suite_result=_make_failing_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.failed_report_refs == ("report-fail",)


def test_factory_derives_failed_suite_refs() -> None:
    """Factory derives failed_suite_refs from reports that did not pass."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass",
            suite_result=_make_passing_suite_result(suite_ref="suite-pass"),
        ),
        _make_report_snapshot(
            report_ref="report-fail",
            suite_result=_make_failing_suite_result(suite_ref="suite-fail"),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.failed_suite_refs == ("suite-fail",)


def test_factory_derives_packet_warning_report_refs() -> None:
    """Factory derives packet_warning_report_refs from reports with warnings."""
    reports = [
        _make_report_snapshot(
            report_ref="report-clean",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-warn",
            suite_result=_make_warning_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.packet_warning_report_refs == ("report-warn",)


def test_factory_sums_status_counts_across_reports() -> None:
    """Factory sums status_counts across all reports."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-fail",
            suite_result=_make_failing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-warn",
            suite_result=_make_warning_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.status_counts["passed"] == 2
    assert snapshot.status_counts["failed"] == 1
    assert snapshot.status_counts["needs_review"] == 1


def test_factory_sums_violation_counts_across_reports() -> None:
    """Factory sums violation_counts across all reports."""
    reports = [
        _make_report_snapshot(
            report_ref="report-pass",
            suite_result=_make_passing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-fail",
            suite_result=_make_failing_suite_result(),
        ),
        _make_report_snapshot(
            report_ref="report-warn",
            suite_result=_make_warning_suite_result(),
        ),
    ]
    snapshot = _make_valid_run_snapshot(reports=reports)
    assert snapshot.violation_counts["forbidden_authority_field_present"] == 1
    assert snapshot.violation_counts["packet_warning_present"] == 1


def test_factory_default_metadata_includes_required_fields() -> None:
    """Default metadata includes run_ref, run_label, total_reports, total_specs, all_passed."""
    reports = [
        _make_report_snapshot(
            report_ref="report-1",
            suite_result=_make_passing_suite_result(),
        )
    ]
    snapshot = _make_valid_run_snapshot(
        run_ref="run-1",
        run_label="Run One",
        reports=reports,
    )
    assert snapshot.metadata["run_ref"] == "run-1"
    assert snapshot.metadata["run_label"] == "Run One"
    assert snapshot.metadata["total_reports"] == 1
    assert snapshot.metadata["total_specs"] == 1
    assert snapshot.metadata["all_passed"] is True


def test_factory_uses_metadata_override_when_supplied() -> None:
    """Supplied metadata replaces the default metadata entirely."""
    snapshot = _make_valid_run_snapshot(metadata={"custom": "only"})
    assert dict(snapshot.metadata) == {"custom": "only"}


# ---------------------------------------------------------------------------
# Serializer validation
# ---------------------------------------------------------------------------


def test_serializer_rejects_non_run_snapshot_input() -> None:
    """Serializer rejects non-run-snapshot input."""
    with pytest.raises(ModelBoundaryCapturedFixtureEvaluationRunError):
        serialize_model_boundary_captured_fixture_evaluation_run_snapshot(
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
