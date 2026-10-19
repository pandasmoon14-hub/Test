# Water domain — capability and expansion register

Owner directive: Cam approved #544 and requested tracking **when and what should add to and expand the water domain**. This register is part of the existing decision/continuity surface. It does not create a semantic owner, authorize future mechanics, or ratify setting facts. Scope: Runtime; Headquarters excluded.

## Current bounded foundation

Approved: #544; implemented candidate: `persistent_world_water_cleaning.py`, `myravant_water_application.py`, `myravant_tarrow_water.py`; see `tarrow_water_1_contract.md`. Certification and merge status are recorded in #544 and its implementation PR. A code path is not certification.

The foundation represents finite whole-unit water quantities, declared vessel/absorbent capacity, adhered residue, exact rational suspended residue, wetness derived from retained water, and qualified transfers/washing. Water and residue follow object identity through existing placement/custody/storage. Rinsing exchanges residue with the bath; wringing leaves adhered dirt. No untracked disposal sink exists. Separate versioned journal replay reconstructs committed operations.

The neutral starting supply and capacities are development profiles. They neither make the channel an unlimited source nor define native water quality, health or material laws. The first package has one mobile residue class and an explicit uniform-mixing abstraction; suspended residue does not displace modeled water volume. Appearance, remembered history and actual condition remain distinct.

## When to revisit this register

At planning for any package involving liquids, cleaning, material alteration, storage, exposure, time, terrain, livelihoods, infrastructure, living beings or extraordinary effects:

1. Identify the desired player consequence and consult affected rows below before implementing an isolated substitute.
2. Reuse current owner procedures where their meanings suffice. Record the actual unsupported attempt or scenario that activates an extension; calendar age alone is not a trigger.
3. Resolve the extension's authority, state, causal inputs and information boundaries. Native decisions are retrieved from their authoritative records, not invented from this register.
4. Define migration/replay treatment for old campaigns and add integrated evidence before changing semantics.
5. Update this register and #544/parent #540 with implemented coverage, test evidence, remaining limits and revised next dependency. Do not mark a row implemented solely because an object was added.

## Dependency-ordered expansion candidates

Except for the explicitly selected drying extension described below, these rows remain **deferred / not yet authorized**. Priority is conditional on a demonstrated trigger, not automatic activation.

| Order / capability | Trigger: when it becomes necessary | What to add | Ownership and prerequisite | Evidence needed before admission |
| --- | --- | --- | --- | --- |
| 1 — Spills, puddles and collection | A player intentionally pours onto terrain, tips a vessel, or needs to recover spilled water | Declared receiving surface/location reservoir, retained identity and quantities, spill/recovery transitions; measured residue goes somewhere | RT-010 material contents; AFQR-18 receiving placement; AFQR-19 method opportunity. Do not invent slip/damage effects | Partial spill and recovery conserve both materials; inaccessible surfaces refuse; restart preserves the puddle; no invisible deletion sink |
| 1 — Wet transfer and absorption | Wrapping, wiping a wet surface, soaking cargo or moving wet cloth is expected to affect another object | Profile-specific absorption/retention and contact transfers, separate surface water where needed | RT-010; qualified contact/access through AFQR-19/20. Neither adjacency nor containment alone causes transfer | Two materials behave differently; saturation, contact removal, wet packing and replay; no water duplication |
| 2 — Drying and evaporation | Waiting, ventilation, shelter or repeated return should change wetness | Explicit timed process with rate/profile/environment witnesses and a tracked environmental destination; interruption/catch-up policy | RT-010 material condition plus WORLD-1 time and relevant environmental authority. Never use wall-clock time or turn count by convenience | Equivalent elapsed histories replay identically; no repeated catch-up; acknowledged water accounting includes evaporated water; indoor/outdoor contrast |
| 2 — Liquid-safe transport and closures | A journey needs tipping, sealing, leakage or movement-sensitive retention | Vessel opening/orientation/route opportunity profiles and explicit retention/leak transitions | Existing closure/custody/displacement owners plus RT-010; geometry/load qualification as needed | Closed/open and carried/displaced contrasts, nested cargo, unsupported vessel shapes, no surprise universal spill law |
| 3 — Flow, channels and drainage | Crossing works, drains, runoff or redirected water must have material consequences | Connected reservoirs/routes, bounded flow rules and explicit source/sink accounting, obstacles and diversion | AFQR-18 topology; RT-010 material stocks; timed/environmental authority; approved infrastructure profiles | Diversion conserves water, blockage changes flow lawfully, upstream/downstream outcomes persist, simultaneous update order is explicit |
| 3 — Weather supply and surface runoff | Rain, flooding, collection or shelter should replenish or redistribute water | Qualified precipitation input, catchments, bounded runoff, drainage and local/offscreen process policy | Environmental/time owners and native regional process bindings. Finite local buckets do not authorize climate simulation | Input/output budgets, shelter contrast, leave/return equivalence, no duplicate precipitation during restore |
| 4 — Filtration, settling and multiple constituents | Players separate silt, filter water, dissolve substances or compare different residues | Distinct constituents and phases, separation/retention profiles and processing yields | RT-010 material transformation; approved constituent properties; thermal/chemical rules only where supplied | Filter clogging/retained matter, partial processing, exact constituent accounting, dirty receiving tools, no magical purification |
| 4 — Temperature, ice, melting and boiling | Heat/cold or freezing affects a player task | Thermal state, energy/process inputs, phase transition quantities, vessel compatibility | Relevant environmental/material authorities; approved thermal profiles. Harm remains outside material ownership | Freeze/thaw and boil/condense budgets, interrupted heating, conservative migration and replay; no free energy or matter |
| 5 — Quality, drinking and biological effects | A being drinks, needs water, becomes exposed or cultivates living material | Quality evidence distinct from true composition, intake destination, embodiment-specific effects, exposure/needs contracts | Canon/embodiment/native rules and applicable harm/resource owners; AFQR-20/knowledge separation. Dirty appearance is not disease | Different embodiments, uncertain quality, consent/opportunity, genuine consumption accounting and persistent consequences |
| 5 — Water as load, pressure or force | Buoyancy, pressure, swimming, lifting, erosion or machinery is necessary | Qualified geometry/load/force mechanism with explicit cross-owner outputs | Spatial/embodiment/environment and consequence owners; no inference from liters alone | Contrasting shapes/routes, stable support and failure behavior, actor constraints, deterministic outcomes and save continuity |
| On demand — Water-driven work and institutions | Washing services, irrigation, supply shortages or NPC tasks need actual activity | Bounded consumption/reservation/work processes and voluntary actor participation using demonstrated material state | Existing actors/work/time/custody authorities; native permissions/economy only if approved | A second actor competes for actual supply, reservations expire lawfully, tasks resume after absence; no blanket consent or stock routine copying |
| On demand — Extraordinary creation/control | A native ability creates, transforms or controls water | Explicit ability provenance, costs/limits, new source/sink accounting and material handoffs | Canon approval, ability/resource authorities and RT-010; no material reducer invents powers | Ability-specific limits, replayed committed randomness where applicable, ordinary water interoperability, hidden knowledge boundaries |
| Scale trigger — Larger histories/regions | Measured save/replay or many-reservoir cost obstructs a real campaign | Equivalent snapshots/compaction and bounded local/offscreen resolution | Existing persistence, commitment, version and scheduling owners; measure before changing architecture | Full journal versus compacted equivalence, fault recovery, migration, no omitted state families or changed physical semantics |

