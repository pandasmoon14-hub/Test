"""VSM-4R INT-1 storage-order-independent replay reconstruction tests."""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import replace

import pytest

from astra_runtime.domain.persistent_world_component_checkpoint import (
    COMPONENT_CHECKPOINT_FORMAT_IDENTITY,
    WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION,
)
from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointEvidenceError,
    write_persistent_world_object_open_close_checkpoint,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    PersistentWorldObjectOpenCloseReplayError,
    PersistentWorldObjectOpenCloseRetryConflictError,
    PersistentWorldObjectOpenState,
    digest_persistent_world_composite_state,
    digest_persistent_world_object_open_states,
    execute_persistent_world_object_open_close,
    replay_persistent_world_object_open_close_transition_history,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID,
    TOOL_CHEST_ID,
)


def _canonical_json(value) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _rewrite_integrity(path, envelope) -> None:
    payload = envelope["authoritative_payload"]
    envelope["integrity_digest"] = hashlib.sha256(
        _canonical_json(payload).encode("utf-8")
    ).hexdigest()
    path.write_text(_canonical_json(envelope), encoding="utf-8")


def _waits(app: MyravantPlayApplication, count: int) -> None:
    for _ in range(count):
        app.wait()


def test_vsm4r_three_wait_checkpoint_restores_while_order_stays_noncausal(
    tmp_path,
):
    checkpoint = tmp_path / "three-waits.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    _waits(app, 3)

    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert [
        transition.receipt.operation
        for transition in app.object_state.committed_object_state_transitions
    ] == ["close", "open"]

    before = app.authoritative_digest()
    app.save()

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert envelope["format_identity"] == COMPONENT_CHECKPOINT_FORMAT_IDENTITY
    assert envelope["format_version"] == WORLD1_COMPONENT_CHECKPOINT_FORMAT_VERSION

    persisted = (
        envelope["authoritative_payload"]["components"]["open_close"]
        ["committed_object_state_transitions"]
    )
    assert [item["receipt"]["operation"] for item in persisted] == [
        "close",
        "open",
    ]

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)

    assert restored.authoritative_digest() == before
    assert restored.runtime_state.logical_time_state.logical_position == 3
    assert restored.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert len(restored.object_state.committed_object_state_transitions) == 2


def test_vsm4r_owner_replay_is_independent_of_transition_collection_order():
    app = MyravantPlayApplication.new()
    _waits(app, 7)

    transitions = app.object_state.committed_object_state_transitions
    assert len(transitions) == 4
    expected_digest = digest_persistent_world_object_open_states(
        app.object_state.object_open_states
    )

    for permutation in itertools.permutations(transitions):
        replayed = replay_persistent_world_object_open_close_transition_history(
            object_open_states=app.fixture.initial_object_open_states,
            committed_transitions=permutation,
        )
        assert digest_persistent_world_object_open_states(replayed) == (
            expected_digest
        )


def test_vsm4r_owner_replay_requires_complete_connected_transition_evidence():
    app = MyravantPlayApplication.new()
    _waits(app, 3)
    transitions = app.object_state.committed_object_state_transitions

    disconnected_receipt = replace(
        transitions[0].receipt,
        pre_state_digest="f" * 64,
    )
    disconnected = replace(
        transitions[0],
        receipt=disconnected_receipt,
    )

    with pytest.raises(PersistentWorldObjectOpenCloseReplayError):
        replay_persistent_world_object_open_close_transition_history(
            object_open_states=app.fixture.initial_object_open_states,
            committed_transitions=(disconnected, transitions[1]),
        )


def test_vsm4r_owner_replay_still_validates_receipt_object_semantics():
    app = MyravantPlayApplication.new()
    _waits(app, 2)
    transition = app.object_state.committed_object_state_transitions[0]

    wrong_target_receipt = replace(
        transition.receipt,
        object_entity_id=LANTERN_ID,
    )
    wrong_target = replace(
        transition,
        receipt=wrong_target_receipt,
    )

    with pytest.raises(PersistentWorldObjectOpenCloseReplayError):
        replay_persistent_world_object_open_close_transition_history(
            object_open_states=app.fixture.initial_object_open_states,
            committed_transitions=(wrong_target,),
        )


def test_vsm4r_sixty_four_waits_round_trip_all_autonomous_int1_evidence(
    tmp_path,
):
    checkpoint = tmp_path / "sixty-four-waits.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    _waits(app, 64)

    assert app.runtime_state.logical_time_state.logical_position == 64
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert len(app.object_state.committed_object_state_transitions) == 32

    before_digest = app.authoritative_digest()
    app.save()
    first_payload = json.loads(
        checkpoint.read_text(encoding="utf-8")
    )["authoritative_payload"]

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)

    assert restored.authoritative_digest() == before_digest
    assert restored.runtime_state.logical_time_state.logical_position == 64
    assert restored.object_open_state(TOOL_CHEST_ID).state == "closed"
    assert len(restored.object_state.committed_object_state_transitions) == 32

    restored.save()
    second_payload = json.loads(
        checkpoint.read_text(encoding="utf-8")
    )["authoritative_payload"]

    assert second_payload == first_payload


