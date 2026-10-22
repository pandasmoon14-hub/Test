# PLAY-TARROW-TRANSFORMATION-1 — approved bounded material change and engineering review

Owner: [issue #555](https://github.com/pandasmoon14-hub/Test/issues/555).
Approved exact scope: [Option A, D1–D7](https://github.com/pandasmoon14-hub/Test/issues/555#issuecomment-6329721513).
Program: [#508-D](https://github.com/pandasmoon14-hub/Test/issues/508).
Implementation: [draft PR #556](https://github.com/pandasmoon14-hub/Test/pull/556).
Initial base: main `bb5117b736b98dd4034be37951e459e63abf85ea`.
This is a noncanonical fixture contract, not an adopted universal material rule.
This file records scope/acceptance; verify live PR/CI for actual completion.

## Player purpose

A player can approach the Yard Tool Station with a visibly unsuitable
Barrier Crossbar, stage it on the Trestle, choose either to refit its declared
lashing interface with an accessible Alignment Tool or replace it with an
already-existing whole Barrier Spare. Each route has distinct physical
prerequisites and irreversible staged outcomes. The old part survives whole
replacement; it may become a compatible workshop spacer, retaining its
identity. A consenting and situated Tali can instead carry their *own*
tool and perform a refit across the existing world clock. Subsequent barrier
fastening must actually block movement, not merely say "repaired".

## Exact admitted profile

| D# | Admitted development rule | Explicit nonclaim |
| --- | --- | --- |
| D1 | The old crossbar begins `unfit`; a distinct matching spare starts `fit`. Only declared role/connection pairs are admitted. | No general breakage, strength, force, shape or durability score. |
| D2 | Old crossbar, spare and alignment tool are individually existing whole objects. No material is minted or destroyed by transformation; tool is reusable. | No lengths, mass, cut yield, recipe conversion, scraps or implicit salvage. |
| D3 | Refit changes existing crossbar's declared fit while preserving ID. Replacement lifts the old whole object and places the existing spare. Repurposing changes the original's qualified role to `spacer`. Receipts reference old/output IDs. | No duplicate output IDs, generated entities, or original-and-replacement cloned from the same stock. |
| D4 | Two-interval refit, two-interval replacement and one-interval whole-part repurposing are distinct qualified methods. Barrier and workshop assemblies have different live physical owners/links. | Not every board/fastener is refittable, and this is not generic crafting. |
| D5 | Accepting/pausing/abandoning makes no free physical contribution. Every contribution advances the existing logical clock, rechecks site/tool/part context and preserves acknowledged prefixes. A new same-actor agreement can renew an abandoned partial undertaking without generating another first stage. NPCs must first acquire actual available tools through their existing owner. | No free handoff, no invented remote actor material access, no automatic consent or wall-clock catchup. |
| D6 | Existing RT-010/AFQR-18 support plus qualified fastening and a `fit` role govern the real barrier; `spacer` permits a specific workshop join. Existing `active_effects` governs movement; disconnecting legally restores passage. | No arbitrary protective shelter, load-bearing property, force, structural repair or invisible effect. |
| D7 | Separate `myravant.transformation-actor-time-material-owner-journal`, profile identity and exact replay of owner actions, receipts and transformation lineage. Old actor, investigation, material, water, time and default checkpoints are untouched and cross-load rejects. | No migration or historical digest rewriting. |

## Authority split

- RT-010: existing material support/connection/custody owner, plus this exact
  opt-in component-fit/lineage state. Physical lifting/placement still calls
  existing `material_for_actor` procedures.
- AFQR-18 and AFQR-19: real position/reach/visibility/qualified method.
  Target observation and known target identity do not grant hidden access.
- WORLD-1 and approved timed environment: one interval, passive effects,
  mixed-owner receipts and persisted chronological history.
- AFQR-11/12 and actor participation: requests are voluntary; actor-local
  acquisition and work are not borrowed from player inventory.
- AFQR-10 and AFQR-20: performed/witnessed evidence; narration does not
  certify a new truth or provide absent player knowledge.
- AFQR-01: durable journal/restore; no new semantic super-owner.
- RT-002, RT-003, RT-004, RT-008 and RT-009 remain outside this no-yield
  whole-part profile; those owners must separately authorize any later
  numeric costs, damage, abilities, generated assets or random salvage.

## Public route

`myravant-play --locality tarrow-transformation --checkpoint new.json`
selects the distinct noncanonical root.

Supported exact forms include `start refitting barrier crossbar using alignment
tool`, `start replacing barrier crossbar with barrier spare`, `start
repurposing barrier crossbar using alignment tool`, `work transformation`,
`pause transformation`, `resume transformation`, `abandon transformation`,
`inspect transformation`, and `ask tali ren to refit barrier crossbar using
alignment tool`. Existing `take`, `put ... on ...`, `lift ... from ...`,
`tie`, `untie`, `go`, `wait`, `save` and `--load` still reach their original owners.
Unknown operations cannot convert into a cosmetic success.

## Required acceptance and evidence class

- Direct tests: profile variation changes placements/opportunity; both routes
  preserve true component counts/identities; required tools and actual
  supported placement qualify the next stage; an interruption cannot erase
  acknowledged progress; abandoned work requires a new agreement; restoring
  a partial journal does not duplicate receipts or output.
- Function: refitted/replaced barrier produces a real movement refusal;
  recovered original may physically join an independent workshop assembly.
- NPC: willingness and actor-local tool acquisition, shared WORLD-1 clock,
  genuine component contention, recovery after restoring opportunity.
- Negative controls: unqualified tool, duplicate output identity, unfit
  component fastening, lost partial progress, stale target opportunity,
  and resealed final-state forgery.
- Public execution: `scripts/report_myravant_transformation.py` runs three
  installed objective-first journeys twice each. Separate declarative
  developer goals are in `tests/fixtures/tarrow_transformation_assessor_goals.json`,
  checked by `scripts/assess_myravant_transformation.py`.
- Required CI: Linux+Windows full suites and focused tests, retained evidence,
  prior investigation evidence and transformation journeys/mutations at the
  exact frozen candidate SHA. Review source and artifacts rather than treating
  authored objective flags as independent proof.

The installed campaigns and separate assessor are **engineering-authored**,
not blind/independent/human-play acceptance. A green draft is not merge
authorization and does not close #508-D's independent held-out generality gate.
No ordinary local player campaign, broader structural repair, water expansion,
NPC cognition, generated fabrication, native canon or human-play readiness is
conferred by this package. Keep #508, #538, #493, #495 and the water register
boundaries distinct.

## Evidence status

The first focused candidate exposed parser-assumption tests and an unavailable
player-to-NPC tool handoff. The repair uses existing actor-owned pickup instead,
with no new consent grant. These earlier runs are not certification of later
heads. Refer to draft PR #556's latest exact-head GitHub run, review and
checkpoint comments for **actual**, not anticipated, results. Final full-source
certification remains required.

## Repair review amendment — source-bound, pending exact-head certification

The review at PR #556 review #5608321209 identified five important gaps beyond
historical domain allowlist failures. The subsequent candidate integrates the
profile-specific whole-component records into the already-authorized
`domain/persistent_world_material.py`, rather than installing a second runtime
domain module or disabling historical guardrails. The repair also requires a
committed replacement stage before the spare's barrier connection; explicit
local, consent-qualified named requests to control NPC work; charged WORLD-1
intervals for stale qualified work attempts; bounded actor blocked interval
handling and atomic rollback of material stages after the clock has advanced.
The installed replacement journey must demonstrate real blocking, lawful
reopening, remnant use, and the `split-spare` remote resource variation. Passing
these source requirements and full CI is necessary; assertions in this note
are not an independent engineering certificate.

## Final bounded-failure control amendments

The player-side blocked-due diagnostic saturates at 32 while preserving every
WORLD-1 due interval and allowing further lawful attempts indefinitely; an
actor-specific blocked limit still causes nonconsenting NPC withdrawal. The
transformation mutation harness now explicitly tests eleven isolated controls,
adding premature spare fastening, remote NPC control, attempted-work clock cost,
post-owner rollback and unbounded player retry to its original six source-copy
defects. A green status requires effective detection with passing unmutated
controls; the changes do not authorize a general crafting or governance layer.
