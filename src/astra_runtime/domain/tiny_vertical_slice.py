"""Tiny vertical slice — static typed state fixture and visibility boundary."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.domain.context_packet_compiler import (
    NoCommitIntentPacket,
    VisibleSummaryPacket,
    create_no_commit_intent_packet,
    create_visible_summary_packet,
    validate_no_commit_intent_packet,
    validate_visible_summary_packet,
)
from astra_runtime.domain.resource_consequence_math import (
    ConsequenceTerm,
    CostTerm,
    ResourceMathDependency,
    ResourceMathRequest,
    ResourceMathResult,
    ResourceMathSubjectReference,
    ResourceReference,
    create_consequence_term,
    create_cost_term,
    create_resource_math_dependency,
    create_resource_math_request,
    create_resource_math_result,
    create_resource_math_subject_reference,
    create_resource_reference,
)


_VALID_SEVERITIES = frozenset({"minor", "moderate", "severe"})
_VALID_COMMAND_KINDS = frozenset({"inspect_lever", "brace_mechanism", "pull_lever", "speak_to_npc"})
_VALID_VALIDATION_STATUSES = frozenset({"valid", "invalid"})
_VALID_PREVIEW_STATUSES = frozenset({"preview_available", "preview_blocked"})
_VALID_LIFECYCLE_STATUSES = frozenset({"validated_preview", "blocked"})
_VALID_COMMIT_STATUSES = frozenset({"not_requested", "blocked", "commit_ready"})
_LEVER_COMMAND_KINDS = frozenset({"inspect_lever", "brace_mechanism", "pull_lever"})


class TinyVerticalSliceError(ValueError):
    """Base error for tiny vertical slice validation failures."""


def _validate_non_empty_str(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise TinyVerticalSliceError(f"{name} must be a non-empty string, got {value!r}")
    return value


def _validate_tuple_of_non_empty_strings(value: object, name: str) -> tuple[str, ...]:
    if not isinstance(value, (tuple, list)):
        raise TinyVerticalSliceError(f"{name} must be a tuple or list, got {type(value).__name__}")
    result = []
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item:
            raise TinyVerticalSliceError(f"{name}[{i}] must be a non-empty string, got {item!r}")
        result.append(item)
    return tuple(result)


def _freeze_metadata(value: Mapping[str, Any]) -> MappingProxyType[str, Any]:
    return MappingProxyType(copy.deepcopy(dict(value)))


def _validate_bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise TinyVerticalSliceError(f"{name} must be a bool, got {value!r}")
    return value


def _validate_int_not_bool(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TinyVerticalSliceError(f"{name} must be an int (not bool), got {value!r}")
    return value


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceScene:
    scene_ref: str
    scene_label: str
    visible_description: str
    visible_tags: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.scene_ref, "scene_ref")
        _validate_non_empty_str(self.scene_label, "scene_label")
        _validate_non_empty_str(self.visible_description, "visible_description")
        normalized_tags = _validate_tuple_of_non_empty_strings(self.visible_tags, "visible_tags")
        object.__setattr__(self, "visible_tags", normalized_tags)
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceActor:
    actor_ref: str
    actor_label: str
    visible_description: str
    visible_condition_refs: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.actor_ref, "actor_ref")
        _validate_non_empty_str(self.actor_label, "actor_label")
        _validate_non_empty_str(self.visible_description, "visible_description")
        normalized = _validate_tuple_of_non_empty_strings(self.visible_condition_refs, "visible_condition_refs")
        object.__setattr__(self, "visible_condition_refs", normalized)
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceNpc:
    npc_ref: str
    npc_label: str
    visible_description: str
    visible_disposition: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.npc_ref, "npc_ref")
        _validate_non_empty_str(self.npc_label, "npc_label")
        _validate_non_empty_str(self.visible_description, "visible_description")
        _validate_non_empty_str(self.visible_disposition, "visible_disposition")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceHazardClock:
    clock_ref: str
    clock_label: str
    visible_description: str
    current_tick: int
    max_ticks: int
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.clock_ref, "clock_ref")
        _validate_non_empty_str(self.clock_label, "clock_label")
        _validate_non_empty_str(self.visible_description, "visible_description")
        _validate_int_not_bool(self.current_tick, "current_tick")
        _validate_int_not_bool(self.max_ticks, "max_ticks")
        if self.current_tick < 0:
            raise TinyVerticalSliceError(f"current_tick must be >= 0, got {self.current_tick}")
        if self.max_ticks <= 0:
            raise TinyVerticalSliceError(f"max_ticks must be > 0, got {self.max_ticks}")
        if self.current_tick > self.max_ticks:
            raise TinyVerticalSliceError(
                f"current_tick ({self.current_tick}) must be <= max_ticks ({self.max_ticks})"
            )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceLever:
    lever_ref: str
    lever_label: str
    visible_description: str
    visible_state: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.lever_ref, "lever_ref")
        _validate_non_empty_str(self.lever_label, "lever_label")
        _validate_non_empty_str(self.visible_description, "visible_description")
        _validate_non_empty_str(self.visible_state, "visible_state")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceInjury:
    injury_ref: str
    injury_label: str
    visible_description: str
    severity: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.injury_ref, "injury_ref")
        _validate_non_empty_str(self.injury_label, "injury_label")
        _validate_non_empty_str(self.visible_description, "visible_description")
        _validate_non_empty_str(self.severity, "severity")
        if self.severity not in _VALID_SEVERITIES:
            raise TinyVerticalSliceError(
                f"severity must be one of {sorted(_VALID_SEVERITIES)}, got {self.severity!r}"
            )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceHiddenFact:
    hidden_fact_ref: str
    hidden_fact_label: str
    backend_only_description: str
    reveal_condition: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.hidden_fact_ref, "hidden_fact_ref")
        _validate_non_empty_str(self.hidden_fact_label, "hidden_fact_label")
        _validate_non_empty_str(self.backend_only_description, "backend_only_description")
        _validate_non_empty_str(self.reveal_condition, "reveal_condition")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceWorldState:
    world_ref: str
    world_label: str
    scene: TinyVerticalSliceScene
    actor: TinyVerticalSliceActor
    npc: TinyVerticalSliceNpc
    hazard_clock: TinyVerticalSliceHazardClock
    lever: TinyVerticalSliceLever
    injury: TinyVerticalSliceInjury
    hidden_fact: TinyVerticalSliceHiddenFact
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.world_ref, "world_ref")
        _validate_non_empty_str(self.world_label, "world_label")
        if not isinstance(self.scene, TinyVerticalSliceScene):
            raise TinyVerticalSliceError(f"scene must be TinyVerticalSliceScene, got {type(self.scene).__name__}")
        if not isinstance(self.actor, TinyVerticalSliceActor):
            raise TinyVerticalSliceError(f"actor must be TinyVerticalSliceActor, got {type(self.actor).__name__}")
        if not isinstance(self.npc, TinyVerticalSliceNpc):
            raise TinyVerticalSliceError(f"npc must be TinyVerticalSliceNpc, got {type(self.npc).__name__}")
        if not isinstance(self.hazard_clock, TinyVerticalSliceHazardClock):
            raise TinyVerticalSliceError(f"hazard_clock must be TinyVerticalSliceHazardClock, got {type(self.hazard_clock).__name__}")
        if not isinstance(self.lever, TinyVerticalSliceLever):
            raise TinyVerticalSliceError(f"lever must be TinyVerticalSliceLever, got {type(self.lever).__name__}")
        if not isinstance(self.injury, TinyVerticalSliceInjury):
            raise TinyVerticalSliceError(f"injury must be TinyVerticalSliceInjury, got {type(self.injury).__name__}")
        if not isinstance(self.hidden_fact, TinyVerticalSliceHiddenFact):
            raise TinyVerticalSliceError(f"hidden_fact must be TinyVerticalSliceHiddenFact, got {type(self.hidden_fact).__name__}")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def create_tiny_vertical_slice_world_state(
    *,
    world_ref: str = "tiny-slice-world-1",
    world_label: str = "Tiny Vertical Slice World 1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceWorldState:
    injury = TinyVerticalSliceInjury(
        injury_ref="injury-burned-palm",
        injury_label="Burned Palm",
        visible_description="A raw burn across the right palm, stinging on contact.",
        severity="minor",
    )

    return TinyVerticalSliceWorldState(
        world_ref=world_ref,
        world_label=world_label,
        scene=TinyVerticalSliceScene(
            scene_ref="scene-threshold-chamber",
            scene_label="Threshold Chamber",
            visible_description="A small chamber with a lever, a cracked floor, and an active hazard clock.",
            visible_tags=("interior", "hazardous", "threshold"),
        ),
        actor=TinyVerticalSliceActor(
            actor_ref="actor-ascendant-1",
            actor_label="Test Ascendant",
            visible_description="A lone ascendant standing at the threshold.",
            visible_condition_refs=(injury.injury_ref,),
        ),
        npc=TinyVerticalSliceNpc(
            npc_ref="npc-watchful-adept",
            npc_label="Watchful Adept",
            visible_description="A robed figure watching from the far wall.",
            visible_disposition="wary",
        ),
        hazard_clock=TinyVerticalSliceHazardClock(
            clock_ref="hazard-clock-cracked-floor",
            clock_label="Cracked Floor Collapse Clock",
            visible_description="Cracks spread across the floor; the clock is ticking.",
            current_tick=1,
            max_ticks=4,
        ),
        lever=TinyVerticalSliceLever(
            lever_ref="lever-brass-threshold",
            lever_label="Brass Threshold Lever",
            visible_description="A brass lever mounted on the north wall.",
            visible_state="untouched",
        ),
        injury=injury,
        hidden_fact=TinyVerticalSliceHiddenFact(
            hidden_fact_ref="hidden-fact-lever-feeds-clock",
            hidden_fact_label="Lever Feeds Clock",
            backend_only_description="Pulling the lever advances the cracked-floor hazard clock unless the actor first braces the mechanism.",
            reveal_condition="Revealed only after backend validates an appropriate inspection or committed lever interaction.",
        ),
        metadata=metadata if metadata is not None else {},
    )


def _serialize_mapping(m: Mapping[str, Any]) -> dict[str, Any]:
    return dict(m)


def serialize_tiny_vertical_slice_visible_state(
    state: TinyVerticalSliceWorldState,
) -> dict[str, Any]:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}"
        )
    return {
        "world_ref": state.world_ref,
        "world_label": state.world_label,
        "scene": {
            "scene_ref": state.scene.scene_ref,
            "scene_label": state.scene.scene_label,
            "visible_description": state.scene.visible_description,
            "visible_tags": list(state.scene.visible_tags),
            "metadata": _serialize_mapping(state.scene.metadata),
        },
        "actor": {
            "actor_ref": state.actor.actor_ref,
            "actor_label": state.actor.actor_label,
            "visible_description": state.actor.visible_description,
            "visible_condition_refs": list(state.actor.visible_condition_refs),
            "metadata": _serialize_mapping(state.actor.metadata),
        },
        "npc": {
            "npc_ref": state.npc.npc_ref,
            "npc_label": state.npc.npc_label,
            "visible_description": state.npc.visible_description,
            "visible_disposition": state.npc.visible_disposition,
            "metadata": _serialize_mapping(state.npc.metadata),
        },
        "hazard_clock": {
            "clock_ref": state.hazard_clock.clock_ref,
            "clock_label": state.hazard_clock.clock_label,
            "visible_description": state.hazard_clock.visible_description,
            "current_tick": state.hazard_clock.current_tick,
            "max_ticks": state.hazard_clock.max_ticks,
            "metadata": _serialize_mapping(state.hazard_clock.metadata),
        },
        "lever": {
            "lever_ref": state.lever.lever_ref,
            "lever_label": state.lever.lever_label,
            "visible_description": state.lever.visible_description,
            "visible_state": state.lever.visible_state,
            "metadata": _serialize_mapping(state.lever.metadata),
        },
        "injury": {
            "injury_ref": state.injury.injury_ref,
            "injury_label": state.injury.injury_label,
            "visible_description": state.injury.visible_description,
            "severity": state.injury.severity,
            "metadata": _serialize_mapping(state.injury.metadata),
        },
        "metadata": _serialize_mapping(state.metadata),
    }


def serialize_tiny_vertical_slice_hidden_state_for_backend(
    state: TinyVerticalSliceWorldState,
) -> dict[str, Any]:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}"
        )
    return {
        "world_ref": state.world_ref,
        "hidden_fact": {
            "hidden_fact_ref": state.hidden_fact.hidden_fact_ref,
            "hidden_fact_label": state.hidden_fact.hidden_fact_label,
            "backend_only_description": state.hidden_fact.backend_only_description,
            "reveal_condition": state.hidden_fact.reveal_condition,
            "metadata": _serialize_mapping(state.hidden_fact.metadata),
        },
    }


# ---------------------------------------------------------------------------
# Increment 2 — Command lifecycle skeleton
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceCommandIntent:
    command_ref: str
    actor_ref: str
    command_kind: str
    target_ref: str
    declared_intent: str
    requests_commit: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.actor_ref, "actor_ref")
        _validate_non_empty_str(self.command_kind, "command_kind")
        _validate_non_empty_str(self.target_ref, "target_ref")
        _validate_non_empty_str(self.declared_intent, "declared_intent")
        _validate_bool(self.requests_commit, "requests_commit")
        if self.command_kind not in _VALID_COMMAND_KINDS:
            raise TinyVerticalSliceError(
                f"command_kind must be one of {sorted(_VALID_COMMAND_KINDS)}, got {self.command_kind!r}"
            )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def create_tiny_vertical_slice_command_intent(
    *,
    command_ref: str = "command-inspect-lever-1",
    actor_ref: str = "actor-ascendant-1",
    command_kind: str = "inspect_lever",
    target_ref: str = "lever-brass-threshold",
    declared_intent: str = "Inspect the brass threshold lever without pulling it.",
    requests_commit: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceCommandIntent:
    return TinyVerticalSliceCommandIntent(
        command_ref=command_ref,
        actor_ref=actor_ref,
        command_kind=command_kind,
        target_ref=target_ref,
        declared_intent=declared_intent,
        requests_commit=requests_commit,
        metadata=metadata if metadata is not None else {},
    )


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceCommandValidationResult:
    command_ref: str
    is_valid: bool
    validation_status: str
    reason_codes: tuple[str, ...]
    visible_explanation: str
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_bool(self.is_valid, "is_valid")
        _validate_non_empty_str(self.validation_status, "validation_status")
        if self.validation_status not in _VALID_VALIDATION_STATUSES:
            raise TinyVerticalSliceError(
                f"validation_status must be one of {sorted(_VALID_VALIDATION_STATUSES)}, got {self.validation_status!r}"
            )
        if self.is_valid and self.validation_status != "valid":
            raise TinyVerticalSliceError("validation_status must be 'valid' when is_valid is True")
        if not self.is_valid and self.validation_status != "invalid":
            raise TinyVerticalSliceError("validation_status must be 'invalid' when is_valid is False")
        normalized = _validate_tuple_of_non_empty_strings(self.reason_codes, "reason_codes")
        object.__setattr__(self, "reason_codes", normalized)
        _validate_non_empty_str(self.visible_explanation, "visible_explanation")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def validate_tiny_vertical_slice_command_intent(
    *,
    state: TinyVerticalSliceWorldState,
    command: TinyVerticalSliceCommandIntent,
) -> TinyVerticalSliceCommandValidationResult:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}")
    if not isinstance(command, TinyVerticalSliceCommandIntent):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceCommandIntent, got {type(command).__name__}")

    if command.actor_ref != state.actor.actor_ref:
        return TinyVerticalSliceCommandValidationResult(
            command_ref=command.command_ref,
            is_valid=False,
            validation_status="invalid",
            reason_codes=("actor_not_in_world",),
            visible_explanation=f"Actor ref '{command.actor_ref}' does not match the world actor.",
        )

    if command.command_kind not in _VALID_COMMAND_KINDS:
        return TinyVerticalSliceCommandValidationResult(
            command_ref=command.command_ref,
            is_valid=False,
            validation_status="invalid",
            reason_codes=("unknown_command_kind",),
            visible_explanation=f"Command kind '{command.command_kind}' is not recognized.",
        )

    if command.command_kind in _LEVER_COMMAND_KINDS:
        expected_target = state.lever.lever_ref
    else:
        expected_target = state.npc.npc_ref

    if command.target_ref != expected_target:
        return TinyVerticalSliceCommandValidationResult(
            command_ref=command.command_ref,
            is_valid=False,
            validation_status="invalid",
            reason_codes=("target_not_valid_for_command",),
            visible_explanation=f"Target ref '{command.target_ref}' is not valid for command kind '{command.command_kind}'.",
        )

    return TinyVerticalSliceCommandValidationResult(
        command_ref=command.command_ref,
        is_valid=True,
        validation_status="valid",
        reason_codes=("command_valid",),
        visible_explanation="Command is valid.",
    )


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceCommandPreviewResult:
    command_ref: str
    preview_status: str
    would_require_resolution: bool
    visible_preview: str
    visible_risk_refs: tuple[str, ...]
    visible_target_refs: tuple[str, ...]
    hidden_fact_refs_used_by_backend: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.preview_status, "preview_status")
        if self.preview_status not in _VALID_PREVIEW_STATUSES:
            raise TinyVerticalSliceError(
                f"preview_status must be one of {sorted(_VALID_PREVIEW_STATUSES)}, got {self.preview_status!r}"
            )
        _validate_bool(self.would_require_resolution, "would_require_resolution")
        _validate_non_empty_str(self.visible_preview, "visible_preview")
        object.__setattr__(self, "visible_risk_refs", _validate_tuple_of_non_empty_strings(self.visible_risk_refs, "visible_risk_refs"))
        object.__setattr__(self, "visible_target_refs", _validate_tuple_of_non_empty_strings(self.visible_target_refs, "visible_target_refs"))
        normalized_hidden = _validate_tuple_of_non_empty_strings(self.hidden_fact_refs_used_by_backend, "hidden_fact_refs_used_by_backend")
        object.__setattr__(self, "hidden_fact_refs_used_by_backend", normalized_hidden)
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def preview_tiny_vertical_slice_command_intent(
    *,
    state: TinyVerticalSliceWorldState,
    command: TinyVerticalSliceCommandIntent,
    validation: TinyVerticalSliceCommandValidationResult,
) -> TinyVerticalSliceCommandPreviewResult:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}")
    if not isinstance(command, TinyVerticalSliceCommandIntent):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceCommandIntent, got {type(command).__name__}")
    if not isinstance(validation, TinyVerticalSliceCommandValidationResult):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceCommandValidationResult, got {type(validation).__name__}")

    if not validation.is_valid:
        return TinyVerticalSliceCommandPreviewResult(
            command_ref=command.command_ref,
            preview_status="preview_blocked",
            would_require_resolution=False,
            visible_preview="Command cannot be previewed because validation failed.",
            visible_risk_refs=(),
            visible_target_refs=(),
            hidden_fact_refs_used_by_backend=(),
        )

    hidden_fact_ref = state.hidden_fact.hidden_fact_ref

    if command.command_kind == "inspect_lever":
        return TinyVerticalSliceCommandPreviewResult(
            command_ref=command.command_ref,
            preview_status="preview_available",
            would_require_resolution=False,
            visible_preview="Inspecting the lever may reveal visible details about its mechanism; backend may determine whether hidden mechanism clues become available.",
            visible_risk_refs=(),
            visible_target_refs=(state.lever.lever_ref,),
            hidden_fact_refs_used_by_backend=(hidden_fact_ref,),
        )

    if command.command_kind == "brace_mechanism":
        return TinyVerticalSliceCommandPreviewResult(
            command_ref=command.command_ref,
            preview_status="preview_available",
            would_require_resolution=False,
            visible_preview="Bracing the mechanism prepares it and may affect a later lever interaction.",
            visible_risk_refs=(),
            visible_target_refs=(state.lever.lever_ref,),
            hidden_fact_refs_used_by_backend=(hidden_fact_ref,),
        )

    if command.command_kind == "pull_lever":
        return TinyVerticalSliceCommandPreviewResult(
            command_ref=command.command_ref,
            preview_status="preview_available",
            would_require_resolution=True,
            visible_preview="Pulling the lever is risky and may interact with the hazard clock.",
            visible_risk_refs=(state.hazard_clock.clock_ref,),
            visible_target_refs=(state.lever.lever_ref,),
            hidden_fact_refs_used_by_backend=(hidden_fact_ref,),
        )

    return TinyVerticalSliceCommandPreviewResult(
        command_ref=command.command_ref,
        preview_status="preview_available",
        would_require_resolution=False,
        visible_preview="Speaking to the NPC may change social posture later, but no social engine is implemented in this increment.",
        visible_risk_refs=(),
        visible_target_refs=(state.npc.npc_ref,),
        hidden_fact_refs_used_by_backend=(),
    )


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceCommandLifecycleResult:
    command_ref: str
    lifecycle_status: str
    commit_status: str
    state_changed: bool
    event_committed: bool
    command: TinyVerticalSliceCommandIntent
    validation: TinyVerticalSliceCommandValidationResult
    preview: TinyVerticalSliceCommandPreviewResult
    resulting_state: TinyVerticalSliceWorldState
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.lifecycle_status, "lifecycle_status")
        if self.lifecycle_status not in _VALID_LIFECYCLE_STATUSES:
            raise TinyVerticalSliceError(
                f"lifecycle_status must be one of {sorted(_VALID_LIFECYCLE_STATUSES)}, got {self.lifecycle_status!r}"
            )
        _validate_non_empty_str(self.commit_status, "commit_status")
        if self.commit_status not in _VALID_COMMIT_STATUSES:
            raise TinyVerticalSliceError(
                f"commit_status must be one of {sorted(_VALID_COMMIT_STATUSES)}, got {self.commit_status!r}"
            )
        _validate_bool(self.state_changed, "state_changed")
        _validate_bool(self.event_committed, "event_committed")
        if not isinstance(self.command, TinyVerticalSliceCommandIntent):
            raise TinyVerticalSliceError(f"command must be TinyVerticalSliceCommandIntent, got {type(self.command).__name__}")
        if not isinstance(self.validation, TinyVerticalSliceCommandValidationResult):
            raise TinyVerticalSliceError(f"validation must be TinyVerticalSliceCommandValidationResult, got {type(self.validation).__name__}")
        if not isinstance(self.preview, TinyVerticalSliceCommandPreviewResult):
            raise TinyVerticalSliceError(f"preview must be TinyVerticalSliceCommandPreviewResult, got {type(self.preview).__name__}")
        if not isinstance(self.resulting_state, TinyVerticalSliceWorldState):
            raise TinyVerticalSliceError(f"resulting_state must be TinyVerticalSliceWorldState, got {type(self.resulting_state).__name__}")
        if self.command_ref != self.command.command_ref:
            raise TinyVerticalSliceError("command_ref must match command.command_ref")
        if self.command_ref != self.validation.command_ref:
            raise TinyVerticalSliceError("command_ref must match validation.command_ref")
        if self.command_ref != self.preview.command_ref:
            raise TinyVerticalSliceError("command_ref must match preview.command_ref")
        if self.state_changed is not False:
            raise TinyVerticalSliceError("state_changed must be False")
        if self.event_committed is not False:
            raise TinyVerticalSliceError("event_committed must be False")
        if not self.validation.is_valid:
            if self.lifecycle_status != "blocked":
                raise TinyVerticalSliceError(
                    f"lifecycle_status must be 'blocked' when validation is invalid, got {self.lifecycle_status!r}"
                )
            if self.commit_status != "blocked":
                raise TinyVerticalSliceError(
                    f"commit_status must be 'blocked' when validation is invalid, got {self.commit_status!r}"
                )
            if self.preview.preview_status != "preview_blocked":
                raise TinyVerticalSliceError(
                    f"preview.preview_status must be 'preview_blocked' when validation is invalid, got {self.preview.preview_status!r}"
                )
        else:
            if self.lifecycle_status != "validated_preview":
                raise TinyVerticalSliceError(
                    f"lifecycle_status must be 'validated_preview' when validation is valid, got {self.lifecycle_status!r}"
                )
            if self.command.requests_commit:
                if self.commit_status != "commit_ready":
                    raise TinyVerticalSliceError(
                        f"commit_status must be 'commit_ready' when command.requests_commit is True, got {self.commit_status!r}"
                    )
            else:
                if self.commit_status != "not_requested":
                    raise TinyVerticalSliceError(
                        f"commit_status must be 'not_requested' when command.requests_commit is False, got {self.commit_status!r}"
                    )
            if self.preview.preview_status != "preview_available":
                raise TinyVerticalSliceError(
                    f"preview.preview_status must be 'preview_available' when validation is valid, got {self.preview.preview_status!r}"
                )
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def run_tiny_vertical_slice_command_lifecycle(
    *,
    state: TinyVerticalSliceWorldState,
    command: TinyVerticalSliceCommandIntent,
) -> TinyVerticalSliceCommandLifecycleResult:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}")
    if not isinstance(command, TinyVerticalSliceCommandIntent):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceCommandIntent, got {type(command).__name__}")

    validation = validate_tiny_vertical_slice_command_intent(state=state, command=command)
    preview = preview_tiny_vertical_slice_command_intent(state=state, command=command, validation=validation)

    if not validation.is_valid:
        lifecycle_status = "blocked"
        commit_status = "blocked"
    elif command.requests_commit:
        lifecycle_status = "validated_preview"
        commit_status = "commit_ready"
    else:
        lifecycle_status = "validated_preview"
        commit_status = "not_requested"

    return TinyVerticalSliceCommandLifecycleResult(
        command_ref=command.command_ref,
        lifecycle_status=lifecycle_status,
        commit_status=commit_status,
        state_changed=False,
        event_committed=False,
        command=command,
        validation=validation,
        preview=preview,
        resulting_state=state,
    )


def serialize_tiny_vertical_slice_command_lifecycle_visible_result(
    result: TinyVerticalSliceCommandLifecycleResult,
) -> dict[str, Any]:
    if not isinstance(result, TinyVerticalSliceCommandLifecycleResult):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceCommandLifecycleResult, got {type(result).__name__}"
        )
    return {
        "command_ref": result.command_ref,
        "lifecycle_status": result.lifecycle_status,
        "commit_status": result.commit_status,
        "state_changed": result.state_changed,
        "event_committed": result.event_committed,
        "command": {
            "command_ref": result.command.command_ref,
            "actor_ref": result.command.actor_ref,
            "command_kind": result.command.command_kind,
            "target_ref": result.command.target_ref,
            "declared_intent": result.command.declared_intent,
            "requests_commit": result.command.requests_commit,
            "metadata": _serialize_mapping(result.command.metadata),
        },
        "validation": {
            "command_ref": result.validation.command_ref,
            "is_valid": result.validation.is_valid,
            "validation_status": result.validation.validation_status,
            "reason_codes": list(result.validation.reason_codes),
            "visible_explanation": result.validation.visible_explanation,
            "metadata": _serialize_mapping(result.validation.metadata),
        },
        "preview": {
            "command_ref": result.preview.command_ref,
            "preview_status": result.preview.preview_status,
            "would_require_resolution": result.preview.would_require_resolution,
            "visible_preview": result.preview.visible_preview,
            "visible_risk_refs": list(result.preview.visible_risk_refs),
            "visible_target_refs": list(result.preview.visible_target_refs),
            "metadata": _serialize_mapping(result.preview.metadata),
        },
        "resulting_visible_state": serialize_tiny_vertical_slice_visible_state(result.resulting_state),
        "metadata": _serialize_mapping(result.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 3 — Resource/consequence planning preview bridge
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceResourceConsequencePlanningPreview:
    preview_ref: str
    command_ref: str
    lifecycle_status: str
    commit_status: str
    resource_math_request: ResourceMathRequest
    resource_math_result: ResourceMathResult
    visible_summary: str
    visible_cost_refs: tuple[str, ...]
    visible_consequence_refs: tuple[str, ...]
    visible_dependency_refs: tuple[str, ...]
    backend_only_ref_ids: tuple[str, ...]
    calculation_executed: bool
    settlement_authorized: bool
    consequence_application_authorized: bool
    state_changed: bool
    event_committed: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.preview_ref, "preview_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.lifecycle_status, "lifecycle_status")
        if self.lifecycle_status not in _VALID_LIFECYCLE_STATUSES:
            raise TinyVerticalSliceError(
                f"lifecycle_status must be one of {sorted(_VALID_LIFECYCLE_STATUSES)}, got {self.lifecycle_status!r}"
            )
        _validate_non_empty_str(self.commit_status, "commit_status")
        if self.commit_status not in _VALID_COMMIT_STATUSES:
            raise TinyVerticalSliceError(
                f"commit_status must be one of {sorted(_VALID_COMMIT_STATUSES)}, got {self.commit_status!r}"
            )
        if not isinstance(self.resource_math_request, ResourceMathRequest):
            raise TinyVerticalSliceError(
                f"resource_math_request must be ResourceMathRequest, got {type(self.resource_math_request).__name__}"
            )
        if not isinstance(self.resource_math_result, ResourceMathResult):
            raise TinyVerticalSliceError(
                f"resource_math_result must be ResourceMathResult, got {type(self.resource_math_result).__name__}"
            )
        if self.resource_math_result.request_id != self.resource_math_request.request_id:
            raise TinyVerticalSliceError(
                "resource_math_result.request_id must match resource_math_request.request_id"
            )
        if self.command_ref != self.resource_math_request.command_ref_id:
            raise TinyVerticalSliceError(
                "command_ref must match resource_math_request.command_ref_id"
            )
        object.__setattr__(
            self, "visible_cost_refs", _validate_tuple_of_non_empty_strings(self.visible_cost_refs, "visible_cost_refs")
        )
        object.__setattr__(
            self, "visible_consequence_refs", _validate_tuple_of_non_empty_strings(self.visible_consequence_refs, "visible_consequence_refs")
        )
        object.__setattr__(
            self, "visible_dependency_refs", _validate_tuple_of_non_empty_strings(self.visible_dependency_refs, "visible_dependency_refs")
        )
        object.__setattr__(
            self, "backend_only_ref_ids", _validate_tuple_of_non_empty_strings(self.backend_only_ref_ids, "backend_only_ref_ids")
        )
        for field_name in (
            "calculation_executed",
            "settlement_authorized",
            "consequence_application_authorized",
            "state_changed",
            "event_committed",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_resource_consequence_planning_preview(
    *,
    state: TinyVerticalSliceWorldState,
    lifecycle_result: TinyVerticalSliceCommandLifecycleResult,
    preview_ref: str = "tiny-slice-resource-consequence-preview-1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceResourceConsequencePlanningPreview:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}")
    if not isinstance(lifecycle_result, TinyVerticalSliceCommandLifecycleResult):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceCommandLifecycleResult, got {type(lifecycle_result).__name__}"
        )
    if lifecycle_result.resulting_state is not state:
        raise TinyVerticalSliceError("lifecycle_result.resulting_state must be the supplied state object")

    command = lifecycle_result.command
    command_ref = command.command_ref
    command_kind = command.command_kind
    is_lever = command_kind in _LEVER_COMMAND_KINDS
    is_blocked = lifecycle_result.lifecycle_status == "blocked"

    actor_subject = create_resource_math_subject_reference(
        subject_binding_id="subject-actor-ascendant-1",
        subject_type="actor",
        subject_ref_id=state.actor.actor_ref,
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
        visibility_policy="actor_visible",
    )
    command_subject = create_resource_math_subject_reference(
        subject_binding_id="subject-command",
        subject_type="command",
        subject_ref_id=command_ref,
        subject_role="source_subject",
        owner_domain="RT002_resource_consequence_math",
        visibility_policy="actor_visible",
    )
    if is_lever:
        target_subject = create_resource_math_subject_reference(
            subject_binding_id="subject-target",
            subject_type="item",
            subject_ref_id=state.lever.lever_ref,
            subject_role="target_subject",
            owner_domain="RT002_resource_consequence_math",
            visibility_policy="actor_visible",
        )
    else:
        target_subject = create_resource_math_subject_reference(
            subject_binding_id="subject-target",
            subject_type="actor",
            subject_ref_id=state.npc.npc_ref,
            subject_role="target_subject",
            owner_domain="RT002_resource_consequence_math",
            visibility_policy="actor_visible",
        )
    subject_refs = (actor_subject, command_subject, target_subject)

    resource_refs: list[ResourceReference] = []
    cost_terms: list[CostTerm] = []
    consequence_terms: list[ConsequenceTerm] = []

    if command_kind == "pull_lever":
        resource_refs.append(
            create_resource_reference(
                resource_ref_id="resource-hazard-clock-pressure",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_family="risk_heat",
                resource_key="cracked_floor_clock_pressure",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
        cost_terms.append(
            create_cost_term(
                term_id="cost-pull-lever-risky-interaction",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_ref_id="resource-hazard-clock-pressure",
                value_mode="resource_reference_only",
                cost_family="activation",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
        consequence_terms.append(
            create_consequence_term(
                consequence_id="consequence-pull-lever-hazard-escalation",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_ref_id="resource-hazard-clock-pressure",
                value_mode="resource_reference_only",
                consequence_family="escalation",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
    elif command_kind == "inspect_lever":
        resource_refs.append(
            create_resource_reference(
                resource_ref_id="resource-lever-mechanism-clue",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_family="clue_information",
                resource_key="lever_mechanism_clue",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
        consequence_terms.append(
            create_consequence_term(
                consequence_id="consequence-inspect-lever-clue-route",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_ref_id="resource-lever-mechanism-clue",
                value_mode="resource_reference_only",
                consequence_family="clue_route",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
    elif command_kind == "brace_mechanism":
        resource_refs.append(
            create_resource_reference(
                resource_ref_id="resource-mechanism-bracing-position",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_family="opportunity",
                resource_key="mechanism_bracing_position",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
        consequence_terms.append(
            create_consequence_term(
                consequence_id="consequence-brace-mechanism-preparation",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_ref_id="resource-mechanism-bracing-position",
                value_mode="resource_reference_only",
                consequence_family="visibility_change",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
    elif command_kind == "speak_to_npc":
        resource_refs.append(
            create_resource_reference(
                resource_ref_id="resource-watchful-adept-social-posture",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_family="social_capital",
                resource_key="watchful_adept_social_posture",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )
        consequence_terms.append(
            create_consequence_term(
                consequence_id="consequence-speak-npc-social-posture",
                subject_binding_id=actor_subject.subject_binding_id,
                resource_ref_id="resource-watchful-adept-social-posture",
                value_mode="resource_reference_only",
                consequence_family="social_faction_change",
                owner_domain="RT002_resource_consequence_math",
                visibility_policy="actor_visible",
            )
        )

    dependencies: list[ResourceMathDependency] = [
        create_resource_math_dependency(
            dependency_id="dep-command-ref",
            dependency_type="command_ref",
            reference_id=command_ref,
            owner_domain="RT002_resource_consequence_math",
            required=True,
            satisfied=True,
            hidden_info_safe=True,
        )
    ]
    if is_lever:
        dependencies.append(
            create_resource_math_dependency(
                dependency_id="dep-hidden-fact-lever-clock",
                dependency_type="hidden_information_ref",
                reference_id=state.hidden_fact.hidden_fact_ref,
                owner_domain="RT002_resource_consequence_math",
                required=False,
                satisfied=True,
                hidden_info_safe=True,
            )
        )

    request_id = f"resource-math-request-{command_ref}"
    trace_ref_id = f"tiny-slice-trace-{command_ref}"
    request = create_resource_math_request(
        request_id=request_id,
        trace_ref_id=trace_ref_id,
        subject_refs=subject_refs,
        command_ref_id=command_ref,
        resource_refs=resource_refs,
        cost_terms=cost_terms,
        consequence_terms=consequence_terms,
        dependencies=dependencies,
        metadata={
            "preview_ref": preview_ref,
            "world_ref": state.world_ref,
            "command_ref": command_ref,
            "command_kind": command_kind,
            "lifecycle_status": lifecycle_result.lifecycle_status,
            "commit_status": lifecycle_result.commit_status,
            "runtime_increment": 3,
        },
    )

    result = create_resource_math_result(
        result_id=f"resource-math-result-{command_ref}",
        request_id=request_id,
        trace_ref_id=trace_ref_id,
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        diagnostics=("reference_only_planning_preview",),
        normalized_reference_ids=(request_id, command_ref),
        request=request,
        metadata={
            "preview_ref": preview_ref,
            "world_ref": state.world_ref,
            "command_ref": command_ref,
            "command_kind": command_kind,
            "reference_only": True,
            "runtime_increment": 3,
        },
    )

    if is_blocked:
        visible_summary = "Resource and consequence planning preview is blocked because the command lifecycle is blocked."
    else:
        visible_summary = "Resource and consequence planning preview is available; no calculation, settlement, state mutation, or event commitment has occurred."

    return TinyVerticalSliceResourceConsequencePlanningPreview(
        preview_ref=preview_ref,
        command_ref=command_ref,
        lifecycle_status=lifecycle_result.lifecycle_status,
        commit_status=lifecycle_result.commit_status,
        resource_math_request=request,
        resource_math_result=result,
        visible_summary=visible_summary,
        visible_cost_refs=tuple(t.term_id for t in cost_terms),
        visible_consequence_refs=tuple(t.consequence_id for t in consequence_terms),
        visible_dependency_refs=tuple(d.dependency_id for d in dependencies),
        backend_only_ref_ids=(state.hidden_fact.hidden_fact_ref,),
        calculation_executed=False,
        settlement_authorized=False,
        consequence_application_authorized=False,
        state_changed=False,
        event_committed=False,
        metadata=metadata if metadata is not None else {},
    )


def _strip_backend_refs(value: Any, backend_ids: set[str]) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_backend_refs(val, backend_ids)
            for key, val in value.items()
            if not (isinstance(val, str) and val in backend_ids)
        }
    if isinstance(value, list):
        return [
            _strip_backend_refs(item, backend_ids)
            for item in value
            if not (isinstance(item, str) and item in backend_ids)
        ]
    return value


def serialize_tiny_vertical_slice_resource_consequence_planning_visible_preview(
    preview: TinyVerticalSliceResourceConsequencePlanningPreview,
) -> dict[str, Any]:
    if not isinstance(preview, TinyVerticalSliceResourceConsequencePlanningPreview):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceResourceConsequencePlanningPreview, got {type(preview).__name__}"
        )
    backend_ids = set(preview.backend_only_ref_ids)
    request_dict = _strip_backend_refs(preview.resource_math_request.to_dict(), backend_ids)
    result_dict = _strip_backend_refs(preview.resource_math_result.to_dict(), backend_ids)
    return {
        "preview_ref": preview.preview_ref,
        "command_ref": preview.command_ref,
        "lifecycle_status": preview.lifecycle_status,
        "commit_status": preview.commit_status,
        "visible_summary": preview.visible_summary,
        "visible_cost_refs": list(preview.visible_cost_refs),
        "visible_consequence_refs": list(preview.visible_consequence_refs),
        "visible_dependency_refs": list(preview.visible_dependency_refs),
        "calculation_executed": preview.calculation_executed,
        "settlement_authorized": preview.settlement_authorized,
        "consequence_application_authorized": preview.consequence_application_authorized,
        "state_changed": preview.state_changed,
        "event_committed": preview.event_committed,
        "resource_math_request": request_dict,
        "resource_math_result": result_dict,
        "metadata": _serialize_mapping(preview.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 4 — Context packet projection bridge
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceContextPacketProjection:
    projection_ref: str
    command_ref: str
    world_ref: str
    no_commit_intent_packet: NoCommitIntentPacket
    visible_summary_packet: VisibleSummaryPacket
    packet_refs: tuple[str, ...]
    visible_packet_kinds: tuple[str, ...]
    visible_context_refs: tuple[str, ...]
    excluded_backend_ref_ids: tuple[str, ...]
    hidden_information_excluded: bool
    state_changed: bool
    event_committed: bool
    model_called: bool
    narration_generated: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.projection_ref, "projection_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")
        if not isinstance(self.no_commit_intent_packet, NoCommitIntentPacket):
            raise TinyVerticalSliceError(
                f"no_commit_intent_packet must be NoCommitIntentPacket, got {type(self.no_commit_intent_packet).__name__}"
            )
        if not isinstance(self.visible_summary_packet, VisibleSummaryPacket):
            raise TinyVerticalSliceError(
                f"visible_summary_packet must be VisibleSummaryPacket, got {type(self.visible_summary_packet).__name__}"
            )
        object.__setattr__(self, "packet_refs", _validate_tuple_of_non_empty_strings(self.packet_refs, "packet_refs"))
        object.__setattr__(
            self, "visible_packet_kinds", _validate_tuple_of_non_empty_strings(self.visible_packet_kinds, "visible_packet_kinds")
        )
        object.__setattr__(
            self, "visible_context_refs", _validate_tuple_of_non_empty_strings(self.visible_context_refs, "visible_context_refs")
        )
        object.__setattr__(
            self, "excluded_backend_ref_ids", _validate_tuple_of_non_empty_strings(self.excluded_backend_ref_ids, "excluded_backend_ref_ids")
        )
        expected_packet_refs = {
            self.no_commit_intent_packet.intent_ref,
            self.visible_summary_packet.summary_ref,
        }
        if set(self.packet_refs) != expected_packet_refs:
            raise TinyVerticalSliceError(
                "packet_refs must contain exactly the no_commit_intent_packet.intent_ref and visible_summary_packet.summary_ref"
            )
        if self.visible_packet_kinds != ("no_commit_intent", "visible_summary"):
            raise TinyVerticalSliceError(
                f"visible_packet_kinds must be ('no_commit_intent', 'visible_summary'), got {self.visible_packet_kinds!r}"
            )
        for field_name in ("hidden_information_excluded",):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not True:
                raise TinyVerticalSliceError(f"{field_name} must be True")
        for field_name in (
            "state_changed",
            "event_committed",
            "model_called",
            "narration_generated",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_context_packet_projection(
    *,
    state: TinyVerticalSliceWorldState,
    lifecycle_result: TinyVerticalSliceCommandLifecycleResult,
    planning_preview: TinyVerticalSliceResourceConsequencePlanningPreview,
    projection_ref: str = "tiny-slice-context-packet-projection-1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceContextPacketProjection:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}")
    if not isinstance(lifecycle_result, TinyVerticalSliceCommandLifecycleResult):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceCommandLifecycleResult, got {type(lifecycle_result).__name__}"
        )
    if not isinstance(planning_preview, TinyVerticalSliceResourceConsequencePlanningPreview):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceResourceConsequencePlanningPreview, got {type(planning_preview).__name__}"
        )
    if lifecycle_result.resulting_state is not state:
        raise TinyVerticalSliceError("lifecycle_result.resulting_state must be the supplied state object")
    command = lifecycle_result.command
    command_ref = command.command_ref
    if planning_preview.command_ref != command_ref:
        raise TinyVerticalSliceError("planning_preview.command_ref must match lifecycle_result.command.command_ref")
    if planning_preview.resource_math_request.command_ref_id != command_ref:
        raise TinyVerticalSliceError(
            "planning_preview.resource_math_request.command_ref_id must match lifecycle_result.command.command_ref"
        )

    is_lever = command.command_kind in _LEVER_COMMAND_KINDS
    intent_timestamp = "tiny-slice-static-t0"
    summary_timestamp = "tiny-slice-static-t0"

    visible_context_refs: list[str] = [
        state.world_ref,
        state.scene.scene_ref,
        state.actor.actor_ref,
        state.injury.injury_ref,
        command_ref,
        planning_preview.preview_ref,
    ]
    if is_lever:
        visible_context_refs.append(state.lever.lever_ref)
    else:
        visible_context_refs.append(state.npc.npc_ref)
    if command.command_kind == "pull_lever":
        visible_context_refs.append(state.hazard_clock.clock_ref)
    visible_context_refs = list(dict.fromkeys(visible_context_refs))

    declared_resource_refs = tuple(
        r.resource_ref_id for r in planning_preview.resource_math_request.resource_refs
    )
    declared_cost_refs = planning_preview.visible_cost_refs

    no_commit_packet = create_no_commit_intent_packet(
        intent_ref=command_ref,
        actor_ref=command.actor_ref,
        proposed_action_kind=command.command_kind,
        intent_timestamp=intent_timestamp,
        target_refs=(command.target_ref,),
        declared_resource_refs=declared_resource_refs,
        declared_cost_refs=declared_cost_refs,
        visible_context_refs=tuple(visible_context_refs),
        confirmation_required=True,
        hidden_information_excluded=True,
        no_commit_marker=True,
        metadata={
            "projection_ref": projection_ref,
            "world_ref": state.world_ref,
            "command_ref": command_ref,
            "lifecycle_status": lifecycle_result.lifecycle_status,
            "commit_status": lifecycle_result.commit_status,
            "runtime_increment": 4,
        },
    )

    visible_fact_refs: list[str] = [
        state.world_ref,
        state.scene.scene_ref,
        state.actor.actor_ref,
        state.npc.npc_ref,
        state.hazard_clock.clock_ref,
        state.injury.injury_ref,
        command_ref,
        planning_preview.preview_ref,
    ]
    if is_lever:
        visible_fact_refs.append(state.lever.lever_ref)
    visible_fact_refs = list(dict.fromkeys(visible_fact_refs))

    item_refs = (state.lever.lever_ref,) if is_lever else ()

    forbidden_claims = (
        "do_not_claim_state_changed",
        "do_not_claim_event_committed",
        "do_not_claim_hidden_fact",
        "do_not_roll_" + "dice",
        "do_not_resolve_action",
        "do_not_generate_reward",
    )

    visible_summary_packet = create_visible_summary_packet(
        summary_ref=f"tiny-slice-visible-summary-{command_ref}",
        summary_scope="tiny_vertical_slice_runtime_preview",
        summary_timestamp=summary_timestamp,
        visible_fact_refs=tuple(visible_fact_refs),
        actor_refs=(state.actor.actor_ref, state.npc.npc_ref),
        location_refs=(state.scene.scene_ref,),
        item_refs=item_refs,
        condition_refs=(state.injury.injury_ref,),
        unresolved_visible_refs=planning_preview.visible_dependency_refs,
        forbidden_claims=forbidden_claims,
        hidden_information_excluded=True,
        committed_state_only=True,
        metadata={
            "projection_ref": projection_ref,
            "world_ref": state.world_ref,
            "command_ref": command_ref,
            "planning_preview_ref": planning_preview.preview_ref,
            "lifecycle_status": lifecycle_result.lifecycle_status,
            "commit_status": lifecycle_result.commit_status,
            "runtime_increment": 4,
        },
    )

    all_visible_context_refs = list(dict.fromkeys(visible_context_refs + list(visible_fact_refs)))

    return TinyVerticalSliceContextPacketProjection(
        projection_ref=projection_ref,
        command_ref=command_ref,
        world_ref=state.world_ref,
        no_commit_intent_packet=no_commit_packet,
        visible_summary_packet=visible_summary_packet,
        packet_refs=(no_commit_packet.intent_ref, visible_summary_packet.summary_ref),
        visible_packet_kinds=("no_commit_intent", "visible_summary"),
        visible_context_refs=tuple(all_visible_context_refs),
        excluded_backend_ref_ids=(state.hidden_fact.hidden_fact_ref,),
        hidden_information_excluded=True,
        state_changed=False,
        event_committed=False,
        model_called=False,
        narration_generated=False,
        metadata=metadata if metadata is not None else {},
    )


def serialize_tiny_vertical_slice_context_packet_projection_visible(
    projection: TinyVerticalSliceContextPacketProjection,
) -> dict[str, Any]:
    if not isinstance(projection, TinyVerticalSliceContextPacketProjection):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceContextPacketProjection, got {type(projection).__name__}"
        )
    return {
        "projection_ref": projection.projection_ref,
        "command_ref": projection.command_ref,
        "world_ref": projection.world_ref,
        "packet_refs": list(projection.packet_refs),
        "visible_packet_kinds": list(projection.visible_packet_kinds),
        "visible_context_refs": list(projection.visible_context_refs),
        "hidden_information_excluded": projection.hidden_information_excluded,
        "state_changed": projection.state_changed,
        "event_committed": projection.event_committed,
        "model_called": projection.model_called,
        "narration_generated": projection.narration_generated,
        "no_commit_intent_packet": projection.no_commit_intent_packet.to_dict(),
        "visible_summary_packet": projection.visible_summary_packet.to_dict(),
        "metadata": _serialize_mapping(projection.metadata),
    }
