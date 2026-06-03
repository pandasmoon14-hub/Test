

<!-- FILE: D07-README_manifest.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07 README Manifest

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Purpose

D07 establishes Astra's harm, recovery, corruption, mutation, identity-harm, Power Economy backlash, and terminal consequence doctrine. It lets Astra handle mundane injury, poison, disease, exhaustion, body transformation, corruption, conceptual-resource exposure, mental strain, identity erosion, route scars, Principle dissonance, failed breakthroughs, carrier backlash, dual-state transformations, source-local sanity systems, source-local death systems, mutation tables, cyberware rejection, biotech infection, undead conversion, eldritch marks, companion/bond harm, platform feedback, and lethal consequences without reducing everything to hit points.


## File order

1. `D07-00_layered_harm_architecture_overview.md`
2. `D07-01_damage_injury_conditions_and_severity.md`
3. `D07-02_corruption_contamination_and_instability.md`
4. `D07-03_mutation_transformation_and_body_change.md`
5. `D07-04_identity_mental_and_principle_harm.md`
6. `D07-05_conceptual_resource_exposure_and_integration_harm.md`
7. `D07-06_carrier_backlash_and_power_strain_handoff.md`
8. `D07-07_recovery_treatment_stabilization_and_adaptation.md`
9. `D07-08_lethality_crippling_and_failure_consequences.md`
10. `D07-09_runtime_records_ui_and_owner_handoffs.md`
11. `D07-10_integration_checklists_and_ddr_register.md`
12. `D07_pack_manifest.json`


## Dependency posture

D07 depends on D03, D04, D05, and D06, but must not rewrite them. It feeds D08, D09, and D10. It deliberately does not finalize actor-state, species-state, companion mechanics, item/platform mechanics, faction/world-state consequences, or live-play GM behavior.

| If the issue concerns... | Owner |
| --- | --- |
| Power Economy pools, carriers, reservoirs, costs, overdraw, Expression mechanics | D03 |
| Proof, advancement, tiers, breakthroughs, Awakening, capstone | D04 |
| Skills, diagnosis, medicine, research, training, treatment competence | D05 |
| Routes, Paths, Principles, Route Features, Techniques, route severance/mutation | D06 |
| Actor-state, kinform, companions, spirits, AI, summons, bonds, personhood | D08 |
| Items, relics, tools, implants, prosthetics, platforms, ships, mechs | D09 |
| Factions, law, reputation, territory, settlement, environment, world-state | D10 |
| Donor-specific sanity, death, mutation, corruption, resurrection, curse systems | Source-local / review |


## Non-negotiable controls

1. Harm is broader than damage.
2. Damage is one input into harm, not the whole system.
3. Pools remain useful; D07 does not delete them.
4. D07 owns harm states and recovery consequences, not every harm source.
5. Corruption is distortive contamination, not moral evil by default.
6. Mutation is governed transformation-state, not random boon table.
7. Identity harm must preserve agency except under strict terminal or possession-equivalent gates.
8. Power Economy failure remains D03-owned; D07 records consequences.
9. Recovery is not synonymous with restoration.
10. Terminal outcomes are possible but gated.
11. Source-local sanity, death, resurrection, mutation, corruption, and curse systems remain bounded.
12. Durable record burden must be controlled through ephemeral, session-relevant, and durable tiers.


## Post-pack expectation

After generation, run a short D03/D04/D06 patch-note check. Do not rewrite D03/D04/D06 unless contradictions are found.



<!-- FILE: D07-00_layered_harm_architecture_overview.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-00 Layered Harm Architecture Overview

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D07 uses Layered Harm Architecture. Harm is any adverse state change to an actor, body, mind, identity, route, carrier, bond, anchor, capability substrate, or source-local state. Damage is only one input into harm. A spear wound, carrier overdraw, undead corruption, source-local madness spiral, conceptual allergy, broken oath, platform feedback burn, failed breakthrough, and eldritch mark cannot all be treated as identical hit point loss. They must share a common grammar without being flattened into sameness.


## Harm families

| Family | Function |
| --- | --- |
| Physical / Bodily | Wounds, organs, limbs, senses, pain, structure, nonhuman anatomy. |
| Fatigue / Depletion | Exhaustion, overexertion, hunger, thirst, sleep loss, stamina collapse. |
| Cognitive / Mental Strain | Confusion, overload, panic, disorientation, forbidden comprehension. |
| Identity / Self-Coherence | Memory continuity, will, selfhood, personhood boundary, values. |
| Corruption / Contamination | Distortive influence, taint, impurity, hostile overwrite, conceptual allergy. |
| Mutation / Transformation | Form change, body alteration, alternate state, dual-state pressure. |
| Carrier / Power-Strain | Carrier tearing, reservoir souring, overdraw harm, confluence sickness. |
| Route / Principle | Route scars, Principle dissonance, route contradiction, route shattering pressure. |
| Bond / Actor-Relation | Companion, pact, spirit, AI, swarm, summon, dual-cultivation link harm. |
| Anchor / Platform Feedback | Relic, implant, vehicle, mech, tool, ship, weapon, or platform backlash. |
| Social / Obligation | Oath strain, exile harm, taboo mark, debt pressure when actor harm results. |
| Environmental / Hazard | Heat, cold, void, pressure, disease ecology, cursed terrain, hostile domain. |
| Concept-Bearing Resource Exposure | Dao-stone-like insight pressure, conceptual resource corrosion, resource allergy. |
| Source-local | Donor-specific sanity, death, corruption, mutation, curse, doom, or disease systems. |
| Mixed | Any event combining multiple families. |


