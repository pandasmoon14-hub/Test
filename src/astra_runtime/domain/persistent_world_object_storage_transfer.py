"""Bounded persistent object containment/storage transfer for TERMINAL-PLAY-INT-3.

This module adds one RT-010-owned immediate physical placement relation,
``contained_by``, and deterministic store/retrieve transitions that compose
with the existing INT-2 runtime state.

It does not implement generalized inventory, capacity, weight, nesting,
ownership, hidden cargo, locks, equipment, damage, effects, or compound
command execution.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
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
    CONTAINED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntityLocationRepresentation,
    PersistentWorldRelation,
    create_carried_by_relation,
    create_contained_by_relation,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRuntimeState,
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyRuntimeState,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitRuntimeState,
    digest_persistent_world_object_lit_runtime_state,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseRuntimeState,
    object_open_state_for,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope, validate_command_envelope
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope, create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import TransactionPreview, create_transaction_preview


RT010_STORAGE_OWNER = "RT-010"
AFQR19_STORAGE_OPPORTUNITY_OWNER = "AFQR-19"
STORAGE_OPERATIONS = frozenset({"store", "retrieve"})
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PersistentWorldObjectStorageError(ValueError):
    pass


class InvalidPersistentWorldObjectStorageRequestError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageEntityError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStoragePlacementError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageEvidenceError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageUnsupportedError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageNoChangeError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageStaleStateError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageRetryConflictError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageRelationIdentityCollisionError(PersistentWorldObjectStorageError):
    pass


class PersistentWorldObjectStorageReplayError(PersistentWorldObjectStorageError):
    pass


def _require_record_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise InvalidPersistentWorldObjectStorageRequestError(
            f"{label} must be a valid record ID"
        )
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise InvalidPersistentWorldObjectStorageRequestError(
            f"{label} must be a lowercase SHA-256 digest"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class ObjectStorageQualificationEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    container_entity_id: str
    operation: str
    qualified: bool
    semantic_owner: str = RT010_STORAGE_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id", "actor_entity_id", "object_entity_id", "container_entity_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.operation not in STORAGE_OPERATIONS:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "operation must be store or retrieve"
            )
        if type(self.qualified) is not bool:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "qualified must be bool"
            )
        if self.semantic_owner != RT010_STORAGE_OWNER:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "qualification semantic_owner must be RT-010"
            )


@dataclass(frozen=True, kw_only=True)
class ObjectStorageOpportunityEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    container_entity_id: str
    operation: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_STORAGE_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id", "actor_entity_id", "object_entity_id", "container_entity_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.operation not in STORAGE_OPERATIONS:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "operation must be store or retrieve"
            )
        if type(self.opportunity_available) is not bool or type(self.resolution_accepted) is not bool:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "opportunity/resolution flags must be bool"
            )
        if self.semantic_owner != AFQR19_STORAGE_OPPORTUNITY_OWNER:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "opportunity semantic_owner must be AFQR-19"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectStorageCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    container_entity_id: str
    operation: str
    source_relation_id: str
    source_relation_type: str
    destination_relation_id: str
    destination_relation_type: str
    pre_state_digest: str
    post_state_digest: str
    preview_id: str
    state_delta_id: str
    rt010_qualification_id: str
    opportunity_evidence_id: str
    status: str = "committed"

    def __post_init__(self) -> None:
        for name in (
            "receipt_id", "actor_entity_id", "object_entity_id", "container_entity_id",
            "source_relation_id", "destination_relation_id", "preview_id", "state_delta_id",
            "rt010_qualification_id", "opportunity_evidence_id",
        ):
            _require_record_id(getattr(self, name), name)
        if not isinstance(self.command_id, str) or not self.command_id:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "command_id must be non-empty"
            )
        _require_sha256(self.command_fingerprint, "command_fingerprint")
        if self.operation not in STORAGE_OPERATIONS:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "operation must be store or retrieve"
            )
        expected_types = (
            (CARRIED_BY_RELATION_TYPE, CONTAINED_BY_RELATION_TYPE)
            if self.operation == "store"
            else (CONTAINED_BY_RELATION_TYPE, CARRIED_BY_RELATION_TYPE)
        )
        if (self.source_relation_type, self.destination_relation_type) != expected_types:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "storage relation types disagree with operation"
            )
        _require_sha256(self.pre_state_digest, "pre_state_digest")
        _require_sha256(self.post_state_digest, "post_state_digest")
        if self.status != "committed":
            raise InvalidPersistentWorldObjectStorageRequestError(
                "receipt status must be committed"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "actor_entity_id": self.actor_entity_id,
            "object_entity_id": self.object_entity_id,
            "container_entity_id": self.container_entity_id,
            "operation": self.operation,
            "source_relation_id": self.source_relation_id,
            "source_relation_type": self.source_relation_type,
            "destination_relation_id": self.destination_relation_id,
            "destination_relation_type": self.destination_relation_type,
            "pre_state_digest": self.pre_state_digest,
            "post_state_digest": self.post_state_digest,
            "preview_id": self.preview_id,
            "state_delta_id": self.state_delta_id,
            "rt010_qualification_id": self.rt010_qualification_id,
            "opportunity_evidence_id": self.opportunity_evidence_id,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectStorageCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldObjectStorageCommitReceipt


def _representation_from_lit_state(
    state: PersistentWorldObjectLitRuntimeState,
) -> PersistentWorldEntityLocationRepresentation:
    return state.open_close_state.custody_state.movement_state.representation


def _immediate_relations(
    representation: PersistentWorldEntityLocationRepresentation,
    object_entity_id: str,
) -> tuple[list[PersistentWorldRelation], list[PersistentWorldRelation], list[PersistentWorldRelation]]:
    direct = [
        r for r in representation.relations
        if r.relation_type == LOCATED_AT_RELATION_TYPE
        and r.subject_entity_id == object_entity_id
    ]
    carried = [
        r for r in representation.relations
        if r.relation_type == CARRIED_BY_RELATION_TYPE
        and r.subject_entity_id == object_entity_id
    ]
    contained = [
        r for r in representation.relations
        if r.relation_type == CONTAINED_BY_RELATION_TYPE
        and r.subject_entity_id == object_entity_id
    ]
    return direct, carried, contained


def validate_persistent_world_storage_placement(
    representation: PersistentWorldEntityLocationRepresentation,
) -> None:
    objects = {
        entity.entity_id for entity in representation.entities
        if entity.classification == "object"
    }
    contained = [
        r for r in representation.relations
        if r.relation_type == CONTAINED_BY_RELATION_TYPE
    ]
    for object_entity_id in objects:
        direct, carried, inside = _immediate_relations(representation, object_entity_id)
        if len(direct) + len(carried) + len(inside) > 1:
            raise PersistentWorldObjectStoragePlacementError(
                "object may have only one immediate physical placement"
            )
    contained_subjects = {r.subject_entity_id for r in contained}
    container_ids = {r.object_entity_id for r in contained}
    if contained_subjects & container_ids:
        raise PersistentWorldObjectStoragePlacementError(
            "INT-3 does not permit nested containment"
        )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectStorageRuntimeState:
    lit_state: PersistentWorldObjectLitRuntimeState
    committed_storage_transitions: tuple[PersistentWorldObjectStorageCommittedTransition, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.lit_state, PersistentWorldObjectLitRuntimeState):
            raise InvalidPersistentWorldObjectStorageRequestError(
                "lit_state must be PersistentWorldObjectLitRuntimeState"
            )
        transitions = tuple(self.committed_storage_transitions)
        for index, transition in enumerate(transitions):
            if not isinstance(transition, PersistentWorldObjectStorageCommittedTransition):
                raise InvalidPersistentWorldObjectStorageRequestError(
                    f"committed_storage_transitions[{index}] has invalid type"
                )
        ids = [item.command_id for item in transitions]
        if len(ids) != len(set(ids)):
            raise InvalidPersistentWorldObjectStorageRequestError(
                "storage command IDs must be unique"
            )
        lower_ids = {
            item.command_id
            for item in self.lit_state.open_close_state.custody_state.movement_state.committed_transitions
        }
        lower_ids.update(
            item.command_id
            for item in self.lit_state.open_close_state.custody_state.committed_custody_transitions
        )
        lower_ids.update(
            item.command_id
            for item in self.lit_state.open_close_state.committed_object_state_transitions
        )
        lower_ids.update(
            item.command_id for item in self.lit_state.committed_object_lit_transitions
        )
        if set(ids) & lower_ids:
            raise InvalidPersistentWorldObjectStorageRequestError(
                "storage command IDs must not collide with lower-layer transitions"
            )
        validate_persistent_world_storage_placement(
            _representation_from_lit_state(self.lit_state)
        )
        object.__setattr__(self, "committed_storage_transitions", transitions)


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectStoragePreparedTransition:
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    container_entity_id: str
    operation: str
    source_relation_id: str
    source_relation_type: str
    destination_relation_id: str
    destination_relation_type: str
    pre_state_digest: str
    post_state_digest: str
    rt010_qualification_id: str
    opportunity_evidence_id: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    post_lit_state: PersistentWorldObjectLitRuntimeState


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectStorageExecutionResult:
    state: PersistentWorldObjectStorageRuntimeState
    receipt: PersistentWorldObjectStorageCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_object_storage_qualification_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    container_entity_id: str, operation: str, qualified: bool,
) -> ObjectStorageQualificationEvidence:
    return ObjectStorageQualificationEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
        operation=operation,
        qualified=qualified,
    )


def create_object_storage_opportunity_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    container_entity_id: str, operation: str,
    opportunity_available: bool, resolution_accepted: bool,
) -> ObjectStorageOpportunityEvidence:
    return ObjectStorageOpportunityEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
        operation=operation,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def create_persistent_world_object_storage_runtime_state(
    *, lit_state: PersistentWorldObjectLitRuntimeState,
) -> PersistentWorldObjectStorageRuntimeState:
    return PersistentWorldObjectStorageRuntimeState(lit_state=lit_state)


def replace_persistent_world_object_storage_lit_state(
    *, state: PersistentWorldObjectStorageRuntimeState,
    lit_state: PersistentWorldObjectLitRuntimeState,
) -> PersistentWorldObjectStorageRuntimeState:
    if not isinstance(state, PersistentWorldObjectStorageRuntimeState):
        raise InvalidPersistentWorldObjectStorageRequestError(
            "state must be PersistentWorldObjectStorageRuntimeState"
        )
    return PersistentWorldObjectStorageRuntimeState(
        lit_state=lit_state,
        committed_storage_transitions=state.committed_storage_transitions,
    )


def containment_relation_for(
    state: PersistentWorldObjectStorageRuntimeState,
    object_entity_id: str,
) -> PersistentWorldRelation | None:
    representation = _representation_from_lit_state(state.lit_state)
    matches = [
        r for r in representation.relations
        if r.relation_type == CONTAINED_BY_RELATION_TYPE
        and r.subject_entity_id == object_entity_id
    ]
    if len(matches) > 1:
        raise PersistentWorldObjectStoragePlacementError(
            "duplicate contained_by relations"
        )
    return matches[0] if matches else None


def contained_object_ids(
    state: PersistentWorldObjectStorageRuntimeState,
    container_entity_id: str,
) -> tuple[str, ...]:
    representation = _representation_from_lit_state(state.lit_state)
    return tuple(sorted(
        r.subject_entity_id
        for r in representation.relations
        if r.relation_type == CONTAINED_BY_RELATION_TYPE
        and r.object_entity_id == container_entity_id
    ))


def canonical_serialize_persistent_world_containment(
    representation: PersistentWorldEntityLocationRepresentation,
) -> str:
    material = {
        "state_family": "rt010_object_containment",
        "relations": [
            r.to_dict()
            for r in sorted(
                (
                    relation for relation in representation.relations
                    if relation.relation_type == CONTAINED_BY_RELATION_TYPE
                ),
                key=lambda item: item.relation_id,
            )
        ],
    }
    return json.dumps(
        material, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def digest_persistent_world_containment(
    representation: PersistentWorldEntityLocationRepresentation,
) -> str:
    return hashlib.sha256(
        canonical_serialize_persistent_world_containment(representation).encode("utf-8")
    ).hexdigest()


def digest_persistent_world_storage_composite_state(
    lit_state: PersistentWorldObjectLitRuntimeState,
) -> str:
    representation = _representation_from_lit_state(lit_state)
    material = {
        "world_state_family": "persistent_world_int2_plus_storage",
        "int2_world_state_digest": digest_persistent_world_object_lit_runtime_state(lit_state),
        "containment_digest": digest_persistent_world_containment(representation),
    }
    canonical = json.dumps(
        material, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def digest_persistent_world_object_storage_runtime_state(
    state: PersistentWorldObjectStorageRuntimeState,
) -> str:
    if not isinstance(state, PersistentWorldObjectStorageRuntimeState):
        raise InvalidPersistentWorldObjectStorageRequestError(
            "state must be PersistentWorldObjectStorageRuntimeState"
        )
    return digest_persistent_world_storage_composite_state(state.lit_state)


def fingerprint_persistent_world_object_storage_command(
    command: CommandEnvelope,
) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectStorageRequestError(
            "command failed CommandEnvelope validation"
        )
    return fingerprint_command_envelope(command, allow_nan=False)


def _operation_from_command(command: CommandEnvelope) -> str:
    normalized = command.command_type.strip().lower().replace("-", "_")
    if normalized == "transfer_to_container":
        return "store"
    if normalized == "transfer_from_container":
        return "retrieve"
    raise InvalidPersistentWorldObjectStorageRequestError(
        "INT-3 supports only transfer_to_container/transfer_from_container"
    )


def _validate_owner_evidence(
    *, qualification_evidence: ObjectStorageQualificationEvidence,
    opportunity_evidence: ObjectStorageOpportunityEvidence,
    actor_entity_id: str, object_entity_id: str, container_entity_id: str,
    operation: str,
) -> None:
    if not isinstance(qualification_evidence, ObjectStorageQualificationEvidence):
        raise PersistentWorldObjectStorageEvidenceError(
            "invalid RT-010 storage qualification evidence"
        )
    if not isinstance(opportunity_evidence, ObjectStorageOpportunityEvidence):
        raise PersistentWorldObjectStorageEvidenceError(
            "invalid AFQR-19 storage opportunity evidence"
        )
    for evidence in (qualification_evidence, opportunity_evidence):
        if (
            evidence.actor_entity_id != actor_entity_id
            or evidence.object_entity_id != object_entity_id
            or evidence.container_entity_id != container_entity_id
            or evidence.operation != operation
        ):
            raise PersistentWorldObjectStorageEvidenceError(
                "owner evidence does not match actor/object/container/operation"
            )
    if not qualification_evidence.qualified:
        raise PersistentWorldObjectStorageEvidenceError(
            "RT-010 rejected storage transition"
        )
    if (
        not opportunity_evidence.opportunity_available
        or not opportunity_evidence.resolution_accepted
    ):
        raise PersistentWorldObjectStorageEvidenceError(
            "AFQR-19 rejected storage transition"
        )


def _current_actor_place(
    representation: PersistentWorldEntityLocationRepresentation,
    actor_entity_id: str,
) -> str:
    matches = [
        r for r in representation.relations
        if r.relation_type == LOCATED_AT_RELATION_TYPE
        and r.subject_entity_id == actor_entity_id
    ]
    if len(matches) != 1:
        raise PersistentWorldObjectStoragePlacementError(
            "actor requires exactly one current location"
        )
    return matches[0].object_entity_id


def _container_accessible(
    representation: PersistentWorldEntityLocationRepresentation,
    *, actor_entity_id: str, container_entity_id: str,
) -> bool:
    place_id = _current_actor_place(representation, actor_entity_id)
    direct, carried, contained = _immediate_relations(representation, container_entity_id)
    if contained:
        return False
    return (
        len(direct) == 1 and not carried and direct[0].object_entity_id == place_id
    ) or (
        len(carried) == 1 and not direct and carried[0].object_entity_id == actor_entity_id
    )


def _replace_representation_in_lit_state(
    state: PersistentWorldObjectLitRuntimeState,
    representation: PersistentWorldEntityLocationRepresentation,
) -> PersistentWorldObjectLitRuntimeState:
    old_movement = state.open_close_state.custody_state.movement_state
    movement = PersistentWorldMovementRuntimeState(
        representation=representation,
        committed_transitions=old_movement.committed_transitions,
    )
    old_custody = state.open_close_state.custody_state
    custody = PersistentWorldObjectCustodyRuntimeState(
        movement_state=movement,
        committed_custody_transitions=old_custody.committed_custody_transitions,
    )
    old_open = state.open_close_state
    open_close = PersistentWorldObjectOpenCloseRuntimeState(
        custody_state=custody,
        object_open_states=old_open.object_open_states,
        committed_object_state_transitions=old_open.committed_object_state_transitions,
    )
    return PersistentWorldObjectLitRuntimeState(
        open_close_state=open_close,
        object_lit_states=state.object_lit_states,
        committed_object_lit_transitions=state.committed_object_lit_transitions,
    )


def _apply_storage_change(
    *, representation: PersistentWorldEntityLocationRepresentation,
    actor_entity_id: str, object_entity_id: str, container_entity_id: str,
    source_relation_id: str, destination_relation_id: str, operation: str,
) -> PersistentWorldEntityLocationRepresentation:
    remaining = [
        relation for relation in representation.relations
        if relation.relation_id != source_relation_id
    ]
    if len(remaining) != len(representation.relations) - 1:
        raise PersistentWorldObjectStoragePlacementError(
            "storage source relation is missing or duplicated"
        )
    if any(r.relation_id == destination_relation_id for r in remaining):
        raise PersistentWorldObjectStorageRelationIdentityCollisionError(
            "deterministic storage destination relation ID collides"
        )
    if operation == "store":
        destination = create_contained_by_relation(
            relation_id=destination_relation_id,
            subject_entity_id=object_entity_id,
            object_entity_id=container_entity_id,
        )
    elif operation == "retrieve":
        destination = create_carried_by_relation(
            relation_id=destination_relation_id,
            subject_entity_id=object_entity_id,
            object_entity_id=actor_entity_id,
        )
    else:
        raise InvalidPersistentWorldObjectStorageRequestError(
            "operation must be store or retrieve"
        )
    post = create_persistent_world_entity_location_representation(
        campaign_id=representation.campaign_id,
        entities=representation.entities,
        relations=(*remaining, destination),
    )
    validate_persistent_world_storage_placement(post)
    return post


def prepare_persistent_world_object_storage(
    *, state: PersistentWorldObjectStorageRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectStorageQualificationEvidence,
    opportunity_evidence: ObjectStorageOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectStoragePreparedTransition:
    if not isinstance(state, PersistentWorldObjectStorageRuntimeState):
        raise InvalidPersistentWorldObjectStorageRequestError(
            "invalid storage runtime state"
        )
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectStorageRequestError(
            "invalid command envelope"
        )
    fingerprint = fingerprint_persistent_world_object_storage_command(command)
    routing = route_command_envelope(
        request_ref=build_record_id("storage_request", fingerprint[:24]),
        command_envelope=command,
    )
    if routing.classification.family != "inventory":
        raise InvalidPersistentWorldObjectStorageRequestError(
            "storage command must route through inventory family"
        )

    operation = _operation_from_command(command)
    actor_entity_id = command.source_actor_id
    object_entity_id = _require_record_id(
        command.payload.get("object_entity_id"), "command.payload.object_entity_id"
    )
    container_entity_id = _require_record_id(
        command.payload.get("container_entity_id"), "command.payload.container_entity_id"
    )
    if object_entity_id == container_entity_id:
        raise PersistentWorldObjectStoragePlacementError("object cannot contain itself")

    representation = _representation_from_lit_state(state.lit_state)
    entities = {entity.entity_id: entity for entity in representation.entities}
    actor = entities.get(actor_entity_id)
    target = entities.get(object_entity_id)
    container = entities.get(container_entity_id)
    if actor is None or actor.classification != "character_or_creature":
        raise PersistentWorldObjectStorageEntityError(
            "actor must exist and be character_or_creature"
        )
    if target is None or target.classification != "object":
        raise PersistentWorldObjectStorageEntityError(
            "storage target must exist and be object"
        )
    if container is None or container.classification != "object":
        raise PersistentWorldObjectStorageEntityError(
            "container must exist and be object"
        )
    if not _container_accessible(
        representation,
        actor_entity_id=actor_entity_id,
        container_entity_id=container_entity_id,
    ):
        raise PersistentWorldObjectStoragePlacementError(
            "container must be directly accessible to the actor"
        )
    open_state = object_open_state_for(
        state.lit_state.open_close_state, container_entity_id,
    )
    if open_state is None:
        raise PersistentWorldObjectStorageUnsupportedError(
            "container has no bounded open/close state"
        )
    if open_state.state != "open":
        raise PersistentWorldObjectStoragePlacementError("container must be open")

    direct, carried, contained = _immediate_relations(representation, object_entity_id)
    if len(direct) + len(carried) + len(contained) > 1:
        raise PersistentWorldObjectStoragePlacementError("object placement is contradictory")
    if operation == "store":
        if (
            len(contained) == 1
            and contained[0].object_entity_id == container_entity_id
            and not direct and not carried
        ):
            raise PersistentWorldObjectStorageNoChangeError(
                "object is already contained by the requested container"
            )
        if (
            len(carried) != 1 or direct or contained
            or carried[0].object_entity_id != actor_entity_id
        ):
            raise PersistentWorldObjectStoragePlacementError(
                "store requires target carried by the actor"
            )
        source_relation = carried[0]
        destination_type = CONTAINED_BY_RELATION_TYPE
    else:
        if (
            len(contained) != 1 or direct or carried
            or contained[0].object_entity_id != container_entity_id
        ):
            raise PersistentWorldObjectStoragePlacementError(
                "retrieve requires target contained by the requested container"
            )
        source_relation = contained[0]
        destination_type = CARRIED_BY_RELATION_TYPE

    _validate_owner_evidence(
        qualification_evidence=qualification_evidence,
        opportunity_evidence=opportunity_evidence,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
        operation=operation,
    )
    actual_digest = digest_persistent_world_entity_location_representation(representation)
    if expected_pre_state_digest != actual_digest:
        raise PersistentWorldObjectStorageStaleStateError("stale pre-state digest")

    token = fingerprint[:24]
    destination_relation_id = build_record_id("relation", f"storage-{token}")
    if (
        destination_relation_id != source_relation.relation_id
        and any(
            relation.relation_id == destination_relation_id
            for relation in representation.relations
        )
    ):
        raise PersistentWorldObjectStorageRelationIdentityCollisionError(
            "destination relation identity already exists"
        )

    preview = create_transaction_preview(
        preview_id=build_record_id("storage_preview", token),
        command=command,
        status="preview_created",
        messages=("bounded persistent object storage transfer prepared",),
        requires_confirmation=False,
        metadata={
            "package": "TERMINAL-PLAY-INT-3",
            "command_family": "inventory",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("storage_delta", token),
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(
            actor_entity_id, object_entity_id, container_entity_id,
            source_relation.relation_id, destination_relation_id,
        ),
        change_type="relationship_update",
        payload={
            "operation": operation,
            "actor_entity_id": actor_entity_id,
            "object_entity_id": object_entity_id,
            "container_entity_id": container_entity_id,
            "source_relation_id": source_relation.relation_id,
            "source_relation_type": source_relation.relation_type,
            "destination_relation_id": destination_relation_id,
            "destination_relation_type": destination_type,
        },
        metadata={
            "package": "TERMINAL-PLAY-INT-3",
            "storage_semantic_owner": RT010_STORAGE_OWNER,
            "opportunity_semantic_owner": AFQR19_STORAGE_OPPORTUNITY_OWNER,
            "qualified_transition_owner": "AFQR-01",
        },
    )
    post_representation = _apply_storage_change(
        representation=representation,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
        source_relation_id=source_relation.relation_id,
        destination_relation_id=destination_relation_id,
        operation=operation,
    )
    post_digest = digest_persistent_world_entity_location_representation(post_representation)
    return PersistentWorldObjectStoragePreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        container_entity_id=container_entity_id,
        operation=operation,
        source_relation_id=source_relation.relation_id,
        source_relation_type=source_relation.relation_type,
        destination_relation_id=destination_relation_id,
        destination_relation_type=destination_type,
        pre_state_digest=actual_digest,
        post_state_digest=post_digest,
        rt010_qualification_id=qualification_evidence.evidence_id,
        opportunity_evidence_id=opportunity_evidence.evidence_id,
        preview=preview,
        state_delta=delta,
        post_lit_state=_replace_representation_in_lit_state(
            state.lit_state, post_representation,
        ),
    )


def _commit_new_persistent_world_object_storage(
    *, state: PersistentWorldObjectStorageRuntimeState,
    prepared: PersistentWorldObjectStoragePreparedTransition,
) -> PersistentWorldObjectStorageExecutionResult:
    current_representation = _representation_from_lit_state(state.lit_state)
    if digest_persistent_world_entity_location_representation(
        current_representation
    ) != prepared.pre_state_digest:
        raise PersistentWorldObjectStorageStaleStateError(
            "storage placement changed after preparation"
        )
    receipt = PersistentWorldObjectStorageCommitReceipt(
        receipt_id=build_record_id("storage_receipt", prepared.command_fingerprint[:24]),
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        actor_entity_id=prepared.actor_entity_id,
        object_entity_id=prepared.object_entity_id,
        container_entity_id=prepared.container_entity_id,
        operation=prepared.operation,
        source_relation_id=prepared.source_relation_id,
        source_relation_type=prepared.source_relation_type,
        destination_relation_id=prepared.destination_relation_id,
        destination_relation_type=prepared.destination_relation_type,
        pre_state_digest=prepared.pre_state_digest,
        post_state_digest=prepared.post_state_digest,
        preview_id=prepared.preview.preview_id,
        state_delta_id=prepared.state_delta.delta_id,
        rt010_qualification_id=prepared.rt010_qualification_id,
        opportunity_evidence_id=prepared.opportunity_evidence_id,
    )
    committed = PersistentWorldObjectStorageCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    post_state = PersistentWorldObjectStorageRuntimeState(
        lit_state=prepared.post_lit_state,
        committed_storage_transitions=(*state.committed_storage_transitions, committed),
    )
    return PersistentWorldObjectStorageExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def commit_prepared_persistent_world_object_storage(
    *, state: PersistentWorldObjectStorageRuntimeState,
    prepared: PersistentWorldObjectStoragePreparedTransition,
) -> PersistentWorldObjectStorageExecutionResult:
    if not isinstance(state, PersistentWorldObjectStorageRuntimeState):
        raise InvalidPersistentWorldObjectStorageRequestError("invalid storage runtime state")
    if not isinstance(prepared, PersistentWorldObjectStoragePreparedTransition):
        raise InvalidPersistentWorldObjectStorageRequestError("invalid prepared transition")
    return commit_prepared_capability_transition(
        spec=STORAGE_TRANSITION_CAPABILITY_SPEC,
        state=state,
        prepared=prepared,
    )


def execute_persistent_world_object_storage(
    *, state: PersistentWorldObjectStorageRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectStorageQualificationEvidence,
    opportunity_evidence: ObjectStorageOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectStorageExecutionResult:
    if not isinstance(state, PersistentWorldObjectStorageRuntimeState):
        raise InvalidPersistentWorldObjectStorageRequestError("invalid storage runtime state")
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


def replay_persistent_world_object_storage(
    *, representation: PersistentWorldEntityLocationRepresentation,
    receipt: PersistentWorldObjectStorageCommitReceipt,
) -> PersistentWorldEntityLocationRepresentation:
    if not isinstance(receipt, PersistentWorldObjectStorageCommitReceipt):
        raise PersistentWorldObjectStorageReplayError("receipt has invalid type")
    if digest_persistent_world_entity_location_representation(
        representation
    ) != receipt.pre_state_digest:
        raise PersistentWorldObjectStorageReplayError("replay pre-state digest mismatch")
    source = [
        relation for relation in representation.relations
        if relation.relation_id == receipt.source_relation_id
    ]
    if len(source) != 1:
        raise PersistentWorldObjectStorageReplayError(
            "replay source relation is absent or duplicated"
        )
    relation = source[0]
    if (
        relation.relation_type != receipt.source_relation_type
        or relation.subject_entity_id != receipt.object_entity_id
    ):
        raise PersistentWorldObjectStorageReplayError(
            "replay source relation disagrees with receipt"
        )
    expected_source_target = (
        receipt.actor_entity_id if receipt.operation == "store" else receipt.container_entity_id
    )
    if relation.object_entity_id != expected_source_target:
        raise PersistentWorldObjectStorageReplayError(
            "replay source target disagrees with receipt"
        )
    post = _apply_storage_change(
        representation=representation,
        actor_entity_id=receipt.actor_entity_id,
        object_entity_id=receipt.object_entity_id,
        container_entity_id=receipt.container_entity_id,
        source_relation_id=receipt.source_relation_id,
        destination_relation_id=receipt.destination_relation_id,
        operation=receipt.operation,
    )
    if digest_persistent_world_entity_location_representation(
        post
    ) != receipt.post_state_digest:
        raise PersistentWorldObjectStorageReplayError("replay post-state digest mismatch")
    return post


STORAGE_TRANSITION_CAPABILITY_SPEC = TransitionCapabilitySpec(
    capability_id="persistent_world_object_storage",
    semantic_owners=("RT-010", "AFQR-19", "AFQR-01", "AFQR-02"),
    state_type=PersistentWorldObjectStorageRuntimeState,
    replay_state_type=PersistentWorldEntityLocationRepresentation,
    receipt_prefix="storage_receipt",
    state_digest=lambda state: digest_persistent_world_entity_location_representation(
        _representation_from_lit_state(state.lit_state)
    ),
    fingerprint_command=fingerprint_persistent_world_object_storage_command,
    committed_transitions=lambda state: state.committed_storage_transitions,
    prepare_new_transition=lambda state, command, context: prepare_persistent_world_object_storage(
        state=state,
        command=command,
        qualification_evidence=context["qualification_evidence"],
        opportunity_evidence=context["opportunity_evidence"],
        expected_pre_state_digest=context["expected_pre_state_digest"],
    ),
    commit_new_transition=lambda state, prepared: _commit_new_persistent_world_object_storage(
        state=state, prepared=prepared,
    ),
    build_retry_result=lambda state, committed: PersistentWorldObjectStorageExecutionResult(
        state=state,
        receipt=committed.receipt,
        preview=committed.preview,
        state_delta=committed.state_delta,
        technical_retry=True,
    ),
    retry_conflict_error=lambda message: PersistentWorldObjectStorageRetryConflictError(message),
    replay_committed_transition=lambda pre_state, receipt: replay_persistent_world_object_storage(
        representation=pre_state, receipt=receipt,
    ),
)


def serialize_persistent_world_object_storage_commit_receipt(
    receipt: PersistentWorldObjectStorageCommitReceipt,
) -> dict[str, str]:
    if not isinstance(receipt, PersistentWorldObjectStorageCommitReceipt):
        raise InvalidPersistentWorldObjectStorageRequestError(
            "receipt must be PersistentWorldObjectStorageCommitReceipt"
        )
    return receipt.to_dict()
