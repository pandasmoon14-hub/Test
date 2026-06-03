# Astra Ascension — D03-05 Expression Validation Gate

Status: design-draft / accepted architecture  
Layer: Native Design Phase / D03  
File ID: D03-05  
Version: v0.1  
Date: 2026-05-29

---

## 1. Purpose

This file defines the Expression Validation Gate.

The gate allows Astra to support converted abilities, canonical abilities, player-created content, re-authored expressions, and experimental ideas while preventing low-level or unprepared actors from gaining game-breaking effects through clever phrasing alone.

---

## 2. Core principle

A player may describe any desired outcome. A character may attempt an Expression only when a lawful route exists and the Expression passes validation.

Astra should support ambition before access. Desired outcomes may become theory, research, training, experimentation, quest pressure, prototype, or future unlock.

---

## 3. Desired Outcome vs. attempted Expression

### Desired Outcome

A desired outcome is what the player wants to happen.

Examples:

- "I want to kill him with a word."
- "I want to make earth orbit me."
- "I want to turn the earthen wisp into steel."
- "I want to bind the spirit into the blade."
- "I want my mundane hunter to learn what power is."

A desired outcome is always allowed as intent.

### Attempted Expression

An attempted Expression is a mechanically valid action using a lawful route.

It requires:

- source;
- medium;
- method;
- target;
- access;
- cost;
- scale/scope;
- counterplay or coherent failure mode;
- retention or temporary route.

Without a lawful route, no supernatural Expression roll occurs.

---

## 4. Lawful route

A lawful route requires enough structure to answer these questions.

| Component | Question |
|---|---|
| Source | What Power Economy, external force, tool, relic, entity, or phenomenon powers it? |
| Medium | Through what carrier does it act: voice, gesture, inscription, weapon, breath, blood, aura, network, spirit, material, etc.? |
| Method | What is the character actually doing? |
| Target | What is being affected, and can the method reach it? |
| Access | Does the character have training, affinity, permission, contact, tool, relic, path, or anchor? |
| Cost | What is paid, risked, reserved, strained, or sacrificed? |
| Scope | Is the grade/scope within authorization or overreach? |
| Counterplay | Can the effect be resisted, interrupted, avoided, misfire, or fail coherently? |
| Retention | Is this known, retained, experimental, external, or theoretical? |

---

## 5. Expression Grade

Expression Grade is a validation scale, not a direct level substitute.

| Grade | Meaning | Example scale |
|---:|---|---|
| 0 | Mundane / utility | Minor trick, hand task, ordinary exertion. |
| 1 | Minor Expression | Small effect, short range, narrow utility. |
| 2 | Basic combat / utility | Single-target harm, small ward, basic detection. |
| 3 | Competent field Expression | Reliable combat use, small area, meaningful control. |
| 4 | Advanced Expression | Strong effect, multiple targets, significant alteration. |
| 5 | Major Expression | Battlefield-relevant, high-cost, high-impact. |
| 6 | Superior Expression | Large-scale, hard to counter, high-lethality. |
| 7 | Apex Expression | Scene-defining, elite-tier, severe backlash if misused. |
| 8 | Transcendent Expression | Site-scale, law-bending, extreme cost or special access. |
| 9 | Mythic Expression | Region-scale, fate/domain-level, rare or source-local. |
| 10 | Cataclysmic / world-pressure | Campaign-defining; not ordinary use without major doctrine support. |

---

## 6. Scope Profile

Scale is not one axis. Use a Scope Profile.

```yaml
scope_profile:
  range_band: self | touch | close | ranged | line_of_sight | remote | sympathetic | domain_bound | planar | undefined
  area_band: none | point | small_object | creature_sized | room | scene | structure | site | region | world_plane
  target_count: self | one | few | group | swarm | mass | environment | abstract
  duration: instant | momentary | sustained | scene | hour | day | indefinite | permanent
  persistence: none | maintained | anchored | autonomous | self_repeating | contagious | permanent
  control_model: direct | guided | commanded | triggered | autonomous | negotiated | uncontrolled
  delivery_model: touch | gesture | spoken | gaze | mark | projectile | aura | field | inscription | network | ritual | sacrifice | environment
  summoning_vector: none | call | manifest | construct | bind | invite | open_gate | borrow | externalize
  banishing_vector: none | dismiss | sever | repel | unbind | exile | seal | return | erase_anchor
  traversal_vector: none | movement | displacement | crossing | phasing | bridging | recall | route_creation
  counterplay_model: avoid | resist | interrupt | dispel | endure | break_anchor | sever_source | bargain | no_common_counter
```

The Scope Profile supports ranged effects, summoning, banishing, traversal, autonomous constructs, wards, field effects, remote effects, and persistent effects.

---

## 7. Effect flags

