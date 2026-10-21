# Bounded CI performance pilot

Owner authorization: Cam's 2026-10-21 CI optimization request. This is developer
tooling only; no runtime/canon/merge authorization changes.

Starting main: `21187d11c10899e0966b76cd089affaeb8df9134`.
Pilot parent: certified draft #553, `c66bca4a5f0993cf5a0e38e474d2047874424e7b`.
This PR stacks on #553 to include its full investigation/replay workload without
changing that certified head. Retarget after #553 lands, then recertify the actual
candidate. Do not merge #553 implicitly to deliver a CI optimization.

Baseline run: https://github.com/pandasmoon14-hub/Test/actions/runs/39558904557
Reported full pytest times: Linux 982.67s; Windows 1377.20s. Historical timings
are context, not a same-head controlled performance comparison.

## Experiment and preserved gates

- Existing core serial jobs retain their names, timeouts, full tests and actor
  report exports. Add top-50 timings and JUnit artifacts even on failure.
- On the `ci-performance-pilot` PR branch only, two additional runners execute
  the entire suite with `pytest-xdist==3.8.0`, two workers, file-level scheduling
  and zero worker restarts. A crash must fail visibly, not be retried away.
- Each runner has its own checkout and actor output paths. Actor campaign tests
  write one file per scenario; the assessor has a separate file. Scratch worlds
  use pytest temporary directories. Process-local monkeypatches remain isolated.
  Static inspection is not proof of full-suite race freedom: both platform runs
  remain required experimental evidence.
- Pilot actor artifacts have distinct names. Linux also executes all actor
  mutations. All retained, focused and investigation jobs are unchanged.
- Same-run, same-platform serial/parallel JUnit comparisons reject missing,
  additional, duplicate, failed or changed-outcome tests, including skip/xfail
  type changes. Compare platforms separately because their legitimate skips differ.
- Compare actor reports' source SHA, scenario coverage, repeat counts, objective
  predicates and deterministic final digests before adoption. Scratch paths and
  timings need not be byte-identical. Keep the six investigation mutations and
  twice-per-circumstance installed journeys in their original jobs.

Official scheduling reference:
https://pytest-xdist.readthedocs.io/en/stable/distribution.html
`loadfile` keeps a file on one worker; it does not isolate shared filesystem writes
across files or parallelize a single expensive file.

## Acceptance and next decision

Require every original job, both pilot jobs and both equivalence jobs to succeed
at the candidate SHA. Review wall-clock job times and full-suite module/case
timings, actor evidence and worker isolation. JUnit timing excludes dependency
setup/upload. The pilot temporarily increases runner usage; it is not itself a
claim of lower CI cost or workflow elapsed time while serial controls still run.

If equivalent and materially faster on both platforms, promote the demonstrated
parallel command into core jobs in a follow-up candidate, remove temporary pilot
jobs, and run all required exact-head certification again. If unsafe, preserve
serial execution and use measured disjoint sharding or bounded hotspot repairs.
Do not relax timeouts, suppress errors, exclude tests, reduce repetition/mutations
or cache mutable replay state. A 10–15 minute target is unproven.

Additional optimizations are evidence-driven: JUnit aggregates expensive modules
for scheduling analysis; case durations identify fixture/subprocess hotspots.
Retain full Git history because historical-object tests use it. Setup caching and
deleting fast focused jobs do not address the measured critical path.

Local validation and moving CI status belong in the owning PR, including source
identity, commands, results, failures and the first unmet adoption condition.
