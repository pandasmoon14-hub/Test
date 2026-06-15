"""Focused skeleton tests for state store domain module."""

from __future__ import annotations

import os
from typing import Mapping

import pytest

from astra_runtime.domain import (
    STATE_AUTHORITY_LEVELS,
    STATE_RECORD_CATEGORIES,
    InvalidStateRecordRefError,
    InvalidStateSnapshotRefError,
    InvalidStateVisibilityDescriptorError,
    StateRecordRef,
    StateSnapshotRef,
    StateStoreError,
    StateStoreService,
    StateVisibilityDescriptor,
    create_state_record_ref,
    create_state_snapshot_ref,
    create_state_visibility_descriptor,
    validate_state_record_ref,
    validate_state_snapshot_ref,
    validate_state_visibility_descriptor,
)


_VALID_VIS_TIERS = [
    "backend_hidden", "gm_visible", "actor_visible",
    "player_visible", "public", "redacted",
]


def _make_vis(**kwargs):
    defaults = dict(
        visibility_id="vis-1",
        visibility_tier="backend_hidden",
        hidden_info_safe=True,
        player_visible=False,
    )
    defaults.update(kwargs)
    return create_state_visibility_descriptor(**defaults)


def _make_ref(**kwargs):
    defaults = dict(
        state_ref_id="ref-1",
        record_id="rec-1",
        record_type="actor",
        category="authoritative_runtime",
        authority_level="authoritative",
        visibility=_make_vis(),
    )
    defaults.update(kwargs)
    return create_state_record_ref(**defaults)


def _make_snap(**kwargs):
    defaults = dict(
        snapshot_id="snap-1",
        snapshot_scope="session",
        state_ref_ids=["ref-1", "ref-2"],
        authority_level="authoritative",
    )
    defaults.update(kwargs)
    return create_state_snapshot_ref(**defaults)


class TestDomainImports:
    def test_state_store_symbols_importable(self):
        assert STATE_RECORD_CATEGORIES is not None
        assert STATE_AUTHORITY_LEVELS is not None
        assert StateVisibilityDescriptor is not None
        assert StateRecordRef is not None
        assert StateSnapshotRef is not None
        assert StateStoreService is not None


class TestStateRecordCategories:
    def test_all_10_categories_present(self):
        expected = {
            "authoritative_runtime", "projected", "visible", "hidden_backend_only",
            "derived", "cached_ephemeral", "source_local_converted", "canon_sourcebook",
            "generated_pending_provenance", "persisted_snapshot_boundary",
        }
        assert expected == set(STATE_RECORD_CATEGORIES)

    def test_unsupported_category_rejected(self):
        with pytest.raises(InvalidStateRecordRefError):
            _make_ref(category="bad_category")


class TestStateAuthorityLevels:
    def test_all_levels_present(self):
        expected = {
            "authoritative", "derived", "projected",
            "reference_only", "non_authoritative", "pending_provenance",
        }
        assert expected == set(STATE_AUTHORITY_LEVELS)

    def test_unsupported_level_rejected(self):
        with pytest.raises(InvalidStateRecordRefError):
            _make_ref(authority_level="supreme")


class TestVisibilityTiers:
    @pytest.mark.parametrize("tier", _VALID_VIS_TIERS)
    def test_all_visibility_tiers_accepted(self, tier):
        v = _make_vis(visibility_tier=tier)
        assert v.visibility_tier == tier

    def test_unsupported_visibility_tier_rejected(self):
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            _make_vis(visibility_tier="omniscient")


class TestStateVisibilityDescriptor:
    def test_valid_creation(self):
        v = _make_vis()
        assert v.visibility_id == "vis-1"
        assert v.visibility_tier == "backend_hidden"
        assert v.hidden_info_safe is True
        assert v.player_visible is False

    def test_invalid_id_rejected(self):
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            _make_vis(visibility_id="")

    def test_non_bool_hidden_info_safe_rejected(self):
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            _make_vis(hidden_info_safe="yes")

    def test_non_bool_player_visible_rejected(self):
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            _make_vis(player_visible=1)

    def test_metadata_defaults_empty(self):
        v = _make_vis()
        assert isinstance(v.metadata, Mapping)
        assert len(v.metadata) == 0

    def test_metadata_deep_copy_safe(self):
        m = {"key": [1, 2, 3]}
        v = _make_vis(metadata=m)
        m["key"].append(99)
        assert 99 not in v.metadata.get("key", [])

    def test_to_dict_returns_copy(self):
        v = _make_vis(metadata={"k": [1]})
        d = v.to_dict()
        d["metadata"]["k"].append(99)
        assert 99 not in v.to_dict()["metadata"]["k"]

    def test_frozen(self):
        v = _make_vis()
        with pytest.raises((AttributeError, TypeError)):
            v.visibility_id = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_state_visibility_descriptor(_make_vis()) is True

    def test_validate_rejects_invalid(self):
        assert validate_state_visibility_descriptor("not a descriptor") is False


