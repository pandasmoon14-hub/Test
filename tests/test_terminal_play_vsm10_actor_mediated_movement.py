from __future__ import annotations

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    PLAYER_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm10_actor_mediated_movement import (
    execute_vsm10_request,
    parse_vsm10_request,
)


def _setup_colocated_yard(app: MyravantPlayApplication) -> None:
    assert app.move("south").authoritative_changed is True
    advanced = app.wait()
    assert advanced.authoritative_changed is True
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def test_vsm10_parser_is_bounded_to_explicit_groundskeeper_movement_requests():
    cases = {
        "ask groundskeeper to go to gatehouse": (None, "gatehouse"),
        "ask the groundskeeper to go to the yard": (None, "yard"),
        "ask groundskeeper to move south": ("south", None),
        "ask groundskeeper to move north": ("north", None),
        "I ask groundskeeper to walk to gatehouse": (None, "gatehouse"),
    }
    for raw, expected in cases.items():
        parsed = parse_vsm10_request(raw)
        assert parsed.parsed is True, (raw, parsed)
        assert (parsed.direction, parsed.destination_reference) == expected
        assert parsed.actor_reference == "groundskeeper"

    for raw in (
        "ask groundskeeper to light lantern",
        "ask groundskeeper to open chest",
        "ask groundskeeper to follow me",
        "ask blacksmith to go to yard",
        "go south",
    ):
        parsed = parse_vsm10_request(raw)
        assert parsed.parsed is False, (raw, parsed)


def test_vsm10_request_refuses_when_requested_actor_is_not_local():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    execution = execute_vsm10_request(
        app,
        "ask groundskeeper to go to yard",
    )

    assert execution.result.authoritative_changed is False
    assert execution.result.failure_class == "vsm10_requested_actor_not_local"
    assert execution.request_receipt.acceptance == "refused"
    assert execution.request_receipt.legality_result == "not_evaluated"
    assert execution.request_receipt.performing_actor_entity_id is None
    assert app.authoritative_digest() == before
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID


def test_vsm10_named_destination_commits_existing_r4c_with_groundskeeper_actor():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    logical_time_before = app.runtime_state.logical_time_state.logical_position

    execution = execute_vsm10_request(
        app,
        "ask groundskeeper to go to gatehouse",
    )

    result = execution.result
    receipt = execution.request_receipt
    assert result.result_type == "actor_mediated_movement_committed"
    assert result.authoritative_changed is True
    assert result.message == "The Groundskeeper moves to the Gatehouse."
    assert receipt.requester_entity_id == PLAYER_ID
    assert receipt.requested_actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.source_place_id == YARD_ID
    assert receipt.destination_place_id == GATEHOUSE_ID
    assert receipt.acceptance == "accepted"
    assert receipt.legality_result == "allowed"
    assert receipt.authoritative_outcome == "committed"
    assert receipt.authoritative_receipt_id == result.receipt_id
    assert receipt.spatial_evidence_id == result.spatial_evidence_id
    assert receipt.opportunity_evidence_id == result.opportunity_evidence_id
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert app.current_place_id() == YARD_ID
    assert app.runtime_state.logical_time_state.logical_position == logical_time_before

    transition = app.state.committed_transitions[-1]
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.source_place_id == YARD_ID
    assert transition.receipt.destination_place_id == GATEHOUSE_ID


def test_vsm10_two_way_directional_requests_follow_existing_fixture_route():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)

    south = execute_vsm10_request(app, "ask groundskeeper to move south")
    assert south.result.authoritative_changed is True
    assert south.request_receipt.destination_place_id == GATEHOUSE_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID

    assert app.move("south").authoritative_changed is True
    assert app.current_place_id() == GATEHOUSE_ID

    north = execute_vsm10_request(app, "ask groundskeeper to move north")
    assert north.result.authoritative_changed is True
    assert north.request_receipt.source_place_id == GATEHOUSE_ID
    assert north.request_receipt.destination_place_id == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert app.current_place_id() == GATEHOUSE_ID


