"""Context projection skeleton — backend-owned, no context-packet compiler."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from types import MappingProxyType

from astra_runtime.kernel.record_identity import is_valid_record_id
from astra_runtime.kernel.hidden_information import (
    ALLOWED_VISIBILITY_TIERS,
    HiddenInformationRecord,
    is_visible_to_tiers,
)


class ContextProjectionError(Exception):
    """Base error for context projection operations."""


class InvalidContextProjectionItemError(ContextProjectionError):
    """Raised when a context projection item fails validation."""


class InvalidContextProjectionError(ContextProjectionError):
    """Raised when a context projection fails validation."""


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


@dataclass(frozen=True)
class ContextProjectionItem:
    """Immutable context projection item. Backend-owned; no context-packet compiler."""

    record_id: str
    visibility_tier: str
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    redacted: bool = False
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "visibility_tier": self.visibility_tier,
            "payload": copy.deepcopy(dict(self.payload)),
            "redacted": self.redacted,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class ContextProjection:
    """Immutable context projection. Backend-owned; no context-packet compiler."""

    projection_id: str
    subject_ref: str
    allowed_visibility_tiers: tuple[str, ...] = ()
    items: tuple[ContextProjectionItem, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_id": self.projection_id,
            "subject_ref": self.subject_ref,
            "allowed_visibility_tiers": list(self.allowed_visibility_tiers),
            "items": [item.to_dict() for item in self.items],
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_context_projection_item(
    record_id: str,
    visibility_tier: str,
    redacted: bool,
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ContextProjectionItem:
    if not isinstance(record_id, str) or not record_id.strip():
        raise InvalidContextProjectionItemError("record_id must be a non-empty string")
    if not is_valid_record_id(record_id):
        raise InvalidContextProjectionItemError(f"record_id is not a valid record ID: {record_id!r}")
    if visibility_tier not in ALLOWED_VISIBILITY_TIERS:
        raise InvalidContextProjectionItemError(
            f"visibility_tier must be one of {sorted(ALLOWED_VISIBILITY_TIERS)}, got: {visibility_tier!r}"
        )
    if not isinstance(redacted, bool):
        raise InvalidContextProjectionItemError("redacted must be a bool")
    safe_payload = _safe_mapping(payload, "payload", InvalidContextProjectionItemError)
    safe_meta = _safe_mapping(metadata, "metadata", InvalidContextProjectionItemError)
    return ContextProjectionItem(
        record_id=record_id,
        visibility_tier=visibility_tier,
        payload=safe_payload,
        redacted=redacted,
        metadata=safe_meta,
    )


def create_context_projection(
    projection_id: str,
    subject_ref: str,
    allowed_visibility_tiers: Sequence[str],
    items: Sequence[ContextProjectionItem] = (),
    metadata: Mapping[str, Any] | None = None,
) -> ContextProjection:
    if not isinstance(projection_id, str) or not projection_id.strip():
        raise InvalidContextProjectionError("projection_id must be a non-empty string")
    if not isinstance(subject_ref, str) or not subject_ref.strip():
        raise InvalidContextProjectionError("subject_ref must be a non-empty string")
    for i, tier in enumerate(allowed_visibility_tiers):
        if tier not in ALLOWED_VISIBILITY_TIERS:
            raise InvalidContextProjectionError(
                f"allowed_visibility_tiers[{i}] must be one of {sorted(ALLOWED_VISIBILITY_TIERS)}, got: {tier!r}"
            )
    for i, item in enumerate(items):
        if not isinstance(item, ContextProjectionItem):
            raise InvalidContextProjectionError(
                f"items[{i}] must be a ContextProjectionItem, got: {type(item).__name__}"
            )
    safe_meta = _safe_mapping(metadata, "metadata", InvalidContextProjectionError)
    return ContextProjection(
        projection_id=projection_id,
        subject_ref=subject_ref,
        allowed_visibility_tiers=tuple(allowed_visibility_tiers),
        items=tuple(items),
        metadata=safe_meta,
    )


def validate_context_projection_item(obj: Any) -> bool:
    if not isinstance(obj, ContextProjectionItem):
        return False
    if not isinstance(obj.record_id, str) or not obj.record_id.strip():
        return False
    if not is_valid_record_id(obj.record_id):
        return False
    if obj.visibility_tier not in ALLOWED_VISIBILITY_TIERS:
        return False
    if not isinstance(obj.redacted, bool):
        return False
    if not isinstance(obj.payload, Mapping):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_context_projection(obj: Any) -> bool:
    if not isinstance(obj, ContextProjection):
        return False
    if not isinstance(obj.projection_id, str) or not obj.projection_id.strip():
        return False
    if not isinstance(obj.subject_ref, str) or not obj.subject_ref.strip():
        return False
    if not isinstance(obj.allowed_visibility_tiers, tuple):
        return False
    for tier in obj.allowed_visibility_tiers:
        if tier not in ALLOWED_VISIBILITY_TIERS:
            return False
    if not isinstance(obj.items, tuple):
        return False
    for item in obj.items:
        if not isinstance(item, ContextProjectionItem):
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def project_hidden_records(
    projection_id: str,
    subject_ref: str,
    records: Sequence[HiddenInformationRecord],
    allowed_visibility_tiers: Sequence[str],
    metadata: Mapping[str, Any] | None = None,
) -> ContextProjection:
    if not isinstance(projection_id, str) or not projection_id.strip():
        raise InvalidContextProjectionError("projection_id must be a non-empty string")
    if not isinstance(subject_ref, str) or not subject_ref.strip():
        raise InvalidContextProjectionError("subject_ref must be a non-empty string")
    for i, tier in enumerate(allowed_visibility_tiers):
        if tier not in ALLOWED_VISIBILITY_TIERS:
            raise InvalidContextProjectionError(
                f"allowed_visibility_tiers[{i}] must be one of {sorted(ALLOWED_VISIBILITY_TIERS)}, got: {tier!r}"
            )

    items: list[ContextProjectionItem] = []
    for i, record in enumerate(records):
        if not isinstance(record, HiddenInformationRecord):
            raise InvalidContextProjectionError(
                f"records[{i}] must be a HiddenInformationRecord, got: {type(record).__name__}"
            )
        if is_visible_to_tiers(record, allowed_visibility_tiers):
            items.append(ContextProjectionItem(
                record_id=record.record_id,
                visibility_tier=record.visibility_tier,
                payload=MappingProxyType(copy.deepcopy(dict(record.payload))),
                redacted=False,
                metadata=MappingProxyType(copy.deepcopy(dict(record.metadata))),
            ))
        else:
            items.append(ContextProjectionItem(
                record_id=record.record_id,
                visibility_tier=record.visibility_tier,
                payload=MappingProxyType({}),
                redacted=True,
                metadata=MappingProxyType(copy.deepcopy(dict(record.metadata))),
            ))

    safe_meta = _safe_mapping(metadata, "metadata", InvalidContextProjectionError)
    return ContextProjection(
        projection_id=projection_id,
        subject_ref=subject_ref,
        allowed_visibility_tiers=tuple(allowed_visibility_tiers),
        items=tuple(items),
        metadata=safe_meta,
    )
