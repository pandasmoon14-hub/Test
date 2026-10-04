"""Extraction-time lifecycle adapters for existing deterministic families.

Each adapter delegates every semantic decision to its existing domain module.
This module only wires the already-owned prepare/commit/retry/replay surfaces
through the shared deterministic lifecycle shell. The capability specs remain
separate so movement, asset state, storage, displacement, and handoff do not
collapse into one universal semantic structure.
"""

from __future__ import annotations

from typing import Mapping

from astra_runtime.domain._deterministic_transition_support import (
    TransitionCapabilitySpec,
    execute_capability_transition,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    PersistentWorldEntityLocationRepresentation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    MovementOpportunityEvidence,
    MovementSpatialEvidence,
    PersistentWorldMovementExecutionResult,
    PersistentWorldMovementRetryConflictError,
    PersistentWorldMovementRuntimeState,
    commit_prepared_persistent_world_movement,
    digest_persistent_world_entity_location_representation,
    fingerprint_persistent_world_movement_command,
    prepare_persistent_world_movement,
    replay_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    ObjectOpenCloseOpportunityEvidence,
    ObjectOpenCloseQualificationEvidence,
    PersistentWorldObjectOpenCloseExecutionResult,
    PersistentWorldObjectOpenCloseRetryConflictError,
    PersistentWorldObjectOpenCloseRuntimeState,
    commit_prepared_persistent_world_object_open_close,
    digest_persistent_world_object_open_states,
    fingerprint_persistent_world_object_open_close_command,
    prepare_persistent_world_object_open_close,
    replay_persistent_world_object_open_close_states,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    ObjectLitStateOpportunityEvidence,
    ObjectLitStateQualificationEvidence,
    PersistentWorldObjectLitRuntimeState,
    PersistentWorldObjectLitStateExecutionResult,
    PersistentWorldObjectLitStateRetryConflictError,
    commit_prepared_persistent_world_object_lit_state,
    digest_persistent_world_object_lit_states,
    fingerprint_persistent_world_object_lit_state_command,
    prepare_persistent_world_object_lit_state,
    replay_persistent_world_object_lit_states,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    ObjectStorageOpportunityEvidence,
    ObjectStorageQualificationEvidence,
    PersistentWorldObjectStorageExecutionResult,
    PersistentWorldObjectStorageRetryConflictError,
    PersistentWorldObjectStorageRuntimeState,
    commit_prepared_persistent_world_object_storage,
    fingerprint_persistent_world_object_storage_command,
    prepare_persistent_world_object_storage,
    replay_persistent_world_object_storage,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    ObjectDisplacementOpportunityEvidence,
    ObjectDisplacementQualificationEvidence,
    ObjectDisplacementSpatialEvidence,
    PersistentWorldObjectDisplacementExecutionResult,
    PersistentWorldObjectDisplacementRetryConflictError,
    PersistentWorldObjectDisplacementRuntimeState,
    commit_prepared_persistent_world_object_displacement,
    fingerprint_persistent_world_object_displacement_command,
    prepare_persistent_world_object_displacement,
    replay_persistent_world_object_displacement,
)
from astra_runtime.domain.persistent_world_actor_object_handoff import (
    ActorObjectHandoffOpportunityEvidence,
    ActorObjectHandoffQualificationEvidence,
    ActorObjectHandoffSpatialEvidence,
    PersistentWorldActorObjectHandoffExecutionResult,
    PersistentWorldActorObjectHandoffRetryConflictError,
    PersistentWorldActorObjectHandoffRuntimeState,
    commit_prepared_persistent_world_actor_object_handoff,
    fingerprint_persistent_world_actor_object_handoff_command,
    prepare_persistent_world_actor_object_handoff,
    replay_persistent_world_actor_object_handoff,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope


def _context_item(context: Mapping[str, object], name: str, expected_type: type):
    value = context.get(name)
    if not isinstance(value, expected_type):
        raise TypeError(f"{name} must be {expected_type.__name__}")
    return value


def _expected_digest(context: Mapping[str, object]) -> str:
    return _context_item(context, "expected_pre_state_digest", str)


def _placement_representation_from_storage(state: PersistentWorldObjectStorageRuntimeState):
    return (
        state.lit_state.open_close_state.custody_state
        .movement_state.representation
    )


def _placement_representation_from_displacement(
    state: PersistentWorldObjectDisplacementRuntimeState,
):
    return _placement_representation_from_storage(state.storage_state)


def _placement_representation_from_handoff(
    state: PersistentWorldActorObjectHandoffRuntimeState,
):
    return _placement_representation_from_displacement(state.displacement_state)


# ---------------------------------------------------------------------------
# R4-C movement
# ---------------------------------------------------------------------------


def _prepare_movement(state, command, context):
    return prepare_persistent_world_movement(
        state=state,
        command=command,
        spatial_evidence=_context_item(context, "spatial_evidence", MovementSpatialEvidence),
        opportunity_evidence=_context_item(
            context, "opportunity_evidence", MovementOpportunityEvidence
        ),
        expected_pre_state_digest=_expected_digest(context),
    )


def _retry_movement(state, committed):
    return PersistentWorldMovementExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    )


