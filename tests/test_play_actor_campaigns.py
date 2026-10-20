"""Public installed #548 campaign objectives, independent of scenario flags."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess

import pytest


def _runner():
    path = Path(__file__).resolve().parents[1] / 'scripts' / 'report_myravant_actors.py'
    spec = importlib.util.spec_from_file_location('actor_campaign_runner', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('kind', ['absent-cleanup', 'cooperative-assembly', 'stale-evidence'])
def test_installed_adaptive_actor_campaign_repeats_with_restart(tmp_path, kind):
    runner = _runner()
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=Path(__file__).resolve().parents[1],
                          text=True, capture_output=True, check=True).stdout.strip()
    runs = []
    for repeat in range(2):
        root = tmp_path / str(repeat); root.mkdir()
        runs.append(runner.campaign(root, kind, head))
    assert runs[0]['final_digest'] == runs[1]['final_digest']
    assert all(all(run['objectives'].values()) for run in runs)
    assert all(len(run['stages']) > 1 for run in runs)
    if report_directory := os.environ.get('MYRAVANT_ACTOR_CAMPAIGN_REPORT_DIR'):
        output = Path(report_directory) / f'{kind}.json'
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({'repository_sha': head, 'implementation_authored': True,
            'not_blind_or_human_acceptance': True, 'repeat_count': 2, 'profile': kind,
            'repeats': runs}, indent=2, sort_keys=True) + '\n')
