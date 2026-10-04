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
    TOOL_CHEST_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm12_terminal import execute_vsm12_terminal_input


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


def test_vsm12_composes_with_world2_vsm11_vsm9_vsm10_and_restore(tmp_path):
    checkpoint = tmp_path / "vsm12-composition.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.drop("lantern").authoritative_changed
    first_wait = app.wait()
    assert first_wait.authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID

    pickup = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to pick up lantern",
    )
    assert pickup.route == "vsm12_actor_mediated_custody"
    assert pickup.result.authoritative_changed
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) == GROUNDSKEEPER_ID

    second_wait = execute_vsm12_terminal_input(app, "wait")
    assert second_wait.route == "existing_terminal"
    assert second_wait.result.authoritative_changed
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    pickup_receipt_id = pickup.result.receipt_id
    assert any(
        transition.receipt.receipt_id == pickup_receipt_id
        and transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
        for transition in app.custody_state.committed_custody_transitions
    )

    stored = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to store lantern in chest",
    )
    assert stored.route == "vsm11_actor_mediated_storage"
    assert stored.result.authoritative_changed

    retrieved = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to retrieve lantern from chest",
    )
    assert retrieved.route == "vsm11_actor_mediated_storage"
    assert retrieved.result.authoritative_changed
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) == GROUNDSKEEPER_ID

    lit = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to light lantern",
    )
    assert lit.route == "vsm9_actor_mediated"
    assert lit.result.authoritative_changed
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    moved = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to go to gatehouse",
    )
    assert moved.route == "vsm10_actor_mediated_movement"
    assert moved.result.authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert _relation_target(app, CARRIED_BY_RELATION_TYPE) == GROUNDSKEEPER_ID

    player_move = execute_vsm12_terminal_input(app, "move south")
    assert player_move.route == "existing_terminal"
    assert player_move.result.authoritative_changed
    assert app.current_place_id() == GATEHOUSE_ID

    look = execute_vsm12_terminal_input(app, "look")
    lantern_fact = next(
        fact for fact in look.result.view.observation_facts if fact.entity_id == LANTERN_ID
    )
    assert lantern_fact.carrier_name == "Groundskeeper"
    assert lantern_fact.lit_state == "lit"

    dropped = execute_vsm12_terminal_input(
        app,
        "ask groundskeeper to drop lantern",
    )
    assert dropped.route == "vsm12_actor_mediated_custody"
    assert dropped.result.authoritative_changed
    assert _relation_target(app, LOCATED_AT_RELATION_TYPE) == GATEHOUSE_ID

    saved = execute_vsm12_terminal_input(app, "save")
    assert saved.result.result_type == "checkpoint_written"
    final_digest = app.authoritative_digest()

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == final_digest
    assert restored.current_place_id() == GATEHOUSE_ID
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    assert _relation_target(restored, LOCATED_AT_RELATION_TYPE) == GATEHOUSE_ID

    actor_custody = [
        transition.receipt
        for transition in restored.custody_state.committed_custody_transitions
        if transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    ]
    assert [receipt.operation for receipt in actor_custody] == ["pickup", "drop"]

    actor_storage = [
        transition.receipt
        for transition in restored.runtime_state.committed_storage_transitions
        if transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    ]
    assert [receipt.operation for receipt in actor_storage] == ["store", "retrieve"]

    direct = execute_vsm12_terminal_input(restored, "pickup lantern")
    assert direct.route == "existing_terminal"
    assert direct.result.authoritative_changed
    assert restored.custody_state.committed_custody_transitions[-1].receipt.actor_entity_id == PLAYER_ID
