# batchB_03_equipment_item_and_gear_object_model.md

## Purpose

This file defines Astra Ascension’s **universal item grammar**.

It governs what counts as an item, equipment object, gear object, consumable, material, container, augment, deployable, relic, bonded object, and other item-bearing construct in Astra-native doctrine. It also defines the stable schema fields, relation fields, state fields, and translation rules required to convert donor inventories, gear ecologies, and item-linked mechanics without flattening materially different constructs into one vague loot bucket.

This file is not a loot catalog, not a wealth chapter, not a crafting chapter, and not a combat equipment appendix in disguised form. It is the **item-schema doctrine file** for Batch B.

Its job is to provide a conversion-stable object model that can absorb donor item pressure from fantasy, sci-fi, hybrid, cultivation, relic-based, biotech, cyberware, alchemical, survival, and logistics-heavy systems while preserving meaningful distinctions between item families, bearer relations, activation modes, capacity models, and exceptional-item behaviors.

## Authority and dependency position

This file is authoritative for:
- item ontology,
- item profile versus item instance doctrine,
- item class and subfamily architecture,
- holder and relation grammar,
- equip/carry/stow/install/deploy/bond state doctrine,
- capacity and containment field architecture,
- universal item profile fields,
- universal item instance fields,
- identification and knowledge-state fields,
- durability and integrity fields,
- item agency and progression flags,
- lawful incomplete item mapping states,
- item-related subsystem handoff boundaries.

This file depends on Batch A doctrine, especially:
- `batchA_01_lexicon_and_reserved_terms.md`,
- `batchA_03_resolution_framework.md`,
- `batchA_04_attribute_and_derived_stat_architecture.md`,
- `batchA_05_competency_and_skill_translation_architecture.md`,
- `batchA_06_access_tags_permissions_and_proficiency_gates.md`,
- `batchA_07_ability_object_model.md`,
- `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`,
- `batchA_08_status_condition_and_effect_architecture.md`,
- `batchA_09_damage_family_and_resistance_taxonomy.md`,
- `batchA_09b_damage_fusion_and_compound_interactions.md`,
- `batchA_14_starting_loadout_and_kit_framework.md`,
- `batchA_15_conversion_invariants.md`.

This file must not silently re-own any of those systems.

## Ownership boundary

This file owns the **ontology and schema of items**.

This file must define:
- what an item is in Astra terms,
- what counts as gear, equipment, consumable, material, augment, deployable, container, relic, bonded object, and item-bearing system,
- how item classes differ,
- what universal fields item profiles and item instances may carry,
- how items relate to owners, bearers, holders, containers, platforms, and environments,
- how equip, carry, stow, install, deploy, consume, mount, embed, and bond states are expressed,
- how capacity and containment are represented without hardcoding one donor inventory law,
- how items reference attached effects, resources, permissions, and abilities without re-owning them,
- how durability, integrity, identification, agency, growth, and transformation states are represented,
- how incomplete or uncertain donor item mappings are lawfully classified.

This file must not define or re-explain:
- starting character gear package procedure,
- value, price, trade, requisition, sellback, or currency economy,
- crafting, salvage, modification, repair procedure, installation procedure, or upgrade procedure,
- general access law, proficiency law, or permission law,
- generic activation resolution or ability construction,
- recharge, fuel, heat, ammo-economy, charge recovery, or backlash law,
- damage-family meanings,
- status-condition meanings,
- health-state or recovery meanings,
- encounter timing for item use,
- companion, drone, summon, or autonomous entity doctrine,
- platform operation for mounts, vehicles, mechs, ships, capitals, or base infrastructure.

If this file begins absorbing economy doctrine, crafting doctrine, platform doctrine, or ability doctrine, that is scope drift and must be corrected by redirection.

## Core doctrine terms

### Item
An **item** is a discrete object, object-bundle, or installable object-bearing construct that can be possessed, manipulated, equipped, carried, stored, consumed, installed, deployed, traded, mounted, bonded, or otherwise treated as a persistent game object.

An item is a thing with durable identity in the rules model, even when its state changes.

### Gear
**Gear** is the broad family of practical items used to support action, survival, travel, defense, manipulation, logistics, operation, maintenance, or access.

Gear may be mundane, advanced, ritual, exotic, biological, arcane, hybrid, or donor-specific in expression.

### Equipment
**Equipment** is gear that occupies, interfaces with, or attaches to a bearer, host, slot, profile, or operational mount.

Equipment is a relational category, not merely a flavor label.

### Consumable
A **consumable** is an item whose use depletes, transforms, expends, or exhausts it, whether in one use or over multiple uses.

