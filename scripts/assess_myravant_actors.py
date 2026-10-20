"""Separate objective assessment of frozen #548 goals; neither blind nor human."""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.domain.persistent_world_water_cleaning import total_water, total_residue


def tick(app):
    return app.runtime_state.logical_time_state.logical_position


def selected(app, who='oren'):
    return [r for r in app.participation_state.records if r.actor_id == identity(who)][-1]


def api_run(root, variant):
    base = create_actor_fixture()
    count = variant.get('actors', 0)
    profiles = tuple(replace(p, **({} if i < count else dict(standing_kind=None, standing_method=None,
        standing_participants=(), standing_place=None)), blocked_limit=variant.get('K', 3))
        for i, p in enumerate(base.actor_profiles))
    fixture = create_actor_fixture(actor_profiles=profiles)
    checkpoint = root / 'state.json'
    app = ActorApplication.new(fixture=fixture, checkpoint_path=checkpoint)
    calls = []

    def act(method, *args, **kwargs):
        before = tick(app)
        result = getattr(app, method)(*args, **kwargs)
        calls.append({'surface': 'public API', 'method': method, 'args': args, 'kwargs': kwargs,
            'message': result.message, 'failure': result.failure_class, 'tick_before': before,
            'tick_after': tick(app), 'digest': app.authoritative_digest()})
        return result

    def restart():
        nonlocal app
        before = app.authoritative_digest()
        app = ActorApplication.restore(fixture=fixture, checkpoint_path=checkpoint)
        assert app.authoritative_digest() == before
        calls.append({'restart_verified_digest': before})

    if variant['goal'] == 'AA01':
        # No requests are synthesized: these are independently configured standing activities.
        for _ in range(3):
            before = tick(app)
            assert act('wait').authoritative_changed
            assert tick(app) == before + 1
            restart()
        tasks = app.participation_state.records
        assert len(tasks) == count
        assert all(len(r.contributions) <= 3 for r in tasks)
        assert all(len(set(r.due_intervals)) == len(r.due_intervals) for r in tasks)
        assert len(app.intervals) == 3
        assert total_water(app.water_state) + sum(dict(app.environment_state.evaporated).values()) == 12
        assert total_residue(app.water_state) + sum(dict(app.environment_state.deposits).values()) == 7
        objectives = {'one_clock_per_interval': tick(app) == 3, 'declared_due_actor_count': len(tasks) == count,
            'one_step_per_actor_interval': all(len(r.contributions) <= len(r.due_intervals) for r in tasks),
            'restarts_preserve_full_digest': True, 'water_and_residue_conserved': True}
    elif variant['goal'] == 'AA04':
        for direction in ('south', 'west', 'west', 'west'):
            assert act('move', direction).authoritative_changed
        clock = tick(app)
        water_before = app.water_state
        assert dict(water_before.adhered)[identity('practice-panel')] > 0
        assert act('tell_actor', 'Oren Kesh', 'practice panel', 'residue', 'clear').authoritative_changed
        assert app.water_state == water_before and tick(app) == clock
        restart()
        reply = act('ask_report', 'Oren Kesh', 'practice panel', 'residue')
        assert 'reported' in reply.message and 'clear' in reply.message
        assert app.water_state == water_before and tick(app) == clock
        reports = [e for e in app.evidence_state.events if e.actor_id == identity('oren') and e.kind == 'reported']
        assert reports[-1].source_actor_id == fixture.player_entity_id and reports[-1].value == 'clear'
        restart()
        objectives = {'false_claim_is_source_qualified_report': True, 'actual_dirty_surface_unchanged': True,
            'communication_zero_time': True, 'report_provenance_survives_restart': True}
    else:
        for direction in ('south', 'west', 'west', 'west'):
            assert act('move', direction).authoritative_changed
        clock = tick(app)
        water_before = app.water_state
        assert act('request_cleaning', 'Oren Kesh', 'practice panel', 'cleaning cloth', 'wipe').authoritative_changed
        assert tick(app) == clock and app.water_state == water_before
        assert selected(app).contributions == ()
        assert placement(app.state.representation, identity('cleaning-cloth')).relation_type == 'located_at'
        restart()
        before = app.authoritative_digest()
        assert act('request_cleaning', 'Oren Kesh', 'practice panel').failure_class
        assert app.authoritative_digest() == before
        assert act('participation_control', 'Oren Kesh', 'pause').authoritative_changed
        assert act('pickup', 'cleaning cloth').authoritative_changed
        assert selected(app).blocked_due == 0 and selected(app).contributions == ()
        assert act('participation_control', 'Oren Kesh', 'resume').authoritative_changed
        K = variant['K']
        for n in range(1, K + 1):
            assert act('wait').authoritative_changed
            assert selected(app).blocked_due == n
            assert selected(app).status == ('withdrawn' if n == K else 'blocked')
            clock = tick(app)
            act('participation_status', 'Oren Kesh')
            assert tick(app) == clock and selected(app).blocked_due == n
            restart()
        old_id = selected(app).task_id
        assert act('wait').authoritative_changed
        assert selected(app).task_id == old_id and selected(app).blocked_due == K
        assert selected(app).contributions == ()
        assert placement(app.state.representation, identity('cleaning-cloth')).object_entity_id == fixture.player_entity_id
        objectives = {'acceptance_zero_time_and_no_reservation': True, 'busy_refusal_unchanged': True,
            'pause_excludes_due_interval': True, 'K_minus_one_K_K_plus_one': True,
            'zero_time_status_excluded': True, 'restart_exact_boundaries': True,
            'withdrawal_no_fake_contribution_or_material_return': True}
    return {'variant': variant, 'commands': calls, 'predicates': objectives, 'final_digest': app.authoritative_digest()}


