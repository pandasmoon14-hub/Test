# Runtime Baseline Failure Inventory

## Status

- **Inventory ID:** `RUNTIME-BASELINE-FAILURE-INVENTORY-2026-07-20`
- **Repository:** `pandasmoon14-hub/Test`
- **Baseline branch:** `main`
- **Baseline commit:** `928bb79ce00a2de749d127dcc5cb8299de788a15`
- **Baseline source:** merged RT-002F / PR #325
- **Document type:** maintenance and rehabilitation audit
- **Runtime authority:** none
- **AFQR authority:** none; this inventory records repository condition only

## Purpose

This document freezes the known failing runtime-test baseline before AFQR-01–20 consolidation or further RT-series implementation.

Its purpose is to prevent three failure modes:

1. treating pre-existing failures as regressions introduced by AFQR consolidation;
2. repairing tests by weakening guardrails or broadening runtime authority;
3. resuming RT-002G before the current repository baseline is understood and green.

This inventory is deliberately separate from:

- AFQR doctrine consolidation;
- extraction or conversion work;
- canon promotion;
- runtime behavior implementation;
- live-play or model-adapter work.

The extraction/conversion subsystem remains disconnected from runtime. Runtime-baseline repair must not create imports, provenance links, donor identifiers, conversion metadata, or other origin-bearing paths into `astra_runtime`.

## Confirmed baseline evidence

The merged RT-002F PR records the following result for the same branch state as `main`:

```text
pytest tests/runtime -q
47 failed, 1443 passed
```

The same PR identifies two confirmed failure clusters:

1. stale `tests/runtime` domain-package allowlists;
2. a `state_store` signature mismatch involving `hidden_info_safe`.

Targeted RT-002F and upstream slice tests passed in that PR. Therefore, the 47 failures are recorded as **pre-existing/mainborne at the RT-002F merge baseline**, not as RT-002F-specific failures.

## Evidence confidence classes

This inventory uses the following confidence labels:

- **confirmed:** stated in merged repository evidence or directly inspectable repository content;
- **strongly indicated:** supported by issue records or repeated repository patterns, but not reproduced in the current audit environment;
- **pending reproduction:** requires a normal local checkout or CI runner to capture exact test node IDs and tracebacks;
- **not a runtime-baseline failure:** maintenance debt that should be scheduled separately and must not be mixed into the baseline repair PR.

## Failure-cluster inventory

### RB-FAIL-001 — Stale runtime domain-package allowlists

- **Confidence:** confirmed
- **Observed symptom:** runtime tests reject the current `astra_runtime.domain` package surface because individual tests maintain stale expected-module or allowed-export lists.
- **Probable cause:** the allowlist model is duplicated across test files and must be manually expanded whenever a narrow RT module is added.
- **Risk:** repair by adding names independently to every test would recreate the same failure after the next module addition.
- **Correct remediation direction:**
  1. identify every duplicated domain-module allowlist;
  2. create one authoritative runtime-domain manifest or shared fixture;
  3. classify each module by status and authority rather than recording only its name;
  4. make all guardrail tests consume that shared source;
  5. preserve strict rejection of undeclared modules.
- **Prohibited shortcut:** remove or broadly weaken package-surface tests.
- **AFQR relevance:** the replacement manifest should later support AFQR conformance metadata, including `fixture_only`, implemented authority, prohibited authority, and applicable AFQR decisions.

### RB-FAIL-002 — `state_store` / `hidden_info_safe` signature drift

- **Confidence:** confirmed
- **Observed symptom:** one or more runtime tests call or inspect a `state_store` interface whose expected signature no longer matches the implementation around `hidden_info_safe`.
- **Probable cause:** interface and test expectations evolved independently.
- **Required reproduction:** capture the exact callable, expected signature, actual signature, and all affected node IDs before changing code.
- **Correct remediation direction:**
  1. determine whether `hidden_info_safe` is an input assertion, returned capability, stored property, or obsolete field;
  2. resolve the authoritative contract from current state-owner and hidden-information doctrine;
  3. update implementation and tests together;
  4. add explicit compatibility or rejection tests;
  5. avoid representing hidden-information safety as a caller-controlled boolean when it must be proven by the owner/projection boundary.
- **Prohibited shortcut:** accept arbitrary caller-supplied `hidden_info_safe=True` as proof that state or a projection is safe.
- **AFQR relevance:** AFQR-10 and the AFQR-01–20 projection amendments require safety to be established by typed owner and projection evidence, not model or caller assertion.

### RB-FAIL-003 — Exact node-level distribution unknown

- **Confidence:** pending reproduction
- **Observed symptom:** the merged PR records aggregate counts but not the complete 47-node inventory in repository documentation.
- **Required output:** a captured list containing, for every failure:
  - test node ID;
  - failure class;
  - first relevant traceback frame;
  - implicated production file;
  - implicated test file;
  - whether it reproduces on clean `main`;
  - whether it is fixed by the baseline-repair branch;
  - whether the fix changes production behavior, test infrastructure, or only expectations.
- **Disposition:** no baseline-green claim may be made until this output exists.

## Reproduction protocol

Run from a clean checkout of the recorded baseline commit.

