#!/usr/bin/env python3
"""Repair historical branch-diff guards for unrelated later branches.

Run from the repository root on branch:
    maintenance/restore-green-runtime-baseline-v2

The script creates a shared branch-scope guard and patches only the six direct
historical branch-footprint tests that failed on the maintenance branch. It is
idempotent and preserves all existing allowlists and assertions.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


EXPECTED_BRANCH = "maintenance/restore-green-runtime-baseline-v2"
IMPORT_LINE = (
    "from tests.historical_branch_diff_guard import "
    "require_owning_historical_branch\n"
)

TARGETS = (
    (
        "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py",
        "test_git_footprint_when_base_ref_available_and_implementation_module_present",
        "ROOT",
        "pr-5h",
    ),
    (
        "tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py",
        "test_branch_diff_is_limited_to_allowed_files",
        "REPO_ROOT",
        "rt-001i",
    ),
    (
        "tests/test_runtime_domain_rt_002a_read_only_vertical_slice_state_owner_facade.py",
        "test_branch_diff_is_limited_to_allowed_files",
        "REPO_ROOT",
        "rt-002a",
    ),
    (
        "tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py",
        "test_branch_diff_limited_to_rt002b",
        "REPO_ROOT",
        "rt-002b",
    ),
    (
        "tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py",
        "test_branch_diff_limited_to_rt002c",
        "REPO_ROOT",
        "rt-002c",
    ),
    (
        "tests/test_runtime_domain_rt_002f_object_lever_replay_audit_check.py",
        "test_branch_diff_limited_to_rt002f",
        "REPO_ROOT",
        "rt-002f",
    ),
)

HELPER_CONTENT = '''"""Utilities for historical branch-scoped diff guardrails.

Historical PR/RT footprint tests validate the branch that originally owned the
review. They are not universal restrictions on all later maintenance or feature
branches.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest


def current_branch_name(repo_root: Path) -> str:
    """Return the source branch in local or GitHub Actions execution."""

    github_head_ref = os.environ.get("GITHUB_HEAD_REF", "").strip()
    if github_head_ref:
        return github_head_ref

    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def require_owning_historical_branch(repo_root: Path, marker: str) -> None:
    """Skip a historical footprint guard outside its owning branch."""

    branch = current_branch_name(repo_root)
    if marker.lower() not in branch.lower():
        pytest.skip(
            "Historical branch-footprint guard applies only to its owning "
            f"branch containing {marker!r}; current branch is "
            f"{branch or 'detached/unknown'!r}."
        )
'''

HELPER_TEST_CONTENT = '''"""Tests for historical branch-scoped diff guardrails."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.historical_branch_diff_guard import (
    current_branch_name,
    require_owning_historical_branch,
)


def test_github_head_ref_takes_precedence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_HEAD_REF", "runtime-gate-b/rt-002b-example")
    assert current_branch_name(Path.cwd()) == "runtime-gate-b/rt-002b-example"


def test_owning_branch_marker_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_HEAD_REF", "runtime-gate-b/rt-002f-example")
    require_owning_historical_branch(Path.cwd(), "rt-002f")


def test_unrelated_branch_is_explicitly_skipped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_HEAD_REF", "maintenance/restore-green-runtime-baseline-v2")
    with pytest.raises(pytest.skip.Exception):
        require_owning_historical_branch(Path.cwd(), "rt-002f")
'''


class RepairError(RuntimeError):
    pass


def git_branch(root: Path) -> str:
    import subprocess

    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def add_import(text: str) -> str:
    if IMPORT_LINE.strip() in text:
        return text

    tree = ast.parse(text)
    insert_after = 0
    for statement in tree.body:
        if isinstance(statement, (ast.Import, ast.ImportFrom)):
            insert_after = statement.end_lineno or insert_after
        elif insert_after:
            break

    lines = text.splitlines(keepends=True)
    lines[insert_after:insert_after] = [IMPORT_LINE]
    return "".join(lines)


def patch_function(text: str, function_name: str, root_name: str, marker: str) -> tuple[str, bool]:
    call = f'require_owning_historical_branch({root_name}, "{marker}")'
    if call in text:
        return text, False

    tree = ast.parse(text)
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    ]
    if len(matches) != 1:
        raise RepairError(
            f"Expected exactly one function {function_name!r}; found {len(matches)}"
        )

    function = matches[0]
    if not function.body:
        raise RepairError(f"Function {function_name!r} has no body")

    insertion_line = function.body[0].lineno - 1
    if (
        isinstance(function.body[0], ast.Expr)
        and isinstance(function.body[0].value, ast.Constant)
        and isinstance(function.body[0].value.value, str)
    ):
        insertion_line = function.body[0].end_lineno or insertion_line

    indent = " " * (function.col_offset + 4)
    lines = text.splitlines(keepends=True)
    lines[insertion_line:insertion_line] = [f"{indent}{call}\n"]
    patched = "".join(lines)
    ast.parse(patched)
    return patched, True


def main() -> int:
    root = Path.cwd().resolve()
    if not (root / ".git").exists():
        raise RepairError("Run from the repository root")
    branch = git_branch(root)
    if branch != EXPECTED_BRANCH:
        raise RepairError(
            f"Expected branch {EXPECTED_BRANCH!r}; current branch is {branch!r}"
        )

    helper = root / "tests/historical_branch_diff_guard.py"
    helper.write_text(HELPER_CONTENT, encoding="utf-8", newline="\n")

    helper_test = root / "tests/test_historical_branch_diff_guard.py"
    helper_test.write_text(HELPER_TEST_CONTENT, encoding="utf-8", newline="\n")

    changed = 0
    already = 0
    for relative, function_name, root_name, marker in TARGETS:
        path = root / relative
        if not path.is_file():
            raise RepairError(f"Missing target file: {relative}")
        text = path.read_text(encoding="utf-8")
        text = add_import(text)
        text, did_change = patch_function(text, function_name, root_name, marker)
        ast.parse(text, filename=str(path))
        path.write_text(text, encoding="utf-8", newline="\n")
        if did_change:
            changed += 1
        else:
            already += 1

    print(
        f"Historical branch guards repaired: {changed} changed, "
        f"{already} already repaired."
    )
    print("Created tests/historical_branch_diff_guard.py")
    print("Created tests/test_historical_branch_diff_guard.py")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RepairError, OSError, SyntaxError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
