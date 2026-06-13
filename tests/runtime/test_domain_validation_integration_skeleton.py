"""Focused skeleton tests for validation integration domain module."""

from __future__ import annotations

import pathlib
from types import MappingProxyType
from typing import Mapping

import pytest

from astra_runtime.domain import (
    VALIDATION_DEPENDENCY_TYPES,
    VALIDATION_FAILURE_ROUTES,
    VALIDATION_INTEGRATION_DECISIONS,
    VALIDATION_INTEGRATION_STAGES,
    VALIDATION_INVARIANT_FAMILIES,
    VALIDATION_PUBLIC_REASON_CODES,
    VALIDATION_SUBJECT_TYPES,
    InvalidValidationFailureRouteError,
    InvalidValidationIntegrationDependencyError,
    InvalidValidationIntegrationRequestError,
    InvalidValidationIntegrationResultError,
    InvalidValidationInvariantDeclarationError,
    ValidationFailureRoute,
    ValidationIntegrationDependency,
    ValidationIntegrationError,
    ValidationIntegrationRequest,
    ValidationIntegrationResult,
    ValidationIntegrationService,
    ValidationInvariantDeclaration,
    create_validation_failure_route,
    create_validation_integration_dependency,
    create_validation_integration_request,
    create_validation_integration_result,
    create_validation_invariant_declaration,
    validate_validation_failure_route,
    validate_validation_integration_dependency,
    validate_validation_integration_request,
    validate_validation_integration_result,
    validate_validation_invariant_declaration,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DOMAIN_PACKAGE_DIR = REPO_ROOT / "src" / "astra_runtime" / "domain"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_dep(**kwargs):
    defaults = dict(
        dependency_id="dep-1",
        dependency_type="schema_registry_ref",
        reference_id="ref-1",
    )
    defaults.update(kwargs)
    return create_validation_integration_dependency(**defaults)


def _make_invariant(**kwargs):
    defaults = dict(
        invariant_id="inv-1",
        invariant_family="command_authority_invariant",
        subject_type="command",
        subject_ref_id="cmd-1",
    )
    defaults.update(kwargs)
    return create_validation_invariant_declaration(**defaults)


def _make_failure_route(**kwargs):
    defaults = dict(
        route_id="route-1",
        route_type="block_command_before_transaction",
        decision="rejected_by_missing_command_ref",
        subject_ref_id="cmd-1",
    )
    defaults.update(kwargs)
    return create_validation_failure_route(**defaults)


def _make_request(**kwargs):
    defaults = dict(
        validation_request_id="vreq-1",
        subject_type="command",
        subject_ref_id="cmd-1",
        requesting_service="command_lifecycle_service",
    )
    defaults.update(kwargs)
    return create_validation_integration_request(**defaults)


def _make_result_dependencies(validation_request_id="vreq-1", trace_id="trace-1", validation_result_ref_id="vres-1", provenance_ref_ids=()):
    dependencies = [
        _make_dep(
            dependency_id="dep-request",
            dependency_type="validation_request_ref",
            reference_id=validation_request_id,
            satisfied=True,
        ),
    ]
    if isinstance(trace_id, str) and trace_id.strip():
        dependencies.append(
            _make_dep(
                dependency_id="dep-trace",
                dependency_type="runtime_trace_ref",
                reference_id=trace_id,
                satisfied=True,
            )
        )
    if isinstance(validation_result_ref_id, str) and validation_result_ref_id.strip():
        dependencies.append(
            _make_dep(
                dependency_id="dep-result",
                dependency_type="validation_result_ref",
                reference_id=validation_result_ref_id,
                satisfied=True,
            )
        )
    for index, ref in enumerate(provenance_ref_ids or ()):
        if isinstance(ref, str) and ref.strip():
            dependencies.append(
                _make_dep(
                    dependency_id=f"dep-provenance-{index}",
                    dependency_type="generated_content_provenance_ref",
                    reference_id=ref,
                    satisfied=True,
                )
            )
    return tuple(dependencies)


def _make_result(**kwargs):
    defaults = dict(
        validation_request_id="vreq-1",
        decision="validation_failed",
        final_stage="validation_failed",
        subject_type="command",
        subject_ref_id="cmd-1",
        request_subject_type="command",
        request_subject_ref_id="cmd-1",
        validation_result_ref_id="vres-1",
        failure_routes=[_make_failure_route(decision="validation_failed")],
        trace_id="trace-1",
    )
    defaults.update(kwargs)
    if "request_subject_type" not in kwargs:
        defaults["request_subject_type"] = defaults["subject_type"]
    if "request_subject_ref_id" not in kwargs:
        defaults["request_subject_ref_id"] = defaults["subject_ref_id"]
    defaults.setdefault(
        "dependencies",
        _make_result_dependencies(
            defaults["validation_request_id"],
            defaults.get("trace_id"),
            defaults.get("validation_result_ref_id"),
            defaults.get("provenance_ref_ids", ()),
        ),
    )
    return create_validation_integration_result(**defaults)


# ---------------------------------------------------------------------------
# Constants tests
# ---------------------------------------------------------------------------


class TestValidationIntegrationStages:
    def test_all_20_stages_present(self):
        expected = {
            "validation_integration_requested",
            "validation_scope_declared",
            "dependency_refs_bound",
            "state_refs_bound",
            "transaction_refs_bound",
            "event_commitment_refs_bound",
            "invariant_set_declared",
            "invariant_precheck_requested",
            "invariant_precheck_passed",
            "invariant_precheck_failed",
            "domain_validation_required",
            "domain_validation_referenced",
            "hidden_info_safety_checked",
            "provenance_checked",
            "validation_passed",
            "validation_failed",
            "validation_quarantined",
            "validation_escalated",
            "validation_cancelled",
            "validation_superseded",
        }
        assert expected == set(VALIDATION_INTEGRATION_STAGES)
        assert len(VALIDATION_INTEGRATION_STAGES) == 20


class TestValidationIntegrationDecisions:
    def test_all_16_decisions_present(self):
        expected = {
            "validation_ready",
            "validation_passed",
            "validation_failed",
            "rejected_by_missing_command_ref",
            "rejected_by_missing_state_ref",
            "rejected_by_missing_transaction_ref",
            "rejected_by_missing_event_commitment_ref",
            "rejected_by_missing_invariant_set",
            "rejected_by_hidden_information_risk",
            "rejected_by_provenance_gap",
            "rejected_by_schema_mismatch",
            "rejected_by_authority_mismatch",
            "rejected_by_phase_boundary",
            "quarantined_for_review",
            "escalated_to_doctrine",
            "unsupported_validation_scope",
        }
        assert expected == set(VALIDATION_INTEGRATION_DECISIONS)
        assert len(VALIDATION_INTEGRATION_DECISIONS) == 16


class TestValidationInvariantFamilies:
    def test_all_21_families_present(self):
        expected = {
            "command_authority_invariant",
            "action_legality_invariant",
            "state_reference_invariant",
            "state_projection_visibility_invariant",
            "transaction_lifecycle_invariant",
            "event_commitment_invariant",
            "state_delta_shape_invariant",
            "event_ledger_shape_invariant",
            "validation_result_authority_invariant",
            "hidden_information_partition_invariant",
            "context_projection_visibility_invariant",
            "persistence_boundary_invariant",
            "replay_audit_invariant",
            "runtime_trace_invariant",
            "schema_record_shape_invariant",
            "source_local_authority_invariant",
            "generated_content_provenance_invariant",
            "canon_boundary_invariant",
            "conversion_boundary_invariant",
            "model_non_authority_invariant",
            "live_play_non_authority_invariant",
        }
        assert expected == set(VALIDATION_INVARIANT_FAMILIES)
        assert len(VALIDATION_INVARIANT_FAMILIES) == 21


class TestValidationFailureRoutes:
    def test_all_12_routes_present(self):
        expected = {
            "block_command_before_transaction",
            "block_transaction_before_commitment",
            "block_event_commitment",
            "quarantine_transaction",
            "quarantine_event_commitment",
            "quarantine_generated_content",
            "escalate_doctrine_gap",
            "reject_source_local_authority",
            "reject_hidden_info_leak",
            "reject_schema_mismatch",
            "reject_phase_boundary_violation",
            "request_downstream_domain_validation",
        }
        assert expected == set(VALIDATION_FAILURE_ROUTES)
        assert len(VALIDATION_FAILURE_ROUTES) == 12


class TestValidationDependencyTypes:
    def test_all_28_types_present(self):
        expected = {
            "schema_registry_ref",
            "record_identity_ref",
            "command_envelope_ref",
            "command_lifecycle_ref",
            "action_legality_ref",
            "state_record_ref",
            "state_snapshot_ref",
            "state_projection_ref",
            "transaction_ref",
            "transaction_plan_ref",
            "transaction_result_ref",
            "event_commitment_request_ref",
            "event_commitment_result_ref",
            "state_delta_ref",
            "event_ledger_ref",
            "validation_pipeline_ref",
            "validation_request_ref",
            "validation_result_ref",
            "invariant_precheck_ref",
            "hidden_information_ref",
            "context_projection_ref",
            "persistence_boundary_ref",
            "replay_audit_ref",
            "runtime_trace_ref",
            "generated_content_provenance_ref",
            "source_local_ref",
            "canon_boundary_ref",
            "conversion_boundary_ref",
        }
        assert expected == set(VALIDATION_DEPENDENCY_TYPES)
        assert len(VALIDATION_DEPENDENCY_TYPES) == 28


class TestValidationSubjectTypes:
    def test_all_15_types_present(self):
        expected = {
            "command",
            "action_legality",
            "state_record",
            "state_projection",
            "transaction",
            "event_commitment",
            "state_delta",
            "event_ledger",
            "generated_content",
            "source_local_content",
            "canon_reference",
            "conversion_artifact",
            "hidden_information",
            "context_projection",
            "runtime_trace",
        }
        assert expected == set(VALIDATION_SUBJECT_TYPES)
        assert len(VALIDATION_SUBJECT_TYPES) == 15


# ---------------------------------------------------------------------------
# Import/export integrity
# ---------------------------------------------------------------------------


class TestDomainImports:
    def test_validation_integration_symbols_importable(self):
        assert VALIDATION_INTEGRATION_STAGES is not None
        assert VALIDATION_INTEGRATION_DECISIONS is not None
        assert VALIDATION_INVARIANT_FAMILIES is not None
        assert VALIDATION_FAILURE_ROUTES is not None
        assert VALIDATION_DEPENDENCY_TYPES is not None
        assert VALIDATION_SUBJECT_TYPES is not None
        assert ValidationIntegrationDependency is not None
        assert ValidationInvariantDeclaration is not None
        assert ValidationFailureRoute is not None
        assert ValidationIntegrationRequest is not None
        assert ValidationIntegrationResult is not None
        assert ValidationIntegrationService is not None
        assert ValidationIntegrationError is not None
        assert InvalidValidationIntegrationDependencyError is not None
        assert InvalidValidationInvariantDeclarationError is not None
        assert InvalidValidationIntegrationRequestError is not None
        assert InvalidValidationIntegrationResultError is not None
        assert InvalidValidationFailureRouteError is not None


# ---------------------------------------------------------------------------
# Dependency tests
# ---------------------------------------------------------------------------


class TestValidationIntegrationDependency:
    def test_valid_creation(self):
        d = _make_dep()
        assert d.dependency_id == "dep-1"
        assert d.dependency_type == "schema_registry_ref"
        assert d.reference_id == "ref-1"
        assert d.required is True
        assert d.satisfied is False
        assert d.hidden_info_safe is True

    @pytest.mark.parametrize("dep_type", sorted(VALIDATION_DEPENDENCY_TYPES))
    def test_all_dependency_types_accepted(self, dep_type):
        d = _make_dep(dependency_type=dep_type)
        assert d.dependency_type == dep_type

    def test_invalid_dependency_type_rejected(self):
        with pytest.raises(InvalidValidationIntegrationDependencyError):
            _make_dep(dependency_type="magic_ref")

    def test_empty_dependency_id_rejected(self):
        with pytest.raises(InvalidValidationIntegrationDependencyError):
            _make_dep(dependency_id="")

    def test_empty_reference_id_rejected(self):
        with pytest.raises(InvalidValidationIntegrationDependencyError):
            _make_dep(reference_id="")

    def test_non_bool_required_rejected(self):
        with pytest.raises(InvalidValidationIntegrationDependencyError):
            _make_dep(required="yes")

    def test_metadata_deep_copy_safe(self):
        m = {"key": [1, 2]}
        d = _make_dep(metadata=m)
        m["key"].append(99)
        assert 99 not in d.metadata.get("key", [])

    def test_to_dict_returns_copy(self):
        d = _make_dep(metadata={"k": [1]})
        out = d.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in d.to_dict()["metadata"]["k"]

    def test_frozen(self):
        d = _make_dep()
        with pytest.raises((AttributeError, TypeError)):
            d.dependency_id = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_validation_integration_dependency(_make_dep()) is True

    def test_validate_rejects_invalid(self):
        assert validate_validation_integration_dependency("not a dep") is False


# ---------------------------------------------------------------------------
# Invariant declaration tests
# ---------------------------------------------------------------------------


class TestValidationInvariantDeclaration:
    def test_valid_creation(self):
        inv = _make_invariant()
        assert inv.invariant_id == "inv-1"
        assert inv.invariant_family == "command_authority_invariant"
        assert inv.subject_type == "command"
        assert inv.subject_ref_id == "cmd-1"
        assert inv.required is True
        assert inv.blocking is True
        assert inv.backend_only is True
        assert inv.hidden_info_safe is True
        assert inv.provenance_required is False

    @pytest.mark.parametrize("family", sorted(VALIDATION_INVARIANT_FAMILIES))
    def test_all_invariant_families_accepted(self, family):
        extra = {}
        if family == "generated_content_provenance_invariant":
            extra["provenance_required"] = True
        inv = _make_invariant(invariant_family=family, **extra)
        assert inv.invariant_family == family

    def test_invalid_invariant_family_rejected(self):
        with pytest.raises(InvalidValidationInvariantDeclarationError):
            _make_invariant(invariant_family="fake_invariant")

    def test_invalid_subject_type_rejected(self):
        with pytest.raises(InvalidValidationInvariantDeclarationError):
            _make_invariant(subject_type="invalid_subject")

    def test_empty_invariant_id_rejected(self):
        with pytest.raises(InvalidValidationInvariantDeclarationError):
            _make_invariant(invariant_id="")

    def test_empty_subject_ref_id_rejected(self):
        with pytest.raises(InvalidValidationInvariantDeclarationError):
            _make_invariant(subject_ref_id="")

    def test_backend_only_false_rejected(self):
        with pytest.raises(InvalidValidationInvariantDeclarationError):
            _make_invariant(backend_only=False)

    def test_generated_content_provenance_requires_provenance(self):
        with pytest.raises(InvalidValidationInvariantDeclarationError):
            _make_invariant(
                invariant_family="generated_content_provenance_invariant",
                provenance_required=False,
            )

    def test_generated_content_provenance_with_provenance_accepted(self):
        inv = _make_invariant(
            invariant_family="generated_content_provenance_invariant",
            provenance_required=True,
        )
        assert inv.provenance_required is True

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1]}
        inv = _make_invariant(metadata=m)
        m["x"].append(99)
        assert 99 not in inv.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        inv = _make_invariant(metadata={"k": [1]})
        out = inv.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in inv.to_dict()["metadata"]["k"]

    def test_frozen(self):
        inv = _make_invariant()
        with pytest.raises((AttributeError, TypeError)):
            inv.invariant_id = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_validation_invariant_declaration(_make_invariant()) is True

    def test_validate_rejects_invalid(self):
        assert validate_validation_invariant_declaration("not an invariant") is False


