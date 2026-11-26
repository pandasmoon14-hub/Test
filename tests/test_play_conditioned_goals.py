"""Public journeys over scoped passage and assembly evidence."""

import json
from pathlib import Path

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.domain.persistent_world_actor_evidence import EvidenceEvent, EvidenceState
from astra_runtime.myravant_actor_knowledge import report_source
from astra_runtime.myravant_structures_application import StructuresApplication
from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from astra_runtime.myravant_tarrow_structures import create_structures_fixture
from astra_runtime.myravant_tarrow import identity

from tests.test_play_constrained_goals import effects, outcomes, play, read_only


ACCESS = ("--locality", "tarrow-structures")
ACTIVITIES = ("--locality", "tarrow-activities", "--activity-case", "reference")
WORK = ("--locality", "tarrow-surface-water", "--surface-case", "shared-workbench")
OPEN = ("go south", "go west", "take work panel", "put work panel on yard work trestle",
        "take barrier crossbar", "put barrier crossbar on yard work trestle")
REPORT = "Ask Tali whether the north passage is open."
BLOCK = ("take work cord", "tie work panel to barrier crossbar with work cord")
REMOTE = ("go south", "go west", "go north", "go south", "go west", "go east", "go west", "go west")
BENCH = ("go south", "go west", "go west", "go west", "take repair board",
         "put repair board on workroom bench", "take repair peg", "put repair peg on workroom bench")
FIT = ("take repair cord", "tie repair board to repair peg with repair cord")
CASES = json.loads((Path(__file__).parent / "fixtures/myravant_conditional/expectations.json").read_bytes())
WORDS = {case["id"]: case["intent"] for case in CASES["cases"]}


def test_firsthand_open_matches_owner_inspection_and_move(tmp_path):
    advice, action = WORDS["advice"], WORDS["open-firsthand"]
    path, output, rows = play(tmp_path, "open-access", (*OPEN, advice, action), ACCESS)
    assert "This preview spends no time." in output
    read_only(outcomes(rows, advice))
    assert "You saw that the north passage was open at step 6." in output
    assert "You move to the Yard Sorting Bay." in output
    assert [row["result_type"] for row in outcomes(rows, action)] == ["inspection", "movement_committed"]
    canonical, _, control = play(tmp_path, "open-control", (*OPEN, "inspect barrier board", "go north"), ACCESS)
    assert effects(rows) == effects(control)
    assert path.read_bytes() == canonical.read_bytes()


def test_named_stale_account_reaches_owner_but_firsthand_does_not(tmp_path):
    fresh, stale = WORDS["closed-firsthand"], WORDS["stale-source"]
    conflict, whose = WORDS["disagreement"], "Whose account was that?"
    path, output, rows = play(tmp_path, "blocked-access", (*OPEN, REPORT, *BLOCK, fresh, stale, whose, conflict), ACCESS)
    assert "Tali Ren reported that the north passage was open at step 6." in output
    assert "You saw that the north passage was closed at step 8." in output
    assert "These accounts differ" in output
    assert "No consequent was attempted" in output
    for rejected in (fresh, conflict):
        observation, stopped = outcomes(rows, rejected)
        assert observation["result_type"] == "inspection" and stopped["failure_class"] == "condition_stopped"
        read_only([stopped])
    attempt = outcomes(rows, stale)
    assert attempt[-1]["failure_class"] == "material_passage_obstructed"
    read_only(attempt)
    assert "Crossing is still pending" in outcomes(rows, whose)[0]["player_visible_output"]
    read_only(outcomes(rows, whose))
    app = StructuresApplication.restore(fixture=create_structures_fixture(), checkpoint_path=path)
    reports = [e for e in app.evidence_state.events if e.kind == "reported"
               and e.qualification.startswith("qualified-local-delivery-at:")]
    assert len(reports) == 2
    by_id = {e.event_id: e for e in app.evidence_state.events}
    assert all(by_id[e.source_event_id].actor_id == identity("tali") for e in reports)
    assert {e.origin_tick for e in reports} == {6}
    assert len({by_id[e.source_event_id].receipt_id for e in reports}) == 1
    assert app.current_place_id() == identity("yard-tools")
    _, resumed, after = play(tmp_path, "access-resume", (
        "Whose account was that?", stale, "untie work cord", fresh,
    ), ACCESS, load=path)
    assert "no retained account in this conversation" in resumed
    read_only(outcomes(after, stale))
    assert outcomes(after, stale)[-1]["failure_class"] == "material_passage_obstructed"
    assert len([row for row in after if row["result_type"] == "movement_committed"]) == 1
    assert "Yard Sorting Bay" in resumed


def test_no_witness_is_unknown_and_travel_for_an_observation_costs_time(tmp_path):
    unknown = WORDS["no-witness"]
    visit = "Check from Yard Tool Station."
    _, output, rows = play(tmp_path, "unknown-witness", (*REMOTE, unknown, visit), ACTIVITIES)
    asked, = outcomes(rows, unknown)
    assert asked["failure_class"] == "actor_report_evidence_unavailable"
    read_only([asked])
    assert "condition is still unknown" in output
    steps = outcomes(rows, visit)
    assert [row["result_type"] for row in steps] == ["movement_committed", "movement_committed", "inspection"]
    assert steps[1]["logical_time_after"] == steps[0]["logical_time_before"] + 2
    assert "You saw that the north passage was open" in steps[-1]["player_visible_output"]


