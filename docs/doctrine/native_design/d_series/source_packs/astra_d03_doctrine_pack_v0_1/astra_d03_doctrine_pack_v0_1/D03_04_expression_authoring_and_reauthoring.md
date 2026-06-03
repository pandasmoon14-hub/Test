# Astra Ascension — D03-04 Expression Authoring and Re-authoring

Status: design-draft / accepted architecture  
Layer: Native Design Phase / D03  
File ID: D03-04  
Version: v0.1  
Date: 2026-05-29

---

## 1. Purpose

This file defines Expression authoring and re-authoring.

Astra must validate converted donor abilities, canonical Astra abilities, player-created abilities, modified abilities, hybrid abilities, cultural techniques, rituals, spells, arts, and custom effects through the same structural grammar.

---

## 2. Core terms

### Expression

Expression is the doctrine-neutral term for a functional power/effect pattern.

Examples:

- fire projection;
- healing pulse;
- ward;
- tracking strike;
- illusion;
- binding;
- assessment scan;
- material control;
- aura suppression;
- memory projection;
- network override;
- blood seal;
- summoning call;
- banishing rite.

### Local term

A culture, path, faction, source, profession, or character may call an Expression by another term:

- spell;
- technique;
- rite;
- art;
- formula;
- working;
- maneuver;
- protocol;
- craft;
- prayer;
- vow;
- dao-working;
- discipline;
- charm;
- pattern.

Local terms do not override doctrine.

---

## 3. Expression vs. Power Economy

An Expression is what the effect does.

A Power Economy is how the effect is powered, shaped, paid for, recovered, and risked.

The same Expression family may be authored through different Power Economies.

Example: fire projection may be authored through Mistra, Zi, Calora, Scrypta, Scintilla, Vitia, or other routes when compatibility, training, cost, and method support it.

---

## 4. Governed re-authoring

Governed Re-authoring is accepted as D03 doctrine.

A re-authored Expression must:

1. preserve a recognizable Expression core;
2. declare the new economy route;
3. pass compatibility checks;
4. satisfy training/access requirements;
5. translate cost and risk;
6. change at least one mechanical vector;
7. update stability state;
8. become a versioned Expression record.

Re-authoring is not cosmetic renaming.

---

## 5. Mechanical vectors

A re-authored Expression must change at least one vector.

| Vector | What may change |
|---|---|
| Cost | Different partition, strain, reserve, overdraw, or recovery burden. |
| Targeting | Single target, area, tracking, touch, mark, line, aura, node, material, spirit. |
| Range | Personal, touch, close, ranged, remote, line of sight, sympathetic, domain-bound. |
| Timing | Immediate, sustained, delayed, triggered, charged, prepared. |
| Support dice | Different magnitude die or dice purpose. |
| Risk | Backlash, instability, corruption, fatigue, exposure, trace, tool strain. |
| Failure mode | Misfire, recoil, leakage, false read, contamination, cascade. |
| Recovery | Rest, breath, meditation, repair, cooling, purification, recharge, offering. |
| Bandwidth | What it can affect, how deeply, precisely, durably, or broadly. |
| Critical payload | What natural 20 or natural 1 does through that route. |
| Stability | Theoretical, prototype, experimental, unstable, functional, refined, integrated, mastered. |

Enhancement, magnification, stabilization, anchoring, transmutation, contamination, restriction, and cost splitting all count as mechanical vector changes.

---

## 6. Compatibility modes

Compatibility is not a simple yes/no or one-dimensional ladder.

