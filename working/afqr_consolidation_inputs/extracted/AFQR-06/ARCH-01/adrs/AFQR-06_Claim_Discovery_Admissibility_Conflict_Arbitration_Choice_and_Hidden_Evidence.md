# AFQR-06 - Claim Discovery, Admissibility, Conflict, Arbitration, Choice, and Hidden Evidence

**Selected architecture:** Invariant-Gated Typed Claim Arbitration  
**Abbreviation:** `IGTCA`  
**Ratification status:** `ratified_with_mandatory_amendments`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines how multiple applicable rules, exceptions, authorities, source-local laws, and owner claims are discovered and combined without file-order precedence, universal numeric priority, global owner vetoes, or model judgment.

## Central law
> Only registered typed claims discovered for a frozen occurrence may participate. Constitutional invariants gate admission but are not precedence claims. Admissibility, applicability, conflict, combination, and owner-fragment feasibility are separate decisions. Arbitration produces evidence and a typed result; it does not mutate state.

## Universal components
- Claim-definition and occurrence registry.
- Claim-discovery index and completeness receipt.
- Constitutional invariant gate.
- Domain admissibility and applicability evaluation.
- Semantic conflict-key construction.
- Domain-authorized partial-order and combination policy.
- Authorized actor choice and administrative adjudication paths.
- Private arbitration receipt and visible projection.
- Post-combination owner-fragment feasibility gate.
- Historical policy-version replay.

## Core contracts
- `ClaimDefinition`
- `ClaimOccurrence`
- `ClaimDiscoveryReceipt`
- `ClaimApplicabilityResult`
- `SemanticConflictKey`
- `ConflictSet`
- `PrecedenceGraphInstance`
- `CombinationCandidate`
- `ArbitrationResult`
- `ChoiceAuthorization`
- `PrivateArbitrationReceipt`
- `VisibleArbitrationProjection`

## Determination or execution pipeline
1. discover all registered candidate claims
2. freeze claim occurrence and applicability basis
3. apply constitutional invariant and domain-admission gates
4. separate nonconflicting facet or slot claims
5. construct conflict sets
6. instantiate and validate the domain precedence or combination graph
7. resolve, combine, choose, adjudicate, or return indeterminate
8. run post-combination owner feasibility
9. emit evidence and receipts for later AFQRs and AFQR-01

## Ratified constraints and amendments
- Constitutional invariants, domain admissibility, claim conflict, and owner-fragment feasibility are separate gates.
- Claim conflict is not the same as inadmissibility or failed implementation feasibility.
- Semantic claim kind, claim origin, and dependency posture are separate fields.
- SemanticConflictKey is separate from occurrence context.
- ClaimDiscoveryReceipt must prove the applicable registered claim universe for the frozen scope.
- Pre-arbitration admission and post-combination feasibility are both mandatory.
- Architecture invariants are not precedence edges.
- Defeated applicable claims remain in the private receipt.
- Fingerprints do not prove semantic equivalence; equivalence requires certification.
- Specificity uses typed domain-authorized partial orders, never prose intuition.
- Indeterminate applicability must follow a registered block, suspend, omit, retry, quarantine, or escalate posture.
- Hidden choice observability categories must prevent option-shape side channels.
- Case adjudication is separate from policy amendment.
- The precedence graph is instantiated and validated per conflict set.
- Private arbitration hash, visible projection hash, and semantic result hash are distinct.
- Arbitration creates evidence, not mutation.

## Guarantees
- Typed conflict domains.
- Complete claim discovery for frozen scope.
- No file-order or popularity precedence.
- Lawful incomparability and indeterminacy.
- Hidden-evidence containment.
- Replayable policy versions.

## Non-guarantees
- Every conflict has a winner.
- A state owner has universal veto.
- Numeric priority is universally meaningful.
- Arbitration can invent missing doctrine.
- Arbitration commits state.

## Required non-mutating prototype
A non-mutating arbitration dry run covering compatible claims, direct conflict, incomparable claims, specificity partial orders, hidden claims, authorized choice, invalid authority, missing discovery completeness, and replay.

## Required artifacts
- AFQR-06 ADR
- claim and conflict schemas
- discovery receipt
- partial-order registry
- choice observability contract
- private and visible receipt schemas
- adversarial arbitration pack

## Blocked work
- universal numeric priority
- file-order precedence
- model-selected winners
- arbitration-owned mutation

## Work unlocked
- AFQR-07 conversion-validity claims
- AFQR-08 identity claims
- AFQR-09 revocation and successor claims

## Cross-question handoff
AFQR-06 determines which claims lawfully survive or combine; domain owners and AFQR-01 determine state consequences.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
