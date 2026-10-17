"""#534 authored installed campaigns; separate from 39-case baseline and blind play."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_play_fixture import ORCHARD_PATH_ID, WAYSTONE_ID, YARD_ID
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application as App


def campaign(root, *, lowered, upright, head):
    launcher = shutil.which("myravant-play")
    if launcher is None:
        raise RuntimeError("installed myravant-play required")
    checkpoint = root / "world.json"
    stages = []
    previous_digest = None

    def stage(*commands):
        nonlocal previous_digest
        trace = root / f"stage-{len(stages)}.jsonl"
        args = [launcher, "--checkpoint", str(checkpoint), "--trace", str(trace),
                "--repository-sha", head]
        if checkpoint.exists():
            args += ["--load", str(checkpoint)]
        proc = subprocess.run(args, input="\n".join((*commands, "save", "exit", "")),
                              capture_output=True, text=True, timeout=60)
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        records = [json.loads(row) for row in trace.read_text(encoding="utf-8").splitlines()]
        assert records[-1]["record_type"] == "session_end" and records[-1]["evidence_complete"]
        rows = [r for r in records if r["record_type"] == "interaction"]
        if previous_digest is not None:
            assert rows[0]["pre_state_digest"] == previous_digest
        for a, b in zip(rows, rows[1:]):
            assert a["post_state_digest"] == b["pre_state_digest"]
        app = App.restore(checkpoint_path=checkpoint)
        assert app.authoritative_digest() == rows[-1]["post_state_digest"]
        previous_digest = app.authoritative_digest()
        stages.append({"commands": commands, "stdout": proc.stdout, "stderr": proc.stderr,
                       "records": records, "trace_sha256": sha256(trace.read_bytes()).hexdigest(),
                       "checkpoint_sha256": sha256(checkpoint.read_bytes()).hexdigest()})
        return proc.stdout, app

    output, app = stage("take lantern", "light lantern", "go south", "go east",
                        "drag waystone west", "go west", upright, "go east", "inspect self")
    assert "obstructs" in output and app.current_place_id() == YARD_ID
    assert app.entity_place_id(WAYSTONE_ID) == YARD_ID
    branches = ["observed refusal while upright; selected an explicitly advised lowered configuration"]
    # Next action is chosen only after actual player-visible refusal and advice.
    assert "crouch" in output and "lying" in output
    output, app = stage(f"{lowered} then walk east", "inspect self")
    assert app.current_place_id() == ORCHARD_PATH_ID
    expected = {"crouch": "crouching", "kneel": "kneeling", "lie down": "lying"}[lowered]
    assert f"Recorded posture: {expected}" in output
    output, app = stage("wait", "go west", "inspect self", "walk east")
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert app.posture_state.configuration == expected
    branches.append("after time and restart, revisited the unchanged obstruction with recorded configuration")
    output, app = stage("go west", upright, "walk east", "inspect self")
    assert "obstructs" in output and app.current_place_id() == YARD_ID
    # Change movement method after observed refusal. It must preserve upright pose.
    output, app = stage("crawl east", "inspect self")
    assert "crawl through" in output and app.current_place_id() == ORCHARD_PATH_ID
    upright_state = "standing" if upright == "stand" else "sitting"
    assert app.posture_state.configuration == upright_state
    branches.append("selected crawl after renewed upright refusal; method did not change posture")
    output, app = stage("wait", "inspect posture")
    objectives = {
        "returned_to_orchard": app.current_place_id() == ORCHARD_PATH_ID,
        "obstruction_unchanged": app.entity_place_id(WAYSTONE_ID) == YARD_ID,
        "method_did_not_set_pose": app.posture_state.configuration == upright_state,
        "recorded_pose_visible_after_restart": f"Recorded posture: {upright_state}" in output,
        "configuration_changes_did_not_charge_time": all(
            e.logical_step in {0, 1} for e in app.posture_state.events),
    }
    assert all(objectives.values()), objectives
    return {"lowered": lowered, "upright": upright, "feedback_branches": branches,
            "objectives": objectives, "final_digest": app.authoritative_digest(), "stages": stages}


def semantic(session):
    return [(s["final_digest"], s["objectives"], [
        (r["raw_player_input"], r["parsed_action"], r["result_type"], r["failure_class"],
         r["receipt_id"], r["pre_state_digest"], r["post_state_digest"])
        for stage in s["stages"] for r in stage["records"] if r["record_type"] == "interaction"
    ]) for s in session]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], check=True, text=True,
                          capture_output=True, timeout=15).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="myravant-posture-") as temp:
        sessions = []
        for repeat in range(2):
            trial = []
            for index, (lowered, upright) in enumerate((("crouch", "stand"), ("kneel", "sit"), ("lie down", "stand"))):
                root = Path(temp) / f"{repeat}-{index}"
                root.mkdir()
                trial.append(campaign(root, lowered=lowered, upright=upright, head=head))
            sessions.append(trial)
        assert semantic(sessions[0]) == semantic(sessions[1])
    evidence = {"repository_sha": head, "evidence_type": "implementation_authored_installed_posture_campaigns",
                "not_blind_holdout": True, "not_human_play": True, "not_canon": True,
                "profiles": 3, "repeat_runs": 2, "deterministic_repetition": True,
                "sessions": sessions[0]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("Posture: 3 feedback-conditioned profiles repeated twice; all access, restart and method predicates passed.")


if __name__ == "__main__":
    main()