def installed_run(root, repository_sha):
    checkpoint = root / 'installed.json'
    fixture = create_actor_fixture()
    stages = []

    def stage(commands):
        trace = root / f'installed-{len(stages)}.jsonl'
        launcher = shutil.which('myravant-play')
        assert launcher, 'installed launcher required'
        argv = [launcher, '--locality', 'tarrow-actors', '--checkpoint', str(checkpoint), '--trace', str(trace), '--repository-sha', repository_sha]
        if checkpoint.exists():
            argv.extend(('--load', str(checkpoint)))
        proc = subprocess.run(argv, input='\n'.join((*commands, 'save', 'exit', '')), capture_output=True, text=True, timeout=60)
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        records = [json.loads(line) for line in trace.read_text().splitlines()]
        assert records[-1]['evidence_complete']
        app = ActorApplication.restore(fixture=fixture, checkpoint_path=checkpoint)
        rows = [r for r in records if r['record_type'] == 'interaction']
        assert rows[-1]['post_state_digest'] == app.authoritative_digest()
        assert 'Soft-Iron Pin Blank' not in proc.stdout
        stages.append({'commands': commands, 'stdout': proc.stdout, 'records': records,
                       'restored_digest': app.authoritative_digest(), 'tick': tick(app)})
        return app, proc.stdout

    app, _ = stage(['look', 'go south', 'ask Tali Ren about work'])
    # Player is adjacent, not at Tali's qualified place; standing progress is private.
    assert 'No last communicated' in stages[-1]['stdout']
    before = tick(app)
    before_digest = app.authoritative_digest()
    app, output = stage(['ask Tali Ren about sorting board residue', 'take nonexistent object'])
    assert tick(app) == before
    refusal_rows = [r for r in stages[-1]['records'] if r.get('record_type') == 'interaction' and r.get('raw_player_input', '').strip() in {'ask Tali Ren about sorting board residue', 'take nonexistent object'}]
    assert len(refusal_rows) == 2
    assert all(r['pre_state_digest'] == r['post_state_digest'] for r in refusal_rows)
    assert 'No qualified local communication route' in output
    for _ in range(12):
        if dict(app.water_state.adhered)[identity('sorting-board')] == 0:
            break
        app, _ = stage(['wait'])
    assert dict(app.water_state.adhered)[identity('sorting-board')] == 0
    assert app.current_place_id() != identity('yard-tools')
    app, output = stage(['go west', 'ask Tali Ren about sorting board residue'])
    assert 'reports' in output.casefold() and 'clear' in output.casefold()
    reported = [e for e in app.evidence_state.events if e.kind == 'reported' and e.actor_id == fixture.player_entity_id]
    assert reported and reported[-1].source_actor_id == identity('tali') and reported[-1].source_event_id
    return {'variant': {'goal': 'AA01/AA04', 'surface': 'installed launcher'}, 'commands': stages,
        'predicates': {'remote_report_refused': True, 'refused_attempt_ticks_nothing': True,
            'absent_work_reaches_actual_clean_goal': True, 'local_later_report_sourced': True,
            'hidden_pin_not_leaked': True, 'restart_trace_digest_validated_each_stage': True},
        'final_digest': app.authoritative_digest()}


def assess(root):
    repository_sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=Path(__file__).resolve().parents[1],
        text=True, capture_output=True, check=True).stdout.strip()
    variants = [{'goal': 'AA01', 'actors': n} for n in (0, 1, 2)] + [{'goal': 'AA03', 'K': k} for k in (2, 3)] + [{'goal': 'AA04'}]
    results = []
    for variant in [*variants, None]:
        repeats = []
        for repeat in range(2):
            path = root / f'{len(results)}-{repeat}'
            path.mkdir()
            repeats.append(installed_run(path, repository_sha) if variant is None else api_run(path, variant))
        assert repeats[0]['final_digest'] == repeats[1]['final_digest']
        results.append({'repeats': repeats})
    return {'repository_sha': repository_sha, 'schema': 'myravant.actor-separate-assessment.v1', 'goals': 'tests/fixtures/tarrow_actor_assessor_goals.json',
        'authorship': 'separate assessor; frozen goals visible to implementers; neither blind nor human',
        'execution': results, 'all_executed_predicates_passed': True,
        'limits': ['Selected variants, not every frozen objective: AA02 and AA05 are not independently executed here.',
            'AA03 successful-reset and consent-policy invalidation branches rely on other certification suites.',
            'AA04 externally-satisfied and dark observer variants rely on other certification suites.',
            'Configuration variants use public API plus validated restore; stock absence/report variant uses installed launcher.',
            'This assessment does not replace mutation checks, full suites, human usability or native canon acceptance.']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='actor-assessor-') as tmp:
        report = assess(Path(tmp))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('Separate assessor: seven selected variants repeated twice; executed predicates passed; scope limits recorded.')


if __name__ == '__main__':
    main()
