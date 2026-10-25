"""Cumulative/exclusive cost inventory for an exact source and connected profile.

No runtime semantic change or optimization is performed by this profiler.
"""
import argparse
import cProfile
from io import StringIO
from pathlib import Path
import platform
import pstats
import subprocess

from astra_runtime import myravant_generated_locality as generated
from astra_runtime.myravant_investigation_application import InvestigationApplication


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--runtime-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.source_root.resolve()
    if not Path(generated.__file__).resolve().is_relative_to(root):
        raise RuntimeError("profiled runtime is not imported from requested source")
    actual_sha = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual_sha != args.runtime_sha:
        raise RuntimeError("profile source SHA mismatch")

    import tempfile
    profiler = cProfile.Profile()
    with tempfile.TemporaryDirectory(prefix="myravant-scale-profiler-") as directory:
        profiler.enable()
        app, _ = generated.build_generated_locality(
            generated.LocalityRecipe("evidence", seed=0, scale_level=3)
        )
        for _ in range(2):
            result = app.wait()
            assert result.authoritative_changed and not result.failure_class
        before = app.authoritative_digest()
        recalled = app.recall_history("Panel A", "residue")
        assert not recalled.authoritative_changed
        assert app.authoritative_digest() == before
        app.checkpoint_path = Path(directory) / "profile.json"
        saved = app.save()
        assert not saved.failure_class
        replayed = InvestigationApplication.restore(
            fixture=app.fixture, checkpoint_path=app.checkpoint_path
        )
        assert replayed.authoritative_digest() == app.authoritative_digest()
        profiler.disable()
    stream = StringIO()
    print("Package 08 exact-source cProfile evidence", file=stream)
    print("sha=" + actual_sha, file=stream)
    print("python=" + platform.python_version() + " platform=" + platform.platform(), file=stream)
    print("workload=evidence seed=0 scale=3, generated history, 2 waits, recall, save/restore", file=stream)
    print("This is an instrumented sample, not an optimization claim.", file=stream)
    pstats.Stats(profiler, stream=stream).sort_stats("cumulative").print_stats(45)
    print("\nSorted by exclusive self time:", file=stream)
    pstats.Stats(profiler, stream=stream).sort_stats("tottime").print_stats(25)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(stream.getvalue())
    print("Retained exact-source connected-level-3 cumulative/exclusive profile.")


if __name__ == "__main__":
    main()
