# D04-03 — Levels, Tiers, and Development Picks

Status: `doctrine-draft / accepted D04 design decisions`  
Layer: D04 advancement doctrine  
Owner: level, tier, and Development Pick architecture  
Depends on: D04-01 Proof Bundles, D04-02 Awakening, D04-04 Advancement Axis Registry

## 1. Purpose

This file defines level cadence, Development Picks, tier authorization, Direct Tier Benefits, and tier transition handling.

Astra uses levels for pacing, tiers for authorization, Development Picks for lawful player choice, and proof for eligibility.

## 2. Level cadence lock

Ordinary levels grant one typed Development Pick by default. This creates reliable advancement cadence without turning levels into universal stat increases or donor-style feature tables.

## 3. Level band structure

| Tier | Level band | Primary advancement behavior |
|---:|---|---|
| 0 | 1–5 | Mortal Development Picks, mundane axes, proof gathering, route seeds, Awakening threshold. |
| 1 | 5–15 | Ascendant Development Picks, low-grade Expressions, first route development. |
| 2 | 16–25 | Stabilization, stronger axes, reliable low-grade development. |
| 3 | 26–35 | Structural development, carrier/slot/economy/route expansion. |
| 4 | 36–45 | Advanced scope, mature Expression families, stronger external anchors. |
| 5 | 46–55 | Major ascendant scale, scene-shaping options, strong route identity. |
| 6 | 56–65 | Superior complexity, high-grade development, major fusion pressure. |
| 7 | 66–75 | Apex-band pressure, dangerous routes, severe consequence scale. |
| 8 | 76–85 | Transcendent-band, region/site/law-bounded influence. |
| 9 | 86–95 | Mythic-band, campaign/world-facing influence. |
| 10 | 95–100 | Capstone Band, final proof, Capstone Picks, Ascension Access at level 100. |

## 4. Level 5 threshold handling

Level 5 is the Mortal Threshold. At level 5, the system checks Awakening Proof, Catalyst/Route/Anchor, pre-awakening axes, proof clusters, Dynamic Triadic Awakening eligibility, and Path/Class/Dao formalization warning.

The level 5 Development Pick may be spent normally, held, shaped toward Awakening readiness, or converted into a pending Awakening preparation option if validation permits.

## 5. Levels 95–100 handling

Levels 95–100 are not ordinary levels. They use Capstone Band Procedure and Capstone Picks. This is defined in `D04-06_capstone_and_ascension_access.md`.

## 6. Typed Development Picks

Doctrine uses typed Development Picks. UI may present them through a simplified universal menu if backend typing remains intact.

| Pick type | Function | Primary owners |
|---|---|---|
| Axis Pick | Advance a registered advancement axis. | D04 + owner file |
| Skill / Profession Pick | Improve skill, trade, craft, knowledge, language, profession. | D05 |
| Expression Pick | Refine, stabilize, re-author, deepen, or improve an Expression. | D03/D06 |
| Capacity Pick | Improve reservoir, carrier, Endura, burden, recovery, tolerance. | D03/D04/D07 |
| Route Pick | Stabilize, branch, clarify, redirect, or reinforce route. | D04/D06 |
| Repair Pick | Reduce strain, instability, slot damage, drift, scar pressure, carrier damage. | D03/D07 |
| Project Pick | Advance research, crafting, exploration, territory, relic, bond, codex, or training project. | D05/D09/D10 |
| Proof Pick | Formalize proof into title seed, route seed, affinity seed, achievement, axis opportunity. | D04 |
| Breakthrough Prep Pick | Improve safety, quality, readiness, or clarity of pending breakthrough. | D04 |
| Bond / Companion Pick | Deepen companion, familiar, spirit, AI, mount, swarm, avatar, or actor bond. | D08 |
| Item / Relic Pick | Improve, awaken, attune, repair, or synchronize tool, relic, weapon, implant, platform, item. | D09 |
| World / Faction Pick | Advance territory, settlement, faction standing, reputation, command, law, exploration, world-state axis. | D10 |
| Drift / Fusion Pick | Support route drift, fusion, syncretism, hybridization, reversion, or controlled divergence. | D04/D06 |
| Capstone Pick | High-end pick for levels 95–100. | D04 + relevant owner |
| Source-local Pick | Pick valid only in a bounded local source/campaign context. | Source-local + owner file |

