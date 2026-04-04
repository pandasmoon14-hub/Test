# batchA_03_resolution_framework.md

## Status
Draft — Core Now

## Authority
This file is the authoritative doctrine file for the **Astra Batch A resolution framework**.

It defines:
- Astra's universal adjudication grammar,
- the recognized kinds of resolution events,
- the doctrine of thresholds, opposition, and difficulty,
- result grades and consequence packages,
- favorable and adverse resolution states,
- critical and catastrophic outcome handling,
- atomic and extended resolution structures,
- and donor-engine mapping hooks for non-identical resolution carriers.

It does **not** define:
- the full combat loop,
- damage-family rules,
- condition/effect architecture,
- resource-cost and recharge logic,
- package-specific bonuses,
- final numerical implementations for every subsystem,
- or donor-specific engine procedures in exhaustive detail.

If a later Batch A file appears to redefine how uncertain actions are adjudicated at the framework level, this file governs unless deliberately revised.

---

## 1. Purpose

Astra requires a stable answer to a foundational question:

**How does Astra adjudicate uncertainty across many different donor engines without freezing one donor procedure as universal law?**

This file answers that question.

Its job is not to canonize one die, one table, one target-number model, or one probability philosophy. Its job is to define the **grammar of adjudication** that later files and future donor conversions may rely upon.

Astra therefore treats resolution as a doctrine layer with four responsibilities:
- identify what kind of uncertain event is being resolved,
- identify what procedure carries that resolution,
- identify what outcome category the procedure produces,
- and identify what consequences follow from that outcome.

This file exists to prevent two opposite failures:
- **engine collapse**, where every later file quietly invents its own hidden resolution model,
- and **donor capture**, where one donor engine is mistaken for Astra's permanent universal law.

---

## 2. Scope Boundaries

### 2.1 This file must include
- core resolution principles,
- recognized resolution carriers,
- event types such as tests, contests, saves, and extended resolution,
- threshold ownership and opposition doctrine,
- static and dynamic difficulty doctrine,
- result grades,
- consequence-package doctrine,
- favorable and adverse modifier-state doctrine,
- critical and catastrophic outcome doctrine,
- automatic resolution and declared impossibility rules,
- fallback adjudication rules,
- and donor-engine mapping hooks.

### 2.2 This file must not include
- the combat turn sequence,
- attack-action catalogs,
- weapon procedures,
- damage-family taxonomy,
- status-condition internals,
- resource-spend formulas,
- recharge tables,
- path/class/archetype bonuses,
- ancestry- or kinform-specific exceptions,
- or full worked conversions for every donor system.

### 2.3 Interpretation rule
If a question asks **how Astra classifies and adjudicates uncertain outcomes at a framework level**, it belongs here.

If a question asks **how a specific subsystem implements that grammar numerically or procedurally**, it belongs in the later file that owns that subsystem.

### 2.4 Numeric restraint rule
`batchA_03` defines adjudication grammar, not the full numeric implementation of every Astra subsystem.

---

## 3. Core Resolution Principles

### 3.1 Uncertainty requires justification
Not every declared action deserves a roll or equivalent procedure.

A resolution event exists only when:
- the outcome is uncertain,
- the difference between outcomes matters,
- the fiction permits an attempt,
- and the system has something meaningful to distinguish.

### 3.2 Resolution serves fiction and framework together
Astra resolution is not purely narrative improvisation and not purely detached arithmetic.

A lawful resolution event must respect:
- the fictional situation,
- the actor's established capabilities and access,
- the governing subsystem,
- and the intended donor function where donor conversion is involved.

### 3.3 One event, one recognized resolution shape
Before resolving anything, Astra should identify what kind of event it is: test, contest, save, progressive structure, automatic outcome, declared impossibility, or fallback adjudication.

### 3.4 A resolution event has a carrier
A **resolution carrier** is the procedure that produces an adjudicable result.

A carrier may be:
- dice-based,
- card-based,
- token- or bid-based,
- tag- or aspect-based,
- clock- or progress-based,
- table-based,
- authority-transfer based,
- choice-based,
- diceless,
- or any lawful donor-native equivalent.

Astra standardizes the grammar around the carrier. It does not require every donor to use the same carrier.

### 3.5 Result and consequence are related but distinct
A resolution event may produce both:
- a **result grade**,
- and a **consequence package**.

The result grade describes how the attempt resolved at the adjudication level.

The consequence package describes what that result changes: effect, cost, exposure, position, progress, resource state, tag creation, follow-up pressure, or similar fallout.

