# D06-08 Profession Routes, Lineages, Schools, and Factions

**File ID:** `D06-08`  
**Pack:** Astra Ascension D06 — Route, Path, Principle, Technique, and Donor Class Normalization Doctrine  
**Version:** v0_1  
**Status:** Design doctrine draft generated from accepted D06 decisions.  
**Purpose:** Define profession-routes, lineages, schools, faction routes, and D10 boundary discipline.

## Standing D06 boundary

D06 owns formal route identity, Path identity, Route Kernels, route facets, Route Feature Ledgers, Techniques, Principle / Concept route facets, route development, multipath / confluence, profession-route formalization, source-local route conversion, and donor class normalization.

D06 does **not** own D03 Power Economy costs, carriers, Expressions, reservoirs, burdens, or confluence math; D04 proof sufficiency, level, tier, Awakening, Development Picks, breakthroughs, capstone, or Ascension Access; D05 skills, professions, knowledge, training, research, methods, and synthesis substrate; D07 harm, corruption, madness, mutation harm, overload, identity erosion, or recovery; D08 companions, summons, spirits, AI, bonds, or nonhuman actor-state mechanics; D09 relics, tools, implants, weapons, vehicles, ships, mechs, or platforms; D10 factions, rank, law, reputation, territory, settlement, economy, or world-state; final runtime/database schemas; canon sourcebook prose; or live-play GM behavior.

D06 records candidates, structure, permissions, limits, and owner-file handoffs. It does not use route language to bypass the owners above.


## 1. Structured Route Source Model

Professions, schools, lineages, factions, guilds, sects, crews, teachers, impossible instructors, and institutions may source or shape routes. They do not grant active Routes automatically.

They may provide access, training, Technique sources, Route Feature candidates, proof challenges, obligations, recognition, source-local boundaries, external anchors, or route constraints.

## 2. Profession-Route

A **Profession-Route** is a D06 Route whose formal identity emerges from a D05 Profession after sufficient proof, transformation, route pressure, and authorization.

Requirements:

1. D05 Profession Record.
2. Proof or route pressure.
3. D04 authorization if advancement-relevant.
4. D06 Route Authorization Packet.
5. Defined permissions.
6. Defined limits.
7. Route Feature Ledger entries or candidates.
8. Owner handoffs when tools, factions, companions, Power Economies, harm, or world-state are involved.

Profession remains D05. Profession-Route is D06.

Examples:

- Beekeeper → **Grey-Hive Wayfarer** only after poisoned orchard travel, hive-weather methods, swarm bond, settlement rescue proof, D08 handoff.
- Court Tailor → **Silk-Writ Envoy** after encoded diplomatic garments and social proof.
- Scrap Mechanic → **Wreck-Saint Mechanist** after war-machine repair under fire and D09 salvage anchor.

## 3. Lineage

A **Lineage** is transmitted route pattern, method family, Technique Set, Principle interpretation, or training inheritance passed through teacher, tradition, ancestry, spirit, archive, AI, institution, faction, relic, or source-local chain.

Lineage is not automatically bloodline. It can transmit technique access, route interpretation, constraints, taboos, teacher authority, and source-local terminology. It does not automatically grant faction rank, proof sufficiency, Power Economy capacity, or active route identity.

## 4. School

A **School** is an organized teaching structure. It may be academy, martial hall, guild workshop, field hospital, machine temple, military unit, ship crew, criminal syndicate, nomad caravan, AI lattice, spirit grove, or source-local sect.

A school may provide curriculum, but curriculum is not automatically a Path table. A student may gain D05 competencies and D06 Technique candidates without becoming a formal Path until proof and authorization exist.

## 5. Faction Route

A **Faction Route** is route identity shaped or granted by faction access, doctrine, techniques, obligations, or recognition. Faction membership is not a Faction Route. Faction rank is D10. Route identity is D06.

| Construct | Owner | Meaning |
|---|---|---|
| Faction membership | D10 | Actor belongs to faction. |
| Faction rank | D10 | Status, office, or authority. |
| Faction reputation | D10 | Standing. |
| Faction training | D05 / D10 | Instruction or access. |
| Faction technique | D06 + owners | Formal capability. |
| Faction Route | D06 + D10 | Route identity shaped by faction. |
| Faction law/world effect | D10 | Macro consequence. |

A character can have faction rank without a Faction Route. A character can have a Faction Route but lose faction rank, creating route scar, dormancy, mutation, exile, or severance.

## 6. Teacher authority

Teacher authority levels:

- Demonstrator: can show a technique or method.
- Instructor: can train route-relevant competencies or Techniques.
- Route Mentor: can guide route development.
- Lineage Bearer: can transmit lineage-specific route structure.
- Initiator: can open access to a route candidate or school gate.
- Route Authority: can validate formal initiation under D06 / D10 rules.
- Impossible Teacher: relic, spirit, AI, domain, ancestor, world-site, or source-local force.

Teacher authority does not erase proof requirements unless the route source itself lawfully supports transmitted route authorization.

## 7. Route obligations

Profession, school, lineage, and faction routes may carry obligations: oath, service, taboo, curriculum requirement, rank duty, guild debt, faction law, secrecy, lineage preservation, payment, pilgrimage, tool maintenance, domain stewardship, companion care, source-local restriction.

Obligations can appear as Route Feature Ledger constraints. D10 validates legal/social obligation. D07 validates identity harm when obligation becomes psychological or metaphysical pressure.

## 8. Source-local school normalization

Donor schools, sects, orders, guilds, prestige classes, faction packages, and colleges normalize by function:

- class → source-local Route candidate or normalized Route;
- subclass → branch, facet, feature option, or source-local package;
- prestige class → advanced branch, second Route, fusion candidate, or source-local Route;
- school / sect → D05 / D10 teaching institution plus D06 route source;
- guild profession class → D05 Profession + D06 Profession-Route candidate + D10 guild;
- spell list → D03 Expression family, D06 Technique Set, source-local list, or escalation.

## 9. Varied examples

- Hermit bridge-builder → **Floodspan Keeper** without faction, after community-saving flood proof.
- Merchant treasurer: D10 faction rank only, no Route unless structured route development appears.
- Storm fencing academy student: D05 training and D06 Technique candidates, no Path until proof / authorization.
- Dying courier teaches “three road silences”: D05 method transmission; later lineage facet if route pressure develops.
- Exiled **Red-Moon Skirmisher**: D10 status lost; D06 route may become scarred, dormant, mutated, or independent.
- Stone-bodied actor receives mining lineage through engraved pressure patterns: D08 nonhuman actor-state, D05 training, D06 lineage.

## 10. Doctrine shape

```yaml
route_source_record:
  source_id: string
  actor_ref: string
  route_ref: string
  source_type: profession_route | lineage | school | faction_route | teacher_transmission | guild | academy | sect | order | crew | military_unit | institution | impossible_teacher | source_local
  source_name: string
  d05_refs: []
  d10_refs: []
  proof_refs: []
  training_refs: []
  method_refs: []
  technique_refs: []
  feature_ledger_refs: []
  permissions_granted: []
  limits_or_obligations: []
  source_local_boundary: null
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D07: []
    D08: []
    D09: []
    D10: []
  validation_state: authorized | pending_proof | pending_access | pending_owner_file | dangerous | source_local | blocked | escalated
```

## 11. Rule

A route can be taught, inherited, earned, recognized, imposed, or institutionally shaped, but route identity still requires proof-shaped authorization and owner-boundary discipline.
