# Myravant — Content-Independent Coverage Discovery Pass
Date: 2026-10-12 · Baseline: `main` at `6c129cf86f2d5c5821536df8f350555ecf99b9ec` · Scope: pre-human-play parallel work while the Myravant-native content bible remains in development.

**Classification:** NONAUTHORITATIVE discovery, executable-capability inventory and package-selection evidence. **Does not create doctrine, choose native world rules, establish new semantic owners, or authorize all downstream implementation.** Preserve historical Astra code names and source IDs exactly; Myravant is the current-facing name.

## 1. Executive finding

The available non-native work is **much larger than a verb list**. Most of the project can advance in lawful, content-independent *behavioral substrates*, including player agency, identity/embodiment interfaces, causality, sensing/knowledge separation, object and resource handling, world persistence and lifecycle, NPC continuity, environmental processes, aggregate/detail transitions, shared play, validation, and presentation. What must wait are the **specific native definitions** that populate those interfaces: kinform bodies, particular world materials, physical profiles, magic/skills, cultures, factions, legal norms, canonical recipes, supernatural laws, settings, stories and economy balance.

The live installed launcher currently exposes a **bounded fixture** with looking/inspection, directional movement, object pickup/drop/custody/handoff, open/close, light/extinguish, storage/retrieval, restricted thrown displacement, waiting, and specific Groundskeeper requests/follow behavior. The executable breadth is narrower than the existing doctrine and runtime skeleton inventory. Synthetic PR #489/#491 grew testing coverage; neither made those wider goals executable.

**Central recommendation:** Execute one coherent *gameplay* vertical at a time, chosen for the number of new goal × method × world-state combinations it enables. Grow ordinary action breadth **alongside** non-action foundations essential to those actions; do not build a universal manager, universal physics/economy, premature distributed cluster, or a documentation-only program. Human-play readiness remains deferred under the owner's latest instruction, not under a made-up numeric threshold.

## 2. How to read this inventory

- **E — executable, fixture-bound:** demonstrated as a path in the live installed-client application or the verified executable domain family. It does **not** mean broadly generalized or content complete.
- **P — partial/infrastructure:** concrete implemented primitives exist, but broad player-facing composition or full target semantics is unproven.
- **S — specified / skeleton / preservation:** documented interfaces, ownership, or typed skeletons; **not evidence of game implementation**.
- **G — material gap:** capability not established in the audited installed-client path; it may have partial doctrine elsewhere.
- **N — native-dependent slice:** general interfaces/tests may proceed now, but final meaning or configuration depends on Myravant-native owner decisions.

**Work-now boundary:** **I** = safely implement a generic/fixture-bounded playable vertical now with owner review. **F** = implement only with explicitly *noncanonical fixture data* and well-scoped owner-qualified semantics. **M** = build verification, ports, instrumentation or test surfaces now, but do not pretend it adds gameplay. **D** = substantive design/runtime semantics deferred to native decisions or a separate authorization. Some cells contain multiple boundaries.

**Source strength:** Live repository source and tests support **E/P/S** claims. **G** means *not shown in the inspected public runtime and application*, not proof that no future, experimental or hidden code exists. **I/F/M/D and priorities** are proposals from this audit, not existing doctrine. In the table, “owner” denotes the current doctrinal handoff family; implementation authority must still be verified per PR.

## 3. Player, embodiment and action coverage — not merely verbs

