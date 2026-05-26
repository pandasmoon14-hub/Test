# PREA01-001 Control Layer Patch v0.1

## Patch intent
Introduce a pre-A01 control layer clarification that locks governance posture **before** A01 drafting pressure expands.

## Scope
- Add A00 control file establishing mechanical non-adoption posture.
- Preserve A01 as `A01_cosmology_and_dimensional_architecture.md`.
- Preserve K01 as `K01_lexicon_governance_and_reserved_terms.md`.
- Add explicit tracking record `PREA01-001` in registry control layer metadata.

## Full control spine requirements
- **Lexicon status gate**: lexicon-control entries route to K01/pre-A01 ledgers and work orders, not direct A01 renumbering.
- **Term status lifecycle**: terms remain candidate -> reviewed -> accepted/rejected only through K01-governed process.
- **Source-local record**: preserve donor provenance without granting doctrine authority.
- **Rejected import record**: explicitly capture donor constructs denied authority.
- **Reserved term family**: reserved naming families remain K01-governed and cannot be silently promoted.
- **Tag namespace separation**: mapping/status tags and reserved-term tags remain distinct namespaces.
- **State mutation gate**: no runtime/state mutation authority is introduced by this patch.
- **State-change digest**: state-change digest is a report generated from committed backend events and is **not authoritative state** by itself.
- **Actor state ledger**: actor updates require ledger-backed committed events in runtime layers, not control-layer memo promotion.
- **Hidden-information boundary**: hidden-information constraints remain runtime/canon boundary rules and are not overridden here.

## Non-goals
- No renaming of A01.
- No migration of lexicon governance into A01.
- No schema/runtime/training promotion changes.
- No implementation of runtime Gate B.

## Constraints
- This is a control/governance patch only.
- Existing layer/phase gates remain in force.
- Downstream doctrine cannot infer mechanical adoption from extraction/conversion readiness.
- Registry records for A00/PREA01 are tracking/work-order records, not canon or accepted terms.

## Effective date
- 2026-05-26
