# D04-02 — Awakening and Dynamic Triadic Choice

Status: `doctrine-draft / accepted D04 design decisions`  
Layer: D04 advancement doctrine  
Owner: Awakening architecture  
Depends on: D04-01 Proof Bundles, D04-03 Level/Tier structure, D03 Power Economy and Expression Doctrine, D06 Path/Class/Dao later mechanics

## 1. Purpose

This file defines the Tier 0→1 transition, the level 5 Mortal Threshold, Dynamic Triadic Awakening, and the Structured Variable Awakening Package.

Awakening is the formalization of a lawful route generated from proof, pressure, desire, context, consequence, and transformation. It is not a generic class kit and not a freeform reward.

## 2. Mortal Threshold rule

Level 5 is the Mortal Threshold. It is a soft cap for Tier 0 and the normal point where Awakening Proof is checked.

A level 5 actor may awaken immediately if eligible, delay Awakening, continue gathering proof, remain mundane, pursue a route-seeking project, seek a teacher/faction/relic/anchor/domain/experiment/method, undergo forced/coerced/corrupted Awakening if the fiction lawfully supports it, or receive a warning that proceeding beyond the threshold may formalize a contextually appropriate route.

The threshold must not railroad a character into a preplanned route. The system may identify lawful routes even when the player did not preplan one.

## 3. Awakening Proof

Awakening requires a Proof Bundle with defining sufficiency. The bundle must identify or substitute for three components:

1. Catalyst
2. Route
3. Anchor

### 3.1 Catalyst

The catalyst is what makes Awakening possible now. Catalysts may include repeated practice reaching saturation, crisis, survival, grief, oath, craft culmination, discovery, teacher initiation, faction rite, relic contact, domain contact, forced experiment, corruption exposure, purification event, world-state change, route realization, impossible achievement, chosen desire, accidental contact, coerced event, or source-local trigger.

### 3.2 Route

The route is the lawful direction of becoming. Routes may arise from profession, Path/Class/Dao pressure, skill mastery, repeated action, title seed, achievement chain, proof cluster, attribute breakthrough, Power Economy contact, Expression theory, faction/teacher method, relic/tool bond, kinform or bloodline pressure, territory/domain relation, corruption or purification, world-state recognition, player-declared desire if proof supports it, or forced/coerced source.

D06 later owns the exact Path/Class/Dao mechanics. D04 records route formalization and route status.

### 3.3 Anchor

The anchor is what holds the route in a lawful structure. Anchors may include body/Vessel, Animus, Integrity, attribute threshold, Power Economy, Expression slot/carrier, tool, relic, implant, companion, faction, teacher, oath, domain, territory, profession pattern, Scrypta inscription, route ledger, external platform, or source-local mechanism.

No Awakening Package may remain mechanically undefined. If no anchor exists, the route remains pending, unstable, dangerous, or project-bound.

## 4. Dynamic Triadic Awakening

When Awakening is ready, the system should normally present three potential routes. The three options represent three lawful versions of what the proof could become. They are not random class choices. They are generated from proof clusters, contextual weight, route pressure, Catalyst/Route/Anchor, player desire, and owner-file constraints.

The three options should not all be the same route with cosmetic names.

## 5. Triadic option roles

| Option role | Meaning |
|---|---|
| Dominant | Strongest proof cluster becomes route. |
| Parallel | Another major proof cluster becomes alternate route. |
| Fusion | Two or more compatible clusters combine. |
| Scarred | Cost, grief, corruption, injury, failure, or loss defines route. |
| Aspirational | Player-declared desire shapes route if proof supports it. |
| Professional | Mundane profession transmuted into ascendant route. |
| Tool-anchored | Route depends on tool, relic, gear, platform, or item. |
| Domain-bound | Route depends on place, realm, ecology, material, or concept. |
| Coerced | Route is imposed by faction, entity, curse, experiment, law, or pressure. |
| Refusal-born | Route forms from what the actor refused to become. |
| Latent | Old proof or hidden potential emerges. |
| Common | Accessible, stable, low-risk version. |
| Rare | More specific, stronger, stranger, or more costly option. |
| Source-local | Bounded option valid in campaign/source-local context. |

## 6. Multiple proof cluster handling

If an actor has multiple meaningful lives, the system must distribute proof rather than forcing a single route. A character who splits their life between fishing and baking should not have every proof record collapsed into whichever cluster is loudest. Dynamic Triadic Awakening should reveal the three most lawful choices, not every possible choice.

Proof clusters may create parallel routes, fusion routes, scarred routes, professional routes, source-local routes, latent routes, or future drift/fusion pressure.

## 7. Examples

### 7.1 Fisher example

Proof: lifelong fishing, desire to catch the largest fish on many planets, memory of a wanderer's saying, route-seeking desire.

