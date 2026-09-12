# Myravant Source-Analysis / Design Information-Barrier Contract — PR2-IR

```yaml
artifact_id: PR2-IR-SOURCE-DESIGN-INFORMATION-BARRIER-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-IR
authority_reference: owner_directive_2026-09-11_pr2_ir_activation
authority_effect: information_barrier_and_representation_contract_only
starting_baseline: 8e2ba57ad61aac366e2d34c47811a3d17fd59220
source_research_authority: none
corpus_governance_authority: none
originality_or_rights_authority: none
native_content_authoring_authority: none
canon_promotion_authority: none
runtime_authority: none
production_schema_authority: none
model_training_authority: none
live_play_authority: none
```

## 1. Purpose

PR2-IR defines the explicit representation and information-flow boundary between
source-aware research and separately governed Myravant-facing design work.

Its purpose is to preserve two requirements simultaneously:

1. **internal traceability** — research provenance must remain exact enough for
   audit, correction, withdrawal, eligibility review, and later impact analysis;
2. **design-context independence** — source expression and unnecessary
   source-shaped detail must not become ordinary input to independent Myravant
   design merely because the project has researched it.

PR2-IR therefore governs what may cross the research-to-design boundary, what
must remain segregated, what audit metadata may exist without becoming design
input, how a boundary breach is recorded, and how the project can use the same
research program at 1,000+ source scale without turning provenance into design
contamination.

PR2-IR is not a legal safe harbor, originality certificate, source-processing
authorization, content-generation authorization, canon gate, runtime IR,
compiler IR, production schema, model-training policy, or live-play policy.

## 2. Authority boundary

PR2-IR owns only:

- the source-aware-research to Myravant-design information barrier;
- the distinction between research-plane, governance-bridge, and design-plane
  representations;
- the minimum lawful design handoff payload;
- governance-only metadata that must remain available for audit without being
  exposed as ordinary design input;
- prohibited and conditionally permitted cross-boundary information classes;
- context, retrieval, tool, and durable-artifact separation requirements at the
  handoff boundary;
- machine-trackable handoff disposition and barrier-breach evidence;
- escalation when lawful abstraction cannot be achieved without source-shaped
  leakage or missing doctrine.

PR2-IR consumes but does not replace PR2-SRC research outputs and provenance.
It coordinates with but does not replace PR2-ORG eligibility review.

PR2-IR must not own:

- source acquisition, reconnaissance, packet execution, or research depth;
- source registry, batching, coverage, genealogy, novelty, saturation, or bias
  governance (`PR2-CORPUS`);
- originality, rights, similarity, contamination disposition, or distribution
  eligibility (`PR2-ORG`);
- fiction/LitRPG-specific research interpretation (`PR2-FICT`);
- simulation/infrastructure exemplar interpretation (`PR2-SIMEX`);
- Myravant-native design authorship;
- gameplay doctrine;
- canon promotion;
- runtime packaging or runtime-origin policy;
- production database or service schemas;
- model training;
- live-play or GM behavior.

If enforcing the barrier would require deciding one of those matters, PR2-IR
must hand off or escalate rather than absorbing the missing authority.

## 3. Relationship to the source-research pipeline

PR2-SRC establishes the conceptual pipeline:

```text
external evidence
-> source-aware observation
-> normalized pressure
-> cross-source synthesis
-> Myravant-facing requirement
-> separately governed independent design
```

PR2-IR does not redefine these stages.

It governs the last information-flow boundary: the transition from
source-aware research/synthesis into a design-facing context.

Movement across that boundary is not a rename, paraphrase, summarization, or
formatting operation. A lawful handoff must deliberately select information
that Myravant design needs while withholding information whose presence would
unnecessarily make the design context source-shaped.

## 4. Three-plane separation

PR2-IR requires three distinguishable information planes.

### 4.1 Source-aware research plane

The research plane may lawfully contain, when acquired and handled under the
source-research program:

