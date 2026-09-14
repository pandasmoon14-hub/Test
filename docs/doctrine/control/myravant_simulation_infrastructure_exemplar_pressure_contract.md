# Myravant Simulation and Infrastructure Exemplar-Pressure Contract — PR2-SIMEX

```yaml
artifact_id: PR2-SIMEX-SIMULATION-INFRASTRUCTURE-EXEMPLAR-PRESSURE-001
status: active_control_doctrine
layer: 0_control
workstream: PR2-SIMEX
authority_reference: owner_directive_2026-09-13_pr2_simex_activation
authority_effect: architecture_pressure_governance_only
starting_baseline: 302732db03175726de2cdd7c24e78eb257520083
inherits:
  - PR2-SRC-A-SOURCE-RESEARCH-ARCHITECTURE-001
  - PR2-SRC-B-RESEARCH-METHOD-QUALIFICATION-001
  - PR2-CORPUS-SCALE-COVERAGE-GOVERNANCE-001
  - PR2-IR-SOURCE-DESIGN-INFORMATION-BARRIER-001
source_acquisition_authority: none
source_processing_authority: none
research_method_authority: none
corpus_selection_authority: none
originality_or_rights_authority: none
information_barrier_authority: none
runtime_architecture_decision_authority: none
runtime_implementation_authority: none
production_schema_authority: none
native_content_authoring_authority: none
canon_authority: none
model_training_authority: none
live_play_authority: none
```

## 1. Purpose

PR2-SIMEX defines how simulation, infrastructure, software, operations, and
related technical exemplars may contribute bounded architecture pressure to
Myravant without becoming mandatory Myravant technologies, implementation
blueprints, runtime doctrine, or hidden architecture defaults.

The workstream exists because technical exemplars create a distinct failure
mode. A real system may demonstrate that some property is achievable, expose a
failure mode, or reveal a tradeoff while still being a poor or irrelevant
implementation choice for Myravant.

PR2-SIMEX therefore governs the interpretation bridge:

```text
lawfully researched exemplar evidence
-> context-qualified technical observation
-> mechanism/property separation
-> normalized architecture pressure or evaluation need
-> existing PR2-IR handoff
-> separately authorized Myravant runtime-architecture decision
```

Every arrow is a boundary.

This contract does not select the project runtime architecture and does not
authorize exemplar research execution.

## 2. What PR2-SIMEX owns

PR2-SIMEX owns only simulation/infrastructure-exemplar-specific interpretation:

- qualification of what makes a research unit relevant as a technical exemplar;
- interpretation of implementation, operational, benchmark, failure,
  maintenance, and evolution evidence after lawful PR2-SRC research;
- preservation of the context needed to understand whether a demonstrated
  property is portable;
- separation of observed property from the mechanism used by the exemplar;
- normalization of technical evidence into architecture pressure;
- interpretation of scale claims without context-free extrapolation;
- interpretation of benchmark and performance evidence;
- interpretation of failure and incident evidence;
- identification of architecture tradeoffs and counterpressures;
- formation of source-independent evaluation-scenario candidates;
- rejection of invalid technology-prescription inferences;
- routing of lawful pressures toward the existing PR2-IR handoff and later
  authorized runtime-architecture owners.

PR2-SIMEX may define what a lawful exemplar interpretation record must preserve.

It may not execute the underlying research or make the downstream design
decision.

## 3. What PR2-SIMEX must not own

PR2-SIMEX must not own or complete:

- source acquisition, licensing, downloading, scraping, or access decisions;
- source reconnaissance, scouting, focused analysis, deep analysis, or
  research-packet execution (`PR2-SRC`);
- corpus registration, actual portfolio selection, batching, genealogy,
  effective-independence accounting, novelty, saturation, or bias governance
  (`PR2-CORPUS`);
- originality, rights, similarity, contamination, quarantine, or distribution
  eligibility (`PR2-ORG`);
