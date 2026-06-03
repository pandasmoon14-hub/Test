from tests.helpers import ROOT, read_utf8

B07_PATH = (
    ROOT
    / "docs"
    / "doctrine"
    / "operations"
    / "batch_b"
    / "B07_recovery_training_research_and_preparation_project_procedure.md"
)

REQUIRED_SECTIONS = [
    "## 1. Purpose and status",
    "## 2. Owner layer",
    "## 3. What B07 owns",
    "## 4. What B07 must not own",
    "## 5. Non-collapse rule",
    "## 6. Recovery, training, research, preparation, readiness, proof, and output definitions",
    "## 7. Recovery/training/research/preparation project intake procedure",
    "## 8. Family and scope classification",
    "## 9. Requirement discovery and protected-hidden handling",
    "## 10. Cost/risk preview and commitment procedure",
    "## 11. Interval setup, progress trigger, and owner-routing procedure",
    "## 12. Recovery project procedure",
    "## 13. Training project procedure",
    "## 14. Teacher, mentor, institution, archive, simulation, and source-local authority procedure",
    "## 15. Research, experimentation, reverse-engineering, and desired-outcome procedure",
    "## 16. Prototype, method-seed, lawful-action-vector, and dangerous-temptation routing",
    "## 17. Preparation, readiness, rehearsal, staging, and risk-reduction procedure",
    "## 18. Proof, advancement, route, technique, expression, and breakthrough handoff rules",
    "## 19. Progress, partial completion, complication, failure, interruption, and abandonment routing",
    "## 20. Output, state-delta, hidden-state, and owner-file handoff rules",
    "## 21. Batch B to C00/C-family handoff rules",
    "## 22. Missing-schema fallback and quarantine/escalation",
    "## 23. Source-local donor recovery/training/research/preparation handling",
    "## 24. Runtime boundary",
    "## 25. Canon boundary",
    "## 26. Live-play/training boundary",
    "## 27. Examples of good and bad B07 usage",
    "## 28. Minimum tests or assertions",
    "## 29. Acceptance criteria",
    "## 30. Follow-up handoff to B08",
]


def b07_text() -> str:
    return read_utf8(B07_PATH)


def test_b07_file_exists_at_expected_path() -> None:
    assert B07_PATH.exists()
    assert B07_PATH.is_file()


def test_b07_required_sections_are_present() -> None:
    text = b07_text()
    for section in REQUIRED_SECTIONS:
        assert section in text


def test_b07_declares_ownership_and_non_ownership() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "recovery/training/research/preparation project intake",
        "recovery posture routing",
        "training posture routing",
        "research posture routing",
        "preparation/readiness project routing",
        "protected-hidden requirement handling without revealing hidden truth",
        "teacher, mentor, manual, faction, institution, archive, simulation, spirit, relic, domain, or source-local authority access routing",
        "proof, advancement, breakthrough, route, technique, expression, method-seed, lawful-action-vector, prototype, warning, theory, hidden-tag-reveal, and dangerous-temptation routing",
        "source-local donor recovery/training/research/preparation/rest/downtime systems quarantine and escalation rules",
    ]:
        assert phrase in lowered

    for phrase in [
        "final recovery schema",
        "final training schema",
        "final research schema",
        "final preparation schema",
        "final project schema",
        "final actor-state schema",
        "c-family schema fields",
        "c01-c14 schema contents",
        "final recovery math",
        "final healing math",
        "final rest rules",
        "final long-rest/short-rest procedure",
        "final condition removal rules",
        "final training rank math",
        "final competency taxonomy",
        "final advancement proof sufficiency",
        "final breakthrough gates",
        "final expression mechanics",
        "final research truth procedure",
        "final hidden-state reveal rules",
        "final clue system",
        "final playable power authorization",
        "final preparation bonuses",
        "runtime project state",
        "runtime actor state",
        "runtime information state",
        "runtime training/research ledger",
        "sourcebook prose",
        "donor recovery/training/research/rest/downtime systems as astra defaults",
    ]:
        assert phrase in lowered


def test_b07_references_b01_through_b06_as_upstream_batch_b_context() -> None:
    lowered = b07_text().lower()
    for marker in [
        "b01_scene_encounter_and_activity_procedure.md",
        "b02_action_declaration_cost_commitment_and_resolution_trigger_procedure.md",
        "b03_item_gear_equipment_and_asset_use_procedure.md",
        "b04_inventory_storage_custody_and_burden_procedure.md",
        "b05_acquisition_reward_requisition_and_value_flow_procedure.md",
        "b06_project_crafting_salvage_repair_and_upgrade_procedure.md",
        "upstream batch b context",
        "must build on them, not rewrite them",
    ]:
        assert marker in lowered


