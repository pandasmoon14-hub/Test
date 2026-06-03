# D18 README Manifest — Structural Time, Campaign Continuity, Arc, Season, and Horizon Doctrine

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18 is Astra Ascension's structural-time doctrine. It governs how campaign time becomes cumulative, felt, navigable, and directional over years of play without collapsing under continuity overload, unresolved state, pacing fatigue, seasonal false resets, power inflation, progression stagnation, source-local campaign structures, or donor campaign-procedure leakage.

D18 is not final live-play GM behavior and is not runtime implementation. It is the doctrine layer that determines how campaign continuity is captured, classified, retrieved, reconciled, aged, archived, retired, reactivated, converted, escalated, or handed off to the correct owner file.

## Architecture
D18 uses the **Structural Time Architecture**.

```text
D00-D17 generate committed deltas
  -> D18 captures structural-time relevance
  -> state receives half-life and salience classification
  -> state is stored under the correct owner file
  -> D18 determines retrieval triggers
  -> arcs organize near-term promises and payoffs
  -> seasons organize medium-term throughlines, renewal, and active-state reclassification
  -> long-horizon progression governs seasons rather than being governed by them
  -> continuity amplifies later payoff when retrieved at the correct scale
  -> stale, resolved, low-salience, or overloaded state is aged, archived, retired, or escalated
```

Core premise:

```text
continuity makes time cumulative;
arc pacing makes time felt;
seasons make time navigable;
long-horizon progression makes time directional.
```

## Pack files
```text
D18-README_manifest.md
D18-00_structural_time_campaign_continuity_arc_season_and_horizon_owner_boundaries.md
D18-01_continuity_lifecycle_state_half_life_salience_retrieval_and_reconciliation.md
D18-02_arc_promises_question_answer_economy_pacing_pressure_contrast_and_payoff_scale.md
D18-03_seasons_throughlines_seams_premise_shifts_and_seasonal_state_reclassification.md
D18-04_long_horizon_progression_campaign_phases_dimensional_rotation_power_envelope_and_transformation_spacing.md
D18-05_time_skips_state_aging_pressure_decay_retirement_archive_and_campaign_state_pruning.md
D18-06_source_local_campaign_structures_donor_structural_time_mapping_quarantine_and_escalation.md
D18-07_records_not_final_schema_and_runtime_persistence_handoff_shapes.md
D18-09_integration_checklists_ddr_register_and_acceptance_criteria.md
D18_pack_manifest.json
```

## Locked decisions
```text
Primary architecture: Structural Time Architecture.
Continuity lifecycle: capture, classify, store, retrieve, reconcile, age/archive/retire.
State half-life: permanent, durable_mutable, active_transient, ephemeral, source-local, quarantined, escalated.
Salience: critical, high, medium, low, background, hidden, source-local, quarantined.
Arc model: Arc Promise–Pressure–Payoff Model.
Season model: Season Throughline–Seam–Reclassification Model.
Long-horizon model: Trajectory–Phase–Rotation Model.
State aging model: State Aging–Pruning–Reactivation Model.
Donor structural-time handling: Functional Donor Structural-Time Mapping Ladder.
Records: lightweight, not-final-schema doctrine controls plus runtime persistence handoff notes.
```

## Research-derived guardrails
```text
Continuity is capture, storage, retrieval, and reconciliation, not storage alone.
State has different half-lives; not every remembered detail deserves equal persistence or active salience.
Continuity can be burden, but it is also payoff fuel.
Arc promises need payoff-scale budgeting so local arcs do not starve seasons or consume horizon promises.
Quiet consolidation is structural work, not filler.
Seasons require throughlines and seams; a grouped set of arcs is not automatically a season.
Seasonal reset may reclassify active state but must not launder consequences.
Long-horizon progression should govern seasons, not be driven by seasonal escalation.
Dimensional rotation is the primary defense against single-axis power inflation and stagnation.
The long middle is a known danger zone where continuity load, arc freshness, seasonal renewal, and horizon pull can fail together.
The visible symptom may be at one structural scale while the needed repair belongs to another.
Externally persisted campaigns require explicit capture and retrieval; state not captured cannot be honored, and state not retrieved cannot affect generated play.
```

## Lawful donor outcomes
Every donor campaign structure, adventure path, clock, faction turn, domain cycle, realm ladder, season, timeline, endgame, metaplot, campaign calendar, or long-horizon progression model must receive one lawful outcome: direct Astra mapping, normalized Astra structural-time mapping, source-local retained construct, quarantined construct pending later doctrine/evidence, or escalated doctrine problem.


---

# D18-00 — Structural Time, Campaign Continuity, Arc, Season, and Horizon Owner Boundaries

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Core question
How does Astra make campaign time cumulative, felt, navigable, and directional over years of play without collapsing under continuity overload, unresolved state, pacing fatigue, seasonal false resets, power inflation, progression stagnation, source-local campaign structures, or donor campaign-procedure leakage?

D18 is Astra's structural-time doctrine. It is not merely campaign pacing. It governs the organized passage of meaning through continuity, arcs, seasons, campaign phases, long-horizon progression, time skips, state pruning, and future runtime persistence handoff.

D18 repeatedly asks:

```text
What must be remembered?
What must be retrieved?
What may safely recede?
What must be resolved?
What can be archived?
What has been promised?
At what scale must that promise pay off?
Which progression axis is currently carrying growth?
Which state is active enough to burden play?
Which state is dormant but still true?
Which transition renews the campaign without laundering consequences?
```

## Why D18 exists after D00-D17
D00 establishes that the world remembers and that meaningful action commits state deltas. D04 owns advancement, breakthroughs, transformations, and discontinuous progression. D10 records world-state, law, factions, public belief, hidden truth, relationships, unresolved pressure, and information-state. D13 owns Projects and downtime interval procedure. D15 owns faction, domain, institution, claim, obligation, and relationship operation. D16 owns opposition and recurring threat construction. D17 owns economy, acquisition, ownership, reward, inventory, requisition, and value-flow.

D18 answers the campaign-scale question that none of those files should answer alone:

```text
What stays active?
What ages?
What decays?
What resolves?
What retires?
What gets archived?
What becomes a season-level arc?
What becomes campaign canon candidate material?
What becomes too small to track?
What must remain retrievable because it affects future play?
```

Without D18, every D00-D17 delta can persist forever at full priority. That creates state overload, continuity error, broken payoff, and eventual runtime collapse.

## Structural Time Architecture
D18 uses this model:

```text
D00-D17 generate committed deltas
  -> D18 captures structural-time relevance
  -> state receives half-life and salience classification
  -> state is stored under the correct owner file
  -> D18 determines retrieval triggers
  -> arcs organize near-term promises and payoffs
  -> seasons organize medium-term throughlines, renewal, and active-state reclassification
  -> long-horizon progression governs seasons rather than being governed by them
  -> continuity amplifies later payoff when retrieved at the correct scale
  -> stale, resolved, low-salience, or overloaded state is aged, archived, retired, or escalated
```

Structural time has four functions:

```text
continuity makes time cumulative;
arc pacing makes time felt;
seasons make time navigable;
long-horizon progression makes time directional.
```

D18 exists to keep those four functions aligned.

## What D18 owns
D18 owns:

```text
structural time doctrine
campaign continuity lifecycle
continuity capture / storage / retrieval / reconciliation procedure
state half-life classification
state salience classification
foreground / background continuity distinction
active / dormant / archived / retired / source-local / quarantined / escalated state classification
arc promise and payoff tracking
arc pacing pressure at campaign scale
question / answer economy at arc and season scale
contrast and breathing-room doctrine
season throughline doctrine
season seam and transition doctrine
seasonal reset without continuity laundering
seasonal false-reset / bloated-season / diminishing-season prevention
campaign phase doctrine
long-horizon progression curve governance
dimensional rotation of progression axes
payoff-scale budgeting across arc, season, and horizon
state load and continuity overload controls
recurring threat / NPC / faction / domain continuity at campaign scale
time skip and downtime season handling
world memory aging and consequence decay
pressure retirement and state pruning
continuity repair and contradiction reconciliation
consumption-rate / persistence-demand notes for future runtime handoff
campaign-scale canon-candidate flagging
source-local campaign structure handling
```

## What D18 does not own
D18 must not own:

```text
D02 resolution math
D03 resource pools, recharge, overdraw, or power economy
D04 advancement mechanics, breakthrough payloads, or transformation rules
D05 method / skill taxonomy
D06 Technique, Principle, oath, route, or domain expression
D07 harm, corruption, injury, condition, or death rules
D08 actor personhood, body/form-state, companion identity, or substrate
D09 object, relic, platform, vehicle, tool, or item-state mechanics
D10 immediate world-state records as primary owner
D11 narration and presentation
D12 scene cadence, turn procedure, action timing, or encounter cadence
D13 Project interval procedure
D14 travel/exploration/site-entry procedure
D15 faction, relationship, obligation, claim, law, and institutional operation
D16 opposition/encounter/hazard construction
D17 economy, acquisition, reward, inventory, requisition, and value-flow procedure
final live-play GM behavior
final runtime implementation
final campaign-state schema
```

D18 can age, classify, retrieve, archive, retire, reclassify, or escalate state owned by those files. It cannot rewrite their procedures.

## Donor-family pressures
D18 must survive the following donor pressures without treating any one as Astra law:

```text
D20/class-level: level-based campaign pacing, tiered play bands, milestone advancement, adventure paths, campaign chapters, escalating villains, endgame bosses.
OSR/sandbox: open-ended exploration, strict calendars, irreversible state, domain play, downtime years, faction drift, hireling aging, strongholds.
Narrative/tag: arcs, fronts, clocks, season finales, spotlight cycles, retcons, flashbacks, player-authored continuity.
Cultivation/LitRPG: realm ladders, breakthrough spacing, sect arcs, hidden masters, reincarnation, inheritance, generational scale, power creep.
Sci-fi/space: long travel spans, station evolution, fleet/domain changes, tech obsolescence, faction wars, political seasons, time jumps.
Cyberpunk: heat decay, corporate escalation, debt persistence, contact aging, reputation burn, recurring institutional pressure.
Horror/investigation: clue continuity, hidden truth, escalating dread, irreversible loss, conspiracy pressure, fatigue.
Faction/domain/kingdom: faction turns, domain seasons, war cycles, settlement growth, succession, legitimacy, tribute, territorial evolution.
Vehicle/mech/ship/platform: maintenance seasons, refit arcs, campaign-scale travel, platform upgrades, crew turnover, salvage campaigns.
```

