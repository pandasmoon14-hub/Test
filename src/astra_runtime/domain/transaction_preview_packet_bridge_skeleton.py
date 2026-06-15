"""Transaction preview packet bridge skeleton  backend-owned packet descriptor bridge.

RUNTIME-DOMAIN-PR-9E: creates a narrow backend-owned transaction preview packet
bridge that compiles PR-9A assembly, PR-9C routing, PR-9D validation bridge, and
kernel TransactionPreview surfaces into deterministic packet descriptor / packet
reference shells suitable for later context/narration packet work.

This module is a skeleton only: no live play, no model authority, no persistence,
no RNG execution, no state mutation, no event append, no settlement, no
consequence application, no conversion, no canon promotion, no packet delivery,
no prompt rendering, no prompt execution, and no prose parsing.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    validate_transaction_preview,
)

from astra_runtime.domain.scene_command_execution_skeleton import (
    SceneCommandExecutionAssemblyResult,
    SceneCommandExecutionContextPacketRef,
    SceneCommandExecutionNarrationPacketRef,
    validate_scene_command_execution_assembly_result,
)
from astra_runtime.domain.command_kind_routing_skeleton import (
    CommandKindRoutingResult,
    validate_command_kind_routing_result,
)
from astra_runtime.domain.validation_integration_bridge_skeleton import (
    ValidationIntegrationBridgeResult,
    validate_validation_integration_bridge_result,
)


# ---------------------------------------------------------------------------
# Packet role constants
# ---------------------------------------------------------------------------

SINGLE_EVENT_CONTEXT_PACKET: str = "single_event_context_packet"
SINGLE_EVENT_NARRATION_PACKET: str = "single_event_narration_packet"
VISIBLE_SUMMARY_PACKET: str = "visible_summary_packet"
NO_COMMIT_INTENT_PACKET: str = "no_commit_intent_packet"

PACKET_ROLES = frozenset({
    SINGLE_EVENT_CONTEXT_PACKET,
    SINGLE_EVENT_NARRATION_PACKET,
    VISIBLE_SUMMARY_PACKET,
    NO_COMMIT_INTENT_PACKET,
})


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------

class TransactionPreviewPacketBridgeSkeletonError(ValueError):
    """Base error for transaction preview packet bridge operations."""


class InvalidTransactionPreviewPacketBridgeRequestError(
    TransactionPreviewPacketBridgeSkeletonError,
):
    """Raised when a bridge request fails validation."""


class InvalidTransactionPreviewPacketBridgeSubjectRefError(
    TransactionPreviewPacketBridgeSkeletonError,
):
    """Raised when a subject reference fails validation."""


class InvalidTransactionPreviewPacketBridgePacketRefError(
    TransactionPreviewPacketBridgeSkeletonError,
):
    """Raised when a packet reference fails validation."""


class InvalidTransactionPreviewPacketBridgePacketDescriptorError(
    TransactionPreviewPacketBridgeSkeletonError,
):
    """Raised when a packet descriptor fails validation."""


class InvalidTransactionPreviewPacketBridgeAuthorityFlagsError(
    TransactionPreviewPacketBridgeSkeletonError,
):
    """Raised when authority flags contain any True value."""


class InvalidTransactionPreviewPacketBridgeResultError(
    TransactionPreviewPacketBridgeSkeletonError,
):
    """Raised when a bridge result fails validation."""


# ---------------------------------------------------------------------------
# Private validation helpers
# ---------------------------------------------------------------------------

def _validate_non_empty_str(
    value: object, name: str, error_cls: type[Exception],
) -> str:
    if not isinstance(value, str) or not value:
        raise error_cls(f"{name} must be a non-empty string, got {value!r}")
    return value


def _validate_record_id(
    value: object, name: str, error_cls: type[Exception],
) -> str:
    value = _validate_non_empty_str(value, name, error_cls)
    if not is_valid_record_id(value):
        raise error_cls(f"{name} must be a valid record ID, got {value!r}")
    return value


def _validate_bool(
    value: object, name: str, error_cls: type[Exception],
) -> bool:
    if not isinstance(value, bool):
        raise error_cls(f"{name} must be a bool, got {value!r}")
    return value


def _safe_metadata(
    metadata: Mapping[str, Any] | None,
    error_cls: type[Exception],
) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    return MappingProxyType(copy.deepcopy(dict(metadata)))


# ---------------------------------------------------------------------------
# Subject ref
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TransactionPreviewPacketBridgeSubjectRef:
    """Lightweight reference to the command subject in the bridge."""

    subject_ref_id: str
    subject_label: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_record_id(
            self.subject_ref_id, "subject_ref_id",
            InvalidTransactionPreviewPacketBridgeSubjectRefError,
        )
        _validate_non_empty_str(
            self.subject_label, "subject_label",
            InvalidTransactionPreviewPacketBridgeSubjectRefError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidTransactionPreviewPacketBridgeSubjectRefError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_ref_id": self.subject_ref_id,
            "subject_label": self.subject_label,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Packet ref
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TransactionPreviewPacketBridgePacketRef:
    """Reference to a packet surface carried by the bridge."""

    packet_ref_id: str
    packet_role: str
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_record_id(
            self.packet_ref_id, "packet_ref_id",
            InvalidTransactionPreviewPacketBridgePacketRefError,
        )
        _validate_non_empty_str(
            self.packet_role, "packet_role",
            InvalidTransactionPreviewPacketBridgePacketRefError,
        )
        if self.packet_role not in PACKET_ROLES:
            raise InvalidTransactionPreviewPacketBridgePacketRefError(
                f"packet_role must be one of {sorted(PACKET_ROLES)}, "
                f"got {self.packet_role!r}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidTransactionPreviewPacketBridgePacketRefError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_ref_id": self.packet_ref_id,
            "packet_role": self.packet_role,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Packet descriptor  lightweight reference shell, not a full packet
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TransactionPreviewPacketDescriptor:
    """Backend-owned packet descriptor reference shell.

    This is NOT a full packet and NOT a model prompt.  It is a deterministic
    reference shell that later packet compilation / delivery surfaces may
    consume.
    """

    descriptor_id: str
    packet_role: str
    packet_kind: str
    source_surface: str
    source_surface_ref: str
    packet_ref_id: str
    ordering: int = 0
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_record_id(
            self.descriptor_id, "descriptor_id",
            InvalidTransactionPreviewPacketBridgePacketDescriptorError,
        )
        _validate_non_empty_str(
            self.packet_role, "packet_role",
            InvalidTransactionPreviewPacketBridgePacketDescriptorError,
        )
        if self.packet_role not in PACKET_ROLES:
            raise InvalidTransactionPreviewPacketBridgePacketDescriptorError(
                f"packet_role must be one of {sorted(PACKET_ROLES)}, "
                f"got {self.packet_role!r}"
            )
        _validate_non_empty_str(
            self.packet_kind, "packet_kind",
            InvalidTransactionPreviewPacketBridgePacketDescriptorError,
        )
        _validate_non_empty_str(
            self.source_surface, "source_surface",
            InvalidTransactionPreviewPacketBridgePacketDescriptorError,
        )
        _validate_non_empty_str(
            self.source_surface_ref, "source_surface_ref",
            InvalidTransactionPreviewPacketBridgePacketDescriptorError,
        )
        _validate_record_id(
            self.packet_ref_id, "packet_ref_id",
            InvalidTransactionPreviewPacketBridgePacketDescriptorError,
        )
        if not isinstance(self.ordering, int):
            raise InvalidTransactionPreviewPacketBridgePacketDescriptorError(
                f"ordering must be an int, got {type(self.ordering).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidTransactionPreviewPacketBridgePacketDescriptorError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "descriptor_id": self.descriptor_id,
            "packet_role": self.packet_role,
            "packet_kind": self.packet_kind,
            "source_surface": self.source_surface,
            "source_surface_ref": self.source_surface_ref,
            "packet_ref_id": self.packet_ref_id,
            "ordering": self.ordering,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Bridge request
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TransactionPreviewPacketBridgeRequest:
    """Input request for the transaction preview packet bridge."""

    request_ref: str
    command_ref: str
    transaction_preview: TransactionPreview
    assembly_result: SceneCommandExecutionAssemblyResult
    routing_result: CommandKindRoutingResult
    validation_bridge_result: ValidationIntegrationBridgeResult
    subject_ref: TransactionPreviewPacketBridgeSubjectRef | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_record_id(
            self.request_ref, "request_ref",
            InvalidTransactionPreviewPacketBridgeRequestError,
        )
        _validate_non_empty_str(
            self.command_ref, "command_ref",
            InvalidTransactionPreviewPacketBridgeRequestError,
        )
        if not isinstance(self.transaction_preview, TransactionPreview):
            raise InvalidTransactionPreviewPacketBridgeRequestError(
                "transaction_preview must be a TransactionPreview instance"
            )
        if not isinstance(self.assembly_result, SceneCommandExecutionAssemblyResult):
            raise InvalidTransactionPreviewPacketBridgeRequestError(
                "assembly_result must be a SceneCommandExecutionAssemblyResult instance"
            )
        if not isinstance(self.routing_result, CommandKindRoutingResult):
            raise InvalidTransactionPreviewPacketBridgeRequestError(
                "routing_result must be a CommandKindRoutingResult instance"
            )
        if not isinstance(self.validation_bridge_result, ValidationIntegrationBridgeResult):
            raise InvalidTransactionPreviewPacketBridgeRequestError(
                "validation_bridge_result must be a ValidationIntegrationBridgeResult instance"
            )
        if (
            self.subject_ref is not None
            and not isinstance(self.subject_ref, TransactionPreviewPacketBridgeSubjectRef)
        ):
            raise InvalidTransactionPreviewPacketBridgeRequestError(
                "subject_ref must be a TransactionPreviewPacketBridgeSubjectRef or None"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidTransactionPreviewPacketBridgeRequestError),
        )


# ---------------------------------------------------------------------------
# Authority flags  all must be False
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TransactionPreviewPacketBridgeAuthorityFlags:
    """Explicit authority denials for the transaction preview packet bridge.

    All flags default to False.  Constructing with any True flag raises
    InvalidTransactionPreviewPacketBridgeAuthorityFlagsError.
    """

    legality_resolution: bool = False
    validation_rule_execution: bool = False
    command_execution: bool = False
    runtime_action_execution: bool = False
    state_mutation: bool = False
    event_append: bool = False
    persistence_write: bool = False
    rng_table_oracle_execution: bool = False
    settlement_authorization: bool = False
    pr5_arithmetic_execution: bool = False
    consequence_application: bool = False
    packet_compilation: bool = False
    packet_delivery: bool = False
    prompt_rendering: bool = False
    prompt_execution: bool = False
    model_authority: bool = False
    prose_parsing: bool = False
    narration_generation: bool = False
    live_play_session_authority: bool = False
    ui_client_authority: bool = False
    conversion: bool = False
    sourcebook_inclusion: bool = False
    canon_promotion: bool = False

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if value is not False:
                raise InvalidTransactionPreviewPacketBridgeAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in PR-9E bridge skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {name: False for name in self.__dataclass_fields__}


# ---------------------------------------------------------------------------
# Bridge result
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TransactionPreviewPacketBridgeResult:
    """Deterministic output of the transaction preview packet bridge.

    Carries references and packet descriptors only.  Does not deliver
    packets, render prompts, execute commands, or mutate state.
    """

    result_ref: str
    request_ref: str
    command_ref: str
    transaction_preview_ref: str
    command_family: str
    command_kind: str
    validation_bridge_ref: str
    context_packet_descriptor: TransactionPreviewPacketDescriptor
    narration_packet_descriptor: TransactionPreviewPacketDescriptor
    visible_summary_packet_descriptor: TransactionPreviewPacketDescriptor
    no_commit_intent_packet_descriptor: TransactionPreviewPacketDescriptor
    packet_ordering: tuple[str, ...] = ()
    authority_flags: TransactionPreviewPacketBridgeAuthorityFlags = field(
        default_factory=TransactionPreviewPacketBridgeAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({}),
    )

    def __post_init__(self) -> None:
        _validate_record_id(
            self.result_ref, "result_ref",
            InvalidTransactionPreviewPacketBridgeResultError,
        )
        _validate_record_id(
            self.request_ref, "request_ref",
            InvalidTransactionPreviewPacketBridgeResultError,
        )
        _validate_non_empty_str(
            self.command_ref, "command_ref",
            InvalidTransactionPreviewPacketBridgeResultError,
        )
        _validate_record_id(
            self.transaction_preview_ref, "transaction_preview_ref",
            InvalidTransactionPreviewPacketBridgeResultError,
        )
        _validate_non_empty_str(
            self.command_family, "command_family",
            InvalidTransactionPreviewPacketBridgeResultError,
        )
        _validate_non_empty_str(
            self.command_kind, "command_kind",
            InvalidTransactionPreviewPacketBridgeResultError,
        )
        _validate_record_id(
            self.validation_bridge_ref, "validation_bridge_ref",
            InvalidTransactionPreviewPacketBridgeResultError,
        )
        if not isinstance(self.context_packet_descriptor, TransactionPreviewPacketDescriptor):
            raise InvalidTransactionPreviewPacketBridgeResultError(
                "context_packet_descriptor must be a TransactionPreviewPacketDescriptor"
            )
        if not isinstance(self.narration_packet_descriptor, TransactionPreviewPacketDescriptor):
            raise InvalidTransactionPreviewPacketBridgeResultError(
                "narration_packet_descriptor must be a TransactionPreviewPacketDescriptor"
            )
        if not isinstance(self.visible_summary_packet_descriptor, TransactionPreviewPacketDescriptor):
            raise InvalidTransactionPreviewPacketBridgeResultError(
                "visible_summary_packet_descriptor must be a TransactionPreviewPacketDescriptor"
            )
        if not isinstance(self.no_commit_intent_packet_descriptor, TransactionPreviewPacketDescriptor):
            raise InvalidTransactionPreviewPacketBridgeResultError(
                "no_commit_intent_packet_descriptor must be a TransactionPreviewPacketDescriptor"
            )
        if not isinstance(self.packet_ordering, tuple):
            raise InvalidTransactionPreviewPacketBridgeResultError(
                "packet_ordering must be a tuple"
            )
        for i, item in enumerate(self.packet_ordering):
            if not isinstance(item, str) or not item:
                raise InvalidTransactionPreviewPacketBridgeResultError(
                    f"packet_ordering[{i}] must be a non-empty string, got {item!r}"
                )
        if not isinstance(self.authority_flags, TransactionPreviewPacketBridgeAuthorityFlags):
            raise InvalidTransactionPreviewPacketBridgeResultError(
                "authority_flags must be a TransactionPreviewPacketBridgeAuthorityFlags"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidTransactionPreviewPacketBridgeResultError),
        )


# ---------------------------------------------------------------------------
# Validator functions
# ---------------------------------------------------------------------------

def validate_transaction_preview_packet_descriptor(obj: Any) -> bool:
    """Validate a TransactionPreviewPacketDescriptor."""
    if not isinstance(obj, TransactionPreviewPacketDescriptor):
        return False
    try:
        _validate_record_id(obj.descriptor_id, "descriptor_id", ValueError)
        _validate_non_empty_str(obj.packet_role, "packet_role", ValueError)
        _validate_non_empty_str(obj.packet_kind, "packet_kind", ValueError)
        _validate_non_empty_str(obj.source_surface, "source_surface", ValueError)
        _validate_non_empty_str(obj.source_surface_ref, "source_surface_ref", ValueError)
        _validate_record_id(obj.packet_ref_id, "packet_ref_id", ValueError)
        if not isinstance(obj.ordering, int):
            return False
        return True
    except (ValueError, TypeError):
        return False


def validate_transaction_preview_packet_bridge_result(obj: Any) -> bool:
    """Validate a TransactionPreviewPacketBridgeResult."""
    if not isinstance(obj, TransactionPreviewPacketBridgeResult):
        return False
    try:
        _validate_record_id(obj.result_ref, "result_ref", ValueError)
        _validate_record_id(obj.request_ref, "request_ref", ValueError)
        _validate_non_empty_str(obj.command_ref, "command_ref", ValueError)
        _validate_record_id(obj.transaction_preview_ref, "transaction_preview_ref", ValueError)
        _validate_non_empty_str(obj.command_family, "command_family", ValueError)
        _validate_non_empty_str(obj.command_kind, "command_kind", ValueError)
        _validate_record_id(obj.validation_bridge_ref, "validation_bridge_ref", ValueError)
        if not validate_transaction_preview_packet_descriptor(obj.context_packet_descriptor):
            return False
        if not validate_transaction_preview_packet_descriptor(obj.narration_packet_descriptor):
            return False
        if not validate_transaction_preview_packet_descriptor(obj.visible_summary_packet_descriptor):
            return False
        if not validate_transaction_preview_packet_descriptor(obj.no_commit_intent_packet_descriptor):
            return False
        if not isinstance(obj.packet_ordering, tuple):
            return False
        return True
    except (ValueError, TypeError):
        return False


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------

def create_transaction_preview_packet_bridge_subject_ref(
    *,
    subject_ref_id: str,
    subject_label: str,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionPreviewPacketBridgeSubjectRef:
    """Create a TransactionPreviewPacketBridgeSubjectRef."""
    return TransactionPreviewPacketBridgeSubjectRef(
        subject_ref_id=subject_ref_id,
        subject_label=subject_label,
        metadata=metadata,
    )


def create_transaction_preview_packet_bridge_packet_ref(
    *,
    packet_ref_id: str,
    packet_role: str,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionPreviewPacketBridgePacketRef:
    """Create a TransactionPreviewPacketBridgePacketRef."""
    return TransactionPreviewPacketBridgePacketRef(
        packet_ref_id=packet_ref_id,
        packet_role=packet_role,
        metadata=metadata,
    )


def create_transaction_preview_packet_descriptor(
    *,
    descriptor_id: str,
    packet_role: str,
    packet_kind: str,
    source_surface: str,
    source_surface_ref: str,
    packet_ref_id: str,
    ordering: int = 0,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionPreviewPacketDescriptor:
    """Create a TransactionPreviewPacketDescriptor."""
    return TransactionPreviewPacketDescriptor(
        descriptor_id=descriptor_id,
        packet_role=packet_role,
        packet_kind=packet_kind,
        source_surface=source_surface,
        source_surface_ref=source_surface_ref,
        packet_ref_id=packet_ref_id,
        ordering=ordering,
        metadata=metadata,
    )


def create_transaction_preview_packet_bridge_request(
    *,
    request_ref: str,
    command_ref: str,
    transaction_preview: TransactionPreview,
    assembly_result: SceneCommandExecutionAssemblyResult,
    routing_result: CommandKindRoutingResult,
    validation_bridge_result: ValidationIntegrationBridgeResult,
    subject_ref: TransactionPreviewPacketBridgeSubjectRef | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> TransactionPreviewPacketBridgeRequest:
    """Create a TransactionPreviewPacketBridgeRequest."""
    return TransactionPreviewPacketBridgeRequest(
        request_ref=request_ref,
        command_ref=command_ref,
        transaction_preview=transaction_preview,
        assembly_result=assembly_result,
        routing_result=routing_result,
        validation_bridge_result=validation_bridge_result,
        subject_ref=subject_ref,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Deterministic serializers
# ---------------------------------------------------------------------------

def serialize_transaction_preview_packet_descriptor(
    descriptor: TransactionPreviewPacketDescriptor,
) -> dict[str, Any]:
    """Deterministic serialization of a packet descriptor."""
    return descriptor.to_dict()


def serialize_transaction_preview_packet_bridge_result(
    result: TransactionPreviewPacketBridgeResult,
) -> dict[str, Any]:
    """Deterministic full serialization of a bridge result."""
    return {
        "result_ref": result.result_ref,
        "request_ref": result.request_ref,
        "command_ref": result.command_ref,
        "transaction_preview_ref": result.transaction_preview_ref,
        "command_family": result.command_family,
        "command_kind": result.command_kind,
        "validation_bridge_ref": result.validation_bridge_ref,
        "context_packet_descriptor": serialize_transaction_preview_packet_descriptor(
            result.context_packet_descriptor,
        ),
        "narration_packet_descriptor": serialize_transaction_preview_packet_descriptor(
            result.narration_packet_descriptor,
        ),
        "visible_summary_packet_descriptor": serialize_transaction_preview_packet_descriptor(
            result.visible_summary_packet_descriptor,
        ),
        "no_commit_intent_packet_descriptor": serialize_transaction_preview_packet_descriptor(
            result.no_commit_intent_packet_descriptor,
        ),
        "packet_ordering": list(result.packet_ordering),
        "authority_flags": result.authority_flags.to_dict(),
        "metadata": copy.deepcopy(dict(result.metadata)),
    }


def serialize_transaction_preview_packet_bridge_result_visible(
    result: TransactionPreviewPacketBridgeResult,
) -> dict[str, Any]:
    """Visible serialization of a bridge result.

    Excludes backend-only metadata fields while preserving the reference
    shell structure.
    """
    full = serialize_transaction_preview_packet_bridge_result(result)
    full["metadata"] = {}
    return full


# ---------------------------------------------------------------------------
# Core bridge builder
# ---------------------------------------------------------------------------

def build_transaction_preview_packet_bridge_result(
    *,
    request: TransactionPreviewPacketBridgeRequest,
    result_id_seed: str | None = None,
) -> TransactionPreviewPacketBridgeResult:
    """Build a deterministic TransactionPreviewPacketBridgeResult.

    Validates all inputs, verifies command reference agreement, and produces
    deterministic packet descriptor shells.  Does NOT call any routing,
    assembly, validation, model, prompt, narration, live-play, state
    mutation, event append, persistence, RNG, settlement, or packet
    delivery code.
    """

    # 1. Validate TransactionPreview
    if not validate_transaction_preview(request.transaction_preview):
        raise InvalidTransactionPreviewPacketBridgeRequestError(
            "transaction_preview is not valid"
        )

    # 2. Validate assembly result
    if not validate_scene_command_execution_assembly_result(request.assembly_result):
        raise InvalidTransactionPreviewPacketBridgeRequestError(
            "assembly_result is not valid"
        )

    # 3. Validate routing result
    if not validate_command_kind_routing_result(request.routing_result):
        raise InvalidTransactionPreviewPacketBridgeRequestError(
            "routing_result is not valid"
        )

    # 4. Validate validation bridge result
    if not validate_validation_integration_bridge_result(request.validation_bridge_result):
        raise InvalidTransactionPreviewPacketBridgeRequestError(
            "validation_bridge_result is not valid"
        )

    # 5. Verify command references agree across all surfaces
    tp_command_id = request.transaction_preview.command_id
    assembly_command_intent = request.assembly_result.command_intent
    routing_command_ref = request.routing_result.command_ref
    bridge_command_ref = request.validation_bridge_result.command_ref

    if tp_command_id != request.command_ref:
        raise InvalidTransactionPreviewPacketBridgeRequestError(
            f"transaction preview command_id {tp_command_id!r} "
            f"does not match request command_ref {request.command_ref!r}"
        )

    if routing_command_ref != request.command_ref:
        raise InvalidTransactionPreviewPacketBridgeRequestError(
            f"routing result command_ref {routing_command_ref!r} "
            f"does not match request command_ref {request.command_ref!r}"
        )

    if bridge_command_ref != request.command_ref:
        raise InvalidTransactionPreviewPacketBridgeRequestError(
            f"validation bridge result command_ref {bridge_command_ref!r} "
            f"does not match request command_ref {request.command_ref!r}"
        )

    # 6. Extract command family and kind from PR-9C routing (no reclassification)
    command_family = request.routing_result.classification.family
    command_kind = request.routing_result.classification.kind

    # 7. Build seed for deterministic IDs (sanitize for record-ID compliance)
    seed = result_id_seed or f"tp_packet_bridge_{request.command_ref}"
    seed = seed.replace(":", "_").replace("~", "_").replace("/", "_")

    # 8. Build context packet descriptor from PR-9A assembly context packet ref
    ctx_ref = request.assembly_result.context_packet_ref
    context_descriptor = TransactionPreviewPacketDescriptor(
        descriptor_id=build_record_id(
            "tp_packet_descriptor", f"{seed}_context",
        ),
        packet_role=SINGLE_EVENT_CONTEXT_PACKET,
        packet_kind="single_event_narration",
        source_surface="PR_9A_assembly_result",
        source_surface_ref=request.assembly_result.result_ref,
        packet_ref_id=ctx_ref.packet_ref,
        ordering=0,
        metadata=MappingProxyType({
            "carried_from": "PR_9A_assembly_result",
            "context_projection_present": ctx_ref.context_projection is not None,
        }),
    )

    # 9. Build narration packet descriptor from PR-9A assembly narration packet ref
    nrr_ref = request.assembly_result.narration_packet_ref
    narration_descriptor = TransactionPreviewPacketDescriptor(
        descriptor_id=build_record_id(
            "tp_packet_descriptor", f"{seed}_narration",
        ),
        packet_role=SINGLE_EVENT_NARRATION_PACKET,
        packet_kind="single_event_narration",
        source_surface="PR_9A_assembly_result",
        source_surface_ref=request.assembly_result.result_ref,
        packet_ref_id=nrr_ref.packet_ref,
        ordering=1,
        metadata=MappingProxyType({
            "carried_from": "PR_9A_assembly_result",
            "narration_kind": nrr_ref.narration_kind,
        }),
    )

    # 10. Build visible summary packet descriptor as reference shell
    visible_descriptor = TransactionPreviewPacketDescriptor(
        descriptor_id=build_record_id(
            "tp_packet_descriptor", f"{seed}_visible_summary",
        ),
        packet_role=VISIBLE_SUMMARY_PACKET,
        packet_kind="visible_summary",
        source_surface="PR_9E_bridge",
        source_surface_ref=build_record_id(
            "tp_packet_bridge_result", seed,
        ),
        packet_ref_id=build_record_id(
            "tp_visible_summary_ref", f"{seed}_visible",
        ),
        ordering=2,
        metadata=MappingProxyType({
            "carried_from": "PR_9E_bridge",
            "note": "reference shell only, not generated text",
        }),
    )

    # 11. Build no-commit intent packet descriptor as reference shell
    no_commit_descriptor = TransactionPreviewPacketDescriptor(
        descriptor_id=build_record_id(
            "tp_packet_descriptor", f"{seed}_no_commit_intent",
        ),
        packet_role=NO_COMMIT_INTENT_PACKET,
        packet_kind="no_commit_intent",
        source_surface="PR_9E_bridge",
        source_surface_ref=build_record_id(
            "tp_packet_bridge_result", seed,
        ),
        packet_ref_id=build_record_id(
            "tp_no_commit_intent_ref", f"{seed}_no_commit",
        ),
        ordering=3,
        metadata=MappingProxyType({
            "carried_from": "PR_9E_bridge",
            "note": "reference shell only, not live parser behavior",
        }),
    )

    # 12. Build result
    result_ref = build_record_id(
        "tp_packet_bridge_result", f"{seed}_result",
    )

    packet_ordering = (
        context_descriptor.packet_ref_id,
        narration_descriptor.packet_ref_id,
        visible_descriptor.packet_ref_id,
        no_commit_descriptor.packet_ref_id,
    )

    return TransactionPreviewPacketBridgeResult(
        result_ref=result_ref,
        request_ref=request.request_ref,
        command_ref=request.command_ref,
        transaction_preview_ref=request.transaction_preview.preview_id,
        command_family=command_family,
        command_kind=command_kind,
        validation_bridge_ref=request.validation_bridge_result.result_ref,
        context_packet_descriptor=context_descriptor,
        narration_packet_descriptor=narration_descriptor,
        visible_summary_packet_descriptor=visible_descriptor,
        no_commit_intent_packet_descriptor=no_commit_descriptor,
        packet_ordering=packet_ordering,
        authority_flags=TransactionPreviewPacketBridgeAuthorityFlags(),
        metadata=request.metadata,
    )
