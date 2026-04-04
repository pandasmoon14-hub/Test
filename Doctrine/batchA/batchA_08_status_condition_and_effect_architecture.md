# batchA_08_status_condition_and_effect_architecture.md

## Status
Draft — Core Now

## Authority
This file is the authoritative doctrine file for Astra's **status, condition, effect, and non-damage state architecture**.

It defines:
- what Astra treats as a condition,
- what Astra treats as an effect,
- what Astra treats as a composite state package,
- how non-damage consequences are applied, carried, persisted, stacked, resisted, suppressed, cleansed, removed, recovered, or concealed,
- how actor-, item-, zone-, link-, and scene-bound states are represented,
- how track-backed, latent, triggered, nested, beneficial, harmful, neutral, and mixed states are handled,
- and how donor-side condition and effect constructs are classified before conversion.

It does **not** define:
- ability-object schema in full,
- resource-cost, recharge, or backlash law,
- damage-family taxonomy,
- progression logic,
- or final donor-specific condition catalogs.

Those belong to other doctrine files.

---

## 1. Purpose

Astra requires a stable architecture for **non-damage consequences**.

Many donor systems apply lasting or semi-lasting state changes that are not reducible to damage alone. Those states may:
- limit action,
- distort movement,
- alter perception,
- impair cognition,
- constrain social agency,
- create ongoing exposure,
- weaken equipment,
- burden a zone,
- establish hidden hazards,
- or grant beneficial protections and enhancements.

This file exists so those consequences do not leak randomly into:
- the ability object model,
- the resource layer,
- the damage taxonomy,
- or ad hoc conversion prose.

Astra therefore treats conditions and effects as a real architectural layer with their own identity, carriers, persistence, stacking, exit logic, and donor-mapping rules.

---

## 2. Scope Boundaries

### 2.1 This file must include
- the distinction between condition, effect, and state package,
- effect carriers and subjects,
- consequence modules for non-damage state change,
- duration and persistence models,
- stacking, escalation, refresh, replacement, coexistence, and immunity-window logic,
- resist / remove / suppress / cleanse / recover handling,
- beneficial, harmful, neutral, and mixed state classes,
- track-backed and exposure-linked states,
- latent and triggered effects,
- zone-, item-, link-, and scene-bound states,
- detectability, concealment, and hidden-state doctrine,
- nested carrier relationships,
- and donor mapping rules for conditions, afflictions, tags, curses, debuffs, buffs, states, zones, and similar constructs.

### 2.2 This file must not include
- damage-family meaning in full,
- full ability definitions,
- full resource-cost or backlash rules,
- progression-track law,
- detailed package grants for classes, paths, ancestries, or backgrounds,
- or a final exhaustive Astra condition list.

### 2.3 Interpretation rule
If a question asks **what non-damage state now exists, what that state does, how long it persists, how it stacks, how it ends, or how it propagates to actors, items, zones, links, or scenes**, it belongs here.

If a question asks **what damage family is involved, what an ability object looks like, how the cost is paid, or how progression modifies the actor long-term**, it belongs elsewhere.

### 2.4 Anti-collapse rule
A condition is not automatically a damage rule.

An effect is not automatically a resource rule.

A track is not automatically a condition.

A tag is not automatically a condition or effect.

This file governs the architecture of non-damage state consequences by function, not by donor label.

---

## 3. Core Condition and Effect Principles

### 3.1 Non-damage consequences are first-class doctrine
Astra treats non-damage consequences as a stable rules layer rather than a loose appendix attached to attacks, spells, items, or scenes.

### 3.2 Classification is by function, not donor name
A donor may call a construct a:
- condition,
- status,
- affliction,
- debuff,
- buff,
- curse,
- contamination,
- hazard,
- tag,
- aspect,
- stigma,
- blessing,
- ward,
- state,
- or similar term.

Astra does not inherit the donor label automatically.

