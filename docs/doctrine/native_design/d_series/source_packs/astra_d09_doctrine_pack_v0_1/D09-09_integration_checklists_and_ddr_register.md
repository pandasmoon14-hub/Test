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
