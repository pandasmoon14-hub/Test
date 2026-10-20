# Source-bound ordinary-chat feedback

This developer workflow supports an ordinary “continue working on the repo”
request without installed skills or persistent assistant memory. Start at
[START_HERE.md](START_HERE.md). Check actual tools, current user scope, owning
issue/PR, current sources and authorization before choosing the first unmet
condition. Headquarters remains separately governed.

The assistant is `scripts/myravant_assist.py`; use command-specific `--help`
for flags and the JSON examples below for input contracts. Its outputs are development
support, not canon, owner decisions, merge permission or certification.

## A compact continuation loop

1. Build a `packet` for the concrete task and inspected comparison base. State
   the player/developer result, scope, affected owners, dependencies and remaining
   acceptance conditions. Do not turn an old open-item summary into new authority.
2. Read the ranked relevant sources and runnable examples. Confirm that the
   current contract admits the intended change. Inspect affected callers,
   checkpoint/replay behavior and public interface, not just the edited module.
3. Define executable acceptance in a task specification before claiming success.
   Include named checks, the required behavior and the next unmet condition.
   Keep human approval, unavailable CI and unobserved play acceptance separate.
4. Implement the authorized work. Run `check` locally against that specification,
   then `resume` using its acceptance evidence to recover task state. A successful
   command only establishes what it actually checked on its recorded source.
5. Use `review` for a bounded second look at the packet. Resolve the relevant
   findings and report remaining gaps. Repeated automatic reviews do not replace
   independent review or justify an endless rewrite loop.
6. Use `refresh` after source changes. Reuse unchanged evidence where valid;
   regenerate evidence whose source identity no longer matches. Return the
   compact state and relevant failures to the existing owning issue/PR.

Write outputs to fresh paths outside the checkout. Preserve earlier evidence;
never overwrite source files or reuse an evidence directory for a later run.

```sh
python scripts/myravant_assist.py packet --task "Continue the authorized water recovery work" --base main --output ../water-packet-001.json
python scripts/myravant_assist.py check --spec ../water-task.json --output ../water-check-001
python scripts/myravant_assist.py resume --spec ../water-task.json --evidence ../water-check-001/acceptance.json --output ../water-state-001.json
python scripts/myravant_assist.py review --packet ../water-packet-001.json --output ../water-review-001.json
```

`refresh --packet OLD.json --output NEW.json` checks an earlier packet; it does
not update it. Exit 1 means stale; build a new packet after checking changed sources.
`benchmark` consumes case and answer JSON plus a fresh output path. Neither
command fetches an approval or grants repository execution access to a chat.

## Local execution when chat has no shell

Prepare the task JSON and source-bound patch in chat. A person with an authorized
checkout can inspect/apply the patch and run the single `check` command above.
Return `acceptance.json` and the relevant failing log excerpts to chat; retain
raw logs with the candidate evidence. Follow [local_execution.md](local_execution.md)
for environment setup, full checks, retained runners and the patch handoff.
Do not export credentials or unrelated log contents.

The bridge admits explicit Python pytest invocations and known retained report
scripts only. Task JSON is data, not a shell program: arbitrary shell commands,
command substitutions, installation steps and unrecognized scripts do not become
executable merely by appearing in an acceptance condition. Inspect the accepted
command forms below; rejected commands need an authorized supported
verification path, not a shell workaround.

## Curated retrieval and failure memory

[feedback_catalog.json](feedback_catalog.json) contains six bounded starting
routes: material, water, time, interface, developer and native/research. Task
terms and changed paths help prioritize them. This is selective retrieval, not
an exhaustive dependency graph. Follow additional owning references only when
the actual task requires them; do not load the entire control archive by default.

Each route supplies:

- Existing source paths and suggested focused test files.
- A runnable pytest node as a reference example; run it with
  `python -m pytest -q PATH::TEST_NAME`.
- An evidenced failure guard with its trigger, cause, correction and source.
- Cross-domain lenses that frame useful questions about the affected behavior.

Failure entries describe conditions explicitly guarded by existing tests, not
an assertion that each was a historical production incident. Inspect the cited
test and relevant contract before reusing a correction. Examples are patterns,
not templates that authorize a new substrate. Historical R4-A design tests bind
historical authority and may require retained Git history; they do not establish
current implementation permission.

The Tarrow material, water and time examples use bounded noncanonical development
fixtures. Their declared quantities, rates, geometry and methods are not universal
physics or setting canon. Suggested tests and matched routes are retrieval leads,
never coverage proof. Missing matches do not prove missing doctrine or capability.

