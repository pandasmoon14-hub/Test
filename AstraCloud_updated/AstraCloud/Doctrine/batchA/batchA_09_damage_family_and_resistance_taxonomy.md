# batchA_09_damage_family_and_resistance_taxonomy.md

## Status
Draft — Core Now

## Authority
This file is the authoritative doctrine file for Astra's **damage-family taxonomy and resistance interaction architecture**.

It defines:
- what Astra treats as a damage family,
- how damage family differs from delivery form and interaction state,
- the core family architecture Astra uses for donor normalization,
- how resistance, vulnerability, immunity, absorption, restoration, conversion, and related response modes are handled,
- how flat and proportional mitigation are distinguished,
- how conditional, source-bound, state-bound, and granted interaction states are represented,
- how untyped, structural, provisional, and multi-family harm are classified,
- how family-tagged harmful interactions may exist even without direct vitality loss,
- how harm may affect actors, items, frames, vehicles, barriers, zones, structures, and scenes,
- and how donor-side damage language is mapped before it is allowed to alter Astra doctrine.

It does **not** define:
- ability-object schema in full,
- non-damage condition or effect meaning,
- full resource-cost or backlash law,
- full compound or fused-family behavior,
- or final donor-specific exception catalogs.

Those belong to other doctrine files.

---

## 1. Purpose

Astra requires a stable answer to three linked questions:

1. What kinds of harm exist at doctrine level?
2. How do targets, carriers, and systems interact with those harm families?
3. How are donor-specific harm labels normalized without polluting Astra every time a new source invents a fresh pain flavor?

This file exists so harm taxonomy does not dissolve into:
- combat prose,
- donor naming habits,
- ad hoc condition riders,
- or improvised resistance logic.

Astra therefore treats damage families and resistance interaction as a distinct architectural layer.

This file governs the taxonomy of harm and the law of response to harm.
It does **not** attempt to become a combat omnibus, condition compendium, or fusion-effects manual.

---

## 2. Scope Boundaries

### 2.1 This file must include
- the distinction between damage family, delivery form, and interaction state,
- Astra's core harm-family architecture,
- response states such as resistance, vulnerability, immunity, absorption, restoration, reduction, and conversion,
- proportional and flat mitigation distinctions,
- conditional, source-based, state-based, and target-class-based interaction logic,
- treatment of untyped, structural, and provisional donor harm labels,
- multi-family harm recognition,
- family-tagged harmful interactions that may not directly reduce vitality,
- harm targeting for actors, items, vehicles, barriers, zones, structures, and scenes,
- donor mapping and alias discipline,
- and an explicit boundary reserving deeper compound/fusion behavior for `batchA_09b_damage_fusion_and_compound_interactions.md`.

### 2.2 This file must not include
- final condition definitions,
- full combat-turn sequence,
- full ability-object fields,
- resource-cost, recharge, or backlash law,
- full progression interaction law,
- or detailed compound-reaction doctrine beyond the minimum needed to classify and defer it.

### 2.3 Interpretation rule
If a question asks **what family of harm this is, what kind of target response applies, how donor damage labels normalize into Astra, or how a family-tagged harmful interaction is classified**, it belongs here.

If a question asks **what state package the harm caused, what the ability object looked like, what resource paid for it, or what emergent fusion behavior occurs when multiple families combine**, it belongs elsewhere.

### 2.4 Anti-collapse rule
A damage family is not a delivery form.

A damage family is not a condition.

A damage family is not a defense layer.

A damage family is not a resource cost.

A donor label is not automatically an Astra family.

This file classifies harm by doctrine function, not by donor wording.

---

## 3. Core Harm-Taxonomy Principles

### 3.1 Harm taxonomy is first-class doctrine
Astra treats harm families and family-response law as a dedicated framework layer rather than a buried combat note.

### 3.2 Classification is by function, not donor label
A donor may describe harm as:
- fire,
- acid,
- force,
- holy,
- radiant,
- necrotic,
- sonic,
- plasma,
- entropy,
- corruption,
- hellfire,
- warp,
- bioelectric,
- psychic,
- void,
- strain,
- integrity loss,
- hull damage,
- stress,
- shock,
- or any other source-local phrase.

Astra does not promote that label automatically.

Before conversion, Astra asks:
- what doctrinal family job the harm is doing,
- whether it is truly a core family,
- whether it is better treated as a donor-local alias,
- whether it is provisional until later doctrine decides,
- or whether it is not primarily a damage family at all.

### 3.3 Family, delivery, and interaction must stay distinct
Astra separates:
- **damage family** = the doctrine-level category of harm,
- **delivery form** = how the harm arrives,
- **interaction state** = how the target responds to that family.

