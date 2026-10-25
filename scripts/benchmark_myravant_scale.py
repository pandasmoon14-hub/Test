"""Source-pinned, nonauthoritative pilot for measured Myravant local scale.

This is a *pilot*, not the three-level workload or a scale certification.
It probes real generated-worksite owners and their deterministic save/restore.
The module deliberately does not mutate source, choose optimization or create law.
"""
import argparse
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc

from astra_runtime import myravant_generated_locality as generated
from astra_runtime.domain.persistent_world_material import active_effects, placement
from astra_runtime.myravant_investigation_application import InvestigationApplication


CASES = ("access", "resources", "evidence")


def snapshot(app):
    """Exact owner projections, not only the top-level digest.

    Reprs contain the existing immutable/dataclass values and journal receipts.
    This pilot uses them only as evidence; repr has no authority in the runtime.
    """
    return {
        "authoritative_digest": app.authoritative_digest(),
        "logical_time": app.runtime_state.logical_time_state.logical_position,
        "representation": repr(app.state.representation),
        "connections": repr(app.connections),
        "water": repr(app.water_state),
        "environment": repr(app.environment_state),
        "work": repr(app.work_state),
        "participation": repr(app.participation_state),
        "evidence_by_actor": repr(app.evidence_state),
        "actor_events": repr(app.actor_events),
        "disclosed_relays": repr(app.disclosed_relays),
        "intervals": repr(app.intervals),
        "journal": repr(app.journal),
    }


def goals(app, case):
    if case == "access":
        return {
            "real_blocked_north_passage": any(
                e.kind == "movement" and e.direction == "north"
                for e in active_effects(
                    app.state.representation, app.connections, app.fixture.material_profile
                )
            )
        }
    if case == "resources":
        brush = next(
            p.entity_id for p in app.fixture.object_presentations if p.name == "Brush"
        )
        return {
            "finite_brush_with_declared_first_actor": (
                placement(app.state.representation, brush).object_entity_id
                == app.fixture.actor_order[0]
            ),
            "two_distinct_contending_actors": len(set(app.fixture.actor_order[:2])) == 2,
        }
    return {
        "lawfully_delivered_prior_account": bool(app.disclosed_relays),
        "actual_evidence_retained": bool(app.evidence_state.events),
    }


def duration_ms(fn):
    t = time.perf_counter_ns()
    result = fn()
    return result, (time.perf_counter_ns() - t) / 1_000_000


