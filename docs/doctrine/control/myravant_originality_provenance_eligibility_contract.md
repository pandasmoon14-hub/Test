# Myravant Originality, Provenance, and Content Eligibility Contract — PR2-ORG

```yaml
artifact_id: PR2-ORG-ORIGINALITY-PROVENANCE-ELIGIBILITY-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-ORG
authority_reference: owner_directive_2026-09-11_pr2_org_activation
authority_effect: content_eligibility_and_provenance_governance_only
starting_baseline: c14da427bf5c5c21c7ef1655e83aea3519587cc6
source_research_authority: none
corpus_governance_authority: none
information_barrier_authority: none
canon_promotion_authority: none
runtime_authority: none
native_content_authoring_authority: none
live_play_authority: none
legal_advice_authority: none
```

## 1. Purpose

PR2-ORG defines the project-side governance required to determine whether a
Myravant candidate may lawfully advance beyond research-only or quarantined
status.

Its scope is operational and evidentiary:

- preserve provenance needed for eligibility review;
- classify the rights basis or unresolved rights question relevant to a candidate;
- record originality and similarity-review state;
- record contamination and quarantine state;
- produce a machine-trackable content-eligibility disposition;
- preserve enough evidence to re-evaluate, withdraw, or isolate affected candidates later.

PR2-ORG does not decide Myravant mechanics, perform source research, implement
the source-to-design information barrier, run the 1,000+ source corpus, promote
canon, implement runtime behavior, or provide legal advice.

The controlling posture is:

> **Traceable internally; independently Myravant externally.**

Traceability is required for audit and correction. Traceability is not
permission to distribute source-derived material.

## 2. Owner boundary

PR2-ORG owns only project-side originality, provenance-for-eligibility,
rights-review state, similarity review, contamination/quarantine, and content
eligibility.

It consumes, but does not replace, PR2-SRC provenance continuity.

It must not own:

- source acquisition, reconnaissance, pressure extraction, or synthesis;
- `PR2-IR` information-barrier design or source/design representation;
- `PR2-CORPUS` registry, coverage, genealogy, novelty, saturation, or batching;
- `PR2-FICT` fiction/LitRPG research interpretation;
- `PR2-SIMEX` simulation/infrastructure exemplar interpretation;
- Myravant-native content authoring;
- gameplay doctrine;
- canon promotion;
- runtime packaging or runtime-origin policy;
- model training;
- live-play or GM behavior;
- in-world institutions, jurisdiction, rights, law, policy, adjudication,
  legitimacy, or enforcement owned by AFQR-15.

AFQR-15 concerns rights and law inside modeled worlds. PR2-ORG concerns the
project's handling of external-source influence and candidate distribution
eligibility. Neither transfers authority to the other.

## 3. Central laws

### 3.1 Provenance preservation is mandatory

Eligibility review must never require destroying or obscuring provenance.

Deleting attribution, lineage, exposure history, or source references from the
offline governance record does not make a candidate more original or more
eligible.

### 3.2 Semantic correctness does not imply eligibility

A candidate may be mechanically correct, doctrinally compatible, useful,
well-designed, or fully normalized and still be ineligible for distribution.

Semantic disposition and content eligibility are separate dimensions.

### 3.3 Eligibility does not imply canon

An eligibility result may remove an originality or rights blocker.

It does not promote canon, establish gameplay doctrine, create runtime identity,
or authorize publication by itself.

`eligible_for_separate_canon_review` means only that PR2-ORG has no remaining
eligibility blocker known within its scope. Canon authority remains separate.

### 3.4 Transformation is not proof of independence

None of the following establishes originality or independent ownership by
itself:

- renaming;
- translation;
- paraphrase;
- numeric alteration;
- format conversion;
- mechanical relabeling;
- recombination of source material;
- AI rewriting or regeneration;
- removal of attribution;
- successful semantic conversion;
- successful normalization;
- successful schema validation.

### 3.5 Source prevalence is irrelevant to ownership

A mechanic, phrase, pattern, or structure appearing in many sources does not
become Myravant property through frequency.

