"""B-2a terminal interpretation for one explicitly licensed service activity.

A natural-language route supplies intent only; the qualified backend owns
persistent labor, method differences, logical time and resulting latch state.
"""

from __future__ import annotations

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

_ACTIONS = {
    "service chest latch": ("work", "manual"),
    "work on chest latch": ("work", "manual"),
    "resume chest latch service": ("work", "manual"),
    "continue chest latch service": ("work", "manual"),
    "repair chest latch": ("work", "manual"),
    "service chest latch with lantern": ("work", "lantern"),
    "repair chest latch with lantern": ("work", "lantern"),
    "check chest latch service": ("check", "none"),
    "check latch service": ("check", "none"),
    "inspect chest latch progress": ("check", "none"),
    "abandon chest latch service": ("abandon", "none"),
    "abandon latch service": ("abandon", "none"),
    "secure chest": ("secure", "none"),
    "secure the chest": ("secure", "none"),
    "release chest latch": ("release", "none"),
    "release the chest latch": ("release", "none"),
}


def parse_b2a_service(raw: str) -> tuple[str, str] | None:
    normalized = " ".join(raw.strip().casefold().split()).rstrip(".!?")
    return _ACTIONS.get(normalized)


def execute_b2a_service(
    app: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    parsed = parse_b2a_service(raw)
    if parsed is None:
        raise ValueError("unrecognized B-2a fixture service request")
    operation, method = parsed
    if operation == "check":
        return app.check_chest_latch()
    return app.service_chest_latch(operation, method=method)
