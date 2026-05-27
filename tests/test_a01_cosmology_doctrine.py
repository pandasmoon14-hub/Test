from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A01_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A01_cosmology_and_dimensional_architecture.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    return {r["file_id"]: r for r in data["registry_records"]}


def test_a01_file_exists():
    assert A01_PATH.exists()


def test_a01_has_required_14_sections():
    text = _read(A01_PATH)
    required = [
        "## 1. Purpose and status",
        "## 2. What this file owns",
        "## 3. What this file must not own",
        "## 4. Required definitions",
        "## 5. Core doctrine rules",
        "## 6. Conversion mapping rules",
        "## 7. Source-local handling",
        "## 8. Donor pressure absorbed",
        "## 9. Hard refusals / rejected imports",
        "## 10. Escalation triggers",
        "## 11. Dependencies",
        "## 12. Handoff to downstream layers",
        "## 13. Test cases / pressure examples",
        "## 14. Versioning and review protocol",
    ]
    for h in required:
        assert h in text


def test_a01_must_not_own_boundaries_present():
    text = _read(A01_PATH).lower()
    for phrase in [
        "travel mechanics",
        "runtime map state",
        "runtime event state",
        "factions",
        "gods",
        "donor cosmology as astra default law",
    ]:
        assert phrase in text


def test_a01_source_local_and_quarantine_language_present():
    text = _read(A01_PATH).lower()
    assert "source-local" in text
    assert "quarantined" in text or "quarantine" in text
    assert "escalated" in text


def test_a01_mentions_c14_filename_without_drafting_c14():
    text = _read(A01_PATH)
    assert "C14_source_local_setting_cosmology_record_schema.md" in text
    assert "A01 does not draft C14" in text


def test_registry_a01_and_k01_separation_and_paths():
    records = _registry_records()
    a01 = records["A01"]
    k01 = records["K01"]

    assert a01["status"] == "draft"
    assert a01["status"] != "current"
    assert a01["proposed_path"] == "docs/doctrine/setting/A01_cosmology_and_dimensional_architecture.md"
    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a01["filename"] != k01["filename"]
