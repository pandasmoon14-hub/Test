"""Shared technical helpers for bounded deterministic transitions.

This module centralizes repeated transition mechanics that are independent of
world-domain meaning. It owns no movement, custody, object-state, storage,
opportunity, qualification, persistence, or replay semantics.

Domain modules remain responsible for command vocabulary, evidence meaning,
legality, state derivation, mutation, receipts, replay reducers, checkpoint
meaning, and semantic ownership. These helpers provide deterministic command
fingerprinting, committed-transition identity lookup/comparison, and an
immutable callback-driven lifecycle shell that can sequence already-owned
capability behavior without becoming a semantic super-owner.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Mapping, Protocol, Sequence, TypeVar

from astra_runtime.kernel.command_envelope import CommandEnvelope


class CommittedTransitionIdentity(Protocol):
    """Minimum technical identity required for retry lookup."""

    command_id: str
    command_fingerprint: str


class PreparedTransitionIdentity(Protocol):
    """Minimum immutable identity required from a prepared transition."""

    command_id: str
    command_fingerprint: str


_TTransition = TypeVar("_TTransition", bound=CommittedTransitionIdentity)
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def fingerprint_command_envelope(
    command: CommandEnvelope,
    *,
    allow_nan: bool,
) -> str:
    """Return the canonical SHA-256 fingerprint for an already-validated command.

    Validation and domain-specific error translation intentionally remain with
    the calling domain so this helper does not acquire command-legality
    ownership.
    """

    canonical = json.dumps(
        command.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=allow_nan,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def find_committed_transition(
    transitions: Sequence[_TTransition],
    command_id: str,
) -> _TTransition | None:
    """Find a committed transition by immutable command identity."""

    for transition in transitions:
        if transition.command_id == command_id:
            return transition
    return None


def command_fingerprint_matches(
    transition: CommittedTransitionIdentity,
    command_fingerprint: str,
) -> bool:
    """Return whether a committed transition has the same command meaning."""

    return transition.command_fingerprint == command_fingerprint


@dataclass(frozen=True, kw_only=True)
class TransitionCapabilitySpec:
    """Immutable wiring for one already-owned deterministic capability.

    The callbacks remain owned by the declaring capability. Listing semantic
    owners here is descriptive provenance only; it grants this technical
    helper no authority over those semantics.
    """

    capability_id: str
    semantic_owners: tuple[str, ...]
    state_type: type
    replay_state_type: type
    receipt_prefix: str
    state_digest: Callable[[object], str]
    fingerprint_command: Callable[[CommandEnvelope], str]
    committed_transitions: Callable[
        [object], Sequence[CommittedTransitionIdentity]
    ]
    prepare_new_transition: Callable[
        [object, CommandEnvelope, Mapping[str, object]],
        PreparedTransitionIdentity,
    ]
    commit_new_transition: Callable[
        [object, PreparedTransitionIdentity],
        object,
    ]
    build_retry_result: Callable[
        [object, CommittedTransitionIdentity],
        object,
    ]
    retry_conflict_error: Callable[[str], Exception]
    replay_committed_transition: Callable[[object, object], object]

    def __post_init__(self) -> None:
        if not isinstance(self.capability_id, str) or not self.capability_id.strip():
            raise ValueError("capability_id must be a non-empty string")
        if (
            not isinstance(self.semantic_owners, tuple)
            or not self.semantic_owners
            or any(
                not isinstance(owner, str) or not owner.strip()
                for owner in self.semantic_owners
            )
            or len(self.semantic_owners) != len(set(self.semantic_owners))
        ):
            raise ValueError(
                "semantic_owners must be a non-empty tuple of unique strings"
            )
        if not isinstance(self.state_type, type):
            raise TypeError("state_type must be a type")
        if not isinstance(self.replay_state_type, type):
            raise TypeError("replay_state_type must be a type")
        if not isinstance(self.receipt_prefix, str) or not self.receipt_prefix.strip():
            raise ValueError("receipt_prefix must be a non-empty string")
        for name in (
            "state_digest",
            "fingerprint_command",
            "committed_transitions",
            "prepare_new_transition",
            "commit_new_transition",
            "build_retry_result",
            "retry_conflict_error",
            "replay_committed_transition",
        ):
            if not callable(getattr(self, name)):
                raise TypeError(f"{name} must be callable")


def _require_capability_state(
    spec: TransitionCapabilitySpec,
    state: object,
) -> None:
    if not isinstance(spec, TransitionCapabilitySpec):
        raise TypeError("spec must be TransitionCapabilitySpec")
    if not isinstance(state, spec.state_type):
        raise TypeError(
            f"{spec.capability_id} state must be {spec.state_type.__name__}"
        )


def _require_replay_state(
    spec: TransitionCapabilitySpec,
    state: object,
) -> None:
    if not isinstance(spec, TransitionCapabilitySpec):
        raise TypeError("spec must be TransitionCapabilitySpec")
    if not isinstance(state, spec.replay_state_type):
        raise TypeError(
            f"{spec.capability_id} replay state must be "
            f"{spec.replay_state_type.__name__}"
        )


def _require_sha256(value: object, *, name: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{name} must be a lowercase SHA-256 digest")
    return value


def digest_capability_state(
    *,
    spec: TransitionCapabilitySpec,
    state: object,
) -> str:
    """Return the declaring capability's own authoritative state digest."""

    _require_capability_state(spec, state)
    return _require_sha256(
        spec.state_digest(state),
        name=f"{spec.capability_id} state digest",
    )


