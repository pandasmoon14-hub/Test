# batchA_16_translation_pattern_library_and_edge_cases

## Purpose and authority

This file is the **conversion-stability operating manual** for the Astra doctrine stack. It exists to help later conversion work recognize recurring donor-side construct shapes, classify them structurally, route them to the correct Astra doctrine owners, and handle ambiguity without improvising fresh logic each time.

This file is authoritative for:
- translation-pattern recognition;
- pattern-axis classification;
- dominant-function routing;
- standard resolution-state vocabulary;
- cross-file routing templates;
- edge-case family handling;
- confidence grading, placeholder use, quarantine, and escalation triggers;
- promotion and demotion criteria for recurring patterns.

This file is **not** authoritative for new mechanics. It must not silently replace any Batch A or Batch B doctrine file. When a construct’s mechanical meaning is already owned elsewhere, this file only classifies and routes it.

Authority order remains:
1. current Astra doctrine files;
2. canonical Astra sourcebook material once formalized;
3. converted Astra-native donor content;
4. example packs / training examples;
5. original donor assumptions.

## Scope boundaries

This file owns **pattern recognition and routing**, not substantive rules content.

It must:
- identify recurring donor-side structural shapes;
- separate donor labels from donor jobs;
- determine primary and secondary Astra owners;
- define lawful resolution states;
- define lawful incomplete mapping behavior;
- specify when a construct should be quarantined or escalated.

It must not:
- invent a new chassis, action, damage, social, vehicle, site, item, or reward system;
- restate the whole contents of other doctrine files;
- turn into a donor-system index;
- become a catch-all appendix for unresolved content;
- perform full donor conversions.

A16 may include **classification examples**, but not full donor-native conversions.

## Why this file exists after A15

Astra first needed stable ownership boundaries and conversion invariants. Only after the core Batch A and Batch B stack exists is it useful to define a conversion meta-layer that teaches later conversion work how to classify recurring ambiguity and route it lawfully.

A15 established that conversion must preserve Astra doctrine, avoid donor leakage, and use explicit outcomes rather than decorative invention. A16 extends that work by defining **how recurring donor-side shapes are recognized and routed before content conversion multiplies edge cases across hundreds of sources**.

## Core conversion-meta principles

1. **Function outranks donor label.**
   A donor name such as skill, feat, talent, technique, relic, city, faction, boon, or companion is not self-authenticating. Structural job matters more than vocabulary.

2. **Pattern outranks novelty.**
   Most difficult donor constructs are not unique. They recur in slightly different surface forms. Conversion stability depends on recognizing the recurring pattern instead of solving each appearance as though it were singular.

3. **Dominant function routes first.**
   When a construct spans multiple doctrine layers, classify its dominant doctrinal job first, then note secondary dependencies and handoffs.

4. **Hybrids are lawful.**
   A construct does not need to be forced into a false one-file answer. Split, fused, overlay, holder-linked, and cross-file outcomes are all lawful if classified explicitly.

5. **Uncertainty must be explicit.**
   If a construct is underspecified, contradictory, or incompletely formalized, the converter must use confidence grading, placeholder states, quarantine, or escalation rather than inventing unsupported details.

6. **Astra doctrine wins over donor shape.**
   If a donor bundle conflicts with Astra’s file ownership boundaries, the construct must be normalized into Astra’s architecture rather than copied wholesale.

7. **Promotion requires recurrence and pressure, not novelty.**
   A repeated donor-side pattern may justify stronger doctrine later. A vivid one-off oddity does not automatically deserve canon elevation.

## Pattern-axis matrix

Before routing any donor construct, classify it across the following axes.

### 1. Ontology axis
What kind of thing is it structurally?
- actor/entity
- auxiliary presence
- item/object
- service
- permission/right
- site
- institution/faction shell
- platform/frame
- state/condition
- resource/currency
- procedure/activity
- output/reward
- hybrid or actorized shell

### 2. Holder-linkage axis
What does it depend on to exist or function?
- independent
- character-linked
- party/crew-linked
- institution-linked
- site-linked
- item-linked
- platform-linked
- effect-linked
- route/access-linked
- environment-linked

