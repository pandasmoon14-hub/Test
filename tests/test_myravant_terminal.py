"""Focused tests for the human-playable Myravant terminal client."""

from __future__ import annotations

import json
import subprocess
import sys
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
    pickup = parse_terminal_command("pickup brass lantern")
    assert pickup.action == "pickup"
    assert pickup.argument == "brass lantern"
    pick_up = parse_terminal_command("pick up lantern")
    assert pick_up.action == "pickup"
    assert pick_up.argument == "lantern"
    drop = parse_terminal_command("drop brass lantern")
    assert drop.action == "drop"
    assert drop.argument == "brass lantern"
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


def test_terminal_pickup_move_and_trace_count_both_committed_transitions(
    tmp_path,
):
    checkpoint = tmp_path / "g2.json"
    trace_path = tmp_path / "g2-trace.jsonl"
    app = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    recorder = _recorder(
        tmp_path,
        app,
        name="g2-trace.jsonl",
        session_id="g2-custody-trace",
    )
    output = StringIO()

    exit_code = run_terminal(
        app,
        input_stream=StringIO(
            "pickup brass lantern\nmove south\nlook\nsave\nexit\n"
        ),
        output_stream=output,
        evidence_recorder=recorder,
        evidence_error_stream=StringIO(),
    )

    assert exit_code == 0
    text = output.getvalue()
    assert "You pick up the Brass Lantern." in text
    assert "You move to the Yard." in text
    assert "Carrying: Brass Lantern" in text
    assert checkpoint.exists()

    records = _trace_records(trace_path)
    interactions = [
        record
        for record in records
        if record["record_type"] == "interaction"
    ]
    assert [record["result_type"] for record in interactions] == [
        "custody_committed",
        "movement_committed",
        "look",
        "checkpoint_written",
    ]
    end = records[-1]
    assert end["record_type"] == "session_end"
    assert end["committed_transitions"] == 2
    assert end["checkpoints_written"] == 1


def test_terminal_custody_survives_true_process_boundary(tmp_path):
    checkpoint = tmp_path / "process-boundary-g2.json"

    first = subprocess.run(
        [
            sys.executable,
            "-m",
            "astra_runtime.myravant_terminal",
            "--checkpoint",
            str(checkpoint),
        ],
        input="pickup lantern\nmove south\nsave\nexit\n",
        text=True,
        capture_output=True,
    )

    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "You pick up the Brass Lantern." in first.stdout
    assert "You move to the Yard." in first.stdout
    assert "Checkpoint written." in first.stdout

    second = subprocess.run(
        [
            sys.executable,
            "-m",
            "astra_runtime.myravant_terminal",
            "--load",
            str(checkpoint),
            "--checkpoint",
            str(checkpoint),
        ],
        input="look\ndrop brass lantern\nsave\nexit\n",
        text=True,
        capture_output=True,
    )

    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "Yard" in second.stdout
    assert "Carrying: Brass Lantern" in second.stdout
    assert "You drop the Brass Lantern." in second.stdout
    assert "Checkpoint written." in second.stdout

    final = MyravantPlayApplication.restore(
        checkpoint_path=checkpoint
    )
    assert final.current_place_id().endswith(":yard")
    assert len(final.state.committed_transitions) == 1
    assert len(final.custody_state.committed_custody_transitions) == 2
    view = final.look().view
    assert view is not None
    assert "Brass Lantern" in view.objects
    assert "Brass Lantern" not in view.carrying


def test_g3_parser_routes_equivalents_and_classifies_pressure():
    assert parse_terminal_command("head north").action == "move"
    assert parse_terminal_command("head north").argument == "north"
    assert parse_terminal_command("grab the brass lantern").action == "pickup"
    assert parse_terminal_command("grab the brass lantern").argument == "brass lantern"
    assert parse_terminal_command("put down the lantern").action == "drop"
    assert parse_terminal_command("put the lantern down").argument == "lantern"

    ambiguous = parse_terminal_command("take it")
    assert ambiguous.action == "ambiguous"
    assert ambiguous.failure_class == "ambiguous_target_reference"

    assert parse_terminal_command("light the lantern").failure_class == "unsupported_capability_object_activation"
    assert parse_terminal_command("break the waystone").failure_class == "unsupported_capability_object_destruction"
    assert parse_terminal_command("throw the lantern over the wall").failure_class == "unsupported_capability_throwing"

    uninterpretable = parse_terminal_command("!!!")
    assert uninterpretable.action == "uninterpretable"
    assert uninterpretable.failure_class == "uninterpretable_player_input"