```bash
git switch main
git pull --ff-only
git rev-parse HEAD
python --version
python -m pip freeze > runtime-baseline-pip-freeze.txt
python -m pytest tests/runtime -q --tb=short -ra \
  > runtime-baseline-tests.txt 2>&1
```

Then run a node-oriented pass:

```bash
python -m pytest tests/runtime --collect-only -q \
  > runtime-baseline-collected-nodes.txt
python -m pytest tests/runtime -q --tb=line -ra \
  > runtime-baseline-failures-line.txt 2>&1
```

Record the environment and result in the companion YAML inventory.

If the result differs from `47 failed, 1443 passed`, do not overwrite the historical baseline. Add a new reproduction record with:

- exact commit;
- environment;
- dependency versions;
- new counts;
- explanation of any difference.

## Failure classification rules

Every failing node must receive exactly one primary classification:

```text
implementation_defect
stale_allowlist_or_manifest
signature_drift
obsolete_test_expectation
test_environment_defect
test_infrastructure_fragility
documentation_contract_drift
known_unsupported_behavior
unknown_pending_investigation
```

A node may also receive secondary risk tags:

```text
hidden_information
runtime_authority
state_ownership
serialization
import_boundary
idempotency
replay
conversion_runtime_firewall
donor_law_leakage
AFQR_conformance
```

## Related open maintenance issues

These issues are relevant to repository rehabilitation but must remain separately scoped.

### Issue #128 — test-helper and subprocess-path maintenance

Relevant findings:

- duplicated pytest helper functions;
- repo-relative subprocess paths that depend on current working directory;
- hard-coded doctrine-registry record count.

Disposition: schedule after or alongside baseline repair only where the same infrastructure directly causes a failing node. Do not expand the runtime-baseline repair into a full test-suite cleanup.

### Issue #130 — expected-failure coverage for extraction gaps

Relevant findings:

- Lane A multi-column/table reconstruction remains a known gap;
- lorebook splitting remains fantasy-biased.

Disposition: not a runtime-baseline failure. Keep separate from runtime rehabilitation. Extraction/conversion remains disconnected from runtime.

### Issue #132 — misleading end-to-end fixture test name

Relevant finding:

- the test verifies fixture generation and required files, not an end-to-end extraction/conversion/runtime path.

Disposition: documentation/test-hygiene follow-up. Its correction should reinforce, not blur, the extraction/conversion–runtime firewall.

### Issue #134 — handoff contract documentation drift

Relevant finding:

- documented packet layout differs from the packet shape currently produced and tested.

Disposition: conversion/handoff documentation repair only. It must not modify runtime packages or runtime contracts.

### Issue #151 — obsolete A06–A15 closeout scope

The issue predates Batch A/B/C completion and AFQR-01–20 ratification.

Disposition: supersede or broaden into an `AFQR-01–20 and Batch A/B/C Doctrine Conformance Audit`. Do not execute its original narrow transition premise unchanged.

## Remediation order

### Phase 1 — Capture

1. reproduce the runtime suite at the exact baseline;
2. record all 47 node IDs and tracebacks;
3. group failures without modifying code;
4. verify whether all failures belong to RB-FAIL-001 or RB-FAIL-002;
5. create additional cluster records when required.

### Phase 2 — Repair shared test infrastructure

1. centralize the runtime-domain module manifest;
2. retain strict undeclared-module rejection;
3. eliminate duplicated allowlists;
4. add a manifest-consistency test;
5. confirm that narrow RT modules remain `fixture_only` or `narrow_reference_only_skeleton` where applicable.

### Phase 3 — Resolve `state_store` contract drift

1. freeze the current expected and actual signatures;
2. determine the authoritative hidden-information contract;
3. implement the smallest compatible correction;
4. add positive, negative, and misuse tests;
5. ensure callers cannot self-certify hidden-information safety.

### Phase 4 — Verify

Run:

```bash
python -m pytest tests/runtime -q
python -m pytest -q
```

The target is:

```text
0 unexpected failures
```

Expected failures are permitted only when they are narrow, documented, and unrelated to runtime-baseline regressions.

## Exit criteria

Gate R0 is complete only when all of the following are true:

- the exact failing-node inventory has been captured;
- each failure has a primary classification;
- the runtime-domain manifest has one authoritative source;
- duplicated module allowlists have been removed or delegated to that source;
- the `state_store`/`hidden_info_safe` contract is explicit and tested;
- `python -m pytest tests/runtime -q` has zero unexpected failures;
- the full suite has zero unexpected failures;
- no guardrail was weakened to obtain green status;
- no extraction or conversion dependency was introduced into runtime;
- no RT-002G behavior was implemented;
- no AFQR decision was marked implemented merely because tests pass.

## Next PR boundary

The next implementation PR after this inventory should be:

```text
MAINTENANCE: Restore green runtime baseline
```

It should contain only:

- the centralized runtime-domain manifest and test-fixture changes required by RB-FAIL-001;
- the smallest contract correction required by RB-FAIL-002;
- focused regression tests;
- the reproduced node-level before/after inventory.

It must not include:

- AFQR-01–20 import or consolidation;
- Batch doctrine rewrites;
- new RT functionality;
- RT-002G;
- extraction or conversion changes;
- canon promotion;
- model-facing behavior.