# ---------------------------------------------------------------------------
# Failure route tests
# ---------------------------------------------------------------------------


class TestValidationFailureRoute:
    def test_valid_creation(self):
        r = _make_failure_route()
        assert r.route_id == "route-1"
        assert r.route_type == "block_command_before_transaction"
        assert r.decision == "rejected_by_missing_command_ref"
        assert r.subject_ref_id == "cmd-1"
        assert r.blocking is True
        assert r.quarantines is False
        assert r.escalates is False
        assert r.player_visible is False
        assert r.hidden_info_safe is True
        assert r.trace_required is True

    def test_invalid_route_type_rejected(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(route_type="invalid_route")

    def test_invalid_decision_rejected(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(decision="invalid_decision")

    def test_empty_route_id_rejected(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(route_id="")

    def test_empty_subject_ref_id_rejected(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(subject_ref_id="")

    def test_validation_passed_decision_rejected(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(decision="validation_passed")

    def test_player_visible_requires_hidden_info_safe(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(player_visible=True, hidden_info_safe=False)

    def test_player_visible_with_hidden_info_safe_accepted(self):
        r = _make_failure_route(
            player_visible=True,
            hidden_info_safe=True,
            public_reason_code="validation_rejected",
        )
        assert r.player_visible is True
        assert r.hidden_info_safe is True

    def test_quarantine_route_requires_quarantines_true(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(
                route_type="quarantine_transaction",
                decision="quarantined_for_review",
                quarantines=False,
            )

    def test_quarantine_route_accepted_with_quarantines_true(self):
        r = _make_failure_route(
            route_type="quarantine_transaction",
            decision="quarantined_for_review",
            quarantines=True,
        )
        assert r.quarantines is True

    def test_doctrine_escalation_requires_escalates_true(self):
        with pytest.raises(InvalidValidationFailureRouteError):
            _make_failure_route(
                route_type="escalate_doctrine_gap",
                decision="escalated_to_doctrine",
                escalates=False,
            )

    def test_doctrine_escalation_accepted_with_escalates_true(self):
        r = _make_failure_route(
            route_type="escalate_doctrine_gap",
            decision="escalated_to_doctrine",
            escalates=True,
        )
        assert r.escalates is True

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1]}
        r = _make_failure_route(metadata=m)
        m["x"].append(99)
        assert 99 not in r.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        r = _make_failure_route(metadata={"k": [1]})
        out = r.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in r.to_dict()["metadata"]["k"]

    def test_frozen(self):
        r = _make_failure_route()
        with pytest.raises((AttributeError, TypeError)):
            r.route_id = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_validation_failure_route(_make_failure_route()) is True

    def test_validate_rejects_invalid(self):
        assert validate_validation_failure_route("not a route") is False


# ---------------------------------------------------------------------------
# Request tests
# ---------------------------------------------------------------------------


class TestValidationIntegrationRequest:
    def test_valid_creation(self):
        r = _make_request()
        assert r.validation_request_id == "vreq-1"
        assert r.subject_type == "command"
        assert r.subject_ref_id == "cmd-1"
        assert r.requesting_service == "command_lifecycle_service"
        assert r.requested_stage == "validation_integration_requested"
        assert r.dependencies == ()
        assert r.invariants == ()

    def test_empty_ids_rejected(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(validation_request_id="")
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(subject_ref_id="")
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(requesting_service="")

    def test_invalid_subject_type_rejected(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(subject_type="invalid")

    def test_invalid_requested_stage_rejected(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(requested_stage="invalid_stage")

    def test_transaction_subject_requires_transaction_ref(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(subject_type="transaction", transaction_ref_id=None)

    def test_transaction_subject_with_ref_accepted(self):
        r = _make_request(subject_type="transaction", transaction_ref_id="txn-1")
        assert r.transaction_ref_id == "txn-1"

    def test_event_commitment_subject_requires_event_commitment_ref(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(subject_type="event_commitment", event_commitment_ref_id=None)

    def test_event_commitment_subject_with_ref_accepted(self):
        r = _make_request(subject_type="event_commitment", event_commitment_ref_id="ec-1")
        assert r.event_commitment_ref_id == "ec-1"

    def test_generated_content_provenance_invariant_requires_gen_refs(self):
        inv = _make_invariant(
            invariant_family="generated_content_provenance_invariant",
            provenance_required=True,
            subject_type="generated_content",
            subject_ref_id="gen-1",
        )
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(
                subject_type="generated_content",
                subject_ref_id="gen-1",
                invariants=[inv],
                generated_content_ref_ids=[],
            )

    def test_generated_content_provenance_invariant_with_gen_refs_accepted(self):
        inv = _make_invariant(
            invariant_family="generated_content_provenance_invariant",
            provenance_required=True,
            subject_type="generated_content",
            subject_ref_id="gen-1",
        )
        r = _make_request(
            subject_type="generated_content",
            subject_ref_id="gen-1",
            invariants=[inv],
            generated_content_ref_ids=["gen-ref-1"],
        )
        assert len(r.invariants) == 1

    def test_dependencies_accept_valid_list(self):
        dep = _make_dep()
        r = _make_request(dependencies=[dep])
        assert len(r.dependencies) == 1
        assert isinstance(r.dependencies, tuple)

    def test_dependencies_reject_bare_string(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(dependencies="dep-1")

    def test_invariants_reject_bare_string(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(invariants="inv-1")

    def test_state_ref_ids_reject_bare_string(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(state_ref_ids="ref-1")

    def test_tuple_fields_normalized(self):
        r = _make_request(state_ref_ids=["a"], projection_ref_ids=["b"])
        assert isinstance(r.state_ref_ids, tuple)
        assert isinstance(r.projection_ref_ids, tuple)

    def test_invalid_tuple_contents_rejected(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(state_ref_ids=[""])

    def test_optional_id_empty_string_rejected(self):
        with pytest.raises(InvalidValidationIntegrationRequestError):
            _make_request(trace_id="")

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1]}
        r = _make_request(metadata=m)
        m["x"].append(99)
        assert 99 not in r.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        r = _make_request(metadata={"k": [1]})
        out = r.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in r.to_dict()["metadata"]["k"]

    def test_frozen(self):
        r = _make_request()
        with pytest.raises((AttributeError, TypeError)):
            r.subject_type = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_validation_integration_request(_make_request()) is True

    def test_validate_rejects_invalid(self):
        assert validate_validation_integration_request("not a request") is False


# ---------------------------------------------------------------------------
# Result tests
# ---------------------------------------------------------------------------


class TestValidationIntegrationResult:
    def test_valid_creation(self):
        r = _make_result()
        assert r.validation_request_id == "vreq-1"
        assert r.decision == "validation_failed"
        assert r.final_stage == "validation_failed"
        assert r.passed is False
        assert r.state_mutation_allowed is False
        assert r.event_append_allowed is False
        assert r.persistence_allowed is False
        assert r.model_authority_allowed is False

    def test_validation_passed_result(self):
        r = _make_result(
            decision="validation_passed",
            final_stage="validation_passed",
            failure_routes=[],
            passed=True,
            blocking=False,
        )
        assert r.passed is True
        assert r.decision == "validation_passed"

    def test_validation_passed_cannot_have_failure_routes(self):
        route = _make_failure_route()
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(
                decision="validation_passed",
                final_stage="validation_passed",
                passed=True,
                blocking=False,
                failure_routes=[route],
            )

    def test_validation_passed_requires_passed_true(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(
                decision="validation_passed",
                final_stage="validation_passed",
                passed=False,
            )

    def test_non_passed_decision_requires_passed_false(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(
                decision="validation_failed",
                final_stage="validation_failed",
                passed=True,
            )

    def test_rejected_decision_requires_failure_routes(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(
                decision="rejected_by_missing_command_ref",
                final_stage="validation_failed",
                failure_routes=[],
            )

    def test_rejected_decision_with_routes_accepted(self):
        route = _make_failure_route()
        r = _make_result(
            decision="rejected_by_missing_command_ref",
            final_stage="validation_failed",
            failure_routes=[route],
        )
        assert len(r.failure_routes) == 1

    def test_quarantined_decision_requires_quarantined_true(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(
                decision="quarantined_for_review",
                final_stage="validation_quarantined",
                quarantined=False,
            )

    def test_quarantined_decision_accepted(self):
        r = _make_result(
            decision="quarantined_for_review",
            final_stage="validation_quarantined",
            failure_routes=[_make_failure_route(
                route_type="quarantine_transaction",
                decision="quarantined_for_review",
                quarantines=True,
            )],
            quarantined=True,
        )
        assert r.quarantined is True

    def test_escalated_decision_requires_escalated_true(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(
                decision="escalated_to_doctrine",
                final_stage="validation_escalated",
                escalated=False,
            )

    def test_escalated_decision_accepted(self):
        r = _make_result(
            decision="escalated_to_doctrine",
            final_stage="validation_escalated",
            failure_routes=[_make_failure_route(
                route_type="escalate_doctrine_gap",
                decision="escalated_to_doctrine",
                escalates=True,
            )],
            escalated=True,
        )
        assert r.escalated is True

    def test_hidden_info_safe_false_cannot_pass(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(
                decision="validation_passed",
                final_stage="validation_passed",
                failure_routes=[],
                passed=True,
                blocking=False,
                hidden_info_safe=False,
            )

    def test_state_mutation_allowed_true_rejected(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(state_mutation_allowed=True)

    def test_event_append_allowed_true_rejected(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(event_append_allowed=True)

    def test_persistence_allowed_true_rejected(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(persistence_allowed=True)

    def test_model_authority_allowed_true_rejected(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(model_authority_allowed=True)

    def test_invalid_decision_rejected(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(decision="bad_decision")

    def test_invalid_final_stage_rejected(self):
        with pytest.raises(InvalidValidationIntegrationResultError):
            _make_result(final_stage="bad_stage")

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1]}
        r = _make_result(metadata=m)
        m["x"].append(99)
        assert 99 not in r.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        r = _make_result(metadata={"k": [1]})
        out = r.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in r.to_dict()["metadata"]["k"]

    def test_frozen(self):
        r = _make_result()
        with pytest.raises((AttributeError, TypeError)):
            r.decision = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_validation_integration_result(_make_result()) is True

    def test_validate_rejects_invalid(self):
        assert validate_validation_integration_result("not a result") is False


# ---------------------------------------------------------------------------
# Validator parity — manually constructed invalid frozen objects
# ---------------------------------------------------------------------------


class TestValidatorParityValidationIntegration:
    def test_validate_dependency_rejects_empty_dependency_id(self):
        bad = ValidationIntegrationDependency(
            dependency_id="", dependency_type="schema_registry_ref",
            reference_id="ref-1", required=True, satisfied=False,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_dependency(bad) is False

    def test_validate_dependency_rejects_invalid_type(self):
        bad = ValidationIntegrationDependency(
            dependency_id="dep-1", dependency_type="bad_type",
            reference_id="ref-1", required=True, satisfied=False,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_dependency(bad) is False

    def test_validate_invariant_rejects_backend_only_false(self):
        bad = ValidationInvariantDeclaration(
            invariant_id="inv-1", invariant_family="command_authority_invariant",
            subject_type="command", subject_ref_id="cmd-1",
            required=True, blocking=True, backend_only=False,
            hidden_info_safe=True, provenance_required=False,
            metadata=MappingProxyType({}),
        )
        assert validate_validation_invariant_declaration(bad) is False

    def test_validate_invariant_rejects_provenance_mismatch(self):
        bad = ValidationInvariantDeclaration(
            invariant_id="inv-1",
            invariant_family="generated_content_provenance_invariant",
            subject_type="generated_content", subject_ref_id="gen-1",
            required=True, blocking=True, backend_only=True,
            hidden_info_safe=True, provenance_required=False,
            metadata=MappingProxyType({}),
        )
        assert validate_validation_invariant_declaration(bad) is False

    def test_validate_failure_route_rejects_passed_decision(self):
        bad = ValidationFailureRoute(
            route_id="route-1",
            route_type="block_command_before_transaction",
            decision="validation_passed",
            subject_ref_id="cmd-1",
            blocking=True, quarantines=False, escalates=False,
            player_visible=False, hidden_info_safe=True,
            trace_required=True, metadata=MappingProxyType({}),
        )
        assert validate_validation_failure_route(bad) is False

    def test_validate_failure_route_rejects_player_visible_without_hidden_safe(self):
        bad = ValidationFailureRoute(
            route_id="route-1",
            route_type="block_command_before_transaction",
            decision="rejected_by_missing_command_ref",
            subject_ref_id="cmd-1",
            blocking=True, quarantines=False, escalates=False,
            player_visible=True, hidden_info_safe=False,
            trace_required=True, metadata=MappingProxyType({}),
        )
        assert validate_validation_failure_route(bad) is False

    def test_validate_failure_route_rejects_quarantine_without_flag(self):
        bad = ValidationFailureRoute(
            route_id="route-1",
            route_type="quarantine_transaction",
            decision="quarantined_for_review",
            subject_ref_id="cmd-1",
            blocking=True, quarantines=False, escalates=False,
            player_visible=False, hidden_info_safe=True,
            trace_required=True, metadata=MappingProxyType({}),
        )
        assert validate_validation_failure_route(bad) is False

    def test_validate_failure_route_rejects_escalation_without_flag(self):
        bad = ValidationFailureRoute(
            route_id="route-1",
            route_type="escalate_doctrine_gap",
            decision="escalated_to_doctrine",
            subject_ref_id="cmd-1",
            blocking=True, quarantines=False, escalates=False,
            player_visible=False, hidden_info_safe=True,
            trace_required=True, metadata=MappingProxyType({}),
        )
        assert validate_validation_failure_route(bad) is False

    def test_validate_request_rejects_transaction_without_ref(self):
        bad = ValidationIntegrationRequest(
            validation_request_id="vreq-1",
            subject_type="transaction",
            subject_ref_id="txn-1",
            requesting_service="svc",
            requested_stage="validation_integration_requested",
            dependencies=(), invariants=(),
            transaction_ref_id=None, event_commitment_ref_id=None,
            state_ref_ids=(), projection_ref_ids=(),
            validation_pipeline_ref_id=None,
            hidden_information_ref_ids=(),
            generated_content_ref_ids=(),
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_request(bad) is False

    def test_validate_request_rejects_event_commitment_without_ref(self):
        bad = ValidationIntegrationRequest(
            validation_request_id="vreq-1",
            subject_type="event_commitment",
            subject_ref_id="ec-1",
            requesting_service="svc",
            requested_stage="validation_integration_requested",
            dependencies=(), invariants=(),
            transaction_ref_id=None, event_commitment_ref_id=None,
            state_ref_ids=(), projection_ref_ids=(),
            validation_pipeline_ref_id=None,
            hidden_information_ref_ids=(),
            generated_content_ref_ids=(),
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_request(bad) is False

    def test_validate_result_rejects_state_mutation_allowed(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="validation_failed",
            final_stage="validation_failed",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=True,
            event_append_allowed=False,
            persistence_allowed=False,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_event_append_allowed(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="validation_failed",
            final_stage="validation_failed",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=True,
            persistence_allowed=False,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_persistence_allowed(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="validation_failed",
            final_stage="validation_failed",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=False,
            persistence_allowed=True,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_model_authority_allowed(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="validation_failed",
            final_stage="validation_failed",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=False,
            persistence_allowed=False,
            model_authority_allowed=True,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_passed_with_wrong_decision(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="validation_failed",
            final_stage="validation_failed",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=True, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=False,
            persistence_allowed=False,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_passed_decision_without_passed_flag(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="validation_passed",
            final_stage="validation_passed",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=False,
            persistence_allowed=False,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_rejected_without_routes(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="rejected_by_missing_command_ref",
            final_stage="validation_failed",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=False,
            persistence_allowed=False,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_quarantined_without_flag(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="quarantined_for_review",
            final_stage="validation_quarantined",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=False,
            persistence_allowed=False,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False

    def test_validate_result_rejects_escalated_without_flag(self):
        bad = ValidationIntegrationResult(
            validation_request_id="vreq-1",
            decision="escalated_to_doctrine",
            final_stage="validation_escalated",
            subject_type="command",
            subject_ref_id="cmd-1",
            validation_result_ref_id=None,
            invariant_precheck_ref_id=None,
            failure_routes=(),
            passed=False, blocking=True, quarantined=False, escalated=False,
            hidden_info_safe=True, provenance_checked=False,
            provenance_ref_ids=(),
            state_mutation_allowed=False,
            event_append_allowed=False,
            persistence_allowed=False,
            model_authority_allowed=False,
            trace_id=None, metadata=MappingProxyType({}),
        )
        assert validate_validation_integration_result(bad) is False


# ---------------------------------------------------------------------------
# Service tests
# ---------------------------------------------------------------------------


class TestValidationIntegrationService:
    def test_service_is_stateless(self):
        svc = ValidationIntegrationService()
        assert svc.__dict__ == {}

    def test_service_delegates_create_dependency(self):
        svc = ValidationIntegrationService()
        d = svc.create_dependency(
            dependency_id="dep-1", dependency_type="schema_registry_ref",
            reference_id="ref-1",
        )
        assert isinstance(d, ValidationIntegrationDependency)

    def test_service_delegates_create_invariant_declaration(self):
        svc = ValidationIntegrationService()
        inv = svc.create_invariant_declaration(
            invariant_id="inv-1",
            invariant_family="command_authority_invariant",
            subject_type="command",
            subject_ref_id="cmd-1",
        )
        assert isinstance(inv, ValidationInvariantDeclaration)

    def test_service_delegates_create_failure_route(self):
        svc = ValidationIntegrationService()
        r = svc.create_failure_route(
            route_id="route-1",
            route_type="block_command_before_transaction",
            decision="rejected_by_missing_command_ref",
            subject_ref_id="cmd-1",
        )
        assert isinstance(r, ValidationFailureRoute)

    def test_service_delegates_create_request(self):
        svc = ValidationIntegrationService()
        r = svc.create_request(
            validation_request_id="vreq-1",
            subject_type="command",
            subject_ref_id="cmd-1",
            requesting_service="command_lifecycle_service",
        )
        assert isinstance(r, ValidationIntegrationRequest)

    def test_service_delegates_create_result(self):
        svc = ValidationIntegrationService()
        r = svc.create_result(
            validation_request_id="vreq-1",
            decision="validation_failed",
            final_stage="validation_failed",
            subject_type="command",
            subject_ref_id="cmd-1",
            request_subject_type="command",
            request_subject_ref_id="cmd-1",
            validation_result_ref_id="vres-1",
            dependencies=_make_result_dependencies(),
            failure_routes=[_make_failure_route(decision="validation_failed")],
            trace_id="trace-1",
        )
        assert isinstance(r, ValidationIntegrationResult)

    def test_service_delegates_validate(self):
        svc = ValidationIntegrationService()
        assert svc.validate_dependency(_make_dep()) is True
        assert svc.validate_invariant_declaration(_make_invariant()) is True
        assert svc.validate_failure_route(_make_failure_route()) is True
        assert svc.validate_request(_make_request()) is True
        assert svc.validate_result(_make_result()) is True

    def test_service_has_no_forbidden_methods(self):
        forbidden = [
            "execute", "run", "mutate", "apply", "apply_delta",
            "commit", "append", "persist", "save", "load",
            "replay", "rollback", "resolve", "roll", "narrate",
            "prompt", "model", "enforce", "evaluate_rules",
            "run_validation_checks", "run_invariant_prechecks",
        ]
        svc_methods = [m for m in dir(ValidationIntegrationService) if not m.startswith("_")]
        for method_name in forbidden:
            assert method_name not in svc_methods, f"Forbidden method found: {method_name}"

    def test_no_mutation_methods(self):
        mutation = [
            "mutate_state", "apply_delta", "commit_event",
            "append_event", "store", "persist", "enforce_invariant",
        ]
        for m in mutation:
            assert not hasattr(ValidationIntegrationService, m)


# ---------------------------------------------------------------------------
# Guardrail tests
# ---------------------------------------------------------------------------


class TestGuardrailsDomainPackage:
    def test_domain_package_contains_only_authorized_files(self):
        authorized = {
            "__init__.py",
            "command_lifecycle.py",
            "action_legality.py",
            "state_store.py",
            "state_projection.py",
            "transaction_lifecycle.py",
            "event_commitment.py",
            "validation_integration.py",
            "resource_consequence_math.py",
            "context_packet_compiler.py",
            "__pycache__",
        }
        entries = {p.name for p in DOMAIN_PACKAGE_DIR.iterdir()}
        unauthorized = entries - authorized
        assert not unauthorized, f"Unauthorized domain files found: {unauthorized}"

    @pytest.mark.parametrize(
        "forbidden_file",
        [
            "resource_math.py",
            "combat.py",
            "ability_effects.py",
            "inventory.py",
            "mission.py",
            "social_faction.py",
            "generated_content.py",
        ],
    )
    def test_no_unauthorized_domain_module(self, forbidden_file):
        assert not (DOMAIN_PACKAGE_DIR / forbidden_file).exists()

    @pytest.mark.parametrize(
        "forbidden_path",
        [
            "src/astra_runtime/kernel/context_packet_compiler.py",
            "src/astra_runtime/model",
            "src/astra_runtime/prompts",
            "src/astra_runtime/live_play",
            "src/astra_runtime/ui",
            "src/astra_runtime/database",
            "src/astra_runtime/store",
        ],
    )
    def test_no_unauthorized_package(self, forbidden_path):
        full_path = REPO_ROOT / forbidden_path
        assert not full_path.exists(), f"Unauthorized path must not exist: {forbidden_path}"


# ---------------------------------------------------------------------------
# Tracking tests
# ---------------------------------------------------------------------------


class TestDecisionLogTracking:
    def test_pr4a_id_appears_in_decision_log(self):
        path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        content = path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-PR-4A" in content


class TestRegistryTracking:
    def test_pr4a_file_id_appears_in_registry(self):
        path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        content = path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-PR-4A-VALIDATION-INTEGRATION-INVARIANT-ENFORCEMENT-SKELETON-IMPLEMENTATION-001" in content
