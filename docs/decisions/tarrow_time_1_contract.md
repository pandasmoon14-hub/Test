# PLAY-TARROW-TIME-1

Source: https://github.com/pandasmoon14-hub/Test/issues/546

## Owner approval — 2026-10-18

Cam directed “Please proceed” after receiving the complete #546 contract, then directed continuation. This authorizes the bounded implementation, tests, register/tracker updates and draft PR preparation described below. Earlier pending-approval wording is historical; merge, milestone closure, NPC activation and human-play remain separate dispositions.

---

## Status, scope and authority

**Approved combined contract; implementation candidate.** Cam authorized the bounded implementation and draft PR after reviewing this contract. Merge, native canon changes and opening the human-play gate remain separate.

Baseline: merged #545, main `ffd7442103c765a1fd322cac21fea529615b99e7`, tree `9e0219a54241306cb5eca19dd9e60cac8e14e3f7`. Parent #540; locality #538; capability programs #493/#495/#508; water foundation/register #544. Headquarters excluded.

Sources: current #540/#508/#495/#544; `docs/decisions/tarrow_environment_depth_1_contract.md`; `tarrow_material_1_contract.md`; `tarrow_water_1_contract.md`; `water_domain_expansion_register.md`; current `AGENTS.md`; `persistent_world_logical_time.py`; `MyravantPlayApplication.wait`; `afqr_world_action_sensing.md`.

The existing WORLD-1 implementation supplies bounded logical position and committed one-step waits, not a universal scheduler/calendar. Current Tarrow wait advances that clock and deliberately skips the stock Groundskeeper routine. The water register lists spills/wet transfer before drying provisionally; selecting drying here is a deliberate dependency-driven work selection, not a claim it was the first listed extension. Older #495/#508 status summaries are historical leads, not evidence of current implementation.

## Player result and admitted package

A player can undertake staged cleaning and reversible assembly, contribute real steps over world time, interrupt and resume against changed circumstances, leave while declared passive environmental processes continue through committed world-time advances, return to inspect qualified physical traces, and restore during unfinished work.

One coherent package contains:
1. Explicit bounded duration and owner-routed time advancement.
2. **Two distinct continuing activities**: cleaning and reversible assembly.
3. Passive drying under contrasting, consequential exposure profiles.
4. Qualified ambient-condition observation and durable physical traces.
5. A separate evidence-based #540 closure assessment.

No arbitrary workflow engine, universal action economy, arbitrary weather generator, NPC autonomy, structural repair, erosion, fluid flow or unlimited trace/investigation capability is admitted.

## Owner and state boundaries

| Concern | Authority / responsibility |
| --- | --- |
| Logical position and causal time ordering | AFQR-04; reuse the WORLD-1 one-step logical-time procedure/receipts |
| Environmental condition, exposure and passive environmental process | AFQR-17; no transfer of environmental meaning to the clock |
| Material placement, contents, washing and connections | Existing AFQR-18 / RT-010 procedures and their material/environment handoffs |
| Actor attempt/declaration and ongoing intention | Existing action representation under AFQR-03; task record references owner-receipted steps and acquires no independent material-result authority |
| Current actor/tool/target opportunity | AFQR-19, freshly qualified for each physical step |
| Perception, observable evidence and audience | AFQR-20 and applicable existing knowledge boundaries; inspecting a trace does not grant hidden history |
| Commitment, ordering receipts and persistence | AFQR-01 and existing qualified checkpoint mechanisms; coordination acquires no domain semantics |

Approved bounded primitives: ongoing task record/lifecycle, exposure-condition/process state, environmental water accounting, deposited residue, and physical trace state/projection. Proposed routing must be checked against current owning contracts during implementation; an actual authority conflict is surfaced rather than silently assigned to the clock.

Definitions/profiles, live instances, committed events and player knowledge remain distinct. Rates, durations, abilities and initial materials below are noncanonical development facts.

## 1. Timing policy and deterministic ordering