def test_b07_includes_c00_handoff_language_and_block() -> None:
    text = b07_text()
    for marker in [
        "C00 remains the schema handoff control surface",
        "batch_b_to_c_handoff",
        "target_schema_family: C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 | C11 | C12 | C13 | C14 | pending_schema",
        "schema_status: not_started | stub_index_only | minimum_unlock_draft | tested_minimum | stable_for_family | stable_cross_family | superseded | deprecated",
        "required_c00_base_fields: true",
        "source_evidence_refs_required: true",
        "construct_refs_required: true",
        "outcome_refs_required: true",
        "provenance_refs_required: true",
        "source_local_boundary_required_if_applicable: true",
        "rejected_donor_elements_required_if_applicable: true",
        "canon_eligibility_required: true",
        "review_routing_required: true",
        "unresolved_schema_gap_action: quarantine | escalation | human_review | defer_until_schema_exists",
    ]:
        assert marker in text


def test_b07_includes_renamed_routing_note_as_doctrine_facing_only() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "recovery_training_research_routing_note",
        "doctrine-facing only",
        "not runtime schema",
        "not backend event",
        "not command object",
        "not c-family record",
        "not project database row",
        "not recovery ledger",
        "not training ledger",
        "not research ledger",
        "not hidden-state truth",
        "not playable power",
        "not advancement grant",
        "not final mechanics",
        "not canon",
        "not player-facing rule text",
    ]:
        assert phrase in lowered
    assert "recovery_training_research_preparation_routing_note" not in lowered


def test_b07_includes_required_vocabularies() -> None:
    text = b07_text()
    for marker in [
        "Project families:",
        "Recovery targets:",
        "Training modes:",
        "Research modes:",
        "Desired-outcome classifications:",
        "Requirement states:",
        "Output states:",
        "Complication families:",
        "recovery",
        "training",
        "research",
        "preparation",
        "readiness",
        "rehearsal",
        "field_practice",
        "pressure_training",
        "corrective_training",
        "cross_training",
        "immersive_training",
        "simulation_training",
        "teacher_access",
        "apprenticeship",
        "study",
        "experimentation",
        "reverse_engineering",
        "prototype_development",
        "field_testing",
        "consultation",
        "meditation_comprehension",
        "source_local_recovery",
        "source_local_training",
        "source_local_research",
        "source_local_preparation",
        "unknown_project",
        "injury",
        "condition",
        "fatigue",
        "exposure",
        "corruption",
        "instability",
        "backlash",
        "poison_like_affliction",
        "disease_like_affliction",
        "source_local_impairment",
        "self_practice",
        "guided_instruction",
        "simulation_controlled_scenario",
        "observation",
        "simulation",
        "currently_lawful",
        "lawful_with_cost_risk",
        "requires_preparation",
        "requires_research",
        "requires_training",
        "requires_access",
        "requires_proof",
        "requires_owner_validation",
        "source_local_only",
        "dangerous_temptation",
        "protected_hidden",
        "blocked_by_owner_file",
        "deferred_until_schema_exists",
        "recovery_stabilized",
        "training_progress",
        "proof_candidate_routed",
        "method_seed_created",
        "lawful_action_vector_created",
        "hidden_tag_reveal_routed",
        "readiness_pressure_routed",
        "quarantined_unresolved_delta",
        "false_mastery",
        "harmful_habit",
        "mislearned_method",
        "false_theory",
        "dangerous_prototype",
        "owner_file_gap",
        "schema_gap",
    ]:
        assert marker in text


def test_b07_separates_core_concepts_and_owner_authority() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "recovery is not automatic healing",
        "rest is not automatic reset",
        "training is not rank purchase",
        "practice is not proof by itself",
        "field use may be proof, but proof sufficiency belongs to advancement owners",
        "a teacher is not a vendor",
        "research is not a power grant",
        "a desired outcome is not automatically a valid action",
        "a prototype is not final mechanics",
        "a `method_seed_created` output is a preliminary route",
        "a `lawful_action_vector_created` output means the desired outcome appears to have a possible lawful path",
        "preparation is not a universal bonus",
        "readiness is not automatic advantage",
        "a theory is not hidden truth",
        "d04-style advancement owners decide sufficiency",
        "it must not decide final proof sufficiency",
        "route mechanics, technique mechanics, expression mechanics",
        "b07 is not runtime authority",
        "b07 does not promote canon",
    ]:
        assert phrase in lowered


