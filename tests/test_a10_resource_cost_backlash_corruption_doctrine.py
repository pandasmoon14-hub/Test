from tests.helpers import ROOT, read_utf8, registry_records_by_id

A10_PATH = ROOT / "docs" / "doctrine" / "advancement" / "A10_resource_cost_backlash_and_corruption_doctrine.md"


def test_a10_file_exists():
    assert A10_PATH.exists()


def test_a10_required_sections_present():
    text = read_utf8(A10_PATH)
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
    lowered = read_utf8(A10_PATH).lower()
    for phrase in [
        "resource construct", "cost construct", "reserve construct", "occupancy/reserve construct",
        "cooldown construct", "recharge construct", "regeneration construct", "backlash construct",
        "corruption construct", "overload construct", "heat/stress construct", "strain/fatigue construct",
        "debt construct", "sacrifice construct", "favor/disfavor construct", "spiritual damage construct",
        "dimensional contamination construct", "source-local resource construct", "quarantined resource construct",
        "escalated resource problem",
        "activation cost", "maintenance cost", "sustained cost", "reserve occupancy", "expendable cost",
        "opportunity cost", "cooldown requirement", "recharge requirement", "depletion pressure",
        "overuse pressure", "risk-bearing cost", "backlash-bearing cost", "corruption-bearing cost",
        "sacrifice cost", "debt cost", "favor/disfavor cost", "source-local cost only",
        "quarantined cost claim", "escalated cost contradiction",
        "minor backlash", "major backlash", "catastrophic backlash", "immediate backlash",
        "delayed backlash", "accumulating corruption", "unstable overload", "heat/stress event",
        "strain/fatigue event", "spiritual injury", "dimensional contamination", "sacrifice consequence",
        "debt obligation", "favor consequence", "disfavor consequence", "source-local backlash only",
        "quarantined backlash claim", "escalated consequence contradiction",
    ]:
        assert phrase in lowered


def test_a10_boundaries_and_source_local_language_present():
    lowered = read_utf8(A10_PATH).lower()
    for phrase in [
        "specific technique costs", "specific spell costs", "specific power costs", "specific item prices",
        "specific currency/economy rules", "specific resource pool numbers", "exact resource values",
        "exact recharge rates", "exact cooldown durations", "exact corruption point tracks",
        "exact heat/stress tracks", "exact favor/debt ledgers", "exact sacrifice formulas",
        "combat damage families", "damage formulas", "condition/status rules", "actor stat blocks",
        "technique mastery", "skill/competency systems", "faction reputation systems", "crafting recipes",
        "travel/exploration resource accounting", "runtime resource values", "runtime cooldown state",
        "runtime corruption state", "runtime event commits", "hidden information state",
        "accepted lexicon terms", "donor resource systems as astra default law",
        "donor resource/cost/backlash/corruption/cooldown/heat/debt/favor systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra resource canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable resource/cost/consequence systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local resource/cost/backlash terms do not become accepted lexicon terms through a10",
        "quarantined resource constructs", "quarantined cost claims", "quarantined backlash claims",
        "escalated resource problems",
    ]:
        assert phrase in lowered


def test_a10_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A10_PATH)
    lowered = text.lower()
    for dep in [
        "A02_source_fields_magic_technology_relation.md",
        "A04_dao_domain_element_architecture.md",
        "A06_cultivation_and_ascension_stage_architecture.md",
        "A08_path_domain_and_technique_mastery_doctrine.md",
        "A09_skill_competency_and_synthesis_doctrine.md",
    ]:
        assert dep in text
    for phrase in [
        "a02 source-field relation matrices", "a04 domain taxonomy", "a06 stage taxonomy",
        "a08 technique mastery or specific technique costs", "a09 skill/competency taxonomy",
        "damage families", "condition/status rules", "actor stats", "runtime resource state",
        "runtime cooldown state", "runtime event commits", "hidden-information behavior",
    ]:
        assert phrase in lowered


def test_registry_a10_posture_and_guards():
    records = registry_records_by_id()
    a02 = records["A02"]
    a04 = records["A04"]
    a06 = records["A06"]
    a08 = records["A08"]
    a09 = records["A09"]
    a10 = records["A10"]
    k01 = records["K01"]

    assert a10["status"] == "draft"
    assert a10["status"] != "current"
    assert a10["authority_level"] == "doctrine-draft"
    assert a10["test_status"] == "designed"
    assert a10["review_status"] == "not_reviewed"
    assert a10["proposed_path"] == "docs/doctrine/advancement/A10_resource_cost_backlash_and_corruption_doctrine.md"

    assert a10["file_id"] == "A10"
    assert a10["filename"] == "A10_resource_cost_backlash_and_corruption_doctrine.md"
    assert a10["layer"] == "2_advancement_action_spine"
    assert a10["phase"] == "1B"
    assert a10["dependencies"] == ["A02", "A04", "A06", "A08", "A09"]
    assert a10["blocked_by"] == []

    for rec in (a02, a04, a06, a08, a09):
        assert rec["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
        assert rec["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a10["filename"] != k01["filename"]

    a11 = records["A11"]
    assert a11["status"] == "draft"
    assert a11["authority_level"] == "doctrine-draft"
    assert a11["test_status"] == "designed"

    for idx in range(13, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
