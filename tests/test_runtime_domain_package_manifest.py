"""Focused guardrails for the shared runtime-domain package manifest."""

from __future__ import annotations

from pathlib import Path

from tests.runtime_domain_package_manifest import (
    AUTHORIZED_RUNTIME_DOMAIN_FILES,
    missing_runtime_domain_files,
    unauthorized_runtime_domain_files,
)


ROOT = Path(__file__).resolve().parents[1]


def test_runtime_domain_manifest_matches_current_package() -> None:
    assert not unauthorized_runtime_domain_files(ROOT)
    assert not missing_runtime_domain_files(ROOT)


def test_runtime_source_does_not_import_test_manifest() -> None:
    runtime_root = ROOT / "src" / "astra_runtime"
    forbidden = "tests.runtime_domain_package_manifest"
    for path in runtime_root.rglob("*.py"):
        assert forbidden not in path.read_text(encoding="utf-8")


def test_manifest_remains_explicit_and_nonempty() -> None:
    assert "__init__.py" in AUTHORIZED_RUNTIME_DOMAIN_FILES
    assert "state_store.py" in AUTHORIZED_RUNTIME_DOMAIN_FILES
    assert "object_lever_replay_audit_check.py" in AUTHORIZED_RUNTIME_DOMAIN_FILES
    assert len(AUTHORIZED_RUNTIME_DOMAIN_FILES) == len(set(AUTHORIZED_RUNTIME_DOMAIN_FILES))
