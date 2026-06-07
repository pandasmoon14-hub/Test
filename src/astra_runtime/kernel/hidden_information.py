"""Hidden-information partition skeleton — backend-owned, no hidden-state database."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from types import MappingProxyType

from astra_runtime.kernel.record_identity import is_valid_record_id, InvalidRecordIdError


class HiddenInformationError(Exception):
    """Base error for hidden-information operations."""


class InvalidHiddenInformationRecordError(HiddenInformationError):
    """Raised when a hidden-information record fails validation."""


class VisibilityTierError(HiddenInformationError):
    """Raised when a visibility tier is invalid."""


ALLOWED_VISIBILITY_TIERS = frozenset({
    "public",
    "player_visible",
    "restricted",
    "backend_hidden",
    "redacted",
})


@dataclass(frozen=True)
class HiddenInformationRecord:
    """Immutable hidden-information record. Backend-owned; no hidden-state database."""

    record_id: str
    visibility_tier: str
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    redaction_label: str = ""
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "visibility_tier": self.visibility_tier,
            "payload": copy.deepcopy(dict(self.payload)),
            "redaction_label": self.redaction_label,
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
        raise error_cls(f"{name} must be a mapping")
    return MappingProxyType(copy.deepcopy(dict(value)))


def create_hidden_information_record(
    record_id: str,
    visibility_tier: str,
    redaction_label: str,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> HiddenInformationRecord:
    if not isinstance(record_id, str) or not record_id.strip():
        raise InvalidHiddenInformationRecordError("record_id must be a non-empty string")
    if not is_valid_record_id(record_id):
        raise InvalidHiddenInformationRecordError(f"record_id is not a valid record ID: {record_id!r}")
    if visibility_tier not in ALLOWED_VISIBILITY_TIERS:
        raise VisibilityTierError(
            f"visibility_tier must be one of {sorted(ALLOWED_VISIBILITY_TIERS)}, got: {visibility_tier!r}"
        )
    if not isinstance(redaction_label, str) or not redaction_label.strip():
        raise InvalidHiddenInformationRecordError("redaction_label must be a non-empty string")
    safe_payload = _safe_mapping(payload, "payload", InvalidHiddenInformationRecordError)
    safe_meta = _safe_mapping(metadata, "metadata", InvalidHiddenInformationRecordError)
    return HiddenInformationRecord(
        record_id=record_id,
        visibility_tier=visibility_tier,
        payload=safe_payload,
        redaction_label=redaction_label,
        metadata=safe_meta,
    )


def validate_hidden_information_record(obj: Any) -> bool:
    if not isinstance(obj, HiddenInformationRecord):
        return False
    if not isinstance(obj.record_id, str) or not obj.record_id.strip():
        return False
    if not is_valid_record_id(obj.record_id):
        return False
    if obj.visibility_tier not in ALLOWED_VISIBILITY_TIERS:
        return False
    if not isinstance(obj.redaction_label, str) or not obj.redaction_label.strip():
        return False
    if not isinstance(obj.payload, Mapping):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def is_visible_to_tiers(
    record: HiddenInformationRecord,
    allowed_tiers: Sequence[str],
) -> bool:
    return record.visibility_tier in allowed_tiers


def redacted_copy(record: HiddenInformationRecord) -> HiddenInformationRecord:
    return HiddenInformationRecord(
        record_id=record.record_id,
        visibility_tier=record.visibility_tier,
        payload=MappingProxyType({}),
        redaction_label=record.redaction_label,
        metadata=MappingProxyType(copy.deepcopy(dict(record.metadata))),
    )
