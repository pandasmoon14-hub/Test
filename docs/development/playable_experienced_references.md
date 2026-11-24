# Experienced references in the installed client

This branch depends on draft [#582](https://github.com/pandasmoon14-hub/Test/pull/582)
at `f939fd4809a4fd0a5f3566222e16f9ca02ddf038`. The client interprets
descriptions against what the player can observe, their own retained evidence
and exchanges, and routes they have actually traversed. Time, replay and physical
effects are still owned by the existing applications. The input client needs
no network, model or provider.

## Return to the workshop

Install the existing entry point with `python -m pip install -e .`. The
noncanonical activity arrangement is fixed and uses no seed. The same locality
and case flags select the checkpoint's declared profile on reload.

```sh
myravant-play --locality tarrow-activities --activity-case reference --checkpoint brush.json --trace brush-out.jsonl
myravant-play --locality tarrow-activities --activity-case reference --load brush.json --trace brush-back.jsonl
```

In the first session enter `go south`, `go west`, `go west`, `go west`,
and `look`. The bench lists the Cleaning Brush and both Oren Kesh and Tali Ren.
Enter `ask Oren Kesh to undertake bench upkeep`, `go east`, `go east`,
`wait 5 steps`, `wait 5 steps`, and `exit`. Oren uses the brush, assembles
the workshop repair pieces, and puts the brush down at the shelf. The player is
at the Yard Tool Station for the latter work. The activity case declares the
starting placement and the existing cleaning, assembly and drop methods.

After reloading, the player can try:

```text
> Where is the brush now?
You saw Cleaning Brush at Workroom Bench at step 5 (11 steps ago). You don't know its current location.

> Go get it
You don't know where to get that object from here.

> Take me back to where I saw the brush
You move to the Workshop Workroom.
You move to the Workroom Bench.
Signs here point to Workshop Workroom, Workroom Shelf.

> Ask Tali whether she heard about the brush
No retained reported evidence for that topic.

> Ask Tali whether she saw the brush
Tali Ren reports historical witnessed evidence: at Workroom Bench. This is a report, not a fresh inspection. Evidence from step 5.
```

On the bench a fresh `look` omits the brush. Asking where it is now adds Tali's
attributed report to the player's own earlier sighting, with an age for each.
The player can follow the sign to `Workroom Shelf`, `look`, and try
`go get it` again. This time the visible brush can be picked up. Repeating the
installed departure and reload in separate processes yields byte-identical
final saves, including Oren's contributions, the report provenance and custody.

## Return the lantern

This separate fixed development locality begins in Workshop. The exchange and
the subsequent return take place in the Yard.

```sh
myravant-play --checkpoint lantern.json --trace lantern-out.jsonl
myravant-play --load lantern.json --trace lantern-back.jsonl
```

Enter `take lantern`, `go south`, `wait`, `give lantern to groundskeeper`,
`ask groundskeeper for lantern`, `go north`, and `exit`. The wait gives
the Groundskeeper time to arrive. After reloading:

```text
> Take this back to the person who lent it to me
The exchange records who gave or received an item. You have no evidence here of a loan.

> Take this back to the person who gave it to me
Your last matching exchange with Groundskeeper was at Yard. You can't reach that person here or tell where they are now.

> Take me back to where they gave it to me
You move to the Yard.

> Take this back to the person who gave it to me
You hand the Brass Lantern to the Groundskeeper.
```

The existing handoff owner verifies the recipient's local availability and
actual custody. A transfer establishes its participants, direction and place.
The owner for any further agreement to lend or borrow is AFQR-10
(custody, possession and ownership). Those terms need an admitted loan term.

## Clarify a later instruction

```sh
myravant-play --locality generated-worksite --generated-case access --generated-seed 0 --generated-scale 1 --checkpoint worksite.json --trace worksite.jsonl
myravant-play --locality generated-worksite --generated-case access --generated-seed 0 --generated-scale 1 --load worksite.json --trace worksite-reloaded.jsonl
```

From Workshop, `go west` to Entrance, then use the description below.
The panels are identifiable when the player reaches Workshop. The client has
no fixture relation that singles out the panel by the entrance.

```text
> Head back to the workroom and examine the panel by the entrance
Instruction 1/2: You move to the Workshop.
Instruction 2/2: I can't verify that position from here. Which panel do you mean? Panel A, Panel B.

> the rear panel, please
Panel B
```

`Look at the other one` now inspects Panel A. A complete new instruction
can supersede a pending question. `Cancel that` clears it. The answer on
its own establishes no attempt after a reload.

## Evidence and authority

- Actor apps admit direct placements with an observation receipt. An observed
  support or container can establish a room only through placements admitted
  on the same receipt. Attributed placement reports have an origin step and
  are selected separately from sightings. Current observations are qualified
  through the public location view. Session sightings fill in where the older
  profiles have no durable per-observer observation owner.
- A player's movement receipts recover specific directed route legs. Other
  routes require current signs or directions observed in the session.
  Current access and physical constraints are checked on each leg.
- A handoff reference uses only receipts in which the player was a participant.
  "The tool I used earlier" uses committed player work and its attributable
  performance receipt in actor-bearing profiles. "The tool I received" uses
  the direction of the exchange and the current method's qualified tools.
- Existing checkpoints and NPC evidence admission remain in use. A broader
  durable sensory memory in profiles with no corresponding observation receipt
  would need AFQR-20 observation and AFQR-01 persistence decisions. The game
  can still use those profiles' current views and player movement and handoff
  receipts.

The installed evaluation compares full traces and canonical control effects.
The code retains all eleven misses from #582's two engineering sets. Codex,
the implementation author, wrote the new cases after seeing the first
implementation on 2026-11-24. The independent 500-case AC-04 benchmark is a
separate acceptance activity.

```sh
MYRAVANT_REFERENCE_REPORT_DIR=../reference-journeys python -m pytest -q tests/test_play_experienced_references.py
python scripts/report_myravant_experienced_references.py --baseline-launcher /path/to/582/bin/myravant-play --output ../reference-comparison.json
python scripts/report_myravant_experienced_reference_mutations.py --output ../reference-mutations.json
```
