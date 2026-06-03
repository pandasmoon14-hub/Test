# D10-06 Reputation, Relationship, Favor, Debt, Grudge, Kinship, Betrayal, and Social Memory Register

## Purpose

This file defines relational world-state. It absorbs adversarial and kinship pressure as structured state without becoming live-play AI, dialogue behavior, romance system, or social encounter mechanics.

## Core rule

D10 records persistent relational memory: who remembers what, how they interpret it, how strongly it matters, whether it is public or hidden, whether it decays, what obligations or grudges exist, and what relationship state may influence future access, faction response, law, social standing, or narrative consequence. D10 does not decide live dialogue or simulate all social behavior.

## Reputation vs relationship

A reputation is a general belief or social standing held by an actor, faction, institution, community, public, or source-local audience. A relationship is a specific persistent connection between entities.

Reputation may exist without direct relationship. Relationship may be private and unknown to public reputation.

## Subject and holder

The subject is the actor, party, faction, object-symbol, location, lineage, route, form-state, or event being judged. The holder is the actor, faction, community, institution, public, hidden faction, family, crew, or source-local system holding the memory or opinion.

The same subject can have different reputations with different holders.

## Relationship axes

D10 uses multiple axes rather than one score: valence, intensity, trust, fear, respect, affection/kinship, obligation, grudge, rivalry, resentment, loyalty, suspicion, and source-local axis.

“High respect, high fear, low trust” is different from simple hostility.

## Summary relational states

States may include unknown, recognized, friendly, trusted, allied, protected, patron/client, kin/oath-bonded, indebted, respected rival, suspicious, resentful, betrayed, grudge-bearing, feared, hostile, vendetta, reconciled, publicly hostile/privately allied, and source-local.

## Social memory record

A social memory record includes memory reference, remembered event, subject, holder, interpretation, valence, intensity, visibility, truth status, decay/permanence, obligations, grudges, rumors, source-local boundary.

Interpretation matters. The same event can produce gratitude in one community, humiliation in a rival, and useful destabilization in a hidden faction.

## Favor, debt, obligation, reciprocity

D10 distinguishes favor, debt, life debt, oath debt, contract debt, patronage, protection, reciprocal expectation, unpaid debt, and source-local favor.

Debt can be positive or coercive. Favor can become resentment if ignored. Patronage can become support, leverage, hierarchy, or control.

## Grudge, rivalry, revenge, vendetta

Grudge sources include harm, humiliation, betrayal, theft, relic desecration, oath breach, killing kin, public insult, faction defeat, loss of territory, corruption spread, sabotage, abandonment, and source-local trigger.

States include minor grievance, active grudge, rivalry, revenge intent, vendetta, inherited grudge, dormant grudge, reconciled grudge, and source-local.

D10 records adversarial memory; it does not choose ambushes.

## Kinship, loyalty, reconciliation

Kinship sources include rescue, shared danger, sacrifice, oath, adoption, crew membership, lineage, faction initiation, spiritual bond, companion bond, patronage, mutual secrecy, restored honor, and source-local bond.

States include affinity, gratitude, shared trial, oath-bond, crew-bond, family/lineage bond, companion bond, patronage bond, protective loyalty, reconciled bond, and source-local.

Reconciliation does not erase history.

## Betrayal, jealousy, resentment

Damage states include strained, resentful, jealous, distrustful, betrayed, alienated, hostile turn, recoverable, irreparable, and source-local. Triggers include broken promise, unpaid debt, favoritism, abandonment, public humiliation, revealed secret, collateral harm, conflicting obligation, taboo violation, object theft, or unauthorized restricted form/power use.

## Public/private/hidden/false reputation

D10 distinguishes public reputation, private reputation, hidden relation, secret alliance, false reputation, rumored reputation, misattributed reputation, propaganda-shaped reputation, suppressed memory, disputed reputation, and source-local.

A false reputation can create real consequences.

## Scope, persistence, and inheritance

Scope may be personal, household/family, crew/party, community, institution, faction, settlement, region, cross-factional, public/world-scale, or source-local.

Persistence modes include immediate, short-term, decaying, reinforced, escalating, dormant, ongoing, permanent, historical, and source-local.

Relationships can pass through family, lineage, house, clan, crew, guild, sect, faction, companion group, patron-client network, religious order, AI collective, or source-local institution. D10 records inherited memory but does not simulate all individual beliefs.

## Source-local reputation systems

Donor reputation ranks, faction favor points, influence scores, bond tracks, loyalty tracks, relationship clocks, nemesis systems, patron favor, honor, infamy, heat/wanted levels, attitude categories, social standing, kingdom loyalty, romance/companion affinity normalize by function or remain source-local.

## Record doctrine shape

```yaml
d10_reputation_relationship_state_record:
  relation_ref: string
  record_type: string
  subject_refs:
    actor_refs: []
    party_refs: []
    faction_refs: []
    institution_refs: []
    object_symbol_refs: []
    place_refs: []
    source_local_refs: []
  holder_refs:
    actor_refs: []
    faction_refs: []
    institution_refs: []
    community_refs: []
    public_refs: []
    hidden_faction_refs: []
    source_local_refs: []
  relationship_axes:
    valence: string
    intensity: string
    trust: string
    fear: string
    respect: string
    affection_kinship: string
    obligation: string
    grudge: string
    rivalry: string
    resentment: string
    loyalty: string
    suspicion: string
  summary_state: string
  memory_profile:
    remembered_event_refs: []
    interpretation: string
    truth_state: string
    visibility: string
  obligation_profile:
    favor_refs: []
    debt_refs: []
    oath_refs: []
    patronage_refs: []
    protection_refs: []
    unpaid_obligation_refs: []
  damage_profile:
    betrayal_refs: []
    resentment_refs: []
    jealousy_refs: []
    alienation_refs: []
    reconciliation_refs: []
  inheritance_profile:
    inheritance_paths: []
    inheriting_group_refs: []
    inherited_from_refs: []
  persistence:
    mode: string
    decay_conditions: []
    reinforcement_conditions: []
    resolution_conditions: []
    historical_retention_required: boolean
  source_local_boundary:
    retained_rules: []
    prohibited_generalizations: []
    promotion_requirements: []
  owner_handoffs:
    D07: []
    D08: []
    D09: []
    source_local: []
  lawful_outcome: [direct_d10_mapping, normalized_register_mapping, source_local_retained, quarantined, escalated]
  validation_state: [active, hidden, decayed, resolved, historical, source_local, escalated]
```

## Acceptance criteria

A relational record is valid when it separates reputation from relationship; uses multiple axes rather than one score; distinguishes favor, debt, obligation, patronage, protection; supports grudge/vendetta without combat AI; supports kinship/reconciliation without narration behavior; separates public/private/hidden/false/rumored states; supports inherited memory; and blocks donor reputation systems from default import.
