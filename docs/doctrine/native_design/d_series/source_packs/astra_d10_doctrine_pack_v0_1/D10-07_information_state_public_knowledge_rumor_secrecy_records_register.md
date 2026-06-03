# D10-07 Public Knowledge, Rumor, Secrecy, Records, Intelligence, and Information-State Register

## Purpose

This file defines information-state: who knows what, who believes what, what is false, what is hidden, what is suppressed, what is recorded, what is rumored, and what can later be revealed.

## Core rule

D10 records information-state: what is true, what is believed, who knows it, how reliable it is, how visible it is, where it is recorded, whether it is spreading, whether it is suppressed, and what future consequence depends on it. D10 does not decide how the player discovers it or how the narrator presents it.

## Truth-state vs. knowledge-state

Truth-state records whether information corresponds to underlying world-state. Knowledge-state records who knows, believes, suspects, records, hides, distorts, or disputes it.

Truth states include true, false, partial, outdated, misleading, unknown, disputed, and source-local.

Knowledge states include public knowledge, private knowledge, faction knowledge, actor knowledge, witness knowledge, secret, hidden truth, rumor, misinformation, propaganda, suppressed, forgotten, archived, and source-local.

A fact can be true and hidden. A rumor can be false and public. A record can be outdated.

## Information subjects

Information may concern actor, faction, location, territory, object, relic, platform, law, ownership, resource, route, Technique, Principle, corruption zone, event, relationship, personhood status, or source-local construct.

Owner substrates remain outside D10.

## Holder and audience

Holder types include actor, party/crew, faction, subfaction, institution, community, public audience, hidden faction, archive, AI memory, spirit memory, legal record, map, rumor network, and source-local holder.

Audience scopes include personal, household, crew, community, institution, faction, settlement, regional, cross-factional, world-scale, hidden network, and source-local.

## Records and archives

Record/archive types include public record, faction archive, secret archive, personal record, legal record, object-bound record, map record, rumor record, suppressed record, and source-local record.

D09 owns record objects when relevant. D10 owns information-state.

## Rumor, misinformation, propaganda

Rumor states include emerging, spreading, widespread, fading, replaced, confirmed, disproven, weaponized, and source-local.

Misinformation is false or misleading belief spread without necessarily deliberate intent. Propaganda is deliberate belief-shaping.

Propaganda records include originator, audience, subject, claim, truth-state, channel, intended effect, current reach, counter-claims, and source-local boundary.

## Witness memory and testimony

Witness records track witness actor/group, witnessed event, interpretation, confidence, reliability, bias, fear/coercion, willingness to testify, public/private status, decay/distortion, and source-local rule.

D08 owns actor memory substrate when mechanically relevant. D10 owns social/legal information consequence.

## Intelligence and surveillance

Intelligence sources may include spy report, surveillance record, intercepted message, hacked archive, divination report, scout map, informant claim, faction dossier, sensor log, AI analysis, spirit vision, and source-local intelligence system.

States include raw, verified, unverified, contradictory, compromised, forged, planted, outdated, classified, leaked, and source-local.

D10 records who has it and reliability. D05/later runtime owns collection.

## Discovery and revelation

Discovery states include undiscovered, discovered privately, discovered by faction, publicly revealed, partially revealed, misrevealed, reconcealed, leaked, exposed, and source-local.

Revelation can create reputation shifts, legal action, faction conflict, resource rush, panic, treaty collapse, or reconciliation.

## Decay and persistence

Information may be immediate, short-term, ongoing, decaying, distorted, archived, suppressed, forgotten, mythologized, permanent, historical, or source-local.

Persistence anchors include public record, oath memory, legal record, faction archive, sacred tradition, propaganda campaign, inherited grievance, relic memory, AI archive, immortal witness, and source-local permanence.

## False attribution and disputed accounts

D10 supports wrong credit, wrong blame, framed events, misattributed disasters, false relic theft accusations, suppressed evidence, and competing histories.

Disputed accounts should record claim holders, evidence state, public leaning, suppressed evidence, faction interest, resolution conditions, and historical retention.

## Propagation without full simulation

Propagation states include contained, leaking, circulating, institutionalized, suppressed, countered, saturated, fragmented, and source-local.

D10 tracks spread state and scope; it does not simulate every conversation.

## Source-local information systems

Donor rumor tables, clue webs, revelation lists, secret clocks, library research tracks, faction intelligence ratings, surveillance systems, wanted posters, prophecy records, map discovery rules, knowledge skill categories, mystery scenario nodes, and source-local truth/rumor mechanics normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_information_state_record:
  information_ref: string
  record_type: string
  subject_refs:
    actor_refs: []
    faction_refs: []
    location_refs: []
    territory_refs: []
    object_refs: []
    platform_refs: []
    route_refs: []
    event_refs: []
    law_refs: []
    resource_refs: []
    source_local_refs: []
  truth_state: string
  knowledge_state: string
  holder_refs:
    actor_refs: []
    faction_refs: []
    institution_refs: []
    community_refs: []
    public_scope_refs: []
    archive_refs: []
    source_local_refs: []
  visibility_scope: string
  reliability_profile:
    confidence: string
    evidence_refs: []
    source_bias: string
    contradiction_refs: []
    verification_state: string
  propagation_state: string
  discovery_state: string
  persistence:
    mode: string
    decay_conditions: []
    persistence_anchors: []
    resolution_conditions: []
    historical_retention_required: boolean
  consequence_links:
    event_refs: []
    reputation_refs: []
    law_refs: []
    faction_refs: []
    territory_refs: []
    economy_refs: []
  source_local_boundary:
    retained_rules: []
    prohibited_generalizations: []
    promotion_requirements: []
  owner_handoffs:
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, hidden, disputed, disproven, confirmed, suppressed, forgotten, historical, source_local, escalated]
```

## Acceptance criteria

An information-state record is valid when it separates truth-state from knowledge-state; identifies subject, holder, audience, reliability, propagation, discovery, persistence; supports false, rumored, suppressed, archived, and disputed information; routes discovery/research to D05 or later runtime; and blocks donor rumor/clue systems from default import.
