# Astra Ascension D09 Doctrine Pack v0.1

Generated: 2026-06-02

This combined export contains the full D09 doctrine pack in file order.


---

<!-- FILE: D09-README_manifest.md -->

# D09 Object-State, Equipment, Relic, Platform, Crafting, and Source-local Object Architecture — Manifest

Version: v0.1  
Phase: Astra Ascension native design doctrine  
Status: Generated from accepted D09 DDR decisions  
Primary owner: D09

## Purpose

D09 defines Astra Ascension object-state doctrine. It covers mundane gear, weapons, armor, tools, foci, consumables, materials, catalysts, relics, artifacts, anchors, intelligent objects, implants, prosthetics, cyberware, biotech, living gear, vehicles, ships, mechs, drones, platforms, crafting, salvage, requisition, and source-local object systems.

D09 exists because Astra must absorb a mixed 200–400 source donor corpus without letting donor equipment math, item rarity, attunement, cyberware, vehicle, crafting, treasure, or requisition systems become canon by accident.

## Core doctrine statement

An object-system construct is any persistent or system-relevant non-actor construct that can be held, worn, installed, consumed, wielded, crafted, repaired, modified, upgraded, salvaged, requisitioned, anchored, used as a platform, or used as a source-local object system. Object-system construct is broader than item, equipment, weapon, armor, tool, relic, implant, vehicle, platform, anchor, consumable, material, intelligent object, or source-local object.

D09 defines object-state substrate. It records what an object is, what it is made of, what function it serves, how it is accessed, what state it is in, what larger systems it interfaces with, and what source-local boundaries apply. D09 does not independently grant powers, resolve combat math, define harm outcomes, confer actor personhood, decide advancement proof, or create economy law.

## File order

1. `D09-00_layered_object_state_architecture.md`
2. `D09-01_identity_material_function_and_access_layers.md`
3. `D09-02_weapons_armor_tools_foci_consumables_and_materials.md`
4. `D09-03_relics_artifacts_anchors_intelligent_objects_and_personhood_interface.md`
5. `D09-04_implants_prosthetics_cyberware_biotech_living_gear_and_body_integrated_objects.md`
6. `D09-05_vehicles_platforms_ships_mechs_drones_and_external_bodies.md`
7. `D09-06_crafting_repair_salvage_modification_upgrade_and_requisition_interface.md`
8. `D09-07_source_local_object_and_equipment_conversion.md`
9. `D09-08_runtime_records_ui_and_owner_handoffs.md`
10. `D09-09_integration_checklists_and_ddr_register.md`
11. `D09_pack_manifest.json`

## D09 owns

D09 owns object-state, object identity, object category, object record depth, material profile, durability and condition state, object function category, object access interface, source-local object boundary, weapon/protection/tool/focus/consumable/material/catalyst object functions, relic/artifact/anchor/intelligent-object object-side interfaces, body-integrated object-side interfaces, platform and external-body object-side records, object work/acquisition state, stack/batch/supply records, object visibility states, promotion/demotion/retirement/destruction/history logic, and owner handoff states.

## D09 does not own

| Domain | Owner |
|---|---|
| Power Economy pools, charges, fuel-as-resource doctrine, reservoirs, recharge, overdraw | D03 |
| Advancement proof, breakthrough gates, item-based capstones, tier proof | D04 |
| Crafting skill, repair training, surgery, piloting, gunnery, engineering, diagnosis, research methods | D05 |
| Routes, Techniques, Principles, Feature Ledgers, object-linked powers | D06 |
| Harm, injury, curse injury, corruption, backlash, rejection, malfunction harm, terminal consequences | D07 |
| Intelligent-object actor-state, AI personhood, spirit-in-object continuity, symbiote agency | D08 |
| Economy, ownership law, faction control, market availability, requisition authority, strategic scarcity | D10 |
| Player-facing narration behavior | D11 / later runtime adapter |
| Donor equipment/object taxonomy as canon | Source-local / canon promotion |
| Final database schema | Later runtime/schema phase |

## Embedded risk safeguards

1. D09 must not become the universal equipment owner.
2. Not every object receives a full record.
3. Important objects remain promotable.
4. Donor weapon and armor math do not leak into D09.
5. Magic-item assumptions do not become default object law.
6. Cyberware and graft assumptions do not become default body law.
7. Platform systems do not import donor vehicle doctrine.
8. Crafting does not become economy doctrine.
9. Relic significance does not collapse into mechanical power.
10. Intelligent objects require D08 handoff when actor-state is implicated.
11. Salvage preserves actor-remains and taboo pressure.
12. D10 economy and faction doctrine is not solved inside D09.


---

<!-- FILE: D09-00_layered_object_state_architecture.md -->

# D09-00 Layered Object-State Architecture

## Purpose

This file establishes D09’s opening architecture. It defines object-system construct as the broadest D09 term and prevents Astra from treating all objects as ordinary equipment, all relics as magic items, all platforms as vehicles, all materials as currency, or all source-local equipment systems as canon.

## Core rule

D09 defines object-state substrate. It records what an object-system construct is, what it is made of, what it does, how it is accessed, what state it is in, what other systems it touches, and what source-local boundaries apply. It does not independently grant powers, resolve combat math, define harm outcomes, confer actor personhood, decide advancement proof, or create economy law.

## Object-system construct

An object-system construct is any persistent or system-relevant non-actor construct that can be held, worn, installed, consumed, wielded, crafted, repaired, modified, upgraded, salvaged, requisitioned, anchored, used as a platform, or used as a source-local object system.

Object-system construct is broader than item, equipment, gear, weapon, armor, tool, relic, implant, prosthetic, vehicle, platform, anchor, consumable, material, intelligent object, or source-local object.

## Categories beneath object-system construct

| Category | Examples |
|---|---|
| Mundane Gear | rope, pack, lamp, supplies, clothing, field gear. |
| Weapon | sword, rifle, staff, bow, drone weapon, ship weapon, natural-weapon harness. |
| Armor / Protection | armor, shield, ward shell, hazard suit, exosuit plating. |
| Tool / Instrument | lockpicks, scanner, alchemy kit, ritual tools, surgical kit. |
| Focus / Channel | wand, staff, prayer wheel, neural jack, spirit bell, route token. |
| Relic / Artifact | named, historically significant, anchor-linked, factional, route-linked, or world-relevant object. |
| Consumable | potion, pill, battery, fuel cell, grenade, scroll-like object, catalyst dose. |
| Material / Component | ore, hide, crystal, reagent, monster core, salvage, concept-bearing shard. |
| Implant / Prosthetic | cyberware, biotech, graft, artificial organ, neural interface, body socket. |
| Vehicle / Platform | cart, ship, starship, mech, drone chassis, mobile base, habitat. |
| Anchor / Vessel | phylactery-like object, spirit talisman, AI core, shrine vessel, relic housing. |
| Intelligent Object | sentient weapon, AI core, bound-spirit item, ego relic, living item. |
| Source-local Object | donor/campaign magic item, cyberware, vehicle, treasure, crafting, attunement, or artifact system. |

A single object may hold many categories. A sentient sword can be weapon, relic, anchor, intelligent object, D08 actor host, D06 route interface, D03 reservoir interface, D07 curse risk, and D10 faction artifact.

## Layered object-state record

| Layer | Purpose |
|---|---|
| Object Identity | Name, source, origin, uniqueness, holder/location. |
| Physical / Material | Matter, structure, durability, wear, repair mode, vulnerability, contamination. |
| Use / Function | Weapon, armor, tool, focus, consumable, material, platform, anchor, implant, catalyst. |
| Wielding / Access | Training, anatomy, interface, permission, bond, synchronization, route, carrier, source-local access. |
| Power / Resource Interface | D03 charges, fuel, reservoirs, recharge, overdraw, instability, powered operation. |
| Route / Technique Interface | D06 object-linked Techniques, route features, Principles, signature forms. |
| Harm / Curse / Failure | D07 breakage harm, backlash, rejection, curse, corruption, malfunction, terminal failure. |
| Actor / Personhood | D08 intelligent item, AI, spirit-in-object, symbiote, platform-as-body, body integration. |
| Platform / Vehicle | Vehicles, ships, mechs, drones, mobile bases, habitats, external bodies. |
| Craft / Upgrade / Maintenance | D09 object work state; D05 procedure; other handoffs as needed. |
| Social / Economic / Legal | D10 ownership, law, faction control, scarcity, market, requisition, strategic assets. |
| Source-local Boundary | Donor object rules, attunement, rarity, cyberware, vehicle, crafting, treasure, requisition. |

