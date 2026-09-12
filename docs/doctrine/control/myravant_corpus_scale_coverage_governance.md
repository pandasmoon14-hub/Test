# Myravant Corpus Scale, Coverage, and Saturation Governance — PR2-CORPUS

```yaml
artifact_id: PR2-CORPUS-SCALE-COVERAGE-GOVERNANCE-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-CORPUS
authority_reference: owner_directive_2026-09-12_pr2_corpus_activation
authority_effect: corpus_governance_only
starting_baseline: 92a4b6e15d9df10dedf4cec8bd1267111975cba2
minimum_external_source_scale: 1000
source_acquisition_authority: none
source_processing_authority: none
research_method_authority: none
information_barrier_authority: none
originality_or_rights_authority: none
native_content_authoring_authority: none
canon_authority: none
runtime_authority: none
model_training_authority: none
live_play_authority: none
```

## 1. Purpose

PR2-CORPUS defines the corpus-scale governance needed for Myravant to plan,
measure, diversify, and audit a heterogeneous external research corpus of at
least 1,000 sources without confusing source count with knowledge, popularity
with authority, repetition with independent evidence, or declining novelty in
one region of the corpus with global completion.

Its purpose is to make the following machine-trackable at corpus scale:

- source registration and stable corpus identity;
- source-family and evidence-family coverage;
- bounded batch planning;
- genealogy and effective-independence accounting;
- research-state accounting without pretending registration equals analysis;
- novelty yield and diminishing-return evidence;
- local and provisional saturation claims;
- coverage gaps, skew, and bias risks;
- explicit preservation of rare and single-source outliers;
- reopening and escalation when new evidence falsifies a saturation claim.

PR2-CORPUS governs the *research portfolio*. It does not perform the research.

The controlling scale assumption is a heterogeneous corpus of at least 1,000
external works spanning game, fiction, actual-use, empirical, institutional,
historical, technical, software, simulation, failure, and other lawful evidence.

The number `1,000` is a scale requirement for architecture. It is not a quota
whose attainment proves adequate coverage, research completion, originality,
canon readiness, or design quality.

## 2. Authority boundary

PR2-CORPUS owns only:

- the corpus registry and stable corpus-facing source identity;
- coverage-dimension governance;
- large-scale batching and selection rationale;
- genealogy and research-independence accounting;
- novelty accounting at source, batch, question, and coverage-cell levels;
- saturation evidence and reopening rules;
- skew, gap, and bias-risk accounting;
- outlier-preservation requirements;
- corpus-level stop, defer, rebalance, and escalation signals;
- machine-trackable corpus governance records;
- auditability of why evidence was or was not selected for deeper research.

PR2-CORPUS consumes but does not replace PR2-SRC research outputs and methods.

It may reference PR2-ORG and PR2-IR records where needed to preserve boundaries,
but it does not perform eligibility review or source-to-design handoff.

PR2-CORPUS must not own:

- source acquisition, licensing, scraping, downloading, or access decisions;
- source reconnaissance, scouting, focused analysis, deep analysis, pressure
  extraction, or cross-source synthesis execution;
- research-method qualification (`PR2-SRC`);
- originality, rights, similarity, contamination, quarantine, or distribution
  eligibility (`PR2-ORG`);
- source-analysis / Myravant-design information-barrier policy (`PR2-IR`);
- fiction/LitRPG-specific interpretation (`PR2-FICT`);
- simulation/infrastructure exemplar-specific interpretation (`PR2-SIMEX`);
- Myravant-native content authoring;
- gameplay doctrine;
- canon promotion;
- runtime architecture or implementation;
- production database or service schemas;
- model training;
- conversion execution;
- live-play or GM behavior.

If corpus governance would require taking one of those authorities, the lawful
result is handoff or escalation.

## 3. Central laws

### 3.1 Source count is not coverage

A corpus containing 1,000 sources may still be narrow if most sources occupy the
same lineage, medium, genre, market, era, rules tradition, problem family, or
evidence mode.

Raw source count must never be the sole corpus-quality metric.

### 3.2 Source frequency is not doctrine authority

A construct appearing in many sources may justify further synthesis, priority,
or confidence that a pressure is common.

