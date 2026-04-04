# batchA_06_access_tags_permissions_and_proficiency_gates.md

## Status
Draft — Core Now

## Authority
This file is the authoritative doctrine file for Astra's **access architecture, access tags, permission states, and proficiency gate logic**.

It defines:
- what access means in Astra doctrine,
- what kinds of lawful interaction may be gated,
- how access tags function,
- how gates evaluate lawful qualification,
- how proficiency gates differ from broader access rules,
- what access outcome states may exist,
- how access may be layered, delegated, contested, time-bounded, or revoked,
- and how donor access constructs are classified before conversion.

It does **not** define:
- practical capability or know-how,
- active ability object structure,
- resource cost, recharge, or backlash logic,
- condition or effect architecture,
- damage-family rules,
- progression architecture in full,
- or detailed package grants for paths, professions, ancestries, or backgrounds.

Those belong to other doctrine files.

---

## 1. Purpose

Astra requires a stable lawful-interaction layer.

Many donor systems distinguish between:
- being able to do something,
- being allowed to do something,
- being equipped to do something,
- being compatible with something,
- being recognized by something,
- and controlling or modifying something once access exists.

This file defines the doctrine that governs those distinctions.

Its purpose is to prevent later Astra files from collapsing **capability**, **access**, **ability**, **resource**, and **progression** into one undisciplined mass.

Astra therefore treats access as its own architecture: a structured layer of lawful qualification, gating, compatibility, authorization, attunement, and restriction that determines whether an interaction is permitted, blocked, limited, degraded, hazardous, or otherwise conditioned.

---

## 2. Scope Boundaries

### 2.1 This file must include
- access tags,
- gate structure,
- lawful qualification logic,
- proficiency gates,
- training-linked permissions,
- license and certification-like permissions,
- school, tradition, or domain-shaped gate constructs,
- armament and armor permissions,
- implant and biotech clearance,
- relic and attunement access,
- tool, platform, and interface access,
- scene, site, and trial-style gated access,
- access outcome states,
- access duration states,
- access contestability,
- and donor mapping rules for mixed permission constructs.

### 2.2 This file must not include
- practical capability lists or capability ratings in full,
- active ability definitions,
- resource expenditure and recharge systems,
- status/effect payload rules,
- damage-resolution logic,
- chargen sequencing,
- package-specific grant tables in full,
- or detailed progression-track formulas.

### 2.3 Interpretation rule
If a question asks **whether an actor, frame, system, crew, item, site, or other subject is lawfully qualified to use, equip, invoke, enter, command, maintain, modify, teach, transmit through, or otherwise interact with a gated object**, it belongs here.

If a question asks **how well the subject performs, what effect the interaction creates, how the cost is paid, or how the action resolves once invoked**, it belongs elsewhere.

### 2.4 Anti-collapse rule
Access is **not** capability.

Capability is **not** access.

Neither one is the same thing as an active ability object.

---

## 3. Core Access Principles

### 3.1 Access is lawful qualification
**Access** is the doctrinal layer that determines whether a subject is permitted, recognized, compatible, authorized, qualified, attuned, or otherwise allowed to perform a gated interaction with an object.

Access may govern whether a subject may:
- use,
- equip,
- invoke,
- enter,
- command,
- modify,
- maintain,
- teach,
- transmit,
- interface with,
- learn,
- install,
- attune to,
- or otherwise interact with a gated construct.

### 3.2 Access does not imply capability
A subject may be lawfully allowed to use something and still be poor at using it.

A subject may also possess the practical know-how to use something while lacking lawful or structural access to do so.

Astra therefore treats access and capability as separate layers even when donor systems blur them.

### 3.3 Access does not imply comprehension, mastery, or safe operation
Lawful or structural access does **not** automatically grant:
- interpretive knowledge,
- correct procedure recall,
- mastery,
- safe operation,
- awareness of hidden functions,
- or immunity from hazard, backlash, corruption, or misuse.

