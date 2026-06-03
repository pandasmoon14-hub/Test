# Astra Ascension — D03-01 Power Economy Lattice

Status: design-draft / accepted architecture  
Layer: Native Design Phase / D03  
File ID: D03-01  
Version: v0.1  
Date: 2026-05-29

---

## 1. Purpose

This file defines Astra's Power Economy Lattice.

A Power Economy is a distinct logic of power: where power comes from, how it is held, how it is spent, what it risks, how it recovers, how it interacts with other economies, and what kind of Expressions it can author or re-author.

Astra does not use one universal mana pool. Astra does not use a fixed set of seven attribute pools. Astra uses many viable power economies arranged into a governed lattice.

---

## 2. Core principle

Power in Astra is ecological, bodily, conceptual, technological, spiritual, social, causal, corruptive, and environmental. Characters do not merely spend points. They route power through economies, and each economy carries distinct costs, recoveries, risks, and expression behaviors.

---

## 3. Naming register

D03 uses a Classical Distortion naming register for working Astra-native Power Economy names.

Naming style:

- clipped, archaic, semi-Latin/Greek register;
- mostly single-word substances or forces;
- no compound "Current / Charge / Flow" constructions as core names;
- phonetically close enough to source pressure to remain learnable;
- distinct from locked attributes such as Vessel, Finesse, Reason, Insight, Integrity, Glamour, Animus, and Pneuma.

All names are lexicon-provisional until formally promoted.

---

## 4. Power Economy Register

| # | Economy | Source pressure | Core economy identity | Likely availability |
|---:|---|---|---|---|
| 1 | Mistra | Mana | Adaptable ambient power absorbed, stored, and shaped internally. | Common / trained |
| 2 | Xakra | Chakra | Body-mind pathway force routed through aligned internal channels. | Trained |
| 3 | Zi | Ki/Qi | Cultivated life force refined through breath, discipline, and circulation. | Common / trained |
| 4 | Essar | Essence | Conceptual force tied to personal, cosmic, or local principles. | Advanced |
| 5 | Tellura | Worldsoul | Ecological or planetary life-current carrying local memory and environmental consequence. | Rare / domain-bound |
| 6 | Endura | Stamina/Endurance | Baseline embodied exertion capacity and fatigue buffer. Does not count against Vessel economy tolerance. | Starter / baseline |
| 7 | Volith | Willpower/Focus | Mental fortitude, concentration, intent pressure, and psychic endurance. | Starter / trained |
| 8 | Fideth | Faith/Devotion | Conviction-powered force tied to vows, doctrine, communion, or communal resonance. | Trained / source-local |
| 9 | Sangua | Vital/Blood Force | Biological sacrifice, lineage resonance, blood-price, and life-fluid expenditure. | Restricted / risky |
| 10 | Aethra | Aether/Ether | Primordial substrate for spatial, realm, enchantment, or permanence effects. | Rare / advanced |
| 11 | Phasma | Spirit/Ectoplasm | Consciousness residue, spirit projection, memory echo, and presence-binding. | Trained / source-local |
| 12 | Noetis | Psionic/Cognitive Energy | Neural or cognitive workload converted into force, perception, or remote influence. | Trained |
| 13 | Scrypta | Inscription/Script | Power stored in prepared symbols, marks, scripts, circuits, patterns, or encoded forms. | Trained / craft-linked |
| 14 | Pressa | Spiritual Pressure/Aura Weight | Density of energetic selfhood used for suppression, deterrence, or amplification. | Advanced |
| 15 | Impeta | Momentum/Flow | Compounding rhythm built through uninterrupted action sequences. | Starter / martial |
| 16 | Calora | Thermal/Heat Exchange | Power drawn from heat differential, cooling, combustion, or phase regulation. | Trained / tech-linked |
| 17 | Sympathis | Resonance/Frequency | Synchronization with matter, allies, structures, domains, frequencies, or patterns. | Trained |
| 18 | Vacuus | Void/Entropy | Decay, negation, absence, erasure, and dissolution pressure. | Rare / dangerous |
| 19 | Sortis | Probability/Luck | Probabilistic pressure, improbable openings, critical manipulation, and fate drift. | Rare / restricted |
| 20 | Mnemora | Memory/Knowledge Archive | Stored experience, memory sacrifice, inherited knowledge, and recalled pattern access. | Trained / risky |
| 21 | Isotra | Equilibrium/Harmony | Stabilizing force maintained between opposites; restorative, balancing, harmonizing. | Trained |
| 22 | Vitia | Corruption/Taint | Degenerative power accumulated through forbidden, hostile, unstable, or contaminating sources. | Restricted / risky |
| 23 | Reticula | Grid/Network Lattice | Distributed computational, energetic, infrastructural, or systemic-access economy. | Tech-linked / setting-dependent |
| 24 | Karmax | Karma/Causal Weight | Accumulated consequence, reciprocity, merit, debt, and delayed trajectory pressure. | Rare / source-local |
| 25 | Ventra | Breath/Respiratory Cycle | Rhythmic power generated through inhalation, exhalation, pacing, and bodily timing. | Starter / trained |
| 26 | Strata | Stress/Tension | Reactive force generated through pressure, fear, injury, emotion, or physical tension. | Starter / risky |
| 27 | Scintilla | Spark/Ignition | Catalytic burst power; creative or destructive ignition with all-or-nothing expenditure. | Rare / build-defining |