def _replay_movement(pre_state, receipt):
    return replay_persistent_world_movement(
        pre_state_representation=pre_state,
        receipt=receipt,
    )


MOVEMENT_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_movement",
    semantic_owners=("AFQR-02", "AFQR-03", "AFQR-18", "AFQR-19", "AFQR-01"),
    state_type=PersistentWorldMovementRuntimeState,
    replay_state_type=PersistentWorldEntityLocationRepresentation,
    receipt_prefix="movement_receipt",
    state_digest=lambda state: digest_persistent_world_entity_location_representation(
        state.representation
    ),
    fingerprint_command=fingerprint_persistent_world_movement_command,
    committed_transitions=lambda state: state.committed_transitions,
    prepare_new_transition=_prepare_movement,
    commit_new_transition=lambda state, prepared: commit_prepared_persistent_world_movement(
        state=state, prepared=prepared
    ),
    build_retry_result=_retry_movement,
    retry_conflict_error=lambda message: PersistentWorldMovementRetryConflictError(message),
    replay_committed_transition=_replay_movement,
)


def execute_movement_via_transition_kernel(
    *, state, command, spatial_evidence, opportunity_evidence, expected_pre_state_digest
):
    return execute_capability_transition(
        spec=MOVEMENT_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "spatial_evidence": spatial_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )


# ---------------------------------------------------------------------------
# INT-1 open/close
# ---------------------------------------------------------------------------


def _prepare_open_close(state, command, context):
    return prepare_persistent_world_object_open_close(
        state=state,
        command=command,
        qualification_evidence=_context_item(
            context, "qualification_evidence", ObjectOpenCloseQualificationEvidence
        ),
        opportunity_evidence=_context_item(
            context, "opportunity_evidence", ObjectOpenCloseOpportunityEvidence
        ),
        expected_pre_state_digest=_expected_digest(context),
    )


def _retry_open_close(state, committed):
    return PersistentWorldObjectOpenCloseExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    )


def _replay_open_close(pre_state, receipt):
    return replay_persistent_world_object_open_close_states(
        object_open_states=pre_state,
        receipt=receipt,
    )


OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_object_open_close",
    semantic_owners=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    state_type=PersistentWorldObjectOpenCloseRuntimeState,
    replay_state_type=tuple,
    receipt_prefix="object_state_receipt",
    state_digest=lambda state: digest_persistent_world_object_open_states(
        state.object_open_states
    ),
    fingerprint_command=fingerprint_persistent_world_object_open_close_command,
    committed_transitions=lambda state: state.committed_object_state_transitions,
    prepare_new_transition=_prepare_open_close,
    commit_new_transition=lambda state, prepared: commit_prepared_persistent_world_object_open_close(
        state=state, prepared=prepared
    ),
    build_retry_result=_retry_open_close,
    retry_conflict_error=lambda message: PersistentWorldObjectOpenCloseRetryConflictError(
        message
    ),
    replay_committed_transition=_replay_open_close,
)


def execute_open_close_via_transition_kernel(
    *, state, command, qualification_evidence, opportunity_evidence, expected_pre_state_digest
):
    return execute_capability_transition(
        spec=OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )


# ---------------------------------------------------------------------------
# INT-2 lit state
# ---------------------------------------------------------------------------