A donor system may combine these into one output or separate them into multiple channels. Astra must be able to represent both arrangements.

### 3.6 Preserve donor intent, not donor ceremony
When converting a donor engine, Astra should preserve the function of the donor procedure rather than mechanically copying every surface ritual.

If a donor uses cards, clocks, tags, or token spend to create pressure, uncertainty, and consequence, Astra should preserve those functions even when the final Astra expression uses different controlled terms.

### 3.7 Automatic certainty is lawful
Some outcomes are automatic, impossible, access-blocked, or fictionally unsupported. Astra must not create performative uncertainty where none is warranted.

---

## 4. Resolution Carriers

A resolution carrier is the mechanism by which a resolution event produces an adjudicable output.

This file recognizes the following carrier families:
- **dice carrier** — one or more dice generate the output,
- **card carrier** — cards, draws, or hands generate the output,
- **token carrier** — spend, bid, reserve, or budget logic generates the output,
- **tag carrier** — invoked descriptors, aspects, or temporary truths generate the output,
- **progress carrier** — clocks, tracks, segments, meters, or staged accumulation generate the output,
- **table carrier** — lookup procedures or outcome tables generate the output,
- **authority carrier** — the right to declare or constrain outcomes passes according to rules,
- **choice carrier** — the acting side or table chooses among structured consequences,
- **hybrid carrier** — two or more carrier families combine.

Carrier doctrine notes:
- The carrier is not the event type.
- The same event type may be carried by different carriers across donor systems.
- A donor's carrier does not automatically dictate Astra's controlled terminology.

---

## 5. Resolution Event Types

Astra recognizes the following framework-level event types.

### 5.1 Test
A **test** is a resolution event in which one actor attempts an uncertain action against a threshold.

Use when:
- one actor is the primary mover,
- opposition is static, environmental, indirect, delayed, or abstracted,
- and success is primarily measured against a benchmark rather than another live roll.

### 5.2 Contest
A **contest** is a resolution event in which two or more sides pursue mutually incompatible outcomes.

Use when:
- both sides are actively asserting opposed intent,
- the outcome depends on comparative performance, resistance, leverage, or position,
- and the system treats opposition as more than passive difficulty.

### 5.3 Save or resist event
A **save** or **resist event** is a resolution event in which an actor attempts to avoid, reduce, defer, suppress, or otherwise withstand an incoming pressure.

Use when:
- an effect is already being applied or threatened,
- the target's role is primarily defensive, absorptive, or mitigating,
- and the governing question is not "can the actor initiate?" but "how fully does the actor endure or reject what is incoming?"

### 5.4 Assisted test
An **assisted test** is a test whose acting side receives support from one or more allies, tools, conditions, preparations, or linked systems.

Assistance may change:
- the carrier state,
- the threshold,
- the consequence package,
- the available result bands,
- or the legal right to attempt the action at all.

### 5.5 Group test
A **group test** is a resolution event in which multiple actors attempt a shared objective under one structured adjudication frame.

Group doctrine must distinguish whether:
- one lead actor carries the event,
- all members contribute equally,
- lowest performance constrains the group,
- highest performance elevates the group,
- or the group accumulates shared progress.

### 5.6 Passive or static opposition
A **passive opposition** event is one in which the obstacle has force without requiring an active counter-roll.

Examples include:
- locked systems,
- environmental hazards,
- standing defenses,
- preset institutional barriers,
- static social resistance,
- or any obstacle whose pressure is represented as a threshold rather than a live opposing procedure.

### 5.7 Progressive or extended resolution
Astra recognizes both **atomic resolution events** and **extended resolution structures**.

An **extended resolution structure** is any important action resolved through staged accumulation, repeated pressure, escalating tracks, or structured progress over time.

Examples include:
- chases,
- research projects,
- rituals,
- hacking sequences,
- cultivation breakthroughs,
- social influence ladders,
- negotiations with shifting position,
- crafting projects,
- and multi-stage infiltration or survival sequences.

This file recognizes the category but does not define every later subsystem that may use it.

### 5.8 Automatic resolution
An **automatic resolution** event occurs when the outcome is certain enough that no uncertainty carrier is required.

Automatic resolution may result from:
- overwhelming capability,
- uncontested ordinary action,
- already established fictional control,
- explicit subsystem certainty,
- or the lack of meaningful opposition.

