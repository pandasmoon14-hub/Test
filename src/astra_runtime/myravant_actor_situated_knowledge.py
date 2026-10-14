"""C-1 bounded actor-owned memory, not world truth or a universal belief engine.

One Groundskeeper can retain separately attributed first-hand sightings and
player testimony about a declared physical object's place. This module owns
only those actor-scoped observations; world placement, time, sight opportunity,
NPC consent, and transport remain under their existing owners. Textual
interpretation is separate from commitment. Event replay is deterministic.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace

from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID, GROUNDSKEEPER_ID, LANTERN_ID, ORCHARD_PATH_ID,
    PLAYER_ID, TOOL_CHEST_ID, WAYSTONE_ID, WORKSHOP_ID, YARD_ID,
)

PROFILE = "myravant-c1-actor-situated-memory"
TARGET_IDS = frozenset({LANTERN_ID, TOOL_CHEST_ID, WAYSTONE_ID})
PLACE_IDS = frozenset({WORKSHOP_ID, YARD_ID, ORCHARD_PATH_ID, GATEHOUSE_ID})
FIELDS = frozenset({
    "command_id", "actor_id", "source_actor_id", "source_kind",
    "target_id", "reported_place_id", "logical_step",
    "source_world_digest", "prior_memory_digest", "receipt_id",
})


class ActorKnowledgeError(ValueError):
    pass


def _digest(material: object) -> str:
    return hashlib.sha256(json.dumps(
        material, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    ).encode("utf-8")).hexdigest()


@dataclass(frozen=True, kw_only=True)
class ActorKnowledgeEvent:
    command_id: str
    actor_id: str
    source_actor_id: str
    source_kind: str
    target_id: str
    reported_place_id: str
    logical_step: int
    source_world_digest: str
    prior_memory_digest: str
    receipt_id: str


@dataclass(frozen=True, kw_only=True)
class ActorKnowledgeState:
    events: tuple[ActorKnowledgeEvent, ...] = ()

    def __post_init__(self) -> None:
        if any(type(x) is not ActorKnowledgeEvent for x in self.events):
            raise ActorKnowledgeError("memory contains a non-event")
        commands = [x.command_id for x in self.events]
        if len(commands) != len(set(commands)):
            raise ActorKnowledgeError("duplicate knowledge command identity")


def digest_actor_knowledge(state: ActorKnowledgeState) -> str:
    return _digest({
        "family": PROFILE,
        "events": [asdict(x) for x in state.events],
    })


def commit_actor_knowledge(
    *, state: ActorKnowledgeState, command_id: str, actor_id: str,
    source_actor_id: str, source_kind: str, target_id: str,
    reported_place_id: str, logical_step: int, source_world_digest: str,
    expected_pre_digest: str,
) -> tuple[ActorKnowledgeState, ActorKnowledgeEvent]:
    """Only a qualified caller may supply witnessed or reported evidence.

    This executor validates format and replay identity. Spatial/sensory
    qualification is performed at the application/fixture opportunity gate.
    """
    if type(state) is not ActorKnowledgeState:
        raise ActorKnowledgeError("invalid actor knowledge state")
    prior = digest_actor_knowledge(state)
    if prior != expected_pre_digest:
        raise ActorKnowledgeError("knowledge optimistic precondition mismatch")
    if (
        type(command_id) is not str
        or command_id != (
            f"terminal-actor-evidence-{len(state.events) + 1:06d}"
        )
        or (state.events and logical_step < state.events[-1].logical_step)
        or actor_id != GROUNDSKEEPER_ID
        or target_id not in TARGET_IDS
        or reported_place_id not in PLACE_IDS
        or type(logical_step) is not int or logical_step < 0
        or type(source_world_digest) is not str
        or len(source_world_digest) != 64
        or any(c not in "0123456789abcdef" for c in source_world_digest)
        or source_kind not in {"witnessed", "reported"}
        or source_actor_id != (
            GROUNDSKEEPER_ID if source_kind == "witnessed" else PLAYER_ID
        )
    ):
        raise ActorKnowledgeError("unqualified actor knowledge event")
    material = {
        "command_id": command_id,
        "actor_id": actor_id,
        "source_actor_id": source_actor_id,
        "source_kind": source_kind,
        "target_id": target_id,
        "reported_place_id": reported_place_id,
        "logical_step": logical_step,
        "source_world_digest": source_world_digest,
        "prior_memory_digest": prior,
    }
    event = ActorKnowledgeEvent(
        **material,
        receipt_id=build_record_id(
            "receipt", "c1-actor-evidence-" + _digest(material),
        ),
    )
    return replace(state, events=(*state.events, event)), event


def last_actor_evidence(
    state: ActorKnowledgeState, actor_id: str, target_id: str,
    *, source_kind: str | None = None,
) -> ActorKnowledgeEvent | None:
    for item in reversed(state.events):
        if (
            item.actor_id == actor_id and item.target_id == target_id
            and (source_kind is None or item.source_kind == source_kind)
        ):
            return item
    return None


def serialize_actor_knowledge(state: ActorKnowledgeState) -> dict[str, object]:
    return {"profile": PROFILE, "events": [asdict(x) for x in state.events]}


def restore_actor_knowledge(material: object, *, maximum_step: int,
                            existing_command_ids: set[str]) -> ActorKnowledgeState:
    if (
        type(material) is not dict or set(material) != {"profile", "events"}
        or material["profile"] != PROFILE or type(material["events"]) is not list
    ):
        raise ActorKnowledgeError("invalid actor-scoped memory component")
    state = ActorKnowledgeState()
    for raw in material["events"]:
        if type(raw) is not dict or set(raw) != FIELDS:
            raise ActorKnowledgeError("invalid actor-scoped memory event")
        try:
            saved = ActorKnowledgeEvent(**raw)
            state, replayed = commit_actor_knowledge(
                state=state, command_id=saved.command_id,
                actor_id=saved.actor_id, source_actor_id=saved.source_actor_id,
                source_kind=saved.source_kind, target_id=saved.target_id,
                reported_place_id=saved.reported_place_id,
                logical_step=saved.logical_step,
                source_world_digest=saved.source_world_digest,
                expected_pre_digest=digest_actor_knowledge(state),
            )
        except (ValueError, TypeError) as exc:
            raise ActorKnowledgeError("actor knowledge replay failed") from exc
        if (
            saved != replayed
            or saved.logical_step > maximum_step
            or saved.command_id in existing_command_ids
        ):
            raise ActorKnowledgeError("actor knowledge evidence diverged")
        existing_command_ids.add(saved.command_id)
    return state
