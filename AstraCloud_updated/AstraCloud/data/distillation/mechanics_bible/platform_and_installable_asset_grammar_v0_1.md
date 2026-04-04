# Astra Platform and Installable Asset Grammar v0.1

Derived from cross-donor consolidation after RHBF, Shadowrun, and Lancer.

## Scope of this file

This file owns Astra's **platform and installable asset grammar**.

It defines:
- what a platform is,
- what an installable asset is,
- how platform records differ from operator records and from operation procedure,
- how mount-bearing, install-bearing, compatible, credentialed, and support-entity object classes are handled,
- how host-cost pressure and compatibility pressure should be represented,
- where deployables, support entities, and controller-linked assets belong,
- and what remains optional-profile support or donor-local retention.

It does **not** own:
- full operation procedure,
- full tactical shell doctrine,
- full access-law doctrine,
- full credential/permit object families,
- exact donor frame statistics,
- exact donor ware catalogs,
- exact donor manufacturer rosters,
- exact donor Matrix or platform-network metaphysics,
- exact donor reserve/repair numbers,
- or full faction/institution logic.

This is an object-side Batch C grammar owner, not a donor catalog and not a procedure owner.

---

## Why this file exists

The first three donors establish that Astra cannot treat all non-organic assets as one undifferentiated "equipment" mass.

RHBF proves that Astra must support:
- bonded objects,
- natural treasures,
- harvest-derived components,
- and progression-significant object classes distinct from ordinary gear.

Shadowrun proves that Astra must also support:
- augmentations,
- installed modifications,
- rated devices,
- credential-shaped assets,
- interface-sensitive objects,
- controlled or regulated technical assets,
- and controller-linked support entities.

Lancer proves that Astra must further support:
- platform-side records,
- chassis identity,
- weapon-bearing capacity distinct from install-bearing capacity,
- deployables and support entities as a middle zone,
- and hostile or allied platform grammars that are neither mere gear nor ordinary creatures.

The stable conclusion is:

> Astra needs an object-side grammar for platforms and installables that is distinct from operator build, distinct from operation procedure, and distinct from ordinary item doctrine.

---

## Core platform law

A **platform** is an object-side record that possesses meaningful operational identity beyond ordinary gear.

A platform may be:
- inhabited,
- piloted,
- remotely controlled,
- partially autonomous,
- fully autonomous,
- bonded,
- licensed,
- installed with subsystems,
- armed through mount-bearing capacity,
- or otherwise complex enough to require its own schema.

The stable rule is:

> A platform is not just an equipment bundle.  
> If an externalized object has durable identity, compatibility fields, capacity structure, or independent operational consequence, Astra should treat it as a platform-side record.

A platform record remains distinct from:
- the operator record,
- the operation loop,
- the tactical shell itself,
- and ordinary carried gear.

---

## Core installable-asset law

An **installable asset** is an object or modification that becomes meaningful through host relationship rather than through ordinary carried possession alone.

An installable asset may:
- occupy capacity,
- require compatibility,
- impose host cost,
- change identity or performance,
- unlock channels,
- alter allowed actions,
- modify durability or operation,
- or create new support functions.

The stable rule is:

> Installables are not just items that happen to be attached.  
> If a donor treats host relationship, compatibility, and cost/burden as structurally important, Astra should preserve that as installable-asset grammar.

Installables may attach to:
- bodies,
- platforms,
- chassis,
- mounts,
- channels,
- frames,
- sockets,
- infrastructures,
- or other lawful hosts.

---

## Platform is not the same as other object families

### Platform is not ordinary gear
Ordinary gear is carried, used, consumed, or wielded.
A platform is a durable object-side owner with meaningful record structure.

### Platform is not an operator
The operator may control, inhabit, authorize, or interface with the platform.
The platform still remains its own record.

### Platform is not operation procedure
Procedure answers how the platform is used in play.
This file answers what kind of object the platform is and what object-side fields it needs.

### Platform is not a creature by default
A platform may behave like an actor.
It is not automatically categorized as an organic creature or summoned being.
Classification belongs elsewhere.

### Installable is not a bonded object by default
A bonded object changes through relationship, attunement, or growth.
An installable changes a host through attachment or integration.
These families may overlap, but they are not identical by default.

### Installable is not a credential asset by default
Credential assets shape permission and identity.
Installables shape host state or function.
Some objects may do both, but the distinction matters.

---

## Recognized platform families

These are the current Astra-facing platform families.

### 1. Vehicle / frame / chassis platforms
These are durable externalized platforms with their own identity, capacity, and performance fields.

Lancer pressures this family most strongly.

They may include:
- frames,
- mechs,
- vehicles,
- combat platforms,
- exo-suits,
- carrier platforms,
- and comparable chassis-bearing systems.