- source-analysis / Myravant-design information-barrier policy (`PR2-IR`);
- fiction/LitRPG interpretation (`PR2-FICT`);
- PR2-SCALE runtime-scalability doctrine;
- PR2-PART partitioning doctrine;
- PR2-CONC concurrency doctrine;
- PR2-FID relevance/fidelity doctrine;
- PR2-EVENT command/event/message/projection doctrine;
- PR2-PERSIST persistence/replay/recovery doctrine;
- PR2-BP performance-budget/backpressure doctrine;
- gameplay doctrine;
- native-content authoring;
- canon promotion;
- runtime implementation;
- production schemas;
- database, message-bus, cloud-provider, orchestration, language, framework, or
  library selection;
- model training;
- conversion execution;
- live-play or GM behavior.

If a technical interpretation would require one of these authorities, the
lawful result is handoff or escalation.

## 4. Relationship to PR2-SRC

PR2-SRC owns research method and evidence discipline.

PR2-SIMEX does not create a competing research method.

SRC-B already distinguishes evidence such as observed implementation, documented
design intent, observed use, empirical finding, failure or incident evidence,
community report or hypothesis, inferred rationale, and historical evolution.

PR2-SIMEX consumes those attributable observations and asks the narrower
question:

> What architecture pressure, tradeoff, boundary, or evaluation need can this
> evidence lawfully support without converting the exemplar implementation into
> a Myravant prescription?

A missing research fact must remain missing.

PR2-SIMEX must not fill research gaps with architecture intuition merely because
the exemplar looks familiar.

## 5. Relationship to PR2-CORPUS

PR2-CORPUS governs the research portfolio.

PR2-SIMEX defines exemplar **qualification and interpretation criteria**. It does
not decide which named sources enter the corpus, when they are researched, how
deeply they are researched, or whether a coverage cell is saturated.

A lawful SIMEX candidate should have a bounded reason for inclusion such as:

- a materially different scale regime;
- a materially different topology;
- a materially different workload shape;
- a materially different fidelity strategy;
- unusual failure or recovery evidence;
- unusual persistence or reconstruction pressure;
- unusual scheduling or concurrency pressure;
- unusual authority-partition pressure;
- unusual hotspot or overload behavior;
- unusually rich maintenance/evolution evidence;
- a counterexample to an existing assumption;
- an outlier that exposes a missing pressure.

Fame, market share, source size, community enthusiasm, technical fashion, or
ease of access are not sufficient exemplar qualifications by themselves.

A small exemplar portfolio must preserve diversity of evidence and leave room
for outliers. It must not become a popularity-ranked technology list.

## 6. Relationship to PR2-ORG and PR2-IR

PR2-SIMEX does not weaken originality, provenance, or information-barrier
governance.

Technical evidence may contain source-specific architecture names, diagrams,
APIs, code, configuration, benchmarks, deployment layouts, operational details,
or other source-shaped material in the lawful research plane.

That does not make those details ordinary Myravant design input.

The normal downstream route remains:

```text
SIMEX interpretation
-> normalized pressure / evaluation need
-> PR2-IR handoff governance
-> separately authorized Myravant architecture work
```

PR2-SIMEX does not redefine the PR2-IR handoff payload.

No SIMEX rule can waive PR2-ORG review where PR2-ORG review is otherwise
required.

## 7. Central anti-prescription laws

### 7.1 Exemplar implementation is evidence, not prescription

A source's implementation is not a Myravant implementation decision.

Observed use of a technology, topology, pattern, framework, data model, protocol,
or operational practice does not make that mechanism a Myravant default.

### 7.2 Observed success is conditional evidence, not universal best practice

A successful system demonstrates success under some combination of workload,
scale, data, hardware, topology, organizational, operational, historical, and
product constraints.

Those conditions matter.

Success does not prove that the same mechanism is optimal outside that envelope.

### 7.3 Observed failure is a bounded pressure, not a universal prohibition

A failure or incident may demonstrate a failure mode, missing control, dangerous
interaction, or operational cost.

It does not prove that every system sharing one superficial feature will fail.

### 7.4 Mechanism is not requirement

A mechanism may be one way to satisfy a property.

The property or constraint must be stated independently whenever the evidence
supports that abstraction.

