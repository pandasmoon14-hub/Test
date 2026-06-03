# D04-01 — Proof Events and Proof Handling Ledger

Status: `doctrine-draft / accepted D04 design decisions`  
Layer: D04 advancement doctrine  
Owner: proof architecture  
Feeds: Awakening, tier transitions, Development Picks, breakthroughs, titles, achievements, route drift/fusion, capstone, runtime proof ledger

## 1. Purpose

This file defines how Astra records proof and decides whether proof is sufficient for advancement.

Proof is not XP. Proof is the recorded shape of what a character has handled, endured, repeated, chosen, refused, changed, paid, repaired, transformed, or become.

D04 uses structured Proof Bundles rather than flat proof points.

## 2. Core proof principle

A Proof Bundle evaluates whether the character has demonstrated the right kind of capacity for the requested advancement.

A Proof Bundle asks:

- What happened?
- How did the actor handle it?
- How hard was it for this actor?
- What did it cost?
- What changed afterward?
- What route, axis, title, breakthrough, tier, or transformation does it support?
- Does it align, branch, contradict, corrupt, coerce, or rewrite the character's route?

## 3. Proof event versus proof handling

A proof event is the recorded occurrence.

A proof handling record is how the actor dealt with the occurrence.

D04 prioritizes handling over raw event existence. A hunter killing one wolf, a hunter killing 100 wolves, a baker killing one wolf, and a baker killing 100 wolves after wolves killed their family are different proof records because the handling, contextual weight, role relationship, cost, and transformation are different.

A proof event without handling may be weak evidence. A modest event handled in a rare, costly, repeated, role-defining, or transformative way may become strong proof.

## 4. Proof Event Record

A proof event should record the visible event.

```yaml
proof_event:
  proof_event_id: string
  actor_ref: string
  event_summary: string
  event_type:
    - action
    - trial
    - training
    - craft
    - study
    - exploration
    - survival
    - social
    - faction
    - profession
    - bond
    - item
    - relic
    - territory
    - corruption
    - purification
    - sacrifice
    - recovery
    - failure
    - victory
    - discovery
    - refusal
    - forced_event
    - coerced_event
    - source_local
  scene_refs: [string]
  time_span: instant | scene | downtime | journey | season | years | generational | unknown
  witnesses: [string]
  location_refs: [string]
  opposition_refs: [string]
  object_refs: [string]
  route_refs: [string]
  axis_refs: [string]
  source_local_boundary: string | null
  extraction_or_conversion_refs: [string]
  status: active | superseded | disputed | source_local | quarantined
```

## 5. Proof Handling Record

A proof handling record captures what advancement actually learns from the event.

```yaml
proof_handling:
  proof_handling_id: string
  proof_event_ref: string
  actor_ref: string
  handling_summary: string
  handling_modes:
    - endured
    - solved
    - mastered
    - repeated
    - resisted
    - sacrificed
    - protected
    - created
    - repaired
    - transformed
    - taught
    - studied
    - discovered
    - failed_and_adapted
    - refused
    - accepted
    - integrated
    - severed
    - exploited
    - corrupted
    - purified
    - externalized
    - bound
    - bargained
    - coerced
    - survived
    - outgrew
  cost_paid:
    - resource
    - injury
    - scar
    - time
    - relationship
    - reputation
    - debt
    - memory
    - opportunity
    - item
    - territory
    - oath
    - route
    - expression
    - economy_pressure
    - corruption
    - identity_pressure
    - none
  outcome_state:
    - clean
    - costly
    - scarred
    - unstable
    - corrupted
    - coerced
    - refused
    - transformed
    - unresolved
  proof_families: [string]
  contextual_weight_factors: [string]
  alignment_state: aligned | adjacent | branching | convergent | divergent | contradictory | corrupted | coerced | insufficient | unknown
  sufficiency_estimate: trace | seed | credible | established | weighty | defining | mythic | capstone
  notes: string
```

## 6. Proof families

Proof families are broad categories used for bundle construction. They are not final skill names and not canon titles.

