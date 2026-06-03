# D06-07 Route Fusion, Multipath, and Confluence

**File ID:** `D06-07`  
**Pack:** Astra Ascension D06 — Route, Path, Principle, Technique, and Donor Class Normalization Doctrine  
**Version:** v0_1  
**Status:** Design doctrine draft generated from accepted D06 decisions.  
**Purpose:** Define governed multipath and route confluence without donor multiclass stacking.

## Standing D06 boundary

D06 owns formal route identity, Path identity, Route Kernels, route facets, Route Feature Ledgers, Techniques, Principle / Concept route facets, route development, multipath / confluence, profession-route formalization, source-local route conversion, and donor class normalization.

D06 does **not** own D03 Power Economy costs, carriers, Expressions, reservoirs, burdens, or confluence math; D04 proof sufficiency, level, tier, Awakening, Development Picks, breakthroughs, capstone, or Ascension Access; D05 skills, professions, knowledge, training, research, methods, and synthesis substrate; D07 harm, corruption, madness, mutation harm, overload, identity erosion, or recovery; D08 companions, summons, spirits, AI, bonds, or nonhuman actor-state mechanics; D09 relics, tools, implants, weapons, vehicles, ships, mechs, or platforms; D10 factions, rank, law, reputation, territory, settlement, economy, or world-state; final runtime/database schemas; canon sourcebook prose; or live-play GM behavior.

D06 records candidates, structure, permissions, limits, and owner-file handoffs. It does not use route language to bypass the owners above.


## 1. Core model

D06 uses **Governed Multipath and Route Confluence**. Actors may have multiple route pressures and, with authorization, multiple active Routes. Multiple Routes do not automatically stack features, Techniques, Domains, Principles, or Development Pick permissions.

## 2. Multipath vs. fusion

**Multipath** means the actor has more than one active or semi-active route structure. The Routes remain distinct.

**Fusion** means two or more Routes become a new combined identity or route structure. Fusion is heavier and requires proof, compatibility or contradiction resolution, rewritten permissions / limits, owner handoffs, and state delta.

## 3. Relationship states

Route relationships may be independent, primary / secondary, latent, dormant, subordinate, parallel, entangled, synergistic, conflicted, dominating, fusing, fused, splitting, severed, source-local, or escalated.

## 4. Compatibility bands

| Band | Meaning |
|---|---|
| compatible | coexist cleanly. |
| complementary | support one another in bounded ways. |
| tense | coexist with friction. |
| contradictory | pull against each other and require management. |
| incompatible | cannot remain active together without mutation, suppression, severance, or exception. |
| unknown | requires research, proof, teacher, or validation. |
| source-local | compatibility valid only inside bounded context. |

Compatibility is function-based, not name-based. Mercy and Severance may conflict or fuse as Mercy-Through-Severance depending on proof.

## 5. Route Confluence

A Route Confluence is a governed interaction between Routes or route facets. It may produce shared features, limited cross-route technique access, compound Principle, merged Domain relation, branch, scar, conflict, mutation, fusion candidate, severance pressure, source-local exception, or owner-file handoff.

Route Confluence is not automatic feature stacking.

## 6. Feature Ledger interaction

Rules:

1. Features do not automatically transfer between Routes.
2. A feature may become cross-route only if Route Confluence authorizes it.
3. A feature may be shared, duplicated, transformed, blocked, retired, or fused.
4. If two features overlap, the actor does not automatically get both benefits.
5. D04 validates Development Pick use.
6. D03 validates powered feature interactions.
7. D07 validates overload, contradiction, corruption, and identity damage.

## 7. Multipath load

Multiple Routes create opportunity and burden. Burdens may include feature conflict, Development Pick dilution, training strain, proof fragmentation, Principle dissonance, identity instability, anchor dependency, social obligation conflict, source-local lock, D03 carrier/resource incompatibility, or D07 overload.

## 8. Fusion gates

Fusion should require:

- at least two active or strong candidate Routes / facets;
- proof of meaningful interaction;
- compatibility or contradiction-resolution basis;
- defined new identity or compound structure;
- retained, transformed, retired, or blocked features identified;
- permissions and limits rewritten;
- owner-file handoffs resolved;
- D04 authorization if advancement-relevant;
- D07 review if identity harm or overload is involved;
- state delta recorded.

## 9. D03 confluence vs. D06 confluence

D03 confluence handles Power Economy interaction, cost partition, carrier tolerance, Expression re-authoring, energetic compatibility, overdraw, backlash, and resource burden.

D06 confluence handles route identity interaction, facet compatibility, Principle / Domain overlap, Technique Set interaction, Route Feature Ledger interaction, route fusion, mutation, and severance.

Both may apply, but they are not the same system.

## 10. Source-local multiclass handling

Donor multiclass systems normalize into source-local Routes, route facets, Technique Sets, Route Features, D05 competencies, D03 Expressions, D04 picks, or escalation. Donor multiclass rules are not imported directly.

## 11. Varied examples

- **Siege-Kettle Quartermaster** + **Refuge-Camp Magistrate**: complementary confluence; Emergency Ration Authority candidate; D10 handoff.
- **Truth-Sworn Witness** + espionage route pressure: contradictory; possible scar, reinterpretation, split, severance, or corruption.
- **Crow-Marked Rooftop Scout** binds fear-mask relic: unknown / tense; D08 crow bond, D09 relic, D07 fear corruption risk.
- Fungal courier Continuity + city courier Roads: complementary fusion candidate **Spore-Road Envoy**; D08 / D10 handoffs.
- Donor “blade priest / storm mage”: blade practice D05 / D06, priest identity D10 / D06, storm magic D03 / D06, package source-local.

## 12. Doctrine shape

```yaml
route_confluence_record:
  confluence_id: string
  actor_ref: string
  route_refs: []
  facet_refs: []
  confluence_type: multipath | primary_secondary | parallel | synergistic | conflicted | dominating | fusing | fused | splitting | severed | source_local | escalated
  compatibility: compatible | complementary | tense | contradictory | incompatible | unknown | source_local
  trigger_source: []
  interaction_summary: string
  permissions_added: []
  permissions_blocked: []
  features_shared: []
  features_transformed: []
  features_retired: []
  principle_changes: []
  domain_changes: []
  technique_set_changes: []
  risks: []
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D07: []
    D08: []
    D09: []
    D10: []
  validation_state: authorized | pending_proof | pending_owner_file | dangerous | source_local | blocked | escalated
```

## 13. Rule

Multipath is not donor multiclassing. Fusion is not routine. Route features, Techniques, Domains, and Principles do not stack across Routes without authorized confluence.
