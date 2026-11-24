"""Source-pinned engineering assessment of the installed intent boundary."""

import argparse
from collections import Counter
from dataclasses import dataclass, replace
from hashlib import sha256
import json
from pathlib import Path
import shutil
from statistics import median
import subprocess
import tempfile
from time import perf_counter_ns


@dataclass(frozen=True)
class Case:
    id: str
    cohort: str
    input: tuple[str, ...]
    expected: str
    setup: tuple[str, ...] = ()
    control: tuple[str, ...] = ()
    cue: str = ""
    canary: str = ""
    locality: str = "generated"


# Engineering-authored assessment. The 39-case legacy assessment is run
# independently using its own original inputs and scoring.
CASES = (
    Case("A01", "A", ("I can go to the Entrance, right?",), "inquiry", cue="Known way"),
    Case("A02", "A", ("Please head towards the Entrance.",), "effect", control=("go west",)),
    Case("A03", "A", ("I'll make my way back to where I came from.",), "effect",
         setup=("go west",), control=("go east",)),
    Case("A04", "A", ("Proceed to the Entrance.",), "effect", control=("go west",)),
    Case("A05", "A", ("Please grab the rag.",), "effect", control=("take cloth",)),
    Case("A06", "A", ("Let me examine the rear panel.",), "effect", control=("inspect panel b",)),
    Case("A07", "A", ("I want to look at the panel.", "No, the front one."), "effect",
         control=("inspect panel a",), cue="Which object do you mean?"),
    Case("A08", "A", ("I'd like to inspect the panel.",), "clarify", cue="Panel A, Panel B"),
    Case("A09", "A", ("Ask Sol whether the rear panel looked sooty.",), "effect",
         setup=("wait",), control=("ask sol about panel b residue",)),
    Case("A10", "A", ("Tell Jun that the rag looks wet.",), "effect",
         control=("tell jun that cloth moisture is wet",)),
    Case("A11", "A", ("I'd like to brush the front panel with this tool.",), "effect",
         setup=("take brush",), control=("scrub panel a using brush",)),
    Case("A12", "A", ("Walk to Workshop and ask Jun whether the front panel was dirty.",), "effect",
         setup=("go west",), control=("go east", "ask jun about panel a residue")),
    Case("A13", "A", ("Let's set off for the Store.",), "effect", setup=("go west",),
         control=("go west",)),
    Case("A14", "A", ("How do I get back?",), "inquiry", setup=("go west",), cue="Known way to Workshop"),
    Case("A15", "A", ("Please check the sorting board.", "Did she notice it dirty?"), "effect",
         setup=("go south", "go west", "inspect tali ren"),
         control=("inspect sorting board", "ask tali ren about sorting board residue"), locality="tarrow"),
    Case("A16", "A", ("I'd like to go to Yard Tool Station.", "Look closely at the sorting board.",
                      "Return to Wayhouse Common."), "effect",
         setup=("go south",), control=("go west", "inspect sorting board", "go east", "go north"),
         locality="tarrow"),
    Case("A17", "A", ("Please untie this fastening.",), "effect", setup=("inspect cord",),
         control=("untie cord",)),
    Case("A18", "A", ("Put the plate on the bench.",), "effect",
         setup=("untie cord", "lift plate from bench",), control=("put plate on bench",)),
    Case("B01", "B", ("Sprint back to the Entrance.",), "frontier"),
    Case("B02", "B", ("Get to the Store without Jun seeing me.",), "frontier"),
    Case("B03", "B", ("Don't pick up the brush.",), "frontier"),
    Case("B04", "B", ('"I take the cloth."',), "frontier"),
    Case("B05", "B", ("If the cloth were wetter, take it.",), "frontier"),
    Case("B06", "B", ("Please melt the cord into a key.",), "frontier"),
    Case("B07", "B", ("Could I clean the front panel without losing any water?",), "frontier"),
    Case("B08", "B", ("Did Tali see it dry?",), "frontier", locality="tarrow", canary="Tali Ren reports"),
    Case("B09", "B", ("I'd like to pick up the soft iron pin blank.",), "frontier",
         locality="tarrow", canary="Soft-Iron Pin Blank"),
    Case("B10", "B", ("Have Jun clean both panels simultaneously.",), "frontier"),
)

