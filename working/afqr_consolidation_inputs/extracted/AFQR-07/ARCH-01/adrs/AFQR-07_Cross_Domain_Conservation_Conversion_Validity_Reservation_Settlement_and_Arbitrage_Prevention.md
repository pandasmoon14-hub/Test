# AFQR-07 - Cross-Domain Conservation, Conversion Validity, Reservation, Settlement, and Arbitrage Prevention

**Selected architecture:** Typed Balance-Domain Flow Ledger with Proof-Carrying Conversion and Atomic Settlement  
**Ratification status:** `ratified_architecture_not_implementation_authority`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines how Astra validates stock, flow, capacity, throughput, costs, production, destruction, conversion, amplification, copying, reservation, settlement, and arbitrage across heterogeneous donor systems without a universal value currency.

## Central law
> Every mechanically relevant quantity belongs to a registered typed balance domain with explicit dimensions, balance class, source, sink, transformer, capacity, and exact arithmetic policy. Cross-domain conversion requires a proof-carrying manifest. Authorization and reservation occur before uncertain resolution; capture, release, loss, refund, byproduct, and liability disposition settle atomically through AFQR-01. No ledger balance, market price, entity ID change, or model-proposed ratio can substitute for conversion validity.

## Universal components
- Typed quantity and balance-domain registry.
- Stock, flow, source, sink, transformer, loss, and byproduct grammar.
- Balance classes for conserved, replenishable, capacity, throughput, debt, issued, non-rival, qualitative, and source-local unbounded domains.
- Commensurability and fungibility rules.
- Proof-carrying conversion manifests with exact ratios and conditions.
- Authorization, reservation, escrow, capture, release, refund, and settlement separation.
- Exact arithmetic, rounding, residual, and canonical unit policies.
- Static conversion-cycle and runtime contextual arbitrage analysis.
- Action-opportunity and cooldown containment.
- Cross-owner settlement fragments and receipts.

## Core contracts
- `BalanceDomainDefinition`
- `TypedQuantity`
- `ResourceStockState`
- `ResourceFlowProposal`
- `SourceSinkDeclaration`
- `ConversionManifestDefinition`
- `ConversionValidityProof`
- `ReservationRecord`
- `SettlementPlan`
- `SettlementReceipt`
- `ArbitrageAnalysis`
- `ExactArithmeticPolicy`
- `CapacityAndThroughputState`

## Determination or execution pipeline
1. classify quantity and balance domain
2. validate commensurability and source/sink law
3. select a registered conversion manifest
4. run static and contextual feasibility
5. authorize and reserve required stocks or capacity
6. resolve uncertainty under AFQR-02 and AFQR-04
7. revalidate post-resolution quantities and identity-sensitive counts
8. prepare owner settlement fragments
9. commit atomic settlement through AFQR-01
10. audit reachable gain cycles and residuals

## Ratified constraints and amendments
- Conservation is separate from accounting; a balanced ledger does not prove a lawful source or sink.
- Quantitative state is separate from qualitative or categorical state.
- Stock, capacity, occupancy, and throughput are separate constructs.
- Market price is not conserved value.
- Entitlement to create or request is not an instantiated asset.
- Duplication, delegation, proxy manifestation, and capability copying are separate operations.
- Reservation is not settlement, escrow, payment, or final consumption.
- Static cycle safety and contextual runtime safety are separate certifications.
- Floating-point arithmetic is prohibited for authoritative settlement unless a domain explicitly defines an exact encoded representation.
- Rounding and residual disposition are canonical and cannot be selected opportunistically.
- Action economy, cooldowns, and opportunities remain profile-local; they are not one universal resource.
- Information and other non-rival constructs require non-rival balance classes rather than fake material conservation.
- Source-local infinite or unbounded sources remain namespaced and cannot leak into other balance domains without certified bridges.
- Mass instantiation requires explicit entity-count, capacity, source, upkeep, and dependency handoffs.
- A model cannot create a conversion ratio or waive conversion validity.

## Guarantees
- Typed quantity domains.
- Explicit lawful sources and sinks.
- Proof-carrying conversion.
- Reservation and settlement separation.
- Exact arithmetic.
- Arbitrage analysis.
- Atomic cross-owner settlement.

## Non-guarantees
- Universal energy or value.
- Strict conservation for every domain.
- Market equilibrium.
- Automatic identity of copied assets.
- Automatic dependency survival.
- Automatic lawful creation from source-local infinity.

## Required non-mutating prototype
A non-mutating quantity and settlement dry run covering strict conservation, replenishment, capacity, throughput, debt, byproducts, catalysts, refunds, partial success, rounding, conversion cycles, action-opportunity laundering, source-local infinity, and familiar mass-instantiation pressure.

## Required artifacts
- AFQR-07 ADR
- balance-domain registry
- quantity and conversion-manifest schemas
- reservation and settlement contracts
- exact arithmetic policy
- arbitrage analysis pack
- source-local unbounded-domain containment contract

## Blocked work
- universal value currency
- numeric-field compatibility
- model-generated ratios
- free duplication
- floating-point settlement

## Work unlocked
- identity-sensitive no-progress comparison in AFQR-08
- reservation and liability handoffs in AFQR-09

## Cross-question handoff
AFQR-07 determines quantity, capacity, conversion, and settlement validity; AFQR-08 determines entity relations and AFQR-09 determines ongoing dependencies.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
