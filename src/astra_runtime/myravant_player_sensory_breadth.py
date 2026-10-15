"""BREADTH-1 public player attempts: bodily holdings and near-field touch.

Interpret method and target without pretending every object is contactable.
Neither this parser nor its executor owns world truth, actor anatomy or a
general sensory system. Fixture and AFQR-20 evidence qualify actual contact.
"""
from __future__ import annotations

import re

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

_HOLDINGS = frozenset({
    "check my hands",
    "look at my hands",
    "examine what i am carrying",
    "check what i'm carrying",
    "check what i am carrying",
    "check my belongings",
    "inspect my carried objects",
    "what am i holding",
    "what do i have in my hands",
    "look down at my belongings",
})
_TARGET_PATTERNS = (
    re.compile(r"^touch (.+)$"),
    re.compile(r"^feel for (.+)$"),
    re.compile(r"^feel around for (.+)$"),
    re.compile(r"^search by touch for (.+)$"),
    re.compile(r"^locate (.+) by touch$"),
    re.compile(r"^run (?:my|your) (?:hand|hands) along (.+)$"),
)


def parse_player_sensory_attempt(raw_text: str) -> tuple[str, str] | None:
    normalized = " ".join(raw_text.strip().casefold().split()).rstrip(".!?")
    if normalized in _HOLDINGS:
        return ("holdings", "")
    for pattern in _TARGET_PATTERNS:
        match = pattern.fullmatch(normalized)
        if match is None:
            continue
        target = match.group(1).strip()
        # Do not infer missing, implicit, possessive or deictic targets.
        if target.startswith("the "):
            target = target[4:]
        if target.startswith("a "):
            target = target[2:]
        if target.startswith("an "):
            target = target[3:]
        return ("contact", target)
    return None


def execute_player_sensory_attempt(
    app: MyravantVSM14Application, raw_text: str,
) -> PlayApplicationResult:
    parsed = parse_player_sensory_attempt(raw_text)
    if parsed is None:
        raise ValueError("not a qualified player sensory attempt")
    operation, target = parsed
    if operation == "holdings":
        return app.inspect_personal_holdings()
    return app.feel_for_local_object(target)