For example, evidence involving a particular partitioning mechanism may support
pressure around authority boundaries, migration, hotspots, or recovery. It does
not thereby require that partitioning mechanism.

### 7.5 Scale does not transfer without context

A scale claim is not portable merely because it contains a large number.

Observed capacity must remain tied to what was simulated or processed, what
interactions were permitted, what fidelity was retained, what hardware and
topology were used, what consistency guarantees applied, and what was omitted.

### 7.6 Benchmark performance is not world-simulation proof

A benchmark proves only what the benchmark actually measures under its recorded
conditions.

Throughput in a stateless benchmark does not prove persistent-world throughput.

Entity count does not prove interactive-agent count.

Batch simulation throughput does not prove low-latency player-facing behavior.

### 7.7 Physical topology does not define semantic authority

A source may colocate or distribute computation for implementation reasons.

That fact does not transfer semantic ownership to a process, worker, shard,
machine, service, region, or database.

Myravant's existing invariant remains controlling:

> Logical simulation semantics must remain independent of physical execution topology.

### 7.8 Technology popularity is not architecture authority

Frequent use of a technology may justify research attention.

It does not vote that technology into Myravant architecture.

### 7.9 Copying a stack does not reproduce its results

Observed performance, reliability, maintainability, scale, or failure behavior
is normally produced by interacting choices and operating conditions.

Copying one named technology or architecture pattern does not establish the same
result.

### 7.10 Missing implementation detail remains unknown

A public description may omit critical constraints, custom infrastructure,
operational process, human intervention, cost, failure frequency, security
controls, or proprietary components.

Narrative completeness must not be inferred from documentation availability.

### 7.11 Exemplar pressure remains falsifiable

A normalized pressure should state what later evidence could weaken, qualify,
contradict, or bound it.

Technical prestige is not a substitute for falsifiability.

## 8. Required context envelope

A material SIMEX interpretation must preserve enough context to prevent a
source-local implementation result from becoming a context-free architecture
claim.

Where relevant and available from lawful upstream research, preserve:

```text
simex_pressure_id
source_observation_refs[]
research_question
evidence_mode_refs[]
demonstrated_property
observed_mechanism
mechanism_scope
workload_context
scale_context
topology_context
state_and_consistency_context
latency_or_time_context
resource_budget_context
failure_and_recovery_context
operational_context
maintenance_and_evolution_context
observed_tradeoffs[]
portability_assumptions[]
nonportable_assumptions[]
counterevidence_refs[]
material_uncertainties[]
pressure_statement
pressure_class
acceptance_or_falsification_conditions[]
outlier_state
routing_state
```

This is a governance contract, not a production schema.

Fields may be omitted when genuinely inapplicable or unavailable. Missing
material context must remain visible as uncertainty rather than being invented.

## 9. Property/mechanism separation

Interpretation should distinguish at least:

1. **demonstrated property** — what behavior or result the evidence supports;
2. **observed mechanism** — how the exemplar appears to achieve it;
3. **operating envelope** — conditions under which the result was observed;
4. **tradeoffs and costs** — what the mechanism gives up, complicates, or moves
   elsewhere;
5. **normalized pressure** — what Myravant may need to account for independent of
   the source mechanism;
6. **evaluation need** — how a later Myravant design could be tested without
   reproducing the source architecture.

A lawful record may conclude that mechanism and property cannot yet be
separated. The correct result is then uncertainty, deeper research, or
escalation—not a disguised prescription.

## 10. Scale-claim discipline

SIMEX must preserve distinctions among:

- directly observed scale;
- benchmarked scale;
- production-reported scale;
- design-target scale;
- extrapolated scale;
- theoretical limit;
- architecture ceiling;
- unknown ceiling.

These must not be collapsed.

Where a scale claim materially informs pressure, the interpretation should
preserve the relevant denominator and workload shape.

Examples of materially different claims include:

- one million simple state updates;
- one million dormant records;
- one million independently deciding agents;
- one million spatially interacting bodies;
- one million concurrent network sessions;
- one million scheduled jobs;
- one million events processed offline.

The shared number does not make the workloads equivalent.

## 11. Topology and distribution discipline

