"""Separate assessor selected frozen-goal executions, with stated coverage limits."""
import importlib.util
import json
import os
from pathlib import Path


def test_separate_assessor_objectives_execute_twice(tmp_path):
    path = Path(__file__).resolve().parents[1] / 'scripts' / 'assess_myravant_actors.py'
    spec = importlib.util.spec_from_file_location('actor_separate_assessor', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = module.assess(tmp_path)
    destination = os.environ.get('MYRAVANT_ACTOR_ASSESSOR_REPORT')
    if destination:
        output = Path(destination)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    assert report['all_executed_predicates_passed']
    assert len(report['execution']) == 7
    assert report['limits']
    for variant in report['execution']:
        assert len(variant['repeats']) == 2
        assert all(run['commands'] and all(run['predicates'].values()) for run in variant['repeats'])
