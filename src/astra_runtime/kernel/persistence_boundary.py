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


def create_persistence_boundary_request(
    *,
    request_id: str,
    operation_type: str,
    subject_ref: str,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> PersistenceBoundaryRequest:
    if not request_id or not isinstance(request_id, str):
        raise InvalidPersistenceBoundaryRequestError("request_id must be a non-empty string")
    if operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryRequestError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}, got {operation_type!r}"
        )
    if not subject_ref or not isinstance(subject_ref, str):
        raise InvalidPersistenceBoundaryRequestError("subject_ref must be a non-empty string")
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
    if not request_id or not isinstance(request_id, str):
        raise InvalidPersistenceBoundaryResultError("request_id must be a non-empty string")
    if operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryResultError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}, got {operation_type!r}"
        )
    if status not in ALLOWED_RESULT_STATUSES:
        raise InvalidPersistenceBoundaryResultError(
            f"status must be one of {sorted(ALLOWED_RESULT_STATUSES)}, got {status!r}"
        )
    if not subject_ref or not isinstance(subject_ref, str):
        raise InvalidPersistenceBoundaryResultError("subject_ref must be a non-empty string")
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
    if not obj.request_id:
        raise InvalidPersistenceBoundaryRequestError("request_id must be non-empty")
    if obj.operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryRequestError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}"
        )
    if not obj.subject_ref:
        raise InvalidPersistenceBoundaryRequestError("subject_ref must be non-empty")
    return True


def validate_persistence_boundary_result(obj: object) -> bool:
    if not isinstance(obj, PersistenceBoundaryResult):
        raise InvalidPersistenceBoundaryResultError(
            f"Expected PersistenceBoundaryResult, got {type(obj).__name__}"
        )
    if not obj.request_id:
        raise InvalidPersistenceBoundaryResultError("request_id must be non-empty")
    if obj.operation_type not in ALLOWED_OPERATION_TYPES:
        raise InvalidPersistenceBoundaryResultError(
            f"operation_type must be one of {sorted(ALLOWED_OPERATION_TYPES)}"
        )
    if obj.status not in ALLOWED_RESULT_STATUSES:
        raise InvalidPersistenceBoundaryResultError(
            f"status must be one of {sorted(ALLOWED_RESULT_STATUSES)}"
        )
    if not obj.subject_ref:
        raise InvalidPersistenceBoundaryResultError("subject_ref must be non-empty")
    return True
