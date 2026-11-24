"""Installed journeys and owner outcomes for grounded terminal intentions."""

import json
import os
from pathlib import Path
import shutil
import subprocess

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_generated_locality import LocalityRecipe, create_generated_locality_fixture
from astra_runtime.myravant_input_context import InputContext
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture


TARROW = ("--locality", "tarrow-actors")
GEN = ("--locality", "generated-worksite", "--generated-case", "access",
       "--generated-seed", "0", "--generated-scale", "1")


def play(root, stem, flags, inputs, *, load=None):
    launcher = shutil.which("myravant-play")
    assert launcher
    checkpoint = load or root / f"{stem}.json"
    trace = root / f"{stem}.jsonl"
    argv = [launcher, *flags, "--load" if load else "--checkpoint", str(checkpoint),
            "--trace", str(trace)]
    stdin = "\n".join((*inputs, "exit", ""))
    result = subprocess.run(argv, input=stdin, capture_output=True, encoding="utf-8", timeout=120)
    assert result.returncode == 0, result.stderr
    data = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    assert data[-1]["evidence_complete"]
    if report := os.getenv("MYRAVANT_INTENTION_REPORT_DIR"):
        target = Path(report) / root.name / (stem + ".json")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"argv": argv, "stdin": stdin, "stdout": result.stdout,
                                      "stderr": result.stderr, "trace": data},
                                     indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return checkpoint, result.stdout, [row for row in data if row["record_type"] == "interaction"]


def no_change(row):
    assert not row["authoritative_changed"] and row["receipt_id"] is None
    assert row["pre_state_digest"] == row["post_state_digest"]


def test_installed_tarrow_two_paraphrases_match_canonical_exactly(tmp_path):
    canonical = (
        "go south", "go west", "inspect sorting board", "ask tali ren about sorting board residue",
        "wait", "ask tali ren for cleaning brush", "go east", "go north",
    )
    plain = (
        "I'll head to the Service Yard.", "Go to the Yard Tool Station.",
        "Let me check the sorting board.", "Did Tali see it dirty?",
        "wait", "I'd like to ask Tali for the cleaning brush.", "Which way back?",
        "I want to return to the common room.",
    )
    alternate = (
        "Make my way to the service yard.", "Head into the tool station.",
        "I'd like to examine the sorting board.", "Ask Tali whether it was sooty when she saw it.",
        "wait", "Please ask Tali for the cleaning brush.", "Go back to Wayhouse Common.",
    )
    first, _, expected = play(tmp_path, "tarrow-canonical", TARROW, canonical)
    for label, inputs in (("tarrow-plain", plain), ("tarrow-alternate", alternate)):
        actual, output, rows = play(tmp_path, label, TARROW, inputs)
        assert "Signs here point to" in output and "You move to the Yard Tool Station." in output
        assert "Tali Ren reports historical witnessed evidence: present." in output
        assert "Give completed." in output and "You move to the Wayhouse Common." in output
        assert actual.read_bytes() == first.read_bytes()
        # All changed-state rows use the same owner receipts, costs and chronology.
        keys = ("receipt_id", "pre_state_digest", "post_state_digest", "logical_time_after", "due_process_ref")
        assert [[row[key] for key in keys] for row in rows if row["authoritative_changed"]] == [
            [row[key] for key in keys] for row in expected if row["authoritative_changed"]]
    app = ActorApplication.restore(fixture=create_actor_fixture(), checkpoint_path=first)
    brush = app.fixture.resolve_object_reference("cleaning brush")
    assert placement(app.state.representation, brush).object_entity_id == app.fixture.player_entity_id
    assert app.runtime_state.logical_time_state.logical_position == 6


def test_generated_interruption_restart_and_improvisation(tmp_path):
    path, output, rows = play(tmp_path, "at-the-barrier", GEN, (
        "Go to Work Annex 1.", "Go back to Covered Yard and check the cloth.",
    ))
    assert "Travel stopped at Workshop." in output and "obstructs that passage" in output
    assert "The rest of that instruction was not attempted." in output
    assert [row["parsed_action"] for row in rows] == ["intent_travel"] * 3
    assert rows[1]["authoritative_changed"] and rows[-1]["failure_class"] == "material_passage_obstructed"
    no_change(rows[-1])
    loaded = lambda: InvestigationApplication.restore(
        fixture=create_generated_locality_fixture(LocalityRecipe("access", scale_level=1)),
        checkpoint_path=path)
    before = loaded()
    assert before.fixture.entity_name(before.current_place_id()) == "Workshop"
    assert len(before.connections) == 1

    _, output, rows = play(tmp_path, "back-through-after-opening", GEN, (
        "I'll untie the cord.", "Go to Covered Yard.",
        "Go back to Workshop and ask Jun if the front panel was dirty when he saw it.",
        "I'd like to grab the brush.", "Clean the front panel.", "Scrub it with what I used earlier.",
        "I want to go into Covered Yard.", "Return to the room where I saw the panel.",
        "Look closely at the front panel.",
    ), load=path)
    assert "Earlier input clarifications have expired." in output
    assert "You untie and recover Cord." in output and "Jun reports historical witnessed evidence: present." in output
    assert "Brush patterns are visible." in output and "Removable residue: 0 unit(s)." in output
    assert loaded().journal[:len(before.journal)] == before.journal
    app = loaded()
    assert not app.connections and app.fixture.entity_name(app.current_place_id()) == "Workshop"
    panel = app.fixture.resolve_object_reference("panel a")
    assert dict(app.water_state.adhered)[panel] == 0
    assert len([row for row in rows if row["parsed_action"] == "intent_report"]) == 1
    assert len([row for row in rows if row["parsed_action"] == "intent_untie" and row["receipt_id"]]) == 1
    assert placement(app.state.representation, app.fixture.resolve_object_reference("cord")).object_entity_id == app.fixture.player_entity_id


