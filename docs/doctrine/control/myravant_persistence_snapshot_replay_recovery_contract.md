# Myravant Persistence, Snapshot, Replay, Recovery, and Reconstruction Contract — PR2-PERSIST

Artifact ID: `PR2-PERSIST-PERSISTENCE-SNAPSHOT-REPLAY-RECOVERY-001`
Status: `active_control_doctrine`
Layer: `0_control`
Workstream: `PR2-PERSIST`
Authority reference: `owner_directive_2026-09-15_pr2_persist_activation`
Authority effect: `runtime_persistence_contract_only`
Starting baseline: `56a5cf065bc37588ee6b62b3a51f1576d0168d6e`

Runtime implementation authority: none.
Production schema authority: none.
Semantic commitment ownership: none.
Semantic replay ownership: none.
Semantic recovery ownership: none.
Command identity authority: none.
Logical-time authority: none.
Timeline or branch authority: none.
Correction authority: none.
Version-applicability authority: none.
Randomness-resolution authority: none.
Message/projection authority: none.
Fidelity authority: none.
Performance-budget authority: none.
Database or storage-engine selection authority: none.
R3 execution authority: none.

## 1. Purpose

PR2-PERSIST defines the bounded runtime-architecture contract for durable
representation, snapshots, reconstruction, replay consumption, crash recovery,
restoration, corruption handling, and persistence evidence.

Its purpose is not to create a new owner of world truth.

Already-governed authoritative history must be able to survive process,
machine, storage, deployment, and representation failure without allowing the
mechanism that stores or reconstructs that history to become its semantic
owner.

The required relationship is:

    authoritative semantics
    -> lawful commitment under existing owners
    -> durable attributable representation
    -> lawful reconstruction
    -> equivalent authoritative state

Persistence owns none of the semantic stages on either side of that
representation boundary.

## 2. Existing semantic owners remain authoritative

AFQR-01 retains qualified state/write ownership, transition commitment,
owner-specific reduction, recovery, replay, transition receipts, and committed
audit.

PR2-PERSIST defines architectural requirements for representing and
reconstructing AFQR-01-governed facts. It does not redefine when a transition
commits, what replay means semantically, or which domain owner may write state.

AFQR-02 retains command identity, attempt identity, retry identity, suspension,
escalation, and durable command progress. Persisting command-progress
representations does not transfer command ownership to PR2-PERSIST.

AFQR-04 retains logical time, causal ordering, simultaneity, scheduling,
resolution groups, and bounded cascades. Storage order, file position,
database sequence, replication order, and restore time are not automatically
world time or causal order.

R2B-CORE remains authoritative that retaining a proposal does not commit it,
persistence alone confers no authority or canonicality, replay and recovery do
not reroll committed uncertainty, and replacement resolution remains
distinguishable from the original.

R2B-CROSS-PHASE retains version identity, applicability, historical pinning,
and effective intervals. Replay and recovery do not silently refresh historical
ruleset, package, override, or schema bases.

R2B-CONTINUITY retains timeline identity, branch classification and ancestry,
correction/compensation/retcon/supersession governance, and continuity-safe
projection boundaries.

PR2-EVENT retains runtime representation and delivery distinctions.
Message loss cannot erase an already committed fact, and projection state
remains derivative.

## 3. Core nonauthority laws

Storage durability is not semantic ownership.

Durability is not semantic commitment.

Snapshot materialization is not canonicality.

Replay reconstruction is not semantic re-execution.

Recovery is not correction.

Replica majority is not semantic authority.

Backup restoration is not branch promotion.

Infrastructure may preserve, reproduce, or materialize authority-bearing state.
It does not acquire the authority represented by that state.

## 4. What PR2-PERSIST owns

PR2-PERSIST owns only the runtime-architecture contract for:

