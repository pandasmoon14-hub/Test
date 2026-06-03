<!-- BEGIN D15-README_manifest.md -->

# D15 — Faction, Relationship, Domain, and Institutional Operations Doctrine Pack

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## Purpose

D15 defines how Astra Ascension handles organized social operation: factions, institutions, relationships, debts, favors, obligations, claims, law authorities, guilds, sects, corporations, kingdoms, domains, player organizations, institutional access, public pressure, and social campaigns.

D15 answers the question: how do organized social structures operate, respond, escalate, decay, negotiate, claim, punish, support, and change posture over time without turning factions into arbitrary AI, universal clocks, or donor kingdom-turn systems?

## Pack contents

1. `D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md`
2. `D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md`
3. `D15-02_operation_creation_trigger_sources_scale_method_leverage_and_commitment.md`
4. `D15-03_operation_resolution_standing_shifts_pressure_lifecycle_and_consequence_routing.md`
5. `D15-04_operation_profiles_institutional_behavior_relationship_procedure_and_domain_operations.md`
6. `D15-05_institutional_capacity_concurrent_operations_pressure_movement_and_conflict.md`
7. `D15-06_source_local_faction_donor_institutional_mapping_quarantine_and_escalation.md`
8. `D15-07_records_not_final_schema_and_conversion_handoff_shapes.md`
9. `D15-09_integration_checklists_ddr_register_and_acceptance_criteria.md`
10. `D15_pack_manifest.json`

## Core architecture

D15 uses a Standing–Pressure–Operation Architecture:

```text
D10 records social/world state
  -> D15 identifies organized actor / relationship / domain pressure
  -> standing, pressure, obligation, claim, and capacity are reviewed
  -> Operation trigger is identified
  -> Operation scope, method, leverage, and cost are declared
  -> D12/D13/D17/D18/source-local handoff occurs when needed
  -> result changes standing, pressure, obligation, claim, access, treaty, law, territory, or domain posture
  -> D10 records resulting world-state delta
```

## Core D15 object families

- Organized Actor
- Standing
- Pressure
- Obligation / Claim
- Operation
- Operation Outcome
- Access Outcome
- Domain Posture
- Institutional Capacity / Operation Load
- Donor Institutional Mapping

## Binding non-ownership

D15 does not own D10 world-state storage, D17 economy procedure, D18 campaign pacing, D16 encounter/war construction, D12 immediate scene cadence, D13 Project intervals, D04/D05/D06 advancement/access/power implications, or final runtime schemas.

## Embedded risk controls

This pack embeds the full D15 pre-generation risk audit directly into the relevant files. The most important controls are:

- D15 does not become arbitrary faction AI.
- Organized actors are not giant NPCs.
- Standing is multi-axis, not a single reputation score.
- Faction clocks/tracks are not universal.
- Public belief is not actual truth.
- D15 domain control is not D06 domain expression.
- Player organizations are not free capability bundles.
- Contacts, favors, debts, obligations, ranks, guilds, sects, and patronage do not bypass owner-file doctrine.
- Source-local faction systems remain bounded unless reviewed.
- Record shapes are not final runtime schemas.


<!-- END D15-README_manifest.md -->


<!-- BEGIN D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md -->

# D15-00 — Faction, Relationship, Domain, and Institutional Operations Owner Boundaries

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Core question

How does Astra handle organized actors, relationships, obligations, institutional power, faction pressure, diplomacy, domain control, law, reputation, and social campaigns over time without turning factions into arbitrary AI, universal clocks, or donor kingdom-turn systems?

D15 is the doctrine layer for organized social operation. It governs how factions, institutions, relationships, debts, obligations, territorial claims, law authorities, guilds, sects, corporations, kingdoms, patron networks, player organizations, and domains act or respond through procedure.

## 2. Why this file exists

D10 records what the world remembers: factions, law, economy, relationships, reputation, hidden truth, rumors, unresolved pressure, and world-state queues. D12 defines scene cadence. D13 defines Projects and long-task intervals. D14 defines travel, territory crossing, route pressure, site entry, and discovery.

D15 defines how organized social structures operate on those records and pressures. Without D15, institutional behavior can drift into arbitrary model narration, faction clocks as hidden law, kingdom turns as campaign structure, or donor reputation scores as social truth.

## 3. Primary architecture

D15 uses a Standing–Pressure–Operation Architecture.

```text
social or institutional state exists in D10
  -> D15 identifies relevant organized actor or relationship structure
  -> standing / posture / obligation / pressure is reviewed
  -> operation trigger is identified
  -> operation scope and scale are set
  -> method, leverage, cost, and risk are declared
  -> D02 / D05 / D10 / D13 / D17 handoffs occur as needed
  -> result changes standing, pressure, obligation, access, treaty, law, or domain posture
  -> D10 records the world-state delta
```

## 4. What D15 owns

D15 owns the procedure by which organized social structures act or react.

D15 owns:

- faction action procedure;
- institutional operation procedure;
- relationship operation procedure;
- standing and posture changes as procedure;
- debts, favors, obligations, and claims as procedural objects;
- diplomacy and negotiation at institutional scale;
- treaties, pacts, accords, and agreements as institutional procedures;
- law authority operation;
- guild, sect, corporation, kingdom, order, agency, domain, and player-organization procedure;
- domain and territory operation;
- influence campaigns;
- social campaigns;
- faction conflict posture;
- institutional response;
- pressure decay and escalation procedure;
- D10 unresolved pressure operation;
- source-local faction and institutional systems.

## 5. What D15 must not own

D15 must not own:

- D02 resolution math;
- D03 resource pool definitions;
- D04 advancement gates or breakthroughs;
- D05 full method / skill taxonomy;
- D06 Technique, Principle, oath, or domain-expression mechanics;
- D07 harm, corruption, or injury consequences;
- D08 actor personhood and substrate doctrine;
- D09 object, relic, platform, or tool state;
- D10 world-state contents, hidden truth, public belief, rumor, or relationship records as stored facts;
- D11 presentation and hidden-state narration;
- D12 scene cadence;
- D13 Project interval procedure;
- D14 travel, territory crossing, discovery, or site entry;
- D16 opposition, encounter, hazard, patrol, raid, army, or war construction;
- D17 economy, acquisition, reward, requisition, licensing, ownership, market, value, and debt-value procedure;
- D18 campaign arcs, seasons, long-horizon pacing, state aging, state pruning, and domain evolution;
- runtime implementation;
- final faction, relationship, law, domain, or institution schema.

D15 may call or affect these owner files. It must not absorb them.

## 6. Donor-family pressures

D15 must survive pressure from many donor families.

D20/class-level donors pressure Astra toward reputation scores, faction ranks, downtime faction benefits, strongholds, patron rules, renown, guild access, and adventure faction rewards.

OSR/domain donors pressure Astra toward stronghold turns, domain income, hirelings, morale, reaction rolls, rulership, tax, law, wilderness claims, and faction-level consequences.

Narrative/tag donors pressure Astra toward clocks, fronts, threats, influence tracks, relationship tags, compels, player-authored facts, and faction moves.

Cyberpunk/skill-pool donors pressure Astra toward contacts, heat, legal exposure, corporate response, black markets, licenses, favors, reputation, surveillance, and institutional retaliation.

Lifepath/career donors pressure Astra toward service history, rank, patrons, debts, career institutions, mustering-out benefits, ship shares, legal status, and institutional obligations.

Cultivation/sect donors pressure Astra toward sect standing, contribution systems, master/disciple ties, clan politics, territory control, duels, sanctions, domain claims, and resource access.

Sci-fi/space donors pressure Astra toward polities, corporations, navies, stations, trade guilds, colonies, licenses, docking rights, fleet authority, and jurisdiction conflicts.

Horror/investigation donors pressure Astra toward secret societies, hidden cults, law suppression, rumor control, conspiracy pressure, institutional denial, and social paranoia.

Faction/kingdom games pressure Astra toward faction turns, asset turns, kingdom phases, domain actions, armies, projects, treaties, wars, and multi-scale political operation.

## 7. Core terms

### Organized Actor

An organized actor is a faction, institution, domain authority, guild, sect, corporation, polity, order, law office, patron network, crew organization, clan, cult, agency, movement, or player-created organization.

An organized actor is not automatically intelligent in the same way as an individual person. D08 owns actor/personhood. D15 owns institutional behavior and procedure.

### Standing

