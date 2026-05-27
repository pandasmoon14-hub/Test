from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A09_PATH = REPO_ROOT / "docs" / "doctrine" / "advancement" / "A09_skill_competency_and_synthesis_doctrine.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a09_file_exists():
    assert A09_PATH.exists()


def test_a09_required_sections_present():
    text = _read(A09_PATH)
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


def test_a09_required_grammar_terms_present():
    lowered = _read(A09_PATH).lower()
    for phrase in [
        "skill construct", "competency construct", "proficiency construct", "expertise construct", "specialization construct",
        "professional competency construct", "cultural competency construct", "background/lifepath competency construct",
        "knowledge competency construct", "practical competency construct", "social competency construct",
        "investigative competency construct", "crafting competency construct", "vehicle/platform competency construct",
        "source-local skill construct", "quarantined skill construct", "escalated skill problem",
        "formal training vector", "informal training vector", "experiential training vector", "cultural training vector",
        "professional training vector", "institutional training vector", "mentor-guided training vector",
        "self-directed training vector", "implanted/uploaded training vector", "inherited competency vector",
        "source-field-influenced training vector", "degraded/lost competency vector", "source-local training vector only",
        "quarantined training vector", "escalated training contradiction",
        "direct competency use", "assisted competency use", "composite competency use", "cross-skill synthesis",
        "multi-domain check", "domain-assisted competency", "technique-assisted competency", "tool-assisted competency",
        "asset/platform-assisted competency", "social/institutional competency support", "cultural-context dependency",
        "competency mismatch", "insufficient competency", "over-specialization pressure", "source-local synthesis only",
        "quarantined synthesis claim", "escalated competency contradiction",
    ]:
        assert phrase in lowered


def test_a09_boundaries_and_source_local_language_present():
    lowered = _read(A09_PATH).lower()
    for phrase in [
        "specific canon skill list", "specific skill names as astra defaults", "specific proficiency bonus math",
        "specific point-buy costs", "specific training time formulas", "specific crafting recipes",
        "specific professional rank ladders", "specific faction reputation systems", "technique mastery",
        "resource costs", "resource pool mechanics", "runtime skill instance state", "runtime progression state",
        "runtime event commits", "hidden information state", "accepted lexicon terms",
        "donor skill systems as astra default law",
        "donor skill/competency/proficiency/profession/career/lifepath/aspect systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra skill canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable skill/competency systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local skill/proficiency/profession terms do not become accepted lexicon terms through a09",
    ]:
        assert phrase in lowered


def test_a09_dependencies_and_non_redefinition_posture_present():
    text = _read(A09_PATH)
    lowered = text.lower()
    assert "A07_advancement_axes_and_progression_pressure.md" in text
    assert "A08_path_domain_and_technique_mastery_doctrine.md" in text
    for phrase in [
        "a07 advancement-axis taxonomy", "a08 technique mastery", "a08 activation/targeting grammar",
        "resource systems", "damage families", "condition/status rules", "actor stats",
        "runtime skill instance state", "runtime progression state", "runtime event commits",
        "hidden-information behavior",
    ]:
        assert phrase in lowered


def test_registry_a09_posture_and_downstream_not_promoted():
    records = _registry_records()
    a07 = records["A07"]
    a08 = records["A08"]
    a09 = records["A09"]
    k01 = records["K01"]

    assert a09["status"] == "draft"
    assert a09["status"] != "current"
    assert a09["authority_level"] == "doctrine-draft"
    assert a09["test_status"] == "designed"
    assert a09["review_status"] == "not_reviewed"
    assert a09["proposed_path"] == "docs/doctrine/advancement/A09_skill_competency_and_synthesis_doctrine.md"
    assert a09["dependencies"] == ["A07", "A08"]
    assert a09["blocked_by"] == []

    for rec in (a07, a08):
        assert rec["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
        assert rec["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a09["filename"] != k01["filename"]

    a10 = records["A10"]
    assert a10["status"] == "draft"
    assert a10["authority_level"] == "doctrine-draft"
    assert a10["test_status"] == "designed"

    for idx in range(11, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