- source identity;
- source locators and provenance;
- source expression needed for audit;
- source-specific terminology;
- attributable observations;
- evidence modes;
- source-local structures and relationships;
- normalized pressures;
- synthesis inputs;
- contradiction and outlier evidence;
- research uncertainty and missing evidence.

The research plane may be source-aware because its job is to understand and
audit evidence.

Research-plane material is not ordinary Myravant design input.

### 4.2 Governance bridge plane

The governance bridge records **why and how** a design-facing handoff was
permitted, blocked, constrained, or escalated.

It may retain:

- research-record and provenance references;
- source-exposure classification;
- abstraction and synthesis rationale;
- withheld information classes;
- barrier checks;
- PR2-ORG review references where applicable;
- breach and remediation evidence;
- supersession history;
- handoff disposition and reviewer evidence.

The governance bridge is auditable project evidence. Its presence does not mean
that every field is visible to a designer or design model.

Exact source identity and provenance may be retained here through opaque or
access-controlled references that remain resolvable by governance tooling
without becoming ordinary design-context content.

### 4.3 Myravant design plane

The design plane receives only the information lawfully required to formulate
independent Myravant solutions.

A normal design-facing payload may contain:

- stable Myravant-facing requirement identity;
- requirement statement;
- capability, constraint, interaction, or evaluation need;
- relevant scope and applicability;
- preserved conflicts or tradeoffs;
- uncertainty that materially constrains design;
- outlier or edge-case pressure expressed without unnecessary source detail;
- acceptance or falsification conditions;
- design-local dependencies on other Myravant requirements.

The design plane does not gain research authority merely because the handoff was
produced from research.

## 5. Central laws

### 5.1 Traceability does not imply exposure

The project must preserve internal provenance without assuming that source
identity, source expression, locators, or source-specific examples belong in the
design context.

A governance record may know more than the design payload.

### 5.2 Paraphrase is not a barrier

Paraphrasing, translating, renaming, reformatting, summarizing, changing
numbers, or asking a model to rewrite source-shaped material does not by itself
make that material lawful design-plane input.

PR2-IR does not use a magic wording-distance or similarity-score threshold as a
substitute for representation separation.

### 5.3 Requirements are not designs

A lawful Myravant-facing requirement constrains or evaluates later design.
It does not prescribe a source construct as the answer.

The handoff must preserve the problem to solve rather than smuggle a preferred
source implementation through the requirement field.

### 5.4 Source frequency is not design authority

Repeated evidence may support synthesis, priority, or confidence.
It does not authorize source terminology, architecture, metaphysics, package
structure, or mechanics as Myravant design defaults.

### 5.5 The barrier does not certify originality or rights

A handoff that satisfies PR2-IR may still require PR2-ORG review.
PR2-ORG remains the owner of originality, similarity, rights, contamination,
and distribution eligibility.

Conversely, a recorded rights basis does not automatically make source-shaped
material appropriate for the independent-design pathway.

### 5.6 PR2-IR is not runtime IR

`PR2-IR` means the source-analysis / Myravant-design information and
representation boundary.

It does not define a compiler intermediate representation, runtime entity
representation, conversion IR, event format, persistence format, schema, or
network protocol.

## 6. Default design-handoff payload

A design handoff should be the smallest payload that preserves the validated
Myravant-facing problem without carrying unnecessary source-shaped material.

The default payload may include:

```text
requirement_id
requirement_version
requirement_statement
requirement_scope
capability_or_constraint_class
interaction_requirements[]
preserved_tradeoffs[]
preserved_uncertainties[]
outlier_pressures[]
acceptance_or_falsification_conditions[]
design_dependency_refs[]
```

This is a governance contract for the handoff surface, not a production schema
mandate.

No field name grants permission to include otherwise prohibited source content.

## 7. Governance-only handoff record

The project must also be capable of retaining a governance record for the
handoff without exposing the entire record to the design plane.

At minimum it must be capable of retaining:

```text
handoff_record_id
handoff_version
requirement_id
upstream_pressure_refs[]
upstream_synthesis_refs[]
research_provenance_refs[]
source_exposure_state
single_source_dependency_state
abstraction_basis
withheld_information_classes[]
prohibited_cue_check
org_review_refs[]
handoff_disposition
handoff_rationale
review_evidence_refs[]
review_decision_ref
supersedes_handoff_record_id
```

