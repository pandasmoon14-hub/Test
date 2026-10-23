"""Installed #563 actor activity journeys, run twice and independently restored.

Engineering-authored qualification, NOT a human or blind play certificate.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_activity_application import ActivityApplication
from astra_runtime.myravant_tarrow_activity import create_activity_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_material import placement

CASES = ("chain", "intervention", "contention")
WORKSHOP = ("go south", "go west", "go west", "go west")


def run_case(folder, case, sha):
    folder.mkdir()
    save = folder / "campaign.json"
    fixture_case = "contended" if case == "contention" else "standard"
    fixture = create_activity_fixture(activity_case=fixture_case)
    launcher = shutil.which("myravant-play")
    assert launcher, "installed executable required"
    traces = []

    def play(*commands):
        trace = folder / f"{len(traces):02}.jsonl"
        cmd = [launcher, "--locality", "tarrow-activities",
               "--activity-case", fixture_case, "--checkpoint", str(save),
               "--trace", str(trace), "--repository-sha", sha]
        if save.exists():
            cmd.extend(["--load", str(save)])
        completed = subprocess.run(cmd, input="\n".join((*commands, "save", "exit", "")),
                                   text=True, capture_output=True, timeout=180)
        assert completed.returncode == 0, (case, commands, completed.stdout[-1600:], completed.stderr)
        events = [json.loads(line) for line in trace.read_text().splitlines()]
        assert events and events[-1].get("evidence_complete") is True
        restored = ActivityApplication.restore(fixture=fixture, checkpoint_path=save)
        traces.append({"input": commands, "trace": str(trace),
                       "tick": restored.runtime_state.logical_time_state.logical_position,
                       "digest": restored.authoritative_digest(),
                       "journal": len(restored.journal)})
        return restored

    a = play(*WORKSHOP)
    if case == "chain":
        a = play("ask oren kesh to undertake bench upkeep")
        assert a.activity_records and not a.activity_records[0].task_ids
        a = play("wait 20 steps")
        record = a.activity_records[0]
        goals = {
            "three_distinct_stages": len(record.stages_finished) == 3,
            "completed": record.status == "completed",
            "assembly_material_truth": any(c.left == identity("repair-board") for c in a.connections),
            "real_tool_recovery": (placement(a.state.representation, identity("cleaning-cloth")).relation_type == "located_at"
                                   and placement(a.state.representation, identity("cleaning-cloth")).object_entity_id == identity("work-bench")),
            "unique_performer_receipts": len({r for t in a.participation_state.records
                                              for r in t.contributions}) == sum(
                                                 len(t.contributions) for t in a.participation_state.records)
        }
    elif case == "intervention":
        a = play("take cleaning cloth",
                 "ask oren kesh to undertake bench upkeep", "wait 2 steps")
        selected = a.participation_state.records[-1]
        assert selected.status == "blocked" and selected.blocked_due == 2
        a = play("drop cleaning cloth", "wait 20 steps")
        record = a.activity_records[0]
        goals = {
            "blocked_then_resumed": any(
                event[1] == "due_resolution" and event[3][3] == "blocked"
                for event in a.actor_events),
            "completion_after_real_tool": record.status == "completed",
            "recovery_preserves_identity": placement(
                a.state.representation, identity("cleaning-cloth")).object_entity_id
                == identity("work-bench"),
        }
    else:
        a = play("ask tali ren to undertake bench upkeep",
                 "ask oren kesh to undertake bench upkeep",
                 "wait 20 steps")
        records = a.activity_records
        goals = {
            "both_distinct_agreements": len(records) == 2 and len({r.activity_id for r in records}) == 2,
            "one_world_clock": len(a.intervals) == a.runtime_state.logical_time_state.logical_position,
            "actual_finite_joint": len(a.connections) <= 1,
            "no_duplicate_receipts": len({r for t in a.participation_state.records
                                          for r in t.contributions}) == sum(
                                             len(t.contributions) for t in a.participation_state.records),
            "different_actor_outcomes": any(r.status != "active" for r in records),
        }
    assert all(goals.values()), (case, goals, a.activity_records,
                                  a.participation_state.records)
    return {"case": case, "activity_case": fixture_case,
            "goals": goals, "digest": a.authoritative_digest(), "traces": traces}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repository-sha")
    args = parser.parse_args()
    sha = args.repository_sha or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, timeout=15).strip()
    assert len(sha) == 40 and all(x in "0123456789abcdef" for x in sha)
    with tempfile.TemporaryDirectory(prefix="myravant-activity-") as root:
        runs = [run_case(Path(root) / (case + "-" + str(repeat)), case, sha)
                for case in CASES for repeat in range(2)]
        for case in CASES:
            pair = [r for r in runs if r["case"] == case]
            assert len(pair) == 2 and pair[0]["digest"] == pair[1]["digest"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"schema": "myravant.actor-activities-installed.v1",
        "source": sha, "engineering_authored": True, "runs": runs}, indent=2,
        sort_keys=True) + "\n")
    print(f"Actor activities: {len(runs)} installed journeys with objective and replay checks passed.")


if __name__ == "__main__":
    main()