### 2. Remote or delegated platforms
These are platforms operated through:
- remote control,
- delegated presence,
- mediated command,
- or indirect operator linkage.

Shadowrun pressures this family strongly.

### 3. Semi-autonomous or autonomous platforms
These are platforms with meaningful onboard logic, intelligence, or limited initiative structure.

Lancer pressures this through intelligent-platform profiles.
Shadowrun pressures adjacent support via drones and related systems.

### 4. Site-anchored or infrastructure platforms
These are fixed or semi-fixed platforms:
- nodes,
- relays,
- turrets,
- controlled gates,
- support towers,
- access frameworks,
- or comparable infrastructure-bearing systems.

These are lawful even if the current donor trio has not exhausted them yet.

### 5. Support-entity platforms
These are bounded middle-zone objects that are more than gear but less than full sovereign actor records.

They may include:
- deployables,
- drones,
- turrets,
- support pods,
- summoned devices,
- relay units,
- and comparable intermediate entities.

Lancer and Shadowrun jointly justify this family strongly.

---

## Recognized installable families

These are the current Astra-facing installable-asset families.

### 1. Bodily installables
These are installed into or onto a living or personal host.

Shadowrun pressures this family strongly.

They may affect:
- capability,
- durability,
- channels,
- perception,
- access,
- and identity.

### 2. Platform-side installables
These are installed into or onto a platform host.

Lancer pressures this family strongly.

They may affect:
- chassis function,
- install-bearing capacity,
- support capabilities,
- systems behavior,
- or platform-side operational profile.

### 3. Mount-linked assets
These are weapon-bearing or emitter-bearing objects that occupy dedicated offensive/active output capacity.

Lancer strongly validates that mount-bearing capacity is distinct from install-bearing capacity.

### 4. Channel/interface-linked assets
These are installables that modify or depend on a specific connection family, channel, or interface relationship.

Shadowrun pressures this family strongly.

### 5. Credential-carrying or access-shaped installables
Some installed or integrated assets materially affect permission, access, or recognized identity.
These may overlap with credential families but are not exhausted by them.

---

## Required platform fields

A lawful Astra platform record should be able to identify at least the following fields where relevant:

- **identity**: what platform this is
- **classification**: what category family it belongs to
- **hosted or standalone state**: whether it carries an operator, is remote, is autonomous, or is fixed
- **control relationship**: how control is established, delegated, or shared
- **compatibility fields**: what can interface with it
- **mount-bearing capacity**: what active/output bearing slots or equivalents it supports
- **install-bearing capacity**: what subsystem/support capacity it supports
- **durability profile**: what kinds of harm/state tracking apply
- **mobility or emplacement posture**: whether movement matters and how
- **support-entity relation**: whether it spawns, carries, or coordinates support entities
- **authorization dependence**: whether legal or access state matters to acquisition or use

Not every donor will use all fields, but these are broad enough to host the current donor set.

---

## Required installable fields

A lawful Astra installable record should be able to identify at least the following fields where relevant:

- **host family**: what kind of host accepts it
- **compatibility condition**: what is required for lawful installation
- **capacity usage**: what kind of host capacity it occupies
- **host-cost profile**: what burden, strain, displacement, or integration pressure it creates
- **effect domain**: what it changes in the host
- **authorization condition**: whether access, license, credential, or special state is required
- **removability state**: whether it is detachable, destructive, invasive, or persistent
- **interaction rules**: what other installs or bonded systems it conflicts with or supports

---

## Compatibility doctrine

Astra must preserve the difference between:

- **authorization**: whether an actor is allowed to acquire, use, or activate,
- **compatibility**: whether the host can receive or sustain the object,
- **control**: whether the actor can meaningfully direct it,
- **ownership**: whether the actor possesses it,
- **attunement/bond**: whether special relational linkage exists.

These may overlap in some donors, but they are not identical.

The stable rule is:

> A lawful object-side record may be ownable but incompatible, compatible but unauthorized, authorized but uncontrolled, or controlled through a host relationship that does not imply full ownership.

---

## Host-cost doctrine

Some installables impose meaningful burden on the host.

This burden may be represented through:
- bodily strain,
- capacity occupation,
- displacement of other installs,
- recovery cost,
- support upkeep,
- maintenance overhead,
- instability risk,
- identity alteration,
- or other host-side consequences.

Shadowrun proves host-cost pressure strongly.
Lancer proves capacity pressure and system occupation strongly.

The stable Astra rule is:

> Host cost is baseline doctrine.  
> Exact donor meters are not.

So Astra should preserve host-cost grammar without universalizing:
- one exact essence meter,
- one exact system-point chart,
- or one exact installation currency.

---

## Mount capacity versus install capacity

This distinction is now too strong to ignore.

### Mount capacity
Mount capacity owns:
- weapon-bearing,
- emitter-bearing,
- or output-bearing attachment positions.