## Core non-negotiables
```text
D18 must not treat “the world remembers” as “everything stays active forever.”
D18 must not use seasons, time skips, phase changes, or source-local closure to erase consequences.
D18 must not equate campaign phase with level, tier, realm, class rank, or donor progression band.
D18 must not make arcs mandatory railroads or seasons mandatory campaign units.
D18 must not define final runtime context-packet schemas.
D18 must preserve owner-file boundaries and lawful donor outcomes.
```


---

# D18-01 — Continuity Lifecycle, State Half-Life, Salience, Retrieval, and Reconciliation

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-01 defines how Astra decides which campaign state must be captured, how long it matters, where it is stored, when it should be retrieved, and how contradictions are repaired without tracking everything forever at full priority.

D18-01 does not define final runtime memory schemas, backend implementation, prompt packet formats, D10 world-state storage, D11 presentation, or live-play GM behavior.

## Core problem
D00 establishes that the world remembers. D18 clarifies that this cannot mean every detail remains active forever. Continuity fails when important state is never captured, when captured state is stored in the wrong owner file, when old state exists but is never retrieved, when minor state clutters active play, or when contradictions are repaired silently.

## Six-stage continuity lifecycle
D18 uses this continuity lifecycle:

```text
1. Capture
2. Classify
3. Store
4. Retrieve
5. Reconcile
6. Age / Archive / Retire
```

### 1. Capture
Capture is the decision that a campaign development is true enough to persist.

Capture should occur when a state change affects or may later affect:

```text
character identity
advancement history
breakthrough or transformation history
persistent harm, scar, condition, corruption, or recovery
relationship state
obligation, debt, favor, claim, or promise
faction standing or pressure
law, reputation, public belief, rumor, or hidden truth
world-state or site-state
domain, territory, settlement, route, or economy
object, relic, platform, vehicle, or ownership state
recurring NPC, rival, threat, or faction proxy
campaign question or arc promise
season throughline
source-local continuity
canon-candidate material
```

Usually non-captured details include incidental weather, passing crowds, uncommitted description, trivial routine color, routine minor expenses unless D17 says they matter, and travel texture unless D14/D10 converts it to state.

### 2. Classify
Captured state receives two classifications: half-life and salience.

#### State half-life
```text
permanent — defining transformations, deaths, irreversible choices, major world alterations, canon-bearing campaign facts, major route choices, completed campaign-phase milestones.
durable_mutable — relationships, reputation, faction standing, obligations, scars, long-term injuries, recurring NPCs, recurring threats, domain posture, settlement state, unresolved promises, campaign truths.
active_transient — current arc pressure, immediate complications, current travel pressure, open encounter consequences, active Projects, active legal/faction traces, temporary custody disputes.
ephemeral — safe-to-drop details unless promoted, such as incidental scenery, minor dialogue color, trivial weather, non-committed names, passing crowds, routine background details.
source_local_half_life — governed by bounded source-local procedure.
quarantined_half_life — cannot be safely classified due to missing evidence or doctrine.
escalated_half_life — exposes missing Astra doctrine or canon authority issue.
```

#### Salience
```text
critical — must be retrieved before relevant play proceeds.
high — likely to affect current arc, season, or active pressure.
medium — may affect future play and should remain searchable.
low — stored but not normally surfaced.
background — contributes to world continuity but should not clutter active play.
hidden — GM/backend-facing only; player-facing presentation controlled by D11.
source_local — bounded to a source-local procedure.
quarantined — cannot be safely surfaced or resolved yet.
```

### 3. Store
D18 does not become the campaign database. It routes captured state to the correct owner file and records structural-time relevance.

Common storage routes:

```text
D04 — breakthrough, advancement, transformation, evolution, progression milestone history.
D07 — persistent harm, scar, condition, corruption, recovery state.
D08 — actor continuity, personhood, form-state, companion/summon identity, recurring NPC substrate.
D09 — object, relic, vehicle, platform, tool, material, custody/object-state.
D10 — world-state, law, faction, relationship, hidden truth, public belief, unresolved pressure, territory, information-state.
D13 — open Projects, long tasks, downtime commitments, recovery, training, crafting, repairs.
D15 — obligations, claims, standing, institutional pressure, faction operations, domain posture.
D16 — recurring opposition continuity and threat posture.
D17 — value, custody, ownership, debt, economy, inventory, reward, requisition, salvage state.
D18 — campaign-scale classification, arc/season/horizon placement, active/dormant/archive/retire status, payoff-scale tracking.
```

### 4. Retrieve
Retrieval surfaces relevant stored state when it can affect current play, conversion, continuity review, campaign planning, or future runtime context.

Retrieval triggers:

```text
same actor appears again
same location or route is revisited
same faction, institution, or law authority becomes relevant
same object, relic, platform, or claim resurfaces
a promised payoff approaches
an arc question is being answered
a season transition occurs
a long time skip occurs
a recurring threat returns
a relationship, debt, or obligation is invoked
a source-local procedure is re-entered
canon-candidate review begins
a contradiction is detected
runtime/context-packet handoff requires relevance filtering
```

Retrieval is selective. It surfaces the relevant slice, not the entire history. Hidden-state boundaries remain protected.

### 5. Reconcile
Reconciliation resolves contradictions, stale assumptions, missing records, or state conflicts.

Reconciliation triggers include owner-file disagreement, source-local state conflicting with Astra doctrine, converted content conflicting with canon, player-facing summary omissions that later matter, time skips creating unclear aging, or state never captured but now claimed as important.

Reconciliation outcomes:

```text
confirm_old_state
confirm_new_state
merge_states
reinterpret_ambiguous_state
promote_ephemeral_to_durable
downgrade_active_to_background
mark_as_source_local
quarantine_pending_evidence
escalate_doctrine_or_canon_conflict
retire_state_with_recorded_reason
create_continuity_repair_note
```

D18 prefers lawful reconciliation over silent retcon. Retcon-like adjustments must be explicit, recorded, bounded, and must not erase meaningful player agency without authority.

### 6. Age / Archive / Retire
State activity status changes over time.

```text
active — currently relevant and should surface in near-term play.
dormant — still true and available, but not currently demanding attention.
archived — preserved for reference, removed from active play burden.
retired — resolved, decayed, transformed, closed, or no longer live.
source_local — bounded to source-local procedure.
quarantined — cannot safely resolve due to missing evidence or doctrine.
escalated — exposes missing doctrine, canon conflict, or authority problem.
```

Archiving is not deletion. Retirement is recorded closure, not forgetting.

## Foreground and background continuity
Foreground continuity is player-facing or actor-facing and likely to be noticed if broken. It includes promises, transformations, active threats, major relationships, significant objects, and key locations.

Background continuity includes world, faction, economic, legal, territorial, route, public-belief, rumor, and distant-state continuity. It creates living-world depth but should not be simulated at full detail unless owner files and runtime support it.

## Promotion and demotion
D18 supports promotion and demotion of state.

Promotion examples: minor NPC becomes recurring; background rumor becomes arc clue; discarded object becomes evidence; ephemeral detail becomes durable because players attached to it; source-local custom becomes canon-candidate.

Demotion examples: active threat becomes dormant after closure; faction claim becomes archived after season transition; unresolved question is retired after payoff; source-local subsystem closes with its converted source.

Promotion and demotion must be recorded when they affect future obligations.

## Anti-drift controls
```text
Do not treat stored state as automatically active.
Do not let retrieval depend only on memory.
Do not flatten half-life into permanent/temporary only.
Do not resolve contradictions silently.
Do not turn D18 into the state owner for every fact.
Do not expose hidden-state retrieval through player-facing narration without D11/owner-file permission.
```


---

# D18-02 — Arc Promises, Question/Answer Economy, Pacing Pressure, Contrast, and Payoff Scale

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-02 defines arc-level structural time. It explains how Astra organizes arcs so they create satisfying pressure, meaningful partial resolution, and campaign-forward movement without becoming railroads, scripted story chapters, donor adventure-path pacing, faction-clock defaults, or pure narrative advice.

D18-02 does not define D12 scene cadence, D02 resolution, D11 narration, D13 Project procedure, D15 faction operation, D16 encounter construction, or season structure.

## Arc Promise–Pressure–Payoff Model
D18 treats arcs as bounded promise containers.

```text
campaign pressure becomes arc-relevant
  -> D18 identifies the arc promise
  -> D18 classifies the central question / pressure
  -> D18 sets payoff scale
  -> D18 identifies required continuity retrieval
  -> escalation and consolidation are tracked
  -> crisis / decision / transformation point is located
  -> closure produces state deltas
  -> unresolved material is routed to season, horizon, dormant, archived, retired, source-local, quarantine, or escalation
```

An arc identifies what kind of payoff is owed. It does not dictate outcome.

## Arc Promise
Possible arc promises:

```text
resolve_a_threat
answer_a_question
expose_a_hidden_truth
survive_a_pressure
recover_from_consequence
complete_a_project
test_a_relationship
repair_or_break_standing
advance_a_faction_pressure
contest_a_claim
secure_access
escape_or_pursue
undergo_training
prepare_for_breakthrough
face_breakthrough_consequence
transform_identity
protect_or_change_a_place
recover_or_lose_value
retire_a_pressure
source_local_promise
```

An arc promising to expose a hidden truth does not require the truth to be fully revealed. It does require the hidden-truth state to move: revealed, partially revealed, misread, protected, deepened, transferred, quarantined, or escalated.

## Central Question / Pressure
Every arc should identify at least one central question or pressure.

Question examples:

