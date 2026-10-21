# PLAY-TARROW-INVESTIGATION-1 — source-bound certification and review packet

Owning contract: [issue #552](https://github.com/pandasmoon14-hub/Test/issues/552).
Candidate: [draft PR #553](https://github.com/pandasmoon14-hub/Test/pull/553).
Baseline: merged #549 / `main` `21187d11c10899e0966b76cd089affaeb8df9134`.
Scope: noncanonical opt-in investigation, not universal canon, NPC intelligence,
new sensing, hidden-truth resolution, or a human-play release.

## Implemented and source-reviewed

- The `myravant-play --locality tarrow-investigation` public client accepts
  `recall <admitted subject> <facet>` and
  `compare reports about <admitted subject> <facet>`, alongside the existing
  actor and physical routes. Explicit supported facets are
  `residue`, `moisture`, `placement`, `assembly`, `trace` and
  `activity`; unsupported or unknown histories yield no hidden target hint.
- Recall and comparison are read-only projections of the requesting player's
  admitted chronological events. They do not observe the current world, consult
  private actor stores, advance WORLD-1 time, alter work, create evidence,
  or decide truth/guilt. Public output distinguishes witnessed, performed and
  received records and labels observation/delivery markers as logical order,
  never an exact event date.
- Comparison displays the most recent admitted records plus one earlier
  admitted contrary value when truncation would erase meaningful disagreement.
  It labels omitted records and does not invent or certify a preferred account.
- A separate versioned investigation checkpoint binds case, query version and
  the **owner-approved Option A** recipient-visible one-hop relay-disclosure
  policy ([#552 owner decision](https://github.com/pandasmoon14-hub/Test/issues/552#issuecomment-6306702761)).
  A prior speaker is durably captured only during an already qualified local
  report delivery and only when that identity is disclosed to the recipient.
  Recall never dereferences the speaker's private source event. Old
  actor/time/material/water/default checkpoints retain their format identities;
  cross-profile restore rejects. The approval is restricted to this opt-in
  runtime profile and does not adopt universal epistemic or communication canon.
- Three existing-owner Tarrow configurations and three neutral development
  roots (`neutral-contended`, `neutral-reverse`, `neutral-relay`) exercise
  finite resource contention, actor ordering, blocking/withdrawal, and
  attributed incorrect testimony. The neutral roots are deliberately bounded
  profile recipes, not an unbounded procedural content generator.
- Causal prehistories are produced through qualified, receipted owner actions
  and replayed via the ordinary durable journal. The builder refuses to
  overwrite a saved campaign. Player follow-up demonstrates actual cleaning
  and a reversible assembly: real joining, historical witnessed evidence,
  player untie/recovery, and continued recall through restarts.
- Existing owner roles remain: AFQR-10 actor-scoped evidence; AFQR-14 qualified
  communication; AFQR-20 sensing; actor participation/consent; material, water,
  environment and WORLD-1 transition owners; AFQR-01 persistence/replay.

## Exact source evidence — code head before this documentation update

The executable tree `5f2a746c73220c10a7cd9da90fbe55203c91adec`
was the tree of reviewed commit
`41cf70bbffa2b8551fe04d2d788433e8ae2199ed`.
[GitHub Actions run #39527170470](https://github.com/pandasmoon14-hub/Test/actions/runs/39527170470)
completed **successfully** with all six exact-head jobs:

| Job | Observed result |
| --- | --- |
| `core-linux` | 11,080 passed, 18 skipped, 2 xfailed, 1 warning; full pytest 738.83 seconds |
| `core-windows` | 11,079 passed, 19 skipped, 2 xfailed, 1 warning; full pytest 1,373.48 seconds |
| `focused-linux` | Investigation+actor focused selection 139 passed; all additional focused family steps green |
| `focused-windows` | Investigation+actor focused selection 139 passed; all additional focused family steps green |
| `retained-evidence-linux` | All original retained runner invocations preserved and successful; no original upload family removed |
| `investigation-evidence-linux` | Three installed objective-first journeys repeated twice; six recorded developer-goal assessments; six isolated negative mutations detected, each with a passing control |

Thirteen evidence artifacts uploaded for the same workflow, including
[`myravant-investigation-linux`](https://github.com/pandasmoon14-hub/Test/actions/runs/39527170470/artifacts/12313623244),
actor evidence on Linux and Windows, and all retained families.
The investigation archive contains the installed journey, assessment and
mutation reports. These are developer-authored and source-qualified
engineering exercises, **not blind, external independent or human acceptance**.
The separated assessment is a separately stated developer goal contract, not
independent from the development program.

The prior failed exact head `8f9d95cc...` exposed incorrect case-count/version
assertions and historical comparison truncation. Both were addressed before
the successful run. Later review added non-vacuous joined/separate witnessing
and actual reversible disassembly. Historical cancelled runs are not counted
as successful certification.

The Linux and Windows complete suites retain their stated skips/xfails and
warning. Windows test execution approached its 25-minute job budget; continue
tracking job-wall headroom rather than increasing timeouts or reducing tests.
The GitHub Actions runners provided certification; no separate local-shell
checkout or human-play study was performed in the authoring session.

**Certification after this document-only update:** this evidence remains
valid for the unchanged executable tree, but any new PR head must obtain its
own required exact-head CI status before a merge-ready declaration.

## Owner decision and remaining gates

**Option A approved:** The owner explicitly selected Option A on
2026-10-20 America/Denver, documented in
[#552 comment #6306702761](https://github.com/pandasmoon14-hub/Test/issues/552#issuecomment-6306702761).
This supersedes the pending A/B decision in #552 comment #6306553665.
The approved design is recipient-owned, replay-bound retention of at most the
immediately prior **already disclosed** speaker on a qualified local report;
no speaker-private source traversal, hidden-target enumeration, truth
promotion or retrospective enrichment of legacy saves is authorized.
The source implementation was already present in the reviewed executable
tree, and the owner choice requires **no executable code modification**.

The remaining gates are:

1. **Merge:** Repository rules require separately scoped owner merge
   authorization and final-head checks; selecting A is not merge permission.
   The source-bound COMMENT review in PR #553 is not an independent external
   approval. The PR remains draft until applicable gates are satisfied.
2. **Exact-head certification:** After this documentation-only decision record,
   check CI for the exact updated head. Earlier passing executable evidence is
   still valid for that unchanged executable tree but cannot be mislabeled as
   a new-head certificate.
3. **Further human / broad scope:** #508-C as an entire program, #538,
   #493, #495, general NPC investigation, universal epistemic projection,
   authored/native canon, new sensing, blind play and human-play readiness
   remain separate gates. Tested fixtures do not imply general coverage.

### Reproduction entry points

```bash
python -m pytest -q
python -m pytest -q tests/test_play_investigation_readonly.py tests/test_play_investigation_neutral.py tests/test_play_investigation_cases.py tests/test_play_investigation_journey_contracts.py tests/test_play_investigation_mutations.py tests/test_play_investigation_assessor.py
python scripts/report_myravant_investigation.py --output investigation-journeys.json
python scripts/assess_myravant_investigation.py --input investigation-journeys.json --output investigation-assessment.json
python scripts/report_myravant_investigation_mutations.py --output investigation-mutations.json
```

The installed `myravant-play` launcher and development requirements must be
available for the evidence scripts. The exact-head GitHub Actions job is the
recorded remote execution; commands above are reproduction instructions, not
claims of additional local execution.