def _prepare_lit(state, command, context):
    return prepare_persistent_world_object_lit_state(
        state=state,
        command=command,
        qualification_evidence=_context_item(
            context, "qualification_evidence", ObjectLitStateQualificationEvidence
        ),
        opportunity_evidence=_context_item(
            context, "opportunity_evidence", ObjectLitStateOpportunityEvidence
        ),
        expected_pre_state_digest=_expected_digest(context),
    )


def _retry_lit(state, committed):
    return PersistentWorldObjectLitStateExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    )


def _replay_lit(pre_state, receipt):
    return replay_persistent_world_object_lit_states(
        object_lit_states=pre_state,
        receipt=receipt,
    )


LIT_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_object_lit_state",
    semantic_owners=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    state_type=PersistentWorldObjectLitRuntimeState,
    replay_state_type=tuple,
    receipt_prefix="object_lit_state_receipt",
    state_digest=lambda state: digest_persistent_world_object_lit_states(
        state.object_lit_states
    ),
    fingerprint_command=fingerprint_persistent_world_object_lit_state_command,
    committed_transitions=lambda state: state.committed_object_lit_transitions,
    prepare_new_transition=_prepare_lit,
    commit_new_transition=lambda state, prepared: commit_prepared_persistent_world_object_lit_state(
        state=state, prepared=prepared
    ),
    build_retry_result=_retry_lit,
    retry_conflict_error=lambda message: PersistentWorldObjectLitStateRetryConflictError(
        message
    ),
    replay_committed_transition=_replay_lit,
)


def execute_lit_via_transition_kernel(
    *, state, command, qualification_evidence, opportunity_evidence, expected_pre_state_digest
):
    return execute_capability_transition(
        spec=LIT_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )


# ---------------------------------------------------------------------------
# INT-3 storage
# ---------------------------------------------------------------------------


def _prepare_storage(state, command, context):
    return prepare_persistent_world_object_storage(
        state=state,
        command=command,
        qualification_evidence=_context_item(
            context, "qualification_evidence", ObjectStorageQualificationEvidence
        ),
        opportunity_evidence=_context_item(
            context, "opportunity_evidence", ObjectStorageOpportunityEvidence
        ),
        expected_pre_state_digest=_expected_digest(context),
    )


def _retry_storage(state, committed):
    return PersistentWorldObjectStorageExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    )


def _replay_storage(pre_state, receipt):
    return replay_persistent_world_object_storage(
        representation=pre_state,
        receipt=receipt,
    )


STORAGE_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_object_storage",
    semantic_owners=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    state_type=PersistentWorldObjectStorageRuntimeState,
    replay_state_type=PersistentWorldEntityLocationRepresentation,
    receipt_prefix="storage_receipt",
    state_digest=lambda state: digest_persistent_world_entity_location_representation(
        _placement_representation_from_storage(state)
    ),
    fingerprint_command=fingerprint_persistent_world_object_storage_command,
    committed_transitions=lambda state: state.committed_storage_transitions,
    prepare_new_transition=_prepare_storage,
    commit_new_transition=lambda state, prepared: commit_prepared_persistent_world_object_storage(
        state=state, prepared=prepared
    ),
    build_retry_result=_retry_storage,
    retry_conflict_error=lambda message: PersistentWorldObjectStorageRetryConflictError(
        message
    ),
    replay_committed_transition=_replay_storage,
)


def execute_storage_via_transition_kernel(
    *, state, command, qualification_evidence, opportunity_evidence, expected_pre_state_digest
):
    return execute_capability_transition(
        spec=STORAGE_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )


# ---------------------------------------------------------------------------
# COMP-3 displacement
# ---------------------------------------------------------------------------


def _prepare_displacement(state, command, context):
    return prepare_persistent_world_object_displacement(
        state=state,
        command=command,
        qualification_evidence=_context_item(
            context, "qualification_evidence", ObjectDisplacementQualificationEvidence
        ),
        spatial_evidence=_context_item(
            context, "spatial_evidence", ObjectDisplacementSpatialEvidence
        ),
        opportunity_evidence=_context_item(
            context, "opportunity_evidence", ObjectDisplacementOpportunityEvidence
        ),
        expected_pre_state_digest=_expected_digest(context),
    )


