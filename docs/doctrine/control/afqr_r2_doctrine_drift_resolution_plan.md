# AFQR R2 Doctrine-Drift Resolution Control Plan

**Layer:** `0_control`
**Authority:** bounded R2 sequencing and routing only
**Overall R2 status:** `complete`

## Invariants

Accepted R1 and R1E decisions outrank research. R2 changes doctrine only through an authorized modular R2B decision after R2A. Storage, commitment, replay, branching, and handoff transfer no substantive ownership. SUB-001–SUB-005 remain unimplemented. R3 execution, R4–R6, RT-002G, temporary evidence deletion, and post-R2 workstreams remain separately authorization-gated.

## R2-0 — research assimilation

**Status:** `complete`

Owns source registration, normalized claim extraction, routing, owner-pressure identification, and work-package planning. It does not own substantive doctrine adoption, repository-wide drift findings, conformance decisions, schema decisions, or implementation. Its durable inputs and outputs are the intake packet, source manifest, claim ledger, assimilation report, this plan, and file manifest.

## R2A — authority-surface and drift inventory

**Status:** `complete`

R2A consumes the R2-0 ledger and inventories repository-wide authority surfaces. It distinguishes current authority from historical text, narrow fixtures from general doctrine, doctrine drift from implementation absence, and real owner conflict from mere keyword overlap. Each finding receives a lawful outcome: governed by an existing owner, normalized mapping, historical/source-local pressure, implementation/schema presupposition, no material authority relation, owner adjudication, doctrine escalation, or a later authorized gate. No-action and existing-owner outcomes are lawful; lexical matches do not manufacture work. It must not adopt doctrine or implement anything.

PR #342 was closed without merge. Its artifacts, occurrence representation, history, and completion claims are not accepted repository authority and are not inputs to this reconstruction. No compact reconstruction or isolated local commit is repository authority.

R2A was reconstructed as twelve bounded pull requests. R2A-1 defined the inventory contract, executable discovery vectors, and partition manifest; R2A-2 and R2A-3 recorded semantic surfaces; R2A-4 through R2A-7 dispositioned candidates under deterministic precedence; R2A-8 verified receipts, parity, and reciprocity; R2A-9 and R2A-10 split the 31 claim assessments; R2A-11 assessed the eleven unresolved questions and synthesized package/module status without beginning R2B; and R2A-12 independently reviewed completion and updated the gate.

R2A-12 verified R2A completion without adopting doctrine, modifying runtime or production schemas, inventing a coordination owner, or beginning R2B. Historical inventory-contract and reconstruction snapshots remain preserved as historical evidence rather than being rewritten for successor currency.

R2A proved exactly three R2B packages necessary:

- `R2B-CORE`;
- `R2B-CROSS-PHASE`;
- `R2B-CONTINUITY`.

`R2B-AGENCY` and `R2B-WORLD` were independently classified `not_required` on the available evidence.

## R2B — modular doctrine resolution

**Status:** `complete`

PR2-CTRL merged through PR #375.

### R2B-CORE

R2B-CORE completed and merged through PR #376.

Certified branch head:

`8a88068b802a9819328e09691e7c1def778a778d`

Merge commit:

`307ab295a8590d60a310d4b8d872971620fa74eb`

It resolved exactly:

- preview persistence / promotion qualification;
- correction-specific randomness identity preservation.

It created no CORE, preview, persistence, replay, RNG, correction, or branch super-owner.

### R2B-CROSS-PHASE

R2B-CROSS-PHASE completed and merged through PR #377.

Certified branch head:

`eededa8e0b845fa14ba303f4d34369cefdd2f861`

Merge commit:

`d70e9a5c1ab67c8e2bb6a2b8331c73269cc3b286`

It resolved exactly the ruleset/content-package/campaign-override/related-schema version identity, applicability, pinning, and effective-interval seam without creating a cross-phase or version super-owner.

### R2B-CONTINUITY

R2B-CONTINUITY completed and merged through PR #378.

Certified branch head:

`d94f5e8f40b1b74d6bdb23e2e419e5cb5d6fb34f`

Merge commit:

`5cae79bcdd86c93c6fe77b6492a8a087a83900b0`

It resolved exactly five bounded coordination seams:

- stable authoritative timeline identity qualification;
- world-valid versus record/commitment-time qualification;
- branch canonicality/class/ancestry governance;
- correction/compensation/retcon/supersession governance;
- branch-safe projection/disclosure qualification.

The authorized modules are exactly:

- `R2B-CONTINUITY-MOD-TIMELINE-IDENTITY-QUALIFICATION`;
- `R2B-CONTINUITY-MOD-BITEMPORAL-QUALIFICATION`;
- `R2B-CONTINUITY-MOD-BRANCH-CANONICALITY-ANCESTRY`;
- `R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE`;
- `R2B-CONTINUITY-MOD-BRANCH-SAFE-PROJECTION`.