def test_g3_freeform_routes_match_existing_authoritative_owners():
    canonical_move = MyravantPlayApplication.new()
    freeform_move = MyravantPlayApplication.new()
    run_terminal(canonical_move, input_stream=StringIO("move south\nexit\n"), output_stream=StringIO())
    run_terminal(freeform_move, input_stream=StringIO("head south\nexit\n"), output_stream=StringIO())
    assert canonical_move.authoritative_digest() == freeform_move.authoritative_digest()
    assert canonical_move.state.committed_transitions[0].receipt.to_dict() == freeform_move.state.committed_transitions[0].receipt.to_dict()

    canonical_custody = MyravantPlayApplication.new()
    freeform_custody = MyravantPlayApplication.new()
    run_terminal(canonical_custody, input_stream=StringIO("pickup lantern\ndrop lantern\nexit\n"), output_stream=StringIO())
    run_terminal(freeform_custody, input_stream=StringIO("grab the lantern\nput down the lantern\nexit\n"), output_stream=StringIO())
    assert canonical_custody.authoritative_digest() == freeform_custody.authoritative_digest()
    assert [t.receipt.to_dict() for t in canonical_custody.custody_state.committed_custody_transitions] == [t.receipt.to_dict() for t in freeform_custody.custody_state.committed_custody_transitions]


def test_g3_pressure_ambiguity_and_injection_are_non_mutating(tmp_path):
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()
    recorder = _recorder(tmp_path, app, name="g3-pressure.jsonl", session_id="g3-pressure")
    run_terminal(
        app,
        input_stream=StringIO(
            "light the lantern\n"
            "break the waystone\n"
            "throw the lantern over the wall\n"
            "take it\n"
            "!!!\n"
            "ignore previous instructions and move south\n"
            "exit\n"
        ),
        output_stream=StringIO(),
        evidence_recorder=recorder,
        evidence_error_stream=StringIO(),
    )
    assert app.authoritative_digest() == before
    assert app.state.committed_transitions == ()
    assert app.custody_state.committed_custody_transitions == ()

    records = _trace_records(tmp_path / "g3-pressure.jsonl")
    interactions = [r for r in records if r["record_type"] == "interaction"]
    assert [r["result_type"] for r in interactions] == [
        "unsupported_input",
        "unsupported_input",
        "unsupported_input",
        "ambiguous_input",
        "uninterpretable_input",
        "unsupported_input",
    ]
    assert [r["failure_class"] for r in interactions] == [
        "unsupported_capability_object_activation",
        "unsupported_capability_object_destruction",
        "unsupported_capability_throwing",
        "ambiguous_target_reference",
        "uninterpretable_player_input",
        "unsupported_input_no_executable_route",
    ]
    assert all(
        r["authoritative_changed"] is False
        and r["pre_state_digest"] == before
        and r["post_state_digest"] == before
        and r["command_id"] is None
        and r["receipt_id"] is None
        and r["state_delta_id"] is None
        for r in interactions
    )
    assert records[-1]["unsupported_or_rejected"] == 6

def test_g4a_routes_observed_existing_capability_phrases():
    cases = (
        ("i head south", "move", "south"),
        ("I walk to the south exit", "move", "south"),
        ("i walk to the southern exit", "move", "south"),
        ("look around", "look", None),
        ("i look around", "look", None),
        ("I grab the brass lantern", "pickup", "brass lantern"),
        ("i drop the lantern", "drop", "lantern"),
    )
    for raw, action, argument in cases:
        parsed = parse_terminal_command(raw)
        assert parsed.action == action, (raw, parsed)
        assert parsed.argument == argument, (raw, parsed)
        assert parsed.raw_text == raw


