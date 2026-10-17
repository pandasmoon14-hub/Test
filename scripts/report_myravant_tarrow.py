"""Authored installed Tarrow journeys, restart and independent end predicates."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_play_application import MyravantPlayApplication as App
from astra_runtime.myravant_tarrow import create_tarrow_fixture, identity


def campaign(root, kind, head):
    checkpoint = root / "save.json"
    stages = []
    previous = None
    def stage(*commands):
        nonlocal previous
        trace = root / f"trace-{len(stages)}.jsonl"
        args = [shutil.which("myravant-play"), "--locality", "tarrow", "--checkpoint", str(checkpoint),
                "--trace", str(trace), "--repository-sha", head]
        if checkpoint.exists():
            args += ["--load", str(checkpoint)]
        result = subprocess.run(args, input="\n".join((*commands, "save", "exit", "")),
                                capture_output=True, text=True, timeout=45)
        assert result.returncode == 0, (result.stdout, result.stderr)
        assert "\\n" not in result.stdout and "\\r" not in result.stdout
        rows = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
        assert rows[-1]["evidence_complete"]
        interactions = [r for r in rows if r["record_type"] == "interaction"]
        if previous is not None:
            assert interactions[0]["pre_state_digest"] == previous
        for a,b in zip(interactions, interactions[1:]):
            assert a["post_state_digest"] == b["pre_state_digest"]
        app = App.restore(checkpoint_path=checkpoint, fixture=create_tarrow_fixture())
        assert app.authoritative_digest() == interactions[-1]["post_state_digest"]
        previous = app.authoritative_digest()
        stages.append({"commands": commands, "stdout": result.stdout, "stderr": result.stderr, "records": rows})
        return result.stdout, app
    if kind == "illumination":
        text, _ = stage("go south then go east", "inspect floodmark post")
        assert "cannot" in text.casefold()
        stage("go west then go north", "take shuttered service lamp", "light shuttered service lamp")
        text, app = stage("go south then go east", "inspect floodmark post", "take floodmark post", "wait")
        assert "Fixed water-level" in text and "cannot pick" in text
        objectives = {"actual_lamp_local": app._bounded_local_light_available(),
                      "player_underbank": app.current_place_id() == identity("underbank"),
                      "fixed_post_retained": any(r.subject_entity_id == identity("post") and r.object_entity_id == identity("underbank") for r in app.state.representation.relations)}
    elif kind == "stores":
        stage("take shuttered service lamp", "light shuttered service lamp", "go south then open red-lashed parts coffer")
        text, app = stage("inspect red-lashed parts coffer", "take oak gate wedge")
        assert "Inside: Oak Gate Wedge, Maintenance Slate" in text and "Soft-Iron Pin Blank" not in text
        stage("put shuttered service lamp in red-lashed parts coffer", "close red-lashed parts coffer")
        _, app = stage("go east", "wait", "look")
        objectives = {"closed_coffer_hides_lamp_signal": not app._bounded_local_light_available(),
                      "wedge_carried": any(r.subject_entity_id == identity("wedge") and r.object_entity_id == app.fixture.player_entity_id for r in app.state.representation.relations)}
    else:
        stage("go north", "inspect nala vey", "go south then go west", "inspect rho pell")
        stage("go east then go south", "go west", "inspect oren kesh", "go east then go south")
        stage("go south then go west", "look", "wait")
        _, app = stage("go east then go north", "go north then go north", "inspect self")
        objectives = {"returned_common": app.current_place_id() == identity("common"),
                      "time_survives_return": app.runtime_state.logical_time_state.logical_position == 1,
                      "seven_individual_actors": len(app.fixture.actor_presentations) == 7}
    assert all(objectives.values()), objectives
    return {"profile": kind, "objectives": objectives, "final_digest": previous, "stages": stages}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    profiles = []
    with tempfile.TemporaryDirectory(prefix="tarrow-evidence-") as directory:
        for kind in ("illumination", "stores", "locality"):
            runs = []
            for repeat in range(2):
                root = Path(directory) / f"{kind}-{repeat}"; root.mkdir()
                runs.append(campaign(root, kind, head))
            assert runs[0]["final_digest"] == runs[1]["final_digest"]
            profiles.append(runs[0])
    args.output.write_text(json.dumps({"repository_sha": head, "implementation_authored": True,
        "not_blind_or_human_acceptance": True, "repeat_count": 2, "profiles": profiles}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Tarrow: 3 installed profiles repeated twice; all restart and objective checks passed.")


if __name__ == "__main__":
    main()
