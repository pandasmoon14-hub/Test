"""Implementation-authored installed actor campaigns; not blind/human acceptance."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.domain.persistent_world_water_cleaning import total_water, total_residue


def campaign(root, kind, head):
    campaign_started = time.perf_counter()
    checkpoint = root / 'state.json'
    stages = []
    previous_tick = 0

    def stage(*commands):
        nonlocal previous_tick
        trace = root / f'{len(stages)}.jsonl'
        launcher = shutil.which('myravant-play')
        if launcher is None:
            raise RuntimeError('installed myravant-play launcher required')
        args = [launcher, '--locality', 'tarrow-actors', '--checkpoint', str(checkpoint),
                '--trace', str(trace), '--repository-sha', head]
        if checkpoint.exists():
            args.extend(('--load', str(checkpoint)))
        started = time.perf_counter()
        proc = subprocess.run(args, input='\n'.join((*commands, 'save', 'exit', '')),
                              text=True, capture_output=True, timeout=60)
        installed_seconds = time.perf_counter() - started
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        records = [json.loads(line) for line in trace.read_text().splitlines()]
        assert records[-1]['evidence_complete']
        rows = [r for r in records if r['record_type'] == 'interaction']
        for row in rows:
            command = row['raw_player_input'].strip().casefold()
            if command.startswith('ask ') and ' for ' not in command:
                before, after = row['logical_time_before'], row['logical_time_after']
                assert before == after, 'participation/report metadata advanced world time'
        for left, right in zip(rows, rows[1:]):
            assert left['post_state_digest'] == right['pre_state_digest']
        restore_started = time.perf_counter()
        app = ActorApplication.restore(fixture=create_actor_fixture(), checkpoint_path=checkpoint)
        restore_seconds = time.perf_counter() - restore_started
        assert app.authoritative_digest() == rows[-1]['post_state_digest']
        tick = app.runtime_state.logical_time_state.logical_position
        timed = [r for r in rows if r['logical_time_after'] is not None and r['logical_time_before'] is not None and r['logical_time_after'] > r['logical_time_before']]
        assert len(timed) == tick - previous_tick
        assert len(app.intervals) == tick
        for row, interval in zip(timed, app.intervals[previous_tick:]):
            assert row['logical_time_before'] == interval[0] - 1
            assert row['logical_time_after'] == interval[0]
            assert row['due_process_ref'] == interval[1]
        assert total_water(app.water_state) + sum(dict(app.environment_state.evaporated).values()) == 12
        assert total_residue(app.water_state) + sum(dict(app.environment_state.deposits).values()) == 7
        assert 'Soft-Iron Pin Blank' not in proc.stdout
        stages.append({'commands': list(commands), 'stdout': proc.stdout, 'stderr': proc.stderr,
                       'records': records, 'tick_before': previous_tick, 'tick_after': tick,
                       'installed_seconds': installed_seconds, 'verification_restore_seconds': restore_seconds,
                       'restored_digest': app.authoritative_digest()})
        previous_tick = tick
        return proc.stdout, app

    def until(predicate, app, limit=20):
        remaining = limit
        while remaining:
            if predicate(app):
                return app
            # Material objectives tolerate a bounded two-interval observation
            # cadence. Exact due/withdrawal boundaries have dedicated tests.
            steps = min(2, remaining)
            _, app = stage(f'wait {steps} steps')
            remaining -= steps
        assert predicate(app), 'bounded adaptive objective remained unmet'
        return app

    def own_task(app, actor):
        return [t for t in app.participation_state.records if t.actor_id == identity(actor)][-1]

    _, app = stage('go south')
    if kind == 'absent-cleanup':
        app = until(lambda a: dict(a.water_state.adhered)[identity('sorting-board')] == 0, app)
        assert app.current_place_id() != identity('yard-tools')
        text, app = stage('go west', 'inspect sorting board', 'ask Tali Ren about sorting board residue')
        task = own_task(app, 'tali')
        report_tick = app.runtime_state.logical_time_state.logical_position
        _, app = stage('ask Tali Ren for cleaning brush')
        brush = placement(app.state.representation, identity('cleaning-brush'))
        objectives = {'real_board_clear': dict(app.water_state.adhered)[identity('sorting-board')] == 0,
                      'tali_contributions_attributed': task.status == 'completed' and bool(task.contributions),
                      'lawful_later_report': 'reports' in text.casefold() and 'clear' in text.casefold(),
                      'not_a_live_remote_view': any(e.kind == 'reported' and e.actor_id == app.fixture.player_entity_id for e in app.evidence_state.events),
                      'agreed_material_return': brush.relation_type == 'carried_by' and brush.object_entity_id == app.fixture.player_entity_id,
                      'return_is_one_physical_interval': app.runtime_state.logical_time_state.logical_position == report_tick + 1,
                      'return_performer_attributed': any(e[1] == 'physical_return' and e[2] == identity('tali') for e in app.actor_events)}
    else:
        app = until(lambda a: own_task(a, 'oren').status in {'completed', 'satisfied', 'withdrawn'}, app)
        _, app = stage('go west', 'go west', 'go west')
        if kind == 'cooperative-assembly':
            text, app = stage('ask Oren Kesh to assemble workshop assembly', 'take repair board')
            task = own_task(app, 'oren')
            assert task.kind == 'assembly', text
            # The player's earlier custody transition defeats the actor's prepared pickup.
            assert task.status == 'blocked'
            _, app = stage('put repair board on workroom bench')
            app = until(lambda a: bool(a.connections), app)
            task = own_task(app, 'oren')
            text, app = stage('ask Oren Kesh about work', 'inspect repair board')
            objectives = {'actual_join': any(c.left == identity('repair-board') for c in app.connections),
                          'player_support_preserved': placement(app.state.representation, identity('repair-board')).relation_type == 'supported_by',
                          'actor_completed_remaining_steps': task.status == 'completed' and bool(task.contributions),
                          'contention_did_not_duplicate_board': sum(r.subject_entity_id == identity('repair-board') for r in app.state.representation.relations) == 1}
        else:
            text, app = stage('ask Oren Kesh about repair board placement')
            assert 'reports' in text.casefold(), text
            _, app = stage('take repair board', 'go east')
            remote, app = stage('ask Oren Kesh about repair board placement')
            assert 'No qualified local communication route' in remote
            text, app = stage('go west', 'ask Oren Kesh about repair board placement')
            reports = [e for e in app.evidence_state.events if e.actor_id == app.fixture.player_entity_id and e.kind == 'reported' and e.target_id == identity('repair-board') and e.facet == 'placement']
            latest = reports[-1]
            actual = placement(app.state.representation, identity('repair-board'))
            objectives = {'actual_board_carried_by_player': actual.relation_type == 'carried_by' and actual.object_entity_id == app.fixture.player_entity_id,
                          'historical_report_not_refreshed': latest.value != (actual.relation_type, actual.object_entity_id),
                          'source_attributed': latest.source_actor_id == identity('oren') and bool(latest.source_event_id),
                          'truthful_stale_presentation': 'not a fresh inspection' in text,
                          'remote_inquiry_refused': 'No qualified local communication route' in remote}
    assert all(objectives.values()), objectives
    return {'kind': kind, 'objectives': objectives, 'final_digest': app.authoritative_digest(),
            'elapsed_seconds': time.perf_counter() - campaign_started, 'stages': stages}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], text=True, capture_output=True, check=True).stdout.strip()
    profiles = []
    with tempfile.TemporaryDirectory(prefix='actor-campaigns-') as temporary:
        for kind in ('absent-cleanup', 'cooperative-assembly', 'stale-evidence'):
            runs = []
            for repeat in range(2):
                root = Path(temporary) / f'{kind}-{repeat}'; root.mkdir()
                runs.append(campaign(root, kind, head))
            assert runs[0]['final_digest'] == runs[1]['final_digest']
            profiles.append({'profile': kind, 'repeats': runs})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'repository_sha': head, 'implementation_authored': True,
        'not_blind_or_human_acceptance': True, 'repeat_count': 2, 'profiles': profiles}, indent=2, sort_keys=True) + '\n')
    print('Actors: three adaptive installed campaigns repeated twice; material, attribution, restart and interval objectives passed.')


if __name__ == '__main__':
    main()
