# D08-03 Companions, Bonds, Mounts, Pets, and Familiars

## Purpose

This file defines companions as bonded actors rather than equipment, class features, or automatic full characters. It supports pets, mounts, familiars, bonded beasts, spirit partners, AI co-pilots, drone swarms, symbiotes, pact entities, retainers, source-local companions, and ordinary allies that may become companions.

## Core rule

A companion is an actor with a durable bond or relation interface to another actor. Companion is not a species, item, class feature, or automatic PC-equivalent actor. Companion depth scales by relevance, agency, personhood, bond strength, permissions, limits, advancement posture, and owner-file impact.

## Distinctions

A companion is a persistent bonded actor. An ally cooperates but does not necessarily have a durable companion bond. A summon is called, created, manifested, contracted, or conjured and may become a companion if it persists and bonds. An item or anchor is D09-owned and may host an actor, but it is not automatically a companion.

## Bond types

Accepted bond types include care, mount, familiar, pact, spirit, AI/machine, swarm/hive, symbiotic, command, kinship, route, and source-local. Bond types can overlap. A wolf mount can have care, mount, kinship, and route bond. A ship AI can have AI/machine, kinship, companion relation, and D09 platform dependency.

## Bond voluntariness

Accepted voluntariness states include mutual, care-based, trained, contracted, commanded, coerced, programmed, symbiotic, parasitic, summoned-bound, and source-local. Coerced, parasitic, programmed, or commanded bonds require personhood and agency review and may create D07 and D10 consequences.

## Companion agency, personhood, and depth

A companion may have full, limited, emergent, fragmentary, contested, no, or source-local personhood. Agency may be full, limited, instinctive, trained, commanded, bond-guided, programmed, summoned-bound, possession-contested, external-controlled, dormant, or source-local. Companion depth grades are minor, functional, bonded, major, route-integrated, shared-state, source-local, and escalated.

## Companion advancement

Companions may be non-advancing, training-advancing, bond-advancing, evolutionary, route-linked, track-based, source-local, or rarely full-advancing. Companion advancement is not automatic and requires owner-file validation.

## Permissions and limits

Permissions may include assist, scout, carry, mount, guard, attack, defend, retrieve, communicate, sense, track, channel power if validated, use Technique if validated, share perception, share resource, trigger bond feature, protect actor, act independently, refuse command, or pursue own goal. Limits may include agency limit, range, communication, environment, size/body, training, loyalty/obedience, resource cost, action economy, harm vulnerability, social restriction, source-local limits, and route/feature permission boundaries. A companion never grants unlimited extra action economy, scouting, resources, or route access by default.

## Bond harm and recovery

D08 records the bond substrate. D07 owns bond harm and recovery. Bond harm includes trust loss, fear, grief, injury, command trauma, pact strain, AI sync damage, swarm cohesion loss, symbiotic rejection, bond corruption, loyalty fracture, companion death, severed bond, inherited grief, and revenge pressure. Recovery may include care, apology, training, rest, ritual, repair, pact renegotiation, route reconciliation, D10 reparations, D09 anchor repair, D07 grief recovery, or source-local treatment.

## Companion death and replacement

Companion death may produce ordinary death, injury/recovery, lost companion, captured companion, transformed companion, corrupted companion, spirit continuation, inherited bond, successor companion, source-local resurrection, route scar, or D10 social memory. A replacement companion is not automatically the same actor.


## Owner boundary

D08 owns actor-state substrate. It does not own every system attached to an actor. D03 owns Power Economy, carriers, reservoirs, costs, and sustainment. D04 owns advancement proof, tiers, breakthroughs, and capstones. D05 owns training, handling, research, diagnosis, medicine, and command methods. D06 owns Routes, Paths, Principles, Techniques, and Route Features. D07 owns harm, injury, corruption, mutation harm, recovery, and terminal outcomes. D09 owns items, relics, tools, implants, prosthetics, platforms, ships, mechs, drone hardware, and anchors. D10 owns factions, culture, law, reputation, social recognition, relationship graphs, territory, and world-state. D11 and later runtime adapters own presentation and live-play behavior.


## Record shape

```yaml
companion_bond_record:
  bond_id: string
  primary_actor_ref: string
  companion_actor_ref: string
  companion_grade: minor | functional | bonded | major | route_integrated | shared_state | source_local | escalated
  bond_types: []
  voluntariness: mutual | care_based | trained | contracted | commanded | coerced | programmed | symbiotic | parasitic | summoned_bound | source_local
  agency_profile: string
  personhood_profile: string
  permissions: []
  limits: []
  advancement_posture: non_advancing | training | bond | evolutionary | route_linked | track | source_local | full
  bond_state: stable | growing | strained | neglected | damaged | corrupted | severed | grieving | transformed | source_local
  harm_refs: []
  route_refs: []
  power_refs: []
  anchor_refs: []
  social_world_refs: []
  source_local_boundary_refs: []
```

## Examples

An ordinary riding horse is functional companion with mount bond and D05 handling. A bonded wolf is a bonded companion but has no route feature unless D06 authorizes it. A spirit familiar is companion plus spirit/nonmaterial actor and possibly pact-bound. An AI co-pilot is AI/machine actor, possible major companion, D09 platform-linked, and D10 legal recognition candidate. A donor animal companion table is source-local or normalized by function.
