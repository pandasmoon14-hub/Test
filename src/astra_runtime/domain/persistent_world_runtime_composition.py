"""Typed flat composition for the currently playable persistent-world state.

This module composes existing owner-controlled runtime state without acquiring
their semantic authority. WORLD-1 adds AFQR-04 logical time as another typed
component rather than restoring implementation chronology nesting.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Sequence

from astra_runtime.domain.persistent_world_logical_time import (
    PersistentWorldLogicalTimeState,
    create_persistent_world_logical_time_state,
    digest_persistent_world_logical_time_state,
)
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
    digest_persistent_world_object_storage_runtime_state,
)


@dataclass(frozen=True, kw_only=True)
class PersistentWorldRuntimeComposition:
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
    logical_time_state: PersistentWorldLogicalTimeState = field(
        default_factory=create_persistent_world_logical_time_state
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "committed_custody_transitions",
            tuple(self.committed_custody_transitions),
        )
        object.__setattr__(
            self, "object_open_states", tuple(self.object_open_states)
        )
        object.__setattr__(
            self, "committed_object_state_transitions",
            tuple(self.committed_object_state_transitions),
        )
        object.__setattr__(
            self, "object_lit_states", tuple(self.object_lit_states)
        )
        object.__setattr__(
            self, "committed_object_lit_transitions",
            tuple(self.committed_object_lit_transitions),
        )
        object.__setattr__(
            self, "committed_storage_transitions",
            tuple(self.committed_storage_transitions),
        )
        if not isinstance(
            self.logical_time_state, PersistentWorldLogicalTimeState
        ):
            raise TypeError(
                "logical_time_state must be PersistentWorldLogicalTimeState"
            )

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

        existing_ids = {
            item.command_id
            for item in storage_state.lit_state.open_close_state
            .custody_state.movement_state.committed_transitions
        }
        existing_ids.update(
            item.command_id
            for item in storage_state.lit_state.open_close_state
            .custody_state.committed_custody_transitions
        )
        existing_ids.update(
            item.command_id
            for item in storage_state.lit_state.open_close_state
            .committed_object_state_transitions
        )
        existing_ids.update(
            item.command_id
            for item in storage_state.lit_state.committed_object_lit_transitions
        )
        existing_ids.update(
            item.command_id
            for item in storage_state.committed_storage_transitions
        )
        time_ids = {
            item.command_id
            for item in self.logical_time_state.committed_transitions
        }
        if existing_ids & time_ids:
            raise ValueError(
                "logical-time command IDs must not collide with existing "
                "domain command IDs"
            )


def _compose_custody_state_unchecked(state):
    return PersistentWorldObjectCustodyRuntimeState(
        movement_state=state.movement_state,
        committed_custody_transitions=state.committed_custody_transitions,
    )


def _compose_open_close_state_unchecked(state):
    return PersistentWorldObjectOpenCloseRuntimeState(
        custody_state=_compose_custody_state_unchecked(state),
        object_open_states=state.object_open_states,
        committed_object_state_transitions=(
            state.committed_object_state_transitions
        ),
    )


def _compose_lit_state_unchecked(state):
    return PersistentWorldObjectLitRuntimeState(
        open_close_state=_compose_open_close_state_unchecked(state),
        object_lit_states=state.object_lit_states,
        committed_object_lit_transitions=(
            state.committed_object_lit_transitions
        ),
    )


def _compose_storage_state_unchecked(state):
    return PersistentWorldObjectStorageRuntimeState(
        lit_state=_compose_lit_state_unchecked(state),
        committed_storage_transitions=state.committed_storage_transitions,
    )


def create_persistent_world_runtime_composition(
    *,
    movement_state: PersistentWorldMovementRuntimeState,
    object_open_states: Sequence[PersistentWorldObjectOpenState] = (),
    object_lit_states: Sequence[PersistentWorldObjectLitState] = (),
    logical_time_state: PersistentWorldLogicalTimeState | None = None,
) -> PersistentWorldRuntimeComposition:
    return PersistentWorldRuntimeComposition(
        movement_state=movement_state,
        object_open_states=tuple(object_open_states),
        object_lit_states=tuple(object_lit_states),
        logical_time_state=(
            logical_time_state or create_persistent_world_logical_time_state()
        ),
    )


def create_persistent_world_runtime_composition_from_storage_state(
    storage_state: PersistentWorldObjectStorageRuntimeState,
    *,
    logical_time_state: PersistentWorldLogicalTimeState | None = None,
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
        committed_storage_transitions=storage_state.committed_storage_transitions,
        logical_time_state=(
            logical_time_state or create_persistent_world_logical_time_state()
        ),
    )


def compose_persistent_world_custody_state(state):
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_custody_state_unchecked(state)


def compose_persistent_world_open_close_state(state):
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_open_close_state_unchecked(state)


def compose_persistent_world_lit_state(state):
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_lit_state_unchecked(state)


def compose_persistent_world_storage_state(state):
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    return _compose_storage_state_unchecked(state)


def digest_persistent_world_runtime_composition(state) -> str:
    if not isinstance(state, PersistentWorldRuntimeComposition):
        raise TypeError("state must be PersistentWorldRuntimeComposition")
    material = {
        "state_family": "persistent_world_runtime_composition_world1",
        "storage_world_state_digest": (
            digest_persistent_world_object_storage_runtime_state(
                _compose_storage_state_unchecked(state)
            )
        ),
        "logical_time_state_digest": (
            digest_persistent_world_logical_time_state(
                state.logical_time_state
            )
        ),
    }
    canonical = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _copy(state, **changes):
    values = {
        "movement_state": state.movement_state,
        "committed_custody_transitions": state.committed_custody_transitions,
        "object_open_states": state.object_open_states,
        "committed_object_state_transitions": (
            state.committed_object_state_transitions
        ),
        "object_lit_states": state.object_lit_states,
        "committed_object_lit_transitions": (
            state.committed_object_lit_transitions
        ),
        "committed_storage_transitions": state.committed_storage_transitions,
        "logical_time_state": state.logical_time_state,
    }
    values.update(changes)
    return PersistentWorldRuntimeComposition(**values)


def replace_persistent_world_runtime_movement_state(*, state, movement_state):
    return _copy(state, movement_state=movement_state)


def replace_persistent_world_runtime_custody_state(*, state, custody_state):
    return _copy(
        state,
        movement_state=custody_state.movement_state,
        committed_custody_transitions=(
            custody_state.committed_custody_transitions
        ),
    )


def replace_persistent_world_runtime_open_close_state(
    *, state, open_close_state
):
    custody_state = open_close_state.custody_state
    return _copy(
        state,
        movement_state=custody_state.movement_state,
        committed_custody_transitions=(
            custody_state.committed_custody_transitions
        ),
        object_open_states=open_close_state.object_open_states,
        committed_object_state_transitions=(
            open_close_state.committed_object_state_transitions
        ),
    )


def replace_persistent_world_runtime_lit_state(*, state, lit_state):
    open_close_state = lit_state.open_close_state
    custody_state = open_close_state.custody_state
    return _copy(
        state,
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
    )


def replace_persistent_world_runtime_storage_state(*, state, storage_state):
    lit_state = storage_state.lit_state
    open_close_state = lit_state.open_close_state
    custody_state = open_close_state.custody_state
    return _copy(
        state,
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


def replace_persistent_world_runtime_logical_time_state(
    *, state, logical_time_state
):
    return _copy(state, logical_time_state=logical_time_state)
