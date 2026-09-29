from __future__ import annotations

import pytest

from astra_runtime.domain.persistent_world_logical_time import (
    PersistentWorldLogicalTimeRetryConflictError,
    create_persistent_world_logical_time_state,
    digest_persistent_world_logical_time_state,
    execute_persistent_world_logical_time,
    replay_persistent_world_logical_time,
)
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.myravant_play_fixture import PLAYER_ID


def _wait(command_id: str = "terminal-time-000001", steps: int = 1):
    return create_command_envelope(
        command_id=command_id,
        command_type="wait",
        source_actor_id=PLAYER_ID,
        payload={
            "advance_steps": steps,
            "scheduler_profile_id": "terminal-play-bounded-world-step-v1",
        },
    )


def test_world1_wait_advances_one_pinned_logical_position():
    state = create_persistent_world_logical_time_state()
    result = execute_persistent_world_logical_time(
        state=state,
        command=_wait(),
        expected_pre_state_digest=(
            digest_persistent_world_logical_time_state(state)
        ),
    )
    assert state.logical_position == 0
    assert result.state.logical_position == 1
    assert result.receipt.pre_position == 0
    assert result.receipt.post_position == 1
    assert result.technical_retry is False


def test_world1_identical_retry_is_idempotent_and_changed_meaning_conflicts():
    state = create_persistent_world_logical_time_state()
    command = _wait()
    first = execute_persistent_world_logical_time(
        state=state,
        command=command,
        expected_pre_state_digest=(
            digest_persistent_world_logical_time_state(state)
        ),
    )
    retry = execute_persistent_world_logical_time(
        state=first.state,
        command=command,
        expected_pre_state_digest=(
            digest_persistent_world_logical_time_state(first.state)
        ),
    )
    assert retry.state == first.state
    assert retry.receipt == first.receipt
    assert retry.technical_retry is True

    with pytest.raises(PersistentWorldLogicalTimeRetryConflictError):
        execute_persistent_world_logical_time(
            state=first.state,
            command=_wait(steps=2),
            expected_pre_state_digest=(
                digest_persistent_world_logical_time_state(first.state)
            ),
        )


def test_world1_logical_time_replay_reproduces_state():
    state = create_persistent_world_logical_time_state()
    result = execute_persistent_world_logical_time(
        state=state,
        command=_wait(),
        expected_pre_state_digest=(
            digest_persistent_world_logical_time_state(state)
        ),
    )
    replayed = replay_persistent_world_logical_time(
        pre_state=state,
        committed=result.state.committed_transitions[-1],
    )
    assert replayed == result.state
