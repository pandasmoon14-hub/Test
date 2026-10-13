"""Installed-client proof of actor-local factual inquiry and method alternatives.

This package does not infer NPC memory or visual knowledge from world truth.
Every answer is read-only, while handoff/movement keep their existing owners.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.myravant_situated_inquiry import (
    execute_situated_inquiry,
    parse_situated_inquiry,
)
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_terminal_capabilities import (
    execute_bounded_terminal_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@pytest.mark.parametrize(
    ("phrase", "kind", "object_reference"),
    (
        ("ask groundskeeper if he has lantern", "own_custody", "lantern"),
        ("I ask the groundskeeper whether they are carrying the lantern",
         "own_custody", "lantern"),
        ("ask groundskeeper if you are holding chest?", "own_custody", "chest"),
        ("ask groundskeeper do you have lantern", "own_custody", "lantern"),
        ("ask groundskeeper where is the lantern?", "own_custody_location", "lantern"),
        ("ask groundskeeper where the lantern is", "own_custody_location", "lantern"),
        ("ask groundskeeper what are you carrying?", "own_inventory", None),
        ("ask groundskeeper if you are following me?", "own_follow_intent", None),
        ("ask groundskeeper are you following me?", "own_follow_intent", None),
        ("ask groundskeeper whether lantern is in the chest",
         "unattested", None),
        ("ask groundskeeper if he remembers the lantern", "unattested", None),
    ),
)
def test_inquiry_anatomy_retains_question_without_claiming_knowledge(
    phrase, kind, object_reference,
):
    parsed = parse_situated_inquiry(phrase + "\n")
    assert parsed.parsed
    assert parsed.raw_text == phrase + "\n"
    assert parsed.kind == kind
    assert parsed.object_reference == object_reference


@pytest.mark.parametrize(
    "phrase",
    (
        "ask groundskeeper for lantern",
        "ask groundskeeper to follow me",
        "ask groundskeeper to slide chest north",
        "give lantern to groundskeeper",
        "ask the town council for a charter",
        "ask someone if they have my cloak",
    ),
)
def test_existing_requests_are_not_taken_over_by_inquiry(phrase):
    assert parse_situated_inquiry(phrase).parsed is False


def _read_only(app, raw, expected_type):
    before = app.authoritative_digest()
    result = execute_situated_inquiry(app, raw)
    assert result.result_type == expected_type
    assert result.authoritative_changed is False
    assert result.command_id is None
    assert result.receipt_id is None
    assert result.state_delta_id is None
    assert result.pre_state_digest == result.post_state_digest == before
    assert app.authoritative_digest() == before
    return result


def _meet_with_lantern(app):
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed


def test_nonlocal_actor_cannot_disclose_presence_or_custody():
    app = MyravantVSM14Application.new()
    first = _read_only(
        app, "ask groundskeeper if he has lantern",
        "situated_inquiry_unavailable",
    )
    assert first.failure_class == "inquiry_actor_not_local"
    assert "not here" in first.message
    assert app.current_place_id() == app.fixture.player_entity_id or (
        app.fixture.place_presentation(app.current_place_id()).name == "Workshop"
    )


def test_grounded_current_custody_changes_with_handoff_and_return():
    app = MyravantVSM14Application.new()
    _meet_with_lantern(app)
    before = _read_only(
        app, "ask groundskeeper if he has lantern",
        "situated_inquiry_answered",
    )
    assert '"No, I am not carrying that."' in before.message

    unknown = _read_only(
        app, "ask groundskeeper where the lantern is",
        "situated_inquiry_unknown",
    )
    assert unknown.failure_class == "inquiry_location_unattested"
    # Query cannot look through the player's hands, despite global state.
    assert "cannot verify" in unknown.message

    transfer = app.give_object("lantern", "groundskeeper")
    assert transfer.authoritative_changed
    assert transfer.receipt_id and transfer.state_delta_id
    with_actor = _read_only(
        app, "ask the groundskeeper whether they are carrying the lantern",
        "situated_inquiry_answered",
    )
    assert '"Yes, I am carrying that."' in with_actor.message
    whereabouts = _read_only(
        app, "ask groundskeeper where is lantern",
        "situated_inquiry_answered",
    )
    assert "with me" in whereabouts.message
    inventory = _read_only(
        app, "ask groundskeeper what are you carrying",
        "situated_inquiry_answered",
    )
    assert "Brass Lantern" in inventory.message

    restored_custody = app.request_object_from_actor("groundskeeper", "lantern")
    assert restored_custody.authoritative_changed
    assert restored_custody.receipt_id and restored_custody.state_delta_id
    after = _read_only(
        app, "ask groundskeeper if he is holding lantern",
        "situated_inquiry_answered",
    )
    assert '"No, I am not carrying that."' in after.message
    empty = _read_only(
        app, "ask groundskeeper what are you carrying",
        "situated_inquiry_answered",
    )
    assert "carrying nothing" in empty.message


def test_actor_follow_intent_is_current_state_not_invented_promise(tmp_path):
    checkpoint = tmp_path / "follow-inquiry.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed
    before = _read_only(
        app, "ask groundskeeper if you are following me",
        "situated_inquiry_answered",
    )
    assert "No, I am not following you." in before.message
    activate = execute_bounded_terminal_request(
        app, "ask groundskeeper to follow me"
    )
    assert activate is not None
    assert activate[1].authoritative_changed
    followed = _read_only(
        app, "ask groundskeeper if you are following me",
        "situated_inquiry_answered",
    )
    assert "Yes, I am following you." in followed.message
    assert app.move("north").authoritative_changed
    after_move = _read_only(
        app, "ask groundskeeper are you following me",
        "situated_inquiry_answered",
    )
    assert "Yes, I am following you." in after_move.message
    assert app.save().result_type == "checkpoint_written"
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    replay = _read_only(
        restored, "ask groundskeeper if you are following me",
        "situated_inquiry_answered",
    )
    assert replay.message == after_move.message
    stop = execute_bounded_terminal_request(
        app, "ask groundskeeper to stop following me"
    )
    assert stop is not None
    assert stop[1].authoritative_changed
    after = _read_only(
        app, "ask groundskeeper are you following me",
        "situated_inquiry_answered",
    )
    assert "No, I am not following you." in after.message


def test_unknown_and_foreign_facts_do_not_use_global_truth():
    app = MyravantVSM14Application.new()
    _meet_with_lantern(app)
    assert app.give_object("lantern", "groundskeeper").authoritative_changed
    for phrase in (
        "ask groundskeeper whether lantern is in the chest",
        "ask groundskeeper if he remembers the lantern",
        "ask groundskeeper if the waystone is near workshop",
    ):
        result = _read_only(app, phrase, "situated_inquiry_unknown")
        assert result.failure_class == "inquiry_fact_unattested"
    invalid = _read_only(
        app, "ask groundskeeper do you have dragonstone",
        "situated_inquiry_unknown",
    )
    assert invalid.failure_class == "inquiry_object_unqualified"


def test_bounded_route_precedes_legacy_only_for_questions():
    app = MyravantVSM14Application.new()
    route = execute_bounded_terminal_request(
        app, "ask groundskeeper if he has lantern"
    )
    assert route is not None and route[0] == "situated_inquiry"
    assert route[1].failure_class == "inquiry_actor_not_local"
    assert execute_bounded_terminal_request(
        app, "ask groundskeeper for lantern"
    ) is None
    legacy = parse_terminal_command("ask groundskeeper for lantern")
    assert legacy.action == "request_handoff"
    # The separate institutional misroute (#490) remains recorded pressure.
    assert parse_terminal_command("ask the town council for a charter").action == (
        "request_handoff"
    )


def _run(commands, *flags):
    binary = shutil.which("myravant-play")
    assert binary is not None, "CI must test the installed player client"
    return subprocess.run(
        [binary, *flags],
        input="\n".join((*commands, "exit", "")),
        text=True,
        capture_output=True,
        timeout=60,
    )


def _rows(path):
    data = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
    assert data[0]["record_type"] == "session_start"
    assert data[-1]["record_type"] == "session_end"
    assert data[-1]["evidence_complete"] is True
    return [item for item in data if item["record_type"] == "interaction"]


def test_installed_client_player_adapts_inquiry_to_handoff_and_save(tmp_path):
    checkpoint = tmp_path / "world.json"
    trace = tmp_path / "first.jsonl"
    cmds = (
        "ask groundskeeper if he has the lantern",
        "pickup lantern",
        "move south",
        "move south",
        "ask groundskeeper where the lantern is",
        "give lantern to groundskeeper",
        "ask groundskeeper if he has the lantern",
        "ask groundskeeper what are you carrying",
        "ask groundskeeper for lantern",
        "ask groundskeeper if he has the lantern",
        "save",
    )
    result = _run(
        cmds, "--checkpoint", str(checkpoint), "--trace", str(trace),
        "--repository-sha", "f" * 40,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    rows = _rows(trace)
    assert len(rows) == len(cmds)
    assert [r["parsed_action"] for r in rows] == [
        "situated_inquiry", "pickup", "move", "move",
        "situated_inquiry", "handoff", "situated_inquiry",
        "situated_inquiry", "request_handoff", "situated_inquiry", "save",
    ]
    assert rows[0]["failure_class"] == "inquiry_actor_not_local"
    assert rows[4]["failure_class"] == "inquiry_location_unattested"
    assert rows[5]["authoritative_changed"] and rows[5]["receipt_id"]
    assert rows[8]["authoritative_changed"] and rows[8]["receipt_id"]
    for i in (0, 4, 6, 7, 9):
        assert rows[i]["authoritative_changed"] is False
        assert rows[i]["pre_state_digest"] == rows[i]["post_state_digest"]
        assert rows[i]["receipt_id"] is None
    assert "Yes, I am carrying that." in rows[6]["player_visible_output"]
    assert "Brass Lantern" in rows[7]["player_visible_output"]
    assert "No, I am not carrying that." in rows[9]["player_visible_output"]
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5

    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    digest = restored.authoritative_digest()
    reread = _read_only(
        restored, "ask groundskeeper what are you carrying",
        "situated_inquiry_answered",
    )
    assert "carrying nothing" in reread.message
    assert restored.authoritative_digest() == digest
    bytes_before = checkpoint.read_bytes()
    second_trace = tmp_path / "resume.jsonl"
    second = _run(
        ("ask groundskeeper if he has lantern", "save"),
        "--load", str(checkpoint), "--checkpoint", str(checkpoint),
        "--trace", str(second_trace), "--repository-sha", "f" * 40,
    )
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert checkpoint.read_bytes() == bytes_before
    resumed = _rows(second_trace)
    assert resumed[0]["result_type"] == "situated_inquiry_answered"
    assert resumed[0]["pre_state_digest"] == resumed[0]["post_state_digest"] == digest
