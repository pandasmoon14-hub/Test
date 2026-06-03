# D04-04 — Advancement Axis Registry

Status: `doctrine-draft / accepted D04 design decisions`  
Layer: D04 advancement doctrine  
Owner: advancement axis routing  
Feeds: D05, D06, D07, D08, D09, D10, runtime progression schema

## 1. Purpose

This file defines how advancement axes are recognized, registered, routed, and bounded.

An advancement axis is a focused growth track that may advance independently of ordinary level and tier cadence, while still respecting proof, tier authorization, Development Pick validation, owner-file rules, and state deltas.

## 2. Axis principle

Astra should support a web of advancement possibilities. Level, tier, Path/Class/Dao, and breakthrough are important, but they are not the only ways an entity can grow.

An axis becomes player-visible only when the actor has contact, proof, training, ownership, exposure, meaningful desire, repeated action, discovery, or event trigger connected to it.

## 3. Progressive Axis Disclosure

Tier 0 and early play must not expose every possible axis. Visible early axes may include Health / Endura, profession, core skills, relationships/community, tool familiarity, active goals, proof records, known achievements, and discovered route seeds.

Other axes appear through play.

| Axis appears when... | Example |
|---|---|
| Actor practices a profession repeatedly | Blacksmithing Axis appears. |
| Actor survives repeated danger | Survival/Trial Proof axis appears. |
| Actor studies creatures | Codex/Bestiary axis appears. |
| Actor receives a relic | Relic Bond axis appears. |
| Actor gains faction notice | Reputation axis appears. |
| Actor explores routes | Map/Exploration axis appears. |
| Actor repeats meaningful action | Achievement chain appears. |
| Actor hears/acts on route rumor | Awakening Vector appears. |
| Actor binds to companion | Bond Depth axis appears. |
| Actor alters territory | Territory/Domain axis appears. |

## 4. Axis registration record

```yaml
advancement_axis:
  axis_id: string
  actor_ref: string
  axis_family: string
  axis_name: string
  axis_status: hidden | seed | visible | active | capped | blocked | source_local | retired | transformed
  owner_file: D04 | D05 | D06 | D07 | D08 | D09 | D10 | source_local
  proof_refs: [string]
  current_band: trace | seed | credible | established | weighty | defining | mythic | capstone | owner_defined
  tier_authorization_required: integer | null
  cap_state: below_cap | at_cap | cap_raise_available | cap_blocked
  access_requirements: [string]
  development_pick_types_allowed: [string]
  breakthrough_relevance: none | possible | required | pending | resolved
  linked_routes: [string]
  linked_expressions: [string]
  linked_power_economies: [string]
  linked_anchors: [string]
  source_local_boundary: string | null
  state_delta_refs: [string]
```

## 5. Axis families

D04 recognizes these axis families for routing. The list is intentionally broad enough to handle donor pressure without making all axes core at character creation.

### 5.1 Attribute / Core Stat Growth

Raw attribute improvement through training, breakthrough, consumables, proof, or transformation.

Owner: D01/D04 with D07/D06 handoffs where structural. Donor ability-score math must not import directly.

### 5.2 Skill Proficiency Ranks

Discrete growth in a skill, competency, knowledge, language, craft, or practice.

Owner: D05. Donor skill lists can overfit if copied.

### 5.3 Technique / Ability / Expression Tree Unlocks

Branching access to methods, powers, techniques, or Expressions.

Owner: D03/D06. This must not grant unsupported ability without lawful vector.

### 5.4 Mastery Specializations

Deep specialization inside a skill, weapon, element, tool, profession, or method.

Owner: D05/D06/D09 depending target.

### 5.5 Kinform / Bloodline / Body Evolution

Biological, mystical, inherited, constructed, or kinform transformation.

Owner: D08/D07/D06. Donor species law must not become Astra law.

### 5.6 Soul / Core / Inner Vessel Development

Internal core, Animus, reservoir, or inner structure growth.

Owner: D03/D04/D07. Donor dantian/meridian metaphysics remains source-local unless adopted.

### 5.7 Dao / Conceptual Comprehension

Understanding or embodiment of principle, concept, domain, law, element, or pattern.

Owner: D06. Donor realm names and cosmology must not import.

### 5.8 Affinity / Elemental Attunement Depth

Depth of relation to element, material, concept, environment, or expression family.