## Ownership boundary

D09 owns object-state. It does not own all consequences of object use. A relic staff may require D03 for charges, D06 for object-linked Techniques, D07 for backlash, D08 for a bound spirit, and D10 for temple ownership. A cybernetic arm requires D08 body compatibility, D05 surgery, D07 rejection handling, D03 powered operation if relevant, and D10 legality. A starship requires D03 reactor/fuel, D05 piloting and repair, D07 crash/breach harm, D08 AI/living ship actor-state, and D10 registry/faction law.

## Source-local restraint

D09 never imports donor object systems as canon by default. Donor weapon damage dice, armor class rules, magic item rarity, attunement slots, item slots, cyberware capacity, humanity loss, starship stat blocks, mech hardpoints, drone command caps, crafting DCs, treasure tables, and requisition ratings remain source-local unless explicitly normalized and promoted.

## Acceptance criteria

A D09 architecture decision is valid when it identifies the construct type, records only necessary object-state, routes attached systems to owner files, allows overlapping categories, preserves source-local boundaries, and avoids making D09 the universal equipment/economy/combat owner.


---

<!-- FILE: D09-01_identity_material_function_and_access_layers.md -->

# D09-01 Object Identity, Material, Function, and Access Layers

## Purpose

This file defines foundational object record layers: identity, material, function, and access. It prevents donor item packages from entering Astra as indivisible bundles.

## Core rule

An object-system construct is recorded through separable identity, material, function, and access layers. These layers may interact, but none automatically grants Power Economy behavior, Route Features, harm consequences, actor personhood, market value, faction authority, or source-local canon status.

## Object identity layer

Identity fields may include object name or label, identity type, uniqueness state, source, origin, maker, current holder, current location, history relevance, recognition state, source-local boundary, and validation state.

| Identity type | Meaning |
|---|---|
| Generic Object | Interchangeable or ordinary object. |
| Tracked Object | Specific object worth tracking but not unique. |
| Named Object | Has a name, history, or persistent identity. |
| Relic Object | Has exceptional age, history, anchor, faction, route, or metaphysical relevance. |
| Artifact Object | High-significance object with major world, route, actor, or source-local pressure. |
| Consumable Object | Designed to be spent, eaten, triggered, discharged, burned, or destroyed by use. |
| Material Object | Ore, hide, crystal, core, reagent, salvage, component, concept-bearing material. |
| Platform Object | Vehicle, ship, mech, drone body, habitat, mobile base, or external chassis. |
| Anchor Object | Houses, binds, stabilizes, stores, or links actor, spirit, AI, route, memory, curse, or power. |
| Intelligent Object | Hosts or expresses cognition, personhood, agency, or actor-state. |
| Source-local Object | Uses donor/campaign object rules. |

## Uniqueness state

Uniqueness is separate from power.

| State | Meaning |
|---|---|
| Generic | Interchangeable object; no persistent identity required. |
| Batch-specific | One of a batch with shared maker, pattern, source, or limited availability. |
| Tracked Individual | Individual object matters due to use, damage, owner, history, or modification. |
| Named | Known by name or title. |
| Unique | Only one known instance. |
| Legendary / Artifact-grade | Unique or near-unique with major route, faction, world, actor, or source-local impact. |
| Source-local Unique | Local source defines uniqueness. |

A unique ring may be socially meaningful but mechanically minor. A mass-produced rifle may be mechanically dangerous without being unique.

## Object status

D09 does not use “magic item” as the universal status.

| Status | Meaning |
|---|---|
| Mundane | No special power or exceptional source-local rule. |
| Fine / Specialized | Superior quality, specialized function, or expert construction. |
| Enhanced | Improved by material, craft, technology, enchantment-equivalent, route interface, or source-local rule. |
| Imbued | Carries power, charge, resonance, technique-support, or Power Economy interface. |
| Relic | Carries history, significance, anchor value, unique power, route relevance, or faction importance. |
| Artifact | Major relic with high-scale world, actor, route, faction, or source-local consequence. |
| Cursed / Dangerous | Has harmful, unstable, corruptive, binding, or failure pressure. |
| Source-local | Status follows bounded donor/campaign object rules. |

Statuses may overlap.

## Material layer

Material fields may include base material, special material, source, purity, grade, stability, durability, wear, repair mode, compatibility, resonance, vulnerability, contamination, scarcity signal, and source-local boundary.

| Material type | Examples |
|---|---|
| Common | wood, iron, leather, cloth, stone, glass. |
| Fine | tempered steel, expert alloy, reinforced hide, precision ceramic. |
| Exotic | star-metal, voidglass, dragonbone, living crystal, alien polymer. |
| Biological | bone, shell, hide, venom sac, organ, blood, silk, resin. |
| Spiritual / Energetic | essence crystal, spirit jade, soul ash, mana-conductive stone. |
| Concept-bearing | Dao stone, principle shard, oathglass, death-ore, time salt. |
| Technological | circuits, nanomesh, plasma conduit, synthetic muscle, quantum lattice. |
| Biotech | grown tissue, symbiotic fiber, engineered organ, living armor substrate. |
| Salvage | scrap, wreckage, battlefield remains, recovered components. |
| Source-local | donor/campaign-specific material rule. |

Material does not automatically define final economy. D10 owns market value, law, faction control, and strategic scarcity.

## Rarity signal

Rarity is a routing signal, not final price: common, local, specialized, rare, strategic, unique, forbidden/restricted, or source-local.

## Durability and condition

D09 owns object condition. D07 owns injury or harm caused by object failure.

Object states include intact, worn, damaged, broken, unstable, contaminated, overloaded, dormant, sealed, destroyed, and source-local.

## Function layer

Function records what the object does: gear, weapon, armor/protection, tool/instrument, focus/channel, consumable, catalyst, material/component, implant/prosthetic, vehicle/platform, anchor/vessel, container/storage, communication/sensor, key/access object, intelligent object, or source-local object.

Functions may be primary, secondary, hidden, dormant, conditional, damaged, or source-local.

## Access layer

Access requirements may include no special access, training, anatomy, interface, power compatibility, route access, bond access, attunement-equivalent synchronization, ownership/permission, rank/authority, environmental condition, or source-local access.

Access does not equal ownership. Ownership does not equal usability.

## Attunement-equivalent without donor lock-in

Astra supports resonance alignment, oath-binding, neural calibration, biometric lock, spirit recognition, route synchronization, power-carrier tuning, identity imprint, ritual claim, faction authorization, and source-local attunement without importing donor attunement slot limits.

## Source-local assumptions to block

D09 blocks assumptions that all magic items use attunement slots, all relics are magical, all cyberware reduces humanity, all vehicles share a stat block model, all treasure has market price, all rare items are purchasable, all artifacts are combat upgrades, all consumables are safe if identified, rarity ladders map to Astra tiers, weapons use donor damage math, armor uses donor armor class, or materials use donor crafting economies.

## Acceptance criteria

A ruling is valid when it separates identity, uniqueness, status, material, function, and access; treats uniqueness separately from power; records rarity as signal; distinguishes ownership from usability; and routes attached systems to owner files.


---

<!-- FILE: D09-02_weapons_armor_tools_foci_consumables_and_materials.md -->

# D09-02 Weapons, Armor, Tools, Foci, Consumables, and Materials

## Purpose

This file defines major object-function families without importing donor damage math, armor class logic, spellcasting assumptions, item-slot rules, treasure economies, cyberware capacity, or crafting systems as Astra defaults.

## Core rule

D09 classifies object function and object-state. It does not independently define attack math, armor math, skill bonuses, resource costs, route powers, harm consequences, actor personhood, or market economy. Object functions may overlap, and each function must state what D09 owns, what it hands off, and what donor assumptions are blocked.

## Functional object families

D09 supports weapons, armor/protection, tools/instruments, foci/channels, consumables, materials/components, catalysts, natural weapon interfaces, body-integrated objects, and source-local functions.

## Weapons

A weapon is an object or object-function used to project force, deliver harm, threaten, defend, channel technique, control space, or enable combat actions. D09 records weapon identity, material, form, scale, range/reach category, handling profile, access, durability, ammunition/charge interface, mounting/interface, source-local boundary, and handoffs.

D09 does not own universal damage math. Donor damage dice, attack bonuses, critical rules, proficiency assumptions, weapon properties, and weapon categories are not Astra defaults.

## Armor and protection

