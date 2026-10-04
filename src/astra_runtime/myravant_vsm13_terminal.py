"""Playable terminal lane for VSM-13 bounded actor-mediated displacement.

VSM-13 gets first refusal only for its exact Groundskeeper/Lantern/east throw
grammar. All other input delegates to the complete VSM-12 terminal lane.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_vsm12_terminal import (
    VSM12TerminalInteraction,
    execute_vsm12_terminal_input,
)
from astra_runtime.myravant_vsm13_actor_mediated_displacement import (
    VSM13RequestReceipt,
    execute_vsm13_request,
    parse_vsm13_request,
)


@dataclass(frozen=True, kw_only=True)
class VSM13TerminalInteraction:
    raw_text: str
    route: str
    result: PlayApplicationResult
    request_receipt: VSM13RequestReceipt | None = None
    prior_interaction: VSM12TerminalInteraction | None = None


def execute_vsm13_terminal_input(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM13TerminalInteraction:
    """Route one input through VSM-13 first, then the complete prior terminal."""

    parsed = parse_vsm13_request(raw_text)
    if parsed.parsed:
        execution = execute_vsm13_request(application, raw_text)
        return VSM13TerminalInteraction(
            raw_text=raw_text,
            route="vsm13_actor_mediated_displacement",
            result=execution.result,
            request_receipt=execution.request_receipt,
        )

    prior = execute_vsm12_terminal_input(application, raw_text)
    return VSM13TerminalInteraction(
        raw_text=raw_text,
        route=prior.route,
        result=prior.result,
        prior_interaction=prior,
    )


def run_vsm13_terminal(
    application: MyravantPlayApplication,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
) -> tuple[VSM13TerminalInteraction, ...]:
    interactions: list[VSM13TerminalInteraction] = []
    output_stream.write("Myravant — VSM-13\n")
    while True:
        raw = input_stream.readline()
        if raw == "":
            break
        if raw.strip().casefold() in {"exit", "quit"}:
            break
        interaction = execute_vsm13_terminal_input(application, raw)
        interactions.append(interaction)
        if interaction.result.message:
            output_stream.write(interaction.result.message + "\n")
    return tuple(interactions)


def new_vsm13_terminal_application(
    *, checkpoint_path: str | Path | None = None,
) -> MyravantPlayApplication:
    return MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