### 3. Control-topology axis
How is it used or directed?
- self-acting
- commanded
- shared-bandwidth
- delegated
- station-based
- passive support
- triggered/conditional
- group-coordinated
- networked/distributed

### 4. Persistence axis
How long does it remain meaningful?
- instantaneous
- scene-bound
- encounter-bound
- interval-bound
- project-bound
- persistent
- dismissible/recallable
- replaceable
- bond-locked
- degrading/decaying

### 5. Time-scale axis
At what procedural scale does it mainly operate?
- action/round
- scene
- encounter
- travel interval
- downtime interval
- long project
- civic/site state
- campaign/arc scale

### 6. Access-mediation axis
What gates it?
- none/open use
- competency
- permission/clearance
- rank/tier
- membership/standing
- sponsor/patron
- payment/value
- token/permit/key
- legality/treaty
- environmental requirement
- bonded eligibility

### 7. Progression-statefulness axis
Does it change through growth, rank, upgrades, or stages?
- static
- scaling by holder
- scaling by direct investment
- scaling by modules/components
- scaling by site/service access
- staged transformation
- unlock tree
- mutable daily/interval state

### 8. Source-state vs output-state axis
Is it primarily a source, an output, or both?
- source state
- extraction method
- output family
- carry-forward state
- recursive source/output loop

### 9. Truth-status axis
What certainty assumptions attach to it?
- directly verified
- inferred
- lead-bearing only
- contested
- deceptive/misleading
- partially known
- unknown
- procedurally unavailable

The pattern-axis matrix exists to classify a construct **before** donor terminology biases routing.

## Pattern record format

Every significant recurring pattern should be recorded in a stable format.

### Standard pattern record fields
- `pattern_id`
- `pattern_name`
- `structural_signature`
- `pattern_axes`
- `common_donor_signals`
- `common_false_friends`
- `primary_astra_owner`
- `secondary_dependencies`
- `allowed_resolution_states`
- `forbidden_collapses`
- `confidence_notes`
- `escalation_triggers`
- `stress_test_examples`

### Pattern record use rules
- Records describe recurring **structural jobs**, not donor-specific lore.
- Records should be brief enough to remain usable in retrieval and conversion prompting.
- Records may include generic classification examples, but not full donor conversions.
- Records should be added when a pattern recurs across multiple donor families or clearly threatens ownership bleed.

## Dominant-function routing doctrine

When a donor construct touches multiple doctrine files, classify its **dominant doctrinal function** first.

### Dominant-function routing rule
1. Identify the construct’s primary job in play/conversion.
2. Assign the primary Astra owner.
3. Record secondary dependencies and handoffs.
4. Forbid collapsed treatment that allows one layer to silently swallow the others.

### Examples of dominant-function routing logic
- A living weapon may be primarily B03 if its main job is item ontology, but it may carry B13 auxiliary-presence notes and A07 granted-ability notes.
- A mobile city is primarily B15 if its dominant job is habitation, governance, districts, and infrastructure; it is secondarily B14 if motion/deployment matter.
- A corpse-questioning effect is primarily B16 as a post-pressure information-bearing output state and extraction channel, but its truth-status and interpretation hand off to B09.
- An eidolon-like partner is primarily B13 if it is a linked secondary actor/presence, even if it shares bandwidth with the holder and uses specialized equipment.
- A donor “investigation skill” that bundles noticing hidden things and interpreting a source must be split across B08 and B09 rather than copied whole.

### Dominant-function warning
Do not use donor chapter placement as dominant-function evidence. Donor books often cluster unlike constructs for convenience.

## Standard resolution states

All recurring translation outcomes should use a standardized vocabulary.

### Core resolution states
- **direct**: donor construct maps cleanly to an existing Astra owner with minimal normalization.
- **normalized**: donor construct maps to an existing Astra owner after Astra-native reframing, vocabulary change, or structural cleanup.
- **split**: one donor construct becomes multiple Astra constructs because the donor bundled unlike functions together.
- **fused**: multiple donor-side subparts become one Astra construct because Astra already formalizes them together.
- **overlay**: the donor construct modifies or rides atop another primary construct rather than existing as a standalone Astra object.
- **holder-linked**: the construct is meaningful only relative to a holder class and cannot be converted as a free-floating object.
- **placeholder**: the construct is recognizable and routable, but insufficiently specified for full conversion; it receives a lawful temporary shell.
- **quarantined**: the construct is real and pressure-bearing but cannot yet be converted without risking doctrine breach.
- **escalated**: the construct exposes genuinely missing doctrine and must trigger doctrinal review.