Effect flags are mandatory but must be managed carefully.

Each flag should carry:

```yaml
effect_flag:
  flag: string
  category: string
  intensity: minor | standard | major | severe | apex
  constraint: string | null
  counterplay: string | null
  grade_pressure: low | medium | high | blocking
```

### Flag categories

| Category | Examples |
|---|---|
| Harm | damaging, lethal, draining, armor-piercing, corrosive, explosive. |
| Control | binding, slowing, suppressing, stunning, agency-denying, commanding. |
| Movement | pushing, pulling, flight, phasing, teleport-like, route-making. |
| Summon / Banish | manifesting, binding, calling, dismissing, sealing, exiling. |
| Creation / Transmutation | shaping, constructing, materializing, densifying, forging. |
| Perception / Information | revealing, tracking, divining, diagnosing, translating, predicting. |
| Protection | warding, shielding, anchoring, filtering, resisting, stabilizing. |
| Restoration | healing, purging, repairing, recovering, harmonizing, restoring memory. |
| Social / Mental | persuading, terrifying, entrancing, masking, glamouring, oath-binding. |
| Economy Interaction | cost-splitting, overdraw, reservoir conversion, partition bleed, stabilizing. |
| Persistence | sustained, autonomous, contagious, self-repeating, permanent. |
| Causal / Probability | luck-shifting, consequence-redirection, debt-marking, fate-weighting. |
| Corruptive / Forbidden | contaminating, degenerating, Vitia-bearing, identity-eroding. |
| World / Environment | terrain-altering, weather-affecting, structure-shaping, ecological. |
| Meta-Expression | countering, copying, rewriting, amplifying, nullifying, fusing. |

New flags may be added, but must include category, intensity, constraint, counterplay, and grade pressure.

---

## 8. Unsafe Expression Attempt Protocol

When a proposed Expression exceeds actor authorization, the system does not automatically offer a clean lower-level version.

Instead, the system provides an immersive warning and lets the player stop, prepare, research, or push into danger if a minimal lawful route exists.

### Validation statuses

| Status | Meaning |
|---|---|
| Valid | Can be used normally. |
| Overreach | Possible but dangerous; warning required. |
| Prototype | Can be attempted in limited or controlled form. |
| Unstable | Works, but risk profile is elevated. |
| Unanchored | Concept has no stable economy route yet. |
| Uncontained | Effect exceeds Vessel, partition, or stabilizer capacity. |
| Forbidden / Restricted | Blocked by access, law, oath, corruption, faction, or source-local condition. |
| Invalid | No coherent target, method, access, or effect logic. No roll. |

---

## 9. Pushing beyond authorization

If the actor pushes a coherent but unauthorized Expression, possible outcomes include:

- failure with consequence;
- severe failure;
- critical failure;
- distorted reduced effect;
- random low-grade manifestation;
- one-time unstable prototype;
- backlash;
- partition damage;
- Endura drain;
- Health harm;
- instability gain;
- Vitia contamination;
- memory loss;
- external attention;
- threshold pressure;
- source-local scar;
- expression slot strain.

The reduced manifestation is a consequence of the attempt, not a design handout.

---

## 10. Low-level instant-kill spoken word example

A player may state the desired outcome: "I want to kill him with a word."

The system should not process this as an attempted Expression unless a lawful route exists.

Possible lawful routes:

- sound affinity;
- compulsory/command affinity;
- Volith will imposition;
- Pressa suppression;
- Phasma name-binding;
- Fideth oath judgment;
- Karmax causal debt;
- Sortis critical-fate manipulation;
- Scrypta encoded speech;
- relic containing a death word;
- planar/entity contact;
- target already marked, bound, dying, cursed, or under finishing condition.

Without route, no supernatural roll occurs.

The desire can become:

- theory;
- research vector;
- forbidden intuition;
- quest hook;
- search for teacher/relic/entity/affinity;
- mundane speech action such as intimidation, command, distraction, prayer, or bluff.

---

## 11. Immersive warning pattern

Warnings should be narrative/contextual rather than UI-only.

Example:

> The shape of the word is not absent. It is simply not yours. Your throat can make sound, but not law. To force it now would not be casting; it would be tearing at a door with your own voice.

Warnings may arise as:

- bodily recoil;
- Animus pressure;
- Reason calculation;
- Insight omen;
- tool diagnostic;
- teacher memory;
- relic refusal;
- domain resonance;
- opposing force attention;
- sudden cost comprehension.

---

## 12. Conversion implications

Donor high-level abilities cannot be imported at low grade because their prose is simple.

Each donor ability must be decomposed into:

- grade;
- scope profile;
- effect flags;
- economy route;
- lawful route;
- cost floor;
- risk profile;
- retention requirement;
- source-local boundary.
