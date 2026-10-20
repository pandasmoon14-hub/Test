"""Exercise real process failures, stale context and truthful continuation."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
module_spec = importlib.util.spec_from_file_location('assist_under_test', SCRIPTS / 'myravant_assist.py')
assist = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(assist)
ROOT = SCRIPTS.parent


def git(repo, *args):
    return subprocess.run(['git', *args], cwd=repo, check=True, capture_output=True).stdout.decode().strip()


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / 'repo'
    root.mkdir()
    git(root, 'init')
    git(root, 'config', 'user.name', 'Fixture')
    git(root, 'config', 'user.email', 'fixture@example.invalid')
    files = {
        '.gitignore': '__pycache__/\n.pytest_cache/\n',
        'AGENTS.md': 'Fixture authority only',
        'docs/development/START_HERE.md': 'Start here',
        'src/sample/__init__.py': '',
        'src/sample/core.py': 'VALUE = 4\n',
        'src/sample/client.py': 'from .core import VALUE\n',
        'tests/test_example.py': 'def test_ok():\n    assert 2 + 2 == 4\n',
        'tests/test_fail.py': 'def test_bad():\n    assert False, "actual child failure"\n',
        'tests/test_mutate.py': 'from pathlib import Path\ndef test_mutate():\n    Path("AGENTS.md").write_text("changed")\n',
        '.github/workflows/ci.yml': 'run: python scripts/report_myravant_fixture.py --output fixture.json\n',
        'scripts/report_myravant_fixture.py': 'print("No report written")\n',
    }
    catalog = {'version': 1, 'routes': [{
        'id': 'example', 'terms': ['example', 'water'],
        'sources': ['src/sample/core.py'], 'tests': ['tests/test_example.py'],
        'examples': [], 'failures': [], 'lenses': ['Check consequences']}]}
    files[assist.CATALOG] = json.dumps(catalog)
    for name, contents in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding='utf-8')
    git(root, 'add', '.')
    git(root, 'commit', '-m', 'fixture')
    return root


def spec(*criteria):
    return {'version': 1, 'task': 'Fixture continuation', 'owning_record': 'fixture only',
            'criteria': [dict(id=str(i), description='Observe ' + target, kind=kind, target=target)
                         for i, (kind, target) in enumerate(criteria)]}


def test_packet_ranking_budget_relative_imports_and_staleness(repo):
    result = assist.packet('water example', 'HEAD', repo, max_chars=600)
    assert result['routes'][0]['id'] == 'example'
    assert result['budget']['used_characters'] <= 600
    assert {'importer': 'src/sample/client.py', 'imported': 'src/sample/core.py'} in result['impact']['edges']
    assert assist.freshness(result, repo)['fresh']
    (repo / 'src/sample/core.py').write_text('VALUE = 5\n')
    state = assist.freshness(result, repo)
    assert not state['fresh']
    assert 'tracked_diff_sha256' in state['changed_source_fields']


def test_unknown_task_does_not_invent_coverage(repo):
    result = assist.packet('unmatched zeppelin', 'HEAD', repo)
    assert result['routes'] == []
    assert result['suggested_tests'] == []
    assert 'explicit source discovery' in result['retrieval_limits'][0]


def test_deleted_source_still_appears_in_changed_paths(repo):
    (repo / 'src/sample/core.py').unlink()
    result = assist.packet('example', 'HEAD', repo)
    assert 'src/sample/core.py' in result['changed_paths']


@pytest.mark.parametrize('base', ['--help', 'not-a-real-ref'])
def test_bad_base_fails_closed(repo, base):
    with pytest.raises((ValueError, RuntimeError)):
        assist.packet('water', base, repo)


def test_real_failure_and_unrun_criteria_are_not_passed(repo, tmp_path):
    task = spec(('test', 'tests/test_fail.py'), ('test', 'tests/test_example.py'))
    out = tmp_path / 'failed'
    result = assist.acceptance(task, out, repo)
    assert [c['status'] for c in result['criteria']] == ['failed', 'pending']
    assert not result['all_criteria_passed']
    assert 'actual child failure' in (out / '0.log').read_text()
    resume = assist.resume(task, out / 'acceptance.json', repo)
    assert resume['next_step'] == 'Resolve criterion 0'
    assert resume['authorization']['merge_authorized'] is False


def test_manual_acceptance_not_inferred_and_resume_detects_drift(repo, tmp_path):
    task = spec(('test', 'tests/test_example.py'), ('manual', 'ordinary-chat observation'))
    out = tmp_path / 'manual'
    result = assist.acceptance(task, out, repo)
    assert result['all_commands_passed'] and not result['all_criteria_passed']
    assert result['criteria'][1]['status'] == 'pending'
    assert not assist.resume(task, out / 'acceptance.json', repo)['evidence_stale']
    (repo / 'AGENTS.md').write_text('changed')
    assert assist.resume(task, out / 'acceptance.json', repo)['evidence_stale']


def test_mutation_during_real_check_invalidates_acceptance(repo, tmp_path):
    result = assist.acceptance(spec(('test', 'tests/test_mutate.py')), tmp_path / 'mutation', repo)
    assert result['criteria'][0]['status'] == 'passed'
    assert not result['source_unchanged'] and not result['all_criteria_passed']


def test_missing_retained_output_is_failure(repo, tmp_path):
    result = assist.acceptance(spec(('retained', 'scripts/report_myravant_fixture.py')),
                               tmp_path / 'missing', repo)
    assert result['criteria'][0]['exit_code'] == 0
    assert result['criteria'][0]['status'] == 'failed'
    assert not result['criteria'][0]['output_present']


def test_pytest_filters_from_environment_and_config_cannot_hide_failure(repo, tmp_path, monkeypatch):
    (repo / 'tests/test_example.py').write_text(
        'def test_ok():\n    assert True\ndef test_bad():\n    assert False, "must run"\n')
    (repo / 'pytest.ini').write_text('[pytest]\naddopts = -k test_ok\n')
    monkeypatch.setenv('PYTEST_ADDOPTS', '-k test_ok')
    result = assist.acceptance(spec(('test', 'tests/test_example.py')), tmp_path / 'filters', repo)
    assert result['criteria'][0]['status'] == 'failed'
    assert '1 failed, 1 passed' in (tmp_path / 'filters/0.log').read_text()
    assert assist.dev.verify('full', tmp_path / 'full-filters', repo=repo) == 1


def test_retained_symlink_is_not_a_fresh_report(repo, tmp_path):
    old = tmp_path / 'old.json'
    old.write_text('{}')
    probe = tmp_path / 'probe-link'
    try:
        probe.symlink_to(old)
    except OSError:
        pytest.skip('Platform does not permit symlinks')
    (repo / 'scripts/report_myravant_fixture.py').write_text(
        'from pathlib import Path\nimport sys\nPath(sys.argv[-1]).symlink_to(' + repr(str(old)) + ')\n')
    result = assist.acceptance(spec(('retained', 'scripts/report_myravant_fixture.py')),
                               tmp_path / 'symlink-output', repo)
    assert not result['criteria'][0]['output_present']
    assert not result['all_criteria_passed']


def test_timeout_is_not_a_successful_check(repo, tmp_path):
    path = repo / 'tests/test_example.py'
    path.write_text('import time\ndef test_slow():\n    time.sleep(10)\n')
    result = assist.acceptance(spec(('test', 'tests/test_example.py')), tmp_path / 'timeout',
                               repo, timeout=0.1)
    assert result['criteria'][0]['exit_code'] == 124
    assert not result['all_criteria_passed']


def test_retained_report_changes_are_detected(repo, tmp_path):
    (repo / 'scripts/report_myravant_fixture.py').write_text(
        'from pathlib import Path\nimport sys\nPath(sys.argv[-1]).write_text("{}")\n')
    task = spec(('retained', 'scripts/report_myravant_fixture.py'))
    out = tmp_path / 'retained'
    assist.acceptance(task, out, repo)
    assert not assist.resume(task, out / 'acceptance.json', repo)['evidence_stale']
    (out / '0.json').write_text('changed')
    with pytest.raises(ValueError, match='report'):
        assist.resume(task, out / 'acceptance.json', repo)


@pytest.mark.parametrize('kind,target', [
    ('shell', 'echo unsafe'), ('test', '../escape.py'),
    ('test', 'scripts/report_myravant_fixture.py'), ('retained', 'scripts/unknown.py'),
    ('test', 'tests/untracked.py')])
def test_arbitrary_or_untracked_targets_rejected(repo, kind, target):
    with pytest.raises(ValueError):
        assist.validate_spec(spec((kind, target)), repo)


def test_no_overwrites_no_source_output_and_tampered_log_rejected(repo, tmp_path):
    task = spec(('test', 'tests/test_example.py'))
    with pytest.raises(ValueError):
        assist.acceptance(task, repo / 'evidence', repo)
    out = tmp_path / 'evidence'
    assist.acceptance(task, out, repo)
    with pytest.raises(ValueError):
        assist.acceptance(task, out, repo)
    (out / '0.log').write_text('forged')
    with pytest.raises(ValueError, match='log'):
        assist.resume(task, out / 'acceptance.json', repo)
    report = tmp_path / 'preserved.json'
    assist.write_report(report, {'a': 1}, repo)
    with pytest.raises(FileExistsError):
        assist.write_report(report, {'a': 2}, repo)


def test_spec_changes_cannot_reuse_old_result(repo, tmp_path):
    task = spec(('test', 'tests/test_example.py'))
    out = tmp_path / 'evidence'
    assist.acceptance(task, out, repo)
    task['criteria'][0]['description'] = 'Different obligation'
    with pytest.raises(ValueError, match='specification'):
        assist.resume(task, out / 'acceptance.json', repo)


def test_symlink_cannot_export_external_source(repo, tmp_path):
    secret = tmp_path / 'private.txt'
    secret.write_text('not context')
    path = repo / 'AGENTS.md'
    path.unlink()
    try:
        path.symlink_to(secret)
    except OSError:
        pytest.skip('Platform does not permit symlinks')
    with pytest.raises(ValueError):
        assist.source(repo, 'AGENTS.md')


def test_review_is_bounded_and_not_independent(repo):
    result = assist.packet('example', 'HEAD', repo)
    (repo / 'src/sample/core.py').write_text('VALUE = 9')
    review = assist.review(result, repo)
    assert len(review['flags']) == 2
    assert not review['independent_review'] and not review['certified']


def test_benchmark_scores_missing_and_forbidden_claims_without_invention():
    cases = {'version': 1, 'cases': [
        {'id': 'a', 'expected_facts': {'merge': False}, 'forbidden_claims': ['certified']},
        {'id': 'b', 'expected_facts': {'head': 'exact'}}]}
    answers = {'version': 1, 'answers': [{'id': 'a', 'facts': {'merge': False}, 'claims': ['certified']}]}
    result = assist.benchmark(cases, answers)
    assert result['completed_cases'] == 0
    assert result['cases'][0]['correct_facts'] == 1
    assert result['cases'][1]['correct_facts'] == 0
    assert result['cases'][1]['elapsed_seconds'] is None
    answers['answers'].append(answers['answers'][0])
    with pytest.raises(ValueError):
        assist.benchmark(cases, answers)


def test_catalog_references_and_executable_examples_are_real():
    catalog = assist.read_json(ROOT / assist.CATALOG)
    assert len(catalog['routes']) >= 6
    for route in catalog['routes']:
        for name in route['sources'] + route['tests']:
            assert (ROOT / name).is_file(), name
        for example in route['examples']:
            name, node = example['test'].split('::')
            assert 'def ' + node + '(' in (ROOT / name).read_text(), example