### Confidence grading
Each resolution state should also carry a confidence grade where useful:
- high-confidence direct
- high-confidence normalized
- medium-confidence split
- medium-confidence overlay
- low-confidence placeholder
- quarantine pending clarification
- escalate immediately

## Pattern families

The following pattern families are expected to recur across large donor corpora.

### 1. Direct-equivalent pattern
A donor construct already has a stable Astra-native home.

### 2. Normalized-equivalent pattern
The donor construct maps after vocabulary correction, scope cleanup, or Astra-native restructuring.

### 3. Split-construct pattern
One donor-side label actually contains multiple doctrinal jobs.

### 4. Fused-construct pattern
Several donor-side components are already one thing under Astra doctrine.

### 5. Overlay pattern
The construct modifies another object, actor, site, or frame rather than existing independently.

### 6. Holder-linked pattern
The construct cannot be understood without its bearer, host, institution, site, or platform.

### 7. Shared-bandwidth / paired pattern
The construct is operationally linked to another actor/frame through shared or constrained bandwidth.

### 8. Access-mediated pattern
The construct is primarily permissioned through rank, sponsor, token, institution, route, or clearance.

### 9. Stateful progression pattern
The construct changes through stages, upgrades, transformations, ranks, or mutable interval states.

### 10. Source-state / extraction / output pattern
The construct matters because it is a source, disposition method, or post-pressure output rather than a stable object.

### 11. Actorization pattern
A place, organization, hazard, vehicle, project, or other non-character shell is functionally treated as a character-like actor for operational purposes.

### 12. Task-fusion pattern
Training, assets, effort/resource spend, environment, permissions, and task execution are bundled into one donor engine and must be separated for Astra.

### 13. Service-vs-asset ambiguity pattern
The donor construct could be mistaken for an item or entity when it is better modeled as a service channel or vice versa.

### 14. Institution-vs-site ambiguity pattern
The donor uses one label for a political body, physical place, and service network at once.

### 15. Route-vs-permission ambiguity pattern
The thing gained looks like a physical reward but is structurally a right of transit, entry, use, or claim.

## Cross-file routing templates

A16 should provide reusable routing templates instead of only naming ambiguity.

### Template A: Primary owner + secondary dependency
Use when one file clearly owns the construct and another file only governs attached consequences.

### Template B: Primary owner + output handoff
Use when the construct is classified in one file but its outputs are governed elsewhere.

### Template C: Holder-linked overlay
Use when a construct modifies a holder without being an independent doctrine object.

### Template D: Shared-bandwidth pair
Use when two linked constructs must be modeled together without collapsing into one actor.

### Template E: Site shell + institution overlay
Use when a place and organized access body overlap but are not identical.

### Template F: Source state + extraction method + output family
Use for post-pressure outputs, harvesting, interrogation, salvage, claim rights, and similar sequences.

### Template G: Platform/frame + civic shell hybrid
Use when a moving or operational frame also hosts districts, governance, or infrastructure.

### Template H: Service channel + effect handoff
Use when access to a service is primary in one file but the service’s substantive effect belongs elsewhere.

## Edge-case family library

The following recurring ambiguities should be treated as formal edge-case families.

### Entity vs item
Living weapons, shard minds, semi-sentient relics, bonded tools, AI-laced gear, spirit implements.

### Entity vs platform
Rideable beast-cities, living transports, modular walkers, giant organism settlements, bonded mechs.

### Site vs faction vs institution
Temple-city, embassy-city, company compound, lawless market node, sect stronghold, treaty station.

### Skill vs ability vs permission
Talents, licenses, techniques, certifications, protocols, rituals, disciplines, or donor “skills” that actually mix competency, permission, and active power.

### Search vs study vs research
Donor “investigation” constructs that bundle noticing hidden things, extracting meaning, and archive work.

### Minion vs partner
Commanded auxiliaries, shared-bandwidth pairs, eidolon-like companions, AI copilots, bonded beasts.

