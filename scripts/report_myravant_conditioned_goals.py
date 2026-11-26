"""Assess the predeclared evidence-conditioned conversations through both clients."""

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_activity_application import ActivityApplication
from astra_runtime.myravant_structures_application import StructuresApplication
from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_activity import create_activity_fixture
from astra_runtime.myravant_tarrow_structures import create_structures_fixture
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from report_myravant_constrained_goals import OFFLINE, ROOT

CORPUS = ROOT / "tests/fixtures/myravant_conditional/expectations.json"
sys.path.insert(0, str(ROOT))
SETUP = runpy.run_path(str(ROOT / "tests/test_play_conditioned_goals.py"))


def run(launcher, sha, folder, label, flags, turns, env, path=None):
    trace = folder / f"{label}.jsonl"
    argv = [launcher, *flags, "--repository-sha", sha, "--trace", str(trace)]
    if path is None:
        path = folder / f"{label}.json"
        argv += ["--checkpoint", str(path)]
    else:
        argv += ["--load", str(path)]
    process = subprocess.run(argv, input="\n".join((*turns, "exit", "")), capture_output=True,
                             encoding="utf-8", check=True, env=env, timeout=120)
    trace_rows = [json.loads(line) for line in trace.read_text().splitlines()]
    assert trace_rows[-1]["evidence_complete"]
    result = {"argv": argv, "turns": turns, "transcript": process.stdout, "trace": trace_rows,
              "checkpoint": snapshot(path, flags)}
    return path, result


