# D11-09 Integration Checklists and DDR Register

## Purpose

This file consolidates D11’s accepted decisions, ownership boundaries, validation checklists, D00–D10 handoff matrix, and pre-generation risk safeguards. D11 remains interface doctrine and is not the final live-play GM adapter.

## Accepted decision register

### D11-NIA — Narrator Interface Architecture and Owner Boundaries

Accepted: D11 uses the State-Grounded Narrator Interface Model; is not the final live-play GM adapter; distinguishes player-facing, GM-facing, state-audit, and escalation modes; reads D00–D10; and must not invent unsupported facts, override owners, reveal hidden truth without reveal path, or generalize source-local donor procedure.

### D11-SF — Scene Framing from Registered State

Accepted: D11 uses Registered-State Scene Frame Model; scene frames draw from D00–D10, source-local boundaries, or lawful provisional state; visible, inferable, and hidden backend state are separate; low-impact color is allowed; provisional detail promotes if consequential; missing major state escalates; and player agency is preserved.

### D11-OC — Outcome Narration and Consequence Surfacing

Accepted: D11 uses Outcome-to-Consequence Presentation Model; Ascendant, Clear, Fractured, Receded, and Sundered have distinct narration logic; cost categories remain separate; D03–D10 deltas surface through player-facing effects; hidden/backend consequences stay hidden unless lawfully discovered; Sundered is proportional; and follow-up choices may be offered without choosing for the player.

### D11-HS — Hidden State, Rumor, Secrecy, and Misinformation Presentation

Accepted: D11 uses Layered Information Presentation Model; backend truth, GM truth, player-known facts, inferable signals, rumors, misinformation, propaganda, suppression, false attribution, and source-local secrets remain distinct; narrator-certified facts differ from claims; hidden truth may create signals; Pneuma remains protected; Sundered assessment may mislead; and severe hidden consequence requires fairness support.

### D11-AS — Assessment Result Presentation

Accepted: D11 uses Outcome-Banded Assessment Presentation Model; Insight probes and Reason interprets; assessment quality follows D02 outcome; Sundered may create false confidence unless safeguarded; PCR is translated into player-facing language; tools/methods/routes/research/companions/source-local systems can improve reliability; persistent discoveries and accepted false beliefs promote to D10.

### D11-UP — Unresolved Pressure Surfacing

Accepted: D11 uses Contextual Pressure Surfacing Model; pressure surfacing depends on relevance, severity, visibility, scope, proximity, timing, player action, fairness, and source-local boundary; intensity is tiered; pressures do not automatically become encounters; hidden pressures need fairness support; dormant/historical pressures require triggers; multiple pressures are paced.

### D11-PGM — Player-Facing vs GM-Facing Summary Modes

Accepted: D11 uses Dual-Layer Summary and Inspection Model; player-facing narration, party-known summary, GM-facing summary, state-audit, and escalation mode are distinct; player-facing output is filtered; GM-facing summaries may include hidden/backend state when labeled; raw inspection is GM/state-audit only; D03–D10 deltas require dual summary handling; unresolved pressure dashboards are GM-facing unless filtered.

### D11-AH — Anti-Hallucination and Unsupported-State Escalation

Accepted: D11 uses Unsupported-State Escalation and Safe Narration Model; meaningful details are classified; low-impact color cannot create persistent facts; provisional detail promotes if consequential; missing major state routes/defers/quarantines/escalates; D11 blocks hidden-truth leakage, owner-file override, source-local leakage, player-agency violation, and unregistered world-state mutation; state-audit supports unsafe-line rewrites.

### D11-SLP — Source-local Presentation Boundaries

Accepted: D11 uses Source-local Presentation Boundary Model; retained donor-local systems require authorized scope; player-facing narration translates raw mechanics into effects; GM-facing mode labels systems as local; source-local generalization is blocked; hidden local mechanics obey hidden-state/fairness rules; repeated pressure escalates for review, not automatic promotion.

## D11 ownership checklist

D11 owns presentation: scene framing, outcome narration, consequence surfacing, summaries, state-audit, escalation, hidden-state presentation, assessment presentation, pressure surfacing, anti-hallucination controls, source-local presentation, and safe rewrites. It does not own D00–D10 mechanics or final live-play adapter behavior.

## Validation checklists

### Mode separation

Ask whether output is player-facing, party-known, GM-facing, state-audit, or escalation; whether player-facing content is filtered; whether rumors are framed as claims; whether hidden facts are excluded; whether raw records are restricted; whether source-local mechanics are labeled local; and whether escalation warnings stay out of immersive narration.

### Scene framing

Ask what D00–D10 records support the scene; what is visible; what is inferable; what hidden state must not be revealed; what pressures are relevant; what source-local systems are active; what color/provisional details are used; what choices are visible; and whether anything assigns player intent or requires escalation.

### Outcome narration

Ask what D02 outcome applies; what declared/over-invested costs apply; what visible consequences can be narrated; what hidden/delayed consequences are GM-facing; what D03–D10 deltas were created; whether Fractured/Receded are meaningful; whether Sundered is proportional; and whether choices are offered without deciding for the player.

### Hidden state

Ask whether information is backend truth, GM truth, known fact, inferable signal, rumor, misinformation, propaganda, suppression, false attribution, or source-local secret; whether claims are separated from facts; whether reveal path exists; whether Pneuma is protected; and whether severe hidden consequence has fairness support.

### Assessment

Ask what D02 outcome applies; what Insight detected; what Reason interpreted; what confidence applies; whether PCR is translated; whether Pneuma is protected; whether safeguards apply; and whether D10 information-state updates are needed.

### Unresolved pressure

Ask what pressure exists; type, severity, visibility, scope, proximity, trigger, timing, intensity, fairness, state, agency preservation, and pacing.

### Source-local

Ask what retained local system is active; scope; player-facing translation; GM-facing local label; prohibited generalizations; hidden-state fairness; and whether repeated pressure escalates.

### Anti-hallucination

Ask whether every consequential detail is supported, known, inferable, low-impact, provisional, source-local, or escalated; whether it invents canon; whether it creates object/faction/law/harm/advancement/Technique/actor/world-state without owner support; whether it reveals hidden truth; whether it decides player agency; whether it generalizes source-local procedure; and whether safe rewrite is required.

## D00–D10 handoff matrix

| D11 presentation pressure | Source owner |
|---|---|
| Core action loop, state-delta expectation, power/cost/context premise | D00 |
| Attribute signal, Insight/Reason split, Pneuma protection | D01 |
| Outcome state, DN, margin, assessment resolution, cost commitment | D02 |
| Pool/resource/fuel/overdraw/instability visibility | D03 |
| Breakthrough, proof, transformation, threshold visibility | D04 |
| Method, research, assessment technique, crafting/investigation procedure | D05 |
| Route, Technique, Principle, oath, domain expression | D06 |
| Harm, damage, corruption, backlash, injury, condition | D07 |
| Actor, companion, AI, personhood, form-state | D08 |
| Object, relic, platform, implant, tool, salvage | D09 |
| World-state, faction, law, economy, relationship, information, unresolved pressure | D10 |
| Retained local procedure | Source-local boundary |

## Embedded risk queue

D11 must not become the final live-play GM adapter; invent canon; leak hidden backend truth; dump raw registers in player-facing output; collapse D02 outcomes; make Fractured/Receded dead outcomes; use Sundered as arbitrary catastrophe; make assessment omniscient or useless; certify rumors as truth; force or forget unresolved pressures; universalize source-local systems; or overwrite player agency.
