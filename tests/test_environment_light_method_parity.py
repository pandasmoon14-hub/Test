"""Environmentally consequential method parity for one licensed light corridor.

Light emitted by a directly placed, lit object derives from *current* RT-010
placement and object-lit state, not whether the player threw it there.
This fixture licenses only a glimmer to the east; it does not grant remote
sight, object location knowledge, physics or a general light propagation law.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID,
    ORCHARD_PATH_ID,
    YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


SIGNAL = "You can see the Brass Lantern's light to the east."


def _method_sequence(method: str) -> tuple[str, ...]:
    if method == "throw":
        return (
            "pickup lantern", "light lantern", "move south",
            "throw lantern east",
        )
    if method == "push":
        return (
            "light lantern", "slide lantern south",
            "move south", "push lantern east",
        )
    if method == "carry_drop":
        return (
            "pickup lantern", "light lantern", "move south",
            "move east", "drop lantern", "move west",
        )
    if method == "unlit_push":
        return (
            "slide lantern south", "move south", "push lantern east",
        )
    raise ValueError(method)


def _perform(app, attempt: str):
    if attempt == "pickup lantern":
        return app.pickup("lantern")
    if attempt == "light lantern":
        return app.light_object("lantern")
    if attempt == "slide lantern south":
        return app.displace_object("lantern", "south", method="slide")
    if attempt == "push lantern east":
        return app.displace_object("lantern", "east", method="push")
    if attempt == "throw lantern east":
        return app.throw_object("lantern", "east")
    if attempt == "drop lantern":
        return app.drop("lantern")
    if attempt.startswith("move "):
        return app.move(attempt.split()[1])
    raise ValueError(attempt)


def _assert_readonly_glimmer(app, *, expected: bool):
    digest = app.authoritative_digest()
    logical = app.runtime_state.logical_time_state.logical_position
    result = app.look_direction("east")
    assert result.authoritative_changed is False
    assert result.pre_state_digest == result.post_state_digest == digest
    assert app.authoritative_digest() == digest
    assert app.runtime_state.logical_time_state.logical_position == logical
    assert result.view is None
    if expected:
        assert result.result_type == "directional_light_signal"
        assert result.message == SIGNAL
        assert result.observation_evidence_id
        assert result.failure_class is None
        # Seeing a distant light never licenses the remote place's contents.
        assert "Orchard Path" not in result.message
        assert "Weathered Waystone" not in result.message
        unseen = app.focused_observation("waystone", direction="east")
        assert unseen.result_type == "focused_observation_unavailable"
        assert unseen.pre_state_digest == unseen.post_state_digest == digest
    else:
        assert result.result_type == "directional_observation_unavailable"
        assert result.failure_class == "directional_observation_unlicensed"
    return result


@pytest.mark.parametrize(
    "method", ("throw", "push", "carry_drop", "unlit_push"),
)
def test_present_lit_placement_not_historical_method_controls_signal(method):
    app = MyravantVSM14Application.new()
    for instruction in _method_sequence(method):
        committed = _perform(app, instruction)
        assert committed.authoritative_changed, (method, instruction, committed)
        assert committed.receipt_id
    assert app.current_place_id() == YARD_ID
    direct = [
        r for r in app.state.representation.relations
        if r.relation_type == LOCATED_AT_RELATION_TYPE
        and r.subject_entity_id == LANTERN_ID
        and r.object_entity_id == ORCHARD_PATH_ID
    ]
    assert len(direct) == 1
    lantern = app.object_lit_state(LANTERN_ID)
    assert lantern is not None
    assert lantern.state == ("unlit" if method == "unlit_push" else "lit")
    # Carry-and-drop creates no displacement receipt. The world effect still
    # matches equivalent present placement and illumination state.
    if method == "carry_drop":
        assert not any(
            t.receipt.destination_place_id == ORCHARD_PATH_ID
            for t in app.runtime_state.committed_object_displacement_transitions
        )
    _assert_readonly_glimmer(app, expected=(method != "unlit_push"))


def test_signal_ceases_when_source_is_extinguished_or_removed():
    app = MyravantVSM14Application.new()
    for attempt in _method_sequence("push"):
        assert _perform(app, attempt).authoritative_changed
    _assert_readonly_glimmer(app, expected=True)
    assert app.move("east").authoritative_changed
    assert app.extinguish_object("lantern").authoritative_changed
    assert app.move("west").authoritative_changed
    _assert_readonly_glimmer(app, expected=False)

    assert app.move("east").authoritative_changed
    assert app.light_object("lantern").authoritative_changed
    assert app.move("west").authoritative_changed
    _assert_readonly_glimmer(app, expected=True)

    assert app.move("east").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.move("west").authoritative_changed
    _assert_readonly_glimmer(app, expected=False)
    # In particular a light the player carries does not appear as a remote
    # independent environmental source.
    assert any(
        r.relation_type == CARRIED_BY_RELATION_TYPE
        and r.subject_entity_id == LANTERN_ID
        and r.object_entity_id == app.fixture.player_entity_id
        for r in app.state.representation.relations
    )


def test_no_unlicensed_light_corridor_is_inferred_from_movement_topology():
    app = MyravantPlayApplication.new()
    assert app.light_object("lantern").authoritative_changed
    assert app.displace_object("lantern", "south", method="slide").authoritative_changed
    # Workshop->Yard is traversable and supports slide, but *not* a fixture
    # eastward light-signal license. No arbitrary remote sensing follows.
    digest = app.authoritative_digest()
    result = app.look_direction("south")
    assert result.result_type == "directional_observation_unavailable"
    assert result.pre_state_digest == result.post_state_digest == digest


def _installed(commands: tuple[str, ...], *args: str):
    binary = shutil.which("myravant-play")
    assert binary is not None, "CI must run the installed Myravant player"
    return subprocess.run(
        [binary, *args],
        input="\n".join((*commands, "exit", "")),
        capture_output=True, text=True, timeout=60,
    )


def _trace(path):
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["record_type"] == "session_start"
    assert rows[-1]["record_type"] == "session_end"
    assert rows[-1]["evidence_complete"] is True
    return [row for row in rows if row["record_type"] == "interaction"]


@pytest.mark.parametrize("method", ("throw", "push", "carry_drop", "unlit_push"))
def test_installed_play_alt_methods_sensing_and_v5_restore(tmp_path, method):
    identical = []
    for label in ("alpha", "beta"):
        checkpoint = tmp_path / f"{method}-{label}.json"
        trace = tmp_path / f"{method}-{label}.jsonl"
        attempts = (*_method_sequence(method), "look east", "save")
        run = _installed(
            attempts, "--checkpoint", str(checkpoint),
            "--trace", str(trace), "--repository-sha", "f" * 40,
        )
        assert run.returncode == 0, (run.stdout, run.stderr)
        rows = _trace(trace)
        assert len(rows) == len(attempts)
        assert [r["raw_player_input"] for r in rows] == [
            s + "\n" for s in attempts
        ]
        assert all(
            row["authoritative_changed"] and row["receipt_id"]
            for row in rows[:-2]
        ), rows
        sensing = rows[-2]
        assert sensing["parsed_action"] == "look_direction"
        assert sensing["authoritative_changed"] is False
        assert sensing["pre_state_digest"] == sensing["post_state_digest"]
        if method == "unlit_push":
            assert sensing["result_type"] == "directional_observation_unavailable"
            assert sensing["failure_class"] == "directional_observation_unlicensed"
        else:
            assert sensing["result_type"] == "directional_light_signal"
            assert sensing["player_visible_output"].strip() == SIGNAL
            assert sensing["observation_evidence_id"]
        assert rows[-1]["result_type"] == "checkpoint_written"
        assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
        restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert restored.authoritative_digest() == rows[-1]["post_state_digest"]
        _assert_readonly_glimmer(restored, expected=(method != "unlit_push"))
        before = checkpoint.read_bytes()
        resumed = _installed(
            ("look east", "save"),
            "--load", str(checkpoint), "--checkpoint", str(checkpoint),
        )
        assert resumed.returncode == 0, (resumed.stdout, resumed.stderr)
        assert checkpoint.read_bytes() == before
        if method == "unlit_push":
            assert SIGNAL not in resumed.stdout
        else:
            assert SIGNAL in resumed.stdout
        identical.append((
            [(row["parsed_action"], row["result_type"],
              row["failure_class"], row["pre_state_digest"],
              row["post_state_digest"]) for row in rows],
            checkpoint.read_bytes(),
        ))
    assert identical[0] == identical[1]


def _prompt(stdout):
    output = ""
    while not output.endswith("\n> "):
        char = stdout.read(1)
        assert char, ("Installed player closed before next decision", output)
        output += char
        assert len(output) < 30000
    return output


@pytest.mark.parametrize("carried", (False, True), ids=("ground", "carried"))
def test_live_player_selects_distinct_physical_method_from_actual_state(
    tmp_path, carried,
):
    outcomes = []
    for label in ("alpha", "beta"):
        checkpoint = tmp_path / f"{label}.json"
        trace = tmp_path / f"{label}.jsonl"
        setup = (
            ("pickup lantern", "light lantern", "move south", "save")
            if carried else
            ("light lantern", "slide lantern south", "move south", "save")
        )
        seeded = _installed(setup, "--checkpoint", str(checkpoint))
        assert seeded.returncode == 0, (seeded.stdout, seeded.stderr)

        binary = shutil.which("myravant-play")
        process = subprocess.Popen(
            [
                binary, "--load", str(checkpoint),
                "--checkpoint", str(checkpoint),
                "--trace", str(trace), "--repository-sha", "f" * 40,
            ],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1,
        )
        assert process.stdin and process.stdout and process.stderr
        actions = []
        try:
            _prompt(process.stdout)

            def act(phrase):
                process.stdin.write(phrase + "\n")
                process.stdin.flush()
                actions.append(phrase)
                return _prompt(process.stdout)

            self_view = act("inspect myself")
            if "Carrying: Brass Lantern." in self_view:
                method = "throw lantern east"
            else:
                # The player cannot deduce ground location from not carrying;
                # it observes the current scene before choosing ground contact.
                visible = act("look")
                assert "Brass Lantern" in visible, visible
                method = "push lantern east"
            assert method == (
                "throw lantern east" if carried else "push lantern east"
            )
            action_output = act(method)
            assert (
                "You throw the Brass Lantern east." in action_output
                if carried else "You push the Brass Lantern east." in action_output
            )
            signal = act("look east")
            assert SIGNAL in signal
            assert "Orchard Path" not in signal
            assert "Checkpoint written." in act("save")
            process.stdin.write("exit\n")
            process.stdin.flush()
            process.stdin.close()
            remainder = process.stdout.read()
            code = process.wait(timeout=45)
            assert code == 0, (actions, remainder, process.stderr.read())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)

        rows = _trace(trace)
        assert [r["raw_player_input"] for r in rows] == [
            a + "\n" for a in actions
        ]
        assert rows[0]["parsed_action"] == "inspect"
        assert not rows[0]["authoritative_changed"]
        assert rows[0]["pre_state_digest"] == rows[0]["post_state_digest"]
        index = 2 if method.startswith("push") else 1
        if index == 2:
            assert rows[1]["parsed_action"] == "look"
            assert not rows[1]["authoritative_changed"]
        assert rows[index]["parsed_action"] in {"push", "throw"}
        assert rows[index]["authoritative_changed"] is True
        assert rows[index]["receipt_id"] and rows[index]["state_delta_id"]
        seen = rows[index + 1]
        assert seen["parsed_action"] == "look_direction"
        assert seen["result_type"] == "directional_light_signal"
        assert not seen["authoritative_changed"]
        assert seen["pre_state_digest"] == seen["post_state_digest"]
        assert rows[-1]["result_type"] == "checkpoint_written"
        restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert restored.authoritative_digest() == rows[-1]["post_state_digest"]
        _assert_readonly_glimmer(restored, expected=True)
        outcomes.append((
            tuple(actions),
            tuple((r["parsed_action"], r["result_type"],
                   r["pre_state_digest"], r["post_state_digest"]) for r in rows),
            checkpoint.read_bytes(),
        ))
    assert outcomes[0] == outcomes[1]
