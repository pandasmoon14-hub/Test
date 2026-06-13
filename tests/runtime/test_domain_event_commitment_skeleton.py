"""Focused skeleton tests for event commitment domain module."""

from __future__ import annotations

import os
import pathlib
from types import MappingProxyType
from typing import Mapping

import pytest

from astra_runtime.domain import (
    EVENT_COMMITMENT_DECISIONS,
    EVENT_COMMITMENT_DEPENDENCY_TYPES,
    EVENT_COMMITMENT_STATUSES,
    EventCommitmentDependency,
    EventCommitmentError,
    EventCommitmentRejection,
    EventCommitmentRequest,
    EventCommitmentResult,
    EventCommitmentService,
    InvalidEventCommitmentDependencyError,
    InvalidEventCommitmentRejectionError,
    InvalidEventCommitmentRequestError,
    InvalidEventCommitmentResultError,
    create_event_commitment_dependency,
    create_event_commitment_rejection,
    create_event_commitment_request,
    create_event_commitment_result,
    validate_event_commitment_dependency,
    validate_event_commitment_rejection,
    validate_event_commitment_request,
    validate_event_commitment_result,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DOMAIN_PACKAGE_DIR = REPO_ROOT / "src" / "astra_runtime" / "domain"


def _make_dep(**kwargs):
    defaults = dict(
        dependency_id="dep-1",
        dependency_type="transaction_ref",
        reference_id="ref-1",
    )
    defaults.update(kwargs)
    return create_event_commitment_dependency(**defaults)


def _make_rejection(**kwargs):
    defaults = dict(
        rejection_id="rej-1",
        decision="rejected_by_validation",
        reason="validation failed",
    )
    defaults.update(kwargs)
    return create_event_commitment_rejection(**defaults)


def _make_request(**kwargs):
    defaults = dict(
        commitment_request_id="ecr-1",
        transaction_id="txn-1",
        event_type="command_outcome",
        state_ref_ids=["ref-1"],
        proposed_delta_ref_ids=["delta-1"],
        validation_ref_id="val-1",
        trace_id="trace-1",
    )
    defaults.update(kwargs)
    return create_event_commitment_request(**defaults)


def _make_result(**kwargs):
    defaults = dict(
        commitment_request_id="ecr-1",
        decision="rejected_by_validation",
        status="rejected",
    )
    defaults.update(kwargs)
    return create_event_commitment_result(**defaults)


class TestDomainImports:
    def test_event_commitment_symbols_importable(self):
        assert EVENT_COMMITMENT_DECISIONS is not None
        assert EVENT_COMMITMENT_STATUSES is not None
        assert EVENT_COMMITMENT_DEPENDENCY_TYPES is not None
        assert EventCommitmentDependency is not None
        assert EventCommitmentRejection is not None
        assert EventCommitmentRequest is not None
        assert EventCommitmentResult is not None
        assert EventCommitmentService is not None
        assert EventCommitmentError is not None


class TestEventCommitmentDecisions:
    def test_all_12_decisions_present(self):
        expected = {
            "commit_ready", "committed", "rejected_by_validation", "rejected_by_scope",
            "rejected_by_missing_state_reference", "rejected_by_missing_delta_reference",
            "rejected_by_hidden_information_risk", "rejected_by_idempotency_conflict",
            "rejected_by_persistence_boundary", "quarantined_for_audit",
            "cancelled_before_commit", "unsupported_event_type",
        }
        assert expected == set(EVENT_COMMITMENT_DECISIONS)
        assert len(EVENT_COMMITMENT_DECISIONS) == 12


class TestEventCommitmentStatuses:
    def test_all_7_statuses_present(self):
        expected = {
            "requested", "validated", "commit_ready", "committed",
            "rejected", "quarantined", "cancelled",
        }
        assert expected == set(EVENT_COMMITMENT_STATUSES)
        assert len(EVENT_COMMITMENT_STATUSES) == 7


class TestEventCommitmentDependencyTypes:
    def test_all_15_types_present(self):
        expected = {
            "transaction_ref", "command_envelope_ref", "actor_ref",
            "state_record_ref", "state_snapshot_ref", "state_projection_ref",
            "state_delta_ref", "validation_result_ref", "event_ledger_ref",
            "hidden_information_ref", "context_projection_ref", "runtime_trace_ref",
            "persistence_boundary_ref", "replay_audit_ref", "idempotency_key_ref",
        }
        assert expected == set(EVENT_COMMITMENT_DEPENDENCY_TYPES)
        assert len(EVENT_COMMITMENT_DEPENDENCY_TYPES) == 15


class TestEventCommitmentDependency:
    def test_valid_creation(self):
        d = _make_dep()
        assert d.dependency_id == "dep-1"
        assert d.dependency_type == "transaction_ref"
        assert d.reference_id == "ref-1"
        assert d.required is True
        assert d.satisfied is False
        assert d.hidden_info_safe is True

    @pytest.mark.parametrize("dep_type", sorted(EVENT_COMMITMENT_DEPENDENCY_TYPES))
    def test_all_dependency_types_accepted(self, dep_type):
        d = _make_dep(dependency_type=dep_type)
        assert d.dependency_type == dep_type

    def test_invalid_dependency_type_rejected(self):
        with pytest.raises(InvalidEventCommitmentDependencyError):
            _make_dep(dependency_type="magic_ref")

    def test_empty_dependency_id_rejected(self):
        with pytest.raises(InvalidEventCommitmentDependencyError):
            _make_dep(dependency_id="")

    def test_empty_reference_id_rejected(self):
        with pytest.raises(InvalidEventCommitmentDependencyError):
            _make_dep(reference_id="")

    def test_non_bool_required_rejected(self):
        with pytest.raises(InvalidEventCommitmentDependencyError):
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
        assert validate_event_commitment_dependency(_make_dep()) is True

    def test_validate_rejects_invalid(self):
        assert validate_event_commitment_dependency("not a dep") is False


class TestEventCommitmentRejection:
    def test_valid_creation(self):
        r = _make_rejection()
        assert r.rejection_id == "rej-1"
        assert r.decision == "rejected_by_validation"
        assert r.reason == "validation failed"
        assert r.blocking is True
        assert r.hidden_info_safe is True
        assert r.player_visible is False

    def test_committed_decision_rejected(self):
        with pytest.raises(InvalidEventCommitmentRejectionError):
            _make_rejection(decision="committed")

    def test_commit_ready_decision_rejected(self):
        with pytest.raises(InvalidEventCommitmentRejectionError):
            _make_rejection(decision="commit_ready")

    def test_empty_rejection_id_rejected(self):
        with pytest.raises(InvalidEventCommitmentRejectionError):
            _make_rejection(rejection_id="")

    def test_empty_reason_rejected(self):
        with pytest.raises(InvalidEventCommitmentRejectionError):
            _make_rejection(reason="")

    def test_player_visible_requires_hidden_info_safe(self):
        with pytest.raises(InvalidEventCommitmentRejectionError):
            _make_rejection(player_visible=True, hidden_info_safe=False)

    def test_player_visible_with_hidden_info_safe_accepted(self):
        r = _make_rejection(player_visible=True, hidden_info_safe=True)
        assert r.player_visible is True
        assert r.hidden_info_safe is True

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1]}
        r = _make_rejection(metadata=m)
        m["x"].append(99)
        assert 99 not in r.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        r = _make_rejection(metadata={"k": [1]})
        out = r.to_dict()
        out["metadata"]["k"].append(99)
        assert 99 not in r.to_dict()["metadata"]["k"]

    def test_frozen(self):
        r = _make_rejection()
        with pytest.raises((AttributeError, TypeError)):
            r.decision = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_event_commitment_rejection(_make_rejection()) is True

    def test_validate_rejects_invalid(self):
        assert validate_event_commitment_rejection("not a rejection") is False


