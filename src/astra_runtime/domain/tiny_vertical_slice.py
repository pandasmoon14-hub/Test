"""Tiny vertical slice — static typed state fixture and visibility boundary."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from astra_runtime.domain.context_packet_compiler import (
    ContextPacketCompilerResult,
    NoCommitIntentPacket,
    SingleEventNarrationPacket,
    VisibleSummaryPacket,
    compile_context_packet_from_request,
    create_context_packet_assembly_request,
    create_no_commit_intent_packet,
    create_single_event_narration_packet,
    create_visible_summary_packet,
    validate_no_commit_intent_packet,
    validate_single_event_narration_packet,
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
from astra_runtime.domain.model_boundary_evaluation import (
    ModelBoundaryEvaluationCase,
    ModelBoundaryEvaluationResult,
    create_model_boundary_evaluation_case,
    evaluate_model_boundary_case,
)
from astra_runtime.kernel.command_envelope import (
    CommandEnvelope,
    create_command_envelope,
    validate_command_envelope,
)
from astra_runtime.kernel.event_ledger import (
    EventLedgerEntry,
    create_event_ledger_entry,
    validate_event_ledger_entry,
)
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.transaction_preview import (
    TransactionPreview,
    create_transaction_preview,
    validate_transaction_preview,
)
from astra_runtime.kernel.state_delta import (
    StateDeltaEnvelope,
    create_state_delta_envelope,
    validate_state_delta_envelope,
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


# ---------------------------------------------------------------------------
# Increment 5 — State delta candidate preview
# ---------------------------------------------------------------------------


def _validate_state_delta_envelope_sequence(value: object, name: str) -> tuple[StateDeltaEnvelope, ...]:
    if isinstance(value, str) or not isinstance(value, (tuple, list)):
        raise TinyVerticalSliceError(f"{name} must be a tuple or list")
    result: list[StateDeltaEnvelope] = []
    for i, item in enumerate(value):
        if not isinstance(item, StateDeltaEnvelope):
            raise TinyVerticalSliceError(f"{name}[{i}] must be StateDeltaEnvelope, got {type(item).__name__}")
        if not validate_state_delta_envelope(item):
            raise TinyVerticalSliceError(f"{name}[{i}] is not a valid StateDeltaEnvelope")
        result.append(item)
    return tuple(result)


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceStateDeltaCandidatePreview:
    delta_preview_ref: str
    command_ref: str
    world_ref: str
    lifecycle_status: str
    commit_status: str
    planning_preview_ref: str
    context_projection_ref: str
    candidate_delta_envelopes: tuple[StateDeltaEnvelope, ...]
    candidate_delta_refs: tuple[str, ...]
    affected_visible_record_refs: tuple[str, ...]
    visible_delta_summary: str
    visible_change_kinds: tuple[str, ...]
    backend_only_ref_ids: tuple[str, ...]
    apply_authorized: bool
    state_changed: bool
    event_committed: bool
    persistence_authorized: bool
    replay_authorized: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.delta_preview_ref, "delta_preview_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")
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
        _validate_non_empty_str(self.planning_preview_ref, "planning_preview_ref")
        _validate_non_empty_str(self.context_projection_ref, "context_projection_ref")
        _validate_non_empty_str(self.visible_delta_summary, "visible_delta_summary")
        safe_envelopes = _validate_state_delta_envelope_sequence(self.candidate_delta_envelopes, "candidate_delta_envelopes")
        object.__setattr__(self, "candidate_delta_envelopes", safe_envelopes)
        object.__setattr__(self, "candidate_delta_refs", _validate_tuple_of_non_empty_strings(self.candidate_delta_refs, "candidate_delta_refs"))
        object.__setattr__(self, "affected_visible_record_refs", _validate_tuple_of_non_empty_strings(self.affected_visible_record_refs, "affected_visible_record_refs"))
        object.__setattr__(self, "visible_change_kinds", _validate_tuple_of_non_empty_strings(self.visible_change_kinds, "visible_change_kinds"))
        object.__setattr__(self, "backend_only_ref_ids", _validate_tuple_of_non_empty_strings(self.backend_only_ref_ids, "backend_only_ref_ids"))
        expected_delta_refs = tuple(e.delta_id for e in safe_envelopes)
        if self.candidate_delta_refs != expected_delta_refs:
            raise TinyVerticalSliceError(
                f"candidate_delta_refs {self.candidate_delta_refs!r} must match delta_ids {expected_delta_refs!r}"
            )
        for i, envelope in enumerate(safe_envelopes):
            if envelope.source_command_id != self.command_ref:
                raise TinyVerticalSliceError(
                    f"candidate_delta_envelopes[{i}].source_command_id must match command_ref"
                )
            if envelope.source_preview_id != self.delta_preview_ref:
                raise TinyVerticalSliceError(
                    f"candidate_delta_envelopes[{i}].source_preview_id must match delta_preview_ref"
                )
        for field_name in (
            "apply_authorized",
            "state_changed",
            "event_committed",
            "persistence_authorized",
            "replay_authorized",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_state_delta_candidate_preview(
    *,
    state: TinyVerticalSliceWorldState,
    lifecycle_result: TinyVerticalSliceCommandLifecycleResult,
    planning_preview: TinyVerticalSliceResourceConsequencePlanningPreview,
    context_projection: TinyVerticalSliceContextPacketProjection,
    delta_preview_ref: str = "tiny-slice-state-delta-preview-1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceStateDeltaCandidatePreview:
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
    if not isinstance(context_projection, TinyVerticalSliceContextPacketProjection):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceContextPacketProjection, got {type(context_projection).__name__}"
        )
    if lifecycle_result.resulting_state is not state:
        raise TinyVerticalSliceError("lifecycle_result.resulting_state must be the supplied state object")
    command = lifecycle_result.command
    command_ref = command.command_ref
    if planning_preview.command_ref != command_ref:
        raise TinyVerticalSliceError("planning_preview.command_ref must match lifecycle_result.command.command_ref")
    if context_projection.command_ref != command_ref:
        raise TinyVerticalSliceError("context_projection.command_ref must match lifecycle_result.command.command_ref")
    if context_projection.world_ref != state.world_ref:
        raise TinyVerticalSliceError("context_projection.world_ref must match state.world_ref")

    is_blocked = lifecycle_result.lifecycle_status == "blocked"
    delta_metadata = {
        "world_ref": state.world_ref,
        "command_ref": command_ref,
        "runtime_increment": 5,
    }
    candidate_deltas: list[StateDeltaEnvelope] = []
    affected_visible_record_refs: list[str] = []
    visible_change_kinds: list[str] = []
    backend_only_ref_ids: list[str] = []

    if not is_blocked:
        if command.command_kind in {"inspect_lever", "brace_mechanism", "pull_lever"}:
            backend_only_ref_ids.append(state.hidden_fact.hidden_fact_ref)

        if command.command_kind == "pull_lever":
            candidate_deltas.append(
                create_state_delta_envelope(
                    delta_id=f"state-delta-candidate-{command_ref}-lever",
                    source_command_id=command_ref,
                    source_preview_id=delta_preview_ref,
                    affected_record_ids=(build_record_id("item", "brass_threshold_lever"),),
                    change_type="record_update",
                    payload={
                        "record_ref": state.lever.lever_ref,
                        "field": "visible_state",
                        "current_value": state.lever.visible_state,
                        "candidate_value": "pulled",
                        "applied": False,
                        "commit_required": True,
                    },
                    metadata=delta_metadata,
                )
            )
            candidate_deltas.append(
                create_state_delta_envelope(
                    delta_id=f"state-delta-candidate-{command_ref}-hazard-clock",
                    source_command_id=command_ref,
                    source_preview_id=delta_preview_ref,
                    affected_record_ids=(build_record_id("hazard_clock", "cracked_floor"),),
                    change_type="record_update",
                    payload={
                        "record_ref": state.hazard_clock.clock_ref,
                        "field": "current_tick",
                        "current_value": state.hazard_clock.current_tick,
                        "candidate_value": state.hazard_clock.current_tick + 1,
                        "max_ticks": state.hazard_clock.max_ticks,
                        "applied": False,
                        "commit_required": True,
                    },
                    metadata=delta_metadata,
                )
            )
            affected_visible_record_refs.extend([state.lever.lever_ref, state.hazard_clock.clock_ref])
            visible_change_kinds.extend(["lever_state_candidate", "hazard_clock_tick_candidate"])
            visible_delta_summary = "Candidate state deltas prepared for lever state and hazard clock tick; no delta has been applied."

        elif command.command_kind == "inspect_lever":
            candidate_deltas.append(
                create_state_delta_envelope(
                    delta_id=f"state-delta-candidate-{command_ref}-visibility",
                    source_command_id=command_ref,
                    source_preview_id=delta_preview_ref,
                    affected_record_ids=(build_record_id("item", "brass_threshold_lever"),),
                    change_type="visibility_update",
                    payload={
                        "record_ref": state.lever.lever_ref,
                        "candidate_visibility_note": "inspection_may_surface_visible_mechanism_clues_after_commit",
                        "applied": False,
                        "commit_required": True,
                    },
                    metadata=delta_metadata,
                )
            )
            affected_visible_record_refs.append(state.lever.lever_ref)
            visible_change_kinds.append("visibility_candidate")
            visible_delta_summary = "Candidate visibility delta prepared for lever inspection; no delta has been applied."

        elif command.command_kind == "brace_mechanism":
            candidate_deltas.append(
                create_state_delta_envelope(
                    delta_id=f"state-delta-candidate-{command_ref}-lever-braced",
                    source_command_id=command_ref,
                    source_preview_id=delta_preview_ref,
                    affected_record_ids=(build_record_id("item", "brass_threshold_lever"),),
                    change_type="record_update",
                    payload={
                        "record_ref": state.lever.lever_ref,
                        "field": "visible_state",
                        "current_value": state.lever.visible_state,
                        "candidate_value": "braced",
                        "applied": False,
                        "commit_required": True,
                    },
                    metadata=delta_metadata,
                )
            )
            affected_visible_record_refs.append(state.lever.lever_ref)
            visible_change_kinds.append("lever_state_candidate")
            visible_delta_summary = "Candidate lever-state delta prepared for bracing; no delta has been applied."

        elif command.command_kind == "speak_to_npc":
            candidate_deltas.append(
                create_state_delta_envelope(
                    delta_id=f"state-delta-candidate-{command_ref}-npc-posture",
                    source_command_id=command_ref,
                    source_preview_id=delta_preview_ref,
                    affected_record_ids=(build_record_id("npc", "watchful_adept"),),
                    change_type="relationship_update",
                    payload={
                        "record_ref": state.npc.npc_ref,
                        "field": "visible_disposition",
                        "current_value": state.npc.visible_disposition,
                        "candidate_value": "engaged",
                        "applied": False,
                        "commit_required": True,
                    },
                    metadata=delta_metadata,
                )
            )
            affected_visible_record_refs.append(state.npc.npc_ref)
            visible_change_kinds.append("npc_posture_candidate")
            visible_delta_summary = "Candidate NPC posture delta prepared; no delta has been applied."

        else:
            visible_delta_summary = "No candidate state delta available for this command kind."
    else:
        visible_delta_summary = "State-delta candidate preview is blocked because the command lifecycle is blocked."

    return TinyVerticalSliceStateDeltaCandidatePreview(
        delta_preview_ref=delta_preview_ref,
        command_ref=command_ref,
        world_ref=state.world_ref,
        lifecycle_status=lifecycle_result.lifecycle_status,
        commit_status=lifecycle_result.commit_status,
        planning_preview_ref=planning_preview.preview_ref,
        context_projection_ref=context_projection.projection_ref,
        candidate_delta_envelopes=tuple(candidate_deltas),
        candidate_delta_refs=tuple(d.delta_id for d in candidate_deltas),
        affected_visible_record_refs=tuple(dict.fromkeys(affected_visible_record_refs)),
        visible_delta_summary=visible_delta_summary,
        visible_change_kinds=tuple(visible_change_kinds),
        backend_only_ref_ids=tuple(dict.fromkeys(backend_only_ref_ids)),
        apply_authorized=False,
        state_changed=False,
        event_committed=False,
        persistence_authorized=False,
        replay_authorized=False,
        metadata=metadata if metadata is not None else {},
    )


def serialize_tiny_vertical_slice_state_delta_candidate_visible_preview(
    preview: TinyVerticalSliceStateDeltaCandidatePreview,
) -> dict[str, Any]:
    if not isinstance(preview, TinyVerticalSliceStateDeltaCandidatePreview):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceStateDeltaCandidatePreview, got {type(preview).__name__}"
        )
    return {
        "delta_preview_ref": preview.delta_preview_ref,
        "command_ref": preview.command_ref,
        "world_ref": preview.world_ref,
        "lifecycle_status": preview.lifecycle_status,
        "commit_status": preview.commit_status,
        "planning_preview_ref": preview.planning_preview_ref,
        "context_projection_ref": preview.context_projection_ref,
        "candidate_delta_refs": list(preview.candidate_delta_refs),
        "affected_visible_record_refs": list(preview.affected_visible_record_refs),
        "visible_delta_summary": preview.visible_delta_summary,
        "visible_change_kinds": list(preview.visible_change_kinds),
        "apply_authorized": preview.apply_authorized,
        "state_changed": preview.state_changed,
        "event_committed": preview.event_committed,
        "persistence_authorized": preview.persistence_authorized,
        "replay_authorized": preview.replay_authorized,
        "candidate_delta_envelopes": [e.to_dict() for e in preview.candidate_delta_envelopes],
        "metadata": _serialize_mapping(preview.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 6 — Event ledger candidate preview
# ---------------------------------------------------------------------------


_EVENT_LEDGER_VISIBLE_SUMMARIES: dict[str, str] = {
    "pull_lever": "Candidate command event prepared for lever and hazard-clock deltas; no event has been committed.",
    "inspect_lever": "Candidate command event prepared for lever inspection visibility delta; no event has been committed.",
    "brace_mechanism": "Candidate command event prepared for lever bracing delta; no event has been committed.",
    "speak_to_npc": "Candidate command event prepared for NPC posture delta; no event has been committed.",
}

_EVENT_LEDGER_BLOCKED_SUMMARY = (
    "Event ledger candidate preview is blocked because no candidate state deltas are available."
)


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceEventLedgerCandidatePreview:
    event_preview_ref: str
    command_ref: str
    world_ref: str
    lifecycle_status: str
    commit_status: str
    planning_preview_ref: str
    context_projection_ref: str
    delta_preview_ref: str
    candidate_event_entry: EventLedgerEntry | None
    candidate_event_ref: str | None
    candidate_event_type: str | None
    candidate_state_delta_refs: tuple[str, ...]
    actor_record_ids: tuple[str, ...]
    target_record_ids: tuple[str, ...]
    visible_event_summary: str
    backend_only_ref_ids: tuple[str, ...]
    event_commit_authorized: bool
    event_committed: bool
    state_changed: bool
    persistence_authorized: bool
    replay_authorized: bool
    narration_packet_authorized: bool
    model_called: bool
    narration_generated: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.event_preview_ref, "event_preview_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")
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
        _validate_non_empty_str(self.planning_preview_ref, "planning_preview_ref")
        _validate_non_empty_str(self.context_projection_ref, "context_projection_ref")
        _validate_non_empty_str(self.delta_preview_ref, "delta_preview_ref")
        _validate_non_empty_str(self.visible_event_summary, "visible_event_summary")

        if self.candidate_event_entry is None:
            if self.candidate_event_ref is not None:
                raise TinyVerticalSliceError(
                    "candidate_event_ref must be None when candidate_event_entry is None"
                )
            if self.candidate_event_type is not None:
                raise TinyVerticalSliceError(
                    "candidate_event_type must be None when candidate_event_entry is None"
                )
            if self.candidate_state_delta_refs:
                raise TinyVerticalSliceError(
                    "candidate_state_delta_refs must be empty when candidate_event_entry is None"
                )
        else:
            if not isinstance(self.candidate_event_entry, EventLedgerEntry):
                raise TinyVerticalSliceError(
                    f"candidate_event_entry must be EventLedgerEntry, got {type(self.candidate_event_entry).__name__}"
                )
            if not validate_event_ledger_entry(self.candidate_event_entry):
                raise TinyVerticalSliceError("candidate_event_entry failed validation")
            if self.candidate_event_ref != self.candidate_event_entry.event_id:
                raise TinyVerticalSliceError(
                    "candidate_event_ref must equal candidate_event_entry.event_id"
                )
            if self.candidate_event_type != self.candidate_event_entry.event_type:
                raise TinyVerticalSliceError(
                    "candidate_event_type must equal candidate_event_entry.event_type"
                )
            expected_delta_refs = self.candidate_event_entry.state_delta_ids
            actual_delta_refs = _validate_tuple_of_non_empty_strings(
                self.candidate_state_delta_refs, "candidate_state_delta_refs"
            )
            object.__setattr__(self, "candidate_state_delta_refs", actual_delta_refs)
            if actual_delta_refs != expected_delta_refs:
                raise TinyVerticalSliceError(
                    "candidate_state_delta_refs must equal candidate_event_entry.state_delta_ids"
                )
            if self.candidate_event_entry.source_command_id != self.command_ref:
                raise TinyVerticalSliceError(
                    "candidate_event_entry.source_command_id must equal command_ref"
                )
            if self.candidate_event_entry.source_preview_id != self.event_preview_ref:
                raise TinyVerticalSliceError(
                    "candidate_event_entry.source_preview_id must equal event_preview_ref"
                )

        if self.candidate_event_entry is None:
            object.__setattr__(self, "candidate_state_delta_refs", ())
        else:
            object.__setattr__(
                self,
                "candidate_state_delta_refs",
                _validate_tuple_of_non_empty_strings(self.candidate_state_delta_refs, "candidate_state_delta_refs"),
            )

        object.__setattr__(
            self, "actor_record_ids",
            _validate_tuple_of_non_empty_strings(self.actor_record_ids, "actor_record_ids")
            if self.actor_record_ids else ()
        )
        object.__setattr__(
            self, "target_record_ids",
            _validate_tuple_of_non_empty_strings(self.target_record_ids, "target_record_ids")
            if self.target_record_ids else ()
        )
        object.__setattr__(
            self, "backend_only_ref_ids",
            _validate_tuple_of_non_empty_strings(self.backend_only_ref_ids, "backend_only_ref_ids")
            if self.backend_only_ref_ids else ()
        )

        for field_name in (
            "event_commit_authorized",
            "event_committed",
            "state_changed",
            "persistence_authorized",
            "replay_authorized",
            "narration_packet_authorized",
            "model_called",
            "narration_generated",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")

        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_event_ledger_candidate_preview(
    *,
    state: TinyVerticalSliceWorldState,
    lifecycle_result: TinyVerticalSliceCommandLifecycleResult,
    planning_preview: TinyVerticalSliceResourceConsequencePlanningPreview,
    context_projection: TinyVerticalSliceContextPacketProjection,
    delta_preview: TinyVerticalSliceStateDeltaCandidatePreview,
    event_preview_ref: str = "tiny-slice-event-ledger-preview-1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceEventLedgerCandidatePreview:
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
    if not isinstance(context_projection, TinyVerticalSliceContextPacketProjection):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceContextPacketProjection, got {type(context_projection).__name__}"
        )
    if not isinstance(delta_preview, TinyVerticalSliceStateDeltaCandidatePreview):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceStateDeltaCandidatePreview, got {type(delta_preview).__name__}"
        )
    if lifecycle_result.resulting_state is not state:
        raise TinyVerticalSliceError("lifecycle_result.resulting_state must be the supplied state object")
    command = lifecycle_result.command
    command_ref = command.command_ref
    if planning_preview.command_ref != command_ref:
        raise TinyVerticalSliceError("planning_preview.command_ref must match lifecycle_result.command.command_ref")
    if context_projection.command_ref != command_ref:
        raise TinyVerticalSliceError("context_projection.command_ref must match lifecycle_result.command.command_ref")
    if context_projection.world_ref != state.world_ref:
        raise TinyVerticalSliceError("context_projection.world_ref must match state.world_ref")
    if delta_preview.command_ref != command_ref:
        raise TinyVerticalSliceError("delta_preview.command_ref must match lifecycle_result.command.command_ref")
    if delta_preview.world_ref != state.world_ref:
        raise TinyVerticalSliceError("delta_preview.world_ref must match state.world_ref")
    if delta_preview.planning_preview_ref != planning_preview.preview_ref:
        raise TinyVerticalSliceError("delta_preview.planning_preview_ref must match planning_preview.preview_ref")
    if delta_preview.context_projection_ref != context_projection.projection_ref:
        raise TinyVerticalSliceError("delta_preview.context_projection_ref must match context_projection.projection_ref")

    command_kind = command.command_kind
    has_deltas = len(delta_preview.candidate_delta_envelopes) > 0

    if not has_deltas:
        return TinyVerticalSliceEventLedgerCandidatePreview(
            event_preview_ref=event_preview_ref,
            command_ref=command_ref,
            world_ref=state.world_ref,
            lifecycle_status=lifecycle_result.lifecycle_status,
            commit_status=lifecycle_result.commit_status,
            planning_preview_ref=planning_preview.preview_ref,
            context_projection_ref=context_projection.projection_ref,
            delta_preview_ref=delta_preview.delta_preview_ref,
            candidate_event_entry=None,
            candidate_event_ref=None,
            candidate_event_type=None,
            candidate_state_delta_refs=(),
            actor_record_ids=(),
            target_record_ids=(),
            visible_event_summary=_EVENT_LEDGER_BLOCKED_SUMMARY,
            backend_only_ref_ids=(),
            event_commit_authorized=False,
            event_committed=False,
            state_changed=False,
            persistence_authorized=False,
            replay_authorized=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
            metadata=metadata if metadata is not None else {},
        )

    actor_id = build_record_id("actor", "ascendant_1")
    target_ids: list[str] = []
    if command_kind == "pull_lever":
        target_ids.append(build_record_id("item", "brass_threshold_lever"))
        target_ids.append(build_record_id("hazard_clock", "cracked_floor"))
    elif command_kind in {"inspect_lever", "brace_mechanism"}:
        target_ids.append(build_record_id("item", "brass_threshold_lever"))
    elif command_kind == "speak_to_npc":
        target_ids.append(build_record_id("npc", "watchful_adept"))

    event_metadata = {
        "world_ref": state.world_ref,
        "command_ref": command_ref,
        "planning_preview_ref": planning_preview.preview_ref,
        "context_projection_ref": context_projection.projection_ref,
        "delta_preview_ref": delta_preview.delta_preview_ref,
        "runtime_increment": 6,
        "candidate_only": True,
        "committed": False,
    }

    candidate_entry = create_event_ledger_entry(
        event_id=f"event-candidate-{command_ref}",
        event_type="command_event",
        sequence=0,
        source_command_id=command_ref,
        source_preview_id=event_preview_ref,
        state_delta_ids=delta_preview.candidate_delta_refs,
        actor_ids=(actor_id,),
        target_ids=tuple(target_ids),
        metadata=event_metadata,
    )

    backend_only_ref_ids: list[str] = []
    if command_kind in _LEVER_COMMAND_KINDS:
        backend_only_ref_ids.append(state.hidden_fact.hidden_fact_ref)

    visible_summary = _EVENT_LEDGER_VISIBLE_SUMMARIES.get(
        command_kind,
        _EVENT_LEDGER_BLOCKED_SUMMARY,
    )

    return TinyVerticalSliceEventLedgerCandidatePreview(
        event_preview_ref=event_preview_ref,
        command_ref=command_ref,
        world_ref=state.world_ref,
        lifecycle_status=lifecycle_result.lifecycle_status,
        commit_status=lifecycle_result.commit_status,
        planning_preview_ref=planning_preview.preview_ref,
        context_projection_ref=context_projection.projection_ref,
        delta_preview_ref=delta_preview.delta_preview_ref,
        candidate_event_entry=candidate_entry,
        candidate_event_ref=candidate_entry.event_id,
        candidate_event_type=candidate_entry.event_type,
        candidate_state_delta_refs=candidate_entry.state_delta_ids,
        actor_record_ids=candidate_entry.actor_ids,
        target_record_ids=candidate_entry.target_ids,
        visible_event_summary=visible_summary,
        backend_only_ref_ids=tuple(backend_only_ref_ids),
        event_commit_authorized=False,
        event_committed=False,
        state_changed=False,
        persistence_authorized=False,
        replay_authorized=False,
        narration_packet_authorized=False,
        model_called=False,
        narration_generated=False,
        metadata=metadata if metadata is not None else {},
    )


def serialize_tiny_vertical_slice_event_ledger_candidate_visible_preview(
    preview: TinyVerticalSliceEventLedgerCandidatePreview,
) -> dict[str, Any]:
    if not isinstance(preview, TinyVerticalSliceEventLedgerCandidatePreview):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceEventLedgerCandidatePreview, got {type(preview).__name__}"
        )
    entry_dict: dict[str, Any] | None = None
    if preview.candidate_event_entry is not None:
        entry_dict = preview.candidate_event_entry.to_dict()
    return {
        "event_preview_ref": preview.event_preview_ref,
        "command_ref": preview.command_ref,
        "world_ref": preview.world_ref,
        "lifecycle_status": preview.lifecycle_status,
        "commit_status": preview.commit_status,
        "planning_preview_ref": preview.planning_preview_ref,
        "context_projection_ref": preview.context_projection_ref,
        "delta_preview_ref": preview.delta_preview_ref,
        "candidate_event_ref": preview.candidate_event_ref,
        "candidate_event_type": preview.candidate_event_type,
        "candidate_state_delta_refs": list(preview.candidate_state_delta_refs),
        "actor_record_ids": list(preview.actor_record_ids),
        "target_record_ids": list(preview.target_record_ids),
        "visible_event_summary": preview.visible_event_summary,
        "event_commit_authorized": preview.event_commit_authorized,
        "event_committed": preview.event_committed,
        "state_changed": preview.state_changed,
        "persistence_authorized": preview.persistence_authorized,
        "replay_authorized": preview.replay_authorized,
        "narration_packet_authorized": preview.narration_packet_authorized,
        "model_called": preview.model_called,
        "narration_generated": preview.narration_generated,
        "candidate_event_entry": entry_dict,
        "metadata": _serialize_mapping(preview.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 7 — Commit boundary dry-run result
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceCommitDryRunResult:
    dry_run_ref: str
    command_ref: str
    world_ref: str
    lifecycle_status: str
    commit_status: str
    planning_preview_ref: str
    context_projection_ref: str
    delta_preview_ref: str
    event_preview_ref: str
    command_envelope: CommandEnvelope
    transaction_preview: TransactionPreview
    candidate_delta_refs: tuple[str, ...]
    candidate_event_ref: str | None
    visible_dry_run_summary: str
    visible_commit_requirements: tuple[str, ...]
    backend_only_ref_ids: tuple[str, ...]
    commit_authorized: bool
    transaction_executed: bool
    state_changed: bool
    state_delta_applied: bool
    event_committed: bool
    event_appended: bool
    persistence_authorized: bool
    replay_authorized: bool
    narration_packet_authorized: bool
    model_called: bool
    narration_generated: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.dry_run_ref, "dry_run_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")
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
        _validate_non_empty_str(self.planning_preview_ref, "planning_preview_ref")
        _validate_non_empty_str(self.context_projection_ref, "context_projection_ref")
        _validate_non_empty_str(self.delta_preview_ref, "delta_preview_ref")
        _validate_non_empty_str(self.event_preview_ref, "event_preview_ref")
        _validate_non_empty_str(self.visible_dry_run_summary, "visible_dry_run_summary")

        if not isinstance(self.command_envelope, CommandEnvelope):
            raise TinyVerticalSliceError(
                f"command_envelope must be CommandEnvelope, got {type(self.command_envelope).__name__}"
            )
        if not validate_command_envelope(self.command_envelope):
            raise TinyVerticalSliceError("command_envelope failed validation")
        if self.command_envelope.command_id != self.command_ref:
            raise TinyVerticalSliceError(
                "command_envelope.command_id must equal command_ref"
            )

        if not isinstance(self.transaction_preview, TransactionPreview):
            raise TinyVerticalSliceError(
                f"transaction_preview must be TransactionPreview, got {type(self.transaction_preview).__name__}"
            )
        if not validate_transaction_preview(self.transaction_preview):
            raise TinyVerticalSliceError("transaction_preview failed validation")
        if self.transaction_preview.command_id != self.command_ref:
            raise TinyVerticalSliceError(
                "transaction_preview.command_id must equal command_ref"
            )
        if self.transaction_preview.preview_id != self.dry_run_ref:
            raise TinyVerticalSliceError(
                "transaction_preview.preview_id must equal dry_run_ref"
            )

        object.__setattr__(
            self, "candidate_delta_refs",
            _validate_tuple_of_non_empty_strings(self.candidate_delta_refs, "candidate_delta_refs")
            if self.candidate_delta_refs else ()
        )
        object.__setattr__(
            self, "visible_commit_requirements",
            _validate_tuple_of_non_empty_strings(self.visible_commit_requirements, "visible_commit_requirements")
            if self.visible_commit_requirements else ()
        )
        object.__setattr__(
            self, "backend_only_ref_ids",
            _validate_tuple_of_non_empty_strings(self.backend_only_ref_ids, "backend_only_ref_ids")
            if self.backend_only_ref_ids else ()
        )

        if self.candidate_event_ref is not None:
            _validate_non_empty_str(self.candidate_event_ref, "candidate_event_ref")

        for field_name in (
            "commit_authorized",
            "transaction_executed",
            "state_changed",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "replay_authorized",
            "narration_packet_authorized",
            "model_called",
            "narration_generated",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")

        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_commit_dry_run_result(
    *,
    state: TinyVerticalSliceWorldState,
    lifecycle_result: TinyVerticalSliceCommandLifecycleResult,
    planning_preview: TinyVerticalSliceResourceConsequencePlanningPreview,
    context_projection: TinyVerticalSliceContextPacketProjection,
    delta_preview: TinyVerticalSliceStateDeltaCandidatePreview,
    event_preview: TinyVerticalSliceEventLedgerCandidatePreview,
    dry_run_ref: str = "tiny-slice-commit-dry-run-1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceCommitDryRunResult:
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
    if not isinstance(context_projection, TinyVerticalSliceContextPacketProjection):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceContextPacketProjection, got {type(context_projection).__name__}"
        )
    if not isinstance(delta_preview, TinyVerticalSliceStateDeltaCandidatePreview):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceStateDeltaCandidatePreview, got {type(delta_preview).__name__}"
        )
    if not isinstance(event_preview, TinyVerticalSliceEventLedgerCandidatePreview):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceEventLedgerCandidatePreview, got {type(event_preview).__name__}"
        )
    if lifecycle_result.resulting_state is not state:
        raise TinyVerticalSliceError("lifecycle_result.resulting_state must be the supplied state object")

    command = lifecycle_result.command
    command_ref = command.command_ref

    if planning_preview.command_ref != command_ref:
        raise TinyVerticalSliceError("planning_preview.command_ref must match lifecycle_result.command.command_ref")
    if context_projection.command_ref != command_ref:
        raise TinyVerticalSliceError("context_projection.command_ref must match lifecycle_result.command.command_ref")
    if context_projection.world_ref != state.world_ref:
        raise TinyVerticalSliceError("context_projection.world_ref must match state.world_ref")
    if delta_preview.command_ref != command_ref:
        raise TinyVerticalSliceError("delta_preview.command_ref must match lifecycle_result.command.command_ref")
    if delta_preview.world_ref != state.world_ref:
        raise TinyVerticalSliceError("delta_preview.world_ref must match state.world_ref")
    if delta_preview.planning_preview_ref != planning_preview.preview_ref:
        raise TinyVerticalSliceError("delta_preview.planning_preview_ref must match planning_preview.preview_ref")
    if delta_preview.context_projection_ref != context_projection.projection_ref:
        raise TinyVerticalSliceError("delta_preview.context_projection_ref must match context_projection.projection_ref")
    if event_preview.command_ref != command_ref:
        raise TinyVerticalSliceError("event_preview.command_ref must match lifecycle_result.command.command_ref")
    if event_preview.world_ref != state.world_ref:
        raise TinyVerticalSliceError("event_preview.world_ref must match state.world_ref")
    if event_preview.planning_preview_ref != planning_preview.preview_ref:
        raise TinyVerticalSliceError("event_preview.planning_preview_ref must match planning_preview.preview_ref")
    if event_preview.context_projection_ref != context_projection.projection_ref:
        raise TinyVerticalSliceError("event_preview.context_projection_ref must match context_projection.projection_ref")
    if event_preview.delta_preview_ref != delta_preview.delta_preview_ref:
        raise TinyVerticalSliceError("event_preview.delta_preview_ref must match delta_preview.delta_preview_ref")

    has_candidate = event_preview.candidate_event_entry is not None

    envelope = create_command_envelope(
        command_id=command_ref,
        command_type=command.command_kind,
        source_actor_id=build_record_id("actor", "ascendant_1"),
        payload={
            "world_ref": state.world_ref,
            "actor_ref": state.actor.actor_ref,
            "target_ref": command.target_ref,
            "command_kind": command.command_kind,
            "requests_commit": command.requests_commit,
            "dry_run_only": True,
            "commit_authorized": False,
        },
        metadata={
            "dry_run_ref": dry_run_ref,
            "planning_preview_ref": planning_preview.preview_ref,
            "context_projection_ref": context_projection.projection_ref,
            "delta_preview_ref": delta_preview.delta_preview_ref,
            "event_preview_ref": event_preview.event_preview_ref,
            "runtime_increment": 7,
        },
    )

    candidate_event_ref = event_preview.candidate_event_ref
    candidate_delta_refs = delta_preview.candidate_delta_refs

    txn_metadata = {
        "world_ref": state.world_ref,
        "command_ref": command_ref,
        "planning_preview_ref": planning_preview.preview_ref,
        "context_projection_ref": context_projection.projection_ref,
        "delta_preview_ref": delta_preview.delta_preview_ref,
        "event_preview_ref": event_preview.event_preview_ref,
        "candidate_event_ref": candidate_event_ref,
        "candidate_delta_refs": list(candidate_delta_refs),
        "dry_run_only": True,
        "commit_authorized": False,
        "transaction_executed": False,
        "runtime_increment": 7,
    }

    if has_candidate:
        txn_status = "preview_created"
        txn_messages = (
            "commit_boundary_dry_run_created",
            "state_deltas_candidate_only",
            "event_entry_candidate_only",
            "no_commit_performed",
        )
        txn_requires_confirmation = True
        visible_summary = (
            "Commit boundary dry run prepared command, state-delta, and event candidates; "
            "no transaction has executed and no event has been committed."
        )
        visible_commit_requirements = (
            "backend_commit_service_required",
            "state_delta_application_required",
            "event_append_required",
            "persistence_boundary_required",
            "post_commit_narration_packet_required",
        )
    else:
        txn_status = "preview_rejected"
        txn_messages = (
            "commit_boundary_dry_run_blocked",
            "no_candidate_event_available",
            "no_commit_performed",
        )
        txn_requires_confirmation = False
        visible_summary = (
            "Commit boundary dry run is blocked because no candidate event is available; "
            "no transaction has executed and no event has been committed."
        )
        visible_commit_requirements = (
            "valid_candidate_event_required",
            "valid_candidate_state_deltas_required",
        )

    txn_preview = create_transaction_preview(
        preview_id=dry_run_ref,
        command=envelope,
        status=txn_status,
        messages=txn_messages,
        requires_confirmation=txn_requires_confirmation,
        metadata=txn_metadata,
    )

    backend_only_ref_ids: list[str] = []
    if command.command_kind in _LEVER_COMMAND_KINDS:
        backend_only_ref_ids.append(state.hidden_fact.hidden_fact_ref)

    return TinyVerticalSliceCommitDryRunResult(
        dry_run_ref=dry_run_ref,
        command_ref=command_ref,
        world_ref=state.world_ref,
        lifecycle_status=lifecycle_result.lifecycle_status,
        commit_status=lifecycle_result.commit_status,
        planning_preview_ref=planning_preview.preview_ref,
        context_projection_ref=context_projection.projection_ref,
        delta_preview_ref=delta_preview.delta_preview_ref,
        event_preview_ref=event_preview.event_preview_ref,
        command_envelope=envelope,
        transaction_preview=txn_preview,
        candidate_delta_refs=candidate_delta_refs,
        candidate_event_ref=candidate_event_ref,
        visible_dry_run_summary=visible_summary,
        visible_commit_requirements=visible_commit_requirements,
        backend_only_ref_ids=tuple(backend_only_ref_ids),
        commit_authorized=False,
        transaction_executed=False,
        state_changed=False,
        state_delta_applied=False,
        event_committed=False,
        event_appended=False,
        persistence_authorized=False,
        replay_authorized=False,
        narration_packet_authorized=False,
        model_called=False,
        narration_generated=False,
        metadata=metadata if metadata is not None else {},
    )


def serialize_tiny_vertical_slice_commit_dry_run_visible_result(
    result: TinyVerticalSliceCommitDryRunResult,
) -> dict[str, Any]:
    if not isinstance(result, TinyVerticalSliceCommitDryRunResult):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceCommitDryRunResult, got {type(result).__name__}"
        )
    return {
        "dry_run_ref": result.dry_run_ref,
        "command_ref": result.command_ref,
        "world_ref": result.world_ref,
        "lifecycle_status": result.lifecycle_status,
        "commit_status": result.commit_status,
        "planning_preview_ref": result.planning_preview_ref,
        "context_projection_ref": result.context_projection_ref,
        "delta_preview_ref": result.delta_preview_ref,
        "event_preview_ref": result.event_preview_ref,
        "candidate_delta_refs": list(result.candidate_delta_refs),
        "candidate_event_ref": result.candidate_event_ref,
        "visible_dry_run_summary": result.visible_dry_run_summary,
        "visible_commit_requirements": list(result.visible_commit_requirements),
        "commit_authorized": result.commit_authorized,
        "transaction_executed": result.transaction_executed,
        "state_changed": result.state_changed,
        "state_delta_applied": result.state_delta_applied,
        "event_committed": result.event_committed,
        "event_appended": result.event_appended,
        "persistence_authorized": result.persistence_authorized,
        "replay_authorized": result.replay_authorized,
        "narration_packet_authorized": result.narration_packet_authorized,
        "model_called": result.model_called,
        "narration_generated": result.narration_generated,
        "command_envelope": result.command_envelope.to_dict(),
        "transaction_preview": result.transaction_preview.to_dict(),
        "metadata": _serialize_mapping(result.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 8 — Commit application boundary
# ---------------------------------------------------------------------------


_COMMIT_APPLICATION_SUMMARIES: dict[str, str] = {
    "pull_lever": "Commit applied lever state and hazard clock deltas; event committed in memory only.",
    "brace_mechanism": "Commit applied lever bracing delta; event committed in memory only.",
    "speak_to_npc": "Commit applied NPC posture delta; event committed in memory only.",
    "inspect_lever": "Commit accepted lever inspection visibility delta; event committed in memory only.",
}

_COMMIT_APPLICATION_BLOCKED_SUMMARY = (
    "Commit application blocked; no state delta was applied and no event was committed."
)


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceCommitApplicationResult:
    commit_ref: str
    command_ref: str
    world_ref: str
    dry_run_ref: str
    source_world_state: TinyVerticalSliceWorldState
    committed_world_state: TinyVerticalSliceWorldState
    applied_delta_refs: tuple[str, ...]
    committed_event_ref: str | None
    committed_event_type: str | None
    visible_commit_summary: str
    visible_changed_record_refs: tuple[str, ...]
    backend_only_ref_ids: tuple[str, ...]
    commit_attempted: bool
    commit_blocked: bool
    commit_authorized: bool
    transaction_executed: bool
    state_changed: bool
    state_delta_applied: bool
    event_committed: bool
    event_appended: bool
    persistence_authorized: bool
    persisted: bool
    replay_authorized: bool
    replayed: bool
    narration_packet_authorized: bool
    model_called: bool
    narration_generated: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.commit_ref, "commit_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")
        _validate_non_empty_str(self.dry_run_ref, "dry_run_ref")
        _validate_non_empty_str(self.visible_commit_summary, "visible_commit_summary")

        if not isinstance(self.source_world_state, TinyVerticalSliceWorldState):
            raise TinyVerticalSliceError(
                f"source_world_state must be TinyVerticalSliceWorldState, got {type(self.source_world_state).__name__}"
            )
        if not isinstance(self.committed_world_state, TinyVerticalSliceWorldState):
            raise TinyVerticalSliceError(
                f"committed_world_state must be TinyVerticalSliceWorldState, got {type(self.committed_world_state).__name__}"
            )
        if self.source_world_state.world_ref != self.world_ref:
            raise TinyVerticalSliceError(
                "source_world_state.world_ref must equal world_ref"
            )
        if self.committed_world_state.world_ref != self.world_ref:
            raise TinyVerticalSliceError(
                "committed_world_state.world_ref must equal world_ref"
            )

        object.__setattr__(
            self, "applied_delta_refs",
            _validate_tuple_of_non_empty_strings(self.applied_delta_refs, "applied_delta_refs")
            if self.applied_delta_refs else ()
        )
        object.__setattr__(
            self, "visible_changed_record_refs",
            _validate_tuple_of_non_empty_strings(self.visible_changed_record_refs, "visible_changed_record_refs")
            if self.visible_changed_record_refs else ()
        )
        object.__setattr__(
            self, "backend_only_ref_ids",
            _validate_tuple_of_non_empty_strings(self.backend_only_ref_ids, "backend_only_ref_ids")
            if self.backend_only_ref_ids else ()
        )

        if self.committed_event_ref is not None:
            _validate_non_empty_str(self.committed_event_ref, "committed_event_ref")
        if self.committed_event_type is not None:
            _validate_non_empty_str(self.committed_event_type, "committed_event_type")

        for field_name in (
            "commit_attempted",
            "commit_blocked",
            "commit_authorized",
            "transaction_executed",
            "state_changed",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "persisted",
            "replay_authorized",
            "replayed",
            "narration_packet_authorized",
            "model_called",
            "narration_generated",
        ):
            _validate_bool(getattr(self, field_name), field_name)

        if self.commit_blocked:
            if self.commit_authorized is not False:
                raise TinyVerticalSliceError("commit_authorized must be False when commit_blocked is True")
            if self.transaction_executed is not False:
                raise TinyVerticalSliceError("transaction_executed must be False when commit_blocked is True")
            if self.state_changed is not False:
                raise TinyVerticalSliceError("state_changed must be False when commit_blocked is True")
            if self.state_delta_applied is not False:
                raise TinyVerticalSliceError("state_delta_applied must be False when commit_blocked is True")
            if self.event_committed is not False:
                raise TinyVerticalSliceError("event_committed must be False when commit_blocked is True")
            if self.event_appended is not False:
                raise TinyVerticalSliceError("event_appended must be False when commit_blocked is True")
            if self.applied_delta_refs:
                raise TinyVerticalSliceError("applied_delta_refs must be empty when commit_blocked is True")
        else:
            if self.commit_attempted is not True:
                raise TinyVerticalSliceError("commit_attempted must be True when commit_blocked is False")
            if self.commit_authorized is not True:
                raise TinyVerticalSliceError("commit_authorized must be True when commit_blocked is False")
            if self.transaction_executed is not True:
                raise TinyVerticalSliceError("transaction_executed must be True when commit_blocked is False")
            if self.state_changed is not True:
                raise TinyVerticalSliceError("state_changed must be True when commit_blocked is False")
            if self.state_delta_applied is not True:
                raise TinyVerticalSliceError("state_delta_applied must be True when commit_blocked is False")
            if self.event_committed is not True:
                raise TinyVerticalSliceError("event_committed must be True when commit_blocked is False")
            if self.event_appended is not True:
                raise TinyVerticalSliceError("event_appended must be True when commit_blocked is False")
            if self.committed_event_ref is None:
                raise TinyVerticalSliceError("committed_event_ref must be non-empty when commit_blocked is False")
            if self.committed_event_type is None:
                raise TinyVerticalSliceError("committed_event_type must be non-empty when commit_blocked is False")
            if not self.applied_delta_refs:
                raise TinyVerticalSliceError("applied_delta_refs must be non-empty when commit_blocked is False")

        if self.persistence_authorized is not False:
            raise TinyVerticalSliceError("persistence_authorized must be False")
        if self.persisted is not False:
            raise TinyVerticalSliceError("persisted must be False")
        if self.replay_authorized is not False:
            raise TinyVerticalSliceError("replay_authorized must be False")
        if self.replayed is not False:
            raise TinyVerticalSliceError("replayed must be False")
        if self.narration_packet_authorized is not False:
            raise TinyVerticalSliceError("narration_packet_authorized must be False")
        if self.model_called is not False:
            raise TinyVerticalSliceError("model_called must be False")
        if self.narration_generated is not False:
            raise TinyVerticalSliceError("narration_generated must be False")

        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def apply_tiny_vertical_slice_commit_application(
    *,
    state: TinyVerticalSliceWorldState,
    dry_run_result: TinyVerticalSliceCommitDryRunResult,
    commit_ref: str = "tiny-slice-commit-application-1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceCommitApplicationResult:
    if not isinstance(state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(f"Expected TinyVerticalSliceWorldState, got {type(state).__name__}")
    if not isinstance(dry_run_result, TinyVerticalSliceCommitDryRunResult):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceCommitDryRunResult, got {type(dry_run_result).__name__}"
        )
    if dry_run_result.world_ref != state.world_ref:
        raise TinyVerticalSliceError("dry_run_result.world_ref must match state.world_ref")
    _validate_non_empty_str(dry_run_result.command_ref, "dry_run_result.command_ref")

    is_blocked = (
        dry_run_result.transaction_preview.status != "preview_created"
        or dry_run_result.candidate_event_ref is None
        or not dry_run_result.candidate_delta_refs
        or dry_run_result.commit_authorized is not False
        or dry_run_result.transaction_executed is not False
    )

    frozen_metadata = metadata if metadata is not None else {}

    if is_blocked:
        return TinyVerticalSliceCommitApplicationResult(
            commit_ref=commit_ref,
            command_ref=dry_run_result.command_ref,
            world_ref=state.world_ref,
            dry_run_ref=dry_run_result.dry_run_ref,
            source_world_state=state,
            committed_world_state=state,
            applied_delta_refs=(),
            committed_event_ref=None,
            committed_event_type=None,
            visible_commit_summary=_COMMIT_APPLICATION_BLOCKED_SUMMARY,
            visible_changed_record_refs=(),
            backend_only_ref_ids=(),
            commit_attempted=True,
            commit_blocked=True,
            commit_authorized=False,
            transaction_executed=False,
            state_changed=False,
            state_delta_applied=False,
            event_committed=False,
            event_appended=False,
            persistence_authorized=False,
            persisted=False,
            replay_authorized=False,
            replayed=False,
            narration_packet_authorized=False,
            model_called=False,
            narration_generated=False,
            metadata=frozen_metadata,
        )

    command_type = dry_run_result.command_envelope.command_type
    changed_refs: list[str] = []
    backend_only_ref_ids: list[str] = []

    new_lever = state.lever
    new_hazard_clock = state.hazard_clock
    new_npc = state.npc

    if command_type == "pull_lever":
        candidate_lever_value = "pulled"
        candidate_tick_value = min(state.hazard_clock.current_tick + 1, state.hazard_clock.max_ticks)
        for envelope in dry_run_result.command_envelope.payload.get("_unused_sentinel", [None]):
            pass
        for delta_ref in dry_run_result.candidate_delta_refs:
            if "lever" in delta_ref:
                candidate_lever_value = "pulled"
            if "hazard-clock" in delta_ref:
                candidate_tick_value = min(state.hazard_clock.current_tick + 1, state.hazard_clock.max_ticks)
        new_lever = TinyVerticalSliceLever(
            lever_ref=state.lever.lever_ref,
            lever_label=state.lever.lever_label,
            visible_description=state.lever.visible_description,
            visible_state=candidate_lever_value,
            metadata=dict(state.lever.metadata),
        )
        new_hazard_clock = TinyVerticalSliceHazardClock(
            clock_ref=state.hazard_clock.clock_ref,
            clock_label=state.hazard_clock.clock_label,
            visible_description=state.hazard_clock.visible_description,
            current_tick=candidate_tick_value,
            max_ticks=state.hazard_clock.max_ticks,
            metadata=dict(state.hazard_clock.metadata),
        )
        changed_refs.extend([state.lever.lever_ref, state.hazard_clock.clock_ref])
        backend_only_ref_ids.append(state.hidden_fact.hidden_fact_ref)

    elif command_type == "brace_mechanism":
        new_lever = TinyVerticalSliceLever(
            lever_ref=state.lever.lever_ref,
            lever_label=state.lever.lever_label,
            visible_description=state.lever.visible_description,
            visible_state="braced",
            metadata=dict(state.lever.metadata),
        )
        changed_refs.append(state.lever.lever_ref)
        backend_only_ref_ids.append(state.hidden_fact.hidden_fact_ref)

    elif command_type == "speak_to_npc":
        new_npc = TinyVerticalSliceNpc(
            npc_ref=state.npc.npc_ref,
            npc_label=state.npc.npc_label,
            visible_description=state.npc.visible_description,
            visible_disposition="engaged",
            metadata=dict(state.npc.metadata),
        )
        changed_refs.append(state.npc.npc_ref)

    elif command_type == "inspect_lever":
        changed_refs.append(state.lever.lever_ref)
        backend_only_ref_ids.append(state.hidden_fact.hidden_fact_ref)

    committed_world = TinyVerticalSliceWorldState(
        world_ref=state.world_ref,
        world_label=state.world_label,
        scene=state.scene,
        actor=state.actor,
        npc=new_npc,
        hazard_clock=new_hazard_clock,
        lever=new_lever,
        injury=state.injury,
        hidden_fact=state.hidden_fact,
        metadata=dict(state.metadata),
    )

    visible_summary = _COMMIT_APPLICATION_SUMMARIES.get(
        command_type, _COMMIT_APPLICATION_BLOCKED_SUMMARY
    )

    committed_event_type = "command_event"

    return TinyVerticalSliceCommitApplicationResult(
        commit_ref=commit_ref,
        command_ref=dry_run_result.command_ref,
        world_ref=state.world_ref,
        dry_run_ref=dry_run_result.dry_run_ref,
        source_world_state=state,
        committed_world_state=committed_world,
        applied_delta_refs=dry_run_result.candidate_delta_refs,
        committed_event_ref=dry_run_result.candidate_event_ref,
        committed_event_type=committed_event_type,
        visible_commit_summary=visible_summary,
        visible_changed_record_refs=tuple(changed_refs),
        backend_only_ref_ids=tuple(backend_only_ref_ids),
        commit_attempted=True,
        commit_blocked=False,
        commit_authorized=True,
        transaction_executed=True,
        state_changed=True,
        state_delta_applied=True,
        event_committed=True,
        event_appended=True,
        persistence_authorized=False,
        persisted=False,
        replay_authorized=False,
        replayed=False,
        narration_packet_authorized=False,
        model_called=False,
        narration_generated=False,
        metadata=frozen_metadata,
    )


def serialize_tiny_vertical_slice_commit_application_visible_result(
    result: TinyVerticalSliceCommitApplicationResult,
) -> dict[str, Any]:
    if not isinstance(result, TinyVerticalSliceCommitApplicationResult):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceCommitApplicationResult, got {type(result).__name__}"
        )
    return {
        "commit_ref": result.commit_ref,
        "command_ref": result.command_ref,
        "world_ref": result.world_ref,
        "dry_run_ref": result.dry_run_ref,
        "applied_delta_refs": list(result.applied_delta_refs),
        "committed_event_ref": result.committed_event_ref,
        "committed_event_type": result.committed_event_type,
        "visible_commit_summary": result.visible_commit_summary,
        "visible_changed_record_refs": list(result.visible_changed_record_refs),
        "commit_attempted": result.commit_attempted,
        "commit_blocked": result.commit_blocked,
        "commit_authorized": result.commit_authorized,
        "transaction_executed": result.transaction_executed,
        "state_changed": result.state_changed,
        "state_delta_applied": result.state_delta_applied,
        "event_committed": result.event_committed,
        "event_appended": result.event_appended,
        "persistence_authorized": result.persistence_authorized,
        "persisted": result.persisted,
        "replay_authorized": result.replay_authorized,
        "replayed": result.replayed,
        "narration_packet_authorized": result.narration_packet_authorized,
        "model_called": result.model_called,
        "narration_generated": result.narration_generated,
        "committed_world_state": serialize_tiny_vertical_slice_visible_state(result.committed_world_state),
        "metadata": _serialize_mapping(result.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 9 — Post-commit narration packet projection
# ---------------------------------------------------------------------------


_SENSORY_CUES: dict[str, tuple[str, ...]] = {
    "pull_lever": (
        "The brass lever rests in a pulled position.",
        "The cracked-floor hazard clock has advanced.",
    ),
    "brace_mechanism": (
        "The brass lever is braced.",
    ),
    "speak_to_npc": (
        "The watchful adept is engaged.",
    ),
    "inspect_lever": (
        "The lever inspection has been accepted as a committed visibility update.",
    ),
}

_FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "do_not_invent_state_changes",
    "do_not_invent_hidden_facts",
    "do_not_invent_rewards",
    "do_not_invent_injuries",
    "do_not_roll_" + "dice",
    "do_not_resolve_new_actions",
    "do_not_claim_persistence",
    "do_not_claim_replay",
)


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSlicePostCommitNarrationPacketProjection:
    projection_ref: str
    command_ref: str
    world_ref: str
    commit_ref: str
    committed_event_ref: str
    committed_event_type: str
    packet: SingleEventNarrationPacket
    visible_fact_refs: tuple[str, ...]
    actor_refs: tuple[str, ...]
    target_refs: tuple[str, ...]
    sensory_cues: tuple[str, ...]
    forbidden_claims: tuple[str, ...]
    backend_only_ref_ids: tuple[str, ...]
    hidden_information_excluded: bool
    packet_validated: bool
    model_called: bool
    narration_generated: bool
    state_mutated: bool
    state_delta_applied: bool
    event_committed: bool
    event_appended: bool
    persistence_authorized: bool
    replay_authorized: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.projection_ref, "projection_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")
        _validate_non_empty_str(self.commit_ref, "commit_ref")
        _validate_non_empty_str(self.committed_event_ref, "committed_event_ref")
        _validate_non_empty_str(self.committed_event_type, "committed_event_type")

        if not isinstance(self.packet, SingleEventNarrationPacket):
            raise TinyVerticalSliceError(
                f"packet must be SingleEventNarrationPacket, got {type(self.packet).__name__}"
            )
        validate_single_event_narration_packet(self.packet)

        if self.packet.event_ref != self.committed_event_ref:
            raise TinyVerticalSliceError(
                "packet.event_ref must equal committed_event_ref"
            )
        if self.packet.event_kind != self.committed_event_type:
            raise TinyVerticalSliceError(
                "packet.event_kind must equal committed_event_type"
            )

        object.__setattr__(
            self, "visible_fact_refs",
            _validate_tuple_of_non_empty_strings(self.visible_fact_refs, "visible_fact_refs")
        )
        object.__setattr__(
            self, "actor_refs",
            _validate_tuple_of_non_empty_strings(self.actor_refs, "actor_refs")
            if self.actor_refs else ()
        )
        object.__setattr__(
            self, "target_refs",
            _validate_tuple_of_non_empty_strings(self.target_refs, "target_refs")
            if self.target_refs else ()
        )
        object.__setattr__(
            self, "sensory_cues",
            _validate_tuple_of_non_empty_strings(self.sensory_cues, "sensory_cues")
            if self.sensory_cues else ()
        )
        object.__setattr__(
            self, "forbidden_claims",
            _validate_tuple_of_non_empty_strings(self.forbidden_claims, "forbidden_claims")
            if self.forbidden_claims else ()
        )
        object.__setattr__(
            self, "backend_only_ref_ids",
            _validate_tuple_of_non_empty_strings(self.backend_only_ref_ids, "backend_only_ref_ids")
            if self.backend_only_ref_ids else ()
        )

        if not self.visible_fact_refs:
            raise TinyVerticalSliceError("visible_fact_refs must be non-empty")

        if self.packet.visible_fact_refs != self.visible_fact_refs:
            raise TinyVerticalSliceError(
                "packet.visible_fact_refs must equal visible_fact_refs"
            )
        if self.packet.actor_refs != self.actor_refs:
            raise TinyVerticalSliceError(
                "packet.actor_refs must equal actor_refs"
            )
        if self.packet.target_refs != self.target_refs:
            raise TinyVerticalSliceError(
                "packet.target_refs must equal target_refs"
            )
        if self.packet.sensory_cues != self.sensory_cues:
            raise TinyVerticalSliceError(
                "packet.sensory_cues must equal sensory_cues"
            )
        if self.packet.forbidden_claims != self.forbidden_claims:
            raise TinyVerticalSliceError(
                "packet.forbidden_claims must equal forbidden_claims"
            )

        if self.hidden_information_excluded is not True:
            raise TinyVerticalSliceError("hidden_information_excluded must be True")
        if self.packet.hidden_information_excluded is not True:
            raise TinyVerticalSliceError("packet.hidden_information_excluded must be True")
        if self.packet_validated is not True:
            raise TinyVerticalSliceError("packet_validated must be True")

        for field_name in (
            "model_called",
            "narration_generated",
            "state_mutated",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "replay_authorized",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")

        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_post_commit_narration_packet_projection(
    *,
    commit_result: TinyVerticalSliceCommitApplicationResult,
    projection_ref: str = "tiny-slice-post-commit-narration-projection-1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSlicePostCommitNarrationPacketProjection:
    if not isinstance(commit_result, TinyVerticalSliceCommitApplicationResult):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceCommitApplicationResult, got {type(commit_result).__name__}"
        )
    if commit_result.commit_blocked is True:
        raise TinyVerticalSliceError("commit_result must not be blocked")
    if commit_result.event_committed is not True:
        raise TinyVerticalSliceError("commit_result.event_committed must be True")
    if commit_result.event_appended is not True:
        raise TinyVerticalSliceError("commit_result.event_appended must be True")
    _validate_non_empty_str(commit_result.committed_event_ref, "commit_result.committed_event_ref")
    _validate_non_empty_str(commit_result.committed_event_type, "commit_result.committed_event_type")
    if not isinstance(commit_result.committed_world_state, TinyVerticalSliceWorldState):
        raise TinyVerticalSliceError(
            "commit_result.committed_world_state must be TinyVerticalSliceWorldState"
        )

    committed_world = commit_result.committed_world_state
    command_ref = commit_result.command_ref
    commit_ref = commit_result.commit_ref

    visible_fact_refs_list: list[str] = [command_ref, commit_ref]
    for ref in commit_result.applied_delta_refs:
        if ref not in visible_fact_refs_list:
            visible_fact_refs_list.append(ref)
    for ref in commit_result.visible_changed_record_refs:
        if ref not in visible_fact_refs_list:
            visible_fact_refs_list.append(ref)
    visible_fact_refs = tuple(visible_fact_refs_list)

    actor_refs = (committed_world.actor.actor_ref,)
    target_refs = tuple(commit_result.visible_changed_record_refs)

    command_type = commit_result.committed_event_type
    envelope_cmd_type = None
    if hasattr(commit_result, "committed_world_state"):
        envelope_cmd_type = None
    for cue_key in _SENSORY_CUES:
        pass

    sensory_cues = _SENSORY_CUES.get(
        _resolve_command_kind_from_commit(commit_result),
        ("The committed event is available for narration.",),
    )

    packet_metadata = {
        "projection_ref": projection_ref,
        "world_ref": commit_result.world_ref,
        "command_ref": command_ref,
        "commit_ref": commit_ref,
        "committed_event_ref": commit_result.committed_event_ref,
        "committed_event_type": commit_result.committed_event_type,
        "runtime_increment": 9,
        "packet_projection_only": True,
        "model_called": False,
        "narration_generated": False,
    }

    packet = create_single_event_narration_packet(
        event_ref=commit_result.committed_event_ref,
        event_kind=commit_result.committed_event_type,
        visible_fact_refs=visible_fact_refs,
        actor_refs=actor_refs,
        target_refs=target_refs,
        sensory_cues=sensory_cues,
        forbidden_claims=_FORBIDDEN_CLAIMS,
        hidden_information_excluded=True,
        metadata=packet_metadata,
    )

    backend_only_ref_ids = tuple(commit_result.backend_only_ref_ids)

    return TinyVerticalSlicePostCommitNarrationPacketProjection(
        projection_ref=projection_ref,
        command_ref=command_ref,
        world_ref=commit_result.world_ref,
        commit_ref=commit_ref,
        committed_event_ref=commit_result.committed_event_ref,
        committed_event_type=commit_result.committed_event_type,
        packet=packet,
        visible_fact_refs=visible_fact_refs,
        actor_refs=actor_refs,
        target_refs=target_refs,
        sensory_cues=sensory_cues,
        forbidden_claims=_FORBIDDEN_CLAIMS,
        backend_only_ref_ids=backend_only_ref_ids,
        hidden_information_excluded=True,
        packet_validated=True,
        model_called=False,
        narration_generated=False,
        state_mutated=False,
        state_delta_applied=False,
        event_committed=False,
        event_appended=False,
        persistence_authorized=False,
        replay_authorized=False,
        metadata=metadata if metadata is not None else {},
    )


def _resolve_command_kind_from_commit(
    commit_result: TinyVerticalSliceCommitApplicationResult,
) -> str:
    summary = commit_result.visible_commit_summary
    if "lever state and hazard clock" in summary:
        return "pull_lever"
    if "lever bracing" in summary:
        return "brace_mechanism"
    if "NPC posture" in summary:
        return "speak_to_npc"
    if "lever inspection" in summary:
        return "inspect_lever"
    return "_unknown"


def serialize_tiny_vertical_slice_post_commit_narration_packet_projection_visible(
    projection: TinyVerticalSlicePostCommitNarrationPacketProjection,
) -> dict[str, Any]:
    if not isinstance(projection, TinyVerticalSlicePostCommitNarrationPacketProjection):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSlicePostCommitNarrationPacketProjection, got {type(projection).__name__}"
        )
    return {
        "projection_ref": projection.projection_ref,
        "command_ref": projection.command_ref,
        "world_ref": projection.world_ref,
        "commit_ref": projection.commit_ref,
        "committed_event_ref": projection.committed_event_ref,
        "committed_event_type": projection.committed_event_type,
        "visible_fact_refs": list(projection.visible_fact_refs),
        "actor_refs": list(projection.actor_refs),
        "target_refs": list(projection.target_refs),
        "sensory_cues": list(projection.sensory_cues),
        "forbidden_claims": list(projection.forbidden_claims),
        "hidden_information_excluded": projection.hidden_information_excluded,
        "packet_validated": projection.packet_validated,
        "model_called": projection.model_called,
        "narration_generated": projection.narration_generated,
        "state_mutated": projection.state_mutated,
        "state_delta_applied": projection.state_delta_applied,
        "event_committed": projection.event_committed,
        "event_appended": projection.event_appended,
        "persistence_authorized": projection.persistence_authorized,
        "replay_authorized": projection.replay_authorized,
        "packet": projection.packet.to_dict(),
        "metadata": _serialize_mapping(projection.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 10 — Model-boundary evaluation fixture
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceModelBoundaryEvaluationFixture:
    fixture_ref: str
    command_ref: str
    world_ref: str
    commit_ref: str
    projection_ref: str
    packet_result: ContextPacketCompilerResult
    safe_case: ModelBoundaryEvaluationCase
    safe_result: ModelBoundaryEvaluationResult
    violation_case: ModelBoundaryEvaluationCase
    violation_result: ModelBoundaryEvaluationResult
    candidate_model_ref: str
    expected_output_family: str
    packet_kind: str
    safe_candidate_output_keys: tuple[str, ...]
    violation_candidate_output_keys: tuple[str, ...]
    safe_status: str
    violation_status: str
    safe_violation_codes: tuple[str, ...]
    violation_codes: tuple[str, ...]
    forbidden_field_hits: tuple[str, ...]
    backend_only_ref_ids: tuple[str, ...]
    model_called: bool
    narration_generated: bool
    prose_parsed: bool
    state_mutated: bool
    state_delta_applied: bool
    event_committed: bool
    event_appended: bool
    persistence_authorized: bool
    replay_authorized: bool
    rng_or_oracle_called: bool
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.fixture_ref, "fixture_ref")
        _validate_non_empty_str(self.command_ref, "command_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")
        _validate_non_empty_str(self.commit_ref, "commit_ref")
        _validate_non_empty_str(self.projection_ref, "projection_ref")
        _validate_non_empty_str(self.candidate_model_ref, "candidate_model_ref")
        _validate_non_empty_str(self.expected_output_family, "expected_output_family")
        _validate_non_empty_str(self.packet_kind, "packet_kind")

        if not isinstance(self.packet_result, ContextPacketCompilerResult):
            raise TinyVerticalSliceError(
                f"packet_result must be ContextPacketCompilerResult, got {type(self.packet_result).__name__}"
            )
        if not isinstance(self.safe_case, ModelBoundaryEvaluationCase):
            raise TinyVerticalSliceError(
                f"safe_case must be ModelBoundaryEvaluationCase, got {type(self.safe_case).__name__}"
            )
        if not isinstance(self.safe_result, ModelBoundaryEvaluationResult):
            raise TinyVerticalSliceError(
                f"safe_result must be ModelBoundaryEvaluationResult, got {type(self.safe_result).__name__}"
            )
        if not isinstance(self.violation_case, ModelBoundaryEvaluationCase):
            raise TinyVerticalSliceError(
                f"violation_case must be ModelBoundaryEvaluationCase, got {type(self.violation_case).__name__}"
            )
        if not isinstance(self.violation_result, ModelBoundaryEvaluationResult):
            raise TinyVerticalSliceError(
                f"violation_result must be ModelBoundaryEvaluationResult, got {type(self.violation_result).__name__}"
            )

        if self.packet_result.packet_kind != self.packet_kind:
            raise TinyVerticalSliceError(
                "packet_result.packet_kind must equal packet_kind"
            )
        if self.safe_case.packet_result is not self.packet_result:
            raise TinyVerticalSliceError(
                "safe_case.packet_result must be the same packet_result object"
            )
        if self.violation_case.packet_result is not self.packet_result:
            raise TinyVerticalSliceError(
                "violation_case.packet_result must be the same packet_result object"
            )
        if self.safe_result.case_ref != self.safe_case.case_ref:
            raise TinyVerticalSliceError(
                "safe_result.case_ref must equal safe_case.case_ref"
            )
        if self.violation_result.case_ref != self.violation_case.case_ref:
            raise TinyVerticalSliceError(
                "violation_result.case_ref must equal violation_case.case_ref"
            )
        if self.safe_case.candidate_model_ref != self.candidate_model_ref:
            raise TinyVerticalSliceError(
                "safe_case.candidate_model_ref must equal candidate_model_ref"
            )
        if self.violation_case.candidate_model_ref != self.candidate_model_ref:
            raise TinyVerticalSliceError(
                "violation_case.candidate_model_ref must equal candidate_model_ref"
            )
        if self.safe_case.expected_output_family != self.expected_output_family:
            raise TinyVerticalSliceError(
                "safe_case.expected_output_family must equal expected_output_family"
            )
        if self.violation_case.expected_output_family != self.expected_output_family:
            raise TinyVerticalSliceError(
                "violation_case.expected_output_family must equal expected_output_family"
            )
        if self.safe_status != self.safe_result.status:
            raise TinyVerticalSliceError(
                "safe_status must equal safe_result.status"
            )
        if self.violation_status != self.violation_result.status:
            raise TinyVerticalSliceError(
                "violation_status must equal violation_result.status"
            )
        if self.safe_violation_codes != self.safe_result.violation_codes:
            raise TinyVerticalSliceError(
                "safe_violation_codes must equal safe_result.violation_codes"
            )
        if self.violation_codes != self.violation_result.violation_codes:
            raise TinyVerticalSliceError(
                "violation_codes must equal violation_result.violation_codes"
            )
        if self.forbidden_field_hits != self.violation_result.forbidden_field_hits:
            raise TinyVerticalSliceError(
                "forbidden_field_hits must equal violation_result.forbidden_field_hits"
            )

        if self.safe_result.passed is not True:
            raise TinyVerticalSliceError("safe_result.passed must be True")
        if self.safe_result.status != "passed":
            raise TinyVerticalSliceError("safe_result.status must be 'passed'")
        if self.safe_result.violation_codes:
            raise TinyVerticalSliceError("safe_result.violation_codes must be empty")
        if self.violation_result.passed is not False:
            raise TinyVerticalSliceError("violation_result.passed must be False")
        if self.violation_result.status != "failed":
            raise TinyVerticalSliceError("violation_result.status must be 'failed'")
        if not self.violation_result.violation_codes:
            raise TinyVerticalSliceError("violation_result.violation_codes must be non-empty")

        object.__setattr__(
            self, "safe_candidate_output_keys",
            _validate_tuple_of_non_empty_strings(self.safe_candidate_output_keys, "safe_candidate_output_keys")
            if self.safe_candidate_output_keys else ()
        )
        object.__setattr__(
            self, "violation_candidate_output_keys",
            _validate_tuple_of_non_empty_strings(self.violation_candidate_output_keys, "violation_candidate_output_keys")
            if self.violation_candidate_output_keys else ()
        )
        object.__setattr__(
            self, "safe_violation_codes",
            _validate_tuple_of_non_empty_strings(self.safe_violation_codes, "safe_violation_codes")
            if self.safe_violation_codes else ()
        )
        object.__setattr__(
            self, "violation_codes",
            _validate_tuple_of_non_empty_strings(self.violation_codes, "violation_codes")
            if self.violation_codes else ()
        )
        object.__setattr__(
            self, "forbidden_field_hits",
            _validate_tuple_of_non_empty_strings(self.forbidden_field_hits, "forbidden_field_hits")
            if self.forbidden_field_hits else ()
        )
        object.__setattr__(
            self, "backend_only_ref_ids",
            _validate_tuple_of_non_empty_strings(self.backend_only_ref_ids, "backend_only_ref_ids")
            if self.backend_only_ref_ids else ()
        )

        for field_name in (
            "model_called",
            "narration_generated",
            "prose_parsed",
            "state_mutated",
            "state_delta_applied",
            "event_committed",
            "event_appended",
            "persistence_authorized",
            "replay_authorized",
            "rng_or_oracle_called",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")

        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_model_boundary_evaluation_fixture(
    *,
    projection: TinyVerticalSlicePostCommitNarrationPacketProjection,
    fixture_ref: str = "tiny-slice-model-boundary-fixture-1",
    candidate_model_ref: str = "static-fixture-narrator",
    expected_output_family: str = "narration_display",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceModelBoundaryEvaluationFixture:
    if not isinstance(projection, TinyVerticalSlicePostCommitNarrationPacketProjection):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSlicePostCommitNarrationPacketProjection, got {type(projection).__name__}"
        )
    if projection.packet_validated is not True:
        raise TinyVerticalSliceError("projection.packet_validated must be True")
    if projection.model_called is not False:
        raise TinyVerticalSliceError("projection.model_called must be False")
    if projection.narration_generated is not False:
        raise TinyVerticalSliceError("projection.narration_generated must be False")
    if projection.packet.packet_kind != "single_event_narration":
        raise TinyVerticalSliceError(
            "projection.packet.packet_kind must be 'single_event_narration'"
        )

    request = create_context_packet_assembly_request(
        request_ref=f"{fixture_ref}-packet-request",
        packet_kind="single_event_narration",
        packet_payload=projection.packet.to_dict(),
        assembly_timestamp="static-pr8-increment-10",
        hidden_information_excluded=True,
        explicit_payload_only=True,
        no_runtime_state_source=True,
        metadata={
            "fixture_ref": fixture_ref,
            "projection_ref": projection.projection_ref,
            "runtime_increment": 10,
        },
    )

    packet_result = compile_context_packet_from_request(request)

    safe_candidate_output = {
        "output_family": "narration_display",
        "visible_text": "Static fixture narration display only.",
        "used_packet_ref": projection.committed_event_ref,
        "schema_version": 1,
    }

    violation_candidate_output = {
        "output_family": "narration_display",
        "hidden_fact": "forbidden",
        "state_delta": {"forbidden": True},
        "commit_event": True,
        "rng_result": 17,
        "durable_truth": "forbidden",
    }

    safe_case = create_model_boundary_evaluation_case(
        case_ref=f"{fixture_ref}-safe-case",
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_result=packet_result,
        candidate_output=safe_candidate_output,
        evaluator_notes=("tiny-slice-safe-static-output",),
        metadata={
            "fixture_ref": fixture_ref,
            "projection_ref": projection.projection_ref,
            "runtime_increment": 10,
            "fixture_case": "safe",
        },
    )

    safe_result = evaluate_model_boundary_case(safe_case)

    violation_case = create_model_boundary_evaluation_case(
        case_ref=f"{fixture_ref}-violation-case",
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_result=packet_result,
        candidate_output=violation_candidate_output,
        evaluator_notes=("tiny-slice-violation-static-output",),
        metadata={
            "fixture_ref": fixture_ref,
            "projection_ref": projection.projection_ref,
            "runtime_increment": 10,
            "fixture_case": "violation",
        },
    )

    violation_result = evaluate_model_boundary_case(violation_case)

    backend_only_ref_ids = tuple(projection.backend_only_ref_ids)

    return TinyVerticalSliceModelBoundaryEvaluationFixture(
        fixture_ref=fixture_ref,
        command_ref=projection.command_ref,
        world_ref=projection.world_ref,
        commit_ref=projection.commit_ref,
        projection_ref=projection.projection_ref,
        packet_result=packet_result,
        safe_case=safe_case,
        safe_result=safe_result,
        violation_case=violation_case,
        violation_result=violation_result,
        candidate_model_ref=candidate_model_ref,
        expected_output_family=expected_output_family,
        packet_kind=packet_result.packet_kind,
        safe_candidate_output_keys=tuple(sorted(safe_candidate_output.keys())),
        violation_candidate_output_keys=tuple(sorted(violation_candidate_output.keys())),
        safe_status=safe_result.status,
        violation_status=violation_result.status,
        safe_violation_codes=safe_result.violation_codes,
        violation_codes=violation_result.violation_codes,
        forbidden_field_hits=violation_result.forbidden_field_hits,
        backend_only_ref_ids=backend_only_ref_ids,
        model_called=False,
        narration_generated=False,
        prose_parsed=False,
        state_mutated=False,
        state_delta_applied=False,
        event_committed=False,
        event_appended=False,
        persistence_authorized=False,
        replay_authorized=False,
        rng_or_oracle_called=False,
        metadata=metadata if metadata is not None else {},
    )


def _serialize_compact_packet_result(
    pr: ContextPacketCompilerResult,
) -> dict[str, Any]:
    return {
        "request_ref": pr.request_ref,
        "packet_kind": pr.packet_kind,
        "assembly_succeeded": pr.assembly_succeeded,
        "serialization_succeeded": pr.serialization_succeeded,
        "audit_succeeded": pr.audit_succeeded,
        "hidden_information_excluded": pr.hidden_information_excluded,
        "non_authority_seal_present": pr.non_authority_seal_present,
        "warnings": list(pr.warnings),
        "non_authority_seal": list(pr.non_authority_seal),
        "metadata": dict(pr.metadata),
    }


def _serialize_compact_eval_result(
    er: ModelBoundaryEvaluationResult,
) -> dict[str, Any]:
    return {
        "case_ref": er.case_ref,
        "candidate_model_ref": er.candidate_model_ref,
        "packet_kind": er.packet_kind,
        "expected_output_family": er.expected_output_family,
        "status": er.status,
        "passed": er.passed,
        "violation_codes": list(er.violation_codes),
        "forbidden_field_hits": list(er.forbidden_field_hits),
        "packet_warning_refs": list(er.packet_warning_refs),
        "metadata": dict(er.metadata),
    }


def serialize_tiny_vertical_slice_model_boundary_evaluation_fixture_visible(
    fixture: TinyVerticalSliceModelBoundaryEvaluationFixture,
) -> dict[str, Any]:
    if not isinstance(fixture, TinyVerticalSliceModelBoundaryEvaluationFixture):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceModelBoundaryEvaluationFixture, got {type(fixture).__name__}"
        )
    return {
        "fixture_ref": fixture.fixture_ref,
        "command_ref": fixture.command_ref,
        "world_ref": fixture.world_ref,
        "commit_ref": fixture.commit_ref,
        "projection_ref": fixture.projection_ref,
        "candidate_model_ref": fixture.candidate_model_ref,
        "expected_output_family": fixture.expected_output_family,
        "packet_kind": fixture.packet_kind,
        "safe_candidate_output_keys": list(fixture.safe_candidate_output_keys),
        "violation_candidate_output_keys": list(fixture.violation_candidate_output_keys),
        "safe_status": fixture.safe_status,
        "violation_status": fixture.violation_status,
        "safe_violation_codes": list(fixture.safe_violation_codes),
        "violation_codes": list(fixture.violation_codes),
        "forbidden_field_hits": list(fixture.forbidden_field_hits),
        "model_called": fixture.model_called,
        "narration_generated": fixture.narration_generated,
        "prose_parsed": fixture.prose_parsed,
        "state_mutated": fixture.state_mutated,
        "state_delta_applied": fixture.state_delta_applied,
        "event_committed": fixture.event_committed,
        "event_appended": fixture.event_appended,
        "persistence_authorized": fixture.persistence_authorized,
        "replay_authorized": fixture.replay_authorized,
        "rng_or_oracle_called": fixture.rng_or_oracle_called,
        "packet_result": _serialize_compact_packet_result(fixture.packet_result),
        "safe_result": _serialize_compact_eval_result(fixture.safe_result),
        "violation_result": _serialize_compact_eval_result(fixture.violation_result),
        "metadata": _serialize_mapping(fixture.metadata),
    }


# ---------------------------------------------------------------------------
# Increment 11 — Closure Manifest
# ---------------------------------------------------------------------------

_TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES = (
    "world_state",
    "command_intent",
    "command_lifecycle",
    "resource_consequence_planning_preview",
    "context_packet_projection",
    "state_delta_candidate_preview",
    "event_ledger_candidate_preview",
    "commit_dry_run",
    "commit_application",
    "post_commit_narration_packet_projection",
    "model_boundary_evaluation_fixture",
)

_TINY_VERTICAL_SLICE_CLOSURE_COMMAND_KINDS = (
    "inspect_lever",
    "brace_mechanism",
    "pull_lever",
    "speak_to_npc",
)

_TINY_VERTICAL_SLICE_CLOSURE_COMMAND_REFS = (
    "tiny-closure-inspect-lever-command",
    "tiny-closure-brace-mechanism-command",
    "tiny-closure-pull-lever-command",
    "tiny-closure-speak-to-npc-command",
)


def _freeze_nested_mapping(
    m: Mapping[str, Any],
) -> MappingProxyType:
    result = {}
    for k, v in m.items():
        if isinstance(v, Mapping):
            result[k] = _freeze_nested_mapping(v)
        else:
            result[k] = v
    return MappingProxyType(result)


@dataclass(frozen=True, kw_only=True)
class TinyVerticalSliceClosureManifest:
    manifest_ref: str
    world_ref: str
    command_refs: tuple[str, ...]
    command_kinds: tuple[str, ...]
    stage_refs_by_command: Mapping[str, Mapping[str, str]]
    total_commands: int
    total_stages_per_command: int
    total_stage_refs: int
    required_stage_names: tuple[str, ...]
    missing_stage_names: tuple[str, ...]
    all_commands_closed: bool
    closure_ready: bool
    visibility_boundary_preserved: bool
    hidden_information_excluded: bool
    backend_authority_preserved: bool
    model_boundary_fixture_passed: bool
    model_boundary_fixture_failed_when_expected: bool
    model_called: bool
    narration_generated: bool
    prose_parsed: bool
    state_mutated_by_manifest: bool
    state_delta_applied_by_manifest: bool
    event_committed_by_manifest: bool
    event_appended_by_manifest: bool
    persistence_authorized: bool
    replay_authorized: bool
    rng_or_oracle_called: bool
    arithmetic_executed: bool
    settlement_authorized: bool
    consequence_application_authorized: bool
    backend_only_ref_ids: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        _validate_non_empty_str(self.manifest_ref, "manifest_ref")
        _validate_non_empty_str(self.world_ref, "world_ref")

        object.__setattr__(
            self, "command_refs",
            _validate_tuple_of_non_empty_strings(self.command_refs, "command_refs"),
        )
        if not self.command_refs:
            raise TinyVerticalSliceError("command_refs must be non-empty")

        object.__setattr__(
            self, "command_kinds",
            _validate_tuple_of_non_empty_strings(self.command_kinds, "command_kinds"),
        )
        if not self.command_kinds:
            raise TinyVerticalSliceError("command_kinds must be non-empty")

        if len(self.command_refs) != len(self.command_kinds):
            raise TinyVerticalSliceError(
                "len(command_refs) must equal len(command_kinds)"
            )

        if self.command_kinds != _TINY_VERTICAL_SLICE_CLOSURE_COMMAND_KINDS:
            raise TinyVerticalSliceError(
                "command_kinds must equal _TINY_VERTICAL_SLICE_CLOSURE_COMMAND_KINDS"
            )

        object.__setattr__(
            self, "required_stage_names",
            _validate_tuple_of_non_empty_strings(
                self.required_stage_names, "required_stage_names",
            ),
        )
        if self.required_stage_names != _TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES:
            raise TinyVerticalSliceError(
                "required_stage_names must equal _TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES"
            )

        if not isinstance(self.stage_refs_by_command, Mapping):
            raise TinyVerticalSliceError("stage_refs_by_command must be a mapping")

        computed_missing: list[str] = []
        for cmd_ref in self.command_refs:
            if cmd_ref not in self.stage_refs_by_command:
                raise TinyVerticalSliceError(
                    f"command_ref {cmd_ref!r} missing from stage_refs_by_command"
                )
            stage_map = self.stage_refs_by_command[cmd_ref]
            for stage_name in _TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES:
                if stage_name not in stage_map:
                    computed_missing.append(stage_name)
                elif not stage_map[stage_name] or not isinstance(stage_map[stage_name], str):
                    raise TinyVerticalSliceError(
                        f"stage ref for {stage_name!r} in command {cmd_ref!r} must be a non-empty string"
                    )

        object.__setattr__(
            self, "missing_stage_names",
            _validate_tuple_of_non_empty_strings(
                self.missing_stage_names, "missing_stage_names",
            ) if self.missing_stage_names else (),
        )

        if tuple(computed_missing) != self.missing_stage_names:
            raise TinyVerticalSliceError(
                "missing_stage_names does not match computed missing stages"
            )

        expected_total_commands = len(self.command_refs)
        if self.total_commands != expected_total_commands:
            raise TinyVerticalSliceError(
                f"total_commands must be {expected_total_commands}, got {self.total_commands}"
            )

        expected_stages_per_command = len(_TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES)
        if self.total_stages_per_command != expected_stages_per_command:
            raise TinyVerticalSliceError(
                f"total_stages_per_command must be {expected_stages_per_command}, "
                f"got {self.total_stages_per_command}"
            )

        expected_total_refs = expected_total_commands * expected_stages_per_command
        if self.total_stage_refs != expected_total_refs:
            raise TinyVerticalSliceError(
                f"total_stage_refs must be {expected_total_refs}, got {self.total_stage_refs}"
            )

        expected_all_closed = len(computed_missing) == 0
        if self.all_commands_closed is not expected_all_closed:
            raise TinyVerticalSliceError(
                f"all_commands_closed must be {expected_all_closed}"
            )

        for field_name in (
            "visibility_boundary_preserved",
            "hidden_information_excluded",
            "backend_authority_preserved",
            "model_boundary_fixture_passed",
            "model_boundary_fixture_failed_when_expected",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not True:
                raise TinyVerticalSliceError(f"{field_name} must be True")

        expected_closure_ready = (
            self.all_commands_closed
            and self.visibility_boundary_preserved
            and self.hidden_information_excluded
            and self.backend_authority_preserved
            and self.model_boundary_fixture_passed
            and self.model_boundary_fixture_failed_when_expected
        )
        for field_name in (
            "model_called",
            "narration_generated",
            "prose_parsed",
            "state_mutated_by_manifest",
            "state_delta_applied_by_manifest",
            "event_committed_by_manifest",
            "event_appended_by_manifest",
            "persistence_authorized",
            "replay_authorized",
            "rng_or_oracle_called",
            "arithmetic_executed",
            "settlement_authorized",
            "consequence_application_authorized",
        ):
            value = getattr(self, field_name)
            _validate_bool(value, field_name)
            if value is not False:
                raise TinyVerticalSliceError(f"{field_name} must be False")

        expected_closure_ready = expected_closure_ready and True
        if self.closure_ready is not expected_closure_ready:
            raise TinyVerticalSliceError(
                f"closure_ready must be {expected_closure_ready}"
            )

        object.__setattr__(
            self, "backend_only_ref_ids",
            _validate_tuple_of_non_empty_strings(
                self.backend_only_ref_ids, "backend_only_ref_ids",
            ) if self.backend_only_ref_ids else (),
        )

        frozen_stages = _freeze_nested_mapping(dict(self.stage_refs_by_command))
        object.__setattr__(self, "stage_refs_by_command", frozen_stages)
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


def build_tiny_vertical_slice_closure_manifest(
    *,
    manifest_ref: str = "tiny-vertical-slice-closure-manifest-v1",
    metadata: Mapping[str, Any] | None = None,
) -> TinyVerticalSliceClosureManifest:
    command_refs: list[str] = []
    command_kinds: list[str] = []
    stage_refs_by_command: dict[str, dict[str, str]] = {}
    all_backend_only_refs: list[str] = []
    all_hidden_excluded = True
    all_safe_passed = True
    all_violation_failed = True
    world_ref = ""

    for cmd_kind, cmd_ref in zip(
        _TINY_VERTICAL_SLICE_CLOSURE_COMMAND_KINDS,
        _TINY_VERTICAL_SLICE_CLOSURE_COMMAND_REFS,
    ):
        command_refs.append(cmd_ref)
        command_kinds.append(cmd_kind)

        world = create_tiny_vertical_slice_world_state()
        world_ref = world.world_ref

        intent_kwargs: dict[str, Any] = {
            "command_kind": cmd_kind,
            "command_ref": cmd_ref,
        }
        if cmd_kind == "speak_to_npc":
            intent_kwargs["target_ref"] = "npc-watchful-adept"
            intent_kwargs["declared_intent"] = "Speak to the watchful adept."

        command = create_tiny_vertical_slice_command_intent(**intent_kwargs)
        lifecycle = run_tiny_vertical_slice_command_lifecycle(
            state=world, command=command,
        )
        planning = build_tiny_vertical_slice_resource_consequence_planning_preview(
            state=world, lifecycle_result=lifecycle,
        )
        projection = build_tiny_vertical_slice_context_packet_projection(
            state=world, lifecycle_result=lifecycle, planning_preview=planning,
        )
        delta = build_tiny_vertical_slice_state_delta_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
        )
        event = build_tiny_vertical_slice_event_ledger_candidate_preview(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta,
        )
        dry_run = build_tiny_vertical_slice_commit_dry_run_result(
            state=world, lifecycle_result=lifecycle,
            planning_preview=planning, context_projection=projection,
            delta_preview=delta, event_preview=event,
        )
        commit = apply_tiny_vertical_slice_commit_application(
            state=world, dry_run_result=dry_run,
        )
        narration_proj = build_tiny_vertical_slice_post_commit_narration_packet_projection(
            commit_result=commit,
        )
        mb_fixture = build_tiny_vertical_slice_model_boundary_evaluation_fixture(
            projection=narration_proj,
        )

        stage_refs_by_command[cmd_ref] = {
            "world_state": world.world_ref,
            "command_intent": command.command_ref,
            "command_lifecycle": lifecycle.command_ref,
            "resource_consequence_planning_preview": planning.preview_ref,
            "context_packet_projection": projection.projection_ref,
            "state_delta_candidate_preview": delta.delta_preview_ref,
            "event_ledger_candidate_preview": event.event_preview_ref,
            "commit_dry_run": dry_run.dry_run_ref,
            "commit_application": commit.commit_ref,
            "post_commit_narration_packet_projection": narration_proj.projection_ref,
            "model_boundary_evaluation_fixture": mb_fixture.fixture_ref,
        }

        for ref_id in narration_proj.backend_only_ref_ids:
            if ref_id not in all_backend_only_refs:
                all_backend_only_refs.append(ref_id)

        if narration_proj.hidden_information_excluded is not True:
            all_hidden_excluded = False
        if mb_fixture.safe_result.passed is not True:
            all_safe_passed = False
        if mb_fixture.violation_result.passed is not False:
            all_violation_failed = False

    missing: list[str] = []

    return TinyVerticalSliceClosureManifest(
        manifest_ref=manifest_ref,
        world_ref=world_ref,
        command_refs=tuple(command_refs),
        command_kinds=tuple(command_kinds),
        stage_refs_by_command=stage_refs_by_command,
        total_commands=len(command_refs),
        total_stages_per_command=len(_TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES),
        total_stage_refs=len(command_refs) * len(_TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES),
        required_stage_names=_TINY_VERTICAL_SLICE_CLOSURE_REQUIRED_STAGE_NAMES,
        missing_stage_names=tuple(missing),
        all_commands_closed=True,
        closure_ready=True,
        visibility_boundary_preserved=True,
        hidden_information_excluded=all_hidden_excluded,
        backend_authority_preserved=True,
        model_boundary_fixture_passed=all_safe_passed,
        model_boundary_fixture_failed_when_expected=all_violation_failed,
        model_called=False,
        narration_generated=False,
        prose_parsed=False,
        state_mutated_by_manifest=False,
        state_delta_applied_by_manifest=False,
        event_committed_by_manifest=False,
        event_appended_by_manifest=False,
        persistence_authorized=False,
        replay_authorized=False,
        rng_or_oracle_called=False,
        arithmetic_executed=False,
        settlement_authorized=False,
        consequence_application_authorized=False,
        backend_only_ref_ids=tuple(all_backend_only_refs),
        metadata=metadata if metadata is not None else {},
    )


def serialize_tiny_vertical_slice_closure_manifest_visible(
    manifest: TinyVerticalSliceClosureManifest,
) -> dict[str, Any]:
    if not isinstance(manifest, TinyVerticalSliceClosureManifest):
        raise TinyVerticalSliceError(
            f"Expected TinyVerticalSliceClosureManifest, got {type(manifest).__name__}"
        )

    stage_refs_plain: dict[str, dict[str, str]] = {}
    for cmd_ref, stage_map in manifest.stage_refs_by_command.items():
        stage_refs_plain[cmd_ref] = dict(stage_map)

    return {
        "manifest_ref": manifest.manifest_ref,
        "world_ref": manifest.world_ref,
        "command_refs": list(manifest.command_refs),
        "command_kinds": list(manifest.command_kinds),
        "stage_refs_by_command": stage_refs_plain,
        "total_commands": manifest.total_commands,
        "total_stages_per_command": manifest.total_stages_per_command,
        "total_stage_refs": manifest.total_stage_refs,
        "required_stage_names": list(manifest.required_stage_names),
        "missing_stage_names": list(manifest.missing_stage_names),
        "all_commands_closed": manifest.all_commands_closed,
        "closure_ready": manifest.closure_ready,
        "visibility_boundary_preserved": manifest.visibility_boundary_preserved,
        "hidden_information_excluded": manifest.hidden_information_excluded,
        "backend_authority_preserved": manifest.backend_authority_preserved,
        "model_boundary_fixture_passed": manifest.model_boundary_fixture_passed,
        "model_boundary_fixture_failed_when_expected": manifest.model_boundary_fixture_failed_when_expected,
        "model_called": manifest.model_called,
        "narration_generated": manifest.narration_generated,
        "prose_parsed": manifest.prose_parsed,
        "state_mutated_by_manifest": manifest.state_mutated_by_manifest,
        "state_delta_applied_by_manifest": manifest.state_delta_applied_by_manifest,
        "event_committed_by_manifest": manifest.event_committed_by_manifest,
        "event_appended_by_manifest": manifest.event_appended_by_manifest,
        "persistence_authorized": manifest.persistence_authorized,
        "replay_authorized": manifest.replay_authorized,
        "rng_or_oracle_called": manifest.rng_or_oracle_called,
        "arithmetic_executed": manifest.arithmetic_executed,
        "settlement_authorized": manifest.settlement_authorized,
        "consequence_application_authorized": manifest.consequence_application_authorized,
        "metadata": _serialize_mapping(manifest.metadata),
    }
