from __future__ import annotations

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    WAYSTONE_ID,
)
from astra_runtime.myravant_vsm9_actor_mediated_object_state import execute_vsm9_request


def test_vsm9_actor_mediated_light_flows_into_existing_comp1_visibility_without_transferring_ownership():
    app = MyravantPlayApplication.new()

    # Bring the Lantern and requester into the Yard, then bring the existing
    # WORLD-2 Groundskeeper into the same locality.
    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.wait().authoritative_changed is True
    assert app.current_place_id() == app.entity_place_id(GROUNDSKEEPER_ID)

    # Player-carried custody is deliberately not actor opportunity.  Dropping
    # the Lantern makes the same request legal for the Groundskeeper.
    assert app.drop("lantern").authoritative_changed is True
    mediated = execute_vsm9_request(
        app,
        "ask groundskeeper to light lantern",
    )
    assert mediated.result.authoritative_changed is True
    assert mediated.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    # Lit state is RT-010-owned.  Existing custody/movement carries that state
    # to the player without changing who performed the committed transition.
    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("east").authoritative_changed is True

    evidence = app.visual_observation_evidence(WAYSTONE_ID)
    assert evidence.local_light_available is True
    assert evidence.observable is True
    assert evidence.semantic_owner == "AFQR-20"
    assert "Weathered Waystone" in app.look().view.objects
    assert app.inspect("waystone").result_type == "inspection"

    transition = app.lit_state.committed_object_lit_transitions[-1]
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.object_entity_id == LANTERN_ID
    assert transition.receipt.operation == "light"
