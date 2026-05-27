from tests.helpers import ROOT, read_utf8, registry_records_by_id

A15_PATH = ROOT / "docs" / "doctrine" / "world" / "A15_faction_society_economy_and_institution_doctrine.md"


def test_a15_file_exists_at_registry_path():
    records = registry_records_by_id()
    a15 = records["A15"]
    assert a15["proposed_path"] == "docs/doctrine/world/A15_faction_society_economy_and_institution_doctrine.md"
    assert A15_PATH.exists()


def test_a15_required_sections_present():
    text = read_utf8(A15_PATH)
    for heading in [
        "## 1. Purpose and status", "## 2. What this file owns", "## 3. What this file must not own",
        "## 4. Required definitions", "## 5. Core doctrine rules", "## 6. Conversion mapping rules",
        "## 7. Source-local handling", "## 8. Donor pressure absorbed", "## 9. Hard refusals / rejected imports",
        "## 10. Escalation triggers", "## 11. Dependencies", "## 12. Handoff to downstream layers",
        "## 13. Test cases / pressure examples", "## 14. Versioning and review protocol",
    ]:
        assert heading in text


def test_a15_required_grammar_terms_present():
    lowered = read_utf8(A15_PATH).lower()
    for phrase in [
        "faction construct", "society construct", "institution construct", "sect construct", "guild construct",
        "corporation construct", "empire construct", "planar-court construct", "hierarchy claim",
        "economy construct", "value construct", "requisition construct", "exchange claim", "scarcity claim",
        "supply claim", "demand claim", "logistics claim", "trade-network claim", "law construct",
        "reputation construct", "standing construct", "diplomacy claim", "war claim", "colonization claim",
        "institutional advancement claim", "source-local institution only", "quarantined institutional claim",
        "escalated institutional contradiction",
    ]:
        assert phrase in lowered


def test_a15_must_not_own_boundaries_present():
    lowered = read_utf8(A15_PATH).lower()
    for phrase in [
        "named faction canon", "specific faction stats", "specific currencies/prices", "price lists",
        "market simulation", "exact reputation systems", "law procedure", "diplomacy procedure",
        "trade procedure", "logistics procedure", "colonization procedure", "settlement/domain procedure",
        "runtime faction state", "runtime economy state", "runtime reputation state", "runtime trade-route state",
        "runtime hidden-information behavior", "runtime event commits", "accepted lexicon terms", "sourcebook prose",
    ]:
        assert phrase in lowered


def test_a15_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A15_PATH)
    lowered = text.lower()
    for dep in [
        "A05_civilization_scale_and_power_scale_doctrine.md",
        "A11_actor_ontology_and_player_grade_actor_doctrine.md",
        "A12_asset_relic_implant_platform_doctrine.md",
        "A13_combat_hazard_damage_and_consequence_doctrine.md",
        "A14_travel_exploration_and_scale_transition_doctrine.md",
    ]:
        assert dep in text
    for phrase in [
        "a15 does not redefine a05 scale boundaries",
        "a11 actor ontology boundaries",
        "a12 asset taxonomy boundaries",
        "a13 hazard/damage/consequence boundaries",
        "a14 travel/exploration boundaries",
    ]:
        assert phrase in lowered


def test_registry_a15_status_guardrail():
    records = registry_records_by_id()
    a15 = records["A15"]
    assert a15["status"] == "todo"
    assert a15["authority_level"] == "doctrine-todo"
    assert a15["test_status"] == "not_started"
    assert a15["review_status"] == "not_reviewed"
    assert a15["blocked_by"] == ["A05", "A11", "A12", "A13", "A14"]
