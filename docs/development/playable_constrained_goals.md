# Constrained goals in the installed client

A player can ask what they can do, name an outcome, or authorize steps toward
it. Advice is read-only. The installed client offers methods grounded in the
player's local view, their own exchange receipts, and their known routes.
When methods change whose cooperation, time, tools or water will be involved,
the client presents the choice. It rechecks each selected step before invoking
the existing owner procedure.

This draft builds on [#583](https://github.com/pandasmoon14-hub/Test/pull/583)
at `ff1bdd45714f5bd925996aef67fbdd320fb89533`. Its published CI, portability
and causal pilot passed at that exact head. Its previous local full suite ran
at `ca657c95561f282ef5e9e456af59f8b58b28b772`, before the guide correction.
The same earlier 19 cases and all 11 inherited misses are rerunnable with
`report_myravant_experienced_references.py`.

## Return a real item

Install with `python -m pip install -e .`. The stock development locality
is fixed. The Yard routine changes the Groundskeeper's availability with
logical time.

```sh
myravant-play --checkpoint lantern.json --trace lantern-out.jsonl
myravant-play --load lantern.json --trace lantern-back.jsonl
```

Enter `take lantern`, `go south`, `wait`,
`give lantern to groundskeeper`, and `ask groundskeeper for lantern`.
At this point asking “Can I get this back to the person who gave it to me?”
offers the local handoff. “Take it back to them” performs it. To exercise
interruption, enter the following from the same setup, before returning it:
`wait` three more times, then `go north`.

```text
> Can I get this back to the person who gave it to me?
You still have Brass Lantern. Groundskeeper is absent from your local view.
Yard is the recorded exchange site and a place to start looking. You can check
Yard along your known route. Finding the recipient is uncertain.

> Take it back to them
Stopped at Workshop. You still have Brass Lantern. Groundskeeper is absent
from your local view. Yard is the recorded exchange site and a place to start
looking. You can check Yard along your known route. Finding the recipient is uncertain.

> Start at the last exchange.
You move to the Yard.
Stopped at Yard. You still have Brass Lantern. Groundskeeper is absent from
your local view. Yard is the recorded exchange site and a place to start looking.
You have reached that site.

> Why did we stop?
1 plan step(s) committed. You still have Brass Lantern. Groundskeeper is
absent from your local view. Yard is the recorded exchange site and a place
to start looking. You have reached that site.
```

Exit and load the same save. `Do it` gives an expired-goal response.
Enter `wait`, then `Return the lantern to its giver`. The Groundskeeper
is now locally visible and the handoff commits. Repeating the goal reports
the completed exchange. The save bytes and owner receipts match the concise
control `go south`, `wait`, `give lantern to groundskeeper` after the
shared setup. Time moved from four to five due to the explicit `wait`.

### Recover it by hand or ask the holder

For direct recovery, start a new development save and enter `take lantern`,
`go south`, `open chest`, and `store lantern in chest`. “Can I recover
the lantern without asking anyone?” gives the publicly visible retrieval
method. “Use your judgment” performs the existing `retrieve lantern from chest`
owner action.

For a voluntary transfer, use a fresh save and enter `take lantern`,
`go south`, `wait`, and `give lantern to groundskeeper`. The same recovery
question now explains why the prohibition rules out asking the local holder.
`Do it` keeps the prohibition. After `Clear the limits`, `Ask the holder`
uses the same request and receipt as `ask groundskeeper for lantern`.
The advice identifies a request opportunity with an uncertain response.
A closed container contributes no current placement to either method.

The earlier giver comes from the player's directional receipt. The physical
handoff establishes custody and place. An explicit loan needs its own
RT-010 agreement with AFQR-11 consent. Permission to search belongings,
ownership and return obligations likewise require their own evidence.

## Clean a panel while preserving water

The timed Tarrow locality is independently configured with compatible tools,
finite water and residue capacity, and the existing material and clock owners.

```sh
myravant-play --locality tarrow-time --checkpoint panel.json --trace panel-out.jsonl
myravant-play --locality tarrow-time --load panel.json --trace panel-back.jsonl
```

For both tools, enter `go south`, `go west`, `take cleaning brush`,
`go west`, `go west` and `take cleaning cloth`. The bench's panel
contains three removable residue units.

- **Dry cloth**. Ask “Could I clean the practice panel without drawing more
  water?” The dry cloth is excluded. “Do that, but stop if you need the
  basin” runs two dry brush strokes, leaves all 12 units in the bucket,
  and removes three residue units. The equivalent concise action is
  `scrub practice panel with cleaning brush` twice.
- **Wet cloth**. Add `soak cleaning cloth from wash bucket` before asking.
  The player chooses between wiping twice to remove two units and scrubbing
  twice to remove all three. “Do that” leaves the choice open. “Use the
  cloth” performs both strokes and halts with one unit remaining when
  the cloth fills. “Why did we stop?” reports the capacity issue.
  “Use the brush instead” resumes from that one remaining unit. If you exit
  after wiping, load and restate “Get the practice panel clean without
  drawing more water.” The fresh attempt performs one scrub from the
  retained world state. The matched control is two wipes and one scrub.
- **Basin reserve**. At a fresh bench carry only the cloth. Take the
  Wash Bucket, `pour 1 unit from wash bucket into rinse basin`, then
  `go east`, `drop wash bucket`, and `go west`. The basin is now the only
  reachable stocked source. “Could I get the practice panel clean and leave
  at least 1 unit in the basin?” identifies the reserve. “Go ahead, but
  stop if you need the basin” still refuses the draw. After clearing limits
  and explicitly attempting the unrestricted goal, soaking draws exactly
  one unit, the cloth wipes twice, and the partial result stops at its
  capacity. The owner's operation reports the actual resource transfer.

Limits apply to the chosen player's plan, with requalification between owner
steps. Existing independent world activity still follows its clock.
`Clear the limits` requests a new preview and `Cancel that` ends the
goal. Spoken selections and limits expire on exit. Reload announces the
need to restate both. Committed work, placements, exchanges and movement
remain under the checkpoint and replay owners.

## What the cleaning integration reused

Both families use the session's read-only preview, method and consequence
options, player selection, bounded step execution, progress, interruption
and cancellation. A method describes its next existing owner action. The
family declares evidence qualifiers and a completion predicate. Cleaning
added local tool and surface qualification, work capacity, one-unit soaking
and stroke counts. It added the phrase “get … clean” and the no-draw, vessel
reserve and stop terms. The custody family uses transfer evidence, visible
holders and open contents. It has its own prohibition on asking. The same
interface can carry an admitted vehicle or extraordinary method where
existing owners expose its opportunities and completion. The package
adds no vehicle or extraordinary mechanics.

## Evidence

```sh
MYRAVANT_GOAL_REPORT_DIR=../goal-journeys python -m pytest -q tests/test_play_constrained_goals.py
python scripts/report_myravant_constrained_goals.py --baseline-launcher /path/to/583/bin/myravant-play --output ../goal-comparison.json
python scripts/report_myravant_constrained_goal_mutations.py --output ../goal-mutations.json
```

The comparison blocks outbound socket connections inside both installed
clients. It saves transcripts, canonical owner receipts, logical time and
the resulting custody or resource compartments. The new cases were written
by the implementation author after reading the baseline and before editing
the candidate. The independent AC-04 500-case benchmark remains open.
