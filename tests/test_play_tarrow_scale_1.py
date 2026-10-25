"""Package 08: connected, version-bound worksite scale through retained owners.

These are engineering-authored objective tests, not human acceptance or canon.
"""
from pathlib import Path

import pytest

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_generated_locality import (
    LocalityRecipe, build_generated_locality, create_generated_locality_fixture,
)
from astra_runtime.myravant_investigation_application import InvestigationApplication


def committed(result):
    assert result.authoritative_changed, (result.result_type, result.message)
    assert not result.failure_class, (result.result_type, result.message)
    assert result.receipt_id
    return result


@pytest.mark.parametrize("level", (0, 1, 2, 3))
def test_connected_profile_envelope_and_unique_shared_root(level):
    fixture = create_generated_locality_fixture(LocalityRecipe("evidence", seed=41, scale_level=level))
    assert len(fixture.place_presentations) == 4 + level
    assert len(fixture.movement_routes) == 8 + 2 * level
    assert len(fixture.object_presentations) == 10 + 2 * level
    assert len(fixture.actor_profiles) == 2 + level
    assert len(fixture.actor_order) == 2 + level
    assert len({p.actor_id for p in fixture.actor_profiles}) == 2 + level
    assert len({p.entity_id for p in fixture.object_presentations}) == 10 + 2 * level
    assert fixture.checkpoint_qualification["fixture_campaign_id"] == fixture.campaign_id
    assert not fixture.provenance.canon
    assert not fixture.provenance.default_world
    graph = {}
    for edge in fixture.movement_routes:
        graph.setdefault(edge.source_place_id, set()).add(edge.destination_place_id)
    reached = {fixture.place_presentations[0].entity_id}
    while True:
        extended = reached | {target for source in reached for target in graph.get(source, ())}
        if reached == extended:
            break
        reached = extended
    assert reached == {p.entity_id for p in fixture.place_presentations}
    assert set(fixture.actor_order) == {p.actor_id for p in fixture.actor_profiles}


@pytest.mark.parametrize("level", (1, 2, 3))
def test_shared_tool_changes_remote_work_without_remote_knowledge(tmp_path, level):
    recipe = LocalityRecipe("evidence", seed=0, scale_level=level)
    app, prehistory = build_generated_locality(recipe)
    assert len(prehistory) == 3
    brush = app.fixture.resolve_object_reference("Brush")
    wing_panel = app.fixture.resolve_object_reference("Wing 1 Panel")
    original_panel = app.fixture.resolve_object_reference("Panel A")
    wing_actor = app.fixture.resolve_actor_reference("Wing 1 Worker")
    jun = app.fixture.resolve_actor_reference("Jun")
    player = app.fixture.player_entity_id

    # The tool is contested at the workshop; the player acts before the
    # ordered actor's due physical action in this same committed interval.
    committed(app.request_cleaning("Jun", "Panel A", tool_reference="Brush", method="scrub"))
    committed(app.pickup("Brush"))
    assert placement(app.state.representation, brush).object_entity_id == player
    assert any(e[1] == "due_resolution" and e[2] == jun
               and e[3][2] == "blocked" for e in app.actor_events)

    # This is genuine same-campaign travel and physical tool relocation,
    # not parallel copies of the world or a remote actor instruction.
    committed(app.move("east"))
    committed(app.drop("Brush"))
    committed(app.request_cleaning("Wing 1 Worker", "Wing 1 Panel",
                                   tool_reference="Brush", method="scrub"))

    committed(app.wait())
    path = tmp_path / ("world-" + str(level) + ".json")
    app.checkpoint_path = path
    save = app.save()
    assert not save.failure_class
    assert path.is_file()
    restored = InvestigationApplication.restore(fixture=app.fixture, checkpoint_path=path)
    assert restored.authoritative_digest() == app.authoritative_digest()

    # Continue both copies independently: restore must replay exactly, with
    # one clock and owner-attributed contribution and conservation.
    for _ in range(3):
        committed(app.wait())
        committed(restored.wait())
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.actor_events == app.actor_events
    assert restored.evidence_state == app.evidence_state
    assert restored.water_state == app.water_state
    assert restored.runtime_state.logical_time_state.logical_position == len(restored.intervals)
    assert any(e[1] == "physical_contribution" and e[2] == wing_actor
               for e in restored.actor_events)
    assert dict(restored.water_state.adhered)[wing_panel] < 3

    # The worker observes the annex, not what happened at a remote workshop.
    assert not any(e.actor_id == wing_actor and e.target_id == original_panel
                   for e in restored.evidence_state.events)
    query_pre = restored.authoritative_digest()
    result = restored.recall_history("Wing 1 Panel", "residue")
    assert not result.authoritative_changed
    assert restored.authoritative_digest() == query_pre


def test_old_scale_zero_binding_unchanged_and_cross_scale_restore_rejected(tmp_path):
    legacy = LocalityRecipe("evidence", seed=2)
    explicit_zero = LocalityRecipe("evidence", seed=2, scale_level=0)
    original = create_generated_locality_fixture(legacy)
    equal = create_generated_locality_fixture(explicit_zero)
    assert original.campaign_id == equal.campaign_id
    assert original.provenance == equal.provenance
    assert original.actors_version == equal.actors_version
    app, _ = build_generated_locality(legacy)
    path = tmp_path / "legacy.json"
    app.checkpoint_path = path
    saved = app.save()
    assert not saved.failure_class
    with pytest.raises(Exception):
        InvestigationApplication.restore(
            fixture=create_generated_locality_fixture(LocalityRecipe("evidence", seed=2, scale_level=1)),
            checkpoint_path=path,
        )


@pytest.mark.parametrize("bad", (-1, 4, True, "1", 1.5))
def test_scale_level_refuses_invalid_or_implicit_semantics(bad):
    with pytest.raises(ValueError):
        LocalityRecipe("evidence", scale_level=bad)