## Severity and persistence

Severity bands: Trace, Minor, Moderate, Severe, Critical, Catastrophic, Lethal/Terminal. Persistence bands: Instant, Scene, Session, Short Recovery, Long Recovery, Persistent, Degenerative, Transformative, Permanent, Source-local. Severity is family-relative. A Critical social/oath harm is not a Critical sword wound, but both threaten major state change.


## Pool preservation

D07 does not replace pool-based play. Astra may still use Vitality, Integrity, stamina, focus, morale, stress, shield/guard, wound thresholds, fatigue reserves, Power Economy pools, carrier capacity, reservoir depth, overdraw tolerance, platform integrity, companion bond stability, and source-local health or sanity pools. Standard sequence: apply pool/resource pressure; check threshold, bypass, critical consequence, overdraw, failed mitigation, or source-local trigger; if no lasting consequence occurs, leave it as pool loss; if meaningful consequence occurs, create a D07 harm event.


## Harm outputs

A harm event may output condition, injury, scar, mutation, corruption state, instability, resource or carrier damage, route damage, bond damage, anchor feedback, world consequence, proof candidate, recovery project, or terminal state. A single event may output several states, but owner handoffs must stay explicit.


## Examples

A town guard takes a spear wound. Physical damage reduces Vitality. If it crosses a wound threshold, D07 records Bleeding. If untreated, it becomes Leg Injury. If it heals badly or becomes proof-bearing, it becomes Gate-Hinge Scar.

A Glass-Tomb Archivist overreads a dead record. D07 records Cognitive Strain and Identity Harm. D05 owns research method, D06 owns Memory Principle consequences, and D09 may own the archive lens.

A living/undead dual-state survivor overuses undead-state power. D03 handles form-specific Power Economy leakage; D07 records Hunger Bleed and Partition-Leaking; D06 owns route boundary; D08 owns actor-state.



<!-- FILE: D07-01_damage_injury_conditions_and_severity.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-01 Damage, Injury, Conditions, Severity, and Persistence

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D07 distinguishes Damage, Condition, Injury, and Scar. Damage is immediate harmful pressure. A Condition is an active named state. An Injury is persistent harm that affects function beyond the immediate event. A Scar is lasting integrated harm that becomes part of body, identity, route, carrier, bond, anchor, history, or source-local state.


## Damage

Damage may be physical, energetic, cognitive, conceptual, corruptive, biological, technological, environmental, social/obligation-based, spiritual, source-local, or mixed. Damage may reduce a pool, trigger a condition, create an injury, expose corruption, destabilize a carrier, or do nothing durable if absorbed. Damage alone is not necessarily durable D07 state.


## Conditions

A Condition is a named active state affecting function. Examples include Bleeding, Burned, Fractured, Winded, Exhausted, Disoriented, Memory Flooded, Self-Dissonant, Tainted, Spore Bloom, Overdrawn, Oath-Strained, Sync-Fractured, Feedback-Burned, Debt-Crushed, Pressure-Sick, False Sky Sick. A condition should define family, severity, persistence, impairment, recovery, escalation, and handoffs if durable.


## Injuries

An Injury is harm that persists beyond the immediate condition stage. Injuries can affect body, mind, identity, carrier, route, bond, anchor, social position, or source-local state. Examples include Pierced Thigh, Torn Carrier Channel, Foreign Memory Intrusion, Broken Speech Injury, Neural Feedback Burn, Spore Memory Fracture, and Star-Map Disorientation.


## Scars

A Scar is lasting integrated harm. Scars may be negative, mixed, adaptive, proof-bearing, route-shaping, mutation-seeding, source-local, or externalized. Scars are not automatically benefits. Any feature or advancement implication requires D04/D06 validation.


## Escalation and transition

A condition may become an injury when severity is moderate or higher and untreated, persistence exceeds scene/session, the condition recurs, a core structure is affected, route/carrier/bond/identity state changes, failed recovery worsens it, breakthrough failure creates lasting harm, or source-local rules require tracking. An injury may become a scar when it heals incompletely, the actor adapts, it becomes proof-bearing, route identity absorbs it, mutation stabilizes around it, or externalization leaves residue.


## Functional stacking

Multiple harms interact by functional overlap, not simple additive stacking. If two conditions impair the same function, one may dominate, combine into higher severity, become a complication trigger, remain latent, form mixed-family injury, or require owner escalation.


## Pool thresholds

Pool loss alone should not create durable D07 records unless it crosses a consequence threshold. Vitality loss alone may remain pool-state. Vitality loss past wound threshold may create injury. Power pool depletion remains D03. Overdraw may create Overdrawn or Carrier-Torn. Platform integrity remains D09 unless actor harm occurs.


## Record shape

```yaml
condition_or_injury_record:
  record_id: string
  actor_ref: string
  record_type: condition | injury | scar
  harm_family: physical | fatigue | cognitive | identity | corruption | mutation | carrier | route | bond | anchor | social_obligation | environmental | conceptual_resource | source_local | mixed
  severity: trace | minor | moderate | severe | critical | catastrophic | lethal_terminal
  persistence: instant | scene | session | short_recovery | long_recovery | persistent | degenerative | transformative | permanent | source_local
  impaired_functions: []
  worsens_when: []
  stabilizes_when: []
  recovery_options: []
  escalation_outputs: []
  owner_handoffs: {}
  validation_state: authorized | pending_owner_file | dangerous | source_local | blocked | escalated
```



<!-- FILE: D07-02_corruption_contamination_and_instability.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-02 Corruption, Contamination, and Instability

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