def test_corrections_and_stale_references_do_not_commit(tmp_path):
    path, output, rows = play(tmp_path, "clarify", GEN, (
        "Let me check the panel.", "No, the rear one.", "Let me check the other panel.",
        "Let me check the panel.", "Actually, leave it.", "No, the rear one.",
        "Take the panel.", "Go to Entrance.", "No, the rear one.", "Let me check it.",
    ))
    assert "Which object do you mean? Panel A, Panel B." in output
    assert "Panel B\n" in output and "Panel A\n" in output
    assert "The unfinished request is set aside." in output
    assert output.count("There is no current question to answer.") == 2
    assert any(row["failure_class"] == "intent_context_blocked" for row in rows)
    for row in rows:
        if row["parsed_action"] == "intent_cancel" or row["failure_class"] in {
                "intent_clarification", "intent_expired", "intent_context_blocked"}:
            no_change(row)
    _, output, rows = play(tmp_path, "expired-after-restart", GEN, ("No, the rear one.",), load=path)
    assert "Earlier input clarifications have expired." in output
    assert "There is no current question to answer." in output
    no_change(rows[-1])


def test_speech_and_methods_are_not_silently_substituted(tmp_path):
    _, output, rows = play(tmp_path, "constraint-contrasts", GEN, (
        "Look at the front panel.",
        "Could I clean that without using the last of the water?",
        '"Take the brush"', "Please don't take the brush.",
        "If Jun says yes, take the brush.", "Do I take the brush?",
        "Take brush then inspect panel a?",
        "Run back.", "Get to the Entrance without being seen.",
        "Did Jun see it dirty?",
        "Tell Jun that it is clean.",
        "Have him scrub it with the brush.",
        "Have him use the brush instead.",
    ))
    by_input = {row["raw_player_input"].strip(): row for row in rows}
    assert by_input["Run back."]["failure_class"] == "intent_missing_mechanic"
    for key in ("Could I clean that without using the last of the water?",
                "Get to the Entrance without being seen."):
        assert by_input[key]["failure_class"] == "intent_constraint_unavailable"
    for row in rows[1:9]:
        no_change(row)
    assert by_input["Did Jun see it dirty?"]["parsed_action"] == "intent_report"
    assert by_input["Tell Jun that it is clean."]["parsed_action"] == "intent_statement"
    assert "reports historical witnessed evidence: present." in output
    assert "received your statement" in output
    assert "Selected scrub using Brush" in output
    assert "busy" in output


def test_lookup_never_names_hidden_object_or_remote_actor(tmp_path):
    _, output, rows = play(tmp_path, "private-reference", TARROW, (
        "I'd like to pick up the soft iron pin blank.",
        "Did Tali see the sorting board dirty?",
        "Take me to where Tali is.",
    ))
    assert "Soft-Iron Pin Blank" not in output and "Tali Ren" not in output
    for row in rows:
        no_change(row)


def test_an_instrument_answer_selects_actual_custody_and_method(tmp_path):
    _, output, rows = play(tmp_path, "tool-choice", ("--locality", "tarrow-time"), (
        "Head into the Service Yard.", "Go to the tool station.", "Grab the cleaning brush.",
        "Go to the workroom.", "Go to the workroom bench.", "Clean the practice panel.",
        "With the brush.", "Can I clean it without using the last of the water?",
    ))
    assert "Which tool would you like to use?" in output
    assert "Cleaning Cloth for wiping" in output and "Cleaning Brush for scrubbing" in output
    assert "Scrub: Practice Panel to Cleaning Brush." in output
    assert rows[-3]["failure_class"] == "intent_clarification"
    no_change(rows[-3])
    assert rows[-2]["receipt_id"] and rows[-2]["authoritative_changed"]
    assert rows[-1]["failure_class"] == "intent_constraint_unavailable"
    no_change(rows[-1])


def test_equally_short_known_routes_require_a_choice():
    app = ActorApplication.new(fixture=create_actor_fixture())
    context = InputContext(app)
    start = context.here
    context.routes = {(start, "north"): "a", (start, "west"): "b",
                      ("a", "north"): "target", ("b", "east"): "target"}
    assert context.shortest_route("target") == [
        (("north", "a"), ("north", "target")),
        (("west", "b"), ("east", "target")),
    ]