Corpus frequency is research evidence. It is not a rights vote, originality
vote, doctrine vote, or eligibility vote.

### 3.6 Unknown must remain unknown

Where the available evidence cannot support an originality, rights, or
distribution conclusion, the lawful result must preserve the unresolved
dimension explicitly: for example `specialist_rights_review_required` for the
rights-review dimension, `similarity_review_required` for originality/similarity,
`quarantined_similarity_risk` or `quarantined_rights_risk` for quarantine, or
`eligibility_review_required` for final eligibility.

The project must not manufacture certainty from missing documentation.

## 4. Candidate and provenance scope

PR2-ORG evaluates a bounded Myravant candidate or candidate package.

A reviewable candidate must have a stable offline governance identity distinct
from external-source, source-observation, pressure-record, synthesized-
requirement, and later canonical/runtime identity.

The eligibility record must be able to reference an **influence cluster**:
the set of source-aware observations, pressures, requirements, prior drafts,
human inputs, generated outputs, licenses, permissions, or other evidence
materially relevant to the candidate's eligibility review.

An influence cluster is an audit scope. It is not proof that every referenced
source contributed protectable expression, and it is not itself a rights
conclusion.

One source may contribute to many pressure records without producing any
Myravant content. Many sources may contribute to one synthesized requirement
without requiring a corresponding Myravant artifact. One candidate may require
review against multiple source families.

## 5. Machine-trackable review dimensions

PR2-ORG requires separate review dimensions. They must not be collapsed into
one confidence score.

### 5.1 Provenance state

Minimum vocabulary:

- `provenance_complete`
- `provenance_incomplete`
- `provenance_conflicted`
- `provenance_withdrawn`

`provenance_complete` means the known influence and authorship evidence
required by the current review is recorded. It does not mean rights are clear.

### 5.2 Rights-review state

Minimum vocabulary:

- `rights_not_applicable_to_distribution_candidate`
- `rights_unreviewed`
- `rights_basis_recorded`
- `specialist_rights_review_required`
- `rights_restricted`
- `rights_prohibited`

`rights_basis_recorded` records the evidentiary basis used by the project. It
does not convert the project into a legal authority and does not create a legal
safe harbor.

A claimed license, permission, public-domain basis, open license, assignment,
commission agreement, or contributor assertion must be recorded as evidence
rather than inferred from availability.

### 5.3 Originality and similarity state

Minimum vocabulary:

- `originality_not_reviewed`
- `myravant_original_candidate`
- `similarity_review_required`
- `myravant_original_review_passed`
- `originality_review_failed`

Originality review evaluates whether the candidate is independently Myravant
rather than a superficial source transformation.

Similarity is not determined only by identical text. Review may consider
distinctive combinations, ordering, relationships, names, examples, visual or
structural presentation, selection, and other recognizable source-shaped
features relevant to the artifact.

### 5.4 Contamination and quarantine state

Minimum vocabulary:

- `contamination_clear`
- `contamination_review_required`
- `quarantined_similarity_risk`
- `quarantined_rights_risk`
- `quarantine_released`
- `withdrawn_from_distribution`

Quarantine is an offline governance state. It is not a runtime state and does
not imply deletion of evidence.

### 5.5 Eligibility disposition

Final eligibility is a downstream decision field. It must not duplicate the
rights, originality, or quarantine dimensions that justify that decision.

The bounded content-eligibility vocabulary is:

- `internal_research_only`
- `eligibility_review_required`
- `distribution_prohibited`
- `distribution_eligible_with_restrictions`
- `distribution_eligible`

These values answer what may happen to the candidate after PR2-ORG review.
They do not encode why that result was reached.

Rights bases such as licensed use, permission, assignment, open licensing, or
public-domain basis remain in `rights_review_state` and `rights_basis_refs[]`.

Originality findings remain in `originality_similarity_state`.

Similarity or rights quarantine remains in
`contamination_quarantine_state`.

`pressure_satisfied_no_content_needed` belongs to the upstream research and
requirements workflow. It is not a PR2-ORG candidate-eligibility result.