Corruption is distortive contamination. It is not moral evil by default. Corruption means a harmful or incompatible influence distorts normal structure, function, identity, route, carrier, bond, anchor, Principle, environment, or source-local state. Contamination is exposure; corruption is active distortion; instability is unreliability; mutation is transformation.


## Targets and vectors

Corruption may target body, mind, identity, carrier, route, Principle, bond, anchor, environment, social/oath state, or source-local systems. Vectors include contact, ingestion, inhalation, Expression backlash, route contradiction, anchor leakage, bond feedback, environmental saturation, social/oath exposure, research exposure, and source-local mechanisms.


## Severity, persistence, and outputs

Trace corruption may be residue or warning. Minor corruption may be mild compulsion. Moderate corruption requires care. Severe corruption distorts route, carrier, body, or identity. Critical corruption threatens collapse. Catastrophic or terminal corruption may overwrite function or end playability. Outputs include condition, injury, scar, mutation, compulsion, blindness, route drift, corrupted feature, carrier damage, bond strain, anchor dependency, social mark, proof candidate, or terminal collapse.


## Recovery paths

Corruption may be resisted, stabilized, suppressed, purged, adapted to, externalized, sealed, reconciled, severed, transformed, or left to degenerate. Suppression is not purge. Adaptation is not free benefit. Externalization creates dependency. Severance creates loss. Transformation may create mutation, route scar, alternate form, or source-local state.


## Corruption Conversion

Corruption Conversion is a rare D07 outcome where corruption is converted into a bounded secondary state, alternate form, route scar, source-local actor-state change, or separate Power Economy interface through an opposing, balancing, harmonizing, or personally claimed force. It requires meaningful exposure, survival or stabilization, opposing/balancing basis, compatibility check, cost/constraint, owner-file validation, durable record, and maintenance/failure consequences. It never grants free immunity, unrestricted power, automatic second route, or automatic second Power Economy.


## Balanced and personalized examples

A world is corrupted by undead Principles. An inhabitant is exposed and uses a rare opposing local resource. D07 may record balanced living/undead dual-state. D03 owns form-linked Power Economies; D06 owns route boundaries; D08 owns actor-state; D09 owns the resource if material; D10 owns world corruption and social reaction; D04 validates proof.

A newly ascended actor is marked by an eldritch being and later severs the claim. D07 records foreign-will corruption, severance harm, personalized scar, and residual risk. D06 handles alien Principle pressure, D03 handles power interface, D10 handles entity attention, and D04 validates proof.


## Conceptual-resource corruption

Concept-bearing resources can corrupt through over-concentrated insight, incompatible Principle imprint, hostile origin, ancient war residue, impure refinement, forced ingestion, inefficient integration, overreliance, and synthesis mismatch. D07 outputs may include Physical Corrosion, Psyche Warping, Conceptual Allergy, Hollow Comprehension, Carrier Inflammation, Route Brittleness, Principle Blindness, Identity Narrowing, Shattering Risk, or Mutation Bloom.


## Anti-drift rules

Do not moralize corruption by default. Do not let corruption grant power automatically. Do not treat all instability as corruption. Do not let Corruption Conversion become dual-build stacking. Do not generalize donor corruption clocks without source-local review.



<!-- FILE: D07-03_mutation_transformation_and_body_change.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-03 Mutation, Transformation, and Body Change

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

Mutation is a governed transformation-state outcome. It is not a random boon table and not pure punishment. Mutation, transformation, alternate form, dual-state condition, and Corruption Conversion are distinct. A mutation may be harmful, beneficial, mixed, adaptive, unstable, controlled, uncontrolled, reversible, permanent, source-local, externalized, or terminal. It becomes a Route feature, Power Economy change, kinform change, proof event, or source-local capability only when relevant owner files validate it.


## Definitions

Mutation is a change to actor structure, function, physiology, body logic, identity interface, carrier behavior, route expression, or source-local form state. Transformation is broader form-state change. Alternate Form is a distinct state the actor may enter, suffer, maintain, suppress, or transform into. Dual-State Condition is a durable state where an actor has two or more bounded form or power postures.


## Sources and targets

Mutation sources include corruption, conceptual resource, breakthrough failure, power backlash, external anchor, implant/biotech, companion/bond, environmental exposure, route contradiction, and source-local rules. Mutation targets include surface body, functional body, defensive body, perceptual body, carrier body, route body, identity body, kinform/species-state, anchor-integrated body, and source-local form.


## Quality, control, and stability

Quality bands include harmful, beneficial, mixed, latent, unstable, adaptive, scarred, corrupted, externalized, source-local, and terminal. Control states include uncontrolled, triggered, suppressed, voluntary, partial, external-controlled, negotiated, stable, degenerating, and severed. Stability states include stable, volatile, degenerative, contained, balanced, partitioned, leaking, collapsing, and source-local.


## Dual-state doctrine

Dual-state actors are allowed but rare and gated. A dual-state condition requires valid transformation source, stabilizing or partitioning basis, defined forms, triggers, control limits, separate permissions/vulnerabilities, owner handoffs, recovery/severance/degeneration options, and durable records. A dual-state actor does not receive a free second build.


## Mutation and owner files

Mutation does not automatically create a Route. D06 must validate route outputs. D03 must validate carrier, reservoir, cost, or form-specific economy changes. D08 must validate kinform/species/actor-state changes. D09 validates implants, relics, prosthetics, tools, and platforms. D10 validates social/world consequences. D04 validates proof.


## Recovery outcomes

Mutation recovery may revert, stabilize, suppress, control, adapt, integrate, partition, externalize, purge, reconcile, sever, transform, degenerate, or terminalize.


