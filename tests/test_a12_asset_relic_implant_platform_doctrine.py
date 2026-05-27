from tests.helpers import ROOT, read_utf8, registry_records_by_id

A12_PATH = ROOT / "docs" / "doctrine" / "world" / "A12_asset_relic_implant_platform_doctrine.md"


def test_a12_file_exists_at_registry_path():
    records = registry_records_by_id()
    a12 = records["A12"]
    assert a12["proposed_path"] == "docs/doctrine/world/A12_asset_relic_implant_platform_doctrine.md"
    assert A12_PATH.exists()


def test_a12_required_sections_present():
    text = read_utf8(A12_PATH)
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


def test_a12_required_asset_grammar_terms_present():
    lowered = read_utf8(A12_PATH).lower()
    for phrase in [
        "asset construct",
        "relic construct",
        "artifact construct",
        "implant construct",
        "cyberware construct",
        "biotech construct",
        "cultivation-tool construct",
        "platform asset construct",
        "starship-scale asset construct",
        "mech-scale asset construct",
        "drone/construct asset construct",
        "dimensional-anchor asset construct",
        "bonded asset construct",
        "source-local asset construct",
        "quarantined asset construct",
        "escalated asset-system problem",
    ]:
        assert phrase in lowered


def test_a12_must_not_own_boundaries_and_source_local_language_present():
    lowered = read_utf8(A12_PATH).lower()
    for phrase in [
        "specific item stats",
        "specific module lists",
        "crafting economy",
        "combat resolution",
        "runtime asset instances",
        "acquisition/licensing law",
        "attunement limits",
        "technology-level defaults",
        "compatibility math",
        "synergy bonuses",
        "upgrade trees",
        "repair/salvage/installation/crafting procedures",
        "accepted lexicon terms",
        "donor item/asset/cyberware/implant/mech/starship/licensing/attunement/technology-level systems as astra default law",
        "may be retained as source-local records",
        "do not become astra asset canon",
        "quarantined",
        "escalated",
        "do not become accepted lexicon terms through a12",
    ]:
        assert phrase in lowered


def test_a12_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A12_PATH)
    lowered = text.lower()
    for dep in [
        "A02_source_fields_magic_technology_relation.md",
        "A05_civilization_scale_and_power_scale_doctrine.md",
        "A10_resource_cost_backlash_and_corruption_doctrine.md",
        "A11_actor_ontology_and_player_grade_actor_doctrine.md",
    ]:
        assert dep in text

    for phrase in [
        "a12 does not redefine a02 source-field relation doctrine",
        "a05 scale doctrine boundaries",
        "a10 resource/cost taxonomy",
        "a11 actor ontology boundaries",
    ]:
        assert phrase in lowered


def test_registry_a12_posture_and_downstream_guardrails():
    records = registry_records_by_id()
    a12 = records["A12"]

    assert a12["status"] == "todo"
    assert a12["status"] != "current"
    assert a12["authority_level"] == "doctrine-todo"
    assert a12["test_status"] == "not_started"
    assert a12["review_status"] == "not_reviewed"
    assert a12["proposed_path"] == "docs/doctrine/world/A12_asset_relic_implant_platform_doctrine.md"

    assert records["K01"]["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"

    for idx in range(13, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
