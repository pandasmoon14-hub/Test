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
