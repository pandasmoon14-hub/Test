"""#559 adversarial capacities, material conservation, exposure and compatibility."""
from dataclasses import replace
from fractions import Fraction
import json
import pytest

from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication
from astra_runtime.myravant_water_application import WaterApplication
from astra_runtime.myravant_tarrow_water import create_water_fixture
from astra_runtime.domain.persistent_world_water_cleaning import (
    WaterCleaningAsset, WaterCleaningProfile, WaterCleaningState, execute, validate,
    canonical_state, total_residue,
)
from astra_runtime.domain.persistent_world_material import digest, MaterialError


def test_dirty_liquid_fraction_cannot_disappear_or_become_pure_by_contact():
    fixture = create_surface_fixture()
    state = fixture.water_initial
    mixed = dict(state.suspended)
    mixed[identity("wash-bucket")] = Fraction(3, 2)
    state = WaterCleaningState(state.water, state.adhered, tuple(mixed.items()))
    before = total_residue(state)
    state = execute(state, fixture.water_profile, "spill",
                    (identity("wash-bucket"), identity("practice-panel")), 3)
    assert dict(state.suspended)[identity("practice-panel")] == Fraction(3, 8)
    state = execute(state, fixture.water_profile, "scoop",
                    (identity("practice-panel"), identity("pouring-jug")))
    assert dict(state.suspended)[identity("pouring-jug")] == Fraction(1, 4)
    state = execute(state, fixture.water_profile, "blot",
                    (identity("practice-panel"), identity("packing-felt")))
    assert dict(state.suspended)[identity("packing-felt")] == Fraction(1, 8)
    assert total_residue(state) == before
    assert dict(state.adhered)[identity("practice-panel")] == 3


def test_surface_profile_rejects_invalid_identity_capacity_and_pairs():
    fixture = create_surface_fixture()
    profile = fixture.water_profile
    with pytest.raises(ValueError):
        WaterCleaningAsset("ghost", "puddle", 1)
    with pytest.raises(ValueError):
        WaterCleaningAsset("ghost", "surface", -1)
    with pytest.raises(ValueError):
        WaterCleaningProfile((*profile.assets, profile.assets[0]), profile.allowed_pairs)
    with pytest.raises(ValueError):
        WaterCleaningProfile(profile.assets, (*profile.allowed_pairs,
                                                ("spill", "ghost", identity("practice-panel"))))
    missing = WaterCleaningState(fixture.water_initial.water[:-1],
                                 fixture.water_initial.adhered,
                                 fixture.water_initial.suspended)
    with pytest.raises(ValueError):
        validate(missing, profile)


def test_surface_evaporation_not_inferred_from_cloth_exposure():
    a = SurfaceWaterApplication.new(fixture=create_surface_fixture())
    for direction in ("south", "west", "west", "west"):
        assert a.move(direction).authoritative_changed
    assert a.pickup("wash bucket").authoritative_changed
    assert a.water("spill", "wash bucket", "practice panel", amount=2).authoritative_changed
    for _ in range(12):
        assert a.wait().authoritative_changed
    assert dict(a.water_state.water)[identity("practice-panel")] == 2
    assert set(dict(a.environment_state.credits)) == {
        identity("cleaning-cloth"), identity("packing-felt")}


def test_stale_and_remote_surface_cannot_be_changed():
    a = SurfaceWaterApplication.new(fixture=create_surface_fixture())
    before = a.authoritative_digest()
    for operation, refs in (("scoop", ("practice panel", "pouring jug")),
                            ("blot", ("practice panel", "packing felt"))):
        result = a.water(operation, *refs)
        assert result.failure_class and not result.authoritative_changed
        assert a.authoritative_digest() == before
        assert "3/3" not in result.message


@pytest.mark.parametrize("kind", ["profile", "final", "journal", "extra"])
def test_resealed_surface_checkpoint_refuses_forged_history(tmp_path, kind):
    fixture = create_surface_fixture()
    path = tmp_path / "checkpoint.json"
    a = SurfaceWaterApplication.new(fixture=fixture, checkpoint_path=path)
    assert a.wait().authoritative_changed
    env = json.loads(path.read_text())
    data = env["payload"]
    if kind == "profile":
        data["profile"]["surface_policy"] = "unapproved"
    elif kind == "final":
        data["final"] = "0" * 64
    elif kind == "journal":
        data["journal"] = []
    else:
        data["secret_surface"] = {"water": 99}
    env["integrity_digest"] = digest(data)
    path.write_text(json.dumps(env))
    with pytest.raises(MaterialError):
        SurfaceWaterApplication.restore(fixture=fixture, checkpoint_path=path)


def test_old_profile_and_versioned_surface_root_do_not_interchange(tmp_path):
    old = WaterApplication.new(fixture=create_water_fixture(),
                               checkpoint_path=tmp_path / "old.json")
    assert old.pickup("wash bucket").failure_class is not None
    assert old.wait().authoritative_changed
    surface = SurfaceWaterApplication.new(fixture=create_surface_fixture(),
                                           checkpoint_path=tmp_path / "surface.json")
    assert surface.wait().authoritative_changed
    with pytest.raises(MaterialError):
        SurfaceWaterApplication.restore(fixture=surface.fixture,
                                        checkpoint_path=old.checkpoint_path)
    with pytest.raises(MaterialError):
        WaterApplication.restore(fixture=old.fixture,
                                 checkpoint_path=surface.checkpoint_path)