def _retry_displacement(state, committed):
    return PersistentWorldObjectDisplacementExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    )


def _replay_displacement(pre_state, receipt):
    return replay_persistent_world_object_displacement(
        pre_state_representation=pre_state,
        receipt=receipt,
    )


DISPLACEMENT_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_object_displacement",
    semantic_owners=("RT-010", "AFQR-18", "AFQR-19", "AFQR-01", "AFQR-02"),
    state_type=PersistentWorldObjectDisplacementRuntimeState,
    replay_state_type=PersistentWorldEntityLocationRepresentation,
    receipt_prefix="object_displacement_receipt",
    state_digest=lambda state: digest_persistent_world_entity_location_representation(
        _placement_representation_from_displacement(state)
    ),
    fingerprint_command=fingerprint_persistent_world_object_displacement_command,
    committed_transitions=lambda state: state.committed_object_displacement_transitions,
    prepare_new_transition=_prepare_displacement,
    commit_new_transition=lambda state, prepared: commit_prepared_persistent_world_object_displacement(
        state=state, prepared=prepared
    ),
    build_retry_result=_retry_displacement,
    retry_conflict_error=lambda message: PersistentWorldObjectDisplacementRetryConflictError(
        message
    ),
    replay_committed_transition=_replay_displacement,
)


def execute_displacement_via_transition_kernel(
    *, state, command, qualification_evidence, spatial_evidence,
    opportunity_evidence, expected_pre_state_digest
):
    return execute_capability_transition(
        spec=DISPLACEMENT_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification_evidence,
            "spatial_evidence": spatial_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )


# ---------------------------------------------------------------------------
# VSM-6 voluntary actor-object handoff
# ---------------------------------------------------------------------------


def _prepare_handoff(state, command, context):
    return prepare_persistent_world_actor_object_handoff(
        state=state,
        command=command,
        qualification_evidence=_context_item(
            context, "qualification_evidence", ActorObjectHandoffQualificationEvidence
        ),
        spatial_evidence=_context_item(
            context, "spatial_evidence", ActorObjectHandoffSpatialEvidence
        ),
        opportunity_evidence=_context_item(
            context, "opportunity_evidence", ActorObjectHandoffOpportunityEvidence
        ),
        expected_pre_state_digest=_expected_digest(context),
    )


def _retry_handoff(state, committed):
    return PersistentWorldActorObjectHandoffExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    )


def _replay_handoff(pre_state, receipt):
    return replay_persistent_world_actor_object_handoff(
        pre_state_representation=pre_state,
        receipt=receipt,
    )


HANDOFF_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_actor_object_handoff",
    semantic_owners=("RT-010", "AFQR-18", "AFQR-19", "AFQR-01", "AFQR-02"),
    state_type=PersistentWorldActorObjectHandoffRuntimeState,
    replay_state_type=PersistentWorldEntityLocationRepresentation,
    receipt_prefix="actor_object_handoff_receipt",
    state_digest=lambda state: digest_persistent_world_entity_location_representation(
        _placement_representation_from_handoff(state)
    ),
    fingerprint_command=fingerprint_persistent_world_actor_object_handoff_command,
    committed_transitions=lambda state: state.committed_actor_object_handoff_transitions,
    prepare_new_transition=_prepare_handoff,
    commit_new_transition=lambda state, prepared: commit_prepared_persistent_world_actor_object_handoff(
        state=state, prepared=prepared
    ),
    build_retry_result=_retry_handoff,
    retry_conflict_error=lambda message: PersistentWorldActorObjectHandoffRetryConflictError(
        message
    ),
    replay_committed_transition=_replay_handoff,
)


def execute_handoff_via_transition_kernel(
    *, state, command, qualification_evidence, spatial_evidence,
    opportunity_evidence, expected_pre_state_digest
):
    return execute_capability_transition(
        spec=HANDOFF_TRANSITION_CAPABILITY_SPEC,
        state=state,
        command=command,
        context={
            "qualification_evidence": qualification_evidence,
            "spatial_evidence": spatial_evidence,
            "opportunity_evidence": opportunity_evidence,
            "expected_pre_state_digest": expected_pre_state_digest,
        },
    )
