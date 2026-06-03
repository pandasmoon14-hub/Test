# D13-05 — Concurrent Projects, Contributors, Facilities, Materials, and Support Burden

Status: doctrine-pack / Phase 1 native doctrine continuation  
Layer: D13 operational procedure doctrine  
Owner: Astra Ascension doctrine architecture  
Generated: 2026-06-02  
Scope: downtime, projects, recovery, crafting, and interval-scale long-task procedure  

> This file is doctrine-facing and conversion-facing. It is not final runtime implementation, not final schema doctrine, not canon-sourcebook prose, and not live-play GM behavior. Runtime Gate B or later schema doctrine may formalize, replace, or narrow the record shapes included here.


## Core question

How does Astra prevent long-task work from becoming unlimited background progress?

D13-05 defines how many Projects can proceed at once, who can contribute, what facilities and materials do, when support assets matter, and how burden, upkeep, access, and interruption constrain progress.

This file does not define exact carrying capacity, prices, crafting values, facility construction rules, assistant statblocks, or faction labor economies. Those belong to D09, D10, D15, D17, D18, and later runtime/schema files.

## Project Load model

D13 uses **Project Load**, not universal Project slots.

A Project creates load when it occupies or requires:

- actor attention;
- time;
- safe location;
- materials;
- tools;
- facility capacity;
- assistant labor;
- specialist access;
- resource cost;
- object availability;
- social/institutional permission;
- legal exposure;
- maintenance burden;
- opportunity cost;
- world-state vulnerability.

A character, group, facility, faction, or platform may maintain multiple Projects only if each Project has clear capacity support.

Unsupported concurrency causes one or more of:

- blocked setup;
- delayed progress;
- increased cost;
- complication;
- Project split;
- Project pause;
- abandonment pressure;
- quarantine;
- escalation.

D13 does not define numeric load values by default. Later owner files or source-local systems may define them if justified.

## Contributor rule

Contributors can assist Projects only when they have a valid role.

Contributor roles:

- primary worker;
- assistant;
- mentor;
- specialist;
- crew;
- guard;
- sponsor;
- supplier;
- research aide;
- ritual participant;
- patient;
- test subject;
- faction representative;
- facility operator;
- companion / summon;
- automated system;
- source-local contributor.

Contributors may provide:

- method support;
- access permission;
- labor;
- protection;
- materials;
- knowledge;
- facility operation;
- social cover;
- faction authorization;
- risk absorption;
- progress acceleration;
- stability.

Contributors may also create:

- cost;
- obligation;
- scrutiny;
- coordination burden;
- safety risk;
- loyalty risk;
- information leak;
- injury exposure;
- facility strain;
- source-local complication.

D13 rejects “assistant equals free bonus” as default law.

## Facility rule

A Facility is any place or infrastructure that enables, improves, stabilizes, or constrains a Project.

Facility examples:

- workshop;
- forge;
- laboratory;
- library;
- clinic;
- meditation chamber;
- ritual site;
- shipyard;
- dock;
- garage;
- hangar;
- sect training hall;
- guild office;
- data vault;
- safehouse;
- salvage bay;
- hospital venue;
- court chamber;
- source-local site.

D13 classifies facilities by function, not donor label.

Facility functions may include:

- safe recovery;
- controlled experimentation;
- fabrication;
- repair;
- storage;
- containment;
- training;
- research access;
- social legitimacy;
- ritual anchoring;
- platform service;
- material processing;
- legal authorization;
- hidden operation.

Facility status may be:

- available;
- adequate;
- strained;
- unsafe;
- occupied;
- damaged;
- source-local;
- unavailable;
- protected hidden;
- unknown.

D09/D10/D15/D17/D18 own the actual facility record, ownership, legality, cost, faction control, and long-term state.

## Materials and support assets

Materials are not generic currency unless D17 later defines them that way.

Material categories include:

- common material;
- scarce material;
- specialized component;
- relic fragment;
- cultivation resource;
- biological sample;
- salvaged part;
- platform component;
- fuel / charge medium;
- data / information resource;
- social favor;
- legal permit;
- faction authorization;
- source-local material.

Support assets may include tools, kits, vehicles, platforms, assistants, licenses, access tags, facilities, or stored resources.

D13 records materials and support assets as requirements, commitments, risks, or outputs. D09/D17 own object and economy state.

## Maintenance and upkeep

Maintenance is a first-class Project family. Some Projects prevent decay, failure, debt, exposure, injury relapse, object degradation, social collapse, faction deterioration, or platform malfunction.

Maintenance may apply to:

- actor recovery;
- implants / relics;
- ships / vehicles / mechs;
- facilities;
- companions / summons;
- social relationships;
- faction obligations;
- legal status;
- resource stockpiles;
- domain stability;
- source-local burdens.

D13 owns the interval and burden procedure. D17 and D18 later own broader support burden, economy pressure, and long-horizon state aging.

## Interruption and abandonment

A Project may be interrupted by:

- active scene trigger;
- resource loss;
- facility loss;
- assistant withdrawal;
- injury;
- travel;
- attack;
- legal action;
- faction pressure;
- hidden threat;
- material spoilage;
- object instability;
- relationship rupture;
- campaign time skip;
- source-local event.

Interruption outcomes:

- `pause_without_loss`
- `pause_with_decay`
- `delay`
- `cost_increase`
- `progress_loss`
- `requirement_change`
- `complication_added`
- `active_scene_triggered`
- `project_split_required`
- `project_abandoned`
- `project_quarantined`
- `project_escalated`

Abandoned Projects must record what is lost, preserved, exposed, recoverable, archived, or converted into unresolved pressure.

## Examples

### Supported concurrency

A character maintains a long-term research Project requiring weekly check-ins while a workshop handles a repair Project under a specialist. The two Projects can coexist if the actor's attention, facility use, and materials do not conflict.

### Unsupported concurrency

A character attempts severe recovery, intensive training, relic crafting, faction diplomacy, and ship repair during the same short interval. D13 should block, delay, split, complicate, or require support burden rather than allow all Projects to progress freely.

## Anti-drift controls

- Do not create universal project-slot counts.
- Do not ignore attention, facility, material, legal, social, or maintenance burden.
- Do not let support assets provide generic bonuses without function.
- Do not let abandonment erase evidence of unresolved pressure.