Possible options:

1. Far Fisher — long-range pursuit, navigation, impossible catch, line/current route.
2. Barbarous Bait — self-risk, lure, predator invitation, survival route.
3. Wishful Waters — trance, desire, water influence, target-luring route.

### 7.2 Baker and wolves example

Proof: baker identity, family killed by wolves, repeated wolf-slaying, grief, protection, role contradiction.

Possible options:

1. Hearth Wolfbane — hearth/protection/anti-pack route.
2. Scarred Pack-Lure — bait, vengeance, predator-sense route.
3. Bread of the Safe Door — protection, community, warding, nourishment route.

### 7.3 Blacksmith example

Proof: repeated sword crafting, craft mastery, tool familiarity, possible exceptional project.

Possible options:

1. Hundred-Blade Smith — craft route, blade pattern, tool carrier.
2. Starforge Initiate — Calora/Aethra/Scrypta pressure if proof supports.
3. Tempered Vessel — body-as-forge route if repeated labor transformed body/discipline.

## 8. Warning requirement

Before a character proceeds past the Mortal Threshold, the system must warn the player that proceeding may formalize a route.

Functional warning:

```text
Your proof has begun to gather into a route. If you advance past this threshold, the system will formalize one of the lawful paths your life has made possible. You may proceed, delay, seek more proof, or redirect your effort before accepting.
```

In live play, narration may be contextual. The mechanical warning must still occur.

## 9. Structured Variable Awakening Package

D04 uses a Structured Variable Awakening Package. Every package has required slots, but the contents vary by proof, route, actor type, access vector, and chosen option.

Required package components:

1. Formalized Route Identity
2. Awakening Vector Record
3. Initial Access Vector
4. Initial Capacity / Carrier State
5. Starter Method or Expression Seed
6. Awakening Development Pick
7. Route Ledger Initialization
8. Unselected Option Ledger
9. Awakening Mark / Visibility Change
10. Cost, Scar, Debt, Claim, or Constraint if applicable
11. Tier 1 Authorization Activation
12. Safety and Scope Limits

## 10. Formalized Route Identity

The chosen Awakening option becomes the first formal ascendant route. This may later be represented through Path/Class/Dao terminology, but D06 owns exact mechanics.

Examples include Far Fisher, Barbarous Bait, Wishful Waters, Hearth Wolfbane, Hundred-Blade Smith, Starforge Apprentice, Relic-Bound Cartographer, Reticula Initiate, Tide-Oath Medic, and Scarred Vessel of the Red Pack.

## 11. Awakening Vector Record

```yaml
awakening_vector:
  chosen_option: string
  presentation_role: dominant | parallel | fusion | scarred | aspirational | professional | tool_anchored | domain_bound | coerced | refusal_born | latent | common | rare | source_local
  catalyst_refs: [string]
  route_refs: [string]
  anchor_refs: [string]
  proof_cluster_refs: [string]
  contextual_weight_summary: string
  player_intent_note: string
  route_status: formalized | unstable | coerced | corrupted | externalized | source_local
```

This prevents route assignment from becoming arbitrary.

## 12. Initial Access Vector

Every Awakening Package must identify the first lawful ascendant access.

| Access vector | Meaning |
|---|---|
| First Power Economy | Actor integrates Mistra, Zi, Volith, Scrypta, or another economy. |
| External Anchor | Power is mediated through relic, tool, implant, ship, companion, place, faction, or domain. |
| Profession Transmutation | A mundane profession becomes an ascendant route. |
| Expression Inscription | First retained Expression becomes entry structure. |
| Attribute Breakthrough | One attribute lattice opens route. |
| Whole-character Breakthrough | Actor crosses through structural transformation. |
| Faction/Teacher Initiation | Institution or mentor grants method. |
| Tech/Platform Access | Device, network, AI, ship, implant, exosystem, or platform grants route. |
| Relic/Tool Bond | Object becomes route-holder or burden carrier. |
| Domain Contact | Place, principle, material, ecology, or force recognizes the actor. |
| Pact/Vow/Debt | Access comes through oath, bargain, or obligation. |
| Forced/Coerced Route | Access occurs through hostile, experimental, cursed, or imposed method. |
| Source-local Route | Campaign or conversion-specific mechanism. |

## 13. Initial Capacity / Carrier State

Awakening must initialize minimum legal capacity. Possible carrier states include first ascendant carrier slot, initial Expression capacity, externalized carrier, tool-bound carrier, economy partition, route-bound carrier, companion-mediated carrier, profession carrier, scarred carrier, unstable carrier, and sealed/dormant carrier.

Awakening grants enough structure to begin Tier 1, not unlimited capacity.

## 14. Starter Method or Expression Seed