### 5.9 Declared impossibility
A **declared impossibility** event occurs when an attempted action is not legally resolvable because it is impossible, unsupported, access-blocked, or fictionally unavailable.

Impossibility may arise because:
- the fiction has not established a viable approach,
- the actor lacks required access,
- the target cannot presently be affected that way,
- the proposed action contradicts established state,
- or the governing subsystem disallows the attempt.

### 5.10 Fallback adjudication
**Fallback adjudication** is used when a donor system or unusual scene does not map cleanly onto Astra's normal event categories, but a lawful and meaningful outcome still must be produced.

Fallback adjudication must identify:
- the acting side,
- the opposed pressure if any,
- the carrier or substitute procedure,
- the result grade,
- and the consequence package.

Fallback adjudication is not permission for shapeless improvisation. It is a controlled bridge for edge cases.

---

## 6. Threshold Ownership and Opposition Doctrine

Astra must distinguish not only what kind of event is occurring, but also **who owns the threshold** and **who generates the pressure**.

### 6.1 Static threshold
The threshold is preset by the subsystem, scene, object, hazard, or known difficulty band.

### 6.2 Actor-generated threshold
One actor creates the threshold another actor must meet or resist.

This includes cases where:
- an attacker sets the pressure,
- a social actor establishes the resistance challenge,
- a hacker creates a defensive load another side resists later,
- or an active effect creates a later resist benchmark.

### 6.3 Comparative threshold
The threshold emerges from direct comparison between sides.

### 6.4 Environment-generated threshold
The scene, zone, system state, institution, terrain, or hazard creates the pressure independently of any one actor.

### 6.5 Deferred threshold
One event establishes a threshold that will matter in a later event.

### 6.6 Asymmetric opposition
Astra explicitly recognizes that opposition may be asymmetric.

Examples include:
- one side rolls while the other compares passively,
- both sides roll,
- neither side rolls because resources or states decide the matter,
- one side creates a threat value and the other resists later,
- or the scene itself acts as the active pressure source.

This file therefore does not assume that every conflict is resolved through symmetrical opposed rolling.

---

## 7. Difficulty Architecture

Difficulty describes how hard it is to secure a given result grade under current conditions.

### 7.1 Static difficulty
A fixed benchmark determined before the event resolves.

### 7.2 Dynamic difficulty
A benchmark that changes due to situation, progress state, opposition, escalation, prior outcomes, or linked subsystem changes.

### 7.3 Situational adjustment
A lawful shift caused by context, preparation, injury, tools, leverage, environmental state, timing, position, or similar circumstances.

### 7.4 Hidden difficulty
A benchmark the adjudicating authority may know but the acting side may not.

### 7.5 Graduated difficulty
A benchmark structure in which higher performance unlocks stronger result grades or reduced consequence burden.

### 7.6 Gated difficulty
An event whose difficulty is secondary because the real question is whether the actor has lawful access to attempt the action at all.

### 7.7 Difficulty doctrine note
Difficulty is not identical to opposition.

A hard task may have no live opponent.
A contest may be low-difficulty but high-stakes.
A resist event may face pressure generated by a prior action, not by a current roll.

---

## 8. Result Grades and Consequence Packages

### 8.1 Result grade
A **result grade** is Astra's controlled statement of how the attempt resolved at the adjudication level.

Astra recognizes the following default result-grade family:
- **failure** — the intended outcome is not secured,
- **weak success** — the intended outcome is secured in diminished, partial, unstable, or compromised form,
- **standard success** — the intended outcome is secured at expected effectiveness,
- **strong success** — the intended outcome is secured with elevated effectiveness, advantage, or reduced drawback,
- **critical success** — the attempt resolves beyond ordinary success bounds in a mechanically meaningful way,
- **mixed result** — the event secures both success and cost, gain and exposure, or another deliberately split outcome,
- **critical failure** — the event resolves below ordinary failure bounds in a mechanically meaningful way,
- **catastrophe** — the attempt produces severe adverse fallout beyond ordinary failure.

Not every subsystem must use every band. This is the doctrine-level family, not a requirement that all later files use the entire ladder.

### 8.2 Consequence package
A **consequence package** is the bundle of state changes produced by a resolution event.

A consequence package may include any lawful combination of:
- achieved effect,
- reduced effect,
- blocked effect,
- resource spend or drain,
- time cost,
- exposure or danger,
- position change,
- progress gain or loss,
- tag creation or removal,
- status or effect application,
- threshold creation,
- follow-up opportunity,
- backlash,
- collateral change,
- or scene-state advancement.

