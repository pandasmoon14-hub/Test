"""Tests for RT-001H: State Owner Interface Contract Skeleton.

Covers: module imports, constants, dataclass invariants, authority flag
enforcement, references, visibility descriptors, projection request references,
dependency declarations, request/result typing, builders, serializers,
visible-serializer containment, metadata safety, public name inspection,
forbidden import enforcement, and domain package exports.
"""

from __future__ import annotations

import ast
import dataclasses
import json
import pathlib
import subprocess
from typing import Any, Mapping

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# T1 — Module imports successfully
# ---------------------------------------------------------------------------

class TestModuleImports:
    def test_import_module(self):
        import astra_runtime.domain.state_owner_interface_contract_skeleton  # noqa: F401

    def test_import_constants(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_INTERFACE_FAMILIES,
            STATE_OWNER_DEPENDENCY_OWNER_FAMILIES,
            STATE_OWNER_INTERFACE_REQUEST_STATUSES,
            STATE_OWNER_INTERFACE_RESULT_STATUSES,
            STATE_OWNER_VISIBILITY_TIERS,
            STATE_OWNER_PROJECTION_KINDS,
            STATE_OWNER_REFERENCE_KINDS,
            STATE_OWNER_DENIAL_REASONS,
            STATE_OWNER_NON_AUTHORITY_NOTE,
        )
        assert isinstance(STATE_OWNER_INTERFACE_FAMILIES, frozenset)
        assert isinstance(STATE_OWNER_DEPENDENCY_OWNER_FAMILIES, frozenset)
        assert isinstance(STATE_OWNER_INTERFACE_REQUEST_STATUSES, frozenset)
        assert isinstance(STATE_OWNER_INTERFACE_RESULT_STATUSES, frozenset)
        assert isinstance(STATE_OWNER_VISIBILITY_TIERS, frozenset)
        assert isinstance(STATE_OWNER_PROJECTION_KINDS, frozenset)
        assert isinstance(STATE_OWNER_REFERENCE_KINDS, frozenset)
        assert isinstance(STATE_OWNER_DENIAL_REASONS, frozenset)
        assert isinstance(STATE_OWNER_NON_AUTHORITY_NOTE, str)

    def test_import_dataclasses(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceAuthorityFlags,
            StateOwnerInterfaceReference,
            StateVisibilityDescriptor,
            StateProjectionRequestReference,
            StateOwnerDependencyDeclaration,
            StateOwnerInterfaceRequest,
            StateOwnerInterfaceResult,
            StateOwnerInterfaceContractSummary,
        )
        assert StateOwnerInterfaceAuthorityFlags is not None
        assert StateOwnerInterfaceReference is not None
        assert StateVisibilityDescriptor is not None
        assert StateProjectionRequestReference is not None
        assert StateOwnerDependencyDeclaration is not None
        assert StateOwnerInterfaceRequest is not None
        assert StateOwnerInterfaceResult is not None
        assert StateOwnerInterfaceContractSummary is not None

    def test_import_factories_builders_serializers_validators(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            create_state_owner_interface_authority_flags,
            create_state_owner_interface_reference,
            create_state_visibility_descriptor,
            create_state_projection_request_reference,
            create_state_owner_dependency_declaration,
            create_state_owner_interface_request,
            create_state_owner_interface_result,
            create_state_owner_interface_contract_summary,
            build_state_owner_dependency_manifest,
            build_unavailable_state_owner_interface_result,
            build_deferred_state_owner_interface_result,
            build_unknown_state_owner_interface_result,
            serialize_state_owner_interface_result,
            serialize_state_owner_interface_result_visible,
            validate_state_owner_interface_authority_flags,
            validate_state_owner_interface_reference,
            validate_state_visibility_descriptor,
            validate_state_projection_request_reference,
            validate_state_owner_dependency_declaration,
            validate_state_owner_interface_request,
            validate_state_owner_interface_result,
            validate_state_owner_interface_contract_summary,
        )
        assert callable(create_state_owner_interface_authority_flags)
        assert callable(create_state_owner_interface_reference)
        assert callable(create_state_visibility_descriptor)
        assert callable(create_state_projection_request_reference)
        assert callable(create_state_owner_dependency_declaration)
        assert callable(create_state_owner_interface_request)
        assert callable(create_state_owner_interface_result)
        assert callable(create_state_owner_interface_contract_summary)
        assert callable(build_state_owner_dependency_manifest)
        assert callable(build_unavailable_state_owner_interface_result)
        assert callable(build_deferred_state_owner_interface_result)
        assert callable(build_unknown_state_owner_interface_result)
        assert callable(serialize_state_owner_interface_result)
        assert callable(serialize_state_owner_interface_result_visible)
        assert callable(validate_state_owner_interface_authority_flags)
        assert callable(validate_state_owner_interface_reference)
        assert callable(validate_state_visibility_descriptor)
        assert callable(validate_state_projection_request_reference)
        assert callable(validate_state_owner_dependency_declaration)
        assert callable(validate_state_owner_interface_request)
        assert callable(validate_state_owner_interface_result)
        assert callable(validate_state_owner_interface_contract_summary)


