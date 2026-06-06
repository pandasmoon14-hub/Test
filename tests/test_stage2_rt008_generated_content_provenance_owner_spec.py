from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "docs" / "doctrine" / "control" / "RT008_generated_content_provenance_recurrence_owner_specification.md"
REGISTRY_PATH = ROOT / "docs" / "doctrine" / "astra_doctrine_registry_v0_1.yaml"
DECISION_LOG_PATH = ROOT / "docs" / "decisions" / "current_decisions_log.md"

TRACKING_ID = "REMEDIATION-STAGE2-RT008-GENERATED-CONTENT-PROVENANCE-RECURRENCE-OWNER-SPEC-001"
STAGE2_PR_ID = "STAGE2-PR-E"
TRACK = "RT-008"
STAGE2_PLAN_ID = "REMEDIATION-SCAFFOLD-COMPLETION-REVIEW-STAGE2-PLAN-001"
REMEDIATION_LEDGER_ID = "REMEDIATION-PRIORITY-LEDGER-001"
AUDIT_IDS = ["AUDIT-001", "AUDIT-WAVE1-001", "AUDIT-WAVE2-001"]

REQUIRED_SOURCE_PATHS = [
    "docs/doctrine/control/RT008_generated_content_provenance_recurrence_owner_scaffold.md",
    "docs/doctrine/control/RT001_command_lifecycle_action_legality_owner_specification.md",
    "docs/doctrine/control/RT005_context_packet_hidden_information_owner_specification.md",
    "docs/doctrine/control/RT011_validation_readiness_tooling_owner_specification.md",
    "docs/doctrine/schema/C01_creature_npc_record_schema.md",
    "docs/doctrine/schema/C02_item_gear_record_schema.md",
    "docs/doctrine/schema/C03_ability_power_technique_record_schema.md",
    "docs/doctrine/schema/C05_faction_institution_record_schema.md",
    "docs/doctrine/schema/C06_location_site_region_record_schema.md",
    "docs/doctrine/schema/C07_mission_scenario_adventure_record_schema.md",
    "docs/doctrine/schema/C08_vehicle_ship_platform_record_schema.md",
    "docs/doctrine/schema/C09_hazard_environment_record_schema.md",
    "docs/doctrine/schema/C10_table_oracle_record_schema.md",
    "docs/doctrine/schema/C14_source_local_setting_cosmology_record_schema.md",
    "docs/doctrine/schema_math_mechanics/SM00_schema_math_mechanics_master_scope_and_sequencing_plan.md",
    "docs/doctrine/schema_math_mechanics/SM01_validation_schema_inventory_and_readiness_controls.md",
    "docs/doctrine/schema_math_mechanics/SM02_minimum_pilot_conversion_readiness_and_packet_validation_controls.md",
    "docs/doctrine/astra_doctrine_roadmap_v0_1.md",
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "docs/decisions/current_decisions_log.md",
    "README.md",
]

STATUSES = [
    "ephemeral_generated_proposal",
    "reviewer_candidate",
    "rejected_generated_proposal",
    "quarantine_pending_provenance",
    "source_local_generated_content",
    "durable_generated_candidate",
    "recurrent_generated_candidate",
    "persistent_generated_record_pending",
    "backend_committed_generated_record",
    "sourcebook_candidate_requires_separate_review",
    "canon_candidate_requires_separate_review",
    "accepted_canon_requires_canon_protocol",
]

FUTURE_ARTIFACTS = [
    "GeneratedProposalRequirement",
    "GeneratedContentProvenanceRequirement",
    "SourceLocalGeneratedBoundaryRequirement",
    "DurableEligibilityRequirement",
    "RecurrenceEligibilityRequirement",
    "StableIdentifierRequirement",
    "GenerationDependencyRequirement",
    "GeneratedContentReviewRequirement",
    "GeneratedContentValidationRequirement",
    "GeneratedContentRejectionRequirement",
    "GeneratedContentQuarantineRequirement",
    "GeneratedContentVisibilityRequirement",
    "GeneratedContentPersistenceHandoffRequirement",
    "GeneratedContentCanonBoundaryRequirement",
    "GeneratedContentSourcebookBoundaryRequirement",
]

GUARDRAILS = [
    "runtime code",
    "schema implementation",
    "command IR implementation",
    "validator implementation",
    "generator implementation",
    "procedural generation engine",
    "generated content records",
    "durable generated records",
    "stable ID allocator",
    "recurrence engine",
    "content writer",
    "persistence writer",
    "retrieval index",
    "context-packet compiler",
    "RNG/dice/table implementation",
    "event ledger implementation",
    "database schema",
    "live-play prompt",
    "training data",
    "donor-content audit",
    "sourcebook inclusion authorization",
    "pilot conversion authorization",
    "canon promotion",
]


def read(path: Path) -> str:
    assert path.exists(), f"Missing expected file: {path}"
    return path.read_text(encoding="utf-8")


def test_owner_specification_file_exists_and_has_core_tracking() -> None:
    text = read(SPEC_PATH)
    for expected in [TRACKING_ID, STAGE2_PR_ID, TRACK]:
        assert expected in text


