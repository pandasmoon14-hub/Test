"""Read-only Myravant runtime structure and binding evidence.

Imports are parsed, NEVER imported during graph construction. The import graph
describes coupling, not semantic authority. Owner classification is sourced
from the two existing test inventories; no owner is inferred from graph edges.

An optional, explicitly selected verifier uses actual existing application
save/restore paths for every installed locality binding. It does not synthesize
or modify committed gameplay outcomes.
"""
from __future__ import annotations

import argparse
import ast
from collections import deque
import hashlib
import importlib
import json
from pathlib import Path
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "myravant.runtime-structure-audit.v1"
ENTRYPOINT = "astra_runtime.myravant_terminal"

# Transcribed from the installed terminal's application_type selections, rather
# than deduced from class names or presumed universal semantics. Source choices
# and each declared class are checked on every audit run.
BINDING_CLASSES = {
    "development": "astra_runtime.myravant_vsm14_application.MyravantVSM14Application",
    "tarrow": "astra_runtime.myravant_play_application.MyravantPlayApplication",
    "tarrow-depth": "astra_runtime.myravant_play_application.MyravantPlayApplication",
    "tarrow-material": "astra_runtime.myravant_material_application.MaterialApplication",
    "tarrow-water": "astra_runtime.myravant_water_application.WaterApplication",
    "tarrow-time": "astra_runtime.myravant_timed_application.TimedApplication",
    "tarrow-actors": "astra_runtime.myravant_actor_application.ActorApplication",
    "tarrow-service": "astra_runtime.myravant_service_application.ServiceApplication",
    "tarrow-surface-water": "astra_runtime.myravant_surface_water_application.SurfaceWaterApplication",
    "tarrow-structures": "astra_runtime.myravant_structures_application.StructuresApplication",
    "tarrow-activities": "astra_runtime.myravant_activity_application.ActivityApplication",
    "tarrow-investigation": "astra_runtime.myravant_investigation_application.InvestigationApplication",
    "tarrow-transformation": "astra_runtime.myravant_transformation_application.TransformationApplication",
    "generated-worksite": "astra_runtime.myravant_investigation_application.InvestigationApplication",
}


