"""Generate trace-grounded evidence for Myravant's adaptive synthetic players.

Executes actual installed-terminal interactions in isolated campaigns. This
report is *not* a human usability rating, AI-generated authority, or canon.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import runpy
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    probes = runpy.run_path(
        str(Path(__file__).resolve().parents[1] /
            "tests" / "test_myravant_terminal_feedback_synthetic_players.py")
    )
    policies = probes["PLAYER_POLICIES"]
    make_seed = probes["_scripted_seed"]
    play = probes["_play_live"]
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True,
        check=True, timeout=15,
    ).stdout.strip()
    routes, failures, result_types = Counter(), Counter(), Counter()
    attempts, changed, refused = 0, 0, 0
    detailed = []
    with tempfile.TemporaryDirectory(prefix="myravant-actual-play-") as d:
        root = Path(d)
        for persona in sorted(policies):
            for seeded in (False, True):
                stem = f"{persona}-{'gatehouse' if seeded else 'workshop'}"
                checkpoint = root / f"{stem}.json"
                trace = root / f"{stem}.jsonl"
                if seeded:
                    make_seed(checkpoint)
                result = play(persona, checkpoint, trace, seeded=seeded)
                records = [
                    json.loads(row)
                    for row in trace.read_text(encoding="utf-8").splitlines()
                ]
                interactions = [
                    row for row in records if row["record_type"] == "interaction"
                ]
                turns = interactions[:-1]
                assert len(turns) == 18
                for record in turns:
                    attempts += 1
                    routes[record["parsed_action"]] += 1
                    result_types[record["result_type"]] += 1
                    if record["failure_class"]:
                        failures[record["failure_class"]] += 1
                        refused += 1
                    if record["authoritative_changed"]:
                        changed += 1
                detailed.append({
                    "persona": persona,
                    "behavior_source": result["pressure_source"],
                    "initial_context": "gatehouse" if seeded else "workshop",
                    "adaptations": result["responsive"],
                    "checkpoint_sha256": sha256(result["checkpoint"]).hexdigest(),
                    "turns": [{
                        "player_input": record["raw_player_input"].rstrip("\n"),
                        "terminal_response": record["player_visible_output"],
                        "route": record["parsed_action"],
                        "result": record["result_type"],
                        "failure": record["failure_class"],
                        "changed": record["authoritative_changed"],
                        "pre_digest": record["pre_state_digest"],
                        "post_digest": record["post_state_digest"],
                        "world_event_class": record.get("world_event_class"),
                        "world_process_action": record.get("world_process_action"),
                        "world_process_outcome": record.get("world_process_outcome"),
                    } for record in turns],
                })
    summary = {
        "schema": "myravant.synthetic_play_discovery_2.evidence.v1",
        "repository_sha": head,
        "evidence_type": "deterministic_feedback_conditioned_synthetic_players",
        "not_human_testers": True,
        "not_canon": True,
        "player_policy_count": len(policies),
        "lawful_start_contexts": 2,
        "measured_player_attempts": attempts,
        "authoritative_changes": changed,
        "reported_failure_classes": refused,
        "route_counts": dict(sorted(routes.items())),
        "failure_class_counts": dict(sorted(failures.items())),
        "result_type_counts": dict(sorted(result_types.items())),
        "source_and_method_document":
            "docs/evidence/myravant_synthetic_play_discovery_2.md",
        "sessions": detailed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"MYRAVANT SYNTHETIC PLAY: {len(detailed)} contexts; "
        f"{attempts} player attempts; {changed} committed state changes; "
        f"{refused} reported failure-class results; "
        f"artifact={args.output}"
    )
    print("ROUTES " + json.dumps(summary["route_counts"], sort_keys=True))
    print("FAILURES " + json.dumps(summary["failure_class_counts"], sort_keys=True))


if __name__ == "__main__":
    main()
