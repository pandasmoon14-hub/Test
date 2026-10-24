# Runtime structure and binding audit (report-only)

This script is development evidence, **not** simulation authority. It resolves
the Part 3 structural-observability gap after #569, #570 and #572 merged.

## What it inspects

Run from an installed development checkout:

```bash
python scripts/myravant_runtime_structure_audit.py --output /tmp/myravant-runtime-structure.json
python scripts/myravant_runtime_structure_audit.py --verify-roundtrips --output /tmp/myravant-runtime-roundtrips.json
python -m pytest -q tests/test_myravant_runtime_structure_audit.py tests/test_runtime_profile_owner_manifest.py tests/test_runtime_domain_package_manifest.py
```

The ordinary command uses the Python AST to parse **all**
`src/astra_runtime/**/*.py`, including function-local imports. It does **not**
import or execute those modules, generate content, make authoritative decisions
or read private campaign files.

The versioned, sorted JSON report includes:

- Exact module/edge inventory, entrypoint reachability from
  `astra_runtime.myravant_terminal`, unreachable modules, strongly connected
  import components, root sibling imports and application-to-terminal edges.
- Cross-reconciliation of both test-enforced registries: root-level profile
  owners/nonowners, `domain/` authorized files, missing and unregistered
  members, plus reachable/unreachable registered profile owners.
- The actual terminal `--locality` choices, the explicitly audited
  application class binding per choice, class-declared checkpoint formats,
  declared replay-method expressions, method inheritance hints, and static
  checkpoint writer/restore function definitions with source line numbers.
- A source-only inventory of literal `--locality` argument pairs in tests and
  evidence scripts, marking computed/unrecognized locality arguments separately.
  This is an index of references, **not** proof that any installed journey ran.

Binding classes are explicitly reviewed against the terminal's actual
`application_type` dispatch; the harness refuses locality-list drift. The
static report describes **expressions** when inherited replay-method tuples
cannot be resolved safely without executing code. It never claims that a
readable `checkpoint_format` attribute proves a saved checkpoint's format.

## Actual round-trip option

`--verify-roundtrips` deliberately imports established runtime classes.
For each of the fourteen public locality bindings it starts one bounded
development fixture, uses the existing public application `new` / `save`
(or the established generated-worksite preparation) / `restore`, compares
`authoritative_digest()` before and after, and records the **actual** saved
`format_identity`, `format_version` and SHA-256 checkpoint bytes, together with the bound class's actual
`replay_methods` declarations observed at runtime. It
rejects mismatches or failed saves. For generated worksite it uses the lawful
source-history constructor, not a fabricated snapshot.

This is a **fresh minimal-state** round trip for each binding, not full
coverage of every checkpoint historical version, mutated case, long journal,
interruption, or incompatible fixture. Existing replay and installed journey
suites continue to own that deeper qualification. It does not supersede
retained evidence or exact-head CI.

## Interpreting observations

A graph edge means a syntactic Python import, including local imports reached
only under specific conditionals; it **does not** mean the import runs in play.
Cycles may be intentional. Unreachable means not statically imported from this
single entrypoint, not unused. Profile registration is a human-reviewed claim.
Storage, checkpoint-writing, serialization, projection, presentation and
scheduling do **not** acquire ownership from these roles.

The report is **not a CI gate on cycles or architectural direction**. The
only test-enforced structural invariant here is that the reporter faithfully
observes current source/registries and distinguishes actual save/restore
results from static metadata. Reclassifying an owner, moving a source module,
promoting a private API, or changing dispatch requires a separate owner-gated
package and specific defect evidence.

## Follow-up interpretation

Review the report for actual ownership or circular import defects; preserve a
minimal reproducer, identify the owning subsystem and add a regression test
before proposing a new gate. The existing immutable `domain/` inventory and
separate profile-local owner registry are never amended by this report.

No parser overlap gate, module-size ceiling, runtime refactor, generated
locality budget decision or identity migration is part of this package.
