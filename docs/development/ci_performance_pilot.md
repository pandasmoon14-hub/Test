# CI performance: verified pilot and production configuration

Owner authorization: Cam's 2026-10-21 CI optimization request and direction to
proceed after the pre-merge assessment. Developer tooling only; no runtime,
canon or merge authorization changes.

## Verified pilot

Pilot source: `d50ac17edfd5e07b88f4d69629baf4e63673c6b0`.
Parent: certified draft #553, `c66bca4a5f0993cf5a0e38e474d2047874424e7b`.
Main inspected: `21187d11c10899e0966b76cd089affaeb8df9134`.
All ten jobs passed in
https://github.com/pandasmoon14-hub/Test/actions/runs/39664480112

| Full-suite JUnit elapsed time | Serial | Two workers | Reduction |
| --- | ---: | ---: | ---: |
| Linux | 848.360s | 584.763s | 31.1% |
| Windows | 892.281s | 841.748s | 5.7% |

Each serial/parallel comparison covered 11,119 JUnit entries with zero identity
or outcome differences: Linux 11,099 passed, 18 skipped, 2 xfailed; Windows
11,098 passed, 19 skipped, 2 xfailed. JUnit timing excludes setup/upload; one run
does not establish sustained throughput or guaranteed elapsed-time savings.
The older Windows result of 1,377.20s is not the controlled serial baseline.

Downloaded serial/pilot actor artifacts showed equal source SHA, three campaign
families twice each, seven assessment variants twice each, objectives, replay
results and final digests. Stable content matched after excluding operational
session IDs, wall timestamps and elapsed measurements. All six actor mutations
had passing controls and intended named-test failures in both Linux modes.
Detection includes assertions, a clock-history invariant error and a missing
expected replay rejection. This is author-side engineering review, not blind,
independent or human acceptance.

## Production candidate

- `core-linux` uses pinned `pytest-xdist==3.8.0` from `requirements-ci.txt`, with
  `-n 2 --dist loadfile --max-worker-restart=0`. Every test remains selected;
  a worker crash fails visibly. Actor report exports and mutations stay in place.
- `core-windows` stays serial: the measured 5.7% gain is insufficient evidence
  for promoting extra worker contention on the critical platform.
- Both core jobs retain top-50 case timings and upload JUnit XML even on failure.
  Profile artifacts are `suite-core-linux` and `suite-core-windows`.
- Remove temporary duplicate full-suite pilot runners and equivalence jobs.
  The original six job names, budgets, retained evidence, focused contracts,
  installed journeys, mutations, full Git history and exact-head checkout remain.
- Keep `scripts/compare_pytest_profiles.py` and its adversarial tests as reusable
  tooling for future controlled comparisons. It rejects missing, extra, duplicate,
  failed and changed-outcome entries, plus suite/collection errors. Inputs must
  be from the same source/platform and trusted successful jobs.

Linux scheduling reduces its observed suite cost; Windows still determines
overall workflow elapsed time. No whole-workflow speedup is claimed from this
Linux-only promotion. Preserve all replay and mutation certification.

## Follow-up triggers and delivery gate

Measured pilot hotspots include actor campaigns (Linux 196.032s of test time;
Windows 225.196s) and nested upstream pytest suites. Windows inventory-contract
tests consumed 170.610s in the parallel pilot. File scheduling keeps campaign
parameters together; future experiments can prioritize expensive files, assess
safe case scheduling, or balance measured disjoint runner shards. Fixture or
subprocess reuse must preserve actual execution and outcome assertions. Do not
delete tests/repetitions, suppress errors, cache mutable replay state or raise
timeouts to manufacture a speed improvement.

PR #554 remains stacked on #553 so the workload includes the certified
investigation package. Do not merge it into #553's certified branch. After
#553's separately approved landing, retarget #554 to main, reconcile the diff
and certify the resulting candidate as needed. A request to prepare production
CI does not implicitly authorize merging #553 or #554.

Fresh exact-head production certification remains required. Pilot success is
not certification for the promotion head. Moving results, source identities and
the first unmet delivery condition belong in PR #554.

Official scheduling reference:
https://pytest-xdist.readthedocs.io/en/stable/distribution.html
`loadfile` keeps each file on one worker; it does not guarantee cross-file
filesystem isolation or parallelize an expensive file. Existing actor exports
use scenario-specific files and a separate assessor file; scratch worlds use
pytest temporary directories.