| Mode | Meaning |
|---|---|
| Native | Economy naturally expresses the effect. |
| Aligned | Economy strongly supports the effect through domain, method, or affinity. |
| Adaptive | Economy can express it with training, altered method, or higher cost. |
| Strained | Economy can force it, but inefficiently or with meaningful risk. |
| Amplifying | Economy increases scale, intensity, density, range, precision, or impact. |
| Stabilizing | Economy reduces backlash, volatility, instability, or misfire. |
| Anchoring | Economy improves duration, persistence, binding, or environmental attachment. |
| Catalytic | Economy triggers, ignites, accelerates, or enables another economy's effect. |
| Transmutive | Economy changes substance, state, damage family, material behavior, or ontological quality. |
| Constraining | Economy narrows expression but increases control, tracking, safety, or specificity. |
| Contaminating | Economy increases power but adds corruption, trace, decay, debt, identity pressure, or hostile signature. |
| Parasitic | Economy feeds on another economy, target, environment, user state, or carrier. |
| Inert | Economy is present but does not meaningfully affect the Expression. |
| Incompatible | Economy cannot participate without bridge, technique, relic, breakthrough, or source-local exception. |

---

## 7. Stability states

Expression stability states:

| State | Meaning |
|---|---|
| Theoretical | Concept is understood but not usable yet. |
| Prototype | Can be tested under controlled conditions. |
| Experimental | Usable, but high cost/risk and not routine. |
| Unstable | Works, but carries persistent failure/backlash risk. |
| Functional | Valid for ordinary play. |
| Refined | Efficient, safer, broader, or cleaner than functional. |
| Integrated | Part of build/path/domain identity. |
| Mastered | Can be modified, taught, re-authored, or used under hostile conditions. |
| Restricted | Valid but blocked by access, law, oath, faction, corruption, or source-local condition. |
| Rejected | Not mechanically valid as written. Must be revised or rerouted. |

---

## 8. Expression Record bridge

An Expression Record should include, at minimum:

```yaml
expression_record:
  expression_id: string
  display_name: string
  doctrine_term: Expression
  local_term: spell | technique | rite | art | formula | working | maneuver | protocol | craft | other
  origin_type: canon | converted | player_created | source_local | experimental
  expression_family: string
  core_function: string
  domain_tags: [string]
  material_or_element_tags: [string]
  primary_economy: string
  secondary_economy: string | null
  stabilizer_or_catalyst: string | null
  economy_roles:
    primary: dominant | secondary | tertiary | external | overlimit
    secondary: dominant | secondary | tertiary | external | overlimit | null
  compatibility_profile:
    - economy: string
      mode: string
      rationale: string
  cost_profile_ref: string
  scope_profile_ref: string
  effect_flags_ref: string
  stability_state: string
  validation_status: proposed | valid_for_testing | valid | restricted | rejected | source_local
  version_parent: string | null
```

D03-05 expands validation. D03-06 expands retention.

---

## 9. Example: Earthen Wisp to Wisp of Steel

### Earthen Wisp

- Expression family: material control.
- Core function: control a small sphere of earthen material.
- Route: Mistra with earth-domain familiarity.
- Stability: experimental to functional.
- Scope: close, small object, sustained, direct control.

### Wisp of Steel

- Re-authored form of Earthen Wisp.
- Route: Mistra + Pressa.
- Mistra provides shaping.
- Pressa provides density, weight, cohesion, suppression, or transmutation toward steel-like behavior.
- Cost split across Mistra and Pressa partitions.
- Higher burden and higher stability requirement.
- May become unstable before training completes.

Possible third economy modifications:

| Third economy | Likely modification |
|---|---|
| Scrypta | Anchoring, persistence, trigger, prepared form. |
| Sympathis | Tracking, resonance sensing, metal/stone feedback. |
| Scintilla | Burst/impact/ignition, volatility. |
| Isotra | Stabilization and reduced backlash. |
| Vitia | Corruptive rust/decay effect, contamination risk. |
| Reticula | Networked or remote control through infrastructure. |

---

## 10. Conversion implications

Donor abilities should be split into:

- Expression family;
- Power Economy route;
- local term/source name;
- method;
- cost;
- risk;
- recovery;
- bandwidth;
- retention requirement;
- source-local wrapper.

A donor fire spell is not automatically a Mistra spell. It may map to Mistra, Calora, Scrypta, Fideth, Vitia, Scintilla, or another route depending on function.
