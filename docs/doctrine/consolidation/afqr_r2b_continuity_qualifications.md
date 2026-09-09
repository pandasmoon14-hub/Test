# AFQR R2B-CONTINUITY Qualifications

**Artifact ID:** `AFQR-R2B-CONTINUITY-QUALIFICATIONS-001`
**Artifact version:** `0.1.0`
**Package:** `R2B-CONTINUITY`
**Workstream:** `PR2-R2B-N`
**Layer:** doctrine qualification
**Authority:** bounded R2B-CONTINUITY doctrine qualification upon accepted merge
**Starting baseline:** `d70e9a5c1ab67c8e2bb6a2b8331c73269cc3b286`

## 1. Purpose and authority boundary

This artifact resolves exactly the five bounded CONTINUITY seams established by R2A-11:

1. stable authoritative timeline-identity qualification;
2. world-valid versus record/commitment-time qualification;
3. branch canonicality/class/ancestry governance;
4. correction/compensation/retcon/supersession governance;
5. branch-safe projection/disclosure qualification.

It does not create a CONTINUITY semantic super-owner. Each module composes existing AFQR owners while preserving their separate semantics.

This artifact does not define or authorize runtime implementation, production schemas, persistence representation, replay infrastructure, package loading, ruleset/package/override version applicability, universal clocks, project canon promotion, donor conversion, source eligibility, a universal branch taxonomy, a universal correction service, a universal timeline root, time-travel metaphysics, or live-play/GM behavior.

The accepted CROSS-PHASE version-identity/effectivity seam is consumed where necessary and is not redefined here. Session-closure snapshot doctrine is not created here; R2A-11 left the closure envelope with AFQR-01 and representation downstream.

## 2. Component-owner preservation

### Timeline identity
`R2B-CONTINUITY-MOD-TIMELINE-IDENTITY-QUALIFICATION`

- AFQR-04 retains logical time, causal ordering, simultaneity, scheduling, and deterministic resolution grouping.
- AFQR-08 retains identity, continuity, copying, transformation, reinstantiation, fusion, fission, and contextual equivalence.

### Bitemporal qualification
`R2B-CONTINUITY-MOD-BITEMPORAL-QUALIFICATION`

- AFQR-01 retains commitment, recovery, replay, receipts, and committed-mutation boundaries.
- AFQR-04 retains logical-time and causal-order semantics.
- AFQR-06 retains claims, evidence submission, admissibility, conflict, arbitration, typed claim results, and hidden-evidence boundaries.
- AFQR-10 retains authoritative world truth, observer-relative truth, epistemic state, knowledge, belief, memory, uncertainty, provenance, revision, and visibility-safe projection doctrine.

### Branch canonicality and ancestry
`R2B-CONTINUITY-MOD-BRANCH-CANONICALITY-ANCESTRY`

- AFQR-01 retains commitment/replay boundaries.
- AFQR-04 retains ordering/causality.
- AFQR-08 retains identity/continuity.
- AFQR-09 retains governed relations, dependency lifecycle, revocation, inheritance, termination, migration, orphaning, and cascading consequences.

### Correction governance
`R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE`

- AFQR-01 retains commitment, replay, recovery, and receipts.
- AFQR-04 retains temporal placement and causal order.
- AFQR-09 retains dependency consequences, migration, revocation, orphaning, and cascades.

### Branch-safe projection
`R2B-CONTINUITY-MOD-BRANCH-SAFE-PROJECTION`

- AFQR-01 retains committed-history boundaries.
- AFQR-08 retains branch/timeline identity and continuity distinctions.
- AFQR-10 retains truth/epistemic/projection semantics.
- AFQR-20 retains sensing, acquisition, detection, recognition, concealment, tracking, and sensing observation candidates.

## 3. Module A — Stable authoritative timeline identity

### CONT-TL-001 — Timeline identity is a continuity-qualified referent
Where an authoritative history must remain referable across recording, recovery, replay, migration, restoration, or representation changes, that history must have a stable identity basis sufficient to distinguish it from other continuity-bearing histories.

### CONT-TL-002 — Timeline identity is not storage identity
A timeline identity is not automatically identical to a save-file identifier, database key, journal identifier, event-store stream, snapshot, replay log, process identifier, server identifier, campaign-folder path, or repository branch.

### CONT-TL-003 — Timeline identity is not canonicality
Identifying a timeline does not determine whether it is canonical, primary, archived, authoritative for a scope, preferred, current, player-visible, or eligible for promotion.