### 8.3 Result/consequence relationship
A donor system may:
- merge result and consequence into one outcome,
- separate them explicitly,
- make the result strong but the cost painful,
- or deny the main result while still advancing some other track.

Astra must be able to represent all of these without pretending they are the same thing.

### 8.4 Binary and banded systems
Some donor systems output binary pass/fail. Others output multiple degrees, success counts, progress segments, or structured tradeoffs.

Astra supports both binary and banded resolution expressions under the same grammar.

---

## 9. Modifier States and Advantage-Equivalent Handling

Astra recognizes that many donor systems modify outcomes without using the same mechanical language.

Instead of canonizing one donor's exact bonus model, Astra uses the broader category of **modifier states**.

### 9.1 Direct modifier state
A numerical or scalar change directly alters the carrier output.

### 9.2 Threshold-shift state
A change alters the benchmark required for a result.

### 9.3 Carrier-state modifier
A change alters the carrier itself.

Examples include:
- extra dice,
- keep-high or keep-low effects,
- card draws,
- success rerouting,
- progress acceleration,
- choice expansion,
- or equivalent donor-native favorable or adverse carrier states.

### 9.4 Reroll state
A change permits or compels repetition, replacement, or selective retention of carrier results.

### 9.5 Result-shift state
A change moves the final outcome to a better or worse result grade without changing the raw carrier output.

### 9.6 Consequence-shift state
A change alters the consequence package while leaving the main result grade intact.

### 9.7 Assistance state
A support effect changes the odds, thresholds, or fallout of a resolution event due to allied help, preparation, linked systems, or positioned support.

### 9.8 Favorable and adverse resolution states
Astra recognizes broad **favorable** and **adverse** resolution states as the universal family behind donor concepts such as advantage, disadvantage, fortune, misfortune, edge, hindrance, momentum, burden, boost, bane, and similar pressure-shaping mechanics.

This file recognizes the family. It does not freeze one donor implementation as universal law.

---

## 10. Critical and Catastrophic Outcomes

### 10.1 Critical success
A **critical success** is a result that exceeds ordinary success bounds in a way that matters mechanically, fictionally, or both.

A critical success may arise from:
- numerical extremity,
- exceptional margin,
- surplus successes,
- strong card or token outcomes,
- accelerated progress thresholds,
- invoked tag states,
- authority-transfer triggers,
- or other lawful donor-native conditions.

### 10.2 Critical failure
A **critical failure** is a result that falls below ordinary failure bounds in a way that matters mechanically, fictionally, or both.

### 10.3 Catastrophe
A **catastrophe** is a severe adverse consequence package that exceeds standard failure.

A catastrophe need not be identical to critical failure, though a subsystem may choose to link them.

### 10.4 Noncombat criticals
Criticals and catastrophes are not limited to attacks or combat actions.

They may apply to:
- research,
- social maneuvering,
- travel,
- crafting,
- rituals,
- hacking,
- cultivation,
- stealth,
- negotiation,
- or any other lawful resolution domain.

### 10.5 Doctrine note
This file defines what critical and catastrophic outcomes are for Astra grammar. Later files may define how specific subsystems trigger and express them.

---

## 11. Automatic Certainty, Access Blocks, and No-Roll Outcomes

### 11.1 Automatic success
If an actor's capability, access, and position are sufficient and no meaningful uncertainty remains, the outcome should resolve without a carrier.

### 11.2 Automatic failure
If the actor cannot presently produce the required effect and no lawful path changes that state, the event may resolve as failure without a carrier.

### 11.3 Access-blocked action
If the actor lacks required access, qualification, attunement, clearance, or lawful entitlement, the event may be blocked before any uncertainty carrier is invoked.

### 11.4 Fictionally unsupported action
If the fiction has not established a viable approach, the correct response may be to deny the attempt until the fiction changes rather than to fabricate a roll.

### 11.5 Certainty doctrine note
Astra rejects meaningless rolls. Uncertainty is a tool, not a ritual obligation.

---

## 12. Extended and Progressive Resolution Structures

Astra recognizes that some important actions should not collapse into one atomic event.

### 12.1 Progressive structure
A **progressive structure** is any resolution frame that tracks advancement, deterioration, pressure, or opportunity across multiple beats.

### 12.2 Common uses
Progressive structures may govern:
- pursuits,
- projects,
- investigations,
- breakthroughs,
- negotiations,
- sieges,
- infiltrations,
- ongoing hazards,
- and any donor subsystem where accumulated momentum matters more than one isolated event.

