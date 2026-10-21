"""Installed objective-first investigation journeys, not blind/human acceptance."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from astra_runtime.myravant_investigation_cases import build_investigation_case
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture
from astra_runtime.domain.persistent_world_material import placement


def _id(fixture, name):
    return next(p.entity_id for p in fixture.object_presentations if p.name == name)


def _actor(fixture, name):
    return next(p.entity_id for p in fixture.actor_presentations if p.name == name)


def journey(root, recipe, repository_sha):
    checkpoint = root / "history.json"
    app, preparation = build_investigation_case(recipe, checkpoint)
    initial = app.authoritative_digest()
    fixture = create_investigation_fixture(recipe)
    launcher = shutil.which("myravant-play")
    assert launcher, "installed launcher required"
    steps = []

    def stage(*commands):
        nonlocal app
        trace = root / (str(len(steps)) + ".jsonl")
        args = [launcher, "--locality", "tarrow-investigation",
                "--investigation-case", recipe, "--checkpoint", str(checkpoint),
                "--load", str(checkpoint), "--trace", str(trace),
                "--repository-sha", repository_sha]
        started = time.perf_counter()
        proc = subprocess.run(args, input="\n".join((*commands, "save", "exit", "")),
                              text=True, capture_output=True, timeout=90)
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        records = [json.loads(line) for line in trace.read_text().splitlines()]
        assert records[-1]["evidence_complete"]
        observed = [r for r in records if r["record_type"] == "interaction"]
        assert observed and observed[-1]["post_state_digest"]
        for row in observed:
            command = row["raw_player_input"].strip().casefold()
            if command.startswith(("recall ", "compare ")):
                assert row["pre_state_digest"] == row["post_state_digest"]
                assert row["logical_time_before"] == row["logical_time_after"]
                assert row.get("failure_class") is None
        restored = InvestigationApplication.restore(fixture=fixture, checkpoint_path=checkpoint)
        assert restored.authoritative_digest() == observed[-1]["post_state_digest"]
        steps.append({"commands": commands, "trace": records, "stdout": proc.stdout,
                      "duration_seconds": time.perf_counter() - started,
                      "restored_digest": restored.authoritative_digest()})
        app = restored
        return proc.stdout

    def until(predicate, limit=12):
        for _ in range(limit):
            if predicate(app):
                return
            stage("wait")
        assert predicate(app), "objective did not become true within bounded intervals"

    if recipe == "neutral-relay":
        panel = _id(fixture, "Panel A")
        before = dict(app.water_state.adhered)[panel]
        assert before == 3 and app.disclosed_relays
        text = stage("inspect panel a", "recall panel a residue",
                     "compare reports about panel a residue")
        assert "received statement from" in text and "own admitted observation" in text
        assert "Different retained values" in text and "No account is selected as true" in text
        assert dict(app.water_state.adhered)[panel] == before
        stage("take brush", "scrub panel a using brush")
        changed = dict(app.water_state.adhered)[panel]
        assert changed < before, "player action must change actual residue, not an investigation flag"
        text = stage("inspect panel a", "compare reports about panel a residue")
        assert "No account is selected as true" in text
        # The comparison must retain an earlier distinct received account
        # even after repeated newer physical observations.
        assert "Different retained values" in text, text
        assert "clear" in text and "present" in text, text
        objectives = {"historical_false_account_retained": bool(app.disclosed_relays),
                      "historical_and_current_contrary_values": (
                          "Different retained values" in text
                          and "clear" in text and "present" in text),
                      "material_after_player_action_changed": changed < before,
                      "no_omniscient_guilt_resolution": True}
    else:
        brush = _id(fixture, "Brush")
        winner = fixture.actor_order[0]
        assert placement(app.state.representation, brush).object_entity_id == winner
        text = stage("go east", "inspect panel a", "recall panel a residue",
                     "compare reports about panel a residue")
        assert "Retained player history" in text and "Comparison of retained" in text
        if recipe == "neutral-contended":
            panel = _id(fixture, "Panel A")
            until(lambda a: dict(a.water_state.adhered)[panel] == 0)
            owner = _actor(fixture, "Jun")
        else:
            owner = _actor(fixture, "Jun")
            from astra_runtime.domain import persistent_world_actor_participation as part
            assert part.selected(app.participation_state, owner).status == "withdrawn"
        name = fixture.entity_name(owner)
        request = stage("ask " + name + " to assemble joining frame")
        assert "assembly" in request.casefold(), request
        until(lambda a: bool(a.connections))
        assert app.connections, "actual assembly joint required"
        text = stage("inspect plate", "compare reports about plate assembly")
        plate = _id(fixture, "Plate")
        admitted_assembly = tuple(
            e for e in app.evidence_state.events
            if e.actor_id == fixture.player_entity_id
            and e.target_id == plate and e.facet == "assembly"
            and e.kind == "witnessed"
        )
        observed_states = {e.value for e in admitted_assembly}
        # A missing history is not a successful investigation objective.
        # The player must have lawfully witnessed both the separate and
        # completed configurations; querying those records changes no owner.
        contrasted = (("joining frame", "separate") in observed_states
                      and ("joining frame", "joined") in observed_states
                      and "Different retained values" in text
                      and "joined" in text and "separate" in text)
        objectives = {"distinct_shared_resource_priority": placement(
                          app.state.representation, brush).object_entity_id == winner,
                      "real_reversible_joining": bool(app.connections),
                      "history_before_and_after_action": contrasted,
                      "work_and_evidence_replay_survive_restart": True}
    assert all(objectives.values()), objectives
    return {"recipe": recipe, "prehistory_receipts": preparation,
            "initial_digest": initial, "final_digest": app.authoritative_digest(),
            "objectives": objectives, "stages": steps,
            "limits": ["engineering-authored scenario, not independent or human",
                       "timing/observations are bounded by the named neutral recipes"]}


def report(output):
    head = subprocess.run(["git", "rev-parse", "HEAD"], text=True,
                          capture_output=True, check=True).stdout.strip()
    entries = []
    with tempfile.TemporaryDirectory(prefix="investigation-journeys-") as temp:
        for recipe in ("neutral-contended", "neutral-reverse", "neutral-relay"):
            repetitions = []
            for i in range(2):
                root = Path(temp) / (recipe + "-" + str(i))
                root.mkdir()
                repetitions.append(journey(root, recipe, head))
            assert repetitions[0]["final_digest"] == repetitions[1]["final_digest"]
            entries.append({"recipe": recipe, "repeats": repetitions})
    body = {"repository_sha": head, "kind": "investigation-installed-journeys",
            "engineering_authored": True, "blind": False,
            "human_acceptance": False, "profiles": entries}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(body, sort_keys=True, indent=2) + "\n")
    print("Investigation: three installed objective-first journeys repeated twice.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report(args.output)


if __name__ == "__main__":
    main()