### CONT-TL-004 — Copying does not silently preserve identity
Copying, snapshotting, cloning, exporting, importing, replaying, or restoring a representation does not by itself prove that the result is the same timeline. AFQR-08 retains that identity determination.

### CONT-TL-005 — Identity stability does not require frozen state
A timeline may accumulate lawful transitions while remaining the same timeline. State similarity likewise does not prove timeline identity.

### CONT-TL-006 — No universal root timeline is required
Astra does not require every campaign, world, simulation, or source-local system to descend from one universal root timeline.

### CONT-TL-007 — Timeline identity does not create authority
A stable timeline identifier does not confer ownership, control, agency, canon, branch priority, truth, persistence authority, or correction authority.

## 4. Module B — World-valid versus record/commitment time

### CONT-BT-001 — The temporal roles are distinct
Where both matter, Astra distinguishes world-valid time (when a fact/state/claim/effect applies in the governed world-history basis) from record/commitment time (when an authority-bearing record, claim, transition, evidence item, revision, or correction entered its governed record history).

### CONT-BT-002 — Neither time substitutes for the other
A later record time does not imply later world-valid time. An earlier world-valid time does not imply the record already existed, was known, was admissible, or was committed then. Where only one dimension matters, no decorative second timestamp is required.

### CONT-BT-003 — AFQR-04 retains time semantics
CONTINUITY does not define timestamp formats, clocks, calendars, tick rates, turn structures, simultaneity policy, or causal ordering rules.

### CONT-BT-004 — Commitment history is not retroactively erased
A record introduced later may be world-valid earlier, but the system may not pretend it was already present in the earlier commitment history.

### CONT-BT-005 — World-valid time does not prove truth or knowledge
World-valid placement does not establish authoritative world truth, observer knowledge, belief, memory, evidence admissibility, or sensing success.

### CONT-BT-006 — Record time does not prove evidence admissibility
A claim/evidence item may have a submission history without becoming admissible or true. AFQR-06 retains admissibility/arbitration.

### CONT-BT-007 — Revision remains attributable
Where a later correction, retcon, supersession, evidentiary ruling, or epistemic revision affects an earlier world-valid interval, both the affected valid-time basis and later record/commitment point must remain distinguishable.

### CONT-BT-008 — CROSS-PHASE version effectivity is not duplicated
Ruleset, package, override, and schema version applicability/effective intervals remain governed by R2B-CROSS-PHASE.

## 5. Module C — Branch canonicality, class, and ancestry

### CONT-BR-001 — Branching is an explicit continuity distinction
Ordinary replay, read-only inspection, cached state, serialization, preview, backup, or snapshotting does not automatically create a branch.

### CONT-BR-002 — Branch classification is explicit and scoped
Where branch class affects behavior or authority, the class must be explicit for the relevant governing scope. Astra does not mandate one universal class enumeration.

### CONT-BR-003 — Canonicality is qualified, not inherent
Canonicality is explicit for a declared scope. It is not automatically conferred by being newest, longest, loaded, writable, on a default server, named `main`/`primary`/`canon`, parent, child, or replayable.

### CONT-BR-004 — Ancestry and canonicality are independent
A branch may descend from another without inheriting canonicality, authority, visibility, or current applicability. Canonicality likewise does not prove ancestry.

### CONT-BR-005 — Fork provenance remains attributable
Where a branch has an ancestor, the continuity basis must distinguish the relevant ancestor, descendant, and divergence/fork relation without requiring one universal schema.

### CONT-BR-006 — Promotion is an explicit authority-bearing change
Persisting, loading, viewing, replaying, archiving, or naming a branch does not promote it. Promotion/canonicality change must be explicit and attributable to lawful authority.

### CONT-BR-007 — Archive status is not deletion or invalidity
Archiving does not erase committed history, ancestry, historical receipts, or prior existence, and does not automatically grant another branch canonicality.

### CONT-BR-008 — Branch creation does not rewrite the ancestor
Creating a descendant or alternate history does not silently rewrite the ancestor's committed history.

### CONT-BR-009 — Branch identity is not actor identity
Branching does not automatically answer whether contained actors/entities retain, copy, lose, fuse, or change identity.

### CONT-BR-010 — No universal alternate-world metaphysics is adopted
Branch ancestry is a continuity relation, not a declaration that every branch is a physically coexisting universe, metaphysical timeline, dream, simulation, save slot, or accessible world.

