# AFQR R2 Continuity and Deterministic-Backend Research Intake Packet

**Status:** nonauthoritative research intake evidence  
**Layer:** R2 review input only  
**Authority:** none beyond source identification, compact restatement, and routing hypotheses  
**Verified repository base:** `bbc9d58cb23f1616327f73294def6ec42055a324`  
**Raw-source posture:** the five full reports remain outside the repository; this packet is a compact substitute for Codex attachment transfer

## 1. Purpose

This packet allows an R2-0 Codex task to consume five user-supplied research reports that cannot be attached directly to Codex.

It does not promote the reports to doctrine, canon, runtime contracts, schemas, implementation specifications, training data, or live-play instructions.

It preserves:

- exact raw-source hashes, byte sizes, and line counts;
- each report's distinct contribution;
- consensus and disagreement clusters;
- normalized claim candidates;
- likely Astra owner seams;
- likely R2/R3/R4/R5/evaluation destinations;
- rejected or premature proposals;
- source limitations and stale repository assumptions.

Codex must still compare every claim against accepted R1 authority and current repository facts. This packet must not be treated as a pre-ratified claim ledger.

## 2. Raw-source inventory

The full raw files were supplied outside the repository and are intentionally not committed.

| Source ID | Original filename | Document role | SHA-256 | Lines | Bytes |
|---|---|---|---|---:|---:|
| `R2-RES-ACTUALPLAY-001` | `dont lose KEEP1.md` | deterministic-backend patterns from long-form actual play | `323ac599df66c5d0db649299fcb68c6f0bbd54ee0cd4166f37e9ab05b1bcc1ea` | 140 | 34007 |
| `R2-RES-CONTINUITY-001` | `dont lose KEEP2md.md` | engineering-heavy branch/time/correction architecture | `f009f74e0ffe128dbf0e5cbee4ca11140175ec8c7927f8242358851e05d32a96` | 942 | 113738 |
| `R2-RES-CONTINUITY-002` | `dont lose KEEP3 (1).md` | branch/time doctrine, adversarial scenarios, benchmarks, and roadmap | `789f1da10fa8d3f9e562b82f049236df17a2006931f26d7bd7a4779ba818e9ac` | 891 | 98886 |
| `R2-RES-CONTINUITY-003` | `dont lose KEEP4.md` | continuity integrated with epistemic, projection, security, and organized-play pressure | `714274a74d63532f268a8e39f7496fc395f2335351c3d70efdc0ba3ddcb56d6b` | 492 | 81818 |
| `R2-RES-CONTINUITY-004` | `dont lose KEEP5.md` | broad synthesis, minimal records, doctrine ownership, and staged roadmap | `ca6d60bcfb605da437d737d341e47a73ebdaef00ece4627a813f09e0e2a3ce3a` | 593 | 72000 |

The session-local external citation tokens embedded in the raw reports are provenance clues only. They are not repository-resident evidence identifiers and must not be copied into governing Astra artifacts as if they were stable citations.

## 3. Source-specific contributions

### 3.1 `R2-RES-ACTUALPLAY-001`

Primary contribution: demonstrates that long-form actual play remains reproducible only when narrative outcomes pass through explicit stateful procedures.

Unique pressure areas:

- explicit scene or combat entry;
- participant sets and turn/priority order;
- binary, opposed, banded, and success-with-cost resolution;
- resource, condition, status, injury, and defeat ledgers;
- meta-currencies and achievement-like state;
- resource-priced retroactive preparation;
- versioned house rules and custom mechanics;
- session-boundary recap and serialization;
- visible-safe projection of authoritative state;
- inserted side chronology and rotating tables.

Use this source primarily for:

- doctrine pressure;
- donor-family-neutral evaluation cases;
- adversarial benchmarks;
- later deterministic-GM and narrator evaluation.

Do not use it to establish D&D initiative, spell slots, death saves, PbtA mixed success, Blades stress, or any other donor procedure as universal Astra law.

### 3.2 `R2-RES-CONTINUITY-001`

Primary contribution: detailed engineering translation of continuity doctrine into a local-first authoritative backend.

Unique strengths:

