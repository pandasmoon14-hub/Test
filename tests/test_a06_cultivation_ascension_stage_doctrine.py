from tests.helpers import ROOT, read_utf8, registry_records_by_id

A06_PATH = ROOT / "docs" / "doctrine" / "advancement" / "A06_cultivation_and_ascension_stage_architecture.md"


def test_a06_required_sections_present():
    text = read_utf8(A06_PATH)
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


def test_a06_required_stage_taxonomy_grammar_terms_present():
    text = read_utf8(A06_PATH).lower()
    for phrase in [
        "stage construct",
        "rank construct",
        "tier construct",
        "grade construct",
        "realm construct",
        "threshold construct",
        "breakthrough construct",
        "bottleneck construct",
        "tribulation construct",
        "ascension construct",
        "evolution construct",
        "initiation construct",
        "milestone construct",
        "source-local stage construct",
        "quarantined stage construct",
        "escalated stage problem",
    ]:
        assert phrase in text


def test_a06_required_transition_permission_grammar_terms_present():
    text = read_utf8(A06_PATH).lower()
    for phrase in [
        "permitted transition",
        "blocked transition",
        "conditional transition",
        "partial transition",
        "failed transition",
        "regressive transition",
        "lateral transition",
        "staged transition",
        "delayed transition",
        "unstable transition",
        "source-local transition only",
        "quarantined transition",
        "escalated transition contradiction",
    ]:
        assert phrase in text


def test_a06_required_breakthrough_bottleneck_tribulation_grammar_terms_present():
    text = read_utf8(A06_PATH).lower()
    for phrase in [
        "readiness gate",
        "knowledge gate",
        "body gate",
        "soul/mind/spirit gate",
        "source-field gate",
        "domain/concept gate",
        "scale gate",
        "social/institutional gate",
        "asset/tool gate",
        "environmental gate",
        "voluntary trial",
        "involuntary tribulation",
        "externalized tribulation",
        "internalized tribulation",
        "symbolic tribulation",
        "consequence-bearing failure",
        "source-local gate only",
        "quarantined gate/tribulation",
        "escalated gate contradiction",
    ]:
        assert phrase in text


def test_a06_must_not_own_boundaries_and_source_local_handling_present():
    text = read_utf8(A06_PATH).lower()
    for phrase in [
        "specific techniques",
        "class features",
        "specific stat bonuses",
        "resource pool numbers",
        "donor stage names",
        "fixed level tables",
        "xp/leveling math",
        "runtime advancement state",
        "hidden information state",
        "accepted lexicon terms",
        "donor progression ladders as astra default law",
        "donor stage/realm/tier/level systems can be retained as source-local records",
        "source-local records preserve donor provenance but do not become astra advancement canon",
        "repeated donor pressure can produce canon candidates only through later k-layer/canon review",
        "unclassifiable advancement systems are quarantined or escalated, not normalized by invention",
        "donor proper nouns remain source-local unless canon promotion accepts them later",
        "source-local stage terms do not become accepted lexicon terms through a06",
        "quarantined",
        "escalated",
    ]:
        assert phrase in text


def test_a06_dependencies_and_non_redefinition_posture_present():
    text = read_utf8(A06_PATH)
    lowered = text.lower()

    for dep in [
        "A01_cosmology_and_dimensional_architecture.md",
        "A02_source_fields_magic_technology_relation.md",
        "A03_soul_body_mind_spirit_ontology.md",
        "A04_dao_domain_element_architecture.md",
        "A05_civilization_scale_and_power_scale_doctrine.md",
    ]:
        assert dep in text

    for forbidden in [
        "a06 defines worlds",
        "a06 defines planes",
        "a06 defines source fields",
        "a06 defines identity continuity",
        "a06 defines dao/domain/element rules",
        "a06 defines scale taxonomy",
        "a06 defines resource systems",
        "a06 defines actor stats",
        "a06 defines runtime state",
        "a06 defines hidden-information behavior",
    ]:
        assert forbidden not in lowered


def test_registry_a06_posture_and_a07_a08_draft_only_promotions():
    records = registry_records_by_id()

    a01 = records["A01"]
    a02 = records["A02"]
    a03 = records["A03"]
    a04 = records["A04"]
    a05 = records["A05"]
    a06 = records["A06"]
    k01 = records["K01"]

    assert a06["status"] == "draft"
    assert a06["status"] != "current"
    assert a06["authority_level"] == "doctrine-draft"
    assert a06["test_status"] == "designed"
    assert a06["review_status"] == "not_reviewed"
    assert a06["proposed_path"] == "docs/doctrine/advancement/A06_cultivation_and_ascension_stage_architecture.md"
    assert a06["dependencies"] == ["A01", "A02", "A03", "A04", "A05"]
    assert a06["blocked_by"] == []

    for rec in (a01, a02, a03, a04, a05):
        assert rec["status"] in {"draft", "review", "pressure-tested", "todo", "blocked", "deprecated"}
        assert rec["status"] != "current"

    assert k01["proposed_path"] == "docs/doctrine/canon/K01_lexicon_governance_and_reserved_terms.md"
    assert a06["filename"] != k01["filename"]

    a07 = records["A07"]
    assert a07["status"] == "draft"
    assert a07["authority_level"] == "doctrine-draft"
    assert a07["test_status"] == "designed"
    assert a07["review_status"] == "not_reviewed"
    assert a07["proposed_path"] == "docs/doctrine/advancement/A07_advancement_axes_and_progression_pressure.md"

    a08 = records["A08"]
    assert a08["status"] == "draft"
    assert a08["authority_level"] == "doctrine-draft"
    assert a08["test_status"] == "designed"
    assert a08["review_status"] == "not_reviewed"
    assert a08["proposed_path"] == "docs/doctrine/advancement/A08_path_domain_and_technique_mastery_doctrine.md"

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

    for idx in range(13, 16):
        rec = records[f"A{idx:02d}"]
        assert rec["status"] == "todo"
        assert rec["authority_level"] == "doctrine-todo"
        assert rec["test_status"] == "not_started"