## 7. Pick shapes

| Pick shape | Meaning |
|---|---|
| Open typed pick | Any legal option of that type. |
| Proof-shaped pick | Only options supported by recent or stored proof. |
| Axis-shaped pick | Tied to a specific axis. |
| Route-shaped pick | Tied to current route, drift, or awakening vector. |
| Recovery-shaped pick | Must repair, stabilize, or recover before further growth. |
| Tier-shaped pick | Granted by tier transition and has higher scale or broader targets. |
| Capstone-shaped pick | Tied to capstone proof and high-end structures. |
| Source-local pick | Valid only inside bounded subsystem, faction, region, relic, or conversion. |

## 8. Spend validation gate

```yaml
development_pick_spend:
  pick_id: string
  pick_type: string
  target: string
  grant_source: level | tier | proof | achievement | title | breakthrough | axis | source_local | capstone
  proof_basis: [proof_record_id]
  owner_file: D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | source_local
  tier_permission: valid | pending | blocked
  route_access: valid | pending | blocked
  cost_or_training_required: string | null
  effect_scope: string
  conflict_check: passed | warning | blocked
  state_delta: string
  validation_result: authorized | pending | unavailable | dangerous | source_local | blocked
```

A pick cannot be spent unless the target exists or can be lawfully created; pick type matches target; proof supports spend; current tier permits scale; route/access exists; owner-file rules allow it; required cost/time/training/material/project needs are satisfied or recorded; the spend produces a clear state delta; and the spend does not bypass breakthrough requirements.

## 9. Pick hold states

| Hold state | Meaning |
|---|---|
| Fresh | Recently gained; no issue. |
| Held | Saved for later. |
| Focused | Reserved for declared target. |
| Stale | Original proof context is weakening or becoming less relevant. |
| Pressurized | Holding the pick creates threshold, route, or proof pressure. |
| Converted | Changed into another legal pick form through training, proof, or doctrine-backed procedure. |
| Expired | Mostly source-local or event-specific picks. Core level picks rarely expire. |

Holding 1–2 picks is normal. Holding many picks may trigger warnings, stale state, or pressure if proof context drifts.

## 10. Pick timing rules

Development Picks are usually spent during advancement screens, downtime, training scenes, recovery scenes, threshold scenes, project-resolution scenes, or source-local timing windows. Mid-action spending is exceptional and requires pick-type justification, breakthrough, crisis, source-local rule, or immediate formalization.

## 11. Higher-tier pick behavior

Higher-tier picks may be somewhat stronger, but their primary advantage is broader legal target access.

| Pick band | Legal target scope |
|---|---|
| Mortal Pick | Mundane axes, profession, skills, proof, achievements, route seeds. |
| Ascendant Pick | Early Expressions, first economy routes, route stabilization, low-grade capacity. |
| Advanced Pick | Deeper axes, confluence prep, structural preparation, stronger mastery. |
| Apex Pick | High-risk route development, major payload prep, high-grade Expressions. |
| Mythic Pick | World-facing axes, rare titles, major fusion, mythic proof structures. |
| Capstone Pick | Final-form, whole-character, world/plane-pressure structures. |

A high-tier pick cannot bypass proof, route, access, tier permission, breakthrough need, or owner-file validation.

## 12. Invalid spend routing

