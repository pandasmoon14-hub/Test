# Conversion–Runtime Separation and Runtime Origin Firewall Doctrine

```yaml
file_id: CTRL-CONVERSION-RUNTIME-ORIGIN-FIREWALL-001
status: active_control_doctrine
layer: 0_control
phase: cross_phase
owner: Astra Doctrine Council
runtime_authority: none
canon_promotion_authority: none
conversion_execution_authority: none
```

## 1. Purpose

This doctrine establishes a hard architectural boundary between:

1. source acquisition and extraction;
2. conversion and normalization;
3. canon review and promotion;
4. runtime packaging and execution.

The extraction and conversion environment exists to produce reviewable evidence and candidate structures. It is not part of the Astra runtime, is not a runtime dependency, and must not be visible to runtime services, runtime retrieval, the live-play model adapter, or players.

## 2. Central law

> Extraction and conversion end before runtime begins. No extraction artifact, conversion artifact, donor identifier, source reference, mapping record, provenance field, or source-derived namespace may cross into runtime. Canon promotion creates a new Astra-native artifact with a new identity and a sanitized payload. Pre-canon lineage is retained only in a segregated offline governance ledger.

This law applies regardless of whether extraction and runtime code temporarily coexist in the same repository.

## 3. Mandatory phase separation

```text
source and extraction environment
→ conversion and normalization environment
→ doctrine, conflict, lexicon, originality, and rights review
→ explicit canon-promotion decision
→ sanitized Astra-native canonical export
→ runtime package
→ campaign installation and runtime state
```

The flow is one-way.

Runtime may not query, import, reconstruct, or traverse backward into any earlier phase.

## 4. Identity-breaking promotion boundary

A canon-promotion operation must create a new Astra-native identity.

The promoted artifact must not reuse or deterministically derive its runtime identity from:

- donor title, author, publisher, product code, ISBN, URL, or external namespace;
- source filename, archive name, directory path, checksum, page identifier, or line identifier;
- extraction packet, page-truth, OCR, lane, queue, or repair identifier;
- conversion intake, construct, mapping, quarantine, escalation, or review identifier;
- a stable hash or token that permits runtime-to-source correlation.

The runtime identity begins at canon promotion. Pre-canon identity remains outside runtime.

## 5. Runtime-origin blindness

Runtime code and runtime-accessible data must behave as though promoted material is native Astra material.

Runtime-origin blindness applies to:

- runtime modules and package dependencies;
- canonical content packages installed into runtime;
- database rows and event records;
- state snapshots and replay data;
- generators and validators;
- retrieval indexes and embeddings;
- context packets and model prompts;
- model-visible tools and metadata;
- logs available to live-play services;
- player-visible exports and diagnostics.

Runtime-origin blindness does not mean destroying governance evidence. It means the evidence is outside the runtime trust boundary.

## 6. Runtime-forbidden data

The following are prohibited in runtime-accessible schemas and payloads:

### 6.1 Source identity

- donor or source titles;
- author, publisher, imprint, contributor, or product identifiers;
- source URLs, store URLs, repository URLs, or external namespace labels;
- donor-family labels when they reveal external lineage.

### 6.2 Extraction identity

- filenames, paths, archive names, page numbers, line numbers, or page hashes;
- OCR state, extraction lane, extraction engine, model name, DPI, repair lane, or parsing notes;
- page-truth, content-unit, routing, defect, repair, queue, or handoff packet identifiers;
- raw extracted text or source-format fragments.

### 6.3 Conversion identity

- conversion intake IDs;
- construct inventory IDs;
- donor-to-Astra mapping records;
- lawful-outcome rationale;
- normalization notes;
- rejected-import, quarantine, or escalation records;
- canon-candidate deliberation;
- conversion confidence or source-comparison notes.

### 6.4 Correlatable metadata

- stable tokens, digests, hashes, UUID derivations, slugs, or names that encode or permit correlation to source or conversion records;
- source-derived comments, debug strings, labels, tags, or exception text;
- runtime-accessible sidecars that can reconstruct pre-canon lineage.

### 6.5 Unapproved source expression

- copied source passages;
- source-format stat blocks;
- source-specific boilerplate;
- distinctive attribution-like headings or formatting;
- content that has not passed originality, rights, doctrine, conflict, and canon review.

## 7. Runtime-allowed provenance

Runtime may retain provenance only for the artifact’s life inside Astra, including:

- Astra canonical artifact identity and version;
- Astra rules family, module, or namespace;
- campaign installation and migration history;
- generator and validator versions;
- command, event, state-transition, replay, and audit records;
- runtime-created derivative lineage;
- campaign-local or module-local identity created after promotion.

Runtime provenance must begin at the Astra-native promotion or generation boundary.

A runtime field named `source`, `origin`, `provenance`, or similar must be qualified as Astra-native runtime provenance and must not carry pre-canon lineage.

## 8. Offline lineage ledger

The project must retain an offline, access-controlled lineage ledger for:

- source evidence;
- extraction history;
- conversion decisions;
- mapping and normalization rationale;
- conflict and lexicon review;
- originality and rights review;
- canon-promotion approval;
- supersession, rejection, quarantine, and withdrawal.

The ledger must be:

- outside runtime packages;
- outside runtime databases and retrieval indexes;
- inaccessible to runtime services and model context;
- inaccessible to player-facing exports;
- separately permissioned;
- auditable and reproducible;
- retained according to governance and rights-review policy.

Runtime artifacts may be associated with ledger records only through a private governance mapping unavailable to runtime. The runtime-facing artifact must not contain the reverse lookup key.

## 9. Code and dependency firewall

