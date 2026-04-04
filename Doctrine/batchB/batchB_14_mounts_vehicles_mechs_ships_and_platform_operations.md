# batchB_14_mounts_vehicles_mechs_ships_and_platform_operations.md

## Purpose and authority

This file defines Astra Ascension doctrine for **operational frames, stations, subsystems, and platform-bound services**.

Batch B14 exists to provide a conversion-stable framework for any construct whose primary job is to transport, shelter, position, empower, deploy, or operationally organize one or more occupants through space, conflict, work, access, or service use.

This file is authoritative for:
- operational frame taxonomy;
- frame scale classes;
- frame, occupant, station, subsystem, and service separation;
- control topology and crew-friction doctrine;
- locomotion state versus operational state;
- transfer states such as mounting, embarkation, docking, boarding, launch, and ejection;
- frame-state, degradation, and subsystem-failure doctrine;
- service and payload outputs of frames and platforms;
- dominant-function boundaries between operational frames, auxiliaries, and settlement-scale constructs.

This file is **not** authoritative for:
- general traversal and routefinding procedure, which belongs to `batchB_06_exploration_travel_navigation_time_and_distance.md`;
- auxiliary-entity doctrine, which belongs to `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md`;
- item ontology or generic equipment schema, which belongs to `batchB_03_equipment_item_and_gear_object_model.md`;
- crafting, repair, modification, or installation procedure in general, which belongs to `batchB_05_crafting_salvage_repair_modification_and_installation.md`;
- organized access law, legitimacy, and service gatekeeping in general, which belongs to `batchB_12_factions_institutions_clearance_and_service_access.md`;
- settlement governance, civic infrastructure, district logic, and macro-operations, which belongs to `batchB_15_settlements_bases_capitals_and_infrastructure_operations.md`;
- body-state survivability doctrine, which belongs to `batchB_02_health_injury_healing_death_and_recovery_framework.md`.

This file should be read as a doctrine for **how operational frames function**, not as a catalog of vehicles, mounts, ships, or mechs.

---

## Scope boundaries

B14 covers constructs whose dominant function is one or more of the following:
- transport of riders, passengers, crew, or cargo;
- provision of shelter, protection, or deployment environment;
- alteration of occupant mobility, reach, firepower, sensor range, or access profile;
- provision of station-bound services, support systems, or operational outputs;
- mediation of embarkation, boarding, docking, launch, or transfer;
- operation as a mobile or fixed platform through which other actions become possible.

B14 does **not** assume that every frame is combat-oriented. A caravan, orbital shuttle, shrine barge, siege engine, walking fortress, submarine, mech, starship, station ring, or teleporter hub can all be operational frames or frame-adjacent constructs if their dominant function is operational rather than purely civic, social, or informational.

B14 should remain doctrine-first and conversion-stable. It must not silently import one donor system's assumptions about initiative, crew load, subsystem granularity, or boarding cadence as universal Astra law.

---

## Core operational-frame principles

### 1. An operational frame is not merely movement
A frame may move, but movement is only one possible output. Frames can also shelter, scan, deploy, dock, board, carry, repair, command, intimidate, or provide protected access.

### 2. Occupancy is not control
Being aboard, mounted, embarked, or sheltered inside a frame does not automatically mean controlling it.

### 3. Control is not throughput
Operating a frame may alter action bandwidth, but it does not erase command burden, crew burden, role contention, station opportunity cost, or subsystem bottlenecks unless the donor construct explicitly does so.

### 4. Platform identity is not donor flavor
Horse, cart, skiff, tank, battle mech, shuttle, frigate, orbital station, walking city, or portal cradle are donor surface labels. Astra doctrine classifies them by dominant function, scale, control topology, subsystem load, and service output.

### 5. Hybrid constructs require dominant-function classification
Some constructs pressure more than one Batch B file. B14 must classify them by dominant operational role, then explicitly hand off secondary concerns to neighboring files.

---

## Core nouns

### Frame
The mount, vehicle, mech, ship, platform, or infrastructure body that provides the operational environment.

### Occupant
Any rider, pilot, driver, handler, crew member, passenger, gunner, engineer, boarder, escort, or remote operator using or located within the frame.

### Station
A role-bearing position, interface point, or operational post from which an occupant affects the frame or its outputs.

