# batchA_07_ability_object_model.md

## Status
Draft — Core Now

## Authority
This file is the authoritative doctrine file for Astra's **ability object model**.

It defines:
- what Astra recognizes as a discrete ability object,
- the minimum and extended record fields for ability objects,
- how activation, timing, scope, persistence, payload, and resolution linkage are represented,
- how single abilities, ability families, and spawned secondary objects are modeled,
- how abilities may reference access, capability, resource, condition, damage, and progression layers without owning them,
- how abilities may be sourced, held, delivered, granted, borrowed, inherited, or platform-mediated,
- and how donor-side spells, powers, techniques, maneuvers, stances, psionics, cyberware functions, biotech activations, relic powers, tool actions, routines, forms, and similar constructs are classified before conversion.

It does **not** define:
- practical non-activated capability,
- access law or gate satisfaction,
- resource cost, recharge, slot, fuel, upkeep economy, backlash economy, or overextension law in full,
- condition and effect architecture in full,
- damage-family taxonomy in full,
- progression formulas,
- or detailed package-grant tables for paths, professions, ancestries, backgrounds, or loadouts.

If any later Batch A file appears to contradict this file on the **structure, classification, or ownership of discrete invoked effect constructs**, this file governs unless deliberately revised.

---

## 1. Purpose

Astra requires a stable schema for discrete invoked effects.

Donor systems express these constructs through many labels, including:
- spell,
- skill,
- power,
- technique,
- maneuver,
- stance,
- exploit,
- rite,
- invocation,
- cyberware routine,
- biotech function,
- relic activation,
- tool action,
- command routine,
- summon call,
- form,
- or donor-local equivalents.

This file exists to prevent five common failures:
- **label capture**, where a donor's preferred noun is treated as Astra law,
- **ability / capability / access collapse**, where training, permission, and effect payload are fused together,
- **prose drift**, where ability records become decorative paragraphs rather than reusable objects,
- **single-effect bias**, where every ability is assumed to do only one thing in one step,
- and **sheet-local bias**, where abilities are assumed to originate from only the actor rather than from items, platforms, summons, sites, or other holders.

Astra therefore treats an ability as an object with a lawful record shape.

---

## 2. Scope Boundaries

### 2.1 This file must include
- doctrine for what qualifies as an ability object,
- minimum core record requirements,
- extended record fields,
- activation and timing models,
- scope and targeting models,
- duration, persistence, and maintenance-state handling,
- effect payload models,
- composite payload doctrine,
- spawned secondary-object doctrine,
- resolution-link models,
- failure, interruption, exception, and response-class handling,
- scaling, upgrade, and family logic,
- ability source, holder, and delivery-platform distinctions,
- grant, inheritance, borrowing, copying, and acquisition-state handling at the schema level,
- and donor mapping rules for invoked constructs.

### 2.2 This file must not include
- capability lists or practical know-how doctrine in full,
- access-law evaluation in full,
- resource economy in full,
- condition definitions in full,
- damage-family definitions in full,
- progression ladders,
- chargen sequencing,
- or exhaustive donor ability catalogs.

### 2.3 Interpretation rule
If a question asks **what a discrete invoked construct is, how it is activated, what it can target, how long it persists, what payload modules it produces, what resolution link it uses, or how it is represented as a reusable rules object**, it belongs here.

If a question asks **whether the subject may lawfully use the construct, how the cost is paid, what a referenced condition means, what a damage family means, or how a progression path grants it**, it belongs elsewhere.

### 2.4 Anti-collapse rule
An ability object is **not** a broad practical capability.

An ability object is **not** a permission state.

An ability object may reference capability, access, resolution, resource, condition, damage, or progression systems, but it does **not** own or redefine them.

---

## 3. Core Ability-Object Principles

### 3.1 Ability objects are discrete invoked constructs
An **ability object** is a discrete rules-bearing construct that may be activated, triggered, sustained, maintained, passively applied, or otherwise invoked as a specific effect-bearing unit.

An ability object is identified by its object-level behavior, not by donor naming convention.

### 3.2 Classification is by function, not donor label
A donor may call a construct a skill, feat, stunt, exploit, invocation, prayer, module, hack, trick, or stance.

Astra does not inherit that label automatically.

