"""Public installed journeys and owner checks for situated generated worksites."""

from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_generated_locality import (
    LocalityRecipe, build_generated_locality, create_generated_locality_fixture,
)


STAGE = (
    "take plate", "put plate on bench", "take peg", "put peg on bench",
    "take cord", "tie plate to peg using cord",
)
FIRST = (
    "wait", "wait", "wait", "go east", "inspect worksite", "inspect panel b",
    "ask jun about panel b activity", *STAGE, "go north", "inspect passage work",
    "ask jun to release joining frame", "ask jun to pause work",
    "untie cord", "drop cord", "ask jun about plate assembly",
)
SECOND = (
    "take cord", "tie plate to peg using cord", "compare reports about plate assembly",
    "ask jun to resume work", "wait", "ask jun about work",
    "ask jun to cancel work", "inspect passage work", "ask jun to release joining frame",
)
THIRD = (
    "wait", "ask jun about plate activity", "ask jun about work",
    "ask jun to clean panel a using cloth by wiping", "take cloth",
    "ask jun about work", "ask jun about cloth moisture", "ask jun to cancel work",
    "go north", "ask jun about cloth moisture", "ask jun about ways to clean panel a",
    "wait", "wait", "inspect cloth", "go south", "ask jun about cloth moisture",
    "drop cloth", "ask jun about cloth moisture", "ask jun to clean panel a using cloth by wiping",
    "ask jun about ways to clean panel a",
    "ask jun to clean panel a using detail scrubber by scrubbing",
)
FOURTH = (
    "wait", "wait", "wait", "ask jun about panel a activity",
    "inspect panel a", "look", "go west", "wait", "go east", "inspect panel a",
)


def play(root, name, recipe, commands=(), *, load=False, expected=0):
    launcher = shutil.which("myravant-play")
    assert launcher, "install myravant-play first"
    root.mkdir(exist_ok=True)
    path, trace = root / "campaign.json", root / (name + ".jsonl")
    before = path.read_bytes() if path.exists() else None
    argv = [launcher, "--locality", "generated-worksite", "--generated-case", recipe.case,
            "--generated-seed", str(recipe.seed), "--generated-scale", str(recipe.scale_level),
            "--load" if load else "--checkpoint", str(path), "--trace", str(trace)]
    stdin = (*commands, "exit", "")
    result = subprocess.run(argv, input="\n".join(stdin), capture_output=True,
                            encoding="utf-8", timeout=120)
    assert result.returncode == expected, (result.stdout, result.stderr)
    after = path.read_bytes() if path.exists() else None
    records = [json.loads(row) for row in trace.read_text(encoding="utf-8").splitlines()] if trace.exists() else []
    if expected:
        assert before == after and not records
    else:
        assert records[-1]["evidence_complete"]
    if report := os.getenv("MYRAVANT_SITUATED_REPORT_DIR"):
        target = Path(report) / root.parent.name / root.name / (name + ".json")
        target.parent.mkdir(parents=True, exist_ok=True)
        data = {"argv": argv, "stdin": stdin, "stdout": result.stdout,
                "stderr": result.stderr, "exit_status": result.returncode,
                "trace": records,
                "checkpoint_before": sha256(before).hexdigest() if before else None,
                "checkpoint_after": sha256(after).hexdigest() if after else None}
        target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return result.stdout, [row for row in records if row["record_type"] == "interaction"]


def restore(root, recipe):
    return recipe.application_type.restore(fixture=create_generated_locality_fixture(recipe),
                                           checkpoint_path=root / "campaign.json")


def refusal(row, kind):
    assert row["failure_class"] == kind
    assert not row["authoritative_changed"] and row["receipt_id"] is None
    assert row["pre_state_digest"] == row["post_state_digest"]


def custody(app, reference, relation, holder):
    item = app.fixture.resolve_object_reference(reference)
    actual = placement(app.state.representation, item)
    assert (actual.relation_type, actual.object_entity_id) == (relation, holder)


