# PLAY-PHYSICAL-ACCESS-BATCH-1 — destination, method and durable access

## Scope and source

Owner requested the proposed Runtime physical-access milestone on 2026-10-17.
This is its first admitted integration batch, not completion of all #493 families.
Main inspected: `55cf119f7558387f10d4be7e4d47759a2ce44b68`.
Dependency: draft #532, repaired head `890079be144f762f54f079ded2114d210c923688`.
No merge authorization, native canon promotion, human-play gate opening, new
semantic primitive, state owner, production schema or fixture route is included.

A player can state a declared object's destination with an existing qualified
physical method, combine that attempt with one other supported step, and revisit
persistent passage/placement consequences after time and restart. Existing
fixture-specific sensory, custody, spatial and opportunity constraints remain.

## Family inventory and admitted batch

| Candidate | Current meaning / decision | This batch |
| --- | --- | --- |
| Push, slide, drag | Existing independent COMP-3 ground-placement methods | Destination interface for declared targets/places; public standalone, two-step and restored use |
| Throw | Existing COMP-3 player-carried to grounded placement | Generic goal respects actual custody; demonstrate compatible new neutral target with explicit throw license |
| Carry, take, drop | Existing custody and movement owners | Compose as alternate delivery approach; no invented automatic carry planner |
| Crawl vs walk | Existing method-specific movement qualification | Sustained bypass-versus-clearance contrast; no new movement method |
| Touch/feel | Existing AFQR-20 near-field contact | Reuse #532 for dark drag and tactile first sequence step; no persisted sensing privilege |
| Open/close, contain, illuminate | Existing RT-010 and sensory/environment contracts | Preserve existing qualification and regression coverage; do not infer container effects from prose |
| Pull | No registered independent COMP-3 method; direct parser intentionally unsupported | Remove destination grammar's incorrect pulling-to-drag alias. Requires a separately qualified meaning before admission |
| Rotate/turn | No orientation representation in this batch's existing owner path | Deferred: identify affected owner/representation and approved meaning before implementation |
| Brace/steady, stack/tip/roll | Existing narrow fixture brace work does not define universal stability/geometry | Deferred pending specific supported qualifications, not universally forbidden |
| Posture, sprint, sneak | Distinctions require supported state/capability/time or information semantics | Outside this physical-access batch; remain breadth candidates |
| Detach/assemble/repair | Existing limited brace/service behavior does not define generic material/component transformation | Inventory qualified structural work next; no recipes, damage or native material law inferred |

No synonym count is a capability count. The gain is wider public availability of
existing owner procedures and demonstrated reuse, not newly invented mechanics.

## Implementation and authority

- `myravant_play_fixture.py`: presentation-only unambiguous place resolution.
  Resolving a known place does not establish reachability or a displacement route.
- `myravant_physical_placement_goal.py`: fixture-based object/place resolution,
  actual custody-sensitive method selection, route filtering, unique reference
  preservation across duplicate display names, strict method preservation and original COMP-3 dispatch. The historical Yard-east clearance
  objective remains explicitly fixture-specific.
- `myravant_terminal.py`: pure two-step preflight recognizes existing physical
  goal adapters, preserving standalone Lantern-goal precedence. Execution still
  rechecks each step through its original application owner. Each accepted step
  retains the existing durable-result/checkpoint/trace boundary.
- `myravant_terminal_capabilities.py`: passes the actual fixture to the generic
  physical-goal recognizer. Existing specialized actor-mediated Lantern route
  keeps priority; consent/performing actor are not generalized.

RT-010/COMP-3 owns physical placement and custody; AFQR-18 owns location/spatial
qualification; AFQR-19 owns opportunity; AFQR-20 owns sensory qualification;
AFQR-01/02 retain commitment/command identity; existing checkpoint composition
retains persistence. No owner/state-family lifecycle is introduced.

## Availability and acceptance

| Surface | Evidence / supported envelope |
| --- | --- |
| Standalone direction | Existing push/slide/drag/throw application paths and regressions |
| Standalone destination | Fixture-resolved target/place, exact licensed method; stock Launcher plus injected neutral fixtures |
| Exactly two explicit steps | Same original goal adapter priority, separately durable transitions, first-refusal halt and durable partial completion |
| Actor-mediated | Existing specialized Lantern/NPC route preserved; no generic forced NPC action |
| Restored session | Stock installed campaigns and compatible neutral fixture round trips; recheck current placement/custody |
| Dark ground target | Explicit #532 drag contact only; generic method advice still requires visual observation or player-held object |
| Other modifiers / methods | Unqualified rather than silently discarded; pulling is not dragging; a waystone-specific directional phrase cannot bind to a different object |