This prevents donor systems from hiding corrosion rules, splash shapes, shield bypass, and resistance behavior inside one overloaded word.

### 3.4 Harm taxonomy must support more than living bodies
Astra harm law must support harm to:
- living actors,
- spiritual or undead actors,
- constructs,
- items and equipment,
- vehicles and platforms,
- barriers and structures,
- zones and scenes,
- and similar carriers.

### 3.5 Family interaction and defense layers are related but distinct
Armor, shielding, soak, guard, DR, barrier HP, ablative layers, and similar defenses may modify incoming harm, but they are not themselves damage families.

This file governs family classification and response law, not every defense implementation.

### 3.6 Family-tagged harm need not always be direct vitality loss
Some harmful interactions are clearly keyed to a family even when they do not immediately reduce HP, vitality, hull, integrity, or equivalent durability.

Astra therefore allows family-tagged harmful interactions that:
- disrupt,
- contaminate,
- corrode,
- irradiate,
- destabilize,
- suppress,
- scar,
- or otherwise inflict meaningful family-keyed harm without immediate direct vitality subtraction.

### 3.7 Multi-family harm is legal, but fusion is not assumed
A single harm event may carry one or more damage families.

The presence of multiple families does **not** automatically create a new canonical family.

If no special fusion rule is defined, Astra resolves the event as a lawful **multi-family harm event** without inventing emergent compound behavior.

Emergent, fused, catalytic, or compound interactions beyond ordinary multi-family classification are reserved for `batchA_09b_damage_fusion_and_compound_interactions.md` unless explicitly defined source-locally.

---

## 4. Damage Family vs Delivery Form vs Interaction State

### 4.1 Damage family
A **damage family** is the doctrinal category of harm being inflicted.

It answers:
- what kind of harm this is,
- what response states may apply to it,
- and how donor labels should be normalized.

A damage family is not the same thing as the visual fiction of the attack.

### 4.2 Delivery form
A **delivery form** is how the harm reaches or expresses upon the target.

Examples may include:
- strike,
- beam,
- burst,
- field,
- cloud,
- corrosion,
- contagion,
- pulse,
- wave,
- impact,
- bleed-through,
- aura,
- trace,
- or similar source-local means.

Delivery form may affect targeting, persistence, exposure, or conditions, but it is not itself the damage family.

### 4.3 Interaction state
An **interaction state** is the response relationship between a target and a damage family.

It answers:
- what happens when this family reaches this target,
- whether the target reduces, ignores, amplifies, converts, absorbs, restores, or otherwise modifies the incoming harm,
- and whether that response is static, conditional, temporary, granted, or source-limited.

### 4.4 Separation rule
A source may describe all three layers together, but Astra must classify them separately.

Example pattern:
- family = energetic,
- delivery form = beam,
- interaction state = absorbed by shields but resisted poorly by living tissue.

That pattern is lawful.
The three layers remain distinct.

---

## 5. Core Family Architecture

Astra uses a stable doctrine-level family architecture broad enough to absorb multiple donor traditions without hard-coding one donor's exact list.

### 5.1 Core family classes
At doctrine level, Astra recognizes the following broad family classes as the primary normalization targets:
- **physical**,
- **elemental**,
- **energetic**,
- **psychic**,
- **spiritual**,
- **biological**,
- **technological**,
- **environmental**,
- and **exotic**.

These are doctrinal family classes, not a promise that every donor will expose them under those exact names.

### 5.2 Family subclasses and aliases
Astra may later recognize stable subclasses, family aliases, or canonical branch terms within a doctrine family class.

However, donor labels do **not** automatically become new Astra families merely because they are vivid, common, or dramatically overexcited.

### 5.3 Untyped, structural, and provisional harm
Astra recognizes that some donors use harm that is:
- untyped,
- generic,
- structural,
- system-only,
- or otherwise not cleanly classifiable into an existing family at first pass.

Such harm may be represented as:
- **untyped harm**,
- **structural harm**,
- or **provisional donor-local harm**

until later doctrine or source-local mapping resolves its correct place.

Untyped or structural harm is lawful doctrine. It is not a failure case.

### 5.4 Donor-local provisional families
When a donor presents a harm label whose doctrinal role is still unclear, Astra may quarantine it as a provisional donor-local family during conversion rather than polluting the core prematurely.

---

## 6. Interaction States

### 6.1 Core interaction states
Astra supports at least the following family-response states:
- **normal**,
- **resistant**,
- **vulnerable**,
- **immune**,
- **absorbing**,
- **restorative**,
- **reduced**,
- **amplified**,
- **converted**,
- **bypassing**, 
- **conditional**,
- **suppressed**,
- and **source-limited**.

