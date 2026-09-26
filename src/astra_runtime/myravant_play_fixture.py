"""Bounded native fixture for the first human-playable Myravant terminal slice.

This module contains only fixture-local world facts and qualification material
needed to exercise already-implemented R4-B, R4-C, R4-D, and R4-E behavior. It is not
a generalized topology, legality, opportunity, persistence, visibility, or
content system.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
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
    digest_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    CustodyOpportunityEvidence,
    CustodyQualificationEvidence,
    create_persistent_world_object_custody_runtime_state,
    create_custody_opportunity_evidence,
    create_custody_qualification_evidence,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    ObjectOpenCloseOpportunityEvidence,
    ObjectOpenCloseQualificationEvidence,
    PersistentWorldObjectOpenState,
    create_persistent_world_object_open_close_runtime_state,
    create_object_open_close_opportunity_evidence,
    create_object_open_close_qualification_evidence,
    create_persistent_world_object_open_state,
    digest_persistent_world_composite_state,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    ObjectLitStateOpportunityEvidence,
    ObjectLitStateQualificationEvidence,
    PersistentWorldObjectLitState,
    create_object_lit_state_opportunity_evidence,
    create_object_lit_state_qualification_evidence,
    create_persistent_world_object_lit_state,
    digest_persistent_world_lit_composite_state,
    digest_persistent_world_object_lit_states,
)
from astra_runtime.kernel.record_identity import build_record_id


FIXTURE_ID = "myravant-native-terminal-g1"
FIXTURE_VERSION = "0.1.3"
FIXTURE_STATUS = "development_validation_content"
FIXTURE_CANON = False
FIXTURE_DEFAULT_WORLD = False
FIXTURE_ORIGIN_WORKSTREAM = "TERMINAL-PLAY-G1"
FIXTURE_ORIGIN_MERGE_COMMIT = "5429cdddf9dc71831fbb5ceab302e83e7f6e0f0c"
FIXTURE_ORIGIN_MERGED_AT = "2026-09-22T05:39:13Z"
FIXTURE_G1_BASELINE_SHA = "55461eb5ab9ac373cca9fa7b978ce71d0a11669c"
FIXTURE_INITIAL_STATE_DIGEST = (
    "124e7b67da79de2e267fe53ba0de51c88ec99070c06fae6ab0bd463d80b146eb"
)
FIXTURE_INITIAL_WORLD_STATE_DIGEST = (
    "f3065b22adb1ac5df2472ad7208048f6dca871e265fd1da1baceebf366a7a75f"
)
FIXTURE_INITIAL_OBJECT_LIT_STATE_DIGEST = (
    "db500e8154586baef322759b6c12690326a52beb79762b40019fd4f06f4d8679"
)
FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST = (
    "a6a130224028dc2ed1841caf604b7d61901c36390a5b1162b8f2da4280bc2628"
)
FIXTURE_PLAYABLE_NEED_REFS = (
    "R4-B",
    "R4-C",
    "R4-D",
    "TERMINAL-PLAY-G1",
    "TERMINAL-PLAY-OBS-1",
    "TERMINAL-PLAY-INT-1",
    "TERMINAL-PLAY-INT-2",
    "R4-E-readiness",
)
FIXTURE_REQUIREMENT_REFS = (
    "REQ-PROD-002",
    "REQ-PROD-003",
    "REQ-PROD-004",
    "REQ-PROD-006",
    "REQ-PROD-012",
    "REQ-PROD-013",
    "REQ-PROD-017",
)
FIXTURE_DIRECT_EXTERNAL_CONTENT_CONSULTED_DURING_G1 = False
FIXTURE_ORIGINALITY_REVIEW_STATUS = (
    "g0_review_complete_no_specific_source_derivation_detected"
)

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


class UnavailableFixtureCustodyError(MyravantPlayFixtureError):
    """Raised when bounded fixture custody policy cannot qualify a request."""


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
class FixtureProvenanceReceipt:
    fixture_id: str
    fixture_version: str
    fixture_status: str
    canon: bool
    default_world: bool
    origin_workstream: str
    origin_merge_commit: str
    origin_merged_at: str
    g1_baseline_sha: str
    playable_need_refs: tuple[str, ...]
    requirement_refs: tuple[str, ...]
    direct_external_content_consulted_during_g1: bool
    originality_review_status: str
    initial_state_digest: str
    initial_world_state_digest: str
    initial_object_lit_state_digest: str
    initial_int2_world_state_digest: str


@dataclass(frozen=True, kw_only=True)
class MyravantPlayFixture:
    campaign_id: str
    player_entity_id: str
    initial_state: PersistentWorldMovementRuntimeState
    initial_object_open_states: tuple[PersistentWorldObjectOpenState, ...]
    initial_object_lit_states: tuple[PersistentWorldObjectLitState, ...]
    place_presentations: tuple[PublicEntityPresentation, ...]
    object_presentations: tuple[PublicEntityPresentation, ...]
    movement_routes: tuple[FixtureMovementRoute, ...]
    checkpoint_qualification: Mapping[str, object]
    provenance: FixtureProvenanceReceipt

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

    def object_presentation(
        self,
        object_entity_id: str,
    ) -> PublicEntityPresentation:
        """Return declared public presentation without claiming observation authority."""

        for presentation in self.object_presentations:
            if presentation.entity_id == object_entity_id:
                return presentation
        raise UnavailableFixtureCustodyError(
            "object presentation is not declared in the bounded fixture"
        )

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

    def resolve_object_reference(self, reference: str) -> str:
        """Resolve a bounded player-facing object reference without authority."""

        normalized = " ".join(
            reference.strip().casefold().replace("-", " ").split()
        )
        if not normalized:
            raise UnavailableFixtureCustodyError(
                "object reference must be non-empty"
            )

        matches: list[str] = []
        for presentation in self.object_presentations:
            name = " ".join(
                presentation.name.casefold().replace("-", " ").split()
            )
            local_id = " ".join(
                presentation.entity_id.rsplit(":", 1)[-1]
                .casefold()
                .replace("-", " ")
                .split()
            )
            last_word = name.split()[-1]
            if normalized in {name, local_id, last_word}:
                matches.append(presentation.entity_id)

        if len(matches) != 1:
            raise UnavailableFixtureCustodyError(
                "object reference is unknown or ambiguous in the bounded fixture"
            )
        return matches[0]

    def custody_evidence(
        self,
        *,
        command_id: str,
        object_entity_id: str,
        operation: str,
    ) -> tuple[CustodyQualificationEvidence, CustodyOpportunityEvidence]:
        """Return fixture-qualified R4-E owner evidence for a known object.

        This policy establishes only that this development fixture adds no
        extra RT-010/AFQR-19 blocker for pickup/drop of its declared objects.
        R4-E still validates actor/object identity, immediate placement,
        co-location, current carrier, command identity, and transition state.
        """

        known_objects = {
            presentation.entity_id
            for presentation in self.object_presentations
        }
        if object_entity_id not in known_objects:
            raise UnavailableFixtureCustodyError(
                "custody target is not a declared fixture object"
            )
        if operation not in {"pickup", "drop"}:
            raise UnavailableFixtureCustodyError(
                "custody operation must be pickup or drop"
            )

        token = hashlib.sha256(
            f"{command_id}|{operation}|{object_entity_id}".encode("utf-8")
        ).hexdigest()[:20]

        qualification = create_custody_qualification_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"g2-custody-{operation}-{token}-rt010",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            qualified=True,
        )
        opportunity = create_custody_opportunity_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"g2-custody-{operation}-{token}-afqr19",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            opportunity_available=True,
            resolution_accepted=True,
        )
        return qualification, opportunity

    def object_open_close_evidence(
        self,
        *,
        command_id: str,
        object_entity_id: str,
        operation: str,
    ) -> tuple[
        ObjectOpenCloseQualificationEvidence,
        ObjectOpenCloseOpportunityEvidence,
    ]:
        """Return bounded RT-010/AFQR-19 evidence for the INT-1 chest route."""

        if object_entity_id != TOOL_CHEST_ID:
            raise UnavailableFixtureCustodyError(
                "target has no bounded fixture open/close state"
            )
        if operation not in {"open", "close"}:
            raise UnavailableFixtureCustodyError(
                "open/close operation must be open or close"
            )

        token = hashlib.sha256(
            f"{command_id}|{operation}|{object_entity_id}".encode("utf-8")
        ).hexdigest()[:20]
        qualification = create_object_open_close_qualification_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int1-{operation}-{token}-rt010",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            qualified=True,
        )
        opportunity = create_object_open_close_opportunity_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int1-{operation}-{token}-afqr19",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            opportunity_available=True,
            resolution_accepted=True,
        )
        return qualification, opportunity

    def public_open_state_description(
        self,
        *,
        object_entity_id: str,
        state: str,
    ) -> str:
        if object_entity_id != TOOL_CHEST_ID or state not in {"open", "closed"}:
            raise UnavailableFixtureCustodyError(
                "no bounded public open-state presentation exists"
            )
        return f"Its heavy lid is {state}."

    def object_lit_state_evidence(
        self,
        *,
        command_id: str,
        object_entity_id: str,
        operation: str,
    ) -> tuple[
        ObjectLitStateQualificationEvidence,
        ObjectLitStateOpportunityEvidence,
    ]:
        """Return bounded RT-010/AFQR-19 evidence for the INT-2 lantern route."""

        if object_entity_id != LANTERN_ID:
            raise UnavailableFixtureCustodyError(
                "target has no bounded fixture lit/unlit state"
            )
        if operation not in {"light", "extinguish"}:
            raise UnavailableFixtureCustodyError(
                "lit-state operation must be light or extinguish"
            )

        token = hashlib.sha256(
            f"{command_id}|{operation}|{object_entity_id}".encode("utf-8")
        ).hexdigest()[:20]
        qualification = create_object_lit_state_qualification_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int2-{operation}-{token}-rt010",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            qualified=True,
        )
        opportunity = create_object_lit_state_opportunity_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int2-{operation}-{token}-afqr19",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            opportunity_available=True,
            resolution_accepted=True,
        )
        return qualification, opportunity

    def public_lit_state_description(
        self,
        *,
        object_entity_id: str,
        state: str,
    ) -> str:
        if object_entity_id != LANTERN_ID or state not in {"unlit", "lit"}:
            raise UnavailableFixtureCustodyError(
                "no bounded public lit-state presentation exists"
            )
        if state == "unlit":
            return "Its flame is out."
        return "A steady flame burns within it."

    def public_entities_carried_by(
        self,
        representation: PersistentWorldEntityLocationRepresentation,
        carrier_entity_id: str,
    ) -> tuple[PublicEntityPresentation, ...]:
        carried_ids = {
            relation.subject_entity_id
            for relation in representation.relations
            if (
                relation.relation_type == CARRIED_BY_RELATION_TYPE
                and relation.object_entity_id == carrier_entity_id
            )
        }
        return tuple(
            presentation
            for presentation in self.object_presentations
            if presentation.entity_id in carried_ids
        )

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

    initial_state_digest = (
        digest_persistent_world_entity_location_representation(
            representation
        )
    )
    if initial_state_digest != FIXTURE_INITIAL_STATE_DIGEST:
        raise MyravantPlayFixtureError(
            "fixture authoritative initial state changed without updating "
            "FIXTURE_VERSION and FIXTURE_INITIAL_STATE_DIGEST"
        )

    initial_object_open_states = (
        create_persistent_world_object_open_state(
            object_entity_id=TOOL_CHEST_ID,
            state="closed",
        ),
    )
    initial_world_state_digest = digest_persistent_world_composite_state(
        representation,
        initial_object_open_states,
    )
    if initial_world_state_digest != FIXTURE_INITIAL_WORLD_STATE_DIGEST:
        raise MyravantPlayFixtureError(
            "fixture composite authoritative initial state changed without "
            "updating FIXTURE_VERSION and FIXTURE_INITIAL_WORLD_STATE_DIGEST"
        )

    initial_object_lit_states = (
        create_persistent_world_object_lit_state(
            object_entity_id=LANTERN_ID,
            state="unlit",
        ),
    )
    initial_object_lit_state_digest = digest_persistent_world_object_lit_states(
        initial_object_lit_states
    )
    if initial_object_lit_state_digest != FIXTURE_INITIAL_OBJECT_LIT_STATE_DIGEST:
        raise MyravantPlayFixtureError(
            "fixture lit-state digest changed without updating FIXTURE_VERSION "
            "and FIXTURE_INITIAL_OBJECT_LIT_STATE_DIGEST"
        )

    initial_int2_world_state_digest = digest_persistent_world_lit_composite_state(
        create_persistent_world_object_open_close_runtime_state(
            custody_state=create_persistent_world_object_custody_runtime_state(
                movement_state=create_persistent_world_movement_runtime_state(
                    representation=representation
                )
            ),
            object_open_states=initial_object_open_states,
        ),
        initial_object_lit_states,
    )
    if initial_int2_world_state_digest != FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST:
        raise MyravantPlayFixtureError(
            "fixture INT-2 authoritative initial state changed without updating "
            "FIXTURE_VERSION and FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST"
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
            description="A plain brass lantern with a dulled, well-handled surface.",
        ),
        PublicEntityPresentation(
            entity_id=TOOL_CHEST_ID,
            name="Tool Chest",
            description="A scarred tool chest with worn fittings and a heavy wooden lid.",
        ),
        PublicEntityPresentation(
            entity_id=WAYSTONE_ID,
            name="Weathered Waystone",
            description=(
                "A small weathered waystone with a rough, timeworn surface."
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

    provenance = FixtureProvenanceReceipt(
        fixture_id=FIXTURE_ID,
        fixture_version=FIXTURE_VERSION,
        fixture_status=FIXTURE_STATUS,
        canon=FIXTURE_CANON,
        default_world=FIXTURE_DEFAULT_WORLD,
        origin_workstream=FIXTURE_ORIGIN_WORKSTREAM,
        origin_merge_commit=FIXTURE_ORIGIN_MERGE_COMMIT,
        origin_merged_at=FIXTURE_ORIGIN_MERGED_AT,
        g1_baseline_sha=FIXTURE_G1_BASELINE_SHA,
        playable_need_refs=FIXTURE_PLAYABLE_NEED_REFS,
        requirement_refs=FIXTURE_REQUIREMENT_REFS,
        direct_external_content_consulted_during_g1=(
            FIXTURE_DIRECT_EXTERNAL_CONTENT_CONSULTED_DURING_G1
        ),
        originality_review_status=FIXTURE_ORIGINALITY_REVIEW_STATUS,
        initial_state_digest=initial_state_digest,
        initial_world_state_digest=initial_world_state_digest,
        initial_object_lit_state_digest=initial_object_lit_state_digest,
        initial_int2_world_state_digest=initial_int2_world_state_digest,
    )

    return MyravantPlayFixture(
        campaign_id=CAMPAIGN_ID,
        player_entity_id=PLAYER_ID,
        initial_state=create_persistent_world_movement_runtime_state(
            representation=representation
        ),
        initial_object_open_states=initial_object_open_states,
        initial_object_lit_states=initial_object_lit_states,
        place_presentations=places,
        object_presentations=objects,
        movement_routes=routes,
        checkpoint_qualification=checkpoint_qualification,
        provenance=provenance,
    )
