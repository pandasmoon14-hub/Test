# Astra Framework Ingestion Pack v0.1

This pack turns Stages 1-3 into machine-usable AstraCloud assets.

It does four things:

1. Seeds canonical lexicon control files from the RHBF-derived Astra chassis.
2. Creates provisional queues for unstable or disputed mappings.
3. Writes canon candidate and canon conflict packets for human adjudication.
4. Adds route-aware conversion and validation guidance so future sourcebook ingestion stays aligned with the emerging Astra framework.

## Source basis

This pack is based on three prior distilled stages already produced for AstraCloud:
- Stage 1: Core Chassis
- Stage 2: World Activity Engine
- Stage 3: Creature and Gear Framework

## Intended install locations

- `data/lexicon/canonical/`
- `data/lexicon/provisional/`
- `data/canon/candidates/`
- `data/canon/conflicts/`
- `configs/routing/`
- `configs/validation/`
- `review/human_queues/lexicon_review/`
- `review/human_queues/conflict_review/`

## Immediate usage rule

During conversion runs:
- canonical lexicon files are read-only inputs
- provisional lexicon files receive extracted candidates and uncertain mappings
- canon candidates are reference outputs for synthesis
- canon conflicts are review-required and should never be silently resolved in code
