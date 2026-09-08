import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTRINE_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "consolidation"
    / "afqr_r2b_cross_phase_version_identity_effectivity.md"
)


def _contract():
    text = DOCTRINE_PATH.read_text(encoding="utf-8")
    marker = "```json\n"
    start = text.index(marker) + len(marker)
    end = text.index("\n```", start)
    return json.loads(text[start:end])


def test_cross_phase_artifact_exists_and_is_single_module():
    assert DOCTRINE_PATH.is_file()
    contract = _contract()
    assert contract["artifact_id"] == "AFQR-R2B-CROSS-PHASE-VERSION-EFFECTIVITY-001"
    assert contract["artifact_version"] == "0.1.0"
    assert contract["package_id"] == "R2B-CROSS-PHASE"
    assert contract["workstream_id"] == "PR2-R2B-X"
    assert contract["module_id"] == "R2B-CROSS-PHASE-MOD-VERSION-IDENTITY-EFFECTIVITY"


def test_component_owners_remain_exact_and_separate():
    contract = _contract()
    assert set(contract["component_owners"]) == {
        "AFQR-01",
        "AFQR-02",
        "AFQR-04",
        "AFQR-09",
        "AFQR-19",
    }
    assert contract["created_semantic_owners"] == []


def test_version_dimensions_remain_distinguishable():
    contract = _contract()
    assert set(contract["version_dimensions"]) == {
        "ruleset_version_identity",
        "content_package_version_identity",
        "campaign_override_version_identity",
        "related_schema_version_identity",
    }
    assert contract["qualifications"]["version_dimensions_remain_distinct"] is True


def test_applicability_is_explicit_and_latest_is_not_authority():
    q = _contract()["qualifications"]
    assert q["version_identity_confers_applicability"] is False
    assert q["version_identity_confers_canon"] is False
    assert q["latest_alias_is_historical_pin"] is False
    assert q["current_applicability_must_be_explicit"] is True


def test_historical_basis_is_attributable_and_does_not_refresh():
    contract = _contract()
    q = contract["qualifications"]
    assert q["historical_execution_basis_must_be_attributable"] is True
    assert q["technical_retry_may_refresh_version_basis"] is False
    assert q["replay_or_recovery_may_substitute_current_version"] is False
    assert q["missing_historical_version_allows_silent_substitution"] is False
    assert "concrete revision actually used" in contract["historical_resolution_requirement"]


def test_effective_intervals_preserve_afqr_04_time_ownership():
    q = _contract()["qualifications"]
    assert q["effective_interval_requires_declared_time_basis"] is True
    assert q["effective_interval_time_semantics_owner"] == "AFQR-04"
    assert q["overlap_creates_implicit_precedence"] is False


def test_override_package_and_schema_identity_do_not_gain_authority():
    q = _contract()["qualifications"]
    assert q["override_identity_confers_override_authority"] is False
    assert q["package_identity_confers_distribution_eligibility"] is False
    assert q["schema_version_confers_domain_semantics"] is False
    assert q["supersession_rewrites_historical_applicability"] is False


def test_existing_component_semantics_remain_with_existing_owners():
    q = _contract()["qualifications"]
    assert q["dependency_consequences_remain_afqr_09"] is True
    assert q["procedure_semantics_remain_afqr_19"] is True
    assert q["command_identity_remains_afqr_02"] is True
    assert q["commitment_remains_afqr_01"] is True


def test_continuity_cannot_duplicate_version_effectivity():
    contract = _contract()
    assert contract["qualifications"]["continuity_may_duplicate_version_effectivity_seam"] is False
    assert "R2B-CONTINUITY" in contract["handoffs"]


def test_no_versioning_or_runtime_implementation_is_mandated():
    nonrequirements = set(_contract()["implementation_nonrequirements"])
    assert {
        "semantic_versioning",
        "global_version_counter",
        "package_manager",
        "dependency_solver",
        "database",
        "migration_engine",
        "runtime_version_field",
        "universal_override_stack",
    }.issubset(nonrequirements)


def test_prohibited_inferences_block_implicit_precedence_and_super_owner():
    prohibited = set(_contract()["prohibited_inferences"])
    assert {
        "latest_wins",
        "installed_means_applicable",
        "load_order_creates_semantic_precedence",
        "cross_phase_is_a_semantic_super_owner",
        "continuity_may_redefine_version_effectivity",
        "r2b_cross_phase_authorizes_runtime_or_schema_implementation",
    }.issubset(prohibited)
