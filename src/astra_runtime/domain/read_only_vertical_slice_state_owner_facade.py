"""Read-only vertical slice state owner facade — RT-002A.

RUNTIME-DOMAIN-RT-002A: implements a narrow, read-only, owner-mediated facade for
the smallest vertical slice. It keeps backend truth inside owner-mediated
runtime structures and exposes only safe references and projections.

This module is intentionally narrow:
* read-only vertical-slice state owner facade only
* typed in-memory vertical-slice records
* owner-mediated references and safe projection descriptors
* validation helpers
* deterministic serializers
* hidden-fact reference containment

It does NOT implement:
* broad state owner service behavior
* general state store
* raw state access outside the narrow owned facade
* state mutation
* event append or event commitment
* persistence/replay writes
* action legality evaluation
* command execution
* transaction preview materialization
* state projection materialization
* RNG/table/oracle execution
* resource/consequence math execution
* combat/ability/skill/effect resolution
* model calls
* prompt rendering
* narration generation
* live-play behavior
* UI/client behavior
* conversion
* sourcebook inclusion
* canon promotion

The smallest vertical slice contains exactly:
* one scene
* one actor
* one NPC/target
* one object/lever
* one hazard clock
* one visible condition/injury
* one hidden fact reference
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.state_owner_interface_contract_skeleton import (
    STATE_OWNER_HIDDEN_INFORMATION_POLICIES,
    STATE_OWNER_INTERFACE_FAMILIES,
    STATE_OWNER_NON_AUTHORITY_NOTE,
    STATE_OWNER_VISIBILITY_TIERS,
    StateOwnerInterfaceReference,
    StateProjectionRequestReference,
    StateVisibilityDescriptor,
)


__all__ = [
    # Constants
    "VERTICAL_SLICE_OWNER_FAMILIES",
    "VERTICAL_SLICE_ENTITY_KINDS",
    "VERTICAL_SLICE_VISIBILITY_TIERS",
    "VERTICAL_SLICE_RECORD_STATUSES",
    "VERTICAL_SLICE_FACADE_RESULT_STATUSES",
    "VERTICAL_SLICE_NON_AUTHORITY_NOTE",
    # Error hierarchy
    "ReadOnlyVerticalSliceStateOwnerFacadeError",
    "InvalidVerticalSliceStateOwnerAuthorityFlagsError",
    "InvalidVerticalSliceStateRecordRefError",
    "InvalidVerticalSliceSceneRecordError",
    "InvalidVerticalSliceActorRecordError",
    "InvalidVerticalSliceNpcTargetRecordError",
    "InvalidVerticalSliceObjectLeverRecordError",
    "InvalidVerticalSliceHazardClockRecordError",
    "InvalidVerticalSliceVisibleConditionRecordError",
    "InvalidVerticalSliceHiddenFactReferenceError",
    "InvalidVerticalSliceReadOnlyStateBundleError",
    "InvalidVerticalSliceOwnerProjectionError",
    "InvalidVerticalSliceOwnerFacadeResultError",
    # Dataclasses
    "VerticalSliceStateOwnerAuthorityFlags",
    "VerticalSliceStateRecordRef",
    "VerticalSliceSceneRecord",
    "VerticalSliceActorRecord",
    "VerticalSliceNpcTargetRecord",
    "VerticalSliceObjectLeverRecord",
    "VerticalSliceHazardClockRecord",
    "VerticalSliceVisibleConditionRecord",
    "VerticalSliceHiddenFactReference",
    "VerticalSliceReadOnlyStateBundle",
    "VerticalSliceOwnerProjection",
    "VerticalSliceOwnerFacadeResult",
    # Factory functions
    "create_vertical_slice_state_owner_authority_flags",
    "create_vertical_slice_state_record_ref",
    "create_vertical_slice_scene_record",
    "create_vertical_slice_actor_record",
    "create_vertical_slice_npc_target_record",
    "create_vertical_slice_object_lever_record",
    "create_vertical_slice_hazard_clock_record",
    "create_vertical_slice_visible_condition_record",
    "create_vertical_slice_hidden_fact_reference",
    "create_vertical_slice_read_only_state_bundle",
    "create_vertical_slice_owner_projection",
    "create_vertical_slice_owner_facade_result",
    # Facade helpers
    "build_vertical_slice_reference_manifest",
    "get_vertical_slice_owner_reference",
    "get_vertical_slice_owner_projection",
    "serialize_vertical_slice_owner_facade_result",
    "serialize_vertical_slice_owner_facade_result_visible",
    # Validators
    "validate_vertical_slice_state_owner_authority_flags",
    "validate_vertical_slice_state_record_ref",
    "validate_vertical_slice_scene_record",
    "validate_vertical_slice_actor_record",
    "validate_vertical_slice_npc_target_record",
    "validate_vertical_slice_object_lever_record",
    "validate_vertical_slice_hazard_clock_record",
    "validate_vertical_slice_visible_condition_record",
    "validate_vertical_slice_hidden_fact_reference",
    "validate_vertical_slice_read_only_state_bundle",
    "validate_vertical_slice_owner_projection",
    "validate_vertical_slice_owner_facade_result",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VERTICAL_SLICE_OWNER_FAMILIES = frozenset({
    "actor_identity_owner",
    "scene_location_owner",
    "target_reachability_owner",
    "object_interactable_owner",
    "hazard_environment_owner",
    "condition_status_owner",
    "hidden_information_visibility_owner",
})

VERTICAL_SLICE_ENTITY_KINDS = frozenset({
    "scene",
    "actor",
    "npc_target",
    "object_lever",
    "hazard_clock",
    "visible_condition",
    "hidden_fact_reference",
})

VERTICAL_SLICE_VISIBILITY_TIERS = STATE_OWNER_VISIBILITY_TIERS

VERTICAL_SLICE_RECORD_STATUSES = frozenset({
    "active",
    "inactive",
    "unavailable",
    "redacted",
})

VERTICAL_SLICE_FACADE_RESULT_STATUSES = frozenset({
    "available_reference",
    "unavailable",
    "redacted",
    "deferred",
    "unknown",
})

_FORBIDDEN_VERTICAL_SLICE_METADATA_KEYS = frozenset({
    "hidden_fact",
    "hidden_facts",
    "secret",
    "secrets",
    "backend_only_fact",
    "backend_only_facts",
    "state_payload",
    "raw_state",
    "actual_state",
    "truth_payload",
})

VERTICAL_SLICE_NON_AUTHORITY_NOTE = (
    "This read-only vertical slice state owner facade is reference-only and "
    "authorizes no state owner service behavior, no raw state access, no state "
    "projection materialization, no state mutation, no action legality "
    "evaluation, no command execution, no transaction preview, no event append "
    "or commitment, no persistence or replay writes, no RNG/table/oracle "
    "execution, no resource or consequence math execution, no "
    "combat/ability/skill/effect resolution, no model calls, no prompt "
    "rendering, no narration generation, no live-play or UI behavior, no "
    "conversion, no sourcebook inclusion, and no canon promotion."
)


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------


class ReadOnlyVerticalSliceStateOwnerFacadeError(ValueError):
    """Base error for RT-002A read-only vertical slice facade operations."""


class InvalidVerticalSliceStateOwnerAuthorityFlagsError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when authority flags contain any non-False value."""


