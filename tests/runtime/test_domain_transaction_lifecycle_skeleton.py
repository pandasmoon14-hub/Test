"""Focused skeleton tests for transaction lifecycle domain module."""

from __future__ import annotations

import os
import pathlib
from types import MappingProxyType
from typing import Mapping

import pytest

from astra_runtime.domain import (
    TRANSACTION_DECISIONS,
    TRANSACTION_DEPENDENCY_TYPES,
    TRANSACTION_LIFECYCLE_STAGES,
    TRANSACTION_PRECONDITION_TYPES,
    InvalidTransactionDependencyError,
    InvalidTransactionPlanError,
    InvalidTransactionPreconditionError,
    InvalidTransactionRequestError,
    InvalidTransactionResultError,
    TransactionDependency,
    TransactionLifecycleError,
    TransactionLifecycleService,
    TransactionPlan,
    TransactionPrecondition,
    TransactionRequest,
    TransactionResult,
    create_transaction_dependency,
    create_transaction_plan,
    create_transaction_precondition,
    create_transaction_request,
    create_transaction_result,
    validate_transaction_dependency,
    validate_transaction_plan,
    validate_transaction_precondition,
    validate_transaction_request,
    validate_transaction_result,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DOMAIN_PACKAGE_DIR = REPO_ROOT / "src" / "astra_runtime" / "domain"


def _make_dep(**kwargs):
    defaults = dict(
        dependency_id="dep-1",
        dependency_type="command_envelope_ref",
        reference_id="ref-1",
    )
    defaults.update(kwargs)
    return create_transaction_dependency(**defaults)


def _make_precond(**kwargs):
    defaults = dict(
        precondition_id="pre-1",
        precondition_type="accepted_command_required",
        satisfied=True,
    )
    defaults.update(kwargs)
    return create_transaction_precondition(**defaults)


def _make_request(**kwargs):
    defaults = dict(
        transaction_id="txn-1",
        command_envelope_id="cmd-1",
        actor_ref_id="actor-1",
    )
    defaults.update(kwargs)
    return create_transaction_request(**defaults)


def _make_plan(**kwargs):
    defaults = dict(
        transaction_id="txn-1",
        current_stage="transaction_requested",
        decision="accepted_for_planning",
    )
    defaults.update(kwargs)
    return create_transaction_plan(**defaults)


def _make_result(**kwargs):
    defaults = dict(
        transaction_id="txn-1",
        final_stage="rejected",
        decision="rejected_by_scope",
        accepted_for_commitment=False,
    )
    defaults.update(kwargs)
    return create_transaction_result(**defaults)


class TestDomainImports:
    def test_transaction_lifecycle_symbols_importable(self):
        assert TRANSACTION_LIFECYCLE_STAGES is not None
        assert TRANSACTION_DECISIONS is not None
        assert TRANSACTION_DEPENDENCY_TYPES is not None
        assert TRANSACTION_PRECONDITION_TYPES is not None
        assert TransactionDependency is not None
        assert TransactionPrecondition is not None
        assert TransactionRequest is not None
        assert TransactionPlan is not None
        assert TransactionResult is not None
        assert TransactionLifecycleService is not None
        assert TransactionLifecycleError is not None


class TestTransactionLifecycleStages:
    def test_all_18_stages_present(self):
        expected = {
            "transaction_requested", "command_reference_bound", "actor_reference_bound",
            "state_projection_bound", "dependencies_declared", "preconditions_declared",
            "domain_resolution_required", "proposed_delta_referenced",
            "validation_requested", "validation_passed", "validation_failed",
            "ready_for_event_commitment", "commitment_requested", "committed",
            "rejected", "quarantined", "cancelled", "superseded",
        }
        assert expected == set(TRANSACTION_LIFECYCLE_STAGES)
        assert len(TRANSACTION_LIFECYCLE_STAGES) == 18


class TestTransactionDecisions:
    def test_all_13_decisions_present(self):
        expected = {
            "accepted_for_planning", "requires_domain_resolution", "requires_validation",
            "ready_for_event_commitment", "rejected_by_missing_command",
            "rejected_by_missing_actor", "rejected_by_missing_state_reference",
            "rejected_by_missing_validation", "rejected_by_scope",
            "rejected_by_hidden_information_risk", "quarantined_for_audit",
            "cancelled", "superseded",
        }
        assert expected == set(TRANSACTION_DECISIONS)
        assert len(TRANSACTION_DECISIONS) == 13


class TestTransactionDependencyTypes:
    def test_all_23_types_present(self):
        expected = {
            "command_envelope_ref", "command_lifecycle_ref", "action_legality_ref",
            "actor_ref", "state_record_ref", "state_snapshot_ref", "state_projection_ref",
            "proposed_delta_ref", "validation_result_ref", "hidden_information_ref",
            "context_projection_ref", "runtime_trace_ref", "event_commitment_ref",
            "persistence_boundary_ref", "replay_audit_ref", "domain_resolution_ref",
            "resource_resolution_ref", "combat_resolution_ref", "ability_resolution_ref",
            "inventory_resolution_ref", "mission_resolution_ref", "social_resolution_ref",
            "generated_content_provenance_ref",
        }
        assert expected == set(TRANSACTION_DEPENDENCY_TYPES)
        assert len(TRANSACTION_DEPENDENCY_TYPES) == 23


class TestTransactionPreconditionTypes:
    def test_all_14_types_present(self):
        expected = {
            "accepted_command_required", "actor_reference_required",
            "state_reference_required", "projection_reference_required",
            "legality_result_required", "domain_resolution_required",
            "proposed_delta_required", "validation_required",
            "hidden_information_safe_required", "trace_required",
            "event_commitment_ready_required", "idempotency_key_required",
            "persistence_boundary_required", "replay_audit_required",
        }
        assert expected == set(TRANSACTION_PRECONDITION_TYPES)
        assert len(TRANSACTION_PRECONDITION_TYPES) == 14


class TestTransactionDependency:
    def test_valid_creation(self):
        d = _make_dep()
        assert d.dependency_id == "dep-1"
        assert d.dependency_type == "command_envelope_ref"
        assert d.reference_id == "ref-1"
        assert d.required is True
        assert d.satisfied is False
        assert d.hidden_info_safe is True

    @pytest.mark.parametrize("dep_type", sorted(TRANSACTION_DEPENDENCY_TYPES))
    def test_all_dependency_types_accepted(self, dep_type):
        d = _make_dep(dependency_type=dep_type)
        assert d.dependency_type == dep_type

    def test_invalid_dependency_type_rejected(self):
        with pytest.raises(InvalidTransactionDependencyError):
            _make_dep(dependency_type="magic_ref")

    def test_empty_dependency_id_rejected(self):
        with pytest.raises(InvalidTransactionDependencyError):
            _make_dep(dependency_id="")

    def test_empty_reference_id_rejected(self):
        with pytest.raises(InvalidTransactionDependencyError):
            _make_dep(reference_id="")

    def test_non_bool_required_rejected(self):
        with pytest.raises(InvalidTransactionDependencyError):
            _make_dep(required="yes")

    def test_non_bool_satisfied_rejected(self):
        with pytest.raises(InvalidTransactionDependencyError):
            _make_dep(satisfied=1)

    def test_non_bool_hidden_info_safe_rejected(self):
        with pytest.raises(InvalidTransactionDependencyError):
            _make_dep(hidden_info_safe="true")

    def test_metadata_defaults_empty(self):
        d = _make_dep()
        assert isinstance(d.metadata, Mapping)
        assert len(d.metadata) == 0

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
        assert validate_transaction_dependency(_make_dep()) is True

    def test_validate_rejects_invalid(self):
        assert validate_transaction_dependency("not a dep") is False


class TestTransactionPrecondition:
    def test_valid_creation(self):
        p = _make_precond()
        assert p.precondition_id == "pre-1"
        assert p.precondition_type == "accepted_command_required"
        assert p.satisfied is True
        assert p.blocking is True
        assert p.message is None
        assert p.hidden_info_safe is True

    @pytest.mark.parametrize("ptype", sorted(TRANSACTION_PRECONDITION_TYPES))
    def test_all_precondition_types_accepted(self, ptype):
        p = _make_precond(precondition_type=ptype)
        assert p.precondition_type == ptype

    def test_invalid_type_rejected(self):
        with pytest.raises(InvalidTransactionPreconditionError):
            _make_precond(precondition_type="magic_required")

    def test_empty_id_rejected(self):
        with pytest.raises(InvalidTransactionPreconditionError):
            _make_precond(precondition_id="")

    def test_non_bool_satisfied_rejected(self):
        with pytest.raises(InvalidTransactionPreconditionError):
            _make_precond(satisfied="yes")

    def test_non_bool_blocking_rejected(self):
        with pytest.raises(InvalidTransactionPreconditionError):
            _make_precond(blocking=1)

    def test_message_accepts_none(self):
        p = _make_precond(message=None)
        assert p.message is None

    def test_message_accepts_non_empty(self):
        p = _make_precond(message="needs actor")
        assert p.message == "needs actor"

    def test_message_rejects_empty(self):
        with pytest.raises(InvalidTransactionPreconditionError):
            _make_precond(message="")

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1]}
        p = _make_precond(metadata=m)
        m["x"].append(99)
        assert 99 not in p.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        p = _make_precond(metadata={"k": [1]})
        out = p.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in p.to_dict()["metadata"]["k"]

    def test_frozen(self):
        p = _make_precond()
        with pytest.raises((AttributeError, TypeError)):
            p.satisfied = False  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_transaction_precondition(_make_precond()) is True

    def test_validate_rejects_invalid(self):
        assert validate_transaction_precondition("not a precond") is False


