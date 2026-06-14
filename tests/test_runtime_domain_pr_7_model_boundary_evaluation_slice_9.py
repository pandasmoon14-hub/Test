"""Tests for PR-7 Slice 9 — Captured Fixture Evaluation Run Orchestrator."""

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
    ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
    ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult,
    ModelBoundaryCapturedFixtureEvaluationRunSnapshot,
    ModelBoundaryCapturedOutputFixture,
    ModelBoundaryEvaluationError,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_model_boundary_captured_fixture_assertion_spec,
    create_model_boundary_captured_fixture_assertion_suite,
    create_model_boundary_captured_output_fixture,
    create_model_boundary_expected_case_outcome,
    run_model_boundary_captured_fixture_evaluation,
    serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result,
)
from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
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


def _make_passing_suite(
    suite_ref: str = "suite-pass",
    suite_label: str = "Passing Suite",
) -> ModelBoundaryCapturedFixtureAssertionSuite:
    """Build a suite where every spec passes."""
    return _make_suite(suite_ref=suite_ref, suite_label=suite_label)


def _make_failing_suite(
    suite_ref: str = "suite-fail",
    suite_label: str = "Failing Suite",
) -> ModelBoundaryCapturedFixtureAssertionSuite:
    """Build a suite with one passing and one failing spec."""
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
    return _make_suite(
        suite_ref=suite_ref,
        suite_label=suite_label,
        specs=[pass_spec, fail_spec],
    )


def _make_warning_suite(
    suite_ref: str = "suite-warn",
    suite_label: str = "Warning Suite",
) -> ModelBoundaryCapturedFixtureAssertionSuite:
    """Build a suite with one spec that carries packet warnings."""
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
            expected_packet_warning_refs=("warn-1",),
            expected_passed=False,
        ),
    )
    return _make_suite(
        suite_ref=suite_ref,
        suite_label=suite_label,
        specs=[warn_spec],
    )


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------


class TestPackageExports:
    """Verify Slice 9 symbols are reachable from astra_runtime.domain."""

    def test_orchestrator_error_exported(self) -> None:
        from astra_runtime.domain import (
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
        )
        assert ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError is not None

    def test_orchestrator_result_exported(self) -> None:
        from astra_runtime.domain import (
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult,
        )
        assert ModelBoundaryCapturedFixtureEvaluationRunOrchestratorResult is not None

    def test_run_function_exported(self) -> None:
        from astra_runtime.domain import (
            run_model_boundary_captured_fixture_evaluation,
        )
        assert callable(run_model_boundary_captured_fixture_evaluation)

    def test_serializer_function_exported(self) -> None:
        from astra_runtime.domain import (
            serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result,
        )
        assert callable(
            serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result
        )


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------


class TestOrchestratorErrorHierarchy:
    """Verify the orchestrator error subclasses ModelBoundaryEvaluationError."""

    def test_subclasses_model_boundary_evaluation_error(self) -> None:
        assert issubclass(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            ModelBoundaryEvaluationError,
        )


# ---------------------------------------------------------------------------
# Orchestrator result immutability
# ---------------------------------------------------------------------------