## 6. Module D — Correction, compensation, supersession, and retcon governance

### CONT-COR-001 — Untyped historical mutation is prohibited
A request described only as `fix`, `correct`, `rollback`, `undo`, `repair`, or `retcon` is not sufficient authority to mutate historical meaning.

### CONT-COR-002 — Metadata/representation repair is nonsemantic only
A metadata/representation repair may correct recording, encoding, linkage, format, or provenance without changing the underlying authoritative domain outcome. If substantive meaning changes, it is not merely metadata repair.

### CONT-COR-003 — Compensation adds a new consequence
Compensation responds to a prior authoritative outcome through a new, distinguishable committed consequence; it does not claim the prior outcome never occurred.

### CONT-COR-004 — Supersession changes scoped authority without erasure
Supersession may replace an older statement/decision/state/qualification for a declared scope or applicability basis while preserving the older record historically.

### CONT-COR-005 — Retcon/canon revision changes authoritative historical interpretation
A retcon/canon-revision class applies where lawful authority deliberately changes what a governed scope treats as authoritative about its own past. The original historical audit remains distinguishable. This classification grants no project-canon promotion authority.

### CONT-COR-006 — Alternate-history creation diverges instead of rewriting
Where the intent is to preserve the original history while creating a different historical course, the operation composes with Module C and does not make either history canonical by itself.

### CONT-COR-007 — Correction authority is external to the journal
A correction log, migration tool, replay engine, branch tool, admin UI, or storage layer cannot authorize a correction merely because it can represent/apply one.

### CONT-COR-008 — Committed audit is preserved
Correction-family operations may change current authoritative interpretation or add new consequences but must not silently erase the fact that an earlier committed record existed.

### CONT-COR-009 — Temporal placement remains AFQR-04
A correction can be recorded later while affecting an earlier world-valid interval; AFQR-04 still owns time/causal semantics.

### CONT-COR-010 — Dependency consequences remain AFQR-09
Correction, supersession, retcon, or branch creation may cause dependency/revocation/migration/orphaning/cascade consequences; those remain AFQR-09 concerns.

### CONT-COR-011 — Randomness identity remains R2B-CORE
If an authorized correction requires new resolution of a randomness-bearing outcome, the accepted R2B-CORE qualification governs preservation of the original and separate randomness provenance.

### CONT-COR-012 — Version applicability remains R2B-CROSS-PHASE
Ruleset/package/override/schema version identity, pinning, applicability, and effective intervals remain CROSS-PHASE concerns.

## 7. Module E — Branch-safe projection and disclosure

### CONT-PROJ-001 — Projection is scoped to an identified continuity basis
A projection that depends on timeline/branch state must identify or inherit a lawful continuity basis sufficient to prevent accidental mixing of incompatible histories.

### CONT-PROJ-002 — Projection never owns truth
AFQR-10 retains authoritative world truth, observer-relative truth, epistemic state, knowledge, belief, memory, uncertainty, and visibility-safe projection semantics.

### CONT-PROJ-003 — Projection never owns sensing
AFQR-20 retains signals, sensing, acquisition, detection, recognition, concealment, tracking, and sensing observation candidates. Existence on a branch does not imply sensing, and sensing does not imply knowledge/truth.

### CONT-PROJ-004 — Cross-branch facts do not leak by default
Information true, known, sensed, recorded, or visible on one branch is not automatically eligible for disclosure on another merely because branches share ancestry, actors, names, assets, or storage.

### CONT-PROJ-005 — Ancestry does not imply inherited knowledge
A descendant may inherit state through a lawful fork without implying every observer inherits every piece of knowledge from the ancestor.

### CONT-PROJ-006 — Historical viewpoints must not be silently collapsed
Where bitemporal/corrected history matters, an `as then` view must not silently become only present revised knowledge, nor an `as now` view only historical pre-revision knowledge.

### CONT-PROJ-007 — Privileged views require independent authority
A GM, administrator, debugger, moderator, auditor, system process, or model does not receive cross-branch/hidden-state access merely from its label.

### CONT-PROJ-008 — Projection cannot mutate the branch
Rendering, summarizing, querying, inspecting, exporting, or model-facing projection does not commit state, change canonicality, create ancestry, or correct history.

### CONT-PROJ-009 — Labels are not disclosure policy
Labels such as `main`, `alternate`, `GM`, `player`, `archive`, `preview`, `canon`, `debug`, or `secret` do not themselves establish disclosure rights.