class TestTransactionRequest:
    def test_valid_creation(self):
        r = _make_request()
        assert r.transaction_id == "txn-1"
        assert r.command_envelope_id == "cmd-1"
        assert r.actor_ref_id == "actor-1"
        assert r.requested_stage == "transaction_requested"
        assert r.dependencies == ()
        assert r.preconditions == ()

    def test_empty_transaction_id_rejected(self):
        with pytest.raises(InvalidTransactionRequestError):
            _make_request(transaction_id="")

    def test_empty_command_envelope_id_rejected(self):
        with pytest.raises(InvalidTransactionRequestError):
            _make_request(command_envelope_id="")

    def test_empty_actor_ref_id_rejected(self):
        with pytest.raises(InvalidTransactionRequestError):
            _make_request(actor_ref_id="")

    def test_invalid_stage_rejected(self):
        with pytest.raises((InvalidTransactionRequestError, Exception)):
            _make_request(requested_stage="bad_stage")

    def test_optional_ids_accept_none(self):
        r = _make_request(command_lifecycle_id=None, idempotency_key=None, trace_id=None)
        assert r.command_lifecycle_id is None
        assert r.idempotency_key is None
        assert r.trace_id is None

    def test_optional_ids_reject_empty(self):
        with pytest.raises(InvalidTransactionRequestError):
            _make_request(command_lifecycle_id="")

    def test_dependencies_reject_bare_string(self):
        with pytest.raises(InvalidTransactionRequestError):
            _make_request(dependencies="dep-1")

    def test_preconditions_reject_bare_string(self):
        with pytest.raises(InvalidTransactionRequestError):
            _make_request(preconditions="pre-1")

    def test_dependencies_accept_valid_list(self):
        dep = _make_dep()
        r = _make_request(dependencies=[dep])
        assert len(r.dependencies) == 1
        assert isinstance(r.dependencies, tuple)

    def test_preconditions_accept_valid_list(self):
        pre = _make_precond()
        r = _make_request(preconditions=[pre])
        assert len(r.preconditions) == 1
        assert isinstance(r.preconditions, tuple)

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
            r.transaction_id = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_transaction_request(_make_request()) is True

    def test_validate_rejects_invalid(self):
        assert validate_transaction_request("not a request") is False