If the dedicated review dimensions conflict with the final eligibility
disposition, the record must fail closed to `eligibility_review_required` or
`distribution_prohibited` until the conflict is lawfully resolved.

### 5.6 Canon handoff state

Canon handoff is separately recorded as:

- `not_ready_for_canon_review`
- `eligible_for_separate_canon_review`

`eligible_for_separate_canon_review` means only that PR2-ORG has no remaining
eligibility blocker known within its scope.

It does not promote canon, establish gameplay doctrine, create runtime
identity, or bind the later canon owner.

## 6. Minimum eligibility record

A machine-usable eligibility record must be capable of retaining at least:

```text
eligibility_record_id
candidate_id
candidate_version
candidate_kind
provenance_state
provenance_refs[]
influence_cluster_refs[]
authorship_or_generation_modes[]
source_expression_exposure_state
rights_review_state
rights_basis_refs[]
originality_similarity_state
contamination_quarantine_state
eligibility_disposition
canon_handoff_state
review_rationale
restrictions_or_obligations[]
review_evidence_refs[]
review_decision_ref
supersedes_record_id
downstream_handoffs[]
```

This is a governance data contract, not a production schema mandate.

PR2-ORG does not decide storage technology, database layout, service topology,
or runtime representation.

## 7. Fail-closed distribution rule

A candidate may remain in internal research or authoring states when otherwise
lawfully retained, but unresolved distribution questions must fail closed.

A candidate must not become distributable merely because provenance is
inconvenient to reconstruct, source expression has been paraphrased, names or
numbers changed, AI produced a different wording, several sources were blended,
a source is common in the genre, a candidate passes gameplay or schema tests, a
source is publicly accessible, or a creator or model asserts that the material
is safe.

Where a material rights or similarity question remains unresolved, the
candidate stays review-required, quarantined, or distribution-prohibited.

## 8. Influence, exposure, and independent authoring

PR2-ORG must distinguish at least:

- research pressure derived from source-aware analysis;
- independently authored design responding to synthesized requirements;
- direct exposure to source expression;
- adaptation under a documented license or permission basis;
- public-domain-basis use;
- user-supplied or commissioned material;
- model-generated or model-transformed material;
- mixed candidates containing multiple provenance classes.

Model generation does not reset provenance.

A model output derived from source-shaped input is not presumed independent
merely because the exact wording changed.

An author assertion of originality is evidence to record. It is not by itself a
complete provenance, rights, or similarity review.

## 9. Mixed-candidate and partial-blocker rule

Eligibility is evaluated at the smallest practical artifact or component scope
that preserves meaningful review.

A mixed package must not receive a clean package-level result merely because
most components are clear.

Where a separable component is blocked, lawful outcomes include quarantine,
evidence-preserving removal, separately governed independent replacement,
distribution restriction, or specialist escalation.

A blocked component must not be hidden by aggregation.

## 10. Rights-basis outliers

PR2-ORG must support escalation for heterogeneous evidence including:

- explicit licenses;
- open-source or open-content licenses;
- public-domain claims or determinations;
- commissioned or assigned work;
- contributor or user submissions;
- third-party permissions;
- mixed-license packages;
- trademark or branding concerns;
- patent or other non-copyright concerns;
- database or dataset restrictions;
- material with uncertain authorship;
- abandoned, orphaned, or unavailable-rightsholder material;
- generated material with uncertain upstream provenance;
- factual, functional, mechanical, or procedural material whose protectability
  or permitted use cannot be safely inferred by the project.

PR2-ORG records operational state and escalation evidence.

It does not issue jurisdiction-specific legal conclusions.

## 11. Withdrawal and correction

Eligibility is revisable.

If provenance is corrected, a license is found to be narrower than recorded, a
permission is withdrawn, a similarity concern is discovered, or an influence
cluster expands materially, affected eligibility records must be re-evaluable.

A later review must supersede the earlier record rather than silently rewriting
the historical decision.

The project must be able to identify affected candidates from retained
provenance without placing that provenance into runtime.

## 12. Relationship to PR2-SRC

PR2-SRC owns exact research provenance continuity and the distinction between
source expression, observation, pressure, synthesis, requirement, and design.

