from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A06_PATH = REPO_ROOT / "docs" / "doctrine" / "advancement" / "A06_cultivation_and_ascension_stage_architecture.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a06_file_exists_and_has_required_sections():
    text = _read(A06_PATH)
    assert A06_PATH.exists()
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


def test_a06_required_stage_taxonomy_terms_present():
    text = _read(A06_PATH).lower()
    for phrase in [
        "foundation stage construct",
        "refinement stage construct",
        "integration stage construct",
        "transformation stage construct",
        "ascension interface stage construct",
        "source-local stage construct",
        "quarantined stage construct",
        "escalated stage problem",
    ]:
        assert phrase in text


def test_a06_required_transition_terms_present():
    text = _read(A06_PATH).lower()
    for phrase in [
        "intra-stage transition",
        "inter-stage transition",
        "upward ascension transition",
        "constrained ascension transition",
        "deferred ascension transition",
        "stage mismatch",
        "ascension gating",
        "ascension spillover",
        "source-local ascension transition only",
        "quarantined ascension transition",
        "escalated ascension contradiction",
    ]:
        assert phrase in text


def test_a06_required_boundary_terms_present():
    text = _read(A06_PATH).lower()
    for phrase in [
        "breakthrough posture",
        "bottleneck posture",
        "tribulation posture",
        "threshold coherence",
        "threshold contradiction",
        "stage permission",
        "stage restriction",
        "source-local breakthrough boundary only",
        "quarantined breakthrough boundary",
        "escalated breakthrough contradiction",
    ]:
        assert phrase in text


def test_a06_hard_boundaries_and_source_local_rules_present():
    text = _read(A06_PATH).lower()
    for phrase in [
        "specific cultivation realms",
        "specific donor stage names",
        "specific techniques",
        "spells or powers",
        "classes or class features",
        "stat bonuses",
        "resource pools, costs, recharge, or backlash",
        "xp tables or level tables",
        "runtime advancement state",
        "runtime event commits",
        "runtime actor state",
        "hidden-information behavior",
        "donor stage systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra stage canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable stage systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local stage terms do not become accepted lexicon terms through a06",
    ]:
        assert phrase in text


def test_registry_a06_status_and_separation_posture():
    records = _registry_records()
    a06 = records["A06"]
    a05 = records["A05"]
    k01 = records["K01"]

    assert a06["status"] == "draft"
    assert a06["status"] != "current"
    assert a06["authority_level"] == "doctrine-draft"
    assert a06["test_status"] == "designed"
    assert a06["review_status"] == "not_reviewed"
    assert a06["proposed_path"] == "docs/doctrine/advancement/A06_cultivation_and_ascension_stage_architecture.md"
    assert a06["dependencies"] == ["A01", "A02", "A03", "A04", "A05"]
    assert a06["blocked_by"] == []

    assert a05["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a05["status"] != "current"
    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a06["filename"] != k01["filename"]
