"""Installed body selection, qualification, compatibility, and durable replay."""

import io
import json
import os
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_local_checkpoint_restore import (
    PersistentWorldCheckpointError,
    PersistentWorldCheckpointWriteError,
)
from astra_runtime.myravant_development_embodiment import create_development_embodiment_fixture
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID, GROUNDSKEEPER_ID, ORCHARD_PATH_ID, WAYSTONE_ID, WORKSHOP_ID, YARD_ID,
)
from astra_runtime.myravant_posture_checkpoint import EMBODIMENT_CHECKPOINT_VERSION
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application as App


OBSTRUCT = (
    "take lantern", "light lantern", "walk south", "walk east",
    "drag waystone west", "walk west",
)
BODY_COMMANDS = [
    ("low-frame", "Low frame", "stand", "standing", "crouch", "crouching"),
    ("folding-frame", "Folding frame", "extend", "extended", "fold", "folded"),
]


def checkpoint(root):
    return root / "checkpoint.json"


def checkpoint_digest(root):
    path = checkpoint(root)
    return sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def play(root, label, commands, *, body=None, course=None, load=False, exit_code=0, locality=None):
    root.mkdir(exist_ok=True)
    trace = root / (label + ".jsonl")
    launcher = shutil.which("myravant-play")
    assert launcher, "install myravant-play before running this suite"
    argv = [launcher, "--trace", str(trace)]
    argv.extend(("--load" if load else "--checkpoint", str(checkpoint(root))))
    if body is not None:
        argv.extend(("--development-body", body))
    if course is not None:
        argv.extend(("--development-course", course))
    if locality is not None:
        argv.extend(("--locality", locality))
    inputs = (*commands, "exit")
    before = checkpoint_digest(root)
    result = subprocess.run(
        argv, input="\n".join((*inputs, "")), text=True, capture_output=True, timeout=60,
    )
    assert result.returncode == exit_code, (argv, result.stdout, result.stderr)
    records = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()] if trace.exists() else []
    if exit_code == 0:
        assert records[0]["record_type"] == "session_start"
        assert records[-1]["evidence_complete"]
    else:
        assert not records
    if directory := os.environ.get("MYRAVANT_EMBODIMENT_REPORT_DIR"):
        path = Path(directory) / root.name / (label + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "argv": argv, "stdin": inputs, "stdout": result.stdout, "stderr": result.stderr,
            "exit_status": result.returncode, "trace": records,
            "checkpoint_before": before, "checkpoint_after": checkpoint_digest(root),
        }, indent=2) + "\n", encoding="utf-8")
    return result, [row for row in records if row["record_type"] == "interaction"]


def restore(root, body, course="orchard"):
    return App.restore(
        fixture=create_development_embodiment_fixture(body, course),
        checkpoint_path=checkpoint(root),
    )


def stable(row, *, failure=None):
    assert not row["authoritative_changed"]
    assert row["pre_state_digest"] == row["post_state_digest"]
    assert row["receipt_id"] is None
    if failure is not None:
        assert row["failure_class"] == failure


@pytest.mark.parametrize("body,name,upright,initial,lower,lowered", BODY_COMMANDS)
@pytest.mark.parametrize("course,direction,destination", [
    ("orchard", "east", ORCHARD_PATH_ID), ("gatehouse", "south", GATEHOUSE_ID),
])
def test_installed_profile_journey(tmp_path, body, name, upright, initial, lower, lowered,
                                   course, direction, destination):
    root = tmp_path / f"{body}-{course}"
    binding = dict(body=body, course=course)
    walk = f"walk {direction}"
    first, rows = play(root, "staged", (
        "inspect self", "help all", *OBSTRUCT, upright, walk, upright, "save",
    ), **binding)
    assert f"Development body: {name}" in first.stdout
    assert "Recorded posture: unrecorded" in first.stdout
    assert "You move to the Orchard Path" in first.stdout
    assert "kneel" not in first.stdout
    assert f"Try {lower} then {walk}" in first.stdout
    if body == "folding-frame":
        assert "crouch" not in first.stdout and "crawl " not in first.stdout
    stable(rows[-3], failure="movement_opportunity_obstructed")
    stable(rows[-2])
    assert rows[-2]["result_type"] == "posture_unchanged"
    before = restore(root, body, course)
    assert before.posture_state.configuration == initial
    assert before.current_place_id() == before.entity_place_id(WAYSTONE_ID) == YARD_ID
    assert before.runtime_state.logical_time_state.logical_position == 0
    assert len(before.posture_state.events) == 1
    assert before.authoritative_digest() == rows[-1]["post_state_digest"]

    second, resumed = play(root, "resumed", (
        walk, f"{lower} silently then {walk}", f"{lower} then {walk}", "inspect self", "save",
    ), load=True, **binding)
    stable(resumed[0], failure="movement_opportunity_obstructed")
    stable(resumed[1])
    assert resumed[1]["failure_class"] and resumed[1]["parsed_action"] == "unsupported"
    assert before.authoritative_digest() == resumed[0]["pre_state_digest"]
    assert resumed[2]["parsed_action"] == "sequence_1_change_posture"
    assert resumed[3]["parsed_action"] == "sequence_2_move"
    assert resumed[2]["receipt_id"] and resumed[3]["receipt_id"]
    assert ":posture-opportunity-" in resumed[3]["opportunity_evidence_id"]
    assert f"Recorded posture: {lowered}" in second.stdout
    after = restore(root, body, course)
    assert after.current_place_id() == destination
    assert after.runtime_state.logical_time_state.logical_position == 0
    assert after.posture_state.events[:1] == before.posture_state.events
    assert tuple(after.state.committed_transitions[:len(before.state.committed_transitions)]) == before.state.committed_transitions
    assert after.state.committed_transitions[-1].receipt.receipt_id == resumed[3]["receipt_id"]
    assert after.authoritative_digest() == resumed[-1]["post_state_digest"]

    uninterrupted_root = tmp_path / f"{body}-{course}-direct"
    _, direct = play(uninterrupted_root, "uninterrupted", (
        *OBSTRUCT, upright, walk, lower, walk,
    ), **binding)
    uninterrupted = restore(uninterrupted_root, body, course)
    assert uninterrupted.state == after.state
    assert uninterrupted.posture_state == after.posture_state
    assert uninterrupted.authoritative_digest() == after.authoritative_digest()
    assert direct[-1]["receipt_id"] == resumed[3]["receipt_id"]