Before conversion, Astra classifies whether the donor construct is functioning as:
- a named standardized condition,
- an effect,
- a state package,
- a track-backed exposure,
- a latent trigger,
- a zone- or scene-bound state,
- a hidden state,
- or a mixed construct that must be split.

### 3.3 Conditions and effects may be harmful, beneficial, neutral, or mixed
Astra does **not** treat this file as a debuff-only graveyard.

A state may be:
- harmful,
- beneficial,
- neutral,
- or mixed.

Beneficial states, protections, concealment, wards, boons, temporary enhancements, and passive environmental supports have equal architectural legitimacy with poisons, curses, control effects, and debilities.

### 3.4 Every valid state needs behavior and exit logic
A non-damage state is not fully defined merely by its name.

A valid Astra state must be understood through at least:
- what it changes,
- where it is carried,
- how it persists,
- how it interacts with repeated application,
- and how it ends, is removed, is suppressed, is resisted, or becomes non-reapplicable.

### 3.5 Effect architecture must support multiple carriers
Astra conditions and effects may belong to:
- actors,
- items and equipment,
- platforms and frames,
- zones,
- links,
- scenes,
- structures,
- or nested combinations of those carriers.

Astra therefore does not assume every meaningful state lives only on a body.

### 3.6 Composite outcomes are lawful
A single state package may bundle multiple non-damage consequence modules and may coexist with damage, without damage becoming the defining criterion of the package.

### 3.7 Hidden and delayed states are legitimate states
A condition or effect may be:
- public,
- concealed,
- partially visible,
- latent,
- armed,
- triggered later,
- or only revealed after detection, disbelief, inspection, exposure, or other threshold events.

---

## 4. Condition vs Effect vs State Package

### 4.1 Condition
A **condition** is a named state with standardized mechanical meaning.

Use a condition when Astra needs a stable, reusable state label whose functional behavior is expected to remain substantially consistent across sources.

A condition should answer:
- what restrictions or changes it imposes,
- what kind of subject can carry it,
- how it persists,
- and how it ends.

A condition is not merely decorative flavor text.

### 4.2 Effect
An **effect** is any non-damage rule consequence that changes an actor, object, zone, link, scene, or other carrier.

An effect may:
- grant a condition,
- modify values,
- alter visibility,
- change movement or action options,
- create a zone,
- alter interaction rules,
- create a hidden state,
- impose a trigger,
- or bundle multiple modules together.

An effect need not always be represented as one named condition.

### 4.3 State package
A **state package** is a bundled set of one or more conditions, effects, modifiers, restrictions, triggers, durations, and exit rules applied as a coherent whole.

Use a state package when a donor construct cannot be represented cleanly by one condition alone.

Examples of package shape include:
- condition plus penalty plus forced-behavior clause,
- zone plus repeated exposure check,
- hidden curse plus source-specific reveal and cure logic,
- or beneficial protection plus upkeep and expiration behavior.

### 4.4 Shell states and source-defined payloads
Some named states primarily function as a shell whose exact payload depends on source.

Astra allows such shell states, but requires that the source-specific payload still be explicitly defined and not smuggled in by implication.

---

## 5. Effect Subjects and Carriers

### 5.1 Subject
The **subject** is the thing currently changed by the state.

The subject may be:
- an actor,
- a body,
- a mind,
- a spirit-like frame,
- an item,
- equipment,
- a vehicle,
- a platform,
- a summon,
- a companion,
- a link,
- a zone,
- a room,
- a site,
- a scene,
- or a donor-local equivalent.

### 5.2 Carrier
The **carrier** is where the state is anchored.

Carrier and subject may be the same, but do not have to be.

Examples:
- a curse carried by an item but affecting its wearer,
- a zone effect carried by a location but affecting entrants,
- a scene effect carried by the scene and altering all tests within it,
- a link effect carried by a bond between subjects,
- an armor degradation state carried by equipment,
- or a hidden ward carried by a structure.

### 5.3 Nested carriers
Astra explicitly supports **nested carrier relationships**.

