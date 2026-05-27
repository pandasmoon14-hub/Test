from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
A10_PATH = REPO_ROOT / "docs" / "doctrine" / "advancement" / "A10_resource_cost_backlash_and_corruption_doctrine.md"
REGISTRY_PATH = REPO_ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry_records():
    data = yaml.safe_load(_read(REGISTRY_PATH))
    records = data.get("file_records", data.get("files"))
    assert isinstance(records, list)
    return {r["file_id"]: r for r in records}


def test_a10_file_exists():
    assert A10_PATH.exists()


def test_a10_required_sections_present():
    text = _read(A10_PATH)
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


def test_a10_required_grammar_terms_present():
    lowered = _read(A10_PATH).lower()
    for phrase in [
        "resource construct", "energy-like resource construct", "reserve-like resource construct",
        "vitality-like resource construct", "focus-like resource construct", "charge-like resource construct",
        "debt-like resource construct", "sacrifice-like resource construct", "favor/disfavor-like resource construct",
        "contamination-like resource construct", "source-local resource construct", "quarantined resource construct",
        "escalated resource contradiction", "baseline cost posture", "elevated cost posture",
        "reserve commitment posture", "overcommitment posture", "deferred payment posture",
        "conditional payment posture", "quarantined cost claim", "backlash exposure", "overload exposure",
        "heat/strain exposure", "fatigue/wear exposure", "debt burden exposure", "sacrifice burden exposure",
        "corruption pressure", "contamination pressure", "reputation/favor fallout pressure",
        "quarantined consequence claim", "escalated consequence contradiction",
    ]:
        assert phrase in lowered


def test_a10_boundaries_and_source_local_language_present():
    lowered = _read(A10_PATH).lower()
    for phrase in [
        "specific technique costs", "specific spell costs", "specific power costs", "specific item prices",
        "economy/currency rules", "resource pool numbers", "exact resource values", "exact recharge rates",
        "exact cooldown durations", "exact corruption tracks", "exact heat/stress tracks",
        "exact favor/debt ledgers", "exact sacrifice formulas", "combat damage families", "damage formulas",
        "condition/status rules", "actor stat blocks", "technique mastery", "skill systems",
        "faction reputation systems", "crafting recipes", "runtime resource/cooldown/corruption state",
        "runtime event commits", "hidden information state", "accepted lexicon terms",
        "donor resource systems as astra default law",
        "donor resource/cost/backlash/corruption systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra resource canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable resource/cost/consequence systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local resource/cost/backlash terms do not become accepted lexicon terms through a10",
    ]:
        assert phrase in lowered


def test_a10_dependencies_and_non_redefinition_posture_present():
    text = _read(A10_PATH)
    lowered = text.lower()
    assert "A02_source_fields_magic_technology_relation.md" in text
    assert "A04_dao_domain_element_architecture.md" in text
    assert "A06_cultivation_and_ascension_stage_architecture.md" in text
    assert "A08_path_domain_and_technique_mastery_doctrine.md" in text
    assert "A09_skill_competency_and_synthesis_doctrine.md" in text
    for phrase in [
        "a02 source-field relation matrices", "a04 domain taxonomy", "a06 stage taxonomy",
        "a08 technique mastery", "a09 skill/competency taxonomy", "damage families",
        "condition/status rules", "actor stats", "runtime event commits", "runtime actor state",
        "hidden-information behavior",
    ]:
        assert phrase in lowered


def test_registry_a10_posture_and_downstream_todo_unchanged():
    records = _registry_records()
    a09 = records["A09"]
    a10 = records["A10"]

    assert a10["status"] == "draft"
    assert a10["status"] != "current"
    assert a10["authority_level"] == "doctrine-draft"
    assert a10["test_status"] == "designed"
    assert a10["review_status"] == "not_reviewed"
    assert a10["proposed_path"] == "docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md"
    assert a10["dependencies"] == ["A02", "A04", "A06", "A08", "A09"]
    assert a10["blocked_by"] == []

    assert a09["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
    assert a09["status"] != "current"

    for idx in range(11, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