| ID | Capability and distinct player outcomes | Current evidence/status | Work-now boundary / semantic owner |
|---|---|---|---|
| CI-01 | Open freeform **goal / method / target / instrument / manner / duration** interpretation, not a closed verb roster | P: `myravant_terminal.py` explicit grammar; `myravant_terminal_capabilities.py` precise VSM routes; compound attempts generally refused | I: AFQR-03, AFQR-19 qualification; preserve command lifecycle AFQR-02 |
| CI-02 | Player **self-inspection**, equipment/person state and visible self-facts | G at public terminal; `inspect` is bounded entity inspection | I/F: AFQR-16 embodiment, AFQR-20 sensing and AFQR-10 self-knowledge; don't invent injuries or anatomy |
| CI-03 | Posture, facing, stationary activity and stance transitions with consequences | G | I/F: AFQR-16 + AFQR-18; generic supported postures on qualified neutral embodiment only |
| CI-04 | Movement **manner** (slow, rapid, cautious, quiet, crawl, lateral) and differentiated costs/risks | E for directional movement, G for meaningful movement methods | I/F: AFQR-18 topology, AFQR-19 opportunity, AFQR-16 body and AFQR-04 timing |
| CI-05 | Multiple movement substrates: climbing, swimming, squeezing, jumping, riding, transit | G in installed fixture | F: qualify environmental support + actor substrate; D for final movement economy and kinform limits |
| CI-06 | Reach, contact, adjacency, facing, enclosure, occupancy, line-of-effect | P: location relation and fixture movement routes; no generalized reach/orientation model shown | F: AFQR-18 geometry and AFQR-19 target opportunity, AFQR-20 contact sensing |
| CI-07 | Contextual object references: articles, descriptions, pronouns, former referents, ambiguity | P: some synonyms; `it/this/him` mostly ambiguous, preserved safely | I: AFQR-03 interpretation, AFQR-10 visibility, AFQR-14 meaning; do not hallucinate referents |
| CI-08 | Multi-step attempts, planned sequences, interruption, retries, abandon/resume | P: command/transition scaffolds, narrow follow intent; compound console actions normally refused | I/F: AFQR-03 plans, AFQR-02 lifecycle, AFQR-04 schedule, AFQR-19 resolution |
| CI-09 | Personal interaction methods (touch, push, pull, lift, turn, drag, steady, stack, position) | E for custody/storage/open-close; G for broad repositioning or manipulation | F: AFQR-19, AFQR-18, qualified object affordances; control is not ownership |
| CI-10 | Throw/lob/roll/slide trajectories and arbitrary objects with lawful target constraints | E **only** for qualified fixture-bound throw/displacement | F: spatial and opportunity checks; no assumed universal ballistics |
| CI-11 | Break/dismantle/assemble/repair/repurpose/use constituent parts | G; explicit terminal destruction/activation failure classes | F for noncanonical structural components; D for actual materials, durability, recipes and injury effects |
| CI-12 | Mundane meaningful “use” and environmental improvisation (brace door, wedge, signal, cover, tie) | P for target-specific open/light; G for method-composed affordances | F: registered target affordances and lawful effects; no magic `use anything` fallback |
| CI-13 | Self-care: rest/sleep, eat/drink, carry load, discomfort, tending | E for `wait` logical time only; G for physiology/self-care state | F generic qualified activity/duration; D for metabolism, fatigue, species needs and recovery rules |
| CI-14 | Read-only agency: consult status, inventory, history, active intentions, explanation | P: `look`, `inspect`, debug receipts; broader player-readable self/status unproven | I: public projection from current owner-state only; no hidden leakage |
| CI-15 | Same goal by different physical/social/temporal means | P: various narrow routes, no broad end-to-end diversity proof | I/F: acceptance V1-04 method diversity and cross-owner tests |

## 4. World state, identity, persistence and systemic consequence

