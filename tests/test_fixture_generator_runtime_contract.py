from __future__ import annotations

"""Fixture-generator/runtime file contract tests.

These checks only verify that fixture-generation support files exist and that the
fixture-generator script can run in this repository runtime context. They do not
exercise the full extraction pipeline end-to-end.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SCRIPT = ROOT / 'tests' / 'fixtures' / 'generate_fixture_pdfs.py'


@pytest.mark.skipif(not FIXTURE_SCRIPT.exists(), reason='fixture generator missing')
def test_fixture_generator_runtime_contract_runs_from_repo_root():
    proc = subprocess.run(
        [sys.executable, str(FIXTURE_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if proc.returncode != 0 and 'PyMuPDF required' in (proc.stderr + proc.stdout):
        pytest.skip('PyMuPDF unavailable in environment')
    assert proc.returncode == 0, proc.stderr


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