## Examples

A body-tempering failure leaves crystal nerves. D04 owns breakthrough failure; D07 records unstable mutation and pain; D08 validates physiology; D06 may later validate route scar. A cybernetic graft rejection causes triggered spasms. D09 owns implant, D08 owns actor-state implications, D07 records mutation/injury. A source-local lycanthropy system remains bounded.



<!-- FILE: D07-04_identity_mental_and_principle_harm.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-04 Identity, Mental, and Principle Harm

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D07 uses Layered Cognitive, Identity, and Principle Harm. Astra does not adopt a universal sanity meter by default, and it does not ignore mental or identity harm. Cognitive harm affects processing. Memory harm affects remembered experience. Identity harm affects self-coherence. Principle harm affects route-aligned meaning. Compulsion creates pressure before control.


## Subfamilies

Subfamilies include Cognitive Strain, Memory Harm, Fear/Panic Pressure, Identity Erosion, Compulsion, Conceptual Blindness, Principle Dissonance, Route Contradiction, Foreign Will Pressure, and Source-local Madness/Sanity.


## Agency safeguard

Most mental, identity, and Principle harm should produce pressure, cost, warning, difficulty, blocked feature, dissonance, risk, recovery requirement, altered information, temptation, partial access loss, or need for resistance/grounding. It should not casually dictate player action. Direct control, forced transformation, possession-equivalent behavior, or non-playable takeover requires severe or worse state, clear source, failed resistance or mitigation, owner-file validation, warning where appropriate, recovery/severance path, and source-local boundary if donor-specific.


## Principle and route harm

Principle Dissonance Harm occurs when actions, exposure, corruption, resources, route choices, or contradictions strain Principle/Concept alignment. Route Contradiction Harm occurs when Route permissions, limits, proof history, obligations, features, or identity are meaningfully violated or pulled apart. D06 owns the structure; D07 owns strain, compulsion, blindness, identity erosion, mental fracture, corruption, scar, or collapse.


## Dual-state identity harm

Dual-state actors may suffer state bleed, partition stress, undead hunger leaking into living form, living empathy weakening undead-form control, memory partition failure, form-trigger panic, identity fatigue, cross-form Power Economy contamination, and route feature leakage.


## Foreign will states

Foreign influence may be influence, pressure, compulsion, contest, override, possession-equivalent, integration, or severance. D07 records harm. D08/source-local owns full possession/personhood mechanics.


## Source-local sanity

A donor sanity system may be retained source-locally while outputs map into Cognitive Strain, Identity Harm, Corruption, Route/Principle Harm, Source-local Madness Track, Fear/Panic Condition, Forbidden Knowledge Injury, D10 environmental pressure, or D04 proof. No donor sanity model becomes Astra default.


## Examples

A Glass-Tomb Archivist overreads a dead record and suffers Memory Flood. A Thorn-Court Mediator breaks a sworn bargain to save children and suffers Oath-Strained identity dissonance. A Mech-Synced Ash Cavalier experiences AI command bleed. A balanced living/undead survivor overuses undead form and develops Hunger Bleed.



<!-- FILE: D07-05_conceptual_resource_exposure_and_integration_harm.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-05 Conceptual Resource Exposure and Integration Harm

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

Concept-bearing resources are not automatically safe advancement fuel. When an actor consumes, refines, studies, wields, grafts, integrates, synthesizes, or externalizes a concept-bearing resource, D07 classifies possible harm from corrosion, cognitive strain, identity erosion, corruption, conceptual allergy, carrier damage, route instability, mutation, overreliance, breakthrough failure, and source-local backlash.


## Resource functions by owner

| Function | Owner |
| --- | --- |
| Energy, pool, cost, carrier, reservoir, integration burden | D03 |
| Breakthrough catalyst, advancement proof, tier gate | D04 |
| Study, comprehension training, research use | D05 |
| Principle/Concept alignment, resonance, dissonance, authority | D06 |
| Corrosion, psyche warping, conceptual allergy, shattering, mutation, corruption | D07 |
| Tool, relic, crafted spiritual object, path weapon | D09 |
| Scarcity, wars, trade, empires, factions, market control | D10 |
| Donor-specific System monitoring or metaphysics | Source-local / escalation |


## Harm vectors

Physical corrosion may occur during ingestion, refinement, grafting, contact, or wielding. Psyche warping may force cognition toward embedded Principle. Conceptual allergy occurs when resource imprint conflicts with Route, Principle, carrier, form, kinform, or metaphysics. Overreliance may create Hollow Comprehension and brittle foundation. Inefficient integration may create dangerous residue. Conceptual synthesis may create overload, contradiction scars, identity split, or corrupted Technique candidates. Breakthrough catalyst misuse may be crippling or lethal.


## Conflict and scarcity

Possessing rare resources can cause theft, war, espionage, faction pressure, and empire-scale conflict. D10 owns scarcity and conflict. D07 owns actor harm from those consequences.


## Source-local System gatekeeping

If a donor source uses an omnipresent System that monitors or grants resources, it remains source-local unless explicitly adopted. D07 may retain source-local harm if misuse is punished, but this does not become Astra law.


## Potential states

Potential D07 states include Physical Corrosion, Resource-Allergic, Carrier Inflamed, Reservoir-Soured, Conceptual Allergy, Principle Blindness, Hollow Comprehension, Identity Narrowing, Route Brittleness, Corrupted Insight, Mutation Bloom, Shattering Risk, and Source-local Resource Doom.


## Recovery

