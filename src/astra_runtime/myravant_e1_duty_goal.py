"""Parse only the noncanonical Yard latch-duty offer and its local followups.

No command here licenses a generic NPC employment, payment or promise system.
"""
from __future__ import annotations

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

_ACTIONS = {
    "ask groundskeeper to secure chest latch later": "request",
    "ask the groundskeeper to secure the chest latch later": "request",
    "ask groundskeeper to secure the chest when ready": "request",
    "request groundskeeper to secure serviced chest": "request",
    "offer groundskeeper the chest latch duty": "request",
    "cancel groundskeeper chest duty": "cancel",
    "cancel the groundskeeper chest duty": "cancel",
    "tell groundskeeper to cancel the chest duty": "cancel",
    "withdraw groundskeeper chest duty": "cancel",
    "check groundskeeper chest duty": "check",
    "ask groundskeeper about chest duty": "check",
    "inspect groundskeeper chest duty": "check",
    "check chest duty": "check",
}


def parse_e1_latch_duty(raw: str) -> str | None:
    return _ACTIONS.get(" ".join(raw.strip().casefold().split()).rstrip(".!?"))


def execute_e1_latch_duty(
    application: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    action = parse_e1_latch_duty(raw)
    if action is None:
        raise ValueError("not an E1 qualified local agreement")
    return application.groundskeeper_chest_duty(action)