`research_provenance_refs[]` and similar fields are governance-plane evidence.
They are not automatically part of the design-facing payload.

## 8. Handoff dispositions

A machine-trackable handoff must support at least:

- `handoff_allowed`
- `handoff_allowed_with_constraints`
- `handoff_deferred_for_synthesis`
- `handoff_blocked_source_expression`
- `handoff_blocked_source_shaped_structure`
- `handoff_requires_org_review`
- `handoff_escalated`

These are information-barrier dispositions, not originality, rights,
distribution, canon, or runtime dispositions.

A blocked or deferred handoff remains lawful research evidence. It must not be
forced through the boundary merely to keep production moving.

## 9. Default-prohibited design-context material

Unless a separately governed exception route explicitly requires otherwise,
the independent-design context must not receive as ordinary design input:

- copied or closely rewritten source passages;
- source titles, authors, publishers, product identifiers, URLs, or source
  locators;
- source-specific proper nouns or signature terminology;
- source-format stat blocks, tables, catalogs, or presentation structure;
- one-to-one source construct inventories;
- source ordering or distinctive source taxonomy used as a design outline;
- source-specific examples whose details are not required by the normalized
  pressure;
- source-signature numeric packages or progression tables;
- donor-to-Myravant mappings or conversion notes;
- research transcripts whose source-aware detail exceeds the handoff payload;
- source-aware retrieval indexes or embeddings;
- provenance records whose identifiers or content expose source lineage to the
  design context without need;
- hidden or ephemeral research context used as an undeclared design input.

Removing attribution from any of these does not make the material safe to pass.

## 10. Conditionally permitted information

Some external information may be necessary to state a real requirement.
PR2-IR therefore does not impose a simplistic rule that every external name,
number, or fact is forbidden.

Conditionally permitted cases include:

- factual or empirical constraints needed to state the problem;
- interoperability identifiers required to interact with an external standard,
  protocol, file format, API, or platform;
- legally or operationally required attribution handled by a separately
  governed publication path;
- quantitative constraints that survive synthesis as functional requirements
  rather than source-signature packages;
- explicit adaptation or compatibility work operating under a separately
  authorized route rather than the independent-design pathway.

The governance record must explain why the information is necessary, what
source-shaped detail was withheld, and which downstream owner governs any
rights, publication, compatibility, or implementation decision.

PR2-IR does not itself decide that a claimed legal or licensing basis is valid.

## 11. Cross-source synthesis and single-source outliers

Cross-source synthesis is the normal research-to-requirement route because it
helps distinguish reusable pressure from one source's particular expression or
implementation.

However, corpus scale also guarantees meaningful outliers.

A requirement may lawfully depend on one source when that source reveals a
unique failure, edge case, embodiment, scale regime, institutional structure,
or capability pressure that other evidence has not yet reproduced.

A single-source handoff must:

- declare `single_source_dependency_state` in governance metadata;
- express the functional or structural pressure rather than the source artifact
  as the required solution;
- preserve uncertainty and lack of corroboration;
- avoid implying that rarity creates Myravant doctrine;
- defer or escalate when the source-shaped details cannot be abstracted without
  losing the actual pressure.

PR2-IR therefore does not require fake cross-source consensus before an outlier
can influence requirements.

## 12. Context and tool separation

The information barrier applies to model, human, tool, and retrieval context.

For independent Myravant design, the design context should be constructed from
the permitted design-handoff payload and applicable Myravant authority, not by
continuing inside an unrestricted source-research context.

A prompt saying “ignore the source material above” is not an information
barrier.

Where the same human or model capability participates in both phases, the
workflow must still create a separately bounded design context whose durable
inputs are the permitted handoff plus lawful Myravant materials.

The design context must not automatically inherit:

- retrieved source chunks;
- source research transcripts;
- source-aware scratch artifacts;
- source-bearing attachments;
- source-aware vector or retrieval indexes;
- research-only connector access;
- research tool state that exposes source material.

