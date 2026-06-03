# D06-10 Runtime Schema and UI Handoff

**File ID:** `D06-10`  
**Pack:** Astra Ascension D06 — Route, Path, Principle, Technique, and Donor Class Normalization Doctrine  
**Version:** v0_1  
**Status:** Design doctrine draft generated from accepted D06 decisions.  
**Purpose:** Define D06 record families, durable thresholds, visibility states, UI grouping, and owner-file handoff state without finalizing implementation schemas.

## Standing D06 boundary

D06 owns formal route identity, Path identity, Route Kernels, route facets, Route Feature Ledgers, Techniques, Principle / Concept route facets, route development, multipath / confluence, profession-route formalization, source-local route conversion, and donor class normalization.

D06 does **not** own D03 Power Economy costs, carriers, Expressions, reservoirs, burdens, or confluence math; D04 proof sufficiency, level, tier, Awakening, Development Picks, breakthroughs, capstone, or Ascension Access; D05 skills, professions, knowledge, training, research, methods, and synthesis substrate; D07 harm, corruption, madness, mutation harm, overload, identity erosion, or recovery; D08 companions, summons, spirits, AI, bonds, or nonhuman actor-state mechanics; D09 relics, tools, implants, weapons, vehicles, ships, mechs, or platforms; D10 factions, rank, law, reputation, territory, settlement, economy, or world-state; final runtime/database schemas; canon sourcebook prose; or live-play GM behavior.

D06 records candidates, structure, permissions, limits, and owner-file handoffs. It does not use route language to bypass the owners above.


## 1. Doctrine-shape warning

D06 record shapes are doctrine handoff structures. They are not final runtime schemas, database tables, UI components, or serialization law.

## 2. Tiered record model

D06 uses three record tiers:

| Tier | Use |
|---|---|
| Ephemeral | Temporary route interpretation during a scene. |
| Session-relevant | Candidate or state information likely to matter soon. |
| Durable | Long-term route identity, facet, feature, technique, Principle, source, confluence, mutation, source-local boundary, or owner handoff. |

## 3. Record families

D06 may define records for:

- Route Kernel;
- Route Authorization Packet;
- Route Facet;
- Route Feature Ledger;
- Principle / Concept facet;
- Technique;
- Technique Set;
- Route Development;
- Route Confluence;
- Route Source;
- Donor Route Normalization;
- Source-local Boundary.

## 4. Durable record thresholds

Durable D06 record required when:

- Route becomes candidate, offered, selected, active, dormant, severed, fused, mutated, source-local, scarred, or retired;
- Authorization Packet is created;
- facet state changes;
- Route Feature Ledger entry changes state;
- Technique is created, authorized, blocked, corrupted, externalized, or source-localized;
- Principle depth, contradiction, or risk changes;
- route branch, drift, scar, mutation, stabilization, severance, fusion, or confluence occurs;
- profession, faction, school, lineage, or donor package sources a route;
- source-local boundary is needed;
- owner-file handoff is required.

No durable record is required for passing flavor, unsupported route ideas without consequence, ordinary use of recorded Technique, minor resonance without proof/effect, or unpursued UI suggestions.

## 5. Visibility states

D06 supports visible, discovered, offered, latent, hidden, obscured, source-local, blocked, dangerous, and retired visibility.

Hidden states must not create arbitrary punishment. They should surface through assessment, consequence, teacher feedback, research, proof events, D04 transition, D07 harm, D09 anchor behavior, D10 world response, or direct evidence.

## 6. UI grouping

Future UI should group route data by:

- Path / Route Summary;
- Facets;
- Features;
- Techniques;
- Growth;
- Risks / Constraints;
- Sources;
- Multipath;
- Conversion Notes.

Player-facing summaries should show useful state first. Raw doctrine detail should be expandable or backend-facing.

## 7. Owner-file handoff state

Cross-system records must preserve handoff state: pending D03, pending D04, pending D05, pending D07, pending D08, pending D09, pending D10, source-local, blocked, or escalated.

Examples:

- Mech-Synced Ash Cavalier: active Route; pending D09 for platform Technique; pending D07 for neural feedback.
- Glass-Tomb Archivist: active Principle feature; pending D07 for identity bleed.
- Thorn-Court Mediator: source-local social Technique; pending D10 court law.
- Fungal Courier: feature blocked outside humid routes until D08 actor physiology and D10 environment validate it.

## 8. Source-local boundary records

Source-local boundaries are durable records, not comments. They must identify source, boundary condition, allowed use, prohibited generalization, promotion requirements, owner handoffs, canon status, and validation state.

## 9. Doctrine shapes

```yaml
route_kernel_record:
  route_id: string
  actor_ref: string
  path_name: string
  route_state: candidate | latent | offered | selected | active | dormant | scarred | coerced | corrupted | externalized | source_local | unstable | rejected | severed | fused | mutated | retired
  route_sources: []
  authorization_packet_ref: string
  route_facets: []
  route_feature_ledger_ref: string
  technique_refs: []
  principle_refs: []
  permissions: []
  limits: []
  source_local_boundary_ref: null
  owner_handoffs:
    D03: []
    D04: []
    D05: []
    D07: []
    D08: []
    D09: []
    D10: []
  visibility_state: visible | discovered | offered | latent | hidden | obscured | source_local | blocked | dangerous | retired
  validation_state: authorized | pending_proof | pending_choice | pending_owner_file | dangerous | source_local | blocked | escalated
```

```yaml
source_local_boundary_record:
  boundary_id: string
  construct_ref: string
  construct_type: route | facet | feature | technique | technique_set | principle | school | donor_package | resource | other
  source_name: string
  boundary_condition: string
  allowed_use: []
  prohibited_generalization: []
  promotion_requirements: []
  owner_handoffs: []
  canon_status: source_local | candidate_for_review | rejected | promoted | retired
  validation_state: active | pending_review | blocked | escalated
```

## 10. Rule

The backend should preserve validation, visibility, handoff, and source-local boundaries. The UI should present route state by function, not raw doctrine sprawl.