### Subsystem
A distinct functional component or operational grouping inside a frame, such as propulsion, steering, sensors, hardpoints, docking clamps, stables, shielding, lift systems, comms, life support, cargo rigging, or maintenance systems.

### Service
A persistent or temporary output that the frame makes available, such as transport, shelter, scanning, cargo handling, deployment, docking, repair support, fire support, life support, mediation, or command support.

### Frame state
The current operational condition of the frame as a whole.

### Transfer state
The current relationship governing movement between bodies, frames, stations, platforms, and environments.

---

## Frame-family taxonomy

B14 recognizes the following top-level operational frame families.

### 1. Mount
A living or quasi-living conveyance whose primary operational relationship is rider-linked or handler-linked.

Typical pressures:
- saddled or harnessed use;
- rider control or partial rider control;
- creature-like locomotion;
- cargo or passenger load;
- barding or protective outfitting;
- role overlap with B13 when the same construct is also an auxiliary entity.

### 2. Vehicle
A nonliving conveyance or machine frame with one or more operators, a propulsion model, and an operational body.

Typical pressures:
- driver or pilot control;
- heading, traction, drift, or momentum;
- crew/passenger separation;
- cargo handling;
- structural durability and subsystem stress.

### 3. Mech
A personal or squad-scale operational frame that changes the user's embodied capability set rather than merely carrying them.

Typical pressures:
- pilot/frame coupling;
- hardpoints, limbs, frame-specific mobility;
- frame-specific deployment and recovery;
- pilot skill versus frame capacity distinction;
- alternate body logic without fully replacing the pilot as primary actor.

### 4. Ship or vessel
A crewed operational frame whose primary doctrine pressures include multi-role crew operation, long-range transport, boarding, docking, subsystem partition, and sustained operational environment.

Typical pressures:
- bridge or cockpit roles;
- engineering, sensors, weapons, navigation, comms, or command roles;
- passenger and cargo separation;
- boarding and shipboard internal movement;
- life support, pressure, gravity, or sealed-environment implications.

### 5. Platform
A fixed, semi-mobile, or mobile operational environment whose users interact with stations, systems, services, and access points rather than merely riding it.

Typical pressures:
- station logic;
- district or compartment structure;
- docking/launch/entry points;
- service-bearing environment;
- civic or military overlap;
- hybridization with B15 when the platform also serves as habitation or infrastructure shell.

### 6. Operational transit infrastructure
A frame-adjacent construct whose dominant job is routing, docking, launching, transferring, or controlling movement rather than simply being a vehicle or settlement.

Examples of doctrine pressure:
- docks;
- gates;
- teleporter hubs;
- launch cradles;
- hangars;
- embarkation platforms;
- lock systems;
- transit rings;
- controlled boarding bridges.

This class exists because many donors treat operational routing infrastructure as mechanically significant without making it a vehicle in its own right.

---

## Frame-scale doctrine

Operational frames should be classified by scale as well as family.

### Personal frame
One primary user or rider, possibly plus minimal cargo or one additional occupant.

### Squad frame
A small tactical frame carrying a small team or supporting a tightly bounded combat/work unit.

### Convoy frame
A linked or coordinated set of transports, mounts, or vehicles whose operational meaning depends on movement and mutual support across several bodies.

### Crewed vessel
A frame that expects multiple distinct occupants or roles to function properly.

### Civic platform
A platform whose main pressures include shelter, services, district or compartment logic, controlled entry, and organizational use.

### Mega-platform
A large operational shell whose scale creates districting, compartmentalization, multiple service layers, overlapping authorities, and complex transfer logic.

Scale should not be inferred from fiction alone. It should be classified by occupant density, role differentiation, subsystem load, transfer complexity, and service outputs.

---

## Occupant, station, subsystem, and service separation

These layers must not collapse.

### Occupant doctrine
An occupant is the user, rider, passenger, crew member, boarder, or operator relative to the frame.

### Station doctrine
A station is the role-bearing interface point through which an occupant affects the frame.

Examples:
- saddle;
- pilot seat;
- bridge console;
- gun battery;
- engineering bay;
- sensor chair;
- launch cradle control;
- cargo rig;
- docking spindle;
- shrine nexus.

### Subsystem doctrine
A subsystem is a functional component or grouped operational element whose condition may differ from the frame as a whole.