class TestEventCommitmentRequest:
    def test_valid_creation(self):
        r = _make_request()
        assert r.commitment_request_id == "ecr-1"
        assert r.transaction_id == "txn-1"
        assert r.event_type == "command_outcome"
        assert r.allow_event_ledger_append is False

    def test_empty_ids_rejected(self):
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(commitment_request_id="")
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(transaction_id="")
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(event_type="")

    def test_state_ref_ids_reject_bare_string(self):
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(state_ref_ids="ref-1")

    def test_state_ref_ids_reject_empty(self):
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(state_ref_ids=[])

    def test_proposed_delta_ref_ids_reject_bare_string(self):
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(proposed_delta_ref_ids="delta-1")

    def test_proposed_delta_ref_ids_reject_empty(self):
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(proposed_delta_ref_ids=[])

    def test_allow_event_ledger_append_true_rejected(self):
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(allow_event_ledger_append=True)

    def test_dependencies_reject_bare_string(self):
        with pytest.raises(InvalidEventCommitmentRequestError):
            _make_request(dependencies="dep-1")

    def test_dependencies_accept_valid_list(self):
        dep = _make_dep()
        r = _make_request(dependencies=[dep])
        assert len(r.dependencies) == 1
        assert isinstance(r.dependencies, tuple)

    def test_tuple_fields_normalized(self):
        r = _make_request(state_ref_ids=["a", "b"], proposed_delta_ref_ids=["d1"])
        assert isinstance(r.state_ref_ids, tuple)
        assert isinstance(r.proposed_delta_ref_ids, tuple)

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
            r.event_type = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_event_commitment_request(_make_request()) is True

    def test_validate_rejects_invalid(self):
        assert validate_event_commitment_request("not a request") is False


