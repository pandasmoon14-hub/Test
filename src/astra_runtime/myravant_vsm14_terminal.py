"""Playable terminal lane for VSM-14 bounded persistent follow intent.

VSM-14 gets first refusal only for its exact Groundskeeper follow / stop-following
grammar. All other input delegates to the complete VSM-13 terminal lane.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_terminal import _write_result
from astra_runtime.myravant_vsm13_terminal import (
    VSM13TerminalInteraction,
    execute_vsm13_terminal_input,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_follow_intent import (
    VSM14FollowRequestReceipt,
    execute_vsm14_follow_request,
    parse_vsm14_follow_request,
)


@dataclass(frozen=True, kw_only=True)
class VSM14TerminalInteraction:
    raw_text: str
    route: str
    result: PlayApplicationResult
    request_receipt: VSM14FollowRequestReceipt | None = None
    prior_interaction: VSM13TerminalInteraction | None = None


def execute_vsm14_terminal_input(
    application: MyravantVSM14Application,
    raw_text: str,
) -> VSM14TerminalInteraction:
    """Route one input through VSM-14 first, then the complete prior terminal."""

    parsed = parse_vsm14_follow_request(raw_text)
    if parsed.parsed:
        execution = execute_vsm14_follow_request(application, raw_text)
        return VSM14TerminalInteraction(
            raw_text=raw_text,
            route="vsm14_persistent_follow_intent",
            result=execution.result,
            request_receipt=execution.request_receipt,
        )

    prior = execute_vsm13_terminal_input(application, raw_text)
    return VSM14TerminalInteraction(
        raw_text=raw_text,
        route=prior.route,
        result=prior.result,
        prior_interaction=prior,
    )


def run_vsm14_terminal(
    application: MyravantVSM14Application,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
) -> tuple[VSM14TerminalInteraction, ...]:
    interactions: list[VSM14TerminalInteraction] = []
    output_stream.write("Myravant — VSM-14\n")
    while True:
        raw = input_stream.readline()
        if raw == "":
            break
        if raw.strip().casefold() in {"exit", "quit"}:
            break
        interaction = execute_vsm14_terminal_input(application, raw)
        interactions.append(interaction)
        _write_result(output_stream, interaction.result, debug=False)
    return tuple(interactions)


def new_vsm14_terminal_application(
    *, checkpoint_path: str | Path | None = None
) -> MyravantVSM14Application:
    return MyravantVSM14Application.new(checkpoint_path=checkpoint_path)
