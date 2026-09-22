"""R4-B persistent-world entity/location representation.

This module implements the bounded R4-B representation package only.

It provides deterministic campaign-scoped entity identity, open-ended entity
classification, the AFQR-18-routed ``located_at`` relation, referential
integrity validation, canonical serialization, and a reference-only
``scene_location_owner`` transport reference.

It does not own spatial semantics, record-identity semantics, persistence,
state mutation, event commitment, control, agency, ownership, knowledge,
visibility, canon, RNG, model calls, networking, or runtime promotion.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from dataclasses import dataclass

from astra_runtime.domain.state_owner_interface_contract_skeleton import (
    StateOwnerInterfaceReference,
    create_state_owner_interface_reference,
)
from astra_runtime.kernel.record_identity import (
    InvalidRecordIdError,
    parse_record_id,
)

__all__ = [
    "MINIMUM_PLAYABLE_ENTITY_CLASSIFICATIONS",
    "LOCATED_AT_RELATION_TYPE",
    "LOCATED_AT_SEMANTIC_OWNER",
    "CARRIED_BY_RELATION_TYPE",
    "CARRIED_BY_SEMANTIC_OWNER",
    "SCENE_LOCATION_OWNER_FAMILY",
    "PersistentWorldEntityLocationRepresentationError",
    "InvalidPersistentWorldEntityError",
    "InvalidPersistentWorldRelationError",
    "DuplicatePersistentWorldEntityIdError",
    "DuplicatePersistentWorldRelationIdError",
    "UnresolvedPersistentWorldRelationReferenceError",
    "InvalidLocatedAtRelationError",
    "InvalidCarriedByRelationError",
    "UnsupportedPersistentWorldRelationTypeError",
    "InvalidPersistentWorldRepresentationError",
    "PersistentWorldEntity",
    "PersistentWorldRelation",
    "PersistentWorldEntityLocationRepresentation",
    "create_persistent_world_entity",
    "create_located_at_relation",
    "create_carried_by_relation",
    "create_persistent_world_entity_location_representation",
    "serialize_persistent_world_entity_location_representation",
    "canonical_serialize_persistent_world_entity_location_representation",
    "create_scene_location_owner_transport_reference",
]

MINIMUM_PLAYABLE_ENTITY_CLASSIFICATIONS = frozenset(
    {
        "character_or_creature",
        "place",
        "object",
    }
)

LOCATED_AT_RELATION_TYPE = "located_at"
LOCATED_AT_SEMANTIC_OWNER = "AFQR-18"
CARRIED_BY_RELATION_TYPE = "carried_by"
CARRIED_BY_SEMANTIC_OWNER = "RT-010"
SCENE_LOCATION_OWNER_FAMILY = "scene_location_owner"

_CLASSIFICATION_PATTERN = re.compile(
    r"^[a-z][a-z0-9_-]*$"
)


class PersistentWorldEntityLocationRepresentationError(ValueError):
    """Base R4-B representation error."""


class InvalidPersistentWorldEntityError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when an entity representation is invalid."""


class InvalidPersistentWorldRelationError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when a relation representation is invalid."""


class DuplicatePersistentWorldEntityIdError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when one representation contains duplicate entity IDs."""


class DuplicatePersistentWorldRelationIdError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when one representation contains duplicate relation IDs."""


class UnresolvedPersistentWorldRelationReferenceError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when a relation refers outside its campaign representation."""


class InvalidLocatedAtRelationError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when a located_at relation violates R4-B semantics."""


class InvalidCarriedByRelationError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when a carried_by relation violates RT-010 semantics."""