CONTINUITY coordination remains a nonowner. AFQR component ownership remains separate.

CONTINUITY does not duplicate:

- CROSS-PHASE version identity/applicability/pinning/effectivity;
- R2B-CORE correction-specific randomness identity;
- session-closure snapshot doctrine.

It does not invent a universal branch taxonomy, universal timeline topology, time-travel/alternate-world metaphysics, correction service, persistence representation, runtime implementation, or production schema.

No authorized R2B doctrine gap remains.

## R2C — formal completion review

**Status:** `complete`

Authorization reference:

`owner_directive_2026-09-08_r2c_activation`

R2C independently reviewed the merged baseline:

`5cae79bcdd86c93c6fe77b6492a8a087a83900b0`

Formal review artifact:

`docs/doctrine/reviews/afqr_r2c_formal_completion_review.md`

Review result:

`PASS`

Publication lifecycle state:

`validated`

Validated branch head:

`949575f42f8b4ba1e01963013b35376d49433faf`

Validation evidence:

- focused R2C, transition-control, and predecessor validation: `63 passed`;
- full repository suite: `8922 passed, 10 skipped, 2 xfailed, 1 warning`;
- `git diff --check`: clean;
- validated working tree: clean.

No R2C pull request or merge commit exists at this validation state.

R2C verified that:

- every material R2A finding has a lawful outcome or explicit downstream deferral;
- the three required R2B packages are merged;
- R2B-AGENCY and R2B-WORLD remain correctly not required;
- no unnecessary CONTINUITY version or session-closure module was created;
- accepted R1/R1E authority remains intact;
- no semantic super-owner was created;
- no runtime, production-schema, persistence, replay, source, canon, conversion, or live-play implementation was smuggled into R2 doctrine;
- historical evidence remains traceable;
- later-phase obligations remain explicitly preserved;
- no blocking R2 doctrine exception remains.

R2C therefore closes R2.

### Exact R3 conformance target

R2C fixes the R3 target to every and only R2A-6 candidate record in:

`docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0001.yaml`

and:

`docs/doctrine/reviews/r2a/dispositions_runtime_schema/dispositions_0002.yaml`

whose `pressure_route` equals `r3_conformance`.

The R2A-6 index proves that this selector contains exactly `34` candidates.

Frozen shard content SHA-256 values:

- `7ddb4d6e7e7342c44a9e6e0e574309b1e084743fd469ef4eec3944b668b0cd05`;
- `e4b1293559231990c0468908c74648ba34c355373857d1b824fd375a648e2569`.

R3 must compare those 34 frozen candidate identities against the accepted R1/R1E plus completed R2 doctrine baseline. It must not silently absorb records routed `r4_substrate`, `later_gate`, or `none`.

This target definition does not authorize R3 execution or remediation.

## Preserved downstream routes

R2 closure does not falsely close later obligations.

Examples remain:

- expected-version / stale-command pressure → R5 retrofit;
- reservation record identity/expiry/storage representation → R4 substrate/schema work under existing AFQR-07/AFQR-01 semantics;
- offline/deferred progression → later implementation/frontier work;
- actor-local/transformed-time representation → later implementation/frontier work;
- alternate-world/cross-reality/time-travel semantics → later frontier doctrine if separately authorized;
- SUB-001–SUB-005 → accepted deferred substrates, still unimplemented.

## Corpus and escalation

R2A and R2B were required to test actual-play, split-party, inserted chronology, correction, replay, disclosure, organized-play, stale-command, recovery, migration, heterogeneous source, and runtime pressure without donor-law promotion.

Outliers that require new semantics remain escalation candidates. Consensus, source frequency, implementation convenience, or one familiar donor family cannot manufacture doctrine authority.

## Post-R2 boundary

R2 closure does not authorize the larger Myravant build-out.

The owner-selected first post-R2 workstream is `PR2-ID` Myravant identity migration, followed by the separately gated source/originality/information-barrier/native-content program. Runtime scalability, compositional assurance, capability assurance, canon, implementation, and live play remain separately gated.

## Gate posture

`R1=complete`; `R2=complete`; `R2-0=complete`; `R2A=complete`; `R2B=complete`; `R2C=complete`.

`R3` has an exact conformance target but remains `ready_pending_authorization` rather than active.

`R4–R6=blocked`; `RT-002G=unauthorized`; `temporary_evidence_deletion=unauthorized`.

No post-R2 identity, source, originality, native-content, runtime-scalability, canon, conversion, implementation, or live-play work is authorized by R2C.