A source need not use all of these, but Astra must be able to represent them.

### 6.2 Resistance
**Resistance** reduces incoming harm from a specified family according to the relevant mitigation rule.

Resistance may be:
- proportional,
- flat,
- conditional,
- granted,
- temporary,
- target-class-specific,
- or source-limited.

### 6.3 Vulnerability
**Vulnerability** amplifies or worsens incoming harm from a specified family according to the relevant amplification rule.

Vulnerability may be innate, granted, temporary, conditional, or source-produced.

### 6.4 Immunity
**Immunity** prevents a specified family interaction from functioning in the ordinary way against the target.

Immunity may be full, partial, conditional, temporary, or interaction-limited.

### 6.5 Absorption and restoration
A target may respond to a family by:
- absorbing the incoming harm into another defense or carrier,
- converting it into usable energy,
- or being restored by it rather than harmed.

Astra treats typed restoration and typed absorption as lawful interaction states.

### 6.6 Conversion
A target or system may convert one family interaction into:
- a different family,
- a different target layer,
- a different resource change,
- or a different response mode.

### 6.7 Bypass
A family or source may bypass a defense layer, mitigation stage, or target class under defined conditions.

Bypass is an interaction-state rule, not a damage family by itself.

---

## 7. Flat vs Proportional Mitigation

### 7.1 Proportional mitigation
Astra allows family interactions that modify incoming harm by proportion, fraction, multiplier, or equivalent scale-based methods.

### 7.2 Flat mitigation
Astra also allows family interactions that reduce, ignore, or alter incoming harm by flat values or threshold subtraction.

### 7.3 Layering rule
Flat and proportional mitigation are not automatically the same operation and should not be conflated.

A source or subsystem may apply one, the other, both, or neither depending on defined doctrine.

### 7.4 Defense distinction
Flat reduction provided by armor, shielding, guard, DR, or barrier systems remains distinct from the doctrinal meaning of the damage family itself, even when the two interact.

---

## 8. Conditional, State-Based, and Source-Based Interaction

### 8.1 Conditional interaction
A family response may depend on:
- target state,
- scene state,
- recent attack history,
- active stance or mode,
- environmental context,
- source class,
- target class,
- or similar qualifying conditions.

### 8.2 State-based interaction
A target may gain, lose, or alter its family interaction because of:
- a condition,
- a mode,
- a transformation,
- a shield phase,
- an attunement,
- a curse,
- a temporary boon,
- or another state package.

### 8.3 Source-based interaction
The same family may interact differently depending on:
- who or what produced it,
- whether the source is mundane, magical, technological, biological, environmental, or donor-local,
- whether the event came from an item, zone, actor, structure, or scene,
- or whether the source carries special riders.

### 8.4 Granted and removable interaction states
Resistance, vulnerability, immunity, or related response states may be:
- innate,
- granted,
- refreshed,
- suppressed,
- removed,
- overwritten,
- or temporarily imposed.

This includes effects that make a target newly vulnerable, newly resistant, or newly immune to a family.

---

## 9. Multi-Family and Composite Harm

### 9.1 Multi-family harm events
A single harm event may lawfully carry one or more damage families.

Astra must not force every source into a single-family fiction when the donor clearly carries more than one family.

### 9.2 Default doctrine behavior
If a source deals multi-family harm and no explicit fusion rule exists, resolve it as a lawful multi-family harm event without inventing emergent compound behavior.

### 9.3 Composite harm and source-local riders
A donor source may pair multi-family harm with:
- family-specific riders,
- source-local modifiers,
- condition references,
- object degradation,
- or other effects.

Those riders do not automatically become doctrine-level fusion law.

### 9.4 Reserved depth for 09b
Questions such as:
- emergent catalytic behavior,
- order-sensitive resolution,
- compound persistence,
- fused named families,
- environment-sensitive family reactions,
- and higher-order multi-family consequence law

are reserved for `batchA_09b_damage_fusion_and_compound_interactions.md` unless the source defines them locally.

---

## 10. Harm to Actors, Items, Zones, Scenes, and Structures

### 10.1 Harm subjects are diverse
Family-tagged harm may target or affect:
- actors,
- corpses,
- spirits,
- constructs,
- weapons,
- armor,
- relics,
- tools,
- vehicles,
- drones,
- barriers,
- doors,
- terminals,
- zones,
- landmarks,
- scenes,
- structures,
- and other lawful carriers.

