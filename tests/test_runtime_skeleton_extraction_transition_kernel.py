from __future__ import annotations

import hashlib
import inspect
import json
from dataclasses import FrozenInstanceError, dataclass, replace

import pytest

import astra_runtime.domain._deterministic_transition_support as support
from astra_runtime.domain._deterministic_transition_support import (
    TransitionCapabilitySpec,
    commit_prepared_capability_transition,
    digest_capability_state,
    execute_capability_transition,
    fingerprint_capability_command,
    fingerprint_command_envelope,
    prepare_capability_transition,
    replay_capability_transition,
)
from astra_runtime.kernel.command_envelope import create_command_envelope


@dataclass(frozen=True)
class _SyntheticCommitted:
    command_id: str
    command_fingerprint: str
    delta: int


@dataclass(frozen=True)
class _SyntheticState:
    value: int
    committed: tuple[_SyntheticCommitted, ...] = ()


@dataclass(frozen=True)
class _SyntheticPrepared:
    command_id: str
    command_fingerprint: str
    pre_value: int
    post_value: int
    delta: int


@dataclass(frozen=True)
class _SyntheticResult:
    state: _SyntheticState
    committed: _SyntheticCommitted
    technical_retry: bool


class _SyntheticRetryConflict(ValueError):
    pass


def _state_digest(state: object) -> str:
    assert isinstance(state, _SyntheticState)
    material = {
        "value": state.value,
        "committed": [
            {
                "command_id": item.command_id,
                "command_fingerprint": item.command_fingerprint,
                "delta": item.delta,
            }
            for item in state.committed
        ],
    }
    canonical = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _fingerprint(command) -> str:
    return fingerprint_command_envelope(command, allow_nan=False)


def _prepare(state, command, context):
    assert isinstance(state, _SyntheticState)
    delta = context.get("delta")
    if type(delta) is not int or delta == 0:
        raise ValueError("synthetic delta must be a non-zero integer")
    fingerprint = _fingerprint(command)
    return _SyntheticPrepared(
        command_id=command.command_id,
        command_fingerprint=fingerprint,
        pre_value=state.value,
        post_value=state.value + delta,
        delta=delta,
    )


def _commit(state, prepared):
    assert isinstance(state, _SyntheticState)
    assert isinstance(prepared, _SyntheticPrepared)
    if state.value != prepared.pre_value:
        raise ValueError("synthetic state changed after preparation")
    committed = _SyntheticCommitted(
        command_id=prepared.command_id,
        command_fingerprint=prepared.command_fingerprint,
        delta=prepared.delta,
    )
    post = _SyntheticState(
        value=prepared.post_value,
        committed=(*state.committed, committed),
    )
    return _SyntheticResult(
        state=post,
        committed=committed,
        technical_retry=False,
    )


def _retry_result(state, committed):
    assert isinstance(state, _SyntheticState)
    assert isinstance(committed, _SyntheticCommitted)
    return _SyntheticResult(
        state=state,
        committed=committed,
        technical_retry=True,
    )


def _replay(pre_state, receipt):
    assert type(pre_state) is int
    assert type(receipt) is int
    return pre_state + receipt


def _spec() -> TransitionCapabilitySpec:
    return TransitionCapabilitySpec(
        capability_id="synthetic_transition",
        semantic_owners=("TEST-OWNER-A", "TEST-OWNER-B"),
        state_type=_SyntheticState,
        replay_state_type=int,
        receipt_prefix="synthetic_receipt",
        state_digest=_state_digest,
        fingerprint_command=_fingerprint,
        committed_transitions=lambda state: state.committed,
        prepare_new_transition=_prepare,
        commit_new_transition=_commit,
        build_retry_result=_retry_result,
        retry_conflict_error=lambda message: _SyntheticRetryConflict(message),
        replay_committed_transition=_replay,
    )


