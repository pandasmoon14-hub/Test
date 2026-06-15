"""Action legality skeleton — RT-001B typed reference-only surfaces.

RUNTIME-DOMAIN-RT-001B: implements the RT-001A action legality vocabulary as
frozen, keyword-only, reference-only dataclasses, controlled constants,
validators, and deterministic serializers.

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


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------

class ActionLegalitySkeletonError(ValueError):
    """Base error for action legality skeleton operations."""


class InvalidActionLegalityReferenceError(ActionLegalitySkeletonError):
    """Raised when a legality reference fails validation."""


class InvalidActionLegalitySubjectReferenceError(ActionLegalitySkeletonError):
    """Raised when a subject reference fails validation."""


class InvalidActionLegalityTargetReferenceError(ActionLegalitySkeletonError):
    """Raised when a target reference fails validation."""


class InvalidActionLegalityDependencyReferenceError(ActionLegalitySkeletonError):
    """Raised when a dependency reference fails validation."""


class InvalidActionLegalityBlockerError(ActionLegalitySkeletonError):
    """Raised when a blocker fails validation."""


class InvalidActionLegalityBackendDetailError(ActionLegalitySkeletonError):
    """Raised when a backend detail fails validation."""


class InvalidActionLegalityVisibilityEnvelopeError(ActionLegalitySkeletonError):
    """Raised when a visibility envelope fails validation."""


class InvalidActionLegalityRequestError(ActionLegalitySkeletonError):
    """Raised when a legality request fails validation."""


class InvalidActionLegalityResultError(ActionLegalitySkeletonError):
    """Raised when a legality result fails validation."""


class InvalidActionLegalityAuthorityFlagsError(ActionLegalitySkeletonError):
    """Raised when authority flags contain any non-False value."""


# ---------------------------------------------------------------------------
# Legality status constants (RT-001A section 8)
# ---------------------------------------------------------------------------

LEGALITY_STATUSES = frozenset({
    "legal",
    "illegal",
    "blocked",
    "deferred",
    "quarantined",
    "unknown",
    "escalated",
})


# ---------------------------------------------------------------------------
# Blocker class constants (RT-001A section 9)
# ---------------------------------------------------------------------------

BLOCKER_CLASSES = frozenset({
    "actor_existence_reference",
    "actor_authority_capability",
    "access_permission",
    "target_existence_reference",
    "target_reachability_scope",
    "scene_location_boundary",
    "command_kind_routing",
    "validation_integration",
    "resource_prerequisite",
    "timing_cooldown_phase",
    "hidden_information",
    "ambiguity_clarification",
    "unsupported_command_family",
    "source_local_donor_specific",
    "doctrine_gap",
    "schema_gap",
    "runtime_owner_handoff",
    "policy_safety_meta_action",
    "anti_authority",
})


# ---------------------------------------------------------------------------
# Player-visible safe message constants (RT-001A section 10)
# ---------------------------------------------------------------------------

SAFE_PLAYER_MESSAGES = frozenset({
    "Invalid actor.",
    "Cannot currently attempt this action.",
    "Access denied.",
    "Requires permission.",
    "Invalid target.",
    "Target is not reachable.",
    "Target is out of range.",
    "This action is not available here.",
    "This type of action is not supported.",
    "Action could not be validated.",
    "Required resources are not available.",
    "This action cannot be taken right now.",
    "Not enough information to attempt this action.",
    "Please clarify your intended action.",
    "This action uses rules that are not currently active.",
    "This action requires further development.",
    "This action references unsupported game elements.",
    "This action cannot be processed at this time.",
    "This action is not permitted.",
    "This action has been referred for review.",
    "Action accepted.",
})

# Hidden-information blockers must use only these generic messages.
_HIDDEN_INFO_SAFE_MESSAGES = frozenset({
    "Not enough information to attempt this action.",
    "This action cannot be taken right now.",
})


# ---------------------------------------------------------------------------
# Reference kind constants
# ---------------------------------------------------------------------------

REFERENCE_KINDS = frozenset({
    "legality_result",
    "legality_request",
    "command",
    "trace",
    "scene",
    "validation",
    "packet",
    "source_local",
    "blocker",
    "backend_detail",
    "dependency",
    "subject",
    "target",
})

# ---------------------------------------------------------------------------
# Dependency owner constants
# ---------------------------------------------------------------------------

DEPENDENCY_OWNERS = frozenset({
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
})


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
class ActionLegalityReference:
    """Generic stable reference object for legality result/request IDs,
    command refs, trace refs, scene refs, validation refs, packet refs,
    and source-local refs."""

    reference_kind: str
    reference_id: str
    owner_surface: str
    summary: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.reference_kind, "reference_kind",
            InvalidActionLegalityReferenceError,
        )
        if self.reference_kind not in REFERENCE_KINDS:
            raise InvalidActionLegalityReferenceError(
                f"reference_kind must be one of {sorted(REFERENCE_KINDS)}, "
                f"got {self.reference_kind!r}"
            )
        _validate_non_empty_str(
            self.reference_id, "reference_id",
            InvalidActionLegalityReferenceError,
        )
        _validate_non_empty_str(
            self.owner_surface, "owner_surface",
            InvalidActionLegalityReferenceError,
        )
        _validate_optional_str(
            self.summary, "summary",
            InvalidActionLegalityReferenceError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidActionLegalityReferenceError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "reference_kind": self.reference_kind,
            "reference_id": self.reference_id,
            "owner_surface": self.owner_surface,
            "summary": self.summary,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalitySubjectReference:
    """Actor/subject reference — does not resolve actual actor state or
    read persistence/state store."""

    subject_id: str
    subject_label: str
    subject_kind: str = "actor"
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.subject_id, "subject_id",
            InvalidActionLegalitySubjectReferenceError,
        )
        _validate_non_empty_str(
            self.subject_label, "subject_label",
            InvalidActionLegalitySubjectReferenceError,
        )
        _validate_non_empty_str(
            self.subject_kind, "subject_kind",
            InvalidActionLegalitySubjectReferenceError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidActionLegalitySubjectReferenceError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "subject_label": self.subject_label,
            "subject_kind": self.subject_kind,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityTargetReference:
    """Target reference — does not resolve target existence."""

    target_id: str
    target_label: str
    target_role: str = "primary"
    target_type: str = "entity"
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.target_id, "target_id",
            InvalidActionLegalityTargetReferenceError,
        )
        _validate_non_empty_str(
            self.target_label, "target_label",
            InvalidActionLegalityTargetReferenceError,
        )
        _validate_non_empty_str(
            self.target_role, "target_role",
            InvalidActionLegalityTargetReferenceError,
        )
        _validate_non_empty_str(
            self.target_type, "target_type",
            InvalidActionLegalityTargetReferenceError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidActionLegalityTargetReferenceError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "target_label": self.target_label,
            "target_role": self.target_role,
            "target_type": self.target_type,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityDependencyReference:
    """Future owner handoff reference — no execution."""

    dependency_id: str
    dependency_owner: str
    summary: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.dependency_id, "dependency_id",
            InvalidActionLegalityDependencyReferenceError,
        )
        _validate_non_empty_str(
            self.dependency_owner, "dependency_owner",
            InvalidActionLegalityDependencyReferenceError,
        )
        if self.dependency_owner not in DEPENDENCY_OWNERS:
            raise InvalidActionLegalityDependencyReferenceError(
                f"dependency_owner must be one of {sorted(DEPENDENCY_OWNERS)}, "
                f"got {self.dependency_owner!r}"
            )
        _validate_optional_str(
            self.summary, "summary",
            InvalidActionLegalityDependencyReferenceError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidActionLegalityDependencyReferenceError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dependency_id": self.dependency_id,
            "dependency_owner": self.dependency_owner,
            "summary": self.summary,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityBackendDetail:
    """Backend-only diagnostic object — no player projection except through
    ActionLegalityVisibilityEnvelope."""

    detail_id: str
    blocker_class: str
    owner_route: str
    resolution_path_summary: str | None = None
    hidden_information_classification: str | None = None
    affected_refs: tuple[ActionLegalityReference, ...] = ()
    doctrine_refs: tuple[str, ...] = ()
    schema_refs: tuple[str, ...] = ()
    source_local_refs: tuple[str, ...] = ()
    severity: str = "standard"
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.detail_id, "detail_id",
            InvalidActionLegalityBackendDetailError,
        )
        _validate_non_empty_str(
            self.blocker_class, "blocker_class",
            InvalidActionLegalityBackendDetailError,
        )
        if self.blocker_class not in BLOCKER_CLASSES:
            raise InvalidActionLegalityBackendDetailError(
                f"blocker_class must be one of {sorted(BLOCKER_CLASSES)}, "
                f"got {self.blocker_class!r}"
            )
        _validate_non_empty_str(
            self.owner_route, "owner_route",
            InvalidActionLegalityBackendDetailError,
        )
        _validate_optional_str(
            self.resolution_path_summary, "resolution_path_summary",
            InvalidActionLegalityBackendDetailError,
        )
        _validate_optional_str(
            self.hidden_information_classification,
            "hidden_information_classification",
            InvalidActionLegalityBackendDetailError,
        )
        object.__setattr__(
            self, "affected_refs",
            _safe_obj_tuple(
                self.affected_refs, "affected_refs",
                InvalidActionLegalityBackendDetailError,
                ActionLegalityReference,
            ),
        )
        object.__setattr__(
            self, "doctrine_refs",
            _safe_str_tuple(
                self.doctrine_refs, "doctrine_refs",
                InvalidActionLegalityBackendDetailError,
            ),
        )
        object.__setattr__(
            self, "schema_refs",
            _safe_str_tuple(
                self.schema_refs, "schema_refs",
                InvalidActionLegalityBackendDetailError,
            ),
        )
        object.__setattr__(
            self, "source_local_refs",
            _safe_str_tuple(
                self.source_local_refs, "source_local_refs",
                InvalidActionLegalityBackendDetailError,
            ),
        )
        _validate_non_empty_str(
            self.severity, "severity",
            InvalidActionLegalityBackendDetailError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata, InvalidActionLegalityBackendDetailError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "detail_id": self.detail_id,
            "blocker_class": self.blocker_class,
            "owner_route": self.owner_route,
            "resolution_path_summary": self.resolution_path_summary,
            "hidden_information_classification": self.hidden_information_classification,
            "affected_refs": [r.to_dict() for r in self.affected_refs],
            "doctrine_refs": list(self.doctrine_refs),
            "schema_refs": list(self.schema_refs),
            "source_local_refs": list(self.source_local_refs),
            "severity": self.severity,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityBlocker:
    """Blocker record — validates blocker class, legality status, and
    player-visible safe message from controlled constants."""

    blocker_id: str
    blocker_class: str
    legality_status: str
    player_visible_message: str
    backend_detail: ActionLegalityBackendDetail | None = None
    affected_refs: tuple[ActionLegalityReference, ...] = ()
    dependency_refs: tuple[ActionLegalityDependencyReference, ...] = ()
    severity: str = "standard"
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.blocker_id, "blocker_id",
            InvalidActionLegalityBlockerError,
        )
        _validate_non_empty_str(
            self.blocker_class, "blocker_class",
            InvalidActionLegalityBlockerError,
        )
        if self.blocker_class not in BLOCKER_CLASSES:
            raise InvalidActionLegalityBlockerError(
                f"blocker_class must be one of {sorted(BLOCKER_CLASSES)}, "
                f"got {self.blocker_class!r}"
            )
        _validate_non_empty_str(
            self.legality_status, "legality_status",
            InvalidActionLegalityBlockerError,
        )
        if self.legality_status not in LEGALITY_STATUSES:
            raise InvalidActionLegalityBlockerError(
                f"legality_status must be one of {sorted(LEGALITY_STATUSES)}, "
                f"got {self.legality_status!r}"
            )
        _validate_non_empty_str(
            self.player_visible_message, "player_visible_message",
            InvalidActionLegalityBlockerError,
        )
        if self.player_visible_message not in SAFE_PLAYER_MESSAGES:
            raise InvalidActionLegalityBlockerError(
                f"player_visible_message must be one of the safe player "
                f"messages, got {self.player_visible_message!r}"
            )
        if self.blocker_class == "hidden_information":
            if self.player_visible_message not in _HIDDEN_INFO_SAFE_MESSAGES:
                raise InvalidActionLegalityBlockerError(
                    f"hidden_information blocker must use a safe generic "
                    f"message, got {self.player_visible_message!r}"
                )
        if self.backend_detail is not None and not isinstance(
            self.backend_detail, ActionLegalityBackendDetail,
        ):
            raise InvalidActionLegalityBlockerError(
                f"backend_detail must be an ActionLegalityBackendDetail, "
                f"got {type(self.backend_detail).__name__}"
            )
        object.__setattr__(
            self, "affected_refs",
            _safe_obj_tuple(
                self.affected_refs, "affected_refs",
                InvalidActionLegalityBlockerError,
                ActionLegalityReference,
            ),
        )
        object.__setattr__(
            self, "dependency_refs",
            _safe_obj_tuple(
                self.dependency_refs, "dependency_refs",
                InvalidActionLegalityBlockerError,
                ActionLegalityDependencyReference,
            ),
        )
        _validate_non_empty_str(
            self.severity, "severity",
            InvalidActionLegalityBlockerError,
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidActionLegalityBlockerError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocker_id": self.blocker_id,
            "blocker_class": self.blocker_class,
            "legality_status": self.legality_status,
            "player_visible_message": self.player_visible_message,
            "backend_detail": (
                self.backend_detail.to_dict()
                if self.backend_detail is not None else None
            ),
            "affected_refs": [r.to_dict() for r in self.affected_refs],
            "dependency_refs": [d.to_dict() for d in self.dependency_refs],
            "severity": self.severity,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityVisibilityEnvelope:
    """Separates player_visible from backend_only. Enforces safe messages
    and hidden-information containment."""

    player_visible_message: str
    player_visible_blockers: tuple[str, ...] = ()
    backend_only_detail: ActionLegalityBackendDetail | None = None
    backend_only_refs: tuple[ActionLegalityReference, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.player_visible_message, "player_visible_message",
            InvalidActionLegalityVisibilityEnvelopeError,
        )
        if self.player_visible_message not in SAFE_PLAYER_MESSAGES:
            raise InvalidActionLegalityVisibilityEnvelopeError(
                f"player_visible_message must be one of the safe player "
                f"messages, got {self.player_visible_message!r}"
            )
        safe_blocker_msgs: list[str] = []
        if self.player_visible_blockers is not None:
            if isinstance(self.player_visible_blockers, (str, bytes)):
                raise InvalidActionLegalityVisibilityEnvelopeError(
                    "player_visible_blockers must not be a bare string"
                )
            for i, msg in enumerate(self.player_visible_blockers):
                if not isinstance(msg, str) or not msg:
                    raise InvalidActionLegalityVisibilityEnvelopeError(
                        f"player_visible_blockers[{i}] must be a non-empty "
                        f"string, got {msg!r}"
                    )
                if msg not in SAFE_PLAYER_MESSAGES:
                    raise InvalidActionLegalityVisibilityEnvelopeError(
                        f"player_visible_blockers[{i}] must be a safe player "
                        f"message, got {msg!r}"
                    )
                safe_blocker_msgs.append(msg)
        object.__setattr__(
            self, "player_visible_blockers", tuple(safe_blocker_msgs),
        )
        if self.backend_only_detail is not None and not isinstance(
            self.backend_only_detail, ActionLegalityBackendDetail,
        ):
            raise InvalidActionLegalityVisibilityEnvelopeError(
                f"backend_only_detail must be an "
                f"ActionLegalityBackendDetail, "
                f"got {type(self.backend_only_detail).__name__}"
            )
        object.__setattr__(
            self, "backend_only_refs",
            _safe_obj_tuple(
                self.backend_only_refs, "backend_only_refs",
                InvalidActionLegalityVisibilityEnvelopeError,
                ActionLegalityReference,
            ),
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(
                self.metadata,
                InvalidActionLegalityVisibilityEnvelopeError,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "player_visible_message": self.player_visible_message,
            "player_visible_blockers": list(self.player_visible_blockers),
            "backend_only_detail": (
                self.backend_only_detail.to_dict()
                if self.backend_only_detail is not None else None
            ),
            "backend_only_refs": [r.to_dict() for r in self.backend_only_refs],
            "metadata": copy.deepcopy(dict(self.metadata)),
        }

    def to_player_visible_dict(self) -> dict[str, Any]:
        return {
            "player_visible_message": self.player_visible_message,
            "player_visible_blockers": list(self.player_visible_blockers),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityAuthorityFlags:
    """All authority flags must be false-only. Any non-False value raises
    during construction."""

    action_legality_engine_authorized: bool = False
    command_execution_authorized: bool = False
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
                raise InvalidActionLegalityAuthorityFlagsError(
                    f"authority flag '{field_name}' must be False in "
                    f"RT-001B skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class ActionLegalityRequest:
    """Request container — no execution, no parsing, no model or narration."""

    request_id: str
    command_ref: ActionLegalityReference
    subject_ref: ActionLegalitySubjectReference
    target_refs: tuple[ActionLegalityTargetReference, ...] = ()
    routed_command_kind_ref: ActionLegalityReference | None = None
    validation_ref: ActionLegalityReference | None = None
    transaction_preview_ref: ActionLegalityReference | None = None
    dependency_refs: tuple[ActionLegalityDependencyReference, ...] = ()
    visibility_contract_refs: tuple[ActionLegalityReference, ...] = ()
    authority_flags: ActionLegalityAuthorityFlags = field(
        default_factory=ActionLegalityAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidActionLegalityRequestError,
        )
        if not isinstance(self.command_ref, ActionLegalityReference):
            raise InvalidActionLegalityRequestError(
                f"command_ref must be an ActionLegalityReference, "
                f"got {type(self.command_ref).__name__}"
            )
        if not isinstance(self.subject_ref, ActionLegalitySubjectReference):
            raise InvalidActionLegalityRequestError(
                f"subject_ref must be an ActionLegalitySubjectReference, "
                f"got {type(self.subject_ref).__name__}"
            )
        object.__setattr__(
            self, "target_refs",
            _safe_obj_tuple(
                self.target_refs, "target_refs",
                InvalidActionLegalityRequestError,
                ActionLegalityTargetReference,
            ),
        )
        if self.routed_command_kind_ref is not None and not isinstance(
            self.routed_command_kind_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityRequestError(
                f"routed_command_kind_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.routed_command_kind_ref).__name__}"
            )
        if self.validation_ref is not None and not isinstance(
            self.validation_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityRequestError(
                f"validation_ref must be an ActionLegalityReference, "
                f"got {type(self.validation_ref).__name__}"
            )
        if self.transaction_preview_ref is not None and not isinstance(
            self.transaction_preview_ref, ActionLegalityReference,
        ):
            raise InvalidActionLegalityRequestError(
                f"transaction_preview_ref must be an "
                f"ActionLegalityReference, "
                f"got {type(self.transaction_preview_ref).__name__}"
            )
        object.__setattr__(
            self, "dependency_refs",
            _safe_obj_tuple(
                self.dependency_refs, "dependency_refs",
                InvalidActionLegalityRequestError,
                ActionLegalityDependencyReference,
            ),
        )
        object.__setattr__(
            self, "visibility_contract_refs",
            _safe_obj_tuple(
                self.visibility_contract_refs, "visibility_contract_refs",
                InvalidActionLegalityRequestError,
                ActionLegalityReference,
            ),
        )
        if not isinstance(self.authority_flags, ActionLegalityAuthorityFlags):
            raise InvalidActionLegalityRequestError(
                f"authority_flags must be an "
                f"ActionLegalityAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidActionLegalityRequestError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "command_ref": self.command_ref.to_dict(),
            "subject_ref": self.subject_ref.to_dict(),
            "target_refs": [t.to_dict() for t in self.target_refs],
            "routed_command_kind_ref": (
                self.routed_command_kind_ref.to_dict()
                if self.routed_command_kind_ref is not None else None
            ),
            "validation_ref": (
                self.validation_ref.to_dict()
                if self.validation_ref is not None else None
            ),
            "transaction_preview_ref": (
                self.transaction_preview_ref.to_dict()
                if self.transaction_preview_ref is not None else None
            ),
            "dependency_refs": [d.to_dict() for d in self.dependency_refs],
            "visibility_contract_refs": [
                v.to_dict() for v in self.visibility_contract_refs
            ],
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class ActionLegalityResult:
    """Result container — exactly one legality status, blockers, dependency
    refs, visibility envelope, trace refs, and authority flags."""

    result_id: str
    request_id: str
    legality_status: str
    blockers: tuple[ActionLegalityBlocker, ...] = ()
    dependency_refs: tuple[ActionLegalityDependencyReference, ...] = ()
    visibility_envelope: ActionLegalityVisibilityEnvelope | None = None
    trace_refs: tuple[ActionLegalityReference, ...] = ()
    authority_flags: ActionLegalityAuthorityFlags = field(
        default_factory=ActionLegalityAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(
            self.result_id, "result_id",
            InvalidActionLegalityResultError,
        )
        _validate_non_empty_str(
            self.request_id, "request_id",
            InvalidActionLegalityResultError,
        )
        _validate_non_empty_str(
            self.legality_status, "legality_status",
            InvalidActionLegalityResultError,
        )
        if self.legality_status not in LEGALITY_STATUSES:
            raise InvalidActionLegalityResultError(
                f"legality_status must be one of "
                f"{sorted(LEGALITY_STATUSES)}, "
                f"got {self.legality_status!r}"
            )
        object.__setattr__(
            self, "blockers",
            _safe_obj_tuple(
                self.blockers, "blockers",
                InvalidActionLegalityResultError,
                ActionLegalityBlocker,
            ),
        )
        if self.legality_status == "legal" and len(self.blockers) > 0:
            raise InvalidActionLegalityResultError(
                "legal result must have empty blockers"
            )
        if (
            self.legality_status not in ("legal", "unknown", "escalated")
            and len(self.blockers) == 0
        ):
            raise InvalidActionLegalityResultError(
                f"non-legal result with status {self.legality_status!r} "
                f"must have at least one blocker"
            )
        object.__setattr__(
            self, "dependency_refs",
            _safe_obj_tuple(
                self.dependency_refs, "dependency_refs",
                InvalidActionLegalityResultError,
                ActionLegalityDependencyReference,
            ),
        )
        if self.visibility_envelope is not None and not isinstance(
            self.visibility_envelope, ActionLegalityVisibilityEnvelope,
        ):
            raise InvalidActionLegalityResultError(
                f"visibility_envelope must be an "
                f"ActionLegalityVisibilityEnvelope, "
                f"got {type(self.visibility_envelope).__name__}"
            )
        object.__setattr__(
            self, "trace_refs",
            _safe_obj_tuple(
                self.trace_refs, "trace_refs",
                InvalidActionLegalityResultError,
                ActionLegalityReference,
            ),
        )
        if not isinstance(self.authority_flags, ActionLegalityAuthorityFlags):
            raise InvalidActionLegalityResultError(
                f"authority_flags must be an "
                f"ActionLegalityAuthorityFlags, "
                f"got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidActionLegalityResultError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "legality_status": self.legality_status,
            "blockers": [b.to_dict() for b in self.blockers],
            "dependency_refs": [d.to_dict() for d in self.dependency_refs],
            "visibility_envelope": (
                self.visibility_envelope.to_dict()
                if self.visibility_envelope is not None else None
            ),
            "trace_refs": [t.to_dict() for t in self.trace_refs],
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def make_action_legality_reference(
    *,
    reference_kind: str,
    reference_id: str,
    owner_surface: str,
    summary: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityReference:
    return ActionLegalityReference(
        reference_kind=reference_kind,
        reference_id=reference_id,
        owner_surface=owner_surface,
        summary=summary,
        metadata=metadata,
    )


def make_action_legality_subject_reference(
    *,
    subject_id: str,
    subject_label: str,
    subject_kind: str = "actor",
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalitySubjectReference:
    return ActionLegalitySubjectReference(
        subject_id=subject_id,
        subject_label=subject_label,
        subject_kind=subject_kind,
        metadata=metadata,
    )


def make_action_legality_target_reference(
    *,
    target_id: str,
    target_label: str,
    target_role: str = "primary",
    target_type: str = "entity",
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityTargetReference:
    return ActionLegalityTargetReference(
        target_id=target_id,
        target_label=target_label,
        target_role=target_role,
        target_type=target_type,
        metadata=metadata,
    )


def make_action_legality_dependency_reference(
    *,
    dependency_id: str,
    dependency_owner: str,
    summary: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityDependencyReference:
    return ActionLegalityDependencyReference(
        dependency_id=dependency_id,
        dependency_owner=dependency_owner,
        summary=summary,
        metadata=metadata,
    )


def make_action_legality_blocker(
    *,
    blocker_id: str,
    blocker_class: str,
    legality_status: str,
    player_visible_message: str,
    backend_detail: ActionLegalityBackendDetail | None = None,
    affected_refs: Sequence[ActionLegalityReference] | None = None,
    dependency_refs: Sequence[ActionLegalityDependencyReference] | None = None,
    severity: str = "standard",
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityBlocker:
    return ActionLegalityBlocker(
        blocker_id=blocker_id,
        blocker_class=blocker_class,
        legality_status=legality_status,
        player_visible_message=player_visible_message,
        backend_detail=backend_detail,
        affected_refs=affected_refs,
        dependency_refs=dependency_refs,
        severity=severity,
        metadata=metadata,
    )


def make_action_legality_backend_detail(
    *,
    detail_id: str,
    blocker_class: str,
    owner_route: str,
    resolution_path_summary: str | None = None,
    hidden_information_classification: str | None = None,
    affected_refs: Sequence[ActionLegalityReference] | None = None,
    doctrine_refs: Sequence[str] | None = None,
    schema_refs: Sequence[str] | None = None,
    source_local_refs: Sequence[str] | None = None,
    severity: str = "standard",
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityBackendDetail:
    return ActionLegalityBackendDetail(
        detail_id=detail_id,
        blocker_class=blocker_class,
        owner_route=owner_route,
        resolution_path_summary=resolution_path_summary,
        hidden_information_classification=hidden_information_classification,
        affected_refs=affected_refs,
        doctrine_refs=doctrine_refs,
        schema_refs=schema_refs,
        source_local_refs=source_local_refs,
        severity=severity,
        metadata=metadata,
    )


def make_action_legality_visibility_envelope(
    *,
    player_visible_message: str,
    player_visible_blockers: Sequence[str] | None = None,
    backend_only_detail: ActionLegalityBackendDetail | None = None,
    backend_only_refs: Sequence[ActionLegalityReference] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityVisibilityEnvelope:
    return ActionLegalityVisibilityEnvelope(
        player_visible_message=player_visible_message,
        player_visible_blockers=player_visible_blockers,
        backend_only_detail=backend_only_detail,
        backend_only_refs=backend_only_refs,
        metadata=metadata,
    )


def make_action_legality_request(
    *,
    request_id: str,
    command_ref: ActionLegalityReference,
    subject_ref: ActionLegalitySubjectReference,
    target_refs: Sequence[ActionLegalityTargetReference] | None = None,
    routed_command_kind_ref: ActionLegalityReference | None = None,
    validation_ref: ActionLegalityReference | None = None,
    transaction_preview_ref: ActionLegalityReference | None = None,
    dependency_refs: Sequence[ActionLegalityDependencyReference] | None = None,
    visibility_contract_refs: Sequence[ActionLegalityReference] | None = None,
    authority_flags: ActionLegalityAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityRequest:
    return ActionLegalityRequest(
        request_id=request_id,
        command_ref=command_ref,
        subject_ref=subject_ref,
        target_refs=target_refs,
        routed_command_kind_ref=routed_command_kind_ref,
        validation_ref=validation_ref,
        transaction_preview_ref=transaction_preview_ref,
        dependency_refs=dependency_refs,
        visibility_contract_refs=visibility_contract_refs,
        authority_flags=authority_flags or ActionLegalityAuthorityFlags(),
        metadata=metadata,
    )


def make_action_legality_result(
    *,
    result_id: str,
    request_id: str,
    legality_status: str,
    blockers: Sequence[ActionLegalityBlocker] | None = None,
    dependency_refs: Sequence[ActionLegalityDependencyReference] | None = None,
    visibility_envelope: ActionLegalityVisibilityEnvelope | None = None,
    trace_refs: Sequence[ActionLegalityReference] | None = None,
    authority_flags: ActionLegalityAuthorityFlags | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ActionLegalityResult:
    return ActionLegalityResult(
        result_id=result_id,
        request_id=request_id,
        legality_status=legality_status,
        blockers=blockers,
        dependency_refs=dependency_refs,
        visibility_envelope=visibility_envelope,
        trace_refs=trace_refs,
        authority_flags=authority_flags or ActionLegalityAuthorityFlags(),
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_action_legality_reference(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityReference):
        return False
    if obj.reference_kind not in REFERENCE_KINDS:
        return False
    if not isinstance(obj.reference_id, str) or not obj.reference_id:
        return False
    if not isinstance(obj.owner_surface, str) or not obj.owner_surface:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_subject_reference(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalitySubjectReference):
        return False
    if not isinstance(obj.subject_id, str) or not obj.subject_id:
        return False
    if not isinstance(obj.subject_label, str) or not obj.subject_label:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_target_reference(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityTargetReference):
        return False
    if not isinstance(obj.target_id, str) or not obj.target_id:
        return False
    if not isinstance(obj.target_label, str) or not obj.target_label:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_dependency_reference(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityDependencyReference):
        return False
    if not isinstance(obj.dependency_id, str) or not obj.dependency_id:
        return False
    if obj.dependency_owner not in DEPENDENCY_OWNERS:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_blocker(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityBlocker):
        return False
    if obj.blocker_class not in BLOCKER_CLASSES:
        return False
    if obj.legality_status not in LEGALITY_STATUSES:
        return False
    if obj.player_visible_message not in SAFE_PLAYER_MESSAGES:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_backend_detail(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityBackendDetail):
        return False
    if obj.blocker_class not in BLOCKER_CLASSES:
        return False
    if not isinstance(obj.owner_route, str) or not obj.owner_route:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_visibility_envelope(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityVisibilityEnvelope):
        return False
    if obj.player_visible_message not in SAFE_PLAYER_MESSAGES:
        return False
    for msg in obj.player_visible_blockers:
        if msg not in SAFE_PLAYER_MESSAGES:
            return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_request(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityRequest):
        return False
    if not isinstance(obj.request_id, str) or not obj.request_id:
        return False
    if not validate_action_legality_reference(obj.command_ref):
        return False
    if not validate_action_legality_subject_reference(obj.subject_ref):
        return False
    for t in obj.target_refs:
        if not validate_action_legality_target_reference(t):
            return False
    if not isinstance(obj.authority_flags, ActionLegalityAuthorityFlags):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_action_legality_result(obj: Any) -> bool:
    if not isinstance(obj, ActionLegalityResult):
        return False
    if not isinstance(obj.result_id, str) or not obj.result_id:
        return False
    if obj.legality_status not in LEGALITY_STATUSES:
        return False
    for b in obj.blockers:
        if not validate_action_legality_blocker(b):
            return False
    if not isinstance(obj.authority_flags, ActionLegalityAuthorityFlags):
        return False
    return isinstance(obj.metadata, Mapping)
