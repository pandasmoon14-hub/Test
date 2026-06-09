"""Focused skeleton tests for state projection domain module."""

from __future__ import annotations

import os
from typing import Mapping

import pytest

from astra_runtime.domain import (
    STATE_PROJECTION_STATUSES,
    STATE_PROJECTION_TYPES,
    InvalidStateProjectionDependencyError,
    InvalidStateProjectionRejectionError,
    InvalidStateProjectionRequestError,
    InvalidStateProjectionResultError,
    StateProjectionDependency,
    StateProjectionError,
    StateProjectionRejection,
    StateProjectionRequest,
    StateProjectionResult,
    StateProjectionService,
    create_state_projection_dependency,
    create_state_projection_rejection,
    create_state_projection_request,
    create_state_projection_result,
    project_state_view,
    validate_state_projection_dependency,
    validate_state_projection_rejection,
    validate_state_projection_request,
    validate_state_projection_result,
    create_state_visibility_descriptor,
)


_ALL_PROJECTION_TYPES = [
    "full_backend", "player_visible", "actor_scoped", "scene_scoped",
    "faction_social", "combat_encounter", "inventory_asset", "mission_clue",
    "hidden_info_redacted", "audit_provenance", "model_facing_candidate",
    "ui_client_candidate",
]

_ALL_PROJECTION_STATUSES = [
    "requested", "validated", "materialized", "redacted", "rejected", "quarantined",
]

_BACKEND_HIDDEN_FORBIDDEN = [
    "player_visible", "actor_scoped", "model_facing_candidate", "ui_client_candidate",
]


def _make_dep(**kwargs):
    defaults = dict(dependency_id="dep-1", dependency_type="state_record_ref", required=True)
    defaults.update(kwargs)
    return create_state_projection_dependency(**defaults)


def _make_rejection(**kwargs):
    defaults = dict(
        rejection_id="rej-1", reason_code="blocked",
        message="not allowed", hidden_info_safe=True, player_visible=False,
    )
    defaults.update(kwargs)
    return create_state_projection_rejection(**defaults)


def _make_request(**kwargs):
    defaults = dict(
        projection_request_id="req-1",
        requester_id="actor-1",
        projection_type="full_backend",
        state_ref_ids=["ref-1"],
        visibility_tier="backend_hidden",
        include_backend_hidden=True,
    )
    defaults.update(kwargs)
    return create_state_projection_request(**defaults)


def _make_result(**kwargs):
    defaults = dict(
        projection_id="proj-1",
        projection_request_id="req-1",
        projection_type="full_backend",
        status="materialized",
    )
    defaults.update(kwargs)
    return create_state_projection_result(**defaults)


class TestDomainImports:
    def test_state_projection_symbols_importable(self):
        assert STATE_PROJECTION_TYPES is not None
        assert STATE_PROJECTION_STATUSES is not None
        assert StateProjectionRequest is not None
        assert StateProjectionResult is not None
        assert StateProjectionService is not None
        assert StateProjectionError is not None


class TestProjectionTypes:
    @pytest.mark.parametrize("ptype", _ALL_PROJECTION_TYPES)
    def test_all_12_projection_types_accepted(self, ptype):
        include_hidden = ptype not in _BACKEND_HIDDEN_FORBIDDEN
        r = _make_request(projection_type=ptype, include_backend_hidden=include_hidden)
        assert r.projection_type == ptype

    def test_unsupported_type_rejected(self):
        with pytest.raises(InvalidStateProjectionRequestError):
            _make_request(projection_type="omniscient_view")


class TestProjectionStatuses:
    @pytest.mark.parametrize("status", _ALL_PROJECTION_STATUSES)
    def test_all_statuses_accepted(self, status):
        r = _make_result(status=status)
        assert r.status == status

    def test_unsupported_status_rejected(self):
        with pytest.raises(InvalidStateProjectionResultError):
            _make_result(status="unknown_status")


class TestStateProjectionDependency:
    def test_valid_creation(self):
        d = _make_dep()
        assert d.dependency_id == "dep-1"
        assert d.dependency_type == "state_record_ref"
        assert d.required is True

    def test_all_dependency_types_accepted(self):
        allowed = [
            "state_record_ref", "state_snapshot_ref", "hidden_information",
            "context_projection", "validation_result", "runtime_trace",
            "persistence_boundary", "replay_audit", "transaction_lifecycle",
            "event_ledger", "command_lifecycle", "model_evaluation", "live_play_gate",
        ]
        for dep_type in allowed:
            d = _make_dep(dependency_type=dep_type)
            assert d.dependency_type == dep_type

    def test_unsupported_dependency_type_rejected(self):
        with pytest.raises(InvalidStateProjectionDependencyError):
            _make_dep(dependency_type="magic_dependency")

    def test_validate_accepts_valid(self):
        assert validate_state_projection_dependency(_make_dep()) is True

    def test_validate_rejects_invalid(self):
        assert validate_state_projection_dependency("not a dep") is False