Standing is the relationship posture between an actor and another actor, faction, institution, domain, public, or legal body. Standing may include trust, respect, hostility, fear, debt, favor, scrutiny, legal status, access, patronage, obligation, rivalry, alliance, neutrality, reputation, and source-local standing.

Standing is multi-axis. It is not a single reputation score.

### Pressure

Pressure is unresolved social, institutional, legal, reputational, territorial, or factional force that may escalate, decay, surface, or transform.

D10 records pressure. D15 defines how it operates.

### Operation

An Operation is a faction, relationship, or institutional procedure that attempts to change social state.

Operations may be scene-scale, project-scale, institutional-scale, source-local, or campaign-scale. D15 defines operation grammar and hands off timing to D12, D13, or D18 as appropriate.

### Domain

A Domain is a controlled, claimed, administered, protected, contested, or symbolically bound social/institutional territory. D15 domain control must remain distinct from D06 domain-expression mechanics.

## 8. Anti-drift controls embedded in this file

- D15 does not become arbitrary faction AI. Significant institutional action requires a lawful trigger, initiator, target, goal, scale, method, leverage, cost/risk, and owner-file handoff.
- Organized actors are not giant NPCs. D08 owns personhood and actor substrate.
- Standing is multi-axis relational posture, not a single score.
- D10 owns stored world-state, public belief, hidden truth, rumor, law records, relationship records, and unresolved pressure queues.
- D15 domain control is not D06 domain expression.
- D15 may create conflict posture, but D12 owns immediate scene cadence, D16 later owns opposition/encounter construction, and D18 owns campaign-scale war pressure.

## 9. Acceptance criteria for D15-00

D15-00 is acceptable if it preserves clear owner boundaries, establishes Standing–Pressure–Operation as the architecture, rejects donor faction-law defaults, and gives every institutional construct a lawful path to mapping, source-local retention, quarantine, or escalation.


<!-- END D15-00_faction_relationship_domain_and_institutional_operations_owner_boundaries.md -->


<!-- BEGIN D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md -->

# D15-01 — Organized Actors, Standing, Pressure, Obligations, Claims, and Operation Anatomy

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file defines the operational objects D15 uses to handle institutional and relationship procedure without reducing factions to statblocks, clocks, or freeform narration.

D15 uses seven core operational objects:

1. Organized Actor
2. Standing
3. Pressure
4. Obligation / Claim
5. Operation
6. Domain Posture
7. Operation State

These are procedural objects, not final schemas.

## 2. Organized Actor

An Organized Actor is a structured social body capable of intention, policy, response, memory, access control, claim enforcement, or institutional behavior.

Examples include guilds, sects, corporations, kingdoms, polities, agencies, orders, cults, clans, families, crew organizations, academies, temples, law offices, patron networks, market authorities, station authorities, navies, rebel cells, criminal syndicates, player organizations, and source-local institutions.

D15 must not treat an organized actor as a giant individual person by default. D08 owns personhood and actor substrate. D15 owns institutional procedure.

An organized actor may have goals, posture, resources, territory, jurisdiction, standing relationships, obligations, claims, unresolved pressures, public face, hidden agenda, and source-local boundaries. D10 stores those facts. D15 operates on them.

## 3. Standing

Standing is the relational posture between two or more actors, institutions, publics, territories, or legal bodies.

Standing may be:

- trusted;
- favored;
- allied;
- patronized;
- neutral;
- watched;
- scrutinized;
- indebted;
- obligated;
- rivalrous;
- hostile;
- banned;
- wanted;
- protected;
- sponsored;
- licensed;
- recognized;
- source-local.

Standing supports multiple axes. A character may be trusted by one faction cell, legally wanted by a city, indebted to a patron, and respected by a rival sect at the same time.

Standing may be public, private, hidden, split by subgroup, conditional, temporary, revoked, transferred, or source-local. D15 must not collapse standing into one reputation score.

## 4. Pressure

Pressure is unresolved force that can surface, decay, escalate, transform, or become an Operation.

Examples include unpaid debt, owed favor, legal scrutiny, border violation, insulted patron, faction suspicion, rumor spread, treaty strain, guild sanction, sect challenge, corporate retaliation, territory dispute, domain instability, public unrest, and source-local threat.

Pressure may be:

- latent;
- active;
- escalating;
- decaying;
- suppressed;
- transferred;
- surfaced;
- converted_to_operation;
- converted_to_scene;
- converted_to_project;
- converted_to_conflict;
- resolved;
- retired;
- source-local.

D10 records unresolved pressure. D15 defines how it behaves procedurally.

## 5. Obligation / Claim

An Obligation is a duty, debt, vow, favor, contract, oath-like social burden, institutional expectation, treaty duty, patron demand, legal requirement, or source-local responsibility.

A Claim is an assertion of right, control, debt, territory, jurisdiction, ownership, access, authority, or grievance.

Examples include owed favors, unpaid debts, guild contracts, sect contributions, license requirements, territorial claims, legal warrants, treaty promises, patron summons, resource entitlements, salvage claims, domain rights, and source-local compacts.

D15 owns how obligations and claims are invoked, contested, enforced, transferred, settled, escalated, or retired. D17 owns economic ownership, value, payment, market, acquisition, and requisition. D10 owns stored world-state. D11 owns presentation.

### Obligation states

- owed
- invoked
- partially_paid
- paid
- deferred
- contested
- transferred
- forgiven
- defaulted
- escalated
- retired
- source-local

### Claim states

- asserted
- recognized
- contested
- rejected
- enforced
- suspended
- transferred
- settled
- violated
- escalated
- retired
- source-local

## 6. Operation

An Operation is a bounded institutional or relationship procedure that attempts to change social or institutional state.

Operation examples include negotiating alliance, settling debt, calling in favor, repairing standing, applying sanction, opening access, closing access, enforcing law, claiming territory, contesting jurisdiction, launching an influence campaign, suppressing rumor, exposing scandal, recruiting support, recognizing organization, protecting a member, retaliating, sponsoring a Project, mediating dispute, or source-local operation.

Every Operation identifies:

- initiator;
- target;
- goal;
- scale;
- method;
- leverage;
- cost;
- risk;
- standing affected;
- pressure affected;
- obligation or claim affected;
- owner-file handoffs;
- outcome state;
- source-local boundary if any.

## 7. Domain Posture

Domain Posture describes control, jurisdiction, access, claim, influence, instability, or contest over a territory, institution, route, market, resource, social space, spiritual territory, or source-local domain.

Examples include controlled, contested, claimed, occupied, restricted, protected, lawless, watched, unstable, hidden_control, shared_jurisdiction, and source-local.

D15 domain control must remain distinct from D06 domain-expression mechanics. A sect’s territory, a corporate zone, a trade route, and a spiritual domain claim may all be D15 domain posture; they do not automatically grant D06 power expression.

## 8. Operation State

Operations use lifecycle states rather than universal clocks.

Operation states:

- proposed
- ready
- active
- contested
- blocked
- delayed
- escalating
- decaying
- completed
- completed_with_cost
- partially_successful
- failed
- settled
- retired
- quarantined
- escalated
- source-local

Numeric tracks or clocks may be used only when source-local, owner-file supported, or later canonized.

## 9. Corpus-scale donor risk notes

Donor faction statblocks, clocks, front sheets, kingdom phases, rank ladders, reputation scores, heat tracks, guild benefits, sect contributions, patron favor economies, and organization trees are evidence. They are not Astra structures until mapped through D15 function and owner-file review.

## 10. Acceptance criteria

This file is acceptable if it gives D15 enough object anatomy to operate on social/institutional state while avoiding faction-statblock drift, reputation-score collapse, clock defaulting, and D06/D15 domain confusion.


<!-- END D15-01_organized_actors_standing_pressure_obligations_claims_and_operation_anatomy.md -->


<!-- BEGIN D15-02_operation_creation_trigger_sources_scale_method_leverage_and_commitment.md -->

# D15-02 — Operation Creation, Trigger Sources, Scale, Method, Leverage, and Commitment

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file defines how faction, relationship, institutional, law, access, claim, obligation, or domain Operations begin.

An Operation must not start merely because a narrator wants faction motion. D15 requires lawful setup before significant institutional state can change.

## 2. Operation setup procedure

D15 uses an eight-checkpoint setup procedure:

1. Trigger checkpoint
2. Initiator and target checkpoint
3. Operation goal checkpoint
4. Scale checkpoint
5. Method checkpoint
6. Leverage / authority checkpoint
7. Cost / risk / commitment checkpoint
8. Procedure handoff checkpoint

