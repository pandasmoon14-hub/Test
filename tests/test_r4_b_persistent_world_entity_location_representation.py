"""Executable R4-B persistent-world entity/location representation tests."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
    LOCATED_AT_SEMANTIC_OWNER,
    MINIMUM_PLAYABLE_ENTITY_CLASSIFICATIONS,
    SCENE_LOCATION_OWNER_FAMILY,
    DuplicatePersistentWorldEntityIdError,
    DuplicatePersistentWorldRelationIdError,
    InvalidLocatedAtRelationError,
    InvalidPersistentWorldEntityError,
    InvalidPersistentWorldRelationError,
    UnresolvedPersistentWorldRelationReferenceError,
    UnsupportedPersistentWorldRelationTypeError,
    PersistentWorldRelation,
    canonical_serialize_persistent_world_entity_location_representation,
    create_located_at_relation,
    create_persistent_world_entity,
    create_persistent_world_entity_location_representation,
    create_scene_location_owner_transport_reference,
    serialize_persistent_world_entity_location_representation,
)
from astra_runtime.domain.state_owner_interface_contract_skeleton import (
    StateOwnerInterfaceReference,
)
from astra_runtime.kernel.record_identity import parse_record_id

ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "src/astra_runtime/domain/"
    "persistent_world_entity_location_representation.py"
)


def _entity(local_id: str, classification: str):
    return create_persistent_world_entity(
        entity_id=f"astra:entity:{local_id}",
        classification=classification,
    )


def _relation(
    local_id: str,
    subject_id: str,
    place_id: str,
):
    return create_located_at_relation(
        relation_id=f"astra:relation:{local_id}",
        subject_entity_id=subject_id,
        object_entity_id=place_id,
    )


def test_existing_record_identity_surface_is_reused():
    entity = _entity(
        "wanderer",
        "character_or_creature",
    )

    parsed = parse_record_id(entity.entity_id)

    assert parsed.full_id == entity.entity_id
    assert entity.entity_id.startswith("astra:")


@pytest.mark.parametrize(
    "bad_id",
    [
        "",
        "not-a-record-id",
        "other:entity:test",
        "astra:Entity:test",
        " astra:entity:test",
    ],
)
def test_malformed_entity_identity_fails_closed(bad_id):
    with pytest.raises(InvalidPersistentWorldEntityError):
        create_persistent_world_entity(
            entity_id=bad_id,
            classification="object",
        )


def test_minimum_playable_classifications_are_supported():
    assert MINIMUM_PLAYABLE_ENTITY_CLASSIFICATIONS == {
        "character_or_creature",
        "place",
        "object",
    }

    for classification in (
        "character_or_creature",
        "place",
        "object",
    ):
        entity = _entity(
            classification,
            classification,
        )
        assert entity.classification == classification


def test_classification_is_open_ended_not_closed_enum():
    vehicle = _entity(
        "river-barge",
        "vehicle",
    )

    assert vehicle.classification == "vehicle"


def test_invalid_classification_fails_closed():
    for value in ("", "Place", "two words", " place"):
        with pytest.raises(InvalidPersistentWorldEntityError):
            _entity("bad-classification", value)


def test_entity_serialization_does_not_imply_authority():
    entity = _entity(
        "traveler",
        "character_or_creature",
    )

    assert entity.to_dict() == {
        "entity_id": "astra:entity:traveler",
        "classification": "character_or_creature",
    }

    serialized = json.dumps(entity.to_dict())

    for token in (
        "control",
        "agency",
        "ownership",
        "authority",
        "knowledge",
        "visibility",
    ):
        assert token not in serialized


def test_located_at_relation_has_exact_required_fields():
    relation = _relation(
        "traveler-at-square",
        "astra:entity:traveler",
        "astra:entity:town-square",
    )

    assert relation.to_dict() == {
        "relation_id": "astra:relation:traveler-at-square",
        "relation_type": LOCATED_AT_RELATION_TYPE,
        "subject_entity_id": "astra:entity:traveler",
        "object_entity_id": "astra:entity:town-square",
        "semantic_owner": LOCATED_AT_SEMANTIC_OWNER,
    }

    assert LOCATED_AT_RELATION_TYPE == "located_at"
    assert LOCATED_AT_SEMANTIC_OWNER == "AFQR-18"


def test_wrong_located_at_semantic_owner_fails_closed():
    with pytest.raises(InvalidLocatedAtRelationError):
        PersistentWorldRelation(
            relation_id="astra:relation:wrong-owner",
            relation_type="located_at",
            subject_entity_id="astra:entity:traveler",
            object_entity_id="astra:entity:square",
            semantic_owner="some-other-owner",
        )


def test_unqualified_relation_extension_fails_closed():
    with pytest.raises(
        UnsupportedPersistentWorldRelationTypeError
    ):
        PersistentWorldRelation(
            relation_id="astra:relation:owns-sword",
            relation_type="owns",
            subject_entity_id="astra:entity:traveler",
            object_entity_id="astra:entity:sword",
            semantic_owner="AFQR-18",
        )


def test_malformed_relation_identity_fails_closed():
    with pytest.raises(InvalidPersistentWorldRelationError):
        create_located_at_relation(
            relation_id="bad-relation-id",
            subject_entity_id="astra:entity:traveler",
            object_entity_id="astra:entity:square",
        )


def test_relations_resolve_inside_same_campaign_representation():
    traveler = _entity(
        "traveler",
        "character_or_creature",
    )

    square = _entity(
        "square",
        "place",
    )

    relation = _relation(
        "traveler-at-square",
        traveler.entity_id,
        square.entity_id,
    )

    representation = (
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:alpha",
            entities=[traveler, square],
            relations=[relation],
        )
    )

    assert len(representation.entities) == 2
    assert len(representation.relations) == 1


def test_missing_relation_subject_fails_closed():
    square = _entity(
        "square",
        "place",
    )

    relation = _relation(
        "missing-at-square",
        "astra:entity:missing",
        square.entity_id,
    )

    with pytest.raises(
        UnresolvedPersistentWorldRelationReferenceError
    ):
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:alpha",
            entities=[square],
            relations=[relation],
        )


def test_missing_relation_object_fails_closed():
    traveler = _entity(
        "traveler",
        "character_or_creature",
    )

    relation = _relation(
        "traveler-at-missing",
        traveler.entity_id,
        "astra:entity:missing",
    )

    with pytest.raises(
        UnresolvedPersistentWorldRelationReferenceError
    ):
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:alpha",
            entities=[traveler],
            relations=[relation],
        )


def test_located_at_object_must_be_place():
    traveler = _entity(
        "traveler",
        "character_or_creature",
    )

    sword = _entity(
        "sword",
        "object",
    )

    relation = _relation(
        "traveler-at-sword",
        traveler.entity_id,
        sword.entity_id,
    )

    with pytest.raises(InvalidLocatedAtRelationError):
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:alpha",
            entities=[traveler, sword],
            relations=[relation],
        )


def test_duplicate_entity_ids_fail_closed():
    first = _entity(
        "duplicate",
        "object",
    )

    second = _entity(
        "duplicate",
        "vehicle",
    )

    with pytest.raises(
        DuplicatePersistentWorldEntityIdError
    ):
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:alpha",
            entities=[first, second],
        )


def test_duplicate_relation_ids_fail_closed():
    traveler = _entity(
        "traveler",
        "character_or_creature",
    )

    sword = _entity(
        "sword",
        "object",
    )

    square = _entity(
        "square",
        "place",
    )

    relation_a = _relation(
        "duplicate",
        traveler.entity_id,
        square.entity_id,
    )

    relation_b = _relation(
        "duplicate",
        sword.entity_id,
        square.entity_id,
    )

    with pytest.raises(
        DuplicatePersistentWorldRelationIdError
    ):
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:alpha",
            entities=[traveler, sword, square],
            relations=[relation_a, relation_b],
        )


def test_serialization_is_stable_across_input_order():
    traveler = _entity(
        "traveler",
        "character_or_creature",
    )

    sword = _entity(
        "sword",
        "object",
    )

    square = _entity(
        "square",
        "place",
    )

    traveler_location = _relation(
        "traveler-location",
        traveler.entity_id,
        square.entity_id,
    )

    sword_location = _relation(
        "sword-location",
        sword.entity_id,
        square.entity_id,
    )

    first = create_persistent_world_entity_location_representation(
        campaign_id="astra:campaign:alpha",
        entities=[traveler, sword, square],
        relations=[traveler_location, sword_location],
    )

    second = create_persistent_world_entity_location_representation(
        campaign_id="astra:campaign:alpha",
        entities=[square, sword, traveler],
        relations=[sword_location, traveler_location],
    )

    assert (
        serialize_persistent_world_entity_location_representation(
            first
        )
        == serialize_persistent_world_entity_location_representation(
            second
        )
    )

    assert (
        canonical_serialize_persistent_world_entity_location_representation(
            first
        )
        == canonical_serialize_persistent_world_entity_location_representation(
            second
        )
    )


def test_canonical_serialization_is_repeatable():
    place = _entity(
        "place",
        "place",
    )

    representation = (
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:repeatable",
            entities=[place],
        )
    )

    outputs = {
        canonical_serialize_persistent_world_entity_location_representation(
            representation
        )
        for _ in range(100)
    }

    assert len(outputs) == 1


def test_scene_location_owner_transport_is_reference_only():
    traveler = _entity(
        "traveler",
        "character_or_creature",
    )

    square = _entity(
        "square",
        "place",
    )

    representation = (
        create_persistent_world_entity_location_representation(
            campaign_id="astra:campaign:alpha",
            entities=[traveler, square],
            relations=[
                _relation(
                    "traveler-at-square",
                    traveler.entity_id,
                    square.entity_id,
                )
            ],
        )
    )

    reference = create_scene_location_owner_transport_reference(
        representation
    )

    assert isinstance(reference, StateOwnerInterfaceReference)
    assert reference.owner_family == SCENE_LOCATION_OWNER_FAMILY
    assert reference.owner_family == "scene_location_owner"
    assert reference.reference_kind == "state_record_ref"

    assert reference.metadata == {
        "representation_kind": (
            "persistent_world_entity_location_representation"
        ),
        "raw_state_included": False,
        "mutation_authorized": False,
        "semantic_authority_acquired": False,
    }

    serialized_reference = reference.to_dict()

    assert "entities" not in serialized_reference
    assert "relations" not in serialized_reference


def test_r4_b_module_has_no_forbidden_runtime_dependencies():
    tree = ast.parse(
        SOURCE.read_text(
            encoding="utf-8",
        )
    )

    imported_roots = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(
                alias.name.split(".", 1)[0]
                for alias in node.names
            )

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_roots.add(
                    node.module.split(".", 1)[0]
                )

    assert imported_roots.isdisjoint(
        {
            "random",
            "requests",
            "httpx",
            "urllib",
            "socket",
            "sqlite3",
            "openai",
            "anthropic",
        }
    )
