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
A03_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A03_soul_body_mind_spirit_ontology.md"
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


def test_a03_required_ontology_classification_terms_present():
    text = _read(A03_PATH).lower()
    for phrase in [
        "body component",
        "mind component",
        "soul component",
        "spirit component",
        "identity anchor",
        "continuity claim",
        "discontinuity event",
        "embodied personhood",
        "disembodied personhood",
        "artificial/constructed personhood",
        "uploaded identity",
        "copied/forked identity",
        "hosted identity",
        "possessed identity",
        "bonded identity",
        "symbiotic identity",
        "reincarnated/returned identity claim",
        "restored/reconstructed identity claim",
        "undead/persistent remnant identity claim",
        "source-local identity construct",
        "quarantined identity construct",
        "escalated identity problem",
    ]:
        assert phrase in text


def test_a03_continuity_outcome_grammar_terms_present():
    text = _read(A03_PATH).lower()
    for phrase in [
        "continuous identity",
        "interrupted but continuous identity",
        "reconstructed identity",
        "copied identity",
        "forked identity",
        "merged identity",
        "hosted identity",
        "possessed identity",
        "bonded/symbiotic identity",
        "remnant identity",
        "apparent continuity only",
        "source-local only",
        "quarantined pending later doctrine",
        "escalated contradiction",
    ]:
        assert phrase in text


def test_a03_must_not_own_boundaries_present():
    text = _read(A03_PATH).lower()
    for phrase in [
        "specific actor stats",
        "specific implants",
        "specific cyberware assets",
        "specific resurrection mechanics",
        "cultivation stages",
        "resource pools",
        "runtime actor state",
        "hidden information state",
        "accepted lexicon terms",
        "donor soul, afterlife, or essence mechanics as astra default law",
    ]:
        assert phrase in text


def test_a03_source_local_quarantine_escalation_language_present():
    text = _read(A03_PATH).lower()
    for phrase in [
        "source-local",
        "preserve donor provenance",
        "do not become astra ontology canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "quarantined",
        "escalated",
        "not normalized by invention",
        "donor proper nouns remain source-local",
        "do not become accepted lexicon terms through a03",
    ]:
        assert phrase in text


def test_a03_references_a01_and_a02_but_does_not_redefine_their_ownership():
    text = _read(A03_PATH)
    lowered = text.lower()

    assert "A01_cosmology_and_dimensional_architecture.md" in text
    assert "A02_source_fields_magic_technology_relation.md" in text

    for phrase in [
        "a03 defines worlds",
        "a03 defines planes",
        "a03 defines voids",
        "a03 defines dimensional topology",
        "a03 defines source fields",
        "a03 defines magic/technology relation",
        "a03 defines runtime state",
    ]:
        assert phrase not in lowered


def test_registry_a03_status_and_dependency_posture_after_a02():
    records = _registry_records()
    a03 = records["A03"]
    a01 = records["A01"]
    a02 = records["A02"]
    k01 = records["K01"]

    assert a03["status"] == "draft"
    assert a03["status"] != "current"
    assert a03["test_status"] == "designed"
    assert a03["review_status"] == "not_reviewed"
    assert a03["proposed_path"] == "docs/doctrine/setting/A03_soul_body_mind_spirit_ontology.md"
    assert "A01" in a03["dependencies"]
    assert "A02" in a03["dependencies"]
    assert a03["blocked_by"] == []

    assert a01["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a01["status"] != "current"

    assert a02["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a02["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a03["filename"] != k01["filename"]
