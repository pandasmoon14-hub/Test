from pathlib import Path

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
A05_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A05_civilization_scale_and_power_scale_doctrine.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a05_file_exists_and_has_required_sections():
    text = _read(A05_PATH)
    assert A05_PATH.exists()
    for heading in [
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
    ]:
        assert heading in text


def test_a05_required_scale_taxonomy_grammar_terms_present():
    text = _read(A05_PATH).lower()
    for phrase in [
        "personal scale",
        "squad/group scale",
        "community/local scale",
        "institutional/factional scale",
        "regional scale",
        "planetary scale",
        "orbital scale",
        "stellar scale",
        "interstellar/sector scale",
        "void scale",
        "planar scale",
        "cosmic scale",
        "source-local scale construct",
        "quarantined scale construct",
        "escalated scale problem",
    ]:
        assert phrase in text


def test_a05_required_scale_transition_grammar_terms_present():
    text = _read(A05_PATH).lower()
    for phrase in [
        "same-scale action",
        "upward scale transition",
        "downward scale transition",
        "cross-scale influence",
        "indirect scale influence",
        "scale mismatch",
        "scale shielding",
        "scale amplification",
        "scale attenuation",
        "scale spillover",
        "constrained scale transition",
        "source-local transition only",
        "quarantined scale transition",
        "escalated scale contradiction",
    ]:
        assert phrase in text


def test_a05_required_power_boundary_grammar_terms_present():
    text = _read(A05_PATH).lower()
    for phrase in [
        "scale-appropriate capability",
        "over-scale capability",
        "under-scale capability",
        "localized overmatch",
        "diffuse influence",
        "macro-actor permission",
        "macro-actor restriction",
        "hazard-scale mismatch",
        "consequence propagation",
        "source-local power boundary only",
        "quarantined power boundary",
        "escalated power-scale contradiction",
    ]:
        assert phrase in text


def test_a05_must_not_own_boundaries_and_source_local_rules_present():
    text = _read(A05_PATH).lower()
    for phrase in [
        "specific empires",
        "specific starships",
        "specific combat math",
        "specific travel times",
        "faction economies",
        "runtime scale state",
        "runtime map state",
        "hidden information state",
        "accepted lexicon terms",
        "donor scale models as astra default law",
        "donor scale systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra scale canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable scale systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local scale terms do not become accepted lexicon terms through a05",
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
        "a05 defines worlds",
        "a05 defines planes",
        "a05 defines source fields",
        "a05 defines magic/technology relations",
        "a05 defines identity continuity",
        "a05 defines dao/domain/element rules",
        "a05 defines resource systems",
        "a05 defines progression ladders",
        "a05 defines runtime state",
        "a05 defines hidden-information behavior",
    ]:
        assert phrase not in lowered


def test_registry_a05_status_and_separation_posture():
    records = _registry_records()
    a01 = records["A01"]
    a02 = records["A02"]
    a03 = records["A03"]
    a04 = records["A04"]
    a05 = records["A05"]
    k01 = records["K01"]

    assert a05["status"] == "draft"
    assert a05["status"] != "current"
    assert a05["authority_level"] == "doctrine-draft"
    assert a05["test_status"] == "designed"
    assert a05["review_status"] == "not_reviewed"
    assert a05["proposed_path"] == "docs/doctrine/setting/A05_civilization_scale_and_power_scale_doctrine.md"
    assert a05["dependencies"] == ["A01", "A02", "A03", "A04"]
    assert a05["blocked_by"] == []

    for rec in (a01, a02, a03, a04):
        assert rec["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
        assert rec["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a05["filename"] != k01["filename"]
