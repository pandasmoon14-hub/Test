"""Action legality gate integration skeleton — RT-001C typed reference-only surfaces.

RUNTIME-DOMAIN-RT-001C: integrates the RT-001B action legality skeleton into the
PR-9A through PR-9E command-path reference seam as frozen, keyword-only,
reference-only dataclasses, controlled constants, validators, and deterministic
serializers.

This module is a skeleton only: no legality evaluation engine, no command
execution, no state reads beyond inert references, no state mutation, no
event append, no event commitment, no persistence or replay writes, no
RNG/table/oracle execution, no resource/consequence math execution, no
affordability calculation, no reservation, no settlement, no consequence
application, no combat resolution, no ability/effect/skill resolution, no
inventory mutation, no mission/clue/reward mutation, no social/faction
mutation, no context packet compilation, no model calls, no prompt rendering,
no prompt execution, no prose parsing, no narration generation, no live-play
adapter, no UI/client behavior, no conversion, no sourcebook inclusion, and
no canon promotion.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.action_legality_skeleton import (
    BLOCKER_CLASSES,
    DEPENDENCY_OWNERS,
    LEGALITY_STATUSES,
    REFERENCE_KINDS,
    SAFE_PLAYER_MESSAGES,
    ActionLegalityAuthorityFlags,
    ActionLegalityBackendDetail,
    ActionLegalityBlocker,
    ActionLegalityDependencyReference,
    ActionLegalityReference,
    ActionLegalityRequest,
    ActionLegalityResult,
    ActionLegalitySubjectReference,
    ActionLegalityTargetReference,
    ActionLegalityVisibilityEnvelope,
    InvalidActionLegalityAuthorityFlagsError,
    make_action_legality_backend_detail,
    make_action_legality_blocker,
    make_action_legality_dependency_reference,
    make_action_legality_reference,
    make_action_legality_request,
    make_action_legality_result,
    make_action_legality_subject_reference,
    make_action_legality_target_reference,
    make_action_legality_visibility_envelope,
    validate_action_legality_reference,
    validate_action_legality_request,
    validate_action_legality_result,
)

__all__ = [
    # Constants
    "ACTION_LEGALITY_GATE_INTEGRATION_STAGES",
    "ACTION_LEGALITY_GATE_ROUTES",
    "ACTION_LEGALITY_GATE_DEFAULT_STATUSES",
    "ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE",
    # Error hierarchy
    "ActionLegalityGateIntegrationSkeletonError",
    "InvalidActionLegalityGateInputRefsError",
    "InvalidActionLegalityGateDependencyPlanError",
    "InvalidActionLegalityGateIntegrationRequestError",
    "InvalidActionLegalityGateIntegrationResultError",
    "InvalidActionLegalityGateIntegrationAuthorityFlagsError",
    # Dataclasses
    "ActionLegalityGateInputRefs",
    "ActionLegalityGateDependencyPlan",
    "ActionLegalityGateIntegrationAuthorityFlags",
    "ActionLegalityGateIntegrationRequest",
    "ActionLegalityGateIntegrationResult",
    # Factory functions
    "create_action_legality_gate_input_refs",
    "create_action_legality_gate_dependency_plan",
    "create_action_legality_gate_integration_authority_flags",
    "create_action_legality_gate_integration_request",
    "create_action_legality_gate_integration_result",
    # Builder functions
    "build_action_legality_request_from_gate_integration",
    "build_deferred_action_legality_result_from_gate_integration",
    "build_unknown_action_legality_result_from_gate_integration",
    "build_action_legality_gate_integration_result",
    # Serializers
    "serialize_action_legality_gate_integration_result",
    "serialize_action_legality_gate_integration_result_visible",
    # Validators
    "validate_action_legality_gate_input_refs",
    "validate_action_legality_gate_dependency_plan",
    "validate_action_legality_gate_integration_request",
    "validate_action_legality_gate_integration_result",
    "validate_action_legality_gate_integration_authority_flags",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ACTION_LEGALITY_GATE_INTEGRATION_STAGES = frozenset({
    "input_refs_received",
    "command_assembly_ref_checked",
    "command_kind_route_ref_checked",
    "validation_bridge_ref_checked",
    "transaction_preview_ref_checked",
    "legality_request_built",
    "legality_result_built",
    "integration_result_built",
})

ACTION_LEGALITY_GATE_ROUTES = frozenset({
    "scene_command_execution",
    "command_kind_routing",
    "validation_integration_bridge",
    "transaction_preview_packet_bridge",
    "resource_consequence_math_reference",
    "rng_table_oracle_reference",
    "state_delta_reference",
    "event_commitment_reference",
    "context_packet_reference",
    "persistence_replay_reference",
    "doctrine_review_reference",
    "schema_review_reference",
    "source_local_review_reference",
})

ACTION_LEGALITY_GATE_DEFAULT_STATUSES = frozenset({
    "deferred",
    "unknown",
})

ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE = (
    "This module is reference-only and authorizes no legality engine or execution."
)


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------

class ActionLegalityGateIntegrationSkeletonError(ValueError):
    """Base error for action legality gate integration skeleton operations."""


class InvalidActionLegalityGateInputRefsError(
    ActionLegalityGateIntegrationSkeletonError,
):
    """Raised when input refs fail validation."""


class InvalidActionLegalityGateDependencyPlanError(
    ActionLegalityGateIntegrationSkeletonError,
):
    """Raised when dependency plan fails validation."""


class InvalidActionLegalityGateIntegrationRequestError(
    ActionLegalityGateIntegrationSkeletonError,
):
    """Raised when integration request fails validation."""


class InvalidActionLegalityGateIntegrationResultError(
    ActionLegalityGateIntegrationSkeletonError,
):
    """Raised when integration result fails validation."""


class InvalidActionLegalityGateIntegrationAuthorityFlagsError(
    ActionLegalityGateIntegrationSkeletonError,
):
    """Raised when authority flags contain any non-False value."""


# ---------------------------------------------------------------------------
# Internal validation helpers
# ---------------------------------------------------------------------------

def _validate_non_empty_str(
    value: object, name: str, error_cls: type[Exception],
) -> str:
    if not isinstance(value, str) or not value:
        raise error_cls(f"{name} must be a non-empty string, got {value!r}")
    return value


def _validate_optional_str(
    value: object, name: str, error_cls: type[Exception],
) -> str | None:
    if value is None:
        return None
    return _validate_non_empty_str(value, name, error_cls)


def _validate_json_safe(value: Any, path: str, error_cls: type[Exception]) -> None:
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, bool):
            return
        if isinstance(value, int) and not isinstance(value, bool):
            return
        if isinstance(value, (str, float, type(None))):
            return
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            _validate_json_safe(item, f"{path}[{i}]", error_cls)
    elif isinstance(value, (dict, Mapping)):
        for k, v in value.items():
            if not isinstance(k, str):
                raise error_cls(
                    f"metadata key at {path} must be a string, "
                    f"got {type(k).__name__}"
                )
            _validate_json_safe(v, f"{path}.{k}", error_cls)
    else:
        raise error_cls(
            f"metadata value at {path} is not JSON-safe: "
            f"{type(value).__name__}"
        )


def _safe_metadata(
    metadata: Mapping[str, Any] | None, error_cls: type[Exception],
) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    _validate_json_safe(metadata, "metadata", error_cls)
    return MappingProxyType(copy.deepcopy(dict(metadata)))


def _safe_obj_tuple(
    value: Sequence[Any] | None,
    name: str,
    error_cls: type[Exception],
    obj_type: type,
) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)):
        raise error_cls(f"{name} must not be a bare string")
    if not isinstance(value, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[Any] = []
    for i, elem in enumerate(value):
        if not isinstance(elem, obj_type):
            raise error_cls(
                f"{name}[{i}] must be a {obj_type.__name__}, "
                f"got {type(elem).__name__}"
            )
        result.append(elem)
    return tuple(result)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ActionLegalityGateInputRefs:
    """Input reference bundle bridging PR-9A through PR-9E command-path refs
    into the action legality gate. No execution, no state reads."""

    scene_command_assembly_ref: ActionLegalityReference
    command_kind_routing_ref: ActionLegalityReference
    validation_bridge_ref: ActionLegalityReference
    transaction_preview_bridge_ref: ActionLegalityReference | None = None
    resource_preview_ref: ActionLegalityReference | None = None
    context_packet_ref: ActionLegalityReference | None = None
    event_ledger_candidate_ref: ActionLegalityReference | None = None
    state_delta_candidate_ref: ActionLegalityReference | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.scene_command_assembly_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"scene_command_assembly_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.scene_command_assembly_ref).__name__}"
            )
        if not isinstance(
            self.command_kind_routing_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"command_kind_routing_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.command_kind_routing_ref).__name__}"
            )
        if not isinstance(
            self.validation_bridge_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"validation_bridge_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.validation_bridge_ref).__name__}"
            )
        if self.transaction_preview_bridge_ref is not None and not isinstance(
            self.transaction_preview_bridge_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"transaction_preview_bridge_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.transaction_preview_bridge_ref).__name__}"
            )
        if self.resource_preview_ref is not None and not isinstance(
            self.resource_preview_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"resource_preview_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.resource_preview_ref).__name__}"
            )
        if self.context_packet_ref is not None and not isinstance(
            self.context_packet_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"context_packet_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.context_packet_ref).__name__}"
            )
        if self.event_ledger_candidate_ref is not None and not isinstance(
            self.event_ledger_candidate_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"event_ledger_candidate_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.event_ledger_candidate_ref).__name__}"
            )
        if self.state_delta_candidate_ref is not None and not isinstance(
            self.state_delta_candidate_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityGateInputRefsError(
                f"state_delta_candidate_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.state_delta_candidate_ref).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidActionLegalityGateInputRefsError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_command_assembly_ref": (
                self.scene_command_assembly_ref.to_dict()
            ),
            "command_kind_routing_ref": (
                self.command_kind_routing_ref.to_dict()
            ),
            "validation_bridge_ref": self.validation_bridge_ref.to_dict(),
            "transaction_preview_bridge_ref": (
                self.transaction_preview_bridge_ref.to_dict()
                if self.transaction_preview_bridge_ref is not None else None
            ),
            "resource_preview_ref": (
                self.resource_preview_ref.to_dict()
                if self.resource_preview_ref is not None else None
            ),
            "context_packet_ref": (
                self.context_packet_ref.to_dict()
                if self.context_packet_ref is not None else None
            ),
            "event_ledger_candidate_ref": (
                self.event_ledger_candidate_ref.to_dict()
                if self.event_ledger_candidate_ref is not None else None
            ),
            "state_delta_candidate_ref": (
                self.state_delta_candidate_ref.to_dict()
                if self.state_delta_candidate_ref is not None else None
            ),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityGateDependencyPlan:
    """Dependency plan for the gate integration — references future owner
    handoffs without executing them."""

    plan_id: str
    dependency_refs: tuple[ActionLegalityDependencyReference, ...] = ()
    default_blocker_class: str = "runtime_owner_handoff"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.plan_id, "plan_id",
            InvalidActionLegalityGateDependencyPlanError,
        )
        object.__setattr__(
            self, "dependency_refs",
            _safe_obj_tuple(
                self.dependency_refs, "dependency_refs",
                InvalidActionLegalityGateDependencyPlanError,
                ActionLegalityDependencyReference,
            ),
        )
        _validate_non_empty_str(
            self.default_blocker_class, "default_blocker_class",
            InvalidActionLegalityGateDependencyPlanError,
        )
        if self.default_blocker_class not in BLOCKER_CLASSES:
            raise InvalidActionLegalityGateDependencyPlanError(
                f"default_blocker_class must be one of "
                f"{sorted(BLOCKER_CLASSES)}, "
                f"got {self.default_blocker_class!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityGateDependencyPlanError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "dependency_refs": [d.to_dict() for d in self.dependency_refs],
            "default_blocker_class": self.default_blocker_class,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityGateIntegrationAuthorityFlags:
    """All authority flags must be false-only. Any non-False value raises
    during construction. Extends the RT-001B authority flags with
    gate-integration-specific flags."""

    action_legality_engine_authorized: bool = False
    real_legality_evaluation_authorized: bool = False
    command_execution_authorized: bool = False
    state_read_authorized: bool = False
    state_mutation_authorized: bool = False
    event_append_authorized: bool = False
    event_commitment_authorized: bool = False
    persistence_write_authorized: bool = False
    replay_authorized: bool = False
    rng_execution_authorized: bool = False
    table_oracle_execution_authorized: bool = False
    resource_math_execution_authorized: bool = False
    affordability_calculation_authorized: bool = False
    reservation_authorized: bool = False
    settlement_authorized: bool = False
    consequence_application_authorized: bool = False
    combat_resolution_authorized: bool = False
    ability_resolution_authorized: bool = False
    inventory_mutation_authorized: bool = False
    mission_mutation_authorized: bool = False
    social_faction_mutation_authorized: bool = False
    context_packet_compilation_authorized: bool = False
    model_call_authorized: bool = False
    prompt_rendering_authorized: bool = False
    prompt_execution_authorized: bool = False
    prose_parsing_authorized: bool = False
    narration_generation_authorized: bool = False
    live_play_authorized: bool = False
    ui_client_authorized: bool = False
    conversion_authorized: bool = False
    sourcebook_inclusion_authorized: bool = False
    canon_promotion_authorized: bool = False

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if value is not False:
                raise InvalidActionLegalityGateIntegrationAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in "
                    f"RT-001C skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class ActionLegalityGateIntegrationRequest:
    """Integration request — bridges input refs, subject, targets, command,
    and dependency plan into the legality gate. No execution."""

    request_id: str
    input_refs: ActionLegalityGateInputRefs
    subject_ref: ActionLegalitySubjectReference
    target_refs: tuple[ActionLegalityTargetReference, ...] = ()
    command_ref: ActionLegalityReference
    dependency_plan: ActionLegalityGateDependencyPlan
    authority_flags: ActionLegalityGateIntegrationAuthorityFlags = field(
        default_factory=ActionLegalityGateIntegrationAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidActionLegalityGateIntegrationRequestError,
        )
        if not isinstance(self.input_refs, ActionLegalityGateInputRefs):
            raise InvalidActionLegalityGateIntegrationRequestError(
                f"input_refs must be an ActionLegalityGateInputRefs, "
                f"got {type(self.input_refs).__name__}"
            )
        if not isinstance(self.subject_ref, ActionLegalitySubjectReference):
            raise InvalidActionLegalityGateIntegrationRequestError(
                f"subject_ref must be an ActionLegalitySubjectReference, "
                f"got {type(self.subject_ref).__name__}"
            )
        object.__setattr__(
            self, "target_refs",
            _safe_obj_tuple(
                self.target_refs, "target_refs",
                InvalidActionLegalityGateIntegrationRequestError,
                ActionLegalityTargetReference,
            ),
        )
        if not isinstance(self.command_ref, ActionLegalityReference):
            raise InvalidActionLegalityGateIntegrationRequestError(
                f"command_ref must be an ActionLegalityReference, "
                f"got {type(self.command_ref).__name__}"
            )
        if not isinstance(
            self.dependency_plan, ActionLegalityGateDependencyPlan,
        ):
            raise InvalidActionLegalityGateIntegrationRequestError(
                f"dependency_plan must be an "
                f"ActionLegalityGateDependencyPlan, "
                f"got {type(self.dependency_plan).__name__}"
            )
        if not isinstance(
            self.authority_flags,
            ActionLegalityGateIntegrationAuthorityFlags,
        ):
            raise InvalidActionLegalityGateIntegrationRequestError(
                f"authority_flags must be an "
                f"ActionLegalityGateIntegrationAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityGateIntegrationRequestError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "input_refs": self.input_refs.to_dict(),
            "subject_ref": self.subject_ref.to_dict(),
            "target_refs": [t.to_dict() for t in self.target_refs],
            "command_ref": self.command_ref.to_dict(),
            "dependency_plan": self.dependency_plan.to_dict(),
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityGateIntegrationResult:
    """Integration result — contains both the RT-001B legality request and
    result, plus gate-level input refs, dependency plan, trace refs, and
    authority flags. No execution."""

    result_id: str
    request_id: str
    legality_request: ActionLegalityRequest
    legality_result: ActionLegalityResult
    input_refs: ActionLegalityGateInputRefs
    dependency_plan: ActionLegalityGateDependencyPlan
    trace_refs: tuple[ActionLegalityReference, ...] = ()
    authority_flags: ActionLegalityGateIntegrationAuthorityFlags = field(
        default_factory=ActionLegalityGateIntegrationAuthorityFlags,
    )
    non_authority_note: str = ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.result_id, "result_id",
            InvalidActionLegalityGateIntegrationResultError,
        )
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidActionLegalityGateIntegrationResultError,
        )
        if not isinstance(self.legality_request, ActionLegalityRequest):
            raise InvalidActionLegalityGateIntegrationResultError(
                f"legality_request must be an ActionLegalityRequest, "
                f"got {type(self.legality_request).__name__}"
            )
        if not isinstance(self.legality_result, ActionLegalityResult):
            raise InvalidActionLegalityGateIntegrationResultError(
                f"legality_result must be an ActionLegalityResult, "
                f"got {type(self.legality_result).__name__}"
            )
        if not isinstance(self.input_refs, ActionLegalityGateInputRefs):
            raise InvalidActionLegalityGateIntegrationResultError(
                f"input_refs must be an ActionLegalityGateInputRefs, "
                f"got {type(self.input_refs).__name__}"
            )
        if not isinstance(
            self.dependency_plan, ActionLegalityGateDependencyPlan,
        ):
            raise InvalidActionLegalityGateIntegrationResultError(
                f"dependency_plan must be an "
                f"ActionLegalityGateDependencyPlan, "
                f"got {type(self.dependency_plan).__name__}"
            )
        object.__setattr__(
            self, "trace_refs",
            _safe_obj_tuple(
                self.trace_refs, "trace_refs",
                InvalidActionLegalityGateIntegrationResultError,
                ActionLegalityReference,
            ),
        )
        if not isinstance(
            self.authority_flags,
            ActionLegalityGateIntegrationAuthorityFlags,
        ):
            raise InvalidActionLegalityGateIntegrationResultError(
                f"authority_flags must be an "
                f"ActionLegalityGateIntegrationAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidActionLegalityGateIntegrationResultError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityGateIntegrationResultError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "legality_request": self.legality_request.to_dict(),
            "legality_result": self.legality_result.to_dict(),
            "input_refs": self.input_refs.to_dict(),
            "dependency_plan": self.dependency_plan.to_dict(),
            "trace_refs": [t.to_dict() for t in self.trace_refs],
            "authority_flags": self.authority_flags.to_dict(),
            "non_authority_note": self.non_authority_note,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_action_legality_gate_input_refs(
    *,
    scene_command_assembly_ref: ActionLegalityReference,
    command_kind_routing_ref: ActionLegalityReference,
    validation_bridge_ref: ActionLegalityReference,
    transaction_preview_bridge_ref: ActionLegalityReference | None = None,
    resource_preview_ref: ActionLegalityReference | None = None,
    context_packet_ref: ActionLegalityReference | None = None,
    event_ledger_candidate_ref: ActionLegalityReference | None = None,
    state_delta_candidate_ref: ActionLegalityReference | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityGateInputRefs:
    return ActionLegalityGateInputRefs(
        scene_command_assembly_ref=scene_command_assembly_ref,
        command_kind_routing_ref=command_kind_routing_ref,
        validation_bridge_ref=validation_bridge_ref,
        transaction_preview_bridge_ref=transaction_preview_bridge_ref,
        resource_preview_ref=resource_preview_ref,
        context_packet_ref=context_packet_ref,
        event_ledger_candidate_ref=event_ledger_candidate_ref,
        state_delta_candidate_ref=state_delta_candidate_ref,
        metadata=metadata,
    )


def create_action_legality_gate_dependency_plan(
    *,
    plan_id: str,
    dependency_refs: Sequence[ActionLegalityDependencyReference] | None = None,
    default_blocker_class: str = "runtime_owner_handoff",
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityGateDependencyPlan:
    return ActionLegalityGateDependencyPlan(
        plan_id=plan_id,
        dependency_refs=dependency_refs,
        default_blocker_class=default_blocker_class,
        metadata=metadata,
    )


def create_action_legality_gate_integration_authority_flags() -> (
    ActionLegalityGateIntegrationAuthorityFlags
):
    return ActionLegalityGateIntegrationAuthorityFlags()


def create_action_legality_gate_integration_request(
    *,
    request_id: str,
    input_refs: ActionLegalityGateInputRefs,
    subject_ref: ActionLegalitySubjectReference,
    command_ref: ActionLegalityReference,
    dependency_plan: ActionLegalityGateDependencyPlan,
    target_refs: Sequence[ActionLegalityTargetReference] | None = None,
    authority_flags: ActionLegalityGateIntegrationAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityGateIntegrationRequest:
    return ActionLegalityGateIntegrationRequest(
        request_id=request_id,
        input_refs=input_refs,
        subject_ref=subject_ref,
        command_ref=command_ref,
        dependency_plan=dependency_plan,
        target_refs=target_refs,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ActionLegalityGateIntegrationAuthorityFlags()
        ),
        metadata=metadata,
    )


def create_action_legality_gate_integration_result(
    *,
    result_id: str,
    request_id: str,
    legality_request: ActionLegalityRequest,
    legality_result: ActionLegalityResult,
    input_refs: ActionLegalityGateInputRefs,
    dependency_plan: ActionLegalityGateDependencyPlan,
    trace_refs: Sequence[ActionLegalityReference] | None = None,
    authority_flags: ActionLegalityGateIntegrationAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityGateIntegrationResult:
    return ActionLegalityGateIntegrationResult(
        result_id=result_id,
        request_id=request_id,
        legality_request=legality_request,
        legality_result=legality_result,
        input_refs=input_refs,
        dependency_plan=dependency_plan,
        trace_refs=trace_refs,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ActionLegalityGateIntegrationAuthorityFlags()
        ),
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Builder functions
# ---------------------------------------------------------------------------


def build_action_legality_request_from_gate_integration(
    *, request: ActionLegalityGateIntegrationRequest,
) -> ActionLegalityRequest:
    """Transform gate integration request refs into an RT-001B
    ActionLegalityRequest. Does NOT evaluate legality, inspect state,
    resolve actor/target existence, or call PR-9A/9C/9D/9E builders.
    Just transforms refs."""
    return make_action_legality_request(
        request_id=request.request_id,
        command_ref=request.command_ref,
        subject_ref=request.subject_ref,
        target_refs=request.target_refs,
        routed_command_kind_ref=request.input_refs.command_kind_routing_ref,
        validation_ref=request.input_refs.validation_bridge_ref,
        transaction_preview_ref=(
            request.input_refs.transaction_preview_bridge_ref
        ),
        dependency_refs=request.dependency_plan.dependency_refs,
        authority_flags=ActionLegalityAuthorityFlags(),
    )


def build_deferred_action_legality_result_from_gate_integration(
    *,
    result_id: str,
    request_id: str,
    dependency_plan: ActionLegalityGateDependencyPlan,
) -> ActionLegalityResult:
    """Produce an RT-001B ActionLegalityResult with status 'deferred'.
    Includes at least one blocker using blocker class
    'runtime_owner_handoff'. Uses safe player-visible message. Includes
    backend-only detail identifying missing downstream owner references."""
    backend_detail = make_action_legality_backend_detail(
        detail_id=f"{result_id}_detail",
        blocker_class="runtime_owner_handoff",
        owner_route="action_legality_gate_integration",
        resolution_path_summary=(
            "Downstream owner services not available in skeleton."
        ),
    )
    blocker = make_action_legality_blocker(
        blocker_id=f"{result_id}_blocker",
        blocker_class="runtime_owner_handoff",
        legality_status="deferred",
        player_visible_message=(
            "This action cannot be processed at this time."
        ),
        backend_detail=backend_detail,
        dependency_refs=list(dependency_plan.dependency_refs),
    )
    envelope = make_action_legality_visibility_envelope(
        player_visible_message=(
            "This action cannot be processed at this time."
        ),
        player_visible_blockers=[
            "This action cannot be processed at this time.",
        ],
        backend_only_detail=backend_detail,
    )
    return make_action_legality_result(
        result_id=result_id,
        request_id=request_id,
        legality_status="deferred",
        blockers=[blocker],
        dependency_refs=list(dependency_plan.dependency_refs),
        visibility_envelope=envelope,
        authority_flags=ActionLegalityAuthorityFlags(),
    )


def build_unknown_action_legality_result_from_gate_integration(
    *,
    result_id: str,
    request_id: str,
    unknown_route: str = "action_legality_gate_integration",
) -> ActionLegalityResult:
    """Produce an RT-001B ActionLegalityResult with status 'unknown'.
    Uses safe player-visible message 'Action could not be validated.'
    Includes a blocker identifying the unknown route."""
    backend_detail = make_action_legality_backend_detail(
        detail_id=f"{result_id}_detail",
        blocker_class="runtime_owner_handoff",
        owner_route=unknown_route,
        resolution_path_summary=(
            "Integration skeleton cannot classify missing owner/handoff."
        ),
    )
    blocker = make_action_legality_blocker(
        blocker_id=f"{result_id}_blocker",
        blocker_class="runtime_owner_handoff",
        legality_status="unknown",
        player_visible_message="Action could not be validated.",
        backend_detail=backend_detail,
    )
    envelope = make_action_legality_visibility_envelope(
        player_visible_message="Action could not be validated.",
        player_visible_blockers=["Action could not be validated."],
    )
    return make_action_legality_result(
        result_id=result_id,
        request_id=request_id,
        legality_status="unknown",
        blockers=[blocker],
        visibility_envelope=envelope,
        authority_flags=ActionLegalityAuthorityFlags(),
    )


def build_action_legality_gate_integration_result(
    *,
    result_id: str,
    request: ActionLegalityGateIntegrationRequest,
    status_override: str = "deferred",
) -> ActionLegalityGateIntegrationResult:
    """Build request and result together. Default behavior: 'deferred',
    not 'legal'. Accepts an explicit status override only for 'deferred'
    or 'unknown'."""
    if status_override not in ACTION_LEGALITY_GATE_DEFAULT_STATUSES:
        raise ActionLegalityGateIntegrationSkeletonError(
            f"status_override must be one of "
            f"{sorted(ACTION_LEGALITY_GATE_DEFAULT_STATUSES)}, "
            f"got {status_override!r}"
        )
    legality_request = build_action_legality_request_from_gate_integration(
        request=request,
    )
    if status_override == "deferred":
        legality_result = (
            build_deferred_action_legality_result_from_gate_integration(
                result_id=f"{result_id}_legality",
                request_id=request.request_id,
                dependency_plan=request.dependency_plan,
            )
        )
    else:
        legality_result = (
            build_unknown_action_legality_result_from_gate_integration(
                result_id=f"{result_id}_legality",
                request_id=request.request_id,
            )
        )
    return create_action_legality_gate_integration_result(
        result_id=result_id,
        request_id=request.request_id,
        legality_request=legality_request,
        legality_result=legality_result,
        input_refs=request.input_refs,
        dependency_plan=request.dependency_plan,
    )


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------


def serialize_action_legality_gate_integration_result(
    result: ActionLegalityGateIntegrationResult,
) -> dict[str, Any]:
    """Full backend serializer. Returns result.to_dict()."""
    return result.to_dict()


def serialize_action_legality_gate_integration_result_visible(
    result: ActionLegalityGateIntegrationResult,
) -> dict[str, Any]:
    """Player-visible serializer. Includes only safe player-facing fields.
    Must NOT include backend-only detail, hidden-information identifiers,
    internal module names, function names, RT owner internals, doctrine ids,
    schema ids, trace internals, or source-local references."""
    legality_result = result.legality_result
    player_visible_message: str | None = None
    if (
        legality_result.visibility_envelope is not None
        and legality_result.visibility_envelope.player_visible_message
    ):
        player_visible_message = (
            legality_result.visibility_envelope.player_visible_message
        )
    visible_blocker_messages: list[str] = []
    if player_visible_message is None:
        for blocker in legality_result.blockers:
            visible_blocker_messages.append(blocker.player_visible_message)
        if visible_blocker_messages:
            player_visible_message = visible_blocker_messages[0]
    else:
        for blocker in legality_result.blockers:
            visible_blocker_messages.append(blocker.player_visible_message)
    return {
        "result_id": result.result_id,
        "request_id": result.request_id,
        "legality_status": legality_result.legality_status,
        "player_visible_message": player_visible_message,
        "visible_blocker_messages": visible_blocker_messages,
        "non_authority_note": result.non_authority_note,
    }


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_action_legality_gate_input_refs(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityGateInputRefs):
        return False
    if not isinstance(
        obj.scene_command_assembly_ref, ActionLegalityReference,
    ):
        return False
    if not validate_action_legality_reference(obj.scene_command_assembly_ref):
        return False
    if not isinstance(
        obj.command_kind_routing_ref, ActionLegalityReference,
    ):
        return False
    if not validate_action_legality_reference(obj.command_kind_routing_ref):
        return False
    if not isinstance(obj.validation_bridge_ref, ActionLegalityReference):
        return False
    if not validate_action_legality_reference(obj.validation_bridge_ref):
        return False
    if obj.transaction_preview_bridge_ref is not None:
        if not isinstance(
            obj.transaction_preview_bridge_ref, ActionLegalityReference,
        ):
            return False
        if not validate_action_legality_reference(
            obj.transaction_preview_bridge_ref,
        ):
            return False
    if obj.resource_preview_ref is not None:
        if not isinstance(
            obj.resource_preview_ref, ActionLegalityReference,
        ):
            return False
        if not validate_action_legality_reference(obj.resource_preview_ref):
            return False
    if obj.context_packet_ref is not None:
        if not isinstance(obj.context_packet_ref, ActionLegalityReference):
            return False
        if not validate_action_legality_reference(obj.context_packet_ref):
            return False
    if obj.event_ledger_candidate_ref is not None:
        if not isinstance(
            obj.event_ledger_candidate_ref, ActionLegalityReference,
        ):
            return False
        if not validate_action_legality_reference(
            obj.event_ledger_candidate_ref,
        ):
            return False
    if obj.state_delta_candidate_ref is not None:
        if not isinstance(
            obj.state_delta_candidate_ref, ActionLegalityReference,
        ):
            return False
        if not validate_action_legality_reference(
            obj.state_delta_candidate_ref,
        ):
            return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_gate_dependency_plan(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityGateDependencyPlan):
        return False
    if not isinstance(obj.plan_id, str) or not obj.plan_id:
        return False
    for dep in obj.dependency_refs:
        if not isinstance(dep, ActionLegalityDependencyReference):
            return False
    if obj.default_blocker_class not in BLOCKER_CLASSES:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_gate_integration_request(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityGateIntegrationRequest):
        return False
    if not isinstance(obj.request_id, str) or not obj.request_id:
        return False
    if not validate_action_legality_gate_input_refs(obj.input_refs):
        return False
    if not isinstance(obj.subject_ref, ActionLegalitySubjectReference):
        return False
    for t in obj.target_refs:
        if not isinstance(t, ActionLegalityTargetReference):
            return False
    if not validate_action_legality_reference(obj.command_ref):
        return False
    if not validate_action_legality_gate_dependency_plan(obj.dependency_plan):
        return False
    if not isinstance(
        obj.authority_flags,
        ActionLegalityGateIntegrationAuthorityFlags,
    ):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_gate_integration_result(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityGateIntegrationResult):
        return False
    if not isinstance(obj.result_id, str) or not obj.result_id:
        return False
    if not isinstance(obj.request_id, str) or not obj.request_id:
        return False
    if not validate_action_legality_request(obj.legality_request):
        return False
    if not validate_action_legality_result(obj.legality_result):
        return False
    if not validate_action_legality_gate_input_refs(obj.input_refs):
        return False
    if not validate_action_legality_gate_dependency_plan(obj.dependency_plan):
        return False
    for t in obj.trace_refs:
        if not validate_action_legality_reference(t):
            return False
    if not isinstance(
        obj.authority_flags,
        ActionLegalityGateIntegrationAuthorityFlags,
    ):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_gate_integration_authority_flags(
    obj: Any,
) -> bool:
    if not isinstance(obj, ActionLegalityGateIntegrationAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True
