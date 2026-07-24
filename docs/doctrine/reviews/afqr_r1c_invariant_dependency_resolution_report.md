# AFQR-01–20 R1C invariant and dependency resolution report

## Baseline and authority

- Verified base SHA used for this R1C branch: `12ec32803f93ca5d0a70a8f245545932387be9e6`.
- `git fetch origin main` was attempted before edits but the execution environment returned `CONNECT tunnel failed, response 403`; the local repository already matched the last independently verified merged baseline.
- R1B remains complete. R1C is the only authorized next gate. R1D becomes ready only after R1C acceptance and is not complete here.
- This report and the primary R1C artifact grant no runtime, conversion, canon/sourcebook, model-facing, narration, live-play, RT-002G, or temporary-evidence deletion authority.

## Source use

R1C uses current repository doctrine first, then the R1B vocabulary artifact, R1A authority/dependency/collision records, and selected primary AFQR source paths recorded in the authority index. Temporary AFQR inputs remain evidence only and are not repository authority.

## Decisions recorded

- Every R1A dependency edge from `DEP-001` through `DEP-094` receives exactly one R1C disposition in the primary artifact.
- Every disposition preserves producer/consumer direction, source evidence identifiers, non-transfer of ownership, unavailable-input behavior, and hidden-information containment.
- Revocation, invalidation, and cascading consequences are recorded as `not_defined_at_r1c` where source evidence does not establish a general rule.

## Cycle-risk resolution summary

- `AFQR-01 / AFQR-09`: bounded feedback; transition commitment and relation/dependency ownership remain separate.
- `AFQR-02 / AFQR-04`: exact edges `DEP-021` (`command_lifecycle`) and `DEP-024` (`time_causality`) use phase ordering. AFQR-02 retains command identity/lifecycle ownership and AFQR-04 retains logical-time/causal-order ownership; scheduling neither creates command identity nor transfers time ownership.
- `AFQR-06 / AFQR-08`: exact edges `DEP-048` (`claim_evidence`) and `DEP-052` (`identity_evidence`) use bounded feedback. AFQR-06 retains claim/admissibility/arbitration ownership and AFQR-08 retains identity/continuity ownership; identity assertions cannot self-certify and claim admission cannot create identity.
- `AFQR-17 / AFQR-18`: exact edges `DEP-089` and `DEP-091` use bounded feedback; environmental process and spatial topology constrain each other without recursive ownership.
- Additional R1A `review_required` pairs involving AFQR-09 (`DEP-022/062`, `DEP-028/063`, `DEP-049/064`, and `DEP-054/066`) are explicitly classified as dependency risks outside the four recorded reciprocal cycle groups; each has one bounded non-recursion treatment.

## Missing substrate summary

R1C classifies each missing substrate independently: governed relations preserve dependency/obligation/revocation/jurisdiction/social boundaries; bitemporal truth/evidence preserves observation, epistemic, time, and hidden-truth boundaries; the owner-reducer journal preserves commitment/recovery/replay/command/causal boundaries; the AFQR-05 bridge hypergraph preserves typed compatibility; and five separate domain-owner contract requirements preserve spatial, signal, embodiment, institutional, and social ownership. None authorizes schemas, runtime services, persistence, conversion behavior, bridge code, or production imports.

## Ownership correction

`DEP-094` now carries an AFQR-20 detected-contact/observation reference into AFQR-19 target construction: AFQR-20 retains sensing/contact semantics, AFQR-19 retains `TERM-011 target`, and detection alone is not a valid target. Every edge now includes R1B term bindings; qualified-family references name the exact qualified form and owner.

## Preserved escalations

`COLL-03`, `COLL-08`, and `COLL-10` remain open. R1C records safe interim handoffs and prohibited assumptions only.

## Corpus-scale pressure finding

The dependency grammar was checked against the required 200–400-source pressure families. R1C provides lawful landing points or escalations and does not promote a single cosmology, anatomy, identity model, action economy, resolution style, progression model, resource economy, spatial topology, sensing model, legal/social system, actor scale, or vehicle/operator relationship.
