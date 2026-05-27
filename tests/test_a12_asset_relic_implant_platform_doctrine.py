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
        "gear construct",
        "equipment construct",
        "tool construct",
        "symbiotic asset construct",
        "living asset construct",
        "vehicle construct",
        "starship construct",
        "mech/frame construct",
        "drone asset construct",
        "construct/station asset construct",
        "artifact construct",
        "implant construct",
        "cyberware construct",
        "biotech construct",
        "cultivation tool construct",
        "platform asset construct",
        "starship-scale asset construct",
        "mech-scale asset construct",
        "drone/construct asset construct",
        "dimensional anchor construct",
        "bonded asset construct",
        "source-local asset construct",
        "quarantined asset construct",
        "escalated asset problem",
    ]:
        assert phrase in lowered


def test_a12_required_attachment_compatibility_grammar_terms_present():
    lowered = read_utf8(A12_PATH).lower()
    for phrase in [
        "carried asset claim",
        "worn asset claim",
        "wielded asset claim",
        "installed asset claim",
        "implanted asset claim",
        "bonded asset claim",
        "attunement-like claim",
        "integrated platform claim",
        "modular attachment claim",
        "upgrade-path claim",
        "compatibility claim",
        "incompatibility claim",
        "synergy claim",
        "conflict claim",
        "source-field compatibility claim",
        "actor-asset boundary claim",
        "platform-asset boundary claim",
        "source-local attachment only",
        "quarantined compatibility claim",
        "escalated compatibility contradiction",
    ]:
        assert phrase in lowered


def test_a12_required_advancement_bonding_grammar_terms_present():
    lowered = read_utf8(A12_PATH).lower()
    for phrase in [
        "asset advancement claim",
        "asset awakening claim",
        "relic evolution claim",
        "artifact maturation claim",
        "implant adaptation claim",
        "cyberware tolerance claim",
        "biotech integration claim",
        "platform advancement claim",
        "module progression claim",
        "bond formation claim",
        "bond strain claim",
        "corruption-bearing asset claim",
        "source-field-altered asset claim",
        "sacrificed asset claim",
        "repaired asset claim",
        "salvaged asset claim",
        "source-local advancement only",
        "quarantined advancement claim",
        "escalated asset advancement contradiction",
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
        "magic-item systems",
        "relic systems",
        "artifact systems",
        "cyberware systems",
        "biotech systems",
        "implant systems",
        "mech/license systems",
        "starship systems",
        "vehicle systems",
        "tool systems",
        "component systems",
        "living-asset systems",
        "cultivation-artifact systems",
        "platform-module systems",
        "may be retained as source-local records",
        "do not become astra asset canon",
        "quarantined",
        "escalated",
        "source-local asset, relic, artifact, implant, cyberware, biotech, starship, mech, vehicle, drone, station, tool, and module terms do not become accepted lexicon terms through a12",
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

    assert a12["status"] == "draft"
    assert a12["status"] != "current"
    assert a12["authority_level"] == "doctrine-draft"
    assert a12["test_status"] == "designed"
    assert a12["review_status"] == "not_reviewed"
    assert a12["proposed_path"] == "docs/doctrine/world/A12_asset_relic_implant_platform_doctrine.md"

    assert records["K01"]["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"


    a13 = records["A13"]
    assert a13["status"] == "draft"
    assert a13["authority_level"] == "doctrine-draft"
    assert a13["test_status"] == "designed"

    a14 = records["A14"]
    assert a14["status"] == "draft"
    assert a14["authority_level"] == "doctrine-draft"
    assert a14["test_status"] == "designed"
    assert a14["review_status"] == "not_reviewed"

    a15 = records["A15"]
    assert a15["status"] == "draft"
    assert a15["status"] != "current"
    assert a15["authority_level"] == "doctrine-draft"
    assert a15["test_status"] == "designed"