### 10.2 Item, equipment, and platform harm
Astra explicitly allows family-tagged harm to produce:
- item degradation,
- corrosion,
- disruption,
- reduced performance,
- repair-needed states,
- or platform-specific harm interactions.

### 10.3 Repair and restoration target classes
Family-tagged harm may require different response logic depending on what was harmed.

Examples include:
- healing for living actors,
- sanctification or restoration for spiritual carriers,
- repair for equipment or vehicles,
- reinforcement for structures,
- cleansing for contaminated zones,
- or other target-class-appropriate recovery logic.

### 10.4 Environmental and scene harm
Astra allows family-tagged harm to arise from:
- attacks,
- abilities,
- hazards,
- terrain,
- aura effects,
- scene states,
- regions,
- structures,
- and other non-weapon carriers.

---

## 11. Family-Tagged Non-Damage Interactions

### 11.1 Not all family-tagged harm is direct damage
A family-tagged interaction may be meaningfully harmful even when it does not immediately reduce vitality.

### 11.2 Lawful examples of family-tagged harmful interaction
This category may include:
- corrosion,
- contamination,
- radiation-like exposure,
- shield disruption,
- phased integrity loss,
- soul burn,
- signal corruption,
- suppression,
- disruption of attunement,
- or similar harmful interactions.

### 11.3 Boundary rule
When a family-tagged interaction primarily creates a non-damage state, track, or effect, `08` still owns the architecture of that state.

This file only governs the harm-family classification and interaction law attached to it.

---

## 12. Donor Mapping Rules

### 12.1 Normalize before promotion
When a donor presents a harm label, Astra must first determine whether it is:
- a core doctrine family match,
- a branch or subclass candidate,
- a source-local alias,
- a provisional donor-local family,
- untyped harm,
- structural harm,
- or not truly a damage family at all.

### 12.2 Family aliases do not become canon automatically
Donor labels such as:
- holy,
- radiant,
- divine,
- necrotic,
- void,
- entropy,
- acid,
- corrosion,
- sonic,
- force,
- plasma,
- bioelectric,
- warp,
- hellfire,
- psychic,
- or similar terms

must be classified by doctrine job before they are admitted to Astra core vocabulary.

### 12.3 Map, supplement, or quarantine
When donor harm language appears, Astra should choose one of three actions:
- **map** it into an existing doctrine family,
- **supplement** the doctrine with a lawful subclass or controlled extension if truly needed,
- or **quarantine** it as donor-local until further doctrine decides.

### 12.4 Do not invent emergent behavior by excitement
If the donor source does not define fused or catalytic family behavior, Astra must not hallucinate it merely because two vivid labels are present in the same event.

### 12.5 Interaction mapping discipline
When mapping donor response states, Astra should classify whether the donor is expressing:
- family resistance,
- vulnerability,
- immunity,
- absorption,
- restoration,
- conversion,
- bypass,
- source-specific mitigation,
- state-sensitive response,
- or a defense-layer rule that belongs elsewhere.

---

## 13. Explicit Exclusions and Downstream Ownership

### 13.1 Ability schema belongs elsewhere
This file may reference that an ability delivers family-tagged harm, but `batchA_07_ability_object_model.md` owns the shape of the ability object.

### 13.2 Cost, recharge, and backlash belong elsewhere
This file may reference that family-tagged harm interacts with resource economy or hazardous use, but `batchA_07b_resource_cost_recharge_and_backlash_architecture.md` owns those rules.

### 13.3 Condition meaning belongs elsewhere
This file may reference that family-tagged harm creates or interacts with conditions, but `batchA_08_status_condition_and_effect_architecture.md` owns condition and effect meaning.

### 13.4 Compound and fused family doctrine is deferred
This file acknowledges that multi-family harm exists and that compound behavior may exist.

However, full doctrine for:
- fusion,
- catalysis,
- compound persistence,
- emergent compound states,
- order-sensitive multi-family resolution,
- and named fused families

is reserved for `batchA_09b_damage_fusion_and_compound_interactions.md`.

### 13.5 Progression and package law belong elsewhere
This file may reference that a target or source gains interaction states through progression, lineage, path, gear, or other systems, but those systems do not belong here.

---

## 14. Reserved Note for batchA_09b_damage_fusion_and_compound_interactions.md

The following topics are intentionally reserved for later doctrine rather than being overbuilt here:
- emergent multi-family reactions,
- catalytic behavior between families,
- environment-sensitive fusion outcomes,
- persistent compound states,
- secondary and tertiary family interaction effects,
- and whether a compound event remains multi-tagged or becomes a distinct named fused construct.

`batchA_09` therefore establishes the legality and classification of multi-family harm while deferring deeper fusion law to `batchA_09b`.
