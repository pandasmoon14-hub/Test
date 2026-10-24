"""Engineering-authored installed worksite journeys with exact-source replay checks."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.domain.persistent_world_material import active_effects, placement
from astra_runtime.myravant_generated_locality import LocalityRecipe, create_generated_locality_fixture
from astra_runtime.myravant_investigation_application import InvestigationApplication

CASES = ("access", "resources", "evidence")
COMMANDS = {
    "access": ("go north", "untie cord", "go north"),
    "resources": ("go east", "inspect panel a", "wait"),
    "evidence": ("recall panel a residue", "inspect panel a",
                 "compare reports about panel a residue"),
}


def journey(root, case, sha):
    root.mkdir()
    save = root / "campaign.json"
    launcher = shutil.which("myravant-play")
    assert launcher, "installed public launcher required"
    seed = 0
    flags = ["--locality", "generated-worksite", "--generated-case", case,
             "--generated-seed", str(seed)]
    traces = []

    def play(commands, load=False):
        trace = root / (str(len(traces)) + ".jsonl")
        args = [launcher, *flags, "--checkpoint", str(save),
                "--trace", str(trace), "--repository-sha", sha]
        if load:
            args.extend(["--load", str(save)])
        proc = subprocess.run(args, input="\n".join((*commands, "save", "exit", "")),
                              text=True, capture_output=True, timeout=120)
        assert proc.returncode == 0, (case, proc.stdout[-3000:], proc.stderr)
        assert save.is_file()
        rows = tuple(json.loads(line) for line in trace.read_text().splitlines())
        assert rows and rows[-1]["evidence_complete"] is True
        app = InvestigationApplication.restore(
            fixture=create_generated_locality_fixture(LocalityRecipe(case, seed)),
            checkpoint_path=save)
        traces.append({"commands": commands, "output": proc.stdout,
                       "evidence": str(trace), "digest": app.authoritative_digest(),
                       "journal": len(app.journal)})
        return app, proc.stdout

    a, output = play(COMMANDS[case])
    if case == "access":
        assert "assembled barrier obstructs" in output.casefold()
        assert not active_effects(a.state.representation, a.connections,
                                  a.fixture.material_profile)
        assert a.current_place_id() == next(
            p.entity_id for p in a.fixture.place_presentations if p.name == "Covered Yard")
        objectives = {"blocked_direct_route": True, "physical_release": not a.connections,
                      "alternate_route_and_reopen": True}
    elif case == "resources":
        brush = next(p.entity_id for p in a.fixture.object_presentations if p.name == "Brush")
        objectives = {"unique_finite_tool_custody": placement(
            a.state.representation, brush).object_entity_id == a.fixture.actor_order[0],
            "actor_time_advances": a.runtime_state.logical_time_state.logical_position >= 2,
            "two_actor_profiles": len(a.fixture.actor_profiles) == 2}
    else:
        panel = next(p.entity_id for p in a.fixture.object_presentations if p.name == "Panel A")
        objectives = {"disclosed_report": bool(a.disclosed_relays),
                      "contrary_material_truth": dict(a.water_state.adhered)[panel] == 3,
                      "admitted_provenance": "received statement" in output.lower(),
                      "no_guilt_solution": "no account is selected as true" in output.lower()}
    assert all(objectives.values()), (case, objectives)
    original = a.authoritative_digest()
    b, _ = play(("wait",), load=True)
    assert b.authoritative_digest() != original
    assert len(b.journal) > len(a.journal)
    restored = InvestigationApplication.restore(fixture=b.fixture, checkpoint_path=save)
    assert restored.authoritative_digest() == b.authoritative_digest()
    return {"case": case, "objectives": objectives, "digest": b.authoritative_digest(),
            "traces": traces}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repository-sha")
    args = parser.parse_args()
    sha = args.repository_sha or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, timeout=15).strip()
    assert len(sha) == 40
    with tempfile.TemporaryDirectory(prefix="myravant-generated-worksite-") as directory:
        runs = [journey(Path(directory) / (case + "-" + str(repeat)), case, sha)
                for case in CASES for repeat in range(2)]
        for case in CASES:
            two = [r for r in runs if r["case"] == case]
            assert len(two) == 2 and two[0]["digest"] == two[1]["digest"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "schema": "myravant.generated-worksite-installed.v1", "source": sha,
        "engineering_authored": True, "blind_assessment": False,
        "runs": runs}, indent=2, sort_keys=True) + "\n")
    print("Generated worksite: six installed two-session journeys passed.")


if __name__ == "__main__":
    main()