| ID | System that can progress without content bible | Current evidence/status | Work-now boundary / semantic owner |
|---|---|---|---|
| CI-16 | Stable entity identity distinct from body, location, controller and player character | P: `persistent_world_entity_location_representation.py`, kernel record IDs; full identity lifecycle not exercised in launcher | I/F: AFQR-08 vs AFQR-16/11/09; no fixed human body assumption |
| CI-17 | Governed relations: follow, carry, contain, attach, support, borrow, control, ownership separately | E for located/carry/contain and narrow follow; G for generalized relations and rights | F: AFQR-09 relation lifecycle; relation storage must not grant jurisdiction/ownership |
| CI-18 | Protagonist death/retirement/replacement with campaign continuity | S/G for launcher; persistence contract and GAS-040 pressure exist | F for generic replacement/proxy test fixtures; D for final death/kinform semantics |
| CI-19 | Bitemporal provenance: fact asserted, observed, believed, corrected and historically remembered | S/P: kernel hidden-information/claim and context skeletons; no rich playable character-memory path | I for time/provenance interfaces and audit; F actor knowledge on explicit qualified facts; AFQR-06/10/20 |
| CI-20 | Stable world geography/connected spaces/entrances, independent of presentation | E for four-place fixture and deterministic movement; G for broader map/topology systems | F: AFQR-18; neutral map/position fixture, no native geography |
| CI-21 | Logical time, ordered events, wait effects, interruption boundaries | E: `persistent_world_logical_time.py`, `world_advancement.py`; narrow WORLD1/2 composition | I/F: AFQR-04; do not impose universal tick/turn economy |
| CI-22 | Local ordinary processes: scheduled routine, change while player elsewhere | E narrow Groundskeeper-related WORLD behavior; broad lifecycle unproven | F: AFQR-04 scheduling, AFQR-12 behavior, domain-owned process; event-driven |
| CI-23 | Off-screen activity and delayed consequences across sessions | P/S: process/test/evaluation contracts, narrow WORLD behavior; not proven general | F for neutral scheduled tasks, receipts and delayed effects; no always-on NPC thinker |
| CI-24 | Environmental conditions: light, weather, sound, temperature, water, surfaces, shelter | E narrowly for fixture illumination; G for generalized environment fields | F: AFQR-17 environment and AFQR-20 signals; D for native ecology and special physics |
| CI-25 | Spatial/environmental hazards, exposure, propagation and stateful aftermath | S/G in installed world; generic hazard skeleton in `tiny_vertical_slice.py` | F for noncanonical finite hazards/effects; D for damage, injuries, disease and native scale |
| CI-26 | Material identity, components, integrity, condition, wear, repair progress | E narrow object open/lit state; G for general item material composition | F: AFQR-16 integrity, AFQR-07 conservation, asset owner; D for final material values |
| CI-27 | Quantity and resource movement: split/merge, consume/produce, loss/byproduct without duplication | P/S: `resource_consequence_math.py`, custody/storage; no general gameplay economy | F: AFQR-07 audited neutral units; D for native resource prices/supply and economies |
| CI-28 | Persistence from interruption, rollback windows, corrupted saves, schema migration | E for bounded v5 save/restore/replay and v4 upgrade; S/P for broader snapshot/recovery contract | I/M: preservation/recovery stress with existing semantics, plus version-compatibility fixtures |
| CI-29 | Provenance and consequences: attribution, intent vs event vs responsibility, no plot armor | P: receipt/state delta and narrow domain consequences; broader consequences unproven | I/F: AFQR-01 commitment, AFQR-06 evidence, AFQR-11 responsibility; D for harm rules |
| CI-30 | Aggregate ↔ detailed simulation, locality fidelity and nonduplication | S: PR2-FID/scale contracts and golden corpus; not verified as playable via terminal | M/F: test with noncanonical aggregates after real need; avoid detailed worldwide ticking |
| CI-31 | World continuity after protagonist succession, multiple simultaneous lives/generations | S/G in public runtime | F neutral successor scenarios; D real reproductive/heritage/lifespan and culture |
| CI-32 | World-scale independent operations: settlements, transport, markets, faction actions | S/G public runtime | F generic event/process substrate after concrete playable need; D native institution/economy/ecology |

## 5. NPC, social, knowledge and communication systems

