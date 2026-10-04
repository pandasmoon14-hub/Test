from __future__ import annotations

from io import StringIO

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    CONTAINED_BY_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm11_terminal import (
    execute_vsm11_terminal_input,
    run_vsm11_terminal,
)


def _carrier(app: MyravantPlayApplication) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def _container(app: MyravantPlayApplication) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == CONTAINED_BY_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def test_vsm11_terminal_first_refusal_preserves_vsm8_vsm9_vsm10_and_existing_terminal():
    app = MyravantPlayApplication.new()

    direct = execute_vsm11_terminal_input(app, "move south")
    assert direct.route == "existing_terminal"
    assert direct.result.authoritative_changed is True

    assert execute_vsm11_terminal_input(app, "wait").result.authoritative_changed

    vsm8 = execute_vsm11_terminal_input(app, "ask groundskeeper to open chest")
    assert vsm8.route == "existing_terminal"
    assert vsm8.result.result_type == "object_state_committed"

    vsm9 = execute_vsm11_terminal_input(app, "ask groundskeeper to light lantern")
    assert vsm9.route == "vsm9_actor_mediated"

    vsm10 = execute_vsm11_terminal_input(app, "ask groundskeeper to go to gatehouse")
    assert vsm10.route == "vsm10_actor_mediated_movement"
    assert vsm10.result.authoritative_changed is True

    assert app.move("south").authoritative_changed is True
    vsm11 = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to retrieve lantern from chest",
    )
    assert vsm11.route == "vsm11_actor_mediated_storage"
    assert vsm11.request_receipt is not None


def test_vsm11_raw_terminal_sustained_play_composes_handoff_object_state_storage_and_restore(
    tmp_path,
):
    path = tmp_path / "vsm11-playable.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    output = StringIO()

    interactions = run_vsm11_terminal(
        app,
        input_stream=StringIO(
            "ask groundskeeper to put lantern in chest\n"  # absent -> refusal
            "pickup lantern\n"
            "light lantern\n"
            "move south\n"
            "wait\n"  # Groundskeeper arrives in Yard
            "ask groundskeeper to put lantern in chest\n"  # player carries -> reject
            "give lantern to groundskeeper\n"
            "ask groundskeeper to put lantern in chest\n"  # chest closed -> reject
            "ask groundskeeper to open chest\n"
            "ask groundskeeper to put lantern in chest\n"  # store commit
            "ask groundskeeper to store lantern in chest\n"  # no change
            "ask groundskeeper to retrieve lantern from chest\n"  # retrieve commit
            "ask groundskeeper to get lantern from chest\n"  # no change
            "ask groundskeeper for lantern\n"  # VSM-7 return to player
            "put lantern in chest\n"  # direct-player INT-3
            "ask groundskeeper to retrieve lantern from chest\n"  # VSM-11 retrieve
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )

    mediated = [
        item
        for item in interactions
        if item.route == "vsm11_actor_mediated_storage"
    ]
    assert len(mediated) == 8
    assert [item.request_receipt.acceptance for item in mediated] == [
        "refused",
        "accepted",
        "accepted",
        "accepted",
        "accepted",
        "accepted",
        "accepted",
        "accepted",
    ]
    assert [item.request_receipt.legality_result for item in mediated] == [
        "not_evaluated",
        "rejected",
        "rejected",
        "allowed",
        "allowed_no_change",
        "allowed",
        "allowed_no_change",
        "allowed",
    ]
    assert [item.result.authoritative_changed for item in mediated] == [
        False,
        False,
        False,
        True,
        False,
        True,
        False,
        True,
    ]

    text = output.getvalue()
    assert "The Groundskeeper is not here to receive that request." in text
    assert text.count(
        "The Groundskeeper accepts, but cannot currently complete that storage transfer."
    ) == 2
    assert "The Groundskeeper stores the Brass Lantern in the Tool Chest." in text
    assert "The Brass Lantern is already in the Tool Chest." in text
    assert "The Groundskeeper retrieves the Brass Lantern from the Tool Chest." in text
    assert "The Groundskeeper already has the Brass Lantern." in text
    assert "The Groundskeeper hands you the Brass Lantern." in text

    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert _container(app) is None
    assert _carrier(app) == GROUNDSKEEPER_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    storage_actors = [
        transition.receipt.actor_entity_id
        for transition in app.storage_state.committed_storage_transitions
    ]
    assert storage_actors.count(GROUNDSKEEPER_ID) == 3
    assert storage_actors.count(PLAYER_ID) == 1

    final_digest = app.authoritative_digest()
    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == final_digest
    assert restored.current_place_id() == YARD_ID
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert _container(restored) is None
    assert _carrier(restored) == GROUNDSKEEPER_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"

    restored_storage_actors = [
        transition.receipt.actor_entity_id
        for transition in restored.storage_state.committed_storage_transitions
    ]
    assert restored_storage_actors == storage_actors
    assert restored_storage_actors.count(GROUNDSKEEPER_ID) == 3
    assert restored_storage_actors.count(PLAYER_ID) == 1


def test_vsm11_direct_player_and_requested_actor_storage_attribution_remain_distinct():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.open_object("chest").authoritative_changed is True

    player_store = execute_vsm11_terminal_input(app, "put lantern in chest")
    assert player_store.result.authoritative_changed is True
    player_receipt_id = player_store.result.receipt_id
    player_transition = next(
        item
        for item in app.storage_state.committed_storage_transitions
        if item.receipt.receipt_id == player_receipt_id
    )
    assert player_transition.receipt.actor_entity_id == PLAYER_ID

    assert execute_vsm11_terminal_input(app, "wait").result.authoritative_changed
    npc_retrieve = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to retrieve lantern from chest",
    )
    assert npc_retrieve.result.authoritative_changed is True
    npc_transition = next(
        item
        for item in app.storage_state.committed_storage_transitions
        if item.receipt.receipt_id == npc_retrieve.result.receipt_id
    )
    assert npc_transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