def residue(app, name):
    return dict(app.water_state.adhered)[app.fixture.resolve_object_reference(name)]


def test_installed_drying_difference_and_return(tmp_path):
    entry = ("go east", "look", "inspect worksite", "take cloth",
             "inspect cloth", "wipe panel a using cloth")
    work = ("take brush", "scrub panel a using brush", "inspect panel a",
            "go west", "wait", "go east", "inspect panel a")
    fast, slow = LocalityRecipe("drying", 0), LocalityRecipe("drying", 1)

    for recipe in (fast, slow):
        root = tmp_path / f"drying-{recipe.seed}"
        stdout, rows = play(root, "same-approach", recipe, entry)
        assert "Inspect worksite to check local methods." in stdout
        assert "Soak Cloth from Basin" in stdout and "Scrub Panel A using Brush" in stdout
        assert not restore(root, recipe).fixture.actor_order
        if recipe == fast:
            assert "wiping requires retained water" in stdout
            refusal(rows[-1], "water_opportunity_unavailable")
            assert "Condition: dry." in stdout and "A drying trace is visible." in stdout
        else:
            assert "Water: 1/2 unit(s)." in stdout and "Wipe: Panel A to Cloth." in stdout
            assert rows[-1]["authoritative_changed"]
        returned, _ = play(root, "different-method-and-return", recipe, work, load=True)
        assert "Scrub: Panel A to Brush." in returned
        remaining = 1 if recipe == fast else 0
        assert returned.count(f"Removable residue: {remaining} unit(s).") == 2
        app = restore(root, recipe)
        assert residue(app, "panel a") == remaining
        assert residue(app, "panel a") + residue(app, "brush") + residue(app, "cloth") == 3

    full = tmp_path / "uninterrupted"
    play(full, "same-actions-with-look", fast, (*entry, "look", *work))
    assert (full / "campaign.json").read_bytes() == (tmp_path / "drying-0" / "campaign.json").read_bytes()
    recovered, _ = play(tmp_path / "rinse", "re-wet", fast, (*entry, "soak cloth from basin",
                        "wipe panel a using cloth", "inspect basin", "inspect panel a"))
    assert "Soak: Basin to Cloth. Transferred 1 water unit(s)." in recovered
    assert "Water: 2/3 unit(s)." in recovered
    assert "Removable residue: 2 unit(s)." in recovered