| ID | Capability | Current evidence/status | Work-now boundary / semantic owner |
|---|---|---|---|
| CI-33 | NPC's persistent identity, goals, schedules, preferred responses and changing local circumstances | E narrow single Groundskeeper follow/routine; G for diverse long-lived NPC behavior | F: AFQR-08/12, not model-written state; generic test personas first |
| CI-34 | Truth ≠ what was sensed ≠ what NPC knows/believes; rumor, uncertainty, false belief | S/P: AFQR-10/20 doctrine; limited sensing and projection; broad NPC belief memory absent in launcher | F for tightly sourced test facts; preserve epistemic privacy and corrections |
| CI-35 | Communication acts: ask, inform, indicate, refuse, promise, negotiate, persuade, lie | E for exact bounded actor requests/transfer; G for general dialogue/meaning | F AFQR-14 conversation act + AFQR-11 consent; D native languages and social norms |
| CI-36 | Social consequences: reputation, trust, factions, alliances, debts, obligation distinct from relation | S: RT-007 owner spec explicitly **non-executable**, no general social state proven | F neutral, explicit relationship test cases only after ownership check; D culture/legal norms |
| CI-37 | Companion orders, delegation, negotiation, independent reaction, contested control | E for constrained follow and object requests; G for general party delegation | F AFQR-11 consent/delegation, AFQR-12 behavior, AFQR-19 opportunity |
| CI-38 | Institutional petitions, rights, office, authority and jurisdiction | G: #490 demonstrates petition misclassified as object handoff | I for correct intent classification/refusal; D for native institutions/rights/legal effects |

## 6. Game services and operational foundations that are also content-independent

