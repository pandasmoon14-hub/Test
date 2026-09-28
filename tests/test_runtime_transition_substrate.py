from __future__ import annotations

import hashlib
import inspect
import json
import math
from dataclasses import dataclass

import pytest

import astra_runtime.domain._deterministic_transition_support as support
from astra_runtime.domain._deterministic_transition_support import (
    command_fingerprint_matches,
    find_committed_transition,
    fingerprint_command_envelope,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    InvalidPersistentWorldMovementRequestError,
    fingerprint_persistent_world_movement_command,
)
from astra_runtime.domain.persistent_world_object_custody_transfer import (
    InvalidPersistentWorldObjectCustodyRequestError,
    fingerprint_persistent_world_object_custody_command,
)
from astra_runtime.domain.persistent_world_object_lit_state import (
    fingerprint_persistent_world_object_lit_state_command,
)
from astra_runtime.domain.persistent_world_object_open_close import (
    fingerprint_persistent_world_object_open_close_command,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    fingerprint_persistent_world_object_storage_command,
)
from astra_runtime.kernel.command_envelope import create_command_envelope


@dataclass(frozen=True)
class _FakeCommittedTransition:
    command_id: str
    command_fingerprint: str


def _command(*, payload: dict[str, object] | None = None):
    return create_command_envelope(
        command_id="transition-support-test-001",
        command_type="bounded_test",
        source_actor_id="astra:entity:transition-support-actor",
        payload=payload or {"z": 2, "a": 1},
        metadata={"client": "transition-support-test"},
    )


def _legacy_fingerprint(command, *, allow_nan: bool) -> str:
    canonical = json.dumps(
        command.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=allow_nan,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def test_shared_fingerprint_preserves_existing_canonical_material() -> None:
    command = _command()

    assert fingerprint_command_envelope(
        command,
        allow_nan=False,
    ) == _legacy_fingerprint(command, allow_nan=False)

    assert fingerprint_command_envelope(
        command,
        allow_nan=True,
    ) == _legacy_fingerprint(command, allow_nan=True)


def test_nan_policy_remains_selected_by_domain_wrapper() -> None:
    command = _command(payload={"value": math.nan})

    assert fingerprint_persistent_world_movement_command(
        command
    ) == _legacy_fingerprint(command, allow_nan=True)

    with pytest.raises(InvalidPersistentWorldObjectCustodyRequestError):
        fingerprint_persistent_world_object_custody_command(command)

    with pytest.raises(ValueError):
        fingerprint_persistent_world_object_open_close_command(command)

    with pytest.raises(ValueError):
        fingerprint_persistent_world_object_lit_state_command(command)

    with pytest.raises(ValueError):
        fingerprint_persistent_world_object_storage_command(command)


def test_current_domain_wrappers_preserve_normal_command_fingerprint() -> None:
    command = _command()
    expected = _legacy_fingerprint(command, allow_nan=False)

    assert fingerprint_persistent_world_movement_command(command) == expected
    assert fingerprint_persistent_world_object_custody_command(command) == expected
    assert fingerprint_persistent_world_object_open_close_command(command) == expected
    assert fingerprint_persistent_world_object_lit_state_command(command) == expected
    assert fingerprint_persistent_world_object_storage_command(command) == expected


def test_committed_transition_lookup_is_identity_only() -> None:
    first = _FakeCommittedTransition(
        command_id="command-001",
        command_fingerprint="a" * 64,
    )
    second = _FakeCommittedTransition(
        command_id="command-002",
        command_fingerprint="b" * 64,
    )

    assert find_committed_transition((first, second), "command-002") is second
    assert find_committed_transition((first, second), "command-003") is None


def test_command_fingerprint_match_does_not_interpret_domain_semantics() -> None:
    transition = _FakeCommittedTransition(
        command_id="command-001",
        command_fingerprint="c" * 64,
    )

    assert command_fingerprint_matches(transition, "c" * 64)
    assert not command_fingerprint_matches(transition, "d" * 64)


def test_support_module_has_no_domain_dependency_or_semantic_owner() -> None:
    source = inspect.getsource(support)

    assert "from astra_runtime.domain." not in source
    assert "semantic_owner" not in source
    assert "qualification" not in source
    assert "opportunity" not in source
