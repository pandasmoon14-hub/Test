"""Focused tests for the bounded Myravant terminal fixture."""

from __future__ import annotations

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
    serialize_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.myravant_play_fixture import (
    CAMPAIGN_ID,
    FIXTURE_CANON,
    FIXTURE_DEFAULT_WORLD,
    FIXTURE_DIRECT_EXTERNAL_CONTENT_CONSULTED_DURING_G1,
    FIXTURE_G1_BASELINE_SHA,
    FIXTURE_ID,
    FIXTURE_INITIAL_STATE_DIGEST,
    FIXTURE_ORIGINALITY_REVIEW_STATUS,
    FIXTURE_ORIGIN_MERGE_COMMIT,
    FIXTURE_ORIGIN_MERGED_AT,
    FIXTURE_ORIGIN_WORKSTREAM,
    FIXTURE_PLAYABLE_NEED_REFS,
    FIXTURE_REQUIREMENT_REFS,
    FIXTURE_STATUS,
    FIXTURE_VERSION,
    GATEHOUSE_ID,
    LANTERN_ID,
    ORCHARD_PATH_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
    WAYSTONE_ID,
    WORKSHOP_ID,
    YARD_ID,
    UnavailableFixtureCustodyError,
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
    assert {
        LANTERN_ID,
        TOOL_CHEST_ID,
        WAYSTONE_ID,
    } == {
        entity_id
        for entity_id, classification in classifications.items()
        if classification == "object"
    }


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


def test_fixture_authoritative_starting_structure_is_version_locked():
    fixture = create_terminal_play_fixture()
    representation = fixture.initial_state.representation

    placements = {
        (relation.subject_entity_id, relation.object_entity_id)
        for relation in representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
    }

    assert placements == {
        (PLAYER_ID, WORKSHOP_ID),
        (LANTERN_ID, WORKSHOP_ID),
        (TOOL_CHEST_ID, YARD_ID),
        (WAYSTONE_ID, ORCHARD_PATH_ID),
    }

    actual_digest = digest_persistent_world_entity_location_representation(
        representation
    )
    assert actual_digest == FIXTURE_INITIAL_STATE_DIGEST
    assert fixture.provenance.initial_state_digest == actual_digest


def test_fixture_construction_is_deterministic_for_same_version():
    first = create_terminal_play_fixture()
    second = create_terminal_play_fixture()

    assert first.provenance.fixture_id == second.provenance.fixture_id
    assert first.provenance.fixture_version == second.provenance.fixture_version
    assert (
        digest_persistent_world_entity_location_representation(
            first.initial_state.representation
        )
        == digest_persistent_world_entity_location_representation(
            second.initial_state.representation
        )
        == FIXTURE_INITIAL_STATE_DIGEST
    )


def test_fixture_provenance_marks_development_noncanon_boundary():
    fixture = create_terminal_play_fixture()
    provenance = fixture.provenance

    assert provenance.fixture_id == FIXTURE_ID
    assert provenance.fixture_version == FIXTURE_VERSION
    assert provenance.fixture_status == FIXTURE_STATUS
    assert provenance.canon is FIXTURE_CANON is False
    assert provenance.default_world is FIXTURE_DEFAULT_WORLD is False
    assert provenance.origin_workstream == FIXTURE_ORIGIN_WORKSTREAM
    assert provenance.origin_merge_commit == FIXTURE_ORIGIN_MERGE_COMMIT
    assert provenance.origin_merged_at == FIXTURE_ORIGIN_MERGED_AT
    assert provenance.g1_baseline_sha == FIXTURE_G1_BASELINE_SHA
    assert provenance.playable_need_refs == FIXTURE_PLAYABLE_NEED_REFS
    assert provenance.requirement_refs == FIXTURE_REQUIREMENT_REFS
    assert (
        provenance.direct_external_content_consulted_during_g1
        is FIXTURE_DIRECT_EXTERNAL_CONTENT_CONSULTED_DURING_G1
        is False
    )
    assert (
        provenance.originality_review_status
        == FIXTURE_ORIGINALITY_REVIEW_STATUS
    )


def test_fixture_presentation_does_not_enter_authoritative_representation():
    fixture = create_terminal_play_fixture()
    serialized = serialize_persistent_world_entity_location_representation(
        fixture.initial_state.representation
    )

    assert set(serialized) == {"campaign_id", "entities", "relations"}
    assert all("name" not in entity for entity in serialized["entities"])
    assert all("description" not in entity for entity in serialized["entities"])
    assert all("name" not in relation for relation in serialized["relations"])
    assert all(
        "description" not in relation for relation in serialized["relations"]
    )


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


def test_fixture_route_set_remains_the_bounded_terminal_g1_topology():
    fixture = create_terminal_play_fixture()

    assert {
        (
            route.source_place_id,
            route.direction,
            route.destination_place_id,
        )
        for route in fixture.movement_routes
    } == {
        (WORKSHOP_ID, "south", YARD_ID),
        (YARD_ID, "north", WORKSHOP_ID),
        (YARD_ID, "east", ORCHARD_PATH_ID),
        (ORCHARD_PATH_ID, "west", YARD_ID),
        (YARD_ID, "south", GATEHOUSE_ID),
        (GATEHOUSE_ID, "north", YARD_ID),
    }


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


def test_fixture_object_reference_resolution_is_bounded_and_unambiguous():
    fixture = create_terminal_play_fixture()

    assert fixture.resolve_object_reference("Brass Lantern") == LANTERN_ID
    assert fixture.resolve_object_reference("lantern") == LANTERN_ID
    assert fixture.resolve_object_reference("tool-chest") == TOOL_CHEST_ID
    assert fixture.resolve_object_reference("waystone") == WAYSTONE_ID

    with pytest.raises(UnavailableFixtureCustodyError):
        fixture.resolve_object_reference("sword")


def test_fixture_custody_policy_emits_only_bounded_owner_evidence():
    fixture = create_terminal_play_fixture()

    qualification, opportunity = fixture.custody_evidence(
        command_id="terminal-custody-000001",
        object_entity_id=LANTERN_ID,
        operation="pickup",
    )

    assert qualification.semantic_owner == "RT-010"
    assert qualification.actor_entity_id == PLAYER_ID
    assert qualification.object_entity_id == LANTERN_ID
    assert qualification.operation == "pickup"
    assert qualification.qualified is True

    assert opportunity.semantic_owner == "AFQR-19"
    assert opportunity.actor_entity_id == PLAYER_ID
    assert opportunity.object_entity_id == LANTERN_ID
    assert opportunity.operation == "pickup"
    assert opportunity.opportunity_available is True
    assert opportunity.resolution_accepted is True

    with pytest.raises(UnavailableFixtureCustodyError):
        fixture.custody_evidence(
            command_id="terminal-custody-000002",
            object_entity_id="astra:entity:not-in-fixture",
            operation="pickup",
        )

    with pytest.raises(UnavailableFixtureCustodyError):
        fixture.custody_evidence(
            command_id="terminal-custody-000003",
            object_entity_id=LANTERN_ID,
            operation="transfer",
        )

def test_obs1_fixture_public_descriptions_are_state_independent_and_versioned():
    fixture = create_terminal_play_fixture()

    assert FIXTURE_VERSION == "0.1.2"
    assert "TERMINAL-PLAY-OBS-1" in FIXTURE_PLAYABLE_NEED_REFS
    assert "TERMINAL-PLAY-INT-1" in FIXTURE_PLAYABLE_NEED_REFS
    assert fixture.provenance.initial_state_digest == FIXTURE_INITIAL_STATE_DIGEST

    lantern = fixture.object_presentation(LANTERN_ID)
    chest = fixture.object_presentation(TOOL_CHEST_ID)
    waystone = fixture.object_presentation(WAYSTONE_ID)

    assert lantern.name == "Brass Lantern"
    assert chest.name == "Tool Chest"
    assert waystone.name == "Weathered Waystone"

    combined = " ".join(
        (lantern.description, chest.description, waystone.description)
    ).casefold()
    for stale_placement_phrase in ("workbench", "yard wall", "orchard path"):
        assert stale_placement_phrase not in combined
