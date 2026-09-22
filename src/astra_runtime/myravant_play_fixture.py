"""Bounded native fixture for the first human-playable Myravant terminal slice.

This module contains only fixture-local world facts and qualification material
needed to exercise already-implemented R4-B, R4-C, and R4-D behavior. It is not
a generalized topology, legality, opportunity, persistence, visibility, or
content system.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
    PersistentWorldEntityLocationRepresentation,
    create_located_at_relation,
    create_persistent_world_entity,
    create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    MovementOpportunityEvidence,
    MovementSpatialEvidence,
    PersistentWorldMovementRuntimeState,
    create_movement_opportunity_evidence,
    create_movement_spatial_evidence,
    create_persistent_world_movement_runtime_state,
)
from astra_runtime.kernel.record_identity import build_record_id


CAMPAIGN_ID = "astra:campaign:myravant-terminal-g1"
PLAYER_ID = "astra:entity:terminal-traveler"
WORKSHOP_ID = "astra:entity:workshop"
YARD_ID = "astra:entity:yard"
ORCHARD_PATH_ID = "astra:entity:orchard-path"
GATEHOUSE_ID = "astra:entity:gatehouse"
LANTERN_ID = "astra:entity:brass-lantern"
TOOL_CHEST_ID = "astra:entity:tool-chest"
WAYSTONE_ID = "astra:entity:weathered-waystone"


class MyravantPlayFixtureError(ValueError):
    """Base error for bounded terminal-fixture operations."""


class UnknownFixturePlaceError(MyravantPlayFixtureError):
    """Raised when fixture presentation is requested for an unknown place."""


class UnavailableFixtureMovementError(MyravantPlayFixtureError):
    """Raised when the bounded fixture has no route for a requested direction."""


@dataclass(frozen=True, kw_only=True)
class PublicEntityPresentation:
    entity_id: str
    name: str
    description: str = ""


@dataclass(frozen=True, kw_only=True)
class FixtureMovementRoute:
    source_place_id: str
    direction: str
    destination_place_id: str


@dataclass(frozen=True, kw_only=True)
class MyravantPlayFixture:
    campaign_id: str
    player_entity_id: str
    initial_state: PersistentWorldMovementRuntimeState
    place_presentations: tuple[PublicEntityPresentation, ...]
    object_presentations: tuple[PublicEntityPresentation, ...]
    movement_routes: tuple[FixtureMovementRoute, ...]
    checkpoint_qualification: Mapping[str, object]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "checkpoint_qualification",
            MappingProxyType(dict(self.checkpoint_qualification)),
        )

    def place_presentation(self, place_id: str) -> PublicEntityPresentation:
        for presentation in self.place_presentations:
            if presentation.entity_id == place_id:
                return presentation
        raise UnknownFixturePlaceError(f"unknown fixture place: {place_id!r}")

    def entity_name(self, entity_id: str) -> str:
        for presentation in (
            *self.place_presentations,
            *self.object_presentations,
        ):
            if presentation.entity_id == entity_id:
                return presentation.name
        if entity_id == self.player_entity_id:
            return "Traveler"
        return entity_id

    def exits_from(self, place_id: str) -> tuple[str, ...]:
        return tuple(
            route.direction
            for route in self.movement_routes
            if route.source_place_id == place_id
        )

    def destination_for(self, *, source_place_id: str, direction: str) -> str:
        normalized = direction.strip().lower()
        for route in self.movement_routes:
            if (
                route.source_place_id == source_place_id
                and route.direction == normalized
            ):
                return route.destination_place_id
        raise UnavailableFixtureMovementError(
            f"no bounded fixture route from {source_place_id!r} toward {normalized!r}"
        )

    def movement_evidence(
        self,
        *,
        command_id: str,
        source_place_id: str,
        direction: str,
        destination_place_id: str,
    ) -> tuple[MovementSpatialEvidence, MovementOpportunityEvidence]:
        expected_destination = self.destination_for(
            source_place_id=source_place_id,
            direction=direction,
        )
        if expected_destination != destination_place_id:
            raise UnavailableFixtureMovementError(
                "requested destination does not match the explicit fixture route"
            )

        token = hashlib.sha256(command_id.encode("utf-8")).hexdigest()[:20]

        spatial = create_movement_spatial_evidence(
            evidence_id=build_record_id("evidence", f"g1-spatial-{token}"),
            actor_entity_id=self.player_entity_id,
            source_place_id=source_place_id,
            destination_place_id=destination_place_id,
            spatially_permitted=True,
        )
        opportunity = create_movement_opportunity_evidence(
            evidence_id=build_record_id("evidence", f"g1-opportunity-{token}"),
            actor_entity_id=self.player_entity_id,
            destination_place_id=destination_place_id,
            opportunity_available=True,
            resolution_accepted=True,
        )
        return spatial, opportunity

    def public_entities_at(
        self,
        representation: PersistentWorldEntityLocationRepresentation,
        place_id: str,
    ) -> tuple[PublicEntityPresentation, ...]:
        visible_ids = {
            relation.subject_entity_id
            for relation in representation.relations
            if (
                relation.relation_type == LOCATED_AT_RELATION_TYPE
                and relation.object_entity_id == place_id
                and relation.subject_entity_id != self.player_entity_id
            )
        }
        return tuple(
            presentation
            for presentation in self.object_presentations
            if presentation.entity_id in visible_ids
        )


def _entity(entity_id: str, classification: str):
    return create_persistent_world_entity(
        entity_id=entity_id,
        classification=classification,
    )


def _located(relation_local_id: str, subject_id: str, place_id: str):
    return create_located_at_relation(
        relation_id=build_record_id("relation", relation_local_id),
        subject_entity_id=subject_id,
        object_entity_id=place_id,
    )


def create_terminal_play_fixture() -> MyravantPlayFixture:
    representation = create_persistent_world_entity_location_representation(
        campaign_id=CAMPAIGN_ID,
        entities=(
            _entity(PLAYER_ID, "character_or_creature"),
            _entity(WORKSHOP_ID, "place"),
            _entity(YARD_ID, "place"),
            _entity(ORCHARD_PATH_ID, "place"),
            _entity(GATEHOUSE_ID, "place"),
            _entity(LANTERN_ID, "object"),
            _entity(TOOL_CHEST_ID, "object"),
            _entity(WAYSTONE_ID, "object"),
        ),
        relations=(
            _located("g1-player-workshop", PLAYER_ID, WORKSHOP_ID),
            _located("g1-lantern-workshop", LANTERN_ID, WORKSHOP_ID),
            _located("g1-tool-chest-yard", TOOL_CHEST_ID, YARD_ID),
            _located("g1-waystone-orchard", WAYSTONE_ID, ORCHARD_PATH_ID),
        ),
    )

    routes = (
        FixtureMovementRoute(
            source_place_id=WORKSHOP_ID,
            direction="south",
            destination_place_id=YARD_ID,
        ),
        FixtureMovementRoute(
            source_place_id=YARD_ID,
            direction="north",
            destination_place_id=WORKSHOP_ID,
        ),
        FixtureMovementRoute(
            source_place_id=YARD_ID,
            direction="east",
            destination_place_id=ORCHARD_PATH_ID,
        ),
        FixtureMovementRoute(
            source_place_id=ORCHARD_PATH_ID,
            direction="west",
            destination_place_id=YARD_ID,
        ),
        FixtureMovementRoute(
            source_place_id=YARD_ID,
            direction="south",
            destination_place_id=GATEHOUSE_ID,
        ),
        FixtureMovementRoute(
            source_place_id=GATEHOUSE_ID,
            direction="north",
            destination_place_id=YARD_ID,
        ),
    )

    places = (
        PublicEntityPresentation(
            entity_id=WORKSHOP_ID,
            name="Workshop",
            description="A narrow workroom opens onto the yard.",
        ),
        PublicEntityPresentation(
            entity_id=YARD_ID,
            name="Yard",
            description=(
                "A packed-earth yard links the workshop, orchard path, "
                "and gatehouse."
            ),
        ),
        PublicEntityPresentation(
            entity_id=ORCHARD_PATH_ID,
            name="Orchard Path",
            description=(
                "A worn path runs beside low fruit trees and returns "
                "toward the yard."
            ),
        ),
        PublicEntityPresentation(
            entity_id=GATEHOUSE_ID,
            name="Gatehouse",
            description=(
                "A small gatehouse marks the southern edge of the "
                "bounded test grounds."
            ),
        ),
    )

    objects = (
        PublicEntityPresentation(
            entity_id=LANTERN_ID,
            name="Brass Lantern",
            description="A plain brass lantern rests near the workbench.",
        ),
        PublicEntityPresentation(
            entity_id=TOOL_CHEST_ID,
            name="Tool Chest",
            description="A scarred tool chest sits against the yard wall.",
        ),
        PublicEntityPresentation(
            entity_id=WAYSTONE_ID,
            name="Weathered Waystone",
            description=(
                "A small weathered waystone stands beside the orchard path."
            ),
        ),
    )

    checkpoint_qualification = {
        "qualification_id": build_record_id(
            "evidence",
            "g1-player-checkpoint-policy",
        ),
        "semantic_owner": "AFQR-01",
        "qualified": True,
        "provenance": "TERMINAL-PLAY-G1 bounded native fixture policy",
        "fixture_campaign_id": CAMPAIGN_ID,
    }

    return MyravantPlayFixture(
        campaign_id=CAMPAIGN_ID,
        player_entity_id=PLAYER_ID,
        initial_state=create_persistent_world_movement_runtime_state(
            representation=representation
        ),
        place_presentations=places,
        object_presentations=objects,
        movement_routes=routes,
        checkpoint_qualification=checkpoint_qualification,
    )
