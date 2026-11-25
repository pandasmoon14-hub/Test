"""Installed outcome requests over custody and water owners."""

import json
import os
from pathlib import Path
import shutil
import subprocess

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_timed_application import TimedApplication
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


GIVE = ("take lantern", "go south", "wait", "give lantern to groundskeeper")
LOCAL = (*GIVE, "ask groundskeeper for lantern")
AWAY = (*LOCAL, "wait", "wait", "wait", "go north")
OPEN_STORED = ("take lantern", "go south", "open chest", "store lantern in chest")
TIMED = ("--locality", "tarrow-time")
GEN = ("--locality", "generated-worksite", "--generated-case", "access",
       "--generated-seed", "0", "--generated-scale", "1")
DRY_BOTH = ("go south", "go west", "take cleaning brush", "go west", "go west", "take cleaning cloth")
DRY_CLOTH = ("go south", "go west", "go west", "go west", "take cleaning cloth")
WET = "soak cleaning cloth from wash bucket"
SCRUB = "scrub practice panel with cleaning brush"
WIPE = "wipe practice panel with cleaning cloth"
BASIN = (*DRY_CLOTH, "take wash bucket", "pour 1 unit from wash bucket into rinse basin",
         "go east", "drop wash bucket", "go west")
RETURN = "Return the lantern to its giver."