Examples:
- propulsion;
- heading/steering;
- communications;
- life support;
- shields;
- weapon mounts;
- sensors;
- cargo clamps;
- hangar doors;
- stables;
- teleporter matrix;
- lift array.

### Service doctrine
A service is what the frame makes available to occupants, passengers, allied systems, or connected structures.

Examples:
- transport;
- shelter;
- storage;
- scanning;
- protected approach;
- docking;
- launch;
- repair support;
- command support;
- cargo transfer;
- boarding mediation;
- tactical fire support.

This separation is mandatory. Without it, later conversions will flatten frames into one HP block or one item card, which is not robust enough for corpus-scale use.

---

## Control-topology doctrine

B14 must support multiple control topologies.

### Rider-led
The frame responds primarily through the rider or handler, often with low station complexity.

### Pilot-led
One operator primarily controls motion, heading, or basic operation.

### Crew-coordinated
Different occupants meaningfully control different outputs or subsystems.

### Station-based
The frame's capability set is partitioned across distinct stations whose use may be exclusive or role-bound.

### Partially autonomous
Some functions are automated or semi-automated while others still require occupants.

### Remotely operated
The frame is used through distance control, relay, drone link, or other non-embarked channel.

### AI-assisted or networked
Automation or integrated intelligence may substitute for some but not all crew/occupant burden.

### Shared-body or paired
The frame and its primary operator function as an unusually coupled system rather than simple rider/vehicle separation.

B14 should not assume one universal answer to “who drives.” It must classify who steers, who powers, who navigates, who senses, who fights, who repairs, who boards, and whether those roles are exclusive, overlapping, remote, or automated.

---

## Lawful crew-friction and throughput doctrine

Operational frames may change what a character can do, but they do not automatically multiply action throughput without cost.

### Core rule
A frame may alter action bandwidth, station access, protected reach, deployment profile, or service output, but it does not remove:
- command burden;
- crew burden;
- role contention;
- subsystem contention;
- station opportunity cost;
- occupancy limits;
- transfer cost;
- deployment friction.

### Application rule
When donor material implies that a frame grants “more actions,” Astra should classify whether those actions come from:
- an independent subsystem;
- an automated output;
- a distinct occupant role;
- a donor-local shared-bandwidth model;
- or a true increase in throughput that must be preserved explicitly.

The default doctrine position is conservative: **do not hand out free throughput accidentally**.

---

## Locomotion state versus operational state

Movement is only one part of frame doctrine.

### Locomotion state
How the frame is presently moving, if at all.

Examples:
- stationary;
- underway;
- airborne;
- submerged;
- orbiting;
- drifting;
- climbing;
- hovering;
- pulled;
- rowed;
- running;
- gliding.

### Operational state
How the frame is presently functioning as a service-bearing or conflict-bearing environment.

Examples:
- docked;
- deployed;
- active-service;
- boarded;
- anchored;
- landed;
- sheltered;
- under-crewed;
- unpowered;
- disabled;
- weapons-hot;
- embargoed;
- denied transfer;
- civilian-mode;
- emergency mode.

A frame may be stationary but operationally intense, or moving while tactically passive. These must not be collapsed.

---

## Propulsion, heading, and movement-state doctrine

B14 does not re-own routefinding or general traversal. It only defines how frame operation changes movement.

Relevant doctrine questions include:
- Does the frame require heading, facing, turn radius, drift, inertia, traction, or braking logic?
- Does the frame move only when directly controlled, or can it continue uncontrolled?
- Does the frame depend on fuel, motive force, biological stamina, magical sustain, power routing, tethering, or environmental medium?
- Does the frame alter occupancy safety while moving?
- Does movement depend on one station or several coordinated stations?

Frame movement should therefore be classified by:
- propulsion class;
- steering class;
- heading dependence;
- momentum or drift pressure;
- environmental medium requirement;
- control burden.

This section only defines doctrine grammar. B06 remains primary for route, pace, navigation, travel state, and broader traversal chains.

---

## Transfer, boarding, docking, and embarkation doctrine

Transfer states deserve first-class treatment.

### Core transfer states
- mounted;
- embarked;
- boarded;
- docked;
- tethered;
- launched;
- landed;
- ejected;
- dropped;
- disembarked;
- denied transfer.

### Transfer doctrine questions
- Who can initiate transfer?
- What stations, locks, saddles, bays, gangways, or gates are required?
- Is transfer voluntary, forced, contested, controlled, or prohibited?
- Does transfer expose occupants to danger, delay, or legal scrutiny?
- Does successful transfer change clearance, readiness, or positional status?

