from pathlib import Path
import re

import pytest

yaml = pytest.importorskip(
    "yaml",
    reason=(
        "PyYAML is required for doctrine/registry validation; "
        "install test dependencies with "
        "python3 -m pip install -r requirements-dev.txt"
    ),
)


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
ROADMAP_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_roadmap_v0_1.md"

REQUIRED_TOP_LEVEL_FIELDS = {
    "registry_version",
    "status",
    "maintained_by",
    "purpose",
    "global_status_values",
    "global_layer_values",
    "global_unlock_values",
    "global_test_status_values",
    "global_review_requirements",
    "dependency_rules",
}

REQUIRED_FILE_FIELDS = {
    "file_id",
    "filename",
    "proposed_path",
    "layer",
    "phase",
    "status",
    "authority_level",
    "owner",
    "purpose",
    "owns",
    "must_not_own",
    "dependencies",
    "blocked_by",
    "unlocks",
    "downstream_consumers",
    "donor_pressure_absorbed",
    "hard_refusals",
    "escalation_triggers",
    "required_tests",
    "test_status",
    "review_status",
    "promotion_requirements",
    "scale_gate_relevance",
    "broad_conversion_relevance",
    "canon_relevance",
    "runtime_relevance",
    "live_play_relevance",
    "notes",
}

CONTROL_FILE_IDS = {"ROADMAP-001", "REGISTRY-001"}

EXPECTED_FILE_IDS = (
    ["ROADMAP-001", "REGISTRY-001", "A00", "PREA01-001"]
    + [f"A{i:02d}" for i in range(1, 16)]
    + ["C00"]
    + [f"C{i:02d}" for i in range(1, 15)]
    + [f"K{i:02d}" for i in range(1, 7)]
    + [f"R{i:02d}" for i in range(1, 9)]
    + [f"T{i:02d}" for i in range(1, 8)]
)

FILE_ID_PATTERN = re.compile(r"^(ROADMAP-001|REGISTRY-001|PREA01-\d+|A\d{2}|C\d{2}|K\d{2}|R\d{2}|T\d{2})$")


def load_registry():
    assert REGISTRY_PATH.exists(), f"Missing registry file: {REGISTRY_PATH}"
    with REGISTRY_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    assert isinstance(data, dict), "Registry YAML must parse as a mapping/object."
    return data


def registry_records(data):
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list), "Registry must contain a list under 'file_records' or 'files'."
    assert records, "Registry file record list must not be empty."
    return records


def as_allowed_values(value):
    if isinstance(value, dict):
        return set(value.keys())
    if isinstance(value, list):
        return set(value)
    return set()


def test_roadmap_and_registry_files_exist():
    assert ROADMAP_PATH.exists(), f"Missing roadmap file: {ROADMAP_PATH}"
    assert REGISTRY_PATH.exists(), f"Missing registry file: {REGISTRY_PATH}"


def test_registry_top_level_shape():
    data = load_registry()

    missing = REQUIRED_TOP_LEVEL_FIELDS - set(data.keys())
    assert not missing, f"Registry missing top-level fields: {sorted(missing)}"

    assert "authority" in data or "authority_level" in data, (
        "Registry must include either top-level 'authority' or 'authority_level'."
    )

    registry_records(data)


def test_every_file_record_has_required_fields():
    data = load_registry()

    for record in registry_records(data):
        assert isinstance(record, dict), f"File record must be a mapping: {record!r}"
        file_id = record.get("file_id", "<missing file_id>")

        missing = REQUIRED_FILE_FIELDS - set(record.keys())
        assert not missing, f"{file_id} missing required fields: {sorted(missing)}"


def test_file_ids_and_filenames_are_unique():
    data = load_registry()
    records = registry_records(data)

    file_ids = [record["file_id"] for record in records]
    filenames = [record["filename"] for record in records]

    assert len(file_ids) == len(set(file_ids)), "Duplicate file_id values found."
    assert len(filenames) == len(set(filenames)), "Duplicate filename values found."


def test_required_file_ids_exist():
    data = load_registry()
    found = {record["file_id"] for record in registry_records(data)}

    missing = set(EXPECTED_FILE_IDS) - found
    assert not missing, f"Registry missing expected file IDs: {sorted(missing)}"


