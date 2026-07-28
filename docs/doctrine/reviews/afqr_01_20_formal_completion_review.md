# AFQR-01–20 R1E Formal Completion Review

**Result: PASS.** R1 is complete. This independent gate closes only the three unresolved dispositions and grants no implementation authority.

The normative, machine-reviewable contract follows. Historical R1A–R1D artifacts remain unchanged.

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
    "reconstructable_from_index_and_manifest": true,
    "afqr_14_provenance": "AFQR-14 owns communication and interpretation; AFQR-15 packaging validates files without ownership transfer, model, narration, or live-play authority",
    "records": [
      {
        "afqr_id": "AFQR-01",
        "selected_architecture": "Atomic Typed Transition Journal with Owner-Specific Reducers and Declared Saga Escape Hatches",
        "authoritative_selected_title": "Atomic State Transition, Ownership, Commitment, Recovery, and Replay",
        "selected_primary_evidence_id": "SRC-0004",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-02",
        "selected_architecture": "Synchronous Command Fast Path with Durable Attempt Escalation",
        "authoritative_selected_title": "Command Identity, Attempts, Retries, Suspension, Escalation, and Durable Progress",
        "selected_primary_evidence_id": "SRC-0005",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-03",
        "selected_architecture": "Typed Action Gateway with Registered Semantics, Capability-Affordance Composition, and Bounded Plan Verification",
        "authoritative_selected_title": "Action Representation, Capability, Affordance, Method Selection, and Bounded Plans",
        "selected_primary_evidence_id": "SRC-0006",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-04",
        "selected_architecture": "Profiled Logical-Time Causal Scheduler with Deterministic Resolution Groups and Bounded Cascade Microsteps",
        "authoritative_selected_title": "Logical Time, Simultaneity, Causal Ordering, Scheduled Effects, and Bounded Cascades",
        "selected_primary_evidence_id": "SRC-0007",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-05",
        "selected_architecture": "Registered Typed Interface-and-Bridge Hypergraph",
        "authoritative_selected_title": "Cross-System Interfaces, Adapters, Bridges, Hyperedges, and Compatibility",
        "selected_primary_evidence_id": "SRC-0008",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-06",
        "selected_architecture": "Invariant-Gated Typed Claim Arbitration",
        "authoritative_selected_title": "Claim Discovery, Admissibility, Conflict, Arbitration, Choice, and Hidden Evidence",
        "selected_primary_evidence_id": "SRC-0009",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-07",
        "selected_architecture": "Typed Balance-Domain Flow Ledger with Proof-Carrying Conversion and Atomic Settlement",
        "authoritative_selected_title": "Cross-Domain Conservation, Conversion Validity, Reservation, Settlement, and Arbitrage Prevention",
        "selected_primary_evidence_id": "SRC-0010",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-08",
        "selected_architecture": "Typed Faceted Identity, Continuity, and Lineage Graph with Purpose-Scoped Equivalence",
        "authoritative_selected_title": "Identity, Continuity, Copying, Transformation, Proxyhood, Reinstantiation, Fusion, Fission, and Contextual Equivalence",
        "selected_primary_evidence_id": "SRC-0011",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-09",
        "selected_architecture": "Registered Typed Dependency-and-Obligation Hypergraph with Version-Pinned Lifecycle Policies and Bounded Causal Propagation",
        "authoritative_selected_title": "Dependency, Revocation, Inheritance, Termination, Migration, Orphaning, and Cascading Consequence",
        "selected_primary_evidence_id": "SRC-0012",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-10",
        "selected_architecture": "Typed Bitemporal Truth–Epistemic Provenance Architecture with Profiled Revision and Visibility-Safe Projection (TTEP-PRV)",
        "authoritative_selected_title": "Epistemic State, Perception, Evidence, Knowledge, Belief, Uncertainty, Secrecy, Deception, Memory, Discovery, and Observer-Relative Truth",
        "selected_primary_evidence_id": "SRC-0022",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-11",
        "selected_architecture": "Registered Purpose-Scoped Agency and Personhood Architecture with Orthogonal Consent-Control Planes, Bitemporal Action-Origin Graphs, and Profiled Responsibility (RPSAP-OCC-BAOG-PR)",
        "authoritative_selected_title": "Agency, Personhood, Consent, Control, Responsibility, Decision Authority, Delegation, Coercion, and Autonomous Action",
        "selected_primary_evidence_id": "SRC-0041",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-12",
        "selected_architecture": "Registered Typed Motivational–Behavioral State Architecture with Bounded Deliberation, Pluggable Plan Interfaces, Profiled Learning, and Bitemporal Continuity (RTMBS-BD-PPI-PL-BTC)",
        "authoritative_selected_title": "Goals, Values, Needs, Drives, Emotion, Personality, Deliberation, Planning, Learning, and Behavioral Continuity",
        "selected_primary_evidence_id": "SRC-0072",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-13",
        "selected_architecture": "Registered Multiplex Social-State Architecture with Domain-Scoped Trust, Audience-Relative Reputation, Modular Culture–Norm Profiles, and Bitemporal Network Continuity (RMSSA-DT-ARR-MCNP-BNC)",
        "authoritative_selected_title": "Social Relationships, Trust, Reputation, Status, Norms, Culture, Affiliation, and Group Dynamics",
        "selected_primary_evidence_id": "SRC-0082",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-14",
        "selected_architecture": "Registered Bitemporal Communication–Interpretation Architecture with Segmented Signal–Expression–Interpretation Pipelines, Multidimensional Dialogue Acts, Protocol-Governed Conversation State, and Validated Model Realization (RBCIA-SEIP-MDA-PGCS-VMR)",
        "authoritative_selected_title": "Communication Language Meaning Dialogue Acts Conversation State Interpretation Argumentation Persuasion Negotiation and Interaction Protocols",
        "selected_primary_evidence_id": "SRC-0103",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-15",
        "selected_architecture": "Registered Federated Institutional–Jurisdictional Architecture with Relational Normative Positions, Versioned Rule Materials, Protocol-Governed Adjudication, Profiled Legitimacy, and Separated Enforcement Authorization and Execution (RFIJA-RNP-VRM-PGA-PL-SEA)",
        "authoritative_selected_title": "Institutions Governance Jurisdiction Rights Law Policy Adjudication Legitimacy and Enforcement",
        "selected_primary_evidence_id": "SRC-0125",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-16",
        "selected_architecture": "Registered Federated Embodiment–Integrity Architecture with Typed Component–Function–Dependency Graphs, Staged Exposure–Transfer–Effect Pipelines, Profile-Scoped Injury–Condition–Death Families, and Bitemporal Recovery–Transformation Continuity (RFEIA-CFDG-SETE-ICD-BRTC)",
        "authoritative_selected_title": "Bodies Structures Integrity Harm Damage Injury Conditions Impairment Death Recovery Repair Replacement and Transformation",
        "selected_primary_evidence_id": "SRC-0152",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-17",
        "selected_architecture": "Registered Federated Environment–Process Architecture with Typed Region–Medium–Field Ownership, Bounded Source–Transport–Hazard Graphs, Profile-Scoped Terrain–Weather–Ecology Families, and Bitemporal Observation–Materialization Continuity (RFEPA-RMF-STHG-TWE-OMC)",
        "authoritative_selected_title": "Environment, Media, Atmosphere, Weather, Terrain, Hazards, Contamination, Exposure, Ecological Processes, and Environmental Change",
        "selected_primary_evidence_id": "SRC-0180",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-18",
        "selected_architecture": "Registered Federated Spatiotemporal Topology Architecture with Typed Domain–Frame–Support Ownership, Plural Metric–Reachability Profiles, Atomic Movement–Occupancy Transitions, and Bitemporal Map–Materialization Continuity (RFSTA-DFS-PMR-AMO-MMC)",
        "authoritative_selected_title": "Space, Location, Position, Scale, Boundaries, Distance, Proximity, Reachability, Movement, Navigation, and Spatial Topology",
        "selected_primary_evidence_id": "SRC-0207",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-19",
        "selected_architecture": "Registered Federated Capability–Opportunity–Targeting–Resolution Architecture with Typed Readiness–Eligibility Closure, Pluggable Deterministic/Stochastic Resolvers, Bounded Trigger–Reaction Partial Orders, and Owner-Prepared Multi-Domain Effect Commitments",
        "authoritative_selected_title": "Capabilities, Opportunities, Targeting, Contests, Reactions, Interrupts, Conflict, Combat, and Multi-Actor Action Resolution",
        "selected_primary_evidence_id": "SRC-0231",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      },
      {
        "afqr_id": "AFQR-20",
        "selected_architecture": "Registered Federated Signal–Sensing–Acquisition Architecture with Typed Source–Modality–Propagation Ownership, Staged Exposure–Acquisition–Detection–Recognition Pipelines, Observer-Relative Concealment–Countermeasure Profiles, and Bitemporal Contact–Track–Evidence Continuity",
        "authoritative_selected_title": "Signals Sensing Attention Perception Detection Recognition Search Concealment Stealth Tracking Surveillance and Information Acquisition",
        "selected_primary_evidence_id": "SRC-0255",
        "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md",
        "source_status": "accepted_architectural_decision",
        "archive_provenance": "manifest-backed",
        "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md",
        "superseded_or_stale_handling": "excluded from primary authority",
        "duplicate_authority_conflict": false,
        "temporary_note_is_owner": false,
        "zip_packaging_is_owner": false,
        "result": "pass"
      }
    ]
  },
  "r1b_completeness": {
    "result": "pass",
    "actual_term_count": 41,
    "reviewed_term_ids": [
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
    "owners_nonowners_and_qualifications_preserved": true,
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
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-02",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-002",
        "partition": "core_internal",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-03",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-003",
        "partition": "core_internal",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-04",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-004",
        "partition": "core_internal",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-05",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-005",
        "partition": "core_internal",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-06",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-006",
        "partition": "core_internal",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-07",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-007",
        "partition": "core_internal",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-08",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-008",
        "partition": "core_internal",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-09",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-009",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-10",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-010",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-11",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-011",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-12",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-012",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-13",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-013",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-14",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-014",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-015",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-16",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-016",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-17",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-017",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-18",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-018",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-019",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-01",
        "consumer_afqr": "AFQR-20",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-01",
          "r1b_terms": [
            "TERM-003",
            "TERM-004"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-003",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            },
            {
              "term_id": "TERM-004",
              "owner_kind": "afqr",
              "owner_id": "AFQR-01"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "commit",
        "result": "pass"
      },
      {
        "edge_id": "DEP-020",
        "partition": "core_internal",
        "producer_afqr": "AFQR-02",
        "consumer_afqr": "AFQR-03",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-02",
          "r1b_terms": [
            "TERM-006"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-006",
              "owner_kind": "afqr",
              "owner_id": "AFQR-02"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "command_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-021",
        "partition": "core_internal",
        "producer_afqr": "AFQR-02",
        "consumer_afqr": "AFQR-04",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-02",
          "r1b_terms": [
            "TERM-006"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-006",
              "owner_kind": "afqr",
              "owner_id": "AFQR-02"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "command_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-022",
        "partition": "core_internal",
        "producer_afqr": "AFQR-02",
        "consumer_afqr": "AFQR-09",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-02",
          "r1b_terms": [
            "TERM-006"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-006",
              "owner_kind": "afqr",
              "owner_id": "AFQR-02"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "command_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-023",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-02",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-02",
          "r1b_terms": [
            "TERM-006"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-006",
              "owner_kind": "afqr",
              "owner_id": "AFQR-02"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "command_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-024",
        "partition": "core_internal",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-02",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-025",
        "partition": "core_internal",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-06",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-026",
        "partition": "core_internal",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-07",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-027",
        "partition": "core_internal",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-08",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-028",
        "partition": "core_internal",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-09",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-029",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-18",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-030",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-031",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-04",
        "consumer_afqr": "AFQR-20",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-04",
          "r1b_terms": [
            "TERM-027",
            "TERM-028"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-027",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            },
            {
              "term_id": "TERM-028",
              "owner_kind": "afqr",
              "owner_id": "AFQR-04"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "time_causality",
        "result": "pass"
      },
      {
        "edge_id": "DEP-032",
        "partition": "core_internal",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-03",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-033",
        "partition": "core_internal",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-06",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-034",
        "partition": "core_internal",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-07",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-035",
        "partition": "core_internal",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-08",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-036",
        "partition": "core_internal",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-09",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-037",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-10",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-038",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-11",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-039",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-13",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-040",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-14",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-041",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-042",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-16",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-043",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-17",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-044",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-18",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-045",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-046",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-05",
        "consumer_afqr": "AFQR-20",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-05",
          "r1b_terms": [],
          "r1b_term_bindings": [],
          "ownership_basis": "direct_source_contract_not_producer_status"
        },
        "relation_or_handoff_kind": "interface_bridge",
        "result": "pass"
      },
      {
        "edge_id": "DEP-047",
        "partition": "core_internal",
        "producer_afqr": "AFQR-06",
        "consumer_afqr": "AFQR-07",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-06",
          "r1b_terms": [
            "TERM-018",
            "TERM-019"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-018",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            },
            {
              "term_id": "TERM-019",
              "qualified_form": "arbitration evidence",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "claim_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-048",
        "partition": "core_internal",
        "producer_afqr": "AFQR-06",
        "consumer_afqr": "AFQR-08",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-06",
          "r1b_terms": [
            "TERM-018",
            "TERM-019"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-018",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            },
            {
              "term_id": "TERM-019",
              "qualified_form": "arbitration evidence",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "claim_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-049",
        "partition": "core_internal",
        "producer_afqr": "AFQR-06",
        "consumer_afqr": "AFQR-09",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-06",
          "r1b_terms": [
            "TERM-018",
            "TERM-019"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-018",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            },
            {
              "term_id": "TERM-019",
              "qualified_form": "arbitration evidence",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "claim_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-050",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-06",
        "consumer_afqr": "AFQR-10",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-06",
          "r1b_terms": [
            "TERM-018",
            "TERM-019"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-018",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            },
            {
              "term_id": "TERM-019",
              "qualified_form": "arbitration evidence",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "claim_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-051",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-06",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-06",
          "r1b_terms": [
            "TERM-018",
            "TERM-019"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-018",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            },
            {
              "term_id": "TERM-019",
              "qualified_form": "arbitration evidence",
              "owner_kind": "afqr",
              "owner_id": "AFQR-06"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "claim_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-052",
        "partition": "core_internal",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-06",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-053",
        "partition": "core_internal",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-07",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-054",
        "partition": "core_internal",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-09",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-055",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-10",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-056",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-11",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-057",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-12",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-058",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-13",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-059",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-060",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-08",
        "consumer_afqr": "AFQR-16",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-08",
          "r1b_terms": [
            "TERM-013"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-013",
              "owner_kind": "afqr",
              "owner_id": "AFQR-08"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "identity_evidence",
        "result": "pass"
      },
      {
        "edge_id": "DEP-061",
        "partition": "core_internal",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-01",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-062",
        "partition": "core_internal",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-02",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-063",
        "partition": "core_internal",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-04",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-064",
        "partition": "core_internal",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-06",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-065",
        "partition": "core_internal",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-07",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-066",
        "partition": "core_internal",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-08",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-067",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-11",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-068",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-13",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-069",
        "partition": "core_agency_boundary",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-070",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-16",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-071",
        "partition": "core_world_boundary",
        "producer_afqr": "AFQR-09",
        "consumer_afqr": "AFQR-17",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-09",
          "r1b_terms": [
            "TERM-023"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-023",
              "owner_kind": "afqr",
              "owner_id": "AFQR-09"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "relation_lifecycle",
        "result": "pass"
      },
      {
        "edge_id": "DEP-072",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-11",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-073",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-12",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-074",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-13",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-075",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-14",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-076",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-077",
        "partition": "agency_world_boundary",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-17",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-078",
        "partition": "agency_world_boundary",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-079",
        "partition": "agency_world_boundary",
        "producer_afqr": "AFQR-10",
        "consumer_afqr": "AFQR-20",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-10",
          "r1b_terms": [
            "TERM-001"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-001",
              "qualified_form": "epistemic state",
              "owner_kind": "afqr",
              "owner_id": "AFQR-10"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "epistemic_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-080",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-11",
        "consumer_afqr": "AFQR-12",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-11",
          "r1b_terms": [
            "TERM-016"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-016",
              "owner_kind": "afqr",
              "owner_id": "AFQR-11"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "agency_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-081",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-11",
        "consumer_afqr": "AFQR-13",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-11",
          "r1b_terms": [
            "TERM-016"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-016",
              "owner_kind": "afqr",
              "owner_id": "AFQR-11"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "agency_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-082",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-11",
        "consumer_afqr": "AFQR-14",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-11",
          "r1b_terms": [
            "TERM-016"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-016",
              "owner_kind": "afqr",
              "owner_id": "AFQR-11"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "agency_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-083",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-11",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-11",
          "r1b_terms": [
            "TERM-016"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-016",
              "owner_kind": "afqr",
              "owner_id": "AFQR-11"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "agency_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-084",
        "partition": "agency_world_boundary",
        "producer_afqr": "AFQR-11",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-11",
          "r1b_terms": [
            "TERM-016"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-016",
              "owner_kind": "afqr",
              "owner_id": "AFQR-11"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "agency_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-085",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-14",
        "consumer_afqr": "AFQR-13",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-14",
          "r1b_terms": [
            "TERM-031"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-031",
              "owner_kind": "afqr",
              "owner_id": "AFQR-14"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "communication_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-086",
        "partition": "agency_internal",
        "producer_afqr": "AFQR-14",
        "consumer_afqr": "AFQR-15",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-14",
          "r1b_terms": [
            "TERM-031"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-031",
              "owner_kind": "afqr",
              "owner_id": "AFQR-14"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "communication_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-087",
        "partition": "agency_world_boundary",
        "producer_afqr": "AFQR-14",
        "consumer_afqr": "AFQR-20",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-14",
          "r1b_terms": [
            "TERM-031"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-031",
              "owner_kind": "afqr",
              "owner_id": "AFQR-14"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "communication_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-088",
        "partition": "world_internal",
        "producer_afqr": "AFQR-17",
        "consumer_afqr": "AFQR-16",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-17",
          "r1b_terms": [
            "TERM-037"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-037",
              "owner_kind": "afqr",
              "owner_id": "AFQR-17"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "environment_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-089",
        "partition": "world_internal",
        "producer_afqr": "AFQR-17",
        "consumer_afqr": "AFQR-18",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-17",
          "r1b_terms": [
            "TERM-037"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-037",
              "owner_kind": "afqr",
              "owner_id": "AFQR-17"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "environment_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-090",
        "partition": "world_internal",
        "producer_afqr": "AFQR-17",
        "consumer_afqr": "AFQR-20",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-17",
          "r1b_terms": [
            "TERM-037"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-037",
              "owner_kind": "afqr",
              "owner_id": "AFQR-17"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "environment_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-091",
        "partition": "world_internal",
        "producer_afqr": "AFQR-18",
        "consumer_afqr": "AFQR-17",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-18",
          "r1b_terms": [
            "TERM-038"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-038",
              "owner_kind": "afqr",
              "owner_id": "AFQR-18"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "space_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-092",
        "partition": "world_internal",
        "producer_afqr": "AFQR-18",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-18",
          "r1b_terms": [
            "TERM-038"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-038",
              "owner_kind": "afqr",
              "owner_id": "AFQR-18"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "space_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-093",
        "partition": "world_internal",
        "producer_afqr": "AFQR-18",
        "consumer_afqr": "AFQR-20",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-18",
          "r1b_terms": [
            "TERM-038"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-038",
              "owner_kind": "afqr",
              "owner_id": "AFQR-18"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "space_handoff",
        "result": "pass"
      },
      {
        "edge_id": "DEP-094",
        "partition": "world_internal",
        "producer_afqr": "AFQR-20",
        "consumer_afqr": "AFQR-19",
        "semantic_type_owner": {
          "owner_kind": "afqr",
          "owner_id": "AFQR-19",
          "r1b_terms": [
            "TERM-011"
          ],
          "r1b_term_bindings": [
            {
              "term_id": "TERM-011",
              "owner_kind": "afqr",
              "owner_id": "AFQR-19"
            }
          ],
          "ownership_basis": "merged_r1b_term_owner"
        },
        "relation_or_handoff_kind": "contact_targeting",
        "result": "pass"
      }
    ]
  },
  "r1d_completeness": {
    "result": "pass",
    "historical_completion_boundaries_preserved": true,
    "cross_family_parity": "exact",
    "r1e_authority_claimed_by_r1d": false
  },
  "twenty_afqr_source_matrix": [
    {
      "afqr_id": "AFQR-01",
      "selected_architecture": "Atomic Typed Transition Journal with Owner-Specific Reducers and Declared Saga Escape Hatches",
      "authoritative_selected_title": "Atomic State Transition, Ownership, Commitment, Recovery, and Replay",
      "selected_primary_evidence_id": "SRC-0004",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-02",
      "selected_architecture": "Synchronous Command Fast Path with Durable Attempt Escalation",
      "authoritative_selected_title": "Command Identity, Attempts, Retries, Suspension, Escalation, and Durable Progress",
      "selected_primary_evidence_id": "SRC-0005",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-03",
      "selected_architecture": "Typed Action Gateway with Registered Semantics, Capability-Affordance Composition, and Bounded Plan Verification",
      "authoritative_selected_title": "Action Representation, Capability, Affordance, Method Selection, and Bounded Plans",
      "selected_primary_evidence_id": "SRC-0006",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-04",
      "selected_architecture": "Profiled Logical-Time Causal Scheduler with Deterministic Resolution Groups and Bounded Cascade Microsteps",
      "authoritative_selected_title": "Logical Time, Simultaneity, Causal Ordering, Scheduled Effects, and Bounded Cascades",
      "selected_primary_evidence_id": "SRC-0007",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-05",
      "selected_architecture": "Registered Typed Interface-and-Bridge Hypergraph",
      "authoritative_selected_title": "Cross-System Interfaces, Adapters, Bridges, Hyperedges, and Compatibility",
      "selected_primary_evidence_id": "SRC-0008",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-06",
      "selected_architecture": "Invariant-Gated Typed Claim Arbitration",
      "authoritative_selected_title": "Claim Discovery, Admissibility, Conflict, Arbitration, Choice, and Hidden Evidence",
      "selected_primary_evidence_id": "SRC-0009",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-07",
      "selected_architecture": "Typed Balance-Domain Flow Ledger with Proof-Carrying Conversion and Atomic Settlement",
      "authoritative_selected_title": "Cross-Domain Conservation, Conversion Validity, Reservation, Settlement, and Arbitrage Prevention",
      "selected_primary_evidence_id": "SRC-0010",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-08",
      "selected_architecture": "Typed Faceted Identity, Continuity, and Lineage Graph with Purpose-Scoped Equivalence",
      "authoritative_selected_title": "Identity, Continuity, Copying, Transformation, Proxyhood, Reinstantiation, Fusion, Fission, and Contextual Equivalence",
      "selected_primary_evidence_id": "SRC-0011",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-09",
      "selected_architecture": "Registered Typed Dependency-and-Obligation Hypergraph with Version-Pinned Lifecycle Policies and Bounded Causal Propagation",
      "authoritative_selected_title": "Dependency, Revocation, Inheritance, Termination, Migration, Orphaning, and Cascading Consequence",
      "selected_primary_evidence_id": "SRC-0012",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-10",
      "selected_architecture": "Typed Bitemporal Truth–Epistemic Provenance Architecture with Profiled Revision and Visibility-Safe Projection (TTEP-PRV)",
      "authoritative_selected_title": "Epistemic State, Perception, Evidence, Knowledge, Belief, Uncertainty, Secrecy, Deception, Memory, Discovery, and Observer-Relative Truth",
      "selected_primary_evidence_id": "SRC-0022",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-11",
      "selected_architecture": "Registered Purpose-Scoped Agency and Personhood Architecture with Orthogonal Consent-Control Planes, Bitemporal Action-Origin Graphs, and Profiled Responsibility (RPSAP-OCC-BAOG-PR)",
      "authoritative_selected_title": "Agency, Personhood, Consent, Control, Responsibility, Decision Authority, Delegation, Coercion, and Autonomous Action",
      "selected_primary_evidence_id": "SRC-0041",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-12",
      "selected_architecture": "Registered Typed Motivational–Behavioral State Architecture with Bounded Deliberation, Pluggable Plan Interfaces, Profiled Learning, and Bitemporal Continuity (RTMBS-BD-PPI-PL-BTC)",
      "authoritative_selected_title": "Goals, Values, Needs, Drives, Emotion, Personality, Deliberation, Planning, Learning, and Behavioral Continuity",
      "selected_primary_evidence_id": "SRC-0072",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-13",
      "selected_architecture": "Registered Multiplex Social-State Architecture with Domain-Scoped Trust, Audience-Relative Reputation, Modular Culture–Norm Profiles, and Bitemporal Network Continuity (RMSSA-DT-ARR-MCNP-BNC)",
      "authoritative_selected_title": "Social Relationships, Trust, Reputation, Status, Norms, Culture, Affiliation, and Group Dynamics",
      "selected_primary_evidence_id": "SRC-0082",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-14",
      "selected_architecture": "Registered Bitemporal Communication–Interpretation Architecture with Segmented Signal–Expression–Interpretation Pipelines, Multidimensional Dialogue Acts, Protocol-Governed Conversation State, and Validated Model Realization (RBCIA-SEIP-MDA-PGCS-VMR)",
      "authoritative_selected_title": "Communication Language Meaning Dialogue Acts Conversation State Interpretation Argumentation Persuasion Negotiation and Interaction Protocols",
      "selected_primary_evidence_id": "SRC-0103",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-15",
      "selected_architecture": "Registered Federated Institutional–Jurisdictional Architecture with Relational Normative Positions, Versioned Rule Materials, Protocol-Governed Adjudication, Profiled Legitimacy, and Separated Enforcement Authorization and Execution (RFIJA-RNP-VRM-PGA-PL-SEA)",
      "authoritative_selected_title": "Institutions Governance Jurisdiction Rights Law Policy Adjudication Legitimacy and Enforcement",
      "selected_primary_evidence_id": "SRC-0125",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-16",
      "selected_architecture": "Registered Federated Embodiment–Integrity Architecture with Typed Component–Function–Dependency Graphs, Staged Exposure–Transfer–Effect Pipelines, Profile-Scoped Injury–Condition–Death Families, and Bitemporal Recovery–Transformation Continuity (RFEIA-CFDG-SETE-ICD-BRTC)",
      "authoritative_selected_title": "Bodies Structures Integrity Harm Damage Injury Conditions Impairment Death Recovery Repair Replacement and Transformation",
      "selected_primary_evidence_id": "SRC-0152",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-17",
      "selected_architecture": "Registered Federated Environment–Process Architecture with Typed Region–Medium–Field Ownership, Bounded Source–Transport–Hazard Graphs, Profile-Scoped Terrain–Weather–Ecology Families, and Bitemporal Observation–Materialization Continuity (RFEPA-RMF-STHG-TWE-OMC)",
      "authoritative_selected_title": "Environment, Media, Atmosphere, Weather, Terrain, Hazards, Contamination, Exposure, Ecological Processes, and Environmental Change",
      "selected_primary_evidence_id": "SRC-0180",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-18",
      "selected_architecture": "Registered Federated Spatiotemporal Topology Architecture with Typed Domain–Frame–Support Ownership, Plural Metric–Reachability Profiles, Atomic Movement–Occupancy Transitions, and Bitemporal Map–Materialization Continuity (RFSTA-DFS-PMR-AMO-MMC)",
      "authoritative_selected_title": "Space, Location, Position, Scale, Boundaries, Distance, Proximity, Reachability, Movement, Navigation, and Spatial Topology",
      "selected_primary_evidence_id": "SRC-0207",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-19",
      "selected_architecture": "Registered Federated Capability–Opportunity–Targeting–Resolution Architecture with Typed Readiness–Eligibility Closure, Pluggable Deterministic/Stochastic Resolvers, Bounded Trigger–Reaction Partial Orders, and Owner-Prepared Multi-Domain Effect Commitments",
      "authoritative_selected_title": "Capabilities, Opportunities, Targeting, Contests, Reactions, Interrupts, Conflict, Combat, and Multi-Actor Action Resolution",
      "selected_primary_evidence_id": "SRC-0231",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    },
    {
      "afqr_id": "AFQR-20",
      "selected_architecture": "Registered Federated Signal–Sensing–Acquisition Architecture with Typed Source–Modality–Propagation Ownership, Staged Exposure–Acquisition–Detection–Recognition Pipelines, Observer-Relative Concealment–Countermeasure Profiles, and Bitemporal Contact–Track–Evidence Continuity",
      "authoritative_selected_title": "Signals Sensing Attention Perception Detection Recognition Search Concealment Stealth Tracking Surveillance and Information Acquisition",
      "selected_primary_evidence_id": "SRC-0255",
      "selected_primary_source_path": "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md",
      "source_status": "accepted_architectural_decision",
      "archive_provenance": "manifest-backed",
      "extraction_or_normalization_path": "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md",
      "superseded_or_stale_handling": "excluded from primary authority",
      "duplicate_authority_conflict": false,
      "temporary_note_is_owner": false,
      "zip_packaging_is_owner": false,
      "result": "pass"
    }
  ],
  "shared_term_completeness_summary": {
    "count": 41,
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
    "core_agency": 21,
    "core_world": 17,
    "agency_world": 5,
    "result": "pass"
  },
  "cycle_decisions": [
    {
      "cycle_id": "CYCLE-001",
      "edge_ids": [
        "DEP-008",
        "DEP-061"
      ],
      "breaker": "AFQR-01 owns transition routing and commitment; AFQR-09 owns governed relation and dependency lifecycle. A committed transition may update a relation, and a relation constraint may govern a later transition, but neither output self-validates or transfers authority.",
      "decision": "bounded_as_r1c"
    },
    {
      "cycle_id": "CYCLE-002",
      "edge_ids": [
        "DEP-021",
        "DEP-024"
      ],
      "breaker": "AFQR-02 owns command identity, attempts, retries, suspension, escalation, and durable command progress. AFQR-04 owns logical time, causal ordering, simultaneity, scheduling, and bounded cascades. Logical time may order command-lifecycle events but cannot create or redefine command identity; command lifecycle may request or consume scheduling but cannot author logical time.",
      "decision": "bounded_as_r1c"
    },
    {
      "cycle_id": "CYCLE-003",
      "edge_ids": [
        "DEP-048",
        "DEP-052"
      ],
      "breaker": "AFQR-06 owns claims, evidence admissibility, conflict, and arbitration; AFQR-08 owns identity and continuity semantics. Identity records may be offered as evidence to AFQR-06. AFQR-06 may accept, reject, qualify, or dispute that evidence but cannot create identity merely by admitting a claim; AFQR-08 identity assertions cannot self-certify admissibility or truth.",
      "decision": "bounded_as_r1c"
    },
    {
      "cycle_id": "CYCLE-004",
      "edge_ids": [
        "DEP-089",
        "DEP-091"
      ],
      "breaker": "AFQR-17 environmental process constraints and AFQR-18 spatial/topology constraints may inform later owner-qualified evaluation. Neither handoff recursively authors the other domain or validates itself; unresolved generic owner-contract needs remain escalated.",
      "decision": "bounded_as_r1c"
    }
  ],
  "dependency_risk_decisions": [
    {
      "risk_id": "CYCLE-RISK-001",
      "edge_ids": [
        "DEP-022",
        "DEP-062"
      ],
      "decision": "bounded_as_r1c"
    },
    {
      "risk_id": "CYCLE-RISK-002",
      "edge_ids": [
        "DEP-028",
        "DEP-063"
      ],
      "decision": "bounded_as_r1c"
    },
    {
      "risk_id": "CYCLE-RISK-003",
      "edge_ids": [
        "DEP-049",
        "DEP-064"
      ],
      "decision": "bounded_as_r1c"
    },
    {
      "risk_id": "CYCLE-RISK-004",
      "edge_ids": [
        "DEP-054",
        "DEP-066"
      ],
      "decision": "bounded_as_r1c"
    }
  ],
  "missing_substrate_decisions": [
    {
      "substrate_id": "SUB-001",
      "name": "generalized governed-relation registry",
      "requiring_afqrs": [
        "AFQR-09",
        "AFQR-13",
        "AFQR-15"
      ],
      "evidence": [
        "SRC-0012",
        "SRC-0082",
        "SRC-0125"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
      ],
      "future_owner_posture": "unresolved: AFQR-09 owns governed relation/dependency semantics while COLL-08 prevents a universal jurisdiction, institution, authority, dependency, or social-state owner",
      "lawful_later_gate": "R1D doctrine-family contracts; any implementation is deferred beyond R1",
      "owner_separation": "all listed AFQR semantic owners remain separate",
      "combined_owner_prohibited": true,
      "failure_or_collapse_risk": "Omission collapses dependency into obligation, reachability into jurisdiction, or relation records into institutional authority/social standing.",
      "implementation_status": "unimplemented",
      "decision": "accepted_as_classified_deferred_substrate"
    },
    {
      "substrate_id": "SUB-002",
      "name": "generalized bitemporal truth/evidence store",
      "requiring_afqrs": [
        "AFQR-04",
        "AFQR-06",
        "AFQR-10",
        "AFQR-20"
      ],
      "evidence": [
        "SRC-0007",
        "SRC-0009",
        "SRC-0022",
        "SRC-0255"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
      ],
      "future_owner_posture": "unresolved cross-owner substrate: AFQR-04 time, AFQR-06 arbitration evidence, AFQR-10 epistemic/truth, and AFQR-20 sensing retain their own semantics",
      "lawful_later_gate": "R1D doctrine-family contracts; persistence and runtime realization require a later authorized gate",
      "owner_separation": "all listed AFQR semantic owners remain separate",
      "combined_owner_prohibited": true,
      "failure_or_collapse_risk": "Omission permits hidden-truth leakage, retroactive evidence overwrite, or logical time to manufacture truth/admissibility.",
      "implementation_status": "unimplemented",
      "decision": "accepted_as_classified_deferred_substrate"
    },
    {
      "substrate_id": "SUB-003",
      "name": "generalized owner-reducer transaction journal",
      "requiring_afqrs": [
        "AFQR-01",
        "AFQR-02",
        "AFQR-04",
        "AFQR-09"
      ],
      "evidence": [
        "SRC-0004",
        "SRC-0005",
        "SRC-0007",
        "SRC-0012"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
      ],
      "future_owner_posture": "AFQR-01 for transition/commitment journal doctrine; participating domain semantics remain with AFQR-02, AFQR-04, and AFQR-09",
      "lawful_later_gate": "R1D transition/lifecycle doctrine; runtime journal implementation remains blocked for later runtime gates",
      "owner_separation": "all listed AFQR semantic owners remain separate",
      "combined_owner_prohibited": true,
      "failure_or_collapse_risk": "Omission allows replay to duplicate commitment, recovery to rewrite command identity, or causal/dependency consequences to recurse without bounds.",
      "implementation_status": "unimplemented",
      "decision": "accepted_as_classified_deferred_substrate"
    },
    {
      "substrate_id": "SUB-004",
      "name": "registered interface/bridge hypergraph",
      "requiring_afqrs": [
        "AFQR-05"
      ],
      "evidence": [
        "SRC-0008"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md"
      ],
      "future_owner_posture": "AFQR-05",
      "lawful_later_gate": "R1D interface/bridge doctrine; registration services and adapters require a later authorized implementation gate",
      "owner_separation": "all listed AFQR semantic owners remain separate",
      "combined_owner_prohibited": true,
      "failure_or_collapse_risk": "Omission encourages pairwise ad hoc adapters, package-symbol ownership inference, and donor-specific compatibility becoming Astra law.",
      "implementation_status": "unimplemented",
      "decision": "accepted_as_classified_deferred_substrate"
    },
    {
      "substrate_id": "SUB-005",
      "name": "generalized spatial, signal, embodiment, institution, and social owner contracts",
      "requiring_afqrs": [
        "AFQR-13",
        "AFQR-15",
        "AFQR-16",
        "AFQR-18",
        "AFQR-20"
      ],
      "evidence": [
        "SRC-0082",
        "SRC-0125",
        "SRC-0152",
        "SRC-0207",
        "SRC-0255"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
      ],
      "future_owner_posture": "separate source-backed owners: AFQR-18 spatial/topology; AFQR-20 signal/sensing; AFQR-16 embodiment; AFQR-15 institution/jurisdiction; AFQR-13 social state, subject to preserved COLL-03 and COLL-08 seams",
      "lawful_later_gate": "R1D separate domain-family doctrine files; no combined runtime substrate is authorized",
      "owner_separation": "all listed AFQR semantic owners remain separate",
      "combined_owner_prohibited": true,
      "failure_or_collapse_risk": "Omission conflates topology with embodiment, sensing with truth, institution with jurisdiction, or social state with identity/authority.",
      "implementation_status": "unimplemented",
      "decision": "accepted_as_classified_deferred_substrate"
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
      "r1c_evidence": [
        "preserved escalation COLL-03"
      ],
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
        "single universal owner",
        "consumer ownership",
        "source-local ambiguity",
        "deferred blocking"
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
        "state/write/resource/property/contract ownership remain qualified or source-local",
        "office, delegation, proxyhood, possession, bodies, clones, vehicles, command, and legal/moral/causal responsibility route to their distinct owners"
      ],
      "decision": "approved_with_qualification",
      "supersession_scope": "supersedes only the historical unresolved disposition; R1B/R1C evidence remains historical",
      "ledger_disposition": "closed_by_r1e",
      "residual_questions": [
        "donor-specific mapping remains R2 work"
      ],
      "downstream_impact": "removes the R1 completion blocker without granting implementation"
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
      "r1c_evidence": [
        "preserved escalation COLL-08"
      ],
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
        "single universal owner",
        "consumer ownership",
        "source-local ambiguity",
        "deferred blocking"
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
        "citizenship, membership, employment, office, territory, contracts, emergency power and enforcement require typed institutional attribution",
        "reputation, informal leadership and prestige remain social rather than jurisdictional"
      ],
      "decision": "approved_with_qualification",
      "supersession_scope": "supersedes only the historical unresolved disposition; R1B/R1C evidence remains historical",
      "ledger_disposition": "closed_by_r1e",
      "residual_questions": [
        "donor-specific mapping remains R2 work"
      ],
      "downstream_impact": "removes the R1 completion blocker without granting implementation"
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
      "r1c_evidence": [
        "preserved escalation COLL-10"
      ],
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
        "single universal owner",
        "consumer ownership",
        "source-local ambiguity",
        "deferred blocking"
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
        "compulsion, control, addiction, trauma, capacity and coercion are evidence inputs to AFQR-11 attribution",
        "AI, swarms and collective agents require purpose-scoped agency; causal contribution remains distinct from legal or moral responsibility"
      ],
      "decision": "approved_with_qualification",
      "supersession_scope": "supersedes only the historical unresolved disposition; R1B/R1C evidence remains historical",
      "ledger_disposition": "closed_by_r1e",
      "residual_questions": [
        "donor-specific mapping remains R2 work"
      ],
      "downstream_impact": "removes the R1 completion blocker without granting implementation"
    }
  ],
  "escalation_ledger_reconciliation": {
    "pre_review_open_set": [
      "COLL-03",
      "COLL-08",
      "COLL-10"
    ],
    "r1b_post_review_status": "closed_by_r1e",
    "r1c_post_review_status": "closed_by_r1e",
    "historical_entries_preserved": true
  },
  "cross_artifact_consistency_matrix": [
    {
      "matrix_id": "CONS-001",
      "producer_artifact": "R1A",
      "consumer_artifact": "R1B",
      "comparison_class": "R1A -> R1B",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1A -> R1B"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-002",
      "producer_artifact": "R1A",
      "consumer_artifact": "R1C",
      "comparison_class": "R1A -> R1C",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1A -> R1C"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-003",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1C",
      "comparison_class": "R1B -> R1C",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1B -> R1C"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-004",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1D-CORE",
      "comparison_class": "R1B -> R1D-CORE",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1B -> R1D-CORE"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-005",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1D-AGENCY",
      "comparison_class": "R1B -> R1D-AGENCY",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1B -> R1D-AGENCY"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-006",
      "producer_artifact": "R1B",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "R1B -> R1D-WORLD",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1B -> R1D-WORLD"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-007",
      "producer_artifact": "R1C",
      "consumer_artifact": "R1D-CORE",
      "comparison_class": "R1C -> R1D-CORE",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1C -> R1D-CORE"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-008",
      "producer_artifact": "R1C",
      "consumer_artifact": "R1D-AGENCY",
      "comparison_class": "R1C -> R1D-AGENCY",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1C -> R1D-AGENCY"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-009",
      "producer_artifact": "R1C",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "R1C -> R1D-WORLD",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1C -> R1D-WORLD"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-010",
      "producer_artifact": "R1D-CORE",
      "consumer_artifact": "R1D-AGENCY",
      "comparison_class": "R1D-CORE <-> R1D-AGENCY",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1D-CORE <-> R1D-AGENCY"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-011",
      "producer_artifact": "R1D-CORE",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "R1D-CORE <-> R1D-WORLD",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1D-CORE <-> R1D-WORLD"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-012",
      "producer_artifact": "R1D-AGENCY",
      "consumer_artifact": "R1D-WORLD",
      "comparison_class": "R1D-AGENCY <-> R1D-WORLD",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1D-AGENCY <-> R1D-WORLD"
      ],
      "blocking_status": "nonblocking"
    },
    {
      "matrix_id": "CONS-013",
      "producer_artifact": "R1D",
      "consumer_artifact": "R1E",
      "comparison_class": "R1D -> R1E",
      "exact_records_compared": "all applicable selected sources, terms, edges, cycles, risks, collisions, substrates, and gates",
      "result": "pass",
      "contradictions": [],
      "missing_records": [],
      "surplus_records": [],
      "authority_transfer_check": "pass_no_transfer",
      "evidence": [
        "R1D -> R1E"
      ],
      "blocking_status": "nonblocking"
    }
  ],
  "corpus_scale_adequacy_matrix": [
    {
      "donor_family": "fantasy",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "science fiction",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "hybrid science-fantasy",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "cultivation",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "class and archetype",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "profession and occupation",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "point-buy",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "narrative tag/aspect",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "cyberware and biotech",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "psionic",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "horror and investigation",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "vehicle, mech, ship, and platform",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "companion, summon, familiar, proxy, swarm",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "crafting, salvage, repair, and requisition",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "bestiary",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "random tables and oracles",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "supplements",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
    },
    {
      "donor_family": "adventures and campaign paths",
      "lawful_paths": [
        "direct_mapping",
        "normalized_mapping",
        "source_local_retention",
        "quarantine",
        "doctrine_escalation"
      ],
      "result": "pass"
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
  }
}
```
