"""Installed, engineering-authored #559 journeys: no human/blind acceptance claim."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication
from astra_runtime.domain.persistent_world_actor_participation import selected

SCENARIOS = ("recovery", "packed-contact", "actor-scarcity")


def stock(app, name):
    return dict(app.water_state.water)[identity(name)]


def accounting(app):
    water = sum(v for _, v in app.water_state.water) + sum(
        v for _, v in app.environment_state.evaporated)
    residue = (sum(v for _, v in app.water_state.adhered)
               + sum(v for _, v in app.water_state.suspended)
               + sum(v for _, v in app.environment_state.deposits))
    return water, str(residue)


def journey(folder, name, sha):
    launcher = shutil.which("myravant-play")
    assert launcher, "Installed myravant-play executable required"
    folder.mkdir()
    checkpoint = folder / "campaign.json"
    order = "reversed" if name == "actor-scarcity" else "standard"
    fixture = create_surface_fixture(reverse_order=order == "reversed")
    stages = []
    app = None

    def play(*commands):
        nonlocal app
        trace = folder / (str(len(stages)) + ".jsonl")
        cmd = [launcher, "--locality", "tarrow-surface-water",
               "--surface-order", order, "--checkpoint", str(checkpoint),
               "--trace", str(trace), "--repository-sha", sha]
        if checkpoint.exists():
            cmd += ["--load", str(checkpoint)]
        result = subprocess.run(
            cmd, input="\n".join((*commands, "save", "exit", "")),
            text=True, capture_output=True, timeout=90)
        assert result.returncode == 0, (cmd, result.stdout, result.stderr)
        events = [json.loads(row) for row in trace.read_text().splitlines()]
        assert events[-1]["evidence_complete"] is True
        restored = SurfaceWaterApplication.restore(fixture=fixture, checkpoint_path=checkpoint)
        if app:
            assert restored.journal[:len(app.journal)] == app.journal
        assert accounting(restored) == (12, "7")
        app = restored
        stages.append({
            "commands": commands, "result": result.stdout[-900:],
            "journal_length": len(app.journal),
            "intervals": len(app.intervals),
            "digest": app.authoritative_digest(),
            "accounting": accounting(app),
            "trace": str(trace),
        })

    workshop = ("go south", "go west", "go west", "go west")
    objectives = {}
    if name == "recovery":
        play(*workshop, "take wash bucket", "take pouring jug",
             "take packing felt", "pour 3 units from wash bucket onto practice panel")
        objectives["real_surface_stock"] = stock(app, "practice-panel") == 3
        play("scoop from practice panel into pouring jug",
             "blot practice panel using packing felt",
             "wring packing felt into wash bucket")
        objectives["recovery_into_specific_compartments"] = (
            stock(app, "practice-panel") == 0
            and stock(app, "pouring-jug") == 2
            and stock(app, "packing-felt") == 0)
    elif name == "packed-contact":
        play(*workshop, "take wash bucket", "take packing felt",
             "take cleaning cloth", "pour 3 units from wash bucket onto practice panel",
             "blot practice panel using packing felt")
        objectives["partial_blot_and_capacity"] = (
            stock(app, "practice-panel") == 1 and stock(app, "packing-felt") == 2)
        play("open parts tray", "store packing felt in parts tray")
        objectives["storage_not_implicit_contact"] = (
            stock(app, "packing-felt") == 2 and stock(app, "cleaning-cloth") == 0)
        play("retrieve packing felt from parts tray",
             "press packing felt against cleaning cloth", "wait 4 steps")
        objectives["explicit_contact_and_only_absorbent_drying"] = (
            stock(app, "practice-panel") == 1
            and sum(v for _, v in app.environment_state.evaporated) >= 1
            and stock(app, "packing-felt") < 2)
    elif name == "actor-scarcity":
        play(*workshop, "take wash bucket",
             "pour 2 units from wash bucket onto practice panel",
             "ask oren to blot practice panel using cleaning cloth")
        objectives["agreement_no_free_work"] = stock(app, "practice-panel") == 2
        play("wait", "wait", "wait", "wait")
        worker = selected(app.participation_state, identity("oren"))
        objectives["qualified_actor_contributed_to_actual_stock"] = (
            stock(app, "practice-panel") == 0
            and worker.status == "completed" and len(worker.contributions) >= 2)
    else:
        raise ValueError(name)
    assert all(objectives.values()), (name, objectives, stages)
    return {"scenario": name, "order": order, "objectives": objectives,
            "stages": stages, "final_digest": app.authoritative_digest(),
            "receipt_ids": tuple(row["result"].get("receipt_id")
                                 for row in app.journal if isinstance(row, dict)
                                 and isinstance(row.get("result"), dict))}


def report(path):
    head = subprocess.run(["git", "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()
    entries = []
    with tempfile.TemporaryDirectory(prefix="myravant-surface-water-") as root:
        for case in SCENARIOS:
            repeats = [journey(Path(root) / (case + "-" + str(i)), case, head)
                       for i in range(2)]
            assert repeats[0]["final_digest"] == repeats[1]["final_digest"]
            assert repeats[0]["receipt_ids"] == repeats[1]["receipt_ids"]
            entries.append({"case": case, "repeats": repeats})
    result = {"schema": "myravant.surface-water-installed.v1",
              "source_sha": head, "engineering_authored": True,
              "blind": False, "human_acceptance": False,
              "journeys": entries}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print("Surface water: three objective-first installed journeys repeated twice.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    report(parser.parse_args().output)
