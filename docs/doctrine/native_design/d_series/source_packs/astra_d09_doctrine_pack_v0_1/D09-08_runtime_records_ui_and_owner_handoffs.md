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
