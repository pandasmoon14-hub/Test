# Astra Starship and Vehicle Grammar v0.1

Derived from cross-donor consolidation after RHBF, Shadowrun, Lancer, and Starfinder.

## Scope of this file

This file owns Astra's **starship and vehicle grammar**.

It defines:
- what counts as a starship-family platform,
- what counts as a vehicle-family platform,
- how starships and vehicles differ from ordinary gear, personal-scale platforms, and generic platform doctrine,
- what object-side fields these families require,
- how travel-support, combat-support, crew-support, and cargo/support roles should be represented,
- how scale, persistence, and infrastructure relationship affect schema,
- and what remains optional-profile support or donor-local retention.

It does **not** own:
- full travel procedure,
- full tactical shell procedure,
- full access-law doctrine,
- exact donor ship-build math,
- exact donor combat phases,
- exact jump/Drift cosmologies,
- exact cargo/trade tables,
- exact manufacturer rosters,
- exact starship component catalogs,
- or exact world-generation systems.

This is a Batch C schema owner for starship and vehicle families, not a movement-procedure owner and not a donor catalog.

---

## Why this file exists

The donor set now proves that Astra cannot leave large mobile platforms as a vague extension of either:
- ordinary equipment,
- generic vehicle mention,
- or mech-specific platform doctrine.

Shadowrun proved that Astra must support:
- drones,
- vehicles,
- rigging/control-linked platforms,
- and technical/platform-adjacent object ecologies.

Lancer proved that Astra must support:
- chassis identity,
- mount/install distinction,
- operator/platform separation,
- and persistent platform records that matter independently of the operator.

Starfinder then proved that Astra must also support:
- starships as major platform families,
- broader vehicle breadth beyond mechs,
- shared mobile anchors,
- crewed large-scale platforms,
- and travel-support/campaign-support platform roles.

The stable conclusion is:

> Astra needs a dedicated owner for starship and vehicle family schema.  
> Generic platform grammar is no longer sufficient by itself.

---

## Core family law

Astra currently recognizes that **starships** and **vehicles** are both platform families, but they are not interchangeable and should not be flattened into one generic object class by default.

The stable rule is:

> A starship or vehicle record should be treated as a durable object-side owner when it has persistent identity, meaningful scale, transport or operational consequences, role-bearing support structure, or campaign-significant state beyond ordinary carried gear.

---

## Starship family

A **starship-family platform** is a large-scale mobile platform whose significance typically includes several of the following:
- transport across major distances or macro-nodes,
- shared support for multiple actors,
- docking or passage relationship to infrastructure,
- crew-role participation,
- significant travel enablement,
- combat or defense capability,
- cargo/support or logistical presence,
- and persistent campaign identity.

A starship is not just:
- a bigger car,
- a background scene prop,
- or a map transition device.

When a donor treats a ship as:
- base,
- transport,
- mission enabler,
- social location,
- deployment vector,
- or major target,

Astra should preserve it as a formal starship-family platform.

---

## Vehicle family

A **vehicle-family platform** is a mobile platform that is meaningful at a scale broader than ordinary carried gear but narrower, lighter, or less infrastructurally central than the typical starship family.

A vehicle may be:
- local or regional transit,
- tactical transport,
- combat-capable,
- support-capable,
- utility-focused,
- piloted,
- crewed,
- remotely operated,
- or semi-autonomous.

Vehicle-family schema matters because Astra must support platform breadth beyond:
- personal frames/mechs only,
- and full starships only.

The stable rule is:

> Vehicle-family doctrine exists so Astra can host multiple mobile platform scales without forcing everything upward into starships or downward into ordinary gear.

---

## Starships and vehicles are not the same as other doctrine owners

### Not ordinary gear
A ship or vehicle may carry gear, but it is not itself just a gear bundle.

### Not the operator
The operator, pilot, rigger, commander, crew member, or passenger remains distinct from the platform record.

### Not travel procedure
Travel procedure answers how transit happens.
This file answers what object-side schema starships and vehicles need.

### Not generic platform doctrine alone
Generic platform/installable doctrine still matters, but starships and vehicles now have enough recurring pressure to justify more explicit family ownership.

### Not tactical shell doctrine
A ship or vehicle may appear inside a shell.
The shell procedure still belongs elsewhere.

---

## Family distinctions

Astra should currently distinguish at least these family tiers.

### 1. Personal or close-support platforms
Smaller or more tightly operator-coupled platforms.
These may overlap with frames, powered armor, drones, or exo-support families.
They do not belong primarily to this file.

### 2. Vehicle-family platforms
Ground, aerial, aquatic, subterranean, or other tactical/regional mobility platforms.

