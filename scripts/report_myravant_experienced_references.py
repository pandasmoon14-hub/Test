"""Compare experienced-reference utterances on installed, source-pinned clients."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, replace
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from report_myravant_player_intentions import CASES as PREVIOUS_CASES
from report_myravant_player_intentions import Case, control_cases, installed, repository_sha, score


BASE = "f939fd4809a4fd0a5f3566222e16f9ca02ddf038"
PLACES = {
    "worksite": ("--locality", "generated-worksite", "--generated-case", "access",
                 "--generated-seed", "0", "--generated-scale", "1"),
    "tarrow": ("--locality", "tarrow-actors"),
    "development": (),
}


@dataclass(frozen=True)
class Exchange:
    id: str
    place: str
    setup: tuple[str, ...]
    words: tuple[str, ...]
    control: tuple[str, ...] = ()
    cues: tuple[str, ...] = ()
    withheld: tuple[str, ...] = ()
    questions: int = 0
    boundary: bool = False


TALI = ("go south", "go west", "wait")
GIVE = ("take lantern", "go south", "wait", "give lantern to groundskeeper",
        "ask groundskeeper for lantern")
HISTORY = ("inspect brush", "ask jun about brush placement", "go west")
AWAY = ("inspect brush", "go west")
FRESH = (
    Exchange("past-sight", "worksite", AWAY, ("Head to the spot where we last saw the brush.",),
             ("go east",), ("You move to the Workshop.",)),
    Exchange("past-report", "worksite", HISTORY, ("Head to the place where I heard about the brush.",),
             ("go east",), ("You move to the Workshop.",)),
    Exchange("unheard-landmark", "worksite", AWAY, ("Head to the place where I heard about the brush.",),
             cues=("can't identify a known destination",), questions=1, boundary=True),
    Exchange("present", "worksite", AWAY, ("Is the brush there now?",),
             cues=("don't know its current location",), boundary=True),
    Exchange("historical", "worksite", AWAY, ("Was the brush there last time?",),
             cues=("You saw Brush at Workshop",), withheld=("current location",)),
    Exchange("fetch-without-sight", "worksite", AWAY, ("Where is the brush now?", "Go fetch it."),
             cues=("don't know its current location", "don't know where to get"), boundary=True),
    Exchange("direct-account", "tarrow", TALI, ("Ask Tali if she saw the cleaning brush.",),
             ("ask tali ren about cleaning brush placement",), ("historical witnessed evidence",)),
    Exchange("secondhand-account", "tarrow", TALI, ("Ask Tali if she heard about the cleaning brush.",),
             cues=("No retained reported evidence",), withheld=("historical witnessed evidence",),
             boundary=True),
    Exchange("request-custody", "tarrow", TALI, ("Ask Tali for the cleaning brush.",),
             ("ask tali ren for cleaning brush",), ("Give completed",)),
    Exchange("return-to-giver", "development", GIVE,
             ("Bring the lantern back to the one who gave it to me.",),
             ("give lantern to groundskeeper",), ("You hand the Brass Lantern to the Groundskeeper.",)),
    Exchange("received-as-loan", "development", GIVE,
             ("Bring the lantern back to the one who lent it to me.",),
             cues=("no evidence here of a loan",), boundary=True),
    Exchange("given-as-loan", "development", GIVE,
             ("Bring the lantern back to the one who borrowed it from me.",),
             cues=("no evidence here of a loan",), boundary=True),
    Exchange("recipient-absent", "development", (*GIVE, "go north"),
             ("Bring the lantern back to the one who gave it to me.",),
             cues=("Groundskeeper was at Yard", "can't reach that person here"), boundary=True),
    Exchange("find-exchange-place", "development", (*GIVE, "go north"),
             ("Lead me to where he gave the lantern to me.", "Give the lantern to the person who gave it to me."),
             ("go south", "give lantern to groundskeeper"),
             ("You move to the Yard.", "You hand the Brass Lantern to the Groundskeeper.")),
    Exchange("reply-without-action", "worksite", (),
             ("Rear panel, please.",), withheld=("Removable residue:",), boundary=True),
    Exchange("answer-after-travel", "worksite", ("go west",),
             ("Head for Workshop and examine the panel by the door.", "The back one, please.",
              "The rear panel, please."),
             ("go east", "inspect panel b"), ("Which panel", "Panel B"), questions=1),
    Exchange("answer-after-travel-short", "worksite", ("go west",),
             ("Head back to the workshop and examine the panel beside the door.", "The rear one, please."),
             ("go east", "inspect panel b"), ("Which panel", "Neutral declared panel-b"), questions=1),
    Exchange("unsupported-condition", "worksite", AWAY,
             ("Head to the spot where I saw the brush without being seen.",),
             cues=("can't guarantee that constraint",), boundary=True),
    Exchange("tool-reuse", "worksite", ("take brush", "scrub panel a using brush"),
             ("Scrub the rear one with the tool I used earlier.",),
             ("scrub panel b using brush",), ("Scrub: Panel B to Brush.",)),
)

# Five original engineering misses plus the six committed held-out misses.
# Any unresolved cases retain their original utterances and controls.
PREVIOUS_MISSES = tuple(case for case in PREVIOUS_CASES if case.id in {"A01", "A04", "A11", "A13", "A17"}) + (
    Case("HA03", "A", ("Go to Work Annex 1 and examine the wing-one panel.",), "effect",
         control=("go east", "inspect wing 1 panel")),
    Case("HA04", "A", ("Can Jun tell me if those things were tied together?",), "effect",
         setup=("inspect plate",), control=("ask jun about plate assembly",)),
    Case("HA05", "A", ("Tell Sol the cloth is dry.",), "effect",
         control=("tell sol that {cloth} moisture is dry",)),
    Case("HA07", "A", ("I would like to look at the rear panel, please.",), "effect",
         control=("inspect panel b",)),
    Case("HA08", "A", ("Could I be shown the way back?",), "inquiry",
         setup=("go west",), cue="Known way to Workshop"),
    Case("HA11", "A", ("Go to the room where we just saw the brush.",), "effect",
         setup=("go west",), control=("go east",)),
)
QUESTIONS = {"ambiguous_input", "intent_clarification", "intent_route_choice"}
UNSUPPORTED = {"unsupported_input", "uninterpretable_input", "intent_unknown_question",
               "intent_context_blocked", "intent_missing_mechanic"}


def run(launcher, sha, folder, name, case, script):
    folder.mkdir(parents=True, exist_ok=True)
    trace = folder / f"{name}.jsonl"
    argv = [launcher, *PLACES[case.place], "--repository-sha", sha,
            "--checkpoint", str(folder / f"{name}.json"), "--trace", str(trace)]
    commands = (*case.setup, *script, "exit")
    output = subprocess.run(argv, input="\n".join((*commands, "")), check=True,
                            capture_output=True, encoding="utf-8", timeout=120)
    records = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    assert records[-1]["evidence_complete"]
    rows = [row for row in records if row["record_type"] == "interaction"]
    assert [row["raw_player_input"].strip() for row in rows[:len(case.setup)]] == list(case.setup)
    actions = rows[len(case.setup):]
    assert all(row["raw_player_input"].strip() in script for row in actions)
    return {"argv": argv, "commands": commands, "transcript": output.stdout,
            "setup_length": len(case.setup), "rows": records, "actions": actions,
            "final_state": records[-1]["final_state_digest"]}


def effects(rows):
    canonical = ("receipt_id", "logical_time_before", "logical_time_after",
                 "post_state_digest", "due_process_ref")
    return [tuple(row[key] for key in canonical) for row in rows if row["authoritative_changed"]]


def evaluate(case, result, control):
    rows = result["actions"]
    rendered = "".join(row["player_visible_output"] for row in rows).casefold()
    prohibited = any(text.casefold() in rendered for text in case.withheld)
    actual, expected = effects(rows), effects(control["actions"])
    boundary = any("without " in line for line in case.words)
    wrong = actual != expected[:len(actual)]
    questions = sum(row["failure_class"] in QUESTIONS for row in rows)
    cues_match = all(text.casefold() in rendered for text in case.cues)
    correct = (actual == expected and result["final_state"] == control["final_state"]
               and cues_match and not prohibited and questions == case.questions)
    return {
        "correct_routing": correct,
        "wrong_commitments": wrong,
        "false_unsupported": not case.boundary and not correct
        and any(row["failure_class"] in UNSUPPORTED for row in rows),
        "unnecessary_questions": questions > case.questions,
        "meaningful_constraints_lost": bool(actual and boundary),
        "prohibited_disclosure": prohibited,
    }


def summarize(sides, key):
    return {"cases": len(sides), **{name: sum(case[key][name] for case in sides)
                                  for name in sides[0][key]}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline-launcher", required=True)
    args = parser.parse_args()
    candidate = shutil.which("myravant-play")
    assert candidate
    head = repository_sha()

    def fresh(pair):
        folder, case = pair
        control = run(candidate, head, folder, "canonical", case, case.control)
        assert not case.control or control["actions"]
        result = {"case": asdict(case), "canonical": control}
        for side, launcher, sha in (("baseline", args.baseline_launcher, BASE),
                                    ("candidate", candidate, head)):
            record = run(launcher, sha, folder, side, case, case.words)
            result[side] = record
            result[side + "_score"] = evaluate(case, record, control)
        return result

    def regression(pair):
        folder, case = pair
        folder.mkdir(parents=True)
        control = installed(candidate, folder, "canonical", case, case.control, head) if case.control else None
        result = {"case": asdict(case), "canonical": control}
        for side, launcher, sha in (("baseline", args.baseline_launcher, BASE),
                                    ("candidate", candidate, head)):
            record = installed(launcher, folder, side, case, case.input, sha)
            result[side] = record
            result[side + "_score"] = score(case, record, control)
        return result

    with tempfile.TemporaryDirectory(prefix="myravant-reference-assessment-") as tmp:
        root = Path(tmp)
        with ThreadPoolExecutor(max_workers=3) as workers:
            fresh_results = list(workers.map(fresh, ((root / case.id, case) for case in FRESH)))
            regs = [case for case in control_cases(PREVIOUS_MISSES)]
            # The original held-out evaluator resolves its exact admitted cloth identity.
            from astra_runtime.myravant_generated_locality import LocalityRecipe, create_generated_locality_fixture
            fixture = create_generated_locality_fixture(LocalityRecipe("access", scale_level=1))
            cloth = next(x.entity_id.rsplit(":", 1)[-1] for x in fixture.object_presentations if x.name == "Cloth")
            regs = [replace(c, control=tuple(t.format(cloth=cloth) for t in c.control)) for c in regs]
            regression_results = list(workers.map(regression, ((root / case.id, case) for case in regs)))
    report = {
        "candidate_sha": head, "baseline_sha": BASE,
        "authorship": "Codex implementation author, written after the initial implementation on 2026-11-24",
        "independent_ac04": False,
        "fresh_cases": fresh_results, "retained_predecessor_misses": regression_results,
        "fresh_summary": {side: summarize(fresh_results, side + "_score") for side in ("baseline", "candidate")},
        "regression_summary": {side: summarize(regression_results, side + "_score")
                               for side in ("baseline", "candidate")},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"fresh": report["fresh_summary"], "retained": report["regression_summary"]}, indent=2))


if __name__ == "__main__":
    main()