def test_status_and_layer_values_are_valid():
    data = load_registry()

    allowed_statuses = as_allowed_values(data["global_status_values"])
    allowed_statuses.update({"roadmap-current", "registry-current"})

    allowed_layers = as_allowed_values(data["global_layer_values"])

    assert allowed_statuses, "global_status_values must define at least one allowed status."
    assert allowed_layers, "global_layer_values must define at least one allowed layer."

    for record in registry_records(data):
        file_id = record["file_id"]
        assert record["status"] in allowed_statuses, (
            f"{file_id} has invalid status {record['status']!r}. "
            f"Allowed: {sorted(allowed_statuses)}"
        )
        assert record["layer"] in allowed_layers, (
            f"{file_id} has invalid layer {record['layer']!r}. "
            f"Allowed: {sorted(allowed_layers)}"
        )


def test_no_unexpected_current_doctrine_records():
    data = load_registry()

    for record in registry_records(data):
        file_id = record["file_id"]
        status = record["status"]

        if file_id in CONTROL_FILE_IDS:
            continue

        assert status not in {"current", "roadmap-current", "registry-current"}, (
            f"{file_id} is marked current before drafting/review pressure tests. "
            "Only ROADMAP-001 and REGISTRY-001 may be current at bootstrap."
        )


def test_owns_and_must_not_own_are_populated():
    data = load_registry()

    for record in registry_records(data):
        file_id = record["file_id"]

        assert isinstance(record["owns"], list), f"{file_id}.owns must be a list."
        assert isinstance(record["must_not_own"], list), f"{file_id}.must_not_own must be a list."

        assert record["owns"], f"{file_id}.owns must not be empty."
        assert record["must_not_own"], f"{file_id}.must_not_own must not be empty."


def test_file_id_dependencies_resolve_when_they_reference_file_ids():
    data = load_registry()
    found = {record["file_id"] for record in registry_records(data)}

    unresolved = []

    for record in registry_records(data):
        file_id = record["file_id"]
        dependencies = record.get("dependencies", [])

        assert isinstance(dependencies, list), f"{file_id}.dependencies must be a list."

        for dep in dependencies:
            if not isinstance(dep, str):
                unresolved.append((file_id, dep, "dependency is not a string"))
                continue

            dep = dep.strip()
            if FILE_ID_PATTERN.match(dep) and dep not in found:
                unresolved.append((file_id, dep, "missing file_id dependency"))

    assert not unresolved, f"Unresolved file_id dependencies: {unresolved}"


def test_registry_contains_control_records():
    data = load_registry()
    records = {record["file_id"]: record for record in registry_records(data)}

    assert "ROADMAP-001" in records
    assert "REGISTRY-001" in records

    assert records["ROADMAP-001"]["layer"] == "0_control"
    assert records["REGISTRY-001"]["layer"] == "0_control"


def test_registry_expected_record_count():
    data = load_registry()
    records = registry_records(data)
    record_ids = [record["file_id"] for record in records]
    unique_record_ids = set(record_ids)
    assert len(records) == len(unique_record_ids), "Registry contains duplicate file_id entries."
    expected_ids = set(EXPECTED_FILE_IDS)
    missing_ids = expected_ids - unique_record_ids
    assert not missing_ids, f"Registry missing expected file_id values: {sorted(missing_ids)}"
    assert len(records) >= len(expected_ids), (
        f"Registry must include all expected records. Found {len(records)} total records "
        f"with {len(expected_ids)} expected ids."
    )


def test_a01_and_k01_filenames_remain_stable():
    data = load_registry()
    records = {record["file_id"]: record for record in registry_records(data)}

    assert records["A01"]["filename"] == "A01_cosmology_and_dimensional_architecture.md"
    assert records["K01"]["filename"] == "K01_lexicon_governance_and_reserved_terms.md"


def test_a00_is_non_current_and_unlocks_a01_without_replacing_it():
    data = load_registry()
    records = {record["file_id"]: record for record in registry_records(data)}
    a00 = records["A00"]

    assert a00["status"] not in {"current", "roadmap-current", "registry-current"}
    assert "A01" in a00["unlocks"]
    assert a00["filename"] != records["A01"]["filename"]


def test_prea01_is_non_current_control_tracking_not_runtime_or_canon_authority():
    data = load_registry()
    records = {record["file_id"]: record for record in registry_records(data)}
    prea01 = records["PREA01-001"]

    assert prea01["status"] not in {"current", "roadmap-current", "registry-current"}
    assert prea01["layer"] == "0_control"
    assert prea01["authority_level"] in {"tracking", "planning", "control"}
    assert "runtime" in " ".join(prea01["must_not_own"]).lower()
