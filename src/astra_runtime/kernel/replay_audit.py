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


def create_replay_audit_record(
    *,
    replay_id: str,
    source_ref: str,
    sequence: int,
    expected_hash: str,
    metadata: Mapping[str, Any] | None = None,
) -> ReplayAuditRecord:
    if not replay_id or not isinstance(replay_id, str):
        raise InvalidReplayAuditRecordError("replay_id must be a non-empty string")
    if not source_ref or not isinstance(source_ref, str):
        raise InvalidReplayAuditRecordError("source_ref must be a non-empty string")
    seq = _validate_sequence(sequence, InvalidReplayAuditRecordError)
    if not expected_hash or not isinstance(expected_hash, str):
        raise InvalidReplayAuditRecordError("expected_hash must be a non-empty string")
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
    if not hash_id or not isinstance(hash_id, str):
        raise InvalidHashAuditRecordError("hash_id must be a non-empty string")
    if not source_ref or not isinstance(source_ref, str):
        raise InvalidHashAuditRecordError("source_ref must be a non-empty string")
    if hash_algorithm not in ALLOWED_HASH_ALGORITHMS:
        raise InvalidHashAuditRecordError(
            f"hash_algorithm must be one of {sorted(ALLOWED_HASH_ALGORITHMS)}, got {hash_algorithm!r}"
        )
    if not payload_hash or not isinstance(payload_hash, str):
        raise InvalidHashAuditRecordError("payload_hash must be a non-empty string")
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
    if not obj.replay_id:
        raise InvalidReplayAuditRecordError("replay_id must be non-empty")
    if not obj.source_ref:
        raise InvalidReplayAuditRecordError("source_ref must be non-empty")
    if obj.sequence < 0:
        raise InvalidReplayAuditRecordError("sequence must be non-negative")
    if not obj.expected_hash:
        raise InvalidReplayAuditRecordError("expected_hash must be non-empty")
    return True


def validate_hash_audit_record(obj: object) -> bool:
    if not isinstance(obj, HashAuditRecord):
        raise InvalidHashAuditRecordError(
            f"Expected HashAuditRecord, got {type(obj).__name__}"
        )
    if not obj.hash_id:
        raise InvalidHashAuditRecordError("hash_id must be non-empty")
    if not obj.source_ref:
        raise InvalidHashAuditRecordError("source_ref must be non-empty")
    if obj.hash_algorithm not in ALLOWED_HASH_ALGORITHMS:
        raise InvalidHashAuditRecordError(
            f"hash_algorithm must be one of {sorted(ALLOWED_HASH_ALGORITHMS)}"
        )
    if not obj.payload_hash:
        raise InvalidHashAuditRecordError("payload_hash must be non-empty")
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
