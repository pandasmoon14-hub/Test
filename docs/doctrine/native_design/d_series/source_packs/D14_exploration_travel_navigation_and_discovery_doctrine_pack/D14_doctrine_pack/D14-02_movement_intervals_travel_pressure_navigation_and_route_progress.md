# D14-02 — Movement Intervals, Travel Pressure, Navigation, and Route Progress

Status: doctrine-draft / Phase 1 native doctrine continuation  
Version: `0.1.0-d14-generated`  
Generated: 2026-06-02  
Layer: D14 operational procedure doctrine  
Owner: Astra doctrine architecture / exploration and discovery procedure layer

## Purpose

This file defines what happens during travel or exploration after intent, posture, route/area, known-state, and owner-file risks are identified.

D14 uses flexible **Travel / Exploration Intervals**, not universal travel turns.

## Travel / Exploration Interval

An interval is a bounded unit of movement or exploration during which posture, route, known-state, environmental pressure, and external risk can change. It may represent a momentary approach, scene segment, site segment, district leg, wilderness leg, watch period, ship/platform vector, stealth movement segment, site survey pass, realm crossing stage, search sweep, or source-local travel turn.

## Seven interval checkpoints

```text
1. Interval scale checkpoint
2. Navigation / orientation checkpoint
3. Posture pressure checkpoint
4. Environmental PCR checkpoint
5. Resource / exposure checkpoint
6. Discovery / hazard / encounter checkpoint
7. Progress and transition checkpoint
```

## Interval scale

The interval scale is context-driven. D14 does not set universal durations. A donor watch, turn, day, jump, phase, or segment is not Astra law unless source-local or owner-file supported.

## Navigation / orientation

D14 checks navigation only when direction, route, position, pursuit, map accuracy, or destination sense is uncertain, contested, hidden, distorted, false, dangerous, pursuit-sensitive, or otherwise risky. If there is no uncertainty, no roll is required. D02 owns resolution. D05 owns method relevance.

## Posture pressure

The declared posture modifies exposure, visibility, blind spots, delay, discovery opportunities, and owner-file handoffs. It is not a generic bonus system.

## Environmental PCR

Environmental PCR may include location_tier, location_tags, domain_alignment, opposition_modifier, hidden_cosmic_modifier, environmental_pressure, and source_local_modifiers. D14 uses PCR to shape route difficulty, risk, distortion, visibility, cost, domain alignment, and hidden pressure. D02 owns resolution, D10 owns truth, D11 owns presentation, and hidden Pneuma remains protected.

## Resource / exposure

Travel may create fatigue, supplies, fuel, power drain, heat/strain, ritual stability, equipment wear, companion burden, platform maintenance, injury aggravation, corruption exposure, legal scrutiny, faction trace, weather/terrain exposure, or source-local attrition. D14 identifies triggers. D03, D07, D08, D09, D10, D17, and D18 own actual state changes.

## Discovery / hazard / encounter

Each interval may produce route progress, map-state improvement, landmarks, clues, resource signs, hidden route hints, hazard exposure, environmental shifts, ambush risk, patrol contact, faction presence, object/salvage opportunities, site entrance, lost route, false route confirmation, pressure escalation, or no notable event.

Discovery, hazard, or encounter triggers require support from route pressure, posture, PCR, owner-file state, source-local procedure, prior state, or scenario design. Random encounters are not default D14 law.

## Progress states

Route progress states include advanced, advanced_with_cost, advanced_with_discovery, advanced_with_exposure, delayed, misdirected, lost, blocked, hazard_triggered, encounter_triggered, site_entry_triggered, map_state_updated, pressure_escalated, transitioned, quarantined, and escalated.

## Anti-drift rules

Do not use fixed travel turns by default. Do not check navigation every interval unless risk supports it. Do not roll random encounters by default. Do not let PCR expose hidden cosmic truth. Do not let D14 define resource loss, harm, fuel economy, weather damage, or encounter math.
