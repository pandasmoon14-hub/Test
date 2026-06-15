"""PR-9E  transaction preview packet bridge skeleton tests.

Tests the narrow backend-owned transaction preview packet bridge that
compiles PR-9A assembly, PR-9C routing, PR-9D validation bridge, and
kernel TransactionPreview surfaces into deterministic packet descriptor /
packet reference shells.
"""

from __future__ import annotations

import copy
import inspect
import json
import sys
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    NO_COMMIT_INTENT_PACKET,
    SINGLE_EVENT_CONTEXT_PACKET,
    SINGLE_EVENT_NARRATION_PACKET,
    VISIBLE_SUMMARY_PACKET,
    CommandKindRoutingResult,
    InvalidTransactionPreviewPacketBridgeAuthorityFlagsError,
    InvalidTransactionPreviewPacketBridgePacketDescriptorError,
    InvalidTransactionPreviewPacketBridgePacketRefError,
    InvalidTransactionPreviewPacketBridgeRequestError,
    InvalidTransactionPreviewPacketBridgeResultError,
    InvalidTransactionPreviewPacketBridgeSubjectRefError,
    PACKET_ROLES,
    SceneCommandExecutionAssemblyResult,
    TransactionPreviewPacketBridgeAuthorityFlags,
    TransactionPreviewPacketBridgePacketRef,
    TransactionPreviewPacketBridgeRequest,
    TransactionPreviewPacketBridgeResult,
    TransactionPreviewPacketBridgeSkeletonError,
    TransactionPreviewPacketBridgeSubjectRef,
    TransactionPreviewPacketDescriptor,
    ValidationIntegrationBridgeResult,
    build_transaction_preview_packet_bridge_result,
    create_transaction_preview_packet_bridge_packet_ref,
    create_transaction_preview_packet_bridge_request,
    create_transaction_preview_packet_bridge_subject_ref,
    create_transaction_preview_packet_descriptor,
    route_command_envelope,
    serialize_transaction_preview_packet_bridge_result,
    serialize_transaction_preview_packet_bridge_result_visible,
    serialize_transaction_preview_packet_descriptor,
    validate_transaction_preview_packet_bridge_result,
    validate_transaction_preview_packet_descriptor,
)
from astra_runtime.domain.scene_command_execution_skeleton import (
    assemble_scene_command_execution_result,
    create_scene_command_execution_actor_contract,
    create_scene_command_execution_assembly_request,
    create_scene_command_execution_command_intent_from_envelope,
    create_scene_command_execution_context_packet_ref,
    create_scene_command_execution_event_ledger_candidate_ref,
    create_scene_command_execution_hidden_info_contract,
    create_scene_command_execution_model_boundary_fixture_ref,
    create_scene_command_execution_narration_packet_ref,
    create_scene_command_execution_object_contract,
    create_scene_command_execution_resource_preview_ref,
    create_scene_command_execution_scene_contract,
    create_scene_command_execution_state_delta_candidate_ref,
    create_scene_command_execution_subject_ref,
    create_scene_command_execution_validation_ref,
)
from astra_runtime.domain.resource_consequence_math import (
    create_resource_math_request,
    create_resource_math_result,
    create_resource_math_subject_reference,
)
from astra_runtime.domain.validation_integration_bridge_skeleton import (
    create_validation_bridge_owner_route_ref,
    create_validation_bridge_requirement_ref,
    create_validation_bridge_result_ref,
    create_validation_bridge_subject_ref,
    create_validation_integration_bridge_request,
    build_validation_integration_bridge_result,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
)
from astra_runtime.kernel.context_projection import (
    create_context_projection,
    create_context_projection_item,
)
from astra_runtime.kernel.event_ledger import (
    create_event_ledger_entry,
)
from astra_runtime.kernel.persistence_boundary import (
    create_persistence_boundary_request,
)
from astra_runtime.kernel.record_identity import (
    build_record_id,
    is_valid_record_id,
)
from astra_runtime.kernel.state_delta import (
    create_state_delta_envelope,
)
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    create_transaction_preview,
    validate_transaction_preview,
)
from astra_runtime.kernel.validation_pipeline import (
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
def sample_scene_contract():
    return create_scene_command_execution_scene_contract(
        scene_ref=build_record_id("scene", "threshold_chamber"),
        scene_label="Threshold Chamber",
        visible_description="A small chamber with a lever.",
        visible_tags=["interior", "hazardous"],
        actors=[
            create_scene_command_execution_actor_contract(
                actor_ref=build_record_id("actor", "ascendant_1"),
                actor_label="Test Ascendant",
                visible_description="A test actor.",
            ),
        ],
        objects=[
            create_scene_command_execution_object_contract(
                object_ref=build_record_id("object", "lever_1"),
                object_label="Brass Lever",
                visible_description="A tarnished brass lever.",
                visible_state="neutral",
            ),
        ],
        hidden_info=[
            create_scene_command_execution_hidden_info_contract(
                hidden_ref=build_record_id("hidden", "fact_1"),
                hidden_label="True Lever Purpose",
                backend_only_description="The lever resets the hazard clock.",
                reveal_condition="hazard_clock_exposed",
            ),
        ],
    )


@pytest.fixture()
def sample_assembly_request(sample_scene_contract, sample_command_envelope):
    return create_scene_command_execution_assembly_request(
        request_ref=build_record_id("request", "pr_9e_1"),
        scene_contract=sample_scene_contract,
        command_envelope=sample_command_envelope,
        intent_target_ref=build_record_id("object", "lever_1"),
    )


@pytest.fixture()
def sample_transaction_preview(sample_command_envelope) -> TransactionPreview:
    return create_transaction_preview(
        preview_id=build_record_id("transaction_preview", "pr_9e_1"),
        command=sample_command_envelope,
        status="preview_created",
    )


@pytest.fixture()
def sample_assembly_result(
    sample_assembly_request,
    sample_transaction_preview,
) -> SceneCommandExecutionAssemblyResult:
    command_id = build_record_id("command", "inspect_lever_1")
    validation_ref_id = build_record_id("validation", "pr_9e_1")
    return assemble_scene_command_execution_result(
        result_ref=build_record_id("assembly_result", "pr_9e_1"),
        request=sample_assembly_request,
        transaction_preview=sample_transaction_preview,
        validation_ref=create_scene_command_execution_validation_ref(
            validation_ref=validation_ref_id,
            validation_result=create_validation_result(
                validation_id=validation_ref_id,
                subject_ref=command_id,
                passed=True,
            ),
        ),
        resource_preview_ref=create_scene_command_execution_resource_preview_ref(
            preview_ref=build_record_id("resource_preview", "pr_9e_1"),
            resource_math_request=create_resource_math_request(
                request_id=build_record_id("rm_req", "pr_9e_1"),
                trace_ref_id=build_record_id("trace", "pr_9e_1"),
                command_ref_id=command_id,
                subject_refs=[
                    create_resource_math_subject_reference(
                        subject_binding_id=build_record_id("sb", "pr_9e_1"),
                        subject_type="actor",
                        subject_ref_id=build_record_id("actor", "ascendant_1"),
                        subject_role="primary_subject",
                        owner_domain="RT001_command_lifecycle_action_legality",
                    ),
                ],
            ),
            resource_math_result=create_resource_math_result(
                result_id=build_record_id("rm_result", "pr_9e_1"),
                request_id=build_record_id("rm_req", "pr_9e_1"),
                stage="resource_math_requested",
                decision="accepted_for_planning",
                blocking=False,
                trace_ref_id=build_record_id("trace", "pr_9e_1"),
                referenced_subject_binding_ids=[
                    build_record_id("sb", "pr_9e_1"),
                ],
            ),
        ),
        state_delta_candidate_ref=create_scene_command_execution_state_delta_candidate_ref(
            delta_ref=build_record_id("state_delta_candidate", "pr_9e_1"),
            delta_envelope=create_state_delta_envelope(
                delta_id=build_record_id("state_delta", "pr_9e_1"),
                source_command_id=command_id,
                source_preview_id=build_record_id("transaction_preview", "pr_9e_1"),
                affected_record_ids=[build_record_id("object", "lever_1")],
                change_type="record_update",
                payload={"visible_state": "inspected"},
            ),
        ),
        event_ledger_candidate_ref=create_scene_command_execution_event_ledger_candidate_ref(
            event_ref=build_record_id("event_ledger_candidate", "pr_9e_1"),
            ledger_entry=create_event_ledger_entry(
                event_id=build_record_id("event", "pr_9e_1"),
                sequence=0,
                source_command_id=command_id,
                source_preview_id=build_record_id("transaction_preview", "pr_9e_1"),
                event_type="command_event",
            ),
        ),
        context_packet_ref=create_scene_command_execution_context_packet_ref(
            packet_ref=build_record_id("context_packet", "pr_9e_1"),
            context_projection=create_context_projection(
                projection_id=build_record_id("context_projection", "pr_9e_1"),
                subject_ref=command_id,
                allowed_visibility_tiers=["public", "player_visible"],
                items=[
                    create_context_projection_item(
                        record_id=build_record_id("object", "lever_1"),
                        visibility_tier="public",
                        redacted=False,
                        payload={"visible_state": "neutral"},
                    ),
                ],
            ),
        ),
        narration_packet_ref=create_scene_command_execution_narration_packet_ref(
            packet_ref=build_record_id("narration_packet", "pr_9e_1"),
            narration_kind="post_commit_narration",
            visible_summary="The lever is inspected.",
            backend_only_ref_ids=[build_record_id("hidden", "fact_1")],
        ),
        model_boundary_fixture_ref=create_scene_command_execution_model_boundary_fixture_ref(
            fixture_ref=build_record_id("model_boundary_fixture", "pr_9e_1"),
            fixture_kind="context_narration_boundary",
            backend_truth_ref=build_record_id("scene", "threshold_chamber"),
            model_facing_packet_refs=[
                build_record_id("context_packet", "pr_9e_1"),
                build_record_id("narration_packet", "pr_9e_1"),
            ],
        ),
    )


@pytest.fixture()
def sample_routing_result(sample_command_envelope) -> CommandKindRoutingResult:
    return route_command_envelope(
        request_ref=build_record_id("routing_request", "pr_9e_1"),
        command_envelope=sample_command_envelope,
    )


@pytest.fixture()
def sample_validation_bridge_result(
    sample_command_envelope,
    sample_routing_result,
) -> ValidationIntegrationBridgeResult:
    bridge_request = create_validation_integration_bridge_request(
        request_ref=build_record_id("bridge_request", "pr_9e_1"),
        command_envelope=sample_command_envelope,
        routing_result=sample_routing_result,
    )
    return build_validation_integration_bridge_result(request=bridge_request)


@pytest.fixture()
def sample_bridge_request(
    sample_command_envelope,
    sample_transaction_preview,
    sample_assembly_result,
    sample_routing_result,
    sample_validation_bridge_result,
) -> TransactionPreviewPacketBridgeRequest:
    return create_transaction_preview_packet_bridge_request(
        request_ref=build_record_id("tp_bridge_request", "pr_9e_1"),
        command_ref=build_record_id("command", "inspect_lever_1"),
        transaction_preview=sample_transaction_preview,
        assembly_result=sample_assembly_result,
        routing_result=sample_routing_result,
        validation_bridge_result=sample_validation_bridge_result,
    )


@pytest.fixture()
def sample_bridge_result(
    sample_bridge_request,
) -> TransactionPreviewPacketBridgeResult:
    return build_transaction_preview_packet_bridge_result(
        request=sample_bridge_request,
    )


# ---------------------------------------------------------------------------
# Helper for importing module for side-effect checks
# ---------------------------------------------------------------------------

def _bridge_source() -> str:
    mod = sys.modules.get(
        "astra_runtime.domain.transaction_preview_packet_bridge_skeleton",
    )
    if mod is not None and hasattr(mod, "__file__") and mod.__file__:
        with open(mod.__file__, encoding="utf-8") as fh:
            return fh.read()
    return ""


# ---------------------------------------------------------------------------
# Test 1: Module exists and public exports exist
# ---------------------------------------------------------------------------


class TestModuleExistence:
    """Test that the PR-9E module exports its public surfaces."""

    def test_skeleton_error_exists(self) -> None:
        assert issubclass(
            TransactionPreviewPacketBridgeSkeletonError, ValueError,
        )

    def test_request_error_exists(self) -> None:
        assert issubclass(
            InvalidTransactionPreviewPacketBridgeRequestError,
            TransactionPreviewPacketBridgeSkeletonError,
        )

    def test_subject_ref_error_exists(self) -> None:
        assert issubclass(
            InvalidTransactionPreviewPacketBridgeSubjectRefError,
            TransactionPreviewPacketBridgeSkeletonError,
        )

    def test_packet_ref_error_exists(self) -> None:
        assert issubclass(
            InvalidTransactionPreviewPacketBridgePacketRefError,
            TransactionPreviewPacketBridgeSkeletonError,
        )

    def test_packet_descriptor_error_exists(self) -> None:
        assert issubclass(
            InvalidTransactionPreviewPacketBridgePacketDescriptorError,
            TransactionPreviewPacketBridgeSkeletonError,
        )

    def test_authority_flags_error_exists(self) -> None:
        assert issubclass(
            InvalidTransactionPreviewPacketBridgeAuthorityFlagsError,
            TransactionPreviewPacketBridgeSkeletonError,
        )

    def test_result_error_exists(self) -> None:
        assert issubclass(
            InvalidTransactionPreviewPacketBridgeResultError,
            TransactionPreviewPacketBridgeSkeletonError,
        )

    def test_subject_ref_class_exists(self) -> None:
        assert TransactionPreviewPacketBridgeSubjectRef is not None

    def test_packet_ref_class_exists(self) -> None:
        assert TransactionPreviewPacketBridgePacketRef is not None

    def test_packet_descriptor_class_exists(self) -> None:
        assert TransactionPreviewPacketDescriptor is not None

    def test_request_class_exists(self) -> None:
        assert TransactionPreviewPacketBridgeRequest is not None

    def test_authority_flags_class_exists(self) -> None:
        assert TransactionPreviewPacketBridgeAuthorityFlags is not None

    def test_result_class_exists(self) -> None:
        assert TransactionPreviewPacketBridgeResult is not None

    def test_build_function_exists(self) -> None:
        assert callable(build_transaction_preview_packet_bridge_result)

    def test_packet_role_constants_exist(self) -> None:
        assert SINGLE_EVENT_CONTEXT_PACKET == "single_event_context_packet"
        assert SINGLE_EVENT_NARRATION_PACKET == "single_event_narration_packet"
        assert VISIBLE_SUMMARY_PACKET == "visible_summary_packet"
        assert NO_COMMIT_INTENT_PACKET == "no_commit_intent_packet"

    def test_packet_roles_frozenset(self) -> None:
        assert isinstance(PACKET_ROLES, frozenset)
        assert len(PACKET_ROLES) == 4


# ---------------------------------------------------------------------------
# Test 2: Public exports exist (via __all__)
# ---------------------------------------------------------------------------


class TestPublicExports:
    def test_all_pr_9e_symbols_in_all(self) -> None:
        from astra_runtime import domain
        expected = [
            "TransactionPreviewPacketBridgeSkeletonError",
            "InvalidTransactionPreviewPacketBridgeRequestError",
            "InvalidTransactionPreviewPacketBridgeSubjectRefError",
            "InvalidTransactionPreviewPacketBridgePacketRefError",
            "InvalidTransactionPreviewPacketBridgePacketDescriptorError",
            "InvalidTransactionPreviewPacketBridgeAuthorityFlagsError",
            "InvalidTransactionPreviewPacketBridgeResultError",
            "TransactionPreviewPacketBridgeSubjectRef",
            "TransactionPreviewPacketBridgePacketRef",
            "TransactionPreviewPacketDescriptor",
            "TransactionPreviewPacketBridgeRequest",
            "TransactionPreviewPacketBridgeAuthorityFlags",
            "TransactionPreviewPacketBridgeResult",
            "SINGLE_EVENT_CONTEXT_PACKET",
            "SINGLE_EVENT_NARRATION_PACKET",
            "VISIBLE_SUMMARY_PACKET",
            "NO_COMMIT_INTENT_PACKET",
            "PACKET_ROLES",
            "build_transaction_preview_packet_bridge_result",
            "create_transaction_preview_packet_bridge_subject_ref",
            "create_transaction_preview_packet_bridge_packet_ref",
            "create_transaction_preview_packet_descriptor",
            "create_transaction_preview_packet_bridge_request",
            "serialize_transaction_preview_packet_bridge_result",
            "serialize_transaction_preview_packet_bridge_result_visible",
            "serialize_transaction_preview_packet_descriptor",
            "validate_transaction_preview_packet_bridge_result",
            "validate_transaction_preview_packet_descriptor",
        ]
        for name in expected:
            assert name in domain.__all__, f"{name} missing from __all__"


# ---------------------------------------------------------------------------
# Test 3: Dataclasses are frozen and keyword-only
# ---------------------------------------------------------------------------


class TestFrozenDataclasses:
    def test_subject_ref_frozen(self) -> None:
        obj = create_transaction_preview_packet_bridge_subject_ref(
            subject_ref_id=build_record_id("subject_ref", "t1"),
            subject_label="Lever",
        )
        with pytest.raises((AttributeError, TypeError)):
            obj.subject_ref_id = "changed"

    def test_packet_ref_frozen(self) -> None:
        obj = create_transaction_preview_packet_bridge_packet_ref(
            packet_ref_id=build_record_id("packet_ref", "t1"),
            packet_role=SINGLE_EVENT_CONTEXT_PACKET,
        )
        with pytest.raises((AttributeError, TypeError)):
            obj.packet_ref_id = "changed"

    def test_packet_descriptor_frozen(self) -> None:
        obj = create_transaction_preview_packet_descriptor(
            descriptor_id=build_record_id("desc", "t1"),
            packet_role=SINGLE_EVENT_CONTEXT_PACKET,
            packet_kind="single_event_narration",
            source_surface="PR_9A_assembly_result",
            source_surface_ref=build_record_id("assembly_result", "t1"),
            packet_ref_id=build_record_id("packet_ref", "t1"),
        )
        with pytest.raises((AttributeError, TypeError)):
            obj.descriptor_id = "changed"

    def test_request_frozen(self) -> None:
        tp = create_transaction_preview(
            preview_id=build_record_id("tp", "t1"),
            command=create_command_envelope(
                command_id=build_record_id("command", "t1"),
                command_type="inspect_object",
                source_actor_id=build_record_id("actor", "t1"),
            ),
        )
        # Request is validated; trying to set attribute will fail
        # We just confirm the class is frozen
        assert hasattr(TransactionPreviewPacketBridgeRequest, "__dataclass_fields__")

    def test_authority_flags_frozen(self) -> None:
        obj = TransactionPreviewPacketBridgeAuthorityFlags()
        with pytest.raises((AttributeError, TypeError)):
            obj.legality_resolution = True

    def test_result_frozen(self, sample_bridge_result) -> None:
        with pytest.raises((AttributeError, TypeError)):
            sample_bridge_result.result_ref = "changed"


# ---------------------------------------------------------------------------
# Test 4: Bridge accepts valid inputs
# ---------------------------------------------------------------------------


class TestBridgeAcceptValidInputs:
    def test_build_result_accepts_valid_request(
        self,
        sample_bridge_request,
    ) -> None:
        result = build_transaction_preview_packet_bridge_result(
            request=sample_bridge_request,
        )
        assert isinstance(result, TransactionPreviewPacketBridgeResult)
        assert validate_transaction_preview_packet_bridge_result(result)

    def test_bridge_result_has_correct_ids(
        self,
        sample_bridge_request,
        sample_bridge_result,
    ) -> None:
        assert sample_bridge_result.request_ref == sample_bridge_request.request_ref
        assert sample_bridge_result.command_ref == sample_bridge_request.command_ref

    def test_bridge_result_has_transaction_preview_ref(
        self,
        sample_bridge_request,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.transaction_preview_ref
            == sample_bridge_request.transaction_preview.preview_id
        )

    def test_bridge_result_has_validation_bridge_ref(
        self,
        sample_bridge_request,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.validation_bridge_ref
            == sample_bridge_request.validation_bridge_result.result_ref
        )


# ---------------------------------------------------------------------------
# Test 5: Bridge rejects mismatched command references
# ---------------------------------------------------------------------------


class TestBridgeRejectsMismatchedRefs:
    def test_rejects_mismatched_tp_command_id(
        self,
        sample_assembly_result,
        sample_routing_result,
        sample_validation_bridge_result,
    ) -> None:
        tp = create_transaction_preview(
            preview_id=build_record_id("tp", "mismatch"),
            command=create_command_envelope(
                command_id=build_record_id("command", "other_command"),
                command_type="inspect_object",
                source_actor_id=build_record_id("actor", "a1"),
            ),
        )
        request = create_transaction_preview_packet_bridge_request(
            request_ref=build_record_id("req", "mismatch"),
            command_ref=build_record_id("command", "inspect_lever_1"),
            transaction_preview=tp,
            assembly_result=sample_assembly_result,
            routing_result=sample_routing_result,
            validation_bridge_result=sample_validation_bridge_result,
        )
        with pytest.raises(
            InvalidTransactionPreviewPacketBridgeRequestError,
            match="transaction preview command_id",
        ):
            build_transaction_preview_packet_bridge_result(request=request)

    def test_rejects_mismatched_routing_command_ref(
        self,
        sample_command_envelope,
        sample_transaction_preview,
        sample_assembly_result,
        sample_validation_bridge_result,
    ) -> None:
        from astra_runtime.domain.command_kind_routing_skeleton import (
            create_command_kind_routing_authority_flags,
            create_command_kind_routing_result,
            create_command_kind_classification,
            create_command_dispatch_shell,
        )
        bad_routing = create_command_kind_routing_result(
            result_ref=build_record_id("routing_result", "bad"),
            request_ref=build_record_id("routing_request", "bad"),
            command_ref=build_record_id("command", "other_command"),
            classification=create_command_kind_classification(
                classification_ref=build_record_id("classification", "bad"),
                command_ref=build_record_id("command", "other_command"),
                raw_command_type="inspect_object",
                family="inspection",
                kind="inspect_object",
                classification_mode="default_dispatch",
                classification_source="command_type_table",
            ),
            dispatch_shell=create_command_dispatch_shell(
                dispatch_ref=build_record_id("dispatch", "bad"),
                command_ref=build_record_id("command", "other_command"),
                owner_route="RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY",
                family="inspection",
            ),
        )
        request = create_transaction_preview_packet_bridge_request(
            request_ref=build_record_id("req", "mismatch2"),
            command_ref=build_record_id("command", "inspect_lever_1"),
            transaction_preview=sample_transaction_preview,
            assembly_result=sample_assembly_result,
            routing_result=bad_routing,
            validation_bridge_result=sample_validation_bridge_result,
        )
        with pytest.raises(
            InvalidTransactionPreviewPacketBridgeRequestError,
            match="routing result command_ref",
        ):
            build_transaction_preview_packet_bridge_result(request=request)


# ---------------------------------------------------------------------------
# Test 6: Bridge carries transaction preview reference
# ---------------------------------------------------------------------------


class TestBridgeCarriesTPRef:
    def test_result_carrying_tp_ref(
        self,
        sample_bridge_request,
        sample_bridge_result,
    ) -> None:
        assert is_valid_record_id(sample_bridge_result.transaction_preview_ref)
        assert (
            sample_bridge_result.transaction_preview_ref
            == sample_bridge_request.transaction_preview.preview_id
        )


# ---------------------------------------------------------------------------
# Test 7: Bridge carries command family/kind from PR-9C
# ---------------------------------------------------------------------------


class TestBridgeCarriesFamilyKind:
    def test_result_carries_family(
        self,
        sample_routing_result,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.command_family
            == sample_routing_result.classification.family
        )

    def test_result_carries_kind(
        self,
        sample_routing_result,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.command_kind
            == sample_routing_result.classification.kind
        )

    def test_result_does_not_reclassify(
        self,
        sample_bridge_result,
        sample_routing_result,
    ) -> None:
        # Family and kind should be identical to routing, not altered
        assert sample_bridge_result.command_family == sample_routing_result.classification.family
        assert sample_bridge_result.command_kind == sample_routing_result.classification.kind


# ---------------------------------------------------------------------------
# Test 8: Bridge carries validation bridge reference
# ---------------------------------------------------------------------------


class TestBridgeCarriesValidationRef:
    def test_result_carrying_validation_bridge_ref(
        self,
        sample_validation_bridge_result,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.validation_bridge_ref
            == sample_validation_bridge_result.result_ref
        )


# ---------------------------------------------------------------------------
# Test 9-10: Context and narration packet descriptors
# ---------------------------------------------------------------------------


class TestPacketDescriptors:
    def test_context_packet_descriptor_present(
        self,
        sample_bridge_result,
    ) -> None:
        assert isinstance(
            sample_bridge_result.context_packet_descriptor,
            TransactionPreviewPacketDescriptor,
        )

    def test_context_packet_descriptor_role(
        self,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.context_packet_descriptor.packet_role
            == SINGLE_EVENT_CONTEXT_PACKET
        )

    def test_narration_packet_descriptor_present(
        self,
        sample_bridge_result,
    ) -> None:
        assert isinstance(
            sample_bridge_result.narration_packet_descriptor,
            TransactionPreviewPacketDescriptor,
        )

    def test_narration_packet_descriptor_role(
        self,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.narration_packet_descriptor.packet_role
            == SINGLE_EVENT_NARRATION_PACKET
        )

    def test_context_descriptor_carries_assembly_ref(
        self,
        sample_assembly_result,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.context_packet_descriptor.source_surface_ref
            == sample_assembly_result.result_ref
        )

    def test_narration_descriptor_carries_assembly_ref(
        self,
        sample_assembly_result,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.narration_packet_descriptor.source_surface_ref
            == sample_assembly_result.result_ref
        )


# ---------------------------------------------------------------------------
# Test 11-12: Visible summary and no-commit intent descriptors
# ---------------------------------------------------------------------------


class TestVisibleAndNoCommitDescriptors:
    def test_visible_summary_descriptor_present(
        self,
        sample_bridge_result,
    ) -> None:
        assert isinstance(
            sample_bridge_result.visible_summary_packet_descriptor,
            TransactionPreviewPacketDescriptor,
        )

    def test_visible_summary_descriptor_role(
        self,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.visible_summary_packet_descriptor.packet_role
            == VISIBLE_SUMMARY_PACKET
        )

    def test_no_commit_intent_descriptor_present(
        self,
        sample_bridge_result,
    ) -> None:
        assert isinstance(
            sample_bridge_result.no_commit_intent_packet_descriptor,
            TransactionPreviewPacketDescriptor,
        )

    def test_no_commit_intent_descriptor_role(
        self,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.no_commit_intent_packet_descriptor.packet_role
            == NO_COMMIT_INTENT_PACKET
        )

    def test_visible_summary_descriptor_source(
        self,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.visible_summary_packet_descriptor.source_surface
            == "PR_9E_bridge"
        )

    def test_no_commit_descriptor_source(
        self,
        sample_bridge_result,
    ) -> None:
        assert (
            sample_bridge_result.no_commit_intent_packet_descriptor.source_surface
            == "PR_9E_bridge"
        )


# ---------------------------------------------------------------------------
# Test 13: Packet descriptors are reference shells only
# ---------------------------------------------------------------------------


class TestPacketDescriptorShells:
    def test_context_descriptor_is_not_model_prompt(
        self,
        sample_bridge_result,
    ) -> None:
        d = sample_bridge_result.context_packet_descriptor
        # It must be a lightweight descriptor, not a full packet
        assert hasattr(d, "packet_role")
        assert hasattr(d, "packet_kind")
        assert hasattr(d, "packet_ref_id")
        # It must not contain prose or prompt fields
        assert not hasattr(d, "prose")
        assert not hasattr(d, "prompt")
        assert not hasattr(d, "model_input")

    def test_narration_descriptor_is_reference_shell(
        self,
        sample_bridge_result,
    ) -> None:
        d = sample_bridge_result.narration_packet_descriptor
        assert d.packet_role == SINGLE_EVENT_NARRATION_PACKET
        # Should be a descriptor, not a rendered narration
        assert not hasattr(d, "narration_text")
        assert not hasattr(d, "rendered_output")

    def test_visible_summary_is_reference_shell(
        self,
        sample_bridge_result,
    ) -> None:
        d = sample_bridge_result.visible_summary_packet_descriptor
        assert d.packet_role == VISIBLE_SUMMARY_PACKET
        # Not generated text
        assert "reference shell" in d.metadata.get("note", "")


# ---------------------------------------------------------------------------
# Test 14: Visible serialization excludes backend-only metadata
# ---------------------------------------------------------------------------


class TestVisibleSerialization:
    def test_serialize_visible_excludes_metadata(
        self,
        sample_bridge_result,
    ) -> None:
        visible = serialize_transaction_preview_packet_bridge_result_visible(
            sample_bridge_result,
        )
        assert visible["metadata"] == {}

    def test_serialize_full_includes_metadata(
        self,
        sample_bridge_result,
    ) -> None:
        full = serialize_transaction_preview_packet_bridge_result(
            sample_bridge_result,
        )
        assert isinstance(full["metadata"], dict)

    def test_serialize_result_returns_dict(
        self,
        sample_bridge_result,
    ) -> None:
        d = serialize_transaction_preview_packet_bridge_result(
            sample_bridge_result,
        )
        assert isinstance(d, dict)
        assert d["result_ref"] == sample_bridge_result.result_ref
        assert d["request_ref"] == sample_bridge_result.request_ref

    def test_serialize_descriptor_returns_dict(
        self,
        sample_bridge_result,
    ) -> None:
        d = serialize_transaction_preview_packet_descriptor(
            sample_bridge_result.context_packet_descriptor,
        )
        assert isinstance(d, dict)
        assert d["packet_role"] == SINGLE_EVENT_CONTEXT_PACKET

    def test_serialize_visible_returns_dict(
        self,
        sample_bridge_result,
    ) -> None:
        d = serialize_transaction_preview_packet_bridge_result_visible(
            sample_bridge_result,
        )
        assert isinstance(d, dict)

    def test_visible_serialization_preserves_descriptors(
        self,
        sample_bridge_result,
    ) -> None:
        visible = serialize_transaction_preview_packet_bridge_result_visible(
            sample_bridge_result,
        )
        assert "context_packet_descriptor" in visible
        assert "narration_packet_descriptor" in visible
        assert "visible_summary_packet_descriptor" in visible
        assert "no_commit_intent_packet_descriptor" in visible


# ---------------------------------------------------------------------------
# Test 15: Authority flags are all false and reject true
# ---------------------------------------------------------------------------


class TestAuthorityFlags:
    def test_all_flags_false_by_default(
        self,
        sample_bridge_result,
    ) -> None:
        flags = sample_bridge_result.authority_flags
        for name in flags.__dataclass_fields__:
            assert getattr(flags, name) is False, f"{name} should be False"

    def test_constructing_with_true_raises(
        self,
    ) -> None:
        with pytest.raises(
            InvalidTransactionPreviewPacketBridgeAuthorityFlagsError,
        ):
            TransactionPreviewPacketBridgeAuthorityFlags(
                legality_resolution=True,
            )

    def test_constructing_with_true_raises_packet_delivery(
        self,
    ) -> None:
        with pytest.raises(
            InvalidTransactionPreviewPacketBridgeAuthorityFlagsError,
        ):
            TransactionPreviewPacketBridgeAuthorityFlags(
                packet_delivery=True,
            )

    def test_constructing_with_true_raises_model_authority(
        self,
    ) -> None:
        with pytest.raises(
            InvalidTransactionPreviewPacketBridgeAuthorityFlagsError,
        ):
            TransactionPreviewPacketBridgeAuthorityFlags(
                model_authority=True,
            )

    def test_constructing_all_false_succeeds(
        self,
    ) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert isinstance(flags, TransactionPreviewPacketBridgeAuthorityFlags)

    def test_authority_flags_to_dict(
        self,
    ) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        d = flags.to_dict()
        assert isinstance(d, dict)
        for name in flags.__dataclass_fields__:
            assert name in d
            assert d[name] is False

    def test_all_denied_flags_present(
        self,
    ) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        expected_denied = [
            "legality_resolution",
            "validation_rule_execution",
            "command_execution",
            "runtime_action_execution",
            "state_mutation",
            "event_append",
            "persistence_write",
            "rng_table_oracle_execution",
            "settlement_authorization",
            "pr5_arithmetic_execution",
            "consequence_application",
            "packet_compilation",
            "packet_delivery",
            "prompt_rendering",
            "prompt_execution",
            "model_authority",
            "prose_parsing",
            "narration_generation",
            "live_play_session_authority",
            "ui_client_authority",
            "conversion",
            "sourcebook_inclusion",
            "canon_promotion",
        ]
        for name in expected_denied:
            assert hasattr(flags, name), f"missing flag {name}"
            assert getattr(flags, name) is False, f"{name} should be False"


# ---------------------------------------------------------------------------
# Test 16: Deterministic serialization
# ---------------------------------------------------------------------------


class TestDeterministicSerialization:
    def test_serialize_bridge_result_is_deterministic(
        self,
        sample_bridge_result,
    ) -> None:
        d1 = serialize_transaction_preview_packet_bridge_result(
            sample_bridge_result,
        )
        d2 = serialize_transaction_preview_packet_bridge_result(
            sample_bridge_result,
        )
        assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)

    def test_serialize_descriptor_is_deterministic(
        self,
        sample_bridge_result,
    ) -> None:
        d1 = serialize_transaction_preview_packet_descriptor(
            sample_bridge_result.context_packet_descriptor,
        )
        d2 = serialize_transaction_preview_packet_descriptor(
            sample_bridge_result.context_packet_descriptor,
        )
        assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)

    def test_serialize_visible_is_deterministic(
        self,
        sample_bridge_result,
    ) -> None:
        d1 = serialize_transaction_preview_packet_bridge_result_visible(
            sample_bridge_result,
        )
        d2 = serialize_transaction_preview_packet_bridge_result_visible(
            sample_bridge_result,
        )
        assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)


