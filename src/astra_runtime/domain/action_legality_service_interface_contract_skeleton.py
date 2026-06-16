"""Action legality service interface contract skeleton — RT-001E.

RUNTIME-DOMAIN-RT-001E: defines the service-facing contract boundary between
the action legality gate (RT-001C) and a future action legality evaluation
service. Frozen, keyword-only dataclasses, controlled constants, validators,
factory/builder functions, and deterministic serializers.

This module is a skeleton only: no legality evaluation engine, no command
execution, no state reads, no state mutation, no event append, no event
commitment, no persistence or replay writes, no RNG/table/oracle execution,
no resource/consequence math execution, no affordability calculation, no
reservation, no settlement, no consequence application, no combat resolution,
no ability/effect/skill resolution, no inventory mutation, no mission/clue/
reward mutation, no social/faction mutation, no context packet compilation,
no model calls, no prompt rendering, no prompt execution, no prose parsing,
no narration generation, no live-play adapter, no UI/client behavior, no
conversion, no sourcebook inclusion, and no canon promotion.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.action_legality_skeleton import (
    SAFE_PLAYER_MESSAGES,
    ActionLegalityAuthorityFlags,
    ActionLegalityDependencyReference,
    ActionLegalityReference,
    ActionLegalityRequest,
    ActionLegalityResult,
    InvalidActionLegalityAuthorityFlagsError,
    _safe_metadata,
    _safe_obj_tuple,
    _safe_str_tuple,
    _validate_non_empty_str,
    _validate_optional_str,
    make_action_legality_backend_detail,
    make_action_legality_blocker,
    make_action_legality_dependency_reference,
    make_action_legality_result,
    make_action_legality_visibility_envelope,
)
from astra_runtime.domain.action_legality_gate_integration_skeleton import (
    ActionLegalityGateInputRefs,
    ActionLegalityGateIntegrationResult,
)


__all__ = [
    # Constants
    "ACTION_LEGALITY_SERVICE_INTERFACE_STAGES",
    "ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS",
    "ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES",
    "ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES",
    "ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE",
    # Error hierarchy
    "ActionLegalityServiceInterfaceContractSkeletonError",
    "InvalidActionLegalityServiceInterfaceAuthorityFlagsError",
    "InvalidActionLegalityServiceInterfaceDependencyManifestError",
    "InvalidActionLegalityServiceInterfaceRequestError",
    "InvalidActionLegalityServiceInterfaceResultError",
    "InvalidActionLegalityServiceInterfaceContractSummaryError",
    # Dataclasses
    "ActionLegalityServiceInterfaceAuthorityFlags",
    "ActionLegalityServiceInterfaceDependencyManifest",
    "ActionLegalityServiceInterfaceRequest",
    "ActionLegalityServiceInterfaceResult",
    "ActionLegalityServiceInterfaceContractSummary",
    # Factory functions
    "create_action_legality_service_interface_authority_flags",
    "create_action_legality_service_interface_dependency_manifest",
    "create_action_legality_service_interface_request",
    "create_action_legality_service_interface_result",
    "create_action_legality_service_interface_contract_summary",
    # Builder functions
    "build_action_legality_service_interface_dependency_manifest",
    "build_deferred_action_legality_service_interface_result",
    "build_unknown_action_legality_service_interface_result",
    # Serializers
    "serialize_action_legality_service_interface_result",
    "serialize_action_legality_service_interface_result_visible",
    # Validators
    "validate_action_legality_service_interface_authority_flags",
    "validate_action_legality_service_interface_dependency_manifest",
    "validate_action_legality_service_interface_request",
    "validate_action_legality_service_interface_result",
    "validate_action_legality_service_interface_contract_summary",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ACTION_LEGALITY_SERVICE_INTERFACE_STAGES = frozenset({
    "request_received",
    "dependency_manifest_built",
    "service_result_built",
    "deferred_result_returned",
    "unknown_result_returned",
})

ACTION_LEGALITY_SERVICE_INTERFACE_DEPENDENCY_KINDS = frozenset({
    "validation",
    "resource_math",
    "rng_table_oracle",
    "state_delta",
    "transaction_preview",
    "event_commitment",
    "context_packet",
    "persistence_replay",
    "doctrine_review",
    "schema_review",
    "source_local_review",
    "combat_resolution",
    "ability_resolution",
    "skill_resolution",
    "effect_resolution",
})

ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES = frozenset({
    "deferred",
    "unknown",
})

ACTION_LEGALITY_SERVICE_INTERFACE_OWNER_ROUTES = frozenset({
    "validation_owner",
    "resource_math_owner",
    "rng_table_oracle_owner",
    "state_delta_owner",
    "transaction_preview_owner",
    "event_commitment_owner",
    "context_packet_owner",
    "persistence_replay_owner",
    "doctrine_review_owner",
    "schema_review_owner",
    "source_local_review_owner",
    "combat_resolution_owner",
    "ability_resolution_owner",
    "skill_resolution_owner",
    "effect_resolution_owner",
})

ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE = (
    "This interface contract is skeleton-only and authorizes no legality "
    "evaluation, command execution, state access, or runtime behavior."
)


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------

class ActionLegalityServiceInterfaceContractSkeletonError(ValueError):
    """Base error for action legality service interface contract operations."""


class InvalidActionLegalityServiceInterfaceAuthorityFlagsError(
    ActionLegalityServiceInterfaceContractSkeletonError,
):
    """Raised when authority flags contain any non-False value."""


class InvalidActionLegalityServiceInterfaceDependencyManifestError(
    ActionLegalityServiceInterfaceContractSkeletonError,
):
    """Raised when dependency manifest fails validation."""


class InvalidActionLegalityServiceInterfaceRequestError(
    ActionLegalityServiceInterfaceContractSkeletonError,
):
    """Raised when service interface request fails validation."""


class InvalidActionLegalityServiceInterfaceResultError(
    ActionLegalityServiceInterfaceContractSkeletonError,
):
    """Raised when service interface result fails validation."""


class InvalidActionLegalityServiceInterfaceContractSummaryError(
    ActionLegalityServiceInterfaceContractSkeletonError,
):
    """Raised when contract summary fails validation."""


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ActionLegalityServiceInterfaceAuthorityFlags:
    """All authority flags must be false-only. Any non-False value raises
    during construction."""

    legality_engine_authorized: bool = False
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
    skill_resolution_authorized: bool = False
    effect_resolution_authorized: bool = False
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
                raise InvalidActionLegalityServiceInterfaceAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in "
                    f"RT-001E skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class ActionLegalityServiceInterfaceDependencyManifest:
    """Dependency manifest describing what future owner services would be
    needed for real legality evaluation. Does not call owner services."""

    manifest_id: str
    dependency_refs: tuple[ActionLegalityDependencyReference, ...] = ()
    required_owner_routes: tuple[str, ...] = ()
    unavailable_owner_routes: tuple[str, ...] = ()
    deferred_reason: str = "skeleton_interface_only"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.manifest_id, "manifest_id",
            InvalidActionLegalityServiceInterfaceDependencyManifestError,
        )
        object.__setattr__(
            self, "dependency_refs",
            _safe_obj_tuple(
                self.dependency_refs, "dependency_refs",
                InvalidActionLegalityServiceInterfaceDependencyManifestError,
                ActionLegalityDependencyReference,
            ),
        )
        object.__setattr__(
            self, "required_owner_routes",
            _safe_str_tuple(
                self.required_owner_routes, "required_owner_routes",
                InvalidActionLegalityServiceInterfaceDependencyManifestError,
            ),
        )
        object.__setattr__(
            self, "unavailable_owner_routes",
            _safe_str_tuple(
                self.unavailable_owner_routes, "unavailable_owner_routes",
                InvalidActionLegalityServiceInterfaceDependencyManifestError,
            ),
        )
        _validate_non_empty_str(
            self.deferred_reason, "deferred_reason",
            InvalidActionLegalityServiceInterfaceDependencyManifestError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityServiceInterfaceDependencyManifestError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "dependency_refs": [d.to_dict() for d in self.dependency_refs],
            "required_owner_routes": list(self.required_owner_routes),
            "unavailable_owner_routes": list(self.unavailable_owner_routes),
            "deferred_reason": self.deferred_reason,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityServiceInterfaceRequest:
    """Service interface request — carries an RT-001B legality request, gate
    input references, dependency manifest, requested stage, and authority
    flags. No execution."""

    request_id: str
    legality_request: ActionLegalityRequest
    gate_integration_result_ref: ActionLegalityReference | None = None
    gate_input_refs: ActionLegalityGateInputRefs | None = None
    dependency_manifest: ActionLegalityServiceInterfaceDependencyManifest | None = None
    requested_stage: str = "request_received"
    authority_flags: ActionLegalityServiceInterfaceAuthorityFlags = field(
        default_factory=ActionLegalityServiceInterfaceAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidActionLegalityServiceInterfaceRequestError,
        )
        if not isinstance(self.legality_request, ActionLegalityRequest):
            raise InvalidActionLegalityServiceInterfaceRequestError(
                f"legality_request must be an ActionLegalityRequest, "
                f"got {type(self.legality_request).__name__}"
            )
        if self.gate_integration_result_ref is not None and not isinstance(
            self.gate_integration_result_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityServiceInterfaceRequestError(
                f"gate_integration_result_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.gate_integration_result_ref).__name__}"
            )
        if self.gate_input_refs is not None and not isinstance(
            self.gate_input_refs, ActionLegalityGateInputRefs,
        ):
            raise InvalidActionLegalityServiceInterfaceRequestError(
                f"gate_input_refs must be an ActionLegalityGateInputRefs, "
                f"got {type(self.gate_input_refs).__name__}"
            )
        if self.dependency_manifest is not None and not isinstance(
            self.dependency_manifest,
            ActionLegalityServiceInterfaceDependencyManifest,
        ):
            raise InvalidActionLegalityServiceInterfaceRequestError(
                f"dependency_manifest must be an "
                f"ActionLegalityServiceInterfaceDependencyManifest, "
                f"got {type(self.dependency_manifest).__name__}"
            )
        _validate_non_empty_str(
            self.requested_stage, "requested_stage",
            InvalidActionLegalityServiceInterfaceRequestError,
        )
        if self.requested_stage not in ACTION_LEGALITY_SERVICE_INTERFACE_STAGES:
            raise InvalidActionLegalityServiceInterfaceRequestError(
                f"requested_stage must be one of "
                f"{sorted(ACTION_LEGALITY_SERVICE_INTERFACE_STAGES)}, "
                f"got {self.requested_stage!r}"
            )
        if not isinstance(
            self.authority_flags,
            ActionLegalityServiceInterfaceAuthorityFlags,
        ):
            raise InvalidActionLegalityServiceInterfaceRequestError(
                f"authority_flags must be an "
                f"ActionLegalityServiceInterfaceAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityServiceInterfaceRequestError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "legality_request": self.legality_request.to_dict(),
            "gate_integration_result_ref": (
                self.gate_integration_result_ref.to_dict()
                if self.gate_integration_result_ref is not None else None
            ),
            "gate_input_refs": (
                self.gate_input_refs.to_dict()
                if self.gate_input_refs is not None else None
            ),
            "dependency_manifest": (
                self.dependency_manifest.to_dict()
                if self.dependency_manifest is not None else None
            ),
            "requested_stage": self.requested_stage,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityServiceInterfaceResult:
    """Service interface result — contains the RT-001B legality result,
    dependency manifest, authority flags, and non-authority note. Never
    approves real legality."""

    result_id: str
    request_id: str
    interface_status: str
    legality_result: ActionLegalityResult
    dependency_manifest: ActionLegalityServiceInterfaceDependencyManifest | None = None
    authority_flags: ActionLegalityServiceInterfaceAuthorityFlags = field(
        default_factory=ActionLegalityServiceInterfaceAuthorityFlags,
    )
    non_authority_note: str = ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.result_id, "result_id",
            InvalidActionLegalityServiceInterfaceResultError,
        )
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidActionLegalityServiceInterfaceResultError,
        )
        _validate_non_empty_str(
            self.interface_status, "interface_status",
            InvalidActionLegalityServiceInterfaceResultError,
        )
        if self.interface_status not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES:
            raise InvalidActionLegalityServiceInterfaceResultError(
                f"interface_status must be one of "
                f"{sorted(ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES)}, "
                f"got {self.interface_status!r}"
            )
        if not isinstance(self.legality_result, ActionLegalityResult):
            raise InvalidActionLegalityServiceInterfaceResultError(
                f"legality_result must be an ActionLegalityResult, "
                f"got {type(self.legality_result).__name__}"
            )
        if self.legality_result.legality_status not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES:
            raise InvalidActionLegalityServiceInterfaceResultError(
                "RT-001E skeleton only permits deferred/unknown legality results; "
                f"got legality_status={self.legality_result.legality_status!r}"
            )
        if self.dependency_manifest is not None and not isinstance(
            self.dependency_manifest,
            ActionLegalityServiceInterfaceDependencyManifest,
        ):
            raise InvalidActionLegalityServiceInterfaceResultError(
                f"dependency_manifest must be an "
                f"ActionLegalityServiceInterfaceDependencyManifest, "
                f"got {type(self.dependency_manifest).__name__}"
            )
        if not isinstance(
            self.authority_flags,
            ActionLegalityServiceInterfaceAuthorityFlags,
        ):
            raise InvalidActionLegalityServiceInterfaceResultError(
                f"authority_flags must be an "
                f"ActionLegalityServiceInterfaceAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidActionLegalityServiceInterfaceResultError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityServiceInterfaceResultError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "interface_status": self.interface_status,
            "legality_result": self.legality_result.to_dict(),
            "dependency_manifest": (
                self.dependency_manifest.to_dict()
                if self.dependency_manifest is not None else None
            ),
            "authority_flags": self.authority_flags.to_dict(),
            "non_authority_note": self.non_authority_note,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityServiceInterfaceContractSummary:
    """Describes the contract surface without executing anything."""

    summary_id: str
    supported_stages: tuple[str, ...] = ()
    supported_dependency_kinds: tuple[str, ...] = ()
    supported_result_statuses: tuple[str, ...] = ()
    supported_owner_routes: tuple[str, ...] = ()
    non_authority_note: str = ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.summary_id, "summary_id",
            InvalidActionLegalityServiceInterfaceContractSummaryError,
        )
        object.__setattr__(
            self, "supported_stages",
            _safe_str_tuple(
                self.supported_stages, "supported_stages",
                InvalidActionLegalityServiceInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_dependency_kinds",
            _safe_str_tuple(
                self.supported_dependency_kinds, "supported_dependency_kinds",
                InvalidActionLegalityServiceInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_result_statuses",
            _safe_str_tuple(
                self.supported_result_statuses, "supported_result_statuses",
                InvalidActionLegalityServiceInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_owner_routes",
            _safe_str_tuple(
                self.supported_owner_routes, "supported_owner_routes",
                InvalidActionLegalityServiceInterfaceContractSummaryError,
            ),
        )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidActionLegalityServiceInterfaceContractSummaryError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityServiceInterfaceContractSummaryError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "supported_stages": list(self.supported_stages),
            "supported_dependency_kinds": list(
                self.supported_dependency_kinds,
            ),
            "supported_result_statuses": list(
                self.supported_result_statuses,
            ),
            "supported_owner_routes": list(self.supported_owner_routes),
            "non_authority_note": self.non_authority_note,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_action_legality_service_interface_authority_flags() -> (
    ActionLegalityServiceInterfaceAuthorityFlags
):
    return ActionLegalityServiceInterfaceAuthorityFlags()


def create_action_legality_service_interface_dependency_manifest(
    *,
    manifest_id: str,
    dependency_refs: Sequence[ActionLegalityDependencyReference] | None = None,
    required_owner_routes: Sequence[str] | None = None,
    unavailable_owner_routes: Sequence[str] | None = None,
    deferred_reason: str = "skeleton_interface_only",
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityServiceInterfaceDependencyManifest:
    return ActionLegalityServiceInterfaceDependencyManifest(
        manifest_id=manifest_id,
        dependency_refs=dependency_refs,
        required_owner_routes=required_owner_routes,
        unavailable_owner_routes=unavailable_owner_routes,
        deferred_reason=deferred_reason,
        metadata=metadata,
    )


def create_action_legality_service_interface_request(
    *,
    request_id: str,
    legality_request: ActionLegalityRequest,
    gate_integration_result_ref: ActionLegalityReference | None = None,
    gate_input_refs: ActionLegalityGateInputRefs | None = None,
    dependency_manifest: ActionLegalityServiceInterfaceDependencyManifest | None = None,
    requested_stage: str = "request_received",
    authority_flags: ActionLegalityServiceInterfaceAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityServiceInterfaceRequest:
    return ActionLegalityServiceInterfaceRequest(
        request_id=request_id,
        legality_request=legality_request,
        gate_integration_result_ref=gate_integration_result_ref,
        gate_input_refs=gate_input_refs,
        dependency_manifest=dependency_manifest,
        requested_stage=requested_stage,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ActionLegalityServiceInterfaceAuthorityFlags()
        ),
        metadata=metadata,
    )


def create_action_legality_service_interface_result(
    *,
    result_id: str,
    request_id: str,
    interface_status: str,
    legality_result: ActionLegalityResult,
    dependency_manifest: ActionLegalityServiceInterfaceDependencyManifest | None = None,
    authority_flags: ActionLegalityServiceInterfaceAuthorityFlags | None = None,
    non_authority_note: str = ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityServiceInterfaceResult:
    return ActionLegalityServiceInterfaceResult(
        result_id=result_id,
        request_id=request_id,
        interface_status=interface_status,
        legality_result=legality_result,
        dependency_manifest=dependency_manifest,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ActionLegalityServiceInterfaceAuthorityFlags()
        ),
        non_authority_note=non_authority_note,
        metadata=metadata,
    )


def create_action_legality_service_interface_contract_summary(
    *,
    summary_id: str,
    supported_stages: Sequence[str] | None = None,
    supported_dependency_kinds: Sequence[str] | None = None,
    supported_result_statuses: Sequence[str] | None = None,
    supported_owner_routes: Sequence[str] | None = None,
    non_authority_note: str = ACTION_LEGALITY_SERVICE_INTERFACE_NON_AUTHORITY_NOTE,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityServiceInterfaceContractSummary:
    return ActionLegalityServiceInterfaceContractSummary(
        summary_id=summary_id,
        supported_stages=supported_stages,
        supported_dependency_kinds=supported_dependency_kinds,
        supported_result_statuses=supported_result_statuses,
        supported_owner_routes=supported_owner_routes,
        non_authority_note=non_authority_note,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Builder functions
# ---------------------------------------------------------------------------


def build_action_legality_service_interface_dependency_manifest(
    *,
    manifest_id: str,
    dependency_refs: Sequence[ActionLegalityDependencyReference] | None = None,
    owner_routes: Sequence[str] | None = None,
) -> ActionLegalityServiceInterfaceDependencyManifest:
    """Build a dependency manifest. All owner routes are treated as
    unavailable in the skeleton — no owner services are called."""
    return create_action_legality_service_interface_dependency_manifest(
        manifest_id=manifest_id,
        dependency_refs=dependency_refs,
        required_owner_routes=owner_routes,
        unavailable_owner_routes=owner_routes,
        deferred_reason="skeleton_interface_only",
    )


def build_deferred_action_legality_service_interface_result(
    *,
    result_id: str,
    request_id: str,
    dependency_manifest: ActionLegalityServiceInterfaceDependencyManifest | None = None,
) -> ActionLegalityServiceInterfaceResult:
    """Produce a service interface result with status 'deferred'. Never
    returns 'legal'. Uses safe player-visible message."""
    backend_detail = make_action_legality_backend_detail(
        detail_id=f"{result_id}_detail",
        blocker_class="runtime_owner_handoff",
        owner_route="action_legality_service_interface",
        resolution_path_summary=(
            "Service interface skeleton defers to future owner services."
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
    legality_result = make_action_legality_result(
        result_id=f"{result_id}_legality",
        request_id=request_id,
        legality_status="deferred",
        blockers=[blocker],
        visibility_envelope=envelope,
        authority_flags=ActionLegalityAuthorityFlags(),
    )
    return create_action_legality_service_interface_result(
        result_id=result_id,
        request_id=request_id,
        interface_status="deferred",
        legality_result=legality_result,
        dependency_manifest=dependency_manifest,
    )


def build_unknown_action_legality_service_interface_result(
    *,
    result_id: str,
    request_id: str,
    dependency_manifest: ActionLegalityServiceInterfaceDependencyManifest | None = None,
) -> ActionLegalityServiceInterfaceResult:
    """Produce a service interface result with status 'unknown'. Never
    returns 'legal'. Uses safe player-visible message."""
    backend_detail = make_action_legality_backend_detail(
        detail_id=f"{result_id}_detail",
        blocker_class="runtime_owner_handoff",
        owner_route="action_legality_service_interface",
        resolution_path_summary=(
            "Service interface skeleton cannot classify this request."
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
    legality_result = make_action_legality_result(
        result_id=f"{result_id}_legality",
        request_id=request_id,
        legality_status="unknown",
        blockers=[blocker],
        visibility_envelope=envelope,
        authority_flags=ActionLegalityAuthorityFlags(),
    )
    return create_action_legality_service_interface_result(
        result_id=result_id,
        request_id=request_id,
        interface_status="unknown",
        legality_result=legality_result,
        dependency_manifest=dependency_manifest,
    )


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------


def serialize_action_legality_service_interface_result(
    result: ActionLegalityServiceInterfaceResult,
) -> dict[str, Any]:
    """Full backend serializer. Deterministic, JSON-safe."""
    return result.to_dict()


def serialize_action_legality_service_interface_result_visible(
    result: ActionLegalityServiceInterfaceResult,
) -> dict[str, Any]:
    """Player-visible serializer. Excludes backend detail, dependency
    internals, owner route internals, state refs, trace refs, metadata,
    hidden information details, doctrine/schema/source-local refs, and
    module names."""
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
        "interface_status": result.interface_status,
        "legality_status": legality_result.legality_status,
        "player_visible_message": player_visible_message,
        "visible_blocker_messages": visible_blocker_messages,
        "non_authority_note": result.non_authority_note,
    }


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_action_legality_service_interface_authority_flags(
    obj: Any,
) -> bool:
    if not isinstance(obj, ActionLegalityServiceInterfaceAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True


def validate_action_legality_service_interface_dependency_manifest(
    obj: Any,
) -> bool:
    if not isinstance(obj, ActionLegalityServiceInterfaceDependencyManifest):
        return False
    if not isinstance(obj.manifest_id, str) or not obj.manifest_id:
        return False
    for dep in obj.dependency_refs:
        if not isinstance(dep, ActionLegalityDependencyReference):
            return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_service_interface_request(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityServiceInterfaceRequest):
        return False
    if not isinstance(obj.request_id, str) or not obj.request_id:
        return False
    if not isinstance(obj.legality_request, ActionLegalityRequest):
        return False
    if obj.requested_stage not in ACTION_LEGALITY_SERVICE_INTERFACE_STAGES:
        return False
    if not isinstance(
        obj.authority_flags,
        ActionLegalityServiceInterfaceAuthorityFlags,
    ):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_service_interface_result(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityServiceInterfaceResult):
        return False
    if not isinstance(obj.result_id, str) or not obj.result_id:
        return False
    if not isinstance(obj.request_id, str) or not obj.request_id:
        return False
    if obj.interface_status not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES:
        return False
    if not isinstance(obj.legality_result, ActionLegalityResult):
        return False
    if obj.legality_result.legality_status not in ACTION_LEGALITY_SERVICE_INTERFACE_RESULT_STATUSES:
        return False
    if not isinstance(
        obj.authority_flags,
        ActionLegalityServiceInterfaceAuthorityFlags,
    ):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_service_interface_contract_summary(
    obj: Any,
) -> bool:
    if not isinstance(obj, ActionLegalityServiceInterfaceContractSummary):
        return False
    if not isinstance(obj.summary_id, str) or not obj.summary_id:
        return False
    return isinstance(obj.metadata, Mapping)