- optimistic concurrency and expected-version checks;
- short-lived reservations for unique resources;
- idempotency, duplicate suppression, and crash recovery;
- append-only event and outbox reasoning;
- distinction between previews and durable branches;
- explicit schema and service staging;
- rejection of CRDT-first canon, multi-master truth, and broad pessimistic locking;
- direct identification of event-envelope migration risk.

### 3.3 `R2-RES-CONTINUITY-002`

Primary contribution: doctrine and governance shape plus a broad adversarial evaluation pack.

Unique strengths:

- clean branch taxonomy and promotion-versus-merge distinction;
- correction and retcon severity taxonomy;
- state-machine sketches for branches, corrections, retcons, migrations, and stale commands;
- approximately forty continuity/adversarial scenarios;
- hard-fail benchmark families;
- explicit decisions-now versus decisions-later roadmap;
- strong organized-play and multi-group continuity framing.

### 3.4 `R2-RES-CONTINUITY-003`

Primary contribution: integration of branch/time doctrine with epistemic state, context-packet safety, and campaign administration.

Unique strengths:

- separation of valid time, transaction time, disclosure time, and causal order;
- branch identity as a projection-policy input;
- explicit protection against abandoned-branch and hidden-state leakage;
- session closure as both continuity and spoiler-safe recap input;
- organized-play and troupe-play administration as persistence pressure;
- human-review boundary for knowledge-affecting retcons;
- explicit AI security and least-privilege concerns;
- compact P0/P1/P2 staging and open questions.

### 3.5 `R2-RES-CONTINUITY-004`

Primary contribution: broadest synthesis and clearest minimal architectural spine.

Unique strengths:

- one timeline and one active canonical branch posture;
- smallest durable record set;
- explicit identification of correction/supersession as the most dangerous missing capability;
- staged progression from single-campaign continuity to split-party, multi-party, and alternate-world support;
- file-ownership and modular doctrine recommendations;
- distinction between standalone records and fields that may remain inline;
- comprehensive decisions-now, deferrals, rejections, and open questions.

## 4. High-confidence consensus

The four continuity reports strongly converge on the following research findings.

1. One authoritative world history must not become several equally writable truths.
2. A persistent world needs stable timeline identity.
3. At most one branch should be active canonical history for one timeline at a time.
4. Replay, migration, correction, hypothetical, debug, and alternate-world histories require explicit classification.
5. An uncommitted preview is not automatically a durable branch.
6. Committed history must remain append-only and audit-preserving.
7. World-valid time and record/commit time are distinct.
8. Causal order must not be inferred solely from chronology.
9. Corrections, compensating events, supersession, soft retcons, and hard retcons are not equivalent.
10. Hard retcons and canon rewrites require explicit authority and human review.
11. Historical replay should default to the ruleset, content package, and campaign override active at original resolution.
12. Committed RNG must not be silently rerolled on the same historical event.
13. Canonical branch divergence should not be resolved by generic mechanical merge.
14. Branch-local, preview, abandoned, or debug facts must not enter canonical context by default.
15. Session closure must serialize more than recap prose.
16. Stale commands and unique-resource races require explicit conflict handling.
17. Offline progression should be scheduled, bounded, aggregate, or lazy rather than continuous simulation of all inactive entities.
18. Replay mismatches and continuity corruption should fail closed and enter quarantine.
19. Model output remains downstream from authoritative state and cannot own canon, hidden truth, correction, or commitment.
20. Full distributed consensus, CRDT-first canon, automatic canonical merge, mandatory graph storage, and universal continuous simulation are premature or wrong for the current single-authority architecture.

The actual-play report independently reinforces that deterministic play requires explicit state transitions, resolution contexts, resource/condition mutation, rule versioning, and session serialization.

## 5. Material differences and unresolved choices

The reports agree on direction but do not fully agree on every representation or implementation boundary.

### 5.1 Logical-time representation

Options presented:

- standalone `LogicalTimeRecord`;
- inline logical-order fields on committed events and session closures.

Routing note: this is a schema/implementation-shape question. R2 should define required semantics without prematurely requiring a standalone record.