Armor/protection includes objects used to reduce, redirect, absorb, deflect, filter, conceal from, or survive harm. D09 records coverage, material, access, compatibility, durability, repair mode, encumbrance signal if needed, and protection function.

D09 does not own universal defense math, armor class, shield action rules, damage reduction formula, or armor slot assumptions. D07 owns harm consequences.

## Tools and instruments

A tool/instrument performs, improves, enables, measures, repairs, crafts, treats, investigates, communicates, pilots, or manipulates a task. D09 records tool identity, material, function, access, condition, calibration, portability, dependencies, and source-local boundary.

Tools enable methods. They do not automatically grant flat skill bonuses. D05 owns competence, method, training, research, and professional application.

## Foci and channels

A focus/channel directs, stabilizes, amplifies, shapes, translates, stores, or accesses power, attention, technique, ritual, computation, signal, or metaphysical relation. D09 records focus/channel function. It does not make the object a spellcasting item by default.

Handoffs: D03 owns cost/carrier/charges/reservoir/recharge/overdraw; D06 owns Techniques/Route Features/Principles/signature forms/object expressions; D07 owns backlash/overload/corruption/rejection/failure; D08 owns intelligent or actor-hosted foci; D10 owns sacred/faction/legal status.

## Consumables

A consumable is intended to be spent, eaten, drunk, injected, burned, discharged, broken, triggered, absorbed, installed, detonated, sacrificed, or otherwise depleted by use. Consumables include potions, pills, medicine, batteries, fuel cells, grenades, scroll-like objects, charms, ritual incense, catalyst doses, monster cores, repair foam, nanite vials, and source-local consumables.

Consumables must record use mode, depletion mode, activation requirements, storage conditions, stability, dose/charge count if relevant, effect owner, side effects, contamination risk, and source-local rule.

A potion, pill, battery, grenade, scroll, and catalyst do not use one universal rule.

## Materials, components, and catalysts

A material/component is used to make, repair, empower, transform, trade, study, feed, catalyze, anchor, or modify another construct. A catalyst enables, accelerates, stabilizes, alters, or risks a transformation, crafting process, ritual, advancement, route expression, Power Economy change, or actor evolution.

D09 records material/catalyst object-state. D04 validates advancement gate/proof. D08 validates actor evolution/body changes. D07 validates pain, rejection, corruption, mutation, partial transformation, and terminal failure. D03 validates carrier/reservoir changes. D06 validates route/Technique/Principle changes. D10 validates scarcity and law.

## Natural weapons and body-integrated tools

D09 must distinguish equipped objects from body-integrated functions. Claws grown from a body are primarily D08/D07/D06; a harvested bone blade is D09 material/weapon; a cybernetic claw implant is D09 implant/weapon plus D08 body integration; a living symbiotic blade is D09 weapon plus D08 companion/symbiote plus D07 rejection risk.

D09 should not convert every body capability into equipment.

## Wear, breakage, depletion, and limits

Object states may include intact, worn, damaged, broken, unstable, contaminated, overloaded, depleted, jammed, misaligned, dormant, sealed, destroyed, or source-local. Limits may include charges, ammunition, fuel, dose count, durability, cooldown, reload time, maintenance interval, environment, access condition, user strain, instability threshold, or source-local limit.

D09 records state and limits. D03 owns resource behavior. D07 owns harm from failure. D05 owns repair/maintenance. D10 owns resupply constraints.

## Source-local assumptions to block

D09 blocks donor weapon damage dice, armor class, defense math, tool bonuses, potion/scroll categories, battery/fuel rules, cyberware capacity/humanity systems, crafting DCs, magic item rarity tiers, natural weapon assumptions, and material pricing from becoming defaults.

## Acceptance criteria

A functional object ruling is valid when it classifies function without importing donor math, separates weapon/armor/tool/focus/consumable/material/catalyst functions, routes attached systems to owners, treats natural weapons as D08-sensitive, and blocks donor equipment assumptions from default import.


---

<!-- FILE: D09-03_relics_artifacts_anchors_intelligent_objects_and_personhood_interface.md -->

# D09-03 Relics, Artifacts, Anchors, Intelligent Objects, and Object Personhood Interface

## Purpose

This file defines objects that matter beyond ordinary use: relics, artifacts, anchors, ego items, intelligent weapons, AI cores, spirit-bound tools, ancestral items, living items, cursed objects, and source-local magic-item equivalents.

## Core rule

A relic or artifact is not defined by power alone. It may matter because of history, faction authority, route interaction, actor anchoring, source-local status, strategic value, curse pressure, or world-state consequence. D09 records object identity, object-state, anchor function, access state, dormancy, recognition, and source-local boundary. It does not independently grant powers, personhood, curse consequences, or ownership authority.

## Object statuses

Enhanced object, imbued object, relic, artifact, cursed/dangerous object, intelligent object, and anchor object are distinct statuses that may overlap.

A sword can be enhanced but not relic. A family ring can be relic but not powerful. A phylactery-like vessel can be anchor, artifact, cursed object, and source-local object. A ship AI core can be platform component, anchor, intelligent object, and D08 actor host.

## Significance axes

Relic significance is not the same as mechanical power. Track historical, mechanical, social, route, actor, world-state, and source-local significance separately.

A relic can matter because of lineage, status, taboo, faction authority, route compatibility, actor-hosting, world-state locks, or local myth without being a combat upgrade.

## Anchor objects

An anchor object houses, binds, stabilizes, stores, links, imprisons, preserves, or indexes another system. Anchor targets may include spirit, AI, soul, memory, curse, oath, pact, route, Technique, Principle, Power Economy reservoir, place, faction authority, body continuity, clone continuity, phylactery-like survival, shrine presence, or source-local entity.

Anchor states include empty, hosting, bound, linked, stabilizing, sealed, damaged, corrupted, dormant, transferring, destroyed, and source-local.

D09 owns anchor object-state. D08 owns actor continuity/personhood. D07 owns harm from anchor failure. D03 owns reservoir rupture. D06 owns route loss. D10 owns social/world consequence.

## Intelligent objects

An intelligent object hosts or expresses cognition, memory, agency, preference, personhood, AI, spirit, ego, bound will, or actor-state. D09 does not decide personhood. It records object-host structure and requires D08 handoff.

Sentient weapons, AI cores, bound-spirit items, ego relics, living items, memory archives, possessed objects, and source-local intelligent items require D08 review when personhood, cognition, agency, continuity, or object-actor state matters.

An object can speak or react without full personhood. An object can have personhood without being usable equipment. An intelligent object can refuse, bargain, deceive, sleep, degrade, fragment, or become corrupted if owner files validate those states.

## Recognition, refusal, bond, dormancy, and awakening

D09 may record whether an object recognizes, refuses, bonds to, awakens for, or remains dormant for a user. This can come from lock, route incompatibility, power incompatibility, social authorization, curse, source-local rule, or actual object agency. Object refusal does not automatically mean the item is a person.

Dormancy/awakening may require D03 recharge/resource, D04 threshold, D05 research/repair/ritual, D06 route alignment, D07 corruption purge, D08 actor awakening, D10 recognition/permission, or source-local trigger.

## Curses, rejection, and anchor destruction

D09 records dangerous object state. D07 owns consequences: backlash, injury, identity harm, compulsion, corruption, resource drain, carrier damage, possession pressure, bond harm, mutation, social contamination, anchor fracture, terminal failure, or source-local curse.

Anchor destruction can produce hosted actor death, AI data loss, spirit release, curse release, soul severance, route feature loss, reservoir rupture, companion grief, faction crisis, world-state shift, source-local resurrection interruption, antagonist release, or no special consequence. D09 only owns destroyed object-state.

## Ownership and usability conflict

Relics often create conflict between legal ownership, inheritance, conquest, theft, pact claim, route recognition, bloodline recognition, faction office, AI authorization, spirit acceptance, and source-local attunement.

D10 owns ownership and public recognition. D09 owns access state. D08 owns intelligent-object agency. D07 owns harm from forced access.

## Acceptance criteria

A relic/anchor/intelligent-object ruling is valid when it distinguishes statuses, tracks significance axes, records anchor targets and states, requires D08 handoff for object-actor state, routes curse/backlash/awakening/recognition to owner files, and preserves donor magic-item systems as source-local unless normalized.


---

<!-- FILE: D09-04_implants_prosthetics_cyberware_biotech_living_gear_and_body_integrated_objects.md -->

# D09-04 Implants, Prosthetics, Cyberware, Biotech, Living Gear, and Body-Integrated Objects

## Purpose

