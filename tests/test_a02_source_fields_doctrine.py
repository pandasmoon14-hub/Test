from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A02_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A02_source_fields_magic_technology_relation.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a02_file_exists():
    assert A02_PATH.exists()


def test_a02_has_required_14_sections():
    text = _read(A02_PATH)
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


def test_a02_boundary_phrases_present():
    text = _read(A02_PATH).lower()
    for phrase in [
        "do not rename",
        "k01 remains separate",
        "not current",
        "runtime state",
        "specific spells",
        "specific devices",
    ]:
        assert phrase in text


def test_a02_mentions_required_pressure_tests():
    text = _read(A02_PATH)
    assert "Magic-opposes-technology model" in text
    assert "Magic-is-technology model" in text
    assert "Technology-is-mundane model" in text
    assert "Cultivation-force-as-source-field model" in text
    assert "Psionic-divine-computational interface model" in text


def test_registry_a02_and_k01_separation_and_paths():
    records = _registry_records()
    a02 = records["A02"]
    k01 = records["K01"]

    assert a02["status"] == "todo"
    assert a02["status"] != "current"
    assert a02["proposed_path"] == "docs/doctrine/setting/A02_source_fields_magic_technology_relation.md"
    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a02["filename"] != k01["filename"]
