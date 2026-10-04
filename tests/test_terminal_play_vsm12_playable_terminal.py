from __future__ import annotations

from io import StringIO

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    LANTERN_ID,
)
from astra_runtime.myravant_vsm12_terminal import (
    execute_vsm12_terminal_input,
    run_vsm12_terminal,
)


def test_vsm12_first_refusal_preserves_vsm11_and_earlier_routes():
    app = MyravantPlayApplication.new()

    storage = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to store lantern in chest",
    )
    assert storage.route == "vsm11_actor_mediated_storage"

    move = execute_vsm12_terminal_input(app, "move south")
    assert move.route == "existing_terminal"
    assert move.result.authoritative_changed
    assert execute_vsm12_terminal_input(app, "wait").result.authoritative_changed

    lit = execute_vsm12_terminal_input(app, "ask groundskeeper to light lantern")
    assert lit.route == "vsm9_actor_mediated"

    actor_move = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to go to gatehouse",
    )
    assert actor_move.route == "vsm10_actor_mediated_movement"


def test_vsm12_raw_sustained_play_covers_full_request_and_owner_chain(tmp_path):
    checkpoint = tmp_path / "vsm12-playable.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    output = StringIO()

    interactions = run_vsm12_terminal(
        app,
        input_stream=StringIO(
            "ask groundskeeper to pick up lantern\n"
            "move south\n"
            "wait\n"
            "ask groundskeeper to pick up lantern\n"
            "move north\n"
            "pickup lantern\n"
            "move south\n"
            "drop lantern\n"
            "ask groundskeeper to pick up lantern\n"
            "wait\n"
            "ask groundskeeper to store lantern in chest\n"
            "ask groundskeeper to retrieve lantern from chest\n"
            "ask groundskeeper to light lantern\n"
            "ask groundskeeper to go to gatehouse\n"
            "move south\n"
            "look\n"
            "ask groundskeeper to drop lantern\n"
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )

    custody = [item for item in interactions if item.route == "vsm12_actor_mediated_custody"]
    assert len(custody) == 4
    assert [item.request_receipt.acceptance for item in custody] == [
        "refused",
        "accepted",
        "accepted",
        "accepted",
    ]
    assert [item.request_receipt.legality_result for item in custody] == [
        "not_evaluated",
        "rejected",
        "allowed",
        "allowed",
    ]
    assert [item.result.authoritative_changed for item in custody] == [
        False,
        False,
        True,
        True,
    ]

    storage = [item for item in interactions if item.route == "vsm11_actor_mediated_storage"]
    assert len(storage) == 2
    assert all(item.result.authoritative_changed for item in storage)
    assert any(item.route == "vsm9_actor_mediated" for item in interactions)
    assert any(item.route == "vsm10_actor_mediated_movement" for item in interactions)

    visible = output.getvalue()
    assert "The Groundskeeper is not here to receive that request." in visible
    assert (
        "The Groundskeeper accepts, but cannot perform that custody action "
        "from the current state."
    ) in visible
    assert "The Groundskeeper picks up the Brass Lantern." in visible
    assert "The Groundskeeper drops the Brass Lantern." in visible

    final_digest = app.authoritative_digest()
    assert app.current_place_id() == GATEHOUSE_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == final_digest
    assert restored.current_place_id() == GATEHOUSE_ID
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    placements = [
        relation.object_entity_id
        for relation in restored.state.representation.relations
        if relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert placements == [GATEHOUSE_ID]


def test_vsm12_repeated_fresh_runs_are_deterministic():
    snapshots = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        assert app.pickup("lantern").authoritative_changed
        assert app.move("south").authoritative_changed
        assert app.drop("lantern").authoritative_changed
        assert app.wait().authoritative_changed

        interaction = execute_vsm12_terminal_input(
            app,
            "ask groundskeeper to pick up lantern",
        )
        transition = app.custody_state.committed_custody_transitions[-1]
        snapshots.append(
            (
                interaction.request_receipt,
                interaction.result.command_fingerprint,
                interaction.result.receipt_id,
                interaction.result.state_delta_id,
                transition.receipt.to_dict(),
                app.authoritative_digest(),
            )
        )

    assert snapshots[0] == snapshots[1]
