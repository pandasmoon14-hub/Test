from tests.helpers import ROOT, read_utf8, registry_records_by_id

A11_PATH = ROOT / "docs" / "doctrine" / "world" / "A11_actor_ontology_and_player_grade_actor_doctrine.md"


def test_a11_file_exists_at_registry_path():
    records = registry_records_by_id()
    a11 = records["A11"]
    assert a11["proposed_path"] == "docs/doctrine/world/A11_actor_ontology_and_player_grade_actor_doctrine.md"
    assert A11_PATH.exists()


def test_a11_required_sections_present():
    text = read_utf8(A11_PATH)
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


def test_a11_required_actor_ontology_grammar_terms_present():
    lowered = read_utf8(A11_PATH).lower()
    for phrase in [
        "actor construct",
        "player-grade actor construct",
        "non-player actor construct",
        "companion actor construct",
        "summon actor construct",
        "factional actor construct",
        "macro-actor construct",
        "ai/digital actor construct",
        "drone/remote actor construct",
        "spirit/immaterial actor construct",
        "platform-embedded actor construct",
        "transformed actor state construct",
        "persistent actor continuity construct",
        "source-local actor construct",
        "quarantined actor construct",
        "escalated actor-ontology problem",
    ]:
        assert phrase in lowered


def test_a11_must_not_own_boundaries_and_source_local_language_present():
    lowered = read_utf8(A11_PATH).lower()
    for phrase in [
        "specific statblocks",
        "resource pool mechanics",
        "faction reputation systems",
        "specific creature/species/ancestry lists",
        "fixed ancestry/culture/background bonuses",
        "donor attribute modifiers",
        "donor skill grants",
        "lifepath tables or career packages",
        "homeworld benefits",
        "full setting history",
        "runtime actor identity state",
        "runtime actor progression state",
        "runtime hidden-information state",
        "accepted lexicon terms",
        "donor race/species/culture/background/lifepath systems as astra default law",
        "may be retained as source-local records",
        "do not become astra actor canon",
        "quarantined",
        "escalated",
        "do not become accepted lexicon terms through a11",
    ]:
        assert phrase in lowered


def test_a11_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A11_PATH)
    lowered = text.lower()
    for dep in [
        "A03_soul_body_mind_spirit_ontology.md",
        "A05_civilization_scale_and_power_scale_doctrine.md",
        "A06_cultivation_and_ascension_stage_architecture.md",
        "A07_advancement_axes_and_progression_pressure.md",
        "A08_path_domain_and_technique_mastery_doctrine.md",
        "A10_resource_cost_backlash_and_corruption_doctrine.md",
    ]:
        assert dep in text

    for phrase in [
        "a11 does not redefine a03 ontology boundaries",
        "a05 scale doctrine boundaries",
        "a06 stage taxonomy",
        "a07 advancement axes",
        "a08 path/technique mastery",
        "a10 resource/cost taxonomy",
    ]:
        assert phrase in lowered


def test_registry_a11_posture_and_downstream_guardrails():
    records = registry_records_by_id()
    a11 = records["A11"]

    assert a11["status"] == "draft"
    assert a11["status"] != "current"
    assert a11["authority_level"] == "doctrine-draft"
    assert a11["test_status"] == "designed"
    assert a11["review_status"] == "not_reviewed"
    assert a11["proposed_path"] == "docs/doctrine/world/A11_actor_ontology_and_player_grade_actor_doctrine.md"

    assert records["K01"]["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"

    a12 = records["A12"]
    assert a12["status"] == "draft"
    assert a12["authority_level"] == "doctrine-draft"
    assert a12["test_status"] == "designed"


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