def test_installed_worksite_stale_report_and_two_fresh_agreements(tmp_path):
    recipe = LocalityRecipe("coordination")
    split = tmp_path / "restart"
    stdout, rows = play(split, "receive", recipe, FIRST)
    assert "Jun reports historical performed evidence: scrub." in stdout
    assert "Jun reports historical witnessed evidence: joining frame, separate." in stdout
    refusal(next(row for row in rows if row["raw_player_input"].strip() == "go north"),
            "material_passage_obstructed")
    reported = restore(split, recipe)
    player, worker = reported.fixture.player_entity_id, reported.fixture.actor_order[0]
    standing, old = reported.participation_state.records
    assert standing.source_actor_id == worker and standing.status == "completed"
    assert len(standing.contributions) == 3 and residue(reported, "panel b") == 0
    assert old.source_actor_id == player and old.status == "paused" and not old.contributions
    custody(reported, "brush", "carried_by", worker)
    assert not reported.connections
    events = {event.event_id: event for event in reported.evidence_state.events}
    statement, = [event for event in events.values()
                  if event.actor_id == player and event.kind == "reported" and event.facet == "assembly"]
    witnessed = events[statement.source_event_id]
    assert witnessed.actor_id == statement.source_actor_id == worker
    assert witnessed.kind == "witnessed" and witnessed.value == statement.value
    assert witnessed.tick == statement.origin_tick <= statement.tick

    stdout, _ = play(split, "stale-then-new", recipe, SECOND, load=True)
    assert any("received statement from Jun" in line and "joining frame, separate" in line
               for line in stdout.splitlines())
    assert any("own admitted observation" in line and "joining frame, joined" in line
               for line in stdout.splitlines())
    assert "The agreed fastening is gone." in stdout
    agreed = restore(split, recipe)
    assert agreed.journal[:len(reported.journal)] == reported.journal
    assert agreed.participation_state.records[0] == standing
    old_agreement, release = agreed.participation_state.records[1:]
    assert old_agreement.task_id == old.task_id and old_agreement.status == "withdrawn"
    assert not old_agreement.contributions
    assert release.status == "active" and not release.contributions
    assert agreed._release_connection(old_agreement) != agreed._release_connection(release)
    assert agreed._release_connection(release) == agreed.connections[0].connection_id

    stdout, rows = play(split, "lost-resource-and-revised-agreement", recipe, THIRD, load=True)
    assert "Jun reports historical performed evidence: untie." in stdout
    assert "The pickup target is not accessible." in stdout
    assert stdout.count("historical witnessed evidence: wet.") == 2
    assert "historical witnessed evidence: dry." in stdout
    assert "No currently qualified declared method is available for that goal." in stdout
    refusal(next(row for row in rows if row["failure_class"] == "actor_request_unavailable"),
            "actor_request_unavailable")
    assert "Jun suggests a method based on what is accessible here." in stdout
    assert "ask Jun to clean Panel A using Detail Scrubber by scrubbing" in stdout
    remote = [row for row in rows
              if "No qualified local communication route" in row["player_visible_output"]]
    assert len(remote) == 2
    assert {row["failure_class"] for row in remote} == {
        "actor_report_unavailable", "work_method_discussion_unavailable"}
    accepted = restore(split, recipe)
    assert accepted.journal[:len(agreed.journal)] == agreed.journal
    completed_release, wipe, scrub = accepted.participation_state.records[-3:]
    assert completed_release.task_id == release.task_id and completed_release.status == "completed"
    assert len(completed_release.contributions) == 1 and not accepted.connections
    assert wipe.status == "withdrawn" and not wipe.contributions
    assert scrub.status == "active" and not scrub.contributions and scrub.tick > wipe.tick
    custody(accepted, "cord", "carried_by", worker)
    custody(accepted, "detail scrubber", "located_at", accepted.current_place_id())

    stdout, rows = play(split, "performed-and-returned", recipe, FOURTH, load=True)
    assert "Jun reports historical performed evidence: scrub." in stdout
    assert stdout.count("Brush patterns are visible.") == 2
    assert any(row["authoritative_changed"] for row in rows)
    final = restore(split, recipe)
    assert final.journal[:len(accepted.journal)] == accepted.journal
    assert final.participation_state.records[:-1] == accepted.participation_state.records[:-1]
    completed = final.participation_state.records[-1]
    assert scrub.task_id == completed.task_id and completed.status == "completed"
    assert len(completed.contributions) == 3
    physical = {event[0] for event in final.actor_events
                if event[1:3] == ("physical_contribution", worker)}
    assert physical == set((*standing.contributions, *completed_release.contributions,
                            *completed.contributions))
    assert residue(final, "panel b") == residue(final, "panel a") == 0
    custody(final, "cord", "carried_by", worker)
    custody(final, "detail scrubber", "carried_by", worker)
    assert tuple(interval[0] for interval in final.intervals) == tuple(range(1, len(final.intervals) + 1))

    # The installed startup admits a first look. The uninterrupted comparison
    # explicitly takes the same look at each seam to keep the inputs identical.
    full = tmp_path / "uninterrupted"
    play(full, "same-actions-with-looks", recipe,
         (*FIRST, "look", *SECOND, "look", *THIRD, "look", *FOURTH))
    assert (full / "campaign.json").read_bytes() == (split / "campaign.json").read_bytes()


