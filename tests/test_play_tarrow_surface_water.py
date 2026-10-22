"""PLAY-TARROW-WATER-2: finite surface water and deliberate contact regression."""
from fractions import Fraction
import io
import pytest

from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication, execute_surface_water_request
from astra_runtime.myravant_tarrow_surface_water import create_surface_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_water_application import WaterApplication, parse_water
from astra_runtime.myravant_tarrow_water import create_water_fixture
from astra_runtime.myravant_terminal import run_terminal
from astra_runtime.domain.persistent_world_water_cleaning import total_water, total_residue


def app(tmp_path=None, reverse=False):
    return SurfaceWaterApplication.new(
        fixture=create_surface_fixture(reverse_order=reverse),
        checkpoint_path=tmp_path / "water.json" if tmp_path else None)


def workshop(a):
    for direction in ("south", "west", "west", "west"):
        r = a.move(direction)
        assert r.authoritative_changed, r.message


def take(a, *names):
    for name in names:
        r = a.pickup(name)
        assert r.authoritative_changed, r.message


def count(a):
    # Independent read of compartments: does not call tested reducer.
    return (total_water(a.water_state) + sum(v for _, v in a.environment_state.evaporated),
            total_residue(a.water_state) + sum((v for _, v in a.environment_state.deposits), Fraction(0)))


def amount(a, name, kind="water"):
    return dict(getattr(a.water_state, kind))[identity(name)]


def act(a, method, *refs, amount=None):
    before = count(a)
    r = a.water(method, *refs, amount=amount)
    assert r.authoritative_changed, r.message
    assert count(a) == before
    return r


def test_recovery_scoop_blot_wring_and_durable_restart(tmp_path):
    a = app(tmp_path)
    workshop(a)
    take(a, "wash bucket", "pouring jug", "packing felt")
    assert count(a) == (12, Fraction(7))
    act(a, "spill", "wash bucket", "practice panel", amount=3)
    act(a, "scoop", "practice panel", "pouring jug")
    assert amount(a, "practice-panel") == 1
    assert amount(a, "pouring-jug") == 2
    act(a, "blot", "practice panel", "packing felt")
    assert amount(a, "practice-panel") == 0
    act(a, "wring", "packing felt", "wash bucket")
    assert amount(a, "packing-felt") == 0
    assert count(a) == (12, Fraction(7))
    b = SurfaceWaterApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()
    assert b.intervals == a.intervals and b.journal == a.journal


def test_rates_and_no_unapproved_contact_or_surface_cleaning():
    a = app()
    workshop(a)
    take(a, "wash bucket", "cleaning cloth", "packing felt")
    act(a, "spill", "wash bucket", "practice panel", amount=3)
    act(a, "blot", "practice panel", "cleaning cloth")
    assert amount(a, "practice-panel") == 2
    before = amount(a, "cleaning-cloth")
    assert a.look().failure_class is None
    assert amount(a, "cleaning-cloth") == before
    act(a, "blot", "practice panel", "packing felt")
    assert amount(a, "practice-panel") == 0
    assert amount(a, "practice-panel", "adhered") == 3
    act(a, "press", "packing felt", "cleaning cloth")
    assert amount(a, "cleaning-cloth") == 2
    assert count(a) == (12, Fraction(7))


def test_overcapacity_refuses_atomically_and_does_not_advance_clock():
    a = app()
    workshop(a)
    take(a, "wash bucket")
    pre = a.authoritative_digest()
    tick = a.runtime_state.logical_time_state.logical_position
    for n in (0, -1, 4, 13, True):
        result = a.water("spill", "wash bucket", "practice panel", amount=n)
        assert not result.authoritative_changed
        assert a.authoritative_digest() == pre
        assert a.runtime_state.logical_time_state.logical_position == tick


def test_actor_blotting_is_consumptive_participation(tmp_path):
    a = app(tmp_path)
    workshop(a)
    take(a, "wash bucket")
    act(a, "spill", "wash bucket", "practice panel", amount=2)
    result = a.request_blotting("oren", "practice panel", "cleaning cloth")
    assert result.authoritative_changed, result.message
    assert amount(a, "practice-panel") == 2
    for _ in range(6):
        if amount(a, "practice-panel") == 0:
            break
        assert a.wait().authoritative_changed
    assert amount(a, "practice-panel") == 0
    task = next(t for t in a.participation_state.records if t.actor_id == identity("oren"))
    assert task.status == "completed" and task.contributions
    restored = SurfaceWaterApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert restored.authoritative_digest() == a.authoritative_digest()


def test_parser_routes_and_legacy_profile():
    assert parse_water("pour 2 units from wash bucket onto practice panel") == (
        "spill", ("wash bucket", "practice panel"), 2)
    assert parse_water("blot practice panel using packing felt") == (
        "blot", ("practice panel", "packing felt"), None)
    assert parse_water("scoop from practice panel into pouring jug") == (
        "scoop", ("practice panel", "pouring jug"), None)
    assert parse_water("press packing felt against cleaning cloth") == (
        "press", ("packing felt", "cleaning cloth"), None)
    old = WaterApplication.new(fixture=create_water_fixture())
    assert all(x.water_capacity == 0 for x in old.water_profile.assets if x.kind == "surface")
    assert not old.water("spill", "wash bucket", "practice panel", amount=1).authoritative_changed


def test_player_public_terminal_stores_actual_surface_water():
    a = app()
    out = io.StringIO()
    run_terminal(a, input_stream=io.StringIO(
        "go south\ngo west\ngo west\ngo west\ntake wash bucket\n"
        "pour 2 units from wash bucket onto practice panel\ninspect practice panel\nexit\n"),
        output_stream=out, specialized_router=execute_surface_water_request)
    assert amount(a, "practice-panel") == 2, out.getvalue()
    assert "Water: 2/3" in out.getvalue()


@pytest.mark.parametrize("reverse", [False, True])
def test_ordered_actor_profiles_retain_one_water_ledger(reverse):
    a = app(reverse=reverse)
    for _ in range(3):
        assert a.wait().authoritative_changed
    assert count(a) == (12, Fraction(7))
