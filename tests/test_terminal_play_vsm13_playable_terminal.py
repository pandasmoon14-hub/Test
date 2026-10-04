from __future__ import annotations

from io import StringIO

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    ORCHARD_PATH_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm13_terminal import (
    execute_vsm13_terminal_input,
    run_vsm13_terminal,
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


def _direct_place(app: MyravantPlayApplication) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def test_vsm13_first_refusal_preserves_vsm12_and_earlier_routes():
    app = MyravantPlayApplication.new()

    prior = execute_vsm13_terminal_input(
        app,
        "ask groundskeeper to drop lantern",
    )
    assert prior.route == "vsm12_actor_mediated_custody"

    movement = execute_vsm13_terminal_input(app, "move south")
    assert movement.route == "existing_terminal"
    assert movement.result.authoritative_changed

    storage = execute_vsm13_terminal_input(
        app,
        "ask groundskeeper to store lantern in chest",
    )
    assert storage.route == "vsm11_actor_mediated_storage"

    actor_move = execute_vsm13_terminal_input(
        app,
        "ask groundskeeper to go to gatehouse",
    )
    assert actor_move.route == "vsm10_actor_mediated_movement"


def test_vsm13_raw_sustained_play_composes_request_handoff_comp3_signal_and_restore(
    tmp_path,
):
    checkpoint = tmp_path / "vsm13-playable.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    output = StringIO()

    interactions = run_vsm13_terminal(
        app,
        input_stream=StringIO(
            "ask groundskeeper to throw lantern east\n"  # absent -> refusal
            "pickup lantern\n"
            "light lantern\n"
            "move south\n"
            "wait\n"  # Groundskeeper arrives in Yard
            "ask groundskeeper to throw lantern east\n"  # player carries -> reject
            "give lantern to groundskeeper\n"
            "ask groundskeeper to throw lantern east\n"  # COMP-3 commit
            "look east\n"  # Orchard light signal remains derived
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )

    mediated = [
        item
        for item in interactions
        if item.route == "vsm13_actor_mediated_displacement"
    ]
    assert len(mediated) == 3
    assert [item.request_receipt.acceptance for item in mediated] == [
        "refused",
        "accepted",
        "accepted",
    ]
    assert [item.request_receipt.legality_result for item in mediated] == [
        "not_evaluated",
        "rejected",
        "allowed",
    ]
    assert [item.result.authoritative_changed for item in mediated] == [
        False,
        False,
        True,
    ]
    assert mediated[-1].request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert mediated[-1].request_receipt.destination_place_id == ORCHARD_PATH_ID

    signal = next(
        item
        for item in interactions
        if item.result.result_type == "directional_light_signal"
    )
    assert signal.route == "existing_terminal"
    assert signal.result.authoritative_changed is False

    text = output.getvalue()
    assert "The Groundskeeper is not here to receive that request." in text
    assert (
        "The Groundskeeper accepts, but cannot throw the Brass Lantern "
        "from the current state."
    ) in text
    assert "The Groundskeeper throws the Brass Lantern east." in text
    assert "You can see the Brass Lantern's light to the east." in text

    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert _carrier(app) is None
    assert _direct_place(app) == ORCHARD_PATH_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    displacement = app.runtime_state.committed_object_displacement_transitions
    assert len(displacement) == 1
    assert displacement[0].receipt.actor_entity_id == GROUNDSKEEPER_ID

    final_digest = app.authoritative_digest()
    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == final_digest
    assert restored.current_place_id() == YARD_ID
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert _carrier(restored) is None
    assert _direct_place(restored) == ORCHARD_PATH_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"

    restored_displacement = (
        restored.runtime_state.committed_object_displacement_transitions
    )
    assert len(restored_displacement) == 1
    assert restored_displacement[0].receipt.to_dict() == displacement[0].receipt.to_dict()
    assert restored_displacement[0].receipt.actor_entity_id == GROUNDSKEEPER_ID


def test_vsm13_direct_player_throw_still_routes_to_existing_terminal():
    app = MyravantPlayApplication.new()
    assert execute_vsm13_terminal_input(app, "pickup lantern").result.authoritative_changed
    assert execute_vsm13_terminal_input(app, "move south").result.authoritative_changed

    interaction = execute_vsm13_terminal_input(app, "throw lantern east")
    assert interaction.route == "existing_terminal"
    assert interaction.result.result_type == "object_displacement_committed"
    assert interaction.result.authoritative_changed is True
