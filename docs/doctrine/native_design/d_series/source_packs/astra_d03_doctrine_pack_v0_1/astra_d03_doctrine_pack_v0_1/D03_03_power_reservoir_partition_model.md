# Astra Ascension — D03-03 Power Reservoir and Partition Model

Status: design-draft / accepted architecture  
Layer: Native Design Phase / D03  
File ID: D03-03  
Version: v0.1  
Date: 2026-05-29

---

## 1. Purpose

This file defines how a character's Power Reservoir unlocks and how capacity is partitioned across integrated Power Economies.

Astra does not create a full separate pool for every Power Economy. A character has a shared Power Reservoir with partitions.

---

## 2. Core principle

A Vessel stabilizes a limited internal ecology of power. Adding economies expands versatility and confluence potential, but does not linearly multiply total fuel.

---

## 3. Reservoir unlock

A physically embodied mundane actor begins with:

- Health/Vital State;
- Endura;
- no non-baseline Power Reservoir.

When the actor integrates a first non-baseline Power Economy, the actor gains a Power Reservoir.

The first integrated economy becomes the Dominant Economy by default.

---

## 4. Shared reservoir

The Power Reservoir is shared across integrated non-baseline economies.

A second or third integrated economy adds fractional capacity, then the total reservoir is partitioned.

Additional economies do not create full independent resource pools.

---

## 5. Fractional capacity

D03 Phase 1 does not lock exact fractional values.

Accepted structure:

| Integrated non-baseline economies | Reservoir model |
|---:|---|
| 0 | No non-baseline Power Reservoir. |
| 1 | Base reservoir. |
| 2 | Base reservoir + secondary fraction. |
| 3 | Base reservoir + secondary fraction + tertiary fraction. |
| 4+ | Overlimit unless stabilized. |

A provisional testing scaffold may use:

| Integrated economies | Test total |
|---:|---:|
| 1 | 100% |
| 2 | 150% |
| 3 | 175% |

This scaffold is not final balance math.

---

## 6. Partition roles

### Dominant Economy

The Dominant Economy is the actor's main power identity.

Typical traits:

- best efficiency;
- deepest expression access;
- strongest recovery;
- easiest refinement;
- most stable cost profile;
- best default expression route.

### Secondary Economy

The Secondary Economy is a reliable alternate route.

Typical traits:

- moderate efficiency;
- strong versatility;
- enables fusion;
- supports re-authoring;
- may require more training for deep expressions.

### Tertiary Economy

The Tertiary Economy is usually support, stabilizer, catalyst, niche specialization, containment, or risky expansion.

Typical traits:

- lower default efficiency;
- high value in confluence;
- may stabilize, anchor, contaminate, amplify, or transform expressions;
- may enable rare expression behavior.

Tertiary must not be designed as useless. Its value is often qualitative rather than raw capacity.

---

## 7. Default role assignment

| Integration order | Default role |
|---:|---|
| First integrated economy | Dominant |
| Second integrated economy | Secondary |
| Third integrated economy | Tertiary |
| Fourth or later | Overlimit unless special support exists |

---

## 8. Advanced allocation

Player-directed allocation exists as an advanced customization rule, not the default.

Advanced allocation may be unlocked through:

- training;
- path doctrine;
- domain mastery;
- breakthrough;
- relic/implant scaffolding;
- Scrypta recalibration;
- Isotra harmonization;
- Aethra anchoring;
- Reticula offload;
- source-local method;
- controlled experimentation.

Advanced allocation may allow:

- dominant role reassignment;
- unequal partitioning;
- temporary partition shifting;
- dynamic partition based on rest or ritual;
- path-defined ratios;
- experimental unstable partitions;
- domain-dependent partitions.

---

## 9. Partition shifting

Partitions cannot be freely shifted during ordinary action by default.

Valid partition-shift procedures include:

- rest;
- meditation;
- training;
- maintenance;
- ritual;
- breakthrough;
- domain alignment;
- path technique;
- relic/implant recalibration;
- source-local transformation;
- recovery treatment;
- controlled experimentation.

Unsafe or rushed shifting may create:

- instability;
- partition leakage;
- adverse posture;
- misfire risk;
- slot strain;
- carrier degradation;
- overdraw;
- threshold pressure.

---

## 10. Fusion draw rules

D03 Phase 1 does not lock exact cost draw values. It does lock the structure:

- a single-economy Expression draws from one partition;
- a dual-economy Expression draws from primary and secondary partitions;
- a triadic Expression may draw from primary, secondary, and stabilizer/catalyst partitions;
- external economies may provide charge, anchor, substitution, or risk rather than internal spend;
- overlimit economies may draw with increased instability or backlash.

---

## 11. Example progression

### Mundane actor

```yaml
baseline:
  health: tracked
  endura: tracked
integrated_economies: []
power_reservoir: none
```

### One integrated economy

```yaml
integrated_economies:
  - Zi
power_reservoir:
  total_capacity: base
  roles:
    dominant: Zi
  partitions:
    Zi: 100%
```

### Two integrated economies

```yaml
integrated_economies:
  - Zi
  - Calora
power_reservoir:
  total_capacity: base + secondary_fraction
  roles:
    dominant: Zi
    secondary: Calora
  partitions:
    Zi: dominant_share
    Calora: secondary_share
```

### Three integrated economies

```yaml
integrated_economies:
  - Zi
  - Calora
  - Scrypta
power_reservoir:
  total_capacity: base + secondary_fraction + tertiary_fraction
  roles:
    dominant: Zi
    secondary: Calora
    tertiary: Scrypta
```

---

## 12. Conversion implications

Donor systems with multiple resource pools should not automatically become multiple full Astra pools.

Possible mappings:

- one donor pool -> one integrated economy partition;
- two donor resource systems -> Dominant/Secondary economies;
- hybrid class resources -> confluence or advanced allocation;
- prepared charges -> Scrypta/external carrier/prepared pattern;
- heat/stress/corruption -> cost channel, overdraw, instability, or specific economy route;
- donor spell slots -> expression retention or cost structure, not automatic Astra pool.
