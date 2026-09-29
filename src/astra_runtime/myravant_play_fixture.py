"""Bounded native fixture for the first human-playable Myravant terminal slice.

This module contains only fixture-local world facts and qualification material
needed to exercise already-implemented R4-B, R4-C, R4-D, and R4-E behavior. It is not
a generalized topology, legality, opportunity, persistence, visibility, or
content system.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    CONTAINED_BY_RELATION_TYPE,
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
    create_persistent_world_object_lit_runtime_state,
    digest_persistent_world_lit_composite_state,
    digest_persistent_world_object_lit_states,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    ObjectStorageOpportunityEvidence,
    ObjectStorageQualificationEvidence,
    create_object_storage_opportunity_evidence,
    create_object_storage_qualification_evidence,
    digest_persistent_world_storage_composite_state,
)
from astra_runtime.kernel.record_identity import build_record_id


FIXTURE_ID = "myravant-native-terminal-g1"
FIXTURE_VERSION = "0.2.1"
FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION = "comp1-v1"
FIXTURE_AMBIENT_VISUAL_CONDITION_DIGEST = (
    "2cb0800bc31c0e4844b25b82fad5c0ed421898b59c3d13c109ea475f05ddfb34"
)
AFQR17_FIXTURE_ENVIRONMENT_OWNER = "AFQR-17"
AFQR20_FIXTURE_SENSING_OWNER = "AFQR-20"
AMBIENT_VISUAL_CONDITIONS = frozenset({"sufficient", "insufficient"})
FIXTURE_STATUS = "development_validation_content"
FIXTURE_CANON = False
FIXTURE_DEFAULT_WORLD = False
FIXTURE_ORIGIN_WORKSTREAM = "TERMINAL-PLAY-G1"
FIXTURE_ORIGIN_MERGE_COMMIT = "5429cdddf9dc71831fbb5ceab302e83e7f6e0f0c"
FIXTURE_ORIGIN_MERGED_AT = "2026-09-22T05:39:13Z"
FIXTURE_G1_BASELINE_SHA = "55461eb5ab9ac373cca9fa7b978ce71d0a11669c"
FIXTURE_INITIAL_STATE_DIGEST = (
    "6034a438607cfbe096a8ef7e7c11f7912bf02b4dc92b23c9cecd89ccf26fd35c"
)
FIXTURE_INITIAL_WORLD_STATE_DIGEST = (
    "46d1a4b67b1045a87efbba4f79429ae2370d35aeff8de2954c78f6580265cfe7"
)
FIXTURE_INITIAL_OBJECT_LIT_STATE_DIGEST = (
    "db500e8154586baef322759b6c12690326a52beb79762b40019fd4f06f4d8679"
)
FIXTURE_INT2_INITIAL_WORLD_STATE_DIGEST = (
    "a5e5f5ad8f1295a787219e10f27401e3dbcf6a12e725a97230cb618245353f2f"
)
FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST = (
    "15d06c3da065020878792cc774d4cf51998094ddd9b76a68eb5da77b26380094"
)
FIXTURE_PLAYABLE_NEED_REFS = (
    "R4-B",
    "R4-C",
    "R4-D",
    "TERMINAL-PLAY-G1",
    "TERMINAL-PLAY-OBS-1",
    "TERMINAL-PLAY-INT-1",
    "TERMINAL-PLAY-INT-2",
    "TERMINAL-PLAY-INT-3",
    "TERMINAL-PLAY-COMP-1",
    "TERMINAL-PLAY-COMP-2",
    "TERMINAL-PLAY-WORLD-1",
    "TERMINAL-PLAY-WORLD-2",
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
GROUNDSKEEPER_ID = "astra:entity:groundskeeper"


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
class FixtureVisualObservationEvidence:
    """Derived AFQR-20 evidence; never authoritative state or actor knowledge."""

    evidence_id: str
    observer_entity_id: str
    target_entity_id: str
    place_id: str
    ambient_condition: str
    local_light_available: bool
    observable: bool
    basis: str
    semantic_owner: str = AFQR20_FIXTURE_SENSING_OWNER


def digest_fixture_ambient_visual_conditions(
    conditions: Mapping[str, str],
) -> str:
    normalized = dict(sorted(conditions.items()))
    if any(value not in AMBIENT_VISUAL_CONDITIONS for value in normalized.values()):
        raise MyravantPlayFixtureError(
            "ambient visual conditions must be sufficient or insufficient"
        )
    material = {
        "state_family": "afqr17_fixture_ambient_visual_condition",
        "semantic_owner": AFQR17_FIXTURE_ENVIRONMENT_OWNER,
        "conditions": normalized,
    }
    canonical = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


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
    initial_int3_world_state_digest: str
    ambient_visual_profile_version: str
    ambient_visual_condition_digest: str


@dataclass(frozen=True, kw_only=True)
class MyravantPlayFixture:
    campaign_id: str
    player_entity_id: str
    initial_state: PersistentWorldMovementRuntimeState
    initial_object_open_states: tuple[PersistentWorldObjectOpenState, ...]
    initial_object_lit_states: tuple[PersistentWorldObjectLitState, ...]
    ambient_visual_conditions: Mapping[str, str]
    ambient_visual_profile_version: str
    place_presentations: tuple[PublicEntityPresentation, ...]
    object_presentations: tuple[PublicEntityPresentation, ...]
    actor_presentations: tuple[PublicEntityPresentation, ...]
    movement_routes: tuple[FixtureMovementRoute, ...]
    checkpoint_qualification: Mapping[str, object]
    provenance: FixtureProvenanceReceipt

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "checkpoint_qualification",
            MappingProxyType(dict(self.checkpoint_qualification)),
        )
        object.__setattr__(
            self,
            "ambient_visual_conditions",
            MappingProxyType(dict(self.ambient_visual_conditions)),
        )
        if self.ambient_visual_profile_version != FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION:
            raise MyravantPlayFixtureError(
                "ambient visual profile version disagrees with fixture constant"
            )
        place_ids = {
            presentation.entity_id
            for presentation in self.place_presentations
        }
        if set(self.ambient_visual_conditions) != place_ids:
            raise MyravantPlayFixtureError(
                "ambient visual conditions must cover every bounded fixture place"
            )
        if any(
            value not in AMBIENT_VISUAL_CONDITIONS
            for value in self.ambient_visual_conditions.values()
        ):
            raise MyravantPlayFixtureError(
                "ambient visual conditions must be sufficient or insufficient"
            )
        declared_ids = [
            *(item.entity_id for item in self.place_presentations),
            *(item.entity_id for item in self.object_presentations),
            *(item.entity_id for item in self.actor_presentations),
        ]
        if len(declared_ids) != len(set(declared_ids)):
            raise MyravantPlayFixtureError(
                "place/object/actor presentation identities must be disjoint"
            )

    def place_presentation(self, place_id: str) -> PublicEntityPresentation:
        for presentation in self.place_presentations:
            if presentation.entity_id == place_id:
                return presentation
        raise UnknownFixturePlaceError(f"unknown fixture place: {place_id!r}")

    def ambient_visual_condition_for(self, place_id: str) -> str:
        try:
            return self.ambient_visual_conditions[place_id]
        except KeyError as exc:
            raise UnknownFixturePlaceError(
                f"no bounded ambient visual condition for place: {place_id!r}"
            ) from exc

    def visual_observation_evidence(
        self,
        *,
        observer_entity_id: str,
        target_entity_id: str,
        place_id: str,
        local_light_available: bool,
    ) -> FixtureVisualObservationEvidence:
        """Derive bounded AFQR-20 observation without creating knowledge or state."""

        if observer_entity_id != self.player_entity_id:
            raise MyravantPlayFixtureError(
                "COMP-1 supports only the bounded fixture player observer"
            )
        observable_target_ids = {
            presentation.entity_id
            for presentation in (
                *self.object_presentations,
                *self.actor_presentations,
            )
        }
        if target_entity_id not in observable_target_ids:
            raise UnavailableFixtureCustodyError(
                "visual observation target is not a declared fixture entity"
            )
        if type(local_light_available) is not bool:
            raise MyravantPlayFixtureError(
                "local_light_available must be bool"
            )

        ambient_condition = self.ambient_visual_condition_for(place_id)
        observable = (
            ambient_condition == "sufficient"
            or local_light_available
        )
        basis = (
            "ambient_sufficient"
            if ambient_condition == "sufficient"
            else "local_light_source"
            if local_light_available
            else "insufficient_visual_signal"
        )
        token = hashlib.sha256(
            (
                f"{observer_entity_id}|{target_entity_id}|{place_id}|"
                f"{ambient_condition}|{int(local_light_available)}"
            ).encode("utf-8")
        ).hexdigest()[:20]
        return FixtureVisualObservationEvidence(
            evidence_id=build_record_id(
                "evidence",
                f"comp1-visual-{token}",
            ),
            observer_entity_id=observer_entity_id,
            target_entity_id=target_entity_id,
            place_id=place_id,
            ambient_condition=ambient_condition,
            local_light_available=local_light_available,
            observable=observable,
            basis=basis,
        )

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

    def actor_presentation(
        self, actor_entity_id: str,
    ) -> PublicEntityPresentation:
        for presentation in self.actor_presentations:
            if presentation.entity_id == actor_entity_id:
                return presentation
        raise MyravantPlayFixtureError(
            "actor presentation is not declared in the bounded fixture"
        )

    def entity_name(self, entity_id: str) -> str:
        for presentation in (
            *self.place_presentations,
            *self.object_presentations,
            *self.actor_presentations,
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

    def autonomous_movement_evidence(
        self,
        *,
        command_id: str,
        actor_entity_id: str,
        source_place_id: str,
        destination_place_id: str,
    ) -> tuple[MovementSpatialEvidence, MovementOpportunityEvidence]:
        if actor_entity_id != GROUNDSKEEPER_ID:
            raise UnavailableFixtureMovementError(
                "WORLD-1 autonomous movement is bounded to Groundskeeper"
            )
        if (source_place_id, destination_place_id) not in {
            (GATEHOUSE_ID, YARD_ID),
            (YARD_ID, GATEHOUSE_ID),
        }:
            raise UnavailableFixtureMovementError(
                "WORLD-1 autonomous movement must use the existing "
                "Yard/Gatehouse route"
            )
        token = hashlib.sha256(command_id.encode("utf-8")).hexdigest()[:20]
        return (
            create_movement_spatial_evidence(
                evidence_id=build_record_id(
                    "evidence", f"world1-spatial-{token}"
                ),
                actor_entity_id=actor_entity_id,
                source_place_id=source_place_id,
                destination_place_id=destination_place_id,
                spatially_permitted=True,
            ),
            create_movement_opportunity_evidence(
                evidence_id=build_record_id(
                    "evidence", f"world1-opportunity-{token}"
                ),
                actor_entity_id=actor_entity_id,
                destination_place_id=destination_place_id,
                opportunity_available=True,
                resolution_accepted=True,
            ),
        )

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
        pickup_observation_evidence: FixtureVisualObservationEvidence | None = None,
    ) -> tuple[CustodyQualificationEvidence, CustodyOpportunityEvidence]:
        """Return bounded RT-010 qualification and AFQR-19 custody opportunity.

        Direct pickup requires the caller to supply the AFQR-20 observation
        candidate for the target. AFQR-19 consumes that evidence reference and
        decides whether the bounded pickup opportunity is currently available.
        Drop remains a custody/control operation and is not visual-gated here.
        R4-E still validates actor/object identity, placement, co-location,
        current carrier, command identity, and transition state.
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

        input_evidence_refs: tuple[str, ...] = ()
        opportunity_available = True
        if operation == "pickup":
            if pickup_observation_evidence is None:
                raise UnavailableFixtureCustodyError(
                    "pickup requires bounded AFQR-20 observation evidence"
                )
            if (
                pickup_observation_evidence.semantic_owner
                != AFQR20_FIXTURE_SENSING_OWNER
                or pickup_observation_evidence.observer_entity_id
                != self.player_entity_id
                or pickup_observation_evidence.target_entity_id
                != object_entity_id
            ):
                raise UnavailableFixtureCustodyError(
                    "pickup observation evidence does not match the bounded target"
                )
            input_evidence_refs = (pickup_observation_evidence.evidence_id,)
            opportunity_available = pickup_observation_evidence.observable

        qualification_token = hashlib.sha256(
            f"{command_id}|{operation}|{object_entity_id}".encode("utf-8")
        ).hexdigest()[:20]
        opportunity_token_material = "|".join((
            command_id,
            operation,
            object_entity_id,
            *input_evidence_refs,
            str(int(opportunity_available)),
        ))
        opportunity_token = hashlib.sha256(
            opportunity_token_material.encode("utf-8")
        ).hexdigest()[:20]

        qualification = create_custody_qualification_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"g2-custody-{operation}-{qualification_token}-rt010",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            qualified=True,
        )
        opportunity = create_custody_opportunity_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"g2-custody-{operation}-{opportunity_token}-afqr19",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            operation=operation,
            opportunity_available=opportunity_available,
            resolution_accepted=True,
            input_evidence_refs=input_evidence_refs,
        )
        return qualification, opportunity

    def object_open_close_evidence(
        self,
        *,
        command_id: str,
        object_entity_id: str,
        operation: str,
        actor_entity_id: str | None = None,
        opportunity_available: bool = True,
    ) -> tuple[
        ObjectOpenCloseQualificationEvidence,
        ObjectOpenCloseOpportunityEvidence,
    ]:
        'Return bounded RT-010/AFQR-19 evidence for INT-1/WORLD-2.'

        if object_entity_id != TOOL_CHEST_ID:
            raise UnavailableFixtureCustodyError(
                "target has no bounded fixture open/close state"
            )
        if operation not in {"open", "close"}:
            raise UnavailableFixtureCustodyError(
                "open/close operation must be open or close"
            )
        bounded_actor_id = (
            self.player_entity_id
            if actor_entity_id is None
            else actor_entity_id
        )
        if bounded_actor_id not in {
            self.player_entity_id,
            GROUNDSKEEPER_ID,
        }:
            raise UnavailableFixtureCustodyError(
                "open/close actor is outside the bounded fixture"
            )
        if type(opportunity_available) is not bool:
            raise UnavailableFixtureCustodyError(
                "opportunity_available must be bool"
            )

        token = hashlib.sha256(
            (
                f"{command_id}|{bounded_actor_id}|{operation}|"
                f"{object_entity_id}|{int(opportunity_available)}"
            ).encode("utf-8")
        ).hexdigest()[:20]
        qualification = create_object_open_close_qualification_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int1-{operation}-{token}-rt010",
            ),
            actor_entity_id=bounded_actor_id,
            object_entity_id=object_entity_id,
            operation=operation,
            qualified=True,
        )
        opportunity = create_object_open_close_opportunity_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int1-{operation}-{token}-afqr19",
            ),
            actor_entity_id=bounded_actor_id,
            object_entity_id=object_entity_id,
            operation=operation,
            opportunity_available=opportunity_available,
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

    def storage_pair_supported(
        self,
        *,
        object_entity_id: str,
        container_entity_id: str,
    ) -> bool:
        return (
            object_entity_id == LANTERN_ID
            and container_entity_id == TOOL_CHEST_ID
        )

    def object_storage_evidence(
        self,
        *,
        command_id: str,
        object_entity_id: str,
        container_entity_id: str,
        operation: str,
    ) -> tuple[
        ObjectStorageQualificationEvidence,
        ObjectStorageOpportunityEvidence,
    ]:
        if not self.storage_pair_supported(
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
        ):
            raise UnavailableFixtureCustodyError(
                "object/container pair has no bounded fixture storage qualification"
            )
        if operation not in {"store", "retrieve"}:
            raise UnavailableFixtureCustodyError(
                "storage operation must be store or retrieve"
            )
        token = hashlib.sha256(
            f"{command_id}|{operation}|{object_entity_id}|{container_entity_id}".encode(
                "utf-8"
            )
        ).hexdigest()[:20]
        qualification = create_object_storage_qualification_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int3-{operation}-{token}-rt010",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            operation=operation,
            qualified=True,
        )
        opportunity = create_object_storage_opportunity_evidence(
            evidence_id=build_record_id(
                "evidence",
                f"int3-{operation}-{token}-afqr19",
            ),
            actor_entity_id=self.player_entity_id,
            object_entity_id=object_entity_id,
            container_entity_id=container_entity_id,
            operation=operation,
            opportunity_available=True,
            resolution_accepted=True,
        )
        return qualification, opportunity

    def public_entities_contained_by(
        self,
        representation: PersistentWorldEntityLocationRepresentation,
        container_entity_id: str,
    ) -> tuple[PublicEntityPresentation, ...]:
        contained_ids = {
            relation.subject_entity_id
            for relation in representation.relations
            if (
                relation.relation_type == CONTAINED_BY_RELATION_TYPE
                and relation.object_entity_id == container_entity_id
            )
        }
        return tuple(
            presentation
            for presentation in self.object_presentations
            if presentation.entity_id in contained_ids
        )

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

    def public_actors_at(
        self,
        representation: PersistentWorldEntityLocationRepresentation,
        place_id: str,
    ) -> tuple[PublicEntityPresentation, ...]:
        actor_ids = {
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
            for presentation in self.actor_presentations
            if presentation.entity_id in actor_ids
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
            _entity(GROUNDSKEEPER_ID, "character_or_creature"),
        ),
        relations=(
            _located("g1-player-workshop", PLAYER_ID, WORKSHOP_ID),
            _located("g1-lantern-workshop", LANTERN_ID, WORKSHOP_ID),
            _located("g1-tool-chest-yard", TOOL_CHEST_ID, YARD_ID),
            _located("g1-waystone-orchard", WAYSTONE_ID, ORCHARD_PATH_ID),
            _located(
                "world1-groundskeeper-gatehouse",
                GROUNDSKEEPER_ID,
                GATEHOUSE_ID,
            ),
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

    initial_int3_world_state_digest = digest_persistent_world_storage_composite_state(
        create_persistent_world_object_lit_runtime_state(
            open_close_state=create_persistent_world_object_open_close_runtime_state(
                custody_state=create_persistent_world_object_custody_runtime_state(
                    movement_state=create_persistent_world_movement_runtime_state(
                        representation=representation
                    )
                ),
                object_open_states=initial_object_open_states,
            ),
            object_lit_states=initial_object_lit_states,
        )
    )
    if initial_int3_world_state_digest != FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST:
        raise MyravantPlayFixtureError(
            "fixture INT-3 authoritative initial state changed without updating "
            "FIXTURE_VERSION and FIXTURE_INT3_INITIAL_WORLD_STATE_DIGEST"
        )

    ambient_visual_conditions = {
        WORKSHOP_ID: "sufficient",
        YARD_ID: "sufficient",
        ORCHARD_PATH_ID: "insufficient",
        GATEHOUSE_ID: "sufficient",
    }
    ambient_visual_condition_digest = digest_fixture_ambient_visual_conditions(
        ambient_visual_conditions
    )
    if (
        ambient_visual_condition_digest
        != FIXTURE_AMBIENT_VISUAL_CONDITION_DIGEST
    ):
        raise MyravantPlayFixtureError(
            "fixture ambient visual conditions changed without updating "
            "FIXTURE_VERSION and FIXTURE_AMBIENT_VISUAL_CONDITION_DIGEST"
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

    actors = (
        PublicEntityPresentation(
            entity_id=GROUNDSKEEPER_ID,
            name="Groundskeeper",
            description=(
                "A quiet groundskeeper tends the bounded test grounds."
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
        initial_int3_world_state_digest=initial_int3_world_state_digest,
        ambient_visual_profile_version=FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION,
        ambient_visual_condition_digest=ambient_visual_condition_digest,
    )

    return MyravantPlayFixture(
        campaign_id=CAMPAIGN_ID,
        player_entity_id=PLAYER_ID,
        initial_state=create_persistent_world_movement_runtime_state(
            representation=representation
        ),
        initial_object_open_states=initial_object_open_states,
        initial_object_lit_states=initial_object_lit_states,
        ambient_visual_conditions=ambient_visual_conditions,
        ambient_visual_profile_version=FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION,
        place_presentations=places,
        object_presentations=objects,
        actor_presentations=actors,
        movement_routes=routes,
        checkpoint_qualification=checkpoint_qualification,
        provenance=provenance,
    )
