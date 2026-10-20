"""Portable execution must not overclaim freshness, success or certification."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('myravant_dev', ROOT / 'scripts/myravant_dev.py')
dev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dev)


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / 'repo';root.mkdir()
    def git(*args):
        return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
    git('init', '-b', 'main');git('config', 'user.email', 'test@example.invalid');git('config', 'user.name', 'Test')
    (root / 'tests').mkdir();(root / 'tests/example.py').write_text('original\n')
    git('add', '.');git('commit', '-m', 'fixture')
    return root


def test_context_distinguishes_dirty_source_and_cached_remote(repo):
    before = dev.context(repo)
    assert not before['dirty'] and not before['remote_freshness_verified']
    assert before['origin_main_cached'] is None
    (repo / 'tests/example.py').write_text('changed\n')
    after = dev.context(repo)
    assert after['dirty'] and after['tracked_diff_sha256'] != before['tracked_diff_sha256']
    assert after['head'] == before['head']


def test_focused_rejects_escape_and_symlink(repo, tmp_path):
    outside = tmp_path / 'outside.py';outside.write_text('')
    for path in ('../outside.py', 'tests/missing.py', '-k'):
        with pytest.raises(ValueError):dev.test_paths([path], repo)
    try:
        (repo / 'tests/link.py').symlink_to(outside)
    except OSError:
        return  # Windows may forbid unprivileged symlinks; escape cases above still ran.
    with pytest.raises(ValueError):dev.test_paths(['tests/link.py'], repo)


def test_process_failure_is_observed_in_log(repo, tmp_path):
    log = tmp_path / 'failure.log'
    result = dev.run_step([sys.executable, '-c', 'print("actual failure");raise SystemExit(7)'], log, repo)
    assert result['exit_code'] == 7 and 'actual failure' in log.read_text()
    assert result['launch_error'] is None


def fake_step(argv, logfile, repo, env):
    return {'argv': argv, 'exit_code': 0, 'log': str(logfile), 'elapsed_seconds': 0.1}


def test_full_command_has_no_filters_and_does_not_certify(repo, tmp_path, monkeypatch):
    monkeypatch.setattr(dev, 'run_step', fake_step)
    output = tmp_path / 'evidence'
    assert dev.verify('full', output, repo=repo) == 0
    report = json.loads((output / 'verification.json').read_text())
    assert report['steps'][0]['argv'] == [sys.executable, '-m', 'pytest', '-q']
    assert report['all_commands_passed'] and not report['certified']
    with pytest.raises(ValueError):dev.verify('full', tmp_path / 'other', ['tests/example.py'], repo)


def test_source_change_during_checks_invalidates_result(repo, tmp_path, monkeypatch):
    def mutate(argv, logfile, root, env):
        (root / 'tests/example.py').write_text('modified during verification\n')
        return fake_step(argv, logfile, root, env)
    monkeypatch.setattr(dev, 'run_step', mutate)
    output = tmp_path / 'changed'
    assert dev.verify('full', output, repo=repo) == 1
    report = json.loads((output / 'verification.json').read_text())
    assert not report['source_unchanged'] and not report['all_commands_passed']


def test_evidence_never_overwrites_checkout_or_earlier_runs(repo, tmp_path, monkeypatch):
    monkeypatch.setattr(dev, 'run_step', fake_step)
    with pytest.raises(ValueError):dev.verify('full', repo / 'evidence', repo=repo)
    output = tmp_path / 'existing';output.mkdir();(output / 'old.json').write_text('keep')
    with pytest.raises(ValueError):dev.verify('full', output, repo=repo)
    assert (output / 'old.json').read_text() == 'keep'


def test_retained_discovery_fails_closed_and_missing_output_fails(repo, tmp_path, monkeypatch):
    workflow = repo / '.github/workflows/ci.yml';workflow.parent.mkdir(parents=True)
    script = repo / 'scripts/report_myravant_demo.py';script.parent.mkdir();script.write_text('')
    workflow.write_text('run: python scripts/report_myravant_demo.py --output demo.json\n')
    assert dev.retained_commands(repo) == [('scripts/report_myravant_demo.py', 'demo.json')]
    monkeypatch.setattr(dev, 'run_step', fake_step)
    output = tmp_path / 'missing-artifact'
    assert dev.verify('retained', output, repo=repo) == 1
    report = json.loads((output / 'verification.json').read_text())
    assert report['steps'][0]['exit_code'] == 0 and not report['steps'][0]['output_present']
    workflow.write_text('run: python scripts/report_myravant_demo.py --new-option value\n')
    with pytest.raises(ValueError):dev.retained_commands(repo)


def test_focused_failure_stays_failure(repo, tmp_path, monkeypatch):
    def fail(argv, logfile, root, env):
        return dict(fake_step(argv, logfile, root, env), exit_code=3)
    monkeypatch.setattr(dev, 'run_step', fail)
    output = tmp_path / 'failure'
    assert dev.verify('focused', output, ['tests/example.py'], repo) == 1
    assert not json.loads((output / 'verification.json').read_text())['all_commands_passed']


def test_development_local_document_links_resolve():
    import re
    documents = [ROOT / 'AGENTS.md', *(ROOT / 'docs/development').glob('*.md')]
    for document in documents:
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if '://' in target or target.startswith('#'):continue
            assert (document.parent / target.split('#')[0]).exists(), (document.name, target)


def test_actual_retained_commands_cover_workflow_reports():
    commands = dev.retained_commands(ROOT)
    assert len(commands) >= 17
    assert len({output for _, output in commands}) == len(commands)


def test_context_export_does_not_overwrite_existing_evidence(repo, tmp_path, monkeypatch):
    monkeypatch.setattr(dev, 'ROOT', repo)
    monkeypatch.setattr(dev, 'context', lambda: {'head': 'fixture'})
    output = tmp_path / 'context.json';output.write_text('preserve previous evidence')
    with pytest.raises(SystemExit) as failure:
        dev.main(['context', '--output', str(output)])
    assert failure.value.code == 2
    assert output.read_text() == 'preserve previous evidence'