A state may be carried by one object and repeatedly apply secondary states to another subject on:
- entry,
- use,
- time passage,
- inspection,
- attack,
- exposure,
- or other trigger windows.

This is important for:
- hazardous zones,
- cursed equipment,
- region afflictions,
- trap-like states,
- and persistent environmental or scene burdens.

---

## 6. Effect Modules and Consequence Types

A valid effect or state package may contain one or more consequence modules.

### 6.1 Common module families
A module may:
- restrict action,
- restrict movement,
- alter positioning,
- alter detection or visibility,
- apply penalties or bonuses,
- impose control constraints,
- alter communication,
- alter targeting,
- alter recovery or rest behavior,
- create ongoing exposure,
- alter equipment or object function,
- create or alter a zone,
- create or alter a link,
- require checks or saves over time,
- establish a latent trigger,
- or define source-specific removal demands.

### 6.2 Track-backed modules
A module may reference a track, magnitude, exposure score, or graded burden.

This does **not** make the track itself a condition by default.

### 6.3 Mixed consequence packages
A package may be:
- purely harmful,
- purely beneficial,
- neutral but behaviorally important,
- or mixed.

Astra allows mixed packages such as:
- a buff with a hidden drawback,
- a curse that grants power while imposing risk,
- or a zone that helps one population and hinders another.

---

## 7. Duration and Persistence Models

Astra recognizes that non-damage states persist in different ways.

### 7.1 Supported persistence families
A state may be:
- instantaneous rider,
- fixed-duration,
- save-ends,
- action-ends,
- heal-ends,
- repair-ends,
- source-bound,
- maintained,
- exposure-based,
- cumulative,
- indefinite until removed,
- conditional on proximity, link, or equipment state,
- latent until triggered,
- or scene-/encounter-bound.

### 7.2 Ongoing versus dormant persistence
A state may persist while actively producing consequences, or it may persist in a dormant or armed state until a trigger condition is met.

### 7.3 Exit logic is mandatory
Every valid state should define one or more exit paths, such as:
- lapse by duration,
- save or resistance event,
- action-based removal,
- cleansing procedure,
- healing,
- repair,
- source destruction,
- disbelief or revelation,
- leaving a carrier or scene,
- special cure,
- or source-specific resolution.

A state without exit logic is incomplete.

---

## 8. Stacking, Escalation, Refresh, Replacement, and Coexistence

### 8.1 Stacking is never assumed
Astra does **not** assume that repeated application of the same or similar state automatically stacks.

Every condition family or effect family must specify how repeated application behaves.

### 8.2 Supported repeat-application models
Repeated application may:
- be ignored,
- refresh duration,
- refresh a trigger window,
- increase magnitude,
- increase exposure,
- escalate to a stronger family state,
- coexist as separate instances,
- replace the weaker instance,
- replace the older instance,
- merge into one package,
- or apply only from distinct sources.

### 8.3 Replacement versus coexistence
When a new state of the same family arrives, Astra should explicitly determine whether it:
- refreshes,
- escalates,
- replaces,
- coexists,
- or is ignored.

This rule is especially important for:
- fear families,
- poison families,
- concealment families,
- curse variants,
- slow/freeze families,
- and repeated equipment degradation.

### 8.4 Immunity windows and temporary non-reapplication
Astra supports **immunity windows** and temporary non-reapplication states.

A subject may, after:
- a successful resist,
- a successful recovery,
- expiration,
- source-specific purge,
- or effect completion,
become temporarily immune or non-valid for immediate reapplication of the same family.

This immunity or non-reapplication state is itself part of the family’s handling logic and must be declared rather than assumed.

---

## 9. Resist, Remove, Suppress, Cleanse, and Recover

These are separate doctrinal operations.

### 9.1 Resist
**Resist** means preventing, reducing, or qualifying application when the state is first attempted or when a later resist window opens.

### 9.2 Remove
**Remove** means ending an existing state.

Removal may be generic or source-specific.

### 9.3 Suppress
**Suppress** means temporarily disabling or muting a state without fully ending it.

A suppressed state may return when the suppressing cause ends.

