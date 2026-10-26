"""Package 08 final adversarial acceptance: one qualified access + all-worker campaign.

Uses existing noncanonical access recipe and owner-owned actions. No private state
injection, second clock, resource cloning, synthetic actor outcomes or new rules.
"""
from __future__ import annotations

import json

import pytest

from astra_runtime.domain.persistent_world_material import (
    MaterialError, active_effects, digest, placement,
)
from astra_runtime.myravant_generated_locality import (
    LocalityRecipe, build_generated_locality, create_generated_locality_fixture,
)
from astra_runtime.myravant_investigation_application import InvestigationApplication
import astra_runtime.myravant_material_application as material


def act(app, method, *args, failure=None):
    pre = app.authoritative_digest()
    tick = app.runtime_state.logical_time_state.logical_position
    result = getattr(app, method)(*args)
    if failure is not None:
        assert result.failure_class == failure, (method, result.failure_class, result.message)
        assert not result.authoritative_changed
        assert app.authoritative_digest() == pre
        assert app.runtime_state.logical_time_state.logical_position == tick
    else:
        assert result.authoritative_changed and not result.failure_class, (
            method, args, result.result_type, result.message,
        )
        assert result.receipt_id and app.authoritative_digest() != pre
    return result


def valid_world(app, finished):
    assert app.runtime_state.logical_time_state.logical_position == len(app.intervals)
    assert len({row[0] for row in app.intervals}) == len(app.intervals)
    assert len({event[0] for event in app.actor_events}) == len(app.actor_events)
    brush = app.fixture.resolve_object_reference("Brush")
    custody = placement(app.state.representation, brush)
    assert custody.relation_type in {"located_at", "carried_by"}
    for n in finished:
        actor = app.fixture.resolve_actor_reference(f"Wing {n} Worker")
        panel = app.fixture.resolve_object_reference(f"Wing {n} Panel")
        contributions = [e for e in app.actor_events
                         if e[1] == "physical_contribution" and e[2] == actor]
        assert len(contributions) >= 2
        assert len({e[0] for e in contributions}) == len(contributions)
        assert dict(app.water_state.adhered)[panel] < 3
        for other in range(1, len(app.fixture.actor_profiles) - 1):
            if other != n:
                other_panel = app.fixture.resolve_object_reference(f"Wing {other} Panel")
                assert not any(e.actor_id == actor and e.target_id == other_panel
                               for e in app.evidence_state.events)


@pytest.mark.parametrize("level", (1, 2, 3))
def test_access_change_contested_resources_private_evidence_and_long_replay(tmp_path, level):
    # In contrast with the older evidence-only all-annex test, this live
    # access-profile history begins with a real assembled passage obstruction.
    app, initial = build_generated_locality(LocalityRecipe("access", 0, scale_level=level))
    assert len(initial) == 6
    assert app.fixture.provenance.canon is False
    assert app.current_place_id() == next(p.entity_id for p in app.fixture.place_presentations
                                          if p.name == "Workshop")
    def obstructed(world):
        return any(e.kind == "movement" and e.direction == "north"
                   for e in active_effects(world.state.representation, world.connections,
                                           world.fixture.material_profile))
    assert obstructed(app)
    act(app, "move", "north", failure="material_passage_obstructed")

    # An actor's earlier accepted workshop request makes genuine competing
    # claims on the same finite brush as it moves through successive sites.
    act(app, "request_cleaning", "Jun", "Panel A", "Brush", "scrub")
    act(app, "pickup", "Brush")
    assert any(e[1] == "due_resolution" and e[2] == app.fixture.resolve_actor_reference("Jun")
               and e[3][2] == "blocked" for e in app.actor_events)

    visited = {app.current_place_id()}
    def move(direction):
        act(app, "move", direction)
        visited.add(app.current_place_id())

    # Access denial changes the actual route and number of committed travel
    # intervals: the older alternate route still exists and is not magical
    # clearing of the same physical obstruction.
    move("west")
    move("north")
    move("south")
    assert obstructed(app)
    act(app, "material", "untie", "Cord")
    assert not obstructed(app)
    move("north")
    move("south")

    # Keep the first-worker handoff as a persistent acknowledged prefix;
    # independently replay *every later action* through the real journal owner.
    mirror = None
    path = tmp_path / f"scale-{level}.json"
    def both(method, *args, failure=None):
        main = act(app, method, *args, failure=failure)
        if mirror is not None:
            other = act(mirror, method, *args, failure=failure)
            assert other.failure_class == main.failure_class
            assert app.authoritative_digest() == mirror.authoritative_digest()
            assert app.journal == mirror.journal
        return main
    def travel(direction):
        both("move", direction)
        visited.add(app.current_place_id())

    for n in range(1, level + 1):
        if n == 1:
            directions = ("east",)
        elif n == 2:
            directions = ("west", "west", "south")
        else:
            directions = ("north", "west", "west")
        for direction in directions:
            travel(direction)
        assert app.current_place_id() == next(p.entity_id for p in app.fixture.place_presentations
                                              if p.name == f"Work Annex {n}")
        both("drop", "Brush")
        if n == 1:
            both("tell_actor", "Wing 1 Worker", "Wing 1 Panel", "residue", "clear")
            both("ask_report", "Wing 1 Worker", "Wing 1 Panel", "residue")
        both("request_cleaning", f"Wing {n} Worker", f"Wing {n} Panel", "Brush", "scrub")
        both("wait")
        brush = app.fixture.resolve_object_reference("Brush")
        assert placement(app.state.representation, brush).object_entity_id == (
            app.fixture.resolve_actor_reference(f"Wing {n} Worker"))
        both("wait")
        assert dict(app.water_state.adhered)[app.fixture.resolve_object_reference(f"Wing {n} Panel")] < 3
        if n == 1:
            both("ask_report", "Wing 1 Worker", "Wing 1 Panel", "residue")
            before = app.authoritative_digest()
            comparison = app.compare_history("Wing 1 Panel", "residue")
            assert not comparison.authoritative_changed and app.authoritative_digest() == before
            assert "clear" in comparison.message and "present" in comparison.message
        if n < level:
            both("participation_control", f"Wing {n} Worker", "pause")
            both("request_object_from_actor", f"Wing {n} Worker", "Brush")
            assert placement(app.state.representation, brush).object_entity_id == app.fixture.player_entity_id
            if n == 1:
                app.checkpoint_path = path
                assert not app.save().failure_class and path.is_file()
                original = path.read_bytes()
                mirror = InvestigationApplication.restore(
                    fixture=app.fixture, checkpoint_path=path)
                assert mirror.authoritative_digest() == app.authoritative_digest()
                assert mirror.journal == app.journal
                # Test future replay without rewriting the frozen mid-work file.
                app.checkpoint_path = None
                mirror.checkpoint_path = None

    if level == 1:
        tail = ("west", "west", "west", "east", "north", "south")
    elif level == 2:
        tail = ("north", "west", "east", "north", "south")
    else:
        tail = ("east", "east", "north", "south")
    for direction in tail:
        travel(direction)
    both("inspect", "Panel A")
    for _ in range(9):
        both("wait")
    assert visited == {p.entity_id for p in app.fixture.place_presentations}
    valid_world(app, range(1, level + 1))
    assert not obstructed(app)
    if mirror is not None:
        assert path.read_bytes() == original
        assert mirror.actor_events == app.actor_events
        assert mirror.evidence_state == app.evidence_state
        assert mirror.water_state == app.water_state
        assert mirror.participation_state == app.participation_state


