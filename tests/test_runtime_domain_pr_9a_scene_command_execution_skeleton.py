"""PR-9A — scene command execution skeleton (backend-owned typed assembly) tests."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from types import MappingProxyType

import pytest

from astra_runtime.domain import (
    InvalidSceneCommandExecutionActorContractError,
    InvalidSceneCommandExecutionAssemblyRequestError,
    InvalidSceneCommandExecutionAssemblyResultError,
    InvalidSceneCommandExecutionCommandIntentError,
    InvalidSceneCommandExecutionContextPacketRefError,
    InvalidSceneCommandExecutionEventLedgerCandidateRefError,
    InvalidSceneCommandExecutionHiddenInfoContractError,
    InvalidSceneCommandExecutionModelBoundaryFixtureRefError,
    InvalidSceneCommandExecutionNarrationPacketRefError,
    InvalidSceneCommandExecutionObjectContractError,
    InvalidSceneCommandExecutionResourcePreviewRefError,
    InvalidSceneCommandExecutionSceneContractError,
    InvalidSceneCommandExecutionStateDeltaCandidateRefError,
    InvalidSceneCommandExecutionSubjectRefError,
    InvalidSceneCommandExecutionValidationRefError,
    SceneCommandExecutionActorContract,
    SceneCommandExecutionAssemblyAuthorityFlags,
    SceneCommandExecutionAssemblyRequest,
    SceneCommandExecutionAssemblyResult,
    SceneCommandExecutionCommandIntent,
    SceneCommandExecutionContextPacketRef,
    SceneCommandExecutionEventLedgerCandidateRef,
    SceneCommandExecutionHiddenInfoContract,
    SceneCommandExecutionModelBoundaryFixtureRef,
    SceneCommandExecutionNarrationPacketRef,
    SceneCommandExecutionObjectContract,
    SceneCommandExecutionResourcePreviewRef,
    SceneCommandExecutionSceneContract,
    SceneCommandExecutionSkeletonError,
    SceneCommandExecutionStateDeltaCandidateRef,
    SceneCommandExecutionSubjectRef,
    SceneCommandExecutionValidationRef,
    assemble_scene_command_execution_result,
    create_scene_command_execution_actor_contract,
    create_scene_command_execution_assembly_authority_flags,
    create_scene_command_execution_assembly_request,
    create_scene_command_execution_command_intent,
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
    serialize_scene_command_execution_assembly_result_backend,
    serialize_scene_command_execution_assembly_result_visible,
    validate_scene_command_execution_actor_contract,
    validate_scene_command_execution_assembly_request,
    validate_scene_command_execution_assembly_result,
    validate_scene_command_execution_command_intent,
    validate_scene_command_execution_context_packet_ref,
    validate_scene_command_execution_event_ledger_candidate_ref,
    validate_scene_command_execution_hidden_info_contract,
    validate_scene_command_execution_model_boundary_fixture_ref,
    validate_scene_command_execution_narration_packet_ref,
    validate_scene_command_execution_object_contract,
    validate_scene_command_execution_resource_preview_ref,
    validate_scene_command_execution_scene_contract,
    validate_scene_command_execution_state_delta_candidate_ref,
    validate_scene_command_execution_subject_ref,
    validate_scene_command_execution_validation_ref,
)
from astra_runtime.domain.resource_consequence_math import (
    ResourceMathRequest,
    ResourceMathResult,
    create_resource_math_request,
    create_resource_math_result,
    create_resource_math_subject_reference,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
)
from astra_runtime.kernel.context_projection import (
    ContextProjection,
    create_context_projection,
    create_context_projection_item,
)
from astra_runtime.kernel.event_ledger import (
    EventLedgerEntry,
    create_event_ledger_entry,
)
from astra_runtime.kernel.persistence_boundary import (
    PersistenceBoundaryRequest,
    create_persistence_boundary_request,
)
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.state_delta import (
    StateDeltaEnvelope,
    create_state_delta_envelope,
)
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    create_transaction_preview,
)
from astra_runtime.kernel.validation_pipeline import (
    ValidationResult,
    create_validation_result,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_command_envelope() -> CommandEnvelope:
    return create_command_envelope(
        command_id=build_record_id("command", "inspect_lever_1"),
        command_type="inspect_object",
        source_actor_id=build_record_id("actor", "ascendant_1"),
        payload={"target_object_ref": build_record_id("object", "lever_1")},
        metadata={"scene_ref": build_record_id("scene", "threshold_chamber")},
    )


@pytest.fixture()
def sample_scene_contract() -> SceneCommandExecutionSceneContract:
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
                visible_condition_refs=[build_record_id("condition", "burned_palm")],
            ),
            create_scene_command_execution_actor_contract(
                actor_ref=build_record_id("actor", "npc_1"),
                actor_label="Watchful Adept",
                visible_description="A watchful NPC.",
            ),
        ],
        objects=[
            create_scene_command_execution_object_contract(
                object_ref=build_record_id("object", "lever_1"),
                object_label="Brass Lever",
                visible_description="A tarnished brass lever.",
                visible_state="neutral",
            ),
            create_scene_command_execution_object_contract(
                object_ref=build_record_id("object", "door_1"),
                object_label="Stone Door",
                visible_description="A heavy stone door.",
                visible_state="sealed",
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
def sample_assembly_request(sample_scene_contract, sample_command_envelope) -> SceneCommandExecutionAssemblyRequest:
    return create_scene_command_execution_assembly_request(
        request_ref=build_record_id("request", "pr_9a_1"),
        scene_contract=sample_scene_contract,
        command_envelope=sample_command_envelope,
        intent_target_ref=build_record_id("object", "lever_1"),
    )


@pytest.fixture()
def sample_transaction_preview(sample_command_envelope) -> TransactionPreview:
    return create_transaction_preview(
        preview_id=build_record_id("transaction_preview", "pr_9a_1"),
        command=sample_command_envelope,
        status="preview_created",
    )


@pytest.fixture()
def sample_validation_ref() -> SceneCommandExecutionValidationRef:
    return create_scene_command_execution_validation_ref(
        validation_ref=build_record_id("validation", "pr_9a_1"),
        validation_result=create_validation_result(
            validation_id=build_record_id("validation", "pr_9a_1"),
            subject_ref=build_record_id("command", "inspect_lever_1"),
            passed=True,
        ),
    )


@pytest.fixture()
def sample_resource_preview_ref() -> SceneCommandExecutionResourcePreviewRef:
    rm_request_id = build_record_id("resource_math_request", "pr_9a_1")
    trace_ref_id = build_record_id("trace", "pr_9a_1")
    subject_ref = create_resource_math_subject_reference(
        subject_binding_id=build_record_id("subject_binding", "ascendant_1"),
        subject_type="actor",
        subject_ref_id=build_record_id("actor", "ascendant_1"),
        subject_role="primary_subject",
        owner_domain="RT001_command_lifecycle_action_legality",
    )
    return create_scene_command_execution_resource_preview_ref(
        preview_ref=build_record_id("resource_preview", "pr_9a_1"),
        resource_math_request=create_resource_math_request(
            request_id=rm_request_id,
            trace_ref_id=trace_ref_id,
            command_ref_id=build_record_id("command", "inspect_lever_1"),
            subject_refs=[subject_ref],
        ),
        resource_math_result=create_resource_math_result(
            result_id=build_record_id("resource_math_result", "pr_9a_1"),
            request_id=rm_request_id,
            stage="resource_math_requested",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id=trace_ref_id,
            referenced_subject_binding_ids=[subject_ref.subject_binding_id],
        ),
    )


@pytest.fixture()
def sample_state_delta_candidate_ref() -> SceneCommandExecutionStateDeltaCandidateRef:
    return create_scene_command_execution_state_delta_candidate_ref(
        delta_ref=build_record_id("state_delta_candidate", "pr_9a_1"),
        delta_envelope=create_state_delta_envelope(
            delta_id=build_record_id("state_delta", "env_1"),
            source_command_id=build_record_id("command", "inspect_lever_1"),
            source_preview_id=build_record_id("transaction_preview", "pr_9a_1"),
            affected_record_ids=[build_record_id("object", "lever_1")],
            change_type="record_update",
            payload={"visible_state": "inspected"},
        ),
    )


@pytest.fixture()
def sample_event_ledger_candidate_ref() -> SceneCommandExecutionEventLedgerCandidateRef:
    return create_scene_command_execution_event_ledger_candidate_ref(
        event_ref=build_record_id("event_ledger_candidate", "pr_9a_1"),
        ledger_entry=create_event_ledger_entry(
            event_id=build_record_id("event", "env_1"),
            sequence=0,
            source_command_id=build_record_id("command", "inspect_lever_1"),
            source_preview_id=build_record_id("transaction_preview", "pr_9a_1"),
            event_type="command_event",
        ),
    )


@pytest.fixture()
def sample_context_packet_ref() -> SceneCommandExecutionContextPacketRef:
    return create_scene_command_execution_context_packet_ref(
        packet_ref=build_record_id("context_packet", "pr_9a_1"),
        context_projection=create_context_projection(
            projection_id=build_record_id("context_projection", "pr_9a_1"),
            subject_ref=build_record_id("command", "inspect_lever_1"),
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
    )


@pytest.fixture()
def sample_narration_packet_ref() -> SceneCommandExecutionNarrationPacketRef:
    return create_scene_command_execution_narration_packet_ref(
        packet_ref=build_record_id("narration_packet", "pr_9a_1"),
        narration_kind="post_commit_narration",
        visible_summary="The lever is inspected.",
        backend_only_ref_ids=[build_record_id("hidden", "fact_1")],
    )


@pytest.fixture()
def sample_model_boundary_fixture_ref() -> SceneCommandExecutionModelBoundaryFixtureRef:
    return create_scene_command_execution_model_boundary_fixture_ref(
        fixture_ref=build_record_id("model_boundary_fixture", "pr_9a_1"),
        fixture_kind="context_narration_boundary",
        backend_truth_ref=build_record_id("scene", "threshold_chamber"),
        model_facing_packet_refs=[
            build_record_id("context_packet", "pr_9a_1"),
            build_record_id("narration_packet", "pr_9a_1"),
        ],
    )


@pytest.fixture()
def sample_assembly_result(
    sample_assembly_request,
    sample_transaction_preview,
    sample_validation_ref,
    sample_resource_preview_ref,
    sample_state_delta_candidate_ref,
    sample_event_ledger_candidate_ref,
    sample_context_packet_ref,
    sample_narration_packet_ref,
    sample_model_boundary_fixture_ref,
) -> SceneCommandExecutionAssemblyResult:
    result_ref = build_record_id("assembly_result", "pr_9a_1")
    return assemble_scene_command_execution_result(
        result_ref=result_ref,
        request=sample_assembly_request,
        transaction_preview=sample_transaction_preview,
        validation_ref=sample_validation_ref,
        resource_preview_ref=sample_resource_preview_ref,
        state_delta_candidate_ref=sample_state_delta_candidate_ref,
        event_ledger_candidate_ref=sample_event_ledger_candidate_ref,
        context_packet_ref=sample_context_packet_ref,
        narration_packet_ref=sample_narration_packet_ref,
        model_boundary_fixture_ref=sample_model_boundary_fixture_ref,
        persistence_prepare_ref=create_persistence_boundary_request(
            request_id=build_record_id("persistence_prepare", "pr_9a_1"),
            operation_type="record_snapshot_prepare",
            subject_ref=result_ref,
        ),
    )


# ---------------------------------------------------------------------------
# Module and exports
# ---------------------------------------------------------------------------


class TestExports:
    def test_all_pr_9a_symbols_exported(self):
        from astra_runtime import domain
        expected = [
            "SceneCommandExecutionSkeletonError",
            "SceneCommandExecutionSubjectRef",
            "SceneCommandExecutionSceneContract",
            "SceneCommandExecutionActorContract",
            "SceneCommandExecutionObjectContract",
            "SceneCommandExecutionHiddenInfoContract",
            "SceneCommandExecutionCommandIntent",
            "SceneCommandExecutionValidationRef",
            "SceneCommandExecutionResourcePreviewRef",
            "SceneCommandExecutionStateDeltaCandidateRef",
            "SceneCommandExecutionEventLedgerCandidateRef",
            "SceneCommandExecutionContextPacketRef",
            "SceneCommandExecutionNarrationPacketRef",
            "SceneCommandExecutionModelBoundaryFixtureRef",
            "SceneCommandExecutionAssemblyRequest",
            "SceneCommandExecutionAssemblyResult",
            "SceneCommandExecutionAssemblyAuthorityFlags",
            "assemble_scene_command_execution_result",
            "create_scene_command_execution_scene_contract",
            "create_scene_command_execution_command_intent_from_envelope",
            "serialize_scene_command_execution_assembly_result_visible",
            "serialize_scene_command_execution_assembly_result_backend",
        ]
        for name in expected:
            assert hasattr(domain, name), f"Missing export: {name}"
            assert name in domain.__all__, f"Missing from __all__: {name}"


class TestModule:
    def test_module_file_exists(self):
        path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "scene_command_execution_skeleton.py"
        assert path.exists(), f"Module missing: {path}"


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------


class TestErrorHierarchy:
    def test_base_error_is_value_error(self):
        assert issubclass(SceneCommandExecutionSkeletonError, ValueError)

    def test_base_error_raises(self):
        with pytest.raises(SceneCommandExecutionSkeletonError):
            raise SceneCommandExecutionSkeletonError("test")

    def test_all_invalid_errors_derive_from_base(self):
        errors = [
            InvalidSceneCommandExecutionSubjectRefError,
            InvalidSceneCommandExecutionSceneContractError,
            InvalidSceneCommandExecutionActorContractError,
            InvalidSceneCommandExecutionObjectContractError,
            InvalidSceneCommandExecutionHiddenInfoContractError,
            InvalidSceneCommandExecutionCommandIntentError,
            InvalidSceneCommandExecutionValidationRefError,
            InvalidSceneCommandExecutionResourcePreviewRefError,
            InvalidSceneCommandExecutionStateDeltaCandidateRefError,
            InvalidSceneCommandExecutionEventLedgerCandidateRefError,
            InvalidSceneCommandExecutionContextPacketRefError,
            InvalidSceneCommandExecutionNarrationPacketRefError,
            InvalidSceneCommandExecutionModelBoundaryFixtureRefError,
            InvalidSceneCommandExecutionAssemblyRequestError,
            InvalidSceneCommandExecutionAssemblyResultError,
        ]
        for err in errors:
            assert issubclass(err, SceneCommandExecutionSkeletonError), err


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------


class TestFrozenDataclasses:
    @pytest.mark.parametrize(
        "cls",
        [
            SceneCommandExecutionSubjectRef,
            SceneCommandExecutionActorContract,
            SceneCommandExecutionObjectContract,
            SceneCommandExecutionHiddenInfoContract,
            SceneCommandExecutionSceneContract,
            SceneCommandExecutionCommandIntent,
            SceneCommandExecutionValidationRef,
            SceneCommandExecutionResourcePreviewRef,
            SceneCommandExecutionStateDeltaCandidateRef,
            SceneCommandExecutionEventLedgerCandidateRef,
            SceneCommandExecutionContextPacketRef,
            SceneCommandExecutionNarrationPacketRef,
            SceneCommandExecutionModelBoundaryFixtureRef,
            SceneCommandExecutionAssemblyAuthorityFlags,
            SceneCommandExecutionAssemblyRequest,
            SceneCommandExecutionAssemblyResult,
        ],
    )
    def test_dataclass_is_frozen(self, cls):
        assert cls.__dataclass_params__.frozen is True

    def test_frozen_modification_raises(self, sample_scene_contract):
        with pytest.raises(AttributeError):
            sample_scene_contract.scene_label = "changed"


# ---------------------------------------------------------------------------
# Factory / validator parity
# ---------------------------------------------------------------------------


class TestFactoryValidatorParity:
    @pytest.mark.parametrize(
        "factory, validator, valid_obj",
        [
            (
                create_scene_command_execution_subject_ref,
                validate_scene_command_execution_subject_ref,
                {"subject_type": "actor", "ref_id": build_record_id("actor", "parity_1")},
            ),
            (
                create_scene_command_execution_actor_contract,
                validate_scene_command_execution_actor_contract,
                {"actor_ref": build_record_id("actor", "parity_1"), "actor_label": "A", "visible_description": "desc"},
            ),
            (
                create_scene_command_execution_object_contract,
                validate_scene_command_execution_object_contract,
                {"object_ref": build_record_id("object", "parity_1"), "object_label": "O", "visible_description": "desc", "visible_state": "s"},
            ),
            (
                create_scene_command_execution_hidden_info_contract,
                validate_scene_command_execution_hidden_info_contract,
                {"hidden_ref": build_record_id("hidden", "parity_1"), "hidden_label": "H", "backend_only_description": "bd", "reveal_condition": "rc"},
            ),
            (
                create_scene_command_execution_scene_contract,
                validate_scene_command_execution_scene_contract,
                {"scene_ref": build_record_id("scene", "parity_1"), "scene_label": "S", "visible_description": "desc"},
            ),
            (
                create_scene_command_execution_command_intent,
                validate_scene_command_execution_command_intent,
                {"intent_ref": build_record_id("intent", "parity_1"), "command_envelope_id": build_record_id("command", "parity_1"), "command_type": "t", "source_actor_ref": build_record_id("actor", "parity_1")},
            ),
            (
                create_scene_command_execution_validation_ref,
                validate_scene_command_execution_validation_ref,
                {"validation_ref": build_record_id("validation", "parity_1")},
            ),
            (
                create_scene_command_execution_resource_preview_ref,
                validate_scene_command_execution_resource_preview_ref,
                {"preview_ref": build_record_id("resource_preview", "parity_1")},
            ),
            (
                create_scene_command_execution_state_delta_candidate_ref,
                validate_scene_command_execution_state_delta_candidate_ref,
                {"delta_ref": build_record_id("state_delta", "parity_1")},
            ),
            (
                create_scene_command_execution_event_ledger_candidate_ref,
                validate_scene_command_execution_event_ledger_candidate_ref,
                {"event_ref": build_record_id("event", "parity_1")},
            ),
            (
                create_scene_command_execution_context_packet_ref,
                validate_scene_command_execution_context_packet_ref,
                {"packet_ref": build_record_id("context_packet", "parity_1")},
            ),
            (
                create_scene_command_execution_narration_packet_ref,
                validate_scene_command_execution_narration_packet_ref,
                {"packet_ref": build_record_id("narration_packet", "parity_1")},
            ),
            (
                create_scene_command_execution_model_boundary_fixture_ref,
                validate_scene_command_execution_model_boundary_fixture_ref,
                {"fixture_ref": build_record_id("model_boundary_fixture", "parity_1")},
            ),
        ],
    )
    def test_factory_output_passes_validator(self, factory, validator, valid_obj):
        obj = factory(**valid_obj)
        assert validator(obj) is True

    def test_validator_rejects_non_object(self):
        assert validate_scene_command_execution_subject_ref("not-a-ref") is False


# ---------------------------------------------------------------------------
# Command envelope consumption
# ---------------------------------------------------------------------------


class TestCommandEnvelopeConsumption:
    def test_command_intent_derived_from_envelope(self, sample_command_envelope):
        intent = create_scene_command_execution_command_intent_from_envelope(
            intent_ref=build_record_id("intent", "envelope_1"),
            command_envelope=sample_command_envelope,
            target_ref=build_record_id("object", "lever_1"),
        )
        assert isinstance(intent, SceneCommandExecutionCommandIntent)
        assert intent.command_envelope_id == sample_command_envelope.command_id
        assert intent.command_type == sample_command_envelope.command_type
        assert intent.source_actor_ref == sample_command_envelope.source_actor_id
        assert intent.target_ref == build_record_id("object", "lever_1")

    def test_invalid_envelope_rejected(self):
        with pytest.raises(SceneCommandExecutionSkeletonError):
            create_scene_command_execution_command_intent_from_envelope(
                intent_ref=build_record_id("intent", "invalid_envelope_1"),
                command_envelope="not-an-envelope",  # type: ignore[arg-type]
            )

    def test_assembly_result_command_id_matches_transaction_preview(self, sample_assembly_result):
        assert (
            sample_assembly_result.command_intent.command_envelope_id
            == sample_assembly_result.transaction_preview.command_id
        )


# ---------------------------------------------------------------------------
# Scene contract generalization
# ---------------------------------------------------------------------------


class TestSceneContractGeneralization:
    def test_scene_contract_supports_multiple_actors_objects_hidden(self, sample_scene_contract):
        assert len(sample_scene_contract.actors) == 2
        assert len(sample_scene_contract.objects) == 2
        assert len(sample_scene_contract.hidden_info) == 1
        assert isinstance(sample_scene_contract.actors[0], SceneCommandExecutionActorContract)
        assert isinstance(sample_scene_contract.objects[0], SceneCommandExecutionObjectContract)
        assert isinstance(sample_scene_contract.hidden_info[0], SceneCommandExecutionHiddenInfoContract)

    def test_empty_actors_objects_hidden_are_valid(self):
        scene = create_scene_command_execution_scene_contract(
            scene_ref=build_record_id("scene", "empty_1"),
            scene_label="Empty Scene",
            visible_description="An empty scene.",
        )
        assert validate_scene_command_execution_scene_contract(scene) is True
        assert scene.actors == ()
        assert scene.objects == ()
        assert scene.hidden_info == ()


# ---------------------------------------------------------------------------
# Transaction assembly result surfaces
# ---------------------------------------------------------------------------


class TestTransactionAssemblyResult:
    def test_result_includes_all_required_surfaces(self, sample_assembly_result):
        assert isinstance(sample_assembly_result.validation_ref, SceneCommandExecutionValidationRef)
        assert isinstance(sample_assembly_result.resource_preview_ref, SceneCommandExecutionResourcePreviewRef)
        assert isinstance(sample_assembly_result.state_delta_candidate_ref, SceneCommandExecutionStateDeltaCandidateRef)
        assert isinstance(sample_assembly_result.event_ledger_candidate_ref, SceneCommandExecutionEventLedgerCandidateRef)
        assert isinstance(sample_assembly_result.context_packet_ref, SceneCommandExecutionContextPacketRef)
        assert isinstance(sample_assembly_result.narration_packet_ref, SceneCommandExecutionNarrationPacketRef)
        assert isinstance(sample_assembly_result.model_boundary_fixture_ref, SceneCommandExecutionModelBoundaryFixtureRef)

    def test_result_uses_existing_kernel_types(self, sample_assembly_result):
        assert isinstance(sample_assembly_result.transaction_preview, TransactionPreview)
        assert isinstance(sample_assembly_result.state_delta_candidate_ref.delta_envelope, StateDeltaEnvelope)
        assert isinstance(sample_assembly_result.event_ledger_candidate_ref.ledger_entry, EventLedgerEntry)
        assert isinstance(sample_assembly_result.context_packet_ref.context_projection, ContextProjection)

    def test_result_rejects_mismatched_command_id(self, sample_assembly_request):
        other_command = create_command_envelope(
            command_id=build_record_id("command", "other_1"),
            command_type="inspect_object",
            source_actor_id=build_record_id("actor", "ascendant_1"),
        )
        other_preview = create_transaction_preview(
            preview_id=build_record_id("transaction_preview", "other_1"),
            command=other_command,
            status="preview_created",
        )
        refs = _minimal_refs_for_assembly()
        with pytest.raises(SceneCommandExecutionSkeletonError, match="transaction_preview.command_id"):
            assemble_scene_command_execution_result(
                result_ref=build_record_id("assembly_result", "mismatch_1"),
                request=sample_assembly_request,
                transaction_preview=other_preview,
                **refs,
            )

    def test_assembly_request_validates_command_envelope(self, sample_scene_contract):
        with pytest.raises(SceneCommandExecutionSkeletonError):
            create_scene_command_execution_assembly_request(
                request_ref=build_record_id("request", "invalid_envelope_1"),
                scene_contract=sample_scene_contract,
                command_envelope="not-an-envelope",  # type: ignore[arg-type]
            )


# ---------------------------------------------------------------------------
# Deterministic serialization
# ---------------------------------------------------------------------------


class TestDeterministicSerialization:
    def test_visible_serialization_deterministic(self, sample_assembly_result):
        first = serialize_scene_command_execution_assembly_result_visible(sample_assembly_result)
        second = serialize_scene_command_execution_assembly_result_visible(sample_assembly_result)
        assert first == second
        assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)

    def test_backend_serialization_deterministic(self, sample_assembly_result):
        first = serialize_scene_command_execution_assembly_result_backend(sample_assembly_result)
        second = serialize_scene_command_execution_assembly_result_backend(sample_assembly_result)
        assert first == second

    def test_visible_serialization_omits_hidden_payloads(self, sample_assembly_result):
        visible = serialize_scene_command_execution_assembly_result_visible(sample_assembly_result)
        assert "backend_only_description" not in str(visible)


# ---------------------------------------------------------------------------
# Input immutability
# ---------------------------------------------------------------------------


class TestInputImmutability:
    def test_scene_contract_not_mutated_by_assembly(self, sample_assembly_request, sample_transaction_preview):
        original = sample_assembly_request.scene_contract.to_dict()
        refs = _minimal_refs_for_assembly()
        assemble_scene_command_execution_result(
            result_ref=build_record_id("assembly_result", "immutable_1"),
            request=sample_assembly_request,
            transaction_preview=sample_transaction_preview,
            **refs,
        )
        assert sample_assembly_request.scene_contract.to_dict() == original

    def test_command_envelope_payload_not_mutated(self, sample_assembly_request, sample_transaction_preview):
        original_payload = dict(sample_assembly_request.command_envelope.payload)
        refs = _minimal_refs_for_assembly()
        assemble_scene_command_execution_result(
            result_ref=build_record_id("assembly_result", "immutable_1"),
            request=sample_assembly_request,
            transaction_preview=sample_transaction_preview,
            **refs,
        )
        assert dict(sample_assembly_request.command_envelope.payload) == original_payload


# ---------------------------------------------------------------------------
# Authority flags
# ---------------------------------------------------------------------------


class TestAuthorityFlags:
    def test_default_authority_flags_are_all_false(self):
        flags = create_scene_command_execution_assembly_authority_flags()
        for field_name in flags.__dataclass_fields__:
            assert getattr(flags, field_name) is False

    @pytest.mark.parametrize(
        "flag_name",
        [
            "implementation_beyond_skeleton",
            "live_play_authority",
            "model_authority",
            "prompt_rendering",
            "prose_parsing",
            "narration_generation",
            "persistence_writes",
            "rng_table_oracle_execution",
            "state_mutation",
            "event_append",
            "settlement_authorization",
            "pr5_arithmetic_execution",
            "consequence_application",
            "conversion",
            "sourcebook_inclusion",
            "canon_promotion",
        ],
    )
    def test_true_authority_flag_rejected(self, flag_name):
        kwargs = {flag_name: True}
        with pytest.raises(SceneCommandExecutionSkeletonError, match=flag_name):
            SceneCommandExecutionAssemblyAuthorityFlags(**kwargs)

    def test_assembly_result_carries_false_flags(self, sample_assembly_result):
        for field_name in sample_assembly_result.authority_flags.__dataclass_fields__:
            assert getattr(sample_assembly_result.authority_flags, field_name) is False


# ---------------------------------------------------------------------------
# No implementation assertions
# ---------------------------------------------------------------------------


class TestNoImplementationAssertions:
    def test_no_model_call_imports(self):
        module_path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "scene_command_execution_skeleton.py"
        text = module_path.read_text(encoding="utf-8")
        assert "openai" not in text.lower()
        assert "anthropic" not in text.lower()
        assert "llm" not in text.lower()

    def test_no_prompt_templates(self):
        module_path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "scene_command_execution_skeleton.py"
        text = module_path.read_text(encoding="utf-8")
        assert "prompt template" not in text.lower()
        assert "render_prompt" not in text.lower()

    def test_no_live_play_adapter_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "live_play").exists()

    def test_no_ui_client_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "ui").exists()

    def test_no_database_package(self):
        assert not (REPO_ROOT / "src" / "astra_runtime" / "database").exists()


# ---------------------------------------------------------------------------
# Tiny vertical slice untouched
# ---------------------------------------------------------------------------


class TestTinyVerticalSliceUntouched:
    def test_tiny_vertical_slice_file_unchanged(self):
        tiny_path = REPO_ROOT / "src" / "astra_runtime" / "domain" / "tiny_vertical_slice.py"
        assert tiny_path.exists()
        # Only assert the file has not been modified in this branch relative to main.
        import subprocess
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert "src/astra_runtime/domain/tiny_vertical_slice.py" not in result.stdout


# ---------------------------------------------------------------------------
# Malformed input handling
# ---------------------------------------------------------------------------


class TestMalformedInputHandling:
    def test_empty_scene_ref_rejected(self):
        with pytest.raises(SceneCommandExecutionSkeletonError, match="scene_ref"):
            create_scene_command_execution_scene_contract(
                scene_ref="",
                scene_label="S",
                visible_description="desc",
            )

    def test_invalid_subject_type_rejected(self):
        with pytest.raises(SceneCommandExecutionSkeletonError, match="subject_type"):
            create_scene_command_execution_subject_ref(
                subject_type="invalid_subject",
                ref_id=build_record_id("actor", "malformed_1"),
            )

    def test_non_command_envelope_rejected(self):
        with pytest.raises(SceneCommandExecutionSkeletonError):
            create_scene_command_execution_command_intent_from_envelope(
                intent_ref="intent-1",
                command_envelope=object(),  # type: ignore[arg-type]
            )

    def test_assembly_result_rejects_invalid_transaction_preview(self, sample_assembly_request):
        refs = _minimal_refs_for_assembly()
        with pytest.raises(SceneCommandExecutionSkeletonError):
            assemble_scene_command_execution_result(
                result_ref=build_record_id("assembly_result", "invalid_preview_1"),
                request=sample_assembly_request,
                transaction_preview="not-a-preview",  # type: ignore[arg-type]
                **refs,
            )


# ---------------------------------------------------------------------------
# Deterministic repeatability
# ---------------------------------------------------------------------------


class TestDeterministicRepeatability:
    def test_repeated_assembly_produces_equal_output(self, sample_assembly_request, sample_transaction_preview):
        refs = _minimal_refs_for_assembly()
        first = assemble_scene_command_execution_result(
            result_ref=build_record_id("assembly_result", "repeat_1"),
            request=sample_assembly_request,
            transaction_preview=sample_transaction_preview,
            **refs,
        )
        second = assemble_scene_command_execution_result(
            result_ref=build_record_id("assembly_result", "repeat_1"),
            request=sample_assembly_request,
            transaction_preview=sample_transaction_preview,
            **refs,
        )
        assert first == second
        assert first.to_dict() == second.to_dict()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _minimal_refs_for_assembly() -> dict[str, object]:
    return {
        "validation_ref": create_scene_command_execution_validation_ref(validation_ref=build_record_id("validation", "minimal_1")),
        "resource_preview_ref": create_scene_command_execution_resource_preview_ref(preview_ref=build_record_id("resource_preview", "minimal_1")),
        "state_delta_candidate_ref": create_scene_command_execution_state_delta_candidate_ref(delta_ref=build_record_id("state_delta", "minimal_1")),
        "event_ledger_candidate_ref": create_scene_command_execution_event_ledger_candidate_ref(event_ref=build_record_id("event", "minimal_1")),
        "context_packet_ref": create_scene_command_execution_context_packet_ref(packet_ref=build_record_id("context_packet", "minimal_1")),
        "narration_packet_ref": create_scene_command_execution_narration_packet_ref(packet_ref=build_record_id("narration_packet", "minimal_1")),
        "model_boundary_fixture_ref": create_scene_command_execution_model_boundary_fixture_ref(fixture_ref=build_record_id("model_boundary_fixture", "minimal_1")),
    }
