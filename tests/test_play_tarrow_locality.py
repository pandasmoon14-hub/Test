"""Authored installed-client and ownership checks; not blind/human acceptance."""
from dataclasses import replace
from io import StringIO
import json
import os
import subprocess
import sys

import pytest

from astra_runtime.myravant_play_application import MyravantPlayApplication as App
from astra_runtime.myravant_play_fixture import create_terminal_play_fixture, MyravantPlayFixtureError
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.myravant_terminal_capabilities import classify_bounded_terminal_request
from astra_runtime.myravant_tarrow import (
    PLACES, EDGES, PEOPLE, OBJECTS, create_tarrow_fixture, execute_tarrow_request, identity,
)


def play(app, *commands):
    output = StringIO()
    assert run_terminal(app, input_stream=StringIO("\n".join((*commands, "exit", ""))), output_stream=output,
                        specialized_router=execute_tarrow_request) == 0
    return output.getvalue()


def new(path=None):
    return App.new(fixture=create_tarrow_fixture(), checkpoint_path=path)


def assert_clean_output(text):
    assert "\\n" not in text and "\\r" not in text


def test_escape_guard_detects_known_presentation_defect():
    with pytest.raises(AssertionError):
        assert_clean_output("Time passes.\\nNext line")
    assert_clean_output("Time passes.\nNext line")


def test_distinct_source_bound_world_and_safe_initial_context():
    a = new()
    old = create_terminal_play_fixture()
    assert a.fixture.campaign_id != old.campaign_id
    assert not {e.entity_id for e in a.state.representation.entities} & {e.entity_id for e in old.initial_state.representation.entities}
    assert len(PLACES) == 12 and len(PEOPLE) == 7
    assert len(a.fixture.object_presentations) == len(OBJECTS) == 10
    assert not a.fixture.provenance.canon
    assert all(p.source for p in PLACES)
    text = play(a, "help", "locality", "community", "activities")
    assert "Mira Venn" in text and "not yet" in text
    assert "Pin Blank" not in text and "failed linkage" not in text
    assert "Groundskeeper" not in text and "Workshop Commons" not in text
    assert_clean_output(text)


@pytest.mark.parametrize("start,direction,end", EDGES)
def test_every_declared_edge_executes_and_restores(tmp_path, start, direction, end):
    # Reach source by public routes, not mutation of authoritative player state.
    from collections import deque
    todo = deque([("common", [])]); seen = set(); route = None
    while todo:
        node, steps = todo.popleft()
        if node == start:
            route = steps; break
        if node in seen:
            continue
        seen.add(node)
        todo.extend((b, steps + [d]) for a,d,b in EDGES if a == node)
    assert route is not None
    path = tmp_path / "journey.json"
    app = new(path)
    for d in route:
        assert app.move(d).authoritative_changed
    result = app.move(direction)
    assert result.receipt_id and result.authoritative_changed
    assert app.current_place_id() == identity(end)
    app.save()
    restored = App.restore(checkpoint_path=path, fixture=create_tarrow_fixture())
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.current_place_id() == identity(end)


def test_light_storage_fixedness_partial_completion_and_replay(tmp_path):
    path = tmp_path / "tarrow.json"
    a = new(path)
    text = play(a, "take shuttered service lamp", "light shuttered service lamp",
                "go south then open red-lashed parts coffer", "inspect red-lashed parts coffer",
                "take oak gate wedge", "go east", "look", "take floodmark post", "wait")
    assert "Inside: Oak Gate Wedge, Maintenance Slate" in text
    assert "Soft-Iron Pin Blank" not in text
    assert "cannot pick" in text and "Time passes." in text
    assert a.current_place_id() == identity("underbank")
    assert a._bounded_local_light_available()
    assert a.runtime_state.logical_time_state.logical_position == 1
    restored = App.restore(checkpoint_path=path, fixture=create_tarrow_fixture())
    assert a.authoritative_digest() == restored.authoritative_digest()
    assert restored.object_lit_state(identity("lamp")).state == "lit"
    # Local illumination follows the qualified source, including containment.
    play(restored, "go west", "put shuttered service lamp in red-lashed parts coffer",
         "close red-lashed parts coffer", "go east")
    assert not restored._bounded_local_light_available()
    assert "cannot" in play(restored, "inspect floodmark post").casefold()
    assert_clean_output(text)


