# Myravant Agent Operating Map

This is the **Myravant** repository. It contains doctrine and control material,
runtime work, schemas, tests, source/conversion research developer tooling,
and historical material. This repository previously operated under the
**Astra Ascension** identity; that name remains valid in historical,
provenance-bearing, frozen-evidence, and compatibility surfaces where changing
it would distort the record or break a contract.

Aether Forge is subordinate developer tooling and history; it is not the
repository's identity. Do not describe this repository as only an extraction
system.

## Preflight before substantive work

1. Resolve current `main` and record the exact commit inspected.
2. Read the current gate and partition authorities, especially
   `docs/doctrine/control/post_r2a_transition_manifest.yaml`,
   `docs/doctrine/control/post_r2a_transition_program.md`, and the applicable
   owner/control artifact. During PR2-ID, also read
   `docs/doctrine/control/myravant_identity_migration_contract.md`.
3. Identify the relevant semantic owner or controlling authority and decide
   whether the requested work is authorized before editing.
4. Distinguish current doctrine (`docs/doctrine/`), decision records
   (`docs/decisions/`), implementation (`src/astra_runtime/`), schemas
   (`schemas/`), tests (`tests/`), review/evidence material
   (`docs/doctrine/reviews/`; authority and currentness must be read from each
   artifact), and source/conversion/handoff developer material and tooling
   (`docs/handoff/`, `scripts/`, and root extraction tools).
5. Treat `src/astra_runtime/` and the `astra_runtime` namespace as
   compatibility-bearing legacy software identifiers until a dedicated PR2-ID
   compatibility tranche explicitly migrates them with alias/import coverage.

Repository authority, currentness, and phase controls live in their owning
artifacts. README, this map, `CLAUDE.md`, examples, research, benchmarks,
converted content, and model output cannot outrank them. Preserve these
separate concerns:

```text
doctrine/framework design != source/conversion research != canonical consolidation != live-play/model behavior
```

## Authority boundaries

Authoritative state belongs to its deterministic backend/runtime owners.
Models may interpret, propose, narrate, and summarize within their contracts;
model prose is not authoritative state. Narration cannot silently create
injuries, rewards, hidden truths, dice outcomes, canon, or state mutations.
Do not infer new runtime architecture from this summary.

Never collapse:

- external/source assumptions into universal Myravant law, or conversion output into canon;
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

Myravant must remain viable across a large, mixed external-source corpus. Do
not manufacture or reconcile an exact source count here. Test heterogeneous
source families and preserve source-local, quarantine, and escalation outcomes
rather than optimizing for one familiar donor family.

## Identity migration rules

Current-facing project branding is Myravant, but historical truth and
compatibility outrank cosmetic consistency.

Do not:

- globally replace `Astra` with `Myravant`;
- rewrite historical commits, PRs, branch names, frozen reviews, provenance,
  artifact IDs, hashes, or evidence paths merely for naming consistency;
- rename `astra-runtime`, `astra_runtime`, or `src/astra_runtime/` without the
  dedicated compatibility tranche required by the migration contract;
- use the identity migration to change gameplay doctrine, semantic ownership,
  runtime architecture, schema semantics, canon status, or source governance.

Use the dispositions defined in
`docs/doctrine/control/myravant_identity_migration_contract.md` when an Astra
identity occurrence is encountered.

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
substrate, or resolution of a genuine authority conflict. Do not invent a
Myravant-sounding solution.
