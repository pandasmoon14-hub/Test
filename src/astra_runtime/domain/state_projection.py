"""State projection skeleton — immutable projection request/result surfaces, no state fetch, no mutation."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.state_store import (
    STATE_AUTHORITY_LEVELS,
    StateRecordRef,
    StateSnapshotRef,
)

_VISIBILITY_TIERS = frozenset({
    "backend_hidden",
    "gm_visible",
    "actor_visible",
    "player_visible",
    "public",
    "redacted",
})

STATE_PROJECTION_TYPES = frozenset({
    "full_backend",
    "player_visible",
    "actor_scoped",
    "scene_scoped",
    "faction_social",
    "combat_encounter",
    "inventory_asset",
    "mission_clue",
    "hidden_info_redacted",
    "audit_provenance",
    "model_facing_candidate",
    "ui_client_candidate",
})

STATE_PROJECTION_STATUSES = frozenset({
    "requested",
    "validated",
    "materialized",
    "redacted",
    "rejected",
    "quarantined",
})

_BACKEND_HIDDEN_FORBIDDEN_TYPES = frozenset({
    "player_visible",
    "actor_scoped",
    "model_facing_candidate",
    "ui_client_candidate",
})

_ALLOWED_DEPENDENCY_TYPES = frozenset({
    "state_record_ref",
    "state_snapshot_ref",
    "hidden_information",
    "context_projection",
    "validation_result",
    "runtime_trace",
    "persistence_boundary",
    "replay_audit",
    "transaction_lifecycle",
    "event_ledger",
    "command_lifecycle",
    "model_evaluation",
    "live_play_gate",
})


class StateProjectionError(Exception):
    """Base error for state projection operations."""


class InvalidStateProjectionRequestError(StateProjectionError):
    """Raised when a projection request fails validation."""


class InvalidStateProjectionResultError(StateProjectionError):
    """Raised when a projection result fails validation."""


class InvalidStateProjectionDependencyError(StateProjectionError):
    """Raised when a projection dependency fails validation."""


class InvalidStateProjectionRejectionError(StateProjectionError):
    """Raised when a projection rejection fails validation."""


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


def _safe_str_seq(value: Any, name: str, error_cls: type[Exception]) -> tuple[str, ...]:
    if isinstance(value, str):
        raise error_cls(f"{name} must not be a bare string")
    if value is None:
        return ()
    if not isinstance(value, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[str] = []
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise error_cls(f"{name}[{i}] must be a non-empty string")
        result.append(item)
    return tuple(result)


@dataclass(frozen=True)
class StateProjectionDependency:
    dependency_id: str
    dependency_type: str
    required: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "dependency_id": self.dependency_id,
            "dependency_type": self.dependency_type,
            "required": self.required,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_projection_dependency(
    dependency_id: str,
    dependency_type: str,
    required: bool,
    metadata: Mapping[str, Any] | None = None,
) -> StateProjectionDependency:
    _require_non_empty(dependency_id, "dependency_id", InvalidStateProjectionDependencyError)
    if dependency_type not in _ALLOWED_DEPENDENCY_TYPES:
        raise InvalidStateProjectionDependencyError(
            f"dependency_type must be one of {sorted(_ALLOWED_DEPENDENCY_TYPES)}, got: {dependency_type!r}"
        )
    if not isinstance(required, bool):
        raise InvalidStateProjectionDependencyError("required must be a bool")
    safe_meta = _safe_meta(metadata, InvalidStateProjectionDependencyError)
    return StateProjectionDependency(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        required=required,
        metadata=safe_meta,
    )


def validate_state_projection_dependency(obj: Any) -> bool:
    if not isinstance(obj, StateProjectionDependency):
        return False
    if not isinstance(obj.dependency_id, str) or not obj.dependency_id.strip():
        return False
    if obj.dependency_type not in _ALLOWED_DEPENDENCY_TYPES:
        return False
    if not isinstance(obj.required, bool):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True)
class StateProjectionRejection:
    rejection_id: str
    reason_code: str
    message: str
    hidden_info_safe: bool
    player_visible: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "rejection_id": self.rejection_id,
            "reason_code": self.reason_code,
            "message": self.message,
            "hidden_info_safe": self.hidden_info_safe,
            "player_visible": self.player_visible,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_projection_rejection(
    rejection_id: str,
    reason_code: str,
    message: str,
    hidden_info_safe: bool,
    player_visible: bool,
    metadata: Mapping[str, Any] | None = None,
) -> StateProjectionRejection:
    _require_non_empty(rejection_id, "rejection_id", InvalidStateProjectionRejectionError)
    _require_non_empty(reason_code, "reason_code", InvalidStateProjectionRejectionError)
    _require_non_empty(message, "message", InvalidStateProjectionRejectionError)
    if not isinstance(hidden_info_safe, bool):
        raise InvalidStateProjectionRejectionError("hidden_info_safe must be a bool")
    if not isinstance(player_visible, bool):
        raise InvalidStateProjectionRejectionError("player_visible must be a bool")
    safe_meta = _safe_meta(metadata, InvalidStateProjectionRejectionError)
    return StateProjectionRejection(
        rejection_id=rejection_id,
        reason_code=reason_code,
        message=message,
        hidden_info_safe=hidden_info_safe,
        player_visible=player_visible,
        metadata=safe_meta,
    )


def validate_state_projection_rejection(obj: Any) -> bool:
    if not isinstance(obj, StateProjectionRejection):
        return False
    if not isinstance(obj.rejection_id, str) or not obj.rejection_id.strip():
        return False
    if not isinstance(obj.reason_code, str) or not obj.reason_code.strip():
        return False
    if not isinstance(obj.message, str) or not obj.message.strip():
        return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if not isinstance(obj.player_visible, bool):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True)
class StateProjectionRequest:
    projection_request_id: str
    requester_id: str
    projection_type: str
    state_ref_ids: tuple[str, ...]
    snapshot_id: str | None
    visibility_tier: str
    include_backend_hidden: bool
    dependencies: tuple[StateProjectionDependency, ...]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_request_id": self.projection_request_id,
            "requester_id": self.requester_id,
            "projection_type": self.projection_type,
            "state_ref_ids": list(self.state_ref_ids),
            "snapshot_id": self.snapshot_id,
            "visibility_tier": self.visibility_tier,
            "include_backend_hidden": self.include_backend_hidden,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_projection_request(
    projection_request_id: str,
    requester_id: str,
    projection_type: str,
    state_ref_ids: Sequence[str],
    visibility_tier: str,
    include_backend_hidden: bool,
    snapshot_id: str | None = None,
    dependencies: Sequence[StateProjectionDependency] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateProjectionRequest:
    _require_non_empty(projection_request_id, "projection_request_id", InvalidStateProjectionRequestError)
    _require_non_empty(requester_id, "requester_id", InvalidStateProjectionRequestError)
    if projection_type not in STATE_PROJECTION_TYPES:
        raise InvalidStateProjectionRequestError(
            f"projection_type must be one of {sorted(STATE_PROJECTION_TYPES)}, got: {projection_type!r}"
        )
    safe_ref_ids = _safe_str_seq(state_ref_ids, "state_ref_ids", InvalidStateProjectionRequestError)
    if visibility_tier not in _VISIBILITY_TIERS:
        raise InvalidStateProjectionRequestError(
            f"visibility_tier must be one of {sorted(_VISIBILITY_TIERS)}, got: {visibility_tier!r}"
        )
    if not isinstance(include_backend_hidden, bool):
        raise InvalidStateProjectionRequestError("include_backend_hidden must be a bool")
    if include_backend_hidden and projection_type in _BACKEND_HIDDEN_FORBIDDEN_TYPES:
        raise InvalidStateProjectionRequestError(
            f"include_backend_hidden must be False for projection_type {projection_type!r}"
        )
    _optional_non_empty(snapshot_id, "snapshot_id", InvalidStateProjectionRequestError)
    if dependencies is None:
        safe_deps: tuple[StateProjectionDependency, ...] = ()
    elif isinstance(dependencies, str):
        raise InvalidStateProjectionRequestError("dependencies must not be a string")
    else:
        for i, dep in enumerate(dependencies):
            if not isinstance(dep, StateProjectionDependency):
                raise InvalidStateProjectionRequestError(
                    f"dependencies[{i}] must be a StateProjectionDependency"
                )
        safe_deps = tuple(dependencies)
    safe_meta = _safe_meta(metadata, InvalidStateProjectionRequestError)
    return StateProjectionRequest(
        projection_request_id=projection_request_id,
        requester_id=requester_id,
        projection_type=projection_type,
        state_ref_ids=safe_ref_ids,
        snapshot_id=snapshot_id,
        visibility_tier=visibility_tier,
        include_backend_hidden=include_backend_hidden,
        dependencies=safe_deps,
        metadata=safe_meta,
    )


def validate_state_projection_request(obj: Any) -> bool:
    if not isinstance(obj, StateProjectionRequest):
        return False
    if not isinstance(obj.projection_request_id, str) or not obj.projection_request_id.strip():
        return False
    if not isinstance(obj.requester_id, str) or not obj.requester_id.strip():
        return False
    if obj.projection_type not in STATE_PROJECTION_TYPES:
        return False
    if not isinstance(obj.state_ref_ids, tuple):
        return False
    if obj.visibility_tier not in _VISIBILITY_TIERS:
        return False
    if not isinstance(obj.include_backend_hidden, bool):
        return False
    if not isinstance(obj.dependencies, tuple):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True)
class StateProjectionResult:
    projection_id: str
    projection_request_id: str
    projection_type: str
    status: str
    state_ref_ids: tuple[str, ...]
    redacted_state_ref_ids: tuple[str, ...]
    visible_state_ref_ids: tuple[str, ...]
    rejection: StateProjectionRejection | None
    validation_id: str | None
    trace_id: str | None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_id": self.projection_id,
            "projection_request_id": self.projection_request_id,
            "projection_type": self.projection_type,
            "status": self.status,
            "state_ref_ids": list(self.state_ref_ids),
            "redacted_state_ref_ids": list(self.redacted_state_ref_ids),
            "visible_state_ref_ids": list(self.visible_state_ref_ids),
            "rejection": self.rejection.to_dict() if self.rejection is not None else None,
            "validation_id": self.validation_id,
            "trace_id": self.trace_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_state_projection_result(
    projection_id: str,
    projection_request_id: str,
    projection_type: str,
    status: str,
    state_ref_ids: Sequence[str] | None = None,
    redacted_state_ref_ids: Sequence[str] | None = None,
    visible_state_ref_ids: Sequence[str] | None = None,
    rejection: StateProjectionRejection | None = None,
    validation_id: str | None = None,
    trace_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateProjectionResult:
    _require_non_empty(projection_id, "projection_id", InvalidStateProjectionResultError)
    _require_non_empty(projection_request_id, "projection_request_id", InvalidStateProjectionResultError)
    if projection_type not in STATE_PROJECTION_TYPES:
        raise InvalidStateProjectionResultError(
            f"projection_type must be one of {sorted(STATE_PROJECTION_TYPES)}, got: {projection_type!r}"
        )
    if status not in STATE_PROJECTION_STATUSES:
        raise InvalidStateProjectionResultError(
            f"status must be one of {sorted(STATE_PROJECTION_STATUSES)}, got: {status!r}"
        )
    safe_ref_ids = _safe_str_seq(state_ref_ids, "state_ref_ids", InvalidStateProjectionResultError)
    safe_redacted = _safe_str_seq(redacted_state_ref_ids, "redacted_state_ref_ids", InvalidStateProjectionResultError)
    safe_visible = _safe_str_seq(visible_state_ref_ids, "visible_state_ref_ids", InvalidStateProjectionResultError)
    if rejection is not None and not isinstance(rejection, StateProjectionRejection):
        raise InvalidStateProjectionResultError("rejection must be None or a StateProjectionRejection")
    _optional_non_empty(validation_id, "validation_id", InvalidStateProjectionResultError)
    _optional_non_empty(trace_id, "trace_id", InvalidStateProjectionResultError)
    safe_meta = _safe_meta(metadata, InvalidStateProjectionResultError)
    return StateProjectionResult(
        projection_id=projection_id,
        projection_request_id=projection_request_id,
        projection_type=projection_type,
        status=status,
        state_ref_ids=safe_ref_ids,
        redacted_state_ref_ids=safe_redacted,
        visible_state_ref_ids=safe_visible,
        rejection=rejection,
        validation_id=validation_id,
        trace_id=trace_id,
        metadata=safe_meta,
    )


def validate_state_projection_result(obj: Any) -> bool:
    if not isinstance(obj, StateProjectionResult):
        return False
    if not isinstance(obj.projection_id, str) or not obj.projection_id.strip():
        return False
    if not isinstance(obj.projection_request_id, str) or not obj.projection_request_id.strip():
        return False
    if obj.projection_type not in STATE_PROJECTION_TYPES:
        return False
    if obj.status not in STATE_PROJECTION_STATUSES:
        return False
    if not isinstance(obj.state_ref_ids, tuple):
        return False
    if not isinstance(obj.redacted_state_ref_ids, tuple):
        return False
    if not isinstance(obj.visible_state_ref_ids, tuple):
        return False
    if obj.rejection is not None and not isinstance(obj.rejection, StateProjectionRejection):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def project_state_view(
    projection_id: str,
    request: StateProjectionRequest,
    *,
    status: str = "materialized",
    visible_state_ref_ids: Sequence[str] | None = None,
    redacted_state_ref_ids: Sequence[str] | None = None,
    rejection: StateProjectionRejection | None = None,
    validation_id: str | None = None,
    trace_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateProjectionResult:
    if not validate_state_projection_request(request):
        raise InvalidStateProjectionRequestError("request must be a valid StateProjectionRequest")
    return create_state_projection_result(
        projection_id=projection_id,
        projection_request_id=request.projection_request_id,
        projection_type=request.projection_type,
        status=status,
        state_ref_ids=list(request.state_ref_ids),
        redacted_state_ref_ids=redacted_state_ref_ids,
        visible_state_ref_ids=visible_state_ref_ids,
        rejection=rejection,
        validation_id=validation_id,
        trace_id=trace_id,
        metadata=metadata,
    )


class StateProjectionService:
    """Stateless wrapper around state projection creation/validation helpers."""

    def create_request(self, **kwargs: Any) -> StateProjectionRequest:
        return create_state_projection_request(**kwargs)

    def create_result(self, **kwargs: Any) -> StateProjectionResult:
        return create_state_projection_result(**kwargs)

    def validate_request(self, obj: Any) -> bool:
        return validate_state_projection_request(obj)

    def validate_result(self, obj: Any) -> bool:
        return validate_state_projection_result(obj)

    def project(
        self,
        projection_id: str,
        request: StateProjectionRequest,
        **kwargs: Any,
    ) -> StateProjectionResult:
        return project_state_view(projection_id, request, **kwargs)
