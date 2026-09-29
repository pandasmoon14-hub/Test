"""WORLD-1/WORLD-2 bounded atomic world-advancement composition.

This module does not own temporal, spatial, or object-state semantics. It
composes immutable prepared/committed values so the application replaces its
authoritative flat root only after AFQR-04 time and the selected already-owned
WORLD-1/WORLD-2 consequence succeed together.
"""

from __future__ import annotations

from dataclasses import dataclass

from astra_runtime.domain.persistent_world_logical_time import (
    PersistentWorldLogicalTimeCommitReceipt,
    PersistentWorldLogicalTimePreparedTransition,
    commit_prepared_persistent_world_logical_time,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementCommitReceipt,
    PersistentWorldMovementPreparedTransition,
    commit_prepared_persistent_world_movement,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseCommitReceipt,
    PersistentWorldObjectOpenClosePreparedTransition,
    commit_prepared_persistent_world_object_open_close,
)
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    compose_persistent_world_open_close_state,
    replace_persistent_world_runtime_logical_time_state,
    replace_persistent_world_runtime_movement_state,
    replace_persistent_world_runtime_open_close_state,
)
from astra_runtime.kernel.record_identity import is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope
from astra_runtime.kernel.transaction_preview import TransactionPreview


class PersistentWorldWorldAdvancementError(ValueError):
    """Raised when bounded WORLD-1/WORLD-2 composition is inconsistent."""


@dataclass(frozen=True, kw_only=True)
class PersistentWorldWorldAdvancementResult:
    state: PersistentWorldRuntimeComposition
    time_receipt: PersistentWorldLogicalTimeCommitReceipt
    time_preview: TransactionPreview
    time_state_delta: StateDeltaEnvelope
    movement_receipt: PersistentWorldMovementCommitReceipt
    movement_preview: TransactionPreview
    movement_state_delta: StateDeltaEnvelope
    due_process_ref: str
    technical_retry: bool


@dataclass(frozen=True, kw_only=True)
class PersistentWorldWorldInteractionAdvancementResult:
    state: PersistentWorldRuntimeComposition
    time_receipt: PersistentWorldLogicalTimeCommitReceipt
    time_preview: TransactionPreview
    time_state_delta: StateDeltaEnvelope
    interaction_receipt: PersistentWorldObjectOpenCloseCommitReceipt
    interaction_preview: TransactionPreview
    interaction_state_delta: StateDeltaEnvelope
    due_process_ref: str
    technical_retry: bool


def _validate_world_advancement_inputs(
    *,
    state: PersistentWorldRuntimeComposition,
    due_process_ref: str,
) -> None:
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise PersistentWorldWorldAdvancementError(
            "state must be PersistentWorldRuntimeComposition"
        )
    if not is_valid_record_id(due_process_ref):
        raise PersistentWorldWorldAdvancementError(
            "due_process_ref must be a valid record ID"
        )


def commit_prepared_persistent_world_world_advancement(
    *,
    state: PersistentWorldRuntimeComposition,
    time_prepared: PersistentWorldLogicalTimePreparedTransition,
    movement_prepared: PersistentWorldMovementPreparedTransition,
    due_process_ref: str,
) -> PersistentWorldWorldAdvancementResult:
    _validate_world_advancement_inputs(
        state=state,
        due_process_ref=due_process_ref,
    )

    time_result = commit_prepared_persistent_world_logical_time(
        state=state.logical_time_state,
        prepared=time_prepared,
    )
    movement_result = commit_prepared_persistent_world_movement(
        state=state.movement_state,
        prepared=movement_prepared,
    )

    if time_result.technical_retry != movement_result.technical_retry:
        raise PersistentWorldWorldAdvancementError(
            "WORLD movement time and consequence retry state disagree"
        )

    candidate = replace_persistent_world_runtime_movement_state(
        state=state,
        movement_state=movement_result.state,
    )
    candidate = replace_persistent_world_runtime_logical_time_state(
        state=candidate,
        logical_time_state=time_result.state,
    )

    return PersistentWorldWorldAdvancementResult(
        state=candidate,
        time_receipt=time_result.receipt,
        time_preview=time_result.preview,
        time_state_delta=time_result.state_delta,
        movement_receipt=movement_result.receipt,
        movement_preview=movement_result.preview,
        movement_state_delta=movement_result.state_delta,
        due_process_ref=due_process_ref,
        technical_retry=time_result.technical_retry,
    )


def commit_prepared_persistent_world_world_interaction_advancement(
    *,
    state: PersistentWorldRuntimeComposition,
    time_prepared: PersistentWorldLogicalTimePreparedTransition,
    interaction_prepared: PersistentWorldObjectOpenClosePreparedTransition,
    due_process_ref: str,
) -> PersistentWorldWorldInteractionAdvancementResult:
    """Atomically compose one time step with one existing open/close owner step."""

    _validate_world_advancement_inputs(
        state=state,
        due_process_ref=due_process_ref,
    )

    time_result = commit_prepared_persistent_world_logical_time(
        state=state.logical_time_state,
        prepared=time_prepared,
    )
    interaction_result = commit_prepared_persistent_world_object_open_close(
        state=compose_persistent_world_open_close_state(state),
        prepared=interaction_prepared,
    )

    if time_result.technical_retry != interaction_result.technical_retry:
        raise PersistentWorldWorldAdvancementError(
            "WORLD interaction time and consequence retry state disagree"
        )

    candidate = replace_persistent_world_runtime_open_close_state(
        state=state,
        open_close_state=interaction_result.state,
    )
    candidate = replace_persistent_world_runtime_logical_time_state(
        state=candidate,
        logical_time_state=time_result.state,
    )

    return PersistentWorldWorldInteractionAdvancementResult(
        state=candidate,
        time_receipt=time_result.receipt,
        time_preview=time_result.preview,
        time_state_delta=time_result.state_delta,
        interaction_receipt=interaction_result.receipt,
        interaction_preview=interaction_result.preview,
        interaction_state_delta=interaction_result.state_delta,
        due_process_ref=due_process_ref,
        technical_retry=time_result.technical_retry,
    )
