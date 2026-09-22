"""R4-E bounded persistent-world object custody transfer.

This module implements deterministic pickup/drop over the existing R4-B
representation while composing the existing R4-C movement runtime state.

Authority remains routed to existing semantic owners:
AFQR-02 command identity/retry, AFQR-19 opportunity/resolution, AFQR-01
qualified commitment, AFQR-18 direct place/location semantics, and RT-010
immediate physical carrying/asset placement through ``carried_by``.

``carried_by`` does not establish ownership, entitlement, legal/social
custody, authority, agency, responsibility, knowledge, or visibility.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

from astra_runtime.domain.command_kind_routing_skeleton import route_command_envelope
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntity,
    PersistentWorldEntityLocationRepresentation,
    PersistentWorldRelation,
    create_carried_by_relation,
    create_located_at_relation,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    PersistentWorldMovementRuntimeState,
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.kernel.command_envelope import CommandEnvelope, validate_command_envelope
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.state_delta import StateDeltaEnvelope, create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import TransactionPreview, create_transaction_preview

__all__ = [
    "RT010_CUSTODY_OWNER",
    "AFQR19_CUSTODY_OPPORTUNITY_OWNER",
    "PersistentWorldObjectCustodyError",
    "InvalidPersistentWorldObjectCustodyRequestError",
    "UnsupportedPersistentWorldObjectCustodyCommandError",
    "PersistentWorldObjectCustodyEntityError",
    "PersistentWorldObjectCustodyPlacementError",
    "PersistentWorldObjectCustodyEvidenceError",
    "PersistentWorldObjectCustodyStaleStateError",
    "PersistentWorldObjectCustodyRetryConflictError",
    "PersistentWorldObjectCustodyRelationIdentityCollisionError",
    "PersistentWorldObjectCustodyReplayError",
    "CustodyQualificationEvidence",
    "CustodyOpportunityEvidence",
    "PersistentWorldObjectCustodyCommitReceipt",
    "PersistentWorldObjectCustodyCommittedTransition",
    "PersistentWorldObjectCustodyRuntimeState",
    "PersistentWorldObjectCustodyPreparedTransition",
    "PersistentWorldObjectCustodyExecutionResult",
    "create_custody_qualification_evidence",
    "create_custody_opportunity_evidence",
    "create_persistent_world_object_custody_runtime_state",
    "replace_persistent_world_object_custody_movement_state",
    "fingerprint_persistent_world_object_custody_command",
    "prepare_persistent_world_object_custody",
    "commit_prepared_persistent_world_object_custody",
    "execute_persistent_world_object_custody",
    "replay_persistent_world_object_custody",
    "serialize_persistent_world_object_custody_commit_receipt",
    "canonical_serialize_persistent_world_object_custody_commit_receipt",
]

RT010_CUSTODY_OWNER = "RT-010"
AFQR19_CUSTODY_OPPORTUNITY_OWNER = "AFQR-19"
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class PersistentWorldObjectCustodyError(ValueError):
    """Base R4-E custody-transfer error."""


class InvalidPersistentWorldObjectCustodyRequestError(PersistentWorldObjectCustodyError):
    """Raised for structurally invalid bounded custody requests."""


class UnsupportedPersistentWorldObjectCustodyCommandError(PersistentWorldObjectCustodyError):
    """Raised when a command is not bounded pickup/drop inventory intent."""


class PersistentWorldObjectCustodyEntityError(PersistentWorldObjectCustodyError):
    """Raised when actor/object identity or classification is invalid."""


class PersistentWorldObjectCustodyPlacementError(PersistentWorldObjectCustodyError):
    """Raised when immediate placement is absent, contradictory, or illegal."""


class PersistentWorldObjectCustodyEvidenceError(PersistentWorldObjectCustodyError):
    """Raised when RT-010 or AFQR-19 evidence is absent or inconsistent."""


class PersistentWorldObjectCustodyStaleStateError(PersistentWorldObjectCustodyError):
    """Raised when the frozen pre-state digest no longer matches."""


class PersistentWorldObjectCustodyRetryConflictError(PersistentWorldObjectCustodyError):
    """Raised when one command ID is reused with changed immutable meaning."""


class PersistentWorldObjectCustodyRelationIdentityCollisionError(PersistentWorldObjectCustodyError):
    """Raised on deterministic destination relation identity collision."""


class PersistentWorldObjectCustodyReplayError(PersistentWorldObjectCustodyError):
    """Raised when committed custody evidence cannot replay exactly."""


def _require_record_id(value: object, label: str, error_cls=InvalidPersistentWorldObjectCustodyRequestError) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise error_cls(f"{label} must be a valid existing RecordId, got {value!r}")
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise InvalidPersistentWorldObjectCustodyRequestError(
            f"{label} must be a lowercase SHA-256 digest"
        )
    return value


@dataclass(frozen=True, kw_only=True)
class CustodyQualificationEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    qualified: bool
    semantic_owner: str = RT010_CUSTODY_OWNER

    def __post_init__(self) -> None:
        _require_record_id(self.evidence_id, "evidence_id", PersistentWorldObjectCustodyEvidenceError)
        _require_record_id(self.actor_entity_id, "actor_entity_id", PersistentWorldObjectCustodyEvidenceError)
        _require_record_id(self.object_entity_id, "object_entity_id", PersistentWorldObjectCustodyEvidenceError)
        if self.operation not in {"pickup", "drop"}:
            raise PersistentWorldObjectCustodyEvidenceError("operation must be pickup or drop")
        if type(self.qualified) is not bool:
            raise PersistentWorldObjectCustodyEvidenceError("qualified must be bool")
        if self.semantic_owner != RT010_CUSTODY_OWNER:
            raise PersistentWorldObjectCustodyEvidenceError("semantic_owner must be RT-010")


@dataclass(frozen=True, kw_only=True)
class CustodyOpportunityEvidence:
    evidence_id: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    opportunity_available: bool
    resolution_accepted: bool
    semantic_owner: str = AFQR19_CUSTODY_OPPORTUNITY_OWNER

    def __post_init__(self) -> None:
        _require_record_id(self.evidence_id, "evidence_id", PersistentWorldObjectCustodyEvidenceError)
        _require_record_id(self.actor_entity_id, "actor_entity_id", PersistentWorldObjectCustodyEvidenceError)
        _require_record_id(self.object_entity_id, "object_entity_id", PersistentWorldObjectCustodyEvidenceError)
        if self.operation not in {"pickup", "drop"}:
            raise PersistentWorldObjectCustodyEvidenceError("operation must be pickup or drop")
        if type(self.opportunity_available) is not bool or type(self.resolution_accepted) is not bool:
            raise PersistentWorldObjectCustodyEvidenceError("opportunity/resolution flags must be bool")
        if self.semantic_owner != AFQR19_CUSTODY_OPPORTUNITY_OWNER:
            raise PersistentWorldObjectCustodyEvidenceError("semantic_owner must be AFQR-19")


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectCustodyCommitReceipt:
    receipt_id: str
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
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
    opportunity_evidence_id: str
    status: str = "committed"

    def __post_init__(self) -> None:
        for name in (
            "receipt_id", "actor_entity_id", "object_entity_id", "place_id",
            "source_relation_id", "destination_relation_id", "preview_id",
            "state_delta_id", "rt010_qualification_id", "opportunity_evidence_id",
        ):
            _require_record_id(getattr(self, name), name)
        if not isinstance(self.command_id, str) or not self.command_id.strip():
            raise InvalidPersistentWorldObjectCustodyRequestError("command_id must be non-empty")
        _require_sha256(self.command_fingerprint, "command_fingerprint")
        _require_sha256(self.pre_state_digest, "pre_state_digest")
        _require_sha256(self.post_state_digest, "post_state_digest")
        if self.operation not in {"pickup", "drop"}:
            raise InvalidPersistentWorldObjectCustodyRequestError("operation must be pickup or drop")
        expected = (
            (LOCATED_AT_RELATION_TYPE, CARRIED_BY_RELATION_TYPE)
            if self.operation == "pickup"
            else (CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE)
        )
        if (self.source_relation_type, self.destination_relation_type) != expected:
            raise InvalidPersistentWorldObjectCustodyRequestError(
                "receipt relation types disagree with operation"
            )
        if self.status != "committed":
            raise InvalidPersistentWorldObjectCustodyRequestError("receipt status must be committed")

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_fingerprint": self.command_fingerprint,
            "actor_entity_id": self.actor_entity_id,
            "object_entity_id": self.object_entity_id,
            "operation": self.operation,
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
            "opportunity_evidence_id": self.opportunity_evidence_id,
            "status": self.status,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectCustodyCommittedTransition:
    command_id: str
    command_fingerprint: str
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    receipt: PersistentWorldObjectCustodyCommitReceipt


def _entity_by_id(representation: PersistentWorldEntityLocationRepresentation) -> dict[str, PersistentWorldEntity]:
    return {entity.entity_id: entity for entity in representation.entities}


def _current_location_relation(
    representation: PersistentWorldEntityLocationRepresentation,
    actor_entity_id: str,
) -> PersistentWorldRelation:
    matches = [
        relation
        for relation in representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == actor_entity_id
    ]
    if len(matches) != 1:
        raise PersistentWorldObjectCustodyPlacementError(
            f"actor requires exactly one located_at relation; observed {len(matches)}"
        )
    return matches[0]


def _object_placement_relations(
    representation: PersistentWorldEntityLocationRepresentation,
    object_entity_id: str,
) -> tuple[list[PersistentWorldRelation], list[PersistentWorldRelation]]:
    direct = [
        r for r in representation.relations
        if r.relation_type == LOCATED_AT_RELATION_TYPE and r.subject_entity_id == object_entity_id
    ]
    carried = [
        r for r in representation.relations
        if r.relation_type == CARRIED_BY_RELATION_TYPE and r.subject_entity_id == object_entity_id
    ]
    return direct, carried


def _validate_participating_placement(
    representation: PersistentWorldEntityLocationRepresentation,
    object_entity_ids: set[str],
) -> None:
    for object_entity_id in object_entity_ids:
        direct, carried = _object_placement_relations(representation, object_entity_id)
        if len(direct) > 1 or len(carried) > 1:
            raise PersistentWorldObjectCustodyPlacementError("duplicate immediate placement relation")
        if direct and carried:
            raise PersistentWorldObjectCustodyPlacementError(
                "participating object may not be both located_at and carried_by"
            )


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectCustodyRuntimeState:
    movement_state: PersistentWorldMovementRuntimeState
    committed_custody_transitions: tuple[PersistentWorldObjectCustodyCommittedTransition, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.movement_state, PersistentWorldMovementRuntimeState):
            raise InvalidPersistentWorldObjectCustodyRequestError(
                "movement_state must be PersistentWorldMovementRuntimeState"
            )
        transitions = tuple(self.committed_custody_transitions)
        for index, transition in enumerate(transitions):
            if not isinstance(transition, PersistentWorldObjectCustodyCommittedTransition):
                raise InvalidPersistentWorldObjectCustodyRequestError(
                    f"committed_custody_transitions[{index}] has invalid type"
                )
        custody_ids = [x.command_id for x in transitions]
        if len(custody_ids) != len(set(custody_ids)):
            raise InvalidPersistentWorldObjectCustodyRequestError("custody command IDs must be unique")
        movement_ids = [x.command_id for x in self.movement_state.committed_transitions]
        if set(custody_ids) & set(movement_ids):
            raise InvalidPersistentWorldObjectCustodyRequestError(
                "movement and custody command IDs must not collide"
            )
        participating = {x.receipt.object_entity_id for x in transitions}
        participating.update(
            r.subject_entity_id
            for r in self.movement_state.representation.relations
            if r.relation_type == CARRIED_BY_RELATION_TYPE
        )
        _validate_participating_placement(self.movement_state.representation, participating)
        object.__setattr__(self, "committed_custody_transitions", transitions)


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectCustodyPreparedTransition:
    command_id: str
    command_fingerprint: str
    actor_entity_id: str
    object_entity_id: str
    operation: str
    place_id: str
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
    post_representation: PersistentWorldEntityLocationRepresentation


@dataclass(frozen=True, kw_only=True)
class PersistentWorldObjectCustodyExecutionResult:
    state: PersistentWorldObjectCustodyRuntimeState
    receipt: PersistentWorldObjectCustodyCommitReceipt
    preview: TransactionPreview
    state_delta: StateDeltaEnvelope
    technical_retry: bool


def create_custody_qualification_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    operation: str, qualified: bool,
) -> CustodyQualificationEvidence:
    return CustodyQualificationEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        qualified=qualified,
    )


def create_custody_opportunity_evidence(
    *, evidence_id: str, actor_entity_id: str, object_entity_id: str,
    operation: str, opportunity_available: bool, resolution_accepted: bool,
) -> CustodyOpportunityEvidence:
    return CustodyOpportunityEvidence(
        evidence_id=evidence_id,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        opportunity_available=opportunity_available,
        resolution_accepted=resolution_accepted,
    )


def create_persistent_world_object_custody_runtime_state(
    *, movement_state: PersistentWorldMovementRuntimeState,
) -> PersistentWorldObjectCustodyRuntimeState:
    return PersistentWorldObjectCustodyRuntimeState(movement_state=movement_state)


def replace_persistent_world_object_custody_movement_state(
    *, state: PersistentWorldObjectCustodyRuntimeState,
    movement_state: PersistentWorldMovementRuntimeState,
) -> PersistentWorldObjectCustodyRuntimeState:
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise InvalidPersistentWorldObjectCustodyRequestError("invalid custody state")
    return PersistentWorldObjectCustodyRuntimeState(
        movement_state=movement_state,
        committed_custody_transitions=state.committed_custody_transitions,
    )


def fingerprint_persistent_world_object_custody_command(command: CommandEnvelope) -> str:
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectCustodyRequestError(
            "command failed CommandEnvelope validation"
        )
    try:
        canonical = json.dumps(
            command.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise InvalidPersistentWorldObjectCustodyRequestError(
            "command must be canonical JSON-compatible"
        ) from exc
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _operation_from_command(command: CommandEnvelope) -> str:
    normalized = command.command_type.strip().lower().replace("-", "_")
    first = normalized.split("_", 1)[0]
    if first in {"pickup", "drop"}:
        return first
    raise UnsupportedPersistentWorldObjectCustodyCommandError(
        "R4-E supports only pickup/drop inventory command kinds"
    )


def _object_from_command(command: CommandEnvelope) -> str:
    return _require_record_id(
        command.payload.get("object_entity_id"),
        "command.payload.object_entity_id",
    )


def _validate_owner_evidence(
    *, qualification_evidence: CustodyQualificationEvidence,
    opportunity_evidence: CustodyOpportunityEvidence,
    actor_entity_id: str, object_entity_id: str, operation: str,
) -> None:
    if not isinstance(qualification_evidence, CustodyQualificationEvidence):
        raise PersistentWorldObjectCustodyEvidenceError(
            "qualification_evidence must be CustodyQualificationEvidence"
        )
    if not isinstance(opportunity_evidence, CustodyOpportunityEvidence):
        raise PersistentWorldObjectCustodyEvidenceError(
            "opportunity_evidence must be CustodyOpportunityEvidence"
        )
    for evidence in (qualification_evidence, opportunity_evidence):
        if (
            evidence.actor_entity_id != actor_entity_id
            or evidence.object_entity_id != object_entity_id
            or evidence.operation != operation
        ):
            raise PersistentWorldObjectCustodyEvidenceError(
                "owner evidence does not match actor/object/operation"
            )
    if not qualification_evidence.qualified:
        raise PersistentWorldObjectCustodyEvidenceError("RT-010 rejected custody transition")
    if (
        not opportunity_evidence.opportunity_available
        or not opportunity_evidence.resolution_accepted
    ):
        raise PersistentWorldObjectCustodyEvidenceError("AFQR-19 rejected custody transition")


def _existing_transition(
    state: PersistentWorldObjectCustodyRuntimeState,
    command_id: str,
) -> PersistentWorldObjectCustodyCommittedTransition | None:
    for transition in state.committed_custody_transitions:
        if transition.command_id == command_id:
            return transition
    return None


def _apply_custody_change(
    *, representation: PersistentWorldEntityLocationRepresentation,
    object_entity_id: str, actor_entity_id: str, place_id: str,
    source_relation_id: str, destination_relation_id: str, operation: str,
) -> PersistentWorldEntityLocationRepresentation:
    remaining = [r for r in representation.relations if r.relation_id != source_relation_id]
    if len(remaining) != len(representation.relations) - 1:
        raise PersistentWorldObjectCustodyPlacementError(
            "custody source relation is missing or duplicated"
        )
    if any(r.relation_id == destination_relation_id for r in remaining):
        raise PersistentWorldObjectCustodyRelationIdentityCollisionError(
            "deterministic destination relation ID collides"
        )
    if operation == "pickup":
        destination = create_carried_by_relation(
            relation_id=destination_relation_id,
            subject_entity_id=object_entity_id,
            object_entity_id=actor_entity_id,
        )
    elif operation == "drop":
        destination = create_located_at_relation(
            relation_id=destination_relation_id,
            subject_entity_id=object_entity_id,
            object_entity_id=place_id,
        )
    else:
        raise InvalidPersistentWorldObjectCustodyRequestError("operation must be pickup or drop")
    return create_persistent_world_entity_location_representation(
        campaign_id=representation.campaign_id,
        entities=representation.entities,
        relations=(*remaining, destination),
    )


def prepare_persistent_world_object_custody(
    *, state: PersistentWorldObjectCustodyRuntimeState, command: CommandEnvelope,
    qualification_evidence: CustodyQualificationEvidence,
    opportunity_evidence: CustodyOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectCustodyPreparedTransition:
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise InvalidPersistentWorldObjectCustodyRequestError("invalid custody state")
    if not validate_command_envelope(command):
        raise InvalidPersistentWorldObjectCustodyRequestError("invalid command envelope")

    fingerprint = fingerprint_persistent_world_object_custody_command(command)
    token = fingerprint[:24]
    routing = route_command_envelope(
        request_ref=build_record_id("custody_request", token),
        command_envelope=command,
    )
    if routing.classification.family != "inventory":
        raise UnsupportedPersistentWorldObjectCustodyCommandError(
            "custody command must route through inventory family"
        )

    operation = _operation_from_command(command)
    actor_entity_id = command.source_actor_id
    object_entity_id = _object_from_command(command)
    representation = state.movement_state.representation
    entities = _entity_by_id(representation)
    actor = entities.get(actor_entity_id)
    target = entities.get(object_entity_id)
    if actor is None or actor.classification != "character_or_creature":
        raise PersistentWorldObjectCustodyEntityError(
            "actor must exist and be character_or_creature"
        )
    if target is None or target.classification != "object":
        raise PersistentWorldObjectCustodyEntityError("target must exist and be object")

    actor_location = _current_location_relation(representation, actor_entity_id)
    place_id = actor_location.object_entity_id
    direct, carried = _object_placement_relations(representation, object_entity_id)
    if len(direct) > 1 or len(carried) > 1 or (direct and carried):
        raise PersistentWorldObjectCustodyPlacementError("object placement is contradictory")

    if operation == "pickup":
        if len(direct) != 1 or carried:
            raise PersistentWorldObjectCustodyPlacementError(
                "pickup requires one direct object location and no carrier"
            )
        if direct[0].object_entity_id != place_id:
            raise PersistentWorldObjectCustodyPlacementError("pickup requires co-location")
        source_relation = direct[0]
        destination_type = CARRIED_BY_RELATION_TYPE
    else:
        if len(carried) != 1 or direct:
            raise PersistentWorldObjectCustodyPlacementError(
                "drop requires one carried_by relation and no direct location"
            )
        if carried[0].object_entity_id != actor_entity_id:
            raise PersistentWorldObjectCustodyPlacementError(
                "drop object is not carried by source actor"
            )
        source_relation = carried[0]
        destination_type = LOCATED_AT_RELATION_TYPE

    _validate_owner_evidence(
        qualification_evidence=qualification_evidence,
        opportunity_evidence=opportunity_evidence,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
    )

    actual_digest = digest_persistent_world_entity_location_representation(representation)
    if expected_pre_state_digest != actual_digest:
        raise PersistentWorldObjectCustodyStaleStateError("stale pre-state digest")

    destination_relation_id = build_record_id("relation", f"custody-{token}")
    if (
        destination_relation_id != source_relation.relation_id
        and any(r.relation_id == destination_relation_id for r in representation.relations)
    ):
        raise PersistentWorldObjectCustodyRelationIdentityCollisionError(
            "destination relation identity already exists"
        )

    preview = create_transaction_preview(
        preview_id=build_record_id("custody_preview", token),
        command=command,
        status="preview_created",
        messages=("bounded persistent-world object custody prepared",),
        requires_confirmation=False,
        metadata={
            "package": "R4-E",
            "command_family": "inventory",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("custody_delta", token),
        source_command_id=command.command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(
            actor_entity_id,
            object_entity_id,
            place_id,
            source_relation.relation_id,
            destination_relation_id,
        ),
        change_type="relationship_update",
        payload={
            "operation": operation,
            "actor_entity_id": actor_entity_id,
            "object_entity_id": object_entity_id,
            "place_id": place_id,
            "source_relation_id": source_relation.relation_id,
            "source_relation_type": source_relation.relation_type,
            "destination_relation_id": destination_relation_id,
            "destination_relation_type": destination_type,
        },
        metadata={
            "package": "R4-E",
            "custody_semantic_owner": "RT-010",
            "direct_location_semantic_owner": "AFQR-18",
            "opportunity_semantic_owner": "AFQR-19",
            "qualified_transition_owner": "AFQR-01",
        },
    )
    post = _apply_custody_change(
        representation=representation,
        object_entity_id=object_entity_id,
        actor_entity_id=actor_entity_id,
        place_id=place_id,
        source_relation_id=source_relation.relation_id,
        destination_relation_id=destination_relation_id,
        operation=operation,
    )
    return PersistentWorldObjectCustodyPreparedTransition(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        actor_entity_id=actor_entity_id,
        object_entity_id=object_entity_id,
        operation=operation,
        place_id=place_id,
        source_relation_id=source_relation.relation_id,
        source_relation_type=source_relation.relation_type,
        destination_relation_id=destination_relation_id,
        destination_relation_type=destination_type,
        pre_state_digest=actual_digest,
        post_state_digest=digest_persistent_world_entity_location_representation(post),
        rt010_qualification_id=qualification_evidence.evidence_id,
        opportunity_evidence_id=opportunity_evidence.evidence_id,
        preview=preview,
        state_delta=delta,
        post_representation=post,
    )


def commit_prepared_persistent_world_object_custody(
    *, state: PersistentWorldObjectCustodyRuntimeState,
    prepared: PersistentWorldObjectCustodyPreparedTransition,
) -> PersistentWorldObjectCustodyExecutionResult:
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise InvalidPersistentWorldObjectCustodyRequestError("invalid custody state")
    if not isinstance(prepared, PersistentWorldObjectCustodyPreparedTransition):
        raise InvalidPersistentWorldObjectCustodyRequestError("invalid prepared transition")

    existing = _existing_transition(state, prepared.command_id)
    if existing is not None:
        if existing.command_fingerprint != prepared.command_fingerprint:
            raise PersistentWorldObjectCustodyRetryConflictError(
                "command ID already committed with different meaning"
            )
        return PersistentWorldObjectCustodyExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )

    current = digest_persistent_world_entity_location_representation(
        state.movement_state.representation
    )
    if current != prepared.pre_state_digest:
        raise PersistentWorldObjectCustodyStaleStateError(
            "authoritative state changed after preparation"
        )

    receipt = PersistentWorldObjectCustodyCommitReceipt(
        receipt_id=build_record_id("custody_receipt", prepared.command_fingerprint[:24]),
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        actor_entity_id=prepared.actor_entity_id,
        object_entity_id=prepared.object_entity_id,
        operation=prepared.operation,
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
        opportunity_evidence_id=prepared.opportunity_evidence_id,
    )
    committed = PersistentWorldObjectCustodyCommittedTransition(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        receipt=receipt,
    )
    custody_transitions = tuple(
        sorted(
            (*state.committed_custody_transitions, committed),
            key=lambda item: (item.command_id, item.command_fingerprint),
        )
    )
    movement_state = PersistentWorldMovementRuntimeState(
        representation=prepared.post_representation,
        committed_transitions=state.movement_state.committed_transitions,
    )
    post_state = PersistentWorldObjectCustodyRuntimeState(
        movement_state=movement_state,
        committed_custody_transitions=custody_transitions,
    )
    return PersistentWorldObjectCustodyExecutionResult(
        state=post_state,
        receipt=receipt,
        preview=prepared.preview,
        state_delta=prepared.state_delta,
        technical_retry=False,
    )


def execute_persistent_world_object_custody(
    *, state: PersistentWorldObjectCustodyRuntimeState, command: CommandEnvelope,
    qualification_evidence: CustodyQualificationEvidence,
    opportunity_evidence: CustodyOpportunityEvidence,
    expected_pre_state_digest: str,
) -> PersistentWorldObjectCustodyExecutionResult:
    if not isinstance(state, PersistentWorldObjectCustodyRuntimeState):
        raise InvalidPersistentWorldObjectCustodyRequestError("invalid custody state")
    fingerprint = fingerprint_persistent_world_object_custody_command(command)
    existing = _existing_transition(state, command.command_id)
    if existing is not None:
        if existing.command_fingerprint != fingerprint:
            raise PersistentWorldObjectCustodyRetryConflictError(
                "command ID already committed with materially different command content"
            )
        return PersistentWorldObjectCustodyExecutionResult(
            state=state,
            receipt=existing.receipt,
            preview=existing.preview,
            state_delta=existing.state_delta,
            technical_retry=True,
        )
    prepared = prepare_persistent_world_object_custody(
        state=state,
        command=command,
        qualification_evidence=qualification_evidence,
        opportunity_evidence=opportunity_evidence,
        expected_pre_state_digest=expected_pre_state_digest,
    )
    return commit_prepared_persistent_world_object_custody(
        state=state,
        prepared=prepared,
    )


def replay_persistent_world_object_custody(
    *, pre_state_representation: PersistentWorldEntityLocationRepresentation,
    receipt: PersistentWorldObjectCustodyCommitReceipt,
) -> PersistentWorldEntityLocationRepresentation:
    if not isinstance(pre_state_representation, PersistentWorldEntityLocationRepresentation):
        raise PersistentWorldObjectCustodyReplayError("invalid replay pre-state")
    if not isinstance(receipt, PersistentWorldObjectCustodyCommitReceipt):
        raise PersistentWorldObjectCustodyReplayError("invalid receipt")
    if (
        digest_persistent_world_entity_location_representation(pre_state_representation)
        != receipt.pre_state_digest
    ):
        raise PersistentWorldObjectCustodyReplayError("replay pre-state digest mismatch")

    entities = _entity_by_id(pre_state_representation)
    actor = entities.get(receipt.actor_entity_id)
    target = entities.get(receipt.object_entity_id)
    place = entities.get(receipt.place_id)
    if actor is None or actor.classification != "character_or_creature":
        raise PersistentWorldObjectCustodyReplayError("invalid receipt actor")
    if target is None or target.classification != "object":
        raise PersistentWorldObjectCustodyReplayError("invalid receipt object")
    if place is None or place.classification != "place":
        raise PersistentWorldObjectCustodyReplayError("invalid receipt place")
    if _current_location_relation(
        pre_state_representation, receipt.actor_entity_id
    ).object_entity_id != receipt.place_id:
        raise PersistentWorldObjectCustodyReplayError("actor location disagrees with receipt")

    sources = [
        r for r in pre_state_representation.relations
        if r.relation_id == receipt.source_relation_id
    ]
    if len(sources) != 1:
        raise PersistentWorldObjectCustodyReplayError("source relation absent or duplicated")
    source = sources[0]
    if (
        source.relation_type != receipt.source_relation_type
        or source.subject_entity_id != receipt.object_entity_id
    ):
        raise PersistentWorldObjectCustodyReplayError("source relation disagrees with receipt")
    if receipt.operation == "pickup":
        if source.object_entity_id != receipt.place_id:
            raise PersistentWorldObjectCustodyReplayError("pickup source place mismatch")
    else:
        if source.object_entity_id != receipt.actor_entity_id:
            raise PersistentWorldObjectCustodyReplayError("drop source carrier mismatch")
    try:
        post = _apply_custody_change(
            representation=pre_state_representation,
            object_entity_id=receipt.object_entity_id,
            actor_entity_id=receipt.actor_entity_id,
            place_id=receipt.place_id,
            source_relation_id=receipt.source_relation_id,
            destination_relation_id=receipt.destination_relation_id,
            operation=receipt.operation,
        )
    except PersistentWorldObjectCustodyError as exc:
        raise PersistentWorldObjectCustodyReplayError("committed transition could not replay") from exc
    if digest_persistent_world_entity_location_representation(post) != receipt.post_state_digest:
        raise PersistentWorldObjectCustodyReplayError("replay post-state digest mismatch")
    return post


def serialize_persistent_world_object_custody_commit_receipt(
    receipt: PersistentWorldObjectCustodyCommitReceipt,
) -> dict[str, str]:
    if not isinstance(receipt, PersistentWorldObjectCustodyCommitReceipt):
        raise InvalidPersistentWorldObjectCustodyRequestError("invalid custody receipt")
    return receipt.to_dict()


def canonical_serialize_persistent_world_object_custody_commit_receipt(
    receipt: PersistentWorldObjectCustodyCommitReceipt,
) -> str:
    return json.dumps(
        serialize_persistent_world_object_custody_commit_receipt(receipt),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
