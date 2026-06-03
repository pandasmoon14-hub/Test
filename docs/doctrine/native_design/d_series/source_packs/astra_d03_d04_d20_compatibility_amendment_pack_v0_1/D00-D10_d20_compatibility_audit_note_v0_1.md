# D00–D10 D20 Compatibility Audit Note

Version: v0.1  
Status: Included audit note for D03/D04 amendment pack  
Generated: 2026-06-02

## Audit result

A compatibility pass across the generated D00–D10 doctrine packs found that the system is broadly compatible with the locked D02 d20-first architecture.

The primary issue was not a live 2d6 dependency. The primary issue was older D02 outcome terminology remaining in D03 and D04.

## Required amendments

### D03

D03 should replace older backlash-result labels such as:

- `Failure with Consequence`;
- `Severe Failure`;
- `Critical Failure`.

These should be read through the locked D02 states:

- Fractured;
- Receded;
- Sundered;
- natural 1 complication flag.

### D04

D04 should replace older breakthrough-result labels such as:

- `Critical Success`;
- `Exceptional Success`;
- `Clean Success`;
- `Partial Result`;
- `Mixed Result`;
- `Failure with Consequence`;
- `Severe Failure`;
- `Critical Failure`.

D04 should also replace older margin breakpoints such as:

- `Margin +5`;
- `Margin 0 to +4`;
- `Margin -4 to -7`;
- `Margin -8 or worse`.

These are superseded by:

| D02 outcome | Margin guide |
|---|---:|
| Ascendant | +10 or higher |
| Clear | 0 to +9 |
| Fractured | -1 to -4 |
| Receded | -5 to -9 |
| Sundered | -10 or lower |

## Non-blocking packaging notes

Before repo integration:

1. D03 should receive a machine-readable `D03_pack_manifest.json` or compatibility manifest.
2. D04’s nested ZIP folder layout should either be normalized or handled by directory-agnostic ingestion scripts.

These are packaging issues, not doctrine contradictions.

## D11 readiness after amendment

After applying this amendment pack, D11 may safely rely on:

- d20-first checks;
- Difficulty Number ladder;
- five-state margin outcomes;
- natural 20 as critical opportunity;
- natural 1 as complication flag;
- Fractured as success-at-cost;
- assessment may produce false/misread information;
- D02 routes deltas to D03–D10;
- D03 and D04 no longer rely on obsolete D02 lane names.
