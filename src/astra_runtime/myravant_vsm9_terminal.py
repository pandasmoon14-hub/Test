"""Playable terminal lane for the bounded VSM-9 actor-mediated capability.

This adapter extends, rather than replaces, the existing Myravant terminal grammar.
VSM-9 gets first refusal only for its exact bounded Groundskeeper + Brass Lantern
request grammar. Every other input is parsed by the existing terminal parser and
routed to the same existing application methods.

The module is deliberately temporary/bounded evidence for the complete VSM-9
vertical path. It does not create a generic plugin command registry or a second
command authority layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.myravant_play_application import (
    CheckpointPathRequiredError,
    MyravantPlayApplication,
    PlayApplicationResult,
)
from astra_runtime.myravant_terminal import (
    _split_handoff_argument,
    _split_request_handoff_argument,
    _split_storage_argument,
    _split_throw_argument,
    parse_terminal_command,
)
from astra_runtime.myravant_vsm9_actor_mediated_object_state import (
    VSM9RequestReceipt,
    execute_vsm9_request,
    parse_vsm9_request,
)


@dataclass(frozen=True, kw_only=True)
class VSM9TerminalInteraction:
    raw_text: str
    route: str
    result: PlayApplicationResult
    request_receipt: VSM9RequestReceipt | None = None


def _nonmutating_result(
    application: MyravantPlayApplication,
    *,
    result_type: str,
    message: str,
    failure_class: str,
) -> PlayApplicationResult:
    digest = application.authoritative_digest()
    return PlayApplicationResult(
        result_type=result_type,
        message=message,
        authoritative_changed=False,
        pre_state_digest=digest,
        post_state_digest=digest,
        failure_class=failure_class,
    )


def execute_vsm9_terminal_input(
    application: MyravantPlayApplication,
    raw_text: str,
) -> VSM9TerminalInteraction:
    """Route one raw player input through VSM-9 or the unchanged legacy grammar."""

    vsm9 = parse_vsm9_request(raw_text)
    if vsm9.parsed:
        execution = execute_vsm9_request(application, raw_text)
        return VSM9TerminalInteraction(
            raw_text=raw_text,
            route="vsm9_actor_mediated",
            result=execution.result,
            request_receipt=execution.request_receipt,
        )

    parsed = parse_terminal_command(raw_text)
    argument = parsed.argument or ""

    if parsed.action == "look":
        result = application.look()
    elif parsed.action == "look_direction":
        result = application.look_direction(argument)
    elif parsed.action == "inspect":
        result = application.inspect(argument)
    elif parsed.action == "move":
        result = application.move(argument)
    elif parsed.action == "pickup":
        result = application.pickup(argument)
    elif parsed.action == "drop":
        result = application.drop(argument)
    elif parsed.action == "light":
        result = application.light_object(argument)
    elif parsed.action == "extinguish":
        result = application.extinguish_object(argument)
    elif parsed.action == "open":
        result = application.open_object(argument)
    elif parsed.action == "close":
        result = application.close_object(argument)
    elif parsed.action == "wait":
        result = application.wait()
    elif parsed.action == "throw":
        try:
            object_reference, direction = _split_throw_argument(argument)
        except ValueError:
            result = _nonmutating_result(
                application,
                result_type="object_displacement_rejected",
                message="That throw could not be routed.",
                failure_class="object_displacement_route_unavailable",
            )
        else:
            result = application.throw_object(object_reference, direction)
    elif parsed.action == "handoff":
        try:
            object_reference, recipient_reference = _split_handoff_argument(argument)
        except ValueError:
            result = _nonmutating_result(
                application,
                result_type="actor_object_handoff_rejected",
                message="That handoff could not be routed.",
                failure_class="actor_object_handoff_route_unavailable",
            )
        else:
            result = application.give_object(object_reference, recipient_reference)
    elif parsed.action == "request_handoff":
        try:
            source_reference, object_reference = _split_request_handoff_argument(argument)
        except ValueError:
            result = _nonmutating_result(
                application,
                result_type="actor_object_handoff_rejected",
                message="That return request could not be routed.",
                failure_class="actor_object_handoff_route_unavailable",
            )
        else:
            result = application.request_object_from_actor(source_reference, object_reference)
    elif parsed.action in {"store", "retrieve"}:
        try:
            object_reference, container_reference = _split_storage_argument(argument)
        except ValueError:
            result = _nonmutating_result(
                application,
                result_type="storage_rejected",
                message="That storage attempt could not be routed.",
                failure_class="storage_target_unavailable",
            )
        else:
            if parsed.action == "store":
                result = application.store_object(object_reference, container_reference)
            else:
                result = application.retrieve_object(object_reference, container_reference)
    elif parsed.action == "request_object_state":
        # Existing VSM-8 request grammar remains owned by the existing terminal
        # application route. Keep its exact argument contract intact here.
        parts = argument.split(" -> ", 2)
        if len(parts) != 3 or not all(parts):
            result = _nonmutating_result(
                application,
                result_type="object_state_request_rejected",
                message="That request could not be routed.",
                failure_class="object_state_request_route_unavailable",
            )
        else:
            result = application.request_object_state_from_actor(
                parts[0], parts[1], parts[2]
            )
    elif parsed.action == "save":
        try:
            result = application.save()
        except CheckpointPathRequiredError as exc:
            result = _nonmutating_result(
                application,
                result_type="checkpoint_unavailable",
                message=f"Save unavailable: {exc}",
                failure_class="checkpoint_path_required",
            )
    elif parsed.action == "empty":
        result = _nonmutating_result(
            application,
            result_type="empty_input",
            message="",
            failure_class="empty_input",
        )
    elif parsed.action == "ambiguous":
        result = _nonmutating_result(
            application,
            result_type="ambiguous_input",
            message=(
                "That attempt needs a clearer target before it can be routed. "
                "No authoritative state changed."
            ),
            failure_class=parsed.failure_class or "ambiguous_target_reference",
        )
    elif parsed.action == "uninterpretable":
        result = _nonmutating_result(
            application,
            result_type="uninterpretable_input",
            message=(
                "That input could not be interpreted as a gameplay attempt. "
                "No authoritative state changed."
            ),
            failure_class=parsed.failure_class or "uninterpretable_input",
        )
    else:
        result = _nonmutating_result(
            application,
            result_type="unsupported_input",
            message=(
                "That attempt does not currently have an executable route. "
                "No authoritative state changed."
            ),
            failure_class=(
                parsed.failure_class or "unsupported_input_no_executable_route"
            ),
        )

    return VSM9TerminalInteraction(
        raw_text=raw_text,
        route="existing_terminal",
        result=result,
    )


def run_vsm9_terminal(
    application: MyravantPlayApplication,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
) -> tuple[VSM9TerminalInteraction, ...]:
    """Run a bounded playable VSM-9 session and return its evaluation trace."""

    interactions: list[VSM9TerminalInteraction] = []
    output_stream.write("Myravant — VSM-9\n")
    while True:
        raw = input_stream.readline()
        if raw == "":
            break
        stripped = raw.strip()
        if stripped.casefold() in {"exit", "quit"}:
            break
        interaction = execute_vsm9_terminal_input(application, raw)
        interactions.append(interaction)
        if interaction.result.message:
            output_stream.write(interaction.result.message + "\n")
    return tuple(interactions)


def new_vsm9_terminal_application(
    *, checkpoint_path: str | Path | None = None,
) -> MyravantPlayApplication:
    return MyravantPlayApplication.new(checkpoint_path=checkpoint_path)
