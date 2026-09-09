# Myravant Identity Migration Contract

**Artifact ID:** `PR2-ID-MIGRATION-CONTRACT-001`
**Workstream:** `PR2-ID`
**Layer:** `0_control`
**Status:** `active`
**Starting baseline:** `843fc89f3769a8e6323fa7b683d3805a9edfc142`
**Authorization reference:** `owner_directive_2026-09-08_pr2_id_activation`
**Authority effect:** identity and brand migration only
**Current tranche:** `PR2-ID-T2A`

## 1. Purpose

This contract governs the controlled migration of the project's current-facing identity from **Astra Ascension** to **Myravant** after formal R2 closure.

It exists to prevent a branding migration from rewriting provenance, altering gameplay doctrine, changing semantic ownership, breaking software compatibility, or erasing the historical identity under which accepted work was produced.

Myravant is the owner-selected current and future umbrella/platform/ecosystem identity. Astra Ascension remains the historical predecessor identity wherever history, provenance, compatibility, or evidence requires it.

This contract does not authorize source-governance work, originality governance, donor/source processing, native-content production, runtime-scalability implementation, R3 execution, canon promotion, conversion work, live-play/GM behavior, or model training.

## 2. Identity relation

The migration uses an explicit successor relationship:

`Astra Ascension (historical predecessor) -> Myravant (current/future identity)`

This is not a claim that every historical Astra-labeled artifact was always Myravant. Historical records must remain truthful about the identity that existed when they were created.

The migration changes current-facing identity where lawful. It does not retroactively rewrite project history.

## 3. Migration dispositions

Every Astra-identity occurrence encountered by PR2-ID must receive one of these dispositions:

- `migrate_current` — mutable current-facing identity that should now say Myravant;
- `migrate_with_historical_qualifier` — current text should name Myravant while explicitly preserving Astra Ascension as the historical predecessor;
- `retain_historical` — the Astra identity is part of a truthful historical record, frozen review, accepted decision, immutable evidence, citation, or provenance chain;
- `retain_compatibility` — the Astra identifier is still required for software, data, import, package, schema, CLI, environment, storage, or integration compatibility;
- `alias_then_migrate` — the surface may migrate only after a compatibility alias or transition path is established and tested;
- `escalate` — the occurrence cannot be changed safely under identity-only authority and requires a separately bounded decision.

No unclassified global replacement is lawful.

## 4. Surface classes

### 4.1 Mutable current-facing branding

These surfaces may migrate directly when the edit changes identity only:

- repository title and descriptive prose;
- current contributor and coding-agent navigation;
- compatibility notes whose purpose is current repository identity;
- future-facing product/platform wording;
- new project-native content branding;
- current operational prose that is not a historical snapshot or evidence record.

Initial tranche targets are limited to current-facing navigation and identity-control material. This contract does not authorize a repository-wide prose rewrite.

### 4.2 Current doctrine and control prose

Current doctrine may contain Astra as the name of the system whose semantics it governs. Such prose is potentially migratable, but only through an audited semantic-preserving tranche.

The migration must not alter:

- doctrine meaning;
- owner boundaries;
- accepted terminology that is semantically distinct from project branding;
- artifact IDs;
- quoted historical decisions;
- frozen baselines;
- source/evidence identifiers;
- hashes;
- historical branch, PR, or commit references.

A doctrine file is not automatically mutable merely because it is current authority.

### 4.3 Compatibility-bearing software identifiers

The following are not cosmetic branding and must not be renamed without a dedicated compatibility tranche:

- Python distribution names such as `astra-runtime`;
- Python import/package namespaces such as `astra_runtime`;
- module paths under `src/`;
- CLI command names;
- environment-variable names;
- serialized type names;
- schema identifiers or `$id` values;
- persisted field names;
- test fixtures whose literal spelling is part of a contract;
- external integration names;
- generated artifact paths consumed by tooling.

A later PR2-ID compatibility tranche must inventory references, define alias/deprecation behavior, prove installation/import behavior, and preserve historical data readability before any such identifier changes.

Identity migration does not create authority to redesign the runtime or schema model.

### 4.4 Immutable, historical, and provenance-bearing surfaces

These retain Astra identity unless a separate correction process proves the historical record itself is wrong:

- Git history and commit metadata;
- merged PR titles, branch names, and historical URLs;
- accepted historical decisions describing events that occurred under Astra Ascension;
- frozen review artifacts and frozen evidence snapshots;
- artifact IDs and stable evidence IDs;
- hashes, blob identities, source IDs, conversion IDs, and provenance keys;
- quoted historical text;
- paths whose exact spelling is part of frozen evidence or accepted provenance;
- archived or explicitly historical documents;
- external-source provenance and research lineage.

Historical truth outranks cosmetic consistency.