class TestStateRecordRef:
    def test_valid_creation(self):
        r = _make_ref()
        assert r.state_ref_id == "ref-1"
        assert r.record_id == "rec-1"
        assert r.record_type == "actor"
        assert r.category == "authoritative_runtime"
        assert r.authority_level == "authoritative"
        assert isinstance(r.visibility, StateVisibilityDescriptor)

    def test_optional_ids_accept_none(self):
        r = _make_ref(schema_id=None, source_event_id=None, source_delta_id=None, provenance_id=None)
        assert r.schema_id is None
        assert r.source_event_id is None
        assert r.source_delta_id is None
        assert r.provenance_id is None

    def test_optional_ids_reject_empty_string(self):
        with pytest.raises(InvalidStateRecordRefError):
            _make_ref(schema_id="")

    def test_invalid_visibility_type_rejected(self):
        with pytest.raises(InvalidStateRecordRefError):
            _make_ref(visibility="not_a_descriptor")

    def test_metadata_defaults_empty(self):
        r = _make_ref()
        assert len(r.metadata) == 0

    def test_metadata_deep_copy_safe(self):
        m = {"x": [1, 2]}
        r = _make_ref(metadata=m)
        m["x"].append(99)
        assert 99 not in r.metadata.get("x", [])

    def test_to_dict_returns_copy(self):
        r = _make_ref(metadata={"x": [1]})
        d = r.to_dict()
        d["metadata"]["x"].append(99)
        assert 99 not in r.to_dict()["metadata"]["x"]

    def test_frozen(self):
        r = _make_ref()
        with pytest.raises((AttributeError, TypeError)):
            r.state_ref_id = "changed"  # type: ignore[misc]

    def test_validate_accepts_valid(self):
        assert validate_state_record_ref(_make_ref()) is True

    def test_validate_rejects_invalid(self):
        assert validate_state_record_ref("not a ref") is False


class TestStateSnapshotRef:
    def test_valid_creation(self):
        s = _make_snap()
        assert s.snapshot_id == "snap-1"
        assert s.snapshot_scope == "session"
        assert s.state_ref_ids == ("ref-1", "ref-2")
        assert s.authority_level == "authoritative"

    def test_state_ref_ids_normalized_to_tuple(self):
        s = _make_snap(state_ref_ids=["a", "b"])
        assert isinstance(s.state_ref_ids, tuple)

    def test_state_ref_ids_reject_bare_string(self):
        with pytest.raises(InvalidStateSnapshotRefError):
            _make_snap(state_ref_ids="ref-1")

    def test_empty_state_ref_id_rejected(self):
        with pytest.raises(InvalidStateSnapshotRefError):
            _make_snap(state_ref_ids=["ref-1", ""])

    def test_validate_accepts_valid(self):
        assert validate_state_snapshot_ref(_make_snap()) is True

    def test_validate_rejects_invalid(self):
        assert validate_state_snapshot_ref("not a snapshot") is False


class TestStateStoreService:
    def test_service_is_stateless(self):
        svc = StateStoreService()
        assert not hasattr(svc, "_state") or svc.__dict__ == {}

    def test_service_has_no_forbidden_methods(self):
        forbidden = ["get_state", "set_state", "read", "write", "save", "load",
                     "apply", "mutate", "commit", "replay", "restore", "execute",
                     "run", "model", "prompt"]
        svc_methods = [m for m in dir(StateStoreService) if not m.startswith("_")]
        for method_name in forbidden:
            assert method_name not in svc_methods, f"Forbidden method found: {method_name}"

    def test_service_create_record_ref(self):
        svc = StateStoreService()
        r = svc.create_record_ref(
            state_ref_id="ref-1",
            record_id="rec-1",
            record_type="actor",
            category="authoritative_runtime",
            authority_level="authoritative",
            visibility=_make_vis(),
        )
        assert isinstance(r, StateRecordRef)

    def test_service_validate_record_ref(self):
        svc = StateStoreService()
        assert svc.validate_record_ref(_make_ref()) is True

    def test_no_state_mutation_methods(self):
        mutation_methods = ["mutate", "apply_delta", "commit_event", "store", "persist"]
        for m in mutation_methods:
            assert not hasattr(StateStoreService, m)


