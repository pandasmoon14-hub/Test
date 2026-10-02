"""Bounded thrown-object displacement for TERMINAL-PLAY-COMP-3.

This module implements one deterministic immediate placement transition:
an object already carried by an actor may be thrown to one explicitly
qualified destination place.

Authority remains with existing semantic owners:
- RT-010: immediate physical carrying/asset placement;
- AFQR-18: direct place/location and bounded spatial qualification;
- AFQR-19: opportunity/resolution qualification;
- AFQR-01: qualified commitment;
- AFQR-02: command identity and technical retry.

This module does not implement projectile physics, trajectories, velocity,
range arithmetic, damage, attacks, accuracy, collision, line of sight,
movement adjacency, discovery, model calls, narration, or generalized
object-motion infrastructure.
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
    create_located_at_relation,
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


RT010_OBJECT_DISPLACEMENT_OWNER = "RT-010"
AFQR18_OBJECT_DISPLACEMENT_SPATIAL_OWNER = "AFQR-18"
AFQR19_OBJECT_DISPLACEMENT_OPPORTUNITY_OWNER = "AFQR-19"
OBJECT_DISPLACEMENT_METHODS = frozenset({"throw"})
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PersistentWorldObjectDisplacementError(ValueError):
    """Base bounded object-displacement failure."""


class InvalidPersistentWorldObjectDisplacementRequestError(
    PersistentWorldObjectDisplacementError
):
    pass


class PersistentWorldObjectDisplacementEntityError(
    PersistentWorldObjectDisplacementError
):
    pass


class PersistentWorldObjectDisplacementPlacementError(
    PersistentWorldObjectDisplacementError
):
    pass


class PersistentWorldObjectDisplacementEvidenceError(
    PersistentWorldObjectDisplacementError
):
    pass


class PersistentWorldObjectDisplacementStaleStateError(
    PersistentWorldObjectDisplacementError
):
    pass


class PersistentWorldObjectDisplacementRetryConflictError(
    PersistentWorldObjectDisplacementError
):
    pass


class PersistentWorldObjectDisplacementRelationIdentityCollisionError(
    PersistentWorldObjectDisplacementError
):
    pass


class PersistentWorldObjectDisplacementReplayError(
    PersistentWorldObjectDisplacementError
):
    pass


def _require_record_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            f"{label} must be a valid record ID"
        )
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            f"{label} must be a lowercase SHA-256 digest"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class ObjectDisplacementQualificationEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    method: str
    qualified: bool
    semantic_owner: str = RT010_OBJECT_DISPLACEMENT_OWNER

    def __post_init__(self) -> None:
        for name in ("evidence_id", "actor_entity_id", "object_entity_id"):
            _require_record_id(getattr(self, name), name)
        if self.method not in OBJECT_DISPLACEMENT_METHODS:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "method must be throw"
            )
        if type(self.qualified) is not bool:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "qualified must be bool"
            )
        if self.semantic_owner != RT010_OBJECT_DISPLACEMENT_OWNER:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "qualification semantic_owner must be RT-010"
            )


@dataclass(frozen=True, kw_only=True)
class ObjectDisplacementSpatialEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    source_place_id: str
    destination_place_id: str
    method: str
    spatially_permitted: bool
    semantic_owner: str = AFQR18_OBJECT_DISPLACEMENT_SPATIAL_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "actor_entity_id",
            "object_entity_id",
            "source_place_id",
            "destination_place_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.method not in OBJECT_DISPLACEMENT_METHODS:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "method must be throw"
            )
        if type(self.spatially_permitted) is not bool:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "spatially_permitted must be bool"
            )
        if self.semantic_owner != AFQR18_OBJECT_DISPLACEMENT_SPATIAL_OWNER:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "spatial semantic_owner must be AFQR-18"
            )


@dataclass(frozen=True, kw_only=True)
class ObjectDisplacementOpportunityEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    source_place_id: str
    destination_place_id: str
    method: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_OBJECT_DISPLACEMENT_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        for name in (
            "evidence_id",
            "actor_entity_id",
            "object_entity_id",
            "source_place_id",
            "destination_place_id",
        ):
            _require_record_id(getattr(self, name), name)
        if self.method not in OBJECT_DISPLACEMENT_METHODS:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "method must be throw"
            )
        if (
            type(self.opportunity_available) is not bool
            or type(self.resolution_accepted) is not bool
        ):
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "opportunity/resolution flags must be bool"
            )
        if self.semantic_owner != AFQR19_OBJECT_DISPLACEMENT_OPPORTUNITY_OWNER:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "opportunity semantic_owner must be AFQR-19"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectDisplacementCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    method: str
    source_place_id: str
    destination_place_id: str
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
            "actor_entity_id",
            "object_entity_id",
            "source_place_id",
            "destination_place_id",
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
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "command_id must be non-empty"
            )
        _require_sha256(self.command_fingerprint, "command_fingerprint")
        _require_sha256(self.pre_state_digest, "pre_state_digest")
        _require_sha256(self.post_state_digest, "post_state_digest")
        if self.method != "throw":
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "receipt method must be throw"
            )
        if self.source_place_id == self.destination_place_id:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "throw destination must differ from source"
            )
        if (
            self.source_relation_type != CARRIED_BY_RELATION_TYPE
            or self.destination_relation_type != LOCATED_AT_RELATION_TYPE
        ):
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "throw relation types must be carried_by -> located_at"
            )
        if self.status != "committed":
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "receipt status must be committed"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "actor_entity_id": self.actor_entity_id,
            "object_entity_id": self.object_entity_id,
            "method": self.method,
            "source_place_id": self.source_place_id,
            "destination_place_id": self.destination_place_id,
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
class PersistentWorldObjectDisplacementCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldObjectDisplacementCommitReceipt


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectDisplacementRuntimeState:
    storage_state: PersistentWorldObjectStorageRuntimeState
    committed_object_displacement_transitions: tuple[
        PersistentWorldObjectDisplacementCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.storage_state, PersistentWorldObjectStorageRuntimeState):
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "storage_state must be PersistentWorldObjectStorageRuntimeState"
            )
        transitions = tuple(self.committed_object_displacement_transitions)
        for index, transition in enumerate(transitions):
            if not isinstance(
                transition,
                PersistentWorldObjectDisplacementCommittedTransition,
            ):
                raise InvalidPersistentWorldObjectDisplacementRequestError(
                    f"committed_object_displacement_transitions[{index}] has invalid type"
                )
        ids = [item.command_id for item in transitions]
        if len(ids) != len(set(ids)):
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "object displacement command IDs must be unique"
            )
        lit = self.storage_state.lit_state
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
            item.command_id for item in self.storage_state.committed_storage_transitions
        )
        if set(ids) & lower_ids:
            raise InvalidPersistentWorldObjectDisplacementRequestError(
                "object displacement command IDs must not collide with lower transitions"
            )
        validate_persistent_world_storage_placement(
            custody.movement_state.representation
        )
        object.__setattr__(
            self,
            "committed_object_displacement_transitions",
            transitions,
        )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectDisplacementPreparedTransition:
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    method: str
    source_place_id: str
    destination_place_id: str
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
    post_storage_state: PersistentWorldObjectStorageRuntimeState


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectDisplacementExecutionResult:
    state: PersistentWorldObjectDisplacementRuntimeState
    receipt: PersistentWorldObjectDisplacementCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_object_displacement_qualification_evidence(
    *,
    evidence_id: str,
    actor_entity_id: str,
    object_entity_id: str,
    method: str,
    qualified: bool,
) -> ObjectDisplacementQualificationEvidence:
    return ObjectDisplacementQualificationEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        method=method,
        qualified=qualified,
    )


def create_object_displacement_spatial_evidence(
    *,
    evidence_id: str,
    actor_entity_id: str,
    object_entity_id: str,
    source_place_id: str,
    destination_place_id: str,
    method: str,
    spatially_permitted: bool,
) -> ObjectDisplacementSpatialEvidence:
    return ObjectDisplacementSpatialEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        method=method,
        spatially_permitted=spatially_permitted,
    )


def create_object_displacement_opportunity_evidence(
    *,
    evidence_id: str,
    actor_entity_id: str,
    object_entity_id: str,
    source_place_id: str,
    destination_place_id: str,
    method: str,
    opportunity_available: bool,
    resolution_accepted: bool,
) -> ObjectDisplacementOpportunityEvidence:
    return ObjectDisplacementOpportunityEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        method=method,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def _representation(
    state: PersistentWorldObjectDisplacementRuntimeState,
) -> PersistentWorldEntityLocationRepresentation:
    return (
        state.storage_state.lit_state.open_close_state.custody_state
        .movement_state.representation
    )


def _replace_representation_in_storage_state(
    state: PersistentWorldObjectStorageRuntimeState,
    representation: PersistentWorldEntityLocationRepresentation,
) -> PersistentWorldObjectStorageRuntimeState:
    old_lit = state.lit_state
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
    return PersistentWorldObjectStorageRuntimeState(
        lit_state=lit,
        committed_storage_transitions=state.committed_storage_transitions,
    )


def fingerprint_persistent_world_object_displacement_command(
    command: CommandEnvelope,
) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            "command failed CommandEnvelope validation"
        )
    if command.command_type.strip().lower().replace("-", "_") != "transfer_object":
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            "COMP-3 requires transfer_object command type"
        )
    if command.payload.get("method") != "throw":
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            "COMP-3 supports only throw method"
        )
    try:
        return fingerprint_command_envelope(command, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            "command must be canonical JSON-compatible"
        ) from exc


def _validate_owner_evidence(
    *,
    qualification_evidence: ObjectDisplacementQualificationEvidence,
    spatial_evidence: ObjectDisplacementSpatialEvidence,
    opportunity_evidence: ObjectDisplacementOpportunityEvidence,
    actor_entity_id: str,
    object_entity_id: str,
    source_place_id: str,
    destination_place_id: str,
) -> None:
    if not isinstance(
        qualification_evidence,
        ObjectDisplacementQualificationEvidence,
    ):
        raise PersistentWorldObjectDisplacementEvidenceError(
            "invalid RT-010 displacement qualification evidence"
        )
    if not isinstance(spatial_evidence, ObjectDisplacementSpatialEvidence):
        raise PersistentWorldObjectDisplacementEvidenceError(
            "invalid AFQR-18 displacement spatial evidence"
        )
    if not isinstance(
        opportunity_evidence,
        ObjectDisplacementOpportunityEvidence,
    ):
        raise PersistentWorldObjectDisplacementEvidenceError(
            "invalid AFQR-19 displacement opportunity evidence"
        )

    expected = (
        actor_entity_id,
        object_entity_id,
        source_place_id,
        destination_place_id,
        "throw",
    )
    if (
        spatial_evidence.actor_entity_id,
        spatial_evidence.object_entity_id,
        spatial_evidence.source_place_id,
        spatial_evidence.destination_place_id,
        spatial_evidence.method,
    ) != expected:
        raise PersistentWorldObjectDisplacementEvidenceError(
            "AFQR-18 evidence does not match displacement transition"
        )
    if (
        opportunity_evidence.actor_entity_id,
        opportunity_evidence.object_entity_id,
        opportunity_evidence.source_place_id,
        opportunity_evidence.destination_place_id,
        opportunity_evidence.method,
    ) != expected:
        raise PersistentWorldObjectDisplacementEvidenceError(
            "AFQR-19 evidence does not match displacement transition"
        )
    if (
        qualification_evidence.actor_entity_id != actor_entity_id
        or qualification_evidence.object_entity_id != object_entity_id
        or qualification_evidence.method != "throw"
    ):
        raise PersistentWorldObjectDisplacementEvidenceError(
            "RT-010 evidence does not match displacement transition"
        )
    if not qualification_evidence.qualified:
        raise PersistentWorldObjectDisplacementEvidenceError(
            "RT-010 rejected displacement transition"
        )
    if not spatial_evidence.spatially_permitted:
        raise PersistentWorldObjectDisplacementEvidenceError(
            "AFQR-18 rejected displacement destination"
        )
    if (
        not opportunity_evidence.opportunity_available
        or not opportunity_evidence.resolution_accepted
    ):
        raise PersistentWorldObjectDisplacementEvidenceError(
            "AFQR-19 rejected displacement opportunity"
        )


def _apply_displacement(
    *,
    representation: PersistentWorldEntityLocationRepresentation,
    object_entity_id: str,
    actor_entity_id: str,
    destination_place_id: str,
    source_relation_id: str,
    destination_relation_id: str,
) -> PersistentWorldEntityLocationRepresentation:
    sources = [
        relation
        for relation in representation.relations
        if relation.relation_id == source_relation_id
    ]
    if len(sources) != 1:
        raise PersistentWorldObjectDisplacementPlacementError(
            "displacement source relation is absent or duplicated"
        )
    source = sources[0]
    if (
        source.relation_type != CARRIED_BY_RELATION_TYPE
        or source.subject_entity_id != object_entity_id
        or source.object_entity_id != actor_entity_id
    ):
        raise PersistentWorldObjectDisplacementPlacementError(
            "throw source must be target object carried by source actor"
        )
    remaining = [
        relation
        for relation in representation.relations
        if relation.relation_id != source_relation_id
    ]
    if any(r.relation_id == destination_relation_id for r in remaining):
        raise PersistentWorldObjectDisplacementRelationIdentityCollisionError(
            "deterministic displacement destination relation ID collides"
        )
    destination = create_located_at_relation(
        relation_id=destination_relation_id,
        subject_entity_id=object_entity_id,
        object_entity_id=destination_place_id,
    )
    post = create_persistent_world_entity_location_representation(
        campaign_id=representation.campaign_id,
        entities=representation.entities,
        relations=(*remaining, destination),
    )
    validate_persistent_world_storage_placement(post)
    return post


def _existing_transition(
    state: PersistentWorldObjectDisplacementRuntimeState,
    command_id: str,
):
    return find_committed_transition(
        state.committed_object_displacement_transitions,
        command_id,
    )


def prepare_persistent_world_object_displacement(
    *,
    state: PersistentWorldObjectDisplacementRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectDisplacementQualificationEvidence,
    spatial_evidence: ObjectDisplacementSpatialEvidence,
    opportunity_evidence: ObjectDisplacementOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectDisplacementPreparedTransition:
    if not isinstance(state, PersistentWorldObjectDisplacementRuntimeState):
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            "invalid object displacement runtime state"
        )
    fingerprint = fingerprint_persistent_world_object_displacement_command(command)
    actor_entity_id = command.source_actor_id
    object_entity_id = _require_record_id(
        command.payload.get("object_entity_id"),
        "command.payload.object_entity_id",
    )
    destination_place_id = _require_record_id(
        command.payload.get("destination_entity_id"),
        "command.payload.destination_entity_id",
    )

    representation = _representation(state)
    entities = {entity.entity_id: entity for entity in representation.entities}
    actor = entities.get(actor_entity_id)
    target = entities.get(object_entity_id)
    destination = entities.get(destination_place_id)
    if actor is None or actor.classification != "character_or_creature":
        raise PersistentWorldObjectDisplacementEntityError(
            "actor must exist and be character_or_creature"
        )
    if target is None or target.classification != "object":
        raise PersistentWorldObjectDisplacementEntityError(
            "displacement target must exist and be object"
        )
    if destination is None or destination.classification != "place":
        raise PersistentWorldObjectDisplacementEntityError(
            "displacement destination must exist and be place"
        )

    actor_locations = [
        relation
        for relation in representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == actor_entity_id
    ]
    if len(actor_locations) != 1:
        raise PersistentWorldObjectDisplacementPlacementError(
            "actor requires exactly one current location"
        )
    source_place_id = actor_locations[0].object_entity_id
    if source_place_id == destination_place_id:
        raise PersistentWorldObjectDisplacementPlacementError(
            "throw destination must differ from actor source place"
        )

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
        or placements[0].object_entity_id != actor_entity_id
    ):
        raise PersistentWorldObjectDisplacementPlacementError(
            "throw requires target object carried by source actor"
        )
    source_relation = placements[0]

    _validate_owner_evidence(
        qualification_evidence=qualification_evidence,
        spatial_evidence=spatial_evidence,
        opportunity_evidence=opportunity_evidence,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
    )

    actual_digest = digest_persistent_world_entity_location_representation(
        representation
    )
    if expected_pre_state_digest != actual_digest:
        raise PersistentWorldObjectDisplacementStaleStateError(
            "stale pre-state digest"
        )

    token = fingerprint[:24]
    destination_relation_id = build_record_id(
        "relation",
        f"object-displacement-{token}",
    )
    if (
        destination_relation_id != source_relation.relation_id
        and any(
            relation.relation_id == destination_relation_id
            for relation in representation.relations
        )
    ):
        raise PersistentWorldObjectDisplacementRelationIdentityCollisionError(
            "destination relation identity already exists"
        )

    preview = create_transaction_preview(
        preview_id=build_record_id("object_displacement_preview", token),
        command=command,
        status="preview_created",
        messages=("bounded thrown-object displacement prepared",),
        requires_confirmation=False,
        metadata={
            "package": "TERMINAL-PLAY-COMP-3",
            "command_family": "inventory",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("object_displacement_delta", token),
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(
            actor_entity_id,
            object_entity_id,
            source_place_id,
            destination_place_id,
            source_relation.relation_id,
            destination_relation_id,
        ),
        change_type="relationship_update",
        payload={
            "method": "throw",
            "actor_entity_id": actor_entity_id,
            "object_entity_id": object_entity_id,
            "source_place_id": source_place_id,
            "destination_place_id": destination_place_id,
            "source_relation_id": source_relation.relation_id,
            "source_relation_type": source_relation.relation_type,
            "destination_relation_id": destination_relation_id,
            "destination_relation_type": LOCATED_AT_RELATION_TYPE,
        },
        metadata={
            "package": "TERMINAL-PLAY-COMP-3",
            "placement_semantic_owner": RT010_OBJECT_DISPLACEMENT_OWNER,
            "spatial_semantic_owner": AFQR18_OBJECT_DISPLACEMENT_SPATIAL_OWNER,
            "opportunity_semantic_owner": (
                AFQR19_OBJECT_DISPLACEMENT_OPPORTUNITY_OWNER
            ),
            "qualified_transition_owner": "AFQR-01",
        },
    )

    post_representation = _apply_displacement(
        representation=representation,
        object_entity_id=object_entity_id,
        actor_entity_id=actor_entity_id,
        destination_place_id=destination_place_id,
        source_relation_id=source_relation.relation_id,
        destination_relation_id=destination_relation_id,
    )
    post_digest = digest_persistent_world_entity_location_representation(
        post_representation
    )
    return PersistentWorldObjectDisplacementPreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        method="throw",
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        source_relation_id=source_relation.relation_id,
        source_relation_type=source_relation.relation_type,
        destination_relation_id=destination_relation_id,
        destination_relation_type=LOCATED_AT_RELATION_TYPE,
        pre_state_digest=actual_digest,
        post_state_digest=post_digest,
        rt010_qualification_id=qualification_evidence.evidence_id,
        spatial_evidence_id=spatial_evidence.evidence_id,
        opportunity_evidence_id=opportunity_evidence.evidence_id,
        preview=preview,
        state_delta=delta,
        post_storage_state=_replace_representation_in_storage_state(
            state.storage_state,
            post_representation,
        ),
    )


def commit_prepared_persistent_world_object_displacement(
    *,
    state: PersistentWorldObjectDisplacementRuntimeState,
    prepared: PersistentWorldObjectDisplacementPreparedTransition,
) -> PersistentWorldObjectDisplacementExecutionResult:
    existing = _existing_transition(state, prepared.command_id)
    if existing is not None:
        if not command_fingerprint_matches(existing, prepared.command_fingerprint):
            raise PersistentWorldObjectDisplacementRetryConflictError(
                "command ID already committed with different meaning"
            )
        return PersistentWorldObjectDisplacementExecutionResult(
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
        raise PersistentWorldObjectDisplacementStaleStateError(
            "object placement changed after preparation"
        )

    receipt = PersistentWorldObjectDisplacementCommitReceipt(
        receipt_id=build_record_id(
            "object_displacement_receipt",
            prepared.command_fingerprint[:24],
        ),
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        actor_entity_id=prepared.actor_entity_id,
        object_entity_id=prepared.object_entity_id,
        method=prepared.method,
        source_place_id=prepared.source_place_id,
        destination_place_id=prepared.destination_place_id,
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
    committed = PersistentWorldObjectDisplacementCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    transitions = tuple(
        sorted(
            (*state.committed_object_displacement_transitions, committed),
            key=lambda item: (item.command_id, item.command_fingerprint),
        )
    )
    post_state = PersistentWorldObjectDisplacementRuntimeState(
        storage_state=prepared.post_storage_state,
        committed_object_displacement_transitions=transitions,
    )
    return PersistentWorldObjectDisplacementExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def execute_persistent_world_object_displacement(
    *,
    state: PersistentWorldObjectDisplacementRuntimeState,
    command: CommandEnvelope,
    qualification_evidence: ObjectDisplacementQualificationEvidence,
    spatial_evidence: ObjectDisplacementSpatialEvidence,
    opportunity_evidence: ObjectDisplacementOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectDisplacementExecutionResult:
    fingerprint = fingerprint_persistent_world_object_displacement_command(command)
    existing = _existing_transition(state, command.command_id)
    if existing is not None:
        if not command_fingerprint_matches(existing, fingerprint):
            raise PersistentWorldObjectDisplacementRetryConflictError(
                "command ID already committed with materially different content"
            )
        return PersistentWorldObjectDisplacementExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )
    prepared = prepare_persistent_world_object_displacement(
        state=state,
        command=command,
        qualification_evidence=qualification_evidence,
        spatial_evidence=spatial_evidence,
        opportunity_evidence=opportunity_evidence,
        expected_pre_state_digest=expected_pre_state_digest,
    )
    return commit_prepared_persistent_world_object_displacement(
        state=state,
        prepared=prepared,
    )


def replay_persistent_world_object_displacement(
    *,
    pre_state_representation: PersistentWorldEntityLocationRepresentation,
    receipt: PersistentWorldObjectDisplacementCommitReceipt,
) -> PersistentWorldEntityLocationRepresentation:
    if not isinstance(
        pre_state_representation,
        PersistentWorldEntityLocationRepresentation,
    ):
        raise PersistentWorldObjectDisplacementReplayError(
            "invalid replay pre-state"
        )
    if not isinstance(receipt, PersistentWorldObjectDisplacementCommitReceipt):
        raise PersistentWorldObjectDisplacementReplayError(
            "receipt has invalid type"
        )
    if (
        digest_persistent_world_entity_location_representation(
            pre_state_representation
        )
        != receipt.pre_state_digest
    ):
        raise PersistentWorldObjectDisplacementReplayError(
            "replay pre-state digest mismatch"
        )
    try:
        post = _apply_displacement(
            representation=pre_state_representation,
            object_entity_id=receipt.object_entity_id,
            actor_entity_id=receipt.actor_entity_id,
            destination_place_id=receipt.destination_place_id,
            source_relation_id=receipt.source_relation_id,
            destination_relation_id=receipt.destination_relation_id,
        )
    except PersistentWorldObjectDisplacementError as exc:
        raise PersistentWorldObjectDisplacementReplayError(
            "committed displacement could not replay"
        ) from exc
    if (
        digest_persistent_world_entity_location_representation(post)
        != receipt.post_state_digest
    ):
        raise PersistentWorldObjectDisplacementReplayError(
            "replay post-state digest mismatch"
        )
    return post


def serialize_persistent_world_object_displacement_commit_receipt(
    receipt: PersistentWorldObjectDisplacementCommitReceipt,
) -> dict[str, str]:
    if not isinstance(receipt, PersistentWorldObjectDisplacementCommitReceipt):
        raise InvalidPersistentWorldObjectDisplacementRequestError(
            "receipt must be PersistentWorldObjectDisplacementCommitReceipt"
        )
    return receipt.to_dict()
