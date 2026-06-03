# Astra Ascension — D02/D05 Relevance Cross-Check Amendment

Version: v0.1  
Status: optional but recommended cross-check / pre-D06  
Applies to: D02 Resolution and Consequence Model, D02-A Dice Interface Amendment  
Source pressure: D05 Relevance Handling for Checks, Competency Records, Research/Training, and Lawful Action Vectors

---

## 1. Purpose

D02 already defines the d20 resolution structure, outcome lanes, criticals, cost commitment posture, and the principle that relevant skill, profession, special knowledge, technology, training, tools, and context may affect advantage, disadvantage, modifiers, cost, and consequence.

D05 now defines what relevance means.

This cross-check clarifies the D02/D05 boundary:

D05 classifies relevance. D02 applies resolution.

---

## 2. No full D02 rewrite required

D05 does not require a D02 redesign.

D02 remains the owner of:

- d20 roll procedure;
- natural 1 and natural 20 handling;
- temporary technical outcome lanes;
- margin bands;
- declared cost and risk;
- advantage/disadvantage as roll posture;
- modifiers as resolution inputs;
- consequence lane interpretation;
- assessment action structure.

D05 now supplies:

- relevance categories;
- relevance strength bands;
- one-primary-roll-posture rule;
- secondary effects;
- access relevance;
- harmful/invalid relevance;
- meaningful relevance records;
- lawful action-vector support.

---

## 3. Core D02/D05 interface laws

### D02/D05-L1 — D05 classifies, D02 resolves

For a check, D05 may classify competency relevance as:

- Direct;
- Supporting;
- Contextual;
- Interpretive;
- Preparatory;
- Recovery;
- Access;
- Harmful;
- Invalid.

D02 then applies any authorized roll effect or outcome effect.

### D02/D05-L2 — One primary roll posture benefit

A single D02 check should normally receive only one primary roll posture benefit from competencies.

Primary roll posture benefits include:

- advantage;
- disadvantage cancellation;
- major modifier;
- major difficulty adjustment.

Other relevant competencies may provide secondary effects.

This preserves D05’s anti-stacking rule.

### D02/D05-L3 — Relevance may affect non-roll outputs

D05 relevance may affect:

- information yield;
- cost;
- consequence;
- risk posture;
- access legality;
- proof generation;
- training progress;
- research progress;
- route pressure;
- hidden tag reveal;
- recovery from failure.

D02 should not treat relevance as only a bonus system.

### D02/D05-L4 — Access relevance controls whether a roll is valid

Some actions require a lawful action vector before rolling.

If the actor lacks access, D02 should route the request to one of:

- requires preparation;
- requires research;
- requires training;
- requires access;
- requires proof;
- requires owner validation;
- source-local only;
- dangerous temptation;
- blocked;
- quarantined.

D02 should not roll unsupported power declarations as if they were valid actions.

### D02/D05-L5 — Harmful relevance is possible but bounded

D05 may classify expertise as harmful when prior training creates confident error in the current context.

D02 may express this as:

- disadvantage;
- false-read risk;
- increased cost;
- increased consequence;
- misdirected research;
- harmful secondary effect.

Harmful relevance requires a real mismatch. It should not be arbitrary punishment for creativity.

### D02/D05-L6 — Relevance records are selective

D02 does not need to preserve every relevance decision.

A Relevance Record should be created when relevance affects:

- proof;
- training;
- research;
- route pressure;
- action-vector legality;
- major consequence;
- hidden-state interpretation;
- Development Pick eligibility.

Ordinary minor checks may remain ephemeral.

---

## 4. D02 outcome lane compatibility

D05 does not change the accepted D02 outcome bands.

The accepted D02 structure remains:

| D02 lane | Trigger |
|---|---:|
| Critical Success | Natural 20 |
| Exceptional Success | Margin +5 or higher |
| Clean Success | Margin 0 to +4 |
| Partial Result | Margin -1 |
| Mixed Result | Margin -2 to -3 |
| Failure with Consequence | Margin -4 to -7 |
| Severe Failure | Margin -8 or worse |
| Critical Failure | Natural 1 |

D05 relevance can modify posture, cost, consequence, access, and information yield, but it does not change these lane definitions.

---

## 5. D02 check procedure amendment

Recommended D02 check procedure after D05:

1. Player declares action and desired outcome.
2. System/GM identifies whether the action is currently lawful.
3. If access is uncertain, D05 Access Relevance or Research/Training classification is applied.
4. Player declares cost/risk if required.
5. Relevant competencies are claimed or inferred.
6. D05 classifies relevance type and strength.
7. One primary roll posture benefit is selected.
8. Secondary relevance effects are assigned if appropriate.
9. D02 performs d20 resolution.
10. D02 outcome lane is interpreted.
11. D05/D03/D04/D06/etc. owner handoffs are recorded if the action created proof, research, training, method, Expression candidate, route pressure, or other durable state.

---

## 6. D02-A dice interface note

If a future dice roller or dice box is integrated, the roll payload should eventually support relevance metadata.

Suggested non-final payload shape:

```yaml
roll_payload:
  actor_ref: string
  action_summary: string
  die: d20
  advantage_state: normal | advantage | disadvantage
  modifier_total: number
  declared_cost: string
  declared_risk: string
  relevance_refs: []
  primary_relevance_effect: string
  secondary_relevance_effects: []
  lawful_action_vector_status: lawful | lawful_with_risk | requires_research | requires_training | requires_access | requires_proof | requires_owner_validation | source_local | dangerous | blocked | quarantined
  result:
    natural_die: number
    total: number
    margin: number
    outcome_lane: string
```

This is not final runtime schema. It is an interface reminder.

---

## 7. Examples

### 7.1 Blacksmith examines sword relic

D05 classification:

- Blacksmith Profession: Direct or Contextual relevance.
- Metallurgy: Direct relevance.
- Relic Appraisal: Interpretive relevance.
- Hammer Rhythm Method: Supporting/Interpretive if stress patterns are involved.

D02 application:

- one primary roll posture benefit, likely advantage or modifier from the strongest relevant competency;
- secondary information yield from the others;
- possible Research Track or D09 handoff if relic behavior is unknown.

### 7.2 Unsupported spoken instant-kill desire

D05 classification:

- No current lawful action vector unless the actor has sound, compulsion, relic, route, entity contact, technique, Expression, or source-local basis.

D02 application:

- no standard power roll;
- route to requires research, requires access, dangerous temptation, blocked, or quarantined;
- if the actor physically shouts anyway, resolve only the mundane/social action that is actually lawful.

### 7.3 Wrong expertise

A mundane doctor examines a spirit wound and applies ordinary trauma assumptions.

D05 classification:

- Medicine may be Supporting or Harmfully Relevant depending context.
- Spirit taxonomy or Esoteric/Occult knowledge may be Access or Interpretive relevance.

D02 application:

- harmful relevance may increase misread risk or consequence if the actor confidently proceeds with false assumptions.
- It should not be punitive if the actor probes cautiously.

---

## 8. Cross-check acceptance checklist

D02 is aligned with D05 when:

- [ ] D02 states that D05 classifies relevance.
- [ ] D02 preserves one-primary-roll-posture benefit per check.
- [ ] D02 allows secondary relevance effects beyond roll modifiers.
- [ ] D02 recognizes Access Relevance and lawful action-vector status.
- [ ] D02 recognizes Harmful and Invalid relevance.
- [ ] D02 keeps accepted d20 outcome bands unchanged.
- [ ] D02-A dice interface can eventually carry relevance metadata.
- [ ] D02 does not roll unsupported desired outcomes as valid powers.

---

## DDR Fragment — D02/D05 Relevance Cross-Check

Status: optional but recommended amendment

Design question:
- Does D02 need adjustment after D05 relevance and competency doctrine?

Current working answer:
- D02 does not need redesign. It should add a cross-reference rule: D05 classifies relevance and lawful action-vector status; D02 applies d20 resolution. One competency may provide the primary roll posture benefit, while additional relevant competencies may provide secondary effects. Relevance can affect cost, consequence, information yield, proof, training, research, and access, not only roll bonuses.

Astra-native principle:
- Dice resolve uncertain actions, but competency determines what is lawful, relevant, costly, interpretable, and consequence-bearing.

Mechanical implication:
- Add D05 relevance classification to D02 check procedure.
- Add one-primary-roll-posture enforcement.
- Add non-roll relevance effects.
- Add Access Relevance and unsupported desired-outcome routing.
- Add optional dice interface metadata.

Player-facing implication:
- A character’s profession, knowledge, tools, and training matter without creating bonus-stacking.
- Unsupported powers become research/access/training/proof problems rather than arbitrary rolls.

Conversion implication:
- Donor skill synergy, advantage, expertise, tool proficiency, knowledge-check, and research modifiers can normalize through D05 relevance and D02 roll posture.

Runtime implication:
- Future roll payloads should carry relevance metadata and lawful-action-vector status.

Decision needed:
- Accept this D02 cross-check or defer until D06/D07 pressure makes D02 revision necessary.
