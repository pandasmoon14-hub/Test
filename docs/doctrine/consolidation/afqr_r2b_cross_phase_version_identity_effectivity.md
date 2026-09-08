# AFQR R2B-CROSS-PHASE Version Identity and Effectivity Qualifications

**Artifact ID:** `AFQR-R2B-CROSS-PHASE-VERSION-EFFECTIVITY-001`
**Artifact version:** `0.1.0`
**Package:** `R2B-CROSS-PHASE`
**Workstream:** `PR2-R2B-X`
**Module:** `R2B-CROSS-PHASE-MOD-VERSION-IDENTITY-EFFECTIVITY`
**Layer:** doctrine qualification
**Authority:** bounded R2B-CROSS-PHASE doctrine qualification upon accepted merge
**Starting baseline:** `307ab295a8590d60a310d4b8d872971620fa74eb`

## 1. Purpose and authority boundary

This artifact resolves exactly the single CROSS-PHASE doctrine seam established
by R2A:

> version identity, applicability, pinning, and effective-interval governance
> for rulesets, content packages, campaign overrides, and related
> schema/version identities.

It does not create a CROSS-PHASE semantic super-owner.

It coordinates existing component-owner boundaries so historical execution,
current applicability, replay, migration, and later runtime work can identify
which versioned basis applies without silently transferring semantics to
storage, package loading, replay machinery, or coordination infrastructure.

No other R2B seam is resolved here.

This artifact does not define canon, content eligibility, conversion authority,
runtime truth, procedure semantics, command semantics, commitment semantics,
logical-time semantics, dependency semantics, branch semantics, correction or
retcon taxonomy, world-valid versus record-time doctrine, package-manager
behavior, schema migration implementation, persistence/replay implementation,
a universal version-numbering scheme, or a universal override-precedence
system.

## 2. Component-owner preservation

The R2A-authorized component-owner references remain separate.

AFQR-01 retains transition commitment, recovery/replay boundaries, transition
receipts, and committed-history provenance.

AFQR-02 retains command identity, attempt identity, retry identity, suspension,
escalation, and durable command progress.

AFQR-04 retains logical time, causal ordering, scheduling, and effective-time
relationships.

AFQR-09 retains dependency lifecycle, revocation consequences, migration
consequences, and orphaning consequences.

AFQR-19 retains applicable procedure-resolution semantics.

A consuming record may reference version applicability without transferring
those component semantics to CROSS-PHASE.

This artifact creates no cross-phase semantic owner, version super-owner,
package owner, ruleset owner, override owner, schema owner, replay owner,
migration owner, or canon owner.

## 3. Versioned dimensions remain distinct

R2B-CROSS-PHASE recognizes four minimum versioned dimensions because R2A proved
that they must be distinguishable across historical and current applicability.

### 3.1 Ruleset version identity

A ruleset version identity identifies the particular ruleset lineage or
revision relevant to a governed scope.

It does not by itself establish canon, procedure meaning, applicability,
priority, compatibility, or migration authority.

### 3.2 Content-package version identity

A content-package version identity identifies the particular package lineage or
revision relevant to a governed scope.

Package identity or installation does not imply canon status, distribution
eligibility, source legitimacy, applicability, dependency satisfaction, or
authority over domain semantics.

### 3.3 Campaign-override version identity

A campaign-override version identity identifies a particular override set or
revision.

The word `override` does not itself confer authority or priority.

An override becomes applicable only through a lawful governing context. Its
identity alone does not establish that it may override anything.

### 3.4 Related schema/version identity

A related schema/version identity identifies the representation or schema
revision required to interpret a versioned record or interface where such
identity is relevant.

Schema identity is representational. It does not acquire gameplay semantics,
canon, command identity, commitment authority, dependency ownership, procedure
ownership, or migration authority merely by being newer.

## 4. Core CROSS-PHASE qualifications

### CROSS-PHASE-001 — Identity and revision must be attributable

Where a ruleset, content package, campaign override, or related schema can exist
in more than one revision, a consuming context that depends on that distinction
must be able to attribute the selected subject and revision.

A display label, filename, load order, install timestamp, repository branch,
or mutable alias is not automatically sufficient evidence of a stable version
identity.

This rule does not require semantic versioning, hashes, UUIDs, numeric versions,
or any particular identifier format.

### CROSS-PHASE-002 — Version dimensions do not collapse

Ruleset, content-package, campaign-override, and related schema/version
identities remain distinguishable dimensions.

No implementation may infer that package version equals ruleset version,
ruleset version equals schema version, override version equals package version,
or one shared counter makes the dimensions semantically identical.

A source-local system may intentionally bind several dimensions together, but
that binding remains explicit and source-local unless separately adopted.

