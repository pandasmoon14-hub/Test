"""Event commitment skeleton — immutable event commitment surfaces, no event append, no state mutation."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


EVENT_COMMITMENT_DECISIONS = frozenset({
    "commit_ready",
    "committed",
    "rejected_by_validation",
    "rejected_by_scope",
    "rejected_by_missing_state_reference",
    "rejected_by_missing_delta_reference",
    "rejected_by_hidden_information_risk",
    "rejected_by_idempotency_conflict",
    "rejected_by_persistence_boundary",
    "quarantined_for_audit",
    "cancelled_before_commit",
    "unsupported_event_type",
})

EVENT_COMMITMENT_STATUSES = frozenset({
    "requested",
    "validated",
    "commit_ready",
    "committed",
    "rejected",
    "quarantined",
    "cancelled",
})

EVENT_COMMITMENT_DEPENDENCY_TYPES = frozenset({
    "transaction_ref",
    "command_envelope_ref",
    "actor_ref",
    "state_record_ref",
    "state_snapshot_ref",
    "state_projection_ref",
    "state_delta_ref",
    "validation_result_ref",
    "event_ledger_ref",
    "hidden_information_ref",
    "context_projection_ref",
    "runtime_trace_ref",
    "persistence_boundary_ref",
    "replay_audit_ref",
    "idempotency_key_ref",
})

_REJECTION_DECISIONS = frozenset({
    "rejected_by_validation",
    "rejected_by_scope",
    "rejected_by_missing_state_reference",
    "rejected_by_missing_delta_reference",
    "rejected_by_hidden_information_risk",
    "rejected_by_idempotency_conflict",
    "rejected_by_persistence_boundary",
    "quarantined_for_audit",
    "cancelled_before_commit",
    "unsupported_event_type",
})


class EventCommitmentError(Exception):
    """Base error for event commitment operations."""


class InvalidEventCommitmentDependencyError(EventCommitmentError):
    """Raised when an event commitment dependency fails validation."""


class InvalidEventCommitmentRequestError(EventCommitmentError):
    """Raised when an event commitment request fails validation."""


class InvalidEventCommitmentResultError(EventCommitmentError):
    """Raised when an event commitment result fails validation."""


class InvalidEventCommitmentRejectionError(EventCommitmentError):
    """Raised when an event commitment rejection fails validation."""


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
    if isinstance(value, (str, bytes)):
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
class EventCommitmentDependency:
    dependency_id: str
    dependency_type: str
    reference_id: str
    required: bool = True
    satisfied: bool = False
    hidden_info_safe: bool = True
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "dependency_id": self.dependency_id,
            "dependency_type": self.dependency_type,
            "reference_id": self.reference_id,
            "required": self.required,
            "satisfied": self.satisfied,
            "hidden_info_safe": self.hidden_info_safe,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class EventCommitmentRejection:
    rejection_id: str
    decision: str
    reason: str
    blocking: bool = True
    hidden_info_safe: bool = True
    player_visible: bool = False
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "rejection_id": self.rejection_id,
            "decision": self.decision,
            "reason": self.reason,
            "blocking": self.blocking,
            "hidden_info_safe": self.hidden_info_safe,
            "player_visible": self.player_visible,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class EventCommitmentRequest:
    commitment_request_id: str
    transaction_id: str
    event_type: str
    state_ref_ids: tuple[str, ...]
    proposed_delta_ref_ids: tuple[str, ...]
    validation_ref_id: str
    trace_id: str
    idempotency_key: str | None = None
    dependencies: tuple[EventCommitmentDependency, ...] = ()
    allow_event_ledger_append: bool = False
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "commitment_request_id": self.commitment_request_id,
            "transaction_id": self.transaction_id,
            "event_type": self.event_type,
            "state_ref_ids": list(self.state_ref_ids),
            "proposed_delta_ref_ids": list(self.proposed_delta_ref_ids),
            "validation_ref_id": self.validation_ref_id,
            "trace_id": self.trace_id,
            "idempotency_key": self.idempotency_key,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "allow_event_ledger_append": self.allow_event_ledger_append,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class EventCommitmentResult:
    commitment_request_id: str
    decision: str
    status: str
    committed_event_ref_id: str | None = None
    event_ledger_ref_id: str | None = None
    state_delta_applied: bool = False
    event_ledger_appended: bool = False
    rejection: EventCommitmentRejection | None = None
    quarantined: bool = False
    cancelled: bool = False
    hidden_info_safe: bool = True
    trace_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "commitment_request_id": self.commitment_request_id,
            "decision": self.decision,
            "status": self.status,
            "committed_event_ref_id": self.committed_event_ref_id,
            "event_ledger_ref_id": self.event_ledger_ref_id,
            "state_delta_applied": self.state_delta_applied,
            "event_ledger_appended": self.event_ledger_appended,
            "rejection": self.rejection.to_dict() if self.rejection is not None else None,
            "quarantined": self.quarantined,
            "cancelled": self.cancelled,
            "hidden_info_safe": self.hidden_info_safe,
            "trace_id": self.trace_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_event_commitment_dependency(
    dependency_id: str,
    dependency_type: str,
    reference_id: str,
    required: bool = True,
    satisfied: bool = False,
    hidden_info_safe: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> EventCommitmentDependency:
    _require_non_empty(dependency_id, "dependency_id", InvalidEventCommitmentDependencyError)
    if dependency_type not in EVENT_COMMITMENT_DEPENDENCY_TYPES:
        raise InvalidEventCommitmentDependencyError(
            f"dependency_type must be one of {sorted(EVENT_COMMITMENT_DEPENDENCY_TYPES)}, got: {dependency_type!r}"
        )
    _require_non_empty(reference_id, "reference_id", InvalidEventCommitmentDependencyError)
    if not isinstance(required, bool):
        raise InvalidEventCommitmentDependencyError("required must be a bool")
    if not isinstance(satisfied, bool):
        raise InvalidEventCommitmentDependencyError("satisfied must be a bool")
    if not isinstance(hidden_info_safe, bool):
        raise InvalidEventCommitmentDependencyError("hidden_info_safe must be a bool")
    safe_meta = _safe_meta(metadata, InvalidEventCommitmentDependencyError)
    return EventCommitmentDependency(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        reference_id=reference_id,
        required=required,
        satisfied=satisfied,
        hidden_info_safe=hidden_info_safe,
        metadata=safe_meta,
    )


def create_event_commitment_rejection(
    rejection_id: str,
    decision: str,
    reason: str,
    blocking: bool = True,
    hidden_info_safe: bool = True,
    player_visible: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> EventCommitmentRejection:
    _require_non_empty(rejection_id, "rejection_id", InvalidEventCommitmentRejectionError)
    if decision not in EVENT_COMMITMENT_DECISIONS:
        raise InvalidEventCommitmentRejectionError(
            f"decision must be one of {sorted(EVENT_COMMITMENT_DECISIONS)}, got: {decision!r}"
        )
    if decision not in _REJECTION_DECISIONS:
        raise InvalidEventCommitmentRejectionError(
            f"decision must be a rejection/quarantine/cancel decision, got: {decision!r}"
        )
    _require_non_empty(reason, "reason", InvalidEventCommitmentRejectionError)
    if not isinstance(blocking, bool):
        raise InvalidEventCommitmentRejectionError("blocking must be a bool")
    if not isinstance(hidden_info_safe, bool):
        raise InvalidEventCommitmentRejectionError("hidden_info_safe must be a bool")
    if not isinstance(player_visible, bool):
        raise InvalidEventCommitmentRejectionError("player_visible must be a bool")
    if player_visible and not hidden_info_safe:
        raise InvalidEventCommitmentRejectionError(
            "hidden_info_safe must be True when player_visible is True"
        )
    safe_meta = _safe_meta(metadata, InvalidEventCommitmentRejectionError)
    return EventCommitmentRejection(
        rejection_id=rejection_id,
        decision=decision,
        reason=reason,
        blocking=blocking,
        hidden_info_safe=hidden_info_safe,
        player_visible=player_visible,
        metadata=safe_meta,
    )


def create_event_commitment_request(
    commitment_request_id: str,
    transaction_id: str,
    event_type: str,
    state_ref_ids: Sequence[str],
    proposed_delta_ref_ids: Sequence[str],
    validation_ref_id: str,
    trace_id: str,
    idempotency_key: str | None = None,
    dependencies: Sequence[EventCommitmentDependency] | None = None,
    allow_event_ledger_append: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> EventCommitmentRequest:
    _require_non_empty(commitment_request_id, "commitment_request_id", InvalidEventCommitmentRequestError)
    _require_non_empty(transaction_id, "transaction_id", InvalidEventCommitmentRequestError)
    _require_non_empty(event_type, "event_type", InvalidEventCommitmentRequestError)
    safe_state_refs = _safe_str_seq(state_ref_ids, "state_ref_ids", InvalidEventCommitmentRequestError)
    if len(safe_state_refs) == 0:
        raise InvalidEventCommitmentRequestError("state_ref_ids must be non-empty")
    safe_delta_refs = _safe_str_seq(proposed_delta_ref_ids, "proposed_delta_ref_ids", InvalidEventCommitmentRequestError)
    if len(safe_delta_refs) == 0:
        raise InvalidEventCommitmentRequestError("proposed_delta_ref_ids must be non-empty")
    _require_non_empty(validation_ref_id, "validation_ref_id", InvalidEventCommitmentRequestError)
    _require_non_empty(trace_id, "trace_id", InvalidEventCommitmentRequestError)
    _optional_non_empty(idempotency_key, "idempotency_key", InvalidEventCommitmentRequestError)
    if dependencies is None:
        safe_deps: tuple[EventCommitmentDependency, ...] = ()
    elif isinstance(dependencies, (str, bytes)):
        raise InvalidEventCommitmentRequestError("dependencies must not be a string")
    else:
        for i, dep in enumerate(dependencies):
            if not isinstance(dep, EventCommitmentDependency):
                raise InvalidEventCommitmentRequestError(
                    f"dependencies[{i}] must be an EventCommitmentDependency"
                )
        safe_deps = tuple(dependencies)
    if not isinstance(allow_event_ledger_append, bool):
        raise InvalidEventCommitmentRequestError("allow_event_ledger_append must be a bool")
    if allow_event_ledger_append:
        raise InvalidEventCommitmentRequestError("allow_event_ledger_append must be False in PR-3A skeleton")
    safe_meta = _safe_meta(metadata, InvalidEventCommitmentRequestError)
    return EventCommitmentRequest(
        commitment_request_id=commitment_request_id,
        transaction_id=transaction_id,
        event_type=event_type,
        state_ref_ids=safe_state_refs,
        proposed_delta_ref_ids=safe_delta_refs,
        validation_ref_id=validation_ref_id,
        trace_id=trace_id,
        idempotency_key=idempotency_key,
        dependencies=safe_deps,
        allow_event_ledger_append=allow_event_ledger_append,
        metadata=safe_meta,
    )


def create_event_commitment_result(
    commitment_request_id: str,
    decision: str,
    status: str,
    committed_event_ref_id: str | None = None,
    event_ledger_ref_id: str | None = None,
    state_delta_applied: bool = False,
    event_ledger_appended: bool = False,
    rejection: EventCommitmentRejection | None = None,
    quarantined: bool = False,
    cancelled: bool = False,
    hidden_info_safe: bool = True,
    trace_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> EventCommitmentResult:
    _require_non_empty(commitment_request_id, "commitment_request_id", InvalidEventCommitmentResultError)
    if decision not in EVENT_COMMITMENT_DECISIONS:
        raise InvalidEventCommitmentResultError(
            f"decision must be one of {sorted(EVENT_COMMITMENT_DECISIONS)}, got: {decision!r}"
        )
    if status not in EVENT_COMMITMENT_STATUSES:
        raise InvalidEventCommitmentResultError(
            f"status must be one of {sorted(EVENT_COMMITMENT_STATUSES)}, got: {status!r}"
        )
    _optional_non_empty(committed_event_ref_id, "committed_event_ref_id", InvalidEventCommitmentResultError)
    _optional_non_empty(event_ledger_ref_id, "event_ledger_ref_id", InvalidEventCommitmentResultError)
    if not isinstance(state_delta_applied, bool):
        raise InvalidEventCommitmentResultError("state_delta_applied must be a bool")
    if state_delta_applied:
        raise InvalidEventCommitmentResultError("state_delta_applied must be False in PR-3A skeleton")
    if not isinstance(event_ledger_appended, bool):
        raise InvalidEventCommitmentResultError("event_ledger_appended must be a bool")
    if event_ledger_appended:
        raise InvalidEventCommitmentResultError("event_ledger_appended must be False in PR-3A skeleton")
    if rejection is not None and not isinstance(rejection, EventCommitmentRejection):
        raise InvalidEventCommitmentResultError("rejection must be None or an EventCommitmentRejection")
    if not isinstance(quarantined, bool):
        raise InvalidEventCommitmentResultError("quarantined must be a bool")
    if not isinstance(cancelled, bool):
        raise InvalidEventCommitmentResultError("cancelled must be a bool")
    if not isinstance(hidden_info_safe, bool):
        raise InvalidEventCommitmentResultError("hidden_info_safe must be a bool")
    _optional_non_empty(trace_id, "trace_id", InvalidEventCommitmentResultError)
    if decision == "committed" and rejection is not None:
        raise InvalidEventCommitmentResultError(
            "rejection must be None when decision is 'committed'"
        )
    if cancelled and quarantined:
        raise InvalidEventCommitmentResultError(
            "cancelled and quarantined may not both be True"
        )
    safe_meta = _safe_meta(metadata, InvalidEventCommitmentResultError)
    return EventCommitmentResult(
        commitment_request_id=commitment_request_id,
        decision=decision,
        status=status,
        committed_event_ref_id=committed_event_ref_id,
        event_ledger_ref_id=event_ledger_ref_id,
        state_delta_applied=state_delta_applied,
        event_ledger_appended=event_ledger_appended,
        rejection=rejection,
        quarantined=quarantined,
        cancelled=cancelled,
        hidden_info_safe=hidden_info_safe,
        trace_id=trace_id,
        metadata=safe_meta,
    )


def validate_event_commitment_dependency(obj: Any) -> bool:
    if not isinstance(obj, EventCommitmentDependency):
        return False
    if not isinstance(obj.dependency_id, str) or not obj.dependency_id.strip():
        return False
    if obj.dependency_type not in EVENT_COMMITMENT_DEPENDENCY_TYPES:
        return False
    if not isinstance(obj.reference_id, str) or not obj.reference_id.strip():
        return False
    if not isinstance(obj.required, bool):
        return False
    if not isinstance(obj.satisfied, bool):
        return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_event_commitment_rejection(obj: Any) -> bool:
    if not isinstance(obj, EventCommitmentRejection):
        return False
    if not isinstance(obj.rejection_id, str) or not obj.rejection_id.strip():
        return False
    if obj.decision not in EVENT_COMMITMENT_DECISIONS:
        return False
    if obj.decision not in _REJECTION_DECISIONS:
        return False
    if not isinstance(obj.reason, str) or not obj.reason.strip():
        return False
    if not isinstance(obj.blocking, bool):
        return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if not isinstance(obj.player_visible, bool):
        return False
    if obj.player_visible and not obj.hidden_info_safe:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_event_commitment_request(obj: Any) -> bool:
    if not isinstance(obj, EventCommitmentRequest):
        return False
    if not isinstance(obj.commitment_request_id, str) or not obj.commitment_request_id.strip():
        return False
    if not isinstance(obj.transaction_id, str) or not obj.transaction_id.strip():
        return False
    if not isinstance(obj.event_type, str) or not obj.event_type.strip():
        return False
    if not isinstance(obj.state_ref_ids, tuple) or len(obj.state_ref_ids) == 0:
        return False
    for ref_id in obj.state_ref_ids:
        if not isinstance(ref_id, str) or not ref_id.strip():
            return False
    if not isinstance(obj.proposed_delta_ref_ids, tuple) or len(obj.proposed_delta_ref_ids) == 0:
        return False
    for ref_id in obj.proposed_delta_ref_ids:
        if not isinstance(ref_id, str) or not ref_id.strip():
            return False
    if not isinstance(obj.validation_ref_id, str) or not obj.validation_ref_id.strip():
        return False
    if not isinstance(obj.trace_id, str) or not obj.trace_id.strip():
        return False
    if obj.idempotency_key is not None:
        if not isinstance(obj.idempotency_key, str) or not obj.idempotency_key.strip():
            return False
    if not isinstance(obj.dependencies, tuple):
        return False
    for dep in obj.dependencies:
        if not isinstance(dep, EventCommitmentDependency):
            return False
        if not validate_event_commitment_dependency(dep):
            return False
    if obj.allow_event_ledger_append:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_event_commitment_result(obj: Any) -> bool:
    if not isinstance(obj, EventCommitmentResult):
        return False
    if not isinstance(obj.commitment_request_id, str) or not obj.commitment_request_id.strip():
        return False
    if obj.decision not in EVENT_COMMITMENT_DECISIONS:
        return False
    if obj.status not in EVENT_COMMITMENT_STATUSES:
        return False
    if obj.committed_event_ref_id is not None:
        if not isinstance(obj.committed_event_ref_id, str) or not obj.committed_event_ref_id.strip():
            return False
    if obj.event_ledger_ref_id is not None:
        if not isinstance(obj.event_ledger_ref_id, str) or not obj.event_ledger_ref_id.strip():
            return False
    if not isinstance(obj.state_delta_applied, bool) or obj.state_delta_applied:
        return False
    if not isinstance(obj.event_ledger_appended, bool) or obj.event_ledger_appended:
        return False
    if obj.rejection is not None:
        if not isinstance(obj.rejection, EventCommitmentRejection):
            return False
        if not validate_event_commitment_rejection(obj.rejection):
            return False
    if obj.rejection is not None and obj.decision == "committed":
        return False
    if not isinstance(obj.quarantined, bool):
        return False
    if not isinstance(obj.cancelled, bool):
        return False
    if obj.cancelled and obj.quarantined:
        return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if obj.trace_id is not None:
        if not isinstance(obj.trace_id, str) or not obj.trace_id.strip():
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


class EventCommitmentService:
    """Stateless wrapper around event commitment creation/validation helpers."""

    def create_dependency(self, **kwargs: Any) -> EventCommitmentDependency:
        return create_event_commitment_dependency(**kwargs)

    def create_rejection(self, **kwargs: Any) -> EventCommitmentRejection:
        return create_event_commitment_rejection(**kwargs)

    def create_request(self, **kwargs: Any) -> EventCommitmentRequest:
        return create_event_commitment_request(**kwargs)

    def create_result(self, **kwargs: Any) -> EventCommitmentResult:
        return create_event_commitment_result(**kwargs)

    def validate_dependency(self, obj: Any) -> bool:
        return validate_event_commitment_dependency(obj)

    def validate_rejection(self, obj: Any) -> bool:
        return validate_event_commitment_rejection(obj)

    def validate_request(self, obj: Any) -> bool:
        return validate_event_commitment_request(obj)

    def validate_result(self, obj: Any) -> bool:
        return validate_event_commitment_result(obj)
