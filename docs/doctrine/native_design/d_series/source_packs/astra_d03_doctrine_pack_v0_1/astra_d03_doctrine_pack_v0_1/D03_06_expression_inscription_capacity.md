# Astra Ascension — D03-06 Expression Inscription, Capacity, and Carrier Tolerance

Status: design-draft / accepted architecture  
Layer: Native Design Phase / D03  
File ID: D03-06  
Version: v0.1  
Date: 2026-05-29

---

## 1. Purpose

This file defines how Astra tracks known Expressions, retained Expressions, Expression Burden, Carrier Tolerance, inscription carriers, slot condition, and replacement/degradation.

Expressions are not freely swappable equipment. They are patterns held by a Vessel, Animus, mind, economy partition, script, relic, tool, domain, companion, platform, or other valid carrier.

---

## 2. Core principle

Knowing an Expression is not the same as retaining it.

Retaining an Expression is not the same as safely using it.

Using an Expression is not the same as mastering it.

A character can know, observe, theorize, study, copy, or learn many Expressions, but can retain only a limited active set through valid carriers.

---

## 3. Knowledge states

| State | Meaning |
|---|---|
| Unknown | Actor has no knowledge. |
| Known-of | Actor has heard of it. |
| Observed | Actor has seen it used. |
| Understood | Actor roughly understands what it does. |
| Theorized | Actor has a possible route. |
| Studied | Actor has begun structured learning. |
| Copied | Actor has incomplete or unstable pattern. |
| Learned | Actor knows the method. |
| Retained | Actor has stored it in a carrier. |
| Inscribed | Actor has stabilized it in a valid slot/carrier. |
| Functional | Actor can use it in ordinary play. |
| Refined | Actor uses it more safely or efficiently. |
| Mastered | Actor can adapt, teach, re-author, or use under pressure. |
| Lost | Actor no longer has working access. |

---

## 4. Expression Burden

Expression Burden is the retention pressure an Expression places on its carrier.

Burden sources include:

| Burden source | What it captures |
|---|---|
| Grade burden | Higher-grade Expressions require more retention structure. |
| Scope burden | Larger range, area, duration, autonomy, summoning, banishing, traversal, or persistence increases burden. |
| Flag burden | Lethal, recursive, autonomous, causal, corruptive, agency-denying, no-common-counter, or irreversible flags increase burden. |
| Economy-route burden | Rare, restricted, corruptive, volatile, or external economies may be harder to retain. |
| Multi-economy burden | Split-cost/confluence Expressions pressure multiple partitions or carriers. |
| Stability burden | Experimental or unstable Expressions burden more than refined/mastered ones. |
| Carrier mismatch burden | Poor carrier fit increases burden. |
| Kinform burden | Some kinforms/species/races retain some Expression families better or worse. |
| Path/domain burden | Aligned path/domain may reduce burden; opposed path/domain may increase it. |
| Cognitive burden | Formula-heavy, predictive, memory-heavy, or multi-stage Expressions strain cognitive carriers. |
| Animus burden | Identity, power-source, spirit, or cultivation Expressions strain Animus carriers. |
| Vessel burden | Body, breath, blood, organ, pathway, or endurance Expressions strain the Vessel. |
| Maintenance burden | Recalibration, feeding, prayer, repair, breathwork, exposure, or upkeep. |
| Secrecy/trace burden | Hidden, masked, forbidden, or trace-avoiding Expressions require additional complexity. |
| Volatility burden | Backlash, instability, corruption, critical-failure volatility. |
| External dependency burden | Reliance on relics, anchors, entities, networks, locations, factions. |
| Replacement history burden | Repeated overwriting makes later retention harder. |
| Scar burden | Prior slot scars alter burden, sometimes reducing one family and increasing another. |

Exact burden formulas are deferred.

---

## 5. Carrier Tolerance

Carrier Tolerance is how much Expression Burden a carrier can safely hold.

Tolerance sources include:

