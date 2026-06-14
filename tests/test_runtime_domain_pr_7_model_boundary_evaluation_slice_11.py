"""PR-7 Slice 11 — Model Boundary Harness Closure Manifest tests."""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    ModelBoundaryEvaluationError,
    ModelBoundaryEvaluationHarnessClosureManifest,
    ModelBoundaryEvaluationHarnessClosureManifestError,
    create_model_boundary_evaluation_harness_closure_manifest,
    serialize_model_boundary_evaluation_harness_closure_manifest,
)


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------


class TestPackageExports:
    def test_error_class_exported(self):
        from astra_runtime.domain import ModelBoundaryEvaluationHarnessClosureManifestError as E  # noqa: N811
        assert E is ModelBoundaryEvaluationHarnessClosureManifestError

    def test_manifest_class_exported(self):
        from astra_runtime.domain import ModelBoundaryEvaluationHarnessClosureManifest as M  # noqa: N811
        assert M is ModelBoundaryEvaluationHarnessClosureManifest

    def test_create_function_exported(self):
        from astra_runtime.domain import create_model_boundary_evaluation_harness_closure_manifest as fn
        assert fn is create_model_boundary_evaluation_harness_closure_manifest

    def test_serialize_function_exported(self):
        from astra_runtime.domain import serialize_model_boundary_evaluation_harness_closure_manifest as fn
        assert fn is serialize_model_boundary_evaluation_harness_closure_manifest


# ---------------------------------------------------------------------------
# Error subclassing
# ---------------------------------------------------------------------------


class TestErrorSubclass:
    def test_subclasses_model_boundary_evaluation_error(self):
        assert issubclass(
            ModelBoundaryEvaluationHarnessClosureManifestError,
            ModelBoundaryEvaluationError,
        )

    def test_is_value_error(self):
        assert issubclass(
            ModelBoundaryEvaluationHarnessClosureManifestError,
            ValueError,
        )


# ---------------------------------------------------------------------------
# Default manifest construction
# ---------------------------------------------------------------------------


@pytest.fixture()
def default_manifest():
    return create_model_boundary_evaluation_harness_closure_manifest()


class TestManifestDataclass:
    def test_frozen(self, default_manifest):
        with pytest.raises(AttributeError):
            default_manifest.manifest_ref = "x"

    def test_metadata_deep_copied_and_frozen(self, default_manifest):
        assert isinstance(default_manifest.metadata, MappingProxyType)

    def test_tuple_fields_are_tuples(self, default_manifest):
        for field_name in (
            "suite_refs",
            "report_refs",
            "required_suite_refs",
            "missing_required_suite_refs",
            "packet_warning_report_refs",
        ):
            assert isinstance(getattr(default_manifest, field_name), tuple), field_name

    def test_mapping_fields_are_frozen(self, default_manifest):
        for field_name in ("status_counts", "violation_counts", "metadata"):
            assert isinstance(
                getattr(default_manifest, field_name), MappingProxyType
            ), field_name


class TestDefaultManifest:
    def test_default_manifest_ref(self, default_manifest):
        assert default_manifest.manifest_ref == "model-boundary-evaluation-harness-closure-v1"

    def test_default_manifest_label(self, default_manifest):
        assert default_manifest.manifest_label == "Model Boundary Evaluation Harness Closure v1"

    def test_default_catalog_ref(self, default_manifest):
        assert default_manifest.catalog_ref == "model-boundary-static-fixture-catalog-v1"

    def test_four_required_suite_refs(self, default_manifest):
        assert default_manifest.required_suite_refs == (
            "static-boundary-pass-suite",
            "static-boundary-hard-violation-suite",
            "static-boundary-warning-suite",
            "static-boundary-mixed-suite",
        )

    def test_no_missing_required_suite_refs(self, default_manifest):
        assert default_manifest.missing_required_suite_refs == ()

    def test_four_suite_refs(self, default_manifest):
        assert len(default_manifest.suite_refs) == 4

    def test_four_report_refs(self, default_manifest):
        assert len(default_manifest.report_refs) == 4

    def test_assertion_passed_true(self, default_manifest):
        assert default_manifest.assertion_passed is True

    def test_closure_ready_true(self, default_manifest):
        assert default_manifest.closure_ready is True

    def test_status_counts_has_passed(self, default_manifest):
        assert default_manifest.status_counts["passed"] >= 1

    def test_status_counts_has_failed(self, default_manifest):
        assert default_manifest.status_counts["failed"] >= 1

    def test_status_counts_has_needs_review(self, default_manifest):
        assert default_manifest.status_counts["needs_review"] >= 1

    def test_violation_counts_non_empty(self, default_manifest):
        assert len(default_manifest.violation_counts) > 0

    def test_packet_warning_report_refs_non_empty(self, default_manifest):
        assert len(default_manifest.packet_warning_report_refs) > 0