## 3. Trigger checkpoint

An Operation begins only when there is a lawful trigger.

Trigger sources may include:

- player request;
- player action creates social consequence;
- D10 unresolved pressure surfaces;
- faction or institution responds to prior state;
- debt, favor, obligation, or claim is invoked;
- law or jurisdiction is triggered;
- territory or domain posture is challenged;
- relationship standing changes enough to require procedure;
- D13 Project requires institutional support;
- D14 travel crosses controlled territory;
- D17 acquisition/requisition requires institutional access;
- source-local faction procedure activates;
- campaign-scale pressure calls for D18 handoff.

A faction should not act merely because something dramatic could happen.

## 4. Initiator and target checkpoint

Every Operation identifies the initiator and target.

Initiators may be player characters, player organizations, NPCs, factions, institutions, law authorities, patrons, guilds, sects, corporations, kingdoms, domain authorities, public groups, hidden organizations, or source-local actors.

Targets may be individual actors, groups, factions, institutions, public audiences, territories, law status, relationships, obligations, claims, resource access, routes, facilities, markets, domain posture, or source-local targets.

D15 must not assume all Operations are faction-versus-faction. Many are relationship, legal, public, institutional, or territorial procedures.

## 5. Operation goal checkpoint

An Operation must state the intended change. Valid goal types include:

- change standing;
- settle debt;
- invoke favor;
- create obligation;
- remove obligation;
- enforce claim;
- contest claim;
- open access;
- close access;
- gain license;
- repair reputation;
- suppress rumor;
- spread rumor;
- negotiate treaty;
- break treaty;
- sanction target;
- protect member;
- retaliate;
- claim territory;
- contest jurisdiction;
- stabilize domain posture;
- destabilize domain posture;
- support Project;
- block Project;
- shift law posture;
- source-local goal.

If no social or institutional state would change, the action may belong to D11 narration, D12 scene handling, D13 Project handling, or ordinary roleplay rather than D15.

## 6. Scale checkpoint

Operation scale bands:

- personal — affects one actor or narrow relationship;
- group — affects a party, crew, cell, household, squad, or small group;
- local — affects a location, district, facility, site, sect hall, station, or neighborhood;
- institutional — affects a formal organization, guild, law office, company, sect, order, or agency;
- territorial — affects land, route, market, jurisdiction, claimed domain, or controlled region;
- regional — affects multiple settlements, stations, branches, factions, or territories;
- campaign-scale — affects arcs, seasons, large polities, wars, migrations, or long-horizon world posture;
- source-local — bounded to a converted source procedure.

Scale determines review depth and handoffs. It is not a power rating by itself.

## 7. Method checkpoint

The Operation must identify how it is being attempted.

Method categories may include negotiation, diplomacy, threat, bribery, legal petition, public pressure, rumor campaign, favor exchange, debt settlement, service, sponsorship, coercion, espionage, infiltration, mediation, ritual/oath procedure, trade leverage, military pressure, resource denial, territory claim, bureaucratic process, or source-local method.

D05 owns method and competency relevance. D15 owns institutional operation structure.

## 8. Leverage / authority checkpoint

An Operation must identify what gives it force.

Leverage or authority may include standing, debt, favor, contract, treaty, legal jurisdiction, territorial claim, access tag, rank, license, patronage, resource control, information, public support, threat capacity, military capacity, economic dependency, religious/sect authority, domain posture, or source-local right.

Leverage can be contested, false, hidden, expired, illegal, source-local, or insufficient.

## 9. Cost / risk / commitment checkpoint

Before an Operation proceeds, the initiator commits visible costs and accepts visible risks when knowable.

Costs and risks may include favor spent, debt incurred, standing risked, public exposure, legal exposure, faction scrutiny, resource commitment, time, D13 Project commitment, D17 payment or requisition, relationship strain, retaliation risk, loss of neutrality, treaty strain, territorial escalation, hidden pressure surfacing, or source-local cost.

Hidden risks remain protected by D10/D11.

D15 should not allow “try institutional operation first, decide whether to pay later” unless an owner file or source-local rule supports it.

## 10. Procedure handoff checkpoint

D15 decides which procedure receives the Operation.

Possible handoffs:

- D12 focused scene or structured exchange for immediate negotiation, trial, confrontation, debate, threat, or social conflict;
- D13 Project for influence campaign, reputation repair, long negotiation, recruitment, propaganda, or institutional preparation;
- D15 operation interval for institutional procedure handled within D15;
- D17 acquisition/requisition for purchasing, permits, supply, bribes, licenses, or market access;
- D18 campaign-scale operation for war, long treaty arc, domain evolution, settlement development, or generational consequences;
- source-local procedure for bounded donor faction or domain systems;
- quarantine when owner support or evidence is missing;
- escalation when repeated or high-impact missing doctrine appears.

D15 should not force every Operation into faction turns.

## 11. Setup outcomes

Operation setup produces one of:

- ready_for_scene;
- ready_for_project;
- ready_for_operation_interval;
- ready_with_risk;
- blocked_pending_requirement;
- contested_before_start;
- source_local_retained;
- quarantined_pending_doctrine_or_evidence;
- escalated_owner_file_problem.

## 12. Anti-drift controls

- Significant faction action requires setup.
- Visible costs and risks commit before outcome when knowable.
- Leverage must be identified and may be contested.
- Institutional response must not be arbitrary.
- Hidden risks remain protected.
- Setup can route to D12, D13, D17, D18, source-local procedure, quarantine, or escalation.

## 13. Acceptance criteria

This file is acceptable if it can lawfully create institutional Operations from triggers while preserving actor/target/goal/scale/method/leverage/cost/handoff discipline and preventing arbitrary faction movement.


<!-- END D15-02_operation_creation_trigger_sources_scale_method_leverage_and_commitment.md -->


<!-- BEGIN D15-03_operation_resolution_standing_shifts_pressure_lifecycle_and_consequence_routing.md -->

# D15-03 — Operation Resolution, Standing Shifts, Pressure Lifecycle, and Consequence Routing

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file defines how Operations resolve after setup. It governs Operation outcomes, standing shifts, pressure movement, obligation and claim changes, access outcomes, and consequence routing.

D15 does not use binary success/failure or universal faction clocks as its default resolution model.

## 2. Resolution model

D15 uses an Operation Outcome and Pressure Routing Model.

An Operation may resolve through:

- D12 scene result;
- D13 Project result;
- D15 operation interval;
- D17 acquisition / requisition outcome;
- D18 campaign-scale handoff;
- source-local procedure;
- quarantine or escalation.

D15 does not require one universal Operation roll. It asks which procedure the Operation entered and routes the outcome back into standing, pressure, obligation, claim, access, treaty, law, territory, or domain posture.

## 3. Operation outcome states

Outcome states include:

- accepted;
- accepted_with_cost;
- partially_accepted;
- contested;
- delayed;
- countered;
- escalated;
- deescalated;
- converted_to_project;
- converted_to_scene;
- converted_to_conflict;
- settled;
- settled_with_debt;
- claim_recognized;
- claim_rejected;
- claim_contested;
- standing_improved;
- standing_damaged;
- access_opened;
- access_restricted;
- obligation_created;
- obligation_reduced;
- obligation_transferred;
- pressure_decayed;
- pressure_escalated;
- pressure_surfaced;
- failed;
- failed_with_consequence;
- quarantined;
- escalated_owner_file_problem;
- source_local_result.

These are procedural states. D10 records the resulting world-state. D11 presents it.

## 4. Standing shifts

Standing changes only when the Operation outcome justifies a state delta.

Standing shifts may be:

- improved;
- damaged;
- complicated;
- formalized;
- publicized;
- hidden;
- split_by_subgroup;
- conditional;
- temporary;
- revoked;
- transferred;
- source-local.

Examples:

- A guild publicly grants access but privately increases scrutiny.
- A sect elder accepts repayment but a rival faction treats the act as insult.
- A corporation opens market access only under license.
- A city drops charges but records the party as watched.
- A clan alliance improves standing with one branch and damages it with another.

D15 must support split standing. One faction is not always socially uniform.

## 5. Pressure lifecycle resolution

Pressure may move through these states:

- latent;
- active;
- escalating;
- decaying;
- suppressed;
- surfaced;
- transferred;
- converted_to_operation;
- converted_to_scene;
- converted_to_project;
- converted_to_conflict;
- resolved;
- retired;
- source-local.

