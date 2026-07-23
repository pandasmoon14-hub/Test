#!/usr/bin/env python3
"""Resume the runtime-domain guardrail migration after a partial run.

This helper reads the merged machine-readable baseline inventory, resolves
historical filename drift, accepts already migrated target files, and changes
only the 30 direct stale package-surface guardrails plus the ambiguous
state-store test import.
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

import yaml


EXPECTED_BRANCH = "maintenance/restore-green-runtime-baseline-v2"
INVENTORY = Path(
    "docs/doctrine/reviews/runtime_baseline_failure_inventory_2026_07_20.yaml"
)
MANIFEST_IMPORT = (
    "from tests.runtime_domain_package_manifest import (\n"
    "    AUTHORIZED_RUNTIME_DOMAIN_ENTRIES,\n"
    "    AUTHORIZED_RUNTIME_DOMAIN_FILES,\n"
    ")\n"
)
DOMAIN_MARKERS = {"__init__.py", "state_store.py"}
MANIFEST_TOKENS = (
    "AUTHORIZED_RUNTIME_DOMAIN_FILES",
    "AUTHORIZED_RUNTIME_DOMAIN_ENTRIES",
)


class MigrationError(RuntimeError):
    pass


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def offsets(text: str) -> list[int]:
    result = [0]
    for line in text.splitlines(keepends=True):
        result.append(result[-1] + len(line))
    return result


def span(text: str, node: ast.AST) -> tuple[int, int]:
    table = offsets(text)
    return (
        table[node.lineno - 1] + node.col_offset,
        table[node.end_lineno - 1] + node.end_col_offset,
    )


def function_matches(tree: ast.Module, name: str) -> list[ast.FunctionDef]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]


def add_manifest_import(text: str) -> str:
    if "from tests.runtime_domain_package_manifest import (" in text:
        return text

    tree = ast.parse(text)
    insert_after = 0
    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        insert_after = tree.body[0].end_lineno or 0

    for statement in tree.body:
        if isinstance(statement, ast.ImportFrom) and statement.module == "__future__":
            insert_after = statement.end_lineno or insert_after

    lines = text.splitlines(keepends=True)
    lines[insert_after:insert_after] = ["\n" + MANIFEST_IMPORT]
    return "".join(lines)


def load_inventory_targets(root: Path) -> list[tuple[str, str]]:
    data = yaml.safe_load((root / INVENTORY).read_text(encoding="utf-8"))
    cluster = next(
        item
        for item in data["failure_clusters"]
        if item["cluster_id"] == "RB-FAIL-001"
    )
    nodes = list(cluster["runtime_node_ids"]) + list(
        cluster["full_suite_additional_direct_node_ids"]
    )

    targets: list[tuple[str, str]] = []
    for node_id in nodes:
        parts = node_id.split("::")
        if len(parts) < 2:
            raise MigrationError(f"Malformed node ID: {node_id}")
        targets.append((parts[0], parts[-1]))

    if len(targets) != 30:
        raise MigrationError(f"Expected 30 inventory targets; found {len(targets)}")
    return targets


def historical_prefix(filename: str) -> str | None:
    match = re.match(
        r"^(test_runtime_(?:domain|impl)_(?:pr|rt)_\d+[a-z]?)",
        filename,
    )
    return match.group(1) if match else None


def resolve_path(root: Path, relative: str, function_name: str) -> Path:
    expected = root / relative
    if expected.is_file():
        return expected

    prefix = historical_prefix(expected.name)
    if prefix is None:
        raise MigrationError(f"Missing target file: {relative}")

    candidates: list[Path] = []
    for candidate in sorted(expected.parent.glob(f"{prefix}*.py")):
        try:
            tree = ast.parse(candidate.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        if len(function_matches(tree, function_name)) == 1:
            candidates.append(candidate)

    if len(candidates) != 1:
        names = ", ".join(str(p.relative_to(root)) for p in candidates) or "none"
        raise MigrationError(
            f"Could not uniquely resolve {relative!r} for {function_name!r}; "
            f"candidates: {names}"
        )

    resolved = candidates[0]
    print(f"Resolved filename drift: {relative} -> {resolved.relative_to(root)}")
    return resolved


def set_values(node: ast.Set) -> set[str]:
    return {
        element.value
        for element in node.elts
        if isinstance(element, ast.Constant) and isinstance(element.value, str)
    }


def migrate_guardrail(path: Path, function_name: str) -> bool:
    original = path.read_text(encoding="utf-8")
    tree = ast.parse(original, filename=str(path))
    matches = function_matches(tree, function_name)
    if len(matches) != 1:
        raise MigrationError(
            f"{path}: expected one {function_name!r}; found {len(matches)}"
        )

    function = matches[0]
    function_start, function_end = span(original, function)
    function_source = original[function_start:function_end]
    already_migrated = any(token in function_source for token in MANIFEST_TOKENS)

    embedded: list[tuple[ast.Set, set[str]]] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Set):
            values = set_values(node)
            if DOMAIN_MARKERS <= values:
                embedded.append((node, values))

    if already_migrated:
        if embedded:
            raise MigrationError(
                f"{path}: shared manifest and embedded domain set coexist"
            )
        migrated = add_manifest_import(original)
        if migrated == original:
            return False
        ast.parse(migrated, filename=str(path))
        path.write_text(migrated, encoding="utf-8", newline="\n")
        return True

    if len(embedded) != 1:
        raise MigrationError(
            f"{path}: expected one embedded domain set; found {len(embedded)}"
        )

    node, values = embedded[0]
    replacement = (
        "set(AUTHORIZED_RUNTIME_DOMAIN_ENTRIES)"
        if "__pycache__" in values
        else "set(AUTHORIZED_RUNTIME_DOMAIN_FILES)"
    )
    start, end = span(original, node)
    migrated = original[:start] + replacement + original[end:]
    migrated = add_manifest_import(migrated)
    ast.parse(migrated, filename=str(path))
    path.write_text(migrated, encoding="utf-8", newline="\n")
    return True


def fix_state_store_import(root: Path) -> bool:
    path = root / "tests/runtime/test_domain_state_store_skeleton.py"
    text = path.read_text(encoding="utf-8")
    old = "from astra_runtime.domain import (\n"
    new = "from astra_runtime.domain.state_store import (\n"
    if new in text:
        return False
    if text.count(old) != 1:
        raise MigrationError("State-store package import could not be resolved")
    migrated = text.replace(old, new, 1)
    ast.parse(migrated, filename=str(path))
    path.write_text(migrated, encoding="utf-8", newline="\n")
    return True


def status_path(line: str) -> str:
    payload = line[3:]
    if " -> " in payload:
        payload = payload.split(" -> ", 1)[1]
    return payload.strip().replace("\\", "/")


def verify_scope(root: Path, targets: dict[Path, str]) -> None:
    allowed = {
        str(path.relative_to(root)).replace("\\", "/") for path in targets
    }
    untracked_prefixes = (".venv/", ".venv-baseline/", "artifacts/")
    unexpected: list[str] = []
    for line in git("status", "--short").splitlines():
        if not line:
            continue
        code = line[:2]
        path = status_path(line)
        if code == "??" and path.startswith(untracked_prefixes):
            continue
        if path in allowed:
            continue
        unexpected.append(line)
    if unexpected:
        raise MigrationError(
            "Unrelated working-tree changes detected:\n" + "\n".join(unexpected)
        )


def main() -> int:
    root = Path.cwd().resolve()
    if not (root / ".git").exists():
        raise MigrationError("Run from the repository root")
    branch = git("branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise MigrationError(
            f"Expected branch {EXPECTED_BRANCH!r}; current branch is {branch!r}"
        )

    resolved: dict[Path, str] = {}
    for relative, function_name in load_inventory_targets(root):
        path = resolve_path(root, relative, function_name)
        if path in resolved:
            raise MigrationError(f"Duplicate resolved target: {path}")
        resolved[path] = function_name
    if len(resolved) != 30:
        raise MigrationError(f"Expected 30 unique targets; found {len(resolved)}")

    verify_scope(root, resolved)

    changed = 0
    already = 0
    for path, function_name in resolved.items():
        if migrate_guardrail(path, function_name):
            changed += 1
        else:
            already += 1

    state_store_changed = fix_state_store_import(root)

    for path in resolved:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    print(
        f"Completed 30 guardrails: {changed} changed now, "
        f"{already} already migrated."
    )
    print(
        "State-store import updated."
        if state_store_changed
        else "State-store import was already updated."
    )
    print(git("status", "--short"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (MigrationError, OSError, SyntaxError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