### 9.4 Cleanse
**Cleanse** means removing a state through a specific curative, purifying, sanctifying, decontaminating, or otherwise specialized procedure.

### 9.5 Recover
**Recover** means leaving the state through normal passage of time, successful checks, recovery procedures, or other built-in exit behavior.

### 9.6 Repair and restoration
Item-, armor-, structure-, vehicle-, and platform-bound states may require **repair** or equivalent restoration rather than healing.

### 9.7 Detect, reveal, and disbelieve
Hidden, illusory, disguised, or latent states may require:
- detection,
- revelation,
- inspection,
- confrontation,
- disbelief,
- or source exposure
before meaningful removal or resistance options become available.

---

## 10. Visibility, Concealment, and Detectability

### 10.1 Public versus hidden states
A state may be:
- openly visible,
- privately known,
- concealed from some observers,
- disguised as another state,
- latent and undetected,
- or only inferable through symptoms or triggers.

### 10.2 Detectability is part of the architecture
Some states matter even before they are known.

Astra therefore treats detectability as a first-class property rather than an afterthought.

### 10.3 Hidden states require reveal pathways
A hidden state should define one or more reveal pathways such as:
- inspection,
- magical or technical scan,
- symptom threshold,
- triggered disclosure,
- contradiction with observed reality,
- source revelation,
- or donor-specific equivalent.

---

## 11. Beneficial, Harmful, Neutral, and Mixed States

### 11.1 Harmful states
Harmful states burden, constrain, distort, or endanger their subjects.

### 11.2 Beneficial states
Beneficial states protect, enhance, conceal, restore, support, or empower their subjects.

### 11.3 Neutral states
Neutral states may be informational, classificatory, situational, or preparatory while still mattering to adjudication.

### 11.4 Mixed states
Mixed states combine helpful and harmful components, or shift value depending on context, allegiance, frame, or source.

Astra treats all four categories as legitimate parts of the same architecture.

---

## 12. Control States, Impairments, Exposures, and Track-Backed States

### 12.1 Control states
Astra recognizes a family of **control states** that alter agency.

These may include:
- action restriction,
- movement denial,
- targeting constraints,
- compelled approach or retreat,
- cognitive interference,
- behavioral distortion,
- social compliance pressure,
- or similar limitations.

### 12.2 Impairment states
Astra recognizes impairment families affecting:
- action quality,
- perception,
- balance,
- coordination,
- cognition,
- communication,
- or system performance.

### 12.3 Exposure and tracker-linked states
Some states reference ongoing magnitude, accumulation, or exposure logic.

Examples of family shape include:
- contamination,
- poison burden,
- bleeding intensity,
- radiation burden,
- infection,
- corrosion,
- corruption,
- signal trace,
- or donor-local equivalents.

Astra requires explicit doctrine for whether the track:
- feeds the condition,
- is fed by the condition,
- coexists beside the condition,
- or merely records severity.

A track is not automatically a condition.

---

## 13. Zone-, Link-, Scene-, and Object-Bound States

### 13.1 Zone-bound states
A state may be carried by a zone or region and affect subjects on:
- entry,
- exit,
- presence,
- movement through,
- time passage,
- or other trigger events.

### 13.2 Link-bound states
A state may exist on a link between subjects, such as:
- telepathic links,
- curse bonds,
- control channels,
- contagion chains,
- command relays,
- or donor-local equivalents.

### 13.3 Scene-bound states
A state may alter a whole scene’s assumptions, visibility, interaction rules, environmental pressures, or response windows.

### 13.4 Object- and equipment-bound states
Items, armor, weapons, relics, implants, vehicles, platforms, or structures may carry states that:
- degrade them,
- empower them,
- hide them,
- corrupt them,
- limit their functions,
- or alter the condition of their users.

Astra therefore rejects any assumption that all meaningful states belong only to living actors.

---

## 14. Latent, Triggered, Composite, and Nested Effects

### 14.1 Latent effects
A **latent effect** is present but not yet actively expressing its consequences.