```text
Can the party reach the site before the rival faction?
What is causing the settlement’s corruption?
Will the claimant’s legal case hold?
Can the unstable relic be repaired before it degrades?
What price will the breakthrough demand?
Can the faction alliance survive the betrayal?
Can the crew escape the interdiction zone?
Who owns the salvage?
Can the character integrate a transformation without identity fracture?
```

Central pressure types:

```text
threat_pressure
mystery_pressure
faction_pressure
relationship_pressure
domain_pressure
resource_pressure
time_pressure
travel_pressure
legal_pressure
identity_pressure
breakthrough_pressure
recovery_pressure
source_local_pressure
```

Question / pressure state:

```text
opened
active
complicated
partially_answered
answered
deferred_to_season
deferred_to_horizon
transformed_into_new_question
retired
archived
source_local
quarantined
escalated
```

Too few questions creates inert arcs. Too many open questions creates chaos and continuity overload.

## Payoff Scale
Every arc classifies expected payoff scale:

```text
scene_payoff
arc_payoff
season_payoff
campaign_phase_payoff
long_horizon_payoff
canon_candidate_payoff
source_local_payoff
```

Rules:

```text
An arc promise should usually pay off at arc scale.
An arc may advance a season or long-horizon payoff, but it should not defer all satisfaction upward.
A season-scale payoff should not be spent casually as a minor arc climax unless D18 records why.
A long-horizon payoff should not be consumed by arc-local pacing pressure without explicit campaign-scale decision.
A source-local payoff may satisfy a converted source without becoming Astra-wide doctrine.
A canon-candidate payoff is flagged only for later review; it is not promoted by dramatic importance.
```

This prevents payoff starvation and payoff misallocation.

## Continuity Retrieval for Arc Payoff
Before an arc payoff, D18 identifies what continuity must be retrieved.

Retrieval categories:

```text
prior promise
prior relationship
prior faction state
prior harm or scar
prior object state
prior place alteration
prior hidden truth
prior public belief
prior reward / debt / claim
prior threat
prior transformation
prior source-local fact
prior canon-candidate note
```

Retrieval priority:

```text
required_for_payoff — the payoff fails if this state is not retrieved.
useful_amplifier — the payoff is stronger if retrieved, but not dependent.
background_texture — retrieval improves coherence but should not burden the arc.
hidden_retrieval — GM/backend-facing only.
not_relevant — should not be surfaced.
```

Continuity is not only burden. It can be payoff fuel.

## Escalation and Consolidation
D18 treats arc pacing as alternating escalation and consolidation.

Escalation may include stakes increase, cost increase, new complication, stronger opposition, worse position, new information, relationship strain, resource pressure, time pressure, identity pressure, domain pressure, or source-local escalation.

Consolidation may include recovery, planning, training, research, social repair, resource gathering, downtime, travel reflection, Project progress, relationship processing, information integration, state audit, or source-local consolidation.

Continuous escalation creates fatigue. Consolidation without new pressure creates stagnation. Quiet material is not automatically filler.

## Crisis / Decision / Transformation Point
An arc should identify its structural high-pressure point:

```text
combat_crisis
social_crisis
legal_crisis
faction_crisis
mystery_reveal
resource_collapse
identity_test
breakthrough_attempt
domain_claim
platform_failure
project_deadline
escape_window
moral_decision
source_local_crisis
```

The crisis is where the arc’s central pressure must be confronted, transformed, deferred, or failed forward. It need not be combat.

## Capability–Challenge Relationship
D18 tracks how current capability relates to arc pressure:

```text
capability_below_pressure
capability_near_pressure
capability_above_old_pressure_but_below_new_pressure
capability_overmatches_pressure
pressure_requires_different_axis
pressure_requires_social_or_world_solution
pressure_requires_resource_or_project_solution
pressure_requires_source_local_solution
```

This prevents long campaigns from making all arcs feel trivial or futile.

## Arc Closure
Arc closure must classify what happened:

```text
resolved
resolved_with_cost
partially_resolved
transformed
deferred_to_season
deferred_to_horizon
opened_new_arc
retired_pressure
archived_pressure
dormant_pressure
failed_forward
quarantined
escalated
source_local_closure
```

Closure routes state to owner files: D10 world-state, D13 Project updates, D15 pressure/claim/standing updates, D16 threat continuity, D17 value/ownership/burden updates, and D18 arc/season/horizon status.

## Anti-drift controls
```text
Do not make arcs mandatory railroads.
Do not make arcs merely narrative labels.
Do not treat every pressure as an arc.
Do not defer every payoff to season or horizon.
Do not spend season/horizon payoffs casually at arc scale.
Do not treat quiet scenes as filler by default.
Do not require combat crisis.
Do not let donor adventure chapters become Astra arc doctrine.
Do not let arc pacing override owner-file procedure.
Do not let arc closure erase consequences without recorded retirement or reconciliation.
```


---

# D18-03 — Seasons, Throughlines, Seams, Premise Shifts, and Seasonal State Reclassification

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-03 defines seasons as optional medium-horizon campaign containers that create renewal, closure, transition, state pruning, premise shifts, and long-campaign navigability without becoming mandatory TV-style structure, donor adventure-path chapters, faction-turn seasons, kingdom turns, cultivation-realm arcs, or continuity laundering.

A grouped set of arcs is not automatically a season. A season is structurally real only when it has a throughline, promise, payoff scale, active-state frame, seam, and state reclassification.

## Season Throughline–Seam–Reclassification Model
```text
several arcs become medium-horizon related
  -> D18 identifies a season throughline
  -> D18 declares the season promise
  -> D18 defines active seasonal pressure
  -> D18 sets season payoff scale
  -> D18 tracks continuity retrieval needed for seasonal payoff
  -> D18 manages escalation, consolidation, and premise shift
  -> D18 executes the season seam
  -> D18 reclassifies state as active, dormant, archived, retired, source-local, quarantined, or escalated
  -> D18 carries forward only what the next phase needs active
  -> D18 preserves history without keeping all history in active burden
```

## Season Throughline
A Season Throughline is the medium-horizon question, pressure, or transformation that binds several arcs together.

```text
survival_under_pressure
territory_or_domain_stabilization
faction_entanglement
settlement_or_platform_recovery
mystery_or_hidden_truth_exposure
war_or_campaign_conflict
relationship_network_realignment
economic_or_resource_crisis
training_and_breakthrough_preparation
identity_transformation
realm_or_route_transition
institutional_ascension
exploration_of_new_region
recovery_after_catastrophe
source_local_throughline
```

A throughline is larger than one arc but smaller than the whole campaign horizon. Each included arc should advance, complicate, reframe, or resolve it.

## Season Promise and Payoff
A Season Promise defines what the season owes before it closes.

Examples:

```text
stabilize_or_lose_a_home_base
resolve_a_faction_war_phase
expose_the_true_source_of_a_crisis
prepare_for_or_fail_a_major_breakthrough
move_from_survival_to_influence
convert_a_recurring_threat_into_a_settled_state
transform_a_relationship_network
settle_a_domain_claim
escape_a_region_or_reach_a_new_one
recover_from_a_major_loss
complete_a_campaign-scale_Project_phase
source_local_promise
```

Season payoff states:

```text
season_throughline_resolved
season_throughline_resolved_with_cost
season_throughline_partially_resolved
season_throughline_transformed
season_throughline_deferred_to_horizon
season_throughline_failed_forward
season_throughline_retired
season_throughline_archived
season_throughline_split_into_new_season
season_throughline_quarantined
season_throughline_escalated
source_local_season_payoff
```

A season should generally resolve its own throughline enough to provide closure while retaining at least one continuation vector if the campaign continues.

## Seasonal Active-State Frame
A season defines what state is actively in frame:

```text
active arc questions
active faction pressures
active relationships
active domain claims
active recurring threats
active Projects
active settlement/platform conditions
active economic or resource pressures
active hidden truths
active route / region / realm pressures
active rewards / debts / obligations
active transformation or breakthrough pressures
active source-local procedures
```

It should also identify what is not active: dormant prior threats, background factions, archived locations, settled relationships, retired claims, inactive reward traces, inactive source-local subsystems, background economy changes, and older continuity useful only as callback or amplifier.

## Season Seam
A Season Seam is the transition point between seasons. It is a structural-time checkpoint, not a casual recap.

A seam includes:

```text
closure list
continuation list
carry-forward list
dormant-state list
archive list
retirement list
new premise or pressure baseline
time skip / no time skip declaration
state reclassification
owner-file updates
canon-candidate flags if any
source-local closure or continuation notes
```

Seam failure risks:

```text
too much closure -> campaign loses forward pull;
too little closure -> season feels unresolved;
too much reset -> continuity laundering;
too little reset -> no renewal;
unclear carry-forward -> state bloat;
unclear retirement -> silent reset;
unclear new premise -> diminishing season risk.
```

## Seasonal Reset Types
```text
soft_reset
active_state_reset
premise_shift
location_shift
faction_landscape_shift
resource_baseline_shift
power_envelope_review
time_skip_reset
cast_or_spotlight_shift
source_local_reset
hard_reset_explicit_authority_only
```

A reset must never silently erase consequences. A valid reset changes active configuration while established history remains true.

## Continuity Laundering Control
Continuity laundering occurs when a season boundary is used to discard inconvenient consequences.

Laundering risks:

```text
faction enemies disappear without retirement;
debts vanish because the campaign moved location;
relationships reset to neutral;
damaged settlements return to normal without recovery;
object/custody claims disappear;
public reputation resets without explanation;
recurring threat is forgotten;
source-local pressure is treated as gone without closure;
economic collapse or scarcity disappears at the seam;
breakthrough consequences vanish after a time skip.
```

Valid alternatives:

```text
retire_with_recorded_reason
archive_as_background
convert_to_dormant_pressure
resolve_through_owner_file
transform_into_new_pressure
handoff_to_D18_long_horizon
mark_source_local_closed
quarantine_if_unclear
escalate_if_doctrine_gap
```

## False, Diminishing, and Bloated Season Controls
A false reset changes surface but not structure: new city, same pressures; new villain, same function; new realm, same challenge axis.

