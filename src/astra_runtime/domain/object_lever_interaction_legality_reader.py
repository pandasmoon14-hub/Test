"""Object/Lever Interaction Legality Reader — RT-002C.

RUNTIME-DOMAIN-RT-002C: implements a narrow, non-executing action legality
reader for exactly one command family:

    interact_with_object_lever

It consumes visibility-classified projection packets produced by RT-002B and
produces a bounded legality classification. It does not read raw state, receive
hidden truth, infer hidden truth from absence, execute the command, generate a
transaction preview, mutate state, or commit an event.

This module is intentionally narrow:
* one command family only
* projection packet intake from RT-002B
* required projection presence checks
* visibility/redaction-aware legality classification
* non-executing legality result envelope
* deterministic serializers
* visible serializer with strict redaction
* validation helpers
* hidden/raw-state metadata containment

It does NOT implement:
* command execution
* action resolution
* state mutation
* event append or event commitment
* transaction preview materialization
* persistence/replay writes
* RNG/table/oracle execution
* resource/consequence math execution
* combat/ability/skill/effect resolution
* general action legality service behavior
* general command parser
* general object interaction engine
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

from astra_runtime.domain.projection_visibility_adapter_v0_1 import (
    FORBIDDEN_PROJECTION_VISIBILITY_METADATA_KEYS,
    PROJECTION_PACKET_KINDS,
    PROJECTION_VISIBILITY_ADAPTER_STATUSES,
    VERTICAL_SLICE_OWNER_FAMILIES,
    ProjectionVisibilityAdapterPacket,
    ProjectionVisibilityAuthorityFlags,
)


__all__ = [
    # Constants
    "OBJECT_LEVER_COMMAND_FAMILY",
    "OBJECT_LEVER_LEGALITY_READER_STATUSES",
    "OBJECT_LEVER_LEGALITY_DECISIONS",
    "OBJECT_LEVER_REQUIRED_ENTITY_KINDS",
    "OBJECT_LEVER_OPTIONAL_ENTITY_KINDS",
    "OBJECT_LEVER_REQUIRED_OWNER_FAMILIES",
    "OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES",
    "OBJECT_LEVER_BLOCK_REASONS",
    "OBJECT_LEVER_NON_AUTHORITY_NOTE",
    "FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS",
    # Error hierarchy
    "ObjectLeverInteractionLegalityReaderError",
    "InvalidObjectLeverInteractionLegalityAuthorityFlagsError",
    "InvalidObjectLeverInteractionCommandDeclarationError",
    "InvalidObjectLeverProjectionRequirementError",
    "InvalidObjectLeverLegalityInputPacketSetError",
    "InvalidObjectLeverLegalityReadingError",
    "InvalidObjectLeverLegalityReaderResultError",
    # Dataclasses
    "ObjectLeverInteractionLegalityAuthorityFlags",
    "ObjectLeverInteractionCommandDeclaration",
    "ObjectLeverProjectionRequirement",
    "ObjectLeverLegalityInputPacketSet",
    "ObjectLeverLegalityReading",
    "ObjectLeverLegalityReaderResult",
    # Factories
    "create_object_lever_interaction_legality_authority_flags",
    "create_object_lever_interaction_command_declaration",
    "create_object_lever_projection_requirement",
    "create_object_lever_legality_input_packet_set",
    "create_object_lever_legality_reading",
    "create_object_lever_legality_reader_result",
    # Reader helpers
    "build_object_lever_projection_requirements",
    "read_object_lever_interaction_legality",
    "serialize_object_lever_legality_reading",
    "serialize_object_lever_legality_reading_visible",
    "serialize_object_lever_legality_reader_result",
    "serialize_object_lever_legality_reader_result_visible",
    # Validators
    "validate_object_lever_interaction_legality_authority_flags",
    "validate_object_lever_interaction_command_declaration",
    "validate_object_lever_projection_requirement",
    "validate_object_lever_legality_input_packet_set",
    "validate_object_lever_legality_reading",
    "validate_object_lever_legality_reader_result",
]


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OBJECT_LEVER_COMMAND_FAMILY = "interact_with_object_lever"

OBJECT_LEVER_LEGALITY_READER_STATUSES = frozenset({
    "legality_read_available",
    "blocked_by_projection",
    "blocked_by_visibility",
    "deferred",
    "unknown",
    "insufficient_projection",
})

OBJECT_LEVER_LEGALITY_DECISIONS = frozenset({
    "permitted_for_preview",
    "blocked",
    "deferred",
    "unknown",
    "insufficient_projection",
})

OBJECT_LEVER_REQUIRED_ENTITY_KINDS = frozenset({
    "scene",
    "actor",
    "object_lever",
})

OBJECT_LEVER_OPTIONAL_ENTITY_KINDS = frozenset({
    "npc_target",
    "hazard_clock",
    "visible_condition",
    "hidden_fact_reference",
})

OBJECT_LEVER_REQUIRED_OWNER_FAMILIES = frozenset({
    "scene_location_owner",
    "actor_identity_owner",
    "object_interactable_owner",
})

OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES = frozenset({
    "available",
    "available_backend_only",
    "missing",
    "redacted",
    "unavailable",
    "deferred",
    "unknown",
})

OBJECT_LEVER_BLOCK_REASONS = frozenset({
    "missing_scene_projection",
    "missing_actor_projection",
    "missing_object_lever_projection",
    "unavailable_scene_projection",
    "unavailable_actor_projection",
    "unavailable_object_lever_projection",
    "redacted_required_projection",
    "backend_only_required_projection",
    "invalid_command_family",
    "hidden_information_not_available",
    "insufficient_projection",
    "unknown_projection_state",
    "deferred_projection_state",
})

OBJECT_LEVER_NON_AUTHORITY_NOTE = (
    "This object/lever interaction legality reader is reference-only and "
    "authorizes no command execution, no transaction preview materialization, "
    "no state mutation, no event append or commitment, no persistence or "
    "replay writes, no RNG/table/oracle execution, no resource or consequence "
    "math execution, no combat/ability/skill/effect resolution, no model "
    "calls, no prompt rendering, no narration generation, no live-play or "
    "UI behavior, no conversion, no sourcebook inclusion, and no canon "
    "promotion. A 'permitted_for_preview' decision means only that the "
    "command may proceed to RT-002D transaction preview construction; it does "
    "not execute the command, authorize mutation, or commit an event."
)

FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS = frozenset({
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
    "transaction_preview",
    "event_commitment",
    "state_delta",
    "mutation_payload",
    "execution_result",
})


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------


class ObjectLeverInteractionLegalityReaderError(ValueError):
    """Base error for RT-002C object lever interaction legality reader."""


class InvalidObjectLeverInteractionLegalityAuthorityFlagsError(
    ObjectLeverInteractionLegalityReaderError,
):
    """Raised when authority flags contain a non-False value."""


class InvalidObjectLeverInteractionCommandDeclarationError(
    ObjectLeverInteractionLegalityReaderError,
):
    """Raised when a command declaration fails validation."""


class InvalidObjectLeverProjectionRequirementError(
    ObjectLeverInteractionLegalityReaderError,
):
    """Raised when a projection requirement fails validation."""


class InvalidObjectLeverLegalityInputPacketSetError(
    ObjectLeverInteractionLegalityReaderError,
):
    """Raised when an input packet set fails validation."""


class InvalidObjectLeverLegalityReadingError(
    ObjectLeverInteractionLegalityReaderError,
):
    """Raised when a legality reading fails validation."""


class InvalidObjectLeverLegalityReaderResultError(
    ObjectLeverInteractionLegalityReaderError,
):
    """Raised when a legality reader result fails validation."""


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


def _validate_no_forbidden_object_lever_legality_metadata_keys(
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
            if k in FORBIDDEN_OBJECT_LEVER_LEGALITY_METADATA_KEYS:
                raise error_cls(
                    f"metadata key {k!r} at {path} is forbidden: "
                    f"object lever legality metadata must not carry hidden, "
                    f"raw-state, execution, preview, or event data"
                )
            _validate_no_forbidden_object_lever_legality_metadata_keys(
                v, f"{path}.{k}", error_cls,
            )
    elif isinstance(value, (list, tuple)):
        for i, item in enumerate(value):
            _validate_no_forbidden_object_lever_legality_metadata_keys(
                item, f"{path}[{i}]", error_cls,
            )


def _safe_object_lever_legality_metadata(
    metadata: Mapping[str, Any] | None, error_cls: type[Exception],
) -> Mapping[str, Any]:
    """JSON-safe metadata that also recursively rejects forbidden keys."""
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    _validate_no_forbidden_object_lever_legality_metadata_keys(
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
class ObjectLeverInteractionLegalityAuthorityFlags:
    """All authority flags must be false-only. Any non-False value raises during
    construction."""

    raw_state_access_authorized: bool = False
    hidden_information_disclosure_authorized: bool = False
    command_execution_authorized: bool = False
    transaction_preview_authorized: bool = False
    state_mutation_authorized: bool = False
    event_append_authorized: bool = False
    event_commitment_authorized: bool = False
    persistence_write_authorized: bool = False
    replay_write_authorized: bool = False
    rng_execution_authorized: bool = False
    resource_math_execution_authorized: bool = False
    combat_resolution_authorized: bool = False
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
                raise InvalidObjectLeverInteractionLegalityAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in "
                    f"RT-002C legality reader, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class ObjectLeverInteractionCommandDeclaration:
    """Narrow command declaration for interact_with_object_lever.

    Carries IDs only. Contains no natural-language parsing output, no effect
    description, and no execution arguments.
    """

    command_id: str
    command_family: str
    actor_ref_id: str
    object_lever_ref_id: str
    scene_ref_id: str
    declared_intent_label: str | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.command_id, "command_id",
            InvalidObjectLeverInteractionCommandDeclarationError,
        )
        _validate_non_empty_str(
            self.command_family, "command_family",
            InvalidObjectLeverInteractionCommandDeclarationError,
        )
        if self.command_family != OBJECT_LEVER_COMMAND_FAMILY:
            raise InvalidObjectLeverInteractionCommandDeclarationError(
                f"command_family must be {OBJECT_LEVER_COMMAND_FAMILY!r}, "
                f"got {self.command_family!r}"
            )
        _validate_non_empty_str(
            self.actor_ref_id, "actor_ref_id",
            InvalidObjectLeverInteractionCommandDeclarationError,
        )
        _validate_non_empty_str(
            self.object_lever_ref_id, "object_lever_ref_id",
            InvalidObjectLeverInteractionCommandDeclarationError,
        )
        _validate_non_empty_str(
            self.scene_ref_id, "scene_ref_id",
            InvalidObjectLeverInteractionCommandDeclarationError,
        )
        if self.declared_intent_label is not None:
            _validate_non_empty_str(
                self.declared_intent_label, "declared_intent_label",
                InvalidObjectLeverInteractionCommandDeclarationError,
            )
        object.__setattr__(
            self, "metadata",
            _safe_object_lever_legality_metadata(
                self.metadata, InvalidObjectLeverInteractionCommandDeclarationError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "command_family": self.command_family,
            "actor_ref_id": self.actor_ref_id,
            "object_lever_ref_id": self.object_lever_ref_id,
            "scene_ref_id": self.scene_ref_id,
            "declared_intent_label": self.declared_intent_label,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ObjectLeverProjectionRequirement:
    """A single projection requirement reading for an entity kind.

    Contains no raw state, no hidden fact payload, and no execution data.
    """

    entity_kind: str
    owner_family: str
    required: bool
    requirement_status: str
    safe_reference_ids: tuple[str, ...] = ()
    block_reason: str | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.entity_kind, "entity_kind",
            InvalidObjectLeverProjectionRequirementError,
        )
        if self.entity_kind not in (
            OBJECT_LEVER_REQUIRED_ENTITY_KINDS | OBJECT_LEVER_OPTIONAL_ENTITY_KINDS
        ):
            raise InvalidObjectLeverProjectionRequirementError(
                f"entity_kind must be one of "
                f"{sorted(OBJECT_LEVER_REQUIRED_ENTITY_KINDS | OBJECT_LEVER_OPTIONAL_ENTITY_KINDS)}, "
                f"got {self.entity_kind!r}"
            )
        _validate_non_empty_str(
            self.owner_family, "owner_family",
            InvalidObjectLeverProjectionRequirementError,
        )
        if self.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
            raise InvalidObjectLeverProjectionRequirementError(
                f"owner_family must be one of "
                f"{sorted(VERTICAL_SLICE_OWNER_FAMILIES)}, "
                f"got {self.owner_family!r}"
            )
        if not isinstance(self.required, bool):
            raise InvalidObjectLeverProjectionRequirementError(
                f"required must be a bool, got {self.required!r}"
            )
        _validate_non_empty_str(
            self.requirement_status, "requirement_status",
            InvalidObjectLeverProjectionRequirementError,
        )
        if self.requirement_status not in OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES:
            raise InvalidObjectLeverProjectionRequirementError(
                f"requirement_status must be one of "
                f"{sorted(OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES)}, "
                f"got {self.requirement_status!r}"
            )
        object.__setattr__(
            self, "safe_reference_ids",
            _safe_str_tuple(
                self.safe_reference_ids, "safe_reference_ids",
                InvalidObjectLeverProjectionRequirementError,
            ),
        )
        if self.block_reason is not None:
            _validate_non_empty_str(
                self.block_reason, "block_reason",
                InvalidObjectLeverProjectionRequirementError,
            )
            if self.block_reason not in OBJECT_LEVER_BLOCK_REASONS:
                raise InvalidObjectLeverProjectionRequirementError(
                    f"block_reason must be one of "
                    f"{sorted(OBJECT_LEVER_BLOCK_REASONS)}, "
                    f"got {self.block_reason!r}"
                )
        object.__setattr__(
            self, "metadata",
            _safe_object_lever_legality_metadata(
                self.metadata, InvalidObjectLeverProjectionRequirementError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_kind": self.entity_kind,
            "owner_family": self.owner_family,
            "required": self.required,
            "requirement_status": self.requirement_status,
            "safe_reference_ids": list(self.safe_reference_ids),
            "block_reason": self.block_reason,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ObjectLeverLegalityInputPacketSet:
    """Input packet set for the legality reader.

    Contains RT-002B projection packets only. No RT-002A raw records, no raw
    state, and no hidden fact payload.
    """

    packet_set_id: str
    command_declaration: ObjectLeverInteractionCommandDeclaration
    projection_packets: tuple[ProjectionVisibilityAdapterPacket, ...]
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.packet_set_id, "packet_set_id",
            InvalidObjectLeverLegalityInputPacketSetError,
        )
        if not isinstance(self.command_declaration, ObjectLeverInteractionCommandDeclaration):
            raise InvalidObjectLeverLegalityInputPacketSetError(
                f"command_declaration must be an ObjectLeverInteractionCommandDeclaration, "
                f"got {type(self.command_declaration).__name__}"
            )
        if not isinstance(self.projection_packets, tuple):
            raise InvalidObjectLeverLegalityInputPacketSetError(
                "projection_packets must be a tuple of ProjectionVisibilityAdapterPacket"
            )
        for i, packet in enumerate(self.projection_packets):
            if not isinstance(packet, ProjectionVisibilityAdapterPacket):
                raise InvalidObjectLeverLegalityInputPacketSetError(
                    f"projection_packets[{i}] must be a ProjectionVisibilityAdapterPacket, "
                    f"got {type(packet).__name__}"
                )
        object.__setattr__(
            self, "metadata",
            _safe_object_lever_legality_metadata(
                self.metadata, InvalidObjectLeverLegalityInputPacketSetError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_set_id": self.packet_set_id,
            "command_declaration": self.command_declaration.to_dict(),
            "projection_packets": [
                packet.to_dict() for packet in self.projection_packets
            ],
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ObjectLeverLegalityReading:
    """A single non-executing legality reading.

    Contains no command execution fields, no transaction preview fields, no
    event commitment fields, no mutation/state-delta fields, and no model
    prompt/narration fields.
    """

    reading_id: str
    reader_status: str
    legality_decision: str
    command_family: str
    requirement_readings: tuple[ObjectLeverProjectionRequirement, ...]
    block_reasons: tuple[str, ...] = ()
    safe_reference_ids: tuple[str, ...] = ()
    non_authority_note: str = OBJECT_LEVER_NON_AUTHORITY_NOTE
    authority_flags: ObjectLeverInteractionLegalityAuthorityFlags = field(
        default_factory=ObjectLeverInteractionLegalityAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.reading_id, "reading_id",
            InvalidObjectLeverLegalityReadingError,
        )
        _validate_non_empty_str(
            self.reader_status, "reader_status",
            InvalidObjectLeverLegalityReadingError,
        )
        if self.reader_status not in OBJECT_LEVER_LEGALITY_READER_STATUSES:
            raise InvalidObjectLeverLegalityReadingError(
                f"reader_status must be one of "
                f"{sorted(OBJECT_LEVER_LEGALITY_READER_STATUSES)}, "
                f"got {self.reader_status!r}"
            )
        _validate_non_empty_str(
            self.legality_decision, "legality_decision",
            InvalidObjectLeverLegalityReadingError,
        )
        if self.legality_decision not in OBJECT_LEVER_LEGALITY_DECISIONS:
            raise InvalidObjectLeverLegalityReadingError(
                f"legality_decision must be one of "
                f"{sorted(OBJECT_LEVER_LEGALITY_DECISIONS)}, "
                f"got {self.legality_decision!r}"
            )
        _validate_non_empty_str(
            self.command_family, "command_family",
            InvalidObjectLeverLegalityReadingError,
        )
        if self.command_family != OBJECT_LEVER_COMMAND_FAMILY:
            raise InvalidObjectLeverLegalityReadingError(
                f"command_family must be {OBJECT_LEVER_COMMAND_FAMILY!r}, "
                f"got {self.command_family!r}"
            )
        if not isinstance(self.requirement_readings, tuple):
            raise InvalidObjectLeverLegalityReadingError(
                "requirement_readings must be a tuple of ObjectLeverProjectionRequirement"
            )
        for i, req in enumerate(self.requirement_readings):
            if not isinstance(req, ObjectLeverProjectionRequirement):
                raise InvalidObjectLeverLegalityReadingError(
                    f"requirement_readings[{i}] must be an ObjectLeverProjectionRequirement, "
                    f"got {type(req).__name__}"
                )
        object.__setattr__(
            self, "block_reasons",
            _safe_str_tuple(
                self.block_reasons, "block_reasons",
                InvalidObjectLeverLegalityReadingError,
            ),
        )
        for reason in self.block_reasons:
            if reason not in OBJECT_LEVER_BLOCK_REASONS:
                raise InvalidObjectLeverLegalityReadingError(
                    f"block_reason {reason!r} is not a valid block reason"
                )
        object.__setattr__(
            self, "safe_reference_ids",
            _safe_str_tuple(
                self.safe_reference_ids, "safe_reference_ids",
                InvalidObjectLeverLegalityReadingError,
            ),
        )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidObjectLeverLegalityReadingError,
        )
        if not isinstance(self.authority_flags, ObjectLeverInteractionLegalityAuthorityFlags):
            raise InvalidObjectLeverLegalityReadingError(
                f"authority_flags must be an ObjectLeverInteractionLegalityAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_object_lever_legality_metadata(
                self.metadata, InvalidObjectLeverLegalityReadingError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "reading_id": self.reading_id,
            "reader_status": self.reader_status,
            "legality_decision": self.legality_decision,
            "command_family": self.command_family,
            "requirement_readings": [
                req.to_dict() for req in self.requirement_readings
            ],
            "block_reasons": list(self.block_reasons),
            "safe_reference_ids": list(self.safe_reference_ids),
            "non_authority_note": self.non_authority_note,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ObjectLeverLegalityReaderResult:
    """Result envelope for the object/lever interaction legality reader.

    Non-executing. Contains no transaction preview, event commitment, state
    mutation, or execution data.
    """

    result_id: str
    reader_status: str
    legality_decision: str
    legality_reading: ObjectLeverLegalityReading
    non_authority_note: str = OBJECT_LEVER_NON_AUTHORITY_NOTE
    authority_flags: ObjectLeverInteractionLegalityAuthorityFlags = field(
        default_factory=ObjectLeverInteractionLegalityAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.result_id, "result_id",
            InvalidObjectLeverLegalityReaderResultError,
        )
        _validate_non_empty_str(
            self.reader_status, "reader_status",
            InvalidObjectLeverLegalityReaderResultError,
        )
        if self.reader_status not in OBJECT_LEVER_LEGALITY_READER_STATUSES:
            raise InvalidObjectLeverLegalityReaderResultError(
                f"reader_status must be one of "
                f"{sorted(OBJECT_LEVER_LEGALITY_READER_STATUSES)}, "
                f"got {self.reader_status!r}"
            )
        _validate_non_empty_str(
            self.legality_decision, "legality_decision",
            InvalidObjectLeverLegalityReaderResultError,
        )
        if self.legality_decision not in OBJECT_LEVER_LEGALITY_DECISIONS:
            raise InvalidObjectLeverLegalityReaderResultError(
                f"legality_decision must be one of "
                f"{sorted(OBJECT_LEVER_LEGALITY_DECISIONS)}, "
                f"got {self.legality_decision!r}"
            )
        if not isinstance(self.legality_reading, ObjectLeverLegalityReading):
            raise InvalidObjectLeverLegalityReaderResultError(
                f"legality_reading must be an ObjectLeverLegalityReading, "
                f"got {type(self.legality_reading).__name__}"
            )
        _validate_non_empty_str(
            self.non_authority_note, "non_authority_note",
            InvalidObjectLeverLegalityReaderResultError,
        )
        if not isinstance(self.authority_flags, ObjectLeverInteractionLegalityAuthorityFlags):
            raise InvalidObjectLeverLegalityReaderResultError(
                f"authority_flags must be an ObjectLeverInteractionLegalityAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_object_lever_legality_metadata(
                self.metadata, InvalidObjectLeverLegalityReaderResultError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "reader_status": self.reader_status,
            "legality_decision": self.legality_decision,
            "legality_reading": self.legality_reading.to_dict(),
            "non_authority_note": self.non_authority_note,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_object_lever_interaction_legality_authority_flags() -> ObjectLeverInteractionLegalityAuthorityFlags:
    return ObjectLeverInteractionLegalityAuthorityFlags()


def create_object_lever_interaction_command_declaration(
    *,
    command_id: str,
    command_family: str,
    actor_ref_id: str,
    object_lever_ref_id: str,
    scene_ref_id: str,
    declared_intent_label: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ObjectLeverInteractionCommandDeclaration:
    return ObjectLeverInteractionCommandDeclaration(
        command_id=command_id,
        command_family=command_family,
        actor_ref_id=actor_ref_id,
        object_lever_ref_id=object_lever_ref_id,
        scene_ref_id=scene_ref_id,
        declared_intent_label=declared_intent_label,
        metadata=metadata,
    )


def create_object_lever_projection_requirement(
    *,
    entity_kind: str,
    owner_family: str,
    required: bool,
    requirement_status: str,
    safe_reference_ids: Sequence[str] | None = None,
    block_reason: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ObjectLeverProjectionRequirement:
    return ObjectLeverProjectionRequirement(
        entity_kind=entity_kind,
        owner_family=owner_family,
        required=required,
        requirement_status=requirement_status,
        safe_reference_ids=safe_reference_ids,
        block_reason=block_reason,
        metadata=metadata,
    )


def create_object_lever_legality_input_packet_set(
    *,
    packet_set_id: str,
    command_declaration: ObjectLeverInteractionCommandDeclaration,
    projection_packets: Sequence[ProjectionVisibilityAdapterPacket],
    metadata: Mapping[str, Any] | None = None,
) -> ObjectLeverLegalityInputPacketSet:
    return ObjectLeverLegalityInputPacketSet(
        packet_set_id=packet_set_id,
        command_declaration=command_declaration,
        projection_packets=tuple(projection_packets),
        metadata=metadata,
    )


def create_object_lever_legality_reading(
    *,
    reading_id: str,
    reader_status: str,
    legality_decision: str,
    command_family: str,
    requirement_readings: Sequence[ObjectLeverProjectionRequirement],
    block_reasons: Sequence[str] | None = None,
    safe_reference_ids: Sequence[str] | None = None,
    non_authority_note: str = OBJECT_LEVER_NON_AUTHORITY_NOTE,
    authority_flags: ObjectLeverInteractionLegalityAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ObjectLeverLegalityReading:
    return ObjectLeverLegalityReading(
        reading_id=reading_id,
        reader_status=reader_status,
        legality_decision=legality_decision,
        command_family=command_family,
        requirement_readings=tuple(requirement_readings),
        block_reasons=block_reasons,
        safe_reference_ids=safe_reference_ids,
        non_authority_note=non_authority_note,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ObjectLeverInteractionLegalityAuthorityFlags()
        ),
        metadata=metadata,
    )


def create_object_lever_legality_reader_result(
    *,
    result_id: str,
    reader_status: str,
    legality_decision: str,
    legality_reading: ObjectLeverLegalityReading,
    non_authority_note: str = OBJECT_LEVER_NON_AUTHORITY_NOTE,
    authority_flags: ObjectLeverInteractionLegalityAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ObjectLeverLegalityReaderResult:
    return ObjectLeverLegalityReaderResult(
        result_id=result_id,
        reader_status=reader_status,
        legality_decision=legality_decision,
        legality_reading=legality_reading,
        non_authority_note=non_authority_note,
        authority_flags=(
            authority_flags
            if authority_flags is not None
            else ObjectLeverInteractionLegalityAuthorityFlags()
        ),
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Reader helpers
# ---------------------------------------------------------------------------


_ENTITY_TO_OWNER_FAMILY = {
    "scene": "scene_location_owner",
    "actor": "actor_identity_owner",
    "object_lever": "object_interactable_owner",
    "npc_target": "target_reachability_owner",
    "hazard_clock": "hazard_environment_owner",
    "visible_condition": "condition_status_owner",
    "hidden_fact_reference": "hidden_information_visibility_owner",
}

_BLOCK_REASON_FOR_MISSING = {
    "scene": "missing_scene_projection",
    "actor": "missing_actor_projection",
    "object_lever": "missing_object_lever_projection",
}

_BLOCK_REASON_FOR_UNAVAILABLE = {
    "scene": "unavailable_scene_projection",
    "actor": "unavailable_actor_projection",
    "object_lever": "unavailable_object_lever_projection",
}


def build_object_lever_projection_requirements(
    projection_packets: Sequence[ProjectionVisibilityAdapterPacket],
) -> tuple[ObjectLeverProjectionRequirement, ...]:
    """Build requirement readings for all known entity kinds.

    Required entity kinds (scene, actor, object_lever) are classified strictly.
    Optional entity kinds are recorded but never block.
    """
    packets_by_entity: dict[str, ProjectionVisibilityAdapterPacket] = {}
    for packet in projection_packets:
        entity_kind = packet.entity_kind
        # Keep the first packet for each entity kind. RT-002C assumes one packet
        # per entity kind in this narrow vertical slice.
        if entity_kind not in packets_by_entity:
            packets_by_entity[entity_kind] = packet

    requirements: list[ObjectLeverProjectionRequirement] = []
    all_entity_kinds = (
        OBJECT_LEVER_REQUIRED_ENTITY_KINDS | OBJECT_LEVER_OPTIONAL_ENTITY_KINDS
    )

    for entity_kind in sorted(all_entity_kinds):
        required = entity_kind in OBJECT_LEVER_REQUIRED_ENTITY_KINDS
        owner_family = _ENTITY_TO_OWNER_FAMILY[entity_kind]
        packet = packets_by_entity.get(entity_kind)

        if packet is None:
            req = create_object_lever_projection_requirement(
                entity_kind=entity_kind,
                owner_family=owner_family,
                required=required,
                requirement_status="missing",
                block_reason=(_BLOCK_REASON_FOR_MISSING.get(entity_kind) if required else None),
            )
        else:
            safe_ids = list(packet.visibility_descriptor.safe_reference_ids)
            packet_kind = packet.packet_kind

            if packet_kind == "visible_safe_projection":
                req = create_object_lever_projection_requirement(
                    entity_kind=entity_kind,
                    owner_family=owner_family,
                    required=required,
                    requirement_status="available",
                    safe_reference_ids=safe_ids,
                )
            elif packet_kind == "backend_safe_projection":
                req = create_object_lever_projection_requirement(
                    entity_kind=entity_kind,
                    owner_family=owner_family,
                    required=required,
                    requirement_status="available_backend_only",
                    safe_reference_ids=safe_ids,
                    block_reason=("backend_only_required_projection" if required else None),
                )
            elif packet_kind == "redacted_projection":
                req = create_object_lever_projection_requirement(
                    entity_kind=entity_kind,
                    owner_family=owner_family,
                    required=required,
                    requirement_status="redacted",
                    safe_reference_ids=safe_ids,
                    block_reason=("redacted_required_projection" if required else None),
                )
            elif packet_kind == "unavailable_projection":
                req = create_object_lever_projection_requirement(
                    entity_kind=entity_kind,
                    owner_family=owner_family,
                    required=required,
                    requirement_status="unavailable",
                    safe_reference_ids=safe_ids,
                    block_reason=(_BLOCK_REASON_FOR_UNAVAILABLE.get(entity_kind) if required else None),
                )
            elif packet_kind == "deferred_projection":
                req = create_object_lever_projection_requirement(
                    entity_kind=entity_kind,
                    owner_family=owner_family,
                    required=required,
                    requirement_status="deferred",
                    safe_reference_ids=safe_ids,
                    block_reason=("deferred_projection_state" if required else None),
                )
            elif packet_kind == "unknown_projection":
                req = create_object_lever_projection_requirement(
                    entity_kind=entity_kind,
                    owner_family=owner_family,
                    required=required,
                    requirement_status="unknown",
                    safe_reference_ids=safe_ids,
                    block_reason=("unknown_projection_state" if required else None),
                )
            else:
                # Defensive fallback; packet_kind validation in RT-002B should
                # prevent reaching here.
                req = create_object_lever_projection_requirement(
                    entity_kind=entity_kind,
                    owner_family=owner_family,
                    required=required,
                    requirement_status="unknown",
                    safe_reference_ids=safe_ids,
                    block_reason=("unknown_projection_state" if required else None),
                )

        requirements.append(req)

    return tuple(requirements)


def _derive_decision_and_status(
    requirements: Sequence[ObjectLeverProjectionRequirement],
) -> tuple[str, str]:
    """Derive (reader_status, legality_decision) from requirement readings.

    Precedence (most conservative first):
        blocked_by_visibility > blocked_by_projection > insufficient_projection
        > unknown > deferred > legality_read_available
    """
    has_redacted_required = False
    has_blocked_required = False
    has_insufficient_required = False
    has_unknown_required = False
    has_deferred_required = False
    has_available_visible_required = True

    for req in requirements:
        if not req.required:
            continue
        status = req.requirement_status
        reason = req.block_reason

        if status == "available":
            continue
        has_available_visible_required = False
        if status == "missing":
            has_insufficient_required = True
        elif status == "unavailable" or status == "available_backend_only":
            has_blocked_required = True
        elif status == "redacted":
            has_redacted_required = True
        elif status == "deferred":
            has_deferred_required = True
        elif status == "unknown":
            has_unknown_required = True
        # Unknown statuses fall through conservatively.
        elif reason is not None:
            has_blocked_required = True
        else:
            has_unknown_required = True

    if has_redacted_required:
        return ("blocked_by_visibility", "blocked")
    if has_blocked_required:
        return ("blocked_by_projection", "blocked")
    if has_insufficient_required:
        return ("insufficient_projection", "insufficient_projection")
    if has_unknown_required:
        return ("unknown", "unknown")
    if has_deferred_required:
        return ("deferred", "deferred")
    if has_available_visible_required:
        return ("legality_read_available", "permitted_for_preview")
    # Defensive fallback.
    return ("unknown", "unknown")


def _collect_block_reasons(
    requirements: Sequence[ObjectLeverProjectionRequirement],
) -> tuple[str, ...]:
    reasons: list[str] = []
    for req in requirements:
        if req.required and req.block_reason is not None:
            reasons.append(req.block_reason)
    return tuple(reasons)


def _collect_safe_reference_ids(
    command_declaration: ObjectLeverInteractionCommandDeclaration,
    requirements: Sequence[ObjectLeverProjectionRequirement],
) -> tuple[str, ...]:
    """Collect safe reference IDs from declarations and available required packets."""
    safe_ids: list[str] = []
    safe_ids.append(command_declaration.scene_ref_id)
    safe_ids.append(command_declaration.actor_ref_id)
    safe_ids.append(command_declaration.object_lever_ref_id)
    for req in requirements:
        if req.required and req.requirement_status in ("available", "available_backend_only"):
            for ref_id in req.safe_reference_ids:
                if ref_id not in safe_ids:
                    safe_ids.append(ref_id)
    return tuple(safe_ids)


def read_object_lever_interaction_legality(
    packet_set: ObjectLeverLegalityInputPacketSet,
    *,
    reading_id: str,
    result_id: str,
) -> ObjectLeverLegalityReaderResult:
    """Read legality for an object/lever interaction from RT-002B packets.

    Does not execute the command, generate a transaction preview, mutate state,
    or commit an event.
    """
    if not isinstance(packet_set, ObjectLeverLegalityInputPacketSet):
        raise InvalidObjectLeverLegalityReaderResultError(
            f"packet_set must be an ObjectLeverLegalityInputPacketSet, "
            f"got {type(packet_set).__name__}"
        )

    command_declaration = packet_set.command_declaration

    # If command family is not the one supported by this reader, block.
    if command_declaration.command_family != OBJECT_LEVER_COMMAND_FAMILY:
        invalid_req = create_object_lever_projection_requirement(
            entity_kind="object_lever",
            owner_family="object_interactable_owner",
            required=True,
            requirement_status="missing",
            block_reason="invalid_command_family",
        )
        reading = create_object_lever_legality_reading(
            reading_id=reading_id,
            reader_status="blocked_by_projection",
            legality_decision="blocked",
            command_family=OBJECT_LEVER_COMMAND_FAMILY,
            requirement_readings=(invalid_req,),
            block_reasons=("invalid_command_family",),
            safe_reference_ids=(
                command_declaration.scene_ref_id,
                command_declaration.actor_ref_id,
                command_declaration.object_lever_ref_id,
            ),
        )
        return create_object_lever_legality_reader_result(
            result_id=result_id,
            reader_status="blocked_by_projection",
            legality_decision="blocked",
            legality_reading=reading,
        )

    requirements = build_object_lever_projection_requirements(
        packet_set.projection_packets,
    )
    reader_status, legality_decision = _derive_decision_and_status(requirements)
    block_reasons = _collect_block_reasons(requirements)
    safe_reference_ids = _collect_safe_reference_ids(command_declaration, requirements)

    reading = create_object_lever_legality_reading(
        reading_id=reading_id,
        reader_status=reader_status,
        legality_decision=legality_decision,
        command_family=OBJECT_LEVER_COMMAND_FAMILY,
        requirement_readings=requirements,
        block_reasons=block_reasons,
        safe_reference_ids=safe_reference_ids,
    )
    return create_object_lever_legality_reader_result(
        result_id=result_id,
        reader_status=reader_status,
        legality_decision=legality_decision,
        legality_reading=reading,
    )


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------


def serialize_object_lever_legality_reading(
    reading: ObjectLeverLegalityReading,
) -> dict[str, Any]:
    """Full backend serializer. Deterministic, JSON-safe."""
    return reading.to_dict()


def serialize_object_lever_legality_reading_visible(
    reading: ObjectLeverLegalityReading,
) -> dict[str, Any]:
    """Visible serializer. Excludes metadata, authority flags, backend-only
    requirement details, and implementation internals."""
    return {
        "reading_id": reading.reading_id,
        "reader_status": reading.reader_status,
        "legality_decision": reading.legality_decision,
        "command_family": reading.command_family,
        "requirement_readings": [
            {
                "entity_kind": req.entity_kind,
                "required": req.required,
                "requirement_status": req.requirement_status,
                "safe_reference_ids": list(req.safe_reference_ids),
                "block_reason": req.block_reason,
            }
            for req in reading.requirement_readings
        ],
        "block_reasons": list(reading.block_reasons),
        "safe_reference_ids": list(reading.safe_reference_ids),
        "non_authority_note": reading.non_authority_note,
    }


def serialize_object_lever_legality_reader_result(
    result: ObjectLeverLegalityReaderResult,
) -> dict[str, Any]:
    """Full backend serializer. Deterministic, JSON-safe."""
    return result.to_dict()


def serialize_object_lever_legality_reader_result_visible(
    result: ObjectLeverLegalityReaderResult,
) -> dict[str, Any]:
    """Visible serializer. Excludes metadata, authority flags, and backend-only
    fields."""
    return {
        "result_id": result.result_id,
        "reader_status": result.reader_status,
        "legality_decision": result.legality_decision,
        "legality_reading": serialize_object_lever_legality_reading_visible(
            result.legality_reading,
        ),
        "non_authority_note": result.non_authority_note,
    }


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_object_lever_interaction_legality_authority_flags(obj: Any) -> bool:
    if not isinstance(obj, ObjectLeverInteractionLegalityAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True


def validate_object_lever_interaction_command_declaration(obj: Any) -> bool:
    if not isinstance(obj, ObjectLeverInteractionCommandDeclaration):
        return False
    if obj.command_family != OBJECT_LEVER_COMMAND_FAMILY:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_object_lever_legality_metadata_keys(
            obj.metadata, "metadata",
            InvalidObjectLeverInteractionCommandDeclarationError,
        )
    except InvalidObjectLeverInteractionCommandDeclarationError:
        return False
    return True


def validate_object_lever_projection_requirement(obj: Any) -> bool:
    if not isinstance(obj, ObjectLeverProjectionRequirement):
        return False
    if obj.entity_kind not in (
        OBJECT_LEVER_REQUIRED_ENTITY_KINDS | OBJECT_LEVER_OPTIONAL_ENTITY_KINDS
    ):
        return False
    if obj.owner_family not in VERTICAL_SLICE_OWNER_FAMILIES:
        return False
    if not isinstance(obj.required, bool):
        return False
    if obj.requirement_status not in OBJECT_LEVER_PACKET_REQUIREMENT_STATUSES:
        return False
    if not isinstance(obj.safe_reference_ids, tuple):
        return False
    for ref_id in obj.safe_reference_ids:
        if not isinstance(ref_id, str) or not ref_id:
            return False
    if obj.block_reason is not None and obj.block_reason not in OBJECT_LEVER_BLOCK_REASONS:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_object_lever_legality_metadata_keys(
            obj.metadata, "metadata", InvalidObjectLeverProjectionRequirementError,
        )
    except InvalidObjectLeverProjectionRequirementError:
        return False
    return True


def validate_object_lever_legality_input_packet_set(obj: Any) -> bool:
    if not isinstance(obj, ObjectLeverLegalityInputPacketSet):
        return False
    if not isinstance(obj.command_declaration, ObjectLeverInteractionCommandDeclaration):
        return False
    if not isinstance(obj.projection_packets, tuple):
        return False
    for packet in obj.projection_packets:
        if not isinstance(packet, ProjectionVisibilityAdapterPacket):
            return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_object_lever_legality_metadata_keys(
            obj.metadata, "metadata", InvalidObjectLeverLegalityInputPacketSetError,
        )
    except InvalidObjectLeverLegalityInputPacketSetError:
        return False
    return True


def validate_object_lever_legality_reading(obj: Any) -> bool:
    if not isinstance(obj, ObjectLeverLegalityReading):
        return False
    if obj.reader_status not in OBJECT_LEVER_LEGALITY_READER_STATUSES:
        return False
    if obj.legality_decision not in OBJECT_LEVER_LEGALITY_DECISIONS:
        return False
    if obj.command_family != OBJECT_LEVER_COMMAND_FAMILY:
        return False
    if not isinstance(obj.requirement_readings, tuple):
        return False
    for req in obj.requirement_readings:
        if not validate_object_lever_projection_requirement(req):
            return False
    if not isinstance(obj.block_reasons, tuple):
        return False
    for reason in obj.block_reasons:
        if reason not in OBJECT_LEVER_BLOCK_REASONS:
            return False
    if not isinstance(obj.safe_reference_ids, tuple):
        return False
    for ref_id in obj.safe_reference_ids:
        if not isinstance(ref_id, str) or not ref_id:
            return False
    if not validate_object_lever_interaction_legality_authority_flags(obj.authority_flags):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_object_lever_legality_metadata_keys(
            obj.metadata, "metadata", InvalidObjectLeverLegalityReadingError,
        )
    except InvalidObjectLeverLegalityReadingError:
        return False
    return True


def validate_object_lever_legality_reader_result(obj: Any) -> bool:
    if not isinstance(obj, ObjectLeverLegalityReaderResult):
        return False
    if obj.reader_status not in OBJECT_LEVER_LEGALITY_READER_STATUSES:
        return False
    if obj.legality_decision not in OBJECT_LEVER_LEGALITY_DECISIONS:
        return False
    if not validate_object_lever_legality_reading(obj.legality_reading):
        return False
    if not validate_object_lever_interaction_legality_authority_flags(obj.authority_flags):
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    try:
        _validate_no_forbidden_object_lever_legality_metadata_keys(
            obj.metadata, "metadata", InvalidObjectLeverLegalityReaderResultError,
        )
    except InvalidObjectLeverLegalityReaderResultError:
        return False
    return True
