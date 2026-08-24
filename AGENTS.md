# Astra Ascension Agent Operating Map

This is the **Astra Ascension** repository. It contains doctrine and control
material, runtime work, schemas, tests, conversion/extraction developer
tooling, and historical material. Aether Forge is subordinate developer
tooling and history; it is not the repository's identity. Do not describe this
repository as only an extraction system.

## Preflight before substantive work

1. Resolve current `main` and record the exact commit inspected.
2. Read the current gate and partition authorities, especially
   `docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md` and
   `docs/doctrine/reviews/afqr_r2a_partition_manifest.yaml`; never copy a
   transient partition into permanent guidance.
3. Identify the relevant semantic owner or controlling authority and decide
   whether the requested work is authorized before editing.
4. Distinguish current doctrine (`docs/doctrine/`), accepted decisions
   (`docs/decisions/`), implementation (`src/astra_runtime/`), schemas
   (`schemas/`), tests (`tests/`), historical/review evidence
   (`docs/doctrine/reviews/`), and source-local conversion material
   (`docs/handoff/`, `scripts/`, and root extraction tools).

Repository authority, currentness, and phase controls live in their owning
artifacts. README, this map, `CLAUDE.md`, examples, research, benchmarks,
converted content, and model output cannot outrank them. Preserve these
separate concerns:

```text
doctrine/framework design != conversion != canonical consolidation != live-play/model behavior
```

## Authority boundaries

Authoritative state belongs to its deterministic backend/runtime owners.
Models may interpret, propose, narrate, and summarize within their contracts;
model prose is not authoritative state. Narration cannot silently create
injuries, rewards, hidden truths, dice outcomes, canon, or state mutations.
Do not infer new runtime architecture from this summary.

Never collapse:

- donor assumptions into universal Astra law, or conversion output into canon;
- Conversion IR into Runtime IR;
- semantic ownership into storage, serialization, commitment, scheduling,
  projection, or consumption;
- observation or sensing into knowledge or truth;
- capability into action, opportunity, target, or resolution;
- identity into control or authority;
- relation into jurisdiction or obligation;
- topology into embodiment, time, or environment;
- missing implementation into missing doctrine;
- schema existence into runtime implementation.

Astra must remain viable across a large, mixed donor corpus. Do not manufacture
or reconcile an exact donor count here. Test mixed donor families and preserve
source-local, quarantine, and escalation outcomes rather than optimizing for
one familiar donor.

## Working rules

- Keep one bounded concern per PR; preserve exact scope and avoid unrelated
  cleanup.
- Do not implement a future substrate merely because doctrine describes it.
- Do not weaken tests just to pass; first determine whether code or test is
  wrong.
- Report exact commands, passes, failures, skips, and environment constraints.
  Distinguish repository facts from inference.
- A local-only commit is not a shared repository baseline.
- Do not merge unless explicitly instructed.

The normal suite entry point is:

```bash
python -m pytest -q
```

See `requirements-dev.txt` for test dependencies. Optional-dependency skips do
not equal full coverage.

## Stop and escalate

Stop implementation and surface the issue if work requires a new owner, a new
semantic primitive, doctrine adoption, ownership transfer, a new generalized
substrate, or resolution of a genuine authority conflict. Do not invent an
Astra-sounding solution.