## Selected extension — approved #546, implementation candidate

Cam approved the combined time/environment/work contract #546. Its current candidate implements drying for the declared Cleaning Cloth in the separate `tarrow-time` profile. This is **implemented candidate coverage, not certification or merge evidence**. The original `tarrow-water` profile retains its earlier meanings.

The selected extension reuses WORLD-1 logical intervals and AFQR-17 environmental authority, with RT-010 material handoffs. Exact fractional drying credit accumulates under explicit exposure rates; whole water units transfer into a per-position evaporated-water accounting compartment. A closed container suspends exposure. On loss of the last retained water unit, suspended residue becomes a separate deposit on the absorbent; it is conserved even when ordinary adhered-residue capacity is already occupied. Qualified rinsing or collection can recover deposited residue. The accounting compartment does not implement humidity, atmospheric transport or recoverable condensation.

Physical mutations consume one declared development interval; observations and work declarations do not. Passive evolution precedes the active contribution, which requalifies after that interval. A contribution losing its opportunity can therefore be interrupted after elapsed time and passive consequences have committed. Bounded waits and work requests commit separately durable intervals. Versioned profile/journal replay reconstructs time, drying credit, deposited residue, environmental water, work lifecycle and physical traces.

The trigger was the combined environmental/time package, so drying was deliberately selected before the provisionally earlier spills/contact-transfer rows. Those rows are still unsupported. Current drying admits one absorbent and two exposure-rate profiles with one declared condition boundary; it does not implement generic ventilation, weather, spontaneous dampness, Screen Cloth absorption, vessel evaporation, offscreen catch-up or wall-clock progression.

Required certification remains: elapsed-history/restart equivalence, containment and exposure contrasts, material accounting including deposited residue, post-passive interruption, interval durability failures and integrated installed-client journeys. Record observed results in the implementation PR before upgrading this status. See `tarrow_environment_depth_closure_assessment.md`; #540 remains open.

## Next selection rule

After the current candidate is certified, select the highest-value still-triggered row alongside the next coherent environmental/material package. Spills and wet transfer remain likely integrations because they extend the conservation model, but require a concrete play need. Drying has an approved bounded environmental/time contract under #546; further absorbents, exposure effects or atmospheric behavior require explicit profile/semantic extensions. Channel flow should be selected when crossing/infrastructure work needs it. Native ingestion, extraordinary abilities and health remain native-rule dependencies, not generic water completeness requirements.

No row is a promise that a specific natural-language action currently executes. Preserve unsupported intentions and truthful limits in player feedback. Keep old water checkpoints under their original profile/rules meanings unless an explicit versioned migration is validated.

## Actor participation integration — #548 candidate

The opt-in actor binding exercises the existing finite stocks, wet cloth,
brush capacity, soak, rinse, collection, deposits and exposure through actual
performer custody. Each due actor can perform at most one physical preparation
or contribution per shared WORLD-1 interval. Ordered contention requalifies
stocks after earlier player/actor changes; acceptance creates no reservation.

Preparation includes deposited residue when evaluating capacity and chooses a
currently qualified declared source/destination. A movement or handoff changes
later exposure through actual placement; it never grants new transfer, spill or
flow rules. Conservation includes the existing environmental evaporation ledger.
Old water/time bindings retain their meanings. Certification for this candidate
is recorded separately in the actor review; this entry does not mark it merged.

Next water triggers remain practical: spills/recovery when work pours onto
terrain; contact absorption when wet cargo must affect another material; safe
closures when transport requires retention/leakage; bounded flow when crossing
infrastructure work actually depends on it. Actor routines alone authorize none
of these extensions, and the existing receiving-profile and conservation gates
still apply.