class TestOrchestratorResultFrozen:
    """Verify that the orchestrator result is frozen."""

    def test_frozen(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        with pytest.raises(FrozenInstanceError):
            result.run_ref = "changed"  # type: ignore[misc]

    def test_metadata_deep_copied_and_frozen(self) -> None:
        original = {"key": "value", "nested": {"a": 1}}
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
            metadata=original,
        )
        assert isinstance(result.metadata, MappingProxyType)
        original["key"] = "mutated"
        assert result.metadata["key"] == "value"

    def test_suites_stored_as_tuple(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        assert isinstance(result.suites, tuple)

    def test_suite_results_stored_as_tuple(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        assert isinstance(result.suite_results, tuple)

    def test_report_snapshots_stored_as_tuple(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        assert isinstance(result.report_snapshots, tuple)

    def test_serialized_run_snapshot_frozen(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        assert isinstance(result.serialized_run_snapshot, MappingProxyType)


# ---------------------------------------------------------------------------
# Orchestrator input validation
# ---------------------------------------------------------------------------


class TestOrchestratorInputValidation:
    """Verify input validation for the orchestrator."""

    def test_rejects_empty_run_ref(self) -> None:
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            match="run_ref",
        ):
            run_model_boundary_captured_fixture_evaluation(
                run_ref="",
                run_label="Run One",
                suites=[_make_passing_suite()],
            )

    def test_rejects_empty_run_label(self) -> None:
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            match="run_label",
        ):
            run_model_boundary_captured_fixture_evaluation(
                run_ref="run-1",
                run_label="",
                suites=[_make_passing_suite()],
            )

    def test_rejects_empty_report_ref_prefix(self) -> None:
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            match="report_ref_prefix",
        ):
            run_model_boundary_captured_fixture_evaluation(
                run_ref="run-1",
                run_label="Run One",
                suites=[_make_passing_suite()],
                report_ref_prefix="",
            )

    def test_rejects_empty_suites(self) -> None:
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            match="suites",
        ):
            run_model_boundary_captured_fixture_evaluation(
                run_ref="run-1",
                run_label="Run One",
                suites=[],
            )

    def test_rejects_bare_string_suites(self) -> None:
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            match="suites",
        ):
            run_model_boundary_captured_fixture_evaluation(
                run_ref="run-1",
                run_label="Run One",
                suites="not-a-list",  # type: ignore[arg-type]
            )

    def test_rejects_non_suite_item(self) -> None:
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            match="suites",
        ):
            run_model_boundary_captured_fixture_evaluation(
                run_ref="run-1",
                run_label="Run One",
                suites=["not-a-suite"],  # type: ignore[list-item]
            )

    def test_rejects_duplicate_suite_refs(self) -> None:
        s1 = _make_passing_suite(suite_ref="dup")
        s2 = _make_passing_suite(suite_ref="dup")
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
            match="duplicate suite_ref",
        ):
            run_model_boundary_captured_fixture_evaluation(
                run_ref="run-1",
                run_label="Run One",
                suites=[s1, s2],
            )


# ---------------------------------------------------------------------------
# Orchestrator behavior
# ---------------------------------------------------------------------------


class TestOrchestratorBehavior:
    """Verify orchestrator processing logic."""

    def test_preserves_suite_order(self) -> None:
        s1 = _make_passing_suite(suite_ref="alpha", suite_label="Alpha")
        s2 = _make_passing_suite(suite_ref="beta", suite_label="Beta")
        s3 = _make_passing_suite(suite_ref="gamma", suite_label="Gamma")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1, s2, s3],
        )
        assert result.suite_refs == ("alpha", "beta", "gamma")
        assert result.suites[0].suite_ref == "alpha"
        assert result.suites[1].suite_ref == "beta"
        assert result.suites[2].suite_ref == "gamma"

    def test_creates_deterministic_report_refs(self) -> None:
        s1 = _make_passing_suite(suite_ref="alpha", suite_label="Alpha")
        s2 = _make_passing_suite(suite_ref="beta", suite_label="Beta")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1, s2],
            report_ref_prefix="rpt",
        )
        assert result.report_refs == ("rpt-1-alpha", "rpt-2-beta")

    def test_produces_one_suite_result_per_suite(self) -> None:
        s1 = _make_passing_suite(suite_ref="a", suite_label="A")
        s2 = _make_passing_suite(suite_ref="b", suite_label="B")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1, s2],
        )
        assert len(result.suite_results) == 2
        assert result.suite_results[0].suite_ref == "a"
        assert result.suite_results[1].suite_ref == "b"

    def test_produces_one_report_snapshot_per_suite(self) -> None:
        s1 = _make_passing_suite(suite_ref="a", suite_label="A")
        s2 = _make_passing_suite(suite_ref="b", suite_label="B")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1, s2],
        )
        assert len(result.report_snapshots) == 2
        assert result.report_snapshots[0].suite_ref == "a"
        assert result.report_snapshots[1].suite_ref == "b"

    def test_run_snapshot_report_refs_match(self) -> None:
        s1 = _make_passing_suite(suite_ref="x", suite_label="X")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1],
        )
        assert result.run_snapshot.report_refs == result.report_refs

    def test_run_snapshot_suite_refs_match(self) -> None:
        s1 = _make_passing_suite(suite_ref="x", suite_label="X")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1],
        )
        assert result.run_snapshot.suite_refs == result.suite_refs


# ---------------------------------------------------------------------------
# Default metadata
# ---------------------------------------------------------------------------


