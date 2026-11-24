# Player intentions in the installed terminal

A player can follow locally readable signs or a known route, refer to a visible
thing by description, ask a witness a question, and select a tool in a follow-up
reply. Each step uses the same movement, observation, custody, evidence and work
procedures as concise commands. A blocked step stops the rest of the instruction.

## Play the generated worksite

From this branch, install and start a new checkpoint.

```sh
python -m pip install -r requirements-ci.txt -e .
myravant-play --locality generated-worksite --generated-case access --generated-seed 0 --generated-scale 1 --checkpoint worksite.json --trace worksite.jsonl
myravant-play --locality generated-worksite --generated-case access --generated-seed 0 --generated-scale 1 --load worksite.json --trace worksite-return.jsonl
```

The client starts in the Workshop. Follow the signs and encounter the closed
passage.

```text
> Go to Work Annex 1.
You move to the Work Annex 1.

> Go back to Covered Yard and check the cloth.
Instruction 1/2: You move to the Workshop.
Instruction 1/2: Travel stopped at Workshop. The assembled barrier obstructs that passage.
The rest of that instruction was not attempted.
```

Exit and load the checkpoint here. Input clarifications expire when the client
closes. The movement back to the Workshop survives.

```text
> I'll untie the cord.
You untie and recover Cord.

> Go to Covered Yard.
You move to the Covered Yard.

> Go back to Workshop and ask Jun if the front panel was dirty when he saw it.
Instruction 1/2: You move to the Workshop.
Instruction 2/2: Jun reports historical witnessed evidence: present. This is a report, not a fresh inspection.

> I'd like to grab the brush.
You pick up the Brush.

> Clean the front panel.
Scrub: Panel A to Brush.

> Scrub it with what I used earlier.
Scrub: Panel A to Brush.

> I want to go into Covered Yard.
You move to the Covered Yard.

> Return to the room where I saw the panel.
You move to the Workshop.

> Look closely at the front panel.
Removable residue: 0 unit(s).
Physical traces: Brush patterns are visible.
```

“Let me check the panel” asks which panel. “No, the rear one” identifies the
rear panel. “Actually, leave it” discards a proposed action. “Run back” keeps the
running method and reports its current unavailability. A question about keeping
the last of the water preserves the constraint and spends no water.

## Transfer to Tarrow

```sh
myravant-play --locality tarrow-actors --checkpoint tarrow.json --trace tarrow.jsonl
myravant-play --locality tarrow-actors --load tarrow.json --trace tarrow-return.jsonl
```

```text
> I'll head to the Service Yard.
You move to the Service Yard.

> Go to the Yard Tool Station.
You move to the Yard Tool Station.

> Let me check the sorting board.
Removable residue: 2 unit(s).
Physical traces: Brush patterns are visible.

> Did Tali see it dirty?
Tali Ren reports historical witnessed evidence: present. This is a report, not a fresh inspection.

> wait
Time passes.

> I'd like to ask Tali for the cleaning brush.
Give completed.

> Which way back?
Known way to Service Yard: Service Yard.

> I want to return to the common room.
You move to the Service Yard.
You move to the Wayhouse Common.
```

Two plain-language variants and concise commands produce byte-identical saves
in this Tarrow journey. The installed test compares movement and communication
receipts, time, custody and resulting state. Another journey brings the brush
to the workroom bench, asks to clean the practice panel, and answers “With the
brush” when the client offers wiping and scrubbing.

## Extend a family

`myravant_player_intentions.py` parses roles into an `Intent` with a speech act,
action, participants, method, instrument and any explicit constraint. The
terminal retains the original input and proposed order in its ordinary evidence
trace. A developer adding a family can define its accepted roles, add a pure
recognizer, resolve each role against the appropriate public candidates and
delegate to an existing application procedure. Supply tests for a lawful
operation, ambiguity, changed opportunity and an explicit modifier. New
mechanics still need their current owners.

Use a fixture's `public_input_aliases` to add terminology for an admitted
presentation. It becomes eligible only while that presentation is in the
player's applicable context. Use `signposted_routes` to expose directions already
declared by the locality. Directional sightings and actual traversal also
establish routes during the current session. Encountered landmarks are recorded
at the place they were seen. Planning uses the player's known graph and stops
at a choice between equally short routes. Each leg rechecks its physical route
and charges the existing movement and time costs. These notes and pending
clarifications expire on reload. The ordinary owner checkpoint records accepted
actions and stays compatible with concise commands.

The implementation is offline. The repository's model-boundary evaluation and
proposal contracts contain no installed gameplay provider that can supply
qualified player interpretations. The terminal uses no provider calls.

## Evidence and limits

```sh
MYRAVANT_INTENTION_REPORT_DIR=../intention-journeys python -m pytest -q tests/test_play_player_intentions.py
python scripts/report_myravant_player_intentions.py --output ../player-intentions.json
python scripts/report_myravant_player_intention_mutations.py --output ../player-intention-mutations.json
python scripts/report_myravant_action_coverage.py --output ../legacy-action-coverage.json
```

The assessment accepts `--baseline-launcher` and `--baseline-sha` together for a
second installed launcher pinned to main. It runs both against the same expected
routes and receipts. Its authored Set A covers 18 cases and Set B covers 10.
Set A uses exact owner effects, required clarification, or a named inquiry
response. Set B measures preservation without harmful execution or tested
disclosure. The raw records retain misses. The separate historical 39-case
suite is a compatibility comparison and was authored for an earlier release.
The new assessment is engineering-authored, frozen for scoring without retuning
the runtime, and has no independent or human acceptance. The broader AC-04 gate
requires 500 independently unseen representable attempts, at least 95% correctly
routed, at most 3% false unsupported, at most 10% unnecessary clarification, and
zero fabricated mechanics or unauthorized state invention.

The parser resolves named and observed landmarks, visible aliases, selected
conditions, short replies, and a travel-first ordered instruction. Free-form
planning beyond those roles, arbitrary multi-clause sentences, unqualified
proximity claims and new traversal or cleaning mechanisms still need further
work. This package uses the existing generated worksite on main. The
[generated coordination draft](https://github.com/pandasmoon14-hub/Test/pull/581)
supplied examples. Its causal pilot was cancelled, and its independent gates
remain in that draft.