# ---------------------------------------------------------------------------
# Missing required suite refs → closure_ready is False
# ---------------------------------------------------------------------------


class TestMissingRequiredSuiteRefs:
    def test_missing_required_causes_not_ready(self):
        manifest = create_model_boundary_evaluation_harness_closure_manifest(
            required_suite_refs=(
                "static-boundary-pass-suite",
                "static-boundary-hard-violation-suite",
                "static-boundary-warning-suite",
                "static-boundary-mixed-suite",
                "nonexistent-suite-ref",
            ),
        )
        assert manifest.closure_ready is False
        assert "nonexistent-suite-ref" in manifest.missing_required_suite_refs


# ---------------------------------------------------------------------------
# Metadata override
# ---------------------------------------------------------------------------


class TestMetadataOverride:
    def test_custom_metadata_used(self):
        custom = {"custom_key": "custom_value"}
        manifest = create_model_boundary_evaluation_harness_closure_manifest(
            metadata=custom,
        )
        assert manifest.metadata["custom_key"] == "custom_value"


# ---------------------------------------------------------------------------
# Serializer tests
# ---------------------------------------------------------------------------


class TestSerializer:
    def test_rejects_non_manifest(self):
        with pytest.raises(ModelBoundaryEvaluationHarnessClosureManifestError):
            serialize_model_boundary_evaluation_harness_closure_manifest("not a manifest")

    def test_key_order(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        expected_keys = [
            "manifest_ref",
            "manifest_label",
            "catalog_ref",
            "catalog_label",
            "run_ref",
            "run_label",
            "suite_refs",
            "report_refs",
            "required_suite_refs",
            "missing_required_suite_refs",
            "total_suites",
            "total_reports",
            "total_specs",
            "assertion_passed",
            "closure_ready",
            "status_counts",
            "violation_counts",
            "packet_warning_report_refs",
            "metadata",
        ]
        assert list(result.keys()) == expected_keys

    def test_tuple_fields_serialized_as_lists(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        for key in (
            "suite_refs",
            "report_refs",
            "required_suite_refs",
            "missing_required_suite_refs",
            "packet_warning_report_refs",
        ):
            assert isinstance(result[key], list), key

    def test_mapping_fields_serialized_as_dicts(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        for key in ("status_counts", "violation_counts", "metadata"):
            assert isinstance(result[key], dict), key
            assert not isinstance(result[key], MappingProxyType), key

    def test_omits_catalog(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "catalog" not in result

    def test_omits_orchestrator_result(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "orchestrator_result" not in result

    def test_omits_suites(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "suites" not in result

    def test_omits_specs(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "specs" not in result
        assert "spec_results" not in result

    def test_omits_fixtures(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "fixtures" not in result

    def test_omits_packet_payloads(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "serialized_packet" not in result
        assert "packet_payload" not in result

    def test_omits_candidate_output(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "candidate_output" not in result

    def test_omits_raw_captured_text(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "raw_captured_text" not in result

    def test_omits_suite_results(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "suite_results" not in result

    def test_omits_report_snapshots(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "report_snapshots" not in result

    def test_omits_source_suite_result(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "source_suite_result" not in result

    def test_omits_run_snapshot(self, default_manifest):
        result = serialize_model_boundary_evaluation_harness_closure_manifest(
            default_manifest,
        )
        assert "run_snapshot" not in result


# ---------------------------------------------------------------------------
# Source scan — forbidden imports / calls
# ---------------------------------------------------------------------------


_FORBIDDEN_PATTERNS = [
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
]


class TestSourceScan:
    def test_no_forbidden_patterns_in_production_module(self):
        source_path = Path(__file__).resolve().parent.parent / (
            "src/astra_runtime/domain/model_boundary_evaluation.py"
        )
        source_text = source_path.read_text(encoding="utf-8")

        found: list[str] = []
        for pattern in _FORBIDDEN_PATTERNS:
            if pattern in source_text:
                found.append(pattern)

        assert found == [], f"Forbidden patterns found in production module: {found}"
