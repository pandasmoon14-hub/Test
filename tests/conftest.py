from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


@pytest.fixture(autouse=True)
def _repo_root_cwd(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def registry_records_by_id() -> dict[str, dict]:
    import yaml

    data = yaml.safe_load(read_utf8(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def repo_script(path: str) -> Path:
    return ROOT / path


def run_repo_python(script: str, *args: str, **kwargs) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(repo_script(script)), *args]
    return subprocess.run(cmd, cwd=ROOT, **kwargs)
