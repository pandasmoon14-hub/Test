"""Larger package 2: licensed sensing, focused search, feedback and persistence.

This uses noncanonical fixture entities, existing owner-qualified transitions,
and the installed myravant-play path. It does not create epistemic knowledge.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_terminal import parse_terminal_command
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@pytest.mark.parametrize(
    ("text", "action", "argument"),
    (
        ("look for the lantern", "focused_observation", "lantern"),
        ("search for lantern", "focused_observation", "lantern"),
        ("I search for the waystone", "focused_observation", "waystone"),
        ("look for the groundskeeper to the south", "focused_observation", "groundskeeper -> south"),
        ("spot groundskeeper south", "focused_observation", "groundskeeper -> south"),
        ("spot lantern toward the east", "focused_observation", "lantern -> east"),
        ("look for it", "ambiguous", "it"),
        ("search for this", "ambiguous", "this"),
        ("look at lantern", "inspect", "lantern"),
        ("look south", "look_direction", "south"),
        ("push lantern east", "push", "lantern -> east"),
    ),
)
def test_preserves_distinct_player_intents(text, action, argument):
    parsed = parse_terminal_command(text)
    assert parsed.action == action
    assert parsed.argument == argument
    assert parsed.raw_text == text


def _assert_read_only(app, result):
    assert result.authoritative_changed is False
    assert result.pre_state_digest == result.post_state_digest
    assert result.pre_state_digest == app.authoritative_digest()


def test_focused_local_search_never_infers_undocumented_target_state():
    app = MyravantVSM14Application.new()
    found = app.focused_observation("lantern")
    assert found.result_type == "focused_sighting"
    assert found.view is not None
    assert found.view.description == "You can see the Brass Lantern here."
    assert found.observation_evidence_id
    _assert_read_only(app, found)

    hidden = app.focused_observation("waystone")
    unknown = app.focused_observation("nonexistent artifact")
    for result in (hidden, unknown):
        assert result.result_type == "focused_observation_unavailable"
        assert result.message == "You cannot verify that target from this view."
        assert result.failure_class == "focused_target_not_observed"
        _assert_read_only(app, result)
    # A detection is deliberately narrower than inspection: no contents,
    # equipment or knowledge facts are inferred.
    assert "open" not in found.view.description
    assert "Inside" not in found.view.description


def test_directional_sightline_discovers_grounded_actor_not_remote_private_objects():
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed  # Workshop -> Yard
    remote = app.look_direction("south")
    assert remote.result_type == "directional_observation"
    assert remote.view is not None
    assert remote.view.visible_actors == ("Groundskeeper",)
    assert remote.view.visible_objects == ()
    _assert_read_only(app, remote)

    located_actor = app.focused_observation("groundskeeper", direction="south")
    assert located_actor.result_type == "focused_sighting"
    assert located_actor.view.description == "You can see the Groundskeeper to the south."
    _assert_read_only(app, located_actor)

    local = app.focused_observation("groundskeeper")
    assert local.result_type == "focused_observation_unavailable"
    _assert_read_only(app, local)

    # East is a spatial movement route but has NO sensing license.
    no_sightline = app.look_direction("east")
    assert no_sightline.result_type == "directional_observation_unavailable"
    _assert_read_only(app, no_sightline)
    for target in ("waystone", "lantern", "unknown relic"):
        unseen = app.focused_observation(target, direction="east")
        assert unseen.message == "You cannot verify that target from this view."
        assert unseen.failure_class == "focused_target_not_observed"
        _assert_read_only(app, unseen)


def test_grounded_distant_object_sighting_changes_with_drop_pickup_and_custody():
    app = MyravantVSM14Application.new()
    assert app.pickup("lantern").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.give_object("lantern", "groundskeeper").authoritative_changed
    assert app.move("north").authoritative_changed
    surveyed = app.look_direction("south")
    assert surveyed.view.visible_objects == ()  # NPC's carried item not visible
    assert surveyed.view.visible_actors == ("Groundskeeper",)
    unseen = app.focused_observation("lantern", direction="south")
    assert unseen.failure_class == "focused_target_not_observed"
    _assert_read_only(app, unseen)

    assert app.move("south").authoritative_changed
    assert app.request_object_from_actor("groundskeeper", "lantern").authoritative_changed
    assert app.drop("lantern").authoritative_changed
    assert app.move("north").authoritative_changed
    now_visible = app.look_direction("south")
    assert now_visible.view.visible_objects == ("Brass Lantern",)
    found = app.focused_observation("lantern", direction="south")
    assert found.result_type == "focused_sighting"
    _assert_read_only(app, found)

    assert app.move("south").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    assert app.move("north").authoritative_changed
    assert app.look_direction("south").view.visible_objects == ()
    again = app.focused_observation("lantern", direction="south")
    assert again.failure_class == "focused_target_not_observed"
    _assert_read_only(app, again)
    current = app.focused_observation("lantern")
    assert current.result_type == "focused_sighting"
    _assert_read_only(app, current)


def test_local_search_after_multiple_physical_methods_and_light():
    dark = MyravantVSM14Application.new()
    assert dark.move("south").authoritative_changed
    assert dark.move("east").authoritative_changed
    denied = dark.focused_observation("waystone")
    assert denied.result_type == "focused_observation_unavailable"
    _assert_read_only(dark, denied)

    app = MyravantVSM14Application.new()
    assert app.light_object("lantern").authoritative_changed
    assert app.displace_object("lantern", "south", method="slide").authoritative_changed
    assert app.focused_observation("lantern").result_type == "focused_observation_unavailable"
    assert app.move("south").authoritative_changed
    assert app.focused_observation("lantern").result_type == "focused_sighting"
    assert app.displace_object("lantern", "east", method="push").authoritative_changed
    assert app.focused_observation("lantern").result_type == "focused_observation_unavailable"
    # Traversal, physical displacement and the light-state owner combine.
    assert app.move("east").authoritative_changed
    found = app.focused_observation("waystone")
    assert found.result_type == "focused_sighting"
    assert found.view.description == "You can see the Weathered Waystone here."
    assert app.focused_observation("lantern").result_type == "focused_sighting"
    _assert_read_only(app, found)


def _terminal(commands, *args):
    installed = shutil.which("myravant-play")
    assert installed, "CI must install myravant-play"
    return subprocess.run(
        [installed, *args],
        input="\n".join((*commands, "exit", "")),
        text=True,
        capture_output=True,
        timeout=45,
    )


def _interactions(path):
    rows = [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
    ]
    assert rows[0]["record_type"] == "session_start"
    assert rows[-1]["record_type"] == "session_end"
    return [row for row in rows if row["record_type"] == "interaction"]


def test_installed_terminal_feedback_and_checkpoint_sightings(tmp_path):
    checkpoint = tmp_path / "save.json"
    trace = tmp_path / "first.jsonl"
    steps = (
        "look for lantern",
        "move south",
        "look south",
        "spot groundskeeper south",
        "spot waystone east",
        "move south",
        "search for groundskeeper",
        "move north",
        "move north",
        "pickup lantern",
        "move south",
        "move south",
        "drop lantern",
        "move north",
        "look south",
        "look for lantern to south",
        "save",
    )
    a = _terminal(steps, "--checkpoint", str(checkpoint), "--trace", str(trace))
    assert a.returncode == 0, (a.stdout, a.stderr)
    row = _interactions(trace)
    assert len(row) == len(steps)
    assert [r["parsed_action"] for r in row] == [
        "focused_observation", "move", "look_direction",
        "focused_observation", "focused_observation", "move",
        "focused_observation", "move", "move", "pickup", "move",
        "move", "drop", "move", "look_direction", "focused_observation", "save",
    ]
    read_only = [r for r in row if r["parsed_action"] in (
        "focused_observation", "look_direction"
    )]
    assert all(
        r["authoritative_changed"] is False
        and r["pre_state_digest"] == r["post_state_digest"]
        for r in read_only
    )
    assert "Visible actors: Groundskeeper" in row[2]["player_visible_output"]
    assert "You can see the Groundskeeper to the south." in row[3]["player_visible_output"]
    assert row[4]["failure_class"] == "focused_target_not_observed"
    assert "Visible objects: Brass Lantern" in row[14]["player_visible_output"]
    assert row[15]["result_type"] == "focused_sighting"
    assert row[15]["observation_evidence_id"]
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5

    replay = _terminal(
        ("look south", "spot lantern south", "search for lantern", "save"),
        "--load", str(checkpoint), "--checkpoint", str(checkpoint),
    )
    assert replay.returncode == 0, (replay.stdout, replay.stderr)
    assert "Visible objects: Brass Lantern" in replay.stdout
    assert "You can see the Brass Lantern to the south." in replay.stdout
    assert "You cannot verify that target from this view." in replay.stdout
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.look_direction("south").view.visible_objects == ("Brass Lantern",)


def test_noncanonical_fixture_projections_do_not_leak_custody_or_closed_contents():
    app = MyravantPlayApplication.new()
    assert app.move("south").authoritative_changed
    assert app.look_direction("south").view.visible_objects == ()
    # Local targeted sighting is not a container contents inspection.
    found = app.focused_observation("chest")
    assert found.result_type == "focused_sighting"
    assert "contains" not in found.view.description
    assert "Inside" not in found.view.description
