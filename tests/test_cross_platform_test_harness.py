from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tests.helpers import (
    ROOT,
    git_text,
    normalize_nested_pytest_command,
    repo_git_path,
)


def test_repo_git_path_uses_posix_repository_identity():
    absolute = ROOT / "docs" / "doctrine" / "reviews" / "example.yaml"
    assert repo_git_path(absolute) == "docs/doctrine/reviews/example.yaml"
    assert repo_git_path(r"docs\doctrine\reviews\example.yaml") == "docs/doctrine/reviews/example.yaml"
    assert "\\" not in repo_git_path(absolute)


def test_repo_git_path_rejects_parent_traversal():
    with pytest.raises(ValueError):
        repo_git_path("../outside.txt")


def test_git_text_reads_committed_blob_with_repository_path_rules():
    text = git_text("HEAD", "tests/helpers.py")
    assert "def repo_git_path" in text
    assert "def normalize_nested_pytest_command" in text


def test_src_tree_is_importable_without_external_pythonpath():
    import astra_runtime

    src_root = (ROOT / "src").resolve()
    module_path = Path(astra_runtime.__file__).resolve()
    assert str(src_root) in sys.path
    assert module_path.is_relative_to(src_root)


def test_nested_pytest_normalization_uses_active_interpreter():
    command = ["python", "-m", "pytest", "--version"]
    normalized = normalize_nested_pytest_command(command)
    assert normalized[0] == sys.executable
    assert normalized[1:] == command[1:]


def test_nested_pytest_normalization_preserves_tuple_shape():
    command = ("python.exe", "-m", "pytest", "--version")
    normalized = normalize_nested_pytest_command(command)
    assert isinstance(normalized, tuple)
    assert normalized[0] == sys.executable
    assert normalized[1:] == command[1:]


def test_non_pytest_python_command_is_not_rewritten():
    command = ["python", "-c", "print('unchanged')"]
    assert normalize_nested_pytest_command(command) is command


def test_nested_bare_python_pytest_runs_in_active_environment():
    result = subprocess.run(
        ["python", "-m", "pytest", "--version"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "pytest" in result.stdout.lower()
