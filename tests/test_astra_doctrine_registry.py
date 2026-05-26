from pathlib import Path
import re


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
    "file_id", "filename", "proposed_path", "layer", "phase", "status", "authority_level",
    "owner", "purpose", "owns", "must_not_own", "dependencies", "blocked_by", "unlocks",
    "downstream_consumers", "donor_pressure_absorbed", "hard_refusals", "escalation_triggers",
    "required_tests", "test_status", "review_status", "promotion_requirements", "scale_gate_relevance",
    "broad_conversion_relevance", "canon_relevance", "runtime_relevance", "live_play_relevance", "notes",
}

CONTROL_FILE_IDS = {"ROADMAP-001", "REGISTRY-001"}
EXPECTED_FILE_IDS = (
    ["ROADMAP-001", "REGISTRY-001", "A00", "PREA01-001"]
    + [f"A{i:02d}" for i in range(1, 16)]
    + ["C00"] + [f"C{i:02d}" for i in range(1, 15)]
    + [f"K{i:02d}" for i in range(1, 7)]
    + [f"R{i:02d}" for i in range(1, 9)]
    + [f"T{i:02d}" for i in range(1, 8)]
)
FILE_ID_PATTERN = re.compile(r"^(ROADMAP-001|REGISTRY-001|PREA01-\d+|A\d{2}|C\d{2}|K\d{2}|R\d{2}|T\d{2})$")


def load_registry_text() -> str:
    assert REGISTRY_PATH.exists(), f"Missing registry file: {REGISTRY_PATH}"
    return REGISTRY_PATH.read_text(encoding="utf-8")


def parse_records(text: str):
    records, current = [], None
    in_file_records = False
    current_list_key = None
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if line.startswith("file_records:"):
            in_file_records = True
            continue
        if not in_file_records:
            continue
        if line.startswith("- file_id:"):
            if current:
                records.append(current)
            current = {"file_id": line.split(":", 1)[1].strip()}
            current_list_key = None
            continue
        if current is None:
            continue
        m = re.match(r"^  ([a-zA-Z0-9_]+):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2)
            if v == "":
                current[k] = []
                current_list_key = k
            elif v.startswith("&") or v.startswith("*"):
                current[k] = []
                current_list_key = k
            else:
                current[k] = v.strip("'")
                current_list_key = None
            continue
        m = re.match(r"^  -\s+(.*)$", line)
        if m and current_list_key:
            current[current_list_key].append(m.group(1).strip().strip("'"))
    if current:
        records.append(current)
    return records


def top_level_keys(text: str):
    keys = set()
    for line in text.splitlines():
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*", line):
            keys.add(line.split(":", 1)[0])
    return keys


def test_roadmap_and_registry_files_exist():
    assert ROADMAP_PATH.exists()
    assert REGISTRY_PATH.exists()


def test_registry_top_level_shape():
    text = load_registry_text()
    keys = top_level_keys(text)
    missing = REQUIRED_TOP_LEVEL_FIELDS - keys
    assert not missing
    assert "authority" in keys or "authority_level" in keys


def test_every_file_record_has_required_fields():
    records = parse_records(load_registry_text())
    assert records
    for record in records:
        missing = REQUIRED_FILE_FIELDS - set(record.keys())
        assert not missing, f"{record.get('file_id')} missing {sorted(missing)}"


def test_file_ids_and_filenames_are_unique():
    records = parse_records(load_registry_text())
    file_ids = [r["file_id"] for r in records]
    filenames = [r["filename"] for r in records]
    assert len(file_ids) == len(set(file_ids))
    assert len(filenames) == len(set(filenames))


def test_required_file_ids_exist():
    found = {r["file_id"] for r in parse_records(load_registry_text())}
    assert not (set(EXPECTED_FILE_IDS) - found)


def test_no_unexpected_current_doctrine_records():
    for record in parse_records(load_registry_text()):
        if record["file_id"] in CONTROL_FILE_IDS:
            continue
        assert record["status"] not in {"current", "roadmap-current", "registry-current"}


def test_file_id_dependencies_resolve_when_they_reference_file_ids():
    records = parse_records(load_registry_text())
    found = {r["file_id"] for r in records}
    unresolved = []
    for record in records:
        for dep in record.get("dependencies", []):
            if FILE_ID_PATTERN.match(dep) and dep not in found:
                unresolved.append((record["file_id"], dep))
    assert not unresolved


def test_registry_expected_record_count():
    assert len(parse_records(load_registry_text())) == 55


def test_a01_and_k01_filenames_remain_stable():
    records = {r["file_id"]: r for r in parse_records(load_registry_text())}
    assert records["A01"]["filename"] == "A01_cosmology_and_dimensional_architecture.md"
    assert records["K01"]["filename"] == "K01_lexicon_governance_and_reserved_terms.md"


def test_a00_is_non_current_and_unlocks_a01_without_replacing_it():
    records = {r["file_id"]: r for r in parse_records(load_registry_text())}
    a00 = records["A00"]
    assert a00["status"] not in {"current", "roadmap-current", "registry-current"}
    assert "A01" in a00["unlocks"]
    assert a00["filename"] != records["A01"]["filename"]


def test_prea01_is_non_current_control_tracking_not_runtime_or_canon_authority():
    records = {r["file_id"]: r for r in parse_records(load_registry_text())}
    prea01 = records["PREA01-001"]
    assert prea01["status"] not in {"current", "roadmap-current", "registry-current"}
    assert prea01["layer"] == "0_control"
    assert prea01["authority_level"] in {"tracking", "planning", "control"}
    assert "runtime" in " ".join(prea01["must_not_own"]).lower()
