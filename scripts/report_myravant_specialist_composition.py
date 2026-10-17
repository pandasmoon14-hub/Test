"""Authored #536 feedback-conditioned installed campaigns; not blind/human play."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from astra_runtime.myravant_vsm14_application import MyravantVSM14Application as App
from astra_runtime.myravant_play_fixture import WORKSHOP_ID, YARD_ID, GROUNDSKEEPER_ID, LANTERN_ID


def campaign(root, kind, head):
    checkpoint = root / 'world.json'
    stages = []
    previous = None
    branches = []
    def stage(*commands):
        nonlocal previous
        trace = root / f'{len(stages)}.jsonl'
        args = [shutil.which('myravant-play'), '--checkpoint', str(checkpoint), '--trace', str(trace), '--repository-sha', head]
        if checkpoint.exists():
            args += ['--load', str(checkpoint)]
        proc = subprocess.run(args, input='\n'.join((*commands, 'save', 'exit', '')), text=True, capture_output=True, timeout=90)
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        records = [json.loads(line) for line in trace.read_text(encoding='utf-8').splitlines()]
        assert records[-1]['record_type'] == 'session_end' and records[-1]['evidence_complete']
        rows = [r for r in records if r['record_type'] == 'interaction']
        if previous is not None:
            assert rows[0]['pre_state_digest'] == previous
        for a, b in zip(rows, rows[1:]):
            assert a['post_state_digest'] == b['pre_state_digest']
        app = App.restore(checkpoint_path=checkpoint)
        assert app.authoritative_digest() == rows[-1]['post_state_digest']
        previous = app.authoritative_digest()
        stages.append({'commands': commands, 'stdout': proc.stdout, 'stderr': proc.stderr, 'records': records})
        return proc.stdout, app
    if kind == 'structure':
        output, app = stage('go south', 'crouch then inspect chest brace')
        assert 'attached' in output
        branches.append('observed attached component before choosing loosening')
        output, app = stage('loosen chest brace then inspect chest brace')
        assert 'loosened' in output and app.brace_state.condition == 'loosened'
        branches.append('observed loosening before choosing refit')
        output, app = stage('refit chest brace then inspect chest brace')
        assert 'attached' in output
        stage('go north then wait')
        output, app = stage('go south then inspect chest brace', 'inspect self')
        objectives = {'component_restored_after_time_restart_return': app.brace_state.condition == 'attached',
                      'posture_retained': app.posture_state.configuration == 'crouching',
                      'player_returned': app.current_place_id() == YARD_ID,
                      'two_component_changes': len(app.brace_state.events) == 2}
    elif kind == 'cooperation':
        output, app = stage('go south then wait', 'ask groundskeeper to inspect lantern then crouch')
        assert 'visual evidence' in output and not app.posture_state.events
        branches.append('remote-target refusal stopped second step; selected actual Lantern acquisition and transport')
        stage('go north then take lantern', 'light lantern then go south', 'drop lantern')
        output, app = stage('ask groundskeeper to inspect lantern then take lantern')
        assert len(app.knowledge_state.events) == 1
        output, app = stage('give lantern to groundskeeper then ask groundskeeper what are you carrying')
        assert 'Brass Lantern' in output
        branches.append('observed actor custody before requesting voluntary return')
        stage('ask groundskeeper for lantern then inspect self')
        stage('go north then wait')
        output, app = stage('go south then ask groundskeeper what are you carrying', 'inspect self')
        objectives = {'player_recovered_lantern': 'Carrying: Brass Lantern' in output,
                      'witness_retained_after_restart_time': len(app.knowledge_state.events) == 1 and app.knowledge_state.events[0].source_kind == 'witnessed',
                      'refused_crouch_never_committed': not app.posture_state.events,
                      'actor_local': app.entity_place_id(GROUNDSKEEPER_ID) == app.current_place_id()}
    else:
        stage('go south', 'service chest latch then service chest latch')
        stage('close chest then ask groundskeeper to secure chest latch later')
        stage('go north then wait')
        output, app = stage('go south then check chest duty', 'open chest then crouch')
        assert app.duty_state.status == 'fulfilled' and app.service_state.secured
        assert 'latch' in output and not app.posture_state.events
        branches.append('observed fulfilled duty and secured latch refusal; selected explicit release')
        output, app = stage('release chest latch then open chest', 'inspect chest')
        objectives = {'delayed_duty_retained': app.duty_state.status == 'fulfilled',
                      'latch_explicitly_released': not app.service_state.secured,
                      'chest_opened_after_release': app.object_open_state(app.fixture.resolve_object_reference('chest')).state == 'open',
                      'refused_second_step_not_executed': not app.posture_state.events}
    assert all(objectives.values()), objectives
    return {'profile': kind, 'feedback_branches': branches, 'objectives': objectives, 'final_digest': previous, 'stages': stages}


def semantic(sessions):
    return [(s['final_digest'], s['objectives'], [(r['raw_player_input'], r['parsed_action'], r['result_type'],
            r['failure_class'], r['receipt_id'], r['pre_state_digest'], r['post_state_digest'])
            for stage in s['stages'] for r in stage['records'] if r['record_type'] == 'interaction']) for s in sessions]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    assert shutil.which('myravant-play'), 'installed launcher required'
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    with tempfile.TemporaryDirectory(prefix='myravant-specialist-') as temp:
        repeats = []
        for repeat in range(2):
            sessions = []
            for kind in ('structure', 'cooperation', 'duty'):
                root = Path(temp) / f'{repeat}-{kind}'
                root.mkdir()
                sessions.append(campaign(root, kind, head))
            repeats.append(sessions)
        assert semantic(repeats[0]) == semantic(repeats[1])
    result = {'repository_sha': head, 'implementation_authored': True, 'not_blind_acceptance': True,
              'not_human_play': True, 'profiles': 3, 'repeat_runs': 2, 'deterministic_repetition': True,
              'sessions': repeats[0]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print('Specialist composition: 3 feedback-conditioned profiles repeated twice; all persistent objectives passed.')


if __name__ == '__main__':
    main()
