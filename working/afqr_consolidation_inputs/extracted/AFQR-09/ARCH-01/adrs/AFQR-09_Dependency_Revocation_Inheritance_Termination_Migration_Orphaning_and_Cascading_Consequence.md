# AFQR-09 - Dependency, Revocation, Inheritance, Termination, Migration, Orphaning, and Cascading Consequence

**Selected architecture:** Registered Typed Dependency-and-Obligation Hypergraph with Version-Pinned Lifecycle Policies and Bounded Causal Propagation  
**Abbreviation:** `RTDOH-VLP-BCP`  
**Ratification status:** `ratified_with_mandatory_amendments`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines persistent support, grant, authority, obligation, entitlement, relationship, resource-link, revocation, inheritance, migration, orphan, and cascade behavior without automatic consequences from identity, provenance, state ownership, possession, graph reachability, deletion, or event order.

## Central law
> Every authoritative persistent link is a version-pinned typed governed-relation instance with explicit semantic family, participant bindings, condition algebra, orthogonal lifecycle status, authority records, consequence policy, source scope, and relation continuity. A registry-backed frozen discovery basis and non-mutating plan must establish the complete affected scope, cycle disposition, atomic closure set, and bounded descendant consequences. Only authoritative owners mutate through AFQR-01. Missing or nonconvergent law produces a lawful blocked, suspended, indeterminate, quarantined, unverifiable, or escalated result.

## Universal components
- Governed-relation definition and instance registries.
- Typed participant roles and target selectors.
- Formal condition truth algebra.
- Versioned lifecycle, authority, revocation, consequence, cycle, and migration policies.
- Relation continuity and lineage.
- Registry snapshot and discovery completeness receipt.
- Non-mutating impact and cascade planner.
- Atomic-root closure certificate and descendant partition.
- Bounded cascade frontier and resume protocol.
- Cycle classification and certified fixed-point evaluator.
- Orphan, replacement, autonomy, and repair state machine.
- Private dependency receipt and observer projection.
- Bitemporal historical replay and semantic policy archive.
- Source-local and aggregate containment.

## Core contracts
- `GovernedRelationDefinition`
- `GovernedRelationInstance`
- `GovernedRelationStatus`
- `DependencyParticipant`
- `ConditionTruth`
- `ConditionEvidenceStatus`
- `DependencyConditionExpression`
- `RevocationAuthorityRecord`
- `RevocationRequest`
- `RevocationDetermination`
- `BreachAssertion`
- `BreachDetermination`
- `OrphanDetermination`
- `ReplacementCandidateSet`
- `GovernedRelationContinuityReceipt`
- `GovernedRelationLineageEdge`
- `DependencyRegistrySnapshot`
- `DependencyDiscoveryReceipt`
- `DependencyImpactSet`
- `CascadePlan`
- `AtomicConsequenceClosureCertificate`
- `ConsequenceOccurrenceKey`
- `CascadeFrontier`
- `CascadeExecutionReceipt`
- `AggregateSemanticsCertificate`
- `DependencyMigrationPlan`
- `HistoricalPolicySemanticArchive`

## Determination or execution pipeline
1. validate governed-relation definition and instance
2. freeze registry, graph, selector, time, and evidence basis
3. evaluate formal condition truth and evidence status
4. determine lifecycle, revocation, breach, migration, or orphan proposal
5. discover complete direct and transitive affected scope
6. classify SCCs and evaluate certified cycles
7. construct non-mutating impact and cascade plan
8. prove the root atomic closure set
9. prepare traversal-independent descendant-command specifications
10. obtain AFQR-06 through AFQR-08 handoffs
11. commit root owner fragments, outbox, and frontier through AFQR-01
12. execute bounded descendants under AFQR-02 and AFQR-04