- durable representation of already-governed authoritative history;
- reconstruction-basis attribution;
- snapshot role and snapshot-cut qualification;
- snapshot plus subsequent-history reconstruction boundaries;
- recovery-point qualification;
- distinction between semantic replay and reconstruction machinery;
- crash/restart recovery envelopes;
- incomplete or partial persistence handling;
- missing-basis handling;
- corruption detection, quarantine, and bounded recovery posture;
- persistence completeness claims;
- exact versus non-exact reconstruction claims;
- representation provenance sufficient for reconstruction;
- backup and restoration nonauthority;
- replication and copy nonauthority;
- compaction and retention correctness boundaries;
- persisted proposal and noncommitted-state separation;
- command-progress representation handoff to AFQR-02;
- historical version-basis preservation;
- committed-randomness preservation;
- projection rebuild handoff to PR2-EVENT;
- topology-independent persistence semantics;
- local/offline authoritative continuity;
- bounded handoffs to PR2-FID and PR2-BP.

## 5. What PR2-PERSIST must not own

PR2-PERSIST must not define or implement:

- semantic commitment;
- state or write ownership;
- command or attempt identity;
- action legality;
- gameplay resolution;
- logical time or causal law;
- scheduler semantics;
- partition identity or migration semantics;
- message or projection authority;
- branch canonicality;
- timeline identity;
- correction or retcon authority;
- ruleset, package, or override applicability;
- randomness resolution;
- fidelity or aggregation semantics;
- overload or backpressure policy;
- runtime production code;
- production schemas;
- database selection;
- storage-engine selection;
- filesystem layout;
- object-store selection;
- event-store selection;
- write-ahead-log requirements;
- replicated-log requirements;
- consensus requirements;
- quorum requirements;
- cloud-provider requirements;
- R3 execution.

## 6. Reconstruction basis

An implementation claiming authoritative reconstruction must identify a
reconstruction basis sufficient for the claim it makes.

That basis may include separately governed references such as:

- authoritative timeline or continuity basis;
- accepted committed-history basis;
- snapshot basis;
- post-snapshot committed-history basis;
- version and effectivity basis;
- logical or causal context;
- command-progress context;
- correction or supersession context;
- representation provenance.

These are architectural roles, not mandatory production fields.

Exact reconstruction may be claimed only when the accepted basis is sufficient
to reproduce the governed authoritative result.

When the basis is insufficient, the system must not call an approximation,
guess, substituted version, stale replica, or partially recovered state an
exact reconstruction.

## 7. Snapshots are materialized checkpoints

A snapshot is a materialized checkpoint of some declared reconstruction basis.

A snapshot does not by itself:

- create commitment;
- create a branch;
- establish timeline identity;
- establish canonicality;
- establish current applicability;
- establish observer knowledge;
- replace the committed audit.

Where a snapshot participates in authoritative recovery, its cut or basis must
be attributable sufficiently to distinguish what authoritative history it
represents.

## 8. Incomplete snapshots fail closed

A partially written, torn, interrupted, corrupted, or otherwise incomplete
snapshot must not be silently accepted as a complete authoritative checkpoint.

A future implementation may use checksums, transactional writes, generation
markers, atomic replacement, redundancy, validation passes, or another lawful
mechanism.

PR2-PERSIST mandates the required semantic result, not the technology.

## 9. Snapshot plus subsequent history

A lawful recovery strategy may reconstruct from an accepted snapshot basis plus
lawfully attributable committed history after that snapshot basis.

The existence of this pattern does not mandate event sourcing or a transaction
log.

The post-snapshot history remains governed by its semantic owners.

## 10. Persisted proposals remain proposals

A preview, speculative resolution, plan, forecast, reservation-bearing preview,
or other noncommitted proposal does not become authoritative merely because it
is durable.

If authoritative and nonauthoritative representations coexist in the same
physical store, their semantic roles must remain distinguishable.

Storage adjacency is not semantic equivalence.

## 11. Replay reconstruction is not new semantic execution

Reconstruction machinery may consume historical committed records in order to
materialize state.

That operation must not silently:

- create a second semantic commitment;
- rerun gameplay resolution as though it were new;
- produce a different stochastic result;
- refresh historical versions;
- convert an old command into a new command;
- manufacture a correction;
- create a branch.

AFQR-01 remains the owner of semantic replay and recovery meaning.

PR2-PERSIST governs reconstruction machinery nonauthority and its evidence
requirements.

## 12. Recovery does not reroll or refresh history