The runtime package must not import, call, or depend on:

- extraction orchestrators;
- OCR or page-repair pipelines;
- conversion intake processors;
- donor-family classifiers;
- mapping or normalization engines;
- quarantine and escalation tooling;
- canon-candidate review tooling;
- offline provenance stores.

The extraction and conversion environment may read runtime-independent doctrine and schema definitions where explicitly allowed. Runtime may not read extraction or conversion outputs.

Shared libraries must be limited to genuinely neutral primitives. A shared library may not carry source lineage, conversion semantics, or donor-specific vocabulary into runtime.

## 10. Packaging firewall

A runtime build must be produced from a sanitized canonical export, not from conversion work directories.

Runtime build inputs must be allowlisted.

Runtime build outputs must exclude:

- extraction directories;
- conversion directories;
- review workspaces;
- source PDFs or source-derived Markdown;
- handoff packets;
- provenance ledgers;
- mapping files;
- quarantine and escalation records;
- conversion logs and caches;
- source-correlated test fixtures.

A build that includes any prohibited artifact must fail closed.

## 11. Canon-promotion scrub contract

Before a candidate may become runtime-eligible, the canon-promotion process must verify:

1. Astra doctrine compatibility;
2. conflict resolution;
3. lexicon compliance;
4. source-local or universal scope classification;
5. originality and rights-review disposition;
6. removal of source and conversion identifiers;
7. removal of source-derived formatting and comments;
8. creation of a new Astra-native identity;
9. validation against Astra-native schemas;
10. runtime-origin firewall certification.

The promotion output must be a new artifact, not a conversion record with fields hidden or ignored.

## 12. Source-local constructs

A source-local construct may survive canon review only as an Astra-governed local construct.

At runtime it must use:

- an Astra-issued identity;
- an Astra-issued namespace;
- Astra-native schema and terminology;
- explicit runtime interfaces;
- no donor name or donor-derived namespace;
- no runtime-accessible lineage to the external source.

The offline governance ledger may retain that the construct originated as source-local donor pressure. Runtime may not.

## 13. Model and retrieval firewall

The live-play model adapter must not receive:

- source names;
- extraction or conversion records;
- mapping notes;
- source excerpts;
- donor-family labels;
- offline provenance identifiers;
- canon-promotion deliberation.

Runtime retrieval must index only sanitized Astra-native canonical material and committed campaign state.

A model response that claims or implies external origin must be rejected unless the user is operating an explicitly separate authoring or governance workflow outside runtime.

## 14. Logging, diagnostics, and errors

Runtime logs and exceptions must not expose pre-canon lineage.

Runtime diagnostics may refer to:

- Astra artifact ID;
- Astra schema version;
- Astra module;
- runtime event or validation record.

They must not refer to the source, extraction packet, conversion record, or private lineage mapping.

Authoring and governance logs may contain such data only inside the offline environment.

## 15. Repository coexistence does not weaken separation

During development, extraction, conversion, doctrine, and runtime code may coexist in one repository. Co-location does not create authority or dependency.

The repository must preserve separate package boundaries, build manifests, tests, and deployment outputs.

Long-term physical separation into different repositories or archives is permitted and may be preferred, but this doctrine applies before and after such separation.

## 16. AFQR and phase handoffs

This doctrine reinforces:

- AFQR-01 authority and event-boundary separation;
- AFQR-05 registered interface and bridge discipline;
- AFQR-08 identity discontinuity and purpose-scoped continuity;
- AFQR-10 provenance, truth, epistemic, and disclosure boundaries;
- AFQR-15 institutional and rights-review handoffs;
- AFQR-19 model-output and effect-authority separation;
- AFQR-20 hidden-information and retrieval safety;
- conversion/canon/runtime/live-play phase separation.

It does not replace the detailed rules of those decisions.

## 17. Acceptance criteria

The firewall is not implementation-complete until all of the following hold:

- [ ] `astra_runtime` has no imports from extraction or conversion packages.
- [ ] Runtime build manifests use allowlisted sanitized inputs only.
- [ ] Runtime schemas reject pre-canon origin fields.
- [ ] Runtime content packages contain no source or conversion metadata.
- [ ] Runtime IDs are not derived from source or conversion IDs.
- [ ] Runtime retrieval indexes exclude extraction and conversion stores.
- [ ] Model context builders exclude offline lineage.
- [ ] Runtime logs and errors expose only Astra-native identifiers.
- [ ] A private offline lineage ledger remains available for governance audit.
- [ ] Promotion tests prove new identity creation and origin-field removal.
- [ ] Source-local constructs use Astra-issued runtime namespaces.
- [ ] Packaging tests fail closed when prohibited files are present.
- [ ] Cross-boundary side-channel tests prevent stable correlation to source records.

## 18. Immediate repository consequences

Until conformance work is completed:

- current extraction and conversion tooling remains authoring-only;
- current runtime modules remain prohibited from reading extraction or conversion outputs;
- RT-series work must not add donor, extraction, conversion, or source provenance fields;
- AFQR consolidation must record this doctrine as a cross-cutting control law;
- future runtime re-entry requires a repository dependency and packaging audit.

## 19. Non-goals

This doctrine does not:

- authorize use of any source;
- determine whether particular material is lawful to use;
- replace originality, licensing, attribution, or rights review;
- perform canon promotion;
- implement extraction or conversion;
- implement runtime behavior;
- erase or destroy governance evidence;
- permit laundering unapproved material by deleting attribution.

Material that cannot be lawfully and coherently promoted as Astra-native canon must remain rejected, quarantined, or confined to the offline authoring environment.
