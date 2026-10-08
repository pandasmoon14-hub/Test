from __future__ import annotations

from astra_runtime.domain.persistent_world_follow_intent import active_follow_intent_for
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    ORCHARD_PATH_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import execute_vsm14_follow_request
from astra_runtime.myravant_vsm14_terminal import execute_vsm14_terminal_input


def _meet_groundskeeper(app: MyravantVSM14Application) -> None:
    assert app.move("south").result_type == "movement_committed"
    assert app.move("south").result_type == "movement_committed"
    assert app.entity_place_id(PLAYER_ID) == app.entity_place_id(GROUNDSKEEPER_ID)


def test_follow_request_requires_local_actor_and_preserves_state_on_refusal() -> None:
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    execution = execute_vsm14_follow_request(
        app, "ask groundskeeper to follow me"
    )
    assert execution.result.result_type == "follow_intent_request_rejected"
    assert execution.result.failure_class == "vsm14_requested_actor_not_local"
    assert execution.result.authoritative_changed is False
    assert app.authoritative_digest() == before
    assert app.follow_intent_state.active_intents == ()


def test_active_follow_intent_drives_separate_existing_r4c_movements() -> None:
    app = MyravantVSM14Application.new()
    _meet_groundskeeper(app)

    activation = execute_vsm14_follow_request(
        app, "ask the groundskeeper to follow me"
    )
    assert activation.result.result_type == "follow_intent_committed"
    assert activation.result.authoritative_changed is True
    active = active_follow_intent_for(app.follow_intent_state, GROUNDSKEEPER_ID)
    assert active is not None
    assert active.leader_entity_id == PLAYER_ID

    movement_count = len(app.state.committed_transitions)
    north = app.move("north")
    assert north.result_type == "movement_committed"
    assert north.world_event_class == "behavioral_intent_consequence"
    assert north.world_process_actor_id == GROUNDSKEEPER_ID
    assert north.world_process_action == "follow_move"
    assert north.world_process_outcome == "committed"
    assert north.consequence_receipt_id is not None
    assert len(app.state.committed_transitions) == movement_count + 2
    assert app.entity_place_id(PLAYER_ID) == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID

    east = app.move("east")
    assert east.world_process_outcome == "committed"
    assert app.entity_place_id(PLAYER_ID) == ORCHARD_PATH_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == ORCHARD_PATH_ID

    follow_moves = [
        transition
        for transition in app.state.committed_transitions
        if transition.command_id.startswith("vsm14-follow-move-")
    ]
    assert len(follow_moves) == 2
    assert all(
        transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
        for transition in follow_moves
    )
    assert all(
        transition.receipt.actor_entity_id != PLAYER_ID
        for transition in follow_moves
    )


def test_cancel_follow_stops_future_consequence_without_rewriting_past_movement() -> None:
    app = MyravantVSM14Application.new()
    _meet_groundskeeper(app)
    assert execute_vsm14_follow_request(
        app, "ask groundskeeper to follow me"
    ).result.authoritative_changed
    assert app.move("north").world_process_outcome == "committed"
    assert app.move("east").world_process_outcome == "committed"

    before_cancel_movement = tuple(app.state.committed_transitions)
    cancellation = execute_vsm14_follow_request(
        app, "ask groundskeeper to stop following me"
    )
    assert cancellation.result.result_type == "follow_intent_committed"
    assert app.follow_intent_state.active_intents == ()

    west = app.move("west")
    assert west.result_type == "movement_committed"
    assert west.world_event_class is None
    assert app.entity_place_id(PLAYER_ID) == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == ORCHARD_PATH_ID
    after_cancel_movement = {
        transition.command_id: transition
        for transition in app.state.committed_transitions
    }
    assert all(
        after_cancel_movement[transition.command_id] == transition
        for transition in before_cancel_movement
    )


def test_redundant_follow_requests_are_nonmutating() -> None:
    app = MyravantVSM14Application.new()
    _meet_groundskeeper(app)
    first = execute_vsm14_follow_request(app, "ask groundskeeper to follow me")
    assert first.result.authoritative_changed is True
    digest = app.authoritative_digest()
    repeated = execute_vsm14_follow_request(app, "ask groundskeeper to follow me")
    assert repeated.result.result_type == "follow_intent_unchanged"
    assert repeated.result.authoritative_changed is False
    assert app.authoritative_digest() == digest

    assert execute_vsm14_follow_request(
        app, "ask groundskeeper to stop following me"
    ).result.authoritative_changed
    digest = app.authoritative_digest()
    repeated_stop = execute_vsm14_follow_request(
        app, "ask groundskeeper to stop following me"
    )
    assert repeated_stop.result.result_type == "follow_intent_unchanged"
    assert app.authoritative_digest() == digest


def test_vsm14_first_refusal_does_not_swallow_vsm10_immediate_movement() -> None:
    app = MyravantVSM14Application.new()
    _meet_groundskeeper(app)
    interaction = execute_vsm14_terminal_input(
        app, "ask groundskeeper to go to the yard"
    )
    assert interaction.route != "vsm14_persistent_follow_intent"
    assert interaction.result.result_type == "actor_mediated_movement_committed"
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert app.follow_intent_state.active_intents == ()


def test_repeated_fresh_follow_runs_are_deterministic() -> None:
    snapshots = []
    for _ in range(2):
        app = MyravantVSM14Application.new()
        _meet_groundskeeper(app)
        activation = execute_vsm14_follow_request(
            app, "ask groundskeeper to follow me"
        )
        move = app.move("north")
        snapshots.append(
            (
                activation.request_receipt,
                move.command_id,
                move.command_fingerprint,
                move.consequence_receipt_id,
                move.consequence_state_delta_id,
                app.follow_intent_state,
                app.state,
                app.authoritative_digest(),
            )
        )
    assert snapshots[0] == snapshots[1]
