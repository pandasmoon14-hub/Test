"""#559 NPC/NPC competition without duplicated stock, for both declared orderings."""
from fractions import Fraction
import pytest

from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication
from astra_runtime.domain.persistent_world_actor_participation import selected


@pytest.mark.parametrize("reverse", [False, True])
def test_two_voluntary_actors_compete_over_same_finite_surface(reverse):
    a = SurfaceWaterApplication.new(fixture=create_surface_fixture(
        reverse_order=reverse, shared_workbench=True))
    for direction in ("south", "west", "west", "west"):
        assert a.move(direction).authoritative_changed
    assert a.pickup("wash bucket").authoritative_changed
    assert a.water("spill", "wash bucket", "practice panel", amount=3).authoritative_changed
    assert a.request_blotting("oren kesh", "practice panel", "cleaning cloth").authoritative_changed
    assert a.request_blotting("tali ren", "practice panel", "packing felt").authoritative_changed
    assert dict(a.water_state.water)[identity("practice-panel")] == 3
    for _ in range(5):
        if dict(a.water_state.water)[identity("practice-panel")] == 0:
            break
        assert a.wait().authoritative_changed
    assert dict(a.water_state.water)[identity("practice-panel")] == 0
    jobs = [selected(a.participation_state, identity(n)) for n in ("oren", "tali")]
    # Both had to prepare real tools and contribute through RT-010, but the
    # declared resolution order decides which actor completes the final stock.
    assert all(job.contributions for job in jobs)
    assert sum(v for _, v in a.water_state.water) + sum(
        v for _, v in a.environment_state.evaporated) == 12
    assert (sum((v for _, v in a.water_state.adhered), Fraction(0))
            + sum((v for _, v in a.water_state.suspended), Fraction(0))
            + sum((v for _, v in a.environment_state.deposits), Fraction(0))) == 7
    assert sum(job.status == "completed" for job in jobs) == 1