---

## 5. Removed core economy

| Removed economy | Status |
|---|---|
| Aevit / Chrono / Temporal | Removed as standalone D03 Power Economy. Temporal effects may exist through other routes, but Astra does not define a core temporal resource economy in D03. |

Temporal constructs may route through:

- Karmax, for causal debt, reciprocity, or delayed consequence;
- Sortis, for probability drift and improbable timing;
- Aethra, for realm, distance, spatial boundary, or permanence effects;
- Scrypta, for delayed, triggered, encoded, or stored effects;
- Mnemora, for memory, past-pattern reconstruction, or experience echo;
- source-local phenomena, relics, sites, or entities.

---

## 6. Availability bands

No economy is antagonist-only.

| Band | Meaning |
|---|---|
| Starter | Can appear during basic character creation. |
| Baseline | Present in most embodied actors by default. |
| Common / trained | Available through ordinary training, path, competency, or doctrine. |
| Advanced | Requires threshold, breakthrough, rare teacher, technique, faction, or specialized path. |
| Rare | Exists, but is campaign-shaping or uncommon. |
| Restricted | Dangerous, regulated, taboo, difficult to stabilize, or permission-locked. |
| Risky | Available but carries high backlash, instability, corruption, or degradation risk. |
| Domain-bound | Stable only in aligned places, planes, regions, sanctums, cultures, or domains. |
| Tech-linked | Requires infrastructure, tools, implants, networks, devices, or platforms. |
| Craft-linked | Requires preparation, construction, inscription, calibration, or maintained forms. |
| Source-local | Valid in a bounded conversion, region, faction, species, relic, campaign, or setting context. |
| Hidden | Backend/narrator-facing; not normally player-readable. |

Threats may use restricted, rare, hidden, dangerous, or source-local economies, but those economies remain part of the same lattice.

---

## 7. Power Economy Record

Every Power Economy should be representable with a record like this:

```yaml
power_economy_record:
  economy_id: string
  astra_name: string
  source_pressure: string
  source_family:
    - internal
    - external
    - environmental
    - conceptual
    - social
    - temporal_effect_only
    - technological
    - biological
    - cosmic
    - corruptive
  storage_mode:
    - pool
    - reserve
    - rhythm
    - charge
    - mark
    - debt
    - alignment
    - saturation
    - prepared_pattern
    - ambient_access
  spend_pattern:
    - burst
    - sustained
    - reserve
    - sacrifice
    - conversion
    - buildup
    - trigger
    - wager
    - decay
    - front_loaded
  recovery_pattern:
    - rest
    - breath
    - meditation
    - environment
    - worship
    - repair
    - feeding
    - cooling
    - discharge
    - randomness
    - milestone
    - purification
    - network_restore
  primary_uses: [string]
  primary_risks: [string]
  failure_modes: [string]
  interaction_tags: [string]
  fusion_behavior:
    - stabilizer
    - amplifier
    - catalyst
    - contaminant
    - converter
    - anchor
    - volatile
    - parasitic
    - harmonizer
    - nullifier
  likely_attribute_links: [string]
  visibility: starter | common | trained | restricted | rare | hidden | source_local
  availability_bands: [string]
```

---

## 8. Interaction grammar

Power Economies may interact through the following patterns.

| Interaction | Meaning |
|---|---|
| Parallel use | Two economies are spent separately for one action. |
| Substitution | One economy can pay a cost normally paid by another. |
| Conversion | One economy is transformed into another at a cost, loss, or risk. |
| Catalysis | One economy triggers, ignites, accelerates, or enables another. |
| Stabilization | One economy reduces instability, backlash, corruption, or misfire risk from another. |
| Amplification | One economy increases output, support dice, intensity, scope, or bandwidth of another. |
| Interference | Two economies conflict and impose adverse posture, cost increase, misfire, or instability. |
| Contamination | One economy stains another, adding Vitia, trace, decay, debt, or identity pressure. |
| Anchoring | One economy gives duration, containment, permanence, position, or environmental attachment to another. |
| Discharge | Excess load vents through environment, item, body, relationship, or world state. |
| Cascade | A failed interaction triggers secondary effects across linked economies. |
| Confluence | Two or more economies fuse into a distinct hybrid expression. |

---

## 9. Fusion limit

A standard internal fused Expression should use:

- one primary economy;
- one optional secondary economy;
- one optional stabilizer or catalyst.

This aligns with the soft three-economy Vessel tolerance.

More than three economies can appear in rituals, artifacts, places, faction projects, world events, or external systems, but a standard Vessel should not safely internalize more than three without overlimit pressure or special support.

---

## 10. Conversion implications

Donor resource names do not decide Astra economy names. Conversion should identify function:

- source of power;
- storage mode;
- spend pattern;
- recovery method;
- risk/failure mode;
- whether the construct is internal, external, prepared, borrowed, ambient, or source-local;
- whether the donor concept maps to a Power Economy, Expression, carrier, cost channel, or source-local phenomenon.

Donor exact math remains evidence only.