Operation outcomes move pressure. A debt settlement may resolve one pressure but create a new obligation. A failed apology may escalate rumor pressure. A treaty may suppress conflict pressure without resolving underlying claims. A faction favor may transfer pressure from the party to a patron. A law petition may convert hidden scrutiny into public legal action.

## 6. Obligation and claim resolution

Obligations and claims do not disappear into flavor. They carry procedural states.

Obligation states:

- owed;
- invoked;
- partially_paid;
- paid;
- deferred;
- contested;
- transferred;
- forgiven;
- defaulted;
- escalated;
- retired;
- source-local.

Claim states:

- asserted;
- recognized;
- contested;
- rejected;
- enforced;
- suspended;
- transferred;
- settled;
- violated;
- escalated;
- retired;
- source-local.

## 7. Access and permission outcomes

Operations often affect access.

Access outcomes may include:

- access_granted;
- access_granted_with_limit;
- access_denied;
- access_revoked;
- license_required;
- sponsor_required;
- debt_required;
- standing_required;
- restricted_access;
- black_market_access;
- temporary_access;
- source-local_access.

D15 may record the operation of access. D17 owns acquisition, market, payment, requisition, license cost, and legality procedure where relevant. D10 stores the resulting state.

## 8. Partial outcomes

D15 treats partial outcomes as meaningful institutional movement.

Partial success may produce access with scrutiny, debt reduced but not cleared, rumor slowed but not killed, treaty accepted by one faction branch, legal charge deferred but not dismissed, standing improved privately but not publicly, domain claim recognized temporarily, favor granted with new obligation, project approved under oversight, or resource access granted with restriction.

Partial outcomes are critical for long campaigns because they prevent social play from becoming total success or total failure.

## 9. Consequence routing

D15 routes outcomes to owner files:

- D02 for contested resolution or uncertainty;
- D05 for method and competency implications;
- D07 for harm, coercion, sanctions with injury or condition consequences;
- D08 for actor/personhood issues when institutions affect persons, companions, or groups;
- D09 for objects, relics, platforms, facilities, or controlled assets;
- D10 for world-state, relationships, law, public belief, rumors, hidden truth, pressure queues;
- D11 for player-facing / GM-facing presentation and hidden-state boundaries;
- D12 for immediate scene, confrontation, chase, debate, conflict, or structured exchange;
- D13 for influence campaigns, reputation repair, treaty work, recruitment, institutional preparation;
- D17 for wealth, requisition, market access, licenses, bribes, debts, rewards, salvage claims;
- D18 for campaign-scale wars, seasons, domain evolution, state aging, arc pressure.

## 10. Anti-drift controls

- Public belief is not actual truth. D10 owns actual truth.
- D15 does not define generic consequences for all Operations.
- D15 does not use clocks as default operation resolution.
- D15 does not decide final harm, object, economy, hidden truth, scene cadence, campaign pacing, or runtime state by itself.

## 11. Acceptance criteria

This file is acceptable if D15 can resolve Operations through outcome states, move standing and pressure, track obligations/claims, route access outcomes, and hand off all non-D15 consequences to their owners.


<!-- END D15-03_operation_resolution_standing_shifts_pressure_lifecycle_and_consequence_routing.md -->


<!-- BEGIN D15-04_operation_profiles_institutional_behavior_relationship_procedure_and_domain_operations.md -->

# D15-04 — Operation Profiles, Institutional Behavior, Relationship Procedure, and Domain Operations

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file defines Operation Profiles: reusable procedure templates for common institutional and relationship operations.

Operation Profiles guide conversion and handoffs. They are not full subsystems, not faction AI, not law codes, not social combat rules, and not economy procedure.

Each profile includes purpose, triggers, initiators/targets, methods, leverage/authority, costs/risks, outcomes, pressure effects, standing/obligation/claim effects, handoffs, source-local risks, and escalation triggers.

## 2. Relationship Repair / Degradation Profile

Used when an actor attempts to improve, worsen, stabilize, formalize, or redefine standing with another actor, group, faction, institution, or public.

Common methods: apology, service, gift, public statement, private assurance, mediation, shared risk, favor repayment, damage control, slander, insult, betrayal, rumor campaign, source-local custom.

Common outcomes: standing_improved, standing_damaged, standing_complicated, standing_formalized, standing_temporary, standing_split_by_subgroup, obligation_created, pressure_decayed, pressure_escalated.

Primary handoffs: D05 for methods; D10 for relationships, public belief, rumors, hidden truth; D11 for presentation; D13 if interval-scale reputation work is required; D17 if gifts, payment, debt, or favors matter.

Boundary control: D15 must not decide loyalty, belief, emotion, or player/NPC interiority without owner support and state evidence.

## 3. Debt / Favor / Obligation Profile

Used when debts, favors, obligations, patron demands, contractual duties, sect contributions, guild expectations, treaty duties, or source-local burdens are created, invoked, settled, contested, transferred, forgiven, or defaulted.

Common methods: call in favor, settle payment, perform service, renegotiate term, contest validity, transfer debt, forgive obligation, default, invoke patron authority, source-local obligation rite.

Common outcomes: obligation_created, obligation_invoked, obligation_reduced, obligation_transferred, obligation_forgiven, obligation_defaulted, standing_improved, standing_damaged, pressure_escalated, access_opened.

Primary handoffs: D10 for obligations and relationship state; D17 for payment, requisition, debt value, market/legal access; D13 if service requires a Project; D11 for presentation.

Boundary control: D15 must not reduce all obligations to money.

## 4. Access / License / Permission Profile

Used when an actor seeks, loses, contests, grants, restricts, or enforces access.

Access may concern markets, guild services, sect libraries, restricted districts, ship docks, platform systems, training halls, legal permits, black markets, trade routes, resource sites, faction facilities, domain crossings, and source-local access.

Common outcomes: access_granted, access_granted_with_limit, access_denied, access_revoked, license_required, sponsor_required, standing_required, debt_required, black_market_access, temporary_access, restricted_access.

Primary handoffs: D10 for law/faction/standing/hidden restrictions; D17 for acquisition, licensing, market, requisition; D14 for route/territory crossing if access affects travel; D13 if preparation or service is required; D11 for presentation.

Boundary control: D15 must not convert every access problem into a price.

## 5. Diplomacy / Treaty / Pact Profile

Used for alliances, non-aggression pacts, trade agreements, sect agreements, patron contracts, ceasefires, prisoner exchanges, jurisdiction agreements, and formal settlements.

Common methods: negotiation, mediation, threat, mutual benefit, hostage/guarantee, public pledge, contract, oath-like procedure, resource exchange, third-party arbitration, source-local treaty custom.

Common outcomes: treaty_created, treaty_modified, treaty_rejected, treaty_breached, claim_settled, obligation_created, standing_formalized, pressure_suppressed, pressure_transferred, pressure_escalated.

Primary handoffs: D05 for method; D10 for treaty, public belief, law, hidden agendas; D13 if long negotiation is a Project; D17 for economic terms; D18 for campaign-scale treaty or war posture changes; D11 for presentation.

Boundary control: a single roll cannot rewrite large-scale political order without scale and owner review.

## 6. Law / Sanction / Enforcement Profile

Used when laws, warrants, bans, fines, exile, arrest, seizure, sanctions, institutional discipline, sect punishment, guild penalties, corporate enforcement, or jurisdictional action are invoked or contested.

Common methods: legal petition, trial, warrant, inspection, fine, seizure, ban, exile, sanction, disciplinary hearing, appeal, bribery, blackmail, jurisdiction challenge, source-local law procedure.

Common outcomes: legal_status_changed, standing_damaged, access_restricted, claim_enforced, claim_contested, pressure_surfaced, pressure_escalated, obligation_created, resource_or_asset_at_risk.

Primary handoffs: D10 for law, public belief, records, hidden truth; D12 for immediate scene/trial/confrontation; D13 for legal work as Project; D17 for fines, seizures, licenses, market access; D18 for large political consequences; D11 for presentation.

Boundary control: D15 does not import donor legal systems or moral assumptions as Astra law.

## 7. Influence / Rumor / Propaganda Profile

Used for public opinion, rumor control, social campaigns, reputation shifts, information suppression, propaganda, exposure, scandal, narrative counter-messaging, and institutional image.

