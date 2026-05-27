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
        "corporation construct", "empire construct", "court construct", "community construct", "polity construct",
        "faction-type construct", "institutional hierarchy claim", "institutional authority claim",
        "institutional membership claim", "institutional advancement claim", "source-local faction construct",
        "quarantined faction construct", "escalated institution problem",
        "economy construct", "value construct", "currency claim", "price claim", "trade construct",
        "market construct", "requisition claim", "logistics construct", "supply-chain claim", "trade-route claim",
        "scarcity claim", "abundance claim", "institutional resource claim", "source-local economy only",
        "quarantined economy claim", "escalated economy contradiction",
        "law construct", "jurisdiction claim", "standing claim", "reputation claim", "legitimacy claim",
        "obligation claim", "debt/favor claim", "sanction claim", "diplomacy claim", "alliance claim",
        "rivalry claim", "colonization claim", "domain-management claim", "conflict-of-law claim",
        "source-local reputation only", "quarantined law claim", "escalated faction contradiction",
    ]:
        assert phrase in lowered


def test_a15_source_local_and_lexicon_boundary_language_present():
    lowered = read_utf8(A15_PATH).lower()
    for phrase in [
        "donor faction, renown, corporation, empire, sect, guild, court, kingdom/domain, trade, currency, market, requisition, reputation, law, diplomacy, colonization, logistics, and institutional-advancement systems can be retained as source-local records",
        "source-local faction, society, economy, currency, trade, market, requisition, law, reputation, standing, diplomacy, empire, corporation, sect, guild, court, kingdom, domain, colony, or institution terms do not become accepted lexicon terms through a15",
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
    assert a15["status"] == "draft"
    assert a15["status"] != "current"
    assert a15["authority_level"] == "doctrine-draft"
    assert a15["test_status"] == "designed"
    assert a15["review_status"] == "not_reviewed"
    assert a15["blocked_by"] == []
    assert records["K01"]["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"


def test_registry_ckrt_layers_not_promoted():
    records = registry_records_by_id()
    for rec in records.values():
        if rec.get("layer") in {"4_schema_base", "5_canon_lexicon", "6_runtime_backend", "7_training_evaluation"}:
            assert rec["status"] != "current"
