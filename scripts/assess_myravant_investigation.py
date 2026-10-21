"""Evaluate frozen declarative scenario objectives against recorded installed evidence.

This is a separate bounded developer evaluator, not independent/blind/human.
It cannot authenticate fabricated reports; replay/campaign CI is a distinct gate.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess


SPEC = Path(__file__).resolve().parents[1] / 'tests/fixtures/tarrow_investigation_assessor_goals.json'


def evaluate(journeys, specification, expected_sha):
    if (specification.get('schema') != 'myravant.investigation-separate-goals.v1'
            or specification.get('contract_issue') != 552
            or journeys.get('kind') != 'investigation-installed-journeys'
            or journeys.get('repository_sha') != expected_sha
            or not re.fullmatch('[0-9a-f]{40}', expected_sha)):
        raise ValueError('wrong source or goals/evidence profile')
    goals = specification['goals']
    profiles = journeys['profiles']
    if (len(goals) != 3 or len(profiles) != 3
            or len({x['id'] for x in goals}) != len(goals)
            or len({x['recipe'] for x in goals}) != len(goals)
            or set(x['recipe'] for x in profiles) != set(x['recipe'] for x in goals)):
        raise ValueError('missing or duplicate assessed circumstance')
    rows = []
    for goal in goals:
        record = next(r for r in profiles if r['recipe'] == goal['recipe'])
        repeats = record['repeats']
        if len(repeats) != specification['require_repeat_count']:
            raise ValueError('missing required repetition')
        if len({r['final_digest'] for r in repeats}) != 1:
            raise ValueError('repeated inputs did not replay to the same world state')
        for number, replay in enumerate(repeats):
            if replay.get('recipe') != goal['recipe'] or not replay.get('prehistory_receipts'):
                raise ValueError('case identity/actual history is missing')
            flags = replay['objectives']
            missing = [key for key in goal['required_objectives']
                       if flags.get(key) is not True]
            if missing:
                raise ValueError('missing or failed independently stated objective: ' + ','.join(missing))
            stages = replay.get('stages')
            if not stages or any(not stage.get('restored_digest')
                                 or not stage.get('trace') for stage in stages):
                raise ValueError('missing installed trace or post-restart assessment')
            if stages[-1]['restored_digest'] != replay['final_digest']:
                raise ValueError('final state does not match verified restore')
            all_interactions = [
                x for stage in stages for x in stage['trace']
                if x.get('record_type') == 'interaction'
            ]
            if not all_interactions:
                raise ValueError('no actual player attempts in journey')
            queried = [x for x in all_interactions
                       if x.get('raw_player_input', '').strip().casefold().startswith(('recall ', 'compare '))]
            if not queried or any(
                x.get('pre_state_digest') != x.get('post_state_digest')
                or x.get('logical_time_before') != x.get('logical_time_after')
                for x in queried
            ):
                raise ValueError('query is missing or not read-only')
            rows.append({'goal': goal['id'], 'recipe': goal['recipe'],
                         'repeat': number, 'named_objectives_passed': len(goal['required_objectives']),
                         'installed_interactions': len(all_interactions),
                         'source_sha': expected_sha})
    return {
        'schema': 'myravant.investigation-separate-assessment.v1',
        'repository_sha': expected_sha,
        'criteria_source': 'tests/fixtures/tarrow_investigation_assessor_goals.json',
        'assessed_repeats': len(rows),
        'all_named_goals_passed': True,
        'blind': False, 'human_acceptance': False,
        'independent_from_implementation_author': False,
        'rows': rows,
        'limits': ['Declaratively separate developer goals, not an independent or blind assessor.',
                   'Uploaded traces and source-bound replay must be verified independently.',
                   'No general NPC investigation, universal sensory knowledge or native canon claim.'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    current = subprocess.run(['git', 'rev-parse', 'HEAD'], text=True,
                             capture_output=True, check=True).stdout.strip()
    report = evaluate(json.loads(args.input.read_text()),
                      json.loads(SPEC.read_text()), current)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    print('Separate developer assessor: three goals, six repeated installed outcomes qualified.')


if __name__ == '__main__':
    main()