| Family | Meaning |
|---|---|
| Practice Proof | Repetition, training, refinement, discipline, routine competence. |
| Trial Proof | Surviving or resolving danger, crisis, contest, hardship, or opposition. |
| Craft Proof | Creating, repairing, improving, refining, or completing work. |
| Profession Proof | Acting through a sustained profession, trade, service, calling, role, or labor identity. |
| Study Proof | Research, analysis, theory, recordkeeping, comprehension, experimentation. |
| Discovery Proof | Finding, revealing, mapping, identifying, or understanding unknown things. |
| Combat Proof | Fighting, hunting, defending, dueling, slaying, surviving battle, tactical growth. |
| Protection Proof | Guarding, sheltering, healing, rescuing, preserving, defending dependents or place. |
| Sacrifice Proof | Paying meaningful cost for goal, route, person, place, oath, or transformation. |
| Recovery Proof | Healing, rebuilding, adapting after failure, integrating injury, overcoming breakdown. |
| Corruption Proof | Contact with hostile, forbidden, degenerative, unstable, or Vitia-like pressure. |
| Purification Proof | Cleansing, reconciling, transforming, quarantining, or redeeming hostile pressure. |
| Social Proof | Leadership, negotiation, oath, reputation, service, community, politics, institution. |
| Faction Proof | Rank, standing, conflict, alliance, duty, rebellion, recognition, law, scrutiny. |
| Bond Proof | Companion, familiar, mount, spirit, AI, relic, family, mentor, community, sworn relation. |
| Item/Relic Proof | Object attunement, tool growth, relic bond, craft anchor, externalized carrier. |
| Territory Proof | Place, settlement, domain, farm, forge, ship, stronghold, route, ecology, world-state. |
| Exploration Proof | Travel, mapping, crossing boundaries, surviving unknown regions, route discovery. |
| Codex Proof | Monster study, bestiary completion, language, lore, taxonomy, archive, map completion. |
| Identity Proof | Choice, refusal, transformation, acceptance, contradiction, personal route definition. |
| World-State Proof | Lasting change to faction, settlement, ecology, law, domain, plane, route, history, memory. |
| Source-local Proof | Bounded proof valid in a local conversion, campaign, faction, world, or source mechanism. |

## 7. Proof sufficiency bands

D04 uses sufficiency bands to avoid hard-coded proof points while still supporting validation.

| Band | Meaning | Typical use |
|---|---|---|
| Trace | Contact, rumor, weak exposure, early clue, faint pattern. | Route seed, future project, theory, hidden option clue. |
| Seed | Meaningful first sign. | Awakening vector candidate, title seed, affinity seed, axis reveal. |
| Credible | Enough proof to justify a minor legal option. | Development Pick target, minor axis progress, project unlock. |
| Established | Repeated or well-supported proof. | Standard tier progress, stable axis advancement, reliable route support. |
| Weighty | Serious proof with cost, difficulty, achievement, or structural pressure. | Structural proof, major title, breakthrough prep, route mutation. |
| Defining | Character-shaping proof. | Awakening option, major breakthrough, route fusion, identity transformation. |
| Mythic | Campaign-shaping, world-facing, or legendary proof. | Tier 8–9 transitions, mythic titles, major world-state impact. |
| Capstone | Endgame-grade proof with world/plane/identity consequence. | Tier 10, levels 95–100, final-form resolution. |

## 8. Proof Bundle anatomy

A Proof Bundle is a structured eligibility package.

```yaml
proof_bundle:
  bundle_id: string
  actor_ref: string
  bundle_type:
    - development_pick
    - awakening
    - tier_transition
    - breakthrough
    - axis_threshold
    - title_achievement
    - route_drift
    - route_fusion
    - capstone
    - ascension_access
  requested_outcome: string
  required_sufficiency_band: trace | seed | credible | established | weighty | defining | mythic | capstone
  required_proof_families: [string]
  optional_proof_families: [string]
  required_handling_modes: [string]
  minimum_intensity: minor | standard | major | apex | mythic | capstone
  contextual_weight_required: none | low | moderate | high | extreme
  alignment_requirement:
    - aligned
    - adjacent
    - branching
    - convergent
    - divergent_allowed
    - contradictory_requires_resolution
  structural_requirement:
    required: true | false
    acceptable_structures: [carrier, slot, route, economy, expression, attribute_threshold, path_branch, reservoir, identity_coherence, external_anchor]
  cost_or_consequence_requirement:
    required: true | false
    acceptable_costs: [string]
  recognition_requirement:
    required: true | false
    scale: personal | witnessed | faction | local | regional | world | mythic | capstone | hidden_cosmic | source_local
  warning_required: true | false
  output_if_ready: authorized | authorized_with_warning | pending_choice
  output_if_not_ready: pending_proof | pending_structure | pending_route | pending_cost | pending_recognition | blocked
```