This file defines objects attached to, installed in, grown into, grafted onto, replacing, sharing, or modifying an actor’s body. It prevents donor cyberware capacity, humanity loss, augmentation slots, graft economies, mutation trees, and magical tattoo systems from becoming default Astra law.

## Core rule

A body-integrated object is an object-system construct installed in, attached to, grafted onto, grown through, replacing, inhabiting, synchronized with, or structurally linked to an actor’s body. D09 records object-side integration state. D08 determines how it relates to actor body-state and identity. D03, D05, D06, D07, and D10 validate power, installation, route effects, harm, and social/legal consequences.

## Object types

Prosthetic, implant, cyberware, biotech, graft, living gear, symbiote, parasitic object, body-integrated weapon/tool, internal reservoir, neural interface, and source-local augmentation are distinct but overlapping object types.

A prosthetic replaces, supplements, or restores body function. An implant is installed inside or through the body. Cyberware is technological or machine-mediated body integration. Biotech is biological, engineered, grown, genetic, cellular, symbiotic, or organic augmentation. A graft is transplanted or fused tissue/material from another source. Living gear is alive, semi-alive, grown, hungry, regenerative, responsive, symbiotic, parasitic, or actor-adjacent.

## Integration modes and states

Integration modes include worn-adjacent, socketed, attached, implanted, prosthetic replacement, grafted, grown-in, symbiotic, parasitic, neural/cognitive, carrier-integrated, route-integrated, anchor-integrated, and source-local.

Integration states include uninstalled, fitted, installed, calibrating, integrated, over-integrated, rejected, infected/contaminated, malfunctioning, damaged, removed, severed, dormant, and source-local.

D05 owns procedure and maintenance. D07 owns harm. D09 owns object condition and integration state.

## Compatibility

Compatibility may depend on body substrate, kinform, scale, anatomy, nervous system or equivalent, cognition interface, D03 carrier, D06 route, immune/repair mode, material resonance, source-local physiology, installation method, maintenance environment, or D10 legality/access.

D08 owns body compatibility. D03 owns carrier compatibility. D06 owns route compatibility. D05 owns installation/calibration. D07 owns rejection/harm.

## Rejection and integration risk

Risk sources include immune rejection, nerve mismatch, carrier mismatch, route incompatibility, material contamination, infection, corruption, identity conflict, symbiote resistance, AI control conflict, overload, power leakage, invasive growth, and source-local curse/mutation.

Outcomes may include no function, partial function, pain, injury, infection, mutation, corruption, identity harm, resource leak, carrier damage, route strain, compulsion if actor/personhood involved, terminal integration failure, or source-local consequence. D07 owns consequences.

## Powered implants and route-linked functions

Powered implants and internal reservoirs require D03 for resource behavior, reservoir capacity, recharge, overdraw, power leakage, and carrier interaction. Implant-linked Techniques require D06. D09 should not convert every integrated object into a Technique or power pool.

## Symbiotes and living gear

Living gear may be object, actor, companion, hazard, infection, or mixed case. D08 handoff is required if it has agency, cognition, personhood, bond, instinctive behavior, continuity, or companion relation. D07 handoff is required if it can reject, corrupt, mutate, feed, dominate, infect, or damage the host. D03 applies if it consumes/provides resources. D10 applies if it is illegal, taboo, sacred, protected, enslaved, faction-controlled, or socially recognized.

Symbiotic does not mean safe. Parasitic does not mean unusable.

## Augmentation burden

D09 supports physical, nervous, cognitive, immune, carrier, route, maintenance, social/legal, identity, and source-local burden signals. D09 does not import universal cyberware capacity, humanity loss, essence loss, graft slots, implant slots, or augmentation limits.

## Removal, replacement, and continuity

Removing or replacing a body-integrated object can be trivial, surgical, traumatic, identity-altering, or impossible. D09 records removal state. D08 owns actor continuity/body-state. D07 owns trauma. D03 owns carrier severance. D06 owns route loss. D10 owns social recognition.

## Source-local augmentation systems

Donor cyberware slots, humanity loss, essence loss, implant capacity, surgery DCs, graft slots, monster graft corruption, biotech mutation trees, living armor bonding, symbiote rules, prosthetic upgrade trees, hacking vulnerability, limb pricing, body cultivation organs, magical tattoos, and body-mod economies normalize by function or remain source-local.

## Acceptance criteria

A body-integrated object ruling is valid when it records integrated object type, integration mode/state, compatibility, burden, risk, maintenance/removal needs, owner handoffs, D08 review for agency/personhood, and source-local boundaries.


---

<!-- FILE: D09-05_vehicles_platforms_ships_mechs_drones_and_external_bodies.md -->

# D09-05 Vehicles, Platforms, Ships, Mechs, Drones, and External Bodies

## Purpose

This file defines large or externally embodied object systems: vehicles, ships, mechs, drones, mobile bases, habitats, siege platforms, mounts-as-platforms, living ships, AI-assisted vessels, bonded machines, and platform-like extensions of an actor.

## Core rule

A platform is an object-system construct that can carry, house, move, protect, extend, host, empower, transport, or operationally support actors, objects, systems, cargo, weapons, habitats, drones, or source-local functions. D09 records platform-state. D03, D05, D06, D07, D08, and D10 validate power, operation, route effects, harm, actor-state, and social/world consequences.

## Vehicle, platform, and external body

A vehicle primarily enables movement, transport, travel, carrying, or maneuvering. A platform supports actors, systems, cargo, weapons, tools, habitats, sensors, movement, or operations. An external body functions as an actor’s extended body, operational shell, remote body, piloted form, bonded form, or hosted embodiment.

A starship can be vehicle, platform, habitat, strategic object, intelligent object host, and source-local object. A mech can be platform, external body, armor/protection, weapon mount, and route interface.

## Platform categories

D09 supports personal vehicles, crew vehicles, starships/spacecraft, mechs/walkers, exosuit/powered armor platforms, drones/remote chassis, drone carriers/network platforms, mobile bases, habitats/stations, siege/heavy platforms, mount-as-platform systems, living platforms, external bodies, and source-local platforms.

## Platform structure layers

Platform records may track hull/frame, propulsion/mobility, power core, control interface, crew stations, payload/cargo, weapons/mounts, armor/shields, sensors/communication, life support/habitability, utility systems, AI/spirit/actor host, anchor/relic interface, and source-local systems.

D09 records structure and platform-state. It does not solve subsystem math.

## Operation types

Operation types include manual, crewed, assisted, autonomous, remote-controlled, programmed, AI-piloted, spirit-piloted, bonded, living, possession-contested, and source-local.

D08 handoff is required when platform operation involves actor-state, AI personhood, spirit agency, living cognition, bonded will, or contested control.

## Crew roles and operation

D09 records crew stations and required interfaces. D05 owns competence. Roles may include pilot, driver, navigator, engineer, mechanic, gunner, sensor operator, commander, quartermaster, medic, ritual operator, AI handler, drone controller, and source-local role.

D09 must not import donor crew-action economies or vehicle action rules as defaults.

## Fuel, power, shields, and reactor systems

D09 may record fuel type, reactor/power core presence, battery bank, essence engine, shield generator, heat/overload signal, recharge method, reserve state, and source-local resource rule. D03 owns fuel, charge, reservoirs, recharge, overdraw, heat/instability if modeled as resource, power routing, shield resource, and engine cost. D07 owns harm from failure.

## Vehicle-scale weapons and armor

D09 records weapon systems, mounts, armor, shields, and hardpoints as object-state. It does not import donor vehicle combat math. D06 owns vehicle-linked Techniques. D03 owns powered weapons/shields. D07 owns damage/failure consequences. Later combat doctrine owns combat math.

## Platform condition and subsystem damage

Platform states include intact, worn, damaged, system-impaired, breached, disabled, stranded, overloaded, contaminated, hostile-controlled, dormant, derelict, destroyed, and source-local.

Subsystem damage may affect propulsion, control, power, shields, weapons, sensors, life support, cargo, crew stations, AI core, anchor, habitat, or source-local systems. D09 records damaged subsystem; D07 owns crash harm, crew harm, breach, fire, decompression, corruption, malfunction injury, and terminal destruction.

## Cargo, habitability, and operational support

Platforms may provide passenger transport, cargo, storage, workshop, medbay, lab, refinery, crafting station, training space, ritual chamber, hangar, drone bay, living quarters, prison, containment, archive, command center, sensor network, or faction presence. D05 owns effective use of facilities. D10 owns cargo law, smuggling, taxation, docking rights, territorial permissions, faction ownership, and strategic asset status.

