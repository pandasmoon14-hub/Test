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
from astra_runtime.myravant_vsm11_terminal import (
    execute_vsm11_terminal_input,
    run_vsm11_terminal,
)


def test_vsm11_terminal_first_refusal_preserves_prior_vsm_routes():
    app = MyravantPlayApplication.new()

    direct = execute_vsm11_terminal_input(app, "move south")
    assert direct.route == "existing_terminal"
    assert direct.result.authoritative_changed is True

    assert execute_vsm11_terminal_input(app, "wait").result.authoritative_changed

    vsm9 = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to light lantern",
    )
    assert vsm9.route == "vsm9_actor_mediated"
    assert vsm9.result.authoritative_changed is False

    vsm10 = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to go to gatehouse",
    )
    assert vsm10.route == "vsm10_actor_mediated_movement"
    assert vsm10.result.authoritative_changed is True


def test_vsm11_raw_terminal_sustained_play_covers_refusal_rejection_commit_and_restore(
    tmp_path,
):
    checkpoint = tmp_path / "vsm11-playable.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    output = StringIO()

    interactions = run_vsm11_terminal(
        app,
        input_stream=StringIO(
            "ask groundskeeper to pick up lantern\n"  # actor absent -> refusal
            "move south\n"
            "wait\n"  # Groundskeeper enters Yard; Lantern remains Workshop
            "ask groundskeeper to pick up lantern\n"  # accepted, custody illegal
            "move north\n"
            "pickup lantern\n"
            "move south\n"
            "drop lantern\n"
            "ask groundskeeper to pick up lantern\n"  # VSM-11 commit
            "ask groundskeeper to light lantern\n"  # VSM-9 commit while actor carries
            "ask groundskeeper to go to gatehouse\n"  # VSM-10 commit
            "move south\n"
            "look\n"
            "ask groundskeeper to drop lantern\n"  # VSM-11 commit at Gatehouse
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )

    mediated = [
        item
        for item in interactions
        if item.route == "vsm11_actor_mediated_custody"
    ]
    assert len(mediated) == 4
    assert [item.request_receipt.acceptance for item in mediated] == [
        "refused",
        "accepted",
        "accepted",
        "accepted",
    ]
    assert [item.request_receipt.legality_result for item in mediated] == [
        "not_evaluated",
        "rejected",
        "allowed",
        "allowed",
    ]
    assert [item.result.authoritative_changed for item in mediated] == [
        False,
        False,
        True,
        True,
    ]

    assert any(item.route == "vsm9_actor_mediated" for item in interactions)
    assert any(
        item.route == "vsm10_actor_mediated_movement"
        for item in interactions
    )

    visible = output.getvalue()
    assert "The Groundskeeper is not here to receive that request." in visible
    assert (
        "The Groundskeeper accepts, but cannot perform that custody action "
        "from the current state."
    ) in visible
    assert "The Groundskeeper picks up the Brass Lantern." in visible
    assert "The Groundskeeper lights the Brass Lantern." in visible
    assert "The Groundskeeper moves to the Gatehouse." in visible
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

    actor_custody = [
        transition.receipt
        for transition in restored.custody_state.committed_custody_transitions
        if transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    ]
    assert [receipt.operation for receipt in actor_custody] == ["pickup", "drop"]


def test_vsm11_repeated_fresh_runs_produce_same_actor_custody_evidence():
    snapshots = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        assert app.pickup("lantern").authoritative_changed
        assert app.move("south").authoritative_changed
        assert app.drop("lantern").authoritative_changed
        assert app.wait().authoritative_changed

        interaction = execute_vsm11_terminal_input(
            app,
            "ask groundskeeper to pick up lantern",
        )
        receipt = interaction.request_receipt
        transition = app.custody_state.committed_custody_transitions[-1]
        snapshots.append(
            (
                receipt,
                interaction.result.command_fingerprint,
                interaction.result.receipt_id,
                interaction.result.state_delta_id,
                transition.receipt.to_dict(),
                app.authoritative_digest(),
            )
        )

    assert snapshots[0] == snapshots[1]
