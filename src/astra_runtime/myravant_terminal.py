"""Human-playable terminal client for the bounded Myravant G1 vertical slice."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointError,
)
from astra_runtime.myravant_play_application import (
    CheckpointPathRequiredError,
    MyravantPlayApplication,
    PlayApplicationResult,
    PublicLocationView,
)


@dataclass(frozen=True, kw_only=True)
class ParsedTerminalCommand:
    action: str
    argument: str | None = None
    raw_text: str = ""


def parse_terminal_command(raw_text: str) -> ParsedTerminalCommand:
    stripped = raw_text.strip()
    if not stripped:
        return ParsedTerminalCommand(action="empty", raw_text=raw_text)

    parts = stripped.split()
    verb = parts[0].lower()

    if verb in {"look", "l"} and len(parts) == 1:
        return ParsedTerminalCommand(action="look", raw_text=raw_text)

    if verb in {"move", "go", "walk"} and len(parts) == 2:
        return ParsedTerminalCommand(
            action="move",
            argument=parts[1].lower(),
            raw_text=raw_text,
        )

    if verb == "save" and len(parts) == 1:
        return ParsedTerminalCommand(action="save", raw_text=raw_text)

    if verb in {"help", "?"} and len(parts) == 1:
        return ParsedTerminalCommand(action="help", raw_text=raw_text)

    if verb in {"exit", "quit"} and len(parts) == 1:
        return ParsedTerminalCommand(action="exit", raw_text=raw_text)

    return ParsedTerminalCommand(
        action="unsupported",
        argument=stripped,
        raw_text=raw_text,
    )


def _render_view(view: PublicLocationView) -> str:
    lines = [view.name, "", view.description]
    if view.exits:
        lines.extend(("", f"Exits: {', '.join(view.exits)}"))
    if view.objects:
        lines.extend(("", f"Objects: {', '.join(view.objects)}"))
    return "\n".join(lines)


def _debug_lines(result: PlayApplicationResult) -> tuple[str, ...]:
    values = (
        ("command_id", result.command_id),
        ("receipt_id", result.receipt_id),
        ("state_delta_id", result.state_delta_id),
        ("pre_state_digest", result.pre_state_digest),
        ("post_state_digest", result.post_state_digest),
        ("checkpoint_digest", result.checkpoint_digest),
        ("failure_class", result.failure_class),
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
) -> None:
    if result.view is not None:
        output.write(_render_view(result.view))
        output.write("\n")
    elif result.message:
        output.write(result.message)
        output.write("\n")

    if debug:
        for line in _debug_lines(result):
            output.write(line)
            output.write("\n")


def _write_help(output: TextIO) -> None:
    output.write(
        "Commands: look, move <direction>, save, help, exit\n"
        "Other fictionally coherent input is preserved as unsupported input; "
        "it does not mutate authoritative state.\n"
    )


def run_terminal(
    application: MyravantPlayApplication,
    *,
    input_stream: TextIO,
    output_stream: TextIO,
    debug: bool = False,
) -> int:
    output_stream.write("Myravant\n\n")
    _write_result(output_stream, application.look(), debug=debug)

    while True:
        output_stream.write("\n> ")
        output_stream.flush()
        raw = input_stream.readline()

        if raw == "":
            output_stream.write("\n")
            return 0

        parsed = parse_terminal_command(raw)

        if parsed.action == "empty":
            continue
        if parsed.action == "exit":
            return 0
        if parsed.action == "help":
            _write_help(output_stream)
            continue
        if parsed.action == "look":
            _write_result(output_stream, application.look(), debug=debug)
            continue
        if parsed.action == "move":
            result = application.move(parsed.argument or "")
            _write_result(output_stream, result, debug=debug)
            continue
        if parsed.action == "save":
            try:
                result = application.save()
            except CheckpointPathRequiredError as exc:
                output_stream.write(f"Save unavailable: {exc}\n")
            else:
                _write_result(output_stream, result, debug=debug)
            continue

        output_stream.write(
            "That attempt does not currently have an executable route. "
            "No authoritative state changed.\n"
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)

    checkpoint_path = args.checkpoint or args.load

    try:
        if args.load is not None:
            application = MyravantPlayApplication.restore(
                checkpoint_path=args.load
            )
            if checkpoint_path is not None:
                application.checkpoint_path = checkpoint_path
        else:
            application = MyravantPlayApplication.new(
                checkpoint_path=checkpoint_path
            )
    except PersistentWorldCheckpointError as exc:
        sys.stderr.write(f"Unable to restore checkpoint: {exc}\n")
        return 2

    return run_terminal(
        application,
        input_stream=sys.stdin,
        output_stream=sys.stdout,
        debug=args.debug,
    )


if __name__ == "__main__":
    raise SystemExit(main())
