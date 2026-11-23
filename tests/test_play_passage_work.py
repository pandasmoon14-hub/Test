"""Installed and owner-path evidence for cooperative passage work."""

import json
import os
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess

import pytest

from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime.domain.persistent_world_material import placement, role
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_transformation import create_transformation_fixture
from astra_runtime.myravant_transformation_application import PassageWorkApplication as App


YARD = "sorting-bay-work"
WORKSHOP = "workshop-passage-work"
STAGE_CROSSBAR = (
    "go south", "go west", "inspect passage work",
    "take barrier crossbar", "put barrier crossbar on yard work trestle",
)
BOARD_ON_TRESTLE = ("take barrier board", "put barrier board on yard work trestle")


def run(root, name, *commands, case=YARD, load=False, expected=0):
    launcher = shutil.which("myravant-play")
    assert launcher, "install myravant-play first"
    checkpoint = root / "campaign.json"
    trace = root / f"{name}.jsonl"
    before = checkpoint.read_bytes() if checkpoint.exists() else None
    argv = [launcher, "--locality", "tarrow-transformation", "--transformation-case", case,
            "--load" if load else "--checkpoint", str(checkpoint), "--trace", str(trace)]
    inputs = (*commands, "exit")
    process = subprocess.run(
        argv, input="\n".join((*inputs, "")), capture_output=True, text=True, timeout=120,
    )
    assert process.returncode == expected, (process.stdout, process.stderr)
    after = checkpoint.read_bytes() if checkpoint.exists() else None
    records = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()] if trace.exists() else []
    if expected == 0:
        assert records[-1]["evidence_complete"]
    else:
        assert before == after and not records
    if output := os.environ.get("MYRAVANT_PASSAGE_WORK_REPORT_DIR"):
        path = Path(output) / root.name / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "argv": argv, "case": case, "stdin": inputs, "stdout": process.stdout,
            "stderr": process.stderr, "exit_status": process.returncode, "trace": records,
            "checkpoint_before": sha256(before).hexdigest() if before else None,
            "checkpoint_after": sha256(after).hexdigest() if after else None,
        }, indent=2) + "\n", encoding="utf-8")
    return process, [row for row in records if row["record_type"] == "interaction"]


def restored(root, case=YARD):
    return App.restore(fixture=create_transformation_fixture(passage_case=case),
                       checkpoint_path=root / "campaign.json")


def refuse(row, failure):
    assert row["failure_class"] == failure and not row["authoritative_changed"]
    assert row["receipt_id"] is None and row["pre_state_digest"] == row["post_state_digest"]


def receipt_events(app, actor, op):
    return [event for event in app.actor_events if event[1:3] == (op, identity(actor))]