def test_vsm10_direction_resolving_outside_bounded_route_is_accepted_then_rejected():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    before = app.authoritative_digest()
    count_before = len(app.state.committed_transitions)

    execution = execute_vsm10_request(app, "ask groundskeeper to move north")

    assert execution.result.authoritative_changed is False
    assert execution.result.failure_class == "vsm10_destination_outside_bounded_route"
    assert execution.request_receipt.acceptance == "accepted"
    assert execution.request_receipt.legality_result == "rejected"
    assert execution.request_receipt.destination_place_id not in {YARD_ID, GATEHOUSE_ID}
    assert app.authoritative_digest() == before
    assert len(app.state.committed_transitions) == count_before
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def test_vsm10_already_at_requested_destination_is_nonmutating():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    before = app.authoritative_digest()
    count_before = len(app.state.committed_transitions)

    execution = execute_vsm10_request(app, "ask groundskeeper to go to yard")

    assert execution.result.result_type == "actor_mediated_movement_unchanged"
    assert execution.result.authoritative_changed is False
    assert execution.request_receipt.performing_actor_entity_id == GROUNDSKEEPER_ID
    assert execution.request_receipt.acceptance == "accepted"
    assert execution.request_receipt.legality_result == "allowed_no_change"
    assert execution.request_receipt.authoritative_outcome == "unchanged"
    assert app.authoritative_digest() == before
    assert len(app.state.committed_transitions) == count_before


def test_vsm10_movement_changes_public_actor_presence_without_changing_player_location():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    assert "Groundskeeper" in app.look().view.actors

    moved = execute_vsm10_request(app, "ask groundskeeper to go to gatehouse")
    assert moved.result.authoritative_changed is True
    assert app.current_place_id() == YARD_ID
    assert "Groundskeeper" not in app.look().view.actors

    assert app.move("south").authoritative_changed is True
    assert app.current_place_id() == GATEHOUSE_ID
    assert "Groundskeeper" in app.look().view.actors


def test_vsm10_world2_interleaving_preserves_actor_and_transition_integrity():
    app = MyravantPlayApplication.new()
    _setup_colocated_yard(app)
    moved = execute_vsm10_request(app, "ask groundskeeper to go to gatehouse")
    assert moved.result.authoritative_changed is True
    receipt_id = moved.result.receipt_id
    time_before = app.runtime_state.logical_time_state.logical_position

    advanced = app.wait()

    assert advanced.authoritative_changed is True
    assert advanced.logical_time_after == time_before + 1
    assert any(
        transition.receipt.receipt_id == receipt_id
        and transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
        for transition in app.state.committed_transitions
    )
    assert app.entity_place_id(GROUNDSKEEPER_ID) in {YARD_ID, GATEHOUSE_ID}


def test_vsm10_save_restore_preserves_actor_location_and_attribution(tmp_path):
    path = tmp_path / "vsm10.json"
    app = MyravantPlayApplication.new(checkpoint_path=path)
    _setup_colocated_yard(app)
    execution = execute_vsm10_request(app, "ask groundskeeper to go to gatehouse")
    assert execution.result.authoritative_changed is True
    final_digest = app.authoritative_digest()
    receipt_id = execution.result.receipt_id
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=path)
    assert restored.authoritative_digest() == final_digest
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    transition = next(
        item
        for item in restored.state.committed_transitions
        if item.receipt.receipt_id == receipt_id
    )
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.source_place_id == YARD_ID
    assert transition.receipt.destination_place_id == GATEHOUSE_ID


def test_vsm10_fresh_runs_are_deterministic():
    evidence = []
    for _ in range(2):
        app = MyravantPlayApplication.new()
        _setup_colocated_yard(app)
        execution = execute_vsm10_request(
            app,
            "ask groundskeeper to go to gatehouse",
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
