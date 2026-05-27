from tests.helpers import ROOT, read_utf8, registry_records_by_id

A07_PATH = ROOT / "docs" / "doctrine" / "advancement" / "A07_advancement_axes_and_progression_pressure.md"


def test_a07_file_exists():
    assert A07_PATH.exists()


def test_a07_required_sections_present():
    text = read_utf8(A07_PATH)
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


def test_a07_required_advancement_axis_taxonomy_grammar_terms_present():
    text = read_utf8(A07_PATH).lower()
    for phrase in [
        "body axis",
        "soul axis",
        "mind axis",
        "spirit axis",
        "path axis",
        "domain axis",
        "technique axis",
        "skill/competency axis",
        "social/institutional axis",
        "asset/equipment/platform axis",
        "companion/familiar/summon axis",
        "faction/reputation/standing axis",
        "narrative/milestone axis",
        "source-local advancement axis",
        "quarantined advancement axis",
        "escalated advancement-axis problem",
    ]:
        assert phrase in text


def test_a07_required_cross_axis_interaction_grammar_terms_present():
    text = read_utf8(A07_PATH).lower()
    for phrase in [
        "independent axis",
        "dependent axis",
        "prerequisite axis",
        "reinforcing axis",
        "conflicting axis",
        "parasitic axis",
        "capped axis",
        "overloaded axis",
        "synergistic interaction",
        "interfering interaction",
        "diminishing returns pressure",
        "compounding pressure",
        "advancement load",
        "advancement strain",
        "source-local axis interaction only",
        "quarantined axis interaction",
        "escalated axis contradiction",
    ]:
        assert phrase in text


def test_a07_required_progression_pressure_grammar_terms_present():
    text = read_utf8(A07_PATH).lower()
    for phrase in [
        "balanced progression pressure",
        "skewed progression pressure",
        "overconcentrated progression pressure",
        "underdeveloped-axis pressure",
        "social/institutional pressure",
        "asset-maintenance pressure",
        "companion-growth pressure",
        "faction-standing pressure",
        "scale-pressure interaction",
        "stage-pressure interaction",
        "source-local pressure only",
        "quarantined pressure",
        "escalated pressure contradiction",
    ]:
        assert phrase in text


def test_a07_must_not_own_boundaries_and_source_local_handling_present():
    text = read_utf8(A07_PATH).lower()
    for phrase in [
        "specific skill lists",
        "specific faction ranks",
        "specific point-buy costs",
        "specific karma costs",
        "specific license ranks",
        "specific class features",
        "specific stat bonuses",
        "resource pool numbers",
        "fixed xp tables",
        "fixed level tables",
        "runtime progression state",
        "hidden information state",
        "accepted lexicon terms",
        "donor advancement systems as astra default law",
        "donor advancement-axis systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra advancement-axis canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable advancement-axis systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local axis terms do not become accepted lexicon terms through a07",
        "quarantined",
        "escalated",
    ]:
        assert phrase in text


def test_a07_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A07_PATH)
    lowered = text.lower()

    assert "A05_civilization_scale_and_power_scale_doctrine.md" in text
    assert "A06_cultivation_and_ascension_stage_architecture.md" in text

    for forbidden in [
        "a07 defines scale taxonomy",
        "a07 defines stage taxonomy",
        "a07 defines breakthrough/tribulation rules",
        "a07 defines resource systems",
        "a07 defines class systems",
        "a07 defines technique mastery",
        "a07 defines actor stats",
        "a07 defines runtime progression state",
        "a07 defines event commits",
        "a07 defines hidden-information behavior",
    ]:
        assert forbidden not in lowered


def test_registry_a07_posture_and_a08_draft_only_promotion():
    records = registry_records_by_id()

    a05 = records["A05"]
    a06 = records["A06"]
    a07 = records["A07"]
    k01 = records["K01"]

    assert a07["status"] == "draft"
    assert a07["status"] != "current"
    assert a07["authority_level"] == "doctrine-draft"
    assert a07["test_status"] == "designed"
    assert a07["review_status"] == "not_reviewed"
    assert a07["proposed_path"] == "docs/doctrine/advancement/A07_advancement_axes_and_progression_pressure.md"
    assert a07["dependencies"] == ["A05", "A06"]
    assert a07["file_id"] == "A07"
    assert a07["filename"] == "A07_advancement_axes_and_progression_pressure.md"
    assert a07["layer"] == "2_advancement_action_spine"
    assert a07["phase"] == "1B"
    assert a07["blocked_by"] == []

    for rec in (a05, a06):
        assert rec["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
        assert rec["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a07["filename"] != k01["filename"]

    a08 = records["A08"]
    assert a08["status"] == "draft"
    assert a08["authority_level"] == "doctrine-draft"
    assert a08["test_status"] == "designed"

    a09 = records["A09"]
    assert a09["status"] == "draft"
    assert a09["authority_level"] == "doctrine-draft"
    assert a09["test_status"] == "designed"

    a10 = records["A10"]
    assert a10["status"] == "draft"
    assert a10["authority_level"] == "doctrine-draft"
    assert a10["test_status"] == "designed"

    a11 = records["A11"]
    assert a11["status"] == "draft"
    assert a11["authority_level"] == "doctrine-draft"
    assert a11["test_status"] == "designed"


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
    assert a15["status"] == "todo"
    assert a15["authority_level"] == "doctrine-todo"
    assert a15["test_status"] == "not_started"
