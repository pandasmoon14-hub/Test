"""Goal-directed physical choice over existing lawful placement owners.

Noncanonical Lantern -> Orchard Path fixture only. Interpret a desired
destination and a player's chosen *method* separately; do not create an
omniscient planner, autonomous multi-step executor or new world truth.
Every mutating result comes directly from COMP-3 or actor-mediated COMP-3.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, YARD_ID,
)
from astra_runtime.myravant_vsm13_actor_mediated_displacement import (
    execute_vsm13_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@dataclass(frozen=True, kw_only=True)
class LanternDestinationGoal:
    raw_text: str
    destination: str
    method: str | None
    raw_method: str | None


_GOAL = re.compile(
    r"^(?:(?:i (?:want|need) to|can i|how (?:do|can) i) )?"
    r"(?:get|send|deliver|move|bring|take|put) (?:the )?"
    r"(?:brass )?lantern (?:to|into|onto) (?:the )?"
    r"(?:orchard|orchard path)"
    r"(?: (?:by|using|with|via) (.+))?$"
)
_METHODS = {
    "push": "push", "pushing": "push", "pushing it": "push",
    "shove": "push", "shoving": "push", "ground push": "push",
    "throw": "throw", "throwing": "throw", "throwing it": "throw",
    "toss": "throw", "tossing": "throw", "tossing it": "throw",
    "ask groundskeeper": "actor_throw",
    "asking groundskeeper": "actor_throw",
    "asking the groundskeeper": "actor_throw",
    "groundskeeper": "actor_throw",
    "the groundskeeper": "actor_throw",
    "asking groundskeeper to throw": "actor_throw",
    "asking the groundskeeper to throw it": "actor_throw",
    "having groundskeeper throw it": "actor_throw",
    "having the groundskeeper throw it": "actor_throw",
}


def parse_lantern_destination_goal(raw: str) -> LanternDestinationGoal | None:
    normalized = " ".join(raw.strip().casefold().split()).rstrip(".!?")
    match = _GOAL.fullmatch(normalized)
    if match is None:
        return None
    raw_method = match.group(1)
    return LanternDestinationGoal(
        raw_text=raw,
        destination="orchard_path",
        method=(_METHODS.get(raw_method, "unqualified") if raw_method else None),
        raw_method=raw_method,
    )


def _read_placement(app: MyravantVSM14Application) -> tuple[str, str] | None:
    placements = [
        rel for rel in app.state.representation.relations
        if rel.subject_entity_id == LANTERN_ID
        and rel.relation_type in {
            LOCATED_AT_RELATION_TYPE, CARRIED_BY_RELATION_TYPE,
        }
    ]
    if len(placements) != 1:
        return None
    rel = placements[0]
    return rel.relation_type, rel.object_entity_id


def execute_lantern_destination_goal(
    app: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    goal = parse_lantern_destination_goal(raw)
    if goal is None:
        raise ValueError("not a qualified Lantern destination goal")
    pre = app.authoritative_digest()

    def refusal(message: str, reason: str) -> PlayApplicationResult:
        return PlayApplicationResult(
            result_type="destination_goal_unavailable", message=message,
            authoritative_changed=False, failure_class=reason,
            pre_state_digest=pre, post_state_digest=pre,
        )

    # A local, explicitly qualified corridor; never report unseen
    # remote placement or treat a distant NPC as present.
    if app.current_place_id() != YARD_ID:
        return refusal(
            "You need to reach the Yard before using this local route.",
            "destination_goal_worksite_not_local",
        )

    placement = _read_placement(app)
    grounded_here = placement == (LOCATED_AT_RELATION_TYPE, YARD_ID)
    carried_by_player = placement == (
        CARRIED_BY_RELATION_TYPE, app.fixture.player_entity_id,
    )
    npc_here = app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID

    if goal.method is None:
        if grounded_here:
            advice = (
                "The Lantern is grounded here. You can try pushing it east "
                "toward Orchard Path. To throw it yourself, first take it."
            )
        elif carried_by_player:
            advice = (
                "You carry the Lantern. You can try throwing it east "
                "toward Orchard Path. To push it, first put it down."
            )
        else:
            advice = (
                "There is no locally established player-held or grounded "
                "Lantern for this route."
            )
        if npc_here:
            advice += (
                " You can also ask the nearby Groundskeeper to throw it "
                "if that actor lawfully carries it."
            )
        return PlayApplicationResult(
            result_type="destination_goal_methods_observed",
            message=advice,
            authoritative_changed=False,
            pre_state_digest=pre, post_state_digest=pre,
        )

    if goal.method == "unqualified":
        return refusal(
            "That proposed method has no qualified local way to move "
            "the Lantern to Orchard Path.",
            "destination_goal_method_unqualified",
        )

    if goal.method == "push":
        # Existing COMP-3 owns the physical method and its receipt; the
        # goal interpreter must not assert success on its own.
        return app.displace_object("lantern", "east", method="push")

    if goal.method == "throw":
        return app.displace_object("lantern", "east", method="throw")

    if goal.method == "actor_throw":
        # Preserve voluntary, situated actor acceptance and actual
        # performing-actor attribution through preexisting VSM-13.
        return execute_vsm13_request(
            app, "ask groundskeeper to throw lantern east",
        ).result

    raise AssertionError("unreachable normalized goal method")