Before conversion, Astra must classify whether the construct is actually functioning as:
- a practical capability,
- an access-gated permission state,
- an ability object,
- a resource mechanic,
- a trait or passive rules modifier,
- a condition/effect package,
- or a mixed construct that must be split across files.

### 3.3 Field categories are rigid; donor expression is flexible
Astra standardizes the **field categories** an ability object may use.

Astra does **not** require every donor to express every field in the same surface format.

This allows one schema family to absorb fantasy, sci-fi, cultivation, psionic, cyberware, relic, biotech, tactical, narrative, and hybrid donors without becoming either mush or bureaucracy.

### 3.4 Ability objects may be simple or complex
An ability object may be:
- one-shot,
- passive,
- reactive,
- sustained,
- mode-switching,
- transformative,
- table-driven,
- modular,
- family-linked,
- platform-mediated,
- or secondary-object-generating.

Astra therefore does not assume every ability is a single instant payload with one roll and one result.

### 3.5 Ability objects may carry one or more payload modules
An ability may contain **one or more payload modules**.

It may therefore produce:
- one effect,
- several simultaneous effects,
- an effect plus a modifier,
- an effect plus forced movement,
- a summon plus control logic,
- a transformation plus a temporary action profile,
- or other lawful composite structures.

### 3.6 Ability objects may create secondary rules objects
An ability may instantiate or alter secondary rules objects such as:
- zones,
- links,
- hazards,
- summons,
- constructs,
- walls,
- portals,
- persistent objects,
- temporary modes,
- alternate forms,
- companion routines,
- or donor-local equivalents.

Those secondary objects may require their own records, but the ability object must have fields that lawfully reference their creation or control.

### 3.7 Ability objects must survive multiple donor genres
Astra ability-object doctrine must remain stable across:
- spells,
- martial maneuvers,
- psionic powers,
- cyberware activations,
- biotech functions,
- relic abilities,
- tool procedures,
- vehicle systems,
- summon controls,
- ritual packages,
- narrative-technique donors,
- and mixed or unusual subsystem donors.

---

## 4. What Qualifies as an Ability Object

A construct qualifies as an Astra ability object if it functions as a **specific reusable effect-bearing unit** with one or more of the following properties:
- defined activation or trigger logic,
- bounded scope or target logic,
- bounded persistence or maintenance logic,
- explicit payload behavior,
- explicit response timing,
- explicit resolution linkage,
- explicit state change,
- explicit creation of a secondary object,
- or explicit upgrade/scaling behavior.

Constructs that are merely broad know-how, passive credentials, raw resource quantities, or pure background facts do not qualify unless another file expressly converts them into ability-bearing form.

---

## 5. Minimum Core Record

Every Astra ability object must be representable by a minimum core record containing the following field families.

### 5.1 Identity
The record must identify the ability as a distinct object.

Minimum identity fields should support:
- ability name or stable object label,
- object identifier or conversion-stable key,
- and short classification summary.

### 5.2 Classification
The record must identify what sort of ability object it is.

Classification may include:
- ability class,
- source family,
- delivery family,
- and donor-local subtype if needed.

### 5.3 Activation
The record must state how the ability enters play.

Minimum activation fields must support:
- activation state,
- action timing or trigger window,
- and initiation requirements if any exist.

### 5.4 Scope
The record must state what the ability can affect.

Minimum scope fields must support:
- target class,
- range or contact relationship,
- and area or count if applicable.

### 5.5 Payload summary
The record must state what kind of effect the ability produces at a high level.

The minimum record may summarize payload as one or more modules rather than full detail.

### 5.6 Resolution link
The record must state how the ability connects to adjudication.

This does not require full numeric implementation, but it must identify the relevant resolution mode.

### 5.7 Persistence
The record must state whether the ability is:
- instantaneous,
- persistent,
- sustained,
- maintained,
- passive while present,
- or otherwise ongoing.

---

## 6. Extended Record Fields

An ability object may also include extended fields where required.

### 6.1 Requirements
The record may declare:
- access tags,
- gate references,
- compatibility requirements,
- holder requirements,
- platform requirements,
- target restrictions,
- environment restrictions,
- prerequisite abilities,
- and donor-local preconditions.