Simulation/infrastructure evidence often overexposes physical topology.

PR2-SIMEX may extract pressure concerning:

- authority boundaries;
- partitionability;
- migration;
- locality;
- coordination;
- conflict;
- ordering;
- communication cost;
- failure domains;
- replication;
- reconstruction;
- hotspots;
- backpressure;
- degraded operation.

It must not decide how Myravant implements those concerns.

Statements such as these are invalid SIMEX conclusions:

- "Myravant should use microservices because the exemplar uses microservices."
- "Myravant should use an ECS because the exemplar uses an ECS."
- "Myravant should use event sourcing because the exemplar uses event sourcing."
- "Myravant should shard by geography because the exemplar shards by geography."
- "Myravant should use the same database because the exemplar scales with it."

The lawful output is the independently stated pressure, tradeoff, or evaluation
need supported by the evidence.

## 12. Concurrency and scheduling discipline

An exemplar may demonstrate worker parallelism, actor scheduling, job systems,
lockstep execution, optimistic execution, queues, work stealing, batching, or
another scheduling mechanism.

PR2-SIMEX may preserve evidence about:

- ordering sensitivity;
- determinism;
- race or conflict behavior;
- synchronization cost;
- starvation;
- fairness;
- work granularity;
- dependency structure;
- rollback or retry behavior;
- overload response;
- utilization;
- latency.

It must not decide PR2-CONC doctrine or select a scheduler.

Worker timing, thread timing, or message arrival must not silently become
Myravant truth merely because an exemplar relies on it.

## 13. Fidelity and relevance discipline

An exemplar may aggregate, cull, sleep, approximate, stream, summarize, or
otherwise vary simulation fidelity.

PR2-SIMEX may extract pressure concerning:

- what state survives fidelity changes;
- which interactions require high detail;
- when approximation becomes visible;
- whether aggregate and detailed states remain compatible;
- reconstitution behavior;
- background progression;
- error bounds;
- hotspot escalation;
- memory and compute budgets.

It must not decide PR2-FID doctrine or copy an exemplar's level-of-detail model.

## 14. Persistence and reconstruction discipline

An exemplar may use snapshots, logs, event histories, checkpoints, replication,
recomputation, append-only records, mutable state, external storage, or mixtures
of these.

PR2-SIMEX may extract pressure around:

- reconstruction;
- recovery;
- auditability;
- replay;
- durability;
- corruption boundaries;
- historical applicability;
- migration;
- partial failure;
- recovery time;
- storage growth;
- operational complexity.

It must not decide PR2-PERSIST doctrine, storage technology, or production data
model.

## 15. Overload and backpressure discipline

Systems often look correct only below saturation.

SIMEX interpretation should preserve evidence about behavior when demand exceeds
capacity, including:

- queue growth;
- latency growth;
- dropped or deferred work;
- degraded fidelity;
- prioritization;
- fairness;
- admission control;
- failure propagation;
- resource exhaustion;
- recovery after overload;
- hotspot migration.

A high average throughput result that omits overload behavior is not sufficient
evidence that overload is safely handled.

PR2-SIMEX does not decide PR2-BP doctrine.

## 16. Failure and incident evidence

Failure-heavy evidence is first-class SIMEX input when lawfully researched.

Interpretation should distinguish:

```text
trigger
-> local failure
-> propagation path
-> user/world-visible consequence
-> detection
-> containment
-> recovery
-> correction
-> long-term architectural or operational response
```

A postmortem may reveal more architecture pressure than a success case.

Failure evidence must retain enough context to avoid converting one incident
into a universal ban.

## 17. Maintainability and evolution evidence

Runtime architecture is not only peak performance.

SIMEX may extract pressure from:

- upgrade difficulty;
- schema or protocol evolution;
- operational burden;
- debugging difficulty;
- observability;
- deployment coupling;
- testability;
- rollback;
- migration;
- component replacement;
- dependency churn;
- long-term staffing or expertise burden;
- accumulated compatibility cost.

A technically fast architecture may still expose severe evolution pressure.