- Keep the existing WORLD-1 scheduler identity and one-step owner transition. A separate versioned **development timing policy** binds which public operations require that transition; it is not a replacement logical-time owner.
- In the new opt-in binding, each successful physical mutation admitted by its profile and each productive work contribution occupies one logical interval. This includes admitted movement, custody/storage, supported placement, connection/separation, open/close/light and water/cleaning changes. Read-only observation/help and task bookkeeping do not advance time.
- Existing old bindings keep their original timing. No universal turn length, day/night, minutes-per-step, stamina, speed or anatomy is inferred.
- Starting/resuming/pausing/abandoning a task changes its explicit intention/lifecycle record but provides no physical contribution or free material effect. Such changes have normal receipts/durability even though no time passes.
- `wait` advances one interval. `wait N steps` / `work N steps` admit positive whole N within an explicit small bound (recommended 1..32); other amounts refuse or request clarification. Each interval is independently committed and acknowledged. No hidden unbounded catch-up or automatic extra step.
- **Interval order:** qualify the requested attempt at t; prepare the existing time transition t→t+1; evaluate declared passive transitions against the actual interval-start state and exposure; commit condition changes scheduled at the boundary for subsequent intervals; requalify the active action against resulting current state; apply its owner transition if still available; commit the combined interval and causally linked receipts before acknowledgement. Stable process/subject identity determines traversal order; shared-resource collisions use an explicit stable conflict policy, never dictionary order.
- Initial qualification failure is a mutation-free refusal: no clock advance, process firing, task progress or trace. If an initially qualified interval advances time but passive changes remove active opportunity, report an **executed interrupted/blocked interval**, preserving real time/environment consequences and recording no false work contribution. Do not label it a mutation-free refusal.
- Passive eligibility/rate uses the interval-start location and condition. A move completed at t+1 affects the next interval; it cannot retroactively expose an object for the entire preceding interval. Boundary condition changes likewise apply prospectively.
- For declared uninterrupted waits, N intervals must equal N consecutive one-step waits in authoritative outcome and semantic event order. A batched command may have a different outer request identity, but its time/process transitions cannot be skipped or reordered.
- No elapsed real time accrues while the application is closed. Leaving an area and advancing committed world time elsewhere still evaluates all admitted passive processes in this bounded locality. Reopening/restoring does not apply the same elapsed interval again.

## 2. Two real continuing activities

### A — Staged cleaning

`start cleaning <surface> using <tool>` creates a task referencing the declared surface/tool, selected wipe or scrub method, owner qualifications and objective: removable residue cleared. No cleaning occurs merely by starting.

Each productive work interval invokes the **existing qualified wipe/scrub procedure** once, preserving its declared rate, tool capacity, custody, water requirement and exact residue transfer. Progress is witnessed by actual surface/tool changes and receipts, not an unrelated percent-complete counter. No hidden automatic rinse, water replenishment, tool replacement or residue disposal.

A full/dry/missing/inaccessible tool or changed target blocks the next contribution. The player can pause, obtain/rinse/wet supplies and resume with current qualification. Such preparation uses its own admitted operations and time intervals.

### B — Reversible assembly work

`start assembling <declared arrangement>` references a profile-defined endpoint/support/fastener arrangement and its separately qualified material steps: place carried endpoint A on its declared support; place carried endpoint B; create the declared connection with an available carried fastener.

Each contribution executes at most one missing material transition through the original support/fastening owner. Already-satisfied requirements are checked from actual state; no duplicate placement, fastener allocation or invented assembled entity. Gathering, transport, tool acquisition and consent are not silently bundled.

Progress is the currently satisfied arrangement plus its contributed receipt history. If another legal action changes a prerequisite, resumption re-evaluates it; a once-completed step is not a permanent privilege. Completion means the profile's actual relationship predicates hold and required contribution/provenance is attributable.

### Shared lifecycle, proven through both

Use explicit active/paused/blocked/completed/abandoned dispositions with stable task identity, actor, declared goal/method/participants and contributed-step references. One active task per selected actor is admitted initially; another start requires explicit disposition of the existing task.

Moving out of the required work context pauses active work at that action boundary. An active task does not perform unattended work during generic waiting or player absence. Only an explicit work interval contributes. Passive drying continues independently.

Pausing preserves real progress. Abandoning terminates the intention but leaves dirt, water, placements, connections and traces where their committed transitions left them. Undoing those effects requires actual lawful actions. Repeated pause/resume/abandon/finish cannot duplicate resources or completion receipts.

Implement both exemplars before extracting shared lifecycle handling. No generalized recipe/workflow authority or NPC work manager is justified by the task abstraction.

## 3. Environmental conditions and drying

Admit explicit development exposure profiles at existing qualified local positions, with at least two observable contrasts: **aired** and **sheltered**. A paused/no-exposure state handles declared closed containment or absent drying opportunity.