### CROSS-PHASE-003 — Identity does not confer authority

Knowing which version something is does not establish that the version is
applicable, canonical, authorized, compatible, preferred, newest, distributable,
or valid for a particular campaign or historical execution.

Version identity answers identity, not authority.

### CROSS-PHASE-004 — Applicability must be explicit

A version becomes applicable only when the governing context identifies it as
applicable for the relevant scope.

Mere existence, installation, discoverability, recency, load order, storage
location, or the label `latest` does not make a version applicable.

If current applicability cannot be resolved from the governing context,
CROSS-PHASE does not invent a winner. The ambiguity remains explicit or is
escalated to the appropriate owner or later gate.

### CROSS-PHASE-005 — `latest` is not a historical basis

A mutable alias such as `latest`, `current`, `recommended`, or an unconstrained
version range may be useful before resolution.

Once a versioned input actually participates in an authority-bearing execution,
the concrete revision used by that execution must be attributable for later
audit, recovery, or exact replay.

The historical basis is the resolved revision actually used, not whatever the
alias resolves to later.

### CROSS-PHASE-006 — Historical pinning preserves the actual basis

A committed or otherwise authority-bearing historical execution that depends on
versioned inputs is pinned, for audit purposes, to the version identities that
actually governed that execution.

Pinning means the historical basis remains attributable.

It does not mean the artifact can never be superseded, remains currently
applicable, is canonical forever, must remain loaded forever, or requires one
storage mechanism.

### CROSS-PHASE-007 — Replay, recovery, and technical retry do not refresh versions

Replay, recovery, duplicate delivery, or technical retry does not silently
replace the historical or already-resolved version basis with a newer or
currently installed version.

AFQR-01 retains replay/recovery and commitment semantics. AFQR-02 retains retry
and command/attempt identity.

CROSS-PHASE only requires that version applicability not drift merely because
technical execution occurs later.

### CROSS-PHASE-008 — Missing historical versions do not authorize substitution

If an exact historical version basis is unavailable, incompatible, revoked, or
otherwise unusable, a consumer may not silently substitute another version and
still claim exact historical replay or recovery equivalence.

Lawful outcomes may include declaring exact replay unavailable, using a
separately authorized migration, producing a new distinguishable execution
under a new applicable basis, preserving the historical record while routing
the dependency problem, or escalation.

The correct outcome depends on existing owners and later implementation
authority. CROSS-PHASE does not choose a migration algorithm or replacement
policy.

### CROSS-PHASE-009 — Effective intervals are explicit applicability facts

Where applicability changes over time, the applicability relation must be
bounded by an effective interval or other AFQR-04-governed temporal
qualification sufficient to distinguish when the version applies.

The interval may be open, closed, point-like, bounded, or source-local as
permitted by the owning time doctrine.

CROSS-PHASE does not impose a universal timestamp format, calendar, tick system,
or duration model.

### CROSS-PHASE-010 — Effective intervals identify their time basis

An effective interval must not silently conflate unlike temporal meanings.

Where more than one time basis exists, the applicability statement must be
interpretable against the applicable AFQR-04-owned time basis.

This module does not establish the later CONTINUITY qualification between
world-valid time and record/commitment time.

It only prohibits CROSS-PHASE applicability from manufacturing an untyped,
ownerless notion of time.

### CROSS-PHASE-011 — Overlap does not create implicit precedence

Two or more versions may lawfully be effective at overlapping times when their
scopes, subjects, or governing contexts differ.

Overlap is not itself an error.

If multiple candidate versions are simultaneously eligible for the same
governed use and the governing context does not distinguish them, load order,
lexical order, recency, storage order, or implementation accident must not
invent precedence.

The ambiguity remains explicit until lawfully resolved.

### CROSS-PHASE-012 — Override identity does not confer override authority

A campaign override must remain distinguishable from the ruleset or package it
affects.

Its identity, presence, or load order does not establish authority to override,
scope of override, priority over another override, priority over a base rule,
permanence, or canon status.

This supports campaign-local, organized-play, modded, scenario-local, and other
override structures without adopting one universal override hierarchy.

### CROSS-PHASE-013 — Package identity does not confer canon or eligibility

A content package can be installed but inapplicable, applicable but
noncanonical, historical but no longer current, source-local, quarantined, or
unavailable while still referenced by history.

CROSS-PHASE records none of those states merely from package identity.

Canon, rights, provenance, distribution eligibility, and content ownership
remain separate concerns.

### CROSS-PHASE-014 — Schema version does not reinterpret domain semantics

A schema or representation revision may affect how information is encoded,
decoded, transported, or migrated.

It may not silently redefine the domain meaning of represented rules, state,
commands, dependencies, procedures, or history.

