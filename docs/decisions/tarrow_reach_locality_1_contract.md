# Tarrow Reach locality binding — first executable batch

Status: implemented candidate for issue #538; owner approved the setting basis
and requested runtime development on 2026-10-17. This is an engineering binding,
not a ratification of additional world canon, new universal mechanics, automatic
merge, or human-play readiness. Headquarters is separate.

## Playable result

`myravant-play --locality tarrow --checkpoint tarrow.json` starts an arriving
wayfarer in Wayhouse Common. Nine connected areas can be visited through sixteen
explicit directed edges. Twelve areas are declared in total: Wayhouse Household,
Service Stores and East Bank Track have no admitted incoming public route.
Seven named inhabitants have distinct identities, initial locations and public
roles; their placements are development configuration. Their routines, personal
knowledge, conversations, consent, jobs and economic activity are not simulated
by this batch. `community` is a public role guide, not remote sensing.

The player can observe local people/objects, move, carry/drop qualified objects,
operate the service lamp, open/close the coffer, store/retrieve declared pairs,
wait, compose exactly two admitted steps, and save/restart. The folio starts in
player custody; the wedge and slate start inside the coffer. The Pin Blank is
hidden in a rack with no admitted search/open interaction. The Floodmark Post,
Sorting Rack and East Gate are fixed and cannot be acquired by ordinary pickup.
Gate repair, east crossing, controlled/private entry, literacy, harvesting and
resource quantities have no fabricated implementation.

## Source packet and refinements

- [NCD-PROD-001 locality core](https://docs.google.com/document/d/1cqeRYeCYlLB1_rxici4SjwQ8bv3yhHeHmqVjoROkcHA/edit),
  NCD-CONT-367..381: four core places, eight objects and the gate situation.
- [Native Content Registry](https://docs.google.com/spreadsheets/d/1j0KUSfqG1H-CI8FtInEA4IOeWSS4aYnX8nitrHepsXI/edit),
  NCD-CONT-544..566: Reach, approaches, channel, habitat and environmental context.
- [Set G](https://docs.google.com/document/d/1uhk_yjTs8nF4WncdvNFWH_OGWFPMXHTBnxuC2VL1hvQ/edit),
  NCD-CONT-620..629: seven people and distinct knowledge/undertakings. Its later
  Pin Blank location refines the initial Gate A coffer placement. Neither public
  object description nor refusal reveals the hidden location or gate diagnosis.
- [Current social-world reconstruction](https://docs.google.com/document/d/10Zgu5MIp2f0J4ozyu2QEGveM-3EL7iiEN6zgLZ7IJLU/edit):
  NCD-DEC-269..284, NCD-VAL-037. Superseded Lethren drafts are not consumed.

The source's canonical place/object/actor identities remain content facts.
Additional room layout, actor positions, storage pairs and bank/guest/workshop
access are explicitly noncanonical development bindings. No new household
membership, role authority, property title or permission is inferred. The runtime
fixture reports `canon=False` and `canon_sources_with_development_bindings` to
avoid promoting this entire executable realization to canon. The player seed
still has no imposed species, anatomy, skill, power or posture profile.

## Spatial and operational model

| Space | Boundary | Binding |
| --- | --- | --- |
| Wayhouse Common | public interior | source core |
| Service Yard | shared exterior | source core |
| Underbank Walk | service passage; dark without light | source core |
| Weir Deck | exposed service exterior | source core |
| Wayhouse Household | private; no entry route | development realization |
| Guest Shelter | guest interior | development realization |
| Workshop Workroom | shared work interior | development realization |
| Service Stores | controlled; no entry route | development realization |
| North Track Approach | public approach | source route, development extent |
| East Bank Track | beyond blocked crossing | source route, no crossing license |
| Lower Channel Bank | bank vantage; no water traversal | source feature, development access |
| Reed Margin | habitat edge; no harvest contract | source habitat, development access |

Public `activities` identifies reception, repair/tool stewardship, stock issue,
record/message handling and environmental inspection, with participants and
explicit missing execution contracts. These are authoring dependencies, not
schedules or progress grants. Waiting advances the existing WORLD-1 clock while
no qualified autonomous process is present. It never borrows the development
Groundskeeper's routine for Tarrow's people.

## Ownership and compatibility

AFQR-18/19 qualify route and opportunity; AFQR-20 owns sensing evidence; RT-010
owns custody, open/lit/storage operations; WORLD-1 owns logical time; existing
checkpoint/replay owners persist their results. This adds no semantic owner.

Fixture qualifications now identify a light source, declared open/lit targets,
fixed objects, storage pairs and admitted specialist routes. Historical defaults
are unchanged. Tarrow admits no stock specialist families: exact old Chest and
Groundskeeper requests cannot call absent entities, and an unadmitted specialist
in a two-step input prevents execution of its first step. Other parsed core
requests still receive current-state qualification and truthful partial outcomes.

The original default launcher and checkpoints remain available. A Tarrow campaign
has a separate identity containing a canonical digest of its declared binding;
changing its layout, initial placements or content cannot silently reinterpret an
existing save. This is not a migration of old development campaigns into canon.

No checkpoint format changes. WORLD-1 restoration optionally accepts an explicit
initial-representation witness. Untouched initial containment is admitted only
when both the independently supplied witness and current canonical digest match
the expected initial digest. Legacy callers without that witness still reject
transition-free containment. Modified placement still needs attributable history.
Existing transitions retain their normal chain/receipt validation.

## Evidence and remaining delivery

`tests/test_play_tarrow_locality.py` covers installed entry/restart, every admitted
edge, initial containment, forged unreceipted placement, incompatible binding,
fixed-object qualifications, illumination/containment, hidden information,
unsupported specialist composition, durable partial completion and save failure.
The output guard catches literal backslash-newline artifacts in generated
presentation; it does not claim to reject legitimate raw/quoted player input.

`report_myravant_tarrow.py` runs three installed journeys twice with full trace,
restart, digest-chain and end-state predicates. `report_myravant_tarrow_mutations.py`
uses isolated copies and passing controls to detect fixed-pickup bypass,
containment without root witness, and unadmitted specialist partial execution.
Evidence is implementation-authored, not independent blind or human acceptance.

Next coherent batches: scoped public NPC interaction/knowledge and consent;
actual stores/work dependencies; qualified environmental/travel changes; then
procedural population using the same persistent actor contracts. New mechanics
or unresolved canon bindings require their own explicit disposition. Do not call
this first locality binding a completed inhabited simulation.