`tests/test_play_physical_access_batch_1.py` changes target identities (new Painted
Crate and Validation Sled), explicit arrangements, place presentation and record
order. Three ground methods execute through public terminal dispatch, and all
restore under the same supplied fixture. An additional explicit neutral throw
route proves custody-sensitive execution without adding a stock-world route.
These are controlled fixture substitutions, not a claim arbitrary objects have
these affordances. Custom fixtures use injected terminal sessions; installed CLI
campaigns use the stock fixture. No CLI custom-world loader is claimed.

Independent outcome predicates check actual object placement and movement
opportunity, separately from receipt/digest changes. Goal and direction forms
must produce identical owner receipts under identical preconditions. Pure
recognizer collision tests preserve prior Lantern-goal routing in sequences.
An isolated in-memory mutation reinstating `pulling -> drag` was killed by the
method-preservation assertion; no mutated production source was written.
Multiple licensed directions for one destination/method are refused rather
than selected by record order.

`scripts/report_myravant_physical_access.py` runs three authored policies twice
through installed `myravant-play`, with actual feedback-conditioned selection:
push clearance + push supply; slide clearance + carried throw supply; crawl
bypass followed by push clearance + carry/drop supply. Each returns after
intervening admitted waits and fresh processes. Checks require Waystone at
Workshop, Lantern on the Orchard ground, ordinary eastward walking after restart
and return, unchanged epistemic state, trace continuity and repeated identical
semantic histories/receipts. Raw player inputs, outputs and owner evidence are
retained in the separate campaign artifact.

The original 39-case coverage corpus is unchanged. These tests/policies are
implementation-authored, not blind held-out acceptance, a population estimate,
human enjoyment evidence, all-method completion or Level 1 certification.

## Historical expectation reconciliation

#532 changed the active dark-drag contract from visual-only targeting to fresh
qualified near-field contact. Its original full CI failed on Linux and Windows
because `test_play_waystone_drag_recovery.py` retained the obsolete refusal.
Repair at dependency head above reproduces the failure and replaces it with:
remote/unknown refusal, unlicensed-route no-mutation, contact-qualified commit,
and stale-contact rejection after the object moves. Visual unavailability still
does not become remote access or persisted knowledge.

This batch replaces the old parser exclusion for `get lantern to orchard` with
explicit pure collision/precedence checks. The older specialized public adapter
keeps priority, including actor-mediated methods. The generic route can also
interpret declared Lantern destinations without claiming to supersede that
adapter's semantics.

## Verification commands and evidence

- Focused: `python -m pytest -q tests/test_play_physical_access_batch_1.py tests/test_play_breadth3_physical_placement.py tests/test_play_composable_two_step.py tests/test_play_contact_affordance_composition_1.py tests/test_play_help_topics.py`
- Full: `python -m pytest -q` with full Git history available (historical doctrine tests require older commits).
- Sustained campaign: `python scripts/report_myravant_physical_access.py --output physical-access-evidence.json`
- Existing discovery: `python scripts/report_myravant_synthetic_play.py --output synthetic-play-evidence.json`
- Original authored corpus: `python scripts/report_myravant_action_coverage.py --output action-coverage-evidence.json`
- Diff hygiene: `git diff --check`.

CI runs focused/new tests and the full suite on Linux/Windows, with Linux campaign
and unchanged baseline artifacts. Exact final-head results belong to the PR/run
record, not a prospective assertion in this document. Local optional skips are
not full environment coverage. No new crash-durability guarantees are claimed;
existing durability tests remain applicable because acknowledgement mechanics
are reused.

## Next dependency and closure

Finish #532 certification without merging automatically. Review this stacked
batch against its exact head and combined Runtime regression. Broader #493/#495
and the human-play gate remain open. Exit the temporary fixture constraints only
when the relevant actor/target qualifications have explicit supported meaning;
never turn neutral tests into native canon. After this milestone, select the
next family from demonstrated missing ordinary behavior, rather than repeatedly
adding routes to the same three stock objects.