# ---------------------------------------------------------------------------
# T2 — Constants include all 16 state owner families
# ---------------------------------------------------------------------------

class TestStateOwnerFamilies:
    _EXPECTED_FAMILIES = {
        "actor_identity_owner",
        "actor_capability_owner",
        "scene_location_owner",
        "target_reachability_owner",
        "object_interactable_owner",
        "hazard_environment_owner",
        "inventory_custody_owner",
        "resource_pool_owner",
        "condition_status_owner",
        "faction_social_owner",
        "mission_discovery_owner",
        "hidden_information_visibility_owner",
        "state_projection_owner",
        "transaction_preview_owner",
        "event_commitment_owner",
        "persistence_replay_owner",
    }

    def test_state_owner_families_complete(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_INTERFACE_FAMILIES,
        )
        assert STATE_OWNER_INTERFACE_FAMILIES == self._EXPECTED_FAMILIES


# ---------------------------------------------------------------------------
# T3 — Constants include all 10 dependency owner families
# ---------------------------------------------------------------------------

class TestDependencyOwnerFamilies:
    _EXPECTED_FAMILIES = {
        "validation_owner",
        "resource_math_owner",
        "rng_table_oracle_owner",
        "state_delta_owner",
        "transaction_lifecycle_owner",
        "event_commitment_owner",
        "context_packet_owner",
        "persistence_replay_owner",
        "doctrine_schema_escalation_owner",
        "combat_ability_skill_effect_owner",
    }

    def test_dependency_owner_families_complete(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_DEPENDENCY_OWNER_FAMILIES,
        )
        assert STATE_OWNER_DEPENDENCY_OWNER_FAMILIES == self._EXPECTED_FAMILIES


# ---------------------------------------------------------------------------
# T3b — Constants include all hidden information policies
# ---------------------------------------------------------------------------

class TestHiddenInformationPolicies:
    _EXPECTED_POLICIES = {
        "generic_safe_message",
        "redact",
        "route_to_hidden_information_visibility_owner",
        "deny_visible_detail",
    }

    def test_hidden_information_policies_complete(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_HIDDEN_INFORMATION_POLICIES,
        )
        assert STATE_OWNER_HIDDEN_INFORMATION_POLICIES == self._EXPECTED_POLICIES


# ---------------------------------------------------------------------------
# T4 — Result statuses exclude execution/final/adjudicative statuses
# ---------------------------------------------------------------------------

