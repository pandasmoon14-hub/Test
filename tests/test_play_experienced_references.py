"""Installed routes, observation boundaries, and durable references."""

import json
import os
from pathlib import Path
import shutil
import subprocess

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_activity_application import ActivityApplication
from astra_runtime.myravant_tarrow_activity import create_activity_fixture
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


BRUSH = ("--locality", "tarrow-activities", "--activity-case", "reference")
GENERATED = ("--locality", "generated-worksite", "--generated-case", "access",
             "--generated-seed", "0", "--generated-scale", "1")
BRUSH_SETUP = ("go south", "go west", "go west", "go west", "look",
               "Ask Oren Kesh to undertake bench upkeep", "go east", "go east",
               "wait 5 steps", "wait 5 steps")
KEEPER_SETUP = ("take lantern", "go south", "wait", "give lantern to groundskeeper",
                "ask groundskeeper for lantern", "go north")


def play(root, label, flags, commands, *, load=None):
    launcher = shutil.which("myravant-play")
    assert launcher
    checkpoint = load or root / f"{label}.json"
    trace = root / f"{label}.jsonl"
    argv = [launcher, *flags, "--load" if load else "--checkpoint", str(checkpoint), "--trace", str(trace)]
    stdin = "\n".join((*commands, "exit", ""))
    result = subprocess.run(argv, input=stdin, capture_output=True, encoding="utf-8", timeout=120)
    assert result.returncode == 0, result.stderr
    data = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    assert data[-1]["evidence_complete"]
    if report := os.getenv("MYRAVANT_REFERENCE_REPORT_DIR"):
        export = Path(report) / root.name
        export.mkdir(parents=True, exist_ok=True)
        (export / f"{label}.json").write_text(json.dumps({
            "argv": argv, "stdin": stdin, "stdout": result.stdout, "trace": data,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return checkpoint, [row for row in data if row["record_type"] == "interaction"]


def outcome(rows, raw):
    return [row for row in rows if row["raw_player_input"].strip() == raw]


def output(rows, raw):
    return "".join(row["player_visible_output"] for row in outcome(rows, raw))


def read_only(row):
    assert not row["authoritative_changed"]
    assert row["receipt_id"] is None
    assert row["pre_state_digest"] == row["post_state_digest"]
    assert row["logical_time_before"] == row["logical_time_after"]


def test_brush_moves_in_absence_and_history_survives_restart(tmp_path):
    path, _ = play(tmp_path, "brush-departure", BRUSH, BRUSH_SETUP)
    fixture = create_activity_fixture(activity_case="reference")
    app = ActivityApplication.restore(fixture=fixture, checkpoint_path=path)
    brush = fixture.resolve_object_reference("cleaning brush")
    shelf = next(p.entity_id for p in fixture.place_presentations if p.name == "Workroom Shelf")
    bench = next(p.entity_id for p in fixture.place_presentations if p.name == "Workroom Bench")
    player = fixture.player_entity_id
    assert placement(app.state.representation, brush).object_entity_id == shelf
    assert app.activity_records[0].status == "completed"
    assert [x[0] for x in app.activity_records[0].stages_finished] == [0, 1, 2]
    assert all(event.value != ("located_at", shelf) for event in app.evidence_state.events
               if event.actor_id == player and event.target_id == brush and event.facet == "placement")
    now = "Where is the brush now?"
    last = "Was the brush there last time?"
    go = "Take me back to where I saw the brush"
    heard = "Ask Tali whether she heard about the brush"
    saw = "Ask Tali whether she saw the brush"
    fetch = "Go get it"
    commands = (now, last, fetch, go, "look", heard, saw, now, fetch,
                "Take me to Workroom Shelf", "look", fetch)
    _, rows = play(tmp_path, "brush-return", BRUSH, commands, load=path)
    current, later = outcome(rows, now)
    assert "at step 5 (11 steps ago)" in current["player_visible_output"]
    assert "You don't know its current location." in current["player_visible_output"]
    assert "You saw Cleaning Brush at Workroom Bench" in output(rows, last)
    assert "current location" not in output(rows, last)
    assert "Workroom Shelf" not in later["player_visible_output"]
    assert "Tali Ren reported Cleaning Brush at Workroom Bench as of step 5" in later["player_visible_output"]
    assert "No retained reported evidence" in output(rows, heard)
    assert "Tali Ren reports historical witnessed evidence" in output(rows, saw)
    for row in (current, later, *outcome(rows, last), *outcome(rows, heard), *outcome(rows, fetch)[:2]):
        read_only(row)
    assert all("don't know where" in row["player_visible_output"] for row in outcome(rows, fetch)[:2])
    moves = outcome(rows, go)
    assert len(moves) == 2 and all(row["receipt_id"] for row in moves)
    assert "You move to the Workshop Workroom." in moves[0]["player_visible_output"]
    assert "You move to the Workroom Bench." in moves[1]["player_visible_output"]
    assert "You pick up the Cleaning Brush." in outcome(rows, fetch)[-1]["player_visible_output"]

    final = ActivityApplication.restore(fixture=fixture, checkpoint_path=path)
    assert placement(final.state.representation, brush).object_entity_id == player
    assert final.runtime_state.logical_time_state.logical_position == 20
    assert final.journal[:len(app.journal)] == app.journal
    reports = [e for e in final.evidence_state.events
               if (e.actor_id, e.kind, e.target_id) == (player, "reported", brush)]
    assert len(reports) == 1
    report = reports[0]
    original = next(e for e in final.evidence_state.events if e.event_id == report.source_event_id)
    assert (original.actor_id, original.kind, original.value, original.tick) == (
        report.source_actor_id, "witnessed", ("located_at", bench), report.origin_tick)
    assert report.tick == 18

    repeated, _ = play(tmp_path, "brush-repeat-departure", BRUSH, BRUSH_SETUP)
    play(tmp_path, "brush-repeat-return", BRUSH, commands, load=repeated)
    assert repeated.read_bytes() == path.read_bytes()


def test_handoff_is_directional_and_live_recipient_is_required(tmp_path):
    path, _ = play(tmp_path, "lantern-departure", (), KEEPER_SETUP)
    received = "Take this back to the person who gave it to me"
    sent = "Take this back to the person I gave it to"
    lent = "Take this back to the person who lent it to me"
    borrowed = "Take this back to the person who borrowed it from me"
    travel = "Take me back to where they gave it to me"
    _, rows = play(tmp_path, "lantern-return", (), (lent, borrowed, received, travel, sent), load=path)
    assert "no evidence here of a loan" in output(rows, lent)
    assert "no evidence here of a loan" in output(rows, borrowed)
    assert "last matching exchange with Groundskeeper was at Yard" in output(rows, received)
    assert "can't reach that person here" in output(rows, received)
    for row in rows[:3]:
        read_only(row)
    assert "You move to the Yard." in output(rows, travel)
    assert "You hand the Brass Lantern to the Groundskeeper." in output(rows, sent)
    app = MyravantVSM14Application.restore(checkpoint_path=path)
    receipts = [t.receipt for t in app.handoff_state.committed_actor_object_handoff_transitions]
    assert len(receipts) == 3
    first, middle, last = receipts
    assert last.receipt_id == rows[-1]["receipt_id"]
    assert first.source_actor_entity_id == last.source_actor_entity_id == middle.recipient_actor_entity_id
    assert first.recipient_actor_entity_id == last.recipient_actor_entity_id == middle.source_actor_entity_id
    assert first.object_entity_id == middle.object_entity_id == last.object_entity_id
    assert placement(app.state.representation, last.object_entity_id).object_entity_id == last.recipient_actor_entity_id


def test_later_target_clarification_never_repeats_travel(tmp_path):
    late = "Head back to the workroom and examine the panel by the entrance"
    reply = "the rear panel, please"
    path, rows = play(tmp_path, "late-inspection", GENERATED, (
        reply, "go west", late, reply, "Look at the other one",
        "I would like to look at the rear panel, please.",
        "go west", "Walk back to the Workshop and examine the front panel",
        "Let me look at the panel", "Actually look at the brush", reply,
        "Let me look at the panel",
    ))
    assert "Panel B" not in rows[0]["player_visible_output"]
    move, blocked = outcome(rows, late)
    assert move["receipt_id"] and "You move to the Workshop" in move["player_visible_output"]
    assert "I can't verify that position from here." in blocked["player_visible_output"]
    read_only(blocked)
    first, answer, after = outcome(rows, reply)
    read_only(first)
    assert "Panel B" in answer["player_visible_output"]
    assert "You move" not in answer["player_visible_output"]
    assert "Panel A" in output(rows, "Look at the other one")
    corrected = output(rows, "Actually look at the brush")
    assert "Brush" in corrected
    assert "Panel B" not in after["player_visible_output"]
    assert len(outcome(rows, "Walk back to the Workshop and examine the front panel")) == 2
    _, rows = play(tmp_path, "expired-question", GENERATED, (reply,), load=path)
    assert "Panel B" not in rows[0]["player_visible_output"]
    read_only(rows[0])


def test_recalled_tool_uses_player_performance_receipt(tmp_path):
    start = "I'd like to brush the front panel with this tool."
    path, rows = play(tmp_path, "brush-used", GENERATED, ("take brush", start))
    assert "Scrub: Panel A to Brush." in output(rows, start)
    repeat = "Scrub the rear panel with the tool I used earlier"
    _, rows = play(tmp_path, "brush-recalled", GENERATED, (repeat,), load=path)
    assert "Scrub: Panel B to Brush." in output(rows, repeat)
    assert rows[-1]["receipt_id"] and rows[-1]["logical_time_after"] == rows[-1]["logical_time_before"] + 1


def test_exchange_projections_preserve_direction_and_audience():
    from types import SimpleNamespace
    from astra_runtime.myravant_experienced_references import ExperiencedReferences

    def transfer(source, recipient, obj, place):
        return SimpleNamespace(receipt=SimpleNamespace(
            source_actor_entity_id=source, recipient_actor_entity_id=recipient,
            object_entity_id=obj, place_id=place))

    app = SimpleNamespace(fixture=SimpleNamespace(player_entity_id="player"),
                          handoff_state=SimpleNamespace(committed_actor_object_handoff_transitions=(
                              transfer("maker", "player", "spade", "shed"),
                              transfer("player", "porter", "spade", "yard"),
                              transfer("porter", "maker", "spade", "loft"),
                          )))
    history = ExperiencedReferences(app)
    assert tuple(history.exchanges("received")) == (("spade", "maker", "shed"),)
    assert tuple(history.exchanges("gave")) == (("spade", "porter", "yard"),)