def _command(*, payload_value: int = 1):
    return create_command_envelope(
        command_id="skeleton-extraction-command-001",
        command_type="synthetic_transition",
        source_actor_id="astra:entity:skeleton-extraction-actor",
        payload={"value": payload_value},
        metadata={"source": "skeleton-extraction-test"},
    )


def test_capability_kernel_delegates_digest_and_fingerprint_exactly() -> None:
    spec = _spec()
    state = _SyntheticState(value=4)
    command = _command()

    assert digest_capability_state(spec=spec, state=state) == _state_digest(state)
    assert (
        fingerprint_capability_command(spec=spec, command=command)
        == _fingerprint(command)
    )


def test_capability_kernel_execute_is_deterministic_and_retry_safe() -> None:
    spec = _spec()
    state = _SyntheticState(value=10)
    command = _command()

    first = execute_capability_transition(
        spec=spec,
        state=state,
        command=command,
        context={"delta": 3},
    )
    assert first.state.value == 13
    assert first.technical_retry is False
    assert len(first.state.committed) == 1

    retry = execute_capability_transition(
        spec=spec,
        state=first.state,
        command=command,
        # Retry resolves before domain preparation can reinterpret context.
        context={"delta": 99},
    )
    assert retry.state is first.state
    assert retry.committed == first.committed
    assert retry.technical_retry is True


def test_capability_kernel_conflicting_command_identity_fails_closed() -> None:
    spec = _spec()
    first = execute_capability_transition(
        spec=spec,
        state=_SyntheticState(value=1),
        command=_command(payload_value=1),
        context={"delta": 2},
    )

    with pytest.raises(_SyntheticRetryConflict):
        execute_capability_transition(
            spec=spec,
            state=first.state,
            command=_command(payload_value=2),
            context={"delta": 2},
        )


def test_prepare_and_commit_preserve_command_identity() -> None:
    spec = _spec()
    state = _SyntheticState(value=2)
    command = _command()
    prepared = prepare_capability_transition(
        spec=spec,
        state=state,
        command=command,
        context={"delta": 5},
    )
    assert prepared.command_id == command.command_id
    assert prepared.command_fingerprint == _fingerprint(command)

    result = commit_prepared_capability_transition(
        spec=spec,
        state=state,
        prepared=prepared,
    )
    assert result.state.value == 7
    assert result.technical_retry is False


def test_replay_remains_callback_owned() -> None:
    assert replay_capability_transition(
        spec=_spec(),
        pre_state=10,
        receipt=4,
    ) == 14


def test_spec_is_immutable_and_preserves_multiple_owner_declarations() -> None:
    spec = _spec()

    assert spec.semantic_owners == ("TEST-OWNER-A", "TEST-OWNER-B")
    with pytest.raises(FrozenInstanceError):
        spec.capability_id = "changed"  # type: ignore[misc]


def test_kernel_rejects_invalid_callback_outputs() -> None:
    state = _SyntheticState(value=0)
    command = _command()

    bad_digest = replace(
        _spec(),
        state_digest=lambda state: "not-a-digest",
    )
    with pytest.raises(ValueError):
        digest_capability_state(spec=bad_digest, state=state)

    bad_conflict = replace(
        _spec(),
        retry_conflict_error=lambda message: "not-an-exception",
    )
    first = execute_capability_transition(
        spec=_spec(),
        state=state,
        command=command,
        context={"delta": 1},
    )
    conflicting = _command(payload_value=2)
    with pytest.raises(TypeError):
        execute_capability_transition(
            spec=bad_conflict,
            state=first.state,
            command=conflicting,
            context={"delta": 1},
        )


def test_shared_support_still_has_no_concrete_domain_dependency() -> None:
    source = inspect.getsource(support)

    assert "from astra_runtime.domain." not in source
    assert "import astra_runtime.domain." not in source
    assert "persistent_world_" not in source
    assert "route_command_envelope" not in source
    assert "create_state_delta_envelope" not in source
    assert "create_transaction_preview" not in source
