"""State delta envelope skeleton — backend-owned, immutable, no state application."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.kernel.record_identity import is_valid_record_id


_ALLOWED_CHANGE_TYPES = frozenset({
    "record_update",
    "record_create",
    "record_remove",
    "relationship_update",
    "visibility_update",
})


class StateDeltaError(Exception):
    """Base error for state delta operations."""


class InvalidStateDeltaError(StateDeltaError):
    """Raised when a state delta envelope fails validation."""


@dataclass(frozen=True)
class StateDeltaEnvelope:
    """Immutable state delta envelope. Backend-owned; no state application, no mutation."""

    delta_id: str
    source_command_id: str
    source_preview_id: str
    affected_record_ids: tuple[str, ...] = ()
    change_type: str = "record_update"
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "delta_id": self.delta_id,
            "source_command_id": self.source_command_id,
            "source_preview_id": self.source_preview_id,
            "affected_record_ids": list(self.affected_record_ids),
            "change_type": self.change_type,
            "payload": copy.deepcopy(dict(self.payload)),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_delta_envelope(
    delta_id: str,
    source_command_id: str,
    source_preview_id: str,
    affected_record_ids: Sequence[str] | None = None,
    change_type: str = "record_update",
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateDeltaEnvelope:
    if not isinstance(delta_id, str) or not delta_id.strip():
        raise InvalidStateDeltaError("delta_id must be a non-empty string")
    if not isinstance(source_command_id, str) or not source_command_id.strip():
        raise InvalidStateDeltaError("source_command_id must be a non-empty string")
    if not isinstance(source_preview_id, str) or not source_preview_id.strip():
        raise InvalidStateDeltaError("source_preview_id must be a non-empty string")

    if not isinstance(change_type, str) or change_type not in _ALLOWED_CHANGE_TYPES:
        raise InvalidStateDeltaError(
            f"change_type must be one of {sorted(_ALLOWED_CHANGE_TYPES)}, got: {change_type!r}"
        )

    if affected_record_ids is None:
        safe_record_ids: tuple[str, ...] = ()
    else:
        for i, rid in enumerate(affected_record_ids):
            if not is_valid_record_id(rid):
                raise InvalidStateDeltaError(
                    f"affected_record_ids[{i}] must be a valid record ID, got: {rid!r}"
                )
        safe_record_ids = tuple(affected_record_ids)

    if payload is None:
        safe_payload: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(payload, Mapping):
        raise InvalidStateDeltaError("payload must be a mapping")
    else:
        safe_payload = MappingProxyType(copy.deepcopy(dict(payload)))

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidStateDeltaError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(copy.deepcopy(dict(metadata)))

    return StateDeltaEnvelope(
        delta_id=delta_id,
        source_command_id=source_command_id,
        source_preview_id=source_preview_id,
        affected_record_ids=safe_record_ids,
        change_type=change_type,
        payload=safe_payload,
        metadata=safe_metadata,
    )


def validate_state_delta_envelope(obj: Any) -> bool:
    if not isinstance(obj, StateDeltaEnvelope):
        return False
    if not isinstance(obj.delta_id, str) or not obj.delta_id.strip():
        return False
    if not isinstance(obj.source_command_id, str) or not obj.source_command_id.strip():
        return False
    if not isinstance(obj.source_preview_id, str) or not obj.source_preview_id.strip():
        return False
    if obj.change_type not in _ALLOWED_CHANGE_TYPES:
        return False
    if not isinstance(obj.affected_record_ids, tuple):
        return False
    if not all(is_valid_record_id(rid) for rid in obj.affected_record_ids):
        return False
    if not isinstance(obj.payload, Mapping):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True