## 8. Explicit exclusions proved by R2A

### No CONTINUITY version module
`R2B-CONTINUITY-MOD-RULESET-PACKAGE-OVERRIDE-VERSIONS` is not adopted. R2A-11 routed that seam exactly once to R2B-CROSS-PHASE.

### No session-closure snapshot module
`R2B-CONTINUITY-MOD-SESSION-CLOSURE-SNAPSHOT` is not adopted. AFQR-01 retains the closure envelope; representation remains downstream.

## 9. Corpus-scale pressure checks

| Pressure | Required CONTINUITY outcome |
| --- | --- |
| ordinary save/load | storage identity does not silently become timeline/branch identity |
| crash recovery | recovery can preserve a timeline without defining identity from file equality |
| duplicated save | copying does not automatically prove same timeline or create a canonical branch |
| what-if simulation | persistence does not confer canonicality |
| multiplayer divergence | branch identity, ancestry, authority, and disclosure remain explicit rather than process-topology-derived |
| campaign fork | ancestry can be recorded without automatic canonicality |
| branch promotion | requires explicit authority-bearing qualification |
| archived campaign | archive does not erase history or ancestry |
| errata correction | version applicability remains CROSS-PHASE |
| compensation | new consequence preserves prior committed audit |
| retcon | revised authoritative interpretation remains distinguishable from original record history |
| alternate-history scenario | divergence does not overwrite the original or universalize multiverse metaphysics |
| imported campaign | import success does not decide timeline identity/canonicality |
| cloned world for testing | copy does not inherit authority by byte equality |
| hidden GM information | branch selection does not grant disclosure |
| delayed discovery | occurrence time may differ from record/knowledge time |
| later evidence about earlier event | AFQR-06 retains admissibility |
| source with no branch concept | no decorative branch taxonomy is imposed |
| source with many branch classes | source-local classes may remain source-local |
| time-travel donor subsystem | metaphysics remain source-local or escalate |
| replay under old rules | CROSS-PHASE historical pinning remains authoritative |
| randomized correction | R2B-CORE randomness preservation remains authoritative |

## 10. Escalation rule

A case leaves R2B-CONTINUITY if resolving it requires new domain-state semantics, new identity/personhood doctrine, a universal branch class list, a universal timeline topology, time-travel/alternate-world metaphysics, version applicability, evidence admissibility, epistemic truth policy, sensing procedures, canon authority/content promotion, domain-specific correction authorization, runtime persistence/replay/schema design, or live-play behavior.

## 11. Machine-reviewable contract

