# C00 Shared Content Record Base and Schema Registry Doctrine

## 1. Purpose and status

C00 defines schema-layer doctrine for the shared conversion record base and schema-registry behavior used by downstream C01-C14 families.

Status posture:
- This file is schema-todo fulfillment drafted as schema-draft material.
- This file is not marked current canon.
- This file does not define runtime event schemas, command lifecycle, event-sourced state model, state delta validator, context packet compiler, hidden-information runtime state, live-play behavior, canon promotion procedure, final mechanics, accepted lexicon terms, final sourcebook prose, or donor record formats as Astra defaults.

Registry identity and governance anchors (source of truth):
- file_id: C00;
- filename: `C00_shared_content_record_base_and_schema_registry.md`;
- proposed_path: `docs/doctrine/schema/C00_shared_content_record_base_and_schema_registry.md`;
- layer: `4_schema_base`;
- phase: `2`;
- owner: Astra Doctrine Council - Schema Working Group.

## 2. What this file owns

C00 owns schema-layer grammar for:
- provenance;
- source-local records;
- rejected imports;
- canon eligibility;
- confidence;
- review routing;
- versioning;
- cross-reference fields;
- schema registry behavior.

C00 additionally owns:
- required base-field constraints for shared conversion records;
- schema-family inheritance posture that C01-C14 must follow;
- registry alignment rules that prevent untracked schema sprawl.

## 3. What this file must not own

C00 must not define:
- final mechanics;
- canon acceptance;
- canon promotion procedure;
- runtime state schema;
- runtime state fields;
- runtime event schemas;
- command lifecycle behavior;
- event-sourced state model;
- state delta validation behavior;
- context packet compiler behavior;
- hidden-information runtime state;
- live-play behavior;
- donor field names as Astra defaults;
- donor record shapes;
- accepted lexicon terms;
- final sourcebook prose.

C00 does not draft C01-C14, K-layer, B-layer, R-layer, or T-layer files.

## 4. Required base record grammar

### 4.1 Provenance grammar

Every shared record must carry explicit provenance fields that preserve:
- donor/source identifier;
- source location granularity (document/section/page or equivalent source-local locator);
- extraction/ingest timestamp and pipeline origin;
- transformation lineage chain from donor material to current record state.

### 4.2 Source-local record grammar

Source-local records must:
- preserve donor-authored semantics without Astra-canon reinterpretation;
- be explicitly typed as source-local to prevent accidental canon uptake;
- retain reversible linkage to original provenance.

### 4.3 Rejected-import grammar

Rejected-import records must:
- capture rejected candidate identity;
- state explicit rejection reason code(s);
- preserve evidence pointer(s) back to source-local/provenance records;
- record reviewer and decision timestamp for auditability.

### 4.4 Canon-eligibility grammar

Canon-eligibility fields must:
- encode eligibility posture only (e.g., ineligible/candidate/review-required);
- never imply canon acceptance;
- require downstream K-layer adjudication before any canon state change.

### 4.5 Confidence grammar

Confidence fields must:
- separate extraction confidence from doctrine-fit confidence;
- carry calibrated score/band plus rationale note;
- preserve uncertainty rather than collapse ambiguous records into invented certainty.

### 4.6 Review-routing grammar

Review-routing fields must:
- route records to doctrine, schema, lexicon, or runtime review queues as applicable;
- encode escalation targets for contradiction or boundary violations;
- preserve review status without mutating source evidence.

### 4.7 Versioning grammar

Versioning fields must:
- support immutable record identity with monotonic revision lineage;
- track supersedes/superseded-by relationships;
- preserve compatibility metadata for downstream schema consumers.

### 4.8 Cross-reference grammar

Cross-reference fields must:
- link related records across schema families via stable IDs;
- distinguish asserted relation type from inferred relation type;
- preserve directional semantics for dependency and trace queries.

### 4.9 Schema-registry behavior grammar

Schema-registry behavior must:
- require each schema-family record to inherit the C00 base-field contract;
- require registry-tracked identity/path ownership before schema promotion;
- refuse unregistered schema files as Astra-authoritative;
- preserve hard-lock sequencing from registry dependencies/unlocks;
- maintain audit-visible change logs for base grammar updates.

## 5. Runtime phase boundary: explicit non-collapse rule

C00 explicitly forbids runtime phase collapse.

Runtime phase collapse means collapsing conversion/schema records directly into runtime behavior authority without required downstream governance gates.

Therefore C00 mandates:
- schema-layer records remain conversion-governance artifacts, not runtime-state authority;
- runtime behavior may consume C-layer outputs only through downstream approved layers;
- no C00 field may be interpreted as direct authorization for runtime execution semantics.

## 6. Conversion mapping and contradiction posture

- Map donor evidence into C00 base grammar before family-specific shaping.
- Preserve source-local evidence when normalization would invent mechanics, runtime state, or lexicon acceptance.
- Route contradictions through review-routing and escalation fields; do not erase tension by forced normalization.
- Rejected imports remain first-class auditable records, never silent drops.

## 7. Dependencies and unlock posture

C00 dependency posture (registry source of truth):
- Depends on A01-A15;
- Is blocked by A01-A15;
- Unlocks C01-C14 and K03.

C00 does not bypass registry hard locks and does not authorize promotion outside registry sequencing.

## 8. Handoff contract to C01-C14

C01-C14 must:
- include all required C00 base fields;
- extend only within family scope while preserving C00 boundary rules;
- preserve source-local and rejected-import audit traces;
- avoid donor-shape default adoption;
- avoid runtime-authority claims.

## 9. Promotion and lifecycle posture

- This file remains draft/not-current until registry promotion gates are satisfied.
- C00 defines schema governance posture, not final doctrine canon, runtime canon, or play canon.
- Substantive changes require registry-aware versioning and re-review.
