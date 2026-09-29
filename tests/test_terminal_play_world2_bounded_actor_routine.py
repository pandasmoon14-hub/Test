"""TERMINAL-PLAY-WORLD-2 bounded autonomous actor routine tests."""

from __future__ import annotations

import json
from io import StringIO

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    digest_persistent_world_object_open_states,
    replay_persistent_world_object_open_close_states,
)
from astra_runtime.myravant_live_play_evidence import (
    LivePlayEvidenceRecorder,
    build_live_play_session_header,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID,
    GROUNDSKEEPER_ID,
    TOOL_CHEST_ID,
    YARD_ID,
)
from astra_runtime.myravant_terminal import run_terminal


def _actor_place(app: MyravantPlayApplication) -> str:
    matches = [
        relation.object_entity_id
        for relation in app.state.representation.relations
        if (
            relation.relation_type == LOCATED_AT_RELATION_TYPE
            and relation.subject_entity_id == GROUNDSKEEPER_ID
        )
    ]
    assert len(matches) == 1
    return matches[0]


def _recorder(path, app):
    return LivePlayEvidenceRecorder(
        trace_path=path,
        header=build_live_play_session_header(
            session_id="world2-test",
            campaign_id=app.fixture.campaign_id,
            repository_sha="d" * 40,
            initial_state_digest=app.authoritative_digest(),
            restore_performed=False,
            network_mode="offline",
        ),
    )


