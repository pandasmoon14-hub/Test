"""Interpret one fixture-declared NPC labor method, never a generic hire.

The player must physically supply a lit Lantern at the Yard. RT-010 owns
actual latch work, and WORLD-2 owns the paid work tick.
"""
from __future__ import annotations

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

_REQUESTS = frozenset({
    "ask groundskeeper to repair chest latch with lantern",
    "ask the groundskeeper to repair the chest latch with lantern",
    "ask groundskeeper to service chest latch with lantern",
    "ask groundskeeper to work on chest latch with lantern",
    "request groundskeeper to service chest latch using lantern",
    "have groundskeeper repair chest latch with lantern",
})


def parse_e2_actor_service(raw_text: str) -> str | None:
    normalized = " ".join(raw_text.strip().casefold().split()).rstrip(".!?")
    return "lantern" if normalized in _REQUESTS else None


def execute_e2_actor_service(
    application: MyravantVSM14Application, raw_text: str,
) -> PlayApplicationResult:
    method = parse_e2_actor_service(raw_text)
    if method is None:
        raise ValueError("not a licensed E2 Groundskeeper work request")
    return application.request_groundskeeper_latch_work(method=method)