| ID | System | Current evidence/status | Work-now boundary / owner caution |
|---|---|---|---|
| CI-39 | Command lifecycle, idempotency, transaction and replay integrity | E for bounded transition families; P/S for generic `command_lifecycle.py` skeleton | I/M: reuse domain transitions and prove deterministic conflict/retry and replay |
| CI-40 | Multiple actors/players, simultaneous attempts, contested shared resources and private views | S/P: kernel envelopes and V1 acceptance; no public multiplayer entrypoint proven | F/M: two-client deterministic conflict test over one neutral resource, not network stack |
| CI-41 | Authoritative world view vs public projection, hidden state, disclosure-safe explanation | E for scoped inspection, visibility checks; P/S for generic hidden-info/context scaffolds | I/M: richer derived read-only views with “unknown” states; no leaking secrets |
| CI-42 | Save portability/offline execution, restart recovery, versioned state compatibility | E for local-installed CLI and checkpoint v5; P for general long-history recovery | I/M: crash injection, upgrade, clean checkout, low-resource compatibility tests |
| CI-43 | Text narration/projection decoupled from truth, model-free/replaceable GM support | E for deterministic terminal response, P/S for model context packet shells | I/M: validate semantic parity across narrator modes; LLM never chooses committed outcome |
| CI-44 | Generated proposals, validation, provenance, quarantine and campaign-scoped admission | S: production governance contracts and kernel validators; no generator-acceptance play path shown | F/M: valid/invalid neutral generated proposal tests, no auto-canon |
| CI-45 | Versioned rules/profile and content-package compatibility without reinterpreting history | S/P: schema registry, provenance contracts, v4→v5 migration narrow | M/F: neutral version-change fixtures; don't choose new native rules |
| CI-46 | Evaluation: unprecedented actions, hidden pressure, long campaigns, replays, failure taxonomy | E: installed launcher CI (#489/#491), JSONL receipts; much wider unseen action coverage incomplete | I/M: measure semantic family/goal/method, refusals, false unsupported, goal fulfillment, replay |
| CI-47 | Performance budgets, fidelity selection, resource use, no provider cost dependency | P/S: runtime scale contract, MCTX and environment evidence; no proof of world-scale measured load | M: profile actual bottlenecks; distribution only after measurements |
| CI-48 | Interfaces: local/offline text, future clients, save transfer, accessibility and input feedback | E installed text console; S for future-client independence; no 3D dependency | I/M: structured public projection and usability while text-first; avoid speculative VR |
| CI-49 | Tool-supported source research, extraction and originality validation | P: Aether Forge/extraction utilities exist; conversion/canon admission remains separate | M: independent synthesis + provenance + negative controls; never import donor rules/canon |
| CI-50 | Campaign configuration, profile divergence, continuity and player-owned saves | E fixture campaign identity + local v5 saves; G for configurable campaigns | F/M: separate neutral campaign identities/checkpoint isolation, D actual canon profiles |

## 7. Candidate coherent vertical packages (ordered by playable leverage, NOT 50 microtasks)

| Order | Candidate package / concrete player experience | Work-now profile | Evidence needed before promotion |
|---|---|---|---|
| **1** | **EMBODIED-AGENCY-1:** see self, know current position/carrying, select and change grounded posture/facing, traverse with meaningfully different supported methods. | I/F: CI-01–08, 14, 16, 20, 41. Neutral embodiment fixture; not universal human anatomy | From public launcher, prove different postures or methods have different legal opportunity/observation results, durable receipts and save/replay |
| **2** | **LOCAL-PHYSICAL-INTERACTION-1:** player can reposition and manipulate explicit fixture objects using several distinct methods rather than only pick up/drop. | F: CI-06, 09–12, 17, 26, 29 | Different routes, legal failure, reversible/irreversible distinctions, existing storage/custody consistency, persisted world location |
| **3** | **OBSERVATION-KNOWLEDGE-1:** look/touch/listen/search one bounded situation while information available differs by sensor, location and actor knowledge. | I/F: CI-02, 07, 14, 19, 24, 34, 41 | No omniscience, unseen knowledge remains unknown, actor-specific trace, multiple methods yield different legitimate facts |
| **4** | **CONTINUING-ACTIVITY-1:** declare a duration-bearing mundane activity, interrupt, resume and return to its real bounded progress after a save. | F: CI-08, 13, 21–23, 29 | Event-driven delayed consequence, no uncommitted progress, no double completion, world-time receipt |
| **5** | **AFFORDANCE-TRANSFORMATION-1:** dismantle/alter/assemble/repair *one synthetic object* with explicit components/constraints and conserved results. | F: CI-11, 12, 25–27; D for native item profiles | Missing component/tools fail; partial state persists; byproducts neither duplicated nor invented; replay |
| **6** | **NPC-SITUATED-INTERACTION-1:** question an actor without mistaking dialogue for object handoff; distinguish request, offer, refusal, follow and voluntary agreement. | I/F: CI-33–38, existing #490/#492 | NPC can truthfully say unknown, refuses when out of reach/opportunity, retains private info, and social intent does not turn into custody automatically |
| **7** | **MULTI-ACTOR-WORLD-CONTINUITY-1:** two agents compete/coordinate for one neutral object while a separate neutral process advances off screen. | F: CI-17, 21–23, 29, 33, 37, 39–40 | deterministic interleaving, no duplicate item, no invisible conflict settlement, replay across process restart |
| **8** | **CAMPAIGN-LONGEVITY-1:** world survives character change, dormant locations and rules/profile version changes; public state stays coherent. | F/M: CI-18, 28, 30–32, 42, 45, 50 | gated identity transfer, aggregate/detail nonduplication, long-history recovery, mode/context equivalence |
| **9** | **AUTONOMOUS-PLAY-READINESS:** connect approved intent routing, bounded planning, truthful descriptions, proposal validation and replay under model-none/local/optional-cloud modes. | M/F: CI-39, 41, 43–49; do not create an LLM authority | identical committed outcomes under model-off/replaced/narration variance; invalid proposals rejected; no routine human GM |

**Selection rule:** Package 1 is a *provisional* first recommendation, not automatic authorization or an instruction to invent posture mechanics. First run a short implementation-owner/gate check; choose the smallest coherent playable implementation from 1/2/3 that introduces real world consequences. Every package includes semantics, owner/authority review, parsing and application, owner-qualified domain transitions, evidence, persistence/replay, cross-family regression and adaptive synthetic-play evaluation. If a package is blocked by a native choice, use explicit neutral fixtures or proceed to the next independent package; never invent permanent rules to bypass it.

## 8. Content-bible dependency classes and examples

- **C0 — content-free invariants:** state authority; record identity; transaction/prepared vs committed; provenance; command retries; replay; cross-platform exactness; hidden-information separation; local/offline continuity; raw-input preservation. Implement or harden based on measured need.
- **C1 — neutral fixtures sufficient:** self-observation of **recorded fields**; location; ordinary movement on explicit paths; local reach; posture for a qualified shape; container capacity if fixture supplies it; object parts; finite environmental fields; activity progress; observation limits; two actors contending for one object; simulated lifetimes independent of lore. Fixture values are **test data**, not universal rules.
- **C2 — owner-qualified interface now / native instances later:** species-dependent capability, anatomy, material failure, tool compatibility, injury and recovery, skill check resolution, travel pressure, object properties, social norm and knowledge, production process, institution or economy. Build interface/validation only as needed by a playable C1 vertical, **not as a speculative platform layer**.
- **C3 — native-decision dependent:** final kinforms and physiology; magical/metaphysical mechanisms; named materials, artifacts, recipes and economies; cultural/social/legal authorities; languages; character advancement; historical canon, geography and plot; final abilities and balance. Do not adopt donor defaults or generic human assumptions.

The distinction is **property provenance**, not an arbitrary ban on entire subsystems. A “repair” method can be modeled generically once the item has qualified components, but whether *this* artifact is repairable, what it becomes, what is lost, and who can do it remain lawfully owned facts/rules.

## 9. Cross-system acceptance matrix

For every new capability claim, score separately:

1. **Recognition:** varied freeform wording identifies a plausible action goal/method without pretending it executed.
2. **Representation:** actor, embodiment/control, target, method, manner, resources, location, time and uncertainty stay distinguishable.
3. **Opportunity:** lawful environmental, spatial, knowledge and target constraints; alternative methods remain distinct.
4. **Execution:** at least one new, player-visible *real* success and one justified failure against contrasting states, not a hard-coded refusal-only “capability”.
5. **Consequence:** receipts, attribution, conservation where applicable, reversible vs irreversible effects, dependent state and off-screen impact.
6. **Persistence:** save/restore, no duplicate effects, deterministic replay and version-compatibility guard.
7. **Information safety:** public-facing explanation grounded in visible facts; private truth stays private.
8. **Breadth:** unseen/novel goal-method variation, not a synonym pass; independent synthetic policies respond to outcomes.
9. **Deployment:** core model-free/offline operation, Linux/Windows green, no new AI subscription requirement.
10. **Ownership/originality:** existing semantic owners retain authority; test content noncanonical, external donor observations only normalized pressure.

**Evaluation baseline to extend:** PR #489 (#489 merged) and PR #491 (#491 merged) are synthetic test harnesses. PR #491 Linux evidence run [#38191227316](https://github.com/pandasmoon14-hub/Test/actions/runs/38191227316) exported 16 contexts, 288 attempted turns, 62 committed state changes and 151 failure-class results; 87 were generic unsupported. It is not a statistically representative player failure rate. The Aug-23 `04_astra_v1_acceptance_criteria_v1_2_0.md` V1-04 sets a **provisional v1** Set A benchmark of ≥500 previously unseen *representable* actions, ≥95% routed correctly, ≤3% falsely unsupported, zero fabricated mechanics, plus a separate genuine frontier Set B. **Not** current achievement or an invented immediate gate for human play.

## 10. Explicit guardrails against a new planning trap

- This discovery is **one** planning/control artifact, not 50 doctrinal or architectural workstreams. Do not convert each row into an issue by default.
- Mark `E` only with executable repository evidence. Mark a doctrinal owner `S` unless a shipped runtime route is verified. `tiny_vertical_slice.py` supplies typed domain demonstration structures; it does not prove the public campaign has full injuries, autonomous GM or general hazards.
- Keep identity ≠ embodiment, sensing ≠ knowledge, relation ≠ authority, control ≠ ownership, intent ≠ method, player command ≠ committed outcome, proposal ≠ canon, storage ≠ semantic ownership, logical time ≠ environmental processes.
- Do not create universal physics, cognition, resource ledgers, force/tick units, combat rolls, “every object works for every verb”, or generalized executor merely to appear broad.
- Prefer **affordance/capability distinctions with noncanonical test profiles** over piles of string verbs; unknown properties produce qualified failure/clarification, not guessed outcome.
- Preserve retry idempotence, interruption recovery, conditional hidden knowledge, narrative honesty and source originality across every new vertical.
- Track *player goal completion*, *meaningful method differentiation* and *world remembering*, not only command parse rates, transition counts and CI pass totals.
- Do not begin human Myravant play as a discovery substitute for known broad omissions. Owner-directed sequencing keeps the pre-human vertical-slice gate open until breadth is independently demonstrated.
- Scale only after a real measured bottleneck; no world-wide full-detail ticking, universal distributed runtime or assumed model subscriptions.
- Keep #493 as the parent breadth program, #490 as a reproducible parser overmatch, and #492 as a situational inquiry candidate. Do not silently close, implement or change ownership of these issues because this report exists.

## 11. Evidence references and confidence

**Verified live repository at baseline:**
- [Public terminal parser](../../src/astra_runtime/myravant_terminal.py), [bounded VSM routes](../../src/astra_runtime/myravant_terminal_capabilities.py), [public application](../../src/astra_runtime/myravant_play_application.py), [v14 application](../../src/astra_runtime/myravant_vsm14_application.py).
- [Runtime composition](../../src/astra_runtime/domain/persistent_world_runtime_composition.py), [entity/place relations](../../src/astra_runtime/domain/persistent_world_entity_location_representation.py), [logical time](../../src/astra_runtime/domain/persistent_world_logical_time.py), [world advancement](../../src/astra_runtime/domain/persistent_world_world_advancement.py), [follow intent](../../src/astra_runtime/domain/persistent_world_follow_intent.py), [v5 checkpoint](../../src/astra_runtime/domain/persistent_world_vsm14_checkpoint.py).
- [Command skeleton](../../src/astra_runtime/domain/command_lifecycle.py), [state-store skeleton](../../src/astra_runtime/domain/state_store.py), [hidden-info kernel skeleton](../../src/astra_runtime/kernel/hidden_information.py), [context compiler](../../src/astra_runtime/domain/context_packet_compiler.py), [tiny slice](../../src/astra_runtime/domain/tiny_vertical_slice.py).
- [AFQR-01–09 current family contract](../doctrine/consolidation/afqr_core_transaction_identity_relation.md), [AFQR-10–15 contract](../doctrine/consolidation/afqr_epistemic_agency_social_communication.md), [AFQR-16–20 contract](../doctrine/consolidation/afqr_world_action_sensing.md), [persistence/scale constraints](../doctrine/control/myravant_persistence_snapshot_replay_recovery_contract.md), [source/evaluation report](myravant_synthetic_play_discovery_2.md).
- [Current owner-directed breadth gate #493](https://github.com/pandasmoon14-hub/Test/issues/493), [#490](https://github.com/pandasmoon14-hub/Test/issues/490), [#492](https://github.com/pandasmoon14-hub/Test/issues/492).

**Attached Project Knowledge used as non-repository authority navigation / owner intent / evaluation pressure (dated Aug 23; not current implementation):**
`01_astra_current_authority_index_v1_2_0.md`,
`02_astra_open_decision_docket_v1_2_0.md` (especially D-004/006/008/009/010),
`03_astra_golden_adversarial_scenario_corpus_v1_1_0(2).md` (GAS-005, 022–040),
`04_astra_v1_acceptance_criteria_v1_2_0.md` (V1-01–17, notably V1-04, 07–10, 13, 16–17),
`05_astra_runtime_failure_evidence_contract_v1_2_0.md`,
`08_astra_live_play_trace_and_evaluation_capture_contract_v1_1_0.md`,
`09_astra_model_context_and_token_efficiency_measurement_specification_v1_1_0.md`,
`10_astra_environment_and_deployment_constraint_matrix_v1_1_0.md`.

**Audit limitation:** This is a bounded source-and-test-path discovery, **not** an exhaustive call-graph audit, live local benchmark, verified AI provider integration, or proof of absence of arbitrary internal code. Capability status should be rechecked against the latest `main` at package selection. Where code and dated attached notes differ, live repository controls runtime truth; newest explicit owner decisions control sequencing intent.