This section governs information exposure at the boundary. It does not specify
agent orchestration technology, memory implementation, model vendor, or
training procedure.

## 13. Durable-state rule

A lawful handoff must be reconstructible from durable project state.

The project must not depend on one model's hidden, ephemeral, or unrecoverable
context to prove what crossed the boundary.

Durable governance records should make it possible to answer:

- which requirement was handed off;
- which research/synthesis records supported it;
- what source-sensitive information was withheld;
- what exceptions were permitted and why;
- whether PR2-ORG review was required;
- what design-facing payload was actually supplied;
- whether the handoff was later superseded or invalidated.

This requirement supports auditability without moving the provenance ledger
into the design payload or runtime.

## 14. Barrier breach and contamination routing

If prohibited source material reaches the independent-design context, the
project must record a barrier breach rather than pretending the material can be
“unseen.”

A breach must preserve enough evidence to identify the affected handoff,
context, and candidate artifacts.

Lawful responses may include:

- stop the affected design work;
- quarantine the affected candidate under PR2-ORG;
- route to `contamination_review_required` or another applicable PR2-ORG state;
- issue a superseding handoff from a properly segregated design context;
- independently replace the affected design where authorized;
- escalate when impact cannot be bounded.

Starting a fresh design context may be required to restore the information
boundary, but doing so does not erase the exposure event or prove originality.
PR2-ORG remains the owner of any resulting contamination or eligibility
disposition.

## 15. Eligibility and independent-design relationship

PR2-IR compliance is evidence about **how information flowed**.
PR2-ORG evaluates **whether a candidate is eligible**.

A PR2-IR-compliant handoff may become one input to an originality/similarity
review, but it does not guarantee `myravant_original_review_passed`,
`distribution_eligible`, or `eligible_for_separate_canon_review`.

A PR2-ORG rights basis likewise does not retroactively convert an information-
barrier breach into an independently authored pathway.

## 16. Licensed, public-domain, compatibility, and adaptation outliers

The project may later authorize work whose purpose is explicit adaptation,
compatibility, standards interoperability, or use under a documented rights
basis.

Such work must not be mislabeled as the default independent-design pathway.

PR2-IR may record that a different route applies and may preserve the necessary
exposure evidence, but:

- PR2-ORG still owns rights/originality/eligibility state;
- the applicable design or compatibility owner must authorize the work;
- canon remains separate;
- runtime remains separate;
- source provenance must not be destroyed to make the result appear native.

## 17. Relationship to PR2-CORPUS

PR2-CORPUS owns source registry, batching, coverage, genealogy, novelty,
saturation, and bias governance.

PR2-IR must scale to those future corpus operations without taking them over.

At 1,000+ source scale:

- design contexts must not receive a provenance dump for every supporting
  source;
- many source records may support one pressure or requirement;
- one source may support many pressures;
- opaque governance references may preserve traceability without exposing
  source identity to the design context;
- handoff review must be queryable independently of corpus frequency;
- a batch boundary must not become an information-barrier boundary by accident;
- saturation does not grant permission to move source expression into design.

## 18. Relationship to PR2-FICT and PR2-SIMEX

PR2-FICT and PR2-SIMEX may later define specialized interpretation rules for
fiction/LitRPG and simulation/infrastructure evidence.

Their outputs must still cross the same PR2-IR information barrier before they
become ordinary Myravant design input.

PR2-IR does not predefine their specialized research semantics.

## 19. Relationship to canon and runtime firewall

The existing conversion/runtime origin firewall remains authoritative.

PR2-IR is an earlier boundary:

```text
source-aware research
-> PR2-IR design handoff
-> separately authorized Myravant design
-> PR2-ORG / doctrine / conflict / canon review as applicable
-> canon promotion
-> runtime-origin firewall
-> runtime
```

Passing PR2-IR does not create canonical identity or runtime eligibility.

Source provenance remains in offline governance. Runtime must still be blind to
pre-canon lineage under the runtime-origin firewall.