A real season transition should show at least one meaningful shift: active pressure baseline, campaign phase, growth axis, relationship/faction structure, domain posture, resource baseline, access horizon, threat posture, transformation pressure, or source-local boundary.

A diminishing season repeats prior season structure with weaker force. A bloated season has too little throughline for too many arcs.

Diagnostics:

```text
Does each arc advance, complicate, reframe, or resolve the season throughline?
Has the season’s throughline become too thin for its length?
Is the new season only a louder version of the prior season?
Has seasonal escalation shifted dimension, or only scale?
Has the season delayed payoff past useful tension?
Are arcs locally busy but seasonally inert?
Does the season’s climax still answer the season promise?
```

Allowed remedies: shorten season, split season, merge arc, retire pressure, shift throughline, promote new pressure, downgrade to arc, archive inactive state, or escalate missing structure.

## Long-Horizon Governance
Seasons serve the long-horizon curve. They do not control it.

```text
long-horizon progression governs seasons;
seasons organize arcs;
arcs organize local pressure;
D12 organizes scene cadence;
continuity threads through all levels.
```

A season may want a larger climax, but the long-horizon curve may require consolidation, lateral growth, or premise shift instead of raw escalation.

## Anti-drift controls
```text
Do not make seasons mandatory.
Do not make seasons TV-episode structure.
Do not treat a group of arcs as a season without a throughline.
Do not use season boundaries to erase consequences.
Do not let seasonal reset launder continuity.
Do not let season escalation force raw power or cosmic stakes inflation.
Do not let every season require a bigger villain.
Do not let season transition replace owner-file resolution.
Do not treat faction turns, kingdom turns, cultivation realm arcs, or adventure-path chapters as Astra seasons by default.
Do not let source-local campaign structures become Astra-wide season doctrine.
```


---

# D18-04 — Long-Horizon Progression, Campaign Phases, Dimensional Rotation, Power Envelope, and Transformation Spacing

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-04 defines long-horizon progression governance. It sustains meaningful progression across years without collapsing into power inflation, progression stagnation, single-axis escalation, meaningless plateaus, broken endgame promises, or donor level/tier/realm pacing assumptions.

D18-04 governs campaign-scale placement and pacing, not advancement mechanics. D04 owns advancement payloads. D06 owns power expression. D03 owns resource economy. D15, D16, and D17 own their respective procedures.

## Trajectory–Phase–Rotation Model
```text
campaign has a long-horizon trajectory
  -> D18 identifies current campaign phase
  -> D18 identifies active progression axes
  -> D18 defines the current power envelope
  -> D18 distinguishes escalation from consolidation
  -> D18 spaces major transformations and discontinuous changes
  -> D18 reserves some payoffs for season, phase, or horizon scale
  -> D18 rotates progression dimensions before any single axis saturates
  -> D18 detects inflation, stagnation, dimensional collapse, and ceiling failure
  -> D18 routes actual mechanics to owner files
```

## Long-Horizon Trajectory
The Long-Horizon Trajectory is the campaign’s broad direction of becoming.

```text
survival_to_stability
local_actor_to_regional_force
wanderer_to_domain_holder
apprentice_to_master
mortal_to_ascendant
isolated_party_to_institutional_power
crew_to_platform_power
fugitive_to_legitimate_authority
ignorance_to_cosmic_understanding
broken_world_to_rebuilt_order
sect_member_to_sect_founder
scavenger_to_artificer_power
source_local_trajectory
```

Trajectory is not a railroad. It is an orienting promise and structural vector.

## Campaign Phase
Campaign phase describes current scale of play, pressure, access, and responsibility.

```text
local_survival
local_stability
regional_emergence
faction_entanglement
institutional_recognition
domain_responsibility
settlement_or_platform_stewardship
inter_realm_or_interstellar_access
mythic_or_apex_pressure
ascendant_conflict
legacy_or_succession
post_apex_transformation
source_local_phase
```

Campaign phase is not level, realm, class rank, or donor tier. It may correlate with advancement, but D04 owns advancement.

## Power Envelope
Power Envelope identifies what scale of challenge and capability is currently meaningful.

```text
below_pressure — current pressures exceed current capability.
near_pressure — capability and pressure are closely matched.
above_old_pressure — prior threats are now meaningfully surpassed.
new_axis_required — old power growth is insufficient because the challenge is of another kind.
consolidation_needed — capability expanded faster than state, identity, resources, world position, or relationships can absorb.
overinflated — raw power or stakes have exceeded emotional or procedural legibility.
source_local_envelope — bounded to a converted source’s campaign structure.
```

Astra should let characters outgrow some old threats. Progression should matter. But old threats should not always be replaced by strictly bigger versions.

## Progression Axis
D18 tracks which axis is carrying growth.

Possible axes:

```text
raw_power
skill_refinement
method_mastery
knowledge_and_truth
relationship_depth
faction_standing
institutional_authority
domain_or_territory_responsibility
resource_access
object_or_platform_capability
route_or_realm_access
identity_integration
spiritual_or_animus_depth
glamour_or_social_presence
integrity_or_self_coherence
legacy
settlement_or_world_influence
moral_complexity
cosmological_understanding
source_local_axis
```

Axis states:

```text
foreground_axis
supporting_axes
resting_axes
saturated_axes
emerging_axes
blocked_axes
source_local_axes
```

## Dimensional Rotation
Dimensional Rotation shifts which axis carries progression before any single axis saturates.

Rotation triggers:

```text
raw power gains no longer feel meaningful;
current season repeats prior season’s escalation pattern;
threat scale is inflating faster than emotional stakes;
players have mastered one type of pressure;
relationships or world consequences are underdeveloped;
domain or institution pressure has emerged;
breakthroughs have become routine;
resource access has outpaced responsibility;
old axis is saturated or blocked;
campaign middle is busy but stagnant;
source-local axis is closing or becoming unsafe to generalize.
```

Rotation outcomes include shifting to skill refinement, relationship depth, faction/domain responsibility, resource/economy pressure, hidden truth/cosmology, identity integration, platform/settlement stewardship, legacy/succession, moral complexity, recovery/consolidation, source-local rotation, quarantine, or escalation.

## Escalation and Consolidation
Escalation increases pressure, scale, risk, consequence, access, difficulty, responsibility, or transformation.

Consolidation explores, stabilizes, integrates, repairs, trains, governs, recovers, understands, or pays for what has already changed.

Consolidation modes:

```text
identity_consolidation
relationship_consolidation
domain_consolidation
resource_consolidation
training_consolidation
recovery_consolidation
faction_consolidation
settlement_or_platform_consolidation
knowledge_consolidation
post_breakthrough_integration
post_war_rebuilding
source_local_consolidation
```

Consolidation is active structural progression, not lack of progress.

## Transformation and Breakthrough Spacing
D18 governs spacing, not mechanics.

Major changes requiring spacing review:

```text
major_breakthrough
realm / tier / phase transition
identity-altering transformation
route-defining oath or principle shift
domain claim
platform acquisition or major upgrade
settlement/domain founding
faction rank change
institutional legitimacy shift
major relationship reconfiguration
recurring threat retirement
long-horizon truth reveal
legacy transition
source_local_phase_change
```

Spacing states:

```text
too_soon
well_timed
delayed_for_consolidation
reserved_for_season_payoff
reserved_for_phase_payoff
reserved_for_horizon_payoff
blocked_by_owner_file
source_local_spacing
quarantined
escalated
```

This prevents breakthroughs from becoming routine and prevents transformations from being so rare that progression feels stalled.

## Horizon Promise
D18 tracks whether the campaign has an implied horizon.

```text
undefined_open_sandbox
emerging_horizon
declared_horizon
phase_horizon
seasonal_horizon
long_horizon_apex
post_apex_continuation
source_local_horizon
quarantined_horizon
```

Broken ceiling controls:

```text
Do not promise an apex indefinitely without payoff review.
Do not continue past an apex without post-apex premise.
Do not inflate the ceiling whenever the campaign nears it unless the new ceiling has structural justification.
Do not let donor “endgame” structures become Astra horizon law.
```

## Catch-Up, Drift, and Party Spread
D18 flags spread without defining advancement mechanics.

Spread types:

```text
character_power_spread
resource_spread
faction_access_spread
knowledge_spread
spotlight_spread
domain_responsibility_spread
platform_access_spread
source_local_spread
```

Responses route to owner files: D04 advancement review, D05 competency spotlight rotation, D13 training/recovery Project, D15 access adjustment, D17 resource/reward review, D18 phase review, source-local adjustment, quarantine, or escalation.

## Long Middle Diagnostic
D18 requires review when:

```text
arcs are locally busy but seasonally inert;
players have many open threads but weak forward pull;
progression continues numerically but not structurally;
same threat function repeats with bigger scale;
season transitions feel cosmetic;
continuity load prevents new material from breathing;
major payoffs are being deferred too often;
old promises are not being retrieved;
new axes of growth are not emerging.
```

Allowed remedies:

```text
activate_dormant_continuity_as_amplifier
rotate_progression_axis
shorten_or_split_season
retire_low-salience pressure
convert_active_state_to_dormant_or_archived
shift_to_consolidation
promote_new_throughline
resolve_stale_question
schedule_phase_payoff
escalate_missing_progression_doctrine
```

## Anti-drift controls
```text
Do not tie campaign phase directly to level, tier, realm, class, or donor advancement rank.
Do not let raw power be the only progression axis.
Do not make each season bigger only because it follows the previous season.
Do not let every arc grant major advancement or transformation.
Do not treat consolidation as lack of progress.
Do not make breakthroughs routine.
Do not defer all meaningful payoff to an indefinite horizon.
Do not promise an apex without tracking how it may be approached, transformed, or retired.
Do not let donor endgame, realm ladder, adventure path, faction rank, or level-band structure become Astra law.
Do not solve stagnation by increasing stakes scale alone.
Do not solve continuity overload by discarding payoff-bearing history.
Do not let long-horizon planning override player agency, owner-file mechanics, or lawful outcomes.
```


---