Frequency does not create Myravant doctrine, canon, ownership, rights,
originality, metaphysics, architecture, or mandatory mechanics.

### 3.3 Registration is not research

A registered source is known to the corpus.

It is not thereby scouted, analyzed, synthesized, converted, eligible, or
design-relevant.

Corpus state must keep registration, examination, and downstream research
outputs distinguishable.

### 3.4 Genealogical repetition is not independent corroboration

Editions, revisions, translations, adaptations, descendants of one rules
engine, derivative implementations, shared standards, copied taxonomies, and
other common-lineage evidence may be useful.

They must not be counted as fully independent convergence merely because they
are separate files, books, repositories, products, or editions.

### 3.5 Coverage is multidimensional

There is no single universal coverage percentage.

Coverage claims must name the dimensions and scope to which they apply.

### 3.6 Saturation is local, provisional, and reversible

PR2-CORPUS forbids an unqualified claim that “the corpus is saturated.”

Saturation may be claimed only for a bounded research question, coverage cell,
source family, interaction family, or other explicit scope, and only from
recorded evidence.

Any material outlier, contradiction, new source family, new evidence mode, or
new downstream requirement may reopen the scope.

### 3.7 Diminishing novelty does not erase outliers

Low average novelty in a mature source family does not justify discarding rare,
structurally unusual, contradictory, failure-heavy, or high-leverage evidence.

Outlier capacity must remain explicitly reserved.

### 3.8 Famous, large, or accessible sources receive no automatic authority

Brand prominence, page count, sales, community size, search ranking, citation
count, ease of access, or familiarity may affect discovery.

None of them independently justifies deep analysis, weighting, or Myravant
authority.

### 3.9 Missing and unknown coverage must remain visible

Unknown genealogy, inaccessible sources, missing languages, missing regions,
unrepresented evidence modes, and unexamined source families must not silently
be treated as zero-risk or complete.

Unknown is a corpus state, not permission to infer coverage.

## 4. Relationship to PR2-SRC

PR2-SRC establishes:

```text
external evidence
-> source-aware observation
-> normalized pressure
-> cross-source synthesis
-> Myravant-facing requirement
-> separately governed independent design
```

PR2-CORPUS does not redefine that pipeline.

It governs how the external-evidence and research-portfolio side of the program
is registered, sampled, balanced, revisited, and measured at scale.

PR2-SRC owns research depth and research method.

PR2-CORPUS may record that a source is `scouted`, `focused_analyzed`, or
`deep_analyzed` only as a corpus-state fact produced by the lawful research
process. It does not decide the research result.

A corpus batch may request scouting, focused analysis, or deep analysis. The
actual method remains PR2-SRC-governed.

## 5. Relationship to PR2-ORG and PR2-IR

PR2-CORPUS may retain references needed to coordinate with eligibility and
information-barrier governance.

It must not collapse their states into corpus states.

In particular:

- a source being common does not make a candidate eligible;
- a source being rare does not make a candidate ineligible;
- a source being open, licensed, public-domain, commissioned, or otherwise
  rights-classified does not make it more doctrinally authoritative;
- a source passing eligibility review does not make source-shaped material
  appropriate design input;
- a source being omitted from a design payload does not remove it from internal
  corpus provenance.

Corpus records may know source identity and lineage because corpus governance is
source-aware.

Design-facing exposure remains governed by PR2-IR.

## 6. Registry model

The corpus registry is an accountability surface, not a content catalog.

Every registered source must be capable of carrying at least:

```text
source_record_id
source_version_id
source_kind
source_identity_ref
source_status
availability_state
modality_labels[]
evidence_mode_signals[]
coverage_dimension_values{}
genealogy_cluster_refs[]
known_predecessor_refs[]
known_successor_refs[]
research_state
research_unit_refs[]
pressure_record_refs[]
synthesis_refs[]
selection_history_refs[]
batch_refs[]
rights_or_eligibility_refs[]
material_uncertainties[]
```

This is a governance contract, not a production database schema.

A field name does not authorize information exposure outside its lawful layer.

`source_identity_ref` must remain sufficient for internal accountability. It
does not imply that the source identity belongs in the Myravant design context.

