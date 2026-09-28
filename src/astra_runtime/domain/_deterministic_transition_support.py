"""Shared technical helpers for bounded deterministic transitions.

This module centralizes repeated transition mechanics that are independent of
world-domain meaning. It owns no movement, custody, object-state, storage,
opportunity, qualification, or persistence semantics.

Domain modules remain responsible for command vocabulary, evidence meaning,
legality, state derivation, mutation, receipts, replay reducers, and semantic
ownership. These helpers only provide deterministic command fingerprinting and
committed-transition identity lookup/comparison.
"""

from __future__ import annotations

import hashlib
import json
from typing import Protocol, Sequence, TypeVar

from astra_runtime.kernel.command_envelope import CommandEnvelope


class CommittedTransitionIdentity(Protocol):
    """Minimum technical identity required for retry lookup."""

    command_id: str
    command_fingerprint: str


_TTransition = TypeVar("_TTransition", bound=CommittedTransitionIdentity)


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
