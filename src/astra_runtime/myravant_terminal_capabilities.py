"""Expose the existing VSM-9..14 request capabilities in the installed client.

Only precisely parsed, fixture-bounded requests receive newer-lane first
refusal. Other attempts remain owned by the original terminal command router.
This module has no world authority, command registry, or new game mechanics.
"""

from __future__ import annotations

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_goal_method_lantern import (
    parse_lantern_destination_goal, execute_lantern_destination_goal,
)
from astra_runtime.myravant_player_sensory_breadth import (
    parse_player_sensory_attempt, execute_player_sensory_attempt,
)
from astra_runtime.myravant_e2_actor_service_goal import (
    parse_e2_actor_service, execute_e2_actor_service,
)
from astra_runtime.myravant_e1_duty_goal import (
    parse_e1_latch_duty, execute_e1_latch_duty,
)
from astra_runtime.myravant_d1_brace_goal import (
    parse_d1_brace, execute_d1_brace,
)
from astra_runtime.myravant_c1_investigation_goal import (
    parse_actor_memory_request, execute_actor_memory_request,
)
from astra_runtime.myravant_b2b_waystone_clearance import (
    parse_waystone_clearance, execute_waystone_clearance,
)
from astra_runtime.myravant_b2a_service_goal import (
    parse_b2a_service, execute_b2a_service,
)
from astra_runtime.myravant_bounded_work_goals import (
    parse_bounded_work_goal, execute_bounded_work_goal,
)
from astra_runtime.myravant_cooperative_delivery_goal import (
    parse_cooperative_delivery_goal,
    execute_cooperative_delivery_goal,
    parse_institutional_petition,
    execute_institutional_petition,
)
from astra_runtime.myravant_situated_inquiry import (
    execute_situated_inquiry,
    parse_situated_inquiry,
)
from astra_runtime.myravant_actor_ground_assistance import (
    parse_ground_contact_request,
)
from astra_runtime.myravant_vsm9_actor_mediated_object_state import parse_vsm9_request
from astra_runtime.myravant_vsm10_actor_mediated_movement import parse_vsm10_request
from astra_runtime.myravant_vsm11_actor_mediated_storage import parse_vsm11_request
from astra_runtime.myravant_vsm12_actor_mediated_custody import parse_vsm12_request
from astra_runtime.myravant_vsm13_actor_mediated_displacement import parse_vsm13_request
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import parse_vsm14_follow_request
from astra_runtime.myravant_vsm14_terminal import execute_vsm14_terminal_input


def execute_bounded_terminal_request(
    application: MyravantVSM14Application,
    raw_text: str,
) -> tuple[str, PlayApplicationResult] | None:
    """Route bounded VSM requests; return None for every other attempt."""

    # A stated physical objective and chosen method are distinct. Execute
    # only through existing player COMP-3 or voluntary actor VSM-13 owners;
    # read-only method inquiry never commits a hidden planner outcome.
    if parse_lantern_destination_goal(raw_text) is not None:
        return (
            "destination_goal_method",
            execute_lantern_destination_goal(application, raw_text),
        )

    # Player sensory methods are distinguished from visual sighting and
    # from third-party actor investigation. No implicit remote reach.
    if parse_player_sensory_attempt(raw_text) is not None:
        return (
            "player_sensory_attempt",
            execute_player_sensory_attempt(application, raw_text),
        )

    # E2 permits actual co-present NPC work only with declared worksite resources.
    if parse_e2_actor_service(raw_text) is not None:
        return "actor_service", execute_e2_actor_service(application, raw_text)

    # A voluntary Yard-latch obligation is recognized only for the declared
    # Groundskeeper fixture; no general service-market parsing is assumed.
    if parse_e1_latch_duty(raw_text) is not None:
        return "fixture_duty", execute_e1_latch_duty(application, raw_text)

    # D-1's structural component exists only in the declared fixture profile.
    # Its executor owns no new world laws: RT-010 + WORLD-2 validate changes.
    if parse_d1_brace(raw_text) is not None:
        return "fixture_brace", execute_d1_brace(application, raw_text)

    # C-1 distinguishes direct actor sensing, unverified player testimony,
    # and historical recall. No current-world omniscience is claimed.
    if parse_actor_memory_request(raw_text) is not None:
        return (
            "actor_situated_investigation",
            execute_actor_memory_request(application, raw_text),
        )

    # B-2b is physical progress: Waystone placement creates/clears a real
    # exit obstruction through the existing COMP-3 and WORLD-2 owners.
    if parse_waystone_clearance(raw_text) is not None:
        return (
            "waystone_clearance",
            execute_waystone_clearance(application, raw_text),
        )

    # B-2a has its own RT-010/AFQR-16 state; B-1 goals remain mere
    # projections of physical location and object state.
    if parse_b2a_service(raw_text) is not None:
        return "fixture_service", execute_b2a_service(application, raw_text)

    # A small piece of real work may span multiple separately committed
    # player actions and saves. Owner state is the only work progress ledger.
    if parse_bounded_work_goal(raw_text) is not None:
        return "bounded_work", execute_bounded_work_goal(application, raw_text)

    # Recognize goal-shaped, actor-situated physical requests before the
    # narrow execution-verb grammars. All consequences remain in the original
    # actor mediators and COMP-3, not this interpretation surface.
    if parse_cooperative_delivery_goal(raw_text):
        return (
            "cooperative_delivery_goal",
            execute_cooperative_delivery_goal(application, raw_text),
        )

    # Distinguish a petition from a request to hand over a physical object.
    # No institution, entitlement or native legal mechanics are fabricated.
    if parse_institutional_petition(raw_text):
        return (
            "institutional_petition",
            execute_institutional_petition(application, raw_text),
        )

    # Qualify dialogue questions before the broad legacy "ask ..." grammar;
    # observations never own or commit NPC knowledge or object transfers.
    if parse_situated_inquiry(raw_text).parsed:
        return "situated_inquiry", execute_situated_inquiry(application, raw_text)

    if not any(
        parse(raw_text).parsed
        for parse in (
            parse_ground_contact_request,
            parse_vsm14_follow_request,
            parse_vsm13_request,
            parse_vsm12_request,
            parse_vsm11_request,
            parse_vsm10_request,
            parse_vsm9_request,
        )
    ):
        return None

    interaction = execute_vsm14_terminal_input(application, raw_text)
    if interaction.route == "existing_terminal":
        raise RuntimeError("A parsed VSM request unexpectedly lost its route")
    return interaction.route, interaction.result
