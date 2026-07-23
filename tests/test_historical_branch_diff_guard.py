"""Tests for historical branch-scoped diff guardrails."""

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