def test_b07_includes_required_family_procedures_and_hidden_state_protection() -> None:
    text = b07_text()
    for section in [
        "## 12. Recovery project procedure",
        "## 13. Training project procedure",
        "## 14. Teacher, mentor, institution, archive, simulation, and source-local authority procedure",
        "## 15. Research, experimentation, reverse-engineering, and desired-outcome procedure",
        "## 16. Prototype, method-seed, lawful-action-vector, and dangerous-temptation routing",
        "## 17. Preparation, readiness, rehearsal, staging, and risk-reduction procedure",
        "## 18. Proof, advancement, route, technique, expression, and breakthrough handoff rules",
        "Protected-hidden handling procedure:",
        "B07 may mark `protected_hidden`, `hidden_pressure_surface`, or `hidden_tag_reveal_routed` without revealing hidden truth.",
    ]:
        assert section in text


def test_b07_rejects_final_schema_math_runtime_and_sourcebook_rules() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "final recovery schema",
        "final training schema",
        "final research schema",
        "final preparation schema",
        "final recovery math",
        "final healing math",
        "final rest rules",
        "final long-rest/short-rest procedure",
        "final condition removal rules",
        "final training rank math",
        "final competency taxonomy",
        "final advancement proof sufficiency",
        "final breakthrough gates",
        "final expression mechanics",
        "final research truth procedure",
        "final hidden-state reveal rules",
        "final clue system",
        "final playable power authorization",
        "final preparation bonuses",
        "final runtime project state",
        "final runtime actor state",
        "final runtime information state",
        "final runtime training/research ledger",
        "sourcebook prose",
    ]:
        assert phrase in lowered


def test_b07_rejects_runtime_event_command_and_c_family_ownership() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "runtime entity/component/event/state schemas",
        "persistent campaign state",
        "command lifecycle implementation",
        "context packet compiler",
        "hidden-information runtime state",
        "c-family schema fields",
        "c01-c14 schema contents",
        "b07 does not require, define, create, or promote c01-c14",
        "batch b procedure may identify that a c-family handoff is needed, but b07 must not invent c-family fields",
    ]:
        assert phrase in lowered


def test_b07_rejects_donor_defaults_and_includes_state_delta_routing() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "donor recovery/training/research/rest/downtime systems as astra defaults",
        "source-local donor systems are evidence, not astra defaults",
        "do not convert donor recovery math, rest reset, training rank purchase, research truth reveal, preparation bonus, downtime menu, or project-clock assumptions into astra defaults",
        "every meaningful recovery/training/research/preparation event must route at least one delta to a recognized owner",
        "recovery outputs route to harm",
        "training outputs route to competency",
        "research outputs route to information",
        "preparation outputs route to b01/b02/b03/b04/b05/b06",
    ]:
        assert phrase in lowered


def test_b07_includes_source_local_quarantine_and_escalation_fallbacks() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "source-local donor recovery/training/research/preparation handling",
        "quarantine",
        "escalation",
        "human_review",
        "defer_until_schema_exists",
        "source_local_review",
        "schema_review",
        "quarantined_unresolved_delta",
        "owner_file_escalation",
    ]:
        assert phrase in lowered


def test_b07_references_d_series_as_draft_source_pack_material_only() -> None:
    text = b07_text()
    lowered = text.lower()
    for marker in [
        "D00-03_state_delta_commit_protocol.md",
        "D02-00_resolution_architecture_and_owner_boundaries.md",
        "D03_01_power_economy_lattice.md",
        "D04-00_advancement_architecture_overview.md",
        "D04-01_proof_events_and_proof_handling_ledger.md",
        "D04-05_breakthrough_procedure_and_payloads.md",
        "D05-04_training_practice_teachers_and_downtime.md",
        "D05-05_research_experimentation_and_theorycraft.md",
        "D12-04_checkpoints_cost_commitment_consequence_timing_and_handoffs.md",
        "D13-00` through `D13-07",
        "D19-03_record_shape_registry_not_final_schema_governance_and_schema_handoff_control.md",
    ]:
        assert marker in text

    for phrase in [
        "d00-d19 source-pack files are referenced only as draft source-pack/reference material",
        "they are not current doctrine authority, final mechanics, runtime authority, canon, sourcebook prose, or astra defaults",
    ]:
        assert phrase in lowered


def test_b07_does_not_require_define_create_or_promote_later_batch_or_schema_files() -> None:
    lowered = b07_text().lower()
    for phrase in [
        "b07 does not require, define, create, or promote b08-b11",
        "b07 must not create b08-b11",
        "b07 does not require, define, create, or promote c01-c14",
        "c00/c-family handoff language is present and does not invent c-family fields",
    ]:
        assert phrase in lowered


def test_b07_does_not_promote_registry_status_to_current() -> None:
    lowered = b07_text().lower()
    assert "b07 must not promote registry status" in lowered
    assert "status: current" not in lowered
    assert "registry-current" not in lowered