def test_cancelled_dialogue_leaves_agreement_and_external_fit_keeps_attribution(tmp_path):
    request = WORDS["request-and-external-work"]
    path, output, rows = play(tmp_path, "accept", (*BENCH, request, request, "Cancel that"), WORK)
    assert "Acceptance reserves no materials." in output
    assert "busy with selected work" in output
    assert output.count("Acceptance reserves no materials.") == 1
    decisions = [row for row in outcomes(rows, request) if row["result_type"] == "actor_participation"]
    assert len(decisions) == 1 and decisions[0]["authoritative_changed"]
    fixture = create_surface_fixture(shared_workbench=True)
    before = SurfaceWaterApplication.restore(fixture=fixture, checkpoint_path=path)
    task, = before.participation_state.records
    assert task.actor_id == identity("oren") and task.status == "active" and not task.contributions
    assert not before.connections
    strip = placement(before.state.representation, identity("strip"))
    _, output, after = play(tmp_path, "external-fitting", (
        "Do it", *FIT, "ask oren kesh about work", "Ask Tali whether the workshop assembly is fitted.",
    ), WORK, load=path)
    assert "There is no open goal" in output
    assert "0 own committed step(s)" in output
    assert "Tali Ren reported that the workshop assembly was fitted" in output
    final = SurfaceWaterApplication.restore(fixture=fixture, checkpoint_path=path)
    task, = final.participation_state.records
    assert task.status == "externally_satisfied" and not task.contributions
    assert len(final.connections) == 1
    assert placement(final.state.representation, identity("strip")) == strip
    assert placement(final.state.representation, identity("repair-cord")).relation_type == "reserved_by"
    assert not any(row["result_type"] == "movement_committed" for row in after)


def test_worker_executes_on_later_intervals_and_protected_part_stays(tmp_path):
    request = WORDS["request-and-external-work"]
    path, output, rows = play(tmp_path, "owner-finishes", (
        *BENCH, request, "wait 2 steps", "Ask Tali whether the workshop assembly is fitted.",
    ), WORK)
    assert "0 own committed step(s)" in output
    assert "Tali Ren reported that the workshop assembly was fitted" in output
    fixture = create_surface_fixture(shared_workbench=True)
    restored = SurfaceWaterApplication.restore(fixture=fixture, checkpoint_path=path)
    task, = restored.participation_state.records
    assert task.status == "completed" and len(task.contributions) == 2
    assert placement(restored.state.representation, identity("strip")).object_entity_id == identity("work-bench")
    control, _, rows_control = play(tmp_path, "owner-control", (
        *BENCH, "inspect repair board", "ask oren kesh to assemble workshop assembly", "wait 2 steps",
        "Ask Tali whether the workshop assembly is fitted.",
    ), WORK)
    assert effects(rows) == effects(rows_control)
    assert path.read_bytes() == control.read_bytes()


def test_work_guard_and_prohibition_never_issue_agreement(tmp_path):
    protected = WORDS["protect-participant"]
    no_ask = "Ask Oren to assemble the workshop assembly if it still needs work. Do not ask anyone."
    _, output, rows = play(tmp_path, "protected", (*BENCH, protected, no_ask), WORK)
    assert "can't guarantee that placement" in output
    assert "prohibition on asking prevents the work request" in output
    assert not any(row["result_type"] == "actor_participation" for row in (*outcomes(rows, protected), *outcomes(rows, no_ask)))


def test_multi_blocker_open_requires_coherent_complete_evidence():
    from types import SimpleNamespace
    from astra_runtime.myravant_condition_methods import _account

    def record(receipt, value):
        return SimpleNamespace(receipt_id=receipt, kind="witnessed", value=("barrier", value), tick=4, origin_tick=None)

    assert _account((), 2) is None
    assert _account((record("a", "separate"), record("b", "separate")), 2) is None
    assert _account((record("a", "separate"), record("a", "separate")), 2).state == "separate"
    assert _account((record("a", "joined"),), 2).state == "joined"


def test_scoped_report_requires_same_receipt_from_same_observer():
    assembly = EvidenceEvent("obs", "witness", "witnessed", "witness", "workpiece", "assembly",
                             ("partition", "separate"), 3, "remote", "qualified")
    anchor = EvidenceEvent("anchor", "witness", "witnessed", "witness", "support", "placement",
                           ("located_at", "claimed-place"), 4, "local", "qualified")
    events = EvidenceState((assembly, anchor))
    assert report_source(events, "witness", "workpiece", "assembly", kind="witnessed") == assembly
    assert report_source(events, "witness", "workpiece", "assembly", kind="witnessed",
                         scope=("partition", "support", "claimed-place")) is None
