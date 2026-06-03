# D15-09 — Integration Checklists, DDR Register, and Acceptance Criteria

Status: doctrine-draft / native doctrine foundation continuation  
Version: `v0.1.0-d15-doctrine-pack`  
Generated: 2026-06-02  
Layer: D15 native operational doctrine  
Owner: Astra Ascension doctrine architecture  
Primary downstream users: conversion intake, canon review, future runtime Gate B, future play-facing adapter design  

Authority posture: current Astra doctrine wins over donor assumptions. D15 is procedure doctrine, not canon sourcebook prose, not conversion output, not final runtime schema, and not live-play GM behavior.


## 1. Purpose

This file provides the final D15 control layer: integration checks, anti-drift rules, source-local boundaries, escalation triggers, DDR register, and acceptance criteria.

## 2. Owner-file integration checklist

### D10 handoff checklist

D15 must hand off to D10 when an Operation affects:

- world-state;
- relationship state;
- law record;
- public belief;
- rumor;
- hidden truth;
- faction record;
- standing record as stored state;
- unresolved pressure queue;
- domain or territory state;
- source-local institutional fact.

D15 owns procedure. D10 owns stored truth and memory.

### D12 handoff checklist

D15 must hand off to D12 when an Operation becomes immediate scene procedure: confrontation, negotiation, trial, debate, chase, violence, public address, ambush, social conflict, or structured exchange.

### D13 handoff checklist

D15 must hand off to D13 when an Operation requires interval-scale work: influence campaign, reputation repair, recruitment, legal preparation, treaty work, propaganda, organization growth, domain preparation, or institutional support Project.

### D16 handoff checklist

D15 must hand off to D16 when institutional pressure creates opposition, encounter, hazard, patrol, raid, security force, war party, monster deployment, or threat construction.

### D17 handoff checklist

D15 must hand off to D17 when an Operation involves acquisition, ownership, value, payment, market access, license cost, requisition, debt value, bribe, reward, salvage claim, supply, or economy procedure.

### D18 handoff checklist

D15 must hand off to D18 when an Operation affects arcs, seasons, long-horizon domain evolution, player-organization aging, state pruning, campaign-scale war posture, settlement evolution, or generational continuity.

### D04/D05/D06 handoff checklist

D15 must hand off to D04/D05/D06 when patronage, rank, guild/sect access, recruitment, training, sponsorship, or institutional membership affects advancement gates, proof, competency, methods, access posture, Techniques, Principles, routes, or domain expression.

## 3. Source-local boundary checklist

A source-local institutional system must record:

- donor source or converted-source boundary;
- procedure retained;
- why it is useful locally;
- why it is unsafe to generalize;
- rejected donor assumptions;
- owner-file dependencies;
- lawful outcome;
- conditions for future escalation or canon candidate review.

Source-local systems do not become Astra law through repetition alone.

## 4. Escalation triggers

Escalate when repeated or high-impact pressure shows missing doctrine that cannot be safely normalized or retained locally.

Escalation examples:

- formal heat/scrutiny pressure beyond current D10/D15 readiness;
- faction-turn or campaign-season interface with D18;
- sect/guild contribution systems requiring access and obligation refinement with D04/D05/D17;
- player-organization capacity and benefit-boundary gaps;
- domain/kingdom long-horizon evolution needing D18;
- public-opinion systems requiring richer D10/D11 public belief and rumor-state doctrine;
- law systems requiring jurisdiction and enforcement doctrine beyond source-local treatment;
- mass conflict requiring D16/D18 coordination.

## 5. Quarantine triggers

Quarantine institutional systems when extraction damage, unclear mutation, missing source-local boundary, unsupported social math, unsupported reputation/heat/domain/economy/law/social-combat/mass-conflict/public-belief/organization-benefit assumptions, or missing owner-file support prevents safe mapping.

## 6. Anti-drift rules

