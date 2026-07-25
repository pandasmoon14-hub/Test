# AFQR-01–09 R1D-CORE: Core Transaction, Identity, and Relation Doctrine

## 1. Metadata and authority

This modular artifact consolidates, without replacing, the nine selected primary AFQR records. Its machine-reviewable contract below is normative for R1D-CORE. Authority follows merged repository doctrine, R1C, R1B, R1A, then the selected primary records. Temporary evidence is supporting evidence only. RT-001/RT-002 names are narrow fixtures, never ownership proof.

## 2. File ownership and nonownership

R1D-CORE owns only family consolidation, boundaries, typed handoffs, and preservation of upstream contracts. It is not a megafile or an implementation design. Consumption, serialization, storage, commitment, scheduling, arbitration, bridge compatibility, and candidate production never establish ownership.

## 3. AFQR responsibility map

`responsibility_records` contains exactly one stable record for each AFQR-01–09, with exact R1B forms, direct primary evidence, edge-indexed inputs/outputs, seams, and deferred implementation handoffs.

## 4. Internal dependency coverage

All 33 R1C edges with both endpoints in the family appear once in `internal_edge_dispositions`; R1C edge IDs are not renumbered or combined.

## 5. Cross-family boundary coverage

All 38 R1C edges with exactly one core endpoint appear once in `boundary_dispositions`. External records define no AFQR-10–20 internal semantics. AFQR-06 exports evidence without defining knowledge; AFQR-08 exports identity without defining agency or responsibility; AFQR-09 exports relation lifecycle without creating jurisdiction; AFQR-04 exports ordering without defining world processes; AFQR-05 compatibility never absorbs endpoint meaning.

## 6. Core-family invariants

R1C `INV-001` preserves ownership nontransfer. `INV-004` keeps capability, opportunity, action, target, and resolution distinct. `INV-005` prevents identity from conferring control, agency, authority, ownership, or responsibility. `INV-006` preserves relation boundaries; `INV-007` separates reservation and settlement and requires declared conservation; `INV-008` makes replay idempotent and recovery identity-preserving; `INV-009` blocks recursive self-authorization. Family-local `CORE-RULE-001` retains donor action economies, time cadences, resource models, identity/body models, persistence assumptions, bridge topologies, evidence standards, legal meanings, relation models, actor scales, and cosmologies as source-local unless explicitly adopted. Commitment never owns the committed domain; scheduling creates neither command identity nor truth; admission proves neither truth nor identity; transformation cannot silently create/destroy conserved quantity.

## 7. Cycles and dependency risks

The machine contract copies the exact R1C treatments for DEP-008/061, DEP-021/024, and DEP-048/052. It also preserves the bounded, nonrecursive reclassifications for DEP-022/062, DEP-028/063, DEP-049/064, and DEP-054/066. No pair is promoted into a new universal cycle.

## 8. Missing substrates

The R1C substrate records are consumed, not implemented. The generalized governed-relation registry retains AFQR-09 and COLL-08 boundaries; reachability is not obligation or jurisdiction. The bitemporal truth/evidence seam exposes only AFQR-04 ordering and AFQR-06 provenance/admissibility history, leaving epistemic truth and sensing external. The owner-reducer transaction journal remains doctrine for commitment/recovery/replay/lifecycle/order/consequences, not fields, schemas, reducers, databases, or APIs. The registered interface/bridge hypergraph retains AFQR-05 typed-endpoint nontransfer without code or schema.

## 9. Escalations

COLL-03, COLL-08, and COLL-10 remain open exactly as recorded by R1B. COLL-03 joins AFQR-01 qualified state/write-owner and AFQR-08 identity boundaries to AFQR-11/15 doctrine; capability readiness is instead a governed AFQR-03/19 qualified-family handoff. COLL-08 joins AFQR-09 governed-relation lifecycle to AFQR-13/15 doctrine without manufacturing jurisdiction or legitimacy. COLL-10 is primarily external AFQR-11/12/13 motivation, behavior, agency, responsibility, and social-state doctrine; bounded AFQR-06/08/09 outputs cannot author it. Every escalation goes only to R1D-AGENCY, and no universal owner is invented.

## 10. Corpus-scale pressure test

Every required pressure has a landing, external handoff, source-local retention, or escalation. No donor conversion is performed, and no universal action economy, identity/body/clock/resource/relation model, persistence model, bridge topology, evidence standard, actor scale, ownership law, or cosmology is adopted.

## 11. Machine-reviewable R1D-CORE contract

