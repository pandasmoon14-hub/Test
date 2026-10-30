"""Report-only Part 3 graph, inventory and lawful round-trip coverage."""
from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "myravant_runtime_structure_audit",
    ROOT / "scripts" / "myravant_runtime_structure_audit.py",
)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def test_current_source_report_is_deterministic_complete_and_report_only():
    first = audit.structure_report(ROOT)
    second = audit.structure_report(ROOT)
    assert first == second
    assert first["schema"] == "myravant.runtime-structure-audit.v1"
    encoded = json.dumps(first, sort_keys=True, indent=2) + "\n"
    assert encoded == json.dumps(second, sort_keys=True, indent=2) + "\n"
    graph = first["graph"]
    assert graph["entrypoint"] in graph["reachable"]
    assert "astra_runtime.myravant_service_commitment" in graph["nodes"]
    assert set(graph["reachable"]).isdisjoint(graph["not_reachable"])
    assert set(graph["reachable"]) | set(graph["not_reachable"]) == set(graph["nodes"])
    assert all(edge == sorted(edge) or len(edge) == 2 for edge in graph["edges"])
    assert all(isinstance(cycle, list) for cycle in graph["cycles"])
    inv = first["inventories"]
    assert "myravant_service_commitment.py" in inv["profile_owners"]
    assert not inv["root_unregistered"]
    assert not inv["root_registered_missing"]
    assert not inv["root_dual_classified"]
    assert not inv["domain_unregistered"]
    assert not inv["domain_registered_missing"]
    assert len(first["locality_bindings"]) == len(audit.BINDING_CLASSES) == 15
    assert set(first["installed_locality_journey_source_references"]["literal_by_binding"]) == set(audit.BINDING_CLASSES)
    assert all(item["roundtrip"] == "not_run_static_report"
               for item in first["locality_bindings"])
    assert any(item["function"].startswith("restore_")
               for item in first["checkpoint_writer_restore_entrypoints"])
    assert any(item["function"].startswith("write_")
               for item in first["checkpoint_writer_restore_entrypoints"])


def test_cli_matches_source_choice_registry_and_real_application_classes():
    sources = audit.source_modules(ROOT)
    graph = audit.structure_report(ROOT)
    choices = audit.locality_choices(
        ast.parse((ROOT / "src/astra_runtime/myravant_terminal.py").read_text())
    )
    assert choices == [row["locality"] for row in graph["locality_bindings"]]
    assert set(choices) == set(audit.BINDING_CLASSES)
    for binding in graph["locality_bindings"]:
        qualified = binding["application"]
        module, _, name = qualified.rpartition(".")
        assert module in sources
        tree = ast.parse(sources[module].read_text())
        contract = audit.class_contract(tree, name)
        assert contract == binding["contract"]


def test_planted_import_cycle_sibling_import_and_terminal_backedge_are_reported(tmp_path):
    base = tmp_path / "src" / "astra_runtime"
    base.mkdir(parents=True)
    (base / "__init__.py").write_text("")
    (base / "myravant_terminal.py").write_text(
        "from astra_runtime import myravant_a\n"
    )
    (base / "myravant_a.py").write_text(
        "from . import myravant_b\n"
    )
    (base / "myravant_b.py").write_text(
        "import astra_runtime.myravant_a\n"
    )
    (base / "myravant_action_application.py").write_text(
        "import astra_runtime.myravant_terminal\n"
    )
    paths = audit.source_modules(tmp_path)
    trees = {name: ast.parse(path.read_text()) for name, path in paths.items()}
    graph = audit.import_report(paths, trees)
    assert ["astra_runtime.myravant_a", "astra_runtime.myravant_b"] in graph["cycles"]
    assert ["astra_runtime.myravant_action_application",
            "astra_runtime.myravant_terminal"] in graph["application_to_terminal"]
    assert ["astra_runtime.myravant_a",
            "astra_runtime.myravant_b"] in graph["root_sibling_imports"]
    assert "astra_runtime.myravant_b" in graph["reachable"]
    assert "astra_runtime.myravant_action_application" in graph["not_reachable"]