Common methods: public performance, rumor spread, rumor suppression, evidence release, blackmail, counter-narrative, sponsorship, symbolic act, media/bulletin/herald network, sect proclamation, corporate PR, source-local influence custom.

Common outcomes: public_belief_shifted, rumor_created, rumor_suppressed, standing_publicized, standing_hidden, scrutiny_increased, pressure_decayed, pressure_escalated, hidden_truth_threatened.

Primary handoffs: D10 for public belief, rumors, hidden truth, information-state; D11 for presentation and misinformation boundaries; D13 if influence campaign is interval-scale; D15 institutional response; D17 if funding, media access, or bribes matter.

Boundary control: D15 must not treat public belief as truth.

## 8. Territorial / Domain Claim Profile

Used for land, routes, markets, resource sites, jurisdiction, ship/station authority, sect territory, spiritual territories, corporate zones, trade lanes, or domain posture.

Common methods: claim declaration, occupation, patrol, legal filing, treaty, resource control, symbolic assertion, military pressure, settlement, infrastructure, ritual boundary, trade control, source-local domain rite.

Common outcomes: claim_asserted, claim_recognized, claim_contested, claim_rejected, claim_enforced, domain_controlled, domain_contested, domain_unstable, access_restricted, pressure_escalated.

Primary handoffs: D10 for territory, law, faction state, world memory; D14 for travel/route/territory crossing; D17 for resources, trade, market, ownership, requisition; D18 for long-horizon domain evolution; D12/D16 if conflict or opposition emerges.

Boundary control: D15 domain control is distinct from D06 domain expression.

## 9. Patronage / Sponsorship / Recruitment Profile

Used when a faction or institution sponsors, recruits, protects, employs, mentors, binds, grants rank, recognizes, or absorbs an actor or group.

Common outcomes: sponsorship_created, protection_granted, rank_or_status_recognized, access_opened, obligation_created, standing_formalized, scrutiny_increased, rival_pressure_created.

Primary handoffs: D04/D05/D06 if training, access, route, or advancement gates are implicated; D10 for standing, obligations, institutional state; D13 if recruitment/training is a Project; D17 for payment, requisition, support, licenses; D11 for presentation.

Boundary control: patronage cannot bypass advancement or access doctrine.

## 10. Retaliation / Protection / Conflict Posture Profile

Used when an institution retaliates, threatens, protects, shields, sanctions, prepares for violence, escalates conflict, or de-escalates conflict.

Common outcomes: protection_declared, retaliation_prepared, threat_issued, sanction_applied, conflict_escalated, conflict_deescalated, pressure_converted_to_scene, pressure_converted_to_conflict, standing_damaged.

Primary handoffs: D10 for unresolved pressure and faction posture; D12 for immediate confrontation or conflict cadence; D13 for preparation Project; D16 for opposition/encounter construction later; D18 for campaign-scale war or arc pressure; D11 for presentation.

Boundary control: D15 must not become tactical encounter construction.

## 11. Player Organization / Institutional Growth Profile

Used when the party forms, grows, maintains, legitimizes, funds, relocates, reforms, or dissolves an organization.

Examples: crew, guild, sect branch, company, cult, mercenary band, trade network, academy, order, settlement council, ship crew command, source-local player institution.

Common outcomes: organization_recognized, organization_hidden, standing_created, access_opened, obligation_created, domain_claim_asserted, support_burden_created, maintenance_required, pressure_created.

Primary handoffs: D10 for organization state and world memory; D13 Projects for growth/maintenance; D17 for funding, support, requisition, assets; D18 for long-horizon organization evolution; D11 for presentation.

Boundary control: player organizations are not free capability bundles.

## 12. Source-local and escalation notes

Any donor-specific operation profile may remain source-local when useful, bounded, and unsafe to generalize. Repeated cross-family pressure should create canon candidate or doctrine escalation review, not automatic promotion.

## 13. Acceptance criteria

This file is acceptable if it covers the major institutional operation families while preserving owner boundaries and avoiding faction AI, law-code import, public-belief truth, domain-expression confusion, and player-organization free capability.


<!-- END D15-04_operation_profiles_institutional_behavior_relationship_procedure_and_domain_operations.md -->


<!-- BEGIN D15-05_institutional_capacity_concurrent_operations_pressure_movement_and_conflict.md -->

# D15-05 — Institutional Capacity, Concurrent Operations, Pressure Movement, and Conflict

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file prevents factions, institutions, relationships, and domains from acting with unlimited reach, perfect coordination, infinite attention, or arbitrary escalation.

D15 uses qualitative institutional capacity and Operation Load rather than universal faction action slots.

## 2. Core rule

An organized actor may operate only within its plausible reach, capacity, knowledge, access, jurisdiction, resources, relationships, and current pressure state.

Unsupported institutional action must be blocked, delayed, weakened, complicated, converted to a Project, made source-local, quarantined, or escalated.

## 3. Institutional capacity

Institutional capacity is the ability of an organized actor to sustain Operations.

Capacity may come from:

- personnel;
- authority;
- jurisdiction;
- territory;
- wealth;
- resources;
- infrastructure;
- information network;
- public legitimacy;
- legal status;
- military force;
- specialists;
- transport;
- communication;
- ritual / sect structure;
- corporate systems;
- patron network;
- source-local capacity.

Capacity may be constrained by:

- distance;
- limited agents;
- internal faction split;
- resource shortage;
- legal exposure;
- public scrutiny;
- rival pressure;
- domain instability;
- poor information;
- damaged infrastructure;
- ongoing obligations;
- campaign-scale disruption;
- source-local limits.

D15 does not create universal numeric capacity ratings at this stage.

## 4. Operation Load

Operation Load describes how much attention, authority, risk, or capacity an Operation occupies.

Operation Load may be created by:

- large scale;
- multiple targets;
- territorial distance;
- hidden operation;
- legal risk;
- resource commitment;
- public exposure;
- military mobilization;
- complex treaty work;
- domain maintenance;
- counter-operation pressure;
- need for specialists;
- source-local burden.

A small personal favor may create little load. A regional propaganda campaign, sect sanction, corporate blockade, legal purge, domain claim, or player-organization expansion may create major load.

## 5. Concurrent Operations

An organized actor may maintain multiple Operations only if capacity supports them.

Unsupported concurrency may cause:

- delay;
- weakened effect;
- cost increase;
- pressure exposure;
- internal strain;
- relationship damage;
- public scrutiny;
- counter-operation opening;
- operation split;
- operation failure;
- quarantine;
- escalation.

This applies to NPC factions and player organizations equally.

## 6. Pressure decay

Pressure may decay when:

- time passes without reinforcement;
- standing improves;
- debt is partially settled;
- rumor loses audience;
- legal attention is redirected;
- threat is suppressed;
- claim is recognized or abandoned;
- faction priorities shift;
- evidence disappears;
- public memory moves on;
- source-local condition expires.

D15 defines pressure movement procedure. D10 records pressure state. D18 later owns long-horizon aging and campaign-scale pruning.

## 7. Pressure escalation

Pressure may escalate when:

- ignored obligation persists;
- public insult spreads;
- territory is violated;
- law is defied;
- debt is defaulted;
- faction loses face;
- rival exploits delay;
- hidden truth surfaces;
- resource scarcity worsens;
- Operation fails with consequence;
- player action creates trace;
- source-local countdown advances.

Pressure escalation must be supported by state, source-local procedure, or owner-file pressure. It must not occur only because narration needs drama.

## 8. Institutional response timing

Institutions do not automatically respond instantly.

Response timing depends on:

- awareness;
- communication speed;
- jurisdiction;
- priority;
- capacity;
- distance;
- available agents;
- standing;
- legal authority;
- hidden agenda;
- source-local procedure;
- D10 unresolved pressure;
- D18 campaign-scale pacing.

D15 supports delayed, partial, mistaken, overbroad, suppressed, delegated, or source-local responses.

## 9. Organized actor conflict

Conflict between organized actors may involve diplomacy, sanctions, market pressure, information warfare, legal claims, proxy actors, territory dispute, resource denial, public legitimacy, covert action, military pressure, domain contest, or source-local conflict procedure.

D15 owns the institutional operation layer. It does not build tactical encounters, army combat, war rules, or campaign-season outcomes.

Handoffs:

- D12 for immediate confrontation, debate, trial, chase, or conflict scene;
- D13 for long influence campaigns, recruitment, repair, propaganda, preparation;
- D16 for opposition, encounter, hazard, patrol, raid, or threat construction later;
- D17 for economic pressure, requisition, sanctions, market access, supply;
- D18 for wars, seasons, domain evolution, campaign-scale consequences.

