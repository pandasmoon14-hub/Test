# D08-00 Layered Actor-State Architecture

## Purpose

This file establishes Actor as the broadest D08 technical term and defines actor-state as a layered substrate. It exists so Astra can support player characters, NPCs, creatures, monsters, companions, mounts, familiars, summons, spirits, AI entities, swarms, hives, undead dual-state survivors, possessed hosts, intelligent items, constructs, source-local creatures, avatars, clones, and transformed actors without assuming one humanoid character-sheet model.

## Core rule

An Actor is any persistent or system-relevant entity that can hold state, receive consequences, act, be targeted, bond, advance, remember, transform, be harmed, or participate in world-state. All player characters are actors. Not all actors are player characters. D08 defines what the actor-state substrate is; other owner files validate power, harm, advancement, route, item, and world consequences.

## Actor hierarchy

- Actor is the broadest technical term.
- Character is an actor with sufficient identity, agency, continuity, and narrative or player significance to be represented as a character-level entity.
- Creature is an actor with a body or presence capable of interacting as organism, construct, spirit, monster, swarm, or source-local being.
- Companion is an actor with a durable bond or operational relation to another actor.
- Summon is an entity or actor brought into play by technique, ritual, route feature, pact, item, environment, faction authority, source-local rule, or Power Economy action.
- Form-state is a distinct body or presence state an actor can enter, suffer, maintain, or become.

## Actor layers

| Layer | Function |
| --- | --- |
| Identity layer | persistent actor identity, label, name, or reference |
| Body / kinform layer | physical, spiritual, constructed, machine, swarm, colony, or source-local body substrate |
| Cognition / personhood layer | how the actor thinks, feels, remembers, chooses, imitates, obeys, or has selfhood |
| Agency / control layer | independent action, command, instinct, program, bond, summoning law, or contested control |
| Bond / relation layer | companion, mount, familiar, AI co-pilot, pact entity, symbiote, or relation interface |
| Route / advancement interface | whether the actor can hold Routes, Techniques, Principles, advancement posture, or source-local progression |
| Harm / recovery interface | how D07 harm, mutation, corruption, recovery, and terminal states apply |
| Power / carrier interface | how D03 Power Economies, carriers, reservoirs, costs, and source-local resources attach |
| Anchor / platform interface | whether the actor depends on item, relic, ship, mech, implant, shrine, body, vessel, or D09 anchor |
| Social / world interface | how D10 society, faction, law, territory, recognition, and relationship state treat the actor |
| Source-local boundary layer | donor or campaign-local actor rules retained and prohibited from generalization |

## Actor categories

Actor categories are overlapping labels rather than mutually exclusive silos. Categories include person, creature, kinform, companion, summon, spirit/nonmaterial, AI/machine, swarm/hive/colony, avatar/projection, anchor-bound, possession-adjacent, source-local, and mixed. A spirit sword can be anchor-bound, spirit, companion, and D09 item-linked. A fungal courier can be person, kinform, colony-linked, and source-local. A ship AI can be AI, companion, platform-linked, and major NPC.

## Record-depth principle

Actor-state depth scales by need. Disposable effects do not need full records. Recurring rivals, bonded companions, AI co-pilots, living/undead dual-state survivors, source-local vampires, and emergent swarm minds do. D08 supports ephemeral entity, simplified actor, functional actor, persistent actor, major actor, companion-grade actor, route-bearing actor, source-local actor, and escalated actor depth grades.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Source-local restraint

D08 never imports donor actor taxonomy as canon by default. A donor ancestry, monster type, familiar rule, construct premise, undead morality, vampire weakness list, summon table, AI property status, or swarm mindlessness rule must be decomposed and routed. It may become direct Astra mapping, normalized mapping, source-local retention, quarantine, or escalation.

## Acceptance criteria

A D08 actor-state decision is valid when it identifies whether the construct is an actor or non-actor construct, assigns actor category and record depth only as needed, separates actor substrate from route/harm/power/item/social systems, preserves source-local boundaries, records owner-file handoffs, avoids making all actors full PC-equivalent records, and leaves D10 relational/social doctrine for D10.