class TestTransactionPlan:
    def test_valid_creation(self):
        p = _make_plan()
        assert p.transaction_id == "txn-1"
        assert p.current_stage == "transaction_requested"
        assert p.decision == "accepted_for_planning"
        assert p.ready_for_event_commitment is False

    def test_invalid_stage_rejected(self):
        with pytest.raises(InvalidTransactionPlanError):
            _make_plan(current_stage="bad_stage")

    def test_invalid_decision_rejected(self):
        with pytest.raises(InvalidTransactionPlanError):
            _make_plan(decision="bad_decision")

    def test_tuple_fields_normalized(self):
        p = _make_plan(dependency_ids=["a", "b"], state_ref_ids=["s1"])
        assert isinstance(p.dependency_ids, tuple)
        assert isinstance(p.state_ref_ids, tuple)

    def test_tuple_fields_reject_bare_string(self):
        with pytest.raises(InvalidTransactionPlanError):
            _make_plan(dependency_ids="dep-1")

    def test_tuple_fields_reject_empty_item(self):
        with pytest.raises(InvalidTransactionPlanError):
            _make_plan(dependency_ids=["dep-1", ""])

    def test_ready_for_commitment_invariant_valid(self):
        p = _make_plan(
            current_stage="ready_for_event_commitment",
            decision="ready_for_event_commitment",
            ready_for_event_commitment=True,
            validation_ref_id="val-1",
            proposed_delta_ref_ids=["delta-1"],
        )
        assert p.ready_for_event_commitment is True

    def test_ready_for_commitment_requires_correct_decision(self):
        with pytest.raises(InvalidTransactionPlanError):
            _make_plan(
                decision="accepted_for_planning",
                ready_for_event_commitment=True,
                validation_ref_id="val-1",
                proposed_delta_ref_ids=["delta-1"],
            )

    def test_ready_for_commitment_requires_validation_ref(self):
        with pytest.raises(InvalidTransactionPlanError):
            _make_plan(
                current_stage="ready_for_event_commitment",
                decision="ready_for_event_commitment",
                ready_for_event_commitment=True,
                proposed_delta_ref_ids=["delta-1"],
            )

    def test_ready_for_commitment_requires_delta_refs(self):
        with pytest.raises(InvalidTransactionPlanError):
            _make_plan(
                current_stage="ready_for_event_commitment",
                decision="ready_for_event_commitment",
                ready_for_event_commitment=True,
                validation_ref_id="val-1",
            )

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1]}
        p = _make_plan(metadata=m)
        m["x"].append(99)
        assert 99 not in p.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        p = _make_plan(metadata={"k": [1]})
        out = p.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in p.to_dict()["metadata"]["k"]

    def test_frozen(self):
        p = _make_plan()
        with pytest.raises((AttributeError, TypeError)):
            p.decision = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_transaction_plan(_make_plan()) is True

    def test_validate_rejects_invalid(self):
        assert validate_transaction_plan("not a plan") is False