class TestStateProjectionRejection:
    def test_valid_creation(self):
        r = _make_rejection()
        assert r.rejection_id == "rej-1"
        assert r.reason_code == "blocked"
        assert r.message == "not allowed"
        assert r.hidden_info_safe is True
        assert r.player_visible is False

    def test_invalid_rejection_fields_rejected(self):
        with pytest.raises(InvalidStateProjectionRejectionError):
            _make_rejection(rejection_id="")
        with pytest.raises(InvalidStateProjectionRejectionError):
            _make_rejection(hidden_info_safe="yes")

    def test_validate_accepts_valid(self):
        assert validate_state_projection_rejection(_make_rejection()) is True

    def test_validate_rejects_invalid(self):
        assert validate_state_projection_rejection("not a rejection") is False


class TestStateProjectionRequest:
    def test_valid_creation(self):
        r = _make_request()
        assert r.projection_request_id == "req-1"
        assert r.requester_id == "actor-1"
        assert r.projection_type == "full_backend"
        assert r.include_backend_hidden is True

    def test_state_ref_ids_normalized_to_tuple(self):
        r = _make_request(state_ref_ids=["a", "b"])
        assert isinstance(r.state_ref_ids, tuple)

    def test_state_ref_ids_reject_bare_string(self):
        with pytest.raises(InvalidStateProjectionRequestError):
            _make_request(state_ref_ids="ref-1")

    def test_rejects_non_bool_include_backend_hidden(self):
        with pytest.raises(InvalidStateProjectionRequestError):
            _make_request(include_backend_hidden=1)

    @pytest.mark.parametrize("ptype", _BACKEND_HIDDEN_FORBIDDEN)
    def test_rejects_backend_hidden_for_public_types(self, ptype):
        with pytest.raises(InvalidStateProjectionRequestError):
            _make_request(projection_type=ptype, include_backend_hidden=True)

    def test_metadata_deep_copy_safe(self):
        m = {"key": [1, 2]}
        r = _make_request(metadata=m)
        m["key"].append(99)
        assert 99 not in r.metadata.get("key", [])

    def test_frozen(self):
        r = _make_request()
        with pytest.raises((AttributeError, TypeError)):
            r.projection_type = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_state_projection_request(_make_request()) is True

    def test_validate_rejects_invalid(self):
        assert validate_state_projection_request("not a request") is False


class TestStateProjectionResult:
    def test_valid_creation(self):
        r = _make_result()
        assert r.projection_id == "proj-1"
        assert r.projection_request_id == "req-1"
        assert r.projection_type == "full_backend"
        assert r.status == "materialized"

    def test_rejects_invalid_rejection_type(self):
        with pytest.raises(InvalidStateProjectionResultError):
            _make_result(rejection="not_a_rejection")

    def test_metadata_deep_copy_safe(self):
        m = {"key": [1]}
        r = _make_result(metadata=m)
        m["key"].append(99)
        assert 99 not in r.metadata.get("key", [])

    def test_to_dict_returns_copy(self):
        r = _make_result(metadata={"k": [1]})
        d = r.to_dict()
        d["metadata"]["k"].append(99)
        assert 99 not in r.to_dict()["metadata"]["k"]

    def test_frozen(self):
        r = _make_result()
        with pytest.raises((AttributeError, TypeError)):
            r.status = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_state_projection_result(_make_result()) is True

    def test_validate_rejects_invalid(self):
        assert validate_state_projection_result("not a result") is False


class TestProjectStateView:
    def test_accepts_valid_request(self):
        req = _make_request()
        result = project_state_view(
            "proj-1",
            req,
            visible_state_ref_ids=["ref-1"],
            redacted_state_ref_ids=[],
        )
        assert isinstance(result, StateProjectionResult)
        assert result.projection_id == "proj-1"
        assert result.projection_request_id == "req-1"

    def test_rejects_invalid_request(self):
        with pytest.raises(InvalidStateProjectionRequestError):
            project_state_view("proj-1", "not_a_request")  # type: ignore[arg-type]

    def test_does_not_fetch_state_payloads(self):
        req = _make_request()
        result = project_state_view("proj-2", req)
        assert result.visible_state_ref_ids == ()
        assert result.redacted_state_ref_ids == ()

    def test_does_not_mutate_request(self):
        req = _make_request()
        original_type = req.projection_type
        project_state_view("proj-3", req)
        assert req.projection_type == original_type


class TestStateProjectionService:
    def test_service_is_stateless(self):
        svc = StateProjectionService()
        assert svc.__dict__ == {}

    def test_service_has_no_forbidden_methods(self):
        forbidden = [
            "fetch_state", "get_state", "set_state", "read", "write", "save",
            "load", "apply", "mutate", "commit", "replay", "restore", "execute",
            "run", "compile_context_packet", "model", "prompt",
        ]
        svc_methods = [m for m in dir(StateProjectionService) if not m.startswith("_")]
        for method_name in forbidden:
            assert method_name not in svc_methods, f"Forbidden method found: {method_name}"

    def test_no_context_packet_model_prompt_live_play_methods(self):
        for m in ["context_packet", "compile_prompt", "run_model", "live_play_gate"]:
            assert not hasattr(StateProjectionService, m)

    def test_service_project(self):
        svc = StateProjectionService()
        req = _make_request()
        result = svc.project("proj-svc-1", req)
        assert isinstance(result, StateProjectionResult)
