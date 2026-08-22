import subprocess
import sys

import pytest

from tests.helpers import (
    REGISTRY_PATH,
    ROOT,
    normalize_nested_pytest_command,
    read_utf8,
    registry_records_by_id,
)


SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(autouse=True)
def nested_pytest_uses_active_interpreter(monkeypatch):
    """Normalize only historical bare `python -m pytest` pass-through calls."""
    original_run = subprocess.run

    def portable_run(args, *pargs, **kwargs):
        return original_run(normalize_nested_pytest_command(args), *pargs, **kwargs)

    monkeypatch.setattr(subprocess, "run", portable_run)


@pytest.fixture
def repo_root():
    return ROOT


@pytest.fixture
def registry_path():
    return REGISTRY_PATH


@pytest.fixture
def registry_records():
    return registry_records_by_id()


@pytest.fixture
def read_text():
    return read_utf8