### 6.2 Maintenance state
The record may distinguish **maintenance behavior** from initial activation.

This may include:
- concentration,
- channeling,
- upkeep state,
- reaffirmation window,
- maintained link state,
- or similar persistence behavior.

This field exists even when the cost economy that supports it is owned by `07b`.

### 6.3 Instance and stacking limits
The record may declare:
- number of concurrent instances,
- stacking rules,
- exclusivity rules,
- mode conflicts,
- and holder/platform conflicts.

### 6.4 Restriction notes
The record may specify:
- invalid target classes,
- terrain restrictions,
- body-state restrictions,
- line-of-effect restrictions,
- interaction-type restrictions,
- and donor-local lawful limitations.

### 6.5 Secondary-object references
The record may identify one or more created or controlled secondary objects and their relationship to the parent ability.

### 6.6 Upgrade and scaling references
The record may specify how the ability improves, branches, intensifies, expands, mutates, or otherwise scales.

### 6.7 Acquisition-state references
The record may note whether the ability is:
- native,
- granted,
- inherited,
- copied,
- borrowed,
- installed,
- equipped,
- learned,
- bonded,
- or donor-locally transferred.

This field does not replace the ownership of progression or package doctrine elsewhere.

---

## 7. Activation and Timing Models

### 7.1 Activation states
An ability may be represented as:
- passive,
- activated,
- reactive,
- triggered,
- sustained,
- maintained,
- toggled,
- stance-like,
- mode-switching,
- transformative,
- or donor-local equivalents.

### 7.2 Initiation timing
Activation timing may include:
- immediate use,
- standard or main action use,
- minor or quick use,
- reaction,
- interrupt,
- free or incidental use,
- predeclared use,
- delayed release,
- charge-up,
- ritual preparation,
- deployment,
- or other donor-native timing models.

### 7.3 Trigger windows and response class
A response-type ability must support at least:
- trigger window,
- event being responded to,
- response class,
- and relationship to the triggering event.

A response class may indicate whether the ability:
- follows,
- modifies,
- interrupts,
- negates,
- replaces,
- reflects,
- hijacks,
- or otherwise rewrites the triggering event.

### 7.4 Transformation and mode-switch activation
Some abilities do not merely apply a one-shot effect.

They may instead:
- enter a mode,
- apply a stance,
- replace part of the actor's active profile,
- create a temporary form,
- install an alternate action package,
- or switch the holder into another lawful operating state.

Such abilities remain ability objects and must be represented accordingly.

---

## 8. Scope and Targeting Models

### 8.1 Valid scope classes
Ability scope may lawfully reference:
- self,
- ally,
- enemy,
- neutral actor,
- object,
- item,
- corpse,
- site,
- structure,
- zone,
- platform,
- summon,
- companion,
- vehicle,
- environment,
- or donor-local target classes.

### 8.2 Range and contact relationships
Range may be represented by:
- self,
- touch,
- reach,
- line,
- sight,
- zone,
- scene,
- linked target,
- platform-local,
- networked,
- remote,
- or other donor-native range forms.

### 8.3 Area and multiplicity
An ability may affect:
- one target,
- several targets,
- a burst,
- a cone,
- a line,
- a radius,
- a zone,
- a chain,
- a sequence,
- or another lawful multiplicity model.

### 8.4 Link-target and object-mediated targeting
Some abilities act through:
- bonded links,
- command channels,
- relays,
- marked targets,
- implanted nodes,
- named objects,
- or summoned intermediaries.

The schema must support target mediation rather than assuming all abilities target directly.

---

## 9. Effect Payload Models

### 9.1 Payload modules
Ability payload should be modeled as one or more **payload modules**.

A payload module may represent:
- damage,
- healing,
- movement,
- forced repositioning,
- defense shift,
- modifier grant,
- condition application,
- condition removal,
- cleanse/suppress effect,
- summon call,
- control command,
- mode shift,
- transformation,
- object creation,
- zone creation,
- link creation,
- illusion,
- barrier,
- reveal/hide effect,
- information transfer,
- restoration,
- duplication,
- payload replacement,
- or donor-local effects.

### 9.2 Composite payload rule
An ability may contain multiple payload modules at once.

Astra therefore does not assume one ability equals one effect.

