"""Tests for RUNTIME-SEQ-PR-D story-capable structure and playable-content plan."""

import pathlib

PLAN_PATH = pathlib.Path("docs/doctrine/reviews/runtime_seq_pr_d_story_capable_structure_playable_content_plan.md")
REGISTRY_PATH = pathlib.Path("docs/doctrine/astra_doctrine_registry_v0_1.yaml")
DECISION_LOG_PATH = pathlib.Path("docs/decisions/current_decisions_log.md")


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


class TestPlanFileExists:
    def test_plan_file_exists(self):
        assert PLAN_PATH.exists(), f"{PLAN_PATH} must exist"


class TestTrackingIds:
    def test_references_pr_d_id(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001" in text

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


class TestOwnerTracks:
    def test_rt006_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-006" in text

    def test_rt007_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-007" in text

    def test_rt008_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-008" in text

    def test_rt011_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-011" in text

    def test_rt012_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-012" in text

    def test_primary_owner_tracks(self):
        text = _read(PLAN_PATH)
        assert "primary_owner_tracks" in text
        for track in ["RT-006", "RT-007", "RT-008", "RT-011", "RT-012"]:
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


class TestStoryCapableStructurePrinciple:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Story-capable structure principle" in text

    def test_not_narrative_prose(self):
        text = _read(PLAN_PATH)
        assert '"narrative prose"' in text or "not narrative prose" in text.lower() or '"story-capable" is **not** "narrative prose"' in text.lower() or 'not** "narrative prose' in text

    def test_expose_player_agency(self):
        text = _read(PLAN_PATH)
        assert "player agency" in text.lower()

    def test_actionable_affordances(self):
        text = _read(PLAN_PATH)
        assert "actionable affordances" in text.lower()

    def test_stateful_consequences(self):
        text = _read(PLAN_PATH)
        assert "stateful consequences" in text.lower()

    def test_renderable_by_narrator_packet(self):
        text = _read(PLAN_PATH)
        assert "narrator packet" in text.lower()


class TestPlayableContentBoundary:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Playable-content boundary" in text

    def test_playable_scene_structure(self):
        text = _read(PLAN_PATH)
        assert "PlayableSceneStructure" in text

    def test_narrative_substrate(self):
        text = _read(PLAN_PATH)
        assert "NarrativeSubstrate" in text

    def test_scene_object_contract(self):
        text = _read(PLAN_PATH)
        assert "SceneObjectContract" in text

    def test_storylet_contract(self):
        text = _read(PLAN_PATH)
        assert "StoryletContract" in text

    def test_scenario_node_contract(self):
        text = _read(PLAN_PATH)
        assert "ScenarioNodeContract" in text

    def test_quest_scenario_dependency_dag(self):
        text = _read(PLAN_PATH)
        assert "QuestScenarioDependencyDAG" in text

    def test_playability_proof_contract(self):
        text = _read(PLAN_PATH)
        assert "PlayabilityProofContract" in text

    def test_player_agency_affordance_set(self):
        text = _read(PLAN_PATH)
        assert "PlayerAgencyAffordanceSet" in text

    def test_consequence_route_contract(self):
        text = _read(PLAN_PATH)
        assert "ConsequenceRouteContract" in text

    def test_failure_partial_success_contract(self):
        text = _read(PLAN_PATH)
        assert "FailurePartialSuccessContract" in text

    def test_escalation_hook_contract(self):
        text = _read(PLAN_PATH)
        assert "EscalationHookContract" in text

    def test_clue_route_playable_contract(self):
        text = _read(PLAN_PATH)
        assert "ClueRoutePlayableContract" in text

    def test_reward_route_playable_contract(self):
        text = _read(PLAN_PATH)
        assert "RewardRoutePlayableContract" in text

    def test_social_contact_playable_contract(self):
        text = _read(PLAN_PATH)
        assert "SocialContactPlayableContract" in text

    def test_hazard_pressure_playable_contract(self):
        text = _read(PLAN_PATH)
        assert "HazardPressurePlayableContract" in text

    def test_source_local_capsule_playable_boundary(self):
        text = _read(PLAN_PATH)
        assert "SourceLocalCapsulePlayableBoundary" in text

    def test_all_marked_future_required(self):
        text = _read(PLAN_PATH)
        assert "future_required_not_implemented" in text


class TestPlayabilityProofContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Playability proof contract" in text

    def test_player_facing_action(self):
        text = _read(PLAN_PATH)
        assert "player-facing action" in text.lower()

    def test_consequence_route(self):
        text = _read(PLAN_PATH)
        assert "consequence route" in text.lower()

    def test_failure_route(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "failure" in lower and "complication" in lower

    def test_future_validation_only(self):
        text = _read(PLAN_PATH)
        assert "future validation planning only" in text.lower()

    def test_routes_through_rt_owners(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Playability proof contract")
        section = text[section_start:section_start + 3000]
        assert "RT-002" in section
        assert "RT-005" in section
        assert "RT-006" in section
        assert "RT-007" in section
        assert "RT-008" in section
        assert "RT-009" in section
        assert "RT-012" in section


class TestNarrativeSubstrateContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Narrative substrate contract" in text

    def test_not_prose(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Narrative substrate contract")
        section = text[section_start:section_start + 3000]
        assert "not** prose" in section or "not prose" in section.lower()

    def test_not_prompt_template(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Narrative substrate contract")
        section = text[section_start:section_start + 3000]
        assert "prompt template" in section.lower()

    def test_not_canon(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Narrative substrate contract")
        section = text[section_start:section_start + 3000]
        assert "not** canon" in section or "not canon" in section.lower()

    def test_not_event_state(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Narrative substrate contract")
        section = text[section_start:section_start + 3000]
        assert "event state" in section.lower()


class TestStoryletContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Storylet contract" in text

    def test_bounded(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 8. Storylet contract")
        section = text[section_start:section_start + 3000]
        assert "Bounded" in section

    def test_triggerable_by_backend(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 8. Storylet contract")
        section = text[section_start:section_start + 3000]
        assert "backend state" in section.lower() or "backend-evaluated" in section.lower()

    def test_provenance_backed(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 8. Storylet contract")
        section = text[section_start:section_start + 3000]
        assert "provenance" in section.lower()

    def test_source_local_unless_promoted(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 8. Storylet contract")
        section = text[section_start:section_start + 3000]
        assert "source-local unless promoted" in section.lower()

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 8. Storylet contract")
        section = text[section_start:section_start + 3000]
        assert "does not implement" in section.lower()


class TestQuestScenarioDependencyDAG:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Quest/scenario dependency DAG contract" in text

    def test_scenario_nodes(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Quest/scenario dependency DAG contract")
        section = text[section_start:section_start + 3000]
        assert "Scenario nodes" in section

    def test_not_quest_engine(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Quest/scenario dependency DAG contract")
        section = text[section_start:section_start + 3000]
        assert "not** a quest engine" in section or "not a quest engine" in section.lower()

    def test_not_runtime_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Quest/scenario dependency DAG contract")
        section = text[section_start:section_start + 3000]
        assert "not** a runtime implementation" in section or "not a runtime implementation" in section.lower()


class TestNPCGoalStackAndActorIntent:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "NPC goal stack and actor-intent contract" in text

    def test_npc_goal_stack(self):
        text = _read(PLAN_PATH)
        assert "NPCGoalStack" in text

    def test_actor_intent_contract(self):
        text = _read(PLAN_PATH)
        assert "ActorIntentContract" in text

    def test_backend_owned(self):
        text = _read(PLAN_PATH)
        section_start = text.find("NPC goal stack and actor-intent contract")
        section = text[section_start:section_start + 4000]
        assert "backend-owned" in section.lower()

    def test_llm_may_not_decide_motives(self):
        text = _read(PLAN_PATH)
        section_start = text.find("NPC goal stack and actor-intent contract")
        section = text[section_start:section_start + 4000]
        assert "private motives" in section.lower()

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("NPC goal stack and actor-intent contract")
        section = text[section_start:section_start + 4000]
        assert "does not implement" in section.lower()


class TestDialogueActIR:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "DialogueActIR planning contract" in text

    def test_dialogue_act_families(self):
        text = _read(PLAN_PATH)
        for act in ["ask", "answer", "refuse", "threaten", "bargain", "deceive", "reveal", "conceal"]:
            assert f"**{act}**" in text.lower() or f"- **{act}" in text.lower()

    def test_dialogue_text_not_social_state(self):
        text = _read(PLAN_PATH)
        assert "dialogue text is not social state" in text.lower() or "Dialogue text is not social state" in text

    def test_promises_require_backend(self):
        text = _read(PLAN_PATH)
        assert "backend commitment" in text.lower()

    def test_deception_not_verified_facts(self):
        text = _read(PLAN_PATH)
        assert "must not become verified facts" in text.lower()

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("DialogueActIR planning contract")
        section = text[section_start:section_start + 5000]
        assert "does not implement" in section.lower()


class TestContentEcologyContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Content ecology contract" in text

    def test_content_ecology_contract_name(self):
        text = _read(PLAN_PATH)
        assert "ContentEcologyContract" in text

    def test_contradiction_pressure(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Content ecology contract")
        section = text[section_start:section_start + 3000]
        assert "contradiction pressure" in section.lower()

    def test_escalation_saturation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Content ecology contract")
        section = text[section_start:section_start + 3000]
        assert "escalation saturation" in section.lower()

    def test_not_canon(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Content ecology contract")
        section = text[section_start:section_start + 3000]
        assert "not** canon" in section or "not canon" in section.lower()


class TestSourceLocalCapsuleBoundaryExpansion:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Source-local capsule boundary expansion" in text

    def test_source_local_capsule_boundary(self):
        text = _read(PLAN_PATH)
        assert "SourceLocalCapsuleBoundary" in text

    def test_cannot_become_canon(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Source-local capsule boundary expansion")
        section = text[section_start:section_start + 3000]
        assert "cannot" in section.lower() and "canon" in section.lower()

    def test_rt012_governance(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Source-local capsule boundary expansion")
        section = text[section_start:section_start + 3000]
        assert "RT-012" in section


class TestGeneratorToValidateToCommitPipeline:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Generator-to-validate-to-commit pipeline" in text

    def test_pipeline_stages(self):
        text = _read(PLAN_PATH)
        for stage in [
            "generate_candidate",
            "assign_provenance",
            "validate_schema_readiness",
            "validate_playability",
            "validate_owner_handoffs",
            "validate_visibility",
            "validate_invariants",
            "validate_packet_renderability",
            "quarantine_or_repair_if_invalid",
            "commit_as_runtime_record",
            "project_to_packets",
        ]:
            assert stage in text, f"Pipeline stage {stage} must be present"

    def test_generation_is_not_commitment(self):
        text = _read(PLAN_PATH)
        assert "generation is not commitment" in text.lower() or "Generation is not commitment" in text

    def test_no_implementation(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Generator-to-validate-to-commit pipeline")
        section = text[section_start:section_start + 4000]
        assert "does not implement" in section.lower()


class TestMinimumViableSceneObject:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Minimum viable scene object contract" in text

    def test_minimum_viable_scene_object(self):
        text = _read(PLAN_PATH)
        assert "MinimumViableSceneObject" in text

    def test_decorative_objects_allowed(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Minimum viable scene object contract")
        section = text[section_start:section_start + 3000]
        assert "decorative" in section.lower()


class TestRuntimeNarrationHandoff:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Runtime/narration handoff" in text

    def test_narrator_may_not_invent(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Runtime/narration handoff")
        section = text[section_start:section_start + 2000]
        assert "invent new actionable objects" in section.lower()

    def test_narrator_may_not_resolve_storylet(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Runtime/narration handoff")
        section = text[section_start:section_start + 2000]
        assert "resolve storylet outcomes" in section.lower()

    def test_narrator_may_not_mutate_npc_goals(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Runtime/narration handoff")
        section = text[section_start:section_start + 2000]
        assert "mutate NPC goals" in section


class TestRuntimeEventHandoff:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Runtime/event handoff" in text

    def test_storylet_triggers_not_commits(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Runtime/event handoff")
        section = text[section_start:section_start + 2000]
        assert "Storylet triggers are not event commits" in section

    def test_generated_structure_not_persistent(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Runtime/event handoff")
        section = text[section_start:section_start + 2000]
        assert "not persistent state until committed" in section.lower()

    def test_correction_events(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Runtime/event handoff")
        section = text[section_start:section_start + 2000]
        assert "correction event" in section.lower()


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
        assert "playability proof tests" in lower
        assert "storylet eligibility boundary tests" in lower
        assert "hidden-info leakage tests" in lower
        assert "llm overreach" in lower


class TestBlockedUntilLedger:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Blocked-until ledger" in text

    def test_representative_blocked_items(self):
        text = _read(PLAN_PATH)
        section_start = text.find("## 20. Blocked-until ledger")
        section = text[section_start:section_start + 4000].lower()
        assert "storylet system" in section
        assert "quest engine" in section
        assert "npc ai" in section
        assert "dialogue system" in section
        assert "canon promotion" in section
        assert "training" in section
        assert "live-play adapter" in section


class TestNextRecommendedPR:
    def test_recommends_pr_e(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-E" in text

    def test_pr_e_topics(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "model evaluation" in lower or "model behavior fingerprinting" in lower
        assert "structured-output" in lower or "structured output" in lower
        assert "adversarial" in lower


class TestNonImplementationReaffirmation:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Non-implementation reaffirmation" in text

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
        assert "authorizes_runtime_implementation: false" in text
        assert "authorizes_schema_implementation: false" in text
        assert "authorizes_canon_promotion: false" in text
        assert "authorizes_storylet_system: false" in text
        assert "authorizes_narrative_substrate_schema: false" in text
        assert "authorizes_playable_content_validator: false" in text
        assert "authorizes_quest_engine: false" in text
        assert "authorizes_scenario_engine: false" in text
        assert "authorizes_dependency_dag_engine: false" in text
        assert "authorizes_npc_ai: false" in text
        assert "authorizes_behavior_tree: false" in text
        assert "authorizes_dialogue_system: false" in text
        assert "authorizes_dialogue_act_ir: false" in text
        assert "authorizes_content_ecology_engine: false" in text
        assert "authorizes_generator_implementation: false" in text
        assert "authorizes_live_play: false" in text
        assert "authorizes_training: false" in text
        assert "authorizes_pilot_conversion: false" in text
        assert "authorizes_sourcebook_inclusion: false" in text

    def test_defines_flags(self):
        text = _read(PLAN_PATH)
        assert "defines_story_capable_structure_principle: true" in text
        assert "defines_playable_content_boundary: true" in text
        assert "defines_playability_proof_contract: true" in text
        assert "defines_narrative_substrate_contract: true" in text
        assert "defines_storylet_contract: true" in text
        assert "defines_quest_scenario_dependency_dag_contract: true" in text
        assert "defines_npc_goal_stack_contract: true" in text
        assert "defines_dialogue_act_ir_planning_contract: true" in text
        assert "defines_content_ecology_contract: true" in text
        assert "defines_source_local_capsule_boundary_expansion: true" in text
        assert "defines_generator_to_validate_to_commit_pipeline: true" in text


class TestRegistryTracking:
    def test_registry_has_pr_d_entry(self):
        text = _read(REGISTRY_PATH)
        assert "RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001" in text


class TestDecisionLogTracking:
    def test_decision_log_has_pr_d_entry(self):
        text = _read(DECISION_LOG_PATH)
        assert "RUNTIME-SEQ-PR-D-STORY-CAPABLE-STRUCTURE-PLAYABLE-CONTENT-PLAN-001" in text


class TestNoImplementationClaims:
    def test_plan_does_not_claim_implementation(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        forbidden_claims = [
            "this pr implements",
            "this plan implements runtime",
            "this plan implements schema",
            "this plan implements storylet system",
            "this plan implements narrative substrate schema",
            "this plan implements playable-content validator",
            "this plan implements quest engine",
            "this plan implements scenario engine",
            "this plan implements dependency dag engine",
            "this plan implements npc ai",
            "this plan implements behavior tree",
            "this plan implements dialogue system",
            "this plan implements dialogueactir",
            "this plan implements content ecology engine",
            "this plan implements generator",
            "this plan implements command ir",
            "this plan implements validator",
            "this plan implements state store",
            "this plan implements event ledger",
            "this plan implements context-packet compiler",
            "this plan implements prompt template",
            "this plan implements live-play",
            "this plan implements training",
            "this plan authorizes donor-content audit",
            "this plan authorizes pilot conversion",
            "this plan authorizes sourcebook inclusion",
            "this plan authorizes canon promotion",
        ]
        for claim in forbidden_claims:
            assert claim not in lower, f"Plan must not contain: '{claim}'"
