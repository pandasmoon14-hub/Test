"""Resource and consequence math skeleton — RT-002 reference-only shapes.

This module provides immutable, keyword-only dataclasses for declaring
resource/cost/consequence math requests, results, and settlement proposals.
It does not execute arithmetic, affordability, reservation, settlement,
consequence application, state mutation, event commitment, persistence,
replay, RNG/table/oracle execution, live-play behavior, UI behavior,
conversion, sourcebook inclusion, or canon promotion.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


RESOURCE_MATH_SUBJECT_TYPES = frozenset({
    "actor",
    "command",
    "action",
    "item",
    "asset",
    "vehicle",
    "mission",
    "faction",
    "location",
    "state_record",
    "generated_content",
    "resource_owner",
    "source_local_subject",
    "unknown_pending_review",
})

RESOURCE_MATH_SUBJECT_ROLES = frozenset({
    "primary_subject",
    "payer_subject",
    "beneficiary_subject",
    "resource_owner",
    "affected_subject",
    "source_subject",
    "target_subject",
    "authority_source",
    "provenance_source",
})

RESOURCE_MATH_OWNER_DOMAINS = frozenset({
    "RT001_command_lifecycle_action_legality",
    "RT002_resource_consequence_math",
    "RT003_combat_hazard_damage_recovery",
    "RT004_ability_effect_skill_binding",
    "RT005_context_packet_hidden_information",
    "RT006_mission_reward_clue_routing",
    "RT007_social_faction_actor_knowledge",
    "RT008_generated_content_provenance_recurrence",
    "RT009_runtime_rng_table_oracle",
    "RT010_inventory_item_vehicle_asset",
    "RT011_validation_readiness_tooling",
    "RT012_d_series_promotion_boundary",
    "source_local_owner",
    "doctrine_escalation",
})

VISIBILITY_POLICIES = frozenset({
    "public",
    "actor_visible",
    "narrator_only",
    "hidden",
    "redacted",
    "delayed_reveal",
    "derived_only",
})

RESOURCE_FAMILIES = frozenset({
    "pooled_expendable",
    "scene_counter",
    "charge",
    "currency_like",
    "material",
    "asset_integrity",
    "vehicle_integrity",
    "time_window",
    "opportunity",
    "social_capital",
    "faction_standing",
    "clue_information",
    "risk_heat",
    "strain_corruption",
    "injury_recovery",
    "cooldown",
    "debt_obligation",
    "source_local_resource",
})

QUANTITY_REPRESENTATION_KINDS = frozenset({
    "integer_exact",
    "decimal_exact",
    "fraction_exact",
    "fixed_point_scaled",
    "source_literal_only",
    "blocked_pending_numeric_choice",
})

CONVERSION_POLICIES = frozenset({
    "no_conversion",
    "exact_conversion",
    "table_driven_conversion",
    "doctrine_approved_conversion",
    "source_local_conversion",
    "escalation_required",
})

ROUNDING_POLICIES = frozenset({
    "no_rounding",
    "round_down",
    "round_up",
    "round_nearest",
    "round_toward_zero",
    "round_away_from_zero",
    "tie_to_even",
    "tie_away_from_zero",
    "blocked_pending_rounding_choice",
})

QUANTITY_NEGATIVE_VALUE_POLICIES = frozenset({
    "negative_values_forbidden",
    "negative_values_allowed_by_source",
    "negative_values_require_owner_handoff",
})

RESOURCE_MATH_DEPENDENCY_TYPES = frozenset({
    "command_ref",
    "action_legality_ref",
    "state_snapshot_ref",
    "state_record_ref",
    "state_projection_ref",
    "state_delta_ref",
    "transaction_ref",
    "transaction_preview_ref",
    "event_commitment_ref",
    "event_record_ref",
    "validation_request_ref",
    "validation_result_ref",
    "runtime_trace_ref",
    "hidden_information_ref",
    "context_projection_ref",
    "provenance_ref",
    "rng_request_ref",
    "rng_result_ref",
    "table_oracle_ref",
    "table_oracle_result_ref",
    "owner_handoff_ref",
    "registry_ref",
    "decision_log_ref",
    "subject_ref",
    "unit_ref",
    "dimension_ref",
    "resource_math_request_ref",
    "resource_math_result_ref",
    "rollback_accounting_ref",
})

COST_FAMILIES = frozenset({
    "activation",
    "upkeep",
    "maintenance",
    "opportunity",
    "prerequisite_lock",
    "reservation_hold",
    "partial_payment",
    "substitution",
    "overcommitment",
    "debt_creation",
    "success_at_cost",
    "failure_at_cost",
    "cancellation",
    "interruption",
    "refund",
    "reversal",
    "compensation",
    "repair",
    "recovery",
    "crafting",
    "salvage",
    "requisition",
    "validation_blocked",
})

CONSEQUENCE_FAMILIES = frozenset({
    "gain",
    "loss",
    "transfer",
    "lock",
    "unlock",
    "exposure",
    "exhaustion",
    "degradation",
    "escalation",
    "cooldown",
    "debt",
    "obligation",
    "harm_pressure",
    "recovery_pressure",
    "visibility_change",
    "mission_route",
    "clue_route",
    "social_faction_change",
    "inventory_asset_change",
    "provenance_recurrence",
    "quarantine_escalation",
})

COST_TIMING_POLICIES = frozenset({
    "pay_before_resolution",
    "reserve_before_resolution",
    "pay_on_attempt",
    "pay_on_success",
    "pay_on_failure",
    "pay_on_commitment",
    "pay_over_time",
    "upkeep_interval",
    "refund_on_cancel",
    "no_refund_on_interrupt",
    "compensate_after_rollback",
    "blocked_pending_validation",
})

COST_OUTCOME_POLICIES = frozenset({
    "success",
    "failure",
    "partial_success",
    "cancelled",
    "interrupted",
    "invalid",
    "validation_blocked",
    "owner_blocked",
    "quarantined",
    "escalated",
    "rollback_required",
})

RESOURCE_TERM_VALUE_MODES = frozenset({
    "resource_quantity",
    "resource_reference_only",
    "quantity_only",
    "policy_only",
})

RESOURCE_TERM_POLICY_ROUTES = frozenset({
    "owner_handoff_required",
    "quarantine_required",
    "doctrine_escalation_required",
})

ATOMICITY_POLICIES = frozenset({
    "all_or_nothing_requested",
    "best_effort_requested",
    "ordered_partial_allowed",
    "unordered_partial_allowed",
    "alternative_exactly_one",
    "alternative_at_least_one",
    "alternative_at_most_one",
    "alternative_any",
    "invalid_mixed_atomicity",
    "blocked_pending_transaction_policy",
})

ORDERING_POLICIES = frozenset({
    "unordered_terms",
    "source_ordered_terms",
    "dependency_ordered_terms",
    "priority_ordered_terms",
    "blocked_pending_ordering_policy",
})

PARTIAL_SETTLEMENT_POLICIES = frozenset({
    "no_partial_settlement",
    "partial_settlement_allowed",
    "partial_settlement_requires_owner_review",
    "partial_settlement_requires_validation",
    "blocked_pending_settlement_policy",
})

RESOURCE_MATH_STAGES = frozenset({
    "resource_math_requested",
    "source_declaration_captured",
    "subject_refs_bound",
    "resource_refs_declared",
    "quantity_specs_declared",
    "terms_declared",
    "bundle_structure_declared",
    "policy_refs_declared",
    "dependency_refs_bound",
    "calculation_ready_for_review",
    "blocked_pending_validation",
    "blocked_pending_owner_handoff",
    "quarantined_for_review",
    "escalated_to_doctrine",
})

RESOURCE_MATH_DECISIONS = frozenset({
    "accepted_for_planning",
    "normalized_for_planning",
    "source_local_retained",
    "requires_validation_review",
    "requires_owner_handoff",
    "blocked_missing_dependency",
    "blocked_incompatible_policy",
    "blocked_hidden_information",
    "quarantined_for_review",
    "escalated_to_doctrine",
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


class ResourceMathError(Exception):
    """Base error for resource and consequence math operations."""


class InvalidResourceMathSubjectReferenceError(ResourceMathError):
    """Raised when a ResourceMathSubjectReference fails validation."""


class InvalidResourceReferenceError(ResourceMathError):
    """Raised when a ResourceReference fails validation."""


class InvalidQuantitySpecificationError(ResourceMathError):
    """Raised when a QuantitySpecification fails validation."""


class InvalidResourceMathDependencyError(ResourceMathError):
    """Raised when a ResourceMathDependency fails validation."""


class InvalidCostTermError(ResourceMathError):
    """Raised when a CostTerm fails validation."""


class InvalidConsequenceTermError(ResourceMathError):
    """Raised when a ConsequenceTerm fails validation."""


class InvalidCostBundleError(ResourceMathError):
    """Raised when a CostBundle fails validation."""


class InvalidResourceMathRequestError(ResourceMathError):
    """Raised when a ResourceMathRequest fails validation."""


class InvalidResourceMathResultError(ResourceMathError):
    """Raised when a ResourceMathResult fails validation."""


class InvalidSettlementProposalError(ResourceMathError):
    """Raised when a SettlementProposal fails validation."""


_RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS: tuple[str, ...] = (
    "calculation_executed",
    "affordability_executed",
    "reservation_authorized",
    "settlement_authorized",
    "consequence_application_authorized",
    "mutation_authorized",
    "state_delta_application_authorized",
    "transaction_execution_authorized",
    "event_commitment_authorized",
    "event_append_authorized",
    "persistence_authorized",
    "replay_authorized",
    "rng_execution_authorized",
    "table_oracle_execution_authorized",
    "model_authority_authorized",
    "live_play_authorized",
    "ui_authorized",
    "conversion_authorized",
    "canon_promotion_authorized",
)


def _validate_non_empty_string(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> None:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string")


def _normalize_string_tuple(
    values: Sequence[str] | None,
    name: str,
    error_cls: type[Exception],
) -> tuple[str, ...]:
    if values is None:
        return ()
    if isinstance(values, str):
        raise error_cls(f"{name} must not be a bare string")
    if not isinstance(values, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[str] = []
    for i, item in enumerate(values):
        if not isinstance(item, str) or not item.strip():
            raise error_cls(f"{name}[{i}] must be a non-empty string")
        result.append(item)
    return tuple(result)


def _safe_metadata(
    metadata: Mapping[str, Any] | None,
    error_cls: type[Exception],
) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    copied: dict[str, Any] = {}
    for key, value in metadata.items():
        if callable(value):
            raise error_cls("metadata values must not be callable")
        copied[key] = copy.deepcopy(value)
    return MappingProxyType(copied)


def _validate_optional_non_empty_string(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> None:
    if value is not None:
        _validate_non_empty_string(value, name, error_cls)


def _validate_non_bool_positive_int(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        raise error_cls(f"{name} must be an int")
    if value <= 0:
        raise error_cls(f"{name} must be a positive integer")


def _validate_non_bool_non_negative_int(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        raise error_cls(f"{name} must be an int")
    if value < 0:
        raise error_cls(f"{name} must be a non-negative integer")


def _validate_bool(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> None:
    if not isinstance(value, bool):
        raise error_cls(f"{name} must be a bool")


def _validate_optional_positive_non_bool_int(
    value: Any,
    name: str,
    error_cls: type[Exception],
) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        raise error_cls(f"{name} must be an int or None")
    if value <= 0:
        raise error_cls(f"{name} must be a positive integer")


def _normalize_alternative_groups(
    groups: Sequence[tuple[str, Sequence[str]]] | None,
    term_ids: tuple[str, ...],
    error_cls: type[Exception],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    if groups is None:
        return ()
    if isinstance(groups, str):
        raise error_cls("alternative_groups must not be a bare string")
    if not isinstance(groups, Sequence):
        raise error_cls("alternative_groups must be a sequence")

    seen_group_ids: set[str] = set()
    seen_term_ids: set[str] = set()
    result: list[tuple[str, tuple[str, ...]]] = []
    term_id_set = set(term_ids)

    for i, group in enumerate(groups):
        if not isinstance(group, tuple) or len(group) != 2:
            raise error_cls(f"alternative_groups[{i}] must be a tuple of (group_id, terms)")
        group_id, terms = group
        if not isinstance(group_id, str) or not group_id.strip():
            raise error_cls(f"alternative_groups[{i}] group_id must be a non-empty string")
        if group_id in seen_group_ids:
            raise error_cls(f"alternative_groups[{i}] group_id is duplicated: {group_id!r}")
        seen_group_ids.add(group_id)

        if isinstance(terms, str):
            raise error_cls(f"alternative_groups[{i}] terms must not be a bare string")
        if not isinstance(terms, Sequence):
            raise error_cls(f"alternative_groups[{i}] terms must be a sequence")
        if len(terms) == 0:
            raise error_cls(f"alternative_groups[{i}] terms must not be empty")

        normalized_terms: list[str] = []
        group_seen: set[str] = set()
        for j, term_id in enumerate(terms):
            if not isinstance(term_id, str) or not term_id.strip():
                raise error_cls(
                    f"alternative_groups[{i}] terms[{j}] must be a non-empty string"
                )
            if term_id in group_seen:
                raise error_cls(
                    f"alternative_groups[{i}] terms[{j}] is duplicated: {term_id!r}"
                )
            if term_id not in term_id_set:
                raise error_cls(
                    f"alternative_groups[{i}] terms[{j}] {term_id!r} is not in term_ids"
                )
            if term_id in seen_term_ids:
                raise error_cls(
                    f"alternative_groups[{i}] terms[{j}] {term_id!r} overlaps another group"
                )
            group_seen.add(term_id)
            seen_term_ids.add(term_id)
            normalized_terms.append(term_id)

        result.append((group_id, tuple(normalized_terms)))

    return tuple(result)


def _validate_false_only_authority_fields(
    kwargs: Mapping[str, Any],
    error_cls: type[Exception],
) -> None:
    """Reject any true value in request false-only authority fields."""
    for field_name in _RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS:
        value = kwargs.get(field_name, False)
        if value is not False:
            raise error_cls(f"{field_name} must be False")


def _normalize_dataclass_tuple(
    values: Sequence[Any] | None,
    name: str,
    expected_cls: type[Any],
    error_cls: type[Exception],
) -> tuple[Any, ...]:
    if values is None:
        return ()
    if isinstance(values, str):
        raise error_cls(f"{name} must not be a bare string")
    if not isinstance(values, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[Any] = []
    for i, item in enumerate(values):
        if not isinstance(item, expected_cls):
            raise error_cls(f"{name}[{i}] must be a {expected_cls.__name__}")
        result.append(item)
    return tuple(result)


def _validate_unique_attr(
    items: Sequence[Any],
    attr_name: str,
    collection_name: str,
    error_cls: type[Exception],
) -> set[str]:
    seen: set[str] = set()
    for item in items:
        value = getattr(item, attr_name)
        if value in seen:
            raise error_cls(
                f"{collection_name} has duplicate {attr_name}: {value!r}"
            )
        seen.add(value)
    return seen


def _validate_exactly_one_primary_subject(
    subjects: Sequence[ResourceMathSubjectReference],
    error_cls: type[Exception],
) -> None:
    primary_count = sum(1 for s in subjects if s.subject_role == "primary_subject")
    if primary_count == 0:
        raise error_cls("subject_refs must contain exactly one primary_subject")
    if primary_count > 1:
        raise error_cls(
            f"subject_refs must contain exactly one primary_subject, found {primary_count}"
        )


def _validate_same_request_reference(
    value: str | None,
    name: str,
    valid_ids: set[str],
    error_cls: type[Exception],
) -> None:
    if value is not None and value not in valid_ids:
        raise error_cls(f"{name} {value!r} does not resolve in this request")


_STAGE_DECISION_MATRIX: dict[str, tuple[str, ...]] = {
    "accepted_for_planning": (
        "resource_math_requested",
        "calculation_ready_for_review",
    ),
    "normalized_for_planning": (
        "source_declaration_captured",
        "subject_refs_bound",
        "resource_refs_declared",
        "quantity_specs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared",
        "dependency_refs_bound",
        "calculation_ready_for_review",
    ),
    "source_local_retained": (
        "source_declaration_captured",
        "resource_refs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared",
    ),
    "requires_validation_review": ("blocked_pending_validation",),
    "requires_owner_handoff": ("blocked_pending_owner_handoff",),
    "blocked_missing_dependency": (
        "dependency_refs_bound",
        "blocked_pending_validation",
        "blocked_pending_owner_handoff",
    ),
    "blocked_incompatible_policy": ("policy_refs_declared",),
    "blocked_hidden_information": (
        "dependency_refs_bound",
        "blocked_pending_validation",
    ),
    "quarantined_for_review": ("quarantined_for_review",),
    "escalated_to_doctrine": ("escalated_to_doctrine",),
}

_NON_BLOCKING_DECISIONS = frozenset({
    "accepted_for_planning",
    "normalized_for_planning",
    "source_local_retained",
})


def _validate_stage_decision_compatibility(
    stage: str,
    decision: str,
    blocking: bool,
    quarantined: bool,
    escalated: bool,
    error_cls: type[Exception],
) -> None:
    allowed_stages = _STAGE_DECISION_MATRIX.get(decision)
    if allowed_stages is None or stage not in allowed_stages:
        raise error_cls(
            f"stage {stage!r} is not allowed for decision {decision!r}"
        )

    expected_blocking = decision not in _NON_BLOCKING_DECISIONS
    if blocking is not expected_blocking:
        raise error_cls(
            f"blocking must be {expected_blocking} for decision {decision!r}, got {blocking!r}"
        )

    is_quarantine_pair = (
        stage == "quarantined_for_review" and decision == "quarantined_for_review"
    )
    is_escalation_pair = (
        stage == "escalated_to_doctrine" and decision == "escalated_to_doctrine"
    )

    if quarantined and not is_quarantine_pair:
        raise error_cls(
            "quarantined=True is only valid for quarantined_for_review stage/decision"
        )
    if not quarantined and is_quarantine_pair:
        raise error_cls(
            "quarantined must be True for quarantined_for_review stage/decision"
        )

    if escalated and not is_escalation_pair:
        raise error_cls(
            "escalated=True is only valid for escalated_to_doctrine stage/decision"
        )
    if not escalated and is_escalation_pair:
        raise error_cls(
            "escalated must be True for escalated_to_doctrine stage/decision"
        )


def _normalize_unique_string_tuple(
    values: Sequence[str] | None,
    name: str,
    error_cls: type[Exception],
) -> tuple[str, ...]:
    if values is None:
        return ()
    if isinstance(values, str):
        raise error_cls(f"{name} must not be a bare string")
    if not isinstance(values, Sequence):
        raise error_cls(f"{name} must be a sequence")
    seen: set[str] = set()
    result: list[str] = []
    for i, item in enumerate(values):
        if not isinstance(item, str) or not item.strip():
            raise error_cls(f"{name}[{i}] must be a non-empty string")
        if item in seen:
            raise error_cls(f"{name}[{i}] is duplicated: {item!r}")
        seen.add(item)
        result.append(item)
    return tuple(result)


def _normalize_state_delta_refs(
    values: Sequence[str] | None,
    error_cls: type[Exception],
) -> tuple[str, ...]:
    if values is None:
        raise error_cls("proposed_state_delta_refs must not be empty")
    if isinstance(values, str):
        raise error_cls("proposed_state_delta_refs must not be a bare string")
    if not isinstance(values, Sequence):
        raise error_cls("proposed_state_delta_refs must be a sequence")
    if len(values) == 0:
        raise error_cls("proposed_state_delta_refs must not be empty")
    seen: set[str] = set()
    result: list[str] = []
    for i, item in enumerate(values):
        if not isinstance(item, str) or not item.strip():
            raise error_cls(f"proposed_state_delta_refs[{i}] must be a non-empty string")
        if item in seen:
            raise error_cls(
                f"proposed_state_delta_refs[{i}] is duplicated: {item!r}"
            )
        seen.add(item)
        result.append(item)
    return tuple(result)


def _validate_dependencies_satisfied(
    dependencies: Sequence[ResourceMathDependency],
    error_cls: type[Exception],
) -> None:
    for dep in dependencies:
        if dep.required and not dep.satisfied:
            raise error_cls(
                f"dependency {dep.dependency_id!r} is required but not satisfied"
            )


def _validate_term_value_mode_shape(
    value_mode: str,
    resource_ref_id: str | None,
    quantity_id: str | None,
    policy_route: str | None,
    error_cls: type[Exception],
) -> None:
    """Enforce PR-5H term_value_mode_matrix structural rules.

    This checks presence/absence and policy-route membership only; it does not
    dereference same-request IDs.
    """
    if value_mode == "resource_quantity":
        if resource_ref_id is None:
            raise error_cls("resource_ref_id is required for resource_quantity value_mode")
        if quantity_id is None:
            raise error_cls("quantity_id is required for resource_quantity value_mode")
        if policy_route is not None:
            raise error_cls("policy_route must be None for resource_quantity value_mode")
    elif value_mode == "resource_reference_only":
        if resource_ref_id is None:
            raise error_cls("resource_ref_id is required for resource_reference_only value_mode")
        if quantity_id is not None:
            raise error_cls("quantity_id must be None for resource_reference_only value_mode")
        if policy_route is not None:
            raise error_cls("policy_route must be None for resource_reference_only value_mode")
    elif value_mode == "quantity_only":
        if resource_ref_id is not None:
            raise error_cls("resource_ref_id must be None for quantity_only value_mode")
        if quantity_id is None:
            raise error_cls("quantity_id is required for quantity_only value_mode")
        if policy_route is not None:
            raise error_cls("policy_route must be None for quantity_only value_mode")
    elif value_mode == "policy_only":
        if resource_ref_id is not None:
            raise error_cls("resource_ref_id must be None for policy_only value_mode")
        if quantity_id is not None:
            raise error_cls("quantity_id must be None for policy_only value_mode")
        if policy_route is None:
            raise error_cls("policy_route is required for policy_only value_mode")
        if policy_route not in RESOURCE_TERM_POLICY_ROUTES:
            raise error_cls(
                f"policy_route must be one of {sorted(RESOURCE_TERM_POLICY_ROUTES)}, "
                f"got: {policy_route!r}"
            )


@dataclass(frozen=True, kw_only=True)
class ResourceMathSubjectReference:
    """Immutable subject reference inside a resource-math request."""

    subject_binding_id: str
    subject_type: str
    subject_ref_id: str
    subject_role: str
    owner_domain: str
    visibility_policy: str = "public"
    provenance_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_binding_id": self.subject_binding_id,
            "subject_type": self.subject_type,
            "subject_ref_id": self.subject_ref_id,
            "subject_role": self.subject_role,
            "owner_domain": self.owner_domain,
            "visibility_policy": self.visibility_policy,
            "provenance_refs": list(self.provenance_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_resource_math_subject_reference(
    *,
    subject_binding_id: str,
    subject_type: str,
    subject_ref_id: str,
    subject_role: str,
    owner_domain: str,
    visibility_policy: str = "public",
    provenance_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ResourceMathSubjectReference:
    """Create a validated ResourceMathSubjectReference."""
    error_cls = InvalidResourceMathSubjectReferenceError

    _validate_non_empty_string(subject_binding_id, "subject_binding_id", error_cls)
    _validate_non_empty_string(subject_type, "subject_type", error_cls)
    if subject_type not in RESOURCE_MATH_SUBJECT_TYPES:
        raise error_cls(
            f"subject_type must be one of {sorted(RESOURCE_MATH_SUBJECT_TYPES)}, "
            f"got: {subject_type!r}"
        )
    _validate_non_empty_string(subject_ref_id, "subject_ref_id", error_cls)
    _validate_non_empty_string(subject_role, "subject_role", error_cls)
    if subject_role not in RESOURCE_MATH_SUBJECT_ROLES:
        raise error_cls(
            f"subject_role must be one of {sorted(RESOURCE_MATH_SUBJECT_ROLES)}, "
            f"got: {subject_role!r}"
        )
    _validate_non_empty_string(owner_domain, "owner_domain", error_cls)
    if owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        raise error_cls(
            f"owner_domain must be one of {sorted(RESOURCE_MATH_OWNER_DOMAINS)}, "
            f"got: {owner_domain!r}"
        )
    _validate_non_empty_string(visibility_policy, "visibility_policy", error_cls)
    if visibility_policy not in VISIBILITY_POLICIES:
        raise error_cls(
            f"visibility_policy must be one of {sorted(VISIBILITY_POLICIES)}, "
            f"got: {visibility_policy!r}"
        )

    safe_provenance_refs = _normalize_string_tuple(
        provenance_refs, "provenance_refs", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    return ResourceMathSubjectReference(
        subject_binding_id=subject_binding_id,
        subject_type=subject_type,
        subject_ref_id=subject_ref_id,
        subject_role=subject_role,
        owner_domain=owner_domain,
        visibility_policy=visibility_policy,
        provenance_refs=safe_provenance_refs,
        metadata=safe_metadata,
    )


def validate_resource_math_subject_reference(value: object) -> bool:
    if not isinstance(value, ResourceMathSubjectReference):
        return False
    if not isinstance(value.subject_binding_id, str) or not value.subject_binding_id.strip():
        return False
    if value.subject_type not in RESOURCE_MATH_SUBJECT_TYPES:
        return False
    if not isinstance(value.subject_ref_id, str) or not value.subject_ref_id.strip():
        return False
    if value.subject_role not in RESOURCE_MATH_SUBJECT_ROLES:
        return False
    if value.owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        return False
    if value.visibility_policy not in VISIBILITY_POLICIES:
        return False
    if not isinstance(value.provenance_refs, tuple):
        return False
    for ref in value.provenance_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True, kw_only=True)
class ResourceReference:
    """Immutable resource reference inside a resource-math request."""

    resource_ref_id: str
    subject_binding_id: str
    resource_family: str
    resource_key: str
    owner_domain: str
    source_label: str | None = None
    source_aliases: tuple[str, ...] = ()
    visibility_policy: str = "public"
    unit_ref_id: str | None = None
    dimension_ref_id: str | None = None
    provenance_refs: tuple[str, ...] = ()
    source_local: bool = False
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "resource_ref_id": self.resource_ref_id,
            "subject_binding_id": self.subject_binding_id,
            "resource_family": self.resource_family,
            "resource_key": self.resource_key,
            "owner_domain": self.owner_domain,
            "source_label": self.source_label,
            "source_aliases": list(self.source_aliases),
            "visibility_policy": self.visibility_policy,
            "unit_ref_id": self.unit_ref_id,
            "dimension_ref_id": self.dimension_ref_id,
            "provenance_refs": list(self.provenance_refs),
            "source_local": self.source_local,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_resource_reference(
    *,
    resource_ref_id: str,
    subject_binding_id: str,
    resource_family: str,
    resource_key: str,
    owner_domain: str,
    source_label: str | None = None,
    source_aliases: Sequence[str] | None = None,
    visibility_policy: str = "public",
    unit_ref_id: str | None = None,
    dimension_ref_id: str | None = None,
    provenance_refs: Sequence[str] | None = None,
    source_local: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> ResourceReference:
    """Create a validated ResourceReference."""
    error_cls = InvalidResourceReferenceError

    _validate_non_empty_string(resource_ref_id, "resource_ref_id", error_cls)
    _validate_non_empty_string(subject_binding_id, "subject_binding_id", error_cls)
    _validate_non_empty_string(resource_family, "resource_family", error_cls)
    if resource_family not in RESOURCE_FAMILIES:
        raise error_cls(
            f"resource_family must be one of {sorted(RESOURCE_FAMILIES)}, "
            f"got: {resource_family!r}"
        )
    _validate_non_empty_string(resource_key, "resource_key", error_cls)
    _validate_non_empty_string(owner_domain, "owner_domain", error_cls)
    if owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        raise error_cls(
            f"owner_domain must be one of {sorted(RESOURCE_MATH_OWNER_DOMAINS)}, "
            f"got: {owner_domain!r}"
        )
    _validate_optional_non_empty_string(source_label, "source_label", error_cls)
    _validate_non_empty_string(visibility_policy, "visibility_policy", error_cls)
    if visibility_policy not in VISIBILITY_POLICIES:
        raise error_cls(
            f"visibility_policy must be one of {sorted(VISIBILITY_POLICIES)}, "
            f"got: {visibility_policy!r}"
        )
    _validate_optional_non_empty_string(unit_ref_id, "unit_ref_id", error_cls)
    _validate_optional_non_empty_string(dimension_ref_id, "dimension_ref_id", error_cls)
    _validate_bool(source_local, "source_local", error_cls)

    safe_source_aliases = _normalize_string_tuple(
        source_aliases, "source_aliases", error_cls
    )
    safe_provenance_refs = _normalize_string_tuple(
        provenance_refs, "provenance_refs", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    return ResourceReference(
        resource_ref_id=resource_ref_id,
        subject_binding_id=subject_binding_id,
        resource_family=resource_family,
        resource_key=resource_key,
        owner_domain=owner_domain,
        source_label=source_label,
        source_aliases=safe_source_aliases,
        visibility_policy=visibility_policy,
        unit_ref_id=unit_ref_id,
        dimension_ref_id=dimension_ref_id,
        provenance_refs=safe_provenance_refs,
        source_local=source_local,
        metadata=safe_metadata,
    )


def validate_resource_reference(value: object) -> bool:
    if not isinstance(value, ResourceReference):
        return False
    if not isinstance(value.resource_ref_id, str) or not value.resource_ref_id.strip():
        return False
    if not isinstance(value.subject_binding_id, str) or not value.subject_binding_id.strip():
        return False
    if value.resource_family not in RESOURCE_FAMILIES:
        return False
    if not isinstance(value.resource_key, str) or not value.resource_key.strip():
        return False
    if value.owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        return False
    if value.source_label is not None and (
        not isinstance(value.source_label, str) or not value.source_label.strip()
    ):
        return False
    if value.visibility_policy not in VISIBILITY_POLICIES:
        return False
    if value.unit_ref_id is not None and (
        not isinstance(value.unit_ref_id, str) or not value.unit_ref_id.strip()
    ):
        return False
    if value.dimension_ref_id is not None and (
        not isinstance(value.dimension_ref_id, str) or not value.dimension_ref_id.strip()
    ):
        return False
    if not isinstance(value.source_aliases, tuple):
        return False
    for alias in value.source_aliases:
        if not isinstance(alias, str) or not alias.strip():
            return False
    if not isinstance(value.provenance_refs, tuple):
        return False
    for ref in value.provenance_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.source_local, bool):
        return False
    if not isinstance(value.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True, kw_only=True)
class QuantitySpecification:
    """Immutable quantity specification inside a resource-math request."""

    quantity_id: str
    representation_kind: str
    magnitude_text: str | None = None
    source_literal: str | None = None
    precision: int | None = None
    scale: int | None = None
    unit_ref_id: str | None = None
    dimension_ref_id: str | None = None
    conversion_policy: str = "no_conversion"
    rounding_policy: str = "no_rounding"
    negative_value_policy: str = "negative_values_forbidden"
    visibility_policy: str = "public"
    provenance_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "quantity_id": self.quantity_id,
            "representation_kind": self.representation_kind,
            "magnitude_text": self.magnitude_text,
            "source_literal": self.source_literal,
            "precision": self.precision,
            "scale": self.scale,
            "unit_ref_id": self.unit_ref_id,
            "dimension_ref_id": self.dimension_ref_id,
            "conversion_policy": self.conversion_policy,
            "rounding_policy": self.rounding_policy,
            "negative_value_policy": self.negative_value_policy,
            "visibility_policy": self.visibility_policy,
            "provenance_refs": list(self.provenance_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_quantity_specification(
    *,
    quantity_id: str,
    representation_kind: str,
    magnitude_text: str | None = None,
    source_literal: str | None = None,
    precision: int | None = None,
    scale: int | None = None,
    unit_ref_id: str | None = None,
    dimension_ref_id: str | None = None,
    conversion_policy: str = "no_conversion",
    rounding_policy: str = "no_rounding",
    negative_value_policy: str = "negative_values_forbidden",
    visibility_policy: str = "public",
    provenance_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> QuantitySpecification:
    """Create a validated QuantitySpecification."""
    error_cls = InvalidQuantitySpecificationError

    _validate_non_empty_string(quantity_id, "quantity_id", error_cls)
    _validate_non_empty_string(representation_kind, "representation_kind", error_cls)
    if representation_kind not in QUANTITY_REPRESENTATION_KINDS:
        raise error_cls(
            f"representation_kind must be one of "
            f"{sorted(QUANTITY_REPRESENTATION_KINDS)}, got: {representation_kind!r}"
        )
    _validate_optional_non_empty_string(magnitude_text, "magnitude_text", error_cls)
    _validate_optional_non_empty_string(source_literal, "source_literal", error_cls)
    _validate_non_bool_positive_int(precision, "precision", error_cls)
    _validate_non_bool_non_negative_int(scale, "scale", error_cls)
    _validate_optional_non_empty_string(unit_ref_id, "unit_ref_id", error_cls)
    _validate_optional_non_empty_string(dimension_ref_id, "dimension_ref_id", error_cls)
    _validate_non_empty_string(conversion_policy, "conversion_policy", error_cls)
    if conversion_policy not in CONVERSION_POLICIES:
        raise error_cls(
            f"conversion_policy must be one of {sorted(CONVERSION_POLICIES)}, "
            f"got: {conversion_policy!r}"
        )
    _validate_non_empty_string(rounding_policy, "rounding_policy", error_cls)
    if rounding_policy not in ROUNDING_POLICIES:
        raise error_cls(
            f"rounding_policy must be one of {sorted(ROUNDING_POLICIES)}, "
            f"got: {rounding_policy!r}"
        )
    _validate_non_empty_string(negative_value_policy, "negative_value_policy", error_cls)
    if negative_value_policy not in QUANTITY_NEGATIVE_VALUE_POLICIES:
        raise error_cls(
            f"negative_value_policy must be one of "
            f"{sorted(QUANTITY_NEGATIVE_VALUE_POLICIES)}, "
            f"got: {negative_value_policy!r}"
        )
    _validate_non_empty_string(visibility_policy, "visibility_policy", error_cls)
    if visibility_policy not in VISIBILITY_POLICIES:
        raise error_cls(
            f"visibility_policy must be one of {sorted(VISIBILITY_POLICIES)}, "
            f"got: {visibility_policy!r}"
        )

    safe_provenance_refs = _normalize_string_tuple(
        provenance_refs, "provenance_refs", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    return QuantitySpecification(
        quantity_id=quantity_id,
        representation_kind=representation_kind,
        magnitude_text=magnitude_text,
        source_literal=source_literal,
        precision=precision,
        scale=scale,
        unit_ref_id=unit_ref_id,
        dimension_ref_id=dimension_ref_id,
        conversion_policy=conversion_policy,
        rounding_policy=rounding_policy,
        negative_value_policy=negative_value_policy,
        visibility_policy=visibility_policy,
        provenance_refs=safe_provenance_refs,
        metadata=safe_metadata,
    )


def validate_quantity_specification(value: object) -> bool:
    if not isinstance(value, QuantitySpecification):
        return False
    if not isinstance(value.quantity_id, str) or not value.quantity_id.strip():
        return False
    if value.representation_kind not in QUANTITY_REPRESENTATION_KINDS:
        return False
    if value.magnitude_text is not None and (
        not isinstance(value.magnitude_text, str) or not value.magnitude_text.strip()
    ):
        return False
    if value.source_literal is not None and (
        not isinstance(value.source_literal, str) or not value.source_literal.strip()
    ):
        return False
    if value.precision is not None and (
        isinstance(value.precision, bool)
        or not isinstance(value.precision, int)
        or value.precision <= 0
    ):
        return False
    if value.scale is not None and (
        isinstance(value.scale, bool)
        or not isinstance(value.scale, int)
        or value.scale < 0
    ):
        return False
    if value.unit_ref_id is not None and (
        not isinstance(value.unit_ref_id, str) or not value.unit_ref_id.strip()
    ):
        return False
    if value.dimension_ref_id is not None and (
        not isinstance(value.dimension_ref_id, str) or not value.dimension_ref_id.strip()
    ):
        return False
    if value.conversion_policy not in CONVERSION_POLICIES:
        return False
    if value.rounding_policy not in ROUNDING_POLICIES:
        return False
    if value.negative_value_policy not in QUANTITY_NEGATIVE_VALUE_POLICIES:
        return False
    if value.visibility_policy not in VISIBILITY_POLICIES:
        return False
    if not isinstance(value.provenance_refs, tuple):
        return False
    for ref in value.provenance_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True, kw_only=True)
class ResourceMathDependency:
    """Immutable external dependency reference inside a resource-math aggregate."""

    dependency_id: str
    dependency_type: str
    reference_id: str
    owner_domain: str
    required: bool = True
    satisfied: bool = False
    hidden_info_safe: bool = True
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dependency_id": self.dependency_id,
            "dependency_type": self.dependency_type,
            "reference_id": self.reference_id,
            "owner_domain": self.owner_domain,
            "required": self.required,
            "satisfied": self.satisfied,
            "hidden_info_safe": self.hidden_info_safe,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_resource_math_dependency(
    *,
    dependency_id: str,
    dependency_type: str,
    reference_id: str,
    owner_domain: str,
    required: bool = True,
    satisfied: bool = False,
    hidden_info_safe: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> ResourceMathDependency:
    """Create a validated ResourceMathDependency."""
    error_cls = InvalidResourceMathDependencyError

    _validate_non_empty_string(dependency_id, "dependency_id", error_cls)
    _validate_non_empty_string(dependency_type, "dependency_type", error_cls)
    if dependency_type not in RESOURCE_MATH_DEPENDENCY_TYPES:
        raise error_cls(
            f"dependency_type must be one of "
            f"{sorted(RESOURCE_MATH_DEPENDENCY_TYPES)}, got: {dependency_type!r}"
        )
    _validate_non_empty_string(reference_id, "reference_id", error_cls)
    _validate_non_empty_string(owner_domain, "owner_domain", error_cls)
    if owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        raise error_cls(
            f"owner_domain must be one of {sorted(RESOURCE_MATH_OWNER_DOMAINS)}, "
            f"got: {owner_domain!r}"
        )
    _validate_bool(required, "required", error_cls)
    _validate_bool(satisfied, "satisfied", error_cls)
    _validate_bool(hidden_info_safe, "hidden_info_safe", error_cls)

    safe_metadata = _safe_metadata(metadata, error_cls)

    return ResourceMathDependency(
        dependency_id=dependency_id,
        dependency_type=dependency_type,
        reference_id=reference_id,
        owner_domain=owner_domain,
        required=required,
        satisfied=satisfied,
        hidden_info_safe=hidden_info_safe,
        metadata=safe_metadata,
    )


def validate_resource_math_dependency(value: object) -> bool:
    if not isinstance(value, ResourceMathDependency):
        return False
    if not isinstance(value.dependency_id, str) or not value.dependency_id.strip():
        return False
    if value.dependency_type not in RESOURCE_MATH_DEPENDENCY_TYPES:
        return False
    if not isinstance(value.reference_id, str) or not value.reference_id.strip():
        return False
    if value.owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        return False
    if not isinstance(value.required, bool):
        return False
    if not isinstance(value.satisfied, bool):
        return False
    if not isinstance(value.hidden_info_safe, bool):
        return False
    if not isinstance(value.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True, kw_only=True)
class CostTerm:
    """Immutable cost term inside a resource-math request."""

    term_id: str
    subject_binding_id: str
    resource_ref_id: str | None = None
    quantity_id: str | None = None
    value_mode: str
    cost_family: str
    owner_domain: str
    policy_route: str | None = None
    timing_policy: str = "blocked_pending_validation"
    outcome_policy: str = "validation_blocked"
    visibility_policy: str = "public"
    dependency_ids: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "term_id": self.term_id,
            "subject_binding_id": self.subject_binding_id,
            "resource_ref_id": self.resource_ref_id,
            "quantity_id": self.quantity_id,
            "value_mode": self.value_mode,
            "cost_family": self.cost_family,
            "owner_domain": self.owner_domain,
            "policy_route": self.policy_route,
            "timing_policy": self.timing_policy,
            "outcome_policy": self.outcome_policy,
            "visibility_policy": self.visibility_policy,
            "dependency_ids": list(self.dependency_ids),
            "provenance_refs": list(self.provenance_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_cost_term(
    *,
    term_id: str,
    subject_binding_id: str,
    resource_ref_id: str | None = None,
    quantity_id: str | None = None,
    value_mode: str,
    cost_family: str,
    owner_domain: str,
    policy_route: str | None = None,
    timing_policy: str = "blocked_pending_validation",
    outcome_policy: str = "validation_blocked",
    visibility_policy: str = "public",
    dependency_ids: Sequence[str] | None = None,
    provenance_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CostTerm:
    """Create a validated CostTerm."""
    error_cls = InvalidCostTermError

    _validate_non_empty_string(term_id, "term_id", error_cls)
    _validate_non_empty_string(subject_binding_id, "subject_binding_id", error_cls)
    _validate_non_empty_string(value_mode, "value_mode", error_cls)
    if value_mode not in RESOURCE_TERM_VALUE_MODES:
        raise error_cls(
            f"value_mode must be one of {sorted(RESOURCE_TERM_VALUE_MODES)}, "
            f"got: {value_mode!r}"
        )
    _validate_optional_non_empty_string(resource_ref_id, "resource_ref_id", error_cls)
    _validate_optional_non_empty_string(quantity_id, "quantity_id", error_cls)
    _validate_optional_non_empty_string(policy_route, "policy_route", error_cls)
    _validate_term_value_mode_shape(
        value_mode, resource_ref_id, quantity_id, policy_route, error_cls
    )
    _validate_non_empty_string(cost_family, "cost_family", error_cls)
    if cost_family not in COST_FAMILIES:
        raise error_cls(
            f"cost_family must be one of {sorted(COST_FAMILIES)}, "
            f"got: {cost_family!r}"
        )
    _validate_non_empty_string(owner_domain, "owner_domain", error_cls)
    if owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        raise error_cls(
            f"owner_domain must be one of {sorted(RESOURCE_MATH_OWNER_DOMAINS)}, "
            f"got: {owner_domain!r}"
        )
    _validate_non_empty_string(timing_policy, "timing_policy", error_cls)
    if timing_policy not in COST_TIMING_POLICIES:
        raise error_cls(
            f"timing_policy must be one of {sorted(COST_TIMING_POLICIES)}, "
            f"got: {timing_policy!r}"
        )
    _validate_non_empty_string(outcome_policy, "outcome_policy", error_cls)
    if outcome_policy not in COST_OUTCOME_POLICIES:
        raise error_cls(
            f"outcome_policy must be one of {sorted(COST_OUTCOME_POLICIES)}, "
            f"got: {outcome_policy!r}"
        )
    _validate_non_empty_string(visibility_policy, "visibility_policy", error_cls)
    if visibility_policy not in VISIBILITY_POLICIES:
        raise error_cls(
            f"visibility_policy must be one of {sorted(VISIBILITY_POLICIES)}, "
            f"got: {visibility_policy!r}"
        )

    safe_dependency_ids = _normalize_string_tuple(
        dependency_ids, "dependency_ids", error_cls
    )
    safe_provenance_refs = _normalize_string_tuple(
        provenance_refs, "provenance_refs", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    return CostTerm(
        term_id=term_id,
        subject_binding_id=subject_binding_id,
        resource_ref_id=resource_ref_id,
        quantity_id=quantity_id,
        value_mode=value_mode,
        cost_family=cost_family,
        owner_domain=owner_domain,
        policy_route=policy_route,
        timing_policy=timing_policy,
        outcome_policy=outcome_policy,
        visibility_policy=visibility_policy,
        dependency_ids=safe_dependency_ids,
        provenance_refs=safe_provenance_refs,
        metadata=safe_metadata,
    )


def validate_cost_term(value: object) -> bool:
    if not isinstance(value, CostTerm):
        return False
    if not isinstance(value.term_id, str) or not value.term_id.strip():
        return False
    if not isinstance(value.subject_binding_id, str) or not value.subject_binding_id.strip():
        return False
    if value.value_mode not in RESOURCE_TERM_VALUE_MODES:
        return False
    if value.resource_ref_id is not None and (
        not isinstance(value.resource_ref_id, str) or not value.resource_ref_id.strip()
    ):
        return False
    if value.quantity_id is not None and (
        not isinstance(value.quantity_id, str) or not value.quantity_id.strip()
    ):
        return False
    if value.policy_route is not None and (
        not isinstance(value.policy_route, str) or not value.policy_route.strip()
    ):
        return False
    if value.value_mode == "policy_only" and (
        value.policy_route is None or value.policy_route not in RESOURCE_TERM_POLICY_ROUTES
    ):
        return False
    if value.value_mode != "policy_only" and value.policy_route is not None:
        return False
    if value.value_mode in ("resource_quantity", "resource_reference_only") and value.resource_ref_id is None:
        return False
    if value.value_mode in ("resource_reference_only", "quantity_only", "policy_only") and value.quantity_id is not None:
        return False
    if value.value_mode in ("resource_quantity", "quantity_only") and value.quantity_id is None:
        return False
    if value.value_mode in ("resource_quantity", "resource_reference_only", "quantity_only") and value.resource_ref_id is not None:
        pass
    if value.value_mode == "policy_only" and value.resource_ref_id is not None:
        return False
    if value.cost_family not in COST_FAMILIES:
        return False
    if value.owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        return False
    if value.timing_policy not in COST_TIMING_POLICIES:
        return False
    if value.outcome_policy not in COST_OUTCOME_POLICIES:
        return False
    if value.visibility_policy not in VISIBILITY_POLICIES:
        return False
    if not isinstance(value.dependency_ids, tuple):
        return False
    for dep_id in value.dependency_ids:
        if not isinstance(dep_id, str) or not dep_id.strip():
            return False
    if not isinstance(value.provenance_refs, tuple):
        return False
    for ref in value.provenance_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True, kw_only=True)
class ConsequenceTerm:
    """Immutable consequence term inside a resource-math request."""

    consequence_id: str
    subject_binding_id: str
    resource_ref_id: str | None = None
    quantity_id: str | None = None
    value_mode: str
    consequence_family: str
    owner_domain: str
    policy_route: str | None = None
    timing_policy: str = "blocked_pending_validation"
    outcome_policy: str = "validation_blocked"
    visibility_policy: str = "public"
    dependency_ids: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "consequence_id": self.consequence_id,
            "subject_binding_id": self.subject_binding_id,
            "resource_ref_id": self.resource_ref_id,
            "quantity_id": self.quantity_id,
            "value_mode": self.value_mode,
            "consequence_family": self.consequence_family,
            "owner_domain": self.owner_domain,
            "policy_route": self.policy_route,
            "timing_policy": self.timing_policy,
            "outcome_policy": self.outcome_policy,
            "visibility_policy": self.visibility_policy,
            "dependency_ids": list(self.dependency_ids),
            "provenance_refs": list(self.provenance_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_consequence_term(
    *,
    consequence_id: str,
    subject_binding_id: str,
    resource_ref_id: str | None = None,
    quantity_id: str | None = None,
    value_mode: str,
    consequence_family: str,
    owner_domain: str,
    policy_route: str | None = None,
    timing_policy: str = "blocked_pending_validation",
    outcome_policy: str = "validation_blocked",
    visibility_policy: str = "public",
    dependency_ids: Sequence[str] | None = None,
    provenance_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ConsequenceTerm:
    """Create a validated ConsequenceTerm."""
    error_cls = InvalidConsequenceTermError

    _validate_non_empty_string(consequence_id, "consequence_id", error_cls)
    _validate_non_empty_string(subject_binding_id, "subject_binding_id", error_cls)
    _validate_non_empty_string(value_mode, "value_mode", error_cls)
    if value_mode not in RESOURCE_TERM_VALUE_MODES:
        raise error_cls(
            f"value_mode must be one of {sorted(RESOURCE_TERM_VALUE_MODES)}, "
            f"got: {value_mode!r}"
        )
    _validate_optional_non_empty_string(resource_ref_id, "resource_ref_id", error_cls)
    _validate_optional_non_empty_string(quantity_id, "quantity_id", error_cls)
    _validate_optional_non_empty_string(policy_route, "policy_route", error_cls)
    _validate_term_value_mode_shape(
        value_mode, resource_ref_id, quantity_id, policy_route, error_cls
    )
    _validate_non_empty_string(consequence_family, "consequence_family", error_cls)
    if consequence_family not in CONSEQUENCE_FAMILIES:
        raise error_cls(
            f"consequence_family must be one of {sorted(CONSEQUENCE_FAMILIES)}, "
            f"got: {consequence_family!r}"
        )
    _validate_non_empty_string(owner_domain, "owner_domain", error_cls)
    if owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        raise error_cls(
            f"owner_domain must be one of {sorted(RESOURCE_MATH_OWNER_DOMAINS)}, "
            f"got: {owner_domain!r}"
        )
    _validate_non_empty_string(timing_policy, "timing_policy", error_cls)
    if timing_policy not in COST_TIMING_POLICIES:
        raise error_cls(
            f"timing_policy must be one of {sorted(COST_TIMING_POLICIES)}, "
            f"got: {timing_policy!r}"
        )
    _validate_non_empty_string(outcome_policy, "outcome_policy", error_cls)
    if outcome_policy not in COST_OUTCOME_POLICIES:
        raise error_cls(
            f"outcome_policy must be one of {sorted(COST_OUTCOME_POLICIES)}, "
            f"got: {outcome_policy!r}"
        )
    _validate_non_empty_string(visibility_policy, "visibility_policy", error_cls)
    if visibility_policy not in VISIBILITY_POLICIES:
        raise error_cls(
            f"visibility_policy must be one of {sorted(VISIBILITY_POLICIES)}, "
            f"got: {visibility_policy!r}"
        )

    safe_dependency_ids = _normalize_string_tuple(
        dependency_ids, "dependency_ids", error_cls
    )
    safe_provenance_refs = _normalize_string_tuple(
        provenance_refs, "provenance_refs", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    return ConsequenceTerm(
        consequence_id=consequence_id,
        subject_binding_id=subject_binding_id,
        resource_ref_id=resource_ref_id,
        quantity_id=quantity_id,
        value_mode=value_mode,
        consequence_family=consequence_family,
        owner_domain=owner_domain,
        policy_route=policy_route,
        timing_policy=timing_policy,
        outcome_policy=outcome_policy,
        visibility_policy=visibility_policy,
        dependency_ids=safe_dependency_ids,
        provenance_refs=safe_provenance_refs,
        metadata=safe_metadata,
    )


def validate_consequence_term(value: object) -> bool:
    if not isinstance(value, ConsequenceTerm):
        return False
    if not isinstance(value.consequence_id, str) or not value.consequence_id.strip():
        return False
    if not isinstance(value.subject_binding_id, str) or not value.subject_binding_id.strip():
        return False
    if value.value_mode not in RESOURCE_TERM_VALUE_MODES:
        return False
    if value.resource_ref_id is not None and (
        not isinstance(value.resource_ref_id, str) or not value.resource_ref_id.strip()
    ):
        return False
    if value.quantity_id is not None and (
        not isinstance(value.quantity_id, str) or not value.quantity_id.strip()
    ):
        return False
    if value.policy_route is not None and (
        not isinstance(value.policy_route, str) or not value.policy_route.strip()
    ):
        return False
    if value.value_mode == "policy_only" and (
        value.policy_route is None or value.policy_route not in RESOURCE_TERM_POLICY_ROUTES
    ):
        return False
    if value.value_mode != "policy_only" and value.policy_route is not None:
        return False
    if value.value_mode in ("resource_quantity", "resource_reference_only") and value.resource_ref_id is None:
        return False
    if value.value_mode in ("resource_reference_only", "quantity_only", "policy_only") and value.quantity_id is not None:
        return False
    if value.value_mode in ("resource_quantity", "quantity_only") and value.quantity_id is None:
        return False
    if value.value_mode == "policy_only" and value.resource_ref_id is not None:
        return False
    if value.consequence_family not in CONSEQUENCE_FAMILIES:
        return False
    if value.owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        return False
    if value.timing_policy not in COST_TIMING_POLICIES:
        return False
    if value.outcome_policy not in COST_OUTCOME_POLICIES:
        return False
    if value.visibility_policy not in VISIBILITY_POLICIES:
        return False
    if not isinstance(value.dependency_ids, tuple):
        return False
    for dep_id in value.dependency_ids:
        if not isinstance(dep_id, str) or not dep_id.strip():
            return False
    if not isinstance(value.provenance_refs, tuple):
        return False
    for ref in value.provenance_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True, kw_only=True)
class CostBundle:
    """Immutable cost bundle inside a resource-math request."""

    bundle_id: str
    term_ids: tuple[str, ...]
    atomicity_policy: str = "all_or_nothing_requested"
    ordering_policy: str = "unordered_terms"
    partial_settlement_policy: str = "no_partial_settlement"
    minimum_required_terms: int | None = None
    maximum_allowed_terms: int | None = None
    alternative_groups: tuple[tuple[str, tuple[str, ...]], ...] = ()
    visibility_policy: str = "public"
    owner_domain: str
    dependency_ids: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "term_ids": list(self.term_ids),
            "atomicity_policy": self.atomicity_policy,
            "ordering_policy": self.ordering_policy,
            "partial_settlement_policy": self.partial_settlement_policy,
            "minimum_required_terms": self.minimum_required_terms,
            "maximum_allowed_terms": self.maximum_allowed_terms,
            "alternative_groups": [
                [group_id, list(group_terms)]
                for group_id, group_terms in self.alternative_groups
            ],
            "visibility_policy": self.visibility_policy,
            "owner_domain": self.owner_domain,
            "dependency_ids": list(self.dependency_ids),
            "provenance_refs": list(self.provenance_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


def create_cost_bundle(
    *,
    bundle_id: str,
    term_ids: Sequence[str],
    atomicity_policy: str = "all_or_nothing_requested",
    ordering_policy: str = "unordered_terms",
    partial_settlement_policy: str = "no_partial_settlement",
    minimum_required_terms: int | None = None,
    maximum_allowed_terms: int | None = None,
    alternative_groups: Sequence[tuple[str, Sequence[str]]] | None = None,
    visibility_policy: str = "public",
    owner_domain: str,
    dependency_ids: Sequence[str] | None = None,
    provenance_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CostBundle:
    """Create a validated CostBundle."""
    error_cls = InvalidCostBundleError

    _validate_non_empty_string(bundle_id, "bundle_id", error_cls)

    if isinstance(term_ids, str):
        raise error_cls("term_ids must not be a bare string")
    if not isinstance(term_ids, Sequence):
        raise error_cls("term_ids must be a sequence")
    if len(term_ids) == 0:
        raise error_cls("term_ids must not be empty")
    safe_term_ids: list[str] = []
    seen_terms: set[str] = set()
    for i, term_id in enumerate(term_ids):
        if not isinstance(term_id, str) or not term_id.strip():
            raise error_cls(f"term_ids[{i}] must be a non-empty string")
        if term_id in seen_terms:
            raise error_cls(f"term_ids[{i}] is duplicated: {term_id!r}")
        seen_terms.add(term_id)
        safe_term_ids.append(term_id)
    safe_term_ids_tuple = tuple(safe_term_ids)

    _validate_non_empty_string(atomicity_policy, "atomicity_policy", error_cls)
    if atomicity_policy not in ATOMICITY_POLICIES:
        raise error_cls(
            f"atomicity_policy must be one of {sorted(ATOMICITY_POLICIES)}, "
            f"got: {atomicity_policy!r}"
        )
    _validate_non_empty_string(ordering_policy, "ordering_policy", error_cls)
    if ordering_policy not in ORDERING_POLICIES:
        raise error_cls(
            f"ordering_policy must be one of {sorted(ORDERING_POLICIES)}, "
            f"got: {ordering_policy!r}"
        )
    _validate_non_empty_string(
        partial_settlement_policy, "partial_settlement_policy", error_cls
    )
    if partial_settlement_policy not in PARTIAL_SETTLEMENT_POLICIES:
        raise error_cls(
            f"partial_settlement_policy must be one of "
            f"{sorted(PARTIAL_SETTLEMENT_POLICIES)}, "
            f"got: {partial_settlement_policy!r}"
        )

    _validate_optional_positive_non_bool_int(
        minimum_required_terms, "minimum_required_terms", error_cls
    )
    _validate_optional_positive_non_bool_int(
        maximum_allowed_terms, "maximum_allowed_terms", error_cls
    )
    if minimum_required_terms is not None and minimum_required_terms > len(safe_term_ids_tuple):
        raise error_cls(
            f"minimum_required_terms ({minimum_required_terms}) cannot exceed "
            f"len(term_ids) ({len(safe_term_ids_tuple)})"
        )
    if maximum_allowed_terms is not None and maximum_allowed_terms > len(safe_term_ids_tuple):
        raise error_cls(
            f"maximum_allowed_terms ({maximum_allowed_terms}) cannot exceed "
            f"len(term_ids) ({len(safe_term_ids_tuple)})"
        )
    if (
        minimum_required_terms is not None
        and maximum_allowed_terms is not None
        and minimum_required_terms > maximum_allowed_terms
    ):
        raise error_cls(
            f"minimum_required_terms ({minimum_required_terms}) cannot exceed "
            f"maximum_allowed_terms ({maximum_allowed_terms})"
        )

    safe_alternative_groups = _normalize_alternative_groups(
        alternative_groups, safe_term_ids_tuple, error_cls
    )

    _validate_non_empty_string(visibility_policy, "visibility_policy", error_cls)
    if visibility_policy not in VISIBILITY_POLICIES:
        raise error_cls(
            f"visibility_policy must be one of {sorted(VISIBILITY_POLICIES)}, "
            f"got: {visibility_policy!r}"
        )
    _validate_non_empty_string(owner_domain, "owner_domain", error_cls)
    if owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        raise error_cls(
            f"owner_domain must be one of {sorted(RESOURCE_MATH_OWNER_DOMAINS)}, "
            f"got: {owner_domain!r}"
        )

    safe_dependency_ids = _normalize_string_tuple(
        dependency_ids, "dependency_ids", error_cls
    )
    safe_provenance_refs = _normalize_string_tuple(
        provenance_refs, "provenance_refs", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    return CostBundle(
        bundle_id=bundle_id,
        term_ids=safe_term_ids_tuple,
        atomicity_policy=atomicity_policy,
        ordering_policy=ordering_policy,
        partial_settlement_policy=partial_settlement_policy,
        minimum_required_terms=minimum_required_terms,
        maximum_allowed_terms=maximum_allowed_terms,
        alternative_groups=safe_alternative_groups,
        visibility_policy=visibility_policy,
        owner_domain=owner_domain,
        dependency_ids=safe_dependency_ids,
        provenance_refs=safe_provenance_refs,
        metadata=safe_metadata,
    )


def validate_cost_bundle(value: object) -> bool:
    if not isinstance(value, CostBundle):
        return False
    if not isinstance(value.bundle_id, str) or not value.bundle_id.strip():
        return False
    if not isinstance(value.term_ids, tuple) or len(value.term_ids) == 0:
        return False
    seen_terms: set[str] = set()
    for term_id in value.term_ids:
        if not isinstance(term_id, str) or not term_id.strip():
            return False
        if term_id in seen_terms:
            return False
        seen_terms.add(term_id)
    if value.atomicity_policy not in ATOMICITY_POLICIES:
        return False
    if value.ordering_policy not in ORDERING_POLICIES:
        return False
    if value.partial_settlement_policy not in PARTIAL_SETTLEMENT_POLICIES:
        return False
    if value.minimum_required_terms is not None and (
        isinstance(value.minimum_required_terms, bool)
        or not isinstance(value.minimum_required_terms, int)
        or value.minimum_required_terms <= 0
        or value.minimum_required_terms > len(value.term_ids)
    ):
        return False
    if value.maximum_allowed_terms is not None and (
        isinstance(value.maximum_allowed_terms, bool)
        or not isinstance(value.maximum_allowed_terms, int)
        or value.maximum_allowed_terms <= 0
        or value.maximum_allowed_terms > len(value.term_ids)
    ):
        return False
    if (
        value.minimum_required_terms is not None
        and value.maximum_allowed_terms is not None
        and value.minimum_required_terms > value.maximum_allowed_terms
    ):
        return False
    if not isinstance(value.alternative_groups, tuple):
        return False
    seen_group_ids: set[str] = set()
    seen_group_terms: set[str] = set()
    for group_id, group_terms in value.alternative_groups:
        if not isinstance(group_id, str) or not group_id.strip():
            return False
        if group_id in seen_group_ids:
            return False
        seen_group_ids.add(group_id)
        if not isinstance(group_terms, tuple) or len(group_terms) == 0:
            return False
        group_seen: set[str] = set()
        for term_id in group_terms:
            if not isinstance(term_id, str) or not term_id.strip():
                return False
            if term_id in group_seen:
                return False
            if term_id not in seen_terms:
                return False
            if term_id in seen_group_terms:
                return False
            group_seen.add(term_id)
            seen_group_terms.add(term_id)
    if value.visibility_policy not in VISIBILITY_POLICIES:
        return False
    if value.owner_domain not in RESOURCE_MATH_OWNER_DOMAINS:
        return False
    if not isinstance(value.dependency_ids, tuple):
        return False
    for dep_id in value.dependency_ids:
        if not isinstance(dep_id, str) or not dep_id.strip():
            return False
    if not isinstance(value.provenance_refs, tuple):
        return False
    for ref in value.provenance_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.metadata, Mapping):
        return False
    return True


@dataclass(frozen=True, kw_only=True)
class ResourceMathRequest:
    """Immutable resource-math request aggregate.

    This is a reference-only planning declaration. It does not execute
    arithmetic, affordability, settlement, mutation, persistence, or any
    other runtime behavior.
    """

    request_id: str
    trace_ref_id: str
    subject_refs: tuple[ResourceMathSubjectReference, ...]
    command_ref_id: str | None = None
    action_legality_ref_id: str | None = None
    state_projection_ref_ids: tuple[str, ...] = ()
    resource_refs: tuple[ResourceReference, ...] = ()
    quantity_specs: tuple[QuantitySpecification, ...] = ()
    cost_terms: tuple[CostTerm, ...] = ()
    cost_bundles: tuple[CostBundle, ...] = ()
    consequence_terms: tuple[ConsequenceTerm, ...] = ()
    dependencies: tuple[ResourceMathDependency, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    owner_handoff_ref_ids: tuple[str, ...] = ()
    validation_request_ref_id: str | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    calculation_executed: bool = False
    affordability_executed: bool = False
    reservation_authorized: bool = False
    settlement_authorized: bool = False
    consequence_application_authorized: bool = False
    mutation_authorized: bool = False
    state_delta_application_authorized: bool = False
    transaction_execution_authorized: bool = False
    event_commitment_authorized: bool = False
    event_append_authorized: bool = False
    persistence_authorized: bool = False
    replay_authorized: bool = False
    rng_execution_authorized: bool = False
    table_oracle_execution_authorized: bool = False
    model_authority_authorized: bool = False
    live_play_authorized: bool = False
    ui_authorized: bool = False
    conversion_authorized: bool = False
    canon_promotion_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "request_id": self.request_id,
            "trace_ref_id": self.trace_ref_id,
            "subject_refs": [s.to_dict() for s in self.subject_refs],
            "command_ref_id": self.command_ref_id,
            "action_legality_ref_id": self.action_legality_ref_id,
            "state_projection_ref_ids": list(self.state_projection_ref_ids),
            "resource_refs": [r.to_dict() for r in self.resource_refs],
            "quantity_specs": [q.to_dict() for q in self.quantity_specs],
            "cost_terms": [t.to_dict() for t in self.cost_terms],
            "cost_bundles": [b.to_dict() for b in self.cost_bundles],
            "consequence_terms": [t.to_dict() for t in self.consequence_terms],
            "dependencies": [d.to_dict() for d in self.dependencies],
            "provenance_refs": list(self.provenance_refs),
            "owner_handoff_ref_ids": list(self.owner_handoff_ref_ids),
            "validation_request_ref_id": self.validation_request_ref_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }
        for field_name in _RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS:
            result[field_name] = getattr(self, field_name)
        return result


def create_resource_math_request(
    *,
    request_id: str,
    trace_ref_id: str,
    subject_refs: Sequence[ResourceMathSubjectReference] | None = None,
    command_ref_id: str | None = None,
    action_legality_ref_id: str | None = None,
    state_projection_ref_ids: Sequence[str] | None = None,
    resource_refs: Sequence[ResourceReference] | None = None,
    quantity_specs: Sequence[QuantitySpecification] | None = None,
    cost_terms: Sequence[CostTerm] | None = None,
    cost_bundles: Sequence[CostBundle] | None = None,
    consequence_terms: Sequence[ConsequenceTerm] | None = None,
    dependencies: Sequence[ResourceMathDependency] | None = None,
    provenance_refs: Sequence[str] | None = None,
    owner_handoff_ref_ids: Sequence[str] | None = None,
    validation_request_ref_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
    calculation_executed: bool = False,
    affordability_executed: bool = False,
    reservation_authorized: bool = False,
    settlement_authorized: bool = False,
    consequence_application_authorized: bool = False,
    mutation_authorized: bool = False,
    state_delta_application_authorized: bool = False,
    transaction_execution_authorized: bool = False,
    event_commitment_authorized: bool = False,
    event_append_authorized: bool = False,
    persistence_authorized: bool = False,
    replay_authorized: bool = False,
    rng_execution_authorized: bool = False,
    table_oracle_execution_authorized: bool = False,
    model_authority_authorized: bool = False,
    live_play_authorized: bool = False,
    ui_authorized: bool = False,
    conversion_authorized: bool = False,
    canon_promotion_authorized: bool = False,
) -> ResourceMathRequest:
    """Create a validated ResourceMathRequest aggregate."""
    error_cls = InvalidResourceMathRequestError

    _validate_non_empty_string(request_id, "request_id", error_cls)
    _validate_non_empty_string(trace_ref_id, "trace_ref_id", error_cls)
    _validate_optional_non_empty_string(command_ref_id, "command_ref_id", error_cls)
    _validate_optional_non_empty_string(
        action_legality_ref_id, "action_legality_ref_id", error_cls
    )
    _validate_optional_non_empty_string(
        validation_request_ref_id, "validation_request_ref_id", error_cls
    )

    authority_kwargs = {
        "calculation_executed": calculation_executed,
        "affordability_executed": affordability_executed,
        "reservation_authorized": reservation_authorized,
        "settlement_authorized": settlement_authorized,
        "consequence_application_authorized": consequence_application_authorized,
        "mutation_authorized": mutation_authorized,
        "state_delta_application_authorized": state_delta_application_authorized,
        "transaction_execution_authorized": transaction_execution_authorized,
        "event_commitment_authorized": event_commitment_authorized,
        "event_append_authorized": event_append_authorized,
        "persistence_authorized": persistence_authorized,
        "replay_authorized": replay_authorized,
        "rng_execution_authorized": rng_execution_authorized,
        "table_oracle_execution_authorized": table_oracle_execution_authorized,
        "model_authority_authorized": model_authority_authorized,
        "live_play_authorized": live_play_authorized,
        "ui_authorized": ui_authorized,
        "conversion_authorized": conversion_authorized,
        "canon_promotion_authorized": canon_promotion_authorized,
    }
    _validate_false_only_authority_fields(authority_kwargs, error_cls)

    safe_subject_refs = _normalize_dataclass_tuple(
        subject_refs, "subject_refs", ResourceMathSubjectReference, error_cls
    )
    if len(safe_subject_refs) == 0:
        raise error_cls("subject_refs must not be empty")
    _validate_unique_attr(
        safe_subject_refs, "subject_binding_id", "subject_refs", error_cls
    )
    _validate_exactly_one_primary_subject(safe_subject_refs, error_cls)

    safe_resource_refs = _normalize_dataclass_tuple(
        resource_refs, "resource_refs", ResourceReference, error_cls
    )
    resource_ref_ids = _validate_unique_attr(
        safe_resource_refs, "resource_ref_id", "resource_refs", error_cls
    )

    safe_quantity_specs = _normalize_dataclass_tuple(
        quantity_specs, "quantity_specs", QuantitySpecification, error_cls
    )
    quantity_ids = _validate_unique_attr(
        safe_quantity_specs, "quantity_id", "quantity_specs", error_cls
    )

    safe_cost_terms = _normalize_dataclass_tuple(
        cost_terms, "cost_terms", CostTerm, error_cls
    )
    cost_term_ids = _validate_unique_attr(
        safe_cost_terms, "term_id", "cost_terms", error_cls
    )

    safe_cost_bundles = _normalize_dataclass_tuple(
        cost_bundles, "cost_bundles", CostBundle, error_cls
    )
    cost_bundle_ids = _validate_unique_attr(
        safe_cost_bundles, "bundle_id", "cost_bundles", error_cls
    )

    safe_consequence_terms = _normalize_dataclass_tuple(
        consequence_terms, "consequence_terms", ConsequenceTerm, error_cls
    )
    consequence_ids = _validate_unique_attr(
        safe_consequence_terms, "consequence_id", "consequence_terms", error_cls
    )

    safe_dependencies = _normalize_dataclass_tuple(
        dependencies, "dependencies", ResourceMathDependency, error_cls
    )
    dependency_ids = _validate_unique_attr(
        safe_dependencies, "dependency_id", "dependencies", error_cls
    )
    seen_dependency_pairs: set[tuple[str, str]] = set()
    for dep in safe_dependencies:
        pair = (dep.dependency_type, dep.reference_id)
        if pair in seen_dependency_pairs:
            raise error_cls(
                f"dependencies has duplicate (dependency_type, reference_id): {pair!r}"
            )
        seen_dependency_pairs.add(pair)

    subject_binding_ids = {s.subject_binding_id for s in safe_subject_refs}

    for ref in safe_resource_refs:
        _validate_same_request_reference(
            ref.subject_binding_id,
            "resource_ref.subject_binding_id",
            subject_binding_ids,
            error_cls,
        )

    for term in safe_cost_terms:
        _validate_same_request_reference(
            term.subject_binding_id,
            "cost_term.subject_binding_id",
            subject_binding_ids,
            error_cls,
        )
        _validate_same_request_reference(
            term.resource_ref_id,
            "cost_term.resource_ref_id",
            resource_ref_ids,
            error_cls,
        )
        _validate_same_request_reference(
            term.quantity_id,
            "cost_term.quantity_id",
            quantity_ids,
            error_cls,
        )
        for dep_id in term.dependency_ids:
            _validate_same_request_reference(
                dep_id,
                "cost_term.dependency_ids",
                dependency_ids,
                error_cls,
            )

    for bundle in safe_cost_bundles:
        for term_id in bundle.term_ids:
            _validate_same_request_reference(
                term_id,
                "cost_bundle.term_ids",
                cost_term_ids,
                error_cls,
            )
        for dep_id in bundle.dependency_ids:
            _validate_same_request_reference(
                dep_id,
                "cost_bundle.dependency_ids",
                dependency_ids,
                error_cls,
            )

    for term in safe_consequence_terms:
        _validate_same_request_reference(
            term.subject_binding_id,
            "consequence_term.subject_binding_id",
            subject_binding_ids,
            error_cls,
        )
        _validate_same_request_reference(
            term.resource_ref_id,
            "consequence_term.resource_ref_id",
            resource_ref_ids,
            error_cls,
        )
        _validate_same_request_reference(
            term.quantity_id,
            "consequence_term.quantity_id",
            quantity_ids,
            error_cls,
        )
        for dep_id in term.dependency_ids:
            _validate_same_request_reference(
                dep_id,
                "consequence_term.dependency_ids",
                dependency_ids,
                error_cls,
            )

    safe_state_projection_ref_ids = _normalize_string_tuple(
        state_projection_ref_ids, "state_projection_ref_ids", error_cls
    )
    safe_provenance_refs = _normalize_string_tuple(
        provenance_refs, "provenance_refs", error_cls
    )
    safe_owner_handoff_ref_ids = _normalize_string_tuple(
        owner_handoff_ref_ids, "owner_handoff_ref_ids", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    return ResourceMathRequest(
        request_id=request_id,
        trace_ref_id=trace_ref_id,
        subject_refs=safe_subject_refs,
        command_ref_id=command_ref_id,
        action_legality_ref_id=action_legality_ref_id,
        state_projection_ref_ids=safe_state_projection_ref_ids,
        resource_refs=safe_resource_refs,
        quantity_specs=safe_quantity_specs,
        cost_terms=safe_cost_terms,
        cost_bundles=safe_cost_bundles,
        consequence_terms=safe_consequence_terms,
        dependencies=safe_dependencies,
        provenance_refs=safe_provenance_refs,
        owner_handoff_ref_ids=safe_owner_handoff_ref_ids,
        validation_request_ref_id=validation_request_ref_id,
        metadata=safe_metadata,
        **authority_kwargs,
    )


def validate_resource_math_request(value: object) -> bool:
    if not isinstance(value, ResourceMathRequest):
        return False
    if not isinstance(value.request_id, str) or not value.request_id.strip():
        return False
    if not isinstance(value.trace_ref_id, str) or not value.trace_ref_id.strip():
        return False
    if value.command_ref_id is not None and (
        not isinstance(value.command_ref_id, str) or not value.command_ref_id.strip()
    ):
        return False
    if value.action_legality_ref_id is not None and (
        not isinstance(value.action_legality_ref_id, str)
        or not value.action_legality_ref_id.strip()
    ):
        return False
    if value.validation_request_ref_id is not None and (
        not isinstance(value.validation_request_ref_id, str)
        or not value.validation_request_ref_id.strip()
    ):
        return False

    for field_name in _RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS:
        if getattr(value, field_name) is not False:
            return False

    if not isinstance(value.subject_refs, tuple) or len(value.subject_refs) == 0:
        return False
    subject_binding_ids: set[str] = set()
    primary_count = 0
    for subject in value.subject_refs:
        if not validate_resource_math_subject_reference(subject):
            return False
        if subject.subject_binding_id in subject_binding_ids:
            return False
        subject_binding_ids.add(subject.subject_binding_id)
        if subject.subject_role == "primary_subject":
            primary_count += 1
    if primary_count != 1:
        return False

    if not isinstance(value.resource_refs, tuple):
        return False
    resource_ref_ids: set[str] = set()
    for ref in value.resource_refs:
        if not validate_resource_reference(ref):
            return False
        if ref.resource_ref_id in resource_ref_ids:
            return False
        resource_ref_ids.add(ref.resource_ref_id)
        if ref.subject_binding_id not in subject_binding_ids:
            return False

    if not isinstance(value.quantity_specs, tuple):
        return False
    quantity_ids: set[str] = set()
    for qty in value.quantity_specs:
        if not validate_quantity_specification(qty):
            return False
        if qty.quantity_id in quantity_ids:
            return False
        quantity_ids.add(qty.quantity_id)

    if not isinstance(value.cost_terms, tuple):
        return False
    cost_term_ids: set[str] = set()
    for term in value.cost_terms:
        if not validate_cost_term(term):
            return False
        if term.term_id in cost_term_ids:
            return False
        cost_term_ids.add(term.term_id)
        if term.subject_binding_id not in subject_binding_ids:
            return False
        if term.resource_ref_id is not None and term.resource_ref_id not in resource_ref_ids:
            return False
        if term.quantity_id is not None and term.quantity_id not in quantity_ids:
            return False

    if not isinstance(value.cost_bundles, tuple):
        return False
    cost_bundle_ids: set[str] = set()
    for bundle in value.cost_bundles:
        if not validate_cost_bundle(bundle):
            return False
        if bundle.bundle_id in cost_bundle_ids:
            return False
        cost_bundle_ids.add(bundle.bundle_id)
        for term_id in bundle.term_ids:
            if term_id not in cost_term_ids:
                return False

    if not isinstance(value.consequence_terms, tuple):
        return False
    consequence_ids: set[str] = set()
    for term in value.consequence_terms:
        if not validate_consequence_term(term):
            return False
        if term.consequence_id in consequence_ids:
            return False
        consequence_ids.add(term.consequence_id)
        if term.subject_binding_id not in subject_binding_ids:
            return False
        if term.resource_ref_id is not None and term.resource_ref_id not in resource_ref_ids:
            return False
        if term.quantity_id is not None and term.quantity_id not in quantity_ids:
            return False

    if not isinstance(value.dependencies, tuple):
        return False
    dependency_ids: set[str] = set()
    dependency_pairs: set[tuple[str, str]] = set()
    for dep in value.dependencies:
        if not validate_resource_math_dependency(dep):
            return False
        if dep.dependency_id in dependency_ids:
            return False
        dependency_ids.add(dep.dependency_id)
        pair = (dep.dependency_type, dep.reference_id)
        if pair in dependency_pairs:
            return False
        dependency_pairs.add(pair)

    for term in value.cost_terms:
        for dep_id in term.dependency_ids:
            if dep_id not in dependency_ids:
                return False
    for bundle in value.cost_bundles:
        for dep_id in bundle.dependency_ids:
            if dep_id not in dependency_ids:
                return False
    for term in value.consequence_terms:
        for dep_id in term.dependency_ids:
            if dep_id not in dependency_ids:
                return False

    if not isinstance(value.state_projection_ref_ids, tuple):
        return False
    for ref in value.state_projection_ref_ids:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.provenance_refs, tuple):
        return False
    for ref in value.provenance_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
    if not isinstance(value.owner_handoff_ref_ids, tuple):
        return False
    for ref in value.owner_handoff_ref_ids:
        if not isinstance(ref, str) or not ref.strip():
            return False

    if not isinstance(value.metadata, Mapping):
        return False

    return True


@dataclass(frozen=True, kw_only=True)
class ResourceMathResult:
    """Immutable resource-math result aggregate.

    This is a reference-only planning result. It does not execute
    arithmetic, affordability, settlement, mutation, persistence, or any
    other runtime behavior. A result never carries a self-binding to its
    own result_id.
    """

    result_id: str
    request_id: str
    stage: str
    decision: str
    blocking: bool
    trace_ref_id: str
    quarantined: bool = False
    escalated: bool = False
    diagnostics: tuple[str, ...] = ()
    normalized_reference_ids: tuple[str, ...] = ()
    referenced_subject_binding_ids: tuple[str, ...] = ()
    referenced_resource_ref_ids: tuple[str, ...] = ()
    referenced_quantity_ids: tuple[str, ...] = ()
    referenced_cost_term_ids: tuple[str, ...] = ()
    referenced_cost_bundle_ids: tuple[str, ...] = ()
    referenced_consequence_term_ids: tuple[str, ...] = ()
    referenced_dependency_ids: tuple[str, ...] = ()
    dependencies: tuple[ResourceMathDependency, ...] = ()
    validation_request_ref_id: str | None = None
    validation_result_ref_id: str | None = None
    validation_decision: str | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    calculation_executed: bool = False
    affordability_executed: bool = False
    reservation_authorized: bool = False
    settlement_authorized: bool = False
    consequence_application_authorized: bool = False
    mutation_authorized: bool = False
    state_delta_application_authorized: bool = False
    transaction_execution_authorized: bool = False
    event_commitment_authorized: bool = False
    event_append_authorized: bool = False
    persistence_authorized: bool = False
    replay_authorized: bool = False
    rng_execution_authorized: bool = False
    table_oracle_execution_authorized: bool = False
    model_authority_authorized: bool = False
    live_play_authorized: bool = False
    ui_authorized: bool = False
    conversion_authorized: bool = False
    canon_promotion_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "stage": self.stage,
            "decision": self.decision,
            "blocking": self.blocking,
            "trace_ref_id": self.trace_ref_id,
            "quarantined": self.quarantined,
            "escalated": self.escalated,
            "diagnostics": list(self.diagnostics),
            "normalized_reference_ids": list(self.normalized_reference_ids),
            "referenced_subject_binding_ids": list(self.referenced_subject_binding_ids),
            "referenced_resource_ref_ids": list(self.referenced_resource_ref_ids),
            "referenced_quantity_ids": list(self.referenced_quantity_ids),
            "referenced_cost_term_ids": list(self.referenced_cost_term_ids),
            "referenced_cost_bundle_ids": list(self.referenced_cost_bundle_ids),
            "referenced_consequence_term_ids": list(self.referenced_consequence_term_ids),
            "referenced_dependency_ids": list(self.referenced_dependency_ids),
            "dependencies": [d.to_dict() for d in self.dependencies],
            "validation_request_ref_id": self.validation_request_ref_id,
            "validation_result_ref_id": self.validation_result_ref_id,
            "validation_decision": self.validation_decision,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }
        for field_name in _RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS:
            result[field_name] = getattr(self, field_name)
        return result


def create_resource_math_result(
    *,
    result_id: str,
    request_id: str,
    stage: str,
    decision: str,
    blocking: bool,
    trace_ref_id: str,
    quarantined: bool = False,
    escalated: bool = False,
    diagnostics: Sequence[str] | None = None,
    normalized_reference_ids: Sequence[str] | None = None,
    referenced_subject_binding_ids: Sequence[str] | None = None,
    referenced_resource_ref_ids: Sequence[str] | None = None,
    referenced_quantity_ids: Sequence[str] | None = None,
    referenced_cost_term_ids: Sequence[str] | None = None,
    referenced_cost_bundle_ids: Sequence[str] | None = None,
    referenced_consequence_term_ids: Sequence[str] | None = None,
    referenced_dependency_ids: Sequence[str] | None = None,
    dependencies: Sequence[ResourceMathDependency] | None = None,
    validation_request_ref_id: str | None = None,
    validation_result_ref_id: str | None = None,
    validation_decision: str | None = None,
    metadata: Mapping[str, Any] | None = None,
    request: ResourceMathRequest | None = None,
    calculation_executed: bool = False,
    affordability_executed: bool = False,
    reservation_authorized: bool = False,
    settlement_authorized: bool = False,
    consequence_application_authorized: bool = False,
    mutation_authorized: bool = False,
    state_delta_application_authorized: bool = False,
    transaction_execution_authorized: bool = False,
    event_commitment_authorized: bool = False,
    event_append_authorized: bool = False,
    persistence_authorized: bool = False,
    replay_authorized: bool = False,
    rng_execution_authorized: bool = False,
    table_oracle_execution_authorized: bool = False,
    model_authority_authorized: bool = False,
    live_play_authorized: bool = False,
    ui_authorized: bool = False,
    conversion_authorized: bool = False,
    canon_promotion_authorized: bool = False,
) -> ResourceMathResult:
    """Create a validated ResourceMathResult aggregate."""
    error_cls = InvalidResourceMathResultError

    _validate_non_empty_string(result_id, "result_id", error_cls)
    _validate_non_empty_string(request_id, "request_id", error_cls)
    _validate_non_empty_string(trace_ref_id, "trace_ref_id", error_cls)
    _validate_non_empty_string(stage, "stage", error_cls)
    if stage not in RESOURCE_MATH_STAGES:
        raise error_cls(
            f"stage must be one of {sorted(RESOURCE_MATH_STAGES)}, got: {stage!r}"
        )
    _validate_non_empty_string(decision, "decision", error_cls)
    if decision not in RESOURCE_MATH_DECISIONS:
        raise error_cls(
            f"decision must be one of {sorted(RESOURCE_MATH_DECISIONS)}, got: {decision!r}"
        )
    _validate_bool(blocking, "blocking", error_cls)
    _validate_bool(quarantined, "quarantined", error_cls)
    _validate_bool(escalated, "escalated", error_cls)
    _validate_stage_decision_compatibility(
        stage, decision, blocking, quarantined, escalated, error_cls
    )

    authority_kwargs = {
        "calculation_executed": calculation_executed,
        "affordability_executed": affordability_executed,
        "reservation_authorized": reservation_authorized,
        "settlement_authorized": settlement_authorized,
        "consequence_application_authorized": consequence_application_authorized,
        "mutation_authorized": mutation_authorized,
        "state_delta_application_authorized": state_delta_application_authorized,
        "transaction_execution_authorized": transaction_execution_authorized,
        "event_commitment_authorized": event_commitment_authorized,
        "event_append_authorized": event_append_authorized,
        "persistence_authorized": persistence_authorized,
        "replay_authorized": replay_authorized,
        "rng_execution_authorized": rng_execution_authorized,
        "table_oracle_execution_authorized": table_oracle_execution_authorized,
        "model_authority_authorized": model_authority_authorized,
        "live_play_authorized": live_play_authorized,
        "ui_authorized": ui_authorized,
        "conversion_authorized": conversion_authorized,
        "canon_promotion_authorized": canon_promotion_authorized,
    }
    _validate_false_only_authority_fields(authority_kwargs, error_cls)

    safe_diagnostics = _normalize_string_tuple(
        diagnostics, "diagnostics", error_cls
    )
    safe_normalized_reference_ids = _normalize_string_tuple(
        normalized_reference_ids, "normalized_reference_ids", error_cls
    )
    safe_referenced_subject_binding_ids = _normalize_unique_string_tuple(
        referenced_subject_binding_ids, "referenced_subject_binding_ids", error_cls
    )
    safe_referenced_resource_ref_ids = _normalize_unique_string_tuple(
        referenced_resource_ref_ids, "referenced_resource_ref_ids", error_cls
    )
    safe_referenced_quantity_ids = _normalize_unique_string_tuple(
        referenced_quantity_ids, "referenced_quantity_ids", error_cls
    )
    safe_referenced_cost_term_ids = _normalize_unique_string_tuple(
        referenced_cost_term_ids, "referenced_cost_term_ids", error_cls
    )
    safe_referenced_cost_bundle_ids = _normalize_unique_string_tuple(
        referenced_cost_bundle_ids, "referenced_cost_bundle_ids", error_cls
    )
    safe_referenced_consequence_term_ids = _normalize_unique_string_tuple(
        referenced_consequence_term_ids, "referenced_consequence_term_ids", error_cls
    )
    safe_referenced_dependency_ids = _normalize_unique_string_tuple(
        referenced_dependency_ids, "referenced_dependency_ids", error_cls
    )

    safe_dependencies = _normalize_dataclass_tuple(
        dependencies, "dependencies", ResourceMathDependency, error_cls
    )
    dependency_ids = _validate_unique_attr(
        safe_dependencies, "dependency_id", "dependencies", error_cls
    )
    seen_dependency_pairs: set[tuple[str, str]] = set()
    for dep in safe_dependencies:
        pair = (dep.dependency_type, dep.reference_id)
        if pair in seen_dependency_pairs:
            raise error_cls(
                f"dependencies has duplicate (dependency_type, reference_id): {pair!r}"
            )
        seen_dependency_pairs.add(pair)

    _validate_optional_non_empty_string(
        validation_request_ref_id, "validation_request_ref_id", error_cls
    )
    _validate_optional_non_empty_string(
        validation_result_ref_id, "validation_result_ref_id", error_cls
    )
    if validation_decision is not None:
        _validate_non_empty_string(
            validation_decision, "validation_decision", error_cls
        )
        if validation_decision not in VALIDATION_INTEGRATION_DECISIONS:
            raise error_cls(
                f"validation_decision must be one of "
                f"{sorted(VALIDATION_INTEGRATION_DECISIONS)}, "
                f"got: {validation_decision!r}"
            )

    safe_metadata = _safe_metadata(metadata, error_cls)

    if request is not None:
        if request_id != request.request_id:
            raise error_cls(
                f"request_id {request_id!r} does not match supplied request "
                f"request_id {request.request_id!r}"
            )
        subject_binding_ids = {s.subject_binding_id for s in request.subject_refs}
        resource_ref_ids = {r.resource_ref_id for r in request.resource_refs}
        quantity_ids = {q.quantity_id for q in request.quantity_specs}
        cost_term_ids = {t.term_id for t in request.cost_terms}
        cost_bundle_ids = {b.bundle_id for b in request.cost_bundles}
        consequence_ids = {c.consequence_id for c in request.consequence_terms}
        request_dependency_ids = {d.dependency_id for d in request.dependencies}

        for ref_id in safe_referenced_subject_binding_ids:
            _validate_same_request_reference(
                ref_id,
                "referenced_subject_binding_ids",
                subject_binding_ids,
                error_cls,
            )
        for ref_id in safe_referenced_resource_ref_ids:
            _validate_same_request_reference(
                ref_id,
                "referenced_resource_ref_ids",
                resource_ref_ids,
                error_cls,
            )
        for ref_id in safe_referenced_quantity_ids:
            _validate_same_request_reference(
                ref_id,
                "referenced_quantity_ids",
                quantity_ids,
                error_cls,
            )
        for ref_id in safe_referenced_cost_term_ids:
            _validate_same_request_reference(
                ref_id,
                "referenced_cost_term_ids",
                cost_term_ids,
                error_cls,
            )
        for ref_id in safe_referenced_cost_bundle_ids:
            _validate_same_request_reference(
                ref_id,
                "referenced_cost_bundle_ids",
                cost_bundle_ids,
                error_cls,
            )
        for ref_id in safe_referenced_consequence_term_ids:
            _validate_same_request_reference(
                ref_id,
                "referenced_consequence_term_ids",
                consequence_ids,
                error_cls,
            )
        for ref_id in safe_referenced_dependency_ids:
            _validate_same_request_reference(
                ref_id,
                "referenced_dependency_ids",
                request_dependency_ids,
                error_cls,
            )

    return ResourceMathResult(
        result_id=result_id,
        request_id=request_id,
        stage=stage,
        decision=decision,
        blocking=blocking,
        trace_ref_id=trace_ref_id,
        quarantined=quarantined,
        escalated=escalated,
        diagnostics=safe_diagnostics,
        normalized_reference_ids=safe_normalized_reference_ids,
        referenced_subject_binding_ids=safe_referenced_subject_binding_ids,
        referenced_resource_ref_ids=safe_referenced_resource_ref_ids,
        referenced_quantity_ids=safe_referenced_quantity_ids,
        referenced_cost_term_ids=safe_referenced_cost_term_ids,
        referenced_cost_bundle_ids=safe_referenced_cost_bundle_ids,
        referenced_consequence_term_ids=safe_referenced_consequence_term_ids,
        referenced_dependency_ids=safe_referenced_dependency_ids,
        dependencies=safe_dependencies,
        validation_request_ref_id=validation_request_ref_id,
        validation_result_ref_id=validation_result_ref_id,
        validation_decision=validation_decision,
        metadata=safe_metadata,
        **authority_kwargs,
    )


def validate_resource_math_result(
    value: object,
    *,
    request: ResourceMathRequest | None = None,
) -> bool:
    if not isinstance(value, ResourceMathResult):
        return False
    if not isinstance(value.result_id, str) or not value.result_id.strip():
        return False
    if not isinstance(value.request_id, str) or not value.request_id.strip():
        return False
    if value.stage not in RESOURCE_MATH_STAGES:
        return False
    if value.decision not in RESOURCE_MATH_DECISIONS:
        return False
    if not isinstance(value.blocking, bool):
        return False
    if not isinstance(value.quarantined, bool):
        return False
    if not isinstance(value.escalated, bool):
        return False

    allowed_stages = _STAGE_DECISION_MATRIX.get(value.decision)
    if allowed_stages is None or value.stage not in allowed_stages:
        return False
    expected_blocking = value.decision not in _NON_BLOCKING_DECISIONS
    if value.blocking is not expected_blocking:
        return False
    is_quarantine_pair = (
        value.stage == "quarantined_for_review"
        and value.decision == "quarantined_for_review"
    )
    is_escalation_pair = (
        value.stage == "escalated_to_doctrine"
        and value.decision == "escalated_to_doctrine"
    )
    if value.quarantined and not is_quarantine_pair:
        return False
    if not value.quarantined and is_quarantine_pair:
        return False
    if value.escalated and not is_escalation_pair:
        return False
    if not value.escalated and is_escalation_pair:
        return False

    for field_name in _RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS:
        if getattr(value, field_name) is not False:
            return False

    if not isinstance(value.trace_ref_id, str) or not value.trace_ref_id.strip():
        return False

    if not isinstance(value.diagnostics, tuple):
        return False
    for item in value.diagnostics:
        if not isinstance(item, str) or not item.strip():
            return False
    if not isinstance(value.normalized_reference_ids, tuple):
        return False
    for item in value.normalized_reference_ids:
        if not isinstance(item, str) or not item.strip():
            return False

    referenced_tuples = [
        ("referenced_subject_binding_ids", value.referenced_subject_binding_ids),
        ("referenced_resource_ref_ids", value.referenced_resource_ref_ids),
        ("referenced_quantity_ids", value.referenced_quantity_ids),
        ("referenced_cost_term_ids", value.referenced_cost_term_ids),
        ("referenced_cost_bundle_ids", value.referenced_cost_bundle_ids),
        ("referenced_consequence_term_ids", value.referenced_consequence_term_ids),
        ("referenced_dependency_ids", value.referenced_dependency_ids),
    ]
    for name, tup in referenced_tuples:
        if not isinstance(tup, tuple):
            return False
        seen: set[str] = set()
        for item in tup:
            if not isinstance(item, str) or not item.strip():
                return False
            if item in seen:
                return False
            seen.add(item)

    if not isinstance(value.dependencies, tuple):
        return False
    dependency_ids: set[str] = set()
    dependency_pairs: set[tuple[str, str]] = set()
    for dep in value.dependencies:
        if not validate_resource_math_dependency(dep):
            return False
        if dep.dependency_id in dependency_ids:
            return False
        dependency_ids.add(dep.dependency_id)
        pair = (dep.dependency_type, dep.reference_id)
        if pair in dependency_pairs:
            return False
        dependency_pairs.add(pair)

    if value.validation_request_ref_id is not None and (
        not isinstance(value.validation_request_ref_id, str)
        or not value.validation_request_ref_id.strip()
    ):
        return False
    if value.validation_result_ref_id is not None and (
        not isinstance(value.validation_result_ref_id, str)
        or not value.validation_result_ref_id.strip()
    ):
        return False
    if value.validation_decision is not None:
        if (
            not isinstance(value.validation_decision, str)
            or not value.validation_decision.strip()
        ):
            return False
        if value.validation_decision not in VALIDATION_INTEGRATION_DECISIONS:
            return False

    if request is not None:
        if value.request_id != request.request_id:
            return False
        subject_binding_ids = {s.subject_binding_id for s in request.subject_refs}
        resource_ref_ids = {r.resource_ref_id for r in request.resource_refs}
        quantity_ids = {q.quantity_id for q in request.quantity_specs}
        cost_term_ids = {t.term_id for t in request.cost_terms}
        cost_bundle_ids = {b.bundle_id for b in request.cost_bundles}
        consequence_ids = {c.consequence_id for c in request.consequence_terms}
        request_dependency_ids = {d.dependency_id for d in request.dependencies}

        for ref_id in value.referenced_subject_binding_ids:
            if ref_id not in subject_binding_ids:
                return False
        for ref_id in value.referenced_resource_ref_ids:
            if ref_id not in resource_ref_ids:
                return False
        for ref_id in value.referenced_quantity_ids:
            if ref_id not in quantity_ids:
                return False
        for ref_id in value.referenced_cost_term_ids:
            if ref_id not in cost_term_ids:
                return False
        for ref_id in value.referenced_cost_bundle_ids:
            if ref_id not in cost_bundle_ids:
                return False
        for ref_id in value.referenced_consequence_term_ids:
            if ref_id not in consequence_ids:
                return False
        for ref_id in value.referenced_dependency_ids:
            if ref_id not in request_dependency_ids:
                return False

    if not isinstance(value.metadata, Mapping):
        return False

    return True


@dataclass(frozen=True, kw_only=True)
class SettlementProposal:
    """Immutable settlement proposal aggregate.

    This is a reference-only planning proposal. It does not execute
    settlement, state-delta application, state mutation, event commitment,
    persistence, replay, or any other runtime behavior.
    """

    proposal_id: str
    result_id: str
    proposed_state_delta_refs: tuple[str, ...]
    validation_result_ref_id: str
    validation_decision: str
    trace_ref_id: str
    dependencies: tuple[ResourceMathDependency, ...] = ()
    visibility_policy: str = "public"
    rollback_accounting_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    calculation_executed: bool = False
    affordability_executed: bool = False
    reservation_authorized: bool = False
    settlement_authorized: bool = False
    consequence_application_authorized: bool = False
    mutation_authorized: bool = False
    state_delta_application_authorized: bool = False
    transaction_execution_authorized: bool = False
    event_commitment_authorized: bool = False
    event_append_authorized: bool = False
    persistence_authorized: bool = False
    replay_authorized: bool = False
    rng_execution_authorized: bool = False
    table_oracle_execution_authorized: bool = False
    model_authority_authorized: bool = False
    live_play_authorized: bool = False
    ui_authorized: bool = False
    conversion_authorized: bool = False
    canon_promotion_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "proposal_id": self.proposal_id,
            "result_id": self.result_id,
            "proposed_state_delta_refs": list(self.proposed_state_delta_refs),
            "validation_result_ref_id": self.validation_result_ref_id,
            "validation_decision": self.validation_decision,
            "trace_ref_id": self.trace_ref_id,
            "dependencies": [d.to_dict() for d in self.dependencies],
            "visibility_policy": self.visibility_policy,
            "rollback_accounting_refs": list(self.rollback_accounting_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }
        for field_name in _RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS:
            result[field_name] = getattr(self, field_name)
        return result


def create_settlement_proposal(
    *,
    proposal_id: str,
    result_id: str,
    proposed_state_delta_refs: Sequence[str],
    validation_result_ref_id: str,
    validation_decision: str,
    trace_ref_id: str,
    dependencies: Sequence[ResourceMathDependency] | None = None,
    visibility_policy: str = "public",
    rollback_accounting_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
    result: ResourceMathResult | None = None,
    calculation_executed: bool = False,
    affordability_executed: bool = False,
    reservation_authorized: bool = False,
    settlement_authorized: bool = False,
    consequence_application_authorized: bool = False,
    mutation_authorized: bool = False,
    state_delta_application_authorized: bool = False,
    transaction_execution_authorized: bool = False,
    event_commitment_authorized: bool = False,
    event_append_authorized: bool = False,
    persistence_authorized: bool = False,
    replay_authorized: bool = False,
    rng_execution_authorized: bool = False,
    table_oracle_execution_authorized: bool = False,
    model_authority_authorized: bool = False,
    live_play_authorized: bool = False,
    ui_authorized: bool = False,
    conversion_authorized: bool = False,
    canon_promotion_authorized: bool = False,
) -> SettlementProposal:
    """Create a validated SettlementProposal aggregate."""
    error_cls = InvalidSettlementProposalError

    _validate_non_empty_string(proposal_id, "proposal_id", error_cls)
    _validate_non_empty_string(result_id, "result_id", error_cls)
    _validate_non_empty_string(validation_result_ref_id, "validation_result_ref_id", error_cls)
    _validate_non_empty_string(trace_ref_id, "trace_ref_id", error_cls)

    authority_kwargs = {
        "calculation_executed": calculation_executed,
        "affordability_executed": affordability_executed,
        "reservation_authorized": reservation_authorized,
        "settlement_authorized": settlement_authorized,
        "consequence_application_authorized": consequence_application_authorized,
        "mutation_authorized": mutation_authorized,
        "state_delta_application_authorized": state_delta_application_authorized,
        "transaction_execution_authorized": transaction_execution_authorized,
        "event_commitment_authorized": event_commitment_authorized,
        "event_append_authorized": event_append_authorized,
        "persistence_authorized": persistence_authorized,
        "replay_authorized": replay_authorized,
        "rng_execution_authorized": rng_execution_authorized,
        "table_oracle_execution_authorized": table_oracle_execution_authorized,
        "model_authority_authorized": model_authority_authorized,
        "live_play_authorized": live_play_authorized,
        "ui_authorized": ui_authorized,
        "conversion_authorized": conversion_authorized,
        "canon_promotion_authorized": canon_promotion_authorized,
    }
    _validate_false_only_authority_fields(authority_kwargs, error_cls)

    safe_proposed_state_delta_refs = _normalize_state_delta_refs(
        proposed_state_delta_refs, error_cls
    )

    _validate_non_empty_string(validation_decision, "validation_decision", error_cls)
    if validation_decision not in VALIDATION_INTEGRATION_DECISIONS:
        raise error_cls(
            f"validation_decision must be one of "
            f"{sorted(VALIDATION_INTEGRATION_DECISIONS)}, "
            f"got: {validation_decision!r}"
        )
    if validation_decision != "validation_passed":
        raise error_cls(
            "validation_decision must be 'validation_passed' for a settlement proposal"
        )

    safe_dependencies = _normalize_dataclass_tuple(
        dependencies, "dependencies", ResourceMathDependency, error_cls
    )
    _validate_unique_attr(safe_dependencies, "dependency_id", "dependencies", error_cls)
    seen_dependency_pairs: set[tuple[str, str]] = set()
    for dep in safe_dependencies:
        pair = (dep.dependency_type, dep.reference_id)
        if pair in seen_dependency_pairs:
            raise error_cls(
                f"dependencies has duplicate (dependency_type, reference_id): {pair!r}"
            )
        seen_dependency_pairs.add(pair)
    _validate_dependencies_satisfied(safe_dependencies, error_cls)

    _validate_non_empty_string(visibility_policy, "visibility_policy", error_cls)
    if visibility_policy not in VISIBILITY_POLICIES:
        raise error_cls(
            f"visibility_policy must be one of {sorted(VISIBILITY_POLICIES)}, "
            f"got: {visibility_policy!r}"
        )

    safe_rollback_accounting_refs = _normalize_string_tuple(
        rollback_accounting_refs, "rollback_accounting_refs", error_cls
    )
    safe_metadata = _safe_metadata(metadata, error_cls)

    if result is not None:
        if result_id != result.result_id:
            raise error_cls(
                f"result_id {result_id!r} does not match supplied result "
                f"result_id {result.result_id!r}"
            )
        if validation_result_ref_id != result.validation_result_ref_id:
            raise error_cls(
                f"validation_result_ref_id {validation_result_ref_id!r} does not match "
                f"supplied result validation_result_ref_id "
                f"{result.validation_result_ref_id!r}"
            )
        if validation_decision != result.validation_decision:
            raise error_cls(
                f"validation_decision {validation_decision!r} does not match "
                f"supplied result validation_decision {result.validation_decision!r}"
            )
        if result.validation_decision != "validation_passed":
            raise error_cls(
                "supplied result validation_decision must be 'validation_passed'"
            )

    return SettlementProposal(
        proposal_id=proposal_id,
        result_id=result_id,
        proposed_state_delta_refs=safe_proposed_state_delta_refs,
        validation_result_ref_id=validation_result_ref_id,
        validation_decision=validation_decision,
        trace_ref_id=trace_ref_id,
        dependencies=safe_dependencies,
        visibility_policy=visibility_policy,
        rollback_accounting_refs=safe_rollback_accounting_refs,
        metadata=safe_metadata,
        **authority_kwargs,
    )


def validate_settlement_proposal(
    value: object,
    *,
    result: ResourceMathResult | None = None,
) -> bool:
    if not isinstance(value, SettlementProposal):
        return False
    if not isinstance(value.proposal_id, str) or not value.proposal_id.strip():
        return False
    if not isinstance(value.result_id, str) or not value.result_id.strip():
        return False
    if not isinstance(value.validation_result_ref_id, str) or not value.validation_result_ref_id.strip():
        return False
    if not isinstance(value.trace_ref_id, str) or not value.trace_ref_id.strip():
        return False

    if not isinstance(value.proposed_state_delta_refs, tuple):
        return False
    if len(value.proposed_state_delta_refs) == 0:
        return False
    seen_deltas: set[str] = set()
    for ref in value.proposed_state_delta_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False
        if ref in seen_deltas:
            return False
        seen_deltas.add(ref)

    if (
        not isinstance(value.validation_decision, str)
        or not value.validation_decision.strip()
    ):
        return False
    if value.validation_decision not in VALIDATION_INTEGRATION_DECISIONS:
        return False
    if value.validation_decision != "validation_passed":
        return False

    if not isinstance(value.dependencies, tuple):
        return False
    dependency_ids: set[str] = set()
    dependency_pairs: set[tuple[str, str]] = set()
    for dep in value.dependencies:
        if not validate_resource_math_dependency(dep):
            return False
        if dep.dependency_id in dependency_ids:
            return False
        dependency_ids.add(dep.dependency_id)
        pair = (dep.dependency_type, dep.reference_id)
        if pair in dependency_pairs:
            return False
        dependency_pairs.add(pair)
        if dep.required and not dep.satisfied:
            return False

    if value.visibility_policy not in VISIBILITY_POLICIES:
        return False

    if not isinstance(value.rollback_accounting_refs, tuple):
        return False
    for ref in value.rollback_accounting_refs:
        if not isinstance(ref, str) or not ref.strip():
            return False

    for field_name in _RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS:
        if getattr(value, field_name) is not False:
            return False

    if result is not None:
        if value.result_id != result.result_id:
            return False
        if value.validation_result_ref_id != result.validation_result_ref_id:
            return False
        if value.validation_decision != result.validation_decision:
            return False
        if result.validation_decision != "validation_passed":
            return False

    if not isinstance(value.metadata, Mapping):
        return False

    return True
