"""Bounded, actor-situated inquiry over already-owned current custody.

This adapter interprets a few ordinary questions, but it does not own NPC
knowledge, memory, sight, consent, object custody, or authoritative state.
The noncanonical Groundskeeper is explicitly willing to disclose only their
*present own carrying* facts when co-located with the player. Questions about
other locations, histories, and third-party state remain unattested.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_follow_intent import (
    active_follow_intent_for,
)
from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    MyravantPlayApplicationError,
    PlayApplicationResult,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    UnavailableFixtureCustodyError,
    UnavailableFixtureHandoffError,
)


# These acceptance and disclosure boundaries belong only to the noncanonical
# development fixture. They do not establish general NPC social rules.
_DISCLOSING_ACTORS = frozenset({GROUNDSKEEPER_ID})
_INTRO = re.compile(
    r"^(?:i\s+)?ask\s+(?:the\s+)?groundskeeper\s+"
    r"(?:if|whether|do|does|where|what|are|is)\s+(.+)$",
    re.IGNORECASE,
)
_SUBJECT = r"(?:you|he|they|the\s+groundskeeper)"
_CARRIES = re.compile(
    rf"^{_SUBJECT}\s+(?:are|is)\s+(?:carrying|holding)\s+(.+)$",
    re.IGNORECASE,
)
_HAS = re.compile(
    rf"^{_SUBJECT}\s+(?:has|have)\s+(.+)$",
    re.IGNORECASE,
)
_DOES_HAVE = re.compile(
    rf"^{_SUBJECT}\s+(?:have|has)\s+(.+)$",
    re.IGNORECASE,
)
_WHAT_CARRY = re.compile(
    rf"^(?:are|is)\s+{_SUBJECT}\s+(?:carrying|holding)(?:\s+anything)?$",
    re.IGNORECASE,
)
_FOLLOWS = re.compile(
    rf"^{_SUBJECT}\s+(?:are|is)\s+following\s+me$",
    re.IGNORECASE,
)
_SIMPLE_FOLLOWS = re.compile(
    rf"^{_SUBJECT}\s+following\s+me$",
    re.IGNORECASE,
)
_WHERE_IS = re.compile(
    r"^(?:is|are)\s+(.+?)$|^(.+?)\s+(?:is|are)$",
    re.IGNORECASE,
)


@dataclass(frozen=True, kw_only=True)
class ParsedSituatedInquiry:
    raw_text: str
    parsed: bool
    kind: str | None = None
    object_reference: str | None = None


def _object_phrase(words: str) -> str:
    target = " ".join(words.casefold().strip(" \t\r\n?.!").split())
    if target.startswith("the "):
        target = target[4:]
    return target


def parse_situated_inquiry(raw_text: str) -> ParsedSituatedInquiry:
    """Parse qualified actor questions, never custody or NPC commands."""

    normalized = " ".join(raw_text.strip().split()).rstrip("?.!")
    introductory = _INTRO.fullmatch(normalized)
    if introductory is None:
        return ParsedSituatedInquiry(raw_text=raw_text, parsed=False)

    # Preserve the interrogative intent: 'ask ... for' and 'ask ... to'
    # never enter this parser, even when their target is a lantern.
    prefix = normalized.casefold()
    head = prefix.split("groundskeeper ", 1)[-1].split(" ", 1)[0]
    content = introductory.group(1)
    kind: str | None = None
    object_reference: str | None = None

    if head in {"if", "whether"}:
        carrying = _CARRIES.fullmatch(content) or _HAS.fullmatch(content)
        if carrying is not None:
            kind = "own_custody"
            object_reference = _object_phrase(carrying.group(1))
        elif _FOLLOWS.fullmatch(content):
            kind = "own_follow_intent"
        else:
            kind = "unattested"
    elif head in {"are", "is"}:
        kind = (
            "own_follow_intent"
            if _SIMPLE_FOLLOWS.fullmatch(content)
            else "unattested"
        )
    elif head in {"do", "does"}:
        carrying = _DOES_HAVE.fullmatch(content)
        if carrying is not None:
            kind = "own_custody"
            object_reference = _object_phrase(carrying.group(1))
        else:
            kind = "unattested"
    elif head == "what":
        if _WHAT_CARRY.fullmatch(content) is not None:
            kind = "own_inventory"
        else:
            kind = "unattested"
    elif head == "where":
        where = _WHERE_IS.fullmatch(content)
        if where is not None:
            kind = "own_custody_location"
            object_reference = _object_phrase(
                where.group(1) or where.group(2) or ""
            )
        else:
            kind = "unattested"

    return ParsedSituatedInquiry(
        raw_text=raw_text,
        parsed=True,
        kind=kind,
        object_reference=object_reference,
    )


def execute_situated_inquiry(
    application: MyravantPlayApplication, raw_text: str,
) -> PlayApplicationResult:
    """Present a bounded actor's voluntary present-tense custody attestation."""

    parsed = parse_situated_inquiry(raw_text)
    if not parsed.parsed:
        raise ValueError("input is not a qualified situated inquiry")

    digest = application.authoritative_digest()

    def answer(result_type: str, message: str, failure: str | None = None):
        return PlayApplicationResult(
            result_type=result_type,
            message=message,
            authoritative_changed=False,
            pre_state_digest=digest,
            post_state_digest=digest,
            failure_class=failure,
        )

    try:
        actor_id = application.fixture.resolve_actor_reference("groundskeeper")
    except UnavailableFixtureHandoffError:
        return answer(
            "situated_inquiry_unavailable",
            "There is no qualified actor to answer that question.",
            "inquiry_actor_unqualified",
        )
    if actor_id not in _DISCLOSING_ACTORS:
        return answer(
            "situated_inquiry_unavailable",
            "That actor has not agreed to disclose this information.",
            "inquiry_disclosure_unqualified",
        )

    try:
        actor_place = application.entity_place_id(actor_id)
    except MyravantPlayApplicationError:
        actor_place = None
    if actor_place != application.current_place_id():
        return answer(
            "situated_inquiry_unavailable",
            "The Groundskeeper is not here to answer.",
            "inquiry_actor_not_local",
        )

    if parsed.kind == "unattested":
        return answer(
            "situated_inquiry_unknown",
            "The Groundskeeper cannot attest to that from current evidence.",
            "inquiry_fact_unattested",
        )

    if parsed.kind == "own_follow_intent":
        follow_state = getattr(application, "follow_intent_state", None)
        if follow_state is None:
            return answer(
                "situated_inquiry_unknown",
                "The Groundskeeper cannot attest to a following commitment.",
                "inquiry_follow_state_unavailable",
            )
        active = active_follow_intent_for(follow_state, actor_id)
        following_player = (
            active is not None
            and active.leader_entity_id == application.fixture.player_entity_id
        )
        return answer(
            "situated_inquiry_answered",
            (
                'The Groundskeeper says, "Yes, I am following you."'
                if following_player else
                'The Groundskeeper says, "No, I am not following you."'
            ),
        )

    carrying = application.fixture.public_entities_carried_by(
        application.state.representation, actor_id
    )
    if parsed.kind == "own_inventory":
        if not carrying:
            return answer(
                "situated_inquiry_answered", 'The Groundskeeper says, "I am carrying nothing."'
            )
        names = ", ".join(item.name for item in carrying)
        return answer(
            "situated_inquiry_answered",
            f'The Groundskeeper says, "I am carrying: {names}."',
        )

    target = parsed.object_reference or ""
    try:
        object_id = application.fixture.resolve_object_reference(target)
    except UnavailableFixtureCustodyError:
        return answer(
            "situated_inquiry_unknown",
            "The Groundskeeper cannot identify that object.",
            "inquiry_object_unqualified",
        )
    held = any(item.entity_id == object_id for item in carrying)
    if parsed.kind == "own_custody":
        message = (
            'The Groundskeeper says, "Yes, I am carrying that."'
            if held else
            'The Groundskeeper says, "No, I am not carrying that."'
        )
        return answer("situated_inquiry_answered", message)
    if parsed.kind == "own_custody_location":
        if held:
            return answer(
                "situated_inquiry_answered",
                'The Groundskeeper says, "I have that object with me."',
            )
        return answer(
            "situated_inquiry_unknown",
            'The Groundskeeper says, "I cannot verify where that object is."',
            "inquiry_location_unattested",
        )
    return answer(
        "situated_inquiry_unknown",
        "The Groundskeeper cannot attest to that from current evidence.",
        "inquiry_fact_unattested",
    )
