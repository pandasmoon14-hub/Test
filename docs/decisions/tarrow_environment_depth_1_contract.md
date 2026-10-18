# Tarrow environmental depth — milestone inventory and first batch

Owner direction, 2026-10-17: maximize environmental depth per coherent PR before
NPC routines, dialogue and work processes. This implements the ready first batch
of the seven-layer milestone, stacked on unmerged PR #539. Neither PR is approved
to merge. Canon sources and development bindings retain #539's distinctions.

## Family inventory and disposition

| Layer | Existing execution / ready integration | Deferred distinction and actual dependency |
| --- | --- | --- |
| Spatial structure | AFQR-18 place identities, explicit corridors, AFQR-19 opportunity: 16 local positions inside 9 publicly traversable areas; named one-edge approach | Continuous coordinates, dimensions, climbing, posture-specific reach and moving platforms need explicit profiles/contracts; no universal geometry inferred |
| Structures and components | 17 fixed observable fittings across thresholds, work, maintenance, deck, guest, track and bank positions; existing pickup qualification | These are observable entity targets, not authoritative part-of/attachment/support relationships. Detaching, dismantling, structural load and changing components need owner-routed state/change contracts |
| Material contents | 6 additional containers and 5 loose material objects; 7 containers in total; explicitly qualified storage pairs and initial contents; shared open/close/custody | Mass, volume, fit calculation, cleaning, cutting, material transformation and arbitrary use are not licensed by descriptions |
| Environmental conditions | Existing sufficient/insufficient visual profile at three dark positions; actual lamp placement/custody/containment; local vs directional sensing | Wetness, wind, sound propagation, smell, friction, temperature and hydrology need explicit inputs/effects before runtime simulation |
| Physical relationships | located_at, carried_by, contained_by; 8 method-specific displacement licenses and one explicit passage obstruction; closing qualifies container movement | on/supporting, attached_to, covering, hanging, tension and load are not represented by substituting containment or prose; define semantic contracts before adding these |
| Observable history | Local visible wear, patches, outlines, streaks and rub marks are authored appearance facts, qualified through sensing | Appearance is not a committed historical event, diagnosis, culprit, memory or automatic knowledge record; dating/inference/tracking require their own contracts |
| Persistent alteration | Movement, pickup/drop, open/close, storage, push/slide, blockage/reopening, time, separate-step durability and replay | Structural deformation, destruction, repair progress, evolving environmental conditions and causal history need supported owner transitions |

Ready mechanisms are reused together rather than split by verb. Deferred cells
are not implemented by a generalized new relation/physics substrate. Ownership:
AFQR-18 location/topology; AFQR-19 current opportunity; AFQR-20 sensing; RT-010
asset changes; AFQR-01 commitment; WORLD-1 time; existing checkpoint owners replay.
See `afqr_world_action_sensing.md` and executable domain procedures. Planning
specifications are not proof that future owner code already exists.

## Locality-wide inventory

| Existing area | Proposed development realization in this batch | Contrast / remaining boundary |
| --- | --- | --- |
| Wayhouse Common | threshold, notice recess, low shelf; frame/board/shelf, document box and loose cloth | public interior; no automatic reading or record creation |
| Service Yard | tool station, sorting bay, underbank threshold; trestle, rack, stone edge, basket and sorting tray | shared outdoor circulation; explicit clearance rather than every object blocking routes |
| Underbank Walk | floodmark and abutment positions; post, joint and visible wall streak | dark local positions; nearby light does not automatically illuminate the next position |
| Weir Deck | control position and inspection edge; gate exterior, housing, guide face and rail | exposed infrastructure; no interior diagnosis, operation or water traversal |
| Wayhouse Household | existing private boundary retained | no new access license or invented household interior |
| Guest Shelter | shared belongings bay; bench and empty box | furnishing does not grant ownership, lodging reservation or custody of others' possessions |
| Workshop Workroom | bench and shelf positions; fixed bench, parts tray, loose strip and tool outlines | open tray cannot use the declared closed-tray displacement route; no invented repair recipe |
| Service Stores | controlled boundary retained | resource quantities, reservations and authority are not inferred |
| North Track Approach | stopping edge; message rest and delivery box | storing goods is not courier dispatch or an obligation |
| East Bank Track | blocked crossing retained | no new bypass/teleport route created to expand coverage |
| Lower Channel Bank | separate observation edge and visible water mark | no depth, swimming, slip or soil-strength law |
| Reed Margin | observation fringe, rooted growth and snagged drift | no automatically local Floodlace yield, harvest permission or clearing effect |

