from pathlib import Path
import subprocess
import sys
from typing import Sequence

import pytest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def repo_git_path(path: Path | str) -> str:
    """Return a repository-relative POSIX path for Git object addressing."""
    value = Path(path) if isinstance(path, Path) else None
    if value is not None and value.is_absolute():
        return value.relative_to(ROOT).as_posix()

    normalized = str(path).replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if normalized.startswith("/") or normalized == ".." or normalized.startswith("../") or "/../" in normalized:
        raise ValueError(f"path must be repository-relative: {path!r}")
    return normalized


def git_blob(ref: str, path: Path | str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{ref}:{repo_git_path(path)}"],
        cwd=ROOT,
    )


def git_text(ref: str, path: Path | str) -> str:
    return git_blob(ref, path).decode("utf-8")


def normalize_nested_pytest_command(args: Sequence[object]) -> Sequence[object]:
    """Keep nested pytest runs on the interpreter that launched this test suite."""
    if isinstance(args, (list, tuple)) and len(args) >= 3:
        executable = str(args[0]).replace("\\", "/").rsplit("/", 1)[-1].lower()
        if executable in {"python", "python.exe"} and list(args[1:3]) == ["-m", "pytest"]:
            normalized = [sys.executable, *args[1:]]
            return tuple(normalized) if isinstance(args, tuple) else normalized
    return args


def registry_records_by_id() -> dict[str, dict]:
    yaml = pytest.importorskip(
        "yaml",
        reason=(
            "PyYAML is required for doctrine/registry validation; "
            "install test dependencies with "
            "python3 -m pip install -r requirements-dev.txt"
        ),
    )

    data = yaml.safe_load(read_utf8(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def repo_script(path: str) -> Path:
    return ROOT / path


def run_repo_python(script: str, *args: str, **kwargs) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(repo_script(script)), *args]
    return subprocess.run(cmd, cwd=ROOT, **kwargs)
