"""#493: Execute authored ordinary-action pressure through the installed game.

This baseline measures *observed* route/outcome, not a universal intent oracle.
The case labels are reviewer-authored hypotheses, never automatic rules. The
report is not the 500 unseen Set A/B v1 acceptance corpus or human play.
Every case runs in an independent fresh campaign with full trace + checkpoint.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


@dataclass(frozen=True)
class Case:
    case_id: str
    family: str
    goal: str
    method: str
    target: str
    modifiers: str
    context: str
    attempt: str
    expectation: str  # representable, novelty, ambiguous; NOT actual result


# A deliberately small, authored baseline across families, NOT an unseen holdout.
# Novel inputs are content-independent pressure, not claims that the engine
# *should* grant success or that relevant material/anatomy/lore exists.
CASES = (
    Case("S01", "self_perception", "inspect self", "visual", "self", "", "workshop",
         "inspect myself", "representable"),
    Case("S02", "self_perception", "inspect present possessions", "body", "self",
         "", "workshop", "check my hands", "representable"),
    Case("S03", "self_perception", "examine posture", "introspect", "self",
         "", "workshop", "check whether I am crouching", "novelty"),
    Case("P01", "posture", "lower stance", "crouch", "self", "", "workshop",
         "crouch down", "novelty"),
    Case("P02", "posture", "rest body", "sit", "self", "on ground", "yard",
         "sit on the ground", "novelty"),
    Case("P03", "posture", "hold position", "stand still", "self", "", "yard",
         "stand still and listen", "novelty"),
    Case("M01", "traversal_method", "enter yard", "walk", "self", "south",
         "workshop", "walk south", "representable"),
    Case("M02", "traversal_method", "enter yard", "sprint", "self", "south",
         "workshop", "sprint south", "novelty"),
    Case("M03", "traversal_method", "enter yard", "sneak", "self", "south",
         "workshop", "sneak south", "novelty"),
    Case("M04", "traversal_method", "enter yard", "crawl", "self", "south",
         "workshop", "crawl south", "novelty"),
    Case("O01", "local_observation", "locate lantern", "look for", "lantern",
         "", "workshop", "look for lantern", "representable"),
    Case("O02", "local_observation", "inspect lantern", "visual", "lantern",
         "", "workshop", "look at the lantern", "representable"),
    Case("O03", "local_observation", "detect noise", "listen", "workshop",
         "", "workshop", "listen for movement outside", "novelty"),
    Case("O04", "local_observation", "sample scent", "smell", "lantern oil",
         "", "workshop", "smell the lantern oil", "novelty"),
    Case("I01", "object_placement", "take lantern", "pickup", "lantern",
         "", "workshop", "take lantern", "representable"),
    Case("I02", "object_placement", "discard lantern", "drop", "lantern",
         "not held", "workshop", "drop lantern", "representable"),
    Case("I03", "object_placement", "move chest", "push", "chest",
         "east", "yard", "push chest east", "representable"),
    Case("I04", "object_placement", "move chest", "pull", "chest",
         "north", "yard", "pull chest north", "novelty"),
    Case("I05", "object_placement", "adjust chest", "rotate", "chest",
         "", "yard", "turn the chest around", "novelty"),
    Case("F01", "object_operation", "inspect chest", "visual", "chest",
         "", "yard", "examine chest", "representable"),
    Case("F02", "object_operation", "open chest", "open", "chest",
         "", "yard", "open chest", "representable"),
    Case("F03", "object_operation", "secure chest latch", "manual work", "chest",
         "", "yard", "service chest latch", "representable"),
    Case("F04", "object_operation", "brace chest", "inspect component", "brace",
         "", "yard", "inspect chest brace", "representable"),
    Case("T01", "structure_transformation", "remove brace", "manual", "brace",
         "", "yard", "remove chest brace", "representable"),
    Case("T02", "structure_transformation", "disassemble chest", "dismantle",
         "chest", "", "yard", "dismantle the chest", "novelty"),
    Case("T03", "structure_transformation", "repair brace", "cloth wrap",
         "brace", "", "yard", "repair chest brace with cloth", "novelty"),
    Case("R01", "projected_placement", "send lantern away", "throw",
         "lantern", "east", "yard", "throw lantern east", "representable"),
    Case("R02", "projected_placement", "pass lantern", "toss to actor",
         "lantern", "groundskeeper", "yard_actor",
         "toss lantern to groundskeeper", "novelty"),
    Case("E01", "environment_improvisation", "block exit", "move waystone",
         "waystone", "", "orchard", "drag waystone west", "representable"),
    Case("E02", "environment_improvisation", "secure doorway",
         "wedge with object", "gatehouse", "", "yard",
         "wedge the doorway shut with a stone", "novelty"),
    Case("E03", "environment_improvisation", "signal actor", "light pulses",
         "lantern", "", "yard", "flash the lantern as a signal", "novelty"),
    Case("N01", "nonviolent_interaction", "record claim", "tell",
         "groundskeeper", "unverified gatehouse report", "yard_actor",
         "tell groundskeeper chest is at gatehouse", "representable"),
    Case("N02", "nonviolent_interaction", "request witness", "ask",
         "groundskeeper", "chest", "yard_actor",
         "ask groundskeeper to inspect chest", "representable"),
    Case("N03", "nonviolent_interaction", "warn actor", "warn",
         "groundskeeper", "obstruction", "yard_actor",
         "warn the groundskeeper about the blocked path", "novelty"),
    Case("D01", "time_duration", "advance time", "wait", "world",
         "one tick", "workshop", "wait", "representable"),
    Case("D02", "time_duration", "long rest", "sleep", "self",
         "until dawn", "workshop", "rest until dawn", "novelty"),
    Case("Q01", "sequencing", "move and inspect", "sequence", "self/chest",
         "two actions", "workshop", "go south then inspect chest", "novelty"),
    Case("Q02", "sequencing", "move while watching", "simultaneous", "self",
         "south + observation", "workshop",
         "walk south while watching the groundskeeper", "novelty"),
    Case("Q03", "sequencing", "repeat previous action", "repeat", "self",
         "last committed", "yard", "do that again", "ambiguous"),
)
CONTEXTS = {
    "workshop": (),
    "yard": ("go south",),
    "yard_actor": ("go south", "wait"),
    "orchard": ("go south", "go east"),
}
GENERIC_RESULTS = {"unsupported_input", "uninterpretable_input", "ambiguous_input"}
SUPPORTED_EXPECTATIONS = {"representable", "novelty", "ambiguous"}


def observed_class(case: Case, record: dict) -> str:
    result = record["result_type"]
    if result == "unsupported_input":
        return ("false_unsupported_candidate" if case.expectation == "representable"
                else "unsupported_novelty")
    if result == "uninterpretable_input":
        return "uninterpretable"
    if result == "ambiguous_input":
        return "clarification_needed"
    if record["authoritative_changed"]:
        return "executed"
    if record["failure_class"]:
        return "contextual_refusal"
    return "observed_no_change"


def execute_case(case: Case, root: Path, *, installed: str, repository_sha: str) -> dict:
    checkpoint = root / f"{case.case_id}.json"
    trace = root / f"{case.case_id}.jsonl"
    commands = (*CONTEXTS[case.context], case.attempt, "save", "exit")
    run = subprocess.run(
        [installed, "--checkpoint", str(checkpoint), "--trace", str(trace),
         "--repository-sha", repository_sha],
        input="\n".join((*commands, "")), text=True, capture_output=True, timeout=70,
    )
    if run.returncode != 0:
        raise AssertionError(
            f"Installed client failed for {case.case_id}: "
            f"{run.returncode}; {run.stderr[-2000:]}; {run.stdout[-2000:]}"
        )
    if not checkpoint.is_file() or not trace.is_file():
        raise AssertionError(f"Missing durable artifacts for {case.case_id}")
    rows = [json.loads(row) for row in trace.read_text(
        encoding="utf-8",
    ).splitlines()]
    assert rows[0]["record_type"] == "session_start"
    assert rows[-1]["record_type"] == "session_end"
    interactions = [r for r in rows if r["record_type"] == "interaction"]
    setup_count = len(CONTEXTS[case.context])
    attempted = interactions[setup_count:-1]
    # One player input can now contain exactly two independently recorded
    # original-owner operations. Count the attempt once; retain both receipts.
    assert len(attempted) in (1, 2), case.case_id
    assert len(interactions) == setup_count + len(attempted) + 1
    assert all(
        item["raw_player_input"] == case.attempt + "\\n"
        for item in attempted
    ), case.case_id
    assert interactions[-1]["raw_player_input"] == "save\\n"
    for index, item in enumerate(attempted):
        assert item["pre_state_digest"] and item["post_state_digest"]
        if item["authoritative_changed"]:
            assert item["pre_state_digest"] != item["post_state_digest"]
        else:
            assert item["pre_state_digest"] == item["post_state_digest"]
        if index:
            assert attempted[index - 1]["post_state_digest"] == (
                item["pre_state_digest"]
            )
    observed = attempted[-1]
    any_changed = any(item["authoritative_changed"] for item in attempted)
    failure = next(
        (item["failure_class"] for item in attempted if item["failure_class"]),
        None,
    )
    aggregate = {
        **observed,
        "authoritative_changed": any_changed,
        "failure_class": failure,
    }
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == interactions[-1]["post_state_digest"]
    assert restored.authoritative_digest() == observed["post_state_digest"]
    return {
        **asdict(case),
        "parsed_action": (
            " + ".join(item["parsed_action"] for item in attempted)
            if len(attempted) > 1 else observed["parsed_action"]
        ),
        "result_type": observed["result_type"],
        "failure_class": failure,
        "authoritative_changed": any_changed,
        "partial_failure": bool(any_changed and failure),
        "outcome": observed_class(case, aggregate),
        "player_visible_output": "".join(
            item["player_visible_output"] for item in attempted
        ),
        "pre_state_digest": attempted[0]["pre_state_digest"],
        "post_state_digest": observed["post_state_digest"],
        "step_count": len(attempted),
        "route_steps": [
            {
                "parsed_action": item["parsed_action"],
                "result_type": item["result_type"],
                "failure_class": item["failure_class"],
                "authoritative_changed": item["authoritative_changed"],
                "pre_state_digest": item["pre_state_digest"],
                "post_state_digest": item["post_state_digest"],
            }
            for item in attempted
        ],
        "checkpoint_sha256": sha256(checkpoint.read_bytes()).hexdigest(),
        "trace_sha256": sha256(trace.read_bytes()).hexdigest(),
        "setup_input": list(CONTEXTS[case.context]),
    }


def run_baseline(*, output: Path, cases=CASES) -> dict:
    binary = shutil.which("myravant-play")
    assert binary, "Installed myravant-play entrypoint is required"
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=True, text=True,
        capture_output=True, timeout=15,
    ).stdout.strip()
    cases = tuple(cases)
    assert len({c.case_id for c in cases}) == len(cases)
    assert all(c.context in CONTEXTS and c.expectation in SUPPORTED_EXPECTATIONS
               for c in cases)
    rows = []
    with tempfile.TemporaryDirectory(prefix="myravant-coverage-") as d:
        for case in cases:
            rows.append(execute_case(
                case, Path(d), installed=binary, repository_sha=head,
            ))
    tally = Counter(row["outcome"] for row in rows)
    families = defaultdict(Counter)
    for row in rows:
        families[row["family"]][row["outcome"]] += 1
    summary = {
        "schema": "myravant.action_coverage_discovery.v1",
        "repository_sha": head,
        "evidence_kind": "author_curated_installed_game_independent_campaign_probes",
        "not_independent_blind_set_a_b": True,
        "not_human_play": True,
        "not_a_new_rules_owner": True,
        "case_count": len(rows),
        "family_count": len(families),
        "expectation_counts": dict(sorted(
            Counter(row["expectation"] for row in rows).items()
        )),
        "observed_outcomes": dict(sorted(tally.items())),
        "per_family": {
            fam: dict(sorted(counts.items()))
            for fam, counts in sorted(families.items())
        },
        "false_unsupported_candidates_not_verified_facts":
            tally["false_unsupported_candidate"],
        "interpretation_warning": (
            "Authored expectations are not independent gold labels. An "
            "unsupported response to a new physical method is a coverage "
            "gap, not evidence the action must succeed; a parsed refusal "
            "is not playable execution. Fixtures are noncanonical."
        ),
        "cases": rows,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print(f"MYRAVANT ACTION COVERAGE: {len(rows)} isolated attempts, "
          f"{len(families)} families, outcomes={dict(sorted(tally.items()))}, "
          f"output={output}")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run_baseline(output=args.output)


if __name__ == "__main__":
    main()