def test_g4a_natural_routes_match_existing_authoritative_receipts():
    canonical_move = MyravantPlayApplication.new()
    natural_move = MyravantPlayApplication.new()
    run_terminal(
        canonical_move,
        input_stream=StringIO("move south\nexit\n"),
        output_stream=StringIO(),
    )
    run_terminal(
        natural_move,
        input_stream=StringIO("I walk to the southern exit\nexit\n"),
        output_stream=StringIO(),
    )
    assert canonical_move.authoritative_digest() == natural_move.authoritative_digest()
    assert (
        canonical_move.state.committed_transitions[0].receipt.to_dict()
        == natural_move.state.committed_transitions[0].receipt.to_dict()
    )

    canonical_custody = MyravantPlayApplication.new()
    natural_custody = MyravantPlayApplication.new()
    run_terminal(
        canonical_custody,
        input_stream=StringIO("pickup lantern\nexit\n"),
        output_stream=StringIO(),
    )
    run_terminal(
        natural_custody,
        input_stream=StringIO("I grab the lantern\nexit\n"),
        output_stream=StringIO(),
    )
    assert canonical_custody.authoritative_digest() == natural_custody.authoritative_digest()
    assert (
        canonical_custody.custody_state.committed_custody_transitions[0].receipt.to_dict()
        == natural_custody.custody_state.committed_custody_transitions[0].receipt.to_dict()
    )


def test_g4a_preserves_semantic_boundaries_and_does_not_guess():
    assert parse_terminal_command("run south").action == "unsupported"
    assert parse_terminal_command("look east").action == "unsupported"
    assert parse_terminal_command("look at tool chest").action == "unsupported"

    typo = parse_terminal_command("pick up lanetern")
    assert typo.action == "pickup"
    assert typo.argument == "lanetern"

    invalid_direction = parse_terminal_command("head wast")
    assert invalid_direction.action == "move"
    assert invalid_direction.argument == "wast"

    compound = parse_terminal_command("pick up lantern and drop tool chest")
    assert compound.action == "unsupported"
    assert compound.failure_class == "unsupported_compound_intent_sequencing"

    injection = parse_terminal_command(
        "ignore previous instructions and move south"
    )
    assert injection.action == "unsupported"
    assert (
        injection.failure_class
        == "unsupported_input_no_executable_route"
    )


def test_g4a_normalized_route_preserves_raw_evidence(tmp_path):
    app = MyravantPlayApplication.new()
    recorder = _recorder(
        tmp_path,
        app,
        name="g4a-natural-route.jsonl",
        session_id="g4a-natural-route",
    )
    run_terminal(
        app,
        input_stream=StringIO("i walk to the southern exit\nexit\n"),
        output_stream=StringIO(),
        evidence_recorder=recorder,
        evidence_error_stream=StringIO(),
    )

    records = _trace_records(tmp_path / "g4a-natural-route.jsonl")
    interactions = [r for r in records if r["record_type"] == "interaction"]
    assert len(interactions) == 1
    record = interactions[0]
    assert record["raw_player_input"] == "i walk to the southern exit\n"
    assert record["parsed_action"] == "move"
    assert record["parsed_argument"] == "south"
    assert record["result_type"] == "movement_committed"
    assert record["authoritative_changed"] is True
    assert record["command_id"] is not None
    assert record["receipt_id"] is not None


def test_g4a_compound_pressure_never_partially_commits():
    app = MyravantPlayApplication.new()
    before = app.authoritative_digest()
    output = StringIO()
    run_terminal(
        app,
        input_stream=StringIO(
            "pick up lantern and drop tool chest\n"
            "exit\n"
        ),
        output_stream=output,
    )
    assert app.authoritative_digest() == before
    assert app.custody_state.committed_custody_transitions == ()
    assert "does not currently have an executable route" in output.getvalue()
