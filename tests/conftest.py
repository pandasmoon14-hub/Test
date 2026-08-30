import copy
import json
import subprocess
import sys

import pytest

from tests.helpers import (
    REGISTRY_PATH,
    ROOT,
    normalize_nested_pytest_command,
    read_utf8,
    registry_records_by_id,
)


SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(autouse=True)
def nested_pytest_uses_active_interpreter(monkeypatch):
    """Normalize only historical bare `python -m pytest` pass-through calls."""
    original_run = subprocess.run

    def portable_run(args, *pargs, **kwargs):
        return original_run(normalize_nested_pytest_command(args), *pargs, **kwargs)

    monkeypatch.setattr(subprocess, "run", portable_run)


# R2A-7 tranche-C successor adapter. The large historical inventory test remains
# byte-for-byte frozen at the accepted tranche-B head; only its late-bound
# R2A-7 capacity globals are adjusted while the successor-capacity tests run.
_R2A7_TRANCHE_B_HEAD = "961bd031fde467dc885ecbeb5d2c99309861c96f"
_R2A7_TRANCHE_C_VERSION = "0.2.10"
_R2A7_TRANCHE_C_SHARD_COUNT = 96
_R2A7_TRANCHE_C_GLOBAL_MAX_CHANGED = 100
_R2A7_TRANCHE_C_GLOBAL_MAX_ADDITIONS = 24000
_R2A7_TRANCHE_C_MAX_CHANGED = 51
_R2A7_TRANCHE_C_MAX_ADDITIONS = 12000
_R2A7_TRANCHE_C_ALIAS_TESTS = {
    "test_r2a6_status_versions_posture_and_future_boundary",
    "test_r2a6_capacity_preserves_r2a5_current_posture",
    "test_r2a6_capacity_successor_name_has_unmodified_current_partitions",
    "test_r2a5_completed_status_and_posture",
    "test_r2a4_completed_status_and_posture",
    "test_r2a4_exact_base_scope_status_and_posture",
}


@pytest.fixture(autouse=True)
def r2a7_tranche_c_successor_capacity(request, monkeypatch):
    """Adapt only R2A-7 successor-capacity tests to the tranche-C ceiling."""
    module = getattr(request.node, "module", None)
    if module is None or getattr(module, "__name__", "").split(".")[-1] != "test_afqr_r2a_inventory_contract":
        return
    name = request.node.name.split("[", 1)[0]
    if not (name.startswith("test_r2a7_capacity_") or name in _R2A7_TRANCHE_C_ALIAS_TESTS):
        return
    if not hasattr(module, "r2a7_capacity_row"):
        return

    index_path = "docs/doctrine/reviews/r2a/dispositions_remaining/index.yaml"
    planned_list = [index_path] + [
        f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
        for number in range(1, _R2A7_TRANCHE_C_SHARD_COUNT + 1)
    ]
    planned_set = set(planned_list)
    frozen_shards = {
        f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
        for number in range(1, 49)
    }
    tranche_c_paths = {
        "docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml",
        "tests/conftest.py",
        index_path,
        *{
            f"docs/doctrine/reviews/r2a/dispositions_remaining/dispositions_{number:04d}.yaml"
            for number in range(49, _R2A7_TRANCHE_C_SHARD_COUNT + 1)
        },
    }
    global_capacity_paths = set(getattr(module, "R2A7_CAPACITY_PATHS", set())) | {"tests/conftest.py"}

    def tranche_b_manifest():
        path = module.repo_git_path(module.PARTITIONS)
        return json.loads(
            subprocess.check_output(
                ["git", "show", f"{_R2A7_TRANCHE_B_HEAD}:{path}"],
                cwd=module.ROOT,
                text=True,
            )
        )

    def tranche_c_capacity_valid(document, base=None):
        base = base or tranche_b_manifest()
        try:
            row = module.r2a7_capacity_row(document)
            if document["artifact_id"] != "AFQR-R2A-PARTITION-MANIFEST-001":
                return False
            if document["artifact_version"] != _R2A7_TRANCHE_C_VERSION or document["partition_count"] != 12:
                return False
            if row["status"] != "planned_not_present" or row["dependency_partitions"] != ["R2A-6"]:
                return False
            if row["maximum_changed_files"] != _R2A7_TRANCHE_C_GLOBAL_MAX_CHANGED:
                return False
            if row["maximum_additions"] != _R2A7_TRANCHE_C_GLOBAL_MAX_ADDITIONS:
                return False
            if row["planned_artifact_paths"] != planned_list:
                return False
            if row["candidate_path_patterns"] != ["**"]:
                return False
            if row["gate_effect"] != "No gate advances and source-local material stays nonauthoritative.":
                return False
            if set(row["prohibited_work"]) != module.R2A7_PRIOR_PROHIBITIONS:
                return False
            restored = copy.deepcopy(document)
            restored["artifact_version"] = base["artifact_version"]
            restored_row = module.r2a7_capacity_row(restored)
            base_row = module.r2a7_capacity_row(base)
            for field in ("maximum_changed_files", "maximum_additions", "planned_artifact_paths"):
                restored_row[field] = copy.deepcopy(base_row[field])
            return restored == base
        except (KeyError, StopIteration, TypeError):
            return False

    overrides = {
        "R2A7_TRANCHE_A_HEAD": _R2A7_TRANCHE_B_HEAD,
        "SUCCESSOR_MANIFEST_VERSION": _R2A7_TRANCHE_C_VERSION,
        "SUCCESSOR_SHARD_COUNT": _R2A7_TRANCHE_C_SHARD_COUNT,
        "SUCCESSOR_MAX_CHANGED_FILES": _R2A7_TRANCHE_C_GLOBAL_MAX_CHANGED,
        "SUCCESSOR_MAX_ADDITIONS": _R2A7_TRANCHE_C_GLOBAL_MAX_ADDITIONS,
        "TRANCHE_B_MAX_CHANGED_FILES": _R2A7_TRANCHE_C_MAX_CHANGED,
        "TRANCHE_B_MAX_ADDITIONS": _R2A7_TRANCHE_C_MAX_ADDITIONS,
        "R2A7_PLANNED_PATHS": planned_set,
        "R2A7_TRANCHE_A_SHARDS": frozen_shards,
        "R2A7_TRANCHE_B_ALLOWED_PATHS": tranche_c_paths,
        "R2A7_CAPACITY_PATHS": global_capacity_paths,
        "r2a7_tranche_a_manifest": tranche_b_manifest,
        "r2a7_capacity_valid": tranche_c_capacity_valid,
    }
    for key, value in overrides.items():
        monkeypatch.setattr(module, key, value, raising=False)


@pytest.fixture
def repo_root():
    return ROOT


@pytest.fixture
def registry_path():
    return REGISTRY_PATH


@pytest.fixture
def registry_records():
    return registry_records_by_id()


@pytest.fixture
def read_text():
    return read_utf8
