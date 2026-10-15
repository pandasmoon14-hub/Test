"""Regression: WORLD-2 time must not stall when follow moves an NPC off routine.

The world routine may not fabricate a location/route, but an unavailable
autonomous move is not a reason to refuse a qualified player wait.
"""
from __future__ import annotations

import subprocess
import sys

from astra_runtime.domain.persistent_world_follow_intent import (
    active_follow_intent_for,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, GATEHOUSE_ID, WORKSHOP_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import (
    execute_vsm14_follow_request,
)


def _follow_from_gatehouse(app):
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.current_place_id() == GATEHOUSE_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    accepted = execute_vsm14_follow_request(
        app, "ask groundskeeper to follow me",
    )
    assert accepted.result.authoritative_changed
    assert active_follow_intent_for(
        app.follow_intent_state, GROUNDSKEEPER_ID,
    ) is not None


def test_gatehouse_follow_yard_wait_commits_due_time_without_fake_move(tmp_path):
    """The user's exact Gatehouse -> Yard -> wait reproduction, now lawful."""
    checkpoint = tmp_path / "follow-yard-wait.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _follow_from_gatehouse(app)
    before = app.authoritative_digest()
    moved = app.move("north")
    assert moved.authoritative_changed
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert app.authoritative_digest() != before

    original_movement_count = len(app.state.committed_transitions)
    first = app.wait()
    assert first.result_type == "world_advanced"
    assert first.authoritative_changed
    assert first.world_process_actor_id == GROUNDSKEEPER_ID
    assert first.world_process_action == "move"
    assert first.world_process_outcome == "already_satisfied"
    assert first.logical_time_before == 0
    assert first.logical_time_after == 1
    assert first.receipt_id and first.state_delta_id
    assert first.due_process_ref and first.world_process_command_id
    assert first.consequence_receipt_id is None
    assert len(app.state.committed_transitions) == original_movement_count
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert active_follow_intent_for(
        app.follow_intent_state, GROUNDSKEEPER_ID,
    ) is not None

    second = app.wait()
    third = app.wait()
    assert second.authoritative_changed and third.authoritative_changed
    assert [first.logical_time_after, second.logical_time_after, third.logical_time_after] == [
        1, 2, 3,
    ]
    assert app.save().checkpoint_digest
    resumed = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert resumed.authoritative_digest() == app.authoritative_digest()
    assert resumed.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert resumed.runtime_state.logical_time_state.logical_position == 3


def test_follow_to_workshop_skips_unlicensed_routine_without_teleport(tmp_path):
    checkpoint = tmp_path / "offroutine.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _follow_from_gatehouse(app)
    assert app.move("north").authoritative_changed
    assert app.move("north").authoritative_changed
    assert app.current_place_id() == WORKSHOP_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == WORKSHOP_ID
    movement_count = len(app.state.committed_transitions)
    first = app.wait()
    assert first.authoritative_changed
    assert first.world_process_outcome == "opportunity_unavailable"
    assert first.logical_time_after == 1
    assert first.consequence_receipt_id is None
    assert len(app.state.committed_transitions) == movement_count
    assert app.entity_place_id(GROUNDSKEEPER_ID) == WORKSHOP_ID

    assert app.wait().authoritative_changed
    assert app.wait().authoritative_changed
    fourth = app.wait()
    assert fourth.authoritative_changed
    assert fourth.logical_time_after == 4
    assert fourth.world_process_outcome == "opportunity_unavailable"
    assert fourth.consequence_receipt_id is None
    assert len(app.state.committed_transitions) == movement_count
    assert app.entity_place_id(GROUNDSKEEPER_ID) == WORKSHOP_ID
    app.save()
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == WORKSHOP_ID


def test_original_qualified_world2_movement_keeps_causal_receipt():
    app = MyravantVSM14Application.new()
    moved = app.wait()
    assert moved.authoritative_changed
    assert moved.world_process_outcome == "committed"
    assert moved.consequence_receipt_id
    assert moved.consequence_state_delta_id
    assert moved.logical_time_after == 1
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert len(app.state.committed_transitions) == 1


def test_follow_stall_replay_is_deterministic_and_time_monotonic():
    receipt_sequences = []
    for _ in range(2):
        app = MyravantVSM14Application.new()
        _follow_from_gatehouse(app)
        assert app.move("north").authoritative_changed
        assert app.move("north").authoritative_changed
        receipts = []
        for step in range(1, 9):
            advance = app.wait()
            assert advance.authoritative_changed
            assert advance.logical_time_before == step - 1
            assert advance.logical_time_after == step
            assert advance.receipt_id
            receipts.append((
                advance.receipt_id,
                advance.state_delta_id,
                advance.world_process_outcome,
                app.authoritative_digest(),
            ))
        receipt_sequences.append(receipts)
    assert receipt_sequences[0] == receipt_sequences[1]


def test_installed_terminal_follow_wait_survives_two_sessions(tmp_path):
    checkpoint = tmp_path / "terminal-follow-wait.json"

    def run(commands, *flags):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *flags],
            input="\n".join((*commands, "exit", "")),
            text=True, capture_output=True, timeout=120,
        )

    first = run((
        "go south", "go south", "ask groundskeeper to follow me",
        "go north", "wait", "wait", "wait",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "agrees to follow you" in first.stdout
    assert first.stdout.count("Time passes.") >= 3
    assert "bounded world advancement was rejected" not in first.stdout
    assert checkpoint.is_file()

    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.runtime_state.logical_time_state.logical_position == 3
    second = run(("wait", "wait"), "--load", str(checkpoint))
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert second.stdout.count("Time passes.") == 2
    assert "bounded world advancement was rejected" not in second.stdout
    later = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert later.runtime_state.logical_time_state.logical_position == 5