| Output | Meaning |
|---|---|
| Pending proof | More proof is needed. |
| Pending route | Lawful route/access is missing. |
| Pending tier | Current tier does not authorize scale. |
| Pending training | Teacher, practice, downtime, competency, or project work is needed. |
| Pending structure | Breakthrough, carrier, slot, economy, tool, or anchor is missing. |
| Dangerous push | Possible but risky. |
| Source-local only | Valid only in bounded source-local context. |
| Converted to project | Desired spend becomes research, training, crafting, exploration, or re-authoring objective. |
| Rejected | No coherent route or owner-file support exists. |

## 13. Tier authorization principle

A tier does not give mastery. It raises the ceiling of lawful development. A Tier 5 character is not automatically master of all Tier 5 effects. They may develop, stabilize, withstand, and be affected by Tier 5-scale structures if proof, route, training, capacity, cost, breakthrough, and validation support it.

## 14. Tier authorization dimensions

| Dimension | Controls |
|---|---|
| Expression Grade Ceiling | Highest ordinary Expression grade an actor can stabilize without exception. |
| Scope Profile Ceiling | Range, area, duration, persistence, target count, summoning, banishing, territory, scale. |
| Axis Depth Ceiling | How far registered axes can progress without higher authorization. |
| Breakthrough Payload Band | Maximum normal breakthrough payload quality. |
| Power Economy Complexity | Number, depth, partition complexity, confluence safety, overdraw tolerance. |
| Route Complexity | Branching, fusion, mutation, re-authoring, multi-path pressure. |
| External Anchor Scale | Relics, tools, platforms, companions, territory, faction links. |
| Risk Authorization | Overdraw, corruption, backlash, lethal breakthrough, instability attempts. |
| Recognition Scale | Personal, witnessed, faction, regional, world-facing, mythic, capstone recognition. |
| World-State Scale | Size of world/faction/domain consequence actor can meaningfully create or survive. |

## 15. Tier authorization table

| Tier | Authorization role |
|---:|---|
| 0 | Mortal/grounded authorization: skills, professions, achievements, title seeds, proof, body conditioning, tool familiarity, relationships, route seeds. Supernatural access requires special route/anchor/exposure. |
| 1 | Initial ascendant authorization: first route, first Power Economy or equivalent anchor, stable low-grade Expressions, basic breakthrough payloads. |
| 2 | Stabilized ascendant authorization: reliable low-grade development, stronger axis ranks, route branches, safer minor confluence, recovery and carrier tolerance. |
| 3 | Structural development authorization: deeper carrier changes, second-economy possibilities, serious Expression refinement, route fusion/mutation beginnings. |
| 4 | Advanced authorization: broader scope, stronger domains, complex Expression families, item/bond/territory growth, bounded overdraw. |
| 5 | Major ascendant authorization: scene-shaping effects, major breakthrough payloads, strong route identity, faction/world attention. |
| 6 | Superior authorization: high-grade Expressions, major identity/economy/expression pressure, larger projects, stronger lower-tier resistance. |
| 7 | Apex-band authorization: elite breakthrough payloads, dangerous route mutation, major domain authority, severe consequence scale. |
| 8 | Transcendent-band authorization: site/region-scale influence, bounded law-bending, rare economy mastery, whole-character breakthroughs. |
| 9 | Mythic-band authorization: campaign-shaping influence, mythic titles, world-facing proof, major route fusion/severance. |
| 10 | Capstone authorization: final-form transformation, world/plane pressure, capstone payloads, ultimate route resolution. |

## 16. Expression authorization bands

Exact numeric Expression Grade ceilings are deferred to D03/D06. D04 uses descriptive authorization bands.

| Tier | Expression authorization |
|---:|---|
| 0 | No stable ascendant Expression by default; route seeds, theories, mundane techniques, tool patterns. |
| 1 | Low-grade stable Expressions; prototypes and simple re-authoring. |
| 2 | Reliable low-grade Expressions; stronger refinements. |
| 3 | Early mid-grade Expressions; structural re-authoring. |
| 4 | Mid-grade Expressions; broader scope. |
| 5 | Major scene-shaping Expressions. |
| 6 | High-grade Expressions with strong proof and cost. |
| 7 | Apex-grade Expressions; severe risk and domain pressure. |
| 8 | Transcendent Expressions; site/region-scale constraints. |
| 9 | Mythic Expressions; world-facing consequences. |
| 10 | Capstone Expressions; final-form, plane/world-pressure, actor-state scale. |