A schema migration that changes substantive meaning requires the applicable
semantic owner or later authorized doctrine; the word `migration` is not an
authority grant.

### CROSS-PHASE-015 — Supersession does not rewrite historical applicability

A new version may become applicable after an older version.

That change does not retroactively make the newer version the basis of earlier
executions.

Likewise, revocation or deactivation of a version does not erase the historical
fact that it was previously applicable where that fact was lawfully recorded.

### CROSS-PHASE-016 — Dependency consequences remain AFQR-09

A version may depend on another package, rule family, schema, feature, or
registered relation.

CROSS-PHASE may preserve which version references participated in the basis.

It does not decide whether a dependency is satisfiable, what revocation means,
whether a dependent becomes orphaned, how migration propagates, or whether a
dependency may be substituted.

Those remain AFQR-09 concerns where applicable.

### CROSS-PHASE-017 — Procedure semantics remain AFQR-19

If ruleset or package versions select different procedures, CROSS-PHASE can
identify which versioned procedure basis was applicable.

It does not define the procedure, outcome grammar, contest semantics, action
economy, dice system, deterministic resolver, or conflict rules.

Those remain with the applicable procedure-resolution owner.

### CROSS-PHASE-018 — Command identity remains AFQR-02

A command or attempt may carry or reference a resolved version basis.

Changing that basis may be material to command/attempt identity under AFQR-02,
but CROSS-PHASE does not decide whether a new command or attempt is required.

It only prohibits silent re-binding disguised as unchanged applicability.

### CROSS-PHASE-019 — Commitment remains AFQR-01

A committed transition may record or reference the version basis used.

The existence of that basis does not make CROSS-PHASE the owner of commitment
or of the committed domain.

Conversely, commitment does not make the journal, replay engine, package
loader, or version store the owner of version applicability.

### CROSS-PHASE-020 — No universal implementation or version scheme is mandated

This qualification does not require semantic versioning, monotonically
increasing integers, Git hashes, UUIDs, content hashes, package lockfiles, one
global version counter, one universal ruleset object, a package manager, a
dependency solver, a database, a registry service, an event store, a migration
engine, a schema language, runtime version fields, or a universal override
stack.

Implementations may choose lawful representations later.

## 5. Corpus-scale pressure checks

| Pressure | Required CROSS-PHASE result |
| --- | --- |
| campaign starts under rules revision A, later updates to B | earlier executions remain attributable to A; later applicability may lawfully select B |
| hotfix published during an unresolved command | no silent basis refresh; AFQR-02 determines command/attempt consequences |
| content package installed but disabled for one campaign | installation does not imply applicability |
| package is historical and no longer installed | historical identity remains; exact replay cannot silently substitute another package |
| organized-play season changes rules | applicability may use scoped effective intervals without universalizing the season model |
| campaign-local house rule changes | override identity remains distinct and does not gain authority by presence |
| two overrides overlap | no implicit precedence from load order or recency |
| package version and schema version advance independently | dimensions remain distinguishable |
| schema migration rewrites representation | representation may change without silently changing domain semantics |
| version range resolves differently months later | historical execution retains the concrete revision actually used |
| mutable `latest` alias used by tooling | alias is not an exact historical pin |
| source-local system binds rules and content to one release number | explicit source-local binding is retained without becoming universal law |
| dependency is revoked | AFQR-09 owns consequences; CROSS-PHASE preserves attributable version basis |
| procedure implementation changes between versions | AFQR-19 owns procedure semantics; applicable version remains explicit |
| replay uses archived executable/package | archive location confers no semantic ownership |
| multiple campaigns use different valid revisions concurrently | coexistence is lawful when scope distinguishes applicability |
| current applicability cannot choose among candidates | ambiguity remains explicit; infrastructure does not invent a winner |

These are pressure classes, not mandatory runtime fixtures.

## 6. Handoff boundaries

### 6.1 R2B-CONTINUITY

Later separately authorized CONTINUITY work may consume CROSS-PHASE outputs for
timeline identity, branch classification and ancestry, correction and
supersession governance, branch-safe projection, and world-valid versus
record/commitment-time qualification.

CONTINUITY must not recreate a second ruleset/package/override version owner or
a second effective-interval system.

The version-identity/effectivity seam is resolved exactly once here.

### 6.2 Runtime and persistence implementation

Later implementation may need representations for version references, resolved
applicability bases, package registries, archives, dependency metadata, lock
records, schema revisions, and migration receipts.

This artifact authorizes none of those implementations.

### 6.3 Canon, conversion, and source governance

Canon, conversion, provenance, source eligibility, originality, rights,
distribution, and Myravant content production remain outside this package.

Version identity may be consumed by those later systems, but it grants them no
authority and gains no authority from them.

