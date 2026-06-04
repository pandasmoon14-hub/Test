# SM00 Schema/Math/Mechanics Master Scope and Sequencing Plan

## 1. Purpose and status

SM00 is the first post-Batch-C schema/math/mechanics planning, readiness, control, and scope file for Astra Ascension. It exists to sequence future work after the Batch C schema-family layer, not to draft final mechanics, exact math, final resolution dice, runtime schema, backend schema, database schema, entity/component/event schema, command lifecycle, context packet contract, save-state shape, sourcebook prose, canon, live-play/GM behavior, training/evaluation corpus creation, or any other implementation contract.

Status posture:
- SM00 is a planning/readiness/scope file only.
- SM00 is not a C-family schema, not C15, not a runtime contract, not final mechanics readiness, not canon readiness, not sourcebook readiness, not live-play readiness, and not training readiness.
- SM00 does not promote C00 or C01-C14, does not invent registry status values, and does not mark anything current, stable_for_family, stable_cross_family, tested_minimum, accepted_canon, runtime_ready, runtime-ready, or canon-ready.
- SM00 uses D00-D19 source packs only as draft source material for gap awareness; D-series authority promotion is explicitly refused.

## 2. Current repository posture

Batch A doctrine exists under setting, advancement, and world files. SM00 must not rewrite Batch A doctrine, collapse its owner boundaries, or treat planning pressure as permission to revise A01-A15 doctrine language.

Batch B is complete through B11. B01-B11 remain operational doctrine and procedure/routing pressure; Batch B is not final mechanics, not final math, not runtime schema, not backend/database contract, not command lifecycle, and not live-play authority.

C00 and C01-C14 exist as Batch C conversion-stage/canon-review schema doctrine. C00 provides the shared content record base and schema-family registry posture. C01-C14 define conversion-stage record-family routing for content extracted from donor material and routed toward Astra-facing review.

The Batch C capstone, `Batch_C_schema_family_integration_conflict_audit_and_readiness_gate.md`, marks the Batch C layer ready with deferred gaps only. Batch C readiness is not canon readiness, runtime readiness, sourcebook readiness, final mechanics readiness, live-play readiness, or training readiness.

D00-D19 source packs are draft source material only. They are not current doctrine, final mechanics, runtime authority, canon, sourcebook prose, live-play behavior, or training authority.

## 3. What Batch C unlocks

Batch C unlocks conversion-stage content record routing across C00 and these C-family records:

- C01 creature/NPC record schema doctrine.
- C02 item/gear record schema doctrine.
- C03 ability/power/technique record schema doctrine.
- C04 relic/implant/installable asset schema doctrine.
- C05 faction/institution record schema doctrine.
- C06 location/site/region record schema doctrine.
- C07 mission/scenario/adventure record schema doctrine.
- C08 vehicle/ship/platform record schema doctrine.
- C09 hazard/environment record schema doctrine.
- C10 table/oracle record schema doctrine.
- C11 companion/summon record schema doctrine.
- C12 crafting/salvage/recipe record schema doctrine.
- C13 map/diagram annotation record schema doctrine.
- C14 source-local setting/cosmology record schema doctrine.
- `pending_schema` as a lawful fallback route when no stable C-family owner exists yet.

C01-C14 make conversion-stage content record routing possible. They provide family ownership, evidence retention, review posture, donor-leakage controls, source-local containment, rejected-donor handling, and canon-review routing. They do not define final math, runtime schemas, canon, sourcebook prose, live-play behavior, final mechanics, backend/database contracts, or accepted lexicon promotion.

Batch C also preserves references to Conversion IR, the lawful outcome taxonomy, and runtime/Gate B as upstream or downstream controls rather than implementation authority. Those references identify handoff boundaries; they do not create command lifecycles, event contracts, context packets, runtime state, save-state shapes, or Gate B runtime behavior.

## 4. What Batch C does not solve

Batch C does not solve:

- final mechanics or exact math;
- final resolution dice or donor dice-system defaults;
- validation schemas or executable validators;
- record instance schemas;
- runtime schema, backend schema, database schema, entity/component/event schema, command lifecycle, context packet contract, or save-state shape;
- canon promotion, accepted lexicon promotion, sourcebook prose, live-play/GM behavior, or training/evaluation corpus creation;
- balance benchmarks, pilot conversion evidence, large-scale corpus conversion evidence, or runtime/Gate B readiness;
- hidden-state handling, protected-truth runtime handling, or RHBF hidden law.

Final math should not be designed before audit, validation, benchmark, and pilot-conversion evidence exist. Without those inputs, math would be donor-shaped by accident, under-tested, disconnected from actual conversion record pressure, and likely to create brittle schemas before the project knows what its records must carry.