A subject may be recognized by a gate and still not understand how to use the object well, safely, or completely.

### 3.4 Access does not imply effect ownership
Having access to an object or subsystem does not by itself define the active effect payload that object produces.

The access layer answers **may this interaction occur?**

It does not answer **what exact effect occurs once it does?**

### 3.5 Access may be broader than one character sheet
Access may belong to or be mediated by:
- an individual actor,
- a player character,
- an NPC,
- a bonded companion,
- a vehicle or mech frame,
- a crew,
- a drone,
- an AI routine,
- a lineage,
- an institution,
- a site,
- a ward,
- an environmental structure,
- or another lawful access subject.

Astra therefore does not assume every gate is evaluated only against one humanoid personal sheet.

### 3.6 Access may be static or dynamic
Access may be:
- always available,
- conditionally available,
- temporarily granted,
- contested,
- revocable,
- time-bounded,
- upkeep-dependent,
- spoofed,
- inherited,
- or context-sensitive.

### 3.7 Passive benefit is not active control
Passive possession, passive presence, inherited benefit, or passive compatibility does **not** automatically grant:
- active invocation,
- command authority,
- advanced function access,
- modification rights,
- or teaching/transmission rights.

A subject may carry, wear, host, or benefit from a thing without lawfully controlling its deeper functions.

### 3.8 Access must survive multiple donor genres
Astra access architecture must remain lawful across fantasy, sci-fi, hybrid, cultivation, biotech, cyberware, relic, occult, factional, military, and tag-heavy donor systems.

This file therefore defines access by **function**, not by one donor's preferred noun.

---

## 4. Access Subject and Access Object

### 4.1 Access subject
The **access subject** is the entity, frame, structure, or system attempting or holding access.

Examples include:
- actor,
- player character,
- creature,
- summon,
- companion,
- mech frame,
- ship,
- crew,
- site,
- institution,
- AI process,
- ward,
- bonded lineage,
- or donor-local equivalents.

### 4.2 Access object
The **access object** is the thing being gated.

Examples include:
- item,
- weapon family,
- armor family,
- relic,
- implant,
- biotech construct,
- ritual,
- tradition,
- school,
- command channel,
- terminal,
- archive,
- location,
- trial,
- platform subsystem,
- sealed zone,
- donor-local interface,
- or an ability family where access law applies.

### 4.3 Subject-object distinction
Astra doctrine keeps the access subject and access object distinct.

This prevents the framework from treating all permission logic as if it were only a personal property of one actor, and it allows lawful modeling of shared systems, site-based permissions, inherited permissions, and nonpersonal gate mediation.

---

## 5. Access Tags and Gate Structure

### 5.1 Access tags
An **access tag** is a controlled rules-side marker used by gate logic.

An access tag:
- identifies a relevant access property,
- participates in lawful qualification checks,
- may belong to a subject, object, context, or interaction mode,
- and grants nothing by itself unless a gate rule says it matters.

### 5.2 Access tags are not metadata tags
Rules-side access tags are **not**:
- retrieval tags,
- doctrine tags,
- donor metadata tags,
- or general database annotations.

Those may exist elsewhere in Astra systems, but they are not access law.

### 5.3 Gate structure
A **gate** is the rule that checks whether access conditions are satisfied.

A gate may evaluate one or more of the following:
- required access tags,
- missing or prohibited tags,
- proficiency thresholds,
- training state,
- compatibility state,
- rank or progression prerequisites,
- possession or infrastructure requirements,
- context conditions,
- bond conditions,
- credential validity,
- active overrides,
- or donor-local lawful qualifiers.

### 5.4 Gate inputs and gate outputs
A gate receives inputs from the access subject, access object, and relevant context.

It produces an access outcome state, not the full effect payload.

### 5.5 Gate law must remain explicit
Astra doctrine does not permit hidden permission mush.

If access is gated, later files must be able to identify:
- what is checking access,
- what is being checked,
- what conditions matter,
- and what outcome state results.