def play(root, stem, commands, flags=(), *, load=None):
    launcher = shutil.which("myravant-play")
    assert launcher
    path = load or root / f"{stem}.json"
    trace = root / f"{stem}.jsonl"
    argv = [launcher, *flags, "--load" if load else "--checkpoint", str(path), "--trace", str(trace)]
    result = subprocess.run(argv, input="\n".join((*commands, "exit", "")), capture_output=True,
                            encoding="utf-8", timeout=120)
    assert result.returncode == 0, (result.stderr, result.stdout)
    data = [json.loads(line) for line in trace.read_text().splitlines()]
    assert data[-1]["evidence_complete"]
    if root_dir := os.getenv("MYRAVANT_GOAL_REPORT_DIR"):
        export = Path(root_dir) / root.name
        export.mkdir(parents=True, exist_ok=True)
        (export / f"{stem}.json").write_text(json.dumps({
            "argv": argv, "input": commands, "stdout": result.stdout, "trace": data,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path, result.stdout, [row for row in data if row["record_type"] == "interaction"]


def outcomes(rows, text):
    return [row for row in rows if row["raw_player_input"].strip() == text]


def effects(rows):
    keys = ("receipt_id", "logical_time_before", "logical_time_after", "post_state_digest")
    return [tuple(row[key] for key in keys) for row in rows if row["authoritative_changed"]]


def read_only(rows):
    assert rows
    for row in rows:
        assert row["pre_state_digest"] == row["post_state_digest"]
        assert row["logical_time_before"] == row["logical_time_after"]
        assert not row["authoritative_changed"] and not row["receipt_id"]


def test_feasibility_is_read_only_then_return_has_exact_owner_custody(tmp_path):
    inquiry = "Can I get this back to the person who gave it to me?"
    attempt = "Take it back to them."
    path, output, rows = play(tmp_path, "natural-return", (*LOCAL, inquiry, attempt, attempt))
    assert "hand it to Groundskeeper here" in output
    assert output.count("You hand the Brass Lantern to the Groundskeeper.") == 2
    read_only(outcomes(rows, inquiry))
    expected, _, control = play(tmp_path, "concise-return", (*LOCAL, "give lantern to groundskeeper"))
    assert effects(rows) == effects(control)
    assert path.read_bytes() == expected.read_bytes()


def test_travel_interrupts_and_restart_finishes_only_remaining_handoff(tmp_path):
    inquiry = "Can I get this back to the person who gave it to me?"
    check = "Start at the last exchange."
    explain = "Why did we stop?"
    first, output, rows = play(tmp_path, "seek-exchange", (*AWAY, inquiry, "Take it back to them.", check, explain))
    assert "Finding the recipient is uncertain." in output and "Gatehouse" not in output
    assert "1 plan step(s) committed" in output and "still have Brass Lantern" in output
    actual = outcomes(rows, check)
    assert len(actual) == 2 and actual[0]["receipt_id"]
    read_only(actual[1:])
    read_only(outcomes(rows, explain))
    restored = MyravantVSM14Application.restore(checkpoint_path=first)
    assert restored.fixture.entity_name(restored.current_place_id()) == "Yard"

    finished, output, after = play(tmp_path, "finish-exchange", ("Do it.", "wait", RETURN, RETURN), load=first)
    assert "Restate an unfinished goal" in output and "There is no open goal." in output
    assert output.count("You hand the Brass Lantern to the Groundskeeper.") == 1
    assert "You move" not in output
    canonical, _, control = play(tmp_path, "concise-exchange",
                                 (*AWAY, "go south", "wait", "give lantern to groundskeeper"))
    assert effects((*rows, *after)) == effects(control)
    assert finished.read_bytes() == canonical.read_bytes()
    app = MyravantVSM14Application.restore(checkpoint_path=finished)
    receipts = app.handoff_state.committed_actor_object_handoff_transitions
    assert len(receipts) == 3
    receipt = receipts[-1].receipt
    assert placement(app.state.representation, receipt.object_entity_id).object_entity_id == receipt.recipient_actor_entity_id


def test_recovery_dispatches_retrieval_or_voluntary_request(tmp_path):
    restricted = "Can I recover the lantern without asking anyone?"
    for prefix, command, canonical, expected in (
        (OPEN_STORED, "Use your judgment.", "retrieve lantern from chest", "You retrieve"),
        (GIVE, "Ask the holder.", "ask groundskeeper for lantern", "hands you the Brass Lantern"),
    ):
        concern = () if prefix == OPEN_STORED else ("Do it.", "Clear the limits.")
        label = "store" if prefix == OPEN_STORED else "holder"
        path, output, rows = play(tmp_path, label, (*prefix, restricted, *concern, command))
        if concern:
            assert "prohibition on asking" in output and "if they agree" in output
            read_only(outcomes(rows, "Do it."))
        assert expected in output
        target, _, control = play(tmp_path, label + "-control", (*prefix, canonical))
        assert effects(rows) == effects(control)
        assert path.read_bytes() == target.read_bytes()


def test_closed_container_and_unsupported_constraint_stay_read_only(tmp_path):
    _, output, rows = play(tmp_path, "closed-and-cancelled", (
        *OPEN_STORED, "close chest", "Could I recover the lantern?", "Do it.",
        "open chest", "Recover the lantern without anyone finding out.", "Do it.", "Cancel that.",
        "Do it.",
    ))
    assert "location is currently unconfirmed" in output
    assert "can't enforce" in output and "set aside" in output and "There is no open goal." in output
    assert "You retrieve" not in output
    read_only(outcomes(rows, "Could I recover the lantern?"))
    read_only(outcomes(rows, "Do it."))


def test_wet_choice_partial_work_and_explicit_revision_preserve_actual_stock(tmp_path):
    question = "Could I clean the practice panel without drawing more water?"
    path, output, rows = play(tmp_path, "wipe-then-scrub", (
        *DRY_BOTH, WET, question, "Do that.", "Use the cloth.", "Why did we stop?",
        "Use the brush instead.",
    ), TIMED)
    assert "Choose a method" in output and "up to 2 of 3 residue" in output and "up to 3 of 3" in output
    assert "has no free residue capacity" in output
    read_only(outcomes(rows, question))
    read_only(outcomes(rows, "Do that."))
    assert "Goal complete. Practice Panel has no removable residue." in output
    controlled, _, control = play(tmp_path, "wet-control", (*DRY_BOTH, WET, WIPE, WIPE, SCRUB), TIMED)
    assert effects(rows) == effects(control)
    assert path.read_bytes() == controlled.read_bytes()
    app = TimedApplication.restore(checkpoint_path=path)
    bucket = app.fixture.resolve_object_reference("wash bucket")
    panel = app.fixture.resolve_object_reference("practice panel")
    assert dict(app.water_state.water)[bucket] == 11
    assert dict(app.water_state.adhered)[panel] == 0


def test_basin_stop_and_reserve_prevent_draw_then_explicit_revision_allows_it(tmp_path):
    question = "Could I get the practice panel clean and leave at least 1 unit in the basin?"
    stop = "Go ahead, but stop if you need the basin."
    path, output, rows = play(tmp_path, "hold-basin", (*BASIN, question, "Do it.", stop, "Clear the limits.", stop), TIMED)
    assert "reserve of 1 unit(s)" in output
    assert "Stop before using Rinse Basin" in output
    read_only(outcomes(rows, question))
    read_only(outcomes(rows, "Do it."))
    read_only(outcomes(rows, stop))
    app = TimedApplication.restore(checkpoint_path=path)
    basin = app.fixture.resolve_object_reference("rinse basin")
    assert dict(app.water_state.water)[basin] == 1
    _, output, tail = play(tmp_path, "draw-basin", (
        "Do it.", "Could I get the practice panel clean?", "Use your judgment.",
    ), TIMED, load=path)
    assert "draw one unit from Rinse Basin" in output
    assert "Soak: Rinse Basin to Cleaning Cloth." in output
    assert "has no free residue capacity" in output
    assert len(effects(tail)) == 3


def test_unmatched_answer_keeps_only_pending_clause_across_next_reply(tmp_path):
    request = "Head for Workshop and examine the panel by the door."
    bad, good = "The back one, please.", "The rear panel, please."
    path, output, rows = play(tmp_path, "door-panel", ("go west", request, bad, good), GEN)
    assert "The earlier question is still open." in output
    assert "Panel B" in outcomes(rows, good)[0]["player_visible_output"]
    assert output.count("You move to the Workshop.") == 1
    read_only(outcomes(rows, bad))
    _, output, after = play(tmp_path, "door-resume", (good,), GEN, load=path)
    assert "Panel B" not in outcomes(after, good)[0]["player_visible_output"]
    read_only(outcomes(after, good))


def test_partial_cleaning_survives_restart_without_duplicate_strokes(tmp_path):
    goal = "Get the practice panel clean without drawing more water."
    partial, output, before = play(tmp_path, "clean-partial", (*DRY_BOTH, WET, goal, "Use the cloth."), TIMED)
    assert output.count("Wipe: Practice Panel to Cleaning Cloth.") == 2
    assert "still has 1 removable residue" in output
    finished, output, after = play(tmp_path, "clean-resumed", ("Continue the plan.", goal), TIMED, load=partial)
    assert "There is no open goal" in output
    assert output.count("Scrub: Practice Panel to Cleaning Brush.") == 1
    assert "Wipe: Practice Panel" not in output
    expected, _, control = play(tmp_path, "clean-concise", (*DRY_BOTH, WET, WIPE, WIPE, SCRUB), TIMED)
    assert effects((*before, *after)) == effects(control)
    assert finished.read_bytes() == expected.read_bytes()


def test_return_pronoun_requires_a_grounded_recipient(tmp_path):
    attempt = "Take it back to them."
    _, output, rows = play(tmp_path, "ungrounded-recipient", (*LOCAL, attempt))
    assert "can't identify who 'them' refers to" in output
    assert output.count("You hand the Brass Lantern to the Groundskeeper.") == 1
    read_only(outcomes(rows, attempt))