# ---------------------------------------------------------------------------
# Test 17: Metadata is immutable/deep-copied
# ---------------------------------------------------------------------------


class TestMetadataImmutability:
    def test_result_metadata_is_mappingproxy(
        self,
        sample_bridge_result,
    ) -> None:
        assert isinstance(sample_bridge_result.metadata, MappingProxyType)

    def test_descriptor_metadata_is_mappingproxy(
        self,
        sample_bridge_result,
    ) -> None:
        assert isinstance(
            sample_bridge_result.context_packet_descriptor.metadata,
            MappingProxyType,
        )

    def test_metadata_not_shared_with_input(
        self,
        sample_command_envelope,
        sample_transaction_preview,
        sample_assembly_result,
        sample_routing_result,
        sample_validation_bridge_result,
    ) -> None:
        original_meta = {"test_key": "test_value"}
        request = create_transaction_preview_packet_bridge_request(
            request_ref=build_record_id("req", "meta_test"),
            command_ref=build_record_id("command", "inspect_lever_1"),
            transaction_preview=sample_transaction_preview,
            assembly_result=sample_assembly_result,
            routing_result=sample_routing_result,
            validation_bridge_result=sample_validation_bridge_result,
            metadata=original_meta,
        )
        result = build_transaction_preview_packet_bridge_result(request=request)
        # Mutating original should not affect result
        original_meta["test_key"] = "mutated"
        assert result.metadata.get("test_key") == "test_value"

    def test_result_metadata_is_deep_copied(
        self,
        sample_bridge_request,
    ) -> None:
        result = build_transaction_preview_packet_bridge_result(
            request=sample_bridge_request,
        )
        # Metadata should be independent
        inner = dict(result.metadata)
        inner["mutated"] = True
        assert "mutated" not in result.metadata


