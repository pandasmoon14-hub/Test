"""Projection and Visibility Adapter — RT-002B.

RUNTIME-DOMAIN-RT-002B: implements a projection and visibility adapter that sits
between RT-002A (read-only vertical slice state owner facade) and future RT-002C
(action legality reads vertical-slice projections). It classifies RT-002A facade
results into visibility-classified projection packets and proves that downstream
runtime components can receive those packets without reading raw state, receiving
hidden truth, inferring hidden truth from absence, or depending directly on
RT-002A internal record structure.

This module is intentionally narrow:
* projection classification for RT-002A facade results
* visibility-classified adapter packets
* backend-safe projection packet
* visible-safe projection packet
* redacted projection packet
* unavailable/deferred/unknown projection packet
* deterministic serializers
* visible serializer with strict redaction
* validation helpers
* hidden/raw-state metadata containment

It does NOT implement:
* action legality evaluation
* command execution
* state mutation
* event append or event commitment
* transaction preview materialization
* persistence/replay writes
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
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.read_only_vertical_slice_state_owner_facade import (
    VERTICAL_SLICE_ENTITY_KINDS,
    VERTICAL_SLICE_NON_AUTHORITY_NOTE,
    VERTICAL_SLICE_OWNER_FAMILIES,
    VERTICAL_SLICE_VISIBILITY_TIERS,
    VerticalSliceOwnerFacadeResult,
    VerticalSliceOwnerProjection,
)


__all__ = [
    # Constants
    "PROJECTION_VISIBILITY_ADAPTER_STATUSES",
    "PROJECTION_VISIBILITY_TIERS",
    "PROJECTION_PACKET_KINDS",
    "PROJECTION_REDACTION_REASONS",
    "PROJECTION_DOWNSTREAM_CONSUMER_TYPES",
    "PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE",
    "FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS",
    # Error hierarchy
    "ProjectionVisibilityAdapterError",
    "InvalidProjectionVisibilityAuthorityFlagsError",
    "InvalidProjectionVisibilitySourceRefError",
    "InvalidProjectionVisibilityDescriptorError",
    "InvalidProjectionVisibilityAdapterPacketError",
    "InvalidProjectionVisibilityAdapterResultError",
    # Dataclasses
    "ProjectionVisibilityAuthorityFlags",
    "ProjectionVisibilitySourceRef",
    "ProjectionVisibilityDescriptor",
    "ProjectionVisibilityAdapterPacket",
    "ProjectionVisibilityAdapterResult",
    # Factory functions
    "create_projection_visibility_authority_flags",
    "create_projection_visibility_source_ref",
    "create_projection_visibility_descriptor",
    "create_projection_visibility_adapter_packet",
    "create_projection_visibility_adapter_result",
    # Adapter functions
    "adapt_vertical_slice_facade_result_for_backend",
    "adapt_vertical_slice_facade_result_for_visible",
    "adapt_vertical_slice_facade_result_for_downstream",
    "serialize_projection_visibility_adapter_packet",
    "serialize_projection_visibility_adapter_packet_visible",
    "serialize_projection_visibility_adapter_result",
    "serialize_projection_visibility_adapter_result_visible",
    # Validators
    "validate_projection_visibility_authority_flags",
    "validate_projection_visibility_source_ref",
    "validate_projection_visibility_descriptor",
    "validate_projection_visibility_adapter_packet",
    "validate_projection_visibility_adapter_result",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECTION_VISIBILITY_ADAPTER_STATUSES = frozenset({
    "backend_projection_available",
    "visible_projection_available",
    "redacted_projection_available",
    "unavailable",
    "deferred",
    "unknown",
})

PROJECTION_VISIBILITY_TIERS = VERTICAL_SLICE_VISIBILITY_TIERS

PROJECTION_PACKET_KINDS = frozenset({
    "backend_safe_projection",
    "visible_safe_projection",
    "redacted_projection",
    "unavailable_projection",
    "deferred_projection",
    "unknown_projection",
})

PROJECTION_REDACTION_REASONS = frozenset({
    "none",
    "hidden_fact",
    "backend_only",
    "unavailable",
    "deferred",
    "unknown",
})

PROJECTION_DOWNSTREAM_CONSUMER_TYPES = frozenset({
    "runtime_legality_reader",
    "transaction_preview_reader",
    "event_audit_reader",
    "context_packet_compiler_reader",
    "model_visible_reader",
})

FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS = frozenset({
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
    "projection_payload",
    "record_payload",
    "world_state",
})

PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE = (
    "This projection and visibility adapter is reference-only and authorizes no "
    "action legality evaluation, no command execution, no state mutation, no "
    "event append or commitment, no transaction preview materialization, no "
    "persistence or replay writes, no RNG/table/oracle execution, no resource or "
    "consequence math execution, no combat/ability/skill/effect resolution, no "
    "model calls, no prompt rendering, no narration generation, no live-play or "
    "UI behavior, no conversion, no sourcebook inclusion, and no canon promotion."
)


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------


class ProjectionVisibilityAdapterError(ValueError):
    """Base error for RT-002B projection and visibility adapter operations."""


class InvalidProjectionVisibilityAuthorityFlagsError(
    ProjectionVisibilityAdapterError,
):
    """Raised when projection visibility authority flags contain a non-False value."""


class InvalidProjectionVisibilitySourceRefError(
    ProjectionVisibilityAdapterError,
):
    """Raised when a projection visibility source reference fails validation."""


class InvalidProjectionVisibilityDescriptorError(
    ProjectionVisibilityAdapterError,
):
    """Raised when a projection visibility descriptor fails validation."""


class InvalidProjectionVisibilityAdapterPacketError(
    ProjectionVisibilityAdapterError,
):
    """Raised when a projection visibility adapter packet fails validation."""


class InvalidProjectionVisibilityAdapterResultError(
    ProjectionVisibilityAdapterError,
):
    """Raised when a projection visibility adapter result fails validation."""


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


def _validate_no_forbidden_projection_visibility_metadata_keys(
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
            if k in FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS:
                raise error_cls(
                    f"metadata key {k!r} at {path} is forbidden: "
                    f"projection visibility metadata must not carry hidden or backend-only data"
                )
            _validate_no_forbidden_projection_visibility_metadata_keys(
                v, f"{path}.{k}", error_cls,
            )
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            _validate_no_forbidden_projection_visibility_metadata_keys(
                item, f"{path}[{i}]", error_cls,
            )


def _safe_projection_visibility_metadata(
    metadata: Mapping[str, Any] | None, error_cls: type[Exception],
) -> Mapping[str, Any]:
    """JSON-safe metadata that also recursively rejects hidden/raw-state keys."""
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    _validate_no_forbidden_projection_visibility_metadata_keys(
        metadata, "metadata", error_cls,
    )
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


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ProjectionVisibilityAuthorityFlags:
    """All authority flags must be false-only. Any non-False value raises during
    construction."""

    raw_state_access_authorized: bool = False
    hidden_information_disclosure_authorized: bool = False
    state_mutation_authorized: bool = False
    action_legality_evaluation_authorized: bool = False
    command_execution_authorized: bool = False
    transaction_preview_authorized: bool = False
    event_commitment_authorized: bool = False
    persistence_write_authorized: bool = False
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
                raise InvalidProjectionVisibilityAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in "
                    f"RT-002B skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class ProjectionVisibilitySourceRef:
    """Reference-only descriptor for an RT-002A facade result/projection/reference.
    Carries no raw RT-002A record payload and no hidden fact payload."""

    source_ref_id: str
    source_facade_result_id: str | None = None
    source_projection_id: str | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.source_ref_id, "source_ref_id",
            InvalidProjectionVisibilitySourceRefError,
        )
        if self.source_facade_result_id is not None:
            _validate_non_empty_str(
                self.source_facade_result_id, "source_facade_result_id",
                InvalidProjectionVisibilitySourceRefError,
            )
        if self.source_projection_id is not None:
            _validate_non_empty_str(
                self.source_projection_id, "source_projection_id",
                InvalidProjectionVisibilitySourceRefError,
            )
        object.__setattr__(
            self, "metadata",
            _safe_projection_visibility_metadata(
                self.metadata, InvalidProjectionVisibilitySourceRefError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_ref_id": self.source_ref_id,
            "source_facade_result_id": self.source_facade_result_id,
            "source_projection_id": self.source_projection_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ProjectionVisibilityDescriptor:
    """Visibility classification for an adapter packet. Contains no hidden truth."""

    visibility_tier: str
    packet_kind: str
    redaction_required: bool = False
    redaction_reason: str = "none"
    safe_reference_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.visibility_tier, "visibility_tier",
            InvalidProjectionVisibilityDescriptorError,
        )
        if self.visibility_tier not in PROJECTION_VISIBILITY_TIERS:
            raise InvalidProjectionVisibilityDescriptorError(
                f"visibility_tier must be one of {sorted(PROJECTION_VISIBILITY_TIERS)}, "
                f"got {self.visibility_tier!r}"
            )
        _validate_non_empty_str(
            self.packet_kind, "packet_kind",
            InvalidProjectionVisibilityDescriptorError,
        )
        if self.packet_kind not in PROJECTION_PACKET_KINDS:
            raise InvalidProjectionVisibilityDescriptorError(
                f"packet_kind must be one of {sorted(PROJECTION_PACKET_KINDS)}, "
                f"got {self.packet_kind!r}"
            )
        _validate_non_empty_str(
            self.redaction_reason, "redaction_reason",
            InvalidProjectionVisibilityDescriptorError,
        )
        if self.redaction_reason not in PROJECTION_REDACTION_REASONS:
            raise InvalidProjectionVisibilityDescriptorError(
                f"redaction_reason must be one of {sorted(PROJECTION_REDACTION_REASONS)}, "
                f"got {self.redaction_reason!r}"
            )
        if not isinstance(self.redaction_required, bool):
            raise InvalidProjectionVisibilityDescriptorError(
                f"redaction_required must be a bool, got {self.redaction_required!r}"
            )
        object.__setattr__(
            self, "safe_reference_ids",
            _safe_str_tuple(
                self.safe_reference_ids, "safe_reference_ids",
                InvalidProjectionVisibilityDescriptorError,
            ),
        )
        object.__setattr__(
            self, "metadata",
            _safe_projection_visibility_metadata(
                self.metadata, InvalidProjectionVisibilityDescriptorError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "visibility_tier": self.visibility_tier,
            "packet_kind": self.packet_kind,
            "redaction_required": self.redaction_required,
            "redaction_reason": self.redaction_reason,
            "safe_reference_ids": list(self.safe_reference_ids),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ProjectionVisibilityAdapterPacket:
    """A visibility-classified projection packet ready for a downstream consumer.
    Contains no raw state, no hidden fact payload, and no forbidden metadata keys."""

    packet_id: str
    adapter_status: str
    owner_family: str
    entity_kind: str
    packet_kind: str
    source_reference: ProjectionVisibilitySourceRef
    visibility_descriptor: ProjectionVisibilityDescriptor
    downstream_consumer_type: str = "runtime_legality_reader"
    non_authority_note: str = PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE
    authority_flags: ProjectionVisibilityAuthorityFlags = field(
        default_factory=ProjectionVisibilityAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.packet_id, "packet_id",
            InvalidProjectionVisibilityAdapterPacketError,
        )
        _validate_non_empty_str(
            self.adapter_status, "adapter_status",
            InvalidProjectionVisibilityAdapterPacketError,
        )
        if self.adapter_status not in PROJECTION_VISIBILITY_ADAPTER_STATUSES:
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"adapter_status must be one of {sorted(PROJECTION_VISIBILITY_ADAPTER_STATUSES)}, "
                f"got {self.adapter_status!r}"
            )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidProjectionVisibilityAdapterPacketError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"owner_family must be one of {sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        _validate_non_empty_str(
            self.entity_kind, "entity_kind",
            InvalidProjectionVisibilityAdapterPacketError,
        )
        if self.entity_kind not in VERTICAL_SLICE_ENTITY_KINDS:
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"entity_kind must be one of {sorted(VERTICAL_SLICE_ENTITY_KINDS)}, "
                f"got {self.entity_kind!r}"
            )
        _validate_non_empty_str(
            self.packet_kind, "packet_kind",
            InvalidProjectionVisibilityAdapterPacketError,
        )
        if self.packet_kind not in PROJECTION_PACKET_KINDS:
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"packet_kind must be one of {sorted(PROJECTION_PACKET_KINDS)}, "
                f"got {self.packet_kind!r}"
            )
        if not isinstance(self.source_reference, ProjectionVisibilitySourceRef):
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"source_reference must be a ProjectionVisibilitySourceRef, "
                f"got {type(self.source_reference).__name__}"
            )
        if not isinstance(self.visibility_descriptor, ProjectionVisibilityDescriptor):
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"visibility_descriptor must be a ProjectionVisibilityDescriptor, "
                f"got {type(self.visibility_descriptor).__name__}"
            )
        _validate_non_empty_str(
            self.downstream_consumer_type, "downstream_consumer_type",
            InvalidProjectionVisibilityAdapterPacketError,
        )
        if self.downstream_consumer_type not in PROJECTION_DOWNSTREAM_CONSUMER_TYPES:
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"downstream_consumer_type must be one of "
                f"{sorted(PROJECTION_DOWNSTREAM_CONSUMER_TYPES)}, "
                f"got {self.downstream_consumer_type!r}"
            )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidProjectionVisibilityAdapterPacketError,
        )
        if not isinstance(self.authority_flags, ProjectionVisibilityAuthorityFlags):
            raise InvalidProjectionVisibilityAdapterPacketError(
                f"authority_flags must be a ProjectionVisibilityAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_projection_visibility_metadata(
                self.metadata, InvalidProjectionVisibilityAdapterPacketError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "adapter_status": self.adapter_status,
            "owner_family": self.owner_family,
            "entity_kind": self.entity_kind,
            "packet_kind": self.packet_kind,
            "source_reference": self.source_reference.to_dict(),
            "visibility_descriptor": self.visibility_descriptor.to_dict(),
            "downstream_consumer_type": self.downstream_consumer_type,
            "non_authority_note": self.non_authority_note,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ProjectionVisibilityAdapterResult:
    """Result envelope containing one or more visibility-classified adapter packets.
    Contains no legality evaluation, no transaction preview, no event commitment,
    no raw state payload, and no hidden fact payload."""

    result_id: str
    adapter_status: str
    packets: tuple[ProjectionVisibilityAdapterPacket, ...]
    non_authority_note: str = PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE
    authority_flags: ProjectionVisibilityAuthorityFlags = field(
        default_factory=ProjectionVisibilityAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.result_id, "result_id",
            InvalidProjectionVisibilityAdapterResultError,
        )
        _validate_non_empty_str(
            self.adapter_status, "adapter_status",
            InvalidProjectionVisibilityAdapterResultError,
        )
        if self.adapter_status not in PROJECTION_VISIBILITY_ADAPTER_STATUSES:
            raise InvalidProjectionVisibilityAdapterResultError(
                f"adapter_status must be one of {sorted(PROJECTION_VISIBILITY_ADAPTER_STATUSES)}, "
                f"got {self.adapter_status!r}"
            )
        if not isinstance(self.packets, tuple) or not self.packets:
            raise InvalidProjectionVisibilityAdapterResultError(
                "packets must be a non-empty tuple of ProjectionVisibilityAdapterPacket"
            )
        for i, packet in enumerate(self.packets):
            if not isinstance(packet, ProjectionVisibilityAdapterPacket):
                raise InvalidProjectionVisibilityAdapterResultError(
                    f"packets[{i}] must be a ProjectionVisibilityAdapterPacket, "
                    f"got {type(packet).__name__}"
                )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidProjectionVisibilityAdapterResultError,
        )
        if not isinstance(self.authority_flags, ProjectionVisibilityAuthorityFlags):
            raise InvalidProjectionVisibilityAdapterResultError(
                f"authority_flags must be a ProjectionVisibilityAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_projection_visibility_metadata(
                self.metadata, InvalidProjectionVisibilityAdapterResultError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "adapter_status": self.adapter_status,
            "packets": [packet.to_dict() for packet in self.packets],
            "non_authority_note": self.non_authority_note,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_projection_visibility_authority_flags() -> ProjectionVisibilityAuthorityFlags:
    return ProjectionVisibilityAuthorityFlags()


def create_projection_visibility_source_ref(
    *,
    source_ref_id: str,
    source_facade_result_id: str | None = None,
    source_projection_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ProjectionVisibilitySourceRef:
    return ProjectionVisibilitySourceRef(
        source_ref_id=source_ref_id,
        source_facade_result_id=source_facade_result_id,
        source_projection_id=source_projection_id,
        metadata=metadata,
    )


def create_projection_visibility_descriptor(
    *,
    visibility_tier: str,
    packet_kind: str,
    redaction_required: bool = False,
    redaction_reason: str = "none",
    safe_reference_ids: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ProjectionVisibilityDescriptor:
    return ProjectionVisibilityDescriptor(
        visibility_tier=visibility_tier,
        packet_kind=packet_kind,
        redaction_required=redaction_required,
        redaction_reason=redaction_reason,
        safe_reference_ids=safe_reference_ids,
        metadata=metadata,
    )


def create_projection_visibility_adapter_packet(
    *,
    packet_id: str,
    adapter_status: str,
    owner_family: str,
    entity_kind: str,
    packet_kind: str,
    source_reference: ProjectionVisibilitySourceRef,
    visibility_descriptor: ProjectionVisibilityDescriptor,
    downstream_consumer_type: str = "runtime_legality_reader",
    non_authority_note: str = PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE,
    authority_flags: ProjectionVisibilityAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ProjectionVisibilityAdapterPacket:
    return ProjectionVisibilityAdapterPacket(
        packet_id=packet_id,
        adapter_status=adapter_status,
        owner_family=owner_family,
        entity_kind=entity_kind,
        packet_kind=packet_kind,
        source_reference=source_reference,
        visibility_descriptor=visibility_descriptor,
        downstream_consumer_type=downstream_consumer_type,
        non_authority_note=non_authority_note,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ProjectionVisibilityAuthorityFlags()
        ),
        metadata=metadata,
    )


def create_projection_visibility_adapter_result(
    *,
    result_id: str,
    adapter_status: str,
    packets: Sequence[ProjectionVisibilityAdapterPacket],
    non_authority_note: str = PROJECTION_VISIBILITY_NON_AUTHORITY_NOTE,
    authority_flags: ProjectionVisibilityAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ProjectionVisibilityAdapterResult:
    return ProjectionVisibilityAdapterResult(
        result_id=result_id,
        adapter_status=adapter_status,
        packets=tuple(packets),
        non_authority_note=non_authority_note,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ProjectionVisibilityAuthorityFlags()
        ),
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Adapter helpers
# ---------------------------------------------------------------------------


def _classify_facade_result(
    facade_result: VerticalSliceOwnerFacadeResult,
) -> tuple[str, str, str, bool, list[str]]:
    """Return (adapter_status, packet_kind, visibility_tier, redaction_required, safe_ids)."""
    result_status = facade_result.result_status
    projection = facade_result.projection
    requested_reference = facade_result.requested_reference

    safe_ids: list[str] = []
    if projection is not None:
        safe_ids.append(projection.reference_id)
    elif requested_reference is not None:
        safe_ids.append(requested_reference.reference_id)

    if result_status == "deferred":
        return ("deferred", "deferred_projection", "hidden", True, safe_ids)
    if result_status == "unknown":
        return ("unknown", "unknown_projection", "hidden", True, safe_ids)
    if result_status == "unavailable":
        return ("unavailable", "unavailable_projection", "hidden", True, safe_ids)

    visibility_tier = "hidden"
    if projection is not None:
        visibility_tier = projection.visibility_tier
    elif requested_reference is not None:
        visibility_tier = requested_reference.visibility_tier

    is_hidden = visibility_tier in ("hidden", "redacted_reference_only")
    is_backend_only = visibility_tier == "backend_visible"

    if result_status == "redacted" or is_hidden:
        return (
            "redacted_projection_available",
            "redacted_projection",
            visibility_tier,
            True,
            safe_ids,
        )

    if is_backend_only:
        return (
            "backend_projection_available",
            "backend_safe_projection",
            visibility_tier,
            True,
            safe_ids,
        )

    return (
        "visible_projection_available",
        "visible_safe_projection",
        visibility_tier,
        False,
        safe_ids,
    )


def _build_source_ref_from_facade_result(
    facade_result: VerticalSliceOwnerFacadeResult,
) -> ProjectionVisibilitySourceRef:
    """Build a source reference that carries RT-002A IDs only."""
    projection = facade_result.projection
    requested_reference = facade_result.requested_reference

    source_projection_id = None
    if projection is not None:
        source_projection_id = projection.projection_id

    source_ref_id = ""
    if requested_reference is not None:
        source_ref_id = requested_reference.reference_id
    elif projection is not None:
        source_ref_id = projection.reference_id
    else:
        source_ref_id = facade_result.result_id

    return create_projection_visibility_source_ref(
        source_ref_id=source_ref_id,
        source_facade_result_id=facade_result.result_id,
        source_projection_id=source_projection_id,
    )


def _redaction_reason_for(
    packet_kind: str, visibility_tier: str,
) -> str:
    if packet_kind == "redacted_projection":
        if visibility_tier in ("hidden", "redacted_reference_only"):
            return "hidden_fact"
        return "backend_only"
    if packet_kind == "unavailable_projection":
        return "unavailable"
    if packet_kind == "deferred_projection":
        return "deferred"
    if packet_kind == "unknown_projection":
        return "unknown"
    return "none"


def adapt_vertical_slice_facade_result_for_backend(
    facade_result: VerticalSliceOwnerFacadeResult,
    *,
    packet_id: str,
    downstream_consumer_type: str = "runtime_legality_reader",
    result_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ProjectionVisibilityAdapterResult:
    """Adapt an RT-002A facade result into a backend-safe projection packet.

    Preserves safe reference IDs, owner family, entity kind, visibility tier,
    result status, and redaction flags. Does not expose raw state, hidden fact
    payloads, RT-002A record payloads, or forbidden metadata keys.
    """
    if not isinstance(facade_result, VerticalSliceOwnerFacadeResult):
        raise InvalidProjectionVisibilityAdapterResultError(
            f"facade_result must be a VerticalSliceOwnerFacadeResult, "
            f"got {type(facade_result).__name__}"
        )

    adapter_status, packet_kind, visibility_tier, redaction_required, safe_ids = (
        _classify_facade_result(facade_result)
    )

    source_ref = _build_source_ref_from_facade_result(facade_result)
    descriptor = create_projection_visibility_descriptor(
        visibility_tier=visibility_tier,
        packet_kind=packet_kind,
        redaction_required=redaction_required,
        redaction_reason=_redaction_reason_for(packet_kind, visibility_tier),
        safe_reference_ids=safe_ids,
    )
    packet = create_projection_visibility_adapter_packet(
        packet_id=packet_id,
        adapter_status=adapter_status,
        owner_family=facade_result.owner_family,
        entity_kind=facade_result.entity_kind,
        packet_kind=packet_kind,
        source_reference=source_ref,
        visibility_descriptor=descriptor,
        downstream_consumer_type=downstream_consumer_type,
        metadata=metadata,
    )
    return create_projection_visibility_adapter_result(
        result_id=result_id or f"adapt_result_{packet_id}",
        adapter_status=adapter_status,
        packets=(packet,),
    )


def adapt_vertical_slice_facade_result_for_visible(
    facade_result: VerticalSliceOwnerFacadeResult,
    *,
    packet_id: str,
    downstream_consumer_type: str = "model_visible_reader",
    result_id: str | None = None,
) -> ProjectionVisibilityAdapterResult:
    """Adapt an RT-002A facade result into a visible-safe projection packet.

    Stricter than the backend adapter. Excludes metadata, authority flags, source
    scope, internal source reference structure, backend-only fields, raw state,
    hidden facts, and implementation details.
    """
    if not isinstance(facade_result, VerticalSliceOwnerFacadeResult):
        raise InvalidProjectionVisibilityAdapterResultError(
            f"facade_result must be a VerticalSliceOwnerFacadeResult, "
            f"got {type(facade_result).__name__}"
        )

    adapter_status, packet_kind, visibility_tier, redaction_required, safe_ids = (
        _classify_facade_result(facade_result)
    )

    # Visible output must always redact backend-only or hidden content.
    if packet_kind in ("backend_safe_projection", "redacted_projection"):
        packet_kind = "redacted_projection"
        adapter_status = "redacted_projection_available"
        redaction_required = True

    # For hidden fact references, only expose redaction-safe information.
    redacted_safe_label: str | None = None
    if (
        facade_result.entity_kind == "hidden_fact_reference"
        and facade_result.projection is not None
    ):
        redacted_safe_label = facade_result.projection.redacted_safe_label

    # Source ref is reduced to a single generic safe reference ID.
    safe_ref_id = safe_ids[0] if safe_ids else facade_result.result_id
    source_ref = create_projection_visibility_source_ref(
        source_ref_id=safe_ref_id,
    )
    descriptor = create_projection_visibility_descriptor(
        visibility_tier=visibility_tier,
        packet_kind=packet_kind,
        redaction_required=redaction_required,
        redaction_reason=_redaction_reason_for(packet_kind, visibility_tier),
        safe_reference_ids=[safe_ref_id],
    )
    packet_metadata: dict[str, Any] = {}
    if redacted_safe_label is not None:
        packet_metadata["redacted_safe_label"] = redacted_safe_label

    packet = create_projection_visibility_adapter_packet(
        packet_id=packet_id,
        adapter_status=adapter_status,
        owner_family=facade_result.owner_family,
        entity_kind=facade_result.entity_kind,
        packet_kind=packet_kind,
        source_reference=source_ref,
        visibility_descriptor=descriptor,
        downstream_consumer_type=downstream_consumer_type,
        metadata=packet_metadata if packet_metadata else None,
    )

    return create_projection_visibility_adapter_result(
        result_id=result_id or f"adapt_visible_result_{packet_id}",
        adapter_status=adapter_status,
        packets=(packet,),
    )


def adapt_vertical_slice_facade_result_for_downstream(
    facade_result: VerticalSliceOwnerFacadeResult,
    *,
    packet_id: str,
    downstream_consumer_type: str = "runtime_legality_reader",
    result_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ProjectionVisibilityAdapterResult:
    """Adapt an RT-002A facade result for a labeled downstream consumer.

    Downstream consumer types are labels only and do not trigger behavior. This
    function returns a backend-safe adapter result with the consumer label set.
    Callers that need strict visible output should use
    adapt_vertical_slice_facade_result_for_visible directly.
    """
    return adapt_vertical_slice_facade_result_for_backend(
        facade_result,
        packet_id=packet_id,
        downstream_consumer_type=downstream_consumer_type,
        result_id=result_id,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------


def serialize_projection_visibility_adapter_packet(
    packet: ProjectionVisibilityAdapterPacket,
) -> dict[str, Any]:
    """Full backend serializer. Deterministic, JSON-safe."""
    return packet.to_dict()


def serialize_projection_visibility_adapter_packet_visible(
    packet: ProjectionVisibilityAdapterPacket,
) -> dict[str, Any]:
    """Visible serializer. Excludes metadata, authority flags, source scope,
    internal source reference structure, backend-only fields, raw state, hidden
    facts, and implementation details."""
    descriptor = packet.visibility_descriptor
    visible: dict[str, Any] = {
        "packet_id": packet.packet_id,
        "adapter_status": packet.adapter_status,
        "owner_family": packet.owner_family,
        "entity_kind": packet.entity_kind,
        "packet_kind": packet.packet_kind,
        "visibility_tier": descriptor.visibility_tier,
        "redaction_required": descriptor.redaction_required,
        "redaction_reason": descriptor.redaction_reason,
        "safe_reference_ids": list(descriptor.safe_reference_ids),
        "downstream_consumer_type": packet.downstream_consumer_type,
        "non_authority_note": packet.non_authority_note,
    }
    if descriptor.redaction_reason == "hidden_fact" and packet.metadata:
        redacted_safe_label = packet.metadata.get("redacted_safe_label")
        if redacted_safe_label is not None:
            visible["redacted_safe_label"] = redacted_safe_label
    return visible


def serialize_projection_visibility_adapter_result(
    result: ProjectionVisibilityAdapterResult,
) -> dict[str, Any]:
    """Full backend serializer. Deterministic, JSON-safe."""
    return result.to_dict()


def serialize_projection_visibility_adapter_result_visible(
    result: ProjectionVisibilityAdapterResult,
) -> dict[str, Any]:
    """Visible serializer. Excludes metadata, authority flags, and backend-only
    fields from every packet."""
    return {
        "result_id": result.result_id,
        "adapter_status": result.adapter_status,
        "packets": [
            serialize_projection_visibility_adapter_packet_visible(packet)
            for packet in result.packets
        ],
        "non_authority_note": result.non_authority_note,
    }


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_projection_visibility_authority_flags(obj: Any) -> bool:
    if not isinstance(obj, ProjectionVisibilityAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True


def validate_projection_visibility_source_ref(obj: Any) -> bool:
    if not isinstance(obj, ProjectionVisibilitySourceRef):
        return False
    if not isinstance(obj.source_ref_id, str) or not obj.source_ref_id:
        return False
    if obj.source_facade_result_id is not None and not obj.source_facade_result_id:
        return False
    if obj.source_projection_id is not None and not obj.source_projection_id:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_projection_visibility_metadata_keys(
            obj.metadata, "metadata", InvalidProjectionVisibilitySourceRefError,
        )
    except InvalidProjectionVisibilitySourceRefError:
        return False
    return True


def validate_projection_visibility_descriptor(obj: Any) -> bool:
    if not isinstance(obj, ProjectionVisibilityDescriptor):
        return False
    if obj.visibility_tier not in PROJECTION_VISIBILITY_TIERS:
        return False
    if obj.packet_kind not in PROJECTION_PACKET_KINDS:
        return False
    if obj.redaction_reason not in PROJECTION_REDACTION_REASONS:
        return False
    if not isinstance(obj.redaction_required, bool):
        return False
    if not isinstance(obj.safe_reference_ids, tuple):
        return False
    for i, ref_id in enumerate(obj.safe_reference_ids):
        if not isinstance(ref_id, str) or not ref_id:
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_projection_visibility_metadata_keys(
            obj.metadata, "metadata", InvalidProjectionVisibilityDescriptorError,
        )
    except InvalidProjectionVisibilityDescriptorError:
        return False
    return True


def validate_projection_visibility_adapter_packet(obj: Any) -> bool:
    if not isinstance(obj, ProjectionVisibilityAdapterPacket):
        return False
    if obj.adapter_status not in PROJECTION_VISIBILITY_ADAPTER_STATUSES:
        return False
    if obj.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
        return False
    if obj.entity_kind not in VERTICAL_SLICE_ENTITY_KINDS:
        return False
    if obj.packet_kind not in PROJECTION_PACKET_KINDS:
        return False
    if obj.downstream_consumer_type not in PROJECTION_DOWNSTREAM_CONSUMER_TYPES:
        return False
    if not validate_projection_visibility_source_ref(obj.source_reference):
        return False
    if not validate_projection_visibility_descriptor(obj.visibility_descriptor):
        return False
    if not validate_projection_visibility_authority_flags(obj.authority_flags):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_projection_visibility_metadata_keys(
            obj.metadata, "metadata", InvalidProjectionVisibilityAdapterPacketError,
        )
    except InvalidProjectionVisibilityAdapterPacketError:
        return False
    return True


def validate_projection_visibility_adapter_result(obj: Any) -> bool:
    if not isinstance(obj, ProjectionVisibilityAdapterResult):
        return False
    if obj.adapter_status not in PROJECTION_VISIBILITY_ADAPTER_STATUSES:
        return False
    if not isinstance(obj.packets, tuple) or not obj.packets:
        return False
    for packet in obj.packets:
        if not validate_projection_visibility_adapter_packet(packet):
            return False
    if not validate_projection_visibility_authority_flags(obj.authority_flags):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_projection_visibility_metadata_keys(
            obj.metadata, "metadata", InvalidProjectionVisibilityAdapterResultError,
        )
    except InvalidProjectionVisibilityAdapterResultError:
        return False
    return True
