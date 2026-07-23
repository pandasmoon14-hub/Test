#!/usr/bin/env python3
"""Migrate duplicated runtime-domain guardrails to the shared test manifest.

Run from the repository root on branch:
    maintenance/restore-green-runtime-baseline-v2

The script:
- updates exactly the 30 direct stale package-surface guardrails recorded in
  the merged baseline inventory;
- replaces only the embedded runtime-domain set literal, preserving every
  other historical assertion in each test;
- changes the state-store test to import its visibility contract from its
  owning module;
- performs syntax validation after writing.

It does not modify production runtime code, extraction/conversion code, AFQR
artifacts, canon, or RT-002G.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


EXPECTED_BRANCH = "maintenance/restore-green-runtime-baseline-v2"

TARGETS: dict[str, str] = {
    "tests/runtime/test_command_envelope_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_context_projection_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_domain_event_commitment_skeleton.py":
        "test_domain_package_contains_only_authorized_files",
    "tests/runtime/test_domain_state_store_skeleton.py":
        "test_domain_package_contains_only_authorized_files",
    "tests/runtime/test_domain_transaction_lifecycle_skeleton.py":
        "test_domain_package_contains_only_authorized_files",
    "tests/runtime/test_domain_validation_integration_skeleton.py":
        "test_domain_package_contains_only_authorized_files",
    "tests/runtime/test_event_ledger_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_hidden_information_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_persistence_boundary_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_replay_audit_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_rng_interface_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_runtime_trace_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_state_delta_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_table_oracle_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/runtime/test_validation_pipeline_skeleton.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/test_runtime_domain_pr_0_domain_service_implementation_sequencing_plan.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/test_runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.py":
        "test_domain_package_contains_only_authorized_modules",
    "tests/test_runtime_domain_pr_1b_command_lifecycle_action_legality_skeleton_review.py":
        "test_domain_package_authorized_files_only",
    "tests/test_runtime_domain_pr_2_state_store_state_projection_service_plan.py":
        "test_domain_package_authorized_files_only",
    "tests/test_runtime_domain_pr_2b_state_store_state_projection_skeleton_review.py":
        "test_domain_package_contains_only_authorized_files",
    "tests/test_runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.py":
        "test_domain_package_authorized_files_only",
    "tests/test_runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.py":
        "test_domain_package_contains_only_authorized_files",
    "tests/test_runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.py":
        "test_domain_package_authorized_files_only",
    "tests/test_runtime_domain_pr_4b_validation_integration_invariant_enforcement_skeleton_hardening_review.py":
        "test_current_authorized_domain_files_remain_narrow",
    "tests/test_runtime_domain_pr_4d_validation_integration_invariant_enforcement_skeleton_hardening_review.py":
        "test_current_authorized_domain_files_remain_narrow",
    "tests/test_runtime_domain_pr_4f_validation_integration_residual_hardening_review.py":
        "test_authorized_domain_files_remain_exactly_expected",
    "tests/test_runtime_domain_pr_5_resource_consequence_math_service_plan.py":
        "test_authorized_domain_files_remain_exactly_expected",
    "tests/test_runtime_domain_pr_5e_resource_consequence_math_final_planning_hardening_review.py":
        "test_scope_review_and_no_runtime_domain_file_added",
    "tests/test_runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.py":
        "test_scope_review_and_no_runtime_domain_implementation_file_added",
    "tests/test_runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.py":
        "test_domain_package_contains_only_authorized_modules",
}

IMPORT_BLOCK = (
    "from tests.runtime_domain_package_manifest import (\n"
    "    AUTHORIZED_RUNTIME_DOMAIN_ENTRIES,\n"
    "    AUTHORIZED_RUNTIME_DOMAIN_FILES,\n"
    ")\n"
)

DOMAIN_SET_MARKERS = {"__init__.py", "state_store.py"}


class MigrationError(RuntimeError):
    pass


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def source_offsets(text: str) -> list[int]:
    offsets = [0]
    for line in text.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    return offsets


def absolute_span(text: str, node: ast.AST) -> tuple[int, int]:
    if not all(
        hasattr(node, attr)
        for attr in ("lineno", "col_offset", "end_lineno", "end_col_offset")
    ):
        raise MigrationError(f"AST node lacks source span: {node!r}")
    offsets = source_offsets(text)
    start = offsets[node.lineno - 1] + node.col_offset
    end = offsets[node.end_lineno - 1] + node.end_col_offset
    return start, end


def string_values(node: ast.Set) -> set[str]:
    values: set[str] = set()
    for element in node.elts:
        if isinstance(element, ast.Constant) and isinstance(element.value, str):
            values.add(element.value)
    return values


def find_target_function(tree: ast.Module, function_name: str) -> ast.FunctionDef:
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    ]
    if len(matches) != 1:
        raise MigrationError(
            f"Expected exactly one function named {function_name!r}; "
            f"found {len(matches)}"
        )
    function = matches[0]
    if not isinstance(function, ast.FunctionDef):
        raise MigrationError(f"Unexpected async target function: {function_name}")
    return function


def add_manifest_import(text: str) -> str:
    if "from tests.runtime_domain_package_manifest import (" in text:
        return text

    tree = ast.parse(text)
    insert_after_line = 0

    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        insert_after_line = tree.body[0].end_lineno or 0

    for statement in tree.body:
        if (
            isinstance(statement, ast.ImportFrom)
            and statement.module == "__future__"
        ):
            insert_after_line = statement.end_lineno or insert_after_line

    lines = text.splitlines(keepends=True)
    insertion_index = insert_after_line
    block = "\n" + IMPORT_BLOCK
    lines[insertion_index:insertion_index] = [block]
    return "".join(lines)


def migrate_guardrail(path: Path, function_name: str) -> None:
    original = path.read_text(encoding="utf-8")
    tree = ast.parse(original, filename=str(path))
    function = find_target_function(tree, function_name)

    matching_sets: list[tuple[ast.Set, set[str]]] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Set):
            values = string_values(node)
            if DOMAIN_SET_MARKERS <= values:
                matching_sets.append((node, values))

    if len(matching_sets) != 1:
        raise MigrationError(
            f"{path}: expected one runtime-domain set in {function_name}; "
            f"found {len(matching_sets)}"
        )

    node, values = matching_sets[0]
    replacement = (
        "set(AUTHORIZED_RUNTIME_DOMAIN_ENTRIES)"
        if "__pycache__" in values
        else "set(AUTHORIZED_RUNTIME_DOMAIN_FILES)"
    )

    start, end = absolute_span(original, node)
    migrated = original[:start] + replacement + original[end:]
    migrated = add_manifest_import(migrated)

    if migrated == original:
        raise MigrationError(f"{path}: migration made no change")

    ast.parse(migrated, filename=str(path))
    path.write_text(migrated, encoding="utf-8", newline="\n")


def fix_state_store_import(repo_root: Path) -> None:
    path = repo_root / "tests/runtime/test_domain_state_store_skeleton.py"
    text = path.read_text(encoding="utf-8")
    old = "from astra_runtime.domain import (\n"
    new = "from astra_runtime.domain.state_store import (\n"

    count = text.count(old)
    if count != 1:
        raise MigrationError(
            f"{path}: expected one ambiguous package import; found {count}"
        )

    migrated = text.replace(old, new, 1)
    ast.parse(migrated, filename=str(path))
    path.write_text(migrated, encoding="utf-8", newline="\n")


def verify_required_branch(repo_root: Path) -> None:
    branch = run_git("branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise MigrationError(
            f"Run on branch {EXPECTED_BRANCH!r}; current branch is {branch!r}"
        )

    if not (repo_root / "tests/runtime_domain_package_manifest.py").is_file():
        raise MigrationError(
            "Shared manifest is missing. Fetch the replacement branch first."
        )


def main() -> int:
    repo_root = Path.cwd().resolve()
    if not (repo_root / ".git").exists():
        raise MigrationError("Run from the Astra repository root")

    verify_required_branch(repo_root)

    before = run_git("status", "--short")
    allowed_untracked_prefixes = (
        "?? .venv-baseline/",
        "?? artifacts/",
        "?? migrate_runtime_domain_guardrails.py",
    )
    unexpected_status = [
        line
        for line in before.splitlines()
        if line and not line.startswith(allowed_untracked_prefixes)
    ]
    if unexpected_status:
        raise MigrationError(
            "Tracked or unrelated working-tree changes must be cleared before "
            "migration:\n" + "\n".join(unexpected_status)
        )

    changed: list[str] = []
    for relative_path, function_name in TARGETS.items():
        path = repo_root / relative_path
        if not path.is_file():
            raise MigrationError(f"Missing target file: {relative_path}")
        migrate_guardrail(path, function_name)
        changed.append(relative_path)

    fix_state_store_import(repo_root)

    for relative_path in TARGETS:
        ast.parse(
            (repo_root / relative_path).read_text(encoding="utf-8"),
            filename=relative_path,
        )

    if len(changed) != 30:
        raise MigrationError(
            f"Expected 30 guardrail migrations; completed {len(changed)}"
        )

    print("Migrated 30 duplicated package-surface guardrails.")
    print("Bound state-store tests to astra_runtime.domain.state_store.")
    print()
    print("Changed files:")
    print(run_git("status", "--short"))
    print()
    print("Next commands:")
    print("  python -m pytest -q tests/test_runtime_domain_package_manifest.py")
    print("  python -m pytest -q tests/runtime")
    print("  python -m pytest -q")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (MigrationError, subprocess.CalledProcessError, SyntaxError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