Awakening usually grants a starter method, route action, prototype Expression, stable low-grade Expression, tool protocol, domain sense, training form, or equivalent first method.

Rule: Awakening grants a lawful first method, not mastery.

Starter methods must remain within Tier 1 authorization and D03/D06 validation.

## 15. Awakening Development Pick

Tier 1 entry grants one Awakening Development Pick. It is not a normal open pick. It is shaped by the chosen route and may be spent on stabilizing initial access vector, refining starter method, improving initial carrier tolerance, formalizing a title or achievement from pre-awakening proof, advancing primary route axis, reducing instability from forced/scarred Awakening, strengthening external anchor, preparing first Tier 1 Expression, or opening a training route.

## 16. Route Ledger Initialization

The selected route becomes active in the route ledger.

| State | Meaning |
|---|---|
| Stable | Route is cleanly formalized. |
| Unstable | Route works but needs stabilization. |
| Scarred | Route is marked by cost, grief, injury, or consequence. |
| Coerced | Route was accepted under pressure. |
| Forced | Route was imposed or triggered without clean consent. |
| Corrupted | Route carries hostile influence or Vitia pressure. |
| Externalized | Route depends on tool, relic, companion, territory, platform, faction, or place. |
| Source-local | Route is valid only under bounded source-local rules. |
| Dormant-secondary | Route exists but is not the chosen primary. |

## 17. Unselected Option Ledger

The two unchosen Awakening options remain recorded. They may become latent routes, rejected routes, dormant routes, future drift routes, fusion candidates, scarred options, rival-route pressure, lost opportunities, or source-local hooks.

```yaml
unselected_routes:
  - route_name: Barbarous Bait
    ledger_state: latent
    recovery_condition: self-risk/predator-lure proof
  - route_name: Wishful Waters
    ledger_state: dormant
    recovery_condition: trance/water/domain proof
```

## 18. Awakening Mark / Visibility Change

Every Awakening should create a state-visible change, but it need not be flashy.

Possible marks include body mark, aura/Animus pressure, tool resonance, profession sign, domain response, faction notice, sensory change, hidden backend change, title seed, dream/omen, altered assessment output, external anchor transformation, and world-state recognition.

A stealth route may become less visible, not more visible. A scholar route may change how hidden information appears. A blacksmith route may change how metal answers. A fisherman route may change how line, water, or prey respond.

## 19. Cost, Scar, Debt, Claim, or Constraint

Not every Awakening has a severe cost, but dangerous awakenings must record consequence.

Forced, coerced, corrupted, hostile, dangerous, or source-local Awakening Packages must record attached consequence: constraint, claim, scar, debt, faction obligation, entity pressure, instability, corruption trace, carrier strain, correction path, severance option, purification route, or resistance state.

Such awakenings do not become clean just because the character survives or selects them.

## 20. Package variants

| Variant | Features |
|---|---|
| Clean | Stable route, clear starter method, initial carrier, Awakening Pick, ordinary visibility change. |
| Scarred | Scarred route quality, stronger specific option, vulnerability/constraint, rare benefit, scar ledger. |
| Externalized | External anchor, external carrier, dependency condition, anchor improvement option. |
| Forced/Coerced | Forced route state, resistance/severance option, claim/debt/faction/entity record, possible instability. |
| Corrupted | Vitia/hostile influence, corruption trace, purification/quarantine route, risk pressure. |
| Fusion | Multiple proof clusters merge; higher complexity, instability, unique starter method. |
| Source-local | Bounded validity, source-local ledger reference, limits on generalization. |

## 21. Tier 1 Authorization Activation

After Awakening, Tier 1 authorizes low-grade stable Expressions, initial Power Economy or equivalent access, Tier 1 Development Picks, basic ascendant axis visibility, early route development, first breakthrough payloads, formal route ledger, and early external anchor growth.

It does not authorize high-grade Expressions, broad multi-economy fusion, major world-scale effects, unrestricted Path/Class/Dao features, deep confluence, or capstone route access.

## 22. Safety and Scope Limits

The Awakening Package must state initial limits: starter method grade, carrier burden limit, current instability, external anchor dependency, route drift risk, unavailable higher expressions, required training/proof for next step, and legal Development Pick options now available.

## 23. Boundaries

D04 owns the Awakening Package structure. D04 does not own final route features, final Expression mechanics, final power math, exact scar mechanics, relic/tool/platform schemas, or faction/world consequences.

## 24. Validation rules

An Awakening Package is invalid if it lacks an Initial Access Vector; lacks route identity or route ledger state; grants unrestricted power; ignores unselected route ledger handling; treats forced/coerced/corrupted awakening as clean without consequence; bypasses D03/D06 validation for starter methods; gives Tier 1 a high-grade Expression without special source-local escalation; or forgets safety and scope limits.
