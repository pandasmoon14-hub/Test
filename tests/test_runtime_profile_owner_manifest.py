"""Exact root-level profile-owner boundary, independent of domain/ manifest."""
from __future__ import annotations

import ast
from pathlib import Path

from tests.runtime_profile_owner_manifest import (
    PROFILE_LOCAL_OWNER_FILES,
    PROFILE_OWNER_WITNESSES,
    REGISTERED_ROOT_NON_OWNER_FILES,
    missing_registered_runtime_root_files,
    unregistered_runtime_root_files,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "src" / "astra_runtime"


def test_root_inventory_exactly_matches_registered_owner_and_nonowner_files():
    assert PROFILE_LOCAL_OWNER_FILES.isdisjoint(REGISTERED_ROOT_NON_OWNER_FILES)
    assert not unregistered_runtime_root_files(ROOT), (
        "New root-level Python module requires owner/non-owner classification"
    )
    assert not missing_registered_runtime_root_files(ROOT)


def test_profile_owner_list_and_source_contract_witnesses_remain_explicit():
    assert set(PROFILE_OWNER_WITNESSES) == PROFILE_LOCAL_OWNER_FILES
    assert "myravant_service_commitment.py" in PROFILE_LOCAL_OWNER_FILES
    for filename, witnesses in PROFILE_OWNER_WITNESSES.items():
        tree = ast.parse((PACKAGE / filename).read_text(encoding="utf-8"))
        defined = {node.name for node in tree.body
                   if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                        ast.ClassDef))}
        assert set(witnesses) <= defined, (filename, set(witnesses) - defined)


def test_profile_owner_registry_does_not_leak_into_runtime_source():
    needle = "tests.runtime_profile_owner_manifest"
    for source in PACKAGE.rglob("*.py"):
        assert needle not in source.read_text(encoding="utf-8"), source


def test_mutation_control_unregistered_new_authority_owner_is_rejected(tmp_path):
    """A planted root owner must require registration even before its import."""
    package = tmp_path / "src" / "astra_runtime"
    package.mkdir(parents=True)
    injected = package / "myravant_unregistered_settlement.py"
    injected.write_text(
        "from dataclasses import dataclass\\n"
        "@dataclass(frozen=True)\\n"
        "class SettlementState:\\n"
        "    accepted: bool = False\\n"
        "def settle(state):\\n"
        "    return SettlementState(accepted=True)\\n",
        encoding="utf-8",
    )
    assert unregistered_runtime_root_files(tmp_path) == frozenset({injected.name})
    assert injected.name not in PROFILE_LOCAL_OWNER_FILES


def test_mutation_control_new_adapter_is_not_silently_exempt(tmp_path):
    """Even non-owning newcomers need a deliberate recorded classification."""
    package = tmp_path / "src" / "astra_runtime"
    package.mkdir(parents=True)
    injected = package / "myravant_new_presentation_adapter.py"
    injected.write_text('"""Non-owning client adapter."""\\n', encoding="utf-8")
    assert unregistered_runtime_root_files(tmp_path) == frozenset({injected.name})
