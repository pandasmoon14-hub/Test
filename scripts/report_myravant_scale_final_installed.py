"""Two repeated public three-session access-and-work campaigns (Package 08).

The generated *access* profile has a real existing assembly obstruction.
Every public operation goes through myravant-play, with checkpoint replay at
each session boundary. No owner state injection or new profile semantics.
"""
import argparse
from pathlib import Path
import shutil
import tempfile

from _myravant_evidence_runner import resolve_repository_sha, run_installed_session, trace_rows, write_json_report
from astra_runtime.domain.persistent_world_material import active_effects, placement
from astra_runtime.myravant_generated_locality import LocalityRecipe, create_generated_locality_fixture
from astra_runtime.myravant_investigation_application import InvestigationApplication


FLAGS = ("--locality", "generated-worksite", "--generated-case", "access",
         "--generated-seed", "0", "--generated-scale", "3")
PHASES = (
    (
        "go north",  # deliberately blocked by an assembled material barrier
        "ask Jun to clean Panel A using Brush by scrubbing",
        "take Brush",
        "go west", "go north", "go south",
        "untie Cord",  # existing physical owner removes the actual obstruction
        "go north", "go south",
        "go east", "drop Brush",
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
        "inspect Panel A", *("wait",) * 9,
    ),
)


def check(app, phase):
    assert len(app.fixture.place_presentations) == 7
    assert len(app.fixture.actor_profiles) == 5
    assert app.runtime_state.logical_time_state.logical_position == len(app.intervals)
    assert len({row[0] for row in app.intervals}) == len(app.intervals)
    assert len({e[0] for e in app.actor_events}) == len(app.actor_events)
    assert not any(e.kind == "movement" and e.direction == "north"
                   for e in active_effects(app.state.representation, app.connections,
                                           app.fixture.material_profile))
    brush = app.fixture.resolve_object_reference("Brush")
    expected = app.fixture.player_entity_id if phase < 2 else app.fixture.resolve_actor_reference("Wing 3 Worker")
    assert placement(app.state.representation, brush).object_entity_id == expected
    panel_a = app.fixture.resolve_object_reference("Panel A")
    for n in range(1, phase + 2):
        actor = app.fixture.resolve_actor_reference(f"Wing {n} Worker")
        panel = app.fixture.resolve_object_reference(f"Wing {n} Panel")
        done = [e for e in app.actor_events if e[1] == "physical_contribution" and e[2] == actor]
        assert len(done) >= 2
        assert dict(app.water_state.adhered)[panel] < 3
        assert not any(e.actor_id == actor and e.target_id == panel_a
                       for e in app.evidence_state.events)
    assert any(e[1] == "due_resolution" and e[2] == app.fixture.resolve_actor_reference("Jun")
               and e[3][2] == "blocked" for e in app.actor_events)


def campaign(folder, sha):
    folder.mkdir()
    launcher = shutil.which("myravant-play")
    assert launcher, "installed public launcher unavailable"
    path = folder / "world.json"
    fixture = create_generated_locality_fixture(LocalityRecipe("access", 0, scale_level=3))
    result = []
    for phase, commands in enumerate(PHASES):
        trace = folder / f"phase-{phase}.jsonl"
        p = run_installed_session(launcher, FLAGS, path, trace, sha,
                                  commands, load=phase > 0, timeout=180)
        assert p.returncode == 0, (phase, p.stdout[-2300:], p.stderr[-1200:])
        if phase == 0:
            assert "assembled barrier obstructs" in p.stdout.casefold()
            assert "wing 1 panel" in p.stdout.casefold()
        events = trace_rows(trace)
        assert events and events[-1]["evidence_complete"] is True
        a = InvestigationApplication.restore(fixture=fixture, checkpoint_path=path)
        check(a, phase)
        result.append({
            "phase": phase, "digest": a.authoritative_digest(),
            "world_intervals": len(a.intervals), "journal_entries": len(a.journal),
            "due_resolutions": sum(e[1] == "due_resolution" for e in a.actor_events),
            "admitted_evidence_events": len(a.evidence_state.events),
            "checkpoint_bytes": path.stat().st_size, "trace": str(trace),
        })
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repository-sha")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    sha = resolve_repository_sha(args.repository_sha)
    with tempfile.TemporaryDirectory(prefix="myravant-final-access-installed-") as tmp:
        runs = [campaign(Path(tmp) / f"campaign-{n}", sha) for n in (0, 1)]
    for a, b in zip(*runs):
        for field in ("digest", "world_intervals", "journal_entries",
                      "due_resolutions", "admitted_evidence_events", "checkpoint_bytes"):
            assert a[field] == b[field], (a["phase"], field)
    write_json_report(args.output, {
        "schema": "myravant.scale-final-access-installed.v1",
        "source": sha, "engineering_authored": True,
        "independent_assessor": False, "human_play": False,
        "limits": "One noncanonical access profile; two deterministic three-session runs.",
        "runs": runs,
    })
    print("Final access and work: 2 x 3 installed sessions with obstruction, "
          "material reopening, all workers, evidence and replay passed.")


if __name__ == "__main__":
    main()
