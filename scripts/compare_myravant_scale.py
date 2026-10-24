"""Compare exact authoritative baseline/candidate pilot results.

Wall timings are reported, never part of equality. Source identities and
hardware are recorded separately; successful comparison is NOT a speedup claim.
"""
import argparse
import json
from pathlib import Path
import statistics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = json.loads(args.baseline.read_text())
    cand = json.loads(args.candidate.read_text())
    assert base["schema"] == cand["schema"] == "myravant.causal-scale-pilot.v1"
    assert base["workload"] == cand["workload"]
    assert len(base["trials"]) == len(cand["trials"])
    differences = []
    for a, b in zip(base["trials"], cand["trials"]):
        key = (a["case"], a["seed"], a["repeat"])
        assert key == (b["case"], b["seed"], b["repeat"])
        for field in ("initial", "final", "counts", "objectives"):
            if a[field] != b[field]:
                differences.append({"trial": key, "field": field})
    def samples(data, field):
        return [t["metrics_ms"][field] for t in data["trials"]]
    timings = {}
    for name in ("construction_and_prehistory", "history_recall",
                 "history_comparison", "checkpoint_save",
                 "checkpoint_restore_and_replay"):
        before, after = samples(base, name), samples(cand, name)
        timings[name] = {"baseline_ms_median": statistics.median(before),
                         "candidate_ms_median": statistics.median(after),
                         "baseline_ms_range": [min(before), max(before)],
                         "candidate_ms_range": [min(after), max(after)]}
    result = {
        "schema": "myravant.causal-scale-comparison.v1",
        "baseline_runtime_sha": base["runtime_sha"],
        "candidate_runtime_sha": cand["runtime_sha"],
        "trial_count": len(base["trials"]), "authoritative_equal": not differences,
        "differences": differences, "timings": timings,
        "limits": [
            "Pilot tests existing fixed three-scenario local worksite only",
            "No growth in independent connected sites or active actor population",
            "Instrumentation overhead included in wall timings",
            "No production benchmark, three-level workload, optimization or human acceptance",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    if differences:
        raise AssertionError(f"authoritative mismatch: {differences[:4]}")
    print(f"Pilot semantic equivalence: {len(base['trials'])} trials identical")
    print("Wall timings recorded but no speedup is inferred.")


if __name__ == "__main__":
    main()