### Body vs resource vs status
Stress, corruption, heat, taint, burnout, trauma, soul-fray, or similar tracks that span multiple Astra domains.

### Temporary vs persistent
Stances, forms, projections, summons, transformed states, recalled shells, interval-bound upgrades.

### Reward vs access right
Permits, titles, route keys, blessings, favor rights, bounty validation, sponsor claims.

### Service vs asset
A healer, archive, training right, teleporter access, AI support line, ritual hall, or legal hearing that may look like an owned asset but is structurally a service channel.

### Truth vs information access
Corpse-questioning, memory extraction, compelled testimony, sensor logs, prophetic traces, witness fragments.

### Actorization edge cases
Hazards, cities, factions, projects, routes, vehicles, and sites temporarily treated as actor-like entities for operational handling.

## Negative pattern doctrine

A16 must state not only what a construct is, but what it is **not allowed to be treated as**.

### Core negative rules
- A donor “skill” is not automatically a capability object.
- A donor tag is not automatically a permission or keyword of universal meaning.
- A city is not automatically one undivided civic shell.
- A bonded weapon is not automatically a normal item.
- A social concession is not automatically reputation gain.
- A corpse-questioning effect is not automatically verified truth.
- A temporary summon is not automatically a persistent companion.
- A faction name is not automatically an institution shell.
- A token is not automatically currency.
- A route key is not automatically physical treasure.
- A donor chapter title is not automatically the correct Astra owner.

Negative pattern doctrine exists to block silent collapse into convenient but false equivalence.

## Confidence grading and lawful incomplete mapping

### Confidence grades
- **High-confidence**: strong structural fit and clear Astra owner.
- **Medium-confidence**: recognizable pattern, but some routing or dependency ambiguity remains.
- **Low-confidence**: construct fits a pattern family but lacks enough detail for full resolution.

### Lawful incomplete mapping outcomes
When conversion evidence is incomplete, contradictory, or donor-local:
- use placeholder shells;
- record unresolved dependencies;
- state the confidence grade;
- quarantine if doctrinal risk is high;
- escalate if the pattern recurs or reveals missing doctrine.

### Anti-false-certainty rule
Never decorate missing structure with Astra-sounding invention merely to avoid admitting uncertainty.

## Quarantine and escalation triggers

### Quarantine when:
- the construct is clearly real and important but cannot be absorbed without breaking existing doctrine;
- the donor description is too incomplete for even placeholder classification;
- the construct appears to depend on missing metaphysics or absent framework law;
- multiple plausible owners exist and no dominant function can yet be defended.

### Escalate when:
- the same unresolved pattern appears repeatedly across donor families;
- a hybrid pattern exposes a missing doctrinal layer rather than a one-off ambiguity;
- existing files cannot jointly route the construct without contradiction;
- the construct would force repeated ad hoc invention during real conversion.

### Escalation note
Escalation is a doctrine problem, not a conversion failure. The correct response is to refine doctrine, not to improvise around the gap indefinitely.

## Promotion and demotion criteria for recurring patterns

### Promote a pattern when:
- it recurs across multiple donor families;
- it creates frequent converter drift or inconsistency;
- it meaningfully affects many conversions rather than a narrow subset;
- it exposes a stable recurring structural need rather than a donor quirk.

### Keep a pattern at translation level when:
- it is rare or donor-local;
- it can be handled reliably through existing routing templates;
- it does not justify new doctrine ownership.

### Demote or retire a pattern when:
- later doctrine absorbs it cleanly elsewhere;
- recurrence proves lower than expected;
- it was initially overfit to donor noise.

## Stress-test construct suite

A16 should maintain a small regression set of canonical edge-case shapes. These are not full conversions; they are classification tests.

Recommended suite:
- living weapon;
- eidolon-like partner;
- investigation construct that fuses search and study;
- token that is both reward and access right;
- mobile city;
- corpse-questioning effect;
- institutionally assigned drone;
- world profile that fuses law, governance, port access, and base access;
- donor “skill” that is actually permission + active effect;
- site that is simultaneously neutral ground, embassy cluster, market, and transport hub.

Future doctrine and conversion prompts should be able to classify these consistently.

