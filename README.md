# Myravant

Myravant is a doctrine-controlled TTRPG rules, content, and persistent play
project. This repository brings together its control and doctrine corpus,
deterministic backend runtime work, schemas and tests, source/conversion
research tooling, and historical review material.

This repository previously operated under the **Astra Ascension** identity.
That name remains valid in historical, provenance-bearing, frozen-evidence,
and compatibility surfaces where rewriting it would make the record less
truthful or break a contract.

The repository is not primarily an extraction system. Aether Forge remains a
useful, subordinate toolchain and part of the project's history, while
Myravant is the current repository and platform identity.

## Architectural stance

Myravant keeps framework design, conversion/source research, canonical
consolidation, and live-play/model behavior separate. External material can
create evidence and design pressure, but does not become universal Myravant
law. Conversion or research output is not canon without explicit review and
promotion.

Authoritative live-play state belongs to deterministic backend/runtime owners,
not an LLM. Models can interpret intent and produce constrained proposals,
narration, and summaries within their contracts. Model prose cannot commit
dice outcomes, hidden facts, injuries, rewards, canon, or state changes.

## Repository map

- `docs/doctrine/` — doctrine, control surfaces, operations, and formal reviews.
- `docs/decisions/` — accepted project-level decision records.
- `src/astra_runtime/` — the current compatibility-bearing backend runtime
  package path. Its `astra_runtime` namespace is a legacy software identifier
  pending a separately audited PR2-ID compatibility tranche; it is not the
  current project identity.
- `schemas/` — schema families, including extraction/handoff schemas.
- `tests/` — the pytest suite.
- `docs/handoff/` and `scripts/` — conversion and handoff contracts/tooling.
- Root Python tools — Aether Forge extraction developer tooling.
- `docs/operations/` — Aether Forge extraction/handoff operational records and
  historical near-term notes; these are not general Myravant decision authority.

### Finding current work

This README is descriptive, not gate authority. Resolve current status from
the owning control artifacts rather than relying on a copied snapshot:

- `docs/doctrine/control/post_r2a_transition_manifest.yaml`
- `docs/doctrine/control/post_r2a_transition_program.md`
- `docs/doctrine/control/myravant_identity_migration_contract.md`
- `docs/doctrine/control/afqr_r2_doctrine_drift_resolution_plan.md`

Consult the relevant owner file under `docs/doctrine/`, and current decisions
under `docs/decisions/`, before changing a controlled surface.

## Source/conversion–runtime firewall

Source research, extraction, and conversion end before runtime begins.

The source/conversion/extraction toolchain is outside the runtime trust
boundary, and its outputs are review evidence rather than runtime dependencies
or automatic canon. Promotion into runtime-facing material is a governed,
one-way, identity-breaking process that creates sanitized Myravant-native
artifacts.

Runtime is origin-blind.

Runtime-facing material must not expose donor/source identity, source paths,
page references, extraction metadata, conversion IDs, mapping rationale, or
offline lineage.

Offline provenance is retained but isolated.

That provenance remains available for governance, reproducibility, conflict
resolution, and rights review, but not for runtime retrieval, model context,
or player-facing output. The controlling doctrine is
`docs/doctrine/control/conversion_runtime_origin_firewall_doctrine.md`.

## Identity migration boundary

Current-facing project branding is Myravant. The identity migration is not an
indiscriminate search-and-replace operation.

Historical Astra Ascension references, stable artifact IDs, frozen evidence,
hashes, provenance keys, merged PR/branch references, and compatibility-bearing
software identifiers remain unchanged unless an owning migration tranche
explicitly proves they can move safely.

The controlling migration contract is
`docs/doctrine/control/myravant_identity_migration_contract.md`.

## Development and tests

Python 3.11 or newer is required. Install the development dependencies, then
run the normal suite:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Focused commands may be appropriate for a bounded change, but report skipped
tests and missing optional dependencies rather than treating skips as full
coverage.

## Contributor and agent guidance

Read [`AGENTS.md`](AGENTS.md) before substantive work. It is the coding-agent
navigation and operating contract; it does not replace the repository's
owning doctrine, decisions, manifests, or control files.

Historical Astra Ascension and Aether Forge documents can explain earlier
identity, extraction, and handoff behavior, but they are not Myravant's
current identity or an automatic current-work queue.
