"""Cooperative local delivery goal over existing actor-mediated physical owners.

This interpreter proposes one bounded fixture-local goal; it does not own
Groundskeeper knowledge, planning, willingness, custody, displacement, RNG,
rules, or a future Myravant-native economy. The current target's *local*
placement chooses an already-qualified owner action, never a generic AI
permission to move anything.
"""

from __future__ import annotations

import re

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_actor_ground_assistance import (
    execute_ground_contact_request,
)
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    ORCHARD_PATH_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm13_actor_mediated_displacement import (
    execute_vsm13_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


# Common goal language, not a list of alternative execution verbs.
# Only this noncanonical Lantern->Orchard situation is presently qualified.
_DELIVERY_GOAL = re.compile(
    r"^(?:i\s+)?(?:ask|request)\s+(?:the\s+)?groundskeeper\s+to\s+"
    r"(?:bring|take|move|get)\s+(?:the\s+)?(?:brass\s+)?lantern\s+"
    r"to\s+(?:the\s+)?(?:orchard|orchard\s+path)\s*[.!?]*$",
    re.IGNORECASE,
)

# These are intent-class examples; they do NOT establish that the named
# institution, its authority, or any requested charter exists in-world.
_INSTITUTIONAL_PETITION = re.compile(
    r"^(?:i\s+)?(?:ask|petition)\s+(?:the\s+)?"
    r"(?:[\w-]+\s+)*(?:council|assembly|magistrate|office|guild)"
    r"\s+for\s+(?:a\s+|an\s+|the\s+)?"
    r"(?:charter|permission|permit|authorization|recognition)"
    r"\s*[.!?]*$",
    re.IGNORECASE,
)


def parse_cooperative_delivery_goal(raw_text: str) -> bool:
    return _DELIVERY_GOAL.fullmatch(" ".join(raw_text.split())) is not None


def parse_institutional_petition(raw_text: str) -> bool:
    return _INSTITUTIONAL_PETITION.fullmatch(" ".join(raw_text.split())) is not None


def _refuse(
    app: MyravantVSM14Application,
    *,
    failure_class: str,
    message: str,
    result_type: str = "cooperative_delivery_rejected",
) -> PlayApplicationResult:
    before = app.authoritative_digest()
    return PlayApplicationResult(
        result_type=result_type,
        message=message,
        authoritative_changed=False,
        pre_state_digest=before,
        post_state_digest=before,
        failure_class=failure_class,
    )


def execute_institutional_petition(
    app: MyravantVSM14Application, raw_text: str,
) -> PlayApplicationResult:
    if not parse_institutional_petition(raw_text):
        raise ValueError("not a recognized institutional petition intent")
    return _refuse(
        app,
        failure_class="institutional_petition_unqualified",
        result_type="institutional_petition_unavailable",
        message=(
            "That petition is understood, but no qualified institutional "
            "recipient or petition procedure is available here."
        ),
    )


def execute_cooperative_delivery_goal(
    app: MyravantVSM14Application, raw_text: str,
) -> PlayApplicationResult:
    """Choose one actor-owned lawful *method* for the same declared local goal.

    Grounded Lantern in Yard -> existing Groundskeeper push east.
    Groundskeeper holding Lantern in Yard -> existing Groundskeeper throw east.
    Any other placement/control/locality -> nonmutating refusal.

    This does not auto-move actors, teleport resources, make promises,
    smuggle remote locations into dialogue, or let an adapter commit state.
    """
    if not parse_cooperative_delivery_goal(raw_text):
        raise ValueError("not a qualified cooperative delivery goal")

    if (
        app.current_place_id() != YARD_ID
        or app.entity_place_id(GROUNDSKEEPER_ID) != YARD_ID
    ):
        return _refuse(
            app,
            failure_class="cooperative_goal_actor_not_local",
            message="The Groundskeeper cannot undertake that request from here.",
        )

    placement = [
        relation for relation in app.state.representation.relations
        if relation.subject_entity_id == LANTERN_ID
        and relation.relation_type in (
            LOCATED_AT_RELATION_TYPE, CARRIED_BY_RELATION_TYPE,
        )
    ]
    if len(placement) != 1:
        return _refuse(
            app,
            failure_class="cooperative_goal_opportunity_unavailable",
            message="There is no qualified local way to complete that request.",
        )

    relation = placement[0]
    if (
        relation.relation_type == LOCATED_AT_RELATION_TYPE
        and relation.object_entity_id == YARD_ID
    ):
        # Existing actor request supplies acceptance and COMP-3 evidence.
        outcome = execute_ground_contact_request(
            app, "ask groundskeeper to push lantern east",
        )
        return outcome.result

    if (
        relation.relation_type == CARRIED_BY_RELATION_TYPE
        and relation.object_entity_id == GROUNDSKEEPER_ID
    ):
        # Existing VSM-13 actor custody qualification/commit controls throw.
        outcome = execute_vsm13_request(
            app, "ask groundskeeper to throw lantern east",
        )
        return outcome.result

    return _refuse(
        app,
        failure_class="cooperative_goal_opportunity_unavailable",
        message="There is no qualified local way to complete that request.",
    )
