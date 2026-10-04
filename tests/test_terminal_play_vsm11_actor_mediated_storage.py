from __future__ import annotations

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
from astra_runtime.myravant_vsm11_actor_mediated_storage import (
    execute_vsm11_request,
    parse_vsm11_request,
)


def _setup_colocated_yard(app: MyravantPlayApplication) -> None:
    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.wait().authoritative_changed is True
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def _setup_groundskeeper_carrying(
    app: MyravantPlayApplication,
    *,
    lit: bool = False,
) -> None:
    _setup_colocated_yard(app)
    if lit:
        assert app.light_object("lantern").authoritative_changed is True
    handoff = app.give_object("lantern", "groundskeeper")
    assert handoff.authoritative_changed is True
    assert _carried_by(app, LANTERN_ID) == GROUNDSKEEPER_ID


def _carried_by(
    app: MyravantPlayApplication,
    object_entity_id: str,
) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def _contained_by(
    app: MyravantPlayApplication,
    object_entity_id: str,
) -> str | None:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if relation.relation_type == CONTAINED_BY_RELATION_TYPE
        and relation.subject_entity_id == object_entity_id
    ]
    assert len(matches) <= 1
    return matches[0] if matches else None


def test_vsm11_parser_is_bounded_to_explicit_storage_and_retrieval_requests():
    cases = {
        "ask groundskeeper to put lantern in chest": "store",
        "ask the groundskeeper to put the brass lantern into the tool chest": "store",
        "ask groundskeeper to store lantern in chest": "store",
        "ask groundskeeper to take lantern from chest": "retrieve",
        "ask the groundskeeper to retrieve the brass lantern from the tool chest": "retrieve",
        "I ask groundskeeper to get lantern from chest": "retrieve",
    }
    for raw, operation in cases.items():
        parsed = parse_vsm11_request(raw)
        assert parsed.parsed is True, (raw, parsed)
        assert parsed.actor_reference == "groundskeeper"
        assert parsed.operation == operation
        assert parsed.object_reference == "lantern"
        assert parsed.container_reference == "chest"

    for raw in (
        "ask groundskeeper to light lantern",
        "ask groundskeeper to open chest",
        "ask groundskeeper to move south",
        "ask groundskeeper to follow me",
        "ask groundskeeper to store lantern",
        "put lantern in chest",
    ):
        assert parse_vsm11_request(raw).parsed is False


def test_vsm11_refuses_when_requested_actor_is_not_local():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    execution = execute_vsm11_request(
        app,
        "ask groundskeeper to put lantern in chest",
    )

    assert execution.result.authoritative_changed is False
    assert execution.result.failure_class == "vsm11_requested_actor_not_local"
    assert execution.request_receipt.acceptance == "refused"
    assert execution.request_receipt.legality_result == "not_evaluated"
    assert execution.request_receipt.performing_actor_entity_id is None
    assert app.authoritative_digest() == before


def test_vsm11_acceptance_does_not_make_player_carried_lantern_legal_for_npc_store():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    assert app.open_object("chest").authoritative_changed is True
    before = app.authoritative_digest()

    execution = execute_vsm11_request(
        app,
        "ask groundskeeper to put lantern in chest",
    )

    assert execution.result.authoritative_changed is False
    assert execution.result.failure_class == "vsm11_int3_opportunity_unavailable"
    assert execution.request_receipt.acceptance == "accepted"
    assert execution.request_receipt.legality_result == "rejected"
    assert execution.request_receipt.performing_actor_entity_id is None
    assert _carried_by(app, LANTERN_ID) == PLAYER_ID
    assert _contained_by(app, LANTERN_ID) is None
    assert app.authoritative_digest() == before


def test_vsm11_closed_container_rejects_after_acceptance_without_mutation():
    app = MyravantPlayApplication.new()
    _setup_groundskeeper_carrying(app)
    before = app.authoritative_digest()

    execution = execute_vsm11_request(
        app,
        "ask groundskeeper to store lantern in chest",
    )

    assert execution.result.authoritative_changed is False
    assert execution.request_receipt.acceptance == "accepted"
    assert execution.request_receipt.legality_result == "rejected"
    assert execution.result.failure_class == "vsm11_int3_opportunity_unavailable"
    assert _carried_by(app, LANTERN_ID) == GROUNDSKEEPER_ID
    assert _contained_by(app, LANTERN_ID) is None
    assert app.authoritative_digest() == before


def test_vsm11_store_commits_existing_int3_as_groundskeeper_action():
    app = MyravantPlayApplication.new()
    _setup_groundskeeper_carrying(app, lit=True)
    assert app.open_object("chest").authoritative_changed is True

    execution = execute_vsm11_request(
        app,
        "ask groundskeeper to put lantern in chest",
    )

    result = execution.result
    receipt = execution.request_receipt
    assert result.result_type == "actor_mediated_storage_committed"
    assert result.authoritative_changed is True
    assert result.message == "The Groundskeeper stores the Brass Lantern in the Tool Chest."
    assert receipt.requester_entity_id == PLAYER_ID
    assert receipt.requested_actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.object_entity_id == LANTERN_ID
    assert receipt.container_entity_id == TOOL_CHEST_ID
    assert receipt.requested_operation == "store"
    assert receipt.acceptance == "accepted"
    assert receipt.legality_result == "allowed"
    assert receipt.authoritative_outcome == "committed"
    assert receipt.authoritative_receipt_id == result.receipt_id
    assert _carried_by(app, LANTERN_ID) is None
    assert _contained_by(app, LANTERN_ID) == TOOL_CHEST_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    transition = next(
        item
        for item in app.storage_state.committed_storage_transitions
        if item.receipt.receipt_id == result.receipt_id
    )
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.operation == "store"


