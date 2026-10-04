"""Bounded Orchard Path directional-light repair for the current playable lane.

This module repairs one composition seam exposed by COMP-3 sustained play. It
derives a nonauthoritative AFQR-20 observation signal from already-authoritative
facts: the bounded displacement route, the Brass Lantern's current placement,
and its existing INT-2 lit state. It does not create sensing state, knowledge,
movement reachability, displacement authority, or a new semantic owner.
"""

from __future__ import annotations

import hashlib

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_play_fixture import LANTERN_ID


ORCHARD_PATH_SIGNAL_OWNER = "AFQR-20"


def derive_displaced_lantern_directional_signal(
    application: MyravantPlayApplication,
    *,
    direction: str,
    prior_result: PlayApplicationResult,
) -> PlayApplicationResult | None:
    """Return the bounded remote lantern signal when current truth supports it.

    The ordinary directional-observation path remains first authority for
    presentation. This repair applies only when that path reports an unlicensed
    direction and the exact bounded COMP-3 route currently contains the lit
    Brass Lantern at its destination.
    """

    if (
        prior_result.result_type != "directional_observation_unavailable"
        or prior_result.failure_class != "directional_observation_unlicensed"
    ):
        return None

    normalized = direction.strip().casefold()
    source_place_id = application.current_place_id()
    route = next(
        (
            item
            for item in application.fixture.object_displacement_routes
            if item.object_entity_id == LANTERN_ID
            and item.source_place_id == source_place_id
            and item.direction == normalized
            and item.method == "throw"
        ),
        None,
    )
    if route is None:
        return None

    lantern_state = application.object_lit_state(LANTERN_ID)
    if lantern_state is None or lantern_state.state != "lit":
        return None

    lantern_at_destination = any(
        relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
        and relation.object_entity_id == route.destination_place_id
        for relation in application.state.representation.relations
    )
    if not lantern_at_destination:
        return None

    destination_name = application.fixture.place_presentation(
        route.destination_place_id
    ).name
    lantern_name = application.fixture.entity_name(LANTERN_ID)
    token = hashlib.sha256(
        (
            f"{application.fixture.player_entity_id}|{source_place_id}|"
            f"{normalized}|{route.destination_place_id}|{LANTERN_ID}|lit"
        ).encode("utf-8")
    ).hexdigest()[:20]
    evidence_id = build_record_id(
        "evidence",
        f"comp3-directional-light-{token}",
    )
    digest = application.authoritative_digest()
    return PlayApplicationResult(
        result_type="directional_signal_observation",
        message=(
            f"A steady {lantern_name} glow is visible {normalized} "
            f"along the {destination_name}."
        ),
        authoritative_changed=False,
        observation_evidence_id=evidence_id,
        pre_state_digest=digest,
        post_state_digest=digest,
    )
