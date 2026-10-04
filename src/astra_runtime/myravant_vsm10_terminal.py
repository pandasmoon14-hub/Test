"""Playable terminal lane for VSM-10 bounded actor-mediated local movement.

VSM-10 gets first refusal only for its exact Groundskeeper movement-request
grammar. Every other input delegates to the complete VSM-9 terminal lane, which
in turn preserves the existing Myravant terminal routes. The Orchard Path repair
then derives one bounded nonauthoritative directional light signal from existing
COMP-3 placement and INT-2 lit state. This remains vertical-slice evidence rather
than a generic command-plugin or sensing system.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.myravant_orchard_path_signal import (
    derive_displaced_lantern_directional_signal,
)
from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_vsm9_actor_mediated_object_state import VSM9RequestReceipt
from astra_runtime.myravant_vsm9_terminal import execute_vsm9_terminal_input
from astra_runtime.myravant_vsm10_actor_mediated_movement import (
    VSM10RequestReceipt,
    execute_vsm10_request,
    parse_vsm10_request,
)


@dataclass(frozen=True, kw_only=True)
class VSM10TerminalInteraction:
    raw_text: str
    route: str
    result: PlayApplicationResult
    request_receipt: VSM10RequestReceipt | None = None
    prior_request_receipt: VSM9RequestReceipt | None = None


def execute_vsm10_terminal_input(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM10TerminalInteraction:
    """Route one input through VSM-10 first, then the complete prior terminal."""

    parsed = parse_vsm10_request(raw_text)
    if parsed.parsed:
        execution = execute_vsm10_request(application, raw_text)
        return VSM10TerminalInteraction(
            raw_text=raw_text,
            route="vsm10_actor_mediated_movement",
            result=execution.result,
            request_receipt=execution.request_receipt,
        )

    prior = execute_vsm9_terminal_input(application, raw_text)
    existing = parse_terminal_command(raw_text)
    if existing.action == "look_direction" and existing.argument is not None:
        repaired = derive_displaced_lantern_directional_signal(
            application,
            direction=existing.argument,
            prior_result=prior.result,
        )
        if repaired is not None:
            return VSM10TerminalInteraction(
                raw_text=raw_text,
                route="orchard_path_directional_light_signal",
                result=repaired,
            )

    return VSM10TerminalInteraction(
        raw_text=raw_text,
        route=prior.route,
        result=prior.result,
        prior_request_receipt=prior.request_receipt,
    )


def run_vsm10_terminal(
    application: MyravantPlayApplication,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
) -> tuple[VSM10TerminalInteraction, ...]:
    """Run a bounded playable VSM-10 session and return its evaluation trace."""

    interactions: list[VSM10TerminalInteraction] = []
    output_stream.write("Myravant — VSM-10\n")
    while True:
        raw = input_stream.readline()
        if raw == "":
            break
        stripped = raw.strip()
        if stripped.casefold() in {"exit", "quit"}:
            break
        interaction = execute_vsm10_terminal_input(application, raw)
        interactions.append(interaction)
        if interaction.result.message:
            output_stream.write(interaction.result.message + "\n")
    return tuple(interactions)


def new_vsm10_terminal_application(
    *, checkpoint_path: str | Path | None = None,
) -> MyravantPlayApplication:
    return MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