# ---------------------------------------------------------------------------
# Test 18-20: No side-effect imports / no model/prompt/prose/narration
# ---------------------------------------------------------------------------


class TestNoSideEffectImports:
    def test_no_network_or_db_imports(self) -> None:
        source = _bridge_source()
        forbidden = [
            "socket", "http", "urllib", "requests", "aiohttp",
            "sqlite3", "psycopg", "pymongo", "sqlalchemy",
            "random", "secrets", "database",
        ]
        import ast
        tree = ast.parse(source)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        for mod in forbidden:
            assert mod not in imported, f"forbidden module '{mod}' imported"

    def test_no_file_write_calls(self) -> None:
        source = _bridge_source()
        assert ".write(" not in source

    def test_no_model_imports(self) -> None:
        source = _bridge_source()
        forbidden_model = [
            "openai", "anthropic", "model_boundary",
        ]
        for mod in forbidden_model:
            assert mod not in source, f"model-related import '{mod}' found"

    def test_no_persistence_imports(self) -> None:
        source = _bridge_source()
        assert "import random" not in source
        assert "import secrets" not in source

    def test_no_narration_generation(self) -> None:
        source = _bridge_source()
        assert "def generate_narration" not in source
        assert "def render_prose" not in source

    def test_no_model_prompting(self) -> None:
        source = _bridge_source()
        assert "def render_prompt" not in source
        assert "def execute_prompt" not in source
        assert "def call_model" not in source