## 9. Bundle calibration by gate

### 9.1 Development Pick Bundle

Used when spending a normal level pick.

- Sufficiency: usually `credible`.
- Breadth: 1–2 proof families is usually enough.
- Depth: at least one handling record or active axis.
- Intensity: minor to standard.
- Contextual weight: low to moderate.
- Structural proof: not required unless the target is structural.
- Recognition: not required.

Example: a blacksmith spends a Skill/Profession Pick to advance Blacksmithing. Craft Proof + Practice Proof is sufficient if owner-file rules allow it.

### 9.2 Title / Achievement Bundle

Used when formalizing a title, achievement, affinity seed, route seed, or milestone.

- Sufficiency: seed to defining depending on title scale.
- Breadth: usually 2–4 proof families.
- Depth: repetition, cost, difficulty, recognition, transformation, or lasting change.
- Contextual weight: important.
- Recognition: personal/witnessed/local for ordinary titles; broader titles need broader recognition.

Example: `Hundred-Wolf Baker` requires stronger contextual weight than `Wolf Hunter` because the role contradiction and grief anchor change what the proof means.

### 9.3 Awakening Proof Bundle

Used for Tier 0→1.

- Sufficiency: defining.
- Required components: Catalyst + Route + Anchor.
- Breadth: at least 3 proof dimensions.
- Depth: at least one meaningful pattern or major event.
- Intensity: standard minimum; major proof can create rarer options.
- Contextual weight: moderate to high.
- Alignment: must support at least one lawful Awakening Vector.
- Warning: required.
- Output: Dynamic Triadic Awakening options.

Awakening does not require a planned path, but it requires enough convergence that the system can generate lawful routes.

### 9.4 Standard Tier Transition Bundle

Used for ordinary tier transitions such as Tier 1→2 and Tier 3→4.

- Sufficiency: established.
- Breadth: 2–3 proof families.
- Depth: sustained activity in current route or axis.
- Intensity: standard.
- Contextual weight: moderate.
- Structural proof: not always required.
- Recognition: personal or witnessed is enough unless tier demands more.

### 9.5 Standard + Structural Proof Bundle

Used for Tier 2→3.

- Sufficiency: weighty.
- Breadth: 3+ proof families.
- Depth: clear growth pattern.
- Intensity: standard to major.
- Structural proof: required.
- Acceptable structures: carrier, slot, route, Power Economy, Expression, attribute threshold, path branch, reservoir, identity coherence, external anchor.
- Warning: required if structural change is unstable.

Tier 2→3 proves the character is not merely gaining power; they are becoming structurally capable of deeper ascendant development.

### 9.6 Major Tier Bundle

Used for Tier 4→5 and similar major transitions.

- Sufficiency: weighty to defining.
- Breadth: 3–5 proof families.
- Intensity: major minimum.
- Cost/consequence: usually required.
- Recognition: witnessed, local, or faction response likely.
- Structural proof: often required, but may be route/world/proof based.
- Output: major scale authorization.

### 9.7 Major + Pressure Bundle

Used for Tier 5→6.

- Sufficiency: defining.
- Required pressure: identity, economy, Expression, route, carrier, or world pressure.
- Breadth: 4+ proof families.
- Intensity: major.
- Cost/consequence: required.
- Alignment: must address route strain, drift, or contradiction.
- Warning: often required.

This transition asks whether the character can keep coherence under deeper complexity.

