from tests.helpers import ROOT, read_utf8, registry_records_by_id

A13_PATH = ROOT / "docs" / "doctrine" / "world" / "A13_combat_hazard_damage_and_consequence_doctrine.md"


def test_a13_file_exists_at_registry_path():
    records = registry_records_by_id()
    a13 = records["A13"]
    assert a13["proposed_path"] == "docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md"
    assert A13_PATH.exists()


def test_a13_required_sections_present():
    text = read_utf8(A13_PATH)
    for heading in [
        "## 1. Purpose and status", "## 2. What this file owns", "## 3. What this file must not own",
        "## 4. Required definitions", "## 5. Core doctrine rules", "## 6. Conversion mapping rules",
        "## 7. Source-local handling", "## 8. Donor pressure absorbed", "## 9. Hard refusals / rejected imports",
        "## 10. Escalation triggers", "## 11. Dependencies", "## 12. Handoff to downstream layers",
        "## 13. Test cases / pressure examples", "## 14. Versioning and review protocol",
    ]:
        assert heading in text


def test_a13_required_conflict_scale_grammar_terms_present():
    lowered = read_utf8(A13_PATH).lower()
    for phrase in [
        "conflict construct", "conflict scale construct", "personal-scale conflict construct", "group-scale conflict construct",
        "vehicle-scale conflict construct", "ship-scale conflict construct", "fleet-scale conflict construct",
        "army-scale conflict construct", "planar-scale conflict construct", "psychic conflict construct",
        "social conflict construct", "cosmic conflict construct", "environmental conflict construct", "hazard construct",
        "source-local conflict construct", "quarantined conflict construct", "escalated conflict-scale problem",
    ]:
        assert phrase in lowered


def test_a13_required_damage_and_interaction_grammar_terms_present():
    lowered = read_utf8(A13_PATH).lower()
    for phrase in [
        "damage family construct", "harm-type claim", "impact claim", "stress claim", "structural damage claim",
        "spiritual damage claim", "psychic damage claim", "environmental damage claim", "social consequence claim",
        "corruption consequence claim", "resistance claim", "immunity claim", "vulnerability claim", "reduction claim",
        "amplification claim", "compound interaction claim", "fused interaction claim", "cascading consequence claim",
        "source-field interaction claim", "dao interaction claim", "source-local damage only",
        "quarantined damage interaction", "escalated damage-family contradiction",
    ]:
        assert phrase in lowered


def test_a13_required_consequence_grammar_terms_present():
    lowered = read_utf8(A13_PATH).lower()
    for phrase in [
        "consequence construct", "injury consequence claim", "death consequence claim", "recovery consequence claim",
        "healing consequence claim", "transformation consequence claim", "trauma consequence claim",
        "degradation consequence claim", "overload consequence claim", "collateral consequence claim",
        "scale spillover claim", "persistent consequence claim", "reversible consequence claim",
        "irreversible consequence claim", "source-local consequence only", "quarantined consequence claim",
        "escalated consequence contradiction",
    ]:
        assert phrase in lowered


def test_a13_must_not_own_boundaries_present():
    lowered = read_utf8(A13_PATH).lower()
    for phrase in [
        "specific conflict math", "combat math formulas", "specific statblocks", "encounter procedure",
        "initiative procedure", "action economy", "resource pools", "injury tables", "death rules",
        "recovery rules", "healing rules", "condition/status rules", "exact damage numbers",
        "resistance/immunity math", "hazard procedures", "faction warfare details", "runtime conflict state",
        "runtime injury state", "runtime hazard state", "runtime hidden-information state", "runtime event commits",
    ]:
        assert phrase in lowered


def test_a13_source_local_handling_and_quarantine_escalation_language_present():
    lowered = read_utf8(A13_PATH).lower()
    for phrase in [
        "donor armor/health/damage-type systems", "stress/structure systems", "drain/initiative systems",
        "vehicle/ship conflict systems", "fleet/mass-conflict systems", "hazard systems", "injury systems",
        "death systems", "recovery systems", "consequence systems can be retained as source-local records",
        "source-local conflict, hazard, damage, resistance, consequence, injury, recovery, and scale terms do not become accepted lexicon terms through a13",
        "quarantined", "escalated",
    ]:
        assert phrase in lowered


def test_a13_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A13_PATH)
    lowered = text.lower()
    for dep in [
        "A05_civilization_scale_and_power_scale_doctrine.md", "A08_path_domain_and_technique_mastery_doctrine.md",
        "A10_resource_cost_backlash_and_corruption_doctrine.md", "A11_actor_ontology_and_player_grade_actor_doctrine.md",
        "A12_asset_relic_implant_platform_doctrine.md",
    ]:
        assert dep in text
    for phrase in [
        "a13 does not redefine a05 scale doctrine boundaries", "a08 path/technique mastery boundaries",
        "a10 resource/cost taxonomy", "a11 actor ontology boundaries", "a12 asset taxonomy boundaries",
    ]:
        assert phrase in lowered


def test_registry_a13_posture_k01_separation_and_downstream_guardrails():
    records = registry_records_by_id()
    a13 = records["A13"]
    assert a13["status"] == "draft"
    assert a13["authority_level"] == "doctrine-draft"
    assert a13["test_status"] == "designed"
    assert a13["review_status"] == "not_reviewed"
    assert records["K01"]["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    a14 = records["A14"]
    assert a14["status"] == "draft"
    assert a14["authority_level"] == "doctrine-draft"
    assert a14["test_status"] == "designed"

    a15 = records["A15"]
    assert a15["status"] == "todo"
    assert a15["authority_level"] == "doctrine-todo"
    assert a15["test_status"] == "not_started"
