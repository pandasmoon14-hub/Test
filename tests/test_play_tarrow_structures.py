"""#561: derived structural functions, actual reuse, exposure and replay."""
from dataclasses import replace
from fractions import Fraction
import io

import pytest

from astra_runtime.domain.persistent_world_material import active_effects, placement, MaterialError
from astra_runtime.domain.persistent_world_water_cleaning import total_water, total_residue
from astra_runtime.myravant_actor_physical import execute_actor_physical
from astra_runtime.myravant_structures_application import StructuresApplication, execute_structures_request
from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_structures import create_structures_fixture, cover_subjects
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from astra_runtime.myravant_terminal import run_terminal


def app(tmp_path=None, case="standard"):
    return StructuresApplication.new(
        fixture=create_structures_fixture(structures_case=case),
        checkpoint_path=tmp_path / "structures.json" if tmp_path else None)


def changed(result):
    assert result.authoritative_changed, result.message
    return result


def go(a, *steps):
    for direction in steps:
        changed(a.move(direction))


def take_on(a, thing, support):
    changed(a.pickup(thing))
    changed(a.material("put_on", thing, support))


def yard(a):
    go(a, "south", "west")


def erect_partition(a):
    yard(a)
    take_on(a, "work panel", "yard work trestle")
    take_on(a, "barrier crossbar", "yard work trestle")
    changed(a.pickup("work cord"))
    changed(a.material("tie", "work panel", "barrier crossbar", "work cord"))


def tally(a):
    return (total_water(a.water_state) + sum(v for _, v in a.environment_state.evaporated),
            total_residue(a.water_state) + sum((v for _, v in a.environment_state.deposits), Fraction(0)))


def test_same_whole_stock_is_reconfigured_into_two_different_functions(tmp_path):
    a = app(tmp_path)
    erect_partition(a)
    assert a.move("north").failure_class == "material_passage_obstructed"
    assert not any(e.kind == "sight" and e.source == identity("common-threshold")
                   for e in active_effects(a.state.representation, a.connections, a.material_profile))
    changed(a.material("untie", "work cord"))
    changed(a.material("lift_from", "work panel", "yard work trestle"))
    assert placement(a.state.representation, identity("work-cord")).object_entity_id == a.fixture.player_entity_id
    # The panel and cord are transported by ordinary player movement, not cloned.
    go(a, "east", "north", "east", "east")
    changed(a.material("put_on", "work panel", "document box"))
    changed(a.material("tie", "work panel", "notice board", "work cord"))
    assert len([c for c in a.connections if c.fastener == identity("work-cord")]) == 1
    go(a, "west")
    assert a.look_direction("east").failure_class == "material_sightline_obstructed"
    changed(a.move("east"))  # Screen is not a movement barrier.
    changed(a.material("untie", "work cord"))
    go(a, "west")
    assert a.look_direction("east").failure_class != "material_sightline_obstructed"
    b = StructuresApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()
    assert b.connections == a.connections and b.intervals == a.intervals


def test_effect_variant_changes_actual_edge_without_changing_material_reducer():
    a = app(case="cross-workshop")
    erect_partition(a)
    assert a.move("west").failure_class == "material_passage_obstructed"
    assert a.move("north").authoritative_changed
    b = app()
    erect_partition(b)
    assert b.move("north").failure_class == "material_passage_obstructed"
    assert b.move("west").authoritative_changed


def test_actor_uses_same_live_partition_and_cannot_bypass_player_block():
    a = app()
    erect_partition(a)
    before = a.authoritative_digest()
    result = execute_actor_physical(a, identity("tali"), "move", identity("yard-sorting"))
    assert not result.authoritative_changed
    assert a.authoritative_digest() == before
    changed(a.material("untie", "work cord"))
    changed(execute_actor_physical(a, identity("tali"), "move", identity("yard-sorting")))