def test_vsm11_redundant_store_is_allowed_no_change():
    app = MyravantPlayApplication.new()
    _setup_groundskeeper_carrying(app)
    assert app.open_object("chest").authoritative_changed is True
    first = execute_vsm11_request(app, "ask groundskeeper to put lantern in chest")
    assert first.result.authoritative_changed is True
    before = app.authoritative_digest()
    count_before = len(app.storage_state.committed_storage_transitions)

    repeat = execute_vsm11_request(app, "ask groundskeeper to store lantern in chest")

    assert repeat.result.result_type == "actor_mediated_storage_unchanged"
    assert repeat.result.authoritative_changed is False
    assert repeat.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert repeat.request_receipt.legality_result == "allowed_no_change"
    assert repeat.request_receipt.authoritative_outcome == "unchanged"
    assert app.authoritative_digest() == before
    assert len(app.storage_state.committed_storage_transitions) == count_before


def test_vsm11_retrieve_commits_to_requested_actor_custody():
    app = MyravantPlayApplication.new()
    _setup_groundskeeper_carrying(app, lit=True)
    assert app.open_object("chest").authoritative_changed is True
    assert execute_vsm11_request(
        app,
        "ask groundskeeper to put lantern in chest",
    ).result.authoritative_changed is True

    execution = execute_vsm11_request(
        app,
        "ask groundskeeper to retrieve lantern from chest",
    )

    assert execution.result.result_type == "actor_mediated_storage_committed"
    assert execution.result.authoritative_changed is True
    assert execution.result.message == "The Groundskeeper retrieves the Brass Lantern from the Tool Chest."
    assert execution.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert execution.request_receipt.requested_operation == "retrieve"
    assert execution.request_receipt.legality_result == "allowed"
    assert _contained_by(app, LANTERN_ID) is None
    assert _carried_by(app, LANTERN_ID) == GROUNDSKEEPER_ID
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    transition = next(
        item
        for item in app.storage_state.committed_storage_transitions
        if item.receipt.receipt_id == execution.result.receipt_id
    )
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.operation == "retrieve"


def test_vsm11_direct_player_int3_remains_player_attributed():
    app = MyravantPlayApplication.new()
    assert app.pickup("lantern").authoritative_changed is True
    assert app.move("south").authoritative_changed is True
    assert app.open_object("chest").authoritative_changed is True

    result = app.store_object("lantern", "chest")

    assert result.authoritative_changed is True
    transition = next(
        item
        for item in app.storage_state.committed_storage_transitions
        if item.receipt.receipt_id == result.receipt_id
    )
    assert transition.receipt.actor_entity_id == PLAYER_ID
    assert transition.receipt.operation == "store"


def test_vsm11_world2_interleaving_preserves_storage_receipt_identity():
    app = MyravantPlayApplication.new()
    _setup_groundskeeper_carrying(app)
    assert app.open_object("chest").authoritative_changed is True
    execution = execute_vsm11_request(app, "ask groundskeeper to store lantern in chest")
    assert execution.result.authoritative_changed is True
    receipt_id = execution.result.receipt_id
    time_before = app.runtime_state.logical_time_state.logical_position

    advanced = app.wait()

    assert advanced.authoritative_changed is True
    assert advanced.logical_time_after == time_before + 1
    assert _contained_by(app, LANTERN_ID) == TOOL_CHEST_ID
    assert any(
        item.receipt.receipt_id == receipt_id
        and item.receipt.actor_entity_id == GROUNDSKEEPER_ID
        for item in app.storage_state.committed_storage_transitions
    )


def test_vsm11_save_restore_preserves_containment_and_actor_attribution(tmp_path):
    path = tmp_path / "vsm11.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_groundskeeper_carrying(app, lit=True)
    assert app.open_object("chest").authoritative_changed is True
    execution = execute_vsm11_request(app, "ask groundskeeper to store lantern in chest")
    assert execution.result.authoritative_changed is True
    expected_digest = app.authoritative_digest()
    receipt_id = execution.result.receipt_id
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)

    assert restored.authoritative_digest() == expected_digest
    assert _contained_by(restored, LANTERN_ID) == TOOL_CHEST_ID
    assert restored.object_lit_state(LANTERN_ID).state == "lit"
    transition = next(
        item
        for item in restored.storage_state.committed_storage_transitions
        if item.receipt.receipt_id == receipt_id
    )
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.operation == "store"


def test_vsm11_fresh_runs_are_deterministic():
    evidence = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        _setup_groundskeeper_carrying(app)
        assert app.open_object("chest").authoritative_changed is True
        execution = execute_vsm11_request(
            app,
            "ask groundskeeper to put lantern in chest",
        )
        evidence.append(
            (
                execution.request_receipt,
                execution.result.command_id,
                execution.result.command_fingerprint,
                execution.result.receipt_id,
                execution.result.state_delta_id,
                execution.result.post_state_digest,
            )
        )
    assert evidence[0] == evidence[1]
