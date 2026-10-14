"""B-2b interpretation: timed physical clearance through existing COMP-3.

Not a general labor controller: the waystone's placement and ordinary
displacement receipts remain sole authorities for actual route clearance.
"""
from __future__ import annotations

from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_play_application import PlayApplicationResult

_CLEAR = frozenset({
    "clear the waystone route", "clear waystone route",
    "clear route obstruction", "continue clearing the waystone",
    "continue waystone clearance", "resume waystone clearance",
    "recover waystone", "recover the waystone",
    "move the waystone out of the route",
})
_CHECK = frozenset({
    "check waystone clearance", "check route clearance",
    "status of waystone clearance", "inspect clearance work",
})
_ABANDON = frozenset({
    "abandon waystone clearance", "stop clearing the waystone",
    "cancel waystone clearance",
})


def parse_waystone_clearance(raw: str) -> str | None:
    candidate = " ".join(raw.casefold().strip().split()).rstrip(".!")
    if candidate in _CLEAR:
        return "continue"
    if candidate in _CHECK:
        return "check"
    if candidate in _ABANDON:
        return "abandon"
    return None


def execute_waystone_clearance(
    application: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    intent = parse_waystone_clearance(raw)
    if intent is None:
        raise ValueError("not a waystone clearance request")
    return application.clear_waystone_route(intent)
