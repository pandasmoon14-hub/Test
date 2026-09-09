import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCTRINE_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "consolidation"
    / "afqr_r2b_continuity_qualifications.md"
)


def _contract():
    text = DOCTRINE_PATH.read_text(encoding="utf-8")
    marker = "```json\n"
    start = text.index(marker) + len(marker)
    end = text.index("\n```", start)
    return json.loads(text[start:end])


def _modules():
    return {
        module["module_id"]: module
        for module in _contract()["required_modules"]
    }


def test_continuity_artifact_is_exact_and_bounded():
    assert DOCTRINE_PATH.is_file()
    contract = _contract()
    assert contract["artifact_id"] == "AFQR-R2B-CONTINUITY-QUALIFICATIONS-001"
    assert contract["artifact_version"] == "0.1.0"
    assert contract["package_id"] == "R2B-CONTINUITY"
    assert contract["workstream_id"] == "PR2-R2B-N"
    assert contract["created_semantic_owners"] == []


def test_exactly_five_required_continuity_modules_exist():
    assert set(_modules()) == {
        "R2B-CONTINUITY-MOD-TIMELINE-IDENTITY-QUALIFICATION",
        "R2B-CONTINUITY-MOD-BITEMPORAL-QUALIFICATION",
        "R2B-CONTINUITY-MOD-BRANCH-CANONICALITY-ANCESTRY",
        "R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE",
        "R2B-CONTINUITY-MOD-BRANCH-SAFE-PROJECTION",
    }


def test_timeline_identity_preserves_exact_component_owners():
    module = _modules()[
        "R2B-CONTINUITY-MOD-TIMELINE-IDENTITY-QUALIFICATION"
    ]
    assert set(module["component_owners"]) == {"AFQR-04", "AFQR-08"}
    q = module["qualification"]
    assert q["timeline_identity_must_be_stably_attributable_when_material"] is True
    assert q["timeline_identity_equals_storage_identity"] is False
    assert q["timeline_identity_confers_canonicality"] is False
    assert q["copying_proves_same_timeline"] is False
    assert q["universal_root_timeline_required"] is False
    assert q["persistence_representation_selected"] is False


def test_bitemporal_qualification_preserves_owner_separation():
    module = _modules()["R2B-CONTINUITY-MOD-BITEMPORAL-QUALIFICATION"]
    assert set(module["component_owners"]) == {
        "AFQR-01",
        "AFQR-04",
        "AFQR-06",
        "AFQR-10",
    }
    q = module["qualification"]
    assert q["world_valid_and_record_commitment_time_are_distinct_when_both_material"] is True
    assert q["decorative_second_time_dimension_required"] is False
    assert q["later_record_time_implies_later_world_valid_time"] is False
    assert q["world_valid_time_proves_truth_or_knowledge"] is False
    assert q["record_time_proves_evidence_admissibility"] is False
    assert q["revision_preserves_record_time_attribution"] is True
    assert q["time_semantics_remain_afqr_04"] is True
    assert q["evidence_admissibility_remains_afqr_06"] is True
    assert q["truth_epistemic_semantics_remain_afqr_10"] is True


def test_branch_canonicality_and_ancestry_do_not_collapse():
    module = _modules()[
        "R2B-CONTINUITY-MOD-BRANCH-CANONICALITY-ANCESTRY"
    ]
    assert set(module["component_owners"]) == {
        "AFQR-01",
        "AFQR-04",
        "AFQR-08",
        "AFQR-09",
    }
    q = module["qualification"]
    assert q["branching_requires_explicit_continuity_distinction_when_material"] is True
    assert q["snapshot_or_replay_automatically_creates_branch"] is False
    assert q["universal_branch_class_enumeration_required"] is False
    assert q["canonicality_is_explicit_and_scoped"] is True
    assert q["ancestry_confers_canonicality"] is False
    assert q["canonicality_proves_ancestry"] is False
    assert q["fork_provenance_remains_attributable"] is True
    assert q["promotion_requires_explicit_authority_bearing_change"] is True
    assert q["archive_erases_history"] is False
    assert q["universal_alternate_world_metaphysics_adopted"] is False


