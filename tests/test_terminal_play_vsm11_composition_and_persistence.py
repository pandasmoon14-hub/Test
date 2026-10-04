from __future__ import annotations

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm11_terminal import execute_vsm11_terminal_input


def _relation_target(
    app: MyravantPlayApplication,
    relation_type: str,
) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == relation_type
        and relation.subject_entity_id == LANTERN_ID
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def test_vsm11_composes_with_vsm9_vsm10_visibility_and_restore(tmp_path):
    checkpoint = tmp_path / "vsm11-composition.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.drop("lantern").authoritative_changed is True
    assert app.wait().authoritative_changed is True
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID

    pickup = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to pick up lantern",
    )
    assert pickup.route == "vsm11_actor_mediated_custody"
    assert pickup.result.authoritative_changed is True
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) == GROUNDSKEEPER_ID

    light = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to light lantern",
    )
    assert light.route == "vsm9_actor_mediated"
    assert light.result.authoritative_changed is True
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    move_actor = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to go to gatehouse",
    )
    assert move_actor.route == "vsm10_actor_mediated_movement"
    assert move_actor.result.authoritative_changed is True
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) == GROUNDSKEEPER_ID

    player_move = execute_vsm11_terminal_input(app, "move south")
    assert player_move.route == "existing_terminal"
    assert player_move.result.authoritative_changed is True
    assert app.current_place_id() == GATEHOUSE_ID

    view = execute_vsm11_terminal_input(app, "look").result.view
    assert view is not None
    lantern_fact = next(
        fact for fact in view.observation_facts if fact.entity_id == LANTERN_ID
    )
    assert lantern_fact.carrier_name == "Groundskeeper"
    assert lantern_fact.lit_state == "lit"

    drop = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to drop lantern",
    )
    assert drop.route == "vsm11_actor_mediated_custody"
    assert drop.result.authoritative_changed is True
    assert _relation_target(app, LOCATED_AT_RELATION_TYPE) == GATEHOUSE_ID
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) is None

    save = execute_vsm11_terminal_input(app, "save")
    assert save.result.result_type == "checkpoint_written"
    final_digest = app.authoritative_digest()

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == final_digest
    assert restored.current_place_id() == GATEHOUSE_ID
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    assert _relation_target(restored, LOCATED_AT_RELATION_TYPE) == GATEHOUSE_ID

    actor_custody = [
        transition
        for transition in restored.custody_state.committed_custody_transitions
        if transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    ]
    assert [transition.receipt.operation for transition in actor_custody] == [
        "pickup",
        "drop",
    ]

    direct = execute_vsm11_terminal_input(restored, "pickup lantern")
    assert direct.route == "existing_terminal"
    assert direct.result.authoritative_changed is True
    assert restored.custody_state.committed_custody_transitions[-1].receipt.actor_entity_id == PLAYER_ID


def test_vsm11_actor_custody_survives_world2_interleave_without_owner_transfer():
    app = MyravantPlayApplication.new()

    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.drop("lantern").authoritative_changed is True
    assert app.wait().authoritative_changed is True

    pickup = execute_vsm11_terminal_input(
        app,
        "ask groundskeeper to pick up lantern",
    )
    assert pickup.result.authoritative_changed is True
    custody_receipt_id = pickup.result.receipt_id

    # WORLD-2 advances and can move the actor; the existing carried_by relation
    # follows the actor semantically without rewriting the custody receipt.
    world = execute_vsm11_terminal_input(app, "wait")
    assert world.result.result_type == "world_advanced"
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) == GROUNDSKEEPER_ID

    matching = [
        transition
        for transition in app.custody_state.committed_custody_transitions
        if transition.receipt.receipt_id == custody_receipt_id
    ]
    assert len(matching) == 1
    assert matching[0].receipt.actor_entity_id == GROUNDSKEEPER_ID