### 5.2 Branch object timing

Options presented:

- introduce a first-class slim `BranchRecord` immediately;
- first introduce branch identity and canonical pointer semantics, then richer branch records later.

Routing note: R2 doctrine should decide branch identity, class, ancestry, authority, and canonicality. R4 should decide the minimal runtime record/service shape.

### 5.3 Knowledge-history materialization

Options presented:

- first-class `KnowledgeEventRecord` is core now;
- preserve branch/disclosure hooks now and deepen historical knowledge later;
- derive some knowledge from event plus visibility history until pressure justifies materialization.

Routing note: preserve AFQR-06/AFQR-10/AFQR-20 separation and route implementation shape to the deferred bitemporal truth/evidence substrate.

### 5.4 Timeline scope

Options presented:

- one timeline per campaign;
- one timeline per authoritative world;
- one campaign may contain multiple explicit timelines only for sanctioned alternate realities.

Routing note: doctrine must define identity and scope without adopting multiverse functionality prematurely.

### 5.5 Disclosure time

Options presented:

- explicit disclosure-time field;
- disclosure represented through knowledge/observation events;
- disclosure references stored on continuity or projection records.

Routing note: preserve semantics now; defer physical representation until AFQR-06/10/20 and SUB-002 integration is settled.

### 5.6 Correction workflow shape

Options presented:

- all state-affecting corrections spawn a correction branch;
- minor bounded corrections may commit supersession directly;
- hard retcons require a correction branch, while some soft corrections use direct append-only adjudication.

Routing note: R2 doctrine must classify correction severity and required authority. Runtime workflow belongs later.

### 5.7 Region, plane, and actor-local time

All reports preserve future compatibility, but they disagree on whether these are Stage 3, Stage 4, or Stage 5 concerns.

Routing note: dual-time and causal semantics are immediate doctrine pressure. Rich local-time mechanics remain deferred unless current donor or runtime pressure proves otherwise.

### 5.8 World ticks and offline progression

All reports prefer scheduled and bounded progression, but implementation detail ranges from near-term records to later multi-party support.

Routing note: R2 may define noncontinuous progression principles. General scheduler and world-tick implementation remain later substrate work.

### 5.9 Human arbitration surface

The reports agree that ambiguous high-impact conflicts require human review, but differ on whether a formal arbitration UI grammar is needed now.

Routing note: doctrine needs statuses and authority boundaries; UI can wait.

## 6. Obsolete or low-trust statements in the raw reports

All four continuity reports state that repository access was unavailable during their research sessions.

That limitation is historical and must not be repeated as a current repository fact.

Current work must inspect the actual repository and distinguish:

- implemented generalized behavior;
- implemented narrow fixtures;
- accepted doctrine;
- planning language;
- missing doctrine;
- missing schema;
- missing implementation.

The raw reports' claims that a feature is missing or unimplemented are research hypotheses until checked against current `main`.

## 7. Normalized claim candidates

The following are claim candidates for R2-0 routing. They are not pre-approved doctrine decisions.

### `R2-INTAKE-CLAIM-001` — Authoritative timeline identity

Claim: each authoritative world history needs stable timeline identity.

Likely owners and seams:

- AFQR-04 for time and chronology semantics;
- AFQR-01 for commitment references;
- AFQR-08 for identity distinctions where timeline identity interacts with copied or alternate realities.

Likely destinations:

- primary: `r2_new_doctrine_candidate`;
- secondary: `r3_conformance_obligation`, `r4_runtime_substrate_obligation`.

Prohibited shortcut: event-store or database identity must not become owner of time or world semantics.

### `R2-INTAKE-CLAIM-002` — One active canonical branch

Claim: one timeline should have at most one active canonical branch; divergent histories are selected, superseded, archived, or preserved as separate alternate realities.

Likely destinations:

- primary: `r2_new_doctrine_candidate`;
- secondary: `r4_runtime_substrate_obligation`, `evaluation_or_benchmark_input`.

Prohibited shortcut: no generic symmetric merge of contradictory canonical histories.

### `R2-INTAKE-CLAIM-003` — Branch taxonomy