A maintainable architecture in one organization may still depend on
organization-specific process or expertise that does not transfer.

## 18. Positive, negative, and boundary evidence

SIMEX must support all of these evidence outcomes:

- **positive demonstration** — a property is achievable under recorded
  conditions;
- **negative/failure demonstration** — a failure mode or cost was observed;
- **boundary evidence** — the approach works only inside a recorded envelope;
- **counterexample** — evidence contradicts or weakens a common assumption;
- **incomparability** — the workload or constraints are too different for the
  intended inference;
- **uncertainty** — evidence is incomplete or ambiguous.

Not every exemplar must produce a positive architecture pressure.

A lawful conclusion may be that no portable Myravant pressure was established.

## 19. Architecture-pressure families

Where supported by evidence, normalized pressures may concern:

- topology independence;
- authority partitioning;
- deterministic ordering or commitment;
- state ownership;
- persistence and reconstruction;
- event identity and delivery;
- relevance, fidelity, aggregation, and reconstitution;
- scheduling and independent computation;
- workload granularity;
- locality and communication cost;
- hotspot behavior;
- overload and backpressure;
- failure isolation;
- degraded operation;
- observability;
- recovery;
- migration;
- resource budgets;
- latency and responsiveness;
- long-horizon maintainability;
- version and compatibility evolution;
- external dependency risk;
- reference-runtime equivalence;
- testability and falsifiability.

This list is a pressure taxonomy, not a list of required Myravant subsystems.

A pressure may route to an existing owner, remain a research uncertainty, or be
escalated when no lawful owner exists.

## 20. Evaluation-scenario candidates

A source-independent SIMEX evaluation candidate may preserve:

```text
evaluation_scenario_candidate_id
pressure_refs[]
architecture_property_under_test
workload_envelope
scale_envelope
topology_variants[]
failure_or_overload_conditions[]
state_and_consistency_conditions[]
time_or_latency_conditions[]
observable_success_conditions[]
observable_failure_conditions[]
equivalence_conditions[]
measurement_dimensions[]
preserved_uncertainties[]
design_dependency_refs[]
handoff_state
```

An evaluation candidate is not:

- a copied benchmark suite;
- a reproduced source workload by default;
- a mandate to use the source technology;
- a runtime implementation;
- an accepted PR2-SCALE design;
- proof that Myravant can already meet the target.

Its purpose is to preserve a testable architecture demand independently of the
source mechanism.

## 21. Lawful SIMEX outputs

Substantive SIMEX outputs are limited to:

- `architecture_pressure`;
- `evaluation_scenario_candidate`;
- `counterpressure_or_tradeoff`.

Failure, scale, topology, scheduling, persistence, fidelity, overload,
maintenance, and similar findings qualify an `architecture_pressure`; they do
not create independent downstream authority classes.

The following are governance dispositions rather than new architecture classes:

- `uncertainty_requires_more_research`;
- `handoff_to_existing_owner`;
- `escalated_missing_doctrine`;
- `rejected_invalid_inference`.

SIMEX outputs are research outcomes.

They are not Myravant runtime decisions.

## 22. Invalid inference patterns

The following inferences are invalid unless separately supported by lawful
Myravant architecture authority:

```text
source uses technology X
-> Myravant should use technology X

source reaches scale N
-> Myravant can reach scale N

source succeeds with topology T
-> topology T is the Myravant default

source failed with mechanism M
-> mechanism M is universally prohibited

several exemplars use pattern P
-> pattern P is Myravant doctrine

benchmark B is fast
-> Myravant world simulation will be fast

source omits failure mode F
-> F does not need handling

source architecture is mature
-> copying its components reproduces its operational result
```

If the only available conclusion has one of these forms, the correct SIMEX
disposition is rejection, uncertainty, or escalation.

## 23. Cross-exemplar synthesis

Cross-exemplar convergence may strengthen confidence that a pressure is worth
investigating.

It does not turn a shared implementation mechanism into Myravant doctrine.

Synthesis should preserve:

- effective independence and genealogy;
- different workload regimes;
- different topology regimes;
- different scale regimes;
- conflicting evidence;
- failure-heavy evidence;
- outliers;
- nonportable assumptions;
- negative results.

