# Tarrow material interaction — approved first combined implementation

## Authority and baseline

Baseline main: `b0cd6a85cf3edd9d8274bb17915b785b43b61c28` (#539/#541).
Owner approval is recorded in issue #542, expanded 2026-10-17 America/Denver;
subsequent owner direction admits workshop preparation, staging/passage obstruction
and removable visual screening in one coherent implementation. This document
implements that bounded contract. No new semantic owner or setting canon.

Existing controls remain: AFQR-18 owns supported spatial placement; RT-010 owns
asset placement, fastening allocation and separation; AFQR-19 qualifies current
opportunity; AFQR-20 qualifies observations; AFQR-01 commits/replays changes.
The implementation adapter composes these responsibilities without acquiring
world authority. RT010 planning text alone is not implementation authorization;
the explicit owner decision in #542 supplies the missing bounded authorization.

## Family inventory and admitted scope

| Family | Implementation in this batch | Remaining boundary |
| --- | --- | --- |
| At / carried / inside | Existing owner reducers, qualification and receipts | No mass, volume, burden or unlimited capacity inference |
| On / lift from | AFQR-18 `supported_by`; explicit surface/object pairs | One support level, no bridging, balance or carried platforms |
| Reversible joining | RT-010 connection record and `reserved_by` fastener allocation | Whole reusable fastener, no implicit length, cutting or consumption |
| Method fidelity | `tie`/`untie` versus `fasten`/`unfasten`, explicit profiles | No universal substitution of cord, peg, adhesive or tool |
| Multiple connections | Independent connection identities; selective removal | No automatic assembly into one new entity |
| Motion constraints | Existing custody/storage/handoff/displacement cannot bypass support or attachment | Disconnect/clear first; group motion requires an explicit later contract |
| Passage obstruction | Conjunction of actual support and connection facts; actor and object corridor checks | No arbitrary object blocks every passage |
| Visual screening | Separate conjunction for a declared sightline | Does not imply movement obstruction, shelter, acoustics or protection |
| Lighting | Existing lit owner reads directly supported placement at the actual location | No propagation or fuel model |
| Water / cleaning / repair / transformation | Preserved in the larger inventory | No simulated effects in this batch |

The immediate placement vocabulary is `located_at`, `carried_by`, `contained_by`,
`supported_by`, `reserved_by`. The last is the placement of a whole fastener
committed to one connection, not endpoint custody or ownership. Connection
endpoints keep their own placement. Composite validation requires exactly one
immediate placement per object; all references resolve; support/containment
cycles and duplicate fastener allocation fail. No parallel mutable location is
stored for supported objects. Effective place is derived from placement.

## Binding and public routes

`myravant-play --locality tarrow-material` selects a separate versioned preview.
The previous `tarrow` and `tarrow-depth` options keep their existing binding and
checkpoint semantics. New layout material is noncanonical development content;
source-backed Tarrow places and people are inherited without new resource,
permission, lore or hidden-location claims. Nine new loose components provide
three coherent groups inside existing locations, not geographic expansion:

- Workshop: Repair Board, Repair Peg, Repair Cord; Workroom Bench.
- Passage: Barrier Board, Barrier Crossbar, Barrier Cord; Yard Work Trestle.
- Screening: Screen Cloth, Screen Cord, Screen Tie; Document Box and Notice Board.

The exterior of the closed Document Box is a surface, not its interior.
All new components also use explicitly admitted existing container transfers.
Profiles, supported pairs, fastening methods and effect dependencies are data;
there are no Tarrow IDs in the material reducer or application adapter.

Commands: `put <object> on <surface>`, `lift <object> from <surface>`,
`tie <left> to <right> using <cord>`, `fasten <left> to <right> using <fastener>`,
`untie <cord>`, `unfasten <fastener>`. Material recognition precedes broad goal
recognizers only for admitted material fixtures. The same classifier/executor
serves standalone and explicit two-step input. Unadmitted methods, modifiers,
third steps and ambiguous/inaccessible objects cannot become simpler successes.

Every participant is freshly qualified for the declared actor and actual local
access/light/closure. No human anatomy, strength, resource costs, permissions or
success chances are inferred. Profiles admit particular feasible methods for
that actor; they do not define a universal body or crafting skill.

## Derived effects and recovery

The barrier requires both components on the trestle and its named tying
connection. It blocks the declared sorting-bay corridor in both directions.
Removing the required connection reopens passage; unrelated state is unchanged.
The screen requires Screen Cloth on Document Box and its Screen Cord connection
to Notice Board. It blocks the threshold's declared sightline while movement
remains available. Screen Tie is independently removable; it is not a substitute
for the required Screen Cord configuration. An unfastened cloth remains at its
actual support; no falling or deformation is invented.

Unfastening releases only the selected connection and recovers that whole
fastener to carried custody. Lift supported endpoints after disconnecting them,
then pack/transport using existing owners. Repeated operations cannot duplicate
components or fasteners. Support/connection constraints are temporary capability
limits: lift them only with admitted group-motion/load/structural contracts and
replay evidence, not as permanent universal prohibitions.

## Commitment and checkpoint lifecycle

Material reducers prepare kernel command/preview/delta/receipt identities and
return immutable candidate representation/connection state. The application
installs the candidate under one chronological transaction boundary. Existing
owner operations keep their own reducers and receipts. Every changed public
operation records its owner receipt, pre/post combined digests, method and exact
arguments; nested dispatch stays one operation. Refusals do not create events.

The opt-in checkpoint identity is `myravant.material-owner-journal`, version 1.
It stores root/binding witnesses, the full chronological owner-operation journal,
its integrity digest and final combined digest. Restore starts at the exact
fixture root, re-executes qualified deterministic owner procedures at each
prestate and compares every recorded receipt/digest and the entire chronology.
No final arrangement snapshot is trusted as a replacement for replay. Initial
material relations cannot be inserted through an old save. Existing checkpoint
formats reject this envelope; material restore rejects legacy envelopes.

Writes reuse the existing atomic/durable checkpoint writer. Direct API calls
with an explicit path persist before returning success; the installed terminal
retains its existing acknowledgement boundary and automatic checkpoint path.
On a write failure the staged in-memory candidate is discarded and future
mutations halt until a validated restart. A failure after filesystem replacement
can have an uncertain on-disk outcome; no success is acknowledged or continued
mutation allowed. Restart validates whatever complete envelope survived.

Journal replay is intentionally bounded local implementation, not a distributed
scheduler or scalable event store claim. Save/replay cost grows with history;
future compaction requires explicit equivalence and migration evidence.

## Acceptance and completion

Tests cover the three complete arrangements, method/target variation,
configuration-only neutral reuse, current light/reach, old-mutation bypass,
closed-interior/exterior distinction, independent connection removal, obstruction
and reopening, screening without movement blocking, partial completion,
write-failure halting, restart, root/profile/receipt/state/chronology forgery,
invalid declarations and legacy compatibility. Four isolated mutations remove
actual relationship, effect, method and replay guarantees with passing controls.
Three installed journeys repeat twice with objective predicates, restart at
stage boundaries and complete trace-digest joins. Engineering-authored evidence
is not independent blind/human acceptance.

Run final-head full local and Linux/Windows CI before certification. Keep
#542/#540/#538/#493/#495 open until their own completion conditions are met.
NPC routines, dialogue and work remain deferred. No merge is implicitly approved.