## 17. Scope authorization bands

| Tier | Scope tendency |
|---:|---|
| 0 | Self, tool, immediate mundane context. |
| 1 | Self, close target, small object, short scene. |
| 2 | Small group, room/field context, reliable short-duration effect. |
| 3 | Encounter/site fragment, sustained technique, modest external anchor. |
| 4 | Site-scale, multi-target, persistent project, localized domain effect. |
| 5 | Scene-shaping, local-faction relevance, serious area/control effect. |
| 6 | Large site or moving battlefield, complex confluence, sustained field. |
| 7 | Major site/faction scale, dangerous domain pressure. |
| 8 | Region-scale or bounded law-scale influence. |
| 9 | World-facing/campaign-shaping influence. |
| 10 | World/plane-pressure and capstone transformation scale. |

Scope authorization is not automatic mastery.

## 18. Tier transition impact package

Each normal tier transition grants Scale Authorization, one Direct Tier Benefit, one Visibility Change, and one Future Unlock Notice. Tier 0→1 uses the Awakening Package instead of the normal tier menu. Tier 9→10 uses Capstone Procedure.

## 19. Filtered Tier Direct Benefit Menu

Normal tier transitions generate one legal Direct Tier Benefit from filtered categories:

1. Development Pick Upgrade
2. Axis Cap Raise
3. Breakthrough Window
4. Carrier / Slot / Capacity Adjustment
5. Expression Capacity or Refinement Opening
6. Power Economy Integration Opportunity
7. Route Stabilization or Branch Permission
8. Recovery / Resistance Improvement
9. Title / Achievement / Recognition Formalization
10. External Anchor Improvement
11. Scope License
12. Proof Conversion / Binding
13. Drift / Fusion Preparation
14. World / Faction / Territory Link

The menu is filtered by proof, route, tier, active axes, unresolved pressure, and owner-file validation.

## 20. Direct Tier Benefit categories

### Development Pick Upgrade

Gain an extra typed pick, upgrade a current pick's tier band, convert a held pick into a more relevant type, protect a held pick from staleness, or focus a pick on tier proof.

### Axis Cap Raise

Raise the ceiling of one registered axis. Does not fill the axis automatically.

### Breakthrough Window

Create a safer or clearer breakthrough opportunity. May mark an eligible vector ready, reduce risk posture if proof supports it, reveal requirements, or manage overripe pressure.

### Carrier / Slot / Capacity Adjustment

Improve one narrow structure that holds advancement. Major structural change still needs breakthrough or equivalent threshold.

### Expression Capacity or Refinement Opening

Permit one Expression-related improvement. Cannot create unrelated Expressions or exceed tier authorization.

### Power Economy Integration Opportunity

Deepen or stabilize one Power Economy relationship. Opportunity, not automatic mastery.

### Route Stabilization or Branch Permission

Clarify, stabilize, branch, or legally mutate route. Not free multi-pathing.

### Recovery / Resistance Improvement

Improve recovery or resistance against one known cost, scar, instability, corruption pattern, or harm pressure.

### Title / Achievement / Recognition Formalization

Formalize a title, achievement, reputation state, domain response, or recognition marker.

### External Anchor Improvement

Improve tool, relic, companion, platform, ship, implant, territory, or domain site as part of transition.

### Scope License

Gain permission to attempt broader version of known action/Expression. License is not mastery.

### Proof Conversion / Binding

Bind or transform proof into formal structure such as title seed, affinity seed, route support, domain contact, or future requirement.

