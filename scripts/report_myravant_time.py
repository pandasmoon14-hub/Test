"""Implementation-authored installed time journeys; not blind or human acceptance."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_timed_application import TimedApplication
from astra_runtime.myravant_tarrow_time import create_timed_fixture
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_water_cleaning import total_water, total_residue
from astra_runtime.domain.persistent_world_material import placement


def quantity(app, field, name):
    return dict(getattr(app.water_state, field))[identity(name)]


def campaign(root, kind, head):
    checkpoint = root / 'state.json'
    stages = []
    previous = None
    previous_intervals = 0

    def stage(*commands):
        nonlocal previous, previous_intervals
        trace = root / f'{len(stages)}.jsonl'
        args = [shutil.which('myravant-play'), '--locality', 'tarrow-time',
                '--checkpoint', str(checkpoint), '--trace', str(trace), '--repository-sha', head]
        if checkpoint.exists():
            args += ['--load', str(checkpoint)]
        proc = subprocess.run(args, input='\n'.join((*commands, 'save', 'exit', '')),
                              text=True, capture_output=True, timeout=60)
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        assert '\\n' not in proc.stdout and '\\r' not in proc.stdout
        records = [json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
        assert records[-1]['evidence_complete']
        rows = [r for r in records if r['record_type'] == 'interaction']
        if previous is not None:
            assert rows[0]['pre_state_digest'] == previous
        for left, right in zip(rows, rows[1:]):
            assert left['post_state_digest'] == right['pre_state_digest']
        app = TimedApplication.restore(fixture=create_timed_fixture(), checkpoint_path=checkpoint)
        assert app.authoritative_digest() == rows[-1]['post_state_digest']
        assert len(app.intervals) == app.runtime_state.logical_time_state.logical_position
        assert [i[0] for i in app.intervals] == list(range(1, len(app.intervals) + 1))
        assert all(i[1] for i in app.intervals)
        new_intervals = app.intervals[previous_intervals:]
        timed_rows = [r for r in rows if r['logical_time_after'] is not None and r['logical_time_before'] is not None and r['logical_time_after'] > r['logical_time_before']]
        assert len(timed_rows) == len(new_intervals)
        for row, interval in zip(timed_rows, new_intervals):
            assert row['logical_time_after'] == interval[0]
            assert row['logical_time_before'] == interval[0] - 1
            assert row['due_process_ref'] == interval[1]
        for left, right in zip(app.intervals, app.intervals[1:]):
            assert left[3] == right[2]
        assert total_water(app.water_state) + sum(dict(app.environment_state.evaporated).values()) == 12
        assert total_residue(app.water_state) + sum(dict(app.environment_state.deposits).values()) == 7
        stages.append({'commands': commands, 'stdout': proc.stdout, 'stderr': proc.stderr,
                       'records': records, 'new_intervals': [list(i) for i in app.intervals[previous_intervals:]],
                       'restored_digest': app.authoritative_digest()})
        previous_intervals = len(app.intervals)
        previous = app.authoritative_digest()
        return proc.stdout, app

    if kind == 'cleaning':
        _, a = stage('go south', 'go west', 'take cleaning brush',
                     'start cleaning sorting board using cleaning brush by scrubbing', 'work', 'pause work')
        assert quantity(a, 'adhered', 'sorting-board') == 2
        _, a = stage('wait 2 steps', 'inspect work', 'resume work', 'work', 'inspect sorting board')
        goals = {'board_clean': quantity(a, 'adhered', 'sorting-board') == 0,
                 'completed_two_contributions': any(t.status == 'completed' and len(t.contributions) == 2 for t in a.work_state.tasks),
                 'observable_brushing_trace': any(t.subject == identity('sorting-board') for t in a.environment_state.traces)}
    elif kind == 'assembly':
        _, a = stage('go south', 'go west', 'go west', 'go west', 'take repair board',
                     'take repair peg', 'take repair cord', 'start assembling workshop assembly', 'work', 'pause work')
        assert not a.connections
        _, a = stage('wait 2 steps', 'resume work', 'work 2 steps', 'inspect repair board', 'inspect work')
        goals = {'actual_connection': len(a.connections) == 1,
                 'three_committed_contributions': any(t.status == 'completed' and len(t.contributions) == 3 for t in a.work_state.tasks),
                 'board_supported': placement(a.state.representation, identity('repair-board')).relation_type == 'supported_by'}
    else:
        stage('go south', 'go west', 'take barrier board', 'take barrier crossbar', 'take barrier cord',
              'start assembling passage barrier', 'work 3 steps', 'go north')
        _, a = stage('go west', 'go west', 'take cleaning cloth',
                     'soak cleaning cloth from wash bucket', 'soak cleaning cloth from wash bucket',
                     'put cleaning cloth on workroom bench')
        assert quantity(a, 'water', 'cleaning-cloth') > 0
        _, a = stage('go east', 'wait 8 steps', 'go west', 'inspect cleaning cloth', 'go east', 'go east', 'go north')
        goals = {'cloth_dry': quantity(a, 'water', 'cleaning-cloth') == 0,
                 'cloth_stays_on_support': placement(a.state.representation, identity('cleaning-cloth')).relation_type == 'supported_by',
                 'environment_accounts_evaporation': sum(dict(a.environment_state.evaporated).values()) == 2,
                 'drying_trace_persists': any(t.kind == 'drying' for t in a.environment_state.traces),
                 'separate_barrier_still_blocks': a.current_place_id() == identity('yard-tools') and len(a.connections) == 1}
    goals.update(water_conserved=total_water(a.water_state) + sum(dict(a.environment_state.evaporated).values()) == 12,
                 residue_conserved=total_residue(a.water_state) + sum(dict(a.environment_state.deposits).values()) == 7)
    assert all(goals.values()), goals
    assert all('Soft-Iron Pin Blank' not in s['stdout'] for s in stages)
    return {'profile': kind, 'objectives': goals, 'final_digest': previous, 'stages': stages}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], check=True, text=True, capture_output=True).stdout.strip()
    profiles = []
    with tempfile.TemporaryDirectory(prefix='time-evidence-') as temporary:
        for kind in ('cleaning', 'assembly', 'passive-composition'):
            runs = []
            for repeat in range(2):
                root = Path(temporary) / f'{kind}-{repeat}'
                root.mkdir()
                runs.append(campaign(root, kind, head))
            assert runs[0]['final_digest'] == runs[1]['final_digest']
            profiles.append({'profile': kind, 'repeats': runs})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({'repository_sha': head, 'implementation_authored': True,
        'not_blind_or_human_acceptance': True, 'repeat_count': 2, 'profiles': profiles}, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('Time: three authored installed journeys repeated twice; objectives, restart, interval joins and conservation passed.')


if __name__ == '__main__':
    main()