## Platform-as-body, drones, and mounts-as-platforms

A platform may be an actor’s body or host: ship AI, bonded mech, living ship, spirit-bound siege engine, drone chassis for an uploaded mind, remote avatar body, necromantic fortress, or source-local sentient vehicle. D08 owns actor continuity, personhood, agency, body-state, bond, and external-body relation.

Drones can be tools, vehicles, platforms, actors, companions, swarm units, or external bodies. D09 owns chassis/function; D08 owns actor/personhood if present. Donor drone command caps remain source-local.

Mount-as-platform cases keep the living mount as D08 actor and the saddle/tower/weapon rig as D09 platform gear.

## Source-local systems

Donor vehicle stat blocks, starship systems, mech construction, ship combat, crew actions, cargo economies, fuel rules, heat systems, hardpoints, vehicle armor, chase rules, docking rules, drone control, remote rigging, living ship rules, sentient vehicle rules, salvage, and platform economies normalize by function or remain source-local.

## Acceptance criteria

A platform ruling is valid when it distinguishes vehicle/platform/external body, records relevant layers, routes operation to D05, power to D03, harm to D07, actor-hosting to D08, social/legal to D10, and blocks donor vehicle systems from default import.


---

<!-- FILE: D09-06_crafting_repair_salvage_modification_upgrade_and_requisition_interface.md -->

# D09-06 Crafting, Repair, Salvage, Modification, Upgrade, and Requisition Interface

## Purpose

This file defines how objects are made, repaired, maintained, altered, upgraded, stripped for parts, recovered from the field, or acquired through institutional channels without importing donor crafting economies, enchantment slots, hardpoints, treasure tables, item levels, or requisition rules as Astra defaults.

## Core rule

Crafting, repair, maintenance, modification, upgrade, salvage, and requisition are object-state operations. D09 records what object is being created, restored, altered, harvested, produced, or acquired. D05 validates method and competence. D03 validates resource/power behavior. D06 validates route-linked object effects. D07 validates dangerous work and failure consequences. D08 validates actor-integrated objects. D10 validates economy, law, ownership, scarcity, and faction authority.

## Operation distinctions

Crafting creates a new object from materials, labor, tools, methods, facilities, plans, and sometimes power or ritual conditions. Repair restores damaged object function. Maintenance prevents degradation or recalibrates. Modification changes function/access/structure without necessarily improving tier. Upgrade improves capability or efficiency and may add constraints. Salvage recovers material, components, information, fuel, relic fragments, monster parts, or usable systems from objects, actors, wrecks, or environments. Requisition acquires objects through institutional, legal, military, guild, sect, corporate, expeditionary, or faction authority.

Requisition is not purchase. Treasure is not automatically wealth. Salvage is not free material.

## Object work states and repair depth

Work states include unworked, diagnosed, planned, materials gathered, in progress, interrupted, field patched, repaired, maintained, modified, upgraded, degraded, failed, dangerous/unstable, contaminated, and source-local.

Repair depths include cosmetic repair, field patch, functional repair, subsystem repair, structural repair, restoration, reconstruction, and source-local repair. A field patch should not erase serious damage.

## Inputs

Crafting, repair, modification, and upgrade may require raw material, refined material, component, rare component, strategic material, catalyst, schematic, recipe, blueprint, toolchain, facility, workshop, lab, shipyard, forge, alchemy furnace, ritual site, software/key/license, trained labor, faction authorization, route permission, Power Economy input, and source-local ingredients.

D09 records input requirements. D05 owns method. D10 owns access and supply.

## Schematics, recipes, and toolchains

A schematic describes structure, assembly, interface, or technical design. A recipe describes material combination, alchemy, ritual procedure, biotech growth, enchantment-equivalent sequence, or source-local production. A toolchain is the required set of tools, facilities, procedures, calibration, and competencies.

D09 records that these exist and what object they apply to. D05 owns interpretation/execution. D10 owns licensing/ownership. Source-local systems retain donor recipe logic unless normalized.

## Upgrade paths

Upgrade path types include material, component, interface, power, route, structural, platform, body-integrated, relic awakening/restoration, safety, and source-local upgrades. D09 must not assume universal item levels, hardpoints, enchantment caps, rarity upgrades, cyberware capacity, or vehicle hardpoint economies.

An upgrade can add constraints. A stronger engine may consume more fuel. A powerful implant may increase maintenance burden. A relic awakening may increase faction attention.

## Salvage doctrine

Salvage outputs may include raw material, component, rare component, fuel, charge cell, subsystem, catalyst, monster part, biological tissue, concept-bearing fragment, data, schematic, memory archive, relic shard, cursed material, contaminated material, or source-local treasure.

Sources include battlefield, monster remains, vehicle wreck, starship wreck, mech wreck, ruin, broken relic, cyberware remains, drone swarm, construct body, carcass, spirit residue, or source-local source.

## Salvage from actors

Salvage from actors requires D08/D10/D07 review when the source was an actor, had personhood, leaves body parts, memory, soul residue, AI core, companion remains, sacred substance, legality/taboo, contamination, identity residue, route residue, curse, or grief implications.

D09 records material output. It does not erase actor/personhood context.

## Dangerous work and contamination

Risk sources include unstable material, cursed object, contaminated salvage, corrupted monster part, AI malware, spiritual residue, concept-bearing incompatibility, power overload, wrong route alignment, poor repair, incompatible parts, unsafe field conditions, and source-local risk.

D07 owns harm/corruption. D03 owns power overload/resource leak. D10 owns legal/social consequences.

## Requisition interface

Requisition fields may include requested object category, quantity, quality, urgency, authority basis, scarcity signal, legal status, faction source, debt/obligation marker, replacement expectation, return requirement, restricted-use condition, and source-local rule.

Outcomes include granted, partially granted, delayed, denied, substituted, debt incurred, favor owed, monitored use, illegal diversion, black-market acquisition, faction conflict, or source-local result. D10 owns approval, law, reputation, and consequence.

## Advancement boundaries

Object work can interact with advancement: crafting a signature weapon as proof, repairing an ancestral relic to unlock route progression, building a mech as capstone, refining a transformation catalyst, restoring a spirit anchor, or upgrading a prosthetic to stabilize a form-state. D04 owns advancement proof, gate, breakthrough, and capstone status.

## Source-local systems

Donor crafting DCs, item levels, recipes, magic item creation, downtime costs, tool proficiency, salvage tables, treasure tables, requisition ratings, wealth-by-level, hardpoints, enchantment slots, vehicle repair, cyberware prices, shipyards, alchemy pill grades, refinement failures, sect exchanges, and black-market systems normalize by function or remain source-local.

## Acceptance criteria

An object work/acquisition ruling is valid when it distinguishes operation type, records work state and repair depth, records inputs/outputs, supports upgrades without donor slot import, treats actor salvage with review, treats requisition as D10 authority/economy, and blocks donor crafting economies from default import.


---

<!-- FILE: D09-07_source_local_object_and_equipment_conversion.md -->

# D09-07 Source-local Object and Equipment Conversion

## Purpose

This file defines how Astra absorbs donor object systems without importing donor equipment math, magic-item assumptions, cyberware rules, vehicle systems, crafting economies, or treasure tables as canon.

## Core rule

D09 does not import donor object taxonomy, item math, rarity ladders, equipment slots, attunement systems, vehicle stat blocks, crafting economies, treasure systems, or requisition rules as canon. It decomposes donor object constructs by function, assigns lawful outcomes, and routes attached mechanics to owner files.

## Functional Object Conversion Routing

Donor object constructs are decomposed into Astra-native object-state functions: identity, material, function, access, power interface, route interface, harm/failure, actor/personhood interface, platform interface, crafting/repair/salvage/requisition interface, social/economic interface, and source-local boundary.

## Lawful outcomes

Every donor object construct must receive one lawful outcome: direct Astra mapping, normalized Astra mapping, source-local retained construct, quarantined construct, or escalated doctrine problem.

No donor object should be converted by label alone.

## Conversion questions

For every donor object construct, ask whether it is object, actor, body-state, power source, route feature, harm condition, social asset, faction asset, economy rule, source-local construct, or mixed case; what identity, material, function, and access apply; whether D03/D04/D05/D06/D07/D08/D10 are implicated; whether a source-local boundary is required; and what lawful outcome applies.

## Donor weapon conversion