Recovery may purge incompatible residue, stabilize insight, reinterpret Principle, seal unused concept residue, adapt to narrowed perception, externalize insight into a tool/journal/relic/teacher record, convert corruption into balanced state, accept route scar, or block advancement until foundation is repaired.


## Examples

A Glass-Tomb Archivist consumes a Memory shard and gains acceleration plus identity bleed. A Mech-Synced Ash Cavalier installs an ash-war core and gains power plus aggression drift. A Hollow-Depth Listener uses a Burial-aligned pressure stone and suffers conceptual allergy against Warning. A Siege-Kettle Quartermaster uses famine-salt and risks compulsive ration control.



<!-- FILE: D07-06_carrier_backlash_and_power_strain_handoff.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-06 Carrier Backlash and Power-Strain Handoff

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D03 decides how power fails. D07 decides what harm the failure leaves behind. D03 owns Power Economy structure, pools, carriers, reservoirs, costs, recharge, overdraw, confluence, Expression mechanics, re-authoring, resource compatibility, and pool math. D07 owns resulting conditions, injuries, scars, corruption, mutation, identity harm, route harm, recovery, and terminal consequences.


## Pool preservation

D07 does not replace pools. Power pool loss, carrier burden, reservoir depletion, stamina depletion, platform integrity loss, or source-local mana loss remains with the relevant system unless threshold consequence emerges.


## Power-strain sources

Sources include overdraw, cost mispayment, carrier overload, reservoir souring, Expression backlash, re-authoring failure, confluence sickness, conceptual-resource incompatibility, form-specific contamination, anchor-mediated backlash, and source-local pool failure.


## Carrier harm states

Carrier-facing states include Overdrawn, Carrier-Torn, Reservoir-Soured, Slot-Burned, Channel-Inflamed, Confluence-Sick, Recoil-Marked, Resource-Allergic, Carrier-Rotted, Partition-Leaking, and Carrier-Collapsing. D03 defines mechanics behind carrier, reservoir, slot, channel, and partition. D07 names and manages harm states.


## Dual-state carrier partition

Rare dual-state actors may have form-linked economy partitions. D03 owns partition rules. D07 records harm from leakage, such as Cross-Form Overdraw, Living Reservoir Souring, Undead Hunger Bleed, Carrier Identity Split, Form-Trigger Collapse, or Dual-State Confluence Sickness.


## Expression backlash and anchors

D03 identifies Expression failure. D07 classifies outputs such as fatigue, carrier injury, physical injury, cognitive strain, corruption, mutation, route harm, anchor feedback, or terminal collapse. If backlash is routed through a tool, relic, implant, platform, or companion, D09/D08 validate the anchor or actor relation.


## Recovery and proof

Recovery may include rest, grounding, recalibration, treatment, purge, seal, reroute, adapt, re-author, externalize, sever, transform, or degenerate. Power-strain harm may become proof-bearing only if D04 validates it.


## Examples

A novice overdraws an Expression and becomes Overdrawn, then Carrier-Inflamed if repeated. A Mercy-route healer uses Slaughter crystal and develops Conceptual Allergy. A living/undead actor uses undead power in living form and develops Partition-Leaking. A Mech-Synced Ash Cavalier overdrives a damaged platform and receives Neural Burn and Feedback Scar.



<!-- FILE: D07-07_recovery_treatment_stabilization_and_adaptation.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-07 Recovery, Treatment, Stabilization, and Adaptation

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

Recovery is not synonymous with restoration. Recovery is the process by which harm is removed, stabilized, suppressed, adapted to, transformed, externalized, reconciled, severed, contained, recalibrated, integrated, or allowed to degenerate.


## Recovery outcomes

Outcomes include Heal, Stabilize, Suppress, Adapt, Scar, Transform, Externalize, Purge, Reconcile, Sever, Contain, Recalibrate, Integrate, Degenerate, and Terminalize. These outcomes may combine.


## Sources and ownership

Recovery may come from rest/care, medical treatment, ritual treatment, technical repair, Power Economy recalibration, research, training, route reinterpretation, bond care, environmental care, anchor externalization, or source-local treatment. D05 owns treatment competence and recovery projects. D07 owns harm outcome.


## Key distinctions

Stabilization prevents worsening; healing removes or repairs harm. Suppression controls harm while it remains; purge removes harmful influence. Restoration returns toward prior state; adaptation teaches function with changed state. Scars can be successful recovery outcomes, not just failed healing.


## Externalization

Externalization moves harm or instability into an anchor: relic, tool, weapon, implant, prosthetic, oath ledger, memory journal, shrine, platform, ship, companion, spirit, AI partition, territory, sealed room, ritual mark, or source-local object. Externalization creates dependency and requires owner handoffs.


## Reconciliation, severance, and containment

Reconciliation resolves contradiction. Severance cuts away harmful route, bond, mark, carrier branch, anchor, entity, mutation, or source-local state and is not casual respec. Containment keeps harm bounded through seals, medicines, rituals, anchors, territory restrictions, route practices, companion monitoring, Power Economy caps, form triggers, social rules, or source-local clocks.


## Recovery Projects

Severe, persistent, degenerative, transformative, source-local, carrier-facing, route-facing, identity-facing, corruptive, mutation-facing, dual-state, externalized, or specialist-dependent harm may require a Recovery Project with goal, target harm, access, competencies, resources, risk, failure output, success output, and owner handoffs.


## Examples

A carrier-torn novice requires D03 recalibration and D05 training. A living/undead survivor maintains balance through Dawn-Salt, route reconciliation, and carrier partition care. A Glass-Tomb Archivist externalizes Foreign Memory Intrusion into a funeral index. A Gate-Hinge Defender stabilizes a wound and later adapts to a proof-bearing scar.



