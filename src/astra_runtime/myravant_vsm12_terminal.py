"""Playable terminal lane for VSM-12 bounded actor-mediated custody.

VSM-12 gets first refusal only for its exact Groundskeeper pickup/drop grammar.
All other input delegates to the complete VSM-11 terminal lane, preserving the
actor-mediated storage capability and every earlier terminal route.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_vsm11_terminal import (
    VSM11TerminalInteraction,
    execute_vsm11_terminal_input,
)
from astra_runtime.myravant_vsm12_actor_mediated_custody import (
    VSM12RequestReceipt,
    execute_vsm12_request,
    parse_vsm12_request,
)


@dataclass(frozen=True, kw_only=True)
class VSM12TerminalInteraction:
    raw_text: str
    route: str
    result: PlayApplicationResult
    request_receipt: VSM12RequestReceipt | None = None
    prior_interaction: VSM11TerminalInteraction | None = None


def execute_vsm12_terminal_input(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM12TerminalInteraction:
    """Route one input through VSM-12 first, then the complete prior terminal."""

    parsed = parse_vsm12_request(raw_text)
    if parsed.parsed:
        execution = execute_vsm12_request(application, raw_text)
        return VSM12TerminalInteraction(
            raw_text=raw_text,
            route="vsm12_actor_mediated_custody",
            result=execution.result,
            request_receipt=execution.request_receipt,
        )

    prior = execute_vsm11_terminal_input(application, raw_text)
    return VSM12TerminalInteraction(
        raw_text=raw_text,
        route=prior.route,
        result=prior.result,
        prior_interaction=prior,
    )


def run_vsm12_terminal(
    application: MyravantPlayApplication,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
) -> tuple[VSM12TerminalInteraction, ...]:
    interactions: list[VSM12TerminalInteraction] = []
    output_stream.write("Myravant — VSM-12\n")
    while True:
        raw = input_stream.readline()
        if raw == "":
            break
        if raw.strip().casefold() in {"exit", "quit"}:
            break
        interaction = execute_vsm12_terminal_input(application, raw)
        interactions.append(interaction)
        if interaction.result.message:
            output_stream.write(interaction.result.message + "\n")
    return tuple(interactions)


def new_vsm12_terminal_application(
    *, checkpoint_path: str | Path | None = None,
) -> MyravantPlayApplication:
    return MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