D09 owns object identity, material, function, access, and durability. D05 owns training/proficiency/use method. D03 owns powered weapon charges, ammo-as-resource, heat, and fuel. D06 owns weapon Techniques/signature forms/route maneuvers. D07 owns injury, breakage harm, malfunction injury. D08 owns body-integrated or living weapon state. D10 owns legality, restriction, social status, and market. Donor damage math, attack bonuses, critical rules, and weapon properties remain source-local or later combat doctrine.

## Donor armor/protection conversion

D09 owns armor/protection object-state, material, coverage, and access. D05 owns armor training/fitting/maintenance. D03 owns powered shields/barriers. D06 owns armor-linked Techniques. D07 owns armor failure harm, contamination, breach, and overload. D08 owns body compatibility/exosuit integration. D10 owns legality/faction uniform/restricted armor. Donor AC, shield math, defense bonus, and damage reduction remain source-local or later combat doctrine.

## Donor tools/foci/consumables/materials

Tools are D09 object-state plus D05 method, not flat bonuses. Foci are D09 channel objects plus D03 resource and D06 Technique handoffs, not spellcasting items by default. Consumables record use/depletion/stability; D03/D04/D05/D06/D07/D10 own resource, advancement, handling, powers, side effects, and economy. Materials/components/catalysts record purity, stability, compatibility, and rarity signal; D05/D03/D04/D06/D07/D08/D10 own use.

## Donor relics, artifacts, magic items, cursed items, and intelligent items

D09 owns object identity, relic/artifact status, anchor profile, access state, dormancy, recognition, and source-local boundary. D03 owns charges/reservoirs. D06 owns powers/Techniques. D07 owns curse/backlash/corruption/rejection. D08 owns intelligent item personhood, AI, spirit, ego, continuity. D10 owns sacred status, inheritance, faction claim, market, and legality. Donor attunement, rarity, ego, and artifact destruction rules remain source-local unless normalized.

## Donor implants, cyberware, biotech, grafts, and body-mod systems

D09 owns prosthetic/implant/cyberware/graft object-state. D08 owns body/kinform compatibility, actor integration, and symbiote personhood. D05 owns surgery, installation, repair, calibration, adaptation training. D03 owns powered implants/internal reservoirs. D06 owns implant-linked Techniques. D07 owns rejection, infection, corruption, mutation, nerve damage, identity harm. D10 owns legality, stigma, black market, and augmentation rights. Donor humanity loss, essence loss, slots, capacity, and body-mod economies remain source-local unless normalized.

## Donor vehicles, ships, mechs, drones, and platforms

D09 owns vehicle/platform state, subsystems, and condition. D03 owns fuel/reactor/shield resource/heat. D05 owns piloting, repair, navigation, gunnery, and operation. D06 owns vehicle-linked Techniques and platform resonance. D07 owns crash, breach, malfunction, overload, crew injury, and destruction. D08 owns AI pilots, living ships, bonded mechs, and platform-as-body cases. D10 owns registry, docking law, ownership, piracy, faction control, and strategic asset status. Donor stat blocks, hardpoints, cargo rules, and chase rules remain source-local unless normalized.

## Donor crafting, repair, salvage, treasure, and requisition systems

D09 owns object work state, operation type, repair depth, and output object. D05 owns procedure and competence. D03 owns powered crafting and reservoir repair. D04 owns proof/gate relevance. D06 owns route-linked crafting. D07 owns dangerous work and cursed salvage. D08 owns actor remains/intelligent/body-integrated object implications. D10 owns economy, requisition, guilds, licensing, strategic materials, and black markets. Donor crafting DCs, item levels, treasure tables, salvage tables, and requisition ratings remain source-local unless normalized.

## Source-local boundary requirements

Any retained donor object system requires a boundary record stating source name/family, retained object rules, allowed use, prohibited generalization, normalized Astra outputs, assumptions rejected, required owner handoffs, promotion requirements, and quarantine/escalation notes.

## Required prohibitions

D09 blocks assumptions that all weapons use donor damage dice, all armor uses donor AC, all magic items use attunement, all rare items are purchasable, all cyberware causes humanity loss, all vehicles use hull points, all mechs use hardpoints, all drones use command caps, all crafting uses DCs/gold costs, all treasure maps to wealth, all relics are magical, all artifacts are combat upgrades, all consumables are safe if identified, and all rarity ladders map to Astra tiers.

## Acceptance criteria

A source-local object conversion is valid when it identifies donor construct type, decomposes bundled rules, assigns lawful outcome, records owner handoffs, states retained local rules, states prohibited generalizations, and escalates missing frameworks instead of inventing decorative doctrine.


---

<!-- FILE: D09-08_runtime_records_ui_and_owner_handoffs.md -->

# D09-08 Runtime Records, UI, and Owner Handoffs

## Purpose

This file defines how object-state is recorded without giving every minor object a full relic-grade record. It is doctrine-shape work, not final database schema.

## Core rule

D09 records object-state only at the depth needed to preserve identity, material, function, access, durability, danger, source-local boundaries, owner-file validation, and historical consequence. Record depth can increase or decrease as object consequence changes.

## Tiered Object Record Model

| Depth grade | Meaning |
|---|---|
| Abstract Supply | Non-individualized supply pool: food, rope, ammo, common spare parts, common reagents. |
| Stack / Batch Record | Similar objects tracked together by quantity, quality, source, or condition. |
| Simple Object | Individual object with basic identity, function, and condition. |
| Tracked Object | Specific object matters due to owner, damage, modification, access, or repeated use. |
| Functional Object | Meaningful access, durability, function, use limits, or owner handoffs. |
| Body-Integrated Object | Implant, prosthetic, graft, symbiote, cyberware, living gear, neural interface. |
| Platform Object | Vehicle, ship, mech, drone chassis, habitat, mobile base, external-body object. |
| Relic / Anchor Object | Relic status, anchor function, hidden state, dormancy, curse, route pressure, hosted state. |
| Intelligent Object | Hosts or expresses cognition/personhood/agency requiring D08 handoff. |
| Strategic Object | D10-controlled rarity, faction claim, legal restriction, strategic value, world consequence. |
| Source-local Object | Uses retained donor/campaign object rules. |
| Escalated Object | Current doctrine cannot classify safely. |

A ration stack should not resemble an artifact record. A damaged AI core should not be reduced to “loot.”

## Record families

D09 record families include object-state header; identity/material/function/access record; function-family record; relic/anchor/intelligent-object record; body-integrated object record; platform/external body record; object work/acquisition record; and source-local object conversion record.

Not every object uses every family.

## Durable record thresholds

A durable D09 record is required when an object has name/history/owner dispute/persistent identity; is relic, artifact, anchor, cursed, intelligent, strategic, or source-local; has hidden/dormant/conditional/damaged/evolving functions; has unusual access requirements; is body-integrated; is a platform; is dangerous/unstable/contaminated; carries D03 resources; gates D04 advancement; requires D05 work/operation; carries D06 route-linked functions; can cause D07 harm; hosts D08 actor-state; has D10 law/rarity/faction/requisition pressure; or may return later as historically significant.

No durable record is required for ordinary non-consequential gear, generic supplies, single-use mundane objects, unnamed ammunition, minor scrap, background objects, flavor-only treasure, fungible common materials, or temporary improvised tools with no consequence.

## Abstract supply, stack, and batch records

Abstract supply is used for broad supplies where individual identity does not matter: trail rations, common ammunition, rope supply, field repair supplies, common reagents, medical basics, low-grade fuel, ordinary salvage.

Stack/batch records are used when a group shares relevant traits: alchemical grenades from one batch, depleted drone batteries, cracked spirit crystals, restricted ammunition, starship-grade wiring, or questionable healing pills.

A stack item may be promoted if it becomes named, malfunctions consequentially, is cursed/contaminated, becomes evidence, is modified, becomes a catalyst, is stolen/disputed, has source-local special rules, or gains historical significance.

## Visibility states

D09 visibility states include visible, identified, partially identified, misidentified, hidden, concealed, disguised, dormant, sealed, dangerous unknown, source-local, destroyed/remnant, and retired/historical.

Hidden functions should be discoverable through D05 identification/research, D06 route sense, D07 symptoms, D08 actor interaction, D09 inspection, D10 records/social inquiry, or source-local methods.

## UI grouping

Recommended D09 UI groups: Equipped / Carried Gear; Weapons & Protection; Tools & Kits; Foci & Channels; Consumables & Charges; Materials & Components; Relics & Anchors; Intelligent / Actor-Hosting Objects; Implants & Body-Integrated Objects; Vehicles & Platforms; Crafting / Repair / Salvage Work; Requisition / Institutional Assets; Source-local Objects; Retired / Destroyed / Historical Objects; Hidden / Unknown Objects.

