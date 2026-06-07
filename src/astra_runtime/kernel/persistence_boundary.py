"""Persistence boundary skeleton — backend-owned, no durable persistence."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Mapping
from types import MappingProxyType


class PersistenceBoundaryError(Exception):
    """Base error for persistence boundary operations."""


class InvalidPersistenceBoundaryRequestError(PersistenceBoundaryError):
    """Raised when a persistence boundary request fails validation."""


class InvalidPersistenceBoundaryResultError(PersistenceBoundaryError):
    """Raised when a persistence boundary result fails validation."""


ALLOWED_OPERATION_TYPES = frozenset({
    "record_snapshot_prepare",
    "event_append_prepare",
    "trace_capture_prepare",
    "audit_snapshot_prepare",
})

ALLOWED_RESULT_STATUSES = frozenset({
    "prepared",
    "rejected",
    "quarantined",
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


@dataclass(frozen=True)
class PersistenceBoundaryRequest:
    """Immutable persistence boundary request envelope. No durable persistence."""

    request_id: str
    operation_type: str
    subject_ref: str
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "operation_type": self.operation_type,
            "subject_ref": self.subject_ref,
            "payload": copy.deepcopy(dict(self.payload)),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class PersistenceBoundaryResult:
    """Immutable persistence boundary result envelope. No durable persistence."""

    request_id: str
    operation_type: str
    status: str
    subject_ref: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "operation_type": self.operation_type,
            "status": self.status,
            "subject_ref": self.subject_ref,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_persistence_boundary_request(
    *,
    request_id: str,
    operation_type: str,
    subject_ref: str,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> PersistenceBoundaryRequest:
    _require_non_empty_string(request_id, "request_id", InvalidPersistenceBoundaryRequestError)
    if operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryRequestError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}, got {operation_type!r}"
        )
    _require_non_empty_string(subject_ref, "subject_ref", InvalidPersistenceBoundaryRequestError)
    safe_payload = _safe_mapping(payload, "payload", InvalidPersistenceBoundaryRequestError)
    safe_metadata = _safe_mapping(metadata, "metadata", InvalidPersistenceBoundaryRequestError)
    return PersistenceBoundaryRequest(
        request_id=request_id,
        operation_type=operation_type,
        subject_ref=subject_ref,
        payload=safe_payload,
        metadata=safe_metadata,
    )


def create_persistence_boundary_result(
    *,
    request_id: str,
    operation_type: str,
    status: str,
    subject_ref: str,
    metadata: Mapping[str, Any] | None = None,
) -> PersistenceBoundaryResult:
    _require_non_empty_string(request_id, "request_id", InvalidPersistenceBoundaryResultError)
    if operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryResultError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}, got {operation_type!r}"
        )
    if status not in ALLOWED_RESULT_STATUSES:
        raise InvalidPersistenceBoundaryResultError(
            f"status must be one of {sorted(ALLOWED_RESULT_STATUSES)}, got {status!r}"
        )
    _require_non_empty_string(subject_ref, "subject_ref", InvalidPersistenceBoundaryResultError)
    safe_metadata = _safe_mapping(metadata, "metadata", InvalidPersistenceBoundaryResultError)
    return PersistenceBoundaryResult(
        request_id=request_id,
        operation_type=operation_type,
        status=status,
        subject_ref=subject_ref,
        metadata=safe_metadata,
    )


def validate_persistence_boundary_request(obj: object) -> bool:
    if not isinstance(obj, PersistenceBoundaryRequest):
        raise InvalidPersistenceBoundaryRequestError(
            f"Expected PersistenceBoundaryRequest, got {type(obj).__name__}"
        )
    _require_non_empty_string(obj.request_id, "request_id", InvalidPersistenceBoundaryRequestError)
    if obj.operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryRequestError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}"
        )
    _require_non_empty_string(obj.subject_ref, "subject_ref", InvalidPersistenceBoundaryRequestError)
    _check_is_mapping(obj.payload, "payload", InvalidPersistenceBoundaryRequestError)
    _check_is_mapping(obj.metadata, "metadata", InvalidPersistenceBoundaryRequestError)
    return True


def validate_persistence_boundary_result(obj: object) -> bool:
    if not isinstance(obj, PersistenceBoundaryResult):
        raise InvalidPersistenceBoundaryResultError(
            f"Expected PersistenceBoundaryResult, got {type(obj).__name__}"
        )
    _require_non_empty_string(obj.request_id, "request_id", InvalidPersistenceBoundaryResultError)
    if obj.operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryResultError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}"
        )
    if obj.status not in ALLOWED_RESULT_STATUSES:
        raise InvalidPersistenceBoundaryResultError(
            f"status must be one of {sorted(ALLOWED_RESULT_STATUSES)}"
        )
    _require_non_empty_string(obj.subject_ref, "subject_ref", InvalidPersistenceBoundaryResultError)
    _check_is_mapping(obj.metadata, "metadata", InvalidPersistenceBoundaryResultError)
    return True
