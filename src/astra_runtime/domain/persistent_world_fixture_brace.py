"""D-1 fixture-qualified RT-010 component alteration with conserved identity.

One explicitly noncanonical Tool Chest brace may be attached, loosened, or
detached onto the Yard worksite. No part creation, universal disassembly law,
materials economy, physics solver, or second semantic owner is implied.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace

from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview
from astra_runtime.kernel.state_delta import create_state_delta_envelope
from astra_runtime.myravant_play_fixture import PLAYER_ID, TOOL_CHEST_ID, YARD_ID

PROFILE = "myravant-d1-tool-chest-brace-v1"
BRACE_ID = "astra:component:tool-chest-brace"
STATES = frozenset({"attached", "loosened", "detached_at_yard"})
METHODS = frozenset({"manual", "lantern", "refit"})


class FixtureBraceError(ValueError):
    """Rejects unlicensed, stale, or non-replayable structural changes."""


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FixtureBraceEvent:
    command_id: str
    actor_id: str
    object_id: str
    component_id: str
    place_id: str
    method: str
    before_condition: str
    after_condition: str
    logical_before: int
    logical_after: int
    time_receipt_id: str
    source_world_digest: str
    pre_digest: str
    post_digest: str
    fingerprint: str
    preview_id: str
    receipt_id: str
    state_delta_id: str


@dataclass(frozen=True)
class FixtureBraceState:
    condition: str = "attached"
    events: tuple[FixtureBraceEvent, ...] = ()

    def __post_init__(self) -> None:
        if self.condition not in STATES or type(self.condition) is not str:
            raise FixtureBraceError("unrecognized chest-brace condition")
        if any(type(e) is not FixtureBraceEvent for e in self.events):
            raise FixtureBraceError("invalid chest-brace event")
        if len({e.command_id for e in self.events}) != len(self.events):
            raise FixtureBraceError("duplicate chest-brace command")


def digest_fixture_brace(state: FixtureBraceState) -> str:
    return _digest({
        "profile": PROFILE,
        "component_id": BRACE_ID,
        "condition": state.condition,
        "quantity": 1,
    })


def next_brace_condition(condition: str, method: str) -> str:
    """Method and part preconditions are fixture declarations, not world law."""
    if method == "manual" and condition == "attached":
        return "loosened"
    if method == "manual" and condition == "loosened":
        return "detached_at_yard"
    if method == "lantern" and condition == "attached":
        return "detached_at_yard"
    if method == "refit" and condition in {"loosened", "detached_at_yard"}:
        return "attached"
    raise FixtureBraceError("brace method is not qualified for this condition")


def execute_fixture_brace(
    *, state: FixtureBraceState, command_id: str, method: str,
    actor_id: str, object_id: str, component_id: str, place_id: str,
    logical_before: int, logical_after: int, time_receipt_id: str,
    source_world_digest: str, expected_pre_digest: str, qualified: bool,
) -> tuple[FixtureBraceState, FixtureBraceEvent, object, object]:
    if type(state) is not FixtureBraceState or not qualified:
        raise FixtureBraceError("unqualified chest-brace state or opportunity")
    if (
        type(command_id) is not str
        or command_id != f"terminal-fixture-brace-{len(state.events) + 1:06d}"
        or actor_id != PLAYER_ID or object_id != TOOL_CHEST_ID
        or component_id != BRACE_ID or place_id != YARD_ID
        or method not in METHODS
        or type(logical_before) is not int or logical_before < 0
        or type(logical_after) is not int
        or logical_after != logical_before + 1
        or type(time_receipt_id) is not str or not time_receipt_id
        or type(source_world_digest) is not str
        or len(source_world_digest) != 64
        or any(c not in "0123456789abcdef" for c in source_world_digest)
        or digest_fixture_brace(state) != expected_pre_digest
    ):
        raise FixtureBraceError("invalid or stale brace transition")
    target = next_brace_condition(state.condition, method)
    post = replace(state, condition=target)
    material = {
        "command_id": command_id,
        "actor_id": actor_id, "object_id": object_id,
        "component_id": component_id, "place_id": place_id,
        "method": method, "before_condition": state.condition,
        "after_condition": target,
        "logical_before": logical_before, "logical_after": logical_after,
        "time_receipt_id": time_receipt_id,
        "source_world_digest": source_world_digest,
        "pre_digest": expected_pre_digest,
        "post_digest": digest_fixture_brace(post),
    }
    fingerprint = _digest(material)
    token = fingerprint[:28]
    command = create_command_envelope(
        command_id=command_id, command_type="interact",
        source_actor_id=actor_id,
        payload={
            "target_id": object_id, "component_id": component_id,
            "method": method, "post_condition": target,
        },
        metadata={"package": "PLAY-MATERIAL-D1", "profile": PROFILE},
    )
    preview = create_transaction_preview(
        preview_id=build_record_id("material_preview", "d1-brace-" + token),
        command=command, status="preview_created",
        messages=("fixture-qualified physical component change prepared",),
        requires_confirmation=False,
        metadata={
            "package": "PLAY-MATERIAL-D1",
            "semantic_owner": "RT-010",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("material_delta", "d1-brace-" + token),
        source_command_id=command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(object_id,),
        change_type="record_update",
        payload={
            "profile": PROFILE, "component_id": component_id, "quantity": 1,
            "method": method, "before_condition": state.condition,
            "after_condition": target, "worksite": place_id,
            "logical_before": logical_before,
            "logical_after": logical_after, "time_receipt_id": time_receipt_id,
        },
        metadata={
            "asset_owner": "RT-010",
            "opportunity_owner": "AFQR-19",
            "transition_owner": "AFQR-01",
        },
    )
    event = FixtureBraceEvent(
        **material, fingerprint=fingerprint, preview_id=preview.preview_id,
        receipt_id=build_record_id("material_receipt", "d1-brace-" + token),
        state_delta_id=delta.delta_id,
    )
    return replace(post, events=(*state.events, event)), event, preview, delta


def serialize_fixture_brace(state: FixtureBraceState) -> dict[str, object]:
    return {
        "profile": PROFILE, "component_id": BRACE_ID,
        "quantity": 1, "condition": state.condition,
        "events": [asdict(e) for e in state.events],
    }


def restore_fixture_brace(material: object) -> FixtureBraceState:
    if (
        type(material) is not dict or set(material) != {
            "profile", "component_id", "quantity", "condition", "events",
        }
        or material["profile"] != PROFILE
        or material["component_id"] != BRACE_ID
        or type(material["quantity"]) is not int
        or material["quantity"] != 1
        or type(material["events"]) is not list
    ):
        raise FixtureBraceError("invalid conserved brace component")
    state = FixtureBraceState()
    fields = set(FixtureBraceEvent.__dataclass_fields__)
    for raw in material["events"]:
        if type(raw) is not dict or set(raw) != fields:
            raise FixtureBraceError("invalid chest-brace event payload")
        try:
            saved = FixtureBraceEvent(**raw)
            state, recomputed, _, _ = execute_fixture_brace(
                state=state, command_id=saved.command_id, method=saved.method,
                actor_id=saved.actor_id, object_id=saved.object_id,
                component_id=saved.component_id, place_id=saved.place_id,
                logical_before=saved.logical_before,
                logical_after=saved.logical_after,
                time_receipt_id=saved.time_receipt_id,
                source_world_digest=saved.source_world_digest,
                expected_pre_digest=digest_fixture_brace(state),
                qualified=True,
            )
        except (ValueError, TypeError) as exc:
            raise FixtureBraceError("chest-brace transition cannot replay") from exc
        if saved != recomputed:
            raise FixtureBraceError("chest-brace replay evidence diverged")
    if state.condition != material["condition"]:
        raise FixtureBraceError("saved brace condition disagrees with replay")
    return state
