"""Expose the existing VSM-9..14 request capabilities in the installed client.

Only precisely parsed, fixture-bounded requests receive newer-lane first
refusal. Other attempts remain owned by the original terminal command router.
This module has no world authority, command registry, or new game mechanics.
"""

from __future__ import annotations

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_chest_investigation_goal import (
    parse_chest_investigation, execute_chest_investigation,
)
from astra_runtime.myravant_chest_readiness_goal import (
    parse_chest_readiness_goal, execute_chest_readiness_goal,
)
from astra_runtime.myravant_orchard_supply_goal import (
    parse_orchard_supply_attempt, execute_orchard_supply_attempt,
)
from astra_runtime.myravant_physical_placement_goal import (
    parse_physical_placement_goal, execute_physical_placement_goal,
)
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


# Static interpreter routes, not a world command registry or semantic owner.
BOUNDED_TERMINAL_ROUTES = frozenset({
    'chest_investigation_goal',
    'chest_readiness_goal',
    'orchard_supply_goal',
    'destination_goal_method',
    'physical_placement_goal',
    'player_sensory_attempt',
    'actor_service',
    'fixture_duty',
    'fixture_brace',
    'actor_situated_investigation',
    'waystone_clearance',
    'fixture_service',
    'bounded_work',
    'cooperative_delivery_goal',
    'institutional_petition',
    'situated_inquiry',
    'large3_actor_mediated_ground_contact',
    'vsm14_persistent_follow_intent',
    'vsm13_actor_mediated_displacement',
    'vsm12_actor_mediated_custody',
    'vsm11_actor_mediated_storage',
    'vsm10_actor_mediated_movement',
    'vsm9_actor_mediated',
})


def _classify_bounded_terminal_request(raw_text: str, *, fixture=None) -> str | None:
    """Pure grammar classification with the same precedence on every surface.

    No application state, opportunity grant, executor, or persistence is touched.
    Qualification remains in the original handlers at each actual execution.
    """
    if parse_chest_investigation(raw_text) is not None:
        return 'chest_investigation_goal'
    if parse_chest_readiness_goal(raw_text) is not None:
        return 'chest_readiness_goal'
    if parse_orchard_supply_attempt(raw_text) is not None:
        return 'orchard_supply_goal'
    if parse_lantern_destination_goal(raw_text) is not None:
        return 'destination_goal_method'
    if parse_physical_placement_goal(raw_text, fixture=fixture) is not None:
        return 'physical_placement_goal'
    if parse_player_sensory_attempt(raw_text) is not None:
        return 'player_sensory_attempt'
    if parse_e2_actor_service(raw_text) is not None:
        return 'actor_service'
    if parse_e1_latch_duty(raw_text) is not None:
        return 'fixture_duty'
    if parse_d1_brace(raw_text) is not None:
        return 'fixture_brace'
    if parse_actor_memory_request(raw_text) is not None:
        return 'actor_situated_investigation'
    if parse_waystone_clearance(raw_text) is not None:
        return 'waystone_clearance'
    if parse_b2a_service(raw_text) is not None:
        return 'fixture_service'
    if parse_bounded_work_goal(raw_text) is not None:
        return 'bounded_work'
    if parse_cooperative_delivery_goal(raw_text):
        return 'cooperative_delivery_goal'
    if parse_institutional_petition(raw_text):
        return 'institutional_petition'
    if parse_situated_inquiry(raw_text).parsed:
        return 'situated_inquiry'
    if parse_ground_contact_request(raw_text).parsed:
        return 'large3_actor_mediated_ground_contact'
    if parse_vsm14_follow_request(raw_text).parsed:
        return 'vsm14_persistent_follow_intent'
    if parse_vsm13_request(raw_text).parsed:
        return 'vsm13_actor_mediated_displacement'
    if parse_vsm12_request(raw_text).parsed:
        return 'vsm12_actor_mediated_custody'
    if parse_vsm11_request(raw_text).parsed:
        return 'vsm11_actor_mediated_storage'
    if parse_vsm10_request(raw_text).parsed:
        return 'vsm10_actor_mediated_movement'
    if parse_vsm9_request(raw_text).parsed:
        return 'vsm9_actor_mediated'
    return None


def classify_bounded_terminal_request(raw_text: str, *, fixture=None) -> str | None:
    route = _classify_bounded_terminal_request(raw_text, fixture=fixture)
    admitted = getattr(fixture, "specialist_routes", None)
    return route if admitted is None or route in admitted else None


def execute_classified_bounded_terminal_request(
    application: MyravantVSM14Application, raw_text: str, *, route: str,
) -> PlayApplicationResult:
    """Call the original handler; a planned grammar match grants no privilege."""
    if classify_bounded_terminal_request(raw_text, fixture=application.fixture) != route:
        raise ValueError("specialist route no longer matches its original grammar")
    if route == 'chest_investigation_goal':
        return execute_chest_investigation(application, raw_text)
    if route == 'chest_readiness_goal':
        return execute_chest_readiness_goal(application, raw_text)
    if route == 'orchard_supply_goal':
        return execute_orchard_supply_attempt(application, raw_text)
    if route == 'destination_goal_method':
        return execute_lantern_destination_goal(application, raw_text)
    if route == 'physical_placement_goal':
        return execute_physical_placement_goal(application, raw_text)
    if route == 'player_sensory_attempt':
        return execute_player_sensory_attempt(application, raw_text)
    if route == 'actor_service':
        return execute_e2_actor_service(application, raw_text)
    if route == 'fixture_duty':
        return execute_e1_latch_duty(application, raw_text)
    if route == 'fixture_brace':
        return execute_d1_brace(application, raw_text)
    if route == 'actor_situated_investigation':
        return execute_actor_memory_request(application, raw_text)
    if route == 'waystone_clearance':
        return execute_waystone_clearance(application, raw_text)
    if route == 'fixture_service':
        return execute_b2a_service(application, raw_text)
    if route == 'bounded_work':
        return execute_bounded_work_goal(application, raw_text)
    if route == 'cooperative_delivery_goal':
        return execute_cooperative_delivery_goal(application, raw_text)
    if route == 'institutional_petition':
        return execute_institutional_petition(application, raw_text)
    if route == 'situated_inquiry':
        return execute_situated_inquiry(application, raw_text)
    interaction = execute_vsm14_terminal_input(application, raw_text)
    if interaction.route != route:
        raise RuntimeError("A classified actor request unexpectedly changed route")
    return interaction.result


def execute_bounded_terminal_request(
    application: MyravantVSM14Application, raw_text: str,
) -> tuple[str, PlayApplicationResult] | None:
    """Standalone and sequenced requests share grammar and original execution."""
    route = classify_bounded_terminal_request(raw_text, fixture=application.fixture)
    if route is None:
        return None
    return route, execute_classified_bounded_terminal_request(
        application, raw_text, route=route,
    )
