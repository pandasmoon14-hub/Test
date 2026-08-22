from __future__ import annotations

"""Fixture-generator/runtime file contract tests.

These checks only verify that fixture-generation support files exist and that the
fixture-generator script can run in this repository runtime context. They do not
exercise the full extraction pipeline end-to-end.
"""

import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SCRIPT = ROOT / 'tests' / 'fixtures' / 'generate_fixture_pdfs.py'
FIXTURE_DIR = ROOT / 'tests' / 'fixtures' / 'pdfs'
FIXTURE_NAMES = {
    'single_column_prose.pdf',
    'two_column_rules.pdf',
    'dense_table.pdf',
    'blank_page.pdf',
    'image_only_scan_like.pdf',
    'multi_page_mixed_10_pages.pdf',
}


def _fixture_hashes() -> dict[str, str]:
    return {
        name: hashlib.sha256((FIXTURE_DIR / name).read_bytes()).hexdigest()
        for name in FIXTURE_NAMES
    }


@pytest.mark.skipif(not FIXTURE_SCRIPT.exists(), reason='fixture generator missing')
def test_fixture_generator_runtime_contract_runs_from_repo_root(tmp_path):
    before = _fixture_hashes()
    isolated_output = tmp_path / 'pdfs'
    env = os.environ.copy()
    env['ASTRA_FIXTURE_OUTPUT_DIR'] = str(isolated_output)

    proc = subprocess.run(
        [sys.executable, str(FIXTURE_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=env,
    )
    if proc.returncode != 0 and 'PyMuPDF required' in (proc.stderr + proc.stdout):
        pytest.skip('PyMuPDF unavailable in environment')
    assert proc.returncode == 0, proc.stderr
    assert {p.name for p in isolated_output.iterdir() if p.is_file()} == FIXTURE_NAMES
    assert _fixture_hashes() == before, 'fixture generator modified tracked PDF fixtures'


def test_fixture_generator_runtime_contract_required_files_present():
    required = [
        ROOT / 'audit_runtime.py',
        ROOT / 'validate_outputs.py',
        ROOT / 'V13_STABILIZATION.md',
        ROOT / 'tests' / 'fixtures' / 'generate_fixture_pdfs.py',
        ROOT / 'tests' / 'test_fixture_generator_runtime_contract.py',
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, f"Missing required files: {missing}"
