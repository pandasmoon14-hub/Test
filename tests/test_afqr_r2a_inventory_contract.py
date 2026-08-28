"""Successor-safe R2A inventory validation for tranche-B bounded sharding.

The accepted tranche-A test module is immutable at PREDECESSOR_HEAD. This
wrapper executes every predecessor test except the obsolete R2A-7 capacity
definitions, then supplies successor capacity tests for the expanded bounded
shard family. It does not replace or weaken the controlled matcher, semantic
surface, R2A-4/5/6, or historical validation logic.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import subprocess
from pathlib import Path

PREDECESSOR_HEAD = "d7f2f69c53f2f683d3555e5eb0c7461e9ba8135b"
PREDECESSOR_PATH = "tests/test_afqr_r2a_inventory_contract.py"
ORIGINAL_CAPACITY_BASE = "20bbf489c3fcd0abe4a45b117fbefda86fcfc97d"
ORIGINAL_CAPACITY_HEAD = "62e1565ed598345901e92dc04f3b686281418d83"
SUCCESSOR_MANIFEST_VERSION = "0.2.9"
SUCCESSOR_SHARD_COUNT = 48
SUCCESSOR_MAX_CHANGED_FILES = 51
SUCCESSOR_MAX_ADDITIONS = 16000
TRANCHE_B_MAX_CHANGED_FILES = 44
TRANCHE_B_MAX_ADDITIONS = 8000

# Defined before predecessor execution so its historical compatibility aliases
# continue to resolve to a current-posture test after obsolete definitions are removed.
def test_r2a7_capacity_preserves_structural_authority():
    base = _predecessor_manifest()
    current_document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    assert [row["partition_id"] for row in current_document["partitions"]] == [row["partition_id"] for row in base["partitions"]]
    assert {row["partition_id"]: row["dependency_partitions"] for row in current_document["partitions"]} == {
        row["partition_id"]: row["dependency_partitions"] for row in base["partitions"]
    }
    for field in (
        "disposition_precedence",
        "disposition_rules",
        "generated_vendor_exclusion_patterns",
        "coordination_domain_ownership",
        "coordination_must_not_own",
        "sharding",
    ):
        assert current_document["ownership_rules"][field] == base["ownership_rules"][field]
    for before, after in zip(base["partitions"], current_document["partitions"]):
        if after["partition_id"] != "R2A-7":
            assert after == before
    expected = {f"R2A-{number}": ("complete" if number <= 6 else "planned_not_present") for number in range(1, 13)}
    contract, clusters, file_manifest = map(
        lambda path: json.loads(path.read_text(encoding="utf-8")),
        (CONTRACT, CLUSTERS, FILES),
    )
    assert contract["r2a_partition_statuses"] == clusters["r2a_partition_statuses"] == expected
    assert {row["partition_id"]: row["status"] for row in current_document["partitions"]} == expected
    assert {row["partition_id"]: row["current_status"] for row in file_manifest["r2a_reconstruction_sequence"]} == expected
    assert contract["project_posture"]["R2A"] == "active_incomplete"
    assert contract["project_posture"]["R2B"] == "blocked"

def test_r2a7_capacity_exact_manifest_and_posture():
    document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    row = r2a7_capacity_row(document)
    assert r2a7_capacity_valid(document)
    assert (document["artifact_id"], document["artifact_version"], document["partition_count"]) == (
        "AFQR-R2A-PARTITION-MANIFEST-001",
        SUCCESSOR_MANIFEST_VERSION,
        12,
    )
    assert (row["status"], row["dependency_partitions"], row["candidate_path_patterns"]) == (
        "planned_not_present",
        ["R2A-6"],
        ["**"],
    )
    assert (row["maximum_changed_files"], row["maximum_additions"]) == (
        SUCCESSOR_MAX_CHANGED_FILES,
        SUCCESSOR_MAX_ADDITIONS,
    )
    assert set(row["planned_artifact_paths"]) == R2A7_PLANNED_PATHS
    assert len(row["planned_artifact_paths"]) == SUCCESSOR_SHARD_COUNT + 1
    existing = r2a7_existing_planned_paths()
    assert R2A7_TRANCHE_A_SHARDS <= existing <= R2A7_PLANNED_PATHS
    assert not r2a7_unplanned_materialized_paths()

def test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes():
    subprocess.check_call(["git", "merge-base", "--is-ancestor", PREDECESSOR_HEAD, "HEAD"], cwd=ROOT)

    # Tranche A is immutable and remains within the accepted predecessor scope.
    for path in sorted(R2A7_TRANCHE_A_SHARDS):
        assert git_blob(PREDECESSOR_HEAD, path) == Path(ROOT / path).read_bytes()

    changed = set(subprocess.check_output(
        ["git", "diff", "--name-only", f"{PREDECESSOR_HEAD}...HEAD"],
        cwd=ROOT, text=True,
    ).splitlines())
    assert changed <= R2A7_TRANCHE_B_ALLOWED_PATHS
    assert len(changed) <= TRANCHE_B_MAX_CHANGED_FILES
    assert not any(path.startswith(("src/", "schemas/", "tests/runtime/")) for path in changed)
    status = subprocess.check_output(
        ["git", "diff", "--name-status", f"{PREDECESSOR_HEAD}...HEAD"],
        cwd=ROOT, text=True,
    ).splitlines()
    assert all(not line.startswith("D\t") for line in status)
    numstat = subprocess.check_output(
        ["git", "diff", "--numstat", f"{PREDECESSOR_HEAD}...HEAD"],
        cwd=ROOT, text=True,
    ).splitlines()
    assert "-\t-" not in "\n".join(numstat)
    assert sum(int(row.split("\t")[0]) for row in numstat) <= TRANCHE_B_MAX_ADDITIONS

    # Global R2A-7 scope remains under the original 16k additions guard.
    global_changed = set(subprocess.check_output(
        ["git", "diff", "--name-only", f"{ORIGINAL_CAPACITY_BASE}...HEAD"],
        cwd=ROOT, text=True,
    ).splitlines())
    assert global_changed <= (R2A7_CAPACITY_PATHS | R2A7_PLANNED_PATHS)
    assert len(global_changed) <= SUCCESSOR_MAX_CHANGED_FILES
    global_numstat = subprocess.check_output(
        ["git", "diff", "--numstat", f"{ORIGINAL_CAPACITY_BASE}...HEAD"],
        cwd=ROOT, text=True,
    ).splitlines()
    assert "-\t-" not in "\n".join(global_numstat)
    assert sum(int(row.split("\t")[0]) for row in global_numstat) <= SUCCESSOR_MAX_ADDITIONS
    assert not r2a7_unplanned_materialized_paths()

def test_r2a7_capacity_mutation_resistance():
    document = json.loads(PARTITIONS.read_text(encoding="utf-8"))
    mutations = []
    for field, value in (
        ("maximum_changed_files", SUCCESSOR_MAX_CHANGED_FILES - 1),
        ("maximum_changed_files", SUCCESSOR_MAX_CHANGED_FILES + 1),
        ("maximum_additions", SUCCESSOR_MAX_ADDITIONS - 1),
        ("maximum_additions", SUCCESSOR_MAX_ADDITIONS + 1),
        ("status", "active_incomplete"),
        ("status", "complete"),
    ):
        bad = copy.deepcopy(document)
        r2a7_capacity_row(bad)[field] = value
        mutations.append(bad)
    for operation in ("remove_shard", "add_shard", "replace_shard", "remove_index"):
        bad = copy.deepcopy(document)
        paths = r2a7_capacity_row(bad)["planned_artifact_paths"]
        if operation == "remove_shard":
            paths.remove("docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_0048.yaml")
        elif operation == "add_shard":
            paths.append("docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_0049.yaml")
        elif operation == "replace_shard":
            paths[8] = "docs/doctrine/reviews/r2a/dispositions_remaining/unplanned.yaml"
        else:
            paths.remove("docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml")
        mutations.append(bad)
    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["dependency_partitions"] = ["R2A-5"]
    mutations.append(bad)
    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["candidate_path_patterns"] = ["docs/**"]
    mutations.append(bad)
    bad = copy.deepcopy(document)
    bad["ownership_rules"]["disposition_precedence"] = ["R2A-5", "R2A-4", "R2A-6", "R2A-7"]
    mutations.append(bad)
    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["gate_effect"] += " Gate advances."
    mutations.append(bad)
    bad = copy.deepcopy(document)
    r2a7_capacity_row(bad)["prohibited_work"].pop()
    mutations.append(bad)
    bad = copy.deepcopy(document)
    bad["partition_count"] = 13
    mutations.append(bad)
    assert all(not r2a7_capacity_valid(bad) for bad in mutations)

_OBSOLETE_R2A7_NAMES = {
    "R2A7_CAPACITY_BASE",
    "R2A7_CAPACITY_PATHS",
    "R2A7_PLANNED_PATHS",
    "R2A7_PRIOR_PROHIBITIONS",
    "R2A7_CAPACITY_HEAD",
    "R2A7_STAGE_REQUIRED_PATHS",
    "r2a7_capacity_base_manifest",
    "r2a7_capacity_valid",
    "r2a7_existing_planned_paths",
    "r2a7_unplanned_materialized_paths",
    "test_r2a7_capacity_exact_manifest_and_posture",
    "test_r2a7_capacity_preserves_structural_authority",
    "test_r2a7_capacity_amendment_scope_no_deletions_or_runtime_changes",
    "test_r2a7_capacity_mutation_resistance",
}

def _defined_names(node: ast.AST) -> set[str]:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, ast.Assign):
        result = set()
        for target in node.targets:
            if isinstance(target, ast.Name):
                result.add(target.id)
        return result
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return {node.target.id}
    return set()

def _predecessor_source() -> str:
    return subprocess.check_output(
        ["git", "show", f"{PREDECESSOR_HEAD}:{PREDECESSOR_PATH}"],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
    )

_source = _predecessor_source()
_tree = ast.parse(_source, filename=PREDECESSOR_PATH)
_filtered = [
    node for node in _tree.body
    if not (_defined_names(node) & _OBSOLETE_R2A7_NAMES)
]
exec(compile(ast.Module(body=_filtered, type_ignores=[]), PREDECESSOR_PATH, "exec"), globals())

# Successor constants deliberately replace only the obsolete capacity layer.
R2A7_CAPACITY_BASE = ORIGINAL_CAPACITY_BASE
R2A7_CAPACITY_PATHS = {
    "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
    "tests/test_afqr_r2a_inventory_contract.py",
}
R2A7_PLANNED_PATHS = {
    "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml",
    *{
        f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
        for number in range(1, SUCCESSOR_SHARD_COUNT + 1)
    },
}
R2A7_PRIOR_PROHIBITIONS = {
    "adopt doctrine",
    "modify runtime or production schemas",
    "perform work assigned to a later partition",
}
R2A7_TRANCHE_A_SHARDS = {
    f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
    for number in range(1, 8)
}
R2A7_TRANCHE_B_ALLOWED_PATHS = (
    R2A7_CAPACITY_PATHS
    | {"docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"}
    | {
        f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
        for number in range(8, SUCCESSOR_SHARD_COUNT + 1)
    }
)

def _predecessor_manifest():
    return json.loads(subprocess.check_output(
        ["git", "show", f"{PREDECESSOR_HEAD}:{PARTITIONS.relative_to(ROOT).as_posix()}"],
        cwd=ROOT,
        text=True,
    ))

def r2a7_capacity_base_manifest():
    return _predecessor_manifest()

def r2a7_capacity_valid(document, base=None):
    base = base or _predecessor_manifest()
    try:
        row = r2a7_capacity_row(document)
        if document["artifact_id"] != "AFQR-R2A-PARTITION-MANIFEST-001":
            return False
        if document["artifact_version"] != SUCCESSOR_MANIFEST_VERSION or document["partition_count"] != 12:
            return False
        if row["status"] != "planned_not_present" or row["dependency_partitions"] != ["R2A-6"]:
            return False
        if row["maximum_changed_files"] != SUCCESSOR_MAX_CHANGED_FILES:
            return False
        if row["maximum_additions"] != SUCCESSOR_MAX_ADDITIONS:
            return False
        if set(row["planned_artifact_paths"]) != R2A7_PLANNED_PATHS or len(row["planned_artifact_paths"]) != SUCCESSOR_SHARD_COUNT + 1:
            return False
        if row["candidate_path_patterns"] != ["**"]:
            return False
        if row["gate_effect"] != "No gate advances and source-local material stays nonauthoritative.":
            return False
        if set(row["prohibited_work"]) != R2A7_PRIOR_PROHIBITIONS:
            return False
        restored = copy.deepcopy(document)
        restored["artifact_version"] = base["artifact_version"]
        restored_row = r2a7_capacity_row(restored)
        base_row = r2a7_capacity_row(base)
        for field in ("maximum_changed_files", "maximum_additions", "planned_artifact_paths"):
            restored_row[field] = copy.deepcopy(base_row[field])
        return restored == base
    except (KeyError, StopIteration, TypeError):
        return False

def r2a7_existing_planned_paths():
    return {path for path in R2A7_PLANNED_PATHS if (ROOT / path).exists()}

def r2a7_unplanned_materialized_paths():
    root = ROOT / "docs/doctrine/reviews/r2a/dispositions_remaining"
    if not root.exists():
        return set()
    return {
        path.relative_to(ROOT).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    } - R2A7_PLANNED_PATHS