### 12.3 Progressive outputs
A progressive structure may output:
- progress gain,
- resistance buildup,
- pressure escalation,
- resource drain,
- state shifts,
- opportunity windows,
- or final-resolution readiness.

### 12.4 Ownership boundary
This file authorizes the category of progressive resolution. Later files and donor mappings may define specialized implementations.

---

## 13. Donor-Engine Mapping Hooks

Astra must absorb donor systems whose uncertainty carriers and result logic differ substantially.

This file therefore recognizes the following donor-engine families as lawful mapping targets:

### 13.1 d20 roll-high systems
Map through tests, contests, saves, thresholds, favorable/adverse states, and banded outcomes where appropriate.

### 13.2 Dice-pool success-count systems
Map through success counts, graded thresholds, comparative pools, and consequence packages.

### 13.3 Step-die systems
Map through carrier-state shifts, threshold logic, and graded outputs.

### 13.4 Roll-under systems
Map through inverted threshold ownership while preserving Astra result grades and consequence doctrine.

### 13.5 Card-based systems
Map through card carriers, hand-state pressure, draw quality, suit/rank significance, or equivalent structured outcomes.

### 13.6 Token, bid, and spend systems
Map through token carriers, declared budgets, commitment pressure, or structured resource-risk exchange.

### 13.7 Tag or aspect invocation systems
Map through tag carriers, invoked truths, temporary descriptors, situational leverage, or fiction-linked modifiers without confusing metadata tags with play-mechanical tags.

### 13.8 Clock and progress systems
Map through progressive structures, segment gain, escalation clocks, countdowns, and readiness thresholds.

### 13.9 Diceless authority-transfer systems
Map through lawful declaration rights, controlled authority shifts, constraint rules, and structured consequence packages.

### 13.10 Choice-based success-at-cost systems
Map through split result/consequence output, explicit cost selection, and controlled mixed-result doctrine.

### 13.11 Fixed-result or table-driven systems
Map through table carriers, state lookups, result bands, and consequence packages.

### 13.12 Hybrid systems
A donor may combine several engine families. Astra should preserve the donor's functional pressure map rather than force false simplicity.

---

## 14. Fallback Adjudication Protocol

When a donor subsystem or unusual situation does not map cleanly into Astra's normal event structures, use the following fallback protocol.

1. Identify the acting side or sides.
2. Identify the uncertain question.
3. Identify the opposed pressure, if any.
4. Identify the most faithful lawful carrier.
5. Identify who owns or generates the threshold.
6. Determine the result grade.
7. Determine the consequence package.
8. Record whether the event was atomic or progressive.
9. Preserve donor intent without importing uncontrolled donor terminology.

Fallback adjudication is a bridge, not a dumping ground.

---

## 15. Explicit Exclusions and Downstream Ownership Boundaries

This file does **not** own:
- the attribute and derived-stat skeleton,
- capability catalogs,
- access-tag and proficiency-gate doctrine,
- ability object schema,
- resource economies,
- status/condition architecture,
- damage-family taxonomy,
- progression-axis implementation,
- or combat sequence architecture.

Those belong to later Batch A files.

This file also does **not** require Astra to express every later subsystem through one universal numerical procedure. It only requires that all such subsystems remain legible inside Astra's adjudication grammar.

---

## 16. Conversion Guardrails

### 16.1 Do not confuse carrier with doctrine
A donor's dice, cards, tokens, tags, clocks, or table structure do not by themselves define Astra law.

### 16.2 Do not collapse result into consequence
A donor that separates success, cost, fallout, and position should remain separated where that distinction matters.

### 16.3 Do not force all resolution into one-roll logic
Extended, progressive, staged, and authority-based systems are lawful.

### 16.4 Do not roll for nonsense
If an action is automatic, impossible, access-blocked, or fictionally unsupported, resolve it accordingly rather than manufacturing uncertainty.

### 16.5 Preserve strange systems without pretending they are identical
Astra's strength is disciplined translation, not fake sameness.

---

## 17. Summary Doctrine Statement

Astra resolution is a **universal adjudication grammar** built to survive many donor engines.

It standardizes:
- event types,
- carriers,
- thresholds,
- result grades,
- consequence packages,
- modifier states,
- critical and catastrophic outcomes,
- certainty and impossibility handling,
- and donor-engine mapping hooks.

It does **not** freeze one donor's dice procedure as the permanent law of Astra Ascension.