Recommended demonstration rates: aired 1 water unit per 2 logical intervals; sheltered 1 per 4. Rates are profile facts, not universal weather/thermodynamic law. Accumulate exact fractional drying progress; preserve earned fractional progress when exposure changes, pause it when ineligible, and clear unused credit at zero retained water. Newly introduced moisture cannot receive retroactive drying credit.

A bounded scheduled exposure change may demonstrate dynamic ambient conditions. Its schedule, affected positions and observation qualification are explicit profile data and owner receipts. No calendar, night temperature, rainfall, free moisture production or cosmetic condition with an unexplained mechanical effect is invented.

Derive actual exposure from admitted placement chains and environment: carried cloth follows its actor; supported cloth follows its support; explicitly closed containment pauses drying. Unspecified containment/exposure combinations remain unqualified. Current player visibility is not a prerequisite for physical drying.

### Water destination and residue deposition

- Evaporated water transfers from retained liquid into a **per-position environmental water-accounting compartment** included in the authoritative digest, receipts and checkpoint binding.
- It remains part of this package's total water accounting. The compartment does not itself assert atmospheric volume, humidity, transport, condensation, recoverability or fluid-flow capability.
- Environmental water is attributed to the actual exposure position for each interval, not wherever the object is inspected later.
- Drying removes no soil. Suspended residue remains in the retained liquid as water decreases; when retained water reaches zero, remaining suspended residue becomes **deposited residue on that same object**.
- Deposited residue is a separate exact compartment. A tool's working uptake limit is not a limit that can delete dirt deposited by drying. Free pickup/removal capacity is max(0, declared working limit − adhered residue − deposited residue); a saturated/over-limit tool refuses additional cleaning until material is removed.
- Rinse and collection explicitly include compatible deposited residue through their qualified existing material handoffs. Rinsing redistributes released residue with the bath; collection respects receiver capacity. No special invisible cleanup.
- Preserve exact water and total residue across liquid, adhered, suspended, deposited and environmental accounting compartments. These are bounded package invariants with explicit declared transfers; they are not a universal law automatically governing future extraordinary creation/destruction.
- No surface spills, puddles, passive wet transfer to neighbors, vapor transport, heat/energy model, filtration or biological consequences are added here.

Use Cleaning Cloth for the first drying exemplars. Screen Cloth does not acquire absorbency merely because of its name; adding a screen moisture profile would be a separately explicit extension, not required for this package.

## 4. Physical traces and qualified observation

Admit only trace types with defined material/event causes, location/attachment and observation qualification:
- A cleaned patch or brush pattern following actual compatible cleaning.
- A disturbance/fastening mark following a specifically profiled assembly step.
- A wet/drying appearance tied to actual retained moisture and drying transitions.

Trace production must identify the actual committed cause, subject and facet. No trace appears merely because a task was named, started, refused or narrated. No arbitrary dusty-crate trace without declared material/trace prerequisites; static authored wear is not rewritten into event history.

Backend provenance may retain causal command/receipt identity and occurrence position. Player inspection returns only currently observable physical features and any separately qualified interpretation. It does not expose actor identity, exact event time, intent, private participants or the raw backend event log automatically.

Physical trace state, immutable causal event provenance, observation evidence and actor knowledge remain distinct. Trace alteration/obscuring/decay occurs only through declared transitions; drying can change the wet appearance without erasing the committed event. No general tracking skill, automatic memory/belief update, omniscient timeline or testimony system.

Prove alternate compatible methods leave meaningfully distinct qualified evidence and that unavailable lighting/access prevents observation. A prior sighting grants no permanent sensing privilege.

## 5. Profiles, client and checkpoint lifecycle

Expose one separately versioned opt-in preview extending the current material/water fixture. All old default/Tarrow/depth/material/water campaign identities and timing meanings remain unchanged. Bind timing policy, task profiles, drying rates, exposure schedules, trace rules and complete initial conditions.

Public controls must support start, inspect progress, work for a bounded duration, pause, resume, abandon, and bounded waiting, with explicit method/target preservation and actionable interruption feedback. Bare generic work/clean intent must clarify where method or target matters.

Exactly-two-step composition remains exactly two steps; a duration is the declared bounded interval sequence within one step, not permission to parse arbitrary compound instructions. Each acknowledged interval is independently durable. If a later interval/step fails, preserve earlier committed consequences and stop truthfully.

Extend the existing owner-journal approach under a **new format/versioned binding** as necessary, not a mandatory universal replacement envelope. Persist/replay: logical-time transitions, task state, work receipts, water/residue/deposit/environment stocks, drying credit and exposure history, condition changes, physical traces and causal links. Restore from the qualified root and verify the complete chronological combined state; do not trust a forged final snapshot.

