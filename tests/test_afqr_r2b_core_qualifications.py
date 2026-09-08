import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTRINE_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "consolidation"
    / "afqr_r2b_core_qualifications.md"
)


def _contract():
    text = DOCTRINE_PATH.read_text(encoding="utf-8")
    marker = "```json\n"
    start = text.index(marker) + len(marker)
    end = text.index("\n```", start)
    return json.loads(text[start:end])


def _modules_by_id():
    contract = _contract()
    return {
        module["module_id"]: module
        for module in contract["modules"]
    }


def test_r2b_core_qualification_artifact_exists_and_is_bounded():
    assert DOCTRINE_PATH.is_file()
    contract = _contract()
    assert contract["artifact_id"] == "AFQR-R2B-CORE-QUALIFICATIONS-001"
    assert contract["artifact_version"] == "0.1.0"
    assert contract["package_id"] == "R2B-CORE"
    assert contract["workstream_id"] == "PR2-R2B-C"
    assert contract["replaces_r1d_core"] is False


def test_only_afqr_01_and_02_are_component_owners():
    contract = _contract()
    assert set(contract["component_owners"]) == {"AFQR-01", "AFQR-02"}
    assert contract["created_semantic_owners"] == []


def test_exactly_two_authorized_core_modules_exist():
    modules = _modules_by_id()
    assert set(modules) == {
        "R2B-CORE-MOD-PREVIEW-PERSISTENCE-PROMOTION",
        "R2B-CORE-MOD-CORRECTION-RNG-IDENTITY",
    }


def test_preview_persistence_never_confers_authority():
    q = _modules_by_id()[
        "R2B-CORE-MOD-PREVIEW-PERSISTENCE-PROMOTION"
    ]["qualification"]
    assert q["retained_preview_status"] == "proposal"
    assert q["persistence_authority_effect"] == "none"
    assert q["persistence_confers_commitment"] is False
    assert q["persistence_confers_canonicality"] is False
    assert q["persistence_confers_branch_status"] is False


def test_preview_promotion_requires_separately_governed_transition():
    q = _modules_by_id()[
        "R2B-CORE-MOD-PREVIEW-PERSISTENCE-PROMOTION"
    ]["qualification"]
    assert q["promotion_requires_explicit_lawful_transition"] is True
    assert q["promotion_target_requires_separate_governance"] is True
    assert q["promotion_retroactively_commits_preview"] is False
    assert q["branch_classification_defined_here"] is False


def test_replay_recovery_and_retry_cannot_become_rerolls():
    q = _modules_by_id()[
        "R2B-CORE-MOD-CORRECTION-RNG-IDENTITY"
    ]["qualification"]
    assert q["original_committed_audit_preserved"] is True
    assert q["replay_or_recovery_may_generate_replacement_outcome"] is False
    assert q["technical_retry_may_reroll"] is False


def test_correction_replacement_resolution_is_distinguishable():
    q = _modules_by_id()[
        "R2B-CORE-MOD-CORRECTION-RNG-IDENTITY"
    ]["qualification"]
    assert (
        q[
            "authorized_correction_new_resolution_requires_distinguishable_replacement_execution"
        ]
        is True
    )
    assert q["replacement_randomness_provenance_separately_attributable"] is True
    assert q["command_attempt_classification_remains_afqr_02"] is True


def test_randomness_qualification_is_mechanism_neutral():
    rng_module = _modules_by_id()[
        "R2B-CORE-MOD-CORRECTION-RNG-IDENTITY"
    ]
    q = rng_module["qualification"]
    expected = {
        "dice",
        "cards",
        "bags",
        "oracle_draws",
        "random_tables",
        "encounter_tables",
        "pseudo_random_generators",
        "deterministic_source_local_uncertainty_procedures",
        "external_randomized_mechanisms",
        "mixed_deterministic_random_resolution",
    }
    assert set(rng_module["randomness_pressure_families"]) == expected
    assert q["deterministic_procedures_require_randomness"] is False
    assert q["universal_rng_implementation_mandated"] is False


def test_downstream_handoffs_remain_separate():
    contract = _contract()
    assert set(contract["handoffs"]) == {
        "R2B-CONTINUITY",
        "R2B-CROSS-PHASE",
        "later_implementation",
    }
    assert "branch_canonicality_class_ancestry" in (
        contract["handoffs"]["R2B-CONTINUITY"]
    )
    assert "correction_compensation_retcon_supersession" in (
        contract["handoffs"]["R2B-CONTINUITY"]
    )
    assert "version_identity" in contract["handoffs"]["R2B-CROSS-PHASE"]
    assert "production_schema" in contract["handoffs"]["later_implementation"]
