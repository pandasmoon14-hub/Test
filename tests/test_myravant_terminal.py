"""Focused tests for the human-playable Myravant terminal client."""

from __future__ import annotations

import json
from io import StringIO

from astra_runtime.myravant_live_play_evidence import (
    LivePlayEvidenceRecorder,
    build_live_play_session_header,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_terminal import (
    parse_terminal_command,
    run_terminal,
)


def _recorder(tmp_path, app, *, name="trace.jsonl", session_id="trace-test"):
    header = build_live_play_session_header(
        session_id=session_id,
        campaign_id=app.fixture.campaign_id,
        repository_sha="b" * 40,
        initial_state_digest=app.authoritative_digest(),
        restore_performed=False,
        environment_id="ENV-T2-TERMUX-ARM64-DEV",
        network_mode="offline",
    )
    return LivePlayEvidenceRecorder(
        trace_path=tmp_path / name,
        header=header,
    )


def _trace_records(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


def test_parser_supports_bounded_commands_without_claiming_closed_action_space():
    assert parse_terminal_command("look").action == "look"
    parsed = parse_terminal_command("move south")
    assert parsed.action == "move"
    assert parsed.argument == "south"
    assert parse_terminal_command("save").action == "save"
    assert parse_terminal_command("exit").action == "exit"

    unsupported = parse_terminal_command("climb onto the roof")
    assert unsupported.action == "unsupported"
    assert unsupported.argument == "climb onto the roof"


def test_player_terminal_can_move_save_and_exit(tmp_path):
    checkpoint = tmp_path / "terminal.json"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    input_stream = StringIO("look\nmove south\nsave\nexit\n")
    output_stream = StringIO()

    exit_code = run_terminal(
        app,
        input_stream=input_stream,
        output_stream=output_stream,
        debug=False,
    )

    text = output_stream.getvalue()
    assert exit_code == 0
    assert "Myravant" in text
    assert "Workshop" in text
    assert "You move to the Yard." in text
    assert "Checkpoint written." in text
    assert "command_id=" not in text
    assert "post_state_digest=" not in text
    assert checkpoint.exists()


def test_unknown_attempt_is_preserved_without_mutation():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()
    input_stream = StringIO("climb onto the roof\nexit\n")
    output_stream = StringIO()

    run_terminal(
        app,
        input_stream=input_stream,
        output_stream=output_stream,
        debug=False,
    )

    assert app.authoritative_digest() == before
    assert (
        "does not currently have an executable route"
        in output_stream.getvalue()
    )


def test_debug_rendering_does_not_change_authoritative_outcome():
    player_app = MyravantPlayApplication.new()
    debug_app = MyravantPlayApplication.new()

    player_output = StringIO()
    debug_output = StringIO()

    run_terminal(
        player_app,
        input_stream=StringIO("move south\nexit\n"),
        output_stream=player_output,
        debug=False,
    )
    run_terminal(
        debug_app,
        input_stream=StringIO("move south\nexit\n"),
        output_stream=debug_output,
        debug=True,
    )

    assert (
        player_app.authoritative_digest()
        == debug_app.authoritative_digest()
    )
    assert (
        "[debug] command_id=terminal-move-000001"
        not in player_output.getvalue()
    )
    assert (
        "[debug] command_id=terminal-move-000001"
        in debug_output.getvalue()
    )
    assert "[debug] command_fingerprint=" in debug_output.getvalue()
    assert "[debug] preview_id=" in debug_output.getvalue()
    assert "[debug] post_state_digest=" in debug_output.getvalue()


def test_trace_preserves_exact_unsupported_input_without_mutation(tmp_path):
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()
    trace_path = tmp_path / "trace.jsonl"
    recorder = _recorder(tmp_path, app)

    run_terminal(
        app,
        input_stream=StringIO("climb onto the roof\nexit\n"),
        output_stream=StringIO(),
        debug=False,
        evidence_recorder=recorder,
        evidence_error_stream=StringIO(),
    )

    assert app.authoritative_digest() == before
    records = _trace_records(trace_path)
    interaction = next(
        record
        for record in records
        if record["record_type"] == "interaction"
    )
    assert interaction["raw_player_input"] == "climb onto the roof\n"
    assert interaction["parsed_action"] == "unsupported"
    assert interaction["authoritative_changed"] is False
    assert interaction["pre_state_digest"] == before
    assert interaction["post_state_digest"] == before


def test_traced_and_untraced_runs_have_identical_authoritative_results(tmp_path):
    traced_checkpoint = tmp_path / "traced-checkpoint.json"
    plain_checkpoint = tmp_path / "plain-checkpoint.json"

    traced_app = MyravantPlayApplication.new(
        checkpoint_path=traced_checkpoint
    )
    plain_app = MyravantPlayApplication.new(
        checkpoint_path=plain_checkpoint
    )
    recorder = _recorder(tmp_path, traced_app)

    traced_exit = run_terminal(
        traced_app,
        input_stream=StringIO("move south\nsave\nexit\n"),
        output_stream=StringIO(),
        debug=False,
        evidence_recorder=recorder,
        evidence_error_stream=StringIO(),
    )
    plain_exit = run_terminal(
        plain_app,
        input_stream=StringIO("move south\nsave\nexit\n"),
        output_stream=StringIO(),
        debug=False,
    )

    assert traced_exit == plain_exit == 0
    assert (
        traced_app.authoritative_digest()
        == plain_app.authoritative_digest()
    )
    assert (
        traced_app.state.committed_transitions[0].receipt.to_dict()
        == plain_app.state.committed_transitions[0].receipt.to_dict()
    )
    assert traced_checkpoint.read_bytes() == plain_checkpoint.read_bytes()


def test_trace_write_failure_cannot_change_authoritative_outcome(
    tmp_path,
    monkeypatch,
):
    traced_app = MyravantPlayApplication.new()
    control_app = MyravantPlayApplication.new()
    recorder = _recorder(tmp_path, traced_app)
    error_stream = StringIO()

    def fail_write(_record):
        raise OSError("synthetic trace write failure")

    monkeypatch.setattr(recorder, "_append_record", fail_write)

    run_terminal(
        traced_app,
        input_stream=StringIO("move south\nexit\n"),
        output_stream=StringIO(),
        evidence_recorder=recorder,
        evidence_error_stream=error_stream,
    )
    run_terminal(
        control_app,
        input_stream=StringIO("move south\nexit\n"),
        output_stream=StringIO(),
    )

    assert (
        traced_app.authoritative_digest()
        == control_app.authoritative_digest()
    )
    assert (
        traced_app.state.committed_transitions[0].receipt.to_dict()
        == control_app.state.committed_transitions[0].receipt.to_dict()
    )
    assert recorder.evidence_complete is False
    assert recorder.trace_write_failures == 1
    assert "Trace evidence incomplete" in error_stream.getvalue()
