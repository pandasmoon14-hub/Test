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


def test_a13_required_conflict_damage_hazard_grammar_terms_present():
    lowered = read_utf8(A13_PATH).lower()
    for phrase in [
        "conflict construct",
        "engagement construct",
        "confrontation construct",
        "duel-scale conflict construct",
        "squad-scale conflict construct",
        "vehicle-scale conflict construct",
        "ship-scale conflict construct",
        "fleet-scale conflict construct",
        "army-scale conflict construct",
        "planar-scale conflict construct",
        "social conflict construct",
        "psychic conflict construct",
        "environmental conflict construct",
        "damage family claim",
        "damage channel claim",
        "mitigated damage claim",
        "resisted damage claim",
        "immunity claim",
        "vulnerability claim",
        "compound effect claim",
        "injury consequence claim",
        "death consequence claim",
        "recovery consequence claim",
        "transformation consequence claim",
        "hazard construct",
        "ambient hazard construct",
        "environmental hazard construct",
        "technological hazard construct",
        "magical hazard construct",
        "cultivation hazard construct",
        "mixed-source hazard construct",
        "persistent hazard claim",
        "transient hazard claim",
        "regional hazard claim",
        "cross-scale hazard claim",
    ]:
        assert phrase in lowered


def test_a13_must_not_own_boundaries_and_source_local_language_present():
    lowered = read_utf8(A13_PATH).lower()
    for phrase in [
        "specific conflict math",
        "combat math formulas",
        "specific statblocks",
        "encounter procedure",
        "initiative procedure",
        "action economy",
        "resource pools",
        "injury tables",
        "death rules",
        "recovery rules",
        "healing rules",
        "condition/status rules",
        "exact damage numbers",
        "resistance/immunity math",
        "hazard procedures",
        "faction warfare details",
        "runtime conflict state",
        "runtime injury state",
        "runtime hazard state",
        "runtime hidden-information state",
        "runtime event commits",
        "accepted lexicon terms",
        "donor armor/health/damage/stress/structure/drain/initiative/vehicle/ship/fleet/hazard/injury/recovery systems as astra default law",
        "may be retained as source-local records",
        "do not become astra conflict canon",
        "quarantined",
        "escalated",
        "do not become accepted lexicon terms through a13",
    ]:
        assert phrase in lowered


def test_a13_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A13_PATH)
    lowered = text.lower()
    for dep in [
        "A05_civilization_scale_and_power_scale_doctrine.md",
        "A08_path_domain_and_technique_mastery_doctrine.md",
        "A10_resource_cost_backlash_and_corruption_doctrine.md",
        "A11_actor_ontology_and_player_grade_actor_doctrine.md",
        "A12_asset_relic_implant_platform_doctrine.md",
    ]:
        assert dep in text

    for phrase in [
        "a13 does not redefine a05 scale doctrine boundaries",
        "a08 path/technique mastery boundaries",
        "a10 resource/cost taxonomy",
        "a11 actor ontology boundaries",
        "a12 asset taxonomy boundaries",
    ]:
        assert phrase in lowered


def test_registry_a13_posture_and_downstream_guardrails():
    records = registry_records_by_id()
    a13 = records["A13"]

    assert a13["status"] == "draft"
    assert a13["status"] != "current"
    assert a13["authority_level"] == "doctrine-draft"
    assert a13["test_status"] == "designed"
    assert a13["review_status"] == "not_reviewed"
    assert a13["proposed_path"] == "docs/doctrine/world/A13_combat_hazard_damage_and_consequence_doctrine.md"

    for idx in range(14, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
