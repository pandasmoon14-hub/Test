"""Time/material edge behavior at the declared owner boundaries (#546)."""
from dataclasses import replace
from fractions import Fraction

import pytest

from astra_runtime.domain import persistent_world_timed_environment as environment
from astra_runtime.domain import persistent_world_water_cleaning as water
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_time import create_timed_fixture
from astra_runtime.myravant_timed_application import TimedApplication


def changed(result):
    assert result.authoritative_changed, result.message
    return result


def quantity(state, field, key):
    return dict(getattr(state, field))[identity(key)]


def domain_case():
    fixture = create_timed_fixture()
    cloth = identity('cleaning-cloth')
    bucket = identity('wash-bucket')
    state = fixture.water_initial
    state = replace(state,
        water=tuple((key, 1 if key == cloth else 3 if key == bucket else value) for key, value in state.water),
        adhered=tuple((key, Fraction(2) if key == cloth else value) for key, value in state.adhered),
        suspended=tuple((key, Fraction(5) if key == cloth else value) for key, value in state.suspended))
    profile = environment.TimedEnvironmentProfile((cloth,), (('room', Fraction(1, 4), 'sheltered'),))
    return fixture, state, profile, environment.initial_environment(profile)


def conserved(before, initial_env, after, final_env):
    assert water.total_water(before) + sum(dict(initial_env.evaporated).values()) == water.total_water(after) + sum(dict(final_env.evaporated).values())
    assert water.total_residue(before) + sum(dict(initial_env.deposits).values()) == water.total_residue(after) + sum(dict(final_env.deposits).values())


@pytest.mark.parametrize('recovery', ['rinse', 'collect'])
def test_complete_drying_preserves_excess_deposit_and_allows_recovery(recovery):
    fixture, original, profile, initial_env = domain_case()
    cloth = identity('cleaning-cloth')
    state, env = original, initial_env
    for tick in range(1, 4):
        state, env = environment.advance_environment(state, env, profile, {cloth: 'room'}, tick, f'interval-{tick}')
        assert quantity(state, 'water', 'cleaning-cloth') == 1
        assert dict(env.credits)[cloth] == Fraction(tick, 4)
        assert dict(env.deposits)[cloth] == 0
    state, env = environment.advance_environment(state, env, profile, {cloth: 'room'}, 4, 'interval-4')
    assert quantity(state, 'water', 'cleaning-cloth') == 0
    assert quantity(state, 'suspended', 'cleaning-cloth') == 0
    assert quantity(state, 'adhered', 'cleaning-cloth') == 2
    assert dict(env.deposits)[cloth] == 5  # Deposits survive beyond the working capacity of two.
    assert dict(env.credits)[cloth] == 0
    conserved(original, initial_env, state, env)
    wet_state, wet_env = environment.execute_with_deposits(
        state, env, fixture.water_profile, 'soak', (identity('wash-bucket'), cloth))
    assert quantity(wet_state, 'water', 'cleaning-cloth') > 0
    with pytest.raises(water.WaterCleaningRefusal):
        environment.execute_with_deposits(wet_state, wet_env, fixture.water_profile, 'wipe', (identity('practice-panel'), cloth))
    recipient = identity('wash-bucket' if recovery == 'rinse' else 'debris-tray')
    state, env = environment.execute_with_deposits(state, env, fixture.water_profile, recovery, (cloth, recipient))
    assert dict(env.deposits)[cloth] == 0
    assert quantity(state, 'adhered', 'cleaning-cloth') == 0
    field = 'suspended' if recovery == 'rinse' else 'adhered'
    assert dict(getattr(state, field))[recipient] == 7
    conserved(original, initial_env, state, env)


def test_closed_exposure_freezes_earned_credit_until_reexposed():
    _, state, profile, env = domain_case()
    cloth = identity('cleaning-cloth')
    state, env = environment.advance_environment(state, env, profile, {cloth: 'room'}, 1, 'open-1')
    before = (state, env)
    for tick in range(2, 8):
        state, env = environment.advance_environment(state, env, profile, {cloth: None}, tick, f'closed-{tick}')
        assert (state, env) == before
    state, env = environment.advance_environment(state, env, profile, {cloth: 'room'}, 8, 'open-8')
    assert dict(env.credits)[cloth] == Fraction(1, 2)
    assert quantity(state, 'water', 'cleaning-cloth') == 1


def test_condition_boundary_changes_only_following_interval_rate():
    _, state, _, _ = domain_case()
    cloth = identity('cleaning-cloth')
    profile = environment.TimedEnvironmentProfile((cloth,), (('room', Fraction(1, 4), 'sheltered'),),
                                                  ((2, 'room', Fraction(1, 2), 'aired'),))
    env = environment.initial_environment(profile)
    for tick in (1, 2):
        state, env = environment.advance_environment(state, env, profile, {cloth: 'room'}, tick, f'interval-{tick}')
        assert dict(env.credits)[cloth] == Fraction(tick, 4)
        assert quantity(state, 'water', 'cleaning-cloth') == 1
    state, env = environment.advance_environment(state, env, profile, {cloth: 'room'}, 3, 'interval-3')
    assert quantity(state, 'water', 'cleaning-cloth') == 0
    assert dict(env.evaporated)['room'] == 1


def app():
    return TimedApplication.new(fixture=create_timed_fixture())


def tick(a):
    return a.runtime_state.logical_time_state.logical_position


def workshop(a):
    for direction in ('south', 'west', 'west', 'west'):
        changed(a.move(direction))


def test_last_water_can_interrupt_contribution_but_initial_dry_refusal_takes_no_time():
    a = app()
    workshop(a)
    changed(a.pickup('cleaning cloth'))
    changed(a.water('soak', 'wash bucket', 'cleaning cloth'))
    changed(a.wait())
    changed(a.wait())
    changed(a.wait())
    assert dict(a.environment_state.credits)[identity('cleaning-cloth')] == Fraction(3, 4)
    changed(a.start_cleaning('practice panel', 'cleaning cloth'))
    panel_before = quantity(a.water_state, 'adhered', 'practice-panel')
    start = tick(a)
    result = changed(a.work_step())
    assert result.failure_class == 'timed_action_interrupted'
    assert tick(a) == start + 1
    assert quantity(a.water_state, 'water', 'cleaning-cloth') == 0
    assert quantity(a.water_state, 'adhered', 'practice-panel') == panel_before
    assert a.work_state.tasks[-1].contributions == ()
    before = a.authoritative_digest()
    result = a.water('wipe', 'practice panel', 'cleaning cloth')
    assert not result.authoritative_changed
    assert tick(a) == start + 1 and a.authoritative_digest() == before


def test_three_assembly_steps_commit_actual_supports_then_connection():
    a = app()
    workshop(a)
    for obj in ('repair board', 'repair peg', 'repair cord'):
        changed(a.pickup(obj))
    changed(a.start_assembly('workshop assembly'))
    start = tick(a)
    for index in (1, 2):
        changed(a.work_step())
        assert len(a.work_state.tasks[-1].contributions) == index
        assert not a.connections and a.work_state.tasks[-1].status == 'active'
    changed(a.work_step())
    assert tick(a) == start + 3
    assert len(a.connections) == 1 and a.work_state.tasks[-1].status == 'completed'
    before = a.authoritative_digest()
    assert not a.work_step().authoritative_changed
    assert a.authoritative_digest() == before


def test_approach_delegating_to_move_commits_only_one_interval():
    a = app()
    start = tick(a)
    changed(a.approach_place('service yard'))
    assert tick(a) == start + 1
    assert len(a.intervals) == 1
    assert a.current_place_id() == identity('yard')