<!-- FILE: D07-08_lethality_crippling_and_failure_consequences.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-08 Lethality, Crippling, and Failure Consequences

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D07 uses a Terminal Harm Gate Model. Death, crippling harm, route death, carrier collapse, identity collapse, terminal corruption, terminal mutation, bond destruction, anchor-fatal feedback, and source-local terminal states are allowed, but terminal outcomes must be gated, validated, recorded, and consequence-bearing. Death is possible; it is not the only catastrophic outcome.


## Terminal categories

Categories include Body Death, Crippling Injury, Carrier Collapse, Route Death/Severance, Identity Collapse, Terminal Corruption, Terminal Mutation, Bond Destruction, Anchor-Fatal Feedback, Source-local Terminal State, and World-state Terminal Consequence.


## Gate requirements

Terminal outcomes require critical/catastrophic/terminal severity, valid harm source, failed mitigation or overwhelming force, owner-file validation, warning where appropriate, durable terminal record, and recovery/continuation options if campaign permits.


## Crippling and near-death

Crippling harm changes capability durably without necessarily ending the actor. Near-death preserves lethal risk while allowing last-chance mitigation or scarred survival. Near-death may include dying condition, coma, suspended state, body/soul separation, route flicker, carrier shutdown, undead-state trigger, emergency externalization, companion intervention, relic sacrifice, source-local death save, or faction/world intervention.


## Last-chance mitigation

Mitigation may reduce death to crippling injury, crippling injury to scar, route death to route scar, carrier collapse to carrier injury, identity collapse to partitioned scar, corruption terminalization to contained dual-state, or body death to source-local undead state if validated. Mitigation requires cost, risk, resource, proof, sacrifice, or prior preparation.


## Breakthrough failure

D04 owns breakthrough gates. D07 owns harm consequences. Breakthrough failure may cause fatigue, injury, carrier damage, route scar, Principle dissonance, mutation, corruption, identity fracture, dual-state instability, crippling injury, terminal collapse, or death. Lethal breakthrough failure should be telegraphed by risk tier, dangerous materials, unstable proof, unsafe route pressure, hostile environment, corruption, or willful overreach.


## Source-local death systems

Donor death saves, resurrection, soul loss, sanity collapse, doom clocks, reincarnation, clone backups, respawn, injury tables, and corruption terminal states remain source-local unless normalized. D07 may map outputs but must not adopt a universal donor death model.


## Examples

A failed body-tempering breakthrough causes crystal nerve crippling rather than death. A Truth route dies through repeated contradiction while the actor lives. A caster overdraws to stop disaster and suffers carrier collapse. A mech pilot survives because the AI sacrifices itself, leaving Sync-Grief Scar.



<!-- FILE: D07-09_runtime_records_ui_and_owner_handoffs.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-09 Runtime Records, UI, and Owner Handoffs

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Core doctrine

D07 uses tiered harm records: ephemeral, session-relevant, and durable. D07 record families are doctrine shapes, not final database schemas. The goal is to preserve consequence, recovery, risk, source-local boundaries, and owner-file validation without turning play into raw condition bookkeeping.


## Record tiers

Ephemeral harm lasts only during a moment or immediate scene and does not require durable storage unless it escalates. Session-relevant harm matters for the current scene or play unit but may clear. Durable harm changes the actor record or creates future obligations: injury, scar, persistent condition, degenerative harm, transformative harm, corruption, mutation, dual-state, carrier injury, route harm, identity harm, bond/anchor harm, recovery project, terminal harm, source-local boundary, proof-relevant harm, or owner-file handoff.


## Record families

Record families include Harm Event, Condition, Injury, Scar, Corruption, Mutation/Transformation, Identity/Mental/Principle Harm, Power-Strain Harm, Recovery, Terminal Harm, and Source-local Harm Boundary.


## Durable thresholds

Durable record required when harm persists beyond scene/session; requires recovery/treatment/project/maintenance; affects route/principle/technique/feature; affects Power Economy; causes corruption/mutation/dual-state/transformation; affects identity/memory/agency; affects companion/bond/anchor; creates faction/legal/social/world consequence; creates proof pressure; reaches severe or worse; creates source-local state; or requires owner validation.


## Visibility states and fairness

Visibility states include Visible, Diagnosed, Discovered, Obscured, Hidden, Dangerous, Source-local, Stabilized, Dormant, and Retired. Hidden or obscured harm must surface through symptoms, assessment, diagnosis, failed action, recovery attempt, teacher feedback, route response, carrier behavior, companion behavior, anchor behavior, environmental response, or source-local trigger. It must not be arbitrary surprise punishment.


## UI grouping

Future UI should group harm by Current Conditions, Injuries, Scars, Corruption/Instability, Mutations/Forms, Mind/Identity, Carrier/Power Strain, Recovery Projects, Dangerous States, Source-local Harm, and History/Retired. Player-facing display may simplify severity and persistence.


## Consolidation and retirement

A condition may retire when it heals, becomes injury, becomes scar, is purged, externalized, source-local resolved, or superseded. An injury may retire when healed, transformed into scar, folded into mutation, stabilized as permanent limitation, externalized, source-local resolved, or terminalized. Scars retire only when canonically removed, severed, overwritten, externalized, boundary closes, or archived inactive.


## Pool-state interaction

D07 records should not duplicate pool state unless harm persists beyond pool loss. Vitality loss alone, stamina depletion alone, Power pool depletion alone, platform integrity loss alone, or source-local stress pool loss alone does not create durable D07 harm unless condition/injury/scar or owner impact results.


