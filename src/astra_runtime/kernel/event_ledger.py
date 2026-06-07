"""Event ledger entry skeleton — backend-owned, immutable, no persistence."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.kernel.record_identity import is_valid_record_id


_ALLOWED_EVENT_TYPES = frozenset({
    "command_event",
    "transaction_event",
    "state_delta_event",
    "validation_event",
    "system_audit_event",
})


class EventLedgerError(Exception):
    """Base error for event ledger operations."""


class InvalidEventLedgerEntryError(EventLedgerError):
    """Raised when an event ledger entry fails validation."""


@dataclass(frozen=True)
class EventLedgerEntry:
    """Immutable event ledger entry. No persistence, no replay, no hash."""

    event_id: str
    event_type: str
    sequence: int
    source_command_id: str
    source_preview_id: str
    state_delta_ids: tuple[str, ...] = ()
    actor_ids: tuple[str, ...] = ()
    target_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "sequence": self.sequence,
            "source_command_id": self.source_command_id,
            "source_preview_id": self.source_preview_id,
            "state_delta_ids": list(self.state_delta_ids),
            "actor_ids": list(self.actor_ids),
            "target_ids": list(self.target_ids),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_event_ledger_entry(
    event_id: str,
    event_type: str,
    sequence: int,
    source_command_id: str,
    source_preview_id: str,
    state_delta_ids: Sequence[str] | None = None,
    actor_ids: Sequence[str] | None = None,
    target_ids: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> EventLedgerEntry:
    if not isinstance(event_id, str) or not event_id.strip():
        raise InvalidEventLedgerEntryError("event_id must be a non-empty string")
    if not isinstance(event_type, str) or event_type not in _ALLOWED_EVENT_TYPES:
        raise InvalidEventLedgerEntryError(
            f"event_type must be one of {sorted(_ALLOWED_EVENT_TYPES)}, got: {event_type!r}"
        )
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
        raise InvalidEventLedgerEntryError("sequence must be a non-negative integer")
    if not isinstance(source_command_id, str) or not source_command_id.strip():
        raise InvalidEventLedgerEntryError("source_command_id must be a non-empty string")
    if not isinstance(source_preview_id, str) or not source_preview_id.strip():
        raise InvalidEventLedgerEntryError("source_preview_id must be a non-empty string")

    if state_delta_ids is None:
        safe_delta_ids: tuple[str, ...] = ()
    else:
        for i, did in enumerate(state_delta_ids):
            if not isinstance(did, str) or not did.strip():
                raise InvalidEventLedgerEntryError(
                    f"state_delta_ids[{i}] must be a non-empty string, got: {did!r}"
                )
        safe_delta_ids = tuple(state_delta_ids)

    if actor_ids is None:
        safe_actor_ids: tuple[str, ...] = ()
    else:
        for i, aid in enumerate(actor_ids):
            if not is_valid_record_id(aid):
                raise InvalidEventLedgerEntryError(
                    f"actor_ids[{i}] must be a valid record ID, got: {aid!r}"
                )
        safe_actor_ids = tuple(actor_ids)

    if target_ids is None:
        safe_target_ids: tuple[str, ...] = ()
    else:
        for i, tid in enumerate(target_ids):
            if not is_valid_record_id(tid):
                raise InvalidEventLedgerEntryError(
                    f"target_ids[{i}] must be a valid record ID, got: {tid!r}"
                )
        safe_target_ids = tuple(target_ids)

    if metadata is None:
        safe_metadata: Mapping[str, Any] = MappingProxyType({})
    elif not isinstance(metadata, Mapping):
        raise InvalidEventLedgerEntryError("metadata must be a mapping")
    else:
        safe_metadata = MappingProxyType(copy.deepcopy(dict(metadata)))

    return EventLedgerEntry(
        event_id=event_id,
        event_type=event_type,
        sequence=sequence,
        source_command_id=source_command_id,
        source_preview_id=source_preview_id,
        state_delta_ids=safe_delta_ids,
        actor_ids=safe_actor_ids,
        target_ids=safe_target_ids,
        metadata=safe_metadata,
    )


def validate_event_ledger_entry(obj: Any) -> bool:
    if not isinstance(obj, EventLedgerEntry):
        return False
    if not isinstance(obj.event_id, str) or not obj.event_id.strip():
        return False
    if obj.event_type not in _ALLOWED_EVENT_TYPES:
        return False
    if not isinstance(obj.sequence, int) or isinstance(obj.sequence, bool) or obj.sequence < 0:
        return False
    if not isinstance(obj.source_command_id, str) or not obj.source_command_id.strip():
        return False
    if not isinstance(obj.source_preview_id, str) or not obj.source_preview_id.strip():
        return False
    if not isinstance(obj.state_delta_ids, tuple):
        return False
    if not all(isinstance(d, str) and d.strip() for d in obj.state_delta_ids):
        return False
    if not isinstance(obj.actor_ids, tuple):
        return False
    if not all(is_valid_record_id(a) for a in obj.actor_ids):
        return False
    if not isinstance(obj.target_ids, tuple):
        return False
    if not all(is_valid_record_id(t) for t in obj.target_ids):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True