def test_installed_stock_contrast_refusal_and_already_satisfied(tmp_path):
    odd = LocalityRecipe("coordination", 1)
    root = tmp_path / "odd"
    commands = (
        "go east", "ask sol about work", "ask sol to clean panel a using cloth by wiping",
        "take cloth", "ask sol to cancel work", "go north", "wait", "go south", "drop cloth",
        "inspect worksite", "ask sol about ways to clean panel a",
        "ask sol to clean panel a using cloth by wiping",
        "ask sol to clean panel a using detail scrubber by scrubbing",
        "go west", "go west", "take detail scrubber", "go east", "go east",
        "drop detail scrubber", "ask sol about ways to clean panel a",
        "ask sol to clean panel a using detail scrubber by scrubbing",
        "take detail scrubber", "ask sol to cancel work",
        "scrub panel a using detail scrubber", "scrub panel a using detail scrubber",
        *STAGE, "go west", "go north", "go south", "go west", "go east",
        "ask sol to release joining frame", "untie cord", "ask sol about work",
    )
    out, rows = play(root, "bring-stock-choose-to-work-alone", odd, commands)
    assert "Sol reports active: cleaning, scrub" in out
    assert "The worker sees no feasible local method right now." in out
    assert "Sol suggests a method based on what is accessible here." in out
    refused = [row for row in rows if row["failure_class"] == "actor_request_unavailable"]
    assert len(refused) == 3
    assert "No currently qualified declared method is available for that goal." in out
    for row in refused:
        refusal(row, "actor_request_unavailable")
    blocked = next(row for row in rows if row["failure_class"] == "material_passage_obstructed")
    assert blocked["raw_player_input"].strip() == "go south"
    refusal(blocked, "material_passage_obstructed")
    assert "externally_satisfied: recovery, joining frame; 0 own committed step(s)." in out
    app = restore(root, odd)
    assert app.participation_state.records[-1].status == "externally_satisfied"
    assert not app.participation_state.records[-1].contributions
    custody(app, "cord", "carried_by", app.fixture.player_entity_id)
    custody(app, "detail scrubber", "carried_by", app.fixture.player_entity_id)
    assert residue(app, "panel a") == 0
    assert not app.connections
    play(root, "wrong-seed", LocalityRecipe("coordination"), load=True, expected=2)


def test_installed_passive_drying_can_interrupt_prepared_wipe(tmp_path):
    recipe = LocalityRecipe("drying", 1)
    out, rows = play(tmp_path / "drying-at-execution", "last-moisture", recipe, (
        "go east", "take cloth", "wait", "wipe panel a using cloth", "inspect panel a",
    ))
    assert "Time passed, but the action was interrupted: wiping requires retained water" in out
    interrupted = rows[-2]
    assert interrupted["failure_class"] == "timed_action_interrupted"
    assert interrupted["authoritative_changed"] and interrupted["receipt_id"]
    assert interrupted["logical_time_after"] == interrupted["logical_time_before"] + 1
    assert residue(restore(tmp_path / "drying-at-execution", recipe), "panel a") == 3