## Evidence, freshness and review limits

Bind conclusions to the inspected head, comparison base, dirty state and recorded
source fingerprints. A locally cached `main` or `origin/main` is not a live remote
freshness check. Resolve current GitHub state separately when access permits;
otherwise report that limit explicitly. Refreshing a packet does not make an
unobserved remote check current or validate unrelated files.

Keep task state compact: authorized goal, acceptance conditions, observed results,
blocked/unavailable conditions and next action. Preserve failed checks as failures;
a missing check is not a pass. Actual installed-client, owner review, CI and human
play gates remain required where the owning contract calls for them. Timings and
command success alone cannot establish player-facing completeness.

Cross-domain analysis must distinguish repository fact, approved decision,
inference and proposal. Use TTRPG mechanics, simulation, ecology, human factors or
software archaeology to identify relevant dependencies and alternatives. State
what the player can attempt, how opportunities differ, which persistent
consequence changes and how that consequence is observed. An analogy supplies
questions, not new laws, owners, hidden truths or canonical facts.

## Measurable chat exercises

Use `benchmark` for explicit case/answer comparisons: retrieval correctness,
source attribution, required distinctions and forbidden claims. It records supplied
elapsed time and interaction counts without inventing missing measurements.
Keep case expectations reviewable and retain both inputs with the result.
Use actual ordinary-chat answers rather than fabricated successful transcripts.
A score measures the declared exercise and supplied answer; it does not measure
general model intelligence or prove an improvement in model performance.

Compare the same cases and source baseline when assessing a workflow change.
Report the number of cases, misses, false claims, measured cost and unavailable
checks. A source-contract test of this tooling is separate from an ordinary-chat
trial, and neither substitutes for gameplay regression or human acceptance.

## Input contracts and installed examples

Task specifications use version 1, a task description, optional owning-record and
authorization-reference strings, and 1..32 criteria with unique IDs:

```json
{"version":1,"task":"Verify water recovery","owning_record":"the existing PR URL",
 "criteria":[
   {"id":"water","description":"Conserve water and residue","kind":"test",
    "target":"tests/test_play_water_cleaning.py"},
   {"id":"play","description":"Observe the actual player journey","kind":"manual"}
 ]}
```

`test` accepts a tracked tests/*.py file or pytest node ID. `retained` accepts only
an exact scripts/report_myravant_*.py target discovered from the current CI.
`manual` remains pending; the runner cannot ratify approvals or human play.
Unknown kinds and arbitrary commands are rejected. Tests clear inherited
PYTEST_ADDOPTS and config addopts so filters cannot silently hide failures.
The timeout is bounded, and a timeout, missing output, source drift or failed
child cannot complete acceptance. Exit 1 with pending manual criteria is expected.
Retained report/log hashes are checked by resume; hashes are not signatures and
do not authenticate fabricated evidence. Review output is explicitly self-review.

[feedback_acceptance.json](feedback_acceptance.json) runs tooling regressions and
real water/material/time/installed-help examples, then leaves an actual ordinary
chat observation pending. Run this file with `check --spec` as a one-command bridge.

Benchmark inputs are version 1. Cases contain `cases:[{id, expected_facts:{...},
forbidden_claims:[...]}]`; observations contain `answers:[{id, facts:{...},
claims:[...], observation_reference, elapsed_seconds?, interactions?}]`.
Facts and forbidden claims are exact structured comparisons, not free-text semantic
judgments. Missing facts fail the relevant case. Repeated or unknown answer IDs
are rejected. Record observed responses faithfully; do not fill expected answers
into an unobserved chat. Case expectations belong to their dated source revision.

[chat_benchmark_cases.json](chat_benchmark_cases.json) and
[chat_benchmark_observation.json](chat_benchmark_observation.json) encode the actual
prior ordinary-chat PR550 observation, attributed to its public PR comment. They
exercise startup and truthful execution limits. They establish no measured uplift,
5.6 Sol model identification, new-tool acceptance or general intelligence score.

The twelve approved additions are represented by: ranked packets (task context),
AST import edges (impact), named check criteria (acceptance), cited regression
guards (failure memory), pytest nodes (runnable gallery), refresh (freshness),
resume (task state), review (bounded scrutiny), benchmark (measured exercises),
check (execution bridge), catalog lenses (cross-domain references), and route/file/
character budgets (selective retrieval). No new plugin or permission is required
for the local route. Shell-less chats retrieve the catalog and relevant sources;
they cannot execute this CLI solely because the guide describes it.