D10 may later add economy, legal, market, ownership, and faction views. D09 UI is object-state function only.

## Ownership, possession, custody, and usability

D09 tracks owned, possessed, custodied, loaned, issued, requisitioned, stolen, claimed, inherited, bonded, seized, abandoned, salvaged, illegal/restricted, and source-local relation states without owning D10 law.

Usability remains separate from ownership. A stolen gun may be usable. A legally inherited relic may refuse the heir.

## Promotion, demotion, destruction, and retirement

Object depth can change. Generic sword can become named. A potion batch can become dangerous. A ring can become a spirit anchor. Salvage can become a breakthrough catalyst. A drone can become an AI body. A stolen relic can trigger faction war.

Objects may be consumed, depleted, broken, dismantled, salvaged, burned out, severed, disenchanted-equivalent, anchor-destroyed, platform-destroyed, actor-hosting destroyed, or source-local destroyed.

Historical retention is required when destruction affects D03 resource state, D04 proof, D06 route state, D07 harm, D08 actor continuity, D10 world/social memory, source-local boundary, or later plot continuity.

## Handoff states

Handoff states are none, pending, resolved, blocked, dangerous, source-local, and escalated.

| Trigger | Required handoff |
|---|---|
| Charges, fuel, reservoir, reactor, shield resource, powered operation | D03 |
| Advancement catalyst, proof object, breakthrough gate, capstone object | D04 |
| Crafting, repair, surgery, piloting, operation, research, identification | D05 |
| Object-linked Techniques, Route Features, Principles, signature forms | D06 |
| Curse, contamination, rejection, backlash, malfunction injury, terminal failure | D07 |
| Intelligent object, AI core, spirit host, symbiote, body-integrated object, platform-as-body | D08 |
| Ownership, legality, rarity, market, faction claim, requisition, strategic scarcity | D10 |
| Donor object rules, equipment math, rarity ladder, attunement, vehicle stat block, crafting economy | Source-local / quarantine |
| Missing object framework | Escalation |

## Acceptance criteria

A runtime object record decision is valid when it assigns record depth, uses stack/batch/supply handling where appropriate, includes only necessary record families, assigns visibility and relation state, records handoffs, allows promotion/demotion/retirement/destruction/history, and avoids full records for ordinary inventory.


---

<!-- FILE: D09-09_integration_checklists_and_ddr_register.md -->

# D09-09 Integration Checklists and DDR Register

## Purpose

This file is the control ledger for the D09 doctrine pack. It consolidates accepted decisions, validates ownership boundaries, provides conversion/runtime checklists, and lists safeguards that must be preserved during conversion, canon consolidation, and later runtime design.

## Accepted decision register

### D09-LOSA — Layered Object-State Architecture

D09 uses Layered Object-State Architecture. Object-system construct is the broadest D09 term. Item, gear, weapon, armor, tool, relic, implant, prosthetic, vehicle, platform, ship, mech, drone, anchor, consumable, material, intelligent object, and source-local object are categories or interfaces beneath it. D09 owns object-state only. Object categories may overlap. Intelligent objects require D08 handoff. Source-local object systems normalize by function rather than direct import.

### D09-IMFA — Object Identity, Material, Function, and Access Layers

D09 uses Layered Identity / Material / Function / Access Model. Object identity states include generic, tracked, named, relic, artifact, consumable, material, platform, anchor, intelligent, and source-local objects. Uniqueness is separate from power. Material profile records type, durability, repair mode, compatibility, vulnerability, and rarity signal without final economy. Functions may be primary, secondary, hidden, dormant, conditional, damaged, or source-local. Access may require training, anatomy, interface, power, route, bond, attunement-equivalent, permission, rank, environment, or source-local rule. Ownership and usability are separate.

### D09-FAM — Weapons, Armor, Tools, Foci, Consumables, and Materials

D09 uses Functional Object Family Model. Weapons do not import donor damage math. Armor/protection does not import donor armor class, shield rules, damage reduction, defense ratings, or armor slots. Tools enable methods and do not automatically grant bonuses. Foci/channels require D03/D06/D07 handoffs. Consumables, materials, components, and catalysts are separated. Natural weapons and body-integrated tools require D08 handoff when body-state is implicated.

### D09-RAIO — Relics, Artifacts, Anchors, Intelligent Objects, and Object Personhood Interface

D09 uses Relic / Anchor / Intelligent Object Interface Model. Enhanced, imbued, relic, artifact, cursed/dangerous, intelligent, and anchor statuses are distinct and may overlap. Historical, mechanical, social, route, actor, world-state, and source-local significance are separate. Anchors may host/link actors, spirits, AI, souls, memories, curses, routes, powers, places, factions, or source-local states. Intelligent objects require D08 handoff. Recognition, refusal, dormancy, awakening, forced access, curse, backlash, corruption, and anchor destruction require owner validation.

### D09-BIO — Implants, Prosthetics, Cyberware, Biotech, Living Gear, and Body-Integrated Objects

D09 uses Body-Integrated Object Interface Model. Prosthetic, implant, cyberware, biotech, graft, living gear, symbiote, parasitic object, body-integrated weapon/tool, internal reservoir, and neural interface are distinct but overlapping object types. Integration mode and state are tracked. Compatibility is owner-validated. Augmentation burden uses signals rather than universal capacity/humanity/essence/slot limits. Living gear and symbiotes require D08 review when actor-state is implicated.

### D09-PLAT — Vehicles, Platforms, Ships, Mechs, Drones, and External Bodies

D09 uses Platform and External Body Interface Model. Vehicle, platform, and external body are distinct but overlapping. Platform records may track hull/frame, propulsion, power core, control interface, crew stations, cargo, weapons, armor/shields, sensors, life support, utility systems, AI/spirit/actor host, anchor/relic interface, and source-local systems. Crewed, autonomous, AI-assisted, bonded, living, remote-controlled, programmed, and possession-contested platforms require owner handoffs. D09 records condition and subsystem damage; D07 owns harm consequences.

### D09-WORK — Crafting, Repair, Salvage, Modification, Upgrade, and Requisition Interface

D09 uses Object Work and Acquisition Interface Model. Crafting, repair, maintenance, modification, upgrade, salvage, and requisition are distinct operations. Work states and repair depths are accepted. Inputs may include materials, components, catalysts, schematics, recipes, toolchains, facilities, labor, power, route permission, legal/faction permission, and source-local inputs. Upgrade paths are supported without universal item levels, hardpoints, enchantment slots, cyberware capacity, rarity ladders, or donor upgrade economies. Salvage records outputs, risks, actor-remains implications, and handoffs. Requisition is separated from purchase and crafting.

### D09-SLC — Source-local Object and Equipment Conversion

D09 uses Functional Object Conversion Routing. Every donor object construct requires a lawful outcome. Donor object bundles are decomposed across owner files. Retained donor systems require source-local boundary records. High-risk donor object assumptions are blocked. Treasure, salvage, crafting, and requisition are acquisition/object interfaces, not economy doctrine. Missing frameworks are quarantined or escalated.

### D09-RUNTIME — Runtime Records, UI, and Owner Handoffs

D09 uses Tiered Object Record Model. Record depths include abstract supply, stack/batch, simple, tracked, functional, body-integrated, platform, relic/anchor, intelligent, strategic, source-local, and escalated objects. Record families include object-state header, identity/material/function/access, function-family, relic/anchor/intelligent-object, body-integrated object, platform/external-body, object work/acquisition, and source-local conversion. Stack, batch, and abstract supply records are accepted. Ownership, possession, custody, issue, requisition, theft, claim, inheritance, bond, seizure, salvage, restriction, and usability remain separate. Object records may promote, demote, retire, be destroyed, or retain history.

## D09 ownership checklist

D09 owns object-state substrate. It does not own D03 Power Economy, D04 advancement proof, D05 competence/procedure, D06 route powers, D07 harm, D08 actor/personhood/body-state, D10 economy/law/faction/social authority, D11 narration, donor taxonomy as canon, or final database schema.

## Object-state checklist

Ask: Is this object, actor, body-state, power source, route feature, harm condition, social asset, faction asset, economy rule, source-local construct, or mixed case? Does it need persistent object-state? What identity/material/function/access applies? Does it carry hidden, dormant, conditional, dangerous, or source-local functions? Which owner-file handoffs apply? Does it need stack/batch/supply handling? Is it direct, normalized, source-local, quarantined, or escalated? What record depth is justified?

