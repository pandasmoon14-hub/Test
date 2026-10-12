"""Feedback-conditioned player tactics through the actual installed terminal.

The synthetic policy does not know or edit backend truth. It branches only
after seeing a real player-facing response and proves that physical operations
change later sensing opportunities.
"""

from __future__ import annotations

import json
import shutil
import subprocess


def _prompt(reader):
    message = ""
    while not message.endswith("\n> "):
        char = reader.read(1)
        if not char:
            raise AssertionError("play client exited before prompt")
        message += char
        if len(message) > 24000:
            raise AssertionError("play client did not produce a complete prompt")
    return message


def test_synthetic_player_chooses_alternate_sightline_and_moves_object(tmp_path):
    binary = shutil.which("myravant-play")
    assert binary, "full suite must install the terminal entrypoint"
    trace = tmp_path / "feedback.jsonl"
    checkpoint = tmp_path / "world.json"
    process = subprocess.Popen(
        [binary, "--trace", str(trace), "--checkpoint", str(checkpoint)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert process.stdin and process.stdout and process.stderr

    def turn(text):
        process.stdin.write(text + "\n")
        process.stdin.flush()
        return _prompt(process.stdout)

    try:
        _prompt(process.stdout)
        assert "Yard" in turn("move south")
        denied_direction = turn("spot groundskeeper east")
        assert "cannot verify" in denied_direction
        # The player adapts to a truly unobservable eastern route rather
        # than assuming traversability grants sensory access.
        tactic = (
            "spot groundskeeper south"
            if "cannot verify" in denied_direction
            else "search for groundskeeper"
        )
        assert tactic == "spot groundskeeper south"
        visible_actor = turn(tactic)
        assert "You can see the Groundskeeper to the south." in visible_actor

        lantern_remote = turn("spot lantern south")
        assert "cannot verify" in lantern_remote
        # Not visible at Gatehouse yet. Instead of falsifying observation,
        # choose a physical method to place it where the sightline is licensed.
        if "cannot verify" in lantern_remote:
            actions = (
                "move north", "pickup lantern", "move south",
                "move south", "drop lantern", "move north",
            )
        else:
            actions = ("look south",)
        assert len(actions) == 6
        for action in actions:
            observed = turn(action)
            assert "cannot" not in observed.lower(), (action, observed)

        seen = turn("spot lantern south")
        assert "You can see the Brass Lantern to the south." in seen
        turn("save")
        process.stdin.write("exit\n")
        process.stdin.flush()
        process.stdin.close()
        code = process.wait(timeout=45)
        stderr = process.stderr.read()
        assert code == 0, stderr
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10)

    rows = [
        json.loads(line)
        for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    assert rows[0]["record_type"] == "session_start"
    assert rows[-1]["record_type"] == "session_end"
    interactions = [r for r in rows if r["record_type"] == "interaction"]
    assert [r["parsed_action"] for r in interactions] == [
        "move", "focused_observation", "focused_observation",
        "focused_observation", "move", "pickup", "move", "move",
        "drop", "move", "focused_observation", "save",
    ]
    assert interactions[1]["failure_class"] == "focused_target_not_observed"
    assert interactions[3]["failure_class"] == "focused_target_not_observed"
    for index in (1, 2, 3, 10):
        row = interactions[index]
        assert row["authoritative_changed"] is False
        assert row["pre_state_digest"] == row["post_state_digest"]
    for index in (0, 4, 5, 6, 7, 8, 9):
        row = interactions[index]
        assert row["authoritative_changed"] is True
        assert row["receipt_id"] and row["state_delta_id"]
    assert interactions[10]["result_type"] == "focused_sighting"
    assert interactions[10]["observation_evidence_id"]
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