def fingerprint_capability_command(
    *,
    spec: TransitionCapabilitySpec,
    command: CommandEnvelope,
) -> str:
    """Return the capability-owned canonical command fingerprint."""

    if not isinstance(spec, TransitionCapabilitySpec):
        raise TypeError("spec must be TransitionCapabilitySpec")
    if not isinstance(command, CommandEnvelope):
        raise TypeError("command must be CommandEnvelope")
    return _require_sha256(
        spec.fingerprint_command(command),
        name=f"{spec.capability_id} command fingerprint",
    )


def _capability_existing_transition(
    *,
    spec: TransitionCapabilitySpec,
    state: object,
    command_id: str,
) -> CommittedTransitionIdentity | None:
    transitions = spec.committed_transitions(state)
    return find_committed_transition(transitions, command_id)


def _capability_retry_result_or_none(
    *,
    spec: TransitionCapabilitySpec,
    state: object,
    command_id: str,
    command_fingerprint: str,
) -> object | None:
    existing = _capability_existing_transition(
        spec=spec,
        state=state,
        command_id=command_id,
    )
    if existing is None:
        return None
    if not command_fingerprint_matches(existing, command_fingerprint):
        error = spec.retry_conflict_error(
            "command ID already committed with different immutable meaning"
        )
        if not isinstance(error, Exception):
            raise TypeError("retry_conflict_error must return an Exception")
        raise error
    return spec.build_retry_result(state, existing)


def prepare_capability_transition(
    *,
    spec: TransitionCapabilitySpec,
    state: object,
    command: CommandEnvelope,
    context: Mapping[str, object] | None = None,
) -> PreparedTransitionIdentity:
    """Delegate semantic preparation while preserving immutable command identity."""

    _require_capability_state(spec, state)
    fingerprint = fingerprint_capability_command(spec=spec, command=command)
    context_view: Mapping[str, object] = MappingProxyType(
        dict(context or {})
    )
    prepared = spec.prepare_new_transition(state, command, context_view)
    if not hasattr(prepared, "command_id") or not hasattr(
        prepared, "command_fingerprint"
    ):
        raise TypeError(
            "prepare_new_transition must return command identity fields"
        )
    if prepared.command_id != command.command_id:
        raise ValueError("prepared transition changed command identity")
    if prepared.command_fingerprint != fingerprint:
        raise ValueError("prepared transition changed command fingerprint")
    return prepared


def commit_prepared_capability_transition(
    *,
    spec: TransitionCapabilitySpec,
    state: object,
    prepared: PreparedTransitionIdentity,
) -> object:
    """Commit one prepared transition or return its idempotent retry result."""

    _require_capability_state(spec, state)
    if not hasattr(prepared, "command_id") or not hasattr(
        prepared, "command_fingerprint"
    ):
        raise TypeError("prepared transition lacks immutable command identity")
    command_fingerprint = _require_sha256(
        prepared.command_fingerprint,
        name=f"{spec.capability_id} prepared command fingerprint",
    )
    retry = _capability_retry_result_or_none(
        spec=spec,
        state=state,
        command_id=prepared.command_id,
        command_fingerprint=command_fingerprint,
    )
    if retry is not None:
        return retry
    return spec.commit_new_transition(state, prepared)


def execute_capability_transition(
    *,
    spec: TransitionCapabilitySpec,
    state: object,
    command: CommandEnvelope,
    context: Mapping[str, object] | None = None,
) -> object:
    """Run retry check -> semantic prepare -> semantic commit deterministically."""

    _require_capability_state(spec, state)
    fingerprint = fingerprint_capability_command(spec=spec, command=command)
    retry = _capability_retry_result_or_none(
        spec=spec,
        state=state,
        command_id=command.command_id,
        command_fingerprint=fingerprint,
    )
    if retry is not None:
        return retry
    prepared = prepare_capability_transition(
        spec=spec,
        state=state,
        command=command,
        context=context,
    )
    return commit_prepared_capability_transition(
        spec=spec,
        state=state,
        prepared=prepared,
    )


def replay_capability_transition(
    *,
    spec: TransitionCapabilitySpec,
    pre_state: object,
    receipt: object,
) -> object:
    """Delegate committed replay without interpreting domain receipt meaning."""

    _require_replay_state(spec, pre_state)
    return spec.replay_committed_transition(pre_state, receipt)