## 10. Player organizations

Player organizations use the same capacity and load doctrine as other organized actors.

A player organization may gain access, recognition, support, labor, territory, resources, contacts, legal status, protection, reputation, and source-local privileges.

It may also create maintenance burden, obligations, scrutiny, rivals, legal exposure, internal politics, resource demand, domain instability, public expectations, and campaign-scale pressure.

D15 rejects organization-as-free-capability-bundle.

## 11. Anti-drift controls

- Qualitative capacity is not a hidden action-slot system.
- Factions do not act everywhere at once.
- Institutions are not omniscient.
- Pressure does not escalate arbitrarily.
- Pressure may decay or retire.
- Player organizations follow the same burden rules as other organizations.
- D15 does not become D18 campaign pacing, D16 war construction, or D17 economy.

## 12. Acceptance criteria

This file is acceptable if it constrains organized actor operation without fixed faction turns, supports pressure movement, handles concurrent operations, and routes organized actor conflict to proper owner files.


<!-- END D15-05_institutional_capacity_concurrent_operations_pressure_movement_and_conflict.md -->


<!-- BEGIN D15-06_source_local_faction_donor_institutional_mapping_quarantine_and_escalation.md -->

# D15-06 — Source-Local Faction, Donor Institutional Mapping, Quarantine, and Escalation

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file defines how Astra converts donor faction, relationship, reputation, domain, kingdom, law, heat, contact, patron, guild, sect, corporation, and institutional systems without allowing donor social procedure to become universal Astra law.

Every donor institutional construct receives one lawful outcome:

- direct Astra mapping;
- normalized Astra mapping;
- source-local retained construct;
- quarantined construct pending later doctrine;
- escalated doctrine problem.

The donor label is evidence only. D15 maps function.

## 2. Functional donor institutional mapping ladder

Use this ladder for every donor faction, relationship, reputation, heat, domain, law, patron, guild, sect, or organization system:

1. Identify the donor procedure’s function.
2. Identify the social or institutional state it changes.
3. Identify the scale it assumes.
4. Identify the timing model it assumes.
5. Identify the leverage, access, authority, rank, or obligation structure it uses.
6. Identify what costs, risks, benefits, and consequences it controls.
7. Identify which Astra owner files are affected.
8. Decide lawful handling: direct, normalized, source-local, quarantine, or escalation.
9. Record rejected donor assumptions.

## 3. Direct Astra mapping

Use direct mapping only when the donor procedure already fits D15 without importing donor-specific social math, clocks, rank systems, faction turns, law codes, advancement assumptions, economy, or setting law.

Example: a donor rule says a public insult may worsen standing with a local guild and create a future demand for apology or restitution. This can map directly to D15 standing damage, pressure creation, and obligation/claim handling, with D10 recording state.

## 4. Normalized Astra mapping

Use normalized mapping when the donor system has a reusable social or institutional function, but donor packaging must be stripped.

Examples:

- A renown score becomes multi-axis standing, access, obligation, or reputation pressure; the exact score ladder is not Astra law.
- A heat track becomes social/legal/faction pressure with D10 unresolved pressure and D15 escalation/decay handling; the exact track is not universal.
- A faction turn becomes one or more D15 Operations or D18 campaign-scale handoff; it is not a default turn cycle.
- A sect contribution system becomes obligation, standing, access, patronage, training, or resource-access pressure; it does not become Astra advancement law.
- A kingdom action becomes territorial/domain Operation, D13 Project, D17 economy/requisition pressure, or D18 campaign-scale procedure; it is not a universal kingdom-turn system.

The function may survive. The donor track, score, clock, rank, phase, turn, or benefit tree does not become Astra law.

## 5. Source-local retained procedure

Use source-local retention when the donor institutional procedure is useful inside a converted source but unsafe to generalize.

Examples:

- a specific kingdom’s domain turn;
- a named guild’s renown ladder;
- a city’s heat table;
- a sect’s contribution exchange;
- a corporation’s internal rank benefits;
- a local law code;
- a campaign faction clock;
- a patron’s favor economy;
- a source-specific stronghold system;
- a local treaty procedure;
- a cult’s influence track.

The retained system must have an explicit boundary. It cannot become general Astra doctrine through polish, repetition, or familiarity.

## 6. Quarantine triggers

Quarantine donor institutional systems when any of the following prevents safe mapping:

- extraction damage blocks faction, relationship, rank, law, or clock procedure;
- missing source-local boundary;
- unclear state mutation;
- unsupported reputation, renown, or heat math;
- unsupported domain / kingdom turn assumptions;
- unsupported economy, requisition, tax, income, or payment model;
- unsupported organization benefit tree;
- unsupported patron benefit or advancement access;
- unsupported legal system or punishment model;
- unsupported social combat system;
- unsupported mass conflict / war procedure;
- unsupported public-belief or propaganda system;
- unsupported donor metaphysics, caste law, sect law, or setting law;
- missing D17 economy support;
- missing D18 campaign-scale support;
- missing D16 opposition/war/encounter support.

Quarantine preserves visible evidence and identifies the blocked owner file.

## 7. Escalation triggers

Escalate only when repeated or high-impact donor pressure exposes a real missing Astra distinction.

Examples:

- repeated donors require formal heat / scrutiny pressure doctrine beyond D10/D15 readiness;
- repeated faction-turn systems require a controlled operation-interval or campaign-season interface with D18;
- repeated sect/guild contribution systems require institutional access and obligation doctrine refined with D04/D05/D17;
- repeated player-organization systems require organization capacity and benefit-boundary doctrine beyond current D15 load rules;
- repeated domain/kingdom systems require a D18 long-horizon domain evolution layer;
- repeated public-opinion systems require richer public belief and rumor-state doctrine in D10/D11;
- repeated law systems require jurisdiction and enforcement doctrine that cannot remain source-local.

D15 escalates missing doctrine rather than solving it with Astra-sounding faction language.

## 8. Rejected donor assumptions

D15 rejects unsupported imports unless adopted by the correct owner file.

Rejected imports include:

- faction clocks as universal procedure;
- faction turns as default institutional timing;
- renown scores as universal standing;
- single reputation tracks as social truth;
- heat tracks as universal legal pressure;
- contact lists as free resources;
- guild rank as automatic capability;
- sect contribution as advancement law;
- patron benefits as free power grants;
- kingdom turns as campaign structure;
- domain actions as default territory control;
- stronghold systems as Astra baseline;
- law codes as setting-wide moral truth;
- corporate response tracks as universal institutional AI;
- public opinion tracks as actual truth;
- relationship tags as mind control;
- debt currencies as universal economy;
- player organization benefits as free capability bundles.

## 9. Clock-like and track-like institutional systems

Clock-like and track-like systems route by function:

- D10 unresolved pressure if they track social, legal, rumor, public belief, or faction pressure;
- D12 cadence if they surface into active confrontation, trial, negotiation, chase, or conflict;
- D13 Project if they represent interval-scale influence, reputation repair, recruitment, institution-building, or propaganda;
- D15 Operation if they represent bounded institutional action;
- D17 economy/acquisition if they track payment, requisition, market access, licenses, debt value, or resource control;
- D18 campaign pacing if they track wars, domain seasons, settlement growth, kingdom turns, arc pressure, or long-horizon evolution;
- source-local retained procedure if bounded;
- quarantine if owner-file support is missing;
- escalation if repeated pressure exposes missing doctrine.

A clock or track is a procedure shape, not authority.

## 10. Acceptance criteria

This file is acceptable if it maps donor institutional systems by function, preserves source-local systems safely, quarantines unsupported systems, escalates repeated/high-impact gaps, and records rejected donor assumptions.


<!-- END D15-06_source_local_faction_donor_institutional_mapping_quarantine_and_escalation.md -->


<!-- BEGIN D15-07_records_not_final_schema_and_conversion_handoff_shapes.md -->

# D15-07 — Records, Not-Final-Schema Shapes, and Conversion Handoff Controls

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Scope and warning

The record shapes in this file are **not final schema**. They are doctrine-facing and conversion-facing control shapes.

Runtime Gate B or later Batch C schema doctrine may replace or formalize them. These records do not create backend schemas, database tables, accepted canon, sourcebook prose, or live-play GM authority.

## 2. Organized Actor Operation Context Record