# D18-05 — Time Skips, State Aging, Pressure Decay, Retirement, Archive, and Campaign State Pruning

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-05 defines how Astra advances campaign time by days, months, years, seasons, generations, travel spans, downtime periods, or phase transitions while preserving meaningful continuity, aging relevant state, retiring stale pressure, archiving history, and preventing state bloat without silently resetting consequences.

D18-05 does not define D13 downtime Project procedure, D15 faction turns, D17 economy simulation, D10 world-state records, D04 advancement mechanics, D12 cadence, or final runtime schema.

## State Aging–Pruning–Reactivation Model
```text
campaign time advances or a structural boundary occurs
  -> D18 identifies affected state
  -> owner files update their own domains
  -> state receives aging outcome
  -> active pressures are reviewed
  -> stale or resolved pressures are retired
  -> low-salience but true material is archived
  -> dormant material remains retrievable
  -> reactivation triggers are recorded
  -> unresolved or unsupported material is quarantined or escalated
```

## Time-Advance Trigger
A state-aging review occurs when campaign time meaningfully advances or campaign structure changes.

```text
end_of_arc
end_of_season
downtime_interval
downtime_season
large_time_skip
travel_span
recovery_period
training_period
project_interval_sequence
faction_operation_cycle
domain_evolution_cycle
settlement_growth_period
platform_refit_period
campaign_phase_transition
source_local_phase_transition
continuity_overload_review
runtime_context_pruning_review
canon_candidate_review
```

D18 does not require full state-aging review after every scene. D12 and D13 handle shorter cadence.

## Time-Advance Scale
```text
scene_to_scene
session_to_session
arc_interval
downtime_interval
season_interval
months
years
generation
realm_or_route_transition
interstellar_or_interrealm_span
post_catastrophe_span
source_local_span
unknown_span
```

Larger spans require stronger aging, decay, evolution, and retirement review.

## Affected-State Inventory
Before major time advances, D18 inventories state that may be affected:

```text
character_state
advancement_pressure
breakthrough_or_transformation_pressure
persistent_harm_or_recovery
relationships
obligations
debts
claims
faction_pressure
law_or_reputation
settlement_or_domain_state
route_or_region_state
object_or_platform_state
projects
resources_and_economy
recurring_threats
hidden_truths
public_beliefs
source_local_state
canon_candidate_material
```

D18 routes these to owner files rather than resolving all directly.

## Aging Outcome
State reviewed across time receives an aging outcome:

```text
unchanged
progressed
decayed
intensified
stabilized
resolved
partially_resolved
transformed
split
merged
dormant
archived
retired
lost
expired
evolved_offscreen
requires_owner_file_resolution
source_local_closed
source_local_continues
quarantined
escalated
```

## Pressure Decay
Pressure decay is the process by which unresolved pressure loses immediate force, changes form, or moves into background continuity.

May apply to rumors, minor faction hostility, legal heat, public attention, resource scarcity, travel danger, minor recurring threats, social embarrassment, market instability, settlement unease, unclaimed rewards, or source-local pressure.

Decay states:

```text
no_decay
slow_decay
ordinary_decay
rapid_decay
decay_with_trace
decay_into_background
decay_into_dormant_pressure
decay_blocked_by_owner_file
source_local_decay
```

Pressure decay is not erasure. It changes activity status or urgency. Concrete effects route to owner files.

## Pressure Intensification
Some unresolved pressures worsen over time.

May apply to unpaid debt, untreated injury, unchecked corruption, faction retaliation, legal prosecution, spreading rumor, unrepaired object/platform damage, starving settlement, unresolved war, unstable relic, depleted resource base, recurring threat preparation, or source-local countdown.

Intensification states:

```text
intensifies_naturally
intensifies_if_ignored
intensifies_by_source_local_rule
intensifies_by_faction_operation
intensifies_by_project_failure
intensifies_by_decay
intensifies_by_hidden_truth
intensifies_by_campaign_phase
blocked_pending_owner_file
quarantined
escalated
```

D18 identifies intensification, but owner files govern concrete effects.

## Retirement
Retirement is the lawful closure of a pressure, state, question, promise, or campaign element.

Retirement can occur when pressure resolved, no longer matters, was formally settled, was transformed, was made obsolete by phase change, was closed by owner file, passed beyond relevance, merged into background, or was marked inactive by continuity review.

Retirement outcomes:

```text
retired_resolved
retired_by_decay
retired_by_owner_file
retired_by_season_seam
retired_by_phase_transition
retired_to_background_history
retired_source_local
retired_as_rejected_import
retired_with_canon_candidate_note
retirement_quarantined
retirement_escalated
```

Silent retirement of meaningful state is not allowed.

## Archive
Archive preserves history without keeping it active.

Archive is used for closed arcs, resolved season pressures, old locations, former NPCs, settled claims, past faction states, completed Projects, former rewards and ownership disputes, old rumors, retired threat profiles, past campaign phase notes, source-local closed procedures, and continuity repair notes.

Archive records should preserve what happened, why it mattered, owner file, ending status, reactivation triggers, visibility boundary, and canon-candidate relevance.

Archive is not deletion.

## Reactivation
Dormant or archived state may return if triggered.

Reactivation triggers:

```text
same actor returns
same place is revisited
same faction regains relevance
old debt is invoked
old relationship is tested
old hidden truth resurfaces
old threat returns through continuity support
old object/relic is used again
season premise activates archived state
long-horizon payoff requires callback
source-local procedure reopens
canon review requires prior evidence
```

Reactivation outcomes:

```text
reactivated_as_active
reactivated_as_background
reactivated_as_arc_hook
reactivated_as_season_throughline
reactivated_as_horizon_payoff
reactivated_as_source_local
reactivation_quarantined
reactivation_escalated
```

## Time Skip Procedure
A time skip is a structured transition, not a narrative fast-forward.

```text
1. Declare time span and scope.
2. Identify actors, locations, factions, objects, Projects, resources, threats, and promises affected.
3. Resolve owner-file-required states before the skip if they cannot be safely skipped.
4. Apply aging outcomes.
5. Apply pressure decay or intensification.
6. Update Projects, recovery, faction/domain states, value/economy states, and object/platform states through owner files.
7. Reclassify active, dormant, archived, retired, source-local, quarantined, and escalated state.
8. Define new campaign baseline.
9. Record reactivation triggers.
10. Preserve hidden-state boundaries.
```

A skipped interval may compress procedure, but cannot erase ownership, debts, injuries, transformations, faction claims, or unresolved promises without lawful outcome.

## State Pruning
Pruning reduces active campaign burden without deleting history.

Pruning triggers:

```text
active state list exceeds usable load;
many pressures have low salience;
players no longer engage a thread;
season seam reached;
campaign phase changed;
source-local boundary closed;
runtime/context packet would become overloaded;
owner files mark state resolved;
state is redundant, merged, or superseded.
```

Pruning outcomes:

```text
demote_to_dormant
move_to_archive
retire_with_reason
merge_with_related_state
summarize_as_background
convert_to_reactivation_trigger
source_local_close
quarantine_unresolved_state
escalate_structural_overload
```

## Anti-drift controls
```text
Do not use time skips to erase consequences.
Do not preserve all state at equal active priority.
Do not treat archive as deletion.
Do not treat retirement as forgetting.
Do not let inactive background state clutter active play.
Do not let pressure decay erase owner-file consequences.
Do not let pressure intensification invent effects without owner-file support.
Do not resolve D13 Projects, D15 faction operations, D17 economy shifts, or D09 object states directly inside D18.
Do not let source-local clocks, seasons, or campaign phases become Astra campaign law.
Do not let pruning discard payoff-bearing continuity.
Do not let runtime/context needs rewrite doctrine; D18 only defines handoff requirements.
```


---

# D18-06 — Source-Local Campaign Structures, Donor Structural-Time Mapping, Quarantine, and Escalation

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-06 defines how Astra converts donor campaign structures, adventure paths, seasonal arcs, faction clocks, domain turns, downtime years, hexcrawl calendars, cultivation realm arcs, endgame tiers, recurring-villain procedures, campaign milestones, generational play, and long-horizon progression models without allowing donor campaign architecture to become universal Astra campaign law.

D18-06 does not define final scenario schemas, adventure-path schemas, faction schemas, runtime state schemas, campaign calendar implementation, or live-play GM behavior.

## Functional Donor Structural-Time Mapping Ladder
Every donor structural-time construct follows this ladder:

```text
1. Identify the donor structural-time construct.
2. Identify the evidence type.
3. Identify the structural-time function.
4. Identify the scale: scene, arc, season, phase, horizon, campaign, generation, or source-local.
5. Identify the state lifecycle effects: capture, retrieval, aging, decay, intensification, retirement, archive, reset, reactivation.
6. Identify campaign promises and payoff scale.
7. Identify progression axis and power-envelope assumptions.
8. Identify donor defaults that must not be imported.
9. Identify owner-file handoffs.
10. Assign one lawful handling:
    - direct Astra mapping;
    - normalized Astra structural-time mapping;
    - source-local retained construct;
    - quarantined construct pending later doctrine/evidence;
    - escalated doctrine problem.
11. Record rejected donor assumptions.
```

Donor structures are evidence, not authority.

## Donor evidence types
```text
adventure_path
campaign_chapter
scenario_sequence
quest_chain
front
clock
countdown
faction_turn
domain_turn
kingdom_turn
downtime_cycle
travel_calendar
hexcrawl_calendar
season_framework
episode_framework
campaign_phase
level_band
tier_band
realm_ladder
rank_ladder
prestige_cycle
reincarnation_cycle
generational_play
legacy_system
endgame_structure
recurring_villain_procedure
campaign_event_table
random_campaign_event_table
timeline
metaplot
source_local_campaign_script
mixed_structural_time_system
```

D18 does not equate these labels with Astra arcs, seasons, phases, or horizon structures.

## Structural-time function
D18 maps function before label.

```text
organizes_local_arc
groups_arcs
paces_campaign_phase
tracks_unresolved_pressure
advances_background_state
ages_world_state
escalates_faction_pressure
paces_downtime
paces_travel
paces_domain_evolution
paces_advancement
paces_breakthroughs
paces_threat_return
paces_resource_pressure
creates_season_boundary
creates_time_skip
creates_reset
creates_recurring_payoff
defines_endgame
defines_legacy_transition
preserves_metaplot
creates_source_local_structure
```

