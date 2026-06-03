# D06-05 Technique Architecture and D05 Method Handoff

**File ID:** `D06-05`  
**Pack:** Astra Ascension D06 — Route, Path, Principle, Technique, and Donor Class Normalization Doctrine  
**Version:** v0_1  
**Status:** Design doctrine draft generated from accepted D06 decisions.  
**Purpose:** Define Technique as a validated formal capability above D05 Method and below or adjacent to D03 Expression when powered.

## Standing D06 boundary

D06 owns formal route identity, Path identity, Route Kernels, route facets, Route Feature Ledgers, Techniques, Principle / Concept route facets, route development, multipath / confluence, profession-route formalization, source-local route conversion, and donor class normalization.

D06 does **not** own D03 Power Economy costs, carriers, Expressions, reservoirs, burdens, or confluence math; D04 proof sufficiency, level, tier, Awakening, Development Picks, breakthroughs, capstone, or Ascension Access; D05 skills, professions, knowledge, training, research, methods, and synthesis substrate; D07 harm, corruption, madness, mutation harm, overload, identity erosion, or recovery; D08 companions, summons, spirits, AI, bonds, or nonhuman actor-state mechanics; D09 relics, tools, implants, weapons, vehicles, ships, mechs, or platforms; D10 factions, rank, law, reputation, territory, settlement, economy, or world-state; final runtime/database schemas; canon sourcebook prose; or live-play GM behavior.

D06 records candidates, structure, permissions, limits, and owner-file handoffs. It does not use route language to bypass the owners above.


## 1. Core boundary

D05 owns Methods. D06 owns Techniques. D03 owns Expression mechanics when cost, carrier, Power Economy, inscription, burden, activation, confluence, overdraw, or supernatural resource behavior enters.

The progression is:

**D05 Method → Technique Candidate → D06 Formal Technique → D03 Expression-linked Technique if powered.**

Not every named repeatable action becomes a Technique.

## 2. Definitions

### Method

A Method is a repeatable application of competency below formal route technique. Examples: Hammer Rhythm, Depth Reading, Ash-Scent Lure, Breath-Step Pattern, Emergency Clamp Sequence, Hostage Listening Posture.

### Technique Candidate

A candidate is a Method, research output, route feature, donor ability, or source-local capability being evaluated for D06 status. It is not fully authorized.

### Formal Technique

A Technique is a validated formal capability with defined use case, trigger, effect boundary, route relation, training path, limits, and validation state.

### Expression-linked Technique

A Technique that uses or modifies D03 Expression mechanics. D06 owns formal structure. D03 owns cost, carrier, burden, inscription, re-authoring, confluence, and activation.

## 3. Technique categories

Techniques may be martial, craft, social / oath, exploration / survival, platform / interface, companion / bond, esoteric / Principle, source-local, or hybrid.

Examples:

- Martial: Gate-Hinge Shielding, Red-Moon Low Cut, Broken Spear Recovery.
- Craft: Stress-Light Reading, Cold-Seam Repair, Siege-Kettle Ration Cycle.
- Social: Thorn-Court Safe Address, Equal-Cost Bargain, Hostage Breath Pause.
- Exploration: Hollow-Depth Fault Listening, Whiteout Trail Split, Wet-Road Spore Marking.
- Platform: Ash Recoil Dump, Quiet Engine Cant, Drone-Swarm Grid Stitch.
- Companion: Split-Watch Signal, Pack Recall Cut, Colony Whisper Relay.
- Esoteric: Memory Echo Stabilization, Oath-Weight Reading, Glass-Mercy Reflection.
- Source-local: donor maneuver, region-specific ritual, sect-only step art.

## 4. Method-to-Technique validation procedure

When a D05 Method might become a Technique:

