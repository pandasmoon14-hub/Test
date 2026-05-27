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


def test_a14_required_travel_and_transition_grammar_terms_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "travel construct", "travel scale construct", "local travel construct", "planetary travel construct",
        "orbital travel construct", "stellar travel construct", "void travel construct", "planar travel construct",
        "dimensional travel construct", "scale transition construct", "transition precondition claim",
        "transition consequence claim", "route stability claim", "gate transition construct",
        "portal transition construct", "jump transition construct", "source-local travel construct",
        "quarantined travel construct", "escalated travel-transition problem",
    ]:
        assert phrase in lowered


def test_a14_required_exploration_grammar_terms_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "exploration construct", "exploration pressure claim", "exploration boundary claim",
        "ruin construct", "megastructure construct", "site traversal claim", "unknown-zone claim",
        "discovered-zone claim", "source-local exploration construct", "quarantined exploration construct",
        "escalated exploration contradiction",
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


def test_a14_source_local_handling_and_quarantine_escalation_language_present():
    lowered = read_utf8(A14_PATH).lower()
    for phrase in [
        "donor jump-drive systems", "teleportation systems", "ftl systems", "gate-network systems",
        "portal systems", "wilderness/hexcrawl systems", "ruin-exploration systems",
        "megastructure exploration systems", "secret-realm traversal systems", "travel-procedure systems can be retained as source-local records",
        "source-local travel, exploration, gate, portal, route, and transition terms do not become accepted lexicon terms through a14",
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


def test_registry_a14_posture_and_a15_guardrail():
    records = registry_records_by_id()
    a14 = records["A14"]
    assert a14["status"] == "draft"
    assert a14["authority_level"] == "doctrine-draft"
    assert a14["test_status"] == "designed"
    assert a14["review_status"] == "not_reviewed"
    assert a14["blocked_by"] == []

    a15 = records["A15"]
    assert a15["status"] == "todo"
    assert a15["authority_level"] == "doctrine-todo"
    assert a15["test_status"] == "not_started"
