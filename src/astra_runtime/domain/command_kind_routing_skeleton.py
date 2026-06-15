"""Command-kind routing skeleton — backend-owned classification and dispatch.

RUNTIME-DOMAIN-PR-9C: defines a narrow command-kind routing layer that classifies
command intent/envelope data into known backend-owned command families and produces
dispatch-shell references. This module is a skeleton only: no legality resolution,
no command execution, no runtime mutation, no persistence, no RNG, no settlement,
no consequence application, no model calls, no prompt execution, no narration
generation, no live play, and no canon promotion.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    validate_command_envelope,
)
from astra_runtime.kernel.record_identity import build_record_id, is_valid_record_id


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class CommandKindRoutingSkeletonError(ValueError):
    """Base error for command-kind routing skeleton operations."""


class InvalidCommandKindFamilyError(CommandKindRoutingSkeletonError):
    """Raised when a command-kind family value is not recognized."""


class InvalidCommandKindDefinitionError(CommandKindRoutingSkeletonError):
    """Raised when a command-kind definition record fails validation."""


class InvalidCommandKindClassificationError(CommandKindRoutingSkeletonError):
    """Raised when a command-kind classification record fails validation."""


class InvalidCommandDispatchShellError(CommandKindRoutingSkeletonError):
    """Raised when a command dispatch shell record fails validation."""


class InvalidCommandKindRoutingRequestError(CommandKindRoutingSkeletonError):
    """Raised when a command-kind routing request record fails validation."""


class InvalidCommandKindRoutingResultError(CommandKindRoutingSkeletonError):
    """Raised when a command-kind routing result record fails validation."""


# ---------------------------------------------------------------------------
# Constants — command families
# ---------------------------------------------------------------------------


COMMAND_KIND_FAMILIES: frozenset[str] = frozenset({
    "movement",
    "inspection",
    "interaction",
    "social",
    "combat",
    "ability",
    "inventory",
    "recovery",
    "crafting",
    "travel",
    "research",
    "mission",
    "system_meta",
    "unknown",
})

_FAMILY_PREFIX_MAP: Mapping[str, str] = MappingProxyType({
    "move": "movement",
    "walk": "movement",
    "run": "movement",
    "dash": "movement",
    "climb": "movement",
    "swim": "movement",
    "fly": "movement",
    "inspect": "inspection",
    "examine": "inspection",
    "look": "inspection",
    "search": "inspection",
    "perceive": "inspection",
    "sense": "inspection",
    "interact": "interaction",
    "use": "interaction",
    "activate": "interaction",
    "open": "interaction",
    "close": "interaction",
    "toggle": "interaction",
    "social": "social",
    "persuade": "social",
    "intimidate": "social",
    "negotiate": "social",
    "diplomacy": "social",
    "deceive": "social",
    "barter": "social",
    "attack": "combat",
    "strike": "combat",
    "defend": "combat",
    "block": "combat",
    "dodge": "combat",
    "parry": "combat",
    "grapple": "combat",
    "ability": "ability",
    "cast": "ability",
    "invoke": "ability",
    "channel": "ability",
    "power": "ability",
    "technique": "ability",
    "spell": "ability",
    "inventory": "inventory",
    "equip": "inventory",
    "unequip": "inventory",
    "drop": "inventory",
    "pickup": "inventory",
    "stow": "inventory",
    "transfer": "inventory",
    "recover": "recovery",
    "rest": "recovery",
    "heal": "recovery",
    "repair": "recovery",
    "meditate": "recovery",
    "craft": "crafting",
    "build": "crafting",
    "forge": "crafting",
    "brew": "crafting",
    "assemble": "crafting",
    "salvage": "crafting",
    "travel": "travel",
    "journey": "travel",
    "navigate": "travel",
    "camp": "travel",
    "explore": "travel",
    "research": "research",
    "study": "research",
    "investigate": "research",
    "analyze": "research",
    "decipher": "research",
    "mission": "mission",
    "quest": "mission",
    "objective": "mission",
    "report": "mission",
    "system": "system_meta",
    "meta": "system_meta",
    "config": "system_meta",
    "debug": "system_meta",
    "admin": "system_meta",
    "help": "system_meta",
    "status": "system_meta",
})


# ---------------------------------------------------------------------------
# Constants — owner-route references (string-only, never called)
# ---------------------------------------------------------------------------


RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY = "RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY"
RT002_RESOURCE_CONSEQUENCE_MATH = "RT002_RESOURCE_CONSEQUENCE_MATH"
RT003_STATE_STORE_STATE_PROJECTION = "RT003_STATE_STORE_STATE_PROJECTION"
RT004_TRANSACTION_LIFECYCLE_EVENT_COMMITMENT = "RT004_TRANSACTION_LIFECYCLE_EVENT_COMMITMENT"
RT005_VALIDATION_INTEGRATION = "RT005_VALIDATION_INTEGRATION"
RT006_CONTEXT_PACKET_COMPILER = "RT006_CONTEXT_PACKET_COMPILER"
RT007_MODEL_BOUNDARY_EVALUATION = "RT007_MODEL_BOUNDARY_EVALUATION"
RT008_TINY_VERTICAL_SLICE_REFERENCE_ONLY = "RT008_TINY_VERTICAL_SLICE_REFERENCE_ONLY"
RT009_RNG_TABLE_ORACLE_REFERENCE_ONLY = "RT009_RNG_TABLE_ORACLE_REFERENCE_ONLY"
DEFERRED_RUNTIME_OWNER = "DEFERRED_RUNTIME_OWNER"
QUARANTINE_UNKNOWN_COMMAND_KIND = "QUARANTINE_UNKNOWN_COMMAND_KIND"

_OWNER_ROUTE_CONSTANTS: frozenset[str] = frozenset({
    RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    RT002_RESOURCE_CONSEQUENCE_MATH,
    RT003_STATE_STORE_STATE_PROJECTION,
    RT004_TRANSACTION_LIFECYCLE_EVENT_COMMITMENT,
    RT005_VALIDATION_INTEGRATION,
    RT006_CONTEXT_PACKET_COMPILER,
    RT007_MODEL_BOUNDARY_EVALUATION,
    RT008_TINY_VERTICAL_SLICE_REFERENCE_ONLY,
    RT009_RNG_TABLE_ORACLE_REFERENCE_ONLY,
    DEFERRED_RUNTIME_OWNER,
    QUARANTINE_UNKNOWN_COMMAND_KIND,
})

_FAMILY_DEFAULT_OWNER_ROUTES: Mapping[str, str] = MappingProxyType({
    "movement": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "inspection": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "interaction": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "social": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "combat": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "ability": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "inventory": RT002_RESOURCE_CONSEQUENCE_MATH,
    "recovery": RT002_RESOURCE_CONSEQUENCE_MATH,
    "crafting": RT002_RESOURCE_CONSEQUENCE_MATH,
    "travel": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "research": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "mission": RT001_COMMAND_LIFECYCLE_ACTION_LEGALITY,
    "system_meta": DEFERRED_RUNTIME_OWNER,
    "unknown": QUARANTINE_UNKNOWN_COMMAND_KIND,
})


# ---------------------------------------------------------------------------
# Constants — authority routing flags (all must be False)
# ---------------------------------------------------------------------------


COMMAND_KIND_ROUTING_AUTHORITY_FLAGS: frozenset[str] = frozenset({
    "legality_resolution",
    "command_execution",
    "runtime_action_execution",
    "state_mutation",
    "event_append",
    "persistence_write",
    "rng_table_oracle_execution",
    "settlement_authorization",
    "pr5_arithmetic_execution",
    "consequence_application",
    "model_authority",
    "prompt_rendering",
    "prompt_execution",
    "prose_parsing",
    "narration_generation",
    "live_play_session_authority",
    "ui_client_authority",
    "conversion",
    "sourcebook_inclusion",
    "canon_promotion",
})


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _validate_non_empty_str(value: object, name: str, error_cls: type[Exception]) -> str:
    if not isinstance(value, str) or not value.strip():
        raise error_cls(f"{name} must be a non-empty string, got {value!r}")
    return value


def _validate_record_id(value: object, name: str, error_cls: type[Exception]) -> str:
    if not isinstance(value, str) or not is_valid_record_id(value):
        raise error_cls(f"{name} must be a valid record ID, got {value!r}")
    return value


def _safe_metadata(
    metadata: Mapping[str, Any] | None, error_cls: type[Exception],
) -> Mapping[str, Any]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise error_cls(f"metadata must be a Mapping, got {type(metadata).__name__}")
    return MappingProxyType(copy.deepcopy(dict(metadata)))


# ---------------------------------------------------------------------------
# Dataclasses — frozen, keyword-only
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CommandKindDefinition:
    """Declares a command kind within a command family — metadata only."""

    kind_id: str
    family: str
    kind_label: str
    description: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "kind_id",
            _validate_non_empty_str(self.kind_id, "kind_id", InvalidCommandKindDefinitionError),
        )
        if self.family not in COMMAND_KIND_FAMILIES:
            raise InvalidCommandKindDefinitionError(
                f"family must be one of {sorted(COMMAND_KIND_FAMILIES)}, got {self.family!r}"
            )
        object.__setattr__(
            self, "kind_label",
            _validate_non_empty_str(self.kind_label, "kind_label", InvalidCommandKindDefinitionError),
        )
        object.__setattr__(
            self, "description",
            _validate_non_empty_str(self.description, "description", InvalidCommandKindDefinitionError),
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidCommandKindDefinitionError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind_id": self.kind_id,
            "family": self.family,
            "kind_label": self.kind_label,
            "description": self.description,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class CommandKindClassification:
    """Result of classifying a command into a family and kind."""

    classification_ref: str
    command_ref: str
    raw_command_type: str
    family: str
    kind: str
    classification_mode: str
    classification_source: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "classification_ref",
            _validate_record_id(self.classification_ref, "classification_ref", InvalidCommandKindClassificationError),
        )
        object.__setattr__(
            self, "command_ref",
            _validate_non_empty_str(self.command_ref, "command_ref", InvalidCommandKindClassificationError),
        )
        object.__setattr__(
            self, "raw_command_type",
            _validate_non_empty_str(self.raw_command_type, "raw_command_type", InvalidCommandKindClassificationError),
        )
        if self.family not in COMMAND_KIND_FAMILIES:
            raise InvalidCommandKindClassificationError(
                f"family must be one of {sorted(COMMAND_KIND_FAMILIES)}, got {self.family!r}"
            )
        object.__setattr__(
            self, "kind",
            _validate_non_empty_str(self.kind, "kind", InvalidCommandKindClassificationError),
        )
        object.__setattr__(
            self, "classification_mode",
            _validate_non_empty_str(self.classification_mode, "classification_mode", InvalidCommandKindClassificationError),
        )
        object.__setattr__(
            self, "classification_source",
            _validate_non_empty_str(self.classification_source, "classification_source", InvalidCommandKindClassificationError),
        )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidCommandKindClassificationError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "classification_ref": self.classification_ref,
            "command_ref": self.command_ref,
            "raw_command_type": self.raw_command_type,
            "family": self.family,
            "kind": self.kind,
            "classification_mode": self.classification_mode,
            "classification_source": self.classification_source,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class CommandDispatchShell:
    """References an intended owner surface without calling or executing it."""

    dispatch_ref: str
    command_ref: str
    owner_route: str
    family: str
    dispatch_note: str = ""
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "dispatch_ref",
            _validate_record_id(self.dispatch_ref, "dispatch_ref", InvalidCommandDispatchShellError),
        )
        object.__setattr__(
            self, "command_ref",
            _validate_non_empty_str(self.command_ref, "command_ref", InvalidCommandDispatchShellError),
        )
        if self.owner_route not in _OWNER_ROUTE_CONSTANTS:
            raise InvalidCommandDispatchShellError(
                f"owner_route must be one of {sorted(_OWNER_ROUTE_CONSTANTS)}, got {self.owner_route!r}"
            )
        if self.family not in COMMAND_KIND_FAMILIES:
            raise InvalidCommandDispatchShellError(
                f"family must be one of {sorted(COMMAND_KIND_FAMILIES)}, got {self.family!r}"
            )
        if not isinstance(self.dispatch_note, str):
            raise InvalidCommandDispatchShellError(
                f"dispatch_note must be a string, got {type(self.dispatch_note).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidCommandDispatchShellError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "dispatch_ref": self.dispatch_ref,
            "command_ref": self.command_ref,
            "owner_route": self.owner_route,
            "family": self.family,
            "dispatch_note": self.dispatch_note,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class CommandKindRoutingRequest:
    """Request to classify and route a command through the routing skeleton."""

    request_ref: str
    command_envelope: CommandEnvelope
    intent_ref: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "request_ref",
            _validate_record_id(self.request_ref, "request_ref", InvalidCommandKindRoutingRequestError),
        )
        if not validate_command_envelope(self.command_envelope):
            raise InvalidCommandKindRoutingRequestError(
                "command_envelope failed validation"
            )
        if self.intent_ref is not None:
            object.__setattr__(
                self, "intent_ref",
                _validate_record_id(self.intent_ref, "intent_ref", InvalidCommandKindRoutingRequestError),
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidCommandKindRoutingRequestError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_ref": self.request_ref,
            "command_envelope": {
                "command_id": self.command_envelope.command_id,
                "command_type": self.command_envelope.command_type,
                "source_actor_id": self.command_envelope.source_actor_id,
                "payload": copy.deepcopy(dict(self.command_envelope.payload)),
                "metadata": copy.deepcopy(dict(self.command_envelope.metadata)),
            },
            "intent_ref": self.intent_ref,
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


@dataclass(frozen=True, kw_only=True)
class CommandKindRoutingAuthorityFlags:
    """All authority flags default to False. Setting any to True raises an error."""

    legality_resolution: bool = False
    command_execution: bool = False
    runtime_action_execution: bool = False
    state_mutation: bool = False
    event_append: bool = False
    persistence_write: bool = False
    rng_table_oracle_execution: bool = False
    settlement_authorization: bool = False
    pr5_arithmetic_execution: bool = False
    consequence_application: bool = False
    model_authority: bool = False
    prompt_rendering: bool = False
    prompt_execution: bool = False
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
                raise InvalidCommandKindRoutingResultError(
                    f"authority flag '{field_name}' must be False in PR-9C skeleton, got {value!r}"
                )

    def to_dict(self) -> dict[str, Any]:
        return {field_name: False for field_name in self.__dataclass_fields__}


@dataclass(frozen=True, kw_only=True)
class CommandKindRoutingResult:
    """Result of command-kind routing: classification + dispatch shell + denied flags."""

    result_ref: str
    request_ref: str
    command_ref: str
    classification: CommandKindClassification
    dispatch_shell: CommandDispatchShell
    authority_flags: CommandKindRoutingAuthorityFlags = field(
        default_factory=CommandKindRoutingAuthorityFlags,
    )
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "result_ref",
            _validate_record_id(self.result_ref, "result_ref", InvalidCommandKindRoutingResultError),
        )
        object.__setattr__(
            self, "request_ref",
            _validate_record_id(self.request_ref, "request_ref", InvalidCommandKindRoutingResultError),
        )
        object.__setattr__(
            self, "command_ref",
            _validate_non_empty_str(self.command_ref, "command_ref", InvalidCommandKindRoutingResultError),
        )
        if not isinstance(self.classification, CommandKindClassification):
            raise InvalidCommandKindRoutingResultError(
                f"classification must be a CommandKindClassification, got {type(self.classification).__name__}"
            )
        if not isinstance(self.dispatch_shell, CommandDispatchShell):
            raise InvalidCommandKindRoutingResultError(
                f"dispatch_shell must be a CommandDispatchShell, got {type(self.dispatch_shell).__name__}"
            )
        if not isinstance(self.authority_flags, CommandKindRoutingAuthorityFlags):
            raise InvalidCommandKindRoutingResultError(
                f"authority_flags must be a CommandKindRoutingAuthorityFlags, got {type(self.authority_flags).__name__}"
            )
        object.__setattr__(
            self, "metadata",
            _safe_metadata(self.metadata, InvalidCommandKindRoutingResultError),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_ref": self.result_ref,
            "request_ref": self.request_ref,
            "command_ref": self.command_ref,
            "classification": self.classification.to_dict(),
            "dispatch_shell": self.dispatch_shell.to_dict(),
            "authority_flags": self.authority_flags.to_dict(),
            "metadata": copy.deepcopy(dict(self.metadata)),
        }


# ---------------------------------------------------------------------------
# Family classification — deterministic, pure
# ---------------------------------------------------------------------------


def classify_command_type_to_family(command_type: str) -> str:
    """Classify a command_type string into a command family using prefix matching."""
    if not isinstance(command_type, str) or not command_type.strip():
        return "unknown"
    normalized = command_type.strip().lower().replace("-", "_")
    first_token = normalized.split("_")[0] if "_" in normalized else normalized
    if first_token in _FAMILY_PREFIX_MAP:
        return _FAMILY_PREFIX_MAP[first_token]
    for prefix, family in _FAMILY_PREFIX_MAP.items():
        if normalized.startswith(prefix):
            return family
    return "unknown"


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


def create_command_kind_definition(
    *,
    kind_id: str,
    family: str,
    kind_label: str,
    description: str,
    metadata: Mapping[str, Any] | None = None,
) -> CommandKindDefinition:
    return CommandKindDefinition(
        kind_id=kind_id,
        family=family,
        kind_label=kind_label,
        description=description,
        metadata=metadata,
    )


def create_command_kind_classification(
    *,
    classification_ref: str,
    command_ref: str,
    raw_command_type: str,
    family: str,
    kind: str,
    classification_mode: str = "prefix_match",
    classification_source: str = "command_kind_routing_skeleton",
    metadata: Mapping[str, Any] | None = None,
) -> CommandKindClassification:
    return CommandKindClassification(
        classification_ref=classification_ref,
        command_ref=command_ref,
        raw_command_type=raw_command_type,
        family=family,
        kind=kind,
        classification_mode=classification_mode,
        classification_source=classification_source,
        metadata=metadata,
    )


def create_command_dispatch_shell(
    *,
    dispatch_ref: str,
    command_ref: str,
    owner_route: str,
    family: str,
    dispatch_note: str = "",
    metadata: Mapping[str, Any] | None = None,
) -> CommandDispatchShell:
    return CommandDispatchShell(
        dispatch_ref=dispatch_ref,
        command_ref=command_ref,
        owner_route=owner_route,
        family=family,
        dispatch_note=dispatch_note,
        metadata=metadata,
    )


def create_command_kind_routing_request(
    *,
    request_ref: str,
    command_envelope: CommandEnvelope,
    intent_ref: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CommandKindRoutingRequest:
    return CommandKindRoutingRequest(
        request_ref=request_ref,
        command_envelope=command_envelope,
        intent_ref=intent_ref,
        metadata=metadata,
    )


def create_command_kind_routing_authority_flags() -> CommandKindRoutingAuthorityFlags:
    return CommandKindRoutingAuthorityFlags()


def create_command_kind_routing_result(
    *,
    result_ref: str,
    request_ref: str,
    command_ref: str,
    classification: CommandKindClassification,
    dispatch_shell: CommandDispatchShell,
    metadata: Mapping[str, Any] | None = None,
) -> CommandKindRoutingResult:
    return CommandKindRoutingResult(
        result_ref=result_ref,
        request_ref=request_ref,
        command_ref=command_ref,
        classification=classification,
        dispatch_shell=dispatch_shell,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Routing — classify and dispatch from CommandEnvelope
# ---------------------------------------------------------------------------


def route_command_envelope(
    *,
    request_ref: str,
    command_envelope: CommandEnvelope,
    intent_ref: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CommandKindRoutingResult:
    """Classify and route a CommandEnvelope. Pure, deterministic, side-effect free."""
    if not validate_command_envelope(command_envelope):
        raise InvalidCommandKindRoutingRequestError(
            "command_envelope failed validation"
        )
    family = classify_command_type_to_family(command_envelope.command_type)
    owner_route = _FAMILY_DEFAULT_OWNER_ROUTES.get(family, QUARANTINE_UNKNOWN_COMMAND_KIND)

    safe_local = command_envelope.command_id.replace(":", "_")
    classification_ref = build_record_id("classification", safe_local)
    dispatch_ref = build_record_id("dispatch", safe_local)
    result_ref_id = build_record_id("routing_result", safe_local) if not is_valid_record_id(request_ref) else request_ref
    _ = result_ref_id  # just for clarity; we use request_ref below

    classification = create_command_kind_classification(
        classification_ref=classification_ref,
        command_ref=command_envelope.command_id,
        raw_command_type=command_envelope.command_type,
        family=family,
        kind=command_envelope.command_type,
        classification_mode="prefix_match",
        classification_source="command_kind_routing_skeleton",
    )

    dispatch_shell = create_command_dispatch_shell(
        dispatch_ref=dispatch_ref,
        command_ref=command_envelope.command_id,
        owner_route=owner_route,
        family=family,
    )

    result_ref_val = build_record_id("routing_result", safe_local)

    return create_command_kind_routing_result(
        result_ref=result_ref_val,
        request_ref=request_ref,
        command_ref=command_envelope.command_id,
        classification=classification,
        dispatch_shell=dispatch_shell,
        metadata=metadata,
    )


def route_command_intent(
    *,
    request_ref: str,
    intent_ref: str,
    command_envelope_id: str,
    command_type: str,
    metadata: Mapping[str, Any] | None = None,
) -> CommandKindRoutingResult:
    """Classify and route from SceneCommandExecutionCommandIntent fields.

    Accepts the relevant fields rather than importing the PR-9A dataclass
    directly, keeping the coupling reference-only.
    """
    _validate_record_id(request_ref, "request_ref", InvalidCommandKindRoutingRequestError)
    _validate_record_id(intent_ref, "intent_ref", InvalidCommandKindRoutingRequestError)
    _validate_non_empty_str(command_envelope_id, "command_envelope_id", InvalidCommandKindRoutingRequestError)
    _validate_non_empty_str(command_type, "command_type", InvalidCommandKindRoutingRequestError)

    family = classify_command_type_to_family(command_type)
    owner_route = _FAMILY_DEFAULT_OWNER_ROUTES.get(family, QUARANTINE_UNKNOWN_COMMAND_KIND)

    safe_local = command_envelope_id.replace(":", "_")
    classification_ref = build_record_id("classification", safe_local)
    dispatch_ref = build_record_id("dispatch", safe_local)
    result_ref = build_record_id("routing_result", safe_local)

    classification = create_command_kind_classification(
        classification_ref=classification_ref,
        command_ref=command_envelope_id,
        raw_command_type=command_type,
        family=family,
        kind=command_type,
        classification_mode="prefix_match",
        classification_source="command_kind_routing_skeleton",
    )

    dispatch_shell = create_command_dispatch_shell(
        dispatch_ref=dispatch_ref,
        command_ref=command_envelope_id,
        owner_route=owner_route,
        family=family,
    )

    return create_command_kind_routing_result(
        result_ref=result_ref,
        request_ref=request_ref,
        command_ref=command_envelope_id,
        classification=classification,
        dispatch_shell=dispatch_shell,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def validate_command_kind_definition(obj: Any) -> bool:
    if not isinstance(obj, CommandKindDefinition):
        return False
    if obj.family not in COMMAND_KIND_FAMILIES:
        return False
    if not obj.kind_id or not obj.kind_label or not obj.description:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_command_kind_classification(obj: Any) -> bool:
    if not isinstance(obj, CommandKindClassification):
        return False
    if not is_valid_record_id(obj.classification_ref):
        return False
    if obj.family not in COMMAND_KIND_FAMILIES:
        return False
    if not obj.command_ref or not obj.raw_command_type or not obj.kind:
        return False
    if not obj.classification_mode or not obj.classification_source:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_command_dispatch_shell(obj: Any) -> bool:
    if not isinstance(obj, CommandDispatchShell):
        return False
    if not is_valid_record_id(obj.dispatch_ref):
        return False
    if obj.owner_route not in _OWNER_ROUTE_CONSTANTS:
        return False
    if obj.family not in COMMAND_KIND_FAMILIES:
        return False
    if not obj.command_ref:
        return False
    return isinstance(obj.metadata, Mapping)


def validate_command_kind_routing_request(obj: Any) -> bool:
    if not isinstance(obj, CommandKindRoutingRequest):
        return False
    if not is_valid_record_id(obj.request_ref):
        return False
    if not validate_command_envelope(obj.command_envelope):
        return False
    if obj.intent_ref is not None and not is_valid_record_id(obj.intent_ref):
        return False
    return isinstance(obj.metadata, Mapping)


def validate_command_kind_routing_authority_flags(obj: Any) -> bool:
    if not isinstance(obj, CommandKindRoutingAuthorityFlags):
        return False
    for field_name in obj.__dataclass_fields__:
        if getattr(obj, field_name) is not False:
            return False
    return True


def validate_command_kind_routing_result(obj: Any) -> bool:
    if not isinstance(obj, CommandKindRoutingResult):
        return False
    if not is_valid_record_id(obj.result_ref):
        return False
    if not is_valid_record_id(obj.request_ref):
        return False
    if not obj.command_ref:
        return False
    if not validate_command_kind_classification(obj.classification):
        return False
    if not validate_command_dispatch_shell(obj.dispatch_shell):
        return False
    if not validate_command_kind_routing_authority_flags(obj.authority_flags):
        return False
    return isinstance(obj.metadata, Mapping)


# ---------------------------------------------------------------------------
# Deterministic serialization
# ---------------------------------------------------------------------------


def serialize_command_kind_routing_result(result: CommandKindRoutingResult) -> dict[str, Any]:
    """Full deterministic serialization of a routing result."""
    return result.to_dict()


def serialize_command_kind_routing_result_visible(result: CommandKindRoutingResult) -> dict[str, Any]:
    """Visible-only serialization — omits backend-internal metadata."""
    return {
        "result_ref": result.result_ref,
        "request_ref": result.request_ref,
        "command_ref": result.command_ref,
        "family": result.classification.family,
        "kind": result.classification.kind,
        "owner_route": result.dispatch_shell.owner_route,
        "authority_flags": result.authority_flags.to_dict(),
    }
