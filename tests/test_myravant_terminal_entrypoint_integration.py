"""Regression tests for the real installed Myravant terminal entrypoint."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys

from astra_runtime.myravant_play_application import MyravantPlayApplication
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _run_terminal(commands: str, *args: str, installed: bool = False):
    if installed:
        executable = shutil.which("myravant-play")
        assert executable is not None, "CI must install the myravant-play entrypoint"
        argv = [executable]
    else:
        argv = [sys.executable, "-m", "astra_runtime.myravant_terminal"]
    return subprocess.run(
        [*argv, *args],
        input=commands,
        text=True,
        capture_output=True,
        timeout=40,
    )


def _interactions(path):
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]
    assert records[0]["record_type"] == "session_start"
    assert records[-1]["record_type"] == "session_end"
    return [record for record in records if record["record_type"] == "interaction"]


def test_installed_entrypoint_follow_restart_cancel_and_evidence(tmp_path):
    checkpoint = tmp_path / "save.json"
    trace = tmp_path / "first.jsonl"
    first = _run_terminal(
        "ask groundskeeper to follow me\n"  # actor absent: no mutation
        "move south\n"
        "move south\n"
        "ask the groundskeeper to follow me\n"
        "move north\n"
        "move east\n"
        "look\n"
        "save\n"
        "exit\n",
        "--checkpoint", str(checkpoint),
        "--trace", str(trace),
        "--repository-sha", "a" * 40,
        installed=True,
    )
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "not here" in first.stdout
    assert "follows" in first.stdout
    assert "Orchard Path" in first.stdout
    assert "Checkpoint written." in first.stdout
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
    original = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert len(original.follow_intent_state.active_intents) == 1
    first_trace = _interactions(trace)
    follow = [item for item in first_trace if item["parsed_action"] == "vsm14_persistent_follow_intent"]
    assert [item["authoritative_changed"] for item in follow] == [False, True]
    assert any(
        item.get("world_process_action") == "follow_move"
        and item.get("world_process_outcome") == "committed"
        for item in first_trace
    )

    trace2 = tmp_path / "second.jsonl"
    second = _run_terminal(
        "look\n"
        "ask groundskeeper to stop following me\n"
        "move west\n"
        "look\n"
        "save\n"
        "exit\n",
        "--load", str(checkpoint),
        "--checkpoint", str(checkpoint),
        "--trace", str(trace2),
        "--repository-sha", "a" * 40,
    )
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "Orchard Path" in second.stdout
    assert "You move to the Yard." in second.stdout
    assert "Checkpoint written." in second.stdout
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.follow_intent_state.active_intents == ()
    assert restored.current_place_id() != original.current_place_id()
    assert "vsm14_persistent_follow_intent" in {
        item["parsed_action"] for item in _interactions(trace2)
    }


def test_installed_entrypoint_preserves_prior_bounded_routes_and_unknown_pressure(tmp_path):
    trace = tmp_path / "routes.jsonl"
    run = _run_terminal(
        "ask groundskeeper to throw lantern east\n"
        "ask groundskeeper to drop lantern\n"
        "ask groundskeeper to store lantern in chest\n"
        "ask groundskeeper to go to yard\n"
        "ask groundskeeper to light lantern\n"
        "climb onto the roof\n"
        "exit\n",
        "--trace", str(trace),
        "--repository-sha", "b" * 40,
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    observed = _interactions(trace)
    assert [row["parsed_action"] for row in observed] == [
        "vsm13_actor_mediated_displacement",
        "vsm12_actor_mediated_custody",
        "vsm11_actor_mediated_storage",
        "vsm10_actor_mediated_movement",
        "vsm9_actor_mediated",
        "unsupported",
    ]
    assert all(row["authoritative_changed"] is False for row in observed)
    assert observed[-1]["failure_class"] == "unsupported_input_no_executable_route"


def test_public_entrypoint_restores_v4_then_upgrades_on_save(tmp_path):
    checkpoint = tmp_path / "historical.json"
    old = MyravantPlayApplication.new(checkpoint_path=checkpoint)
    # V4 is selected only when the historical application has a committed
    # actor-object handoff; movement alone uses its V2 checkpoint writer.
    assert old.pickup("lantern").authoritative_changed
    assert old.move("south").authoritative_changed
    assert old.move("south").authoritative_changed
    assert old.give_object("lantern", "groundskeeper").authoritative_changed
    old.save()
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 4
    run = _run_terminal(
        "look\nsave\nexit\n",
        "--load", str(checkpoint),
        "--checkpoint", str(checkpoint),
    )
    assert run.returncode == 0, (run.stdout, run.stderr)
    assert "Gatehouse" in run.stdout
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
    new = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert new.follow_intent_state.active_intents == ()
    assert new.current_place_id() == old.current_place_id()
    assert new.state.representation == old.state.representation
    assert new.runtime_state.committed_actor_object_handoff_transitions == (
        old.runtime_state.committed_actor_object_handoff_transitions
    )


def test_public_entrypoint_refuses_corrupt_v5_and_does_not_replace_file(tmp_path):
    checkpoint = tmp_path / "bad.json"
    checkpoint.write_text('{"format_version":5,"unexpected":true}', encoding="utf-8")
    before = checkpoint.read_bytes()
    run = _run_terminal("look\nexit\n", "--load", str(checkpoint))
    assert run.returncode == 2
    assert "Unable to restore checkpoint:" in run.stderr
    assert checkpoint.read_bytes() == before
