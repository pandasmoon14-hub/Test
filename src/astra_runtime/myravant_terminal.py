"""Human-playable terminal client for the bounded Myravant vertical slice."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

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

    if verb in {"pickup", "take"} and len(parts) >= 2:
        return ParsedTerminalCommand(
            action="pickup",
            argument=" ".join(parts[1:]),
            raw_text=raw_text,
        )

    if (
        verb == "pick"
        and len(parts) >= 3
        and parts[1].lower() == "up"
    ):
        return ParsedTerminalCommand(
            action="pickup",
            argument=" ".join(parts[2:]),
            raw_text=raw_text,
        )

    if verb == "drop" and len(parts) >= 2:
        return ParsedTerminalCommand(
            action="drop",
            argument=" ".join(parts[1:]),
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
    if view.carrying:
        lines.extend(("", f"Carrying: {', '.join(view.carrying)}"))
    return "\n".join(lines)


def _player_visible_result_text(result: PlayApplicationResult) -> str:
    if result.view is not None:
        return _render_view(result.view)
    return result.message


def _debug_lines(result: PlayApplicationResult) -> tuple[str, ...]:
    values = (
        ("command_id", result.command_id),
        ("command_fingerprint", result.command_fingerprint),
        ("preview_id", result.preview_id),
        ("receipt_id", result.receipt_id),
        ("state_delta_id", result.state_delta_id),
        ("spatial_evidence_id", result.spatial_evidence_id),
        ("opportunity_evidence_id", result.opportunity_evidence_id),
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
        "Commands: look, move <direction>, pickup <object>, "
        "drop <object>, save, help, exit\n"
        "Other fictionally coherent input is preserved as unsupported input; "
        "it does not mutate authoritative state.\n"
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
            opportunity_evidence_id=result.opportunity_evidence_id,
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

        visible = (
            "That attempt does not currently have an executable route. "
            "No authoritative state changed.\n"
        )
        output_stream.write(visible)
        digest = application.authoritative_digest()
        result = PlayApplicationResult(
            result_type="unsupported_input",
            message=visible.rstrip("\n"),
            authoritative_changed=False,
            pre_state_digest=digest,
            post_state_digest=digest,
            failure_class="unsupported_input_no_executable_route",
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
    )


if __name__ == "__main__":
    raise SystemExit(main())
