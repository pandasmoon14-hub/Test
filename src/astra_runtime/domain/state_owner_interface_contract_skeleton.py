"""State owner interface contract skeleton — RT-001H.

RUNTIME-DOMAIN-RT-001H: defines a reference-only state owner interface contract
skeleton. It creates typed references, request/result envelopes, visibility
descriptors, dependency declarations, read-only authority flags, and
deterministic serializers for future state-owner and dependency-owner
interfaces.

This module is a skeleton only: no state owner service behavior, no state reads,
no raw state access, no state projection materialization, no state mutation, no
action legality evaluation, no command execution, no event append or event
commitment, no persistence or replay writes, no RNG/table/oracle execution, no
resource/consequence math execution, no combat/ability/skill/effect resolution,
no model calls, no prompt rendering, no narration generation, no live-play or
UI behavior, no conversion, no sourcebook inclusion, and no canon promotion.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


__all__ = [
    # Constants
    "STATE_OWNER_INTERFACE_FAMILIES",
    "STATE_OWNER_DEPENDENCY_OWNER_FAMILIES",
    "STATE_OWNER_INTERFACE_REQUEST_STATUSES",
    "STATE_OWNER_INTERFACE_RESULT_STATUSES",
    "STATE_OWNER_VISIBILITY_TIERS",
    "STATE_OWNER_PROJECTION_KINDS",
    "STATE_OWNER_REFERENCE_KINDS",
    "STATE_OWNER_DENIAL_REASONS",
    "STATE_OWNER_NON_AUTHORITY_NOTE",
    # Error hierarchy
    "StateOwnerInterfaceContractSkeletonError",
    "InvalidStateOwnerInterfaceAuthorityFlagsError",
    "InvalidStateOwnerInterfaceReferenceError",
    "InvalidStateVisibilityDescriptorError",
    "InvalidStateProjectionRequestReferenceError",
    "InvalidStateOwnerDependencyDeclarationError",
    "InvalidStateOwnerInterfaceRequestError",
    "InvalidStateOwnerInterfaceResultError",
    "InvalidStateOwnerInterfaceContractSummaryError",
    # Dataclasses
    "StateOwnerInterfaceAuthorityFlags",
    "StateOwnerInterfaceReference",
    "StateVisibilityDescriptor",
    "StateProjectionRequestReference",
    "StateOwnerDependencyDeclaration",
    "StateOwnerInterfaceRequest",
    "StateOwnerInterfaceResult",
    "StateOwnerInterfaceContractSummary",
    # Factory functions
    "create_state_owner_interface_authority_flags",
    "create_state_owner_interface_reference",
    "create_state_visibility_descriptor",
    "create_state_projection_request_reference",
    "create_state_owner_dependency_declaration",
    "create_state_owner_interface_request",
    "create_state_owner_interface_result",
    "create_state_owner_interface_contract_summary",
    # Builder functions
    "build_state_owner_dependency_manifest",
    "build_unavailable_state_owner_interface_result",
    "build_deferred_state_owner_interface_result",
    "build_unknown_state_owner_interface_result",
    # Serializers
    "serialize_state_owner_interface_result",
    "serialize_state_owner_interface_result_visible",
    # Validators
    "validate_state_owner_interface_authority_flags",
    "validate_state_owner_interface_reference",
    "validate_state_visibility_descriptor",
    "validate_state_projection_request_reference",
    "validate_state_owner_dependency_declaration",
    "validate_state_owner_interface_request",
    "validate_state_owner_interface_result",
    "validate_state_owner_interface_contract_summary",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STATE_OWNER_INTERFACE_FAMILIES = frozenset({
    "actor_identity_owner",
    "actor_capability_owner",
    "scene_location_owner",
    "target_reachability_owner",
    "object_interactable_owner",
    "hazard_environment_owner",
    "inventory_custody_owner",
    "resource_pool_owner",
    "condition_status_owner",
    "faction_social_owner",
    "mission_discovery_owner",
    "hidden_information_visibility_owner",
    "state_projection_owner",
    "transaction_preview_owner",
    "event_commitment_owner",
    "persistence_replay_owner",
})

STATE_OWNER_DEPENDENCY_OWNER_FAMILIES = frozenset({
    "validation_owner",
    "resource_math_owner",
    "rng_table_oracle_owner",
    "state_delta_owner",
    "transaction_lifecycle_owner",
    "event_commitment_owner",
    "context_packet_owner",
    "persistence_replay_owner",
    "doctrine_schema_escalation_owner",
    "combat_ability_skill_effect_owner",
})

STATE_OWNER_INTERFACE_REQUEST_STATUSES = frozenset({
    "declared",
    "reference_only",
    "owner_unavailable",
    "deferred",
    "unknown",
})

STATE_OWNER_INTERFACE_RESULT_STATUSES = frozenset({
    "unavailable",
    "deferred",
    "unknown",
    "rejected",
    "quarantined",
    "escalated",
})

STATE_OWNER_VISIBILITY_TIERS = frozenset({
    "player_visible",
    "actor_visible",
    "backend_visible",
    "redacted_reference_only",
    "hidden",
})

STATE_OWNER_PROJECTION_KINDS = frozenset({
    "actor_scoped",
    "scene_scoped",
    "inventory_asset",
    "hidden_info_redacted",
    "resource_pool_reference",
    "condition_status_reference",
    "faction_social_reference",
    "mission_discovery_reference",
    "transaction_preview_reference",
    "persistence_replay_reference",
    "unavailable_projection",
})

STATE_OWNER_REFERENCE_KINDS = frozenset({
    "state_record_ref",
    "state_snapshot_ref",
    "state_projection_request_ref",
    "state_owner_interface_request_ref",
    "state_owner_interface_result_ref",
    "dependency_declaration_ref",
    "visibility_descriptor_ref",
    "trace_ref",
    "runtime_ref",
})

STATE_OWNER_DENIAL_REASONS = frozenset({
    "owner_unavailable",
    "owner_not_implemented",
    "reference_only_skeleton",
    "insufficient_visibility",
    "hidden_information_requires_routing",
    "dependency_unavailable",
    "mutation_authority_denied",
    "state_read_authority_denied",
    "projection_materialization_denied",
    "source_local_donor_specific",
    "doctrine_gap",
    "schema_gap",
})

STATE_OWNER_NON_AUTHORITY_NOTE = (
    "This state owner interface contract is skeleton-only and authorizes no "
    "state owner service behavior, no state reads, no raw state access, no "
    "state projection materialization, no state mutation, no action legality "
    "evaluation, no command execution, no event commitment, no persistence or "
    "replay writes, no RNG/table/oracle execution, no resource math, no "
    "combat/ability/skill/effect resolution, no model calls, no prompt "
    "rendering, no narration generation, no live-play or UI behavior, no "
    "conversion, no sourcebook inclusion, and no canon promotion."
)


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------

class StateOwnerInterfaceContractSkeletonError(ValueError):
    """Base error for state owner interface contract skeleton operations."""


class InvalidStateOwnerInterfaceAuthorityFlagsError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when authority flags contain any non-False value."""