## Anti-hallucination rules

1. Do not assume donor labels indicate doctrinal ownership.
2. Do not flatten repeated ambiguities into the nearest familiar Astra term without pattern checking.
3. Do not solve under-specification with decorative lore.
4. Do not treat repeated conversion pain as a one-off oddity if a recurring pattern is clearly emerging.
5. Do not let examples outrank doctrine.
6. Do not treat “works in one donor” as sufficient justification for Astra-wide law.
7. Do not collapse cross-file constructs into one owner merely because the donor bundled them.

## Batch A / Batch B / future Batch C handoff map

### Batch A primary owners commonly implicated
- A02 player chassis doctrine
- A03 resolution framework
- A05 competency and skill translation architecture
- A06 access tags, permissions, and proficiency gates
- A07 ability object model
- A07b resource, cost, recharge, and backlash architecture
- A08 status, condition, and effect architecture
- A09/A09b damage taxonomy and compound interactions
- A10 progression axes
- A12 path, archetype, and profession framework
- A13 character creation procedure
- A14 starting loadout and kit framework
- A15 conversion invariants

### Batch B primary owners commonly implicated
- B01 scene/conflict/action/encounter procedure
- B02 health/injury/healing/death/recovery
- B03 item and gear object model
- B04 wealth/currency/requisition/trade/value
- B05 crafting/salvage/repair/modification/installation
- B06 exploration/travel/navigation/time/distance
- B07 environmental hazards/weather/regions/afflictions
- B08 stealth/detection/visibility/sensory procedure
- B09 investigation/research/discovery/clues/information
- B10 social conflict/influence/reputation/negotiation
- B11 downtime/rest/training/projects/services
- B12 factions/institutions/clearance/service access
- B13 companions/retinues/summons/drones/auxiliaries
- B14 mounts/vehicles/mechs/ships/platform operations
- B15 settlements/bases/capitals/infrastructure operations
- B16 loot/rewards/salvage/post-encounter inflows

### Future Batch C implication
If a pattern repeatedly points toward creatures/NPCs, traps/trials, scenario schema, or generator schema, route forward to Batch C once those files are created instead of overloading A16.

## Classification examples, not full conversions

### Example 1: donor “investigation” skill
Pattern axes suggest: procedure, not one unified capability; truth-status-sensitive; likely split across search/study/research.
Primary owners: B08 and B09.
Resolution: split, medium-confidence.
Forbidden collapse: do not convert as one monolithic Astra skill.

### Example 2: donor token that grants trial access and can be traded
Pattern axes suggest: permission/right plus value-bearing object.
Primary owner: B12 or B06 depending on dominant function.
Secondary dependency: B04 for value/exchange semantics.
Resolution: holder-linked overlay or primary-owner + secondary dependency.
Forbidden collapse: do not treat as pure currency or pure treasure.

### Example 3: mobile city on a giant creature
Pattern axes suggest: site shell, institution overlay, platform/frame dependency.
Primary owner: B15 if habitation/governance/infrastructure dominate.
Secondary dependency: B14 for movement/deployment frame logic.
Resolution: hybrid, dominant-function routed.
Forbidden collapse: do not treat as only vehicle or only town.

### Example 4: corpse-questioning effect
Pattern axes suggest: information-access method with uncertain truth-status.
Primary owner: B16 for post-pressure information-bearing output state.
Secondary dependency: B09 for interpretation, verification, and truth-status.
Resolution: source-state + extraction method + output family.
Forbidden collapse: do not treat as automatic solved truth.

### Example 5: eidolon-like shared partner
Pattern axes suggest: linked secondary actor with shared-bandwidth control topology.
Primary owner: B13.
Secondary dependencies: B01, A07, B03 as needed.
Resolution: shared-bandwidth pair.
Forbidden collapse: do not treat as normal summon or normal companion if bandwidth is structurally shared.

## Final doctrine statement

A16 exists to keep Astra coherent at scale. It teaches the conversion layer how to recognize recurring structural patterns, separate donor labels from donor jobs, route hybrids lawfully, use explicit uncertainty states, and escalate when the doctrine stack is genuinely missing something.

It is not a replacement for the stack. It is the file that keeps the stack usable across a mixed donor ecosystem.