A cluster of related implementations must not masquerade as independent
architecture consensus.

PR2-CORPUS remains the owner of genealogy and effective-independence accounting.

## 24. Corpus-scale pressure breadth

A robust simulation/infrastructure exemplar program may eventually need pressure
from materially different families such as:

- single-process deep simulations;
- multiplayer authoritative simulations;
- large-agent social or economic simulations;
- ecology and world-process simulations;
- spatial streaming systems;
- persistent virtual economies;
- transaction-heavy systems;
- event/message systems;
- schedulers and job systems;
- HPC and scientific simulation;
- fault-tolerant infrastructure;
- database and storage systems;
- distributed coordination systems;
- offline/batch systems;
- real-time interactive systems;
- relevance/fidelity systems;
- infrastructure with strong incident/postmortem evidence;
- long-lived systems with major migration and compatibility histories.

No family is automatically required, privileged, or sufficient.

The list describes pressure breadth, not an exemplar quota.

## 25. Outliers and hard cases

SIMEX must preserve rather than flatten hard cases such as:

- highly specialized hardware;
- proprietary systems with incomplete public evidence;
- approximate or probabilistic simulation;
- eventually consistent infrastructure;
- deterministic lockstep systems;
- offline simulations with enormous scale but weak interactivity;
- tiny-scale systems with extreme interaction depth;
- centralized systems that outperform distributed alternatives;
- distributed systems whose primary value is organizational rather than
  computational;
- systems whose performance depends on custom operational practice;
- systems whose public architecture changed substantially over time;
- systems whose benchmark and production behavior diverge;
- failure evidence that contradicts published architecture claims.

Outliers do not automatically create Myravant requirements.

They must have a lawful landing, quarantine, or escalation route.

## 26. Escalation rules

Escalate rather than invent architecture when:

- property and mechanism cannot be separated from available evidence;
- a scale inference requires unsupported extrapolation;
- source evidence materially conflicts and no lawful synthesis exists;
- a pressure appears to contradict existing Myravant doctrine;
- a requested interpretation would require PR2-SCALE or another downstream
  owner to make a design decision;
- evidence is too source-shaped to cross the PR2-IR barrier;
- missing research context would have to be fabricated;
- a new pressure family has no lawful owner;
- rights or originality questions block lawful handling;
- a proposed evaluation candidate is actually a copied benchmark or source
  workload.

Escalation is a successful governance outcome when the alternative would be
false certainty.

## 27. Downstream handoff

PR2-SIMEX ends before Myravant runtime architecture begins.

Its lawful downstream output is a bounded, source-independent architecture
pressure or evaluation need suitable for the existing PR2-IR handoff and later
authorized runtime-architecture work.

PR2-SCALE remains a separate workstream and separate authority boundary.

PR2-SIMEX does not activate PR2-SCALE.

PR2-SIMEX does not authorize PR2-PART, PR2-CONC, PR2-FID, PR2-EVENT,
PR2-PERSIST, PR2-BP, PR2-AUDIT, R3 execution, runtime implementation, corpus
execution, model training, native-content authoring, canon, conversion, or live
play.

## 28. Completion condition

PR2-SIMEX is complete when the project can machine-test that:

1. exemplar qualification is distinct from corpus portfolio selection;
2. research method remains owned by PR2-SRC;
3. observed properties remain distinguishable from source mechanisms;
4. scale and benchmark claims cannot lose their material context;
5. physical topology cannot silently become semantic authority;
6. successful exemplars do not become mandatory technologies;
7. failure evidence does not become universal prohibition without support;
8. lawful outputs are architecture pressures, evaluation candidates, or
   counterpressures/tradeoffs;
9. governance dispositions remain distinct from architecture outputs;
10. PR2-IR remains the source-to-design handoff owner;
11. PR2-SCALE remains a separate, unactivated architecture owner;
12. R3 and all execution authorities remain unchanged.

Completion of this contract does not mean any exemplar has been researched,
Myravant's runtime architecture has been selected, or any runtime implementation
has begun.