class InvalidVerticalSliceStateRecordRefError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice state record ref fails validation."""


class InvalidVerticalSliceSceneRecordError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice scene record fails validation."""


class InvalidVerticalSliceActorRecordError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice actor record fails validation."""


class InvalidVerticalSliceNpcTargetRecordError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice NPC/target record fails validation."""


class InvalidVerticalSliceObjectLeverRecordError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice object/lever record fails validation."""


class InvalidVerticalSliceHazardClockRecordError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice hazard clock record fails validation."""


class InvalidVerticalSliceVisibleConditionRecordError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice visible condition record fails validation."""


class InvalidVerticalSliceHiddenFactReferenceError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice hidden fact reference fails validation."""


class InvalidVerticalSliceReadOnlyStateBundleError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice read-only state bundle fails validation."""


class InvalidVerticalSliceOwnerProjectionError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice owner projection fails validation."""


class InvalidVerticalSliceOwnerFacadeResultError(
    ReadOnlyVerticalSliceStateOwnerFacadeError,
):
    """Raised when a vertical slice owner facade result fails validation."""


# ---------------------------------------------------------------------------
# Internal validation helpers
# ---------------------------------------------------------------------------


def _validate_non_empty_str(
    value: object, name: str, error_cls: type[Exception],
) -> str:
    if not isinstance(value, str) or not value:
        raise error_cls(f"{name} must be a non-empty string, got {value!r}")
    return value


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


def _safe_vertical_slice_metadata(
    metadata: Mapping[str, Any] | None, error_cls: type[Exception],
) -> Mapping[str, Any]:
    """JSON-safe metadata that also recursively rejects hidden/raw-state keys."""
    if metadata is not None:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            metadata, "metadata", error_cls,
        )
    return _safe_metadata(metadata, error_cls)