| Tolerance source | What it modifies |
|---|---|
| Vessel structure | Embodied, breath, blood, kinetic, pathway Expressions. |
| Integrity | Resistance to degradation, corruption, identity fracture, carrier collapse. |
| Animus | Power-source identity, cultivation force, spiritual retention. |
| Reason | Formula retention, structured learning, Scrypta logic, multi-step Expressions. |
| Insight | Perceptual, diagnostic, hidden-state, resonance, assessment-heavy Expressions. |
| Glamour | Social, illusion, presence, perception-shaping, performance, reality-adjacent retention. |
| Finesse | Tempo, motion, precision, sequencing, Impeta, kinetic Expressions. |
| Endura conditioning | Physical expression tolerance and overexertion resistance. |
| Kinform/species/race | Natural carrier structures and incompatibilities. |
| Culture/tradition | Learned inscription practices and safe replacement methods. |
| Path/archetype/profession | Specialized carrier support and lawful routes. |
| Domain alignment | Reduces burden or increases tolerance for aligned Expressions. |
| Breakthrough state | Expands, transforms, repairs, or destabilizes tolerance. |
| Economy role | Dominant economy supports deeper retention; tertiary supports niche/stabilizing retention. |
| Relic/tool/implant scaffold | Externalizes or increases tolerance through equipment. |
| Scrypta support | Structured retention, preparation, external storage. |
| Isotra support | Stability and reduced burden volatility. |
| Aethra support | Anchoring persistence, space, permanence, domain-stable retention. |
| Reticula support | Offloads retention into network/platform infrastructure. |
| Phasma support | Nonphysical, spirit, echo, or memory-presence retention. |
| Mnemora support | Memory-pattern retention with autobiographical cost risk. |
| Vitia/corruption | May unlock forbidden access while degrading safe tolerance. |
| Injury/trauma | Reduces or warps tolerance. |
| Training time | Increases tolerance through deliberate integration. |

Exact tolerance formulas are deferred.

---

## 6. Carrier types

| Carrier | Meaning | Primary handoff |
|---|---|---|
| Vessel Carrier | Body, embodied structure, organs, breath, channels. | D03/D07 |
| Animus Carrier | Inner force, spirit, will, cultivation identity. | D03/D04/D06 |
| Cognitive Carrier | Memory, formula, logic, visualization, mental map. | D03/D05 |
| Economy Carrier | Partition-specific retention tied to a Power Economy. | D03 |
| Scrypta Carrier | Marks, scripts, circuits, seals, prepared patterns. | D03/D09 |
| Relic Carrier | External object holds the Expression. | D09 |
| Tool/Tech Carrier | Device, implant, weapon, network node, platform. | D09 |
| Domain Carrier | Place, oath, faction, realm, sanctum, region, domain anchor. | D06/D10 |
| Companion/Platform Carrier | AI, spirit, summon, ship, mech, beast, familiar, construct. | D08/D09 |
| External Anchor | Separate stabilizer or link outside actor. | D09/D10 |

---

## 7. Slot condition families

### Stable states

| Condition | Meaning |
|---|---|
| Healthy | Stable and safe. |
| Reinforced | Hardened against degradation or backlash. |
| Expanded | Holds more burden than normal. |
| Harmonized | Reduced interference with other slots/economies. |
| Specialized | Better for one Expression family, worse or neutral for others. |
| Externalized | Burden is moved to external carrier. |
| Dormant | Slot exists but is not active. |
| Reserved | Held open for known future Expression, path, ritual, or inscription. |

### Strain states

| Condition | Meaning |
|---|---|
| Strained | Usable with increased cost/risk. |
| Crowded | Near capacity; new inscriptions are harder. |
| Unstable | Misfire, backlash, drift risk. |
| Frayed | Repeated use/replacement weakened structure. |
| Overwritten | Recently replaced; residue from prior Expression remains. |
| Contested | Two patterns/economies interfere in same carrier. |
| Leaking | Reservoir, trace, memory, or force escapes. |
| Misaligned | Poor match with current economy, domain, or Vessel state. |

### Damage states

| Condition | Meaning |
|---|---|
| Degraded | Reduced tolerance and higher failure risk. |
| Scarred | Permanent alteration; weakness or new affinity possible. |
| Sealed | Temporarily inaccessible. |
| Closed | Lost until major repair, breakthrough, restoration, or transformation. |
| Cracked | Can hold power but risks collapse under pressure. |
| Burned | Damaged by overdraw, critical failure, Scintilla, Calora, overload. |
| Corroded | Damaged by Vitia, Vacuus, entropy, poison, hostile influence. |
| Hollowed | Capacity remains but identity, memory, or Animus support missing. |
| Severed | Route to economy, domain, relic, entity, or carrier is cut. |
| Infected | Corruptive, parasitic, hostile, or foreign pattern present. |

