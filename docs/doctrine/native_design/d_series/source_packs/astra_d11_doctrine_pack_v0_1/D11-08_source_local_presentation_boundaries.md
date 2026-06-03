# D11-08 Source-local Presentation Boundaries

## Purpose

This file defines how D11 presents retained donor-local or campaign-local systems without implying they are universal Astra doctrine. D11 remains interface doctrine. It presents source-local systems within scope; it does not promote them to canon.

## Core rule

D11 may present retained source-local systems only within their authorized scope. Player-facing narration should translate them into visible effects, choices, symptoms, and consequences. GM-facing summaries may name the source-local system, but must label it as local and prohibit generalization.

## Source-local categories

Source-local categories include local clocks, local reputation/heat, local clue/reveal systems, local domain/kingdom systems, local economy/market systems, local travel/map systems, local horror/stability systems, local resolution exceptions, and mixed retained procedures.

## Player-facing translation

Player-facing narration should usually not expose raw local labels.

Bad: “The faction clock advances to 4/6.”  
Better: “The guild has stopped pretending this is private. Their messengers now wear house colors openly.”

Bad: “Your heat level rises.”  
Better: “Patrols that ignored you yesterday now pause long enough to compare your faces to a folded notice.”

Bad: “The rumor table result is 7.”  
Better: “The dockhands repeat the same story with different names: someone paid well to keep cargo off the south pier.”

## GM-facing label rule

GM-facing summaries may name retained systems only when labeled local.

```yaml
source_local_status:
  system_type: "local faction clock"
  source_scope: "current converted module only"
  current_state: "4/6"
  player_facing_signal_used: "guild messengers now act openly"
  prohibited_generalization:
    - "not universal Astra faction AI"
    - "not default D10 faction procedure"
```

## Scope labels

Scopes include encounter-local, site-local, adventure-local, campaign-local, faction-local, region-local, source-family-local, and source-local pending promotion. No scope is global Astra unless later canon promotion occurs.

## Prohibited generalizations

D11 blocks: Astra factions use clocks; Astra cities have heat levels; Astra mysteries use clue webs; Astra markets use ratings; Astra domains use kingdom turns; Astra horror uses sanity loss; Astra travel uses hex turns; Astra rumors come from tables; Astra corruption advances by clocks.

Safe phrasing uses “this retained local…,” “under this source-local…,” “this site-local…,” or “this campaign-local…” language.

## Hidden source-local mechanics

Hidden local systems still obey D11 hidden-state and fairness rules. Player-facing narration may show symptoms or signals, not hidden mechanics unless lawfully revealed.

## Source-local escalation

Escalate for doctrine review when a retained system appears in multiple unrelated conversions, solves a general Astra problem better than current doctrine, conflicts with D00–D10, produces consequences outside authorized scope, needs canonical promotion, contradicts another retained local system, or becomes necessary across many D11 presentations. Escalation is not automatic promotion.

## Conflict handling

If local systems conflict, identify each as source-local, preserve scope, map shared outputs to D10 if needed, keep procedure local, and escalate repeated pressure if a broader Astra framework is needed. Do not create universal hybrids casually.

## Player agency

Local systems may increase pressure, but D11 still presents choices unless owner/source-local state removes them.

## Record shape

```yaml
d11_source_local_presentation_record:
  source_local_ref: string
  system_type: string
  scope: string
  player_facing_translation: string
  gm_facing_raw_status: []
  hidden_state_not_to_reveal: []
  surfacing_intensity: string
  prohibited_generalizations: []
  owner_outputs:
    D02: []
    D03: []
    D04: []
    D05: []
    D06: []
    D07: []
    D08: []
    D09: []
    D10: []
  escalation_flags: []
```