## 7. Source and research-state distinction

Corpus-scale tracking must distinguish at least these research states:

- `registered`
- `scout_requested`
- `scouted`
- `focused_analysis_requested`
- `focused_analyzed`
- `deep_analysis_requested`
- `deep_analyzed`
- `deferred`
- `inaccessible`
- `withdrawn_from_future_research`

These states describe research progress or routing.

They do not encode originality, rights, design authority, canon status, or
runtime identity.

A source may move through several states over time.

A source may also contain many research units at different research depths.

Therefore source-level research state must not erase unit-level detail when that
detail is material.

## 8. Coverage dimensions

PR2-CORPUS requires an extensible coverage-dimension registry rather than one
hard-coded universal taxonomy.

Coverage dimensions may include, when materially relevant:

- medium and source kind;
- research modality;
- evidence mode;
- game/system family;
- problem or capability family;
- content-heavy versus framework-heavy emphasis;
- procedural/generative emphasis;
- actor, institution, world, or infrastructure focus;
- scale regime;
- lifecycle stage;
- failure and rules-in-use evidence;
- temporal period;
- technical lineage;
- disciplinary lineage;
- geographic or cultural context;
- language or translation context;
- commercial, community, academic, governmental, open-source, or other
  production context;
- accessibility and survivorship conditions;
- empirical versus conceptual evidence;
- ordinary-life versus exceptional-system evidence;
- source genealogy and effective independence.

This list is deliberately non-exhaustive.

A coverage dimension must exist because it affects research risk, missing
pressure, representativeness, independence, or downstream confidence—not merely
because metadata is available.

Coverage governance must avoid unnecessary sensitive-person profiling. The
corpus concerns source evidence, not demographic surveillance of individual
people.

## 9. Coverage records

A bounded coverage record must be capable of carrying:

```text
coverage_record_id
coverage_scope
coverage_dimensions{}
registered_source_refs[]
examined_source_refs[]
independent_lineage_refs[]
unresolved_genealogy_refs[]
research_depth_summary
novelty_summary_refs[]
contradiction_refs[]
outlier_refs[]
known_gap_refs[]
bias_risk_refs[]
saturation_state
saturation_evidence_refs[]
last_reopened_reason
review_decision_ref
```

Coverage must distinguish at least:

1. **registered coverage** — what the registry knows exists;
2. **examined coverage** — what has received lawful research attention;
3. **independent-lineage coverage** — how much evidence is not merely repeated
   lineage;
4. **pressure coverage** — which normalized research pressures are represented;
5. **contradiction/outlier coverage** — whether rare and conflicting evidence is
   being preserved.

No one of these substitutes for the others.

## 10. Genealogy and effective independence

PR2-CORPUS owns research-genealogy accounting.

Genealogy may record relationships such as:

- edition or revision;
- translation or localization;
- adaptation;
- supplement or extension;
- shared engine or rules lineage;
- fork or derivative implementation;
- shared standard or protocol ancestry;
- compilation or anthology relationship;
- common upstream dataset;
- common institutional or methodological lineage;
- direct response, patch, errata, or rebuttal;
- unknown or disputed lineage.

These are research-dependence relationships.

They are not copyright, licensing, originality, or legal conclusions.

A corpus report must be able to distinguish:

```text
raw_source_count
examined_source_count
genealogy_cluster_count
independent_lineage_count
unknown_lineage_count
```

A hundred closely related descendants may still reveal important variation.

They must not masquerade as one hundred independent confirmations.

## 11. Batch governance

Corpus work must be planned in bounded batches.

A batch is a research-portfolio unit, not a donor-conversion wave.

A batch record must be capable of carrying:

```text
batch_id
batch_version
research_question_refs[]
selection_rationale
target_coverage_gaps[]
target_contradictions[]
target_genealogy_diversification[]
selected_source_refs[]
reserved_outlier_slots[]
requested_research_depths{}
depth_budget_rationale
expected_information_gain
known_selection_biases[]
stop_conditions[]
reopen_conditions[]
batch_state
resulting_coverage_refs[]
resulting_novelty_refs[]
review_decision_ref
```

Batch selection should be explainable before execution.