class TestTransactionResult:
    def test_valid_creation(self):
        r = _make_result()
        assert r.transaction_id == "txn-1"
        assert r.final_stage == "rejected"
        assert r.decision == "rejected_by_scope"
        assert r.accepted_for_commitment is False

    def test_invalid_stage_rejected(self):
        with pytest.raises(InvalidTransactionResultError):
            _make_result(final_stage="bad_stage")

    def test_invalid_decision_rejected(self):
        with pytest.raises(InvalidTransactionResultError):
            _make_result(decision="bad_decision")

    def test_accepted_invariant_valid(self):
        r = _make_result(
            final_stage="ready_for_event_commitment",
            decision="ready_for_event_commitment",
            accepted_for_commitment=True,
            event_commitment_request_id="ecr-1",
            rejection_reason=None,
        )
        assert r.accepted_for_commitment is True

    def test_accepted_requires_valid_stage(self):
        with pytest.raises(InvalidTransactionResultError):
            _make_result(
                final_stage="rejected",
                decision="ready_for_event_commitment",
                accepted_for_commitment=True,
                event_commitment_request_id="ecr-1",
            )

    def test_accepted_requires_commitment_request_id(self):
        with pytest.raises(InvalidTransactionResultError):
            _make_result(
                final_stage="ready_for_event_commitment",
                decision="ready_for_event_commitment",
                accepted_for_commitment=True,
            )

    def test_accepted_requires_no_rejection(self):
        with pytest.raises(InvalidTransactionResultError):
            _make_result(
                final_stage="ready_for_event_commitment",
                decision="ready_for_event_commitment",
                accepted_for_commitment=True,
                event_commitment_request_id="ecr-1",
                rejection_reason="should not be here",
            )

    def test_rejection_reason_requires_not_accepted(self):
        with pytest.raises(InvalidTransactionResultError):
            _make_result(
                final_stage="commitment_requested",
                decision="ready_for_event_commitment",
                accepted_for_commitment=True,
                event_commitment_request_id="ecr-1",
                rejection_reason="conflict",
            )

    def test_cancelled_quarantined_not_both(self):
        with pytest.raises(InvalidTransactionResultError):
            _make_result(cancelled=True, quarantined=True)

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
        assert validate_transaction_result(_make_result()) is True

    def test_validate_rejects_invalid(self):
        assert validate_transaction_result("not a result") is False