Claim: canonical, replay, correction, migration, hypothetical, debug, archived, quarantined, and alternate-reality histories need governed distinctions.

Likely destinations:

- primary: `r2_new_doctrine_candidate`;
- secondary: `r3_conformance_obligation`, `r4_runtime_substrate_obligation`.

Open question: which classes require durable branch records versus ephemeral evaluation contexts.

### `R2-INTAKE-CLAIM-004` — Preview is not branch

Claim: ordinary uncommitted command previews should remain branchless proposals or sandboxes unless intentionally persisted.

Likely destinations:

- primary: `partially_governed_r2_qualification_needed`;
- secondary: `r3_conformance_obligation`, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-005` — Valid time and transaction time

Claim: authoritative history needs distinct world-valid and record/commit time semantics.

Likely owners and seams:

- AFQR-04 time semantics;
- AFQR-01 commitment;
- AFQR-06/10 for correction and epistemic consequences.

Likely destinations:

- primary: `r2_new_doctrine_candidate` or `partially_governed_r2_qualification_needed` after R1 comparison;
- secondary: `r4_runtime_substrate_obligation` under SUB-002/SUB-003.

### `R2-INTAKE-CLAIM-006` — Causal order distinct from chronology

Claim: causal parentage, enabling conditions, scheduling, cancellation, and downstream revalidation cannot be reconstructed safely from timestamps alone.

Likely owners:

- AFQR-04 causal order and scheduled effects;
- AFQR-09 dependency, revocation, migration, and cascades.

Likely destinations:

- primary: `already_governed_by_r1` or `partially_governed_r2_qualification_needed`;
- secondary: `r3_conformance_obligation`, `r4_runtime_substrate_obligation`.

### `R2-INTAKE-CLAIM-007` — Append-only correction governance

Claim: committed historical records must not be silently mutated; current canon changes through new correction, compensation, supersession, or retcon records.

Likely owners:

- AFQR-01 transition, commitment, recovery, and replay;
- AFQR-04 temporal placement;
- AFQR-09 dependency consequences.

Likely destinations:

- primary: `r2_new_doctrine_candidate` or `partially_governed_r2_qualification_needed`;
- secondary: `r4_runtime_substrate_obligation` under SUB-003.

### `R2-INTAKE-CLAIM-008` — Correction taxonomy

Claim: display, metadata, provenance, arithmetic, resource, dice-entry, rule-interpretation, compensation, soft-retcon, hard-retcon, canon-revision, and alternate-timeline cases require distinct authority and replay rules.

Likely destinations:

- primary: `r2_new_doctrine_candidate`;
- secondary: `evaluation_or_benchmark_input`, `later_gm_adapter_input`.

### `R2-INTAKE-CLAIM-009` — Historical RNG preservation

Claim: correction must not reroll a lawfully committed RNG outcome on the same historical event; replacement resolution uses a distinct corrected execution path while preserving original audit.

Likely owners:

- existing RNG doctrine;
- AFQR-01 commitment and replay;
- AFQR-02 command identity.

Likely destinations:

- primary: `partially_governed_r2_qualification_needed`;
- secondary: `r3_conformance_obligation`, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-010` — Ruleset and package pinning

Claim: every historical resolution must identify the ruleset, content-package set, campaign overrides, and schema context that governed it.

Likely destinations:

- primary: `r2_new_doctrine_candidate` or `r2_drift_audit_input`;
- secondary: `r3_conformance_obligation`, `r4_runtime_substrate_obligation`.

Prohibited shortcut: latest installed rules must not silently reinterpret old events.

### `R2-INTAKE-CLAIM-011` — Session closure contract

Claim: session or scene closure must serialize event range, hashes, versions, time span, unresolved reservations, scheduled consequences, knowledge/projection deltas, and recap inputs.

Likely destinations:

- primary: `r2_new_doctrine_candidate`;
- secondary: `r4_runtime_substrate_obligation`, `later_gm_adapter_input`.

### `R2-INTAKE-CLAIM-012` — Branch-safe visibility

Claim: branch identity and disclosure frontier must participate in projection and context-packet policy; noncanonical data is excluded by default.

