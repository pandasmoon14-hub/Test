# D08-05 Swarms, Hives, Colonies, and Distributed Actors

## Purpose

This file defines actors whose body, cognition, memory, agency, or continuity is spread across multiple units, nodes, hosts, drones, spores, fragments, or locations. It prevents swarms from becoming one normal creature by default and prevents every unit from requiring a full actor record.

## Core rule

A distributed actor is an actor whose body, cognition, memory, agency, or continuity is distributed across multiple units or nodes. D08 records whether the collective is treated as one actor, many actors, a collective actor with sub-actors, a companion swarm, a faction/world-state entity, a platform network, or a source-local construct.

## Definitions

A swarm is a distributed body composed of many small or similar units acting together. A hive is a distributed actor or society with coordinated members, often organized around shared purpose, command, queen/core, or collective cognition. A colony is a distributed organism or actor made of linked bodies, cells, organisms, fungi, drones, or symbiotic units. Collective cognition means cognition is shared, aggregated, voted, broadcast, synchronized, emergent, or distributed.

## Distributed forms

Accepted forms include single collective actor, collective with key nodes, many actors with shared link, companion swarm, platform network, territory-embedded actor, source-local distributed actor, and escalated case. A simple insect swarm can be one collective actor. A hive queen plus drones can be collective with key nodes. Linked clones may be many actors with shared link. A drone familiar can be companion swarm. A sentient mycelial city may be territory-embedded actor plus D10 handoff.

## Unit and node structure

D08 tracks units only as needed. Relevant node categories include expendable units, significant units, core unit, queen/core, anchor node, memory node, command node, sensory node, reproductive/replication node, carrier node, route node, platform node, and source-local node. A swarm may lose many units without individual death records. A queen, memory grove, AI core, or bonded familiar-node may require durable records.

## Cohesion

Cohesion is the distributed actor’s ability to function as a unified actor. States include coherent, stretched, fragmented, disrupted, panicked, command-broken, corrupted, partitioned, merged, dissolving, and source-local. Cohesion may represent physical clustering, command synchronization, shared will, hive signal strength, memory continuity, swarm morale, AI network integrity, mycelial continuity, spirit flock resonance, necromantic control, or source-local group body stability.

## Unit loss and distributed harm

Distributed actors do not always suffer ordinary injury. Harm may be unit loss, cohesion loss, memory-node damage, signal disruption, command-node destruction, queen/core injury, carrier-node burnout, territory damage, anchor damage, identity fragmentation, sub-swarm severance, corrupted unit spread, or terminal dispersal. D07 owns harm consequences. D08 owns the actor structure.

## Continuity, personhood, and agency

Continuity questions include whether the actor survives unit loss, whether there is a core, where continuity resides, whether fragments can become new actors, whether fragments can merge later, and whether social recognition identifies the collective after unit changes. Distributed actors may have no, emergent, full collective, core-located, distributed, contested, or source-local personhood. Agency may be instinctive, commanded, programmed, queen-directed, democratic, emergent, bond-guided, route-driven, external-controlled, or source-local.

## D08/D10 boundary

D08 owns hive/colony/swarm as actor. D10 owns hive/colony/swarm as society, faction, settlement, population, economy, territory, relationship network, or world-state structure.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record shape

```yaml
distributed_actor_record:
  actor_ref: string
  distributed_form: single_collective_actor | collective_with_key_nodes | many_actors_with_shared_link | companion_swarm | platform_network | territory_embedded_actor | source_local | escalated
  unit_structure:
    unit_types: []
    key_nodes: []
    core_or_queen_ref: string | null
    command_nodes: []
    memory_nodes: []
    sensory_nodes: []
    carrier_nodes: []
    platform_nodes: []
    source_local_nodes: []
  cohesion_state: coherent | stretched | fragmented | disrupted | panicked | command_broken | corrupted | partitioned | merged | dissolving | source_local
  continuity_state: continuous | altered | fragmented | partitioned | copied | merged | severed | dormant | source_local | escalated
  cognition_profile: instinctive | commanded | programmed | queen_directed | collective | emergent | sapient | foreign | source_local
  personhood_state: none | emergent | full_collective | core_located | distributed | contested | source_local
  agency_control_state: instinctive | commanded | programmed | queen_directed | democratic | emergent | bond_guided | route_driven | external_controlled | source_local
```

## Examples

An ordinary insect swarm is a single collective actor, instinctive, no personhood. A fungal courier is person plus colony-linked physiology. A drone cloud companion is companion swarm and platform network. A distributed AI fork can be copied or partitioned continuity. An undead horde may be source-local swarm, command-bound group, or many actors with shared link.
