"""Expose the existing VSM-9..14 request capabilities in the installed client.

Only precisely parsed, fixture-bounded requests receive newer-lane first
refusal. Other attempts remain owned by the original terminal command router.
This module has no world authority, command registry, or new game mechanics.
"""

from __future__ import annotations

from astra_runtime.myravant_play_application import PlayApplicationResult
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

    if not any(
        parse(raw_text).parsed
        for parse in (
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