def test_fixedness_is_a_declared_qualification_not_a_name_special_case():
    f = create_tarrow_fixture()
    a = App.new(fixture=replace(f, fixed_object_ids=(*f.fixed_object_ids, identity("lamp"))))
    before = a.authoritative_digest()
    result = a.pickup("shuttered service lamp")
    assert not result.authoritative_changed and result.failure_class
    assert a.authoritative_digest() == before
    with pytest.raises(MyravantPlayFixtureError):
        replace(f, fixed_object_ids=(identity("not-declared"),))


@pytest.mark.parametrize("raw", [
    "inspect chest brace", "ask groundskeeper to repair chest latch with lantern",
    "ask groundskeeper to follow me", "get lantern to orchard", "service chest latch",
])
def test_stock_specialists_not_admitted_or_partially_executed(raw):
    a = new(); before = a.authoritative_digest()
    assert classify_bounded_terminal_request(raw, fixture=a.fixture) is None
    play(a, "go south then " + raw)
    assert a.authoritative_digest() == before
    play(a, raw)
    assert a.authoritative_digest() == before


def test_unknown_or_hidden_targets_do_not_disclose_or_mutate():
    a = new(); play(a, "go south")
    before = a.authoritative_digest()
    text = play(a, "inspect soft-iron pin blank", "take soft-iron pin blank", "open sorting rack", "ask kera doss for soft-iron pin blank")
    assert "behind" not in text and "warped" not in text and "Inside:" not in text
    assert a.authoritative_digest() == before


def test_wait_advances_time_without_default_actor_process(tmp_path):
    a = new(tmp_path / "time.json")
    relations = a.state.representation.relations
    text = play(a, *("wait" for _ in range(9)))
    assert text.count("Time passes.") == 9
    assert a.runtime_state.logical_time_state.logical_position == 9
    assert a.state.representation.relations == relations
    b = App.restore(checkpoint_path=a.checkpoint_path, fixture=create_tarrow_fixture())
    assert b.authoritative_digest() == a.authoritative_digest()


def test_interiors_do_not_create_implicit_routes_or_access():
    assert not any(b in {"household", "stores", "east"} for a,d,b in EDGES)
    a = new(); play(a, "go south", "go south")
    before = a.authoritative_digest()
    assert not a.move("east").authoritative_changed
    assert a.authoritative_digest() == before


def test_installed_launch_restore_and_wrong_locality_rejection(tmp_path):
    import shutil
    executable = shutil.which("myravant-play")
    assert executable, "package must be installed"
    checkpoint = tmp_path / "saved.json"
    args = [executable, "--locality", "tarrow", "--checkpoint", str(checkpoint)]
    first = subprocess.run(args, input="take shuttered service lamp\nlight shuttered service lamp\ngo south then go east\nwait\nsave\nexit\n", text=True, capture_output=True, timeout=30)
    assert first.returncode == 0, first.stderr
    assert "Underbank Walk" in first.stdout and "Time passes." in first.stdout
    second = subprocess.run([executable, "--locality", "tarrow", "--load", str(checkpoint)], input="look\nexit\n", text=True, capture_output=True, timeout=30)
    assert second.returncode == 0, second.stderr
    assert "Floodmark Post" in second.stdout
    wrong = subprocess.run([executable, "--load", str(checkpoint)], input="exit\n", text=True, capture_output=True, timeout=30)
    assert wrong.returncode == 2 and "Unable to restore" in wrong.stderr
    assert_clean_output(first.stdout + second.stdout)


def test_durable_write_failure_stops_before_acknowledgement(tmp_path, monkeypatch):
    a = new(tmp_path / "save.json")
    def fail():
        raise OSError("injected write failure")
    monkeypatch.setattr(a, "save", fail)
    out = StringIO()
    with pytest.raises(SystemExit) as failure:
        run_terminal(a, input_stream=StringIO("take shuttered service lamp then go south\nexit\n"),
                     output_stream=out, specialized_router=execute_tarrow_request)
    assert failure.value.code == 3
    text = out.getvalue()
    assert "durably acknowledged" in text
    assert "You pick up" not in text and "You move" not in text
    assert a.current_place_id() == identity("common")