class UnsupportedPersistentWorldRelationTypeError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised for relation types that lack separately qualified ownership."""


class InvalidPersistentWorldRepresentationError(
    PersistentWorldEntityLocationRepresentationError,
):
    """Raised when the campaign-scoped representation itself is invalid."""


def _validate_record_id(
    value: object,
    label: str,
    error_cls: type[Exception],
) -> str:
    if not isinstance(value, str):
        raise error_cls(
            f"{label} must be an existing RecordId string, "
            f"got {type(value).__name__}"
        )

    try:
        parsed = parse_record_id(value)
    except (InvalidRecordIdError, TypeError) as exc:
        raise error_cls(
            f"{label} must be a valid existing RecordId: {value!r}"
        ) from exc

    if parsed.full_id != value:
        raise error_cls(
            f"{label} must be canonical RecordId text: {value!r}"
        )

    return value


def _validate_classification(value: object) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or not _CLASSIFICATION_PATTERN.fullmatch(value)
    ):
        raise InvalidPersistentWorldEntityError(
            "classification must be a non-empty lower-case classification "
            "identifier using letters, digits, underscores, or hyphens"
        )

    return value


@dataclass(frozen=True, kw_only=True)
class PersistentWorldEntity:
    """Identity-stable entity representation.

    Classification is intentionally open-ended. It carries no control, agency,
    ownership, knowledge, visibility, or authority semantics.
    """

    entity_id: str
    classification: str

    def __post_init__(self) -> None:
        _validate_record_id(
            self.entity_id,
            "entity_id",
            InvalidPersistentWorldEntityError,
        )
        _validate_classification(self.classification)

    def to_dict(self) -> dict[str, str]:
        return {
            "entity_id": self.entity_id,
            "classification": self.classification,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldRelation:
    """Typed relation envelope for the initial R4-B located_at relation."""

    relation_id: str
    relation_type: str
    subject_entity_id: str
    object_entity_id: str
    semantic_owner: str

    def __post_init__(self) -> None:
        _validate_record_id(
            self.relation_id,
            "relation_id",
            InvalidPersistentWorldRelationError,
        )
        _validate_record_id(
            self.subject_entity_id,
            "subject_entity_id",
            InvalidPersistentWorldRelationError,
        )
        _validate_record_id(
            self.object_entity_id,
            "object_entity_id",
            InvalidPersistentWorldRelationError,
        )

        if self.relation_type == LOCATED_AT_RELATION_TYPE:
            if self.semantic_owner != LOCATED_AT_SEMANTIC_OWNER:
                raise InvalidLocatedAtRelationError(
                    "located_at semantic_owner must be exactly 'AFQR-18'"
                )
        elif self.relation_type == CARRIED_BY_RELATION_TYPE:
            if self.semantic_owner != CARRIED_BY_SEMANTIC_OWNER:
                raise InvalidCarriedByRelationError(
                    "carried_by semantic_owner must be exactly 'RT-010'"
                )
        else:
            raise UnsupportedPersistentWorldRelationTypeError(
                "relation type lacks separately qualified semantic ownership"
            )

    def to_dict(self) -> dict[str, str]:
        return {
            "relation_id": self.relation_id,
            "relation_type": self.relation_type,
            "subject_entity_id": self.subject_entity_id,
            "object_entity_id": self.object_entity_id,
            "semantic_owner": self.semantic_owner,
        }


@dataclass(frozen=True, kw_only=True)
class PersistentWorldEntityLocationRepresentation:
    """One deterministic campaign-scoped R4-B representation."""

    campaign_id: str
    entities: tuple[PersistentWorldEntity, ...] = ()
    relations: tuple[PersistentWorldRelation, ...] = ()

    def __post_init__(self) -> None:
        _validate_record_id(
            self.campaign_id,
            "campaign_id",
            InvalidPersistentWorldRepresentationError,
        )

        if isinstance(self.entities, (str, bytes)) or not isinstance(
            self.entities,
            Sequence,
        ):
            raise InvalidPersistentWorldRepresentationError(
                "entities must be a sequence of PersistentWorldEntity values"
            )

        if isinstance(self.relations, (str, bytes)) or not isinstance(
            self.relations,
            Sequence,
        ):
            raise InvalidPersistentWorldRepresentationError(
                "relations must be a sequence of PersistentWorldRelation values"
            )

        entities = tuple(self.entities)
        relations = tuple(self.relations)

        for index, entity in enumerate(entities):
            if not isinstance(entity, PersistentWorldEntity):
                raise InvalidPersistentWorldRepresentationError(
                    f"entities[{index}] must be PersistentWorldEntity, "
                    f"got {type(entity).__name__}"
                )

        for index, relation in enumerate(relations):
            if not isinstance(relation, PersistentWorldRelation):
                raise InvalidPersistentWorldRepresentationError(
                    f"relations[{index}] must be PersistentWorldRelation, "
                    f"got {type(relation).__name__}"
                )

        entity_by_id: dict[str, PersistentWorldEntity] = {}

        for entity in entities:
            if entity.entity_id in entity_by_id:
                raise DuplicatePersistentWorldEntityIdError(
                    f"duplicate entity_id: {entity.entity_id!r}"
                )
            entity_by_id[entity.entity_id] = entity

        relation_ids: set[str] = set()

        for relation in relations:
            if relation.relation_id in relation_ids:
                raise DuplicatePersistentWorldRelationIdError(
                    f"duplicate relation_id: {relation.relation_id!r}"
                )
            relation_ids.add(relation.relation_id)

            if relation.subject_entity_id not in entity_by_id:
                raise UnresolvedPersistentWorldRelationReferenceError(
                    "relation subject_entity_id does not resolve within "
                    f"campaign representation: {relation.subject_entity_id!r}"
                )

            if relation.object_entity_id not in entity_by_id:
                raise UnresolvedPersistentWorldRelationReferenceError(
                    "relation object_entity_id does not resolve within "
                    f"campaign representation: {relation.object_entity_id!r}"
                )

            location = entity_by_id[relation.object_entity_id]

            if (
                relation.relation_type == LOCATED_AT_RELATION_TYPE
                and location.classification != "place"
            ):
                raise InvalidLocatedAtRelationError(
                    "located_at object_entity_id must resolve to an entity "
                    "classified exactly as 'place'"
                )

            if relation.relation_type == CARRIED_BY_RELATION_TYPE:
                subject = entity_by_id[relation.subject_entity_id]
                if subject.classification != "object":
                    raise InvalidCarriedByRelationError(
                        "carried_by subject must be classified exactly as 'object'"
                    )
                if location.classification != "character_or_creature":
                    raise InvalidCarriedByRelationError(
                        "carried_by carrier must be classified exactly as "
                        "'character_or_creature'"
                    )

        object.__setattr__(self, "entities", entities)
        object.__setattr__(self, "relations", relations)


def create_persistent_world_entity(
    *,
    entity_id: str,
    classification: str,
) -> PersistentWorldEntity:
    return PersistentWorldEntity(
        entity_id=entity_id,
        classification=classification,
    )


def create_located_at_relation(
    *,
    relation_id: str,
    subject_entity_id: str,
    object_entity_id: str,
) -> PersistentWorldRelation:
    return PersistentWorldRelation(
        relation_id=relation_id,
        relation_type=LOCATED_AT_RELATION_TYPE,
        subject_entity_id=subject_entity_id,
        object_entity_id=object_entity_id,
        semantic_owner=LOCATED_AT_SEMANTIC_OWNER,
    )


def create_carried_by_relation(
    *,
    relation_id: str,
    subject_entity_id: str,
    object_entity_id: str,
) -> PersistentWorldRelation:
    return PersistentWorldRelation(
        relation_id=relation_id,
        relation_type=CARRIED_BY_RELATION_TYPE,
        subject_entity_id=subject_entity_id,
        object_entity_id=object_entity_id,
        semantic_owner=CARRIED_BY_SEMANTIC_OWNER,
    )


def create_persistent_world_entity_location_representation(
    *,
    campaign_id: str,
    entities: Sequence[PersistentWorldEntity] = (),
    relations: Sequence[PersistentWorldRelation] = (),
) -> PersistentWorldEntityLocationRepresentation:
    return PersistentWorldEntityLocationRepresentation(
        campaign_id=campaign_id,
        entities=tuple(entities),
        relations=tuple(relations),
    )


def serialize_persistent_world_entity_location_representation(
    representation: PersistentWorldEntityLocationRepresentation,
) -> dict[str, object]:
    if not isinstance(
        representation,
        PersistentWorldEntityLocationRepresentation,
    ):
        raise InvalidPersistentWorldRepresentationError(
            "representation must be "
            "PersistentWorldEntityLocationRepresentation"
        )

    return {
        "campaign_id": representation.campaign_id,
        "entities": [
            entity.to_dict()
            for entity in sorted(
                representation.entities,
                key=lambda item: item.entity_id,
            )
        ],
        "relations": [
            relation.to_dict()
            for relation in sorted(
                representation.relations,
                key=lambda item: item.relation_id,
            )
        ],
    }


def canonical_serialize_persistent_world_entity_location_representation(
    representation: PersistentWorldEntityLocationRepresentation,
) -> str:
    return json.dumps(
        serialize_persistent_world_entity_location_representation(
            representation
        ),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def create_scene_location_owner_transport_reference(
    representation: PersistentWorldEntityLocationRepresentation,
) -> StateOwnerInterfaceReference:
    """Create a reference-only scene_location_owner transport reference.

    No entity/relation payload is transported. The reference grants no raw
    state access, mutation authority, or semantic ownership.
    """

    if not isinstance(
        representation,
        PersistentWorldEntityLocationRepresentation,
    ):
        raise InvalidPersistentWorldRepresentationError(
            "representation must be "
            "PersistentWorldEntityLocationRepresentation"
        )

    return create_state_owner_interface_reference(
        reference_id=(
            f"{representation.campaign_id}"
            "#persistent-world-entity-location"
        ),
        reference_kind="state_record_ref",
        owner_family=SCENE_LOCATION_OWNER_FAMILY,
        source_scope=representation.campaign_id,
        metadata={
            "representation_kind": (
                "persistent_world_entity_location_representation"
            ),
            "raw_state_included": False,
            "mutation_authorized": False,
            "semantic_authority_acquired": False,
        },
    )