Replay, restoration, crash recovery, replica recovery, or rebuilding from a
snapshot must not reroll or replace randomness already committed.

Committed dice, cards, bags, oracle draws, random tables, deterministic
uncertainty procedures, PRNG-derived results, external randomized results, and
mixed deterministic/random results retain the accepted R2B-CORE identity and
provenance boundaries.

Recovery or replay must also not silently substitute a currently installed or
newer ruleset, package, override, schema, or procedure basis for the historical
basis that actually governed the original execution.

If a required historical basis is unavailable, the system cannot claim exact
historical reconstruction merely by substituting another basis.

Migration or replacement remains separately governed.

## 13. Crash windows preserve semantic distinctions

A crash before semantic commitment must not cause durable fragments, temporary
files, partially written records, queued messages, cached state, or other
representation debris to be interpreted as a committed transition.

If a transition lawfully committed before a later notification, projection,
replication, or persistence-side operation failed, recovery must not erase that
committed fact merely because downstream work was incomplete.

A crash during reconstruction must not convert an incomplete reconstruction
into a new authoritative history.

The implementation must resume, restart, reject, quarantine, or escalate
according to its lawful recovery envelope rather than guess.

## 14. Command progress remains AFQR-02

Durable command-progress state may be represented or reconstructed.

PR2-PERSIST does not decide:

- whether an interrupted command resumes;
- whether a retry is the same attempt;
- whether a replacement command is required;
- whether a command has reached terminal progress.

Those decisions remain AFQR-02.

## 15. Missing evidence and missing history

Missing durable material does not authorize invented state.

When required committed history, version basis, continuity basis, transition
evidence, or other reconstruction evidence is unavailable, lawful responses
may include:

- declaring exact recovery unavailable;
- bounded partial restoration with explicit qualification;
- quarantine;
- restoration from another attributable copy;
- separately governed migration;
- escalation.

Silently fabricating missing authoritative history is prohibited.

## 16. Corruption is evidence of failure, not permission to improvise

Detected corruption must not be repaired by inventing semantic content.

A corrupted representation may be rejected, quarantined, compared against an
independently attributable copy, reconstructed from another accepted basis, or
escalated.

No specific checksum, redundancy code, RAID level, filesystem, database
feature, or repair algorithm is required here.

Corruption-handling machinery remains infrastructure. It does not gain semantic
authority merely because it detects or repairs physical representation damage.

## 17. Backup and restoration do not decide continuity identity

A backup, export, archive, save bundle, replicated copy, restored snapshot, or
machine image may represent a continuity-bearing history.

Restoration success does not itself determine whether the resulting runtime is:

- the same timeline;
- a restored instance of the same campaign;
- a copy;
- a descendant branch;
- an alternate branch;
- an archival inspection;
- a nonauthoritative test instance.

R2B-CONTINUITY and the applicable identity doctrine retain those distinctions.

Byte equality, storage location, filename, process identity, server identity,
or restoration timestamp cannot substitute for continuity qualification.

## 18. Corrections cannot be smuggled through persistence

Editing a database row, rewriting a snapshot, modifying a save file, changing a
journal entry, restoring an older backup, deleting a record, or replacing a
stored object does not acquire correction authority merely because the storage
mechanism permits it.

Lawful correction, compensation, supersession, or retcon remains governed by
its existing owner.

The applicable historical audit must remain preserved as required by accepted
doctrine.

Recovery is not a covert mechanism for rewriting committed history.

## 19. Replication and copies are representations

Replication may improve availability, durability, locality, or recovery
capacity.

It does not create semantic votes.

More copies do not mean more truth.

Replica majority does not establish canonicality.

The newest replica is not automatically the authoritative winner.

The fastest replica is not automatically the authoritative winner.

A future implementation may use replication, consensus, leader/follower,
multi-primary, quorum, erasure coding, local copies, remote copies, or no
replication at all.

Those are implementation choices subject to this contract rather than semantic
owners.

## 20. Stale replicas cannot silently overwrite accepted history

A stale copy or replica may remain useful evidence.

It must not overwrite or replace a newer accepted authoritative basis merely
because it reconnects, becomes reachable, carries a later wall-clock timestamp,
contains a larger file, or is physically closer to a consumer.