### Material / component
A **material** or **component** is an item primarily valued as an ingredient, input, reagent, structural component, salvage output, crafting substrate, or exchange-relevant good rather than as directly wielded or worn equipment.

### Container
A **container** is an item whose primary function is to hold, group, preserve, transport, shield, or spatially organize other items.

### Deployable
A **deployable** is an item that changes relation state by being placed, activated, armed, seeded, unfolded, anchored, or otherwise projected into the environment.

### Augment
An **augment** is an item that is installed into or onto a host body, chassis, shell, frame, system, or platform such that it changes bearer or host capabilities through persistent attachment.

### Exceptional item
An **exceptional item** is any item that requires extended schema beyond ordinary gear due to rarity, bond structure, agency, hidden function, transformational behavior, progression relevance, extraordinary access constraints, or special metaphysical/technological significance.

### Item-bearing system
An **item-bearing system** is an item that contains internal substructure significant enough to hold nested item relations, modules, states, loads, or configurable internal components while still remaining below the threshold where a separate platform doctrine is required.

### Item profile
An **item profile** is the canonical definition of what a class of item is.

It defines stable identity-level facts such as class, traits, bearer requirements, activation mode, capacity type, effect references, and default durability pattern.

### Item instance
An **item instance** is a specific copy of an item profile in a specific current state.

It defines stateful facts such as damage, wear, bond status, charges remaining, installed modules, identification state, location, owner, container relationship, current load, and modifications.

### Owner
The **owner** is the actor, institution, faction, site, or other recognized authority that possesses the claim relationship to an item.

### Bearer
The **bearer** is the actor currently wearing, wielding, carrying on-body, or otherwise directly using an item in a meaningful active relation.

### Holder
The **holder** is the immediate relation point currently containing or supporting the item, which may be a bearer, container, rack, environment, mount, platform, or system slot.

### Container relation
A **container relation** is the direct relation by which an item is stored inside another item or item-bearing system.

### Mount / platform relation
A **mount** or **platform relation** is the relation by which an item is installed on, attached to, fed into, or operationally linked with a host structure, vehicle, mech, ship, capital subsystem, drone rack, or similar larger system.

### Environment relation
An **environment relation** describes an item existing as placed, dropped, anchored, hidden, embedded, planted, or otherwise situated in the world rather than held directly by a bearer.

## Design principle: item ecology must survive conversion

Astra must preserve donor **item ecology**, not merely donor item names.

Different donor systems distinguish different things for meaningful reasons. Some distinguish worn gear from carried gear. Some distinguish consumables from charges. Some distinguish materials from treasure. Some distinguish relics from mundane tools. Some distinguish cyberware from equipment. Some distinguish bonded items from ordinary market goods. Some distinguish an installable module from a hand-held item.

Astra conversion must not erase those distinctions by flattening unlike objects into a generic “loot” bucket unless the donor genuinely treats them as equivalent.

## Design principle: object first, surrounding procedure second

An item object is not the same thing as:
- the effect it can produce,
- the action timing used to activate it,
- the economy surrounding it,
- the repair procedure surrounding it,
- the crafting procedure surrounding it,
- the hazard source it may neutralize,
- the survivability consequence it may restore,
- the platform it may plug into.

This file therefore defines the item as object and schema. Downstream files define the procedures and consequences attached to that object.

## Translation scope: multiple donor item ecologies

This file must be broad enough to absorb at minimum:
- ordinary fantasy equipment ecologies,
- survival/logistics-heavy gear ecologies,
- relic and artifact ecologies,
- alchemical and consumable ecologies,
- ammunition and payload ecologies,
- sci-fi module and augment ecologies,
- cyberware / biotech / implant ecologies,
- cultivation treasure and resource ecologies,
- procedural treasure/material ecologies,
- strange or semi-sentient item ecologies,
- donor systems where gear is low-importance,
- donor systems where gear is core progression infrastructure.

The file therefore must describe a grammar, not merely a fantasy equipment chapter.

## Item ontology doctrine

An item exists in Astra doctrine when all of the following are materially true:
- it has persistent identity across more than an instant,
- it can stand in a possession, holder, bearer, container, install, or environment relation,
- it can meaningfully change state or position,
- its presence or absence can alter capabilities, options, access, logistics, or outcomes.

A construct should generally **not** be treated as an item in this file when it is better represented as:
- an active ability,
- a status or effect,
- a service,
- a companion or summon entity,
- a vehicle/platform-scale system,
- a base/infrastructure element,
- a faction permission,
- a narrative tag with no durable object identity.

### Doctrine test: item versus non-item
A construct should be modeled here as an item when the object itself matters.

