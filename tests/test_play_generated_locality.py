"""G1-G12 generated worksite controls: owner effects, audience, and replay."""
from dataclasses import replace
import io

import pytest

from astra_runtime.domain.persistent_world_material import MaterialError, active_effects, placement
from astra_runtime.myravant_generated_locality import (
    CASES, InvalidLocality, LocalityBudgetExhausted, LocalityRecipe,
    UnsatisfiableLocality, build_generated_locality, create_generated_locality_fixture,
)
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture
from astra_runtime.myravant_terminal import main, run_terminal
from astra_runtime.myravant_tarrow_investigation import execute_investigation_request


def changed(result):
    assert result.authoritative_changed and result.failure_class is None, result.message
    return result


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("seed", (0, 1))
def test_neutral_roots_are_deterministic_and_distinct_from_legacy(case, seed):
    recipe = LocalityRecipe(case, seed)
    a = create_generated_locality_fixture(recipe)
    b = create_generated_locality_fixture(recipe)
    assert a.campaign_id == b.campaign_id
    assert a.provenance.initial_state_digest == b.provenance.initial_state_digest
    assert a.provenance.fixture_version == b.provenance.fixture_version
    assert a.campaign_id != create_investigation_fixture("neutral-relay").campaign_id
    assert len(a.place_presentations) == 4
    assert {p.name for p in a.place_presentations} == {
        "Entrance", "Workshop", "Covered Yard", "Store"}
    assert all("generated-worksite-" in p.entity_id for p in a.object_presentations)
    assert a.provenance.canon is False
    assert a.provenance.origin_merge_commit == '0' * 40
    assert a.provenance.origin_merged_at == ''  # not inherited neutral merge evidence