PR2-ORG consumes provenance and influence evidence for eligibility review.

PR2-ORG does not re-run source research and does not redefine source
observations or normalized pressures.

A PR2-SRC result such as `research_only`, quarantine, or rights-blocked
pressure may inform PR2-ORG, but semantic or research status never substitutes
for an eligibility review.

## 13. Relationship to PR2-IR

PR2-IR will own the explicit representation and information-flow barrier
between source-aware analysis and Myravant-facing design.

PR2-ORG may require evidence that a candidate's authoring path and source
exposure are reviewable.

PR2-ORG must not pre-implement the PR2-IR barrier, define the final IR schemas,
or decide what exact source fields a Myravant-facing authoring context may
receive.

Once PR2-IR exists, its compliance evidence may become an input to originality
review.

## 14. Relationship to PR2-CORPUS

PR2-CORPUS will own the 1,000+ source registry, source batching, coverage,
genealogy, novelty, saturation, and bias controls.

PR2-ORG does not turn the corpus registry into an eligibility database and does
not make source frequency an originality or rights signal.

PR2-CORPUS may later reference PR2-ORG states to prevent blocked material from
entering downstream design or distribution workflows.

## 15. Relationship to canon and runtime

The existing conversion/runtime origin firewall remains authoritative.

PR2-ORG determines whether an offline candidate has an eligibility blocker.

It does not create canonical identity, perform canon promotion, sanitize
runtime payloads, or authorize runtime packaging.

Pre-canon provenance and eligibility evidence remain outside runtime.

Canon promotion must still satisfy its own doctrine, conflict, identity,
schema, and runtime-firewall requirements.

## 16. Relationship to AFQR-15

AFQR-15 governs modeled institutions, governance, jurisdiction, rights, law,
policy, adjudication, legitimacy, and enforcement inside the Myravant
architecture.

PR2-ORG does not decide fictional or simulated legal rights.

AFQR-15 does not decide external-source copyright, licensing, originality,
similarity, or Myravant distribution eligibility.

The word `rights` is therefore explicitly qualified by owner and context.

## 17. Corpus-scale pressures and outliers

PR2-ORG must survive thousands of sources and large numbers of independently
authored candidates without requiring manual folklore or hidden reviewer
memory.

At corpus scale:

- provenance references must remain machine-addressable;
- eligibility state must be queryable independently of semantic disposition;
- one source must not imply one candidate;
- one candidate may have many influence records;
- one requirement may be supported by many sources without carrying source
  expression into design;
- repeated source patterns must not become presumed public property;
- a later correction must support impact analysis;
- quarantine must be reversible and evidence-preserving;
- absence of a source match must not be treated as proof of originality.

Outliers that cannot be resolved by this contract must escalate rather than
forcing a false eligibility state.

## 18. Explicit nonauthority

PR2-ORG does not authorize source acquisition, source reconnaissance or
research-packet execution, bulk corpus processing, autonomous agent research,
legacy source/conversion remediation, source-to-Myravant transformation,
Myravant-native content production, PR2-IR implementation, PR2-CORPUS
execution, PR2-FICT or PR2-SIMEX execution, canon promotion, runtime or schema
implementation, R3 execution, model training, live-play or GM behavior,
deletion of provenance to obtain a cleaner eligibility result, or
legal-safe-harbor claims.

## 19. Completion and handoff

PR2-ORG is complete only when:

1. provenance-for-eligibility remains distinct from source research provenance ownership;
2. rights-review, originality/similarity, contamination/quarantine, and eligibility states are explicit and machine-trackable;
3. transformation operations are explicitly rejected as automatic proof of originality;
4. mixed candidates and unresolved rights/similarity cases have lawful fail-closed outcomes;
5. eligibility remains distinct from semantic mapping and canon;
6. AFQR-15 and runtime-firewall ownership remain intact;
7. downstream PR2-CORPUS and PR2-IR can consume ORG decisions without inheriting ORG authority.

This activation does not pre-claim PR2-ORG as complete or merged.

Any missing framework discovered during validation must be escalated rather than
filled with decorative policy language.