## 5. Product-family naming boundary

The owner-selected umbrella identity is **Myravant**.

Reserved family names may include:

- `Myravant Core`;
- `Myravant Runtime`;
- `Myravant Worlds`;
- `Myravant Creator`;
- optional title/subtitle forms such as `Myravant: Ascension` where separately useful.

Reservation does not automatically assign a family name to an existing module. A specific surface adopts a family name only when its role is clear and the change does not imply new architecture.

## 6. First bounded migration tranche

The first PR2-ID tranche may change only:

1. this migration contract;
2. post-R2 transition control/manifest bookkeeping needed to activate PR2-ID;
3. the current decisions log entry recording authorization;
4. `README.md` current-facing identity prose;
5. `AGENTS.md` current-facing identity/navigation prose;
6. `CLAUDE.md` current-facing identity/navigation prose;
7. tests dedicated to enforcing this migration boundary.

The first tranche must not rename `astra-runtime`, `astra_runtime`, `src/astra_runtime/`, schemas, artifact IDs, historical review files, frozen evidence, or repository history.

## 7. Required current-facing wording

After the first tranche:

- the repository's current umbrella identity is Myravant;
- Astra Ascension is described as the historical predecessor identity where relevant;
- Aether Forge remains subordinate historical/developer tooling rather than the project identity;
- authority continues to reside in owning doctrine/control artifacts rather than README or agent guidance;
- references to current runtime package paths may retain `astra_runtime` explicitly as compatibility-bearing legacy identifiers pending a later audited compatibility tranche.

## 8. Anti-drift rules

PR2-ID must not:

- perform an indiscriminate `Astra` -> `Myravant` replacement;
- claim historical Astra artifacts were originally authored as Myravant;
- rewrite immutable provenance for cosmetic consistency;
- rename compatibility-bearing software identifiers without an alias and regression plan;
- use the rename to alter gameplay doctrine or semantic ownership;
- treat Myravant branding as canon promotion;
- treat migration completion as source-governance authorization;
- erase donor/source provenance;
- make old serialized or stored data unreadable merely to obtain naming consistency;
- manufacture new platform components solely because family names are reserved.

## 9. Validation requirements

Every PR2-ID tranche must prove, as applicable:

- changed files stay within the authorized tranche;
- prohibited historical/evidence surfaces are unchanged;
- current-facing identity assertions are consistent;
- compatibility-bearing Astra identifiers remain unchanged unless that tranche explicitly owns their migration;
- `git diff --check` is clean;
- relevant focused tests pass;
- the full repository suite passes before final PR2-ID completion, or any environment-limited deviation is explicitly recorded and separately accepted.

## 9A. Identity-surface disposition control

PR2-ID-T2A adds the machine-readable disposition ledger:

`docs/doctrine/control/myravant_identity_surface_disposition_ledger.yaml`

The ledger is subordinate to this migration contract. It classifies discovered
identity surfaces; it does not amend gameplay doctrine, promote canon, redefine
semantic ownership, or authorize a later migration tranche.

The inventory basis for T2A contains 2,495 identity-bearing occurrence lines
across 454 tracked files, with 233 tracked paths whose filenames contain
`Astra`.

At this scale, directory membership and lexical spelling are insufficient
grounds for migration. T2A therefore uses semantic-role classification,
precedence rules, and explicit dispositions.

In particular:

- historical decisions and frozen reviews retain truthful Astra identity;
- imported D-series source packs retain their predecessor-era identity and
  provenance;
- `astra-runtime`, `astra_runtime`, and `src/astra_runtime/` remain
  compatibility-bearing identifiers;
- the roadmap and registry require separate occurrence-level adjudication;
- verified current AFQR consolidation doctrine and the active
  conversion/runtime firewall are identified only as candidates for a later
  semantic-neutral doctrine tranche;
- unmatched doctrine and test surfaces escalate rather than receiving an
  inferred rename.

T2A performs classification only. It does not activate `PR2-ID-T2B`.

## 10. Completion rule

PR2-ID is complete only when every material current-facing identity surface discovered by the migration inventory has a lawful disposition and all authorized `migrate_current` / `migrate_with_historical_qualifier` changes are complete.

Completion does not require historical Astra references to disappear. A successful migration should leave many truthful Astra references in history, provenance, frozen evidence, compatibility aliases, and accepted historical records.

Any remaining compatibility-bearing identifiers must have an explicit retained/alias/deferred disposition rather than being silently ignored.

## 11. Downstream boundary

PR2-ID completion may unblock the owner-selected post-R2 sequence, but it does not by itself authorize `PR2-SRC`, `PR2-ORG`, `PR2-IR`, corpus-scale source work, native-content production, runtime scalability, R3 execution, canon consolidation, or live-play work.
