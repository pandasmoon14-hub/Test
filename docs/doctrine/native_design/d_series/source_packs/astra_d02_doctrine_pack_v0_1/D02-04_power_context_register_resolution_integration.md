# D02-04 Power Context Register Resolution Integration

## Purpose

This file defines how the Power Context Register affects d20 resolution.

## PCR fields

Minimum PCR fields:

```yaml
power_context_register:
  location_tier: string
  location_tags: []
  opposition_modifier: string
  domain_alignment: []
  hidden_cosmic_modifier: string
```

D00 establishes PCR need. D02 uses PCR in resolution. D10 may record persistent world-state that feeds PCR.

## PCR-to-DN bands

| PCR tier | DN band |
|---|---|
| Mundane | 5–12 |
| Elevated | 8–16 |
| Charged | 12–20 |
| Apex | 16–24 |
| Transcendent | 20–28 |
| Mythic / Cosmic / Source-local | 24–32+ |

PCR tier is not the same as character level or donor challenge rating. It is contextual pressure.

## Location tags

Location tags can alter DN, advantage/disadvantage, cost, consequence severity, assessment output, or owner-file routing.

Examples:

- corrupted;
- sanctified;
- unstable;
- depleted;
- resource-rich;
- watched;
- contested;
- lawful;
- lawless;
- domain-aligned;
- domain-hostile;
- source-local.

## Opposition modifier

Opposition can be static or active.

Opposition may:

- set a DN;
- shift DN;
- trigger active contested check;
- impose disadvantage;
- increase consequence severity;
- require defense/resistance check;
- create D10 attention or memory.

## Domain alignment

Domain alignment can express compatibility or friction between action method and context.

Favorable alignment may:

- lower DN;
- grant advantage;
- reduce cost;
- reduce consequence severity;
- improve assessment quality;
- improve progress units.

Hostile alignment may:

- raise DN;
- impose disadvantage;
- increase cost;
- worsen consequence severity;
- trigger D07/D08/D10 pressure;
- produce source-local restriction.

Domain alignment may involve elements, death, law, machine, spirit, oath, route, faction, object, territory, corruption, scarcity, lineage, or source-local metaphysics.

## Hidden cosmic modifier

Hidden cosmic/Pneuma-style pressure is backend-only.

It may:

- subtly shift DN;
- affect consequence severity;
- alter coincidence or timing;
- influence relic resonance;
- create D10 world-facing myth only after surfacing.

It must not be displayed as ordinary luck, spendable currency, or player-visible modifier.

## PCR and impossible actions

A high PCR tier may indicate that ordinary methods cannot work. In that case, D02 should require a condition, resource, route, object, advancement threshold, or assessment discovery rather than assigning an arbitrarily high DN.

## PCR and consequence

PCR can affect not only success probability but also what failure means.

Examples:

- failed fire Technique in fuel-rich station may trigger D03/D07/D10 pressure;
- failed undead-form use in sanctified zone may trigger D07/D08/D10 pressure;
- failed relic use in sacred site may trigger D09/D10 pressure;
- failed stealth in watched district may trigger D10 information/law pressure.

## Acceptance criteria

A PCR resolution ruling is valid when it:

1. uses PCR as a real resolution input;
2. does not reveal hidden Pneuma as ordinary stat;
3. distinguishes DN shifts from consequence shifts;
4. respects domain alignment;
5. routes persistent effects to owner files.
