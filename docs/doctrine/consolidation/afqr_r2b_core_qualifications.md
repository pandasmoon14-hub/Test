# AFQR R2B-CORE Doctrine Qualifications

**Artifact ID:** `AFQR-R2B-CORE-QUALIFICATIONS-001`
**Artifact version:** `0.1.0`
**Package:** `R2B-CORE`
**Workstream:** `PR2-R2B-C`
**Layer:** doctrine qualification
**Authority:** bounded R2B-CORE doctrine qualification upon accepted merge
**Starting baseline:** `0a52db603589168a14f3c50beefbbf28274d0836`

## 1. Purpose and authority boundary

This artifact resolves exactly the two bounded CORE doctrine gaps established by
R2A and authorized for `PR2-R2B-C`.

It does not replace
`docs/doctrine/consolidation/afqr_core_transaction_identity_relation.md`.

It qualifies existing AFQR-01 and AFQR-02 doctrine without merging those owners.

The two authorized modules are:

1. `R2B-CORE-MOD-PREVIEW-PERSISTENCE-PROMOTION`;
2. `R2B-CORE-MOD-CORRECTION-RNG-IDENTITY`.

No other R2B seam is resolved here.

In particular, this artifact does not define:

- branch classes, canonicality, ancestry, fork, archive, or branch-promotion policy;
- correction, compensation, supersession, or retcon taxonomy;
- ruleset/package/override version applicability or effective intervals;
- persistence schemas or storage technology;
- runtime fields or services;
- a universal randomness implementation.

Those concerns remain with their accepted owners or later separately authorized
R2B packages.

## 2. Component-owner preservation

AFQR-01 retains:

- transition commitment;
- qualified state/write ownership;
- recovery;
- replay;
- transition receipts;
- committed-audit preservation.

AFQR-02 retains:

- command identity;
- attempt identity;
- execution identity distinctions;
- retries;
- suspension and escalation;
- durable command progress.

Neither owner absorbs the other.

This artifact creates no:

- CORE super-owner;
- preview owner;
- persistence owner;
- replay owner;
- RNG owner;
- correction owner;
- branch owner.

Storage, serialization, caching, journaling, transmission, replay machinery,
randomness records, and execution identifiers remain representations or
consumers unless another accepted doctrine explicitly grants them semantics.

## 3. R2B-CORE-MOD-PREVIEW-PERSISTENCE-PROMOTION

### 3.1 Central qualification

> Persistence preserves a proposal. Persistence alone confers no commitment,
> authority, canonicality, or branch status. Any promotion requires an explicit
> lawful transition into a separately governed authoritative target.

### 3.2 Normative rules

**CORE-PREVIEW-001 — Retention preserves proposal status.**

An uncommitted preview remains an uncommitted proposal when it is retained.

Retention includes, without limitation:

- persistence;
- caching;
- journaling;
- serialization;
- storage;
- transmission;
- copying;
- checkpointing;
- later retrieval.

None of those operations is a commitment event merely because the proposal
survives longer or becomes durable.

**CORE-PREVIEW-002 — Infrastructure confers no authority.**

A preview store, cache, journal, serializer, transport, index, or persistence
mechanism does not gain commitment, command, canonicality, identity, branch, or
domain semantics merely because it represents a preview.

**CORE-PREVIEW-003 — Saved proposals may remain useful.**

A speculative preview, tactical forecast, planning simulation, what-if
resolution, reservation-bearing preview, or saved-but-never-committed proposal
may be retained for lawful later use without becoming authoritative state.

Retention therefore does not require discarding useful proposal evidence.

**CORE-PREVIEW-004 — Promotion is an explicit transition, not a storage side effect.**

If a retained preview is later used as input toward authoritative state, the
authoritative result requires an explicit lawful transition satisfying the
governance of the target state.

A persistence bit, filename, journal location, cache lifetime, serialization
format, or similar representation change cannot substitute for that transition.

**CORE-PREVIEW-005 — Promotion is not retroactive commitment.**

A later lawful authoritative transition does not rewrite the earlier period in
which the retained preview was only a proposal.

The proposal and the later authoritative result remain distinguishable for
audit and provenance purposes.

**CORE-PREVIEW-006 — Target semantics remain external to this module.**

This module does not define what kinds of authoritative targets exist.

If a later target is classified as a branch, canonical history, alternate
history, simulation result, campaign state, or another continuity construct,
that classification belongs to the applicable separately authorized doctrine.

R2B-CORE establishes only that persistence cannot manufacture that status.

**CORE-PREVIEW-007 — No persistence implementation is mandated.**

This qualification does not require:

- a database;
- snapshot storage;
- a branch store;
- a journal format;
- an object store;
- a cache technology;
- a filesystem representation;
- a production schema.

