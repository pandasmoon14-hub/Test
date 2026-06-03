# D11-04 Assessment Result Presentation

## Purpose

This file defines how D11 presents assessment results across D02 outcomes while preserving the Insight/Reason split, PCR visibility, hidden-state protection, and D10 information-state promotion. D11 remains interface doctrine. D02 owns assessment resolution. D05 owns method. D10 owns persistent information-state.

## Core rule

D11 presents assessment as information quality, not omniscience. Assessment may reveal actionable state, partial signals, uncertainty, false reads, or distorted interpretations depending on D02 outcome, method, tools, route support, source-local safeguards, and D10 knowledge-state. Insight detects. Reason interprets. Hidden backend truth remains protected unless lawfully revealed.

## Insight and Reason

Insight probes, detects, senses, notices, reads pressure, and catches anomaly. Reason interprets, analyzes, compares, infers, explains, and models. A strong assessment may include both; a weak assessment may reveal one without the other.

## Assessment targets

Assessment may target location tier, location tags, visible PCR pressure, opposition bracket, approximate DN band, domain alignment, hazard type, object-state clue, actor-state clue, route/Technique risk, resource cost risk, law/faction risk, social/reputation pressure, information reliability, hidden-state symptoms, and source-local constraints.

Assessment does not automatically reveal exact hidden modifiers, hidden Pneuma/cosmic pressure, true culprit, secret faction controller, concealed object full power, undiscovered curse profile, full hidden opposition plan, or backend register contents.

## Outcome-banded assessment

Ascendant gives a clear actionable read plus an extra useful signal. Clear gives accurate actionable information. Fractured gives useful but incomplete information with possible cost, exposure, ambiguity, or missing tag. Receded gives vague, limited, or low-confidence information. Sundered may produce false, distorted, outdated, or dangerously incomplete information unless safeguards apply.

Fractured should support better choices without removing all uncertainty. Receded should not be pure nothing if the roll was meaningful. Sundered may sound confident and wrong if no safeguard applies.

## Confidence language

High confidence: “You can confirm…”, “The read is stable…”, “The pattern is consistent…”

Medium confidence: “The most likely reading is…”, “The signs point toward…”, “Enough to act on, not enough to prove…”

Low confidence: “You cannot verify…”, “The signal is incomplete…”, “The read does not settle…”

False confidence is allowed only when D02 outcome supports it, normally Sundered.

## PCR presentation

PCR elements are translated into player-facing language rather than raw tags. Hidden Pneuma/cosmic pressure is never shown as raw score, modifier, or backend tag. It may appear as “the timing feels wrong,” “the omen is readable but not measurable,” or “this is not ordinary luck.”

## Tools, methods, routes, and safeguards

Reliability may improve through D05 expertise, D05 research method, D09 tool/relic, D06 route/Technique, D03 resource investment, D10 archive access, companion expertise, or source-local procedure. A safeguard may prevent Sundered from producing full false confidence.

## D10 promotion

Assessment should promote to D10 when it creates or changes player-known fact, party-known fact, rumor reliability, hidden truth discovered, accepted false belief, map knowledge, object identity knowledge, faction suspicion, witness knowledge, public knowledge, source-local clue state, or suppressed-record awareness.

## Agency

Assessment informs choice; it does not choose for the player. D11 should avoid “you should,” “you must,” or “you know the correct choice is.”

## Record shape

```yaml
d11_assessment_presentation_record:
  assessment_ref: string
  d02_outcome: string
  assessment_target: []
  insight_probe_output: []
  reason_interpretation_output: []
  confidence_language: string
  player_facing_read: string
  gm_facing_truth: []
  hidden_backend_not_revealed: []
  safeguards_applied: []
  d10_information_updates: []
  source_local_boundary: []
  escalation_flags: []
```