def _validate_no_forbidden_vertical_slice_metadata_keys(
    value: Any, path: str, error_cls: type[Exception],
) -> None:
    """Recursively reject metadata keys that could carry hidden/backend state."""
    if isinstance(value, (dict, Mapping)):
        for k, v in value.items():
            if not isinstance(k, str):
                raise error_cls(
                    f"metadata key at {path} must be a string, "
                    f"got {type(k).__name__}"
                )
            if k in _FORBIDDEN_VERTICAL_SLICE_METADATA_KEYS:
                raise error_cls(
                    f"metadata key {k!r} at {path} is forbidden: "
                    f"vertical slice records must not carry hidden or backend-only data"
                )
            _validate_no_forbidden_vertical_slice_metadata_keys(
                v, f"{path}.{k}", error_cls,
            )
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            _validate_no_forbidden_vertical_slice_metadata_keys(
                item, f"{path}[{i}]", error_cls,
            )


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
class VerticalSliceStateOwnerAuthorityFlags:
    """All authority flags must be false-only. Any non-False value raises during
    construction."""

    state_read_authorized: bool = False
    raw_state_access_authorized: bool = False
    state_mutation_authorized: bool = False
    state_projection_materialization_authorized: bool = False
    action_legality_evaluation_authorized: bool = False
    command_execution_authorized: bool = False
    transaction_preview_authorized: bool = False
    event_append_authorized: bool = False
    event_commitment_authorized: bool = False
    persistence_write_authorized: bool = False
    replay_write_authorized: bool = False
    rng_execution_authorized: bool = False
    resource_math_execution_authorized: bool = False
    model_call_authorized: bool = False
    narration_generation_authorized: bool = False
    live_play_authorized: bool = False
    ui_authorized: bool = False
    conversion_authorized: bool = False
    canon_promotion_authorized: bool = False

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if value is not False:
                raise InvalidVerticalSliceStateOwnerAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in "
                    f"RT-002A skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class VerticalSliceStateRecordRef:
    """Reference-only descriptor for a vertical slice state record. Carries no
    raw state payload."""

    reference_id: str
    entity_kind: str
    owner_family: str
    visibility_tier: str
    source_scope: str
    record_status: str = "active"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.reference_id, "reference_id",
            InvalidVerticalSliceStateRecordRefError,
        )
        _validate_non_empty_str(
            self.entity_kind, "entity_kind",
            InvalidVerticalSliceStateRecordRefError,
        )
        if self.entity_kind not in VERTICAL_SLICE_ENTITY_KINDS:
            raise InvalidVerticalSliceStateRecordRefError(
                f"entity_kind must be one of {sorted(VERTICAL_SLICE_ENTITY_KINDS)}, "
                f"got {self.entity_kind!r}"
            )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceStateRecordRefError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceStateRecordRefError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceStateRecordRefError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceStateRecordRefError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceStateRecordRefError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceStateRecordRefError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceStateRecordRefError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceStateRecordRefError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "reference_id": self.reference_id,
            "entity_kind": self.entity_kind,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceSceneRecord:
    """Scene identifier and safe visible labels only. No full world state. No
    hidden facts."""

    scene_id: str
    scene_label: str
    owner_family: str = "scene_location_owner"
    visibility_tier: str = "player_visible"
    source_scope: str
    record_status: str = "active"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.scene_id, "scene_id",
            InvalidVerticalSliceSceneRecordError,
        )
        _validate_non_empty_str(
            self.scene_label, "scene_label",
            InvalidVerticalSliceSceneRecordError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceSceneRecordError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceSceneRecordError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceSceneRecordError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceSceneRecordError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceSceneRecordError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceSceneRecordError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceSceneRecordError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceSceneRecordError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "scene_label": self.scene_label,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceActorRecord:
    """Actor identifier and safe reference fields only. No action legality
    result."""

    actor_id: str
    actor_label: str
    owner_family: str = "actor_identity_owner"
    visibility_tier: str = "player_visible"
    source_scope: str
    record_status: str = "active"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.actor_id, "actor_id",
            InvalidVerticalSliceActorRecordError,
        )
        _validate_non_empty_str(
            self.actor_label, "actor_label",
            InvalidVerticalSliceActorRecordError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceActorRecordError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceActorRecordError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceActorRecordError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceActorRecordError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceActorRecordError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceActorRecordError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceActorRecordError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceActorRecordError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor_id": self.actor_id,
            "actor_label": self.actor_label,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceNpcTargetRecord:
    """NPC/target identifier and safe reference fields only. No AI behavior. No
    combat behavior."""

    npc_target_id: str
    npc_target_label: str
    owner_family: str = "target_reachability_owner"
    visibility_tier: str = "player_visible"
    source_scope: str
    record_status: str = "active"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.npc_target_id, "npc_target_id",
            InvalidVerticalSliceNpcTargetRecordError,
        )
        _validate_non_empty_str(
            self.npc_target_label, "npc_target_label",
            InvalidVerticalSliceNpcTargetRecordError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceNpcTargetRecordError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceNpcTargetRecordError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceNpcTargetRecordError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceNpcTargetRecordError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceNpcTargetRecordError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceNpcTargetRecordError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceNpcTargetRecordError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceNpcTargetRecordError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "npc_target_id": self.npc_target_id,
            "npc_target_label": self.npc_target_label,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceObjectLeverRecord:
    """Object/lever identifier and safe reference fields only. No command
    execution behavior."""

    object_lever_id: str
    object_lever_label: str
    owner_family: str = "object_interactable_owner"
    visibility_tier: str = "player_visible"
    source_scope: str
    record_status: str = "active"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.object_lever_id, "object_lever_id",
            InvalidVerticalSliceObjectLeverRecordError,
        )
        _validate_non_empty_str(
            self.object_lever_label, "object_lever_label",
            InvalidVerticalSliceObjectLeverRecordError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceObjectLeverRecordError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceObjectLeverRecordError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceObjectLeverRecordError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceObjectLeverRecordError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceObjectLeverRecordError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceObjectLeverRecordError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceObjectLeverRecordError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceObjectLeverRecordError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_lever_id": self.object_lever_id,
            "object_lever_label": self.object_lever_label,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceHazardClockRecord:
    """Hazard clock identifier and safe visible counter/status fields only. No
    ticking logic. No consequence application."""

    hazard_clock_id: str
    hazard_clock_label: str
    visible_counter: str
    visible_status: str
    owner_family: str = "hazard_environment_owner"
    visibility_tier: str = "player_visible"
    source_scope: str
    record_status: str = "active"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.hazard_clock_id, "hazard_clock_id",
            InvalidVerticalSliceHazardClockRecordError,
        )
        _validate_non_empty_str(
            self.hazard_clock_label, "hazard_clock_label",
            InvalidVerticalSliceHazardClockRecordError,
        )
        _validate_non_empty_str(
            self.visible_counter, "visible_counter",
            InvalidVerticalSliceHazardClockRecordError,
        )
        _validate_non_empty_str(
            self.visible_status, "visible_status",
            InvalidVerticalSliceHazardClockRecordError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceHazardClockRecordError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceHazardClockRecordError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceHazardClockRecordError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceHazardClockRecordError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceHazardClockRecordError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceHazardClockRecordError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceHazardClockRecordError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceHazardClockRecordError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "hazard_clock_id": self.hazard_clock_id,
            "hazard_clock_label": self.hazard_clock_label,
            "visible_counter": self.visible_counter,
            "visible_status": self.visible_status,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceVisibleConditionRecord:
    """Condition/injury identifier and safe visible condition label only. No
    damage math. No recovery logic."""

    condition_id: str
    condition_label: str
    owner_family: str = "condition_status_owner"
    visibility_tier: str = "player_visible"
    source_scope: str
    record_status: str = "active"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.condition_id, "condition_id",
            InvalidVerticalSliceVisibleConditionRecordError,
        )
        _validate_non_empty_str(
            self.condition_label, "condition_label",
            InvalidVerticalSliceVisibleConditionRecordError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceVisibleConditionRecordError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceVisibleConditionRecordError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceVisibleConditionRecordError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceVisibleConditionRecordError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceVisibleConditionRecordError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceVisibleConditionRecordError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceVisibleConditionRecordError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceVisibleConditionRecordError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "condition_id": self.condition_id,
            "condition_label": self.condition_label,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceHiddenFactReference:
    """Hidden fact reference identifier only. No hidden fact payload. No secret
    text. No backend-only fact content."""

    hidden_fact_reference_id: str
    owner_family: str = "hidden_information_visibility_owner"
    visibility_tier: str = "hidden"
    redacted_safe_label: str
    routing_policy: str = "redact"
    source_scope: str
    record_status: str = "redacted"
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.hidden_fact_reference_id, "hidden_fact_reference_id",
            InvalidVerticalSliceHiddenFactReferenceError,
        )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceHiddenFactReferenceError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceHiddenFactReferenceError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceHiddenFactReferenceError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceHiddenFactReferenceError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.redacted_safe_label, "redacted_safe_label",
            InvalidVerticalSliceHiddenFactReferenceError,
        )
        _validate_non_empty_str(
            self.routing_policy, "routing_policy",
            InvalidVerticalSliceHiddenFactReferenceError,
        )
        if self.routing_policy not in STATE_OWNER_HIDDEN_INFORMATION_POLICIES:
            raise InvalidVerticalSliceHiddenFactReferenceError(
                f"routing_policy must be one of {sorted(STATE_OWNER_HIDDEN_INFORMATION_POLICIES)}, "
                f"got {self.routing_policy!r}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceHiddenFactReferenceError,
        )
        _validate_non_empty_str(
            self.record_status, "record_status",
            InvalidVerticalSliceHiddenFactReferenceError,
        )
        if self.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
            raise InvalidVerticalSliceHiddenFactReferenceError(
                f"record_status must be one of {sorted(VERTICAL_SLICE_RECORD_STATUSES)}, "
                f"got {self.record_status!r}"
            )
        if self.metadata:
            _validate_no_forbidden_vertical_slice_metadata_keys(
                self.metadata, "metadata", InvalidVerticalSliceHiddenFactReferenceError,
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceHiddenFactReferenceError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "hidden_fact_reference_id": self.hidden_fact_reference_id,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "redacted_safe_label": self.redacted_safe_label,
            "routing_policy": self.routing_policy,
            "source_scope": self.source_scope,
            "record_status": self.record_status,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceReadOnlyStateBundle:
    """Contains exactly the seven minimal vertical-slice records. Frozen. No
    mutation methods."""

    bundle_id: str
    scene: VerticalSliceSceneRecord
    actor: VerticalSliceActorRecord
    npc_target: VerticalSliceNpcTargetRecord
    object_lever: VerticalSliceObjectLeverRecord
    hazard_clock: VerticalSliceHazardClockRecord
    visible_condition: VerticalSliceVisibleConditionRecord
    hidden_fact_reference: VerticalSliceHiddenFactReference
    source_scope: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.bundle_id, "bundle_id",
            InvalidVerticalSliceReadOnlyStateBundleError,
        )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceReadOnlyStateBundleError,
        )
        for field_name, expected_type in (
            ("scene", VerticalSliceSceneRecord),
            ("actor", VerticalSliceActorRecord),
            ("npc_target", VerticalSliceNpcTargetRecord),
            ("object_lever", VerticalSliceObjectLeverRecord),
            ("hazard_clock", VerticalSliceHazardClockRecord),
            ("visible_condition", VerticalSliceVisibleConditionRecord),
            ("hidden_fact_reference", VerticalSliceHiddenFactReference),
        ):
            value = getattr(self, field_name)
            if not isinstance(value, expected_type):
                raise InvalidVerticalSliceReadOnlyStateBundleError(
                    f"{field_name} must be a {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceReadOnlyStateBundleError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "scene": self.scene.to_dict(),
            "actor": self.actor.to_dict(),
            "npc_target": self.npc_target.to_dict(),
            "object_lever": self.object_lever.to_dict(),
            "hazard_clock": self.hazard_clock.to_dict(),
            "visible_condition": self.visible_condition.to_dict(),
            "hidden_fact_reference": self.hidden_fact_reference.to_dict(),
            "source_scope": self.source_scope,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceOwnerProjection:
    """Reference-only safe projection. No raw state payload. No hidden fact
    payload. No narration."""

    projection_id: str
    entity_kind: str
    owner_family: str
    visibility_tier: str
    reference_id: str
    redacted_safe_label: str | None = None
    redaction_required: bool = True
    source_scope: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.projection_id, "projection_id",
            InvalidVerticalSliceOwnerProjectionError,
        )
        _validate_non_empty_str(
            self.entity_kind, "entity_kind",
            InvalidVerticalSliceOwnerProjectionError,
        )
        if self.entity_kind not in VERTICAL_SLICE_ENTITY_KINDS:
            raise InvalidVerticalSliceOwnerProjectionError(
                f"entity_kind must be one of {sorted(VERTICAL_SLICE_ENTITY_KINDS)}, "
                f"got {self.entity_kind!r}"
            )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceOwnerProjectionError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidVerticalSliceOwnerProjectionError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidVerticalSliceOwnerProjectionError,
        )
        if self.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
            raise InvalidVerticalSliceOwnerProjectionError(
                f"visibility_tier must be one of {sorted(VERTICAL_SLICE_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.reference_id, "reference_id",
            InvalidVerticalSliceOwnerProjectionError,
        )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceOwnerProjectionError,
        )
        if self.metadata:
            _validate_no_forbidden_vertical_slice_metadata_keys(
                self.metadata, "metadata", InvalidVerticalSliceOwnerProjectionError,
            )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceOwnerProjectionError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_id": self.projection_id,
            "entity_kind": self.entity_kind,
            "owner_family": self.owner_family,
            "visibility_tier": self.visibility_tier,
            "reference_id": self.reference_id,
            "redacted_safe_label": self.redacted_safe_label,
            "redaction_required": self.redaction_required,
            "source_scope": self.source_scope,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class VerticalSliceOwnerFacadeResult:
    """Result envelope for the read-only vertical slice owner facade. Contains
    no legality evaluation, no transaction preview, no event commitment, no raw
    state payload, and no hidden fact payload."""

    result_id: str
    result_status: str
    owner_family: str
    entity_kind: str
    requested_reference: VerticalSliceStateRecordRef | None = None
    projection: VerticalSliceOwnerProjection | None = None
    non_authority_note: str = VERTICAL_SLICE_NON_AUTHORITY_NOTE
    authority_flags: VerticalSliceStateOwnerAuthorityFlags = field(
        default_factory=VerticalSliceStateOwnerAuthorityFlags,
    )
    source_scope: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.result_id, "result_id",
            InvalidVerticalSliceOwnerFacadeResultError,
        )
        _validate_non_empty_str(
            self.result_status, "result_status",
            InvalidVerticalSliceOwnerFacadeResultError,
        )
        if self.result_status not in VERTICAL_SLICE_FACADE_RESULT_STATUSES:
            raise InvalidVerticalSliceOwnerFacadeResultError(
                f"result_status must be one of {sorted(VERTICAL_SLICE_FACADE_RESULT_STATUSES)}, "
                f"got {self.result_status!r}"
            )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidVerticalSliceOwnerFacadeResultError,
        )
        _validate_non_empty_str(
            self.entity_kind, "entity_kind",
            InvalidVerticalSliceOwnerFacadeResultError,
        )
        if self.requested_reference is not None and not isinstance(
            self.requested_reference, VerticalSliceStateRecordRef,
        ):
            raise InvalidVerticalSliceOwnerFacadeResultError(
                f"requested_reference must be a VerticalSliceStateRecordRef, "
                f"got {type(self.requested_reference).__name__}"
            )
        if self.projection is not None and not isinstance(
            self.projection, VerticalSliceOwnerProjection,
        ):
            raise InvalidVerticalSliceOwnerFacadeResultError(
                f"projection must be a VerticalSliceOwnerProjection, "
                f"got {type(self.projection).__name__}"
            )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidVerticalSliceOwnerFacadeResultError,
        )
        if not isinstance(self.authority_flags, VerticalSliceStateOwnerAuthorityFlags):
            raise InvalidVerticalSliceOwnerFacadeResultError(
                f"authority_flags must be a VerticalSliceStateOwnerAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        _validate_non_empty_str(
            self.source_scope, "source_scope",
            InvalidVerticalSliceOwnerFacadeResultError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_vertical_slice_metadata(self.metadata, InvalidVerticalSliceOwnerFacadeResultError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "result_status": self.result_status,
            "owner_family": self.owner_family,
            "entity_kind": self.entity_kind,
            "requested_reference": (
                self.requested_reference.to_dict()
                if self.requested_reference is not None else None
            ),
            "projection": (
                self.projection.to_dict()
                if self.projection is not None else None
            ),
            "non_authority_note": self.non_authority_note,
            "authority_flags": self.authority_flags.to_dict(),
            "source_scope": self.source_scope,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_vertical_slice_state_owner_authority_flags() -> VerticalSliceStateOwnerAuthorityFlags:
    return VerticalSliceStateOwnerAuthorityFlags()


def create_vertical_slice_state_record_ref(
    *,
    reference_id: str,
    entity_kind: str,
    owner_family: str,
    visibility_tier: str,
    source_scope: str,
    record_status: str = "active",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceStateRecordRef:
    return VerticalSliceStateRecordRef(
        reference_id=reference_id,
        entity_kind=entity_kind,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_scene_record(
    *,
    scene_id: str,
    scene_label: str,
    owner_family: str = "scene_location_owner",
    visibility_tier: str = "player_visible",
    source_scope: str,
    record_status: str = "active",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceSceneRecord:
    return VerticalSliceSceneRecord(
        scene_id=scene_id,
        scene_label=scene_label,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_actor_record(
    *,
    actor_id: str,
    actor_label: str,
    owner_family: str = "actor_identity_owner",
    visibility_tier: str = "player_visible",
    source_scope: str,
    record_status: str = "active",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceActorRecord:
    return VerticalSliceActorRecord(
        actor_id=actor_id,
        actor_label=actor_label,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_npc_target_record(
    *,
    npc_target_id: str,
    npc_target_label: str,
    owner_family: str = "target_reachability_owner",
    visibility_tier: str = "player_visible",
    source_scope: str,
    record_status: str = "active",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceNpcTargetRecord:
    return VerticalSliceNpcTargetRecord(
        npc_target_id=npc_target_id,
        npc_target_label=npc_target_label,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_object_lever_record(
    *,
    object_lever_id: str,
    object_lever_label: str,
    owner_family: str = "object_interactable_owner",
    visibility_tier: str = "player_visible",
    source_scope: str,
    record_status: str = "active",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceObjectLeverRecord:
    return VerticalSliceObjectLeverRecord(
        object_lever_id=object_lever_id,
        object_lever_label=object_lever_label,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_hazard_clock_record(
    *,
    hazard_clock_id: str,
    hazard_clock_label: str,
    visible_counter: str,
    visible_status: str,
    owner_family: str = "hazard_environment_owner",
    visibility_tier: str = "player_visible",
    source_scope: str,
    record_status: str = "active",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceHazardClockRecord:
    return VerticalSliceHazardClockRecord(
        hazard_clock_id=hazard_clock_id,
        hazard_clock_label=hazard_clock_label,
        visible_counter=visible_counter,
        visible_status=visible_status,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_visible_condition_record(
    *,
    condition_id: str,
    condition_label: str,
    owner_family: str = "condition_status_owner",
    visibility_tier: str = "player_visible",
    source_scope: str,
    record_status: str = "active",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceVisibleConditionRecord:
    return VerticalSliceVisibleConditionRecord(
        condition_id=condition_id,
        condition_label=condition_label,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_hidden_fact_reference(
    *,
    hidden_fact_reference_id: str,
    owner_family: str = "hidden_information_visibility_owner",
    visibility_tier: str = "hidden",
    redacted_safe_label: str,
    routing_policy: str = "redact",
    source_scope: str,
    record_status: str = "redacted",
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceHiddenFactReference:
    return VerticalSliceHiddenFactReference(
        hidden_fact_reference_id=hidden_fact_reference_id,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        redacted_safe_label=redacted_safe_label,
        routing_policy=routing_policy,
        source_scope=source_scope,
        record_status=record_status,
        metadata=metadata,
    )


def create_vertical_slice_read_only_state_bundle(
    *,
    bundle_id: str,
    scene: VerticalSliceSceneRecord,
    actor: VerticalSliceActorRecord,
    npc_target: VerticalSliceNpcTargetRecord,
    object_lever: VerticalSliceObjectLeverRecord,
    hazard_clock: VerticalSliceHazardClockRecord,
    visible_condition: VerticalSliceVisibleConditionRecord,
    hidden_fact_reference: VerticalSliceHiddenFactReference,
    source_scope: str,
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceReadOnlyStateBundle:
    return VerticalSliceReadOnlyStateBundle(
        bundle_id=bundle_id,
        scene=scene,
        actor=actor,
        npc_target=npc_target,
        object_lever=object_lever,
        hazard_clock=hazard_clock,
        visible_condition=visible_condition,
        hidden_fact_reference=hidden_fact_reference,
        source_scope=source_scope,
        metadata=metadata,
    )


def create_vertical_slice_owner_projection(
    *,
    projection_id: str,
    entity_kind: str,
    owner_family: str,
    visibility_tier: str,
    reference_id: str,
    redacted_safe_label: str | None = None,
    redaction_required: bool = True,
    source_scope: str,
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceOwnerProjection:
    return VerticalSliceOwnerProjection(
        projection_id=projection_id,
        entity_kind=entity_kind,
        owner_family=owner_family,
        visibility_tier=visibility_tier,
        reference_id=reference_id,
        redacted_safe_label=redacted_safe_label,
        redaction_required=redaction_required,
        source_scope=source_scope,
        metadata=metadata,
    )


def create_vertical_slice_owner_facade_result(
    *,
    result_id: str,
    result_status: str,
    owner_family: str,
    entity_kind: str,
    requested_reference: VerticalSliceStateRecordRef | None = None,
    projection: VerticalSliceOwnerProjection | None = None,
    non_authority_note: str = VERTICAL_SLICE_NON_AUTHORITY_NOTE,
    authority_flags: VerticalSliceStateOwnerAuthorityFlags | None = None,
    source_scope: str,
    metadata: Mapping[str, Any] | None = None,
) -> VerticalSliceOwnerFacadeResult:
    return VerticalSliceOwnerFacadeResult(
        result_id=result_id,
        result_status=result_status,
        owner_family=owner_family,
        entity_kind=entity_kind,
        requested_reference=requested_reference,
        projection=projection,
        non_authority_note=non_authority_note,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else VerticalSliceStateOwnerAuthorityFlags()
        ),
        source_scope=source_scope,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Facade helpers
# ---------------------------------------------------------------------------


def _bundle_record_by_owner_family(
    bundle: VerticalSliceReadOnlyStateBundle,
) -> dict[tuple[str, str], Any]:
    """Map (owner_family, entity_kind) to the corresponding bundle record."""
    return {
        (bundle.scene.owner_family, "scene"): bundle.scene,
        (bundle.actor.owner_family, "actor"): bundle.actor,
        (bundle.npc_target.owner_family, "npc_target"): bundle.npc_target,
        (bundle.object_lever.owner_family, "object_lever"): bundle.object_lever,
        (bundle.hazard_clock.owner_family, "hazard_clock"): bundle.hazard_clock,
        (bundle.visible_condition.owner_family, "visible_condition"): bundle.visible_condition,
        (bundle.hidden_fact_reference.owner_family, "hidden_fact_reference"): bundle.hidden_fact_reference,
    }


def _record_to_reference(record: Any) -> VerticalSliceStateRecordRef:
    """Build a VerticalSliceStateRecordRef from any bundle record."""
    mapping = {
        VerticalSliceSceneRecord: (
            "scene", lambda r: (r.scene_id, r.scene_label)
        ),
        VerticalSliceActorRecord: (
            "actor", lambda r: (r.actor_id, r.actor_label)
        ),
        VerticalSliceNpcTargetRecord: (
            "npc_target", lambda r: (r.npc_target_id, r.npc_target_label)
        ),
        VerticalSliceObjectLeverRecord: (
            "object_lever", lambda r: (r.object_lever_id, r.object_lever_label)
        ),
        VerticalSliceHazardClockRecord: (
            "hazard_clock", lambda r: (r.hazard_clock_id, r.hazard_clock_label)
        ),
        VerticalSliceVisibleConditionRecord: (
            "visible_condition", lambda r: (r.condition_id, r.condition_label)
        ),
        VerticalSliceHiddenFactReference: (
            "hidden_fact_reference", lambda r: (r.hidden_fact_reference_id, r.redacted_safe_label)
        ),
    }
    entity_kind, id_label_fn = mapping[type(record)]
    reference_id, _ = id_label_fn(record)
    return VerticalSliceStateRecordRef(
        reference_id=reference_id,
        entity_kind=entity_kind,
        owner_family=record.owner_family,
        visibility_tier=record.visibility_tier,
        source_scope=record.source_scope,
        record_status=record.record_status,
        metadata=record.metadata,
    )


def _record_to_projection(record: Any) -> VerticalSliceOwnerProjection:
    """Build a VerticalSliceOwnerProjection from any bundle record."""
    mapping = {
        VerticalSliceSceneRecord: (
            "scene", lambda r: (r.scene_id, r.scene_label)
        ),
        VerticalSliceActorRecord: (
            "actor", lambda r: (r.actor_id, r.actor_label)
        ),
        VerticalSliceNpcTargetRecord: (
            "npc_target", lambda r: (r.npc_target_id, r.npc_target_label)
        ),
        VerticalSliceObjectLeverRecord: (
            "object_lever", lambda r: (r.object_lever_id, r.object_lever_label)
        ),
        VerticalSliceHazardClockRecord: (
            "hazard_clock", lambda r: (r.hazard_clock_id, r.hazard_clock_label)
        ),
        VerticalSliceVisibleConditionRecord: (
            "visible_condition", lambda r: (r.condition_id, r.condition_label)
        ),
        VerticalSliceHiddenFactReference: (
            "hidden_fact_reference",
            lambda r: (r.hidden_fact_reference_id, r.redacted_safe_label),
        ),
    }
    entity_kind, id_label_fn = mapping[type(record)]
    reference_id, label = id_label_fn(record)
    redacted_safe_label = None
    redaction_required = record.visibility_tier in ("hidden", "redacted_reference_only")
    if isinstance(record, VerticalSliceHiddenFactReference):
        redacted_safe_label = record.redacted_safe_label
    return VerticalSliceOwnerProjection(
        projection_id=f"proj_{reference_id}",
        entity_kind=entity_kind,
        owner_family=record.owner_family,
        visibility_tier=record.visibility_tier,
        reference_id=reference_id,
        redacted_safe_label=redacted_safe_label,
        redaction_required=redaction_required,
        source_scope=record.source_scope,
        metadata=record.metadata if not redaction_required else MappingProxyType({}),
    )


def build_vertical_slice_reference_manifest(
    bundle: VerticalSliceReadOnlyStateBundle,
) -> tuple[VerticalSliceStateRecordRef, ...]:
    """Build owner-mediated record refs for every record in the bundle."""
    records = (
        bundle.scene,
        bundle.actor,
        bundle.npc_target,
        bundle.object_lever,
        bundle.hazard_clock,
        bundle.visible_condition,
        bundle.hidden_fact_reference,
    )
    return tuple(_record_to_reference(record) for record in records)


def get_vertical_slice_owner_reference(
    bundle: VerticalSliceReadOnlyStateBundle,
    owner_family: str,
    entity_kind: str,
    *,
    result_id: str,
) -> VerticalSliceOwnerFacadeResult:
    """Return an owner-mediated reference for the requested owner family and
    entity kind. Only reads from the frozen bundle; does not mutate state."""
    index = _bundle_record_by_owner_family(bundle)
    record = index.get((owner_family, entity_kind))

    if record is None:
        return create_vertical_slice_owner_facade_result(
            result_id=result_id,
            result_status="unavailable",
            owner_family=owner_family,
            entity_kind=entity_kind,
            source_scope=bundle.source_scope,
        )

    ref = _record_to_reference(record)
    if entity_kind == "hidden_fact_reference":
        return create_vertical_slice_owner_facade_result(
            result_id=result_id,
            result_status="redacted",
            owner_family=owner_family,
            entity_kind=entity_kind,
            requested_reference=ref,
            source_scope=bundle.source_scope,
        )

    if record.record_status == "unavailable":
        return create_vertical_slice_owner_facade_result(
            result_id=result_id,
            result_status="unavailable",
            owner_family=owner_family,
            entity_kind=entity_kind,
            requested_reference=ref,
            source_scope=bundle.source_scope,
        )

    return create_vertical_slice_owner_facade_result(
        result_id=result_id,
        result_status="available_reference",
        owner_family=owner_family,
        entity_kind=entity_kind,
        requested_reference=ref,
        source_scope=bundle.source_scope,
    )


def get_vertical_slice_owner_projection(
    bundle: VerticalSliceReadOnlyStateBundle,
    owner_family: str,
    entity_kind: str,
    *,
    result_id: str,
) -> VerticalSliceOwnerFacadeResult:
    """Return a safe owner-mediated projection for the requested owner family
    and entity kind. Hidden facts are returned as redacted projections."""
    index = _bundle_record_by_owner_family(bundle)
    record = index.get((owner_family, entity_kind))

    if record is None:
        return create_vertical_slice_owner_facade_result(
            result_id=result_id,
            result_status="unavailable",
            owner_family=owner_family,
            entity_kind=entity_kind,
            source_scope=bundle.source_scope,
        )

    projection = _record_to_projection(record)
    ref = _record_to_reference(record)

    if entity_kind == "hidden_fact_reference":
        return create_vertical_slice_owner_facade_result(
            result_id=result_id,
            result_status="redacted",
            owner_family=owner_family,
            entity_kind=entity_kind,
            requested_reference=ref,
            projection=projection,
            source_scope=bundle.source_scope,
        )

    if record.record_status == "unavailable":
        return create_vertical_slice_owner_facade_result(
            result_id=result_id,
            result_status="unavailable",
            owner_family=owner_family,
            entity_kind=entity_kind,
            requested_reference=ref,
            projection=projection,
            source_scope=bundle.source_scope,
        )

    return create_vertical_slice_owner_facade_result(
        result_id=result_id,
        result_status="available_reference",
        owner_family=owner_family,
        entity_kind=entity_kind,
        requested_reference=ref,
        projection=projection,
        source_scope=bundle.source_scope,
    )


def serialize_vertical_slice_owner_facade_result(
    result: VerticalSliceOwnerFacadeResult,
) -> dict[str, Any]:
    """Full backend serializer. Deterministic, JSON-safe."""
    return result.to_dict()


def serialize_vertical_slice_owner_facade_result_visible(
    result: VerticalSliceOwnerFacadeResult,
) -> dict[str, Any]:
    """Visible serializer. Excludes metadata, raw state, hidden fact payload,
    authority flags, backend-only fields, and implementation details."""
    visible: dict[str, Any] = {
        "result_id": result.result_id,
        "result_status": result.result_status,
        "owner_family": result.owner_family,
        "entity_kind": result.entity_kind,
        "non_authority_note": result.non_authority_note,
    }

    if result.projection is not None:
        visible["visibility_tier"] = result.projection.visibility_tier
        visible["redaction_required"] = result.projection.redaction_required
        visible["safe_reference_ids"] = [result.projection.reference_id]
        if result.projection.redacted_safe_label is not None:
            visible["redacted_safe_label"] = result.projection.redacted_safe_label
    elif result.requested_reference is not None:
        visible["visibility_tier"] = result.requested_reference.visibility_tier
        visible["redaction_required"] = (
            result.requested_reference.visibility_tier
            in ("hidden", "redacted_reference_only")
        )
        visible["safe_reference_ids"] = [result.requested_reference.reference_id]
    else:
        visible["visibility_tier"] = None
        visible["redaction_required"] = True
        visible["safe_reference_ids"] = []

    return visible


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_vertical_slice_state_owner_authority_flags(obj: Any) -> bool:
    if not isinstance(obj, VerticalSliceStateOwnerAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True


def validate_vertical_slice_state_record_ref(obj: Any) -> bool:
    if not isinstance(obj, VerticalSliceStateRecordRef):
        return False
    if not isinstance(obj.reference_id, str) or not obj.reference_id:
        return False
    if obj.entity_kind not in VERTICAL_SLICE_ENTITY_KINDS:
        return False
    if obj.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
        return False
    if obj.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
        return False
    if obj.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            obj.metadata, "metadata", InvalidVerticalSliceStateRecordRefError,
        )
    except InvalidVerticalSliceStateRecordRefError:
        return False
    return True


def _validate_vertical_slice_record_common(
    obj: Any,
    expected_cls: type,
    id_field: str,
    label_field: str,
    error_cls: type[Exception],
) -> bool:
    if not isinstance(obj, expected_cls):
        return False
    if not isinstance(getattr(obj, id_field), str) or not getattr(obj, id_field):
        return False
    if not isinstance(getattr(obj, label_field), str) or not getattr(obj, label_field):
        return False
    if obj.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
        return False
    if obj.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
        return False
    if obj.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            obj.metadata, "metadata", error_cls,
        )
    except error_cls:
        return False
    return True


def validate_vertical_slice_scene_record(obj: Any) -> bool:
    return _validate_vertical_slice_record_common(
        obj, VerticalSliceSceneRecord, "scene_id", "scene_label",
        InvalidVerticalSliceSceneRecordError,
    )


def validate_vertical_slice_actor_record(obj: Any) -> bool:
    return _validate_vertical_slice_record_common(
        obj, VerticalSliceActorRecord, "actor_id", "actor_label",
        InvalidVerticalSliceActorRecordError,
    )


def validate_vertical_slice_npc_target_record(obj: Any) -> bool:
    return _validate_vertical_slice_record_common(
        obj, VerticalSliceNpcTargetRecord, "npc_target_id", "npc_target_label",
        InvalidVerticalSliceNpcTargetRecordError,
    )


def validate_vertical_slice_object_lever_record(obj: Any) -> bool:
    return _validate_vertical_slice_record_common(
        obj, VerticalSliceObjectLeverRecord, "object_lever_id", "object_lever_label",
        InvalidVerticalSliceObjectLeverRecordError,
    )


def validate_vertical_slice_hazard_clock_record(obj: Any) -> bool:
    if not isinstance(obj, VerticalSliceHazardClockRecord):
        return False
    for field_name in ("hazard_clock_id", "hazard_clock_label", "visible_counter", "visible_status"):
        if not isinstance(getattr(obj, field_name), str) or not getattr(obj, field_name):
            return False
    if obj.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
        return False
    if obj.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
        return False
    if obj.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            obj.metadata, "metadata", InvalidVerticalSliceHazardClockRecordError,
        )
    except InvalidVerticalSliceHazardClockRecordError:
        return False
    return True


def validate_vertical_slice_visible_condition_record(obj: Any) -> bool:
    return _validate_vertical_slice_record_common(
        obj, VerticalSliceVisibleConditionRecord, "condition_id", "condition_label",
        InvalidVerticalSliceVisibleConditionRecordError,
    )


def validate_vertical_slice_hidden_fact_reference(obj: Any) -> bool:
    if not isinstance(obj, VerticalSliceHiddenFactReference):
        return False
    if (
        not isinstance(obj.hidden_fact_reference_id, str)
        or not obj.hidden_fact_reference_id
    ):
        return False
    if obj.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
        return False
    if obj.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
        return False
    if obj.record_status not in VERTICAL_SLICE_RECORD_STATUSES:
        return False
    if obj.routing_policy not in STATE_OWNER_HIDDEN_INFORMATION_POLICIES:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            obj.metadata, "metadata", InvalidVerticalSliceHiddenFactReferenceError,
        )
    except InvalidVerticalSliceHiddenFactReferenceError:
        return False
    return True


def validate_vertical_slice_read_only_state_bundle(obj: Any) -> bool:
    if not isinstance(obj, VerticalSliceReadOnlyStateBundle):
        return False
    if not isinstance(obj.bundle_id, str) or not obj.bundle_id:
        return False
    for field_name, expected_type in (
        ("scene", VerticalSliceSceneRecord),
        ("actor", VerticalSliceActorRecord),
        ("npc_target", VerticalSliceNpcTargetRecord),
        ("object_lever", VerticalSliceObjectLeverRecord),
        ("hazard_clock", VerticalSliceHazardClockRecord),
        ("visible_condition", VerticalSliceVisibleConditionRecord),
        ("hidden_fact_reference", VerticalSliceHiddenFactReference),
    ):
        if not isinstance(getattr(obj, field_name), expected_type):
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            obj.metadata, "metadata", InvalidVerticalSliceReadOnlyStateBundleError,
        )
    except InvalidVerticalSliceReadOnlyStateBundleError:
        return False
    return True


def validate_vertical_slice_owner_projection(obj: Any) -> bool:
    if not isinstance(obj, VerticalSliceOwnerProjection):
        return False
    if not isinstance(obj.projection_id, str) or not obj.projection_id:
        return False
    if obj.entity_kind not in VERTICAL_SLICE_ENTITY_KINDS:
        return False
    if obj.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
        return False
    if obj.visibility_tier not in VERTICAL_SLICE_VISIBILITY_TIERS:
        return False
    if not isinstance(obj.reference_id, str) or not obj.reference_id:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            obj.metadata, "metadata", InvalidVerticalSliceOwnerProjectionError,
        )
    except InvalidVerticalSliceOwnerProjectionError:
        return False
    return True


def validate_vertical_slice_owner_facade_result(obj: Any) -> bool:
    if not isinstance(obj, VerticalSliceOwnerFacadeResult):
        return False
    if not isinstance(obj.result_id, str) or not obj.result_id:
        return False
    if obj.result_status not in VERTICAL_SLICE_FACADE_RESULT_STATUSES:
        return False
    if obj.requested_reference is not None and not isinstance(
        obj.requested_reference, VerticalSliceStateRecordRef,
    ):
        return False
    if obj.projection is not None and not isinstance(
        obj.projection, VerticalSliceOwnerProjection,
    ):
        return False
    if not isinstance(obj.authority_flags, VerticalSliceStateOwnerAuthorityFlags):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_vertical_slice_metadata_keys(
            obj.metadata, "metadata", InvalidVerticalSliceOwnerFacadeResultError,
        )
    except InvalidVerticalSliceOwnerFacadeResultError:
        return False
    return True