class TestGuardrailsDomainPackage:
    def test_domain_package_contains_only_authorized_files(self):
        domain_dir = "src/astra_runtime/domain"
        authorized = {
            "__init__.py",
            "command_lifecycle.py",
            "action_legality.py",
            "state_store.py",
            "state_projection.py",
            "transaction_lifecycle.py",
            "event_commitment.py",
            "validation_integration.py",
            "validation_integration_bridge_skeleton.py",
            "transaction_preview_packet_bridge_skeleton.py",
            "resource_consequence_math.py",
            "context_packet_compiler.py",
            "model_boundary_evaluation.py",
            "tiny_vertical_slice.py", "scene_command_execution_skeleton.py",
            "command_kind_routing_skeleton.py", "__pycache__",
        }
        entries = set(os.listdir(domain_dir))
        unauthorized = entries - authorized
        assert not unauthorized, f"Unauthorized domain files found: {unauthorized}"

    def test_no_resource_math_module(self):
        assert not os.path.exists("src/astra_runtime/domain/resource_math.py")

    def test_no_combat_module(self):
        assert not os.path.exists("src/astra_runtime/domain/combat.py")

    def test_no_model_package(self):
        assert not os.path.exists("src/astra_runtime/model")

    def test_no_context_packet_compiler(self):
        assert not os.path.exists("src/astra_runtime/kernel/context_packet_compiler.py")


class TestValidatorParityStateStore:
    """Validator parity: validate_ functions must mirror constructor constraints."""

    def test_validate_record_ref_rejects_empty_schema_id(self):
        from types import MappingProxyType
        from astra_runtime.domain.state_store import StateRecordRef
        vis = _make_vis()
        # Bypass create helper to plant bad schema_id
        bad = StateRecordRef(
            state_ref_id="ref-1", record_id="rec-1", record_type="actor",
            category="authoritative_runtime", authority_level="authoritative",
            visibility=vis, schema_id="", source_event_id=None,
            source_delta_id=None, provenance_id=None, metadata=MappingProxyType({}),
        )
        assert validate_state_record_ref(bad) is False

    def test_validate_record_ref_rejects_empty_source_event_id(self):
        from types import MappingProxyType
        from astra_runtime.domain.state_store import StateRecordRef
        vis = _make_vis()
        bad = StateRecordRef(
            state_ref_id="ref-1", record_id="rec-1", record_type="actor",
            category="authoritative_runtime", authority_level="authoritative",
            visibility=vis, schema_id=None, source_event_id="",
            source_delta_id=None, provenance_id=None, metadata=MappingProxyType({}),
        )
        assert validate_state_record_ref(bad) is False

    def test_validate_record_ref_accepts_all_none_optionals(self):
        assert validate_state_record_ref(_make_ref(
            schema_id=None, source_event_id=None, source_delta_id=None, provenance_id=None
        )) is True

    def test_validate_snapshot_ref_rejects_empty_replay_audit_id(self):
        from types import MappingProxyType
        from astra_runtime.domain.state_store import StateSnapshotRef
        bad = StateSnapshotRef(
            snapshot_id="snap-1", snapshot_scope="session",
            state_ref_ids=("ref-1",), authority_level="authoritative",
            source_event_id=None, replay_audit_id="",
            persistence_boundary_id=None, metadata=MappingProxyType({}),
        )
        assert validate_state_snapshot_ref(bad) is False

    def test_validate_snapshot_ref_rejects_empty_source_event_id(self):
        from types import MappingProxyType
        from astra_runtime.domain.state_store import StateSnapshotRef
        bad = StateSnapshotRef(
            snapshot_id="snap-1", snapshot_scope="session",
            state_ref_ids=("ref-1",), authority_level="authoritative",
            source_event_id="", replay_audit_id=None,
            persistence_boundary_id=None, metadata=MappingProxyType({}),
        )
        assert validate_state_snapshot_ref(bad) is False

    def test_validate_snapshot_ref_accepts_all_none_optionals(self):
        assert validate_state_snapshot_ref(_make_snap(
            source_event_id=None, replay_audit_id=None, persistence_boundary_id=None
        )) is True


class TestDecisionLogTracking:
    """Verify PR-2A appears exactly once in the decision log."""

    def test_pr2a_id_appears_exactly_once(self):
        path = "docs/decisions/current_decisions_log.md"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        id_str = "RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001"
        # Count heading occurrences (## lines)
        heading = f"## {id_str}"
        count = content.count(heading)
        assert count == 1, f"Expected exactly 1 heading occurrence, found {count}"


class TestRegistryTracking:
    """Verify PR-2A registry record uses file_id and appears once."""

    def test_pr2a_file_id_appears_exactly_once(self):
        path = "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        file_id_str = "file_id: RUNTIME-DOMAIN-PR-2A-STATE-STORE-STATE-PROJECTION-SKELETON-IMPLEMENTATION-001"
        count = content.count(file_id_str)
        assert count == 1, f"Expected exactly 1 file_id occurrence, found {count}"

    def test_pr2a_changelog_entry_appears_exactly_once(self):
        path = "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        count = content.count("version: 0.1.71")
        assert count == 1, f"Expected exactly 1 v0.1.71 changelog entry, found {count}"