def test_vsm4r_mixed_autonomous_open_then_player_close_round_trips(tmp_path):
    checkpoint = tmp_path / "mixed.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)

    app.wait()
    opened = app.wait()
    assert opened.world_process_action == "open_object"
    assert opened.world_process_outcome == "committed"

    app.move("south")
    closed = app.close_object("tool chest")
    assert closed.result_type == "object_state_committed"

    transitions = app.object_state.committed_object_state_transitions
    assert [item.receipt.operation for item in transitions] == [
        "close",
        "open",
    ]
    assert transitions[0].command_id.startswith("terminal-object-state-")
    assert transitions[1].command_id.startswith("world2-npc-open-")

    before = app.authoritative_digest()
    app.save()
    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)

    assert restored.authoritative_digest() == before
    assert restored.object_open_state(TOOL_CHEST_ID).state == "closed"


def test_vsm4r_restore_rejects_terminal_state_that_disagrees_with_replay(
    tmp_path,
):
    checkpoint = tmp_path / "terminal-mismatch.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    _waits(app, 3)

    write_persistent_world_object_open_close_checkpoint(
        state=app.object_state,
        checkpoint_path=checkpoint,
        qualification_evidence=app.fixture.checkpoint_qualification,
    )

    envelope = json.loads(checkpoint.read_text(encoding="utf-8"))
    payload = envelope["authoritative_payload"]

    changed_states = tuple(
        PersistentWorldObjectOpenState(
            object_entity_id=item.object_entity_id,
            state=(
                "open"
                if item.object_entity_id == TOOL_CHEST_ID
                else item.state
            ),
        )
        for item in app.object_state.object_open_states
    )
    payload["object_open_states"] = [
        item.to_dict() for item in changed_states
    ]
    payload["object_state_digest"] = (
        digest_persistent_world_object_open_states(changed_states)
    )
    payload["world_state_digest"] = digest_persistent_world_composite_state(
        app.state.representation,
        changed_states,
    )
    _rewrite_integrity(checkpoint, envelope)

    with pytest.raises(PersistentWorldCheckpointEvidenceError):
        MyravantPlayApplication.restore(checkpoint_path=checkpoint)


def test_vsm4r_post_restore_retry_identity_and_conflict_are_preserved(tmp_path):
    checkpoint = tmp_path / "retry.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    app.move("south")
    opened = app.open_object("tool chest")
    app.save()

    restored = MyravantPlayApplication.restore(checkpoint_path=checkpoint)

    retry_command = create_command_envelope(
        command_id=opened.command_id,
        command_type="open_object",
        source_actor_id=restored.fixture.player_entity_id,
        payload={"object_entity_id": TOOL_CHEST_ID},
        metadata={"client": "myravant-terminal-int1"},
    )
    qualification, opportunity = restored.fixture.object_open_close_evidence(
        command_id=retry_command.command_id,
        actor_entity_id=restored.fixture.player_entity_id,
        object_entity_id=TOOL_CHEST_ID,
        operation="open",
        opportunity_available=True,
    )
    retried = execute_persistent_world_object_open_close(
        state=restored.object_state,
        command=retry_command,
        qualification_evidence=qualification,
        opportunity_evidence=opportunity,
        expected_pre_state_digest=restored.object_state_digest(),
    )

    assert retried.technical_retry is True
    assert retried.receipt.receipt_id == opened.receipt_id

    conflict_command = create_command_envelope(
        command_id=opened.command_id,
        command_type="close_object",
        source_actor_id=restored.fixture.player_entity_id,
        payload={"object_entity_id": TOOL_CHEST_ID},
        metadata={"client": "myravant-terminal-int1"},
    )
    qualification, opportunity = restored.fixture.object_open_close_evidence(
        command_id=conflict_command.command_id,
        actor_entity_id=restored.fixture.player_entity_id,
        object_entity_id=TOOL_CHEST_ID,
        operation="close",
        opportunity_available=True,
    )

    with pytest.raises(PersistentWorldObjectOpenCloseRetryConflictError):
        execute_persistent_world_object_open_close(
            state=restored.object_state,
            command=conflict_command,
            qualification_evidence=qualification,
            opportunity_evidence=opportunity,
            expected_pre_state_digest=restored.object_state_digest(),
        )
