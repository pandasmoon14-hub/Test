"""Human-playable terminal client for the bounded Myravant vertical slice."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointError,
)
from astra_runtime.myravant_live_play_evidence import (
    LivePlayEvidenceError,
    LivePlayEvidenceRecorder,
    build_live_play_session_header,
)
from astra_runtime.myravant_play_application import (
    CheckpointPathRequiredError,
    MyravantPlayApplication,
    PlayApplicationResult,
    PublicDirectionalObservationView,
    PublicInspectionView,
    PublicLocationView,
    PublicObservationFact,
)


@dataclass(frozen=True, kw_only=True)
class ParsedTerminalCommand:
    action: str
    argument: str | None = None
    raw_text: str = ""
    failure_class: str | None = None


_DEICTIC_TARGETS = frozenset({"it", "that", "this", "them", "these", "those"})
_TARGET_ARTICLES = frozenset({"a", "an", "the"})
_DIRECTION_ALIASES = {
    "north": "north",
    "northern": "north",
    "south": "south",
    "southern": "south",
    "east": "east",
    "eastern": "east",
    "west": "west",
    "western": "west",
}
_COMPOUND_ACTION_STARTERS = frozenset({
    "look",
    "inspect",
    "examine",
    "move",
    "go",
    "walk",
    "head",
    "pickup",
    "pick",
    "take",
    "grab",
    "drop",
    "give",
    "hand",
    "put",
    "place",
    "store",
    "remove",
    "retrieve",
    "open",
    "close",
    "shut",
    "save",
    "light",
    "ignite",
    "extinguish",
    "activate",
    "break",
    "smash",
    "destroy",
    "throw",
    "toss",
    "hurl",
    "ask",
    "wait",
})
_UNSUPPORTED_CAPABILITY_BY_VERB = {
    "activate": "unsupported_capability_object_activation",
    "break": "unsupported_capability_object_destruction",
    "smash": "unsupported_capability_object_destruction",
    "destroy": "unsupported_capability_object_destruction",
    "throw": "unsupported_capability_throwing",
    "toss": "unsupported_capability_throwing",
    "hurl": "unsupported_capability_throwing",
}


def _normalized_target(tokens: list[str]) -> str:
    normalized = [token.casefold() for token in tokens]
    if normalized and normalized[0] in _TARGET_ARTICLES:
        normalized = normalized[1:]
    return " ".join(normalized).strip()


def _object_action(*, action: str, target_tokens: list[str], raw_text: str) -> ParsedTerminalCommand:
    target = _normalized_target(target_tokens)
    if not target or target in _DEICTIC_TARGETS:
        return ParsedTerminalCommand(
            action="ambiguous",
            argument=target or None,
            raw_text=raw_text,
            failure_class="ambiguous_target_reference",
        )
    return ParsedTerminalCommand(action=action, argument=target, raw_text=raw_text)


def _storage_action(
    *,
    action: str,
    object_tokens: list[str],
    container_tokens: list[str],
    raw_text: str,
) -> ParsedTerminalCommand:
    object_target = _normalized_target(object_tokens)
    container_target = _normalized_target(container_tokens)
    if (
        not object_target
        or not container_target
        or object_target in _DEICTIC_TARGETS
        or container_target in _DEICTIC_TARGETS
    ):
        ambiguous = (
            object_target
            if object_target in _DEICTIC_TARGETS
            else container_target
            if container_target in _DEICTIC_TARGETS
            else None
        )
        return ParsedTerminalCommand(
            action="ambiguous",
            argument=ambiguous,
            raw_text=raw_text,
            failure_class="ambiguous_target_reference",
        )
    return ParsedTerminalCommand(
        action=action,
        argument=f"{object_target} -> {container_target}",
        raw_text=raw_text,
    )


def _split_storage_argument(argument: str) -> tuple[str, str]:
    parts = argument.split(" -> ", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("invalid bounded storage parser argument")
    return parts[0], parts[1]


def _split_throw_argument(argument: str) -> tuple[str, str]:
    parts = argument.rsplit(" -> ", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("invalid bounded throw parser argument")
    return parts[0], parts[1]


def _split_requested_object_state_argument(
    argument: str,
) -> tuple[str, str, str]:
    parts = argument.split(" -> ", 2)
    if len(parts) != 3 or not all(parts):
        raise ValueError("invalid bounded requested object-state argument")
    return parts[0], parts[1], parts[2]


def _split_request_handoff_argument(argument: str) -> tuple[str, str]:
    parts = argument.split(" -> ", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("invalid bounded return-request parser argument")
    return parts[0], parts[1]


def _split_handoff_argument(argument: str) -> tuple[str, str]:
    parts = argument.split(" -> ", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("invalid bounded handoff parser argument")
    return parts[0], parts[1]


def _action_tokens(parts: list[str]) -> list[str]:
    if parts and parts[0].casefold() == "i":
        return parts[1:]
    return parts


def _movement_direction(tokens: list[str]) -> str | None:
    lowered = [token.casefold() for token in tokens]
    if len(lowered) == 1:
        return _DIRECTION_ALIASES.get(lowered[0], lowered[0])

    if lowered and lowered[0] == "to":
        remainder = lowered[1:]
        if remainder and remainder[0] == "the":
            remainder = remainder[1:]
        if remainder and remainder[-1] == "exit":
            remainder = remainder[:-1]
        if len(remainder) == 1:
            return _DIRECTION_ALIASES.get(remainder[0])

    return None


def _is_compound_action(lowered: list[str]) -> bool:
    if not lowered or lowered[0] not in _COMPOUND_ACTION_STARTERS:
        return False

    for index, token in enumerate(lowered[:-1]):
        if token not in {"and", "then"}:
            continue
        next_token = lowered[index + 1]
        if next_token == "then" and index + 2 < len(lowered):
            next_token = lowered[index + 2]
        if next_token in _COMPOUND_ACTION_STARTERS:
            return True
    return False


def parse_terminal_command(raw_text: str) -> ParsedTerminalCommand:
    stripped = raw_text.strip()
    if not stripped:
        return ParsedTerminalCommand(action="empty", raw_text=raw_text)

    parts = _action_tokens(stripped.split())
    if not parts:
        return ParsedTerminalCommand(
            action="unsupported",
            argument=stripped,
            raw_text=raw_text,
            failure_class="unsupported_input_no_executable_route",
        )

    lowered = [part.casefold() for part in parts]
    verb = lowered[0]

    if _is_compound_action(lowered):
        return ParsedTerminalCommand(
            action="unsupported",
            argument=stripped,
            raw_text=raw_text,
            failure_class="unsupported_compound_intent_sequencing",
        )

    if verb in {"look", "l"} and (
        len(parts) == 1
        or (verb == "look" and lowered[1:] == ["around"])
    ):
        return ParsedTerminalCommand(action="look", raw_text=raw_text)

    if verb == "look" and len(parts) == 2:
        direction = _DIRECTION_ALIASES.get(lowered[1])
        if direction is not None:
            return ParsedTerminalCommand(
                action="look_direction",
                argument=direction,
                raw_text=raw_text,
            )

    if verb in {"inspect", "examine"}:
        return _object_action(
            action="inspect",
            target_tokens=parts[1:],
            raw_text=raw_text,
        )

    if verb == "look" and len(parts) >= 3 and lowered[1] == "at":
        return _object_action(
            action="inspect",
            target_tokens=parts[2:],
            raw_text=raw_text,
        )

    if (
        verb == "look"
        and len(parts) >= 4
        and lowered[1:3] == ["closely", "at"]
    ):
        return _object_action(
            action="inspect",
            target_tokens=parts[3:],
            raw_text=raw_text,
        )

    if verb in {"move", "go", "walk", "head"}:
        direction = _movement_direction(parts[1:])
        if direction is not None:
            return ParsedTerminalCommand(
                action="move",
                argument=direction,
                raw_text=raw_text,
            )

    if verb in {"throw", "toss", "hurl"} and len(parts) >= 3:
        direction = _DIRECTION_ALIASES.get(lowered[-1])
        if direction is not None:
            object_reference = _normalized_target(parts[1:-1])
            if object_reference in _DEICTIC_TARGETS:
                return ParsedTerminalCommand(
                    action="ambiguous",
                    argument=object_reference,
                    raw_text=raw_text,
                    failure_class="ambiguous_target_reference",
                )
            if object_reference:
                return ParsedTerminalCommand(
                    action="throw",
                    argument=f"{object_reference} -> {direction}",
                    raw_text=raw_text,
                )

    if verb == "ask" and "to" in lowered[1:]:
        index = lowered.index("to", 1)
        actor_target = _normalized_target(parts[1:index])
        requested_tokens = parts[index + 1:]
        requested_lower = [token.casefold() for token in requested_tokens]
        if requested_lower and requested_lower[0] in {"open", "close", "shut"}:
            operation = (
                "close" if requested_lower[0] == "shut"
                else requested_lower[0]
            )
            object_target = _normalized_target(requested_tokens[1:])
            request_actor_pronouns = _DEICTIC_TARGETS | {
                "him",
                "her",
                "me",
                "you",
            }
            if (
                not actor_target
                or not object_target
                or actor_target in request_actor_pronouns
                or object_target in _DEICTIC_TARGETS
            ):
                ambiguous = (
                    actor_target
                    if actor_target in request_actor_pronouns
                    else object_target
                    if object_target in _DEICTIC_TARGETS
                    else None
                )
                return ParsedTerminalCommand(
                    action="ambiguous",
                    argument=ambiguous,
                    raw_text=raw_text,
                    failure_class="ambiguous_target_reference",
                )
            return ParsedTerminalCommand(
                action="request_object_state",
                argument=(
                    f"{actor_target} -> {operation} -> {object_target}"
                ),
                raw_text=raw_text,
            )

    if verb == "ask" and "for" in lowered[1:]:
        index = lowered.index("for", 1)
        source_target = _normalized_target(parts[1:index])
        object_target = _normalized_target(parts[index + 1:])
        request_actor_pronouns = _DEICTIC_TARGETS | {
            "him",
            "her",
            "me",
            "you",
        }
        if (
            not source_target
            or not object_target
            or source_target in request_actor_pronouns
            or object_target in _DEICTIC_TARGETS
        ):
            ambiguous = (
                source_target
                if source_target in request_actor_pronouns
                else object_target
                if object_target in _DEICTIC_TARGETS
                else None
            )
            return ParsedTerminalCommand(
                action="ambiguous",
                argument=ambiguous,
                raw_text=raw_text,
                failure_class="ambiguous_target_reference",
            )
        return ParsedTerminalCommand(
            action="request_handoff",
            argument=f"{source_target} -> {object_target}",
            raw_text=raw_text,
        )

    if verb in {"give", "hand"} and "to" in lowered[1:]:
        index = lowered.index("to", 1)
        object_target = _normalized_target(parts[1:index])
        recipient_target = _normalized_target(parts[index + 1:])
        handoff_recipient_pronouns = _DEICTIC_TARGETS | {
            "him",
            "her",
            "me",
            "you",
        }
        if (
            not object_target
            or not recipient_target
            or object_target in _DEICTIC_TARGETS
            or recipient_target in handoff_recipient_pronouns
        ):
            ambiguous = (
                object_target
                if object_target in _DEICTIC_TARGETS
                else recipient_target
                if recipient_target in handoff_recipient_pronouns
                else None
            )
            return ParsedTerminalCommand(
                action="ambiguous",
                argument=ambiguous,
                raw_text=raw_text,
                failure_class="ambiguous_target_reference",
            )
        return ParsedTerminalCommand(
            action="handoff",
            argument=f"{object_target} -> {recipient_target}",
            raw_text=raw_text,
        )

    if verb in {"take", "remove", "retrieve"} and "from" in lowered[1:]:
        index = lowered.index("from", 1)
        return _storage_action(
            action="retrieve",
            object_tokens=parts[1:index],
            container_tokens=parts[index + 1:],
            raw_text=raw_text,
        )

    if verb in {"put", "place", "store"}:
        separator = next(
            (
                index
                for index, token in enumerate(lowered[1:], 1)
                if token in {"in", "into"}
            ),
            None,
        )
        if separator is not None:
            return _storage_action(
                action="store",
                object_tokens=parts[1:separator],
                container_tokens=parts[separator + 1:],
                raw_text=raw_text,
            )

    if verb in {"pickup", "take", "grab"}:
        return _object_action(action="pickup", target_tokens=parts[1:], raw_text=raw_text)

    if verb == "pick" and len(parts) >= 2 and lowered[1] == "up":
        return _object_action(action="pickup", target_tokens=parts[2:], raw_text=raw_text)

    if verb == "drop":
        return _object_action(action="drop", target_tokens=parts[1:], raw_text=raw_text)

    if verb in {"light", "ignite"}:
        return _object_action(action="light", target_tokens=parts[1:], raw_text=raw_text)

    if verb == "extinguish":
        return _object_action(action="extinguish", target_tokens=parts[1:], raw_text=raw_text)

    if verb == "open":
        return _object_action(action="open", target_tokens=parts[1:], raw_text=raw_text)

    if verb in {"close", "shut"}:
        return _object_action(action="close", target_tokens=parts[1:], raw_text=raw_text)

    if verb == "put":
        target_tokens = None
        if len(parts) >= 2 and lowered[1] == "down":
            target_tokens = parts[2:]
        elif len(parts) >= 2 and lowered[-1] == "down":
            target_tokens = parts[1:-1]
        if target_tokens is not None:
            return _object_action(action="drop", target_tokens=target_tokens, raw_text=raw_text)

    if verb == "wait" and len(parts) == 1:
        return ParsedTerminalCommand(action="wait", raw_text=raw_text)
    if verb == "save" and len(parts) == 1:
        return ParsedTerminalCommand(action="save", raw_text=raw_text)
    if verb in {"help", "?"} and len(parts) == 1:
        return ParsedTerminalCommand(action="help", raw_text=raw_text)
    if verb in {"exit", "quit"} and len(parts) == 1:
        return ParsedTerminalCommand(action="exit", raw_text=raw_text)

    if not any(char.isalnum() for char in stripped):
        return ParsedTerminalCommand(
            action="uninterpretable",
            argument=stripped,
            raw_text=raw_text,
            failure_class="uninterpretable_player_input",
        )

    pressure = _UNSUPPORTED_CAPABILITY_BY_VERB.get(verb)
    if pressure is not None:
        return ParsedTerminalCommand(
            action="unsupported",
            argument=stripped,
            raw_text=raw_text,
            failure_class=pressure,
        )

    return ParsedTerminalCommand(
        action="unsupported",
        argument=stripped,
        raw_text=raw_text,
        failure_class="unsupported_input_no_executable_route",
    )


def _render_observation_fact(fact: PublicObservationFact) -> str:
    if fact.entity_kind != "object":
        return fact.name

    details: list[str] = []
    if fact.open_state is not None:
        details.append(fact.open_state)
    if fact.lit_state is not None:
        details.append(fact.lit_state)
    if fact.visible_contents:
        details.append("contains " + ", ".join(fact.visible_contents))
    if fact.carrier_name is not None:
        details.append(f"carried by {fact.carrier_name}")

    if not details:
        return fact.name
    return f"{fact.name} [{'; '.join(details)}]"


def _render_view(view: PublicLocationView) -> str:
    lines = [view.name, "", view.description]
    if view.exits:
        lines.extend(("", f"Exits: {', '.join(view.exits)}"))

    object_facts = tuple(
        fact
        for fact in view.observation_facts
        if fact.entity_kind == "object"
    )
    actor_facts = tuple(
        fact
        for fact in view.observation_facts
        if fact.entity_kind == "actor"
    )

    if object_facts:
        lines.extend((
            "",
            "Objects: " + ", ".join(
                _render_observation_fact(fact)
                for fact in object_facts
            ),
        ))
    elif view.objects:
        lines.extend(("", f"Objects: {', '.join(view.objects)}"))

    if actor_facts:
        lines.extend((
            "",
            "Actors: " + ", ".join(
                fact.name
                for fact in actor_facts
            ),
        ))
    elif view.actors:
        lines.extend(("", f"Actors: {', '.join(view.actors)}"))

    if view.carrying:
        lines.extend(("", f"Carrying: {', '.join(view.carrying)}"))
    return "\n".join(lines)


def _render_directional_observation_view(
    view: PublicDirectionalObservationView,
) -> str:
    return "\n".join((
        f"To the {view.direction}: {view.name}",
        "",
        view.description,
    ))


def _render_inspection_view(view: PublicInspectionView) -> str:
    return "\n".join((view.name, "", view.description))


def _player_visible_result_text(result: PlayApplicationResult) -> str:
    if isinstance(result.view, PublicLocationView):
        return _render_view(result.view)
    if isinstance(result.view, PublicDirectionalObservationView):
        return _render_directional_observation_view(result.view)
    if isinstance(result.view, PublicInspectionView):
        return _render_inspection_view(result.view)
    return result.message


def _debug_lines(result: PlayApplicationResult) -> tuple[str, ...]:
    values = (
        ("command_id", result.command_id),
        ("command_fingerprint", result.command_fingerprint),
        ("preview_id", result.preview_id),
        ("receipt_id", result.receipt_id),
        ("state_delta_id", result.state_delta_id),
        ("spatial_evidence_id", result.spatial_evidence_id),
        ("observation_evidence_id", result.observation_evidence_id),
        ("opportunity_evidence_id", result.opportunity_evidence_id),
        ("due_process_ref", result.due_process_ref),
        ("consequence_receipt_id", result.consequence_receipt_id),
        (
            "consequence_state_delta_id",
            result.consequence_state_delta_id,
        ),
        ("world_event_class", result.world_event_class),
        ("world_process_actor_id", result.world_process_actor_id),
        ("world_process_action", result.world_process_action),
        ("world_process_target_id", result.world_process_target_id),
        ("world_process_command_id", result.world_process_command_id),
        ("world_process_outcome", result.world_process_outcome),
        ("logical_time_before", result.logical_time_before),
        ("logical_time_after", result.logical_time_after),
        ("pre_state_digest", result.pre_state_digest),
        ("post_state_digest", result.post_state_digest),
        ("checkpoint_digest", result.checkpoint_digest),
        ("failure_class", result.failure_class),
        ("technical_retry", result.technical_retry),
    )
    return tuple(
        f"[debug] {name}={value}"
        for name, value in values
        if value is not None
    )


def _write_result(
    output: TextIO,
    result: PlayApplicationResult,
    *,
    debug: bool,
) -> str:
    visible = _player_visible_result_text(result)
    if visible:
        output.write(visible)
        output.write("\n")

    if debug:
        for line in _debug_lines(result):
            output.write(line)
            output.write("\n")

    return f"{visible}\n" if visible else ""


def _write_help(output: TextIO) -> str:
    visible = (
        "Commands: look, look <direction>, inspect <entity>, move <direction>, "
        "drop <object>, give <object> to <actor>, "
        "ask <actor> for <object>, "
        "ask <actor> to open/close <object>, "
        "throw <object> <direction>, open <object>, "
        "close <object>, light <object>, "
        "extinguish <object>, put <object> in <container>, "
        "take <object> from <container>, wait, save, help, exit\n"
        "Natural equivalents such as 'I head north', 'look around', "
        "'examine the lantern', 'look at the lantern', 'open the chest', "
        "'walk to the south exit', and 'grab the lantern' route to existing "
        "mechanics when unambiguous.\n"
        "Additional fixture-bounded requests: ask groundskeeper to light lantern, "
        "ask groundskeeper to go to yard, "
        "ask groundskeeper to pick up/drop lantern, ask groundskeeper to "
        "store/retrieve lantern in/from chest, ask groundskeeper to throw "
        "lantern east, ask groundskeeper to follow me, and ask groundskeeper "
        "to stop following me. These are not general NPC controls.\n"
        "Compound intentions and genuinely unsupported attempts are preserved "
        "as capability pressure; they do not mutate authoritative state.\n"
    )
    output.write(visible)
    return visible


def _record_result(
    recorder: LivePlayEvidenceRecorder | None,
    *,
    parsed: ParsedTerminalCommand,
    visible_output: str,
    result: PlayApplicationResult,
    error_stream: TextIO | None,
) -> None:
    if recorder is None:
        return

    try:
        recorder.record_interaction(
            raw_player_input=parsed.raw_text,
            parsed_action=parsed.action,
            parsed_argument=parsed.argument,
            player_visible_output=visible_output,
            result_type=result.result_type,
            authoritative_changed=result.authoritative_changed,
            command_id=result.command_id,
            command_fingerprint=result.command_fingerprint,
            preview_id=result.preview_id,
            receipt_id=result.receipt_id,
            state_delta_id=result.state_delta_id,
            spatial_evidence_id=result.spatial_evidence_id,
            observation_evidence_id=result.observation_evidence_id,
            opportunity_evidence_id=result.opportunity_evidence_id,
            due_process_ref=result.due_process_ref,
            consequence_receipt_id=result.consequence_receipt_id,
            consequence_state_delta_id=result.consequence_state_delta_id,
            world_event_class=result.world_event_class,
            world_process_actor_id=result.world_process_actor_id,
            world_process_action=result.world_process_action,
            world_process_target_id=result.world_process_target_id,
            world_process_command_id=result.world_process_command_id,
            world_process_outcome=result.world_process_outcome,
            logical_time_before=result.logical_time_before,
            logical_time_after=result.logical_time_after,
            pre_state_digest=result.pre_state_digest,
            post_state_digest=result.post_state_digest,
            checkpoint_digest=result.checkpoint_digest,
            failure_class=result.failure_class,
        )
    except LivePlayEvidenceError as exc:
        recorder.mark_incomplete()
        if error_stream is not None:
            error_stream.write(f"Trace evidence incomplete: {exc}\n")


def _finish_evidence(
    recorder: LivePlayEvidenceRecorder | None,
    *,
    application: MyravantPlayApplication,
    error_stream: TextIO | None,
) -> None:
    if recorder is None:
        return

    try:
        recorder.finish(
            final_state_digest=application.authoritative_digest()
        )
    except LivePlayEvidenceError as exc:
        recorder.mark_incomplete()
        if error_stream is not None:
            error_stream.write(f"Trace evidence incomplete: {exc}\n")


def run_terminal(
    application: MyravantPlayApplication,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
    debug: bool = False,
    evidence_recorder: LivePlayEvidenceRecorder | None = None,
    evidence_error_stream: TextIO | None = None,
    specialized_router: Callable[
        [MyravantPlayApplication, str],
        tuple[str, PlayApplicationResult] | None,
    ] | None = None,
) -> int:
    output_stream.write("Myravant\n\n")
    _write_result(output_stream, application.look(), debug=debug)

    while True:
        output_stream.write("\n> ")
        output_stream.flush()
        raw = input_stream.readline()

        if raw == "":
            output_stream.write("\n")
            _finish_evidence(
                evidence_recorder,
                application=application,
                error_stream=evidence_error_stream,
            )
            return 0

        parsed = parse_terminal_command(raw)

        if parsed.action == "empty":
            continue
        if parsed.action == "exit":
            _finish_evidence(
                evidence_recorder,
                application=application,
                error_stream=evidence_error_stream,
            )
            return 0
        if parsed.action == "help":
            _write_help(output_stream)
            continue
        if specialized_router is not None:
            specialized = specialized_router(application, raw)
            if specialized is not None:
                route, result = specialized
                visible = _write_result(output_stream, result, debug=debug)
                _record_result(
                    evidence_recorder,
                    parsed=ParsedTerminalCommand(action=route, raw_text=raw),
                    visible_output=visible,
                    result=result,
                    error_stream=evidence_error_stream,
                )
                continue
        if parsed.action == "look":
            result = application.look()
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "look_direction":
            result = application.look_direction(parsed.argument or "")
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "inspect":
            result = application.inspect(parsed.argument or "")
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "move":
            result = application.move(parsed.argument or "")
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "throw":
            try:
                object_reference, direction = _split_throw_argument(
                    parsed.argument or ""
                )
            except ValueError:
                digest = application.authoritative_digest()
                result = PlayApplicationResult(
                    result_type="object_displacement_rejected",
                    message="That throw could not be routed.",
                    authoritative_changed=False,
                    pre_state_digest=digest,
                    post_state_digest=digest,
                    failure_class="object_displacement_route_unavailable",
                )
            else:
                result = application.throw_object(
                    object_reference,
                    direction,
                )
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "request_object_state":
            try:
                actor_reference, operation, object_reference = (
                    _split_requested_object_state_argument(
                        parsed.argument or ""
                    )
                )
            except ValueError:
                digest = application.authoritative_digest()
                result = PlayApplicationResult(
                    result_type="object_state_request_rejected",
                    message="That request could not be routed.",
                    authoritative_changed=False,
                    pre_state_digest=digest,
                    post_state_digest=digest,
                    failure_class="object_state_request_route_unavailable",
                )
            else:
                result = application.request_object_state_from_actor(
                    actor_reference,
                    operation,
                    object_reference,
                )
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "request_handoff":
            try:
                source_reference, object_reference = (
                    _split_request_handoff_argument(parsed.argument or "")
                )
            except ValueError:
                digest = application.authoritative_digest()
                result = PlayApplicationResult(
                    result_type="actor_object_handoff_rejected",
                    message="That return request could not be routed.",
                    authoritative_changed=False,
                    pre_state_digest=digest,
                    post_state_digest=digest,
                    failure_class="actor_object_handoff_route_unavailable",
                )
            else:
                result = application.request_object_from_actor(
                    source_reference,
                    object_reference,
                )
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "handoff":
            try:
                object_reference, recipient_reference = (
                    _split_handoff_argument(parsed.argument or "")
                )
            except ValueError:
                digest = application.authoritative_digest()
                result = PlayApplicationResult(
                    result_type="actor_object_handoff_rejected",
                    message="That handoff could not be routed.",
                    authoritative_changed=False,
                    pre_state_digest=digest,
                    post_state_digest=digest,
                    failure_class="actor_object_handoff_route_unavailable",
                )
            else:
                result = application.give_object(
                    object_reference,
                    recipient_reference,
                )
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action in {"store", "retrieve"}:
            try:
                object_reference, container_reference = _split_storage_argument(
                    parsed.argument or ""
                )
            except ValueError:
                digest = application.authoritative_digest()
                result = PlayApplicationResult(
                    result_type="storage_rejected",
                    message="That storage attempt could not be routed.",
                    authoritative_changed=False,
                    pre_state_digest=digest,
                    post_state_digest=digest,
                    failure_class="storage_target_unavailable",
                )
            else:
                if parsed.action == "store":
                    result = application.store_object(
                        object_reference,
                        container_reference,
                    )
                else:
                    result = application.retrieve_object(
                        object_reference,
                        container_reference,
                    )
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action in {"light", "extinguish"}:
            if parsed.action == "light":
                result = application.light_object(parsed.argument or "")
            else:
                result = application.extinguish_object(parsed.argument or "")
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action in {"open", "close"}:
            if parsed.action == "open":
                result = application.open_object(parsed.argument or "")
            else:
                result = application.close_object(parsed.argument or "")
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action in {"pickup", "drop"}:
            if parsed.action == "pickup":
                result = application.pickup(parsed.argument or "")
            else:
                result = application.drop(parsed.argument or "")
            visible = _write_result(output_stream, result, debug=debug)
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "wait":
            result = application.wait()
            visible = _write_result(
                output_stream, result, debug=debug
            )
            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue
        if parsed.action == "save":
            try:
                result = application.save()
            except CheckpointPathRequiredError as exc:
                visible = f"Save unavailable: {exc}\n"
                output_stream.write(visible)
                digest = application.authoritative_digest()
                result = PlayApplicationResult(
                    result_type="checkpoint_unavailable",
                    message=visible.rstrip("\n"),
                    authoritative_changed=False,
                    pre_state_digest=digest,
                    post_state_digest=digest,
                    failure_class="checkpoint_path_required",
                )
            else:
                visible = _write_result(
                    output_stream,
                    result,
                    debug=debug,
                )

            _record_result(
                evidence_recorder,
                parsed=parsed,
                visible_output=visible,
                result=result,
                error_stream=evidence_error_stream,
            )
            continue

        if parsed.action == "ambiguous":
            visible = (
                "That attempt needs a clearer target before it can be routed. "
                "No authoritative state changed.\n"
            )
            result_type = "ambiguous_input"
        elif parsed.action == "uninterpretable":
            visible = (
                "That input could not be interpreted as a gameplay attempt. "
                "No authoritative state changed.\n"
            )
            result_type = "uninterpretable_input"
        else:
            visible = (
                "That attempt does not currently have an executable route. "
                "No authoritative state changed.\n"
            )
            result_type = "unsupported_input"

        output_stream.write(visible)
        digest = application.authoritative_digest()
        result = PlayApplicationResult(
            result_type=result_type,
            message=visible.rstrip("\n"),
            authoritative_changed=False,
            pre_state_digest=digest,
            post_state_digest=digest,
            failure_class=(
                parsed.failure_class
                or "unsupported_input_no_executable_route"
            ),
        )
        _record_result(
            evidence_recorder,
            parsed=parsed,
            visible_output=visible,
            result=result,
            error_stream=evidence_error_stream,
        )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="myravant-play",
        description="Run the bounded Myravant terminal-play vertical slice.",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        help="Local checkpoint path used by the save command.",
    )
    parser.add_argument(
        "--load",
        type=Path,
        help="Restore an existing bounded checkpoint before play.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show deterministic command/receipt/digest references.",
    )
    parser.add_argument(
        "--trace",
        type=Path,
        help=(
            "Append nonauthoritative live-play evidence as local JSONL. "
            "Trace failure never changes authoritative state."
        ),
    )
    parser.add_argument(
        "--repository-sha",
        help=(
            "Override the repository SHA recorded in --trace evidence. "
            "Normally resolved from MYRAVANT_REPOSITORY_SHA or git."
        ),
    )
    parser.add_argument(
        "--environment-id",
        help="Optional environment-matrix identity recorded in --trace.",
    )
    parser.add_argument(
        "--network-mode",
        choices=("offline", "restricted", "online", "unknown"),
        help="Optional network mode recorded in --trace.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)

    # The installed command and `python -m` share the latest playable lane.
    # Keep imports here to avoid a circular dependency with VSM terminal modules.
    from astra_runtime.myravant_terminal_capabilities import (
        execute_bounded_terminal_request,
    )
    from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

    checkpoint_path = args.checkpoint or args.load

    if (
        args.trace is not None
        and checkpoint_path is not None
        and args.trace.resolve() == checkpoint_path.resolve()
    ):
        sys.stderr.write(
            "Trace path and checkpoint path must be different files.\n"
        )
        return 2

    try:
        if args.load is not None:
            application = MyravantVSM14Application.restore(
                checkpoint_path=args.load
            )
            if checkpoint_path is not None:
                application.checkpoint_path = checkpoint_path
        else:
            application = MyravantVSM14Application.new(
                checkpoint_path=checkpoint_path
            )
    except PersistentWorldCheckpointError as exc:
        sys.stderr.write(f"Unable to restore checkpoint: {exc}\n")
        return 2

    recorder = None

    if args.trace is not None:
        try:
            header = build_live_play_session_header(
                campaign_id=application.fixture.campaign_id,
                initial_state_digest=application.authoritative_digest(),
                repository_sha=args.repository_sha,
                restore_performed=args.load is not None,
                debug_mode=args.debug,
                environment_id=args.environment_id,
                network_mode=args.network_mode,
            )
            recorder = LivePlayEvidenceRecorder(
                trace_path=args.trace,
                header=header,
            )
        except LivePlayEvidenceError as exc:
            sys.stderr.write(f"Trace evidence unavailable: {exc}\n")

    return run_terminal(
        application,
        input_stream=sys.stdin,
        output_stream=sys.stdout,
        debug=args.debug,
        evidence_recorder=recorder,
        evidence_error_stream=sys.stderr,
        specialized_router=execute_bounded_terminal_request,
    )


if __name__ == "__main__":
    raise SystemExit(main())