A construct should be modeled elsewhere when the object is merely a thin carrier for another doctrine layer and item identity is not important.

Examples of likely item treatment:
- weapon,
- armor,
- medkit,
- potion,
- toolkit,
- container,
- ammo pack,
- relic,
- implant,
- portable scanner,
- encoded key,
- teleport token,
- power cell,
- crafting reagent,
- deployable beacon.

Examples of likely non-item treatment:
- learned combat technique,
- spell known intrinsically,
- faction standing,
- summoned entity,
- owned vehicle as platform,
- social privilege,
- room in a settlement,
- ongoing blessing as a condition-like effect without persistent object identity.

## Item profile versus item instance doctrine

This split is mandatory.

Astra must distinguish between:
- the **item profile**, which defines what kind of item something is,
- and the **item instance**, which defines the current state of a particular copy.

Without this split, conversion cannot cleanly support:
- damaged versus pristine copies,
- identified versus unidentified copies,
- bonded versus unbonded copies,
- loaded versus empty copies,
- partially expended consumables,
- modified variants,
- inherited relics,
- unstable or corrupted copies,
- donor materials where a class entry exists but current copy state matters.

### Item profile doctrine
An item profile must define stable and reusable identity-level facts.

Typical profile-level fields include:
- profile identifier,
- canonical item name,
- item class,
- item subfamily,
- ordinary / exceptional / item-bearing-system flag,
- bearer requirement fields,
- host compatibility fields,
- default holder relation type,
- slot or relation affordances,
- capacity model,
- trait list,
- activation mode,
- effect reference hooks,
- default durability model,
- default identification model,
- progression / growth flags,
- translation notes,
- mapping certainty state.

### Item instance doctrine
An item instance must define current state facts for a specific copy.

Typical instance-level fields include:
- instance identifier,
- linked profile identifier,
- owner relation,
- bearer relation,
- immediate holder relation,
- location / environment relation,
- current integrity or damage state,
- current identification state,
- current bond / attunement state,
- current load, ammo, charge, fuel, or contents state,
- current installed modules or modifications,
- current contamination/corruption status if relevant,
- current transformation state,
- current lock/key/authorization state if relevant,
- current scarcity or legal-tag state if relevant,
- current active/passive suppression state if relevant.

### Doctrine rule
Where donor text describes what the item *is*, translate to a profile.

Where donor text describes the condition of a specific copy, translate to an instance.

If donor material ambiguously mixes both, Astra conversion must separate the two rather than preserve the ambiguity unchanged.

## Item classes and subfamilies

This file defines item classes as translation-stable ontology buckets, not as donor chapter titles.

### 1. Equipable gear
Items designed to be worn, wielded, carried on-body, held ready, or otherwise placed into an active bearer relation.

Examples include:
- weapons,
- armor,
- shields,
- belts,
- rings,
- pendants,
- visors,
- packs if treated as equipped containers,
- harnesses,
- focus devices,
- combat rigs,
- sensor rigs.

### 2. Carried utility gear
Items primarily used from carried/stowed state rather than continuously worn.

Examples include:
- ropes,
- lamps,
- climbing gear,
- rations,
- lockkits,
- medkits,
- scanners,
- field tools,
- maps,
- keys,
- token devices,
- ritual components held in reserve.

### 3. Consumables
Items that are expended, transformed, or depleted through use.

Examples include:
- potions,
- injectors,
- grenades,
- scroll-like one-use objects,
- food rations,
- chemical cartridges,
- stims,
- batteries if single-use,
- sacrificial offerings,
- temporary one-use relic fragments.

### 4. Ammunition and expendable payloads
Items whose primary purpose is to feed, charge, fuel, seed, or empower another item or host process.

Examples include:
- arrows,
- bolts,
- magazines,
- shells,
- charges,
- fuel rods,
- essence cartridges,
- catalyst vials,
- drone payloads,
- ritual reagents consumed per use.

### 5. Tools and kits
Items or bundled items whose primary purpose is enabling a competency, procedure, or operation rather than directly inflicting or preventing harm.

Examples include:
- surgical kits,
- repair kits,
- artisan tools,
- hacking kits,
- survey kits,
- laboratory sets,
- camping kits,
- breach kits.

### 6. Materials and components
Items primarily significant as input goods, salvage, ingredients, structural pieces, trade goods, or conversion substrates.

Examples include:
- ore,
- herbs,
- monster parts,
- crystals,
- cores,
- reagents,
- spare components,
- relic shards,
- treated alloys,
- biotech tissue stock,
- spirit condensates.

### 7. Valuables and exchange goods
Items whose primary significance lies in value-bearing, tokenized, ceremonial, scarcity-marked, or exchange-related function.

