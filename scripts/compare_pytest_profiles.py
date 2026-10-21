"""Fail closed on changed pytest identities/outcomes; report comparable timings.

Input artifacts must come from serial/parallel jobs in the same workflow run
and platform. This checks execution outcomes, not independent gameplay acceptance.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET


def profile(path):
    root = ET.parse(path).getroot()
    cases = {}
    file_seconds = Counter()
    for case in root.iter('testcase'):
        key = case.get('classname', '') + '::' + case.get('name', '')
        if key in cases:
            raise ValueError('Duplicate test identity: ' + key)
        outcome = 'passed'
        for tag in ('failure', 'error', 'skipped'):
            if (element := case.find(tag)) is not None:
                outcome = tag + ':' + element.get('type', '')
                break
        cases[key] = outcome
        file_seconds[case.get('classname', '')] += float(case.get('time', '0'))
    if not cases:
        raise ValueError('Empty suite')
    if any(value.startswith(('failure:', 'error:')) for value in cases.values()):
        raise ValueError('Suite contains failures or errors')
    suites = list(root.iter('testsuite'))
    if any(int(s.get(field, '0')) for s in suites for field in ('failures', 'errors')):
        raise ValueError('Suite summary contains failures or collection errors')
    elapsed = sum(float(s.get('time', '0')) for s in suites)
    if not math.isfinite(elapsed) or elapsed <= 0:
        raise ValueError('Invalid elapsed suite time')
    return cases, {
        'cases': len(cases), 'outcomes': dict(Counter(cases.values())),
        'elapsed_seconds': elapsed,
        'slowest_modules_seconds': file_seconds.most_common(50),
    }


def compare(serial, parallel):
    left, baseline = profile(serial)
    right, candidate = profile(parallel)
    changes = {key: [left.get(key), right.get(key)] for key in left.keys() | right.keys()
               if left.get(key) != right.get(key)}
    return {'equivalent': not changes, 'changes': changes,
            'serial': baseline, 'parallel': candidate,
            'speedup': (baseline['elapsed_seconds'] / candidate['elapsed_seconds']
                        if candidate['elapsed_seconds'] else None),
            'limits': ['Same-run/platform input provenance is supplied by the workflow.',
                       'Outcome equality does not replace replay, mutation or installed evidence.',
                       'JUnit elapsed time excludes setup and artifact upload.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('serial', type=Path)
    parser.add_argument('parallel', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = compare(args.serial, args.parallel)
    except (ValueError, OSError, ET.ParseError) as error:
        result = {'equivalent': False, 'error': str(error)}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(result, sort_keys=True))
    return 0 if result['equivalent'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