Likely owners:

- AFQR-10 epistemic state;
- AFQR-20 sensing/contacts;
- existing projection and model-boundary doctrine.

Likely destinations:

- primary: `partially_governed_r2_qualification_needed`;
- secondary: `r3_conformance_obligation`, `r4_runtime_substrate_obligation`, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-013` — Truth, evidence, knowledge, and belief separation

Claim: corrections and replay require separate histories for world truth, admissible evidence, actor knowledge, belief, player discovery, and model-visible context.

Likely owners:

- AFQR-06 evidence and arbitration;
- AFQR-10 truth, knowledge, and belief;
- AFQR-20 observation and sensing;
- AFQR-04 temporal relationships.

Likely destinations:

- primary: `already_governed_by_r1` or `partially_governed_r2_qualification_needed`;
- secondary: `r4_runtime_substrate_obligation` under SUB-002.

Prohibited shortcut: no combined truth/evidence/knowledge/sensing owner.

### `R2-INTAKE-CLAIM-014` — Optimistic concurrency and reservations

Claim: commands compiled from stale state must fail or re-enter arbitration; unique resources require short-lived reservations with expiry and settlement.

Likely owners:

- AFQR-02 command lifecycle;
- AFQR-01 commitment;
- AFQR-07 typed quantity reservation/settlement where quantities actually apply;
- AFQR-19 action/conflict procedure where scene ordering applies.

Likely destinations:

- primary: `r4_runtime_substrate_obligation` or `r5_runtime_retrofit_obligation`;
- secondary: `r2_new_doctrine_candidate` for principles, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-015` — Crash-safe in-flight work

Claim: durable command status, reservation state, idempotency keys, and publication receipts are required to recover without duplicate commitment or orphaned locks.

Likely destinations:

- primary: `r4_runtime_substrate_obligation` under SUB-003;
- secondary: `r3_conformance_obligation`, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-016` — Scheduled and bounded offline progression

Claim: inactive-world progression should use scheduled events, bounded aggregate ticks, and lazy catch-up, not unrestricted micro-simulation.

Likely owners:

- AFQR-04 scheduled effects;
- AFQR-17 environment where environmental state advances;
- domain owners for faction, crafting, recovery, travel, or economy semantics.

Likely destinations:

- primary: `deferred_frontier` or `r2_new_doctrine_candidate` for high-level bounds;
- secondary: `r4_runtime_substrate_obligation`, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-017` — Quarantine on continuity corruption

Claim: replay hash mismatch, missing packages, broken causal references, corrupt snapshots, or invalid branch pointers must freeze affected canonical mutation and preserve forensic evidence.

Likely destinations:

