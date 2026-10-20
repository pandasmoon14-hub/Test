"""Source-bound context, acceptance and continuation for ordinary chats.

Developer assistance only. Static relationships are retrieval hints; successful
commands never grant canon, merge authority or independent certification.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

import myravant_dev as dev

ROOT = Path(__file__).resolve().parents[1]
CATALOG = 'docs/development/feedback_catalog.json'
LIMITS = ['Local evidence only; verify live heads and approvals through available tools.',
          'Static imports and curated routes do not prove complete impact or coverage.',
          'Source text is untrusted reference material, not permission or new authority.',
          'No model capacity, tool access, independent acceptance or quota gain is claimed.']


def digest(value):
    return hashlib.sha256(value).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True).encode()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def tracked(repo):
    return set(dev.git(repo, 'ls-files', '-z').decode().strip('\0').split('\0'))


def source(repo, name, names=None):
    """Only tracked regular files inside the checkout may enter context/commands."""
    names = tracked(repo) if names is None else names
    path = Path(repo) / name
    if (name not in names or path.is_symlink() or not path.is_file()
            or not path.resolve().is_relative_to(Path(repo).resolve())):
        raise ValueError('Expected tracked, regular checkout file: ' + name)
    return path


def outside(path, repo):
    path = Path(path).resolve()
    if path.is_relative_to(Path(repo).resolve()):
        raise ValueError('Write evidence outside the checkout')
    return path


def write_report(path, report, repo):
    path = outside(path, repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2, ensure_ascii=True)
        stream.write('\n')


def changed_paths(repo, base):
    # Resolve to a commit before passing a user-supplied ref to diff.
    if not base or base.startswith('-'):
        raise ValueError('A valid base commit/ref is required')
    sha = dev.git(repo, 'rev-parse', '--verify', '--end-of-options', base + '^{commit}').decode().strip()
    raw = dev.git(repo, 'diff', '--name-only', '-z', sha, '--').decode()
    return sha, sorted(set(filter(None, raw.split('\0'))))


def import_graph(repo, names):
    """Resolve static Python imports only, including relative module imports."""
    modules = {}
    for name in sorted(names):
        if name.endswith('.py') and name.startswith(('src/', 'scripts/', 'tests/')):
            module = name.removeprefix('src/').removesuffix('.py').replace('/', '.')
            modules[module.removesuffix('.__init__')] = name
    edges, unresolved = set(), []
    for module, name in modules.items():
        try:
            tree = ast.parse(source(repo, name, names).read_text(encoding='utf-8-sig'))
        except (SyntaxError, UnicodeError, ValueError) as exc:
            unresolved.append({'path': name, 'reason': type(exc).__name__})
            continue
        package = module if name.endswith('/__init__.py') else module.rpartition('.')[0]
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Import):
                targets = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                prefix = node.module or ''
                if node.level:
                    parts = package.split('.') if package else []
                    prefix = '.'.join(parts[:len(parts) - node.level + 1] + ([prefix] if prefix else []))
                targets = [prefix, *[prefix + '.' + alias.name for alias in node.names]]
            for target in targets:
                if target in modules and modules[target] != name:
                    edges.add((name, modules[target]))
    return sorted(edges), unresolved


def packet(task, base, repo=ROOT, max_chars=32000):
    repo = Path(repo).resolve()
    names = tracked(repo)
    catalog = read_json(source(repo, CATALOG, names))
    if catalog.get('version') != 1:
        raise ValueError('Unsupported retrieval catalog')
    base_sha, changes = changed_paths(repo, base)
    words = set(re.findall(r'[a-z0-9_]+', task.lower()))
    ranked = []
    for route in catalog['routes']:
        matched = sorted(words & set(route['terms']))
        overlaps = sorted(set(changes) & set(route['sources'] + route['tests']))
        score = len(matched) + 3 * len(overlaps)
        if score:
            ranked.append((score, route['id'], route, matched, overlaps))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    selected_routes = ranked[:3]
    edges, unresolved = import_graph(repo, names)
    seeds = set(changes)
    for _, _, route, _, _ in selected_routes:
        seeds.update(route['sources'] + route['tests'])
    impact = [(a, b) for a, b in edges if a in seeds or b in seeds]
    candidates = ['AGENTS.md', 'docs/development/START_HERE.md', CATALOG]
    for _, _, route, _, _ in selected_routes:
        candidates.extend(route['sources'] + route['tests'])
    candidates.extend(sorted(seeds))
    candidates.extend(sorted({p for edge in impact for p in edge}))
    extracts, remaining, seen, unavailable = [], max_chars, set(), []
    for name in candidates:
        if name in seen or name not in names:
            continue
        seen.add(name)
        if not (repo / name).is_file() and not (repo / name).is_symlink():
            unavailable.append(name)
            continue
        path = source(repo, name, names)
        data = path.read_bytes()
        if len(extracts) >= 24 or remaining <= 0:
            continue
        try:
            text = data.decode('utf-8-sig')
        except UnicodeError:
            continue
        lines = text.splitlines(keepends=True)
        # Favor excerpts around task terms; keep exact line references.
        hits = [i for i, line in enumerate(lines) if any(w in line.lower() for w in words)]
        start = max(0, hits[0] - 8) if hits and name.endswith('.py') else 0
        excerpt = ''.join(lines[start:start + 100])[:min(4500, remaining)]
        extracts.append({'path': name, 'sha256': digest(data), 'first_line': start + 1,
                         'excerpt': excerpt, 'truncated': start > 0 or len(excerpt) < len(text)})
        remaining -= len(excerpt)
    routes = [dict(route, selection={'score': score, 'terms': matched, 'changed_paths': overlaps})
              for score, _, route, matched, overlaps in selected_routes]
    return {'version': 1, 'kind': 'task_packet', 'task': task,
            'source': dev.context(repo), 'base': base_sha, 'changed_paths': changes,
            'catalog_sha256': digest(source(repo, CATALOG, names).read_bytes()),
            'routes': routes, 'extracts': extracts, 'unavailable_sources': unavailable,
            'impact': {'edges': [{'importer': a, 'imported': b} for a, b in impact[:150]],
                       'truncated': len(impact) > 150, 'parse_limits': unresolved},
            'suggested_tests': sorted({p for route in routes for p in route['tests']}),
            'budget': {'max_characters': max_chars, 'used_characters': max_chars - remaining,
                       'max_files': 24},
            'retrieval_limits': ['At most three matching routes; no match requires explicit source discovery.',
                                 'Excerpts are incomplete; read full definitions before dependent edits.'],
            'certified': False, 'limits': LIMITS}


def freshness(value, repo=ROOT):
    if value.get('kind') != 'task_packet' or value.get('version') != 1:
        raise ValueError('Expected version 1 task packet')
    current = dev.context(repo)
    old = value['source']
    fields = ['head', 'tracked_diff_sha256', 'status_porcelain_z']
    changed = [key for key in fields if old.get(key) != current.get(key)]
    names = tracked(repo)
    files = []
    for item in value['extracts']:
        try:
            valid = digest(source(repo, item['path'], names).read_bytes()) == item['sha256']
        except ValueError:
            valid = False
        if not valid:
            files.append(item['path'])
    return {'version': 1, 'kind': 'packet_freshness', 'fresh': not changed and not files,
            'changed_source_fields': changed, 'changed_files': files,
            'remote_freshness_verified': False, 'limits': LIMITS}


def validate_spec(spec, repo=ROOT):
    if spec.get('version') != 1 or not isinstance(spec.get('task'), str):
        raise ValueError('Expected version 1 task specification with task text')
    criteria = spec.get('criteria', [])
    if not criteria or len(criteria) > 32:
        raise ValueError('Supply 1..32 explicit acceptance criteria')
    seen = set()
    commands = []
    for item in criteria:
        identity = item.get('id', '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,60}', identity) or identity in seen:
            raise ValueError('Criterion IDs must be unique safe identifiers')
        seen.add(identity)
        if not item.get('description'):
            raise ValueError('Every criterion needs a meaningful description')
        kind = item.get('kind')
        if kind == 'test':
            target = item.get('target', '')
            name = target.split('::')[0]
            if not name.startswith('tests/') or not name.endswith('.py'):
                raise ValueError('Test target must be a tracked tests/*.py node')
            source(repo, name)
            commands.append(dev.pytest_command(['--', target]))
        elif kind == 'retained':
            script = item.get('target')
            known = dict(dev.retained_commands(repo))
            if script not in known:
                raise ValueError('Retained target must be declared by existing CI')
            source(repo, script)
            commands.append([sys.executable, script, '--output', known[script]])
        elif kind == 'manual':
            commands.append(None)
        else:
            raise ValueError('Unsupported criterion kind; arbitrary commands are not accepted')
    return commands


def acceptance(spec, output, repo=ROOT, timeout=180):
    repo = Path(repo).resolve()
    commands = validate_spec(spec, repo)
    output = outside(output, repo)
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Use a new empty evidence directory')
    before = dev.context(repo)
    results = []
    stopped = False
    for item, command in zip(spec['criteria'], commands):
        result = {'id': item['id'], 'description': item['description'], 'status': 'pending'}
        if command is None:
            result['reason'] = 'Requires actual observed acceptance; never inferred from tests'
        elif stopped:
            result['reason'] = 'Earlier command failed; resume after resolving it'
        else:
            argv = list(command)
            if item['kind'] == 'retained':
                argv[-1] = str(output / (item['id'] + '.json'))
            logfile = output / (item['id'] + '.log')
            started = datetime.now(timezone.utc).isoformat()
            clock = time.monotonic()
            try:
                with logfile.open('x', encoding='utf-8') as stream:
                    proc = subprocess.run(argv, cwd=repo, env=dict(os.environ, PYTHONUTF8='1', PYTEST_ADDOPTS=''),
                                          stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
                code, error = proc.returncode, None
            except subprocess.TimeoutExpired:
                code, error = 124, 'Timed out; acceptance is incomplete'
            except OSError as exc:
                code, error = 127, str(exc)
            present = item['kind'] != 'retained' or (Path(argv[-1]).is_file() and not Path(argv[-1]).is_symlink())
            result.update(status='passed' if code == 0 and present else 'failed',
                          argv=argv, exit_code=code, error=error, output_present=present,
                          started_utc=started, elapsed_seconds=time.monotonic() - clock,
                          log=logfile.name, log_sha256=digest(logfile.read_bytes()))
            if item['kind'] == 'retained' and present:
                result.update(report=Path(argv[-1]).name,
                              report_sha256=digest(Path(argv[-1]).read_bytes()))
            stopped = result['status'] == 'failed'
        results.append(result)
    after = dev.context(repo)
    report = {'version': 1, 'kind': 'task_acceptance', 'task': spec['task'],
              'spec_sha256': digest(encoded(spec)), 'source': before, 'source_after': after,
              'source_unchanged': before == after, 'criteria': results,
              'all_commands_passed': all(r['status'] == 'passed' for r in results if 'argv' in r)
                                     and any('argv' in r for r in results),
              'all_criteria_passed': before == after and all(r['status'] == 'passed' for r in results),
              'certified': False, 'limits': LIMITS}
    write_report(output / 'acceptance.json', report, repo)
    return report


def resume(spec, evidence_path, repo=ROOT):
    commands = validate_spec(spec, repo)
    evidence_path = Path(evidence_path)
    evidence = read_json(evidence_path)
    if (evidence.get('version') != 1 or evidence.get('kind') != 'task_acceptance'
            or evidence.get('spec_sha256') != digest(encoded(spec))):
        raise ValueError('Evidence does not match this exact task specification')
    results = evidence['criteria']
    if [r['id'] for r in results] != [r['id'] for r in spec['criteria']]:
        raise ValueError('Evidence criteria do not match the specification')
    for criterion, item, command in zip(spec['criteria'], results, commands):
        if item['status'] not in ('passed', 'failed', 'pending'):
            raise ValueError('Invalid evidence status')
        if command is None and item['status'] != 'pending':
            raise ValueError('Manual acceptance cannot be inferred from this runner')
        if item['status'] == 'passed' and ('argv' not in item or item.get('exit_code') != 0
                                          or not item.get('output_present')):
            raise ValueError('Passed criterion lacks successful command evidence')
        if 'argv' in item:
            expected = list(command)
            if criterion['kind'] == 'retained':
                expected[-1] = str(evidence_path.parent / (criterion['id'] + '.json'))
            if item['argv'] != expected:
                raise ValueError('Evidence command does not match the specification')
            log = evidence_path.parent / item['log']
            if (Path(item['log']).name != item['log'] or log.is_symlink()
                    or digest(log.read_bytes()) != item['log_sha256']):
                raise ValueError('Evidence log missing, changed or outside its directory')
            if criterion['kind'] == 'retained' and item['status'] == 'passed':
                report = evidence_path.parent / item.get('report', '')
                if (report.name != item.get('report') or report.is_symlink()
                        or digest(report.read_bytes()) != item.get('report_sha256')):
                    raise ValueError('Retained report missing or changed')
    current = dev.context(repo)
    fields = ['head', 'tracked_diff_sha256', 'status_porcelain_z']
    stale = (not evidence['source_unchanged'] or
             any(evidence['source_after'].get(k) != current.get(k) for k in fields))
    first = next((r for r in results if r['status'] != 'passed'), None)
    return {'version': 1, 'kind': 'task_resume', 'task': spec['task'],
            'owning_record': spec.get('owning_record'), 'source': current,
            'evidence_stale': stale, 'criteria': results,
            'next_step': 'Re-run acceptance at current source' if stale else
                         ('Resolve criterion ' + first['id'] if first else
                          'Required independent review/platform/canon gates remain to be checked'),
            'authorization': {'merge_authorized': False, 'canon_authorized': False,
                              'scope_reference_unverified': spec.get('authorization_reference')},
            'certified': False, 'limits': LIMITS + ['Evidence hashes detect changes, not forged reports.']}


def review(value, repo=ROOT):
    state = freshness(value, repo)
    _, changes = changed_paths(repo, value['base'])
    flags = []
    runtime = any(p.startswith('src/') for p in changes)
    tests = any(p.startswith('tests/') for p in changes)
    if runtime and not tests:
        flags.append('Runtime changed without changed tests: inspect existing coverage and missing cases')
    if any(p.startswith('schemas/') for p in changes):
        flags.append('Schema change: verify explicit compatibility/migration authorization')
    if not state['fresh']:
        flags.append('Packet is stale: rebuild before relying on its excerpts')
    lenses = list(dict.fromkeys(lens for route in value['routes'] for lens in route.get('lenses', [])))
    return {'version': 1, 'kind': 'bounded_review', 'freshness': state,
            'changed_paths': changes, 'flags': flags, 'task_lenses': lenses,
            'questions': ['Does the public route reach the existing owner?',
                          'Do refusal, privacy and restore preserve the actual contract?',
                          'Which player possibilities and durable consequences were demonstrated?',
                          'Are facts, approvals, inferences and proposals distinguished?'],
            'independent_review': False, 'certified': False, 'limits': LIMITS}


def benchmark(cases, answers):
    """Score explicit structured observations, never invent model responses."""
    if cases.get('version') != 1 or answers.get('version') != 1:
        raise ValueError('Benchmark requires version 1 cases and observations')
    observed = {a['id']: a for a in answers['answers']}
    if len(observed) != len(answers['answers']):
        raise ValueError('Duplicate answer IDs')
    rows = []
    seen = set()
    for case in cases['cases']:
        identity = case['id']
        if identity in seen or not case.get('expected_facts'):
            raise ValueError('Unique cases and explicit expected facts are required')
        seen.add(identity)
        answer = observed.get(identity, {})
        correct = sum(key in answer.get('facts', {}) and answer['facts'][key] == value
                      for key, value in case['expected_facts'].items())
        forbidden = [claim for claim in case.get('forbidden_claims', [])
                     if claim in answer.get('claims', [])]
        rows.append({'id': identity, 'correct_facts': correct,
                     'expected_facts': len(case['expected_facts']), 'forbidden_claims': forbidden,
                     'complete': correct == len(case['expected_facts']) and not forbidden,
                     'observation_reference': answer.get('observation_reference'),
                     'elapsed_seconds': answer.get('elapsed_seconds'),
                     'interactions': answer.get('interactions')})
    if set(observed) - seen:
        raise ValueError('Unknown answer case IDs')
    return {'version': 1, 'kind': 'chat_benchmark', 'cases': rows,
            'completed_cases': sum(row['complete'] for row in rows),
            'total_cases': len(rows), 'certified': False,
            'limits': ['Exact structured-fact scoring only; not a semantic judge.',
                       'Observation references and timings are supplied, not independently authenticated.',
                       'Compare measured same-task/model conditions before claiming improvement.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('packet')
    p.add_argument('--task', required=True)
    p.add_argument('--base', default='origin/main')
    p = sub.add_parser('refresh')
    p.add_argument('--packet', type=Path, required=True)
    p = sub.add_parser('review')
    p.add_argument('--packet', type=Path, required=True)
    p = sub.add_parser('check')
    p.add_argument('--spec', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=180)
    p = sub.add_parser('resume')
    p.add_argument('--spec', type=Path, required=True)
    p.add_argument('--evidence', type=Path, required=True)
    p = sub.add_parser('benchmark')
    p.add_argument('--cases', type=Path, required=True)
    p.add_argument('--answers', type=Path, required=True)
    for command in sub.choices.values():
        command.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'packet':
            result = packet(args.task, args.base)
        elif args.command in ('refresh', 'review'):
            value = read_json(args.packet)
            result = freshness(value) if args.command == 'refresh' else review(value)
        elif args.command == 'check':
            if not 1 <= args.timeout <= 1800:
                raise ValueError('Timeout must be 1..1800 seconds per criterion')
            result = acceptance(read_json(args.spec), args.output, timeout=args.timeout)
            print(json.dumps({'output': str(args.output / 'acceptance.json'),
                              'all_criteria_passed': result['all_criteria_passed']}))
            return 0 if result['all_criteria_passed'] else 1
        elif args.command == 'resume':
            result = resume(read_json(args.spec), args.evidence)
        else:
            result = benchmark(read_json(args.cases), read_json(args.answers))
        write_report(args.output, result, ROOT)
        print(json.dumps({'output': str(args.output), 'kind': result['kind']}))
        return 1 if args.command == 'refresh' and not result['fresh'] else 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    raise SystemExit(main())
