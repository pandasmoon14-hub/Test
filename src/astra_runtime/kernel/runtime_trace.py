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


def _require_non_empty_string(
    value: object,
    name: str,
    error_cls: type[Exception],
) -> str:
    if not isinstance(value, str):
        raise error_cls(f"{name} must be a string, got {type(value).__name__}")
    if not value.strip():
        raise error_cls(f"{name} must be a non-empty string (whitespace-only not allowed)")
    return value


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


def _check_is_mapping(
    value: object,
    name: str,
    error_cls: type[Exception],
) -> None:
    if not isinstance(value, Mapping):
        raise error_cls(f"{name} must be a mapping, got {type(value).__name__}")


def _validate_sequence(value: Any, error_cls: type[Exception]) -> int:
    if isinstance(value, bool):
        raise error_cls("sequence must be an integer, not bool")
    if not isinstance(value, int):
        raise error_cls(f"sequence must be an integer, got {type(value).__name__}")
    if value < 0:
        raise error_cls(f"sequence must be non-negative, got {value}")
    return value


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


def create_runtime_trace_entry(
    *,
    trace_id: str,
    operation_type: str,
    subject_ref: str,
    sequence: int,
    metadata: Mapping[str, Any] | None = None,
) -> RuntimeTraceEntry:
    _require_non_empty_string(trace_id, "trace_id", InvalidRuntimeTraceEntryError)
    if operation_type not in ALLOWED_TRACE_OPERATION_TYPES:
        raise InvalidRuntimeTraceEntryError(
            f"operation_type must be one of {sorted(ALLOWED_TRACE_OPERATION_TYPES)}, got {operation_type!r}"
        )
    _require_non_empty_string(subject_ref, "subject_ref", InvalidRuntimeTraceEntryError)
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
    _require_non_empty_string(obj.trace_id, "trace_id", InvalidRuntimeTraceEntryError)
    if obj.operation_type not in ALLOWED_TRACE_OPERATION_TYPES:
        raise InvalidRuntimeTraceEntryError(
            f"operation_type must be one of {sorted(ALLOWED_TRACE_OPERATION_TYPES)}"
        )
    _require_non_empty_string(obj.subject_ref, "subject_ref", InvalidRuntimeTraceEntryError)
    _validate_sequence(obj.sequence, InvalidRuntimeTraceEntryError)
    _check_is_mapping(obj.metadata, "metadata", InvalidRuntimeTraceEntryError)
    return True