Owner: D06/D03. Affinity must not become simple damage bonus only.

### 5.9 Bond Depth

Deepening link with familiar, mount, companion, spirit, AI, relic, family, oath, or faction representative.

Owner: D08/D09/D10.

### 5.10 Swarm / Hive / Collective Strain Evolution

Growth in minion collective, swarm body, hive intelligence, genetic strain, or distributed actor form.

Owner: D08.

### 5.11 Avatar / Incarnation Refinement

Secondary body, clone, projection, proxy, or incarnation growth.

Owner: D08/D03/D07.

### 5.12 Equipment Grade Ascension

Gear, tools, armor, weapons, vehicles, platforms, or installables improve over time.

Owner: D09.

### 5.13 Soulbound Weapon / Item Awakening

Bonded item grows with actor.

Owner: D09/D08.

### 5.14 Crafting Profession Mastery

Blacksmithing, enchanting, tailoring, cooking, medicine, alchemy-like work, engineering, shipwrighting, or other craft grows.

Owner: D05/D09/D10.

### 5.15 Territory / Domain Tier

Stronghold, settlement, dungeon core, territory, ship-domain, domain site, farm, forge, city, or region grows.

Owner: D10/D09.

### 5.16 Settlement Specialization Path

A place develops specialization such as academy, trade hub, military bastion, sanctuary, forge-city, garden world, or hidden archive.

Owner: D10.

### 5.17 Reputation / Fame / Infamy / Standing Ladder

Social recognition, faction standing, trace, scrutiny, title reputation, law status.

Owner: D10.

### 5.18 Title Collection and Upgrade

Titles from deeds, roles, achievements, scars, oaths, records, myths.

Owner: D04/D10/D06.

### 5.19 Achievement / Milestone Unlocks

Permanent milestone records from repeated feats, extreme tasks, discoveries, completion chains.

Owner: D04 with owner-file target.

### 5.20 Alignment / Karma / Causal Weight

Moral, causal, reciprocity, merit, debt, oath, or consequence axis.

Owner: D04/D10/D03 if Sortis/Karmax-like economy involved. Moral law must not universalize without setting doctrine.

### 5.21 Corruption / Taint / Vitia Depth

Forbidden, degenerative, hostile, unstable, corruptive force accumulation or transformation.

Owner: D03/D07/D06. This is not antagonist-only by default; player access is possible with risk and validation.

### 5.22 Power Reservoir Depth

Maximum resource capacity or reservoir quality separate from level.

Owner: D03.

### 5.23 Regeneration / Recovery Rate

Recovery from health, Endura, economy drain, carrier strain, corruption, overdraw, fatigue.

Owner: D07/D03.

### 5.24 Channeling / Casting / Activation Speed

Reducing activation windows, chants, gestures, focus time, setup, interface time.

Owner: D03/D06/D02.

### 5.25 Area / Range / Scope Extension

Increasing reach, area, target count, duration, persistence, summoning/banishing reach, remote operation.

Owner: D03/D06/D10.

### 5.26 Cleave / Multi-Target Capacity

Increasing number of targets, chaining, splitting, projectile branching, area multitarget effect.

Owner: D03/D07/D06.

### 5.27 Perception / Senses Depth

Mundane sight into special senses, domain reading, threat sense, truth reading, thermal, mana-like sight, codex recognition.

Owner: D05/D06/D08/D10.

### 5.28 Mental Fortress / Willpower Rank

Defense against intrusion, possession, fear, Glamour, psychic pressure, compulsion, route hijack.

Owner: D07/D05/D03.

### 5.29 Comprehension / Insight Currency

Epiphanies, study breakthroughs, deductions, insight points, bottleneck breaks.

Owner: D05/D04.

### 5.30 Language / Lexicon Unlock

Ancient scripts, beast speech, machine language, symbolic grammar, domain lexicon, intent-broadcast.

Owner: D05/D10/D03 if Scrypta/Reticula involved.

### 5.31 Leadership / Command Aura

Follower coordination, morale, remote tactical support, group action, faction command.

Owner: D10/D08.

### 5.32 Body Tempering / Flesh Refinement Layers

Physical reinforcement through training, exposure, rituals, scars, technology, cultivation, craft.

Owner: D07/D03/D08.

### 5.33 Personal Realm / Inner World Evolution