### 9.3 Secondary-object payloads
The following payload families must be explicitly supported:
- object creation,
- zone creation,
- entity creation,
- entity control,
- link creation,
- and form or mode package creation.

### 9.4 Payload references to external doctrine
A payload may reference:
- condition objects,
- effect objects,
- damage families,
- access tags,
- capability interactions,
- progression hooks,
- and resource interactions.

Those references do not transfer ownership of those doctrines into this file.

---

## 10. Resolution-Link Models

### 10.1 Resolution linkage is required
Every ability object must state how it connects to Astra's resolution framework.

### 10.2 Supported resolution-link classes
At minimum, the model must support:
- automatic resolution,
- binary resolution,
- graded resolution,
- table/band resolution,
- hybrid resolution,
- opposed or contested resolution,
- generated-threshold resolution,
- and donor-local lawful variants.

### 10.3 Ability objects do not own the whole resolution system
The ability record may identify:
- attack-style resolution,
- standard test,
- contest,
- save against generated threshold,
- passive opposition,
- automatic application,
- table lookup,
- or another lawful link.

It does not restate the full doctrine of tests, contests, saves, carriers, or consequence packages. That belongs to `batchA_03_resolution_framework.md`.

### 10.4 Non-binary outcome support
The schema must support abilities whose outcomes are:
- pass/fail,
- scaled by result band,
- chosen from a table,
- escalated by threshold bands,
- or split between result grade and consequence package.

---

## 11. Duration, Persistence, and Instance Logic

### 11.1 Persistence classes
An ability may be:
- instant,
- temporary,
- ongoing,
- sustained,
- maintained,
- passive while present,
- toggled,
- permanent until removed,
- delayed,
- latent until triggered,
- or donor-local equivalents.

### 11.2 Maintenance and concentration distinction
A maintained ability is not identical to an instantaneous or merely timed ability.

The schema must therefore support ongoing maintenance state even when the actual upkeep cost or recharge economy is handled elsewhere.

### 11.3 Instance logic
An ability record may declare:
- whether multiple instances may coexist,
- whether one instance replaces another,
- whether instances stack,
- whether the holder may maintain several at once,
- and whether the target may host several copies.

### 11.4 Overlay and form persistence
Some abilities temporarily replace or overlay baseline behavior rather than adding a simple modifier.

The model must support temporary forms, stances, modes, alternate profiles, or similar overlay states.

---

## 12. Scaling, Upgrade, and Family Logic

### 12.1 Scaling
An ability may scale by:
- holder statistics,
- target count,
- potency tier,
- range increase,
- duration increase,
- payload expansion,
- additional modules,
- donor-local branching,
- or other lawful scaling models.

### 12.2 Upgrade and branch structure
Some abilities improve through:
- upgrades,
- branches,
- side grades,
- specialization,
- chained forms,
- add-on riders,
- or tier-unlocked expansions.

The schema must support these references without forcing every ability to use them.

### 12.3 Ability families
Astra recognizes both:
- **single abilities**, which stand alone,
- and **ability families**, which share common metadata, source logic, or upgrade structure across several related abilities.

### 12.4 Source is not type
An ability's source category does not by itself determine its object structure.

A relic beam, a psionic scream, a cyberware overdrive, and a martial maneuver may all use the same schema family even when their fiction and acquisition differ.

---

## 13. Requirements and External References

### 13.1 Access requirements remain external law
An ability record may declare required:
- access tags,
- gate classes,
- licenses,
- schools,
- traditions,
- training marks,
- compatibility states,
- or donor-local access prerequisites.

The ability object does not decide whether those requirements are satisfied. That belongs to `batchA_06_access_tags_permissions_and_proficiency_gates.md`.

### 13.2 Capability references remain external doctrine
An ability may reference:
- required capability,
- capability threshold,
- tool-linked capability,
- language or literacy precondition,
- or donor-local know-how references.

The doctrine of practical capability remains owned by `batchA_05_competency_and_skill_translation_architecture.md`.

### 13.3 Resource references remain external doctrine
An ability may declare that activation, maintenance, recharge, recovery, overextension, or catastrophe interacts with a resource model.

The doctrine of those resource economies remains owned by `07b` and later related files.