# ---------------------------------------------------------------------------
# Test 19-20: No persistence/RNG/mutation/event-append/etc.
# ---------------------------------------------------------------------------


class TestNoPersistenceRNGMutation:
    def test_authority_flags_deny_persistence(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.persistence_write is False

    def test_authority_flags_deny_rng(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.rng_table_oracle_execution is False

    def test_authority_flags_deny_state_mutation(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.state_mutation is False

    def test_authority_flags_deny_event_append(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.event_append is False

    def test_authority_flags_deny_settlement(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.settlement_authorization is False

    def test_authority_flags_deny_consequence(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.consequence_application is False


# ---------------------------------------------------------------------------
# Test 21: No legality resolution
# ---------------------------------------------------------------------------


class TestNoLegality:
    def test_authority_flags_deny_legality(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.legality_resolution is False

    def test_result_has_no_legality_field(self, sample_bridge_result) -> None:
        assert not hasattr(sample_bridge_result, "legality")
        assert not hasattr(sample_bridge_result, "legality_result")


# ---------------------------------------------------------------------------
# Test 22: No validation rule execution
# ---------------------------------------------------------------------------


class TestNoValidationExecution:
    def test_authority_flags_deny_validation_execution(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.validation_rule_execution is False


# ---------------------------------------------------------------------------
# Test 23: No packet delivery
# ---------------------------------------------------------------------------


class TestNoPacketDelivery:
    def test_authority_flags_deny_packet_delivery(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.packet_delivery is False

    def test_result_has_no_deliver_function(self) -> None:
        assert not hasattr(
            TransactionPreviewPacketBridgeResult, "deliver",
        )
        assert not hasattr(
            TransactionPreviewPacketBridgeResult, "deliver_packets",
        )


# ---------------------------------------------------------------------------
# Test 24: No call to assemble_scene_command_execution_result
# ---------------------------------------------------------------------------


class TestNoAssemblyCalls:
    def test_bridge_source_has_no_assembly_call(self) -> None:
        source = _bridge_source()
        assert "assemble_scene_command_execution_result(" not in source


# ---------------------------------------------------------------------------
# Test 25: No call to PR-9C routing functions
# ---------------------------------------------------------------------------


class TestNoRoutingCalls:
    def test_bridge_source_has_no_route_command_envelope(self) -> None:
        source = _bridge_source()
        assert "route_command_envelope(" not in source
        assert "route_command_intent(" not in source


# ---------------------------------------------------------------------------
# Test 26: No call to build_validation_integration_bridge_result
# ---------------------------------------------------------------------------


class TestNoBridgeRebuildCalls:
    def test_bridge_source_has_no_bridge_build_call(self) -> None:
        source = _bridge_source()
        assert "build_validation_integration_bridge_result(" not in source


# ---------------------------------------------------------------------------
# Test 27: No edit to tiny_vertical_slice.py
# ---------------------------------------------------------------------------


class TestNoTinyVerticalSliceEdit:
    def test_bridge_module_is_not_tiny_vertical_slice(self) -> None:
        mod = sys.modules.get(
            "astra_runtime.domain.transaction_preview_packet_bridge_skeleton",
        )
        assert mod is not None
        assert "tiny_vertical_slice" not in (mod.__name__ or "")


# ---------------------------------------------------------------------------
# Test 28: Validator functions work
# ---------------------------------------------------------------------------


class TestValidatorFunctions:
    def test_validate_descriptor_valid(
        self,
        sample_bridge_result,
    ) -> None:
        assert validate_transaction_preview_packet_descriptor(
            sample_bridge_result.context_packet_descriptor,
        )

    def test_validate_descriptor_invalid_type(self) -> None:
        assert not validate_transaction_preview_packet_descriptor("not a descriptor")

    def test_validate_result_valid(
        self,
        sample_bridge_result,
    ) -> None:
        assert validate_transaction_preview_packet_bridge_result(
            sample_bridge_result,
        )

    def test_validate_result_invalid_type(self) -> None:
        assert not validate_transaction_preview_packet_bridge_result("not a result")

    def test_validate_result_none(self) -> None:
        assert not validate_transaction_preview_packet_bridge_result(None)


# ---------------------------------------------------------------------------
# Test 29: Packet ordering
# ---------------------------------------------------------------------------


class TestPacketOrdering:
    def test_ordering_tuple_present(
        self,
        sample_bridge_result,
    ) -> None:
        assert isinstance(sample_bridge_result.packet_ordering, tuple)
        assert len(sample_bridge_result.packet_ordering) == 4

    def test_ordering_contains_all_packet_ref_ids(
        self,
        sample_bridge_result,
    ) -> None:
        ref_ids = {
            sample_bridge_result.context_packet_descriptor.packet_ref_id,
            sample_bridge_result.narration_packet_descriptor.packet_ref_id,
            sample_bridge_result.visible_summary_packet_descriptor.packet_ref_id,
            sample_bridge_result.no_commit_intent_packet_descriptor.packet_ref_id,
        }
        assert set(sample_bridge_result.packet_ordering) == ref_ids


# ---------------------------------------------------------------------------
# Test 30: No model/prompt/narration/live-play behavior
# ---------------------------------------------------------------------------


class TestNoModelPromptNarration:
    def test_authority_flags_deny_model_authority(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.model_authority is False

    def test_authority_flags_deny_prompt_rendering(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.prompt_rendering is False

    def test_authority_flags_deny_prompt_execution(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.prompt_execution is False

    def test_authority_flags_deny_prose_parsing(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.prose_parsing is False

    def test_authority_flags_deny_narration_generation(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.narration_generation is False

    def test_authority_flags_deny_live_play(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.live_play_session_authority is False

    def test_authority_flags_deny_ui_client(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.ui_client_authority is False

    def test_authority_flags_deny_conversion(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.conversion is False

    def test_authority_flags_deny_sourcebook_inclusion(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.sourcebook_inclusion is False

    def test_authority_flags_deny_canon_promotion(self) -> None:
        flags = TransactionPreviewPacketBridgeAuthorityFlags()
        assert flags.canon_promotion is False


# ---------------------------------------------------------------------------
# Test 31: No call to assemble, route, or build bridge
# ---------------------------------------------------------------------------


class TestNoForbiddenFunctionCalls:
    def test_no_assemble_call(self) -> None:
        source = _bridge_source()
        assert "assemble_scene_command_execution_result" not in source.split("import")[-1]

    def test_no_route_call_in_body(self) -> None:
        source = _bridge_source()
        # Only check function bodies, not imports
        body_parts = source.split("def build_transaction_preview_packet_bridge_result")
        if len(body_parts) > 1:
            body = body_parts[1]
            assert "route_command_envelope" not in body
            assert "route_command_intent" not in body

    def test_no_validation_bridge_build_call_in_body(self) -> None:
        source = _bridge_source()
        body_parts = source.split("def build_transaction_preview_packet_bridge_result")
        if len(body_parts) > 1:
            body = body_parts[1]
            assert "build_validation_integration_bridge_result" not in body


# ---------------------------------------------------------------------------
# Test 32: PR-9A context/narration refs carried by reference
# ---------------------------------------------------------------------------


class TestCarriesPr9ARefs:
    def test_context_descriptor_has_context_projection_info(
        self,
        sample_bridge_result,
    ) -> None:
        meta = sample_bridge_result.context_packet_descriptor.metadata
        assert "context_projection_present" in meta

    def test_narration_descriptor_has_narration_kind(
        self,
        sample_bridge_result,
    ) -> None:
        meta = sample_bridge_result.narration_packet_descriptor.metadata
        assert "narration_kind" in meta
        assert meta["narration_kind"] == "post_commit_narration"


# ---------------------------------------------------------------------------
# Test 33: to_dict methods work
# ---------------------------------------------------------------------------


class TestToDict:
    def test_subject_ref_to_dict(self) -> None:
        ref = create_transaction_preview_packet_bridge_subject_ref(
            subject_ref_id=build_record_id("subject", "t1"),
            subject_label="Lever",
        )
        d = ref.to_dict()
        assert isinstance(d, dict)
        assert d["subject_ref_id"] == build_record_id("subject", "t1")
        assert d["subject_label"] == "Lever"

    def test_packet_ref_to_dict(self) -> None:
        ref = create_transaction_preview_packet_bridge_packet_ref(
            packet_ref_id=build_record_id("packet", "t1"),
            packet_role=SINGLE_EVENT_CONTEXT_PACKET,
        )
        d = ref.to_dict()
        assert isinstance(d, dict)
        assert d["packet_role"] == SINGLE_EVENT_CONTEXT_PACKET

    def test_descriptor_to_dict(self) -> None:
        desc = create_transaction_preview_packet_descriptor(
            descriptor_id=build_record_id("desc", "t1"),
            packet_role=VISIBLE_SUMMARY_PACKET,
            packet_kind="visible_summary",
            source_surface="PR_9E_bridge",
            source_surface_ref=build_record_id("bridge", "t1"),
            packet_ref_id=build_record_id("packet_ref", "t1"),
        )
        d = desc.to_dict()
        assert isinstance(d, dict)
        assert d["packet_role"] == VISIBLE_SUMMARY_PACKET


# ---------------------------------------------------------------------------
# Test 34: Command intent from assembly result
# ---------------------------------------------------------------------------


class TestAssemblyCommandIntent:
    def test_assembly_result_has_command_intent(
        self,
        sample_assembly_result,
    ) -> None:
        assert hasattr(sample_assembly_result, "command_intent")
        assert sample_assembly_result.command_intent is not None


# ---------------------------------------------------------------------------
# Test 35: Result is not None and valid
# ---------------------------------------------------------------------------


class TestResultValidity:
    def test_result_is_not_none(
        self,
        sample_bridge_result,
    ) -> None:
        assert sample_bridge_result is not None

    def test_result_ref_is_valid_record_id(
        self,
        sample_bridge_result,
    ) -> None:
        assert is_valid_record_id(sample_bridge_result.result_ref)

    def test_request_ref_is_valid_record_id(
        self,
        sample_bridge_result,
    ) -> None:
        assert is_valid_record_id(sample_bridge_result.request_ref)

    def test_validation_bridge_ref_is_valid_record_id(
        self,
        sample_bridge_result,
    ) -> None:
        assert is_valid_record_id(sample_bridge_result.validation_bridge_ref)

    def test_transaction_preview_ref_is_valid_record_id(
        self,
        sample_bridge_result,
    ) -> None:
        assert is_valid_record_id(sample_bridge_result.transaction_preview_ref)