class TestValidatorParityTransactionLifecycle:
    def test_validate_dependency_rejects_empty_dependency_id(self):
        bad = TransactionDependency(
            dependency_id="", dependency_type="command_envelope_ref",
            reference_id="ref-1", required=True, satisfied=False,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_transaction_dependency(bad) is False

    def test_validate_dependency_rejects_invalid_type(self):
        bad = TransactionDependency(
            dependency_id="dep-1", dependency_type="bad_type",
            reference_id="ref-1", required=True, satisfied=False,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_transaction_dependency(bad) is False

    def test_validate_precondition_rejects_empty_id(self):
        bad = TransactionPrecondition(
            precondition_id="", precondition_type="accepted_command_required",
            satisfied=True, blocking=True, message=None,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_transaction_precondition(bad) is False

    def test_validate_precondition_rejects_invalid_type(self):
        bad = TransactionPrecondition(
            precondition_id="pre-1", precondition_type="bad_type",
            satisfied=True, blocking=True, message=None,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_transaction_precondition(bad) is False

    def test_validate_precondition_rejects_empty_message(self):
        bad = TransactionPrecondition(
            precondition_id="pre-1", precondition_type="accepted_command_required",
            satisfied=True, blocking=True, message="",
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_transaction_precondition(bad) is False

    def test_validate_request_rejects_empty_transaction_id(self):
        bad = TransactionRequest(
            transaction_id="", command_envelope_id="cmd-1",
            command_lifecycle_id=None, actor_ref_id="actor-1",
            requested_stage="transaction_requested",
            dependencies=(), preconditions=(),
            idempotency_key=None, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_request(bad) is False

    def test_validate_request_rejects_bad_dependency_entry(self):
        bad = TransactionRequest(
            transaction_id="txn-1", command_envelope_id="cmd-1",
            command_lifecycle_id=None, actor_ref_id="actor-1",
            requested_stage="transaction_requested",
            dependencies=("bad",), preconditions=(),
            idempotency_key=None, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_request(bad) is False

    def test_validate_plan_rejects_ready_with_wrong_decision(self):
        bad = TransactionPlan(
            transaction_id="txn-1", current_stage="ready_for_event_commitment",
            decision="accepted_for_planning",
            dependency_ids=(), precondition_ids=(),
            state_ref_ids=(), projection_ref_ids=(),
            proposed_delta_ref_ids=("delta-1",),
            validation_ref_id="val-1", trace_id=None,
            ready_for_event_commitment=True,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_plan(bad) is False

    def test_validate_plan_rejects_ready_without_validation(self):
        bad = TransactionPlan(
            transaction_id="txn-1", current_stage="ready_for_event_commitment",
            decision="ready_for_event_commitment",
            dependency_ids=(), precondition_ids=(),
            state_ref_ids=(), projection_ref_ids=(),
            proposed_delta_ref_ids=("delta-1",),
            validation_ref_id=None, trace_id=None,
            ready_for_event_commitment=True,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_plan(bad) is False

    def test_validate_plan_rejects_ready_without_deltas(self):
        bad = TransactionPlan(
            transaction_id="txn-1", current_stage="ready_for_event_commitment",
            decision="ready_for_event_commitment",
            dependency_ids=(), precondition_ids=(),
            state_ref_ids=(), projection_ref_ids=(),
            proposed_delta_ref_ids=(),
            validation_ref_id="val-1", trace_id=None,
            ready_for_event_commitment=True,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_plan(bad) is False

    def test_validate_result_rejects_accepted_with_wrong_stage(self):
        bad = TransactionResult(
            transaction_id="txn-1", final_stage="rejected",
            decision="ready_for_event_commitment",
            accepted_for_commitment=True,
            event_commitment_request_id="ecr-1",
            rejection_reason=None, quarantined=False, cancelled=False,
            hidden_info_safe=True, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_result(bad) is False

    def test_validate_result_rejects_accepted_without_ecr_id(self):
        bad = TransactionResult(
            transaction_id="txn-1", final_stage="ready_for_event_commitment",
            decision="ready_for_event_commitment",
            accepted_for_commitment=True,
            event_commitment_request_id=None,
            rejection_reason=None, quarantined=False, cancelled=False,
            hidden_info_safe=True, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_result(bad) is False

    def test_validate_result_rejects_cancelled_and_quarantined(self):
        bad = TransactionResult(
            transaction_id="txn-1", final_stage="rejected",
            decision="rejected_by_scope",
            accepted_for_commitment=False,
            event_commitment_request_id=None,
            rejection_reason=None, quarantined=True, cancelled=True,
            hidden_info_safe=True, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_transaction_result(bad) is False


class TestTransactionLifecycleService:
    def test_service_is_stateless(self):
        svc = TransactionLifecycleService()
        assert svc.__dict__ == {}

    def test_service_delegates_create_dependency(self):
        svc = TransactionLifecycleService()
        d = svc.create_dependency(
            dependency_id="dep-1", dependency_type="command_envelope_ref",
            reference_id="ref-1",
        )
        assert isinstance(d, TransactionDependency)

    def test_service_delegates_create_precondition(self):
        svc = TransactionLifecycleService()
        p = svc.create_precondition(
            precondition_id="pre-1", precondition_type="accepted_command_required",
            satisfied=True,
        )
        assert isinstance(p, TransactionPrecondition)

    def test_service_delegates_create_request(self):
        svc = TransactionLifecycleService()
        r = svc.create_request(
            transaction_id="txn-1", command_envelope_id="cmd-1",
            actor_ref_id="actor-1",
        )
        assert isinstance(r, TransactionRequest)

    def test_service_delegates_create_plan(self):
        svc = TransactionLifecycleService()
        p = svc.create_plan(
            transaction_id="txn-1", current_stage="transaction_requested",
            decision="accepted_for_planning",
        )
        assert isinstance(p, TransactionPlan)

    def test_service_delegates_create_result(self):
        svc = TransactionLifecycleService()
        r = svc.create_result(
            transaction_id="txn-1", final_stage="rejected",
            decision="rejected_by_scope", accepted_for_commitment=False,
        )
        assert isinstance(r, TransactionResult)

    def test_service_delegates_validate(self):
        svc = TransactionLifecycleService()
        assert svc.validate_dependency(_make_dep()) is True
        assert svc.validate_precondition(_make_precond()) is True
        assert svc.validate_request(_make_request()) is True
        assert svc.validate_plan(_make_plan()) is True
        assert svc.validate_result(_make_result()) is True

    def test_service_has_no_forbidden_methods(self):
        forbidden = [
            "execute", "run", "mutate", "apply", "apply_delta", "commit",
            "append", "persist", "save", "load", "replay", "rollback",
            "resolve", "roll", "narrate", "prompt", "model",
        ]
        svc_methods = [m for m in dir(TransactionLifecycleService) if not m.startswith("_")]
        for method_name in forbidden:
            assert method_name not in svc_methods, f"Forbidden method found: {method_name}"

    def test_no_mutation_methods(self):
        mutation = ["mutate", "apply_delta", "commit_event", "store", "persist", "append"]
        for m in mutation:
            assert not hasattr(TransactionLifecycleService, m)


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
            "model_boundary_evaluation.py",
            "tiny_vertical_slice.py",
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


class TestDecisionLogTracking:
    def test_pr3a_id_appears_in_decision_log(self):
        path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        content = path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-PR-3A" in content

    def test_pr3a_heading_appears_exactly_once(self):
        path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        content = path.read_text(encoding="utf-8")
        heading = "## RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001"
        count = content.count(heading)
        assert count == 1, f"Expected exactly 1 heading occurrence, found {count}"


class TestRegistryTracking:
    def test_pr3a_file_id_appears_exactly_once(self):
        path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        content = path.read_text(encoding="utf-8")
        file_id_str = "file_id: RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001"
        count = content.count(file_id_str)
        assert count == 1, f"Expected exactly 1 file_id occurrence, found {count}"