@pytest.mark.parametrize("case", CASES)
def test_lawful_preplay_history_roundtrips_and_continues(case, tmp_path):
    recipe = LocalityRecipe(case, 0)
    path = tmp_path / ("generated-" + case + ".json")
    app, receipts = build_generated_locality(recipe, path)
    assert len(receipts) >= 1
    assert len({r for _, r in receipts}) == len(receipts)
    assert path.is_file()
    restored = InvestigationApplication.restore(
        fixture=create_generated_locality_fixture(recipe), checkpoint_path=path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.journal == app.journal
    changed(restored.wait())
    next_restore = InvestigationApplication.restore(
        fixture=create_generated_locality_fixture(recipe), checkpoint_path=path)
    assert next_restore.authoritative_digest() == restored.authoritative_digest()
    assert len(next_restore.journal) == len(restored.journal)


def test_access_barrier_is_live_material_and_alternate_route_exists(tmp_path):
    app, _ = build_generated_locality(LocalityRecipe("access"), tmp_path / "a.json")
    assert app.current_place_id() == next(
        p.entity_id for p in app.fixture.place_presentations if p.name == "Workshop")
    effects = active_effects(app.state.representation, app.connections,
                             app.fixture.material_profile)
    assert any(e.kind == "movement" and e.direction == "north" for e in effects)
    denied = app.move("north")
    assert denied.failure_class == "material_passage_obstructed"
    # A different existing path is not a magically cleared material barrier.
    changed(app.move("west"))
    changed(app.move("north"))
    changed(app.move("south"))
    changed(app.material("untie", "Cord"))
    assert not active_effects(app.state.representation, app.connections,
                              app.fixture.material_profile)
    changed(app.move("north"))
    restored = InvestigationApplication.restore(
        fixture=app.fixture, checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert restored.current_place_id() == app.current_place_id()


@pytest.mark.parametrize("seed", (0, 1))
def test_resource_contest_allocates_one_real_tool_to_declared_actor(seed, tmp_path):
    app, _ = build_generated_locality(LocalityRecipe("resources", seed),
                                      tmp_path / "resource.json")
    brush = next(p.entity_id for p in app.fixture.object_presentations
                 if p.name == "Brush")
    held = placement(app.state.representation, brush)
    assert held.relation_type == "carried_by"
    assert held.object_entity_id == app.fixture.actor_order[0]
    assert len([r for r in app.state.representation.relations
                if r.subject_entity_id == brush]) == 1
    assert app.fixture.actor_order[0] != create_generated_locality_fixture(
        LocalityRecipe("resources", 1 - seed)).actor_order[0]
    assert dict(app.water_state.adhered)[next(
        p.entity_id for p in app.fixture.object_presentations if p.name == "Panel A")] >= 0


@pytest.mark.parametrize("seed", (0, 1))
def test_evidence_reports_are_admitted_not_transmuted_into_truth(seed, tmp_path):
    app, _ = build_generated_locality(LocalityRecipe("evidence", seed),
                                      tmp_path / "evidence.json")
    assert app.disclosed_relays
    panel = next(p.entity_id for p in app.fixture.object_presentations
                 if p.name == "Panel A")
    assert dict(app.water_state.adhered)[panel] == 3
    recall = app.recall_history("panel a", "residue")
    assert not recall.authoritative_changed
    assert "received statement" in recall.message.casefold()
    assert "clear" in recall.message.casefold()
    assert app.compare_history("panel a", "residue").failure_class is None
    assert app.authoritative_digest() == InvestigationApplication.restore(
        fixture=app.fixture, checkpoint_path=app.checkpoint_path).authoritative_digest()


def test_generation_failures_are_bounded_and_distinct(tmp_path, monkeypatch):
    with pytest.raises(UnsatisfiableLocality):
        LocalityRecipe("access", require_unobstructed_direct_route=True)
    with pytest.raises(LocalityBudgetExhausted):
        create_generated_locality_fixture(LocalityRecipe("resources", budget=0))
    for value in (-1, 65536, True, "5"):
        with pytest.raises(ValueError):
            LocalityRecipe("evidence", seed=value)
    with pytest.raises(ValueError):
        LocalityRecipe("other")
    with pytest.raises(ValueError):
        LocalityRecipe("access", family="future-version")
    with pytest.raises(ValueError):
        LocalityRecipe("evidence", budget=17)
    valid = create_generated_locality_fixture(LocalityRecipe("access"))
    bad = replace(valid, material_profile=replace(valid.material_profile, actor_id="astra:entity:unqualified-actor"))
    import astra_runtime.myravant_generated_locality as generator
    monkeypatch.setattr(generator, "_build_neutral", lambda **kwargs: bad)
    with pytest.raises(InvalidLocality):
        generator.create_generated_locality_fixture(LocalityRecipe("access"))


def test_existing_state_never_regenerates_and_wrong_binding_rejects(tmp_path):
    path = tmp_path / "worksite.json"
    a, _ = build_generated_locality(LocalityRecipe("evidence", 7), path)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="restored"):
        build_generated_locality(LocalityRecipe("evidence", 7), path)
    assert path.read_bytes() == before
    with pytest.raises((ValueError, MaterialError)):
        InvestigationApplication.restore(
            fixture=create_generated_locality_fixture(LocalityRecipe("evidence", 8)),
            checkpoint_path=path)
    assert a.fixture.actors_version.startswith("investigation-neutral-generated-1")


def test_existing_neutral_root_and_history_remain_separate():
    old = create_investigation_fixture("neutral-contended")
    new = create_generated_locality_fixture(LocalityRecipe("resources"))
    assert old.provenance.fixture_id == "neutral-investigation-laboratory"
    assert old.actors_version == "investigation-neutral-1-contended"
    assert len(old.place_presentations) == 3
    assert old.provenance.canon is False
    assert old.campaign_id != new.campaign_id


def test_public_installed_routes_and_hidden_recipe_non_disclosure(tmp_path):
    path = tmp_path / "public.json"
    a, _ = build_generated_locality(LocalityRecipe("evidence"), path)
    out = io.StringIO()
    run_terminal(a, input_stream=io.StringIO(
        "help\nrecall panel a residue\ncompare reports about panel a residue\n"
        "go west\nlook\nexit\n"),
        output_stream=out, specialized_router=execute_investigation_request)
    body = out.getvalue().casefold()
    assert "received statement" in body
    assert "actor activities (noncanonical)" not in body
    assert "generated_token" not in body and "recipe_identity" not in body


def test_authored_and_generated_materials_share_the_same_owner_execution():
    authored = InvestigationApplication.new(
        fixture=create_investigation_fixture("neutral-relay"))
    generated = InvestigationApplication.new(
        fixture=create_generated_locality_fixture(LocalityRecipe("access")))
    for app in (authored, generated):
        changed(app.move("east"))
        changed(app.pickup("Plate"))
        changed(app.material("put_on", "Plate", "Bench"))
        changed(app.pickup("Peg"))
        changed(app.material("put_on", "Peg", "Bench"))
        changed(app.pickup("Cord"))
        changed(app.material("tie", "Plate", "Peg", "Cord"))
        cord = next(p.entity_id for p in app.fixture.object_presentations
                    if p.name == "Cord")
        assert len(app.connections) == 1
        assert placement(app.state.representation, cord).relation_type == "reserved_by"
        changed(app.material("untie", "Cord"))
        assert not app.connections
        assert placement(app.state.representation, cord).relation_type != "reserved_by"


def test_read_only_queries_do_not_reroll_root_or_commit_private_facts():
    fixture = create_generated_locality_fixture(LocalityRecipe("evidence", 1))
    left = InvestigationApplication.new(fixture=fixture)
    right = InvestigationApplication.new(fixture=fixture)
    root = left.fixture.provenance.initial_state_digest
    before = left.authoritative_digest()
    for query in ("panel a", "brush"):
        left.recall_history(query, "residue")
        right.compare_history(query, "residue")
    assert left.authoritative_digest() == before == right.authoritative_digest()
    assert left.fixture.provenance.initial_state_digest == root
