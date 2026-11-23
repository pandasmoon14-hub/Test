# Generated worksites and revised agreements

At the uninhabited Cloth Shed, the cloth can dry before you use it. A basin lets
you wet it again, or you can scrub with a brush. On returning, you can see how
much residue is left and where work was done.

At Gauge Workshop, the resident cleans the rear panel under their own standing
agreement. You can work on the other panel, ask the resident to help, or keep
walking. The workshop's supplies and exposure determine which method you can
use. A report describes what the speaker saw at the time. Changing a work
agreement starts a new agreement with its own scope and history.

## Launch and return

Install with `python -m pip install -r requirements-ci.txt -e .`. Use a fresh
checkpoint for each new session. Repeat the case, seed and scale on load.

```sh
myravant-play --locality generated-worksite --generated-case drying --generated-seed 0 --generated-scale 0 --checkpoint cloth-0.json
myravant-play --locality generated-worksite --generated-case drying --generated-seed 0 --generated-scale 0 --load cloth-0.json
myravant-play --locality generated-worksite --generated-case drying --generated-seed 1 --generated-scale 0 --checkpoint cloth-1.json
myravant-play --locality generated-worksite --generated-case coordination --generated-seed 0 --generated-scale 0 --checkpoint gauge-0.json
myravant-play --locality generated-worksite --generated-case coordination --generated-seed 0 --generated-scale 0 --load gauge-0.json
myravant-play --locality generated-worksite --generated-case coordination --generated-seed 1 --generated-scale 0 --checkpoint gauge-1.json
myravant-play --locality generated-worksite --generated-case sealed-annex --generated-seed 0 --generated-scale 1 --checkpoint packing.json
myravant-play --locality generated-worksite --generated-case sealed-annex --generated-seed 0 --generated-scale 1 --load packing.json
```

The startup names the gate and shows its exits. Enter `go east`, `look`, and
`inspect worksite` for locally visible tools and the command forms. Observations
and discussion have no world interval. Actions such as movement, pickup and
work do. The workshop steps below use `wait` to advance intervals while the
player makes no physical intervention.

## Cloth Shed, uninhabited

Enter `go east`, `inspect worksite`, `take cloth`, `inspect cloth`, and
`wipe panel a using cloth` on both seeds. With the same inputs, these lines
come from the installed client:

| Seed | Cloth after pickup | First wipe | After one scrub and returning |
| --- | --- | --- | --- |
| 0 | `Condition: dry.` and `A drying trace is visible.` | `wiping requires retained water` | 1 unit of residue on Panel A |
| 1 | `Water: 1/2 unit(s).` and `Condition: wet.` | `Wipe: Panel A to Cloth.` | 0 units of residue on Panel A |

Use `take brush`, `scrub panel a using brush`, `go west`, `wait`,
`go east`, and `inspect panel a` for the return. Another seed-0 route after
the refused wipe is `soak cloth from basin` and `wipe panel a using cloth`.
The basin has 2 of its initial 3 water units left and the panel has 2 of its
initial 3 residue units. On seed 1, inserting `wait` between taking the cloth
and the first wipe leaves just enough water to begin. The next interval dries
it and the client reports that the action was interrupted. The panel still has
3 residue units.

## Gauge Workshop, inhabited

- **Purpose during the player's absence.** From Marker Court enter `wait`
  three times before `go east`. `inspect panel b` shows 0 residue and brush
  patterns. `ask jun about panel b activity` returns his historical scrub.
  The resident's three committed steps were tool pickup and two scrubs. The
  real Brush remains with him. On entering immediately in the seed-1 session,
  Sol is still doing this work and can decline a conflicting request.
- **Agree, observe, report, and revise.** Take Plate and put it on Bench, take
  Peg and put it on Bench, then `take cord` and `tie plate to peg using cord`.
  `go north` is blocked. `inspect passage work` shows the release options.
  Enter `ask jun to release joining frame`, `ask jun to pause work`,
  `untie cord`, `drop cord`, and `ask jun about plate assembly`. Jun reports
  that he witnessed the pieces separate. Exit and load here if desired.
  Take Cord, re-tie the pieces, and `compare reports about plate assembly`.
  The attributed statement says separate and the player's later observation
  says joined. `ask jun to resume work`, `wait`, and `ask jun about work`
  show that the agreed fastening is gone. Cancel that work and
  `ask jun to release joining frame` again. Exit and load after acceptance.
  `wait` now opens the north passage. `ask jun about plate activity` returns
  his own untie, and he holds the Cord.
