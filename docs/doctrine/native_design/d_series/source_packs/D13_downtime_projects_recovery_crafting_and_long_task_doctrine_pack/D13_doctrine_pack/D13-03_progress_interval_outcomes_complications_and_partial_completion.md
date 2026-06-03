# D13-03 — Progress, Interval Outcomes, Complications, and Partial Completion

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra determine what happens during each Project interval without forcing every Project into a universal progress clock, fixed downtime table, or binary success/failure result?

D13-03 defines how Projects advance, stall, complicate, partially complete, fail, accelerate, or hand off across intervals. It does not define final recovery values, item crafting math, research truth, training advancement, faction operations, market acquisition, or campaign-season pacing.

## Core progress model

D13 uses **Interval Outcome States** rather than universal progress points or clocks.

Each interval can produce one of these outcomes:

- `advanced`
- `advanced_with_cost`
- `partial`
- `stalled`
- `blocked`
- `complicated`
- `damaged`
- `interrupted`
- `completed`
- `completed_with_complication`
- `failed`
- `abandoned`
- `quarantined`
- `escalated`

Owner files decide what each outcome means for the state they own.

## Progress is not always numeric

A Project may advance by:

- stage completion;
- requirement satisfaction;
- risk reduction;
- evidence discovery;
- object-state improvement;
- condition stabilization;
- relationship repair;
- material accumulation;
- facility preparation;
- training posture improvement;
- route/principle refinement;
- faction access improvement;
- source-local milestone.

Numeric progress is allowed only when an owner file, source-local procedure, or later schema supports it.

## Interval check trigger

An interval check occurs only when uncertainty, opposition, risk, consequence, or source-local procedure requires it.

Triggers include:

- committed interval ends and outcome is uncertain;
- risky method is used;
- requirement is unstable;
- hidden pressure may surface;
- resource or material may be consumed;
- external pressure interrupts;
- progress is contested;
- actor attempts to accelerate;
- actor works under poor conditions;
- source-local procedure calls for a check.

Not every interval requires a roll. D13 calls D02 only when uncertainty, opposition, risk, or consequence exists. D02 owns the roll and outcome math.

## Interval outcome routing

D13 routes interval outcomes by Project family.

| Project family | Likely owner-file routing |
|---|---|
| recovery | D07 for injury, condition, corruption, relapse, recovery limits; D08 if substrate/form-state matters; D03 if backlash/recharge interacts. |
| training | D04/D05/D06 for advancement gate, competency, method, access, route, Technique, or domain implications. |
| research | D05/D10/D11 for methods, information-state, clue handling, hidden truth, rumor, public belief, and presentation. |
| crafting | D09/D17 for object state, material use, ownership, scarcity, and economy; D03/D06 if resource or power expression matters. |
| salvage | D09/D17 for recovered components, legality, scarcity, ownership, and salvage rights. |
| repair | D09 for object/platform state; D07 if unsafe repair threatens actors; D17 for parts/cost. |
| social | D10/D15 for relationship, reputation, standing, law, institution, and faction pressure. |
| faction-support | D10/D15 for faction status, pressure, trace, obligations, and institutional response. |
| preparation | D03/D04/D05/D06/D09/D10/D14/D15/D17/D18 depending target. |
| resource gathering | D17/D10/D14/D09 depending source, location, and ownership. |
| special/source-local | source-local boundary plus owner-file review. |

## Partial completion

Partial completion is a first-class outcome.

It may produce:

- usable but flawed object;
- temporary recovery;
- limited clue;
- reduced cost for later attempt;
- improved requirement status;
- new access route;
- smaller material yield;
- progress toward a later stage;
- relationship thaw but not trust;
- facility prepared but not completed;
- salvage recovered but damaged;
- ritual site stabilized but exposed.

Partial completion should not be treated as failure unless the Project goal specifically required all-or-nothing completion.

## Complication classification

Complications are classified and routed to owner files.

Complication families:

- `cost_increase`
- `delay`
- `material_loss`
- `tool_or_facility_damage`
- `assistant_risk`
- `injury_or_condition_setback`
- `corruption_or_instability_pressure`
- `object_instability`
- `social_scrutiny`
- `faction_attention`
- `legal_exposure`
- `information_false_lead`
- `hidden_pressure_surface`
- `source_local_threat`
- `active_scene_trigger`
- `owner_file_gap`

A complication may trigger a D12 transition into an active scene if immediate response matters.

## Failure handling

D13 distinguishes failure types:

| Failure type | Meaning |
|---|---|
| clean failure | Project does not advance but no extra harm occurs. |
| costly failure | Project fails and consumes cost/material/time. |
| reversible failure | Project can retry after a requirement changes. |
| damaging failure | Project worsens actor, object, world, faction, or source-local state. |
| revealing failure | Project fails but exposes useful information. |
| terminal failure | Project cannot continue without new doctrine, major requirement, or source-local event. |

Failure does not automatically erase all progress unless the Project structure or owner file says it does.

## Acceleration and overcommitment

A player may attempt to accelerate a Project by spending more resources, accepting more exposure, using unsafe methods, invoking Techniques, calling in favors, overworking contributors, using unstable facilities, or compressing interval time.

Acceleration is allowed only when supported by owner files and explicit cost/risk exposure.

Acceleration may produce:

- shorter interval;
- extra progress;
- higher complication risk;
- material waste;
- fatigue or injury;
- object instability;
- social scrutiny;
- resource overdraw;
- backlash;
- source-local consequences.

D03, D07, D09, D10, and D17 own the actual consequences where relevant.

## Donor clock warning

D13 does not use universal project clocks. A donor clock, progress track, faction clock, or downtime track must be mapped by function. It may become source-local, route to D10/D14/D15/D18, or quarantine/escalate if unsupported.

## Anti-drift controls

- Do not reduce every Project to one check.
- Do not make every Project a clock.
- Do not treat partial completion as failure by default.
- Do not invent generic complications without owner-file routing.
- Do not let acceleration bypass cost and risk.
- Do not let failure erase all state unless owner-file support exists.