- primary: `r4_runtime_substrate_obligation`;
- secondary: `partially_governed_r2_qualification_needed`, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-018` — Explicit scene/procedure transitions

Claim: deterministic play requires explicit transition into combat, contest, downtime, travel, research, recovery, or another procedure mode rather than narration silently changing resolution law.

Likely owners:

- AFQR-02 command lifecycle;
- AFQR-19 action and conflict resolution;
- procedure-specific doctrine owners.

Likely destinations:

- primary: `evaluation_or_benchmark_input`;
- secondary: `r2_drift_audit_input`, `r3_conformance_obligation`.

### `R2-INTAKE-CLAIM-019` — Multiple resolution grammars

Claim: Astra must represent binary outcomes, opposed contests, outcome bands, success with cost, questions, follow-up choices, and source-local procedures without making one donor grammar universal.

Likely destinations:

- primary: `evaluation_or_benchmark_input`;
- secondary: `r2_drift_audit_input`, `later_conversion_or_canon_review`.

Prohibited shortcut: no universal D&D, PbtA, or Blades resolution baseline.

### `R2-INTAKE-CLAIM-020` — Resource, condition, and defeat ledgers

Claim: persistent play requires typed, provenance-aware resource, condition, status, injury, and defeat state transitions.

Likely destinations:

- primary: `r3_conformance_obligation` or `r4_runtime_substrate_obligation` depending current repository state;
- secondary: `evaluation_or_benchmark_input`.

Prohibited shortcut: the continuity or event subsystem must not own substantive resource, harm, recovery, or condition semantics.

### `R2-INTAKE-CLAIM-021` — Versioned custom rules

Claim: house rules and source-local procedures require explicit identifiers, authority, effective intervals, and replay behavior rather than hidden code forks or informal notes.

Likely destinations:

- primary: `r2_new_doctrine_candidate`;
- secondary: `r3_conformance_obligation`, `r4_runtime_substrate_obligation`, `later_conversion_or_canon_review`.

### `R2-INTAKE-CLAIM-022` — Recap compiler consumes projections

Claim: recaps and restart packets should consume session closure plus visibility/knowledge projections rather than raw authoritative state or raw transcripts.

Likely destinations:

- primary: `later_gm_adapter_input`;
- secondary: `r2_new_doctrine_candidate`, `r4_runtime_substrate_obligation`, `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-023` — Branch and continuity benchmark pack

Claim: automatic hard failures should cover silent historical mutation, wrong-version replay, branch leakage, duplicate unique resources, unauthorized retcon, stale-command commitment, preview contamination, incomplete session closure, and unquarantined replay divergence.

Likely destinations:

- primary: `evaluation_or_benchmark_input`;
- secondary: `r3_conformance_obligation`, `r4_runtime_substrate_obligation`.

### `R2-INTAKE-CLAIM-024` — Storage does not transfer semantic ownership

Claim: event stores, journals, reducers, branch managers, timeline records, replay services, and snapshot systems consume and preserve domain semantics but do not become their substantive owners.

Likely destinations:

- primary: `already_governed_by_r1`;
- secondary: `r2_drift_audit_input`, `r3_conformance_obligation`.

Relevant R1 pressure: INV-001 and the owner separation recorded for SUB-002 and SUB-003.

### `R2-INTAKE-CLAIM-025` — Rejected CRDT/multi-master canon

Claim: CRDT-first canonical storage, multi-master world truth, and generic automatic canonical branch merging are incompatible with Astra's single-authority world model.

Likely destinations:

- primary: `rejected_as_overengineered`;
- secondary: `r2_new_doctrine_candidate` only as an explicit prohibition.

### `R2-INTAKE-CLAIM-026` — Rejected universal continuous simulation

Claim: simulating every inactive entity continuously is unnecessary, expensive, and less auditable than bounded scheduled progression.

Likely destinations:

- primary: `rejected_as_overengineered`;
- secondary: `evaluation_or_benchmark_input`.

### `R2-INTAKE-CLAIM-027` — Rejected graph-database mandate

Claim: causality is graph-shaped, but Astra does not need a graph database as a foundational requirement; typed references may suffice until query pressure proves otherwise.

Likely destinations:

- primary: `rejected_as_overengineered`.

### `R2-INTAKE-CLAIM-028` — Deferred actor-local temporal physics

Claim: actor-local time, region/plane transforms, cryosleep, and time-dilation mechanics should remain compatible with the core model but need not be implemented now.

Likely destinations:

- primary: `deferred_frontier`.

### `R2-INTAKE-CLAIM-029` — Deferred alternate-timeline gameplay

Claim: alternate timelines may be a lawful future construct, but full multiverse functionality, cross-reality identity, and time travel should not enter current Gate B work.

Likely destinations:

- primary: `deferred_frontier`.

### `R2-INTAKE-CLAIM-030` — Later GM-adapter use

Claim: actual-play examples are valuable later for arbitration, clarification, pacing, interruption, recap, and observability behavior, but only after doctrine and runtime authority are settled.

Likely destinations:

- primary: `later_gm_adapter_input`;
- secondary: `evaluation_or_benchmark_input`.

## 8. R1E deferred-substrate alignment

### SUB-002 — generalized bitemporal truth/evidence store

Research pressure landing here includes:

- valid time versus record time;
- delayed revelation;
- branch-local truth;
- historical knowledge and belief;
- correction-safe evidence;
- context-packet and recap leakage prevention.

Mandatory owner separation:

- AFQR-04: time, simultaneity, causal order, scheduled effects;
- AFQR-06: claims, evidence admission, arbitration;
- AFQR-10: truth, epistemic state, knowledge, belief;
- AFQR-20: sensing, detection, contacts, tracks.

R2 may refine doctrine and conformance obligations. It may not implement the generalized substrate or create a universal time/truth/evidence/sensing owner.

### SUB-003 — generalized owner-reducer transaction journal

Research pressure landing here includes:

- append-only commitment;
- command identity across retries;
- branch/timeline references;
- supersession and correction records;
- causal parents;
- expected owner versions;
- crash-safe reservations;
- session closure;
- historical replay and migration provenance.

Mandatory owner separation:

- AFQR-01: transition, routing, commitment, recovery/replay doctrine;
- AFQR-02: command identity and durable progress;
- AFQR-04: time and causal ordering;
- AFQR-09: dependency, revocation, migration, and cascades.

R2 may define doctrine. Generalized journal, reducer, persistence, and branch-service implementation remain later work.

### SUB-001, SUB-004, and SUB-005

Secondary pressure exists for:

- governed relations, obligations, and institutional continuity under SUB-001;
- adapter/bridge registration under SUB-004;
- spatial, signal, embodiment, institution, and social owner contracts under SUB-005.

A continuity layer must not combine or transfer these domain owners.

## 9. Candidate evaluation families

The reports support later benchmark families for:

1. timeline ordering;
2. valid-time versus transaction-time insertion;
3. causal integrity;
4. branch isolation;
5. branch leakage;
6. correction classification;
7. retcon authority;
8. replay after correction;
9. ruleset-version replay;
10. stale-command rejection;
11. conflict detection;
12. reservation settlement;
13. session-closure completeness;
14. offline progression bounds;
15. actor-knowledge history;
16. hidden-information preservation;
17. snapshot invalidation;
18. migration safety;
19. model-boundary compliance;
20. explicit procedure-mode transition;
21. multiple resolution grammars;
22. resource and condition ledger fidelity;
23. recap projection safety.

These are evaluation obligations, not proof that corresponding runtime services exist.

## 10. Rejected or premature proposals

The research set strongly rejects or defers:

- multi-master canonical truth;
- CRDT-first canon;
- automatic three-way canonical branch merge;
- treating every preview as a durable branch;
- rerolling committed RNG during ordinary correction;
- replaying all history under the newest rules by default;
- graph-database adoption as a prerequisite;
- distributed consensus for the local-first phase;
- continuous simulation of every inactive entity;
- exhaustive actor cognition or belief graphs in the initial kernel;
- full alternate-world tooling before single-world correction is stable;
- time travel as core continuity doctrine;
- model inference as a replacement for authoritative world ticks, hidden truth, or correction adjudication.

## 11. Proposed R2-0 processing requirements

Codex should use this packet to create the authoritative R2-0 source manifest, normalized claim-routing ledger, assimilation report, R2 control plan, R2 file manifest, tests, and tracking updates.

Codex must:

1. Treat the thirty intake claims as candidates, not final routing decisions.
2. Verify every owner and R1 reference against current repository artifacts.
3. Split or combine candidate claims when semantic review requires it.
4. Record the five raw-source hashes from this packet.
5. Mark the raw reports as external nonauthoritative evidence and not repository-resident.
6. Preserve source-specific unique contributions.
7. Record disagreements rather than forcing false consensus.
8. Reject obsolete repository-status assumptions from the raw reports.
9. Route schema and implementation requests to later gates.
10. Keep R2A blocked unless every material claim is routed.

## 12. Nonauthority and gate boundary

This intake packet grants no authority for:

- substantive R2 doctrine adoption;
- runtime implementation;
- persistence;
- reducers or journals;
- production schemas;
- timelines or branch services;
- correction or retcon execution;
- reservations or world ticks;
- conversion;
- canon promotion;
- sourcebook drafting;
- model training;
- narration;
- UI;
- live play;
- R3, R4, R5, or R6 work;
- RT-002G;
- temporary evidence deletion.

The intended next operation is R2-0 research assimilation. If R2-0 passes, R2A becomes ready. Overall R2 remains active and incomplete.