def prepare_cover(a, connected=True):
    yard(a)
    take_on(a, "barrier crossbar", "yard work trestle")
    take_on(a, "cover cloth", "yard work trestle")
    changed(a.pickup("cover tie"))
    if connected:
        changed(a.material("tie", "cover cloth", "barrier crossbar", "cover tie"))
    else:
        changed(a.wait())  # Equal number of intervals, unconnected cloth.
    go(a, "west", "west")
    changed(a.pickup("packing felt"))
    changed(a.pickup("wash bucket"))
    go(a, "east", "east")
    changed(a.water("soak", "wash bucket", "packing felt"))
    changed(a.material("put_on", "packing felt", "yard work trestle"))


def test_cover_reduces_only_qualified_drying_with_conserved_compartments(tmp_path):
    covered, aired = app(tmp_path), app()
    prepare_cover(covered)
    prepare_cover(aired, connected=False)
    assert covered.runtime_state.logical_time_state.logical_position == aired.runtime_state.logical_time_state.logical_position
    assert identity("packing-felt") in cover_subjects(covered.state.representation, covered.connections, covered.fixture.cover_profile)
    assert not cover_subjects(aired.state.representation, aired.connections, aired.fixture.cover_profile)
    start = tally(covered)
    for _ in range(4):
        changed(covered.wait())
        changed(aired.wait())
    assert dict(covered.water_state.water)[identity("packing-felt")] > dict(aired.water_state.water)[identity("packing-felt")]
    assert tally(covered) == tally(aired) == start
    b = StructuresApplication.restore(fixture=covered.fixture, checkpoint_path=covered.checkpoint_path)
    assert b.authoritative_digest() == covered.authoritative_digest()
    changed(b.material("untie", "cover tie"))
    assert not cover_subjects(b.state.representation, b.connections, b.fixture.cover_profile)
    assert tally(b) == start


def test_cover_no_passive_water_contact_and_no_loss_from_storage():
    a = app()
    prepare_cover(a)
    before = tally(a)
    assert identity("packing-felt") in cover_subjects(a.state.representation, a.connections, a.fixture.cover_profile)
    changed(a.wait())
    assert tally(a) == before
    assert dict(a.water_state.water)[identity("practice-panel")] == 0


def test_invalid_cover_profile_and_mutually_incompatible_partitions_fail_closed():
    f = create_structures_fixture()
    with pytest.raises(ValueError):
        replace(f.cover_profile, fastener=identity("work-cord")).validate(f)
    with pytest.raises(ValueError):
        replace(f.cover_profile, rate=Fraction(2)).validate(f)
    with pytest.raises(ValueError):
        create_structures_fixture(structures_case="unbounded")
    a = app()
    erect_partition(a)
    before = a.authoritative_digest()
    assert not a.material("tie", "work panel", "notice board", "work cord").authoritative_changed
    assert not a.material("lift_from", "work panel", "yard work trestle").authoritative_changed
    assert a.authoritative_digest() == before


def test_preexisting_surface_binding_and_checkpoint_are_unchanged(tmp_path):
    first = create_surface_fixture()
    assert first.provenance.fixture_version.startswith("surface-water-1-")
    assert len([p for p in first.object_presentations if p.name == "Work Panel"]) == 0
    a = app(tmp_path)
    erect_partition(a)
    with pytest.raises(MaterialError) as err:
        SurfaceWaterApplication.restore(fixture=create_surface_fixture(), checkpoint_path=a.checkpoint_path)
    assert err.value is not None
    assert create_structures_fixture().provenance.fixture_version != first.provenance.fixture_version


def test_player_terminal_uses_real_owner_method_and_help():
    a = app()
    output = io.StringIO()
    run_terminal(a, input_stream=io.StringIO(
        "help\ngo south\ngo west\ntake work panel\nput work panel on yard work trestle\n"
        "take barrier crossbar\nput barrier crossbar on yard work trestle\n"
        "take work cord\ntie work panel to barrier crossbar using work cord\n"
        "go north\nexit\n"),
        output_stream=output, specialized_router=execute_structures_request)
    assert "drying cover" in output.getvalue()
    assert "obstructs" in output.getvalue()
    assert len(a.connections) == 1
