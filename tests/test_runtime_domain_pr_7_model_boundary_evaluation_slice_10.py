"""Tests for PR-7 Slice 10 — Static Boundary Fixture Catalog."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from types import MappingProxyType
from typing import Any

import pytest

from astra_runtime.domain import (
    ModelBoundaryCapturedFixtureAssertionSuite,
    ModelBoundaryEvaluationError,
    ModelBoundaryStaticFixtureCatalog,
    ModelBoundaryStaticFixtureCatalogError,
    create_model_boundary_static_fixture_catalog,
    run_model_boundary_captured_fixture_evaluation,
    serialize_model_boundary_static_fixture_catalog,
)


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------


class TestPackageExports:
    def test_catalog_error_exported(self) -> None:
        from astra_runtime.domain import ModelBoundaryStaticFixtureCatalogError as E
        assert E is not None

    def test_catalog_class_exported(self) -> None:
        from astra_runtime.domain import ModelBoundaryStaticFixtureCatalog as C
        assert C is not None

    def test_create_factory_exported(self) -> None:
        from astra_runtime.domain import create_model_boundary_static_fixture_catalog as f
        assert callable(f)

    def test_serialize_factory_exported(self) -> None:
        from astra_runtime.domain import serialize_model_boundary_static_fixture_catalog as f
        assert callable(f)


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------


class TestErrorHierarchy:
    def test_catalog_error_subclasses_evaluation_error(self) -> None:
        assert issubclass(
            ModelBoundaryStaticFixtureCatalogError,
            ModelBoundaryEvaluationError,
        )

    def test_catalog_error_subclasses_value_error(self) -> None:
        assert issubclass(ModelBoundaryStaticFixtureCatalogError, ValueError)


# ---------------------------------------------------------------------------
# Dataclass properties
# ---------------------------------------------------------------------------


class TestCatalogDataclass:
    def test_catalog_is_frozen(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        with pytest.raises(FrozenInstanceError):
            catalog.catalog_ref = "changed"  # type: ignore[misc]

    def test_metadata_is_deep_copied_and_frozen(self) -> None:
        original_meta = {"key": "value", "nested": {"a": 1}}
        catalog = create_model_boundary_static_fixture_catalog(
            metadata=original_meta,
        )
        original_meta["key"] = "changed"
        assert catalog.metadata["key"] == "value"
        assert isinstance(catalog.metadata, MappingProxyType)

    def test_suites_stored_as_tuple(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert isinstance(catalog.suites, tuple)

    def test_suite_refs_stored_as_tuple(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert isinstance(catalog.suite_refs, tuple)


# ---------------------------------------------------------------------------
# Catalog validation
# ---------------------------------------------------------------------------


class TestCatalogValidation:
    def test_rejects_empty_catalog_ref(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        with pytest.raises(ModelBoundaryStaticFixtureCatalogError):
            ModelBoundaryStaticFixtureCatalog(
                catalog_ref="",
                catalog_label="label",
                suite_refs=catalog.suite_refs,
                suites=catalog.suites,
            )

    def test_rejects_empty_catalog_label(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        with pytest.raises(ModelBoundaryStaticFixtureCatalogError):
            ModelBoundaryStaticFixtureCatalog(
                catalog_ref="ref",
                catalog_label="",
                suite_refs=catalog.suite_refs,
                suites=catalog.suites,
            )

    def test_rejects_empty_suites(self) -> None:
        with pytest.raises(ModelBoundaryStaticFixtureCatalogError):
            ModelBoundaryStaticFixtureCatalog(
                catalog_ref="ref",
                catalog_label="label",
                suite_refs=(),
                suites=(),
            )

    def test_rejects_bare_string_suites(self) -> None:
        with pytest.raises(ModelBoundaryStaticFixtureCatalogError):
            ModelBoundaryStaticFixtureCatalog(
                catalog_ref="ref",
                catalog_label="label",
                suite_refs=("a",),
                suites="not-a-sequence",  # type: ignore[arg-type]
            )

    def test_rejects_non_suite_item(self) -> None:
        with pytest.raises(ModelBoundaryStaticFixtureCatalogError):
            ModelBoundaryStaticFixtureCatalog(
                catalog_ref="ref",
                catalog_label="label",
                suite_refs=("a",),
                suites=[42],  # type: ignore[list-item]
            )

    def test_rejects_duplicate_suite_refs(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        suite = catalog.suites[0]
        with pytest.raises(ModelBoundaryStaticFixtureCatalogError, match="duplicate suite_ref"):
            ModelBoundaryStaticFixtureCatalog(
                catalog_ref="ref",
                catalog_label="label",
                suite_refs=(suite.suite_ref, suite.suite_ref),
                suites=[suite, suite],
            )


# ---------------------------------------------------------------------------
# Catalog factory defaults
# ---------------------------------------------------------------------------


class TestCatalogFactoryDefaults:
    def test_returns_exactly_four_suites(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert len(catalog.suites) == 4

    def test_suite_refs_match_expected(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert catalog.suite_refs == (
            "static-boundary-pass-suite",
            "static-boundary-hard-violation-suite",
            "static-boundary-warning-suite",
            "static-boundary-mixed-suite",
        )

    def test_default_metadata_includes_catalog_ref(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert catalog.metadata["catalog_ref"] == catalog.catalog_ref

    def test_default_metadata_includes_catalog_label(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert catalog.metadata["catalog_label"] == catalog.catalog_label

    def test_default_metadata_includes_suite_count(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert catalog.metadata["suite_count"] == 4

    def test_default_metadata_includes_fixture_family(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert catalog.metadata["fixture_family"] == "model_boundary_static_fixture_catalog"

    def test_default_metadata_includes_version(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        assert catalog.metadata["version"] == 1

    def test_metadata_override(self) -> None:
        custom = {"custom_key": "custom_value"}
        catalog = create_model_boundary_static_fixture_catalog(metadata=custom)
        assert catalog.metadata["custom_key"] == "custom_value"
        assert "catalog_ref" not in catalog.metadata


# ---------------------------------------------------------------------------
# Serializer
# ---------------------------------------------------------------------------


class TestCatalogSerializer:
    def test_rejects_non_catalog_input(self) -> None:
        with pytest.raises(ModelBoundaryStaticFixtureCatalogError):
            serialize_model_boundary_static_fixture_catalog("not-a-catalog")  # type: ignore[arg-type]

    def test_returns_keys_in_exact_order(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        assert list(serialized.keys()) == [
            "catalog_ref",
            "catalog_label",
            "suite_refs",
            "metadata",
        ]

    def test_suite_refs_serialized_as_list(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        assert isinstance(serialized["suite_refs"], list)

    def test_omits_suites(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        assert "suites" not in serialized

    def test_omits_specs(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        assert "specs" not in serialized

    def test_omits_fixtures(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        assert "fixtures" not in serialized

    def test_omits_raw_captured_text(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        serialized_str = str(serialized)
        assert "raw_captured_text" not in serialized_str

    def test_omits_candidate_output(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        assert "candidate_output" not in serialized

    def test_omits_packet_payloads(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        serialized = serialize_model_boundary_static_fixture_catalog(catalog)
        serialized_str = str(serialized)
        assert "packet_payload" not in serialized_str
        assert "serialized_packet" not in serialized_str


# ---------------------------------------------------------------------------
# Orchestrator integration
# ---------------------------------------------------------------------------


class TestOrchestratorIntegration:
    def test_catalog_passes_to_orchestrator(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="catalog-test-run",
            run_label="Catalog Test Run",
            suites=list(catalog.suites),
        )
        assert result is not None

    def test_orchestrator_result_has_four_suite_refs(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="catalog-test-run",
            run_label="Catalog Test Run",
            suites=list(catalog.suites),
        )
        assert len(result.suite_refs) == 4

    def test_orchestrator_result_has_four_report_refs(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="catalog-test-run",
            run_label="Catalog Test Run",
            suites=list(catalog.suites),
        )
        assert len(result.report_refs) == 4

    def test_orchestrator_all_assertions_pass(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="catalog-test-run",
            run_label="Catalog Test Run",
            suites=list(catalog.suites),
        )
        assert result.run_snapshot.all_passed is True

    def test_orchestrator_hard_violation_suite_evaluates_failures(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="catalog-test-run",
            run_label="Catalog Test Run",
            suites=list(catalog.suites),
        )
        hard_report = result.report_snapshots[1]
        assert hard_report.suite_ref == "static-boundary-hard-violation-suite"
        assert hard_report.status_counts["failed"] == 3

    def test_orchestrator_mixed_suite_has_mixed_statuses(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="catalog-test-run",
            run_label="Catalog Test Run",
            suites=list(catalog.suites),
        )
        mixed_report = result.report_snapshots[3]
        assert mixed_report.suite_ref == "static-boundary-mixed-suite"
        assert mixed_report.status_counts["passed"] == 1
        assert mixed_report.status_counts["failed"] == 1
        assert mixed_report.status_counts["needs_review"] == 1

    def test_orchestrator_packet_warning_report_refs(self) -> None:
        catalog = create_model_boundary_static_fixture_catalog()
        result = run_model_boundary_captured_fixture_evaluation(
            run_ref="catalog-test-run",
            run_label="Catalog Test Run",
            suites=list(catalog.suites),
        )
        warning_report_refs = result.run_snapshot.packet_warning_report_refs
        warning_suite_refs = set()
        for report in result.report_snapshots:
            if report.report_ref in warning_report_refs:
                warning_suite_refs.add(report.suite_ref)
        assert "static-boundary-warning-suite" in warning_suite_refs
        assert "static-boundary-mixed-suite" in warning_suite_refs


# ---------------------------------------------------------------------------
# Source scan — forbidden imports/calls
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
    @pytest.fixture()
    def module_source(self) -> str:
        source_path = (
            Path(__file__).resolve().parent.parent
            / "src"
            / "astra_runtime"
            / "domain"
            / "model_boundary_evaluation.py"
        )
        return source_path.read_text(encoding="utf-8")

    @pytest.mark.parametrize("pattern", _FORBIDDEN_PATTERNS)
    def test_module_does_not_contain_forbidden_pattern(
        self, module_source: str, pattern: str
    ) -> None:
        assert pattern not in module_source, (
            f"Forbidden pattern {pattern!r} found in module source"
        )
