# D01-03 Multi-Axis Breakthrough Lattices

## Purpose

This file defines D01’s attribute breakthrough substrate.

## Core rule

Each visible attribute may have an independent threshold lattice. Breakthroughs are not automatically whole-character level-ups.

The seven visible breakthrough lattices are:

- Vessel lattice;
- Finesse lattice;
- Reason lattice;
- Insight lattice;
- Integrity lattice;
- Glamour lattice;
- Animus lattice.

Pneuma has no ordinary breakthrough lattice.

## Breakthrough lattice fields

Each visible attribute may track:

```yaml
attribute_breakthrough_lattice:
  attribute_ref: string
  current_value: string
  threshold_state: string
  breakthrough_eligibility: string
  breakthrough_history: []
  post_breakthrough_altered_state: string
  owner_handoffs:
    D03: []
    D04: []
    D06: []
    D07: []
    D08: []
    D10: []
```

D01 defines the existence of these fields. D04 owns advancement gates, proof, and breakthrough procedure.

## Threshold state

Possible threshold states:

- stable;
- pressured;
- saturated;
- unstable;
- eligible;
- blocked;
- divergent;
- corrupted;
- transformed;
- source-local.

D07 owns corruption/harm outcomes. D08 owns actor/form changes. D04 owns advancement logic.

## Breakthrough history

Breakthrough history matters because long campaigns need path dependency.

Record:
- attribute;
- trigger;
- cost;
- consequence;
- owner handoffs;
- altered state;
- source-local boundary;
- historical retention.

D10 may record public breakthrough consequence if socially visible.

## Independent but interacting axes

Breakthrough axes are independent, but may interact.

Examples:
- Vessel breakthrough affects body capacity but not Reason automatically.
- Animus breakthrough may enable power carrier expansion if D03/D04 validate.
- Integrity breakthrough may stabilize a transformation if D07/D08 validate.
- Insight breakthrough may improve assessment potential if D02/D05 validate.
- Glamour breakthrough may affect faction presence or social legitimacy if D10 validates.

## Multi-axis breakthroughs

Rare breakthroughs may involve multiple attributes at once.

Examples:
- Vessel + Integrity body remolding;
- Reason + Insight revelation;
- Glamour + Animus command aura;
- Vessel + Animus cultivation body;
- Integrity + Pneuma-adjacent cosmic survival event, with Pneuma still hidden.

D04 owns whether this is allowed and how it is gated.

## Acceptance criteria

A breakthrough-lattice ruling is valid when it:

1. preserves independent visible attribute lattices;
2. excludes Pneuma from ordinary breakthrough;
3. records history and altered state;
4. routes advancement procedure to D04;
5. routes harm/transformation/world consequence to D07/D08/D10;
6. prevents one donor level system from replacing Astra thresholds.
