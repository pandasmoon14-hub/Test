"""Portable developer context and verification; never simulation authority.

No network or shell interpolation. Evidence reports describe actual subprocesses;
they do not replace owning contracts, independent review or CI certification.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import platform
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REPORT_VERSION = 1


def git(repo, *args):
    result = subprocess.run(['git', *args], cwd=repo, capture_output=True)
    if result.returncode:
        raise RuntimeError('git ' + args[0] + ' failed; a Git checkout is required')
    return result.stdout


def context(repo=ROOT):
    """Local tracked fingerprint. origin/main is explicitly not live GitHub."""
    repo = Path(repo)
    status = git(repo, 'status', '--porcelain=v1', '-z').decode('utf-8', errors='replace')
    diff = git(repo, 'diff', 'HEAD', '--binary')
    try:
        origin = git(repo, 'rev-parse', '--verify', 'refs/remotes/origin/main').decode().strip()
    except RuntimeError:
        origin = None
    hashes = {}
    for name in ('AGENTS.md', 'docs/development/START_HERE.md',
                 'docs/development/runtime_delivery_protocol.md'):
        path = repo / name
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    return {'report_version': REPORT_VERSION, 'kind': 'local_context',
            'head': git(repo, 'rev-parse', 'HEAD').decode().strip(),
            'branch': git(repo, 'rev-parse', '--abbrev-ref', 'HEAD').decode().strip(),
            'origin_main_cached': origin, 'remote_freshness_verified': False,
            'dirty': bool(status), 'status_porcelain_z': status,
            'tracked_diff_sha256': hashlib.sha256(diff).hexdigest(),
            'guidance_sha256': hashes,
            'environment': {'python': sys.version, 'platform': platform.platform(),
                            'executable': sys.executable},
            'limits': ['Untracked file contents are not fingerprinted.',
                       'No GitHub approval, PR, CI or remote freshness query was made.',
                       'This is developer evidence, not runtime truth or certification.']}


def retained_commands(repo=ROOT):
    """Discover the explicit retained report commands in the owning CI workflow."""
    source = (Path(repo) / '.github/workflows/ci.yml').read_text(encoding='utf-8')
    found = []
    for line in source.splitlines():
        if 'python scripts/report_myravant_' not in line:
            continue
        command = re.sub(r'^\s*(?:run:\s*)?', '', line).strip()
        match = re.fullmatch(r'python (scripts/report_myravant_[\w]+\.py) --output ([\w.-]+\.json)', command)
        if not match:
            raise ValueError('Unsupported report command; inspect CI instead of silently skipping: ' + command)
        script, output = match.groups()
        if not (Path(repo) / script).is_file():
            raise ValueError('CI report script is missing: ' + script)
        if (script, output) not in found:
            found.append((script, output))
    if not found:
        raise ValueError('No retained report commands discovered; inspect current CI')
    return found


def test_paths(paths, repo=ROOT):
    repo = Path(repo).resolve()
    resolved = []
    for name in paths:
        path = (repo / name).resolve()
        if not path.is_relative_to(repo / 'tests') or not path.exists():
            raise ValueError('Focused paths must exist under this checkout tests/: ' + name)
        resolved.append(path.relative_to(repo).as_posix())
    if not resolved:
        raise ValueError('Focused verification requires explicit affected test paths')
    return resolved


def run_step(argv, logfile, repo=ROOT, env=None):
    start = time.monotonic()
    stamp = datetime.now(timezone.utc).isoformat()
    try:
        with Path(logfile).open('w', encoding='utf-8') as stream:
            result = subprocess.run(argv, cwd=repo, env=env, stdout=stream, stderr=subprocess.STDOUT)
        code, error = result.returncode, None
    except OSError as exc:
        code, error = 127, str(exc)
    return {'argv': list(argv), 'exit_code': code, 'started_utc': stamp,
            'elapsed_seconds': time.monotonic() - start, 'log': str(logfile),
            'launch_error': error}


def verify(profile, output, paths=(), repo=ROOT):
    repo = Path(repo).resolve()
    output = Path(output).resolve()
    # Existing tracked files must never become log destinations.
    if output.is_relative_to(repo):
        raise ValueError('Use an evidence directory outside the Git checkout')
    before = context(repo)
    if profile == 'focused':
        jobs = [([sys.executable, '-m', 'pytest', '-q', *test_paths(paths, repo)], 'pytest')]
    elif profile == 'full':
        if paths:
            raise ValueError('Full verification cannot filter test paths')
        jobs = [([sys.executable, '-m', 'pytest', '-q'], 'pytest')]
    else:
        if paths:
            raise ValueError('Retained evidence does not accept test filters')
        jobs = [([sys.executable, script, '--output', str(output / filename)], Path(script).stem)
                for script, filename in retained_commands(repo)]
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Use a new empty evidence directory to preserve earlier runs')
    env = dict(os.environ, PYTHONUTF8='1')
    if profile == 'full':
        env.update(MYRAVANT_ACTOR_CAMPAIGN_REPORT_DIR=str(output / 'actor-campaigns'),
                   MYRAVANT_ACTOR_ASSESSOR_REPORT=str(output / 'actor-assessor.json'))
    steps = []
    for number, (argv, name) in enumerate(jobs):
        step = run_step(argv, output / f'{number:02d}-{name}.log', repo, env)
        if profile == 'retained':
            step['output_present'] = Path(argv[-1]).is_file()
        steps.append(step)
        print(f'{name}: exit {step["exit_code"]}; {step["elapsed_seconds"]:.2f}s', flush=True)
        if step['exit_code'] or not step.get('output_present', True):
            break
    after = context(repo)
    unchanged = before == after
    passed = unchanged and len(steps) == len(jobs) and all(s['exit_code'] == 0 and s.get('output_present', True) for s in steps)
    report = {'report_version': REPORT_VERSION, 'kind': 'local_verification',
              'profile': profile, 'source': before, 'source_after': after,
              'source_unchanged': unchanged, 'steps': steps, 'planned_steps': len(jobs),
              'all_commands_passed': passed, 'certified': False,
              'limits': ['Command success is not independent or human acceptance.',
                         'Check owning contract, clean source and exact-head platform CI before certification.']}
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0 if passed else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    packet = sub.add_parser('context')
    packet.add_argument('--output', type=Path)
    checks = sub.add_parser('verify')
    checks.add_argument('--profile', choices=('focused', 'full', 'retained'), required=True)
    checks.add_argument('--output', type=Path, required=True)
    checks.add_argument('--test-path', action='append', default=[])
    sub.add_parser('list-retained')
    args = parser.parse_args(argv)
    try:
        if args.command == 'context':
            value = json.dumps(context(), indent=2) + '\n'
            if args.output:
                if args.output.resolve().is_relative_to(ROOT):
                    raise ValueError('Write context output outside the checkout')
                with args.output.open('x', encoding='utf-8') as stream:
                    stream.write(value)
            else:
                print(value, end='')
            return 0
        if args.command == 'list-retained':
            print(json.dumps(retained_commands(), indent=2))
            return 0
        return verify(args.profile, args.output, args.test_path)
    except (OSError, RuntimeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    raise SystemExit(main())