### Drift / Fusion Preparation

Permit controlled divergence, convergence, hybridization, or route syncretism preparation.

### World / Faction / Territory Link

Create or strengthen external world-state connection.

## 21. Tier-band benefit restrictions

| Transition | Preferred benefit types |
|---|---|
| Tier 0→1 | Awakening Package, not normal tier menu. |
| Tier 1→2 | Pick upgrade, axis cap, Expression refinement, route stabilization, recovery, title formalization. |
| Tier 2→3 | Structural relevance: carrier/slot/capacity, breakthrough window, economy integration, route branch, drift/fusion prep. |
| Tier 3→4 | Axis cap, Expression refinement, scope license, external anchor, route stabilization, proof binding. |
| Tier 4→5 | Breakthrough window, scope license, recognition, economy integration, world/faction/territory link. |
| Tier 5→6 | Recovery/resistance, drift/fusion, economy stabilization, breakthrough window, route stabilization, scar integration. |
| Tier 6→7 | High-risk breakthrough window, major axis cap, scope license, high-tier Expression opening, external anchor, recognition. |
| Tier 7→8 | Site/region scope, whole-character breakthrough prep, domain recognition, external anchor/territory, rare economy mastery. |
| Tier 8→9 | Mythic title, world-facing recognition, route fusion/severance prep, high-tier economy transformation, mythic axis cap. |
| Tier 9→10 | Capstone Procedure, not normal tier menu. |

## 22. Pending Tier Benefit

If no legal target exists, a Direct Tier Benefit becomes pending.

| Pending state | Meaning |
|---|---|
| Pending Proof | Need additional proof. |
| Pending Owner File | Downstream doctrine/schema needed. |
| Pending Route | Need route clarification. |
| Pending Structure | Need breakthrough, carrier, economy, slot, anchor, or recovery. |
| Pending Choice | Player must choose direction. |
| Pending Project | Benefit becomes a project. |
| Deferred Benefit | Held until legal target emerges. |

## 23. Tier Direct Benefit validation

```yaml
tier_direct_benefit:
  benefit_id: string
  tier_transition: string
  benefit_category: string
  target: string
  proof_basis: [string]
  owner_file: D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | source_local
  tier_authorization_dimension:
    - expression_grade
    - scope
    - axis_depth
    - breakthrough_payload
    - economy_complexity
    - route_complexity
    - external_anchor_scale
    - risk
    - recognition
    - world_state
  effect_scope: narrow | moderate | major | source_local
  structural_change: true | false
  breakthrough_required: true | false
  state_delta: string
  validation_result: authorized | pending | dangerous | source_local | blocked
```

Direct benefits are narrow or moderate by default. Major effects require breakthrough, capstone, special proof, structural threshold, owner-file approval, or source-local authorization.

## 24. Tier visibility changes

Tier visibility changes are proof/context-dependent, not fixed effects. Possible changes include body mark, aura/Animus pressure, reputation shift, faction recognition, domain response, title formation, sensory signature, hidden cosmic pressure, tool/relic resonance, world-state notice, UI state change, stealth/absence signature, archival recognition, territory change, or platform response.

## 25. Non-player tier applicability

Tier authorization may apply to major NPCs, companions, spirits, AIs, swarms, summons, relic-bound entities, items/relics/tools, platforms/ships/mechs, factions, territories, settlements, and source-local entities if owner files support it.

Owner files may use full tracking, abstracted tier bands, or source-local equivalents.

## 26. Validation rules

A level/tier/pick structure is invalid if it grants untyped advancement by doctrine; lets a pick bypass proof, route, tier, or owner-file validation; treats tier as mastery; treats Tier 10 as normal Tier 9+; uses fixed donor reward tables as Astra law; forces a bad tier benefit when no legal target exists; lets stored picks become generic stockpiled power without proof relation; assigns Awakening through a normal tier benefit; or assigns Capstone through normal direct tier menu.