@pytest.mark.parametrize("after_replace", (False, True))
def test_scale_three_late_write_fault_preserves_acknowledged_prefix(tmp_path, monkeypatch, after_replace):
    app, _ = build_generated_locality(LocalityRecipe("access", 0, scale_level=3))
    act(app, "pickup", "Brush")
    act(app, "move", "east")
    act(app, "drop", "Brush")
    act(app, "request_cleaning", "Wing 1 Worker", "Wing 1 Panel", "Brush", "scrub")
    act(app, "wait")  # acknowledged actor custody, due work pending
    path = tmp_path / "fault.json"
    app.checkpoint_path = path
    assert not app.save().failure_class
    acknowledged = app.authoritative_digest()
    original_journal = app.journal
    original_bytes = path.read_bytes()
    candidate_digests = []
    write = material._write_envelope
    def fault(**kwargs):
        candidate_digests.append(app.authoritative_digest())
        if after_replace:
            write(**kwargs)
        raise OSError("injected late durable-write interruption")
    monkeypatch.setattr(material, "_write_envelope", fault)
    result = app.wait()
    assert result.failure_class == "material_checkpoint_write_failed"
    assert not result.authoritative_changed
    assert app.authoritative_digest() == acknowledged
    assert app.journal == original_journal
    assert app.runtime_state.logical_time_state.logical_position == len(app.intervals)
    halted = app.wait()
    assert not halted.authoritative_changed
    assert halted.failure_class == "material_session_halted"
    monkeypatch.setattr(material, "_write_envelope", write)
    restored = InvestigationApplication.restore(fixture=app.fixture, checkpoint_path=path)
    assert restored.authoritative_digest() == (
        candidate_digests[0] if after_replace else acknowledged)
    assert len(restored.intervals) == len(app.intervals) + (1 if after_replace else 0)
    assert len(restored.journal) == len(original_journal) + (1 if after_replace else 0)
    if not after_replace:
        assert path.read_bytes() == original_bytes
    actor = app.fixture.resolve_actor_reference("Wing 1 Worker")
    before_count = sum(e[1] == "physical_contribution" and e[2] == actor
                       for e in restored.actor_events)
    act(restored, "wait")
    after_count = sum(e[1] == "physical_contribution" and e[2] == actor
                      for e in restored.actor_events)
    assert after_count - before_count in (0, 1)
    assert after_count >= 2
    valid_world(restored, (1,))


@pytest.mark.parametrize("change", ("order", "lost_work", "duplicate_time", "receipt", "binding", "extra"))
def test_scale_three_resealed_checkpoint_mutations_refused(tmp_path, change):
    app, _ = build_generated_locality(LocalityRecipe("access", 0, scale_level=3))
    act(app, "pickup", "Brush")
    act(app, "move", "east")
    act(app, "drop", "Brush")
    act(app, "request_cleaning", "Wing 1 Worker", "Wing 1 Panel", "Brush", "scrub")
    act(app, "wait")
    path = tmp_path / f"tamper-{change}.json"
    app.checkpoint_path = path
    assert not app.save().failure_class
    envelope = json.loads(path.read_text())
    payload = envelope["payload"]
    if change == "order":
        payload["profile"]["order"].reverse()
    elif change == "lost_work":
        payload["journal"].pop()
    elif change == "duplicate_time":
        payload["journal"].append(dict(payload["journal"][-1]))
    elif change == "receipt":
        payload["journal"][-1]["result"]["receipt_id"] = "astra:actor_receipt:forged"
    elif change == "binding":
        payload["profile"]["actors"][0]["actor_id"] = app.fixture.player_entity_id
    else:
        payload["evidence_snapshot"] = {"cross_site_omniscience": True}
    envelope["integrity_digest"] = digest(payload)
    path.write_text(json.dumps(envelope))
    with pytest.raises(MaterialError):
        InvestigationApplication.restore(fixture=app.fixture, checkpoint_path=path)