Examples:

```text
A faction clock is not automatically a D18 season or D15 faction procedure. Its function may be unresolved pressure tracking, background-state advancement, faction-operation pacing, or source-local countdown.
A cultivation realm sequence is not automatically Astra campaign phase doctrine. Its function may be advancement pacing, breakthrough spacing, power-envelope shift, identity transformation, or source-local progression structure.
An adventure path chapter is not automatically an Astra arc. Its function may be scenario sequence, site progression, faction pressure, reward pacing, or source-local campaign script.
A kingdom turn is not automatically D18 season procedure. Its function may be D15 institutional operation, D17 economy update, D13 Project interval, D10 world-state update, or source-local domain procedure.
```

## Scale classification
```text
scene_scale
arc_scale
season_scale
campaign_phase_scale
long_horizon_scale
campaign_calendar_scale
domain_or_institution_scale
generation_scale
metaplot_scale
source_local_scale
mixed_scale
unclear_scale
```

A donor campaign book may include arc-scale chapters, season-scale acts, level-band progression, reward pacing, faction cycles, and metaplot escalation. D18 should split and route parts rather than treat the whole book as one construct.

## State lifecycle effects
```text
captures_state
stores_state
retrieves_state
reconciles_state
ages_state
decays_pressure
intensifies_pressure
archives_state
retires_state
reactivates_state
resets_active_state
hard_resets_state
creates_time_skip
prevents_time_skip
creates_background_evolution
creates_campaign_event
creates_payoff
defers_payoff
creates_endgame_horizon
source_local_state_effect
```

Any donor structure that erases state without authority must be source-local, quarantined, or escalated.

## Promise and payoff handling
Donor campaign promises may include defeating a final antagonist, liberating a region, ascending to a realm, restoring a kingdom, solving a conspiracy, surviving apocalypse, founding a sect, claiming a throne, repairing a ship, breaking a curse, completing a pilgrimage, or unlocking endgame.

D18 classifies those by payoff scale:

```text
arc_payoff
season_payoff
campaign_phase_payoff
long_horizon_payoff
legacy_payoff
source_local_payoff
unclear_payoff
```

A converted source may retain its own promise source-locally. Astra does not become structured around that promise unless later canonized.

## Progression and power-envelope assumption review
D18 rejects unreviewed assumptions such as:

```text
level range defines campaign phase;
realm rank defines season;
faction rank defines arc;
adventure chapter defines advancement;
kingdom/domain tier defines campaign scale;
endgame unlock defines horizon;
prestige/reincarnation cycle defines long-horizon law;
boss escalation defines progression curve;
source metaplot defines Astra canon trajectory.
```

## Lawful outcomes
### Direct Astra mapping
Use direct mapping only when the donor structural-time construct already fits D18 without importing unsupported campaign assumptions.

### Normalized Astra structural-time mapping
Use normalized mapping when the donor structure has reusable campaign-time function but donor packaging must be stripped.

Examples:

```text
A donor faction clock becomes unresolved pressure with decay/intensification states and D15/D10 owner-file handoffs. The donor clock shape is evidence, not Astra law.
A donor adventure path act becomes a source-local season throughline or arc cluster, not universal campaign structure.
A donor level band becomes power-envelope evidence, not campaign phase law.
A donor cultivation realm arc becomes breakthrough-spacing and power-envelope evidence with D04/D06/D18 handoffs, not Astra realm pacing.
A donor downtime year becomes time-advance scale with D13/D15/D17/D18 handoffs, not automatic free progression.
A donor endgame chapter becomes horizon-promise evidence, not Astra endgame doctrine.
```

### Source-local retained construct
Use source-local retention when the donor structural-time system is valuable inside a converted source but unsafe to generalize.

Examples:

```text
a named adventure path sequence;
a campaign-specific metaplot;
a setting-specific apocalypse clock;
a source-local faction countdown;
a realm-ladder tied to one cultivation setting;
a unique reincarnation cycle;
a donor-specific prestige/endgame reset;
a campaign chapter structure;
a source-local kingdom turn;
a particular hexcrawl calendar;
a scenario event table;
a named prophecy timeline;
a source-local season script.
```

### Quarantine
Quarantine donor structural-time systems when extraction damage, missing timelines/tables/sidecars, unclear boundaries, unsupported reset/calendar/faction/domain/realm/downtime/generational/endgame/event/metaplot assumptions, unclear state mutation, unclear payoff scale, unclear owner-file support, or unclear source-local boundary prevents safe mapping.

### Escalation
Escalate repeated or high-impact missing doctrine.

Examples:

```text
Repeated adventure-path donors require mission/scenario/adventure structural schema with D18 arc/season fields.
Repeated faction-clock donors require unresolved-pressure clock interface with D10/D15/D18.
Repeated cultivation donors require coordinated D04/D18 breakthrough-spacing and horizon-phase doctrine.
Repeated domain/kingdom donors require season/domain cycle doctrine with D10/D13/D15/D17/D18.
Repeated hexcrawl/calendar donors require campaign-calendar handoff doctrine with D14/D18.
Repeated generational-play donors require legacy/succession doctrine with D08/D10/D15/D18.
Repeated endgame/post-apex donors require horizon-ceiling and post-apex continuation doctrine.
Repeated metaplot donors require source-local metaplot containment and canon-candidate rules.
Repeated campaign-event tables require table/oracle governance with D10/D18/Batch C.
```

## Rejected imports
```text
adventure path as Astra campaign law;
chapter sequence as Astra arc sequence;
act structure as Astra season structure;
faction clock as universal pressure tracking;
front as universal campaign-threat model;
kingdom/domain turn as universal season procedure;
hexcrawl calendar as universal campaign time;
downtime year as automatic progression;
level band as campaign phase;
realm ladder as horizon structure;
tier rank as power envelope;
prestige/reincarnation as default long-horizon reset;
hard reset as lawful seasonal renewal without authority;
metaplot as Astra canon;
final boss as required horizon structure;
endgame tier as campaign apex law;
recurring villain survival by fiat;
time skip as consequence erasure;
season finale as required campaign rhythm;
source-local prophecy as Astra long-horizon promise;
campaign event table as world-state truth.
```

## Table-like, clock-like, and path-like routing
Campaign paths, clocks, event tables, realm ladders, faction/domain turns, hexcrawl calendars, metaplots, timelines, and endgame structures route by function to D18, D10, D13, D14, D15, D16, D17, D04, Batch C, source-local retention, quarantine, or escalation.

## Structural-time guardrails
```text
Structural time is integrated; continuity, arcs, seasons, and horizon cannot be converted independently when a donor campaign structure ties them together.
Each scale makes its own promise; arc payoff cannot always be deferred to season, and season payoff cannot always be deferred to horizon.
Continuity can be burden, but it is also payoff fuel.
Long-horizon progression should govern seasons, not be driven by seasonal escalation.
Dimensional rotation is required when single-axis growth begins to saturate.
The long middle is a known danger zone where continuity load, arc freshness, season renewal, and horizon pull can all fail together.
The correct fix may be at a different scale than the symptom.
```


---

# D18-07 — Records, Integration Checklists, Anti-Drift Rules, and Runtime Persistence Handoff Shapes

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-07 defines lightweight **not-final-schema** record shapes and final integration controls so campaign continuity, arc promises, seasons, state aging, progression horizons, source-local campaign structures, time skips, payoff scale, dimensional rotation, and donor structural-time systems remain auditable during conversion, canon review, future runtime design, and eventual play.

These are doctrine-facing and conversion-facing controls. They are not final runtime schemas, save-state schemas, context-packet formats, campaign calendar implementations, or live-play GM procedures.

## Record family list
```text
Structural Time State Record
Continuity Lifecycle Record
Arc Promise / Question Record
Pacing / Contrast / Payoff Budget Record
Season Throughline / Seam Record
Long-Horizon Trajectory / Phase / Rotation Record
Transformation / Breakthrough / Major Change Spacing Record
Time Skip / State Aging / Pruning Record
Donor Structural-Time Mapping Record
Runtime Persistence Handoff Note Record
Owner-file handoff / unresolved structural-time pressure
```

## 1. Structural Time State Record
```yaml
structural_time_state_record:
  record_type: structural_time_state
  state_id: string
  state_summary: string
  owner_file_primary: D04 | D07 | D08 | D09 | D10 | D13 | D15 | D16 | D17 | D18 | source_local | unknown
  owner_file_handoffs: []
  half_life: permanent | durable_mutable | active_transient | ephemeral | source_local_half_life | quarantined_half_life | escalated_half_life
  salience: critical | high | medium | low | background | hidden | source_local | quarantined
  continuity_layer: foreground | background | hidden | source_local | mixed
  activity_status: active | dormant | archived | retired | source_local | quarantined | escalated
  capture_reason: identity | advancement | transformation | persistent_harm | relationship | obligation | faction | law | world_state | domain | object_state | recurring_threat | arc_promise | season_throughline | source_local_continuity | canon_candidate | other
  retrieval_triggers: []
  reactivation_triggers: []
  hidden_state_boundary: player_visible | gm_visible | backend_hidden | source_local_hidden | mixed
  notes: string
```

## 2. Continuity Lifecycle Record
```yaml
continuity_lifecycle_record:
  record_type: continuity_lifecycle
  lifecycle_id: string
  state_ref: string
  capture_status: captured | not_captured | promoted_after_initial_omission | disputed_capture | source_local_capture | quarantined
  storage_status: stored_in_owner_file | stored_in_D18_index | missing_owner_storage | source_local_storage | quarantined_storage
  retrieval_status: not_yet_retrieved | retrieved_for_arc | retrieved_for_season | retrieved_for_horizon | retrieved_for_reconciliation | retrieved_for_runtime_handoff | retrieval_blocked | source_local_retrieval
  reconciliation_status: none_required | confirmed_old_state | confirmed_new_state | merged_states | reinterpreted_ambiguous_state | promoted | downgraded | marked_source_local | quarantined | escalated | retired_with_reason | continuity_repair_note_created
  aging_status: unchanged | progressed | decayed | intensified | stabilized | resolved | partially_resolved | transformed | split | merged | dormant | archived | retired | lost | expired | evolved_offscreen | source_local_closed | source_local_continues | quarantined | escalated
  last_review_context: arc | season | time_skip | phase_transition | contradiction | source_local_boundary | canon_candidate_review | runtime_handoff | other
  notes: string
```