This file may classify them, but does not own their economy logic.

### 8. Containers and storage objects
Items whose primary role is holding, preserving, sorting, or spatially organizing other items.

Examples include:
- pouches,
- backpacks,
- cases,
- satchels,
- lockboxes,
- spatial bags,
- reagent racks,
- vault capsules.

### 9. Augments and installables
Items designed to be installed into or onto a host body, chassis, shell, weapon, suit, drone, or other compatible system.

Examples include:
- implants,
- cyberware,
- biotech grafts,
- weapon mods,
- armor modules,
- sensor packages,
- socketable cores,
- shipboard upgrade modules below platform-doctrine threshold.

### 10. Deployables
Items designed to enter an environment relation and produce persistent local effect, threat, support, or access.

Examples include:
- mines,
- traps-as-items,
- field generators,
- beacons,
- camp kits,
- shield emitters,
- surveillance bugs,
- anchored ritual objects.

### 11. Exceptional items
Items with extended schema due to rarity, agency, progression, bond state, hidden function, or extraordinary ontological weight.

Examples include:
- relics,
- wondrous items,
- living weapons,
- named artifacts,
- lineage-bound heirlooms,
- fate-linked devices,
- metamorphic treasures.

### 12. Item-bearing systems
Items that remain item-scale but contain meaningful internal loadout, module, or nested-relation structure.

Examples include:
- modular med-stations,
- deployable workbenches,
- complex portable labs,
- powered suits treated as items rather than platforms,
- weapon systems with swappable integrated payloads,
- storage matrices.

## Ordinary items, exceptional items, and item-bearing systems

This three-way separation is mandatory.

### Ordinary items
Ordinary items are conventional objects whose schema needs no extended agency or progression model.

They may still be rare, expensive, or powerful.

### Exceptional items
Exceptional items require additional schema because they may:
- hide functions,
- demand attunement or bond state,
- evolve,
- resist ordinary use,
- carry personality,
- transform,
- alter bearer identity,
- serve as progression anchors,
- persist as named singular objects.

### Item-bearing systems
Item-bearing systems are still items, but they carry meaningful internal substructure such as slots, module racks, nested components, or internal storage states.

This category exists to prevent premature collapse into full platform doctrine while still allowing complex portable systems.

## Universal item field architecture

The following field families must be supported by Astra item doctrine. Not every item requires every field, but the schema must have room for them.

### Identity fields
- profile identifier,
- instance identifier,
- canonical name,
- alternate/alias name if relevant,
- item class,
- item subfamily,
- ordinary / exceptional / item-bearing-system designation,
- source translation notes,
- mapping certainty state.

### Relation fields
- owner,
- bearer,
- holder,
- container parent,
- mount/platform parent,
- environment location relation,
- host relation for installed items,
- linked item dependencies.

### Access and compatibility fields
- bearer requirement tags,
- access restrictions,
- compatibility flags,
- host requirements,
- slot compatibility,
- authorization flags,
- species/body/chassis/lineage/path restrictions where relevant.

The meaning of these restrictions is not owned by this file. This file only permits items to carry them.

### Capacity and containment fields
- weight or mass expression,
- bulk expression,
- slot footprint,
- bundle/stack rules,
- quantity unit,
- contained volume/capacity,
- item count capacity,
- preservation or stasis flags,
- containment prohibitions,
- nesting permissions.

### State fields
- equipped state,
- carried state,
- stowed state,
- installed state,
- deployed state,
- consumed/depleted state,
- bonded/attuned state,
- hidden/revealed state,
- locked/unlocked state,
- loaded/unloaded state,
- active/inactive state,
- broken/degraded state,
- corrupted/contaminated state,
- transformed state.

### Mechanical hook fields
- trait list,
- activation mode,
- action-interface reference,
- effect reference hooks,
- granted ability references,
- resource-carrier hooks,
- ammo/fuel/charge carrier hooks,
- passive modifier hooks,
- durability model,
- maintenance tags,
- progression flags,
- identification model.

### Knowledge fields
- known appearance,
- known function,
- identified capabilities,
- misidentification possibility,
- hidden functions,
- bearer familiarity,
- handling instructions known/unknown.

### Exceptional-item fields
- attunement/bond state,
- agency/sentience flag,
- disposition or relationship marker if needed,
- growth vector,
- hunger or demand vector,
- transformation state,
- lineage/faction/path resonance,
- singularity flag,
- destiny/progression relevance.

## Holder relation grammar

This file must define holder relations more sharply than “equipped or carried.”

### Owner relation
Who possesses formal claim or authority over the item.

This may differ from current bearer.