### 9.8 Apex, Transcendent, and Mythic Bundles

| Band | Used for | Required sufficiency | Key requirement |
|---|---|---|---|
| Apex | Tier 6→7 | defining | Severe pressure, high-risk proof, major opposition or transformation. |
| Transcendent | Tier 7→8 | defining to mythic | Site/region-scale consequence, law/domain pressure, rare proof. |
| Mythic | Tier 8→9 | mythic | Campaign-shaping consequence, world/faction/domain recognition. |

These bundles require proof that the actor's actions matter beyond ordinary personal advancement.

### 9.9 Capstone Proof Bundle

Used for Tier 9→10 and levels 95–100.

- Sufficiency: capstone.
- Breadth: multiple high-grade proof families.
- Intensity: capstone.
- Cost/consequence: required.
- World/recognition: required or equivalent hidden/cosmic/source-local response.
- Identity resolution: required.
- Mastery or axis culmination: required.
- Whole-character breakthrough: often required.
- Single-route restriction: prohibited.

Capstone proof must be nearly impossible to satisfy accidentally, but possible through many life paths.

## 10. Breadth, depth, intensity, and contextual weight

### Breadth

Breadth measures how many different proof families are involved.

Low breadth: only repetition, only combat, only training.  
High breadth: practice + cost + discovery + world consequence + identity transformation.

### Depth

Depth measures whether proof has been sustained and integrated.

Depth increases through repetition with improvement, repeated handling records, teaching, failure correction, long-term project completion, identity integration, route consistency, mastery, axis progress, and lasting world response.

### Intensity

Intensity measures severity, rarity, cost, danger, or consequence.

Intensity increases through danger, mismatch, sacrifice, grief, world response, rare discovery, impossible conditions, high-tier opposition, corruption risk, lethal risk, and scale increase.

### Contextual Weight

Contextual Weight modifies proof significance based on who the actor is and how the event fits the actor.

| Factor | Effect |
|---|---|
| Role alignment | Reliable proof for aligned routes. |
| Role contradiction | Increases uniqueness when action is unusual for the actor. |
| Difficulty mismatch | Actor was underqualified, under-resourced, or outmatched. |
| Emotional anchor | Grief, love, devotion, fear, obsession, wonder, shame, duty, vengeance. |
| Cost paid | Injury, loss, debt, corruption, opportunity, reputation, relationship. |
| Repetition beyond normal | Continued pursuit beyond ordinary completion. |
| World response | Factions, places, enemies, communities, domains, or hidden systems react. |
| Transformation signal | Actor changed behavior, identity, body, route, future, or world relation. |
| Scar or consequence | Lasting mark gives proof weight. |
| Player-declared desire | Shapes route relevance but does not override missing proof. |
| Hidden pressure | Backend-only factors may alter route generation, not player-visible proof math. |

## 11. Multiple proof clusters and distributed proof

Proof should not collapse into one dominant route when an actor has multiple meaningful lives.

If the same actor is both baker and fisher, or smith and wolf-slayer, or scholar and relic-bound wanderer, proof must be clustered and distributed.

Proof clusters may become:

- parallel Awakening options;
- fusion routes;
- dormant routes;
- split routes;
- rival routes;
- branch candidates;
- title seeds;
- axis seeds;
- future drift/fusion pressure.

The system should not force every proof record into the first route it identifies.

## 12. Proof conflicts and contradiction states

A proof bundle may have these fit states:

| State | Meaning |
|---|---|
| Clean fit | Proof supports requested outcome. |
| Adjacent fit | Proof supports a nearby outcome. |
| Split fit | Proof supports multiple outcomes. |
| Drift fit | Proof supports route change. |
| Contradictory fit | Proof supports conflicting outcomes. |
| Corrupted fit | Proof supports outcome through hostile/degenerative route. |
| Coerced fit | Proof supports outcome but agency was compromised. |
| Insufficient fit | Proof exists but does not support this request. |

Contradictory proof can produce warnings, route drift, unstable breakthrough, fusion opportunity, delayed authorization, forced choice, scarred option, or project requirement.

## 13. Proof handling modes

