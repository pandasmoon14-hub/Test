"""Feedback-conditioned goal completion, not merely new inquiry syntax.

Two lawful saved situations differ only in who presently controls the lantern.
The installed-player policy must read the Groundskeeper's answer and choose
between a voluntary handoff and ground pickup, then carry *and light* the
lantern at the dark Orchard Path. The question itself makes no state change.

Neutral fixture only. No NPC memory, omniscient answers, or generated world.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID,
    LANTERN_ID,
    ORCHARD_PATH_ID,
)
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _binary() -> str:
    executable = shutil.which("myravant-play")
    assert executable is not None, "Exercise the actual installed client"
    return executable


def _prompt(stdout):
    response = ""
    while not response.endswith("\n> "):
        character = stdout.read(1)
        assert character, ("Installed terminal closed before next prompt", response)
        response += character
        assert len(response) < 30000, "Unbounded terminal response"
    return response


def _events(path):
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    assert records[-1]["evidence_complete"] is True
    return [record for record in records if record["record_type"] == "interaction"]


def _seed(checkpoint, *, held_by_npc):
    # Construct state lawfully through the normal installed client.
    # NPC-held: player -> Groundskeeper. Other case: dropped in Gatehouse.
    action = "give lantern to groundskeeper" if held_by_npc else "drop lantern"
    commands = ("pickup lantern", "move south", "move south", action, "save")
    completed = subprocess.run(
        [_binary(), "--checkpoint", str(checkpoint)],
        input="\n".join((*commands, "exit", "")),
        text=True, capture_output=True, timeout=45,
    )
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert "Checkpoint written." in completed.stdout
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5

    app = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert app.fixture.place_presentation(app.current_place_id()).name == "Gatehouse"
    carrying = app.fixture.public_entities_carried_by(
        app.state.representation, GROUNDSKEEPER_ID
    )
    assert (LANTERN_ID in {item.entity_id for item in carrying}) is held_by_npc


def _play_feedback_conditioned(checkpoint, trace):
    # The goal is the same irrespective of the saved custody relation.
    # The policy cannot inspect the hidden branch flag; it uses the live answer.
    process = subprocess.Popen(
        [
            _binary(), "--load", str(checkpoint),
            "--checkpoint", str(checkpoint),
            "--trace", str(trace), "--repository-sha", "f" * 40,
        ],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=1,
    )
    assert process.stdin and process.stdout and process.stderr
    commands = []
    responses = []
    try:
        _prompt(process.stdout)

        def act(command):
            process.stdin.write(command + "\n")
            process.stdin.flush()
            commands.append(command)
            response = _prompt(process.stdout)
            responses.append(response)
            return response

        # New held-out expression, not one of the inquiry-unit-test phrases.
        question = "I ask the groundskeeper whether he is carrying the lantern"
        assert parse_terminal_command(question).action == "unsupported"
        answer = act(question)
        if 'Yes, I am carrying that.' in answer:
            chosen = "ask groundskeeper for lantern"
        elif 'No, I am not carrying that.' in answer:
            # NPC self-custody does not establish an object's location.
            # The player must use its own visible scene before pickup.
            sighting = act("look")
            assert "Brass Lantern" in sighting, sighting
            chosen = "pickup lantern"
        else:
            pytest.fail("The inquiry did not provide a grounded actionable answer")

        obtained = act(chosen)
        assert (
            ("hands you" in obtained) if chosen.startswith("ask")
            else ("pick up" in obtained.lower())
        ), obtained
        light = act("light lantern")
        assert "You light the Brass Lantern." in light, light
        assert "Yard" in act("move north")
        assert "Orchard Path" in act("move east")
        viewed = act("look")
        assert "Orchard Path" in viewed
        assert "Checkpoint written." in act("save")
        process.stdin.write("exit\n")
        process.stdin.flush()
        process.stdin.close()
        remaining = process.stdout.read()
        code = process.wait(timeout=45)
        errors = process.stderr.read()
        assert code == 0, (commands, remaining, errors)
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10)

    rows = _events(trace)
    assert len(rows) == len(commands) == (
        7 if chosen.startswith("ask") else 8
    )
    assert [row["raw_player_input"] for row in rows] == [
        command + "\n" for command in commands
    ]
    assert rows[0]["parsed_action"] == "situated_inquiry"
    assert rows[0]["result_type"] == "situated_inquiry_answered"
    assert rows[0]["failure_class"] is None
    assert rows[0]["authoritative_changed"] is False
    assert rows[0]["pre_state_digest"] == rows[0]["post_state_digest"]
    assert rows[0]["receipt_id"] is None
    acquisition_index = 1 if chosen.startswith("ask") else 2
    if acquisition_index == 2:
        assert rows[1]["parsed_action"] == "look"
        assert rows[1]["authoritative_changed"] is False
        assert rows[1]["pre_state_digest"] == rows[1]["post_state_digest"]
        assert rows[1]["receipt_id"] is None
    acquisition = rows[acquisition_index]
    assert acquisition["authoritative_changed"] is True
    assert acquisition["receipt_id"] and acquisition["state_delta_id"]
    assert acquisition["parsed_action"] in {"request_handoff", "pickup"}
    for i in range(acquisition_index + 1, acquisition_index + 4):
        assert rows[i]["authoritative_changed"], (i, rows[i])
        assert rows[i]["receipt_id"], (i, rows[i])
    viewed = rows[acquisition_index + 4]
    assert viewed["parsed_action"] == "look"
    assert viewed["authoritative_changed"] is False
    assert viewed["pre_state_digest"] == viewed["post_state_digest"]
    assert rows[-1]["result_type"] == "checkpoint_written"

    app = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert app.authoritative_digest() == rows[-1]["post_state_digest"]
    assert app.current_place_id() == ORCHARD_PATH_ID
    carrying = app.fixture.public_entities_carried_by(
        app.state.representation, app.fixture.player_entity_id
    )
    assert LANTERN_ID in {item.entity_id for item in carrying}
    assert app.object_lit_state(LANTERN_ID).state == "lit"
    # The dark-path visual signal is qualified by the actually lit lantern.
    assert app.visual_observation_evidence(LANTERN_ID).observable is True

    saved_bytes = checkpoint.read_bytes()
    verified = subprocess.run(
        [_binary(), "--load", str(checkpoint), "--checkpoint", str(checkpoint)],
        input="inspect myself\nlook\nsave\nexit\n",
        text=True, capture_output=True, timeout=45,
    )
    assert verified.returncode == 0, (verified.stdout, verified.stderr)
    assert "Orchard Path" in verified.stdout
    assert checkpoint.read_bytes() == saved_bytes
    return {
        "commands": tuple(commands),
        "goal_state_digest": app.authoritative_digest(),
        "transitions": tuple(
            (row["parsed_action"], row["result_type"],
             row["failure_class"], row["authoritative_changed"],
             row["pre_state_digest"], row["post_state_digest"])
            for row in rows
        ),
    }


@pytest.mark.parametrize("held_by_npc", [False, True], ids=["grounded", "npc_held"])
def test_player_changes_method_from_live_answer_and_completes_same_goal(
    tmp_path, held_by_npc,
):
    outcomes = []
    for trial in ("alpha", "beta"):
        checkpoint = tmp_path / f"{trial}.json"
        trace = tmp_path / f"{trial}.jsonl"
        _seed(checkpoint, held_by_npc=held_by_npc)
        outcome = _play_feedback_conditioned(checkpoint, trace)
        assert outcome["commands"][1:3] == (
            ("ask groundskeeper for lantern", "light lantern")
            if held_by_npc else ("look", "pickup lantern")
        )
        outcomes.append(outcome)
    # Same initial state and player policy => identical committed history.
    assert outcomes[0] == outcomes[1]