### Bearer relation
Who is currently wearing, wielding, or actively using the item in a primary operational sense.

### Holder relation
What immediately supports, contains, or presents the item.

Examples:
- a bearer’s main hand,
- a belt slot,
- a backpack,
- a weapon rack,
- a workbench,
- a shrine pedestal,
- a shipboard mount,
- the ground,
- a hidden compartment.

### Container relation
Which container currently encloses the item, if any.

### Host relation
Which body, chassis, shell, weapon, armor, or system hosts the item when installed or embedded.

### Mount/platform relation
Which mount or larger system the item is attached to.

### Environment relation
Whether the item is placed, dropped, buried, planted, hidden, anchored, floating, embedded, or otherwise situated in the environment.

### Doctrine rule
An item may have multiple relations at once, but they are not interchangeable.

For example, an item may be:
- owned by a faction,
- borne by a field operative,
- held in an off-hand slot,
- loaded with a charge,
- and simultaneously bonded to a previous owner.

Astra conversion must preserve these layered relations when donor material meaningfully distinguishes them.

## Holder-state doctrine

Items may occupy one or more recognized relation states.

Core holder states include:
- **equipped**,
- **wielded**,
- **worn**,
- **carried**,
- **stowed**,
- **stored**,
- **installed**,
- **embedded**,
- **mounted**,
- **deployed**,
- **consumed/exhausted**,
- **bonded/attuned**,
- **unclaimed/environmental**.

These are doctrinal states, not fixed donor action timings.

### Equipped / worn / wielded
The item is in an active bearer relation and occupies or interfaces with a bearer slot, attachment point, or operational hand state.

### Carried
The item is presently on the bearer’s person or immediate load but not necessarily in ready-use relation.

### Stowed
The item is presently contained, packed, holstered, folded away, or otherwise not in immediate ready-use relation.

### Stored
The item is kept in a non-personal storage relation such as a locker, vault, depot, shrine, repository, or field cache.

### Installed / embedded
The item has been attached to or integrated into a host such that removal or change of state is materially different from ordinary carrying.

### Mounted
The item is attached to a mount point or larger item/system/platform relation.

### Deployed
The item has left bearer/container state and entered an environmental or anchored operational state.

### Consumed / exhausted
The item has been spent, transformed, emptied, discharged, or otherwise made unavailable except by replenishment, restoration, or reconstruction.

### Bonded / attuned
The item has an active relational link to a bearer, owner, lineage, path, soul-pattern, authorization key, or other special compatibility state.

## Capacity and containment doctrine

Astra must support multiple donor inventory expressions without declaring one universal carrying law.

### Capacity expression must support:
- exact weight systems,
- bulk systems,
- slot systems,
- range-band or load-band systems,
- abstract heroic carry systems,
- bundle/stack rules,
- nested container rules,
- preservation/stasis rules,
- environmental transport rules,
- hybrid systems using more than one model.

### Doctrine rule
This file defines the fields needed to express capacity. It does not declare which one universal capacity model all Astra conversions must use.

### Capacity field families
- weight/mass,
- bulk,
- slot footprint,
- carry band,
- bundle size,
- stack limit,
- quantity abstraction,
- container volume/capacity,
- special containment traits,
- nesting prohibition flags,
- preservation flags,
- retrieval difficulty flags.

### Container doctrine
Containers are items with their own profile and instance states.

A container may have:
- capacity fields,
- access fields,
- preservation fields,
- security fields,
- quick-draw or retrieval flags,
- segmentation or compartmentalization,
- compatibility restrictions,
- anti-nesting or special nesting rules,
- environment protection traits.

A container does not erase the identity of contained items. Containment is a relation, not a merger.

## Buffer, load, payload, and contents doctrine

This file must sharply distinguish:
- the item object,
- the resources or payload it carries,
- the contents it contains,
- and the load state of a particular instance.

### Item versus payload
A bow is not the same thing as its arrows.
A firearm is not the same thing as its magazine.
A battery-backed tool is not the same thing as the energy reserve it carries.
A medkit is not the same thing as its remaining doses.

### Item versus contents
A backpack is not identical to the items inside it.
A stasis case is not identical to the preserved object held within.

### Doctrine rule
Items must be able to carry, reference, or contain resources and contents without losing their own object identity.

## Item activation and use semantics

This file defines item activation as an item-schema concern, not a full use-procedure concern.

An item profile may specify one or more of the following activation modes:
- passive,
- bearer-triggered,
- manually activated,
- consumptive,
- charge-spending,
- ammo-fed,
- reaction-triggered,
- sustained,
- install-based,
- deployed,
- bonded/unlocked,
- environment-conditional,
- one-use,
- multi-stage.

