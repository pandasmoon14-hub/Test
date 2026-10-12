"""Larger capability package 1: method-qualified grounded physical displacement.

Exercises the installed launcher, owner transitions, deterministic replay and
existing custody, observation and follow integration. Neutral fixture policy
is not a universal push/slide rule, material claim, or canon decision.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_object_displacement import (
    replay_persistent_world_object_displacement,
)
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _installed(commands: tuple[str, ...], *args: str):
    binary = shutil.which("myravant-play")
    assert binary is not None
    return subprocess.run(
        [binary, *args],
        input="\n".join((*commands, "exit", "")),
        text=True, capture_output=True, timeout=60,
    )


def _trace(path):
    records = [
        json.loads(row)
        for row in path.read_text(encoding="utf-8").splitlines()
    ]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    return [r for r in records if r["record_type"] == "interaction"]


@pytest.mark.parametrize(("text", "action", "argument"), (
    ("slide the brass lantern south", "slide", "brass lantern -> south"),
    ("I slide the lantern south", "slide", "lantern -> south"),
    ("push the tool chest north", "push", "tool chest -> north"),
    ("I push chest north", "push", "chest -> north"),
    ("push it north", "ambiguous", "it"),
    ("slide that south", "ambiguous", "that"),
    ("push chest off the roof", "unsupported", "push chest off the roof"),
    ("throw lantern east", "throw", "lantern -> east"),
))
def test_distinct_methods_and_unknown_target_stay_separate(text, action, argument):
    result = parse_terminal_command(text)
    assert (result.action, result.argument) == (action, argument)


def test_slide_and_push_are_real_distinct_grounded_world_transitions():
    app = MyravantVSM14Application.new()
    start = app.authoritative_digest()
    before = app.state.representation

    # No carry step is needed: slide is qualified on the workshop floor.
    slide = app.displace_object("lantern", "south", method="slide")
    assert slide.result_type == "object_displacement_committed"
    assert slide.message == "You slide the Brass Lantern south."
    assert slide.authoritative_changed
    assert slide.receipt_id and slide.state_delta_id
    assert app.authoritative_digest() != start
    assert app.inspect("lantern").result_type == "inspection_unavailable"
    transition = app.runtime_state.committed_object_displacement_transitions[-1]
    assert transition.receipt.method == "slide"
    assert transition.receipt.source_relation_type == "located_at"
    assert transition.receipt.destination_relation_type == "located_at"
    assert replay_persistent_world_object_displacement(
        pre_state_representation=before, receipt=transition.receipt,
    ) == app.state.representation

    # Same player, alternate physical method, different available route.
    assert app.move("south").authoritative_changed
    assert app.inspect("lantern").result_type == "inspection"
    before_push = app.state.representation
    pushed = app.displace_object("lantern", "east", method="push")
    assert pushed.authoritative_changed
    assert pushed.message == "You push the Brass Lantern east."
    assert app.inspect("lantern").result_type == "inspection_unavailable"
    assert app.current_place_id() != app.entity_place_id(
        app.fixture.resolve_object_reference("lantern")
    )
    assert app.inspect("self").view is not None
    assert "Carrying: nothing." in app.inspect("self").view.description
    receipt = app.runtime_state.committed_object_displacement_transitions[-1].receipt
    assert receipt.method == "push"
    assert replay_persistent_world_object_displacement(
        pre_state_representation=before_push, receipt=receipt,
    ) == app.state.representation


def test_push_chest_qualified_without_claiming_arbitrary_object_pushability():
    app = MyravantVSM14Application.new()
    pre = app.authoritative_digest()
    no_access = app.displace_object("chest", "north", method="push")
    assert no_access.failure_class == "object_displacement_target_unavailable"
    assert no_access.post_state_digest == pre
    assert app.move("south").authoritative_changed
    original = app.authoritative_digest()
    cannot_slide = app.displace_object("chest", "north", method="slide")
    assert cannot_slide.failure_class == "object_displacement_route_unavailable"
    assert cannot_slide.pre_state_digest == cannot_slide.post_state_digest == original

    push = app.displace_object("chest", "north", method="push")
    assert push.authoritative_changed
    assert push.message == "You push the Tool Chest north."
    assert app.inspect("chest").result_type == "inspection_unavailable"
    assert app.move("north").authoritative_changed
    assert app.inspect("chest").result_type == "inspection"
    assert app.object_open_state(app.fixture.resolve_object_reference("chest")).state == "closed"

    # Ground objects may not be thrown; carrying something disables sliding it.
    assert app.throw_object("chest", "east").authoritative_changed is False
    assert app.displace_object("chest", "south", method="slide").authoritative_changed is False
    assert app.authoritative_digest() == app.inspect("self").pre_state_digest


def test_held_contested_hidden_and_unsupported_methods_are_nonmutating():
    app = MyravantVSM14Application.new()
    assert app.pickup("lantern").authoritative_changed
    pre = app.authoritative_digest()
    for method, direction in (
        ("push", "south"), ("slide", "south"),
        ("teleport", "south"), ("push", "north"),
    ):
        denial = app.displace_object("lantern", direction, method=method)
        assert not denial.authoritative_changed
        assert denial.pre_state_digest == denial.post_state_digest == pre
    assert app.authoritative_digest() == pre

    assert app.move("south").authoritative_changed
    # The existing throw custody→location path still works.
    thrown = app.throw_object("lantern", "east")
    assert thrown.authoritative_changed
    assert thrown.message == "You throw the Brass Lantern east."
    assert app.runtime_state.committed_object_displacement_transitions[-1].receipt.method == "throw"
    # A faraway object cannot be repositioned by a local push or slide.
    before = app.authoritative_digest()
    for method in ("push", "slide"):
        denial = app.displace_object("lantern", "south", method=method)
        assert not denial.authoritative_changed
        assert denial.pre_state_digest == denial.post_state_digest == before


def test_installed_multi_method_play_state_restarts_and_replays(tmp_path):
    command_set = (
        "look",
        "slide the brass lantern south",
        "inspect myself",
        "move south",
        "look at the lantern",
        "push lantern east",
        "look",
        "push tool chest north",
        "look",
        "move north",
        "inspect chest",
        "inventory",
        "save",
    )
    results = []
    for trial in ("run_a", "run_b"):
        save = tmp_path / f"{trial}.json"
        trace = tmp_path / f"{trial}.jsonl"
        run = _installed(
            command_set, "--checkpoint", str(save), "--trace", str(trace),
            "--repository-sha", "9" * 40,
        )
        assert run.returncode == 0, (run.stdout, run.stderr)
        assert "You slide the Brass Lantern south." in run.stdout
        assert "You push the Brass Lantern east." in run.stdout
        assert "You push the Tool Chest north." in run.stdout
        assert "Checkpoint written." in run.stdout
        events = _trace(trace)
        assert len(events) == len(command_set)
        changed = [r for r in events if r["authoritative_changed"]]
        assert [r["parsed_action"] for r in changed] == [
            "slide", "move", "push", "push", "move",
        ]
        assert all(r["pre_state_digest"] != r["post_state_digest"] for r in changed)
        assert [r["raw_player_input"] for r in events] == [
            cmd + "\n" for cmd in command_set
        ]
        saved = MyravantVSM14Application.restore(checkpoint_path=save)
        assert json.loads(save.read_text(encoding="utf-8"))["format_version"] == 5
        assert saved.authoritative_digest() == events[-1]["post_state_digest"]
        rest = _installed(
            ("look", "inspect chest", "inventory", "save"),
            "--load", str(save), "--checkpoint", str(save),
        )
        assert rest.returncode == 0, (rest.stdout, rest.stderr)
        assert "Tool Chest" in rest.stdout
        assert save.read_bytes() == save.read_bytes()
        results.append((
            [(
                r["parsed_action"], r["result_type"], r["failure_class"],
                r["pre_state_digest"], r["post_state_digest"]
            ) for r in events],
            json.loads(save.read_text(encoding="utf-8")),
        ))
    assert results[0] == results[1]


def test_feedback_conditioned_recovery_chooses_available_method(tmp_path):
    # Attempt an invalid method, read that refusal, then select a licensed
    # physical method without changing canon or granting arbitrary success.
    checkpoint = tmp_path / "feedback.json"
    trace = tmp_path / "feedback.jsonl"
    first = _installed(
        ("slide chest north", "push chest north", "move south",
         "slide chest north", "push chest north", "save"),
        "--checkpoint", str(checkpoint), "--trace", str(trace),
    )
    assert first.returncode == 0, (first.stdout, first.stderr)
    rows = _trace(trace)
    assert [r["authoritative_changed"] for r in rows] == [
        False, False, True, False, True, False
    ]
    assert rows[3]["failure_class"] == "object_displacement_route_unavailable"
    assert rows[4]["result_type"] == "object_displacement_committed"
    assert rows[4]["parsed_action"] == "push"
