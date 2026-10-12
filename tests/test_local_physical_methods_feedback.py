"""Feedback-conditioned synthetic player using real terminal output.

Policy branches on actual visible denial; the simulator does not predict or
rewrite authoritative game results and does not claim to be human play.
"""

from __future__ import annotations

import json
import shutil
import subprocess


def _prompt(reader):
    output = ""
    while not output.endswith("\n> "):
        char = reader.read(1)
        if not char:
            raise AssertionError("terminal exited before producing prompt")
        output += char
        if len(output) > 20000:
            raise AssertionError("no complete terminal prompt")
    return output


def test_failed_slide_causes_synthetic_player_to_change_method(tmp_path):
    binary = shutil.which("myravant-play")
    assert binary is not None
    trace = tmp_path / "pressure.jsonl"
    checkpoint = tmp_path / "pressure.json"
    process = subprocess.Popen(
        [binary, "--trace", str(trace), "--checkpoint", str(checkpoint)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, bufsize=1,
    )
    assert process.stdin and process.stdout and process.stderr

    def turn(action):
        process.stdin.write(action + "\n")
        process.stdin.flush()
        return _prompt(process.stdout)

    try:
        _prompt(process.stdout)
        move = turn("move south")
        assert "Yard" in move
        refusal = turn("slide chest north")
        assert "cannot slide" in refusal
        # Only because the terminal refused the slide does this policy change
        # method. If the runtime unexpectedly reports success, we reject it.
        next_method = "push chest north" if "cannot slide" in refusal else "inspect chest"
        assert next_method == "push chest north"
        accepted = turn(next_method)
        assert "You push the Tool Chest north." in accepted
        view = turn("inspect chest")
        assert "cannot inspect" in view.lower()
        turn("move north")
        found = turn("inspect chest")
        assert "Tool Chest" in found
        assert "You cannot inspect" not in found
        turn("save")
        process.stdin.write("exit\n")
        process.stdin.flush()
        process.stdin.close()
        code = process.wait(timeout=40)
        stderr = process.stderr.read()
        assert code == 0, stderr
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=10)
    lines = [json.loads(s) for s in trace.read_text(encoding="utf-8").splitlines()]
    actions = [r for r in lines if r["record_type"] == "interaction"]
    assert [r["parsed_action"] for r in actions] == [
        "move", "slide", "push", "inspect", "move", "inspect", "save"
    ]
    assert [r["authoritative_changed"] for r in actions] == [
        True, False, True, False, True, False, False,
    ]
    assert actions[1]["pre_state_digest"] == actions[1]["post_state_digest"]
    assert actions[1]["failure_class"] == "object_displacement_route_unavailable"
    assert actions[2]["receipt_id"] and actions[2]["state_delta_id"]
    assert json.loads(checkpoint.read_text(encoding="utf-8"))["format_version"] == 5