## 20. Machine-checkable barrier assurances

Later tooling should be able to test, without requiring semantic guesswork for
every check:

- whether a handoff has a stable ID and version;
- whether required governance references exist;
- whether a design payload is distinct from governance-only metadata;
- whether prohibited source identifiers or locators appear in allowlisted
  design fields;
- whether source-aware attachments or indexes are configured for the design
  context;
- whether a barrier breach record exists when exposure is known;
- whether superseded handoffs remain traceable;
- whether PR2-ORG review is referenced when the handoff disposition requires it.

Deterministic checks cannot prove originality. Semantic review remains necessary
for source-shaped structure, distinctive combinations, and disguised
paraphrase.

## 21. Failure and escalation conditions

A handoff must stop, defer, or escalate when:

- the proposed design payload still depends on source expression;
- the requirement is effectively a source implementation specification;
- source-specific structure cannot be removed without losing the claimed
  pressure;
- provenance needed for audit is missing or conflicted;
- contradictory evidence has been flattened into fake consensus;
- a rights or similarity question belongs to PR2-ORG;
- the research question must be reopened under PR2-SRC;
- corpus coverage or saturation questions belong to PR2-CORPUS;
- specialized fiction/simulation interpretation belongs to PR2-FICT or
  PR2-SIMEX;
- missing gameplay or framework doctrine would have to be invented;
- implementation, canon, runtime, training, or live-play authority would be
  required.

`handoff_escalated` is preferable to decorative Myravant wording that conceals
an unresolved boundary problem.

## 22. Anti-drift refusals

PR2-IR rejects:

- `source text -> paraphrase -> design input`;
- `source mechanic -> renamed requirement -> Myravant mechanic`;
- `source taxonomy -> Myravant taxonomy by default`;
- `source implementation -> Myravant implementation specification`;
- `many sources agree -> source structure may cross the barrier`;
- `licensed -> therefore independently authored`;
- `publicly available -> therefore safe design context`;
- `AI rewritten -> therefore independent`;
- `source removed from prompt -> prior exposure no longer matters`;
- `provenance deleted -> contamination solved`;
- `PR2-IR passed -> originality passed`;
- `PR2-IR passed -> canon`;
- `PR2-IR passed -> runtime`;
- `PR2-IR -> runtime/compiler intermediate representation`.

## 23. Acceptance conditions

PR2-IR is complete only when:

1. research, governance-bridge, and design planes are explicit;
2. exact provenance can remain auditable without becoming ordinary design input;
3. a bounded design-handoff payload is explicit;
4. governance-only metadata is distinct from design-visible payload;
5. default-prohibited and conditionally permitted information classes are
   explicit;
6. paraphrase and similarity thresholds cannot substitute for the barrier;
7. cross-source synthesis and single-source outliers both have lawful routes;
8. context, retrieval, attachment, and tool-state separation are explicit;
9. barrier breaches are evidence-preserving and route to PR2-ORG when needed;
10. licensed/adaptation/compatibility outliers do not masquerade as independent
    design;
11. corpus-scale many-to-many provenance remains compatible with future
    PR2-CORPUS;
12. PR2-IR is explicitly distinct from runtime/compiler IR;
13. the existing runtime-origin firewall remains complementary authority;
14. no source processing, corpus execution, native-content authoring, canon,
    runtime implementation, R3 execution, model training, or live-play behavior
    is authorized.

## 24. Current activation state

PR2-ORG post-merge closure merged through PR `#388` as merge commit
`8e2ba57ad61aac366e2d34c47811a3d17fd59220`.

PR2-IR is active under `owner_directive_2026-09-11_pr2_ir_activation` from that
exact merged baseline.

`PR2-CORPUS`, `PR2-FICT`, and `PR2-SIMEX` remain
`ready_pending_authorization` and are not activated by PR2-IR.

R3 remains `ready_pending_authorization` against its exact 34-record conformance
target with execution disabled.

No source acquisition, research execution, corpus execution, native-content
authoring, canon promotion, runtime/schema implementation, model training, or
live-play/GM behavior is authorized by this file.
