"""Installed public connected-worksite travel and restart evidence (engineering only)."""
import argparse
from pathlib import Path
import shutil
import tempfile

from _myravant_evidence_runner import (
    assert_repeat_digest_equality, resolve_repository_sha, run_installed_session,
    trace_rows, write_json_report,
)
from astra_runtime.myravant_generated_locality import LocalityRecipe, create_generated_locality_fixture
from astra_runtime.myravant_investigation_application import InvestigationApplication


def journey(root, level, sha):
    root.mkdir()
    checkpoint = root / "campaign.json"
    launcher = shutil.which("myravant-play")
    assert launcher, "the public installed launcher must be available"
    flags = ["--locality", "generated-worksite", "--generated-case", "evidence",
             "--generated-seed", "0", "--generated-scale", str(level)]
    commands = ["look", "go east", "inspect wing 1 panel", "go west"]
    if level >= 2:
        commands.extend(["go west", "go south", "inspect wing 2 panel", "go north"])
    if level == 3:
        commands.extend(["go west", "go west", "inspect wing 3 panel",
                         "go east", "go east", "go east"])
    commands.extend(["recall panel a residue", "wait"])
    rows = []
    for repeat in (0, 1):
        trace = root / (str(repeat) + ".jsonl")
        process = run_installed_session(
            launcher, flags, checkpoint, trace, sha,
            commands if repeat == 0 else ("wait",), load=repeat == 1, timeout=120,
        )
        assert process.returncode == 0, (level, repeat, process.stdout[-2000:], process.stderr)
        assert checkpoint.is_file()
        events = trace_rows(trace)
        assert events and events[-1]["evidence_complete"] is True
        fixture = create_generated_locality_fixture(LocalityRecipe("evidence", 0, scale_level=level))
        app = InvestigationApplication.restore(fixture=fixture, checkpoint_path=checkpoint)
        assert len(app.fixture.place_presentations) == 4 + level
        assert len(app.intervals) == app.runtime_state.logical_time_state.logical_position
        rows.append({"repeat": repeat, "trace": str(trace),
                     "digest": app.authoritative_digest(),
                     "world_intervals": len(app.intervals),
                     "checkpoint_bytes": checkpoint.stat().st_size,
                     "output": process.stdout[-2500:]})
        if repeat == 0:
            assert "wing 1 panel" in process.stdout.casefold()
            if level >= 2:
                assert "wing 2 panel" in process.stdout.casefold()
            if level == 3:
                assert "wing 3 panel" in process.stdout.casefold()
        else:
            assert rows[-1]["digest"] != rows[0]["digest"]
    return {"scale": level, "first": rows[0], "resumed": rows[1]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-sha")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    sha = resolve_repository_sha(args.repository_sha)
    with tempfile.TemporaryDirectory(prefix="myravant-connected-scale-") as directory:
        result = [journey(Path(directory) / f"scale-{level}-{repeat}", level, sha)
                  for level in (1, 2, 3) for repeat in (0, 1)]
    for level in (1, 2, 3):
        pair = [item for item in result if item["scale"] == level]
        assert len(pair) == 2
        assert pair[0]["first"]["digest"] == pair[1]["first"]["digest"]
        assert pair[0]["resumed"]["digest"] == pair[1]["resumed"]["digest"]
    write_json_report(args.output, {
        "schema": "myravant.connected-scale-installed.v1",
        "source": sha, "engineering_authored": True, "human_acceptance": False,
        "results": result,
    })
    print("Connected scale: six installed travel campaigns plus six resumed sessions passed.")


if __name__ == "__main__":
    main()