def run_one(case, seed, intervals, repeat, scale_level=0):
    with tempfile.TemporaryDirectory(prefix="myravant-scale-pilot-") as directory:
        checkpoint = Path(directory) / "world.json"
        tracemalloc.start()
        try:
            (app, history), initialize_ms = duration_ms(
                lambda: generated.build_generated_locality(
                    (generated.LocalityRecipe(case, seed) if scale_level == 0 else
                     generated.LocalityRecipe(case, seed, scale_level=scale_level))
                )
            )
            initial = snapshot(app)
            initial_objectives = goals(app, case)
            assert all(initial_objectives.values()), (case, initial_objectives)
            interval_ms = []
            for _ in range(intervals):
                result, ms = duration_ms(app.wait)
                assert result.authoritative_changed and not result.failure_class
                interval_ms.append(ms)
            before_query = app.authoritative_digest()
            recalled, recall_ms = duration_ms(
                lambda: app.recall_history("panel a", "residue")
            )
            compared, compare_ms = duration_ms(
                lambda: app.compare_history("panel a", "residue")
            )
            assert not recalled.authoritative_changed
            assert not compared.authoritative_changed
            assert before_query == app.authoritative_digest()
            app.checkpoint_path = checkpoint
            saved, save_ms = duration_ms(app.save)
            assert not saved.failure_class and checkpoint.is_file()
            expected = snapshot(app)
            restored, restore_ms = duration_ms(
                lambda: InvestigationApplication.restore(
                    fixture=app.fixture, checkpoint_path=checkpoint
                )
            )
            actual = snapshot(restored)
            assert actual == expected, {
                key: "restore difference" for key in expected if expected[key] != actual[key]
            }
            assert len(app.intervals) == app.runtime_state.logical_time_state.logical_position
            objectives = dict(initial_objectives)
            objectives["one_world_clock"] = (
                len(app.intervals) == app.runtime_state.logical_time_state.logical_position
            )
            assert all(objectives.values()), (case, objectives)
            _, peak_bytes = tracemalloc.get_traced_memory()
            return {
                "case": case, "seed": seed, "repeat": repeat,
                "intervals_added": intervals, "initial": initial, "final": expected,
                "objectives": objectives,
                "counts": {
                    "places": len(app.fixture.place_presentations),
                    "connections": len(app.fixture.movement_routes),
                    "presented_objects": len(app.fixture.object_presentations),
                    "active_actor_profiles": len(app.fixture.actor_profiles),
                    "admitted_events": len(app.evidence_state.events),
                    "actor_events": len(app.actor_events),
                    "actor_tasks": len(app.participation_state.records),
                    "committed_intervals": len(app.intervals),
                    "journal_entries": len(app.journal),
                    "prehistory_receipts": len(history),
                },
                "metrics_ms": {
                    "construction_and_prehistory": initialize_ms,
                    "interval_samples": interval_ms,
                    "history_recall": recall_ms,
                    "history_comparison": compare_ms,
                    "checkpoint_save": save_ms,
                    "checkpoint_restore_and_replay": restore_ms,
                },
                "checkpoint_bytes": checkpoint.stat().st_size,
                "tracemalloc_peak_bytes": peak_bytes,
                "measurement_overhead": "tracemalloc active; timing includes instrumentation",
            }
        finally:
            tracemalloc.stop()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--runtime-sha", required=True)
    p.add_argument("--intervals", type=int, default=3)
    p.add_argument("--repeats", type=int, default=2)
    p.add_argument("--scale-level", type=int, choices=(0, 1, 2, 3), default=0)
    args = p.parse_args()
    if not 1 <= args.intervals <= 32 or not 1 <= args.repeats <= 5:
        p.error("pilot accepts 1..32 intervals and 1..5 repeats")
    root = args.source_root.resolve()
    module = Path(generated.__file__).resolve()
    if not module.is_relative_to(root):
        raise RuntimeError(f"imported runtime {module} is not from requested checkout {root}")
    sha = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True, timeout=15
    ).strip()
    if sha != args.runtime_sha:
        raise RuntimeError(f"runtime commit mismatch: {sha} != {args.runtime_sha}")
    rows = [
        run_one(case, seed, args.intervals, repeat, args.scale_level)
        for case in CASES for seed in (0, 1) for repeat in range(args.repeats)
    ]
    # The current two parity seeds change admitted input; each identical
    # recipe+case must reproduce exact authoritative history across repeats.
    for case in CASES:
        for seed in (0, 1):
            matches = [x for x in rows if x["case"] == case and x["seed"] == seed]
            assert all(x["initial"] == matches[0]["initial"] for x in matches)
            assert all(x["final"] == matches[0]["final"] for x in matches)
            assert all(x["objectives"] == matches[0]["objectives"] for x in matches)
    durations = [sum(x["metrics_ms"]["interval_samples"]) for x in rows]
    result = {
        "schema": "myravant.causal-scale-pilot.v1",
        "scope": ("legacy worksite pilot" if args.scale_level == 0 else
                  "one connected noncanonical campaign with annex scale; benchmark not acceptance"),
        "engineering_authored": True, "human_acceptance": False,
        "runtime_sha": sha, "runtime_module_path": str(module.relative_to(root)),
        "environment": {
            "platform": platform.platform(), "python": sys.version.split()[0],
            "processors": os.cpu_count(),
        },
        "workload": {"cases": list(CASES), "seeds": [0, 1],
                     "repeats": args.repeats, "intervals_per_trial": args.intervals,
                     "connected_scale_level": args.scale_level},
        "interval_total_ms_distribution": {
            "min": min(durations), "median": statistics.median(durations),
            "max": max(durations),
        },
        "trials": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(f"Scale baseline pilot: {len(rows)} exact-source trials; "
          f"median total interval time {statistics.median(durations):.3f} ms")
    print(f"Recorded source {sha}; this is not scale certification.")


if __name__ == "__main__":
    main()