Conflict resolution that affects authoritative meaning remains with the
relevant semantic owners.

Infrastructure must fail closed or escalate when it cannot determine a lawful
reconstruction basis.

## 21. Compaction and retention preserve required semantics

Physical representations may be compacted, reorganized, indexed, archived,
deduplicated, compressed, checkpointed, or otherwise transformed.

Such changes must not silently remove information required to satisfy accepted:

- reconstruction obligations;
- committed-audit obligations;
- historical version attribution;
- continuity and correction attribution;
- randomness provenance;
- transition-receipt obligations.

This rule does not require infinite retention of every physical byte.

It requires preservation of the semantics and evidence that accepted owners say
must remain available.

A compacted representation may replace another physical representation only
when the resulting reconstruction and audit obligations remain demonstrably
satisfied.

## 22. Projection stores remain derivative

A read model, search index, cache, summary, projection database, materialized
view, or model-facing representation does not become an authoritative
reconstruction source merely because it is convenient or appears complete.

A projection may be rebuilt from an accepted persistence basis.

If a projection disagrees with authoritative reconstruction, the projection
does not silently win.

PR2-EVENT retains projection semantics.

## 23. Message failure and persistence failure remain distinct

A committed fact may survive even when its notification or projection update
was lost.

A delivered message may survive even when the consumer's durable state was not
safely reconstructed.

PR2-EVENT governs transport and projection representation.

PR2-PERSIST governs durable reconstruction.

Neither subsystem may infer the other's success merely from its own evidence.

## 24. Physical storage order is not logical order

File order, append position, row identifier, object creation time, database
sequence, write-ahead-log offset, replication sequence, modification time,
backup time, and restore time are physical facts.

They do not automatically become AFQR-04 logical time or causal order.

A storage system may preserve separately governed ordering evidence without
becoming the owner of that evidence.

## 25. Representation migration does not acquire semantic authority

A persistence representation may require schema or format migration.

A representation migration may change encoding without changing domain
semantics.

If a migration changes substantive world meaning, command meaning,
applicability, continuity, correction status, or authoritative outcome, it
requires the applicable semantic authority.

The word migration is not an authority grant.

R2B-CROSS-PHASE remains authoritative for version identity and applicability.

R2B-CONTINUITY remains authoritative for continuity and correction semantics.

## 26. Local and offline operation remain first-class

The persistence contract must remain satisfiable by a local authoritative
runtime without requiring:

- a network service;
- a cloud provider;
- an external AI provider;
- a replicated database;
- an always-online account.

Networked and distributed deployments may add lawful redundancy or operational
capability.

Campaign continuity must not depend on those deployment choices becoming
semantic owners.

## 27. Topology independence is preserved

The same accepted persistence semantics must remain valid whether the runtime
uses:

- one process;
- multiple processes;
- one machine;
- several machines;
- local files;
- embedded storage;
- remote storage;
- replicated storage;
- partitioned execution;
- later deployment topologies.

Changing physical topology must not change authoritative game meaning.

PR2-SCALE remains authoritative for topology independence.

PR2-PART remains authoritative for authority partitioning and migration.

PR2-CONC remains authoritative for deterministic concurrency and scheduling.

## 28. Fidelity remains PR2-FID

PR2-PERSIST may preserve whatever aggregate or detailed representation is
lawfully authoritative at a given boundary.

It does not decide when aggregation is lawful, what information may be omitted,
how detail is reconstituted, or what fidelity tier should apply.

Persistence must not invent detailed state that PR2-FID says was lawfully
represented only in aggregate form.

PR2-FID remains a separately authorized downstream owner.

## 29. Overload and backpressure remain PR2-BP

PR2-PERSIST does not define:

- queue limits;
- storage budgets;
- flush cadence;
- throughput targets;
- write batching;
- eviction priorities;
- overload degradation;
- backpressure policy.

PR2-BP must later ensure that performance pressure cannot silently discard,
delay, mutate, or misclassify authority-bearing persistence obligations.

PR2-BP remains a separately authorized downstream owner.

