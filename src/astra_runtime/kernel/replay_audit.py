"""Replay/hash audit skeleton — backend-owned, no replay engine or hash-chain service."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from types import MappingProxyType


class ReplayAuditError(Exception):
    """Base error for replay/hash audit operations."""


class InvalidReplayAuditRecordError(ReplayAuditError):
    """Raised when a replay audit record fails validation."""


class InvalidHashAuditRecordError(ReplayAuditError):
    """Raised when a hash audit record fails validation."""


ALLOWED_HASH_ALGORITHMS = frozenset({"sha256"})


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
class ReplayAuditRecord:
    """Immutable replay audit record. No replay engine or event replay."""

    replay_id: str
    source_ref: str
    sequence: int
    expected_hash: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "replay_id": self.replay_id,
            "source_ref": self.source_ref,
            "sequence": self.sequence,
            "expected_hash": self.expected_hash,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class HashAuditRecord:
    """Immutable hash audit record. No hash-chain enforcement engine."""

    hash_id: str
    source_ref: str
    hash_algorithm: str
    payload_hash: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "hash_id": self.hash_id,
            "source_ref": self.source_ref,
            "hash_algorithm": self.hash_algorithm,
            "payload_hash": self.payload_hash,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_replay_audit_record(
    *,
    replay_id: str,
    source_ref: str,
    sequence: int,
    expected_hash: str,
    metadata: Mapping[str, Any] | None = None,
) -> ReplayAuditRecord:
    _require_non_empty_string(replay_id, "replay_id", InvalidReplayAuditRecordError)
    _require_non_empty_string(source_ref, "source_ref", InvalidReplayAuditRecordError)
    seq = _validate_sequence(sequence, InvalidReplayAuditRecordError)
    _require_non_empty_string(expected_hash, "expected_hash", InvalidReplayAuditRecordError)
    safe_metadata = _safe_mapping(metadata, "metadata", InvalidReplayAuditRecordError)
    return ReplayAuditRecord(
        replay_id=replay_id,
        source_ref=source_ref,
        sequence=seq,
        expected_hash=expected_hash,
        metadata=safe_metadata,
    )


def create_hash_audit_record(
    *,
    hash_id: str,
    source_ref: str,
    hash_algorithm: str,
    payload_hash: str,
    metadata: Mapping[str, Any] | None = None,
) -> HashAuditRecord:
    _require_non_empty_string(hash_id, "hash_id", InvalidHashAuditRecordError)
    _require_non_empty_string(source_ref, "source_ref", InvalidHashAuditRecordError)
    if hash_algorithm not in ALLOWED_HASH_ALGORITHMS:
        raise InvalidHashAuditRecordError(
            f"hash_algorithm must be one of {sorted(ALLOWED_HASH_ALGORITHMS)}, got {hash_algorithm!r}"
        )
    _require_non_empty_string(payload_hash, "payload_hash", InvalidHashAuditRecordError)
    safe_metadata = _safe_mapping(metadata, "metadata", InvalidHashAuditRecordError)
    return HashAuditRecord(
        hash_id=hash_id,
        source_ref=source_ref,
        hash_algorithm=hash_algorithm,
        payload_hash=payload_hash,
        metadata=safe_metadata,
    )


def validate_replay_audit_record(obj: object) -> bool:
    if not isinstance(obj, ReplayAuditRecord):
        raise InvalidReplayAuditRecordError(
            f"Expected ReplayAuditRecord, got {type(obj).__name__}"
        )
    _require_non_empty_string(obj.replay_id, "replay_id", InvalidReplayAuditRecordError)
    _require_non_empty_string(obj.source_ref, "source_ref", InvalidReplayAuditRecordError)
    _validate_sequence(obj.sequence, InvalidReplayAuditRecordError)
    _require_non_empty_string(obj.expected_hash, "expected_hash", InvalidReplayAuditRecordError)
    _check_is_mapping(obj.metadata, "metadata", InvalidReplayAuditRecordError)
    return True


def validate_hash_audit_record(obj: object) -> bool:
    if not isinstance(obj, HashAuditRecord):
        raise InvalidHashAuditRecordError(
            f"Expected HashAuditRecord, got {type(obj).__name__}"
        )
    _require_non_empty_string(obj.hash_id, "hash_id", InvalidHashAuditRecordError)
    _require_non_empty_string(obj.source_ref, "source_ref", InvalidHashAuditRecordError)
    if obj.hash_algorithm not in ALLOWED_HASH_ALGORITHMS:
        raise InvalidHashAuditRecordError(
            f"hash_algorithm must be one of {sorted(ALLOWED_HASH_ALGORITHMS)}"
        )
    _require_non_empty_string(obj.payload_hash, "payload_hash", InvalidHashAuditRecordError)
    _check_is_mapping(obj.metadata, "metadata", InvalidHashAuditRecordError)
    return True


def canonical_payload_hash(
    payload: Mapping[str, Any] | Sequence[Any] | str | int | float | bool | None,
    *,
    algorithm: str = "sha256",
) -> str:
    if algorithm not in ALLOWED_HASH_ALGORITHMS:
        raise ReplayAuditError(
            f"Unsupported hash algorithm: {algorithm!r}; supported: {sorted(ALLOWED_HASH_ALGORITHMS)}"
        )
    try:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    except (TypeError, ValueError) as exc:
        raise ReplayAuditError(f"Payload is not JSON-serializable: {exc}") from exc
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
