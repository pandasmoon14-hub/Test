"""B-2a: one noncanonical RT-010/AFQR-16 fixture-latch service state.

This is not a generic crafting/process engine. The chest's service condition,
abandoned effort and secured latch are persistent asset facts. AFQR-04 owns
elapsed logical time, AFQR-19 qualifies opportunity and AFQR-01/02 provide
attributable immutable commit identity. No resource is created or consumed.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace

from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.state_delta import create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview

SERVICE_OWNER = "RT-010/AFQR-16"
SERVICE_PROFILE = "myravant-b2a-tool-chest-latch-v1"
OPERATIONS = frozenset({"work", "abandon", "secure", "release"})
METHODS = frozenset({"manual", "lantern", "none"})


class FixtureServiceError(ValueError):
    """Unqualified, stale or inconsistent fixture service action."""


def _digest(material: object) -> str:
    return hashlib.sha256(json.dumps(
        material, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FixtureServiceEvent:
    command_id: str
    operation: str
    method: str
    actor_id: str
    target_id: str
    place_id: str
    logical_before: int
    logical_after: int
    time_receipt_id: str
    pre_progress: int
    post_progress: int
    pre_abandoned: bool
    post_abandoned: bool
    pre_secured: bool
    post_secured: bool
    pre_digest: str
    post_digest: str
    fingerprint: str
    preview_id: str
    receipt_id: str
    state_delta_id: str


@dataclass(frozen=True)
class FixtureServiceState:
    progress: int = 0
    abandoned: bool = False
    secured: bool = False
    events: tuple[FixtureServiceEvent, ...] = ()

    def __post_init__(self) -> None:
        if type(self.progress) is not int or not 0 <= self.progress <= 2:
            raise FixtureServiceError("service progress must be 0..2")
        if type(self.abandoned) is not bool or type(self.secured) is not bool:
            raise FixtureServiceError("service status flags must be boolean")
        if self.secured and (self.progress != 2 or self.abandoned):
            raise FixtureServiceError("unserviceable latch cannot be secured")
        if self.abandoned and self.progress in (0, 2):
            raise FixtureServiceError("only incomplete invested work can be abandoned")
        if any(not isinstance(x, FixtureServiceEvent) for x in self.events):
            raise FixtureServiceError("invalid service transition history")
        if len({x.command_id for x in self.events}) != len(self.events):
            raise FixtureServiceError("duplicate service command identity")


def digest_fixture_service_state(state: FixtureServiceState) -> str:
    return _digest({
        "family": SERVICE_PROFILE,
        "progress": state.progress,
        "abandoned": state.abandoned,
        "secured": state.secured,
    })


def _transition(
    state: FixtureServiceState, operation: str, method: str
) -> tuple[int, bool, bool]:
    if operation == "work":
        if state.progress == 2:
            raise FixtureServiceError("fixture service is already complete")
        if method not in {"manual", "lantern"}:
            raise FixtureServiceError("service work method is unqualified")
        return min(2, state.progress + (2 if method == "lantern" else 1)), False, False
    if method != "none":
        raise FixtureServiceError("this operation does not admit a work method")
    if operation == "abandon":
        if state.progress not in (1,) or state.abandoned:
            raise FixtureServiceError("no active unfinished work can be abandoned")
        return state.progress, True, False
    if operation == "secure":
        if state.progress != 2 or state.secured:
            raise FixtureServiceError("the latch is not serviceable or already secured")
        return state.progress, False, True
    if operation == "release":
        if not state.secured:
            raise FixtureServiceError("the latch is not secured")
        return state.progress, False, False
    raise FixtureServiceError("unsupported fixture service operation")


def execute_fixture_service(
    *, state: FixtureServiceState, command_id: str, operation: str,
    method: str, actor_id: str, target_id: str, place_id: str,
    logical_before: int, logical_after: int, time_receipt_id: str,
    qualified: bool, expected_pre_digest: str,
):
    """Commit one qualified service change; return state, event, preview, delta.

    A work contribution requires a separately committed AFQR-04 time receipt
    covering exactly one logical step. Status/custody commands cost no time.
    The caller validates actor, location, availability and optional lit lantern.
    """
    if not qualified:
        raise FixtureServiceError("service opportunity was not qualified")
    if not command_id or not actor_id or not target_id or not place_id:
        raise FixtureServiceError("service command context is incomplete")
    if type(logical_before) is not int or logical_before < 0:
        raise FixtureServiceError("invalid logical position")
    cost = 1 if operation == "work" else 0
    if logical_after != logical_before + cost:
        raise FixtureServiceError("labor time does not match AFQR-04")
    if (cost == 1) != bool(time_receipt_id):
        raise FixtureServiceError("time receipt mismatch")
    immutable = {
        "profile": SERVICE_PROFILE, "command_id": command_id,
        "operation": operation, "method": method,
        "actor_id": actor_id, "target_id": target_id,
        "place_id": place_id, "logical_before": logical_before,
        "logical_after": logical_after, "time_receipt_id": time_receipt_id,
    }
    fingerprint = _digest(immutable)
    for existing in state.events:
        if existing.command_id == command_id:
            if existing.fingerprint != fingerprint:
                raise FixtureServiceError("conflicting service command retry")
            return state, existing, None, None
    if digest_fixture_service_state(state) != expected_pre_digest:
        raise FixtureServiceError("stale fixture service state")
    progress, abandoned, secured = _transition(state, operation, method)
    post = FixtureServiceState(
        progress=progress, abandoned=abandoned, secured=secured,
        events=state.events,
    )
    token = fingerprint[:24]
    command = create_command_envelope(
        command_id=command_id, command_type="interact",
        source_actor_id=actor_id,
        payload={"target_id": target_id, "operation": operation, "method": method},
        metadata={"package": "PLAY-UNDERTAKINGS-B2A", "profile": SERVICE_PROFILE},
    )
    preview = create_transaction_preview(
        preview_id=build_record_id("work_preview", token),
        command=command, status="preview_created",
        messages=("bounded asset servicing prepared",),
        requires_confirmation=False,
        metadata={"package": "PLAY-UNDERTAKINGS-B2A",
                  "semantic_owner": SERVICE_OWNER, "mutation_performed": False},
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("work_delta", token),
        source_command_id=command_id,
        source_preview_id=preview.preview_id,
        affected_record_ids=(target_id,),
        change_type="record_update",
        payload={
            "profile": SERVICE_PROFILE,
            "operation": operation, "method": method,
            "pre_progress": state.progress, "post_progress": progress,
            "pre_abandoned": state.abandoned, "post_abandoned": abandoned,
            "pre_secured": state.secured, "post_secured": secured,
            "logical_before": logical_before, "logical_after": logical_after,
            "time_receipt_id": time_receipt_id,
        },
        metadata={"asset_owner": SERVICE_OWNER,
                  "opportunity_owner": "AFQR-19",
                  "transition_owner": "AFQR-01"},
    )
    event = FixtureServiceEvent(
        command_id=command_id, operation=operation, method=method,
        actor_id=actor_id, target_id=target_id, place_id=place_id,
        logical_before=logical_before, logical_after=logical_after,
        time_receipt_id=time_receipt_id, pre_progress=state.progress,
        post_progress=progress, pre_abandoned=state.abandoned,
        post_abandoned=abandoned, pre_secured=state.secured,
        post_secured=secured, pre_digest=expected_pre_digest,
        post_digest=digest_fixture_service_state(post), fingerprint=fingerprint,
        preview_id=preview.preview_id,
        receipt_id=build_record_id("work_receipt", token),
        state_delta_id=delta.delta_id,
    )
    return replace(post, events=(*state.events, event)), event, preview, delta


def restore_fixture_service(material: object) -> FixtureServiceState:
    """Rebuild every authoritative bit from serializable committed events."""
    if type(material) is not dict or set(material) != {
        "profile", "progress", "abandoned", "secured", "events",
    } or material["profile"] != SERVICE_PROFILE or type(material["events"]) is not list:
        raise FixtureServiceError("invalid fixture service checkpoint component")
    state = FixtureServiceState()
    event_keys = set(FixtureServiceEvent.__dataclass_fields__)
    for item in material["events"]:
        if type(item) is not dict or set(item) != event_keys:
            raise FixtureServiceError("malformed service event")
        try:
            saved = FixtureServiceEvent(**item)
            state, computed, _, _ = execute_fixture_service(
                state=state, command_id=saved.command_id,
                operation=saved.operation, method=saved.method,
                actor_id=saved.actor_id, target_id=saved.target_id,
                place_id=saved.place_id, logical_before=saved.logical_before,
                logical_after=saved.logical_after,
                time_receipt_id=saved.time_receipt_id, qualified=True,
                expected_pre_digest=digest_fixture_service_state(state),
            )
        except (TypeError, ValueError) as exc:
            raise FixtureServiceError("service transition replay failed") from exc
        if computed != saved:
            raise FixtureServiceError("service transition provenance diverged")
    if (material["progress"], material["abandoned"], material["secured"]) != (
        state.progress, state.abandoned, state.secured,
    ):
        raise FixtureServiceError("service state differs from replay")
    return state


def serialize_fixture_service(state: FixtureServiceState) -> dict[str, object]:
    return {
        "profile": SERVICE_PROFILE, "progress": state.progress,
        "abandoned": state.abandoned, "secured": state.secured,
        "events": [asdict(x) for x in state.events],
    }
