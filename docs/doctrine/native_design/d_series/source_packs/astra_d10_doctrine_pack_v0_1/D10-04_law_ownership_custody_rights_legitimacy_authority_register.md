# D10-04 Law, Ownership, Custody, Rights, Legitimacy, and Authority Register

## Purpose

This file defines how Astra tracks law-facing consequence without becoming a legal simulator, courtroom engine, enforcement AI, market simulator, or punishment mechanic.

## Core rule

D10 records persistent legal, ownership, custody, rights, legitimacy, and authority state. It records who claims what, who is recognized, who is restricted, what is legal or illegal, what authority applies, what enforcement pressure exists, and what disputes remain unresolved. It does not simulate full legal proceedings or define final economy.

## Jurisdiction

A jurisdiction is a law-facing authority zone or authority relationship. It may belong to state, city, sect, guild, corporation, temple, military command, ship captaincy, station authority, noble house, tribal council, AI collective, hidden faction, or source-local authority.

Jurisdiction fields include authority holder, territory/location scope, actor scope, object scope, law-zone rules, recognition status, contested status, enforcement capacity, and source-local boundary.

Jurisdiction is not physical control.

## Legal relation states

| State | Meaning |
|---|---|
| Ownership | Recognized claim over object, place, resource, platform, asset, or right. |
| Possession | Physical holding or practical control. |
| Custody | Temporary legal, sacred, institutional, or protective responsibility. |
| Use Right | Permission to use something without owning it. |
| Access Right | Permission to enter, inspect, dock, cross, operate, or approach. |
| Stewardship | Duty-bound holding for faction, office, lineage, spirit, deity, public, or heir. |
| Loan | Temporary use under terms. |
| Issuance | Faction/institution grants object or authority for role. |
| Requisition | Authorized acquisition through rank, office, emergency, or institutional demand. |
| Seizure | Authority or force takes possession. |
| Theft | Possession violates recognized ownership/custody. |
| Salvage Claim | Claim from recovery from wreck, ruin, battlefield, corpse, abandoned site, source-local context. |
| Inheritance | Claim based on lineage, office, will, oath, tradition, source-local rule. |
| Sacred Claim | Claim based on taboo, religion, metaphysical authority, ritual office, ancestor, or oath. |
| Source-local | Donor/campaign legal relation. |

Ownership, possession, custody, and use rights must remain distinct.

## Legitimacy and recognition

Legal status, legitimacy, and recognition are separate. States include legal, illegal, tolerated, contested, illegitimate, legitimate, sacredly legitimate, socially legitimate, faction-recognized, publicly recognized, secretly recognized, and source-local.

This matters for rulers, heirs, relic bearers, AI citizens, undead survivors, clone successors, spirit vessels, ship captains, sect disciples, and faction officers.

## Restricted objects, forms, and statuses

D10 tracks restrictions without owning object or actor mechanics. Restrictions may apply to weapons, armor, relics, artifacts, strategic materials, monster cores, catalysts, cyberware, biotech, grafts, living gear, AI cores, spirit vessels, necromantic objects, cursed items, platforms, starships, drones, military gear, undead forms, transformed states, clone bodies, forbidden Techniques, and source-local contraband.

D09 owns object-state. D08 owns actor/body/personhood. D06 owns Techniques. D10 owns law, license, taboo, and enforcement pressure.

## Contraband and black-market status

States include legal, licensed, restricted, contraband, taboo, black-market, tolerated, protected, confiscatable, destroy-on-sight, and source-local. Black-market status is not economy math. It is legal and access pressure.

## Enforcement pressure

Enforcement records may include warrant, bounty, arrest order, kill order, exile, banishment, interdiction, seizure order, customs hold, docking denial, travel ban, restricted trade, embargo, sanction, quarantine order, religious condemnation, military pursuit, and source-local enforcement clock.

Each record should include authority, target, scope, visibility, basis, severity, capacity, expiration/decay, resolution, and source-local boundary. D10 does not run enforcement AI.

## Personhood recognition and rights

D10 tracks legal/social recognition while D08 owns actor substrate.

Subjects may include AI, spirit, undead, clone, construct, awakened animal, symbiote, living ship, uploaded mind, summoned being, bound entity, transformed actor, split self, and source-local being.

Recognition states include recognized person, non-person property, protected non-person, ward/dependent, contested personhood, conditional personhood, secret personhood, illegal existence, sacred status, and source-local.

D08 owns whether the subject has actor/personhood substrate. D10 owns whether society/law recognizes it.

## Custody over actors and actor-adjacent entities

Custody targets may include prisoner, ward, child/heir, bound spirit, summoned being, AI core, clone body, undead actor, companion creature, symbiote, construct, and source-local actor.

Custody types include legal custody, protective custody, sacred custody, faction custody, medical custody, military custody, contractual custody, enslavement claim, guardianship, unlawful detention, and source-local custody.

## Platform registration and travel authority

D10 tracks ship registration, transponder identity, docking rights, customs status, cargo inspection, military restriction, lane permission, platform ownership, fleet command status, salvage title, piracy designation, quarantine flag, AI captain recognition, and source-local vehicle law.

D09 owns platform object-state. D10 owns registry/law/permission/enforcement.

## Salvage rights, inheritance, requisition

Salvage law applies to abandoned property, battlefield salvage, wreck salvage, corpse salvage, monster-part harvesting, relic recovery, sacred remains, AI core recovery, ship salvage title, state-seized salvage, forbidden salvage, and source-local salvage.

D10 supports inheritance of title, office, territory, faction rank, relic, platform, estate, debt, obligation, curse, sacred duty, AI custody, and source-local inheritance.

D10 tracks who can requisition issued assets and under what authority. D09 records issued object-state. D10 records authority, terms, debt, return obligation, monitoring, and legal/faction consequence.

## Source-local law systems

Donor law levels, wanted ratings, bounty systems, legal codes, ownership models, salvage law, starship registry, cyberware licensing, contraband tables, reputation-based access, noble legitimacy, inheritance law, sanctuary laws, domain edicts, and source-local courts normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_law_authority_state_record:
  law_record_ref: string
  record_type: string
  authority_refs: []
  jurisdiction_scope:
    territory_refs: []
    location_refs: []
    faction_refs: []
    actor_refs: []
    object_refs: []
    platform_refs: []
    source_local_refs: []
  legal_relation:
    owner_refs: []
    possessor_refs: []
    custodian_refs: []
    claimant_refs: []
    recognized_user_refs: []
    disputed_party_refs: []
  legitimacy_state: string
  restriction_state: string
  enforcement_profile:
    enforcement_type: string
    severity: string
    visibility: string
    enforcement_capacity: string
    expiration_or_decay: string
    resolution_conditions: []
  personhood_rights_profile:
    subject_refs: []
    recognition_state: string
    rights_notes: string
  requisition_profile:
    issued_asset_refs: []
    authority_basis: []
    return_terms: []
    debt_or_obligation_refs: []
    monitoring_terms: []
  source_local_boundary:
    retained_rules: []
    prohibited_generalizations: []
    promotion_requirements: []
  owner_handoffs:
    D06: []
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, disputed, resolved, expired, suppressed, source_local, escalated]
```

## Acceptance criteria

A law/authority record is valid when it separates jurisdiction from control; separates ownership, possession, custody, use, access, requisition, salvage, inheritance, sacred claim; separates legal status, legitimacy, and recognition; supports personhood recognition without taking over D08; treats enforcement as pressure, not AI; and blocks donor law levels/wanted tracks from default import.
