from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A05_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A05_civilization_scale_and_power_scale_doctrine.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a05_file_exists():
    assert A05_PATH.exists()


def test_a05_has_required_14_sections():
    text = _read(A05_PATH)
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


def test_a05_required_scale_taxonomy_terms_present():
    text = _read(A05_PATH).lower()
    for phrase in [
        "personal scale",
        "small-group scale",
        "large-group scale",
        "institutional scale",
        "regional scale",
        "planetary scale",
        "orbital scale",
        "stellar-system scale",
        "interstellar/void scale",
        "planar scale",
        "cosmic scale",
        "scale boundary",
        "scale transition",
        "cross-scale influence",
        "scale collapse risk",
        "scale inflation risk",
        "source-local scale claim",
        "quarantined scale claim",
        "escalated scale contradiction",
    ]:
        assert phrase in text


def test_a05_must_not_own_boundaries_present():
    text = _read(A05_PATH).lower()
    for phrase in [
        "specific empires",
        "specific starships",
        "combat math",
        "mass-combat mechanics",
        "starship rules",
        "travel mechanics",
        "faction economies",
        "resource pools",
        "runtime scale state",
        "runtime map state",
        "hidden-information behavior",
        "lore canon declarations",
    ]:
        assert phrase in text


def test_a05_dependency_mentions_and_non_redefinition_posture_present():
    text = _read(A05_PATH)
    lowered = text.lower()

    assert "A01_cosmology_and_dimensional_architecture.md" in text
    assert "A02_source_fields_magic_technology_relation.md" in text
    assert "A03_soul_body_mind_spirit_ontology.md" in text
    assert "A04_dao_domain_element_architecture.md" in text

    for phrase in [
        "a05 defines combat math",
        "a05 defines starship rules",
        "a05 defines travel mechanics",
        "a05 defines faction economies",
        "a05 defines runtime scale state",
        "a05 defines hidden-information behavior",
    ]:
        assert phrase not in lowered


def test_registry_a05_status_and_dependencies_posture():
    records = _registry_records()
    a05 = records["A05"]
    a04 = records["A04"]
    k01 = records["K01"]

    assert a05["status"] == "draft"
    assert a05["status"] != "current"
    assert a05["authority_level"] == "doctrine-draft"
    assert a05["test_status"] == "designed"
    assert a05["review_status"] == "not_reviewed"
    assert a05["proposed_path"] == "docs/doctrine/setting/A05_civilization_scale_and_power_scale_doctrine.md"
    assert a05["file_id"] == "A05"
    assert a05["filename"] == "A05_civilization_scale_and_power_scale_doctrine.md"
    assert a05["layer"] == "1_setting_spine"
    assert a05["phase"] == "1A"
    assert a05["dependencies"] == ["A01", "A02", "A03", "A04"]
    assert a05["blocked_by"] == []

    assert a04["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a04["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a05["filename"] != k01["filename"]