### Passive items
Items that modify state, grant tags, or alter bearer capability without active triggering each time.

### Activated items
Items that require a deliberate use step.

### Triggered items
Items that respond to conditions, thresholds, impacts, reactions, or environmental states.

### Sustained items
Items that remain active across time and may require upkeep, concentration analogue, fuel, or maintained relation.

### Consumptive items
Items that transform or deplete through use.

### Installed or bonded items
Items whose capabilities depend on install relation, attunement, compatibility, or unlocked state.

### Doctrine rule
Activation mode belongs to the item profile. Activation timing and procedural resolution belong to downstream encounter, downtime, or subsystem doctrine.

## Effect attachment doctrine

An item object is not the same thing as the effect it can produce.

This distinction is mandatory.

An item may:
- grant an ability,
- reference an ability,
- modify a derived stat,
- alter access permissions,
- carry a resource,
- apply a status,
- deliver damage,
- restore survivability,
- enable movement modes,
- alter sensor profile,
- modify capacity,
- change environmental interaction.

But B03 does not define the full meaning of those effects.

### Item mechanical hooks may include:
- granted ability references,
- passive modifier hooks,
- condition application hooks,
- damage-profile hooks,
- survivability-restoration hooks,
- mobility hooks,
- detection/sensing hooks,
- compatibility and keying hooks,
- deployment outcome hooks,
- progression unlock hooks.

### Doctrine rule
Where a donor item carries an effect, B03 must preserve the attachment relation while handing off full effect meaning to the authoritative doctrine file.

## Identification and knowledge-state doctrine

Identification and knowledge state are formal item field families.

Astra must support at minimum the following knowledge states:
- **unknown**,
- **partially known**,
- **identified**,
- **misidentified**,
- **hidden-function**,
- **bearer-familiar**,
- **restricted knowledge**.

### Unknown
The item’s function, traits, or risks are not known.

### Partially known
Some properties are known, but not all.

### Identified
The item’s materially relevant profile functions are known to the current knowledgeable actor or doctrine record.

### Misidentified
A false understanding exists and is presently treated as true by some actor.

### Hidden-function
The item has dormant, concealed, masked, sealed, or undisclosed behaviors not yet available to ordinary identification.

### Bearer-familiar
A specific bearer or institution knows how to use or interpret the item even if the item remains obscure to others.

### Restricted knowledge
The item’s function is known only to authorized actors, bonded holders, institutional archives, or keyed systems.

### Doctrine rule
This file supports knowledge-state representation. It does not universalize any donor’s identification shortcut, ritual, scan mechanic, or lore gate as Astra law.

## Durability and integrity doctrine

Durability is a first-class item schema concern.

Astra item doctrine must support items that can:
- remain effectively permanent,
- degrade through use,
- lose integrity through impact,
- become impaired without full destruction,
- be corroded, jammed, cracked, depleted, blunted, broken, or destabilized,
- require maintenance,
- become unusable until repaired,
- suffer partial functionality loss.

### Durability-related fields may include:
- integrity tier or track,
- wear state,
- breakage threshold,
- repairability flag,
- maintenance cadence,
- corrosion susceptibility,
- overload susceptibility,
- catastrophic failure risk,
- degradation stage,
- salvageable state.

### Doctrine rule
This file permits durability and integrity to exist as item properties. It does not own the repair procedure, maintenance action timing, or salvage workflow.

## Ordinary survivability protection versus item durability

This file must distinguish between:
- the item protecting a bearer,
- the item itself being damaged,
- the item carrying restoration payload,
- the item becoming unusable even when the bearer survives.

This distinction prevents item durability from collapsing into health-state doctrine.

## Item agency and progression flags

Some items are not inert.

Astra item doctrine must permit explicit schema support for items that:
- possess agency,
- possess sentience or quasi-sentience,
- cultivate or evolve,
- transform with use,
- demand feeding, resonance, or sacrifice,
- bond selectively,
- alter bearer identity,
- unlock staged functionality,
- carry singular named continuity across generations.

### Relevant field families include:
- attunement/bond state,
- agency flag,
- sentience flag,
- disposition marker if required,
- resonance requirements,
- growth vector,
- hunger/demand vector,
- transformation state,
- stage/unlock markers,
- bearer imprint state,
- legacy chain,
- progression relevance.

### Doctrine rule
This file provides the schema room for such items. It does not assume all Astra exceptional items are alive, magical, spiritual, technological, or donor-metaphysically identical.

## Bond, attunement, authorization, and keyed access

These related concepts must be represented without being collapsed together.

### Bond
A personal or structural relational link between item and bearer or owner.

