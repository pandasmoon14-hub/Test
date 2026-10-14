"""Alternative-method investigation using transportable contained illumination.

This is an explicitly noncanonical fixture scenario. A container moved by an
existing lawful displacement transition preserves its contained object. The
fixture's narrow Orchard corridor requires a closed lid, and current object
placement/open state controls illumination in the dark Orchard Path.

No container physics, universal lid rule, body assumptions or new state owner.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    CONTAINED_BY_RELATION_TYPE,
    LOCATED_AT_RELATION_TYPE,
)
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, TOOL_CHEST_ID, ORCHARD_PATH_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application

WAYSTONE = "waystone"


def _put_lit_lantern_in_open_chest(app):
    assert app.light_object("lantern").authoritative_changed
    assert app.displace_object("lantern", "south", method="slide").authoritative_changed
    assert app.move("south").authoritative_changed
    assert app.open_object("chest").authoritative_changed
    assert app.pickup("lantern").authoritative_changed
    stored = app.store_object("lantern", "chest")
    assert stored.authoritative_changed
    assert stored.receipt_id and stored.state_delta_id
    assert app.current_place_id() == YARD_ID
    assert any(
        r.relation_type == CONTAINED_BY_RELATION_TYPE
        and r.subject_entity_id == LANTERN_ID
        and r.object_entity_id == TOOL_CHEST_ID
        for r in app.state.representation.relations
    )


def _read_only_sighting(app, expected: bool):
    digest = app.authoritative_digest()
    result = app.focused_observation(WAYSTONE)
    assert result.authoritative_changed is False
    assert result.pre_state_digest == result.post_state_digest == digest
    assert app.authoritative_digest() == digest
    if expected:
        assert result.result_type == "focused_sighting"
        assert result.observation_evidence_id
        assert "Weathered Waystone" in result.message
    else:
        assert result.result_type == "focused_observation_unavailable"
        assert result.failure_class == "focused_target_not_observed"
    return result


def test_container_condition_is_true_owner_opportunity_and_no_state_change():
    app = MyravantVSM14Application.new()
    _put_lit_lantern_in_open_chest(app)
    digest = app.authoritative_digest()
    before = app.state.representation
    refusal = app.displace_object("chest", "east", method="push")
    assert refusal.result_type == "object_displacement_rejected"
    assert refusal.failure_class == "object_displacement_opportunity_unavailable"
    assert "must be closed" in refusal.message
    assert refusal.opportunity_evidence_id and refusal.spatial_evidence_id
    assert refusal.receipt_id is None and refusal.state_delta_id is None
    assert refusal.pre_state_digest == refusal.post_state_digest == digest
    assert app.authoritative_digest() == digest
    assert app.state.representation == before

    assert app.close_object("chest").authoritative_changed
    changed = app.displace_object("chest", "east", method="push")
    assert changed.result_type == "object_displacement_committed"
    assert changed.authoritative_changed
    assert changed.receipt_id and changed.state_delta_id
    assert changed.opportunity_evidence_id
    assert app.state.representation != before
    assert app.entity_place_id(TOOL_CHEST_ID) == ORCHARD_PATH_ID
    assert any(
        r.relation_type == CONTAINED_BY_RELATION_TYPE
        and r.subject_entity_id == LANTERN_ID
        and r.object_entity_id == TOOL_CHEST_ID
        for r in app.state.representation.relations
    )
    assert app.object_lit_state(LANTERN_ID).state == "lit"

    assert app.move("east").authoritative_changed
    _read_only_sighting(app, expected=False)
    assert app.open_object("chest").authoritative_changed
    _read_only_sighting(app, expected=True)
    assert app.close_object("chest").authoritative_changed
    _read_only_sighting(app, expected=False)
    assert app.open_object("chest").authoritative_changed
    _read_only_sighting(app, expected=True)
    recovered = app.retrieve_object("lantern", "chest")
    assert recovered.authoritative_changed and recovered.receipt_id
    _read_only_sighting(app, expected=True)


def test_direct_carry_is_alternative_goal_method_without_route_condition():
    app = MyravantVSM14Application.new()
    for transition in (
        app.pickup("lantern"),
        app.light_object("lantern"),
        app.move("south"),
        app.move("east"),
    ):
        assert transition.authoritative_changed and transition.receipt_id
    assert app.current_place_id() == ORCHARD_PATH_ID
    _read_only_sighting(app, expected=True)
    assert app.object_open_state(TOOL_CHEST_ID).state == "closed"


def _binary():
    executable = shutil.which("myravant-play")
    assert executable is not None, "Must exercise installed player launcher"
    return executable


def _run(commands, *args):
    return subprocess.run(
        [_binary(), *args],
        input="\n".join((*commands, "exit", "")),
        text=True, capture_output=True, timeout=60,
    )


def _prompt(stdout):
    response = ""
    while not response.endswith("\n> "):
        char = stdout.read(1)
        assert char, ("Installed player closed before a decision", response)
        response += char
        assert len(response) < 30000
    return response


def _trace(path):
    records = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    assert records[-1]["evidence_complete"] is True
    return [r for r in records if r["record_type"] == "interaction"]


@pytest.mark.parametrize("transport", ("carried", "enclosed"))
def test_installed_player_adapts_method_condition_and_darkness(tmp_path, transport):
    outputs = []
    for trial in ("alpha", "beta"):
        checkpoint = tmp_path / f"{trial}.json"
        trace = tmp_path / f"{trial}.jsonl"
        seed = (
            ("pickup lantern", "light lantern", "move south", "save")
            if transport == "carried"
            else (
                "light lantern", "slide lantern south", "move south",
                "open chest", "pickup lantern", "put lantern in chest", "save",
            )
        )
        seeded = _run(seed, "--checkpoint", str(checkpoint))
        assert seeded.returncode == 0, (seeded.stdout, seeded.stderr)
        assert "Checkpoint written." in seeded.stdout

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
        try:
            _prompt(process.stdout)

            def act(command):
                process.stdin.write(command + "\n")
                process.stdin.flush()
                commands.append(command)
                return _prompt(process.stdout)

            self_view = act("inspect myself")
            if "Carrying: Brass Lantern." in self_view:
                assert transport == "carried"
                assert "Orchard Path" in act("move east")
                assert "Weathered Waystone" in act("look for waystone")
            else:
                assert transport == "enclosed"
                local = act("look")
                assert "Tool Chest" in local
                attempted = act("push chest east")
                assert "must be closed" in attempted
                assert "You close the Tool Chest." in act("close chest")
                pushed = act("push chest east")
                assert "You push the Tool Chest east." in pushed
                assert "Orchard Path" in act("move east")
                dark = act("look for waystone")
                assert "cannot verify" in dark
                assert "You open the Tool Chest." in act("open chest")
                revealed = act("look for waystone")
                assert "Weathered Waystone" in revealed
            assert "Checkpoint written." in act("save")
            process.stdin.write("exit\n")
            process.stdin.flush()
            process.stdin.close()
            remaining = process.stdout.read()
            code = process.wait(timeout=45)
            assert code == 0, (commands, remaining, process.stderr.read())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)

        rows = _trace(trace)
        assert len(rows) == len(commands)
        assert [r["raw_player_input"] for r in rows] == [c + "\n" for c in commands]
        assert rows[0]["parsed_action"] == "inspect"
        assert rows[0]["pre_state_digest"] == rows[0]["post_state_digest"]
        assert not rows[0]["authoritative_changed"]
        if transport == "enclosed":
            refused = next(
                r for r in rows if r["parsed_action"] == "push"
                and r["failure_class"] == "object_displacement_opportunity_unavailable"
            )
            assert not refused["authoritative_changed"]
            assert refused["pre_state_digest"] == refused["post_state_digest"]
            assert refused["receipt_id"] is None
            assert refused["opportunity_evidence_id"]
            committed = next(
                r for r in rows if r["parsed_action"] == "push"
                and r["result_type"] == "object_displacement_committed"
            )
            assert committed["authoritative_changed"] and committed["receipt_id"]
            sights = [r for r in rows if r["parsed_action"] == "focused_observation"]
            assert [r["result_type"] for r in sights] == [
                "focused_observation_unavailable", "focused_sighting",
            ]
        else:
            sights = [r for r in rows if r["parsed_action"] == "focused_observation"]
            assert [r["result_type"] for r in sights] == ["focused_sighting"]
        assert rows[-1]["result_type"] == "checkpoint_written"
        assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
        saved = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert saved.authoritative_digest() == rows[-1]["post_state_digest"]
        assert saved.current_place_id() == ORCHARD_PATH_ID
        _read_only_sighting(saved, expected=True)
        prior = checkpoint.read_bytes()
        resumed = _run(
            ("look for waystone", "save"),
            "--load", str(checkpoint), "--checkpoint", str(checkpoint),
        )
        assert resumed.returncode == 0, (resumed.stdout, resumed.stderr)
        assert "Weathered Waystone" in resumed.stdout
        assert checkpoint.read_bytes() == prior
        outputs.append((
            tuple(commands),
            tuple((r["parsed_action"], r["result_type"], r["failure_class"],
                r["pre_state_digest"], r["post_state_digest"]) for r in rows),
            checkpoint.read_bytes(),
        ))
    assert outputs[0] == outputs[1]


def test_no_unlicensed_method_or_remote_light_leak_after_sealed_transport():
    app = MyravantVSM14Application.new()
    _put_lit_lantern_in_open_chest(app)
    assert app.close_object("chest").authoritative_changed
    digest = app.authoritative_digest()
    bad_method = app.displace_object("chest", "east", method="slide")
    assert bad_method.failure_class == "object_displacement_route_unavailable"
    assert bad_method.pre_state_digest == bad_method.post_state_digest == digest
    assert app.displace_object("chest", "east", method="push").authoritative_changed
    # Contained lantern light is not a directly placed source, so the
    # separate Yard->Orchard glimmer corridor from #504 stays silent.
    from_yard = app.look_direction("east")
    assert from_yard.result_type == "directional_observation_unavailable"
    assert from_yard.failure_class == "directional_observation_unlicensed"
    assert from_yard.pre_state_digest == from_yard.post_state_digest
