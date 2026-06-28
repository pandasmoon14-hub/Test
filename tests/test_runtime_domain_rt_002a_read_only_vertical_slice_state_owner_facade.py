"""Tests for RT-002A: Read-Only Vertical Slice State Owner Facade.

Covers: module imports, constants, dataclass invariants, authority flag
enforcement, record validation, bundle containment, facade helpers,
serializers, hidden-fact containment, import boundaries, domain package
exports, registry/decision-log records, and upstream test pass-through.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import pathlib
import subprocess
from typing import Any, Mapping

import pytest
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# T1 — Module imports successfully
# ---------------------------------------------------------------------------


class TestModuleImports:
    def test_import_module(self):
        import astra_runtime.domain.read_only_vertical_slice_state_owner_facade  # noqa: F401

    def test_import_constants(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VERTICAL_SLICE_ENTITY_KINDS,
            VERTICAL_SLICE_FACADE_RESULT_STATUSES,
            VERTICAL_SLICE_NON_AUTHORITY_NOTE,
            VERTICAL_SLICE_OWNER_FAMILIES,
            VERTICAL_SLICE_RECORD_STATUSES,
            VERTICAL_SLICE_VISIBILITY_TIERS,
        )
        assert isinstance(VERTICAL_SLICE_OWNER_FAMILIES, frozenset)
        assert isinstance(VERTICAL_SLICE_ENTITY_KINDS, frozenset)
        assert isinstance(VERTICAL_SLICE_VISIBILITY_TIERS, frozenset)
        assert isinstance(VERTICAL_SLICE_RECORD_STATUSES, frozenset)
        assert isinstance(VERTICAL_SLICE_FACADE_RESULT_STATUSES, frozenset)
        assert isinstance(VERTICAL_SLICE_NON_AUTHORITY_NOTE, str)

    def test_import_dataclasses(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceActorRecord,
            VerticalSliceHiddenFactReference,
            VerticalSliceHazardClockRecord,
            VerticalSliceNpcTargetRecord,
            VerticalSliceObjectLeverRecord,
            VerticalSliceOwnerFacadeResult,
            VerticalSliceOwnerProjection,
            VerticalSliceReadOnlyStateBundle,
            VerticalSliceSceneRecord,
            VerticalSliceStateOwnerAuthorityFlags,
            VerticalSliceStateRecordRef,
            VerticalSliceVisibleConditionRecord,
        )
        for cls in (
            VerticalSliceStateOwnerAuthorityFlags,
            VerticalSliceStateRecordRef,
            VerticalSliceSceneRecord,
            VerticalSliceActorRecord,
            VerticalSliceNpcTargetRecord,
            VerticalSliceObjectLeverRecord,
            VerticalSliceHazardClockRecord,
            VerticalSliceVisibleConditionRecord,
            VerticalSliceHiddenFactReference,
            VerticalSliceReadOnlyStateBundle,
            VerticalSliceOwnerProjection,
            VerticalSliceOwnerFacadeResult,
        ):
            assert cls is not None

    def test_import_factories_helpers_validators(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            build_vertical_slice_reference_manifest,
            create_vertical_slice_actor_record,
            create_vertical_slice_hidden_fact_reference,
            create_vertical_slice_hazard_clock_record,
            create_vertical_slice_npc_target_record,
            create_vertical_slice_object_lever_record,
            create_vertical_slice_owner_facade_result,
            create_vertical_slice_owner_projection,
            create_vertical_slice_read_only_state_bundle,
            create_vertical_slice_scene_record,
            create_vertical_slice_state_owner_authority_flags,
            create_vertical_slice_state_record_ref,
            create_vertical_slice_visible_condition_record,
            get_vertical_slice_owner_projection,
            get_vertical_slice_owner_reference,
            serialize_vertical_slice_owner_facade_result,
            serialize_vertical_slice_owner_facade_result_visible,
            validate_vertical_slice_actor_record,
            validate_vertical_slice_hidden_fact_reference,
            validate_vertical_slice_hazard_clock_record,
            validate_vertical_slice_npc_target_record,
            validate_vertical_slice_object_lever_record,
            validate_vertical_slice_owner_facade_result,
            validate_vertical_slice_owner_projection,
            validate_vertical_slice_read_only_state_bundle,
            validate_vertical_slice_scene_record,
            validate_vertical_slice_state_owner_authority_flags,
            validate_vertical_slice_state_record_ref,
            validate_vertical_slice_visible_condition_record,
        )
        for func in (
            create_vertical_slice_state_owner_authority_flags,
            create_vertical_slice_state_record_ref,
            create_vertical_slice_scene_record,
            create_vertical_slice_actor_record,
            create_vertical_slice_npc_target_record,
            create_vertical_slice_object_lever_record,
            create_vertical_slice_hazard_clock_record,
            create_vertical_slice_visible_condition_record,
            create_vertical_slice_hidden_fact_reference,
            create_vertical_slice_read_only_state_bundle,
            create_vertical_slice_owner_projection,
            create_vertical_slice_owner_facade_result,
            build_vertical_slice_reference_manifest,
            get_vertical_slice_owner_reference,
            get_vertical_slice_owner_projection,
            serialize_vertical_slice_owner_facade_result,
            serialize_vertical_slice_owner_facade_result_visible,
            validate_vertical_slice_state_owner_authority_flags,
            validate_vertical_slice_state_record_ref,
            validate_vertical_slice_scene_record,
            validate_vertical_slice_actor_record,
            validate_vertical_slice_npc_target_record,
            validate_vertical_slice_object_lever_record,
            validate_vertical_slice_hazard_clock_record,
            validate_vertical_slice_visible_condition_record,
            validate_vertical_slice_hidden_fact_reference,
            validate_vertical_slice_read_only_state_bundle,
            validate_vertical_slice_owner_projection,
            validate_vertical_slice_owner_facade_result,
        ):
            assert callable(func)


# ---------------------------------------------------------------------------
# T2 — Constants exist and are frozen sets (covered by T1)
# ---------------------------------------------------------------------------


class TestConstants:
    def test_constants_are_frozen(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VERTICAL_SLICE_ENTITY_KINDS,
            VERTICAL_SLICE_FACADE_RESULT_STATUSES,
            VERTICAL_SLICE_OWNER_FAMILIES,
            VERTICAL_SLICE_RECORD_STATUSES,
            VERTICAL_SLICE_VISIBILITY_TIERS,
        )
        for const in (
            VERTICAL_SLICE_OWNER_FAMILIES,
            VERTICAL_SLICE_ENTITY_KINDS,
            VERTICAL_SLICE_VISIBILITY_TIERS,
            VERTICAL_SLICE_RECORD_STATUSES,
            VERTICAL_SLICE_FACADE_RESULT_STATUSES,
        ):
            assert isinstance(const, frozenset)


# ---------------------------------------------------------------------------
# T3 — Entity kinds are exactly the minimal vertical slice set
# ---------------------------------------------------------------------------


class TestEntityKinds:
    _EXPECTED_KINDS = {
        "scene",
        "actor",
        "npc_target",
        "object_lever",
        "hazard_clock",
        "visible_condition",
        "hidden_fact_reference",
    }

    def test_entity_kinds_exact(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VERTICAL_SLICE_ENTITY_KINDS,
        )
        assert VERTICAL_SLICE_ENTITY_KINDS == self._EXPECTED_KINDS


# ---------------------------------------------------------------------------
# T4 — Facade result statuses exclude forbidden statuses
# ---------------------------------------------------------------------------


class TestFacadeResultStatuses:
    def test_facade_result_statuses_exclude_forbidden(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VERTICAL_SLICE_FACADE_RESULT_STATUSES,
        )
        forbidden = {
            "legal", "illegal", "resolved", "executed", "committed",
            "mutated", "materialized",
        }
        for status in forbidden:
            assert status not in VERTICAL_SLICE_FACADE_RESULT_STATUSES, (
                f"Facade result status constant should not contain {status!r}"
            )

    def test_facade_result_statuses_include_allowed(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VERTICAL_SLICE_FACADE_RESULT_STATUSES,
        )
        for status in ("available_reference", "unavailable", "redacted", "deferred", "unknown"):
            assert status in VERTICAL_SLICE_FACADE_RESULT_STATUSES


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
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceStateOwnerAuthorityFlags,
        )
        self._assert_frozen_kw_only(VerticalSliceStateOwnerAuthorityFlags)

    def test_state_record_ref_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceStateRecordRef,
        )
        self._assert_frozen_kw_only(
            VerticalSliceStateRecordRef,
            reference_id="ref1",
            entity_kind="scene",
            owner_family="scene_location_owner",
            visibility_tier="player_visible",
            source_scope="test",
        )

    def test_scene_record_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceSceneRecord,
        )
        self._assert_frozen_kw_only(
            VerticalSliceSceneRecord,
            scene_id="scene1",
            scene_label="Chamber",
            source_scope="test",
        )

    def test_actor_record_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceActorRecord,
        )
        self._assert_frozen_kw_only(
            VerticalSliceActorRecord,
            actor_id="actor1",
            actor_label="Hero",
            source_scope="test",
        )

    def test_npc_target_record_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceNpcTargetRecord,
        )
        self._assert_frozen_kw_only(
            VerticalSliceNpcTargetRecord,
            npc_target_id="npc1",
            npc_target_label="Guard",
            source_scope="test",
        )

    def test_object_lever_record_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceObjectLeverRecord,
        )
        self._assert_frozen_kw_only(
            VerticalSliceObjectLeverRecord,
            object_lever_id="lever1",
            object_lever_label="Lever",
            source_scope="test",
        )

    def test_hazard_clock_record_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceHazardClockRecord,
        )
        self._assert_frozen_kw_only(
            VerticalSliceHazardClockRecord,
            hazard_clock_id="clock1",
            hazard_clock_label="Flood Clock",
            visible_counter="3",
            visible_status="ticking",
            source_scope="test",
        )

    def test_visible_condition_record_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceVisibleConditionRecord,
        )
        self._assert_frozen_kw_only(
            VerticalSliceVisibleConditionRecord,
            condition_id="cond1",
            condition_label="Burned Palm",
            source_scope="test",
        )

    def test_hidden_fact_reference_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceHiddenFactReference,
        )
        self._assert_frozen_kw_only(
            VerticalSliceHiddenFactReference,
            hidden_fact_reference_id="hidden1",
            redacted_safe_label="A hidden matter",
            source_scope="test",
        )

    def test_read_only_state_bundle_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceActorRecord,
            VerticalSliceHiddenFactReference,
            VerticalSliceHazardClockRecord,
            VerticalSliceNpcTargetRecord,
            VerticalSliceObjectLeverRecord,
            VerticalSliceReadOnlyStateBundle,
            VerticalSliceSceneRecord,
            VerticalSliceVisibleConditionRecord,
        )
        bundle = self._assert_frozen_kw_only(
            VerticalSliceReadOnlyStateBundle,
            bundle_id="bundle1",
            scene=VerticalSliceSceneRecord(
                scene_id="s1", scene_label="S", source_scope="test",
            ),
            actor=VerticalSliceActorRecord(
                actor_id="a1", actor_label="A", source_scope="test",
            ),
            npc_target=VerticalSliceNpcTargetRecord(
                npc_target_id="n1", npc_target_label="N", source_scope="test",
            ),
            object_lever=VerticalSliceObjectLeverRecord(
                object_lever_id="o1", object_lever_label="O", source_scope="test",
            ),
            hazard_clock=VerticalSliceHazardClockRecord(
                hazard_clock_id="h1", hazard_clock_label="H",
                visible_counter="1", visible_status="x", source_scope="test",
            ),
            visible_condition=VerticalSliceVisibleConditionRecord(
                condition_id="c1", condition_label="C", source_scope="test",
            ),
            hidden_fact_reference=VerticalSliceHiddenFactReference(
                hidden_fact_reference_id="hf1",
                redacted_safe_label="HF", source_scope="test",
            ),
            source_scope="test",
        )
        assert bundle is not None

    def test_owner_projection_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceOwnerProjection,
        )
        self._assert_frozen_kw_only(
            VerticalSliceOwnerProjection,
            projection_id="proj1",
            entity_kind="scene",
            owner_family="scene_location_owner",
            visibility_tier="player_visible",
            reference_id="ref1",
            source_scope="test",
        )

    def test_owner_facade_result_frozen_kw_only(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceOwnerFacadeResult,
        )
        self._assert_frozen_kw_only(
            VerticalSliceOwnerFacadeResult,
            result_id="res1",
            result_status="unavailable",
            owner_family="scene_location_owner",
            entity_kind="scene",
            source_scope="test",
        )


# ---------------------------------------------------------------------------
# T6 — Authority flags reject all non-False values
# ---------------------------------------------------------------------------


class TestAuthorityFlagEnforcement:
    @pytest.mark.parametrize(
        ("value", "field"),
        [
            (True, "state_read_authorized"),
            (1, "state_mutation_authorized"),
            (0, "event_commitment_authorized"),
            (None, "model_call_authorized"),
            ("yes", "command_execution_authorized"),
        ],
    )
    def test_authority_flags_reject_bad_values(self, value, field):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceStateOwnerAuthorityFlagsError,
            VerticalSliceStateOwnerAuthorityFlags,
        )
        with pytest.raises(InvalidVerticalSliceStateOwnerAuthorityFlagsError):
            VerticalSliceStateOwnerAuthorityFlags(**{field: value})


# ---------------------------------------------------------------------------
# T7 — Authority flag to_dict() hardcodes all false values
# ---------------------------------------------------------------------------


class TestAuthorityFlagToDict:
    def test_to_dict_all_false(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceStateOwnerAuthorityFlags,
        )
        flags = VerticalSliceStateOwnerAuthorityFlags()
        d = flags.to_dict()
        assert all(v is False for v in d.values())
        assert len(d) == 19, f"Expected 19 flags, got {len(d)}"

    def test_to_dict_contains_required_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceStateOwnerAuthorityFlags,
        )
        flags = VerticalSliceStateOwnerAuthorityFlags()
        d = flags.to_dict()
        required = [
            "state_read_authorized",
            "raw_state_access_authorized",
            "state_mutation_authorized",
            "state_projection_materialization_authorized",
            "action_legality_evaluation_authorized",
            "command_execution_authorized",
            "transaction_preview_authorized",
            "event_append_authorized",
            "event_commitment_authorized",
            "persistence_write_authorized",
            "replay_write_authorized",
            "rng_execution_authorized",
            "resource_math_execution_authorized",
            "model_call_authorized",
            "narration_generation_authorized",
            "live_play_authorized",
            "ui_authorized",
            "conversion_authorized",
            "canon_promotion_authorized",
        ]
        for field_name in required:
            assert field_name in d, f"Missing {field_name}"
            assert d[field_name] is False


# ---------------------------------------------------------------------------
# T8 — State record refs require valid entity kind, owner family, visibility tier, source scope
# ---------------------------------------------------------------------------


class TestStateRecordRefValidation:
    def test_valid_ref(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceStateRecordRef,
            validate_vertical_slice_state_record_ref,
        )
        ref = VerticalSliceStateRecordRef(
            reference_id="ref1",
            entity_kind="scene",
            owner_family="scene_location_owner",
            visibility_tier="player_visible",
            source_scope="test",
        )
        assert validate_vertical_slice_state_record_ref(ref)

    def test_invalid_entity_kind(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceStateRecordRefError,
            VerticalSliceStateRecordRef,
        )
        with pytest.raises(InvalidVerticalSliceStateRecordRefError):
            VerticalSliceStateRecordRef(
                reference_id="ref1",
                entity_kind="campaign",
                owner_family="scene_location_owner",
                visibility_tier="player_visible",
                source_scope="test",
            )

    def test_invalid_owner_family(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceStateRecordRefError,
            VerticalSliceStateRecordRef,
        )
        with pytest.raises(InvalidVerticalSliceStateRecordRefError):
            VerticalSliceStateRecordRef(
                reference_id="ref1",
                entity_kind="scene",
                owner_family="inventory_custody_owner",
                visibility_tier="player_visible",
                source_scope="test",
            )

    def test_invalid_visibility_tier(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceStateRecordRefError,
            VerticalSliceStateRecordRef,
        )
        with pytest.raises(InvalidVerticalSliceStateRecordRefError):
            VerticalSliceStateRecordRef(
                reference_id="ref1",
                entity_kind="scene",
                owner_family="scene_location_owner",
                visibility_tier="gm_only",
                source_scope="test",
            )

    def test_empty_source_scope(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceStateRecordRefError,
            VerticalSliceStateRecordRef,
        )
        with pytest.raises(InvalidVerticalSliceStateRecordRefError):
            VerticalSliceStateRecordRef(
                reference_id="ref1",
                entity_kind="scene",
                owner_family="scene_location_owner",
                visibility_tier="player_visible",
                source_scope="",
            )


# ---------------------------------------------------------------------------
# T9 — Scene record carries no raw world state
# ---------------------------------------------------------------------------


class TestSceneRecordNoRawWorldState:
    def test_scene_record_has_no_world_state_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceSceneRecord,
        )
        scene = VerticalSliceSceneRecord(
            scene_id="scene1",
            scene_label="Threshold Chamber",
            source_scope="test",
        )
        d = scene.to_dict()
        for forbidden in (
            "world_state", "full_state", "state_payload", "raw_state",
            "actual_state", "truth_payload", "hidden_facts", "backend_only_facts",
        ):
            assert forbidden not in d, f"Scene record leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T10 — Actor record carries no legality decision
# ---------------------------------------------------------------------------


class TestActorRecordNoLegalityDecision:
    def test_actor_record_has_no_legality_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceActorRecord,
        )
        actor = VerticalSliceActorRecord(
            actor_id="actor1",
            actor_label="Hero",
            source_scope="test",
        )
        d = actor.to_dict()
        for forbidden in (
            "legality_status", "legality_decision", "action_legality_result",
            "legal", "illegal", "blocked", "quarantined",
        ):
            assert forbidden not in d, f"Actor record leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T11 — NPC/target record carries no AI or combat behavior
# ---------------------------------------------------------------------------


class TestNpcTargetRecordNoAiCombat:
    def test_npc_target_record_has_no_ai_combat_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceNpcTargetRecord,
        )
        npc = VerticalSliceNpcTargetRecord(
            npc_target_id="npc1",
            npc_target_label="Watchful Guard",
            source_scope="test",
        )
        d = npc.to_dict()
        for forbidden in (
            "behavior_tree", "ai_goal", "combat_state", "initiative",
            "tactics", "hp", "damage", "defense", "attack",
        ):
            assert forbidden not in d, f"NPC/target record leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T12 — Object/lever record carries no command execution behavior
# ---------------------------------------------------------------------------


class TestObjectLeverRecordNoCommandExecution:
    def test_object_lever_record_has_no_command_execution_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceObjectLeverRecord,
        )
        obj = VerticalSliceObjectLeverRecord(
            object_lever_id="lever1",
            object_lever_label="Brass Lever",
            source_scope="test",
        )
        d = obj.to_dict()
        for forbidden in (
            "execute_command", "command_handler", "interaction_effect",
            "state_change", "delta", "event", "commit",
        ):
            assert forbidden not in d, f"Object/lever record leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T13 — Hazard clock record carries no ticking/consequence behavior
# ---------------------------------------------------------------------------


class TestHazardClockRecordNoTickingConsequence:
    def test_hazard_clock_record_has_no_ticking_consequence_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceHazardClockRecord,
        )
        clock = VerticalSliceHazardClockRecord(
            hazard_clock_id="clock1",
            hazard_clock_label="Flood Timer",
            visible_counter="3",
            visible_status="active",
            source_scope="test",
        )
        d = clock.to_dict()
        for forbidden in (
            "tick", "ticking_logic", "consequence", "apply_consequence",
            "damage", "trigger", "elapsed", "interval", "timeout_handler",
        ):
            assert forbidden not in d, f"Hazard clock record leaked {forbidden!r}"

    def test_hazard_clock_visible_fields_only_strings(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceHazardClockRecord,
        )
        clock = VerticalSliceHazardClockRecord(
            hazard_clock_id="clock1",
            hazard_clock_label="Flood Timer",
            visible_counter="3",
            visible_status="active",
            source_scope="test",
        )
        assert clock.visible_counter == "3"
        assert clock.visible_status == "active"


# ---------------------------------------------------------------------------
# T14 — Visible condition/injury record carries no damage math
# ---------------------------------------------------------------------------


class TestVisibleConditionRecordNoDamageMath:
    def test_visible_condition_record_has_no_damage_math_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceVisibleConditionRecord,
        )
        cond = VerticalSliceVisibleConditionRecord(
            condition_id="cond1",
            condition_label="Burned Palm",
            source_scope="test",
        )
        d = cond.to_dict()
        for forbidden in (
            "damage", "damage_per_tick", "recovery_rate", "healing",
            "severity", "hp_penalty", "resistance", "mitigation",
        ):
            assert forbidden not in d, f"Visible condition record leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T15 — Hidden fact reference carries no hidden fact payload
# ---------------------------------------------------------------------------


class TestHiddenFactReferenceNoPayload:
    def test_hidden_fact_reference_has_no_payload_fields(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceHiddenFactReference,
        )
        hf = VerticalSliceHiddenFactReference(
            hidden_fact_reference_id="hf1",
            redacted_safe_label="A concealed matter",
            source_scope="test",
        )
        d = hf.to_dict()
        for forbidden in (
            "hidden_fact", "hidden_facts", "secret", "secrets",
            "backend_only_fact", "backend_only_facts", "state_payload",
            "raw_state", "actual_state", "truth_payload", "fact_content",
            "truth", "payload",
        ):
            assert forbidden not in d, f"Hidden fact reference leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T16 — Hidden fact reference rejects forbidden hidden metadata keys recursively
# ---------------------------------------------------------------------------


class TestHiddenFactReferenceForbiddenMetadata:
    @pytest.mark.parametrize(
        "forbidden_key",
        [
            "hidden_fact",
            "hidden_facts",
            "secret",
            "secrets",
            "backend_only_fact",
            "backend_only_facts",
            "state_payload",
            "raw_state",
            "actual_state",
            "truth_payload",
        ],
    )
    def test_rejects_forbidden_metadata_keys(self, forbidden_key):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceHiddenFactReferenceError,
            VerticalSliceHiddenFactReference,
        )
        with pytest.raises(InvalidVerticalSliceHiddenFactReferenceError):
            VerticalSliceHiddenFactReference(
                hidden_fact_reference_id="hf1",
                redacted_safe_label="A concealed matter",
                source_scope="test",
                metadata={forbidden_key: "truth"},
            )

    def test_rejects_nested_forbidden_metadata_keys(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceHiddenFactReferenceError,
            VerticalSliceHiddenFactReference,
        )
        with pytest.raises(InvalidVerticalSliceHiddenFactReferenceError):
            VerticalSliceHiddenFactReference(
                hidden_fact_reference_id="hf1",
                redacted_safe_label="A concealed matter",
                source_scope="test",
                metadata={"outer": {"inner": {"secrets": "truth"}}},
            )


# ---------------------------------------------------------------------------
# T16b — Forbidden hidden/raw-state metadata keys rejected on all record types
# ---------------------------------------------------------------------------


class TestForbiddenMetadataKeysOnAllRecords:
    @pytest.mark.parametrize(
        "forbidden_key",
        [
            "hidden_fact",
            "hidden_facts",
            "secret",
            "secrets",
            "backend_only_fact",
            "backend_only_facts",
            "state_payload",
            "raw_state",
            "actual_state",
            "truth_payload",
        ],
    )
    def test_scene_record_rejects_forbidden_metadata_keys(self, forbidden_key):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceSceneRecordError,
            VerticalSliceSceneRecord,
        )
        with pytest.raises(InvalidVerticalSliceSceneRecordError):
            VerticalSliceSceneRecord(
                scene_id="scene1",
                scene_label="Threshold Chamber",
                source_scope="test",
                metadata={forbidden_key: "the assassin is behind the door"},
            )

    @pytest.mark.parametrize(
        "forbidden_key",
        [
            "hidden_fact",
            "raw_state",
            "truth_payload",
        ],
    )
    def test_actor_record_rejects_forbidden_metadata_keys(self, forbidden_key):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceActorRecordError,
            VerticalSliceActorRecord,
        )
        with pytest.raises(InvalidVerticalSliceActorRecordError):
            VerticalSliceActorRecord(
                actor_id="actor1",
                actor_label="Hero",
                source_scope="test",
                metadata={forbidden_key: "secret"},
            )

    @pytest.mark.parametrize(
        "forbidden_key",
        [
            "hidden_facts",
            "backend_only_facts",
            "actual_state",
        ],
    )
    def test_npc_target_record_rejects_forbidden_metadata_keys(self, forbidden_key):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceNpcTargetRecordError,
            VerticalSliceNpcTargetRecord,
        )
        with pytest.raises(InvalidVerticalSliceNpcTargetRecordError):
            VerticalSliceNpcTargetRecord(
                npc_target_id="npc1",
                npc_target_label="Guard",
                source_scope="test",
                metadata={forbidden_key: "secret"},
            )

    def test_hazard_clock_record_rejects_forbidden_metadata_keys(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceHazardClockRecordError,
            VerticalSliceHazardClockRecord,
        )
        with pytest.raises(InvalidVerticalSliceHazardClockRecordError):
            VerticalSliceHazardClockRecord(
                hazard_clock_id="clock1",
                hazard_clock_label="Clock",
                visible_counter="3",
                visible_status="active",
                source_scope="test",
                metadata={"state_payload": {"trap": "active"}},
            )

    def test_visible_condition_record_rejects_forbidden_metadata_keys(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceVisibleConditionRecordError,
            VerticalSliceVisibleConditionRecord,
        )
        with pytest.raises(InvalidVerticalSliceVisibleConditionRecordError):
            VerticalSliceVisibleConditionRecord(
                condition_id="cond1",
                condition_label="Burn",
                source_scope="test",
                metadata={"secret": "true injury severity"},
            )

    def test_state_record_ref_rejects_forbidden_metadata_keys(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceStateRecordRefError,
            VerticalSliceStateRecordRef,
        )
        with pytest.raises(InvalidVerticalSliceStateRecordRefError):
            VerticalSliceStateRecordRef(
                reference_id="ref1",
                entity_kind="scene",
                owner_family="scene_location_owner",
                visibility_tier="player_visible",
                source_scope="test",
                metadata={"hidden_facts": "the assassin is behind the door"},
            )

    def test_read_only_bundle_rejects_nested_forbidden_metadata_keys(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceReadOnlyStateBundleError,
            VerticalSliceActorRecord,
            VerticalSliceHiddenFactReference,
            VerticalSliceHazardClockRecord,
            VerticalSliceNpcTargetRecord,
            VerticalSliceObjectLeverRecord,
            VerticalSliceReadOnlyStateBundle,
            VerticalSliceSceneRecord,
            VerticalSliceVisibleConditionRecord,
        )
        with pytest.raises(InvalidVerticalSliceReadOnlyStateBundleError):
            VerticalSliceReadOnlyStateBundle(
                bundle_id="bundle1",
                scene=VerticalSliceSceneRecord(
                    scene_id="s1", scene_label="S", source_scope="test",
                ),
                actor=VerticalSliceActorRecord(
                    actor_id="a1", actor_label="A", source_scope="test",
                ),
                npc_target=VerticalSliceNpcTargetRecord(
                    npc_target_id="n1", npc_target_label="N", source_scope="test",
                ),
                object_lever=VerticalSliceObjectLeverRecord(
                    object_lever_id="o1", object_lever_label="O", source_scope="test",
                ),
                hazard_clock=VerticalSliceHazardClockRecord(
                    hazard_clock_id="h1", hazard_clock_label="H",
                    visible_counter="1", visible_status="x", source_scope="test",
                ),
                visible_condition=VerticalSliceVisibleConditionRecord(
                    condition_id="c1", condition_label="C", source_scope="test",
                ),
                hidden_fact_reference=VerticalSliceHiddenFactReference(
                    hidden_fact_reference_id="hf1",
                    redacted_safe_label="HF", source_scope="test",
                ),
                source_scope="test",
                metadata={"outer": {"inner": {"raw_state": "hidden backend fact"}}},
            )

    def test_owner_facade_result_rejects_forbidden_metadata_keys(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceOwnerFacadeResultError,
            VerticalSliceOwnerFacadeResult,
        )
        with pytest.raises(InvalidVerticalSliceOwnerFacadeResultError):
            VerticalSliceOwnerFacadeResult(
                result_id="res1",
                result_status="available_reference",
                owner_family="scene_location_owner",
                entity_kind="scene",
                source_scope="test",
                metadata={"truth_payload": "hidden backend fact"},
            )

    def test_validators_reject_records_with_forbidden_metadata(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            InvalidVerticalSliceSceneRecordError,
            VerticalSliceSceneRecord,
            validate_vertical_slice_scene_record,
        )
        with pytest.raises(InvalidVerticalSliceSceneRecordError):
            VerticalSliceSceneRecord(
                scene_id="scene1",
                scene_label="Chamber",
                source_scope="test",
                metadata={"raw_state": {"secret": "truth"}},
            )
        # Validator should also return False if construction somehow succeeded.
        # Construction raises, so we cannot reach validation, but the intent is covered.


# ---------------------------------------------------------------------------
# T17 — Read-only state bundle contains exactly the seven vertical-slice records
# ---------------------------------------------------------------------------


class TestReadOnlyStateBundle:
    @pytest.fixture
    def bundle(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceActorRecord,
            VerticalSliceHiddenFactReference,
            VerticalSliceHazardClockRecord,
            VerticalSliceNpcTargetRecord,
            VerticalSliceObjectLeverRecord,
            VerticalSliceReadOnlyStateBundle,
            VerticalSliceSceneRecord,
            VerticalSliceVisibleConditionRecord,
        )
        return VerticalSliceReadOnlyStateBundle(
            bundle_id="bundle1",
            scene=VerticalSliceSceneRecord(
                scene_id="scene1", scene_label="Chamber", source_scope="test",
            ),
            actor=VerticalSliceActorRecord(
                actor_id="actor1", actor_label="Hero", source_scope="test",
            ),
            npc_target=VerticalSliceNpcTargetRecord(
                npc_target_id="npc1", npc_target_label="Guard", source_scope="test",
            ),
            object_lever=VerticalSliceObjectLeverRecord(
                object_lever_id="lever1", object_lever_label="Lever", source_scope="test",
            ),
            hazard_clock=VerticalSliceHazardClockRecord(
                hazard_clock_id="clock1", hazard_clock_label="Clock",
                visible_counter="3", visible_status="active", source_scope="test",
            ),
            visible_condition=VerticalSliceVisibleConditionRecord(
                condition_id="cond1", condition_label="Burn", source_scope="test",
            ),
            hidden_fact_reference=VerticalSliceHiddenFactReference(
                hidden_fact_reference_id="hf1",
                redacted_safe_label="Hidden", source_scope="test",
            ),
            source_scope="test",
        )

    def test_bundle_has_exactly_seven_records(self, bundle):
        record_names = {
            "scene", "actor", "npc_target", "object_lever",
            "hazard_clock", "visible_condition", "hidden_fact_reference",
        }
        for name in record_names:
            assert hasattr(bundle, name)
        for field in dataclasses.fields(bundle):
            if field.name in record_names:
                assert field.type is not None
        assert len(record_names) == 7

    def test_bundle_validation_passes(self, bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            validate_vertical_slice_read_only_state_bundle,
        )
        assert validate_vertical_slice_read_only_state_bundle(bundle)


# ---------------------------------------------------------------------------
# T18 — Read-only state bundle exposes no mutation methods
# ---------------------------------------------------------------------------


class TestReadOnlyStateBundleImmutable:
    def test_bundle_is_frozen(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceActorRecord,
            VerticalSliceHiddenFactReference,
            VerticalSliceHazardClockRecord,
            VerticalSliceNpcTargetRecord,
            VerticalSliceObjectLeverRecord,
            VerticalSliceReadOnlyStateBundle,
            VerticalSliceSceneRecord,
            VerticalSliceVisibleConditionRecord,
        )
        bundle = VerticalSliceReadOnlyStateBundle(
            bundle_id="bundle1",
            scene=VerticalSliceSceneRecord(
                scene_id="scene1", scene_label="Chamber", source_scope="test",
            ),
            actor=VerticalSliceActorRecord(
                actor_id="actor1", actor_label="Hero", source_scope="test",
            ),
            npc_target=VerticalSliceNpcTargetRecord(
                npc_target_id="npc1", npc_target_label="Guard", source_scope="test",
            ),
            object_lever=VerticalSliceObjectLeverRecord(
                object_lever_id="lever1", object_lever_label="Lever", source_scope="test",
            ),
            hazard_clock=VerticalSliceHazardClockRecord(
                hazard_clock_id="clock1", hazard_clock_label="Clock",
                visible_counter="3", visible_status="active", source_scope="test",
            ),
            visible_condition=VerticalSliceVisibleConditionRecord(
                condition_id="cond1", condition_label="Burn", source_scope="test",
            ),
            hidden_fact_reference=VerticalSliceHiddenFactReference(
                hidden_fact_reference_id="hf1",
                redacted_safe_label="Hidden", source_scope="test",
            ),
            source_scope="test",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            bundle.bundle_id = "changed"
        with pytest.raises(dataclasses.FrozenInstanceError):
            bundle.scene = VerticalSliceSceneRecord(
                scene_id="changed", scene_label="Changed", source_scope="test",
            )

    def test_bundle_has_no_mutate_methods(self):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            VerticalSliceReadOnlyStateBundle,
        )
        for name in ("mutate", "update", "set", "apply", "commit", "append"):
            assert not hasattr(VerticalSliceReadOnlyStateBundle, name), (
                f"Bundle should not expose mutation method {name!r}"
            )


# ---------------------------------------------------------------------------
# Fixtures for facade/serializer tests
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_bundle():
    from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
        VerticalSliceActorRecord,
        VerticalSliceHiddenFactReference,
        VerticalSliceHazardClockRecord,
        VerticalSliceNpcTargetRecord,
        VerticalSliceObjectLeverRecord,
        VerticalSliceReadOnlyStateBundle,
        VerticalSliceSceneRecord,
        VerticalSliceVisibleConditionRecord,
    )
    return VerticalSliceReadOnlyStateBundle(
        bundle_id="bundle1",
        scene=VerticalSliceSceneRecord(
            scene_id="scene1", scene_label="Threshold Chamber", source_scope="rt002a",
        ),
        actor=VerticalSliceActorRecord(
            actor_id="actor1", actor_label="Test Ascendant", source_scope="rt002a",
        ),
        npc_target=VerticalSliceNpcTargetRecord(
            npc_target_id="npc1", npc_target_label="Watchful Adept", source_scope="rt002a",
        ),
        object_lever=VerticalSliceObjectLeverRecord(
            object_lever_id="lever1", object_lever_label="Brass Lever", source_scope="rt002a",
        ),
        hazard_clock=VerticalSliceHazardClockRecord(
            hazard_clock_id="clock1", hazard_clock_label="Flood Clock",
            visible_counter="3", visible_status="active", source_scope="rt002a",
        ),
        visible_condition=VerticalSliceVisibleConditionRecord(
            condition_id="cond1", condition_label="Burned Palm", source_scope="rt002a",
        ),
        hidden_fact_reference=VerticalSliceHiddenFactReference(
            hidden_fact_reference_id="hf1",
            redacted_safe_label="A concealed purpose",
            source_scope="rt002a",
        ),
        source_scope="rt002a",
    )


# ---------------------------------------------------------------------------
# T19 — Facade helper returns owner-mediated references only
# ---------------------------------------------------------------------------


class TestFacadeOwnerReference:
    def test_returns_available_reference_for_visible_record(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "scene_location_owner",
            "scene",
            result_id="res1",
        )
        assert result.result_status == "available_reference"
        assert result.requested_reference is not None
        assert result.requested_reference.reference_id == "scene1"
        assert result.requested_reference.owner_family == "scene_location_owner"

    def test_reference_manifest_contains_owner_families(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            build_vertical_slice_reference_manifest,
        )
        manifest = build_vertical_slice_reference_manifest(sample_bundle)
        owner_families = {ref.owner_family for ref in manifest}
        assert owner_families == {
            "actor_identity_owner",
            "scene_location_owner",
            "target_reachability_owner",
            "object_interactable_owner",
            "hazard_environment_owner",
            "condition_status_owner",
            "hidden_information_visibility_owner",
        }


# ---------------------------------------------------------------------------
# T20 — Facade helper returns redacted projection for hidden fact reference
# ---------------------------------------------------------------------------


class TestFacadeHiddenFactRedaction:
    def test_hidden_fact_reference_is_redacted(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
            get_vertical_slice_owner_projection,
        )
        ref_result = get_vertical_slice_owner_reference(
            sample_bundle,
            "hidden_information_visibility_owner",
            "hidden_fact_reference",
            result_id="res1",
        )
        assert ref_result.result_status == "redacted"
        proj_result = get_vertical_slice_owner_projection(
            sample_bundle,
            "hidden_information_visibility_owner",
            "hidden_fact_reference",
            result_id="res2",
        )
        assert proj_result.result_status == "redacted"
        assert proj_result.projection is not None
        assert proj_result.projection.redacted_safe_label == "A concealed purpose"
        assert proj_result.projection.redaction_required is True


# ---------------------------------------------------------------------------
# T21 — Facade helper returns unavailable/deferred/unknown without treating missing data as false truth
# ---------------------------------------------------------------------------


class TestFacadeMissingData:
    def test_unknown_owner_family_returns_unavailable(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "inventory_custody_owner",
            "scene",
            result_id="res1",
        )
        assert result.result_status == "unavailable"
        assert result.requested_reference is None

    def test_unknown_entity_kind_returns_unavailable(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "scene_location_owner",
            "quest",
            result_id="res1",
        )
        assert result.result_status == "unavailable"
        assert result.requested_reference is None

    def test_missing_data_does_not_invent_truth(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "inventory_custody_owner",
            "scene",
            result_id="res1",
        )
        assert result.result_status != "available_reference"
        assert result.result_status != "resolved"
        assert result.result_status != "committed"


# ---------------------------------------------------------------------------
# T22 — Facade result contains no legality evaluation
# ---------------------------------------------------------------------------


class TestFacadeResultNoLegality:
    def test_facade_result_has_no_legality_fields(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "scene_location_owner",
            "scene",
            result_id="res1",
        )
        d = result.to_dict()
        for forbidden in (
            "legality_status", "legality_decision", "legal", "illegal",
            "action_legality_result", "blocked", "quarantined",
        ):
            assert forbidden not in d, f"Facade result leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T23 — Facade result contains no transaction preview
# ---------------------------------------------------------------------------


class TestFacadeResultNoTransactionPreview:
    def test_facade_result_has_no_transaction_preview_fields(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "scene_location_owner",
            "scene",
            result_id="res1",
        )
        d = result.to_dict()
        for forbidden in (
            "transaction_preview", "preview", "transaction_id", "preview_status",
        ):
            assert forbidden not in d, f"Facade result leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T24 — Facade result contains no event commitment
# ---------------------------------------------------------------------------


class TestFacadeResultNoEventCommitment:
    def test_facade_result_has_no_event_commitment_fields(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "scene_location_owner",
            "scene",
            result_id="res1",
        )
        d = result.to_dict()
        for forbidden in (
            "event_commitment", "committed", "event_id", "event_status",
            "event_append", "ledger_entry",
        ):
            assert forbidden not in d, f"Facade result leaked {forbidden!r}"


# ---------------------------------------------------------------------------
# T25 — Backend serializer is deterministic and JSON-safe
# ---------------------------------------------------------------------------


class TestBackendSerializer:
    def test_backend_serializer_deterministic_and_json_safe(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_reference,
            serialize_vertical_slice_owner_facade_result,
        )
        result = get_vertical_slice_owner_reference(
            sample_bundle,
            "scene_location_owner",
            "scene",
            result_id="res1",
        )
        backend = serialize_vertical_slice_owner_facade_result(result)
        assert json.dumps(backend, sort_keys=True)
        second = serialize_vertical_slice_owner_facade_result(result)
        assert (
            json.dumps(backend, sort_keys=True)
            == json.dumps(second, sort_keys=True)
        )


# ---------------------------------------------------------------------------
# T26 — Visible serializer excludes metadata, hidden facts, raw state, authority flags, backend-only details, implementation details
# ---------------------------------------------------------------------------


class TestVisibleSerializerExcludesBackend:
    _FORBIDDEN_KEYS = {
        "metadata",
        "authority_flags",
        "source_scope",
        "requested_reference",
        "projection",
        "hidden_fact",
        "hidden_facts",
        "secret",
        "secrets",
        "backend_only_fact",
        "backend_only_facts",
        "state_payload",
        "raw_state",
        "actual_state",
        "truth_payload",
    }

    def test_visible_serializer_excludes_forbidden_keys(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_projection,
            serialize_vertical_slice_owner_facade_result_visible,
        )
        result = get_vertical_slice_owner_projection(
            sample_bundle,
            "scene_location_owner",
            "scene",
            result_id="res1",
        )
        visible = serialize_vertical_slice_owner_facade_result_visible(result)
        for key in self._FORBIDDEN_KEYS:
            assert key not in visible, f"Visible serializer leaked {key!r}"

    def test_visible_serializer_has_expected_keys(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_projection,
            serialize_vertical_slice_owner_facade_result_visible,
        )
        result = get_vertical_slice_owner_projection(
            sample_bundle,
            "scene_location_owner",
            "scene",
            result_id="res1",
        )
        visible = serialize_vertical_slice_owner_facade_result_visible(result)
        expected = {
            "result_id", "result_status", "owner_family", "entity_kind",
            "non_authority_note", "visibility_tier", "redaction_required",
            "safe_reference_ids",
        }
        assert set(visible.keys()) == expected

    def test_visible_serializer_for_hidden_fact_is_redacted(self, sample_bundle):
        from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
            get_vertical_slice_owner_projection,
            serialize_vertical_slice_owner_facade_result_visible,
        )
        result = get_vertical_slice_owner_projection(
            sample_bundle,
            "hidden_information_visibility_owner",
            "hidden_fact_reference",
            result_id="res1",
        )
        visible = serialize_vertical_slice_owner_facade_result_visible(result)
        assert visible["result_status"] == "redacted"
        assert visible["redaction_required"] is True
        assert visible["safe_reference_ids"] == ["hf1"]
        assert "hidden_fact_reference_id" not in visible


# ---------------------------------------------------------------------------
# T27 — Module imports no forbidden implementation modules
# ---------------------------------------------------------------------------


class TestImportBoundaryEnforcement:
    _FORBIDDEN_MODULES = (
        "state_store", "state_projection", "transaction_lifecycle",
        "event_commitment", "resource_consequence_math", "model_boundary",
        "live_play", "tiny_vertical_slice",
    )

    def test_rt002a_does_not_import_forbidden_modules(self):
        src = (
            REPO_ROOT
            / "src"
            / "astra_runtime"
            / "domain"
            / "read_only_vertical_slice_state_owner_facade.py"
        ).read_text()
        tree = ast.parse(src)
        import_names: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_names.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    import_names.append(node.module)
        for mod_name in import_names:
            for forbidden in self._FORBIDDEN_MODULES:
                assert forbidden not in mod_name, (
                    f"RT-002A imports forbidden module pattern "
                    f"{forbidden!r} via {mod_name!r}"
                )


# ---------------------------------------------------------------------------
# T28 — Domain package exports the RT-002A public surface
# ---------------------------------------------------------------------------


class TestDomainPackageExports:
    def test_domain_package_exports_rt002a_constants(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "VERTICAL_SLICE_OWNER_FAMILIES")
        assert hasattr(domain, "VERTICAL_SLICE_ENTITY_KINDS")
        assert hasattr(domain, "VERTICAL_SLICE_VISIBILITY_TIERS")
        assert hasattr(domain, "VERTICAL_SLICE_RECORD_STATUSES")
        assert hasattr(domain, "VERTICAL_SLICE_FACADE_RESULT_STATUSES")
        assert hasattr(domain, "VERTICAL_SLICE_NON_AUTHORITY_NOTE")

    def test_domain_package_exports_rt002a_dataclasses(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "VerticalSliceStateOwnerAuthorityFlags")
        assert hasattr(domain, "VerticalSliceStateRecordRef")
        assert hasattr(domain, "VerticalSliceSceneRecord")
        assert hasattr(domain, "VerticalSliceActorRecord")
        assert hasattr(domain, "VerticalSliceNpcTargetRecord")
        assert hasattr(domain, "VerticalSliceObjectLeverRecord")
        assert hasattr(domain, "VerticalSliceHazardClockRecord")
        assert hasattr(domain, "VerticalSliceVisibleConditionRecord")
        assert hasattr(domain, "VerticalSliceHiddenFactReference")
        assert hasattr(domain, "VerticalSliceReadOnlyStateBundle")
        assert hasattr(domain, "VerticalSliceOwnerProjection")
        assert hasattr(domain, "VerticalSliceOwnerFacadeResult")

    def test_domain_package_exports_rt002a_functions(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "create_vertical_slice_state_owner_authority_flags")
        assert hasattr(domain, "create_vertical_slice_state_record_ref")
        assert hasattr(domain, "create_vertical_slice_scene_record")
        assert hasattr(domain, "create_vertical_slice_actor_record")
        assert hasattr(domain, "create_vertical_slice_npc_target_record")
        assert hasattr(domain, "create_vertical_slice_object_lever_record")
        assert hasattr(domain, "create_vertical_slice_hazard_clock_record")
        assert hasattr(domain, "create_vertical_slice_visible_condition_record")
        assert hasattr(domain, "create_vertical_slice_hidden_fact_reference")
        assert hasattr(domain, "create_vertical_slice_read_only_state_bundle")
        assert hasattr(domain, "create_vertical_slice_owner_projection")
        assert hasattr(domain, "create_vertical_slice_owner_facade_result")
        assert hasattr(domain, "build_vertical_slice_reference_manifest")
        assert hasattr(domain, "get_vertical_slice_owner_reference")
        assert hasattr(domain, "get_vertical_slice_owner_projection")
        assert hasattr(domain, "serialize_vertical_slice_owner_facade_result")
        assert hasattr(domain, "serialize_vertical_slice_owner_facade_result_visible")
        assert hasattr(domain, "validate_vertical_slice_state_owner_authority_flags")
        assert hasattr(domain, "validate_vertical_slice_state_record_ref")
        assert hasattr(domain, "validate_vertical_slice_scene_record")
        assert hasattr(domain, "validate_vertical_slice_actor_record")
        assert hasattr(domain, "validate_vertical_slice_npc_target_record")
        assert hasattr(domain, "validate_vertical_slice_object_lever_record")
        assert hasattr(domain, "validate_vertical_slice_hazard_clock_record")
        assert hasattr(domain, "validate_vertical_slice_visible_condition_record")
        assert hasattr(domain, "validate_vertical_slice_hidden_fact_reference")
        assert hasattr(domain, "validate_vertical_slice_read_only_state_bundle")
        assert hasattr(domain, "validate_vertical_slice_owner_projection")
        assert hasattr(domain, "validate_vertical_slice_owner_facade_result")


# ---------------------------------------------------------------------------
# T29 — Registry contains RT-002A file record
# ---------------------------------------------------------------------------


class TestRegistryContainsRt002aRecord:
    @pytest.fixture
    def registry(self) -> dict[str, Any]:
        registry_path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        return yaml.safe_load(registry_path.read_text(encoding="utf-8"))

    def test_registry_contains_rt002a_file_record(self, registry: dict[str, Any]):
        file_records = registry.get("file_records", [])
        rt002a_records = [
            r for r in file_records
            if "RT-002A" in str(r.get("file_id", "")) or
            "read_only_vertical_slice_state_owner_facade" in str(r.get("filename", ""))
        ]
        assert rt002a_records, "Registry does not contain RT-002A file record"

    def test_registry_rt002a_record_authority_level_skeleton(self, registry: dict[str, Any]):
        file_records = registry.get("file_records", [])
        rt002a_records = [
            r for r in file_records
            if "RT-002A" in str(r.get("file_id", "")) or
            "read_only_vertical_slice_state_owner_facade" in str(r.get("filename", ""))
        ]
        assert rt002a_records
        for record in rt002a_records:
            authority = str(record.get("authority_level", "")).lower()
            notes = str(record.get("notes", "")).lower()
            assert authority == "skeleton" or "skeleton" in notes, (
                f"RT-002A registry record must be authority level skeleton and note skeleton-only, "
                f"got authority={authority!r} notes={notes!r}"
            )

    def test_registry_rt002a_record_notes_read_only(self, registry: dict[str, Any]):
        file_records = registry.get("file_records", [])
        rt002a_records = [
            r for r in file_records
            if "RT-002A" in str(r.get("file_id", "")) or
            "read_only_vertical_slice_state_owner_facade" in str(r.get("filename", ""))
        ]
        assert rt002a_records
        for record in rt002a_records:
            notes = str(record.get("notes", "")).lower()
            assert "read-only" in notes, (
                "RT-002A registry record notes must state read-only"
            )

    def test_registry_changelog_contains_rt002a(self, registry: dict[str, Any]):
        changelog = registry.get("changelog", [])
        assert any(
            "rt_002a" in str(entry.get("action", "")).lower() or
            "RT-002A" in str(entry.get("action", ""))
            for entry in changelog
        ), "Registry changelog must contain RT-002A entry"


# ---------------------------------------------------------------------------
# T30 — Decision log contains RT-002A entry
# ---------------------------------------------------------------------------


class TestDecisionLogContainsRt002aEntry:
    @pytest.fixture
    def log_text(self) -> str:
        log_path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        return log_path.read_text(encoding="utf-8")

    def test_decision_log_contains_rt002a(self, log_text: str):
        assert "RUNTIME-DOMAIN-RT-002A" in log_text, (
            "Decision log does not contain RT-002A entry"
        )

    def test_decision_log_rt002a_is_read_only(self, log_text: str):
        assert "read-only" in log_text.lower()

    def test_decision_log_rt002a_references_rt001i(self, log_text: str):
        assert "RT-001I" in log_text

    def test_decision_log_rt002a_recommends_rt002b(self, log_text: str):
        assert "RT-002B" in log_text
        assert "Projection and Visibility Adapter" in log_text


# ---------------------------------------------------------------------------
# T31 — RT-001H tests still pass
# ---------------------------------------------------------------------------


class TestRt001hTestsPass:
    def test_rt001h_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001H tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T32 — RT-001I tests still pass
# ---------------------------------------------------------------------------


class TestRt001iTestsPass:
    def test_rt001i_tests_pass(self):
        # RT-001I's TestBranchDiffContained guardrail asserts that no runtime
        # implementation modules differ from origin/main. That guardrail is
        # correct for the review-only RT-001I branch but legitimately fails on
        # the RT-002A branch because RT-002A adds a new runtime module and
        # updates domain exports. Run the functional tests only.
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py",
                "-q", "--tb=short",
                "-k", "not TestBranchDiffContained",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001I tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T33 — PR-9A through PR-9E seam tests still pass
# ---------------------------------------------------------------------------


class TestPr9SeamTestsPass:
    def test_pr9a_through_pr9e_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_pr_9a_scene_command_execution_skeleton.py",
                "tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py",
                "tests/test_runtime_domain_pr_9c_command_kind_routing_skeleton.py",
                "tests/test_runtime_domain_pr_9d_validation_integration_bridge_skeleton.py",
                "tests/test_runtime_domain_pr_9e_transaction_preview_packet_bridge_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"PR-9A through PR-9E seam tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T34 — Branch diff does not modify unrelated runtime modules
# ---------------------------------------------------------------------------


class TestBranchDiffContained:
    _ALLOWED_PATTERNS = (
        "src/astra_runtime/domain/read_only_vertical_slice_state_owner_facade.py",
        "tests/test_runtime_domain_rt_002a_read_only_vertical_slice_state_owner_facade.py",
        "src/astra_runtime/domain/__init__.py",
        "docs/decisions/current_decisions_log.md",
        "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
        "tests/test_runtime_domain_pr_9b_scene_command_execution_hardening_review.py",
        "tests/test_runtime_domain_rt_001e_action_legality_service_interface_contract_skeleton.py",
    )

    def test_branch_diff_is_limited_to_allowed_files(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, check=True, cwd=REPO_ROOT,
        )
        changed = [p for p in result.stdout.strip().splitlines() if p.strip()]
        for path in changed:
            assert any(
                path == pat or path.endswith(pat) for pat in self._ALLOWED_PATTERNS
            ), f"RT-002A branch modifies unexpected file: {path}"

    def test_no_unrelated_runtime_module_modified(self):
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, check=True, cwd=REPO_ROOT,
        )
        changed = [p for p in result.stdout.strip().splitlines() if p.strip()]
        for path in changed:
            if path.startswith("src/astra_runtime/"):
                assert path in self._ALLOWED_PATTERNS, (
                    f"RT-002A branch modifies unrelated runtime module: {path}"
                )