---

## 6. Access Families

### 6.1 Training access
Access gained through instruction, drilling, initiation, handling qualification, operational schooling, or practice-based authorization.

This family answers questions like:
- has the subject been trained to lawfully operate this category,
- has the subject completed the required handling doctrine,
- or does the subject hold the relevant school or tradition training.

### 6.2 Qualification access
Access gained through formal requirements, certifications, ranks, prior unlocks, faction standing, procedural conditions, or validated credentials.

This family covers licenses, authorization chains, role clearance, and similar gate logic.

### 6.3 Attunement or compatibility access
Access gained because the subject is metaphysically, biologically, technologically, spiritually, or structurally compatible with the object.

This includes examples such as:
- relic resonance,
- implant compatibility,
- biotech tolerance,
- soul-pattern matching,
- chassis support,
- neural handshakes,
- donor-local symbiosis logic.

### 6.4 Possession or infrastructure access
Access gained because the subject possesses, hosts, controls, or is connected to the required object, platform, toolkit, node, frame, ritual environment, or support structure.

This does **not** automatically imply capability or advanced control rights.

### 6.5 Contextual access
Access gained or denied based on location, scene state, environmental condition, encounter state, timing window, ritual phase, security posture, or other contextual factors.

### 6.6 Bonded or inherited access
Access gained because of bond, oath, lineage, pact, crew identity, inherited pattern, authorized succession, or other durable relationship structure.

### 6.7 Temporary or override access
Access gained through short-term authorization, emergency mode, spoofed credentials, temporary key, hacked clearance, override token, borrowed privilege, or similar limited grant.

Temporary access remains lawful doctrine even when the fiction treats it as illicit or unstable.

### 6.8 Prohibited or quarantined access
Access may also be structured around active rejection states such as:
- blacklisting,
- quarantine,
- banned compatibility,
- revoked standing,
- cursed lockout,
- unsafe interface rejection,
- or donor-local exclusion structures.

These are not just absences of permission; they are explicit negative access states.

---

## 7. Proficiency Gates and Handling Tiers

### 7.1 Proficiency gate definition
A **proficiency gate** is a specific kind of access rule that checks whether a subject has the required trained handling level, operational qualification, or lawful familiarity needed to use an object or interaction type without restriction.

### 7.2 Proficiency gate is narrower than total access law
A proficiency gate is one part of access architecture.

It does not replace broader gate logic such as:
- certification,
- compatibility,
- attunement,
- rank prerequisites,
- site authorization,
- or command authority.

### 7.3 Handling tiers
Astra permits access law to distinguish between multiple handling states, such as:
- unqualified,
- minimally qualified,
- standard qualified,
- advanced qualified,
- specialist qualified,
- or donor-local equivalent bands.

The exact numerical or band structure belongs to the relevant subsystem, but the doctrine permits more than binary yes/no handling law.

### 7.4 Proficiency does not imply command or modification
A subject may be proficient enough to use or equip an object while lacking the rights to:
- command,
- reconfigure,
- alter permissions,
- maintain advanced systems,
- teach restricted procedures,
- or access hidden modes.

---

## 8. Gate Outcome States and Access Duration

### 8.1 Core outcome states
A gate may produce outcomes such as:
- allowed,
- denied,
- partial,
- restricted,
- degraded,
- revoked,
- forbidden,
- hazardous,
- concealed,
- conditional,
- or donor-local lawful equivalents.

### 8.2 Partial and restricted access
Partial or restricted access means the subject may interact with the object in some lawful ways but not others.

This may include distinctions such as:
- use but not command,
- enter but not modify,
- equip but not fully invoke,
- read but not transmit,
- operate basic functions but not advanced functions.

### 8.3 Degraded access
Degraded access means the subject is recognized as having some valid pathway, but the interaction occurs with reduced safety, reduced fidelity, reduced authority, or increased constraint.

### 8.4 Forbidden and hazardous access
Astra distinguishes blocked access from **forbidden** or **hazardous** access.