Timed results must be reproducible across restart, repeated delivery under existing retry contracts, batch boundaries and different observation frequency. Technical retries cannot advance time twice; deliberately repeated player attempts remain separate requests. No model call or wall-clock read participates in authoritative advancement.

On persistence failure, all affected owners roll back staged memory together; do not acknowledge a partially saved interval. Halt further mutation after an uncertain write until validated restart. Existing format families reject incompatible new envelopes. Historical campaigns are never silently reinterpreted.

## 6. Combined acceptance matrix

1. **Both activities:** real intermediate material effects; distinct tools/methods; interruption, pause, resource preparation, changed prerequisites, resume, completion and abandonment; no resource/receipt duplication.
2. **Elapsed-time equivalence:** batched/consecutive waits; mixed work/wait; ambient changes at boundaries; different observation frequencies; restart before/at/after due events; multiple due processes and explicit resource-conflict order.
3. **Exposure:** same wet cloth under aired/sheltered/paused profiles; moved/carried/supported/contained positions; leave/wait elsewhere/return; no wall-clock advancement or duplicate catch-up.
4. **Conservation and deposits:** dirty-water cloth dries with all water accounted for and all soil retained; deposition beyond working uptake limit; saturated tool refuses new pickup; rinse/collect restores opportunity lawfully.
5. **Traces and privacy:** different qualifying methods leave distinct evidence; hidden source events do not leak actors/times; darkness/closure/reach; refusal creates no fictional event; static wear remains distinct.
6. **Cross-family journeys:** build the declared passage barrier; stage a wet Cleaning Cloth on a support; start/interfere with work; leave and advance world time elsewhere; return and inspect; dismantle/recover; restore mid-process. The visual screen and movement barrier retain their separate effects. Drying does not grant either effect automatically.
7. **Generality:** at least two configuration-only exposure/activity variations and neutral identities using the same procedures. No canned scenario completion flags or Tarrow-ID branches in shared execution.
8. **Failure depth:** initial refusal vs executed interrupted interval; per-interval persistence failure; failure after replacement; task/process/profile/trace/environment/deposit forgery; old-format rejection and complete mixed-owner replay.
9. **Test effectiveness:** isolated mutations targeting duplicate elapsed processing, deletion of residue/water, stale active opportunity, hidden trace provenance and missing replay state, with passing controls.
10. **Installed evidence:** multiple objective-checked campaigns repeated twice through the actual launcher, with intermediate restart and trace/digest joins; label authored, held-out and human evidence separately.
11. **Regression:** retained owners/old locality behavior, unchanged baseline corpus, full local suite and exact-head Linux/Windows CI. Measure new runtime and existing CI headroom before a timeout change; explain any budget increase and retain all checks.
12. **Coverage reporting:** report genuinely new executed goal×method×context outcomes and supported refusals separately from vocabulary, conditions displayed or object count.

## 7. Milestone assessment and remaining work

Produce a source-linked closure assessment against #540's seven layers and explicit admitted sufficiency, identifying implemented/verified behavior, open gaps and justified deferrals. Touching a layer is not completing it. #543/#545 did not automatically finish every physical/material capability; timed conditions/traces likewise do not promise structural deformation, repair, hydrology or complete environmental simulation.

No automatic #540 closure, NPC-routine activation, #508-B/C completion claim, or human-play gate opening. #508-B requires both merged certified activity exemplars and its own acceptance disposition; traces support #508-C but do not complete actor-scoped knowledge. Native content and NPC opportunity/consent dependencies remain separately grounded.

Update the existing water expansion register with this package's admitted coverage, verified evidence and remaining triggers. Drying support does not imply humidity/condensation/flow. Reconcile stale tracker summaries without erasing historical records.

## Requested owner disposition

Recommended: approve this bounded combined contract for implementation, tests, register/tracker updates and draft PR preparation. This includes the explicit timing policy, two real activities, AFQR-17 exposure/process state, accounting destination, deposited residue, qualified traces and separate closure assessment. Merge and any subsequent milestone/authority changes remain separate.

Meaningful alternative: deliver time-qualified drying/conditions/traces first and keep continuing work for a later package; this lowers active-lifecycle integration risk but does not meet the two-activity #508-B proof in this delivery. Avoid a generic scheduler-only package or a drying-only object script, because neither supplies the integrated player outcome.