## Shared record header

```yaml
d07_harm_record_header:
  record_id: string
  actor_or_target_ref: string
  record_family: harm_event | condition | injury | scar | corruption | mutation_transformation | identity_mental_principle_harm | power_strain | recovery | terminal_harm | source_local_boundary
  record_tier: ephemeral | session_relevant | durable
  visibility_state: visible | diagnosed | discovered | obscured | hidden | dangerous | source_local | stabilized | dormant | retired
  severity: trace | minor | moderate | severe | critical | catastrophic | lethal_terminal | not_applicable
  persistence: instant | scene | session | short_recovery | long_recovery | persistent | degenerative | transformative | permanent | source_local | not_applicable
  source_ref: string
  source_owner: D02 | D03 | D04 | D05 | D06 | D07 | D08 | D09 | D10 | source_local | unknown
  owner_handoff_state: {}
  active_effect_summary: string
  recovery_or_resolution_summary: string
  history_retention_required: boolean
  validation_state: authorized | pending_owner_file | dangerous | source_local | blocked | escalated | retired
```



<!-- FILE: D07-10_integration_checklists_and_ddr_register.md -->

---
project: Astra Ascension
pack: D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine
version: v0.1
status: doctrine draft generated from accepted D07 design decisions
phase: Phase 1 — Doctrine and framework build
scope: Batch D native Astra design doctrine
---

# D07-10 Integration Checklists and DDR Register

## Status

This file is part of the D07 doctrine pack. It is doctrine-facing, conversion-facing, and future-runtime-facing. It is not final implementation code, not a finished Core Sourcebook chapter, and not live-play GM behavior.

## Global D07 boundary

D07 defines harm-state grammar for Astra Ascension. It does not replace health, vitality, stamina, stress, Power Economy pools, carrier capacity, platform integrity, companion stability, or source-local pool systems. Pools remain valid when useful for pacing, tactical pressure, spend, depletion, buffer, or resistance. D07 begins when pressure produces a meaningful harm state: condition, injury, scar, corruption, mutation, recovery requirement, terminal state, source-local consequence, proof relevance, or owner-file impact.

D07 owns harm states and recovery consequences. It does not own every cause of harm. D03 owns Power Economy mechanics. D04 owns advancement proof and breakthrough gates. D05 owns skills, diagnosis, research, training, treatment competence, and recovery projects. D06 owns Routes, Paths, Principles, Techniques, route features, route mutation/severance structure, and route contradiction. D08 owns actor-state, kinform, companions, spirits, AI, summons, bonds, and personhood complications. D09 owns items, relics, implants, prosthetics, platforms, vehicles, ships, mechs, and external anchors. D10 owns factions, law, reputation, territory, settlement, environment, world-state, and social consequences. Source-local systems remain bounded unless formally normalized or canon-promoted.

## Purpose

This file is the D07 control ledger. It consolidates accepted decisions, ownership boundaries, validation checklists, owner handoff matrix, source-local controls, and risk controls.


## Accepted decision register

D07-LHA: Layered Harm Architecture accepted; harm broader than damage; pools remain valid.

D07-DICS: Damage, Condition, Injury, and Scar are separate; severity and persistence required; functional stacking accepted.

D07-CORR: Corruption is distortive contamination; Corruption Conversion rare and gated.

D07-MUT: Mutation is governed transformation-state; dual-state and alternate forms allowed but rare/gated.

D07-IMP: Cognitive, identity, and Principle harm distinguished; agency safeguard accepted.

D07-CPS: D03 failure / D07 consequence boundary accepted; power-strain harm states accepted.

D07-REC: Recovery Outcome Model accepted; scars, externalization, projects, and dual-state maintenance accepted.

D07-TERM: Terminal Harm Gate Model accepted; death is one terminal outcome, not the only one.

D07-RUNTIME: Tiered Harm Record Model accepted; UI grouping and owner handoffs accepted.


## Ownership checklist

D07 owns harm-state classification, escalation, severity, persistence, corruption as harm state, mutation/transformation outcome, identity harm states, Power Economy harm consequences, recovery outcome grammar, terminal harm categories, record doctrine shapes, and UI grouping. It does not own D03/D04/D05/D06/D08/D09/D10 mechanics or source-local systems as canon defaults.

| If the issue concerns... | Owner |
| --- | --- |
| Power Economy pools, carriers, reservoirs, costs, overdraw, Expression mechanics | D03 |
| Proof, advancement, tiers, breakthroughs, Awakening, capstone | D04 |
| Skills, diagnosis, medicine, research, training, treatment competence | D05 |
| Routes, Paths, Principles, Route Features, Techniques, route severance/mutation | D06 |
| Actor-state, kinform, companions, spirits, AI, summons, bonds, personhood | D08 |
| Items, relics, tools, implants, prosthetics, platforms, ships, mechs | D09 |
| Factions, law, reputation, territory, settlement, environment, world-state | D10 |
| Donor-specific sanity, death, mutation, corruption, resurrection, curse systems | Source-local / review |


## Validation checklists

Harm-family checklist: classify physical, fatigue, cognitive, identity, corruption, mutation, carrier, route/principle, bond, anchor/platform, social/oath, environmental, conceptual-resource, source-local, or mixed.

Damage/Condition/Injury/Scar checklist: determine immediate pressure, active state, persistent record, lasting integrated harm, severity, persistence, recovery need, pool interaction, owner impact, durable threshold.

Corruption checklist: distinguish contamination, corruption, instability, mutation; identify target, vector, severity, persistence, recovery, Corruption Conversion possibility, source-local boundary, handoffs.