### 3. Major transport/support platforms
Larger platforms that may carry multiple actors, cargo, escorts, or support functions without yet requiring full starship doctrine.

### 4. Starship-family platforms
Macro-node transit and campaign-support platforms with significant travel and infrastructure relationships.

These distinctions are schema-facing. Exact donor names remain donor-local.

---

## Required starship-family fields

A lawful Astra starship-family record should be able to identify at least the following where relevant:

- **identity**: what the ship is
- **class/family**: what kind of ship-family role it belongs to
- **scale**: what movement/support/combat scale it operates at
- **mobility/travel profile**: what kind of movement or passage it enables
- **anchor relationship**: whether it acts as a shared anchor, transport base, staging node, or support platform
- **crew support profile**: whether and how multiple roles interact with it
- **capacity structure**: what kind of mount/install/cargo/support capacity families matter
- **durability profile**: what damage/state layers or impairment logic matter
- **infrastructure relationship**: docking, passage, corridor, route, or network dependency
- **access relationship**: what permissions, clearances, or route rights may matter
- **cargo/support role**: whether it materially carries people, cargo, resources, or support functions
- **combat/support role**: whether it can defend, project, escort, or support operations
- **persistence state**: whether it remains a persistent campaign-side asset

Not every donor will use every field, but these are broad enough to host the current donor set.

---

## Required vehicle-family fields

A lawful Astra vehicle-family record should be able to identify at least the following where relevant:

- **identity**
- **class/family**
- **scale**
- **movement profile**
- **crew/operator profile**
- **capacity structure**
- **durability profile**
- **terrain or route dependency**
- **access/authorization dependency**
- **cargo/passenger/support role**
- **combat or utility role**
- **persistence state**

Vehicle-family records may be lighter than starship-family records, but they are still meaningful platform-side owners.

---

## Scale doctrine

Scale matters here, but Astra should not universalize one donor’s exact scales.

The important distinction is functional:

### Personal-support scale
Used directly with or around one actor or a very small team.

### Tactical mobility scale
Changes engagement, transport, support, or extraction inside one theater or route network.

### Regional mobility scale
Moves people or assets meaningfully across larger areas.

### Macro-node mobility scale
Moves between major nodes such as worlds, habitats, systems, or similarly separated infrastructures.

Starships are the clearest macro-node family currently supported.  
Vehicles most often live below that, though donor-local overlap may exist.

---

## Starship/vehicle roles

Astra should currently support at least these object-side roles.

### 1. Transport role
The platform’s main significance is moving people or goods.

### 2. Anchor/support role
The platform functions as a mobile base, staging point, or recurring support node.

### 3. Combat role
The platform is expected to survive or act under hostile conditions and may project force or defend others.

### 4. Escort/protection role
The platform matters because it carries, screens, or defends another actor, convoy, or route.

### 5. Utility/service role
The platform enables repair, salvage, scanning, recovery, towing, logistics, or similar support functions.

### 6. Exploration role
The platform exists to enable difficult travel, discovery, frontier support, or research-linked access.

One record may carry several roles. Exact donor role menus remain donor-local.

---

## Crew-support doctrine

Some large platforms require or strongly imply multiple actor roles.

Astra should preserve **crew-support profile** as a schema field rather than treating every ship/vehicle as:
- one pilot only,
- or a fully abstract party object.

Crew-support profile may indicate:
- solo operation,
- multi-role support,
- distributed task ownership,
- passenger vs operator distinction,
- support staff assumptions,
- or whether different action families matter while the platform is in use.

This file stops at the schema level.
The live procedure of crew-role action belongs in Batch B.

---

## Persistence doctrine

Not every ship or vehicle is a persistent campaign asset.

Astra should preserve the distinction between:
- temporary/opportunistic vehicles,
- recurring support vehicles,
- persistent owned/shared vehicles,
- mission-issued transports,
- and long-horizon campaign starships.

Persistence matters because it changes:
- upgrade pressure,
- maintenance relevance,
- anchor/support role,
- standing consequences,
- and operation planning.

---

## Platform capacities

Starships and vehicles may both care about capacity structure, but exact donors differ.

Astra should preserve the possibility that these families may have:
- output/mount-bearing capacity,
- subsystem/install-bearing capacity,
- cargo/passenger capacity,
- service/support capacity,
- docking or carried-asset capacity,
- route or fuel-support dependence,
- and maintenance burden.

The stable rule is:

> Starships and vehicles should be allowed to have multiple capacity families.  
> Exact donor slot math is not universal law.

---

## Durability and impairment

Starships and vehicles may carry durability profiles distinct from:
- personal bodies,
- mechs/frames,
- bonded objects,
- and ordinary gear.