It may require:
- contact,
- inspection,
- activation,
- damage,
- entry,
- time passage,
- or another trigger before becoming active.

### 14.2 Triggered effects
A **triggered effect** activates when a declared condition is met.

Triggers may include:
- entering a zone,
- using an item,
- speaking a phrase,
- failing a check,
- receiving healing,
- crossing a threshold,
- or donor-local equivalents.

### 14.3 Composite effects
A **composite effect** contains multiple coordinated modules.

Examples of composite shape include:
- zone plus repeated poison check,
- fear plus movement restriction,
- blessing plus hidden curse rider,
- item degradation plus wielder penalty,
- or illusion plus disbelief interaction plus reveal threshold.

### 14.4 Nested effects
A **nested effect** is an effect carried by one thing that applies further states to other subjects over time or under trigger conditions.

Astra explicitly supports this relationship and does not require all effects to be flat.

---

## 15. Donor Mapping Rules

### 15.1 Donor labels are not binding
If a donor calls something a:
- condition,
- status,
- buff,
- debuff,
- hazard,
- contamination,
- blessing,
- curse,
- tag,
- scene effect,
- stance,
- environmental rule,
- or affliction,
Astra still classifies the construct by function first.

### 15.2 First-pass donor classification questions
When mapping a donor state, Astra should ask:
1. Is this a standardized named condition, a broader effect, or a composite package?
2. What is the subject and what is the carrier?
3. Is the state harmful, beneficial, neutral, or mixed?
4. Is the state public, concealed, latent, or revealed only by trigger?
5. Does it reference tracks, counters, or exposure values?
6. How does repeated application behave?
7. How does the state end, and can it create immunity windows or non-reapplication states?
8. Is it actor-bound, item-bound, link-bound, zone-bound, scene-bound, or nested?
9. Does it belong here, or is part of it actually ability structure, damage law, access law, or resource law?

### 15.3 Split mixed constructs when necessary
If a donor construct bundles:
- damage,
- access restriction,
- resource burden,
- progression mutation,
- and non-damage state change,
Astra should split the construct into its proper doctrine layers rather than importing the whole bundle intact.

---

## 16. Explicit Exclusions and Downstream Ownership

### 16.1 This file does not own ability objects
Ability objects belong to `batchA_07_ability_object_model.md`.

This file may define what states an ability can apply, but not the full ability schema.

### 16.2 This file does not own resource or backlash law
Cost, recharge, upkeep, exhaustion, debt, and backlash belong to `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`.

### 16.3 This file does not own damage-family meaning
Damage-family taxonomy, resistance, vulnerability, immunity, absorption, and recovery interaction belong to `batchA_09_damage_family_and_resistance_taxonomy.md`.

### 16.4 This file does not own broad access law
Permissions, access tags, proficiency gates, and lawful qualification belong to `batchA_06_access_tags_permissions_and_proficiency_gates.md`.

### 16.5 This file does not own progression law
Long-form advancement and progression-axis doctrine belong to `batchA_10_progression_axes.md` and related later files.

---

## 17. Canonical Astra Rules from This File

1. A condition is a named standardized state; an effect is a broader non-damage consequence; a state package is a bundled cluster of multiple consequence modules.
2. Non-damage states may be harmful, beneficial, neutral, or mixed.
3. States may be carried by actors, items, frames, zones, links, scenes, structures, or nested carrier relationships.
4. A valid state requires persistence logic and exit logic.
5. Repeated application never has an implicit meaning; refresh, escalation, replacement, coexistence, and immunity windows must be declared.
6. Resist, remove, suppress, cleanse, repair, detect, and recover are distinct doctrinal operations.
7. Tracks may support conditions, but tracks are not automatically conditions.
8. Hidden, latent, and triggered states are legitimate parts of Astra’s effect architecture.
9. Effects may create secondary states through nested carriers and trigger windows.
10. This file governs non-damage state architecture only and does not absorb ability schema, resource law, or damage taxonomy.
