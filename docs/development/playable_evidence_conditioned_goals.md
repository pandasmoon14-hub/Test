# Investigate before acting in the installed client

At a documented passage, a player can check access, ask a reachable witness
what they saw, or make crossing conditional on a particular source. At a workshop
assembly, the same instruction can check whether fitting is still needed and
ask a worker to take the next available step. The inquiry and the consequential
action have separate receipts. A worker can agree without taking custody or
performing any work.

## Yard Tool Station

Install with `python -m pip install -e .`, then launch the fixed structures profile.

```sh
myravant-play --locality tarrow-structures --checkpoint access.json --trace access.jsonl
myravant-play --locality tarrow-structures --load access.json --trace access-reload.jsonl
```

Enter one command per line.

```text
go south
go west
take work panel
put work panel on yard work trestle
take barrier crossbar
put barrier crossbar on yard work trestle
Could I check whether the north passage is clear?
Ask Tali whether the north passage is open.
take work cord
tie work panel to barrier crossbar with work cord
```

The preview takes no time and admits no observation. Tali's report is based on
her observation at step 6 while the north passage was open. Tying the panel to
the crossbar closes it by step 8. There are two configured barriers on this edge.
Seeing one closed establishes obstruction. An open finding requires one scoped
inspection that covers both.

```text
> If I see that it's open, take me through.
You saw that the north passage was closed at step 8.
You saw that the north passage was closed at step 8. Tali Ren reported that the north passage was open at step 6. The condition was false. No consequent was attempted.
> If Tali says it was open, take me through.
Tali Ren reported that the north passage was open at step 6. Proceeding under the named account condition.
Tali Ren reported that the north passage was open at step 6. The assembled barrier obstructs that passage. Remove a necessary fastening or component to reopen it. Crossing is still pending.
```

`Take me through if the evidence says it is open.` shows the two accounts and
leaves the evidence standard to the player. `Check it yourself instead.` is a
new personal check. `Whose account was that?` repeats the session's last
qualified finding and what remains. Exit and load. The scoped report and the
closed barrier survive. The dialogue expires, so restate either authorization.
After `untie work cord`, try:

```text
> Find out whether the passage is usable. Ask someone who saw it if you need to. If you can verify it's open, take me through. Otherwise stop there.
You saw that the north passage was open at step 9.
You move to the Yard Sorting Bay.
```

For a reachable person who lacks the matching observation, start with
`--locality tarrow-activities --activity-case reference`. Enter `go south`,
`go west`, `go north`, `go south`, `go west`, `go east`, `go west`, `go west`.
`Ask Oren whether the north passage at Yard Tool Station is open.` returns
unknown. `Check from Yard Tool Station.` then takes two ordinary walking
steps along the known route and inspects. The observation commits at arrival
without crossing the passage. You can instead wait, take another route, or
stop. Reachable witnesses can answer only with observations they actually
made and can report through the local inquiry owner.

## Shared Workroom Bench

```sh
myravant-play --locality tarrow-surface-water --surface-case shared-workbench --checkpoint bench.json --trace bench.jsonl
myravant-play --locality tarrow-surface-water --surface-case shared-workbench --load bench.json --trace bench-reload.jsonl
```

Set up the actual parts at the bench.

```text
go south
go west
go west
go west
take repair board
put repair board on workroom bench
take repair peg
put repair peg on workroom bench
```

```text
> Check whether the workshop assembly is already fitted. If it still needs work, ask Oren to finish the next available step. Leave the wooden strip where it is.
You saw that the workshop assembly was unfinished at step 8.
Oren Kesh reports active: assembly, workshop assembly; 0 own committed step(s). Acceptance reserves no materials.
```

An immediate duplicate request reaches Oren's participation owner, which
refuses because he is busy with selected work. `Cancel that` closes the
player's dialogue. Exit and reload. To finish it yourself, enter
`take repair cord` and `tie repair board to repair peg with repair cord`.
`ask oren kesh about work` then shows an externally satisfied agreement
with zero contributions by Oren. `Ask Tali whether the workshop assembly is
fitted.` delivers her dated firsthand observation. The cord stays reserved
in the join and the wooden strip stays at the bench. If instead you use
`wait 2 steps` from the initial acceptance, Oren takes the cord and fits
the parts through the same owners. His completed agreement attributes two
actual contributions to him.

Requesting work on an assembly that already meets the condition stops
after inspection. A request that protects the repair peg cannot guarantee
its placement through the selected procedure and creates no agreement.
Stopping a dialogue leaves any standing agreement to its own owner.

## Implementation and verification scope

The terminal uses the constrained goal executor from [#584](https://github.com/pandasmoon14-hub/Test/pull/584)
at `f186d9e8d1684f24a3eb216ab3f9cdd2ed3209dd`. Both activities share the
language, session, evidence selection, inspection and step dispatch. Passage
binding uses known routes and exact material-effect predicates. Work binding
uses a visible declared assembly, its fixed support and the existing
participation method. The work adapter additionally checks whether a protected
part is outside the selected procedure and still at the bench. The fixtures
configure the place, people, materials and procedure. Neither activity names
a fixture or person in the shared dispatcher.

The supported conditions are material obstruction of a documented route and
the fitted state of a declared fixed-support assembly. Historical testimony
can satisfy an explicitly named report condition. Ordinary crossing still
qualifies at the movement owner. A personal condition requires a current
qualified observation, and a generic evidence condition stops on conflicting
accounts. Unknown remains a separate result. This package uses existing
chronology, inspection, work, material, evidence and checkpoint owners.

To reproduce the paired conversations from two installed checkouts, put the
candidate virtual environment first on `PATH` and pass the installed #584
launcher. The report disables network socket operations in both processes,
checks the guard, and includes traces, restored custody, agreement records,
source event IDs and checkpoint digests.

```sh
python scripts/report_myravant_conditioned_goals.py \
  --baseline-launcher /path/to/584-venv/bin/myravant-play --output paired.json
python -m pytest -q tests/test_play_conditioned_goals.py
python scripts/report_myravant_conditioned_goal_mutations.py --output mutations.json
```

The comparison expectations were frozen before runtime edits. The five
acceptance cases and five unfamiliar phrasings were selected by the
implementation author. The independent 500-case AC-04 benchmark remains open.
