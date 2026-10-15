"""PLAY-E1 noncanonical Groundskeeper latch duty: one actor commitment.

A voluntary local request is durable but does not grant universal NPC obedience.
The existing RT-010 latch owner performs fulfillment; WORLD-2 alone advances
time. This fixture profile owns only the accepted, cancelled or fulfilled
commitment record, not the chest condition or its physical consequences.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace

from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.state_delta import create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, PLAYER_ID, TOOL_CHEST_ID, YARD_ID,
)

PROFILE = "myravant-e1-groundskeeper-latch-duty-v1"
STATUS = frozenset({"none", "pending", "cancelled", "fulfilled"})
OPERATIONS = frozenset({"request", "cancel", "fulfill"})


class FixtureDutyError(ValueError):
    """Invalid or unverifiable E1 fixture obligation."""


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FixtureDutyEvent:
    command_id: str
    operation: str
    actor_id: str
    target_id: str
    place_id: str
    logical_step: int
    time_receipt_id: str
    service_receipt_id: str
    pre_status: str
    post_status: str
    pre_digest: str
    post_digest: str
    fingerprint: str
    preview_id: str
    receipt_id: str
    state_delta_id: str


@dataclass(frozen=True)
class FixtureDutyState:
    status: str = "none"
    events: tuple[FixtureDutyEvent, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in STATUS:
            raise FixtureDutyError("invalid duty status")
        if any(type(e) is not FixtureDutyEvent for e in self.events):
            raise FixtureDutyError("invalid duty history")
        if len({e.command_id for e in self.events}) != len(self.events):
            raise FixtureDutyError("duplicate duty command identity")


def digest_fixture_duty(state: FixtureDutyState) -> str:
    return _digest({"profile": PROFILE, "status": state.status})


def _next_status(status: str, operation: str) -> str:
    if operation == "request" and status in {"none", "cancelled"}:
        return "pending"
    if operation == "cancel" and status == "pending":
        return "cancelled"
    if operation == "fulfill" and status == "pending":
        return "fulfilled"
    raise FixtureDutyError("duty transition is unavailable")


def execute_fixture_duty(
    *, state: FixtureDutyState, command_id: str, operation: str,
    logical_step: int, time_receipt_id: str = "",
    service_receipt_id: str = "", expected_pre_digest: str,
    qualified: bool,
):
    """Commit only a qualified, profile-specific commitment transition."""
    if not qualified or not command_id or operation not in OPERATIONS:
        raise FixtureDutyError("unqualified duty instruction")
    if type(logical_step) is not int or logical_step < 0:
        raise FixtureDutyError("invalid duty logical step")
    if state.events and logical_step < state.events[-1].logical_step:
        raise FixtureDutyError("duty clock regressed")
    if operation == "fulfill":
        if not time_receipt_id or not service_receipt_id:
            raise FixtureDutyError("fulfilled duty lacks causal evidence")
    elif time_receipt_id or service_receipt_id:
        raise FixtureDutyError("unfulfilled duty cites a nonexistent consequence")
    actor_id = (
        GROUNDSKEEPER_ID if operation == "fulfill" else PLAYER_ID
    )
    fingerprint = _digest({
        "profile": PROFILE, "command_id": command_id, "operation": operation,
        "actor_id": actor_id, "target_id": TOOL_CHEST_ID, "place_id": YARD_ID,
        "logical_step": logical_step, "time_receipt_id": time_receipt_id,
        "service_receipt_id": service_receipt_id,
    })
    for prior in state.events:
        if prior.command_id == command_id:
            if prior.fingerprint != fingerprint:
                raise FixtureDutyError("conflicting duty command retry")
            return state, prior, None, None
    if digest_fixture_duty(state) != expected_pre_digest:
        raise FixtureDutyError("stale duty state")
    new_status = _next_status(state.status, operation)
    post = FixtureDutyState(status=new_status, events=state.events)
    token = fingerprint[:24]
    command = create_command_envelope(
        command_id=command_id, command_type="interact",
        source_actor_id=actor_id,
        payload={"operation": operation, "object_id": TOOL_CHEST_ID},
        metadata={"package": "PLAY-E1", "profile": PROFILE},
    )
    preview = create_transaction_preview(
        preview_id=build_record_id("work_preview", token),
        command=command, status="preview_created",
        messages=("bounded local duty decision prepared",),
        requires_confirmation=False,
        metadata={
            "package": "PLAY-E1", "semantic_owner": "AFQR-12/RT-010",
            "mutation_performed": False,
        },
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("work_delta", token),
        source_command_id=command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(GROUNDSKEEPER_ID, TOOL_CHEST_ID),
        change_type="record_update",
        payload={
            "profile": PROFILE, "operation": operation,
            "pre_status": state.status, "post_status": new_status,
            "logical_step": logical_step,
            "time_receipt_id": time_receipt_id,
            "service_receipt_id": service_receipt_id,
        },
        metadata={
            "commitment_profile": PROFILE, "asset_owner": "RT-010",
            "time_owner": "AFQR-04",
        },
    )
    event = FixtureDutyEvent(
        command_id=command_id, operation=operation, actor_id=actor_id,
        target_id=TOOL_CHEST_ID, place_id=YARD_ID,
        logical_step=logical_step, time_receipt_id=time_receipt_id,
        service_receipt_id=service_receipt_id,
        pre_status=state.status, post_status=new_status,
        pre_digest=expected_pre_digest,
        post_digest=digest_fixture_duty(post), fingerprint=fingerprint,
        preview_id=preview.preview_id,
        receipt_id=build_record_id("work_receipt", token),
        state_delta_id=delta.delta_id,
    )
    return replace(post, events=(*state.events, event)), event, preview, delta


def serialize_fixture_duty(state: FixtureDutyState) -> dict[str, object]:
    return {
        "profile": PROFILE, "status": state.status,
        "events": [asdict(e) for e in state.events],
    }


def restore_fixture_duty(material: object) -> FixtureDutyState:
    if (
        type(material) is not dict
        or set(material) != {"profile", "status", "events"}
        or material["profile"] != PROFILE
        or type(material["events"]) is not list
    ):
        raise FixtureDutyError("invalid duty checkpoint")
    state = FixtureDutyState()
    keys = set(FixtureDutyEvent.__dataclass_fields__)
    for item in material["events"]:
        if type(item) is not dict or set(item) != keys:
            raise FixtureDutyError("malformed duty event")
        try:
            saved = FixtureDutyEvent(**item)
            state, computed, _, _ = execute_fixture_duty(
                state=state, command_id=saved.command_id,
                operation=saved.operation, logical_step=saved.logical_step,
                time_receipt_id=saved.time_receipt_id,
                service_receipt_id=saved.service_receipt_id,
                expected_pre_digest=digest_fixture_duty(state),
                qualified=True,
            )
        except (TypeError, ValueError) as exc:
            raise FixtureDutyError("duty transition cannot replay") from exc
        if saved != computed:
            raise FixtureDutyError("duty transition provenance diverged")
    if not state.events or material["status"] != state.status:
        raise FixtureDutyError("duty state diverged from replay")
    return state
