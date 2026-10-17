"""Native environmental recovery by independently qualified drag versus carry.

The first drag fixture only licenses Weathered Waystone from Orchard to Yard.
This demonstrates meaningful alternative control/custody with RT-010 receipts,
AFQR-18/19 spatial opportunity, AFQR-20 situated sensing and v5 persistence.
It does not imply universal stone weight, force, friction or hand anatomy.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_object_displacement import (
    replay_persistent_world_object_displacement,
)
from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_fixture import (
    WAYSTONE_ID, LANTERN_ID, YARD_ID, ORCHARD_PATH_ID,
)
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@pytest.mark.parametrize(("raw", "action", "argument"), (
    ("drag waystone west", "drag", "waystone -> west"),
    ("I drag the weathered waystone west", "drag", "weathered waystone -> west"),
    ("haul waystone west", "drag", "waystone -> west"),
    ("drag it west", "ambiguous", "it"),
    ("drag waystone over the gate", "unsupported", "drag waystone over the gate"),
    ("pull waystone west", "unsupported", "pull waystone west"),
))
def test_drag_method_distinct_from_push_or_unqualified_pull(raw, action, argument):
    parsed = parse_terminal_command(raw)
    assert (parsed.action, parsed.argument) == (action, argument)


def _to_orchard_with_light(app):
    for op in (
        app.pickup("lantern"),
        app.light_object("lantern"),
        app.move("south"),
        app.move("east"),
    ):
        assert op.authoritative_changed and op.receipt_id
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert app.focused_observation("waystone").result_type == "focused_sighting"


def _stone_ground_at_yard(app):
    matches = [
        rel for rel in app.state.representation.relations
        if rel.subject_entity_id == WAYSTONE_ID
        and rel.relation_type in (LOCATED_AT_RELATION_TYPE, CARRIED_BY_RELATION_TYPE)
    ]
    assert len(matches) == 1
    assert matches[0].relation_type == LOCATED_AT_RELATION_TYPE
    assert matches[0].object_entity_id == YARD_ID


def test_new_ground_drag_has_true_commit_and_native_owner_replay():
    app = MyravantVSM14Application.new()
    _to_orchard_with_light(app)
    before = app.state.representation
    digest = app.authoritative_digest()

    drag = app.displace_object("waystone", "west", method="drag")
    assert drag.result_type == "object_displacement_committed"
    assert drag.message == "You drag the Weathered Waystone west."
    assert drag.authoritative_changed
    assert drag.pre_state_digest == digest
    assert drag.post_state_digest == app.authoritative_digest()
    assert drag.receipt_id and drag.state_delta_id
    assert drag.spatial_evidence_id and drag.opportunity_evidence_id
    _stone_ground_at_yard(app)
    receipt = app.runtime_state.committed_object_displacement_transitions[-1].receipt
    assert receipt.method == "drag"
    assert receipt.source_relation_type == LOCATED_AT_RELATION_TYPE
    assert receipt.destination_relation_type == LOCATED_AT_RELATION_TYPE
    assert replay_persistent_world_object_displacement(
        pre_state_representation=before, receipt=receipt,
    ) == app.state.representation

    now = app.authoritative_digest()
    missing = app.focused_observation("waystone")
    assert missing.result_type == "focused_observation_unavailable"
    assert missing.pre_state_digest == missing.post_state_digest == now
    repeat = app.displace_object("waystone", "west", method="drag")
    assert not repeat.authoritative_changed
    assert repeat.pre_state_digest == repeat.post_state_digest == now
    assert app.move("west").authoritative_changed
    sighting = app.focused_observation("waystone")
    assert sighting.result_type == "focused_sighting"
    assert sighting.pre_state_digest == sighting.post_state_digest
    _stone_ground_at_yard(app)


def test_unlit_contact_allows_ground_drag_without_confirming_remote_placement():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    assert app.move("east").authoritative_changed
    baseline = app.authoritative_digest()
    assert app.focused_observation("waystone").result_type == "focused_observation_unavailable"
    # CONTACT-1 supersedes the historical sight-only prerequisite. Darkness
    # still grants neither remote target access nor an unlicensed route.
    for target in ("lantern", "chest", "unknown trinket"):
        denied = app.displace_object(target, "west", method="drag")
        assert denied.result_type == "object_displacement_rejected"
        assert denied.failure_class == "object_displacement_target_unavailable"
        assert denied.receipt_id is None and denied.state_delta_id is None
        assert denied.pre_state_digest == denied.post_state_digest == baseline
    assert app.authoritative_digest() == baseline

    for result in (
        app.displace_object("waystone", "west", method="push"),
        app.displace_object("waystone", "east", method="drag"),
    ):
        assert not result.authoritative_changed
        assert result.pre_state_digest == result.post_state_digest == baseline
    assert app.authoritative_digest() == baseline

    contact = app.feel_for_local_object("waystone")
    assert contact.result_type == "player_contact_observed"
    moved = app.displace_object("waystone", "west", method="drag")
    assert moved.authoritative_changed and moved.receipt_id
    assert moved.observation_evidence_id == contact.observation_evidence_id
    _stone_ground_at_yard(app)
    after = app.authoritative_digest()
    stale = app.displace_object("waystone", "west", method="drag")
    assert stale.failure_class == "object_displacement_target_unavailable"
    assert stale.pre_state_digest == stale.post_state_digest == after
    assert app.authoritative_digest() == after


def test_waystone_carry_and_ground_drag_complete_same_world_goal():
    for method in ("carry", "drag"):
        app = MyravantVSM14Application.new()
        _to_orchard_with_light(app)
        if method == "carry":
            picked = app.pickup("waystone")
            assert picked.authoritative_changed and picked.receipt_id
            assert any(
                r.relation_type == CARRIED_BY_RELATION_TYPE
                and r.subject_entity_id == WAYSTONE_ID
                and r.object_entity_id == app.fixture.player_entity_id
                for r in app.state.representation.relations
            )
            assert app.move("west").authoritative_changed
            placed = app.drop("waystone")
            assert placed.authoritative_changed and placed.receipt_id
            assert not app.runtime_state.committed_object_displacement_transitions
        else:
            dragged = app.displace_object("waystone", "west", method="drag")
            assert dragged.authoritative_changed and dragged.receipt_id
            assert app.move("west").authoritative_changed
        _stone_ground_at_yard(app)
        observed = app.focused_observation("waystone")
        assert observed.result_type == "focused_sighting"
        assert observed.pre_state_digest == observed.post_state_digest


def _installed(commands, *args):
    binary = shutil.which("myravant-play")
    assert binary is not None, "Must test the installed terminal client"
    return subprocess.run(
        [binary, *args], input="\n".join((*commands, "exit", "")),
        text=True, capture_output=True, timeout=65,
    )


def _prompt(stdout):
    result = ""
    while not result.endswith("\n> "):
        char = stdout.read(1)
        assert char, ("player process ended before prompt", result)
        result += char
        assert len(result) < 30000
    return result


def _trace(path):
    records = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    assert records[-1]["evidence_complete"] is True
    return [r for r in records if r["record_type"] == "interaction"]


@pytest.mark.parametrize("carried", (False, True), ids=("ground_drag", "carry_drop"))
def test_installed_player_selects_custody_sensitive_recovery_after_observing(
    tmp_path, carried,
):
    comparable = []
    for trial in ("alpha", "beta"):
        checkpoint = tmp_path / f"{carried}-{trial}.json"
        trace = tmp_path / f"{carried}-{trial}.jsonl"
        seed = (
            "pickup lantern", "light lantern",
            "move south", "move east",
            *(("pickup waystone",) if carried else ()),
            "save",
        )
        run = _installed(seed, "--checkpoint", str(checkpoint))
        assert run.returncode == 0, (run.stdout, run.stderr)
        assert "Checkpoint written." in run.stdout

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
        commands = []
        try:
            _prompt(process.stdout)

            def act(command):
                process.stdin.write(command + "\n")
                process.stdin.flush()
                commands.append(command)
                return _prompt(process.stdout)

            observation = act("inspect myself")
            if "Weathered Waystone" in observation:
                assert carried
                assert "Yard" in act("move west")
                assert "You drop the Weathered Waystone." in act("drop waystone")
            else:
                assert not carried
                present = act("look for waystone")
                assert "Weathered Waystone" in present
                assert "You drag the Weathered Waystone west." in act(
                    "I drag the waystone west"
                )
                assert "Yard" in act("move west")
            assert "Weathered Waystone" in act("look for waystone")
            assert "Checkpoint written." in act("save")
            process.stdin.write("exit\n")
            process.stdin.flush()
            process.stdin.close()
            remainder = process.stdout.read()
            assert process.wait(timeout=45) == 0, (commands, remainder, process.stderr.read())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)

        rows = _trace(trace)
        assert len(rows) == len(commands)
        assert [r["raw_player_input"] for r in rows] == [c + "\n" for c in commands]
        assert rows[0]["parsed_action"] == "inspect"
        assert rows[0]["pre_state_digest"] == rows[0]["post_state_digest"]
        assert rows[0]["authoritative_changed"] is False
        if carried:
            assert [x["parsed_action"] for x in rows[1:3]] == ["move", "drop"]
            assert all(x["receipt_id"] for x in rows[1:3])
        else:
            sight, dragged = rows[1:3]
            assert sight["parsed_action"] == "focused_observation"
            assert sight["pre_state_digest"] == sight["post_state_digest"]
            assert dragged["parsed_action"] == "drag"
            assert dragged["result_type"] == "object_displacement_committed"
            assert dragged["receipt_id"] and dragged["state_delta_id"]
        assert rows[-2]["result_type"] == "focused_sighting"
        assert rows[-2]["pre_state_digest"] == rows[-2]["post_state_digest"]
        assert rows[-1]["result_type"] == "checkpoint_written"
        assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
        restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert restored.authoritative_digest() == rows[-1]["post_state_digest"]
        _stone_ground_at_yard(restored)
        prior = checkpoint.read_bytes()
        verified = _installed(
            ("look for waystone", "save"),
            "--load", str(checkpoint), "--checkpoint", str(checkpoint),
        )
        assert verified.returncode == 0, (verified.stdout, verified.stderr)
        assert "Weathered Waystone" in verified.stdout
        assert checkpoint.read_bytes() == prior
        comparable.append((
            tuple(commands),
            tuple((row["parsed_action"], row["result_type"],
                   row["failure_class"], row["pre_state_digest"],
                   row["post_state_digest"]) for row in rows),
            checkpoint.read_bytes(),
        ))
    assert comparable[0] == comparable[1]