A forbidden state means the system actively rejects or prohibits the interaction.

A hazardous state means access may technically occur but creates danger, corruption, backlash, tracking, instability, contamination, or other harmful consequence.

### 8.5 Concealed access
A subject may possess lawful access while lacking awareness of that fact, lacking the correct trigger sequence, or lacking interpretive knowledge needed to express it properly.

Likewise, an object may conceal that it is accessible at all.

### 8.6 Duration states
Access may be:
- persistent,
- temporary,
- single-use,
- expiring,
- upkeep-dependent,
- scene-bound,
- session-bound,
- phase-bound,
- or donor-local in duration logic.

### 8.7 Revocation and collapse
Access may be revoked, suspended, invalidated, or collapsed when:
- credentials change,
- a bond breaks,
- the subject loses compatibility,
- required infrastructure is removed,
- context expires,
- a blacklist is applied,
- or another gate condition fails.

### 8.8 Contested access
Access itself may be contested.

A gate may be:
- resisted,
- interrupted,
- traced,
- spoofed,
- challenged,
- countermanded,
- defended,
- or otherwise forced into active adjudication.

When this occurs, the access layer interfaces with the resolution framework without ceasing to be access law.

---

## 9. Multi-Part and Layered Access

### 9.1 Access may require multiple conditions
Astra recognizes that many access objects require more than one independent qualifier.

Examples include combinations such as:
- tradition plus attunement,
- implant clearance plus body compatibility,
- command authority plus live platform presence,
- lineage claim plus relic recognition,
- role credential plus secure channel validation.

### 9.2 Layered gate logic
A single interaction may involve multiple layers of access, including:
- baseline legality,
- trained handling,
- advanced-mode authorization,
- modification rights,
- maintenance rights,
- transmission rights,
- or donor-local secondary permissions.

### 9.3 Authority chains
Astra permits one-to-many and many-to-one access structures.

This includes cases where:
- one credential unlocks a family of objects,
- one object requires multiple authorities,
- a crew or bonded group jointly holds access,
- a lineage mediates access for descendants,
- or a site grants nested levels of authority.

### 9.4 Interaction-type distinction
Access may differ by interaction type.

Lawful gate logic may distinguish between rights to:
- use,
- equip,
- invoke,
- enter,
- command,
- modify,
- maintain,
- teach,
- transmit,
- install,
- bind,
- or detach.

Astra does not flatten all of those into one yes/no state.

---

## 10. Shared, Delegated, Platform, and System-Mediated Access

### 10.1 Individual access
Access may belong directly to one actor or entity.

### 10.2 Shared access
Access may be shared across:
- crews,
- bonded groups,
- institutions,
- households,
- factions,
- command cells,
- or donor-local collectives.

### 10.3 Delegated access
Access may be delegated temporarily or conditionally from one subject to another.

Delegation does not necessarily transfer every interaction right or every duration state.

### 10.4 Platform-bound access
Some access belongs primarily to a frame, vehicle, mech, drone, ship, terminal, ritual platform, or support environment rather than the baseline actor.

### 10.5 System-mediated access
An AI routine, security lattice, bonded ward, inherited protocol, or institutional system may hold, evaluate, or broker access on behalf of others.

### 10.6 External and nonhuman mediation
Astra explicitly permits nonhuman and nonpersonal access mediation.

Drones, AI processes, wards, sites, bonded lineages, environmental structures, and other nonpersonal subjects may hold or express access states if the donor or Astra subsystem supports it.

---

## 11. Scene, Location, and Trial-Style Access

### 11.1 Site access
Locations, archives, vaults, sanctums, portals, terminals, command bridges, trial spaces, and sealed environments may themselves be gated access objects.

### 11.2 Scene-state access
Some access only exists during a particular scene condition, ritual phase, security posture, environmental state, or narrative window.

### 11.3 Trial-style access
A donor may structure access around trials, tiers, sectors, floors, sanctified chambers, challenge gates, or other place-based progression checks.