## 4. R2B-CORE-MOD-CORRECTION-RNG-IDENTITY

### 4.1 Central qualification

> A committed randomness-bearing outcome remains part of the original
> committed audit. Replay or recovery of that execution must not silently
> generate a replacement outcome. If an authorized correction requires new
> resolution, the replacement resolution and its randomness provenance are
> distinguishable from the original while the original audit remains
> preserved.

### 4.2 Normative rules

**CORE-RNG-001 — Committed uncertainty evidence belongs to the original execution.**

Once a randomness-bearing or otherwise uncertainty-resolving outcome is
committed, its resolution evidence remains attributable to the execution that
produced that committed result.

**CORE-RNG-002 — Replay and recovery do not reroll.**

Replay, duplicate delivery handling, recovery, or technical retry of an
already-resolved execution must not silently generate a replacement stochastic
outcome.

They preserve or reconstruct the original committed execution and audit under
existing AFQR-01 and AFQR-02 rules.

**CORE-RNG-003 — New resolution is replacement execution, not historical aliasing.**

If a separately authorized correction requires uncertainty to be resolved
again, that new resolution is distinguishable from the original committed
execution.

This qualification does not decide whether AFQR-02 requires a new command, a
new attempt under an existing command, a descendant command, or another
already-lawful command-lifecycle form. That classification remains governed by
AFQR-02.

**CORE-RNG-004 — Replacement provenance is separately attributable.**

Any newly resolved stochastic result required by an authorized correction must
have provenance attributable to the replacement resolution rather than being
silently substituted into the original execution record.

**CORE-RNG-005 — Original committed audit remains preserved.**

A replacement resolution does not erase, overwrite, or masquerade as the
original committed randomness-bearing outcome.

The original audit remains available as historical committed evidence even
when later doctrine lawfully changes what follows from it.

**CORE-RNG-006 — Technical retry cannot become reroll shopping.**

A delivery retry, replay, crash recovery, duplicate request, process restart,
or equivalent technical event cannot be used to obtain a different random
outcome while claiming continuation of the same historical execution.

**CORE-RNG-007 — Randomness is mechanism-neutral.**

This qualification applies to heterogeneous uncertainty sources including:

- dice;
- cards;
- bags or token draws;
- oracle draws;
- random tables;
- encounter tables;
- pseudo-random generators;
- deterministic source-local procedures that resolve uncertainty from a
  declared basis;
- external randomized mechanisms;
- mixed deterministic and randomized procedures.

The presence of one mechanism does not make that mechanism universal Myravant law.

**CORE-RNG-008 — Deterministic procedures remain deterministic.**

A donor or native procedure that is deterministic does not acquire an RNG,
entropy source, seed, die roll, or random draw merely to satisfy this
qualification.

**CORE-RNG-009 — Mixed procedures preserve attribution.**

Where one execution combines deterministic and stochastic resolution, any
portion newly resolved during an authorized replacement must remain
distinguishable from the corresponding original resolution.

This rule does not define the correction taxonomy or decide which portions a
particular correction is permitted to replace.

**CORE-RNG-010 — No universal RNG implementation is mandated.**

This qualification does not require:

- PRNG seeds;
- dice;
- a particular random-number generator;
- a particular entropy source;
- deck storage;
- shuffle algorithms;
- bag-state representation;
- runtime RNG fields;
- one universal stochastic provenance schema.

It governs identity, commitment, audit, replay, and replacement boundaries.

## 5. Corpus-scale pressure checks

| Pressure | Required R2B-CORE result |
| --- | --- |
| speculative preview saved for later | remains proposal |
| tactical forecast cached | remains proposal |
| planning simulation journaled | remains proposal |
| reservation-bearing preview retained | retention does not commit the preview |
| preview transmitted to another subsystem | transmission confers no authority |
| retained preview later selected for authoritative use | requires explicit lawful transition into target |
| exact replay of committed die result | original outcome preserved |
| crash after committed card draw | recovery does not redraw |
| duplicate delivery after oracle result | no replacement result |
| authorized correction requiring a new draw | distinguishable replacement execution and provenance |
| external randomized mechanism | provenance remains attributable without requiring a universal seed |
| deterministic resolution procedure | no artificial randomness introduced |
| mixed deterministic/random resolution | newly resolved uncertainty cannot masquerade as original |

These are pressure classes, not runtime fixtures or universal mechanics.

## 6. Cross-package handoff boundaries

### R2B-CONTINUITY

Later separately authorized CONTINUITY work may govern:

- stable authoritative timeline identity;
- branch canonicality, class, and ancestry;
- correction/compensation/retcon/supersession classification;
- branch-safe projection and disclosure;
- world-valid versus record/commitment-time qualification.