def test_installed_personal_refit_then_voluntary_release_and_cord_return(tmp_path):
    first, rows = run(
        tmp_path, "refit-interrupted", *STAGE_CROSSBAR, "take alignment tool",
        "start refitting barrier crossbar using alignment tool", "work transformation",
        "drop alignment tool", "work transformation", "save",
    )
    assert "start refitting Barrier Crossbar using Alignment Tool" in first.stdout
    assert "with Barrier Spare" not in first.stdout
    interrupted = rows[-2]
    assert interrupted["failure_class"] == "timed_action_interrupted"
    assert interrupted["logical_time_after"] == interrupted["logical_time_before"] + 1
    partial = restored(tmp_path)
    assert partial.transform_state.work.stage == 1
    assert partial.transform_state.work.status == "blocked"
    prefix = partial.transform_state.lineage
    assert len(prefix) == 1 and prefix[0][1] == partial.fixture.player_entity_id

    separate, _ = run(
        tmp_path, "separate-work-during-partial-refit",
        "ask tali ren to clean sorting board using cleaning brush by scrubbing",
        "wait", "wait", "wait", "ask tali ren about sorting board activity", load=True,
    )
    assert "Tali Ren reports historical performed evidence: scrub" in separate.stdout
    kept = restored(tmp_path)
    assert kept.transform_state == partial.transform_state
    assert placement(kept.state.representation, identity("barrier-crossbar")) == placement(
        partial.state.representation, identity("barrier-crossbar"))
    cleaning = participation.selected(kept.participation_state, identity("tali"))
    assert cleaning.status == "completed" and len(cleaning.contributions) == 3

    next_run, rows = run(
        tmp_path, "assemble-and-agree", "take alignment tool", "work transformation",
        *BOARD_ON_TRESTLE, "take barrier cord", "start assembling passage barrier",
        "work", "go north",
        "inspect passage work then ask tali ren to release passage barrier",
        "ask tali ren to release passage barrier", "save", load=True,
    )
    refuse(next(row for row in rows if row["raw_player_input"].strip() == "go north"),
           "material_passage_obstructed")
    refuse(rows[-2], "passage_release_unavailable")
    assert "The actor is busy" in next_run.stdout
    assert "You can ask Tali Ren to release passage barrier" in next_run.stdout
    assert rows[-3]["parsed_action"] == "sequence_2_passage_work"
    before_release = restored(tmp_path)
    assert before_release.transform_state.lineage[:1] == prefix
    assert role(before_release.transform_state, identity("barrier-crossbar")) == "fit"
    accepted = participation.selected(before_release.participation_state, identity("tali"))
    assert accepted.status == "active" and not accepted.contributions
    assert len(before_release.connections) == 1

    repeat_root = tmp_path / "repeat"
    repeat_root.mkdir()
    shutil.copyfile(tmp_path / "campaign.json", repeat_root / "campaign.json")
    commands = ("wait", "ask tali ren about barrier board activity",
                "ask tali ren for barrier cord", "go north", "save")
    final, rows = run(tmp_path, "release-and-return", *commands, load=True)
    app = restored(tmp_path)
    assert app.journal[:len(before_release.journal)] == before_release.journal
    # The installed startup records the ordinary first look before reading stdin.
    startup = app.journal[len(before_release.journal)]
    assert startup["method"] == "look"
    assert startup["result"]["pre_state_digest"] == before_release.authoritative_digest()
    assert startup["result"]["post_state_digest"] == rows[0]["pre_state_digest"]
    assert app.current_place_id() == identity("yard-sorting") and not app.connections
    task = participation.selected(app.participation_state, identity("tali"))
    event, = (event for event in receipt_events(app, "tali", "physical_contribution")
              if event[3][0] == "passage_release")
    assert task.status == "completed" and task.contributions == (event[0],)
    assert event[3][1] == "untie"
    assert "Tali Ren reports historical performed evidence: untie" in final.stdout
    assert placement(app.state.representation, identity("barrier-cord")).object_entity_id == app.fixture.player_entity_id
    assert len(receipt_events(app, "tali", "physical_return")) == 1
    _, repeated = run(repeat_root, "release-and-return", *commands, load=True)
    assert [r["receipt_id"] for r in rows] == [r["receipt_id"] for r in repeated]
    assert restored(repeat_root).authoritative_digest() == app.authoritative_digest()


def test_installed_spare_and_qualified_worker_change_west_passage(tmp_path):
    setup, rows = run(
        tmp_path, "spare-route", *STAGE_CROSSBAR,
        "start refitting barrier crossbar using alignment tool",
        "ask tali ren to replace barrier crossbar with barrier spare",
        "ask oren kesh to replace barrier crossbar with barrier spare",
        *BOARD_ON_TRESTLE, "take barrier cord",
        "tie barrier board to barrier spare using barrier cord", "go west", "save",
        case=WORKSHOP,
    )
    assert "start replacing Barrier Crossbar with Barrier Spare" in setup.stdout
    assert "using Alignment Tool" not in setup.stdout
    assert "The actor declines." in setup.stdout
    refusals = [row for row in rows if row["failure_class"] == "transformation_acceptance_unavailable"]
    assert len(refusals) == 2
    for row in refusals:
        refuse(row, "transformation_acceptance_unavailable")
    refuse(rows[-2], "material_passage_obstructed")
    blocked = restored(tmp_path, WORKSHOP)
    assert [row[1] for row in blocked.transform_state.lineage] == [identity("oren")] * 2
    assert all(row[6] for row in blocked.transform_state.lineage)
    assert len(receipt_events(blocked, "oren", "transformation_preparation")) == 1
    assert placement(blocked.state.representation, identity("barrier-crossbar")).object_entity_id == identity("oren")
    assert placement(blocked.state.representation, identity("barrier-spare")).relation_type == "supported_by"
    assert blocked.fixture.passage_work.direction == "west"
    for variant in (YARD, "standard"):
        rejected, _ = run(tmp_path, "foreign-" + variant, "save", case=variant, load=True, expected=2)
        assert "Unable to restore checkpoint" in rejected.stderr

    result, rows = run(
        tmp_path, "release-west", "go north", "go south",
        "ask tali ren to release restored barrier",
        "ask oren kesh to release restored barrier", "wait", "go west", "save",
        case=WORKSHOP, load=True,
    )
    assert rows[0]["receipt_id"] and not rows[0]["failure_class"]
    refuse(rows[2], "passage_release_unavailable")
    assert "The actor declines this work" in result.stdout
    assert rows[-2]["receipt_id"] and not rows[-2]["failure_class"]
    app = restored(tmp_path, WORKSHOP)
    assert app.journal[:len(blocked.journal)] == blocked.journal
    assert app.current_place_id() == identity("workshop") and not app.connections
    assert placement(app.state.representation, identity("barrier-cord")).object_entity_id == identity("oren")
    assert len(receipt_events(app, "oren", "physical_contribution")) == 1
    digest = app.authoritative_digest()
    status = app.transformation_status()
    assert status.failure_class == "transformation_status_unavailable"
    assert all(word not in status.message for word in ("Oren", "replace", "completed", "unfit"))
    assert app.authoritative_digest() == digest


