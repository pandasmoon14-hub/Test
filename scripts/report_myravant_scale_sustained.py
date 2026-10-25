"""Repeatable installed sustained-locality journeys over existing runtime owners.

No direct state injection or fixture remapping. Each public-client input creates
its own qualified receipt, and every session restarts from the same checkpoint.
"""
import argparse
from pathlib import Path
import shutil
import tempfile

from _myravant_evidence_runner import (
    resolve_repository_sha, run_installed_session, trace_rows, write_json_report,
)
from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_generated_locality import (
    LocalityRecipe, create_generated_locality_fixture,
)
from astra_runtime.myravant_investigation_application import InvestigationApplication


FLAGS = ("--locality", "generated-worksite", "--generated-case", "evidence",
         "--generated-seed", "0", "--generated-scale", "3")

PHASES = (
    (
        "ask Jun to clean Panel A using Brush by scrubbing",
        "take Brush",
        "go east",
        "drop Brush",
        "tell Wing 1 Worker that Wing 1 Panel residue is clear",
        "ask Wing 1 Worker about Wing 1 Panel residue",
        "ask Wing 1 Worker to clean Wing 1 Panel using Brush by scrubbing",
        "wait", "wait",
        "ask Wing 1 Worker about Wing 1 Panel residue",
        "compare reports about Wing 1 Panel residue",
        "ask Wing 1 Worker to pause work",
        "ask Wing 1 Worker for Brush",
    ),
    (
        "go west", "go west", "go south",
        "drop Brush",
        "ask Wing 2 Worker to clean Wing 2 Panel using Brush by scrubbing",
        "wait", "wait",
        "ask Wing 2 Worker to pause work",
        "ask Wing 2 Worker for Brush",
    ),
    (
        "go north", "go west", "go west",
        "drop Brush",
        "ask Wing 3 Worker to clean Wing 3 Panel using Brush by scrubbing",
        "wait", "wait",
        "go east", "go east", "go north", "go south",
        "inspect Panel A",
        *("wait",) * 9,
    ),
)


def selected_panel(app, number):
    return app.fixture.resolve_object_reference(f"Wing {number} Panel")


def validate(app, phase):
    assert len(app.fixture.place_presentations) == 7
    assert len(app.fixture.actor_profiles) == 5
    assert app.runtime_state.logical_time_state.logical_position == len(app.intervals)
    ids = {e[0] for e in app.actor_events}
    assert len(ids) == len(app.actor_events), "duplicate owner receipt"
    brush = app.fixture.resolve_object_reference("Brush")
    carrier = placement(app.state.representation, brush)
    if phase < 2:
        assert carrier.object_entity_id == app.fixture.player_entity_id
    else:
        assert carrier.object_entity_id == app.fixture.resolve_actor_reference("Wing 3 Worker")
    for n in range(1, phase + 2):
        actor = app.fixture.resolve_actor_reference(f"Wing {n} Worker")
        contributions = [e for e in app.actor_events if e[1] == "physical_contribution" and e[2] == actor]
        assert len(contributions) >= 2, (phase, n, contributions)
        assert dict(app.water_state.adhered)[selected_panel(app, n)] < 3
        assert not any(e.actor_id == actor and e.target_id ==
                       app.fixture.resolve_object_reference("Panel A")
                       for e in app.evidence_state.events)
    if phase == 2:
        assert app.current_place_id() == next(p.entity_id for p in app.fixture.place_presentations
                                              if p.name == "Workshop")
        assert any(e[1] == "due_resolution" and e[3][2] == "blocked"
                   and e[2] == app.fixture.resolve_actor_reference("Jun")
                   for e in app.actor_events)


def journey(root, source):
    root.mkdir(parents=True)
    launcher = shutil.which("myravant-play")
    assert launcher, "installed public game launcher is required"
    checkpoint = root / "campaign.json"
    fixture = create_generated_locality_fixture(LocalityRecipe("evidence", 0, scale_level=3))
    stages = []
    for phase, commands in enumerate(PHASES):
        trace = root / f"phase-{phase}.jsonl"
        result = run_installed_session(launcher, FLAGS, checkpoint, trace,
                                       source, commands, load=phase > 0, timeout=180)
        assert result.returncode == 0, (phase, result.stdout[-2500:], result.stderr)
        rows = trace_rows(trace)
        assert rows and rows[-1]["evidence_complete"] is True
        app = InvestigationApplication.restore(fixture=fixture, checkpoint_path=checkpoint)
        validate(app, phase)
        stages.append({
            "phase": phase,
            "commands": commands,
            "world_intervals": len(app.intervals),
            "journal_entries": len(app.journal),
            "evidence_events": len(app.evidence_state.events),
            "digest": app.authoritative_digest(),
            "checkpoint_bytes": checkpoint.stat().st_size,
            "trace": str(trace),
        })
    return stages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-sha")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = resolve_repository_sha(args.repository_sha)
    with tempfile.TemporaryDirectory(prefix="myravant-sustained-scale-") as directory:
        runs = [journey(Path(directory) / f"campaign-{i}", source) for i in range(2)]
    for left, right in zip(*runs):
        assert left["digest"] == right["digest"]
        assert left["world_intervals"] == right["world_intervals"]
        assert left["journal_entries"] == right["journal_entries"]
    write_json_report(args.output, {
        "schema": "myravant.scale-sustained-installed.v1",
        "source": source,
        "engineering_authored": True,
        "independent_assessor": False,
        "human_play_acceptance": False,
        "runs": runs,
    })
    print("Sustained scale: two three-session installed campaigns, "
          "three participating annex workers, replay and evidence verified.")


if __name__ == "__main__":
    main()