### Transformative states

| Condition | Meaning |
|---|---|
| Mutating | Slot is changing due to pressure, breakthrough, corruption, experimentation. |
| Transformed | Slot type or behavior changed. |
| Awakened | Previously unavailable slot becomes usable. |
| Split | One slot becomes multiple weaker slots/routes. |
| Merged | Multiple slots combine into stronger but less flexible structure. |
| Inverted | Slot favors opposed or altered Expression family. |
| Haunted / Echoed | Prior Expression leaves residue, ghost pattern, Phasma/Mnemora trace. |
| Bound | Slot tied to oath, entity, relic, faction, domain, or condition. |
| Claimed | External force has partial ownership or access. |
| Sanctified / Purified | Cleansed/aligned for certain use, possibly rejecting others. |

---

## 8. Replacement rule

Expressions are not freely swapped.

Replacing or overwriting a retained Expression requires a procedure.

### Safe replacement

May require:

- teacher-guided retraining;
- downtime;
- ritual;
- meditation;
- Scrypta recalibration;
- healing/restoration;
- domain alignment;
- breakthrough;
- technical maintenance;
- relic refitting;
- formal path procedure.

### Risky replacement

May cause:

- slot strain;
- slot degradation;
- loss of refinement;
- increased cost;
- misfire risk;
- memory fragmentation;
- instability gain;
- Vitia contamination;
- carrier scar;
- temporary seal;
- permanent closure on severe or critical failure.

---

## 9. Capacity states

| Capacity state | Meaning |
|---|---|
| Empty | No retained Expressions in that carrier. |
| Stable | Burden within tolerance. |
| Crowded | Near tolerance; minor risk or recovery pressure. |
| Overloaded | Burden exceeds tolerance; risk increases. |
| Fracturing | Continued use risks slot damage, instability, backlash. |
| Collapsed | Carrier cannot safely hold or use some Expressions. |
| Mutating | Carrier changes due to pressure, corruption, breakthrough, experimentation. |

---

## 10. Actor Expression Profile

```yaml
actor_expression_profile:
  actor_id: string
  expression_capacity:
    carriers:
      - carrier_id: string
        carrier_type: vessel | animus | cognitive | economy | scrypta | relic | tool_tech | domain | companion_platform | external_anchor
        tolerance_rating: integer | band | formula_ref
        current_burden: integer | band
        capacity_state: empty | stable | crowded | overloaded | fracturing | collapsed | mutating
        slot_conditions:
          healthy: integer
          reinforced: integer
          expanded: integer
          harmonized: integer
          specialized: integer
          externalized: integer
          dormant: integer
          reserved: integer
          strained: integer
          crowded: integer
          unstable: integer
          frayed: integer
          overwritten: integer
          contested: integer
          leaking: integer
          misaligned: integer
          degraded: integer
          scarred: integer
          sealed: integer
          closed: integer
          cracked: integer
          burned: integer
          corroded: integer
          hollowed: integer
          severed: integer
          infected: integer
          mutating: integer
          transformed: integer
          awakened: integer
          split: integer
          merged: integer
          inverted: integer
          haunted_echoed: integer
          bound: integer
          claimed: integer
          sanctified_purified: integer
  known_expressions:
    - expression_id: string
      display_name: string
      knowledge_state: string
      retention_state: string
      carrier_ref: string | null
      burden_rating: integer | band | formula_ref
      inscription_condition: string | none
      lawful_routes: [string]
      economy_routes: [string]
      expression_grade: integer
      scope_profile_ref: string
      learned_from: training | teacher | relic | observation | copying | theft | breakthrough | research | source_local | player_created | conversion | other
      replacement_count: integer
      degradation_risk: none | low | medium | high
```

---

## 11. UI implication

Known Expressions and Inscribed Expressions should be separate UI areas.

The UI may track:

- Known Expressions;
- Inscribed Expressions;
- Expression Projects;
- Carriers & Slots;
- Slot Condition;
- Power Economies;
- Reservoir;
- Summary Cards;
- hidden/backend notes.

---

## 12. Conversion implications

Donor known/prepared spells, powers known, maneuvers, techniques, mutations, implants, relic abilities, class features, and rituals should be split into:

- known state;
- learned state;
- retention state;
- carrier;
- burden;
- access route;
- external anchor;
- replacement risk;
- source-local boundary.

Donor slot systems are evidence only.