FLAGS = {
    "generated": ("--locality", "generated-worksite", "--generated-case", "access",
                  "--generated-seed", "0", "--generated-scale", "1"),
    "tarrow": ("--locality", "tarrow-actors"),
}
UNSUPPORTED = {"unsupported_input", "uninterpretable_input", "intent_unknown_question",
               "intent_missing_mechanic", "intent_context_blocked"}
QUESTIONS = {"ambiguous_input", "intent_clarification", "intent_route_choice"}


def installed(launcher, root, stem, case, commands, source):
    save, trace = (root / (stem + suffix) for suffix in (".json", ".jsonl"))
    argv = [launcher, *FLAGS[case.locality], "--checkpoint", str(save), "--trace", str(trace),
            "--repository-sha", source]
    inputs = (*case.setup, *commands, "exit")
    result = subprocess.run(argv, input="\n".join((*inputs, "")), capture_output=True,
                            encoding="utf-8", timeout=120)
    if result.returncode:
        raise RuntimeError((argv, result.stderr, result.stdout))
    rows = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    assert rows[-1]["evidence_complete"]
    selected = [row for row in rows if row["record_type"] == "interaction"][len(case.setup):]
    assert selected and all(row["raw_player_input"].strip() in commands for row in selected)
    return {
        "argv": argv, "inputs": inputs, "stdout": result.stdout, "trace": rows, "attempts": selected,
        "checkpoint_sha256": sha256(save.read_bytes()).hexdigest(),
        "final_world": rows[-1]["final_state_digest"],
    }


def score(case, actual, control):
    attempts = actual["attempts"]
    committed = [row for row in attempts if row["authoritative_changed"]]
    failures = {row["failure_class"] for row in attempts}
    result_types = {row["result_type"] for row in attempts}
    rendered = "".join(row["player_visible_output"] for row in attempts)
    changed = bool(committed)
    clarification = bool((failures | result_types) & QUESTIONS)
    cue = not case.cue or case.cue.casefold() in rendered.casefold()
    disclosure = bool(case.canary and case.canary in rendered)
    invented = any(row["receipt_id"] is None for row in committed)
    if case.expected == "effect":
        signature = ("receipt_id", "logical_time_after", "post_state_digest", "due_process_ref")
        expected = [row for row in control["attempts"] if row["authoritative_changed"]]
        correct = bool(expected) and actual["final_world"] == control["final_world"] and [
            tuple(row[key] for key in signature) for row in committed
        ] == [tuple(row[key] for key in signature) for row in expected] and cue
    elif case.expected == "frontier":
        correct = not changed and not disclosure
    else:
        correct = not changed and cue and (clarification == (case.expected == "clarify"))
    unexpected_questions = sum(
        (row["failure_class"] in QUESTIONS or row["result_type"] in QUESTIONS)
        for row in attempts
    ) if not case.cue.startswith("Which") and case.expected != "clarify" and case.cohort == "A" else 0
    return {
        "correct": correct, "false_unsupported": case.cohort == "A" and not correct
        and bool((result_types | failures) & UNSUPPORTED),
        "unnecessary_clarifications": unexpected_questions,
        "wrong_action": changed and not correct,
        "dropped_constraint": changed and any("without " in line.casefold() for line in case.input),
        "hidden_disclosure": disclosure,
        "fabricated_or_unreceipted_effect": invented,
    }