class TestEventCommitmentResult:
    def test_valid_creation(self):
        r = _make_result()
        assert r.commitment_request_id == "ecr-1"
        assert r.decision == "rejected_by_validation"
        assert r.status == "rejected"
        assert r.state_delta_applied is False
        assert r.event_ledger_appended is False

    def test_state_delta_applied_true_rejected(self):
        with pytest.raises(InvalidEventCommitmentResultError):
            _make_result(state_delta_applied=True)

    def test_event_ledger_appended_true_rejected(self):
        with pytest.raises(InvalidEventCommitmentResultError):
            _make_result(event_ledger_appended=True)

    def test_committed_with_rejection_rejected(self):
        rej = _make_rejection()
        with pytest.raises(InvalidEventCommitmentResultError):
            _make_result(decision="committed", status="committed", rejection=rej)

    def test_cancelled_quarantined_not_both(self):
        with pytest.raises(InvalidEventCommitmentResultError):
            _make_result(cancelled=True, quarantined=True)

    def test_invalid_decision_rejected(self):
        with pytest.raises(InvalidEventCommitmentResultError):
            _make_result(decision="bad_decision")

    def test_invalid_status_rejected(self):
        with pytest.raises(InvalidEventCommitmentResultError):
            _make_result(status="bad_status")

    def test_committed_decision_accepted_with_commit_ready_status(self):
        r = _make_result(decision="committed", status="commit_ready")
        assert r.decision == "committed"
        assert r.state_delta_applied is False
        assert r.event_ledger_appended is False

    def test_rejection_with_valid_result(self):
        rej = _make_rejection()
        r = _make_result(
            decision="rejected_by_validation",
            status="rejected",
            rejection=rej,
        )
        assert r.rejection is not None
        assert r.rejection.decision == "rejected_by_validation"

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
        assert validate_event_commitment_result(_make_result()) is True

    def test_validate_rejects_invalid(self):
        assert validate_event_commitment_result("not a result") is False


