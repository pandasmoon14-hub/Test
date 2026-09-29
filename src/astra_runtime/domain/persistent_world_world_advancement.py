"""WORLD-1 bounded atomic composition of time plus one due movement.

This module does not own temporal or spatial semantics. It composes immutable
prepared/committed values so the application can replace its authoritative flat
root only after both AFQR-04 time and R4-C movement succeed.
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
from astra_runtime.domain.persistent_world_runtime_composition import (
    PersistentWorldRuntimeComposition,
    replace_persistent_world_runtime_logical_time_state,
    replace_persistent_world_runtime_movement_state,
)
from astra_runtime.kernel.record_identity import is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope
from astra_runtime.kernel.transaction_preview import TransactionPreview


class PersistentWorldWorldAdvancementError(ValueError):
    """Raised when bounded WORLD-1 composition is inconsistent."""


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


def commit_prepared_persistent_world_world_advancement(
    *,
    state: PersistentWorldRuntimeComposition,
    time_prepared: PersistentWorldLogicalTimePreparedTransition,
    movement_prepared: PersistentWorldMovementPreparedTransition,
    due_process_ref: str,
) -> PersistentWorldWorldAdvancementResult:
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise PersistentWorldWorldAdvancementError(
            "state must be PersistentWorldRuntimeComposition"
        )
    if not is_valid_record_id(due_process_ref):
        raise PersistentWorldWorldAdvancementError(
            "due_process_ref must be a valid record ID"
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
            "WORLD-1 time and mandatory movement retry state disagree"
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
