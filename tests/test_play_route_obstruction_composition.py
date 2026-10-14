"""Player-produced route obstruction: stateful environment changes movement.

Held-out semantic matrix exercises route opportunity, object custody,
physical methods, sensing, source evidence, installed adaptive player,
v5 persistence, and negative controls. Noncanonical fixture facts do not
become universal collision/weight or object physics rules.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import replace

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CARRIED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    replay_persistent_world_movement,
)
from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_play_fixture import (
    ORCHARD_PATH_ID, WAYSTONE_ID, WORKSHOP_ID, YARD_ID,
    FixtureMovementObstructionLicense,
    MyravantPlayFixtureError,
    create_terminal_play_fixture,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _place_waystone_at_yard(app):
    for name, result in (
        ("pickup lantern", app.pickup("lantern")),
        ("light lantern", app.light_object("lantern")),
        ("move south", app.move("south")),
        ("move east", app.move("east")),
        ("drag waystone west", app.displace_object("waystone", "west", method="drag")),
        ("move west", app.move("west")),
    ):
        assert result.authoritative_changed and result.receipt_id, (name, result)
    assert app.current_place_id() == YARD_ID
    assert _placement(app, WAYSTONE_ID) == (LOCATED_AT_RELATION_TYPE, YARD_ID)


def _placement(app, entity):
    relations = [
        rel for rel in app.state.representation.relations
        if rel.subject_entity_id == entity
        and rel.relation_type in (CARRIED_BY_RELATION_TYPE, LOCATED_AT_RELATION_TYPE)
    ]
    assert len(relations) == 1
    return relations[0].relation_type, relations[0].object_entity_id


def _blocked(app):
    digest = app.authoritative_digest()
    count = len(app.state.committed_transitions)
    result = app.move("east")
    assert result.result_type == "movement_rejected"
    assert result.failure_class == "movement_opportunity_obstructed"
    assert "obstructs" in result.message
    assert result.authoritative_changed is False
    assert result.pre_state_digest == result.post_state_digest == digest
    assert result.command_id
    assert result.spatial_evidence_id and result.opportunity_evidence_id
    assert result.receipt_id is None and result.state_delta_id is None
    assert len(app.state.committed_transitions) == count
    assert app.current_place_id() == YARD_ID
    assert app.authoritative_digest() == digest
    return result


def _clear(app, method):
    if method == "pickup":
        result = app.pickup("waystone")
        assert result.result_type == "custody_committed"
        assert _placement(app, WAYSTONE_ID) == (
            CARRIED_BY_RELATION_TYPE, app.fixture.player_entity_id
        )
    elif method == "push":
        result = app.displace_object("waystone", "north", method="push")
        assert result.result_type == "object_displacement_committed"
        assert _placement(app, WAYSTONE_ID) == (
            LOCATED_AT_RELATION_TYPE, WORKSHOP_ID
        )
    else:
        raise AssertionError(method)
    assert result.authoritative_changed
    assert result.receipt_id and result.state_delta_id
    assert result.opportunity_evidence_id
    return result


@pytest.mark.parametrize("clearance", ("pickup", "push"))
def test_obstacle_blocks_only_licensed_corridor_then_owner_replay_restores(clearance):
    app = MyravantVSM14Application.new()
    _place_waystone_at_yard(app)

    refused = _blocked(app)
    same = _blocked(app)
    assert refused.opportunity_evidence_id == same.opportunity_evidence_id

    # Other directions are still legal; a single obstructed exit is not
    # an invisible area-wide arrest or an invented closure of the room.
    untouched_digest = app.authoritative_digest()
    north = app.move("north")
    assert north.authoritative_changed and north.receipt_id
    assert app.move("south").authoritative_changed
    assert app.authoritative_digest() != untouched_digest
    _blocked(app)

    cleared = _clear(app, clearance)
    pre_move = app.state.representation
    moved = app.move("east")
    assert moved.result_type == "movement_committed"
    assert moved.authoritative_changed and moved.receipt_id
    assert moved.spatial_evidence_id and moved.opportunity_evidence_id
    receipt = app.state.committed_transitions[-1].receipt
    assert replay_persistent_world_movement(
        pre_state_representation=pre_move, receipt=receipt,
    ) == app.state.representation
    assert app.current_place_id() == ORCHARD_PATH_ID
    # The two legal methods had DIFFERENT authoritative object outcomes.
    assert _placement(app, WAYSTONE_ID)[0] == (
        CARRIED_BY_RELATION_TYPE if clearance == "pickup"
        else LOCATED_AT_RELATION_TYPE
    )

    if clearance == "pickup":
        assert app.move("west").authoritative_changed
        assert app.drop("waystone").authoritative_changed
        _blocked(app)


def test_only_registered_object_placement_obstructs_not_any_nearby_object():
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed
    # At initial state, the Tool Chest is in Yard and lantern is elsewhere.
    # Neither blocks the east exit. This explicitly disproves a generic
    # co-located-object => collision rule.
    initial = app.move("east")
    assert initial.result_type == "movement_committed"
    assert initial.authoritative_changed and initial.receipt_id
    assert app.move("west").authoritative_changed
    assert app.displace_object("chest", "east", method="push").authoritative_changed
    assert app.move("east").authoritative_changed


def test_fixture_rejects_unqualified_obstacle_identity_and_nonexistent_route():
    fixture = create_terminal_play_fixture()
    wrong_identity = replace(
        fixture.movement_obstruction_licenses[0],
        blocking_object_entity_id="astra:entity:not-a-real-object",
    )
    with pytest.raises(MyravantPlayFixtureError):
        replace(fixture, movement_obstruction_licenses=(wrong_identity,))
    wrong_route = replace(
        fixture.movement_obstruction_licenses[0], direction="northwest",
    )
    with pytest.raises(MyravantPlayFixtureError):
        replace(fixture, movement_obstruction_licenses=(wrong_route,))


# Fixed semantic outcomes, not a count of lexical aliases.
# Each cell is a distinct actor/goal/method/target/state opportunity.
HELD_OUT_OUTCOMES = (
    ("unblocked traversal", "move", "Yard->Orchard", "initial", "commit"),
    ("blocked traversal", "move", "Yard->Orchard", "waystone_ground_Yard", "deny"),
    ("blocked retry", "move", "Yard->Orchard", "waystone_ground_Yard", "deny"),
    ("unrelated route", "move", "Yard->Workshop", "waystone_ground_Yard", "commit"),
    ("carry clearance", "pickup", "Waystone", "waystone_ground_Yard", "commit"),
    ("carry-enabled traversal", "move", "Yard->Orchard", "waystone_carried", "commit"),
    ("ground clearance", "push", "Waystone->Workshop", "waystone_ground_Yard", "commit"),
    ("push-enabled traversal", "move", "Yard->Orchard", "waystone_ground_Workshop", "commit"),
    ("restored blockage", "drop", "Waystone->Yard", "waystone_carried", "commit"),
)


def test_held_out_goal_method_context_matrix_measures_real_coverage():
    assert len(HELD_OUT_OUTCOMES) == 9
    # Prior to this package the candidate was a normal route even when
    # the Waystone was grounded in Yard; now its outcome differs.
    # The broader 288-attempt synthetic corpus is not modified here.
    actual = []

    baseline = MyravantVSM14Application.new()
    assert baseline.move("south").authoritative_changed
    res = baseline.move("east")
    actual.append(("unblocked traversal", "commit" if res.authoritative_changed else "deny"))

    blocked = MyravantVSM14Application.new()
    _place_waystone_at_yard(blocked)
    for label in ("blocked traversal", "blocked retry"):
        res = blocked.move("east")
        actual.append((label, "commit" if res.authoritative_changed else "deny"))
    res = blocked.move("north")
    actual.append(("unrelated route", "commit" if res.authoritative_changed else "deny"))

    carried = MyravantVSM14Application.new()
    _place_waystone_at_yard(carried)
    picked = carried.pickup("waystone")
    actual.append(("carry clearance", "commit" if picked.authoritative_changed else "deny"))
    moved = carried.move("east")
    actual.append(("carry-enabled traversal", "commit" if moved.authoritative_changed else "deny"))

    pushed = MyravantVSM14Application.new()
    _place_waystone_at_yard(pushed)
    press = pushed.displace_object("waystone", "north", method="push")
    actual.append(("ground clearance", "commit" if press.authoritative_changed else "deny"))
    moved = pushed.move("east")
    actual.append(("push-enabled traversal", "commit" if moved.authoritative_changed else "deny"))

    assert carried.move("west").authoritative_changed
    dropped = carried.drop("waystone")
    actual.append(("restored blockage", "commit" if dropped.authoritative_changed else "deny"))
    expected = [(row[0], row[4]) for row in HELD_OUT_OUTCOMES]
    assert actual == expected
    assert sum(o == "commit" for _, o in actual) == 7
    assert sum(o == "deny" for _, o in actual) == 2
    _blocked(carried)


def _installed(commands, *args):
    executable = shutil.which("myravant-play")
    assert executable is not None, "CI must exercise installed player"
    return subprocess.run(
        [executable, *args],
        input="\n".join((*commands, "exit", "")),
        text=True, capture_output=True, timeout=65,
    )


def _prompt(stdout):
    output = ""
    while not output.endswith("\n> "):
        c = stdout.read(1)
        assert c, ("player ended unexpectedly", output)
        output += c
        assert len(output) < 32000
    return output


def _trace(path):
    records = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    assert records[-1]["evidence_complete"] is True
    return [r for r in records if r["record_type"] == "interaction"]


@pytest.mark.parametrize("choice", ("pickup", "push"))
def test_installed_adaptive_obstruction_clearance_survives_restore_and_replay(
    tmp_path, choice,
):
    comparisons = []
    for trial in ("alpha", "beta"):
        checkpoint = tmp_path / f"{choice}-{trial}.json"
        trace = tmp_path / f"{choice}-{trial}.jsonl"
        seeded = _installed((
            "pickup lantern", "light lantern", "move south", "move east",
            "drag waystone west", "move west", "save",
        ), "--checkpoint", str(checkpoint))
        assert seeded.returncode == 0, (seeded.stdout, seeded.stderr)
        assert "Checkpoint written." in seeded.stdout

        executable = shutil.which("myravant-play")
        process = subprocess.Popen(
            [
                executable, "--load", str(checkpoint),
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

            def act(command):
                process.stdin.write(command + "\n")
                process.stdin.flush()
                actions.append(command)
                return _prompt(process.stdout)

            denied = act("go east")
            assert "obstructs that passage" in denied
            scene = act("look")
            assert "Weathered Waystone" in scene
            if choice == "pickup":
                assert "You pick up the Weathered Waystone." in act("pickup waystone")
            else:
                assert "You push the Weathered Waystone north." in act("push waystone north")
            assert "Orchard Path" in act("go east")
            assert "Checkpoint written." in act("save")
            process.stdin.write("exit\n")
            process.stdin.flush()
            process.stdin.close()
            rest = process.stdout.read()
            assert process.wait(timeout=45) == 0, (rest, process.stderr.read())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)

        rows = _trace(trace)
        assert len(rows) == len(actions)
        assert [r["raw_player_input"] for r in rows] == [x + "\n" for x in actions]
        denied = rows[0]
        assert denied["parsed_action"] == "move"
        assert denied["failure_class"] == "movement_opportunity_obstructed"
        assert denied["pre_state_digest"] == denied["post_state_digest"]
        assert not denied["authoritative_changed"] and not denied["receipt_id"]
        assert denied["spatial_evidence_id"] and denied["opportunity_evidence_id"]
        assert rows[1]["parsed_action"] == "look"
        assert not rows[1]["authoritative_changed"]
        assert rows[2]["parsed_action"] == choice
        assert rows[2]["authoritative_changed"] and rows[2]["receipt_id"]
        assert rows[3]["result_type"] == "movement_committed"
        assert rows[3]["receipt_id"] and rows[3]["state_delta_id"]
        assert rows[-1]["result_type"] == "checkpoint_written"
        assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
        restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert restored.authoritative_digest() == rows[-1]["post_state_digest"]
        assert restored.current_place_id() == ORCHARD_PATH_ID
        assert _placement(restored, WAYSTONE_ID)[0] == (
            CARRIED_BY_RELATION_TYPE if choice == "pickup"
            else LOCATED_AT_RELATION_TYPE
        )
        saved_bytes = checkpoint.read_bytes()
        replay = _installed(
            ("inspect myself", "save"),
            "--load", str(checkpoint), "--checkpoint", str(checkpoint),
        )
        assert replay.returncode == 0, (replay.stdout, replay.stderr)
        assert checkpoint.read_bytes() == saved_bytes
        comparisons.append((
            tuple(actions),
            tuple((r["parsed_action"], r["result_type"],
                   r["failure_class"], r["pre_state_digest"],
                   r["post_state_digest"]) for r in rows),
            saved_bytes,
        ))
    assert comparisons[0] == comparisons[1]
