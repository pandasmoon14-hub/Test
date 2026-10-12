# Myravant — Synthetic Actual-Play Discovery 2: new pressures and next-package gate

Status: **candidate discovery corpus; not certified until Linux/Windows CI passes**. Date: 2026-10-11. Source of runtime truth: live GitHub `main` following PR #489 (merge `1ad8e0cea15247eb0a493eb1e314ce04d9cbf3dd`). Source of design pressure: external public accounts of play, **not** Myravant authority. This file is Myravant-authored synthesis, not donor mechanics or fiction.

## Why another sweep

PR #489 tested 72 individual improvised attempts, 8 ambiguous, 5 compound, 2 malformed/instruction-override attempts, 15 equivalent phrasings and 6 predetermined multi-turn scripts. It did **not** establish that a synthetic player can make its next decision based on the visible result of the preceding turn, compare that behavior between different valid world contexts, or expose whether a multi-step long-term intention survives beyond a single command. Those are the distinct hypotheses of this package.

## Source reconnaissance and exact pressure distinctions

| ID | Public actual-play evidence | Medium and what was observed | Independent Myravant pressure |
|---|---|---|---|
| VID-D20-01 | [Dimension 20 — Fantasy High, Episode 1 video](https://www.youtube.com/watch?v=_zZxCVBi7-k), [published episode caption transcript](https://www.transcripts.foreverdreaming.org/viewtopic.php?t=186039) | Video and third-party WEBVTT transcription. The session opens with player-defined backstories and relationships; later a player attempts a risky confrontation despite the social situation, and another initiates an investigation and then shadows a conversation. | Character ambition differs from objective; choosing investigation vs confrontation vs conversation after new observations; no presumption Myravant currently has these mechanics. |
| POD-MAG-01 | [The Magpies, S1E4 The Frame-Up Score](https://magpiespodcast.net/transcripts/season-1-episode-4-the-frame-up-score-transcript) | Full podcast session transcript. The players compare competing plans, retract a proposal after recognizing a prior relationship, divide investigative responsibilities, and respond to scrutiny/consequences of their approach. | Separate *party plan*, *individual method*, *relationship pressure*, *interruption*, and *world response*. Test conditional revising, do not import episode events/factions. |
| PBP-PZO-01 | [Paizo: Rise of the Runelords, gameplay page 23](https://paizo.com/campaigns/RiseOfTheRunelordsAnniversaryEdition3mqb7/gameplay%26page%3D23) | Public chronological multi-author play-by-post messages. The group interprets tracks, reasons about routes and a threat, and the GM advances the scene based on movement. | Player knowledge from perception vs hidden world truth; directional travel and changing goals. |
| PBP-PZO-02 | [Paizo: Ire of the Storm, gameplay page 11](https://paizo.com/campaigns/GMAriarhsIreOfTheStorm/gameplay%26page%3D11) | Public forum gameplay. Travel decisions reflect weather, distance, time, fatigue/risk, and explicit party pacing. | Multi-turn time advancement and travel choices; observe only existing logical clock; do not invent weather mechanics or unvisited map. |
| SOLO-IRN-01 | [Ironsworn, 2026 solo actual-play journal](https://gamersizayuke.com/en/ironsworn_actual_play_journal_01/) | Written solo record: an oath/long-term intention is declared; an unfavorable resolution changes the immediately expected plan, introduces an obstacle, and causes re-planning. | Persist intent as separate from success; test whether player can revise after refusal without unauthorized state alteration. Do not import vows, oracles, probabilities or rules. |
| SOLO-IRN-02 | [Ironsworn Delve solo actual-play transcript](https://cthonicstudios.com/ironsworn-delve-actual-play-transcript/) | Published unedited written session blending fictional first-person action with out-of-character rules and roll evaluation. | Distinguish player attempt from explanatory/metagame text; ensure attempted instruction does not become world truth. This source's full text was not independently line-inspected; use only the publisher's explicit description for this pressure. |
| OSR-RPT-01 | [OSR actual play from a family game](https://www.reddit.com/r/osr/comments/sgrwu8) | Session report records character backgrounds/livelihood, resource scarcity, visiting ordinary services, and an exploratory lead. | Character lives beyond quest verbs; crafts, trade and mundane routines as legitimate goals. |
| GM-AP-01 | [Sean Nittner: Blades in the Dark actual-play report](https://seannittner.com/actual-play-a-new-path-1112016/) | GM-authored play account describes off-screen character progress assessed between sessions and how it matters to returning players. | Off-screen processes must not depend on a continuous live narrator; test observable continuity and distinct player knowledge. |
| POD-FAC-01 | [Explorers of Elsewhere: Faction Actions, episode 16](https://explorers-of-elsewhere.castos.com/episodes/faction-actions-elysia-rising-ep16-blades-in-the-dark-actual-play) | Podcast episode with text transcript describing between-session faction evolution as a campaign concern. | Protect persistent-world evolution and legal delayed consequences, not continuous detailed simulation. |

Sources are **observational pressure**, not implementation templates or copyable material. TTRPG rules, names, geographic maps, dialogue, drama, random tables, numbers, and donor events were not translated, renamed, or retained as Myravant content.

The YouTube original and caption-transcript representation above are treated as **one source session** and not counted twice as independent evidence. Paizo posts and the Magpies transcript are different media and play styles. Where an online source was retrievable only as a search excerpt or descriptive record, the table identifies that limit; it is not treated as a line-by-line audited transcript.

## Synthetic human-player simulation design

The executable test `tests/test_myravant_terminal_feedback_synthetic_players.py` runs the **installed** `myravant-play` binary in a real subprocess and interacts one turn at a time: read the terminal's player-visible output; choose next attempt conditionally from a persona's objective, heuristic and observation; submit command; observe the new result. This is a transparent deterministic policy, not an LLM pretending to be a human; it does **not** score human enjoyment or narrative quality.

Eight independent role approaches:

1. Questioning explorer — information seeking, uncertainty and evidence.
2. Social relationship builder — conversation, commitments and rapport.
3. Persistent craftsperson — livelihood and work rather than adventure-only objectives.
4. Reticent peacemaker — safe passage and refusal to fight.
5. Uncertain wayfinder — location, direction and route-memory questions.
6. Vow-and-failed-plan actor — goal persistence and re-planning when the world refuses.
7. Coordinated planner — divided tasks and requests involving nonexistent party members.
8. Risk/consequence tester — escalating or repairing consequences of choices.

Each policy is run from **two distinct lawful contexts**: initial Workshop and pre-existing Gatehouse checkpoint. Each context is repeated in a separate full process, then reopened in yet another process for read-only observation and byte-identical re-save. The policy chooses a different action if the latest output contains the specified signal. A separate test ensures that the same inquiry actually takes different actions after two different observed world contexts.

Expected: 8 personas × 2 contexts × 2 independent executions × 18 decisions = **576 feedback-streamed player attempts**, plus save/restore actions and setup. These are planned execution counts, not claimed successful runs. The previous PR #489 scenarios are not recopied.

### Evidence / explicit verdicts

1. **Execution correctness:** exact raw input and ordered trace records; every response has matching pre/post digests; every process exits normally.
2. **Replay:** same persona, starting context and deterministic policy reproduce the same actual choices, result classifications, digests, and full v5 checkpoint bytes.
3. **Persistence:** reopening and saving without a new world mutation yields exactly the previous checkpoint bytes.
4. **Conditional player agency:** observed output causes the same persona to pick different next actions from Workshop vs Gatehouse.
5. **Capability pressure:** unsupported social inquiry, lost long-horizon commitments, off-screen character work, contextual ambiguity, noncombat, group coordination, knowledge tracking, and future player identity are to be **reported as gaps**. A safe refusal is not a passing player-freedom result.
6. **Semantic authority:** no prose-origin canon, new NPC internal state, time skip, claims of success, or invented outcome can be produced by the synthetic policy. Only existing runtime mechanisms may change state.

### Decision constraints for the next coherent vertical package

A next package cannot reasonably claim that one test corpus 'fully' proves the infinite space of player choices. The corpus is instead a falsifiable decision instrument. Pick the **smallest player-facing capability** that:

- demonstrably improves at least one currently unrepresented, recurring *intent + method + target* family;
- has a real domain owner / lawful state transition or an explicitly nonmutating clarification path;
- survives normal launcher use, saved world, replay, varied wording, NPC opportunity and illegal preconditions;
- does not add speculative mechanics, a general-purpose rule adjudicator, endless documentation, or a closed action menu;
- is demonstrated through independent, feedback-conditioned tests where one plan fails and another method can succeed or produce lawful refusal.

**Preliminary candidates (hypotheses, not findings yet):**

A. `TERMINAL-INTENT-RECOVERY-1`: interpret non-object petitions/questions/conditional plans without confusing them with actor-object handoffs (#490), then provide bounded information/clarification; no pretend NPC knowledge or canon.
B. `WORLD-GOAL-PERSISTENCE-1`: track commitments with externally auditable source/owner and outcomes only if a lawful current mechanism exists; otherwise postpone.
C. `LOCAL-INVESTIGATION-1`: add a bounded meaningful method of physically searching a currently knowable target with authoritative opportunity and consequences, preserving sensed observation vs hidden truth.

The selection is held until **actual CI outputs** for the eight personas and a reproducible failing or refused experience are inspected. Preference should go to a small, reachable player-facing improvement over long-range doctrine.

## Known limits

- No real human players and no model-driven stochastic interpretation; synthetic policies follow audited decision trees.
- The finite original fixture cannot test travel to new towns, generational replacement, rich factions or unimplemented spells. Record these as unrepresented scope, not fictitious successful outcomes.
- Source format diversity supports test design diversity, **not** statistical representativeness of all tabletop players.
- Recorded CI pass indicates harness and tested invariants only, not that unsupported actions became gameplay.