Pocket dimension, inner sanctuary, storage, training ground, living internal domain.

Owner: D08/D10/D03. This should be rare, high-tier, and high-runtime burden.

### 5.34 Sigil / Rune / Scrypta Comprehension

Understanding prepared symbols, inscriptions, circuits, runes, scripts, patterns.

Owner: D03/D05/D09.

### 5.35 Map / Exploration Completion

Uncovering regions, routes, leyline paths, hidden maps, travel networks.

Owner: D10/D05.

### 5.36 Bestiary / Codex Mastery

Researching creatures, enemies, ecology, weaknesses, mimicry, counters.

Owner: D05/D07/D08.

### 5.37 Legend / Mythic Imprint

World record of deeds becoming mechanically significant.

Owner: D04/D10/D06.

### 5.38 Devotion / Favor Rank

Faith, vow, doctrine, communion, patron relation, communal resonance.

Owner: D03/D06/D10. Donor gods/cosmology remain source-local unless promoted.

### 5.39 Skill Fusion / Syncretism

Merging skills, Expressions, economies, routes, or methods.

Owner: D04/D06/D03.

### 5.40 Seal Unlocking / Inner Potential

Breaking seals, unlocking latent power, inherited memory, past-life fragments, engineered locks.

Owner: D08/D06/D03.

## 6. Advancement Layer Grant Matrix

| Layer | Typical grant | Must not grant |
|---|---|---|
| Ordinary Level | One typed Development Pick. | Free universal power. |
| Tier Transition | Authorization + Direct Tier Benefit + Visibility + Future Notice. | Mastery of whole tier. |
| Proof Bundle | Eligibility, legal options, pending outputs. | Generic spendable XP by default. |
| Axis Progress | Narrow advancement in axis owner scope. | Unrelated ability. |
| Breakthrough | Transformative payload + consequence. | Safe automatic success if risk unresolved. |
| Awakening | Route identity + access vector + starter method. | Full class table or unrestricted power. |
| Title/Achievement | Formal proof binding, recognition, narrow benefit/access. | Stacking universal stat bloat. |
| Project | Progress toward defined target. | Instant result without cost/time/proof. |
| Capstone | Final proof, final-form pressure, Capstone Pick. | Routine level feature. |
| Ascension Access | Opportunity to attempt/delay/refuse Ascension. | Mandatory departure or cosmology import. |

## 7. Axis anti-sprawl rule

An axis should be registered only if it creates a meaningful tracked distinction. Do not create an axis for every repeated action. Create or reveal an axis when the action pattern affects advancement, proof, route, state, access, title, achievement, owner-file mechanics, or future choices.

## 8. Axis cap rule

An axis may reach a cap before the actor has the tier authorization, proof, teacher, tool, anchor, or breakthrough needed to progress.

At cap, outputs may include cap raise available through tier benefit, pending proof, pending route, pending training, breakthrough required, owner-file blocked, source-local only, axis transforms, axis branches, or axis retires.

## 9. Axis state deltas

Axis advancement must eventually commit state deltas: axis created/revealed, axis band changed, axis cap raised, axis stalled/capped, axis transformed, axis linked to route, axis linked to Expression, axis bound to title/achievement, axis externalized to item/territory/companion, axis corrupted/scarred, or axis retired.

## 10. Conversion implications

Donor advancement structures map into D04 axes by function, not packaging.

Examples:

- donor skill rank -> Skill/Profession axis if D05 supports;
- donor class feature tree -> route/Expression/Development Pick target, not direct class law;
- donor item rarity progression -> Item/Relic axis, not universal rarity table;
- donor settlement tier -> Territory/Settlement axis, not character tier;
- donor reputation ranks -> World/Faction axis;
- donor bloodline evolution -> Kinform/Bloodline axis with D08 review;
- donor cultivation realm -> tier/proof/breakthrough pressure, not direct imported realm name;
- donor point-buy advancement -> typed pick or axis progress if validation supports.

## 11. Validation rules

An axis is invalid if it duplicates an existing axis without reason; has no owner file; grants benefits without proof or picks; bypasses tier authorization; silently imports donor rank names or math; becomes visible to player with no contact/proof/exposure/desire; collapses item, actor, faction, and character growth into one record; has no state-delta path; or lacks source-local boundary when donor-specific.