```yaml
organized_actor_operation_context_record:
  record_type: organized_actor_operation_context
  context_id: string
  organized_actor_ref: string
  actor_kind: faction | institution | guild | sect | corporation | polity | order | agency | movement | patron_network | law_authority | domain_authority | player_organization | source_local | mixed
  public_face_known: true | false | partial | unknown
  hidden_agenda_present: true | false | unknown
  capacity_summary: string
  jurisdiction_or_domain_refs: []
  standing_refs: []
  pressure_refs: []
  obligation_claim_refs: []
  source_local_boundary: string | null
  D10_state_owner: true
  D15_procedure_owner: true
  notes: string
```

## 3. Standing Record

```yaml
standing_record:
  record_type: standing
  standing_id: string
  subject_ref: string
  counterpart_ref: string
  standing_axes:
    - trust | respect | hostility | fear | debt | favor | scrutiny | legal_status | access | patronage | obligation | rivalry | alliance | neutrality | reputation | protection | license | source_local
  standing_state: trusted | favored | allied | patronized | neutral | watched | scrutinized | indebted | obligated | rivalrous | hostile | banned | wanted | protected | sponsored | licensed | recognized | source_local | mixed
  public_private_status: public | private | hidden | split | unknown
  subgroup_split_present: true | false | unknown
  temporary: true | false
  owner_file_handoffs: []
  D10_state_owner: true
  notes: string
```

## 4. Pressure Record

```yaml
pressure_record:
  record_type: institutional_pressure
  pressure_id: string
  pressure_family: debt | favor | legal_scrutiny | faction_suspicion | rumor | treaty_strain | sanction | territorial_claim | public_unrest | domain_instability | retaliation | patron_demand | source_local | other
  current_state: latent | active | escalating | decaying | suppressed | transferred | surfaced | converted_to_operation | converted_to_scene | converted_to_project | converted_to_conflict | resolved | retired | source_local
  origin_ref: string | null
  affected_refs: []
  trigger_conditions: []
  decay_conditions: []
  escalation_conditions: []
  owner_file_handoffs: []
  D10_state_owner: true
  notes: string
```

## 5. Obligation / Claim Record

```yaml
obligation_claim_record:
  record_type: obligation_or_claim
  record_id: string
  record_kind: obligation | claim | mixed
  obligation_state: owed | invoked | partially_paid | paid | deferred | contested | transferred | forgiven | defaulted | escalated | retired | source_local | not_applicable
  claim_state: asserted | recognized | contested | rejected | enforced | suspended | transferred | settled | violated | escalated | retired | source_local | not_applicable
  claimant_ref: string
  obligated_or_target_ref: string
  basis: favor | debt | contract | treaty | law | jurisdiction | territory | rank | license | patronage | resource_right | salvage_claim | source_local | other
  economic_component_present: true | false | unknown
  D17_handoff_required: true | false | unknown
  source_local_boundary: string | null
  notes: string
```

## 6. Operation Record

```yaml
operation_record:
  record_type: institutional_operation
  operation_id: string
  operation_profile: relationship_repair_degradation | debt_favor_obligation | access_license_permission | diplomacy_treaty_pact | law_sanction_enforcement | influence_rumor_propaganda | territorial_domain_claim | patronage_sponsorship_recruitment | retaliation_protection_conflict_posture | player_organization_growth | source_local | mixed
  initiator_ref: string
  target_refs: []
  goal_summary: string
  scale: personal | group | local | institutional | territorial | regional | campaign_scale | source_local
  method_summary: string
  leverage_or_authority_refs: []
  cost_risk_commitment_refs: []
  affected_standing_refs: []
  affected_pressure_refs: []
  affected_obligation_claim_refs: []
  affected_domain_posture_refs: []
  setup_outcome: ready_for_scene | ready_for_project | ready_for_operation_interval | ready_with_risk | blocked_pending_requirement | contested_before_start | source_local_retained | quarantined_pending_doctrine_or_evidence | escalated_owner_file_problem
  current_state: proposed | ready | active | contested | blocked | delayed | escalating | decaying | completed | completed_with_cost | partially_successful | failed | settled | retired | quarantined | escalated | source_local
  owner_file_handoffs: []
  source_local_boundary: string | null
  notes: string
```

## 7. Operation Outcome Record

```yaml
operation_outcome_record:
  record_type: operation_outcome
  outcome_id: string
  operation_ref: string
  outcome_state: accepted | accepted_with_cost | partially_accepted | contested | delayed | countered | escalated | deescalated | converted_to_project | converted_to_scene | converted_to_conflict | settled | settled_with_debt | claim_recognized | claim_rejected | claim_contested | standing_improved | standing_damaged | access_opened | access_restricted | obligation_created | obligation_reduced | obligation_transferred | pressure_decayed | pressure_escalated | pressure_surfaced | failed | failed_with_consequence | quarantined | escalated_owner_file_problem | source_local_result
  standing_shift_refs: []
  pressure_movement_refs: []
  obligation_claim_change_refs: []
  access_outcome_refs: []
  domain_posture_change_refs: []
  state_delta_owner: D10
  presentation_owner: D11
  owner_file_handoffs: []
  notes: string
```

## 8. Access Outcome Record

```yaml
access_outcome_record:
  record_type: access_outcome
  access_outcome_id: string
  operation_ref: string
  access_target_ref: string
  access_state: access_granted | access_granted_with_limit | access_denied | access_revoked | license_required | sponsor_required | debt_required | standing_required | restricted_access | black_market_access | temporary_access | source_local_access
  limit_or_condition_summary: string | null
  D17_handoff_required: true | false | unknown
  D10_state_owner: true
  source_local_boundary: string | null
  notes: string
```

## 9. Domain Posture Record

```yaml
domain_posture_record:
  record_type: domain_posture
  domain_posture_id: string
  domain_ref: string
  domain_kind: land | district | route | market | jurisdiction | station | ship | sect_territory | corporate_zone | resource_site | spiritual_domain | trade_lane | source_local | other
  posture_state: controlled | contested | claimed | occupied | restricted | protected | lawless | watched | unstable | hidden_control | shared_jurisdiction | source_local
  controlling_or_claiming_refs: []
  contested_by_refs: []
  D15_domain_control_not_D06_expression: true
  D14_route_or_territory_handoff_required: true | false | unknown
  D17_resource_or_market_handoff_required: true | false | unknown
  D18_long_horizon_handoff_required: true | false | unknown
  notes: string
```

## 10. Institutional Capacity / Operation Load Record

```yaml
institutional_capacity_operation_load_record:
  record_type: institutional_capacity_operation_load
  load_id: string
  organized_actor_ref: string
  operation_ref: string | null
  capacity_sources:
    - personnel | authority | jurisdiction | territory | wealth | resources | infrastructure | information_network | public_legitimacy | legal_status | military_force | specialists | transport | communication | patron_network | source_local_capacity
  capacity_constraints:
    - distance | limited_agents | internal_split | resource_shortage | legal_exposure | public_scrutiny | rival_pressure | domain_instability | poor_information | damaged_infrastructure | ongoing_obligation | campaign_disruption | source_local_limit
  operation_load_sources:
    - large_scale | multiple_targets | territorial_distance | hidden_operation | legal_risk | resource_commitment | public_exposure | military_mobilization | complex_treaty | domain_maintenance | counter_operation_pressure | specialist_need | source_local_burden
  concurrency_supported: true | false | unknown
  unsupported_concurrency_effect: delay | weakened_effect | cost_increase | pressure_exposure | internal_strain | relationship_damage | public_scrutiny | counter_opening | operation_split | operation_failure | quarantine | escalation | none
  notes: string
```

## 11. Donor Institutional Mapping Record

```yaml
donor_institutional_mapping_record:
  record_type: donor_institutional_mapping
  donor_label: string
  donor_function_summary: string
  donor_social_state_changed: []
  donor_scale_assumption: string | null
  donor_timing_assumption: string | null
  donor_track_or_clock_present: true | false
  mapped_d15_element: organized_actor | standing | pressure | obligation_claim | operation | domain_posture | operation_profile | capacity_load | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  stripped_donor_assumptions: []
  rejected_import_notes: []
  owner_file_handoffs: []
  source_local_boundary: string | null
  confidence: high | medium | low | blocked
```

## 12. Record use rules

