from __future__ import annotations

from io import StringIO

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    TOOL_CHEST_ID,
)
from astra_runtime.myravant_vsm9_terminal import (
    execute_vsm9_terminal_input,
    run_vsm9_terminal,
)


def test_vsm9_terminal_first_refusal_is_only_for_exact_bounded_request():
    app = MyravantPlayApplication.new()

    ordinary = execute_vsm9_terminal_input(app, "light lantern")
    assert ordinary.route == "existing_terminal"
    assert ordinary.result.result_type == "object_lit_state_committed"
    assert app.lit_state.committed_object_lit_transitions[-1].receipt.actor_entity_id == PLAYER_ID

    out_of_scope = execute_vsm9_terminal_input(
        app, "ask groundskeeper to activate lantern"
    )
    assert out_of_scope.route == "existing_terminal"
    assert out_of_scope.result.result_type == "unsupported_input"
    assert out_of_scope.result.authoritative_changed is False


def test_vsm9_terminal_preserves_vsm8_and_vsm7_routes_unchanged():
    app = MyravantPlayApplication.new()
    assert execute_vsm9_terminal_input(app, "pickup lantern").result.authoritative_changed
    assert execute_vsm9_terminal_input(app, "move south").result.authoritative_changed
    assert execute_vsm9_terminal_input(app, "wait").result.authoritative_changed

    vsm8 = execute_vsm9_terminal_input(app, "ask groundskeeper to open chest")
    assert vsm8.route == "existing_terminal"
    assert vsm8.result.result_type == "object_state_committed"
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"

    vsm6 = execute_vsm9_terminal_input(app, "give lantern to groundskeeper")
    assert vsm6.route == "existing_terminal"
    assert vsm6.result.authoritative_changed is True

    vsm7 = execute_vsm9_terminal_input(app, "ask groundskeeper for lantern")
    assert vsm7.route == "existing_terminal"
    assert vsm7.result.authoritative_changed is True


def test_vsm9_raw_terminal_session_proves_request_acceptance_legality_commit_and_rejection(tmp_path):
    path = tmp_path / "vsm9-playable.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    output = StringIO()

    interactions = run_vsm9_terminal(
        app,
        input_stream=StringIO(
            "ask groundskeeper to light lantern\n"  # actor absent -> refusal
            "pickup lantern\n"
            "move south\n"
            "wait\n"  # Groundskeeper enters Yard
            "ask groundskeeper to light lantern\n"  # player carries -> legality reject
            "drop lantern\n"
            "ask groundskeeper to light lantern\n"  # nearby -> commit
            "ask groundskeeper to light lantern\n"  # redundant -> no change
            "save\n"
            "exit\n"
        ),
        output_stream=output,
    )

    mediated = [item for item in interactions if item.route == "vsm9_actor_mediated"]
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
        "allowed_no_change",
    ]
    assert [item.result.authoritative_changed for item in mediated] == [
        False,
        False,
        True,
        False,
    ]
    assert mediated[2].request_receipt.requester_entity_id == PLAYER_ID
    assert mediated[2].request_receipt.requested_actor_entity_id == GROUNDSKEEPER_ID
    assert mediated[2].request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert mediated[2].request_receipt.target_entity_id == LANTERN_ID
    assert mediated[2].request_receipt.authoritative_receipt_id is not None

    text = output.getvalue()
    assert "The Groundskeeper is not here to receive that request." in text
    assert "The Groundskeeper accepts, but cannot currently reach the Brass Lantern." in text
    assert "The Groundskeeper lights the Brass Lantern." in text
    assert "The Brass Lantern is already lit." in text

    final_digest = app.authoritative_digest()
    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == final_digest
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    transition = restored.lit_state.committed_object_lit_transitions[-1]
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.object_entity_id == LANTERN_ID
    assert transition.receipt.operation == "light"