def source_modules(repo_root: Path) -> dict[str, Path]:
    base = repo_root / "src" / "astra_runtime"
    paths = {}
    for path in sorted(base.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        relative = path.relative_to(repo_root / "src")
        parts = relative.with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        paths[".".join(parts)] = path
    return paths


def imported_modules(module: str, path: Path, tree: ast.AST,
                     available: set[str]) -> set[str]:
    """Resolve only imports that name an existing local source module."""
    parent = module if path.name == "__init__.py" else module.rpartition(".")[0]
    edges = set()

    def admit(qualified: str) -> None:
        if qualified in available:
            edges.add(qualified)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                admit(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                prefix = parent.split(".")
                remove = node.level - 1
                if remove >= len(prefix):
                    continue
                prefix = prefix[:len(prefix) - remove] if remove else prefix
                package = ".".join(prefix)
                base = package + ("." + node.module if node.module else "")
            else:
                base = node.module or ""
            if not base.startswith("astra_runtime"):
                continue
            admit(base)
            for alias in node.names:
                if alias.name != "*":
                    admit(base + "." + alias.name)
    return edges


def cycles(nodes: set[str], edges: dict[str, set[str]]) -> list[list[str]]:
    """Sorted strongly connected components; cycles are reported, not gated."""
    index = 0
    stack = []
    active = set()
    ranks = {}
    low = {}
    results = []

    def visit(v: str) -> None:
        nonlocal index
        ranks[v] = low[v] = index
        index += 1
        stack.append(v)
        active.add(v)
        for w in sorted(edges[v]):
            if w not in ranks:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in active:
                low[v] = min(low[v], ranks[w])
        if low[v] == ranks[v]:
            component = []
            while True:
                w = stack.pop()
                active.remove(w)
                component.append(w)
                if w == v:
                    break
            if len(component) > 1 or v in edges[v]:
                results.append(sorted(component))

    for item in sorted(nodes):
        if item not in ranks:
            visit(item)
    return sorted(results)


def import_report(modules: dict[str, Path], trees: dict[str, ast.AST],
                  entrypoint: str = ENTRYPOINT) -> dict:
    available = set(modules)
    if entrypoint not in available:
        raise ValueError("terminal entrypoint does not exist in source tree")
    edges = {key: imported_modules(key, path, trees[key], available)
             for key, path in modules.items()}
    reached = {entrypoint}
    queue = deque([entrypoint])
    while queue:
        for name in sorted(edges[queue.popleft()]):
            if name not in reached:
                reached.add(name)
                queue.append(name)
    root_files = {n for n, p in modules.items() if p.parent.name == "astra_runtime"}
    connections = sorted([src, dst] for src in edges for dst in edges[src])
    return {
        "entrypoint": entrypoint,
        "nodes": sorted(available),
        "edges": connections,
        "reachable": sorted(reached),
        "not_reachable": sorted(available - reached),
        "cycles": cycles(available, edges),
        "root_sibling_imports": sorted([src, dst] for src, dst in connections
                                       if src in root_files and dst in root_files),
        "application_to_terminal": sorted([src, dst] for src, dst in connections
            if src.endswith("_application") and dst == ENTRYPOINT),
        "source_sha256": {key: hashlib.sha256(path.read_bytes()).hexdigest()
                          for key, path in sorted(modules.items())},
    }


def _literal_set(path: Path, assignment: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for item in tree.body:
        if isinstance(item, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == assignment
                   for t in item.targets):
                value = item.value
                if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "frozenset":
                    value = value.args[0]
                found = ast.literal_eval(value)
                if not isinstance(found, (set, frozenset)) or not all(
                    isinstance(x, str) for x in found
                ):
                    raise ValueError("inventory is not an explicit string set: " + assignment)
                return set(found)
    raise ValueError("missing authoritative test inventory: " + assignment)


def inventory_report(repo_root: Path, graph: dict) -> dict:
    test_root = repo_root / "tests"
    root = repo_root / "src" / "astra_runtime"
    profile = test_root / "runtime_profile_owner_manifest.py"
    domain = test_root / "runtime_domain_package_manifest.py"
    owners = _literal_set(profile, "PROFILE_LOCAL_OWNER_FILES")
    nonowners = _literal_set(profile, "REGISTERED_ROOT_NON_OWNER_FILES")
    domain_names = _literal_set(domain, "AUTHORIZED_RUNTIME_DOMAIN_FILES")
    actual_root = {p.name for p in root.glob("*.py")}
    actual_domain = {p.name for p in (root / "domain").glob("*.py")}
    reachable = set(graph["reachable"])
    return {
        "profile_owners": sorted(owners),
        "root_nonowners": sorted(nonowners),
        "root_unregistered": sorted(actual_root - owners - nonowners),
        "root_registered_missing": sorted((owners | nonowners) - actual_root),
        "root_dual_classified": sorted(owners & nonowners),
        "domain_authorized": sorted(domain_names),
        "domain_unregistered": sorted(actual_domain - domain_names),
        "domain_registered_missing": sorted(domain_names - actual_domain),
        "reachable_profile_owners": sorted(
            "astra_runtime." + n[:-3] for n in owners
            if "astra_runtime." + n[:-3] in reachable),
        "unreachable_profile_owners": sorted(
            "astra_runtime." + n[:-3] for n in owners
            if "astra_runtime." + n[:-3] not in reachable),
        "classification_note": (
            "Registration is a human-reviewed claim, not proof of semantic ownership. "
            "Import, storage, scheduling, serialization and checkpoint transport do "
            "not confer ownership. All graph findings remain report-only."
        ),
    }


def locality_choices(tree: ast.AST) -> list[str]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "add_argument" or not node.args:
            continue
        if not isinstance(node.args[0], ast.Constant) or node.args[0].value != "--locality":
            continue
        for keyword in node.keywords:
            if keyword.arg == "choices":
                value = ast.literal_eval(keyword.value)
                return list(value)
    raise ValueError("public terminal --locality choices not found")


def class_contract(tree: ast.AST, class_name: str) -> dict:
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    if class_name not in classes:
        raise ValueError("binding application class missing from source: " + class_name)
    found = classes[class_name]
    variables = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                variables[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    values = {}
    for node in found.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"checkpoint_format", "replay_methods"}:
                    try:
                        val = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        val = variables.get(node.value.id) if isinstance(node.value, ast.Name) else None
                    values[target.id] = {"declared_value": val,
                                         "expression": ast.unparse(node.value)}
    methods = sorted(node.name for node in found.body if isinstance(
        node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    return {
        "bases": [ast.unparse(x) for x in found.bases],
        "checkpoint_format": values.get("checkpoint_format"),
        "replay_methods": values.get("replay_methods"),
        "declares_save": "save" in methods,
        "declares_restore": "restore" in methods,
        "declares_authoritative_digest": "authoritative_digest" in methods,
        "note": "Absent declarations may be inherited; no methods or formats were executed.",
    }


def checkpoint_procedures(trees: dict[str, ast.AST]) -> list[dict]:
    """Enumerate distinct implementation entrypoints, without assuming ownership."""
    rows = []
    for module, tree in sorted(trees.items()):
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                "checkpoint" in node.name and
                (node.name.startswith("write_") or node.name.startswith("restore_"))
            ):
                rows.append({"module": module, "function": node.name, "line": node.lineno})
    return rows



def installed_locality_references(repo_root: Path) -> dict:
    """AST census of literal --locality argv pairs in tests and evidence scripts.

    This records source references, NOT whether an installed journey executed.
    Computed locality arguments are recorded separately rather than guessed.
    """
    references = {key: set() for key in BINDING_CLASSES}
    dynamic = set()
    for folder in ("tests", "scripts"):
        for path in sorted((repo_root / folder).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            source = path.read_text(encoding="utf-8")
            if "--locality" not in source:
                continue
            tree = ast.parse(source, filename=str(path))
            relative = path.relative_to(repo_root).as_posix()
            for node in ast.walk(tree):
                if not isinstance(node, (ast.List, ast.Tuple)):
                    continue
                for pos, part in enumerate(node.elts):
                    if not isinstance(part, ast.Constant) or part.value != "--locality":
                        continue
                    if pos + 1 < len(node.elts) and isinstance(node.elts[pos + 1], ast.Constant):
                        target = node.elts[pos + 1].value
                        if isinstance(target, str) and target in references:
                            references[target].add(relative)
                        else:
                            dynamic.add(relative)
                    else:
                        dynamic.add(relative)
    return {
        "literal_by_binding": {key: sorted(value) for key, value in sorted(references.items())},
        "no_literal_argv_evidence": sorted(key for key, value in references.items() if not value),
        "computed_or_unrecognized_argv_sources": sorted(dynamic),
        "qualification": (
            "AST-discovered source references only. A test file mentioning a "
            "locality is not proof of installed-client execution or replay."
        ),
    }

def structure_report(repo_root: Path = ROOT) -> dict:
    repo_root = Path(repo_root)
    modules = source_modules(repo_root)
    trees = {name: ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
             for name, path in sorted(modules.items())}
    graph = import_report(modules, trees)
    choices = locality_choices(trees[ENTRYPOINT])
    if sorted(choices) != sorted(BINDING_CLASSES) or len(choices) != len(BINDING_CLASSES):
        raise ValueError("terminal locality list has drifted; reconcile explicit bindings")
    bindings = []
    for name in choices:
        qualified = BINDING_CLASSES[name]
        module, _, cls = qualified.rpartition(".")
        bindings.append({
            "locality": name,
            "application": qualified,
            "contract": class_contract(trees[module], cls),
            "roundtrip": "not_run_static_report",
        })
    return {
        "schema": SCHEMA,
        "graph": graph,
        "inventories": inventory_report(repo_root, graph),
        "locality_bindings": bindings,
        "checkpoint_writer_restore_entrypoints": checkpoint_procedures(trees),
        "installed_locality_journey_source_references": installed_locality_references(repo_root),
        "evidence_boundary": "static analysis only; no replay/digest success inferred",
    }


def verify_binding_roundtrip(binding: str, folder: Path) -> dict:
    """Real deterministic save/restore for an installed terminal application.

    This is OPT-IN and imports runtime code. Any failure is propagated. It uses
    backend digest and checkpoint APIs unchanged and never proposes world state.
    """
    if binding not in BINDING_CLASSES:
        raise ValueError("unknown terminal binding")
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "campaign.json"
    qualified = BINDING_CLASSES[binding]
    module, _, cls_name = qualified.rpartition(".")
    cls = getattr(importlib.import_module(module), cls_name)
    if binding == "generated-worksite":
        from astra_runtime.myravant_generated_locality import (
            LocalityRecipe, build_generated_locality, create_generated_locality_fixture,
        )
        recipe = LocalityRecipe("access", 0)
        app, _receipts = build_generated_locality(recipe, checkpoint_path=path)
        fixture = create_generated_locality_fixture(recipe)
    else:
        if binding == "tarrow":
            from astra_runtime.myravant_tarrow import create_tarrow_fixture
            fixture = create_tarrow_fixture()
        elif binding == "tarrow-depth":
            from astra_runtime.myravant_tarrow_environment import create_environment_fixture
            fixture = create_environment_fixture()
        elif binding == "development":
            from astra_runtime.myravant_play_fixture import create_terminal_play_fixture
            fixture = create_terminal_play_fixture()
        else:
            fixture = cls.default_fixture()
        app = cls.new(fixture=fixture, checkpoint_path=path)
        saved = app.save()
        if getattr(saved, "failure_class", None):
            raise AssertionError("save failed: " + str(saved.failure_class))
    before = app.authoritative_digest()
    if not path.is_file():
        raise AssertionError("binding did not create a checkpoint: " + binding)
    raw = json.loads(path.read_text(encoding="utf-8"))
    restored = cls.restore(fixture=fixture, checkpoint_path=path)
    after = restored.authoritative_digest()
    if before != after:
        raise AssertionError("restored authoritative digest differs for " + binding)
    if hasattr(app, "journal") and getattr(restored, "journal", None) != app.journal:
        raise AssertionError("restored journal differs for " + binding)
    return {
        "locality": binding,
        "application": qualified,
        "format_identity": raw.get("format_identity"),
        "format_version": raw.get("format_version"),
        "before_digest": before,
        "restored_digest": after,
        "checkpoint_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "equal": True,
        "fixture_initial_digest": fixture.provenance.initial_state_digest,
        "replay_methods": list(getattr(cls, "replay_methods", ())),
        "method": "actual backend save and restore, same explicit fixture",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional deterministic JSON output")
    parser.add_argument("--verify-roundtrips", action="store_true",
                        help="Exercise actual save/restore for each public locality")
    args = parser.parse_args(argv)
    report = structure_report()
    if args.verify_roundtrips:
        with tempfile.TemporaryDirectory(prefix="myravant-structure-") as temporary:
            report["roundtrip_verification"] = [
                verify_binding_roundtrip(name, Path(temporary) / name)
                for name in sorted(BINDING_CLASSES)
            ]
    content = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
