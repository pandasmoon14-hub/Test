"""Installed client and feedback-responsive synthetic play for package 3.

The synthetic player never modifies the world directly. It branches on actual
terminal refusals, chooses lawful alternative actions, then tests observation
and saved continuity of an NPC-attributed result.
"""

from __future__ import annotations

import json
import shutil
import subprocess

from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _read_prompt(out):
    text = ""
    while not text.endswith("\n> "):
        ch = out.read(1)
        if not ch:
            raise AssertionError("installed terminal exited before prompt")
        text += ch
        if len(text) > 24000:
            raise AssertionError("installed terminal did not issue next prompt")
    return text


def test_installed_player_recruits_and_changes_methods_on_actual_refusal(tmp_path):
    binary = shutil.which("myravant-play")
    assert binary is not None
    trace = tmp_path / "npc-ground.jsonl"
    checkpoint = tmp_path / "npc-ground.json"
    proc = subprocess.Popen(
        [binary, "--trace", str(trace), "--checkpoint", str(checkpoint)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1,
    )
    assert proc.stdin and proc.stdout and proc.stderr

    def turn(command):
        proc.stdin.write(command + "\n")
        proc.stdin.flush()
        return _read_prompt(proc.stdout)

    try:
        assert "Workshop" in _read_prompt(proc.stdout)

        remote_refusal = turn("ask groundskeeper to slide lantern south")
        assert "not here" in remote_refusal.lower()
        # The policy responds to actual feedback and meets the actor.
        assert "light" in turn("light lantern").lower()
        assert "Yard" in turn("move south")
        assert "Gatehouse" in turn("move south")
        assert "follow" in turn("ask groundskeeper to follow me").lower()
        assert "Yard" in turn("move north")

        wrong_method = turn("ask groundskeeper to slide chest north")
        assert "cannot move" in wrong_method.lower()
        # A lawful alternative method exists on the same grounded object.
        method = (
            "ask groundskeeper to push chest north"
            if "cannot move" in wrong_method.lower()
            else "spot chest"
        )
        assert method == "ask groundskeeper to push chest north"
        accepted = turn(method)
        assert "The Groundskeeper pushes the Tool Chest north." in accepted
        assert "cannot verify" in turn("search for chest")
        assert "Workshop" in turn("move north")
        assert "You can see the Tool Chest here." in turn("search for chest")

        slid = turn("ask groundskeeper to slide lantern south")
        assert "The Groundskeeper slides the Brass Lantern south." in slid
        assert "Yard" in turn("move south")
        pushed = turn("ask groundskeeper to push lantern east")
        assert "The Groundskeeper pushes the Brass Lantern east." in pushed
        assert "cannot verify" in turn("search for lantern")
        assert "Orchard Path" in turn("move east")
        assert "You can see the Weathered Waystone here." in turn("search for waystone")
        assert "You can see the Brass Lantern here." in turn("search for lantern")
        turn("save")

        proc.stdin.write("exit\n")
        proc.stdin.flush()
        proc.stdin.close()
        exit_code = proc.wait(timeout=45)
        stderr = proc.stderr.read()
        assert exit_code == 0, stderr
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=10)

    rows = [json.loads(s) for s in trace.read_text(encoding="utf-8").splitlines()]
    assert rows[0]["record_type"] == "session_start"
    assert rows[-1]["record_type"] == "session_end"
    actions = [r for r in rows if r["record_type"] == "interaction"]
    ground = [
        r for r in actions
        if r["parsed_action"] == "large3_actor_mediated_ground_contact"
    ]
    assert len(ground) == 5
    assert [r["authoritative_changed"] for r in ground] == [
        False, False, True, True, True,
    ]
    assert ground[0]["failure_class"] == "ground_request_actor_not_local"
    assert ground[1]["failure_class"] == "ground_request_route_unavailable"
    assert ground[2]["receipt_id"] and ground[2]["state_delta_id"]
    assert ground[3]["receipt_id"] and ground[3]["state_delta_id"]
    assert ground[4]["receipt_id"] and ground[4]["state_delta_id"]
    for result in ground[:2]:
        assert result["pre_state_digest"] == result["post_state_digest"]
    for result in ground[2:]:
        assert result["pre_state_digest"] != result["post_state_digest"]

    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
    saved = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert saved.focused_observation("waystone").result_type == "focused_sighting"
    assert saved.focused_observation("lantern").result_type == "focused_sighting"
    assert [
        x.receipt.method
        for x in saved.runtime_state.committed_object_displacement_transitions
    ] == ["push", "slide", "push"]
    assert all(
        x.receipt.actor_entity_id == saved.fixture.resolve_actor_reference("groundskeeper")
        for x in saved.runtime_state.committed_object_displacement_transitions
    )

    # The player can resume at the same persistent place and observe the
    # exact same world; read-only actions must not rewrite the checkpoint.
    resumed = subprocess.run(
        [binary, "--load", str(checkpoint), "--checkpoint", str(checkpoint)],
        input="search for lantern\nsearch for waystone\nexit\n",
        capture_output=True, text=True, timeout=45,
    )
    assert resumed.returncode == 0, resumed.stderr
    assert "You can see the Brass Lantern here." in resumed.stdout
    assert "You can see the Weathered Waystone here." in resumed.stdout
