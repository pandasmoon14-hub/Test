"""Tiny vertical slice — static typed state fixture and visibility boundary."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


_VALID_SEVERITIES = frozenset({"minor", "moderate", "severe"})


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