class TestValidatorParityEventCommitment:
    def test_validate_dependency_rejects_empty_dependency_id(self):
        bad = EventCommitmentDependency(
            dependency_id="", dependency_type="transaction_ref",
            reference_id="ref-1", required=True, satisfied=False,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_dependency(bad) is False

    def test_validate_dependency_rejects_invalid_type(self):
        bad = EventCommitmentDependency(
            dependency_id="dep-1", dependency_type="bad_type",
            reference_id="ref-1", required=True, satisfied=False,
            hidden_info_safe=True, metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_dependency(bad) is False

    def test_validate_rejection_rejects_committed_decision(self):
        bad = EventCommitmentRejection(
            rejection_id="rej-1", decision="committed",
            reason="bad", blocking=True, hidden_info_safe=True,
            player_visible=False, metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_rejection(bad) is False

    def test_validate_rejection_rejects_player_visible_without_hidden_safe(self):
        bad = EventCommitmentRejection(
            rejection_id="rej-1", decision="rejected_by_validation",
            reason="bad", blocking=True, hidden_info_safe=False,
            player_visible=True, metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_rejection(bad) is False

    def test_validate_request_rejects_allow_event_ledger_append(self):
        bad = EventCommitmentRequest(
            commitment_request_id="ecr-1", transaction_id="txn-1",
            event_type="command_outcome",
            state_ref_ids=("ref-1",), proposed_delta_ref_ids=("delta-1",),
            validation_ref_id="val-1", trace_id="trace-1",
            idempotency_key=None, dependencies=(),
            allow_event_ledger_append=True,
            metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_request(bad) is False

    def test_validate_request_rejects_empty_state_ref_ids(self):
        bad = EventCommitmentRequest(
            commitment_request_id="ecr-1", transaction_id="txn-1",
            event_type="command_outcome",
            state_ref_ids=(), proposed_delta_ref_ids=("delta-1",),
            validation_ref_id="val-1", trace_id="trace-1",
            idempotency_key=None, dependencies=(),
            allow_event_ledger_append=False,
            metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_request(bad) is False

    def test_validate_result_rejects_state_delta_applied(self):
        bad = EventCommitmentResult(
            commitment_request_id="ecr-1", decision="committed",
            status="committed",
            committed_event_ref_id=None, event_ledger_ref_id=None,
            state_delta_applied=True, event_ledger_appended=False,
            rejection=None, quarantined=False, cancelled=False,
            hidden_info_safe=True, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_result(bad) is False

    def test_validate_result_rejects_event_ledger_appended(self):
        bad = EventCommitmentResult(
            commitment_request_id="ecr-1", decision="committed",
            status="committed",
            committed_event_ref_id=None, event_ledger_ref_id=None,
            state_delta_applied=False, event_ledger_appended=True,
            rejection=None, quarantined=False, cancelled=False,
            hidden_info_safe=True, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_result(bad) is False

    def test_validate_result_rejects_committed_with_rejection(self):
        rej = EventCommitmentRejection(
            rejection_id="rej-1", decision="rejected_by_validation",
            reason="bad", blocking=True, hidden_info_safe=True,
            player_visible=False, metadata=MappingProxyType({}),
        )
        bad = EventCommitmentResult(
            commitment_request_id="ecr-1", decision="committed",
            status="committed",
            committed_event_ref_id=None, event_ledger_ref_id=None,
            state_delta_applied=False, event_ledger_appended=False,
            rejection=rej, quarantined=False, cancelled=False,
            hidden_info_safe=True, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_result(bad) is False

    def test_validate_result_rejects_cancelled_and_quarantined(self):
        bad = EventCommitmentResult(
            commitment_request_id="ecr-1", decision="rejected_by_scope",
            status="rejected",
            committed_event_ref_id=None, event_ledger_ref_id=None,
            state_delta_applied=False, event_ledger_appended=False,
            rejection=None, quarantined=True, cancelled=True,
            hidden_info_safe=True, trace_id=None,
            metadata=MappingProxyType({}),
        )
        assert validate_event_commitment_result(bad) is False


class TestEventCommitmentService:
    def test_service_is_stateless(self):
        svc = EventCommitmentService()
        assert svc.__dict__ == {}

    def test_service_delegates_create_dependency(self):
        svc = EventCommitmentService()
        d = svc.create_dependency(
            dependency_id="dep-1", dependency_type="transaction_ref",
            reference_id="ref-1",
        )
        assert isinstance(d, EventCommitmentDependency)

    def test_service_delegates_create_rejection(self):
        svc = EventCommitmentService()
        r = svc.create_rejection(
            rejection_id="rej-1", decision="rejected_by_validation",
            reason="bad",
        )
        assert isinstance(r, EventCommitmentRejection)

    def test_service_delegates_create_request(self):
        svc = EventCommitmentService()
        r = svc.create_request(
            commitment_request_id="ecr-1", transaction_id="txn-1",
            event_type="command_outcome",
            state_ref_ids=["ref-1"], proposed_delta_ref_ids=["delta-1"],
            validation_ref_id="val-1", trace_id="trace-1",
        )
        assert isinstance(r, EventCommitmentRequest)

    def test_service_delegates_create_result(self):
        svc = EventCommitmentService()
        r = svc.create_result(
            commitment_request_id="ecr-1", decision="rejected_by_validation",
            status="rejected",
        )
        assert isinstance(r, EventCommitmentResult)

    def test_service_delegates_validate(self):
        svc = EventCommitmentService()
        assert svc.validate_dependency(_make_dep()) is True
        assert svc.validate_rejection(_make_rejection()) is True
        assert svc.validate_request(_make_request()) is True
        assert svc.validate_result(_make_result()) is True

    def test_service_has_no_forbidden_methods(self):
        forbidden = [
            "commit", "append", "apply", "apply_delta", "mutate",
            "persist", "save", "load", "replay", "rollback",
            "execute", "run", "resolve", "roll", "narrate", "prompt", "model",
        ]
        svc_methods = [m for m in dir(EventCommitmentService) if not m.startswith("_")]
        for method_name in forbidden:
            assert method_name not in svc_methods, f"Forbidden method found: {method_name}"

    def test_no_append_commit_methods(self):
        mutation = ["commit_event", "append_event", "apply_delta", "store", "persist"]
        for m in mutation:
            assert not hasattr(EventCommitmentService, m)


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


class TestRegistryTracking:
    def test_pr3a_file_id_appears_in_registry(self):
        path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        content = path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-PR-3A-TRANSACTION-LIFECYCLE-EVENT-COMMITMENT-SKELETON-IMPLEMENTATION-001" in content
