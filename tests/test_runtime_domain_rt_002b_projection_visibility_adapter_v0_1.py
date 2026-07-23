"""Tests for RT-002B: Projection and Visibility Adapter v0.1.

Covers: module imports, constants, dataclass invariants, authority flag
enforcement, source-reference containment, descriptor validation, packet/result
metadata safety, backend and visible adapters, hidden-fact containment,
deterministic serializers, import boundaries, domain package exports,
registry/decision-log records, and upstream test pass-through.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import os
import pathlib
import subprocess
import sys
from typing import Any, Mapping

import pytest
import yaml
from tests.historical_branch_diff_guard import require_owning_historical_branch

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# T1 — Module imports successfully
# ---------------------------------------------------------------------------


class TestModuleImports:
    def test_import_module(self):
        import astra_runtime.domain.projection_visibility_adapter_v0_1  # noqa: F401

    def test_import_constants(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS,
            PROJECTION_DOWNSTREAM_CONSUMER_TYPES,
            PROJECTION_PACKET_KINDS,
            PROJECTION_REDACTION_REASONS,
            PROJECTION_VISIBILITY_ADAPTER_STATUSES,
            PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE,
            PROJECTION_VISIBILITY_TIERS,
        )
        assert isinstance(PROJECTION_VISIBILITY_ADAPTER_STATUSES, frozenset)
        assert isinstance(PROJECTION_VISIBILITY_TIERS, frozenset)
        assert isinstance(PROJECTION_PACKET_KINDS, frozenset)
        assert isinstance(PROJECTION_REDACTION_REASONS, frozenset)
        assert isinstance(PROJECTION_DOWNSTREAM_CONSUMER_TYPES, frozenset)
        assert isinstance(FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS, frozenset)
        assert isinstance(PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE, str)

    def test_import_dataclasses(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityAdapterResult,
            ProjectionVisibilityAuthorityFlags,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
        )
        for cls in (
            ProjectionVisibilityAuthorityFlags,
            ProjectionVisibilitySourceRef,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityAdapterResult,
        ):
            assert cls is not None

    def test_import_factories_adapters_serializers_validators(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_backend,
            adapt_vertical_slice_facade_result_for_downstream,
            adapt_vertical_slice_facade_result_for_visible,
            create_projection_visibility_adapter_packet,
            create_projection_visibility_adapter_result,
            create_projection_visibility_authority_flags,
            create_projection_visibility_descriptor,
            create_projection_visibility_source_ref,
            serialize_projection_visibility_adapter_packet,
            serialize_projection_visibility_adapter_packet_visible,
            serialize_projection_visibility_adapter_result,
            serialize_projection_visibility_adapter_result_visible,
            validate_projection_visibility_adapter_packet,
            validate_projection_visibility_adapter_result,
            validate_projection_visibility_authority_flags,
            validate_projection_visibility_descriptor,
            validate_projection_visibility_source_ref,
        )
        for func in (
            create_projection_visibility_authority_flags,
            create_projection_visibility_source_ref,
            create_projection_visibility_descriptor,
            create_projection_visibility_adapter_packet,
            create_projection_visibility_adapter_result,
            adapt_vertical_slice_facade_result_for_backend,
            adapt_vertical_slice_facade_result_for_visible,
            adapt_vertical_slice_facade_result_for_downstream,
            serialize_projection_visibility_adapter_packet,
            serialize_projection_visibility_adapter_packet_visible,
            serialize_projection_visibility_adapter_result,
            serialize_projection_visibility_adapter_result_visible,
            validate_projection_visibility_authority_flags,
            validate_projection_visibility_source_ref,
            validate_projection_visibility_descriptor,
            validate_projection_visibility_adapter_packet,
            validate_projection_visibility_adapter_result,
        ):
            assert callable(func)


# ---------------------------------------------------------------------------
# T2 — Constants exist and are frozen sets (covered by T1)
# ---------------------------------------------------------------------------


class TestConstants:
    def test_constants_are_frozen(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS,
            PROJECTION_DOWNSTREAM_CONSUMER_TYPES,
            PROJECTION_PACKET_KINDS,
            PROJECTION_REDACTION_REASONS,
            PROJECTION_VISIBILITY_ADAPTER_STATUSES,
            PROJECTION_VISIBILITY_TIERS,
        )
        for const in (
            PROJECTION_VISIBILITY_ADAPTER_STATUSES,
            PROJECTION_VISIBILITY_TIERS,
            PROJECTION_PACKET_KINDS,
            PROJECTION_REDACTION_REASONS,
            PROJECTION_DOWNSTREAM_CONSUMER_TYPES,
            FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS,
        ):
            assert isinstance(const, frozenset)


# ---------------------------------------------------------------------------
# T3 — Adapter statuses exclude forbidden adjudicative/execution statuses
# ---------------------------------------------------------------------------


class TestAdapterStatuses:
    def test_adapter_statuses_exclude_forbidden(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            PROJECTION_VISIBILITY_ADAPTER_STATUSES,
        )
        forbidden = {
            "legal", "illegal", "resolved", "executed", "committed",
            "mutated", "materialized", "authorized", "applied",
        }
        for status in forbidden:
            assert status not in PROJECTION_VISIBILITY_ADAPTER_STATUSES, (
                f"Adapter status constant should not contain {status!r}"
            )

    def test_adapter_statuses_include_allowed(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            PROJECTION_VISIBILITY_ADAPTER_STATUSES,
        )
        for status in (
            "backend_projection_available",
            "visible_projection_available",
            "redacted_projection_available",
            "unavailable",
            "deferred",
            "unknown",
        ):
            assert status in PROJECTION_VISIBILITY_ADAPTER_STATUSES


# ---------------------------------------------------------------------------
# T4 — Packet kinds are limited to allowed projection packets
# ---------------------------------------------------------------------------


class TestPacketKinds:
    def test_packet_kinds_limited(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            PROJECTION_PACKET_KINDS,
        )
        expected = {
            "backend_safe_projection",
            "visible_safe_projection",
            "redacted_projection",
            "unavailable_projection",
            "deferred_projection",
            "unknown_projection",
        }
        assert PROJECTION_PACKET_KINDS == expected


# ---------------------------------------------------------------------------
# T5 — All dataclasses are frozen and keyword-only
# ---------------------------------------------------------------------------


class TestDataclassInvariants:
    def _assert_frozen_kw_only(self, cls: type, **kwargs: Any) -> Any:
        obj = cls(**kwargs)
        first_field = dataclasses.fields(cls)[0].name
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(obj, first_field, "changed")
        return obj

    def test_authority_flags_frozen_kw_only(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityAuthorityFlags,
        )
        self._assert_frozen_kw_only(ProjectionVisibilityAuthorityFlags)

    def test_source_ref_frozen_kw_only(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilitySourceRef,
        )
        self._assert_frozen_kw_only(
            ProjectionVisibilitySourceRef,
            source_ref_id="ref1",
        )

    def test_descriptor_frozen_kw_only(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityDescriptor,
        )
        self._assert_frozen_kw_only(
            ProjectionVisibilityDescriptor,
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )

    def test_packet_frozen_kw_only(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
            ProjectionVisibilityAdapterPacket,
        )
        source_ref = ProjectionVisibilitySourceRef(source_ref_id="ref1")
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )
        self._assert_frozen_kw_only(
            ProjectionVisibilityAdapterPacket,
            packet_id="pkt1",
            adapter_status="visible_projection_available",
            owner_family="actor_identity_owner",
            entity_kind="actor",
            packet_kind="visible_safe_projection",
            source_reference=source_ref,
            visibility_descriptor=descriptor,
        )

    def test_result_frozen_kw_only(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityAdapterResult,
        )
        source_ref = ProjectionVisibilitySourceRef(source_ref_id="ref1")
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )
        packet = ProjectionVisibilityAdapterPacket(
            packet_id="pkt1",
            adapter_status="visible_projection_available",
            owner_family="actor_identity_owner",
            entity_kind="actor",
            packet_kind="visible_safe_projection",
            source_reference=source_ref,
            visibility_descriptor=descriptor,
        )
        self._assert_frozen_kw_only(
            ProjectionVisibilityAdapterResult,
            result_id="res1",
            adapter_status="visible_projection_available",
            packets=(packet,),
        )


# ---------------------------------------------------------------------------
# T6 — Authority flags reject all non-False values
# ---------------------------------------------------------------------------


class TestAuthorityFlags:
    def test_authority_flags_reject_non_false(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityAuthorityFlagsError,
            ProjectionVisibilityAuthorityFlags,
        )
        flag_names = [f.name for f in dataclasses.fields(ProjectionVisibilityAuthorityFlags)]
        for flag_name in flag_names:
            kwargs = {f: False for f in flag_names}
            for bad_value in (True, 1, "false", None, 0):
                kwargs[flag_name] = bad_value
                with pytest.raises(InvalidProjectionVisibilityAuthorityFlagsError):
                    ProjectionVisibilityAuthorityFlags(**kwargs)


# ---------------------------------------------------------------------------
# T7 — Authority flag to_dict() hardcodes false values
# ---------------------------------------------------------------------------


class TestAuthorityFlagsDict:
    def test_to_dict_hardcodes_false(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityAuthorityFlags,
        )
        flags = ProjectionVisibilityAuthorityFlags()
        d = flags.to_dict()
        assert isinstance(d, dict)
        for field_name in dataclasses.fields(ProjectionVisibilityAuthorityFlags):
            assert d[field_name.name] is False


# ---------------------------------------------------------------------------
# T8 — Source refs carry IDs only and no raw RT-002A records
# ---------------------------------------------------------------------------


class TestSourceRefs:
    def test_source_ref_id_only(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilitySourceRef,
        )
        ref = ProjectionVisibilitySourceRef(
            source_ref_id="facade-result-1",
            source_facade_result_id="facade-result-1",
            source_projection_id="proj_actor_1",
        )
        d = ref.to_dict()
        assert d["source_ref_id"] == "facade-result-1"
        assert d["source_facade_result_id"] == "facade-result-1"
        assert d["source_projection_id"] == "proj_actor_1"
        assert "record_payload" not in d
        assert "projection_payload" not in d
        assert "raw_state" not in d
        assert "hidden_fact" not in d

    def test_source_ref_rejects_raw_record_payload_in_metadata(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilitySourceRefError,
            ProjectionVisibilitySourceRef,
        )
        with pytest.raises(InvalidProjectionVisibilitySourceRefError):
            ProjectionVisibilitySourceRef(
                source_ref_id="ref1",
                metadata={"record_payload": {"scene_id": "s1"}},
            )


# ---------------------------------------------------------------------------
# T9 — Visibility descriptor rejects invalid values
# ---------------------------------------------------------------------------


class TestVisibilityDescriptor:
    def test_descriptor_rejects_invalid_packet_kind(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityDescriptorError,
            ProjectionVisibilityDescriptor,
        )
        with pytest.raises(InvalidProjectionVisibilityDescriptorError):
            ProjectionVisibilityDescriptor(
                visibility_tier="player_visible",
                packet_kind="illegal_projection",
            )

    def test_descriptor_rejects_invalid_visibility_tier(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityDescriptorError,
            ProjectionVisibilityDescriptor,
        )
        with pytest.raises(InvalidProjectionVisibilityDescriptorError):
            ProjectionVisibilityDescriptor(
                visibility_tier="gm_only_secret",
                packet_kind="backend_safe_projection",
            )

    def test_descriptor_rejects_invalid_redaction_reason(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityDescriptorError,
            ProjectionVisibilityDescriptor,
        )
        with pytest.raises(InvalidProjectionVisibilityDescriptorError):
            ProjectionVisibilityDescriptor(
                visibility_tier="player_visible",
                packet_kind="visible_safe_projection",
                redaction_reason="committed",
            )

    def test_descriptor_rejects_unsafe_reference_id_list(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityDescriptorError,
            ProjectionVisibilityDescriptor,
        )
        with pytest.raises(InvalidProjectionVisibilityDescriptorError):
            ProjectionVisibilityDescriptor(
                visibility_tier="player_visible",
                packet_kind="visible_safe_projection",
                safe_reference_ids=[""],
            )


# ---------------------------------------------------------------------------
# T10 — Adapter packets reject forbidden metadata keys recursively
# ---------------------------------------------------------------------------


class TestPacketMetadata:
    def test_packet_rejects_forbidden_keys(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityAdapterPacketError,
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
        )
        source_ref = ProjectionVisibilitySourceRef(source_ref_id="ref1")
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )
        forbidden_keys = [
            "hidden_fact",
            "secret",
            "backend_only_fact",
            "state_payload",
            "raw_state",
            "actual_state",
            "truth_payload",
            "projection_payload",
            "record_payload",
            "world_state",
        ]
        for key in forbidden_keys:
            with pytest.raises(InvalidProjectionVisibilityAdapterPacketError):
                ProjectionVisibilityAdapterPacket(
                    packet_id="pkt1",
                    adapter_status="visible_projection_available",
                    owner_family="actor_identity_owner",
                    entity_kind="actor",
                    packet_kind="visible_safe_projection",
                    source_reference=source_ref,
                    visibility_descriptor=descriptor,
                    metadata={key: "value"},
                )

    def test_packet_rejects_nested_forbidden_keys(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityAdapterPacketError,
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
        )
        source_ref = ProjectionVisibilitySourceRef(source_ref_id="ref1")
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )
        with pytest.raises(InvalidProjectionVisibilityAdapterPacketError):
            ProjectionVisibilityAdapterPacket(
                packet_id="pkt1",
                adapter_status="visible_projection_available",
                owner_family="actor_identity_owner",
                entity_kind="actor",
                packet_kind="visible_safe_projection",
                source_reference=source_ref,
                visibility_descriptor=descriptor,
                metadata={"outer": {"secret": "value"}},
            )


# ---------------------------------------------------------------------------
# T11 — Adapter results reject forbidden metadata keys recursively
# ---------------------------------------------------------------------------


class TestResultMetadata:
    def test_result_rejects_forbidden_keys(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityAdapterResultError,
            ProjectionVisibilityAdapterResult,
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
        )
        source_ref = ProjectionVisibilitySourceRef(source_ref_id="ref1")
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )
        packet = ProjectionVisibilityAdapterPacket(
            packet_id="pkt1",
            adapter_status="visible_projection_available",
            owner_family="actor_identity_owner",
            entity_kind="actor",
            packet_kind="visible_safe_projection",
            source_reference=source_ref,
            visibility_descriptor=descriptor,
        )
        with pytest.raises(InvalidProjectionVisibilityAdapterResultError):
            ProjectionVisibilityAdapterResult(
                result_id="res1",
                adapter_status="visible_projection_available",
                packets=(packet,),
                metadata={"hidden_facts": ["fact1"]},
            )

    def test_result_rejects_nested_forbidden_keys(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            InvalidProjectionVisibilityAdapterResultError,
            ProjectionVisibilityAdapterResult,
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
        )
        source_ref = ProjectionVisibilitySourceRef(source_ref_id="ref1")
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )
        packet = ProjectionVisibilityAdapterPacket(
            packet_id="pkt1",
            adapter_status="visible_projection_available",
            owner_family="actor_identity_owner",
            entity_kind="actor",
            packet_kind="visible_safe_projection",
            source_reference=source_ref,
            visibility_descriptor=descriptor,
        )
        with pytest.raises(InvalidProjectionVisibilityAdapterResultError):
            ProjectionVisibilityAdapterResult(
                result_id="res1",
                adapter_status="visible_projection_available",
                packets=(packet,),
                metadata={"outer": {"world_state": {"x": 1}}},
            )


# ---------------------------------------------------------------------------
# Helpers for facade-result fixtures
# ---------------------------------------------------------------------------


def _make_visible_object_facade_result() -> Any:
    from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
        create_vertical_slice_object_lever_record,
        create_vertical_slice_owner_facade_result,
        create_vertical_slice_owner_projection,
    )
    record = create_vertical_slice_object_lever_record(
        object_lever_id="lever_1",
        object_lever_label="Rusty Lever",
        source_scope="rt002b_test",
    )
    projection = create_vertical_slice_owner_projection(
        projection_id="proj_lever_1",
        entity_kind="object_lever",
        owner_family="object_interactable_owner",
        visibility_tier="player_visible",
        reference_id="lever_1",
        redaction_required=False,
        source_scope="rt002b_test",
    )
    return create_vertical_slice_owner_facade_result(
        result_id="facade_object_1",
        result_status="available_reference",
        owner_family="object_interactable_owner",
        entity_kind="object_lever",
        requested_reference=None,
        projection=projection,
        source_scope="rt002b_test",
    )


def _make_hidden_fact_facade_result(redacted_safe_label: str = "A hidden presence") -> Any:
    from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
        create_vertical_slice_hidden_fact_reference,
        create_vertical_slice_owner_facade_result,
        create_vertical_slice_owner_projection,
        create_vertical_slice_state_record_ref,
    )
    record = create_vertical_slice_hidden_fact_reference(
        hidden_fact_reference_id="hidden_1",
        redacted_safe_label=redacted_safe_label,
        source_scope="rt002b_test",
    )
    ref = create_vertical_slice_state_record_ref(
        reference_id="hidden_1",
        entity_kind="hidden_fact_reference",
        owner_family="hidden_information_visibility_owner",
        visibility_tier="hidden",
        source_scope="rt002b_test",
        record_status="redacted",
    )
    projection = create_vertical_slice_owner_projection(
        projection_id="proj_hidden_1",
        entity_kind="hidden_fact_reference",
        owner_family="hidden_information_visibility_owner",
        visibility_tier="hidden",
        reference_id="hidden_1",
        redacted_safe_label=redacted_safe_label,
        redaction_required=True,
        source_scope="rt002b_test",
    )
    return create_vertical_slice_owner_facade_result(
        result_id="facade_hidden_1",
        result_status="redacted",
        owner_family="hidden_information_visibility_owner",
        entity_kind="hidden_fact_reference",
        requested_reference=ref,
        projection=projection,
        source_scope="rt002b_test",
    )


def _make_unavailable_facade_result() -> Any:
    from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
        create_vertical_slice_owner_facade_result,
    )
    return create_vertical_slice_owner_facade_result(
        result_id="facade_unavailable_1",
        result_status="unavailable",
        owner_family="object_interactable_owner",
        entity_kind="object_lever",
        source_scope="rt002b_test",
    )


# ---------------------------------------------------------------------------
# T12 — Backend adapter accepts visible facade result -> backend-safe packet
# ---------------------------------------------------------------------------


class TestBackendAdapter:
    def test_backend_adapter_visible_result(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_backend,
        )
        facade_result = _make_visible_object_facade_result()
        result = adapt_vertical_slice_facade_result_for_backend(
            facade_result,
            packet_id="pkt_visible_1",
        )
        assert result.adapter_status == "visible_projection_available"
        packet = result.packets[0]
        assert packet.packet_kind == "visible_safe_projection"
        assert packet.owner_family == "object_interactable_owner"
        assert packet.entity_kind == "object_lever"
        assert packet.visibility_descriptor.visibility_tier == "player_visible"
        assert packet.visibility_descriptor.redaction_required is False
        assert "lever_1" in packet.visibility_descriptor.safe_reference_ids
        assert packet.source_reference.source_facade_result_id == "facade_object_1"


# ---------------------------------------------------------------------------
# T13 — Backend adapter accepts hidden fact -> redacted packet
# ---------------------------------------------------------------------------


class TestBackendAdapterHiddenFact:
    def test_backend_adapter_hidden_fact(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_backend,
        )
        facade_result = _make_hidden_fact_facade_result()
        result = adapt_vertical_slice_facade_result_for_backend(
            facade_result,
            packet_id="pkt_hidden_1",
        )
        assert result.adapter_status == "redacted_projection_available"
        packet = result.packets[0]
        assert packet.packet_kind == "redacted_projection"
        assert packet.owner_family == "hidden_information_visibility_owner"
        assert packet.entity_kind == "hidden_fact_reference"
        assert packet.visibility_descriptor.visibility_tier == "hidden"
        assert packet.visibility_descriptor.redaction_required is True
        assert packet.visibility_descriptor.redaction_reason == "hidden_fact"
        assert "hidden_1" in packet.visibility_descriptor.safe_reference_ids


# ---------------------------------------------------------------------------
# T14 — Visible adapter excludes metadata, flags, raw state, hidden facts, etc.
# ---------------------------------------------------------------------------


class TestVisibleAdapter:
    def test_visible_adapter_excludes_sensitive_fields(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_visible,
            serialize_projection_visibility_adapter_result_visible,
        )
        facade_result = _make_visible_object_facade_result()
        result = adapt_vertical_slice_facade_result_for_visible(
            facade_result,
            packet_id="pkt_visible_1",
        )
        visible = serialize_projection_visibility_adapter_result_visible(result)
        assert "authority_flags" not in visible
        assert "metadata" not in visible
        packet = visible["packets"][0]
        assert "authority_flags" not in packet
        assert "metadata" not in packet
        assert "source_scope" not in packet
        assert "source_facade_result_id" not in packet
        assert "source_projection_id" not in packet
        assert "raw_state" not in packet
        assert "hidden_fact" not in packet
        assert "backend_only" not in packet


# ---------------------------------------------------------------------------
# T15 — Visible adapter for hidden fact exposes only redaction-safe information
# ---------------------------------------------------------------------------


class TestVisibleAdapterHiddenFact:
    def test_visible_adapter_hidden_fact_redaction_only(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_visible,
            serialize_projection_visibility_adapter_packet_visible,
        )
        facade_result = _make_hidden_fact_facade_result()
        result = adapt_vertical_slice_facade_result_for_visible(
            facade_result,
            packet_id="pkt_hidden_visible_1",
        )
        packet = result.packets[0]
        visible_packet = serialize_projection_visibility_adapter_packet_visible(packet)
        assert "hidden_fact_reference_id" not in visible_packet
        assert "hidden_fact" not in visible_packet
        assert "source_facade_result_id" not in visible_packet
        assert "source_projection_id" not in visible_packet
        assert "metadata" not in visible_packet
        assert "authority_flags" not in visible_packet
        assert visible_packet["packet_kind"] == "redacted_projection"
        assert visible_packet["redaction_required"] is True
        assert visible_packet["redaction_reason"] == "hidden_fact"
        assert "hidden_1" in visible_packet["safe_reference_ids"]
        assert visible_packet.get("redacted_safe_label") == "A hidden presence"


# ---------------------------------------------------------------------------
# T16 — Missing/unavailable RT-002A result -> unavailable/deferred/unknown
# ---------------------------------------------------------------------------


class TestUnavailableBehavior:
    def test_unavailable_facade_result(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_backend,
        )
        facade_result = _make_unavailable_facade_result()
        result = adapt_vertical_slice_facade_result_for_backend(
            facade_result,
            packet_id="pkt_unavailable_1",
        )
        assert result.adapter_status == "unavailable"
        packet = result.packets[0]
        assert packet.packet_kind == "unavailable_projection"
        assert packet.visibility_descriptor.redaction_required is True
        assert packet.visibility_descriptor.redaction_reason == "unavailable"

    def test_missing_data_not_false_truth(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_backend,
        )
        facade_result = _make_unavailable_facade_result()
        result = adapt_vertical_slice_facade_result_for_backend(
            facade_result,
            packet_id="pkt_unavailable_1",
        )
        assert result.adapter_status != "visible_projection_available"
        assert result.adapter_status != "backend_projection_available"
        assert "legal" not in result.adapter_status
        assert "possible" not in result.adapter_status


# ---------------------------------------------------------------------------
# T17-T21 — Adapter output never contains legality/preview/commitment/mutation/narration fields
# ---------------------------------------------------------------------------


class TestOutputFieldContainment:
    _FORBIDDEN_FIELD_SUBSTRINGS = {
        # legality
        "legal", "illegal", "legality",
        # preview
        "transaction_preview", "preview_result",
        # commitment
        "event_commitment", "committed",
        # mutation/state-delta
        "state_delta", "mutation", "mutated", "state_mutation",
        # model/prompt/narration
        "model_call", "prompt", "narration", "narrate",
    }

    def _all_result_keys(
        self, d: Any, prefix: str = "", skip_authority_flags: bool = True,
    ) -> set[str]:
        keys: set[str] = set()
        if isinstance(d, dict):
            for k, v in d.items():
                key_str = str(k)
                if skip_authority_flags and key_str == "authority_flags":
                    continue
                keys.add(key_str)
                keys.update(self._all_result_keys(v, prefix=f"{prefix}.{key_str}"))
        elif isinstance(d, (list, tuple)):
            for item in d:
                keys.update(self._all_result_keys(item, prefix=prefix))
        return keys

    def test_backend_output_no_forbidden_fields(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_backend,
            serialize_projection_visibility_adapter_result,
        )
        facade_result = _make_visible_object_facade_result()
        result = adapt_vertical_slice_facade_result_for_backend(
            facade_result,
            packet_id="pkt_containment_1",
        )
        serialized = serialize_projection_visibility_adapter_result(result)
        keys = self._all_result_keys(serialized)
        for substring in self._FORBIDDEN_FIELD_SUBSTRINGS:
            matching = [k for k in keys if substring in k.lower()]
            assert not matching, (
                f"Forbidden field substring {substring!r} found in keys: {matching}"
            )

    def test_visible_output_no_forbidden_fields(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_visible,
            serialize_projection_visibility_adapter_result_visible,
        )
        facade_result = _make_visible_object_facade_result()
        result = adapt_vertical_slice_facade_result_for_visible(
            facade_result,
            packet_id="pkt_containment_visible_1",
        )
        serialized = serialize_projection_visibility_adapter_result_visible(result)
        keys = self._all_result_keys(serialized)
        for substring in self._FORBIDDEN_FIELD_SUBSTRINGS:
            matching = [k for k in keys if substring in k.lower()]
            assert not matching, (
                f"Forbidden field substring {substring!r} found in keys: {matching}"
            )


# ---------------------------------------------------------------------------
# T22-T23 — Serializers are deterministic and JSON-safe
# ---------------------------------------------------------------------------


class TestSerializers:
    def test_backend_serializer_deterministic_and_json_safe(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_backend,
            serialize_projection_visibility_adapter_result,
        )
        facade_result = _make_visible_object_facade_result()
        result = adapt_vertical_slice_facade_result_for_backend(
            facade_result,
            packet_id="pkt_det_1",
        )
        a = serialize_projection_visibility_adapter_result(result)
        b = serialize_projection_visibility_adapter_result(result)
        assert a == b
        json_text = json.dumps(a, sort_keys=True)
        assert json.loads(json_text) == a

    def test_visible_serializer_deterministic_and_json_safe(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            adapt_vertical_slice_facade_result_for_visible,
            serialize_projection_visibility_adapter_result_visible,
        )
        facade_result = _make_hidden_fact_facade_result()
        result = adapt_vertical_slice_facade_result_for_visible(
            facade_result,
            packet_id="pkt_det_visible_1",
        )
        a = serialize_projection_visibility_adapter_result_visible(result)
        b = serialize_projection_visibility_adapter_result_visible(result)
        assert a == b
        json_text = json.dumps(a, sort_keys=True)
        assert json.loads(json_text) == a


# ---------------------------------------------------------------------------
# T24 — Module imports no forbidden implementation modules
# ---------------------------------------------------------------------------


class TestImportBoundaries:
    _FORBIDDEN_MODULE_SUBSTRINGS = {
        "action_legality",
        "transaction_preview",
        "event_commitment",
        "state_store",
        "persistence",
        "resource_consequence_math",
        "rng",
        "model_boundary",
        "live_play",
    }

    def _collect_imports(self, module_path: pathlib.Path) -> set[str]:
        source = module_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.add(module)
                for alias in node.names:
                    imports.add(f"{module}.{alias.name}")
        return imports

    def test_module_imports_no_forbidden_modules(self):
        module_path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "projection_visibility_adapter_v0_1.py"
        imports = self._collect_imports(module_path)
        for substring in self._FORBIDDEN_MODULE_SUBSTRINGS:
            forbidden = [imp for imp in imports if substring in imp]
            assert not forbidden, (
                f"Forbidden module substring {substring!r} found in imports: {forbidden}"
            )


# ---------------------------------------------------------------------------
# T25 — Domain package exports the RT-002B public surface
# ---------------------------------------------------------------------------


class TestDomainExports:
    _EXPECTED_EXPORTS = {
        "PROJECTION_VISIBILITY_ADAPTER_STATUSES",
        "PROJECTION_VISIBILITY_TIERS",
        "PROJECTION_PACKET_KINDS",
        "PROJECTION_REDACTION_REASONS",
        "PROJECTION_DOWNSTREAM_CONSUMER_TYPES",
        "PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE",
        "FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS",
        "ProjectionVisibilityAdapterError",
        "InvalidProjectionVisibilityAuthorityFlagsError",
        "InvalidProjectionVisibilitySourceRefError",
        "InvalidProjectionVisibilityDescriptorError",
        "InvalidProjectionVisibilityAdapterPacketError",
        "InvalidProjectionVisibilityAdapterResultError",
        "ProjectionVisibilityAuthorityFlags",
        "ProjectionVisibilitySourceRef",
        "ProjectionVisibilityDescriptor",
        "ProjectionVisibilityAdapterPacket",
        "ProjectionVisibilityAdapterResult",
        "create_projection_visibility_authority_flags",
        "create_projection_visibility_source_ref",
        "create_projection_visibility_descriptor",
        "create_projection_visibility_adapter_packet",
        "create_projection_visibility_adapter_result",
        "adapt_vertical_slice_facade_result_for_backend",
        "adapt_vertical_slice_facade_result_for_visible",
        "adapt_vertical_slice_facade_result_for_downstream",
        "serialize_projection_visibility_adapter_packet",
        "serialize_projection_visibility_adapter_packet_visible",
        "serialize_projection_visibility_adapter_result",
        "serialize_projection_visibility_adapter_result_visible",
        "validate_projection_visibility_authority_flags",
        "validate_projection_visibility_source_ref",
        "validate_projection_visibility_descriptor",
        "validate_projection_visibility_adapter_packet",
        "validate_projection_visibility_adapter_result",
    }

    def test_exports_include_rt002b(self):
        from astra_runtime import domain
        domain_all = set(domain.__all__)
        missing = self._EXPECTED_EXPORTS - domain_all
        assert not missing, f"Missing RT-002B exports in domain.__all__: {missing}"


# ---------------------------------------------------------------------------
# T26 — Registry contains RT-002B file record
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_registry_contains_rt002b_module_record(self):
        registry_path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        rt002b_records = [
            r for r in registry.get("file_records", [])
            if "RT-002B" in str(r.get("file_id", ""))
            or "projection_visibility_adapter_v0_1" in str(r.get("filename", ""))
        ]
        assert rt002b_records, "Registry does not contain RT-002B module record"

    def test_registry_contains_rt002b_test_record(self):
        registry_path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        test_files: list[str] = []
        for record in registry.get("file_records", []):
            if "RT-002B" in str(record.get("file_id", "")):
                test_files.extend(record.get("test_files", []))
        assert "tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py" in test_files


# ---------------------------------------------------------------------------
# T27 — Decision log contains RT-002B entry
# ---------------------------------------------------------------------------


class TestDecisionLog:
    def test_decision_log_contains_rt002b(self):
        log_path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        text = log_path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-RT-002B" in text
        assert "projection and visibility adapter" in text.lower()
        assert "RT-002C" in text


# ---------------------------------------------------------------------------
# T28 — RT-002A tests still pass
# ---------------------------------------------------------------------------


class TestUpstreamPassThrough:
    def test_rt002a_tests_pass(self):
        # RT-002A's TestBranchDiffContained guardrail asserts that no runtime
        # implementation modules differ from origin/main. That guardrail is
        # correct for the RT-002A branch but legitimately fails on the RT-002B
        # branch because RT-002B adds a new runtime module and updates domain
        # exports. Run the functional tests only.
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_runtime_domain_rt_002a_read_only_vertical_slice_state_owner_facade.py",
                "-k", "not TestBranchDiffContained",
                "-q",
            ],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"RT-002A tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T29 — RT-001H and RT-001I tests still pass
# ---------------------------------------------------------------------------

    def test_rt001h_tests_pass(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py",
                "-q",
            ],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"RT-001H tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001i_tests_pass(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py",
                "-k", "not TestBranchDiffContained",
                "-q",
            ],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"RT-001I tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T30 — PR-9A through PR-9E seam tests still pass
# ---------------------------------------------------------------------------

    def test_pr9_seam_tests_pass(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_runtime_domain_pr_9a_scene_command_execution_skeleton.py",
                "tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py",
                "tests/test_runtime_domain_pr_9c_command_kind_routing_skeleton.py",
                "tests/test_runtime_domain_pr_9d_validation_integration_bridge_skeleton.py",
                "tests/test_runtime_domain_pr_9e_transaction_preview_packet_bridge_skeleton.py",
                "-q",
            ],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"PR-9 seam tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T31 — Branch diff does not modify unrelated runtime modules
# ---------------------------------------------------------------------------


class TestBranchDiff:
    def test_branch_diff_limited_to_rt002b(self):
        require_owning_historical_branch(REPO_ROOT, "rt-002b")
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        changed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
        allowed = {
            "src/astra_runtime/domain/projection_visibility_adapter_v0_1.py",
            "tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py",
            "src/astra_runtime/domain/__init__.py",
            "docs/decisions/current_decisions_log.md",
            "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
            # guardrail allowlist updates required by the new module
            "tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py",
            "tests/test_runtime_domain_rt_001e_action_legality_service_interface_contract_skeleton.py",
            # RT-002C follow-on files; RT-002B branch-diff guardrail must tolerate
            # downstream RT-002C additions because RT-002C depends on RT-002B.
            "src/astra_runtime/domain/object_lever_interaction_legality_reader.py",
            "tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py",
            # RT-002E follow-on files; RT-002B branch-diff guardrail must tolerate
            # downstream RT-002E additions because RT-002E depends on RT-002D/RT-002C/RT-002B.
            "src/astra_runtime/domain/object_lever_event_commit_state_delta_path.py",
            "tests/test_runtime_domain_rt_002e_object_lever_event_commit_state_delta_path.py",
            # RT-002F follow-on files; RT-002B branch-diff guardrail must tolerate
            # downstream RT-002F additions because RT-002F depends on RT-002E/RT-002D/RT-002C/RT-002B.
            "src/astra_runtime/domain/object_lever_replay_audit_check.py",
            "tests/test_runtime_domain_rt_002f_object_lever_replay_audit_check.py",
        }
        unexpected = changed - allowed
        assert not unexpected, (
            f"Branch diff modifies unexpected files: {unexpected}"
        )
