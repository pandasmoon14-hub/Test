# Playable development bodies

Low frame and Folding frame are noncanonical development bodies. They use the
same player identity and starting world with separate saves. Select one body
each time you start or resume. On first inspection, posture is unrecorded.

```sh
myravant-play --development-body low-frame --checkpoint low.json
myravant-play --development-body folding-frame --checkpoint folding.json
myravant-play --development-body folding-frame --load folding.json
```

Try `inspect self` and `help travel`. In the Workshop, Low frame can
`crawl south`. Folding frame can use `walk south` to reach the same Yard.
Both can take and light the lantern, walk to Orchard Path, `drag waystone west`,
and return to the Yard. This puts the Waystone in the Yard and obstructs the
licensed east passage. Try to walk east and use the resulting advice:

- Low frame can `crouch then walk east` or `crawl east`.
- Folding frame can `fold then walk east`. While extended, it can instead
  `push waystone north` to clear the passage before walking east.

To compare an independently declared corridor, launch both with
`--development-course gatehouse`. The same setup now obstructs the Yard's
south passage. Use `walk south` to discover the qualified methods. Repeat the
course flag on resume. Keep a separate checkpoint for each body and course.

## Verification

```sh
python -m pip install -r requirements-dev.txt -e .
MYRAVANT_SAVE_DIR=../embodiment-saves \
MYRAVANT_EMBODIMENT_REPORT_DIR=../embodiment-evidence \
python -m pytest -q tests/test_play_development_embodiment.py \
  tests/test_play_posture_movement.py tests/test_play_breadth_traversal_crawl.py \
  tests/test_play_composable_two_step.py tests/test_play_help_topics.py \
  tests/test_myravant_terminal_entrypoint_integration.py
```

The installed tests retain public input, output, trace, exit status, and save
hashes when the report directory is set. They check actual actor and object
locations, recorded posture, time, movement receipts, and acknowledged prefixes.
The two courses test the same owner procedure with different route declarations.

## Runtime binding

AFQR-16 records configuration. AFQR-19 qualifies it and the current movement
opportunity. AFQR-18 retains spatial ownership. AFQR-01 retains the commitment
boundary. Walking, crawling, and posture changes use the existing procedures.

The opt-in v12 checkpoint pins the body and course from the first save, even
with unrecorded posture. It binds the initial world witness, selected actor,
profile and accepted commands, corridor, obstruction and traversal declarations,
and fixture inputs used by adjacent stock actions. The current blocker and
recorded posture remain replayed state. Course or body changes require a fresh
start. Supported legacy saves continue to use their existing formats.

The shared self view now projects the character's name, the selected body,
recorded configuration, local configuration commands, travel options, and
carried items. The attached tabletop profiles also need qualified aquatic
support and exchange, charge and partial travel, fitted contact sensing,
learned cues, tool interfaces, and voluntary service. Those require their own
applicable owner bindings and case decisions before native integration.
