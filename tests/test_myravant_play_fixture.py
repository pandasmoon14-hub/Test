"""Focused tests for the bounded Myravant terminal fixture."""

from __future__ import annotations

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_fixture import (
    CAMPAIGN_ID,
    GATEHOUSE_ID,
    ORCHARD_PATH_ID,
    PLAYER_ID,
    WORKSHOP_ID,
    YARD_ID,
    UnavailableFixtureMovementError,
    create_terminal_play_fixture,
)


def test_fixture_has_one_player_four_places_and_persistent_objects():
    fixture = create_terminal_play_fixture()
    representation = fixture.initial_state.representation

    assert representation.campaign_id == CAMPAIGN_ID
    assert fixture.player_entity_id == PLAYER_ID

    classifications = {
        entity.entity_id: entity.classification
        for entity in representation.entities
    }

    assert classifications[PLAYER_ID] == "character_or_creature"
    assert {
        WORKSHOP_ID,
        YARD_ID,
        ORCHARD_PATH_ID,
        GATEHOUSE_ID,
    } == {
        entity_id
        for entity_id, classification in classifications.items()
        if classification == "place"
    }
    assert sum(
        classification == "object"
        for classification in classifications.values()
    ) == 3


def test_fixture_player_starts_at_exactly_one_authoritative_location():
    fixture = create_terminal_play_fixture()
    relations = [
        relation
        for relation in fixture.initial_state.representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == PLAYER_ID
        )
    ]

    assert len(relations) == 1
    assert relations[0].object_entity_id == WORKSHOP_ID


def test_fixture_routes_are_explicit_not_inferred():
    fixture = create_terminal_play_fixture()

    assert fixture.destination_for(
        source_place_id=WORKSHOP_ID,
        direction="south",
    ) == YARD_ID

    with pytest.raises(UnavailableFixtureMovementError):
        fixture.destination_for(
            source_place_id=WORKSHOP_ID,
            direction="east",
        )


def test_fixture_builds_owner_routed_movement_evidence_only_for_declared_route():
    fixture = create_terminal_play_fixture()

    spatial, opportunity = fixture.movement_evidence(
        command_id="terminal-move-000001",
        source_place_id=WORKSHOP_ID,
        direction="south",
        destination_place_id=YARD_ID,
    )

    assert spatial.semantic_owner == "AFQR-18"
    assert spatial.spatially_permitted is True
    assert opportunity.semantic_owner == "AFQR-19"
    assert opportunity.opportunity_available is True
    assert opportunity.resolution_accepted is True

    with pytest.raises(UnavailableFixtureMovementError):
        fixture.movement_evidence(
            command_id="terminal-move-000002",
            source_place_id=WORKSHOP_ID,
            direction="east",
            destination_place_id=ORCHARD_PATH_ID,
        )


def test_checkpoint_qualification_is_fixture_policy_not_terminal_assertion():
    fixture = create_terminal_play_fixture()
    qualification = fixture.checkpoint_qualification

    assert qualification["semantic_owner"] == "AFQR-01"
    assert qualification["qualified"] is True
    assert qualification["fixture_campaign_id"] == CAMPAIGN_ID
    assert "TERMINAL-PLAY-G1" in qualification["provenance"]
