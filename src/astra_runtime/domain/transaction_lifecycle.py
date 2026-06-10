"""Transaction lifecycle skeleton — immutable transaction reference surfaces, no execution, no state mutation."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


TRANSACTION_LIFECYCLE_STAGES = frozenset({
    "transaction_requested",
    "command_reference_bound",
    "actor_reference_bound",
    "state_projection_bound",
    "dependencies_declared",
    "preconditions_declared",
    "domain_resolution_required",
    "proposed_delta_referenced",
    "validation_requested",
    "validation_passed",
    "validation_failed",
    "ready_for_event_commitment",
    "commitment_requested",
    "committed",
    "rejected",
    "quarantined",
    "cancelled",
    "superseded",
})

TRANSACTION_DECISIONS = frozenset({
    "accepted_for_planning",
    "requires_domain_resolution",
    "requires_validation",
    "ready_for_event_commitment",
    "rejected_by_missing_command",
    "rejected_by_missing_actor",
    "rejected_by_missing_state_reference",
    "rejected_by_missing_validation",
    "rejected_by_scope",
    "rejected_by_hidden_information_risk",
    "quarantined_for_audit",
    "cancelled",
    "superseded",
})

TRANSACTION_DEPENDENCY_TYPES = frozenset({
    "command_envelope_ref",
    "command_lifecycle_ref",
    "action_legality_ref",
    "actor_ref",
    "state_record_ref",
    "state_snapshot_ref",
    "state_projection_ref",
    "proposed_delta_ref",
    "validation_result_ref",
    "hidden_information_ref",
    "context_projection_ref",
    "runtime_trace_ref",
    "event_commitment_ref",
    "persistence_boundary_ref",
    "replay_audit_ref",
    "domain_resolution_ref",
    "resource_resolution_ref",
    "combat_resolution_ref",
    "ability_resolution_ref",
    "inventory_resolution_ref",
    "mission_resolution_ref",
    "social_resolution_ref",
    "generated_content_provenance_ref",
})

TRANSACTION_PRECONDITION_TYPES = frozenset({
    "accepted_command_required",
    "actor_reference_required",
    "state_reference_required",
    "projection_reference_required",
    "legality_result_required",
    "domain_resolution_required",
    "proposed_delta_required",
    "validation_required",
    "hidden_information_safe_required",
    "trace_required",
    "event_commitment_ready_required",
    "idempotency_key_required",
    "persistence_boundary_required",
    "replay_audit_required",
})


class TransactionLifecycleError(Exception):
    """Base error for transaction lifecycle operations."""


class InvalidTransactionDependencyError(TransactionLifecycleError):
    """Raised when a transaction dependency fails validation."""


class InvalidTransactionPreconditionError(TransactionLifecycleError):
    """Raised when a transaction precondition fails validation."""


class InvalidTransactionRequestError(TransactionLifecycleError):
    """Raised when a transaction request fails validation."""


class InvalidTransactionPlanError(TransactionLifecycleError):
    """Raised when a transaction plan fails validation."""


class InvalidTransactionResultError(TransactionLifecycleError):
    """Raised when a transaction result fails validation."""


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


def _safe_obj_seq(
    value: Any,
    name: str,
    error_cls: type[Exception],
    obj_type: type,
    validator_fn: Any,
) -> tuple:
    if isinstance(value, (str, bytes)):
        raise error_cls(f"{name} must not be a bare string")
    if value is None:
        return ()
    if not isinstance(value, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[Any] = []
    for i, elem in enumerate(value):
        if not isinstance(elem, obj_type):
            raise error_cls(f"{name}[{i}] must be a {obj_type.__name__}")
        if not validator_fn(elem):
            raise error_cls(f"{name}[{i}] failed validation")
        result.append(elem)
    return tuple(result)


@dataclass(frozen=True)
class TransactionDependency:
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
class TransactionPrecondition:
    precondition_id: str
    precondition_type: str
    satisfied: bool
    blocking: bool = True
    message: str | None = None
    hidden_info_safe: bool = True
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "precondition_id": self.precondition_id,
            "precondition_type": self.precondition_type,
            "satisfied": self.satisfied,
            "blocking": self.blocking,
            "message": self.message,
            "hidden_info_safe": self.hidden_info_safe,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class TransactionRequest:
    transaction_id: str
    command_envelope_id: str
    command_lifecycle_id: str | None
    actor_ref_id: str
    requested_stage: str = "transaction_requested"
    dependencies: tuple[TransactionDependency, ...] = ()
    preconditions: tuple[TransactionPrecondition, ...] = ()
    idempotency_key: str | None = None
    trace_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "command_envelope_id": self.command_envelope_id,
            "command_lifecycle_id": self.command_lifecycle_id,
            "actor_ref_id": self.actor_ref_id,
            "requested_stage": self.requested_stage,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "preconditions": [p.to_dict() for p in self.preconditions],
            "idempotency_key": self.idempotency_key,
            "trace_id": self.trace_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class TransactionPlan:
    transaction_id: str
    current_stage: str
    decision: str
    dependency_ids: tuple[str, ...] = ()
    precondition_ids: tuple[str, ...] = ()
    state_ref_ids: tuple[str, ...] = ()
    projection_ref_ids: tuple[str, ...] = ()
    proposed_delta_ref_ids: tuple[str, ...] = ()
    validation_ref_id: str | None = None
    trace_id: str | None = None
    ready_for_event_commitment: bool = False
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "current_stage": self.current_stage,
            "decision": self.decision,
            "dependency_ids": list(self.dependency_ids),
            "precondition_ids": list(self.precondition_ids),
            "state_ref_ids": list(self.state_ref_ids),
            "projection_ref_ids": list(self.projection_ref_ids),
            "proposed_delta_ref_ids": list(self.proposed_delta_ref_ids),
            "validation_ref_id": self.validation_ref_id,
            "trace_id": self.trace_id,
            "ready_for_event_commitment": self.ready_for_event_commitment,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class TransactionResult:
    transaction_id: str
    final_stage: str
    decision: str
    accepted_for_commitment: bool
    event_commitment_request_id: str | None = None
    rejection_reason: str | None = None
    quarantined: bool = False
    cancelled: bool = False
    hidden_info_safe: bool = True
    trace_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "transaction_id": self.transaction_id,
            "final_stage": self.final_stage,
            "decision": self.decision,
            "accepted_for_commitment": self.accepted_for_commitment,
            "event_commitment_request_id": self.event_commitment_request_id,
            "rejection_reason": self.rejection_reason,
            "quarantined": self.quarantined,
            "cancelled": self.cancelled,
            "hidden_info_safe": self.hidden_info_safe,
            "trace_id": self.trace_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_transaction_dependency(
    dependency_id: str,
    dependency_type: str,
    reference_id: str,
    required: bool = True,
    satisfied: bool = False,
    hidden_info_safe: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionDependency:
    _require_non_empty(dependency_id, "dependency_id", InvalidTransactionDependencyError)
    if dependency_type not in TRANSACTION_DEPENDENCY_TYPES:
        raise InvalidTransactionDependencyError(
            f"dependency_type must be one of {sorted(TRANSACTION_DEPENDENCY_TYPES)}, got: {dependency_type!r}"
        )
    _require_non_empty(reference_id, "reference_id", InvalidTransactionDependencyError)
    if not isinstance(required, bool):
        raise InvalidTransactionDependencyError("required must be a bool")
    if not isinstance(satisfied, bool):
        raise InvalidTransactionDependencyError("satisfied must be a bool")
    if not isinstance(hidden_info_safe, bool):
        raise InvalidTransactionDependencyError("hidden_info_safe must be a bool")
    safe_meta = _safe_meta(metadata, InvalidTransactionDependencyError)
    return TransactionDependency(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        reference_id=reference_id,
        required=required,
        satisfied=satisfied,
        hidden_info_safe=hidden_info_safe,
        metadata=safe_meta,
    )


def create_transaction_precondition(
    precondition_id: str,
    precondition_type: str,
    satisfied: bool,
    blocking: bool = True,
    message: str | None = None,
    hidden_info_safe: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionPrecondition:
    _require_non_empty(precondition_id, "precondition_id", InvalidTransactionPreconditionError)
    if precondition_type not in TRANSACTION_PRECONDITION_TYPES:
        raise InvalidTransactionPreconditionError(
            f"precondition_type must be one of {sorted(TRANSACTION_PRECONDITION_TYPES)}, got: {precondition_type!r}"
        )
    if not isinstance(satisfied, bool):
        raise InvalidTransactionPreconditionError("satisfied must be a bool")
    if not isinstance(blocking, bool):
        raise InvalidTransactionPreconditionError("blocking must be a bool")
    _optional_non_empty(message, "message", InvalidTransactionPreconditionError)
    if not isinstance(hidden_info_safe, bool):
        raise InvalidTransactionPreconditionError("hidden_info_safe must be a bool")
    safe_meta = _safe_meta(metadata, InvalidTransactionPreconditionError)
    return TransactionPrecondition(
        precondition_id=precondition_id,
        precondition_type=precondition_type,
        satisfied=satisfied,
        blocking=blocking,
        message=message,
        hidden_info_safe=hidden_info_safe,
        metadata=safe_meta,
    )


def create_transaction_request(
    transaction_id: str,
    command_envelope_id: str,
    actor_ref_id: str,
    command_lifecycle_id: str | None = None,
    requested_stage: str = "transaction_requested",
    dependencies: Sequence[TransactionDependency] | None = None,
    preconditions: Sequence[TransactionPrecondition] | None = None,
    idempotency_key: str | None = None,
    trace_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionRequest:
    _require_non_empty(transaction_id, "transaction_id", InvalidTransactionRequestError)
    _require_non_empty(command_envelope_id, "command_envelope_id", InvalidTransactionRequestError)
    _require_non_empty(actor_ref_id, "actor_ref_id", InvalidTransactionRequestError)
    _optional_non_empty(command_lifecycle_id, "command_lifecycle_id", InvalidTransactionRequestError)
    if requested_stage not in TRANSACTION_LIFECYCLE_STAGES:
        raise InvalidTransactionRequestError(
            f"requested_stage must be one of {sorted(TRANSACTION_LIFECYCLE_STAGES)}, got: {requested_stage!r}"
        )
    safe_deps = _safe_obj_seq(
        dependencies,
        "dependencies",
        InvalidTransactionRequestError,
        TransactionDependency,
        validate_transaction_dependency,
    )
    safe_preconds = _safe_obj_seq(
        preconditions,
        "preconditions",
        InvalidTransactionRequestError,
        TransactionPrecondition,
        validate_transaction_precondition,
    )
    _optional_non_empty(idempotency_key, "idempotency_key", InvalidTransactionRequestError)
    _optional_non_empty(trace_id, "trace_id", InvalidTransactionRequestError)
    safe_meta = _safe_meta(metadata, InvalidTransactionRequestError)
    return TransactionRequest(
        transaction_id=transaction_id,
        command_envelope_id=command_envelope_id,
        command_lifecycle_id=command_lifecycle_id,
        actor_ref_id=actor_ref_id,
        requested_stage=requested_stage,
        dependencies=safe_deps,
        preconditions=safe_preconds,
        idempotency_key=idempotency_key,
        trace_id=trace_id,
        metadata=safe_meta,
    )


def create_transaction_plan(
    transaction_id: str,
    current_stage: str,
    decision: str,
    dependency_ids: Sequence[str] | None = None,
    precondition_ids: Sequence[str] | None = None,
    state_ref_ids: Sequence[str] | None = None,
    projection_ref_ids: Sequence[str] | None = None,
    proposed_delta_ref_ids: Sequence[str] | None = None,
    validation_ref_id: str | None = None,
    trace_id: str | None = None,
    ready_for_event_commitment: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionPlan:
    _require_non_empty(transaction_id, "transaction_id", InvalidTransactionPlanError)
    if current_stage not in TRANSACTION_LIFECYCLE_STAGES:
        raise InvalidTransactionPlanError(
            f"current_stage must be one of {sorted(TRANSACTION_LIFECYCLE_STAGES)}, got: {current_stage!r}"
        )
    if decision not in TRANSACTION_DECISIONS:
        raise InvalidTransactionPlanError(
            f"decision must be one of {sorted(TRANSACTION_DECISIONS)}, got: {decision!r}"
        )
    safe_dep_ids = _safe_str_seq(dependency_ids, "dependency_ids", InvalidTransactionPlanError)
    safe_precond_ids = _safe_str_seq(precondition_ids, "precondition_ids", InvalidTransactionPlanError)
    safe_state_ids = _safe_str_seq(state_ref_ids, "state_ref_ids", InvalidTransactionPlanError)
    safe_proj_ids = _safe_str_seq(projection_ref_ids, "projection_ref_ids", InvalidTransactionPlanError)
    safe_delta_ids = _safe_str_seq(proposed_delta_ref_ids, "proposed_delta_ref_ids", InvalidTransactionPlanError)
    _optional_non_empty(validation_ref_id, "validation_ref_id", InvalidTransactionPlanError)
    _optional_non_empty(trace_id, "trace_id", InvalidTransactionPlanError)
    if not isinstance(ready_for_event_commitment, bool):
        raise InvalidTransactionPlanError("ready_for_event_commitment must be a bool")
    if ready_for_event_commitment:
        if decision != "ready_for_event_commitment":
            raise InvalidTransactionPlanError(
                "ready_for_event_commitment requires decision to be 'ready_for_event_commitment'"
            )
        if validation_ref_id is None:
            raise InvalidTransactionPlanError(
                "ready_for_event_commitment requires validation_ref_id"
            )
        if not safe_delta_ids:
            raise InvalidTransactionPlanError(
                "ready_for_event_commitment requires non-empty proposed_delta_ref_ids"
            )
    safe_meta = _safe_meta(metadata, InvalidTransactionPlanError)
    return TransactionPlan(
        transaction_id=transaction_id,
        current_stage=current_stage,
        decision=decision,
        dependency_ids=safe_dep_ids,
        precondition_ids=safe_precond_ids,
        state_ref_ids=safe_state_ids,
        projection_ref_ids=safe_proj_ids,
        proposed_delta_ref_ids=safe_delta_ids,
        validation_ref_id=validation_ref_id,
        trace_id=trace_id,
        ready_for_event_commitment=ready_for_event_commitment,
        metadata=safe_meta,
    )


def create_transaction_result(
    transaction_id: str,
    final_stage: str,
    decision: str,
    accepted_for_commitment: bool,
    event_commitment_request_id: str | None = None,
    rejection_reason: str | None = None,
    quarantined: bool = False,
    cancelled: bool = False,
    hidden_info_safe: bool = True,
    trace_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionResult:
    _require_non_empty(transaction_id, "transaction_id", InvalidTransactionResultError)
    if final_stage not in TRANSACTION_LIFECYCLE_STAGES:
        raise InvalidTransactionResultError(
            f"final_stage must be one of {sorted(TRANSACTION_LIFECYCLE_STAGES)}, got: {final_stage!r}"
        )
    if decision not in TRANSACTION_DECISIONS:
        raise InvalidTransactionResultError(
            f"decision must be one of {sorted(TRANSACTION_DECISIONS)}, got: {decision!r}"
        )
    if not isinstance(accepted_for_commitment, bool):
        raise InvalidTransactionResultError("accepted_for_commitment must be a bool")
    if not isinstance(quarantined, bool):
        raise InvalidTransactionResultError("quarantined must be a bool")
    if not isinstance(cancelled, bool):
        raise InvalidTransactionResultError("cancelled must be a bool")
    if not isinstance(hidden_info_safe, bool):
        raise InvalidTransactionResultError("hidden_info_safe must be a bool")
    _optional_non_empty(event_commitment_request_id, "event_commitment_request_id", InvalidTransactionResultError)
    _optional_non_empty(rejection_reason, "rejection_reason", InvalidTransactionResultError)
    _optional_non_empty(trace_id, "trace_id", InvalidTransactionResultError)
    if accepted_for_commitment:
        if final_stage not in {"ready_for_event_commitment", "commitment_requested"}:
            raise InvalidTransactionResultError(
                "accepted_for_commitment requires final_stage to be "
                "'ready_for_event_commitment' or 'commitment_requested'"
            )
        if event_commitment_request_id is None:
            raise InvalidTransactionResultError(
                "accepted_for_commitment requires event_commitment_request_id"
            )
        if rejection_reason is not None:
            raise InvalidTransactionResultError(
                "accepted_for_commitment must not have rejection_reason"
            )
    if rejection_reason is not None and accepted_for_commitment:
        raise InvalidTransactionResultError(
            "rejection_reason requires accepted_for_commitment to be False"
        )
    if cancelled and quarantined:
        raise InvalidTransactionResultError(
            "cancelled and quarantined may not both be True"
        )
    safe_meta = _safe_meta(metadata, InvalidTransactionResultError)
    return TransactionResult(
        transaction_id=transaction_id,
        final_stage=final_stage,
        decision=decision,
        accepted_for_commitment=accepted_for_commitment,
        event_commitment_request_id=event_commitment_request_id,
        rejection_reason=rejection_reason,
        quarantined=quarantined,
        cancelled=cancelled,
        hidden_info_safe=hidden_info_safe,
        trace_id=trace_id,
        metadata=safe_meta,
    )


def validate_transaction_dependency(obj: Any) -> bool:
    if not isinstance(obj, TransactionDependency):
        return False
    if not isinstance(obj.dependency_id, str) or not obj.dependency_id.strip():
        return False
    if obj.dependency_type not in TRANSACTION_DEPENDENCY_TYPES:
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


def validate_transaction_precondition(obj: Any) -> bool:
    if not isinstance(obj, TransactionPrecondition):
        return False
    if not isinstance(obj.precondition_id, str) or not obj.precondition_id.strip():
        return False
    if obj.precondition_type not in TRANSACTION_PRECONDITION_TYPES:
        return False
    if not isinstance(obj.satisfied, bool):
        return False
    if not isinstance(obj.blocking, bool):
        return False
    if obj.message is not None:
        if not isinstance(obj.message, str) or not obj.message.strip():
            return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_transaction_request(obj: Any) -> bool:
    if not isinstance(obj, TransactionRequest):
        return False
    if not isinstance(obj.transaction_id, str) or not obj.transaction_id.strip():
        return False
    if not isinstance(obj.command_envelope_id, str) or not obj.command_envelope_id.strip():
        return False
    if not isinstance(obj.actor_ref_id, str) or not obj.actor_ref_id.strip():
        return False
    if obj.command_lifecycle_id is not None:
        if not isinstance(obj.command_lifecycle_id, str) or not obj.command_lifecycle_id.strip():
            return False
    if obj.requested_stage not in TRANSACTION_LIFECYCLE_STAGES:
        return False
    if not isinstance(obj.dependencies, tuple):
        return False
    for dep in obj.dependencies:
        if not isinstance(dep, TransactionDependency):
            return False
        if not validate_transaction_dependency(dep):
            return False
    if not isinstance(obj.preconditions, tuple):
        return False
    for precond in obj.preconditions:
        if not isinstance(precond, TransactionPrecondition):
            return False
        if not validate_transaction_precondition(precond):
            return False
    if obj.idempotency_key is not None:
        if not isinstance(obj.idempotency_key, str) or not obj.idempotency_key.strip():
            return False
    if obj.trace_id is not None:
        if not isinstance(obj.trace_id, str) or not obj.trace_id.strip():
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_transaction_plan(obj: Any) -> bool:
    if not isinstance(obj, TransactionPlan):
        return False
    if not isinstance(obj.transaction_id, str) or not obj.transaction_id.strip():
        return False
    if obj.current_stage not in TRANSACTION_LIFECYCLE_STAGES:
        return False
    if obj.decision not in TRANSACTION_DECISIONS:
        return False
    for field_name in ("dependency_ids", "precondition_ids", "state_ref_ids", "projection_ref_ids", "proposed_delta_ref_ids"):
        val = getattr(obj, field_name)
        if not isinstance(val, tuple):
            return False
        for item in val:
            if not isinstance(item, str) or not item.strip():
                return False
    if obj.validation_ref_id is not None:
        if not isinstance(obj.validation_ref_id, str) or not obj.validation_ref_id.strip():
            return False
    if obj.trace_id is not None:
        if not isinstance(obj.trace_id, str) or not obj.trace_id.strip():
            return False
    if not isinstance(obj.ready_for_event_commitment, bool):
        return False
    if obj.ready_for_event_commitment:
        if obj.decision != "ready_for_event_commitment":
            return False
        if obj.validation_ref_id is None:
            return False
        if not obj.proposed_delta_ref_ids:
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_transaction_result(obj: Any) -> bool:
    if not isinstance(obj, TransactionResult):
        return False
    if not isinstance(obj.transaction_id, str) or not obj.transaction_id.strip():
        return False
    if obj.final_stage not in TRANSACTION_LIFECYCLE_STAGES:
        return False
    if obj.decision not in TRANSACTION_DECISIONS:
        return False
    if not isinstance(obj.accepted_for_commitment, bool):
        return False
    if not isinstance(obj.quarantined, bool):
        return False
    if not isinstance(obj.cancelled, bool):
        return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if obj.event_commitment_request_id is not None:
        if not isinstance(obj.event_commitment_request_id, str) or not obj.event_commitment_request_id.strip():
            return False
    if obj.rejection_reason is not None:
        if not isinstance(obj.rejection_reason, str) or not obj.rejection_reason.strip():
            return False
    if obj.trace_id is not None:
        if not isinstance(obj.trace_id, str) or not obj.trace_id.strip():
            return False
    if obj.accepted_for_commitment:
        if obj.final_stage not in {"ready_for_event_commitment", "commitment_requested"}:
            return False
        if obj.event_commitment_request_id is None:
            return False
        if obj.rejection_reason is not None:
            return False
    if obj.rejection_reason is not None and obj.accepted_for_commitment:
        return False
    if obj.cancelled and obj.quarantined:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


class TransactionLifecycleService:
    """Stateless wrapper around transaction lifecycle creation/validation helpers."""

    def create_dependency(self, **kwargs: Any) -> TransactionDependency:
        return create_transaction_dependency(**kwargs)

    def create_precondition(self, **kwargs: Any) -> TransactionPrecondition:
        return create_transaction_precondition(**kwargs)

    def create_request(self, **kwargs: Any) -> TransactionRequest:
        return create_transaction_request(**kwargs)

    def create_plan(self, **kwargs: Any) -> TransactionPlan:
        return create_transaction_plan(**kwargs)

    def create_result(self, **kwargs: Any) -> TransactionResult:
        return create_transaction_result(**kwargs)

    def validate_dependency(self, obj: Any) -> bool:
        return validate_transaction_dependency(obj)

    def validate_precondition(self, obj: Any) -> bool:
        return validate_transaction_precondition(obj)

    def validate_request(self, obj: Any) -> bool:
        return validate_transaction_request(obj)

    def validate_plan(self, obj: Any) -> bool:
        return validate_transaction_plan(obj)

    def validate_result(self, obj: Any) -> bool:
        return validate_transaction_result(obj)
