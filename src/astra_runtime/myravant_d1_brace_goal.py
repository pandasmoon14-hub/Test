"""D-1 player interpretation of a conserved noncanonical chest component.

Parser owns no materials, identity or world state. Other methods and novel
attempts retain the terminal's existing fallback/refusal semantics.
"""
from __future__ import annotations

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

_ACTIONS = {
    "remove chest brace": "manual",
    "loosen chest brace": "manual",
    "pull chest brace free": "manual",
    "continue removing chest brace": "manual",
    "resume removing chest brace": "manual",
    "remove the chest brace": "manual",
    "remove chest brace with lantern": "lantern",
    "detach chest brace with lantern": "lantern",
    "remove the chest brace with lantern": "lantern",
    "refit chest brace": "refit",
    "reinstall chest brace": "refit",
    "reattach chest brace": "refit",
    "tighten chest brace": "refit",
    "inspect chest brace": "inspect",
    "check chest brace": "inspect",
    "check brace condition": "inspect",
}


def parse_d1_brace(raw: str) -> str | None:
    return _ACTIONS.get(" ".join(raw.strip().casefold().split()).rstrip(".!?"))


def execute_d1_brace(
    application: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    method = parse_d1_brace(raw)
    if method is None:
        raise ValueError("not a fixture-brace material request")
    if method == "inspect":
        return application.inspect_chest_brace()
    return application.alter_chest_brace(method)
