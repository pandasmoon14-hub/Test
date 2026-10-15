"""Game-led Orchard supply attempt over existing movement, custody and object owners.

An independently chosen method performs AT MOST ONE existing authoritative
transition. This is not a task engine, silent multi-action plan, or permanent
"supplies" state. The scenario is noncanonical and world facts remain with
their original owners; advice uses only situated observed/owned context.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_storage_transfer import (
    containment_relation_for,
)
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, TOOL_CHEST_ID, WAYSTONE_ID,
    ORCHARD_PATH_ID, YARD_ID,
)
from astra_runtime.myravant_vsm13_actor_mediated_displacement import (
    execute_vsm13_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@dataclass(frozen=True, kw_only=True)
class OrchardSupplyAttempt:
    raw_text: str
    method: str | None
    is_status: bool = False


_GOAL = re.compile(
    r"^(?:(?:i (?:want|need) to|how (?:do|can) i|can i) )?"
    r"(?:supply|stock|provision) (?:the )?orchard(?: path)? "
    r"(?:with|using) (?:the )?(?:brass )?lantern"
    r"(?: (?:by|via|with|using) (?P<method>.+))?$"
)
_STATUS = frozenset({
    "check orchard supply", "check orchard lantern supply",
    "check orchard path supply", "inspect orchard lantern supply",
    "what supplies are at orchard", "what supplies are at the orchard",
})
_METHOD = {
    "carrying": "carry", "carrying it": "carry",
    "carrying the lantern": "carry", "walking with it": "carry",
    "walking with lantern": "carry", "taking it myself": "carry",
    "throwing": "throw", "throwing it": "throw",
    "throwing the lantern": "throw", "tossing it": "throw",
    "asking groundskeeper": "actor_throw",
    "asking the groundskeeper": "actor_throw",
    "asking groundskeeper to throw": "actor_throw",
    "asking the groundskeeper to throw it": "actor_throw",
    "having groundskeeper throw it": "actor_throw",
    "pushing the loaded chest": "chest_push",
    "pushing loaded chest": "chest_push",
    "pushing the chest": "chest_push",
    "pushing chest": "chest_push",
    "opening the chest": "open_chest",
    "opening chest": "open_chest",
    "taking the lantern from the chest": "retrieve",
    "retrieving lantern from chest": "retrieve",
    "taking it from chest": "retrieve",
    "dropping the lantern": "drop",
    "setting lantern down": "drop",
    "putting lantern down": "drop",
}


def parse_orchard_supply_attempt(raw: str) -> OrchardSupplyAttempt | None:
    normalized = " ".join(raw.casefold().strip().split()).rstrip(".!?")
    if normalized in _STATUS:
        return OrchardSupplyAttempt(raw_text=raw, method=None, is_status=True)
    match = _GOAL.fullmatch(normalized)
    if match is None:
        return None
    method = match.group("method")
    return OrchardSupplyAttempt(
        raw_text=raw,
        method=(_METHOD.get(method, "unqualified") if method else None),
    )


def _located(app: MyravantVSM14Application, obj: str, place: str) -> bool:
    return any(
        rel.relation_type == LOCATED_AT_RELATION_TYPE
        and rel.subject_entity_id == obj and rel.object_entity_id == place
        for rel in app.state.representation.relations
    )


def _carried(app: MyravantVSM14Application, obj: str, actor: str) -> bool:
    return any(
        rel.relation_type == CARRIED_BY_RELATION_TYPE
        and rel.subject_entity_id == obj and rel.object_entity_id == actor
        for rel in app.state.representation.relations
    )


def execute_orchard_supply_attempt(
    app: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    attempt = parse_orchard_supply_attempt(raw)
    if attempt is None:
        raise ValueError("not an Orchard supply attempt")
    pre = app.authoritative_digest()

    def refusal(reason: str, msg: str) -> PlayApplicationResult:
        return PlayApplicationResult(
            result_type="orchard_supply_unavailable",
            message=msg, authoritative_changed=False,
            pre_state_digest=pre, post_state_digest=pre,
            failure_class=reason,
        )

    def report(msg: str) -> PlayApplicationResult:
        return PlayApplicationResult(
            result_type="orchard_supply_observed",
            message=msg, authoritative_changed=False,
            pre_state_digest=pre, post_state_digest=pre,
        )

    here = app.current_place_id()
    held = _carried(app, LANTERN_ID, app.fixture.player_entity_id)
    chest_here = _located(app, TOOL_CHEST_ID, here)

    # A report is not a global campaign-omniscient achievement test.
    # Closed-container contents and remote physical placement are not
    # automatically known to the player.
    if attempt.is_status or attempt.method is None:
        if here == ORCHARD_PATH_ID:
            if held:
                return report(
                    "You have brought the Lantern to Orchard Path and still "
                    "carry it. You may set it down here."
                )
            if _located(app, LANTERN_ID, here) and (
                app._object_currently_observable(LANTERN_ID)
            ):
                return report(
                    "The Lantern is visibly present at Orchard Path. "
                    "You can inspect, take or use it under existing rules."
                )
            if chest_here and app._object_currently_observable(TOOL_CHEST_ID):
                chest = app.object_open_state(TOOL_CHEST_ID)
                if chest is not None and chest.state == "closed":
                    return report(
                        "A closed Tool Chest is here. Its contents are not "
                        "established by this observation. You can open it "
                        "and inspect or retrieve accessible contents."
                    )
                return report(
                    "An open Tool Chest is here. Inspect its visible "
                    "contents before attempting to retrieve the Lantern."
                )
            return report(
                "No presently observable Lantern supply is established "
                "here. Concealed objects are not ruled out."
            )
        if here == YARD_ID:
            blockade = _located(app, WAYSTONE_ID, YARD_ID)
            parts = [
                "From the Yard you may supply Orchard Path by carrying "
                "the Lantern east if you hold it; throwing it east if "
                "you hold it; asking the Groundskeeper to throw it "
                "if present and carrying it; or pushing a closed, "
                "Lantern-loaded Tool Chest east."
            ]
            if held:
                parts.append("You currently carry the Lantern.")
            if _located(app, LANTERN_ID, YARD_ID) and (
                app._object_currently_observable(LANTERN_ID)
            ):
                parts.append(
                    "The Lantern is on the ground here; taking it is "
                    "a separate, qualified action."
                )
            if chest_here and app._object_currently_observable(TOOL_CHEST_ID):
                state = app.object_open_state(TOOL_CHEST_ID)
                if state is not None:
                    parts.append(f"The local Tool Chest is {state.state}.")
            if blockade and app._object_currently_observable(WAYSTONE_ID):
                parts.append(
                    "The local Waystone obstructs the east passage. "
                    "Clearing it is a separate physical task; throwing "
                    "an object does not imply the player can walk east."
                )
            return report(" ".join(parts))
        return report(
            "You can assess that Orchard supply objective from the Yard "
            "or by locally inspecting what reached Orchard Path. "
            "This request does not reveal remote inventory."
        )

    if attempt.method == "unqualified":
        return refusal(
            "orchard_supply_method_unqualified",
            "That proposed supply method is not qualified. "
            "You may still attempt another coherent method.",
        )

    if attempt.method in {"carry", "throw", "chest_push", "actor_throw"}:
        if here != YARD_ID:
            return refusal(
                "orchard_supply_start_not_local",
                "This selected delivery method requires you at the Yard; "
                "it cannot act remotely.",
            )
        if attempt.method == "carry":
            if not held:
                return refusal(
                    "orchard_supply_player_control_unavailable",
                    "You must lawfully carry the Lantern before walking "
                    "it to Orchard Path.",
                )
            return app.move("east")
        if attempt.method == "throw":
            return app.displace_object("lantern", "east", method="throw")
        if attempt.method == "actor_throw":
            return execute_vsm13_request(
                app, "ask groundskeeper to throw lantern east",
            ).result
        # A container move is licensed only when the specified cargo
        # really exists in it; never fabricate cargo by calling push.
        if not chest_here or not (
            (contained := containment_relation_for(app.storage_state, LANTERN_ID))
            is not None and contained.object_entity_id == TOOL_CHEST_ID
        ):
            return refusal(
                "orchard_supply_loaded_container_unavailable",
                "This loaded-container delivery is not qualified from "
                "the current local arrangement.",
            )
        return app.displace_object("chest", "east", method="push")

    if here != ORCHARD_PATH_ID:
        return refusal(
            "orchard_supply_unload_not_local",
            "Unpacking or leaving a delivered Lantern requires your "
            "presence at Orchard Path.",
        )

    if attempt.method == "drop":
        return app.drop("lantern")

    if not chest_here:
        return refusal(
            "orchard_supply_container_not_local",
            "No local Tool Chest is available for this unloading action.",
        )
    if attempt.method == "open_chest":
        return app.open_object("chest")
    if attempt.method == "retrieve":
        # The storage owner distinguishes opened access from possession
        # and refuses without reconstructing arbitrary hidden contents.
        return app.retrieve_object("lantern", "chest")

    raise AssertionError("unexpected Orchard supply method")
