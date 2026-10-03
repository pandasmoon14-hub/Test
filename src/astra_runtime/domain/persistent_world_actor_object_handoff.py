"""Bounded voluntary actor-to-actor object handoff for TERMINAL-PLAY-VSM-6.

This module implements one deterministic immediate placement transition:
an object already carried by a source actor may be handed to one explicitly
qualified recipient actor when both actors are co-located.

Authority remains with existing semantic owners:
- RT-010: immediate physical carrying/asset placement;
- AFQR-18: co-location/spatial qualification;
- AFQR-19: opportunity/resolution qualification;
- AFQR-01: qualified commitment;
- AFQR-02: command identity and technical retry.

This module does not implement ownership, entitlement, trust, reputation,
dialogue, persuasion, NPC planning, actor knowledge, economy, theft,
combat, model calls, narration, or a generalized interaction framework.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from astra_runtime.domain._deterministic_transition_support import (
    command_fingerprint_matches,
    find_committed_transition,
    fingerprint_command_envelope,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    CONTAINED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntityLocationRepresentation,
    create_carried_by_relation,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRuntimeState,
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    PersistentWorldObjectCustodyRuntimeState,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    PersistentWorldObjectDisplacementRuntimeState,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    PersistentWorldObjectLitRuntimeState,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseRuntimeState,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    PersistentWorldObjectStorageRuntimeState,
    validate_persistent_world_storage_placement,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope, validate_command_envelope
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope, create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import TransactionPreview, create_transaction_preview


RT010_ACTOR_OBJECT_HANDOFF_OWNER = "RT-010"
AFQR18_ACTOR_OBJECT_HANDOFF_SPATIAL_OWNER = "AFQR-18"
AFQR19_ACTOR_OBJECT_HANDOFF_OPPORTUNITY_OWNER = "AFQR-19"
ACTOR_OBJECT_HANDOFF_METHODS = frozenset({"handoff"})
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PersistentWorldActorObjectHandoffError(ValueError):
    """Base bounded actor-object handoff failure."""


class InvalidPersistentWorldActorObjectHandoffRequestError(
    PersistentWorldActorObjectHandoffError
):
    pass


class PersistentWorldActorObjectHandoffEntityError(
    PersistentWorldActorObjectHandoffError
):
    pass


class PersistentWorldActorObjectHandoffPlacementError(
    PersistentWorldActorObjectHandoffError
):
    pass


class PersistentWorldActorObjectHandoffEvidenceError(
    PersistentWorldActorObjectHandoffError
):
    pass


class PersistentWorldActorObjectHandoffStaleStateError(
    PersistentWorldActorObjectHandoffError
):
    pass


class PersistentWorldActorObjectHandoffRetryConflictError(
    PersistentWorldActorObjectHandoffError
):
    pass


class PersistentWorldActorObjectHandoffRelationIdentityCollisionError(
    PersistentWorldActorObjectHandoffError
):
    pass


class PersistentWorldActorObjectHandoffReplayError(
    PersistentWorldActorObjectHandoffError
):
    pass


def _require_record_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            f"{label} must be a valid record ID"
        )
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            f"{label} must be a lowercase SHA-256 digest"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class ActorObjectHandoffQualificationEvidence:
    evidence_id: str
    source_actor_entity_id: str
    recipient_actor_entity_id: str
    object_entity_id: str
    method: str
    qualified: bool
    semantic_owner: str = RT010_ACTOR_OBJECT_HANDOFF_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "source_actor_entity_id",
            "recipient_actor_entity_id",
            "object_entity_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.source_actor_entity_id == self.recipient_actor_entity_id:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "source and recipient actors must differ"
            )
        if self.method not in ACTOR_OBJECT_HANDOFF_METHODS:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "method must be handoff"
            )
        if type(self.qualified) is not bool:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "qualified must be bool"
            )
        if self.semantic_owner != RT010_ACTOR_OBJECT_HANDOFF_OWNER:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "qualification semantic_owner must be RT-010"
            )


@dataclass(frozen=True, kw_only=True)
class ActorObjectHandoffSpatialEvidence:
    evidence_id: str
    source_actor_entity_id: str
    recipient_actor_entity_id: str
    object_entity_id: str
    place_id: str
    method: str
    spatially_permitted: bool
    semantic_owner: str = AFQR18_ACTOR_OBJECT_HANDOFF_SPATIAL_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "source_actor_entity_id",
            "recipient_actor_entity_id",
            "object_entity_id",
            "place_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.source_actor_entity_id == self.recipient_actor_entity_id:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "source and recipient actors must differ"
            )
        if self.method not in ACTOR_OBJECT_HANDOFF_METHODS:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "method must be handoff"
            )
        if type(self.spatially_permitted) is not bool:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "spatially_permitted must be bool"
            )
        if self.semantic_owner != AFQR18_ACTOR_OBJECT_HANDOFF_SPATIAL_OWNER:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "spatial semantic_owner must be AFQR-18"
            )


@dataclass(frozen=True, kw_only=True)
class ActorObjectHandoffOpportunityEvidence:
    evidence_id: str
    source_actor_entity_id: str
    recipient_actor_entity_id: str
    object_entity_id: str
    place_id: str
    method: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_ACTOR_OBJECT_HANDOFF_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "source_actor_entity_id",
            "recipient_actor_entity_id",
            "object_entity_id",
            "place_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.source_actor_entity_id == self.recipient_actor_entity_id:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "source and recipient actors must differ"
            )
        if self.method not in ACTOR_OBJECT_HANDOFF_METHODS:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "method must be handoff"
            )
        if (
            type(self.opportunity_available) is not bool
            or type(self.resolution_accepted) is not bool
        ):
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "opportunity/resolution flags must be bool"
            )
        if self.semantic_owner != AFQR19_ACTOR_OBJECT_HANDOFF_OPPORTUNITY_OWNER:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "opportunity semantic_owner must be AFQR-19"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldActorObjectHandoffCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    source_actor_entity_id: str
    recipient_actor_entity_id: str
    object_entity_id: str
    method: str
    place_id: str
    source_relation_id: str
    source_relation_type: str
    destination_relation_id: str
    destination_relation_type: str
    pre_state_digest: str
    post_state_digest: str
    preview_id: str
    state_delta_id: str
    rt010_qualification_id: str
    spatial_evidence_id: str
    opportunity_evidence_id: str
    status: str = "committed"

    def __post_init__(self) -> None:
        for name in (
            "receipt_id",
            "source_actor_entity_id",
            "recipient_actor_entity_id",
            "object_entity_id",
            "place_id",
            "source_relation_id",
            "destination_relation_id",
            "preview_id",
            "state_delta_id",
            "rt010_qualification_id",
            "spatial_evidence_id",
            "opportunity_evidence_id",
        ):
            _require_record_id(getattr(self, name), name)
        if not isinstance(self.command_id, str) or not self.command_id:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "command_id must be non-empty"
            )
        _require_sha256(self.command_fingerprint, "command_fingerprint")
        _require_sha256(self.pre_state_digest, "pre_state_digest")
        _require_sha256(self.post_state_digest, "post_state_digest")
        if self.source_actor_entity_id == self.recipient_actor_entity_id:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "source and recipient actors must differ"
            )
        if self.method != "handoff":
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "receipt method must be handoff"
            )
        if (
            self.source_relation_type != CARRIED_BY_RELATION_TYPE
            or self.destination_relation_type != CARRIED_BY_RELATION_TYPE
        ):
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "handoff relation types must be carried_by -> carried_by"
            )
        if self.status != "committed":
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "receipt status must be committed"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "source_actor_entity_id": self.source_actor_entity_id,
            "recipient_actor_entity_id": self.recipient_actor_entity_id,
            "object_entity_id": self.object_entity_id,
            "method": self.method,
            "place_id": self.place_id,
            "source_relation_id": self.source_relation_id,
            "source_relation_type": self.source_relation_type,
            "destination_relation_id": self.destination_relation_id,
            "destination_relation_type": self.destination_relation_type,
            "pre_state_digest": self.pre_state_digest,
            "post_state_digest": self.post_state_digest,
            "preview_id": self.preview_id,
            "state_delta_id": self.state_delta_id,
            "rt010_qualification_id": self.rt010_qualification_id,
            "spatial_evidence_id": self.spatial_evidence_id,
            "opportunity_evidence_id": self.opportunity_evidence_id,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldActorObjectHandoffCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldActorObjectHandoffCommitReceipt


@dataclass(frozen=True, kw_only=True)
class PersistentWorldActorObjectHandoffRuntimeState:
    displacement_state: PersistentWorldObjectDisplacementRuntimeState
    committed_actor_object_handoff_transitions: tuple[
        PersistentWorldActorObjectHandoffCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        if not isinstance(
            self.displacement_state,
            PersistentWorldObjectDisplacementRuntimeState,
        ):
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "displacement_state must be PersistentWorldObjectDisplacementRuntimeState"
            )
        transitions = tuple(self.committed_actor_object_handoff_transitions)
        for index, transition in enumerate(transitions):
            if not isinstance(
                transition,
                PersistentWorldActorObjectHandoffCommittedTransition,
            ):
                raise InvalidPersistentWorldActorObjectHandoffRequestError(
                    f"committed_actor_object_handoff_transitions[{index}] has invalid type"
                )
        ids = [item.command_id for item in transitions]
        if len(ids) != len(set(ids)):
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "actor-object handoff command IDs must be unique"
            )

        storage = self.displacement_state.storage_state
        lit = storage.lit_state
        open_close = lit.open_close_state
        custody = open_close.custody_state
        lower_ids = {
            item.command_id for item in custody.movement_state.committed_transitions
        }
        lower_ids.update(
            item.command_id for item in custody.committed_custody_transitions
        )
        lower_ids.update(
            item.command_id for item in open_close.committed_object_state_transitions
        )
        lower_ids.update(
            item.command_id for item in lit.committed_object_lit_transitions
        )
        lower_ids.update(
            item.command_id for item in storage.committed_storage_transitions
        )
        lower_ids.update(
            item.command_id
            for item in (
                self.displacement_state
                .committed_object_displacement_transitions
            )
        )
        if set(ids) & lower_ids:
            raise InvalidPersistentWorldActorObjectHandoffRequestError(
                "actor-object handoff command IDs must not collide with lower transitions"
            )
        validate_persistent_world_storage_placement(
            custody.movement_state.representation
        )
        object.__setattr__(
            self,
            "committed_actor_object_handoff_transitions",
            transitions,
        )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldActorObjectHandoffPreparedTransition:
    command_id: str
    command_fingerprint: str
    source_actor_entity_id: str
    recipient_actor_entity_id: str
    object_entity_id: str
    method: str
    place_id: str
    source_relation_id: str
    source_relation_type: str
    destination_relation_id: str
    destination_relation_type: str
    pre_state_digest: str
    post_state_digest: str
    rt010_qualification_id: str
    spatial_evidence_id: str
    opportunity_evidence_id: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    post_displacement_state: PersistentWorldObjectDisplacementRuntimeState


@dataclass(frozen=True, kw_only=True)
class PersistentWorldActorObjectHandoffExecutionResult:
    state: PersistentWorldActorObjectHandoffRuntimeState
    receipt: PersistentWorldActorObjectHandoffCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_actor_object_handoff_qualification_evidence(
    *,
    evidence_id: str,
    source_actor_entity_id: str,
    recipient_actor_entity_id: str,
    object_entity_id: str,
    method: str,
    qualified: bool,
) -> ActorObjectHandoffQualificationEvidence:
    return ActorObjectHandoffQualificationEvidence(
        evidence_id=evidence_id,
        source_actor_entity_id=source_actor_entity_id,
        recipient_actor_entity_id=recipient_actor_entity_id,
        object_entity_id=object_entity_id,
        method=method,
        qualified=qualified,
    )


def create_actor_object_handoff_spatial_evidence(
    *,
    evidence_id: str,
    source_actor_entity_id: str,
    recipient_actor_entity_id: str,
    object_entity_id: str,
    place_id: str,
    method: str,
    spatially_permitted: bool,
) -> ActorObjectHandoffSpatialEvidence:
    return ActorObjectHandoffSpatialEvidence(
        evidence_id=evidence_id,
        source_actor_entity_id=source_actor_entity_id,
        recipient_actor_entity_id=recipient_actor_entity_id,
        object_entity_id=object_entity_id,
        place_id=place_id,
        method=method,
        spatially_permitted=spatially_permitted,
    )


def create_actor_object_handoff_opportunity_evidence(
    *,
    evidence_id: str,
    source_actor_entity_id: str,
    recipient_actor_entity_id: str,
    object_entity_id: str,
    place_id: str,
    method: str,
    opportunity_available: bool,
    resolution_accepted: bool,
) -> ActorObjectHandoffOpportunityEvidence:
    return ActorObjectHandoffOpportunityEvidence(
        evidence_id=evidence_id,
        source_actor_entity_id=source_actor_entity_id,
        recipient_actor_entity_id=recipient_actor_entity_id,
        object_entity_id=object_entity_id,
        place_id=place_id,
        method=method,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def _representation(
    state: PersistentWorldActorObjectHandoffRuntimeState,
) -> PersistentWorldEntityLocationRepresentation:
    return (
        state.displacement_state.storage_state.lit_state.open_close_state
        .custody_state.movement_state.representation
    )


def _replace_representation_in_displacement_state(
    state: PersistentWorldObjectDisplacementRuntimeState,
    representation: PersistentWorldEntityLocationRepresentation,
) -> PersistentWorldObjectDisplacementRuntimeState:
    old_storage = state.storage_state
    old_lit = old_storage.lit_state
    old_open = old_lit.open_close_state
    old_custody = old_open.custody_state
    old_movement = old_custody.movement_state
    movement = PersistentWorldMovementRuntimeState(
        representation=representation,
        committed_transitions=old_movement.committed_transitions,
    )
    custody = PersistentWorldObjectCustodyRuntimeState(
        movement_state=movement,
        committed_custody_transitions=old_custody.committed_custody_transitions,
    )
    open_close = PersistentWorldObjectOpenCloseRuntimeState(
        custody_state=custody,
        object_open_states=old_open.object_open_states,
        committed_object_state_transitions=old_open.committed_object_state_transitions,
    )
    lit = PersistentWorldObjectLitRuntimeState(
        open_close_state=open_close,
        object_lit_states=old_lit.object_lit_states,
        committed_object_lit_transitions=old_lit.committed_object_lit_transitions,
    )
    storage = PersistentWorldObjectStorageRuntimeState(
        lit_state=lit,
        committed_storage_transitions=old_storage.committed_storage_transitions,
    )
    return PersistentWorldObjectDisplacementRuntimeState(
        storage_state=storage,
        committed_object_displacement_transitions=(
            state.committed_object_displacement_transitions
        ),
    )


def fingerprint_persistent_world_actor_object_handoff_command(
    command: CommandEnvelope,
) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            "command failed CommandEnvelope validation"
        )
    if command.command_type.strip().lower().replace("-", "_") != "transfer_object":
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            "VSM-6 requires transfer_object command type"
        )
    if command.payload.get("method") != "handoff":
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            "VSM-6 supports only handoff method"
        )
    try:
        return fingerprint_command_envelope(command, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            "command must be canonical JSON-compatible"
        ) from exc


def _validate_owner_evidence(
    *,
    qualification_evidence: ActorObjectHandoffQualificationEvidence,
    spatial_evidence: ActorObjectHandoffSpatialEvidence,
    opportunity_evidence: ActorObjectHandoffOpportunityEvidence,
    source_actor_entity_id: str,
    recipient_actor_entity_id: str,
    object_entity_id: str,
    place_id: str,
) -> None:
    if not isinstance(
        qualification_evidence,
        ActorObjectHandoffQualificationEvidence,
    ):
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "invalid RT-010 handoff qualification evidence"
        )
    if not isinstance(spatial_evidence, ActorObjectHandoffSpatialEvidence):
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "invalid AFQR-18 handoff spatial evidence"
        )
    if not isinstance(
        opportunity_evidence,
        ActorObjectHandoffOpportunityEvidence,
    ):
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "invalid AFQR-19 handoff opportunity evidence"
        )

    expected = (
        source_actor_entity_id,
        recipient_actor_entity_id,
        object_entity_id,
        place_id,
        "handoff",
    )
    if (
        spatial_evidence.source_actor_entity_id,
        spatial_evidence.recipient_actor_entity_id,
        spatial_evidence.object_entity_id,
        spatial_evidence.place_id,
        spatial_evidence.method,
    ) != expected:
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "AFQR-18 evidence does not match handoff transition"
        )
    if (
        opportunity_evidence.source_actor_entity_id,
        opportunity_evidence.recipient_actor_entity_id,
        opportunity_evidence.object_entity_id,
        opportunity_evidence.place_id,
        opportunity_evidence.method,
    ) != expected:
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "AFQR-19 evidence does not match handoff transition"
        )
    if (
        qualification_evidence.source_actor_entity_id
        != source_actor_entity_id
        or qualification_evidence.recipient_actor_entity_id
        != recipient_actor_entity_id
        or qualification_evidence.object_entity_id != object_entity_id
        or qualification_evidence.method != "handoff"
    ):
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "RT-010 evidence does not match handoff transition"
        )
    if not qualification_evidence.qualified:
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "RT-010 rejected handoff transition"
        )
    if not spatial_evidence.spatially_permitted:
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "AFQR-18 rejected handoff co-location"
        )
    if (
        not opportunity_evidence.opportunity_available
        or not opportunity_evidence.resolution_accepted
    ):
        raise PersistentWorldActorObjectHandoffEvidenceError(
            "AFQR-19 rejected handoff opportunity"
        )


def _apply_handoff(
    *,
    representation: PersistentWorldEntityLocationRepresentation,
    object_entity_id: str,
    source_actor_entity_id: str,
    recipient_actor_entity_id: str,
    source_relation_id: str,
    destination_relation_id: str,
) -> PersistentWorldEntityLocationRepresentation:
    sources = [
        relation
        for relation in representation.relations
        if relation.relation_id == source_relation_id
    ]
    if len(sources) != 1:
        raise PersistentWorldActorObjectHandoffPlacementError(
            "handoff source relation is absent or duplicated"
        )
    source = sources[0]
    if (
        source.relation_type != CARRIED_BY_RELATION_TYPE
        or source.subject_entity_id != object_entity_id
        or source.object_entity_id != source_actor_entity_id
    ):
        raise PersistentWorldActorObjectHandoffPlacementError(
            "handoff source must be target object carried by source actor"
        )
    remaining = [
        relation
        for relation in representation.relations
        if relation.relation_id != source_relation_id
    ]
    if any(r.relation_id == destination_relation_id for r in remaining):
        raise PersistentWorldActorObjectHandoffRelationIdentityCollisionError(
            "deterministic handoff destination relation ID collides"
        )
    destination = create_carried_by_relation(
        relation_id=destination_relation_id,
        subject_entity_id=object_entity_id,
        object_entity_id=recipient_actor_entity_id,
    )
    post = create_persistent_world_entity_location_representation(
        campaign_id=representation.campaign_id,
        entities=representation.entities,
        relations=(*remaining, destination),
    )
    validate_persistent_world_storage_placement(post)
    return post


def _existing_transition(
    state: PersistentWorldActorObjectHandoffRuntimeState,
    command_id: str,
):
    return find_committed_transition(
        state.committed_actor_object_handoff_transitions,
        command_id,
    )


def prepare_persistent_world_actor_object_handoff(
    *,
    state: PersistentWorldActorObjectHandoffRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ActorObjectHandoffQualificationEvidence,
    spatial_evidence: ActorObjectHandoffSpatialEvidence,
    opportunity_evidence: ActorObjectHandoffOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldActorObjectHandoffPreparedTransition:
    if not isinstance(state, PersistentWorldActorObjectHandoffRuntimeState):
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            "invalid actor-object handoff runtime state"
        )
    fingerprint = fingerprint_persistent_world_actor_object_handoff_command(
        command
    )
    source_actor_entity_id = command.source_actor_id
    recipient_actor_entity_id = _require_record_id(
        command.payload.get("recipient_actor_entity_id"),
        "command.payload.recipient_actor_entity_id",
    )
    object_entity_id = _require_record_id(
        command.payload.get("object_entity_id"),
        "command.payload.object_entity_id",
    )
    if source_actor_entity_id == recipient_actor_entity_id:
        raise PersistentWorldActorObjectHandoffEntityError(
            "source and recipient actors must differ"
        )

    representation = _representation(state)
    entities = {entity.entity_id: entity for entity in representation.entities}
    source_actor = entities.get(source_actor_entity_id)
    recipient_actor = entities.get(recipient_actor_entity_id)
    target = entities.get(object_entity_id)
    if (
        source_actor is None
        or source_actor.classification != "character_or_creature"
    ):
        raise PersistentWorldActorObjectHandoffEntityError(
            "source actor must exist and be character_or_creature"
        )
    if (
        recipient_actor is None
        or recipient_actor.classification != "character_or_creature"
    ):
        raise PersistentWorldActorObjectHandoffEntityError(
            "recipient actor must exist and be character_or_creature"
        )
    if target is None or target.classification != "object":
        raise PersistentWorldActorObjectHandoffEntityError(
            "handoff target must exist and be object"
        )

    def actor_place(actor_entity_id: str) -> str:
        locations = [
            relation
            for relation in representation.relations
            if relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == actor_entity_id
        ]
        if len(locations) != 1:
            raise PersistentWorldActorObjectHandoffPlacementError(
                "handoff actors require exactly one current location each"
            )
        return locations[0].object_entity_id

    source_place_id = actor_place(source_actor_entity_id)
    recipient_place_id = actor_place(recipient_actor_entity_id)
    if source_place_id != recipient_place_id:
        raise PersistentWorldActorObjectHandoffPlacementError(
            "handoff requires source and recipient actors to be co-located"
        )
    place_id = source_place_id

    placements = [
        relation
        for relation in representation.relations
        if relation.subject_entity_id == object_entity_id
        and relation.relation_type
        in {
            LOCATED_AT_RELATION_TYPE,
            CARRIED_BY_RELATION_TYPE,
            CONTAINED_BY_RELATION_TYPE,
        }
    ]
    if (
        len(placements) != 1
        or placements[0].relation_type != CARRIED_BY_RELATION_TYPE
        or placements[0].object_entity_id != source_actor_entity_id
    ):
        raise PersistentWorldActorObjectHandoffPlacementError(
            "handoff requires target object carried by source actor"
        )
    source_relation = placements[0]

    _validate_owner_evidence(
        qualification_evidence=qualification_evidence,
        spatial_evidence=spatial_evidence,
        opportunity_evidence=opportunity_evidence,
        source_actor_entity_id=source_actor_entity_id,
        recipient_actor_entity_id=recipient_actor_entity_id,
        object_entity_id=object_entity_id,
        place_id=place_id,
    )

    actual_digest = digest_persistent_world_entity_location_representation(
        representation
    )
    if expected_pre_state_digest != actual_digest:
        raise PersistentWorldActorObjectHandoffStaleStateError(
            "stale pre-state digest"
        )

    token = fingerprint[:24]
    destination_relation_id = build_record_id(
        "relation",
        f"actor-object-handoff-{token}",
    )
    if (
        destination_relation_id != source_relation.relation_id
        and any(
            relation.relation_id == destination_relation_id
            for relation in representation.relations
        )
    ):
        raise PersistentWorldActorObjectHandoffRelationIdentityCollisionError(
            "destination relation identity already exists"
        )

    preview = create_transaction_preview(
        preview_id=build_record_id("actor_object_handoff_preview", token),
        command=command,
        status="preview_created",
        messages=("bounded voluntary actor-object handoff prepared",),
        requires_confirmation=False,
        metadata={
            "package": "TERMINAL-PLAY-VSM-6",
            "command_family": "inventory",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("actor_object_handoff_delta", token),
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(
            source_actor_entity_id,
            recipient_actor_entity_id,
            object_entity_id,
            place_id,
            source_relation.relation_id,
            destination_relation_id,
        ),
        change_type="relationship_update",
        payload={
            "method": "handoff",
            "source_actor_entity_id": source_actor_entity_id,
            "recipient_actor_entity_id": recipient_actor_entity_id,
            "object_entity_id": object_entity_id,
            "place_id": place_id,
            "source_relation_id": source_relation.relation_id,
            "source_relation_type": source_relation.relation_type,
            "destination_relation_id": destination_relation_id,
            "destination_relation_type": CARRIED_BY_RELATION_TYPE,
        },
        metadata={
            "package": "TERMINAL-PLAY-VSM-6",
            "placement_semantic_owner": RT010_ACTOR_OBJECT_HANDOFF_OWNER,
            "spatial_semantic_owner": AFQR18_ACTOR_OBJECT_HANDOFF_SPATIAL_OWNER,
            "opportunity_semantic_owner": (
                AFQR19_ACTOR_OBJECT_HANDOFF_OPPORTUNITY_OWNER
            ),
            "qualified_transition_owner": "AFQR-01",
        },
    )

    post_representation = _apply_handoff(
        representation=representation,
        object_entity_id=object_entity_id,
        source_actor_entity_id=source_actor_entity_id,
        recipient_actor_entity_id=recipient_actor_entity_id,
        source_relation_id=source_relation.relation_id,
        destination_relation_id=destination_relation_id,
    )
    post_digest = digest_persistent_world_entity_location_representation(
        post_representation
    )
    return PersistentWorldActorObjectHandoffPreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        source_actor_entity_id=source_actor_entity_id,
        recipient_actor_entity_id=recipient_actor_entity_id,
        object_entity_id=object_entity_id,
        method="handoff",
        place_id=place_id,
        source_relation_id=source_relation.relation_id,
        source_relation_type=source_relation.relation_type,
        destination_relation_id=destination_relation_id,
        destination_relation_type=CARRIED_BY_RELATION_TYPE,
        pre_state_digest=actual_digest,
        post_state_digest=post_digest,
        rt010_qualification_id=qualification_evidence.evidence_id,
        spatial_evidence_id=spatial_evidence.evidence_id,
        opportunity_evidence_id=opportunity_evidence.evidence_id,
        preview=preview,
        state_delta=delta,
        post_displacement_state=_replace_representation_in_displacement_state(
            state.displacement_state,
            post_representation,
        ),
    )


def commit_prepared_persistent_world_actor_object_handoff(
    *,
    state: PersistentWorldActorObjectHandoffRuntimeState,
    prepared: PersistentWorldActorObjectHandoffPreparedTransition,
) -> PersistentWorldActorObjectHandoffExecutionResult:
    existing = _existing_transition(state, prepared.command_id)
    if existing is not None:
        if not command_fingerprint_matches(
            existing,
            prepared.command_fingerprint,
        ):
            raise PersistentWorldActorObjectHandoffRetryConflictError(
                "command ID already committed with different meaning"
            )
        return PersistentWorldActorObjectHandoffExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )

    current = digest_persistent_world_entity_location_representation(
        _representation(state)
    )
    if current != prepared.pre_state_digest:
        raise PersistentWorldActorObjectHandoffStaleStateError(
            "object placement changed after preparation"
        )

    receipt = PersistentWorldActorObjectHandoffCommitReceipt(
        receipt_id=build_record_id(
            "actor_object_handoff_receipt",
            prepared.command_fingerprint[:24],
        ),
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        source_actor_entity_id=prepared.source_actor_entity_id,
        recipient_actor_entity_id=prepared.recipient_actor_entity_id,
        object_entity_id=prepared.object_entity_id,
        method=prepared.method,
        place_id=prepared.place_id,
        source_relation_id=prepared.source_relation_id,
        source_relation_type=prepared.source_relation_type,
        destination_relation_id=prepared.destination_relation_id,
        destination_relation_type=prepared.destination_relation_type,
        pre_state_digest=prepared.pre_state_digest,
        post_state_digest=prepared.post_state_digest,
        preview_id=prepared.preview.preview_id,
        state_delta_id=prepared.state_delta.delta_id,
        rt010_qualification_id=prepared.rt010_qualification_id,
        spatial_evidence_id=prepared.spatial_evidence_id,
        opportunity_evidence_id=prepared.opportunity_evidence_id,
    )
    committed = PersistentWorldActorObjectHandoffCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    transitions = tuple(
        sorted(
            (*state.committed_actor_object_handoff_transitions, committed),
            key=lambda item: (item.command_id, item.command_fingerprint),
        )
    )
    post_state = PersistentWorldActorObjectHandoffRuntimeState(
        displacement_state=prepared.post_displacement_state,
        committed_actor_object_handoff_transitions=transitions,
    )
    return PersistentWorldActorObjectHandoffExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def execute_persistent_world_actor_object_handoff(
    *,
    state: PersistentWorldActorObjectHandoffRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ActorObjectHandoffQualificationEvidence,
    spatial_evidence: ActorObjectHandoffSpatialEvidence,
    opportunity_evidence: ActorObjectHandoffOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldActorObjectHandoffExecutionResult:
    fingerprint = fingerprint_persistent_world_actor_object_handoff_command(
        command
    )
    existing = _existing_transition(state, command.command_id)
    if existing is not None:
        if not command_fingerprint_matches(existing, fingerprint):
            raise PersistentWorldActorObjectHandoffRetryConflictError(
                "command ID already committed with materially different content"
            )
        return PersistentWorldActorObjectHandoffExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )
    prepared = prepare_persistent_world_actor_object_handoff(
        state=state,
        command=command,
        qualification_evidence=qualification_evidence,
        spatial_evidence=spatial_evidence,
        opportunity_evidence=opportunity_evidence,
        expected_pre_state_digest=expected_pre_state_digest,
    )
    return commit_prepared_persistent_world_actor_object_handoff(
        state=state,
        prepared=prepared,
    )


def replay_persistent_world_actor_object_handoff(
    *,
    pre_state_representation: PersistentWorldEntityLocationRepresentation,
    receipt: PersistentWorldActorObjectHandoffCommitReceipt,
) -> PersistentWorldEntityLocationRepresentation:
    if not isinstance(
        pre_state_representation,
        PersistentWorldEntityLocationRepresentation,
    ):
        raise PersistentWorldActorObjectHandoffReplayError(
            "invalid replay pre-state"
        )
    if not isinstance(
        receipt,
        PersistentWorldActorObjectHandoffCommitReceipt,
    ):
        raise PersistentWorldActorObjectHandoffReplayError(
            "receipt has invalid type"
        )
    if (
        digest_persistent_world_entity_location_representation(
            pre_state_representation
        )
        != receipt.pre_state_digest
    ):
        raise PersistentWorldActorObjectHandoffReplayError(
            "replay pre-state digest mismatch"
        )

    entities = {
        entity.entity_id: entity
        for entity in pre_state_representation.entities
    }
    for actor_id in (
        receipt.source_actor_entity_id,
        receipt.recipient_actor_entity_id,
    ):
        actor = entities.get(actor_id)
        if actor is None or actor.classification != "character_or_creature":
            raise PersistentWorldActorObjectHandoffReplayError(
                "replay actor is absent or ineligible"
            )
        places = [
            relation.object_entity_id
            for relation in pre_state_representation.relations
            if relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == actor_id
        ]
        if places != [receipt.place_id]:
            raise PersistentWorldActorObjectHandoffReplayError(
                "replay actors are not co-located at committed place"
            )

    try:
        post = _apply_handoff(
            representation=pre_state_representation,
            object_entity_id=receipt.object_entity_id,
            source_actor_entity_id=receipt.source_actor_entity_id,
            recipient_actor_entity_id=receipt.recipient_actor_entity_id,
            source_relation_id=receipt.source_relation_id,
            destination_relation_id=receipt.destination_relation_id,
        )
    except PersistentWorldActorObjectHandoffError as exc:
        raise PersistentWorldActorObjectHandoffReplayError(
            "committed actor-object handoff could not replay"
        ) from exc
    if (
        digest_persistent_world_entity_location_representation(post)
        != receipt.post_state_digest
    ):
        raise PersistentWorldActorObjectHandoffReplayError(
            "replay post-state digest mismatch"
        )
    return post


def serialize_persistent_world_actor_object_handoff_commit_receipt(
    receipt: PersistentWorldActorObjectHandoffCommitReceipt,
) -> dict[str, str]:
    if not isinstance(
        receipt,
        PersistentWorldActorObjectHandoffCommitReceipt,
    ):
        raise InvalidPersistentWorldActorObjectHandoffRequestError(
            "receipt must be PersistentWorldActorObjectHandoffCommitReceipt"
        )
    return receipt.to_dict()
