"""Two resumable noncanonical undertakings expressed through *existing* state.

The state of each work goal is a projection of owner-committed location,
lit-state or open-state changes. This interpreter neither stores a second work
ledger nor owns time, consumption, material rules, process duration, or RNG.
This is a first gameplay bridge, not general crafting or timed construction.
"""

from __future__ import annotations

import re

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, TOOL_CHEST_ID, WORKSHOP_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


_GOALS = {
    "prepare lantern for yard": "prepare_lantern",
    "prepare the lantern for the yard": "prepare_lantern",
    "lantern preparation": "prepare_lantern",
    "stage chest in workshop": "stage_chest",
    "stage the chest in the workshop": "stage_chest",
    "chest staging": "stage_chest",
}
_PREFIX = re.compile(
    r"^(?:(?P<verb>work on|continue|resume|check|inspect progress on)\s+)?(?P<goal>.+?)\s*[.!?]*$",
    re.IGNORECASE,
)


def parse_bounded_work_goal(raw: str) -> tuple[str, bool] | None:
    normalized = " ".join(raw.strip().casefold().split()).rstrip(".!?")
    match = _PREFIX.fullmatch(normalized)
    if match is None:
        return None
    goal = _GOALS.get(match.group("goal"))
    if goal is None:
        return None
    return goal, match.group("verb") in {"check", "inspect progress on"}


def _response(
    app: MyravantVSM14Application, message: str, *, failure: str | None = None,
    kind: str = "bounded_work_status",
) -> PlayApplicationResult:
    digest = app.authoritative_digest()
    return PlayApplicationResult(
        result_type=kind, message=message, authoritative_changed=False,
        pre_state_digest=digest, post_state_digest=digest, failure_class=failure,
    )


def _single_placement(app, target: str) -> tuple[str, str] | None:
    placement = [
        (r.relation_type, r.object_entity_id)
        for r in app.state.representation.relations
        if r.subject_entity_id == target
        and r.relation_type in (LOCATED_AT_RELATION_TYPE, CARRIED_BY_RELATION_TYPE)
    ]
    return placement[0] if len(placement) == 1 else None


def execute_bounded_work_goal(
    app: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    """Carry forward exactly one stage through a current authoritative owner.

    Status is limited to the observed/local worksite. Remote goal-state
    inspection must not leak a hidden target's changing committed placement.
    Any refusal or interruption leaves owner state intact for future resume.
    """
    parsed = parse_bounded_work_goal(raw)
    if parsed is None:
        raise ValueError("not a bounded undertaking")
    goal, inspect_only = parsed
    current = app.current_place_id()
    target = LANTERN_ID if goal == "prepare_lantern" else TOOL_CHEST_ID
    placement = _single_placement(app, target)
    # A work plan may not read remote object facts into player narration.
    local = placement is not None and (
        placement == (LOCATED_AT_RELATION_TYPE, current)
        or placement == (
            CARRIED_BY_RELATION_TYPE, app.fixture.player_entity_id
        )
    )
    if not local:
        return _response(
            app, "That worksite or required object is not accessible here.",
            failure="bounded_work_target_not_local",
        )

    if goal == "prepare_lantern":
        lit = app.object_lit_state(LANTERN_ID)
        if lit is None:
            return _response(
                app, "This fixture does not qualify that lantern preparation.",
                failure="bounded_work_lit_state_unqualified",
            )
        if current == YARD_ID and lit.state == "lit" and placement == (
            LOCATED_AT_RELATION_TYPE, YARD_ID,
        ):
            return _response(app, "The lantern preparation is complete.")
        if inspect_only:
            if lit.state != "lit":
                next_step = "light the local lantern"
            elif current == WORKSHOP_ID and placement == (
                LOCATED_AT_RELATION_TYPE, WORKSHOP_ID,
            ):
                next_step = "move the lit lantern toward the yard"
            elif placement[0] == CARRIED_BY_RELATION_TYPE:
                next_step = "bring the carried lantern to the yard and set it down"
            else:
                next_step = "finish positioning the prepared lantern"
            return _response(app, f"Lantern work remains: {next_step}.")
        if lit.state != "lit":
            return app.light_object("lantern")
        if current == WORKSHOP_ID and placement == (
            LOCATED_AT_RELATION_TYPE, WORKSHOP_ID,
        ):
            return app.displace_object("lantern", "south", method="slide")
        if current == YARD_ID and placement[0] == CARRIED_BY_RELATION_TYPE:
            return app.drop("lantern")
        return _response(
            app, "That stage requires another lawful movement or placement.",
            failure="bounded_work_stage_requires_player_action",
        )

    if current == WORKSHOP_ID and placement == (
        LOCATED_AT_RELATION_TYPE, WORKSHOP_ID,
    ):
        opened = app.object_open_state(TOOL_CHEST_ID)
        if opened is None:
            return _response(
                app, "This fixture does not qualify chest access work.",
                failure="bounded_work_open_state_unqualified",
            )
        if opened.state == "open":
            return _response(app, "The workshop chest staging is complete.")
        if inspect_only:
            return _response(app, "Chest staging remains: open the local chest.")
        return app.open_object("chest")
    if current == YARD_ID and placement == (
        LOCATED_AT_RELATION_TYPE, YARD_ID,
    ):
        if inspect_only:
            return _response(
                app, "Chest staging remains: move the chest into the workshop.",
            )
        return app.displace_object("chest", "north", method="push")
    return _response(
        app, "That stage requires another lawful movement or placement.",
        failure="bounded_work_stage_requires_player_action",
    )
