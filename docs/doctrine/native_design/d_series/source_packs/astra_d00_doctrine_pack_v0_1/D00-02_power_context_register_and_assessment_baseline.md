# D00-02 Power Context Register and Assessment Baseline

## Purpose

This file defines the baseline need for a Power Context Register and makes assessment/reconnaissance part of the core action loop.

## Power Context Register

The Power Context Register, or PCR, is the minimum context layer used to interpret action difficulty, risk, power meaning, and consequence pressure.

Minimum runtime fields:

```yaml
power_context_register:
  location_tier: string
  location_tags: []
  opposition_modifier: string
  domain_alignment: []
  hidden_cosmic_modifier: string
```

D00 establishes the need for these fields. D02 owns resolution use. D10 later records persistent place/world context.

## Location tier

Location tier is a broad signal of environmental pressure.

Example tiers may include mundane, elevated, charged, apex, transcendent, or source-local equivalents. D00 does not lock exact numeric bands; D02 may do that.

## Location tags

Location tags describe context that changes action meaning.

Examples:

- sanctified;
- corrupted;
- unstable;
- low-resource;
- high-resource;
- watched;
- contested;
- lawful;
- lawless;
- hidden;
- source-local;
- domain-aligned;
- domain-hostile.

## Opposition modifier

Opposition modifier records how local opposition changes pressure. It may represent relative tier, faction preparedness, environmental advantage, hidden defenses, social authority, or source-local pressure.

D02 owns resolution effect.

## Domain alignment

Domain alignment records whether the declared method aligns with, conflicts with, or is neutral to the location, opposition, route, Principle, object, faction law, or source-local context.

Domain alignment is not only elemental. It may involve death, law, oath, machine, spirit, territory, corruption, scarcity, lineage, route, or faction context.

## Hidden cosmic modifier

The hidden cosmic modifier is a backend-only pressure axis for rare fate/cosmic/Pneuma-like conditions. It should never become an ordinary player-visible luck score.

D01 owns Pneuma doctrine. D02 owns how hidden modifier affects resolution if used. D10 may record world-facing cosmic consequence only when it becomes visible.

## Assessment baseline

Assessment is a core action family. It rewards probing before commitment.

Assessment may attempt to learn:

- location tier;
- location tags;
- opposition pressure;
- approximate difficulty band;
- domain alignment;
- resource risks;
- hidden dangers;
- source-local constraints.

D00 requires assessment to exist. D02 owns resolution procedure. D05 owns competence/method if assessment depends on skills. D10 owns persistent information state when discovered knowledge matters.

## Visibility principle

Players should not always know all context. They should usually have enough visible or discoverable signal to make informed risk choices.

Visible context may include:

- apparent location tier;
- obvious tags;
- known law/faction constraints;
- visible hazards;
- public reputation;
- known object state.

Hidden context may include:

- concealed opposition;
- suppressed records;
- secret route effects;
- hidden Pneuma/cosmic modifier;
- source-local secrets.

## Acceptance criteria

PCR doctrine is satisfied when later files:

1. use context to affect resolution without arbitrary GM fiat;
2. keep hidden state lawful and discoverable where appropriate;
3. support assessment before commitment;
4. avoid forcing all context into visible UI;
5. preserve D01 Pneuma as backend-only.