def test_initial_containment_requires_a_verified_root_witness(tmp_path):
    from astra_runtime.domain.persistent_world_component_checkpoint import restore_persistent_world_world1_checkpoint
    from astra_runtime.domain.persistent_world_local_checkpoint_restore import PersistentWorldCheckpointEvidenceError
    f = create_tarrow_fixture(); a = new(tmp_path / "initial.json"); a.save()
    args = dict(checkpoint_path=a.checkpoint_path, expected_campaign_id=f.campaign_id,
                expected_initial_open_states=f.initial_object_open_states,
                expected_initial_lit_states=f.initial_object_lit_states,
                expected_initial_representation_digest=f.provenance.initial_state_digest)
    # Legacy callers still fail closed rather than accepting a blanket exemption.
    with pytest.raises(PersistentWorldCheckpointEvidenceError, match="without attributable"):
        restore_persistent_world_world1_checkpoint(**args)
    restored = restore_persistent_world_world1_checkpoint(
        **args, expected_initial_representation=f.initial_state.representation)
    assert restored.movement_state.representation.campaign_id == f.campaign_id
    wrong = create_terminal_play_fixture().initial_state.representation
    with pytest.raises(PersistentWorldCheckpointEvidenceError, match="witness"):
        restore_persistent_world_world1_checkpoint(**args, expected_initial_representation=wrong)


def test_unreceipted_initial_contents_change_is_not_laundered(tmp_path):
    from astra_runtime.domain.persistent_world_entity_location_representation import create_persistent_world_entity_location_representation
    from astra_runtime.domain.persistent_world_movement_integration import create_persistent_world_movement_runtime_state
    from astra_runtime.domain.persistent_world_local_checkpoint_restore import PersistentWorldCheckpointEvidenceError
    f = create_tarrow_fixture()
    rep = f.initial_state.representation
    # A self-consistent writer can checksum a forged placement; only the
    # independently supplied original fixture root must authorize its history.
    changed = create_persistent_world_entity_location_representation(
        campaign_id=rep.campaign_id, entities=rep.entities,
        relations=tuple(replace(r, object_entity_id=identity("coffer"))
                        if r.subject_entity_id == identity("blank") else r for r in rep.relations))
    bad = App.new(fixture=replace(f, initial_state=create_persistent_world_movement_runtime_state(representation=changed)),
                  checkpoint_path=tmp_path / "forged.json")
    bad.save()
    with pytest.raises(PersistentWorldCheckpointEvidenceError, match="initial representation"):
        App.restore(fixture=f, checkpoint_path=bad.checkpoint_path)


def test_binding_revision_cannot_reinterpret_existing_campaign(tmp_path, monkeypatch):
    from astra_runtime import myravant_tarrow as t
    from astra_runtime.domain.persistent_world_local_checkpoint_restore import PersistentWorldCheckpointError
    a = new(tmp_path / "revision.json"); a.save()
    monkeypatch.setattr(t, "EDGES", tuple(e for e in t.EDGES if e != ("common", "west", "guest")))
    different = t.create_tarrow_fixture()
    assert different.campaign_id != a.fixture.campaign_id
    with pytest.raises(PersistentWorldCheckpointError):
        App.restore(fixture=different, checkpoint_path=a.checkpoint_path)


def test_second_refusal_preserves_first_durable_step(tmp_path):
    a = new(tmp_path / "partial.json")
    text = play(a, "take shuttered service lamp then take floodmark post")
    assert "step 1/2: You pick up" in text and "step 2/2:" in text
    b = App.restore(fixture=create_tarrow_fixture(), checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()
    assert b.current_place_id() == identity("common")
    assert any(r.subject_entity_id == identity("lamp") and r.object_entity_id == a.fixture.player_entity_id
               for r in b.state.representation.relations)