The selection rationale should state what gap, contradiction, outlier, lineage,
or uncertainty the batch is intended to reduce.

## 12. Selection law

Source selection should optimize information value rather than volume read.

Lawful selection reasons include:

- filling a declared coverage gap;
- testing a saturation hypothesis;
- diversifying genealogy;
- investigating a contradiction;
- preserving an unusual outlier;
- studying severe failure evidence;
- probing an underrepresented scale regime;
- examining an unusual institution or ordinary-life process;
- comparing implementation with actual use;
- testing whether a supposedly common pattern survives outside one lineage;
- investigating a generative structure with high downstream leverage.

The following are not sufficient by themselves:

- famous source;
- popular source;
- large source;
- recent source;
- old source;
- source already owned by the project;
- source easy for a model to process;
- source with many options;
- source from the dominant current genre;
- source repeated across many derivative works.

## 13. Research-depth portfolio control

PR2-SRC-B defines scout, focused, and deep research methods.

PR2-CORPUS governs the portfolio distribution of those requests.

At 1,000+ source scale, uniform deep analysis is prohibited as a default
strategy.

A lawful corpus program should use scouting broadly, focused analysis where a
bounded question justifies it, and deep analysis where information value,
contradiction, interaction density, failure significance, novelty, or downstream
leverage justify the cost.

This is not a fixed percentage allocation.

The distribution may change as the corpus reveals new gaps and saturation.

## 14. Novelty accounting

Novelty means materially new research information, not merely new wording,
names, entries, products, or examples.

A novelty record must be scoped to a research question or coverage context.

Minimum novelty states:

- `novelty_unassessed`
- `no_material_novelty`
- `local_novelty`
- `cross_family_novelty`
- `outlier_novelty`
- `contradictory_novelty`
- `novelty_uncertain`

Novelty may arise from:

- a new normalized pressure;
- a new interaction among known pressures;
- a new failure mode;
- a new utilization path;
- a new scale or lifecycle regime;
- a contradiction of prior synthesis;
- a new generative dimension;
- a new institutional or social relationship;
- evidence that a supposed universal is lineage-local;
- evidence that reopens a saturation claim.

Novelty does not imply the project should create new Myravant content.

## 15. Saturation governance

Saturation is a research-allocation signal.

It is not proof of completeness.

Minimum saturation states:

- `saturation_not_assessed`
- `insufficient_coverage`
- `declining_novelty_observed`
- `provisionally_saturated`
- `saturation_reopened`

A `provisionally_saturated` claim must identify:

```text
saturation_scope
research_question_refs[]
coverage_dimensions{}
genealogy_diversity_evidence
recent_batch_refs[]
novelty_yield_evidence
known_exclusions[]
known_outliers[]
known_contradictions[]
reopen_conditions[]
review_decision_ref
```

A saturation claim must fail closed to `insufficient_coverage` or remain
unassessed when genealogy, coverage, or novelty evidence is too incomplete to
support the claim.

No fixed global source count or fixed “N consecutive low-novelty sources”
threshold is universal doctrine.

A project may define operational thresholds later for a bounded campaign, but
those thresholds must remain reviewable and scope-specific.

## 16. Saturation reopening

A provisionally saturated scope must be reopened when materially new evidence
appears, including:

- a new independent lineage;
- a source family previously absent from the scope;
- a high-information outlier;
- a contradiction of the current synthesis;
- a severe failure mode;
- a new evidence mode;
- a new downstream capability question;
- a new scale regime;
- evidence of systematic selection bias;
- evidence that genealogy had been misclassified;
- evidence that the prior novelty measure was too coarse.

Reopening is not a failure.

It is the normal mechanism that prevents stale corpus conclusions from becoming
hidden doctrine.

## 17. Outlier preservation

Outliers are first-class corpus evidence.

A corpus program must reserve capacity for sources that are rare, awkward,
cross-genre, noncommercial, unsuccessful, inaccessible in part, culturally or
technically distant from the dominant sample, structurally unusual, or
apparently incompatible with prevailing assumptions.

An outlier must not be discarded solely because:

- no other source corroborates it;
- it complicates a clean taxonomy;
- it lowers apparent saturation;
- it is expensive to analyze;
- it is not a game;
- it is not currently popular;
- its design failed;
- it represents a minority architecture or interaction pattern.

A single source may lawfully reveal a project-falsifying edge case.

PR2-CORPUS must therefore support `outlier_novelty` and explicit escalation
without requiring fake cross-source consensus.

## 18. Bias and skew governance

Corpus-scale research is vulnerable to selection bias.

At minimum, governance must be able to record risks from:

- overrepresentation of one genre or rules lineage;
- English-language or translation availability;
- commercial visibility and search ranking;
- survivorship and publication bias;
- recency bias;
- nostalgia or familiarity bias;
- platform availability;
- open-source visibility;
- academic-publication bias;
- Western or other regional/cultural concentration;
- digital-availability bias;
- successful-product bias;
- rules-heavy-source bias;
- content-heavy-source bias;
- source-size bias;
- benchmark or exemplar overfitting.

Bias records are not accusations about a source.

They describe the research portfolio.

Minimum bias states:

- `bias_not_assessed`
- `known_skew`
- `mitigation_planned`
- `mitigation_applied`
- `accepted_with_rationale`
- `bias_unknown`

Equal quotas across every dimension are not required.

The purpose is to make skew visible and deliberate rather than accidental.

## 19. Unknown, inaccessible, and unavailable evidence

A corpus registry may know about evidence that cannot currently be examined.

Such evidence should remain distinguishable from absent evidence.

`inaccessible` may reflect technical, legal, financial, language, archival, or
other access constraints.

PR2-CORPUS records the gap.

It does not authorize circumvention, acquisition, scraping, or rights decisions.

A saturation claim must state whether inaccessible evidence could materially
change the conclusion.

## 20. Failure, abandoned, and superseded sources

Failed, abandoned, deprecated, superseded, or commercially unsuccessful systems
remain lawful research evidence when acquired and handled under the source
program.

Corpus selection must not optimize only for surviving successful products.

Negative evidence may have high information value.

Genealogy must also preserve supersession relationships so later versions do
not silently erase the existence of prior failures.

## 21. Cross-family coverage

The corpus architecture must survive at least these pressure families without
making any one family the baseline:

- fantasy;
- science fiction;
- science-fantasy and hybrid;
- cultivation and progression;
- class/archetype;
- profession/occupation;
- point-buy;
- narrative/tag/aspect;
- cyberware and biotech;
- psionic and supernatural;
- horror and investigation;
- vehicle, mech, ship, and platform;
- companion and summon;
- crafting, salvage, and requisition;
- bestiary and ecology;
- setting and world supplement;
- procedural/generator-heavy;
- adventure and scenario;
- fiction and actual play;
- software and repositories;
- simulation and infrastructure;
- economics, ecology, medicine, engineering, war, history, institutions, and
  other ordinary-life or technical evidence.

This is a pressure checklist, not a fixed quota system.

Unseen families are expected.

The architecture must allow new dimensions and escalation without redefining
the whole registry.

## 22. Corpus metrics that are lawful

Lawful metrics may include:

- registered source count;
- examined source count;
- research-unit count;
- genealogy-cluster count;
- independent-lineage count;
- coverage-gap count;
- unresolved-genealogy count;
- batch-level novelty yield;
- contradiction discovery;
- outlier discovery;
- provisional-saturation scope count;
- reopened-saturation count;
- bias-risk count;
- pressure and requirement coverage references;
- research-depth distribution.

Metrics must retain their scope.

No metric becomes a doctrine vote merely because it is numeric.

## 23. Metrics that are insufficient or prohibited as sole success measures

The following must not be used alone to prove corpus quality:

- number of books owned;
- number of files downloaded;
- number of pages processed;
- number of sources registered;
- number of sources summarized;
- number of mechanics extracted;
- number of converted artifacts;
- number of renamed constructs;
- number of embeddings;
- number of generated requirements;
- percentage of one genre represented;
- raw frequency of a mechanic;
- model token consumption.

These may be operational measurements.

They are not proof of coverage, independence, originality, or saturation.

## 24. Corpus-level stop and rebalance signals

A batch or bounded research campaign may stop, defer, or rebalance when:

- its declared research question is answered;
- novelty yield is declining within a sufficiently diverse local scope;
- the next useful evidence requires a new source family;
- genealogy shows the current sample is too dependent;
- bias risk makes more of the same sample misleading;
- a contradiction requires focused investigation before breadth expansion;
- a severe outlier justifies deep analysis;
- source access blocks the current plan;
- the research method must be escalated to PR2-SRC;
- the information barrier or eligibility process exposes a governance gap.

Stopping one batch does not close the corpus.

## 25. Escalation conditions

PR2-CORPUS must escalate rather than invent doctrine when:

- a necessary coverage dimension cannot be represented without semantic loss;
- genealogy is materially disputed or unknowable;
- a saturation conclusion depends on an unjustified threshold;
- a selection plan would require source acquisition authority;
- a batch requires a new research method rather than merely a new selection;
- bias mitigation would require collecting inappropriate personal data;
- a source family exposes missing PR2-SRC, PR2-ORG, or PR2-IR doctrine;
- source-scale behavior creates a genuine new Astra/Myravant doctrine question;
- coverage conflicts cannot be resolved without choosing a gameplay or runtime
  design.

Escalation preserves the gap.

PR2-CORPUS must not create decorative Myravant terminology to hide it.

## 26. Corpus execution separation

This contract does not authorize:

- bulk source acquisition;
- automated scraping;
- bulk reconnaissance;
- packet execution;
- model-driven source reading;
- embedding production;
- source summarization at scale;
- pressure extraction at scale;
- cross-source synthesis execution;
- native-content generation;
- conversion;
- training.

Those activities require separately authorized execution work.

PR2-CORPUS activation means the portfolio-governance architecture exists.

It does not mean the research corpus is running.

## 27. Completion meaning for PR2-CORPUS

PR2-CORPUS is complete when the governance framework itself can lawfully and
machine-trackably represent:

- source registry state;
- coverage dimensions;
- genealogy and effective independence;
- bounded batches;
- research-depth portfolio requests;
- novelty;
- local provisional saturation;
- saturation reopening;
- outliers;
- bias and gaps;
- stop/rebalance decisions;
- escalation.

Completion does not require processing 1,000 sources.

Completion does not assert that any corpus region is saturated.

Completion does not authorize PR2-AUDIT, PR2-FICT, PR2-SIMEX, source execution,
native-content authoring, canon, runtime work, R3, training, conversion, or
live play.

## 28. Corpus-scale adversarial cases

The framework must remain lawful when confronted with:

1. 500 sources descended from one rules engine;
2. 20 obscure sources producing more novelty than 300 popular sources;
3. a single failed game exposing a severe economy failure;
4. one non-game institutional source invalidating a common game assumption;
5. a rare source family appearing only after a scope was provisionally saturated;
6. multiple translations that look independent but share one underlying text;
7. a famous source with low information value for the current question;
8. a tiny source with high cross-family leverage;
9. a source with unknown genealogy;
10. inaccessible but plausibly material evidence;
11. one culture, language, region, era, or platform dominating discovery;
12. a batch whose low novelty reflects poor selection rather than true
    saturation;
13. a mature source family that still contains unresolved contradictions;
14. a source that is deeply analyzed but contributes no new pressure;
15. a new downstream requirement reopening previously settled coverage;
16. a content catalog with thousands of entries but little generative novelty;
17. a small generator encoding a large possibility space;
18. empirical evidence that conflicts with rules-heavy source consensus;
19. many sources repeating one inherited misconception;
20. a structurally novel outlier with no corroborating peer.

These cases require lawful registration, coverage, genealogy, novelty,
saturation, bias, outlier, or escalation outcomes.

They do not justify corpus-shaped Myravant design.

## 29. Non-authority statement

PR2-CORPUS is portfolio governance only.

It does not create source authority, donor authority, doctrine authority,
originality authority, legal authority, canon authority, design authority,
runtime authority, training authority, or live-play authority.

Its job is to make a large research corpus *auditable, selective, diverse,
reopenable, and resistant to false confidence*.

Nothing in this contract permits a source, source family, majority pattern,
popular mechanic, or saturation metric to become hidden Myravant law.
