# D14-04 — Exploration Context Profiles, Site Entry, Watches, and Ambush Exposure

Status: doctrine-draft / Phase 1 native doctrine continuation  
Version: `0.1.0-d14-generated`  
Generated: 2026-06-02  
Layer: D14 operational procedure doctrine  
Owner: Astra doctrine architecture / exploration and discovery procedure layer

## Purpose

This file defines Exploration Context Profiles and special transition tools for site entry, watches, and ambush exposure. Profiles are routing/procedure templates, not full subsystems.

## Profile structure

Each profile identifies movement logic, route forms, posture pressures, discovery types, hazard/encounter triggers, map-state concerns, watch/ambush exposure concerns, resource/exposure pressures, owner-file handoffs, source-local risks, and quarantine/escalation triggers.

## Core profiles

### Urban / Social-Dense

Used for cities, districts, ports, markets, stations, arcologies, courts, sect compounds, slums, campuses, corporate zones, and settlements. Movement logic: access, legality, visibility, social blending, surveillance, restricted areas, contacts, faction territory, transport networks, checkpoints. Handoffs: D05, D09, D10, D11, D15, D17. Do not import city encounter tables, crime systems, social-status systems, or faction clocks as universal law.

### Wilderness / Open-Region

Used for forests, deserts, mountains, tundra, oceans, plains, wastelands, jungles, and frontiers. Movement logic: route finding, weather/terrain pressure, supplies, exposure, landmarks, tracking, foraging, visibility, ambush space, environmental PCR. Handoffs: D03, D05, D07, D10, D16, D17. Do not universalize hexes, foraging, travel pace, random encounters, or watch shifts.

### Site / Dungeon / Interior

Used for ruins, buildings, dungeons, ships, bases, caves, labs, temples, tombs, vaults, bunkers, and facilities. Movement logic: entry control, room/node relation, visibility, sound, traps/hazards, keyed areas, locked paths, hidden doors, site memory, map uncertainty. Handoffs: D09, D10, D12, D16, D17. Do not import dungeon turns, keyed-room reveal assumptions, trap procedures, or wandering monster checks.

### Space / Vehicle / Platform

Used for ships, vehicles, mechs, stations, derelicts, convoys, fleets, star lanes, debris fields, and mobile bases. Movement logic: vectors, sensors, crew roles, fuel/power pressure, system integrity, platform scale, external hazards, docking/approach, instruments, communications. Handoffs: D03, D08, D09, D10, D12, D16, D17. Do not collapse platform movement into actor movement or import ship-turn, fuel, hardpoint, grid, or tactical-frame law.

### Dimensional / Realm / Threshold

Used for planes, realms, spirit roads, pocket worlds, gates, unstable zones, dream spaces, cultivation territories, domain regions, and mythic thresholds. Movement logic: access, domain alignment, stability, resonance, threshold conditions, identity pressure, route truth instability, hidden cosmic pressure, source-local metaphysics. Handoffs: D03, D06, D07, D08, D10, D11. Do not import donor cosmology, planar law, tribulation travel, astral travel, or realm metaphysics.

### Hazardous / Anomalous Zone

Used for radiation-like zones, corrupted regions, magical storms, hostile biomes, broken reality spaces, battlefield aftermath, cursed terrain, unstable ruins, and environmental anomaly zones. Movement logic: exposure management, hazard pulses, safe path discovery, protective posture, depletion, sensor/ritual distortion, environmental PCR, escalating instability. Handoffs: D03, D07, D09, D10, D12, D16. D14 must not define final exposure math or damage families.

### Pursuit / Evasion

Used when travel occurs under chase, escape, hunt, tailing, interception, or tracking pressure. Movement logic: distance/position pressure, route choice under time, concealment, speed versus safety, tracking signs, ambush reversal, transition into active chase cadence. Handoffs: D02, D05, D07, D10, D12, D16. D14 handles route/exploration under pursuit; D12 owns active chase cadence.

## Site Entry

Site Entry is the transition from route/area movement into a bounded location, structure, region, platform, node, or scene space. It may trigger known-state review, entry posture, map-state update, hazard scan, ambush exposure, D12 transition, D10 pressure, D11 presentation, or source-local procedure.

Site Entry is not automatic boxed-text reveal. It does not reveal all room facts, trigger every trap, or start an encounter unless owner-file state, posture, route pressure, scenario design, or source-local procedure supports it.

## Watches

A Watch is a posture or role assignment for monitoring danger, route-state, environment, or hidden pressure during a travel/exploration interval. Watch types include guard, scout, sensor, ritual, social, rear, platform systems, faction/surveillance, and source-local watch. It is not a fixed universal shift system.

## Ambush Exposure

Ambush Exposure is the risk that movement, posture, route, visibility, opposition, or hidden pressure creates an opportunity for hostile or hazardous action before the party controls the scene. It is not automatic surprise. D12 handles sequencing transition; D02 handles uncertainty.