Astra recognizes this as a lawful site-access pattern, not as proof that all access is just progression in disguise.

### 11.4 Entry does not imply deeper authority
A subject may gain lawful entry to a place while lacking authority to:
- modify it,
- extract from it,
- command it,
- activate its deeper systems,
- or inherit rights within it.

---

## 12. Nonstandard and Compressed Access Expressions

### 12.1 Reduced expressions are lawful
Not every subject requires the full player-facing access expression.

NPCs, hazards, creatures, drones, vehicles, sites, institutions, summons, and environmental systems may use reduced, compressed, bundled, or inferred access models so long as they map lawfully back into the same architecture.

### 12.2 Compression must remain interpretable
A compressed access expression must still permit later doctrine to answer, at minimum:
- what kind of access is being represented,
- what object is being gated,
- and what outcome state applies.

### 12.3 Compression does not erase distinctions
Even when access is bundled for convenience, Astra should not silently collapse:
- capability into access,
- access into control,
- passive benefit into active invocation,
- or compatibility into mastery.

---

## 13. Donor Mapping Rules

### 13.1 Donor labels are not accepted without classification
When a donor uses terms such as:
- domain,
- school,
- tradition,
- license,
- rite,
- attunement,
- command rank,
- authorization,
- proficiency,
- access level,
- bond,
- or clearance,
Astra must first classify what job the construct is actually doing.

### 13.2 Classification questions
Before converting a donor access construct, ask:
1. What is the access subject?
2. What is the access object?
3. What interaction type is being gated?
4. Is the rule checking training, compatibility, authorization, context, bond, infrastructure, or something else?
5. Is the gate binary, banded, layered, or contested?
6. Is the access persistent, temporary, revocable, or hazardous?
7. Does the construct also contain capability or ability logic that must be split out?

### 13.3 Split mixed constructs when necessary
If a donor construct simultaneously does multiple jobs, Astra must split it rather than importing it whole.

Examples of mixed jobs include:
- practical know-how plus lawful permission,
- access plus active effect payload,
- progression requirement plus command authority,
- compatibility plus mastery,
- or site entry plus deeper subsystem control.

### 13.4 Domain-like donor constructs
A donor may use a term like **domain** as an all-purpose marker for school, field, alignment, access, and activation law.

Astra must not assume such a term becomes the whole doctrine layer.

If a domain-like construct survives conversion, it survives only with a disciplined, explicit job inside the broader access architecture.

### 13.5 Progression-linked gates
Rank, tier, lineage stage, cultivation stage, or similar progression constructs may participate in access law, but they do not replace access architecture.

They are one possible gate input, not the whole doctrine.

---

## 14. Explicit Exclusions and Downstream Ownership

This file does **not** define:
- how practical capability is rated or cataloged in full (`batchA_05`),
- the structure of active ability objects (`batchA_07`),
- resource cost, recharge, and backlash systems (`batchA_07b`),
- condition and effect architecture (`batchA_08`),
- damage and resistance taxonomy (`batchA_09`),
- or progression axes in full (`batchA_10`).

This file may reference those layers when explaining gate inputs or ownership boundaries, but it does not absorb their doctrine.

---

## 15. Core Doctrine Summary

Astra access doctrine rests on the following non-negotiable rules:

1. Access is its own lawful interaction layer.
2. Access is not capability.
3. Access is not the same thing as an active ability object.
4. Access does not automatically grant comprehension, mastery, or safe operation.
5. Passive possession does not automatically grant active control.
6. Gates may be layered, contested, spoofed, revocable, hazardous, or time-bounded.
7. Access rights may differ by interaction type.
8. Access may belong to individuals, crews, systems, lineages, frames, sites, institutions, or other nonhuman subjects.
9. Mixed donor constructs must be split when they do more than one doctrinal job.
10. Astra converts donor access logic into explicit access law rather than importing donor metaphysics whole.