## Ratified constraints and amendments
- The shared graph uses a governed-relation supertype; grants, obligations, authority, support, custody, control, and resource links are not flattened into one semantic dependency.
- Lifecycle is represented by orthogonal status planes rather than one mutually exclusive enum.
- Relation-instance continuity, amendment, split, merge, migration, supersession, and termination receive explicit receipts and lineage.
- Condition truth is separate from evidentiary or procedural status and has canonical operator truth tables.
- Evaluators are deterministic, total or explicitly partial, non-mutating, no-I/O, no-model, bounded, versioned, and preferably declarative.
- Discovery completeness binds an authoritative registry snapshot and index roots; unregistered or unindexed links cannot create authoritative consequences.
- Fixed-point policy declares least, greatest, unique, or source-local selected fixed point plus canonical seed and order-independent semantics.
- Planning references are separate from committed transition references.
- An AtomicConsequenceClosureCertificate proves which effects must commit with the root and why deferred descendants are safe.
- Descendant command identity is traversal-independent and deduplicates overlapping discovery paths unless multiplicity is explicit.
- Aggregate execution requires an AggregateSemanticsCertificate proving batch and retry equivalence.
- Participant bindings, authority, evidence, assertions, and lifecycle records are bitemporal.
- Historical replay archives canonical semantic policy IR and interpreter contracts rather than depending on arbitrary old executable code.
- Revocation ordering binds to AFQR-04 logical-time checkpoints and common-prestate profiles, never worker races.
- Identity continuity and provenance never transfer dependencies or revocation authority automatically.
- Breach, revocation, expiration, suspension, destruction, dissolution, orphaning, termination, and retirement remain distinct.
- Root write sets freeze before commit; late precommit discovery replans and late postcommit discovery reconciles.
- Cycle budgets yield and persist; they never truncate semantics.
- Hidden clauses and graph size remain private and cannot leak through option count, timing, progress, or receipt hashes.
- The current AFQR-01 through AFQR-09 sequence completes the cross-system execution foundation, not all Astra foundational doctrine.

## Guarantees
- Typed governed relations.
- Version-pinned lifecycle and authority.
- Explicit revocation and breach.
- Identity-safe inheritance and migration.
- Lawful orphan states.
- Complete frozen discovery.
- Atomic-root and durable-descendant partition.
- Bounded fan-out and cycle handling.
- Hidden dependency containment.
- Historical semantic replay.

## Non-guarantees
- Universal contract, property, inheritance, debt, familiar, patron, or office law.
- All cycles are invalid.
- All orphans terminate.
- Identity determines survival.
- Generalized dependency execution is currently authorized.

## Required non-mutating prototype
The AFQR-09 Dependency Discovery, Lifecycle, and Cascade Planning Dry Run, implemented in layers: relation validation; condition algebra; registry snapshot and discovery; cycle analysis; lifecycle and revocation determination; orphan and successor candidates; impact analysis; atomic closure; descendant specifications; private and visible receipts. The first shared end-to-end fixture is the bloodline familiar, proxy grant, signer entitlement, capability suppression, revocation dispute, reservation disposition, and proxy survival sequence.

## Required artifacts
- AFQR-09 ADR
- governed-relation doctrine
- orthogonal lifecycle contract
- condition algebra
- authority and revocation registry
- relation continuity and lineage
- registry snapshot and discovery receipt
- impact and cascade contracts
- atomic closure certificate
- cycle and fixed-point doctrine
- aggregate semantics certificate
- orphan and migration contracts
- hidden projection contract
- dependency pressure IR pack
- adversarial fixture pack

## Blocked work
- generalized persistent-link mutation
- revocation execution
- automatic inheritance
- cascade mutation
- mass fan-out mutation

## Work unlocked
- AFQR-01 through AFQR-09 artifact ratification
- shared AFQR-08/09 fixtures
- non-mutating identity and dependency dry runs

## Cross-question handoff
AFQR-09 closes the current cross-system execution sequence. Domain-specific legal, social, consent, metaphysical, and simulation doctrines remain later work.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
