from tests.helpers import ROOT, read_utf8, registry_records_by_id

A08_PATH = ROOT / "docs" / "doctrine" / "advancement" / "A08_path_domain_and_technique_mastery_doctrine.md"


def test_a08_file_exists():
    assert A08_PATH.exists()


def test_a08_required_sections_present():
    text = read_utf8(A08_PATH)
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


def test_a08_required_grammar_terms_present():
    text = read_utf8(A08_PATH).lower()
    for phrase in [
        "path construct",
        "domain construct",
        "technique construct",
        "spell-like construct",
        "power-like construct",
        "art-like construct",
        "maneuver-like construct",
        "ritual-like construct",
        "system/module-like construct",
        "charm/tree-like construct",
        "discipline-like construct",
        "source-local technique construct",
        "quarantined technique construct",
        "escalated technique problem",
        "passive expression",
        "active expression",
        "triggered expression",
        "sustained expression",
        "prepared expression",
        "channeled expression",
        "reactive expression",
        "ritual expression",
        "self-targeted expression",
        "single-target expression",
        "area expression",
        "zone expression",
        "aura expression",
        "line/cone/burst-like expression",
        "environmental expression",
        "source-local expression only",
        "quarantined expression",
        "escalated expression contradiction",
        "known technique",
        "practiced technique",
        "mastered technique",
        "evolving technique",
        "incomplete technique",
        "forbidden technique",
        "inherited technique",
        "researched technique",
        "improvised technique",
        "synthesized technique",
        "incompatible synthesis",
        "constrained synthesis",
        "unstable synthesis",
        "path-locked technique",
        "domain-gated technique",
        "permission-gated learning",
        "research-gated learning",
        "source-local mastery only",
        "quarantined mastery claim",
        "escalated mastery contradiction",
    ]:
        assert phrase in text


def test_a08_must_not_own_boundaries_and_source_local_language_present():
    text = read_utf8(A08_PATH).lower()
    for phrase in [
        "specific technique stats",
        "specific spell lists",
        "specific power lists",
        "specific maneuver lists",
        "specific resource pool mechanics",
        "exact resource costs",
        "recharge/backlash mechanics",
        "exact action economy",
        "exact ranges",
        "exact target counts",
        "exact damage formulas",
        "damage family rules",
        "condition/status rules",
        "actor stat blocks",
        "fixed mastery bonuses",
        "fixed path switching costs",
        "runtime ability state",
        "runtime progression state",
        "runtime event commits",
        "hidden information state",
        "accepted lexicon terms",
        "donor spell/power/technique systems as astra default law",
        "donor spell/power/art/maneuver/technique systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra technique canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable technique systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local spell/power/technique terms do not become accepted lexicon terms through a08",
        "quarantined",
        "escalated",
    ]:
        assert phrase in text


def test_a08_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A08_PATH)
    lowered = text.lower()

    assert "A04_dao_domain_element_architecture.md" in text
    assert "A06_cultivation_and_ascension_stage_architecture.md" in text
    assert "A07_advancement_axes_and_progression_pressure.md" in text

    for phrase in [
        "a08 does not redefine a04 domain taxonomy",
        "a06 stage taxonomy",
        "a07 advancement-axis taxonomy",
        "resource systems",
        "damage families",
        "condition/status rules",
        "actor stats",
        "runtime ability state",
        "runtime progression state",
        "runtime event commits",
        "hidden-information behavior",
    ]:
        assert phrase in lowered


def test_registry_a08_posture_and_downstream_not_promoted():
    records = registry_records_by_id()

    a04 = records["A04"]
    a06 = records["A06"]
    a07 = records["A07"]
    a08 = records["A08"]
    k01 = records["K01"]

    assert a08["status"] == "draft"
    assert a08["status"] != "current"
    assert a08["authority_level"] == "doctrine-draft"
    assert a08["test_status"] == "designed"
    assert a08["review_status"] == "not_reviewed"
    assert a08["proposed_path"] == "docs/doctrine/advancement/A08_path_domain_and_technique_mastery_doctrine.md"
    assert a08["dependencies"] == ["A04", "A06", "A07"]

    for rec in (a04, a06, a07):
        assert rec["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
        assert rec["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a08["filename"] != k01["filename"]

    a09 = records["A09"]
    assert a09["status"] == "draft"
    assert a09["authority_level"] == "doctrine-draft"
    assert a09["test_status"] == "designed"

    a10 = records["A10"]
    assert a10["status"] == "draft"
    assert a10["authority_level"] == "doctrine-draft"
    assert a10["test_status"] == "designed"

    for idx in range(11, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
