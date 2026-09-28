"""Typed flat composition for the currently playable persistent-world state.

This module composes existing owner-controlled runtime state without acquiring
their semantic authority. The flat root stores the currently implemented state
families directly. Historical nested runtime-state classes remain the
validation, execution, digest, replay, and checkpoint compatibility views.

There is intentionally no generic state manager, dynamic component registry,
property bag, ECS conversion, semantic dispatch, or new authoritative digest.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRuntimeState,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyCommittedTransition,
    PersistentWorldObjectCustodyRuntimeState,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitRuntimeState,
    PersistentWorldObjectLitState,
    PersistentWorldObjectLitStateCommittedTransition,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseCommittedTransition,
    PersistentWorldObjectOpenCloseRuntimeState,
    PersistentWorldObjectOpenState,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageCommittedTransition,
    PersistentWorldObjectStorageRuntimeState,
)


__all__ = [
    "PersistentWorldRuntimeComposition",
    "create_persistent_world_runtime_composition",
    "create_persistent_world_runtime_composition_from_storage_state",
    "compose_persistent_world_custody_state",
    "compose_persistent_world_open_close_state",
    "compose_persistent_world_lit_state",
    "compose_persistent_world_storage_state",
    "replace_persistent_world_runtime_movement_state",
    "replace_persistent_world_runtime_custody_state",
    "replace_persistent_world_runtime_open_close_state",
    "replace_persistent_world_runtime_lit_state",
]


@dataclass(frozen=True, kw_only=True)
class PersistentWorldRuntimeComposition:
    """Flat typed root for current persistent-world runtime state.

    Each field remains semantically owned by its existing domain. Construction
    validates the whole composition by rebuilding the existing nested storage
    view, so no owner-local validation is reimplemented here.
    """

    movement_state: PersistentWorldMovementRuntimeState
    committed_custody_transitions: tuple[
        PersistentWorldObjectCustodyCommittedTransition, ...
    ] = ()
    object_open_states: tuple[PersistentWorldObjectOpenState, ...] = ()
    committed_object_state_transitions: tuple[
        PersistentWorldObjectOpenCloseCommittedTransition, ...
    ] = ()
    object_lit_states: tuple[PersistentWorldObjectLitState, ...] = ()
    committed_object_lit_transitions: tuple[
        PersistentWorldObjectLitStateCommittedTransition, ...
    ] = ()
    committed_storage_transitions: tuple[
        PersistentWorldObjectStorageCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "committed_custody_transitions",
            tuple(self.committed_custody_transitions),
        )
        object.__setattr__(
            self,
            "object_open_states",
            tuple(self.object_open_states),
        )
        object.__setattr__(
            self,
            "committed_object_state_transitions",
            tuple(self.committed_object_state_transitions),
        )
        object.__setattr__(
            self,
            "object_lit_states",
            tuple(self.object_lit_states),
        )
        object.__setattr__(
            self,
            "committed_object_lit_transitions",
            tuple(self.committed_object_lit_transitions),
        )
        object.__setattr__(
            self,
            "committed_storage_transitions",
            tuple(self.committed_storage_transitions),
        )

        # Existing domain constructors remain the semantic validators. This
        # projection also canonicalizes owner-local state ordering.
        storage_state = _compose_storage_state_unchecked(self)

        object.__setattr__(
            self,
            "committed_custody_transitions",
            storage_state.lit_state.open_close_state.custody_state
            .committed_custody_transitions,
        )
        object.__setattr__(
            self,
            "object_open_states",
            storage_state.lit_state.open_close_state.object_open_states,
        )
        object.__setattr__(
            self,
            "committed_object_state_transitions",
            storage_state.lit_state.open_close_state
            .committed_object_state_transitions,
        )
        object.__setattr__(
            self,
            "object_lit_states",
            storage_state.lit_state.object_lit_states,
        )
        object.__setattr__(
            self,
            "committed_object_lit_transitions",
            storage_state.lit_state.committed_object_lit_transitions,
        )
        object.__setattr__(
            self,
            "committed_storage_transitions",
            storage_state.committed_storage_transitions,
        )


def _compose_custody_state_unchecked(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectCustodyRuntimeState:
    return PersistentWorldObjectCustodyRuntimeState(
        movement_state=state.movement_state,
        committed_custody_transitions=state.committed_custody_transitions,
    )


def _compose_open_close_state_unchecked(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectOpenCloseRuntimeState:
    return PersistentWorldObjectOpenCloseRuntimeState(
        custody_state=_compose_custody_state_unchecked(state),
        object_open_states=state.object_open_states,
        committed_object_state_transitions=(
            state.committed_object_state_transitions
        ),
    )


def _compose_lit_state_unchecked(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectLitRuntimeState:
    return PersistentWorldObjectLitRuntimeState(
        open_close_state=_compose_open_close_state_unchecked(state),
        object_lit_states=state.object_lit_states,
        committed_object_lit_transitions=(
            state.committed_object_lit_transitions
        ),
    )


def _compose_storage_state_unchecked(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectStorageRuntimeState:
    return PersistentWorldObjectStorageRuntimeState(
        lit_state=_compose_lit_state_unchecked(state),
        committed_storage_transitions=state.committed_storage_transitions,
    )


def create_persistent_world_runtime_composition(
    *,
    movement_state: PersistentWorldMovementRuntimeState,
    object_open_states: Sequence[PersistentWorldObjectOpenState] = (),
    object_lit_states: Sequence[PersistentWorldObjectLitState] = (),
) -> PersistentWorldRuntimeComposition:
    return PersistentWorldRuntimeComposition(
        movement_state=movement_state,
        object_open_states=tuple(object_open_states),
        object_lit_states=tuple(object_lit_states),
    )


def create_persistent_world_runtime_composition_from_storage_state(
    storage_state: PersistentWorldObjectStorageRuntimeState,
) -> PersistentWorldRuntimeComposition:
    if not isinstance(storage_state, PersistentWorldObjectStorageRuntimeState):
        raise TypeError(
            "storage_state must be PersistentWorldObjectStorageRuntimeState"
        )

    lit_state = storage_state.lit_state
    open_close_state = lit_state.open_close_state
    custody_state = open_close_state.custody_state

    return PersistentWorldRuntimeComposition(
        movement_state=custody_state.movement_state,
        committed_custody_transitions=(
            custody_state.committed_custody_transitions
        ),
        object_open_states=open_close_state.object_open_states,
        committed_object_state_transitions=(
            open_close_state.committed_object_state_transitions
        ),
        object_lit_states=lit_state.object_lit_states,
        committed_object_lit_transitions=(
            lit_state.committed_object_lit_transitions
        ),
        committed_storage_transitions=(
            storage_state.committed_storage_transitions
        ),
    )


def compose_persistent_world_custody_state(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectCustodyRuntimeState:
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_custody_state_unchecked(state)


def compose_persistent_world_open_close_state(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectOpenCloseRuntimeState:
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_open_close_state_unchecked(state)


def compose_persistent_world_lit_state(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectLitRuntimeState:
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_lit_state_unchecked(state)


def compose_persistent_world_storage_state(
    state: PersistentWorldRuntimeComposition,
) -> PersistentWorldObjectStorageRuntimeState:
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_storage_state_unchecked(state)


def replace_persistent_world_runtime_movement_state(
    *,
    state: PersistentWorldRuntimeComposition,
    movement_state: PersistentWorldMovementRuntimeState,
) -> PersistentWorldRuntimeComposition:
    return PersistentWorldRuntimeComposition(
        movement_state=movement_state,
        committed_custody_transitions=state.committed_custody_transitions,
        object_open_states=state.object_open_states,
        committed_object_state_transitions=(
            state.committed_object_state_transitions
        ),
        object_lit_states=state.object_lit_states,
        committed_object_lit_transitions=(
            state.committed_object_lit_transitions
        ),
        committed_storage_transitions=state.committed_storage_transitions,
    )


def replace_persistent_world_runtime_custody_state(
    *,
    state: PersistentWorldRuntimeComposition,
    custody_state: PersistentWorldObjectCustodyRuntimeState,
) -> PersistentWorldRuntimeComposition:
    return PersistentWorldRuntimeComposition(
        movement_state=custody_state.movement_state,
        committed_custody_transitions=(
            custody_state.committed_custody_transitions
        ),
        object_open_states=state.object_open_states,
        committed_object_state_transitions=(
            state.committed_object_state_transitions
        ),
        object_lit_states=state.object_lit_states,
        committed_object_lit_transitions=(
            state.committed_object_lit_transitions
        ),
        committed_storage_transitions=state.committed_storage_transitions,
    )


def replace_persistent_world_runtime_open_close_state(
    *,
    state: PersistentWorldRuntimeComposition,
    open_close_state: PersistentWorldObjectOpenCloseRuntimeState,
) -> PersistentWorldRuntimeComposition:
    custody_state = open_close_state.custody_state
    return PersistentWorldRuntimeComposition(
        movement_state=custody_state.movement_state,
        committed_custody_transitions=(
            custody_state.committed_custody_transitions
        ),
        object_open_states=open_close_state.object_open_states,
        committed_object_state_transitions=(
            open_close_state.committed_object_state_transitions
        ),
        object_lit_states=state.object_lit_states,
        committed_object_lit_transitions=(
            state.committed_object_lit_transitions
        ),
        committed_storage_transitions=state.committed_storage_transitions,
    )


def replace_persistent_world_runtime_lit_state(
    *,
    state: PersistentWorldRuntimeComposition,
    lit_state: PersistentWorldObjectLitRuntimeState,
) -> PersistentWorldRuntimeComposition:
    open_close_state = lit_state.open_close_state
    custody_state = open_close_state.custody_state
    return PersistentWorldRuntimeComposition(
        movement_state=custody_state.movement_state,
        committed_custody_transitions=(
            custody_state.committed_custody_transitions
        ),
        object_open_states=open_close_state.object_open_states,
        committed_object_state_transitions=(
            open_close_state.committed_object_state_transitions
        ),
        object_lit_states=lit_state.object_lit_states,
        committed_object_lit_transitions=(
            lit_state.committed_object_lit_transitions
        ),
        committed_storage_transitions=state.committed_storage_transitions,
    )