class TestOrchestratorDefaultMetadata:
    """Verify default metadata population."""

    def test_default_metadata_includes_required_keys(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        meta = result.metadata
        assert meta["run_ref"] == "run-1"
        assert meta["run_label"] == "Run One"
        assert meta["report_ref_prefix"] == "report"
        assert meta["suite_count"] == 1
        assert meta["all_passed"] is True
        assert meta["total_specs"] == 1

    def test_metadata_override_when_supplied(self) -> None:
        custom = {"custom_key": "custom_value"}
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
            metadata=custom,
        )
        assert result.metadata["custom_key"] == "custom_value"
        assert "run_ref" not in result.metadata


# ---------------------------------------------------------------------------
# all_passed derivation
# ---------------------------------------------------------------------------


class TestOrchestratorAllPassed:
    """Verify all_passed derivation."""

    def test_all_passed_true_when_all_suites_pass(self) -> None:
        s1 = _make_passing_suite(suite_ref="a", suite_label="A")
        s2 = _make_passing_suite(suite_ref="b", suite_label="B")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1, s2],
        )
        assert result.metadata["all_passed"] is True
        assert result.run_snapshot.all_passed is True

    def test_all_passed_false_when_any_suite_fails(self) -> None:
        s1 = _make_passing_suite(suite_ref="pass", suite_label="Pass")
        s2 = _make_failing_suite(suite_ref="fail", suite_label="Fail")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1, s2],
        )
        assert result.metadata["all_passed"] is False
        assert result.run_snapshot.all_passed is False


# ---------------------------------------------------------------------------
# Packet warnings
# ---------------------------------------------------------------------------


class TestOrchestratorPacketWarnings:
    """Verify packet warning report refs carry through the run snapshot."""

    def test_carries_packet_warning_report_refs(self) -> None:
        s1 = _make_warning_suite(suite_ref="warn", suite_label="Warn")
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[s1],
        )
        assert len(result.run_snapshot.packet_warning_report_refs) > 0
        assert result.report_snapshots[0].report_ref in (
            result.run_snapshot.packet_warning_report_refs
        )


# ---------------------------------------------------------------------------
# Serializer
# ---------------------------------------------------------------------------


class TestOrchestratorSerializer:
    """Verify the orchestrator result serializer."""

    def test_rejects_non_orchestrator_result(self) -> None:
        with pytest.raises(
            ModelBoundaryCapturedFixtureEvaluationRunOrchestratorError,
        ):
            serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
                "not-a-result",  # type: ignore[arg-type]
            )

    def test_keys_in_exact_order(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        keys = list(serialized.keys())
        assert keys == [
            "run_ref",
            "run_label",
            "report_ref_prefix",
            "suite_refs",
            "report_refs",
            "run_snapshot",
            "metadata",
        ]

    def test_suite_refs_serialized_as_list(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        assert isinstance(serialized["suite_refs"], list)

    def test_report_refs_serialized_as_list(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        assert isinstance(serialized["report_refs"], list)

    def test_includes_serialized_run_snapshot(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        assert isinstance(serialized["run_snapshot"], dict)
        assert serialized["run_snapshot"]["run_ref"] == "run-1"

    def test_does_not_include_suites(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        assert "suites" not in serialized

    def test_does_not_include_suite_results(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        assert "suite_results" not in serialized

    def test_does_not_include_report_snapshots(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        assert "report_snapshots" not in serialized

    def test_does_not_include_source_suite_result(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        assert "source_suite_result" not in serialized

    def test_does_not_include_raw_captured_text(self) -> None:
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="run-1",
            run_label="Run One",
            suites=[_make_passing_suite()],
        )
        serialized = serialize_model_boundary_captured_fixture_evaluation_run_orchestrator_result(
            result
        )
        serialized_str = str(serialized)
        assert "raw_captured_text" not in serialized_str


# ---------------------------------------------------------------------------
# Source scan — forbidden imports
# ---------------------------------------------------------------------------


class TestSourceScanForbiddenImports:
    """Verify the module does not import or call forbidden systems."""

    @pytest.fixture(scope="class")
    def source_text(self) -> str:
        source_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "astra_runtime"
            / "domain"
            / "model_boundary_evaluation.py"
        )
        return source_path.read_text(encoding="utf-8")

    @pytest.mark.parametrize(
        "forbidden",
        [
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
            "ollama",
            "claude",
            "json.loads",
            "ast.literal_eval",
            "re.search",
            "re.match",
            "open(",
            "Path(",
            ".read_text(",
            ".write_text(",
        ],
    )
    def test_no_forbidden_import(self, source_text: str, forbidden: str) -> None:
        assert forbidden not in source_text, (
            f"Forbidden symbol {forbidden!r} found in source"
        )
