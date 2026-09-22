"""Focused tests for the bounded Myravant terminal application adapter."""

from __future__ import annotations

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import WORKSHOP_ID, YARD_ID


def test_look_reads_authoritative_location_without_mutation():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.look()

    assert result.result_type == "look"
    assert result.view is not None
    assert result.view.place_id == WORKSHOP_ID
    assert "Brass Lantern" in result.view.objects
    assert app.authoritative_digest() == before


def test_move_routes_through_r4_c_and_changes_authoritative_location():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.move("south")

    assert result.result_type == "movement_committed"
    assert result.authoritative_changed is True
    assert result.command_id == "terminal-move-000001"
    assert result.receipt_id is not None
    assert result.state_delta_id is not None
    assert result.pre_state_digest == before
    assert result.post_state_digest == app.authoritative_digest()
    assert result.post_state_digest != before
    assert app.current_place_id() == YARD_ID


def test_undeclared_route_fails_without_authoritative_change():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()

    result = app.move("east")

    assert result.result_type == "movement_rejected"
    assert result.failure_class == "unavailable_fixture_route"
    assert result.authoritative_changed is False
    assert result.pre_state_digest == before
    assert result.post_state_digest == before
    assert app.authoritative_digest() == before
    assert app.current_place_id() == WORKSHOP_ID


def test_save_restore_and_new_play_cross_process_shape(tmp_path):
    checkpoint = tmp_path / "myravant-g1.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    first = app.move("south")
    saved = app.save()

    assert checkpoint.exists()
    assert saved.checkpoint_digest is not None

    del app

    restored = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert restored.current_place_id() == YARD_ID

    second = restored.move("north")
    assert second.command_id == "terminal-move-000002"
    assert second.command_id != first.command_id
    assert restored.current_place_id() == WORKSHOP_ID

    restored.save()
    del restored

    restored_again = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert restored_again.current_place_id() == WORKSHOP_ID
    assert len(restored_again.state.committed_transitions) == 2