### Attunement
A specialized compatibility state requiring synchronization, resonance, calibration, or other deep alignment.

### Authorization
A permission state tied to credentials, rank, institutional clearance, encoded identity, or lawful access.

### Keyed access
A narrower function-unlocking relationship tied to codes, signatures, tokens, biometrics, or similar gating constructs.

### Doctrine rule
B03 allows items to carry these fields. B03 does not define the full access law or authorization procedure.

## Augment and installable doctrine

Augments and installables are still items, but they require explicit host and compatibility fields.

### Required schema support includes:
- host type compatibility,
- install location,
- removal difficulty or reversibility flags,
- embedded versus surface-mounted state,
- host dependency,
- host burden or slot usage,
- persistent passive effect hooks,
- failure / incompatibility hooks,
- nested module support where relevant.

### Doctrine rule
If a construct remains a discrete installed object, it belongs here.
If it becomes a full companion/entity, separate platform, or body-state transformation that eclipses item identity, it likely belongs elsewhere.

## Deployable doctrine

Deployables require explicit environment relation and local persistence fields.

A deployable may need:
- anchor state,
- arming state,
- trigger state,
- duration or persistence tags,
- retrieval possibility,
- ownership trace,
- concealment relation,
- environment dependence,
- area-of-effect hooks,
- deactivation or dismantle hooks.

### Doctrine rule
Deployables remain items while their identity as placeable objects remains primary.
If conversion instead requires a full trap, hazard, infrastructure, or encounter object model, later doctrine may split or hand off as needed.

## Item-bearing systems doctrine

Item-bearing systems exist to prevent premature collapse between ordinary item and full platform.

An item-bearing system may have:
- internal slots,
- module sockets,
- nested items,
- internal resource carriers,
- configurable modes,
- user-interface requirements,
- maintenance or calibration state,
- bearer/host compatibility fields,
- subcomponent integrity.

### Examples of likely treatment
- portable field lab,
- powered armor treated as equipment rather than full platform,
- modular toolkit,
- integrated med-station,
- advanced rifle with swappable cores and payload assemblies,
- ritual array case with slotted implements.

### Doctrine boundary
If the object’s operational complexity primarily becomes a vehicle, mech, ship, or infrastructure system, hand off to B14 or B15.

## Translation invariants for donor item ecologies

### Invariant 1: preserve donor item ecology
Conversion must preserve materially meaningful distinctions between equipment, consumables, materials, exchange goods, relics, augments, containers, payloads, and deployables when the donor distinguishes them.

### Invariant 2: do not collapse object into effect
An item object is not identical to the effect, status, damage, healing, movement, or permission change it may produce.

### Invariant 3: do not collapse item into economy
An item is not identical to its price, sellback rule, requisition path, rarity market, or barter logic.

### Invariant 4: do not collapse item into crafting/repair procedure
An item is not identical to the process used to create, repair, modify, salvage, or install it.

### Invariant 5: preserve bearer and holder distinctions
Who owns an item, who bears it, where it is stored, and what it is mounted to are not interchangeable relationships.

### Invariant 6: preserve exceptional-item structure
Where donor material distinguishes named relics, bonded weapons, singular artifacts, living tools, or evolving treasures, Astra must preserve that exceptionality in schema.

### Invariant 7: preserve complex items as item-bearing systems when needed
Do not flatten internally modular item constructs into a single fieldless object when their internal substructure matters.

### Invariant 8: avoid false universalization
Do not import any donor’s exact slot count, encumbrance formula, identification shortcut, item-rank law, attunement cap, or repair rule as hidden Astra default unless later doctrine explicitly canonizes it.

## Threat and significance preservation rule for items

Conversion must preserve the intended **item significance** and **item pressure** of donor constructs.

This includes preserving when donor items are:
- central to survival,
- central to progression,
- central to logistics,
- central to scarcity pressure,
- central to power access,
- central to body modification,
- central to treasure motivation,
- or intentionally low-significance background objects.

Do not inflate low-significance donor gear into needless Astra complexity.
Do not flatten high-significance donor gear into generic padding.

## Lawful incomplete item mapping

For a corpus of this size, incomplete mapping is lawful and expected.

If a donor item cannot be fully resolved without inventing unsupported certainty, Astra conversion may classify the item as one of the following:

### Directly mapped
The donor item profile and its meaningful state relations map cleanly into existing Astra doctrine with minimal normalization.

### Normalized
The donor item is translated into Astra-native schema using existing field families where exact donor expression is adjusted but meaning is preserved.

### Profile-assigned
The donor item lacks complete instance detail, but enough is known to assign a stable Astra item profile.

### Placeholder-classified
The donor item’s broad class is known, but important subfields remain unresolved pending downstream doctrine or additional source material.

