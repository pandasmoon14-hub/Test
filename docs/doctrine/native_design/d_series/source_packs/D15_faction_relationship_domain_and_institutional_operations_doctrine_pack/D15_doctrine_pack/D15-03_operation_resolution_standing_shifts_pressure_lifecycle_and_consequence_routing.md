# D15-03 — Operation Resolution, Standing Shifts, Pressure Lifecycle, and Consequence Routing

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file defines how Operations resolve after setup. It governs Operation outcomes, standing shifts, pressure movement, obligation and claim changes, access outcomes, and consequence routing.

D15 does not use binary success/failure or universal faction clocks as its default resolution model.

## 2. Resolution model

D15 uses an Operation Outcome and Pressure Routing Model.

An Operation may resolve through:

- D12 scene result;
- D13 Project result;
- D15 operation interval;
- D17 acquisition / requisition outcome;
- D18 campaign-scale handoff;
- source-local procedure;
- quarantine or escalation.

D15 does not require one universal Operation roll. It asks which procedure the Operation entered and routes the outcome back into standing, pressure, obligation, claim, access, treaty, law, territory, or domain posture.

## 3. Operation outcome states

Outcome states include:

- accepted;
- accepted_with_cost;
- partially_accepted;
- contested;
- delayed;
- countered;
- escalated;
- deescalated;
- converted_to_project;
- converted_to_scene;
- converted_to_conflict;
- settled;
- settled_with_debt;
- claim_recognized;
- claim_rejected;
- claim_contested;
- standing_improved;
- standing_damaged;
- access_opened;
- access_restricted;
- obligation_created;
- obligation_reduced;
- obligation_transferred;
- pressure_decayed;
- pressure_escalated;
- pressure_surfaced;
- failed;
- failed_with_consequence;
- quarantined;
- escalated_owner_file_problem;
- source_local_result.

These are procedural states. D10 records the resulting world-state. D11 presents it.

## 4. Standing shifts

Standing changes only when the Operation outcome justifies a state delta.

Standing shifts may be:

- improved;
- damaged;
- complicated;
- formalized;
- publicized;
- hidden;
- split_by_subgroup;
- conditional;
- temporary;
- revoked;
- transferred;
- source-local.

Examples:

- A guild publicly grants access but privately increases scrutiny.
- A sect elder accepts repayment but a rival faction treats the act as insult.
- A corporation opens market access only under license.
- A city drops charges but records the party as watched.
- A clan alliance improves standing with one branch and damages it with another.

D15 must support split standing. One faction is not always socially uniform.

## 5. Pressure lifecycle resolution

Pressure may move through these states:

- latent;
- active;
- escalating;
- decaying;
- suppressed;
- surfaced;
- transferred;
- converted_to_operation;
- converted_to_scene;
- converted_to_project;
- converted_to_conflict;
- resolved;
- retired;
- source-local.

Operation outcomes move pressure. A debt settlement may resolve one pressure but create a new obligation. A failed apology may escalate rumor pressure. A treaty may suppress conflict pressure without resolving underlying claims. A faction favor may transfer pressure from the party to a patron. A law petition may convert hidden scrutiny into public legal action.

## 6. Obligation and claim resolution

Obligations and claims do not disappear into flavor. They carry procedural states.

Obligation states:

- owed;
- invoked;
- partially_paid;
- paid;
- deferred;
- contested;
- transferred;
- forgiven;
- defaulted;
- escalated;
- retired;
- source-local.

Claim states:

- asserted;
- recognized;
- contested;
- rejected;
- enforced;
- suspended;
- transferred;
- settled;
- violated;
- escalated;
- retired;
- source-local.

## 7. Access and permission outcomes

Operations often affect access.

Access outcomes may include:

- access_granted;
- access_granted_with_limit;
- access_denied;
- access_revoked;
- license_required;
- sponsor_required;
- debt_required;
- standing_required;
- restricted_access;
- black_market_access;
- temporary_access;
- source-local_access.

D15 may record the operation of access. D17 owns acquisition, market, payment, requisition, license cost, and legality procedure where relevant. D10 stores the resulting state.

## 8. Partial outcomes

D15 treats partial outcomes as meaningful institutional movement.

Partial success may produce access with scrutiny, debt reduced but not cleared, rumor slowed but not killed, treaty accepted by one faction branch, legal charge deferred but not dismissed, standing improved privately but not publicly, domain claim recognized temporarily, favor granted with new obligation, project approved under oversight, or resource access granted with restriction.

Partial outcomes are critical for long campaigns because they prevent social play from becoming total success or total failure.

## 9. Consequence routing

D15 routes outcomes to owner files:

- D02 for contested resolution or uncertainty;
- D05 for method and competency implications;
- D07 for harm, coercion, sanctions with injury or condition consequences;
- D08 for actor/personhood issues when institutions affect persons, companions, or groups;
- D09 for objects, relics, platforms, facilities, or controlled assets;
- D10 for world-state, relationships, law, public belief, rumors, hidden truth, pressure queues;
- D11 for player-facing / GM-facing presentation and hidden-state boundaries;
- D12 for immediate scene, confrontation, chase, debate, conflict, or structured exchange;
- D13 for influence campaigns, reputation repair, treaty work, recruitment, institutional preparation;
- D17 for wealth, requisition, market access, licenses, bribes, debts, rewards, salvage claims;
- D18 for campaign-scale wars, seasons, domain evolution, state aging, arc pressure.

## 10. Anti-drift controls

- Public belief is not actual truth. D10 owns actual truth.
- D15 does not define generic consequences for all Operations.
- D15 does not use clocks as default operation resolution.
- D15 does not decide final harm, object, economy, hidden truth, scene cadence, campaign pacing, or runtime state by itself.

## 11. Acceptance criteria

This file is acceptable if D15 can resolve Operations through outcome states, move standing and pressure, track obligations/claims, route access outcomes, and hand off all non-D15 consequences to their owners.
