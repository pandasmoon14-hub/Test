"""Bounded persistent Brass Lantern lit/unlit state for TERMINAL-PLAY-INT-2.

This module proves a second narrow persistent asset-state family. It composes
TERMINAL-PLAY-INT-1 open/close state without merging the two vocabularies or
creating a generic property/state manager.

Authority remains routed to existing owners:
* RT-010: bounded asset lit-state semantics
* AFQR-19: target/opportunity qualification
* AFQR-01: qualified transition commitment
* AFQR-02: command identity/retry behavior through CommandEnvelope identity

This is not illumination, visibility, fuel, heat, fire propagation, durability,
an effect engine, a generic activation system, or a property bag.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Sequence

from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntityLocationRepresentation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseRuntimeState,
    digest_persistent_world_object_open_close_runtime_state,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope, validate_command_envelope
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope, create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import TransactionPreview, create_transaction_preview


RT010_OBJECT_LIT_STATE_OWNER = "RT-010"
AFQR19_OBJECT_LIT_STATE_OPPORTUNITY_OWNER = "AFQR-19"
OBJECT_LIT_STATES = frozenset({"unlit", "lit"})
OBJECT_LIT_OPERATIONS = frozenset({"light", "extinguish"})
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PersistentWorldObjectLitStateError(ValueError):
    pass


class InvalidPersistentWorldObjectLitStateRequestError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStateEntityError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStatePlacementError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStateEvidenceError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStateUnsupportedError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStateNoChangeError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStateStaleStateError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStateRetryConflictError(PersistentWorldObjectLitStateError):
    pass


class PersistentWorldObjectLitStateReplayError(PersistentWorldObjectLitStateError):
    pass


def _require_record_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            f"{label} must be a valid record ID"
        )
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise InvalidPersistentWorldObjectLitStateRequestError(
            f"{label} must be a lowercase SHA-256 digest"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class ObjectLitStateQualificationEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    qualified: bool
    semantic_owner: str = RT010_OBJECT_LIT_STATE_OWNER

    def __post_init__(self) -> None:
        for name in ("evidence_id", "actor_entity_id", "object_entity_id"):
            _require_record_id(getattr(self, name), name)
        if self.operation not in OBJECT_LIT_OPERATIONS:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "operation must be light or extinguish"
            )
        if type(self.qualified) is not bool:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "qualified must be bool"
            )
        if self.semantic_owner != RT010_OBJECT_LIT_STATE_OWNER:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "qualification semantic_owner must be RT-010"
            )


@dataclass(frozen=True, kw_only=True)
class ObjectLitStateOpportunityEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_OBJECT_LIT_STATE_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        for name in ("evidence_id", "actor_entity_id", "object_entity_id"):
            _require_record_id(getattr(self, name), name)
        if self.operation not in OBJECT_LIT_OPERATIONS:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "operation must be light or extinguish"
            )
        if type(self.opportunity_available) is not bool:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "opportunity_available must be bool"
            )
        if type(self.resolution_accepted) is not bool:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "resolution_accepted must be bool"
            )
        if self.semantic_owner != AFQR19_OBJECT_LIT_STATE_OPPORTUNITY_OWNER:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "opportunity semantic_owner must be AFQR-19"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectLitState:
    object_entity_id: str
    state: str
    semantic_owner: str = RT010_OBJECT_LIT_STATE_OWNER

    def __post_init__(self) -> None:
        _require_record_id(self.object_entity_id, "object_entity_id")
        if self.state not in OBJECT_LIT_STATES:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "state must be unlit or lit"
            )
        if self.semantic_owner != RT010_OBJECT_LIT_STATE_OWNER:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "lit-state semantic_owner must be RT-010"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "object_entity_id": self.object_entity_id,
            "state": self.state,
            "semantic_owner": self.semantic_owner,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectLitStateCommitReceipt:
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
            "receipt_id",
            "actor_entity_id",
            "object_entity_id",
            "preview_id",
            "state_delta_id",
            "rt010_qualification_id",
            "opportunity_evidence_id",
        ):
            _require_record_id(getattr(self, name), name)
        if not isinstance(self.command_id, str) or not self.command_id.strip():
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "command_id must be non-empty"
            )
        _require_sha256(self.command_fingerprint, "command_fingerprint")
        _require_sha256(self.pre_state_digest, "pre_state_digest")
        _require_sha256(self.post_state_digest, "post_state_digest")
        _require_sha256(self.placement_digest, "placement_digest")
        if self.operation not in OBJECT_LIT_OPERATIONS:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "operation must be light or extinguish"
            )
        expected = ("unlit", "lit") if self.operation == "light" else ("lit", "unlit")
        if (self.pre_object_state, self.post_object_state) != expected:
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "receipt object states disagree with operation"
            )
        if self.status != "committed":
            raise InvalidPersistentWorldObjectLitStateRequestError(
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
class PersistentWorldObjectLitStateCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldObjectLitStateCommitReceipt


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectLitRuntimeState:
    open_close_state: PersistentWorldObjectOpenCloseRuntimeState
    object_lit_states: tuple[PersistentWorldObjectLitState, ...] = ()
    committed_object_lit_transitions: tuple[
        PersistentWorldObjectLitStateCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.open_close_state, PersistentWorldObjectOpenCloseRuntimeState):
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "open_close_state must be PersistentWorldObjectOpenCloseRuntimeState"
            )
        states = tuple(sorted(self.object_lit_states, key=lambda item: item.object_entity_id))
        for item in states:
            if not isinstance(item, PersistentWorldObjectLitState):
                raise InvalidPersistentWorldObjectLitStateRequestError(
                    "object_lit_states contains an invalid value"
                )
        ids = [item.object_entity_id for item in states]
        if len(ids) != len(set(ids)):
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "object_lit_states must have unique object_entity_id values"
            )
        representation = self.open_close_state.custody_state.movement_state.representation
        entity_by_id = {entity.entity_id: entity for entity in representation.entities}
        for object_entity_id in ids:
            entity = entity_by_id.get(object_entity_id)
            if entity is None or entity.classification != "object":
                raise PersistentWorldObjectLitStateEntityError(
                    "lit-state target must exist and be classified as object"
                )

        transitions = tuple(sorted(
            self.committed_object_lit_transitions,
            key=lambda item: (item.command_id, item.command_fingerprint),
        ))
        for transition in transitions:
            if not isinstance(transition, PersistentWorldObjectLitStateCommittedTransition):
                raise InvalidPersistentWorldObjectLitStateRequestError(
                    "committed_object_lit_transitions contains an invalid value"
                )
        command_ids = [item.command_id for item in transitions]
        if len(command_ids) != len(set(command_ids)):
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "lit-state command IDs must be unique"
            )
        movement_ids = {
            item.command_id
            for item in self.open_close_state.custody_state.movement_state.committed_transitions
        }
        custody_ids = {
            item.command_id
            for item in self.open_close_state.custody_state.committed_custody_transitions
        }
        open_close_ids = {
            item.command_id
            for item in self.open_close_state.committed_object_state_transitions
        }
        if set(command_ids) & (movement_ids | custody_ids | open_close_ids):
            raise InvalidPersistentWorldObjectLitStateRequestError(
                "lit-state command IDs must not collide with lower-layer transitions"
            )
        object.__setattr__(self, "object_lit_states", states)
        object.__setattr__(self, "committed_object_lit_transitions", transitions)


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectLitStatePreparedTransition:
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
    post_object_lit_states: tuple[PersistentWorldObjectLitState, ...]


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectLitStateExecutionResult:
    state: PersistentWorldObjectLitRuntimeState
    receipt: PersistentWorldObjectLitStateCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_object_lit_state_qualification_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    operation: str, qualified: bool,
) -> ObjectLitStateQualificationEvidence:
    return ObjectLitStateQualificationEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        qualified=qualified,
    )


def create_object_lit_state_opportunity_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    operation: str, opportunity_available: bool, resolution_accepted: bool,
) -> ObjectLitStateOpportunityEvidence:
    return ObjectLitStateOpportunityEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def create_persistent_world_object_lit_state(
    *, object_entity_id: str, state: str,
) -> PersistentWorldObjectLitState:
    return PersistentWorldObjectLitState(
        object_entity_id=object_entity_id,
        state=state,
    )


def create_persistent_world_object_lit_runtime_state(
    *, open_close_state: PersistentWorldObjectOpenCloseRuntimeState,
    object_lit_states: Sequence[PersistentWorldObjectLitState] = (),
) -> PersistentWorldObjectLitRuntimeState:
    return PersistentWorldObjectLitRuntimeState(
        open_close_state=open_close_state,
        object_lit_states=tuple(object_lit_states),
    )


def replace_persistent_world_object_lit_open_close_state(
    *, state: PersistentWorldObjectLitRuntimeState,
    open_close_state: PersistentWorldObjectOpenCloseRuntimeState,
) -> PersistentWorldObjectLitRuntimeState:
    if not isinstance(state, PersistentWorldObjectLitRuntimeState):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "state must be PersistentWorldObjectLitRuntimeState"
        )
    return PersistentWorldObjectLitRuntimeState(
        open_close_state=open_close_state,
        object_lit_states=state.object_lit_states,
        committed_object_lit_transitions=state.committed_object_lit_transitions,
    )


def object_lit_state_for(
    state: PersistentWorldObjectLitRuntimeState,
    object_entity_id: str,
) -> PersistentWorldObjectLitState | None:
    for item in state.object_lit_states:
        if item.object_entity_id == object_entity_id:
            return item
    return None


def serialize_persistent_world_object_lit_state(
    state: PersistentWorldObjectLitState,
) -> dict[str, str]:
    if not isinstance(state, PersistentWorldObjectLitState):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "state must be PersistentWorldObjectLitState"
        )
    return state.to_dict()


def canonical_serialize_persistent_world_object_lit_states(
    object_lit_states: Sequence[PersistentWorldObjectLitState],
) -> str:
    states = tuple(sorted(object_lit_states, key=lambda item: item.object_entity_id))
    material = {
        "state_family": "rt010_object_lit_state",
        "object_lit_states": [serialize_persistent_world_object_lit_state(x) for x in states],
    }
    return json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def digest_persistent_world_object_lit_states(
    object_lit_states: Sequence[PersistentWorldObjectLitState],
) -> str:
    return hashlib.sha256(
        canonical_serialize_persistent_world_object_lit_states(
            object_lit_states
        ).encode("utf-8")
    ).hexdigest()


def digest_persistent_world_lit_composite_state(
    open_close_state: PersistentWorldObjectOpenCloseRuntimeState,
    object_lit_states: Sequence[PersistentWorldObjectLitState],
) -> str:
    material = {
        "world_state_family": "persistent_world_int1_plus_lit_state",
        "int1_world_state_digest": (
            digest_persistent_world_object_open_close_runtime_state(open_close_state)
        ),
        "object_lit_state_digest": digest_persistent_world_object_lit_states(
            object_lit_states
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


def digest_persistent_world_object_lit_runtime_state(
    state: PersistentWorldObjectLitRuntimeState,
) -> str:
    if not isinstance(state, PersistentWorldObjectLitRuntimeState):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "state must be PersistentWorldObjectLitRuntimeState"
        )
    return digest_persistent_world_lit_composite_state(
        state.open_close_state,
        state.object_lit_states,
    )


def fingerprint_persistent_world_object_lit_state_command(
    command: CommandEnvelope,
) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "command failed CommandEnvelope validation"
        )
    canonical = json.dumps(
        command.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _operation_from_command(command: CommandEnvelope) -> str:
    operation = command.payload.get("operation")
    if operation in OBJECT_LIT_OPERATIONS:
        return operation
    raise InvalidPersistentWorldObjectLitStateRequestError(
        "INT-2 supports only light/extinguish object operations"
    )


def _validate_owner_evidence(
    *, qualification_evidence: ObjectLitStateQualificationEvidence,
    opportunity_evidence: ObjectLitStateOpportunityEvidence,
    actor_entity_id: str, object_entity_id: str, operation: str,
) -> None:
    if not isinstance(qualification_evidence, ObjectLitStateQualificationEvidence):
        raise PersistentWorldObjectLitStateEvidenceError(
            "invalid RT-010 qualification evidence"
        )
    if not isinstance(opportunity_evidence, ObjectLitStateOpportunityEvidence):
        raise PersistentWorldObjectLitStateEvidenceError(
            "invalid AFQR-19 opportunity evidence"
        )
    for evidence in (qualification_evidence, opportunity_evidence):
        if (
            evidence.actor_entity_id != actor_entity_id
            or evidence.object_entity_id != object_entity_id
            or evidence.operation != operation
        ):
            raise PersistentWorldObjectLitStateEvidenceError(
                "owner evidence does not match actor/object/operation"
            )
    if not qualification_evidence.qualified:
        raise PersistentWorldObjectLitStateEvidenceError(
            "RT-010 rejected lit-state transition"
        )
    if (
        not opportunity_evidence.opportunity_available
        or not opportunity_evidence.resolution_accepted
    ):
        raise PersistentWorldObjectLitStateEvidenceError(
            "AFQR-19 rejected lit-state transition"
        )


def _validate_current_availability(
    *, representation: PersistentWorldEntityLocationRepresentation,
    actor_entity_id: str, object_entity_id: str,
) -> None:
    entities = {entity.entity_id: entity for entity in representation.entities}
    actor = entities.get(actor_entity_id)
    target = entities.get(object_entity_id)
    if actor is None or actor.classification != "character_or_creature":
        raise PersistentWorldObjectLitStateEntityError(
            "actor must exist and be character_or_creature"
        )
    if target is None or target.classification != "object":
        raise PersistentWorldObjectLitStateEntityError(
            "target must exist and be object"
        )
    actor_locations = [
        relation
        for relation in representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == actor_entity_id
    ]
    if len(actor_locations) != 1:
        raise PersistentWorldObjectLitStatePlacementError(
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
        raise PersistentWorldObjectLitStatePlacementError(
            "target must be nearby or carried by the actor"
        )


def _replace_lit_state(
    object_lit_states: Sequence[PersistentWorldObjectLitState],
    *, object_entity_id: str, new_state: str,
) -> tuple[PersistentWorldObjectLitState, ...]:
    found = False
    updated = []
    for item in object_lit_states:
        if item.object_entity_id == object_entity_id:
            found = True
            updated.append(PersistentWorldObjectLitState(
                object_entity_id=object_entity_id,
                state=new_state,
            ))
        else:
            updated.append(item)
    if not found:
        raise PersistentWorldObjectLitStateUnsupportedError(
            "target has no bounded lit/unlit state"
        )
    return tuple(sorted(updated, key=lambda item: item.object_entity_id))


def _existing_transition(
    state: PersistentWorldObjectLitRuntimeState,
    command_id: str,
) -> PersistentWorldObjectLitStateCommittedTransition | None:
    for transition in state.committed_object_lit_transitions:
        if transition.command_id == command_id:
            return transition
    return None


def prepare_persistent_world_object_lit_state(
    *, state: PersistentWorldObjectLitRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectLitStateQualificationEvidence,
    opportunity_evidence: ObjectLitStateOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectLitStatePreparedTransition:
    if not isinstance(state, PersistentWorldObjectLitRuntimeState):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "invalid object lit-state runtime state"
        )
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "invalid command envelope"
        )

    fingerprint = fingerprint_persistent_world_object_lit_state_command(command)
    routing = route_command_envelope(
        request_ref=build_record_id("object_lit_state_request", fingerprint[:24]),
        command_envelope=command,
    )
    if routing.classification.family != "interaction":
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "lit-state command must route through interaction family"
        )

    operation = _operation_from_command(command)
    actor_entity_id = command.source_actor_id
    object_entity_id = _require_record_id(
        command.payload.get("object_entity_id"),
        "command.payload.object_entity_id",
    )
    representation = state.open_close_state.custody_state.movement_state.representation
    _validate_current_availability(
        representation=representation,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
    )

    current = object_lit_state_for(state, object_entity_id)
    if current is None:
        raise PersistentWorldObjectLitStateUnsupportedError(
            "target has no bounded lit/unlit state"
        )

    _validate_owner_evidence(
        qualification_evidence=qualification_evidence,
        opportunity_evidence=opportunity_evidence,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
    )

    actual_state_digest = digest_persistent_world_object_lit_states(
        state.object_lit_states
    )
    if expected_pre_state_digest != actual_state_digest:
        raise PersistentWorldObjectLitStateStaleStateError(
            "owner-local lit state changed before preparation"
        )

    desired = "lit" if operation == "light" else "unlit"
    if current.state == desired:
        raise PersistentWorldObjectLitStateNoChangeError(
            f"target is already {desired}"
        )

    post_states = _replace_lit_state(
        state.object_lit_states,
        object_entity_id=object_entity_id,
        new_state=desired,
    )
    post_state_digest = digest_persistent_world_object_lit_states(post_states)
    placement_digest = digest_persistent_world_entity_location_representation(
        representation
    )

    token = fingerprint[:24]
    preview = create_transaction_preview(
        preview_id=build_record_id("object_lit_state_preview", token),
        command=command,
        status="preview_created",
        messages=("bounded persistent object lit/unlit state prepared",),
        requires_confirmation=False,
        metadata={
            "package": "TERMINAL-PLAY-INT-2",
            "command_family": "interaction",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("object_lit_state_delta", token),
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
            "package": "TERMINAL-PLAY-INT-2",
            "asset_state_semantic_owner": RT010_OBJECT_LIT_STATE_OWNER,
            "opportunity_semantic_owner": AFQR19_OBJECT_LIT_STATE_OPPORTUNITY_OWNER,
            "qualified_transition_owner": "AFQR-01",
        },
    )
    return PersistentWorldObjectLitStatePreparedTransition(
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
        post_object_lit_states=post_states,
    )


def commit_prepared_persistent_world_object_lit_state(
    *, state: PersistentWorldObjectLitRuntimeState,
    prepared: PersistentWorldObjectLitStatePreparedTransition,
) -> PersistentWorldObjectLitStateExecutionResult:
    existing = _existing_transition(state, prepared.command_id)
    if existing is not None:
        if existing.command_fingerprint != prepared.command_fingerprint:
            raise PersistentWorldObjectLitStateRetryConflictError(
                "command ID already committed with different meaning"
            )
        return PersistentWorldObjectLitStateExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )

    if digest_persistent_world_object_lit_states(state.object_lit_states) != prepared.pre_state_digest:
        raise PersistentWorldObjectLitStateStaleStateError(
            "owner-local lit state changed after preparation"
        )
    representation = state.open_close_state.custody_state.movement_state.representation
    if digest_persistent_world_entity_location_representation(representation) != prepared.placement_digest:
        raise PersistentWorldObjectLitStateStaleStateError(
            "target placement changed after preparation"
        )

    receipt = PersistentWorldObjectLitStateCommitReceipt(
        receipt_id=build_record_id(
            "object_lit_state_receipt",
            prepared.command_fingerprint[:24],
        ),
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
    committed = PersistentWorldObjectLitStateCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    post_state = PersistentWorldObjectLitRuntimeState(
        open_close_state=state.open_close_state,
        object_lit_states=prepared.post_object_lit_states,
        committed_object_lit_transitions=(
            *state.committed_object_lit_transitions,
            committed,
        ),
    )
    return PersistentWorldObjectLitStateExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def execute_persistent_world_object_lit_state(
    *, state: PersistentWorldObjectLitRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectLitStateQualificationEvidence,
    opportunity_evidence: ObjectLitStateOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectLitStateExecutionResult:
    fingerprint = fingerprint_persistent_world_object_lit_state_command(command)
    existing = _existing_transition(state, command.command_id)
    if existing is not None:
        if existing.command_fingerprint != fingerprint:
            raise PersistentWorldObjectLitStateRetryConflictError(
                "command ID already committed with materially different command content"
            )
        return PersistentWorldObjectLitStateExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )
    prepared = prepare_persistent_world_object_lit_state(
        state=state,
        command=command,
        qualification_evidence=qualification_evidence,
        opportunity_evidence=opportunity_evidence,
        expected_pre_state_digest=expected_pre_state_digest,
    )
    return commit_prepared_persistent_world_object_lit_state(
        state=state,
        prepared=prepared,
    )


def replay_persistent_world_object_lit_states(
    *, object_lit_states: Sequence[PersistentWorldObjectLitState],
    receipt: PersistentWorldObjectLitStateCommitReceipt,
) -> tuple[PersistentWorldObjectLitState, ...]:
    if not isinstance(receipt, PersistentWorldObjectLitStateCommitReceipt):
        raise PersistentWorldObjectLitStateReplayError(
            "receipt has invalid type"
        )
    current = tuple(object_lit_states)
    if digest_persistent_world_object_lit_states(current) != receipt.pre_state_digest:
        raise PersistentWorldObjectLitStateReplayError(
            "replay pre-state digest mismatch"
        )
    existing = next(
        (item for item in current if item.object_entity_id == receipt.object_entity_id),
        None,
    )
    if existing is None or existing.state != receipt.pre_object_state:
        raise PersistentWorldObjectLitStateReplayError(
            "replay object state disagrees with receipt"
        )
    post = _replace_lit_state(
        current,
        object_entity_id=receipt.object_entity_id,
        new_state=receipt.post_object_state,
    )
    if digest_persistent_world_object_lit_states(post) != receipt.post_state_digest:
        raise PersistentWorldObjectLitStateReplayError(
            "replay post-state digest mismatch"
        )
    return post


def serialize_persistent_world_object_lit_state_commit_receipt(
    receipt: PersistentWorldObjectLitStateCommitReceipt,
) -> dict[str, str]:
    if not isinstance(receipt, PersistentWorldObjectLitStateCommitReceipt):
        raise InvalidPersistentWorldObjectLitStateRequestError(
            "receipt must be PersistentWorldObjectLitStateCommitReceipt"
        )
    return receipt.to_dict()
