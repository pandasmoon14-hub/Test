from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_SCRIPT = ROOT / 'tests' / 'fixtures' / 'generate_fixture_pdfs.py'


@pytest.mark.skipif(not FIXTURE_SCRIPT.exists(), reason='fixture generator missing')
def test_fixture_generator_exists_and_runs():
    proc = subprocess.run([sys.executable, str(FIXTURE_SCRIPT)], capture_output=True, text=True)
    if proc.returncode != 0 and 'PyMuPDF required' in (proc.stderr + proc.stdout):
        pytest.skip('PyMuPDF unavailable in environment')
    assert proc.returncode == 0, proc.stderr


def test_required_v13_files_present():
    required = [
        ROOT / 'audit_runtime.py',
        ROOT / 'validate_outputs.py',
        ROOT / 'V13_STABILIZATION.md',
        ROOT / 'tests' / 'fixtures' / 'generate_fixture_pdfs.py',
        ROOT / 'tests' / 'test_end_to_end_fixtures.py',
    ]
    missing = [str(p) for p in required if not p.exists()]
    assert not missing, f"Missing required files: {missing}"
