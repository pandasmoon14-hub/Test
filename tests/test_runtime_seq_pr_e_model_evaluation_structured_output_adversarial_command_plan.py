"""Tests for RUNTIME-SEQ-PR-E model evaluation, structured-output, and adversarial-command plan."""

import pathlib

PLAN_PATH = pathlib.Path("docs/doctrine/reviews/runtime_seq_pr_e_model_evaluation_structured_output_adversarial_command_plan.md")
REGISTRY_PATH = pathlib.Path("docs/doctrine/astra_doctrine_registry_v0_1.yaml")
DECISION_LOG_PATH = pathlib.Path("docs/decisions/current_decisions_log.md")


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


class TestPlanFileExists:
    def test_plan_file_exists(self):
        assert PLAN_PATH.exists(), f"{PLAN_PATH} must exist"


class TestTrackingIds:
    def test_references_pr_e_id(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001" in text

    def test_references_sequencing_review(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in text

    def test_references_pr_a(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001" in text

    def test_references_pr_b(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001" in text

    def test_references_pr_c(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001" in text

    def test_references_pr_d(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001" in text


class TestOwnerTracks:
    def test_rt005_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-005" in text

    def test_rt011_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-011" in text

    def test_rt012_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-012" in text

    def test_primary_owner_tracks(self):
        text = _read(PLAN_PATH)
        assert "primary_owner_tracks" in text
        for track in ["RT-005", "RT-011", "RT-012"]:
            assert track in text, f"{track} must be referenced as primary"

    def test_all_rt_tracks_referenced(self):
        text = _read(PLAN_PATH)
        for i in range(1, 13):
            tag = f"RT-{i:03d}"
            assert tag in text, f"{tag} must be referenced"


class TestBackendFirstInvariant:
    def test_model_interchangeability(self):
        text = _read(PLAN_PATH)
        assert "model-interchangeable" in text

    def test_llm_not_game_engine(self):
        text = _read(PLAN_PATH)
        assert "LLM is not the game engine" in text

    def test_backend_owns_truth(self):
        text = _read(PLAN_PATH)
        assert "backend runtime kernel owns truth" in text


class TestModelRoleTaxonomy:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Model role taxonomy" in text

    def test_local_8b_narrator(self):
        text = _read(PLAN_PATH)
        assert "local_8b_narrator" in text

    def test_local_8b_intent_parser(self):
        text = _read(PLAN_PATH)
        assert "local_8b_intent_parser" in text

    def test_local_8b_clarification_assistant(self):
        text = _read(PLAN_PATH)
        assert "local_8b_clarification_assistant" in text

    def test_local_8b_visible_summary_assistant(self):
        text = _read(PLAN_PATH)
        assert "local_8b_visible_summary_assistant" in text

    def test_api_reflective_summarizer(self):
        text = _read(PLAN_PATH)
        assert "api_reflective_summarizer" in text

    def test_api_evaluator_or_judge(self):
        text = _read(PLAN_PATH)
        assert "api_evaluator_or_judge" in text

    def test_api_canon_or_sourcebook_drafter(self):
        text = _read(PLAN_PATH)
        assert "api_canon_or_sourcebook_drafter" in text

    def test_conversion_assistant(self):
        text = _read(PLAN_PATH)
        assert "conversion_assistant" in text

    def test_backend_validator(self):
        text = _read(PLAN_PATH)
        assert "backend_validator" in text

    def test_backend_packet_compiler(self):
        text = _read(PLAN_PATH)
        assert "backend_packet_compiler" in text

    def test_backend_roles_not_llm(self):
        text = _read(PLAN_PATH)
        assert "not** LLM roles" in text or "not LLM roles" in text.lower()

    def test_all_marked_future_required(self):
        text = _read(PLAN_PATH)
        assert "future_required_not_implemented" in text


class TestModelBehaviorFingerprint:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "ModelBehaviorFingerprint" in text

    def test_instruction_adherence(self):
        text = _read(PLAN_PATH)
        assert "Instruction adherence" in text

    def test_packet_boundary_obedience(self):
        text = _read(PLAN_PATH)
        assert "Packet-boundary obedience" in text

    def test_hidden_information_discipline(self):
        text = _read(PLAN_PATH)
        assert "Hidden-information discipline" in text

    def test_schema_key_obedience(self):
        text = _read(PLAN_PATH)
        assert "Schema-key obedience" in text

    def test_structured_output_completeness(self):
        text = _read(PLAN_PATH)
        assert "Structured-output completeness" in text

    def test_truncation_behavior(self):
        text = _read(PLAN_PATH)
        assert "Truncation behavior" in text

    def test_hallucinated_mechanics_rate(self):
        text = _read(PLAN_PATH)
        assert "Hallucinated mechanics rate" in text

    def test_soft_state_mutation_rate(self):
        text = _read(PLAN_PATH)
        assert "Soft-state mutation rate" in text

    def test_invented_reward_clue_item_rate(self):
        text = _read(PLAN_PATH)
        assert "Invented reward/clue/item/faction/action rate" in text

    def test_actor_knowledge_leakage(self):
        text = _read(PLAN_PATH)
        assert "Actor-knowledge leakage rate" in text

    def test_source_local_canon_boundary(self):
        text = _read(PLAN_PATH)
        assert "Source-local/canon boundary obedience" in text

    def test_narration_faithfulness(self):
        text = _read(PLAN_PATH)
        assert "Narration faithfulness to packet facts" in text

    def test_consistency_under_repeated_runs(self):
        text = _read(PLAN_PATH)
        assert "Consistency under repeated runs" in text

    def test_tendency_to_over_author(self):
        text = _read(PLAN_PATH)
        assert "Tendency to over-author or become GM" in text

    def test_no_final_thresholds(self):
        text = _read(PLAN_PATH)
        assert "future calibration" in text.lower()


class TestRoleQualificationContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Role qualification contract" in text

    def test_narrator_gates(self):
        text = _read(PLAN_PATH)
        section_start = text.find("local_8b_narrator gates")
        section = text[section_start:section_start + 1000]
        assert "Narration faithfulness" in section
        assert "Hidden-info discipline" in section

    def test_intent_parser_gates(self):
        text = _read(PLAN_PATH)
        section_start = text.find("local_8b_intent_parser gates")
        section = text[section_start:section_start + 1000]
        assert "Command intent extraction" in section

    def test_evaluator_gates(self):
        text = _read(PLAN_PATH)
        section_start = text.find("api_evaluator_or_judge gates")
        section = text[section_start:section_start + 1000]
        assert "Rubric adherence" in section

    def test_conversion_gates(self):
        text = _read(PLAN_PATH)
        section_start = text.find("conversion_assistant gates")
        section = text[section_start:section_start + 1000]
        assert "Lawful outcome taxonomy" in section

    def test_future_governance_only(self):
        text = _read(PLAN_PATH)
        assert "future governance planning only" in text.lower()


class TestStructuredOutputContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Structured-output contract" in text

    def test_output_type_field(self):
        text = _read(PLAN_PATH)
        assert "output_type" in text

    def test_model_role_field(self):
        text = _read(PLAN_PATH)
        assert "model_role" in text

    def test_source_packet_ref_field(self):
        text = _read(PLAN_PATH)
        assert "source_packet_ref" in text

    def test_not_backend_truth(self):
        text = _read(PLAN_PATH)
        assert "not** backend truth" in text or "not backend truth" in text.lower()

    def test_not_event_commitment(self):
        text = _read(PLAN_PATH)
        assert "not** event commitment" in text or "not event commitment" in text.lower()

    def test_not_memory_authority(self):
        text = _read(PLAN_PATH)
        assert "not** memory authority" in text or "not memory authority" in text.lower()

    def test_not_canon_promotion(self):
        text = _read(PLAN_PATH)
        assert "not** canon/sourcebook promotion" in text or "not canon/sourcebook promotion" in text.lower()

    def test_unparseable_rejected(self):
        text = _read(PLAN_PATH)
        assert "unparseable" in text.lower()

    def test_no_schema_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Structured-output contract")
        section = text[section_start:section_start + 5000]
        assert "does not implement" in section.lower()


class TestSchemaKeyBehaviorEvaluation:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "SchemaKeyBehaviorEvaluationPolicy" in text

    def test_required_key_presence(self):
        text = _read(PLAN_PATH)
        assert "Required key presence" in text

    def test_forbidden_key_absence(self):
        text = _read(PLAN_PATH)
        assert "Forbidden key absence" in text

    def test_no_invented_schema_fields(self):
        text = _read(PLAN_PATH)
        assert "No invented schema fields" in text

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Schema-key behavior evaluation")
        section = text[section_start:section_start + 4000]
        assert "does not implement" in section.lower()


class TestTruncationSafeStructuredOutputPolicy:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "TruncationSafeStructuredOutputPolicy" in text

    def test_critical_metadata_before_prose(self):
        text = _read(PLAN_PATH)
        assert "Critical metadata must appear before optional prose" in text

    def test_partially_completed_not_complete(self):
        text = _read(PLAN_PATH)
        assert "Partially completed output must not be treated as complete" in text

    def test_continuation_no_invention(self):
        text = _read(PLAN_PATH)
        assert "Continuation requests must not invent new facts" in text

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Truncation-safe structured output policy")
        section = text[section_start:section_start + 3000]
        assert "does not implement" in section.lower()


class TestAdversarialPlayerCommandCorpus:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "AdversarialPlayerCommandCorpus" in text

    def test_hidden_info_reveal(self):
        text = _read(PLAN_PATH)
        assert "Hidden-information reveal attempts" in text

    def test_cost_bypass(self):
        text = _read(PLAN_PATH)
        assert "Cost-bypass attempts" in text

    def test_reward_grant(self):
        text = _read(PLAN_PATH)
        assert "Reward-grant attempts" in text

    def test_inventory_invention(self):
        text = _read(PLAN_PATH)
        assert "Inventory-invention attempts" in text

    def test_dice_roll_through_narration(self):
        text = _read(PLAN_PATH)
        assert "Dice-roll-through-narration attempts" in text

    def test_npc_knowledge_override(self):
        text = _read(PLAN_PATH)
        assert "NPC-knowledge-override attempts" in text

    def test_rumor_to_fact(self):
        text = _read(PLAN_PATH)
        assert "Rumor-to-fact conversion attempts" in text

    def test_source_local_to_canon(self):
        text = _read(PLAN_PATH)
        assert "Source-local-to-canon promotion attempts" in text

    def test_gm_behavior(self):
        text = _read(PLAN_PATH)
        assert "GM-behavior attempts" in text

    def test_prompt_injection(self):
        text = _read(PLAN_PATH)
        assert "Prompt-injection inside player speech" in text

    def test_ambiguity_exploitation(self):
        text = _read(PLAN_PATH)
        assert "Ambiguity exploitation" in text

    def test_all_marked_future_required(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Adversarial player-command corpus")
        section = text[section_start:section_start + 15000]
        assert section.count("future_required_not_implemented") >= 10


class TestMetamorphicRuntimeNarrationTestPlan:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "MetamorphicRuntimeNarrationTestPlan" in text

    def test_packet_fact_reorder(self):
        text = _read(PLAN_PATH)
        assert "Packet-fact reorder invariance" in text

    def test_hidden_fact_removal(self):
        text = _read(PLAN_PATH)
        assert "Hidden-fact removal invariance" in text

    def test_model_provider_backend_truth(self):
        text = _read(PLAN_PATH)
        assert "Model-provider backend-truth invariance" in text

    def test_repeated_run_state(self):
        text = _read(PLAN_PATH)
        assert "Repeated-run state invariance" in text

    def test_rng_backend_reference(self):
        text = _read(PLAN_PATH)
        assert "RNG-backend-reference invariance" in text

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Metamorphic runtime/narration test plan")
        section = text[section_start:section_start + 8000]
        assert "does not implement" in section.lower()


class TestLocalCloudModelComparisonContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Local/cloud model comparison contract" in text

    def test_local_narrator_suitability(self):
        text = _read(PLAN_PATH)
        assert "local_8b_narrator suitability" in text

    def test_api_evaluator_suitability(self):
        text = _read(PLAN_PATH)
        assert "API evaluator/judge suitability" in text

    def test_cannot_change_backend_authority(self):
        text = _read(PLAN_PATH)
        assert "Model comparison cannot change backend authority" in text


class TestFailureModeRoutingContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "FailureModeRoutingContract" in text

    def test_malformed_output(self):
        text = _read(PLAN_PATH)
        assert "malformed_output" in text

    def test_hidden_info_leakage(self):
        text = _read(PLAN_PATH)
        assert "hidden_info_leakage" in text

    def test_soft_state_mutation(self):
        text = _read(PLAN_PATH)
        assert "soft_state_mutation_attempt" in text

    def test_invented_mechanic(self):
        text = _read(PLAN_PATH)
        assert "invented_mechanic" in text

    def test_canon_promotion_attempt(self):
        text = _read(PLAN_PATH)
        assert "canon_promotion_attempt" in text

    def test_unsafe_role_escalation(self):
        text = _read(PLAN_PATH)
        assert "unsafe_role_escalation" in text

    def test_quarantine_routing(self):
        text = _read(PLAN_PATH)
        assert "quarantine output" in text

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Failure-mode routing")
        section = text[section_start:section_start + 8000]
        assert "does not implement" in section.lower()


class TestEvaluationPacketAndTraceRequirements:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Evaluation packet and trace requirements" in text

    def test_evaluation_id(self):
        text = _read(PLAN_PATH)
        assert "evaluation_id" in text

    def test_model_id_or_alias(self):
        text = _read(PLAN_PATH)
        assert "model_id_or_alias" in text

    def test_fingerprint_version(self):
        text = _read(PLAN_PATH)
        assert "fingerprint_version" in text

    def test_not_runtime_truth(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Evaluation packet and trace requirements")
        section = text[section_start:section_start + 3000]
        assert "not runtime truth" in section.lower() or "not model memory" in section.lower()


class TestModelRoleEligibilityLedger:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "ModelRoleEligibilityLedger" in text

    def test_model_identifier(self):
        text = _read(PLAN_PATH)
        assert "model_identifier" in text

    def test_no_permanent_qualification(self):
        text = _read(PLAN_PATH)
        assert "No model should be treated as permanently qualified" in text

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Model-role eligibility ledger")
        section = text[section_start:section_start + 3000]
        assert "does not implement" in section.lower()


class TestTrainingAndFineTuningBoundary:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Training and fine-tuning boundary" in text

    def test_training_not_doctrine(self):
        text = _read(PLAN_PATH)
        assert "Training examples are **not** doctrine" in text

    def test_training_not_canon(self):
        text = _read(PLAN_PATH)
        assert "Training examples are **not** canon" in text

    def test_behavior_not_authority(self):
        text = _read(PLAN_PATH)
        assert "Model behavior is **not** authority" in text

    def test_no_training_authorized(self):
        text = _read(PLAN_PATH)
        assert "does not authorize training data creation" in text.lower()


class TestRuntimeNarrationHandoff:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Runtime/narration handoff" in text

    def test_narrator_receives_narration_render_packet(self):
        text = _read(PLAN_PATH)
        assert "NarrationRenderPacket" in text

    def test_intent_parser_receives_intent_parsing_packet(self):
        text = _read(PLAN_PATH)
        assert "IntentParsingPacket" in text

    def test_no_backend_state_context(self):
        text = _read(PLAN_PATH)
        assert "No model role receives BackendStateContext" in text


class TestRuntimeEventHandoff:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Runtime/event handoff" in text

    def test_output_not_event_commitment(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 18. Runtime/event handoff")
        section = text[section_start:section_start + 2000]
        assert "not** event commitment" in section or "not event commitment" in section.lower()

    def test_cannot_create_state_delta(self):
        text = _read(PLAN_PATH)
        assert "StateDeltaEnvelope" in text

    def test_cannot_append_event_ledger(self):
        text = _read(PLAN_PATH)
        assert "EventLedgerEntry" in text

    def test_proposal_artifacts_only(self):
        text = _read(PLAN_PATH)
        assert "proposal artifacts only" in text


class TestPlayableContentHandoff:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Playable-content handoff" in text

    def test_may_not_validate_playability(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Playable-content handoff")
        section = text[section_start:section_start + 2000]
        assert "not** validate playability proof" in section or "may not validate playability" in section.lower()

    def test_may_not_activate_storylets(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Playable-content handoff")
        section = text[section_start:section_start + 2000]
        assert "not** activate storylets" in section or "may not activate storylets" in section.lower()

    def test_may_not_mutate_quest_dag(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Playable-content handoff")
        section = text[section_start:section_start + 2000]
        assert "not** mutate quest/scenario DAG" in section or "may not mutate quest" in section.lower()


class TestDomainHandoffCrosswalk:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Domain handoff crosswalk" in text

    def test_all_rt_tracks_in_crosswalk(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Domain handoff crosswalk")
        section = text[section_start:section_start + 5000]
        for i in range(1, 13):
            tag = f"RT-{i:03d}"
            assert tag in section, f"{tag} must appear in domain handoff crosswalk"


class TestValidationAndTestRequirements:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Validation and test requirements" in text

    def test_representative_test_families(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "model behavior fingerprint tests" in lower
        assert "role qualification tests" in lower
        assert "structured-output parse tests" in lower
        assert "adversarial tests" in lower
        assert "metamorphic packet tests" in lower


class TestBlockedUntilLedger:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Blocked-until ledger" in text

    def test_representative_blocked_items(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 22. Blocked-until ledger")
        section = text[section_start:section_start + 4000].lower()
        assert "model evaluation runner" in section
        assert "benchmark harness" in section
        assert "adversarial command corpus" in section
        assert "metamorphic test runner" in section
        assert "canon promotion" in section
        assert "training" in section
        assert "live-play adapter" in section


class TestNextRecommendedPR:
    def test_recommends_pr_f(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-F" in text

    def test_pr_f_topics(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "implementation-readiness" in lower or "implementation readiness" in lower
        assert "executable-kernel" in lower or "executable kernel" in lower

    def test_pr_e_does_not_authorize_pr_f(self):
        text = _read(PLAN_PATH)
        assert "does not authorize PR-F" in text.lower() or "does **not** authorize PR-F" in text


class TestNonImplementationReaffirmation:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Non-implementation reaffirmation" in text

    def test_no_model_evaluation_code(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Non-implementation reaffirmation")
        section = text[section_start:section_start + 2000]
        assert "model evaluation code" in section.lower()

    def test_no_benchmark_runner(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Non-implementation reaffirmation")
        section = text[section_start:section_start + 2000]
        assert "benchmark runner" in section.lower()

    def test_no_runtime_code(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Non-implementation reaffirmation")
        section = text[section_start:section_start + 2000]
        assert "runtime code" in section.lower()


class TestClassificationBlock:
    def test_classification_present(self):
        text = _read(PLAN_PATH)
        assert "Classification block" in text

    def test_classification_fields(self):
        text = _read(PLAN_PATH)
        assert "authorizes_model_evaluation_code: false" in text
        assert "authorizes_benchmark_runner: false" in text
        assert "authorizes_prompt_templates: false" in text
        assert "authorizes_model_routing: false" in text
        assert "authorizes_structured_output_schema: false" in text
        assert "authorizes_schema_key_validator: false" in text
        assert "authorizes_adversarial_test_harness: false" in text
        assert "authorizes_metamorphic_test_runner: false" in text
        assert "authorizes_training_data: false" in text
        assert "authorizes_fine_tuning: false" in text
        assert "authorizes_runtime_implementation: false" in text
        assert "authorizes_command_ir: false" in text
        assert "authorizes_context_packet_compiler: false" in text
        assert "authorizes_live_play: false" in text
        assert "authorizes_pilot_conversion: false" in text
        assert "authorizes_sourcebook_inclusion: false" in text
        assert "authorizes_canon_promotion: false" in text

    def test_defines_flags(self):
        text = _read(PLAN_PATH)
        assert "defines_model_role_taxonomy: true" in text
        assert "defines_model_behavior_fingerprint_contract: true" in text
        assert "defines_role_qualification_contract: true" in text
        assert "defines_structured_output_contract: true" in text
        assert "defines_schema_key_behavior_evaluation_policy: true" in text
        assert "defines_truncation_safe_structured_output_policy: true" in text
        assert "defines_adversarial_player_command_corpus_plan: true" in text
        assert "defines_metamorphic_runtime_narration_test_plan: true" in text
        assert "defines_local_cloud_model_comparison_contract: true" in text
        assert "defines_failure_mode_routing_contract: true" in text
        assert "defines_model_role_eligibility_ledger: true" in text


class TestRegistryTracking:
    def test_registry_has_pr_e_entry(self):
        text = _read(REGISTRY_PATH)
        assert "RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001" in text


class TestDecisionLogTracking:
    def test_decision_log_has_pr_e_entry(self):
        text = _read(DECISION_LOG_PATH)
        assert "RUNTIME-SEQ-PR-E-MODEL-EVALUATION-STRUCTURED-OUTPUT-ADVERSARIAL-COMMAND-PLAN-001" in text


class TestNoImplementationClaims:
    def test_plan_does_not_claim_implementation(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        forbidden_claims = [
            "this pr implements",
            "this plan implements model evaluation",
            "this plan implements benchmark",
            "this plan implements runtime",
            "this plan implements schema",
            "this plan implements structured-output schema",
            "this plan implements schema-key validator",
            "this plan implements adversarial test harness",
            "this plan implements metamorphic test runner",
            "this plan implements model behavior fingerprint",
            "this plan implements role eligibility ledger",
            "this plan implements prompt template",
            "this plan implements model routing",
            "this plan implements model adapter",
            "this plan implements command ir",
            "this plan implements validator",
            "this plan implements generator",
            "this plan implements state store",
            "this plan implements event ledger",
            "this plan implements context-packet compiler",
            "this plan implements live-play",
            "this plan implements training",
            "this plan authorizes donor-content audit",
            "this plan authorizes pilot conversion",
            "this plan authorizes sourcebook inclusion",
            "this plan authorizes canon promotion",
        ]
        for claim in forbidden_claims:
            assert claim not in lower, f"Plan must not contain: '{claim}'"
