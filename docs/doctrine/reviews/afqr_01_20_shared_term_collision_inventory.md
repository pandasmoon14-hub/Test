# AFQR-01–20 shared-term collision inventory

All dispositions are R1A records, not substantive resolutions. Evidence references are physical source records in the authority index and manifest.

| ID | Terms / AFQR usages | Evidence | Class | Likely owner / handoff | Severity / corpus collapse risk | R1A disposition |
|---|---|---|---|---|---|---|
| COLL-01 | state, truth, transition, transaction, event — 01/04/10/17 | SRC-0004, SRC-0035, SRC-0149 | overloaded | AFQR-01 mutation; AFQR-10 truth; typed handoff | critical: donor state models may collapse truth into mutation | requires_R1B_resolution |
| COLL-02 | command, attempt, action, capability, opportunity, target, resolution — 02/03/19 | SRC-0005, SRC-0006, SRC-0231 | nested | 02 lifecycle → 03 representation → 19 resolution | critical: donor action economy could become default | requires_R1B_resolution |
| COLL-03 | identity, owner, authority, agency, responsibility — 01/08/11/15 | SRC-0004, SRC-0011, SRC-0059, SRC-0157 | overloaded | 08 identity; 11 agency; 15 institution; 01 state owner | critical: possession/title could imply control | escalate_to_doctrine |
| COLL-04 | claim, evidence, belief, knowledge, observation — 06/10/20 | SRC-0009, SRC-0035, SRC-0255 | nested | 06 arbitration → 10 epistemic → 20 sensing | critical: hidden truth could leak to observers | requires_R1B_resolution |
| COLL-05 | relation, dependency, obligation, integrity — 05/09/16 | SRC-0008, SRC-0012, SRC-0184 | adjacent | 09 governed lifecycle; 05 bridge; 16 component integrity | high: graph reachability may imply legal effect | requires_R1B_resolution |
| COLL-06 | time, causality, process, transition — 01/04/12/17/18 | SRC-0004, SRC-0007, SRC-0092, SRC-0209, SRC-0231 | overloaded | 04 logical time; 18 topology; domain processes hand off | critical: turn cadence could become universal time | requires_R1B_resolution |
| COLL-07 | signal, communication, interpretation, observation — 10/14/20 | SRC-0035, SRC-0130, SRC-0255 | nested | 20 signal → 14 communication → 10 epistemic | critical: sensing may imply meaning/knowledge | requires_R1B_resolution |
| COLL-08 | jurisdiction, institution, authority, social state — 09/13/15 | SRC-0012, SRC-0110, SRC-0157 | adjacent | 15 institutional law; 13 social state; 09 relations | high: reputation may imply jurisdiction | escalate_to_doctrine |
| COLL-09 | embodiment, integrity, environment, space, topology — 16/17/18 | SRC-0184, SRC-0209, SRC-0231 | adjacent | 18 support/frame → 17 exposure → 16 harm | critical: humanoid anatomy/grid space could default | requires_R1B_resolution |
| COLL-10 | motivation, behavior, agency, responsibility, social state — 11/12/13 | SRC-0059, SRC-0092, SRC-0110 | contradictory-risk | 12 motive proposals; 11 agency; 13 social observations | critical: prediction could become authored action | escalate_to_doctrine |

Additional terms `dependency`, `obligation`, `opportunity`, `target`, `resolution`, `belief`, `knowledge`, `causality`, `communication`, `interpretation`, and `behavior` are deliberately retained within these grouped collision records rather than declared aliases. No obvious alias is accepted until R1B validates type ownership.
