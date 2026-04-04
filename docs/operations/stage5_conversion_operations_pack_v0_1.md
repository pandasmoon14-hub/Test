# Stage 5 — Conversion Operations Pack v0.1

This stage turns the AstraCloud framework from a distilled design archive into an operational conversion system.

## Mission

Provide reusable run assets so future sourcebooks can be converted through the same spine rather than by one-off manual interpretation.

## What this stage defines

- sourcebook profiles to bias conversion behavior
- chunk-type conversion rules by route and content class
- lexicon extraction packet structure
- canon conflict packet structure
- validator failure packet structure
- run summary report structure

## Operating stance

1. Preserve function before flavor.
2. Prefer Astra-native reinterpretation over source-label mimicry.
3. Do not auto-canonize unstable mappings.
4. Route tables and stat blocks conservatively.
5. Every run must emit lexicon deltas and conflict candidates, even if empty.
6. Validator failures should generate review packets, not silent overrides.

## Initial profile set

- `cultivation_primary.yaml`: for texts mechanically close to RHBF or other cultivation-forward systems.
- `hybrid_scifi_fantasy.yaml`: for mixed tech-plus-metaphysics donor systems.
- `tactical_d20_conversion.yaml`: for cleaner class/feat/gear combat systems.

## Recommended run order for a new donor book

1. normalize markdown
2. chunk and classify
3. assign route per chunk
4. convert by profile plus route rules
5. run validators
6. emit lexicon delta packet
7. emit canon conflict packet(s)
8. generate run summary
9. review escalated chunks
