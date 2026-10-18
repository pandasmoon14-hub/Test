"""Player goal/method composition over existing fixture-authorized object routes.

Declared fixture object/place references select explicitly licensed routes;
this is not a planner. RT-010/COMP-3 owns every displacement,
AFQR-19 owns opportunity and WORLD-2 owns exit obstruction. Read-only
choices use only co-local visually qualified or player-carried object context.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import (
    ORCHARD_PATH_ID, TOOL_CHEST_ID, WAYSTONE_ID,
    WORKSHOP_ID, YARD_ID, GATEHOUSE_ID, LANTERN_ID,
    MyravantPlayFixture, UnavailableFixtureCustodyError, UnknownFixturePlaceError,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@dataclass(frozen=True, kw_only=True)
class ParsedPhysicalGoal:
    raw_text: str
    target_id: str
    destination_id: str
    method: str | None
    clearance: bool = False
    target_reference: str | None = None


_GOAL = re.compile(
    r"^(?:(?:i (?:want|need) to|how (?:do|can) i|can i) )?"
    r"(?:get|move|bring|send|put|take) (?:the )?"
    r"(?P<object>.+?) "
    r"(?P<placement>to|into|onto) (?:the )?"
    r"(?P<destination>.+?)"
    r"(?: (?:by|with|using|via) (?P<method>.+))?$"
)
_CLEAR = re.compile(
    r"^(?:(?:i (?:want|need) to|how (?:do|can) i|can i) )?"
    r"clear (?:the )?(?:yard )?east (?:exit|passage|route)"
    r"(?: (?:by|with|using|via) (?P<method>.+))?$"
)
_TARGETS = {
    "lantern": LANTERN_ID,
    "brass lantern": LANTERN_ID,
    "chest": TOOL_CHEST_ID,
    "tool chest": TOOL_CHEST_ID,
    "waystone": WAYSTONE_ID,
    "weathered waystone": WAYSTONE_ID,
}
_PLACES = {
    "yard": YARD_ID,
    "workshop": WORKSHOP_ID,
    "orchard": ORCHARD_PATH_ID,
    "orchard path": ORCHARD_PATH_ID,
    "gatehouse": GATEHOUSE_ID,
}
_METHODS = {
    "push": "push",
    "pushing": "push",
    "pushing it": "push",
    "shove": "push",
    "shoving": "push",
    "shoving it": "push",
    "drag": "drag",
    "dragging": "drag",
    "dragging it": "drag",
    "slide": "slide",
    "sliding": "slide",
    "sliding it": "slide",
    "throw": "throw",
    "throwing": "throw",
    "throwing it": "throw",
    "toss": "throw",
    "tossing": "throw",
    "tossing it": "throw",
}


def parse_physical_placement_goal(
    raw: str, *, fixture: MyravantPlayFixture | None = None,
) -> ParsedPhysicalGoal | None:
    normalized = " ".join(raw.strip().casefold().split()).rstrip(".!?")
    # Never absorb a compound command or drop a material constraint while
    # resolving a target/destination. Method modifiers remain unqualified.
    if re.search(r"\b(?:then|and|while)\b", normalized):
        return None
    clear = _CLEAR.fullmatch(normalized)
    if clear is not None:
        if fixture is not None and WAYSTONE_ID not in {p.entity_id for p in fixture.object_presentations}:
            return None
        named_method = clear.group("method")
        return ParsedPhysicalGoal(
            raw_text=raw, target_id=WAYSTONE_ID,
            destination_id=WORKSHOP_ID,
            method=({**_METHODS,
                "pushing waystone north": "push",
                "pushing the waystone north": "push",
                "push waystone north": "push",
                "push the waystone north": "push",
            }.get(named_method, "unqualified") if named_method else None),
            clearance=True,
        )
    match = _GOAL.fullmatch(normalized)
    if match is None:
        return None
    named_method = match.group("method")
    if fixture is None:
        # Compatibility for parser-only callers; execution always supplies
        # the actual fixture, including renamed and additional neutral targets.
        target = _TARGETS.get(match.group("object"))
        destination = _PLACES.get(match.group("destination"))
        if target is None or destination is None:
            return None
    else:
        try:
            target = fixture.resolve_object_reference(match.group("object"))
            destination = fixture.resolve_place_reference(match.group("destination"))
        except (UnavailableFixtureCustodyError, UnknownFixturePlaceError):
            return None
    if (fixture is not None and match.group("placement") != "to"
        and destination in dict(fixture.position_areas)):
        # A work position is not the supporting surface or interior of a
        # similarly named fitting. Preserve the requested relationship.
        return None
    return ParsedPhysicalGoal(
        raw_text=raw,
        target_id=target,
        destination_id=destination,
        method=_METHODS.get(named_method, "unqualified") if named_method else None,
        target_reference=match.group("object"),
    )


def execute_physical_placement_goal(
    app: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    parsed = parse_physical_placement_goal(raw, fixture=app.fixture)
    if parsed is None:
        raise ValueError("not a bounded physical placement goal")
    before = app.authoritative_digest()

    def reject(message: str, failure: str) -> PlayApplicationResult:
        return PlayApplicationResult(
            result_type="physical_goal_refused",
            message=message, authoritative_changed=False,
            pre_state_digest=before, post_state_digest=before,
            failure_class=failure,
        )

    here = app.current_place_id()
    is_grounded_here = any(
        rel.relation_type == LOCATED_AT_RELATION_TYPE
        and rel.subject_entity_id == parsed.target_id
        and rel.object_entity_id == here
        for rel in app.state.representation.relations
    )
    # Avoid leaking object placement and a dark-room target through method
    # advice. The underlying COMP-3 path remains responsible for an explicitly
    # attempted method and its own AFQR-20/AFQR-19 legality.
    is_carried_by_player = any(
        rel.relation_type == CARRIED_BY_RELATION_TYPE
        and rel.subject_entity_id == parsed.target_id
        and rel.object_entity_id == app.fixture.player_entity_id
        for rel in app.state.representation.relations
    )
    if parsed.method is None and (
        not is_carried_by_player and (
            not is_grounded_here
            or not app._object_currently_observable(parsed.target_id)
        )
    ):
        return reject(
            "There is no currently qualified local observation of that "
            "object for this physical goal.",
            "physical_goal_local_evidence_unavailable",
        )

    if parsed.method == "unqualified":
        return reject(
            "That proposed method is not qualified for this physical goal.",
            "physical_goal_method_unqualified",
        )

    if not is_grounded_here and not (
        is_carried_by_player and parsed.method in {None, "throw"}
    ):
        return reject(
            "You cannot establish the target on the ground at your "
            "current worksite for that physical goal.",
            "physical_goal_local_placement_unavailable",
        )

    routes = tuple(
        route for route in app.fixture.object_displacement_routes
        if route.object_entity_id == parsed.target_id
        and route.source_place_id == here
        and route.destination_place_id == parsed.destination_id
        and (route.method == "throw" if is_carried_by_player else route.method != "throw")
    )

    if parsed.method is None:
        if not routes:
            return reject(
                "No licensed one-step physical placement route connects "
                "that local object to the proposed destination.",
                "physical_goal_destination_unavailable",
            )
        current = app.object_open_state(parsed.target_id)
        suggestions = []
        for route in routes:
            condition = ""
            if route.required_open_state is not None and (
                current is None or current.state != route.required_open_state
            ):
                condition = (
                    f" (requires the object to be {route.required_open_state})"
                )
            suggestions.append(
                f"{route.method} {route.direction}{condition}"
            )
        return PlayApplicationResult(
            result_type="physical_goal_methods_observed",
            message=(
                "From here, the declared physical route allows: "
                + "; ".join(suggestions)
                + ". These are conditional methods, not automatic moves."
            ),
            authoritative_changed=False,
            pre_state_digest=before, post_state_digest=before,
        )

    matching = [route for route in routes if route.method == parsed.method]
    if len(matching) != 1:
        return reject(
            "That method has no licensed one-step route for the proposed "
            "object and destination at this worksite.",
            "physical_goal_route_unavailable",
        )

    # Exact chosen method and direction pass unchanged to the existing
    # authoritative executor, including chest closure and drag observation.
    direction = matching[0].direction
    # Preserve the unique reference that actually resolved. A display name
    # may be shared by another object even when the supplied local ID is not.
    target_reference = parsed.target_reference or app.fixture.entity_name(parsed.target_id)
    return app.displace_object(target_reference, direction, method=parsed.method)