R2B-CORE does not pre-solve those questions.

### R2B-CROSS-PHASE

Later separately authorized CROSS-PHASE work may govern:

- ruleset identity;
- content-package identity;
- campaign-override identity;
- related version identity;
- applicability;
- pinning;
- effective intervals.

R2B-CORE does not pre-solve those questions.

### Runtime and persistence implementation

This artifact grants no authority to implement:

- persistence;
- snapshots;
- event stores;
- branch stores;
- RNG services;
- replay engines;
- correction services;
- production schemas.

Those remain later authorized implementation obligations.

## 7. Escalation rule

A pressure that cannot be resolved by these two qualifications without
defining branch semantics, correction taxonomy, version effectivity, new domain
semantics, or implementation architecture must be routed to the applicable
later owner or gate.

Do not broaden R2B-CORE merely to keep the pressure local.

## 8. Machine-reviewable contract

```json
{
  "artifact_id": "AFQR-R2B-CORE-QUALIFICATIONS-001",
  "artifact_version": "0.1.0",
  "package_id": "R2B-CORE",
  "workstream_id": "PR2-R2B-C",
  "authority_effect": "bounded_r2b_core_doctrine_qualification",
  "replaces_r1d_core": false,
  "component_owners": {
    "AFQR-01": [
      "transition_commitment",
      "qualified_write_ownership",
      "recovery",
      "replay",
      "transition_receipts",
      "committed_audit"
    ],
    "AFQR-02": [
      "command_identity",
      "attempt_identity",
      "execution_identity_distinction",
      "technical_retry",
      "suspension_escalation",
      "durable_command_progress"
    ]
  },
  "created_semantic_owners": [],
  "modules": [
    {
      "module_id": "R2B-CORE-MOD-PREVIEW-PERSISTENCE-PROMOTION",
      "qualification": {
        "retained_preview_status": "proposal",
        "persistence_authority_effect": "none",
        "persistence_confers_commitment": false,
        "persistence_confers_canonicality": false,
        "persistence_confers_branch_status": false,
        "promotion_requires_explicit_lawful_transition": true,
        "promotion_target_requires_separate_governance": true,
        "promotion_retroactively_commits_preview": false,
        "branch_classification_defined_here": false
      }
    },
    {
      "module_id": "R2B-CORE-MOD-CORRECTION-RNG-IDENTITY",
      "qualification": {
        "original_committed_audit_preserved": true,
        "replay_or_recovery_may_generate_replacement_outcome": false,
        "technical_retry_may_reroll": false,
        "authorized_correction_new_resolution_requires_distinguishable_replacement_execution": true,
        "replacement_randomness_provenance_separately_attributable": true,
        "command_attempt_classification_remains_afqr_02": true,
        "deterministic_procedures_require_randomness": false,
        "universal_rng_implementation_mandated": false
      },
      "randomness_pressure_families": [
        "dice",
        "cards",
        "bags",
        "oracle_draws",
        "random_tables",
        "encounter_tables",
        "pseudo_random_generators",
        "deterministic_source_local_uncertainty_procedures",
        "external_randomized_mechanisms",
        "mixed_deterministic_random_resolution"
      ]
    }
  ],
  "implementation_nonrequirements": [
    "database",
    "snapshot_representation",
    "branch_store",
    "journal_format",
    "prng_seed",
    "dice",
    "random_number_generator",
    "entropy_source",
    "deck_storage",
    "shuffle_algorithm",
    "runtime_rng_field"
  ],
  "handoffs": {
    "R2B-CONTINUITY": [
      "timeline_identity",
      "world_valid_vs_record_time",
      "branch_canonicality_class_ancestry",
      "correction_compensation_retcon_supersession",
      "branch_safe_projection_disclosure"
    ],
    "R2B-CROSS-PHASE": [
      "version_identity",
      "applicability",
      "pinning",
      "effective_intervals"
    ],
    "later_implementation": [
      "persistence",
      "snapshot",
      "event_store",
      "branch_store",
      "rng_service",
      "replay_engine",
      "correction_service",
      "production_schema"
    ]
  },
  "prohibited_inferences": [
    "persistence_makes_preview_authoritative",
    "storage_creates_branch_status",
    "promotion_is_retroactive_commitment",
    "replay_may_reroll",
    "correction_may_overwrite_original_randomness",
    "one_rng_mechanism_is_universal",
    "r2b_core_owns_branch_semantics",
    "r2b_core_owns_correction_taxonomy",
    "r2b_core_owns_version_effectivity",
    "r2b_core_authorizes_runtime_implementation"
  ]
}
```
