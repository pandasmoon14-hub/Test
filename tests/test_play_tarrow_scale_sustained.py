"""Package 08 sustained cross-site acceptance using existing owner transitions.

One world and one brush: each declared annex worker must actually acquire and
use it at their own location. This test does not mint parallel resources,
teleport actors, inject events, or treat remote evidence as player knowledge.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_generated_locality import LocalityRecipe, build_generated_locality, create_generated_locality_fixture
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_material_application import MaterialError


@dataclass(frozen=True)
class Step:
    method: str
    args: tuple
    expected_changed: bool = True


def committed(app, step):
    before = app.authoritative_digest()
    tick_before = app.runtime_state.logical_time_state.logical_position
    result = getattr(app, step.method)(*step.args)
    if step.expected_changed:
        assert result.authoritative_changed and not result.failure_class, (
            step, result.result_type, result.message)
        assert result.receipt_id, step
        assert app.authoritative_digest() != before, step
    else:
        assert not result.authoritative_changed and result.failure_class, (
            step, result.result_type, result.message)
        assert app.authoritative_digest() == before, step
        assert app.runtime_state.logical_time_state.logical_position == tick_before
    if step.method in ("move", "pickup", "drop", "request_object_from_actor", "wait"):
        if step.expected_changed:
            assert app.runtime_state.logical_time_state.logical_position == tick_before + 1
    return result


def move(app, direction, visited):
    committed(app, Step("move", (direction,)))
    visited.add(app.current_place_id())


def worker_id(app, n):
    return app.fixture.resolve_actor_reference(f"Wing {n} Worker")


def panel_id(app, n):
    return app.fixture.resolve_object_reference(f"Wing {n} Panel")


def assert_owner_truth(app, visited, finished):
    brush = app.fixture.resolve_object_reference("Brush")
    actors = {app.fixture.player_entity_id, *app.fixture.actor_order}
    relation = placement(app.state.representation, brush)
    assert relation.relation_type in {"carried_by", "located_at"}
    assert relation.object_entity_id in actors or relation.object_entity_id in {
        p.entity_id for p in app.fixture.place_presentations}
    for n in finished:
        actor, panel = worker_id(app, n), panel_id(app, n)
        records = [e for e in app.actor_events if e[1] == "physical_contribution" and e[2] == actor]
        assert len(records) >= 2, (n, records)
        assert len({e[0] for e in records}) == len(records)
        assert dict(app.water_state.adhered)[panel] < 3
        # The worker never gains knowledge of panels at another worksite,
        # even though all places share the same authoritative campaign.
        for other in range(1, len(app.fixture.actor_profiles) - 1):
            if other != n and other <= len(app.fixture.actor_profiles) - 2:
                assert not any(e.actor_id == actor and e.target_id == panel_id(app, other)
                               for e in app.evidence_state.events)
    assert app.runtime_state.logical_time_state.logical_position == len(app.intervals)
    assert len({interval[0] for interval in app.intervals}) == len(app.intervals)


def drive(app, level, *, checkpoint_path=None):
    visited = {app.current_place_id()}
    brush = app.fixture.resolve_object_reference("Brush")
    original_panel = app.fixture.resolve_object_reference("Panel A")
    # The original workshop remains reachable but has no immediate line of
    # communication to any annex. This rejection cannot change world truth.
    apply(Step("request_cleaning", ("Wing 1 Worker", "Wing 1 Panel", "Brush", "scrub"), False))
    apply(Step("ask_report", ("Wing 1 Worker", "Wing 1 Panel", "residue"), False))

    # The workshop has a lawful competing need for the one tool.
    apply(Step("request_cleaning", ("Jun", "Panel A", "Brush", "scrub")))
    apply(Step("pickup", ("Brush",)))
    assert placement(app.state.representation, brush).object_entity_id == app.fixture.player_entity_id
    assert any(e[1] == "due_resolution" and e[2] == app.fixture.resolve_actor_reference("Jun")
               and e[3][2] == "blocked" for e in app.actor_events)

    # Player physically delivers the brush, then each worker acquires and
    # scrubs. The previous actor must consent to a pause and handoff before
    # the same finite resource can be moved to the next annex.
    routes = {
        1: ("east",),
        2: ("west", "west", "south"),
        3: ("north", "west", "west"),
    }
    finished = []
    split_digest = None
    split_journal = None
    split_bytes = None
    replay_steps = []

    def apply(step):
        result = committed(app, step)
        if split_bytes is not None:
            replay_steps.append(step)
        return result

    def travel(direction):
        result = apply(Step("move", (direction,)))
        visited.add(app.current_place_id())
        return result
    for n in range(1, level + 1):
        for direction in routes[n]:
            travel(direction)
        assert app.current_place_id() == next(
            p.entity_id for p in app.fixture.place_presentations if p.name == f"Work Annex {n}")
        apply(Step("drop", ("Brush",)))
        # Witnessed vs deliberately reported assertions remain distinct.
        if n == 1:
            apply(Step("tell_actor", (f"Wing {n} Worker", f"Wing {n} Panel", "residue", "clear")))
            apply(Step("ask_report", (f"Wing {n} Worker", f"Wing {n} Panel", "residue")))
        apply(Step("request_cleaning", (f"Wing {n} Worker", f"Wing {n} Panel", "Brush", "scrub")))
        apply(Step("wait", ()))  # worker takes custody
        assert placement(app.state.representation, brush).object_entity_id == worker_id(app, n)
        # The player cannot take a tool carried by the worker.
        apply(Step("pickup", ("Brush",), False))
        apply(Step("wait", ()))  # worker actually cleans
        assert dict(app.water_state.adhered)[panel_id(app, n)] < 3
        if n == 1:
            apply(Step("ask_report", ("Wing 1 Worker", "Wing 1 Panel", "residue")))
            comparison = app.compare_history("Wing 1 Panel", "residue")
            assert not comparison.authoritative_changed
            assert "clear" in comparison.message and "present" in comparison.message
            assert "No account is selected as true" in comparison.message

        finished.append(n)
        if n < level:
            apply(Step("participation_control", (f"Wing {n} Worker", "pause")))
            apply(Step("request_object_from_actor", (f"Wing {n} Worker", "Brush")))
            assert placement(app.state.representation, brush).object_entity_id == app.fixture.player_entity_id
            if n == 1 and checkpoint_path is not None:
                app.checkpoint_path = checkpoint_path
                saved = app.save()
                assert not saved.failure_class and checkpoint_path.is_file()
                snapshot = InvestigationApplication.restore(
                    fixture=app.fixture, checkpoint_path=checkpoint_path)
                assert snapshot.authoritative_digest() == app.authoritative_digest()
                assert snapshot.journal == app.journal
                split_digest = app.authoritative_digest()
                split_journal = app.journal
                split_bytes = checkpoint_path.read_bytes()
                app.checkpoint_path = None
        # All work is in the one campaign; no other worker knows these
        # panel changes through an automatic universal broadcast.
        assert not any(e.actor_id == worker_id(app, n) and e.target_id == original_panel
                       for e in app.evidence_state.events)

    # Visit both the store and yard, then return to the workshop and check
    # the workshop's unresolved/withdrawn status without omniscience.
    if level == 1:
        tail = ("west", "west", "west", "east", "north", "south")
    elif level == 2:
        tail = ("north", "west", "east", "north", "south")
    else:
        tail = ("east", "east", "north", "south")
    for direction in tail:
        travel(direction)
    apply(Step("inspect", ("Panel A",)))
    for _ in range(9):
        apply(Step("wait", ()))
    assert visited == {p.entity_id for p in app.fixture.place_presentations}, (
        level, visited, [p.name for p in app.fixture.place_presentations])
    assert_owner_truth(app, visited, finished)
    if split_bytes is not None:
        assert checkpoint_path.read_bytes() == split_bytes
        shadow = InvestigationApplication.restore(
            fixture=app.fixture, checkpoint_path=checkpoint_path)
        assert shadow.authoritative_digest() == split_digest
        assert shadow.journal == split_journal
        shadow.checkpoint_path = None
        for step in replay_steps:
            committed(shadow, step)
        assert shadow.authoritative_digest() == app.authoritative_digest()
        assert shadow.journal == app.journal
        assert shadow.actor_events == app.actor_events
        assert shadow.evidence_state == app.evidence_state
        assert shadow.participation_state == app.participation_state
        assert shadow.water_state == app.water_state
        assert shadow.runtime_state.logical_time_state == app.runtime_state.logical_time_state
    jun = app.fixture.resolve_actor_reference("Jun")
    assert any(e[1] == "due_resolution" and e[2] == jun and e[3][2] == "blocked"
               for e in app.actor_events)
    return {"finished": tuple(finished), "visited": tuple(sorted(visited)),
            "split_digest": split_digest, "split_journal": split_journal,
            "final_digest": app.authoritative_digest(), "intervals": len(app.intervals),
            "journal": app.journal}


@pytest.mark.parametrize("level", (1, 2, 3))
def test_sustained_all_annex_workers_and_world_continuity(tmp_path, level):
    recipe = LocalityRecipe("evidence", seed=0, scale_level=level)
    a, prehistory = build_generated_locality(recipe)
    assert len(prehistory) == 3
    outcome = drive(a, level, checkpoint_path=tmp_path / "midworld.json")
    assert len(outcome["finished"]) == level
    assert outcome["intervals"] >= 15
    assert all(any(e[1] == "physical_contribution" and e[2] == worker_id(a, n)
                   for e in a.actor_events) for n in range(1, level + 1))
    if level >= 2:
        # Every later result must be replayable from the original generation
        # plus its qualified ordered journal, and not from an invented history.
        checkpoint = tmp_path / "midworld.json"
        assert checkpoint.exists()
        a.checkpoint_path = checkpoint
        saved = a.save()
        assert not saved.failure_class
        b = InvestigationApplication.restore(fixture=a.fixture, checkpoint_path=checkpoint)
        assert b.authoritative_digest() == a.authoritative_digest()
        assert b.journal == a.journal
        assert b.evidence_state == a.evidence_state
        assert b.participation_state == a.participation_state
        for _ in range(4):
            committed(a, Step("wait", ()))
            committed(b, Step("wait", ()))
        assert a.authoritative_digest() == b.authoritative_digest()
        assert len(a.intervals) == len(b.intervals)


def test_sustained_strict_checkpoint_binding_and_negative_controls(tmp_path):
    recipe = LocalityRecipe("evidence", 0, scale_level=3)
    app, _ = build_generated_locality(recipe)
    checkpoint = tmp_path / "world.json"
    app.checkpoint_path = checkpoint
    assert not app.save().failure_class
    original = checkpoint.read_bytes()
    with pytest.raises((ValueError, MaterialError)):
        InvestigationApplication.restore(fixture=create_generated_locality_fixture(
            LocalityRecipe("evidence", 0, scale_level=2)), checkpoint_path=checkpoint)
    assert checkpoint.read_bytes() == original
    # Resealing unrelated content must not promote a mismatched profile.
    with pytest.raises(ValueError, match="restored"):
        build_generated_locality(recipe, checkpoint)
    assert checkpoint.read_bytes() == original
