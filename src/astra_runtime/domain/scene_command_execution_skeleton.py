"""Scene command execution skeleton — backend-owned typed assembly.

RUNTIME-DOMAIN-PR-9A: generalizes the PR-8 tiny vertical slice into a reusable,
backend-owned runtime transaction assembly path. This module is a skeleton only:
no live play, no model authority, no persistence, no RNG execution, no state
mutation, no event append, no settlement, no consequence application, no
conversion, and no canon promotion.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from astra_runtime.domain.resource_consequence_math import (
    ResourceMathRequest,
    ResourceMathResult,
    validate_resource_math_request,
    validate_resource_math_result,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    validate_command_envelope,
)
from astra_runtime.kernel.context_projection import (
    ContextProjection,
    validate_context_projection,
)
from astra_runtime.kernel.event_ledger import (
    EventLedgerEntry,
    validate_event_ledger_entry,
)
from astra_runtime.kernel.persistence_boundary import (
    PersistenceBoundaryRequest,
    validate_persistence_boundary_request,
)
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id
from astra_runtime.kernel.state_delta import (
    StateDeltaEnvelope,
    validate_state_delta_envelope,
)
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    validate_transaction_preview,
)
from astra_runtime.kernel.validation_pipeline import (
    ValidationResult,
    validate_validation_result,
)


class SceneCommandExecutionSkeletonError(ValueError):
    """Base error for scene command execution skeleton operations."""


class InvalidSceneCommandExecutionSubjectRefError(SceneCommandExecutionSkeletonError):
    """Raised when a subject reference fails validation."""


class InvalidSceneCommandExecutionSceneContractError(SceneCommandExecutionSkeletonError):
    """Raised when a scene contract fails validation."""


class InvalidSceneCommandExecutionActorContractError(SceneCommandExecutionSkeletonError):
    """Raised when an actor contract fails validation."""


class InvalidSceneCommandExecutionObjectContractError(SceneCommandExecutionSkeletonError):
    """Raised when an object contract fails validation."""


class InvalidSceneCommandExecutionHiddenInfoContractError(SceneCommandExecutionSkeletonError):
    """Raised when a hidden-info contract fails validation."""


class InvalidSceneCommandExecutionCommandIntentError(SceneCommandExecutionSkeletonError):
    """Raised when a command intent record fails validation."""


class InvalidSceneCommandExecutionValidationRefError(SceneCommandExecutionSkeletonError):
    """Raised when a validation reference fails validation."""


class InvalidSceneCommandExecutionResourcePreviewRefError(SceneCommandExecutionSkeletonError):
    """Raised when a resource preview reference fails validation."""


class InvalidSceneCommandExecutionStateDeltaCandidateRefError(SceneCommandExecutionSkeletonError):
    """Raised when a state-delta candidate reference fails validation."""


class InvalidSceneCommandExecutionEventLedgerCandidateRefError(SceneCommandExecutionSkeletonError):
    """Raised when an event-ledger candidate reference fails validation."""


class InvalidSceneCommandExecutionContextPacketRefError(SceneCommandExecutionSkeletonError):
    """Raised when a context packet reference fails validation."""


class InvalidSceneCommandExecutionNarrationPacketRefError(SceneCommandExecutionSkeletonError):
    """Raised when a narration packet reference fails validation."""


class InvalidSceneCommandExecutionModelBoundaryFixtureRefError(SceneCommandExecutionSkeletonError):
    """Raised when a model-boundary fixture reference fails validation."""


class InvalidSceneCommandExecutionAssemblyRequestError(SceneCommandExecutionSkeletonError):
    """Raised when an assembly request fails validation."""


class InvalidSceneCommandExecutionAssemblyResultError(SceneCommandExecutionSkeletonError):
    """Raised when an assembly result fails validation."""


_VALID_SUBJECT_TYPES = frozenset({
    "actor",
    "object",
    "scene",
    "hidden_info",
    "command",
    "transaction",
    "event",
})


def _validate_non_empty_str(value: object, name: str, error_cls: type[Exception]) -> str:
    if not isinstance(value, str) or not value:
        raise error_cls(f"{name} must be a non-empty string, got {value!r}")
    return value


def _validate_record_id(value: object, name: str, error_cls: type[Exception]) -> str:
    value = _validate_non_empty_str(value, name, error_cls)
    if not is_valid_record_id(value):
        raise error_cls(f"{name} must be a valid record ID, got {value!r}")
    return value


def _validate_bool(value: object, name: str, error_cls: type[Exception]) -> bool:
    if not isinstance(value, bool):
        raise error_cls(f"{name} must be a bool, got {value!r}")
    return value


def _safe_metadata(metadata: Mapping[str, Any] | None, error_cls: type[Exception]) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls("metadata must be a mapping")
    return MappingProxyType(copy.deepcopy(dict(metadata)))


def _safe_str_seq(value: Sequence[str] | None, name: str, error_cls: type[Exception]) -> tuple[str, ...]:
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


def _safe_obj_seq(
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
            raise error_cls(f"{name}[{i}] must be a {obj_type.__name__}, got {type(elem).__name__}")
        result.append(elem)
    return tuple(result)


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionSubjectRef:
    """Immutable reference to a subject inside a scene contract."""

    subject_type: str
    ref_id: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.subject_type, "subject_type", InvalidSceneCommandExecutionSubjectRefError)
        if self.subject_type not in _VALID_SUBJECT_TYPES:
            raise InvalidSceneCommandExecutionSubjectRefError(
                f"subject_type must be one of {sorted(_VALID_SUBJECT_TYPES)}, got {self.subject_type!r}"
            )
        _validate_record_id(self.ref_id, "ref_id", InvalidSceneCommandExecutionSubjectRefError)
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionSubjectRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_type": self.subject_type,
            "ref_id": self.ref_id,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionActorContract:
    """Immutable actor contract within a scene."""

    actor_ref: str
    actor_label: str
    visible_description: str
    visible_condition_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.actor_ref, "actor_ref", InvalidSceneCommandExecutionActorContractError)
        _validate_non_empty_str(self.actor_label, "actor_label", InvalidSceneCommandExecutionActorContractError)
        _validate_non_empty_str(
            self.visible_description, "visible_description", InvalidSceneCommandExecutionActorContractError
        )
        object.__setattr__(
            self, "visible_condition_refs", _safe_str_seq(self.visible_condition_refs, "visible_condition_refs", InvalidSceneCommandExecutionActorContractError)
        )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionActorContractError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor_ref": self.actor_ref,
            "actor_label": self.actor_label,
            "visible_description": self.visible_description,
            "visible_condition_refs": list(self.visible_condition_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionObjectContract:
    """Immutable object/interactable contract within a scene."""

    object_ref: str
    object_label: str
    visible_description: str
    visible_state: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.object_ref, "object_ref", InvalidSceneCommandExecutionObjectContractError)
        _validate_non_empty_str(self.object_label, "object_label", InvalidSceneCommandExecutionObjectContractError)
        _validate_non_empty_str(
            self.visible_description, "visible_description", InvalidSceneCommandExecutionObjectContractError
        )
        _validate_non_empty_str(self.visible_state, "visible_state", InvalidSceneCommandExecutionObjectContractError)
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionObjectContractError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_ref": self.object_ref,
            "object_label": self.object_label,
            "visible_description": self.visible_description,
            "visible_state": self.visible_state,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionHiddenInfoContract:
    """Immutable hidden-information contract within a scene."""

    hidden_ref: str
    hidden_label: str
    backend_only_description: str
    reveal_condition: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.hidden_ref, "hidden_ref", InvalidSceneCommandExecutionHiddenInfoContractError)
        _validate_non_empty_str(self.hidden_label, "hidden_label", InvalidSceneCommandExecutionHiddenInfoContractError)
        _validate_non_empty_str(
            self.backend_only_description, "backend_only_description", InvalidSceneCommandExecutionHiddenInfoContractError
        )
        _validate_non_empty_str(self.reveal_condition, "reveal_condition", InvalidSceneCommandExecutionHiddenInfoContractError)
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionHiddenInfoContractError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "hidden_ref": self.hidden_ref,
            "hidden_label": self.hidden_label,
            "backend_only_description": self.backend_only_description,
            "reveal_condition": self.reveal_condition,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionSceneContract:
    """Immutable scene contract describing a playable scene reference surface.

    Supports multiple actors, objects, and hidden-info references while remaining
    a declaration rather than a live-play engine.
    """

    scene_ref: str
    scene_label: str
    visible_description: str
    visible_tags: tuple[str, ...] = ()
    actors: tuple[SceneCommandExecutionActorContract, ...] = ()
    objects: tuple[SceneCommandExecutionObjectContract, ...] = ()
    hidden_info: tuple[SceneCommandExecutionHiddenInfoContract, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.scene_ref, "scene_ref", InvalidSceneCommandExecutionSceneContractError)
        _validate_non_empty_str(self.scene_label, "scene_label", InvalidSceneCommandExecutionSceneContractError)
        _validate_non_empty_str(
            self.visible_description, "visible_description", InvalidSceneCommandExecutionSceneContractError
        )
        object.__setattr__(self, "visible_tags", _safe_str_seq(self.visible_tags, "visible_tags", InvalidSceneCommandExecutionSceneContractError))
        object.__setattr__(
            self,
            "actors",
            _safe_obj_seq(self.actors, "actors", InvalidSceneCommandExecutionSceneContractError, SceneCommandExecutionActorContract),
        )
        object.__setattr__(
            self,
            "objects",
            _safe_obj_seq(self.objects, "objects", InvalidSceneCommandExecutionSceneContractError, SceneCommandExecutionObjectContract),
        )
        object.__setattr__(
            self,
            "hidden_info",
            _safe_obj_seq(self.hidden_info, "hidden_info", InvalidSceneCommandExecutionSceneContractError, SceneCommandExecutionHiddenInfoContract),
        )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionSceneContractError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_ref": self.scene_ref,
            "scene_label": self.scene_label,
            "visible_description": self.visible_description,
            "visible_tags": list(self.visible_tags),
            "actors": [a.to_dict() for a in self.actors],
            "objects": [o.to_dict() for o in self.objects],
            "hidden_info": [h.to_dict() for h in self.hidden_info],
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionCommandIntent:
    """Immutable backend-owned command intent record derived from a CommandEnvelope."""

    intent_ref: str
    command_envelope_id: str
    command_type: str
    source_actor_ref: str
    target_ref: str | None = None
    payload_snapshot: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.intent_ref, "intent_ref", InvalidSceneCommandExecutionCommandIntentError)
        _validate_record_id(
            self.command_envelope_id, "command_envelope_id", InvalidSceneCommandExecutionCommandIntentError
        )
        _validate_non_empty_str(self.command_type, "command_type", InvalidSceneCommandExecutionCommandIntentError)
        _validate_record_id(self.source_actor_ref, "source_actor_ref", InvalidSceneCommandExecutionCommandIntentError)
        if self.target_ref is not None:
            _validate_record_id(self.target_ref, "target_ref", InvalidSceneCommandExecutionCommandIntentError)
        object.__setattr__(self, "payload_snapshot", _safe_metadata(self.payload_snapshot, InvalidSceneCommandExecutionCommandIntentError))
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionCommandIntentError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_ref": self.intent_ref,
            "command_envelope_id": self.command_envelope_id,
            "command_type": self.command_type,
            "source_actor_ref": self.source_actor_ref,
            "target_ref": self.target_ref,
            "payload_snapshot": copy.deepcopy(dict(self.payload_snapshot)),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionValidationRef:
    """Immutable validation reference/surface for transaction assembly."""

    validation_ref: str
    validation_result: ValidationResult | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.validation_ref, "validation_ref", InvalidSceneCommandExecutionValidationRefError)
        if self.validation_result is not None and not isinstance(self.validation_result, ValidationResult):
            raise InvalidSceneCommandExecutionValidationRefError(
                f"validation_result must be a ValidationResult, got {type(self.validation_result).__name__}"
            )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionValidationRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_ref": self.validation_ref,
            "validation_result": self.validation_result.to_dict() if self.validation_result is not None else None,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionResourcePreviewRef:
    """Immutable resource preview reference/surface for transaction assembly.

    Carries only RT-002 reference shapes; no arithmetic execution.
    """

    preview_ref: str
    resource_math_request: ResourceMathRequest | None = None
    resource_math_result: ResourceMathResult | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.preview_ref, "preview_ref", InvalidSceneCommandExecutionResourcePreviewRefError)
        if self.resource_math_request is not None and not isinstance(self.resource_math_request, ResourceMathRequest):
            raise InvalidSceneCommandExecutionResourcePreviewRefError(
                f"resource_math_request must be a ResourceMathRequest, got {type(self.resource_math_request).__name__}"
            )
        if self.resource_math_result is not None and not isinstance(self.resource_math_result, ResourceMathResult):
            raise InvalidSceneCommandExecutionResourcePreviewRefError(
                f"resource_math_result must be a ResourceMathResult, got {type(self.resource_math_result).__name__}"
            )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionResourcePreviewRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "preview_ref": self.preview_ref,
            "resource_math_request": self.resource_math_request.to_dict() if self.resource_math_request is not None else None,
            "resource_math_result": self.resource_math_result.to_dict() if self.resource_math_result is not None else None,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionStateDeltaCandidateRef:
    """Immutable state-delta candidate reference/surface for transaction assembly."""

    delta_ref: str
    delta_envelope: StateDeltaEnvelope | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.delta_ref, "delta_ref", InvalidSceneCommandExecutionStateDeltaCandidateRefError)
        if self.delta_envelope is not None and not isinstance(self.delta_envelope, StateDeltaEnvelope):
            raise InvalidSceneCommandExecutionStateDeltaCandidateRefError(
                f"delta_envelope must be a StateDeltaEnvelope, got {type(self.delta_envelope).__name__}"
            )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionStateDeltaCandidateRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "delta_ref": self.delta_ref,
            "delta_envelope": self.delta_envelope.to_dict() if self.delta_envelope is not None else None,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionEventLedgerCandidateRef:
    """Immutable event-ledger candidate reference/surface for transaction assembly."""

    event_ref: str
    ledger_entry: EventLedgerEntry | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.event_ref, "event_ref", InvalidSceneCommandExecutionEventLedgerCandidateRefError)
        if self.ledger_entry is not None and not isinstance(self.ledger_entry, EventLedgerEntry):
            raise InvalidSceneCommandExecutionEventLedgerCandidateRefError(
                f"ledger_entry must be an EventLedgerEntry, got {type(self.ledger_entry).__name__}"
            )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionEventLedgerCandidateRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_ref": self.event_ref,
            "ledger_entry": self.ledger_entry.to_dict() if self.ledger_entry is not None else None,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionContextPacketRef:
    """Immutable context packet reference/surface for transaction assembly."""

    packet_ref: str
    context_projection: ContextProjection | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.packet_ref, "packet_ref", InvalidSceneCommandExecutionContextPacketRefError)
        if self.context_projection is not None and not isinstance(self.context_projection, ContextProjection):
            raise InvalidSceneCommandExecutionContextPacketRefError(
                f"context_projection must be a ContextProjection, got {type(self.context_projection).__name__}"
            )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionContextPacketRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_ref": self.packet_ref,
            "context_projection": self.context_projection.to_dict() if self.context_projection is not None else None,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionNarrationPacketRef:
    """Immutable narration packet reference/surface for transaction assembly.

    Backend-owned projection only; no prose generation.
    """

    packet_ref: str
    narration_kind: str = "post_commit_narration"
    visible_summary: str = ""
    backend_only_ref_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.packet_ref, "packet_ref", InvalidSceneCommandExecutionNarrationPacketRefError)
        _validate_non_empty_str(self.narration_kind, "narration_kind", InvalidSceneCommandExecutionNarrationPacketRefError)
        if not isinstance(self.visible_summary, str):
            raise InvalidSceneCommandExecutionNarrationPacketRefError(
                f"visible_summary must be a string, got {type(self.visible_summary).__name__}"
            )
        object.__setattr__(
            self,
            "backend_only_ref_ids",
            _safe_str_seq(self.backend_only_ref_ids, "backend_only_ref_ids", InvalidSceneCommandExecutionNarrationPacketRefError),
        )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionNarrationPacketRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_ref": self.packet_ref,
            "narration_kind": self.narration_kind,
            "visible_summary": self.visible_summary,
            "backend_only_ref_ids": list(self.backend_only_ref_ids),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionModelBoundaryFixtureRef:
    """Immutable model-boundary fixture reference for transaction assembly.

    Records the relationship between model-facing packets and backend truth
    without calling any model.
    """

    fixture_ref: str
    fixture_kind: str = "context_narration_boundary"
    backend_truth_ref: str = ""
    model_facing_packet_refs: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.fixture_ref, "fixture_ref", InvalidSceneCommandExecutionModelBoundaryFixtureRefError)
        _validate_non_empty_str(self.fixture_kind, "fixture_kind", InvalidSceneCommandExecutionModelBoundaryFixtureRefError)
        if self.backend_truth_ref:
            _validate_record_id(self.backend_truth_ref, "backend_truth_ref", InvalidSceneCommandExecutionModelBoundaryFixtureRefError)
        object.__setattr__(
            self,
            "model_facing_packet_refs",
            _safe_str_seq(self.model_facing_packet_refs, "model_facing_packet_refs", InvalidSceneCommandExecutionModelBoundaryFixtureRefError),
        )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionModelBoundaryFixtureRefError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_ref": self.fixture_ref,
            "fixture_kind": self.fixture_kind,
            "backend_truth_ref": self.backend_truth_ref,
            "model_facing_packet_refs": list(self.model_facing_packet_refs),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionAssemblyAuthorityFlags:
    """Explicit anti-authority guardrails for an assembly result.

    All flags default to False. Setting any to True during construction raises
    an error, making the skeleton's non-authority explicit and auditable.
    """

    implementation_beyond_skeleton: bool = False
    live_play_authority: bool = False
    model_authority: bool = False
    prompt_rendering: bool = False
    prose_parsing: bool = False
    narration_generation: bool = False
    persistence_writes: bool = False
    rng_table_oracle_execution: bool = False
    state_mutation: bool = False
    event_append: bool = False
    settlement_authorization: bool = False
    pr5_arithmetic_execution: bool = False
    consequence_application: bool = False
    conversion: bool = False
    sourcebook_inclusion: bool = False
    canon_promotion: bool = False

    def __post_init__(self) -> None:
        for field_name in self.__dataclass_fields__:
            value = getattr(self, field_name)
            if value is not False:
                raise InvalidSceneCommandExecutionAssemblyResultError(
                    f"authority flag '{field_name}' must be False in PR-9A skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionAssemblyRequest:
    """Immutable request to assemble a backend-owned scene command transaction."""

    request_ref: str
    scene_contract: SceneCommandExecutionSceneContract
    command_envelope: CommandEnvelope
    intent_target_ref: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.request_ref, "request_ref", InvalidSceneCommandExecutionAssemblyRequestError)
        if not isinstance(self.scene_contract, SceneCommandExecutionSceneContract):
            raise InvalidSceneCommandExecutionAssemblyRequestError(
                f"scene_contract must be a SceneCommandExecutionSceneContract, got {type(self.scene_contract).__name__}"
            )
        if not isinstance(self.command_envelope, CommandEnvelope):
            raise InvalidSceneCommandExecutionAssemblyRequestError(
                f"command_envelope must be a CommandEnvelope, got {type(self.command_envelope).__name__}"
            )
        if self.intent_target_ref is not None:
            _validate_record_id(self.intent_target_ref, "intent_target_ref", InvalidSceneCommandExecutionAssemblyRequestError)
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionAssemblyRequestError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_ref": self.request_ref,
            "scene_contract": self.scene_contract.to_dict(),
            "command_envelope": self.command_envelope.to_dict(),
            "intent_target_ref": self.intent_target_ref,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class SceneCommandExecutionAssemblyResult:
    """Immutable backend-owned transaction assembly result.

    References validation, resource preview, state-delta candidate, event-ledger
    candidate, context packet, narration packet, and model-boundary fixture
    surfaces. Carries explicit non-authority flags.
    """

    result_ref: str
    request_ref: str
    command_intent: SceneCommandExecutionCommandIntent
    transaction_preview: TransactionPreview
    validation_ref: SceneCommandExecutionValidationRef
    resource_preview_ref: SceneCommandExecutionResourcePreviewRef
    state_delta_candidate_ref: SceneCommandExecutionStateDeltaCandidateRef
    event_ledger_candidate_ref: SceneCommandExecutionEventLedgerCandidateRef
    context_packet_ref: SceneCommandExecutionContextPacketRef
    narration_packet_ref: SceneCommandExecutionNarrationPacketRef
    model_boundary_fixture_ref: SceneCommandExecutionModelBoundaryFixtureRef
    persistence_prepare_ref: PersistenceBoundaryRequest | None = None
    authority_flags: SceneCommandExecutionAssemblyAuthorityFlags = field(
        default_factory=SceneCommandExecutionAssemblyAuthorityFlags
    )
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_record_id(self.result_ref, "result_ref", InvalidSceneCommandExecutionAssemblyResultError)
        _validate_record_id(self.request_ref, "request_ref", InvalidSceneCommandExecutionAssemblyResultError)
        if not isinstance(self.command_intent, SceneCommandExecutionCommandIntent):
            raise InvalidSceneCommandExecutionAssemblyResultError(
                f"command_intent must be a SceneCommandExecutionCommandIntent, got {type(self.command_intent).__name__}"
            )
        if not isinstance(self.transaction_preview, TransactionPreview):
            raise InvalidSceneCommandExecutionAssemblyResultError(
                f"transaction_preview must be a TransactionPreview, got {type(self.transaction_preview).__name__}"
            )
        if self.command_intent.command_envelope_id != self.transaction_preview.command_id:
            raise InvalidSceneCommandExecutionAssemblyResultError(
                "command_intent.command_envelope_id must match transaction_preview.command_id"
            )
        for field_name, expected_type in {
            "validation_ref": SceneCommandExecutionValidationRef,
            "resource_preview_ref": SceneCommandExecutionResourcePreviewRef,
            "state_delta_candidate_ref": SceneCommandExecutionStateDeltaCandidateRef,
            "event_ledger_candidate_ref": SceneCommandExecutionEventLedgerCandidateRef,
            "context_packet_ref": SceneCommandExecutionContextPacketRef,
            "narration_packet_ref": SceneCommandExecutionNarrationPacketRef,
            "model_boundary_fixture_ref": SceneCommandExecutionModelBoundaryFixtureRef,
        }.items():
            value = getattr(self, field_name)
            if not isinstance(value, expected_type):
                raise InvalidSceneCommandExecutionAssemblyResultError(
                    f"{field_name} must be a {expected_type.__name__}, got {type(value).__name__}"
                )
        if self.persistence_prepare_ref is not None and not isinstance(self.persistence_prepare_ref, PersistenceBoundaryRequest):
            raise InvalidSceneCommandExecutionAssemblyResultError(
                f"persistence_prepare_ref must be a PersistenceBoundaryRequest, got {type(self.persistence_prepare_ref).__name__}"
            )
        if not isinstance(self.authority_flags, SceneCommandExecutionAssemblyAuthorityFlags):
            raise InvalidSceneCommandExecutionAssemblyResultError(
                f"authority_flags must be a SceneCommandExecutionAssemblyAuthorityFlags, got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(self, "metadata", _safe_metadata(self.metadata, InvalidSceneCommandExecutionAssemblyResultError))

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_ref": self.result_ref,
            "request_ref": self.request_ref,
            "command_intent": self.command_intent.to_dict(),
            "transaction_preview": self.transaction_preview.to_dict(),
            "validation_ref": self.validation_ref.to_dict(),
            "resource_preview_ref": self.resource_preview_ref.to_dict(),
            "state_delta_candidate_ref": self.state_delta_candidate_ref.to_dict(),
            "event_ledger_candidate_ref": self.event_ledger_candidate_ref.to_dict(),
            "context_packet_ref": self.context_packet_ref.to_dict(),
            "narration_packet_ref": self.narration_packet_ref.to_dict(),
            "model_boundary_fixture_ref": self.model_boundary_fixture_ref.to_dict(),
            "persistence_prepare_ref": self.persistence_prepare_ref.to_dict() if self.persistence_prepare_ref is not None else None,
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def create_scene_command_execution_subject_ref(
    *,
    subject_type: str,
    ref_id: str,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionSubjectRef:
    return SceneCommandExecutionSubjectRef(
        subject_type=subject_type,
        ref_id=ref_id,
        metadata=metadata,
    )


def create_scene_command_execution_actor_contract(
    *,
    actor_ref: str,
    actor_label: str,
    visible_description: str,
    visible_condition_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionActorContract:
    return SceneCommandExecutionActorContract(
        actor_ref=actor_ref,
        actor_label=actor_label,
        visible_description=visible_description,
        visible_condition_refs=_safe_str_seq(
            visible_condition_refs, "visible_condition_refs", InvalidSceneCommandExecutionActorContractError
        ),
        metadata=metadata,
    )


def create_scene_command_execution_object_contract(
    *,
    object_ref: str,
    object_label: str,
    visible_description: str,
    visible_state: str,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionObjectContract:
    return SceneCommandExecutionObjectContract(
        object_ref=object_ref,
        object_label=object_label,
        visible_description=visible_description,
        visible_state=visible_state,
        metadata=metadata,
    )


def create_scene_command_execution_hidden_info_contract(
    *,
    hidden_ref: str,
    hidden_label: str,
    backend_only_description: str,
    reveal_condition: str,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionHiddenInfoContract:
    return SceneCommandExecutionHiddenInfoContract(
        hidden_ref=hidden_ref,
        hidden_label=hidden_label,
        backend_only_description=backend_only_description,
        reveal_condition=reveal_condition,
        metadata=metadata,
    )


def create_scene_command_execution_scene_contract(
    *,
    scene_ref: str,
    scene_label: str,
    visible_description: str,
    visible_tags: Sequence[str] | None = None,
    actors: Sequence[SceneCommandExecutionActorContract] | None = None,
    objects: Sequence[SceneCommandExecutionObjectContract] | None = None,
    hidden_info: Sequence[SceneCommandExecutionHiddenInfoContract] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionSceneContract:
    return SceneCommandExecutionSceneContract(
        scene_ref=scene_ref,
        scene_label=scene_label,
        visible_description=visible_description,
        visible_tags=_safe_str_seq(visible_tags, "visible_tags", InvalidSceneCommandExecutionSceneContractError),
        actors=_safe_obj_seq(
            actors, "actors", InvalidSceneCommandExecutionSceneContractError, SceneCommandExecutionActorContract
        ),
        objects=_safe_obj_seq(
            objects, "objects", InvalidSceneCommandExecutionSceneContractError, SceneCommandExecutionObjectContract
        ),
        hidden_info=_safe_obj_seq(
            hidden_info, "hidden_info", InvalidSceneCommandExecutionSceneContractError, SceneCommandExecutionHiddenInfoContract
        ),
        metadata=metadata,
    )


def create_scene_command_execution_command_intent(
    *,
    intent_ref: str,
    command_envelope_id: str,
    command_type: str,
    source_actor_ref: str,
    target_ref: str | None = None,
    payload_snapshot: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionCommandIntent:
    return SceneCommandExecutionCommandIntent(
        intent_ref=intent_ref,
        command_envelope_id=command_envelope_id,
        command_type=command_type,
        source_actor_ref=source_actor_ref,
        target_ref=target_ref,
        payload_snapshot=payload_snapshot,
        metadata=metadata,
    )


def create_scene_command_execution_command_intent_from_envelope(
    *,
    intent_ref: str,
    command_envelope: CommandEnvelope,
    target_ref: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionCommandIntent:
    """Derive a backend-owned command intent record from an existing CommandEnvelope."""
    if not validate_command_envelope(command_envelope):
        raise InvalidSceneCommandExecutionCommandIntentError(
            "command_envelope must be a valid CommandEnvelope"
        )
    return create_scene_command_execution_command_intent(
        intent_ref=intent_ref,
        command_envelope_id=command_envelope.command_id,
        command_type=command_envelope.command_type,
        source_actor_ref=command_envelope.source_actor_id,
        target_ref=target_ref,
        payload_snapshot=dict(command_envelope.payload),
        metadata=metadata,
    )


def create_scene_command_execution_validation_ref(
    *,
    validation_ref: str,
    validation_result: ValidationResult | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionValidationRef:
    return SceneCommandExecutionValidationRef(
        validation_ref=validation_ref,
        validation_result=validation_result,
        metadata=metadata,
    )


def create_scene_command_execution_resource_preview_ref(
    *,
    preview_ref: str,
    resource_math_request: ResourceMathRequest | None = None,
    resource_math_result: ResourceMathResult | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionResourcePreviewRef:
    return SceneCommandExecutionResourcePreviewRef(
        preview_ref=preview_ref,
        resource_math_request=resource_math_request,
        resource_math_result=resource_math_result,
        metadata=metadata,
    )


def create_scene_command_execution_state_delta_candidate_ref(
    *,
    delta_ref: str,
    delta_envelope: StateDeltaEnvelope | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionStateDeltaCandidateRef:
    return SceneCommandExecutionStateDeltaCandidateRef(
        delta_ref=delta_ref,
        delta_envelope=delta_envelope,
        metadata=metadata,
    )


def create_scene_command_execution_event_ledger_candidate_ref(
    *,
    event_ref: str,
    ledger_entry: EventLedgerEntry | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionEventLedgerCandidateRef:
    return SceneCommandExecutionEventLedgerCandidateRef(
        event_ref=event_ref,
        ledger_entry=ledger_entry,
        metadata=metadata,
    )


def create_scene_command_execution_context_packet_ref(
    *,
    packet_ref: str,
    context_projection: ContextProjection | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionContextPacketRef:
    return SceneCommandExecutionContextPacketRef(
        packet_ref=packet_ref,
        context_projection=context_projection,
        metadata=metadata,
    )


def create_scene_command_execution_narration_packet_ref(
    *,
    packet_ref: str,
    narration_kind: str = "post_commit_narration",
    visible_summary: str = "",
    backend_only_ref_ids: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionNarrationPacketRef:
    return SceneCommandExecutionNarrationPacketRef(
        packet_ref=packet_ref,
        narration_kind=narration_kind,
        visible_summary=visible_summary,
        backend_only_ref_ids=_safe_str_seq(
            backend_only_ref_ids, "backend_only_ref_ids", InvalidSceneCommandExecutionNarrationPacketRefError
        ),
        metadata=metadata,
    )


def create_scene_command_execution_model_boundary_fixture_ref(
    *,
    fixture_ref: str,
    fixture_kind: str = "context_narration_boundary",
    backend_truth_ref: str = "",
    model_facing_packet_refs: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionModelBoundaryFixtureRef:
    return SceneCommandExecutionModelBoundaryFixtureRef(
        fixture_ref=fixture_ref,
        fixture_kind=fixture_kind,
        backend_truth_ref=backend_truth_ref,
        model_facing_packet_refs=_safe_str_seq(
            model_facing_packet_refs, "model_facing_packet_refs", InvalidSceneCommandExecutionModelBoundaryFixtureRefError
        ),
        metadata=metadata,
    )


def create_scene_command_execution_assembly_authority_flags() -> SceneCommandExecutionAssemblyAuthorityFlags:
    """Return the default PR-9A anti-authority flag set (all False)."""
    return SceneCommandExecutionAssemblyAuthorityFlags()


def create_scene_command_execution_assembly_request(
    *,
    request_ref: str,
    scene_contract: SceneCommandExecutionSceneContract,
    command_envelope: CommandEnvelope,
    intent_target_ref: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionAssemblyRequest:
    return SceneCommandExecutionAssemblyRequest(
        request_ref=request_ref,
        scene_contract=scene_contract,
        command_envelope=command_envelope,
        intent_target_ref=intent_target_ref,
        metadata=metadata,
    )


def assemble_scene_command_execution_result(
    *,
    result_ref: str,
    request: SceneCommandExecutionAssemblyRequest,
    transaction_preview: TransactionPreview,
    validation_ref: SceneCommandExecutionValidationRef,
    resource_preview_ref: SceneCommandExecutionResourcePreviewRef,
    state_delta_candidate_ref: SceneCommandExecutionStateDeltaCandidateRef,
    event_ledger_candidate_ref: SceneCommandExecutionEventLedgerCandidateRef,
    context_packet_ref: SceneCommandExecutionContextPacketRef,
    narration_packet_ref: SceneCommandExecutionNarrationPacketRef,
    model_boundary_fixture_ref: SceneCommandExecutionModelBoundaryFixtureRef,
    persistence_prepare_ref: PersistenceBoundaryRequest | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> SceneCommandExecutionAssemblyResult:
    """Assemble a backend-owned transaction assembly result from typed references.

    Produces a deterministic, immutable result without live play, model calls,
    persistence writes, RNG execution, state mutation, event append, settlement,
    consequence application, conversion, or canon promotion.
    """
    if not isinstance(request, SceneCommandExecutionAssemblyRequest):
        raise InvalidSceneCommandExecutionAssemblyResultError(
            f"request must be a SceneCommandExecutionAssemblyRequest, got {type(request).__name__}"
        )
    if not validate_transaction_preview(transaction_preview):
        raise InvalidSceneCommandExecutionAssemblyResultError(
            "transaction_preview must be a valid TransactionPreview"
        )
    if transaction_preview.command_id != request.command_envelope.command_id:
        raise InvalidSceneCommandExecutionAssemblyResultError(
            "transaction_preview.command_id must match request.command_envelope.command_id"
        )
    safe_local_id = request.command_envelope.command_id.replace(":", "_")
    command_intent = create_scene_command_execution_command_intent_from_envelope(
        intent_ref=build_record_id("intent", safe_local_id),
        command_envelope=request.command_envelope,
        target_ref=request.intent_target_ref,
    )
    return SceneCommandExecutionAssemblyResult(
        result_ref=result_ref,
        request_ref=request.request_ref,
        command_intent=command_intent,
        transaction_preview=transaction_preview,
        validation_ref=validation_ref,
        resource_preview_ref=resource_preview_ref,
        state_delta_candidate_ref=state_delta_candidate_ref,
        event_ledger_candidate_ref=event_ledger_candidate_ref,
        context_packet_ref=context_packet_ref,
        narration_packet_ref=narration_packet_ref,
        model_boundary_fixture_ref=model_boundary_fixture_ref,
        persistence_prepare_ref=persistence_prepare_ref,
        authority_flags=create_scene_command_execution_assembly_authority_flags(),
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_scene_command_execution_subject_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionSubjectRef):
        return False
    if obj.subject_type not in _VALID_SUBJECT_TYPES:
        return False
    if not isinstance(obj.ref_id, str) or not is_valid_record_id(obj.ref_id):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_actor_contract(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionActorContract):
        return False
    if not isinstance(obj.actor_ref, str) or not is_valid_record_id(obj.actor_ref):
        return False
    if not obj.actor_label or not obj.visible_description:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_object_contract(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionObjectContract):
        return False
    if not isinstance(obj.object_ref, str) or not is_valid_record_id(obj.object_ref):
        return False
    if not obj.object_label or not obj.visible_description or not obj.visible_state:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_hidden_info_contract(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionHiddenInfoContract):
        return False
    if not isinstance(obj.hidden_ref, str) or not is_valid_record_id(obj.hidden_ref):
        return False
    if not obj.hidden_label or not obj.backend_only_description or not obj.reveal_condition:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_scene_contract(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionSceneContract):
        return False
    if not isinstance(obj.scene_ref, str) or not is_valid_record_id(obj.scene_ref):
        return False
    if not obj.scene_label or not obj.visible_description:
        return False
    if not isinstance(obj.metadata, Mapping):
        return False
    for a in obj.actors:
        if not validate_scene_command_execution_actor_contract(a):
            return False
    for o in obj.objects:
        if not validate_scene_command_execution_object_contract(o):
            return False
    for h in obj.hidden_info:
        if not validate_scene_command_execution_hidden_info_contract(h):
            return False
    return True


def validate_scene_command_execution_command_intent(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionCommandIntent):
        return False
    for attr in ("intent_ref", "command_envelope_id", "source_actor_ref"):
        value = getattr(obj, attr)
        if not isinstance(value, str) or not is_valid_record_id(value):
            return False
    if not isinstance(obj.command_type, str) or not obj.command_type:
        return False
    if obj.target_ref is not None and not is_valid_record_id(obj.target_ref):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_validation_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionValidationRef):
        return False
    if not isinstance(obj.validation_ref, str) or not is_valid_record_id(obj.validation_ref):
        return False
    if obj.validation_result is not None and not validate_validation_result(obj.validation_result):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_resource_preview_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionResourcePreviewRef):
        return False
    if not isinstance(obj.preview_ref, str) or not is_valid_record_id(obj.preview_ref):
        return False
    if obj.resource_math_request is not None and not validate_resource_math_request(obj.resource_math_request):
        return False
    if obj.resource_math_result is not None and not validate_resource_math_result(obj.resource_math_result):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_state_delta_candidate_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionStateDeltaCandidateRef):
        return False
    if not isinstance(obj.delta_ref, str) or not is_valid_record_id(obj.delta_ref):
        return False
    if obj.delta_envelope is not None and not validate_state_delta_envelope(obj.delta_envelope):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_event_ledger_candidate_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionEventLedgerCandidateRef):
        return False
    if not isinstance(obj.event_ref, str) or not is_valid_record_id(obj.event_ref):
        return False
    if obj.ledger_entry is not None and not validate_event_ledger_entry(obj.ledger_entry):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_context_packet_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionContextPacketRef):
        return False
    if not isinstance(obj.packet_ref, str) or not is_valid_record_id(obj.packet_ref):
        return False
    if obj.context_projection is not None and not validate_context_projection(obj.context_projection):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_narration_packet_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionNarrationPacketRef):
        return False
    if not isinstance(obj.packet_ref, str) or not is_valid_record_id(obj.packet_ref):
        return False
    if not isinstance(obj.narration_kind, str) or not obj.narration_kind:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_model_boundary_fixture_ref(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionModelBoundaryFixtureRef):
        return False
    if not isinstance(obj.fixture_ref, str) or not is_valid_record_id(obj.fixture_ref):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_assembly_request(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionAssemblyRequest):
        return False
    if not isinstance(obj.request_ref, str) or not is_valid_record_id(obj.request_ref):
        return False
    if not validate_scene_command_execution_scene_contract(obj.scene_contract):
        return False
    if not validate_command_envelope(obj.command_envelope):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_scene_command_execution_assembly_result(obj: Any) -> bool:
    if not isinstance(obj, SceneCommandExecutionAssemblyResult):
        return False
    if not isinstance(obj.result_ref, str) or not is_valid_record_id(obj.result_ref):
        return False
    if not isinstance(obj.request_ref, str) or not is_valid_record_id(obj.request_ref):
        return False
    if not validate_scene_command_execution_command_intent(obj.command_intent):
        return False
    if not validate_transaction_preview(obj.transaction_preview):
        return False
    for attr, validator in {
        "validation_ref": validate_scene_command_execution_validation_ref,
        "resource_preview_ref": validate_scene_command_execution_resource_preview_ref,
        "state_delta_candidate_ref": validate_scene_command_execution_state_delta_candidate_ref,
        "event_ledger_candidate_ref": validate_scene_command_execution_event_ledger_candidate_ref,
        "context_packet_ref": validate_scene_command_execution_context_packet_ref,
        "narration_packet_ref": validate_scene_command_execution_narration_packet_ref,
        "model_boundary_fixture_ref": validate_scene_command_execution_model_boundary_fixture_ref,
    }.items():
        if not validator(getattr(obj, attr)):
            return False
    if obj.persistence_prepare_ref is not None and not validate_persistence_boundary_request(obj.persistence_prepare_ref):
        return False
    if not isinstance(obj.authority_flags, SceneCommandExecutionAssemblyAuthorityFlags):
        return False
    return isinstance(obj.metadata, Mapping)


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------


def serialize_scene_command_execution_assembly_result_visible(result: SceneCommandExecutionAssemblyResult) -> dict[str, Any]:
    """Deterministic visible serialization of an assembly result.

    Omits backend-only hidden-info payloads by keeping references only.
    """
    if not validate_scene_command_execution_assembly_result(result):
        raise SceneCommandExecutionSkeletonError("result must be a valid SceneCommandExecutionAssemblyResult")
    return {
        "result_ref": result.result_ref,
        "request_ref": result.request_ref,
        "command_intent": result.command_intent.to_dict(),
        "transaction_preview": result.transaction_preview.to_dict(),
        "validation_ref": result.validation_ref.validation_ref,
        "resource_preview_ref": result.resource_preview_ref.preview_ref,
        "state_delta_candidate_ref": result.state_delta_candidate_ref.delta_ref,
        "event_ledger_candidate_ref": result.event_ledger_candidate_ref.event_ref,
        "context_packet_ref": result.context_packet_ref.packet_ref,
        "narration_packet_ref": result.narration_packet_ref.packet_ref,
        "model_boundary_fixture_ref": result.model_boundary_fixture_ref.fixture_ref,
        "authority_flags": result.authority_flags.to_dict(),
    }


def serialize_scene_command_execution_assembly_result_backend(result: SceneCommandExecutionAssemblyResult) -> dict[str, Any]:
    """Deterministic backend serialization of an assembly result (full)."""
    if not validate_scene_command_execution_assembly_result(result):
        raise SceneCommandExecutionSkeletonError("result must be a valid SceneCommandExecutionAssemblyResult")
    return result.to_dict()