## 3. Arc Promise / Question Record
```yaml
arc_promise_question_record:
  record_type: arc_promise_question
  arc_id: string
  arc_title_or_label: string
  arc_promise: []
  central_question_or_pressure: string
  question_state: opened | active | complicated | partially_answered | answered | deferred_to_season | deferred_to_horizon | transformed_into_new_question | retired | archived | source_local | quarantined | escalated
  primary_pressure_type: threat_pressure | mystery_pressure | faction_pressure | relationship_pressure | domain_pressure | resource_pressure | time_pressure | travel_pressure | legal_pressure | identity_pressure | breakthrough_pressure | recovery_pressure | source_local_pressure | mixed
  payoff_scale: scene_payoff | arc_payoff | season_payoff | campaign_phase_payoff | long_horizon_payoff | canon_candidate_payoff | source_local_payoff
  required_continuity_refs: []
  useful_amplifier_refs: []
  background_texture_refs: []
  hidden_retrieval_refs: []
  crisis_type: combat_crisis | social_crisis | legal_crisis | faction_crisis | mystery_reveal | resource_collapse | identity_test | breakthrough_attempt | domain_claim | platform_failure | project_deadline | escape_window | moral_decision | source_local_crisis | mixed
  closure_outcome: unresolved | resolved | resolved_with_cost | partially_resolved | transformed | deferred_to_season | deferred_to_horizon | opened_new_arc | retired_pressure | archived_pressure | dormant_pressure | failed_forward | quarantined | escalated | source_local_closure
  owner_file_handoffs: []
  notes: string
```

## 4. Pacing / Contrast / Payoff Budget Record
```yaml
pacing_contrast_payoff_budget_record:
  record_type: pacing_contrast_payoff_budget
  pacing_id: string
  arc_or_season_ref: string
  escalation_state: escalating | consolidating | breathing_room | crisis_approaching | crisis_active | denouement | stagnant | fatigued | source_local
  consolidation_modes: []
  payoff_scale_budgeted: scene_payoff | arc_payoff | season_payoff | campaign_phase_payoff | long_horizon_payoff | canon_candidate_payoff | source_local_payoff
  payoff_status: unspent | partially_spent | spent | deferred | transformed | overdrawn | misallocated | quarantined | escalated
  fatigue_risk: none | low | medium | high | active
  stagnation_risk: none | low | medium | high | active
  wrong_scale_repair_risk: none | low | medium | high | active
  notes: string
```

## 5. Season Throughline / Seam Record
```yaml
season_throughline_seam_record:
  record_type: season_throughline_seam
  season_id: string
  season_label: string
  season_throughline: survival_under_pressure | territory_or_domain_stabilization | faction_entanglement | settlement_or_platform_recovery | mystery_or_hidden_truth_exposure | war_or_campaign_conflict | relationship_network_realignment | economic_or_resource_crisis | training_and_breakthrough_preparation | identity_transformation | realm_or_route_transition | institutional_ascension | exploration_of_new_region | recovery_after_catastrophe | source_local_throughline | mixed
  season_promise: string
  active_arc_refs: []
  season_payoff_state: season_throughline_unresolved | season_throughline_resolved | season_throughline_resolved_with_cost | season_throughline_partially_resolved | season_throughline_transformed | season_throughline_deferred_to_horizon | season_throughline_failed_forward | season_throughline_retired | season_throughline_archived | season_throughline_split_into_new_season | season_throughline_quarantined | season_throughline_escalated | source_local_season_payoff
  active_state_refs: []
  dormant_state_refs: []
  archive_state_refs: []
  retirement_state_refs: []
  carry_forward_refs: []
  closure_list: []
  continuation_list: []
  reset_type: none | soft_reset | active_state_reset | premise_shift | location_shift | faction_landscape_shift | resource_baseline_shift | power_envelope_review | time_skip_reset | cast_or_spotlight_shift | source_local_reset | hard_reset_explicit_authority_only
  continuity_laundering_review: passed | failed | requires_reconciliation | quarantined | escalated
  false_reset_review: passed | failed | requires_new_baseline | source_local | quarantined
  seam_status: not_reached | pending | completed | incomplete_closure | incomplete_continuation | overloaded | quarantined | escalated
  owner_file_handoffs: []
  notes: string
```

## 6. Long-Horizon Trajectory / Phase / Rotation Record
```yaml
long_horizon_trajectory_phase_rotation_record:
  record_type: long_horizon_trajectory_phase_rotation
  horizon_id: string
  long_horizon_trajectory: survival_to_stability | local_actor_to_regional_force | wanderer_to_domain_holder | apprentice_to_master | mortal_to_ascendant | isolated_party_to_institutional_power | crew_to_platform_power | fugitive_to_legitimate_authority | ignorance_to_cosmic_understanding | broken_world_to_rebuilt_order | sect_member_to_sect_founder | scavenger_to_artificer_power | source_local_trajectory | mixed
  campaign_phase: local_survival | local_stability | regional_emergence | faction_entanglement | institutional_recognition | domain_responsibility | settlement_or_platform_stewardship | inter_realm_or_interstellar_access | mythic_or_apex_pressure | ascendant_conflict | legacy_or_succession | post_apex_transformation | source_local_phase
  power_envelope: below_pressure | near_pressure | above_old_pressure | new_axis_required | consolidation_needed | overinflated | source_local_envelope
  foreground_axes: []
  supporting_axes: []
  resting_axes: []
  saturated_axes: []
  emerging_axes: []
  blocked_axes: []
  source_local_axes: []
  dimensional_rotation_state: not_needed | recommended | active | overdue | blocked | source_local | quarantined | escalated
  escalation_consolidation_posture: escalation | consolidation | mixed | wrong_scale_escalation | stagnation | inflation_risk | source_local
  horizon_promise_state: undefined_open_sandbox | emerging_horizon | declared_horizon | phase_horizon | seasonal_horizon | long_horizon_apex | post_apex_continuation | source_local_horizon | quarantined_horizon
  long_middle_status: not_in_long_middle | healthy | busy_but_stagnant | overloaded | payoff_starved | dimensionally_collapsed | retrieval_failure | continuity_overload | source_local | quarantined | escalated
  owner_file_handoffs: []
  notes: string
```

## 7. Transformation / Breakthrough / Major Change Spacing Record
```yaml
transformation_breakthrough_spacing_record:
  record_type: transformation_breakthrough_spacing
  spacing_id: string
  major_change_kind: major_breakthrough | realm_tier_phase_transition | identity_altering_transformation | route_defining_oath_or_principle_shift | domain_claim | platform_acquisition_or_major_upgrade | settlement_or_domain_founding | faction_rank_change | institutional_legitimacy_shift | major_relationship_reconfiguration | recurring_threat_retirement | long_horizon_truth_reveal | legacy_transition | source_local_phase_change
  owner_file_primary: D04 | D06 | D08 | D09 | D10 | D15 | D16 | D17 | D18 | source_local | unknown
  spacing_state: too_soon | well_timed | delayed_for_consolidation | reserved_for_season_payoff | reserved_for_phase_payoff | reserved_for_horizon_payoff | blocked_by_owner_file | source_local_spacing | quarantined | escalated
  payoff_scale: arc_payoff | season_payoff | campaign_phase_payoff | long_horizon_payoff | source_local_payoff
  consolidation_required_before: true | false | unknown
  consolidation_required_after: true | false | unknown
  notes: string
```

## 8. Time Skip / State Aging / Pruning Record
```yaml
time_skip_state_aging_pruning_record:
  record_type: time_skip_state_aging_pruning
  time_advance_id: string
  time_advance_trigger: end_of_arc | end_of_season | downtime_interval | downtime_season | large_time_skip | travel_span | recovery_period | training_period | project_interval_sequence | faction_operation_cycle | domain_evolution_cycle | settlement_growth_period | platform_refit_period | campaign_phase_transition | source_local_phase_transition | continuity_overload_review | runtime_context_pruning_review | canon_candidate_review
  time_advance_scale: scene_to_scene | session_to_session | arc_interval | downtime_interval | season_interval | months | years | generation | realm_or_route_transition | interstellar_or_interrealm_span | post_catastrophe_span | source_local_span | unknown_span
  affected_state_refs: []
  aging_outcomes: []
  pressure_decay_states: []
  pressure_intensification_states: []
  retirement_refs: []
  archive_refs: []
  reactivation_triggers: []
  new_campaign_baseline: string
  hidden_state_boundary_review: passed | required | blocked | source_local | quarantined
  continuity_laundering_review: passed | failed | requires_reconciliation | quarantined | escalated
  owner_file_handoffs: []
  notes: string
```

## 9. Donor Structural-Time Mapping Record
```yaml
donor_structural_time_mapping_record:
  record_type: donor_structural_time_mapping
  donor_label: string
  donor_evidence_type: adventure_path | campaign_chapter | scenario_sequence | quest_chain | front | clock | countdown | faction_turn | domain_turn | kingdom_turn | downtime_cycle | travel_calendar | hexcrawl_calendar | season_framework | episode_framework | campaign_phase | level_band | tier_band | realm_ladder | rank_ladder | prestige_cycle | reincarnation_cycle | generational_play | legacy_system | endgame_structure | recurring_villain_procedure | campaign_event_table | random_campaign_event_table | timeline | metaplot | source_local_campaign_script | mixed_structural_time_system
  donor_function_summary: string
  structural_time_function: []
  scale_classification: scene_scale | arc_scale | season_scale | campaign_phase_scale | long_horizon_scale | campaign_calendar_scale | domain_or_institution_scale | generation_scale | metaplot_scale | source_local_scale | mixed_scale | unclear_scale
  lifecycle_effects: []
  mapped_d18_element: continuity_lifecycle | arc_promise | season_throughline | long_horizon_trajectory | transformation_spacing | time_skip_aging_pruning | source_local | quarantine | escalation
  lawful_outcome: direct_astra_mapping | normalized_astra_mapping | source_local_retained_construct | quarantined_construct_pending_later_doctrine | escalated_doctrine_problem
  rejected_import_notes: []
  source_local_boundary: string | null
  structural_time_guardrail_flags:
    - payoff_deferral_risk
    - continuity_overload_risk
    - dimensional_collapse_risk
    - long_middle_failure_risk
    - wrong_scale_repair_risk
    - continuity_laundering_risk
    - donor_campaign_law_leakage_risk
  owner_file_handoffs: []
  confidence: high | medium | low | blocked
```

