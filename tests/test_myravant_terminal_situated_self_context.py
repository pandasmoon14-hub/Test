"""Actor-local public self-observation composes existing location/custody state.

The player receives only facts already owned by the current scene and immediate
carrying relation. No anatomy, injuries, abilities, personality, omniscient
knowledge or new authoritative state is created by the observation.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _run(commands: tuple[str, ...], *args: str):
    binary = shutil.which("myravant-play")
    assert binary is not None, "CI must test the actually installed client"
    return subprocess.run(
        [binary, *args],
        input="\n".join((*commands, "exit", "")),
        capture_output=True,
        text=True,
        timeout=45,
    )


def _interactions(path):
    records = [
        json.loads(row)
        for row in path.read_text(encoding="utf-8").splitlines()
    ]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    assert records[-1]["evidence_complete"] is True
    return [row for row in records if row["record_type"] == "interaction"]


@pytest.mark.parametrize(
    ("phrase", "route", "target"),
    (
        ("inspect myself", "inspect", "myself"),
        ("examine self", "inspect", "self"),
        ("inspect me", "inspect", "me"),
        ("look at myself", "inspect", "myself"),
        ("inventory", "inspect_self", None),
        ("check inventory", "inspect_self", None),
        ("my inventory", "inspect_self", None),
        ("I inspect myself", "inspect", "myself"),
    ),
)
def test_existing_grammar_reuses_qualified_self_observation(phrase, route, target):
    parsed = parse_terminal_command(phrase + "\n")
    assert parsed.action == route
    assert parsed.argument == target
    assert parsed.raw_text == phrase + "\n"


def test_player_self_view_updates_from_existing_authoritative_owners():
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    first = app.inspect("myself")
    assert first.result_type == "self_inspection"
    assert first.view is not None
    assert first.view.name == "Traveler"
    assert first.view.description == (
        "Current place: Workshop.\nCarrying: nothing.\nRecorded posture: unrecorded."
    )
    assert first.pre_state_digest == first.post_state_digest == before
    assert app.authoritative_digest() == before

    assert app.pickup("lantern").authoritative_changed
    held = app.inspect("self")
    assert "Current place: Workshop." in held.view.description
    assert "Carrying: Brass Lantern." in held.view.description
    assert held.pre_state_digest == held.post_state_digest == app.authoritative_digest()

    assert app.move("south").authoritative_changed
    after_move = app.inspect("me")
    assert "Current place: Yard." in after_move.view.description
    assert "Carrying: Brass Lantern." in after_move.view.description
    assert after_move.pre_state_digest == after_move.post_state_digest

    assert app.move("south").authoritative_changed
    assert app.give_object("lantern", "groundskeeper").authoritative_changed
    handed_over = app.inspect("self")
    assert "Current place: Gatehouse." in handed_over.view.description
    assert "Carrying: nothing." in handed_over.view.description
    assert handed_over.pre_state_digest == handed_over.post_state_digest
    assert "Brass Lantern" not in handed_over.view.description


def test_unqualified_bodily_inference_or_third_party_is_not_self_projection():
    app = MyravantVSM14Application.new()
    initial = app.authoritative_digest()
    for target in (
        "my wounds", "my appearance", "my body", "my strength",
        "the groundskeeper", "everyone", "the traveler's hidden memory",
    ):
        result = app.inspect(target)
        assert result.result_type == "inspection_unavailable", target
        assert result.authoritative_changed is False
        assert result.pre_state_digest == result.post_state_digest == initial
    assert app.authoritative_digest() == initial


def test_installed_play_self_observation_crosses_movement_custody_and_resume(tmp_path):
    checkpoint = tmp_path / "campaign.json"
    trace = tmp_path / "campaign.jsonl"
    attempts = (
        "inspect myself",
        "inventory",
        "pickup lantern",
        "check inventory",
        "move south",
        "look at myself",
        "move south",
        "inspect me",
        "give lantern to groundskeeper",
        "inventory",
        "save",
    )
    first = _run(
        attempts, "--checkpoint", str(checkpoint),
        "--trace", str(trace), "--repository-sha", "f" * 40,
    )
    assert first.returncode == 0, (first.stdout, first.stderr)
    rows = _interactions(trace)
    assert len(rows) == len(attempts)
    assert [row["parsed_action"] for row in rows] == [
        "inspect", "inspect_self", "pickup", "inspect_self", "move",
        "inspect", "move", "inspect", "handoff", "inspect_self", "save",
    ]
    inspections = [row for row in rows if row["result_type"] == "self_inspection"]
    assert len(inspections) == 6
    assert all(
        row["authoritative_changed"] is False
        and row["pre_state_digest"] == row["post_state_digest"]
        for row in inspections
    )
    assert "Current place: Workshop." in inspections[0]["player_visible_output"]
    assert "Carrying: nothing." in inspections[0]["player_visible_output"]
    assert "Carrying: Brass Lantern." in inspections[2]["player_visible_output"]
    assert "Current place: Yard." in inspections[3]["player_visible_output"]
    assert "Current place: Gatehouse." in inspections[4]["player_visible_output"]
    assert "Carrying: nothing." in inspections[5]["player_visible_output"]

    app = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    saved_digest = app.authoritative_digest()
    assert saved_digest == rows[-1]["post_state_digest"]
    saved_bytes = checkpoint.read_bytes()

    restored_trace = tmp_path / "restored.jsonl"
    restart = _run(
        ("look at myself", "check inventory", "save"),
        "--load", str(checkpoint), "--checkpoint", str(checkpoint),
        "--trace", str(restored_trace), "--repository-sha", "f" * 40,
    )
    assert restart.returncode == 0, (restart.stdout, restart.stderr)
    reread = _interactions(restored_trace)
    assert [x["result_type"] for x in reread] == [
        "self_inspection", "self_inspection", "checkpoint_written",
    ]
    assert all(x["pre_state_digest"] == x["post_state_digest"] == saved_digest for x in reread)
    assert checkpoint.read_bytes() == saved_bytes
    assert "Current place: Gatehouse." in restart.stdout
    assert "Carrying: nothing." in restart.stdout


def test_nonself_petition_and_real_handoff_remain_distinct_without_state_change(tmp_path):
    trace = tmp_path / "refusal.jsonl"
    run = _run(
        (
            "ask the town council for a charter",
            "ask groundskeeper for lantern",
            "inspect my wounds",
        ),
        "--trace", str(trace),
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    rows = _interactions(trace)
    assert [x["parsed_action"] for x in rows] == [
        "institutional_petition", "request_handoff", "inspect",
    ]
    assert rows[0]["failure_class"] == "institutional_petition_unqualified"
    assert rows[0]["receipt_id"] is None
    assert rows[1]["result_type"] == "actor_object_handoff_rejected"
    assert rows[2]["failure_class"] == "inspection_target_unavailable"
    assert all(
        x["authoritative_changed"] is False
        and x["pre_state_digest"] == x["post_state_digest"]
        for x in rows
    )