1. Identify Method and parent competencies.
2. Confirm repeated use, training, research, proof, route pressure, or teacher validation.
3. Identify Route or facet support.
4. Define trigger and effect boundary.
5. Define limits.
6. Determine if mundane, route-linked, source-local, or powered.
7. Determine D03, D04, D07, D08, D09, D10 handoffs.
8. Add as Technique Candidate.
9. Authorize, block, source-localize, or escalate.

## 5. Technique anatomy

Every formal Technique should define:

- name;
- source;
- Route / facet relation;
- category;
- trigger;
- action posture;
- effect boundary;
- limits;
- cost;
- risk;
- training path;
- rank or depth if any;
- owner handoffs;
- validation state;
- Route Feature Ledger link if present.

## 6. Technique states

| State | Meaning |
|---|---|
| candidate | proposed but not authorized. |
| drafted | structure exists pending validation. |
| authorized | legal to learn or use under limits. |
| training | actor is learning it. |
| known | actor knows it but may not be able to use it now. |
| active | usable under current conditions. |
| dormant | known but inaccessible. |
| scarred | usable but carries damage or cost. |
| corrupted | hostile or unstable. |
| externalized | depends on anchor / tool / platform / companion. |
| source-local | bound to source context. |
| retired | no longer develops or is replaced. |
| blocked | requirements not met. |

## 7. Technique permission bands

Working bands: minor, standard, advanced, severe, capstone, source-local. These are not final balance math; they prevent early Techniques from granting late-route effects.

## 8. Technique vs. Expression boundary

A Technique remains D06-only when it is formal structure, training, procedure, or route capability without D03 Power Economy mechanics.

A Technique requires D03 handoff when it uses Mistra / Zi / Volith / other Power Economies, cost partition, carrier burden, resource pool, recharge, Expression inscription, confluence, overdraw, backlash, supernatural activation, or re-authoring.

Examples:

- **Oath-Weight Reading** as D06 Technique reads social / oath tension through trained court procedure and route sense.
- **Oath-Weight Binding** as D03 Expression-linked Technique spends Power Economy to enforce a spoken bargain.
- **Quiet Engine Cant** as D06 Technique synchronizes engine crew rhythm.
- **Engine-Soul Overchant** as D03 / D09 Expression-linked Technique forces impossible engine output with cost and feedback risk.

## 9. Technique Sets

A Technique Set is a related family of Techniques associated with Route, facet, teacher, lineage, source-local system, profession-route, or external anchor. It can be fixed, branching, research-grown, method-grown, teacher-gated, route-ledger generated, source-local, or anchor-dependent. It is not a class table by default.

## 10. Failure modes

Technique failure may involve misfire, overstrain, backlash, misread, anchor fault, domain mismatch, dissonance, collateral, source-local failure, or corruption leak. D02 handles resolution when rolled. Owner files resolve consequences.

## 11. Donor ability normalization

Donor spells, maneuvers, feats, class features, rituals, powers, cultivation arts, protocols, and companion commands may map to D05 Method, D06 Technique, D03 Expression, Route Feature, source-local entry, or escalation. They are not imported as-is.

## 12. Doctrine shape

```yaml
technique_record:
  technique_id: string
  actor_or_route_ref: string
  technique_name: string
  source_type: []
  category: []
  technique_state: candidate | drafted | authorized | training | known | active | dormant | scarred | corrupted | externalized | source_local | retired | blocked
  route_refs: []
  facet_refs: []
  feature_ledger_refs: []
  trigger: string
  action_posture: action | reaction | preparation | downtime | passive | extended | ritual | other
  effect_boundary: string
  limits: []
  cost_profile:
    cost_type: none | time | fatigue | material | social_debt | risk | power_economy | mixed
    d03_required: boolean
  risk_tags: []
  training_path_refs: []
  proof_refs: []
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  validation_state: authorized | pending_proof | pending_owner_file | dangerous | source_local | blocked | escalated
```

## 13. Rule

A Technique is formal enough to train, validate, limit, and develop. It is not so broad that every named action becomes a power.
