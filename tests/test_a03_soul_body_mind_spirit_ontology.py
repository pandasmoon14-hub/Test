from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A03_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A03_soul_body_mind_spirit_ontology.md"
A02_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A02_source_fields_magic_technology_relation.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a03_file_exists():
    assert A03_PATH.exists()


def test_a03_has_required_14_sections():
    text = _read(A03_PATH)
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


def test_a03_required_ontology_terms_present():
    text = _read(A03_PATH).lower()
    for phrase in [
        "body component",
        "soul component",
        "mind component",
        "spirit component",
        "identity continuity profile",
        "ai personhood candidate",
        "upload/copy instance",
        "possession/bonding construct",
        "death/persistence boundary event class",
        "source-local ontology construct",
        "quarantined ontology construct",
        "escalated ontology problem",
    ]:
        assert phrase in text


def test_a03_must_not_own_boundaries_present():
    text = _read(A03_PATH).lower()
    for phrase in [
        "specific actor stats",
        "specific implants",
        "specific resurrection mechanics",
        "resource pools",
        "action economy",
        "damage",
        "conditions",
        "cultivation stages",
        "progression",
        "runtime actor state",
        "event commits",
        "accepted lexicon terms",
        "canon lore declarations",
    ]:
        assert phrase in text


def test_a03_k01_separation_and_no_renaming_constraints_present():
    text = _read(A03_PATH)
    lowered = text.lower()

    assert "A03_soul_body_mind_spirit_ontology.md" in text
    assert "K01 remains separate" in text

    for phrase in [
        "rename a03",
        "move k01 into a03",
        "a03 is current",
    ]:
        assert phrase not in lowered


def test_registry_a03_status_and_dependency_posture_after_a02():
    records = _registry_records()
    a03 = records["A03"]
    a02 = records["A02"]

    assert a03["status"] == "draft"
    assert a03["status"] != "current"
    assert a03["review_status"] == "not_reviewed"
    assert a03["proposed_path"] == "docs/doctrine/setting/A03_soul_body_mind_spirit_ontology.md"
    assert "A01" in a03["dependencies"]
    assert "A02" in a03["dependencies"]
    assert a03["blocked_by"] == []

    assert a02["status"] in {"draft", "review", "pressure-tested"}
