# AFQR-01–20 R1E Formal Completion Review

**Result: PASS.** This independent result is derived from the exact machine comparisons below and remains capable of becoming `fail` on any recorded mismatch, open blocking substrate, or blocking defect.

```json
{
  "review_id": "AFQR-01-20-R1E-FORMAL-COMPLETION-001",
  "phase": "R1E",
  "result": "pass",
  "r1_status": "complete",
  "r1d_status": "complete",
  "metadata": {
    "date": "2026-07-28",
    "review_kind": "independent formal completion gate"
  },
  "verified_repository_baseline": {
    "method": "established local fallback after fetch failed because no origin remote is configured",
    "verified_main_sha": "017984a1598b9c60324c62e54d80372c364654ae",
    "external_baseline_ancestor": true,
    "working_tree_clean_before_branch": true
  },
  "review_authority": "formal doctrine completion review and gate adjudication only",
  "review_nonauthority": [
    "runtime implementation",
    "conversion execution",
    "canon/sourcebook",
    "model behavior",
    "narration",
    "live play",
    "UI behavior",
    "temporary evidence deletion",
    "R2 implementation",
    "RT-002G implementation"
  ],
  "phase_results": {
    "R1A": "complete",
    "R1B": "complete",
    "R1C": "complete",
    "R1D-CORE": "complete",
    "R1D-AGENCY": "complete",
    "R1D-WORLD": "complete",
    "R1D": "complete",
    "R1E": "complete"
  },
  "r1a_completeness": {
    "result": "pass",
    "reviewed_count": 20,
    "records": [
      {
        "afqr_id": "AFQR-01",
        "selected_architecture": "Atomic Typed Transition Journal with Owner-Specific Reducers and Declared Saga Escape Hatches",
        "authoritative_title": "Atomic State Transition, Ownership, Commitment, Recovery, and Replay",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0004"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0004",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md"
        ],
        "title_evidence": [
          "SRC-0004"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0004",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-02",
        "selected_architecture": "Synchronous Command Fast Path with Durable Attempt Escalation",
        "authoritative_title": "Command Identity, Attempts, Retries, Suspension, Escalation, and Durable Progress",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0005"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0005",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md"
        ],
        "title_evidence": [
          "SRC-0005"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0005",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-03",
        "selected_architecture": "Typed Action Gateway with Registered Semantics, Capability-Affordance Composition, and Bounded Plan Verification",
        "authoritative_title": "Action Representation, Capability, Affordance, Method Selection, and Bounded Plans",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0006"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0006",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md"
        ],
        "title_evidence": [
          "SRC-0006"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0006",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-04",
        "selected_architecture": "Profiled Logical-Time Causal Scheduler with Deterministic Resolution Groups and Bounded Cascade Microsteps",
        "authoritative_title": "Logical Time, Simultaneity, Causal Ordering, Scheduled Effects, and Bounded Cascades",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0007"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0007",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md"
        ],
        "title_evidence": [
          "SRC-0007"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0007",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-05",
        "selected_architecture": "Registered Typed Interface-and-Bridge Hypergraph",
        "authoritative_title": "Cross-System Interfaces, Adapters, Bridges, Hyperedges, and Compatibility",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0008"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0008",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md"
        ],
        "title_evidence": [
          "SRC-0008"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0008",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-06",
        "selected_architecture": "Invariant-Gated Typed Claim Arbitration",
        "authoritative_title": "Claim Discovery, Admissibility, Conflict, Arbitration, Choice, and Hidden Evidence",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0009"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0009",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
        ],
        "title_evidence": [
          "SRC-0009"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0009",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-07",
        "selected_architecture": "Typed Balance-Domain Flow Ledger with Proof-Carrying Conversion and Atomic Settlement",
        "authoritative_title": "Cross-Domain Conservation, Conversion Validity, Reservation, Settlement, and Arbitrage Prevention",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0010"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0010",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
        ],
        "title_evidence": [
          "SRC-0010"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0010",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-08",
        "selected_architecture": "Typed Faceted Identity, Continuity, and Lineage Graph with Purpose-Scoped Equivalence",
        "authoritative_title": "Identity, Continuity, Copying, Transformation, Proxyhood, Reinstantiation, Fusion, Fission, and Contextual Equivalence",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0011"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0011",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md"
        ],
        "title_evidence": [
          "SRC-0011"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0011",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-09",
        "selected_architecture": "Registered Typed Dependency-and-Obligation Hypergraph with Version-Pinned Lifecycle Policies and Bounded Causal Propagation",
        "authoritative_title": "Dependency, Revocation, Inheritance, Termination, Migration, Orphaning, and Cascading Consequence",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0012"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0012",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ],
        "title_evidence": [
          "SRC-0012"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0012",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-01",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_01_09_Ratification_Pack_v1_0.zip",
            "sha256": "87c8a6d2504b160ddab001a61a49fda965914eecc1703d3c2a6db75ec7f9c376"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-10",
        "selected_architecture": "Typed Bitemporal Truth–Epistemic Provenance Architecture with Profiled Revision and Visibility-Safe Projection (TTEP-PRV)",
        "authoritative_title": "Epistemic State, Perception, Evidence, Knowledge, Belief, Uncertainty, Secrecy, Deception, Memory, Discovery, and Observer-Relative Truth",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0022"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0022",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
        ],
        "title_evidence": [
          "SRC-0021"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0021",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_10_Ratification_Pack_v1_0.zip::AFQR_10_Ratification_Pack_v1_0/master/Astra_AFQR_10_Master_Ratification_v1_0.md",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_10_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_10_Ratification_Pack_v1_0/master/Astra_AFQR_10_Master_Ratification_v1_0.md",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-02",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_10_Ratification_Pack_v1_0.zip",
            "sha256": "03c28c215ca022360855456365003a6808b37f9bff5c01f1d75caa496fe91252"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-11",
        "selected_architecture": "Registered Purpose-Scoped Agency and Personhood Architecture with Orthogonal Consent-Control Planes, Bitemporal Action-Origin Graphs, and Profiled Responsibility (RPSAP-OCC-BAOG-PR)",
        "authoritative_title": "Agency, Personhood, Consent, Control, Responsibility, Decision Authority, Delegation, Coercion, and Autonomous Action",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0041"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0041",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md"
        ],
        "title_evidence": [
          "SRC-0051"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0051",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip::AFQR_11_Ratification_Pack_v1_0/master/Astra_AFQR_11_Master_Ratification_v1_0.md",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_11_Ratification_Pack_v1_0/master/Astra_AFQR_11_Master_Ratification_v1_0.md",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-03",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip",
            "sha256": "740a35c7b982bceb20b04695a9faa0f7bcd6f0cbc8269a5cce057337d75ff96b"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-12",
        "selected_architecture": "Registered Typed Motivational–Behavioral State Architecture with Bounded Deliberation, Pluggable Plan Interfaces, Profiled Learning, and Bitemporal Continuity (RTMBS-BD-PPI-PL-BTC)",
        "authoritative_title": "Goals, Values, Needs, Drives, Emotion, Personality, Deliberation, Planning, Learning, and Behavioral Continuity",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0072"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0072",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md"
        ],
        "title_evidence": [
          "SRC-0072"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0072",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-04",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_12_Ratification_Pack_v1_0.zip",
            "sha256": "693ee333816a69d9ba054f6f61cdc92b8b89b9c9dd745a6483de047f4b686c3b"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-13",
        "selected_architecture": "Registered Multiplex Social-State Architecture with Domain-Scoped Trust, Audience-Relative Reputation, Modular Culture–Norm Profiles, and Bitemporal Network Continuity (RMSSA-DT-ARR-MCNP-BNC)",
        "authoritative_title": "Social Relationships, Trust, Reputation, Status, Norms, Culture, Affiliation, and Group Dynamics",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0082"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0082",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
        ],
        "title_evidence": [
          "SRC-0093"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0093",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_13_Ratification_Pack_v1_0.zip::AFQR_13_Ratification_Pack_v1_0/master/Astra_AFQR_13_Master_Ratification_v1_0.md",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_13_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_13_Ratification_Pack_v1_0/master/Astra_AFQR_13_Master_Ratification_v1_0.md",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-05",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_13_Ratification_Pack_v1_0.zip",
            "sha256": "dba976f03a39244ed2c09c70b0086345fbf7bcbaa99c3317c5c8d2c01b199356"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-14",
        "selected_architecture": "Registered Bitemporal Communication–Interpretation Architecture with Segmented Signal–Expression–Interpretation Pipelines, Multidimensional Dialogue Acts, Protocol-Governed Conversation State, and Validated Model Realization (RBCIA-SEIP-MDA-PGCS-VMR)",
        "authoritative_title": "Communication Language Meaning Dialogue Acts Conversation State Interpretation Argumentation Persuasion Negotiation and Interaction Protocols",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0103"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0103",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md"
        ],
        "title_evidence": [
          "SRC-0114"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0114",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip::AFQR_14_Ratification_Pack_v1_0/registries/afqr_14_decision_registry.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_14_Ratification_Pack_v1_0/registries/afqr_14_decision_registry.yaml",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [
          "SRC-0103",
          "SRC-0139",
          "SRC-0121"
        ],
        "corrected_baseline_evidence_locators": [
          {
            "evidence_id": "SRC-0103",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0139",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-07/registries/afqr_14_corrected_baseline_note.yaml",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0121",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/tests/artifact_manifest.yaml",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-06",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip",
            "sha256": "f294236502a0ee8edec683af1f223e027add32480c087b2993e927057873564c"
          }
        ],
        "superseded_stale_handling": "The AFQR-14 normative architecture is selected directly from the AFQR-14 package. A validation note packaged in the AFQR-15 ratification archive confirms the normative AFQR-14 files and supersedes reliance only on the stale AFQR-14 artifact manifest; it does not alter AFQR-14’s architectural decision, transfer AFQR-14 ownership, or replace it with AFQR-15 doctrine.",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-15",
        "selected_architecture": "Registered Federated Institutional–Jurisdictional Architecture with Relational Normative Positions, Versioned Rule Materials, Protocol-Governed Adjudication, Profiled Legitimacy, and Separated Enforcement Authorization and Execution (RFIJA-RNP-VRM-PGA-PL-SEA)",
        "authoritative_title": "Institutions Governance Jurisdiction Rights Law Policy Adjudication Legitimacy and Enforcement",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0125"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0125",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
        ],
        "title_evidence": [
          "SRC-0140"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0140",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_15_Ratification_Pack_v1_0(1)(1).zip::AFQR_15_Ratification_Pack_v1_0/registries/afqr_15_decision_registry.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_15_Ratification_Pack_v1_0(1)(1).zip",
            "archive_member_path": "AFQR_15_Ratification_Pack_v1_0/registries/afqr_15_decision_registry.yaml",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-07",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_15_Ratification_Pack_v1_0(1)(1).zip",
            "sha256": "e8af119787a6973e4c1d637684317a86aff24c638c2fb0fb3ea6a03f9064f842"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-16",
        "selected_architecture": "Registered Federated Embodiment–Integrity Architecture with Typed Component–Function–Dependency Graphs, Staged Exposure–Transfer–Effect Pipelines, Profile-Scoped Injury–Condition–Death Families, and Bitemporal Recovery–Transformation Continuity (RFEIA-CFDG-SETE-ICD-BRTC)",
        "authoritative_title": "Bodies Structures Integrity Harm Damage Injury Conditions Impairment Death Recovery Repair Replacement and Transformation",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0152"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0152",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md"
        ],
        "title_evidence": [
          "SRC-0166"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0166",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip::AFQR_16_Ratification_Pack_v1_0/registries/afqr_16_decision_registry.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_16_Ratification_Pack_v1_0/registries/afqr_16_decision_registry.yaml",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-08",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip",
            "sha256": "b4207bbf04e7039bd7ac4402528fa1f50003f0471ce869bfd63823ac4de09f74"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-17",
        "selected_architecture": "Registered Federated Environment–Process Architecture with Typed Region–Medium–Field Ownership, Bounded Source–Transport–Hazard Graphs, Profile-Scoped Terrain–Weather–Ecology Families, and Bitemporal Observation–Materialization Continuity (RFEPA-RMF-STHG-TWE-OMC)",
        "authoritative_title": "Environment, Media, Atmosphere, Weather, Terrain, Hazards, Contamination, Exposure, Ecological Processes, and Environmental Change",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0180"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0180",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md"
        ],
        "title_evidence": [
          "SRC-0192"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0192",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_17_Ratification_Pack_v1_0.zip::AFQR_17_Ratification_Pack_v1_0/master/Astra_AFQR_17_Master_Ratification_v1_0.md",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_17_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_17_Ratification_Pack_v1_0/master/Astra_AFQR_17_Master_Ratification_v1_0.md",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-09",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_17_Ratification_Pack_v1_0.zip",
            "sha256": "cb37f734e2b87f10e3a36e3fe76923cd731a3224094ebae0b43d27901dc2281f"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-18",
        "selected_architecture": "Registered Federated Spatiotemporal Topology Architecture with Typed Domain–Frame–Support Ownership, Plural Metric–Reachability Profiles, Atomic Movement–Occupancy Transitions, and Bitemporal Map–Materialization Continuity (RFSTA-DFS-PMR-AMO-MMC)",
        "authoritative_title": "Space, Location, Position, Scale, Boundaries, Distance, Proximity, Reachability, Movement, Navigation, and Spatial Topology",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0207"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0207",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md"
        ],
        "title_evidence": [
          "SRC-0220"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0220",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_18_Ratification_Pack_v1_0.zip::AFQR_18_Ratification_Pack_v1_0/master/Astra_AFQR_18_Master_Ratification_v1_0.md",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_18_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_18_Ratification_Pack_v1_0/master/Astra_AFQR_18_Master_Ratification_v1_0.md",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-10",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_18_Ratification_Pack_v1_0.zip",
            "sha256": "fc2b0194d4574f9f51196a838727de64e37a5b2906a12eba73a73e2b883c5ca4"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-19",
        "selected_architecture": "Registered Federated Capability–Opportunity–Targeting–Resolution Architecture with Typed Readiness–Eligibility Closure, Pluggable Deterministic/Stochastic Resolvers, Bounded Trigger–Reaction Partial Orders, and Owner-Prepared Multi-Domain Effect Commitments",
        "authoritative_title": "Capabilities, Opportunities, Targeting, Contests, Reactions, Interrupts, Conflict, Combat, and Multi-Actor Action Resolution",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0231"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0231",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md"
        ],
        "title_evidence": [
          "SRC-0244"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0244",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_19_Ratification_Pack_v1_0.zip::AFQR_19_Ratification_Pack_v1_0/master/Astra_AFQR_19_Master_Ratification_v1_0.md",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_19_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_19_Ratification_Pack_v1_0/master/Astra_AFQR_19_Master_Ratification_v1_0.md",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-11",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_19_Ratification_Pack_v1_0.zip",
            "sha256": "222f67cac5ab0b88f3d525fa3d84fe99ea79637fed6a5b30388b8acd0db857e5"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      },
      {
        "afqr_id": "AFQR-20",
        "selected_architecture": "Registered Federated Signal–Sensing–Acquisition Architecture with Typed Source–Modality–Propagation Ownership, Staged Exposure–Acquisition–Detection–Recognition Pipelines, Observer-Relative Concealment–Countermeasure Profiles, and Bitemporal Contact–Track–Evidence Continuity",
        "authoritative_title": "Signals Sensing Attention Perception Detection Recognition Search Concealment Stealth Tracking Surveillance and Information Acquisition",
        "decision_status": "accepted_architectural_decision",
        "source_evidence_identifiers": [
          "SRC-0255"
        ],
        "source_evidence_locators": [
          {
            "evidence_id": "SRC-0255",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md",
            "path_kind": "materialized_normalized_file"
          }
        ],
        "source_packet_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
        ],
        "title_evidence": [
          "SRC-0270"
        ],
        "title_evidence_locators": [
          {
            "evidence_id": "SRC-0270",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_20_Ratification_Pack_v1_0.zip::AFQR_20_Ratification_Pack_v1_0/registries/afqr_20_decision_registry.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_20_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_20_Ratification_Pack_v1_0/registries/afqr_20_decision_registry.yaml",
            "path_kind": "manifest_archive_member"
          }
        ],
        "corrected_baseline_evidence": [],
        "corrected_baseline_evidence_locators": [],
        "archive_provenance": [
          {
            "archive_record_id": "ARCH-12",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_20_Ratification_Pack_v1_0.zip",
            "sha256": "e514648bad084b26d01f54f7e79c3cd62c7e9243c081d6aa2fe3bc3c1a102363"
          }
        ],
        "superseded_stale_handling": "not_applicable",
        "duplicate_authority_status": "none_unresolved",
        "result": "pass",
        "mismatches": []
      }
    ],
    "afqr_14_provenance": {
      "architecture_owner": "AFQR-14",
      "primary_source": "SRC-0103",
      "title_evidence": [
        "SRC-0114"
      ],
      "corrected_baseline_evidence": [
        "SRC-0103",
        "SRC-0139",
        "SRC-0121"
      ],
      "packaging_rule": "AFQR-15 packaging validates AFQR-14 files and does not transfer ownership"
    }
  },
  "r1b_completeness": {
    "result": "pass",
    "actual_term_count": 41,
    "review_records": [
      {
        "term_id": "TERM-001",
        "normalized_root": "state",
        "canonical_form": "state",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "epistemic state",
            "definition": "Observer-relative epistemic state governed as separately owned, versioned, append-only epistemic posture.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-10",
            "owner_evidence_records": [
              "SRC-0022"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
            ],
            "owner_evidence_rationale": "AFQR-10 explicitly owns observer-relative epistemic state and its provenance; AFQR-01 commitment does not own those semantics."
          },
          {
            "qualified_form": "social state",
            "definition": "Federated, purpose- and profile-scoped social state.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-13",
            "owner_evidence_records": [
              "SRC-0082"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
            ],
            "owner_evidence_rationale": "AFQR-13 explicitly defines social state as federated and profile-scoped."
          },
          {
            "qualified_form": "environmental state",
            "definition": "Federated environmental state governed by declared environmental state owners.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-17",
            "owner_evidence_records": [
              "SRC-0180"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md"
            ],
            "owner_evidence_rationale": "AFQR-17 explicitly introduces federated environmental state owners and environmental state mutation boundaries."
          }
        ],
        "explicit_nonowners": [
          "AFQR-04"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "state as synonym for truth",
          "state as synonym for transition",
          "state as synonym for transaction",
          "state as synonym for event"
        ],
        "explicit_non_equivalences": [
          "event",
          "transaction",
          "transition",
          "truth"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0035",
          "SRC-0149"
        ],
        "collision_membership": [
          "COLL-01"
        ],
        "authoritative_record_sha256": "6d942e48eed16c0d9e0f325f9c0460793bc2da5878e73d7858e21157429c4821",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-002",
        "normalized_root": "truth",
        "canonical_form": "truth",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "authoritative world truth",
            "definition": "AFQR-10 explicitly separates and owns authoritative world truth.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-10",
            "owner_evidence_records": [
              "SRC-0022"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
            ],
            "owner_evidence_rationale": "AFQR-10 explicitly separates and owns authoritative world truth."
          },
          {
            "qualified_form": "observer-relative truth",
            "definition": "AFQR-10 explicitly governs observer-relative epistemic truth posture.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-10",
            "owner_evidence_records": [
              "SRC-0022"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
            ],
            "owner_evidence_rationale": "AFQR-10 explicitly governs observer-relative epistemic truth posture."
          }
        ],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-04",
          "AFQR-17"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "truth as synonym for state",
          "truth as synonym for transition",
          "truth as synonym for transaction",
          "truth as synonym for event"
        ],
        "explicit_non_equivalences": [
          "event",
          "state",
          "transaction",
          "transition"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0035",
          "SRC-0149"
        ],
        "collision_membership": [
          "COLL-01"
        ],
        "authoritative_record_sha256": "3c7ea5469aa3be25679b56314d6985fe84f959bd1b99b084f2834027c7c18760",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-003",
        "normalized_root": "transition",
        "canonical_form": "transition",
        "owner_kind": "afqr",
        "owner_id": "AFQR-01",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-04",
          "AFQR-10",
          "AFQR-12",
          "AFQR-17",
          "AFQR-18"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "transition as synonym for state",
          "transition as synonym for truth",
          "transition as synonym for transaction",
          "transition as synonym for event"
        ],
        "explicit_non_equivalences": [
          "causality",
          "event",
          "process",
          "state",
          "time",
          "transaction",
          "truth"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0007",
          "SRC-0035",
          "SRC-0092",
          "SRC-0149",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-01",
          "COLL-06"
        ],
        "authoritative_record_sha256": "f2f1d677329507baa7b3838aa13cd9511b5f03a5496d7203b6365ed9183502a1",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-004",
        "normalized_root": "transaction",
        "canonical_form": "transaction",
        "owner_kind": "afqr",
        "owner_id": "AFQR-01",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-10",
          "AFQR-17"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "transaction as synonym for state",
          "transaction as synonym for truth",
          "transaction as synonym for transition",
          "transaction as synonym for event"
        ],
        "explicit_non_equivalences": [
          "event",
          "state",
          "transition",
          "truth"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0035",
          "SRC-0149"
        ],
        "collision_membership": [
          "COLL-01"
        ],
        "authoritative_record_sha256": "e6bdc784cdcca78719d2cda9336914563b526fd92a2c5ce79677044ea9eacc7d",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-005",
        "normalized_root": "event",
        "canonical_form": "event",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "committed event receipt",
            "definition": "AFQR-01 explicitly owns append-only committed transition and event receipts.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-01",
            "owner_evidence_records": [
              "SRC-0004"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md"
            ],
            "owner_evidence_rationale": "AFQR-01 explicitly owns append-only committed transition and event receipts."
          },
          {
            "qualified_form": "scheduled effect",
            "definition": "AFQR-04 explicitly owns scheduled effects and their logical-time placement; this does not own committed events.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-04",
            "owner_evidence_records": [
              "SRC-0007"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md"
            ],
            "owner_evidence_rationale": "AFQR-04 explicitly owns scheduled effects and their logical-time placement; this does not own committed events."
          }
        ],
        "explicit_nonowners": [
          "AFQR-10",
          "AFQR-17"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "event as synonym for state",
          "event as synonym for truth",
          "event as synonym for transition",
          "event as synonym for transaction"
        ],
        "explicit_non_equivalences": [
          "state",
          "transaction",
          "transition",
          "truth"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0035",
          "SRC-0149"
        ],
        "collision_membership": [
          "COLL-01"
        ],
        "authoritative_record_sha256": "8016ac29ea1e5b1c7c6417b8aa05a0bd5c7a292e03a67a362843e2a87d36912c",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-006",
        "normalized_root": "command",
        "canonical_form": "command",
        "owner_kind": "afqr",
        "owner_id": "AFQR-02",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-03",
          "AFQR-19"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "command as synonym for attempt",
          "command as synonym for action",
          "command as synonym for capability",
          "command as synonym for opportunity"
        ],
        "explicit_non_equivalences": [
          "action",
          "attempt",
          "capability",
          "opportunity",
          "resolution",
          "target"
        ],
        "source_evidence": [
          "SRC-0005",
          "SRC-0006",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-02"
        ],
        "authoritative_record_sha256": "a990718615d1dca67063daa61fa069d56372718261005edb659486bab0d14b84",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-007",
        "normalized_root": "attempt",
        "canonical_form": "attempt",
        "owner_kind": "afqr",
        "owner_id": "AFQR-02",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-03",
          "AFQR-19"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "attempt as synonym for command",
          "attempt as synonym for action",
          "attempt as synonym for capability",
          "attempt as synonym for opportunity"
        ],
        "explicit_non_equivalences": [
          "action",
          "capability",
          "command",
          "opportunity",
          "resolution",
          "target"
        ],
        "source_evidence": [
          "SRC-0005",
          "SRC-0006",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-02"
        ],
        "authoritative_record_sha256": "0c2882c40f7338bcc635275874c8622c820021b283992bd7995b0ebc618c0239",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-008",
        "normalized_root": "action",
        "canonical_form": "action",
        "owner_kind": "afqr",
        "owner_id": "AFQR-03",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-02",
          "AFQR-19"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "action as synonym for command",
          "action as synonym for attempt",
          "action as synonym for capability",
          "action as synonym for opportunity"
        ],
        "explicit_non_equivalences": [
          "attempt",
          "capability",
          "command",
          "opportunity",
          "resolution",
          "target"
        ],
        "source_evidence": [
          "SRC-0005",
          "SRC-0006",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-02"
        ],
        "authoritative_record_sha256": "5e9a67a403e0e48164f6686239f0072a3d712bac4268958235fcdd8ec691d86c",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-009",
        "normalized_root": "capability",
        "canonical_form": "capability",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "action-route capability requirement",
            "definition": "AFQR-03 explicitly owns CapabilityRequirement in registered action-route composition.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-03",
            "owner_evidence_records": [
              "SRC-0006"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md"
            ],
            "owner_evidence_rationale": "AFQR-03 explicitly owns CapabilityRequirement in registered action-route composition."
          },
          {
            "qualified_form": "capability readiness determination",
            "definition": "AFQR-19 explicitly owns capability readiness determinations.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-19",
            "owner_evidence_records": [
              "SRC-0231"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md"
            ],
            "owner_evidence_rationale": "AFQR-19 explicitly owns capability readiness determinations."
          }
        ],
        "explicit_nonowners": [
          "AFQR-02"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "capability as synonym for command",
          "capability as synonym for attempt",
          "capability as synonym for action",
          "capability as synonym for opportunity"
        ],
        "explicit_non_equivalences": [
          "action",
          "attempt",
          "command",
          "opportunity",
          "resolution",
          "target"
        ],
        "source_evidence": [
          "SRC-0005",
          "SRC-0006",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-02"
        ],
        "authoritative_record_sha256": "cc008c64b2ded81eb63067b1e03d5bba52d34a0a324af30a7e477f931a2dee1f",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-010",
        "normalized_root": "opportunity",
        "canonical_form": "opportunity",
        "owner_kind": "afqr",
        "owner_id": "AFQR-19",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-02"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "opportunity as synonym for command",
          "opportunity as synonym for attempt",
          "opportunity as synonym for action",
          "opportunity as synonym for capability"
        ],
        "explicit_non_equivalences": [
          "action",
          "attempt",
          "capability",
          "command",
          "resolution",
          "target"
        ],
        "source_evidence": [
          "SRC-0005",
          "SRC-0006",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-02"
        ],
        "authoritative_record_sha256": "00d1dc0fe8af7a489681dd9c52f49bf914bbcd20e7397c7473893644a4dd9ef6",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-011",
        "normalized_root": "target",
        "canonical_form": "target",
        "owner_kind": "afqr",
        "owner_id": "AFQR-19",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-02",
          "AFQR-03"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "target as synonym for command",
          "target as synonym for attempt",
          "target as synonym for action",
          "target as synonym for capability"
        ],
        "explicit_non_equivalences": [
          "action",
          "attempt",
          "capability",
          "command",
          "opportunity",
          "resolution"
        ],
        "source_evidence": [
          "SRC-0005",
          "SRC-0006",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-02"
        ],
        "authoritative_record_sha256": "fe9f03d67e156da5ce166dc6d4e9c28ae26cfb9cc7ba470b68ebffb54123057b",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-012",
        "normalized_root": "resolution",
        "canonical_form": "resolution",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "action resolution",
            "definition": "AFQR-19 explicitly owns resolver selection, execution receipts, and action resolution candidates.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-19",
            "owner_evidence_records": [
              "SRC-0231"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md"
            ],
            "owner_evidence_rationale": "AFQR-19 explicitly owns resolver selection, execution receipts, and action resolution candidates."
          },
          {
            "qualified_form": "claim arbitration result",
            "definition": "AFQR-06 explicitly owns claim arbitration and its typed result/evidence.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-06",
            "owner_evidence_records": [
              "SRC-0009"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
            ],
            "owner_evidence_rationale": "AFQR-06 explicitly owns claim arbitration and its typed result/evidence."
          },
          {
            "qualified_form": "resolution group",
            "definition": "AFQR-04 explicitly owns deterministic resolution groups; a group is not an action result.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-04",
            "owner_evidence_records": [
              "SRC-0007"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md"
            ],
            "owner_evidence_rationale": "AFQR-04 explicitly owns deterministic resolution groups; a group is not an action result."
          }
        ],
        "explicit_nonowners": [
          "AFQR-02",
          "AFQR-03"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "resolution as synonym for command",
          "resolution as synonym for attempt",
          "resolution as synonym for action",
          "resolution as synonym for capability"
        ],
        "explicit_non_equivalences": [
          "action",
          "attempt",
          "capability",
          "command",
          "opportunity",
          "target"
        ],
        "source_evidence": [
          "SRC-0005",
          "SRC-0006",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-02"
        ],
        "authoritative_record_sha256": "606cc933b383ae99d9a237938d9381a1c8a98a7e65b5fef2a152123ebf93d84d",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-013",
        "normalized_root": "identity",
        "canonical_form": "identity",
        "owner_kind": "afqr",
        "owner_id": "AFQR-08",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-11",
          "AFQR-15"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "identity as synonym for owner",
          "identity as synonym for authority",
          "identity as synonym for agency",
          "identity as synonym for responsibility"
        ],
        "explicit_non_equivalences": [
          "agency",
          "authority",
          "owner",
          "responsibility"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0011",
          "SRC-0059",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-03"
        ],
        "authoritative_record_sha256": "a5c8ad459f21b621853aff2403fdb06f5f675cdd27dfe434fef67f0c6bb6bc87",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-014",
        "normalized_root": "owner",
        "canonical_form": "owner",
        "owner_kind": "unresolved_escalation",
        "owner_id": "Doctrine Council",
        "qualified_forms": [
          {
            "qualified_form": "state owner",
            "definition": "AFQR-01 explicitly defines exclusive state/write owners and owner-specific reducers.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-01",
            "owner_evidence_records": [
              "SRC-0004"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md"
            ],
            "owner_evidence_rationale": "AFQR-01 explicitly defines exclusive state/write owners and owner-specific reducers."
          }
        ],
        "explicit_nonowners": [
          "AFQR-08",
          "AFQR-11",
          "AFQR-15"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "owner as synonym for identity",
          "owner as synonym for authority",
          "owner as synonym for agency",
          "owner as synonym for responsibility"
        ],
        "explicit_non_equivalences": [
          "agency",
          "authority",
          "identity",
          "responsibility"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0011",
          "SRC-0059",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-03"
        ],
        "authoritative_record_sha256": "7ca24a030d57c05a7924696fae3ebe7be2809b8b3427376db528eb918fd78780",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-015",
        "normalized_root": "authority",
        "canonical_form": "authority",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "project authority",
            "definition": "Current project governance controls phase and doctrine authority; this is not domain authority.",
            "owner_kind": "project_governance",
            "owner_id": "Astra Doctrine Council",
            "owner_evidence_records": [],
            "owner_evidence_paths": [
              "docs/doctrine/control/afqr_01_20_consolidation_program_plan.md"
            ],
            "owner_evidence_rationale": "Current project governance controls phase and doctrine authority; this is not domain authority."
          },
          {
            "qualified_form": "institutional authority",
            "definition": "AFQR-15 explicitly governs institutional authority and jurisdiction.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-15",
            "owner_evidence_records": [
              "SRC-0125"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
            ],
            "owner_evidence_rationale": "AFQR-15 explicitly governs institutional authority and jurisdiction."
          },
          {
            "qualified_form": "governed-relation authority record",
            "definition": "AFQR-09 explicitly owns authority records on governed persistent relations.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-09",
            "owner_evidence_records": [
              "SRC-0012"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
            ],
            "owner_evidence_rationale": "AFQR-09 explicitly owns authority records on governed persistent relations."
          }
        ],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-08",
          "AFQR-11",
          "AFQR-13"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "authority as synonym for identity",
          "authority as synonym for owner",
          "authority as synonym for agency",
          "authority as synonym for responsibility"
        ],
        "explicit_non_equivalences": [
          "agency",
          "identity",
          "institution",
          "jurisdiction",
          "owner",
          "responsibility",
          "social state"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0011",
          "SRC-0012",
          "SRC-0059",
          "SRC-0110",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-03",
          "COLL-08"
        ],
        "authoritative_record_sha256": "87fbc6965b35b5cb4b67a294f8fddc939890ca2309b229eae1076d3c3c3abd7f",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-016",
        "normalized_root": "agency",
        "canonical_form": "agency",
        "owner_kind": "afqr",
        "owner_id": "AFQR-11",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-08",
          "AFQR-12",
          "AFQR-13",
          "AFQR-15"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "agency as synonym for identity",
          "agency as synonym for owner",
          "agency as synonym for authority",
          "agency as synonym for responsibility"
        ],
        "explicit_non_equivalences": [
          "authority",
          "behavior",
          "identity",
          "motivation",
          "owner",
          "responsibility",
          "social state"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0011",
          "SRC-0059",
          "SRC-0092",
          "SRC-0110",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-03",
          "COLL-10"
        ],
        "authoritative_record_sha256": "d327fc19db0ec4d2fce43719415fe292811cd23336efea7c086a26151c272735",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-017",
        "normalized_root": "responsibility",
        "canonical_form": "responsibility",
        "owner_kind": "afqr",
        "owner_id": "AFQR-11",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-08",
          "AFQR-12",
          "AFQR-13",
          "AFQR-15"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "responsibility as synonym for identity",
          "responsibility as synonym for owner",
          "responsibility as synonym for authority",
          "responsibility as synonym for agency"
        ],
        "explicit_non_equivalences": [
          "agency",
          "authority",
          "behavior",
          "identity",
          "motivation",
          "owner",
          "social state"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0011",
          "SRC-0059",
          "SRC-0092",
          "SRC-0110",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-03",
          "COLL-10"
        ],
        "authoritative_record_sha256": "9683832e8efa7be99ad28e7957a8a56cfc93adec889370f9191ed93fcd3fa01e",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-018",
        "normalized_root": "claim",
        "canonical_form": "claim",
        "owner_kind": "afqr",
        "owner_id": "AFQR-06",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-10",
          "AFQR-20"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "claim as synonym for evidence",
          "claim as synonym for belief",
          "claim as synonym for knowledge",
          "claim as synonym for observation"
        ],
        "explicit_non_equivalences": [
          "belief",
          "evidence",
          "knowledge",
          "observation"
        ],
        "source_evidence": [
          "SRC-0009",
          "SRC-0035",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-04"
        ],
        "authoritative_record_sha256": "defaba2b668edc283b4a9411d08f0fbe7c23068e2683dd775fc270ff55ff0f42",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-019",
        "normalized_root": "evidence",
        "canonical_form": "evidence",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "arbitration evidence",
            "definition": "AFQR-06 explicitly produces evidence from claim arbitration.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-06",
            "owner_evidence_records": [
              "SRC-0009"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
            ],
            "owner_evidence_rationale": "AFQR-06 explicitly produces evidence from claim arbitration."
          },
          {
            "qualified_form": "epistemic evidence record",
            "definition": "AFQR-10 explicitly owns immutable typed epistemic evidence records.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-10",
            "owner_evidence_records": [
              "SRC-0022"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
            ],
            "owner_evidence_rationale": "AFQR-10 explicitly owns immutable typed epistemic evidence records."
          },
          {
            "qualified_form": "sensing evidence candidate",
            "definition": "AFQR-20 explicitly produces evidence candidates only for AFQR-10/19 acceptance.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-20",
            "owner_evidence_records": [
              "SRC-0255"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
            ],
            "owner_evidence_rationale": "AFQR-20 explicitly produces evidence candidates only for AFQR-10/19 acceptance."
          }
        ],
        "explicit_nonowners": [],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "evidence as synonym for claim",
          "evidence as synonym for belief",
          "evidence as synonym for knowledge",
          "evidence as synonym for observation"
        ],
        "explicit_non_equivalences": [
          "belief",
          "claim",
          "knowledge",
          "observation"
        ],
        "source_evidence": [
          "SRC-0009",
          "SRC-0035",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-04"
        ],
        "authoritative_record_sha256": "6faf7204c29828fa396dacdeac884946f7bbb199e6cc007d50667837c3bf2df9",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-020",
        "normalized_root": "belief",
        "canonical_form": "belief",
        "owner_kind": "afqr",
        "owner_id": "AFQR-10",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-06",
          "AFQR-20"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "belief as synonym for claim",
          "belief as synonym for evidence",
          "belief as synonym for knowledge",
          "belief as synonym for observation"
        ],
        "explicit_non_equivalences": [
          "claim",
          "evidence",
          "knowledge",
          "observation"
        ],
        "source_evidence": [
          "SRC-0009",
          "SRC-0035",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-04"
        ],
        "authoritative_record_sha256": "c85c88a4210c9dcc38bc4fa09268a4e6c55e24f97f0250b88f3dbd073e944e4f",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-021",
        "normalized_root": "knowledge",
        "canonical_form": "knowledge",
        "owner_kind": "afqr",
        "owner_id": "AFQR-10",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-06",
          "AFQR-20"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "knowledge as synonym for claim",
          "knowledge as synonym for evidence",
          "knowledge as synonym for belief",
          "knowledge as synonym for observation"
        ],
        "explicit_non_equivalences": [
          "belief",
          "claim",
          "evidence",
          "observation"
        ],
        "source_evidence": [
          "SRC-0009",
          "SRC-0035",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-04"
        ],
        "authoritative_record_sha256": "b9be8620783826f788aee40b63718a192d7e52eb4d30dcfa654f5b9122a4c516",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-022",
        "normalized_root": "observation",
        "canonical_form": "observation",
        "owner_kind": "shared_qualified_family",
        "owner_id": "R1B shared vocabulary",
        "qualified_forms": [
          {
            "qualified_form": "sensing observation candidate",
            "definition": "AFQR-20 explicitly produces observation candidates only.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-20",
            "owner_evidence_records": [
              "SRC-0255"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
            ],
            "owner_evidence_rationale": "AFQR-20 explicitly produces observation candidates only."
          },
          {
            "qualified_form": "epistemic observation record",
            "definition": "AFQR-10 explicitly owns immutable observation records and epistemic provenance.",
            "owner_kind": "afqr",
            "owner_id": "AFQR-10",
            "owner_evidence_records": [
              "SRC-0022"
            ],
            "owner_evidence_paths": [
              "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
            ],
            "owner_evidence_rationale": "AFQR-10 explicitly owns immutable observation records and epistemic provenance."
          }
        ],
        "explicit_nonowners": [
          "AFQR-06",
          "AFQR-14"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "observation as synonym for claim",
          "observation as synonym for evidence",
          "observation as synonym for belief",
          "observation as synonym for knowledge"
        ],
        "explicit_non_equivalences": [
          "belief",
          "claim",
          "communication",
          "evidence",
          "interpretation",
          "knowledge",
          "signal"
        ],
        "source_evidence": [
          "SRC-0009",
          "SRC-0035",
          "SRC-0130",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-04",
          "COLL-07"
        ],
        "authoritative_record_sha256": "208d407816e5c0ebc581c04efb895b50724663b1dac4ed035dc049a7125a7c17",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-023",
        "normalized_root": "relation",
        "canonical_form": "relation",
        "owner_kind": "afqr",
        "owner_id": "AFQR-09",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-05",
          "AFQR-16"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "relation as synonym for dependency",
          "relation as synonym for obligation",
          "relation as synonym for integrity"
        ],
        "explicit_non_equivalences": [
          "dependency",
          "integrity",
          "obligation"
        ],
        "source_evidence": [
          "SRC-0008",
          "SRC-0012",
          "SRC-0184"
        ],
        "collision_membership": [
          "COLL-05"
        ],
        "authoritative_record_sha256": "9e16f1af70fbb31f911d741839a21300fd7f524d5fef47cd08c43768c4883bfb",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-024",
        "normalized_root": "dependency",
        "canonical_form": "dependency",
        "owner_kind": "afqr",
        "owner_id": "AFQR-09",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-16"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "dependency as synonym for relation",
          "dependency as synonym for obligation",
          "dependency as synonym for integrity"
        ],
        "explicit_non_equivalences": [
          "integrity",
          "obligation",
          "relation"
        ],
        "source_evidence": [
          "SRC-0008",
          "SRC-0012",
          "SRC-0184"
        ],
        "collision_membership": [
          "COLL-05"
        ],
        "authoritative_record_sha256": "4d74a14f911f6ddc38407f4a8da0476ac62987d1243afdfc08c8a2653231075f",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-025",
        "normalized_root": "obligation",
        "canonical_form": "obligation",
        "owner_kind": "afqr",
        "owner_id": "AFQR-09",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-05",
          "AFQR-16"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "obligation as synonym for relation",
          "obligation as synonym for dependency",
          "obligation as synonym for integrity"
        ],
        "explicit_non_equivalences": [
          "dependency",
          "integrity",
          "relation"
        ],
        "source_evidence": [
          "SRC-0008",
          "SRC-0012",
          "SRC-0184"
        ],
        "collision_membership": [
          "COLL-05"
        ],
        "authoritative_record_sha256": "75586cd97f14d111b32d007bed467edab0bf755f8f2a46c57c7589d2b7f42b02",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-026",
        "normalized_root": "integrity",
        "canonical_form": "integrity",
        "owner_kind": "afqr",
        "owner_id": "AFQR-16",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-05",
          "AFQR-09",
          "AFQR-17",
          "AFQR-18"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "integrity as synonym for relation",
          "integrity as synonym for dependency",
          "integrity as synonym for obligation",
          "integrity as synonym for embodiment"
        ],
        "explicit_non_equivalences": [
          "dependency",
          "embodiment",
          "environment",
          "obligation",
          "relation",
          "space",
          "topology"
        ],
        "source_evidence": [
          "SRC-0008",
          "SRC-0012",
          "SRC-0184",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-05",
          "COLL-09"
        ],
        "authoritative_record_sha256": "3440b8bdf3cfcae2b4dea71cdbdf0e9bbdbff88a5ffcbea5a6b988ff4cccd2d3",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-027",
        "normalized_root": "time",
        "canonical_form": "time",
        "owner_kind": "afqr",
        "owner_id": "AFQR-04",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-12",
          "AFQR-17",
          "AFQR-18"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "time as synonym for transition",
          "time as synonym for causality",
          "time as synonym for process"
        ],
        "explicit_non_equivalences": [
          "causality",
          "process",
          "transition"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0007",
          "SRC-0092",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-06"
        ],
        "authoritative_record_sha256": "3b1b092d9c6f031023e72314da03f71a796267c9fdb194f7476b33cc23195b91",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-028",
        "normalized_root": "causality",
        "canonical_form": "causality",
        "owner_kind": "afqr",
        "owner_id": "AFQR-04",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-12",
          "AFQR-17",
          "AFQR-18"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "causality as synonym for transition",
          "causality as synonym for time",
          "causality as synonym for process"
        ],
        "explicit_non_equivalences": [
          "process",
          "time",
          "transition"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0007",
          "SRC-0092",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-06"
        ],
        "authoritative_record_sha256": "79341b22925356d55e62a36e0d0fe4bfb94158a7baef902564939ebb8e3a4c10",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-029",
        "normalized_root": "process",
        "canonical_form": "process",
        "owner_kind": "afqr",
        "owner_id": "AFQR-17",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-01",
          "AFQR-04",
          "AFQR-12",
          "AFQR-18"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "process as synonym for transition",
          "process as synonym for time",
          "process as synonym for causality"
        ],
        "explicit_non_equivalences": [
          "causality",
          "time",
          "transition"
        ],
        "source_evidence": [
          "SRC-0004",
          "SRC-0007",
          "SRC-0092",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-06"
        ],
        "authoritative_record_sha256": "f5237a3ec21b9849c725f9c11e12cb970a71eaadeeb049aa8bfb4e6c2bb099ac",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-030",
        "normalized_root": "signal",
        "canonical_form": "signal",
        "owner_kind": "afqr",
        "owner_id": "AFQR-20",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-10",
          "AFQR-14"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "signal as synonym for observation",
          "signal as synonym for communication",
          "signal as synonym for interpretation"
        ],
        "explicit_non_equivalences": [
          "communication",
          "interpretation",
          "observation"
        ],
        "source_evidence": [
          "SRC-0035",
          "SRC-0130",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-07"
        ],
        "authoritative_record_sha256": "6803f9d4cfa08264d62eb5c21a6c79b2cda3bd40b021d28833ee3178d1fd1b9b",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-031",
        "normalized_root": "communication",
        "canonical_form": "communication",
        "owner_kind": "afqr",
        "owner_id": "AFQR-14",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-10",
          "AFQR-20"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "communication as synonym for observation",
          "communication as synonym for signal",
          "communication as synonym for interpretation"
        ],
        "explicit_non_equivalences": [
          "interpretation",
          "observation",
          "signal"
        ],
        "source_evidence": [
          "SRC-0035",
          "SRC-0130",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-07"
        ],
        "authoritative_record_sha256": "df0c27ccaa676f873350316e3e2d9a82d9beec30d14e869d273f61fd799d0a97",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-032",
        "normalized_root": "interpretation",
        "canonical_form": "interpretation",
        "owner_kind": "afqr",
        "owner_id": "AFQR-14",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-10",
          "AFQR-20"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "interpretation as synonym for observation",
          "interpretation as synonym for signal",
          "interpretation as synonym for communication"
        ],
        "explicit_non_equivalences": [
          "communication",
          "observation",
          "signal"
        ],
        "source_evidence": [
          "SRC-0035",
          "SRC-0130",
          "SRC-0255"
        ],
        "collision_membership": [
          "COLL-07"
        ],
        "authoritative_record_sha256": "27033cf262f022aee61afc5c98e752833a5d13c2dd4ba7aa3dbb0cd681a460f0",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-033",
        "normalized_root": "jurisdiction",
        "canonical_form": "jurisdiction",
        "owner_kind": "afqr",
        "owner_id": "AFQR-15",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-09",
          "AFQR-13"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "jurisdiction as synonym for authority",
          "jurisdiction as synonym for institution",
          "jurisdiction as synonym for social state"
        ],
        "explicit_non_equivalences": [
          "authority",
          "institution",
          "social state"
        ],
        "source_evidence": [
          "SRC-0012",
          "SRC-0110",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-08"
        ],
        "authoritative_record_sha256": "99aa1d6d5b9dd7b445d5b1330f9b86f30b476ad0bfc6ce4d8cb55a30dd60e802",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-034",
        "normalized_root": "institution",
        "canonical_form": "institution",
        "owner_kind": "afqr",
        "owner_id": "AFQR-15",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-09",
          "AFQR-13"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "institution as synonym for authority",
          "institution as synonym for jurisdiction",
          "institution as synonym for social state"
        ],
        "explicit_non_equivalences": [
          "authority",
          "jurisdiction",
          "social state"
        ],
        "source_evidence": [
          "SRC-0012",
          "SRC-0110",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-08"
        ],
        "authoritative_record_sha256": "c5e7d8e87566f7fe07b2c673dd756bc336accfdec86ed493b645e03c5433f36c",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-035",
        "normalized_root": "social state",
        "canonical_form": "social state",
        "owner_kind": "afqr",
        "owner_id": "AFQR-13",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-09",
          "AFQR-11",
          "AFQR-12",
          "AFQR-15"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "social state as synonym for authority",
          "social state as synonym for agency",
          "social state as synonym for responsibility",
          "social state as synonym for jurisdiction"
        ],
        "explicit_non_equivalences": [
          "agency",
          "authority",
          "behavior",
          "institution",
          "jurisdiction",
          "motivation",
          "responsibility"
        ],
        "source_evidence": [
          "SRC-0012",
          "SRC-0059",
          "SRC-0092",
          "SRC-0110",
          "SRC-0157"
        ],
        "collision_membership": [
          "COLL-08",
          "COLL-10"
        ],
        "authoritative_record_sha256": "0b2377d80524a37b3a9e0be385313dade6fa233712414f6921e728f24421c558",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-036",
        "normalized_root": "embodiment",
        "canonical_form": "embodiment",
        "owner_kind": "afqr",
        "owner_id": "AFQR-16",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-17",
          "AFQR-18"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "embodiment as synonym for integrity",
          "embodiment as synonym for environment",
          "embodiment as synonym for space",
          "embodiment as synonym for topology"
        ],
        "explicit_non_equivalences": [
          "environment",
          "integrity",
          "space",
          "topology"
        ],
        "source_evidence": [
          "SRC-0184",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-09"
        ],
        "authoritative_record_sha256": "1555d24ebf43696902997de8970e18dc40842334f0e3d8bcdddea5accba95577",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-037",
        "normalized_root": "environment",
        "canonical_form": "environment",
        "owner_kind": "afqr",
        "owner_id": "AFQR-17",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-16",
          "AFQR-18"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "environment as synonym for integrity",
          "environment as synonym for embodiment",
          "environment as synonym for space",
          "environment as synonym for topology"
        ],
        "explicit_non_equivalences": [
          "embodiment",
          "integrity",
          "space",
          "topology"
        ],
        "source_evidence": [
          "SRC-0184",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-09"
        ],
        "authoritative_record_sha256": "5044de0eb92bee4a647a0ae63fdc618abc17de44a856953ff9bb1beeafa127f7",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-038",
        "normalized_root": "space",
        "canonical_form": "space",
        "owner_kind": "afqr",
        "owner_id": "AFQR-18",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-16",
          "AFQR-17"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "space as synonym for integrity",
          "space as synonym for embodiment",
          "space as synonym for environment",
          "space as synonym for topology"
        ],
        "explicit_non_equivalences": [
          "embodiment",
          "environment",
          "integrity",
          "topology"
        ],
        "source_evidence": [
          "SRC-0184",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-09"
        ],
        "authoritative_record_sha256": "4b43c25f1c7fd85e8127f808e6cf3b3e97ac723c3e3495c6ed1b6c013a6af630",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-039",
        "normalized_root": "topology",
        "canonical_form": "topology",
        "owner_kind": "afqr",
        "owner_id": "AFQR-18",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-16",
          "AFQR-17"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "topology as synonym for integrity",
          "topology as synonym for embodiment",
          "topology as synonym for environment",
          "topology as synonym for space"
        ],
        "explicit_non_equivalences": [
          "embodiment",
          "environment",
          "integrity",
          "space"
        ],
        "source_evidence": [
          "SRC-0184",
          "SRC-0209",
          "SRC-0231"
        ],
        "collision_membership": [
          "COLL-09"
        ],
        "authoritative_record_sha256": "437c5d7cdae940713450d4280409e7113b68077f77a5790c950dd2587cf93671",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-040",
        "normalized_root": "motivation",
        "canonical_form": "motivation",
        "owner_kind": "afqr",
        "owner_id": "AFQR-12",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-11",
          "AFQR-13"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "motivation as synonym for agency",
          "motivation as synonym for responsibility",
          "motivation as synonym for social state",
          "motivation as synonym for behavior"
        ],
        "explicit_non_equivalences": [
          "agency",
          "behavior",
          "responsibility",
          "social state"
        ],
        "source_evidence": [
          "SRC-0059",
          "SRC-0092",
          "SRC-0110"
        ],
        "collision_membership": [
          "COLL-10"
        ],
        "authoritative_record_sha256": "1d934e98a7c74e5f7601ae3533040ccc2802ac3f66198b09f6727440499d38d1",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      },
      {
        "term_id": "TERM-041",
        "normalized_root": "behavior",
        "canonical_form": "behavior",
        "owner_kind": "afqr",
        "owner_id": "AFQR-12",
        "qualified_forms": [],
        "explicit_nonowners": [
          "AFQR-11",
          "AFQR-13"
        ],
        "handoff_only_uses": [],
        "rejected_aliases": [
          "behavior as synonym for agency",
          "behavior as synonym for responsibility",
          "behavior as synonym for social state",
          "behavior as synonym for motivation"
        ],
        "explicit_non_equivalences": [
          "agency",
          "motivation",
          "responsibility",
          "social state"
        ],
        "source_evidence": [
          "SRC-0059",
          "SRC-0092",
          "SRC-0110"
        ],
        "collision_membership": [
          "COLL-10"
        ],
        "authoritative_record_sha256": "852df1dee823612bab24cd956ca9882db43c40a3c151fc101186444ca9e797cc",
        "compared_fields": [
          "term_id",
          "root_term",
          "canonical_form",
          "type_owner",
          "qualified_forms",
          "explicit_nonowners",
          "handoff_only_consumers",
          "disallowed_aliases",
          "explicit_non_equivalences",
          "source_evidence_records",
          "collision_ids"
        ],
        "result": "pass",
        "mismatch_list": []
      }
    ],
    "new_unqualified_owners": [],
    "historical_collisions_rewritten": false,
    "pre_review_open_collisions": [
      "COLL-03",
      "COLL-08",
      "COLL-10"
    ]
  },
  "r1c_completeness": {
    "result": "pass",
    "actual_edge_count": 94,
    "partition_counts": {
      "core_internal": 33,
      "agency_internal": 11,
      "world_internal": 7,
      "core_agency_boundary": 21,
      "core_world_boundary": 17,
      "agency_world_boundary": 5
    },
    "partitions": {
      "core_internal": [
        "DEP-001",
        "DEP-002",
        "DEP-003",
        "DEP-004",
        "DEP-005",
        "DEP-006",
        "DEP-007",
        "DEP-008",
        "DEP-020",
        "DEP-021",
        "DEP-022",
        "DEP-024",
        "DEP-025",
        "DEP-026",
        "DEP-027",
        "DEP-028",
        "DEP-032",
        "DEP-033",
        "DEP-034",
        "DEP-035",
        "DEP-036",
        "DEP-047",
        "DEP-048",
        "DEP-049",
        "DEP-052",
        "DEP-053",
        "DEP-054",
        "DEP-061",
        "DEP-062",
        "DEP-063",
        "DEP-064",
        "DEP-065",
        "DEP-066"
      ],
      "agency_internal": [
        "DEP-072",
        "DEP-073",
        "DEP-074",
        "DEP-075",
        "DEP-076",
        "DEP-080",
        "DEP-081",
        "DEP-082",
        "DEP-083",
        "DEP-085",
        "DEP-086"
      ],
      "world_internal": [
        "DEP-088",
        "DEP-089",
        "DEP-090",
        "DEP-091",
        "DEP-092",
        "DEP-093",
        "DEP-094"
      ],
      "core_agency_boundary": [
        "DEP-009",
        "DEP-010",
        "DEP-011",
        "DEP-012",
        "DEP-013",
        "DEP-014",
        "DEP-037",
        "DEP-038",
        "DEP-039",
        "DEP-040",
        "DEP-041",
        "DEP-050",
        "DEP-051",
        "DEP-055",
        "DEP-056",
        "DEP-057",
        "DEP-058",
        "DEP-059",
        "DEP-067",
        "DEP-068",
        "DEP-069"
      ],
      "core_world_boundary": [
        "DEP-015",
        "DEP-016",
        "DEP-017",
        "DEP-018",
        "DEP-019",
        "DEP-023",
        "DEP-029",
        "DEP-030",
        "DEP-031",
        "DEP-042",
        "DEP-043",
        "DEP-044",
        "DEP-045",
        "DEP-046",
        "DEP-060",
        "DEP-070",
        "DEP-071"
      ],
      "agency_world_boundary": [
        "DEP-077",
        "DEP-078",
        "DEP-079",
        "DEP-084",
        "DEP-087"
      ]
    },
    "edge_reviews": [
      {
        "edge_id": "DEP-001",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-02",
        "authoritative_r1c_record_sha256": "e6c9179aab79aa1f6952091ec8790a579a769f65b83636ef93f422d10b50e5f7",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-001",
            "record_sha256": "8205093416b4ba6cdc359a0c6e430c8d5c7e529086ce1e3f5962f1d237f96577",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-002",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-03",
        "authoritative_r1c_record_sha256": "6cbd0073154f362b07e46da6742193fa1e5b65da43160d425d55136c92d3ee5a",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-002",
            "record_sha256": "9292753358973cc4d0549ed8a6724bd3f131b1a84fbc6f64fce007c220e42f62",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-003",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-04",
        "authoritative_r1c_record_sha256": "c2d3f223acfef6787c9e970436e82adec1a79be2116a0fc55edbbcb9d7ee7e81",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-003",
            "record_sha256": "1c212e245d366ad1c1830ec5586c5341a983ae7b9cec9642d2e7aabba2599c73",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-004",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-05",
        "authoritative_r1c_record_sha256": "cedd3b6210a642abec18b9d0ab523cd0ffd3cec6ee702a312121d0da96c236c2",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-004",
            "record_sha256": "15c192b182b1ce57ae0bc7c8de64c41069600e93a130b364ca39c5526f5b974e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-005",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-06",
        "authoritative_r1c_record_sha256": "d19c566eaa502fdaac8abb4629f4c48ceaaabe8ea5c40adebeaa88ad687c75b0",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-005",
            "record_sha256": "72b6d0074319fff6f2778318ec24ef2e74e06f4be732fd207770c4ff0249e3d6",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-006",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-07",
        "authoritative_r1c_record_sha256": "89d1d78b09ac0e72dc4308a8fa79651cb82c401c52c77035af42b50a36888066",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-006",
            "record_sha256": "061d8a8483d96d596d0dc01def113bfd6df52812e452f8f82f1b3f60d574c067",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-007",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-08",
        "authoritative_r1c_record_sha256": "65b9a93ebdef9ab896b4bd1c53bf5e6d88c294c903b6545f3294cc8aa4cbfdee",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-007",
            "record_sha256": "91ce84a76162c4480b95c2730e9cbabd045ba23be45ce038a937d802ef5a1b5e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-008",
        "partition": "core_internal",
        "producer": "AFQR-01",
        "consumer": "AFQR-09",
        "authoritative_r1c_record_sha256": "e289d49985c2e6a4884e71a6497f831aa95fce8aa522fefba180fabb18f53dbf",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-008",
            "record_sha256": "ea991f1569229bd91f8f9fd1079dec9d8a1e0bd8e7d7910c3957165777c2e553",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-009",
        "partition": "core_agency_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-10",
        "authoritative_r1c_record_sha256": "7932611f5cd605486e524e1fbdab698f2384fe2617f250af6945567c88655553",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-009",
            "record_sha256": "e5889b54e8879281bcc9ac9312617838e00f483c447d510426bef0f039ce3855",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-009",
            "record_sha256": "86479284f062caa5a2232192113fb114aa850223c1d6988908c1e71d1341ab13",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-010",
        "partition": "core_agency_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-11",
        "authoritative_r1c_record_sha256": "498cbbdb2c71ca83613d801c65182ad231bce4c541b9f3de4d49a0334d5e1a79",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-010",
            "record_sha256": "175b3bcb872f65554f4c2d88900628a9a7c9b4b447ed9786255980ab16d14b12",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-010",
            "record_sha256": "9919ccf9f0cd000006080b64d2077846d24685eb3c7b8f4d6d265bb784bf70d8",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-011",
        "partition": "core_agency_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-12",
        "authoritative_r1c_record_sha256": "51d54a0d00dba26d27dc6f36ee650534fd2b2206a6f070cfe226d4cd21a513c6",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-011",
            "record_sha256": "a140c5747fcd907dc8f659e1839d219d2392f2a602ebc4a7a0072e7d94f84f6b",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-011",
            "record_sha256": "8400c424a3c7f7787d18f5a94dd634b1308b093bd993b6b53a4fa1977f28a36c",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-012",
        "partition": "core_agency_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-13",
        "authoritative_r1c_record_sha256": "d1bdf49e0d9fd6bebfc398a37f318cbe791f2640690491d5ea41d8ce4bae1bb3",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-012",
            "record_sha256": "d69425c1186400deae87f8b3f69376c9cabe735341f892d97e2523c8c47b352c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-012",
            "record_sha256": "144bd22d29af9501181b2a53dd75b0ec54044827b89e79af9ea9399f77608162",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-013",
        "partition": "core_agency_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-14",
        "authoritative_r1c_record_sha256": "03f03cd7c055fd0754803809f3bc9e358f1d0a034de8e6c12dfe362c6f597d71",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-013",
            "record_sha256": "3c69262603574a5ee7c711500ea5d4f602ecbf331551276b5b9462f8eb7268ee",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-013",
            "record_sha256": "1e10e74ceea0136a53f6efc43e0e28b5935425b271c6467804fa9737b7e2ce39",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-014",
        "partition": "core_agency_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "56e005bd315cf4377bb865bb32651cbe909e482422534353ab36cb8cb052927f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-014",
            "record_sha256": "0e7ebd788beaeff995db8ae56fa410264cef4ccda710de8d0a969d91cbd06f8c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-014",
            "record_sha256": "78357516fa3c96e8eee04a5b342157660810f26ec597826ea0f421dfc1155e64",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-015",
        "partition": "core_world_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-16",
        "authoritative_r1c_record_sha256": "8a5e9258ffc5072ea2a3f94154d5c863bd08edbfcd45e22b189d62d93922d72f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-015",
            "record_sha256": "b60c6cc3c4671993628a1a83853ab6b4699e07432a47fb5a32a442ddcd4b7079",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-015",
            "record_sha256": "255a128fc445b27f57eca21df9f437510c341540affbd953347434d2b22b55ff",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-016",
        "partition": "core_world_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-17",
        "authoritative_r1c_record_sha256": "55bc1a39c67885a5205dbeab3a6d6277694c46b7a0614c74facff7da3a8bd1f8",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-016",
            "record_sha256": "29ef11711557461f23d552e0d21e3e9d721a4bed4492dab88ce8690bbbc4ab16",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-016",
            "record_sha256": "a4f282cf2d0e551ef3feaf656ce3499cd5fa550dc3f60f655047e4223c811702",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-017",
        "partition": "core_world_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-18",
        "authoritative_r1c_record_sha256": "b4fbae3953adf25e4b34f6a9f73c9ee1a0d36dde2930afad8d05004d62857f99",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-017",
            "record_sha256": "a3be3e1ccfc6467fd85851b7f540a5365c4b27accf1b5e0247e57af98357dcb2",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-017",
            "record_sha256": "760985fdc44997d56a4de5f870480df32a4c25d092546e8d304235cfbcf02103",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-018",
        "partition": "core_world_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "dd412dc9e8dcbdaed258285162202f08e1d93e3e8acd8f3f41368be8dfbf0818",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-018",
            "record_sha256": "ac2ce057ec792aa9c4c50660f1e74b69fe7bfee6f11a3a3c580f98d37b0036cf",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-018",
            "record_sha256": "075137d679d9c7bdd72e2ec571d6db9ab2a57b9269db58a350c0272fc1505758",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-019",
        "partition": "core_world_boundary",
        "producer": "AFQR-01",
        "consumer": "AFQR-20",
        "authoritative_r1c_record_sha256": "d52defdce00242ef0f672e986d03c6ecbc25384bbec8f4ae47f379fe53a340f4",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-019",
            "record_sha256": "fe44752d31a12df615f6ea01f3e4a9e2ba4387e421fa0189b799b96d56afd95e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-019",
            "record_sha256": "d8dccb25a1393ec3ea8ba82e2b92f40bf03e0e62123c4dd39a088355d73b79ca",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-020",
        "partition": "core_internal",
        "producer": "AFQR-02",
        "consumer": "AFQR-03",
        "authoritative_r1c_record_sha256": "77bf93d040c63429a69a5d722e7436ac71827968d089a96e69386670e475a7a7",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-020",
            "record_sha256": "328fa36f80180bd11dca9f7280a964abc6bd5b13a09c1152c75db5d425fdacfc",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-021",
        "partition": "core_internal",
        "producer": "AFQR-02",
        "consumer": "AFQR-04",
        "authoritative_r1c_record_sha256": "2f7e01b2734a830e590083126fc09ec40126239336611a2dbac41efc9418321f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-021",
            "record_sha256": "f1738f6fc74695de5174816e078bfebdfa2913bf1d0096c77f6f1082ea06dffa",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-022",
        "partition": "core_internal",
        "producer": "AFQR-02",
        "consumer": "AFQR-09",
        "authoritative_r1c_record_sha256": "6e6cde3d01a57e997d94a127648f177d6de0d3d8943b0a1b613dc7381703d74b",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-022",
            "record_sha256": "62508e541f0f4245d1013118c1b7a26edde8f0c737887dcacd1e0d2dfa719a3f",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-023",
        "partition": "core_world_boundary",
        "producer": "AFQR-02",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "3109b8d7b5434b8b6ddc10680c571deefae031d9fcb9360f2f26c7f4b7f10b1f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-023",
            "record_sha256": "b65066ff1443326e890babeb212d8db6e1ac7ebbdc6281b91d01f4df61fb9f67",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-023",
            "record_sha256": "5b3d44b13d849e6e8671d1a057d75c62e654c2758dcb1628297ad72aa80c14eb",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-024",
        "partition": "core_internal",
        "producer": "AFQR-04",
        "consumer": "AFQR-02",
        "authoritative_r1c_record_sha256": "8c09f1a59768c15008ccc7e0b746b1b3797788223735b8bf75765ea954669fb8",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-024",
            "record_sha256": "d290bda577984b9097542e3ae33d9c4f57cd9b6a5bac590c83008470374d4aef",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-025",
        "partition": "core_internal",
        "producer": "AFQR-04",
        "consumer": "AFQR-06",
        "authoritative_r1c_record_sha256": "4cd41eda358cb0cedc697a1fc01a643e11d3625f3dc8740f0512603e3ccf1e81",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-025",
            "record_sha256": "9cd9f25c3de5cbb6c85b88633b5def15510a9c3e296f40677c4600f23b8db9f3",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-026",
        "partition": "core_internal",
        "producer": "AFQR-04",
        "consumer": "AFQR-07",
        "authoritative_r1c_record_sha256": "033df940016a0de6725caec6df191f1e7c65622bde2fb499323362e57f3ac7d9",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-026",
            "record_sha256": "a1bb3a1f4d36fea9d84761d42619c6ac04d012663ab63205509529e8831e46cc",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-027",
        "partition": "core_internal",
        "producer": "AFQR-04",
        "consumer": "AFQR-08",
        "authoritative_r1c_record_sha256": "63fc3edf9f1dfeeee1d1b2dbb3dc033e32b5d319da37e3d0d8b5c1cefa046cf0",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-027",
            "record_sha256": "192c6fcc63551f68b677f85e7f250497a0eae4f006a088f5c6b00ae4827b15f7",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-028",
        "partition": "core_internal",
        "producer": "AFQR-04",
        "consumer": "AFQR-09",
        "authoritative_r1c_record_sha256": "abf9ec9268f9dff3eb7b733f8a221dad91f668bf487ad605a2c3aa9967285fa7",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-028",
            "record_sha256": "f202c2ebc3dc4d96543c4fb387e56c633734f0dcc8da887ca65be6d47573083c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-029",
        "partition": "core_world_boundary",
        "producer": "AFQR-04",
        "consumer": "AFQR-18",
        "authoritative_r1c_record_sha256": "9e9533b3f9b7c07e1ff190f5b14f880d563e3080e4766d61046d07da1867094f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-029",
            "record_sha256": "b70ecb6d11052e350af9e481ddd36bc9089d8566612a811d3aa854383508e243",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-029",
            "record_sha256": "f6bd52feb4a0edbf7371a0d541ae050d57f5f05a49add595dcdcda9caf72a9bb",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-030",
        "partition": "core_world_boundary",
        "producer": "AFQR-04",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "2b09e1011c449baf19ccaefca02cbfad114585a9852a8855e2345f8284f9e1d2",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-030",
            "record_sha256": "0b0d91deeb49f677bad275ea3116fb378f643f3c949d037aaa74860fb40f6fc2",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-030",
            "record_sha256": "cd24a6e95991644b7a78eb88c99c1c75fd3c8c35b8aae9e3d5043ca8ac8fe204",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-031",
        "partition": "core_world_boundary",
        "producer": "AFQR-04",
        "consumer": "AFQR-20",
        "authoritative_r1c_record_sha256": "72ce4b23b92e2389367ee0d23d5e32952b476f8b6123c6322d26391517431be4",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-031",
            "record_sha256": "59cf4f2a51bee8e1b47c3402f551bf3c812b2d081d4265ed13c9343066fa6097",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-031",
            "record_sha256": "a693d64d92c8c019108a983457a510fb5d1d3c2ec24407e03256e3284d54fb7e",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-032",
        "partition": "core_internal",
        "producer": "AFQR-05",
        "consumer": "AFQR-03",
        "authoritative_r1c_record_sha256": "8bd79e202bae8b8c527b9b3483bcda429ed6d3f82f59ce5cb0d8ff1353c42682",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-032",
            "record_sha256": "da5e08858c7b0a17b180f680b4d59a91da7528aa37abea7e37e18a14a9436c30",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-033",
        "partition": "core_internal",
        "producer": "AFQR-05",
        "consumer": "AFQR-06",
        "authoritative_r1c_record_sha256": "ef755948a9c91c563fbc34a64890c495675ab012a3786a7331635d01f7d7f02e",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-033",
            "record_sha256": "580e9c52bd12392b04263d736989a48d926dedd8fa6dde85a8820b143bb9013e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-034",
        "partition": "core_internal",
        "producer": "AFQR-05",
        "consumer": "AFQR-07",
        "authoritative_r1c_record_sha256": "9d91ba06c7b1ff6c26dfbd3b0a9708e4af118a0129ca0ecb0b7fd34c756614ba",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-034",
            "record_sha256": "4d73b3be740ed85b4aa1d8406a61308cc0f0f1391eb1f88e2158b479c84daf43",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-035",
        "partition": "core_internal",
        "producer": "AFQR-05",
        "consumer": "AFQR-08",
        "authoritative_r1c_record_sha256": "deec4bd3eda64464a6fe9c99d653de9e45255fe4bc3624395e870b77a704ba82",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-035",
            "record_sha256": "142bb353c379b6bbbff1b448e673b85230327b644b3171d99e69395876395d6f",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-036",
        "partition": "core_internal",
        "producer": "AFQR-05",
        "consumer": "AFQR-09",
        "authoritative_r1c_record_sha256": "797cd51a7e6f73e025b2b4ffa45b3cce9493a8c54f5cd67b7f7e8666a6e0baad",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-036",
            "record_sha256": "918cd1d4f1c700d33d99fb7855890301b03735bc1b6fd7b945ea7bc930a63535",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-037",
        "partition": "core_agency_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-10",
        "authoritative_r1c_record_sha256": "d911ad0361e65295a8aeba55dde5cd5d146b9466844c23c32a4ee8db47340eaa",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-037",
            "record_sha256": "ce01ddbb0e963ea218fc150a57177f7bed40154b8c025461984ca4e70dfeb428",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-037",
            "record_sha256": "a8ef5843454941c7c5cfb2d67adb1ef2738c469611b6041705fb76e4eb11209a",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-038",
        "partition": "core_agency_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-11",
        "authoritative_r1c_record_sha256": "eb985d585032b4ea4d08138ff9e7a3f9a8ede24a823398bc2a2d43369c36d940",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-038",
            "record_sha256": "e2ec083d8a1fe0b3733f2e3fbf45b6774f8114132ff173a0ab7abc7d9a32ed4c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-038",
            "record_sha256": "290fd1e0ac9958e0fcf8ff081360318209d8880dc3e99cee99d815b763108b07",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-039",
        "partition": "core_agency_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-13",
        "authoritative_r1c_record_sha256": "e2d28dd92a1e2de0c7e23970e94a1e1843f3f07a10e46e1f04a0fe57f55af49f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-039",
            "record_sha256": "8e40a563e33da1700eba7b3b6d04a5846caa42edf0b2b7ec83d800a734ed42d9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-039",
            "record_sha256": "76651ecd1313df9e6a7caa7bfefad3726d93f2d5a60a5afbe0251e8cd81959e8",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-040",
        "partition": "core_agency_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-14",
        "authoritative_r1c_record_sha256": "70e8bcc551245437b5fa81f699fadf6b96c3bb544907a231f730c8ee967ca5cd",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-040",
            "record_sha256": "b83a182c379a802c9cc8975b7556cb352a2cdad43aa4d131cb81eb89a68b5c95",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-040",
            "record_sha256": "e338dcc6449190ebc689d4ba0e34ec7838bafa85af9166207c97946a6c468d19",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-041",
        "partition": "core_agency_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "1526853e0fd30f376a46ac44ab684d216cbc9b4e5d892b6b180cb5d2f07ef5bf",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-041",
            "record_sha256": "04f48e9a6bd9d07aed90e59f5a2a85936640db9a40f3b751333554b134b632c3",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-041",
            "record_sha256": "7014b6404560d20dbaf1af4b2e059c83e0808bf56b2977607d224df2123282e1",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-042",
        "partition": "core_world_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-16",
        "authoritative_r1c_record_sha256": "59e0cfb78fdff2df825325ed73d88e616791c09b64da07a42925e2eb3df31b03",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-042",
            "record_sha256": "e72f47ea281e1a967e72dc20fdb87aa001101dbd56cc537b962cb909f92332e9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-042",
            "record_sha256": "a4ffa29d6c3fded8e0dd6bf42316b53e6f6f3b1e6a45810ab9b87ab2e44bc5a3",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-043",
        "partition": "core_world_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-17",
        "authoritative_r1c_record_sha256": "48b4350dc393599eded76663146099edc6fce13d6e76df3ce1aaa282a14860cd",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-043",
            "record_sha256": "ff7931bb2ee9e9f8d0a53eabcca13eca42f8b699c93c3ffe895dc61546e94cde",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-043",
            "record_sha256": "f537611c7e3fd2fa809dfd510e6b6b5336cb6fe9862190f7ad9ccbb72a1fbd34",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-044",
        "partition": "core_world_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-18",
        "authoritative_r1c_record_sha256": "a8c6447df1b6399e1d1e4b0961f9ad2310dc26071616234972ccd4088493741b",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-044",
            "record_sha256": "991c9938cfff222b12c737862629ba79d50995449a525451bb4ac1da4fb6b433",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-044",
            "record_sha256": "de8996caf01180c35df43b776b7008aa4a6630e1107c02d80591bcccb120eed7",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-045",
        "partition": "core_world_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "36d5f676e007dd539a3233c5d4e5beb6d067826f36938b3946fb6cbdb27fd89e",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-045",
            "record_sha256": "2419157809b152b4f315e8404284852603b7d27b0b1e41df11283ad515edaf16",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-045",
            "record_sha256": "2954f4bbf2a8a7f3e5dc025543d6a39d25659d58c2dccf98eff1d66e71d0a58d",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-046",
        "partition": "core_world_boundary",
        "producer": "AFQR-05",
        "consumer": "AFQR-20",
        "authoritative_r1c_record_sha256": "301235e2e1334f7fdf3b46c4c9efc7e92f67cf5ce3413939de05eb79e3c2baa1",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-046",
            "record_sha256": "9fa361d21596b0868ff98a78cad04be5a872892f5c2eb620148038e549fc8eae",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-046",
            "record_sha256": "925e311529e4ee8ecc83c38dec063185c488a8da40be1959a2bf981f0682a638",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-047",
        "partition": "core_internal",
        "producer": "AFQR-06",
        "consumer": "AFQR-07",
        "authoritative_r1c_record_sha256": "75fd355cd24f39a9a03b1e001d547777a1e903bba426a0a591fece2ab14810ab",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-047",
            "record_sha256": "d1f98ba1820ccbe474ab968900477c056cfe3e59d8b750bcc043f535500fb31c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-048",
        "partition": "core_internal",
        "producer": "AFQR-06",
        "consumer": "AFQR-08",
        "authoritative_r1c_record_sha256": "a86ed5a2cf21dd2dd1c3f23c6541850688916e5c690e9ae8545e80a6d5168279",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-048",
            "record_sha256": "cfefc698e2598172a14e3391f040c846ae4bc088eb81efe1c527aeae3d896b68",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-049",
        "partition": "core_internal",
        "producer": "AFQR-06",
        "consumer": "AFQR-09",
        "authoritative_r1c_record_sha256": "7b528b91a5fb93be80164a7b14268d7a6a8db7e1c34f86e455d5909357cd141b",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-049",
            "record_sha256": "1b1aa0658c7b64ae250fcf7788c3ed6811b58d67434fb2c927e36becb8a6633b",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-050",
        "partition": "core_agency_boundary",
        "producer": "AFQR-06",
        "consumer": "AFQR-10",
        "authoritative_r1c_record_sha256": "952459cb315eabd819fb00dfe7ce780412839f72102f65e0359db4d2a263e56a",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-050",
            "record_sha256": "f0d7fd760594856bc4ddd978c7036d652b09886277773eb94fbd69e446757cf0",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-050",
            "record_sha256": "c4d63bd1c49370f1d5b99da281527befee015e413d555a3ab6bfe647fee5bd8c",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-051",
        "partition": "core_agency_boundary",
        "producer": "AFQR-06",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "456acbe78ed0aefa93700ac0fd2f9570891631ce0af37c1ea4f72af38f785647",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-051",
            "record_sha256": "4ff0339ff3bb9551538ac56f9d24c8bff90f08b5f09f08ee476521961bd2e54d",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-051",
            "record_sha256": "87bd246f2cc4624831098d8356502c9df51cc3e762d7f0d0ea91ca23e1fed697",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-052",
        "partition": "core_internal",
        "producer": "AFQR-08",
        "consumer": "AFQR-06",
        "authoritative_r1c_record_sha256": "7cc2bef9e5960a12abe0d07c178c44354dca64b8aaac2c0dd01aa034a7466edf",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-052",
            "record_sha256": "5aa6886c63461e4a6b4b18194dc8527a79746acd49348eba0fc1039392a8635a",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-053",
        "partition": "core_internal",
        "producer": "AFQR-08",
        "consumer": "AFQR-07",
        "authoritative_r1c_record_sha256": "84cf28b59dbe7fb0074a9aa5f280801d2986d613444bcfa094756e86a0beadde",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-053",
            "record_sha256": "4e27f746e2c84abb64dd0e4536e3951642c962b6fc1b4c23dcee43140844833a",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-054",
        "partition": "core_internal",
        "producer": "AFQR-08",
        "consumer": "AFQR-09",
        "authoritative_r1c_record_sha256": "704d1eccac71defd1787bf7e54455100b93fa3ce4473260ecb17348ebaba44ab",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-054",
            "record_sha256": "f0b7d9773b0dac4515fd5c385888eab696ea1966d0ae225aa25981c0a4733360",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-055",
        "partition": "core_agency_boundary",
        "producer": "AFQR-08",
        "consumer": "AFQR-10",
        "authoritative_r1c_record_sha256": "dd3e3a04e5ee92886c3465f0d895ab8685a3c088a6c58296c95a82bdcab98af5",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-055",
            "record_sha256": "597a526fe2362c34db7138085a3d2453a28c30c8e1c815e68d4663d373f42619",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-055",
            "record_sha256": "f22112f472a51767d511eb9c66bab71ad72f3ab3ec26c675906d959a5ddff2ac",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-056",
        "partition": "core_agency_boundary",
        "producer": "AFQR-08",
        "consumer": "AFQR-11",
        "authoritative_r1c_record_sha256": "9110f515151525f346dab62f1c8aa048add87075affcddec14bd1e03337e57e0",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-056",
            "record_sha256": "7430810a0b3d9e10787e0dbeffc8099b81aed2aa8da509f2c4b73c7eb48f71ab",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-056",
            "record_sha256": "98f67ff6726b232ddf7627a8da70599e112b69b3093a61d540fc70eeb0250f14",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-057",
        "partition": "core_agency_boundary",
        "producer": "AFQR-08",
        "consumer": "AFQR-12",
        "authoritative_r1c_record_sha256": "1429abec32bde8fc0ca6fe0e186f0d3f8a15612d5b926d0c6a42fa11bdef5508",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-057",
            "record_sha256": "7ade0513b74c1b744baba6832f717c5670f059f5f32f3fb99ceb1d357b3dfae9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-057",
            "record_sha256": "8985773221205cff55938a7b3ad8f9d02d4ff72a99eb170d525964f7ab287673",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-058",
        "partition": "core_agency_boundary",
        "producer": "AFQR-08",
        "consumer": "AFQR-13",
        "authoritative_r1c_record_sha256": "2e585856d26d4790eb0d6b69bcfe7b07e0fb6ae65950d3dc05f1db34e2f4bafd",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-058",
            "record_sha256": "b1012dfb2f5362e368a63961efd527dc75ddf96fab1cdbfb1a18f59c5651bce6",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-058",
            "record_sha256": "c0007d361d069f34dd7445001d0dfdfd87e4a90492247ff0e5768476a07ac4d3",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-059",
        "partition": "core_agency_boundary",
        "producer": "AFQR-08",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "4d0e2ebe075cadb8793eefb34af59594fd5743504aa3484a90174dce3d2bc542",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-059",
            "record_sha256": "b2b6628183219a68759f10702e3c3efd62c537e9a30fa21f1d2be6bb81dca2e9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-059",
            "record_sha256": "0a57bf8b3b0de74b3dc74890d1415ba730dfdad0ea4796d8372c417acbfb8cbb",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-060",
        "partition": "core_world_boundary",
        "producer": "AFQR-08",
        "consumer": "AFQR-16",
        "authoritative_r1c_record_sha256": "5b1e99039bceeba1d1fe0b445617037e0d98c42e2da6263fe506f6443b7558e3",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-060",
            "record_sha256": "d44ed0534f7d62e605c63b397750ef2437d6e1b0d2b8d6b2fa8aa2e3b020c2e4",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-060",
            "record_sha256": "465ced7e91a95db900456bb430b5fa01bfcc1f93c2301d97c69759797b18dc23",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-061",
        "partition": "core_internal",
        "producer": "AFQR-09",
        "consumer": "AFQR-01",
        "authoritative_r1c_record_sha256": "75cf026c632eef35724c71eaa214e273e27a5b54f9717a581f507e895ec6537d",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-061",
            "record_sha256": "ad26602015ab9881afdf90c4934caec67bbe438bda10cf18e65dc56144d6c7f4",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-062",
        "partition": "core_internal",
        "producer": "AFQR-09",
        "consumer": "AFQR-02",
        "authoritative_r1c_record_sha256": "6be9d52c0c2c4f47268797365b602b12ecff2003029b5c945d7ff330ff242e54",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-062",
            "record_sha256": "8d061f5d29b5bae8c6a9c35afc13802e914194d2e689487f6264be73cab14912",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-063",
        "partition": "core_internal",
        "producer": "AFQR-09",
        "consumer": "AFQR-04",
        "authoritative_r1c_record_sha256": "56c4c7035b25c69472ec9e37860603725e28943e8f68dff5b462df15d951ce3f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-063",
            "record_sha256": "0793bf3a63d112468b3129f0f9bc40de6ecaaef4432e6b7ff99513f3edc055b5",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-064",
        "partition": "core_internal",
        "producer": "AFQR-09",
        "consumer": "AFQR-06",
        "authoritative_r1c_record_sha256": "31cfcf3971436b343b56e6e3ca92f545e7f4058c5a188f4846685051a04b4b03",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-064",
            "record_sha256": "792714ff7f8fb789898c437870028a09d38ba7b45fb5c0c592ec9e8b63094c27",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-065",
        "partition": "core_internal",
        "producer": "AFQR-09",
        "consumer": "AFQR-07",
        "authoritative_r1c_record_sha256": "68e5ad15da9e8ba764163649df4f9e743c3c6a56cb160d68105e8c18e956ffc6",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-065",
            "record_sha256": "6237a59503e10be7f1d4b62ccb2e5ff68e26c6a251aeb355d731b3ec3c52ae55",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-066",
        "partition": "core_internal",
        "producer": "AFQR-09",
        "consumer": "AFQR-08",
        "authoritative_r1c_record_sha256": "ee14d6cc15f43e894595a0b281165f956c5fbdc9fbb8fa871e499429ce366ebc",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-066",
            "record_sha256": "9e190f2326644cf561eccd90ab30b2174c6b52e98fa0d9d5a1c1ffff99e5732f",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-067",
        "partition": "core_agency_boundary",
        "producer": "AFQR-09",
        "consumer": "AFQR-11",
        "authoritative_r1c_record_sha256": "934ab3e80096b78dba011796194fc7499c4e1c1a2aa829b5db95aedf361dee3a",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-067",
            "record_sha256": "baf74457a5bcd39a44763585a95de40206b984de16bd9fa221ef939c60410b52",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-067",
            "record_sha256": "ae878ebeaa30d4043a8c317a35485699afb2beb8aa590d501f89e7eaf573eb69",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-068",
        "partition": "core_agency_boundary",
        "producer": "AFQR-09",
        "consumer": "AFQR-13",
        "authoritative_r1c_record_sha256": "be52cfc0bf3828f9ddf440873c558d857d4dd8960c94ba495e816b265aba8f65",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-068",
            "record_sha256": "f2a9d64bb0bbd36660582ab198174fc9fe26041826ce6d0aa5963b8e7e2225f2",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-068",
            "record_sha256": "a712a6c4219453f8da3c50e1a790f60204403f9a2d6d5ef872eba0fb9374ef64",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-069",
        "partition": "core_agency_boundary",
        "producer": "AFQR-09",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "ce3442aedcebf79620ee7c831e27ecf3bee4e527d2748b64554048f3337def20",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-069",
            "record_sha256": "a09c7eda1919256a8a625ea399d2f30706c7022a686b713319e8661cc0ff6586",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-069",
            "record_sha256": "af82d3fbac8c1fc2144ed4502cab972622e182551eb87b986a1d018d4ab3e505",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-070",
        "partition": "core_world_boundary",
        "producer": "AFQR-09",
        "consumer": "AFQR-16",
        "authoritative_r1c_record_sha256": "91ce26638118b62fa7585814902fb562de418dc6e17a34f3c3bfa0659b66c2d2",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-070",
            "record_sha256": "2b2da07bd688ea2c947f00e91ccef3300693e621a17e73e41df3589e0677b7ec",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-070",
            "record_sha256": "4960603a293b0ecde15f779be8f7e629003a41b176a1e5981fd2fa69358e8c8a",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-071",
        "partition": "core_world_boundary",
        "producer": "AFQR-09",
        "consumer": "AFQR-17",
        "authoritative_r1c_record_sha256": "fe26982b21db5e1973034cd11d2e5ccbe78d77827affbd5f658dcf583b641267",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-071",
            "record_sha256": "b1d3bdbb9194ca63c5b9d7d379a7c3688b07b393fd253d0bebcaca4050fc6fa9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-071",
            "record_sha256": "4786db5fe11409ad0677791e4c6fd3935e3faf1761a6ca0486cbf9e1e9725c4e",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-072",
        "partition": "agency_internal",
        "producer": "AFQR-10",
        "consumer": "AFQR-11",
        "authoritative_r1c_record_sha256": "ba0b42b92382d5f68de7a9503833a22f281173f8acebdbe322a616e13cc9ec72",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-072",
            "record_sha256": "fe8fa21d8f77c3828645c73287d3cc159941f565598496b64e177ec3ccaa97e4",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-073",
        "partition": "agency_internal",
        "producer": "AFQR-10",
        "consumer": "AFQR-12",
        "authoritative_r1c_record_sha256": "3624f7ff38c532ce8eb4a93751670aad8097559ecf6d17081626e53b93f9bc96",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-073",
            "record_sha256": "baa10304f75b9f520046746ed603682c4a8c068d42352db7d12248338ca60dec",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-074",
        "partition": "agency_internal",
        "producer": "AFQR-10",
        "consumer": "AFQR-13",
        "authoritative_r1c_record_sha256": "3ee14af40d1945af9bdaae3dc65740a6c00a7435775be2d4a907a0e15d6c6fdd",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-074",
            "record_sha256": "57d52c90486c343f7768bce163330662702dab2dbe03ede66bc3c4f3d5842f9e",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-075",
        "partition": "agency_internal",
        "producer": "AFQR-10",
        "consumer": "AFQR-14",
        "authoritative_r1c_record_sha256": "de509244015238ab1de766b064b4227a1389ce35eb21ea33c7a1c7ab72c20819",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-075",
            "record_sha256": "7d75b0c61a3407ec48a2c1881fcc7adc56b9363aa1216cd8ce04fafd5afe6d0d",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-076",
        "partition": "agency_internal",
        "producer": "AFQR-10",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "6d33a1bce4f3740248ea5bb2ba021c1694422ec8f4ff5d11474f4ded81cf0dd9",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-076",
            "record_sha256": "1b5fab05f2ae0ae199fab00ccb292aecd39817c6a771892d17b515b35e225673",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-077",
        "partition": "agency_world_boundary",
        "producer": "AFQR-10",
        "consumer": "AFQR-17",
        "authoritative_r1c_record_sha256": "515c5cd8ea92d5764cc404289754c6159a741896b06f17ab9db7c8d4c82378e1",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-077",
            "record_sha256": "2708a45d049b384a78d8cf694961a6790eda028c5c12040a312f66b65cb64565",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-077",
            "record_sha256": "91d9e9ee1796e2ac5e05184fd32b3609d88bd390f5c96afe85d81f4ea8e1d329",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-078",
        "partition": "agency_world_boundary",
        "producer": "AFQR-10",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "69163e40cb5cd00206f6efd95b5fdf3721394a42250e2ca8bf41c072fa4f22be",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-078",
            "record_sha256": "3203498f359d7003b77034ead8e801693f7fc60705499e4d059547f0f5a38ceb",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-078",
            "record_sha256": "ca77f70409e7a2135e6c783ce302532a4e1615bb9fa5e982c1bd39624642b7ca",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-079",
        "partition": "agency_world_boundary",
        "producer": "AFQR-10",
        "consumer": "AFQR-20",
        "authoritative_r1c_record_sha256": "bd85321a4710252c255fe11d6f6ecaeadddc03b298418aded878d7902fc97b70",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-079",
            "record_sha256": "0e756aaf7be1a7fc8c767ed44970ae4d1784d50f9bb27a21ecfd6ba803244bbe",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-079",
            "record_sha256": "ae03f27cad95714b7567105cc5ef071163d279250e68fd72a2dc8e1ea7f6bb41",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-080",
        "partition": "agency_internal",
        "producer": "AFQR-11",
        "consumer": "AFQR-12",
        "authoritative_r1c_record_sha256": "83fc1ef5aded813e4af97ec070bfb3ea5d745ca48026c2db192a7a2548a415d0",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-080",
            "record_sha256": "3860935b7b1c4fea548524dfc6285be9a8afb940f9c7f2f6c4a5537338d23494",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-081",
        "partition": "agency_internal",
        "producer": "AFQR-11",
        "consumer": "AFQR-13",
        "authoritative_r1c_record_sha256": "09e7b95b49d553f030e1da44c9b47b9abd7358f6f5524e39d5da188b206c33c2",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-081",
            "record_sha256": "5b943f2e5351a20a2179e90afa0934dfbf2da97a3feddb772fe33299829914b7",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-082",
        "partition": "agency_internal",
        "producer": "AFQR-11",
        "consumer": "AFQR-14",
        "authoritative_r1c_record_sha256": "2be138553dbcad78884bf70c3796437713268f4cc6690aa32753a5bb0d2235b9",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-082",
            "record_sha256": "9d256e7fdbf3ad0a43dd6918db7fdfd373d60e0d198961753948294d61ef6b36",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-083",
        "partition": "agency_internal",
        "producer": "AFQR-11",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "1cd3295696338e56bc803deb1e6bf9592ae8eb7ce6ca2a3ebe1a22e831be1d0f",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-083",
            "record_sha256": "fdba1929dcf4d5016e6055b76ec0cee7cfe3ec33d6308cfcb49b0a11a2ee6b10",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-084",
        "partition": "agency_world_boundary",
        "producer": "AFQR-11",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "f22b0e437677e2817ec36aead4fe404c4c039ade3abfe95071a0c3a57d25b2cf",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-084",
            "record_sha256": "6a75a58642ddaba721fc3bd028df9faeeea4b62c36056cb948cee1ed8704ac13",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-084",
            "record_sha256": "2d9a5a293b4962b83c6c12910000d92a1078034c36aa0cd7900088cc5b00bc16",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-085",
        "partition": "agency_internal",
        "producer": "AFQR-14",
        "consumer": "AFQR-13",
        "authoritative_r1c_record_sha256": "3e433edd74826df451f57c8baa347110070e2f315be75f561a847b9c3d0a70da",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-085",
            "record_sha256": "b4fd96261d1abfc64416a0bd589bf41eed3de5bd2df2e7fe93f9910ab347d7a5",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-086",
        "partition": "agency_internal",
        "producer": "AFQR-14",
        "consumer": "AFQR-15",
        "authoritative_r1c_record_sha256": "e899e783341c145105f685eb9b3fbad8c34fb24c705ca16d934063b55578c0c3",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-086",
            "record_sha256": "d4d07f86e71ee611c7321867169552cd07cbea263fc452a43733e12060c8095d",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-087",
        "partition": "agency_world_boundary",
        "producer": "AFQR-14",
        "consumer": "AFQR-20",
        "authoritative_r1c_record_sha256": "afbce09bd70ef07cfbb90ae3d8686fd860f5256138cec7d445f5fb4f0195cf96",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-087",
            "record_sha256": "755c61723390c3eea616bfd502c3c2fa6271c85298ead1e6cec1f05ed996ef08",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-087",
            "record_sha256": "9ca78200c06526780d349a6f4080ac14cbfd222de8dd0b3d2fe1f9be60b6fb2d",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 2
      },
      {
        "edge_id": "DEP-088",
        "partition": "world_internal",
        "producer": "AFQR-17",
        "consumer": "AFQR-16",
        "authoritative_r1c_record_sha256": "b5ba54283b5b8a9555357b957d4816edb4c3d328d7e26afb050b48f511740266",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "world",
            "record_id": "DEP-088",
            "record_sha256": "270da795c22f7434071e340c4505878fbb3b4fbfbdb12224d77e5aca6f010dc3",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-089",
        "partition": "world_internal",
        "producer": "AFQR-17",
        "consumer": "AFQR-18",
        "authoritative_r1c_record_sha256": "c9ce83e2a1f357bfe36301cfbd730e5a3bc223f3ccef7adabe2bfa7cd9d0b866",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "world",
            "record_id": "DEP-089",
            "record_sha256": "2bee02b4fdd18914ec1806223a6fc5b9f7715e57630fc71c102c6964f4572186",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-090",
        "partition": "world_internal",
        "producer": "AFQR-17",
        "consumer": "AFQR-20",
        "authoritative_r1c_record_sha256": "7e307e2b6d340a40d41924c60e1cc065f88abeeb26567416397d2f1887d87922",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "world",
            "record_id": "DEP-090",
            "record_sha256": "0bda16d6d71e7ab67f90cf4049df5a8ba56ef226a3cdd340a80c5eaabc36b3cc",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-091",
        "partition": "world_internal",
        "producer": "AFQR-18",
        "consumer": "AFQR-17",
        "authoritative_r1c_record_sha256": "d2343154151bd4ec4582f8cd41811f70982330a5fe49248aea89d33b06db97c5",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "world",
            "record_id": "DEP-091",
            "record_sha256": "d01d3a2eee05e33d4768d33ce68f4633c8bfb7fe48cbe0b177e47f3a274ee333",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-092",
        "partition": "world_internal",
        "producer": "AFQR-18",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "61083252f83c6966584f016770b2ced44c4f3e8514eb3eb7e19efadc2a61545e",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "world",
            "record_id": "DEP-092",
            "record_sha256": "1064a6d4f1cf853811f659fe16e066eb426d619c6d0ff6c3db70ac2cd213180b",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-093",
        "partition": "world_internal",
        "producer": "AFQR-18",
        "consumer": "AFQR-20",
        "authoritative_r1c_record_sha256": "e852f63ef4e929217d596d8b3f24a543d9404e7b8d85798fa39da1229f1192b7",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "world",
            "record_id": "DEP-093",
            "record_sha256": "87e0eddbb73f29138db1ed2630bc9091632592b6c64bfa755bf54026ecd7372d",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 1
      },
      {
        "edge_id": "DEP-094",
        "partition": "world_internal",
        "producer": "AFQR-20",
        "consumer": "AFQR-19",
        "authoritative_r1c_record_sha256": "08b730f981eb85f7f9bbd1e4d90f65fe1cfbda2f82ca10ce0f5cfc1baea22b66",
        "compared_fields": [
          "relation_or_handoff_kind",
          "semantic_type_owner",
          "semantic_type_owner.r1b_term_bindings",
          "producer_supplies",
          "consumer_may_use",
          "ownership_does_not_transfer",
          "consumer_not_semantic_owner_by_consumption",
          "preconditions",
          "postconditions",
          "unavailable_input_behavior",
          "failure_behavior (represented by unavailable_input_behavior where R1C records no separate field)",
          "revocation_invalidation_or_cascade",
          "hidden_information_or_projection_constraints",
          "source_evidence_records",
          "source_evidence_paths",
          "cycle_participation",
          "r1d_destination_family_or_escalation"
        ],
        "mismatch_list": [],
        "result": "pass",
        "applicable_r1d_projection_records": [
          {
            "family": "world",
            "record_id": "DEP-094",
            "record_sha256": "c0ae527fc9b27d49be99189fb7ff1ad51d618e7fc7fd4359d4f535d2d46ca8c6",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "projection_count_expected": 1
      }
    ]
  },
  "r1d_completeness": {
    "result": "pass",
    "historical_completion_boundaries_preserved": true,
    "projection_review_records": [
      {
        "edge_id": "DEP-001",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-001",
            "record_sha256": "8205093416b4ba6cdc359a0c6e430c8d5c7e529086ce1e3f5962f1d237f96577",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-002",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-002",
            "record_sha256": "9292753358973cc4d0549ed8a6724bd3f131b1a84fbc6f64fce007c220e42f62",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-003",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-003",
            "record_sha256": "1c212e245d366ad1c1830ec5586c5341a983ae7b9cec9642d2e7aabba2599c73",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-004",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-004",
            "record_sha256": "15c192b182b1ce57ae0bc7c8de64c41069600e93a130b364ca39c5526f5b974e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-005",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-005",
            "record_sha256": "72b6d0074319fff6f2778318ec24ef2e74e06f4be732fd207770c4ff0249e3d6",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-006",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-006",
            "record_sha256": "061d8a8483d96d596d0dc01def113bfd6df52812e452f8f82f1b3f60d574c067",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-007",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-007",
            "record_sha256": "91ce84a76162c4480b95c2730e9cbabd045ba23be45ce038a937d802ef5a1b5e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-008",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-008",
            "record_sha256": "ea991f1569229bd91f8f9fd1079dec9d8a1e0bd8e7d7910c3957165777c2e553",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-009",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-009",
            "record_sha256": "e5889b54e8879281bcc9ac9312617838e00f483c447d510426bef0f039ce3855",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-009",
            "record_sha256": "86479284f062caa5a2232192113fb114aa850223c1d6988908c1e71d1341ab13",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-010",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-010",
            "record_sha256": "175b3bcb872f65554f4c2d88900628a9a7c9b4b447ed9786255980ab16d14b12",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-010",
            "record_sha256": "9919ccf9f0cd000006080b64d2077846d24685eb3c7b8f4d6d265bb784bf70d8",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-011",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-011",
            "record_sha256": "a140c5747fcd907dc8f659e1839d219d2392f2a602ebc4a7a0072e7d94f84f6b",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-011",
            "record_sha256": "8400c424a3c7f7787d18f5a94dd634b1308b093bd993b6b53a4fa1977f28a36c",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-012",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-012",
            "record_sha256": "d69425c1186400deae87f8b3f69376c9cabe735341f892d97e2523c8c47b352c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-012",
            "record_sha256": "144bd22d29af9501181b2a53dd75b0ec54044827b89e79af9ea9399f77608162",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-013",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-013",
            "record_sha256": "3c69262603574a5ee7c711500ea5d4f602ecbf331551276b5b9462f8eb7268ee",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-013",
            "record_sha256": "1e10e74ceea0136a53f6efc43e0e28b5935425b271c6467804fa9737b7e2ce39",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-014",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-014",
            "record_sha256": "0e7ebd788beaeff995db8ae56fa410264cef4ccda710de8d0a969d91cbd06f8c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-014",
            "record_sha256": "78357516fa3c96e8eee04a5b342157660810f26ec597826ea0f421dfc1155e64",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-015",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-015",
            "record_sha256": "b60c6cc3c4671993628a1a83853ab6b4699e07432a47fb5a32a442ddcd4b7079",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-015",
            "record_sha256": "255a128fc445b27f57eca21df9f437510c341540affbd953347434d2b22b55ff",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-016",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-016",
            "record_sha256": "29ef11711557461f23d552e0d21e3e9d721a4bed4492dab88ce8690bbbc4ab16",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-016",
            "record_sha256": "a4f282cf2d0e551ef3feaf656ce3499cd5fa550dc3f60f655047e4223c811702",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-017",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-017",
            "record_sha256": "a3be3e1ccfc6467fd85851b7f540a5365c4b27accf1b5e0247e57af98357dcb2",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-017",
            "record_sha256": "760985fdc44997d56a4de5f870480df32a4c25d092546e8d304235cfbcf02103",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-018",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-018",
            "record_sha256": "ac2ce057ec792aa9c4c50660f1e74b69fe7bfee6f11a3a3c580f98d37b0036cf",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-018",
            "record_sha256": "075137d679d9c7bdd72e2ec571d6db9ab2a57b9269db58a350c0272fc1505758",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-019",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-019",
            "record_sha256": "fe44752d31a12df615f6ea01f3e4a9e2ba4387e421fa0189b799b96d56afd95e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-019",
            "record_sha256": "d8dccb25a1393ec3ea8ba82e2b92f40bf03e0e62123c4dd39a088355d73b79ca",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-020",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-020",
            "record_sha256": "328fa36f80180bd11dca9f7280a964abc6bd5b13a09c1152c75db5d425fdacfc",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-021",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-021",
            "record_sha256": "f1738f6fc74695de5174816e078bfebdfa2913bf1d0096c77f6f1082ea06dffa",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-022",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-022",
            "record_sha256": "62508e541f0f4245d1013118c1b7a26edde8f0c737887dcacd1e0d2dfa719a3f",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-023",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-023",
            "record_sha256": "b65066ff1443326e890babeb212d8db6e1ac7ebbdc6281b91d01f4df61fb9f67",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-023",
            "record_sha256": "5b3d44b13d849e6e8671d1a057d75c62e654c2758dcb1628297ad72aa80c14eb",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-024",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-024",
            "record_sha256": "d290bda577984b9097542e3ae33d9c4f57cd9b6a5bac590c83008470374d4aef",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-025",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-025",
            "record_sha256": "9cd9f25c3de5cbb6c85b88633b5def15510a9c3e296f40677c4600f23b8db9f3",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-026",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-026",
            "record_sha256": "a1bb3a1f4d36fea9d84761d42619c6ac04d012663ab63205509529e8831e46cc",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-027",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-027",
            "record_sha256": "192c6fcc63551f68b677f85e7f250497a0eae4f006a088f5c6b00ae4827b15f7",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-028",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-028",
            "record_sha256": "f202c2ebc3dc4d96543c4fb387e56c633734f0dcc8da887ca65be6d47573083c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-029",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-029",
            "record_sha256": "b70ecb6d11052e350af9e481ddd36bc9089d8566612a811d3aa854383508e243",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-029",
            "record_sha256": "f6bd52feb4a0edbf7371a0d541ae050d57f5f05a49add595dcdcda9caf72a9bb",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-030",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-030",
            "record_sha256": "0b0d91deeb49f677bad275ea3116fb378f643f3c949d037aaa74860fb40f6fc2",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-030",
            "record_sha256": "cd24a6e95991644b7a78eb88c99c1c75fd3c8c35b8aae9e3d5043ca8ac8fe204",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-031",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-031",
            "record_sha256": "59cf4f2a51bee8e1b47c3402f551bf3c812b2d081d4265ed13c9343066fa6097",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-031",
            "record_sha256": "a693d64d92c8c019108a983457a510fb5d1d3c2ec24407e03256e3284d54fb7e",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-032",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-032",
            "record_sha256": "da5e08858c7b0a17b180f680b4d59a91da7528aa37abea7e37e18a14a9436c30",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-033",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-033",
            "record_sha256": "580e9c52bd12392b04263d736989a48d926dedd8fa6dde85a8820b143bb9013e",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-034",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-034",
            "record_sha256": "4d73b3be740ed85b4aa1d8406a61308cc0f0f1391eb1f88e2158b479c84daf43",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-035",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-035",
            "record_sha256": "142bb353c379b6bbbff1b448e673b85230327b644b3171d99e69395876395d6f",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-036",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-036",
            "record_sha256": "918cd1d4f1c700d33d99fb7855890301b03735bc1b6fd7b945ea7bc930a63535",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-037",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-037",
            "record_sha256": "ce01ddbb0e963ea218fc150a57177f7bed40154b8c025461984ca4e70dfeb428",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-037",
            "record_sha256": "a8ef5843454941c7c5cfb2d67adb1ef2738c469611b6041705fb76e4eb11209a",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-038",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-038",
            "record_sha256": "e2ec083d8a1fe0b3733f2e3fbf45b6774f8114132ff173a0ab7abc7d9a32ed4c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-038",
            "record_sha256": "290fd1e0ac9958e0fcf8ff081360318209d8880dc3e99cee99d815b763108b07",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-039",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-039",
            "record_sha256": "8e40a563e33da1700eba7b3b6d04a5846caa42edf0b2b7ec83d800a734ed42d9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-039",
            "record_sha256": "76651ecd1313df9e6a7caa7bfefad3726d93f2d5a60a5afbe0251e8cd81959e8",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-040",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-040",
            "record_sha256": "b83a182c379a802c9cc8975b7556cb352a2cdad43aa4d131cb81eb89a68b5c95",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-040",
            "record_sha256": "e338dcc6449190ebc689d4ba0e34ec7838bafa85af9166207c97946a6c468d19",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-041",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-041",
            "record_sha256": "04f48e9a6bd9d07aed90e59f5a2a85936640db9a40f3b751333554b134b632c3",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-041",
            "record_sha256": "7014b6404560d20dbaf1af4b2e059c83e0808bf56b2977607d224df2123282e1",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-042",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-042",
            "record_sha256": "e72f47ea281e1a967e72dc20fdb87aa001101dbd56cc537b962cb909f92332e9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-042",
            "record_sha256": "a4ffa29d6c3fded8e0dd6bf42316b53e6f6f3b1e6a45810ab9b87ab2e44bc5a3",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-043",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-043",
            "record_sha256": "ff7931bb2ee9e9f8d0a53eabcca13eca42f8b699c93c3ffe895dc61546e94cde",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-043",
            "record_sha256": "f537611c7e3fd2fa809dfd510e6b6b5336cb6fe9862190f7ad9ccbb72a1fbd34",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-044",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-044",
            "record_sha256": "991c9938cfff222b12c737862629ba79d50995449a525451bb4ac1da4fb6b433",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-044",
            "record_sha256": "de8996caf01180c35df43b776b7008aa4a6630e1107c02d80591bcccb120eed7",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-045",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-045",
            "record_sha256": "2419157809b152b4f315e8404284852603b7d27b0b1e41df11283ad515edaf16",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-045",
            "record_sha256": "2954f4bbf2a8a7f3e5dc025543d6a39d25659d58c2dccf98eff1d66e71d0a58d",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-046",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-046",
            "record_sha256": "9fa361d21596b0868ff98a78cad04be5a872892f5c2eb620148038e549fc8eae",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-046",
            "record_sha256": "925e311529e4ee8ecc83c38dec063185c488a8da40be1959a2bf981f0682a638",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-047",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-047",
            "record_sha256": "d1f98ba1820ccbe474ab968900477c056cfe3e59d8b750bcc043f535500fb31c",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-048",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-048",
            "record_sha256": "cfefc698e2598172a14e3391f040c846ae4bc088eb81efe1c527aeae3d896b68",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-049",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-049",
            "record_sha256": "1b1aa0658c7b64ae250fcf7788c3ed6811b58d67434fb2c927e36becb8a6633b",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-050",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-050",
            "record_sha256": "f0d7fd760594856bc4ddd978c7036d652b09886277773eb94fbd69e446757cf0",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-050",
            "record_sha256": "c4d63bd1c49370f1d5b99da281527befee015e413d555a3ab6bfe647fee5bd8c",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-051",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-051",
            "record_sha256": "4ff0339ff3bb9551538ac56f9d24c8bff90f08b5f09f08ee476521961bd2e54d",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-051",
            "record_sha256": "87bd246f2cc4624831098d8356502c9df51cc3e762d7f0d0ea91ca23e1fed697",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-052",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-052",
            "record_sha256": "5aa6886c63461e4a6b4b18194dc8527a79746acd49348eba0fc1039392a8635a",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-053",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-053",
            "record_sha256": "4e27f746e2c84abb64dd0e4536e3951642c962b6fc1b4c23dcee43140844833a",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-054",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-054",
            "record_sha256": "f0b7d9773b0dac4515fd5c385888eab696ea1966d0ae225aa25981c0a4733360",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-055",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-055",
            "record_sha256": "597a526fe2362c34db7138085a3d2453a28c30c8e1c815e68d4663d373f42619",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-055",
            "record_sha256": "f22112f472a51767d511eb9c66bab71ad72f3ab3ec26c675906d959a5ddff2ac",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-056",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-056",
            "record_sha256": "7430810a0b3d9e10787e0dbeffc8099b81aed2aa8da509f2c4b73c7eb48f71ab",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-056",
            "record_sha256": "98f67ff6726b232ddf7627a8da70599e112b69b3093a61d540fc70eeb0250f14",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-057",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-057",
            "record_sha256": "7ade0513b74c1b744baba6832f717c5670f059f5f32f3fb99ceb1d357b3dfae9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-057",
            "record_sha256": "8985773221205cff55938a7b3ad8f9d02d4ff72a99eb170d525964f7ab287673",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-058",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-058",
            "record_sha256": "b1012dfb2f5362e368a63961efd527dc75ddf96fab1cdbfb1a18f59c5651bce6",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-058",
            "record_sha256": "c0007d361d069f34dd7445001d0dfdfd87e4a90492247ff0e5768476a07ac4d3",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-059",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-059",
            "record_sha256": "b2b6628183219a68759f10702e3c3efd62c537e9a30fa21f1d2be6bb81dca2e9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-059",
            "record_sha256": "0a57bf8b3b0de74b3dc74890d1415ba730dfdad0ea4796d8372c417acbfb8cbb",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-060",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-060",
            "record_sha256": "d44ed0534f7d62e605c63b397750ef2437d6e1b0d2b8d6b2fa8aa2e3b020c2e4",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-060",
            "record_sha256": "465ced7e91a95db900456bb430b5fa01bfcc1f93c2301d97c69759797b18dc23",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-061",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-061",
            "record_sha256": "ad26602015ab9881afdf90c4934caec67bbe438bda10cf18e65dc56144d6c7f4",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-062",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-062",
            "record_sha256": "8d061f5d29b5bae8c6a9c35afc13802e914194d2e689487f6264be73cab14912",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-063",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-063",
            "record_sha256": "0793bf3a63d112468b3129f0f9bc40de6ecaaef4432e6b7ff99513f3edc055b5",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-064",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-064",
            "record_sha256": "792714ff7f8fb789898c437870028a09d38ba7b45fb5c0c592ec9e8b63094c27",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-065",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-065",
            "record_sha256": "6237a59503e10be7f1d4b62ccb2e5ff68e26c6a251aeb355d731b3ec3c52ae55",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-066",
        "partition": "core_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-INT-DEP-066",
            "record_sha256": "9e190f2326644cf561eccd90ab30b2174c6b52e98fa0d9d5a1c1ffff99e5732f",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-067",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-067",
            "record_sha256": "baf74457a5bcd39a44763585a95de40206b984de16bd9fa221ef939c60410b52",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-067",
            "record_sha256": "ae878ebeaa30d4043a8c317a35485699afb2beb8aa590d501f89e7eaf573eb69",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-068",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-068",
            "record_sha256": "f2a9d64bb0bbd36660582ab198174fc9fe26041826ce6d0aa5963b8e7e2225f2",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-068",
            "record_sha256": "a712a6c4219453f8da3c50e1a790f60204403f9a2d6d5ef872eba0fb9374ef64",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-069",
        "partition": "core_agency_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-069",
            "record_sha256": "a09c7eda1919256a8a625ea399d2f30706c7022a686b713319e8661cc0ff6586",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-069",
            "record_sha256": "af82d3fbac8c1fc2144ed4502cab972622e182551eb87b986a1d018d4ab3e505",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-070",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-070",
            "record_sha256": "2b2da07bd688ea2c947f00e91ccef3300693e621a17e73e41df3589e0677b7ec",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-070",
            "record_sha256": "4960603a293b0ecde15f779be8f7e629003a41b176a1e5981fd2fa69358e8c8a",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-071",
        "partition": "core_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "core",
            "record_id": "CORE-BND-DEP-071",
            "record_sha256": "b1d3bdbb9194ca63c5b9d7d379a7c3688b07b393fd253d0bebcaca4050fc6fa9",
            "source_path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
          },
          {
            "family": "world",
            "record_id": "DEP-071",
            "record_sha256": "4786db5fe11409ad0677791e4c6fd3935e3faf1761a6ca0486cbf9e1e9725c4e",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-072",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-072",
            "record_sha256": "fe8fa21d8f77c3828645c73287d3cc159941f565598496b64e177ec3ccaa97e4",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-073",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-073",
            "record_sha256": "baa10304f75b9f520046746ed603682c4a8c068d42352db7d12248338ca60dec",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-074",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-074",
            "record_sha256": "57d52c90486c343f7768bce163330662702dab2dbe03ede66bc3c4f3d5842f9e",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-075",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-075",
            "record_sha256": "7d75b0c61a3407ec48a2c1881fcc7adc56b9363aa1216cd8ce04fafd5afe6d0d",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-076",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-076",
            "record_sha256": "1b5fab05f2ae0ae199fab00ccb292aecd39817c6a771892d17b515b35e225673",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-077",
        "partition": "agency_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-077",
            "record_sha256": "2708a45d049b384a78d8cf694961a6790eda028c5c12040a312f66b65cb64565",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-077",
            "record_sha256": "91d9e9ee1796e2ac5e05184fd32b3609d88bd390f5c96afe85d81f4ea8e1d329",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-078",
        "partition": "agency_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-078",
            "record_sha256": "3203498f359d7003b77034ead8e801693f7fc60705499e4d059547f0f5a38ceb",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-078",
            "record_sha256": "ca77f70409e7a2135e6c783ce302532a4e1615bb9fa5e982c1bd39624642b7ca",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-079",
        "partition": "agency_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-079",
            "record_sha256": "0e756aaf7be1a7fc8c767ed44970ae4d1784d50f9bb27a21ecfd6ba803244bbe",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-079",
            "record_sha256": "ae03f27cad95714b7567105cc5ef071163d279250e68fd72a2dc8e1ea7f6bb41",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-080",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-080",
            "record_sha256": "3860935b7b1c4fea548524dfc6285be9a8afb940f9c7f2f6c4a5537338d23494",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-081",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-081",
            "record_sha256": "5b943f2e5351a20a2179e90afa0934dfbf2da97a3feddb772fe33299829914b7",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-082",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-082",
            "record_sha256": "9d256e7fdbf3ad0a43dd6918db7fdfd373d60e0d198961753948294d61ef6b36",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-083",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-083",
            "record_sha256": "fdba1929dcf4d5016e6055b76ec0cee7cfe3ec33d6308cfcb49b0a11a2ee6b10",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-084",
        "partition": "agency_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-084",
            "record_sha256": "6a75a58642ddaba721fc3bd028df9faeeea4b62c36056cb948cee1ed8704ac13",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-084",
            "record_sha256": "2d9a5a293b4962b83c6c12910000d92a1078034c36aa0cd7900088cc5b00bc16",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-085",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-085",
            "record_sha256": "b4fd96261d1abfc64416a0bd589bf41eed3de5bd2df2e7fe93f9910ab347d7a5",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-086",
        "partition": "agency_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-086",
            "record_sha256": "d4d07f86e71ee611c7321867169552cd07cbea263fc452a43733e12060c8095d",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-087",
        "partition": "agency_world_boundary",
        "expected_projection_count": 2,
        "projections": [
          {
            "family": "agency",
            "record_id": "AGENCY-DEP-087",
            "record_sha256": "755c61723390c3eea616bfd502c3c2fa6271c85298ead1e6cec1f05ed996ef08",
            "source_path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
          },
          {
            "family": "world",
            "record_id": "DEP-087",
            "record_sha256": "9ca78200c06526780d349a6f4080ac14cbfd222de8dd0b3d2fe1f9be60b6fb2d",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-088",
        "partition": "world_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "world",
            "record_id": "DEP-088",
            "record_sha256": "270da795c22f7434071e340c4505878fbb3b4fbfbdb12224d77e5aca6f010dc3",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-089",
        "partition": "world_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "world",
            "record_id": "DEP-089",
            "record_sha256": "2bee02b4fdd18914ec1806223a6fc5b9f7715e57630fc71c102c6964f4572186",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-090",
        "partition": "world_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "world",
            "record_id": "DEP-090",
            "record_sha256": "0bda16d6d71e7ab67f90cf4049df5a8ba56ef226a3cdd340a80c5eaabc36b3cc",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-091",
        "partition": "world_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "world",
            "record_id": "DEP-091",
            "record_sha256": "d01d3a2eee05e33d4768d33ce68f4633c8bfb7fe48cbe0b177e47f3a274ee333",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-092",
        "partition": "world_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "world",
            "record_id": "DEP-092",
            "record_sha256": "1064a6d4f1cf853811f659fe16e066eb426d619c6d0ff6c3db70ac2cd213180b",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-093",
        "partition": "world_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "world",
            "record_id": "DEP-093",
            "record_sha256": "87e0eddbb73f29138db1ed2630bc9091632592b6c64bfa755bf54026ecd7372d",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      },
      {
        "edge_id": "DEP-094",
        "partition": "world_internal",
        "expected_projection_count": 1,
        "projections": [
          {
            "family": "world",
            "record_id": "DEP-094",
            "record_sha256": "c0ae527fc9b27d49be99189fb7ff1ad51d618e7fc7fd4359d4f535d2d46ca8c6",
            "source_path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
          }
        ],
        "mismatch_list": [],
        "result": "pass"
      }
    ],
    "calculated_counts": {
      "core_internal": 33,
      "agency_internal": 11,
      "world_internal": 7,
      "core_agency_boundary": 21,
      "core_world_boundary": 17,
      "agency_world_boundary": 5
    },
    "r1e_authority_claimed_by_r1d": false
  },
  "twenty_afqr_source_matrix": {
    "record_source": "r1a_completeness.records",
    "count": 20,
    "record_set_sha256": "d8ed822f9993b52f531ee1f498a6213307ab49c7b33f58576fcd7c0ef25f35db"
  },
  "shared_term_completeness_summary": {
    "count": 41,
    "record_set_sha256": "0ca272f7358128204cd32e245846fa11116a65d38f5c47518520f7d55df5a963",
    "result": "pass"
  },
  "dependency_edge_partition_summary": {
    "core_internal": 33,
    "agency_internal": 11,
    "world_internal": 7,
    "core_agency_boundary": 21,
    "core_world_boundary": 17,
    "agency_world_boundary": 5
  },
  "cross_family_parity_summary": {
    "counts": {
      "core_internal": 33,
      "agency_internal": 11,
      "world_internal": 7,
      "core_agency_boundary": 21,
      "core_world_boundary": 17,
      "agency_world_boundary": 5
    },
    "projection_record_set_sha256": "34bc3e94bfb1f7ca58518d759871f94e2abec4be76aaf341564edd89508d73db",
    "result": "pass"
  },
  "cycle_decisions": [
    {
      "cycle_id": "CYCLE-001",
      "authoritative_record": {
        "cycle_id": "CYCLE-001",
        "afqrs": [
          "AFQR-01",
          "AFQR-09"
        ],
        "actual_dependency_directions": [
          "AFQR-01 -> AFQR-09 (DEP-008 commit)",
          "AFQR-09 -> AFQR-01 (DEP-061 relation_lifecycle)"
        ],
        "valid_edges_preserved": true,
        "resolution": "bounded_feedback_rule",
        "breaker": "AFQR-01 owns transition routing and commitment; AFQR-09 owns governed relation and dependency lifecycle. A committed transition may update a relation, and a relation constraint may govern a later transition, but neither output self-validates or transfers authority.",
        "edge_ids": [
          "DEP-008",
          "DEP-061"
        ]
      },
      "authoritative_record_sha256": "bf7a9af200d5c8add95cd87cf1c32b756d3dab6bcd11edf3cb6845d36875f5af",
      "exact_edge_ids": [
        "DEP-008",
        "DEP-061"
      ],
      "exact_directions": [
        "AFQR-01 -> AFQR-09 (DEP-008 commit)",
        "AFQR-09 -> AFQR-01 (DEP-061 relation_lifecycle)"
      ],
      "classification": "bounded_feedback_rule",
      "breaker_or_phase_rule": "AFQR-01 owns transition routing and commitment; AFQR-09 owns governed relation and dependency lifecycle. A committed transition may update a relation, and a relation constraint may govern a later transition, but neither output self-validates or transfers authority.",
      "owner_separation": "AFQR-01 owns transition routing and commitment; AFQR-09 owns governed relation and dependency lifecycle. A committed transition may update a relation, and a relation constraint may govern a later transition, but neither output self-validates or transfers authority.",
      "prohibited_recursion": "neither output self-validates or recursively authors the other",
      "evidence": [
        "SRC-0004",
        "SRC-0012",
        "SRC-0012",
        "SRC-0004"
      ],
      "r1d_treatments": [
        {
          "family": "core",
          "record_sha256": "bf7a9af200d5c8add95cd87cf1c32b756d3dab6bcd11edf3cb6845d36875f5af",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    },
    {
      "cycle_id": "CYCLE-002",
      "authoritative_record": {
        "cycle_id": "CYCLE-002",
        "afqrs": [
          "AFQR-02",
          "AFQR-04"
        ],
        "actual_dependency_directions": [
          "AFQR-02 -> AFQR-04 (DEP-021 command_lifecycle)",
          "AFQR-04 -> AFQR-02 (DEP-024 time_causality)"
        ],
        "valid_edges_preserved": true,
        "resolution": "phase_ordering",
        "breaker": "AFQR-02 owns command identity, attempts, retries, suspension, escalation, and durable command progress. AFQR-04 owns logical time, causal ordering, simultaneity, scheduling, and bounded cascades. Logical time may order command-lifecycle events but cannot create or redefine command identity; command lifecycle may request or consume scheduling but cannot author logical time.",
        "edge_ids": [
          "DEP-021",
          "DEP-024"
        ]
      },
      "authoritative_record_sha256": "7767359f12e03934ea28a103eaf66883af5e2cb79ee7bfa5157582e2ad34f564",
      "exact_edge_ids": [
        "DEP-021",
        "DEP-024"
      ],
      "exact_directions": [
        "AFQR-02 -> AFQR-04 (DEP-021 command_lifecycle)",
        "AFQR-04 -> AFQR-02 (DEP-024 time_causality)"
      ],
      "classification": "phase_ordering",
      "breaker_or_phase_rule": "AFQR-02 owns command identity, attempts, retries, suspension, escalation, and durable command progress. AFQR-04 owns logical time, causal ordering, simultaneity, scheduling, and bounded cascades. Logical time may order command-lifecycle events but cannot create or redefine command identity; command lifecycle may request or consume scheduling but cannot author logical time.",
      "owner_separation": "AFQR-02 owns command identity, attempts, retries, suspension, escalation, and durable command progress. AFQR-04 owns logical time, causal ordering, simultaneity, scheduling, and bounded cascades. Logical time may order command-lifecycle events but cannot create or redefine command identity; command lifecycle may request or consume scheduling but cannot author logical time.",
      "prohibited_recursion": "neither output self-validates or recursively authors the other",
      "evidence": [
        "SRC-0005",
        "SRC-0007",
        "SRC-0007",
        "SRC-0005"
      ],
      "r1d_treatments": [
        {
          "family": "core",
          "record_sha256": "7767359f12e03934ea28a103eaf66883af5e2cb79ee7bfa5157582e2ad34f564",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    },
    {
      "cycle_id": "CYCLE-003",
      "authoritative_record": {
        "cycle_id": "CYCLE-003",
        "afqrs": [
          "AFQR-06",
          "AFQR-08"
        ],
        "actual_dependency_directions": [
          "AFQR-06 -> AFQR-08 (DEP-048 claim_evidence)",
          "AFQR-08 -> AFQR-06 (DEP-052 identity_evidence)"
        ],
        "valid_edges_preserved": true,
        "resolution": "bounded_feedback_rule",
        "breaker": "AFQR-06 owns claims, evidence admissibility, conflict, and arbitration; AFQR-08 owns identity and continuity semantics. Identity records may be offered as evidence to AFQR-06. AFQR-06 may accept, reject, qualify, or dispute that evidence but cannot create identity merely by admitting a claim; AFQR-08 identity assertions cannot self-certify admissibility or truth.",
        "edge_ids": [
          "DEP-048",
          "DEP-052"
        ]
      },
      "authoritative_record_sha256": "ccc0ddd4b1a63a078d5f2d8f2baf6f74e658c1951771b351411767f8d767deab",
      "exact_edge_ids": [
        "DEP-048",
        "DEP-052"
      ],
      "exact_directions": [
        "AFQR-06 -> AFQR-08 (DEP-048 claim_evidence)",
        "AFQR-08 -> AFQR-06 (DEP-052 identity_evidence)"
      ],
      "classification": "bounded_feedback_rule",
      "breaker_or_phase_rule": "AFQR-06 owns claims, evidence admissibility, conflict, and arbitration; AFQR-08 owns identity and continuity semantics. Identity records may be offered as evidence to AFQR-06. AFQR-06 may accept, reject, qualify, or dispute that evidence but cannot create identity merely by admitting a claim; AFQR-08 identity assertions cannot self-certify admissibility or truth.",
      "owner_separation": "AFQR-06 owns claims, evidence admissibility, conflict, and arbitration; AFQR-08 owns identity and continuity semantics. Identity records may be offered as evidence to AFQR-06. AFQR-06 may accept, reject, qualify, or dispute that evidence but cannot create identity merely by admitting a claim; AFQR-08 identity assertions cannot self-certify admissibility or truth.",
      "prohibited_recursion": "neither output self-validates or recursively authors the other",
      "evidence": [
        "SRC-0009",
        "SRC-0011",
        "SRC-0011",
        "SRC-0009"
      ],
      "r1d_treatments": [
        {
          "family": "core",
          "record_sha256": "ccc0ddd4b1a63a078d5f2d8f2baf6f74e658c1951771b351411767f8d767deab",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    },
    {
      "cycle_id": "CYCLE-004",
      "authoritative_record": {
        "cycle_id": "CYCLE-004",
        "afqrs": [
          "AFQR-17",
          "AFQR-18"
        ],
        "actual_dependency_directions": [
          "AFQR-17 -> AFQR-18 (DEP-089 environment_handoff)",
          "AFQR-18 -> AFQR-17 (DEP-091 space_handoff)"
        ],
        "valid_edges_preserved": true,
        "resolution": "bounded_feedback_rule",
        "breaker": "AFQR-17 environmental process constraints and AFQR-18 spatial/topology constraints may inform later owner-qualified evaluation. Neither handoff recursively authors the other domain or validates itself; unresolved generic owner-contract needs remain escalated.",
        "edge_ids": [
          "DEP-089",
          "DEP-091"
        ]
      },
      "authoritative_record_sha256": "6f23da95e5e3baa61e5c86878f0c27ccb97765b54a62bac8bc4303fd40617961",
      "exact_edge_ids": [
        "DEP-089",
        "DEP-091"
      ],
      "exact_directions": [
        "AFQR-17 -> AFQR-18 (DEP-089 environment_handoff)",
        "AFQR-18 -> AFQR-17 (DEP-091 space_handoff)"
      ],
      "classification": "bounded_feedback_rule",
      "breaker_or_phase_rule": "AFQR-17 environmental process constraints and AFQR-18 spatial/topology constraints may inform later owner-qualified evaluation. Neither handoff recursively authors the other domain or validates itself; unresolved generic owner-contract needs remain escalated.",
      "owner_separation": "AFQR-17 environmental process constraints and AFQR-18 spatial/topology constraints may inform later owner-qualified evaluation. Neither handoff recursively authors the other domain or validates itself; unresolved generic owner-contract needs remain escalated.",
      "prohibited_recursion": "neither output self-validates or recursively authors the other",
      "evidence": [
        "SRC-0180",
        "SRC-0207",
        "SRC-0207",
        "SRC-0180"
      ],
      "r1d_treatments": [
        {
          "family": "world",
          "record_sha256": "6f23da95e5e3baa61e5c86878f0c27ccb97765b54a62bac8bc4303fd40617961",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    }
  ],
  "dependency_risk_decisions": [
    {
      "risk_id": "CYCLE-RISK-001",
      "authoritative_record": {
        "reclassification_id": "CYCLE-RISK-001",
        "edge_ids": [
          "DEP-022",
          "DEP-062"
        ],
        "afqrs": [
          "AFQR-02",
          "AFQR-09"
        ],
        "classification": "dependency_risk_not_recorded_cycle_group",
        "reason": "Command lifecycle and governed-relation lifecycle can constrain later processing, but R1A names only AFQR-02/AFQR-04 as the command reciprocal cycle group. AFQR-02 and AFQR-09 retain separate owners; no recursive authority is authorized."
      },
      "authoritative_record_sha256": "93c766c0b66dbe46a5f8495962e532613158a819ef929b281e5df76fe37004af",
      "exact_edge_ids": [
        "DEP-022",
        "DEP-062"
      ],
      "exact_directions": [
        "AFQR-02 -> AFQR-09",
        "AFQR-09 -> AFQR-02"
      ],
      "classification": "dependency_risk_not_recorded_cycle_group",
      "breaker_or_phase_rule": "Command lifecycle and governed-relation lifecycle can constrain later processing, but R1A names only AFQR-02/AFQR-04 as the command reciprocal cycle group. AFQR-02 and AFQR-09 retain separate owners; no recursive authority is authorized.",
      "owner_separation": "Command lifecycle and governed-relation lifecycle can constrain later processing, but R1A names only AFQR-02/AFQR-04 as the command reciprocal cycle group. AFQR-02 and AFQR-09 retain separate owners; no recursive authority is authorized.",
      "prohibited_recursion": "no recursive authority or combined owner",
      "evidence": [
        "SRC-0005",
        "SRC-0012",
        "SRC-0012",
        "SRC-0005"
      ],
      "r1d_treatments": [
        {
          "family": "core",
          "record_sha256": "93c766c0b66dbe46a5f8495962e532613158a819ef929b281e5df76fe37004af",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    },
    {
      "risk_id": "CYCLE-RISK-002",
      "authoritative_record": {
        "reclassification_id": "CYCLE-RISK-002",
        "edge_ids": [
          "DEP-028",
          "DEP-063"
        ],
        "afqrs": [
          "AFQR-04",
          "AFQR-09"
        ],
        "classification": "dependency_risk_not_recorded_cycle_group",
        "reason": "Logical/causal ordering and relation lifecycle exchange bounded inputs, but R1A does not designate this pair as one of its four reciprocal cycle groups. Scheduling cannot author relations and relations cannot author logical time."
      },
      "authoritative_record_sha256": "69c9a722932d3bb8a2133181144dc2c4146fc15a2668f119bb55895e038ea0e2",
      "exact_edge_ids": [
        "DEP-028",
        "DEP-063"
      ],
      "exact_directions": [
        "AFQR-04 -> AFQR-09",
        "AFQR-09 -> AFQR-04"
      ],
      "classification": "dependency_risk_not_recorded_cycle_group",
      "breaker_or_phase_rule": "Logical/causal ordering and relation lifecycle exchange bounded inputs, but R1A does not designate this pair as one of its four reciprocal cycle groups. Scheduling cannot author relations and relations cannot author logical time.",
      "owner_separation": "Logical/causal ordering and relation lifecycle exchange bounded inputs, but R1A does not designate this pair as one of its four reciprocal cycle groups. Scheduling cannot author relations and relations cannot author logical time.",
      "prohibited_recursion": "no recursive authority or combined owner",
      "evidence": [
        "SRC-0007",
        "SRC-0012",
        "SRC-0012",
        "SRC-0007"
      ],
      "r1d_treatments": [
        {
          "family": "core",
          "record_sha256": "69c9a722932d3bb8a2133181144dc2c4146fc15a2668f119bb55895e038ea0e2",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    },
    {
      "risk_id": "CYCLE-RISK-003",
      "authoritative_record": {
        "reclassification_id": "CYCLE-RISK-003",
        "edge_ids": [
          "DEP-049",
          "DEP-064"
        ],
        "afqrs": [
          "AFQR-06",
          "AFQR-09"
        ],
        "classification": "dependency_risk_not_recorded_cycle_group",
        "reason": "Claims may concern governed relations and relation records may be offered in arbitration, but AFQR-06 and AFQR-09 retain separate adjudication and relation ownership. Neither handoff self-certifies the other."
      },
      "authoritative_record_sha256": "611c9a4679c95e8eec498f0f0042d3b0286f59ff1e5d892023f8efb9e16d7935",
      "exact_edge_ids": [
        "DEP-049",
        "DEP-064"
      ],
      "exact_directions": [
        "AFQR-06 -> AFQR-09",
        "AFQR-09 -> AFQR-06"
      ],
      "classification": "dependency_risk_not_recorded_cycle_group",
      "breaker_or_phase_rule": "Claims may concern governed relations and relation records may be offered in arbitration, but AFQR-06 and AFQR-09 retain separate adjudication and relation ownership. Neither handoff self-certifies the other.",
      "owner_separation": "Claims may concern governed relations and relation records may be offered in arbitration, but AFQR-06 and AFQR-09 retain separate adjudication and relation ownership. Neither handoff self-certifies the other.",
      "prohibited_recursion": "no recursive authority or combined owner",
      "evidence": [
        "SRC-0009",
        "SRC-0012",
        "SRC-0012",
        "SRC-0009"
      ],
      "r1d_treatments": [
        {
          "family": "core",
          "record_sha256": "611c9a4679c95e8eec498f0f0042d3b0286f59ff1e5d892023f8efb9e16d7935",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    },
    {
      "risk_id": "CYCLE-RISK-004",
      "authoritative_record": {
        "reclassification_id": "CYCLE-RISK-004",
        "edge_ids": [
          "DEP-054",
          "DEP-066"
        ],
        "afqrs": [
          "AFQR-08",
          "AFQR-09"
        ],
        "classification": "dependency_risk_not_recorded_cycle_group",
        "reason": "Identity evidence and relation lifecycle can refer to each other, but identity does not create a governed relation and a relation does not create identity. R1A does not list this pair among the four recorded reciprocal groups."
      },
      "authoritative_record_sha256": "496db13ace0ce325c2fd4972792223cc70bb660af00f0e7dde797d1777615c0b",
      "exact_edge_ids": [
        "DEP-054",
        "DEP-066"
      ],
      "exact_directions": [
        "AFQR-08 -> AFQR-09",
        "AFQR-09 -> AFQR-08"
      ],
      "classification": "dependency_risk_not_recorded_cycle_group",
      "breaker_or_phase_rule": "Identity evidence and relation lifecycle can refer to each other, but identity does not create a governed relation and a relation does not create identity. R1A does not list this pair among the four recorded reciprocal groups.",
      "owner_separation": "Identity evidence and relation lifecycle can refer to each other, but identity does not create a governed relation and a relation does not create identity. R1A does not list this pair among the four recorded reciprocal groups.",
      "prohibited_recursion": "no recursive authority or combined owner",
      "evidence": [
        "SRC-0011",
        "SRC-0012",
        "SRC-0012",
        "SRC-0011"
      ],
      "r1d_treatments": [
        {
          "family": "core",
          "record_sha256": "496db13ace0ce325c2fd4972792223cc70bb660af00f0e7dde797d1777615c0b",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        }
      ],
      "mismatches": [],
      "result": "pass"
    }
  ],
  "missing_substrate_decisions": [
    {
      "decision_id": "R1E-SUB-001-DECISION-001",
      "substrate_id": "SUB-001",
      "decision": "accepted_as_classified_deferred_substrate",
      "authoritative_r1c_record": {
        "substrate_id": "SUB-001",
        "name": "generalized governed-relation registry",
        "why_required": "Dependency, obligation, revocation, jurisdiction, and social/institutional relation pressure requires owner-qualified relation references without turning reachability or storage into legal or social authority.",
        "requiring_afqrs": [
          "AFQR-09",
          "AFQR-13",
          "AFQR-15"
        ],
        "source_evidence_records": [
          "SRC-0012",
          "SRC-0082",
          "SRC-0125"
        ],
        "source_evidence_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
        ],
        "future_doctrine_owner": "unresolved: AFQR-09 owns governed relation/dependency semantics while COLL-08 prevents a universal jurisdiction, institution, authority, dependency, or social-state owner",
        "later_gate": "R1D doctrine-family contracts; any implementation is deferred beyond R1",
        "r1c_may_define": "R1C defines typed relation handoff and non-transfer boundaries and preserves COLL-08; it does not define a registry schema.",
        "r1c_must_not_implement": "must_not_implement production schemas, runtime services, persistence, conversion behavior, bridge code, or production imports",
        "failure_or_collapse_risk": "Omission collapses dependency into obligation, reachability into jurisdiction, or relation records into institutional authority/social standing.",
        "status": "classified_unimplemented"
      },
      "authoritative_r1c_record_sha256": "ab6187520e0c5d9cd3e12edfb7c87471fa10772abd1d19b47f86254e573848a8",
      "requiring_afqrs": [
        "AFQR-09",
        "AFQR-13",
        "AFQR-15"
      ],
      "evidence_identifiers": [
        "SRC-0012",
        "SRC-0082",
        "SRC-0125"
      ],
      "evidence_locators": [
        {
          "evidence_id": "SRC-0012",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0082",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0125",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
      ],
      "accepted_future_owner_posture": "unresolved: AFQR-09 owns governed relation/dependency semantics while COLL-08 prevents a universal jurisdiction, institution, authority, dependency, or social-state owner",
      "owner_separation_rule": "Each requiring AFQR retains its source-backed semantics; the substrate is only a future typed coordination boundary.",
      "combined_owner_prohibition": true,
      "implementation_status": "unimplemented",
      "historical_pre_r1e_blocking_effect": "blocks final R1/R2-R6/RT-002G implementation decisions, not bounded R1C",
      "current_post_r1e_blocking_effect": "does not block R1 completion or R2 doctrine-drift review; continues to block implementation until an explicitly authorized later gate",
      "lawful_next_gate": "R1D doctrine-family contracts; any implementation is deferred beyond R1",
      "acceptance_rationale": "Exact owners, evidence, handoffs, collapse risk, and later escalation path are classified without implementing the substrate.",
      "ledger_status": "accepted_deferred_by_r1e",
      "mismatch_list": [],
      "result": "pass"
    },
    {
      "decision_id": "R1E-SUB-002-DECISION-001",
      "substrate_id": "SUB-002",
      "decision": "accepted_as_classified_deferred_substrate",
      "authoritative_r1c_record": {
        "substrate_id": "SUB-002",
        "name": "generalized bitemporal truth/evidence store",
        "why_required": "Claim evidence, epistemic state, observation, logical time, and hidden-truth pressure require distinct owner-qualified valid-time and record-time handoffs without equating observation, evidence, or schedule with truth.",
        "requiring_afqrs": [
          "AFQR-04",
          "AFQR-06",
          "AFQR-10",
          "AFQR-20"
        ],
        "source_evidence_records": [
          "SRC-0007",
          "SRC-0009",
          "SRC-0022",
          "SRC-0255"
        ],
        "source_evidence_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
        ],
        "future_doctrine_owner": "unresolved cross-owner substrate: AFQR-04 time, AFQR-06 arbitration evidence, AFQR-10 epistemic/truth, and AFQR-20 sensing retain their own semantics",
        "later_gate": "R1D doctrine-family contracts; persistence and runtime realization require a later authorized gate",
        "r1c_may_define": "R1C defines ordering, provenance, visibility, and non-promotion invariants only.",
        "r1c_must_not_implement": "must_not_implement production schemas, runtime services, persistence, conversion behavior, bridge code, or production imports",
        "failure_or_collapse_risk": "Omission permits hidden-truth leakage, retroactive evidence overwrite, or logical time to manufacture truth/admissibility.",
        "status": "classified_unimplemented"
      },
      "authoritative_r1c_record_sha256": "fae3e7aa03ee1d42a330647e024d402064b8e1eae3205821bcab74e19a4e3e29",
      "requiring_afqrs": [
        "AFQR-04",
        "AFQR-06",
        "AFQR-10",
        "AFQR-20"
      ],
      "evidence_identifiers": [
        "SRC-0007",
        "SRC-0009",
        "SRC-0022",
        "SRC-0255"
      ],
      "evidence_locators": [
        {
          "evidence_id": "SRC-0007",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0009",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0022",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0255",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
      ],
      "accepted_future_owner_posture": "unresolved cross-owner substrate: AFQR-04 time, AFQR-06 arbitration evidence, AFQR-10 epistemic/truth, and AFQR-20 sensing retain their own semantics",
      "owner_separation_rule": "Each requiring AFQR retains its source-backed semantics; the substrate is only a future typed coordination boundary.",
      "combined_owner_prohibition": true,
      "implementation_status": "unimplemented",
      "historical_pre_r1e_blocking_effect": "blocks final R1/R2-R6/RT-002G implementation decisions, not bounded R1C",
      "current_post_r1e_blocking_effect": "does not block R1 completion or R2 doctrine-drift review; continues to block implementation until an explicitly authorized later gate",
      "lawful_next_gate": "R1D doctrine-family contracts; persistence and runtime realization require a later authorized gate",
      "acceptance_rationale": "Exact owners, evidence, handoffs, collapse risk, and later escalation path are classified without implementing the substrate.",
      "ledger_status": "accepted_deferred_by_r1e",
      "mismatch_list": [],
      "result": "pass"
    },
    {
      "decision_id": "R1E-SUB-003-DECISION-001",
      "substrate_id": "SUB-003",
      "decision": "accepted_as_classified_deferred_substrate",
      "authoritative_r1c_record": {
        "substrate_id": "SUB-003",
        "name": "generalized owner-reducer transaction journal",
        "why_required": "State ownership, commitment, recovery, replay, command lifecycle, causal order, and dependency consequences require durable receipts that preserve each domain owner and bounded cascade ordering.",
        "requiring_afqrs": [
          "AFQR-01",
          "AFQR-02",
          "AFQR-04",
          "AFQR-09"
        ],
        "source_evidence_records": [
          "SRC-0004",
          "SRC-0005",
          "SRC-0007",
          "SRC-0012"
        ],
        "source_evidence_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ],
        "future_doctrine_owner": "AFQR-01 for transition/commitment journal doctrine; participating domain semantics remain with AFQR-02, AFQR-04, and AFQR-09",
        "later_gate": "R1D transition/lifecycle doctrine; runtime journal implementation remains blocked for later runtime gates",
        "r1c_may_define": "R1C defines owner-preserving lifecycle and cascade handoff constraints, not journal fields or reducers.",
        "r1c_must_not_implement": "must_not_implement production schemas, runtime services, persistence, conversion behavior, bridge code, or production imports",
        "failure_or_collapse_risk": "Omission allows replay to duplicate commitment, recovery to rewrite command identity, or causal/dependency consequences to recurse without bounds.",
        "status": "classified_unimplemented"
      },
      "authoritative_r1c_record_sha256": "44f8cb1ed0c6dda0df7bf186f39295ca007c1a4eb2752b4aac36e41e1843d2c5",
      "requiring_afqrs": [
        "AFQR-01",
        "AFQR-02",
        "AFQR-04",
        "AFQR-09"
      ],
      "evidence_identifiers": [
        "SRC-0004",
        "SRC-0005",
        "SRC-0007",
        "SRC-0012"
      ],
      "evidence_locators": [
        {
          "evidence_id": "SRC-0004",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0005",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0007",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0012",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
      ],
      "accepted_future_owner_posture": "AFQR-01 for transition/commitment journal doctrine; participating domain semantics remain with AFQR-02, AFQR-04, and AFQR-09",
      "owner_separation_rule": "Each requiring AFQR retains its source-backed semantics; the substrate is only a future typed coordination boundary.",
      "combined_owner_prohibition": true,
      "implementation_status": "unimplemented",
      "historical_pre_r1e_blocking_effect": "blocks final R1/R2-R6/RT-002G implementation decisions, not bounded R1C",
      "current_post_r1e_blocking_effect": "does not block R1 completion or R2 doctrine-drift review; continues to block implementation until an explicitly authorized later gate",
      "lawful_next_gate": "R1D transition/lifecycle doctrine; runtime journal implementation remains blocked for later runtime gates",
      "acceptance_rationale": "Exact owners, evidence, handoffs, collapse risk, and later escalation path are classified without implementing the substrate.",
      "ledger_status": "accepted_deferred_by_r1e",
      "mismatch_list": [],
      "result": "pass"
    },
    {
      "decision_id": "R1E-SUB-004-DECISION-001",
      "substrate_id": "SUB-004",
      "decision": "accepted_as_classified_deferred_substrate",
      "authoritative_r1c_record": {
        "substrate_id": "SUB-004",
        "name": "registered interface/bridge hypergraph",
        "why_required": "AFQR-05 interface, adapter, and bridge ownership requires registered typed cross-system compatibility without allowing bridge compatibility to transfer semantic ownership.",
        "requiring_afqrs": [
          "AFQR-05"
        ],
        "source_evidence_records": [
          "SRC-0008"
        ],
        "source_evidence_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md"
        ],
        "future_doctrine_owner": "AFQR-05",
        "later_gate": "R1D interface/bridge doctrine; registration services and adapters require a later authorized implementation gate",
        "r1c_may_define": "R1C defines bridge nonownership, typed endpoint, and compatibility handoff constraints only.",
        "r1c_must_not_implement": "must_not_implement production schemas, runtime services, persistence, conversion behavior, bridge code, or production imports",
        "failure_or_collapse_risk": "Omission encourages pairwise ad hoc adapters, package-symbol ownership inference, and donor-specific compatibility becoming Astra law.",
        "status": "classified_unimplemented"
      },
      "authoritative_r1c_record_sha256": "92ba21f574417e694d609b07bd035c73d30a15b518c67690849a417f9b006ff3",
      "requiring_afqrs": [
        "AFQR-05"
      ],
      "evidence_identifiers": [
        "SRC-0008"
      ],
      "evidence_locators": [
        {
          "evidence_id": "SRC-0008",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md"
      ],
      "accepted_future_owner_posture": "AFQR-05",
      "owner_separation_rule": "Each requiring AFQR retains its source-backed semantics; the substrate is only a future typed coordination boundary.",
      "combined_owner_prohibition": true,
      "implementation_status": "unimplemented",
      "historical_pre_r1e_blocking_effect": "blocks final R1/R2-R6/RT-002G implementation decisions, not bounded R1C",
      "current_post_r1e_blocking_effect": "does not block R1 completion or R2 doctrine-drift review; continues to block implementation until an explicitly authorized later gate",
      "lawful_next_gate": "R1D interface/bridge doctrine; registration services and adapters require a later authorized implementation gate",
      "acceptance_rationale": "Exact owners, evidence, handoffs, collapse risk, and later escalation path are classified without implementing the substrate.",
      "ledger_status": "accepted_deferred_by_r1e",
      "mismatch_list": [],
      "result": "pass"
    },
    {
      "decision_id": "R1E-SUB-005-DECISION-001",
      "substrate_id": "SUB-005",
      "decision": "accepted_as_classified_deferred_substrate",
      "authoritative_r1c_record": {
        "substrate_id": "SUB-005",
        "name": "generalized spatial, signal, embodiment, institution, and social owner contracts",
        "why_required": "Distinct spatial, signal, embodiment, institution, and social handoffs need explicit domain contracts so one substrate or consumer cannot absorb all five semantic domains.",
        "requiring_afqrs": [
          "AFQR-13",
          "AFQR-15",
          "AFQR-16",
          "AFQR-18",
          "AFQR-20"
        ],
        "source_evidence_records": [
          "SRC-0082",
          "SRC-0125",
          "SRC-0152",
          "SRC-0207",
          "SRC-0255"
        ],
        "source_evidence_paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
        ],
        "future_doctrine_owner": "separate source-backed owners: AFQR-18 spatial/topology; AFQR-20 signal/sensing; AFQR-16 embodiment; AFQR-15 institution/jurisdiction; AFQR-13 social state, subject to preserved COLL-03 and COLL-08 seams",
        "later_gate": "R1D separate domain-family doctrine files; no combined runtime substrate is authorized",
        "r1c_may_define": "R1C records separate owner-qualified handoffs and forbids collapsing them into a generic state or relation owner.",
        "r1c_must_not_implement": "must_not_implement production schemas, runtime services, persistence, conversion behavior, bridge code, or production imports",
        "failure_or_collapse_risk": "Omission conflates topology with embodiment, sensing with truth, institution with jurisdiction, or social state with identity/authority.",
        "status": "classified_unimplemented",
        "domain_owner_requirements": [
          {
            "domain": "spatial/topology",
            "owner": "AFQR-18",
            "requiring_afqrs": [
              "AFQR-17",
              "AFQR-18"
            ]
          },
          {
            "domain": "signal/sensing",
            "owner": "AFQR-20",
            "requiring_afqrs": [
              "AFQR-14",
              "AFQR-19",
              "AFQR-20"
            ]
          },
          {
            "domain": "embodiment",
            "owner": "AFQR-16",
            "requiring_afqrs": [
              "AFQR-08",
              "AFQR-16",
              "AFQR-17"
            ]
          },
          {
            "domain": "institution/jurisdiction",
            "owner": "AFQR-15",
            "requiring_afqrs": [
              "AFQR-09",
              "AFQR-13",
              "AFQR-15"
            ],
            "escalation": "COLL-08"
          },
          {
            "domain": "social state",
            "owner": "AFQR-13",
            "requiring_afqrs": [
              "AFQR-08",
              "AFQR-11",
              "AFQR-12",
              "AFQR-13"
            ],
            "escalations": [
              "COLL-03",
              "COLL-10"
            ]
          }
        ]
      },
      "authoritative_r1c_record_sha256": "3f4c31c0928bdb347ed1901660f538ad5d6ce77713a89e9d72d314031a4cb67d",
      "requiring_afqrs": [
        "AFQR-13",
        "AFQR-15",
        "AFQR-16",
        "AFQR-18",
        "AFQR-20"
      ],
      "evidence_identifiers": [
        "SRC-0082",
        "SRC-0125",
        "SRC-0152",
        "SRC-0207",
        "SRC-0255"
      ],
      "evidence_locators": [
        {
          "evidence_id": "SRC-0082",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0125",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0152",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0207",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0255",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
      ],
      "accepted_future_owner_posture": "separate source-backed owners: AFQR-18 spatial/topology; AFQR-20 signal/sensing; AFQR-16 embodiment; AFQR-15 institution/jurisdiction; AFQR-13 social state, subject to preserved COLL-03 and COLL-08 seams",
      "owner_separation_rule": "Each requiring AFQR retains its source-backed semantics; the substrate is only a future typed coordination boundary.",
      "combined_owner_prohibition": true,
      "implementation_status": "unimplemented",
      "historical_pre_r1e_blocking_effect": "blocks final R1/R2-R6/RT-002G implementation decisions, not bounded R1C",
      "current_post_r1e_blocking_effect": "does not block R1 completion or R2 doctrine-drift review; continues to block implementation until an explicitly authorized later gate",
      "lawful_next_gate": "R1D separate domain-family doctrine files; no combined runtime substrate is authorized",
      "acceptance_rationale": "Exact owners, evidence, handoffs, collapse risk, and later escalation path are classified without implementing the substrate.",
      "ledger_status": "accepted_deferred_by_r1e",
      "mismatch_list": [],
      "result": "pass"
    }
  ],
  "global_escalations": [
    {
      "decision_id": "R1E-COLL-03-DECISION-001",
      "collision_id": "COLL-03",
      "terms": [
        "identity",
        "owner",
        "authority",
        "agency",
        "responsibility"
      ],
      "affected_afqrs": [
        "AFQR-01",
        "AFQR-08",
        "AFQR-11",
        "AFQR-15"
      ],
      "r1b_owner_candidates": [
        "AFQR-01",
        "AFQR-08",
        "AFQR-11",
        "AFQR-15",
        "Astra Doctrine Council"
      ],
      "r1b_evidence_records": [
        "SRC-0004",
        "SRC-0011",
        "SRC-0059",
        "SRC-0157"
      ],
      "r1c_evidence": {
        "escalation_id": "R1C-ESC-COLL-03",
        "invariant_ids": [
          "INV-001",
          "INV-005",
          "INV-009"
        ],
        "dependency_edge_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-027",
          "DEP-035",
          "DEP-038",
          "DEP-041",
          "DEP-048",
          "DEP-051",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-061",
          "DEP-066",
          "DEP-067",
          "DEP-069",
          "DEP-072",
          "DEP-076",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-086"
        ],
        "evidence_identifiers": [
          "SRC-0004",
          "SRC-0011",
          "SRC-0041",
          "SRC-0059",
          "SRC-0125",
          "SRC-0157"
        ],
        "evidence_locators": [
          {
            "evidence_id": "SRC-0004",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0011",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0041",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0059",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip::AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
            "path_kind": "manifest_archive_member"
          },
          {
            "evidence_id": "SRC-0125",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0157",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip::AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
            "path_kind": "manifest_archive_member"
          }
        ]
      },
      "r1d_candidate_evidence": [
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
      ],
      "primary_source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
      ],
      "candidate_under_review": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
      "alternatives_considered": [
        {
          "alternative": "universal root owner",
          "rejection_reason": "collapses distinct source-backed semantics"
        },
        {
          "alternative": "consumer ownership",
          "rejection_reason": "handoff consumption never transfers ownership"
        },
        {
          "alternative": "defer blocking",
          "rejection_reason": "existing evidence supports bounded attribution"
        }
      ],
      "rejected_alternatives": [
        "single universal owner",
        "consumer ownership",
        "source-local ambiguity",
        "deferred blocking"
      ],
      "final_attribution_rule": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
      "lawful_qualified_uses": [
        "state/write/resource/property/contract ownership remain qualified or source-local",
        "office, delegation, proxyhood, possession, bodies, clones, vehicles, command, and legal/moral/causal responsibility route to their distinct owners"
      ],
      "prohibited_inferences": [
        "identity does not create agency or responsibility",
        "write or transition ownership does not create personhood or property ownership",
        "agency does not create institutional authority",
        "institutional authority does not create identity"
      ],
      "handoff_rules": [
        "references and typed inputs do not transfer semantic ownership",
        "consumers may validate or apply only their owned semantics"
      ],
      "corpus_scale_pressure_test": [
        {
          "case": "state/write ownership",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "resource and property ownership",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "contractual ownership",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "delegated control",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "institutional office",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "proxyhood and possession",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "cloning and replacement bodies",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "synthetic personhood",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "companion control",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "vehicle operation",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "legal responsibility",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "moral responsibility",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "causal responsibility",
          "disposition": "AFQR-08 owns identity/continuity; AFQR-01 owns qualified transition/write and commitment ownership; AFQR-11 owns purpose-scoped agency, consent, control and responsibility; AFQR-15 owns qualified institutional authority. No universal substantive owner root.",
          "result": "bounded_to_distinct_owner_or_source_local"
        }
      ],
      "decision": "approved_with_qualification",
      "supersession_scope": "supersedes only the historical unresolved disposition; R1B/R1C evidence remains historical",
      "ledger_disposition": "closed_by_r1e",
      "residual_questions": [
        "donor-specific mapping remains R2 work"
      ],
      "downstream_impact": "removes the R1 completion blocker without granting implementation",
      "r1b_evidence_locators": [
        {
          "evidence_id": "SRC-0004",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0011",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0059",
          "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip::AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
          "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip",
          "archive_member_path": "AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
          "path_kind": "manifest_archive_member"
        },
        {
          "evidence_id": "SRC-0157",
          "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip::AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
          "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip",
          "archive_member_path": "AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
          "path_kind": "manifest_archive_member"
        }
      ],
      "r1d_candidate_record": {
        "record_id": "AGENCY-CAND-03",
        "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
        "record_sha256": "f2521486c8b1648766c10efde9b50984291ff6b760fdab9f7e3c89c4c55f395a",
        "exact_fields": {
          "record_id": "AGENCY-CAND-03",
          "collision_id": "COLL-03",
          "exact_terms": [
            "identity",
            "owner",
            "authority",
            "agency",
            "responsibility"
          ],
          "exact_affected_afqrs": [
            "AFQR-01",
            "AFQR-08",
            "AFQR-11",
            "AFQR-15"
          ],
          "exact_r1b_owner_candidates": [
            "AFQR-01",
            "AFQR-08",
            "AFQR-11",
            "AFQR-15",
            "Astra Doctrine Council"
          ],
          "exact_r1b_evidence_record_identifiers": [
            "SRC-0004",
            "SRC-0011",
            "SRC-0059",
            "SRC-0157"
          ],
          "exact_r1b_lawful_interim_usage": "Use accepted qualified forms and explicit AFQR owner scopes only.",
          "exact_r1b_prohibited_interim_usage": "No inference of agency, consent, responsibility, jurisdiction, ownership, or authority from adjacent terms.",
          "participating_agency_family_owners": [
            "AFQR-11",
            "AFQR-15"
          ],
          "external_core_family_owners": [
            "AFQR-01",
            "AFQR-08"
          ],
          "source_paths": [
            "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
            "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
            "working/afqr_consolidation_inputs/manifest.yaml",
            "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
            "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
          ],
          "candidate_attribution_rule": "AFQR-08 owns identity and continuity; AFQR-01 owns only accepted qualified transition/write-owner semantics; AFQR-11 owns purpose-scoped agency, personhood, consent, control, and responsibility doctrine; AFQR-15 owns qualified institutional authority and institutional attribution. None automatically creates another, and no universal substantive owner is invented.",
          "candidate_specific_prohibited_inferences": [
            "identity or continuity proving personhood, agency, control, consent, responsibility, or institutional authority",
            "state transition or write routing proving substantive ownership, personhood, agency, responsibility, or authority",
            "control proving consent; agency proving responsibility; institutional authority proving generic ownership"
          ],
          "candidate_specific_safe_handoffs": [
            "AFQR-08 identity/continuity records to AFQR-11 without personhood or agency inference",
            "AFQR-01 qualified transition/write-owner routing without substantive owner inference",
            "AFQR-11 purpose-scoped action-origin/responsibility output to AFQR-15 without creating institutional authority"
          ],
          "candidate_specific_corpus_scale_risks": [
            "donor property ownership becoming universal personhood or control law",
            "identity-copy or proxy rules silently transferring agency/responsibility",
            "institutional office being treated as universal authority or ownership"
          ],
          "candidate_specific_r1e_review_questions": [
            "Are AFQR-01 qualified write-owner semantics sufficiently separated from substantive owner?",
            "Are identity/personhood/agency/control/consent/responsibility boundaries source-complete?",
            "Does institutional attribution remain qualified without manufacturing a universal owner?"
          ],
          "upstream_r1b_status": "open",
          "upstream_r1c_status": "open",
          "status": "candidate_pending_R1E"
        }
      },
      "primary_evidence_identifiers": [
        "SRC-0004",
        "SRC-0011",
        "SRC-0041",
        "SRC-0125"
      ],
      "primary_evidence_locators": [
        {
          "evidence_id": "SRC-0004",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0011",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0041",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0125",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "lawful_qualified_forms": [
        "identity",
        "owner",
        "authority",
        "agency",
        "responsibility"
      ],
      "residual_r2_questions": [
        "Map donor-specific constructs without promoting donor defaults."
      ]
    },
    {
      "decision_id": "R1E-COLL-08-DECISION-001",
      "collision_id": "COLL-08",
      "terms": [
        "jurisdiction",
        "institution",
        "authority",
        "social state"
      ],
      "affected_afqrs": [
        "AFQR-09",
        "AFQR-13",
        "AFQR-15"
      ],
      "r1b_owner_candidates": [
        "AFQR-09",
        "AFQR-13",
        "AFQR-15",
        "Astra Doctrine Council"
      ],
      "r1b_evidence_records": [
        "SRC-0012",
        "SRC-0110",
        "SRC-0157"
      ],
      "r1c_evidence": {
        "escalation_id": "R1C-ESC-COLL-08",
        "invariant_ids": [
          "INV-001",
          "INV-005",
          "INV-006"
        ],
        "dependency_edge_ids": [
          "DEP-008",
          "DEP-012",
          "DEP-014",
          "DEP-022",
          "DEP-028",
          "DEP-036",
          "DEP-039",
          "DEP-041",
          "DEP-049",
          "DEP-051",
          "DEP-054",
          "DEP-058",
          "DEP-059",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-074",
          "DEP-076",
          "DEP-081",
          "DEP-083",
          "DEP-085",
          "DEP-086"
        ],
        "evidence_identifiers": [
          "SRC-0012",
          "SRC-0082",
          "SRC-0110",
          "SRC-0125",
          "SRC-0157"
        ],
        "evidence_locators": [
          {
            "evidence_id": "SRC-0012",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0082",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0110",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip::AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
            "path_kind": "manifest_archive_member"
          },
          {
            "evidence_id": "SRC-0125",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0157",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip::AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
            "path_kind": "manifest_archive_member"
          }
        ]
      },
      "r1d_candidate_evidence": [
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
      ],
      "primary_source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
      ],
      "candidate_under_review": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
      "alternatives_considered": [
        {
          "alternative": "universal root owner",
          "rejection_reason": "collapses distinct source-backed semantics"
        },
        {
          "alternative": "consumer ownership",
          "rejection_reason": "handoff consumption never transfers ownership"
        },
        {
          "alternative": "defer blocking",
          "rejection_reason": "existing evidence supports bounded attribution"
        }
      ],
      "rejected_alternatives": [
        "single universal owner",
        "consumer ownership",
        "source-local ambiguity",
        "deferred blocking"
      ],
      "final_attribution_rule": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
      "lawful_qualified_uses": [
        "citizenship, membership, employment, office, territory, contracts, emergency power and enforcement require typed institutional attribution",
        "reputation, informal leadership and prestige remain social rather than jurisdictional"
      ],
      "prohibited_inferences": [
        "relation existence, graph reachability, or spatial proximity does not establish jurisdiction",
        "social status or institutional membership does not establish every authority, right, duty, obligation, or jurisdiction",
        "institutional authority does not create general agency or identity"
      ],
      "handoff_rules": [
        "references and typed inputs do not transfer semantic ownership",
        "consumers may validate or apply only their owned semantics"
      ],
      "corpus_scale_pressure_test": [
        {
          "case": "citizenship",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "faction and guild membership",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "employment and military command",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "religious and corporate office",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "territory and extradimensional jurisdiction",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "network and shipboard jurisdiction",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "emergency powers",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "contracts",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "reputation and informal leadership",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "cross-border enforcement",
          "disposition": "AFQR-09 owns governed-relation/dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institutions, jurisdiction, rights, law, adjudication and qualified institutional authority.",
          "result": "bounded_to_distinct_owner_or_source_local"
        }
      ],
      "decision": "approved_with_qualification",
      "supersession_scope": "supersedes only the historical unresolved disposition; R1B/R1C evidence remains historical",
      "ledger_disposition": "closed_by_r1e",
      "residual_questions": [
        "donor-specific mapping remains R2 work"
      ],
      "downstream_impact": "removes the R1 completion blocker without granting implementation",
      "r1b_evidence_locators": [
        {
          "evidence_id": "SRC-0012",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0110",
          "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip::AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
          "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip",
          "archive_member_path": "AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
          "path_kind": "manifest_archive_member"
        },
        {
          "evidence_id": "SRC-0157",
          "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip::AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
          "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_16_Ratification_Pack_v1_0.zip",
          "archive_member_path": "AFQR_16_Ratification_Pack_v1_0/fixtures/afqr_16_non_mutating_dry_run.yaml",
          "path_kind": "manifest_archive_member"
        }
      ],
      "r1d_candidate_record": {
        "record_id": "AGENCY-CAND-08",
        "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
        "record_sha256": "48906ee7221b3f1db5211e0b123b5bd1905f630577f76588c68e223a66573c15",
        "exact_fields": {
          "record_id": "AGENCY-CAND-08",
          "collision_id": "COLL-08",
          "exact_terms": [
            "jurisdiction",
            "institution",
            "authority",
            "social state"
          ],
          "exact_affected_afqrs": [
            "AFQR-09",
            "AFQR-13",
            "AFQR-15"
          ],
          "exact_r1b_owner_candidates": [
            "AFQR-09",
            "AFQR-13",
            "AFQR-15",
            "Astra Doctrine Council"
          ],
          "exact_r1b_evidence_record_identifiers": [
            "SRC-0012",
            "SRC-0110",
            "SRC-0157"
          ],
          "exact_r1b_lawful_interim_usage": "Use accepted qualified forms and explicit AFQR owner scopes only.",
          "exact_r1b_prohibited_interim_usage": "No inference of agency, consent, responsibility, jurisdiction, ownership, or authority from adjacent terms.",
          "participating_agency_family_owners": [
            "AFQR-13",
            "AFQR-15"
          ],
          "external_core_family_owners": [
            "AFQR-09"
          ],
          "source_paths": [
            "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
            "working/afqr_consolidation_inputs/manifest.yaml",
            "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
            "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
          ],
          "candidate_attribution_rule": "AFQR-09 owns governed-relation and dependency lifecycle; AFQR-13 owns social state; AFQR-15 owns institution, jurisdiction, and qualified institutional authority. Relation existence does not establish jurisdiction; social status does not establish authority; membership does not establish every jurisdiction, right, duty, or obligation; reachability has no automatic legal effect.",
          "candidate_specific_prohibited_inferences": [
            "governed relation or dependency proving jurisdiction, institution, social status, or authority",
            "social status, reputation, or affiliation proving institutional office or authority",
            "institutional membership or graph reachability proving every jurisdiction, right, duty, obligation, or legal effect"
          ],
          "candidate_specific_safe_handoffs": [
            "AFQR-09 typed relation lifecycle handoff to AFQR-13 without social standing inference",
            "AFQR-09 typed governed relation handoff to AFQR-15 for separately adjudicated jurisdiction",
            "AFQR-13 social context handoff to AFQR-15 without institutional authority transfer"
          ],
          "candidate_specific_corpus_scale_risks": [
            "faction graphs becoming universal legal jurisdiction",
            "reputation scores becoming offices, rights, or obligations",
            "membership tags importing donor law or political assumptions"
          ],
          "candidate_specific_r1e_review_questions": [
            "Are relation lifecycle and social association still distinct?",
            "Are membership, jurisdiction, rights, duties, and authority independently typed?",
            "Can reachability ever be consumed without creating legal effect?"
          ],
          "upstream_r1b_status": "open",
          "upstream_r1c_status": "open",
          "status": "candidate_pending_R1E"
        }
      },
      "primary_evidence_identifiers": [
        "SRC-0012",
        "SRC-0082",
        "SRC-0125"
      ],
      "primary_evidence_locators": [
        {
          "evidence_id": "SRC-0012",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0082",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0125",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "lawful_qualified_forms": [
        "jurisdiction",
        "institution",
        "authority",
        "social state"
      ],
      "residual_r2_questions": [
        "Map donor-specific constructs without promoting donor defaults."
      ]
    },
    {
      "decision_id": "R1E-COLL-10-DECISION-001",
      "collision_id": "COLL-10",
      "terms": [
        "motivation",
        "behavior",
        "agency",
        "responsibility",
        "social state"
      ],
      "affected_afqrs": [
        "AFQR-11",
        "AFQR-12",
        "AFQR-13"
      ],
      "r1b_owner_candidates": [
        "AFQR-11",
        "AFQR-12",
        "AFQR-13",
        "Astra Doctrine Council"
      ],
      "r1b_evidence_records": [
        "SRC-0059",
        "SRC-0092",
        "SRC-0110"
      ],
      "r1c_evidence": {
        "escalation_id": "R1C-ESC-COLL-10",
        "invariant_ids": [
          "INV-005",
          "INV-006",
          "INV-008"
        ],
        "dependency_edge_ids": [
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-038",
          "DEP-039",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-067",
          "DEP-068",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-085"
        ],
        "evidence_identifiers": [
          "SRC-0041",
          "SRC-0059",
          "SRC-0072",
          "SRC-0082",
          "SRC-0092",
          "SRC-0110"
        ],
        "evidence_locators": [
          {
            "evidence_id": "SRC-0041",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0059",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip::AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
            "path_kind": "manifest_archive_member"
          },
          {
            "evidence_id": "SRC-0072",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0082",
            "path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
            "path_kind": "materialized_normalized_file"
          },
          {
            "evidence_id": "SRC-0092",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_13_Ratification_Pack_v1_0.zip::AFQR_13_Ratification_Pack_v1_0/manifest/artifact_manifest.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_13_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_13_Ratification_Pack_v1_0/manifest/artifact_manifest.yaml",
            "path_kind": "manifest_archive_member"
          },
          {
            "evidence_id": "SRC-0110",
            "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip::AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
            "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip",
            "archive_member_path": "AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
            "path_kind": "manifest_archive_member"
          }
        ]
      },
      "r1d_candidate_evidence": [
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
      ],
      "primary_source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
      ],
      "candidate_under_review": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
      "alternatives_considered": [
        {
          "alternative": "universal root owner",
          "rejection_reason": "collapses distinct source-backed semantics"
        },
        {
          "alternative": "consumer ownership",
          "rejection_reason": "handoff consumption never transfers ownership"
        },
        {
          "alternative": "defer blocking",
          "rejection_reason": "existing evidence supports bounded attribution"
        }
      ],
      "rejected_alternatives": [
        "single universal owner",
        "consumer ownership",
        "source-local ambiguity",
        "deferred blocking"
      ],
      "final_attribution_rule": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
      "lawful_qualified_uses": [
        "compulsion, control, addiction, trauma, capacity and coercion are evidence inputs to AFQR-11 attribution",
        "AI, swarms and collective agents require purpose-scoped agency; causal contribution remains distinct from legal or moral responsibility"
      ],
      "prohibited_inferences": [
        "motive, predicted behavior, emotion, reputation, or social classification does not establish agency or responsibility",
        "observed behavior alone does not establish responsibility",
        "behavioral prediction is neither authorization nor adjudication"
      ],
      "handoff_rules": [
        "references and typed inputs do not transfer semantic ownership",
        "consumers may validate or apply only their owned semantics"
      ],
      "corpus_scale_pressure_test": [
        {
          "case": "compulsion and mind control",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "possession",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "addiction and trauma",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "fear and morale",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "ideology and conditioning",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "programmed behavior and AI",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "swarms and collective agents",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "coercion and misinformation",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "diminished capacity",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "instinct and habit",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "reputation",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "legal culpability",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "moral blame",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        },
        {
          "case": "causal contribution",
          "disposition": "AFQR-12 owns motivational/behavioral state; AFQR-11 owns agency, consent, control, coercion, decision authority and responsibility; AFQR-13 owns social state.",
          "result": "bounded_to_distinct_owner_or_source_local"
        }
      ],
      "decision": "approved_with_qualification",
      "supersession_scope": "supersedes only the historical unresolved disposition; R1B/R1C evidence remains historical",
      "ledger_disposition": "closed_by_r1e",
      "residual_questions": [
        "donor-specific mapping remains R2 work"
      ],
      "downstream_impact": "removes the R1 completion blocker without granting implementation",
      "r1b_evidence_locators": [
        {
          "evidence_id": "SRC-0059",
          "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip::AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
          "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_11_Ratification_Pack_v1_0.zip",
          "archive_member_path": "AFQR_11_Ratification_Pack_v1_0/sources/external_research_synthesis.yaml",
          "path_kind": "manifest_archive_member"
        },
        {
          "evidence_id": "SRC-0092",
          "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_13_Ratification_Pack_v1_0.zip::AFQR_13_Ratification_Pack_v1_0/manifest/artifact_manifest.yaml",
          "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_13_Ratification_Pack_v1_0.zip",
          "archive_member_path": "AFQR_13_Ratification_Pack_v1_0/manifest/artifact_manifest.yaml",
          "path_kind": "manifest_archive_member"
        },
        {
          "evidence_id": "SRC-0110",
          "path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip::AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
          "archive_path": "working/afqr_consolidation_inputs/incoming/Astra_AFQR_14_Ratification_Pack_v1_0.zip",
          "archive_member_path": "AFQR_14_Ratification_Pack_v1_0/fixtures/persistent_rival_negotiation_typed_graph.yaml",
          "path_kind": "manifest_archive_member"
        }
      ],
      "r1d_candidate_record": {
        "record_id": "AGENCY-CAND-10",
        "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
        "record_sha256": "d299ac2bb145c0e8ec3d4a617aaa68285992043e01a95f6d3887b511a2e69d8e",
        "exact_fields": {
          "record_id": "AGENCY-CAND-10",
          "collision_id": "COLL-10",
          "exact_terms": [
            "motivation",
            "behavior",
            "agency",
            "responsibility",
            "social state"
          ],
          "exact_affected_afqrs": [
            "AFQR-11",
            "AFQR-12",
            "AFQR-13"
          ],
          "exact_r1b_owner_candidates": [
            "AFQR-11",
            "AFQR-12",
            "AFQR-13",
            "Astra Doctrine Council"
          ],
          "exact_r1b_evidence_record_identifiers": [
            "SRC-0059",
            "SRC-0092",
            "SRC-0110"
          ],
          "exact_r1b_lawful_interim_usage": "Use accepted qualified forms and explicit AFQR owner scopes only.",
          "exact_r1b_prohibited_interim_usage": "No inference of agency, consent, responsibility, jurisdiction, ownership, or authority from adjacent terms.",
          "participating_agency_family_owners": [
            "AFQR-11",
            "AFQR-12",
            "AFQR-13"
          ],
          "external_core_family_owners": [],
          "source_paths": [
            "working/afqr_consolidation_inputs/manifest.yaml",
            "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
            "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
            "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
          ],
          "candidate_attribution_rule": "AFQR-12 owns motivation and behavioral-state doctrine; AFQR-11 owns agency and responsibility doctrine; AFQR-13 owns social state. Motive, emotion, personality, predicted or observed behavior, reputation, and social classification do not establish agency or responsibility; prediction is neither authorization nor adjudication.",
          "candidate_specific_prohibited_inferences": [
            "motive, emotion, personality, drive, or predicted behavior proving agency, consent, choice, or responsibility",
            "observed behavior proving motive, authorization, culpability, or responsibility",
            "reputation or social classification proving agency, incapacity, responsibility, or adjudicated status"
          ],
          "candidate_specific_safe_handoffs": [
            "AFQR-12 bounded predictions to AFQR-11 as nonauthoritative decision inputs",
            "AFQR-11 provenance/responsibility outputs to AFQR-13 without generating reputation automatically",
            "AFQR-13 audience-relative social records to AFQR-12 without determining behavior"
          ],
          "candidate_specific_corpus_scale_risks": [
            "alignment or personality models becoming deterministic responsibility rules",
            "predictive AI authoring actor choice or authorization",
            "reputation, sanity, corruption, caste, or faction labels becoming culpability"
          ],
          "candidate_specific_r1e_review_questions": [
            "Do all behavioral predictions remain nonauthoritative?",
            "Are agency and responsibility evaluated independently from motive and observed behavior?",
            "Can social classification influence without determining agency or culpability?"
          ],
          "upstream_r1b_status": "open",
          "upstream_r1c_status": "open",
          "status": "candidate_pending_R1E"
        }
      },
      "primary_evidence_identifiers": [
        "SRC-0041",
        "SRC-0072",
        "SRC-0082"
      ],
      "primary_evidence_locators": [
        {
          "evidence_id": "SRC-0041",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0072",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
          "path_kind": "materialized_normalized_file"
        },
        {
          "evidence_id": "SRC-0082",
          "path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
          "path_kind": "materialized_normalized_file"
        }
      ],
      "lawful_qualified_forms": [
        "motivation",
        "behavior",
        "agency",
        "responsibility",
        "social state"
      ],
      "residual_r2_questions": [
        "Map donor-specific constructs without promoting donor defaults."
      ]
    }
  ],
  "escalation_ledger_reconciliation": {
    "pre_review_open_set": [
      "COLL-03",
      "COLL-08",
      "COLL-10"
    ],
    "collision_status": "closed_by_r1e",
    "substrate_status": "accepted_deferred_by_r1e",
    "historical_entries_preserved": true
  },
  "cross_artifact_consistency_matrix": [
    {
      "matrix_id": "CONS-001",
      "producer_artifact": "R1A",
      "consumer_artifact": "R1B",
      "comparison_class": "authority evidence to vocabulary",
      "exact_compared_record_sets": {
        "producer_ids": [
          "AFQR-01",
          "AFQR-02",
          "AFQR-03",
          "AFQR-04",
          "AFQR-05",
          "AFQR-06",
          "AFQR-07",
          "AFQR-08",
          "AFQR-09",
          "AFQR-10",
          "AFQR-11",
          "AFQR-12",
          "AFQR-13",
          "AFQR-14",
          "AFQR-15",
          "AFQR-16",
          "AFQR-17",
          "AFQR-18",
          "AFQR-19",
          "AFQR-20"
        ],
        "consumer_ids": [
          "TERM-001",
          "TERM-002",
          "TERM-003",
          "TERM-004",
          "TERM-005",
          "TERM-006",
          "TERM-007",
          "TERM-008",
          "TERM-009",
          "TERM-010",
          "TERM-011",
          "TERM-012",
          "TERM-013",
          "TERM-014",
          "TERM-015",
          "TERM-016",
          "TERM-017",
          "TERM-018",
          "TERM-019",
          "TERM-020",
          "TERM-021",
          "TERM-022",
          "TERM-023",
          "TERM-024",
          "TERM-025",
          "TERM-026",
          "TERM-027",
          "TERM-028",
          "TERM-029",
          "TERM-030",
          "TERM-031",
          "TERM-032",
          "TERM-033",
          "TERM-034",
          "TERM-035",
          "TERM-036",
          "TERM-037",
          "TERM-038",
          "TERM-039",
          "TERM-040",
          "TERM-041"
        ]
      },
      "exact_record_counts": {
        "producer": 20,
        "consumer": 41
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "228d2cc962e4092446e6edf191eac6040f6579c11e8bee231293d820ba4698bb",
        "consumer_sha256": "0ca272f7358128204cd32e245846fa11116a65d38f5c47518520f7d55df5a963"
      },
      "comparison_rules": [
        "authority evidence to vocabulary",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml",
        "working/afqr_consolidation_inputs/manifest.yaml",
        "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-002",
      "producer_artifact": "R1A",
      "consumer_artifact": "R1C",
      "comparison_class": "authority evidence to dependencies",
      "exact_compared_record_sets": {
        "producer_ids": [
          "AFQR-01",
          "AFQR-02",
          "AFQR-03",
          "AFQR-04",
          "AFQR-05",
          "AFQR-06",
          "AFQR-07",
          "AFQR-08",
          "AFQR-09",
          "AFQR-10",
          "AFQR-11",
          "AFQR-12",
          "AFQR-13",
          "AFQR-14",
          "AFQR-15",
          "AFQR-16",
          "AFQR-17",
          "AFQR-18",
          "AFQR-19",
          "AFQR-20"
        ],
        "consumer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-023",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-050",
          "DEP-051",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-085",
          "DEP-086",
          "DEP-087",
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094"
        ]
      },
      "exact_record_counts": {
        "producer": 20,
        "consumer": 94
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "228d2cc962e4092446e6edf191eac6040f6579c11e8bee231293d820ba4698bb",
        "consumer_sha256": "b2e3416d2f8b497df5ee6635f7325e10e4ebd911be37ef2dfa65dbb62ec3c0f5"
      },
      "comparison_rules": [
        "authority evidence to dependencies",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/reviews/afqr_01_20_authority_status_index.yaml",
        "working/afqr_consolidation_inputs/manifest.yaml",
        "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-003",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1C",
      "comparison_class": "term bindings",
      "exact_compared_record_sets": {
        "producer_ids": [
          "TERM-001",
          "TERM-002",
          "TERM-003",
          "TERM-004",
          "TERM-005",
          "TERM-006",
          "TERM-007",
          "TERM-008",
          "TERM-009",
          "TERM-010",
          "TERM-011",
          "TERM-012",
          "TERM-013",
          "TERM-014",
          "TERM-015",
          "TERM-016",
          "TERM-017",
          "TERM-018",
          "TERM-019",
          "TERM-020",
          "TERM-021",
          "TERM-022",
          "TERM-023",
          "TERM-024",
          "TERM-025",
          "TERM-026",
          "TERM-027",
          "TERM-028",
          "TERM-029",
          "TERM-030",
          "TERM-031",
          "TERM-032",
          "TERM-033",
          "TERM-034",
          "TERM-035",
          "TERM-036",
          "TERM-037",
          "TERM-038",
          "TERM-039",
          "TERM-040",
          "TERM-041"
        ],
        "consumer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-023",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-050",
          "DEP-051",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-085",
          "DEP-086",
          "DEP-087",
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094"
        ]
      },
      "exact_record_counts": {
        "producer": 41,
        "consumer": 94
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "0ca272f7358128204cd32e245846fa11116a65d38f5c47518520f7d55df5a963",
        "consumer_sha256": "b2e3416d2f8b497df5ee6635f7325e10e4ebd911be37ef2dfa65dbb62ec3c0f5"
      },
      "comparison_rules": [
        "term bindings",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml",
        "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-004",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1D-CORE",
      "comparison_class": "owned terms",
      "exact_compared_record_sets": {
        "producer_ids": [
          "TERM-001",
          "TERM-002",
          "TERM-003",
          "TERM-004",
          "TERM-005",
          "TERM-006",
          "TERM-007",
          "TERM-008",
          "TERM-009",
          "TERM-010",
          "TERM-011",
          "TERM-012",
          "TERM-013",
          "TERM-014",
          "TERM-015",
          "TERM-016",
          "TERM-017",
          "TERM-018",
          "TERM-019",
          "TERM-020",
          "TERM-021",
          "TERM-022",
          "TERM-023",
          "TERM-024",
          "TERM-025",
          "TERM-026",
          "TERM-027",
          "TERM-028",
          "TERM-029",
          "TERM-030",
          "TERM-031",
          "TERM-032",
          "TERM-033",
          "TERM-034",
          "TERM-035",
          "TERM-036",
          "TERM-037",
          "TERM-038",
          "TERM-039",
          "TERM-040",
          "TERM-041"
        ],
        "consumer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "CORE-BND-DEP-009",
          "CORE-BND-DEP-010",
          "CORE-BND-DEP-011",
          "CORE-BND-DEP-012",
          "CORE-BND-DEP-013",
          "CORE-BND-DEP-014",
          "CORE-BND-DEP-015",
          "CORE-BND-DEP-016",
          "CORE-BND-DEP-017",
          "CORE-BND-DEP-018",
          "CORE-BND-DEP-019",
          "CORE-BND-DEP-023",
          "CORE-BND-DEP-029",
          "CORE-BND-DEP-030",
          "CORE-BND-DEP-031",
          "CORE-BND-DEP-037",
          "CORE-BND-DEP-038",
          "CORE-BND-DEP-039",
          "CORE-BND-DEP-040",
          "CORE-BND-DEP-041",
          "CORE-BND-DEP-042",
          "CORE-BND-DEP-043",
          "CORE-BND-DEP-044",
          "CORE-BND-DEP-045",
          "CORE-BND-DEP-046",
          "CORE-BND-DEP-050",
          "CORE-BND-DEP-051",
          "CORE-BND-DEP-055",
          "CORE-BND-DEP-056",
          "CORE-BND-DEP-057",
          "CORE-BND-DEP-058",
          "CORE-BND-DEP-059",
          "CORE-BND-DEP-060",
          "CORE-BND-DEP-067",
          "CORE-BND-DEP-068",
          "CORE-BND-DEP-069",
          "CORE-BND-DEP-070",
          "CORE-BND-DEP-071"
        ]
      },
      "exact_record_counts": {
        "producer": 41,
        "consumer": 71
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "0ca272f7358128204cd32e245846fa11116a65d38f5c47518520f7d55df5a963",
        "consumer_sha256": "64eaf1c5832a56e302d84c8a1d28b603b9da266a1db502136a61c7128ca70f19"
      },
      "comparison_rules": [
        "owned terms",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml",
        "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-005",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1D-AGENCY",
      "comparison_class": "owned terms",
      "exact_compared_record_sets": {
        "producer_ids": [
          "TERM-001",
          "TERM-002",
          "TERM-003",
          "TERM-004",
          "TERM-005",
          "TERM-006",
          "TERM-007",
          "TERM-008",
          "TERM-009",
          "TERM-010",
          "TERM-011",
          "TERM-012",
          "TERM-013",
          "TERM-014",
          "TERM-015",
          "TERM-016",
          "TERM-017",
          "TERM-018",
          "TERM-019",
          "TERM-020",
          "TERM-021",
          "TERM-022",
          "TERM-023",
          "TERM-024",
          "TERM-025",
          "TERM-026",
          "TERM-027",
          "TERM-028",
          "TERM-029",
          "TERM-030",
          "TERM-031",
          "TERM-032",
          "TERM-033",
          "TERM-034",
          "TERM-035",
          "TERM-036",
          "TERM-037",
          "TERM-038",
          "TERM-039",
          "TERM-040",
          "TERM-041"
        ],
        "consumer_ids": [
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-085",
          "DEP-086",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-050",
          "DEP-051",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ]
      },
      "exact_record_counts": {
        "producer": 41,
        "consumer": 37
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "0ca272f7358128204cd32e245846fa11116a65d38f5c47518520f7d55df5a963",
        "consumer_sha256": "e00feb9ea358799638a31b85152a872f32fe36e2474bc886635fd8a4b5794c65"
      },
      "comparison_rules": [
        "owned terms",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml",
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-006",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "owned terms",
      "exact_compared_record_sets": {
        "producer_ids": [
          "TERM-001",
          "TERM-002",
          "TERM-003",
          "TERM-004",
          "TERM-005",
          "TERM-006",
          "TERM-007",
          "TERM-008",
          "TERM-009",
          "TERM-010",
          "TERM-011",
          "TERM-012",
          "TERM-013",
          "TERM-014",
          "TERM-015",
          "TERM-016",
          "TERM-017",
          "TERM-018",
          "TERM-019",
          "TERM-020",
          "TERM-021",
          "TERM-022",
          "TERM-023",
          "TERM-024",
          "TERM-025",
          "TERM-026",
          "TERM-027",
          "TERM-028",
          "TERM-029",
          "TERM-030",
          "TERM-031",
          "TERM-032",
          "TERM-033",
          "TERM-034",
          "TERM-035",
          "TERM-036",
          "TERM-037",
          "TERM-038",
          "TERM-039",
          "TERM-040",
          "TERM-041"
        ],
        "consumer_ids": [
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-023",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-060",
          "DEP-070",
          "DEP-071",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ]
      },
      "exact_record_counts": {
        "producer": 41,
        "consumer": 29
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "0ca272f7358128204cd32e245846fa11116a65d38f5c47518520f7d55df5a963",
        "consumer_sha256": "d4284b6e99b4392e6b96529dbd7f65985e8a80254f733c6fe7f981f62c667c04"
      },
      "comparison_rules": [
        "owned terms",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_shared_vocabulary_and_type_owners.yaml",
        "docs/doctrine/consolidation/afqr_world_action_sensing.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-007",
      "producer_artifact": "R1C",
      "consumer_artifact": "R1D-CORE",
      "comparison_class": "edge projections",
      "exact_compared_record_sets": {
        "producer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-023",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-050",
          "DEP-051",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-085",
          "DEP-086",
          "DEP-087",
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094"
        ],
        "consumer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "CORE-BND-DEP-009",
          "CORE-BND-DEP-010",
          "CORE-BND-DEP-011",
          "CORE-BND-DEP-012",
          "CORE-BND-DEP-013",
          "CORE-BND-DEP-014",
          "CORE-BND-DEP-015",
          "CORE-BND-DEP-016",
          "CORE-BND-DEP-017",
          "CORE-BND-DEP-018",
          "CORE-BND-DEP-019",
          "CORE-BND-DEP-023",
          "CORE-BND-DEP-029",
          "CORE-BND-DEP-030",
          "CORE-BND-DEP-031",
          "CORE-BND-DEP-037",
          "CORE-BND-DEP-038",
          "CORE-BND-DEP-039",
          "CORE-BND-DEP-040",
          "CORE-BND-DEP-041",
          "CORE-BND-DEP-042",
          "CORE-BND-DEP-043",
          "CORE-BND-DEP-044",
          "CORE-BND-DEP-045",
          "CORE-BND-DEP-046",
          "CORE-BND-DEP-050",
          "CORE-BND-DEP-051",
          "CORE-BND-DEP-055",
          "CORE-BND-DEP-056",
          "CORE-BND-DEP-057",
          "CORE-BND-DEP-058",
          "CORE-BND-DEP-059",
          "CORE-BND-DEP-060",
          "CORE-BND-DEP-067",
          "CORE-BND-DEP-068",
          "CORE-BND-DEP-069",
          "CORE-BND-DEP-070",
          "CORE-BND-DEP-071"
        ]
      },
      "exact_record_counts": {
        "producer": 94,
        "consumer": 71
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "b2e3416d2f8b497df5ee6635f7325e10e4ebd911be37ef2dfa65dbb62ec3c0f5",
        "consumer_sha256": "64eaf1c5832a56e302d84c8a1d28b603b9da266a1db502136a61c7128ca70f19"
      },
      "comparison_rules": [
        "edge projections",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",
        "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-008",
      "producer_artifact": "R1C",
      "consumer_artifact": "R1D-AGENCY",
      "comparison_class": "edge projections",
      "exact_compared_record_sets": {
        "producer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-023",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-050",
          "DEP-051",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-085",
          "DEP-086",
          "DEP-087",
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094"
        ],
        "consumer_ids": [
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-085",
          "DEP-086",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-050",
          "DEP-051",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ]
      },
      "exact_record_counts": {
        "producer": 94,
        "consumer": 37
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "b2e3416d2f8b497df5ee6635f7325e10e4ebd911be37ef2dfa65dbb62ec3c0f5",
        "consumer_sha256": "e00feb9ea358799638a31b85152a872f32fe36e2474bc886635fd8a4b5794c65"
      },
      "comparison_rules": [
        "edge projections",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-009",
      "producer_artifact": "R1C",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "edge projections",
      "exact_compared_record_sets": {
        "producer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-023",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-050",
          "DEP-051",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-085",
          "DEP-086",
          "DEP-087",
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094"
        ],
        "consumer_ids": [
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-023",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-060",
          "DEP-070",
          "DEP-071",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ]
      },
      "exact_record_counts": {
        "producer": 94,
        "consumer": 29
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "b2e3416d2f8b497df5ee6635f7325e10e4ebd911be37ef2dfa65dbb62ec3c0f5",
        "consumer_sha256": "d4284b6e99b4392e6b96529dbd7f65985e8a80254f733c6fe7f981f62c667c04"
      },
      "comparison_rules": [
        "edge projections",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_cross_invariants_and_dependencies.yaml",
        "docs/doctrine/consolidation/afqr_world_action_sensing.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-010",
      "producer_artifact": "R1D-CORE",
      "consumer_artifact": "R1D-AGENCY",
      "comparison_class": "boundary parity",
      "exact_compared_record_sets": {
        "producer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "CORE-BND-DEP-009",
          "CORE-BND-DEP-010",
          "CORE-BND-DEP-011",
          "CORE-BND-DEP-012",
          "CORE-BND-DEP-013",
          "CORE-BND-DEP-014",
          "CORE-BND-DEP-015",
          "CORE-BND-DEP-016",
          "CORE-BND-DEP-017",
          "CORE-BND-DEP-018",
          "CORE-BND-DEP-019",
          "CORE-BND-DEP-023",
          "CORE-BND-DEP-029",
          "CORE-BND-DEP-030",
          "CORE-BND-DEP-031",
          "CORE-BND-DEP-037",
          "CORE-BND-DEP-038",
          "CORE-BND-DEP-039",
          "CORE-BND-DEP-040",
          "CORE-BND-DEP-041",
          "CORE-BND-DEP-042",
          "CORE-BND-DEP-043",
          "CORE-BND-DEP-044",
          "CORE-BND-DEP-045",
          "CORE-BND-DEP-046",
          "CORE-BND-DEP-050",
          "CORE-BND-DEP-051",
          "CORE-BND-DEP-055",
          "CORE-BND-DEP-056",
          "CORE-BND-DEP-057",
          "CORE-BND-DEP-058",
          "CORE-BND-DEP-059",
          "CORE-BND-DEP-060",
          "CORE-BND-DEP-067",
          "CORE-BND-DEP-068",
          "CORE-BND-DEP-069",
          "CORE-BND-DEP-070",
          "CORE-BND-DEP-071"
        ],
        "consumer_ids": [
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-085",
          "DEP-086",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-050",
          "DEP-051",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ]
      },
      "exact_record_counts": {
        "producer": 71,
        "consumer": 37
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "64eaf1c5832a56e302d84c8a1d28b603b9da266a1db502136a61c7128ca70f19",
        "consumer_sha256": "e00feb9ea358799638a31b85152a872f32fe36e2474bc886635fd8a4b5794c65"
      },
      "comparison_rules": [
        "boundary parity",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md",
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-011",
      "producer_artifact": "R1D-CORE",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "boundary parity",
      "exact_compared_record_sets": {
        "producer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "CORE-BND-DEP-009",
          "CORE-BND-DEP-010",
          "CORE-BND-DEP-011",
          "CORE-BND-DEP-012",
          "CORE-BND-DEP-013",
          "CORE-BND-DEP-014",
          "CORE-BND-DEP-015",
          "CORE-BND-DEP-016",
          "CORE-BND-DEP-017",
          "CORE-BND-DEP-018",
          "CORE-BND-DEP-019",
          "CORE-BND-DEP-023",
          "CORE-BND-DEP-029",
          "CORE-BND-DEP-030",
          "CORE-BND-DEP-031",
          "CORE-BND-DEP-037",
          "CORE-BND-DEP-038",
          "CORE-BND-DEP-039",
          "CORE-BND-DEP-040",
          "CORE-BND-DEP-041",
          "CORE-BND-DEP-042",
          "CORE-BND-DEP-043",
          "CORE-BND-DEP-044",
          "CORE-BND-DEP-045",
          "CORE-BND-DEP-046",
          "CORE-BND-DEP-050",
          "CORE-BND-DEP-051",
          "CORE-BND-DEP-055",
          "CORE-BND-DEP-056",
          "CORE-BND-DEP-057",
          "CORE-BND-DEP-058",
          "CORE-BND-DEP-059",
          "CORE-BND-DEP-060",
          "CORE-BND-DEP-067",
          "CORE-BND-DEP-068",
          "CORE-BND-DEP-069",
          "CORE-BND-DEP-070",
          "CORE-BND-DEP-071"
        ],
        "consumer_ids": [
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-023",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-060",
          "DEP-070",
          "DEP-071",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ]
      },
      "exact_record_counts": {
        "producer": 71,
        "consumer": 29
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "64eaf1c5832a56e302d84c8a1d28b603b9da266a1db502136a61c7128ca70f19",
        "consumer_sha256": "d4284b6e99b4392e6b96529dbd7f65985e8a80254f733c6fe7f981f62c667c04"
      },
      "comparison_rules": [
        "boundary parity",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md",
        "docs/doctrine/consolidation/afqr_world_action_sensing.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-012",
      "producer_artifact": "R1D-AGENCY",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "boundary parity",
      "exact_compared_record_sets": {
        "producer_ids": [
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-085",
          "DEP-086",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-050",
          "DEP-051",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ],
        "consumer_ids": [
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-023",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-060",
          "DEP-070",
          "DEP-071",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087"
        ]
      },
      "exact_record_counts": {
        "producer": 37,
        "consumer": 29
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "e00feb9ea358799638a31b85152a872f32fe36e2474bc886635fd8a4b5794c65",
        "consumer_sha256": "d4284b6e99b4392e6b96529dbd7f65985e8a80254f733c6fe7f981f62c667c04"
      },
      "comparison_rules": [
        "boundary parity",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
        "docs/doctrine/consolidation/afqr_world_action_sensing.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-013",
      "producer_artifact": "R1D",
      "consumer_artifact": "R1E",
      "comparison_class": "completion inputs",
      "exact_compared_record_sets": {
        "producer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-023",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-050",
          "DEP-051",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-085",
          "DEP-086",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-084",
          "DEP-087",
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094"
        ],
        "consumer_ids": [
          "DEP-001",
          "DEP-002",
          "DEP-003",
          "DEP-004",
          "DEP-005",
          "DEP-006",
          "DEP-007",
          "DEP-008",
          "DEP-009",
          "DEP-010",
          "DEP-011",
          "DEP-012",
          "DEP-013",
          "DEP-014",
          "DEP-015",
          "DEP-016",
          "DEP-017",
          "DEP-018",
          "DEP-019",
          "DEP-020",
          "DEP-021",
          "DEP-022",
          "DEP-023",
          "DEP-024",
          "DEP-025",
          "DEP-026",
          "DEP-027",
          "DEP-028",
          "DEP-029",
          "DEP-030",
          "DEP-031",
          "DEP-032",
          "DEP-033",
          "DEP-034",
          "DEP-035",
          "DEP-036",
          "DEP-037",
          "DEP-038",
          "DEP-039",
          "DEP-040",
          "DEP-041",
          "DEP-042",
          "DEP-043",
          "DEP-044",
          "DEP-045",
          "DEP-046",
          "DEP-047",
          "DEP-048",
          "DEP-049",
          "DEP-050",
          "DEP-051",
          "DEP-052",
          "DEP-053",
          "DEP-054",
          "DEP-055",
          "DEP-056",
          "DEP-057",
          "DEP-058",
          "DEP-059",
          "DEP-060",
          "DEP-061",
          "DEP-062",
          "DEP-063",
          "DEP-064",
          "DEP-065",
          "DEP-066",
          "DEP-067",
          "DEP-068",
          "DEP-069",
          "DEP-070",
          "DEP-071",
          "DEP-072",
          "DEP-073",
          "DEP-074",
          "DEP-075",
          "DEP-076",
          "DEP-077",
          "DEP-078",
          "DEP-079",
          "DEP-080",
          "DEP-081",
          "DEP-082",
          "DEP-083",
          "DEP-084",
          "DEP-085",
          "DEP-086",
          "DEP-087",
          "DEP-088",
          "DEP-089",
          "DEP-090",
          "DEP-091",
          "DEP-092",
          "DEP-093",
          "DEP-094"
        ]
      },
      "exact_record_counts": {
        "producer": 94,
        "consumer": 94
      },
      "normalized_record_set_hashes": {
        "producer_sha256": "4efa9dfdd4b0b1f0c902342d55dcb5b0fbbfc15ccfafb5368b433252eb349dbe",
        "consumer_sha256": "1f1bb17ac75e74738c406997044285a96c03917cbf008137c6e48277aa4eefac"
      },
      "comparison_rules": [
        "completion inputs",
        "ownership is never inferred from consumption",
        "all applicable IDs and exact records are hash-bound"
      ],
      "missing_ids": [],
      "surplus_ids": [],
      "mismatched_ids_and_fields": [],
      "authority_transfer_tests": [
        "no consumer ownership",
        "no combined owner",
        "no phase-authority leak"
      ],
      "evidence_paths": [
        "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md",
        "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md",
        "docs/doctrine/consolidation/afqr_world_action_sensing.md",
        "docs/doctrine/reviews/afqr_01_20_formal_completion_review.md"
      ],
      "result": "pass",
      "blocking_status": "nonblocking"
    }
  ],
  "corpus_scale_adequacy_matrix": [
    {
      "donor_family": "fantasy anatomy, damage, conditions, grids, initiative, combat, stealth, terrain, and weather",
      "representative_construct_pressures": [
        "armor-class procedures",
        "hit-point formulas",
        "initiative systems",
        "grid units",
        "condition lists",
        "vision rules",
        "alignment grids",
        "setting-specific morality axes"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-04",
        "AFQR-08",
        "AFQR-09",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-04": "initiative ordering without world-owned time",
          "AFQR-08": "identity continuity across bodily change"
        },
        "world_to_agency": {
          "AFQR-11": "actor agency remains separate from body and combat state"
        },
        "agency_to_core": [
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-04 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize armor-class procedures through typed owner handoff"
      ],
      "source_local_examples": [
        "armor-class procedures",
        "hit-point formulas",
        "initiative systems",
        "grid units",
        "condition lists",
        "vision rules",
        "alignment grids",
        "setting-specific morality axes",
        "reaction tables"
      ],
      "quarantine_triggers": [
        "untyped hit-point loss is applied as universal AFQR-16 harm",
        "grid adjacency silently establishes AFQR-19 opportunity or target validity",
        "alignment determines agency or responsibility"
      ],
      "doctrine_escalation_triggers": [
        "a donor condition has no typed AFQR-16 profile",
        "initiative needs a new AFQR-04/AFQR-19 reaction-order contract",
        "incompatible morality or universal culpability claim"
      ],
      "prohibited_universalizations": [
        "one armor-class, hit-point, initiative, grid, condition, or vision procedure becoming Astra law",
        "one alignment, morality, or reaction model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-01",
          "record_sha256": "240ef0f6c69712adc358c1e997419cbcde82682d0e12ed090f7766c8943c55c2",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-01",
          "record_sha256": "21f27483b514d5e2f0f8e05034ffff1aa3c1d577027cc9fb6e41ff637119418d",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-01",
          "record_sha256": "58f3f508756ebf1500854fcb4a4431ec15a138874bb21dc68376def7443117b1",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Fantasy anatomy and harm land in AFQR-16, terrain/weather in AFQR-17, grids and movement in AFQR-18, combat in AFQR-19, and stealth/search in AFQR-20; donor mechanics remain profiled. Route motives to behavior and social perceptions separately; only typed bonds become governed relations.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "science-fiction vacuum, radiation, cybernetics, vehicles, mechs, ships, sensors, and electronic warfare",
      "representative_construct_pressures": [
        "ship facing rules",
        "radiation tracks",
        "electronic-warfare action economies",
        "mech hit-location tables",
        "crew-role systems",
        "autopilot behavior profiles"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-07",
        "AFQR-08",
        "AFQR-09",
        "AFQR-11",
        "AFQR-12",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-07": "resource and repair conservation",
          "AFQR-08": "platform, body, and replacement continuity",
          "AFQR-09": "operator/platform governed dependencies"
        },
        "world_to_agency": {
          "AFQR-11": "operator agency and control"
        },
        "agency_to_core": [
          "AFQR-08"
        ],
        "agency_to_world": [
          "AFQR-16",
          "AFQR-19"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-07 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize ship facing rules through typed owner handoff"
      ],
      "source_local_examples": [
        "ship facing rules",
        "radiation tracks",
        "electronic-warfare action economies",
        "mech hit-location tables",
        "crew-role systems",
        "autopilot behavior profiles"
      ],
      "quarantine_triggers": [
        "vacuum or radiation is applied directly as injury without AFQR-17 exposure and AFQR-16 harm stages",
        "sensor lock is treated as AFQR-19 target validity",
        "capability or execution proves operator consent/agency"
      ],
      "doctrine_escalation_triggers": [
        "a cybernetic platform cannot preserve AFQR-08 identity and AFQR-09 operator dependency boundaries",
        "electronic warfare requires an unsupported reaction or signal propagation contract",
        "delegated control or platform responsibility unresolved"
      ],
      "prohibited_universalizations": [
        "one vacuum model, radiation track, vehicle scale, sensor suite, or electronic-warfare economy becoming Astra law",
        "one vehicle actor, control, or responsibility model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-09",
          "record_sha256": "ab3c4e0b9869ad522fc91ba3c80a61d6fd510dc8b7307b7e1c267f70e1db2e53",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-11",
          "record_sha256": "70079ed09a9a3f5d4f52f8c727e75dd86ad1df529aa47db31c944afa3f0c4e23",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-02",
          "record_sha256": "6819f8559867052b68232446ca37a2009ffaddc977e0764a47f1f8431cab3180",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Cybernetics and platform integrity land in AFQR-16, hazardous media in AFQR-17, platform geometry in AFQR-18, resolution in AFQR-19, and sensors/countermeasures in AFQR-20. Operator identity, delegation, autonomous planning, embodiment, and action resolution remain orthogonal.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "hybrid science-fantasy embodiment, environments, spatial layers, weapons, and sensing",
      "representative_construct_pressures": [
        "mana-radiation equivalence tables",
        "astral weapon procedures",
        "layer-specific sensor ranges",
        "alignment grids",
        "setting-specific morality axes",
        "reaction tables"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-07",
        "AFQR-08",
        "AFQR-09",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-07": "cross-domain conservation",
          "AFQR-08": "transformation continuity"
        },
        "world_to_agency": {
          "AFQR-11": "agency across transformed embodiments"
        },
        "agency_to_core": [
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-07 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize mana-radiation equivalence tables through typed owner handoff"
      ],
      "source_local_examples": [
        "mana-radiation equivalence tables",
        "astral weapon procedures",
        "layer-specific sensor ranges",
        "alignment grids",
        "setting-specific morality axes",
        "reaction tables"
      ],
      "quarantine_triggers": [
        "mana and radiation are collapsed into one universal field",
        "astral layer reach is treated as target validity",
        "alignment determines agency or responsibility"
      ],
      "doctrine_escalation_triggers": [
        "a hybrid weapon effect has no owner-qualified AFQR-16/17/18 settlement",
        "transformation cannot preserve AFQR-08 continuity",
        "incompatible morality or universal culpability claim"
      ],
      "prohibited_universalizations": [
        "one mana-technology equivalence, astral topology, weapon procedure, or sensing model becoming Astra law",
        "one alignment, morality, or reaction model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-01",
          "record_sha256": "240ef0f6c69712adc358c1e997419cbcde82682d0e12ed090f7766c8943c55c2",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-01",
          "record_sha256": "21f27483b514d5e2f0f8e05034ffff1aa3c1d577027cc9fb6e41ff637119418d",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-03",
          "record_sha256": "bead86b1aa7f8ce0dce42a468fc5425598525b88ec106e546e5c034786eb6241",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Each hybrid construct lands by semantics across AFQR-16–20; no AFQR-13 handoff is invented because the pressure names no social-state construct. Route motives to behavior and social perceptions separately; only typed bonds become governed relations.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "cultivation meridians, cores, body refinement, tribulations, domains, movement arts, perception, and conflict",
      "representative_construct_pressures": [
        "realm ladders",
        "universal meridian maps",
        "tribulation schedules",
        "sect combat cadence",
        "dao conviction scales",
        "heart-demon models",
        "karmic reputation systems"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-07",
        "AFQR-08",
        "AFQR-09",
        "AFQR-10",
        "AFQR-11",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-07": "resource conservation",
          "AFQR-08": "transformation continuity"
        },
        "world_to_agency": {
          "AFQR-11": "personhood and agency through refinement"
        },
        "agency_to_core": [
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-07 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize realm ladders through typed owner handoff"
      ],
      "source_local_examples": [
        "realm ladders",
        "universal meridian maps",
        "tribulation schedules",
        "sect combat cadence",
        "dao conviction scales",
        "heart-demon models",
        "karmic reputation systems"
      ],
      "quarantine_triggers": [
        "one meridian or core anatomy is treated as universal embodiment",
        "spiritual perception is promoted directly to truth or knowledge",
        "karma treated as truth or responsibility"
      ],
      "doctrine_escalation_triggers": [
        "domain reach requires a new AFQR-18/19 targeting boundary",
        "tribulation effects cannot be represented through AFQR-17 exposure and AFQR-16 harm",
        "oath legal effect or sect jurisdiction is unspecified"
      ],
      "prohibited_universalizations": [
        "one meridian/core anatomy, tribulation schedule, domain jurisdiction, cultivation cadence, or perception truth model becoming Astra law",
        "one cultivation psychology, oath, or karma law",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-04",
          "record_sha256": "f37ddcfe535e9b354a19a49febe8c8992e96b60976c18b66b5f14423e656a4ba",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-03",
          "record_sha256": "e39b816ff1410800723702c08497b3164a6998b887e3e8aabc25c7b766047c28",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-04",
          "record_sha256": "6c86a7e5cca055edfb39fe688234a9d6b18234bfd97b0ce9aea657199bf36b35",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Refinement uses AFQR-16, tribulations AFQR-17, domains/movement AFQR-18, conflict AFQR-19, and perception AFQR-20, with AFQR-07 conservation and AFQR-08 continuity handoffs. Conviction and drives remain behavioral; oaths require governed-relation handoff and reputation stays audience-relative.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "class and archetype capability and combat packages",
      "representative_construct_pressures": [
        "class action economies",
        "level tables",
        "fixed recharge schedules",
        "class personality packages",
        "background status tables"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-03",
        "AFQR-07",
        "AFQR-08",
        "AFQR-09",
        "AFQR-12",
        "AFQR-13",
        "AFQR-19"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-03": "action-route capability requirements",
          "AFQR-07": "resource costs when present"
        },
        "world_to_agency": {},
        "agency_to_core": [
          "AFQR-08",
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-03 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize class action economies through typed owner handoff"
      ],
      "source_local_examples": [
        "class action economies",
        "level tables",
        "fixed recharge schedules",
        "class personality packages",
        "background status tables"
      ],
      "quarantine_triggers": [
        "class possession is silently treated as capability readiness",
        "capability, opportunity, target, and resolution are merged into one package",
        "class or profession determines behavior/personhood"
      ],
      "doctrine_escalation_triggers": [
        "a capability category has no lawful AFQR-03 requirement/AFQR-19 readiness split",
        "a package needs a new resource or reaction contract",
        "background obligation lacks typed relation"
      ],
      "prohibited_universalizations": [
        "one class progression, action economy, recharge schedule, or combat package becoming Astra law",
        "one class, profession, caste, or status model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-01",
          "record_sha256": "240ef0f6c69712adc358c1e997419cbcde82682d0e12ed090f7766c8943c55c2",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-04",
          "record_sha256": "1b38995190b6a64f3c1ab8ab8f1f2438a7fd09cbca62a284eca6ea70ff2a04c2",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-05",
          "record_sha256": "2db78312c2e26cfc8a0a724ecbbf0f2cd392febe4ea8094555de109637affb13",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "AFQR-19 is the sole necessary world landing for readiness and combat; AFQR-03 receives action requirements, and no motivation handoff is invented. Archetype tendencies remain source-local while identity and governed ties use core owners.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "profession and occupation hazard, tool, movement, and sensing assumptions",
      "representative_construct_pressures": [
        "profession skill lists",
        "tool-range tables",
        "shift exposure schedules",
        "class personality packages",
        "background status tables"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-03",
        "AFQR-08",
        "AFQR-09",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-03": "tool actions and requirements",
          "AFQR-09": "employment dependencies only when governed"
        },
        "world_to_agency": {
          "AFQR-11": "worker agency and consent"
        },
        "agency_to_core": [
          "AFQR-08",
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-03 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize profession skill lists through typed owner handoff"
      ],
      "source_local_examples": [
        "profession skill lists",
        "tool-range tables",
        "shift exposure schedules",
        "class personality packages",
        "background status tables"
      ],
      "quarantine_triggers": [
        "tool proficiency is treated as physical reach or successful search",
        "workplace exposure is applied directly as injury",
        "class or profession determines behavior/personhood"
      ],
      "doctrine_escalation_triggers": [
        "a tool action lacks an AFQR-03 requirement contract",
        "an employment relation needs an actual governed AFQR-09 dependency",
        "background obligation lacks typed relation"
      ],
      "prohibited_universalizations": [
        "one profession list, tool range, hazard schedule, or sensory assumption becoming Astra law",
        "one class, profession, caste, or status model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-01",
          "record_sha256": "240ef0f6c69712adc358c1e997419cbcde82682d0e12ed090f7766c8943c55c2",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-04",
          "record_sha256": "1b38995190b6a64f3c1ab8ab8f1f2438a7fd09cbca62a284eca6ea70ff2a04c2",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-06",
          "record_sha256": "826d48396eaecd396de1f2d5c8297497542bb3f5821c336fa8553cc17811e558",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Occupational injury, hazards, movement, and sensing land in AFQR-16/17/18/20; command requirements and genuine governed employment dependencies cross to core owners. Archetype tendencies remain source-local while identity and governed ties use core owners.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "point-buy physical, sensory, movement, combat, and resilience traits",
      "representative_construct_pressures": [
        "point costs",
        "attribute caps",
        "derived defense formulas",
        "vision-distance purchases",
        "trait scales",
        "influence currencies"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-07",
        "AFQR-08",
        "AFQR-10",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-07": "point-resource conservation if retained",
          "AFQR-08": "identity remains separate from purchased traits"
        },
        "world_to_agency": {
          "AFQR-11": "personhood is not a purchased physical trait"
        },
        "agency_to_core": [],
        "agency_to_world": [
          "AFQR-19"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-07 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize point costs through typed owner handoff"
      ],
      "source_local_examples": [
        "point costs",
        "attribute caps",
        "derived defense formulas",
        "vision-distance purchases",
        "trait scales",
        "influence currencies"
      ],
      "quarantine_triggers": [
        "purchased perception is treated as knowledge",
        "combat points merge readiness and resolution",
        "trait score proves knowledge, consent, or authority"
      ],
      "doctrine_escalation_triggers": [
        "a point pool creates or destroys a conserved quantity without AFQR-07 settlement",
        "a trait cannot be separated among embodiment, movement, combat, and sensing owners",
        "cross-domain trait has no declared semantic owner"
      ],
      "prohibited_universalizations": [
        "one point cost, attribute cap, defense formula, or sensory range becoming Astra law",
        "one personality, knowledge, or influence scale",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-02",
          "record_sha256": "8437a6b0ab2ccf085fa81b5e2275b5ca6ab2be36bc96617f8405b49d6d0a8822",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-05",
          "record_sha256": "55778ccb6a564dc589734f7690a5fb84fe1014cff3ae269a566405e078d0a90a",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-07",
          "record_sha256": "29c013d430b214f72f19ed03c819dd2f4a2267d2406bdecb0d3371a0e502efcb",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Physical resilience lands in AFQR-16, movement in AFQR-18, combat in AFQR-19, and sensory traits in AFQR-20; point settlement uses AFQR-07 only when a quantity is conserved. Trait values land only in their declared domain and mechanical resolution remains world-owned.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "narrative tags, aspects, harm tracks, consequences, clocks, zones, and fictional positioning",
      "representative_construct_pressures": [
        "stress boxes",
        "consequence slots",
        "scene clocks",
        "zone adjacency rules",
        "aspect invocation rules",
        "relationship clocks",
        "instinct triggers"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-03",
        "AFQR-04",
        "AFQR-09",
        "AFQR-10",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-18",
        "AFQR-19"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-04": "clock ordering without transfer of logical-time ownership",
          "AFQR-03": "tagged action representation"
        },
        "world_to_agency": {
          "AFQR-10": "fictional information state remains epistemically typed"
        },
        "agency_to_core": [
          "AFQR-04",
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-03 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize stress boxes through typed owner handoff"
      ],
      "source_local_examples": [
        "stress boxes",
        "consequence slots",
        "scene clocks",
        "zone adjacency rules",
        "aspect invocation rules",
        "relationship clocks",
        "instinct triggers"
      ],
      "quarantine_triggers": [
        "a narrative clock is treated as AFQR-04 logical time by naming alone",
        "a zone tag establishes target validity without AFQR-19",
        "tag or clock silently establishes truth/obligation"
      ],
      "doctrine_escalation_triggers": [
        "a consequence cannot be typed as AFQR-16 harm or retained source-locally",
        "a clock needs a new ordering contract beyond AFQR-04",
        "aspect spans identity, relation, and behavior without typing"
      ],
      "prohibited_universalizations": [
        "one stress track, consequence ladder, scene clock, zone system, or fictional-positioning rule becoming Astra law",
        "one narrative tag or clock semantics",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-03",
          "record_sha256": "34d6fce56614861975e4fe35af0fc77ee2d03606eb7a4f9a2a6042d861a358e4",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-06",
          "record_sha256": "ed4681c823a87bb44abda8d9b02e4663a1601408670cd7144ba010aaf43bdb8d",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-08",
          "record_sha256": "df9ceec6120109848fc7060b2c1ee2b502e444985666c89b6219906d9adb2bbb",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Harm tracks land in AFQR-16, zones in AFQR-18, and contests in AFQR-19; clocks hand off to AFQR-04 without transferring time ownership. Beliefs and drives separate from timed governed relations; narrative mechanics remain source-local.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "cyberware, biotech, prosthetics, replacement bodies, neural sensing, and transformation",
      "representative_construct_pressures": [
        "implant slot systems",
        "humanity-loss tracks",
        "brand-specific neural ranges",
        "editing procedures",
        "augmentation psychology"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-08",
        "AFQR-09",
        "AFQR-10",
        "AFQR-11",
        "AFQR-12",
        "AFQR-16",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-08": "identity and continuity across replacement",
          "AFQR-09": "implant dependencies only when governed"
        },
        "world_to_agency": {
          "AFQR-11": "consent, agency, and control of augmentation"
        },
        "agency_to_core": [
          "AFQR-08"
        ],
        "agency_to_world": [
          "AFQR-16",
          "AFQR-19"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-08 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize implant slot systems through typed owner handoff"
      ],
      "source_local_examples": [
        "implant slot systems",
        "humanity-loss tracks",
        "brand-specific neural ranges",
        "editing procedures",
        "augmentation psychology"
      ],
      "quarantine_triggers": [
        "replacement-body installation rewrites identity automatically",
        "neural contact becomes knowledge or target validity",
        "modification automatically removes personhood/consent"
      ],
      "doctrine_escalation_triggers": [
        "augmentation dependencies require a new governed AFQR-09 contract",
        "replacement cannot preserve AFQR-08 continuity",
        "memory replacement identity or responsibility seam unresolved"
      ],
      "prohibited_universalizations": [
        "one implant-slot, humanity-loss, replacement-body, or neural-range model becoming Astra law",
        "one impairment, personality, or memory-continuity rule",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-06",
          "record_sha256": "a829faceecd0766b22e55303fb2138928ed91dc7bb9918aa5b0f238837af2a9b",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-07",
          "record_sha256": "79086b4e408f37593ce5604b807a4fc248fc08e55100ed98b7ff35e4157caeb5",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-09",
          "record_sha256": "9fe35a18e5f6b4df987f7de1fa56f14246b4ba7c49bc6ca37a297317b074db6d",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "AFQR-16 owns augmentation embodiment and replacement; AFQR-20 owns neural sensing; AFQR-08 preserves identity and AFQR-09 applies only to actual governed implant dependencies. Edits route through memory, behavior, identity, embodiment, and resolution without collapsing personhood.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "psionic perception, telepathy, concealment, possession, targeting, and mental conflict",
      "representative_construct_pressures": [
        "mind-point economies",
        "universal telepathy ranges",
        "possession save procedures",
        "psionic disciplines",
        "shared-mind metaphysics"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-06",
        "AFQR-08",
        "AFQR-10",
        "AFQR-11",
        "AFQR-12",
        "AFQR-14",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-08": "identity continuity under possession",
          "AFQR-06": "evidence status of sensed impressions"
        },
        "world_to_agency": {
          "AFQR-11": "consent and control under possession",
          "AFQR-14": "telepathy as communication/interpretation"
        },
        "agency_to_core": [
          "AFQR-08"
        ],
        "agency_to_world": [
          "AFQR-19",
          "AFQR-20"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-06 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize mind-point economies through typed owner handoff"
      ],
      "source_local_examples": [
        "mind-point economies",
        "universal telepathy ranges",
        "possession save procedures",
        "psionic disciplines",
        "shared-mind metaphysics"
      ],
      "quarantine_triggers": [
        "telepathic detection is treated as interpreted communication",
        "possession is treated as consent or identity transfer",
        "telepathy treated as automatic truth, consent, control, or communication success"
      ],
      "doctrine_escalation_triggers": [
        "mental targeting lacks an AFQR-19 validity contract",
        "telepathy needs a new AFQR-14 communication modality contract",
        "possessor/host identity or responsibility unresolved"
      ],
      "prohibited_universalizations": [
        "one mind-point economy, telepathy range, possession procedure, or mental-conflict resolver becoming Astra law",
        "one telepathy, possession, or domination model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-07",
          "record_sha256": "966e9200c2dafffb4b83d9230afbfe91dd78530f5def65c3e61a9129091147e1",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-08",
          "record_sha256": "d92b08978bb12f30a35dca1394e2e2b4339812853ba4a2b522f6fd17673584b2",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-10",
          "record_sha256": "29567d30b5bca75d52b348237324abcef7bfc80d49d40e4894559be78ab76c2a",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "AFQR-20 owns psionic acquisition and AFQR-19 targeting/conflict, while identity, consent, and communication cross to AFQR-08/11/14. Signal, interpretation, knowledge, identity, coercion, behavior, and resolution remain typed.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "horror injury, trauma, contamination, transformation, unreliable sensing, and environmental threat",
      "representative_construct_pressures": [
        "sanity tracks",
        "mutation tables",
        "contamination clocks",
        "false-perception procedures",
        "corruption ladders",
        "forbidden-knowledge effects"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-06",
        "AFQR-08",
        "AFQR-10",
        "AFQR-11",
        "AFQR-12",
        "AFQR-16",
        "AFQR-17",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-08": "continuity through transformation",
          "AFQR-06": "evidence treatment of unreliable observations"
        },
        "world_to_agency": {
          "AFQR-10": "belief and uncertainty",
          "AFQR-11": "agency under trauma"
        },
        "agency_to_core": [],
        "agency_to_world": [
          "AFQR-16",
          "AFQR-20"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-06 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize sanity tracks through typed owner handoff"
      ],
      "source_local_examples": [
        "sanity tracks",
        "mutation tables",
        "contamination clocks",
        "false-perception procedures",
        "corruption ladders",
        "forbidden-knowledge effects"
      ],
      "quarantine_triggers": [
        "unreliable sensing rewrites hidden world truth",
        "contamination automatically becomes injury or transformation",
        "fear or trauma proves incapacity or nonpersonhood"
      ],
      "doctrine_escalation_triggers": [
        "trauma cannot preserve agency and epistemic uncertainty boundaries",
        "a mutation lacks an AFQR-08 continuity disposition",
        "unreliable perception cannot preserve hidden truth"
      ],
      "prohibited_universalizations": [
        "one sanity track, mutation table, contamination clock, or unreliable-perception procedure becoming Astra law",
        "one sanity, corruption, secrecy, or capacity rule",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-08",
          "record_sha256": "7566a5e5021a3f43cdae4d82ee57698e585aa8bc0f37eb226362f1ba8c7bbf82",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-09",
          "record_sha256": "88f9d006fc2758c8c3df59dcfeccfd97db54564232bbb19757a4166785da60a5",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-11",
          "record_sha256": "ae3a7c8a5f1a6ededb35bc27359d45dc945566b4a35ed0c06cf7d60deaf4c9ea",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Injury/transformation land in AFQR-16, contamination in AFQR-17, and unreliable sensing in AFQR-20, with identity, evidence, epistemic, and agency handoffs. Epistemic uncertainty and behavioral effects remain distinct from consent, personhood, embodiment, and sensing.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "investigation searches, clues, surveillance, tracking, concealment, and evidence acquisition",
      "representative_construct_pressures": [
        "automatic clue rules",
        "search-turn procedures",
        "surveillance range tables",
        "clue-distribution procedures",
        "rumor tables"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-06",
        "AFQR-10",
        "AFQR-14",
        "AFQR-18",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-06": "evidence admissibility and arbitration"
        },
        "world_to_agency": {
          "AFQR-10": "knowledge and epistemic records",
          "AFQR-14": "communication and interpretation of clues"
        },
        "agency_to_core": [
          "AFQR-06"
        ],
        "agency_to_world": [
          "AFQR-20"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-06 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize automatic clue rules through typed owner handoff"
      ],
      "source_local_examples": [
        "automatic clue rules",
        "search-turn procedures",
        "surveillance range tables",
        "clue-distribution procedures",
        "rumor tables"
      ],
      "quarantine_triggers": [
        "detection becomes admitted evidence",
        "clues become truth or knowledge automatically",
        "surveillance contacts become valid targets",
        "search failure erases authoritative world truth",
        "clue admission or witness statement treated as truth"
      ],
      "doctrine_escalation_triggers": [
        "a clue cannot receive an AFQR-06 evidence disposition",
        "surveillance requires a new AFQR-20/19 contact-target contract",
        "hidden-information projection leaks authoritative truth"
      ],
      "prohibited_universalizations": [
        "one automatic-clue rule, search-turn procedure, surveillance range, or detection-success model becoming Astra law",
        "one clue, evidence, or discovery procedure",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-08",
          "record_sha256": "7566a5e5021a3f43cdae4d82ee57698e585aa8bc0f37eb226362f1ba8c7bbf82",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-10",
          "record_sha256": "155694e814523f80d1a0534fc6c9fedc5c18bc910443eae7c5f5853706a060da",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-12",
          "record_sha256": "de48b1401649b0736b7f9218327beba9930d6cfae784c4de620918e05808ba61",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "AFQR-20 owns search, contacts, and tracking and AFQR-18 location; AFQR-06 admits evidence, AFQR-10 records knowledge, and AFQR-14 interprets communicated clues. Admissibility, truth, interpretation, sensing, belief, and deception use separate handoffs.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "vehicles, ships, mechs, platforms, operators, components, scale, movement, damage, targeting, and sensors",
      "representative_construct_pressures": [
        "vehicle action economies",
        "facing systems",
        "hit-location tables",
        "crew-station initiative",
        "crew-role systems",
        "autopilot behavior profiles"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-07",
        "AFQR-08",
        "AFQR-09",
        "AFQR-11",
        "AFQR-12",
        "AFQR-16",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-07": "damage/resource settlement",
          "AFQR-08": "platform identity and proxyhood",
          "AFQR-09": "operator/platform dependencies"
        },
        "world_to_agency": {
          "AFQR-11": "operator agency and control"
        },
        "agency_to_core": [
          "AFQR-08"
        ],
        "agency_to_world": [
          "AFQR-16",
          "AFQR-19"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-07 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize vehicle action economies through typed owner handoff"
      ],
      "source_local_examples": [
        "vehicle action economies",
        "facing systems",
        "hit-location tables",
        "crew-station initiative",
        "crew-role systems",
        "autopilot behavior profiles"
      ],
      "quarantine_triggers": [
        "operator agency becomes platform identity",
        "component damage becomes operator injury",
        "sensor contact becomes target validity",
        "movement reach becomes jurisdiction or opportunity",
        "capability or execution proves operator consent/agency"
      ],
      "doctrine_escalation_triggers": [
        "a platform cannot separate operator, component, and identity dependencies",
        "multi-scale combat needs a new movement/target/reaction contract",
        "delegated control or platform responsibility unresolved"
      ],
      "prohibited_universalizations": [
        "one vehicle action economy, facing system, hit-location table, sensor lock, or crew initiative becoming Astra law",
        "one vehicle actor, control, or responsibility model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-09",
          "record_sha256": "ab3c4e0b9869ad522fc91ba3c80a61d6fd510dc8b7307b7e1c267f70e1db2e53",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-11",
          "record_sha256": "70079ed09a9a3f5d4f52f8c727e75dd86ad1df529aa47db31c944afa3f0c4e23",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-13",
          "record_sha256": "10df531c9075d88aa84fd1e3bccf2dc1f619490c9e48f895a45e06ec465300c7",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Platform integrity, topology, resolution, and sensing land in AFQR-16/18/19/20; identity, governed dependencies, settlement, and operator agency retain separate owners. Operator identity, delegation, autonomous planning, embodiment, and action resolution remain orthogonal.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "companions, summons, familiars, proxies, swarms, and distributed bodies",
      "representative_construct_pressures": [
        "shared hit-point pools",
        "summon action taxes",
        "swarm-square rules",
        "summoning bonds",
        "swarm cognition rules"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-08",
        "AFQR-09",
        "AFQR-10",
        "AFQR-11",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-08": "identity and proxy continuity",
          "AFQR-09": "summoner/companion dependency lifecycle"
        },
        "world_to_agency": {
          "AFQR-11": "separate agency and control"
        },
        "agency_to_core": [
          "AFQR-08",
          "AFQR-09"
        ],
        "agency_to_world": [
          "AFQR-16",
          "AFQR-19"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-08 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize shared hit-point pools through typed owner handoff"
      ],
      "source_local_examples": [
        "shared hit-point pools",
        "summon action taxes",
        "swarm-square rules",
        "summoning bonds",
        "swarm cognition rules"
      ],
      "quarantine_triggers": [
        "summoner identity is copied onto a companion",
        "shared sensing automatically becomes shared knowledge",
        "membership or copying proves shared agency/responsibility"
      ],
      "doctrine_escalation_triggers": [
        "a distributed body cannot distinguish AFQR-08 identity from AFQR-16 components",
        "control requires a new AFQR-11 agency contract",
        "collective identity, consent, or control attribution unresolved"
      ],
      "prohibited_universalizations": [
        "one summon action tax, shared hit-point pool, swarm grid, or familiar-sensing rule becoming Astra law",
        "one companion, proxy, swarm, or collective-personhood model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-10",
          "record_sha256": "7234edb916295ff2427f91619a77ffc95a7e6ef920c04c97ccebab736a1906b9",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-12",
          "record_sha256": "b63bae5459cacd461f260f5d7b41fa25d81046999a3072b476520d51673014f8",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-14",
          "record_sha256": "14d1d67e6ac0414627ce14c09b0f37197b5be3a29859c8c37052956eb8c3f824",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Distributed embodiment and position land in AFQR-16/18, multi-actor resolution in AFQR-19, and sensing in AFQR-20; identity, dependency, and agency remain separate. Identity, governed bonds, social membership, agency, cognition, embodiment, and action remain separate.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "crafting, salvage, repair, replacement, environmental modification, and constructed platforms",
      "representative_construct_pressures": [
        "recipe lists",
        "salvage yield tables",
        "repair-time formulas",
        "editing procedures",
        "augmentation psychology"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-07",
        "AFQR-08",
        "AFQR-09",
        "AFQR-10",
        "AFQR-11",
        "AFQR-12",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-07": "material conservation and settlement",
          "AFQR-08": "replacement continuity where identity-bearing",
          "AFQR-09": "governed component, operator, contract, or support dependencies only when the donor construct creates an actual typed dependency"
        },
        "world_to_agency": {
          "AFQR-11": "maker and operator agency"
        },
        "agency_to_core": [
          "AFQR-08"
        ],
        "agency_to_world": [
          "AFQR-16",
          "AFQR-19"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-07 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize recipe lists through typed owner handoff"
      ],
      "source_local_examples": [
        "recipe lists",
        "salvage yield tables",
        "repair-time formulas",
        "editing procedures",
        "augmentation psychology"
      ],
      "quarantine_triggers": [
        "salvage creates matter or value without AFQR-07 settlement",
        "repair rewrites identity without AFQR-08",
        "platform construction collapses embodiment, topology, and operator control",
        "modification automatically removes personhood/consent"
      ],
      "doctrine_escalation_triggers": [
        "a constructed platform needs a new operator/component support contract",
        "a recipe transforms a typed quantity without a conservation owner",
        "memory replacement identity or responsibility seam unresolved"
      ],
      "prohibited_universalizations": [
        "one recipe list, salvage yield, repair formula, crafting clock, or platform schema becoming Astra law",
        "one impairment, personality, or memory-continuity rule",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-11",
          "record_sha256": "b5227f15e85f6949958aa1d064b75219e0d525329a3e2fb783efac4807475ee3",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-07",
          "record_sha256": "79086b4e408f37593ce5604b807a4fc248fc08e55100ed98b7ff35e4157caeb5",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-15",
          "record_sha256": "4e78b2a5655bf133b5acf41b58ccb19b71f7653fda1775dad942727e91de2c89",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Repair and constructed integrity use AFQR-16, modification AFQR-17, and platform topology AFQR-18; AFQR-09 receives governed component, operator, contract, or support dependencies only when an actual typed dependency exists. Edits route through memory, behavior, identity, embodiment, and resolution without collapsing personhood.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "bestiary anatomy, scales, movement forms, senses, hazards, attacks, defenses, and transformations",
      "representative_construct_pressures": [
        "challenge ratings",
        "universal stat blocks",
        "fixed reach grids",
        "species vision defaults",
        "alignment grids",
        "setting-specific morality axes",
        "reaction tables"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-08",
        "AFQR-09",
        "AFQR-12",
        "AFQR-13",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-08": "identity through transformation"
        },
        "world_to_agency": {
          "AFQR-11": "agency/personhood cannot be inferred from anatomy"
        },
        "agency_to_core": [
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-08 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize challenge ratings through typed owner handoff"
      ],
      "source_local_examples": [
        "challenge ratings",
        "universal stat blocks",
        "fixed reach grids",
        "species vision defaults",
        "alignment grids",
        "setting-specific morality axes",
        "reaction tables"
      ],
      "quarantine_triggers": [
        "species anatomy is treated as the universal AFQR-16 profile",
        "creature reach or sense establishes opportunity or target validity",
        "alignment determines agency or responsibility"
      ],
      "doctrine_escalation_triggers": [
        "a transformation lacks AFQR-08 continuity",
        "a creature hazard cannot separate AFQR-17 exposure from AFQR-16 harm",
        "incompatible morality or universal culpability claim"
      ],
      "prohibited_universalizations": [
        "one stat block, challenge rating, anatomy, reach grid, species sense, or attack cadence becoming Astra law",
        "one alignment, morality, or reaction model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-06",
          "record_sha256": "a829faceecd0766b22e55303fb2138928ed91dc7bb9918aa5b0f238837af2a9b",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-01",
          "record_sha256": "21f27483b514d5e2f0f8e05034ffff1aa3c1d577027cc9fb6e41ff637119418d",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-16",
          "record_sha256": "b088a7b11e89a1902ae56a19047399d43090d8c9ff5b3da250b1025da278eace",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Plural anatomy, ecology, movement, conflict, and senses route across AFQR-16–20; identity and personhood are never inferred from species anatomy. Route motives to behavior and social perceptions separately; only typed bonds become governed relations.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "tables and oracles for weather, terrain, encounters, damage, targeting, and sensing",
      "representative_construct_pressures": [
        "random weather tables",
        "critical-hit charts",
        "encounter-distance dice",
        "detection matrices",
        "quest structures",
        "social encounter procedures",
        "trial scripts"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-02",
        "AFQR-04",
        "AFQR-06",
        "AFQR-07",
        "AFQR-09",
        "AFQR-10",
        "AFQR-11",
        "AFQR-13",
        "AFQR-14",
        "AFQR-15",
        "AFQR-16",
        "AFQR-17",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-04": "table timing inputs",
          "AFQR-07": "conservation or settlement only when an oracle creates, destroys, reserves, transforms, or settles a typed quantity"
        },
        "world_to_agency": {
          "AFQR-10": "oracle output is not truth without epistemic handling"
        },
        "agency_to_core": [
          "AFQR-02",
          "AFQR-06",
          "AFQR-09"
        ],
        "agency_to_world": [
          "AFQR-19"
        ]
      },
      "direct_mapping_examples": [
        "AFQR-02 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize random weather tables through typed owner handoff"
      ],
      "source_local_examples": [
        "random weather tables",
        "critical-hit charts",
        "encounter-distance dice",
        "detection matrices",
        "quest structures",
        "social encounter procedures",
        "trial scripts"
      ],
      "quarantine_triggers": [
        "oracle output is treated as committed truth",
        "a random table silently overrides its domain owner",
        "untyped results apply directly as damage, target, weather, position, or sensing state",
        "negotiation creates obligation or adjudication performs execution"
      ],
      "doctrine_escalation_triggers": [
        "a table result lacks a typed domain disposition",
        "a quantity-changing result needs an AFQR-07 conservation or settlement contract",
        "contract/oath lifecycle or evidence standard unspecified"
      ],
      "prohibited_universalizations": [
        "one random weather table, critical chart, encounter-distance table, targeting matrix, or sensing oracle becoming Astra law",
        "one mission, contract, diplomacy, trial, or encounter procedure",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-01",
          "record_sha256": "240ef0f6c69712adc358c1e997419cbcde82682d0e12ed090f7766c8943c55c2",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-17",
          "record_sha256": "7855d1df2867be66da943b0dc4de132cfd638ab66f2c0ede41fd3de84c65aef3",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-17",
          "record_sha256": "ca36dec62c3305610998ef1a0d357b87f610b9697b5054e0ef1bc47b7c7a8907",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Timing uses AFQR-04; injury AFQR-16; weather AFQR-17; distance/topology AFQR-18; targeting AFQR-19; sensing AFQR-20; AFQR-07 applies only when a typed quantity is created, destroyed, reserved, transformed, or settled. Epistemics, consent, communication, social state, institutions, commands, evidence, relations, and resolution remain typed.",
      "result": "pass",
      "blocking_defects": []
    },
    {
      "donor_family": "missions, scenarios, supplements, and adventure paths with local combat, map, hazard, and sensory assumptions",
      "representative_construct_pressures": [
        "scripted encounter turns",
        "adventure-only maps",
        "boxed-text detection outcomes",
        "supplement combat variants",
        "class personality packages",
        "background status tables"
      ],
      "lawful_astra_owner_afqrs": [
        "AFQR-03",
        "AFQR-04",
        "AFQR-08",
        "AFQR-09",
        "AFQR-12",
        "AFQR-13",
        "AFQR-17",
        "AFQR-18",
        "AFQR-19",
        "AFQR-20"
      ],
      "required_cross_owner_handoffs": {
        "world_to_core": {
          "AFQR-03": "scenario actions",
          "AFQR-04": "sequence scheduling without time ownership"
        },
        "world_to_agency": {
          "AFQR-11": "participant agency",
          "AFQR-14": "briefing interpretation"
        },
        "agency_to_core": [
          "AFQR-08",
          "AFQR-09"
        ],
        "agency_to_world": []
      },
      "direct_mapping_examples": [
        "AFQR-03 owned construct when source semantics match"
      ],
      "normalized_mapping_examples": [
        "normalize scripted encounter turns through typed owner handoff"
      ],
      "source_local_examples": [
        "scripted encounter turns",
        "adventure-only maps",
        "boxed-text detection outcomes",
        "supplement combat variants",
        "class personality packages",
        "background status tables"
      ],
      "quarantine_triggers": [
        "boxed text is treated as authoritative sensed truth",
        "scenario map reach establishes target validity",
        "class or profession determines behavior/personhood"
      ],
      "doctrine_escalation_triggers": [
        "a scenario-only combat rule cannot remain source-local without breaking AFQR-19",
        "a scripted sequence requires a new AFQR-04 ordering contract",
        "background obligation lacks typed relation"
      ],
      "prohibited_universalizations": [
        "one adventure map, scripted encounter cadence, hazard shortcut, or boxed-text sensory outcome becoming Astra law",
        "one class, profession, caste, or status model",
        "prohibited"
      ],
      "source_r1d_pressure_records": [
        {
          "family": "core",
          "record_id": "PRESS-16",
          "record_sha256": "3d957f21c1658222fa033ca74f9c802857d4f1e73d17f8dffaaa84f1342a3de6",
          "path": "docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md"
        },
        {
          "family": "agency",
          "record_id": "AGENCY-PRESSURE-04",
          "record_sha256": "1b38995190b6a64f3c1ab8ab8f1f2438a7fd09cbca62a284eca6ea70ff2a04c2",
          "path": "docs/doctrine/consolidation/afqr_epistemic_agency_social_communication.md"
        },
        {
          "family": "world",
          "record_id": "WORLD-PRESS-18",
          "record_sha256": "b853862c04942a6e8b564e7f1ca656257d4ef0cdce7f717aa994b3c50e9afac1",
          "path": "docs/doctrine/consolidation/afqr_world_action_sensing.md"
        }
      ],
      "rationale": "Scenario hazards, maps, combat, and sensing land in AFQR-17–20; actions and scheduling cross to AFQR-03/04 while participant agency and briefing interpretation remain AFQR-11/14. Archetype tendencies remain source-local while identity and governed ties use core owners.",
      "result": "pass",
      "blocking_defects": []
    }
  ],
  "phase_separation_review": {
    "result": "pass",
    "hidden_universal_models_rejected": [
      "RHBF",
      "anatomy",
      "action economy",
      "damage model",
      "grid",
      "cosmology",
      "morality system",
      "class model",
      "perception system",
      "institutional model",
      "resource economy",
      "progression model"
    ]
  },
  "unresolved_defects": [],
  "blocking_defects": [],
  "final_result": "pass",
  "next_lawful_gate": "R2 — doctrine-drift resolution",
  "downstream_gate_states": {
    "R2": "ready",
    "R3": "blocked",
    "R4": "blocked",
    "R5": "blocked",
    "R6": "blocked",
    "RT-002G": "unauthorized"
  },
  "authority_granted": [
    "formal doctrine completion review and gate adjudication only"
  ],
  "authority_not_granted": [
    "runtime",
    "conversion",
    "canon",
    "sourcebook",
    "model",
    "narration",
    "live-play",
    "UI",
    "RT-002G",
    "temporary evidence deletion"
  ],
  "completion_certificate": {
    "certificate_id": "R1E-CERT-001",
    "result": "pass",
    "r1_complete": true,
    "only_next_gate_ready": "R2"
  },
  "deferred_substrates": {
    "record_source": "missing_substrate_decisions",
    "count": 5,
    "record_set_sha256": "88444bd8cb4fb349015c510b24b4233cda724868976bb8347692e04427a96e6a"
  }
}
```