## 10. Runtime Persistence Handoff Note Record
This is not implementation. It is a doctrine-facing handoff control.

```yaml
runtime_persistence_handoff_note_record:
  record_type: runtime_persistence_handoff_note
  handoff_id: string
  state_refs: []
  capture_required: true | false | unknown
  owner_file_storage_required: true | false | unknown
  retrieval_trigger_required: true | false | unknown
  salience_filter_required: true | false | unknown
  hidden_state_boundary_required: true | false | unknown
  context_packet_candidate: true | false | unknown
  over_surface_risk: none | low | medium | high
  under_surface_risk: none | low | medium | high
  not_final_runtime_schema: true
  notes: string
```

## Record posture rules
```text
Every record here is not final schema.
Every record is doctrine-facing and conversion-facing.
D18 records structural-time relevance, not all owner-file detail.
Runtime Gate B or later schema doctrine may replace or formalize these shapes.
Do not implement these directly as save schemas without later schema review.
```


---

# D18-09 — Integration Checklists, DDR Register, Anti-Drift Rules, and Acceptance Criteria

> Doctrine status: D18 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied structural-time research is used as non-final research pressure and guardrail material, not canon terminology by default.


## Purpose
D18-09 is the final control file for the D18 doctrine pack. It records integration expectations, owner-file dependencies, source-local boundaries, donor-family pressures, risk controls, DDR summary, and acceptance criteria.

## Owner-file integration checklist
```text
D04 — breakthrough history, advancement milestones, transformations, major change payloads. D18 governs spacing and horizon placement only.
D07 — persistent harm, scars, corruption, recovery, pressure intensification/degradation consequences.
D08 — actor continuity, personhood, companion/summon identity, recurring NPC substrate, generational/legacy actor issues.
D09 — object, relic, platform, vehicle, tool, container, salvage, material, and custody state.
D10 — world-state, factions, law, public belief, hidden truth, relationships, region evolution, unresolved pressure, market/world facts.
D13 — Projects, downtime, training, recovery, crafting, repair, maintenance, long tasks, interval progress.
D14 — travel spans, route revisits, exploration returns, site re-entry, regional discovery, hexcrawl/calendar handoffs.
D15 — faction operations, claims, obligations, law enforcement, domain authority, institutions, standing, access operations.
D16 — recurring opposition, threat posture, hazard recurrence, boss/source-local threat continuity.
D17 — value, ownership, custody, debt, economy, reward, requisition, inventory, salvage, economic aging.
D18 — structural-time classification, half-life, salience, arc promise, season seam, horizon, pruning, archive, retirement, source-local campaign mapping.
```

D18 must not replace any owner file. It classifies campaign-scale relevance and routes concrete effects.

## Source-local boundary checklist
A donor structural-time system may remain source-local only if it records:

```text
donor construct label;
evidence type;
function;
scale;
lifecycle effects;
payoff scale;
owner-file handoffs;
source-local boundary;
rejected-import notes;
quarantine/escalation trigger if repeated or unsafe;
closure, continuation, or re-entry rule.
```

Source-local systems do not become Astra law through polish, repetition, or convenience.

## Quarantine checklist
Quarantine is required when:

```text
state cannot be classified by half-life or salience;
continuity evidence is missing or contradictory;
arc promise or payoff scale is unclear;
season seam would erase consequences;
time skip would mutate owner-file state without support;
donor campaign structure has unclear function or scale;
donor reset, clock, event table, realm ladder, faction turn, or endgame assumption lacks owner-file support;
runtime handoff would over-surface or under-surface hidden/critical state without later schema support.
```

## Escalation checklist
Escalate when repeated or high-impact pressure exposes missing Astra doctrine, especially:

```text
formal campaign-state schema needs;
mission/scenario/adventure structural schema needs;
unresolved-pressure clock interface needs;
calendar / time-scale governance needs;
generational / legacy play doctrine needs;
post-apex continuation doctrine needs;
domain/kingdom/seasonal operation interface needs;
source-local metaplot containment rules;
runtime context-packet salience/filtering doctrine.
```

## Anti-drift rules
```text
Do not treat “the world remembers” as “everything stays active forever.”
Do not use time skips, seasons, phase changes, or source-local closure to erase consequences.
Do not treat archive as deletion or retirement as forgetting.
Do not let continuity tracking become the sole measure of campaign quality.
Do not make arcs mandatory railroads or narrative-only labels.
Do not defer every payoff to season or horizon.
Do not consume season or long-horizon payoff casually at arc scale.
Do not make seasons mandatory.
Do not treat grouped arcs as a season without a throughline.
Do not use seasonal reset for continuity laundering.
Do not equate campaign phase with level, tier, realm, class rank, or donor progression band.
Do not let raw power be the only long-horizon progression axis.
Do not treat consolidation as lack of progress.
Do not solve stagnation only by increasing stakes.
Do not solve continuity overload by discarding payoff-bearing history.
Do not let donor adventure paths, faction clocks, hexcrawl calendars, realm ladders, kingdom turns, metaplots, endgame tiers, or campaign-event tables become Astra campaign law.
Do not let D18 become D04 advancement, D10 world-state, D11 presentation, D13 project, D15 faction, D16 opposition, D17 economy, or final runtime doctrine.
```

## Risk fixes embedded
The following high-priority risks were embedded throughout D18:

```text
World memory could become active-state overload.
Continuity could be treated as storage only.
State half-life and salience could be flattened.
D18 could become the campaign database.
Retrieval could be left to memory or future runtime.
Reconciliation could become silent retcon.
Arcs could become railroads or vague labels.
Payoff scale could be misallocated.
Consolidation could be treated as filler.
Seasons could become mandatory or launder consequences.
False resets, diminishing seasons, and bloated seasons could pass unmarked.
Long-horizon progression could collapse into raw power escalation.
Campaign phase could import donor level/realm/tier/rank structures.
Breakthroughs and transformations could become routine.
Horizon promises could become indefinite bait.
Long-middle failure could be misdiagnosed at the wrong scale.
Time skips could erase consequences.
Pressure decay could erase owner-file consequences.
Pressure intensification could invent owner-file effects.
Archive and retirement could be confused.
Dormant/archived state could become inaccessible.
Donor campaign labels could become Astra structure by false equivalency.
Runtime persistence notes could become final schema.
```

## DDR register
```text
D18-00 Decision: Use Structural Time Architecture.
Rationale: captures continuity, arcs, seasons, and horizon as integrated structural time rather than separate flavor layers.
Risk: may seem more complex than campaign pacing.
Control: lightweight records and owner-file handoffs; no final runtime schema.

D18-01 Decision: Use continuity lifecycle with half-life and salience.
Rationale: avoids both forgetting and active-state overload.
Risk: classification overhead.
Control: classify only captured state that may matter later.

D18-02 Decision: Use Arc Promise–Pressure–Payoff Model.
Rationale: avoids railroads while making arcs auditable.
Risk: arc language may drift narrative.
Control: payoff scale, question state, closure routing.

D18-03 Decision: Use Season Throughline–Seam–Reclassification Model.
Rationale: supports optional renewal and state pruning without consequence erasure.
Risk: seasons may become mandatory.
Control: seasons are optional and require throughline to qualify.

D18-04 Decision: Use Trajectory–Phase–Rotation Model.
Rationale: protects long campaigns from single-axis escalation, stagnation, and broken horizon promises.
Risk: trajectory may seem like railroading.
Control: trajectory is a vector, not an outcome guarantee.

D18-05 Decision: Use State Aging–Pruning–Reactivation Model.
Rationale: separates history from active burden and makes time skips lawful.
Risk: pruning could become deletion.
Control: archive is not deletion; retirement requires recorded reason.

D18-06 Decision: Use Functional Donor Structural-Time Mapping Ladder.
Rationale: donor campaign architecture is high-leakage and must map by function, not label.
Risk: source-local structures may over-accumulate.
Control: quarantine/escalation for repeated or high-impact gaps.

D18-07 Decision: Include lightweight not-final-schema records and runtime persistence handoff notes.
Rationale: structural time cannot be audited from prose alone.
Risk: records could be mistaken for runtime schema.
Control: every record is explicitly not final schema.
```

## Acceptance criteria
D18 is acceptable only if it can:

```text
Treat structural time as an integrated campaign layer.
Define continuity lifecycle through capture, classify, store, retrieve, reconcile, and age/archive/retire.
Classify state by half-life, salience, foreground/background continuity, and activity status.
Preserve meaningful history without keeping all history active.
Retrieve state selectively and lawfully.
Reconcile contradictions without silent retcon.
Treat arcs as promise/pressure/payoff containers, not railroads.
Track question/answer economy and payoff scale.
Use seasons as optional throughline/seam/reclassification containers.
Prevent false resets and continuity laundering.
Govern long-horizon progression through trajectory, phase, power envelope, progression axes, dimensional rotation, and transformation spacing.
Treat consolidation as active progression.
Track horizon promises and long-middle failure risks.
Use structured time skip, state aging, pruning, archive, retirement, and reactivation procedures.
Map donor campaign structures by function, not label.
Preserve bounded source-local campaign structures.
Quarantine unsupported structural-time constructs.
Escalate repeated or high-impact missing doctrine.
Prepare runtime persistence handoff requirements without defining final runtime schemas.
```


---
