# D06-09 Source-local Route Conversion and Donor Class Normalization

**File ID:** `D06-09`  
**Pack:** Astra Ascension D06 — Route, Path, Principle, Technique, and Donor Class Normalization Doctrine  
**Version:** v0_1  
**Status:** Design doctrine draft generated from accepted D06 decisions.  
**Purpose:** Define how donor class-like packages are decomposed, routed, retained source-locally, quarantined, or escalated.

## Standing D06 boundary

D06 owns formal route identity, Path identity, Route Kernels, route facets, Route Feature Ledgers, Techniques, Principle / Concept route facets, route development, multipath / confluence, profession-route formalization, source-local route conversion, and donor class normalization.

D06 does **not** own D03 Power Economy costs, carriers, Expressions, reservoirs, burdens, or confluence math; D04 proof sufficiency, level, tier, Awakening, Development Picks, breakthroughs, capstone, or Ascension Access; D05 skills, professions, knowledge, training, research, methods, and synthesis substrate; D07 harm, corruption, madness, mutation harm, overload, identity erosion, or recovery; D08 companions, summons, spirits, AI, bonds, or nonhuman actor-state mechanics; D09 relics, tools, implants, weapons, vehicles, ships, mechs, or platforms; D10 factions, rank, law, reputation, territory, settlement, economy, or world-state; final runtime/database schemas; canon sourcebook prose; or live-play GM behavior.

D06 records candidates, structure, permissions, limits, and owner-file handoffs. It does not use route language to bypass the owners above.


## 1. Core rule

A donor class-like package is evidence, not authority. D06 decomposes donor packages by function and routes elements to the proper Astra owner. Donor tables, resources, level logic, metaphysics, terminology, and packaging do not become Astra law unless normalized and promoted.

## 2. Donor package problem

A donor class may bundle identity, progression table, features, spell list, resource economy, proficiencies, equipment, faction lore, metaphysics, advancement math, action economy, balance assumptions, setting assumptions, capstone, and multiclass logic. Astra separates these layers.

## 3. Lawful outcomes

Every donor construct must land in a lawful outcome:

- direct Astra mapping;
- normalized Astra mapping;
- source-local retained construct;
- Route candidate;
- Route facet;
- Route Feature;
- Technique candidate / Technique Set;
- D03 Expression / resource handoff;
- D04 advancement handoff;
- D05 competency / profession handoff;
- D07 harm / corruption handoff;
- D08 actor / companion handoff;
- D09 item / platform handoff;
- D10 faction / world handoff;
- quarantine;
- doctrine escalation.

## 4. Decomposition procedure

1. Identify package type: class, subclass, prestige class, profession class, school, archetype, path, sect role, cultivation lineage, playbook, hybrid package.
2. Separate identity from mechanics.
3. Identify route-facing material.
4. Identify non-route material.
5. Determine source-local status.
6. Create Astra outputs.
7. Record rejected donor assumptions.

## 5. Donor routing table

| Donor element | Astra handling |
|---|---|
| Class name | Path name candidate, source-local label, or rejected term. |
| Class identity | D06 Route candidate or source-local Route. |
| Subclass | Route branch, facet, feature option, or source-local package. |
| Prestige class | Advanced branch, second Route, fusion candidate, or source-local Route. |
| Archetype | D06 Archetype facet if functional; not subclass by default. |
| Class feature | Route Feature, Technique, D03 Expression, D05 Method, D09 item feature, D10 faction feature, or source-local. |
| Spell / power list | D03 Expression family, D06 Technique Set, source-local list, or escalation. |
| Class resource | D03 Power Economy or source-local retained resource. |
| Proficiencies | D05 competencies or training access. |
| Equipment package | D09 starting kit / item / tool handling. |
| Faction / order | D10 institution plus possible D06 route source. |
| Oath / pact | D06 constraint / Principle / source plus D07 / D08 / D09 / D10 handoffs. |
| Companion feature | D08 actor / companion; possible D06 feature or Technique. |
| Vehicle / mech feature | D09 platform; possible D06 anchor. |
| Advancement table | D04 handling; not imported directly. |
| Capstone | D04 capstone candidate plus D06 route review. |
| Metaphysics | Source-local, lexicon candidate, quarantine, or escalation. |

## 6. Source-local retention

Source-local retention is valid and expected when the construct depends on donor cosmology, setting institutions, local resource models, donor action economy, unadopted terms, local species metaphysics, or unbuilt Astra owner frameworks.

Retention must record boundary, allowed use, prohibited generalization, owner handoffs, review condition, and canon status.

## 7. Promotion requirements

A source-local Route or donor construct may be considered for Astra-native promotion only when:

1. It maps cleanly to Route Kernel structure.
2. It does not require donor cosmology as universal law.
3. Permissions and limits are defined.
4. Owner-file handoffs are resolved.
5. Terminology is lexicon-approved or normalized.
6. It supports corpus-scale use.
7. It does not duplicate existing Astra structure unnecessarily.
8. It has conversion evidence or strong design need.
9. It can be expressed without hidden donor mechanics.

Promotion is not automatic.

## 8. Quarantine and escalation

Quarantine when ownership is unclear, donor metaphysics conflict with Astra, power scale is unsupported, no D03 cost framework exists, no D04 gate exists, source-local term would leak, mechanics require missing future files, or conversion would require invention.

Escalate when a construct exposes a missing Astra framework required at corpus scale.

## 9. Varied examples

- Armored duelist class: identity → Route candidate; proficiencies → D05; stances → D06 Techniques; armor → D09; level table → D04; resource → D03 or source-local.
- Study caster: knowledge / research → D05; spellbook → D09; slots → D03 or source-local; schools → Domains / Technique Sets; academy → D10.
- Beastmaster: handling → D05; companion → D08; commands → D06 Techniques; route identity → candidate.
- Mech pilot: platform operation → D05; mech → D09; sync → D09 / D08 / D03 depending function; license → D10.
- Cultivation sect path: meridians → D03 or source-local; Dao → Principle source-local; tribulation → D04; sect rank → D10.
- Social playbook: intrigue moves → D06 / D05; reputation / favors → D10; emotional leverage → D05 or D07.
- Territory lord: leadership → D05 / D10; settlement → D10; territory powers → D10 / D06 / D03.

## 10. Normalization record

```yaml
donor_route_normalization_record:
  source_construct_id: string
  donor_label: string
  donor_construct_type: class | subclass | prestige_class | archetype | school | sect_path | profession_class | playbook | faction_package | companion_class | platform_class | hybrid_package | other
  source_local_boundary: string
  astra_outputs:
    route_candidates: []
    source_local_routes: []
    route_facets: []
    route_features: []
    technique_candidates: []
    technique_sets: []
    d03_expression_or_resource_handoffs: []
    d04_advancement_handoffs: []
    d05_competency_handoffs: []
    d07_risk_handoffs: []
    d08_actor_companion_handoffs: []
    d09_item_platform_handoffs: []
    d10_faction_world_handoffs: []
    quarantined_constructs: []
    escalation_items: []
  donor_assumptions_rejected: []
  terminology_status: retained_source_local | normalized | rejected | lexicon_candidate
  validation_state: direct_mapping | normalized_mapping | source_local_retained | quarantined | escalated
```

## 11. Rule

Donor identity may be preserved as signal. Donor structure is not imported as Astra law.
