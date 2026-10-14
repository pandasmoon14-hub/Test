"""PLAY-COOPERATIVE-GOAL-1: a real local goal through alternate agents/methods.

The actor chooses only among existing owner-qualified physical operations. No
new social autonomy, invented authority, game rules or hidden NPC knowledge.
Source-pressure inspiration: bounded action stages and behavior selections;
this file copies no foreign engine code or game content.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_object_displacement import (
    replay_persistent_world_object_displacement,
)
from astra_runtime.myravant_cooperative_delivery_goal import (
    parse_cooperative_delivery_goal,
    parse_institutional_petition,
)
from astra_runtime.myravant_play_fixture import (
    GROUNDSKEEPER_ID, LANTERN_ID, ORCHARD_PATH_ID, PLAYER_ID, YARD_ID,
)
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_terminal_capabilities import (
    execute_bounded_terminal_request,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_vsm14_terminal import execute_vsm14_terminal_input


def _groundkeeper_to_workshop():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed
    assert execute_vsm14_terminal_input(
        app, "ask groundskeeper to follow me",
    ).result.authoritative_changed
    assert app.move("north").world_process_outcome == "committed"
    assert app.move("north").world_process_outcome == "committed"
    assert app.entity_place_id(GROUNDSKEEPER_ID) == app.current_place_id()
    return app


def _in_yard(method):
    app = _groundkeeper_to_workshop()
    if method == "ground":
        moved = app.displace_object("lantern", "south", method="slide")
        assert moved.authoritative_changed and moved.receipt_id
    elif method == "custody":
        moved = execute_vsm14_terminal_input(
            app, "ask groundskeeper to pick up lantern",
        ).result
        assert moved.authoritative_changed and moved.receipt_id
    else:
        raise AssertionError(method)
    assert app.move("south").world_process_outcome == "committed"
    assert app.current_place_id() == YARD_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    return app


def _place_of(app, entity_id):
    rows = [
        r for r in app.state.representation.relations
        if r.subject_entity_id == entity_id and
        r.relation_type == LOCATED_AT_RELATION_TYPE
    ]
    return rows[0].object_entity_id if len(rows) == 1 else None


@pytest.mark.parametrize("spoken", [
    "ask groundskeeper to bring lantern to orchard",
    "I ask the groundskeeper to get the brass lantern to the orchard path",
    "request groundskeeper to move lantern to orchard",
    "ask groundskeeper to take the lantern to orchard path",
])
def test_goal_variations_classify_without_claiming_universal_nlp(spoken):
    assert parse_cooperative_delivery_goal(spoken)
    assert not parse_institutional_petition(spoken)
    assert not parse_cooperative_delivery_goal("ask groundskeeper to build a home")
    assert not parse_cooperative_delivery_goal("ask groundskeeper to move it there")


@pytest.mark.parametrize(("method", "expected_owner_method"), [
    ("ground", "push"),
    ("custody", "throw"),
])
def test_same_player_goal_selects_different_existing_owner_method(method, expected_owner_method):
    app = _in_yard(method)
    before = app.state.representation
    digest = app.authoritative_digest()

    routed = execute_bounded_terminal_request(
        app, "ask groundskeeper to bring lantern to orchard",
    )
    assert routed is not None
    route, result = routed
    assert route == "cooperative_delivery_goal"
    assert result.authoritative_changed and result.receipt_id
    assert result.command_id and result.state_delta_id
    assert result.post_state_digest != digest
    receipt = app.runtime_state.committed_object_displacement_transitions[-1].receipt
    assert receipt.actor_entity_id == GROUNDSKEEPER_ID
    assert receipt.object_entity_id == LANTERN_ID
    assert receipt.method == expected_owner_method
    assert receipt.destination_place_id == ORCHARD_PATH_ID
    assert _place_of(app, LANTERN_ID) == ORCHARD_PATH_ID
    assert replay_persistent_world_object_displacement(
        pre_state_representation=before, receipt=receipt,
    ) == app.state.representation

    # The same goal is now unavailable, not silently a second successful
    # transfer or knowledge of the remotely situated lantern.
    settled = app.authoritative_digest()
    refused = execute_bounded_terminal_request(
        app, "ask groundskeeper to bring lantern to orchard",
    )
    assert refused is not None and refused[0] == "cooperative_delivery_goal"
    assert refused[1].failure_class == "cooperative_goal_opportunity_unavailable"
    assert not refused[1].authoritative_changed
    assert app.authoritative_digest() == settled


def test_player_can_pursue_same_goal_with_separate_attributed_owner_action():
    app = MyravantVSM14Application.new()
    assert app.displace_object("lantern", "south", method="slide").authoritative_changed
    assert app.move("south").authoritative_changed
    pre = app.state.representation
    result = app.displace_object("lantern", "east", method="push")
    assert result.authoritative_changed and result.receipt_id
    receipt = app.runtime_state.committed_object_displacement_transitions[-1].receipt
    assert receipt.actor_entity_id == PLAYER_ID
    assert receipt.method == "push"
    assert receipt.object_entity_id == LANTERN_ID
    assert _place_of(app, LANTERN_ID) == ORCHARD_PATH_ID
    assert replay_persistent_world_object_displacement(
        pre_state_representation=pre, receipt=receipt,
    ) == app.state.representation


def test_refusals_do_not_disclose_remote_truth_or_commit():
    app = MyravantVSM14Application.new()
    initial = app.authoritative_digest()
    distant = execute_bounded_terminal_request(
        app, "ask groundskeeper to bring lantern to orchard",
    )
    assert distant is not None
    assert distant[1].failure_class == "cooperative_goal_actor_not_local"
    assert distant[1].pre_state_digest == distant[1].post_state_digest == initial
    assert not distant[1].authoritative_changed

    # A player-controlled lantern cannot be silently delegated as though
    # held by the Groundskeeper, despite both actors being co-located.
    app = _in_yard("ground")
    assert app.pickup("lantern").authoritative_changed
    before = app.authoritative_digest()
    denied = execute_bounded_terminal_request(
        app, "request groundskeeper to take lantern to orchard",
    )
    assert denied is not None
    assert denied[1].failure_class == "cooperative_goal_opportunity_unavailable"
    assert denied[1].receipt_id is None
    assert app.authoritative_digest() == before


@pytest.mark.parametrize("words", (
    "ask the town council for a charter",
    "ask town council for charter",
    "petition the assembly for permission",
))
def test_institutional_petition_is_not_object_handoff_or_canon(words):
    assert parse_institutional_petition(words)
    app = MyravantVSM14Application.new()
    digest = app.authoritative_digest()
    route, result = execute_bounded_terminal_request(app, words)
    assert route == "institutional_petition"
    assert result.failure_class == "institutional_petition_unqualified"
    assert not result.authoritative_changed
    assert result.receipt_id is None
    assert result.pre_state_digest == result.post_state_digest == digest
    assert app.authoritative_digest() == digest

    assert not parse_institutional_petition("ask groundskeeper for lantern")
    assert execute_bounded_terminal_request(
        app, "ask groundskeeper for lantern",
    ) is None
    assert parse_terminal_command("ask groundskeeper for lantern").action == "request_handoff"


def _installed(commands, *args):
    executable = shutil.which("myravant-play")
    assert executable is not None, "installed client required for the gameplay gate"
    return subprocess.run(
        [executable, *args],
        input="\n".join((*commands, "exit", "")),
        text=True, capture_output=True, timeout=90,
    )


def _trace(path):
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["record_type"] == "session_start"
    assert rows[-1]["record_type"] == "session_end"
    assert rows[-1]["evidence_complete"] is True
    return [r for r in rows if r["record_type"] == "interaction"]


@pytest.mark.parametrize(("method", "commands", "receipt_method"), [
    ("ground", (
        "slide lantern south", "move south", "move south",
        "ask groundskeeper to follow me", "move north",
        "ask groundskeeper to bring lantern to orchard",
    ), "push"),
    ("custody", (
        "move south", "move south", "ask groundskeeper to follow me",
        "move north", "move north", "ask groundskeeper to pick up lantern",
        "move south", "ask groundskeeper to bring lantern to orchard",
    ), "throw"),
])
def test_installed_goal_variation_v5_restore_and_repeated_determinism(
    method, commands, receipt_method, tmp_path,
):
    comparisons = []
    for repetition in ("alpha", "beta"):
        checkpoint = tmp_path / f"{method}-{repetition}.json"
        trace = tmp_path / f"{method}-{repetition}.jsonl"
        run = _installed(
            (*commands, "save"), "--checkpoint", str(checkpoint),
            "--trace", str(trace), "--repository-sha", "a" * 40,
        )
        assert run.returncode == 0, (run.stdout, run.stderr)
        assert "Groundskeeper" in run.stdout
        assert "Checkpoint written." in run.stdout
        rows = _trace(trace)
        assert len(rows) == len(commands) + 1
        assert [r["raw_player_input"] for r in rows[:-1]] == [
            line + "\n" for line in commands
        ]
        goal = rows[-2]
        assert goal["parsed_action"] == "cooperative_delivery_goal"
        assert goal["authoritative_changed"] is True
        assert goal["receipt_id"] and goal["state_delta_id"]
        assert goal["result_type"] == (
            "actor_mediated_ground_displacement_committed"
            if receipt_method == "push"
            else "actor_mediated_displacement_committed"
        )
        app = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert app.authoritative_digest() == rows[-1]["post_state_digest"]
        assert _place_of(app, LANTERN_ID) == ORCHARD_PATH_ID
        assert app.runtime_state.committed_object_displacement_transitions[-1].receipt.method == receipt_method
        raw = checkpoint.read_bytes()
        inspection = _installed(
            ("look", "save"), "--load", str(checkpoint),
            "--checkpoint", str(checkpoint),
        )
        assert inspection.returncode == 0, (inspection.stdout, inspection.stderr)
        assert checkpoint.read_bytes() == raw
        comparisons.append((
            tuple((r["parsed_action"], r["result_type"],
                   r["pre_state_digest"], r["post_state_digest"]) for r in rows),
            raw,
        ))
    assert comparisons[0] == comparisons[1]


def test_installed_petition_does_not_modify_world_or_hide_raw_input(tmp_path):
    trace = tmp_path / "petition.jsonl"
    run = _installed(
        ("ask the town council for a charter",),
        "--trace", str(trace), "--repository-sha", "a" * 40,
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    rows = _trace(trace)
    assert len(rows) == 1
    row = rows[0]
    assert row["raw_player_input"] == "ask the town council for a charter\n"
    assert row["parsed_action"] == "institutional_petition"
    assert row["failure_class"] == "institutional_petition_unqualified"
    assert row["pre_state_digest"] == row["post_state_digest"]
    assert not row["authoritative_changed"] and row["receipt_id"] is None
