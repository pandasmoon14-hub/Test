# D02-09 Integration Checklists and DDR Register

## Purpose

This file records accepted D02 decisions, validation checklists, owner handoffs, and risk fixes.

## Accepted decision register

### D02-D20 — D20-first resolution architecture

Accepted:
- D02 uses `d20 + Resolution Modifier vs Difficulty Number` as the primary model.
- 2d6 is rejected as primary resolution.
- D20 is Astra-native and does not import donor d20 math.

### D02-DN — Difficulty Number ladder

Accepted:
- D02 uses a DN ladder from 5 to 32+.
- PCR tier, opposition, domain alignment, owner-file state, and source-local boundaries can shape DN.
- Some actions require gates rather than merely high DN.

### D02-OUTCOME — Margin outcome ladder

Accepted:
- Ascendant: +10 or higher.
- Clear: 0 to +9.
- Fractured: -1 to -4.
- Receded: -5 to -9.
- Sundered: -10 or lower.
- Meaningful rolls should avoid “nothing happens” as default.

### D02-CRIT — Natural 20 and natural 1

Accepted:
- Natural 20 is a critical opportunity, not automatic impossible success.
- Natural 1 is a complication flag, not automatic failure.

### D02-COST — Cost commitment

Accepted:
- Intent, method, known cost, optional over-investment, and visible risk are declared before rolling.
- Declared cost usually commits.
- Over-investment is never free.
- Fractured is the primary success-at-cost band.

### D02-PCR — PCR integration

Accepted:
- PCR affects DN, advantage/disadvantage, consequence severity, assessment output, hidden risk, and owner-file routing.
- Pneuma/cosmic pressure remains backend-only.

### D02-CONTEST — Opposition and resistance

Accepted:
- D02 supports static opposition, active contested checks, defense checks, and resistance checks.
- Defense/resistance outcomes are graduated, not binary by default.

### D02-GROUP — Group and extended tasks

Accepted:
- D02 supports lead/support, majority, weakest-link, best-link, and accumulated group checks.
- D02 supports extended progress tasks without physical timers or metacurrency.

### D02-ASSESS — Assessment

Accepted:
- Assessment is a formal action family.
- Insight probes; Reason interprets.
- Sundered assessment may be silently false by default.
- Persistent knowledge changes route to D10.

### D02-SLC — Source-local resolution

Accepted:
- Donor resolution systems receive lawful outcomes.
- Donor resolution math does not become Astra default.

## D02 ownership checklist

D02 owns:
- d20 check procedure;
- DN ladder;
- margin outcome interpretation;
- natural 20/natural 1 handling;
- cost commitment grammar;
- opposed/contested checks;
- defense/resistance check grammar;
- group and extended task grammar;
- assessment resolution grammar;
- outcome-to-delta routing;
- source-local resolution boundaries.

D02 does not own:
- attribute meanings;
- final modifier formulas;
- pools/resources;
- advancement;
- skill lists/methods;
- route powers;
- harm mechanics;
- actor substrate;
- object-state;
- world-state record formats;
- narration.

## Resolution checklist

For any roll, ask:

1. Is a roll needed?
2. What is the intent?
3. What is the method?
4. What is the target?
5. What is the known cost?
6. What is the visible risk?
7. Is over-investment declared?
8. What owner-file states contribute?
9. What DN or opposition applies?
10. What PCR pressure applies?
11. Is the action gated by missing requirements?
12. What is the margin?
13. Which outcome state applies?
14. What declared costs commit?
15. What consequence deltas route to D03–D10?
16. Is source-local boundary relevant?

## D03–D10 handoff matrix

| Trigger | Required handoff |
|---|---|
| pool/resource/fuel/charge/reserve/overdraw/instability | D03 |
| proof/threshold/breakthrough/tier/transformation progress | D04 |
| skill/method/research/crafting/investigation/competence | D05 |
| route/Technique/Principle/oath/domain expression | D06 |
| harm/injury/condition/curse/corruption/backlash/disaster | D07 |
| actor/form/body/companion/AI/spirit/clone/personhood substrate | D08 |
| object/relic/platform/implant/tool/material/salvage | D09 |
| faction/law/economy/reputation/relationship/information/territory | D10 |

## Pre-generation risk fixes embedded

### Risk 1 — D20 becomes donor d20 clone

Fix:
- D02 explicitly blocks donor proficiency, class math, spell assumptions, armor conventions, saving throw categories, critical damage rules, and action economy.

### Risk 2 — D20 swinginess overwhelms competence

Fix:
- no-roll principle, bounded modifiers, advantage/disadvantage, assessment, over-investment, group/extended tasks, and margin-based partial outcomes.

### Risk 3 — Natural 20 breaks gates

Fix:
- natural 20 is opportunity, not automatic impossible success.

### Risk 4 — Natural 1 makes experts incompetent

Fix:
- natural 1 is complication flag, not automatic failure.

### Risk 5 — Partial outcomes disappear

Fix:
- Fractured and Receded remain core outcome states.

### Risk 6 — Cost becomes optional

Fix:
- declared cost commits; over-investment routes to owner files.

### Risk 7 — PCR becomes flavor

Fix:
- PCR affects DN, roll state, consequence severity, information quality, and hidden risk.

### Risk 8 — Defense becomes binary saving throw

Fix:
- defense/resistance use full outcome ladder.

### Risk 9 — Group checks punish parties

Fix:
- support multiple group-check types and reserve weakest-link for true weakest-link fiction.

### Risk 10 — Source-local resolution leaks

Fix:
- donor systems receive lawful outcomes and source-local boundaries.

## Acceptance criteria

D02 is doctrine-ready when it:

1. uses d20-first resolution;
2. keeps Astra’s five outcome states;
3. uses declared cost and over-investment lawfully;
4. integrates PCR;
5. supports contested, defense, group, extended, and assessment checks;
6. routes deltas to D03–D10;
7. blocks donor resolution leakage.