Proof is usually not spent. History remains.

| Mode | Meaning |
|---|---|
| Referenced | Proof supports eligibility but remains part of history. |
| Bound | Proof becomes attached to a title, route, axis, breakthrough, or formal state. |
| Transformed | Proof becomes a new structure: affinity, title, route, scar, achievement, capability. |
| Corrupted | Proof remains valid but carries taint, contradiction, coercion, or instability. |
| Rejected | Player rejects a route or offer generated by proof; proof remains but changes ledger state. |
| Spent | Rare; used for bargains, consumable opportunities, source-local mechanics, unstable rituals, or one-time transformations. |

## 14. Proof Bundle outputs

A bundle should never be pass/fail only.

| Output | Meaning |
|---|---|
| Authorized | Bundle satisfies gate. |
| Authorized with warning | Gate can proceed, but risk/formalization/consequence exists. |
| Pending breadth | Need more proof families. |
| Pending depth | Need sustained practice, repetition, mastery, or integration. |
| Pending intensity | Need a stronger trial, cost, risk, or meaningful event. |
| Pending contextual weight | Proof exists, but it is not character-defining enough. |
| Pending structural proof | Need carrier, route, economy, Expression, identity, or axis change. |
| Pending recognition | Needs witness, faction, world, domain, title, or hidden recognition. |
| Split route | Multiple proof clusters compete. |
| Fusion possible | Multiple proof clusters can lawfully combine. |
| Contradiction unresolved | Proof conflicts must be handled. |
| Dangerous authorization | Proceeding is possible but risky. |
| Source-local only | Valid only in bounded source-local context. |
| Blocked | No lawful bundle fit. |

## 15. Examples

### 15.1 Hunter killing a wolf

Proof families: Combat Proof, Profession Proof if hunting is established.  
Likely sufficiency: trace or seed unless repeated or costly.  
Likely outputs: ordinary proof record, possible bestiary/codex seed, no rare route by default.

### 15.2 Hunter killing 100 wolves

Proof families: Combat Proof, Profession Proof, Repetition, Survival, possible Territory Proof.  
Likely sufficiency: credible to established.  
Likely outputs: wolf-slaying title seed, anti-pack axis, bestiary/codex growth, possible route seed if contextual weight supports.

### 15.3 Baker killing one wolf

Proof families: Combat Proof, Role Contradiction, Survival, possibly Protection.  
Likely sufficiency: seed due to role contradiction.  
Likely outputs: unusual proof marker, possible route clue, not enough alone for major Awakening unless intensity/cost is high.

### 15.4 Baker killing 100 wolves after family was killed by wolves

Proof families: Combat Proof, Grief/Emotional Anchor, Role Contradiction, Repetition, Sacrifice, Protection, Identity Proof.  
Likely sufficiency: weighty or defining if handled consistently.  
Likely outputs: Hearth Wolfbane route option, title seed, scarred Awakening option, anti-pack axis, grief-scar integration choice.

### 15.5 Blacksmith crafting 100 swords

Proof families: Craft Proof, Profession Proof, Practice Proof.  
Likely sufficiency: credible or established depending quality and handling.  
Likely outputs: profession axis progress, title seed, tool-anchor project, craft route seed.

### 15.6 Blacksmith crafting 10,000 swords

Proof families: Craft Proof, Profession Proof, Practice Proof, Identity Proof, Endurance/Time Proof.  
Likely sufficiency: weighty or defining if the work transformed the actor.  
Likely outputs: rare profession route, Hundred-Blade Smith title, forge-pattern carrier, Scrypta/Calora/Zi-related access vector if supported by proof.

## 16. Validation rules

A Proof Bundle is invalid if:

- it has no proof event references;
- it ignores handling records;
- it treats proof as generic spendable currency by default;
- it converts unrelated proof into unrelated power without drift/fusion logic;
- it hides a contradiction that should be recorded;
- it grants capstone proof from a single ordinary event;
- it satisfies Awakening without Catalyst, Route, and Anchor or equivalent owner-file substitute;
- it treats hidden backend pressure as visible proof math;
- it bypasses owner-file validation.
