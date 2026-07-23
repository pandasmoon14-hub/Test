"""Utilities for historical branch-scoped diff guardrails.

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
