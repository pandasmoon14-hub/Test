"""State store skeleton — immutable state reference surfaces, no mutable state, no persistence."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


STATE_RECORD_CATEGORIES = frozenset({
    "authoritative_runtime",
    "projected",
    "visible",
    "hidden_backend_only",
    "derived",
    "cached_ephemeral",
    "source_local_converted",
    "canon_sourcebook",
    "generated_pending_provenance",
    "persisted_snapshot_boundary",
})

STATE_AUTHORITY_LEVELS = frozenset({
    "authoritative",
    "derived",
    "projected",
    "reference_only",
    "non_authoritative",
    "pending_provenance",
})

_VISIBILITY_TIERS = frozenset({
    "backend_hidden",
    "gm_visible",
    "actor_visible",
    "player_visible",
    "public",
    "redacted",
})


class StateStoreError(Exception):
    """Base error for state store operations."""


class InvalidStateRecordRefError(StateStoreError):
    """Raised when a state record ref fails validation."""


class InvalidStateSnapshotRefError(StateStoreError):
    """Raised when a state snapshot ref fails validation."""


class InvalidStateVisibilityDescriptorError(StateStoreError):
    """Raised when a visibility descriptor fails validation."""


def _require_non_empty(value: Any, name: str, error_cls: type[Exception]) -> None:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string")


def _optional_non_empty(value: Any, name: str, error_cls: type[Exception]) -> None:
    if value is not None:
        _require_non_empty(value, name, error_cls)


def _safe_meta(metadata: Mapping[str, Any] | None, error_cls: type[Exception]) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    return MappingProxyType(copy.deepcopy(dict(metadata)))


@dataclass(frozen=True)
class StateVisibilityDescriptor:
    visibility_id: str
    visibility_tier: str
    hidden_info_safe: bool
    player_visible: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "visibility_id": self.visibility_id,
            "visibility_tier": self.visibility_tier,
            "hidden_info_safe": self.hidden_info_safe,
            "player_visible": self.player_visible,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_visibility_descriptor(
    visibility_id: str,
    visibility_tier: str,
    hidden_info_safe: bool,
    player_visible: bool,
    metadata: Mapping[str, Any] | None = None,
) -> StateVisibilityDescriptor:
    _require_non_empty(visibility_id, "visibility_id", InvalidStateVisibilityDescriptorError)
    if visibility_tier not in _VISIBILITY_TIERS:
        raise InvalidStateVisibilityDescriptorError(
            f"visibility_tier must be one of {sorted(_VISIBILITY_TIERS)}, got: {visibility_tier!r}"
        )
    if not isinstance(hidden_info_safe, bool):
        raise InvalidStateVisibilityDescriptorError("hidden_info_safe must be a bool")
    if not isinstance(player_visible, bool):
        raise InvalidStateVisibilityDescriptorError("player_visible must be a bool")
    safe_meta = _safe_meta(metadata, InvalidStateVisibilityDescriptorError)
    return StateVisibilityDescriptor(
        visibility_id=visibility_id,
        visibility_tier=visibility_tier,
        hidden_info_safe=hidden_info_safe,
        player_visible=player_visible,
        metadata=safe_meta,
    )


def validate_state_visibility_descriptor(obj: Any) -> bool:
    if not isinstance(obj, StateVisibilityDescriptor):
        return False
    if not isinstance(obj.visibility_id, str) or not obj.visibility_id.strip():
        return False
    if obj.visibility_tier not in _VISIBILITY_TIERS:
        return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if not isinstance(obj.player_visible, bool):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True)
class StateRecordRef:
    state_ref_id: str
    record_id: str
    record_type: str
    category: str
    authority_level: str
    visibility: StateVisibilityDescriptor
    schema_id: str | None
    source_event_id: str | None
    source_delta_id: str | None
    provenance_id: str | None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_ref_id": self.state_ref_id,
            "record_id": self.record_id,
            "record_type": self.record_type,
            "category": self.category,
            "authority_level": self.authority_level,
            "visibility": self.visibility.to_dict(),
            "schema_id": self.schema_id,
            "source_event_id": self.source_event_id,
            "source_delta_id": self.source_delta_id,
            "provenance_id": self.provenance_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_record_ref(
    state_ref_id: str,
    record_id: str,
    record_type: str,
    category: str,
    authority_level: str,
    visibility: StateVisibilityDescriptor,
    schema_id: str | None = None,
    source_event_id: str | None = None,
    source_delta_id: str | None = None,
    provenance_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateRecordRef:
    _require_non_empty(state_ref_id, "state_ref_id", InvalidStateRecordRefError)
    _require_non_empty(record_id, "record_id", InvalidStateRecordRefError)
    _require_non_empty(record_type, "record_type", InvalidStateRecordRefError)
    if category not in STATE_RECORD_CATEGORIES:
        raise InvalidStateRecordRefError(
            f"category must be one of {sorted(STATE_RECORD_CATEGORIES)}, got: {category!r}"
        )
    if authority_level not in STATE_AUTHORITY_LEVELS:
        raise InvalidStateRecordRefError(
            f"authority_level must be one of {sorted(STATE_AUTHORITY_LEVELS)}, got: {authority_level!r}"
        )
    if not isinstance(visibility, StateVisibilityDescriptor):
        raise InvalidStateRecordRefError("visibility must be a StateVisibilityDescriptor")
    _optional_non_empty(schema_id, "schema_id", InvalidStateRecordRefError)
    _optional_non_empty(source_event_id, "source_event_id", InvalidStateRecordRefError)
    _optional_non_empty(source_delta_id, "source_delta_id", InvalidStateRecordRefError)
    _optional_non_empty(provenance_id, "provenance_id", InvalidStateRecordRefError)
    safe_meta = _safe_meta(metadata, InvalidStateRecordRefError)
    return StateRecordRef(
        state_ref_id=state_ref_id,
        record_id=record_id,
        record_type=record_type,
        category=category,
        authority_level=authority_level,
        visibility=visibility,
        schema_id=schema_id,
        source_event_id=source_event_id,
        source_delta_id=source_delta_id,
        provenance_id=provenance_id,
        metadata=safe_meta,
    )


def validate_state_record_ref(obj: Any) -> bool:
    if not isinstance(obj, StateRecordRef):
        return False
    if not isinstance(obj.state_ref_id, str) or not obj.state_ref_id.strip():
        return False
    if not isinstance(obj.record_id, str) or not obj.record_id.strip():
        return False
    if not isinstance(obj.record_type, str) or not obj.record_type.strip():
        return False
    if obj.category not in STATE_RECORD_CATEGORIES:
        return False
    if obj.authority_level not in STATE_AUTHORITY_LEVELS:
        return False
    if not isinstance(obj.visibility, StateVisibilityDescriptor):
        return False
    if not validate_state_visibility_descriptor(obj.visibility):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True)
class StateSnapshotRef:
    snapshot_id: str
    snapshot_scope: str
    state_ref_ids: tuple[str, ...]
    authority_level: str
    source_event_id: str | None
    replay_audit_id: str | None
    persistence_boundary_id: str | None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "snapshot_scope": self.snapshot_scope,
            "state_ref_ids": list(self.state_ref_ids),
            "authority_level": self.authority_level,
            "source_event_id": self.source_event_id,
            "replay_audit_id": self.replay_audit_id,
            "persistence_boundary_id": self.persistence_boundary_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_snapshot_ref(
    snapshot_id: str,
    snapshot_scope: str,
    state_ref_ids: Sequence[str],
    authority_level: str,
    source_event_id: str | None = None,
    replay_audit_id: str | None = None,
    persistence_boundary_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateSnapshotRef:
    _require_non_empty(snapshot_id, "snapshot_id", InvalidStateSnapshotRefError)
    _require_non_empty(snapshot_scope, "snapshot_scope", InvalidStateSnapshotRefError)
    if isinstance(state_ref_ids, str):
        raise InvalidStateSnapshotRefError("state_ref_ids must not be a bare string")
    if not isinstance(state_ref_ids, Sequence):
        raise InvalidStateSnapshotRefError("state_ref_ids must be a sequence")
    safe_ids: list[str] = []
    for i, ref_id in enumerate(state_ref_ids):
        if not isinstance(ref_id, str) or not ref_id.strip():
            raise InvalidStateSnapshotRefError(f"state_ref_ids[{i}] must be a non-empty string")
        safe_ids.append(ref_id)
    if authority_level not in STATE_AUTHORITY_LEVELS:
        raise InvalidStateSnapshotRefError(
            f"authority_level must be one of {sorted(STATE_AUTHORITY_LEVELS)}, got: {authority_level!r}"
        )
    _optional_non_empty(source_event_id, "source_event_id", InvalidStateSnapshotRefError)
    _optional_non_empty(replay_audit_id, "replay_audit_id", InvalidStateSnapshotRefError)
    _optional_non_empty(persistence_boundary_id, "persistence_boundary_id", InvalidStateSnapshotRefError)
    safe_meta = _safe_meta(metadata, InvalidStateSnapshotRefError)
    return StateSnapshotRef(
        snapshot_id=snapshot_id,
        snapshot_scope=snapshot_scope,
        state_ref_ids=tuple(safe_ids),
        authority_level=authority_level,
        source_event_id=source_event_id,
        replay_audit_id=replay_audit_id,
        persistence_boundary_id=persistence_boundary_id,
        metadata=safe_meta,
    )


def validate_state_snapshot_ref(obj: Any) -> bool:
    if not isinstance(obj, StateSnapshotRef):
        return False
    if not isinstance(obj.snapshot_id, str) or not obj.snapshot_id.strip():
        return False
    if not isinstance(obj.snapshot_scope, str) or not obj.snapshot_scope.strip():
        return False
    if not isinstance(obj.state_ref_ids, tuple):
        return False
    for ref_id in obj.state_ref_ids:
        if not isinstance(ref_id, str) or not ref_id.strip():
            return False
    if obj.authority_level not in STATE_AUTHORITY_LEVELS:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


class StateStoreService:
    """Stateless wrapper around state store creation/validation helpers."""

    def create_record_ref(self, **kwargs: Any) -> StateRecordRef:
        return create_state_record_ref(**kwargs)

    def create_snapshot_ref(self, **kwargs: Any) -> StateSnapshotRef:
        return create_state_snapshot_ref(**kwargs)

    def validate_record_ref(self, obj: Any) -> bool:
        return validate_state_record_ref(obj)

    def validate_snapshot_ref(self, obj: Any) -> bool:
        return validate_state_snapshot_ref(obj)