def test_owner_spec_references_required_sources() -> None:
    text = read(SPEC_PATH)
    for expected in [STAGE2_PLAN_ID, REMEDIATION_LEDGER_ID, *AUDIT_IDS, *REQUIRED_SOURCE_PATHS]:
        assert expected in text


def test_scope_and_authority_model_cover_required_boundaries() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "generated-content provenance ownership boundaries",
        "source-local versus generated versus persistent versus recurrent versus canon/sourcebook status separation",
        "ephemeral proposal versus durable generated content separation",
        "durable-record eligibility requirements",
        "recurrence eligibility requirements",
        "stable identifier requirement boundaries",
        "generator-output review requirements",
        "generator-disablement posture",
        "context-packet projection handoffs through RT-005",
        "validation/readiness handoffs through RT-011",
        "RT-001 owns command/event lifecycle",
        "RT-005 owns whether generated-content facts may be projected",
        "RT-011 owns validation/readiness requirements",
        "RT-009 owns random/table/oracle authority",
        "The LLM may propose text or options only inside bounded context",
    ]:
        assert phrase in text


def test_status_contract_is_placeholder_only() -> None:
    text = read(SPEC_PATH)
    for status in STATUSES:
        assert status in text
    for phrase in [
        "not final schemas",
        "not database fields",
        "not generated records",
        "not persistence states",
        "not runtime state",
        "not content writer output",
        "not sourcebook statuses by themselves",
        "not canon statuses by themselves",
    ]:
        assert phrase in text


def test_provenance_recurrence_family_artifacts_and_validation_are_future_only() -> None:
    text = read(SPEC_PATH)
    for phrase in [
        "generated content must preserve generation source, prompt/context basis, originating command/event if any",
        "durable generated content must have backend-owned provenance, stable identity, validation status, and event/state/persistence handoff before recurrence",
        "recurrent generated content requires explicit recurrence eligibility",
        "source-local generated content must remain bounded",
        "generated content depending on random tables/oracles must route through RT-009",
        "generated content visible to the LLM/player must route through RT-005",
        "does not define final fields, JSON schema, database schema, ID format, generator logic, recurrence algorithm, content writer logic, validator code",
    ]:
        assert phrase in text
    for artifact in FUTURE_ARTIFACTS:
        assert artifact in text
    assert text.count("future_required_not_implemented") >= len(FUTURE_ARTIFACTS)
    for validation in [
        "source linkage validation",
        "generated status separation validation",
        "ephemeral-versus-durable separation validation",
        "source-local boundary validation",
        "provenance chain coverage validation",
        "stable identifier authorization validation",
        "recurrence eligibility validation",
        "random dependency routing validation",
        "context projection routing validation",
        "canon/sourcebook boundary validation",
        "LLM non-authority validation",
        "non-implementation guardrail validation",
    ]:
        assert validation in text


def test_downstream_handoffs_and_llm_non_authority_are_explicit() -> None:
    text = read(SPEC_PATH)
    for rt in [f"RT-{index:03d}" for index in range(1, 13)]:
        assert rt in text
    for phrase in [
        "creating durable generated records",
        "deciding recurrence eligibility",
        "assigning persistent IDs",
        "deciding generated-content provenance as accepted",
        "treating repeated narration as recurrence",
        "treating summaries as generated-content memory authority",
        "treating generated prose as canon or sourcebook content",
        "promoting generated content to canon",
        "deciding source-local boundaries",
        "bypassing reviewer/backend validation",
        "writing generated content to files or databases",
        "choosing random generated outputs without RT-009 authority",
        "projecting hidden generated facts without RT-005 authority",
        "authorizing live-play/training/sourcebook/canon use",
    ]:
        assert phrase in text


def test_non_implementation_classification_registry_and_decision_log_are_present() -> None:
    text = read(SPEC_PATH)
    for phrase in GUARDRAILS:
        assert phrase in text
    for phrase in [
        "stage2_output:",
        "stage2_pr_id: STAGE2-PR-E",
        "track: RT-008",
        "artifact_type: owner_specification",
        "implementation_status: non_executable_planning",
        "authorizes_runtime_implementation: false",
        "authorizes_schema_implementation: false",
        "authorizes_validator_implementation: false",
        "authorizes_generator_implementation: false",
        "authorizes_generated_records: false",
        "authorizes_durable_generated_records: false",
        "authorizes_stable_id_allocator: false",
        "authorizes_recurrence_engine: false",
        "authorizes_persistence_writer: false",
        "authorizes_retrieval_index: false",
        "authorizes_context_packet_compiler: false",
        "authorizes_live_play: false",
        "authorizes_training: false",
        "authorizes_sourcebook_inclusion: false",
        "authorizes_canon_promotion: false",
        "authorizes_pilot_conversion: false",
        "next_allowed_step: RT-009 owner specification, pending review",
    ]:
        assert phrase in text
    for tracked_text in [read(REGISTRY_PATH), read(DECISION_LOG_PATH)]:
        assert TRACKING_ID in tracked_text
        assert "Stage 2 owner" in tracked_text or "Stage 2 owner-specification" in tracked_text
        for phrase in GUARDRAILS:
            assert phrase in tracked_text
