from __future__ import annotations

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_follow_intent import active_follow_intent_for
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    ORCHARD_PATH_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import execute_vsm14_follow_request


def _meet_groundskeeper(app: MyravantVSM14Application) -> None:
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.entity_place_id(PLAYER_ID) == app.entity_place_id(GROUNDSKEEPER_ID)


def test_follow_composes_with_carried_lit_object_without_absorbing_custody_or_lit_state() -> None:
    app = MyravantVSM14Application.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    _meet_groundskeeper(app)
    assert app.give_object("lantern", "groundskeeper").authoritative_changed
    assert execute_vsm14_follow_request(
        app, "ask groundskeeper to follow me"
    ).result.authoritative_changed

    assert app.move("north").world_process_outcome == "committed"
    assert app.move("east").world_process_outcome == "committed"
    assert app.entity_place_id(GROUNDSKEEPER_ID) == ORCHARD_PATH_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    assert any(
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
        and relation.object_entity_id == GROUNDSKEEPER_ID
        for relation in app.state.representation.relations
    )

    view = app.look().view
    assert view is not None
    assert "Groundskeeper" in view.actors
    assert any(
        fact.entity_id == LANTERN_ID
        and fact.lit_state == "lit"
        and fact.carrier_name == "Groundskeeper"
        for fact in view.observation_facts
    )


def test_world2_can_move_follower_independently_without_cancelling_follow_intent() -> None:
    app = MyravantVSM14Application.new()
    _meet_groundskeeper(app)
    assert execute_vsm14_follow_request(
        app, "ask groundskeeper to follow me"
    ).result.authoritative_changed

    active_before = active_follow_intent_for(
        app.follow_intent_state, GROUNDSKEEPER_ID
    )
    assert active_before is not None

    world = app.wait()
    assert world.result_type == "world_advanced"
    assert world.world_process_actor_id == GROUNDSKEEPER_ID
    assert world.world_process_action == "move"
    assert world.world_process_outcome == "committed"
    assert app.entity_place_id(PLAYER_ID) != app.entity_place_id(GROUNDSKEEPER_ID)
    assert active_follow_intent_for(
        app.follow_intent_state, GROUNDSKEEPER_ID
    ) == active_before

    rejoin = app.move("north")
    assert rejoin.result_type == "movement_committed"
    assert rejoin.world_event_class is None
    assert app.entity_place_id(PLAYER_ID) == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID

    resumed = app.move("east")
    assert resumed.world_event_class == "behavioral_intent_consequence"
    assert resumed.world_process_outcome == "committed"
    assert app.entity_place_id(PLAYER_ID) == ORCHARD_PATH_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == ORCHARD_PATH_ID