def test_installed_constructed_annex_keeps_custody_and_limits_access(tmp_path):
    recipe = LocalityRecipe("sealed-annex", scale_level=1)
    root = tmp_path / "annex"
    out, rows = play(root, "inspect-open-and-retrieve", recipe, (
        "go east", "go east", "look", "inspect annex rag 1",
        "retrieve annex rag 1 from dry box", "open dry box", "look",
        "retrieve annex rag 1 from dry box", "inspect annex rag 1",
        "drop annex rag 1", "go west",
    ))
    assert "Packing Annex" in out and "Dry Box [closed]" in out
    assert "The container must be open first." in out
    assert "Dry Box [open; contains Annex Rag 1]" in out
    assert "Water: 2/2 unit(s)." in out
    row = next(row for row in rows if row["raw_player_input"].strip() == "retrieve annex rag 1 from dry box")
    assert row["failure_class"] and not row["authoritative_changed"]
    state = restore(root, recipe)
    rag = state.fixture.resolve_object_reference("annex rag 1")
    annex = next(p.entity_id for p in state.fixture.place_presentations if p.name == "Packing Annex")
    custody(state, "annex rag 1", "located_at", annex)
    out, _ = play(root, "return-to-the-same-annex", recipe, (
        "wait", "wait", "wait", "go east", "inspect annex rag 1", "go west", "go north", "go west",
    ), load=True)
    assert "Condition: dry." in out and "A drying trace is visible." in out
    final = restore(root, recipe)
    assert dict(final.water_state.water)[rag] == 0
    assert len(final.fixture.place_presentations) == 5 and not final.fixture.actor_order
    gate = next(p.entity_id for p in state.fixture.place_presentations if p.name == "Rain Gate")
    assert final.current_place_id() == gate
    custody(final, "annex rag 1", "located_at", annex)
    play(root, "wrong-scale", LocalityRecipe("sealed-annex", scale_level=2), load=True, expected=2)


def test_adjoining_annex_admission_preserves_prefix_identities_and_edges():
    near, detailed = (create_generated_locality_fixture(LocalityRecipe("sealed-annex", scale_level=n))
                      for n in (1, 3))
    assert near.campaign_id != detailed.campaign_id
    assert {p.entity_id for p in near.place_presentations} < {p.entity_id for p in detailed.place_presentations}
    assert set(near.initial_state.representation.relations) < set(detailed.initial_state.representation.relations)
    assert set(near.movement_routes) < set(detailed.movement_routes)
    actual = [(edge.source_place_id, edge.direction) for edge in detailed.movement_routes]
    assert len(actual) == len(set(actual))


def test_failed_acknowledgement_preserves_revised_cleaning_agreement(tmp_path, monkeypatch):
    path = tmp_path / "campaign.json"
    app, _ = build_generated_locality(LocalityRecipe("coordination"), path)
    for method, args in (
        ("wait", ()), ("wait", ()), ("wait", ()), ("move", ("east",)),
        ("request_cleaning", ("Jun", "Panel A", "Cloth", "wipe")),
        ("pickup", ("Cloth",)), ("participation_control", ("Jun", "cancel")),
        ("request_cleaning", ("Jun", "Panel A", "Detail Scrubber", "scrub")),
    ):
        assert getattr(app, method)(*args).authoritative_changed
    before = path.read_bytes(), app.authoritative_digest()
    worker = app.fixture.actor_order[0]
    prior, revised = app.participation_state.records[-2:]

    def fail_write():
        raise OSError("injected checkpoint failure before acknowledgement")

    with monkeypatch.context() as patch:
        patch.setattr(app, "save", fail_write)
        failure = app.wait()
    assert failure.failure_class == "material_checkpoint_write_failed"
    assert not failure.authoritative_changed and (path.read_bytes(), app.authoritative_digest()) == before
    resumed = restore(tmp_path, LocalityRecipe("coordination"))
    assert resumed.wait().authoritative_changed
    assert resumed.participation_state.records[-2] == prior
    progressed = resumed.participation_state.records[-1]
    assert progressed.task_id == revised.task_id and len(progressed.contributions) == 1
    custody(resumed, "detail scrubber", "carried_by", worker)
    assert restore(tmp_path, LocalityRecipe("coordination")).authoritative_digest() == resumed.authoritative_digest()


def test_worksite_discussion_does_not_reach_an_absent_worker():
    app, _ = build_generated_locality(LocalityRecipe("coordination"))
    original = app.authoritative_digest()
    result = app.suggest_cleaning("Jun", "Panel A")
    assert result.failure_class == "work_method_discussion_unavailable"
    assert "No qualified local communication route is available." in result.message
    assert "Detail Scrubber" not in result.message
    assert app.authoritative_digest() == original