### Boarding doctrine
Boarding is not merely “moving into melee.” It is a change in relationship between operational frames, compartments, or occupancy regimes.

### Docking doctrine
Docking is a structured connection between frames or between a frame and operational transit infrastructure.

B14 should support contested docking, protected docking, tactical docking, ceremonial docking, clandestine docking, and emergency docking without needing separate donor-specific mini-games in every case.

---

## Occupant and role classes

B14 should support at least the following occupant roles:
- rider;
- handler;
- pilot;
- driver;
- navigator;
- gunner;
- engineer;
- sensor/science operator;
- captain/commander;
- passenger;
- crew support;
- boarder;
- escort rider or outrider;
- remote operator;
- maintenance operator;
- launch or dock controller.

Not every frame needs all roles. The point of the doctrine is to classify whether a role exists, whether it is exclusive, whether multiple occupants can share it, and whether the role is required, optional, or automated.

---

## Subsystem doctrine

Subsystems are not optional fluff. For many donor frames, subsystem state is the frame.

### Subsystem families
- propulsion and power;
- steering or locomotion control;
- protection and shielding;
- weapons and hardpoints;
- communications and command;
- sensors and scanning;
- life support or environmental conditioning;
- cargo, clamp, tether, or transfer systems;
- launch, dock, embark, or bay systems;
- habitation or readiness systems;
- repair and self-maintenance systems.

### Doctrine rule
A frame may be intact as a shell while one or more subsystems are degraded, contested, offline, jammed, broken, or overloaded.

This is why subsystem doctrine must remain separate from both generic item ontology and body-state survivability.

---

## Payload and service-output doctrine

Players do not only use frames to move. B14 must support frames as providers of lawful outputs.

### Payload families
- passengers;
- cargo;
- mounts or sub-vehicles;
- deployables;
- launch craft;
- boarding teams;
- ritual or technical payloads;
- diplomatic or ceremonial payloads.

### Service-output families
- transport;
- shelter;
- storage;
- protected approach;
- scanning and recon support;
- command support;
- repair support;
- deployment support;
- docking and transfer support;
- fire support;
- life support;
- mobile workshop or processing support;
- symbolic legitimacy or prestige support;
- route or approach access.

A frame’s mechanical meaning often lives in these outputs more than in its raw speed.

---

## Access-mediated frame use

B12 remains primary for organized access law, but B14 must support the fact that some frame operations depend on lawful occupancy or operator status.

Examples of access-mediated use:
- credentialed-only operation;
- ranked-user operation;
- bonded-user operation;
- faction-locked operation;
- restricted direct approach;
- pilot certification;
- emergency override;
- escort-only embarkation;
- token-gated launch or transfer;
- authorized crew list;
- sanctioned docking window.

This doctrine exists because many donor systems do not separate “the frame exists” from “you are allowed to use or approach it.”

---

## Damage, degradation, and operational failure doctrine

B14 must not reduce platform harm to creature HP or generic item wear.

### Frame-state classes
- intact;
- strained;
- degraded;
- under-crewed;
- overburdened;
- broken-subsystem;
- uncontrolled;
- disabled;
- breached;
- boarded;
- catastrophic-loss.

### Doctrine questions
- Is the frame still occupiable?
- Is it still controllable?
- Which services still function?
- Which transfer routes still function?
- Which subsystems are degraded or offline?
- Can the frame still shelter, carry, or deploy?
- Has the frame shifted from transport asset to hazard site?

This section is about operational state, not biological trauma or generic repair procedure.

---

## Dominant-function rule and hybrid constructs

Hybrid constructs are inevitable at Astra scale.

### Dominant-function rule
If the construct’s primary job is being a linked secondary actor, B13 is primary.
If the construct’s primary job is being a transport/combat/service frame, B14 is primary.
If the construct’s primary job is civic habitation, governance, districts, and infrastructure, B15 is primary.

### Cross-file note rule
When a construct meaningfully pressures more than one file, classify a primary file and then record explicit cross-file notes rather than trying to solve everything inside one doctrine layer.

### Example edge-case families
- rideable bonded beasts;
- mule drones and cargo drones;
- mechs used as both personal frame and command node;
- mobile forts;
- station-cities;
- walking cities;
- teleporter hubs with attached districts;
- carrier platforms.