## 30. No storage architecture is mandated

PR2-PERSIST does not require:

- an event store;
- event sourcing;
- CQRS;
- a relational database;
- a document database;
- a key-value database;
- an object store;
- a graph database;
- a write-ahead log;
- an append-only log;
- journaling;
- snapshots;
- checkpoint files;
- replicated logs;
- consensus;
- quorum reads or writes;
- distributed transactions;
- cloud storage;
- one universal save-file format.

A lawful implementation may use any, several, or none of these patterns where
the accepted persistence contract remains demonstrably satisfied.

## 31. Representative pressure cases

The contract must remain valid under at least the following pressure classes.

Local single-player save/load:
authoritative continuity must remain possible without network dependency.

Crash before commitment:
durable debris must not become committed truth.

Crash after commitment before notification:
the committed fact must remain recoverable.

Crash during snapshot write:
an incomplete snapshot must not become an authoritative checkpoint.

Snapshot plus later committed history:
lawful reconstruction may use both without requiring event sourcing.

Duplicate backup:
copy count does not create authority.

Stale replica returns:
staleness does not create a winner policy.

Missing historical rules version:
no silent version substitution is allowed.

Committed randomized result:
recovery does not reroll.

Retained preview:
persistence does not commit the proposal.

Correction after an earlier outcome:
storage rewriting cannot masquerade as correction authority.

Restored campaign copy:
continuity and branch identity remain separately governed.

Corrupted snapshot:
corruption does not authorize invented state.

Missing history segment:
exact reconstruction cannot be falsely claimed.

Compacted history:
required audit and reconstruction obligations must remain satisfiable.

Projection database survives while its reconstruction basis is lost:
the projection does not silently become authoritative truth.

Offline campaign:
authoritative continuity remains possible locally.

Distributed deployment:
topology does not change game semantics.

## 32. Evidence and escalation

A persistence implementation claiming conformance must produce evidence
sufficient to demonstrate its declared reconstruction and failure guarantees.

Evidence may include deterministic recovery tests, replay comparisons,
snapshot/reconstruction comparisons, corruption tests, partial-write tests,
version-pinning tests, randomness-preservation tests, continuity tests, and
local/offline recovery tests.

PR2-PERSIST does not require one universal evidence format.

If a failure cannot be resolved without redefining semantic ownership,
commitment, command identity, logical time, continuity, version applicability,
correction authority, randomness resolution, fidelity, or performance policy,
the failure must be routed to the applicable existing owner.

Do not invent a new persistence semantic owner merely to keep the failure local.

## 33. R3 remains separate

The exact 34-record R3 conformance target remains separately governed.

PR2-PERSIST does not:

- execute R3;
- authorize R3;
- redefine the R3 selector;
- change the R3 candidate count;
- relabel historical R3 status;
- claim historical R3 completion.

R3 remains `ready_pending_authorization` until separately authorized.

## 34. Completion condition

PR2-PERSIST is complete when the repository can state and test, without
choosing a production storage technology, that:

- durable representation does not acquire semantic ownership;
- snapshots remain materializations rather than commitment or canonicality;
- reconstruction preserves accepted authoritative history;
- replay and recovery do not become semantic re-execution;
- committed randomness is preserved;
- historical version bases do not silently drift;
- proposal persistence does not create authority;
- corruption and missing evidence fail safely rather than invent state;
- backup, restore, replication, and copying do not create branch or canonicality semantics;
- compaction preserves required reconstruction and audit obligations;
- projections remain derivative;
- storage order does not become logical order;
- representation migration does not acquire semantic authority;
- local and offline authoritative continuity remain possible;
- physical topology remains semantically irrelevant;
- AFQR-01, AFQR-02, AFQR-04, and accepted R2B owner boundaries remain intact;
- PR2-EVENT remains the owner of message and projection boundaries;
- PR2-FID and PR2-BP remain separate downstream owners;
- R3 remains separately authorized;
- no runtime implementation, production schema, database, event store,
  write-ahead log, consensus protocol, quorum model, replicated log, cloud
  dependency, or universal persistence technology is mandated.

This contract is architecture governance only.

Implementation remains separately authorized.