def test_planted_unregistered_root_owner_and_domain_file_are_reported(tmp_path):
    test_root = tmp_path / "tests"
    test_root.mkdir()
    (test_root / "runtime_profile_owner_manifest.py").write_text(
        'PROFILE_LOCAL_OWNER_FILES = frozenset({"myravant_service_commitment.py"})\n'
        'REGISTERED_ROOT_NON_OWNER_FILES = frozenset({"myravant_terminal.py"})\n'
    )
    (test_root / "runtime_domain_package_manifest.py").write_text(
        'AUTHORIZED_RUNTIME_DOMAIN_FILES = frozenset({"__init__.py"})\n'
    )
    src = tmp_path / "src" / "astra_runtime"
    src.mkdir(parents=True)
    (src / "domain").mkdir()
    (src / "domain" / "__init__.py").write_text("")
    (src / "domain" / "new_custody.py").write_text("pass\n")
    for name in ("myravant_terminal.py", "myravant_service_commitment.py",
                 "myravant_new_settlement.py"):
        (src / name).write_text("pass\n")
    paths = audit.source_modules(tmp_path)
    trees = {name: ast.parse(p.read_text()) for name, p in paths.items()}
    graph = audit.import_report(paths, trees)
    result = audit.inventory_report(tmp_path, graph)
    assert result["root_unregistered"] == ["myravant_new_settlement.py"]
    assert result["domain_unregistered"] == ["new_custody.py"]
    assert result["unreachable_profile_owners"] == [
        "astra_runtime.myravant_service_commitment"
    ]



def test_installed_locality_source_inventory_reports_literals_and_dynamic_refs(tmp_path):
    tests = tmp_path / "tests"
    scripts = tmp_path / "scripts"
    tests.mkdir()
    scripts.mkdir()
    (tests / "test_installed.py").write_text(
        'args = ["myravant-play", "--locality", "tarrow-service"]\n'
    )
    (scripts / "report_dynamic.py").write_text(
        'args = ["myravant-play", "--locality", case]\n'
    )
    evidence = audit.installed_locality_references(tmp_path)
    assert evidence["literal_by_binding"]["tarrow-service"] == [
        "tests/test_installed.py"
    ]
    assert "scripts/report_dynamic.py" in evidence["computed_or_unrecognized_argv_sources"]
    assert "generated-worksite" in evidence["no_literal_argv_evidence"]
    assert "not proof" in evidence["qualification"]


def test_report_only_scan_never_imports_runtime(tmp_path, monkeypatch):
    """No world state, provider, RNG, checkpoint or runtime API is touched."""
    src = tmp_path / "src" / "astra_runtime"
    src.mkdir(parents=True)
    (src / "myravant_terminal.py").write_text(
        "raise RuntimeError('executed runtime source')\n"
        "import astra_runtime.no_such_runtime\n"
    )
    paths = audit.source_modules(tmp_path)
    trees = {name: ast.parse(p.read_text()) for name, p in paths.items()}
    graph = audit.import_report(paths, trees)
    assert graph["reachable"] == ["astra_runtime.myravant_terminal"]


@pytest.mark.parametrize("binding", sorted(audit.BINDING_CLASSES))
def test_actual_binding_roundtrip_preserves_authoritative_digest(binding, tmp_path):
    """Every public binding uses its own actual backend checkpoint writer/replay."""
    result = audit.verify_binding_roundtrip(binding, tmp_path / binding)
    assert result["equal"]
    assert len(result["before_digest"]) == 64
    assert result["before_digest"] == result["restored_digest"]
    assert len(result["checkpoint_sha256"]) == 64
    assert isinstance(result["replay_methods"], list)
    assert isinstance(result["format_identity"], str) and result["format_identity"]
    assert isinstance(result["format_version"], int)
