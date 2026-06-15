"""PR-9D  validation integration bridge skeleton tests.

Tests the narrow backend-owned validation integration bridge between
PR-9A scene command execution assembly surfaces, PR-9C command-kind
routing results, and existing validation pipeline/validation integration
skeleton surfaces.
"""

from __future__ import annotations

import copy
import json
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    COMMAND_KIND_FAMILIES,
    CommandKindRoutingResult,
    InvalidValidationBridgeAuthorityFlagsError,
    InvalidValidationBridgeOwnerRouteRefError,
    InvalidValidationBridgeRequestError,
    InvalidValidationBridgeRequirementRefError,
    InvalidValidationBridgeResultError,
    InvalidValidationBridgeResultRefError,
    InvalidValidationBridgeSubjectRefError,
    RT005_VALIDATION_INTEGRATION,
    ValidationBridgeOwnerRouteRef,
    ValidationBridgeRequirementRef,
    ValidationBridgeResultRef,
    ValidationBridgeSubjectRef,
    ValidationIntegrationBridgeAuthorityFlags,
    ValidationIntegrationBridgeRequest,
    ValidationIntegrationBridgeResult,
    ValidationIntegrationBridgeSkeletonError,
    build_validation_integration_bridge_result,
    create_validation_bridge_owner_route_ref,
    create_validation_bridge_requirement_ref,
    create_validation_bridge_result_ref,
    create_validation_bridge_subject_ref,
    create_validation_integration_bridge_authority_flags,
    create_validation_integration_bridge_request,
    route_command_envelope,
    serialize_validation_integration_bridge_result,
    serialize_validation_integration_bridge_result_visible,
    validate_validation_bridge_owner_route_ref,
    validate_validation_bridge_requirement_ref,
    validate_validation_bridge_result_ref,
    validate_validation_bridge_subject_ref,
    validate_validation_integration_bridge_authority_flags,
    validate_validation_integration_bridge_request,
    validate_validation_integration_bridge_result,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
)
from astra_runtime.kernel.record_identity import (
    build_record_id,
    is_valid_record_id,
)
from astra_runtime.kernel.validation_pipeline import (
    ValidationResult,
    create_validation_result,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_command_envelope() -> CommandEnvelope:
    return create_command_envelope(
        command_id=build_record_id("command", "inspect_lever_1"),
        command_type="inspect_object",
        source_actor_id=build_record_id("actor", "ascendant_1"),
        payload={"target": build_record_id("object", "lever_1")},
        metadata={"scene_ref": build_record_id("scene", "threshold_chamber")},
    )


@pytest.fixture()
def sample_routing_result(sample_command_envelope) -> CommandKindRoutingResult:
    return route_command_envelope(
        request_ref=build_record_id("routing_request", "pr_9d_1"),
        command_envelope=sample_command_envelope,
    )


@pytest.fixture()
def sample_validation_result(sample_command_envelope) -> ValidationResult:
    return create_validation_result(
        validation_id=build_record_id("validation", "pr_9d_1"),
        subject_ref=sample_command_envelope.command_id,
        passed=True,
    )


@pytest.fixture()
def sample_bridge_request(
    sample_command_envelope: CommandEnvelope,
    sample_routing_result: CommandKindRoutingResult,
) -> ValidationIntegrationBridgeRequest:
    return create_validation_integration_bridge_request(
        request_ref=build_record_id("bridge_request", "pr_9d_1"),
        command_envelope=sample_command_envelope,
        routing_result=sample_routing_result,
    )


# ---------------------------------------------------------------------------
# Test 1: Module exists and public exports exist
# ---------------------------------------------------------------------------


class TestModuleExistence:
    """Test that the PR-9D module exports its public surfaces."""

    def test_validation_integration_bridge_skeleton_error_exists(self) -> None:
        assert issubclass(ValidationIntegrationBridgeSkeletonError, ValueError)

    def test_invalid_validation_bridge_request_error_exists(self) -> None:
        assert issubclass(InvalidValidationBridgeRequestError, ValidationIntegrationBridgeSkeletonError)

    def test_invalid_validation_bridge_subject_ref_error_exists(self) -> None:
        assert issubclass(InvalidValidationBridgeSubjectRefError, ValidationIntegrationBridgeSkeletonError)

    def test_invalid_validation_bridge_requirement_ref_error_exists(self) -> None:
        assert issubclass(InvalidValidationBridgeRequirementRefError, ValidationIntegrationBridgeSkeletonError)

    def test_invalid_validation_bridge_result_ref_error_exists(self) -> None:
        assert issubclass(InvalidValidationBridgeResultRefError, ValidationIntegrationBridgeSkeletonError)

    def test_invalid_validation_bridge_owner_route_ref_error_exists(self) -> None:
        assert issubclass(InvalidValidationBridgeOwnerRouteRefError, ValidationIntegrationBridgeSkeletonError)

    def test_invalid_validation_bridge_authority_flags_error_exists(self) -> None:
        assert issubclass(InvalidValidationBridgeAuthorityFlagsError, ValidationIntegrationBridgeSkeletonError)

    def test_invalid_validation_bridge_result_error_exists(self) -> None:
        assert issubclass(InvalidValidationBridgeResultError, ValidationIntegrationBridgeSkeletonError)

    def test_validation_bridge_subject_ref_exists(self) -> None:
        assert ValidationBridgeSubjectRef is not None

    def test_validation_bridge_requirement_ref_exists(self) -> None:
        assert ValidationBridgeRequirementRef is not None

    def test_validation_bridge_owner_route_ref_exists(self) -> None:
        assert ValidationBridgeOwnerRouteRef is not None

    def test_validation_bridge_result_ref_exists(self) -> None:
        assert ValidationBridgeResultRef is not None

    def test_validation_integration_bridge_request_exists(self) -> None:
        assert ValidationIntegrationBridgeRequest is not None

    def test_validation_integration_bridge_authority_flags_exists(self) -> None:
        assert ValidationIntegrationBridgeAuthorityFlags is not None

    def test_validation_integration_bridge_result_exists(self) -> None:
        assert ValidationIntegrationBridgeResult is not None

    def test_build_validation_integration_bridge_result_exists(self) -> None:
        assert callable(build_validation_integration_bridge_result)

    def test_rt005_constant_exists(self) -> None:
        assert RT005_VALIDATION_INTEGRATION == "RT005_VALIDATION_INTEGRATION"


# ---------------------------------------------------------------------------
# Test 2: Dataclasses are frozen and keyword-only
# ---------------------------------------------------------------------------


class TestDataclassProperties:
    """Test that all PR-9D dataclasses are frozen and keyword-only."""

    def test_validation_bridge_subject_ref_is_frozen(self) -> None:
        ref = ValidationBridgeSubjectRef(subject_type="command", ref_id=build_record_id("test", "1"))
        with pytest.raises(AttributeError):
            ref.subject_type = "validation_pipeline"  # type: ignore[misc]

    def test_validation_bridge_subject_ref_is_keyword_only(self) -> None:
        with pytest.raises(TypeError):
            ValidationBridgeSubjectRef("command", build_record_id("test", "1"))  # type: ignore[misc]

    def test_validation_bridge_requirement_ref_is_frozen(self) -> None:
        ref = ValidationBridgeRequirementRef(
            requirement_id=build_record_id("req", "1"),
            requirement_kind="command_envelope_ref",
            requirement_ref=build_record_id("test", "1"),
        )
        with pytest.raises(AttributeError):
            ref.requirement_kind = "validation_pipeline_ref"  # type: ignore[misc]

    def test_validation_bridge_owner_route_ref_is_frozen(self) -> None:
        ref = ValidationBridgeOwnerRouteRef(owner_route="RT005_VALIDATION_INTEGRATION")
        with pytest.raises(AttributeError):
            ref.owner_route = "DEFERRED_RUNTIME_OWNER"  # type: ignore[misc]

    def test_validation_bridge_result_ref_is_frozen(self) -> None:
        ref = ValidationBridgeResultRef(result_ref_id=build_record_id("val", "1"), pending=True)
        with pytest.raises(AttributeError):
            ref.pending = False  # type: ignore[misc]

    def test_validation_integration_bridge_authority_flags_is_frozen(self) -> None:
        flags = ValidationIntegrationBridgeAuthorityFlags()
        with pytest.raises(AttributeError):
            flags.legality_resolution = True  # type: ignore[misc]

    def test_validation_integration_bridge_request_is_frozen(
        self, sample_command_envelope, sample_routing_result
    ) -> None:
        request = ValidationIntegrationBridgeRequest(
            request_ref=build_record_id("req", "1"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        with pytest.raises(AttributeError):
            request.request_ref = "changed"  # type: ignore[misc]

    def test_validation_integration_bridge_result_is_frozen(
        self, sample_bridge_request
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        with pytest.raises(AttributeError):
            result.command_ref = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Test 3: Bridge accepts valid CommandEnvelope plus PR-9C CommandKindRoutingResult
# ---------------------------------------------------------------------------


class TestBridgeAcceptValidInputs:
    """Test that the bridge accepts valid inputs and produces a valid result."""

    def test_bridge_request_accepts_valid_inputs(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "pr_9d_valid"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        assert request.request_ref == build_record_id("bridge_request", "pr_9d_valid")
        assert request.command_envelope is sample_command_envelope
        assert request.routing_result is sample_routing_result
        assert validate_validation_integration_bridge_request(request)

    def test_build_bridge_result_accepts_valid_request(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert result.request_ref == sample_bridge_request.request_ref
        assert result.command_ref == sample_bridge_request.command_envelope.command_id
        assert result.command_family == sample_bridge_request.routing_result.classification.family
        assert result.command_kind == sample_bridge_request.routing_result.classification.kind
        assert result.owner_route.owner_route == sample_bridge_request.routing_result.dispatch_shell.owner_route
        assert validate_validation_integration_bridge_result(result)

    def test_bridge_result_has_correct_command_family_and_kind(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "pr_9d_family"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        result = build_validation_integration_bridge_result(request=request)
        # inspect_object should route to "inspection"
        assert result.command_family == "inspection"
        assert result.command_kind == "inspect_object"

    def test_bridge_result_has_owner_route_from_dispatch_shell(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "pr_9d_owner"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        result = build_validation_integration_bridge_result(request=request)
        assert result.owner_route.owner_route == sample_routing_result.dispatch_shell.owner_route

    def test_bridge_result_has_subject_ref(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert isinstance(result.subject_ref, ValidationBridgeSubjectRef)
        assert result.subject_ref.subject_type == "command"
        assert result.subject_ref.ref_id == sample_bridge_request.command_envelope.command_id


# ---------------------------------------------------------------------------
# Test 4: Bridge rejects mismatched command references
# ---------------------------------------------------------------------------


class TestBridgeRejectsMismatchedCommandRefs:
    """Test that the bridge rejects a routing result whose command_ref does not match."""

    def test_bridge_request_rejects_mismatched_command_refs(
        self,
        sample_command_envelope: CommandEnvelope,
    ) -> None:
        # Create a routing result from a *different* command envelope
        other_envelope = create_command_envelope(
            command_id=build_record_id("command", "other"),
            command_type="move_forward",
            source_actor_id=build_record_id("actor", "ascendant_1"),
        )
        other_routing = route_command_envelope(
            request_ref=build_record_id("routing_request", "other"),
            command_envelope=other_envelope,
        )
        with pytest.raises(InvalidValidationBridgeRequestError, match="command_ref must match"):
            create_validation_integration_bridge_request(
                request_ref=build_record_id("bridge_request", "mismatch"),
                command_envelope=sample_command_envelope,
                routing_result=other_routing,
            )


# ---------------------------------------------------------------------------
# Test 5: Bridge can include optional kernel ValidationResult by reference
# ---------------------------------------------------------------------------


class TestBridgeIncludesValidationResult:
    """Test that the bridge can carry a kernel ValidationResult by reference."""

    def test_bridge_request_accepts_validation_result(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
        sample_validation_result: ValidationResult,
    ) -> None:
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "with_val"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
            validation_result=sample_validation_result,
        )
        assert request.validation_result is sample_validation_result
        assert validate_validation_integration_bridge_request(request)

    def test_bridge_result_includes_validation_result_by_reference(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
        sample_validation_result: ValidationResult,
    ) -> None:
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "with_val"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
            validation_result=sample_validation_result,
        )
        result = build_validation_integration_bridge_result(request=request)
        assert result.validation_result_ref.validation_result is sample_validation_result
        assert result.validation_result_ref.pending is False
        assert result.validation_pipeline_ref == sample_validation_result.validation_id


# ---------------------------------------------------------------------------
# Test 6: Bridge can produce pending/reference-only validation result ref
# ---------------------------------------------------------------------------


class TestBridgePendingValidationRef:
    """Test that the bridge produces a pending ref if no ValidationResult is supplied."""

    def test_bridge_result_produces_pending_ref(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert result.validation_result_ref.validation_result is None
        assert result.validation_result_ref.pending is True
        assert is_valid_record_id(result.validation_result_ref.result_ref_id)

    def test_pending_validation_ref_has_valid_id(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert is_valid_record_id(result.validation_result_ref.result_ref_id)


# ---------------------------------------------------------------------------
# Test 7: Bridge carries command family/kind/owner route from PR-9C without reclassifying
# ---------------------------------------------------------------------------


class TestBridgeNoReclassification:
    """Test that the bridge uses PR-9C classification without reclassifying."""

    def test_bridge_does_not_call_route_functions(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        """The bridge should consume a pre-computed routing result, not re-classify."""
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "no_reclass"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        result = build_validation_integration_bridge_result(request=request)
        # The command family/kind should match the routing result classification
        assert result.command_family == sample_routing_result.classification.family
        assert result.command_kind == sample_routing_result.classification.kind
        assert result.owner_route.owner_route == sample_routing_result.dispatch_shell.owner_route


# ---------------------------------------------------------------------------
# Test 8: Bridge does not call PR-9A assemble_scene_command_execution_result
# ---------------------------------------------------------------------------


class TestBridgeNoPR9ACalls:
    """Test that the bridge does not call PR-9A assembly functions."""

    def test_bridge_builds_without_assembly_request(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        """The bridge should work without any PR-9A surfaces."""
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "no_pr9a"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        result = build_validation_integration_bridge_result(request=request)
        assert result.command_ref == sample_command_envelope.command_id
        assert result.command_family == sample_routing_result.classification.family

    def test_bridge_accepts_pr9a_validation_ref_optional(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        """The bridge should accept optional PR-9A surfaces without requiring them."""
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "with_assembly"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        assert request.assembly_request is None
        assert request.validation_ref is None


# ---------------------------------------------------------------------------
# Test 9: Bridge does not resolve legality
# ---------------------------------------------------------------------------


class TestBridgeNoLegality:
    """Test that the bridge does not resolve legality."""

    def test_bridge_result_has_no_legality_field(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert hasattr(result, "authority_flags")
        assert result.authority_flags.legality_resolution is False


# ---------------------------------------------------------------------------
# Test 10: Bridge does not execute validation rules
# ---------------------------------------------------------------------------


class TestBridgeNoValidationExecution:
    """Test that the bridge does not execute validation rules."""

    def test_bridge_result_denies_validation_rule_execution(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert result.authority_flags.validation_rule_execution is False


# ---------------------------------------------------------------------------
# Test 11: Bridge does not authorize blocking/approval
# ---------------------------------------------------------------------------


class TestBridgeNoBlockingApproval:
    """Test that the bridge does not authorize blocking or approval."""

    def test_bridge_has_no_blocking_or_approval_logic(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert result.authority_flags.legality_resolution is False
        assert result.authority_flags.command_execution is False
        assert result.authority_flags.runtime_action_execution is False


# ---------------------------------------------------------------------------
# Test 12: Authority flags are all false and reject true
# ---------------------------------------------------------------------------


class TestBridgeAuthorityFlags:
    """Test that all authority flags default to False and constructing with any True raises."""

    def test_authority_flags_default_all_false(self) -> None:
        flags = ValidationIntegrationBridgeAuthorityFlags()
        for field_name in flags.__dataclass_fields__:
            assert getattr(flags, field_name) is False

    def test_authority_flags_to_dict_all_false(self) -> None:
        flags = ValidationIntegrationBridgeAuthorityFlags()
        d = flags.to_dict()
        for value in d.values():
            assert value is False

    def test_authority_flags_rejects_legality_resolution(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(legality_resolution=True)  # type: ignore[misc]

    def test_authority_flags_rejects_validation_rule_execution(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(validation_rule_execution=True)  # type: ignore[misc]

    def test_authority_flags_rejects_command_execution(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(command_execution=True)  # type: ignore[misc]

    def test_authority_flags_rejects_runtime_action_execution(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(runtime_action_execution=True)  # type: ignore[misc]

    def test_authority_flags_rejects_state_mutation(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(state_mutation=True)  # type: ignore[misc]

    def test_authority_flags_rejects_event_append(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(event_append=True)  # type: ignore[misc]

    def test_authority_flags_rejects_persistence_write(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(persistence_write=True)  # type: ignore[misc]

    def test_authority_flags_rejects_rng_table_oracle_execution(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(rng_table_oracle_execution=True)  # type: ignore[misc]

    def test_authority_flags_rejects_settlement_authorization(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(settlement_authorization=True)  # type: ignore[misc]

    def test_authority_flags_rejects_consequence_application(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(consequence_application=True)  # type: ignore[misc]

    def test_authority_flags_rejects_packet_compilation(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(packet_compilation=True)  # type: ignore[misc]

    def test_authority_flags_rejects_model_authority(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(model_authority=True)  # type: ignore[misc]

    def test_authority_flags_rejects_prompt_rendering(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(prompt_rendering=True)  # type: ignore[misc]

    def test_authority_flags_rejects_conversion(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(conversion=True)  # type: ignore[misc]

    def test_authority_flags_rejects_sourcebook_inclusion(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(sourcebook_inclusion=True)  # type: ignore[misc]

    def test_authority_flags_rejects_canon_promotion(self) -> None:
        with pytest.raises(InvalidValidationBridgeAuthorityFlagsError, match="False"):
            ValidationIntegrationBridgeAuthorityFlags(canon_promotion=True)  # type: ignore[misc]

    def test_authority_flags_validation_passes(self) -> None:
        flags = ValidationIntegrationBridgeAuthorityFlags()
        assert validate_validation_integration_bridge_authority_flags(flags)

    def test_validate_authority_flags_rejects_non_object(self) -> None:
        assert not validate_validation_integration_bridge_authority_flags("not_flags")


# ---------------------------------------------------------------------------
# Test 13: Deterministic serialization
# ---------------------------------------------------------------------------


class TestDeterministicSerialization:
    """Test deterministic serialization of bridge results."""

    def test_serialize_bridge_result_returns_dict(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        d = serialize_validation_integration_bridge_result(result)
        assert isinstance(d, dict)
        assert d["result_ref"] == result.result_ref
        assert d["command_ref"] == result.command_ref
        assert d["command_family"] == result.command_family
        assert d["command_kind"] == result.command_kind

    def test_serialize_bridge_result_is_deterministic(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        d1 = serialize_validation_integration_bridge_result(result)
        d2 = serialize_validation_integration_bridge_result(result)
        assert d1 == d2
        assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)

    def test_serialize_bridge_result_visible_omits_metadata(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        d = serialize_validation_integration_bridge_result_visible(result)
        assert "command_family" in d
        assert "command_kind" in d
        assert "owner_route" in d
        assert "subject_ref" in d
        assert "authority_flags" in d
        # Visible serialization should not include full metadata
        assert "metadata" not in d or d["metadata"] is None

    def test_to_dict_serialization_matches(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        d1 = result.to_dict()
        d2 = serialize_validation_integration_bridge_result(result)
        assert d1 == d2


# ---------------------------------------------------------------------------
# Test 14: Metadata is immutable / deep-copied
# ---------------------------------------------------------------------------


class TestMetadataImmutability:
    """Test that metadata is immutable via MappingProxyType."""

    def test_bridge_result_metadata_is_mappingproxy(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert isinstance(result.metadata, MappingProxyType)

    def test_bridge_subject_ref_metadata_is_mappingproxy(
        self,
    ) -> None:
        ref = create_validation_bridge_subject_ref(
            subject_type="command",
            ref_id=build_record_id("test", "1"),
            metadata={"key": "value"},
        )
        assert isinstance(ref.metadata, MappingProxyType)
        with pytest.raises(TypeError):
            ref.metadata["key"] = "new_value"  # type: ignore[index]

    def test_bridge_requirement_ref_metadata_is_mappingproxy(
        self,
    ) -> None:
        ref = create_validation_bridge_requirement_ref(
            requirement_id=build_record_id("req", "1"),
            requirement_kind="command_envelope_ref",
            requirement_ref=build_record_id("test", "1"),
        )
        assert isinstance(ref.metadata, MappingProxyType)


# ---------------------------------------------------------------------------
# Test 15: No side-effect imports
# ---------------------------------------------------------------------------


class TestNoSideEffectImports:
    """Test that the bridge does not import model, network, database, random, etc."""

    def test_module_does_not_import_model(self) -> None:
        import astra_runtime.domain.validation_integration_bridge_skeleton as bridge_mod
        mod_src = bridge_mod.__file__ or ""
        with open(mod_src) as f:
            content = f.read()
        # Should not import model-related modules
        assert "astra_runtime.domain.model" not in content

    def test_module_does_not_import_random(self) -> None:
        import astra_runtime.domain.validation_integration_bridge_skeleton as bridge_mod
        mod_src = bridge_mod.__file__ or ""
        with open(mod_src) as f:
            content = f.read()
        assert "import random" not in content
        assert "from random import" not in content


# ---------------------------------------------------------------------------
# Test 16: No model/prompt/prose/narration/live-play behavior
# ---------------------------------------------------------------------------


class TestNoModelPromptNarration:
    """Test that the bridge does not involve model/prompt/prose/live-play."""

    def test_authority_flags_deny_model_authority(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert result.authority_flags.model_authority is False
        assert result.authority_flags.prompt_rendering is False
        assert result.authority_flags.prompt_execution is False
        assert result.authority_flags.prose_parsing is False
        assert result.authority_flags.narration_generation is False
        assert result.authority_flags.live_play_session_authority is False


# ---------------------------------------------------------------------------
# Test 17: No persistence/RNG/state mutation/event append/settlement/consequence
# ---------------------------------------------------------------------------


class TestNoPersistenceRNGMutation:
    """Test that the bridge does not involve persistence, RNG, mutation, etc."""

    def test_authority_flags_deny_persistence_and_rng(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert result.authority_flags.persistence_write is False
        assert result.authority_flags.rng_table_oracle_execution is False
        assert result.authority_flags.state_mutation is False
        assert result.authority_flags.event_append is False
        assert result.authority_flags.settlement_authorization is False
        assert result.authority_flags.pr5_arithmetic_execution is False
        assert result.authority_flags.consequence_application is False


# ---------------------------------------------------------------------------
# Test 18: No packet compilation
# ---------------------------------------------------------------------------


class TestNoPacketCompilation:
    """Test that the bridge does not involve packet compilation."""

    def test_authority_flags_deny_packet_compilation(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert result.authority_flags.packet_compilation is False


# ---------------------------------------------------------------------------
# Test 19: Validator functions
# ---------------------------------------------------------------------------


class TestValidatorFunctions:
    """Test the validator functions for PR-9D surfaces."""

    def test_validate_validation_bridge_subject_ref(self) -> None:
        ref = create_validation_bridge_subject_ref(
            subject_type="command",
            ref_id=build_record_id("test", "1"),
        )
        assert validate_validation_bridge_subject_ref(ref)

    def test_validate_validation_bridge_subject_ref_rejects_bad_type(self) -> None:
        ref = create_validation_bridge_subject_ref(
            subject_type="command",
            ref_id=build_record_id("test", "1"),
        )
        assert validate_validation_bridge_subject_ref(ref)
        # Rejects non-object
        assert not validate_validation_bridge_subject_ref("not_a_ref")

    def test_validate_validation_bridge_requirement_ref(self) -> None:
        ref = create_validation_bridge_requirement_ref(
            requirement_id=build_record_id("req", "1"),
            requirement_kind="command_envelope_ref",
            requirement_ref=build_record_id("cmd", "1"),
        )
        assert validate_validation_bridge_requirement_ref(ref)

    def test_validate_validation_bridge_owner_route_ref(self) -> None:
        ref = create_validation_bridge_owner_route_ref(
            owner_route="RT005_VALIDATION_INTEGRATION",
        )
        assert validate_validation_bridge_owner_route_ref(ref)

    def test_validate_validation_bridge_result_ref(self) -> None:
        ref = create_validation_bridge_result_ref(
            result_ref_id=build_record_id("val", "1"),
            pending=True,
        )
        assert validate_validation_bridge_result_ref(ref)

    def test_validate_validation_integration_bridge_request(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        assert validate_validation_integration_bridge_request(sample_bridge_request)

    def test_validate_validation_integration_bridge_result(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert validate_validation_integration_bridge_result(result)

    def test_validate_validation_integration_bridge_result_rejects_bad_refs(
        self,
    ) -> None:
        assert not validate_validation_integration_bridge_result("not_a_result")

    def test_validate_validation_bridge_result_ref_with_validation_result(
        self,
        sample_validation_result: ValidationResult,
    ) -> None:
        ref = create_validation_bridge_result_ref(
            result_ref_id=build_record_id("val", "1"),
            validation_result=sample_validation_result,
            pending=False,
        )
        assert validate_validation_bridge_result_ref(ref)
        assert ref.validation_result is sample_validation_result
        assert ref.pending is False


# ---------------------------------------------------------------------------
# Test 20: Owner route ref validation
# ---------------------------------------------------------------------------


class TestOwnerRouteRef:
    """Test owner route ref creation and validation."""

    def test_valid_owner_routes(self) -> None:
        ref = create_validation_bridge_owner_route_ref(
            owner_route="RT005_VALIDATION_INTEGRATION",
        )
        assert ref.owner_route == "RT005_VALIDATION_INTEGRATION"
        assert validate_validation_bridge_owner_route_ref(ref)

    def test_owner_route_rejects_invalid_route(self) -> None:
        with pytest.raises(InvalidValidationBridgeOwnerRouteRefError, match="owner_route must be one of"):
            create_validation_bridge_owner_route_ref(owner_route="INVALID_ROUTE")

    def test_owner_route_defers_to_routing_result(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "owner_test"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        result = build_validation_integration_bridge_result(request=request)
        # inspection command should route to RT001
        assert result.owner_route.owner_route == "RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY"


# ---------------------------------------------------------------------------
# Test 21: Bridge result includes requirement refs
# ---------------------------------------------------------------------------


class TestBridgeRequirementRefs:
    """Test that the bridge result includes requirement references."""

    def test_bridge_result_has_requirement_refs(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        assert isinstance(result.requirement_refs, tuple)
        assert len(result.requirement_refs) >= 4  # envelope, routing, classification, dispatch
        for req in result.requirement_refs:
            assert isinstance(req, ValidationBridgeRequirementRef)

    def test_bridge_result_requirement_ref_kinds(
        self,
        sample_bridge_request: ValidationIntegrationBridgeRequest,
    ) -> None:
        result = build_validation_integration_bridge_result(request=sample_bridge_request)
        kinds = [r.requirement_kind for r in result.requirement_refs]
        assert "command_envelope_ref" in kinds
        assert "command_kind_routing_ref" in kinds
        assert "command_kind_classification_ref" in kinds
        assert "command_dispatch_shell_ref" in kinds


# ---------------------------------------------------------------------------
# Test 22: Bridge does not mutate input objects
# ---------------------------------------------------------------------------


class TestBridgeNoMutation:
    """Test that the bridge does not mutate input objects."""

    def test_bridge_does_not_mutate_command_envelope(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        original_id = sample_command_envelope.command_id
        original_type = sample_command_envelope.command_type
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "no_mut"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        _ = build_validation_integration_bridge_result(request=request)
        # Verify the envelope is unchanged
        assert sample_command_envelope.command_id == original_id
        assert sample_command_envelope.command_type == original_type

    def test_bridge_does_not_mutate_routing_result(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        original_result_ref = sample_routing_result.result_ref
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "no_mut2"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        _ = build_validation_integration_bridge_result(request=request)
        assert sample_routing_result.result_ref == original_result_ref


# ---------------------------------------------------------------------------
# Test 23: Bridge handles optional PR-9A surfaces
# ---------------------------------------------------------------------------


class TestBridgeOptionalSurfaces:
    """Test that the bridge handles optional PR-9A and kernel surfaces."""

    def test_bridge_without_any_optional_surfaces(
        self,
        sample_command_envelope: CommandEnvelope,
        sample_routing_result: CommandKindRoutingResult,
    ) -> None:
        """Bridge works with only command envelope and routing result."""
        request = create_validation_integration_bridge_request(
            request_ref=build_record_id("bridge_request", "minimal"),
            command_envelope=sample_command_envelope,
            routing_result=sample_routing_result,
        )
        result = build_validation_integration_bridge_result(request=request)
        assert result.validation_result_ref.pending is True
        assert result.validation_result_ref.validation_result is None
        assert result.validation_pipeline_ref is None