The dominant-function rule exists to prevent silent scope collapse.

---

## Personal, crewed, and civic platform differentiation

B14 should explicitly support three large operational patterns.

### Personal frames
Frames centered on one user or rider.

### Crewed frames
Frames whose use assumes meaningful role differentiation, shared burden, and station logic.

### Civic platforms
Frames whose operational meaning includes service-bearing environment, district or compartment structure, and controlled access beyond simple transport.

This differentiation is important because many donor constructs shift category depending on use context.

---

## Carry-forward states and fallout

Frame use should produce carry-forward state rather than disappearing after a single scene.

Examples of carry-forward states:
- embarked and ready;
- embarked but under scrutiny;
- damaged frame awaiting repair;
- depleted fuel or sustainment state;
- boarded and insecure;
- docked and protected;
- stranded or unpowered;
- overburdened;
- crew-fatigued;
- restricted to emergency operation;
- flagged by authorities;
- bonded occupancy maintained;
- subsystem offline pending recovery.

This doctrine supports continuity between B14, B11, B12, and B15.

---

## Watch note for possible later split

If later conversion pressure causes B14 to swell with doctrines for fleet combat, convoy logistics, mobile-city adjudication, carrier launch doctrine, station-grid operations, or networked multi-platform management, reserve a later sister file such as:

`batchB_14b_fleets_convoys_mobile_cities_and_networked_platforms.md`

This note is a reserve only. It does not create a new active file in Batch B at this stage.

---

## Mandatory subsystem handoff map

- General traversal, routes, pace, navigation, and exploration chains -> `batchB_06_exploration_travel_navigation_time_and_distance.md`
- Environmental source hazards affecting frames -> `batchB_07_environment_hazards_weather_regions_and_afflictions.md`
- Stealth, visibility, and sensory uncertainty involving frames -> `batchB_08_stealth_detection_visibility_and_sensory_procedure.md`
- Social and authority pressure aboard or around frames -> `batchB_10_social_conflict_influence_reputation_and_negotiation.md`
- Structured non-encounter time, maintenance windows, and service scheduling -> `batchB_11_downtime_rest_training_projects_and_services.md`
- Organized access, legitimacy, clearance, docking rights, and sanctioned usage -> `batchB_12_factions_institutions_clearance_and_service_access.md`
- Linked secondary actors such as companions, drones, or rideable auxiliaries -> `batchB_13_companions_retinues_summons_drones_and_auxiliary_entities.md`
- Settlement, district, infrastructure, and civic macro-operations -> `batchB_15_settlements_bases_capitals_and_infrastructure_operations.md`
- Item ontology and ordinary gear schema -> `batchB_03_equipment_item_and_gear_object_model.md`
- Crafting, modification, installation, and repair procedure in general -> `batchB_05_crafting_salvage_repair_modification_and_installation.md`
- Body-state survivability and healing consequences for occupants -> `batchB_02_health_injury_healing_death_and_recovery_framework.md`
- Encounter sequencing and scene-time action procedure -> `batchB_01_scene_conflict_action_and_encounter_procedure.md`

---

## Lawful incomplete mapping and anti-hallucination rules

B14 must support lawful incomplete mapping when donor material is suggestive but underspecified.

Permitted mapping outcomes:
- directly mapped;
- normalized Astra mapping;
- dominant-function classified;
- scale-assigned;
- control-topology assigned;
- placeholder subsystem profile;
- quarantined pending later doctrine.

### Anti-hallucination rules
1. Do not assume every frame has separate subsystems if the donor clearly does not.
2. Do not assume every crewed frame needs one role per character if the donor treats automation or abstraction differently.
3. Do not assume every mount or mech is an auxiliary entity; classify by dominant function.
4. Do not assume every platform is a settlement; classify by dominant function.
5. Do not assume all boarding, docking, or embarkation transitions work alike.
6. Do not assume free action multiplication from frame use unless the donor explicitly grants it.
7. Do not silently import donor-local pilot, initiative, or station logic as Astra default law.

### Preservation invariant
Conversion must preserve donor frame pressure. Do not flatten crewed vessels, mounts, mechs, docking systems, mobile bases, or hybrid platforms into generic movement objects, and do not inflate light-touch donors into subsystem-heavy operational simulations they do not support.
