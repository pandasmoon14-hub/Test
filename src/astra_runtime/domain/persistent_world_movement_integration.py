"""R4-C bounded persistent-world playable movement integration.

This module implements one deterministic in-memory movement transition
over the R4-B persistent-world entity/location representation.

Authority remains routed to existing semantic owners:

- AFQR-02: command identity and technical retry semantics;
- AFQR-03: action representation;
- AFQR-18: spatial/location semantics;
- AFQR-19: opportunity and target/resolution evidence;
- AFQR-01: qualified authoritative transition semantics;
- AFQR-09: generalized relation lifecycle remains outside this module.

This module does not implement durable persistence, generalized replay,
generalized transaction coordination, a world-state manager, pathfinding,
adjacency, movement speed, stamina, travel time, terrain costs, encounters,
networking, RNG, model calls, narration, or canon authority.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from astra_runtime.domain.command_kind_routing_skeleton import (
    route_command_envelope,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntity,
    PersistentWorldEntityLocationRepresentation,
    PersistentWorldRelation,
    canonical_serialize_persistent_world_entity_location_representation,
    create_located_at_relation,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    validate_command_envelope,
)
from astra_runtime.kernel.record_identity import (
    build_record_id,
    is_valid_record_id,
)
from astra_runtime.kernel.state_delta import (
    StateDeltaEnvelope,
    create_state_delta_envelope,
)
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    create_transaction_preview,
)


__all__ = [
    "AFQR18_SPATIAL_OWNER",
    "AFQR19_OPPORTUNITY_OWNER",
    "PersistentWorldMovementIntegrationError",
    "InvalidPersistentWorldMovementRequestError",
    "UnsupportedPersistentWorldMovementCommandError",
    "PersistentWorldMovementEntityNotFoundError",
    "PersistentWorldMovementDestinationNotPlaceError",
    "PersistentWorldMovementSourceLocationError",
    "PersistentWorldMovementOwnerEvidenceError",
    "PersistentWorldMovementStaleStateError",
    "PersistentWorldMovementRetryConflictError",
    "PersistentWorldMovementRelationIdentityCollisionError",
    "PersistentWorldMovementReplayError",
    "MovementSpatialEvidence",
    "MovementOpportunityEvidence",
    "PersistentWorldMovementCommitReceipt",
    "PersistentWorldMovementCommittedTransition",
    "PersistentWorldMovementRuntimeState",
    "PersistentWorldMovementPreparedTransition",
    "PersistentWorldMovementExecutionResult",
    "create_movement_spatial_evidence",
    "create_movement_opportunity_evidence",
    "create_persistent_world_movement_runtime_state",
    "digest_persistent_world_entity_location_representation",
    "fingerprint_persistent_world_movement_command",
    "prepare_persistent_world_movement",
    "commit_prepared_persistent_world_movement",
    "execute_persistent_world_movement",
    "replay_persistent_world_movement",
    "serialize_persistent_world_movement_commit_receipt",
    "canonical_serialize_persistent_world_movement_commit_receipt",
]


AFQR18_SPATIAL_OWNER = "AFQR-18"
AFQR19_OPPORTUNITY_OWNER = "AFQR-19"


class PersistentWorldMovementIntegrationError(ValueError):
    """Base error for the bounded R4-C movement implementation."""


class InvalidPersistentWorldMovementRequestError(
    PersistentWorldMovementIntegrationError
):
    """Raised when a movement request is structurally invalid."""


class UnsupportedPersistentWorldMovementCommandError(
    PersistentWorldMovementIntegrationError
):
    """Raised when a command does not route through movement."""


class PersistentWorldMovementEntityNotFoundError(
    PersistentWorldMovementIntegrationError
):
    """Raised when a required entity does not exist."""


class PersistentWorldMovementDestinationNotPlaceError(
    PersistentWorldMovementIntegrationError
):
    """Raised when the destination is not a place."""


class PersistentWorldMovementSourceLocationError(
    PersistentWorldMovementIntegrationError
):
    """Raised when current-location cardinality is invalid."""


class PersistentWorldMovementOwnerEvidenceError(
    PersistentWorldMovementIntegrationError
):
    """Raised when AFQR-18/19 evidence is absent or inconsistent."""


class PersistentWorldMovementStaleStateError(
    PersistentWorldMovementIntegrationError
):
    """Raised when the frozen pre-state basis no longer matches."""


class PersistentWorldMovementRetryConflictError(
    PersistentWorldMovementIntegrationError
):
    """Raised when one command ID is reused with changed meaning."""


class PersistentWorldMovementRelationIdentityCollisionError(
    PersistentWorldMovementIntegrationError
):
    """Raised if a deterministic bounded relation ID collides."""


class PersistentWorldMovementReplayError(
    PersistentWorldMovementIntegrationError
):
    """Raised when committed evidence cannot replay exactly."""


def _require_record_id(
    value: object,
    label: str,
    error_cls: type[Exception],
) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise error_cls(
            f"{label} must be a valid existing RecordId, got: {value!r}"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class MovementSpatialEvidence:
    evidence_id: str
    actor_entity_id: str
    source_place_id: str
    destination_place_id: str
    spatially_permitted: bool
    semantic_owner: str = AFQR18_SPATIAL_OWNER

    def __post_init__(self) -> None:
        _require_record_id(
            self.evidence_id,
            "evidence_id",
            PersistentWorldMovementOwnerEvidenceError,
        )
        _require_record_id(
            self.actor_entity_id,
            "actor_entity_id",
            PersistentWorldMovementOwnerEvidenceError,
        )
        _require_record_id(
            self.source_place_id,
            "source_place_id",
            PersistentWorldMovementOwnerEvidenceError,
        )
        _require_record_id(
            self.destination_place_id,
            "destination_place_id",
            PersistentWorldMovementOwnerEvidenceError,
        )

        if type(self.spatially_permitted) is not bool:
            raise PersistentWorldMovementOwnerEvidenceError(
                "spatially_permitted must be bool"
            )

        if self.semantic_owner != AFQR18_SPATIAL_OWNER:
            raise PersistentWorldMovementOwnerEvidenceError(
                "movement spatial evidence semantic_owner must be AFQR-18"
            )


@dataclass(frozen=True, kw_only=True)
class MovementOpportunityEvidence:
    evidence_id: str
    actor_entity_id: str
    destination_place_id: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        _require_record_id(
            self.evidence_id,
            "evidence_id",
            PersistentWorldMovementOwnerEvidenceError,
        )
        _require_record_id(
            self.actor_entity_id,
            "actor_entity_id",
            PersistentWorldMovementOwnerEvidenceError,
        )
        _require_record_id(
            self.destination_place_id,
            "destination_place_id",
            PersistentWorldMovementOwnerEvidenceError,
        )

        if type(self.opportunity_available) is not bool:
            raise PersistentWorldMovementOwnerEvidenceError(
                "opportunity_available must be bool"
            )

        if type(self.resolution_accepted) is not bool:
            raise PersistentWorldMovementOwnerEvidenceError(
                "resolution_accepted must be bool"
            )

        if self.semantic_owner != AFQR19_OPPORTUNITY_OWNER:
            raise PersistentWorldMovementOwnerEvidenceError(
                "movement opportunity evidence semantic_owner must be AFQR-19"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldMovementCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    source_place_id: str
    destination_place_id: str
    source_relation_id: str
    destination_relation_id: str
    pre_state_digest: str
    post_state_digest: str
    preview_id: str
    state_delta_id: str
    spatial_evidence_id: str
    opportunity_evidence_id: str
    status: str = "committed"

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "actor_entity_id": self.actor_entity_id,
            "source_place_id": self.source_place_id,
            "destination_place_id": self.destination_place_id,
            "source_relation_id": self.source_relation_id,
            "destination_relation_id": self.destination_relation_id,
            "pre_state_digest": self.pre_state_digest,
            "post_state_digest": self.post_state_digest,
            "preview_id": self.preview_id,
            "state_delta_id": self.state_delta_id,
            "spatial_evidence_id": self.spatial_evidence_id,
            "opportunity_evidence_id": self.opportunity_evidence_id,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldMovementCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldMovementCommitReceipt


@dataclass(frozen=True, kw_only=True)
class PersistentWorldMovementRuntimeState:
    """Bounded immutable R4-C state, not a generalized state manager."""

    representation: PersistentWorldEntityLocationRepresentation
    committed_transitions: tuple[
        PersistentWorldMovementCommittedTransition, ...
    ] = ()

    def __post_init__(self) -> None:
        if not isinstance(
            self.representation,
            PersistentWorldEntityLocationRepresentation,
        ):
            raise InvalidPersistentWorldMovementRequestError(
                "representation must be the R4-B persistent-world "
                "entity/location representation"
            )

        transitions = tuple(self.committed_transitions)

        for index, transition in enumerate(transitions):
            if not isinstance(
                transition,
                PersistentWorldMovementCommittedTransition,
            ):
                raise InvalidPersistentWorldMovementRequestError(
                    "committed_transitions"
                    f"[{index}] has invalid type"
                )

        command_ids = [
            transition.command_id
            for transition in transitions
        ]

        if len(command_ids) != len(set(command_ids)):
            raise InvalidPersistentWorldMovementRequestError(
                "committed movement command IDs must be unique"
            )

        object.__setattr__(
            self,
            "committed_transitions",
            transitions,
        )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldMovementPreparedTransition:
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    source_place_id: str
    destination_place_id: str
    source_relation_id: str
    destination_relation_id: str
    pre_state_digest: str
    post_state_digest: str
    routing_family: str
    owner_route: str
    spatial_evidence_id: str
    opportunity_evidence_id: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    post_representation: PersistentWorldEntityLocationRepresentation


@dataclass(frozen=True, kw_only=True)
class PersistentWorldMovementExecutionResult:
    state: PersistentWorldMovementRuntimeState
    receipt: PersistentWorldMovementCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_movement_spatial_evidence(
    *,
    evidence_id: str,
    actor_entity_id: str,
    source_place_id: str,
    destination_place_id: str,
    spatially_permitted: bool,
) -> MovementSpatialEvidence:
    return MovementSpatialEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        spatially_permitted=spatially_permitted,
    )


def create_movement_opportunity_evidence(
    *,
    evidence_id: str,
    actor_entity_id: str,
    destination_place_id: str,
    opportunity_available: bool,
    resolution_accepted: bool,
) -> MovementOpportunityEvidence:
    return MovementOpportunityEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        destination_place_id=destination_place_id,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def create_persistent_world_movement_runtime_state(
    *,
    representation: PersistentWorldEntityLocationRepresentation,
) -> PersistentWorldMovementRuntimeState:
    return PersistentWorldMovementRuntimeState(
        representation=representation,
    )


def digest_persistent_world_entity_location_representation(
    representation: PersistentWorldEntityLocationRepresentation,
) -> str:
    canonical = (
        canonical_serialize_persistent_world_entity_location_representation(
            representation
        )
    )
    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def fingerprint_persistent_world_movement_command(
    command: CommandEnvelope,
) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldMovementRequestError(
            "command failed CommandEnvelope validation"
        )

    try:
        canonical = json.dumps(
            command.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
    except (TypeError, ValueError) as exc:
        raise InvalidPersistentWorldMovementRequestError(
            "command payload and metadata must be deterministically "
            "JSON-serializable"
        ) from exc

    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def _entity_by_id(
    representation: PersistentWorldEntityLocationRepresentation,
) -> dict[str, PersistentWorldEntity]:
    return {
        entity.entity_id: entity
        for entity in representation.entities
    }


def _current_location_relation(
    representation: PersistentWorldEntityLocationRepresentation,
    actor_entity_id: str,
) -> PersistentWorldRelation:
    matches = [
        relation
        for relation in representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == actor_entity_id
        )
    ]

    if len(matches) != 1:
        raise PersistentWorldMovementSourceLocationError(
            "bounded movement requires exactly one active "
            f"located_at relation for {actor_entity_id!r}; "
            f"observed {len(matches)}"
        )

    return matches[0]


def _destination_from_command(
    command: CommandEnvelope,
) -> str:
    destination = command.payload.get(
        "destination_entity_id"
    )

    return _require_record_id(
        destination,
        "command.payload.destination_entity_id",
        InvalidPersistentWorldMovementRequestError,
    )


def _validate_owner_evidence(
    *,
    spatial_evidence: MovementSpatialEvidence,
    opportunity_evidence: MovementOpportunityEvidence,
    actor_entity_id: str,
    source_place_id: str,
    destination_place_id: str,
) -> None:
    if not isinstance(
        spatial_evidence,
        MovementSpatialEvidence,
    ):
        raise PersistentWorldMovementOwnerEvidenceError(
            "spatial_evidence must be MovementSpatialEvidence"
        )

    if not isinstance(
        opportunity_evidence,
        MovementOpportunityEvidence,
    ):
        raise PersistentWorldMovementOwnerEvidenceError(
            "opportunity_evidence must be MovementOpportunityEvidence"
        )

    if (
        spatial_evidence.actor_entity_id
        != actor_entity_id
        or spatial_evidence.source_place_id
        != source_place_id
        or spatial_evidence.destination_place_id
        != destination_place_id
    ):
        raise PersistentWorldMovementOwnerEvidenceError(
            "AFQR-18 movement evidence does not match the "
            "bounded movement transition"
        )

    if not spatial_evidence.spatially_permitted:
        raise PersistentWorldMovementOwnerEvidenceError(
            "AFQR-18 movement evidence rejected the movement"
        )

    if (
        opportunity_evidence.actor_entity_id
        != actor_entity_id
        or opportunity_evidence.destination_place_id
        != destination_place_id
    ):
        raise PersistentWorldMovementOwnerEvidenceError(
            "AFQR-19 opportunity evidence does not match the "
            "bounded movement transition"
        )

    if not opportunity_evidence.opportunity_available:
        raise PersistentWorldMovementOwnerEvidenceError(
            "AFQR-19 reports no lawful movement opportunity"
        )

    if not opportunity_evidence.resolution_accepted:
        raise PersistentWorldMovementOwnerEvidenceError(
            "AFQR-19 movement resolution was rejected"
        )


def _apply_location_change(
    *,
    representation: PersistentWorldEntityLocationRepresentation,
    actor_entity_id: str,
    source_relation_id: str,
    destination_relation_id: str,
    destination_place_id: str,
) -> PersistentWorldEntityLocationRepresentation:
    remaining_relations = [
        relation
        for relation in representation.relations
        if relation.relation_id != source_relation_id
    ]

    if len(remaining_relations) == len(
        representation.relations
    ):
        raise PersistentWorldMovementReplayError(
            "source located_at relation is absent"
        )

    if any(
        relation.relation_id == destination_relation_id
        for relation in remaining_relations
    ):
        raise PersistentWorldMovementRelationIdentityCollisionError(
            "deterministic bounded destination relation ID "
            "collides with an existing relation"
        )

    destination_relation = create_located_at_relation(
        relation_id=destination_relation_id,
        subject_entity_id=actor_entity_id,
        object_entity_id=destination_place_id,
    )

    return (
        create_persistent_world_entity_location_representation(
            campaign_id=representation.campaign_id,
            entities=representation.entities,
            relations=[
                *remaining_relations,
                destination_relation,
            ],
        )
    )


def _existing_transition(
    state: PersistentWorldMovementRuntimeState,
    command_id: str,
) -> PersistentWorldMovementCommittedTransition | None:
    for transition in state.committed_transitions:
        if transition.command_id == command_id:
            return transition

    return None


def prepare_persistent_world_movement(
    *,
    state: PersistentWorldMovementRuntimeState,
    command: CommandEnvelope,
    spatial_evidence: MovementSpatialEvidence,
    opportunity_evidence: MovementOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldMovementPreparedTransition:
    """Prepare one movement without mutating authoritative state."""

    if not isinstance(
        state,
        PersistentWorldMovementRuntimeState,
    ):
        raise InvalidPersistentWorldMovementRequestError(
            "state must be PersistentWorldMovementRuntimeState"
        )

    if not validate_command_envelope(command):
        raise InvalidPersistentWorldMovementRequestError(
            "command failed CommandEnvelope validation"
        )

    fingerprint = (
        fingerprint_persistent_world_movement_command(
            command
        )
    )
    token = fingerprint[:24]

    request_ref = build_record_id(
        "movement_request",
        token,
    )

    routing = route_command_envelope(
        request_ref=request_ref,
        command_envelope=command,
    )

    if routing.classification.family != "movement":
        raise UnsupportedPersistentWorldMovementCommandError(
            "command must route through the existing "
            "movement command family"
        )

    actor_entity_id = command.source_actor_id
    destination_place_id = _destination_from_command(
        command
    )

    entities = _entity_by_id(state.representation)

    if actor_entity_id not in entities:
        raise PersistentWorldMovementEntityNotFoundError(
            f"actor does not exist: {actor_entity_id!r}"
        )

    destination = entities.get(destination_place_id)

    if destination is None:
        raise PersistentWorldMovementEntityNotFoundError(
            "destination does not exist: "
            f"{destination_place_id!r}"
        )

    if destination.classification != "place":
        raise PersistentWorldMovementDestinationNotPlaceError(
            "movement destination must be classified exactly "
            "as 'place'"
        )

    source_relation = _current_location_relation(
        state.representation,
        actor_entity_id,
    )
    source_place_id = source_relation.object_entity_id

    if destination_place_id == source_place_id:
        raise InvalidPersistentWorldMovementRequestError(
            "bounded R4-C movement requires a distinct "
            "destination place"
        )

    _validate_owner_evidence(
        spatial_evidence=spatial_evidence,
        opportunity_evidence=opportunity_evidence,
        actor_entity_id=actor_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
    )

    actual_pre_state_digest = (
        digest_persistent_world_entity_location_representation(
            state.representation
        )
    )

    if (
        expected_pre_state_digest
        != actual_pre_state_digest
    ):
        raise PersistentWorldMovementStaleStateError(
            "expected pre-state digest does not match "
            "current authoritative representation"
        )

    destination_relation_id = build_record_id(
        "relation",
        f"movement-{token}",
    )

    if (
        destination_relation_id
        != source_relation.relation_id
        and any(
            relation.relation_id
            == destination_relation_id
            for relation in state.representation.relations
        )
    ):
        raise (
            PersistentWorldMovementRelationIdentityCollisionError(
                "deterministic destination relation ID "
                "already exists"
            )
        )

    preview_id = build_record_id(
        "movement_preview",
        token,
    )

    preview = create_transaction_preview(
        preview_id=preview_id,
        command=command,
        status="preview_created",
        messages=(
            "bounded persistent-world movement prepared",
        ),
        requires_confirmation=False,
        metadata={
            "package": "R4-C",
            "movement_family": "movement",
            "mutation_performed": False,
        },
    )

    state_delta_id = build_record_id(
        "movement_delta",
        token,
    )

    state_delta = create_state_delta_envelope(
        delta_id=state_delta_id,
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(
            actor_entity_id,
            source_place_id,
            destination_place_id,
            source_relation.relation_id,
            destination_relation_id,
        ),
        change_type="relationship_update",
        payload={
            "relation_type": "located_at",
            "subject_entity_id": actor_entity_id,
            "from_place_id": source_place_id,
            "to_place_id": destination_place_id,
            "source_relation_id": (
                source_relation.relation_id
            ),
            "destination_relation_id": (
                destination_relation_id
            ),
        },
        metadata={
            "package": "R4-C",
            "semantic_owner": "AFQR-18",
            "qualified_transition_owner": "AFQR-01",
        },
    )

    post_representation = _apply_location_change(
        representation=state.representation,
        actor_entity_id=actor_entity_id,
        source_relation_id=source_relation.relation_id,
        destination_relation_id=destination_relation_id,
        destination_place_id=destination_place_id,
    )

    post_state_digest = (
        digest_persistent_world_entity_location_representation(
            post_representation
        )
    )

    return PersistentWorldMovementPreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        actor_entity_id=actor_entity_id,
        source_place_id=source_place_id,
        destination_place_id=destination_place_id,
        source_relation_id=source_relation.relation_id,
        destination_relation_id=destination_relation_id,
        pre_state_digest=actual_pre_state_digest,
        post_state_digest=post_state_digest,
        routing_family=routing.classification.family,
        owner_route=routing.dispatch_shell.owner_route,
        spatial_evidence_id=spatial_evidence.evidence_id,
        opportunity_evidence_id=(
            opportunity_evidence.evidence_id
        ),
        preview=preview,
        state_delta=state_delta,
        post_representation=post_representation,
    )


def commit_prepared_persistent_world_movement(
    *,
    state: PersistentWorldMovementRuntimeState,
    prepared: PersistentWorldMovementPreparedTransition,
) -> PersistentWorldMovementExecutionResult:
    """Atomically commit a previously prepared bounded transition."""

    if not isinstance(
        state,
        PersistentWorldMovementRuntimeState,
    ):
        raise InvalidPersistentWorldMovementRequestError(
            "state must be PersistentWorldMovementRuntimeState"
        )

    if not isinstance(
        prepared,
        PersistentWorldMovementPreparedTransition,
    ):
        raise InvalidPersistentWorldMovementRequestError(
            "prepared must be "
            "PersistentWorldMovementPreparedTransition"
        )

    existing = _existing_transition(
        state,
        prepared.command_id,
    )

    if existing is not None:
        if (
            existing.command_fingerprint
            != prepared.command_fingerprint
        ):
            raise PersistentWorldMovementRetryConflictError(
                "command ID already committed with different "
                "immutable command meaning"
            )

        return PersistentWorldMovementExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )

    current_digest = (
        digest_persistent_world_entity_location_representation(
            state.representation
        )
    )

    if current_digest != prepared.pre_state_digest:
        raise PersistentWorldMovementStaleStateError(
            "authoritative state changed after movement "
            "preparation"
        )

    receipt = PersistentWorldMovementCommitReceipt(
        receipt_id=build_record_id(
            "movement_receipt",
            prepared.command_fingerprint[:24],
        ),
        command_id=prepared.command_id,
        command_fingerprint=(
            prepared.command_fingerprint
        ),
        actor_entity_id=prepared.actor_entity_id,
        source_place_id=prepared.source_place_id,
        destination_place_id=(
            prepared.destination_place_id
        ),
        source_relation_id=prepared.source_relation_id,
        destination_relation_id=(
            prepared.destination_relation_id
        ),
        pre_state_digest=prepared.pre_state_digest,
        post_state_digest=prepared.post_state_digest,
        preview_id=prepared.preview.preview_id,
        state_delta_id=prepared.state_delta.delta_id,
        spatial_evidence_id=(
            prepared.spatial_evidence_id
        ),
        opportunity_evidence_id=(
            prepared.opportunity_evidence_id
        ),
    )

    committed = (
        PersistentWorldMovementCommittedTransition(
            command_id=prepared.command_id,
            command_fingerprint=(
                prepared.command_fingerprint
            ),
            preview=prepared.preview,
            state_delta=prepared.state_delta,
            receipt=receipt,
        )
    )

    transitions = tuple(
        sorted(
            (
                *state.committed_transitions,
                committed,
            ),
            key=lambda item: (
                item.command_id,
                item.command_fingerprint,
            ),
        )
    )

    post_state = PersistentWorldMovementRuntimeState(
        representation=prepared.post_representation,
        committed_transitions=transitions,
    )

    return PersistentWorldMovementExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def execute_persistent_world_movement(
    *,
    state: PersistentWorldMovementRuntimeState,
    command: CommandEnvelope,
    spatial_evidence: MovementSpatialEvidence,
    opportunity_evidence: MovementOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldMovementExecutionResult:
    """Execute or idempotently return one bounded movement result."""

    if not isinstance(
        state,
        PersistentWorldMovementRuntimeState,
    ):
        raise InvalidPersistentWorldMovementRequestError(
            "state must be PersistentWorldMovementRuntimeState"
        )

    fingerprint = (
        fingerprint_persistent_world_movement_command(
            command
        )
    )

    existing = _existing_transition(
        state,
        command.command_id,
    )

    if existing is not None:
        if (
            existing.command_fingerprint
            != fingerprint
        ):
            raise PersistentWorldMovementRetryConflictError(
                "command ID already committed with materially "
                "different command content"
            )

        return PersistentWorldMovementExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )

    prepared = prepare_persistent_world_movement(
        state=state,
        command=command,
        spatial_evidence=spatial_evidence,
        opportunity_evidence=opportunity_evidence,
        expected_pre_state_digest=(
            expected_pre_state_digest
        ),
    )

    return commit_prepared_persistent_world_movement(
        state=state,
        prepared=prepared,
    )


def replay_persistent_world_movement(
    *,
    pre_state_representation: (
        PersistentWorldEntityLocationRepresentation
    ),
    receipt: PersistentWorldMovementCommitReceipt,
) -> PersistentWorldEntityLocationRepresentation:
    """Replay one committed movement from authoritative evidence only."""

    if not isinstance(
        pre_state_representation,
        PersistentWorldEntityLocationRepresentation,
    ):
        raise PersistentWorldMovementReplayError(
            "pre_state_representation has invalid type"
        )

    if not isinstance(
        receipt,
        PersistentWorldMovementCommitReceipt,
    ):
        raise PersistentWorldMovementReplayError(
            "receipt has invalid type"
        )

    pre_digest = (
        digest_persistent_world_entity_location_representation(
            pre_state_representation
        )
    )

    if pre_digest != receipt.pre_state_digest:
        raise PersistentWorldMovementReplayError(
            "replay pre-state digest does not match "
            "committed receipt"
        )

    entities = _entity_by_id(
        pre_state_representation
    )

    if receipt.actor_entity_id not in entities:
        raise PersistentWorldMovementReplayError(
            "receipt actor does not exist in replay pre-state"
        )

    destination = entities.get(
        receipt.destination_place_id
    )

    if (
        destination is None
        or destination.classification != "place"
    ):
        raise PersistentWorldMovementReplayError(
            "receipt destination is not a valid place "
            "in replay pre-state"
        )

    source_relation = _current_location_relation(
        pre_state_representation,
        receipt.actor_entity_id,
    )

    if (
        source_relation.relation_id
        != receipt.source_relation_id
        or source_relation.object_entity_id
        != receipt.source_place_id
    ):
        raise PersistentWorldMovementReplayError(
            "replay source location does not match "
            "committed receipt"
        )

    try:
        post = _apply_location_change(
            representation=pre_state_representation,
            actor_entity_id=receipt.actor_entity_id,
            source_relation_id=receipt.source_relation_id,
            destination_relation_id=(
                receipt.destination_relation_id
            ),
            destination_place_id=(
                receipt.destination_place_id
            ),
        )
    except PersistentWorldMovementIntegrationError as exc:
        raise PersistentWorldMovementReplayError(
            "committed movement could not be replayed"
        ) from exc

    post_digest = (
        digest_persistent_world_entity_location_representation(
            post
        )
    )

    if post_digest != receipt.post_state_digest:
        raise PersistentWorldMovementReplayError(
            "replay post-state digest differs from "
            "committed receipt"
        )

    return post


def serialize_persistent_world_movement_commit_receipt(
    receipt: PersistentWorldMovementCommitReceipt,
) -> dict[str, str]:
    if not isinstance(
        receipt,
        PersistentWorldMovementCommitReceipt,
    ):
        raise InvalidPersistentWorldMovementRequestError(
            "receipt must be "
            "PersistentWorldMovementCommitReceipt"
        )

    return receipt.to_dict()


def canonical_serialize_persistent_world_movement_commit_receipt(
    receipt: PersistentWorldMovementCommitReceipt,
) -> str:
    return json.dumps(
        serialize_persistent_world_movement_commit_receipt(
            receipt
        ),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
