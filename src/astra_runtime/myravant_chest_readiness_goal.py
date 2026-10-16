"""Goal-led Tool Chest restoration and transport, using existing owners only.

A player can choose how to perform latch work, repair the conserved brace,
secure the finished latch personally or commission the Groundskeeper, and
physically move the real Chest. Each request does at most one explicitly
chosen action; the interpreter owns no tasks, outcomes, physics, or secrets.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, ORCHARD_PATH_ID, TOOL_CHEST_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@dataclass(frozen=True, kw_only=True)
class ChestReadinessGoal:
    raw_text: str
    method: str | None


_GOAL = re.compile(
    r"^(?:(?:i (?:want|need) to|how (?:do|can) i|can i) )?"
    r"(?:prepare|ready|restore|finish|make ready|secure) "
    r"(?:the )?(?:tool )?chest "
    r"(?:for|to) (?:orchard(?: path)?|transport|delivery|journey|shipment|ship)"
    r"(?: (?:by|using|with|via) (?P<method>.+))?$"
)
_METHODS = {
    "manual service": "manual",
    "working on the latch manually": "manual",
    "working on latch myself": "manual",
    "servicing the latch by hand": "manual",
    "servicing it myself": "manual",
    "repairing the latch manually": "manual",
    "lantern service": "lantern",
    "servicing latch with lantern": "lantern",
    "repairing latch with lantern": "lantern",
    "using a lit lantern for latch work": "lantern",
    "asking groundskeeper to service the latch": "npc_service",
    "asking groundskeeper to work with lantern": "npc_service",
    "having groundskeeper service with lantern": "npc_service",
    "asking the groundskeeper to repair with lantern": "npc_service",
    "refitting the brace": "refit",
    "reattaching the brace": "refit",
    "reinstalling the brace": "refit",
    "closing the lid": "close",
    "closing chest": "close",
    "securing the latch myself": "secure",
    "securing it myself": "secure",
    "securing the chest": "secure",
    "asking groundskeeper to secure later": "request_duty",
    "asking the groundskeeper to secure it later": "request_duty",
    "delegating later securing to groundskeeper": "request_duty",
    "cancelling groundskeeper duty": "cancel_duty",
    "withdrawing the groundskeeper agreement": "cancel_duty",
    "waiting for groundskeeper to finish": "wait_duty",
    "waiting for the groundskeeper to finish": "wait_duty",
    "pushing it to orchard": "transport",
    "pushing the chest east": "transport",
    "pushing chest to orchard": "transport",
    "pushing it east": "transport",
}


def parse_chest_readiness_goal(raw: str) -> ChestReadinessGoal | None:
    normalized = " ".join(raw.strip().casefold().split()).rstrip(".!?")
    match = _GOAL.fullmatch(normalized)
    if match is None:
        return None
    raw_method = match.group("method")
    # Do not silently ignore a second action after an authorized first
    # transition. The durable terminal acknowledgement is per action.
    if raw_method is not None and re.search(r"\b(?:and|then)\b", raw_method):
        return None
    return ChestReadinessGoal(
        raw_text=raw,
        method=(
            _METHODS.get(raw_method, "unqualified")
            if raw_method is not None else None
        ),
    )


def _grounded_here(app: MyravantVSM14Application, target: str, here: str) -> bool:
    return any(
        rel.relation_type == LOCATED_AT_RELATION_TYPE
        and rel.subject_entity_id == target
        and rel.object_entity_id == here
        for rel in app.state.representation.relations
    )


def execute_chest_readiness_goal(
    app: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    goal = parse_chest_readiness_goal(raw)
    if goal is None:
        raise ValueError("not a qualified Tool Chest readiness goal")
    digest = app.authoritative_digest()

    def refused(reason: str, message: str) -> PlayApplicationResult:
        return PlayApplicationResult(
            result_type="chest_readiness_unavailable",
            message=message, authoritative_changed=False,
            pre_state_digest=digest, post_state_digest=digest,
            failure_class=reason,
        )

    here = app.current_place_id()
    if here != YARD_ID:
        return refused(
            "chest_readiness_worksite_not_local",
            "This repair and dispatch work requires your presence at "
            "the Yard; this attempt does not inspect a remote Chest.",
        )
    if not _grounded_here(app, TOOL_CHEST_ID, here):
        return refused(
            "chest_readiness_chest_not_local",
            "No grounded Tool Chest is established at this worksite.",
        )
    # Yard is a sufficient-light fixture. Do not turn the goal status
    # into a remote item/location oracle or intrinsic material law.
    if not app._object_currently_observable(TOOL_CHEST_ID):
        return refused(
            "chest_readiness_visual_opportunity_unavailable",
            "The Chest cannot currently be observed for this work goal.",
        )

    if goal.method is None:
        progress = app.service_state.progress
        brace = app.brace_state.condition
        chest = app.object_open_state(TOOL_CHEST_ID)
        closed = chest is not None and chest.state == "closed"
        secured = app.service_state.secured
        duty = app.duty_state.status
        parts = [
            f"The local Tool Chest latch has {progress}/2 work "
            f"contributions; the conserved brace is {brace.replace('_', ' ')}; "
            f"the Chest is {chest.state if chest else 'not qualified'}; "
            f"the latch is {'secured' if secured else 'not secured'}."
        ]
        if progress < 2:
            parts.append(
                "You may contribute manual latch work (two contributions "
                "in total), use a placed lit Lantern for one-step player "
                "service, or request a co-present Groundskeeper to service "
                "with a physically supplied lit Lantern."
            )
        if brace != "attached":
            parts.append(
                "The structural brace must be refitted before securing."
            )
        if not closed:
            parts.append("Close the Chest before securing.")
        if (
            progress == 2 and brace == "attached" and closed
            and not secured and duty != "pending"
        ):
            parts.append(
                "You can secure the latch yourself, or ask a co-present "
                "Groundskeeper to secure it later, when willing."
            )
        if duty == "pending":
            parts.append(
                "A local securing agreement is pending; a separate WORLD-2 "
                "wait may allow lawful completion, or you can request "
                "cancellation while the actor is present."
            )
        elif duty == "fulfilled":
            parts.append("The Groundskeeper's earlier duty is fulfilled.")
        if secured:
            parts.append(
                "The secured Chest remains physically movable only along "
                "qualified routes; securing does not move it."
            )
        if _grounded_here(app, LANTERN_ID, here):
            parts.append(
                "A Lantern is grounded at this worksite; the owner must "
                "still qualify its lit condition for assisted work."
            )
        if app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID:
            parts.append("The Groundskeeper is presently at this worksite.")
        parts.append(
            "Pushing the Chest to Orchard is a separate qualified "
            "physical choice. Moving it away before completing local "
            "work or an accepted Yard duty may remove the opportunity "
            "to finish those actions. Nothing is repaired, secured, "
            "loaded or delivered by asking for these options."
        )
        return PlayApplicationResult(
            result_type="chest_readiness_methods_observed",
            message=" ".join(parts),
            authoritative_changed=False,
            pre_state_digest=digest, post_state_digest=digest,
        )

    if goal.method == "unqualified":
        return refused(
            "chest_readiness_method_unqualified",
            "That proposed method is not qualified for this local Chest goal.",
        )

    # Existing owners verify all prerequisites, actor willingness,
    # causal time and persisted receipts, without interpreter short cuts.
    dispatch = {
        "manual": lambda: app.service_chest_latch("work", method="manual"),
        "lantern": lambda: app.service_chest_latch("work", method="lantern"),
        "npc_service": lambda: app.request_groundskeeper_latch_work(
            method="lantern",
        ),
        "refit": lambda: app.alter_chest_brace("refit"),
        "close": lambda: app.close_object("chest"),
        "secure": lambda: app.service_chest_latch("secure"),
        "request_duty": lambda: app.groundskeeper_chest_duty("request"),
        "cancel_duty": lambda: app.groundskeeper_chest_duty("cancel"),
        "transport": lambda: app.displace_object(
            "chest", "east", method="push",
        ),
    }
    if goal.method == "wait_duty":
        if app.duty_state.status != "pending":
            return refused(
                "chest_readiness_no_pending_duty",
                "There is no accepted, pending local Chest duty to wait for.",
            )
        return app.wait()
    return dispatch[goal.method]()