def closed_app(path=None):
    app = App.new(checkpoint_path=path)
    attempts = [
        (app.move, "south"), (app.move, "west"),
        (app.pickup, "barrier crossbar"),
        (app.material, "put_on", "barrier crossbar", "yard work trestle"),
        (app.pickup, "alignment tool"),
        (app.begin_transformation, "refit", "barrier crossbar", "alignment tool"),
        (app.contribute_transformation,), (app.contribute_transformation,),
        (app.pickup, "barrier board"),
        (app.material, "put_on", "barrier board", "yard work trestle"),
        (app.pickup, "barrier cord"),
        (app.material, "tie", "barrier board", "barrier crossbar", "barrier cord"),
    ]
    for action, *args in attempts:
        assert action(*args).authoritative_changed
    return app


def test_stale_release_remains_bound_to_old_fastening_after_restart(tmp_path):
    app = closed_app(tmp_path / "campaign.json")
    actor = "tali ren"
    original, = app.connections
    assert app.request_passage_release(actor, "passage barrier").authoritative_changed
    assert app.participation_control(actor, "pause").authoritative_changed
    assert app.material("untie", "barrier cord").authoritative_changed
    assert app.material("tie", "barrier board", "barrier crossbar", "barrier cord").authoritative_changed
    replacement, = app.connections
    assert replacement.connection_id != original.connection_id
    before = app.authoritative_digest()
    app = restored(tmp_path)
    assert app.authoritative_digest() == before
    assert app.participation_control(actor, "resume").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.connections == (replacement,)
    blocked = participation.selected(app.participation_state, identity("tali"))
    assert blocked.status == "blocked" and not blocked.contributions
    assert "agreed fastening is gone" in blocked.reason
    assert app.participation_control(actor, "cancel").authoritative_changed
    assert app.request_passage_release(actor, "passage barrier").authoritative_changed
    assert app.wait().authoritative_changed
    assert restored(tmp_path).authoritative_digest() == app.authoritative_digest()
    assert not app.connections and len(receipt_events(app, "tali", "physical_contribution")) == 1


def test_player_release_wins_same_interval_without_npc_credit():
    app = closed_app()
    assert app.request_passage_release("tali ren", "passage barrier").authoritative_changed
    result = app.material("untie", "barrier cord")
    assert result.authoritative_changed
    assert result.logical_time_after == result.logical_time_before + 1
    task = participation.selected(app.participation_state, identity("tali"))
    assert task.status == "externally_satisfied" and not task.contributions
    assert not receipt_events(app, "tali", "physical_contribution")
    assert placement(app.state.representation, identity("barrier-cord")).object_entity_id == app.fixture.player_entity_id
    assert app.move("north").authoritative_changed


def test_nonlocal_request_and_inspection_do_not_disclose_work():
    app = closed_app()
    assert app.move("east").authoritative_changed
    before = app.authoritative_digest()
    result = app.request_passage_release("tali ren", "passage barrier")
    assert result.failure_class == "passage_release_unavailable"
    assert "local communication route" in result.message
    result = app.inspect_passage_work()
    assert result.failure_class == "passage_work_unavailable"
    assert all(name not in result.message for name in ("Tali", "Cord", "north"))
    assert app.authoritative_digest() == before


def test_release_write_failure_preserves_accepted_prefix_and_then_replays(tmp_path, monkeypatch):
    path = tmp_path / "campaign.json"
    app = closed_app(path)
    assert app.request_passage_release("tali ren", "passage barrier").authoritative_changed
    saved = path.read_bytes()
    before = app.authoritative_digest()

    def broken_write():
        raise OSError("injected before acknowledgement")

    monkeypatch.setattr(app, "save", broken_write)
    failure = app.wait()
    assert failure.failure_class == "material_checkpoint_write_failed"
    assert not failure.authoritative_changed and path.read_bytes() == saved
    assert app.authoritative_digest() == before
    app = restored(tmp_path)
    assert app.wait().authoritative_changed
    assert len(receipt_events(app, "tali", "physical_contribution")) == 1
    assert restored(tmp_path).authoritative_digest() == app.authoritative_digest()
