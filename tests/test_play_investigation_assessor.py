"""Separate objective criteria fail closed on missing replay or false positives."""
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/assess_myravant_investigation.py'
spec = importlib.util.spec_from_file_location('separate_investigation_assessment', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SHA = '1' * 40


def successful_report():
    goals = json.loads(module.SPEC.read_text())
    records = []
    for goal in goals['goals']:
        rows = []
        for _ in range(2):
            trace = [{'record_type': 'interaction',
                      'raw_player_input': 'compare reports about panel a residue',
                      'pre_state_digest': 'stable', 'post_state_digest': 'stable',
                      'logical_time_before': 1, 'logical_time_after': 1}]
            preparation = [['move', 'qualified']]
            rows.append({'recipe': goal['recipe'], 'initial_digest': 'prepared',
                         'final_digest': 'same', 'prehistory_receipts': preparation,
                         'public_start': {
                             'launch_args': ['--locality', 'tarrow-investigation',
                                             '--prepare-investigation', '--checkpoint', 'fresh.json'],
                             'restored_digest': 'prepared',
                             'prehistory_receipts': preparation,
                             'stdout': 'Noncanonical investigation circumstance prepared through committed world actions',
                             'trace': [{'record_type': 'session_end', 'evidence_complete': True}],
                         },
                         'objectives': {key: True for key in goal['required_objectives']},
                         'stages': [{'restored_digest': 'same', 'trace': trace,
                                     'stdout': module.NONCONCLUSIVE_NOTICE}]})
        records.append({'recipe': goal['recipe'], 'repeats': rows})
    return {'kind': 'investigation-installed-journeys', 'repository_sha': SHA,
            'profiles': records}, goals


def test_assessor_requirements_are_explicit_and_reproducible():
    report, goals = successful_report()
    checked = module.evaluate(report, goals, SHA)
    assert checked['assessed_repeats'] == 6 and checked['all_named_goals_passed']
    assert not checked['blind'] and not checked['human_acceptance']
    assert not checked['independent_from_implementation_author']


def test_assessor_rejects_missing_goal_bad_sha_and_forged_satisfaction():
    report, goals = successful_report()
    with pytest.raises(ValueError, match='wrong source'):
        module.evaluate(report, goals, '2' * 40)
    report['profiles'][0]['repeats'][0]['objectives'] = {}
    with pytest.raises(ValueError, match='missing or failed'):
        module.evaluate(report, goals, SHA)


def test_assessor_rejects_unstable_restore_and_query_advancement():
    report, goals = successful_report()
    report['profiles'][1]['repeats'][1]['final_digest'] = 'different'
    with pytest.raises(ValueError, match='repeated inputs'):
        module.evaluate(report, goals, SHA)
    report, goals = successful_report()
    report['profiles'][0]['repeats'][0]['stages'][0]['trace'][0]['logical_time_after'] = 2
    with pytest.raises(ValueError, match='read-only'):
        module.evaluate(report, goals, SHA)


def test_assessor_rejects_prebuilt_dev_only_case_without_public_start():
    report, goals = successful_report()
    report['profiles'][0]['repeats'][0].pop('public_start')
    with pytest.raises(ValueError, match='public fresh-start'):
        module.evaluate(report, goals, SHA)


def test_assessor_rejects_public_loader_masquerading_as_fresh_start():
    report, goals = successful_report()
    start = report['profiles'][0]['repeats'][0]['public_start']
    start['launch_args'] = ['--load', 'prepared.json']
    with pytest.raises(ValueError, match='public fresh-start'):
        module.evaluate(report, goals, SHA)


def test_assessor_rejects_false_success_flag_with_conclusive_public_verdict():
    report, goals = successful_report()
    stage = report['profiles'][2]['repeats'][1]['stages'][0]
    stage['stdout'] += ' The first account is established true.'
    assert report['profiles'][2]['repeats'][1]['objectives']['no_omniscient_guilt_resolution']
    with pytest.raises(ValueError, match='public comparison'):
        module.evaluate(report, goals, SHA)


def test_assessor_rejects_missing_public_comparison_even_with_true_flags():
    report, goals = successful_report()
    for stage in report['profiles'][1]['repeats'][0]['stages']:
        stage['trace'][0]['raw_player_input'] = 'recall panel a residue'
    with pytest.raises(ValueError, match='public comparison'):
        module.evaluate(report, goals, SHA)


def test_assessor_rejects_missing_public_disclaimer_even_with_true_flags():
    report, goals = successful_report()
    report['profiles'][2]['repeats'][0]['stages'][0]['stdout'] = 'An account appears elsewhere.'
    with pytest.raises(ValueError, match='public comparison'):
        module.evaluate(report, goals, SHA)
