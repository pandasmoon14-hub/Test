"""Human-playable terminal client for the bounded Myravant vertical slice."""

from __future__ import annotations

import argparse
import os
import re
import sys
import uuid
from pathlib import Path
from dataclasses import dataclass
from typing import Callable, TextIO

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointError,
)
from astra_runtime.myravant_live_play_evidence import (
    LivePlayEvidenceError,
    LivePlayEvidenceRecorder,
    build_live_play_session_header,
)
from astra_runtime.myravant_player_sensory_breadth import (
    parse_player_sensory_attempt, execute_player_sensory_attempt,
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
    "approach",
    "look",
    "inspect",
    "examine",
    "search",
    "spot",
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
    "push",
    "slide",
    "drag",
    "haul",
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
    "push": "unsupported_capability_ground_displacement",
    "slide": "unsupported_capability_ground_displacement",
    "drag": "unsupported_capability_ground_displacement",
    "haul": "unsupported_capability_ground_displacement",
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


def _focused_observation_action(
    target_tokens: list[str], raw_text: str,
) -> ParsedTerminalCommand:
    """Represent local or explicitly direction-scoped sensing, not a use action."""

    lowered = [token.casefold() for token in target_tokens]
    direction = None
    for index in range(1, len(lowered)):
        if lowered[index] not in {"to", "in", "toward", "towards"}:
            continue
        following = lowered[index + 1:]
        if following and following[0] == "the":
            following = following[1:]
        if len(following) != 1:
            continue
        candidate = _DIRECTION_ALIASES.get(following[0])
        if candidate is not None:
            direction = candidate
            target_tokens = target_tokens[:index]
            break

    if direction is None and len(lowered) >= 2:
        candidate = _DIRECTION_ALIASES.get(lowered[-1])
        if candidate is not None:
            direction = candidate
            target_tokens = target_tokens[:-1]

    target = _normalized_target(target_tokens)
    if not target or target in _DEICTIC_TARGETS:
        return ParsedTerminalCommand(
            action="ambiguous",
            argument=target or None,
            raw_text=raw_text,
            failure_class="ambiguous_target_reference",
        )
    return ParsedTerminalCommand(
        action="focused_observation",
        argument=f"{target} -> {direction}" if direction else target,
        raw_text=raw_text,
    )


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

    from astra_runtime.myravant_posture import parse_posture
    posture = parse_posture(" ".join(parts))
    if " ".join(lowered) in {"inspect posture", "check posture"}:
        return ParsedTerminalCommand(action="inspect_self", raw_text=raw_text)
    if posture is not None:
        return ParsedTerminalCommand(action="change_posture", argument=posture, raw_text=raw_text)

    if lowered in (["inventory"], ["check", "inventory"], ["my", "inventory"]):
        return ParsedTerminalCommand(action="inspect_self", raw_text=raw_text)

    if (
        (verb in {"look", "search"} and len(lowered) > 1 and lowered[1] == "for")
        or (verb == "spot" and len(lowered) > 1)
    ):
        return _focused_observation_action(
            parts[2:] if verb in {"look", "search"} else parts[1:],
            raw_text,
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

    if verb == "approach":
        return _object_action(action="move_to", target_tokens=parts[1:], raw_text=raw_text)

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

    if verb in {"move", "go", "walk", "head", "crawl"}:
        direction = _movement_direction(parts[1:])
        if direction is not None:
            return ParsedTerminalCommand(
                action="move_crawl" if verb == "crawl" else "move",
                argument=direction,
                raw_text=raw_text,
            )

    if verb in {"throw", "toss", "hurl", "push", "slide", "drag", "haul"} and len(parts) >= 3:
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
                    action=(
                        ("drag" if verb == "haul" else verb)
                        if verb in {"push", "slide", "drag", "haul"} else "throw"
                    ),
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
    if verb in {"help", "?"} and len(parts) in {1, 2}:
        return ParsedTerminalCommand(
            action="help",
            argument=lowered[1] if len(parts) == 2 else None,
            raw_text=raw_text,
        )
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
    lines = [
        f"To the {view.direction}: {view.name}",
        "",
        view.description,
    ]
    if view.visible_objects:
        lines.extend(("", "Visible objects: " + ", ".join(view.visible_objects)))
    if view.visible_actors:
        lines.extend(("", "Visible actors: " + ", ".join(view.visible_actors)))
    return "\n".join(lines)


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


def _write_durable_result(
    output: TextIO,
    application: MyravantPlayApplication,
    result: PlayApplicationResult,
    *,
    debug: bool,
) -> str:
    """Player success is acknowledged only after the owner checkpoint is durable.

    This is the *player-facing acknowledgement boundary*, not an extra owner
    of domain truth. In-process results from application operations are staged
    until the terminal successfully writes the current authoritative snapshot.
    A failed save is fail-closed: no success text, no more commands accepted.
    """
    if result.authoritative_changed:
        generated_path = None
        if application.checkpoint_path is None:
            # Session identity is a storage locator, never authoritative RNG.
            home = Path(os.environ.get(
                "MYRAVANT_SAVE_DIR",
                str(Path.home() / ".myravant" / "saves"),
            ))
            try:
                home.mkdir(mode=0o700, parents=True, exist_ok=True)
            except OSError as exc:
                output.write(f"Unable to establish durable storage: {exc}\n")
                output.flush()
                raise SystemExit(3) from exc
            generated_path = home / f"session-{uuid.uuid4().hex}.json"
            application.checkpoint_path = generated_path
        try:
            acknowledgement = application.save()
            if not acknowledgement.checkpoint_digest:
                raise RuntimeError("checkpoint writer returned no durable digest")
        except Exception as exc:
            output.write(
                "Action could not be durably acknowledged. "
                "Session closed to prevent use of uncertain state.\n"
            )
            output.flush()
            raise SystemExit(3) from exc
        if generated_path is not None:
            output.write(f"Recovery checkpoint: {generated_path}\n")
    visible = _write_result(output, result, debug=debug)
    output.flush()
    return visible


# Player-facing discoverability is presentation, not a command whitelist.
# A category describes methods that depend on actual world opportunity; it
# does not promise universal object affordances or NPC obedience.
_HELP_TOPICS: dict[str, str] = {
    "travel": (
        "Travel and time\n"
        "Look around: look; look north/south/east/west; look for lantern.\n"
        "Travel: go south, walk north, or move east. Routes and obstructions "
        "depend on current location and world state.\n"
        "Try crawl south from the Workshop or crawl east at the Yard. "
        "These are route-specific crawl clearances, not universal mobility "
        "or a guarantee that a body can bypass every obstruction.\n"
        "This fixture also admits stand, crouch, kneel, sit and lie down. "
        "Inspect self shows your recorded posture; old sessions start unrecorded. "
        "A recorded crouch, kneel or lying configuration qualifies the Yard's "
        "low passage when obstructed. Walking and crawling keep their own methods. "
        "Changing posture alone does not advance time.\n"
        "Wait advances world time; people may act independently. "
        "Use look again to observe what changed.\n"
        "For exactly two independent steps, try go south then inspect chest, "
        "crouch then inspect chest brace, or service chest latch then close chest. "
        "Existing specialist work and actor requests use their ordinary checks. "
        "Each step is checked and saved separately; a refusal stops the "
        "second step. This does not promise simultaneous actions.\n"
        "Other attempts are evaluated on their own terms; the examples "
        "are not a list of everything you may try."
    ),
    "senses": (
        "Observation and yourself\n"
        "look, inspect lantern, examine chest, look at chest, "
        "search for waystone, look south.\n"
        "To inspect current possessions: inventory, inspect myself, "
        "check my hands, or examine what I am carrying.\n"
        "To attempt direct physical sensing: touch chest, feel for waystone, "
        "or search by touch for chest. Touch needs a reachable, grounded "
        "object with a known affordance; it does not grant hidden knowledge.\n"
        "What can be seen and what can be touched may differ in poor light."
    ),
    "objects": (
        "Handling objects\n"
        "take/drop lantern; give lantern to groundskeeper or ask for its return. "
        "open/close chest, light/extinguish lantern, put lantern in chest, "
        "take lantern from chest.\n"
        "Grounded placement is route- and method-specific: push chest north, "
        "slide lantern south, drag waystone west, throw lantern east. "
        "Additional licensed examples: drag lantern south from Workshop; "
        "drag a closed chest north from Yard; slide a closed chest east "
        "from Yard; slide a recovered Waystone north. No universal "
        "material, force, dragging or sliding rule is implied.\n"
        "In poor light, try feel for waystone then drag waystone west; "
        "contact is rechecked and does not authorize unlicensed routes.\n"
        "Goal-led attempts: get lantern to yard by sliding then go south; "
        "get lantern to orchard; get waystone to yard "
        "by dragging, clear the yard east exit by pushing waystone north, "
        "or move chest to orchard by pushing. Ask how to get chest to "
        "orchard to inspect current methods; a chosen action is one step, "
        "not an automatic plan.\n"
        "At Yard you may send a Lantern toward Orchard by push or throw, "
        "or ask a present Groundskeeper to throw a Lantern they carry. "
        "Carrying, custody and actor willingness remain distinct.\n"
        "Try supply orchard with lantern for qualified choices. A lit "
        "Lantern may be carried, or stored in an open Chest; close the "
        "Chest before a licensed east push or slide transports actual "
        "contents. In darkness, sealed contents do not illuminate the "
        "path. Open and retrieve separately on arrival. Waystone "
        "placement can obstruct the east exit; lawful clearance changes "
        "access. Each action has its own consequence."
    ),
    "people": (
        "People and cooperation\n"
        "Ask a present, willing person to help with a qualified task; "
        "the request is not automatic obedience.\n"
        "Examples: ask groundskeeper to follow me; ask groundskeeper to "
        "stop following me; ask groundskeeper to go to yard; ask "
        "groundskeeper to bring lantern to orchard; ask groundskeeper to "
        "open chest; ask groundskeeper to light lantern.\n"
        "Ask groundskeeper to pick up lantern, drop lantern, store "
        "lantern in chest, retrieve lantern from chest, or throw lantern east "
        "when the necessary object, location and opportunity exist.\n"
        "For recollection and investigation, see help inquiry. "
        "A petition is not the same as handing over an object."
    ),
    "work": (
        "Ongoing work and consequences\n"
        "Try work on lantern preparation or work on chest staging. "
        "Check or resume an unfinished goal; actual object state persists.\n"
        "At the Yard, service chest latch (two manual contributions) "
        "or service chest latch with lantern after supplying a lit lantern. "
        "Check latch service, resume chest latch service or abandon latch service.\n"
        "Remove chest brace (manual method), or remove chest brace with "
        "lantern when the tool is lit at the worksite. Inspect chest "
        "brace or refit chest brace. Refit and close the chest before "
        "securing the serviced latch; release chest latch to reopen.\n"
        "At Orchard Path, recover waystone; clear waystone route after "
        "meeting the actual route, placement and light conditions. "
        "Check route clearance or abandon waystone clearance.\n"
        "When co-present at the Yard, ask groundskeeper to repair chest "
        "latch with lantern, or ask groundskeeper to secure chest latch "
        "later when the latch is ready. Check chest duty or "
        "cancel groundskeeper chest duty while the actor is available.\n"
        "For Chest readiness, try prepare chest for orchard at the Yard. "
        "Choose one qualified step: manual service, lantern service, "
        "Groundskeeper-assisted service, brace refit, closure, direct "
        "securing, delayed duty, or a separately qualified push east. "
        "Each step has actual prerequisites and no automatic success.\n"
        "Resources, voluntary commitments, work progress and time "
        "are real; general crafting, wages and a market are not defined."
    ),
    "inquiry": (
        "Learning from another person\n"
        "Ask groundskeeper if they have lantern, where lantern is, what "
        "are you carrying, or are you following me.\n"
        "Ask groundskeeper to inspect chest for a first-hand visual "
        "sighting. Tell groundskeeper chest is at gatehouse to offer an "
        "unverified report, not rewrite world truth.\n"
        "Ask groundskeeper where they last saw chest, where they think "
        "chest is, or to investigate last witnessed location of chest "
        "or last reported location of chest.\n"
        "Ask groundskeeper to touch chest or check chest by touch "
        "where near-field contact is qualified. A touch is not "
        "automatically a remembered visual sighting. Reports may be stale.\n"
        "For conflicting local Chest leads, try trace chest with "
        "groundskeeper. You may choose a firsthand witnessed sighting, "
        "give an explicitly unverified report, compare the two historical "
        "sources, follow either lead with the consenting actor, verify "
        "directly, or physically push the Chest along a qualified route. "
        "A lead is never proof of present placement."
    ),
    "session": (
        "Session controls\n"
        "save writes an authoritative checkpoint when available. "
        "The terminal automatically checkpoints acknowledged state "
        "changes when configured for durable play.\n"
        "wait advances time. exit ends your current session.\n"
        "To resume a saved game, launch Myravant with --load <checkpoint>. "
        "A recovery checkpoint may be printed when one is created.\n"
        "Try help travel, help senses, help objects, help people, "
        "help work or help inquiry for other possibilities."
    ),
}
_HELP_ALIASES = {
    "movement": "travel",
    "time": "travel",
    "observation": "senses",
    "self": "senses",
    "inventory": "senses",
    "items": "objects",
    "npc": "people",
    "npcs": "people",
    "tasks": "work",
    "memory": "inquiry",
    "investigation": "inquiry",
    "save": "session",
    "system": "session",
}


def _write_help(output: TextIO, topic: str | None = None) -> str:
    """Display concise ordinary help or one requested capability section."""
    normalized = topic.strip().casefold() if topic else ""
    normalized = _HELP_ALIASES.get(normalized, normalized)
    overview = (
        "Commands: look, inspect, inventory, move, wait, save, exit.\n"
        "You can attempt other coherent actions; outcomes depend on "
        "your situation, resources and other actors.\n"
        "Explore: help travel, help senses, help objects, help people, "
        "help work, help inquiry, help session.\n"
        "For every topic together: help all.\n"
    )
    if not normalized:
        visible = overview
    elif normalized == "all":
        visible = overview + "\n" + "\n\n".join(_HELP_TOPICS.values()) + "\n"
    elif normalized in _HELP_TOPICS:
        visible = _HELP_TOPICS[normalized] + "\n"
    else:
        visible = (
            "No help topic named " + repr(topic) + ".\n"
            "Choose travel, senses, objects, people, work, inquiry or session.\n"
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


# A deliberately bounded sequence interpreter, not an action authority.
# Both ordinary one-step commands and this explicit two-step path call the
# identical existing application owners below. No hidden planner/automation.
_COMPOSABLE_STEP_ACTIONS = frozenset({
    "look", "look_direction", "focused_observation", "inspect", "inspect_self",
    "move", "move_crawl", "move_to", "pickup", "drop", "open", "close", "light", "extinguish",
    "store", "retrieve", "throw", "push", "slide", "drag", "wait",
    "player_sense", "request_object_state", "request_handoff", "handoff",
    "physical_placement_goal", "destination_goal_method", "change_posture",
})


def _explicit_two_step_intent(raw_text: str, *, fixture=None) -> tuple[
    ParsedTerminalCommand, ParsedTerminalCommand,
] | None:
    # Sequence is explicit, ordered and exactly two independent commands.
    # Simultaneous 'while', mixed 'and', malformed third steps and internal
    # save/exit/help are not silently collapsed into a single success.
    pieces = re.split(r"\s+then\s+", raw_text.strip(), flags=re.IGNORECASE)
    if len(pieces) != 2 or not all(pieces):
        return None
    # Local import avoids the historical VSM terminal import cycle.
    from astra_runtime.myravant_terminal_capabilities import (
        BOUNDED_TERMINAL_ROUTES, classify_bounded_terminal_request,
        _classify_bounded_terminal_request,
    )
    parsed_steps = []
    for piece in pieces:
        admitted = getattr(fixture, "specialist_routes", None)
        candidate = _classify_bounded_terminal_request(piece, fixture=fixture)
        if admitted is not None and candidate is not None and candidate not in admitted:
            return None
        step = parse_terminal_command(piece)
        # Standalone specialists have first refusal even when generic inspect
        # or ask also recognizes the words. Preflight must preserve that meaning.
        route = classify_bounded_terminal_request(piece, fixture=fixture)
        if route is not None:
            # Preserve existing trace names for the three prior adapters.
            action = "player_sense" if route == "player_sensory_attempt" else route
            step = ParsedTerminalCommand(action=action, argument=piece, raw_text=piece)
        parsed_steps.append(step)
    parsed = tuple(parsed_steps)
    if any(step.action not in _COMPOSABLE_STEP_ACTIONS
           and step.action not in BOUNDED_TERMINAL_ROUTES for step in parsed):
        return None
    return parsed[0], parsed[1]


def _execute_composable_core_step(
    application: MyravantPlayApplication, parsed: ParsedTerminalCommand,
) -> PlayApplicationResult:
    # This dispatcher is presentation-level reuse of original one-step
    # semantics. Every authoritative transition is still made by its owner.
    action = parsed.action
    argument = parsed.argument or ""
    from astra_runtime.myravant_terminal_capabilities import (
        BOUNDED_TERMINAL_ROUTES, execute_classified_bounded_terminal_request,
    )
    if action in BOUNDED_TERMINAL_ROUTES:
        return execute_classified_bounded_terminal_request(
            application, argument, route=action,
        )
    if action == "change_posture":
        if not hasattr(application, "change_posture"):
            digest = application.authoritative_digest()
            return PlayApplicationResult(
                result_type="posture_rejected",
                message="No posture profile is qualified for this starting character.",
                authoritative_changed=False, pre_state_digest=digest, post_state_digest=digest,
                failure_class="posture_profile_unavailable",
            )
        return application.change_posture(argument)
    if action == "player_sense":
        # Existing BREADTH-1 AFQR-20 contact/holdings owner; read-only
        # result has no persisted target or deferred manipulation privilege.
        return execute_player_sensory_attempt(application, argument)
    if action == "request_object_state":
        try:
            actor_reference, operation, object_reference = (
                _split_requested_object_state_argument(
                    argument
                )
            )
        except ValueError:
            digest = application.authoritative_digest()
            return PlayApplicationResult(
                result_type="object_state_request_rejected",
                message="That request could not be routed.",
                authoritative_changed=False,
                pre_state_digest=digest,
                post_state_digest=digest,
                failure_class="object_state_request_route_unavailable",
            )
        else:
            return application.request_object_state_from_actor(
                actor_reference,
                operation,
                object_reference,
            )
    if action == "request_handoff":
        try:
            source_reference, object_reference = (
                _split_request_handoff_argument(argument)
            )
        except ValueError:
            digest = application.authoritative_digest()
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="That return request could not be routed.",
                authoritative_changed=False,
                pre_state_digest=digest,
                post_state_digest=digest,
                failure_class="actor_object_handoff_route_unavailable",
            )
        else:
            return application.request_object_from_actor(
                source_reference,
                object_reference,
            )
    if action == "handoff":
        try:
            object_reference, recipient_reference = (
                _split_handoff_argument(argument)
            )
        except ValueError:
            digest = application.authoritative_digest()
            return PlayApplicationResult(
                result_type="actor_object_handoff_rejected",
                message="That handoff could not be routed.",
                authoritative_changed=False,
                pre_state_digest=digest,
                post_state_digest=digest,
                failure_class="actor_object_handoff_route_unavailable",
            )
        else:
            return application.give_object(
                object_reference,
                recipient_reference,
            )
    if action == "look":
        return application.look()
    if action == "look_direction":
        return application.look_direction(argument)
    if action == "focused_observation":
        if " -> " in argument:
            target, direction = argument.rsplit(" -> ", 1)
            return application.focused_observation(target, direction=direction)
        return application.focused_observation(argument)
    if action in {"inspect", "inspect_self"}:
        return application.inspect("self" if action == "inspect_self" else argument)
    if action == "move_to":
        return application.approach_place(argument)
    if action in {"move", "move_crawl"}:
        return application.move(
            argument,
            method="crawl" if action == "move_crawl" else "walk",
        )
    if action in {"throw", "push", "slide", "drag"}:
        try:
            object_reference, direction = _split_throw_argument(argument)
        except ValueError:
            digest = application.authoritative_digest()
            return PlayApplicationResult(
                result_type="object_displacement_rejected",
                message="That throw could not be routed.",
                authoritative_changed=False,
                pre_state_digest=digest, post_state_digest=digest,
                failure_class="object_displacement_route_unavailable",
            )
        return (
            application.throw_object(object_reference, direction)
            if action == "throw"
            else application.displace_object(
                object_reference, direction, method=action,
            )
        )
    if action in {"store", "retrieve"}:
        try:
            object_reference, container_reference = _split_storage_argument(argument)
        except ValueError:
            digest = application.authoritative_digest()
            return PlayApplicationResult(
                result_type="storage_rejected",
                message="That storage attempt could not be routed.",
                authoritative_changed=False,
                pre_state_digest=digest, post_state_digest=digest,
                failure_class="storage_target_unavailable",
            )
        return (
            application.store_object(object_reference, container_reference)
            if action == "store" else
            application.retrieve_object(object_reference, container_reference)
        )
    if action in {"light", "extinguish"}:
        return (
            application.light_object(argument) if action == "light"
            else application.extinguish_object(argument)
        )
    if action in {"open", "close"}:
        return (
            application.open_object(argument) if action == "open"
            else application.close_object(argument)
        )
    if action in {"pickup", "drop"}:
        return (
            application.pickup(argument) if action == "pickup"
            else application.drop(argument)
        )
    if action == "wait":
        return application.wait()
    raise ValueError("not a bounded, qualified composable core step")


def _interval_stream(application, raw):
    """Optional bounded duration presentation; each yield follows one owner commit."""
    handler = getattr(application, 'interval_results_for_request', None)
    return None if handler is None else handler(raw)


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
    _write_durable_result(output_stream, application, application.look(), debug=debug)

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
            if getattr(application.fixture, "locality_help", None):
                output_stream.write(application.fixture.locality_help + "\n")
            else:
                _write_help(output_stream, parsed.argument)
            continue
        # Preflight *both* independently parseable steps before executing
        # either. Once execution begins, each step is independently durable;
        # a contextual refusal stops the sequence but does not undo a lawful
        # first transition. This is explicit sequence, not simultaneous work.
        planned = _explicit_two_step_intent(raw, fixture=application.fixture)
        if planned is not None:
            halted = False
            for ordinal, step in enumerate(planned, 1):
                stream = _interval_stream(application, step.argument)
                if stream is None:
                    stream = (_execute_composable_core_step(application, step),)
                for result in stream:
                    output_stream.write(f"Sequence step {ordinal}/2: ")
                    visible = _write_durable_result(output_stream, application, result, debug=debug)
                    _record_result(evidence_recorder,
                        parsed=ParsedTerminalCommand(action=f"sequence_{ordinal}_{step.action}",argument=step.argument,raw_text=raw),
                        visible_output=f"Sequence step {ordinal}/2: "+visible,result=result,error_stream=evidence_error_stream)
                    if result.failure_class is not None:
                        output_stream.write("Sequence halted after this refusal; no later step was attempted.\n")
                        halted = True
                        break
                if halted:
                    break
            continue
        stream = _interval_stream(application, raw)
        if stream is not None:
            for result in stream:
                visible = _write_durable_result(output_stream, application, result, debug=debug)
                _record_result(evidence_recorder,parsed=ParsedTerminalCommand(action="timed_interval",raw_text=raw),
                               visible_output=visible,result=result,error_stream=evidence_error_stream)
                if result.failure_class is not None:
                    break
            continue
        if specialized_router is not None:
            specialized = specialized_router(application, raw)
            if specialized is not None:
                route, result = specialized
                visible = _write_durable_result(output_stream, application, result, debug=debug)
                _record_result(
                    evidence_recorder,
                    parsed=ParsedTerminalCommand(action=route, raw_text=raw),
                    visible_output=visible,
                    result=result,
                    error_stream=evidence_error_stream,
                )
                continue
        if parsed.action in {
            "look", "look_direction", "focused_observation",
            "inspect", "inspect_self", "move", "move_crawl", "move_to", "throw", "push", "slide", "drag", "change_posture",
        }:
            result = _execute_composable_core_step(application, parsed)
            visible = _write_durable_result(
                output_stream, application, result, debug=debug,
            )
            _record_result(
                evidence_recorder, parsed=parsed, visible_output=visible,
                result=result, error_stream=evidence_error_stream,
            )
            continue
        if parsed.action in {
            "store", "retrieve", "light", "extinguish",
            "open", "close", "pickup", "drop", "wait",
            "request_object_state", "request_handoff", "handoff",
        }:
            result = _execute_composable_core_step(application, parsed)
            visible = _write_durable_result(
                output_stream, application, result, debug=debug,
            )
            _record_result(
                evidence_recorder, parsed=parsed, visible_output=visible,
                result=result, error_stream=evidence_error_stream,
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
                visible = _write_durable_result(
                    output_stream, application,
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
        "--locality", choices=("development", "tarrow", "tarrow-depth", "tarrow-material", "tarrow-water", "tarrow-time", "tarrow-actors", "tarrow-investigation"), default="development",
        help="Select a qualified locality; saved campaigns are not converted.",
    )
    parser.add_argument(
        "--investigation-case", choices=("cleanup", "assembly", "relay", "neutral-contended", "neutral-reverse", "neutral-relay"), default="cleanup",
        help="Select a noncanonical, version-bound investigation circumstance profile.",
    )
    parser.add_argument(
        "--prepare-investigation",
        action="store_true",
        help=(
            "Start a neutral, noncanonical investigation with lawful, receipted "
            "prehistory at a new --checkpoint. Refuses --load and existing saves; "
            "use --load for every subsequent session."
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
    application_type = MyravantVSM14Application
    locality_args = {}
    if args.locality in {"tarrow", "tarrow-depth", "tarrow-material"}:
        from astra_runtime.myravant_tarrow import create_tarrow_fixture, execute_tarrow_request
        application_type = MyravantPlayApplication
        locality_args = {"fixture": create_tarrow_fixture()}
        execute_bounded_terminal_request = execute_tarrow_request
        if args.locality == "tarrow-depth":
            from astra_runtime.myravant_tarrow_environment import create_environment_fixture, execute_environment_request
            locality_args = {"fixture": create_environment_fixture()}
            execute_bounded_terminal_request = execute_environment_request

    if args.locality == "tarrow-material":
        from astra_runtime.myravant_material_application import MaterialApplication
        from astra_runtime.myravant_tarrow_material import create_material_fixture, execute_material_locality_request
        application_type = MaterialApplication
        locality_args = {"fixture": create_material_fixture()}
        execute_bounded_terminal_request = execute_material_locality_request

    if args.locality == "tarrow-water":
        from astra_runtime.myravant_water_application import WaterApplication
        from astra_runtime.myravant_tarrow_water import create_water_fixture, execute_water_locality_request
        application_type = WaterApplication
        locality_args = {"fixture": create_water_fixture()}
        execute_bounded_terminal_request = execute_water_locality_request

    if args.locality == "tarrow-time":
        from astra_runtime.myravant_timed_application import TimedApplication
        from astra_runtime.myravant_tarrow_time import create_timed_fixture, execute_timed_locality_request
        application_type = TimedApplication
        locality_args = {"fixture": create_timed_fixture()}
        execute_bounded_terminal_request = execute_timed_locality_request

    if args.locality == "tarrow-actors":
        from astra_runtime.myravant_actor_application import ActorApplication
        from astra_runtime.myravant_tarrow_actors import create_actor_fixture, execute_actor_locality_request
        application_type = ActorApplication
        locality_args = {"fixture": create_actor_fixture()}
        execute_bounded_terminal_request = execute_actor_locality_request

    if args.locality == "tarrow-investigation":
        from astra_runtime.myravant_investigation_application import InvestigationApplication
        from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture, execute_investigation_request
        application_type = InvestigationApplication
        locality_args = {"fixture": create_investigation_fixture(args.investigation_case)}
        execute_bounded_terminal_request = execute_investigation_request

    if (
        args.trace is not None
        and checkpoint_path is not None
        and args.trace.resolve() == checkpoint_path.resolve()
    ):
        sys.stderr.write(
            "Trace path and checkpoint path must be different files.\n"
        )
        return 2

    # Noncanonical case preparation is a deliberate fresh-start choice, never
    # an implicit fixture side effect and never run when restoring a campaign.
    # The existing case builder performs only qualified owner actions, saves
    # their receipts and returns the replay-validated state.
    if args.prepare_investigation:
        from astra_runtime.myravant_investigation_cases import PREHISTORIES
        if (args.locality != "tarrow-investigation" or args.load is not None
                or args.checkpoint is None or args.investigation_case not in PREHISTORIES):
            sys.stderr.write(
                "Prepared investigation requires --locality tarrow-investigation, "
                "a neutral --investigation-case, a new --checkpoint and no --load.\n"
            )
            return 2

    try:
        if args.prepare_investigation:
            from astra_runtime.myravant_investigation_cases import build_investigation_case
            application, _preparation_receipts = build_investigation_case(
                args.investigation_case, checkpoint_path
            )
        elif args.load is not None:
            application = application_type.restore(
                checkpoint_path=args.load, **locality_args
            )
            if checkpoint_path is not None:
                application.checkpoint_path = checkpoint_path
        else:
            application = application_type.new(
                checkpoint_path=checkpoint_path, **locality_args
            )
    except (PersistentWorldCheckpointError, ValueError) as exc:
        sys.stderr.write(f"Unable to initialize or restore checkpoint: {exc}\n")
        return 2

    if args.prepare_investigation:
        sys.stdout.write(
            "Noncanonical investigation circumstance prepared through "
            "committed world actions; inspect, recall and inquire to learn "
            "what your character has actually admitted.\n"
        )

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
