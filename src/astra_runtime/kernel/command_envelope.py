"""Command envelope skeleton — backend-owned, immutable, no execution."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.kernel.record_identity import is_valid_record_id


class CommandEnvelopeError(Exception):
    """Base error for command envelope operations."""


class InvalidCommandEnvelopeError(CommandEnvelopeError):
    """Raised when a command envelope fails validation."""


@dataclass(frozen=True)
class CommandEnvelope:
    """Immutable command envelope. Backend-owned; no execution, no state mutation."""

    command_id: str
    command_type: str
    source_actor_id: str
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "command_type": self.command_type,
            "source_actor_id": self.source_actor_id,
            "payload": copy.deepcopy(dict(self.payload)),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_command_envelope(
    command_id: str,
    command_type: str,
    source_actor_id: str,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CommandEnvelope:
    if not isinstance(command_id, str) or not command_id.strip():
        raise InvalidCommandEnvelopeError("command_id must be a non-empty string")
    if not isinstance(command_type, str) or not command_type.strip():
        raise InvalidCommandEnvelopeError("command_type must be a non-empty string")
    if not is_valid_record_id(source_actor_id):
        raise InvalidCommandEnvelopeError(
            f"source_actor_id must be a valid record ID, got: {source_actor_id!r}"
        )

    if payload is None:
        safe_payload: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(payload, Mapping):
        raise InvalidCommandEnvelopeError("payload must be a mapping")
    else:
        safe_payload = MappingProxyType(copy.deepcopy(dict(payload)))

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidCommandEnvelopeError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(copy.deepcopy(dict(metadata)))

    return CommandEnvelope(
        command_id=command_id,
        command_type=command_type,
        source_actor_id=source_actor_id,
        payload=safe_payload,
        metadata=safe_metadata,
    )


def validate_command_envelope(obj: Any) -> bool:
    if not isinstance(obj, CommandEnvelope):
        return False
    if not isinstance(obj.command_id, str) or not obj.command_id.strip():
        return False
    if not isinstance(obj.command_type, str) or not obj.command_type.strip():
        return False
    if not is_valid_record_id(obj.source_actor_id):
        return False
    if not isinstance(obj.payload, Mapping):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True