### Quarantined
The donor item cannot yet be converted without likely doctrinal invention, contradiction, or false certainty. It should remain flagged for later review rather than improvised carelessly.

### Doctrine rule
Lawful incompleteness is preferable to fabricated certainty.

## Conversion notes: item profile versus item catalog

This file does not create item lists.
It creates the schema required for later item conversion.

Later conversion work may produce:
- Astra-native armories,
- gear lists,
- relic catalogs,
- implant libraries,
- material tables,
- loot outputs,
- procedural treasure generators.

Those later assets must obey the schema defined here.

## Mandatory subsystem handoff map

The following handoffs are mandatory.

### Batch A handoffs
- starting kits and initial character packages -> `batchA_14_starting_loadout_and_kit_framework.md`
- bearer permissions, proficiency requirements, access tags -> `batchA_06_access_tags_permissions_and_proficiency_gates.md`
- granted abilities, activated powers, item-bestowed techniques -> `batchA_07_ability_object_model.md`
- charges, recharge, fuel, heat, backlash, resource-carrier semantics -> `batchA_07b_resource_cost_recharge_and_backlash_architecture.md`
- status-condition meanings -> `batchA_08_status_condition_and_effect_architecture.md`
- damage-family meanings and resist/vulnerability hooks -> `batchA_09_damage_family_and_resistance_taxonomy.md`
- compound damage or cross-family effects -> `batchA_09b_damage_fusion_and_compound_interactions.md`

### Batch B handoffs
- encounter timing, readying, use windows, procedural action timing -> `batchB_01_scene_conflict_action_and_encounter_procedure.md`
- survivability meaning of medical, restorative, toxic, or body-altering items -> `batchB_02_health_injury_healing_death_and_recovery_framework.md`
- value, price, requisition, trade, sellback, and exchange systems -> `batchB_04_wealth_currency_requisition_trade_and_value_framework.md`
- crafting, salvage, repair, modification, installation procedure -> `batchB_05_crafting_salvage_repair_modification_and_installation.md`
- environmental exposure or hazard-source semantics -> `batchB_07_environment_hazards_weather_regions_and_afflictions.md`
- downtime maintenance, servicing, study, calibration, and project use -> `batchB_11_downtime_rest_training_projects_and_services.md`
- institutional issue, clearance-gated access, faction service supply -> `batchB_12_factions_institutions_clearance_and_service_access.md`
- drones, companions, summons, and auxiliary entities as entities rather than items -> `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md`
- mounts, vehicles, mechs, ships, and operational platform systems -> `batchB_14_mounts_vehicles_mechs_ships_and_platform_operations.md`
- settlement-scale depots, armories, workshops, vaults, and infrastructure interfaces -> `batchB_15_settlements_bases_capitals_and_infrastructure_operations.md`
- loot inflow and post-encounter acquisition procedure -> `batchB_16_loot_rewards_salvage_and_post_encounter_inflows.md`

## Anti-drift warnings

### 1. Do not make this the wealth file
If discussion turns primarily to prices, sell ratios, barter law, market scarcity, requisition, or currency logic, hand off to B04.

### 2. Do not make this the crafting file
If discussion turns primarily to recipes, salvage outputs, repair checks, install procedure, upgrade procedure, or workshop operations, hand off to B05.

### 3. Do not make this the ability file
If discussion turns primarily to what an item power does mechanically, how it resolves, how it scales, or how it recharges, hand off to Batch A ability/resource doctrine.

### 4. Do not make this the platform file
If the object is functionally a vehicle, mech, ship, capital subsystem, or platform operations problem, hand off to B14 or B15.

### 5. Do not let donor identification rules become hidden law
Some donors make identification instant, rare, ritualized, dangerous, or impossible without special knowledge. Astra must preserve the possibility space without universalizing one donor solution.

### 6. Do not flatten every strange object into “relic”
Exceptional does not mean mystical by default. Some donor exceptional items are biotech, psionic, computational, ceremonial, dimensional, or hybrid.

## Summary doctrine statement

`batchB_03_equipment_item_and_gear_object_model.md` defines Astra Ascension’s item ontology and item schema.

It specifies:
- what an item is,
- what item classes and relation types exist,
- how item profiles differ from item instances,
- what universal fields items may carry,
- how holders, containers, hosts, and platforms relate to items,
- how capacity, containment, identification, durability, agency, and progression states are expressed,
- and where all item-linked downstream rules must hand off.

It must remain a universal object-model file.
It must not become the wealth chapter, crafting chapter, or platform chapter.
It must preserve donor item ecology without copying donor structure wholesale.