class TestResultStatusConstant:
    def test_result_statuses_exclude_forbidden(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_INTERFACE_RESULT_STATUSES,
        )
        forbidden = {
            "available", "resolved", "legal", "illegal", "committed",
            "mutated", "executed", "materialized",
        }
        for status in forbidden:
            assert status not in STATE_OWNER_INTERFACE_RESULT_STATUSES, (
                f"Result status constant should not contain {status!r}"
            )


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
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceAuthorityFlags,
        )
        self._assert_frozen_kw_only(StateOwnerInterfaceAuthorityFlags)

    def test_reference_frozen_kw_only(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
        )
        self._assert_frozen_kw_only(
            StateOwnerInterfaceReference,
            reference_id="ref1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )

    def test_visibility_descriptor_frozen_kw_only(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateVisibilityDescriptor,
        )
        self._assert_frozen_kw_only(
            StateVisibilityDescriptor,
            visibility_id="vis1",
            visibility_tier="player_visible",
        )

    def test_projection_request_reference_frozen_kw_only(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateProjectionRequestReference,
            StateVisibilityDescriptor,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        visibility = StateVisibilityDescriptor(
            visibility_id="vis1",
            visibility_tier="player_visible",
        )
        self._assert_frozen_kw_only(
            StateProjectionRequestReference,
            projection_request_id="pr1",
            projection_kind="actor_scoped",
            requesting_owner_family="actor_identity_owner",
            target_owner_family="state_projection_owner",
            subject_ref=subject,
            visibility_descriptor=visibility,
        )

    def test_dependency_declaration_frozen_kw_only(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerDependencyDeclaration,
        )
        self._assert_frozen_kw_only(
            StateOwnerDependencyDeclaration,
            dependency_id="dep1",
            dependency_owner_family="validation_owner",
            dependency_reason="validation_required",
        )

    def test_request_frozen_kw_only(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateOwnerInterfaceRequest,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        self._assert_frozen_kw_only(
            StateOwnerInterfaceRequest,
            request_id="req1",
            requesting_surface="action_legality_service",
            owner_family="actor_identity_owner",
            request_status="declared",
            subject_ref=subject,
        )

    def test_result_frozen_kw_only(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateOwnerInterfaceResult,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        self._assert_frozen_kw_only(
            StateOwnerInterfaceResult,
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            result_status="unavailable",
            subject_ref=subject,
        )

    def test_contract_summary_frozen_kw_only(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceContractSummary,
        )
        self._assert_frozen_kw_only(
            StateOwnerInterfaceContractSummary,
            summary_id="sum1",
        )


# ---------------------------------------------------------------------------
# T6 — Authority flags reject True, 1, 0, None, and truthy strings
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
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceAuthorityFlags,
            InvalidStateOwnerInterfaceAuthorityFlagsError,
        )
        with pytest.raises(InvalidStateOwnerInterfaceAuthorityFlagsError):
            StateOwnerInterfaceAuthorityFlags(**{field: value})


# ---------------------------------------------------------------------------
# T7 — Authority flag to_dict() hardcodes every flag to False
# ---------------------------------------------------------------------------

class TestAuthorityFlagToDict:
    def test_to_dict_all_false(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceAuthorityFlags,
        )
        flags = StateOwnerInterfaceAuthorityFlags()
        d = flags.to_dict()
        assert all(v is False for v in d.values())
        assert len(d) == 31, f"Expected 31 flags, got {len(d)}"

    def test_to_dict_contains_required_fields(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceAuthorityFlags,
        )
        flags = StateOwnerInterfaceAuthorityFlags()
        d = flags.to_dict()
        required = [
            "state_owner_service_authorized",
            "state_read_authorized",
            "raw_state_access_authorized",
            "state_projection_materialization_authorized",
            "state_mutation_authorized",
            "event_append_authorized",
            "event_commitment_authorized",
            "persistence_write_authorized",
            "replay_write_authorized",
            "rng_execution_authorized",
            "table_oracle_execution_authorized",
            "resource_math_execution_authorized",
            "affordability_execution_authorized",
            "reservation_authorized",
            "settlement_authorized",
            "consequence_application_authorized",
            "action_legality_evaluation_authorized",
            "command_execution_authorized",
            "combat_resolution_authorized",
            "ability_resolution_authorized",
            "skill_resolution_authorized",
            "effect_resolution_authorized",
            "context_packet_compilation_authorized",
            "model_call_authorized",
            "prompt_rendering_authorized",
            "narration_generation_authorized",
            "live_play_authorized",
            "ui_authorized",
            "conversion_authorized",
            "sourcebook_inclusion_authorized",
            "canon_promotion_authorized",
        ]
        for field_name in required:
            assert field_name in d, f"Missing {field_name}"
            assert d[field_name] is False


# ---------------------------------------------------------------------------
# T8 — StateOwnerInterfaceReference requires valid reference kind and owner family
# ---------------------------------------------------------------------------

class TestReferenceValidation:
    def test_valid_reference(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            validate_state_owner_interface_reference,
        )
        ref = StateOwnerInterfaceReference(
            reference_id="ref1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        assert validate_state_owner_interface_reference(ref)

    def test_invalid_reference_kind(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceReferenceError,
            StateOwnerInterfaceReference,
        )
        with pytest.raises(InvalidStateOwnerInterfaceReferenceError):
            StateOwnerInterfaceReference(
                reference_id="ref1",
                reference_kind="invalid_kind",
                owner_family="actor_identity_owner",
                source_scope="test",
            )

    def test_invalid_owner_family(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceReferenceError,
            StateOwnerInterfaceReference,
        )
        with pytest.raises(InvalidStateOwnerInterfaceReferenceError):
            StateOwnerInterfaceReference(
                reference_id="ref1",
                reference_kind="state_record_ref",
                owner_family="invalid_family",
                source_scope="test",
            )


# ---------------------------------------------------------------------------
# T9 — StateVisibilityDescriptor requires a valid visibility tier
# ---------------------------------------------------------------------------

class TestVisibilityDescriptorValidation:
    def test_valid_tier(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateVisibilityDescriptor,
            validate_state_visibility_descriptor,
        )
        vis = StateVisibilityDescriptor(
            visibility_id="vis1",
            visibility_tier="player_visible",
        )
        assert validate_state_visibility_descriptor(vis)

    def test_invalid_tier(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateVisibilityDescriptorError,
            StateVisibilityDescriptor,
        )
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            StateVisibilityDescriptor(
                visibility_id="vis1",
                visibility_tier="invalid_tier",
            )


# ---------------------------------------------------------------------------
# T10 — Visibility descriptor does not carry hidden facts
# ---------------------------------------------------------------------------

class TestVisibilityDescriptorNoHiddenFacts:
    def test_no_hidden_fact_fields(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateVisibilityDescriptor,
        )
        vis = StateVisibilityDescriptor(
            visibility_id="vis1",
            visibility_tier="player_visible",
        )
        d = vis.to_dict()
        assert "hidden_facts" not in d
        assert "backend_only_facts" not in d
        assert "state_payload" not in d

    def test_rejects_arbitrary_hidden_information_policy(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateVisibilityDescriptorError,
            StateVisibilityDescriptor,
        )
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            StateVisibilityDescriptor(
                visibility_id="vis1",
                visibility_tier="player_visible",
                hidden_information_policy="secret_door_exists",
            )

    def test_rejects_forbidden_hidden_fact_metadata_keys(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateVisibilityDescriptorError,
            StateVisibilityDescriptor,
        )
        for forbidden_key in (
            "hidden_fact",
            "hidden_facts",
            "secret",
            "secrets",
            "backend_only_fact",
            "backend_only_facts",
            "state_payload",
            "projection_payload",
            "actual_state",
        ):
            with pytest.raises(InvalidStateVisibilityDescriptorError):
                StateVisibilityDescriptor(
                    visibility_id="vis1",
                    visibility_tier="player_visible",
                    metadata={forbidden_key: "the assassin is behind the door"},
                )

    def test_rejects_nested_forbidden_hidden_fact_metadata_keys(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateVisibilityDescriptorError,
            StateVisibilityDescriptor,
        )
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            StateVisibilityDescriptor(
                visibility_id="vis1",
                visibility_tier="player_visible",
                metadata={
                    "outer": {
                        "inner": {
                            "hidden_facts": "the assassin is behind the door",
                        },
                    },
                },
            )

    def test_validator_rejects_descriptor_with_forbidden_metadata(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateVisibilityDescriptorError,
            StateVisibilityDescriptor,
            validate_state_visibility_descriptor,
        )
        # Construction itself must raise; if it somehow did not, validator returns False.
        with pytest.raises(InvalidStateVisibilityDescriptorError):
            vis = StateVisibilityDescriptor(
                visibility_id="vis1",
                visibility_tier="player_visible",
                metadata={"hidden_facts": "the assassin is behind the door"},
            )
            assert not validate_state_visibility_descriptor(vis)


# ---------------------------------------------------------------------------
# T11 — Projection request reference requires StateVisibilityDescriptor
# ---------------------------------------------------------------------------

class TestProjectionRequestReferenceRequiresVisibility:
    def test_requires_visibility_descriptor(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateProjectionRequestReferenceError,
            StateOwnerInterfaceReference,
            StateProjectionRequestReference,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        with pytest.raises(InvalidStateProjectionRequestReferenceError):
            StateProjectionRequestReference(
                projection_request_id="pr1",
                projection_kind="actor_scoped",
                requesting_owner_family="actor_identity_owner",
                target_owner_family="state_projection_owner",
                subject_ref=subject,
                visibility_descriptor="not_a_descriptor",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# T12 — Projection request reference does not contain actual projection payload data
# ---------------------------------------------------------------------------

class TestProjectionRequestReferenceNoPayload:
    def test_no_payload_fields(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateProjectionRequestReference,
            StateVisibilityDescriptor,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        visibility = StateVisibilityDescriptor(
            visibility_id="vis1",
            visibility_tier="player_visible",
        )
        pr = StateProjectionRequestReference(
            projection_request_id="pr1",
            projection_kind="actor_scoped",
            requesting_owner_family="actor_identity_owner",
            target_owner_family="state_projection_owner",
            subject_ref=subject,
            visibility_descriptor=visibility,
        )
        d = pr.to_dict()
        assert "projection_payload" not in d
        assert "state_data" not in d
        assert "actual_state" not in d


# ---------------------------------------------------------------------------
# T13 — Dependency declarations require valid dependency owner family
# ---------------------------------------------------------------------------

class TestDependencyDeclarationValidation:
    def test_valid_dependency_owner_family(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerDependencyDeclaration,
            validate_state_owner_dependency_declaration,
        )
        dep = StateOwnerDependencyDeclaration(
            dependency_id="dep1",
            dependency_owner_family="validation_owner",
            dependency_reason="validation_required",
        )
        assert validate_state_owner_dependency_declaration(dep)

    def test_invalid_dependency_owner_family(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerDependencyDeclarationError,
            StateOwnerDependencyDeclaration,
        )
        with pytest.raises(InvalidStateOwnerDependencyDeclarationError):
            StateOwnerDependencyDeclaration(
                dependency_id="dep1",
                dependency_owner_family="invalid_owner",
                dependency_reason="validation_required",
            )


# ---------------------------------------------------------------------------
# T14 — Interface request requires valid owner family and request status
# ---------------------------------------------------------------------------

class TestInterfaceRequestValidation:
    def test_valid_request(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateOwnerInterfaceRequest,
            validate_state_owner_interface_request,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        req = StateOwnerInterfaceRequest(
            request_id="req1",
            requesting_surface="action_legality_service",
            owner_family="actor_identity_owner",
            request_status="declared",
            subject_ref=subject,
        )
        assert validate_state_owner_interface_request(req)

    def test_invalid_owner_family(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceRequestError,
            StateOwnerInterfaceReference,
            StateOwnerInterfaceRequest,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        with pytest.raises(InvalidStateOwnerInterfaceRequestError):
            StateOwnerInterfaceRequest(
                request_id="req1",
                requesting_surface="action_legality_service",
                owner_family="invalid_family",
                request_status="declared",
                subject_ref=subject,
            )

    def test_invalid_request_status(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceRequestError,
            StateOwnerInterfaceReference,
            StateOwnerInterfaceRequest,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        with pytest.raises(InvalidStateOwnerInterfaceRequestError):
            StateOwnerInterfaceRequest(
                request_id="req1",
                requesting_surface="action_legality_service",
                owner_family="actor_identity_owner",
                request_status="resolved",
                subject_ref=subject,
            )


# ---------------------------------------------------------------------------
# T15 — Interface request rejects state read, raw state access, or mutation authority
# ---------------------------------------------------------------------------

class TestInterfaceRequestRejectsAuthorities:
    def test_request_rejects_state_read_authority(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceAuthorityFlagsError,
            StateOwnerInterfaceAuthorityFlags,
            StateOwnerInterfaceReference,
            StateOwnerInterfaceRequest,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        with pytest.raises(InvalidStateOwnerInterfaceAuthorityFlagsError):
            StateOwnerInterfaceRequest(
                request_id="req1",
                requesting_surface="action_legality_service",
                owner_family="actor_identity_owner",
                request_status="declared",
                subject_ref=subject,
                authority_flags=StateOwnerInterfaceAuthorityFlags(
                    state_read_authorized=True,
                ),
            )

    def test_request_rejects_raw_state_access_authority(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceAuthorityFlagsError,
            StateOwnerInterfaceAuthorityFlags,
            StateOwnerInterfaceReference,
            StateOwnerInterfaceRequest,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        with pytest.raises(InvalidStateOwnerInterfaceAuthorityFlagsError):
            StateOwnerInterfaceRequest(
                request_id="req1",
                requesting_surface="action_legality_service",
                owner_family="actor_identity_owner",
                request_status="declared",
                subject_ref=subject,
                authority_flags=StateOwnerInterfaceAuthorityFlags(
                    raw_state_access_authorized=True,
                ),
            )

    def test_request_rejects_state_mutation_authority(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceAuthorityFlagsError,
            StateOwnerInterfaceAuthorityFlags,
            StateOwnerInterfaceReference,
            StateOwnerInterfaceRequest,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        with pytest.raises(InvalidStateOwnerInterfaceAuthorityFlagsError):
            StateOwnerInterfaceRequest(
                request_id="req1",
                requesting_surface="action_legality_service",
                owner_family="actor_identity_owner",
                request_status="declared",
                subject_ref=subject,
                authority_flags=StateOwnerInterfaceAuthorityFlags(
                    state_mutation_authorized=True,
                ),
            )


# ---------------------------------------------------------------------------
# T16 — Interface result requires valid result status
# ---------------------------------------------------------------------------

class TestInterfaceResultValidation:
    def test_valid_result(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateOwnerInterfaceResult,
            validate_state_owner_interface_result,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        res = StateOwnerInterfaceResult(
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            result_status="unavailable",
            subject_ref=subject,
        )
        assert validate_state_owner_interface_result(res)

    def test_invalid_result_status(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceResultError,
            StateOwnerInterfaceReference,
            StateOwnerInterfaceResult,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        with pytest.raises(InvalidStateOwnerInterfaceResultError):
            StateOwnerInterfaceResult(
                result_id="res1",
                request_id="req1",
                owner_family="actor_identity_owner",
                result_status="legal",
                subject_ref=subject,
            )


# ---------------------------------------------------------------------------
# T17 — Interface result rejects actual state payload fields or committed deltas
# ---------------------------------------------------------------------------

class TestInterfaceResultNoPayload:
    def test_result_has_no_payload_fields(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateOwnerInterfaceResult,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        res = StateOwnerInterfaceResult(
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            result_status="unavailable",
            subject_ref=subject,
        )
        d = res.to_dict()
        assert "state_payload" not in d
        assert "projection_payload" not in d
        assert "committed_delta" not in d
        assert "hidden_facts" not in d


# ---------------------------------------------------------------------------
# T18 — Unavailable/deferred/unknown builders produce only allowed skeleton statuses
# ---------------------------------------------------------------------------

class TestResultBuilders:
    def _make_subject(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
        )
        return StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )

    def test_unavailable_builder(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_INTERFACE_RESULT_STATUSES,
            build_unavailable_state_owner_interface_result,
        )
        res = build_unavailable_state_owner_interface_result(
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            subject_ref=self._make_subject(),
        )
        assert res.result_status == "unavailable"
        assert res.result_status in STATE_OWNER_INTERFACE_RESULT_STATUSES

    def test_deferred_builder(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_INTERFACE_RESULT_STATUSES,
            build_deferred_state_owner_interface_result,
        )
        res = build_deferred_state_owner_interface_result(
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            subject_ref=self._make_subject(),
        )
        assert res.result_status == "deferred"
        assert res.result_status in STATE_OWNER_INTERFACE_RESULT_STATUSES

    def test_unknown_builder(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            STATE_OWNER_INTERFACE_RESULT_STATUSES,
            build_unknown_state_owner_interface_result,
        )
        res = build_unknown_state_owner_interface_result(
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            subject_ref=self._make_subject(),
        )
        assert res.result_status == "unknown"
        assert res.result_status in STATE_OWNER_INTERFACE_RESULT_STATUSES


# ---------------------------------------------------------------------------
# T19 — Backend serializer is deterministic and JSON-safe
# ---------------------------------------------------------------------------

class TestBackendSerializer:
    def test_backend_serializer_deterministic_and_json_safe(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateOwnerInterfaceResult,
            serialize_state_owner_interface_result,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        res = StateOwnerInterfaceResult(
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            result_status="unavailable",
            subject_ref=subject,
        )
        backend = serialize_state_owner_interface_result(res)
        assert json.dumps(backend, sort_keys=True)
        second = serialize_state_owner_interface_result(res)
        assert json.dumps(backend, sort_keys=True) == json.dumps(second, sort_keys=True)


# ---------------------------------------------------------------------------
# T20 — Visible serializer excludes backend/internal/hidden/projection/state payload fields
# ---------------------------------------------------------------------------

class TestVisibleSerializerExcludesBackend:
    _FORBIDDEN_KEYS = {
        "subject_ref",
        "projection_request_ref",
        "dependency_declarations",
        "authority_flags",
        "metadata",
        "backend_only",
        "hidden_information",
        "state_payload",
        "projection_payload",
        "committed_delta",
    }

    def _make_result(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            StateOwnerInterfaceReference,
            StateOwnerInterfaceResult,
            StateVisibilityDescriptor,
        )
        subject = StateOwnerInterfaceReference(
            reference_id="sub1",
            reference_kind="state_record_ref",
            owner_family="actor_identity_owner",
            source_scope="test",
        )
        visibility = StateVisibilityDescriptor(
            visibility_id="vis1",
            visibility_tier="player_visible",
            player_visible_allowed=True,
        )
        return StateOwnerInterfaceResult(
            result_id="res1",
            request_id="req1",
            owner_family="actor_identity_owner",
            result_status="unavailable",
            subject_ref=subject,
            visibility_descriptor=visibility,
        )

    def test_visible_serializer_excludes_forbidden_keys(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            serialize_state_owner_interface_result_visible,
        )
        res = self._make_result()
        visible = serialize_state_owner_interface_result_visible(res)
        for key in self._FORBIDDEN_KEYS:
            assert key not in visible, f"Visible serializer leaked {key!r}"

    def test_visible_serializer_has_expected_keys(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            serialize_state_owner_interface_result_visible,
        )
        res = self._make_result()
        visible = serialize_state_owner_interface_result_visible(res)
        expected_keys = {
            "result_id", "request_id", "owner_family", "result_status",
            "non_authority_note", "visibility_tier", "player_visible_allowed",
            "redaction_required",
        }
        assert set(visible.keys()) == expected_keys


# ---------------------------------------------------------------------------
# T21 — Metadata rejects non-JSON-safe values
# ---------------------------------------------------------------------------

class TestMetadataSafety:
    def test_metadata_rejects_non_json_safe(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            InvalidStateOwnerInterfaceReferenceError,
            StateOwnerInterfaceReference,
        )
        with pytest.raises(InvalidStateOwnerInterfaceReferenceError):
            StateOwnerInterfaceReference(
                reference_id="ref1",
                reference_kind="state_record_ref",
                owner_family="actor_identity_owner",
                source_scope="test",
                metadata={"bad": object()},
            )


# ---------------------------------------------------------------------------
# T22 — Public names contain no forbidden execution/mutation/model/prompt/narration patterns
# ---------------------------------------------------------------------------

class TestPublicSurfaceNameInspection:
    _FORBIDDEN_PATTERNS = (
        "execute", "mutate", "commit_event", "model_call",
        "prompt_render", "narration", "live_play_run",
        "persist_write", "replay_run",
    )

    def test_public_names_no_execution_patterns(self):
        from astra_runtime.domain.state_owner_interface_contract_skeleton import (
            __all__ as RT001H_ALL,
        )
        for name in RT001H_ALL:
            lower = name.lower()
            for pat in self._FORBIDDEN_PATTERNS:
                assert pat not in lower, (
                    f"Public name {name!r} contains forbidden pattern {pat!r}"
                )


# ---------------------------------------------------------------------------
# T23 — Module imports no forbidden downstream implementation modules
# ---------------------------------------------------------------------------

class TestImportBoundaryEnforcement:
    _FORBIDDEN_MODULES = (
        "state_store", "state_projection", "transaction_lifecycle",
        "event_commitment", "model_boundary", "tiny_vertical_slice",
        "context_packet_compiler", "live_play", "resource_consequence_math",
    )

    def test_rt001h_does_not_import_forbidden_modules(self):
        src = (
            REPO_ROOT
            / "src"
            / "astra_runtime"
            / "domain"
            / "state_owner_interface_contract_skeleton.py"
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
                    f"RT-001H imports forbidden module pattern "
                    f"{forbidden!r} via {mod_name!r}"
                )


# ---------------------------------------------------------------------------
# T24 — Domain package exports include the new RT-001H public surface
# ---------------------------------------------------------------------------

class TestDomainPackageExports:
    def test_domain_package_exports_rt001h_constants(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "STATE_OWNER_INTERFACE_FAMILIES")
        assert hasattr(domain, "STATE_OWNER_DEPENDENCY_OWNER_FAMILIES")
        assert hasattr(domain, "STATE_OWNER_INTERFACE_REQUEST_STATUSES")
        assert hasattr(domain, "STATE_OWNER_INTERFACE_RESULT_STATUSES")
        assert hasattr(domain, "STATE_OWNER_VISIBILITY_TIERS")
        assert hasattr(domain, "STATE_OWNER_PROJECTION_KINDS")
        assert hasattr(domain, "STATE_OWNER_REFERENCE_KINDS")
        assert hasattr(domain, "STATE_OWNER_DENIAL_REASONS")
        assert hasattr(domain, "STATE_OWNER_NON_AUTHORITY_NOTE")

    def test_domain_package_exports_rt001h_dataclasses(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "StateOwnerInterfaceAuthorityFlags")
        assert hasattr(domain, "StateOwnerInterfaceReference")
        assert hasattr(domain, "StateVisibilityDescriptor")
        assert hasattr(domain, "StateProjectionRequestReference")
        assert hasattr(domain, "StateOwnerDependencyDeclaration")
        assert hasattr(domain, "StateOwnerInterfaceRequest")
        assert hasattr(domain, "StateOwnerInterfaceResult")
        assert hasattr(domain, "StateOwnerInterfaceContractSummary")

    def test_domain_package_exports_rt001h_functions(self):
        import astra_runtime.domain as domain
        assert hasattr(domain, "create_state_owner_interface_authority_flags")
        assert hasattr(domain, "create_state_owner_interface_reference")
        assert hasattr(domain, "create_state_visibility_descriptor")
        assert hasattr(domain, "create_state_projection_request_reference")
        assert hasattr(domain, "create_state_owner_dependency_declaration")
        assert hasattr(domain, "create_state_owner_interface_request")
        assert hasattr(domain, "create_state_owner_interface_result")
        assert hasattr(domain, "create_state_owner_interface_contract_summary")
        assert hasattr(domain, "build_state_owner_dependency_manifest")
        assert hasattr(domain, "build_unavailable_state_owner_interface_result")
        assert hasattr(domain, "build_deferred_state_owner_interface_result")
        assert hasattr(domain, "build_unknown_state_owner_interface_result")
        assert hasattr(domain, "serialize_state_owner_interface_result")
        assert hasattr(domain, "serialize_state_owner_interface_result_visible")
        assert hasattr(domain, "validate_state_owner_interface_authority_flags")
        assert hasattr(domain, "validate_state_owner_interface_reference")
        assert hasattr(domain, "validate_state_visibility_descriptor")
        assert hasattr(domain, "validate_state_projection_request_reference")
        assert hasattr(domain, "validate_state_owner_dependency_declaration")
        assert hasattr(domain, "validate_state_owner_interface_request")
        assert hasattr(domain, "validate_state_owner_interface_result")
        assert hasattr(domain, "validate_state_owner_interface_contract_summary")


# ---------------------------------------------------------------------------
# T25 — RT-001H branch does not modify action legality implementation files
# ---------------------------------------------------------------------------

class TestNoModificationOfActionLegalityFiles:
    def test_action_legality_files_not_modified(self):
        protected_files = [
            "src/astra_runtime/domain/action_legality.py",
            "src/astra_runtime/domain/action_legality_skeleton.py",
            "src/astra_runtime/domain/action_legality_gate_integration_skeleton.py",
            "src/astra_runtime/domain/action_legality_service_interface_contract_skeleton.py",
        ]
        for path in protected_files:
            result = subprocess.run(
                ["git", "diff", "origin/main", "--", path],
                capture_output=True, text=True, cwd=REPO_ROOT,
            )
            assert result.returncode == 0, "git diff failed"
            assert not result.stdout.strip(), (
                f"RT-001H branch modifies protected action legality file: {path}"
            )


# ---------------------------------------------------------------------------
# T26 — RT-001B through RT-001G tests still pass
# ---------------------------------------------------------------------------

class TestExistingTestsStillPass:
    def test_rt001b_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001b_action_legality_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001B tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001c_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001c_action_legality_gate_integration_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001C tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001d_tests_pass(self):
        # RT-001D's TestImplementationModuleSafety asserts that no files under
        # src/astra_runtime/domain/ differ from origin/main...HEAD. That guardrail
        # is correct for the review-only RT-001D branch but legitimately fails on
        # the RT-001H branch because RT-001H adds a new runtime module. Run the
        # functional tests only.
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001d_action_legality_integration_hardening_review.py",
                "-q", "--tb=short",
                "-k", "not TestImplementationModuleSafety",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001D tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001e_tests_pass(self):
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001e_action_legality_service_interface_contract_skeleton.py",
                "-q", "--tb=short",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001E tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001f_tests_pass(self):
        # RT-001F's TestExistingTestsStillPass runs RT-001D recursively, which
        # includes RT-001D's branch-specific TestImplementationModuleSafety
        # guardrail. That guardrail fails on the RT-001H branch because RT-001H
        # adds a new runtime module. Run RT-001F's own functional tests only.
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py",
                "-q", "--tb=short",
                "-k", "not TestExistingTestsStillPass",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001F tests failed:\n{result.stdout}\n{result.stderr}"
        )

    def test_rt001g_tests_pass(self):
        # RT-001G includes TestNoModificationOfRuntimeModules which asserts that
        # no files under src/astra_runtime/ differ from origin/main. That guardrail
        # is correct for the review-only RT-001G branch but will legitimately fail
        # on the RT-001H branch because RT-001H adds a new runtime module and
        # updates __init__.py exports. RT-001G's TestExistingTestsStillPass also
        # runs RT-001D/RT-001F recursively and therefore hits the same branch-
        # specific guardrails. Run RT-001G's own functional tests only.
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "tests/test_runtime_domain_rt_001g_state_owner_interface_prerequisite_review.py",
                "-q", "--tb=short",
                "-k", "not TestNoModificationOfRuntimeModules and not TestExistingTestsStillPass",
            ],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"RT-001G functional tests failed:\n{result.stdout}\n{result.stderr}"
        )


# ---------------------------------------------------------------------------
# T27 — Registry contains RT-001H file record
# ---------------------------------------------------------------------------

class TestRegistryContainsRt001hRecord:
    def test_registry_contains_rt001h_file_record(self):
        import yaml
        registry_path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        file_records = registry.get("file_records", [])
        rt001h_records = [
            r for r in file_records
            if "RT-001H" in str(r.get("file_id", "")) or
               "state_owner_interface_contract_skeleton" in str(r.get("filename", ""))
        ]
        assert rt001h_records, "Registry does not contain RT-001H file record"

    def test_registry_rt001h_record_is_skeleton(self):
        import yaml
        registry_path = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        file_records = registry.get("file_records", [])
        rt001h_records = [
            r for r in file_records
            if "RT-001H" in str(r.get("file_id", "")) or
               "state_owner_interface_contract_skeleton" in str(r.get("filename", ""))
        ]
        assert rt001h_records
        for record in rt001h_records:
            authority = str(record.get("authority_level", "")).lower()
            notes = str(record.get("notes", "")).lower()
            assert authority == "skeleton" or "skeleton" in notes, (
                "RT-001H registry record must be authority level skeleton and note skeleton-only"
            )


# ---------------------------------------------------------------------------
# T28 — Decision log contains RT-001H entry
# ---------------------------------------------------------------------------

class TestDecisionLogContainsRt001hEntry:
    def test_decision_log_contains_rt001h_entry(self):
        log_path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        content = log_path.read_text(encoding="utf-8")
        assert "RUNTIME-DOMAIN-RT-001H" in content, (
            "Decision log does not contain RT-001H entry"
        )

    def test_decision_log_rt001h_entry_notes_next_step(self):
        log_path = REPO_ROOT / "docs" / "decisions" / "current_decisions_log.md"
        content = log_path.read_text(encoding="utf-8")
        assert "RT-001I" in content, (
            "RT-001H decision log entry must reference RT-001I next step"
        )
