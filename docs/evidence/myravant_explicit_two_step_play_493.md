# Myravant — Explicit two-step player intention, composed owners, source evidence

Status: candidate PR, not merged, not doctrine, not new world authority.

## Evidence and selection
Source: exact-head #527 artifact `myravant-action-coverage-baseline-linux` ID `12053218556`, current baseline `main` `11e0424f482a1292c7640e24e5dbdac451bdf141`. Its 39 *author-curated* isolated actions include **3/3 sequencing attempts unsupported**, including `go south then inspect chest`. Other gaps include posture 3/3 and traversal method 3/4; these are separate problems. The owner-approved #495 direction prioritizes composition of existing qualified owners before new generalized semantics. No independence/blind-acceptance claim follows from these cases.

## Meaningful new capability
A player can now express **exactly two sequential, individually executable simple actions** in one utterance separated by the word `then`. An explicit two-step method executes in order through its original owners, with each authoritative change durably checkpointed **before** the next step starts. This is **not one atomic command**: if the second step fails its current environment check, the first committed consequence remains. The client presents distinct step results and records each step in the existing trace with the **same original raw input**, a numbered action route, its own result/refusal and state digests.

Supported step families: movement, player sensory observation, custody pickup/drop, object state operation (light/open etc.), grounded storage and qualified directional displacement, plus original WORLD-2 waiting. These are existing public terminal actions, *not invented results*. No automatic compound NPC control, hidden information disclosure, unsupported spell, third step, simultaneous action or arbitrary plan is accepted. Unsupported/ambiguous **step syntax is rejected for the whole input before the first commit**. The concrete simulation and each subsequent contextual refusal still belong to the existing R4/AFQR/RT owners.

## Multi-system objective demonstrated in automated installed play
1. `take lantern then go south`: custody + persistent player relocation in Workshop → Yard, separate owner receipts/checkpoints.
2. Save, terminate the installed client and launch a second session.
3. `open chest then put lantern in chest`: object operation + container storage. Lantern leaves player custody and remains inside the same Chest across another checkpoint restore.

Additional adversaries: original walking/custody command digest and receipt equivalence; unknown second action prevents the first from running; a lawful first movement remains after later unknown-target pickup fails; denied first move stops before pickup; remote inspection never reveals hidden world placement; deterministic repeated time/movement; three steps refused rather than partial execution; no implicit "while" simultaneity or "and" alias.

## Evidence integration and backward compatibility
The #527 installed-action report still has **39 player inputs**. A newly executing two-step input can produce **two valid authoritative trace records**; the report now preserves `step_count`, `route_steps`, aggregated per-input pre/post digests and `partial_failure`, while **not inflating one player attempt to two**. Existing one-step evidence fields remain and historical report artifacts are unchanged.

The older intentionally negative synthetic corpus changes one row from a formerly valid-but-unsupported sequence to an **unqualified second method**, preserving its original refusal/no-mutation purpose. A dedicated new positive test measures the newly executed `then` sequence. The baseline is not secretly relabeled as new blinded evidence.

## Acceptance and stop conditions
- Exact-head focused tests then complete Linux+Windows, public installed client and two-session restore, native receipts and checkpoint chain.
- No new semantic owner, asynchronous task queue, universal attempt resolver, native anatomy or mechanics, automatic third action, or world mutation on failed parse.
- A committed first step is acknowledged durably even when second method fails; this is not an unannounced all-or-nothing transaction.
- No human-play gate, unseen 500-case Set A/B threshold, doctrine changes, or authorized merge claimed by this candidate.