- **The resource changes, too.** With Panel A still dirty, enter
  `ask jun to clean panel a using cloth by wiping` and `take cloth`. The
  pickup blocks the worker's planned preparation, with no contribution.
  `ask jun about cloth moisture` returns his last witnessed wet condition.
  Cancel the original work. Go north to Open Walk, where questions to Jun
  fail through the local communication route. Wait twice and inspect the
  cloth. Return south and ask about moisture before dropping the cloth.
  Jun still reports wet. Drop it where he can see it and ask again. He now
  reports dry and declines a new wipe using that dry cloth. Enter
  `ask jun about ways to clean panel a`. He suggests
  `ask Jun to clean Panel A using Detail Scrubber by scrubbing`.
  A suggestion makes no agreement. Use the suggested command to agree, then
  exit and load. Wait three times to let him acquire the tool and scrub.
  `ask jun about panel a activity` returns his own scrub. Leave west, wait,
  return east and inspect Panel A. It has 0 residue and retains brush patterns.
- **Try the same switch with different stock.** Seed 1 places the Detail
  Scrubber in Supply Recess, two exits west of Gauge Workshop. After the
  cloth dries there is no feasible local method for Sol and he refuses a
  request using the inaccessible tool. Bring the scrubber back and drop it
  in the workshop. Sol can now propose the same scrub. You can carry out the
  method yourself after canceling the work. If Sol agrees to release a
  fastening and you untie it first, his agreement ends externally satisfied
  with 0 own steps. The Cord remains in your own custody.

## Packing Annex transfer

Use the third launch family at scale 1, then `go east`, `go east`, and
`look`. The closed Dry Box hides its contents and blocks retrieval. Open it
and `retrieve annex rag 1 from dry box`. Inspection shows 2 retained water
units. Drop the rag, leave west, wait three turns, and return east. The rag
is on the same floor with a drying trace. The existing open/close and custody
rules control access. The exposure owner pauses drying inside the closed box
and resolves exposure on the normal clock when the rag is accessible.

A proposed continuation is to test a lidded but permeable enclosure: keep the
box shut to a hand and let moisture cross a declared boundary. The first missing
rule is a container-bound exposure rate independent of the open/closed access
state. AFQR-17 owns the exposure decision with RT-010 admitting the relevant
container property. Current constructed rooms, enclosure access, retention and
subsequent drying are already executable.

## Changing the recipe

`LocalityRecipe` supplies the version-bound case, seed (0–65535), finite
construction budget, and number of adjoining rooms (0–3). The neutral
constructor declares starting custody, physical routes, tool/surface pairs,
water and residue stocks, exposure rates, and resident qualifications. Change
these inputs for another working place. Keep each method matched to an existing
owner and each exit unique at its source. Seed parity selects a shed exposure
rate of 1/2 versus 1/4 per interval, or moves the secondary workshop scrubber
between the workshop and supply recess. The resident's public name varies with
the coordination seed. Standing work has the same purpose in both variants.

Admitted adjoining detail ranges from four rooms to seven across the profiles.
Packing Annex requires at least one added room. Additional rooms preserve
existing entity and placement IDs and adjoining routes for the same seed and
case. Each scale has its own checkpoint binding. Explore the admitted rooms
and inspect their current contents within that campaign. A restart replays the
journal for the same seed and scale. Live expansion of a saved campaign, world
geometry beyond the declared graph, planet/plane generation, and physical or
credit transfer of partial refits still require owner decisions. The workshop
demonstrates a fresh agreement on a separable cleaning method. The original
passage-work case also demonstrates a separable action during a partial refit.
At stage one of the interrupted player refit, ask Tali to clean Sorting Board
using Cleaning Brush by scrubbing and wait three times. She reports her scrub.
The Crossbar stays on the trestle and the original refitter still holds their
one committed stage when that separate work ends. [Passage work](playable_passage_work.md)

WORLD-1 advances the shared clock. AFQR-17 owns continuous exposure, RT-010 owns
material relationships and water state, and the current actor owners qualify
observation, communication and voluntary work. AFQR-01 commits and replays the
owners' receipts.

## Reproduce the evidence

```sh
MYRAVANT_SITUATED_REPORT_DIR=../situated-evidence python -m pytest -q tests/test_play_situated_worksite.py
python scripts/report_myravant_generated_locality.py --output ../generated-locality.json
python scripts/report_myravant_generated_locality_mutations.py --output ../generated-mutations.json
```

The installed evidence includes exact inputs, visible output, trace receipts and
before/after checkpoint hashes. The restart comparison inserts the same first
look explicitly at each seam of the uninterrupted run. It checks byte-identical
saves, including chronology, accepted scopes, actor contributions and custody.
The fault case injects a checkpoint-write failure before acknowledgement, then
replays the accepted prefix and advances once. This is engineering-authored play
and verification.
