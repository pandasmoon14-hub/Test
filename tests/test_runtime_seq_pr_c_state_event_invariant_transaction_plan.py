"""Tests for RUNTIME-SEQ-PR-C state/event/invariant/transaction plan."""

import pathlib

PLAN_PATH = pathlib.Path("docs/doctrine/reviews/runtime_seq_pr_c_state_event_invariant_transaction_plan.md")
REGISTRY_PATH = pathlib.Path("docs/doctrine/astra_doctrine_registry_v0_1.yaml")
DECISION_LOG_PATH = pathlib.Path("docs/decisions/current_decisions_log.md")


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


class TestPlanFileExists:
    def test_plan_file_exists(self):
        assert PLAN_PATH.exists(), f"{PLAN_PATH} must exist"


class TestTrackingIds:
    def test_references_pr_c_id(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001" in text

    def test_references_sequencing_review(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SCHEMA-IMPLEMENTATION-SEQUENCING-REVIEW-001" in text

    def test_references_pr_a(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-A-MINIMUM-BACKEND-KERNEL-RUNTIME-QUALITY-CONTRACT-PLAN-001" in text

    def test_references_pr_b(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-B-NARRATION-CONTEXT-PACKET-CONTRACT-PLAN-001" in text


class TestOwnerTracks:
    def test_rt001_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-001" in text

    def test_rt011_primary(self):
        text = _read(PLAN_PATH)
        assert "RT-011" in text

    def test_primary_owner_tracks(self):
        text = _read(PLAN_PATH)
        assert "Primary owner tracks: RT-001, RT-011" in text or (
            "primary_owner_tracks" in text and "RT-001" in text and "RT-011" in text
        )

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


class TestStateEventBoundary:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "State/event boundary" in text

    def test_backend_state_store(self):
        text = _read(PLAN_PATH)
        assert "BackendStateStore" in text

    def test_state_projection(self):
        text = _read(PLAN_PATH)
        assert "StateProjection" in text

    def test_transaction_preview(self):
        text = _read(PLAN_PATH)
        assert "TransactionPreview" in text

    def test_state_delta_envelope(self):
        text = _read(PLAN_PATH)
        assert "StateDeltaEnvelope" in text

    def test_event_ledger_entry(self):
        text = _read(PLAN_PATH)
        assert "EventLedgerEntry" in text

    def test_runtime_trace(self):
        text = _read(PLAN_PATH)
        assert "RuntimeTrace" in text

    def test_narration_display_output(self):
        text = _read(PLAN_PATH)
        assert "NarrationDisplayOutput" in text

    def test_summary_artifact(self):
        text = _read(PLAN_PATH)
        assert "SummaryArtifact" in text

    def test_correction_event(self):
        text = _read(PLAN_PATH)
        assert "CorrectionEvent" in text


class TestTransactionLifecycleContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Transaction lifecycle contract" in text

    def test_representative_stages(self):
        text = _read(PLAN_PATH)
        for stage in [
            "player_input_received",
            "command_legality_checked",
            "transaction_preview_created",
            "state_delta_prepared",
            "event_commit_authorized",
            "event_appended",
            "narration_displayed",
            "trace_recorded",
        ]:
            assert stage in text, f"Stage {stage} must be present"

    def test_rejection_stages(self):
        text = _read(PLAN_PATH)
        for stage in [
            "command_rejected",
            "invariant_violation_detected",
            "hidden_info_leakage_blocked",
            "event_commit_denied",
        ]:
            assert stage in text, f"Rejection stage {stage} must be present"

    def test_planning_labels_disclaimer(self):
        text = _read(PLAN_PATH)
        assert "planning labels only" in text


class TestTransactionPreviewContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Transaction preview contract" in text

    def test_preview_not_commitment(self):
        text = _read(PLAN_PATH)
        assert "preview is not event commitment" in text.lower() or "Transaction preview is not event commitment" in text


class TestStateDeltaContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "State delta contract" in text

    def test_conceptual_contract_disclaimer(self):
        text = _read(PLAN_PATH)
        assert "conceptual contract" in text


class TestEventLedgerContract:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Event ledger contract" in text

    def test_event_families(self):
        text = _read(PLAN_PATH)
        for family in [
            "command_event",
            "transaction_event",
            "state_delta_event",
            "correction_event",
            "validation_event",
        ]:
            assert family in text, f"Event family {family} must be present"


class TestEventChannelBoundary:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Event-channel boundary" in text

    def test_representative_channels(self):
        text = _read(PLAN_PATH)
        for channel in [
            "mechanical_state_channel",
            "visibility_channel",
            "narration_display_channel",
            "rng_table_channel",
            "correction_channel",
        ]:
            assert channel in text, f"Channel {channel} must be present"

    def test_narration_cannot_mutate(self):
        text = _read(PLAN_PATH)
        assert "narration display events may be logged but cannot mutate mechanical state" in text.lower() or \
               "logged but cannot mutate mechanical state" in text


class TestWorldInvariantRegistry:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "WorldInvariantRegistry" in text

    def test_representative_invariant_categories(self):
        text = _read(PLAN_PATH)
        for cat in [
            "authority_invariants",
            "state_consistency_invariants",
            "visibility_hidden_info_invariants",
            "resource_cost_invariants",
            "rng_replay_invariants",
            "packet_narration_invariants",
        ]:
            assert cat in text, f"Invariant category {cat} must be present"

    def test_representative_invariant_language(self):
        text = _read(PLAN_PATH)
        assert "hidden facts must not appear in player-visible packets" in text.lower() or \
               "Hidden facts must not appear in player-visible packets" in text
        assert "narration must not become state" in text.lower() or \
               "Narration must not become state" in text


class TestRollbackSafeValidation:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Rollback-safe validation" in text

    def test_failed_validation_leaves_state_unchanged(self):
        text = _read(PLAN_PATH)
        assert "leave state unchanged" in text.lower() or "Failed validation must leave state unchanged" in text


class TestCorrectionEventProtocol:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Correction event protocol" in text

    def test_append_only(self):
        text = _read(PLAN_PATH)
        assert "append-only" in text


class TestReplayHashAudit:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Replay/hash/audit requirements" in text

    def test_future_required(self):
        text = _read(PLAN_PATH)
        assert "future-required and not implemented here" in text


class TestRuntimeTraceRequirements:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Runtime trace requirements" in text

    def test_traces_not_state_authority(self):
        text = _read(PLAN_PATH)
        assert "not state authority" in text


class TestLLMNonAuthority:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "LLM non-authority rules" in text

    def test_prohibitions(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "creating backend state" in lower
        assert "mutating backend state" in lower
        assert "rolling dice" in lower
        assert "converting narration into truth" in lower


class TestDomainHandoffCrosswalk:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Domain handoff crosswalk" in text

    def test_rt001_mapping(self):
        text = _read(PLAN_PATH)
        assert "command lifecycle" in text.lower()
        assert "event commit boundary" in text.lower() or "event commit" in text.lower()


class TestValidationAndTestRequirements:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Validation and test requirements" in text

    def test_representative_test_families(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "transaction preview no-mutation" in lower
        assert "event append-only" in lower
        assert "narration-not-state" in lower


class TestBlockedUntilLedger:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Blocked-until ledger" in text

    def test_representative_blocked_items(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "state store implementation" in lower
        assert "event ledger implementation" in lower
        assert "canon promotion" in lower


class TestNextRecommendedPR:
    def test_recommends_pr_d(self):
        text = _read(PLAN_PATH)
        assert "RUNTIME-SEQ-PR-D" in text

    def test_pr_d_topics(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        assert "story-capable" in lower
        assert "playable-content" in lower or "playable content" in lower


class TestNonImplementationReaffirmation:
    def test_heading_present(self):
        text = _read(PLAN_PATH)
        assert "Non-implementation reaffirmation" in text

    def test_no_runtime_code(self):
        text = _read(PLAN_PATH)
        section_start = text.find("Non-implementation reaffirmation")
        section = text[section_start:section_start + 1500]
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
        assert "defines_state_event_boundary: true" in text
        assert "defines_transaction_lifecycle_contract: true" in text
        assert "defines_world_invariant_registry_requirements: true" in text


class TestRegistryTracking:
    def test_registry_has_pr_c_entry(self):
        text = _read(REGISTRY_PATH)
        assert "RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001" in text


class TestDecisionLogTracking:
    def test_decision_log_has_pr_c_entry(self):
        text = _read(DECISION_LOG_PATH)
        assert "RUNTIME-SEQ-PR-C-STATE-EVENT-INVARIANT-TRANSACTION-PLAN-001" in text


class TestNoImplementationClaims:
    def test_plan_does_not_claim_implementation(self):
        text = _read(PLAN_PATH)
        lower = text.lower()
        forbidden_claims = [
            "this pr implements",
            "this plan implements runtime",
            "this plan implements schema",
            "this plan implements command ir",
            "this plan implements validator",
            "this plan implements generator",
            "this plan implements state store",
            "this plan implements state delta",
            "this plan implements event ledger",
            "this plan implements transaction preview",
            "this plan implements rollback",
            "this plan implements invariant validator",
            "this plan implements correction event schema",
            "this plan implements replay",
            "this plan implements runtime trace",
            "this plan implements persistence",
            "this plan implements database",
            "this plan implements context-packet compiler",
            "this plan implements rng",
            "this plan implements domain",
            "this plan implements live-play",
            "this plan implements training",
            "this plan authorizes donor-content audit",
            "this plan authorizes pilot conversion",
            "this plan authorizes sourcebook inclusion",
            "this plan authorizes canon promotion",
        ]
        for claim in forbidden_claims:
            assert claim not in lower, f"Plan must not contain: '{claim}'"