Astra should preserve the possibility of:
- layered damage,
- subsystem impairment,
- mobility impairment,
- cargo/support degradation,
- partial failure,
- or threshold collapse.

But Astra should not yet universalize:
- one exact starship health structure,
- one exact shield or arc model,
- one exact structure/stress model,
- or one exact donor vehicle durability schema.

---

## Infrastructure relationship

A starship or vehicle record may depend on:
- ports,
- stations,
- roads,
- routes,
- docking systems,
- checkpoints,
- hangars,
- corridors,
- convoys,
- relays,
- passage networks,
- or support nodes.

This matters because some platforms are meaningful only in relation to available infrastructure.

The stable rule is:

> Starship/vehicle schema should remain aware of infrastructure relationship without collapsing into travel procedure.

---

## Travel and combat handoff boundaries

This file must remain clear about its handoffs.

### Travel handoff
- This file owns what sort of travel-support object the platform is.
- `transit_and_travel_infrastructure_v0_1.md` owns how passage and routes behave procedurally.

### Combat handoff
- This file owns what kind of object-side record a ship/vehicle has.
- `tactical_shell_doctrine_v0_1.md` and later procedure owners handle structured scenes and conflict.

### Access handoff
- This file may note that permissions matter.
- `access_and_authorization_grammar_v0_1.md` and `credential_and_access_assets_v0_1.md` own the actor-side and asset-side permission layers.

---

## Optional-profile support

The following are lawful recurring profiles, but not universal Astra schema law:

- shared starship as default campaign possession,
- one exact ship-role roster,
- one exact docking/fuel/support economy,
- one exact starship combat phase order,
- one exact vehicle handling subsystem,
- exact cargo/trade accounting,
- exact ship-upgrade trees,
- exact platform-tuning matrices as universal,
- exact powered-armor/vehicle/starship bridge assumptions,
- exact world-to-world passage costs or timings.

These may appear across donors, but should remain profile-level until broader confirmation.

---

## What remains donor-local

### Shadowrun donor-local
- exact rigging/drone/vehicle catalog structures,
- exact Matrix-linked vehicular assumptions,
- exact control and legality payload tied to donor systems.

### Lancer donor-local
- exact frame statistics when extrapolated upward,
- exact mount/install counts,
- exact structure/stress math,
- exact manufacturer and chassis payload assumptions.

### Starfinder donor-local
- exact BP/tier math,
- exact shield/arc/power-core structures,
- exact ship-combat turn structure,
- exact component catalogs,
- exact Drift-linked travel dependencies,
- exact Pact Worlds administrative framing.

### RHBF donor-local
- any world-assimilation or seal-framed travel assumptions when tied to exact donor cosmology.

---

## Design rules for Astra-facing starship/vehicle schema

1. Starships and vehicles must remain distinct from ordinary gear.
2. Starships and vehicles must remain distinct from operator records.
3. Starships and vehicles must remain aware of persistence, support role, and infrastructure relationship.
4. Crew-support profile should be allowed without forcing every platform into one crew model.
5. Capacity families should remain plural rather than one universal slot math.
6. Travel-support and combat-support roles should be visible without forcing one donor’s subsystem structure.
7. Macro-node transit platforms should remain distinguishable from smaller tactical/regional vehicles.
8. No one donor’s starship math or cosmology should become Astra baseline by default.

---

## Handoffs to other files

This file should hand off to:

- `platform_and_installable_asset_grammar_v0_1.md` for broader platform/installable object doctrine,
- `transit_and_travel_infrastructure_v0_1.md` for movement and route procedure,
- `tactical_shell_doctrine_v0_1.md` for ship/vehicle scene procedure,
- `access_and_authorization_grammar_v0_1.md` for permission/state logic,
- `credential_and_access_assets_v0_1.md` for docking/passage/route/authorization objects,
- `standing_scrutiny_and_trace_v0_1.md` for consequences tied to platform use or passage,
- `mixed_object_ecology_v0_1.md` for coexistence with magical, hybrid, bonded, and installed object families.

---

## Current Astra-facing summary

Astra now recognizes starship and vehicle families as stable platform-side schema owners.

It supports:
- persistent and temporary mobile platforms,
- multiple mobility scales,
- multiple platform roles,
- crew-support profiles,
- capacity families broader than one slot system,
- infrastructure-aware platform records,
- and clear handoffs to travel, access, and tactical procedure.

The final rule is simple:

> If a mobile object has persistent identity, meaningful scale, support or transport consequence, infrastructure relationship, or crew-facing significance, Astra should treat it as a starship/vehicle record rather than flattening it into generic gear or vague platform mention.