### 13.4 Condition and damage references remain external doctrine
An ability may reference conditions, effects, damage families, resistances, immunities, or vulnerabilities.

The meaning of those constructs remains owned elsewhere.

---

## 14. Failure, Interruption, and Exception Handling

### 14.1 Failure surface
An ability record may define or reference:
- fail state,
- invalid target state,
- resisted state,
- interruption state,
- lost-target state,
- misfire,
- partial application,
- catastrophe band,
- and donor-local exception handling.

### 14.2 Interruption and replacement
The model must support abilities that:
- are interrupted,
- interrupt others,
- replace a normal action,
- replace another effect,
- negate a trigger,
- or reroute an event.

### 14.3 Exceptions and immunity notes
An ability record may include exception notes such as:
- target immunities,
- valid biology or frame class,
- environmental restrictions,
- source restrictions,
- and donor-local exclusions.

### 14.4 Failure-state scope discipline
This file may represent failure-state fields, but it does not absorb the entire doctrine of backlash, recharge failure, overcast law, or catastrophic resource economy.

---

## 15. Ability Source, Holder, and Delivery Platform

### 15.1 Source
**Source** identifies where the ability originates conceptually.

Examples may include:
- learned technique,
- path-granted power,
- relic source,
- implant source,
- biotech source,
- lineage source,
- bonded source,
- summon source,
- site source,
- or donor-local origin.

### 15.2 Holder
**Holder** identifies who or what currently possesses the ability in lawful terms.

The holder may be:
- an actor,
- a companion,
- a summon,
- an item,
- a frame,
- a vehicle,
- a crew system,
- a site,
- an institution,
- or another lawful ability bearer.

### 15.3 Delivery platform
**Platform** identifies what physically or systemically delivers the effect when the ability is used.

Examples include:
- body,
- weapon,
- relic,
- implant,
- suit,
- drone,
- vehicle,
- ritual environment,
- command network,
- summon,
- or donor-local medium.

### 15.4 These fields must remain distinct
Source, holder, and delivery platform may coincide, but Astra must not assume they are always the same.

---

## 16. Grant, Borrowing, Inheritance, and Transfer States

### 16.1 Ability possession is not always native
An ability may be:
- native,
- learned,
- granted,
- inherited,
- bonded,
- installed,
- equipped,
- copied,
- borrowed,
- transmitted,
- cloned,
- or otherwise transferred.

### 16.2 Acquisition-state handling is descriptive, not totalizing
This file only ensures the record can represent those states.

It does not replace package, progression, lineage, loadout, or access doctrine that explains **why** those states exist.

### 16.3 Temporary possession states
An ability may be granted or held:
- persistently,
- temporarily,
- conditionally,
- while linked,
- while equipped,
- while transformed,
- or while a donor-local relationship remains active.

---

## 17. Donor Mapping Rules

### 17.1 Functional mapping rule
When a donor-side construct is presented as a skill, feat, power, exploit, trick, rite, hack, module, invocation, maneuver, form, or other named element, Astra must first ask:

Does this function as a discrete invoked effect-bearing object?

If yes, it maps here.

If no, it must be classified elsewhere.

### 17.2 Mixed-construct split rule
If a donor construct combines:
- access qualification,
- practical know-how,
- effect payload,
- resource engine,
- condition definition,
- or progression logic,

Astra must split those components across the proper doctrine files rather than importing the donor object whole.

### 17.3 Simple donor mapping
A simple donor ability may map using only the minimum core record.

### 17.4 Complex donor mapping
A complex donor ability may require:
- extended fields,
- several payload modules,
- family references,
- spawned-object references,
- maintenance behavior,
- and rich failure/exception handling.

### 17.5 Donor labels are evidence, not verdicts
A donor's use of the word “skill” or any equivalent does not determine Astra classification.

---

## 18. Explicit Exclusions and Downstream Ownership

This file does **not** own the full doctrine for:
- practical capability (`batchA_05`),
- access law and gate satisfaction (`batchA_06`),
- resource cost/recharge/backlash economies (`07b`),
- status, condition, and effect architecture (`batchA_08`),
- damage-family taxonomy (`batchA_09`),
- or progression-axis law (`batchA_10`).

This file provides the reusable object model by which ability-bearing constructs can reference those systems without absorbing them.

That division is mandatory.

