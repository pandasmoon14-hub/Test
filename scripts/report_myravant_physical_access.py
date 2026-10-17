"""Authored feedback-conditioned physical-access campaigns via installed CLI.

Separate from the unchanged 39-case discovery corpus and any blind holdout.
Private end-state predicates are evaluator checks, never player knowledge.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.domain.persistent_world_entity_location_representation import LOCATED_AT_RELATION_TYPE
from astra_runtime.myravant_play_fixture import LANTERN_ID, WAYSTONE_ID, WORKSHOP_ID, ORCHARD_PATH_ID
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def placed(app, target, destination):
    return any(r.subject_entity_id == target and r.object_entity_id == destination
               and r.relation_type == LOCATED_AT_RELATION_TYPE
               for r in app.state.representation.relations)


def campaign(root, approach, supply, head):
    launcher = shutil.which("myravant-play")
    if launcher is None:
        raise RuntimeError("installed myravant-play launcher required")
    checkpoint = root / f"{approach}-{supply}.json"
    records = []
    stages = []

    def stage(*commands):
        trace = root / f"{approach}-{supply}-{len(stages)}.jsonl"
        args = [launcher, "--checkpoint", str(checkpoint), "--trace", str(trace),
                "--repository-sha", head]
        if checkpoint.exists():
            args.extend(["--load", str(checkpoint)])
        result = subprocess.run(args, input="\n".join((*commands, "save", "exit", "")),
                                capture_output=True, text=True, timeout=120)
        if result.returncode:
            raise RuntimeError((result.stdout, result.stderr))
        rows = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
        assert rows[-1]["record_type"] == "session_end" and rows[-1]["evidence_complete"]
        interactions = [r for r in rows if r["record_type"] == "interaction"]
        for first, second in zip(interactions, interactions[1:]):
            assert first["post_state_digest"] == second["pre_state_digest"]
        if records:
            assert interactions[0]["pre_state_digest"] == records[-1]["post_state_digest"]
        records.extend(interactions)
        app = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
        assert app.authoritative_digest() == interactions[-1]["post_state_digest"]
        stages.append({"commands": commands, "checkpoint_sha256": sha256(checkpoint.read_bytes()).hexdigest(),
                       "trace_sha256": sha256(trace.read_bytes()).hexdigest()})
        return result.stdout, app

    output, _ = stage("get lantern to yard by sliding then go south", "go east",
                      "feel for waystone then get waystone to yard by dragging", "go west", "go east")
    # The policy only selects its next move after observing real refusal.
    assert "obstructs" in output
    branches = ["observed walking obstruction"]
    if approach == "crawl_then_clear":
        output, _ = stage("crawl east", "go west", "get waystone to workshop")
        assert "crawl through" in output and "push north" in output
        branches.append("bypassed obstruction without moving it; returned for clearance")
        method = "pushing"
    else:
        output, _ = stage("get waystone to workshop")
        method = {"push": "pushing", "slide": "sliding"}[approach]
        assert ("push north" if approach == "push" else "slide north") in output
        branches.append(f"selected {approach} after current method advice")
    _, _ = stage(f"get waystone to workshop by {method} then go east", "wait", "go west")
    output, _ = stage("light lantern", "get lantern to orchard")
    assert "pushing it east" in output
    if supply == "throw":
        output, _ = stage("take lantern", "get lantern to orchard")
        assert "throwing it east" in output
        branches.append("changed from ground handling to carried throw after custody feedback")
        stage("get lantern to orchard by throwing then go east")
    elif supply == "push":
        stage("get lantern to orchard by pushing then go east")
    else:
        stage("take lantern then go east", "drop lantern")
    _, final = stage("wait", "go west", "go east", "look for lantern")
    objectives = {
        "obstruction_object_relocated_to_workshop": placed(final, WAYSTONE_ID, WORKSHOP_ID),
        "lantern_delivered_on_ground_to_orchard": placed(final, LANTERN_ID, ORCHARD_PATH_ID),
        "ordinary_walk_east_succeeds_after_time_restart_and_return": final.current_place_id() == ORCHARD_PATH_ID,
    }
    assert all(objectives.values()), objectives
    assert not final.knowledge_state.events
    return {"approach": approach, "supply_method": supply, "feedback_branches": branches,
            "objectives": objectives, "final_digest": final.authoritative_digest(),
            "stages": stages, "interactions": records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True,
                          text=True, timeout=15).stdout.strip()
    profiles = (("push", "push"), ("slide", "throw"), ("crawl_then_clear", "carry"))
    with tempfile.TemporaryDirectory(prefix="myravant-physical-access-") as temp:
        root = Path(temp)
        sessions = []
        for index in range(2):
            trial = root / str(index)
            trial.mkdir()
            sessions.append([campaign(trial, *profile, head) for profile in profiles])
        # Compare semantic traces and authoritative histories, not UUID/session paths.
        def comparable(session):
            return [(s["final_digest"], s["objectives"], [
                (r["raw_player_input"], r["parsed_action"], r["result_type"], r["failure_class"],
                 r["receipt_id"], r["pre_state_digest"], r["post_state_digest"])
                for r in s["interactions"]]) for s in session]
        assert comparable(sessions[0]) == comparable(sessions[1])
    evidence = {"repository_sha": head, "evidence_type": "implementation_authored_feedback_conditioned_installed_campaigns",
                "not_blind_holdout": True, "not_human_play": True, "not_canon": True,
                "profiles": len(profiles), "repeat_runs": 2, "deterministic_repetition": True,
                "sessions": sessions[0]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(f"Physical access: {len(profiles)} profiles repeated twice; all objective predicates and replay comparisons passed.")


if __name__ == "__main__":
    main()
