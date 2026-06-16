# RT-001D: Action Legality Integration Hardening Review

## Source PRs

This review covers the merged surfaces from RT-001A, RT-001B, and RT-001C.

## Scope

RT-001D is review-only and does not authorize implementation. It inspects
the RT-001B and RT-001C skeleton surfaces for correctness, safety, and
hardening without adding new behavior or modifying implementation modules.

## Risk Ledger

The following risk categories are evaluated in this hardening review:

1. **Legal approval bypass** -- Can the skeleton be tricked into emitting
   a "legal" status through any constructor, factory, or builder path?

2. **Backend detail leakage** -- Can backend-only detail, trace refs,
   doctrine refs, schema refs, or source-local refs leak into the
   player-visible serialization surface?

3. **Hidden-information specificity** -- Do hidden-information blockers
   use only the restricted generic safe messages, preventing information
   about what is hidden from reaching the player?

4. **Dependency reference accidentally becoming a service call** -- Do
   dependency references remain inert, or could a downstream consumer
   accidentally treat them as live service invocations?

5. **Guardrail allowlist drift** -- Could new SAFE_PLAYER_MESSAGES,
   BLOCKER_CLASSES, or LEGALITY_STATUSES be added without updating the
   corresponding validators and constructors?

6. **Metadata serialization** -- Is metadata validated as JSON-safe before
   storage? Are sets, custom objects, or non-string keys rejected?

7. **Authority flag bypass** -- Can any authority flag be set to a truthy
   value (True, 1, 0, None, "yes", empty string, empty list) without the
   constructor raising?

8. **Constructor/factory divergence** -- Do factories and direct
   constructors enforce the same invariants, or can one path bypass
   constraints the other enforces?

9. **Validator being weaker than constructor** -- Does any validator
   accept objects that the constructor would reject, or vice versa?

10. **PR-9A/9C/9D/9E reference seam overreach** -- Do the gate
    integration input refs stay within reference-passing, or do they
    accidentally invoke PR-9A/9C/9D/9E builders or executors?

11. **action legality engine accidentally reading state** -- Does any path
    in the skeleton read actor state, scene state, world state, or
    persistence stores?

12. **Donor-specific legality assumptions** -- Does the skeleton embed
    donor-specific legality rules (e.g., D&D opportunity attack rules,
    Pathfinder flat-footed conditions) rather than staying system-neutral?

13. **Live-play/model adapter treating skeleton statuses** -- Could a
    downstream live-play adapter or model adapter treat "deferred" or
    "unknown" skeleton statuses as actionable without the real legality
    engine being present?