It answers:
- what can be actively mounted for offensive or active projection.

### Install capacity
Install capacity owns:
- subsystem-bearing,
- support-bearing,
- utility-bearing,
- or passive/active internal augmentation positions.

It answers:
- what the host can meaningfully sustain as a subsystem/support layer.

The stable rule is:

> Mount capacity and install capacity must not collapse into one generic slot family by default.

---

## Support-entity middle zone

Astra now clearly needs a middle zone between:
- ordinary gear,
- subsystems fixed entirely inside a host,
- and full independent actors.

This middle zone includes:
- deployables,
- bounded drones,
- support units,
- turrets,
- relay entities,
- detachable support assets,
- and comparable limited-presence operational objects.

These support entities may have:
- partial autonomy,
- shared control,
- limited lifespan,
- host dependence,
- area-bound presence,
- or narrow objective scope.

The stable rule is:

> Support entities are object-side records in their own right, but they do not automatically become full sovereign actor classes.

---

## Controller-linked objects

Some platforms and support entities are meaningfully linked to:
- a pilot,
- a controller,
- a rigger,
- a command source,
- an authorized bearer,
- a bonded host,
- or an onboard intelligence.

Astra should preserve this controller-linked object grammar.

This matters because:
- platform operation may route through the controller,
- authorization may belong to one side while compatibility belongs to the other,
- and consequence may attach to either the operator, the platform, or both.

Object-side grammar stops here.
The actual procedure of control belongs to Batch B.

---

## Platform-side durability and state

A platform may have a durability profile distinct from:
- a personal body,
- a bonded relic,
- or an ordinary carried object.

Astra should preserve the possibility of:
- layered damage,
- subsystem degradation,
- operational impairment,
- threshold shifts,
- or multi-stage collapse.

But Astra should not yet universalize one donor's exact stress/structure law or one donor's exact armor/condition system as baseline.

---

## Optional-profile support

The following are lawful recurring profiles, but not universal Astra object law:

- single-scalar host-cost implementation,
- platform-tuning matrices,
- structure/stress durability profiles,
- intelligent-platform profiles,
- exact drone-rigger hierarchy models,
- exact manufacturer/faction-specific platform lines,
- exact install-capacity numbers,
- exact mount counts,
- exact deployable lifetimes,
- exact repair/reserve charts.

These should be supported, but not presented as universal baseline.

---

## What remains donor-local

### RHBF donor-local
- exact relic/treasure payload tables when treated as platform-adjacent object logic,
- exact world-assimilation object flavor,
- exact reserve-triplet payload semantics.

### Shadowrun donor-local
- exact Essence law,
- exact ware catalogs,
- exact drone and device catalogs,
- exact Matrix-host interface metaphysics,
- exact device-rating structures as universal default,
- exact permit-linked technical legality charts.

### Lancer donor-local
- exact frame statistics,
- exact manufacturer rosters,
- exact mount counts,
- exact system-point numbers,
- exact structure/stress math,
- exact NHP/cascade metaphysics,
- exact weapon/system catalogs.

---

## Design rules for Astra-facing platform/installable objects

1. A platform record must remain distinct from the operator record.
2. A platform record must remain distinct from operation procedure.
3. Compatibility, authorization, control, and ownership should not collapse by default.
4. Mount capacity and install capacity should remain distinct owners.
5. Host-cost grammar should be visible even when exact donor meters are not promoted.
6. Support entities should be able to exist in a bounded middle zone.
7. Installables should be able to attach to body, platform, or other lawful hosts.
8. Intelligent-platform logic should remain optional-profile support until wider donor pressure justifies more.
9. Donor catalogs should not outrank object grammar.

---

## Handoffs to other files

This file should hand off to:

- `layered_build_grammar_v0_1.md` for operator/platform build ownership,
- `access_and_authorization_grammar_v0_1.md` for actor-side permission and authorization,
- `credential_and_access_assets_v0_1.md` for credential-shaped object records,
- `tactical_shell_doctrine_v0_1.md` for scene-level use of platforms and support entities,
- `standing_scrutiny_and_trace_v0_1.md` for aftermath and exposure consequences,
- `astra_live_creatures_and_bound_relics_packet_v0_1.md` for broader Batch C umbrella grammar,
- `bound_relics_v0_1.md` for bonded-growth object families.

---

## Current Astra-facing summary

Astra now recognizes platform and installable asset grammar as a stable object-side doctrine family.

It supports:
- platform-side records,
- host relationships,
- compatibility fields,
- mount-bearing and install-bearing capacity,
- host-cost pressure,
- support-entity middle zones,
- and controller-linked object families.

The final rule is simple:

> If a donor gives an object durable identity, host dependence, capacity structure, compatibility pressure, or linked operational consequence, Astra should treat it as a platform/installable record rather than flattening it into ordinary gear.
