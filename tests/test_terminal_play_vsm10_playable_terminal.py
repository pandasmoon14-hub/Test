from __future__ import annotations

from io import StringIO

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm10_terminal import (
    execute_vsm10_terminal_input,
    run_vsm10_terminal,
)


def test_vsm10_terminal_first_refusal_does_not_steal_vsm8_vsm9_or_player_movement():
    app = MyravantPlayApplication.new()

    direct = execute_vsm10_terminal_input(app, "move south")
    assert direct.route == "existing_terminal"
    assert direct.result.result_type == "movement_committed"
    assert app.current_place_id() == YARD_ID

    assert execute_vsm10_terminal_input(app, "wait").result.authoritative_changed

    vsm8 = execute_vsm10_terminal_input(app, "ask groundskeeper to open chest")
    assert vsm8.route == "existing_terminal"
    assert vsm8.result.result_type == "object_state_committed"

    vsm9 = execute_vsm10_terminal_input(app, "ask groundskeeper to light lantern")
    assert vsm9.route == "vsm9_actor_mediated"
    assert vsm9.prior_request_receipt is not None
    assert vsm9.result.authoritative_changed is False

    vsm10 = execute_vsm10_terminal_input(app, "ask groundskeeper to go to gatehouse")
    assert vsm10.route == "vsm10_actor_mediated_movement"
    assert vsm10.request_receipt is not None
    assert vsm10.result.authoritative_changed is True


def test_vsm10_raw_terminal_sustained_play_composes_vsm9_movement_and_restore(tmp_path):
    path = tmp_path / "vsm10-playable.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    output = StringIO()

    interactions = run_vsm10_terminal(
        app,
        input_stream=StringIO(
            "ask groundskeeper to go to yard\n"  # absent -> refusal
            "pickup lantern\n"
            "move south\n"
            "wait\n"  # Groundskeeper enters Yard
            "ask groundskeeper to move north\n"  # resolves Workshop -> bounded reject
            "ask groundskeeper to go to yard\n"  # already there -> no change
            "drop lantern\n"
            "ask groundskeeper to light lantern\n"  # VSM-9 commit
            "ask groundskeeper to go to gatehouse\n"  # VSM-10 commit
            "look\n"
            "move south\n"
            "ask groundskeeper to move north\n"  # VSM-10 return to Yard
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )

    mediated = [
        item
        for item in interactions
        if item.route == "vsm10_actor_mediated_movement"
    ]
    assert len(mediated) == 5
    assert [item.request_receipt.acceptance for item in mediated] == [
        "refused",
        "accepted",
        "accepted",
        "accepted",
        "accepted",
    ]
    assert [item.request_receipt.legality_result for item in mediated] == [
        "not_evaluated",
        "rejected",
        "allowed_no_change",
        "allowed",
        "allowed",
    ]
    assert [item.result.authoritative_changed for item in mediated] == [
        False,
        False,
        False,
        True,
        True,
    ]

    vsm9 = [item for item in interactions if item.route == "vsm9_actor_mediated"]
    assert len(vsm9) == 1
    assert vsm9[0].prior_request_receipt is not None
    assert vsm9[0].result.authoritative_changed is True
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    text = output.getvalue()
    assert "The Groundskeeper is not here to receive that request." in text
    assert "outside the bounded movement route" in text
    assert "The Groundskeeper is already at the Yard." in text
    assert "The Groundskeeper lights the Brass Lantern." in text
    assert "The Groundskeeper moves to the Gatehouse." in text
    assert "The Groundskeeper moves to the Yard." in text

    final_digest = app.authoritative_digest()
    assert app.current_place_id() == GATEHOUSE_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == final_digest
    assert restored.current_place_id() == GATEHOUSE_ID
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"

    groundskeeper_movements = [
        transition
        for transition in restored.state.committed_transitions
        if transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    ]
    assert len(groundskeeper_movements) >= 3  # WORLD-2 arrival + two VSM-10 moves
    assert any(
        transition.receipt.command_id.startswith("world2-npc-move-")
        for transition in groundskeeper_movements
    )
    assert any(
        transition.receipt.source_place_id == YARD_ID
        and transition.receipt.destination_place_id == GATEHOUSE_ID
        for transition in groundskeeper_movements
    )
    assert any(
        transition.receipt.source_place_id == GATEHOUSE_ID
        and transition.receipt.destination_place_id == YARD_ID
        for transition in groundskeeper_movements
    )


def test_vsm10_direct_player_and_actor_movement_keep_attribution_distinct():
    app = MyravantPlayApplication.new()
    player_move = execute_vsm10_terminal_input(app, "move south")
    assert player_move.result.authoritative_changed is True
    assert app.state.committed_transitions[-1].receipt.actor_entity_id == PLAYER_ID

    assert execute_vsm10_terminal_input(app, "wait").result.authoritative_changed
    actor_move = execute_vsm10_terminal_input(
        app,
        "ask groundskeeper to go to gatehouse",
    )
    assert actor_move.result.authoritative_changed is True
    assert app.state.committed_transitions[-1].receipt.actor_entity_id == GROUNDSKEEPER_ID
