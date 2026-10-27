"""Active-workload cost and owner-output probe for bounded scale profiles 1–3.

One worksite access profile per trial, one finite brush, real worker changes
at each additional annex, journal restore. Instrumentation is not authority.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import os
import platform
import statistics
import subprocess
import tempfile
import time
import tracemalloc

from astra_runtime.myravant_generated_locality import LocalityRecipe, build_generated_locality
from astra_runtime.myravant_investigation_application import InvestigationApplication


def measure(op):
    started = time.perf_counter_ns()
    result = op()
    return result, (time.perf_counter_ns() - started) / 1e6


def run(level, repeat):
    with tempfile.TemporaryDirectory(prefix="myravant-final-scale-") as directory:
        path = Path(directory) / "checkpoint.json"
        tracemalloc.start()
        try:
            (app, history), setup_ms = measure(
                lambda: build_generated_locality(LocalityRecipe("access", 0, scale_level=level)))
            intervals_ms, steps_ms = [], []
            def do(method, *args):
                before = app.runtime_state.logical_time_state.logical_position
                result, elapsed = measure(lambda: getattr(app, method)(*args))
                assert result.authoritative_changed and not result.failure_class, (method, args, result.message)
                steps_ms.append(elapsed)
                if app.runtime_state.logical_time_state.logical_position != before:
                    assert app.runtime_state.logical_time_state.logical_position == before + 1
                    intervals_ms.append(elapsed)
            blocked, block_ms = measure(lambda: app.move("north"))
            assert blocked.failure_class == "material_passage_obstructed" and not blocked.authoritative_changed
            # The owner-approved alternate path exists while the direct passage
            # remains blocked. Undoing the material connection opens the short route.
            for direction in ("west", "north", "south"):
                do("move", direction)
            do("material", "untie", "Cord")
            for direction in ("north", "south"):
                do("move", direction)
            do("request_cleaning", "Jun", "Panel A", "Brush", "scrub")
            do("pickup", "Brush")
            for n in range(1, level + 1):
                route = ("east",) if n == 1 else (
                    ("west", "west", "south") if n == 2 else ("north", "west", "west"))
                for direction in route:
                    do("move", direction)
                do("drop", "Brush")
                do("request_cleaning", f"Wing {n} Worker", f"Wing {n} Panel", "Brush", "scrub")
                do("wait")
                do("wait")
                if n < level:
                    do("participation_control", f"Wing {n} Worker", "pause")
                    do("request_object_from_actor", f"Wing {n} Worker", "Brush")
            # Leave all actors with actual attributed work: original workshop
            # contender has stopped at its bounded refusal, each new actor
            # produced material cleaning rather than inert fixture population.
            for _ in range(3):
                do("wait")
            before = app.authoritative_digest()
            recalled, query_ms = measure(lambda: app.recall_history(f"Wing {level} Panel", "residue"))
            assert not recalled.authoritative_changed
            assert before == app.authoritative_digest()
            app.checkpoint_path = path
            saved, save_ms = measure(app.save)
            assert not saved.failure_class
            restored, replay_ms = measure(
                lambda: InvestigationApplication.restore(fixture=app.fixture, checkpoint_path=path))
            assert restored.authoritative_digest() == app.authoritative_digest()
            assert restored.journal == app.journal
            assert restored.evidence_state == app.evidence_state
            assert restored.actor_events == app.actor_events
            assert restored.participation_state == app.participation_state
            assert restored.water_state == app.water_state
            assert len(app.intervals) == app.runtime_state.logical_time_state.logical_position
            evidence = app.actor_events
            contributors = {row[2] for row in evidence if row[1] == "physical_contribution"}
            due = [row for row in evidence if row[1] == "due_resolution"]
            blocked_due = [row for row in due if row[3][2] == "blocked"]
            worker_ids = {app.fixture.resolve_actor_reference(f"Wing {n} Worker") for n in range(1, level + 1)}
            assert worker_ids <= contributors
            assert len(blocked_due) >= 1
            assert all(dict(app.water_state.adhered)[app.fixture.resolve_object_reference(
                f"Wing {n} Panel")] < 3 for n in range(1, level + 1))
            _, peak = tracemalloc.get_traced_memory()
            return {
                "level": level, "repeat": repeat, "case": "access", "seed": 0,
                "campaign": app.fixture.campaign_id,
                "authoritative_final": app.authoritative_digest(),
                "places": len(app.fixture.place_presentations),
                "connections": len(app.fixture.movement_routes),
                "objects": len(app.fixture.object_presentations),
                "actors": len(app.fixture.actor_profiles),
                "actor_ids_with_contribution": len(contributors),
                "annex_workers_contributed": len(worker_ids & contributors),
                "due_resolutions": len(due),
                "blocked_due_resolutions": len(blocked_due),
                "actor_events": len(app.actor_events),
                "admitted_evidence": len(app.evidence_state.events),
                "intervals": len(app.intervals),
                "journal_entries": len(app.journal),
                "checkpoint_bytes": path.stat().st_size,
                "times_ms": {
                    "initial_construction": setup_ms, "blocked_access_probe": block_ms,
                    "interval_samples": intervals_ms, "action_samples": steps_ms,
                    "history_recall": query_ms, "checkpoint_save": save_ms,
                    "checkpoint_restore_full_replay": replay_ms,
                },
                "tracemalloc_peak_bytes": peak,
            }
        finally:
            tracemalloc.stop()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runtime-sha", required=True)
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    root = args.source_root.resolve()
    import astra_runtime.myravant_generated_locality as generated
    if not Path(generated.__file__).resolve().is_relative_to(root):
        raise RuntimeError("running library is not loaded from exact candidate source")
    sha = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if sha != args.runtime_sha:
        raise RuntimeError("exact-source SHA mismatch")
    rows = [run(level, repeat) for level in (1, 2, 3) for repeat in (0, 1)]
    for level in (1, 2, 3):
        x = [row for row in rows if row["level"] == level]
        assert len(x) == 2
        for field in ("campaign", "authoritative_final", "intervals", "journal_entries",
                      "admitted_evidence", "due_resolutions", "blocked_due_resolutions",
                      "annex_workers_contributed", "checkpoint_bytes"):
            assert x[0][field] == x[1][field], (level, field)
    summaries = {}
    for level in (1, 2, 3):
        xs = [row for row in rows if row["level"] == level]
        metrics = ("checkpoint_restore_full_replay", "checkpoint_save", "initial_construction")
        summaries[str(level)] = {
            "active_annexes": level,
            "due_resolutions": xs[0]["due_resolutions"],
            "interval_count": xs[0]["intervals"],
            "checkpoint_bytes": xs[0]["checkpoint_bytes"],
            "measurements_ms": {
                label: {"min": min(row["times_ms"][label] for row in xs),
                        "median": statistics.median(row["times_ms"][label] for row in xs),
                        "max": max(row["times_ms"][label] for row in xs)}
                for label in metrics},
            "interval_ms": {"min": min(t for row in xs for t in row["times_ms"]["interval_samples"]),
                            "median": statistics.median(t for row in xs for t in row["times_ms"]["interval_samples"]),
                            "max": max(t for row in xs for t in row["times_ms"]["interval_samples"])},
        }
    payload = {
        "schema": "myravant.scale-final-active-cost.v1",
        "source_sha": sha, "engineering_authored": True, "human_acceptance": False,
        "environment": {"python": platform.python_version(),
                        "platform": platform.platform(), "processors": os.cpu_count()},
        "limits": ("Two repeated trials for each of 3 bounded profiles on one runner; "
                   "tracemalloc active, first-run effects not separated; no "
                   "adopted runtime budget confirmed; not a speedup or "
                   "large-world performance guarantee."),
        "summaries": summaries, "trials": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("Final scale: 6 active-owner trials passed deterministic same-level replay.")


if __name__ == "__main__":
    main()