```json
{
  "artifact_id": "AFQR-01-09-R1D-CORE-TRANSACTION-IDENTITY-RELATION-001",
  "artifact_version": "1.0.0",
  "family_identifier": "R1D-CORE",
  "verified_repository_baseline": {
    "verified_base_method": "external GitHub main-ref verification plus exact local SHA match",
    "verified_base_sha": "179bfdda605f45d26ffb018da12805780710bdb3",
    "fetch_status": "unavailable due environment network policy; not a doctrine or baseline defect"
  },
  "included_afqrs": [
    "AFQR-01",
    "AFQR-02",
    "AFQR-03",
    "AFQR-04",
    "AFQR-05",
    "AFQR-06",
    "AFQR-07",
    "AFQR-08",
    "AFQR-09"
  ],
  "excluded_afqrs": [
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
  "authority_boundary": "doctrine family consolidation only; no runtime, persistence, conversion execution, canon/sourcebook, model-facing, narration, live-play, RT-002G, or evidence-deletion authority",
  "prerequisites": [
    "R1A complete",
    "R1B complete",
    "R1C complete"
  ],
  "downstream_gates": {
    "R1D-CORE": "complete",
    "overall_R1D": "incomplete",
    "R1D-AGENCY": "ready_not_started",
    "R1D-WORLD": "ready_not_started",
    "R1E": "blocked",
    "R2-R6": "blocked",
    "RT-002G": "unauthorized"
  },
  "temporary_evidence_status": "present, checksum-backed, temporary, non-authoritative, deletion unauthorized; production imports forbidden",
  "file_ownership": {
    "owns": [
      "AFQR-01–09 family-doctrine consolidation",
      "internal family boundaries",
      "source-backed intra-family handoffs",
      "source-backed cross-family interface declarations",
      "preservation of R1B ownership and R1C invariants"
    ],
    "does_not_own": [
      "runtime types or services",
      "persistence",
      "conversion execution",
      "canon",
      "sourcebook language",
      "model prompts",
      "live-play procedures",
      "AFQR-10–20 semantics",
      "universal donor assumptions"
    ]
  },
  "responsibility_records": [
    {
      "record_id": "CORE-RESP-01",
      "afqr_id": "AFQR-01",
      "owned_concerns": "state-transition routing; exclusive qualified state/write ownership; owner-specific reducers; commitment; recovery; replay; transition receipts",
      "explicit_nonowned_concerns": "generic epistemic, social, environmental, identity, agency, institutional, spatial, or sensing state; committed-domain semantics",
      "r1b_terms_or_qualified_forms": [
        {
          "term_id": "TERM-003",
          "form": "transition",
          "owner": "AFQR-01"
        },
        {
          "term_id": "TERM-004",
          "form": "transaction",
          "owner": "AFQR-01"
        },
        {
          "term_id": "TERM-005",
          "form": "committed event receipt",
          "owner": "AFQR-01"
        },
        {
          "term_id": "TERM-014",
          "form": "state owner",
          "owner": "AFQR-01"
        }
      ],
      "source_evidence_identifiers": [
        "SRC-0004"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md"
      ],
      "internal_family_inputs": [
        "DEP-061"
      ],
      "internal_family_outputs": [
        "DEP-001",
        "DEP-002",
        "DEP-003",
        "DEP-004",
        "DEP-005",
        "DEP-006",
        "DEP-007",
        "DEP-008"
      ],
      "cross_family_inputs": [],
      "cross_family_outputs": [
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
        "DEP-019"
      ],
      "unresolved_seams": [
        "COLL-03: qualified state/write-owner semantics establish neither substantive ownership, authority, agency, consent, control, nor responsibility"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-02",
      "afqr_id": "AFQR-02",
      "owned_concerns": "command identity; attempts; retry identity; suspension; escalation; durable command progress",
      "explicit_nonowned_concerns": "execution; action representation; opportunity; target; resolution",
      "r1b_terms_or_qualified_forms": [
        {
          "term_id": "TERM-006",
          "form": "command",
          "owner": "AFQR-02"
        },
        {
          "term_id": "TERM-007",
          "form": "attempt",
          "owner": "AFQR-02"
        }
      ],
      "source_evidence_identifiers": [
        "SRC-0005"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md"
      ],
      "internal_family_inputs": [
        "DEP-001",
        "DEP-024",
        "DEP-062"
      ],
      "internal_family_outputs": [
        "DEP-020",
        "DEP-021",
        "DEP-022"
      ],
      "cross_family_inputs": [],
      "cross_family_outputs": [
        "DEP-023"
      ],
      "unresolved_seams": [
        "none beyond preserved R1B/R1C boundaries"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-03",
      "afqr_id": "AFQR-03",
      "owned_concerns": "action representation; action-route composition; registered-route capability requirements; directly supported affordance/method selection; bounded plans",
      "explicit_nonowned_concerns": "command lifecycle; readiness determinations; opportunity; targeting; action resolution",
      "r1b_terms_or_qualified_forms": [
        {
          "term_id": "TERM-008",
          "form": "action",
          "owner": "AFQR-03"
        },
        {
          "term_id": "TERM-009",
          "form": "action-route capability requirement",
          "owner": "AFQR-03"
        }
      ],
      "source_evidence_identifiers": [
        "SRC-0006"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md"
      ],
      "internal_family_inputs": [
        "DEP-002",
        "DEP-020",
        "DEP-032"
      ],
      "internal_family_outputs": [],
      "cross_family_inputs": [],
      "cross_family_outputs": [],
      "unresolved_seams": [
        "governed R1D-WORLD boundary: action-route capability requirement remains AFQR-03; capability readiness determination remains AFQR-19; neither owns unqualified capability"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-04",
      "afqr_id": "AFQR-04",
      "owned_concerns": "logical time; causal ordering; simultaneity; scheduling; deterministic resolution groups; bounded cascades",
      "explicit_nonowned_concerns": "truth; command identity; dependency; domain ownership; universal rounds, turns, initiative, phases, or ticks",
      "r1b_terms_or_qualified_forms": [
        {
          "term_id": "TERM-005",
          "form": "scheduled effect",
          "owner": "AFQR-04"
        },
        {
          "term_id": "TERM-012",
          "form": "resolution group",
          "owner": "AFQR-04"
        },
        {
          "term_id": "TERM-027",
          "form": "time",
          "owner": "AFQR-04"
        },
        {
          "term_id": "TERM-028",
          "form": "causality",
          "owner": "AFQR-04"
        }
      ],
      "source_evidence_identifiers": [
        "SRC-0007"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md"
      ],
      "internal_family_inputs": [
        "DEP-003",
        "DEP-021",
        "DEP-063"
      ],
      "internal_family_outputs": [
        "DEP-024",
        "DEP-025",
        "DEP-026",
        "DEP-027",
        "DEP-028"
      ],
      "cross_family_inputs": [],
      "cross_family_outputs": [
        "DEP-029",
        "DEP-030",
        "DEP-031"
      ],
      "unresolved_seams": [
        "none beyond preserved R1B/R1C boundaries"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-05",
      "afqr_id": "AFQR-05",
      "owned_concerns": "registered interfaces; adapters; bridges; hyperedges; typed compatibility",
      "explicit_nonowned_concerns": "endpoint semantics; runtime bridge/hypergraph implementation",
      "r1b_terms_or_qualified_forms": [],
      "source_evidence_identifiers": [
        "SRC-0008"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md"
      ],
      "internal_family_inputs": [
        "DEP-004"
      ],
      "internal_family_outputs": [
        "DEP-032",
        "DEP-033",
        "DEP-034",
        "DEP-035",
        "DEP-036"
      ],
      "cross_family_inputs": [],
      "cross_family_outputs": [
        "DEP-037",
        "DEP-038",
        "DEP-039",
        "DEP-040",
        "DEP-041",
        "DEP-042",
        "DEP-043",
        "DEP-044",
        "DEP-045",
        "DEP-046"
      ],
      "unresolved_seams": [
        "none beyond preserved R1B/R1C boundaries"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-06",
      "afqr_id": "AFQR-06",
      "owned_concerns": "claims; evidence submission; admissibility; conflicts; arbitration; typed claim results; hidden-evidence boundaries",
      "explicit_nonowned_concerns": "truth; identity; knowledge; institutional authority; committed mutation",
      "r1b_terms_or_qualified_forms": [
        {
          "term_id": "TERM-012",
          "form": "claim arbitration result",
          "owner": "AFQR-06"
        },
        {
          "term_id": "TERM-018",
          "form": "claim",
          "owner": "AFQR-06"
        },
        {
          "term_id": "TERM-019",
          "form": "arbitration evidence",
          "owner": "AFQR-06"
        }
      ],
      "source_evidence_identifiers": [
        "SRC-0009"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
      ],
      "internal_family_inputs": [
        "DEP-005",
        "DEP-025",
        "DEP-033",
        "DEP-052",
        "DEP-064"
      ],
      "internal_family_outputs": [
        "DEP-047",
        "DEP-048",
        "DEP-049"
      ],
      "cross_family_inputs": [],
      "cross_family_outputs": [
        "DEP-050",
        "DEP-051"
      ],
      "unresolved_seams": [
        "none beyond preserved R1B/R1C boundaries"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-07",
      "afqr_id": "AFQR-07",
      "owned_concerns": "conserved quantities; sources/sinks; transformations; reservation; settlement; losses; byproducts; validity; arbitrage prevention",
      "explicit_nonowned_concerns": "a universal resource economy, unit, currency, energy, inventory, or progression model; runtime ledgers",
      "r1b_terms_or_qualified_forms": [],
      "source_evidence_identifiers": [
        "SRC-0010"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
      ],
      "internal_family_inputs": [
        "DEP-006",
        "DEP-026",
        "DEP-034",
        "DEP-047",
        "DEP-053",
        "DEP-065"
      ],
      "internal_family_outputs": [],
      "cross_family_inputs": [],
      "cross_family_outputs": [],
      "unresolved_seams": [
        "none beyond preserved R1B/R1C boundaries"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-08",
      "afqr_id": "AFQR-08",
      "owned_concerns": "identity; continuity; copying; transformation; proxyhood; reinstantiation; fusion; fission; contextual equivalence",
      "explicit_nonowned_concerns": "ownership; agency; control; authority; responsibility; personhood; legal standing",
      "r1b_terms_or_qualified_forms": [
        {
          "term_id": "TERM-013",
          "form": "identity",
          "owner": "AFQR-08"
        }
      ],
      "source_evidence_identifiers": [
        "SRC-0011"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md"
      ],
      "internal_family_inputs": [
        "DEP-007",
        "DEP-027",
        "DEP-035",
        "DEP-048",
        "DEP-066"
      ],
      "internal_family_outputs": [
        "DEP-052",
        "DEP-053",
        "DEP-054"
      ],
      "cross_family_inputs": [],
      "cross_family_outputs": [
        "DEP-055",
        "DEP-056",
        "DEP-057",
        "DEP-058",
        "DEP-059",
        "DEP-060"
      ],
      "unresolved_seams": [
        "COLL-03: AFQR-01 qualified state/write-owner semantics and AFQR-08 identity semantics establish neither substantive ownership, authority, agency, nor responsibility"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    },
    {
      "record_id": "CORE-RESP-09",
      "afqr_id": "AFQR-09",
      "owned_concerns": "governed relations; dependencies; revocation; inheritance; termination; migration; orphaning; cascading consequences",
      "explicit_nonowned_concerns": "automatic obligation, jurisdiction, ownership, authority, social standing, or legal effect; runtime relation registry",
      "r1b_terms_or_qualified_forms": [
        {
          "term_id": "TERM-015",
          "form": "governed-relation authority record",
          "owner": "AFQR-09"
        },
        {
          "term_id": "TERM-023",
          "form": "relation",
          "owner": "AFQR-09"
        },
        {
          "term_id": "TERM-024",
          "form": "dependency",
          "owner": "AFQR-09"
        },
        {
          "term_id": "TERM-025",
          "form": "obligation",
          "owner": "AFQR-09"
        }
      ],
      "source_evidence_identifiers": [
        "SRC-0012"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
      ],
      "internal_family_inputs": [
        "DEP-008",
        "DEP-022",
        "DEP-028",
        "DEP-036",
        "DEP-049",
        "DEP-054"
      ],
      "internal_family_outputs": [
        "DEP-061",
        "DEP-062",
        "DEP-063",
        "DEP-064",
        "DEP-065",
        "DEP-066"
      ],
      "cross_family_inputs": [],
      "cross_family_outputs": [
        "DEP-067",
        "DEP-068",
        "DEP-069",
        "DEP-070",
        "DEP-071"
      ],
      "unresolved_seams": [
        "COLL-08: governed relation/dependency lifecycle does not create jurisdiction, institutional legitimacy, authority, or social state"
      ],
      "later_implementation_handoff": "future owner contract after R1E and later explicit authorization; no schema, service, persistence, or runtime work here"
    }
  ],
  "internal_edge_dispositions": [
    {
      "disposition_id": "CORE-INT-DEP-001",
      "edge_id": "DEP-001",
      "producer": "AFQR-01",
      "consumer": "AFQR-02",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-001; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0005"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-002",
      "edge_id": "DEP-002",
      "producer": "AFQR-01",
      "consumer": "AFQR-03",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-002; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0006"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-003",
      "edge_id": "DEP-003",
      "producer": "AFQR-01",
      "consumer": "AFQR-04",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-003; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0007"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-004",
      "edge_id": "DEP-004",
      "producer": "AFQR-01",
      "consumer": "AFQR-05",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-004; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0008"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-005",
      "edge_id": "DEP-005",
      "producer": "AFQR-01",
      "consumer": "AFQR-06",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-005; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0009"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-006",
      "edge_id": "DEP-006",
      "producer": "AFQR-01",
      "consumer": "AFQR-07",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-006; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0010"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-007",
      "edge_id": "DEP-007",
      "producer": "AFQR-01",
      "consumer": "AFQR-08",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-007; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0011"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-008",
      "edge_id": "DEP-008",
      "producer": "AFQR-01",
      "consumer": "AFQR-09",
      "handoff_kind": "commit",
      "semantic_owner": {
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
      "producer_output": "Bounded commit output identified by DEP-008; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0012"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-020",
      "edge_id": "DEP-020",
      "producer": "AFQR-02",
      "consumer": "AFQR-03",
      "handoff_kind": "command_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded command_lifecycle output identified by DEP-020; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0005",
          "SRC-0006"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-021",
      "edge_id": "DEP-021",
      "producer": "AFQR-02",
      "consumer": "AFQR-04",
      "handoff_kind": "command_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded command_lifecycle output identified by DEP-021; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0005",
          "SRC-0007"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-022",
      "edge_id": "DEP-022",
      "producer": "AFQR-02",
      "consumer": "AFQR-09",
      "handoff_kind": "command_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded command_lifecycle output identified by DEP-022; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0005",
          "SRC-0012"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-024",
      "edge_id": "DEP-024",
      "producer": "AFQR-04",
      "consumer": "AFQR-02",
      "handoff_kind": "time_causality",
      "semantic_owner": {
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
      "producer_output": "Bounded time_causality output identified by DEP-024; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0005"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-025",
      "edge_id": "DEP-025",
      "producer": "AFQR-04",
      "consumer": "AFQR-06",
      "handoff_kind": "time_causality",
      "semantic_owner": {
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
      "producer_output": "Bounded time_causality output identified by DEP-025; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0009"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-026",
      "edge_id": "DEP-026",
      "producer": "AFQR-04",
      "consumer": "AFQR-07",
      "handoff_kind": "time_causality",
      "semantic_owner": {
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
      "producer_output": "Bounded time_causality output identified by DEP-026; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0010"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-027",
      "edge_id": "DEP-027",
      "producer": "AFQR-04",
      "consumer": "AFQR-08",
      "handoff_kind": "time_causality",
      "semantic_owner": {
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
      "producer_output": "Bounded time_causality output identified by DEP-027; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0011"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-028",
      "edge_id": "DEP-028",
      "producer": "AFQR-04",
      "consumer": "AFQR-09",
      "handoff_kind": "time_causality",
      "semantic_owner": {
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
      "producer_output": "Bounded time_causality output identified by DEP-028; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0012"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-032",
      "edge_id": "DEP-032",
      "producer": "AFQR-05",
      "consumer": "AFQR-03",
      "handoff_kind": "interface_bridge",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "producer_output": "Bounded interface_bridge output identified by DEP-032; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0006"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-03/ARCH-01/adrs/AFQR-03_Action_Representation_Capability_Affordance_Method_Selection_and_Bounded_Plans.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-033",
      "edge_id": "DEP-033",
      "producer": "AFQR-05",
      "consumer": "AFQR-06",
      "handoff_kind": "interface_bridge",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "producer_output": "Bounded interface_bridge output identified by DEP-033; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0009"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-034",
      "edge_id": "DEP-034",
      "producer": "AFQR-05",
      "consumer": "AFQR-07",
      "handoff_kind": "interface_bridge",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "producer_output": "Bounded interface_bridge output identified by DEP-034; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0010"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-035",
      "edge_id": "DEP-035",
      "producer": "AFQR-05",
      "consumer": "AFQR-08",
      "handoff_kind": "interface_bridge",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "producer_output": "Bounded interface_bridge output identified by DEP-035; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0011"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-036",
      "edge_id": "DEP-036",
      "producer": "AFQR-05",
      "consumer": "AFQR-09",
      "handoff_kind": "interface_bridge",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "producer_output": "Bounded interface_bridge output identified by DEP-036; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0012"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-047",
      "edge_id": "DEP-047",
      "producer": "AFQR-06",
      "consumer": "AFQR-07",
      "handoff_kind": "claim_evidence",
      "semantic_owner": {
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
      "producer_output": "Bounded claim_evidence output identified by DEP-047; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0009",
          "SRC-0010"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-048",
      "edge_id": "DEP-048",
      "producer": "AFQR-06",
      "consumer": "AFQR-08",
      "handoff_kind": "claim_evidence",
      "semantic_owner": {
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
      "producer_output": "Bounded claim_evidence output identified by DEP-048; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0009",
          "SRC-0011"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-049",
      "edge_id": "DEP-049",
      "producer": "AFQR-06",
      "consumer": "AFQR-09",
      "handoff_kind": "claim_evidence",
      "semantic_owner": {
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
      "producer_output": "Bounded claim_evidence output identified by DEP-049; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0009",
          "SRC-0012"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-052",
      "edge_id": "DEP-052",
      "producer": "AFQR-08",
      "consumer": "AFQR-06",
      "handoff_kind": "identity_evidence",
      "semantic_owner": {
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
      "producer_output": "Bounded identity_evidence output identified by DEP-052; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0009"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-053",
      "edge_id": "DEP-053",
      "producer": "AFQR-08",
      "consumer": "AFQR-07",
      "handoff_kind": "identity_evidence",
      "semantic_owner": {
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
      "producer_output": "Bounded identity_evidence output identified by DEP-053; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0010"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-054",
      "edge_id": "DEP-054",
      "producer": "AFQR-08",
      "consumer": "AFQR-09",
      "handoff_kind": "identity_evidence",
      "semantic_owner": {
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
      "producer_output": "Bounded identity_evidence output identified by DEP-054; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0012"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-061",
      "edge_id": "DEP-061",
      "producer": "AFQR-09",
      "consumer": "AFQR-01",
      "handoff_kind": "relation_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded relation_lifecycle output identified by DEP-061; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0004"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-062",
      "edge_id": "DEP-062",
      "producer": "AFQR-09",
      "consumer": "AFQR-02",
      "handoff_kind": "relation_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded relation_lifecycle output identified by DEP-062; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0005"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-063",
      "edge_id": "DEP-063",
      "producer": "AFQR-09",
      "consumer": "AFQR-04",
      "handoff_kind": "relation_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded relation_lifecycle output identified by DEP-063; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0007"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-064",
      "edge_id": "DEP-064",
      "producer": "AFQR-09",
      "consumer": "AFQR-06",
      "handoff_kind": "relation_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded relation_lifecycle output identified by DEP-064; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0009"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-065",
      "edge_id": "DEP-065",
      "producer": "AFQR-09",
      "consumer": "AFQR-07",
      "handoff_kind": "relation_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded relation_lifecycle output identified by DEP-065; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0010"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-07/ARCH-01/adrs/AFQR-07_Cross_Domain_Conservation_Conversion_Validity_Reservation_Settlement_and_Arbitrage_Prevention.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001"
      ],
      "cycle_or_dependency_risk_treatment": false,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    },
    {
      "disposition_id": "CORE-INT-DEP-066",
      "edge_id": "DEP-066",
      "producer": "AFQR-09",
      "consumer": "AFQR-08",
      "handoff_kind": "relation_lifecycle",
      "semantic_owner": {
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
      "producer_output": "Bounded relation_lifecycle output identified by DEP-066; scope remains limited to the producing AFQR source contract.",
      "permitted_consumer_use": "May consume the handoff as typed input only after declared preconditions; consumption grants no ownership of the producer domain.",
      "ownership_nontransfer": true,
      "ordering_or_phase_constraint": [
        "producer source contract exists",
        "consumer accepts bounded handoff",
        "R1B qualified vocabulary is used where applicable"
      ],
      "failure_or_unavailable_input_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0011"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md"
        ]
      },
      "relevant_invariant_ids": [
        "INV-001",
        "INV-005"
      ],
      "cycle_or_dependency_risk_treatment": true,
      "downstream_implementation_status": "unimplemented and unauthorized; doctrine handoff only",
      "r1b_semantic_binding": {
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
      }
    }
  ],
  "boundary_dispositions": [
    {
      "disposition_id": "CORE-BND-DEP-009",
      "r1c_edge_ids_covered": [
        "DEP-009"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-10",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-009; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-10 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0022"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-10",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-009; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-010",
      "r1c_edge_ids_covered": [
        "DEP-010"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-11",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-010; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-11 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0041"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-11",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-010; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-011",
      "r1c_edge_ids_covered": [
        "DEP-011"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-12",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-011; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-12 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0072"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-12",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-011; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-012",
      "r1c_edge_ids_covered": [
        "DEP-012"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-13",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-012; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-13 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0082"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-13",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-012; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-013",
      "r1c_edge_ids_covered": [
        "DEP-013"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-14",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-013; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-14 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0103"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-14",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-013; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-014",
      "r1c_edge_ids_covered": [
        "DEP-014"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-15",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-014; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-15 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0125"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-15",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-014; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-015",
      "r1c_edge_ids_covered": [
        "DEP-015"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-16",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-015; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-16 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0152"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-16",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-015; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-016",
      "r1c_edge_ids_covered": [
        "DEP-016"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-17",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-016; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-17 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0180"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-17",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-016; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-017",
      "r1c_edge_ids_covered": [
        "DEP-017"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-18",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-017; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-18 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0207"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-18",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-017; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-018",
      "r1c_edge_ids_covered": [
        "DEP-018"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-19",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-018; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-19 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0231"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-19",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-018; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-019",
      "r1c_edge_ids_covered": [
        "DEP-019"
      ],
      "core_family_endpoint": "AFQR-01",
      "external_endpoint": "AFQR-20",
      "direction": "export",
      "typed_handoff": "Bounded commit output identified by DEP-019; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-20 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0004",
          "SRC-0255"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-01",
      "consumer": "AFQR-20",
      "handoff_kind": "commit",
      "typed_producer_output": "Bounded commit output identified by DEP-019; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-023",
      "r1c_edge_ids_covered": [
        "DEP-023"
      ],
      "core_family_endpoint": "AFQR-02",
      "external_endpoint": "AFQR-19",
      "direction": "export",
      "typed_handoff": "Bounded command_lifecycle output identified by DEP-023; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-19 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0005",
          "SRC-0231"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-02/ARCH-01/adrs/AFQR-02_Command_Identity_Attempts_Retries_Suspension_Escalation_and_Durable_Progress.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-02",
      "consumer": "AFQR-19",
      "handoff_kind": "command_lifecycle",
      "typed_producer_output": "Bounded command_lifecycle output identified by DEP-023; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-029",
      "r1c_edge_ids_covered": [
        "DEP-029"
      ],
      "core_family_endpoint": "AFQR-04",
      "external_endpoint": "AFQR-18",
      "direction": "export",
      "typed_handoff": "Bounded time_causality output identified by DEP-029; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-18 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0207"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-04",
      "consumer": "AFQR-18",
      "handoff_kind": "time_causality",
      "typed_producer_output": "Bounded time_causality output identified by DEP-029; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-030",
      "r1c_edge_ids_covered": [
        "DEP-030"
      ],
      "core_family_endpoint": "AFQR-04",
      "external_endpoint": "AFQR-19",
      "direction": "export",
      "typed_handoff": "Bounded time_causality output identified by DEP-030; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-19 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0231"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-04",
      "consumer": "AFQR-19",
      "handoff_kind": "time_causality",
      "typed_producer_output": "Bounded time_causality output identified by DEP-030; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-031",
      "r1c_edge_ids_covered": [
        "DEP-031"
      ],
      "core_family_endpoint": "AFQR-04",
      "external_endpoint": "AFQR-20",
      "direction": "export",
      "typed_handoff": "Bounded time_causality output identified by DEP-031; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-20 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0007",
          "SRC-0255"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-04/ARCH-01/adrs/AFQR-04_Logical_Time_Simultaneity_Causal_Ordering_Scheduled_Effects_and_Bounded_Cascades.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-04",
      "consumer": "AFQR-20",
      "handoff_kind": "time_causality",
      "typed_producer_output": "Bounded time_causality output identified by DEP-031; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-037",
      "r1c_edge_ids_covered": [
        "DEP-037"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-10",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-037; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-10 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0022"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-10",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-037; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-038",
      "r1c_edge_ids_covered": [
        "DEP-038"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-11",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-038; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-11 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0041"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-11",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-038; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-039",
      "r1c_edge_ids_covered": [
        "DEP-039"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-13",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-039; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-13 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0082"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-13",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-039; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-040",
      "r1c_edge_ids_covered": [
        "DEP-040"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-14",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-040; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-14 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0103"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-14/ARCH-06/adrs/AFQR-14_Communication_Interpretation_Dialogue_Protocols.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-14",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-040; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-041",
      "r1c_edge_ids_covered": [
        "DEP-041"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-15",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-041; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-15 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0125"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-15",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-041; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-042",
      "r1c_edge_ids_covered": [
        "DEP-042"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-16",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-042; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-16 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0152"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-16",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-042; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-043",
      "r1c_edge_ids_covered": [
        "DEP-043"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-17",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-043; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-17 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0180"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-17",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-043; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-044",
      "r1c_edge_ids_covered": [
        "DEP-044"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-18",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-044; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-18 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0207"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-18/ARCH-10/adrs/AFQR-18_Spatiotemporal_Topology.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-18",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-044; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-045",
      "r1c_edge_ids_covered": [
        "DEP-045"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-19",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-045; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-19 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0231"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-19/ARCH-11/adrs/AFQR-19_Capability_Targeting_Reaction_Resolution.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-19",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-045; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-046",
      "r1c_edge_ids_covered": [
        "DEP-046"
      ],
      "core_family_endpoint": "AFQR-05",
      "external_endpoint": "AFQR-20",
      "direction": "export",
      "typed_handoff": "Bounded interface_bridge output identified by DEP-046; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
        "owner_kind": "afqr",
        "owner_id": "AFQR-05",
        "r1b_terms": [],
        "r1b_term_bindings": [],
        "ownership_basis": "direct_source_contract_not_producer_status"
      },
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-20 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0008",
          "SRC-0255"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-20/ARCH-12/adrs/AFQR-20_Signal_Sensing_Detection_Tracking.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-05",
      "consumer": "AFQR-20",
      "handoff_kind": "interface_bridge",
      "typed_producer_output": "Bounded interface_bridge output identified by DEP-046; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-050",
      "r1c_edge_ids_covered": [
        "DEP-050"
      ],
      "core_family_endpoint": "AFQR-06",
      "external_endpoint": "AFQR-10",
      "direction": "export",
      "typed_handoff": "Bounded claim_evidence output identified by DEP-050; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-10 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0009",
          "SRC-0022"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-06",
      "consumer": "AFQR-10",
      "handoff_kind": "claim_evidence",
      "typed_producer_output": "Bounded claim_evidence output identified by DEP-050; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-051",
      "r1c_edge_ids_covered": [
        "DEP-051"
      ],
      "core_family_endpoint": "AFQR-06",
      "external_endpoint": "AFQR-15",
      "direction": "export",
      "typed_handoff": "Bounded claim_evidence output identified by DEP-051; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-15 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0009",
          "SRC-0125"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-06/ARCH-01/adrs/AFQR-06_Claim_Discovery_Admissibility_Conflict_Arbitration_Choice_and_Hidden_Evidence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-06",
      "consumer": "AFQR-15",
      "handoff_kind": "claim_evidence",
      "typed_producer_output": "Bounded claim_evidence output identified by DEP-051; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-055",
      "r1c_edge_ids_covered": [
        "DEP-055"
      ],
      "core_family_endpoint": "AFQR-08",
      "external_endpoint": "AFQR-10",
      "direction": "export",
      "typed_handoff": "Bounded identity_evidence output identified by DEP-055; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-10 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0022"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-10/ARCH-02/adrs/AFQR-10_Epistemic_State_Observer_Relative_Truth.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-08",
      "consumer": "AFQR-10",
      "handoff_kind": "identity_evidence",
      "typed_producer_output": "Bounded identity_evidence output identified by DEP-055; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-056",
      "r1c_edge_ids_covered": [
        "DEP-056"
      ],
      "core_family_endpoint": "AFQR-08",
      "external_endpoint": "AFQR-11",
      "direction": "export",
      "typed_handoff": "Bounded identity_evidence output identified by DEP-056; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-11 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0041"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-08",
      "consumer": "AFQR-11",
      "handoff_kind": "identity_evidence",
      "typed_producer_output": "Bounded identity_evidence output identified by DEP-056; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-057",
      "r1c_edge_ids_covered": [
        "DEP-057"
      ],
      "core_family_endpoint": "AFQR-08",
      "external_endpoint": "AFQR-12",
      "direction": "export",
      "typed_handoff": "Bounded identity_evidence output identified by DEP-057; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-12 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0072"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-08",
      "consumer": "AFQR-12",
      "handoff_kind": "identity_evidence",
      "typed_producer_output": "Bounded identity_evidence output identified by DEP-057; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-058",
      "r1c_edge_ids_covered": [
        "DEP-058"
      ],
      "core_family_endpoint": "AFQR-08",
      "external_endpoint": "AFQR-13",
      "direction": "export",
      "typed_handoff": "Bounded identity_evidence output identified by DEP-058; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-13 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0082"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-08",
      "consumer": "AFQR-13",
      "handoff_kind": "identity_evidence",
      "typed_producer_output": "Bounded identity_evidence output identified by DEP-058; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-059",
      "r1c_edge_ids_covered": [
        "DEP-059"
      ],
      "core_family_endpoint": "AFQR-08",
      "external_endpoint": "AFQR-15",
      "direction": "export",
      "typed_handoff": "Bounded identity_evidence output identified by DEP-059; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-15 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0125"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-08",
      "consumer": "AFQR-15",
      "handoff_kind": "identity_evidence",
      "typed_producer_output": "Bounded identity_evidence output identified by DEP-059; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-060",
      "r1c_edge_ids_covered": [
        "DEP-060"
      ],
      "core_family_endpoint": "AFQR-08",
      "external_endpoint": "AFQR-16",
      "direction": "export",
      "typed_handoff": "Bounded identity_evidence output identified by DEP-060; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-16 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0011",
          "SRC-0152"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-08",
      "consumer": "AFQR-16",
      "handoff_kind": "identity_evidence",
      "typed_producer_output": "Bounded identity_evidence output identified by DEP-060; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-067",
      "r1c_edge_ids_covered": [
        "DEP-067"
      ],
      "core_family_endpoint": "AFQR-09",
      "external_endpoint": "AFQR-11",
      "direction": "export",
      "typed_handoff": "Bounded relation_lifecycle output identified by DEP-067; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-11 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0041"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-09",
      "consumer": "AFQR-11",
      "handoff_kind": "relation_lifecycle",
      "typed_producer_output": "Bounded relation_lifecycle output identified by DEP-067; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-068",
      "r1c_edge_ids_covered": [
        "DEP-068"
      ],
      "core_family_endpoint": "AFQR-09",
      "external_endpoint": "AFQR-13",
      "direction": "export",
      "typed_handoff": "Bounded relation_lifecycle output identified by DEP-068; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-13 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0082"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-09",
      "consumer": "AFQR-13",
      "handoff_kind": "relation_lifecycle",
      "typed_producer_output": "Bounded relation_lifecycle output identified by DEP-068; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-069",
      "r1c_edge_ids_covered": [
        "DEP-069"
      ],
      "core_family_endpoint": "AFQR-09",
      "external_endpoint": "AFQR-15",
      "direction": "export",
      "typed_handoff": "Bounded relation_lifecycle output identified by DEP-069; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-AGENCY owns AFQR-15 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0125"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-09",
      "consumer": "AFQR-15",
      "handoff_kind": "relation_lifecycle",
      "typed_producer_output": "Bounded relation_lifecycle output identified by DEP-069; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-AGENCY"
    },
    {
      "disposition_id": "CORE-BND-DEP-070",
      "r1c_edge_ids_covered": [
        "DEP-070"
      ],
      "core_family_endpoint": "AFQR-09",
      "external_endpoint": "AFQR-16",
      "direction": "export",
      "typed_handoff": "Bounded relation_lifecycle output identified by DEP-070; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-16 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0152"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-16/ARCH-08/adrs/AFQR-16_Embodiment_Integrity_Harm_Recovery.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-09",
      "consumer": "AFQR-16",
      "handoff_kind": "relation_lifecycle",
      "typed_producer_output": "Bounded relation_lifecycle output identified by DEP-070; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    },
    {
      "disposition_id": "CORE-BND-DEP-071",
      "r1c_edge_ids_covered": [
        "DEP-071"
      ],
      "core_family_endpoint": "AFQR-09",
      "external_endpoint": "AFQR-17",
      "direction": "export",
      "typed_handoff": "Bounded relation_lifecycle output identified by DEP-071; scope remains limited to the producing AFQR source contract.",
      "semantic_owner": {
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
      "r1d_core_may_assert": "only the core endpoint output and R1C handoff constraints",
      "external_family_owns": "R1D-WORLD owns AFQR-17 internal semantics; this record does not define them",
      "ownership_nontransfer": true,
      "unresolved_escalation": "none unless separately listed in escalation records",
      "source_evidence": {
        "identifiers": [
          "SRC-0012",
          "SRC-0180"
        ],
        "paths": [
          "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
          "working/afqr_consolidation_inputs/extracted/AFQR-17/ARCH-09/adrs/AFQR-17_Environment_Processes_Hazards_Ecology.md"
        ]
      },
      "failure_behavior": "defer_or_escalate_without_fabricating_truth_or_owner",
      "producer": "AFQR-09",
      "consumer": "AFQR-17",
      "handoff_kind": "relation_lifecycle",
      "typed_producer_output": "Bounded relation_lifecycle output identified by DEP-071; scope remains limited to the producing AFQR source contract.",
      "external_family": "R1D-WORLD"
    }
  ],
  "cycle_resolutions": [
    {
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
    {
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
    {
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
    }
  ],
  "dependency_risk_reclassifications": [
    {
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
    {
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
    {
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
    {
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
    }
  ],
  "missing_substrates": [
    {
      "substrate_id": "SUB-001",
      "name": "generalized governed-relation registry",
      "core_family_scope": "AFQR-09 governed-relation and dependency lifecycle",
      "external_family_scope": "AFQR-13 social state and AFQR-15 jurisdiction/institution/authority",
      "r1d_core_may_consolidate": "relation lifecycle, revocation, migration, orphaning, cascade boundaries, and reachability non-equivalence",
      "r1d_core_must_not_implement": "schemas, fields, graph registry, persistence, APIs, or inference of obligation/jurisdiction",
      "later_owner_or_gate": "R1D-AGENCY, then R1E and a later explicit implementation gate",
      "collapse_risk": "Omission collapses dependency into obligation, reachability into jurisdiction, or relation records into institutional authority/social standing.",
      "source_evidence_identifiers": [
        "SRC-0012",
        "SRC-0082",
        "SRC-0125"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
      ],
      "status": "classified_unimplemented"
    },
    {
      "substrate_id": "SUB-002",
      "name": "generalized bitemporal truth/evidence store",
      "core_family_scope": "AFQR-04 logical ordering and AFQR-06 claim/evidence provenance, admissibility history, and non-overwrite constraints",
      "external_family_scope": "AFQR-10 epistemic truth and AFQR-20 sensing",
      "r1d_core_may_consolidate": "core-side ordering, provenance, admissibility history, and non-overwrite doctrine",
      "r1d_core_must_not_implement": "truth store, evidence database, sensing service, schemas, fields, persistence, or APIs",
      "later_owner_or_gate": "R1D-AGENCY and R1D-WORLD, then R1E and a later explicit implementation gate",
      "collapse_risk": "Omission permits hidden-truth leakage, retroactive evidence overwrite, or logical time to manufacture truth/admissibility.",
      "source_evidence_identifiers": [
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
      "status": "classified_unimplemented"
    },
    {
      "substrate_id": "SUB-003",
      "name": "generalized owner-reducer transaction journal",
      "core_family_scope": "AFQR-01, AFQR-02, AFQR-04, and AFQR-09 transition, command lifecycle, logical order, and dependency-consequence doctrine only",
      "external_family_scope": "none inside R1D-AGENCY/WORLD; later implementation ownership remains undecided",
      "r1d_core_may_consolidate": "commitment, recovery, replay, command identity, causal ordering, and dependency-consequence doctrine",
      "r1d_core_must_not_implement": "journal schemas, fields, reducers, databases, persistence, APIs, or runtime services",
      "later_owner_or_gate": "R1E and a later explicit implementation gate",
      "collapse_risk": "Omission allows replay to duplicate commitment, recovery to rewrite command identity, or causal/dependency consequences to recurse without bounds.",
      "source_evidence_identifiers": [
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
      "status": "classified_unimplemented"
    },
    {
      "substrate_id": "SUB-004",
      "name": "registered interface/bridge hypergraph",
      "core_family_scope": "AFQR-05 registered-interface, bridge, hyperedge, typed-compatibility, and endpoint-nontransfer doctrine only",
      "external_family_scope": "typed external endpoints retain their R1D-AGENCY or R1D-WORLD semantics",
      "r1d_core_may_consolidate": "typed compatibility and semantic nontransfer boundaries",
      "r1d_core_must_not_implement": "registry schema, bridge code, adapters, runtime hypergraph, persistence, or APIs",
      "later_owner_or_gate": "R1E and a later explicit implementation gate",
      "collapse_risk": "Omission encourages pairwise ad hoc adapters, package-symbol ownership inference, and donor-specific compatibility becoming Astra law.",
      "source_evidence_identifiers": [
        "SRC-0008"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-05/ARCH-01/adrs/AFQR-05_Cross_System_Interfaces_Adapters_Bridges_Hyperedges_and_Compatibility.md"
      ],
      "status": "classified_unimplemented"
    }
  ],
  "escalations": [
    {
      "record_id": "CORE-ESC-COLL-03",
      "collision_identifier": "COLL-03",
      "exact_collision_terms": [
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
      "core_family_afqrs": [
        "AFQR-01",
        "AFQR-08"
      ],
      "external_family_afqrs": [
        "AFQR-11",
        "AFQR-15"
      ],
      "core_family_seam": "AFQR-01 owns qualified state/write-owner semantics only; AFQR-08 owns identity and continuity only; neither state ownership nor identity establishes substantive ownership, authority, agency, consent, control, or responsibility.",
      "prohibited_inference": "No inference of agency, consent, responsibility, jurisdiction, ownership, or authority from adjacent terms.",
      "safe_interim_usage": "Use accepted qualified forms and explicit AFQR owner scopes only.",
      "source_evidence_identifiers": [
        "SRC-0004",
        "SRC-0011",
        "SRC-0059",
        "SRC-0157"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-01/ARCH-01/adrs/AFQR-01_Atomic_State_Transition_Ownership_Commitment_Recovery_and_Replay.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-08/ARCH-01/adrs/AFQR-08_Identity_Continuity_Copying_Transformation_Proxyhood_Reinstantiation_Fusion_Fission_and_Contextual_Equivalence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
      ],
      "downstream_family": "R1D-AGENCY",
      "blocked_gates": [
        "R1E",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
        "RT-002G"
      ],
      "ledger_escalation_id": "R1B-ESC-001"
    },
    {
      "record_id": "CORE-ESC-COLL-08",
      "collision_identifier": "COLL-08",
      "exact_collision_terms": [
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
      "core_family_afqrs": [
        "AFQR-09"
      ],
      "external_family_afqrs": [
        "AFQR-13",
        "AFQR-15"
      ],
      "core_family_seam": "AFQR-09 owns governed relation and dependency lifecycle; a relation or dependency does not itself create jurisdiction, institutional legitimacy, authority, or social state. Obligation remains distinct: an accepted qualified obligation form does not make relation existence automatically generate obligation or legal effect.",
      "prohibited_inference": "No inference of agency, consent, responsibility, jurisdiction, ownership, or authority from adjacent terms.",
      "safe_interim_usage": "Use accepted qualified forms and explicit AFQR owner scopes only.",
      "source_evidence_identifiers": [
        "SRC-0012",
        "SRC-0110",
        "SRC-0157"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-09/ARCH-01/adrs/AFQR-09_Dependency_Revocation_Inheritance_Termination_Migration_Orphaning_and_Cascading_Consequence.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-15/ARCH-07/adrs/AFQR-15_Institutions_Governance_Law_Adjudication.md"
      ],
      "downstream_family": "R1D-AGENCY",
      "blocked_gates": [
        "R1E",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
        "RT-002G"
      ],
      "ledger_escalation_id": "R1B-ESC-002"
    },
    {
      "record_id": "CORE-ESC-COLL-10",
      "collision_identifier": "COLL-10",
      "exact_collision_terms": [
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
      "core_family_afqrs": [
        "AFQR-06",
        "AFQR-08",
        "AFQR-09"
      ],
      "external_family_afqrs": [
        "AFQR-11",
        "AFQR-12",
        "AFQR-13"
      ],
      "core_family_seam": "Primarily external to R1D-CORE: AFQR-06 claim or evidence results do not author motivation or behavior; AFQR-08 identity records do not author agency or responsibility; AFQR-09 governed relations do not author behavior, agency, responsibility, or social state; core-family outputs may be consumed as bounded evidence or references only.",
      "prohibited_inference": "No inference of agency, consent, responsibility, jurisdiction, ownership, or authority from adjacent terms.",
      "safe_interim_usage": "Use accepted qualified forms and explicit AFQR owner scopes only.",
      "source_evidence_identifiers": [
        "SRC-0059",
        "SRC-0092",
        "SRC-0110"
      ],
      "source_paths": [
        "working/afqr_consolidation_inputs/extracted/AFQR-11/ARCH-03/adrs/AFQR-11_Agency_Personhood_Consent_Control_Responsibility.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-12/ARCH-04/master/Astra_AFQR_12_Master_Ratification_v1_0.md",
        "working/afqr_consolidation_inputs/extracted/AFQR-13/ARCH-05/adrs/AFQR-13_Social_Relations_Trust_Reputation_Culture.md"
      ],
      "downstream_family": "R1D-AGENCY",
      "blocked_gates": [
        "R1E",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
        "RT-002G"
      ],
      "ledger_escalation_id": "R1B-ESC-003"
    }
  ],
  "corpus_pressure_records": [
    {
      "record_id": "PRESS-01",
      "pressure_class": "class and archetype actions",
      "disposition": "AFQR-03 action representation; source-local cadence",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-02",
      "pressure_class": "point-buy action construction",
      "disposition": "AFQR-03 bounded route composition; readiness to AFQR-19",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-03",
      "pressure_class": "narrative moves and aspects",
      "disposition": "source-local retention; claims may hand to AFQR-06",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-04",
      "pressure_class": "cultivation techniques and advancement transactions",
      "disposition": "AFQR-01 transition and AFQR-07 conservation only when source declares them; advancement external/source-local",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-05",
      "pressure_class": "spells, powers, maneuvers, and procedures",
      "disposition": "AFQR-03 representation; opportunity/resolution to AFQR-19",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-06",
      "pressure_class": "cyberware and biotech transformations",
      "disposition": "AFQR-08 identity continuity; body effects to AFQR-16",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-07",
      "pressure_class": "psionic identity and proxy constructs",
      "disposition": "AFQR-08 identity/proxy; agency and responsibility to AFQR-11",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-08",
      "pressure_class": "horror evidence and hidden-information systems",
      "disposition": "AFQR-06 evidence boundary; truth/knowledge to AFQR-10 and sensing to AFQR-20",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-09",
      "pressure_class": "vehicles, mechs, ships, and operator separation",
      "disposition": "AFQR-08 identity/proxy; control and agency to AFQR-11; bodies/platforms external",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-10",
      "pressure_class": "companions, summons, copies, and proxies",
      "disposition": "AFQR-08 continuity; agency/social semantics external",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-11",
      "pressure_class": "crafting, salvage, requisition, and settlement",
      "disposition": "AFQR-07 reservation/settlement; procedures and institutional authority source-local/external",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-12",
      "pressure_class": "currencies, charges, fuel, ammunition, heat, stress, and abstract reserves",
      "disposition": "AFQR-07 only under separately declared conservation profiles; otherwise source-local",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-13",
      "pressure_class": "clocks, turns, rounds, phases, real time, downtime, and asynchronous processes",
      "disposition": "AFQR-04 can profile logical ordering; every cadence remains source-local, never universal",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-14",
      "pressure_class": "social or legal obligations attached to relations",
      "disposition": "AFQR-09 relation lifecycle; COLL-08 and AFQR-13/15 handoff; no automatic legal effect",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-15",
      "pressure_class": "identity copying, body replacement, fusion, fission, possession, and reinstantiation",
      "disposition": "AFQR-08 identity continuity; body, agency, responsibility external",
      "universalization": "prohibited"
    },
    {
      "record_id": "PRESS-16",
      "pressure_class": "mission and adventure structures that contain source-local procedures",
      "disposition": "source-local retention; only typed declared handoffs may reach AFQR-01–09",
      "universalization": "prohibited"
    }
  ]
}
```

## 12. Completion boundary

R1D-CORE is complete only as a reviewed doctrine family. Overall R1D remains incomplete; R1D-AGENCY and R1D-WORLD remain ready and unstarted; R1E, R2–R6, and RT-002G remain blocked or unauthorized. Temporary evidence remains present and non-authoritative.