def latency():
    from astra_runtime.myravant_generated_locality import LocalityRecipe, build_generated_locality
    from astra_runtime.myravant_player_intentions import Intent, IntentSession
    from astra_runtime.myravant_terminal import parse_terminal_command

    app, _ = build_generated_locality(LocalityRecipe("access"))
    session = IntentSession(app)
    session.context.route_labels()
    inputs = ("I'd like to check the rear panel.", "Head over to Entrance.",
              "Did Sol see the cloth dry?", "Ask Jun to clean Panel A using Brush.")
    samples = {"legacy_parse": [], "parse_and_propose": [], "owner_move": []}
    for index in range(128):
        raw = inputs[index % len(inputs)]
        start = perf_counter_ns()
        parsed = parse_terminal_command(raw)
        ended = perf_counter_ns()
        session.offer(raw, parsed)
        samples["legacy_parse"].append((ended - start) / 1_000_000)
        samples["parse_and_propose"].append((perf_counter_ns() - start) / 1_000_000)
    for _ in range(12):
        app, _ = build_generated_locality(LocalityRecipe("access"))
        start = perf_counter_ns()
        result = app.move("west", method="walk")
        assert result.authoritative_changed
        samples["owner_move"].append((perf_counter_ns() - start) / 1_000_000)
    return {name: {"n": len(values), "median_ms": median(values),
                   "p95_ms": sorted(values)[int(.95 * (len(values) - 1))]}
            for name, values in samples.items()}


def summarize(records, side):
    return {cohort: {
        "cases": len(group),
        "unambiguous_cases": sum(r["expected"] in {"inquiry", "effect"} and not r["required_clarification"]
                                for r in group),
        **Counter({key: sum(r[side]["score"][key] for r in group)
                   for key in group[0][side]["score"]}),
    } for cohort in ("A", "B") if (group := [r for r in records if r["cohort"] == cohort])}


def repository_sha():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def control_cases(cases):
    from astra_runtime.myravant_generated_locality import LocalityRecipe, create_generated_locality_fixture

    fixture = create_generated_locality_fixture(LocalityRecipe("access", scale_level=1))
    # Bare 'cloth' also matches the annex cloth in the legacy owner resolver.
    # The canonical control uses the existing exact object reference instead.
    cloth = next(item.entity_id.rsplit(":", 1)[-1] for item in fixture.object_presentations
                 if item.name == "Cloth")
    controls = {"A05": (f"take {cloth}",), "A10": (f"tell jun that {cloth} moisture is wet",)}
    return (replace(case, control=controls[case.id]) if case.id in controls else case for case in cases)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--baseline-launcher")
    parser.add_argument("--baseline-sha")
    args = parser.parse_args()
    if bool(args.baseline_launcher) != bool(args.baseline_sha):
        parser.error("provide the baseline launcher and its exact source SHA together")
    head = repository_sha()
    launcher = shutil.which("myravant-play")
    assert launcher
    records = []
    with tempfile.TemporaryDirectory(prefix="myravant-grounded-evaluation-") as directory:
        root = Path(directory)
        for case in control_cases(CASES):
            ref = (installed(launcher, root, case.id + "-control", case, case.control, head)
                   if case.control else None)
            observed = installed(launcher, root, case.id + "-head", case, case.input, head)
            record = {"id": case.id, "cohort": case.cohort, "expected": case.expected,
                      "required_clarification": case.cue.startswith("Which"), "control": ref,
                      "candidate": {"run": observed, "score": score(case, observed, ref)}}
            if args.baseline_launcher:
                run = installed(args.baseline_launcher, root, case.id + "-base", case,
                                case.input, args.baseline_sha)
                record["baseline"] = {"run": run, "score": score(case, run, ref)}
            records.append(record)
    summary = {"candidate": summarize(records, "candidate")}
    if args.baseline_launcher:
        summary["baseline"] = summarize(records, "baseline")
    document = {"repository_sha": head, "baseline_sha": args.baseline_sha, "engineering_authored": True,
                "independent_or_human_acceptance": False, "provider_calls": 0,
                "latency": latency(), "summary": summary, "cases": records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