## 5. Workstream scope definition

SM00 defines the scope of a future schema/math/mechanics workstream at the planning level only. It may name future owner files cautiously as proposed files, but it does not assert that those owner files exist and does not pre-decide their contents.

The workstream has four separated layers:

1. Schema planning: inventory required validation schemas, instance shapes, provenance/evidence shapes, conflict ledgers, conversion packets, test fixtures, and runtime-prep handoff shapes without drafting final runtime implementation.
2. Math/mechanics planning: inventory unresolved mechanics and benchmark needs without choosing exact values, dice, formulas, economies, class structures, progression tables, or donor defaults.
3. Conversion readiness: separate minimum pilot conversion readiness from large-scale corpus conversion readiness.
4. V1 runtime readiness: identify dependencies for runtime/Gate B without designing runtime schemas, backend/database contracts, entity/component/event schemas, command lifecycles, context packet contracts, or save-state shapes.

## 6. Full schema gap inventory

The schema gap inventory is complete enough for sequencing, not implementation. Required future schema work includes:

- validation schemas;
- record instance schemas;
- cross-record references;
- conversion packet schemas;
- evidence/provenance schemas;
- canon-review schemas;
- conflict ledger schemas;
- pilot conversion output schemas;
- mechanics I/O schemas;
- runtime-prep schemas;
- test fixture schemas.

Each gap must be routed to a named proposed future owner or lawful fallback before implementation. Until then, `pending_schema`, quarantine, review routing, owner assignment, or deferred gap routing are the lawful fallbacks.

## 7. Full math/mechanics gap inventory

The math/mechanics gap inventory names unresolved areas only. It does not set exact math, final mechanics, final resolution dice, donor math defaults, donor statblock defaults, donor economy defaults, donor class/progression defaults, donor dice-system defaults, or donor cosmology defaults.

Required future math/mechanics work includes:

- resolution math;
- difficulty bands;
- action economy;
- timing/cadence;
- cost commitment;
- partial outcome states;
- damage;
- injury;
- conditions;
- resources;
- recovery/recharge;
- progression;
- thresholds;
- character scaling;
- opposition scaling;
- hazards;
- gear/relic scaling;
- abilities/techniques;
- crafting/salvage/requisition;
- faction/social pressure;
- travel/exploration;
- vehicle/platform mechanics;
- companion/summon control;
- table/oracle probability;
- map/spatial abstraction;
- hidden-state handling;
- balance benchmarks.

## 8. Conversion-readiness checklist

Minimum pilot conversion readiness is a narrow, evidence-gathering threshold. It requires enough validation-schema inventory, record instance schema planning, conversion packet schema planning, evidence/provenance schema planning, conflict ledger schema planning, and test fixture schema planning to convert a deliberately small pilot set and learn from it. Minimum pilot conversion readiness does not require final math, runtime schemas, canon promotion, sourcebook prose, live-play behavior, or training data.

Large-scale corpus conversion readiness is a later and stricter threshold. It requires pilot evidence, benchmark evidence, validator coverage, error taxonomy, cross-record reference discipline, conflict-ledger discipline, rejected-donor routing, D-series non-authority safeguards, and owner-approved escalation handling at corpus scale. Large-scale corpus conversion readiness must not be claimed merely because minimum pilot conversion readiness exists.

## 9. V1 runtime-readiness checklist

V1 runtime-readiness scope is downstream of schema/math planning. It depends on audited schema inventories, validated conversion outputs, benchmarked math proposals, accepted runtime-prep schemas, runtime/Gate B owner review, and explicit non-leakage controls for hidden state.

This checklist does not design implementation. It does not define runtime schema, backend schema, database schema, entity/component/event schema, command lifecycle, context packet contract, save-state shape, API contract, persistence contract, orchestration command, UI state, hidden-information runtime state, or live-play behavior. Runtime/Gate B remains a later owner-controlled readiness gate.

## 10. Doctrine/mechanics owner map

Proposed future owner files are named cautiously as planning targets, not existing files and not approved doctrine:

- Proposed SM01 validation/schema inventory owner: validation schemas, record instance schemas, cross-record references, conversion packet schemas, evidence/provenance schemas, canon-review schemas, conflict ledger schemas, pilot conversion output schemas, mechanics I/O schemas, runtime-prep schemas, and test fixture schemas.
- Proposed SM02 pilot conversion packet owner: minimum pilot conversion readiness, pilot fixtures, evidence review, and conversion-output learning.
- Proposed SM03 math benchmark owner: balance benchmarks, difficulty bands, scaling hypotheses, and rejection of donor math defaults before final math.
- Proposed SM04 mechanics boundary owner: action economy, timing/cadence, cost commitment, partial outcome states, damage, injury, conditions, resources, recovery/recharge, progression, and thresholds as unresolved workstreams only.
- Proposed SM05 runtime-prep handoff owner: runtime/Gate B dependencies and runtime-prep schemas without runtime schema implementation.
- Lawful fallback owner: if no proposed owner can accept a gap, route to `pending_schema`, quarantine, deferred gap ledger, or Astra Doctrine Council review.

## 11. Risk register

The risk register for this workstream includes:

- donor math leakage: donor formulas become Astra defaults without audit.
- donor statblock leakage: donor statblock shapes become record instance schemas or final mechanics.
- donor economy leakage: donor prices, currencies, rewards, requisition rules, or crafting economies become Astra defaults.
- donor class/progression leakage: donor class, level, feat, route, or advancement structures become defaults.
- donor dice-system leakage: donor resolution dice or probability curves become final resolution dice.
- donor cosmology leakage: donor cosmology defaults or source-local metaphysics become Astra law.
- RHBF overfitting: repeated handling of recurrent bad form becomes hidden doctrine instead of evidence routing.
- C-family schema drift: C01-C14 drift from C00 or invent unauthorized fields.
- Batch B procedure mistaken for final mechanics: B01-B11 operational doctrine is misread as final mechanics or math.
- Batch C records mistaken for runtime schemas: conversion-stage/canon-review records are misread as runtime schemas.
- D-series authority leakage: D00-D19 draft source packs are treated as current doctrine or implementation authority.
- premature canon/sourcebook/live-play/runtime promotion: planning language is misread as canon readiness, sourcebook readiness, live-play readiness, or runtime readiness.
- hidden-state leakage: protected truth enters player-facing records, sourcebook prose, training data, runtime state, or public canon.
- unvalidated math: exact math is designed before audit, validation, benchmark, and pilot-conversion evidence exist.
- brittle tests: tests fail merely because later valid planning files are added.
- insufficient benchmarks: mechanics proposals lack comparison targets, stress cases, or conversion evidence.
- megafile risk: future planning tries to solve every schema, math, runtime, and canon problem in one oversized file.
- underdesigned mechanics: excessive refusal language leaves later owners without an accountable sequencing path.

## 12. Recommended sequencing

The next PR after SM00 should be a validation/schema inventory PR, not final mechanics. Recommended sequence:

1. SM01 validation/schema inventory PR: enumerate validation schemas, record instance schemas, cross-record references, conversion packet schemas, evidence/provenance schemas, canon-review schemas, conflict ledger schemas, pilot conversion output schemas, mechanics I/O schemas, runtime-prep schemas, and test fixture schemas.
2. SM02 pilot conversion readiness PR: define minimum pilot conversion readiness fixtures and evidence capture without canon/sourcebook/runtime promotion.
3. SM03 benchmark and audit PR: establish benchmark questions and audit criteria before exact math.
4. SM04 mechanics gap decomposition PRs: split resolution, economy, damage, resources, progression, scaling, exploration, vehicles, companions, tables, maps, hidden state, and balance into separate owner scopes.
5. SM05 runtime/Gate B handoff planning PR: only after schema inventory, pilot evidence, and benchmark evidence exist.

Final math must wait until audit, validation, benchmark, and pilot-conversion evidence exist because those inputs reveal actual Astra record pressure, donor-leakage risks, unresolved owner gaps, and the minimum viable data needed for lawful mechanics decisions.

## 13. Proposed first follow-up PRs

Proposed follow-up PRs, all cautious and non-final:

- Add SM01 validation/schema inventory and readiness controls.
- Add SM02 minimum pilot conversion readiness plan.
- Add SM03 benchmark/audit question ledger for math and mechanics.
- Add SM04 deferred mechanics decomposition plan by owner area.
- Add SM05 runtime-prep dependency map for runtime/Gate B without runtime schema design.

None of these proposed PRs should promote C00, C01-C14, Batch A, Batch B, D-series packs, final mechanics, runtime schemas, canon/sourcebook prose, live-play behavior, or training corpora.

## 14. Testing strategy

Focused SM00 tests should verify that SM00 exists, required sections are present, C00 and C01-C14 are named, `pending_schema` is present, B11 is named, the Batch C capstone is named, Conversion IR is named, lawful outcome taxonomy is named, and runtime/Gate B is named.

Tests should assert that Batch C readiness is not canon readiness, runtime readiness, sourcebook readiness, final mechanics readiness, live-play readiness, or training readiness. Tests should assert that D-series source packs are draft source material only and not authority.