def test_body_changes_crawl_access_on_the_same_corridor_and_keeps_ordinary_walk(tmp_path):
    low, folding = (tmp_path / name for name in ("crawl-low-frame", "crawl-folding-frame"))
    _, lowered = play(low, "crawl", ("inspect self", "crawl south"), body="low-frame")
    folded, held = play(folding, "crawl", ("inspect self", "crawl south", "save"), body="folding-frame")
    assert lowered[-1]["result_type"] == "movement_committed" and lowered[-1]["receipt_id"]
    stable(held[1], failure="traversal_method_opportunity_unavailable")
    assert "no qualified crawl" in folded.stdout
    left, right = restore(low, "low-frame"), restore(folding, "folding-frame")
    assert left.current_place_id() == YARD_ID and right.current_place_id() == WORKSHOP_ID
    assert left.fixture.initial_state == right.fixture.initial_state
    assert left.posture_state.configuration is right.posture_state.configuration is None
    assert left.runtime_state.logical_time_state.logical_position == right.runtime_state.logical_time_state.logical_position == 0
    _, alternative = play(folding, "walk", ("walk south",), body="folding-frame", load=True)
    assert alternative[-1]["receipt_id"] and restore(folding, "folding-frame").current_place_id() == YARD_ID


def test_follower_cannot_borrow_folding_clearance(tmp_path):
    root = tmp_path / "independent-follower"
    result, rows = play(root, "crossing", (
        *OBSTRUCT, "wait", "ask groundskeeper to follow me", "fold then walk east",
    ), body="folding-frame")
    assert rows[-1]["receipt_id"] and rows[-1]["consequence_receipt_id"] is None
    assert "cannot use your recorded posture's passage clearance" in result.stdout
    app = restore(root, "folding-frame")
    assert app.current_place_id() == ORCHARD_PATH_ID
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


@pytest.mark.parametrize("course,direction,destination", [
    ("orchard", "east", ORCHARD_PATH_ID), ("gatehouse", "south", GATEHOUSE_ID),
])
def test_lawful_displacement_changes_opportunity_without_rebinding(tmp_path, course, direction, destination):
    root = tmp_path / f"clear-{course}"
    args = dict(body="folding-frame", course=course)
    walk = f"walk {direction}"
    _, blocked = play(root, "blocked", (*OBSTRUCT, "extend", walk), **args)
    stable(blocked[-1], failure="movement_opportunity_obstructed")
    old = restore(root, **args)
    envelope = json.loads(checkpoint(root).read_text(encoding="utf-8"))
    _, cleared = play(root, "cleared", ("push waystone north", walk), load=True, **args)
    assert [row["result_type"] for row in cleared] == ["object_displacement_committed", "movement_committed"]
    assert all(row["receipt_id"] for row in cleared)
    assert ":posture-opportunity-" not in cleared[-1]["opportunity_evidence_id"]
    app = restore(root, **args)
    assert app.current_place_id() == destination
    assert app.posture_state == old.posture_state
    assert app.entity_place_id(WAYSTONE_ID) == WORKSHOP_ID
    new = json.loads(checkpoint(root).read_text(encoding="utf-8"))
    assert envelope["authoritative_payload"]["components"]["embodiment_binding"] == (
        new["authoritative_payload"]["components"]["embodiment_binding"]
    )