def _records(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_world2_four_step_routine_reuses_movement_and_open_close_owners():
    app = MyravantPlayApplication.new()

    first = app.wait()
    assert first.logical_time_after == 1
    assert first.world_event_class == "world_autonomous_action"
    assert first.world_process_actor_id == GROUNDSKEEPER_ID
    assert first.world_process_action == "move"
    assert first.world_process_target_id == YARD_ID
    assert first.world_process_outcome == "committed"
    assert first.spatial_evidence_id
    assert first.opportunity_evidence_id
    assert _actor_place(app) == YARD_ID
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"

    second = app.wait()
    assert second.logical_time_after == 2
    assert second.world_process_action == "open_object"
    assert second.world_process_target_id == TOOL_CHEST_ID
    assert second.world_process_outcome == "committed"
    assert second.consequence_receipt_id
    assert second.consequence_state_delta_id
    assert _actor_place(app) == YARD_ID
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"

    third = app.wait()
    assert third.logical_time_after == 3
    assert third.world_process_action == "close_object"
    assert third.world_process_outcome == "committed"
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert _actor_place(app) == YARD_ID

    fourth = app.wait()
    assert fourth.logical_time_after == 4
    assert fourth.world_process_action == "move"
    assert fourth.world_process_target_id == GATEHOUSE_ID
    assert fourth.world_process_outcome == "committed"
    assert _actor_place(app) == GATEHOUSE_ID


def test_world2_player_preopen_changes_due_open_to_explicit_already_satisfied():
    app = MyravantPlayApplication.new()
    app.move("south")
    player_open = app.open_object("tool chest")
    assert player_open.result_type == "object_state_committed"

    app.wait()
    before_count = len(
        app.object_state.committed_object_state_transitions
    )
    due_open = app.wait()

    assert due_open.logical_time_after == 2
    assert due_open.world_process_action == "open_object"
    assert due_open.world_process_outcome == "already_satisfied"
    assert due_open.world_process_command_id
    assert due_open.opportunity_evidence_id
    assert due_open.consequence_receipt_id is None
    assert due_open.consequence_state_delta_id is None
    assert len(
        app.object_state.committed_object_state_transitions
    ) == before_count
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"


def test_world2_player_removal_changes_due_open_to_opportunity_unavailable():
    app = MyravantPlayApplication.new()
    app.move("south")
    pickup = app.pickup("tool chest")
    assert pickup.result_type == "custody_committed"
    app.move("north")

    app.wait()
    due_open = app.wait()

    assert due_open.logical_time_after == 2
    assert due_open.world_process_action == "open_object"
    assert due_open.world_process_outcome == "opportunity_unavailable"
    assert due_open.opportunity_evidence_id
    assert due_open.consequence_receipt_id is None
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert len(app.object_state.committed_object_state_transitions) == 0
    assert _actor_place(app) == YARD_ID


def test_world2_player_and_autonomous_command_ids_remain_disjoint():
    app = MyravantPlayApplication.new()
    app.move("south")
    app.open_object("tool chest")
    app.close_object("tool chest")
    app.wait()
    actor_open = app.wait()

    object_ids = {
        transition.command_id
        for transition in app.object_state.committed_object_state_transitions
    }
    movement_ids = {
        transition.command_id
        for transition in app.state.committed_transitions
    }
    time_ids = {
        transition.command_id
        for transition in app.runtime_state.logical_time_state.committed_transitions
    }

    assert "terminal-object-state-000001" in object_ids
    assert "terminal-object-state-000002" in object_ids
    assert actor_open.world_process_command_id in object_ids
    assert actor_open.world_process_command_id.startswith("world2-npc-open-")
    assert not (object_ids & movement_ids)
    assert not (object_ids & time_ids)
    assert not (movement_ids & time_ids)


def test_world2_checkpoint_restore_continues_same_derived_routine_phase(tmp_path):
    checkpoint = tmp_path / "world2.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    app.wait()
    opened = app.wait()
    assert opened.world_process_action == "open_object"
    assert app.object_open_state(TOOL_CHEST_ID).state == "open"
    app.save()
    before = app.authoritative_digest()

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == before
    assert restored.runtime_state.logical_time_state.logical_position == 2
    assert _actor_place(restored) == YARD_ID
    assert restored.object_open_state(TOOL_CHEST_ID).state == "open"

    closed = restored.wait()
    assert closed.logical_time_after == 3
    assert closed.world_process_action == "close_object"
    assert closed.world_process_outcome == "committed"
    assert restored.object_open_state(TOOL_CHEST_ID).state == "closed"


def test_world2_identical_initial_state_and_waits_are_deterministic():
    left = MyravantPlayApplication.new()
    right = MyravantPlayApplication.new()

    left_results = [left.wait() for _ in range(8)]
    right_results = [right.wait() for _ in range(8)]

    assert left.authoritative_digest() == right.authoritative_digest()
    assert [
        (
            result.logical_time_after,
            result.world_process_action,
            result.world_process_target_id,
            result.world_process_command_id,
            result.world_process_outcome,
            result.consequence_receipt_id,
        )
        for result in left_results
    ] == [
        (
            result.logical_time_after,
            result.world_process_action,
            result.world_process_target_id,
            result.world_process_command_id,
            result.world_process_outcome,
            result.consequence_receipt_id,
        )
        for result in right_results
    ]


def test_world2_autonomous_open_receipt_replays_through_existing_owner():
    app = MyravantPlayApplication.new()
    initial_states = app.object_state.object_open_states

    app.wait()
    due_open = app.wait()
    transition = next(
        transition
        for transition in app.object_state.committed_object_state_transitions
        if transition.command_id == due_open.world_process_command_id
    )

    replayed = replay_persistent_world_object_open_close_states(
        object_open_states=initial_states,
        receipt=transition.receipt,
    )
    assert digest_persistent_world_object_open_states(replayed) == (
        transition.receipt.post_state_digest
    )
    assert transition.receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert transition.receipt.object_entity_id == TOOL_CHEST_ID
    assert transition.receipt.operation == "open"


def test_world2_unobserved_action_is_trace_evidence_not_player_knowledge(tmp_path):
    trace = tmp_path / "world2-trace.jsonl"
    app = MyravantPlayApplication.new()
    recorder = _recorder(trace, app)
    output = StringIO()

    run_terminal(
        app,
        input_stream=StringIO("wait\nwait\nlook\nexit\n"),
        output_stream=output,
        evidence_recorder=recorder,
    )

    visible = output.getvalue().casefold()
    assert "time passes." in visible
    assert "groundskeeper" not in visible
    assert "tool chest" not in visible

    interactions = [
        row
        for row in _records(trace)
        if row["record_type"] == "interaction"
    ]
    second_wait = [
        row for row in interactions
        if row["parsed_action"] == "wait"
    ][1]
    assert second_wait["world_event_class"] == "world_autonomous_action"
    assert second_wait["world_process_actor_id"] == GROUNDSKEEPER_ID
    assert second_wait["world_process_action"] == "open_object"
    assert second_wait["world_process_target_id"] == TOOL_CHEST_ID
    assert second_wait["world_process_outcome"] == "committed"

    app.move("south")
    inspection = app.inspect("tool chest")
    assert "lid is open" in inspection.view.description.casefold()
