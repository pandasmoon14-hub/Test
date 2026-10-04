"""Playable terminal lane for VSM-11 bounded actor-mediated custody.

VSM-11 gets first refusal only for its exact Groundskeeper pickup/drop request
grammar. Every other input delegates to the complete VSM-10 terminal lane, which
preserves VSM-9 and the existing Myravant terminal routes. This is bounded
vertical-slice evidence, not a generic NPC-command registry.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.myravant_play_application import (
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_vsm9_actor_mediated_object_state import VSM9RequestReceipt
from astra_runtime.myravant_vsm10_actor_mediated_movement import VSM10RequestReceipt
from astra_runtime.myravant_vsm10_terminal import execute_vsm10_terminal_input
from astra_runtime.myravant_vsm11_actor_mediated_custody import (
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
    prior_request_receipt: VSM10RequestReceipt | VSM9RequestReceipt | None = None


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
            route="vsm11_actor_mediated_custody",
            result=execution.result,
            request_receipt=execution.request_receipt,
        )

    prior = execute_vsm10_terminal_input(application, raw_text)
    return VSM11TerminalInteraction(
        raw_text=raw_text,
        route=prior.route,
        result=prior.result,
        prior_request_receipt=(
            prior.request_receipt
            if prior.request_receipt is not None
            else prior.prior_request_receipt
        ),
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
        stripped = raw.strip()
        if stripped.casefold() in {"exit", "quit"}:
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