Mutation checklist: identify source, target, quality, control, stability, triggers, permissions, limits, vulnerabilities, costs, owner validation, source-local status.

Identity checklist: classify subfamily, agency impact, direct-control gates, route/Principle handoff, personhood handoff, source-local sanity boundary.

Carrier checklist: confirm D03 failure first; determine if pool loss became harm; classify power-strain state; preserve D03 boundary.

Recovery checklist: choose recovery goal and determine if project, externalization, D04 proof, or owner tools are required.

Terminal checklist: confirm severity gate, terminal category, warning, mitigation, owner validation, death alternative, cost, durable record.

Runtime checklist: assign record tier, family, visibility, UI group, handoff state, consolidation/retirement, history retention.


## Source-local checklist

For donor or campaign-local harm systems, identify source, retained pieces, Astra outputs, rejected assumptions, prohibited generalization, handoffs, promotion conditions, and quarantine/escalation need. Source-local retention is normal, not failure.


## Handoff matrix

| If the issue concerns... | Owner |
| --- | --- |
| Power Economy pools, carriers, reservoirs, costs, overdraw, Expression mechanics | D03 |
| Proof, advancement, tiers, breakthroughs, Awakening, capstone | D04 |
| Skills, diagnosis, medicine, research, training, treatment competence | D05 |
| Routes, Paths, Principles, Route Features, Techniques, route severance/mutation | D06 |
| Actor-state, kinform, companions, spirits, AI, summons, bonds, personhood | D08 |
| Items, relics, tools, implants, prosthetics, platforms, ships, mechs | D09 |
| Factions, law, reputation, territory, settlement, environment, world-state | D10 |
| Donor-specific sanity, death, mutation, corruption, resurrection, curse systems | Source-local / review |


## Risk controls embedded

1. D07 does not own all consequence.
2. Pools remain usable.
3. Corruption Conversion is rare and gated.
4. Mutation is not random boon generation.
5. Identity harm preserves agency.
6. Conceptual resources have a dedicated file.
7. Terminal harm is gated.
8. Recovery does not erase consequence by default.
9. Source-local systems stay bounded.
10. Record burden is controlled through tiers.


## Post-pack check

After generation, run a D03/D04/D06 patch-note check. Do not rewrite D03/D04/D06 unless contradictions are found.



<!-- FILE: D07_pack_manifest.json -->

```json
{
  "project": "Astra Ascension",
  "pack": "D07 Layered Harm, Recovery, Corruption, Mutation, and Terminal Consequence Doctrine",
  "version": "v0.1",
  "generated_date": "2026-06-01",
  "status": "doctrine draft generated from accepted D07 design decisions",
  "phase": "Phase 1 — Doctrine and framework build",
  "files": [
    "D07-README_manifest.md",
    "D07-00_layered_harm_architecture_overview.md",
    "D07-01_damage_injury_conditions_and_severity.md",
    "D07-02_corruption_contamination_and_instability.md",
    "D07-03_mutation_transformation_and_body_change.md",
    "D07-04_identity_mental_and_principle_harm.md",
    "D07-05_conceptual_resource_exposure_and_integration_harm.md",
    "D07-06_carrier_backlash_and_power_strain_handoff.md",
    "D07-07_recovery_treatment_stabilization_and_adaptation.md",
    "D07-08_lethality_crippling_and_failure_consequences.md",
    "D07-09_runtime_records_ui_and_owner_handoffs.md",
    "D07-10_integration_checklists_and_ddr_register.md",
    "D07_pack_manifest.json",
    "astra_d07_doctrine_pack_combined_v0_1.md"
  ],
  "depends_on": [
    "D03 Power Economy and Expression doctrine",
    "D04 Advancement, proof, breakthrough, and capstone doctrine",
    "D05 Competency, profession, method, research, and advancement-track routing doctrine",
    "D06 Route, Path, Technique, Principle, and source-local route doctrine"
  ],
  "feeds": [
    "D08 Actor-state, kinform, companion, spirit, AI, bond, summon doctrine",
    "D09 Item, relic, implant, prosthetic, platform, vehicle, tool, and anchor doctrine",
    "D10 Faction, law, territory, environment, settlement, and world-state doctrine",
    "Future runtime/schema phase",
    "Conversion pipeline source-local harm handling",
    "Core sourcebook consolidation"
  ],
  "accepted_decisions": [
    "Layered Harm Architecture",
    "Damage / Condition / Injury / Scar distinction",
    "Corruption as distortive contamination",
    "Governed Mutation and Transformation",
    "Layered Cognitive, Identity, and Principle Harm",
    "D03 Failure / D07 Consequence boundary",
    "Recovery Outcome Model",
    "Terminal Harm Gate Model",
    "Tiered Harm Record Model",
    "Dedicated conceptual-resource exposure file"
  ],
  "risk_controls": [
    "D07 does not become universal consequence owner",
    "Pools remain valid and are not replaced by harm states",
    "Corruption Conversion is rare, gated, and owner-validated",
    "Mutation is governed and not a random boon table",
    "Identity harm preserves agency except under strict gates",
    "Conceptual-resource harm is cross-owned and source-local where needed",
    "Terminal outcomes are gated and consequence-bearing",
    "Recovery is not always restoration",
    "Source-local harm systems stay bounded",
    "Record burden controlled by ephemeral/session/durable tiers"
  ],
  "required_followups": [
    "Run D03/D04/D06 patch-note check after D07 generation.",
    "Do not perform full upstream amendment unless contradictions are found.",
    "Proceed to D08 only after patch-note check or explicit user instruction."
  ]
}
```
