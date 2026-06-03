# D06-01 Route Authorization and Path Identity

**File ID:** `D06-01`  
**Pack:** Astra Ascension D06 — Route, Path, Principle, Technique, and Donor Class Normalization Doctrine  
**Version:** v0_1  
**Status:** Design doctrine draft generated from accepted D06 decisions.  
**Purpose:** Define the gate by which Route candidates become active Routes and Path identities.

## Standing D06 boundary

D06 owns formal route identity, Path identity, Route Kernels, route facets, Route Feature Ledgers, Techniques, Principle / Concept route facets, route development, multipath / confluence, profession-route formalization, source-local route conversion, and donor class normalization.

D06 does **not** own D03 Power Economy costs, carriers, Expressions, reservoirs, burdens, or confluence math; D04 proof sufficiency, level, tier, Awakening, Development Picks, breakthroughs, capstone, or Ascension Access; D05 skills, professions, knowledge, training, research, methods, and synthesis substrate; D07 harm, corruption, madness, mutation harm, overload, identity erosion, or recovery; D08 companions, summons, spirits, AI, bonds, or nonhuman actor-state mechanics; D09 relics, tools, implants, weapons, vehicles, ships, mechs, or platforms; D10 factions, rank, law, reputation, territory, settlement, economy, or world-state; final runtime/database schemas; canon sourcebook prose; or live-play GM behavior.

D06 records candidates, structure, permissions, limits, and owner-file handoffs. It does not use route language to bypass the owners above.


## 1. Core problem

Astra must prevent automatic identity inflation. A profession, title, research result, donor class, faction rank, or conceptual affinity cannot become a Route by itself. D06 therefore uses the **Route Authorization Packet**.

A Route Authorization Packet is the doctrine structure that records why a Route is lawful now.

## 2. Route Authorization Packet requirements

A Route may become active only when it has:

1. lawful route source;
2. authorization basis;
3. selected Path identity;
4. route function;
5. route permissions;
6. route limits;
7. route facets;
8. required owner-file handoffs;
9. route state;
10. validation state;
11. actor-state delta.

The packet may be lightweight in play, but doctrine requires these elements so route identity is auditable.

## 3. Authorization sources

Valid route sources include:

- D04 Awakening Package;
- D05 Profession-Route pressure;
- D05 mastery, research, method, or synthesis records;
- teacher, lineage, school, guild, faction, order, sect, crew, or institution;
- external anchor such as relic, ship, mech, implant, companion, AI, territory, shrine, archive, or office;
- Principle / Concept route event;
- Domain contact;
- forced, coerced, corrupted, cursed, accidental, or hostile route imposition;
- source-local converted class or path;
- D04 breakthrough, capstone, or Ascension Access transformation.

Invalid sources include naming a desired Path without basis, copying donor class packaging, high profession rank alone, faction rank alone, one impressive event without route-relevant proof, or a D05 method without D06 authorization.

## 4. Path identity

A **Path** is the player-facing identity of an authorized Route. A strong Path identity answers:

- What has the actor become authorized to develop?
- What proof, source, or event shaped this Route?
- What facets does it contain?
- What permissions does it create?
- What limits does it impose?
- What obligations, scars, anchors, or source-local boundaries apply?

Bad Path design: “Far Fisher: magical fisher.”

Better Path design: “Far Fisher: a profession-route formed from impossible pursuit, aquatic reading, long-distance prey logic, line-and-depth methods, and world-crossing desire. It authorizes development around distance, lure, hidden movement, patient pursuit, aquatic domains, and impossible catch logic. It does not automatically grant teleportation, planar travel, creature domination, or tide authority.”

## 5. Route states

D06 tracks route states so unusual cases can be handled without improvising new systems.

| State | Meaning |
|---|---|
| candidate | Possible route, not yet authorized. |
| latent | Route seed exists but is not active. |
| offered | Route appears as a bounded choice. |
| selected | Chosen but still resolving packet requirements. |
| active | Lawful route development can proceed. |
| dormant | Route exists but is inaccessible or inactive. |
| scarred | Route carries lasting wound, cost, trauma, or contradiction. |
| coerced | Route was forced or imposed. |
| corrupted | Route is contaminated, hostile, or unstable. |
| externalized | Route depends on an external anchor. |
| source-local | Route is bounded to a source or context. |
| unstable | Route works but risks drift, backlash, or contradiction. |
| rejected | Route was refused but may remain in the ledger. |
| severed | Route was cut away, lost, or intentionally removed. |
| fused | Route merged with another route structure. |
| mutated | Route changed into another structure. |
| retired | Route no longer develops but remains historical. |

UI may simplify these, but doctrine should preserve them.

## 6. Candidate handling

Multiple route candidates may exist internally. Player-facing choice should usually remain bounded, especially at Awakening. A character with many proof clusters should not receive dozens of choices. D06 may collapse candidates into strongest lawful options while recording latent, rejected, dormant, scarred, or future fusion candidates.

## 7. Low-tier Principle / Concept limit

A Principle or Concept route at low tier may shape perception, route pressure, method development, resonance signals, bounded technique candidates, and domain alignment. It does not grant reality override, immunity, conceptual damage, resurrection, universal truth, or cosmic rank by default. Those require D04 proof / tier authorization and D03 / D07 / D10 handoffs as relevant.

## 8. Doctrine shape

```yaml
route_authorization_packet:
  route_id: string
  actor_ref: string
  proposed_path_name: string
  route_source: []
  authorization_basis:
    proof_refs: []
    d04_refs: []
    d05_refs: []
    source_local_refs: []
    owner_handoff_refs: []
  route_function: string
  route_permissions: []
  route_limits: []
  route_facets: []
  required_handoffs:
    D03: []
    D04: []
    D05: []
    D07: []
    D08: []
    D09: []
    D10: []
  route_state: candidate | latent | offered | selected | active | dormant | scarred | coerced | corrupted | externalized | source_local | unstable | rejected | severed | fused | mutated | retired
  validation_state: authorized | pending_proof | pending_choice | pending_owner_file | dangerous | source_local | blocked | escalated
  state_delta: string
```

This is a doctrine handoff shape, not final runtime schema.

## 9. Varied examples

### Lawful: Oathbound Street Surgeon

A street medic repeatedly saves hostile faction members under oath-bound neutrality. D05 records medical skill, profession, and trauma methods. D04 records proof. D10 records faction recognition. D06 authorizes **Oathbound Street Surgeon** with permissions around triage, oath-protected neutrality, battlefield medical Techniques, and limits against universal healing or legal invulnerability.

### Unlawful: “I name myself Void Emperor”

A player declares a Path name without proof, source, authorization basis, facets, permissions, limits, or handoffs. D06 classifies this as unsupported route declaration. It may become a desired route, research project, or dangerous temptation, but it is not active.

### Source-local: Cloud Palm Disciple

A donor sect grants Cloud Palm Disciple rank. D06 records a source-local Route candidate. D10 owns sect rank. D03 reviews cloud qi resource if retained. D06 may normalize palm Techniques, but the donor sect path does not become canon Astra law.

## 10. Rule

A formal Path is proof-shaped, bounded, and authorized. It is not a donor class table, profession label, skill rank, faction rank, title, research output, or player-declared identity.
