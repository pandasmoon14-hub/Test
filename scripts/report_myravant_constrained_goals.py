"""Score predeclared offline goal exchanges against #583 and owner controls."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_generated_locality import LocalityRecipe, create_generated_locality_fixture
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_timed_application import TimedApplication
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests/fixtures/myravant_goals/held_out.json"
JOURNEYS = runpy.run_path(str(ROOT / "tests/test_play_constrained_goals.py"))
OFFLINE = """import socket

def denied(*args, **kwargs):
    raise OSError("Network disabled for Myravant installed evidence")

socket.create_connection = denied
socket.socket.connect = denied
socket.socket.connect_ex = denied
socket.socket.sendto = denied
socket.getaddrinfo = denied
"""
UNSUPPORTED = {"unsupported_input", "uninterpretable_input", "intent_unknown_question",
               "intent_feasibility_unavailable", "intent_constraint_unavailable", "goal_reference_unavailable"}
CLARIFICATIONS = {"ambiguous_input", "intent_clarification", "intent_route_choice"}


def profiles():
    j = JOURNEYS
    return {
        "giver-local": ((), j["LOCAL"]),
        "giver-away": ((), j["AWAY"]),
        "stored-open": ((), j["OPEN_STORED"]),
        "holder-local": ((), j["GIVE"]),
        "wet-both": (j["TIMED"], (*j["DRY_BOTH"], j["WET"], j["SCRUB"])),
        "dry-both": (j["TIMED"], j["DRY_BOTH"]),
        "dry-cloth-basin": (j["TIMED"], j["BASIN"]),
        "panels": (j["GEN"], ("go west",)),
    }


def snapshot(path, flags):
    if flags == JOURNEYS["TIMED"]:
        app = TimedApplication.restore(checkpoint_path=path)
    elif flags == JOURNEYS["GEN"]:
        fixture = create_generated_locality_fixture(LocalityRecipe("access", scale_level=1))
        app = InvestigationApplication.restore(fixture=fixture, checkpoint_path=path)
    else:
        app = MyravantVSM14Application.restore(checkpoint_path=path)
    clock = app.runtime_state.logical_time_state.logical_position
    if not flags:
        item = app.fixture.resolve_object_reference("lantern")
        relation = placement(app.state.representation, item)
        tracked = {"lantern": [relation.relation_type, relation.object_entity_id]}
    else:
        tracked = {
            "water": dict(app.water_state.water),
            "removable_residue": {key: str(value) for key, value in app.water_state.adhered},
        }
    return {"place": app.current_place_id(), "time": clock, "tracked_state": tracked,
            "authoritative_digest": app.authoritative_digest(),
            "checkpoint_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def installed(binary, sha, root, stem, flags, setup, commands, env):
    checkpoint, trace = (root / f"{stem}{ext}" for ext in (".json", ".jsonl"))
    argv = [binary, *flags, "--repository-sha", sha, "--checkpoint", str(checkpoint), "--trace", str(trace)]
    result = subprocess.run(argv, input="\n".join((*setup, *commands, "exit", "")), env=env,
                            capture_output=True, check=True, encoding="utf-8", timeout=120)
    records = [json.loads(line) for line in trace.read_text().splitlines()]
    assert records[-1]["evidence_complete"]
    rows = [row for row in records if row["record_type"] == "interaction"]
    assert [row["raw_player_input"].strip() for row in rows[:len(setup)]] == list(setup)
    assert all(row["raw_player_input"].strip() in commands for row in rows[len(setup):])
    return {"argv": argv, "setup": setup, "commands": commands, "transcript": result.stdout,
            "trace": records, "actions": rows[len(setup):], "checkpoint": snapshot(checkpoint, flags)}


def effects(rows):
    keys = ("receipt_id", "logical_time_before", "logical_time_after", "post_state_digest", "due_process_ref")
    return [tuple(row[key] for key in keys) for row in rows if row["authoritative_changed"]]


def score(case, attempt, control):
    rows = attempt["actions"]
    rendered = "\n".join(row["player_visible_output"] for row in rows).casefold()
    canary = any(term.casefold() in rendered for term in case.get("withhold", ()))
    actual, expected = effects(rows), effects(control["actions"])
    # A concise command present in both journeys is separately authorized.
    # An earlier missed goal step can change its digest without making it a wrong commitment.
    independent = set(case["turns"]) & set(control["commands"])
    goal_effects = effects(row for row in rows if row["raw_player_input"].strip() not in independent)
    goal_controls = effects(row for row in control["actions"]
                            if row["raw_player_input"].strip() not in independent)
    wrong = goal_effects != goal_controls[:len(goal_effects)]
    questions = sum(bool({row["failure_class"], row["result_type"]} & CLARIFICATIONS) for row in rows)
    cue = all(expected_text.casefold() in rendered for expected_text in case["cues"])
    recovery = case.get("recovery", False)
    correct = (actual == expected and attempt["checkpoint"]["authoritative_digest"]
               == control["checkpoint"]["authoritative_digest"] and cue and not canary)
    constrained = any(any(term in line.casefold() for term in ("without ", "reserve", "leave at least ", "stop if"))
                      for line in case["turns"])
    return {
        "correct": correct,
        "wrong_commitment": wrong,
        "false_unsupported": not correct and case["id"] != "unsupported-constraint"
        and any({row["failure_class"], row["result_type"]} & UNSUPPORTED for row in rows),
        "unnecessary_clarification": questions > int(case["id"] == "reply-chain"),
        "missing_constraint": wrong and constrained,
        "private_disclosure": canary,
        "recovery_after_interruption": bool(recovery and correct),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-launcher", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    candidate = shutil.which("myravant-play")
    assert candidate
    specification = json.loads(CORPUS.read_bytes())
    baseline = specification["baseline"]
    bindings = profiles()
    with tempfile.TemporaryDirectory(prefix="myravant-goal-evidence-") as directory:
        root = Path(directory)
        (root / "sitecustomize.py").write_text(OFFLINE, encoding="utf-8")
        env = dict(os.environ, PYTHONPATH=str(root), MYRAVANT_SAVE_DIR=str(root))
        canary = subprocess.run([os.fspath(Path(candidate).with_name("python")), "-c",
                                 "import socket; socket.create_connection(('127.0.0.1', 9))"],
                                env=env, capture_output=True, check=False)
        assert canary.returncode and b"Network disabled for Myravant installed evidence" in canary.stderr

        def evaluate(case):
            folder = root / case["id"]
            folder.mkdir()
            flags, setup = bindings[case["profile"]]
            control = installed(candidate, head, folder, "owner", flags, setup, case["controls"], env)
            assert not case["controls"] or effects(control["actions"])
            assert not case.get("no_commit") or not effects(control["actions"])
            record = {"case": case, "owner_control": control}
            for label, launch, sha in (("baseline", args.baseline_launcher, baseline),
                                       ("candidate", candidate, head)):
                result = installed(launch, sha, folder, label, flags, setup, case["turns"], env)
                record[label] = result
                record[label + "_score"] = score(case, result, control)
            return record

        with ThreadPoolExecutor(max_workers=2) as workers:
            records = list(workers.map(evaluate, specification["cases"]))

    report = {
        "candidate_sha": head, "baseline_sha": baseline, "corpus_sha256": hashlib.sha256(CORPUS.read_bytes()).hexdigest(),
        "authorship": specification["authorship"], "independent_AC04": False, "outbound_sockets": "disabled",
        "cases": records, "summary": {
            side: {"cases": len(records), "recovery_cases": sum(bool(r["case"].get("recovery")) for r in records),
                   **{key: sum(r[side + "_score"][key] for r in records) for key in records[0][side + "_score"]}}
            for side in ("baseline", "candidate")
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
