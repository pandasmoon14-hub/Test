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
A02_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A02_source_fields_magic_technology_relation.md"
A01_PATH = REPO_ROOT / "docs" / "doctrine" / "setting" / "A01_cosmology_and_dimensional_architecture.md"
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


def test_a02_required_source_field_classification_terms_present():
    text = _read(A02_PATH).lower()
    for phrase in [
        "arcane/magical source field",
        "technological/instrumental source field",
        "psionic/cognitive source field",
        "divine/sacral source field",
        "cultivation/internal-refinement source field",
        "biological/biotech source field",
        "cybernetic/implant source field",
        "computational/informational source field",
        "dimensional/topological source field",
        "relic/artifact-mediated source field",
        "environmental/local field",
        "hybrid source field",
        "source-local donor field",
        "quarantined source-field construct",
        "escalated source-field problem",
    ]:
        assert phrase in text


def test_a02_interaction_matrix_grammar_terms_present():
    text = _read(A02_PATH).lower()
    for phrase in [
        "compatible",
        "incompatible",
        "attenuating",
        "amplifying",
        "transforming",
        "parasitic",
        "masking/occluding",
        "mutually exclusive under current doctrine",
        "source-local only",
        "quarantined pending later doctrine",
        "escalated contradiction",
    ]:
        assert phrase in text


def test_a02_must_not_own_boundaries_present():
    text = _read(A02_PATH).lower()
    for phrase in [
        "specific spells",
        "specific techniques",
        "specific devices",
        "resource pools",
        "cultivation stage",
        "runtime state",
        "accepted lexicon terms",
        "donor metaphysics as astra default law",
    ]:
        assert phrase in text


def test_a02_source_local_quarantine_escalation_language_present():
    text = _read(A02_PATH).lower()
    assert "source-local" in text
    assert "quarantined" in text or "quarantine" in text
    assert "escalated" in text


def test_a02_depends_on_a01_but_does_not_redefine_a01_cosmology_terms():
    text = _read(A02_PATH)
    lowered = text.lower()

    assert "A01_cosmology_and_dimensional_architecture.md" in text
    assert "dimensional/topological source field" in lowered

    for phrase in [
        "a02 owns worlds",
        "a02 owns planes",
        "a02 owns voids",
        "a02 defines worlds",
        "a02 defines planes",
        "a02 defines voids",
        "a02 defines dimensional topology",
        "a02 replaces a01",
        "a02 supersedes a01",
    ]:
        assert phrase not in lowered

    assert "Specific planets or planes as canon." in text


def test_registry_a02_a01_and_k01_status_and_separation():
    records = _registry_records()
    a02 = records["A02"]
    a01 = records["A01"]
    k01 = records["K01"]

    assert a02["status"] == "draft"
    assert a02["status"] != "current"
    assert a02["review_status"] == "not_reviewed"
    assert a02["proposed_path"] == "docs/doctrine/setting/A02_source_fields_magic_technology_relation.md"
    assert "A01" in a02["dependencies"]

    assert a01["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a01["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a02["filename"] != k01["filename"]
