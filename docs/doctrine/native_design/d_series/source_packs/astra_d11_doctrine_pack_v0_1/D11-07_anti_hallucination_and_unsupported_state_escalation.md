# D11-07 Anti-Hallucination and Unsupported-State Escalation

## Purpose

This file defines how D11 prevents unsupported narration, invented canon, hidden-truth leakage, owner-file override, source-local leakage, player-agency violation, and unregistered world-state mutation. D11 remains interface doctrine. It detects gaps and routes them; it does not solve missing D03–D10 doctrine by narration.

## Core rule

D11 may narrate supported state, player-visible effects, low-impact color, and clearly bounded provisional detail. It must not create persistent facts, mechanics, hidden truths, owner-file deltas, source-local rules, or player decisions without lawful support. When required support is missing, D11 must route, defer, quarantine, ask for decision, or escalate.

## Support categories

D11 classifies meaningful details as supported state, player-known state, player-inferable state, low-impact color, provisional detail, missing owner state, hidden backend state, source-local state, quarantined state, or escalated state.

## Hard prohibitions

D11 must not invent persistent factions, institutions, laws, markets, territories, object powers, Techniques, routes, actor identities, or world history; reveal hidden truth without reveal path; treat rumor/propaganda/misinformation as narrator-certified truth; assign player intent/emotion/loyalty/belief/memory/action; create D03 costs, D04 eligibility, D06 Technique behavior, D07 harm, D08 substrate changes, D09 object powers, or D10 world changes without owner support; generalize source-local procedure; or expose hidden Pneuma/cosmic pressure as score/modifier/backend rule.

## Low-impact color

Allowed: smell of rain, worn stone, distant crowd, lantern shadows, ordinary clutter, non-specific banners, generic travelers, dust, smoke, weather, texture. Not allowed: named faction symbols, new law notices, relic sigils with mechanics, suspicious NPCs with hidden agenda, map routes, unique monster traces, market shortages, public accusations, hidden cult phrases.

## Provisional detail

Allowed provisional details include unnamed guards, ordinary shopkeepers, minor witnesses, routine clerks, ordinary doors, generic stalls, and nonpersistent weather. They must be low consequence, non-contradictory, mechanically non-defining, not hidden-truth-bearing, and promotable if important.

## Escalation triggers

Escalate when narration requires unknown object power, undefined faction action, missing law/authority state, unregistered world consequence, unsupported transformation, hidden truth reveal without path, source-local conflict, donor mechanic import, missing harm/corruption doctrine, missing economy/scarcity doctrine, missing advancement eligibility, player agency override, contradiction between records, or raw backend state entering player-facing output.

## Escalation output

Good escalation identifies what cannot be safely stated, which owner file is required, whether low-impact/provisional narration is allowed, whether source-local retention applies, and a safe player-facing alternative.

## Unsafe-line rewrite

D11 state-audit mode may rewrite unsafe narration.

Unsafe: “The hidden cult has already bought the city guard.”  
Safe: “The guards use the same refusal phrase you heard at the district office. It may be coordination, training, or coincidence, but it no longer feels isolated.”

Unsafe: “You feel guilty and decide to confess.”  
Safe: “The accusation lands in a room already waiting for your reaction. Confessing, denying, redirecting, or staying silent are all still open.”

## Player agency

D11 must not decide what the player feels, believes, intends, says, trusts, or accepts. It may present bodily sensation from an effect, social pressure, perceived risk, available interpretations, NPC reaction, prior-action consequence, and options.

## Anti-hallucination checklist

Before accepting meaningful narration, ask whether the detail is supported by D00–D10 or source-local state; whether mode is correct; whether it is visible/inferable/known/rumored/hidden/secret; whether it creates persistent world-state; whether it assigns player emotion/action; whether it reveals hidden truth; whether owner mechanics are required; whether donor assumptions are imported; whether it can remain low-impact color; how provisional detail promotes; which owner resolves unsupported state; and whether a safe rewrite is available.

## Record shape

```yaml
d11_unsupported_state_audit_record:
  proposed_content_ref: string
  presentation_mode: string
  support_status: string
  owner_required:
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
    source_local: []
  risk_flags:
    - hidden_truth_exposure
    - invented_canon
    - owner_override
    - source_local_leakage
    - player_agency_violation
    - unsupported_mechanic
    - raw_register_contamination
  safe_rewrite: string
  escalation_note: string
  promotion_route: []
```