```json
{
  "artifact_id": "AFQR-R2B-CONTINUITY-QUALIFICATIONS-001",
  "artifact_version": "0.1.0",
  "package_id": "R2B-CONTINUITY",
  "workstream_id": "PR2-R2B-N",
  "starting_baseline": "d70e9a5c1ab67c8e2bb6a2b8331c73269cc3b286",
  "authority_effect": "bounded_continuity_doctrine_resolution_only",
  "created_semantic_owners": [],
  "required_modules": [
    {
      "module_id": "R2B-CONTINUITY-MOD-TIMELINE-IDENTITY-QUALIFICATION",
      "component_owners": ["AFQR-04", "AFQR-08"],
      "qualification": {
        "timeline_identity_must_be_stably_attributable_when_material": true,
        "timeline_identity_equals_storage_identity": false,
        "timeline_identity_confers_canonicality": false,
        "copying_proves_same_timeline": false,
        "universal_root_timeline_required": false,
        "persistence_representation_selected": false
      }
    },
    {
      "module_id": "R2B-CONTINUITY-MOD-BITEMPORAL-QUALIFICATION",
      "component_owners": ["AFQR-01", "AFQR-04", "AFQR-06", "AFQR-10"],
      "qualification": {
        "world_valid_and_record_commitment_time_are_distinct_when_both_material": true,
        "decorative_second_time_dimension_required": false,
        "later_record_time_implies_later_world_valid_time": false,
        "world_valid_time_proves_truth_or_knowledge": false,
        "record_time_proves_evidence_admissibility": false,
        "revision_preserves_record_time_attribution": true,
        "time_semantics_remain_afqr_04": true,
        "evidence_admissibility_remains_afqr_06": true,
        "truth_epistemic_semantics_remain_afqr_10": true
      }
    },
    {
      "module_id": "R2B-CONTINUITY-MOD-BRANCH-CANONICALITY-ANCESTRY",
      "component_owners": ["AFQR-01", "AFQR-04", "AFQR-08", "AFQR-09"],
      "qualification": {
        "branching_requires_explicit_continuity_distinction_when_material": true,
        "snapshot_or_replay_automatically_creates_branch": false,
        "universal_branch_class_enumeration_required": false,
        "canonicality_is_explicit_and_scoped": true,
        "ancestry_confers_canonicality": false,
        "canonicality_proves_ancestry": false,
        "fork_provenance_remains_attributable": true,
        "promotion_requires_explicit_authority_bearing_change": true,
        "archive_erases_history": false,
        "universal_alternate_world_metaphysics_adopted": false
      }
    },
    {
      "module_id": "R2B-CONTINUITY-MOD-CORRECTION-GOVERNANCE",
      "component_owners": ["AFQR-01", "AFQR-04", "AFQR-09"],
      "qualification": {
        "untyped_historical_mutation_allowed": false,
        "metadata_repair_may_change_domain_semantics": false,
        "compensation_erases_prior_outcome": false,
        "supersession_erases_historical_record": false,
        "retcon_revision_preserves_original_audit_distinction": true,
        "alternate_history_creation_rewrites_original": false,
        "journal_or_storage_confers_correction_authority": false,
        "committed_audit_is_preserved": true,
        "dependency_consequences_remain_afqr_09": true,
        "randomness_identity_remains_r2b_core": true,
        "version_applicability_remains_r2b_cross_phase": true
      }
    },
    {
      "module_id": "R2B-CONTINUITY-MOD-BRANCH-SAFE-PROJECTION",
      "component_owners": ["AFQR-01", "AFQR-08", "AFQR-10", "AFQR-20"],
      "qualification": {
        "projection_requires_lawful_continuity_basis_when_branch_sensitive": true,
        "continuity_basis_grants_visibility": false,
        "projection_owns_truth": false,
        "projection_owns_sensing": false,
        "cross_branch_information_leaks_by_default": false,
        "ancestry_implies_inherited_observer_knowledge": false,
        "historical_viewpoints_must_not_be_silently_collapsed": true,
        "role_label_grants_privileged_cross_branch_access": false,
        "projection_mutates_branch": false
      }
    }
  ],
  "explicitly_not_adopted_modules": [
    "R2B-CONTINUITY-MOD-RULESET-PACKAGE-OVERRIDE-VERSIONS",
    "R2B-CONTINUITY-MOD-SESSION-CLOSURE-SNAPSHOT"
  ],
  "cross_phase_nonduplication": {
    "version_identity_effectivity_may_be_redefined_by_continuity": false,
    "cross_phase_artifact": "AFQR-R2B-CROSS-PHASE-VERSION-EFFECTIVITY-001"
  },
  "core_nonduplication": {
    "randomness_identity_may_be_redefined_by_continuity": false,
    "core_artifact": "AFQR-R2B-CORE-QUALIFICATIONS-001"
  },
  "implementation_nonrequirements": [
    "timeline_database",
    "branch_registry",
    "event_store",
    "snapshot_format",
    "save_file_format",
    "replay_engine",
    "correction_service",
    "retcon_service",
    "projection_api",
    "query_language",
    "universal_timestamp_schema",
    "universal_branch_enum",
    "universal_timeline_root",
    "universal_multiverse_model"
  ],
  "prohibited_inferences": [
    "storage_identity_is_timeline_identity",
    "timeline_identity_confers_canonicality",
    "copying_proves_identity_continuity",
    "record_time_equals_world_valid_time",
    "world_valid_time_proves_truth",
    "record_time_proves_admissibility",
    "branch_ancestry_confers_canonicality",
    "load_or_write_status_confers_branch_authority",
    "archive_erases_historical_existence",
    "correction_tool_confers_correction_authority",
    "retcon_may_erase_original_audit",
    "branch_selection_confers_knowledge",
    "cross_branch_information_is_visible_by_default",
    "continuity_may_duplicate_version_effectivity",
    "continuity_may_duplicate_rng_identity",
    "continuity_is_a_semantic_super_owner",
    "r2b_continuity_authorizes_runtime_or_schema_implementation"
  ],
  "downstream_handoffs": {
    "PR2-R2C": ["independent_formal_r2_completion_review"],
    "later_implementation": [
      "timeline_identity_representation",
      "branch_relation_representation",
      "bitemporal_record_representation",
      "correction_record_representation",
      "projection_query_representation"
    ]
  }
}
```