- These shapes are not final schemas.
- Every record that touches stored social/world state must show D10 as state owner.
- Every economy, market, payment, license, requisition, value, or acquisition implication must identify D17 handoff.
- Every domain posture record must explicitly distinguish D15 domain control from D06 domain expression.
- Every source-local record must define its boundary.
- Donor institutional mapping must include rejected imports and confidence.

## 13. Acceptance criteria

This file is acceptable if it gives conversion and future runtime design auditable control shapes without pretending to finalize schema or backend implementation.


<!-- END D15-07_records_not_final_schema_and_conversion_handoff_shapes.md -->


<!-- BEGIN D15-09_integration_checklists_ddr_register_and_acceptance_criteria.md -->

# D15-09 — Integration Checklists, DDR Register, and Acceptance Criteria

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file provides the final D15 control layer: integration checks, anti-drift rules, source-local boundaries, escalation triggers, DDR register, and acceptance criteria.

## 2. Owner-file integration checklist

### D10 handoff checklist

D15 must hand off to D10 when an Operation affects:

- world-state;
- relationship state;
- law record;
- public belief;
- rumor;
- hidden truth;
- faction record;
- standing record as stored state;
- unresolved pressure queue;
- domain or territory state;
- source-local institutional fact.

D15 owns procedure. D10 owns stored truth and memory.

### D12 handoff checklist

D15 must hand off to D12 when an Operation becomes immediate scene procedure: confrontation, negotiation, trial, debate, chase, violence, public address, ambush, social conflict, or structured exchange.

### D13 handoff checklist

D15 must hand off to D13 when an Operation requires interval-scale work: influence campaign, reputation repair, recruitment, legal preparation, treaty work, propaganda, organization growth, domain preparation, or institutional support Project.

### D16 handoff checklist

D15 must hand off to D16 when institutional pressure creates opposition, encounter, hazard, patrol, raid, security force, war party, monster deployment, or threat construction.

### D17 handoff checklist

D15 must hand off to D17 when an Operation involves acquisition, ownership, value, payment, market access, license cost, requisition, debt value, bribe, reward, salvage claim, supply, or economy procedure.

### D18 handoff checklist

D15 must hand off to D18 when an Operation affects arcs, seasons, long-horizon domain evolution, player-organization aging, state pruning, campaign-scale war posture, settlement evolution, or generational continuity.

### D04/D05/D06 handoff checklist

D15 must hand off to D04/D05/D06 when patronage, rank, guild/sect access, recruitment, training, sponsorship, or institutional membership affects advancement gates, proof, competency, methods, access posture, Techniques, Principles, routes, or domain expression.

## 3. Source-local boundary checklist

A source-local institutional system must record:

- donor source or converted-source boundary;
- procedure retained;
- why it is useful locally;
- why it is unsafe to generalize;
- rejected donor assumptions;
- owner-file dependencies;
- lawful outcome;
- conditions for future escalation or canon candidate review.

Source-local systems do not become Astra law through repetition alone.

## 4. Escalation triggers

Escalate when repeated or high-impact pressure shows missing doctrine that cannot be safely normalized or retained locally.

Escalation examples:

- formal heat/scrutiny pressure beyond current D10/D15 readiness;
- faction-turn or campaign-season interface with D18;
- sect/guild contribution systems requiring access and obligation refinement with D04/D05/D17;
- player-organization capacity and benefit-boundary gaps;
- domain/kingdom long-horizon evolution needing D18;
- public-opinion systems requiring richer D10/D11 public belief and rumor-state doctrine;
- law systems requiring jurisdiction and enforcement doctrine beyond source-local treatment;
- mass conflict requiring D16/D18 coordination.

## 5. Quarantine triggers

Quarantine institutional systems when extraction damage, unclear mutation, missing source-local boundary, unsupported social math, unsupported reputation/heat/domain/economy/law/social-combat/mass-conflict/public-belief/organization-benefit assumptions, or missing owner-file support prevents safe mapping.

## 6. Anti-drift rules

- Do not turn factions into giant NPCs.
- Do not reduce standing to one reputation score.
- Do not make faction clocks, fronts, heat tracks, or kingdom turns universal.
- Do not make donor law codes Astra moral law.
- Do not treat public belief as actual truth.
- Do not let contacts, rank, guild access, patronage, or organization membership become free resources or powers.
- Do not let sect contribution, renown, or rank bypass D04/D05/D06 access or advancement doctrine.
- Do not let player organizations become free capability bundles.
- Do not let domain control become D06 domain expression.
- Do not let D15 become arbitrary faction AI.
- Do not let D15 become D17 economy doctrine, D16 encounter/war construction, or D18 campaign pacing.
- Do not let source-local institutional systems become Astra law through repetition alone.
- Do not treat not-final-schema record shapes as runtime implementation.

## 7. Hidden-state and public-belief checklist

D15 may alter public belief, rumor pressure, standing, and scrutiny. It must not turn public belief into actual truth.

D10 owns hidden truth. D11 owns presentation. D15 may record that an Operation threatens, obscures, exposes, suppresses, distorts, or publicizes information, but it does not reveal protected truth by itself.

## 8. DDR register

| Decision block | Locked architecture | Key rejection |
|---|---|---|
| D15-00 | Standing–Pressure–Operation Architecture | universal faction turns / arbitrary faction AI |
| D15-01 | operational object anatomy | faction statblocks / clock-first objects |
| D15-02 | eight-checkpoint Operation setup | faction action by fiat |
| D15-03 | Operation Outcome and Pressure Routing | binary check or clock-only resolution |
| D15-04 | Operation Profile model | full law/economy/domain subsystems inside D15 |
| D15-05 | qualitative capacity + Operation Load | fixed faction action slots |
| D15-06 | functional donor institutional mapping ladder | fixed equivalency table or preserve-by-default |
| D15-07 | not-final-schema record pack | final runtime/faction schema |

## 9. D15 acceptance criteria

D15 is acceptable only if it can:

- create an Operation from a lawful trigger;
- identify initiator, target, goal, scale, method, leverage, cost, and risk;
- represent standing as multi-axis relational posture;
- operate on D10-recorded unresolved pressure without replacing D10;
- track obligations and claims as first-class procedural objects;
- resolve Operations through outcome states rather than binary success/failure or universal clocks;
- route social, institutional, legal, factional, access, domain, and relationship outcomes to owner files;
- support relationship repair/degradation, debts/favors, access/licensing, diplomacy/treaties, law/sanctions, influence/rumor, territorial/domain claims, patronage/recruitment, retaliation/protection, and player organization growth;
- constrain factions and institutions through qualitative capacity and Operation Load;
- support pressure decay and escalation without arbitrary narration;
- support player organizations without free capability bundles;
- map donor institutional procedures by function, not label;
- preserve bounded source-local institutional systems;
- quarantine unsupported institutional systems;
- escalate repeated or high-impact missing doctrine;
- keep D15 domain control separate from D06 domain expression;
- keep public belief separate from actual truth;
- keep records clearly marked as not final schema.

## 10. Generation risk-fix embedding map

| Risk | Embedded locations |
|---|---|
| arbitrary faction AI | D15-00, D15-02, D15-05, D15-09 |
| factions as giant NPCs | D15-00, D15-01, D15-07, D15-09 |
| standing as single score | D15-01, D15-03, D15-07, D15-09 |
| clocks/tracks universalized | D15-01, D15-03, D15-06, D15-09 |
| D10 ownership stolen | D15-00, D15-03, D15-07, D15-09 |
| public belief as truth | D15-03, D15-04, D15-09 |
| donor law codes imported | D15-00, D15-04, D15-06, D15-09 |
| D15 domain vs D06 domain blur | D15-00, D15-01, D15-04, D15-07, D15-09 |
| rank/patronage bypasses advancement | D15-04, D15-06, D15-09 |
| player organizations as free bundles | D15-04, D15-05, D15-07, D15-09 |
| obligations collapse into economy | D15-01, D15-03, D15-04, D15-07, D15-09 |
| capacity becomes faction slots | D15-05, D15-07, D15-09 |
| D17 economy stolen | D15-00, D15-03, D15-04, D15-07, D15-09 |
| D18 campaign pacing stolen | D15-00, D15-04, D15-05, D15-09 |
| D16 encounter/war stolen | D15-04, D15-05, D15-09 |
| source-local systems generalize | D15-06, D15-07, D15-09 |
| records treated as runtime schemas | D15-07, D15_pack_manifest.json, D15-09 |


<!-- END D15-09_integration_checklists_ddr_register_and_acceptance_criteria.md -->