## Identity / material / function / access checklist

Check whether the object is generic, tracked, named, relic, artifact, consumable, material, platform, anchor, intelligent, source-local, or mixed. Keep uniqueness separate from power. Keep rarity signal separate from economy. Keep ownership separate from usability. Block donor slots, rarity ladders, attunement limits, and item economies.

Red flags: unique means powerful; rare means expensive; relic means magical; magic item means attunement; ownership means usable; usability means lawful possession.

## Functional object checklist

Check whether it is weapon, armor/protection, tool/instrument, focus/channel, consumable, material/component, catalyst, natural weapon interface, body-integrated object, or source-local function. Block donor weapon damage dice, donor armor class, tool-as-flat-bonus, focus-as-spellcasting-item, one-model consumables, and body capabilities converted into equipment.

## Relic / anchor / intelligent-object checklist

Check status, significance axes, anchor targets, anchor state, D08 intelligent-object handoff, personhood separation, recognition/refusal/bond/dormancy/awakening, forced access risks, ownership/usability separation, and source-local donor magic-item assumptions.

## Implant / body-integrated object checklist

Check integrated object type, integration mode, integration state, compatibility, D08 body/kinform/actor integration, D03 carrier/resource behavior, D06 route-linked functions, D05 installation/calibration/maintenance, D07 rejection/corruption/harm, D10 legality/stigma/faction control, and source-local augmentation assumptions.

## Platform / external-body checklist

Check vehicle/platform/external-body distinction, platform category, operation type, structure layers, condition, subsystem damage, D03 fuel/reactor/shield, D05 operation/repair, D06 maneuvers/route platforms, D08 AI/living/bonded/platform-as-body, D10 registry/docking/law/faction, and donor vehicle-system containment.

## Crafting / repair / salvage / requisition checklist

Check operation type, work state, repair depth, inputs, outputs, upgrade constraints, salvage source, actor-remains/taboo/contamination/ownership issues, requisition authority, and D03/D04/D05/D06/D07/D08/D10 handoffs. Block crafting DC import, treasure-as-economy, free salvage, requisition-as-purchase, pure-upgrade assumptions, field patch erasure, and actor remains treated as ordinary parts.

## Source-local object conversion checklist

For donor object systems, record donor label, construct type, function, D09 object-state parts, D03/D04/D05/D06/D07/D08/D10 parts, rejected assumptions, retained source-local rules, prohibited generalizations, promotion requirements, and lawful outcome.

Required prohibitions: all weapons use donor damage dice; all armor uses donor AC/defense; all magic items use attunement; all rare items are purchasable; all cyberware causes humanity loss; all vehicles use hull points; all mechs use hardpoints; all drones use command caps; all crafting uses DCs/gold; all treasure maps to wealth; all relics are magical; all artifacts are combat upgrades; all consumables are safe if identified; all rarity ladders map to Astra tiers.

## Runtime / UI checklist

Check record depth, record families, durable threshold, quantity/stack profile, visibility state, relation state, UI group, simplification, promotion, demotion, retirement, destruction, historical retention, owner handoff states, and source-local boundary visibility.

## Owner handoff matrix

| Trigger | Required handoff |
|---|---|
| Charges, fuel, reservoir, reactor, shield resource, powered operation, recharge, overdraw | D03 |
| Advancement catalyst, proof object, breakthrough gate, capstone object, transformation catalyst | D04 |
| Crafting, repair, surgery, piloting, operation, research, identification, tool use, engineering | D05 |
| Object-linked Techniques, Route Features, Principles, signature forms, route-linked crafting | D06 |
| Curse, contamination, rejection, backlash, malfunction injury, corruption, terminal failure | D07 |
| Intelligent object, AI core, spirit host, symbiote, body-integrated object, platform-as-body | D08 |
| Ownership, legality, rarity, market, faction claim, requisition, strategic scarcity, law | D10 |
| Donor object rules, equipment math, rarity ladder, attunement, vehicle stat block, crafting economy | Source-local / quarantine |
| Missing object framework | Escalation |

## Pre-generation risk queue

1. D09 becomes universal equipment owner. Fix: repeat object-state-only boundary.
2. Every object gets full record. Fix: tiered depth, abstract supply, stack/batch, durable thresholds.
3. Important objects are under-recorded. Fix: promotion, historical retention, and deep record thresholds.
4. Donor combat math leaks into weapons/armor. Fix: route combat math to source-local/later combat doctrine.
5. Magic-item assumptions become law. Fix: distinguish statuses and retain donor systems source-locally.
6. Cyberware/graft assumptions become law. Fix: use burden signals and owner handoffs.
7. Platforms import vehicle doctrine. Fix: D09 records platform-state; owners validate power, operation, harm, actor, social.
8. Crafting becomes economy doctrine. Fix: D09 records object work; D05 owns method; D10 owns economy/faction.
9. Relic significance collapses into power. Fix: preserve significance axes.
10. Intelligent objects are mishandled. Fix: require D08 for personhood/cognition/agency/continuity.
11. Salvage ignores actor-remains/taboo. Fix: require D08/D10/D07 review.
12. D10 economy/faction doctrine solved too early. Fix: D09 records scarcity/relation only; D10 owns law/economy/faction.

## Pack generation checklist

The D09 pack is complete when all D09 files from README through D09-09 and `D09_pack_manifest.json` exist and preserve these accepted decisions.


---

<!-- FILE: D09_pack_manifest.json -->

```json
{
  "pack": "D09 Object-State, Equipment, Relic, Platform, Crafting, and Source-local Object Architecture",
  "version": "v0.1",
  "generated_date": "2026-06-02",
  "status": "generated",
  "phase": "Astra Ascension native design doctrine",
  "primary_owner": "D09",
  "doctrine_files": [
    {
      "path": "D09-README_manifest.md"
    },
    {
      "path": "D09-00_layered_object_state_architecture.md"
    },
    {
      "path": "D09-01_identity_material_function_and_access_layers.md"
    },
    {
      "path": "D09-02_weapons_armor_tools_foci_consumables_and_materials.md"
    },
    {
      "path": "D09-03_relics_artifacts_anchors_intelligent_objects_and_personhood_interface.md"
    },
    {
      "path": "D09-04_implants_prosthetics_cyberware_biotech_living_gear_and_body_integrated_objects.md"
    },
    {
      "path": "D09-05_vehicles_platforms_ships_mechs_drones_and_external_bodies.md"
    },
    {
      "path": "D09-06_crafting_repair_salvage_modification_upgrade_and_requisition_interface.md"
    },
    {
      "path": "D09-07_source_local_object_and_equipment_conversion.md"
    },
    {
      "path": "D09-08_runtime_records_ui_and_owner_handoffs.md"
    },
    {
      "path": "D09-09_integration_checklists_and_ddr_register.md"
    }
  ],
  "owner_boundaries": {
    "D09_owns": [
      "object-state substrate",
      "object identity and category",
      "object record depth",
      "material profile and durability",
      "function category and access interface",
      "functional object family records",
      "relic/anchor/intelligent-object object-side records",
      "body-integrated object-side records",
      "platform/external-body object-side records",
      "object work/acquisition state",
      "source-local object conversion routing",
      "stack/batch/supply/visibility/handoff records"
    ],
    "D09_does_not_own": {
      "D03": "Power Economy, charges, fuel, reservoirs, recharge, overdraw",
      "D04": "advancement proof and gates",
      "D05": "crafting/repair/surgery/piloting/engineering/research competence",
      "D06": "Routes, Techniques, Principles, Feature Ledgers",
      "D07": "harm, curse, corruption, backlash, rejection, malfunction consequences",
      "D08": "actor-state, personhood, continuity, symbiote agency, body integration",
      "D10": "economy, ownership law, faction control, market, requisition, strategic scarcity",
      "D11": "narration behavior"
    }
  },
  "risk_fixes_embedded": [
    "object-state-only boundary",
    "tiered object record depth",
    "promotion/demotion/destruction/history rules",
    "donor combat math blocked",
    "magic-item assumptions source-local",
    "cyberware/graft assumptions source-local",
    "platform systems do not import donor vehicle doctrine",
    "crafting/salvage/treasure/requisition do not define economy",
    "relic significance separate from power",
    "intelligent objects require D08 handoff",
    "salvage preserves actor-remains and taboo pressure",
    "D10 economy/faction doctrine reserved for D10"
  ],
  "file_count_excluding_combined_export": 12
}
```