## 7. Escalation rule

A case that cannot be resolved without defining canon selection, branch
canonicality, correction taxonomy, world-valid versus record-time doctrine,
dependency substitution, procedure semantics, command retry semantics,
commitment behavior, schema migration semantics, runtime package-loading policy,
universal override precedence, or new domain semantics must leave
R2B-CROSS-PHASE.

Do not broaden CROSS-PHASE merely because a versioned construct crosses several
phases.

## 8. Machine-reviewable contract

```json
{
  "artifact_id": "AFQR-R2B-CROSS-PHASE-VERSION-EFFECTIVITY-001",
  "artifact_version": "0.1.0",
  "package_id": "R2B-CROSS-PHASE",
  "workstream_id": "PR2-R2B-X",
  "module_id": "R2B-CROSS-PHASE-MOD-VERSION-IDENTITY-EFFECTIVITY",
  "authority_effect": "bounded_cross_phase_version_identity_applicability_pinning_and_effectivity_qualification",
  "component_owners": {
    "AFQR-01": [
      "transition_commitment",
      "recovery_replay",
      "transition_receipts",
      "committed_history_provenance"
    ],
    "AFQR-02": [
      "command_identity",
      "attempt_identity",
      "retry_identity",
      "suspension_escalation",
      "durable_command_progress"
    ],
    "AFQR-04": [
      "logical_time",
      "causal_order",
      "scheduling",
      "effective_time_relationships"
    ],
    "AFQR-09": [
      "dependency_lifecycle",
      "revocation_consequences",
      "migration_consequences",
      "orphaning_consequences"
    ],
    "AFQR-19": [
      "applicable_procedure_resolution_semantics"
    ]
  },
  "created_semantic_owners": [],
  "version_dimensions": [
    "ruleset_version_identity",
    "content_package_version_identity",
    "campaign_override_version_identity",
    "related_schema_version_identity"
  ],
  "qualifications": {
    "version_dimensions_remain_distinct": true,
    "version_identity_confers_applicability": false,
    "version_identity_confers_canon": false,
    "latest_alias_is_historical_pin": false,
    "current_applicability_must_be_explicit": true,
    "historical_execution_basis_must_be_attributable": true,
    "technical_retry_may_refresh_version_basis": false,
    "replay_or_recovery_may_substitute_current_version": false,
    "missing_historical_version_allows_silent_substitution": false,
    "effective_interval_requires_declared_time_basis": true,
    "effective_interval_time_semantics_owner": "AFQR-04",
    "overlap_creates_implicit_precedence": false,
    "override_identity_confers_override_authority": false,
    "package_identity_confers_distribution_eligibility": false,
    "schema_version_confers_domain_semantics": false,
    "supersession_rewrites_historical_applicability": false,
    "dependency_consequences_remain_afqr_09": true,
    "procedure_semantics_remain_afqr_19": true,
    "command_identity_remains_afqr_02": true,
    "commitment_remains_afqr_01": true,
    "continuity_may_duplicate_version_effectivity_seam": false
  },
  "allowed_pre_resolution_indirection": [
    "mutable_alias",
    "version_range",
    "source_local_selector"
  ],
  "historical_resolution_requirement": "the concrete revision actually used by an authority-bearing execution must remain attributable",
  "implementation_nonrequirements": [
    "semantic_versioning",
    "numeric_versions",
    "git_hashes",
    "uuid_versions",
    "content_hash_versions",
    "global_version_counter",
    "package_manager",
    "dependency_solver",
    "database",
    "registry_service",
    "event_store",
    "migration_engine",
    "schema_language",
    "runtime_version_field",
    "universal_override_stack"
  ],
  "handoffs": {
    "R2B-CONTINUITY": [
      "timeline_identity",
      "world_valid_vs_record_time",
      "branch_canonicality_class_ancestry",
      "correction_supersession_governance",
      "branch_safe_projection"
    ],
    "later_implementation": [
      "version_reference_representation",
      "package_registry",
      "archive",
      "dependency_metadata",
      "lock_record",
      "schema_revision_representation",
      "migration_receipt"
    ]
  },
  "prohibited_inferences": [
    "latest_wins",
    "installed_means_applicable",
    "package_identity_means_canon",
    "override_name_confers_override_authority",
    "load_order_creates_semantic_precedence",
    "schema_version_owns_domain_semantics",
    "replay_may_refresh_to_current_versions",
    "missing_historical_version_may_be_silently_substituted",
    "one_version_counter_makes_dimensions_semantically_identical",
    "cross_phase_is_a_semantic_super_owner",
    "continuity_may_redefine_version_effectivity",
    "r2b_cross_phase_authorizes_runtime_or_schema_implementation"
  ]
}
```