All new positions, objects, appearances and geometric licenses are noncanonical
engineering realizations. The source-backed Tarrow identities and core facts are
preserved, including Set G's hidden Pin Blank location. No private mechanics or
content from other conversations is consumed. This is not a canon amendment.

## Player meaning and first PR scope

The preview is `myravant-play --locality tarrow-depth`. `tarrow` v1 and the original
development locality remain unchanged. The preview contains 28 place identities
(12 areas plus 16 local positions), 38 object identities, 48 directed movement
corridors and explicit directional sensing licenses. Three private/blocked areas
still have no public incoming route. No player receives a new anatomical profile.

`approach <exact adjacent position>` resolves one declared destination and calls
the same movement executor as a cardinal move. It performs no pathfinding,
teleport, action bundle or target-visibility grant. Parent-area labels are static
presentation grouping, not a new spatial relation or authority. Current position
is still the existing AFQR-18 place state. Being in the same named building does
not grant interaction with everything inside it. Duplicate movement directions,
unknown endpoints and inconsistent presentation grouping fail declaration checks.

Generic goal-method placement reuses actual scenario object/place references.
Old Waystone clearance syntax is not admitted where no Waystone exists. Stock
Chest, Groundskeeper, NPC-work and duty handlers remain excluded. Two-step input
preserves preflight, current-state requalification, stopping and durable partial
completion; source input and separate receipts remain in the existing trace.

One concrete scenario: a closed delivery basket at the yard obstructs this
explicit underbank approach. Push or slide it to the tool station to clear the
passage; move it back to re-obstruct. Opening it exposes contents locally but
prevents either declared relocation method until closed. Cargo keeps its actual
identity and containment throughout. Another scenario uses a parts tray at the
workbench, with a different route/method. The rule is declared opportunity, not
an inferred universal mass, force, container or corridor law.

Existing checkpoints are not migrated. The preview has a distinct version and a
binding digest covering layout, people, objects, initial states, contents,
qualifications, sightlines and presentation grouping. V1 campaign/provenance
identity is regression-checked. A self-consistent incompatible preview cannot
reinterpret a v1 save. No checkpoint format change.

## Replay repair exposed by plural containers

The older INT-1 replay comparison compared serialized state tuples in incidental
order even though the state family's canonical serialization/digests are sorted
by object identity. A plural initial-state vector without open/close history
therefore failed restoration. Compare the complete canonical serialized state
vectors instead; do the corresponding direct/nested INT-2 comparisons too.
Receipt replay, stored digests, identity and actual state values remain checked.
Tests must accept permutations, with and without transitions, while rejecting
real unreceipted state differences. No dummy event or exemption is introduced.

## Combined acceptance and completion limits

- Every local position is reachable only through declared routes; visits and
  changed target opportunity restore correctly. Private/blocked areas remain so.
- Every fitting is observable at a qualified position and refused by ordinary
  pickup. Source refinement and hidden cargo remain private until actual access.
- Both basket methods clear and re-block the route; tray condition and cargo
  persist; a stale observation grants no permanent reach.
- Declared sightlines permit observation without granting manipulation; observer
  light does not illuminate an adjacent dark position by assumption.
- Fresh neutral position/object/container declarations use the same execution
  and replay paths without shared code edits or fixture-ID branches.
- Full player routes, explicit refusals, partial completion, write failure before
  acknowledgement, installed repeat journeys and isolated mutations are required.
- Original corpora remain unchanged; report measured outcomes separately.
  Full final-head Linux/Windows CI is required before merge readiness.

Implementation-authored checks are not independent blind or human acceptance.
This first PR strengthens existing layers and their composition; it does not
complete the environmental milestone. Next batches should resolve support,
attachment/covering and structural-change contracts, then qualified environmental
processes/evidence. NPC systems remain behind this environmental priority.
