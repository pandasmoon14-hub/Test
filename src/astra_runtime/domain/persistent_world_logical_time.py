"""WORLD-1 bounded AFQR-04 logical-time runtime.

This module implements only the smallest executable logical-time capability
required by the Myravant WORLD-1 playable slice. It owns logical position and
immutable evidence of bounded `wait` transitions. It does not own spatial
movement, NPC agency, wall-clock progression, calendars, universal turns,
offline progression, generalized scheduling, or model decisions.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Mapping

from astra_runtime.domain._deterministic_transition_support import (
    command_fingerprint_matches,
    find_committed_transition,
    fingerprint_command_envelope,
)
from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
from astra_runtime.kernel.command_envelope import CommandEnvelope, validate_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.state_delta import (
    StateDeltaEnvelope,
    create_state_delta_envelope,
    validate_state_delta_envelope,
)
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    create_transaction_preview,
    validate_transaction_preview,
)

WORLD1_SCHEDULER_PROFILE_ID = "terminal-play-bounded-world-step-v1"
WORLD1_LOGICAL_TIME_RECORD_ID = build_record_id("state", "world1-logical-time")


class PersistentWorldLogicalTimeError(ValueError):
    """Base WORLD-1 logical-time error."""


class InvalidPersistentWorldLogicalTimeRequestError(PersistentWorldLogicalTimeError):
    pass


class PersistentWorldLogicalTimeStaleStateError(PersistentWorldLogicalTimeError):
    pass


class PersistentWorldLogicalTimeRetryConflictError(PersistentWorldLogicalTimeError):
    pass


class PersistentWorldLogicalTimeReplayError(PersistentWorldLogicalTimeError):
    pass


@dataclass(frozen=True, kw_only=True)
class PersistentWorldLogicalTimeCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    scheduler_profile_id: str
    pre_position: int
    post_position: int
    pre_state_digest: str
    post_state_digest: str
    preview_id: str
    state_delta_id: str
    status: str = "committed"

    def to_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "scheduler_profile_id": self.scheduler_profile_id,
            "pre_position": self.pre_position,
            "post_position": self.post_position,
            "pre_state_digest": self.pre_state_digest,
            "post_state_digest": self.post_state_digest,
            "preview_id": self.preview_id,
            "state_delta_id": self.state_delta_id,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldLogicalTimeCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldLogicalTimeCommitReceipt


@dataclass(frozen=True, kw_only=True)
class PersistentWorldLogicalTimeState:
    scheduler_profile_id: str = WORLD1_SCHEDULER_PROFILE_ID
    logical_position: int = 0
    committed_transitions: tuple[
        PersistentWorldLogicalTimeCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        if self.scheduler_profile_id != WORLD1_SCHEDULER_PROFILE_ID:
            raise InvalidPersistentWorldLogicalTimeRequestError(
                "WORLD-1 supports only its pinned scheduler profile"
            )
        if type(self.logical_position) is not int or self.logical_position < 0:
            raise InvalidPersistentWorldLogicalTimeRequestError(
                "logical_position must be a non-negative integer"
            )
        transitions = tuple(self.committed_transitions)
        if any(
            not isinstance(item, PersistentWorldLogicalTimeCommittedTransition)
            for item in transitions
        ):
            raise InvalidPersistentWorldLogicalTimeRequestError(
                "committed_transitions must contain logical-time transitions"
            )
        ids = [item.command_id for item in transitions]
        if len(ids) != len(set(ids)):
            raise InvalidPersistentWorldLogicalTimeRequestError(
                "committed logical-time command IDs must be unique"
            )
        object.__setattr__(self, "committed_transitions", transitions)


@dataclass(frozen=True, kw_only=True)
class PersistentWorldLogicalTimePreparedTransition:
    command_id: str
    command_fingerprint: str
    scheduler_profile_id: str
    pre_position: int
    post_position: int
    pre_state_digest: str
    post_state_digest: str
    routing_family: str
    owner_route: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope


@dataclass(frozen=True, kw_only=True)
class PersistentWorldLogicalTimeExecutionResult:
    state: PersistentWorldLogicalTimeState
    receipt: PersistentWorldLogicalTimeCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_persistent_world_logical_time_state(
    *,
    scheduler_profile_id: str = WORLD1_SCHEDULER_PROFILE_ID,
    logical_position: int = 0,
) -> PersistentWorldLogicalTimeState:
    return PersistentWorldLogicalTimeState(
        scheduler_profile_id=scheduler_profile_id,
        logical_position=logical_position,
    )


def digest_persistent_world_logical_time_state(
    state: PersistentWorldLogicalTimeState,
) -> str:
    if not isinstance(state, PersistentWorldLogicalTimeState):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "state must be PersistentWorldLogicalTimeState"
        )
    canonical = json.dumps(
        {
            "state_family": "world1_logical_time",
            "scheduler_profile_id": state.scheduler_profile_id,
            "logical_position": state.logical_position,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def fingerprint_persistent_world_logical_time_command(command: CommandEnvelope) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "command failed CommandEnvelope validation"
        )
    try:
        return fingerprint_command_envelope(command, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "logical-time command must be deterministically JSON-serializable"
        ) from exc


def _validate_wait_command(command: CommandEnvelope) -> None:
    normalized = command.command_type.strip().lower().replace("-", "_")
    if normalized != "wait":
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "WORLD-1 logical time supports only wait"
        )
    if dict(command.payload) != {
        "advance_steps": 1,
        "scheduler_profile_id": WORLD1_SCHEDULER_PROFILE_ID,
    }:
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "WORLD-1 wait must request exactly one step under the pinned profile"
        )


def prepare_persistent_world_logical_time(
    *,
    state: PersistentWorldLogicalTimeState,
    command: CommandEnvelope,
    expected_pre_state_digest: str,
) -> PersistentWorldLogicalTimePreparedTransition:
    if not isinstance(state, PersistentWorldLogicalTimeState):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "state must be PersistentWorldLogicalTimeState"
        )
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "invalid command envelope"
        )
    _validate_wait_command(command)

    fingerprint = fingerprint_persistent_world_logical_time_command(command)
    routing = route_command_envelope(
        request_ref=build_record_id("time_request", fingerprint[:24]),
        command_envelope=command,
    )
    if routing.classification.family != "time":
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "wait command must route through time family"
        )

    actual_pre = digest_persistent_world_logical_time_state(state)
    if expected_pre_state_digest != actual_pre:
        raise PersistentWorldLogicalTimeStaleStateError(
            "expected logical-time pre-state digest is stale"
        )

    post_position = state.logical_position + 1
    post_state = PersistentWorldLogicalTimeState(
        scheduler_profile_id=state.scheduler_profile_id,
        logical_position=post_position,
        committed_transitions=state.committed_transitions,
    )
    post_digest = digest_persistent_world_logical_time_state(post_state)
    token = fingerprint[:24]

    preview = create_transaction_preview(
        preview_id=build_record_id("time_preview", token),
        command=command,
        status="preview_created",
        messages=("bounded WORLD-1 logical-time advancement prepared",),
        requires_confirmation=False,
        metadata={
            "package": "TERMINAL-PLAY-WORLD-1",
            "semantic_owner": "AFQR-04",
            "mutation_performed": False,
        },
    )
    state_delta = create_state_delta_envelope(
        delta_id=build_record_id("time_delta", token),
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(WORLD1_LOGICAL_TIME_RECORD_ID,),
        change_type="record_update",
        payload={
            "scheduler_profile_id": state.scheduler_profile_id,
            "from_logical_position": state.logical_position,
            "to_logical_position": post_position,
        },
        metadata={
            "package": "TERMINAL-PLAY-WORLD-1",
            "semantic_owner": "AFQR-04",
            "qualified_transition_owner": "AFQR-01",
        },
    )

    return PersistentWorldLogicalTimePreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        scheduler_profile_id=state.scheduler_profile_id,
        pre_position=state.logical_position,
        post_position=post_position,
        pre_state_digest=actual_pre,
        post_state_digest=post_digest,
        routing_family=routing.classification.family,
        owner_route=routing.dispatch_shell.owner_route,
        preview=preview,
        state_delta=state_delta,
    )


def commit_prepared_persistent_world_logical_time(
    *,
    state: PersistentWorldLogicalTimeState,
    prepared: PersistentWorldLogicalTimePreparedTransition,
) -> PersistentWorldLogicalTimeExecutionResult:
    if not isinstance(state, PersistentWorldLogicalTimeState):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "state must be PersistentWorldLogicalTimeState"
        )
    if not isinstance(prepared, PersistentWorldLogicalTimePreparedTransition):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "prepared must be PersistentWorldLogicalTimePreparedTransition"
        )

    existing = find_committed_transition(
        state.committed_transitions, prepared.command_id
    )
    if existing is not None:
        if not command_fingerprint_matches(existing, prepared.command_fingerprint):
            raise PersistentWorldLogicalTimeRetryConflictError(
                "command ID already committed with different immutable meaning"
            )
        return PersistentWorldLogicalTimeExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )

    if digest_persistent_world_logical_time_state(state) != prepared.pre_state_digest:
        raise PersistentWorldLogicalTimeStaleStateError(
            "logical-time state changed after preparation"
        )
    if state.logical_position != prepared.pre_position:
        raise PersistentWorldLogicalTimeStaleStateError(
            "logical-time position changed after preparation"
        )

    receipt = PersistentWorldLogicalTimeCommitReceipt(
        receipt_id=build_record_id(
            "time_receipt", prepared.command_fingerprint[:24]
        ),
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        scheduler_profile_id=prepared.scheduler_profile_id,
        pre_position=prepared.pre_position,
        post_position=prepared.post_position,
        pre_state_digest=prepared.pre_state_digest,
        post_state_digest=prepared.post_state_digest,
        preview_id=prepared.preview.preview_id,
        state_delta_id=prepared.state_delta.delta_id,
    )
    committed = PersistentWorldLogicalTimeCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    post_state = PersistentWorldLogicalTimeState(
        scheduler_profile_id=state.scheduler_profile_id,
        logical_position=prepared.post_position,
        committed_transitions=tuple(
            sorted(
                (*state.committed_transitions, committed),
                key=lambda item: (item.command_id, item.command_fingerprint),
            )
        ),
    )
    if (
        digest_persistent_world_logical_time_state(post_state)
        != prepared.post_state_digest
    ):
        raise PersistentWorldLogicalTimeReplayError(
            "prepared logical-time post-state digest does not reproduce"
        )
    return PersistentWorldLogicalTimeExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def execute_persistent_world_logical_time(
    *,
    state: PersistentWorldLogicalTimeState,
    command: CommandEnvelope,
    expected_pre_state_digest: str,
) -> PersistentWorldLogicalTimeExecutionResult:
    fingerprint = fingerprint_persistent_world_logical_time_command(command)
    existing = find_committed_transition(
        state.committed_transitions, command.command_id
    )
    if existing is not None:
        if not command_fingerprint_matches(existing, fingerprint):
            raise PersistentWorldLogicalTimeRetryConflictError(
                "command ID already committed with materially different content"
            )
        return PersistentWorldLogicalTimeExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )
    prepared = prepare_persistent_world_logical_time(
        state=state,
        command=command,
        expected_pre_state_digest=expected_pre_state_digest,
    )
    return commit_prepared_persistent_world_logical_time(
        state=state,
        prepared=prepared,
    )


def replay_persistent_world_logical_time(
    *,
    pre_state: PersistentWorldLogicalTimeState,
    committed: PersistentWorldLogicalTimeCommittedTransition,
) -> PersistentWorldLogicalTimeState:
    if (
        digest_persistent_world_logical_time_state(pre_state)
        != committed.receipt.pre_state_digest
    ):
        raise PersistentWorldLogicalTimeReplayError(
            "replay pre-state digest mismatch"
        )
    if pre_state.logical_position != committed.receipt.pre_position:
        raise PersistentWorldLogicalTimeReplayError("replay pre-position mismatch")
    post = PersistentWorldLogicalTimeState(
        scheduler_profile_id=pre_state.scheduler_profile_id,
        logical_position=committed.receipt.post_position,
        committed_transitions=tuple(
            sorted(
                (*pre_state.committed_transitions, committed),
                key=lambda item: (item.command_id, item.command_fingerprint),
            )
        ),
    )
    if (
        digest_persistent_world_logical_time_state(post)
        != committed.receipt.post_state_digest
    ):
        raise PersistentWorldLogicalTimeReplayError(
            "replay post-state digest mismatch"
        )
    return post


def serialize_persistent_world_logical_time_state(
    state: PersistentWorldLogicalTimeState,
) -> dict[str, object]:
    if not isinstance(state, PersistentWorldLogicalTimeState):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "state must be PersistentWorldLogicalTimeState"
        )
    return {
        "scheduler_profile_id": state.scheduler_profile_id,
        "logical_position": state.logical_position,
        "logical_time_digest": digest_persistent_world_logical_time_state(state),
        "committed_time_transitions": [
            {
                "command_id": item.command_id,
                "command_fingerprint": item.command_fingerprint,
                "preview": item.preview.to_dict(),
                "state_delta": item.state_delta.to_dict(),
                "receipt": item.receipt.to_dict(),
            }
            for item in state.committed_transitions
        ],
    }


def _require_digest(value: object, name: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            f"{name} must be a lowercase SHA-256 digest"
        )
    return value


def restore_persistent_world_logical_time_state(
    material: object,
) -> PersistentWorldLogicalTimeState:
    if not isinstance(material, Mapping):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "logical-time checkpoint component must be a mapping"
        )
    if set(material) != {
        "scheduler_profile_id",
        "logical_position",
        "logical_time_digest",
        "committed_time_transitions",
    }:
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "logical-time checkpoint component has unexpected field membership"
        )

    transitions_material = material["committed_time_transitions"]
    if not isinstance(transitions_material, list):
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "committed_time_transitions must be a list"
        )

    transitions: list[PersistentWorldLogicalTimeCommittedTransition] = []
    for index, raw in enumerate(transitions_material):
        if not isinstance(raw, Mapping) or set(raw) != {
            "command_id",
            "command_fingerprint",
            "preview",
            "state_delta",
            "receipt",
        }:
            raise InvalidPersistentWorldLogicalTimeRequestError(
                f"committed_time_transitions[{index}] has invalid shape"
            )
        preview_raw = raw["preview"]
        delta_raw = raw["state_delta"]
        receipt_raw = raw["receipt"]
        if not all(
            isinstance(item, Mapping)
            for item in (preview_raw, delta_raw, receipt_raw)
        ):
            raise InvalidPersistentWorldLogicalTimeRequestError(
                "logical-time transition records must be mappings"
            )
        preview = TransactionPreview(
            preview_id=preview_raw["preview_id"],
            command_id=preview_raw["command_id"],
            status=preview_raw["status"],
            messages=tuple(preview_raw["messages"]),
            requires_confirmation=preview_raw["requires_confirmation"],
            metadata=dict(preview_raw["metadata"]),
        )
        delta = StateDeltaEnvelope(
            delta_id=delta_raw["delta_id"],
            source_command_id=delta_raw["source_command_id"],
            source_preview_id=delta_raw["source_preview_id"],
            affected_record_ids=tuple(delta_raw["affected_record_ids"]),
            change_type=delta_raw["change_type"],
            payload=dict(delta_raw["payload"]),
            metadata=dict(delta_raw["metadata"]),
        )
        receipt = PersistentWorldLogicalTimeCommitReceipt(
            receipt_id=receipt_raw["receipt_id"],
            command_id=receipt_raw["command_id"],
            command_fingerprint=_require_digest(
                receipt_raw["command_fingerprint"],
                "receipt.command_fingerprint",
            ),
            scheduler_profile_id=receipt_raw["scheduler_profile_id"],
            pre_position=receipt_raw["pre_position"],
            post_position=receipt_raw["post_position"],
            pre_state_digest=_require_digest(
                receipt_raw["pre_state_digest"], "receipt.pre_state_digest"
            ),
            post_state_digest=_require_digest(
                receipt_raw["post_state_digest"], "receipt.post_state_digest"
            ),
            preview_id=receipt_raw["preview_id"],
            state_delta_id=receipt_raw["state_delta_id"],
            status=receipt_raw["status"],
        )
        if (
            not validate_transaction_preview(preview)
            or not validate_state_delta_envelope(delta)
        ):
            raise InvalidPersistentWorldLogicalTimeRequestError(
                "logical-time preview/state-delta checkpoint material is invalid"
            )
        fingerprint = _require_digest(
            raw["command_fingerprint"], "command_fingerprint"
        )
        if (
            preview.command_id != raw["command_id"]
            or delta.source_command_id != raw["command_id"]
            or receipt.command_id != raw["command_id"]
            or receipt.command_fingerprint != fingerprint
        ):
            raise InvalidPersistentWorldLogicalTimeRequestError(
                "logical-time transition identity disagrees"
            )
        transitions.append(
            PersistentWorldLogicalTimeCommittedTransition(
                command_id=raw["command_id"],
                command_fingerprint=fingerprint,
                preview=preview,
                state_delta=delta,
                receipt=receipt,
            )
        )

    state = PersistentWorldLogicalTimeState(
        scheduler_profile_id=material["scheduler_profile_id"],
        logical_position=material["logical_position"],
        committed_transitions=tuple(transitions),
    )
    expected_digest = _require_digest(
        material["logical_time_digest"], "logical_time_digest"
    )
    if digest_persistent_world_logical_time_state(state) != expected_digest:
        raise InvalidPersistentWorldLogicalTimeRequestError(
            "logical-time checkpoint semantic digest mismatch"
        )
    return state
