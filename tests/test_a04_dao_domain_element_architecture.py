from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A04_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A04_dao_domain_element_architecture.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a04_file_exists():
    assert A04_PATH.exists()


def test_a04_has_required_14_sections():
    text = _read(A04_PATH)
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


def test_a04_required_conceptual_classification_grammar_terms_present():
    text = _read(A04_PATH).lower()
    for phrase in [
        "dao construct",
        "domain construct",
        "element construct",
        "concept/law construct",
        "aspect/tag-like construct",
        "sphere/paradigm-like construct",
        "tradition/school-like construct",
        "portfolio-like construct",
        "elemental family",
        "conceptual family",
        "source-local conceptual construct",
        "quarantined conceptual construct",
        "escalated conceptual problem",
    ]:
        assert phrase in text


def test_a04_required_interaction_grammar_terms_present():
    text = _read(A04_PATH).lower()
    for phrase in [
        "resonance",
        "antagonism",
        "synthesis",
        "containment",
        "adjacency",
        "opposition",
        "transformation",
        "contamination",
        "occlusion/masking",
        "unstable hybridization",
        "source-local only",
        "quarantined pending later doctrine",
        "escalated contradiction",
    ]:
        assert phrase in text


def test_a04_required_synthesis_grammar_terms_present():
    text = _read(A04_PATH).lower()
    for phrase in [
        "compatible synthesis",
        "constrained synthesis",
        "unstable synthesis",
        "antagonistic synthesis",
        "dominant-subordinate synthesis",
        "balanced synthesis",
        "source-local synthesis only",
        "quarantined synthesis",
        "escalated synthesis contradiction",
    ]:
        assert phrase in text


def test_a04_must_not_own_boundaries_present():
    text = _read(A04_PATH).lower()
    for phrase in [
        "specific techniques",
        "specific spells",
        "resource pools",
        "cultivation stages",
        "faction control of domains",
        "donor dao imports",
        "runtime state",
        "hidden information state",
        "accepted lexicon terms",
        "donor conceptual metaphysics as astra default law",
    ]:
        assert phrase in text


def test_a04_source_local_quarantine_escalation_language_present():
    text = _read(A04_PATH).lower()
    for phrase in [
        "source-local",
        "provenance",
        "do not become astra architecture canon",
        "repeated donor pressure may form canon candidates only through later k-layer/canon review",
        "quarantined",
        "escalated",
        "not normalized by invention",
    ]:
        assert phrase in text


def test_a04_mentions_a01_a02_a03_but_does_not_redefine_owned_areas():
    text = _read(A04_PATH)
    lowered = text.lower()

    assert "A01_cosmology_and_dimensional_architecture.md" in text
    assert "A02_source_fields_magic_technology_relation.md" in text
    assert "A03_soul_body_mind_spirit_ontology.md" in text

    for phrase in [
        "a04 defines worlds",
        "a04 defines planes",
        "a04 defines source fields",
        "a04 defines magic/technology relation",
        "a04 defines identity continuity",
        "a04 defines resource systems",
        "a04 defines progression ladders",
        "a04 defines runtime state",
        "a04 defines hidden-information behavior",
    ]:
        assert phrase not in lowered


def test_registry_a04_status_and_dependencies_posture():
    records = _registry_records()
    a04 = records["A04"]
    a01 = records["A01"]
    a02 = records["A02"]
    a03 = records["A03"]
    k01 = records["K01"]

    assert a04["status"] == "draft"
    assert a04["status"] != "current"
    assert a04["authority_level"] == "doctrine-draft"
    assert a04["test_status"] == "designed"
    assert a04["review_status"] == "not_reviewed"
    assert a04["proposed_path"] == "docs/doctrine/setting/A04_dao_domain_element_architecture.md"
    assert a04["file_id"] == "A04"
    assert a04["filename"] == "A04_dao_domain_element_architecture.md"
    assert a04["layer"] == "1_setting_spine"
    assert a04["phase"] == "1A"
    assert a04["dependencies"] == ["A01", "A02", "A03"]

    assert a01["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a01["status"] != "current"
    assert a02["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a02["status"] != "current"
    assert a03["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a03["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a04["filename"] != k01["filename"]
