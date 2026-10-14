"""Bounded persistent object open/close state for TERMINAL-PLAY-INT-1.

This module proves one narrow persistent asset-state family: an object may have
an authoritative ``open`` or ``closed`` state. It composes R4-E custody state
without changing R4-B location/custody representation semantics.

Authority remains routed to existing owners:
* RT-010: bounded asset/open-state semantics
* AFQR-19: target/opportunity qualification
* AFQR-01: qualified transition commitment
* AFQR-02: command identity/retry behavior through CommandEnvelope identity

This is not a generalized property bag, container system, activation system,
inventory system, durability system, resource system, effect system, or sensing
system.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict, replace
from typing import Sequence

from astra_runtime.domain._deterministic_transition_support import (
    TransitionCapabilitySpec,
    commit_prepared_capability_transition,
    execute_capability_transition,
    fingerprint_command_envelope,
)
from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntityLocationRepresentation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyRuntimeState,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope, validate_command_envelope, create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope, create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import TransactionPreview, create_transaction_preview


RT010_OBJECT_OPEN_CLOSE_OWNER = "RT-010"
AFQR19_OBJECT_OPEN_CLOSE_OPPORTUNITY_OWNER = "AFQR-19"
OBJECT_OPEN_CLOSE_STATES = frozenset({"open", "closed"})
OBJECT_OPEN_CLOSE_OPERATIONS = frozenset({"open", "close"})
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PersistentWorldObjectOpenCloseError(ValueError):
    pass


class InvalidPersistentWorldObjectOpenCloseRequestError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenCloseEntityError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenClosePlacementError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenCloseEvidenceError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenCloseUnsupportedStateError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenCloseNoChangeError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenCloseStaleStateError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenCloseRetryConflictError(PersistentWorldObjectOpenCloseError):
    pass


class PersistentWorldObjectOpenCloseReplayError(PersistentWorldObjectOpenCloseError):
    pass


def _require_record_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            f"{label} must be a valid record ID"
        )
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            f"{label} must be a lowercase SHA-256 digest"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class ObjectOpenCloseQualificationEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    qualified: bool
    semantic_owner: str = RT010_OBJECT_OPEN_CLOSE_OWNER

    def __post_init__(self) -> None:
        for name in ("evidence_id", "actor_entity_id", "object_entity_id"):
            _require_record_id(getattr(self, name), name)
        if self.operation not in OBJECT_OPEN_CLOSE_OPERATIONS:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "operation must be open or close"
            )
        if type(self.qualified) is not bool:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "qualified must be bool"
            )
        if self.semantic_owner != RT010_OBJECT_OPEN_CLOSE_OWNER:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "qualification semantic_owner must be RT-010"
            )


@dataclass(frozen=True, kw_only=True)
class ObjectOpenCloseOpportunityEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_OBJECT_OPEN_CLOSE_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        for name in ("evidence_id", "actor_entity_id", "object_entity_id"):
            _require_record_id(getattr(self, name), name)
        if self.operation not in OBJECT_OPEN_CLOSE_OPERATIONS:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "operation must be open or close"
            )
        if type(self.opportunity_available) is not bool:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "opportunity_available must be bool"
            )
        if type(self.resolution_accepted) is not bool:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "resolution_accepted must be bool"
            )
        if self.semantic_owner != AFQR19_OBJECT_OPEN_CLOSE_OPPORTUNITY_OWNER:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "opportunity semantic_owner must be AFQR-19"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectOpenState:
    object_entity_id: str
    state: str
    semantic_owner: str = RT010_OBJECT_OPEN_CLOSE_OWNER

    def __post_init__(self) -> None:
        _require_record_id(self.object_entity_id, "object_entity_id")
        if self.state not in OBJECT_OPEN_CLOSE_STATES:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "state must be open or closed"
            )
        if self.semantic_owner != RT010_OBJECT_OPEN_CLOSE_OWNER:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "open/close semantic_owner must be RT-010"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "object_entity_id": self.object_entity_id,
            "state": self.state,
            "semantic_owner": self.semantic_owner,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectOpenCloseCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    pre_object_state: str
    post_object_state: str
    pre_state_digest: str
    post_state_digest: str
    placement_digest: str
    preview_id: str
    state_delta_id: str
    rt010_qualification_id: str
    opportunity_evidence_id: str
    status: str = "committed"

    def __post_init__(self) -> None:
        for name in (
            "receipt_id", "actor_entity_id", "object_entity_id", "preview_id",
            "state_delta_id", "rt010_qualification_id", "opportunity_evidence_id",
        ):
            _require_record_id(getattr(self, name), name)
        if not isinstance(self.command_id, str) or not self.command_id.strip():
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "command_id must be non-empty"
            )
        _require_sha256(self.command_fingerprint, "command_fingerprint")
        _require_sha256(self.pre_state_digest, "pre_state_digest")
        _require_sha256(self.post_state_digest, "post_state_digest")
        _require_sha256(self.placement_digest, "placement_digest")
        if self.operation not in OBJECT_OPEN_CLOSE_OPERATIONS:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "operation must be open or close"
            )
        expected = ("closed", "open") if self.operation == "open" else ("open", "closed")
        if (self.pre_object_state, self.post_object_state) != expected:
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "receipt object states disagree with operation"
            )
        if self.status != "committed":
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "receipt status must be committed"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "actor_entity_id": self.actor_entity_id,
            "object_entity_id": self.object_entity_id,
            "operation": self.operation,
            "pre_object_state": self.pre_object_state,
            "post_object_state": self.post_object_state,
            "pre_state_digest": self.pre_state_digest,
            "post_state_digest": self.post_state_digest,
            "placement_digest": self.placement_digest,
            "preview_id": self.preview_id,
            "state_delta_id": self.state_delta_id,
            "rt010_qualification_id": self.rt010_qualification_id,
            "opportunity_evidence_id": self.opportunity_evidence_id,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectOpenCloseCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldObjectOpenCloseCommitReceipt


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectOpenCloseRuntimeState:
    custody_state: PersistentWorldObjectCustodyRuntimeState
    object_open_states: tuple[PersistentWorldObjectOpenState, ...] = ()
    committed_object_state_transitions: tuple[
        PersistentWorldObjectOpenCloseCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.custody_state, PersistentWorldObjectCustodyRuntimeState):
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "custody_state must be PersistentWorldObjectCustodyRuntimeState"
            )
        states = tuple(sorted(self.object_open_states, key=lambda item: item.object_entity_id))
        for item in states:
            if not isinstance(item, PersistentWorldObjectOpenState):
                raise InvalidPersistentWorldObjectOpenCloseRequestError(
                    "object_open_states contains an invalid value"
                )
        ids = [item.object_entity_id for item in states]
        if len(ids) != len(set(ids)):
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "object_open_states must have unique object_entity_id values"
            )
        entity_by_id = {
            entity.entity_id: entity
            for entity in self.custody_state.movement_state.representation.entities
        }
        for object_entity_id in ids:
            entity = entity_by_id.get(object_entity_id)
            if entity is None or entity.classification != "object":
                raise PersistentWorldObjectOpenCloseEntityError(
                    "open/close state target must exist and be classified as object"
                )

        transitions = tuple(sorted(
            self.committed_object_state_transitions,
            key=lambda item: (item.command_id, item.command_fingerprint),
        ))
        for transition in transitions:
            if not isinstance(transition, PersistentWorldObjectOpenCloseCommittedTransition):
                raise InvalidPersistentWorldObjectOpenCloseRequestError(
                    "committed_object_state_transitions contains an invalid value"
                )
        command_ids = [item.command_id for item in transitions]
        if len(command_ids) != len(set(command_ids)):
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "object-state command IDs must be unique"
            )
        movement_ids = {
            item.command_id for item in self.custody_state.movement_state.committed_transitions
        }
        custody_ids = {
            item.command_id for item in self.custody_state.committed_custody_transitions
        }
        if set(command_ids) & (movement_ids | custody_ids):
            raise InvalidPersistentWorldObjectOpenCloseRequestError(
                "object-state command IDs must not collide with movement/custody"
            )
        object.__setattr__(self, "object_open_states", states)
        object.__setattr__(self, "committed_object_state_transitions", transitions)


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectOpenClosePreparedTransition:
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    pre_object_state: str
    post_object_state: str
    pre_state_digest: str
    post_state_digest: str
    placement_digest: str
    rt010_qualification_id: str
    opportunity_evidence_id: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    post_object_open_states: tuple[PersistentWorldObjectOpenState, ...]


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectOpenCloseExecutionResult:
    state: PersistentWorldObjectOpenCloseRuntimeState
    receipt: PersistentWorldObjectOpenCloseCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_object_open_close_qualification_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    operation: str, qualified: bool,
) -> ObjectOpenCloseQualificationEvidence:
    return ObjectOpenCloseQualificationEvidence(
        evidence_id=evidence_id, actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id, operation=operation, qualified=qualified,
    )


def create_object_open_close_opportunity_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    operation: str, opportunity_available: bool, resolution_accepted: bool,
) -> ObjectOpenCloseOpportunityEvidence:
    return ObjectOpenCloseOpportunityEvidence(
        evidence_id=evidence_id, actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id, operation=operation,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def create_persistent_world_object_open_state(
    *, object_entity_id: str, state: str,
) -> PersistentWorldObjectOpenState:
    return PersistentWorldObjectOpenState(object_entity_id=object_entity_id, state=state)


def create_persistent_world_object_open_close_runtime_state(
    *, custody_state: PersistentWorldObjectCustodyRuntimeState,
    object_open_states: Sequence[PersistentWorldObjectOpenState] = (),
) -> PersistentWorldObjectOpenCloseRuntimeState:
    return PersistentWorldObjectOpenCloseRuntimeState(
        custody_state=custody_state, object_open_states=tuple(object_open_states),
    )


def replace_persistent_world_object_open_close_custody_state(
    *, state: PersistentWorldObjectOpenCloseRuntimeState,
    custody_state: PersistentWorldObjectCustodyRuntimeState,
) -> PersistentWorldObjectOpenCloseRuntimeState:
    if not isinstance(state, PersistentWorldObjectOpenCloseRuntimeState):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "state must be PersistentWorldObjectOpenCloseRuntimeState"
        )
    return PersistentWorldObjectOpenCloseRuntimeState(
        custody_state=custody_state,
        object_open_states=state.object_open_states,
        committed_object_state_transitions=state.committed_object_state_transitions,
    )


def object_open_state_for(
    state: PersistentWorldObjectOpenCloseRuntimeState,
    object_entity_id: str,
) -> PersistentWorldObjectOpenState | None:
    for item in state.object_open_states:
        if item.object_entity_id == object_entity_id:
            return item
    return None


def serialize_persistent_world_object_open_state(
    state: PersistentWorldObjectOpenState,
) -> dict[str, str]:
    if not isinstance(state, PersistentWorldObjectOpenState):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "state must be PersistentWorldObjectOpenState"
        )
    return state.to_dict()


def canonical_serialize_persistent_world_object_open_states(
    object_open_states: Sequence[PersistentWorldObjectOpenState],
) -> str:
    states = tuple(sorted(object_open_states, key=lambda item: item.object_entity_id))
    material = {
        "state_family": "rt010_object_open_close",
        "object_open_states": [serialize_persistent_world_object_open_state(x) for x in states],
    }
    return json.dumps(
        material, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def digest_persistent_world_object_open_states(
    object_open_states: Sequence[PersistentWorldObjectOpenState],
) -> str:
    return hashlib.sha256(
        canonical_serialize_persistent_world_object_open_states(
            object_open_states
        ).encode("utf-8")
    ).hexdigest()


def digest_persistent_world_composite_state(
    representation: PersistentWorldEntityLocationRepresentation,
    object_open_states: Sequence[PersistentWorldObjectOpenState],
) -> str:
    material = {
        "world_state_family": "persistent_world_location_custody_plus_open_close",
        "representation_digest": digest_persistent_world_entity_location_representation(
            representation
        ),
        "object_state_digest": digest_persistent_world_object_open_states(
            object_open_states
        ),
    }
    canonical = json.dumps(
        material, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def digest_persistent_world_object_open_close_runtime_state(
    state: PersistentWorldObjectOpenCloseRuntimeState,
) -> str:
    if not isinstance(state, PersistentWorldObjectOpenCloseRuntimeState):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "state must be PersistentWorldObjectOpenCloseRuntimeState"
        )
    return digest_persistent_world_composite_state(
        state.custody_state.movement_state.representation,
        state.object_open_states,
    )


def fingerprint_persistent_world_object_open_close_command(
    command: CommandEnvelope,
) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "command failed CommandEnvelope validation"
        )
    return fingerprint_command_envelope(command, allow_nan=False)


def _operation_from_command(command: CommandEnvelope) -> str:
    normalized = command.command_type.strip().lower().replace("-", "_")
    first = normalized.split("_", 1)[0]
    if first in OBJECT_OPEN_CLOSE_OPERATIONS:
        return first
    raise InvalidPersistentWorldObjectOpenCloseRequestError(
        "INT-1 supports only open/close object commands"
    )


def _validate_owner_evidence(
    *, qualification_evidence: ObjectOpenCloseQualificationEvidence,
    opportunity_evidence: ObjectOpenCloseOpportunityEvidence,
    actor_entity_id: str, object_entity_id: str, operation: str,
) -> None:
    if not isinstance(qualification_evidence, ObjectOpenCloseQualificationEvidence):
        raise PersistentWorldObjectOpenCloseEvidenceError(
            "invalid RT-010 qualification evidence"
        )
    if not isinstance(opportunity_evidence, ObjectOpenCloseOpportunityEvidence):
        raise PersistentWorldObjectOpenCloseEvidenceError(
            "invalid AFQR-19 opportunity evidence"
        )
    for evidence in (qualification_evidence, opportunity_evidence):
        if (
            evidence.actor_entity_id != actor_entity_id
            or evidence.object_entity_id != object_entity_id
            or evidence.operation != operation
        ):
            raise PersistentWorldObjectOpenCloseEvidenceError(
                "owner evidence does not match actor/object/operation"
            )
    if not qualification_evidence.qualified:
        raise PersistentWorldObjectOpenCloseEvidenceError(
            "RT-010 rejected object-state transition"
        )
    if (
        not opportunity_evidence.opportunity_available
        or not opportunity_evidence.resolution_accepted
    ):
        raise PersistentWorldObjectOpenCloseEvidenceError(
            "AFQR-19 rejected object-state transition"
        )


def _validate_current_availability(
    *, representation: PersistentWorldEntityLocationRepresentation,
    actor_entity_id: str, object_entity_id: str,
) -> None:
    entities = {entity.entity_id: entity for entity in representation.entities}
    actor = entities.get(actor_entity_id)
    target = entities.get(object_entity_id)
    if actor is None or actor.classification != "character_or_creature":
        raise PersistentWorldObjectOpenCloseEntityError(
            "actor must exist and be character_or_creature"
        )
    if target is None or target.classification != "object":
        raise PersistentWorldObjectOpenCloseEntityError(
            "target must exist and be object"
        )
    actor_locations = [
        relation for relation in representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == actor_entity_id
    ]
    if len(actor_locations) != 1:
        raise PersistentWorldObjectOpenClosePlacementError(
            "actor requires exactly one current location"
        )
    place_id = actor_locations[0].object_entity_id
    nearby = any(
        relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
        and relation.object_entity_id == place_id
        for relation in representation.relations
    )
    carried = any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
        and relation.object_entity_id == actor_entity_id
        for relation in representation.relations
    )
    if not (nearby or carried):
        raise PersistentWorldObjectOpenClosePlacementError(
            "target must be nearby or carried by the actor"
        )


def persistent_world_object_open_close_opportunity_available(
    *, state: PersistentWorldObjectOpenCloseRuntimeState,
    actor_entity_id: str, object_entity_id: str,
) -> bool:
    """Return current bounded physical opportunity without mutating state."""
    if not isinstance(state, PersistentWorldObjectOpenCloseRuntimeState):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "state must be PersistentWorldObjectOpenCloseRuntimeState"
        )
    if object_open_state_for(state, object_entity_id) is None:
        return False
    try:
        _validate_current_availability(
            representation=state.custody_state.movement_state.representation,
            actor_entity_id=actor_entity_id,
            object_entity_id=object_entity_id,
        )
    except (
        PersistentWorldObjectOpenCloseEntityError,
        PersistentWorldObjectOpenClosePlacementError,
    ):
        return False
    return True


def _replace_open_state(
    object_open_states: Sequence[PersistentWorldObjectOpenState],
    *, object_entity_id: str, new_state: str,
) -> tuple[PersistentWorldObjectOpenState, ...]:
    found = False
    updated = []
    for item in object_open_states:
        if item.object_entity_id == object_entity_id:
            found = True
            updated.append(PersistentWorldObjectOpenState(
                object_entity_id=object_entity_id, state=new_state,
            ))
        else:
            updated.append(item)
    if not found:
        raise PersistentWorldObjectOpenCloseUnsupportedStateError(
            "target has no bounded open/closed state"
        )
    return tuple(sorted(updated, key=lambda item: item.object_entity_id))


def prepare_persistent_world_object_open_close(
    *, state: PersistentWorldObjectOpenCloseRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectOpenCloseQualificationEvidence,
    opportunity_evidence: ObjectOpenCloseOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectOpenClosePreparedTransition:
    if not isinstance(state, PersistentWorldObjectOpenCloseRuntimeState):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "invalid object open/close runtime state"
        )
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "invalid command envelope"
        )

    fingerprint = fingerprint_persistent_world_object_open_close_command(command)
    routing = route_command_envelope(
        request_ref=build_record_id("object_state_request", fingerprint[:24]),
        command_envelope=command,
    )
    if routing.classification.family != "interaction":
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "open/close command must route through interaction family"
        )

    operation = _operation_from_command(command)
    actor_entity_id = command.source_actor_id
    object_entity_id = _require_record_id(
        command.payload.get("object_entity_id"),
        "command.payload.object_entity_id",
    )
    representation = state.custody_state.movement_state.representation
    _validate_current_availability(
        representation=representation,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
    )

    current = object_open_state_for(state, object_entity_id)
    if current is None:
        raise PersistentWorldObjectOpenCloseUnsupportedStateError(
            "target has no bounded open/closed state"
        )

    _validate_owner_evidence(
        qualification_evidence=qualification_evidence,
        opportunity_evidence=opportunity_evidence,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
    )

    actual_state_digest = digest_persistent_world_object_open_states(
        state.object_open_states
    )
    if expected_pre_state_digest != actual_state_digest:
        raise PersistentWorldObjectOpenCloseStaleStateError(
            "owner-local object state changed before preparation"
        )

    desired = "open" if operation == "open" else "closed"
    if current.state == desired:
        raise PersistentWorldObjectOpenCloseNoChangeError(
            f"target is already {desired}"
        )

    post_states = _replace_open_state(
        state.object_open_states,
        object_entity_id=object_entity_id,
        new_state=desired,
    )
    post_state_digest = digest_persistent_world_object_open_states(post_states)
    placement_digest = digest_persistent_world_entity_location_representation(
        representation
    )
    token = fingerprint[:24]
    preview = create_transaction_preview(
        preview_id=build_record_id("object_state_preview", token),
        command=command,
        status="preview_created",
        messages=("bounded persistent object open/close state prepared",),
        requires_confirmation=False,
        metadata={
            "package": "TERMINAL-PLAY-INT-1",
            "command_family": "interaction",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("object_state_delta", token),
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(actor_entity_id, object_entity_id),
        change_type="record_update",
        payload={
            "operation": operation,
            "actor_entity_id": actor_entity_id,
            "object_entity_id": object_entity_id,
            "pre_object_state": current.state,
            "post_object_state": desired,
        },
        metadata={
            "package": "TERMINAL-PLAY-INT-1",
            "asset_state_semantic_owner": RT010_OBJECT_OPEN_CLOSE_OWNER,
            "opportunity_semantic_owner": AFQR19_OBJECT_OPEN_CLOSE_OPPORTUNITY_OWNER,
            "qualified_transition_owner": "AFQR-01",
        },
    )
    return PersistentWorldObjectOpenClosePreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        pre_object_state=current.state,
        post_object_state=desired,
        pre_state_digest=actual_state_digest,
        post_state_digest=post_state_digest,
        placement_digest=placement_digest,
        rt010_qualification_id=qualification_evidence.evidence_id,
        opportunity_evidence_id=opportunity_evidence.evidence_id,
        preview=preview,
        state_delta=delta,
        post_object_open_states=post_states,
    )


def _commit_new_persistent_world_object_open_close(
    *, state: PersistentWorldObjectOpenCloseRuntimeState,
    prepared: PersistentWorldObjectOpenClosePreparedTransition,
) -> PersistentWorldObjectOpenCloseExecutionResult:
    if (
        digest_persistent_world_object_open_states(state.object_open_states)
        != prepared.pre_state_digest
    ):
        raise PersistentWorldObjectOpenCloseStaleStateError(
            "owner-local object state changed after preparation"
        )
    if (
        digest_persistent_world_entity_location_representation(
            state.custody_state.movement_state.representation
        )
        != prepared.placement_digest
    ):
        raise PersistentWorldObjectOpenCloseStaleStateError(
            "target placement changed after preparation"
        )

    receipt = PersistentWorldObjectOpenCloseCommitReceipt(
        receipt_id=build_record_id("object_state_receipt", prepared.command_fingerprint[:24]),
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        actor_entity_id=prepared.actor_entity_id,
        object_entity_id=prepared.object_entity_id,
        operation=prepared.operation,
        pre_object_state=prepared.pre_object_state,
        post_object_state=prepared.post_object_state,
        pre_state_digest=prepared.pre_state_digest,
        post_state_digest=prepared.post_state_digest,
        placement_digest=prepared.placement_digest,
        preview_id=prepared.preview.preview_id,
        state_delta_id=prepared.state_delta.delta_id,
        rt010_qualification_id=prepared.rt010_qualification_id,
        opportunity_evidence_id=prepared.opportunity_evidence_id,
    )
    committed = PersistentWorldObjectOpenCloseCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    post_state = PersistentWorldObjectOpenCloseRuntimeState(
        custody_state=state.custody_state,
        object_open_states=prepared.post_object_open_states,
        committed_object_state_transitions=(
            *state.committed_object_state_transitions, committed,
        ),
    )
    return PersistentWorldObjectOpenCloseExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def commit_prepared_persistent_world_object_open_close(
    *, state: PersistentWorldObjectOpenCloseRuntimeState,
    prepared: PersistentWorldObjectOpenClosePreparedTransition,
) -> PersistentWorldObjectOpenCloseExecutionResult:
    if not isinstance(state, PersistentWorldObjectOpenCloseRuntimeState):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "invalid object open/close runtime state"
        )
    if not isinstance(prepared, PersistentWorldObjectOpenClosePreparedTransition):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "invalid prepared transition"
        )
    return commit_prepared_capability_transition(
        spec=OPEN_CLOSE_TRANSITION_CAPABILITY_SPEC,
        state=state,
        prepared=prepared,
    )


def execute_persistent_world_object_open_close(
    *, state: PersistentWorldObjectOpenCloseRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectOpenCloseQualificationEvidence,
    opportunity_evidence: ObjectOpenCloseOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectOpenCloseExecutionResult:
    if not isinstance(state, PersistentWorldObjectOpenCloseRuntimeState):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "invalid object open/close runtime state"
        )
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


def replay_persistent_world_object_open_close_states(
    *, object_open_states: Sequence[PersistentWorldObjectOpenState],
    receipt: PersistentWorldObjectOpenCloseCommitReceipt,
) -> tuple[PersistentWorldObjectOpenState, ...]:
    if not isinstance(receipt, PersistentWorldObjectOpenCloseCommitReceipt):
        raise PersistentWorldObjectOpenCloseReplayError("receipt has invalid type")
    current = tuple(object_open_states)
    if digest_persistent_world_object_open_states(current) != receipt.pre_state_digest:
        raise PersistentWorldObjectOpenCloseReplayError("replay pre-state digest mismatch")
    existing = next(
        (item for item in current if item.object_entity_id == receipt.object_entity_id),
        None,
    )
    if existing is None or existing.state != receipt.pre_object_state:
        raise PersistentWorldObjectOpenCloseReplayError(
            "replay object state disagrees with receipt"
        )
    post = _replace_open_state(
        current,
        object_entity_id=receipt.object_entity_id,
        new_state=receipt.post_object_state,
    )
    if digest_persistent_world_object_open_states(post) != receipt.post_state_digest:
        raise PersistentWorldObjectOpenCloseReplayError("replay post-state digest mismatch")
    return post


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
    prepare_new_transition=lambda state, command, context: prepare_persistent_world_object_open_close(
        state=state,
        command=command,
        qualification_evidence=context["qualification_evidence"],
        opportunity_evidence=context["opportunity_evidence"],
        expected_pre_state_digest=context["expected_pre_state_digest"],
    ),
    commit_new_transition=lambda state, prepared: _commit_new_persistent_world_object_open_close(
        state=state, prepared=prepared,
    ),
    build_retry_result=lambda state, committed: PersistentWorldObjectOpenCloseExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    ),
    retry_conflict_error=lambda message: PersistentWorldObjectOpenCloseRetryConflictError(message),
    replay_committed_transition=lambda pre_state, receipt: replay_persistent_world_object_open_close_states(
        object_open_states=pre_state, receipt=receipt,
    ),
)


def replay_persistent_world_object_open_close_transition_history(
    *, object_open_states: Sequence[PersistentWorldObjectOpenState],
    committed_transitions: Sequence[PersistentWorldObjectOpenCloseCommittedTransition],
) -> tuple[PersistentWorldObjectOpenState, ...]:
    """Replay complete INT-1 evidence without treating storage order as causal."""
    current = tuple(object_open_states)
    transitions = tuple(committed_transitions)
    for transition in transitions:
        if not isinstance(transition, PersistentWorldObjectOpenCloseCommittedTransition):
            raise PersistentWorldObjectOpenCloseReplayError(
                "transition history contains an invalid transition"
            )
    command_ids = [transition.command_id for transition in transitions]
    if len(command_ids) != len(set(command_ids)):
        raise PersistentWorldObjectOpenCloseReplayError(
            "transition history contains duplicate command identity"
        )
    if not transitions:
        return current

    adjacency: dict[str, list[PersistentWorldObjectOpenCloseCommittedTransition]] = {}
    for transition in transitions:
        adjacency.setdefault(transition.receipt.pre_state_digest, []).append(transition)
    for candidates in adjacency.values():
        candidates.sort(
            key=lambda item: (item.command_id, item.command_fingerprint),
            reverse=True,
        )

    start_digest = digest_persistent_world_object_open_states(current)
    vertex_stack = [start_digest]
    edge_stack: list[PersistentWorldObjectOpenCloseCommittedTransition] = []
    reverse_path: list[PersistentWorldObjectOpenCloseCommittedTransition] = []
    while vertex_stack:
        candidates = adjacency.get(vertex_stack[-1])
        if candidates:
            transition = candidates.pop()
            vertex_stack.append(transition.receipt.post_state_digest)
            edge_stack.append(transition)
            continue
        vertex_stack.pop()
        if edge_stack:
            reverse_path.append(edge_stack.pop())

    replay_path = tuple(reversed(reverse_path))
    if len(replay_path) != len(transitions):
        raise PersistentWorldObjectOpenCloseReplayError(
            "transition history is disconnected from the accepted initial state"
        )
    replayed = current
    for transition in replay_path:
        replayed = replay_persistent_world_object_open_close_states(
            object_open_states=replayed,
            receipt=transition.receipt,
        )
    return replayed


def serialize_persistent_world_object_open_close_commit_receipt(
    receipt: PersistentWorldObjectOpenCloseCommitReceipt,
) -> dict[str, str]:
    if not isinstance(receipt, PersistentWorldObjectOpenCloseCommitReceipt):
        raise InvalidPersistentWorldObjectOpenCloseRequestError(
            "receipt must be PersistentWorldObjectOpenCloseCommitReceipt"
        )
    return receipt.to_dict()


# B-2a bounded asset condition: deliberately alongside the existing RT-010
# asset-state owner, not a new root domain module or universal labor manager.
SERVICE_OWNER = "RT-010/AFQR-16"
SERVICE_PROFILE = "myravant-b2a-tool-chest-latch-v1"
OPERATIONS = frozenset({"work", "abandon", "secure", "release"})
METHODS = frozenset({"manual", "lantern", "none"})


class FixtureServiceError(ValueError):
    """Unqualified, stale or inconsistent fixture service action."""


def _digest(material: object) -> str:
    return hashlib.sha256(json.dumps(
        material, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FixtureServiceEvent:
    command_id: str
    operation: str
    method: str
    actor_id: str
    target_id: str
    place_id: str
    logical_before: int
    logical_after: int
    time_receipt_id: str
    pre_progress: int
    post_progress: int
    pre_abandoned: bool
    post_abandoned: bool
    pre_secured: bool
    post_secured: bool
    pre_digest: str
    post_digest: str
    fingerprint: str
    preview_id: str
    receipt_id: str
    state_delta_id: str


@dataclass(frozen=True)
class FixtureServiceState:
    progress: int = 0
    abandoned: bool = False
    secured: bool = False
    events: tuple[FixtureServiceEvent, ...] = ()

    def __post_init__(self) -> None:
        if type(self.progress) is not int or not 0 <= self.progress <= 2:
            raise FixtureServiceError("service progress must be 0..2")
        if type(self.abandoned) is not bool or type(self.secured) is not bool:
            raise FixtureServiceError("service status flags must be boolean")
        if self.secured and (self.progress != 2 or self.abandoned):
            raise FixtureServiceError("unserviceable latch cannot be secured")
        if self.abandoned and self.progress in (0, 2):
            raise FixtureServiceError("only incomplete invested work can be abandoned")
        if any(not isinstance(x, FixtureServiceEvent) for x in self.events):
            raise FixtureServiceError("invalid service transition history")
        if len({x.command_id for x in self.events}) != len(self.events):
            raise FixtureServiceError("duplicate service command identity")


def digest_fixture_service_state(state: FixtureServiceState) -> str:
    return _digest({
        "family": SERVICE_PROFILE,
        "progress": state.progress,
        "abandoned": state.abandoned,
        "secured": state.secured,
    })


def _transition(
    state: FixtureServiceState, operation: str, method: str
) -> tuple[int, bool, bool]:
    if operation == "work":
        if state.progress == 2:
            raise FixtureServiceError("fixture service is already complete")
        if method not in {"manual", "lantern"}:
            raise FixtureServiceError("service work method is unqualified")
        return min(2, state.progress + (2 if method == "lantern" else 1)), False, False
    if method != "none":
        raise FixtureServiceError("this operation does not admit a work method")
    if operation == "abandon":
        if state.progress not in (1,) or state.abandoned:
            raise FixtureServiceError("no active unfinished work can be abandoned")
        return state.progress, True, False
    if operation == "secure":
        if state.progress != 2 or state.secured:
            raise FixtureServiceError("the latch is not serviceable or already secured")
        return state.progress, False, True
    if operation == "release":
        if not state.secured:
            raise FixtureServiceError("the latch is not secured")
        return state.progress, False, False
    raise FixtureServiceError("unsupported fixture service operation")


def execute_fixture_service(
    *, state: FixtureServiceState, command_id: str, operation: str,
    method: str, actor_id: str, target_id: str, place_id: str,
    logical_before: int, logical_after: int, time_receipt_id: str,
    qualified: bool, expected_pre_digest: str,
):
    """Commit one qualified service change; return state, event, preview, delta.

    A work contribution requires a separately committed AFQR-04 time receipt
    covering exactly one logical step. Status/custody commands cost no time.
    The caller validates actor, location, availability and optional lit lantern.
    """
    if not qualified:
        raise FixtureServiceError("service opportunity was not qualified")
    if not command_id or not actor_id or not target_id or not place_id:
        raise FixtureServiceError("service command context is incomplete")
    if type(logical_before) is not int or logical_before < 0:
        raise FixtureServiceError("invalid logical position")
    cost = 1 if operation == "work" else 0
    if logical_after != logical_before + cost:
        raise FixtureServiceError("labor time does not match AFQR-04")
    if (cost == 1) != bool(time_receipt_id):
        raise FixtureServiceError("time receipt mismatch")
    immutable = {
        "profile": SERVICE_PROFILE, "command_id": command_id,
        "operation": operation, "method": method,
        "actor_id": actor_id, "target_id": target_id,
        "place_id": place_id, "logical_before": logical_before,
        "logical_after": logical_after, "time_receipt_id": time_receipt_id,
    }
    fingerprint = _digest(immutable)
    for existing in state.events:
        if existing.command_id == command_id:
            if existing.fingerprint != fingerprint:
                raise FixtureServiceError("conflicting service command retry")
            return state, existing, None, None
    if digest_fixture_service_state(state) != expected_pre_digest:
        raise FixtureServiceError("stale fixture service state")
    progress, abandoned, secured = _transition(state, operation, method)
    post = FixtureServiceState(
        progress=progress, abandoned=abandoned, secured=secured,
        events=state.events,
    )
    token = fingerprint[:24]
    command = create_command_envelope(
        command_id=command_id, command_type="interact",
        source_actor_id=actor_id,
        payload={"target_id": target_id, "operation": operation, "method": method},
        metadata={"package": "PLAY-UNDERTAKINGS-B2A", "profile": SERVICE_PROFILE},
    )
    preview = create_transaction_preview(
        preview_id=build_record_id("work_preview", token),
        command=command, status="preview_created",
        messages=("bounded asset servicing prepared",),
        requires_confirmation=False,
        metadata={"package": "PLAY-UNDERTAKINGS-B2A",
                  "semantic_owner": SERVICE_OWNER, "mutation_performed": False},
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("work_delta", token),
        source_command_id=command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(target_id,),
        change_type="record_update",
        payload={
            "profile": SERVICE_PROFILE,
            "operation": operation, "method": method,
            "pre_progress": state.progress, "post_progress": progress,
            "pre_abandoned": state.abandoned, "post_abandoned": abandoned,
            "pre_secured": state.secured, "post_secured": secured,
            "logical_before": logical_before, "logical_after": logical_after,
            "time_receipt_id": time_receipt_id,
        },
        metadata={"asset_owner": SERVICE_OWNER,
                  "opportunity_owner": "AFQR-19",
                  "transition_owner": "AFQR-01"},
    )
    event = FixtureServiceEvent(
        command_id=command_id, operation=operation, method=method,
        actor_id=actor_id, target_id=target_id, place_id=place_id,
        logical_before=logical_before, logical_after=logical_after,
        time_receipt_id=time_receipt_id, pre_progress=state.progress,
        post_progress=progress, pre_abandoned=state.abandoned,
        post_abandoned=abandoned, pre_secured=state.secured,
        post_secured=secured, pre_digest=expected_pre_digest,
        post_digest=digest_fixture_service_state(post), fingerprint=fingerprint,
        preview_id=preview.preview_id,
        receipt_id=build_record_id("work_receipt", token),
        state_delta_id=delta.delta_id,
    )
    return replace(post, events=(*state.events, event)), event, preview, delta


def restore_fixture_service(material: object) -> FixtureServiceState:
    """Rebuild every authoritative bit from serializable committed events."""
    if type(material) is not dict or set(material) != {
        "profile", "progress", "abandoned", "secured", "events",
    } or material["profile"] != SERVICE_PROFILE or type(material["events"]) is not list:
        raise FixtureServiceError("invalid fixture service checkpoint component")
    state = FixtureServiceState()
    event_keys = set(FixtureServiceEvent.__dataclass_fields__)
    for item in material["events"]:
        if type(item) is not dict or set(item) != event_keys:
            raise FixtureServiceError("malformed service event")
        try:
            saved = FixtureServiceEvent(**item)
            state, computed, _, _ = execute_fixture_service(
                state=state, command_id=saved.command_id,
                operation=saved.operation, method=saved.method,
                actor_id=saved.actor_id, target_id=saved.target_id,
                place_id=saved.place_id, logical_before=saved.logical_before,
                logical_after=saved.logical_after,
                time_receipt_id=saved.time_receipt_id, qualified=True,
                expected_pre_digest=digest_fixture_service_state(state),
            )
        except (TypeError, ValueError) as exc:
            raise FixtureServiceError("service transition replay failed") from exc
        if computed != saved:
            raise FixtureServiceError("service transition provenance diverged")
    if (material["progress"], material["abandoned"], material["secured"]) != (
        state.progress, state.abandoned, state.secured,
    ):
        raise FixtureServiceError("service state differs from replay")
    return state


def serialize_fixture_service(state: FixtureServiceState) -> dict[str, object]:
    return {
        "profile": SERVICE_PROFILE, "progress": state.progress,
        "abandoned": state.abandoned, "secured": state.secured,
        "events": [asdict(x) for x in state.events],
    }
