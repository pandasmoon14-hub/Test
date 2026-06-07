"""Runtime trace skeleton — backend-owned, no trace store or telemetry backend."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Mapping
from types import MappingProxyType


class RuntimeTraceError(Exception):
    """Base error for runtime trace operations."""


class InvalidRuntimeTraceEntryError(RuntimeTraceError):
    """Raised when a runtime trace entry fails validation."""


ALLOWED_TRACE_OPERATION_TYPES = frozenset({
    "schema_registry",
    "record_identity",
    "command_envelope",
    "transaction_preview",
    "state_delta",
    "event_ledger",
    "rng_interface",
    "table_oracle",
    "validation_pipeline",
    "hidden_information",
    "context_projection",
    "persistence_boundary",
    "replay_audit",
    "runtime_trace",
})


@dataclass(frozen=True)
class RuntimeTraceEntry:
    """Immutable runtime trace entry. No trace store or telemetry backend."""

    trace_id: str
    operation_type: str
    subject_ref: str
    sequence: int
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "operation_type": self.operation_type,
            "subject_ref": self.subject_ref,
            "sequence": self.sequence,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def _safe_mapping(
    value: Mapping[str, Any] | None,
    name: str,
    error_cls: type[Exception],
) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise error_cls(f"{name} must be a mapping, got {type(value).__name__}")
    return MappingProxyType(copy.deepcopy(dict(value)))


def _validate_sequence(value: Any, error_cls: type[Exception]) -> int:
    if isinstance(value, bool):
        raise error_cls("sequence must be an integer, not bool")
    if not isinstance(value, int):
        raise error_cls(f"sequence must be an integer, got {type(value).__name__}")
    if value < 0:
        raise error_cls(f"sequence must be non-negative, got {value}")
    return value


def create_runtime_trace_entry(
    *,
    trace_id: str,
    operation_type: str,
    subject_ref: str,
    sequence: int,
    metadata: Mapping[str, Any] | None = None,
) -> RuntimeTraceEntry:
    if not trace_id or not isinstance(trace_id, str):
        raise InvalidRuntimeTraceEntryError("trace_id must be a non-empty string")
    if operation_type not in ALLOWED_TRACE_OPERATION_TYPES:
        raise InvalidRuntimeTraceEntryError(
            f"operation_type must be one of {sorted(ALLOWED_TRACE_OPERATION_TYPES)}, got {operation_type!r}"
        )
    if not subject_ref or not isinstance(subject_ref, str):
        raise InvalidRuntimeTraceEntryError("subject_ref must be a non-empty string")
    seq = _validate_sequence(sequence, InvalidRuntimeTraceEntryError)
    safe_metadata = _safe_mapping(metadata, "metadata", InvalidRuntimeTraceEntryError)
    return RuntimeTraceEntry(
        trace_id=trace_id,
        operation_type=operation_type,
        subject_ref=subject_ref,
        sequence=seq,
        metadata=safe_metadata,
    )


def validate_runtime_trace_entry(obj: object) -> bool:
    if not isinstance(obj, RuntimeTraceEntry):
        raise InvalidRuntimeTraceEntryError(
            f"Expected RuntimeTraceEntry, got {type(obj).__name__}"
        )
    if not obj.trace_id:
        raise InvalidRuntimeTraceEntryError("trace_id must be non-empty")
    if obj.operation_type not in ALLOWED_TRACE_OPERATION_TYPES:
        raise InvalidRuntimeTraceEntryError(
            f"operation_type must be one of {sorted(ALLOWED_TRACE_OPERATION_TYPES)}"
        )
    if not obj.subject_ref:
        raise InvalidRuntimeTraceEntryError("subject_ref must be non-empty")
    if obj.sequence < 0:
        raise InvalidRuntimeTraceEntryError("sequence must be non-negative")
    return True