- Do not turn factions into giant NPCs.
- Do not reduce standing to one reputation score.
- Do not make faction clocks, fronts, heat tracks, or kingdom turns universal.
- Do not make donor law codes Astra moral law.
- Do not treat public belief as actual truth.
- Do not let contacts, rank, guild access, patronage, or organization membership become free resources or powers.
- Do not let sect contribution, renown, or rank bypass D04/D05/D06 access or advancement doctrine.
- Do not let player organizations become free capability bundles.
- Do not let domain control become D06 domain expression.
- Do not let D15 become arbitrary faction AI.
- Do not let D15 become D17 economy doctrine, D16 encounter/war construction, or D18 campaign pacing.
- Do not let source-local institutional systems become Astra law through repetition alone.
- Do not treat not-final-schema record shapes as runtime implementation.

## 7. Hidden-state and public-belief checklist

D15 may alter public belief, rumor pressure, standing, and scrutiny. It must not turn public belief into actual truth.

D10 owns hidden truth. D11 owns presentation. D15 may record that an Operation threatens, obscures, exposes, suppresses, distorts, or publicizes information, but it does not reveal protected truth by itself.

## 8. DDR register

| Decision block | Locked architecture | Key rejection |
|---|---|---|
| D15-00 | Standing–Pressure–Operation Architecture | universal faction turns / arbitrary faction AI |
| D15-01 | operational object anatomy | faction statblocks / clock-first objects |
| D15-02 | eight-checkpoint Operation setup | faction action by fiat |
| D15-03 | Operation Outcome and Pressure Routing | binary check or clock-only resolution |
| D15-04 | Operation Profile model | full law/economy/domain subsystems inside D15 |
| D15-05 | qualitative capacity + Operation Load | fixed faction action slots |
| D15-06 | functional donor institutional mapping ladder | fixed equivalency table or preserve-by-default |
| D15-07 | not-final-schema record pack | final runtime/faction schema |

## 9. D15 acceptance criteria

D15 is acceptable only if it can:

- create an Operation from a lawful trigger;
- identify initiator, target, goal, scale, method, leverage, cost, and risk;
- represent standing as multi-axis relational posture;
- operate on D10-recorded unresolved pressure without replacing D10;
- track obligations and claims as first-class procedural objects;
- resolve Operations through outcome states rather than binary success/failure or universal clocks;
- route social, institutional, legal, factional, access, domain, and relationship outcomes to owner files;
- support relationship repair/degradation, debts/favors, access/licensing, diplomacy/treaties, law/sanctions, influence/rumor, territorial/domain claims, patronage/recruitment, retaliation/protection, and player organization growth;
- constrain factions and institutions through qualitative capacity and Operation Load;
- support pressure decay and escalation without arbitrary narration;
- support player organizations without free capability bundles;
- map donor institutional procedures by function, not label;
- preserve bounded source-local institutional systems;
- quarantine unsupported institutional systems;
- escalate repeated or high-impact missing doctrine;
- keep D15 domain control separate from D06 domain expression;
- keep public belief separate from actual truth;
- keep records clearly marked as not final schema.

## 10. Generation risk-fix embedding map

| Risk | Embedded locations |
|---|---|
| arbitrary faction AI | D15-00, D15-02, D15-05, D15-09 |
| factions as giant NPCs | D15-00, D15-01, D15-07, D15-09 |
| standing as single score | D15-01, D15-03, D15-07, D15-09 |
| clocks/tracks universalized | D15-01, D15-03, D15-06, D15-09 |
| D10 ownership stolen | D15-00, D15-03, D15-07, D15-09 |
| public belief as truth | D15-03, D15-04, D15-09 |
| donor law codes imported | D15-00, D15-04, D15-06, D15-09 |
| D15 domain vs D06 domain blur | D15-00, D15-01, D15-04, D15-07, D15-09 |
| rank/patronage bypasses advancement | D15-04, D15-06, D15-09 |
| player organizations as free bundles | D15-04, D15-05, D15-07, D15-09 |
| obligations collapse into economy | D15-01, D15-03, D15-04, D15-07, D15-09 |
| capacity becomes faction slots | D15-05, D15-07, D15-09 |
| D17 economy stolen | D15-00, D15-03, D15-04, D15-07, D15-09 |
| D18 campaign pacing stolen | D15-00, D15-04, D15-05, D15-09 |
| D16 encounter/war stolen | D15-04, D15-05, D15-09 |
| source-local systems generalize | D15-06, D15-07, D15-09 |
| records treated as runtime schemas | D15-07, D15_pack_manifest.json, D15-09 |
