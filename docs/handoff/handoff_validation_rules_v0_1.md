# Handoff Validation Rules v0.1

## Hard invariants
1. Every source page has page truth.
2. Every content unit has a source page reference.
3. Every content unit has a readiness class.
4. Every non-ready unit has queue/quarantine/failure reason.
5. Every mapped construct has exactly one lawful mapping outcome.
6. No `needs_repair` unit can become canon candidate.
7. No queued page/unit may be used for final conversion without repair result.
8. No donor stat/math/economy term may be promoted without doctrine owner.
9. Every map-dependent unit has map validation status.
10. Every table-dependent unit has table normalization status.

## Strict contract checks
- Envelope files must exist and validate against v0.1 schemas.
- Enumerated fields must use contract enums (no free-form substitutes).
- Queue references must point to allowed queue names only.
- `conversion_permission` and `canon_permission` must be consistent with readiness.
