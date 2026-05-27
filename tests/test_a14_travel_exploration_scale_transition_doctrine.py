from tests.helpers import ROOT, read_utf8, registry_records_by_id

A14_PATH = ROOT / "docs" / "doctrine" / "world" / "A14_travel_exploration_and_scale_transition_doctrine.md"


def test_a14_file_exists_at_registry_path():
    records = registry_records_by_id()
    a14 = records["A14"]
    assert a14["proposed_path"] == "docs/doctrine/world/A14_travel_exploration_and_scale_transition_doctrine.md"
    assert A14_PATH.exists()


def test_a14_required_sections_present():
    text = read_utf8(A14_PATH)
    for heading in [
        "## 1. Purpose and status", "## 2. What this file owns", "## 3. What this file must not own",
        "## 4. Required definitions", "## 5. Core doctrine rules", "## 6. Conversion mapping rules",
        "## 7. Source-local handling", "## 8. Donor pressure absorbed", "## 9. Hard refusals / rejected imports",
        "## 10. Escalation triggers", "## 11. Dependencies", "## 12. Handoff to downstream layers",
        "## 13. Test cases / pressure examples", "## 14. Versioning and review protocol",
    ]:
        assert heading in text


def test_a14_required_travel_scale_grammar_terms_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "travel construct", "travel scale construct", "local travel construct", "regional travel construct",
        "planetary travel construct", "orbital travel construct", "stellar travel construct", "void travel construct",
        "planar travel construct", "dimensional travel construct", "scale-transition construct",
        "source-local travel construct", "quarantined travel construct", "escalated travel-scale problem",
    ]:
        assert phrase in lowered


def test_a14_required_route_and_transition_grammar_terms_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "route construct", "path construct", "corridor construct", "gate construct", "portal construct",
        "jump construct", "transit-vector construct", "route-stability claim", "route-instability claim",
        "transition-cost claim", "transition-constraint claim", "access-precondition claim",
        "arrival-consequence claim", "travel-risk claim", "travel-hazard claim", "source-field transit claim",
        "asset-mediated transit claim", "source-local route only", "quarantined transition claim",
        "escalated transition contradiction",
    ]:
        assert phrase in lowered


def test_a14_required_exploration_and_site_grammar_terms_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "exploration construct", "discovery claim", "survey claim", "navigation claim", "route-finding claim",
        "wilderness-exploration claim", "urban-exploration claim", "void-exploration claim",
        "planar-exploration claim", "ruin construct", "megastructure construct", "exploration-hazard claim",
        "exploration-consequence claim", "provenance-bearing site claim", "hidden-site claim",
        "source-local exploration only", "quarantined exploration claim", "escalated exploration contradiction",
    ]:
        assert phrase in lowered


def test_a14_must_not_own_boundaries_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "cosmology topology", "plane topology", "route maps", "gate-network maps", "portal lists",
        "travel time math", "fuel/supply rules", "navigation procedure", "hexcrawl procedure",
        "random encounter procedure", "starship operation procedure", "jump-drive rules", "teleportation rules",
        "specific starship stats", "vehicle stats", "specific hazard tables", "faction logistics",
        "trade/economy rules", "settlement procedure", "runtime travel state", "runtime location state",
        "runtime route state", "runtime hidden-information state", "runtime event commits",
    ]:
        assert phrase in lowered


def test_a14_source_local_and_lexicon_boundary_language_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "donor travel systems", "donor route systems", "donor portal/gate systems",
        "donor dimensional transit systems", "donor wilderness exploration systems",
        "donor ruin exploration systems", "donor megastructure systems", "donor secret-realm systems",
        "donor exploration-procedure systems can be retained as source-local records",
        "source-local travel, route, gate, portal, jump, transit, exploration, ruin, megastructure, hexcrawl, teleportation, plane, and dimension terms do not become accepted lexicon terms through a14",
        "quarantined", "escalated",
    ]:
        assert phrase in lowered


def test_a14_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A14_PATH)
    lowered = text.lower()
    for dep in [
        "A01_cosmology_and_dimensional_architecture.md", "A05_civilization_scale_and_power_scale_doctrine.md",
        "A12_asset_relic_implant_platform_doctrine.md", "A13_combat_hazard_damage_and_consequence_doctrine.md",
    ]:
        assert dep in text
    for phrase in [
        "a14 does not redefine a01 cosmology boundaries", "a05 scale doctrine boundaries",
        "a12 asset taxonomy boundaries", "a13 hazard/damage/consequence taxonomy boundaries",
    ]:
        assert phrase in lowered


def test_registry_a14_k01_separation_and_a15_guardrail():
    records = registry_records_by_id()
    a14 = records["A14"]
    assert a14["status"] == "draft"
    assert a14["authority_level"] == "doctrine-draft"
    assert a14["test_status"] == "designed"
    assert a14["review_status"] == "not_reviewed"
    assert a14["blocked_by"] == []

    assert records["K01"]["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"

    a15 = records["A15"]
    assert a15["status"] == "draft"
    assert a15["status"] != "current"
    assert a15["authority_level"] == "doctrine-draft"
    assert a15["test_status"] == "designed"
    assert a15["review_status"] == "not_reviewed"


def test_registry_ckrt_layers_not_promoted():
    records = registry_records_by_id()
    for rec in records.values():
        if rec.get("layer") in {"4_schema_base", "5_canon_lexicon", "6_runtime_backend", "7_training_evaluation"}:
            assert rec["status"] in {"todo", "blocked", "deprecated", "draft", "review", "pressure-tested"}
            assert rec["status"] != "current"
