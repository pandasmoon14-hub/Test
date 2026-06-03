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