def test_correction_governance_preserves_history_and_component_owners():
    module = _modules()["R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE"]
    assert set(module["component_owners"]) == {
        "AFQR-01",
        "AFQR-04",
        "AFQR-09",
    }
    q = module["qualification"]
    assert q["untyped_historical_mutation_allowed"] is False
    assert q["metadata_repair_may_change_domain_semantics"] is False
    assert q["compensation_erases_prior_outcome"] is False
    assert q["supersession_erases_historical_record"] is False
    assert q["retcon_revision_preserves_original_audit_distinction"] is True
    assert q["alternate_history_creation_rewrites_original"] is False
    assert q["journal_or_storage_confers_correction_authority"] is False
    assert q["committed_audit_is_preserved"] is True
    assert q["dependency_consequences_remain_afqr_09"] is True


def test_correction_does_not_duplicate_core_or_cross_phase():
    q = _modules()[
        "R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE"
    ]["qualification"]
    assert q["randomness_identity_remains_r2b_core"] is True
    assert q["version_applicability_remains_r2b_cross_phase"] is True


def test_branch_safe_projection_preserves_truth_and_sensing_owners():
    module = _modules()["R2B-CONTINUITY-MOD-BRANCH-SAFE-PROJECTION"]
    assert set(module["component_owners"]) == {
        "AFQR-01",
        "AFQR-08",
        "AFQR-10",
        "AFQR-20",
    }
    q = module["qualification"]
    assert q["projection_requires_lawful_continuity_basis_when_branch_sensitive"] is True
    assert q["continuity_basis_grants_visibility"] is False
    assert q["projection_owns_truth"] is False
    assert q["projection_owns_sensing"] is False
    assert q["cross_branch_information_leaks_by_default"] is False
    assert q["ancestry_implies_inherited_observer_knowledge"] is False
    assert q["historical_viewpoints_must_not_be_silently_collapsed"] is True
    assert q["role_label_grants_privileged_cross_branch_access"] is False
    assert q["projection_mutates_branch"] is False


def test_r2a_excluded_modules_remain_not_adopted():
    assert set(_contract()["explicitly_not_adopted_modules"]) == {
        "R2B-CONTINUITY-MOD-RULESET-PACKAGE-OVERRIDE-VERSIONS",
        "R2B-CONTINUITY-MOD-SESSION-CLOSURE-SNAPSHOT",
    }


def test_cross_phase_and_core_nonduplication_are_explicit():
    contract = _contract()
    assert (
        contract["cross_phase_nonduplication"][
            "version_identity_effectivity_may_be_redefined_by_continuity"
        ]
        is False
    )
    assert (
        contract["cross_phase_nonduplication"]["cross_phase_artifact"]
        == "AFQR-R2B-CROSS-PHASE-VERSION-EFFECTIVITY-001"
    )
    assert (
        contract["core_nonduplication"][
            "randomness_identity_may_be_redefined_by_continuity"
        ]
        is False
    )
    assert (
        contract["core_nonduplication"]["core_artifact"]
        == "AFQR-R2B-CORE-QUALIFICATIONS-001"
    )


def test_no_runtime_or_universal_continuity_implementation_is_required():
    nonrequirements = set(_contract()["implementation_nonrequirements"])
    assert {
        "timeline_database",
        "branch_registry",
        "event_store",
        "snapshot_format",
        "replay_engine",
        "correction_service",
        "projection_api",
        "universal_timestamp_schema",
        "universal_branch_enum",
        "universal_timeline_root",
        "universal_multiverse_model",
    }.issubset(nonrequirements)


def test_prohibited_inferences_block_continuity_super_owner_and_leakage():
    prohibited = set(_contract()["prohibited_inferences"])
    assert {
        "storage_identity_is_timeline_identity",
        "timeline_identity_confers_canonicality",
        "record_time_equals_world_valid_time",
        "world_valid_time_proves_truth",
        "branch_ancestry_confers_canonicality",
        "correction_tool_confers_correction_authority",
        "retcon_may_erase_original_audit",
        "branch_selection_confers_knowledge",
        "cross_branch_information_is_visible_by_default",
        "continuity_may_duplicate_version_effectivity",
        "continuity_may_duplicate_rng_identity",
        "continuity_is_a_semantic_super_owner",
        "r2b_continuity_authorizes_runtime_or_schema_implementation",
    }.issubset(prohibited)


def test_r2c_is_only_immediate_doctrine_completion_handoff():
    contract = _contract()
    assert contract["downstream_handoffs"]["PR2-R2C"] == [
        "independent_formal_r2_completion_review"
    ]
