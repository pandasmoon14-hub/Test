# Practical passage work

Two noncanonical worksites put the same barrier, whole parts, and material
procedures on different corridors. A worker can agree to release the exact
tied fastening that currently obstructs a passage. The release runs on a
later world interval and puts the actual cord in that worker's custody.

```sh
myravant-play --locality tarrow-transformation --transformation-case sorting-bay-work --checkpoint sorting.json
myravant-play --locality tarrow-transformation --transformation-case workshop-passage-work --checkpoint workshop.json
myravant-play --locality tarrow-transformation --transformation-case sorting-bay-work --load sorting.json
```

From the common room, enter `go south`, `go west`, and `inspect passage work`.
The inspection offers locally available preparation and currently visible
fastenings. Keep separate saves and repeat the case on load.

- **Sorting Bay.** Take Barrier Crossbar, put it on Yard Work Trestle, and
  take Alignment Tool. Enter
  `start refitting barrier crossbar using alignment tool` and
  `work transformation` twice. Put Barrier Board on the trestle, take
  Barrier Cord, then `start assembling passage barrier` and `work`.
  The assembly stops `go north`. Use `untie barrier cord` yourself, or
  `ask tali ren to release passage barrier` and `wait`. Once the cord is
  released, `go north` works again.
- **Workshop passage.** The spare is available at the station. Stage the
  original on the trestle and
  `ask oren kesh to replace barrier crossbar with barrier spare`.
  Accepting work does not move the spare. While you place the board and
  get the cord, Oren can acquire the spare, lift the original, and support
  the replacement over successive intervals. Then
  `tie barrier board to barrier spare using barrier cord`. The west
  passage is now obstructed. `ask oren kesh to release restored barrier`
  and `wait` reopen it. Tali declines this work in this case.

`ask tali ren about work` gives participation status through the existing
communication route. `ask tali ren about barrier board activity` can return
her retained performed evidence. `ask tali ren for barrier cord` uses the
existing voluntary task-material return. An NPC who did the release holds
the recovered cord until a qualified transfer.

An accepted request makes no physical change. Pause, resume, or cancel through
the usual `ask <actor> to ... work` commands. If someone opens the passage first,
the worker can observe it already open and earns no untie receipt. Retying
creates a distinct fastening. An old agreement can report the change, and a
new agreement can release the new tie. A failed acknowledgement preserves the
last durably saved prefix.

Each performer keeps their own accepted task. Transferring a partial refit
between performers needs a ruling about the prepared part, the remaining work,
and attribution of the earlier contribution.

## Verification

```sh
python -m pip install -r requirements-ci.txt -e .
MYRAVANT_SAVE_DIR=../passage-saves \
MYRAVANT_PASSAGE_WORK_REPORT_DIR=../passage-evidence \
python -m pytest -q tests/test_play_passage_work.py tests/test_play_transformation_1.py
python scripts/report_myravant_transformation.py --output ../transformation-journeys.json
python scripts/report_myravant_transformation_mutations.py --output ../transformation-mutations.json
```

The new cases use the existing transformation, material, actor, and time owners.
Their own journal binding pins the corridor, declared arrangements, helper
scope, and starting resources. The accepted fastening ID is replayed from the
actual relationship at request time. The scheduler resolves the voluntary work
on the existing clock, and RT-010 owns the release and resulting custody.
Performer history, observation, and reports retain their existing distinctions.
GitHub's Linux core job exports raw installed inputs, traces, and save hashes.