Tests should assert schema gap inventory terms, math/mechanics gap inventory terms, minimum pilot conversion readiness, large-scale corpus conversion readiness, v1 runtime-readiness dependencies without implementation design, required risk-register terms, deferred gaps routed to named future owners or lawful fallbacks, and hard refusals.

Tests must be future-safe. They should not fail merely because later valid planning files are added. Registry tests should assert C00-C14 records are not promoted by this PR rather than asserting no future planning or control files can exist.

## 15. Deferred gap ledger

Deferred gaps are routed as follows:

- validation schemas -> proposed SM01 validation/schema inventory owner; fallback `pending_schema` or deferred gap ledger.
- record instance schemas -> proposed SM01 validation/schema inventory owner; fallback quarantine and owner assignment.
- cross-record references -> proposed SM01 validation/schema inventory owner; fallback conflict ledger and Astra Doctrine Council review.
- conversion packet schemas -> proposed SM01 and SM02 owners; fallback pilot deferral.
- evidence/provenance schemas -> proposed SM01 owner; fallback evidence quarantine.
- canon-review schemas -> proposed SM01 owner plus later canon governance owner; fallback no canon promotion.
- conflict ledger schemas -> proposed SM01 owner; fallback deferred conflict ledger.
- pilot conversion output schemas -> proposed SM02 owner; fallback no large-scale corpus conversion readiness.
- mechanics I/O schemas -> proposed SM01 and SM04 owners; fallback no final mechanics.
- runtime-prep schemas -> proposed SM05 owner; fallback no runtime/Gate B readiness.
- test fixture schemas -> proposed SM01 owner; fallback no tested_minimum claims.
- resolution math, difficulty bands, action economy, timing/cadence, cost commitment, partial outcome states, damage, injury, conditions, resources, recovery/recharge, progression, thresholds, character scaling, opposition scaling, hazards, gear/relic scaling, abilities/techniques, crafting/salvage/requisition, faction/social pressure, travel/exploration, vehicle/platform mechanics, companion/summon control, table/oracle probability, map/spatial abstraction, hidden-state handling, and balance benchmarks -> proposed SM03 owner and proposed SM04 owner; fallback no final mechanics or exact math.
- backend/database contracts, entity/component/event schema, command lifecycle, context packet contract, and save-state shape -> proposed SM05 runtime-prep handoff owner only after prerequisites; fallback no runtime schema.

## 16. Non-goals and hard refusals

SM00 explicitly refuses:

- final mechanics;
- exact math;
- final resolution dice;
- runtime schema and runtime schemas;
- backend schema;
- database schema;
- backend/database contracts;
- entity/component/event schema;
- command lifecycle;
- context packet contract;
- save-state shape;
- canon promotion;
- accepted lexicon promotion;
- sourcebook prose;
- live-play/GM behavior;
- training/evaluation corpus creation;
- canon/sourcebook/live-play/training promotion;
- donor math defaults;
- donor statblock defaults;
- donor economy defaults;
- donor class/progression defaults;
- donor dice-system defaults;
- donor cosmology defaults;
- donor proper noun import;
- donor defaults of any kind;
- RHBF hidden law;
- D-series authority promotion.

These refusals apply even if a donor source, D-series source pack, Batch B procedure, C-family record, or test fixture appears to imply a ready-made answer.

## 17. Acceptance criteria

SM00 is acceptable only if:

- it remains a planning/readiness/scope file only;
- it does not draft final mechanics, exact math, final resolution dice, runtime schemas, backend/database contracts, canon, sourcebook prose, live-play behavior, or training content;
- it preserves Batch A doctrine without rewrite;
- it preserves Batch B through B11 as operational doctrine, not final mechanics;
- it preserves C00 and C01-C14 as Batch C conversion-stage/canon-review schema doctrine;
- it treats the Batch C capstone as readiness with deferred gaps only;
- it preserves D00-D19 source packs as draft source material only and not authority;
- it includes C01-C14 family names and `pending_schema`;
- it separates minimum pilot conversion readiness from large-scale corpus conversion readiness;
- it separates v1 runtime readiness from schema/math planning;
- it routes deferred schema/math/mechanics/runtime gaps to named proposed future owners or lawful fallbacks;
- it recommends that the next PR be validation/schema inventory, not final mechanics;
- it refuses final mechanics, runtime schemas, backend/database contracts, canon/sourcebook/live-play/training, donor defaults, RHBF hidden law, and D-series authority promotion;
- it does not change C01-C14 file contents, does not add C15, and does not promote registry records for C00-C14.