def snapshot(path, flags):
    if flags == SETUP["WORK"]:
        owner, fixture = SurfaceWaterApplication, create_surface_fixture(shared_workbench=True)
        tracked = ("repair-board", "repair-peg", "repair-cord", "strip")
    elif flags == SETUP["ACTIVITIES"]:
        owner, fixture = ActivityApplication, create_activity_fixture(activity_case="reference")
        tracked = ("work-panel", "barrier-crossbar", "work-cord")
    else:
        owner, fixture = StructuresApplication, create_structures_fixture()
        tracked = ("work-panel", "barrier-crossbar", "work-cord")
    app = owner.restore(fixture=fixture, checkpoint_path=path)
    custody = {}
    for name in tracked:
        if identity(name) in {entry.entity_id for entry in fixture.object_presentations}:
            relation = placement(app.state.representation, identity(name))
            custody[name] = (relation.relation_type, relation.object_entity_id)
    records = [asdict(event) for event in app.evidence_state.events
               if event.actor_id == fixture.player_entity_id and event.facet == "assembly"]
    return {"place": app.current_place_id(), "time": app.runtime_state.logical_time_state.logical_position,
            "custody": custody, "connections": [asdict(connection) for connection in app.connections],
            "agreements": [asdict(record) for record in app.participation_state.records],
            "player_evidence": records, "authoritative_digest": app.authoritative_digest(),
            "checkpoint_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def interactions(journey, utterance=None):
    return [row for row in journey["trace"] if row["record_type"] == "interaction"
            and (utterance is None or row["raw_player_input"].strip() == utterance)]


def score(case, journey, continued):
    rows = interactions(journey, case["intent"])
    output = " ".join(row["player_visible_output"] for row in rows)
    changed = [row for row in rows if row["authoritative_changed"]]
    effects = [row["result_type"] for row in changed]
    failure = {row["failure_class"] for row in rows}
    key = case["id"]
    cue, expected = {
        "open-firsthand": ("was open at step 6", ["inspection", "movement_committed"]),
        "closed-firsthand": ("condition was false", ["inspection"]),
        "stale-source": ("Proceeding under the named account condition", []),
        "no-witness": ("condition is still unknown", []),
        "request-and-external-work": ("Acceptance reserves no materials", ["material_observation", "actor_participation"]),
        "same-state-new-standard": ("condition was false", ["inspection"]),
        "advice": ("This preview spends no time", []),
        "disagreement": ("These accounts differ", ["inspection"]),
        "work-already-done": ("condition was false", ["material_observation"]),
        "protect-participant": ("can't guarantee that placement", ["material_observation"]),
    }[key]
    correct = cue in output and effects == expected
    if key == "stale-source":
        correct &= "material_passage_obstructed" in failure and "at step 6" in output
    if key == "closed-firsthand":
        correct &= "Tali Ren reported" in output
    if key == "no-witness":
        correct &= "actor_report_evidence_unavailable" in failure
    recovery = False
    if continued and len(journey["checkpoint"]["agreements"]) == len(continued["checkpoint"]["agreements"]) == 1:
        accepted, = journey["checkpoint"]["agreements"]
        completed, = continued["checkpoint"]["agreements"]
        recovery = (
            accepted["status"] == "active" and not accepted["contributions"]
            and completed["status"] == "externally_satisfied" and not completed["contributions"]
            and accepted["actor_id"] == completed["actor_id"]
            and journey["checkpoint"]["custody"]["strip"] == continued["checkpoint"]["custody"]["strip"]
            and "no retained account in this conversation" in continued["transcript"]
            and len(continued["checkpoint"]["connections"]) == 1
        )
    if continued:
        correct &= recovery
    unsafe_observation = key == "advice" and bool(changed)
    wrong = effects != expected[:len(effects)]
    return {"correct": correct, "wrong_commitment": wrong, "private_disclosure": (
                key == "no-witness" and ("was open" in output or "was closed" in output)
            ), "false_unsupported": not correct and not any(
                str(row["parsed_action"]).startswith("intent_condition") for row in rows
            ), "unnecessary_clarification": key != "disagreement" and (
                "Choose one" in output or "Choose whom" in output or "Choose which" in output
            ), "missing_constraint": unsafe_observation or (wrong and key in {
                "protect-participant", "work-already-done", "same-state-new-standard", "closed-firsthand",
            }), "recovery_after_interruption": recovery}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-launcher", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = CORPUS.read_bytes()
    specification = json.loads(source)
    candidate = shutil.which("myravant-play")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    j = SETUP
    profiles = {
        "open": (j["ACCESS"], j["OPEN"]),
        "closed-with-open-report": (j["ACCESS"], (*j["OPEN"], j["REPORT"], *j["BLOCK"])),
        "remote-bench": (j["ACTIVITIES"], j["REMOTE"]),
        "bench-supported": (j["WORK"], j["BENCH"]),
        "bench-fitted": (j["WORK"], (*j["BENCH"], *j["FIT"])),
    }
    comparisons = []
    with tempfile.TemporaryDirectory(prefix="myravant-condition-pairs-") as directory:
        root = Path(directory)
        (root / "sitecustomize.py").write_text(OFFLINE, encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(root), MYRAVANT_SAVE_DIR=str(root))
        for launcher in (candidate, args.baseline_launcher):
            canary = subprocess.run([os.fspath(Path(launcher).with_name("python")), "-c",
                                     "import socket; socket.create_connection(('127.0.0.1', 9))"],
                                    env=env, capture_output=True, check=False)
            assert canary.returncode and b"Network disabled for Myravant installed evidence" in canary.stderr
        for case in specification["cases"]:
            folder = root / case["id"]
            folder.mkdir()
            flags, setup = profiles[case["setup"]]
            item = {"case": case}
            for side, launcher, sha in (("baseline", args.baseline_launcher, specification["base"]),
                                        ("candidate", candidate, head)):
                restart = case["id"] == "request-and-external-work"
                turns = (*setup, case["intent"], *(("Cancel that",) if restart else ()))
                path, journey = run(launcher, sha, folder, side, flags, turns, env)
                resumed = None
                if restart:
                    _, resumed = run(launcher, sha, folder, f"{side}-load", flags, (
                        "Whose account was that?", *j["FIT"], "ask oren kesh about work",
                        "Ask Tali whether the workshop assembly is fitted.",
                    ), env, path=path)
                item[side] = {"original": journey, "reloaded": resumed}
                item[f"{side}_score"] = score(case, journey, resumed)
            comparisons.append(item)
    summary = {}
    for side in ("baseline", "candidate"):
        summary[side] = {}
        for cohort in ("acceptance", "new-phrasing"):
            rows = [item[f"{side}_score"] for item in comparisons if item["case"]["cohort"] == cohort]
            counts = Counter()
            for row in rows:
                counts.update(row)
            summary[side][cohort] = {"cases": len(rows), **dict(counts)}
    report = {"baseline_sha": specification["base"], "candidate_sha": head,
              "expectations_sha256": hashlib.sha256(source).hexdigest(), "authorship": specification["authorship"],
              "offline": "network socket calls disabled in each installed client", "summary": summary,
              "comparisons": comparisons}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
