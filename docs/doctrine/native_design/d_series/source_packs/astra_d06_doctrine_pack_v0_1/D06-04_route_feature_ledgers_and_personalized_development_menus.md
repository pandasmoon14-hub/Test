# D06-04 Route Feature Ledgers and Personalized Development Menus

**File ID:** `D06-04`  
**Pack:** Astra Ascension D06 — Route, Path, Principle, Technique, and Donor Class Normalization Doctrine  
**Version:** v0_1  
**Status:** Design doctrine draft generated from accepted D06 decisions.  
**Purpose:** Define personalized route-instance feature ledgers without turning archetypes or Paths into fixed class tables.

## Standing D06 boundary

D06 owns formal route identity, Path identity, Route Kernels, route facets, Route Feature Ledgers, Techniques, Principle / Concept route facets, route development, multipath / confluence, profession-route formalization, source-local route conversion, and donor class normalization.

D06 does **not** own D03 Power Economy costs, carriers, Expressions, reservoirs, burdens, or confluence math; D04 proof sufficiency, level, tier, Awakening, Development Picks, breakthroughs, capstone, or Ascension Access; D05 skills, professions, knowledge, training, research, methods, and synthesis substrate; D07 harm, corruption, madness, mutation harm, overload, identity erosion, or recovery; D08 companions, summons, spirits, AI, bonds, or nonhuman actor-state mechanics; D09 relics, tools, implants, weapons, vehicles, ships, mechs, or platforms; D10 factions, rank, law, reputation, territory, settlement, economy, or world-state; final runtime/database schemas; canon sourcebook prose; or live-play GM behavior.

D06 records candidates, structure, permissions, limits, and owner-file handoffs. It does not use route language to bypass the owners above.


## 1. Purpose

Astra needs personalized and customized feature lists, but not universal class tables. D06 therefore uses the **Route Feature Ledger**.

A Route Feature Ledger is actor-specific or route-instance-specific. It records lawful feature options, active features, candidates, constraints, scars, permissions, refinements, Techniques, Expression candidates, route modifications, source-local entries, blocked entries, and future unlocks generated from that Route Kernel.

## 2. Feature Ledger is not a class table

A class table says: at level X, all members of this class gain Y.

A Route Feature Ledger says: this actor's Route has generated these lawful features or options because of their Path identity, proof, facets, competencies, Expressions, advancement state, scars, anchors, faction relations, and owner-file handoffs.

Fixed tables are allowed only as source-local structures, simplified templates, conversion artifacts, UI convenience layers, or later canon-designed route packages. They are not the default D06 model.

## 3. Sources for Route Features

A Route Feature may arise from:

- Route Kernel facets;
- D04 proof;
- D04 Awakening Package;
- D04 Development Pick;
- D05 competencies;
- D05 methods;
- D05 research tracks;
- D05 synthesis records;
- D03 Expression or Power Economy state;
- D06 Path identity, Domains, Archetypes, Principles, Techniques;
- D07 scars, corruption, harm, mutation, constraints;
- D08 companions, spirits, AI, bonds;
- D09 relics, tools, platforms, implants;
- D10 factions, territory, law, institutions;
- source-local grants.

Features are not generated from Archetype alone.

## 4. Required fields

Every Route Feature should define:

- feature name;
- source;
- unlock basis;
- owner file;
- permissions;
- limits;
- state;
- validation state;
- route and facet links;
- handoff refs if cross-system.

A feature cannot exist merely because it sounds thematic.

## 5. Feature states

| State | Meaning |
|---|---|
| candidate | possible feature, not yet legal. |
| available | legal option not selected or not active. |
| selected | chosen but may require final validation. |
| active | currently usable under limits. |
| dormant | exists but inaccessible. |
| scarred | carries route damage, cost, or trauma. |
| corrupted | hostile, unstable, or tainted. |
| externalized | depends on anchor. |
| source-local | valid only in bounded context. |
| blocked | requirements not met. |
| retired | no longer develops but remains historical. |

## 6. Feature types

Feature entries may represent:

- permission;
- Technique;
- Technique candidate;
- Expression candidate;
- domain interaction;
- Principle development;
- constraint;
- obligation;
- route scar;
- anchor dependency;
- source-local rule;
- capstone candidate;
- future Development Pick target.

## 7. Owner validation

D06 owns the ledger. It does not own every feature's mechanics.

- D03 validates powered features, Expressions, cost, carrier, burden, confluence, activation, and recharge.
- D04 validates proof, Development Pick timing, tier authorization, Awakening, breakthrough, and capstone.
- D05 validates competency, training, research, method, synthesis basis.
- D07 validates harm, compulsion, corruption, overload, identity erosion, mutation harm.
- D08 validates companion, spirit, AI, bond, summon, nonhuman actor state.
- D09 validates relic, tool, implant, platform, item, vehicle, ship, mech.
- D10 validates faction, rank, law, territory, institution, reputation, world-state.

## 8. Examples

### Glass-Tomb Archivist

Possible ledger:

- Sealed Record Reading — Technique, D06 / D05.
- Dead-Language Cross Index — knowledge / method feature, D05.
- Memory Echo Stabilization — Technique candidate with D07 identity risk.
- Tomb-Glass Lens Dependency — external anchor constraint, D09.
- Identity Bleed Warning — drift / scar feature, D07.

### Mech-Synced Ash Cavalier

Possible ledger:

- Ash-Screen Charge — Technique candidate, D06 / D09.
- Neural Recoil Dump — platform feature with D07 risk.
- Cockpit Prayer Cant — D05 Method or D06 Technique depending effect.
- Sync Limit Break — dangerous D03 / D09 / D07 handoff.
- Mech Disabled Route Degradation — externalized constraint.

### Thorn-Court Mediator

Possible ledger:

- Oath-Reading Courtesy — social / Domain feature, D05 / D06 / D10.
- Thorn-Court Safe Address — faction / source-local feature, D10.
- Reciprocal Binding Clause — Principle / Technique candidate, D06 / D03.
- Cannot Casually Break Sworn Speech — route constraint, D06 / D07.
- Diplomatic Immunity in Thorn Courts — D10 source-local feature.

### Fungal Courier

Possible ledger:

- Spore-Trail Memory — actor physiology feature, D08 / D06.
- Humid Passage Domain — Domain facet.
- Dry-Air Weakness — constraint feature, D07 / D10.
- Colony Whisper — companion / collective feature, D08.
- Human Road Customs — D05 Knowledge / Training feature.

## 9. Doctrine shape

```yaml
route_feature_ledger_record:
  ledger_id: string
  route_ref: string
  actor_ref: string
  feature_entries:
    - feature_id: string
      feature_name: string
      feature_state: candidate | available | selected | active | dormant | scarred | corrupted | externalized | source_local | blocked | retired
      feature_type: permission | technique | technique_candidate | expression_candidate | domain_interaction | principle_development | constraint | obligation | scar | anchor_dependency | source_local | capstone_candidate | other
      unlock_basis: []
      owner_file: D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | source_local | unresolved
      permissions: []
      limits: []
      validation_state: authorized | pending_proof | pending_owner_file | dangerous | source_local | blocked | escalated
```

## 10. Rule

Route Feature Ledgers allow unique character-specific development without returning to fixed donor class tables. They must remain source-bound, permission-bound, limit-bound, and owner-validated.
