"""Tests for RT-002C: Object/Lever Interaction Legality Reader.

Covers: module imports, constants, dataclass invariants, authority flag
enforcement, command declaration containment, projection requirement validation,
input packet set containment, legality classification over RT-002B packets,
hidden-information containment, deterministic serializers, import boundaries,
domain package exports, registry/decision-log records, and upstream test
pass-through.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import os
import pathlib
import subprocess
import sys
from typing import Any

import pytest
import yaml
from tests.historical_branch_diff_guard import require_owning_historical_branch

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _visibility_tier_for_packet_kind(packet_kind: str) -> str:
    return {
        "visible_safe_projection": "player_visible",
        "backend_safe_projection": "backend_visible",
        "redacted_projection": "hidden",
        "unavailable_projection": "hidden",
        "deferred_projection": "hidden",
        "unknown_projection": "hidden",
    }.get(packet_kind, "hidden")


def _redaction_reason_for_packet_kind(packet_kind: str) -> str:
    return {
        "visible_safe_projection": "none",
        "backend_safe_projection": "backend_only",
        "redacted_projection": "hidden_fact",
        "unavailable_projection": "unavailable",
        "deferred_projection": "deferred",
        "unknown_projection": "unknown",
    }.get(packet_kind, "none")


def _make_packet(
    entity_kind: str,
    packet_kind: str,
    packet_id: str | None = None,
    safe_reference_ids: list[str] | None = None,
) -> Any:
    from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
        ProjectionVisibilityAdapterPacket,
        ProjectionVisibilityDescriptor,
        ProjectionVisibilitySourceRef,
    )
    from astra_runtime.domain.object_lever_interaction_legality_reader import (
        _ENTITY_TO_OWNER_FAMILY,
    )

    owner_family = _ENTITY_TO_OWNER_FAMILY[entity_kind]
    ref_id = safe_reference_ids[0] if safe_reference_ids else f"{entity_kind}_1"
    source_ref = ProjectionVisibilitySourceRef(source_ref_id=ref_id)
    descriptor = ProjectionVisibilityDescriptor(
        visibility_tier=_visibility_tier_for_packet_kind(packet_kind),
        packet_kind=packet_kind,
        redaction_required=packet_kind != "visible_safe_projection",
        redaction_reason=_redaction_reason_for_packet_kind(packet_kind),
        safe_reference_ids=safe_reference_ids or [ref_id],
    )
    adapter_status = {
        "visible_safe_projection": "visible_projection_available",
        "backend_safe_projection": "backend_projection_available",
        "redacted_projection": "redacted_projection_available",
        "unavailable_projection": "unavailable",
        "deferred_projection": "deferred",
        "unknown_projection": "unknown",
    }.get(packet_kind, "unknown")

    return ProjectionVisibilityAdapterPacket(
        packet_id=packet_id or f"pkt_{entity_kind}",
        adapter_status=adapter_status,
        owner_family=owner_family,
        entity_kind=entity_kind,
        packet_kind=packet_kind,
        source_reference=source_ref,
        visibility_descriptor=descriptor,
    )


def _make_command_declaration(
    command_id: str = "cmd_1",
    actor_ref_id: str = "actor_1",
    object_lever_ref_id: str = "lever_1",
    scene_ref_id: str = "scene_1",
) -> Any:
    from astra_runtime.domain.object_lever_interaction_legality_reader import (
        create_object_lever_interaction_command_declaration,
    )
    return create_object_lever_interaction_command_declaration(
        command_id=command_id,
        command_family="interact_with_object_lever",
        actor_ref_id=actor_ref_id,
        object_lever_ref_id=object_lever_ref_id,
        scene_ref_id=scene_ref_id,
    )


def _make_input_packet_set(
    packets: list[Any],
    packet_set_id: str = "ps_1",
) -> Any:
    from astra_runtime.domain.object_lever_interaction_legality_reader import (
        create_object_lever_legality_input_packet_set,
    )
    return create_object_lever_legality_input_packet_set(
        packet_set_id=packet_set_id,
        command_declaration=_make_command_declaration(),
        projection_packets=packets,
    )


def _read_legality(packets: list[Any]) -> Any:
    from astra_runtime.domain.object_lever_interaction_legality_reader import (
        read_object_lever_interaction_legality,
    )
    packet_set = _make_input_packet_set(packets)
    return read_object_lever_interaction_legality(
        packet_set,
        reading_id="reading_1",
        result_id="result_1",
    )


# ---------------------------------------------------------------------------
# T1 — Module imports successfully
# ---------------------------------------------------------------------------


class TestModuleImports:
    def test_import_module(self):
        import astra_runtime.domain.object_lever_interaction_legality_reader  # noqa: F401

    def test_import_constants(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS,
            OBJECT_LEVER_BLOCK_REASONS,
            OBJECT_LEVER_COMMAND_FAMILY,
            OBJECT_LEVER_LEGALITY_DECISIONS,
            OBJECT_LEVER_LEGALITY_READER_STATUSES,
            OBJECT_LEVER_NON_AUTHORITY_NOTE,
            OBJECT_LEVER_OPTIONAL_ENTITY_KINDS,
            OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES,
            OBJECT_LEVER_REQUIRED_ENTITY_KINDS,
            OBJECT_LEVER_REQUIRED_OWNER_FAMILIES,
        )
        for const in (
            OBJECT_LEVER_LEGALITY_READER_STATUSES,
            OBJECT_LEVER_LEGALITY_DECISIONS,
            OBJECT_LEVER_REQUIRED_ENTITY_KINDS,
            OBJECT_LEVER_OPTIONAL_ENTITY_KINDS,
            OBJECT_LEVER_REQUIRED_OWNER_FAMILIES,
            OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES,
            OBJECT_LEVER_BLOCK_REASONS,
            FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS,
        ):
            assert isinstance(const, frozenset)
        assert isinstance(OBJECT_LEVER_COMMAND_FAMILY, str)
        assert isinstance(OBJECT_LEVER_NON_AUTHORITY_NOTE, str)

    def test_import_dataclasses(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverInteractionCommandDeclaration,
            ObjectLeverInteractionLegalityAuthorityFlags,
            ObjectLeverLegalityInputPacketSet,
            ObjectLeverLegalityReaderResult,
            ObjectLeverLegalityReading,
            ObjectLeverProjectionRequirement,
        )
        for cls in (
            ObjectLeverInteractionLegalityAuthorityFlags,
            ObjectLeverInteractionCommandDeclaration,
            ObjectLeverProjectionRequirement,
            ObjectLeverLegalityInputPacketSet,
            ObjectLeverLegalityReading,
            ObjectLeverLegalityReaderResult,
        ):
            assert cls is not None

    def test_import_factories_reader_serializers_validators(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            build_object_lever_projection_requirements,
            create_object_lever_interaction_command_declaration,
            create_object_lever_interaction_legality_authority_flags,
            create_object_lever_legality_input_packet_set,
            create_object_lever_legality_reader_result,
            create_object_lever_legality_reading,
            create_object_lever_projection_requirement,
            read_object_lever_interaction_legality,
            serialize_object_lever_legality_reader_result,
            serialize_object_lever_legality_reader_result_visible,
            serialize_object_lever_legality_reading,
            serialize_object_lever_legality_reading_visible,
            validate_object_lever_interaction_command_declaration,
            validate_object_lever_interaction_legality_authority_flags,
            validate_object_lever_legality_input_packet_set,
            validate_object_lever_legality_reader_result,
            validate_object_lever_legality_reading,
            validate_object_lever_projection_requirement,
        )
        for func in (
            create_object_lever_interaction_legality_authority_flags,
            create_object_lever_interaction_command_declaration,
            create_object_lever_projection_requirement,
            create_object_lever_legality_input_packet_set,
            create_object_lever_legality_reading,
            create_object_lever_legality_reader_result,
            build_object_lever_projection_requirements,
            read_object_lever_interaction_legality,
            serialize_object_lever_legality_reading,
            serialize_object_lever_legality_reading_visible,
            serialize_object_lever_legality_reader_result,
            serialize_object_lever_legality_reader_result_visible,
            validate_object_lever_interaction_legality_authority_flags,
            validate_object_lever_interaction_command_declaration,
            validate_object_lever_projection_requirement,
            validate_object_lever_legality_input_packet_set,
            validate_object_lever_legality_reading,
            validate_object_lever_legality_reader_result,
        ):
            assert callable(func)


# ---------------------------------------------------------------------------
# T2 — Constants exist and are frozen sets
# ---------------------------------------------------------------------------


class TestConstants:
    def test_constants_are_frozen(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS,
            OBJECT_LEVER_BLOCK_REASONS,
            OBJECT_LEVER_LEGALITY_DECISIONS,
            OBJECT_LEVER_LEGALITY_READER_STATUSES,
            OBJECT_LEVER_OPTIONAL_ENTITY_KINDS,
            OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES,
            OBJECT_LEVER_REQUIRED_ENTITY_KINDS,
            OBJECT_LEVER_REQUIRED_OWNER_FAMILIES,
        )
        for const in (
            OBJECT_LEVER_LEGALITY_READER_STATUSES,
            OBJECT_LEVER_LEGALITY_DECISIONS,
            OBJECT_LEVER_REQUIRED_ENTITY_KINDS,
            OBJECT_LEVER_OPTIONAL_ENTITY_KINDS,
            OBJECT_LEVER_REQUIRED_OWNER_FAMILIES,
            OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES,
            OBJECT_LEVER_BLOCK_REASONS,
            FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS,
        ):
            assert isinstance(const, frozenset)


# ---------------------------------------------------------------------------
# T3 — Command family is exactly interact_with_object_lever
# ---------------------------------------------------------------------------


class TestCommandFamily:
    def test_command_family_exact(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            OBJECT_LEVER_COMMAND_FAMILY,
        )
        assert OBJECT_LEVER_COMMAND_FAMILY == "interact_with_object_lever"


# ---------------------------------------------------------------------------
# T4/T5 — Required and optional entity kinds are exact
# ---------------------------------------------------------------------------


class TestEntityKinds:
    def test_required_entity_kinds_exact(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            OBJECT_LEVER_REQUIRED_ENTITY_KINDS,
        )
        assert OBJECT_LEVER_REQUIRED_ENTITY_KINDS == {
            "scene", "actor", "object_lever",
        }

    def test_optional_entity_kinds_exact(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            OBJECT_LEVER_OPTIONAL_ENTITY_KINDS,
        )
        assert OBJECT_LEVER_OPTIONAL_ENTITY_KINDS == {
            "npc_target", "hazard_clock", "visible_condition", "hidden_fact_reference",
        }


# ---------------------------------------------------------------------------
# T6 — Reader statuses exclude forbidden adjudicative/execution statuses
# ---------------------------------------------------------------------------


class TestReaderStatuses:
    def test_reader_statuses_exclude_forbidden(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            OBJECT_LEVER_LEGALITY_READER_STATUSES,
        )
        forbidden = {
            "executed", "resolved", "committed", "mutated", "applied",
            "preview_materialized", "event_appended", "event_committed",
            "state_delta_applied", "success", "failure",
        }
        for status in forbidden:
            assert status not in OBJECT_LEVER_LEGALITY_READER_STATUSES, (
                f"Reader status constant should not contain {status!r}"
            )

    def test_reader_statuses_include_allowed(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            OBJECT_LEVER_LEGALITY_READER_STATUSES,
        )
        for status in (
            "legality_read_available",
            "blocked_by_projection",
            "blocked_by_visibility",
            "deferred",
            "unknown",
            "insufficient_projection",
        ):
            assert status in OBJECT_LEVER_LEGALITY_READER_STATUSES


# ---------------------------------------------------------------------------
# T7 — All dataclasses are frozen and keyword-only
# ---------------------------------------------------------------------------


class TestDataclassInvariants:
    def _assert_frozen_kw_only(self, cls: type, **kwargs: Any) -> Any:
        obj = cls(**kwargs)
        first_field = dataclasses.fields(cls)[0].name
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(obj, first_field, "changed")
        return obj

    def test_authority_flags_frozen_kw_only(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverInteractionLegalityAuthorityFlags,
        )
        self._assert_frozen_kw_only(ObjectLeverInteractionLegalityAuthorityFlags)

    def test_command_declaration_frozen_kw_only(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverInteractionCommandDeclaration,
        )
        self._assert_frozen_kw_only(
            ObjectLeverInteractionCommandDeclaration,
            command_id="cmd_1",
            command_family="interact_with_object_lever",
            actor_ref_id="actor_1",
            object_lever_ref_id="lever_1",
            scene_ref_id="scene_1",
        )

    def test_projection_requirement_frozen_kw_only(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverProjectionRequirement,
        )
        self._assert_frozen_kw_only(
            ObjectLeverProjectionRequirement,
            entity_kind="scene",
            owner_family="scene_location_owner",
            required=True,
            requirement_status="available",
        )

    def test_input_packet_set_frozen_kw_only(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverLegalityInputPacketSet,
        )
        cmd = _make_command_declaration()
        self._assert_frozen_kw_only(
            ObjectLeverLegalityInputPacketSet,
            packet_set_id="ps_1",
            command_declaration=cmd,
            projection_packets=(),
        )

    def test_legality_reading_frozen_kw_only(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverLegalityReading,
        )
        self._assert_frozen_kw_only(
            ObjectLeverLegalityReading,
            reading_id="reading_1",
            reader_status="legality_read_available",
            legality_decision="permitted_for_preview",
            command_family="interact_with_object_lever",
            requirement_readings=(),
        )

    def test_reader_result_frozen_kw_only(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverLegalityReading,
            ObjectLeverLegalityReaderResult,
        )
        reading = ObjectLeverLegalityReading(
            reading_id="reading_1",
            reader_status="legality_read_available",
            legality_decision="permitted_for_preview",
            command_family="interact_with_object_lever",
            requirement_readings=(),
        )
        self._assert_frozen_kw_only(
            ObjectLeverLegalityReaderResult,
            result_id="result_1",
            reader_status="legality_read_available",
            legality_decision="permitted_for_preview",
            legality_reading=reading,
        )


# ---------------------------------------------------------------------------
# T8 — Authority flags reject all non-False values
# ---------------------------------------------------------------------------


class TestAuthorityFlags:
    def test_authority_flags_reject_non_false(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverInteractionLegalityAuthorityFlagsError,
            ObjectLeverInteractionLegalityAuthorityFlags,
        )
        flag_names = [f.name for f in dataclasses.fields(ObjectLeverInteractionLegalityAuthorityFlags)]
        for flag_name in flag_names:
            kwargs = {f: False for f in flag_names}
            for bad_value in (True, 1, "false", None, 0):
                kwargs[flag_name] = bad_value
                with pytest.raises(InvalidObjectLeverInteractionLegalityAuthorityFlagsError):
                    ObjectLeverInteractionLegalityAuthorityFlags(**kwargs)


# ---------------------------------------------------------------------------
# T9 — Authority flag to_dict() hardcodes false values
# ---------------------------------------------------------------------------


class TestAuthorityFlagsDict:
    def test_to_dict_hardcodes_false(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            ObjectLeverInteractionLegalityAuthorityFlags,
        )
        flags = ObjectLeverInteractionLegalityAuthorityFlags()
        d = flags.to_dict()
        assert isinstance(d, dict)
        for field_name in dataclasses.fields(ObjectLeverInteractionLegalityAuthorityFlags):
            assert d[field_name.name] is False


# ---------------------------------------------------------------------------
# T10 — Command declaration rejects any command family except interact_with_object_lever
# ---------------------------------------------------------------------------


class TestCommandDeclaration:
    def test_command_declaration_rejects_wrong_family(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverInteractionCommandDeclarationError,
            create_object_lever_interaction_command_declaration,
        )
        with pytest.raises(InvalidObjectLeverInteractionCommandDeclarationError):
            create_object_lever_interaction_command_declaration(
                command_id="cmd_1",
                command_family="move_actor",
                actor_ref_id="actor_1",
                object_lever_ref_id="lever_1",
                scene_ref_id="scene_1",
            )

    def test_command_declaration_accepts_correct_family(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            create_object_lever_interaction_command_declaration,
        )
        decl = create_object_lever_interaction_command_declaration(
            command_id="cmd_1",
            command_family="interact_with_object_lever",
            actor_ref_id="actor_1",
            object_lever_ref_id="lever_1",
            scene_ref_id="scene_1",
            declared_intent_label="pull",
        )
        assert decl.command_family == "interact_with_object_lever"
        assert decl.actor_ref_id == "actor_1"
        assert decl.object_lever_ref_id == "lever_1"
        assert decl.scene_ref_id == "scene_1"
        assert decl.declared_intent_label == "pull"


# ---------------------------------------------------------------------------
# T11 — Command declaration carries IDs only
# ---------------------------------------------------------------------------


class TestCommandDeclarationIdsOnly:
    def test_command_declaration_no_parser_output(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            create_object_lever_interaction_command_declaration,
        )
        decl = _make_command_declaration()
        d = decl.to_dict()
        assert "natural_language" not in d
        assert "parsed_intent" not in d
        assert "effect_description" not in d
        assert "execution_arguments" not in d
        assert d["command_id"] == "cmd_1"
        assert d["actor_ref_id"] == "actor_1"


# ---------------------------------------------------------------------------
# T12 — Projection requirement validates fields
# ---------------------------------------------------------------------------


class TestProjectionRequirement:
    def test_projection_requirement_valid(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            create_object_lever_projection_requirement,
        )
        req = create_object_lever_projection_requirement(
            entity_kind="scene",
            owner_family="scene_location_owner",
            required=True,
            requirement_status="available",
            safe_reference_ids=["scene_1"],
        )
        assert req.entity_kind == "scene"
        assert req.owner_family == "scene_location_owner"
        assert req.required is True
        assert req.requirement_status == "available"
        assert req.safe_reference_ids == ("scene_1",)
        assert req.block_reason is None

    def test_projection_requirement_rejects_invalid_entity_kind(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverProjectionRequirementError,
            create_object_lever_projection_requirement,
        )
        with pytest.raises(InvalidObjectLeverProjectionRequirementError):
            create_object_lever_projection_requirement(
                entity_kind="spell_effect",
                owner_family="scene_location_owner",
                required=True,
                requirement_status="available",
            )

    def test_projection_requirement_rejects_invalid_owner_family(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverProjectionRequirementError,
            create_object_lever_projection_requirement,
        )
        with pytest.raises(InvalidObjectLeverProjectionRequirementError):
            create_object_lever_projection_requirement(
                entity_kind="scene",
                owner_family="unknown_owner",
                required=True,
                requirement_status="available",
            )

    def test_projection_requirement_rejects_invalid_requirement_status(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverProjectionRequirementError,
            create_object_lever_projection_requirement,
        )
        with pytest.raises(InvalidObjectLeverProjectionRequirementError):
            create_object_lever_projection_requirement(
                entity_kind="scene",
                owner_family="scene_location_owner",
                required=True,
                requirement_status="executed",
            )

    def test_projection_requirement_rejects_invalid_block_reason(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverProjectionRequirementError,
            create_object_lever_projection_requirement,
        )
        with pytest.raises(InvalidObjectLeverProjectionRequirementError):
            create_object_lever_projection_requirement(
                entity_kind="scene",
                owner_family="scene_location_owner",
                required=True,
                requirement_status="missing",
                block_reason="committed",
            )


# ---------------------------------------------------------------------------
# T13 — Input packet set accepts RT-002B packets and rejects non-RT-002B objects
# ---------------------------------------------------------------------------


class TestInputPacketSet:
    def test_input_packet_set_accepts_rt002b_packets(self):
        packet = _make_packet("scene", "visible_safe_projection")
        packet_set = _make_input_packet_set([packet])
        assert len(packet_set.projection_packets) == 1

    def test_input_packet_set_rejects_non_rt002b_objects(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverLegalityInputPacketSetError,
            create_object_lever_legality_input_packet_set,
        )
        with pytest.raises(InvalidObjectLeverLegalityInputPacketSetError):
            create_object_lever_legality_input_packet_set(
                packet_set_id="ps_1",
                command_declaration=_make_command_declaration(),
                projection_packets=["not_a_packet"],  # type: ignore[list-item]
            )


# ---------------------------------------------------------------------------
# T14 — Input packet set carries no RT-002A raw records
# ---------------------------------------------------------------------------


class TestInputPacketSetNoRawRecords:
    def test_input_packet_set_has_no_raw_record_fields(self):
        packet = _make_packet("scene", "visible_safe_projection")
        packet_set = _make_input_packet_set([packet])
        d = packet_set.to_dict()
        assert "record_payload" not in d
        assert "projection_payload" not in d
        assert "raw_state" not in d
        assert "hidden_fact" not in d
        assert "actual_state" not in d


# ---------------------------------------------------------------------------
# T15 — Metadata rejects forbidden keys recursively on all dataclasses
# ---------------------------------------------------------------------------


class TestMetadataForbiddenKeys:
    def _packet(self):
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
        )
        source_ref = ProjectionVisibilitySourceRef(source_ref_id="ref1")
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier="player_visible",
            packet_kind="visible_safe_projection",
        )
        return source_ref, descriptor

    def test_command_declaration_rejects_forbidden_keys(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverInteractionCommandDeclarationError,
            create_object_lever_interaction_command_declaration,
        )
        forbidden_keys = [
            "hidden_fact", "secret", "backend_only_fact", "state_payload",
            "raw_state", "actual_state", "truth_payload", "projection_payload",
            "record_payload", "world_state", "transaction_preview",
            "event_commitment", "state_delta", "mutation_payload", "execution_result",
        ]
        for key in forbidden_keys:
            with pytest.raises(InvalidObjectLeverInteractionCommandDeclarationError):
                create_object_lever_interaction_command_declaration(
                    command_id="cmd_1",
                    command_family="interact_with_object_lever",
                    actor_ref_id="actor_1",
                    object_lever_ref_id="lever_1",
                    scene_ref_id="scene_1",
                    metadata={key: "value"},
                )

    def test_command_declaration_rejects_nested_forbidden_keys(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverInteractionCommandDeclarationError,
            create_object_lever_interaction_command_declaration,
        )
        with pytest.raises(InvalidObjectLeverInteractionCommandDeclarationError):
            create_object_lever_interaction_command_declaration(
                command_id="cmd_1",
                command_family="interact_with_object_lever",
                actor_ref_id="actor_1",
                object_lever_ref_id="lever_1",
                scene_ref_id="scene_1",
                metadata={"outer": {"secret": "value"}},
            )

    def test_input_packet_set_rejects_forbidden_keys(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverLegalityInputPacketSetError,
            create_object_lever_legality_input_packet_set,
        )
        with pytest.raises(InvalidObjectLeverLegalityInputPacketSetError):
            create_object_lever_legality_input_packet_set(
                packet_set_id="ps_1",
                command_declaration=_make_command_declaration(),
                projection_packets=[_make_packet("scene", "visible_safe_projection")],
                metadata={"state_payload": {"x": 1}},
            )

    def test_legality_reading_rejects_forbidden_keys(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverLegalityReadingError,
            ObjectLeverLegalityReading,
        )
        with pytest.raises(InvalidObjectLeverLegalityReadingError):
            ObjectLeverLegalityReading(
                reading_id="reading_1",
                reader_status="legality_read_available",
                legality_decision="permitted_for_preview",
                command_family="interact_with_object_lever",
                requirement_readings=(),
                metadata={"execution_result": "success"},
            )

    def test_reader_result_rejects_forbidden_keys(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            InvalidObjectLeverLegalityReaderResultError,
            ObjectLeverLegalityReading,
            ObjectLeverLegalityReaderResult,
        )
        reading = ObjectLeverLegalityReading(
            reading_id="reading_1",
            reader_status="legality_read_available",
            legality_decision="permitted_for_preview",
            command_family="interact_with_object_lever",
            requirement_readings=(),
        )
        with pytest.raises(InvalidObjectLeverLegalityReaderResultError):
            ObjectLeverLegalityReaderResult(
                result_id="result_1",
                reader_status="legality_read_available",
                legality_decision="permitted_for_preview",
                legality_reading=reading,
                metadata={"transaction_preview": {"x": 1}},
            )


# ---------------------------------------------------------------------------
# T16-T23 — Legality classification over RT-002B packets
# ---------------------------------------------------------------------------


class TestLegalityClassification:
    def test_all_required_available_permitted_for_preview(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "permitted_for_preview"
        assert result.reader_status == "legality_read_available"
        assert result.legality_reading.legality_decision == "permitted_for_preview"

    def test_missing_scene_packet_insufficient_projection(self):
        result = _read_legality([
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "insufficient_projection"
        assert result.reader_status == "insufficient_projection"
        assert "missing_scene_projection" in result.legality_reading.block_reasons

    def test_missing_actor_packet_insufficient_projection(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "insufficient_projection"
        assert "missing_actor_projection" in result.legality_reading.block_reasons

    def test_missing_object_lever_packet_insufficient_projection(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
        ])
        assert result.legality_decision == "insufficient_projection"
        assert "missing_object_lever_projection" in result.legality_reading.block_reasons

    def test_required_unavailable_blocked(self):
        result = _read_legality([
            _make_packet("scene", "unavailable_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "blocked"
        assert result.reader_status == "blocked_by_projection"
        assert "unavailable_scene_projection" in result.legality_reading.block_reasons

    def test_required_deferred_deferred(self):
        result = _read_legality([
            _make_packet("scene", "deferred_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "deferred"
        assert result.reader_status == "deferred"

    def test_required_unknown_unknown(self):
        result = _read_legality([
            _make_packet("scene", "unknown_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "unknown"
        assert result.reader_status == "unknown"

    def test_required_redacted_blocked_by_visibility(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "redacted_projection"),
        ])
        assert result.legality_decision == "blocked"
        assert result.reader_status == "blocked_by_visibility"
        assert "redacted_required_projection" in result.legality_reading.block_reasons

    def test_backend_only_required_blocked(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "backend_safe_projection"),
        ])
        assert result.legality_decision == "blocked"
        assert result.reader_status == "blocked_by_projection"
        assert "backend_only_required_projection" in result.legality_reading.block_reasons


# ---------------------------------------------------------------------------
# T24 — Hidden fact packet redacted does not block by itself
# ---------------------------------------------------------------------------


class TestHiddenFactRedacted:
    def test_hidden_fact_redacted_does_not_block(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
            _make_packet("hidden_fact_reference", "redacted_projection"),
        ])
        assert result.legality_decision == "permitted_for_preview"
        assert result.reader_status == "legality_read_available"


# ---------------------------------------------------------------------------
# T25 — Hidden fact absence does not block by itself
# ---------------------------------------------------------------------------


class TestHiddenFactAbsence:
    def test_hidden_fact_absence_does_not_block(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "permitted_for_preview"
        assert result.reader_status == "legality_read_available"


# ---------------------------------------------------------------------------
# T26 — NPC/hazard/condition packets are optional and do not block by absence
# ---------------------------------------------------------------------------


class TestOptionalPackets:
    def test_optional_packets_absent_do_not_block(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "permitted_for_preview"

    def test_optional_packets_present_do_not_block(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
            _make_packet("npc_target", "visible_safe_projection"),
            _make_packet("hazard_clock", "visible_safe_projection"),
            _make_packet("visible_condition", "visible_safe_projection"),
        ])
        assert result.legality_decision == "permitted_for_preview"


# ---------------------------------------------------------------------------
# Owner-family mismatch checks
# ---------------------------------------------------------------------------


class TestOwnerFamilyMismatch:
    def _make_packet_with_owner(
        self, entity_kind: str, owner_family: str, packet_kind: str,
    ) -> Any:
        from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
            ProjectionVisibilityAdapterPacket,
            ProjectionVisibilityDescriptor,
            ProjectionVisibilitySourceRef,
        )
        ref_id = f"{entity_kind}_1"
        source_ref = ProjectionVisibilitySourceRef(source_ref_id=ref_id)
        descriptor = ProjectionVisibilityDescriptor(
            visibility_tier=_visibility_tier_for_packet_kind(packet_kind),
            packet_kind=packet_kind,
            redaction_required=packet_kind != "visible_safe_projection",
            redaction_reason=_redaction_reason_for_packet_kind(packet_kind),
            safe_reference_ids=[ref_id],
        )
        adapter_status = {
            "visible_safe_projection": "visible_projection_available",
            "backend_safe_projection": "backend_projection_available",
            "redacted_projection": "redacted_projection_available",
            "unavailable_projection": "unavailable",
            "deferred_projection": "deferred",
            "unknown_projection": "unknown",
        }.get(packet_kind, "unknown")
        return ProjectionVisibilityAdapterPacket(
            packet_id=f"pkt_{entity_kind}",
            adapter_status=adapter_status,
            owner_family=owner_family,
            entity_kind=entity_kind,
            packet_kind=packet_kind,
            source_reference=source_ref,
            visibility_descriptor=descriptor,
        )

    def test_object_lever_with_actor_owner_does_not_permit(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            self._make_packet_with_owner(
                "object_lever", "actor_identity_owner", "visible_safe_projection",
            ),
        ])
        assert result.legality_decision == "blocked"
        assert result.reader_status == "blocked_by_projection"
        reasons = result.legality_reading.block_reasons
        assert any("owner_family_mismatch" in r for r in reasons)

    def test_scene_with_object_owner_does_not_satisfy_scene(self):
        result = _read_legality([
            self._make_packet_with_owner(
                "scene", "object_interactable_owner", "visible_safe_projection",
            ),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "blocked"
        assert "scene_owner_family_mismatch" in result.legality_reading.block_reasons

    def test_actor_with_scene_owner_does_not_satisfy_actor(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            self._make_packet_with_owner(
                "actor", "scene_location_owner", "visible_safe_projection",
            ),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "blocked"
        assert "actor_owner_family_mismatch" in result.legality_reading.block_reasons

    def test_optional_packet_owner_mismatch_does_not_block_required(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
            self._make_packet_with_owner(
                "npc_target", "scene_location_owner", "visible_safe_projection",
            ),
        ])
        assert result.legality_decision == "permitted_for_preview"
        # Optional mismatch is recorded but does not block.
        npc_req = [
            r for r in result.legality_reading.requirement_readings
            if r.entity_kind == "npc_target"
        ][0]
        assert npc_req.requirement_status == "unknown"
        assert npc_req.block_reason is None

    def test_owner_mismatch_does_not_expose_hidden_or_execution_data(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            self._make_packet_with_owner(
                "object_lever", "actor_identity_owner", "visible_safe_projection",
            ),
        ])
        d = result.to_dict()
        text = json.dumps(d)
        # No hidden facts, execution outcomes, previews, events, or mutations.
        keys = set()
        def _walk(obj: Any) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    keys.add(k)
                    _walk(v)
            elif isinstance(obj, (list, tuple)):
                for item in obj:
                    _walk(item)
        _walk(d)
        assert "hidden_fact" not in keys
        assert "execution_result" not in keys
        assert "transaction_preview" not in keys
        assert "event_commitment" not in keys
        assert "state_delta" not in keys
        assert "mutation_payload" not in keys
        assert "executed" not in text
        assert "success" not in text
        assert "failure" not in text


# ---------------------------------------------------------------------------
# T27 — Reader never exposes hidden fact payloads
# ---------------------------------------------------------------------------


class TestHiddenFactContainment:
    def _collect_keys(self, obj: Any, skip_keys: set[str] | None = None) -> set[str]:
        keys: set[str] = set()
        skip = skip_keys or set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.add(k)
                if k not in skip:
                    keys.update(self._collect_keys(v, skip_keys=skip))
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                keys.update(self._collect_keys(item, skip_keys=skip))
        return keys

    def test_result_has_no_hidden_fact_payload(self):
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
            _make_packet("hidden_fact_reference", "redacted_projection"),
        ])
        d = result.to_dict()
        keys = self._collect_keys(d, skip_keys={"authority_flags"})
        assert "hidden_fact" not in keys
        assert "hidden_facts" not in keys
        assert "secret" not in keys
        assert "secrets" not in keys
        assert "truth_payload" not in keys


# ---------------------------------------------------------------------------
# T28 — Reader never treats missing data as false truth
# ---------------------------------------------------------------------------


class TestMissingDataNotTruth:
    def test_missing_data_does_not_claim_truth(self):
        result = _read_legality([
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        assert result.legality_decision == "insufficient_projection"
        for reason in result.legality_reading.block_reasons:
            assert "safe" not in reason
            assert "trapped" not in reason
            assert "usable" not in reason
            assert "locked" not in reason


# ---------------------------------------------------------------------------
# T29-T33 — Reader output contains no forbidden execution/preview/event fields
# ---------------------------------------------------------------------------


class TestOutputContainment:
    def _result(self):
        return _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])

    def _collect_keys(self, obj: Any, skip_keys: set[str] | None = None) -> set[str]:
        keys: set[str] = set()
        skip = skip_keys or set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.add(k)
                if k not in skip:
                    keys.update(self._collect_keys(v, skip_keys=skip))
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                keys.update(self._collect_keys(item, skip_keys=skip))
        return keys

    def test_no_execution_fields(self):
        d = self._result().to_dict()
        keys = self._collect_keys(d, skip_keys={"authority_flags"})
        assert "execution_result" not in keys
        # 'executed', 'resolved', 'success', 'failure' are forbidden decision/status
        # values and should not appear as legality decisions or statuses.
        assert d["legality_decision"] != "executed"
        assert d["reader_status"] != "executed"
        assert d["legality_decision"] != "resolved"
        assert d["legality_decision"] not in ("success", "failure")

    def test_no_transaction_preview_fields(self):
        d = self._result().to_dict()
        keys = self._collect_keys(d, skip_keys={"authority_flags"})
        assert "transaction_preview" not in keys
        assert "preview_materialized" not in keys

    def test_no_event_commitment_fields(self):
        d = self._result().to_dict()
        keys = self._collect_keys(d, skip_keys={"authority_flags"})
        assert "event_commitment" not in keys
        assert "event_appended" not in keys
        assert "event_committed" not in keys

    def test_no_mutation_or_state_delta_fields(self):
        d = self._result().to_dict()
        keys = self._collect_keys(d, skip_keys={"authority_flags"})
        assert "state_delta" not in keys
        assert "mutation_payload" not in keys
        assert "mutated" not in keys
        assert "applied" not in keys

    def test_no_model_prompt_or_narration_fields(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            serialize_object_lever_legality_reader_result_visible,
        )
        visible = serialize_object_lever_legality_reader_result_visible(self._result())
        keys = self._collect_keys(visible)
        assert "prompt" not in keys
        assert "narration" not in keys
        assert "model_call" not in keys


# ---------------------------------------------------------------------------
# T34-T35 — Serializers deterministic and JSON-safe
# ---------------------------------------------------------------------------


class TestSerializers:
    def test_backend_serializer_deterministic_json_safe(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            serialize_object_lever_legality_reader_result,
        )
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        s1 = serialize_object_lever_legality_reader_result(result)
        s2 = serialize_object_lever_legality_reader_result(result)
        assert s1 == s2
        text = json.dumps(s1, sort_keys=True)
        assert isinstance(text, str)
        loaded = json.loads(text)
        assert loaded["result_id"] == "result_1"

    def test_visible_serializer_deterministic_json_safe_excludes_backend_fields(self):
        from astra_runtime.domain.object_lever_interaction_legality_reader import (
            serialize_object_lever_legality_reader_result_visible,
        )
        result = _read_legality([
            _make_packet("scene", "visible_safe_projection"),
            _make_packet("actor", "visible_safe_projection"),
            _make_packet("object_lever", "visible_safe_projection"),
        ])
        visible = serialize_object_lever_legality_reader_result_visible(result)
        assert visible["result_id"] == "result_1"
        assert visible["reader_status"] == "legality_read_available"
        assert visible["legality_decision"] == "permitted_for_preview"
        assert "metadata" not in visible
        assert "authority_flags" not in visible
        assert "transaction_preview" not in visible
        assert "event_commitment" not in visible
        text = json.dumps(visible, sort_keys=True)
        assert isinstance(text, str)
        loaded = json.loads(text)
        assert loaded["result_id"] == "result_1"


# ---------------------------------------------------------------------------
# T36 — Module imports no forbidden implementation modules
# ---------------------------------------------------------------------------


class TestImportBoundaries:
    _FORBIDDEN_MODULE_SUBSTRINGS = {
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
        module_path = (
            REPO_ROOT / "src" / "astra_runtime" / "domain"
            / "object_lever_interaction_legality_reader.py"
        )
        imports = self._collect_imports(module_path)
        for substring in self._FORBIDDEN_MODULE_SUBSTRINGS:
            forbidden = [imp for imp in imports if substring in imp]
            assert not forbidden, (
                f"Forbidden module substring {substring!r} found in imports: {forbidden}"
            )


# ---------------------------------------------------------------------------
# T37 — Module does not import RT-002A directly
# ---------------------------------------------------------------------------


class TestNoDirectRT002AImport:
    def test_no_direct_rt002a_import(self):
        module_path = (
            REPO_ROOT / "src" / "astra_runtime" / "domain"
            / "object_lever_interaction_legality_reader.py"
        )
        source = module_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert "read_only_vertical_slice_state_owner_facade" not in module, (
                    "RT-002C must depend on RT-002B packets, not RT-002A facade structures"
                )


# ---------------------------------------------------------------------------
# T38 — Domain package exports the RT-002C public surface
# ---------------------------------------------------------------------------


class TestDomainExports:
    _EXPECTED_EXPORTS = {
        "FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS",
        "InvalidObjectLeverInteractionCommandDeclarationError",
        "InvalidObjectLeverInteractionLegalityAuthorityFlagsError",
        "ObjectLeverInteractionLegalityReaderError",
        "InvalidObjectLeverLegalityInputPacketSetError",
        "InvalidObjectLeverLegalityReaderResultError",
        "InvalidObjectLeverLegalityReadingError",
        "InvalidObjectLeverProjectionRequirementError",
        "OBJECT_LEVER_BLOCK_REASONS",
        "OBJECT_LEVER_COMMAND_FAMILY",
        "OBJECT_LEVER_LEGALITY_DECISIONS",
        "OBJECT_LEVER_LEGALITY_READER_STATUSES",
        "OBJECT_LEVER_NON_AUTHORITY_NOTE",
        "OBJECT_LEVER_OPTIONAL_ENTITY_KINDS",
        "OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES",
        "OBJECT_LEVER_REQUIRED_ENTITY_KINDS",
        "OBJECT_LEVER_REQUIRED_OWNER_FAMILIES",
        "ObjectLeverInteractionCommandDeclaration",
        "ObjectLeverInteractionLegalityAuthorityFlags",
        "ObjectLeverLegalityInputPacketSet",
        "ObjectLeverLegalityReaderResult",
        "ObjectLeverLegalityReading",
        "ObjectLeverProjectionRequirement",
        "build_object_lever_projection_requirements",
        "create_object_lever_interaction_command_declaration",
        "create_object_lever_interaction_legality_authority_flags",
        "create_object_lever_legality_input_packet_set",
        "create_object_lever_legality_reader_result",
        "create_object_lever_legality_reading",
        "create_object_lever_projection_requirement",
        "read_object_lever_interaction_legality",
        "serialize_object_lever_legality_reader_result",
        "serialize_object_lever_legality_reader_result_visible",
        "serialize_object_lever_legality_reading",
        "serialize_object_lever_legality_reading_visible",
        "validate_object_lever_interaction_command_declaration",
        "validate_object_lever_interaction_legality_authority_flags",
        "validate_object_lever_legality_input_packet_set",
        "validate_object_lever_legality_reader_result",
        "validate_object_lever_legality_reading",
        "validate_object_lever_projection_requirement",
    }

    def test_exports_include_rt002c(self):
        from astra_runtime import domain
        domain_all = set(domain.__all__)
        missing = self._EXPECTED_EXPORTS - domain_all
        assert not missing, f"Missing RT-002C exports in domain.__all__: {missing}"


# ---------------------------------------------------------------------------
# T39 — Registry contains RT-002C file record
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_registry_contains_rt002c_module_record(self):
        registry_path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        rt002c_records = [
            r for r in registry.get("file_records", [])
            if "RT-002C" in str(r.get("file_id", ""))
            or "object_lever_interaction_legality_reader" in str(r.get("filename", ""))
        ]
        assert rt002c_records, "Registry does not contain RT-002C module record"

    def test_registry_contains_rt002c_test_record(self):
        registry_path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        test_files: list[str] = []
        for record in registry.get("file_records", []):
            if "RT-002C" in str(record.get("file_id", "")):
                test_files.extend(record.get("test_files", []))
        assert (
            "tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py"
            in test_files
        )


# ---------------------------------------------------------------------------
# T40 — Decision log contains RT-002C entry
# ---------------------------------------------------------------------------


class TestDecisionLog:
    def test_decision_log_contains_rt002c(self):
        log_path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        text = log_path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-RT-002C" in text
        assert "object lever interaction legality reader" in text.lower()
        assert "RT-002D" in text


# ---------------------------------------------------------------------------
# T41-T44 — Upstream tests still pass
# ---------------------------------------------------------------------------


class TestUpstreamPassThrough:
    def test_rt002b_tests_pass(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py",
                "-q",
            ],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"RT-002B tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt002a_tests_pass(self):
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
# T45 — Branch diff does not modify unrelated runtime modules
# ---------------------------------------------------------------------------


class TestBranchDiff:
    def test_branch_diff_limited_to_rt002c(self):
        require_owning_historical_branch(REPO_ROOT, "rt-002c")
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        changed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
        allowed = {
            "src/astra_runtime/domain/object_lever_interaction_legality_reader.py",
            "tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py",
            "src/astra_runtime/domain/__init__.py",
            "docs/decisions/current_decisions_log.md",
            "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
            # guardrail allowlist updates required by the new module
            "tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py",
            "tests/test_runtime_domain_rt_001e_action_legality_service_interface_contract_skeleton.py",
            # RT-002B branch-diff guardrail must tolerate RT-002C downstream files.
            "tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py",
            # RT-002E follow-on files; RT-002C branch-diff guardrail must tolerate
            # downstream RT-002E additions because RT-002E depends on RT-002D/RT-002C.
            "src/astra_runtime/domain/object_lever_event_commit_state_delta_path.py",
            "tests/test_runtime_domain_rt_002e_object_lever_event_commit_state_delta_path.py",
            # RT-002F follow-on files; RT-002C branch-diff guardrail must tolerate
            # downstream RT-002F additions because RT-002F depends on RT-002E/RT-002D/RT-002C.
            "src/astra_runtime/domain/object_lever_replay_audit_check.py",
            "tests/test_runtime_domain_rt_002f_object_lever_replay_audit_check.py",
        }
        unexpected = changed - allowed
        assert not unexpected, (
            f"Branch diff modifies unexpected files: {unexpected}"
        )
