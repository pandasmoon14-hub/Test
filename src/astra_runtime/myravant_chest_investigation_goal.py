"""Source-qualified Chest investigation across persistent memory and real action.

The investigative goal never owns current world truth, NPC memory, movement,
visual sensing, physical contact, or displacement. Its role is interpreting one
player choice into an already-qualified application command. Competing witness
and reported evidence remain independent even after the Chest physically moves.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from astra_runtime.myravant_actor_situated_knowledge import last_actor_evidence
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import GROUNDSKEEPER_ID, TOOL_CHEST_ID
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@dataclass(frozen=True, kw_only=True)
class ChestInvestigation:
    raw_text: str
    method: str | None
    report_place: str | None = None


_GOAL = re.compile(
    r"^(?:(?:i (?:want|need) to|how (?:do|can) i|can i) )?"
    r"(?:trace|investigate|locate|find|resolve) "
    r"(?:the )?(?:tool )?chest (?:with|alongside) "
    r"(?:the )?groundskeeper"
    r"(?: (?:by|using|through|via) (?P<method>.+))?$"
)
_REPORT = re.compile(
    r"^(?:reporting|giving an unverified report of|reporting it at) "
    r"(?:the )?(?P<place>yard|gatehouse|workshop|orchard path)$"
)
_METHODS = {
    "having groundskeeper witness it": "witness",
    "having the groundskeeper inspect the chest": "witness",
    "asking groundskeeper to inspect chest": "witness",
    "asking for a firsthand sighting": "witness",
    "asking for a first hand sighting": "witness",
    "comparing eyewitness and reported leads": "compare",
    "comparing their leads": "compare",
    "comparing the two leads": "compare",
    "asking what groundskeeper witnessed": "recall_witness",
    "asking about the firsthand sighting": "recall_witness",
    "asking what groundskeeper was told": "recall_report",
    "asking about the unverified report": "recall_report",
    "following the firsthand lead": "follow_witness",
    "following the witnessed lead": "follow_witness",
    "following the eyewitness lead": "follow_witness",
    "following the reported lead": "follow_report",
    "following the unverified report": "follow_report",
    "checking chest by touch": "touch",
    "asking groundskeeper to touch chest": "touch",
    "inspecting the chest myself": "player_inspect",
    "checking the chest myself": "player_inspect",
    "pushing the chest east": "push_east",
    "pushing chest to orchard": "push_east",
}


def parse_chest_investigation(raw: str) -> ChestInvestigation | None:
    normalized = " ".join(raw.strip().casefold().split()).rstrip("!? .")
    match = _GOAL.fullmatch(normalized)
    if match is None:
        return None
    method_raw = match.group("method")
    if method_raw is None:
        return ChestInvestigation(raw_text=raw, method="compare")
    # Do not silently execute the first action of a chained instruction.
    if re.search(r"\b(?:and|then|afterwards)\b", method_raw):
        return None
    report = _REPORT.fullmatch(method_raw)
    if report is not None:
        return ChestInvestigation(
            raw_text=raw, method="report", report_place=report.group("place"),
        )
    return ChestInvestigation(
        raw_text=raw, method=_METHODS.get(method_raw, "unqualified"),
    )


def execute_chest_investigation(
    app: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    request = parse_chest_investigation(raw)
    if request is None:
        raise ValueError("not a Chest investigation request")
    before = app.authoritative_digest()

    def refusal(reason: str, message: str) -> PlayApplicationResult:
        return PlayApplicationResult(
            result_type="chest_investigation_unavailable",
            message=message, authoritative_changed=False,
            failure_class=reason,
            pre_state_digest=before, post_state_digest=before,
        )

    if request.method == "unqualified":
        return refusal(
            "chest_investigation_method_unqualified",
            "That method has no qualified route in this investigation.",
        )

    # Independent local physical acts never become NPC memory by themselves.
    if request.method == "push_east":
        return app.displace_object("chest", "east", method="push")
    if request.method == "player_inspect":
        return app.inspect("chest")

    # No consultation of private NPC memory or co-opted NPC action when
    # the player cannot actually speak with the actor in the same place.
    if app.entity_place_id(GROUNDSKEEPER_ID) != app.current_place_id():
        return refusal(
            "chest_investigation_actor_not_local",
            "The Groundskeeper is not here to compare or act on leads.",
        )

    if request.method == "compare":
        firsthand = last_actor_evidence(
            app.knowledge_state, GROUNDSKEEPER_ID, TOOL_CHEST_ID,
            source_kind="witnessed",
        )
        hearsay = last_actor_evidence(
            app.knowledge_state, GROUNDSKEEPER_ID, TOOL_CHEST_ID,
            source_kind="reported",
        )
        if firsthand is None and hearsay is None:
            return PlayApplicationResult(
                result_type="chest_investigation_leads_observed",
                message=(
                    "The Groundskeeper has no recorded Chest sightings or "
                    "attributed reports. A local visual observation and a "
                    "player's unverified report are separate choices."
                ),
                authoritative_changed=False,
                pre_state_digest=before, post_state_digest=before,
            )
        pieces: list[str] = []
        for event, kind in (
            (firsthand, "firsthand sighting"),
            (hearsay, "player's unverified report"),
        ):
            if event is None:
                pieces.append(f"No {kind} is recorded.")
            else:
                place = app.fixture.place_presentation(
                    event.reported_place_id,
                ).name
                pieces.append(
                    f"Last {kind}: {place} at logical step "
                    f"{event.logical_step}."
                )
        pieces.append(
            "These are separate historical sources, not evidence of the "
            "Chest's current location. You may ask the Groundskeeper to "
            "follow either qualified lead, inspect a local Chest, or "
            "choose an independent physical action."
        )
        return PlayApplicationResult(
            result_type="chest_investigation_leads_observed",
            message=" ".join(pieces), authoritative_changed=False,
            pre_state_digest=before, post_state_digest=before,
        )

    operations = {
        "witness": "witness",
        "recall_witness": "last_saw",
        "recall_report": "heard",
        "follow_witness": "follow_sighting",
        "follow_report": "follow_report",
        "touch": "touch",
    }
    if request.method == "report":
        return app.actor_memory_interaction(
            "report", "chest", reported_place=request.report_place,
        )
    return app.actor_memory_interaction(operations[request.method], "chest")
