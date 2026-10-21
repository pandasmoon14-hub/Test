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
            trace = [{'record_type': 'interaction', 'raw_player_input': 'recall panel a residue',
                      'pre_state_digest': 'stable', 'post_state_digest': 'stable',
                      'logical_time_before': 1, 'logical_time_after': 1}]
            rows.append({'recipe': goal['recipe'], 'final_digest': 'same',
                         'prehistory_receipts': [['move', 'qualified']],
                         'objectives': {key: True for key in goal['required_objectives']},
                         'stages': [{'restored_digest': 'same', 'trace': trace}]})
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