class InvalidStateOwnerInterfaceReferenceError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when a state owner interface reference fails validation."""


class InvalidStateVisibilityDescriptorError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when a state visibility descriptor fails validation."""


class InvalidStateProjectionRequestReferenceError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when a state projection request reference fails validation."""


class InvalidStateOwnerDependencyDeclarationError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when a state owner dependency declaration fails validation."""


class InvalidStateOwnerInterfaceRequestError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when a state owner interface request fails validation."""


class InvalidStateOwnerInterfaceResultError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when a state owner interface result fails validation."""


class InvalidStateOwnerInterfaceContractSummaryError(
    StateOwnerInterfaceContractSkeletonError,
):
    """Raised when a state owner interface contract summary fails validation."""


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


def _safe_str_tuple(
    value: Sequence[str] | None, name: str, error_cls: type[Exception],
) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)):
        raise error_cls(f"{name} must not be a bare string")
    if not isinstance(value, Sequence):
        raise error_cls(f"{name} must be a sequence")
    result: list[str] = []
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item:
            raise error_cls(f"{name}[{i}] must be a non-empty string, got {item!r}")
        result.append(item)
    return tuple(result)


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
class StateOwnerInterfaceAuthorityFlags:
    """All authority flags must be false-only. Any non-False value raises
    during construction."""

    state_owner_service_authorized: bool = False
    state_read_authorized: bool = False
    raw_state_access_authorized: bool = False
    state_projection_materialization_authorized: bool = False
    state_mutation_authorized: bool = False
    event_append_authorized: bool = False
    event_commitment_authorized: bool = False
    persistence_write_authorized: bool = False
    replay_write_authorized: bool = False
    rng_execution_authorized: bool = False
    table_oracle_execution_authorized: bool = False
    resource_math_execution_authorized: bool = False
    affordability_execution_authorized: bool = False
    reservation_authorized: bool = False
    settlement_authorized: bool = False
    consequence_application_authorized: bool = False
    action_legality_evaluation_authorized: bool = False
    command_execution_authorized: bool = False
    combat_resolution_authorized: bool = False
    ability_resolution_authorized: bool = False
    skill_resolution_authorized: bool = False
    effect_resolution_authorized: bool = False
    context_packet_compilation_authorized: bool = False
    model_call_authorized: bool = False
    prompt_rendering_authorized: bool = False
    narration_generation_authorized: bool = False
    live_play_authorized: bool = False
    ui_authorized: bool = False
    conversion_authorized: bool = False
    sourcebook_inclusion_authorized: bool = False
    canon_promotion_authorized: bool = False

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if value is not False:
                raise InvalidStateOwnerInterfaceAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in "
                    f"RT-001H skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class StateOwnerInterfaceReference:
    """Typed reference to a state owner domain object. Reference-only: does not
    resolve anything and carries no raw state."""

    reference_id: str
    reference_kind: str
    owner_family: str
    source_scope: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.reference_id, "reference_id",
            InvalidStateOwnerInterfaceReferenceError,
        )
        _validate_non_empty_str(
            self.reference_kind, "reference_kind",
            InvalidStateOwnerInterfaceReferenceError,
        )
        if self.reference_kind not in STATE_OWNER_REFERENCE_KINDS:
            raise InvalidStateOwnerInterfaceReferenceError(
                f"reference_kind must be one of {sorted(STATE_OWNER_REFERENCE_KINDS)}, "
                f"got {self.reference_kind!r}"
            )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidStateOwnerInterfaceReferenceError,
        )
        if self.owner_family not in STATE_OWNER_INTERFACE_FAMILIES:
            raise InvalidStateOwnerInterfaceReferenceError(
                f"owner_family must be one of {sorted(STATE_OWNER_INTERFACE_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidStateOwnerInterfaceReferenceError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidStateOwnerInterfaceReferenceError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "reference_id": self.reference_id,
            "reference_kind": self.reference_kind,
            "owner_family": self.owner_family,
            "source_scope": self.source_scope,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class StateVisibilityDescriptor:
    """Visibility contract for a state owner mediated projection or result.
    Must not carry hidden facts or backend-only data intended for visible
    output."""

    visibility_id: str
    visibility_tier: str
    hidden_information_policy: str = "generic_safe_message"
    player_visible_allowed: bool = False
    actor_visible_allowed: bool = False
    backend_visible_allowed: bool = False
    redaction_required: bool = True
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.visibility_id, "visibility_id",
            InvalidStateVisibilityDescriptorError,
        )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidStateVisibilityDescriptorError,
        )
        if self.visibility_tier not in STATE_OWNER_VISIBILITY_TIERS:
            raise InvalidStateVisibilityDescriptorError(
                f"visibility_tier must be one of {sorted(STATE_OWNER_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.hidden_information_policy, "hidden_information_policy",
            InvalidStateVisibilityDescriptorError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidStateVisibilityDescriptorError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "visibility_id": self.visibility_id,
            "visibility_tier": self.visibility_tier,
            "hidden_information_policy": self.hidden_information_policy,
            "player_visible_allowed": self.player_visible_allowed,
            "actor_visible_allowed": self.actor_visible_allowed,
            "backend_visible_allowed": self.backend_visible_allowed,
            "redaction_required": self.redaction_required,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class StateProjectionRequestReference:
    """Reference-only request for a state projection. Does not materialize the
    projection and carries no projection payload data."""

    projection_request_id: str
    projection_kind: str
    requesting_owner_family: str
    target_owner_family: str
    subject_ref: StateOwnerInterfaceReference
    visibility_descriptor: StateVisibilityDescriptor
    dependency_refs: tuple[StateOwnerInterfaceReference, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.projection_request_id, "projection_request_id",
            InvalidStateProjectionRequestReferenceError,
        )
        _validate_non_empty_str(
            self.projection_kind, "projection_kind",
            InvalidStateProjectionRequestReferenceError,
        )
        if self.projection_kind not in STATE_OWNER_PROJECTION_KINDS:
            raise InvalidStateProjectionRequestReferenceError(
                f"projection_kind must be one of {sorted(STATE_OWNER_PROJECTION_KINDS)}, "
                f"got {self.projection_kind!r}"
            )
        for family_name, label in (
            (self.requesting_owner_family, "requesting_owner_family"),
            (self.target_owner_family, "target_owner_family"),
        ):
            _validate_non_empty_str(
                family_name, label,
                InvalidStateProjectionRequestReferenceError,
            )
            if family_name not in STATE_OWNER_INTERFACE_FAMILIES:
                raise InvalidStateProjectionRequestReferenceError(
                    f"{label} must be one of {sorted(STATE_OWNER_INTERFACE_FAMILIES)}, "
                    f"got {family_name!r}"
                )
        if not isinstance(self.subject_ref, StateOwnerInterfaceReference):
            raise InvalidStateProjectionRequestReferenceError(
                f"subject_ref must be a StateOwnerInterfaceReference, "
                f"got {type(self.subject_ref).__name__}"
            )
        if not isinstance(self.visibility_descriptor, StateVisibilityDescriptor):
            raise InvalidStateProjectionRequestReferenceError(
                f"visibility_descriptor must be a StateVisibilityDescriptor, "
                f"got {type(self.visibility_descriptor).__name__}"
            )
        object.__setattr__(
            self, "dependency_refs",
            _safe_obj_tuple(
                self.dependency_refs, "dependency_refs",
                InvalidStateProjectionRequestReferenceError,
                StateOwnerInterfaceReference,
            ),
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidStateProjectionRequestReferenceError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_request_id": self.projection_request_id,
            "projection_kind": self.projection_kind,
            "requesting_owner_family": self.requesting_owner_family,
            "target_owner_family": self.target_owner_family,
            "subject_ref": self.subject_ref.to_dict(),
            "visibility_descriptor": self.visibility_descriptor.to_dict(),
            "dependency_refs": [r.to_dict() for r in self.dependency_refs],
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class StateOwnerDependencyDeclaration:
    """Reference-only declaration of a dependency on a downstream owner
    service. Does not call the owner service."""

    dependency_id: str
    dependency_owner_family: str
    dependency_reason: str
    required_reference_kinds: tuple[str, ...] = ()
    unavailable_reason: str = "owner_not_implemented"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.dependency_id, "dependency_id",
            InvalidStateOwnerDependencyDeclarationError,
        )
        _validate_non_empty_str(
            self.dependency_owner_family, "dependency_owner_family",
            InvalidStateOwnerDependencyDeclarationError,
        )
        if self.dependency_owner_family not in STATE_OWNER_DEPENDENCY_OWNER_FAMILIES:
            raise InvalidStateOwnerDependencyDeclarationError(
                f"dependency_owner_family must be one of "
                f"{sorted(STATE_OWNER_DEPENDENCY_OWNER_FAMILIES)}, "
                f"got {self.dependency_owner_family!r}"
            )
        _validate_non_empty_str(
            self.dependency_reason, "dependency_reason",
            InvalidStateOwnerDependencyDeclarationError,
        )
        object.__setattr__(
            self, "required_reference_kinds",
            _safe_str_tuple(
                self.required_reference_kinds, "required_reference_kinds",
                InvalidStateOwnerDependencyDeclarationError,
            ),
        )
        for kind in self.required_reference_kinds:
            if kind not in STATE_OWNER_REFERENCE_KINDS:
                raise InvalidStateOwnerDependencyDeclarationError(
                    f"required_reference_kinds value {kind!r} must be one of "
                    f"{sorted(STATE_OWNER_REFERENCE_KINDS)}"
                )
        _validate_non_empty_str(
            self.unavailable_reason, "unavailable_reason",
            InvalidStateOwnerDependencyDeclarationError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidStateOwnerDependencyDeclarationError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dependency_id": self.dependency_id,
            "dependency_owner_family": self.dependency_owner_family,
            "dependency_reason": self.dependency_reason,
            "required_reference_kinds": list(self.required_reference_kinds),
            "unavailable_reason": self.unavailable_reason,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class StateOwnerInterfaceRequest:
    """Request envelope for a state owner interface. Reference-only: does not
    read state or execute owner behavior."""

    request_id: str
    requesting_surface: str
    owner_family: str
    request_status: str
    subject_ref: StateOwnerInterfaceReference
    projection_request_ref: StateProjectionRequestReference | None = None
    visibility_descriptor: StateVisibilityDescriptor | None = None
    dependency_declarations: tuple[StateOwnerDependencyDeclaration, ...] = ()
    authority_flags: StateOwnerInterfaceAuthorityFlags = field(
        default_factory=StateOwnerInterfaceAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidStateOwnerInterfaceRequestError,
        )
        _validate_non_empty_str(
            self.requesting_surface, "requesting_surface",
            InvalidStateOwnerInterfaceRequestError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidStateOwnerInterfaceRequestError,
        )
        if self.owner_family not in STATE_OWNER_INTERFACE_FAMILIES:
            raise InvalidStateOwnerInterfaceRequestError(
                f"owner_family must be one of {sorted(STATE_OWNER_INTERFACE_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.request_status, "request_status",
            InvalidStateOwnerInterfaceRequestError,
        )
        if self.request_status not in STATE_OWNER_INTERFACE_REQUEST_STATUSES:
            raise InvalidStateOwnerInterfaceRequestError(
                f"request_status must be one of {sorted(STATE_OWNER_INTERFACE_REQUEST_STATUSES)}, "
                f"got {self.request_status!r}"
            )
        if not isinstance(self.subject_ref, StateOwnerInterfaceReference):
            raise InvalidStateOwnerInterfaceRequestError(
                f"subject_ref must be a StateOwnerInterfaceReference, "
                f"got {type(self.subject_ref).__name__}"
            )
        if self.projection_request_ref is not None and not isinstance(
            self.projection_request_ref, StateProjectionRequestReference,
        ):
            raise InvalidStateOwnerInterfaceRequestError(
                f"projection_request_ref must be a StateProjectionRequestReference, "
                f"got {type(self.projection_request_ref).__name__}"
            )
        if self.visibility_descriptor is not None and not isinstance(
            self.visibility_descriptor, StateVisibilityDescriptor,
        ):
            raise InvalidStateOwnerInterfaceRequestError(
                f"visibility_descriptor must be a StateVisibilityDescriptor, "
                f"got {type(self.visibility_descriptor).__name__}"
            )
        object.__setattr__(
            self, "dependency_declarations",
            _safe_obj_tuple(
                self.dependency_declarations, "dependency_declarations",
                InvalidStateOwnerInterfaceRequestError,
                StateOwnerDependencyDeclaration,
            ),
        )
        if not isinstance(self.authority_flags, StateOwnerInterfaceAuthorityFlags):
            raise InvalidStateOwnerInterfaceRequestError(
                f"authority_flags must be a StateOwnerInterfaceAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidStateOwnerInterfaceRequestError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "requesting_surface": self.requesting_surface,
            "owner_family": self.owner_family,
            "request_status": self.request_status,
            "subject_ref": self.subject_ref.to_dict(),
            "projection_request_ref": (
                self.projection_request_ref.to_dict()
                if self.projection_request_ref is not None else None
            ),
            "visibility_descriptor": (
                self.visibility_descriptor.to_dict()
                if self.visibility_descriptor is not None else None
            ),
            "dependency_declarations": [
                d.to_dict() for d in self.dependency_declarations
            ],
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class StateOwnerInterfaceResult:
    """Result envelope for a state owner interface. Contains no actual state
    data, projection payloads, hidden facts, committed deltas, or resolved
    legality decisions."""

    result_id: str
    request_id: str
    owner_family: str
    result_status: str
    subject_ref: StateOwnerInterfaceReference
    projection_request_ref: StateProjectionRequestReference | None = None
    visibility_descriptor: StateVisibilityDescriptor | None = None
    dependency_declarations: tuple[StateOwnerDependencyDeclaration, ...] = ()
    non_authority_note: str = STATE_OWNER_NON_AUTHORITY_NOTE
    authority_flags: StateOwnerInterfaceAuthorityFlags = field(
        default_factory=StateOwnerInterfaceAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.result_id, "result_id",
            InvalidStateOwnerInterfaceResultError,
        )
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidStateOwnerInterfaceResultError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidStateOwnerInterfaceResultError,
        )
        if self.owner_family not in STATE_OWNER_INTERFACE_FAMILIES:
            raise InvalidStateOwnerInterfaceResultError(
                f"owner_family must be one of {sorted(STATE_OWNER_INTERFACE_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.result_status, "result_status",
            InvalidStateOwnerInterfaceResultError,
        )
        if self.result_status not in STATE_OWNER_INTERFACE_RESULT_STATUSES:
            raise InvalidStateOwnerInterfaceResultError(
                f"result_status must be one of {sorted(STATE_OWNER_INTERFACE_RESULT_STATUSES)}, "
                f"got {self.result_status!r}"
            )
        if not isinstance(self.subject_ref, StateOwnerInterfaceReference):
            raise InvalidStateOwnerInterfaceResultError(
                f"subject_ref must be a StateOwnerInterfaceReference, "
                f"got {type(self.subject_ref).__name__}"
            )
        if self.projection_request_ref is not None and not isinstance(
            self.projection_request_ref, StateProjectionRequestReference,
        ):
            raise InvalidStateOwnerInterfaceResultError(
                f"projection_request_ref must be a StateProjectionRequestReference, "
                f"got {type(self.projection_request_ref).__name__}"
            )
        if self.visibility_descriptor is not None and not isinstance(
            self.visibility_descriptor, StateVisibilityDescriptor,
        ):
            raise InvalidStateOwnerInterfaceResultError(
                f"visibility_descriptor must be a StateVisibilityDescriptor, "
                f"got {type(self.visibility_descriptor).__name__}"
            )
        object.__setattr__(
            self, "dependency_declarations",
            _safe_obj_tuple(
                self.dependency_declarations, "dependency_declarations",
                InvalidStateOwnerInterfaceResultError,
                StateOwnerDependencyDeclaration,
            ),
        )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidStateOwnerInterfaceResultError,
        )
        if not isinstance(self.authority_flags, StateOwnerInterfaceAuthorityFlags):
            raise InvalidStateOwnerInterfaceResultError(
                f"authority_flags must be a StateOwnerInterfaceAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidStateOwnerInterfaceResultError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "owner_family": self.owner_family,
            "result_status": self.result_status,
            "subject_ref": self.subject_ref.to_dict(),
            "projection_request_ref": (
                self.projection_request_ref.to_dict()
                if self.projection_request_ref is not None else None
            ),
            "visibility_descriptor": (
                self.visibility_descriptor.to_dict()
                if self.visibility_descriptor is not None else None
            ),
            "dependency_declarations": [
                d.to_dict() for d in self.dependency_declarations
            ],
            "non_authority_note": self.non_authority_note,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class StateOwnerInterfaceContractSummary:
    """Summary of the state owner interface contract surface. No execution."""

    summary_id: str
    supported_owner_families: tuple[str, ...] = ()
    supported_dependency_owner_families: tuple[str, ...] = ()
    supported_request_statuses: tuple[str, ...] = ()
    supported_result_statuses: tuple[str, ...] = ()
    supported_visibility_tiers: tuple[str, ...] = ()
    supported_projection_kinds: tuple[str, ...] = ()
    non_authority_note: str = STATE_OWNER_NON_AUTHORITY_NOTE
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.summary_id, "summary_id",
            InvalidStateOwnerInterfaceContractSummaryError,
        )
        object.__setattr__(
            self, "supported_owner_families",
            _safe_str_tuple(
                self.supported_owner_families, "supported_owner_families",
                InvalidStateOwnerInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_dependency_owner_families",
            _safe_str_tuple(
                self.supported_dependency_owner_families,
                "supported_dependency_owner_families",
                InvalidStateOwnerInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_request_statuses",
            _safe_str_tuple(
                self.supported_request_statuses, "supported_request_statuses",
                InvalidStateOwnerInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_result_statuses",
            _safe_str_tuple(
                self.supported_result_statuses, "supported_result_statuses",
                InvalidStateOwnerInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_visibility_tiers",
            _safe_str_tuple(
                self.supported_visibility_tiers, "supported_visibility_tiers",
                InvalidStateOwnerInterfaceContractSummaryError,
            ),
        )
        object.__setattr__(
            self, "supported_projection_kinds",
            _safe_str_tuple(
                self.supported_projection_kinds, "supported_projection_kinds",
                InvalidStateOwnerInterfaceContractSummaryError,
            ),
        )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidStateOwnerInterfaceContractSummaryError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidStateOwnerInterfaceContractSummaryError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "supported_owner_families": list(self.supported_owner_families),
            "supported_dependency_owner_families": list(
                self.supported_dependency_owner_families,
            ),
            "supported_request_statuses": list(self.supported_request_statuses),
            "supported_result_statuses": list(self.supported_result_statuses),
            "supported_visibility_tiers": list(self.supported_visibility_tiers),
            "supported_projection_kinds": list(self.supported_projection_kinds),
            "non_authority_note": self.non_authority_note,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_state_owner_interface_authority_flags() -> StateOwnerInterfaceAuthorityFlags:
    return StateOwnerInterfaceAuthorityFlags()


def create_state_owner_interface_reference(
    *,
    reference_id: str,
    reference_kind: str,
    owner_family: str,
    source_scope: str,
    metadata: Mapping[str, Any] | None = None,
) -> StateOwnerInterfaceReference:
    return StateOwnerInterfaceReference(
        reference_id=reference_id,
        reference_kind=reference_kind,
        owner_family=owner_family,
        source_scope=source_scope,
        metadata=metadata,
    )


def create_state_visibility_descriptor(
    *,
    visibility_id: str,
    visibility_tier: str,
    hidden_information_policy: str = "generic_safe_message",
    player_visible_allowed: bool = False,
    actor_visible_allowed: bool = False,
    backend_visible_allowed: bool = False,
    redaction_required: bool = True,
    metadata: Mapping[str, Any] | None = None,
) -> StateVisibilityDescriptor:
    return StateVisibilityDescriptor(
        visibility_id=visibility_id,
        visibility_tier=visibility_tier,
        hidden_information_policy=hidden_information_policy,
        player_visible_allowed=player_visible_allowed,
        actor_visible_allowed=actor_visible_allowed,
        backend_visible_allowed=backend_visible_allowed,
        redaction_required=redaction_required,
        metadata=metadata,
    )


def create_state_projection_request_reference(
    *,
    projection_request_id: str,
    projection_kind: str,
    requesting_owner_family: str,
    target_owner_family: str,
    subject_ref: StateOwnerInterfaceReference,
    visibility_descriptor: StateVisibilityDescriptor,
    dependency_refs: Sequence[StateOwnerInterfaceReference] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateProjectionRequestReference:
    return StateProjectionRequestReference(
        projection_request_id=projection_request_id,
        projection_kind=projection_kind,
        requesting_owner_family=requesting_owner_family,
        target_owner_family=target_owner_family,
        subject_ref=subject_ref,
        visibility_descriptor=visibility_descriptor,
        dependency_refs=dependency_refs,
        metadata=metadata,
    )


def create_state_owner_dependency_declaration(
    *,
    dependency_id: str,
    dependency_owner_family: str,
    dependency_reason: str,
    required_reference_kinds: Sequence[str] | None = None,
    unavailable_reason: str = "owner_not_implemented",
    metadata: Mapping[str, Any] | None = None,
) -> StateOwnerDependencyDeclaration:
    return StateOwnerDependencyDeclaration(
        dependency_id=dependency_id,
        dependency_owner_family=dependency_owner_family,
        dependency_reason=dependency_reason,
        required_reference_kinds=required_reference_kinds,
        unavailable_reason=unavailable_reason,
        metadata=metadata,
    )


def create_state_owner_interface_request(
    *,
    request_id: str,
    requesting_surface: str,
    owner_family: str,
    request_status: str,
    subject_ref: StateOwnerInterfaceReference,
    projection_request_ref: StateProjectionRequestReference | None = None,
    visibility_descriptor: StateVisibilityDescriptor | None = None,
    dependency_declarations: Sequence[StateOwnerDependencyDeclaration] | None = None,
    authority_flags: StateOwnerInterfaceAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateOwnerInterfaceRequest:
    return StateOwnerInterfaceRequest(
        request_id=request_id,
        requesting_surface=requesting_surface,
        owner_family=owner_family,
        request_status=request_status,
        subject_ref=subject_ref,
        projection_request_ref=projection_request_ref,
        visibility_descriptor=visibility_descriptor,
        dependency_declarations=dependency_declarations,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else StateOwnerInterfaceAuthorityFlags()
        ),
        metadata=metadata,
    )


def create_state_owner_interface_result(
    *,
    result_id: str,
    request_id: str,
    owner_family: str,
    result_status: str,
    subject_ref: StateOwnerInterfaceReference,
    projection_request_ref: StateProjectionRequestReference | None = None,
    visibility_descriptor: StateVisibilityDescriptor | None = None,
    dependency_declarations: Sequence[StateOwnerDependencyDeclaration] | None = None,
    non_authority_note: str = STATE_OWNER_NON_AUTHORITY_NOTE,
    authority_flags: StateOwnerInterfaceAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> StateOwnerInterfaceResult:
    return StateOwnerInterfaceResult(
        result_id=result_id,
        request_id=request_id,
        owner_family=owner_family,
        result_status=result_status,
        subject_ref=subject_ref,
        projection_request_ref=projection_request_ref,
        visibility_descriptor=visibility_descriptor,
        dependency_declarations=dependency_declarations,
        non_authority_note=non_authority_note,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else StateOwnerInterfaceAuthorityFlags()
        ),
        metadata=metadata,
    )


def create_state_owner_interface_contract_summary(
    *,
    summary_id: str,
    supported_owner_families: Sequence[str] | None = None,
    supported_dependency_owner_families: Sequence[str] | None = None,
    supported_request_statuses: Sequence[str] | None = None,
    supported_result_statuses: Sequence[str] | None = None,
    supported_visibility_tiers: Sequence[str] | None = None,
    supported_projection_kinds: Sequence[str] | None = None,
    non_authority_note: str = STATE_OWNER_NON_AUTHORITY_NOTE,
    metadata: Mapping[str, Any] | None = None,
) -> StateOwnerInterfaceContractSummary:
    return StateOwnerInterfaceContractSummary(
        summary_id=summary_id,
        supported_owner_families=supported_owner_families,
        supported_dependency_owner_families=supported_dependency_owner_families,
        supported_request_statuses=supported_request_statuses,
        supported_result_statuses=supported_result_statuses,
        supported_visibility_tiers=supported_visibility_tiers,
        supported_projection_kinds=supported_projection_kinds,
        non_authority_note=non_authority_note,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Builder functions
# ---------------------------------------------------------------------------


def build_state_owner_dependency_manifest(
    *,
    manifest_id: str,
    dependency_owner_families: Sequence[str] | None = None,
    dependency_reason: str = "owner_not_implemented",
) -> tuple[StateOwnerDependencyDeclaration, ...]:
    """Build a tuple of dependency declarations. No owner services are called."""
    families = dependency_owner_families or sorted(STATE_OWNER_DEPENDENCY_OWNER_FAMILIES)
    return tuple(
        create_state_owner_dependency_declaration(
            dependency_id=f"{manifest_id}_dep_{family}",
            dependency_owner_family=family,
            dependency_reason=dependency_reason,
            unavailable_reason="owner_not_implemented",
        )
        for family in families
    )


def build_unavailable_state_owner_interface_result(
    *,
    result_id: str,
    request_id: str,
    owner_family: str,
    subject_ref: StateOwnerInterfaceReference,
    dependency_declarations: Sequence[StateOwnerDependencyDeclaration] | None = None,
) -> StateOwnerInterfaceResult:
    """Produce a state owner interface result with status 'unavailable'."""
    return create_state_owner_interface_result(
        result_id=result_id,
        request_id=request_id,
        owner_family=owner_family,
        result_status="unavailable",
        subject_ref=subject_ref,
        dependency_declarations=dependency_declarations,
    )


def build_deferred_state_owner_interface_result(
    *,
    result_id: str,
    request_id: str,
    owner_family: str,
    subject_ref: StateOwnerInterfaceReference,
    dependency_declarations: Sequence[StateOwnerDependencyDeclaration] | None = None,
) -> StateOwnerInterfaceResult:
    """Produce a state owner interface result with status 'deferred'."""
    return create_state_owner_interface_result(
        result_id=result_id,
        request_id=request_id,
        owner_family=owner_family,
        result_status="deferred",
        subject_ref=subject_ref,
        dependency_declarations=dependency_declarations,
    )


def build_unknown_state_owner_interface_result(
    *,
    result_id: str,
    request_id: str,
    owner_family: str,
    subject_ref: StateOwnerInterfaceReference,
    dependency_declarations: Sequence[StateOwnerDependencyDeclaration] | None = None,
) -> StateOwnerInterfaceResult:
    """Produce a state owner interface result with status 'unknown'."""
    return create_state_owner_interface_result(
        result_id=result_id,
        request_id=request_id,
        owner_family=owner_family,
        result_status="unknown",
        subject_ref=subject_ref,
        dependency_declarations=dependency_declarations,
    )


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------


def serialize_state_owner_interface_result(
    result: StateOwnerInterfaceResult,
) -> dict[str, Any]:
    """Full backend serializer. Deterministic, JSON-safe."""
    return result.to_dict()


def serialize_state_owner_interface_result_visible(
    result: StateOwnerInterfaceResult,
) -> dict[str, Any]:
    """Visible serializer. Excludes backend/internal/hidden/projection/state
    payload fields, dependency internals, metadata, trace internals, and
    implementation details."""
    visible: dict[str, Any] = {
        "result_id": result.result_id,
        "request_id": result.request_id,
        "owner_family": result.owner_family,
        "result_status": result.result_status,
        "non_authority_note": result.non_authority_note,
    }
    if result.visibility_descriptor is not None:
        visible["visibility_tier"] = result.visibility_descriptor.visibility_tier
        visible["player_visible_allowed"] = (
            result.visibility_descriptor.player_visible_allowed
        )
        visible["redaction_required"] = result.visibility_descriptor.redaction_required
    else:
        visible["visibility_tier"] = None
        visible["player_visible_allowed"] = False
        visible["redaction_required"] = True
    return visible


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_state_owner_interface_authority_flags(
    obj: Any,
) -> bool:
    if not isinstance(obj, StateOwnerInterfaceAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True


def validate_state_owner_interface_reference(obj: Any) -> bool:
    if not isinstance(obj, StateOwnerInterfaceReference):
        return False
    if not isinstance(obj.reference_id, str) or not obj.reference_id:
        return False
    if obj.reference_kind not in STATE_OWNER_REFERENCE_KINDS:
        return False
    if obj.owner_family not in STATE_OWNER_INTERFACE_FAMILIES:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_state_visibility_descriptor(obj: Any) -> bool:
    if not isinstance(obj, StateVisibilityDescriptor):
        return False
    if not isinstance(obj.visibility_id, str) or not obj.visibility_id:
        return False
    if obj.visibility_tier not in STATE_OWNER_VISIBILITY_TIERS:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_state_projection_request_reference(obj: Any) -> bool:
    if not isinstance(obj, StateProjectionRequestReference):
        return False
    if not isinstance(obj.projection_request_id, str) or not obj.projection_request_id:
        return False
    if obj.projection_kind not in STATE_OWNER_PROJECTION_KINDS:
        return False
    if not isinstance(obj.subject_ref, StateOwnerInterfaceReference):
        return False
    if not isinstance(obj.visibility_descriptor, StateVisibilityDescriptor):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_state_owner_dependency_declaration(obj: Any) -> bool:
    if not isinstance(obj, StateOwnerDependencyDeclaration):
        return False
    if not isinstance(obj.dependency_id, str) or not obj.dependency_id:
        return False
    if obj.dependency_owner_family not in STATE_OWNER_DEPENDENCY_OWNER_FAMILIES:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_state_owner_interface_request(obj: Any) -> bool:
    if not isinstance(obj, StateOwnerInterfaceRequest):
        return False
    if not isinstance(obj.request_id, str) or not obj.request_id:
        return False
    if obj.owner_family not in STATE_OWNER_INTERFACE_FAMILIES:
        return False
    if obj.request_status not in STATE_OWNER_INTERFACE_REQUEST_STATUSES:
        return False
    if not isinstance(obj.subject_ref, StateOwnerInterfaceReference):
        return False
    if not isinstance(obj.authority_flags, StateOwnerInterfaceAuthorityFlags):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_state_owner_interface_result(obj: Any) -> bool:
    if not isinstance(obj, StateOwnerInterfaceResult):
        return False
    if not isinstance(obj.result_id, str) or not obj.result_id:
        return False
    if not isinstance(obj.request_id, str) or not obj.request_id:
        return False
    if obj.owner_family not in STATE_OWNER_INTERFACE_FAMILIES:
        return False
    if obj.result_status not in STATE_OWNER_INTERFACE_RESULT_STATUSES:
        return False
    if not isinstance(obj.subject_ref, StateOwnerInterfaceReference):
        return False
    if not isinstance(obj.authority_flags, StateOwnerInterfaceAuthorityFlags):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_state_owner_interface_contract_summary(obj: Any) -> bool:
    if not isinstance(obj, StateOwnerInterfaceContractSummary):
        return False
    if not isinstance(obj.summary_id, str) or not obj.summary_id:
        return False
    return isinstance(obj.metadata, Mapping)
