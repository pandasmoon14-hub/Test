# D11-03 Hidden State, Rumor, Secrecy, and Misinformation Presentation

## Purpose

This file defines how D11 presents hidden truth, secrets, rumors, misinformation, propaganda, suppressed records, false attribution, partial truths, and backend uncertainty without spoiling hidden state or misleading the player unfairly. D11 remains interface doctrine. D10 owns information-state records. D02 owns assessment resolution. D05 owns investigation/research method.

## Core rule

D11 must present information according to its knowledge-state, truth-state, visibility, reliability, and discovery status. Hidden truth may influence symptoms, uncertainty, tone, NPC behavior, or scene pressure, but it must not be directly exposed to the player unless a lawful reveal path exists.

## Information layers

D11 distinguishes backend truth, GM-facing truth, player-known fact, player-inferable signal, rumor, misinformation, propaganda, suppressed record, false attribution, and source-local secret. Player-facing handling depends on the layer. Backend truth and GM-facing truth are not revealed unless discovered or explicitly in GM mode. Rumors, misinformation, propaganda, and false attribution must be framed as claims or beliefs, not narrator-certified fact.

## Narrator-certified truth vs in-world claim

D11 distinguishes neutral narration from in-world assertions. “The bridge is broken” is narrator-certified. “The dockworkers insist the bridge is cursed” is an in-world claim. “The governor’s notice blames foreign saboteurs” is propaganda or official claim, not confirmed truth.

## Hidden truth signals

Hidden truth may produce unusual silence, physical symptoms, NPC evasion, inconsistent records, abnormal scarcity, changed patrol routes, object reactions, environmental anomalies, rumor contradictions, legal overreactions, emotional mismatches, faction behavior, or sensory clues. It may not reveal hidden faction names, secret motives, true culprits, concealed object functions, exact hidden modifiers, or backend Pneuma/cosmic pressure unless lawfully discovered.

## Rumors, misinformation, and propaganda

Rumors should indicate source, spread, contradiction, scope, and trustworthiness when relevant. Misinformation may create real social consequence without being true. Propaganda should be presented as deliberate message or official claim, not neutral truth.

## Suppressed records and false attribution

Suppression may appear as missing archive sections, sealed files, redacted testimony, dead witnesses, altered maps, inconsistent official stories, unusually aggressive denials, or restricted shelves. D11 should not automatically explain the suppression’s cause. False attribution separates what happened, who believes what happened, who benefits, what the player knows, and what D10 records as truth.

## Concealed object identity and hidden hazards

Before identification, D11 may present material, weight, markings, environmental reaction, public claims, uncertain appraisal, rumor, partial function, or instability symptom. It must not reveal exact hidden power, true origin, secret owner, curse profile, sentience, final value, or source-local unique function. Hidden hazards and corruption must produce fairness support before severe consequence.

## Hidden Pneuma/cosmic pressure

Pneuma remains backend-only. D11 must not expose it as a score, modifier, or stat. It may appear as omen, impossible coincidence, mythic timing, repeated symbol, unsettling alignment, relic resonance, witness interpretation, or later world-facing myth if D10 records it.

## Assessment misreads

Sundered assessment may produce false, distorted, outdated, or dangerously incomplete reads unless safeguards apply. D11 must not reveal unreliability unless the character has reason to know.

## Fairness rule

Hidden information is fair when it can be assessed, produces symptoms, has source-local reveal procedure, has witness/rumor/record paths, follows prior player action, is known genre/context risk, remains GM-facing and does not punish until surfaced, or was accepted as unknown risk. Severe hidden consequence without signal, accepted risk, assessment path, or source-local justification is unfair.

## Record shape

```yaml
d11_information_presentation_record:
  information_ref: string
  presentation_mode: string
  truth_state: string
  knowledge_state: string
  player_visible_claims: []
  player_inferable_signals: []
  hidden_backend_not_to_reveal: []
  rumor_framing: []
  misinformation_framing: []
  propaganda_framing: []
  suppression_signals: []
  lawful_reveal_paths: []
  assessment_quality: string
  source_local_boundary: []
  escalation_flags: []
```
