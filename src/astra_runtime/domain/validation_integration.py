"""Validation integration skeleton — immutable validation integration surfaces, no validation rules, no invariant enforcement."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


VALIDATION_INTEGRATION_STAGES = frozenset({
    "validation_integration_requested",
    "validation_scope_declared",
    "dependency_refs_bound",
    "state_refs_bound",
    "transaction_refs_bound",
    "event_commitment_refs_bound",
    "invariant_set_declared",
    "invariant_precheck_requested",
    "invariant_precheck_passed",
    "invariant_precheck_failed",
    "domain_validation_required",
    "domain_validation_referenced",
    "hidden_info_safety_checked",
    "provenance_checked",
    "validation_passed",
    "validation_failed",
    "validation_quarantined",
    "validation_escalated",
    "validation_cancelled",
    "validation_superseded",
})

VALIDATION_INTEGRATION_DECISIONS = frozenset({
    "validation_ready",
    "validation_passed",
    "validation_failed",
    "rejected_by_missing_command_ref",
    "rejected_by_missing_state_ref",
    "rejected_by_missing_transaction_ref",
    "rejected_by_missing_event_commitment_ref",
    "rejected_by_missing_invariant_set",
    "rejected_by_hidden_information_risk",
    "rejected_by_provenance_gap",
    "rejected_by_schema_mismatch",
    "rejected_by_authority_mismatch",
    "rejected_by_phase_boundary",
    "quarantined_for_review",
    "escalated_to_doctrine",
    "unsupported_validation_scope",
})

VALIDATION_INVARIANT_FAMILIES = frozenset({
    "command_authority_invariant",
    "action_legality_invariant",
    "state_reference_invariant",
    "state_projection_visibility_invariant",
    "transaction_lifecycle_invariant",
    "event_commitment_invariant",
    "state_delta_shape_invariant",
    "event_ledger_shape_invariant",
    "validation_result_authority_invariant",
    "hidden_information_partition_invariant",
    "context_projection_visibility_invariant",
    "persistence_boundary_invariant",
    "replay_audit_invariant",
    "runtime_trace_invariant",
    "schema_record_shape_invariant",
    "source_local_authority_invariant",
    "generated_content_provenance_invariant",
    "canon_boundary_invariant",
    "conversion_boundary_invariant",
    "model_non_authority_invariant",
    "live_play_non_authority_invariant",
})

VALIDATION_FAILURE_ROUTES = frozenset({
    "block_command_before_transaction",
    "block_transaction_before_commitment",
    "block_event_commitment",
    "quarantine_transaction",
    "quarantine_event_commitment",
    "quarantine_generated_content",
    "escalate_doctrine_gap",
    "reject_source_local_authority",
    "reject_hidden_info_leak",
    "reject_schema_mismatch",
    "reject_phase_boundary_violation",
    "request_downstream_domain_validation",
})


VALIDATION_PUBLIC_REASON_CODES = frozenset({
    "validation_pending",
    "validation_blocked",
    "validation_rejected",
    "validation_quarantined",
    "validation_escalated",
    "unsupported_validation_scope",
})

_REQUESTABLE_VALIDATION_STAGES = frozenset({
    "validation_integration_requested",
    "validation_scope_declared",
    "dependency_refs_bound",
    "state_refs_bound",
    "transaction_refs_bound",
    "event_commitment_refs_bound",
    "invariant_set_declared",
    "invariant_precheck_requested",
    "domain_validation_required",
    "domain_validation_referenced",
})

_QUARANTINE_FAILURE_ROUTES = frozenset({
    "quarantine_transaction",
    "quarantine_event_commitment",
    "quarantine_generated_content",
})

_ROUTE_DECISION_COMPATIBILITY = MappingProxyType({
    "block_command_before_transaction": frozenset({
        "validation_failed",
        "rejected_by_missing_command_ref",
        "rejected_by_authority_mismatch",
        "rejected_by_phase_boundary",
    }),
    "block_transaction_before_commitment": frozenset({
        "validation_failed",
        "rejected_by_missing_state_ref",
        "rejected_by_missing_transaction_ref",
        "rejected_by_missing_invariant_set",
        "rejected_by_schema_mismatch",
        "rejected_by_authority_mismatch",
        "rejected_by_phase_boundary",
    }),
    "block_event_commitment": frozenset({
        "validation_failed",
        "rejected_by_missing_event_commitment_ref",
        "rejected_by_missing_state_ref",
        "rejected_by_missing_invariant_set",
        "rejected_by_hidden_information_risk",
        "rejected_by_provenance_gap",
        "rejected_by_schema_mismatch",
        "rejected_by_authority_mismatch",
        "rejected_by_phase_boundary",
    }),
    "quarantine_transaction": frozenset({"quarantined_for_review"}),
    "quarantine_event_commitment": frozenset({"quarantined_for_review"}),
    "quarantine_generated_content": frozenset({"quarantined_for_review"}),
    "escalate_doctrine_gap": frozenset({"escalated_to_doctrine"}),
    "reject_source_local_authority": frozenset({
        "rejected_by_authority_mismatch",
        "rejected_by_phase_boundary",
    }),
    "reject_hidden_info_leak": frozenset({"rejected_by_hidden_information_risk"}),
    "reject_schema_mismatch": frozenset({"rejected_by_schema_mismatch"}),
    "reject_phase_boundary_violation": frozenset({"rejected_by_phase_boundary"}),
    "request_downstream_domain_validation": frozenset({
        "validation_ready",
        "unsupported_validation_scope",
    }),
})

_PUBLIC_REASON_COMPATIBILITY = MappingProxyType({
    "validation_ready": frozenset({"validation_pending", "validation_blocked"}),
    "validation_failed": frozenset({"validation_blocked", "validation_rejected"}),
    "quarantined_for_review": frozenset({"validation_quarantined"}),
    "escalated_to_doctrine": frozenset({"validation_escalated"}),
    "unsupported_validation_scope": frozenset({"unsupported_validation_scope", "validation_pending"}),
})

# validation_cancelled, validation_superseded, and invariant_precheck_failed remain
# reserved stages until a later doctrine decision adds lawful decision mappings.
_DECISION_FINAL_STAGE_COMPATIBILITY = MappingProxyType({
    "validation_passed": frozenset({"validation_passed"}),
    "validation_failed": frozenset({"validation_failed"}),
    "rejected_by_missing_command_ref": frozenset({"validation_failed"}),
    "rejected_by_missing_state_ref": frozenset({"validation_failed"}),
    "rejected_by_missing_transaction_ref": frozenset({"validation_failed"}),
    "rejected_by_missing_event_commitment_ref": frozenset({"validation_failed"}),
    "rejected_by_missing_invariant_set": frozenset({"validation_failed"}),
    "rejected_by_hidden_information_risk": frozenset({"validation_failed"}),
    "rejected_by_provenance_gap": frozenset({"validation_failed"}),
    "rejected_by_schema_mismatch": frozenset({"validation_failed"}),
    "rejected_by_authority_mismatch": frozenset({"validation_failed"}),
    "rejected_by_phase_boundary": frozenset({"validation_failed"}),
    "quarantined_for_review": frozenset({"validation_quarantined"}),
    "escalated_to_doctrine": frozenset({"validation_escalated"}),
    "unsupported_validation_scope": frozenset({"domain_validation_required"}),
    "validation_ready": frozenset({
        "validation_integration_requested",
        "validation_scope_declared",
        "dependency_refs_bound",
        "state_refs_bound",
        "transaction_refs_bound",
        "event_commitment_refs_bound",
        "invariant_set_declared",
        "invariant_precheck_requested",
        "invariant_precheck_passed",
        "domain_validation_required",
        "domain_validation_referenced",
        "hidden_info_safety_checked",
        "provenance_checked",
    }),
})

VALIDATION_DEPENDENCY_TYPES = frozenset({
    "schema_registry_ref",
    "record_identity_ref",
    "command_envelope_ref",
    "command_lifecycle_ref",
    "action_legality_ref",
    "state_record_ref",
    "state_snapshot_ref",
    "state_projection_ref",
    "transaction_ref",
    "transaction_plan_ref",
    "transaction_result_ref",
    "event_commitment_request_ref",
    "event_commitment_result_ref",
    "state_delta_ref",
    "event_ledger_ref",
    "validation_pipeline_ref",
    "validation_result_ref",
    "invariant_precheck_ref",
    "hidden_information_ref",
    "context_projection_ref",
    "persistence_boundary_ref",
    "replay_audit_ref",
    "runtime_trace_ref",
    "generated_content_provenance_ref",
    "source_local_ref",
    "canon_boundary_ref",
    "conversion_boundary_ref",
})

VALIDATION_SUBJECT_TYPES = frozenset({
    "command",
    "action_legality",
    "state_record",
    "state_projection",
    "transaction",
    "event_commitment",
    "state_delta",
    "event_ledger",
    "generated_content",
    "source_local_content",
    "canon_reference",
    "conversion_artifact",
    "hidden_information",
    "context_projection",
    "runtime_trace",
})


class ValidationIntegrationError(Exception):
    """Base error for validation integration operations."""


class InvalidValidationIntegrationDependencyError(ValidationIntegrationError):
    """Raised when a validation integration dependency fails validation."""


class InvalidValidationInvariantDeclarationError(ValidationIntegrationError):
    """Raised when a validation invariant declaration fails validation."""


class InvalidValidationIntegrationRequestError(ValidationIntegrationError):
    """Raised when a validation integration request fails validation."""


class InvalidValidationIntegrationResultError(ValidationIntegrationError):
    """Raised when a validation integration result fails validation."""


class InvalidValidationFailureRouteError(ValidationIntegrationError):
    """Raised when a validation failure route fails validation."""


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


def _require_bool(value: Any, name: str, error_cls: type[Exception]) -> None:
    if not isinstance(value, bool):
        raise error_cls(f"{name} must be a bool")


def _public_reason_codes_for_decision(decision: str) -> frozenset[str]:
    if decision.startswith("rejected_by_"):
        return frozenset({"validation_rejected", "validation_blocked"})
    return _PUBLIC_REASON_COMPATIBILITY.get(decision, frozenset())


def _validate_failure_route_fields(obj: Any, error_cls: type[Exception]) -> None:
    _require_non_empty(obj.route_id, "route_id", error_cls)
    if obj.route_type not in VALIDATION_FAILURE_ROUTES:
        raise error_cls("route_type must be a known validation failure route")
    if obj.decision not in VALIDATION_INTEGRATION_DECISIONS:
        raise error_cls("decision must be a known validation integration decision")
    _require_non_empty(obj.subject_ref_id, "subject_ref_id", error_cls)
    _require_bool(obj.blocking, "blocking", error_cls)
    _require_bool(obj.quarantines, "quarantines", error_cls)
    _require_bool(obj.escalates, "escalates", error_cls)
    _require_bool(obj.player_visible, "player_visible", error_cls)
    _require_bool(obj.hidden_info_safe, "hidden_info_safe", error_cls)
    _require_bool(obj.trace_required, "trace_required", error_cls)
    if obj.decision == "validation_passed":
        raise error_cls("decision must not be 'validation_passed' on a failure route")
    if not obj.blocking:
        raise error_cls("blocking must be True on every failure route")
    if not obj.trace_required:
        raise error_cls("trace_required must be True on every failure route")
    if obj.quarantines != (obj.route_type in _QUARANTINE_FAILURE_ROUTES):
        raise error_cls("quarantines must exactly match quarantine route types")
    if obj.escalates != (obj.route_type == "escalate_doctrine_gap"):
        raise error_cls("escalates must be True only for doctrine escalation routes")
    if obj.decision not in _ROUTE_DECISION_COMPATIBILITY[obj.route_type]:
        raise error_cls("route_type and decision are incompatible")
    public_reason_code = getattr(obj, "public_reason_code", None)
    if public_reason_code is not None:
        if public_reason_code not in VALIDATION_PUBLIC_REASON_CODES:
            raise error_cls("public_reason_code must be a supported sanitized reason code")
        if public_reason_code not in _public_reason_codes_for_decision(obj.decision):
            raise error_cls("public_reason_code is incompatible with decision")
    if obj.player_visible:
        if not obj.hidden_info_safe:
            raise error_cls("hidden_info_safe must be True when player_visible is True")
        if public_reason_code is None:
            raise error_cls("public_reason_code is required when player_visible is True")
    if not isinstance(obj.metadata, Mapping):
        raise error_cls("metadata must be a mapping")


def _validate_request_stage(requested_stage: str, error_cls: type[Exception]) -> None:
    if requested_stage not in VALIDATION_INTEGRATION_STAGES:
        raise error_cls("requested_stage must be a known validation integration stage")
    if requested_stage not in _REQUESTABLE_VALIDATION_STAGES:
        raise error_cls("requested_stage must not claim a terminal or outcome stage")


def _validate_result_semantics(obj: Any, error_cls: type[Exception]) -> None:
    _require_non_empty(obj.validation_request_id, "validation_request_id", error_cls)
    if obj.decision not in VALIDATION_INTEGRATION_DECISIONS:
        raise error_cls("decision must be a known validation integration decision")
    if obj.final_stage not in VALIDATION_INTEGRATION_STAGES:
        raise error_cls("final_stage must be a known validation integration stage")
    if obj.final_stage not in _DECISION_FINAL_STAGE_COMPATIBILITY[obj.decision]:
        raise error_cls("decision and final_stage are incompatible")
    if getattr(obj, "subject_type", None) not in VALIDATION_SUBJECT_TYPES:
        raise error_cls("subject_type must be a known validation subject type")
    _require_non_empty(getattr(obj, "subject_ref_id", None), "subject_ref_id", error_cls)
    _require_non_empty(obj.trace_id, "trace_id", error_cls)
    if obj.validation_result_ref_id is not None:
        _require_non_empty(obj.validation_result_ref_id, "validation_result_ref_id", error_cls)
    if obj.decision != "validation_ready":
        _require_non_empty(obj.validation_result_ref_id, "validation_result_ref_id", error_cls)
    _optional_non_empty(obj.invariant_precheck_ref_id, "invariant_precheck_ref_id", error_cls)
    if obj.final_stage in {"invariant_precheck_passed", "invariant_precheck_failed"}:
        _require_non_empty(obj.invariant_precheck_ref_id, "invariant_precheck_ref_id", error_cls)
    if not isinstance(obj.failure_routes, tuple):
        raise error_cls("failure_routes must be a tuple")
    for route in obj.failure_routes:
        if not isinstance(route, ValidationFailureRoute):
            raise error_cls("failure_routes entries must be ValidationFailureRoute")
        _validate_failure_route_fields(route, error_cls)
    for bool_field in (
        "passed", "blocking", "quarantined", "escalated", "hidden_info_safe",
        "provenance_checked", "state_mutation_allowed", "event_append_allowed",
        "persistence_allowed", "model_authority_allowed",
    ):
        _require_bool(getattr(obj, bool_field), bool_field, error_cls)
    if not isinstance(getattr(obj, "provenance_ref_ids", None), tuple):
        raise error_cls("provenance_ref_ids must be a tuple")
    for i, ref in enumerate(obj.provenance_ref_ids):
        if not isinstance(ref, str) or not ref.strip():
            raise error_cls(f"provenance_ref_ids[{i}] must be a non-empty string")
    if obj.provenance_ref_ids and not obj.provenance_checked:
        raise error_cls("provenance_checked must be True when provenance_ref_ids are present")
    if obj.state_mutation_allowed:
        raise error_cls("state_mutation_allowed must be False in PR-4C skeleton")
    if obj.event_append_allowed:
        raise error_cls("event_append_allowed must be False in PR-4C skeleton")
    if obj.persistence_allowed:
        raise error_cls("persistence_allowed must be False in PR-4C skeleton")
    if obj.model_authority_allowed:
        raise error_cls("model_authority_allowed must be False in PR-4C skeleton")
    if obj.quarantined != (obj.decision == "quarantined_for_review"):
        raise error_cls("quarantined flag must exactly match quarantined_for_review decision")
    if obj.escalated != (obj.decision == "escalated_to_doctrine"):
        raise error_cls("escalated flag must exactly match escalated_to_doctrine decision")
    if obj.blocking != (obj.decision != "validation_passed"):
        raise error_cls("blocking must be False if and only if decision is validation_passed")
    if obj.decision == "validation_passed":
        if not obj.passed:
            raise error_cls("passed must be True when decision is validation_passed")
        if obj.final_stage != "validation_passed":
            raise error_cls("final_stage must be validation_passed for passed results")
        if obj.failure_routes:
            raise error_cls("failure_routes must be empty for passed results")
        if not obj.hidden_info_safe:
            raise error_cls("hidden_info_safe must be True for passed results")
        if obj.subject_type == "generated_content":
            if not obj.provenance_checked or not obj.provenance_ref_ids:
                raise error_cls("generated-content pass requires provenance linkage")
        return
    if obj.passed:
        raise error_cls("passed must be False for non-passed decisions")
    if obj.decision == "validation_ready":
        for route in obj.failure_routes:
            if route.route_type != "request_downstream_domain_validation" or route.decision != "validation_ready":
                raise error_cls("validation_ready routes must request downstream domain validation")
        return
    if not obj.failure_routes:
        raise error_cls("terminal non-passed decisions require at least one failure route")
    if obj.decision == "validation_failed" or obj.decision.startswith("rejected_by_"):
        for route in obj.failure_routes:
            if route.decision != obj.decision:
                raise error_cls("failure route decision must match result decision")
        return
    if obj.decision == "quarantined_for_review":
        for route in obj.failure_routes:
            if route.route_type not in _QUARANTINE_FAILURE_ROUTES or route.decision != obj.decision:
                raise error_cls("quarantine decisions require quarantine routes")
        return
    if obj.decision == "escalated_to_doctrine":
        for route in obj.failure_routes:
            if route.route_type != "escalate_doctrine_gap" or route.decision != obj.decision:
                raise error_cls("escalation decisions require doctrine escalation routes")
        return
    if obj.decision == "unsupported_validation_scope":
        for route in obj.failure_routes:
            if route.route_type != "request_downstream_domain_validation" or route.decision != obj.decision:
                raise error_cls("unsupported scope requires downstream validation route")
        return


@dataclass(frozen=True)
class ValidationIntegrationDependency:
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
class ValidationInvariantDeclaration:
    invariant_id: str
    invariant_family: str
    subject_type: str
    subject_ref_id: str
    required: bool = True
    blocking: bool = True
    backend_only: bool = True
    hidden_info_safe: bool = True
    provenance_required: bool = False
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "invariant_id": self.invariant_id,
            "invariant_family": self.invariant_family,
            "subject_type": self.subject_type,
            "subject_ref_id": self.subject_ref_id,
            "required": self.required,
            "blocking": self.blocking,
            "backend_only": self.backend_only,
            "hidden_info_safe": self.hidden_info_safe,
            "provenance_required": self.provenance_required,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class ValidationFailureRoute:
    route_id: str
    route_type: str
    decision: str
    subject_ref_id: str
    blocking: bool = True
    quarantines: bool = False
    escalates: bool = False
    player_visible: bool = False
    hidden_info_safe: bool = True
    trace_required: bool = True
    public_reason_code: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "route_id": self.route_id,
            "route_type": self.route_type,
            "decision": self.decision,
            "subject_ref_id": self.subject_ref_id,
            "blocking": self.blocking,
            "quarantines": self.quarantines,
            "escalates": self.escalates,
            "player_visible": self.player_visible,
            "hidden_info_safe": self.hidden_info_safe,
            "trace_required": self.trace_required,
            "public_reason_code": self.public_reason_code,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }

    def to_public_dict(self) -> dict[str, Any]:
        if not self.player_visible or not self.hidden_info_safe:
            raise InvalidValidationFailureRouteError(
                "public route serialization requires player_visible=True and hidden_info_safe=True"
            )
        _validate_failure_route_fields(self, InvalidValidationFailureRouteError)
        return {
            "reason_code": self.public_reason_code,
            "blocking": self.blocking,
            "quarantines": self.quarantines,
            "escalates": self.escalates,
        }


@dataclass(frozen=True)
class ValidationIntegrationRequest:
    validation_request_id: str
    subject_type: str
    subject_ref_id: str
    requesting_service: str
    requested_stage: str = "validation_integration_requested"
    dependencies: tuple[ValidationIntegrationDependency, ...] = ()
    invariants: tuple[ValidationInvariantDeclaration, ...] = ()
    transaction_ref_id: str | None = None
    event_commitment_ref_id: str | None = None
    state_ref_ids: tuple[str, ...] = ()
    projection_ref_ids: tuple[str, ...] = ()
    validation_pipeline_ref_id: str | None = None
    hidden_information_ref_ids: tuple[str, ...] = ()
    generated_content_ref_ids: tuple[str, ...] = ()
    trace_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_request_id": self.validation_request_id,
            "subject_type": self.subject_type,
            "subject_ref_id": self.subject_ref_id,
            "requesting_service": self.requesting_service,
            "requested_stage": self.requested_stage,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "invariants": [i.to_dict() for i in self.invariants],
            "transaction_ref_id": self.transaction_ref_id,
            "event_commitment_ref_id": self.event_commitment_ref_id,
            "state_ref_ids": list(self.state_ref_ids),
            "projection_ref_ids": list(self.projection_ref_ids),
            "validation_pipeline_ref_id": self.validation_pipeline_ref_id,
            "hidden_information_ref_ids": list(self.hidden_information_ref_ids),
            "generated_content_ref_ids": list(self.generated_content_ref_ids),
            "trace_id": self.trace_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True)
class ValidationIntegrationResult:
    validation_request_id: str
    decision: str
    final_stage: str
    subject_type: str
    subject_ref_id: str
    validation_result_ref_id: str | None = None
    invariant_precheck_ref_id: str | None = None
    failure_routes: tuple[ValidationFailureRoute, ...] = ()
    passed: bool = False
    blocking: bool = True
    quarantined: bool = False
    escalated: bool = False
    hidden_info_safe: bool = True
    provenance_checked: bool = False
    provenance_ref_ids: tuple[str, ...] = ()
    state_mutation_allowed: bool = False
    event_append_allowed: bool = False
    persistence_allowed: bool = False
    model_authority_allowed: bool = False
    trace_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_request_id": self.validation_request_id,
            "decision": self.decision,
            "final_stage": self.final_stage,
            "subject_type": self.subject_type,
            "subject_ref_id": self.subject_ref_id,
            "validation_result_ref_id": self.validation_result_ref_id,
            "invariant_precheck_ref_id": self.invariant_precheck_ref_id,
            "failure_routes": [r.to_dict() for r in self.failure_routes],
            "passed": self.passed,
            "blocking": self.blocking,
            "quarantined": self.quarantined,
            "escalated": self.escalated,
            "hidden_info_safe": self.hidden_info_safe,
            "provenance_checked": self.provenance_checked,
            "provenance_ref_ids": list(self.provenance_ref_ids),
            "state_mutation_allowed": self.state_mutation_allowed,
            "event_append_allowed": self.event_append_allowed,
            "persistence_allowed": self.persistence_allowed,
            "model_authority_allowed": self.model_authority_allowed,
            "trace_id": self.trace_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------


def create_validation_integration_dependency(
    dependency_id: str,
    dependency_type: str,
    reference_id: str,
    required: bool = True,
    satisfied: bool = False,
    hidden_info_safe: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationIntegrationDependency:
    _require_non_empty(dependency_id, "dependency_id", InvalidValidationIntegrationDependencyError)
    if dependency_type not in VALIDATION_DEPENDENCY_TYPES:
        raise InvalidValidationIntegrationDependencyError(
            f"dependency_type must be one of {sorted(VALIDATION_DEPENDENCY_TYPES)}, got: {dependency_type!r}"
        )
    _require_non_empty(reference_id, "reference_id", InvalidValidationIntegrationDependencyError)
    _require_bool(required, "required", InvalidValidationIntegrationDependencyError)
    _require_bool(satisfied, "satisfied", InvalidValidationIntegrationDependencyError)
    _require_bool(hidden_info_safe, "hidden_info_safe", InvalidValidationIntegrationDependencyError)
    safe_meta = _safe_meta(metadata, InvalidValidationIntegrationDependencyError)
    return ValidationIntegrationDependency(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        reference_id=reference_id,
        required=required,
        satisfied=satisfied,
        hidden_info_safe=hidden_info_safe,
        metadata=safe_meta,
    )


def create_validation_invariant_declaration(
    invariant_id: str,
    invariant_family: str,
    subject_type: str,
    subject_ref_id: str,
    required: bool = True,
    blocking: bool = True,
    backend_only: bool = True,
    hidden_info_safe: bool = True,
    provenance_required: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationInvariantDeclaration:
    _require_non_empty(invariant_id, "invariant_id", InvalidValidationInvariantDeclarationError)
    if invariant_family not in VALIDATION_INVARIANT_FAMILIES:
        raise InvalidValidationInvariantDeclarationError(
            f"invariant_family must be one of {sorted(VALIDATION_INVARIANT_FAMILIES)}, got: {invariant_family!r}"
        )
    if subject_type not in VALIDATION_SUBJECT_TYPES:
        raise InvalidValidationInvariantDeclarationError(
            f"subject_type must be one of {sorted(VALIDATION_SUBJECT_TYPES)}, got: {subject_type!r}"
        )
    _require_non_empty(subject_ref_id, "subject_ref_id", InvalidValidationInvariantDeclarationError)
    _require_bool(required, "required", InvalidValidationInvariantDeclarationError)
    _require_bool(blocking, "blocking", InvalidValidationInvariantDeclarationError)
    _require_bool(backend_only, "backend_only", InvalidValidationInvariantDeclarationError)
    _require_bool(hidden_info_safe, "hidden_info_safe", InvalidValidationInvariantDeclarationError)
    _require_bool(provenance_required, "provenance_required", InvalidValidationInvariantDeclarationError)
    if not backend_only:
        raise InvalidValidationInvariantDeclarationError(
            "backend_only must be True in PR-4A skeleton"
        )
    if not hidden_info_safe and not backend_only:
        raise InvalidValidationInvariantDeclarationError(
            "hidden_info_safe must be True when backend_only is False"
        )
    if invariant_family == "generated_content_provenance_invariant" and not provenance_required:
        raise InvalidValidationInvariantDeclarationError(
            "provenance_required must be True when invariant_family is 'generated_content_provenance_invariant'"
        )
    safe_meta = _safe_meta(metadata, InvalidValidationInvariantDeclarationError)
    return ValidationInvariantDeclaration(
        invariant_id=invariant_id,
        invariant_family=invariant_family,
        subject_type=subject_type,
        subject_ref_id=subject_ref_id,
        required=required,
        blocking=blocking,
        backend_only=backend_only,
        hidden_info_safe=hidden_info_safe,
        provenance_required=provenance_required,
        metadata=safe_meta,
    )


def create_validation_failure_route(
    route_id: str,
    route_type: str,
    decision: str,
    subject_ref_id: str,
    blocking: bool = True,
    quarantines: bool = False,
    escalates: bool = False,
    player_visible: bool = False,
    hidden_info_safe: bool = True,
    trace_required: bool = True,
    public_reason_code: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationFailureRoute:
    safe_meta = _safe_meta(metadata, InvalidValidationFailureRouteError)
    route = ValidationFailureRoute(
        route_id=route_id,
        route_type=route_type,
        decision=decision,
        subject_ref_id=subject_ref_id,
        blocking=blocking,
        quarantines=quarantines,
        escalates=escalates,
        player_visible=player_visible,
        hidden_info_safe=hidden_info_safe,
        trace_required=trace_required,
        public_reason_code=public_reason_code,
        metadata=safe_meta,
    )
    _validate_failure_route_fields(route, InvalidValidationFailureRouteError)
    return route


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


def create_validation_integration_request(
    validation_request_id: str,
    subject_type: str,
    subject_ref_id: str,
    requesting_service: str,
    requested_stage: str = "validation_integration_requested",
    dependencies: Sequence[ValidationIntegrationDependency] | None = None,
    invariants: Sequence[ValidationInvariantDeclaration] | None = None,
    transaction_ref_id: str | None = None,
    event_commitment_ref_id: str | None = None,
    state_ref_ids: Sequence[str] | None = None,
    projection_ref_ids: Sequence[str] | None = None,
    validation_pipeline_ref_id: str | None = None,
    hidden_information_ref_ids: Sequence[str] | None = None,
    generated_content_ref_ids: Sequence[str] | None = None,
    trace_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationIntegrationRequest:
    _require_non_empty(validation_request_id, "validation_request_id", InvalidValidationIntegrationRequestError)
    if subject_type not in VALIDATION_SUBJECT_TYPES:
        raise InvalidValidationIntegrationRequestError(
            f"subject_type must be one of {sorted(VALIDATION_SUBJECT_TYPES)}, got: {subject_type!r}"
        )
    _require_non_empty(subject_ref_id, "subject_ref_id", InvalidValidationIntegrationRequestError)
    _require_non_empty(requesting_service, "requesting_service", InvalidValidationIntegrationRequestError)
    _validate_request_stage(requested_stage, InvalidValidationIntegrationRequestError)
    safe_deps = _safe_obj_seq(
        dependencies,
        "dependencies",
        InvalidValidationIntegrationRequestError,
        ValidationIntegrationDependency,
        validate_validation_integration_dependency,
    )
    safe_invs = _safe_obj_seq(
        invariants,
        "invariants",
        InvalidValidationIntegrationRequestError,
        ValidationInvariantDeclaration,
        validate_validation_invariant_declaration,
    )
    _optional_non_empty(transaction_ref_id, "transaction_ref_id", InvalidValidationIntegrationRequestError)
    _optional_non_empty(event_commitment_ref_id, "event_commitment_ref_id", InvalidValidationIntegrationRequestError)
    _optional_non_empty(validation_pipeline_ref_id, "validation_pipeline_ref_id", InvalidValidationIntegrationRequestError)
    _optional_non_empty(trace_id, "trace_id", InvalidValidationIntegrationRequestError)
    safe_state_refs = _safe_str_seq(state_ref_ids, "state_ref_ids", InvalidValidationIntegrationRequestError)
    safe_proj_refs = _safe_str_seq(projection_ref_ids, "projection_ref_ids", InvalidValidationIntegrationRequestError)
    safe_hidden_refs = _safe_str_seq(hidden_information_ref_ids, "hidden_information_ref_ids", InvalidValidationIntegrationRequestError)
    safe_gen_refs = _safe_str_seq(generated_content_ref_ids, "generated_content_ref_ids", InvalidValidationIntegrationRequestError)
    if subject_type == "transaction" and transaction_ref_id is None:
        raise InvalidValidationIntegrationRequestError(
            "transaction_ref_id must be present when subject_type is 'transaction'"
        )
    if subject_type == "event_commitment" and event_commitment_ref_id is None:
        raise InvalidValidationIntegrationRequestError(
            "event_commitment_ref_id must be present when subject_type is 'event_commitment'"
        )
    for inv in safe_invs:
        if inv.invariant_family == "generated_content_provenance_invariant" and not safe_gen_refs:
            raise InvalidValidationIntegrationRequestError(
                "generated_content_ref_ids must be non-empty when any invariant family is 'generated_content_provenance_invariant'"
            )
    safe_meta = _safe_meta(metadata, InvalidValidationIntegrationRequestError)
    return ValidationIntegrationRequest(
        validation_request_id=validation_request_id,
        subject_type=subject_type,
        subject_ref_id=subject_ref_id,
        requesting_service=requesting_service,
        requested_stage=requested_stage,
        dependencies=safe_deps,
        invariants=safe_invs,
        transaction_ref_id=transaction_ref_id,
        event_commitment_ref_id=event_commitment_ref_id,
        state_ref_ids=safe_state_refs,
        projection_ref_ids=safe_proj_refs,
        validation_pipeline_ref_id=validation_pipeline_ref_id,
        hidden_information_ref_ids=safe_hidden_refs,
        generated_content_ref_ids=safe_gen_refs,
        trace_id=trace_id,
        metadata=safe_meta,
    )


def create_validation_integration_result(
    validation_request_id: str,
    decision: str,
    final_stage: str,
    subject_type: str,
    subject_ref_id: str,
    validation_result_ref_id: str | None = None,
    invariant_precheck_ref_id: str | None = None,
    failure_routes: Sequence[ValidationFailureRoute] | None = None,
    passed: bool = False,
    blocking: bool = True,
    quarantined: bool = False,
    escalated: bool = False,
    hidden_info_safe: bool = True,
    provenance_checked: bool = False,
    provenance_ref_ids: Sequence[str] | None = None,
    state_mutation_allowed: bool = False,
    event_append_allowed: bool = False,
    persistence_allowed: bool = False,
    model_authority_allowed: bool = False,
    trace_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ValidationIntegrationResult:
    # Runtime validation success for source-local, conversion, or canon-reference
    # subjects is only a backend decision about this runtime reference; it never
    # promotes canon or grants authority beyond the validated reference.
    safe_routes = _safe_obj_seq(
        failure_routes,
        "failure_routes",
        InvalidValidationIntegrationResultError,
        ValidationFailureRoute,
        validate_validation_failure_route,
    )
    safe_provenance_refs = _safe_str_seq(
        provenance_ref_ids,
        "provenance_ref_ids",
        InvalidValidationIntegrationResultError,
    )
    safe_meta = _safe_meta(metadata, InvalidValidationIntegrationResultError)
    result = ValidationIntegrationResult(
        validation_request_id=validation_request_id,
        decision=decision,
        final_stage=final_stage,
        subject_type=subject_type,
        subject_ref_id=subject_ref_id,
        validation_result_ref_id=validation_result_ref_id,
        invariant_precheck_ref_id=invariant_precheck_ref_id,
        failure_routes=safe_routes,
        passed=passed,
        blocking=blocking,
        quarantined=quarantined,
        escalated=escalated,
        hidden_info_safe=hidden_info_safe,
        provenance_checked=provenance_checked,
        provenance_ref_ids=safe_provenance_refs,
        state_mutation_allowed=state_mutation_allowed,
        event_append_allowed=event_append_allowed,
        persistence_allowed=persistence_allowed,
        model_authority_allowed=model_authority_allowed,
        trace_id=trace_id,
        metadata=safe_meta,
    )
    _validate_result_semantics(result, InvalidValidationIntegrationResultError)
    return result


# ---------------------------------------------------------------------------
# Validator helpers
# ---------------------------------------------------------------------------


def validate_validation_integration_dependency(obj: Any) -> bool:
    if not isinstance(obj, ValidationIntegrationDependency):
        return False
    if not isinstance(obj.dependency_id, str) or not obj.dependency_id.strip():
        return False
    if obj.dependency_type not in VALIDATION_DEPENDENCY_TYPES:
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


def validate_validation_invariant_declaration(obj: Any) -> bool:
    if not isinstance(obj, ValidationInvariantDeclaration):
        return False
    if not isinstance(obj.invariant_id, str) or not obj.invariant_id.strip():
        return False
    if obj.invariant_family not in VALIDATION_INVARIANT_FAMILIES:
        return False
    if obj.subject_type not in VALIDATION_SUBJECT_TYPES:
        return False
    if not isinstance(obj.subject_ref_id, str) or not obj.subject_ref_id.strip():
        return False
    if not isinstance(obj.required, bool):
        return False
    if not isinstance(obj.blocking, bool):
        return False
    if not isinstance(obj.backend_only, bool):
        return False
    if not isinstance(obj.hidden_info_safe, bool):
        return False
    if not isinstance(obj.provenance_required, bool):
        return False
    if not obj.backend_only:
        return False
    if not obj.hidden_info_safe and not obj.backend_only:
        return False
    if obj.invariant_family == "generated_content_provenance_invariant" and not obj.provenance_required:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_validation_failure_route(obj: Any) -> bool:
    if not isinstance(obj, ValidationFailureRoute):
        return False
    try:
        _validate_failure_route_fields(obj, InvalidValidationFailureRouteError)
    except InvalidValidationFailureRouteError:
        return False
    return True


def validate_validation_integration_request(obj: Any) -> bool:
    if not isinstance(obj, ValidationIntegrationRequest):
        return False
    if not isinstance(obj.validation_request_id, str) or not obj.validation_request_id.strip():
        return False
    if obj.subject_type not in VALIDATION_SUBJECT_TYPES:
        return False
    if not isinstance(obj.subject_ref_id, str) or not obj.subject_ref_id.strip():
        return False
    if not isinstance(obj.requesting_service, str) or not obj.requesting_service.strip():
        return False
    try:
        _validate_request_stage(obj.requested_stage, InvalidValidationIntegrationRequestError)
    except InvalidValidationIntegrationRequestError:
        return False
    if not isinstance(obj.dependencies, tuple):
        return False
    for dep in obj.dependencies:
        if not isinstance(dep, ValidationIntegrationDependency):
            return False
        if not validate_validation_integration_dependency(dep):
            return False
    if not isinstance(obj.invariants, tuple):
        return False
    for inv in obj.invariants:
        if not isinstance(inv, ValidationInvariantDeclaration):
            return False
        if not validate_validation_invariant_declaration(inv):
            return False
    if obj.transaction_ref_id is not None:
        if not isinstance(obj.transaction_ref_id, str) or not obj.transaction_ref_id.strip():
            return False
    if obj.event_commitment_ref_id is not None:
        if not isinstance(obj.event_commitment_ref_id, str) or not obj.event_commitment_ref_id.strip():
            return False
    if obj.validation_pipeline_ref_id is not None:
        if not isinstance(obj.validation_pipeline_ref_id, str) or not obj.validation_pipeline_ref_id.strip():
            return False
    if obj.trace_id is not None:
        if not isinstance(obj.trace_id, str) or not obj.trace_id.strip():
            return False
    for field_name in ("state_ref_ids", "projection_ref_ids", "hidden_information_ref_ids", "generated_content_ref_ids"):
        val = getattr(obj, field_name)
        if not isinstance(val, tuple):
            return False
        for item in val:
            if not isinstance(item, str) or not item.strip():
                return False
    if obj.subject_type == "transaction" and obj.transaction_ref_id is None:
        return False
    if obj.subject_type == "event_commitment" and obj.event_commitment_ref_id is None:
        return False
    for inv in obj.invariants:
        if inv.invariant_family == "generated_content_provenance_invariant" and not obj.generated_content_ref_ids:
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


def validate_validation_integration_result(obj: Any) -> bool:
    if not isinstance(obj, ValidationIntegrationResult):
        return False
    try:
        _validate_result_semantics(obj, InvalidValidationIntegrationResultError)
    except InvalidValidationIntegrationResultError:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    return True


# ---------------------------------------------------------------------------
# Stateless service wrapper
# ---------------------------------------------------------------------------


class ValidationIntegrationService:
    """Stateless wrapper around validation integration creation/validation helpers."""

    def create_dependency(self, **kwargs: Any) -> ValidationIntegrationDependency:
        return create_validation_integration_dependency(**kwargs)

    def create_invariant_declaration(self, **kwargs: Any) -> ValidationInvariantDeclaration:
        return create_validation_invariant_declaration(**kwargs)

    def create_request(self, **kwargs: Any) -> ValidationIntegrationRequest:
        return create_validation_integration_request(**kwargs)

    def create_result(self, **kwargs: Any) -> ValidationIntegrationResult:
        return create_validation_integration_result(**kwargs)

    def create_failure_route(self, **kwargs: Any) -> ValidationFailureRoute:
        return create_validation_failure_route(**kwargs)

    def validate_dependency(self, obj: Any) -> bool:
        return validate_validation_integration_dependency(obj)

    def validate_invariant_declaration(self, obj: Any) -> bool:
        return validate_validation_invariant_declaration(obj)

    def validate_request(self, obj: Any) -> bool:
        return validate_validation_integration_request(obj)

    def validate_result(self, obj: Any) -> bool:
        return validate_validation_integration_result(obj)

    def validate_failure_route(self, obj: Any) -> bool:
        return validate_validation_failure_route(obj)