def test_immediate_checkpoint_pins_body_and_course_and_preserves_legacy(tmp_path):
    root = tmp_path / "immediate-save"
    play(root, "first", ("save",), body="folding-frame")
    saved = checkpoint(root).read_bytes()
    assert json.loads(saved)["format_version"] == EMBODIMENT_CHECKPOINT_VERSION
    assert restore(root, "folding-frame").posture_state.configuration is None
    assert restore(root, "folding-frame").current_place_id() == WORKSHOP_ID
    for description, args in (
        ("wrong-body", {"body": "low-frame"}),
        ("wrong-course", {"body": "folding-frame", "course": "gatehouse"}),
        ("legacy-loader", {}),
    ):
        result, _ = play(root, description, ("save",), load=True, exit_code=2, **args)
        assert "Unable to restore checkpoint" in result.stderr
        assert checkpoint(root).read_bytes() == saved
    result, _ = play(root, "new-over-save", ("save",), body="folding-frame", exit_code=2)
    assert "Use --load" in result.stderr and checkpoint(root).read_bytes() == saved
    result, _ = play(root, "invalid-combination", ("save",), body="folding-frame", locality="tarrow",
                     load=True, exit_code=2)
    assert "require the development locality" in result.stderr
    assert checkpoint(root).read_bytes() == saved

    legacy = tmp_path / "legacy-save"
    play(legacy, "first", ("crouch", "save"))
    saved = checkpoint(legacy).read_bytes()
    assert json.loads(saved)["format_version"] == 11
    play(legacy, "matching", ("inspect self",), load=True)
    play(legacy, "new-body", ("save",), body="low-frame", load=True, exit_code=2)
    assert checkpoint(legacy).read_bytes() == saved


@pytest.mark.parametrize("change", ["posture-clearance", "crawl-clearance", "obstruction", "commands"])
def test_static_declaration_change_refuses_before_any_affected_movement(tmp_path, change):
    root = tmp_path / f"change-{change}"
    play(root, "before-crossing", (*OBSTRUCT, "crouch"), body="low-frame")
    path = checkpoint(root)
    saved = path.read_bytes()
    good = restore(root, "low-frame")
    fixture = good.fixture
    assert good.current_place_id() == YARD_ID and good.posture_state.configuration == "crouching"
    if change == "posture-clearance":
        changed = replace(fixture, posture_movement_licenses=(
            replace(fixture.posture_movement_licenses[0], configurations=("standing",)),))
    elif change == "crawl-clearance":
        changed = replace(fixture, movement_method_routes=())
    elif change == "obstruction":
        changed = replace(fixture, movement_obstruction_licenses=(
            replace(fixture.movement_obstruction_licenses[0], blocking_object_place_id=ORCHARD_PATH_ID),))
    else:
        changed = replace(fixture, embodiment=replace(
            fixture.embodiment, configuration_commands=(("rise", "standing"), ("crouch", "crouching"))))
    assert changed.posture_profile == fixture.posture_profile and changed.provenance == fixture.provenance
    with pytest.raises(PersistentWorldCheckpointError, match="binding does not match"):
        App.restore(fixture=changed, checkpoint_path=path)
    assert path.read_bytes() == saved
    assert restore(root, "low-frame").move("east").authoritative_changed


def test_checkpoint_failure_keeps_the_acknowledged_sequence_prefix(tmp_path, monkeypatch):
    import astra_runtime.myravant_posture_checkpoint as checkpoints

    root = tmp_path / "failed-crossing"
    play(root, "setup", OBSTRUCT, body="folding-frame")
    app = restore(root, "folding-frame")
    original = checkpoints._write_envelope
    durable = []

    def fail_second(**kwargs):
        if durable:
            raise PersistentWorldCheckpointWriteError("injected before replacement")
        digest = original(**kwargs)
        durable.append(checkpoint(root).read_bytes())
        return digest

    monkeypatch.setattr(checkpoints, "_write_envelope", fail_second)
    output = io.StringIO()
    with pytest.raises(SystemExit) as failure:
        run_terminal(app, input_stream=io.StringIO("fold then walk east\n"), output_stream=output)
    assert failure.value.code == 3
    assert "Your recorded posture is now folded" in output.getvalue()
    assert "You move to the Orchard Path" not in output.getvalue()
    assert checkpoint(root).read_bytes() == durable[0]
    restored = restore(root, "folding-frame")
    assert restored.posture_state.configuration == "folded"
    assert restored.current_place_id() == YARD_ID
    assert restored.move("east").authoritative_changed
