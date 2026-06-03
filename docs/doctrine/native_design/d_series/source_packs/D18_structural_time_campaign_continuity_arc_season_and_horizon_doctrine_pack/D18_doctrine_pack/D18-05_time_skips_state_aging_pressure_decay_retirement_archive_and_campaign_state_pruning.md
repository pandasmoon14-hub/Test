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
