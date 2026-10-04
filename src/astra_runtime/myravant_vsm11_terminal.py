"""Playable terminal lane for VSM-11 bounded actor-mediated storage.

VSM-11 gets first refusal only for its exact Groundskeeper/Lantern/Tool-Chest
storage grammar. Every other input delegates to the complete VSM-10 terminal
lane. This is bounded vertical-slice evidence, not a generic command registry.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_vsm10_terminal import (
    VSM10TerminalInteraction,
    execute_vsm10_terminal_input,
)
from astra_runtime.myravant_vsm11_actor_mediated_storage import (
    VSM11RequestReceipt,
    execute_vsm11_request,
    parse_vsm11_request,
)


@dataclass(frozen=True, kw_only=True)
class VSM11TerminalInteraction:
    raw_text: str
    route: str
    result: PlayApplicationResult
    request_receipt: VSM11RequestReceipt | None = None
    prior_interaction: VSM10TerminalInteraction | None = None


def execute_vsm11_terminal_input(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM11TerminalInteraction:
    """Route one input through VSM-11 first, then the complete prior terminal."""

    parsed = parse_vsm11_request(raw_text)
    if parsed.parsed:
        execution = execute_vsm11_request(application, raw_text)
        return VSM11TerminalInteraction(
            raw_text=raw_text,
            route="vsm11_actor_mediated_storage",
            result=execution.result,
            request_receipt=execution.request_receipt,
        )

    prior = execute_vsm10_terminal_input(application, raw_text)
    return VSM11TerminalInteraction(
        raw_text=raw_text,
        route=prior.route,
        result=prior.result,
        prior_interaction=prior,
    )


def run_vsm11_terminal(
    application: MyravantPlayApplication,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
) -> tuple[VSM11TerminalInteraction, ...]:
    """Run a bounded playable VSM-11 session and return its evaluation trace."""

    interactions: list[VSM11TerminalInteraction] = []
    output_stream.write("Myravant — VSM-11\n")
    while True:
        raw = input_stream.readline()
        if raw == "":
            break
        if raw.strip().casefold() in {"exit", "quit"}:
            break
        interaction = execute_vsm11_terminal_input(application, raw)
        interactions.append(interaction)
        if interaction.result.message:
            output_stream.write(interaction.result.message + "\n")
    return tuple(interactions)


def new_vsm11_terminal_application(
    *, checkpoint_path: str | Path | None = None,
) -> MyravantPlayApplication:
    return MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
