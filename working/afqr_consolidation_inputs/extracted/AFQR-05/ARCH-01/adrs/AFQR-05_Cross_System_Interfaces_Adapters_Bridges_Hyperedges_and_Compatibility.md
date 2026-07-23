# AFQR-05 - Cross-System Interfaces, Adapters, Bridges, Hyperedges, and Compatibility

**Selected architecture:** Registered Typed Interface-and-Bridge Hypergraph  
**Abbreviation:** `RTIBH`  
**Ratification status:** `ratified_with_mandatory_amendments`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines how independently owned Astra systems interact without pairwise integration sprawl, universal effect records, direct cross-owner mutation, or donor-specific assumptions becoming hidden law.

## Central law
> Cross-system interaction exists only through registered typed interfaces and versioned bridge definitions. Adapters transform representations but do not mutate or create authority. A bridge may connect several semantic participants through a hyperedge, but compatibility never implies permission, success, identity, quantity validity, or dependency survival.

## Universal components
- Interface-definition registry.
- Bridge-definition and bridge-instance registry.
- Typed semantic slots and participant roles.
- Pure adapter registry.
- Multi-party hyperedge support.
- Applicability and compatibility predicates.
- Version pinning and bridge certification.
- Source-local export and import boundaries.
- Persistent relationship ownership separation.
- Bridge discovery and completeness receipts.

## Core contracts
- `InterfaceDefinition`
- `InterfaceOccurrence`
- `BridgeDefinition`
- `BridgeInstance`
- `SemanticSlot`
- `BridgeParticipant`
- `PureAdapterDefinition`
- `CompatibilityResult`
- `BridgeDiscoveryReceipt`
- `BridgeCertificationReceipt`
- `SourceLocalExportContract`

## Determination or execution pipeline
1. identify required semantic slots
2. discover registered interfaces
3. discover applicable bridges
4. validate participant compatibility and versions
5. run pure adapters
6. freeze bridge occurrence and participants
7. route resulting claims and handoffs to AFQR-06 through AFQR-09
8. commit only owner-prepared fragments through AFQR-01

## Ratified constraints and amendments
- Interfaces, adapters, bridges, and persistent relationships are different artifact classes.
- A bridge occurrence is contextual; a bridge definition is reusable law.
- Adapters are total or explicitly partial, deterministic, versioned, and non-mutating.
- A bridge may expose capability or compatibility but cannot manufacture authority.
- No pairwise integration matrix is required; typed semantic slots permit reusable many-party composition.
- Persistent relationship state has exactly one relationship owner.
- Bridge discovery must be complete for the frozen registered scope.
- Source-local bridges remain namespaced and require certified export contracts for cross-package use.
- Generic effect payloads and executable metadata are prohibited.
- Bridge fingerprints are verification aids and do not prove semantic equivalence.

## Guarantees
- Typed cross-system composition.
- Reusable bridge architecture.
- Pure adapters.
- Multi-party interaction.
- Source-local containment.
- No direct cross-owner mutation.

## Non-guarantees
- Compatibility means legality.
- A bridge determines conflict precedence.
- A bridge settles quantities.
- A bridge determines identity or dependency consequences.
- Every donor subsystem receives a core bridge.

## Required non-mutating prototype
A bridge-discovery and composition dry run covering direct interfaces, adapters, multi-party hyperedges, version mismatch, missing bridges, source-local exports, hidden participants, and no-authority compatibility.

## Required artifacts
- AFQR-05 ADR
- interface and bridge registries
- adapter purity contract
- bridge certification protocol
- source-local export contract
- cross-domain fixture pack

## Blocked work
- direct subsystem callbacks
- universal effect soup
- pairwise hard-coded integration as doctrine
- uncertified source-local bridge export

## Work unlocked
- AFQR-06 typed claims
- AFQR-07 cross-domain conversions
- AFQR-08 identity-sensitive bridges
- AFQR-09 governed relations

## Cross-question handoff
AFQR-05 proves a lawful interaction route exists; it does not decide the authoritative outcome.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
