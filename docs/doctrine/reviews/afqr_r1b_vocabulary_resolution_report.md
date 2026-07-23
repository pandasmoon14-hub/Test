# AFQR R1B vocabulary resolution report

**Received HEAD:** `1855cb2460542c0f912a0830276c9cdea90f1b07`
**Gate:** R1B complete; R1 remains incomplete. **Next:** R1C only.

## Scope and method
R1B converts the source-backed R1A collision inventory into a vocabulary, qualification, alias, non-equivalence, and type-owner contract. It does not decide invariants, sequencing, runtime interfaces or data, conversion, canon, sourcebook prose, model behavior, or live play. Decisions follow current doctrine, the R1A authority index, temporary physical evidence, repository fixtures, then donor assumptions. K01 remains the existing lexicon-governance owner; this artifact does not compete with it.

The review inspected the program plan, authority index, dependency matrix, collision inventory, file manifest, working README/manifest and committed extracted evidence, plus the doctrine registry, decisions log, roadmap, conversion/runtime firewall, lawful-outcome doctrine, and K01/K02 registry contracts. Every evidence ID below is manifest-backed.

## All 41 owner assignments and dispositions
| ID | Root term | Disposition | Unqualified use | Owner posture | Collisions |
|---|---|---|---|---|---|
| TERM-001 | state | qualified_canonical_family | qualified_only | shared_qualified_family / R1B shared vocabulary | COLL-01 |
| TERM-002 | truth | qualified_canonical_family | qualified_only | shared_qualified_family / R1B shared vocabulary | COLL-01 |
| TERM-003 | transition | canonical_distinct_type | allowed | afqr / AFQR-01 | COLL-01, COLL-06 |
| TERM-004 | transaction | canonical_distinct_type | allowed | afqr / AFQR-04 | COLL-01 |
| TERM-005 | event | canonical_distinct_type | allowed | afqr / AFQR-04 | COLL-01 |
| TERM-006 | command | canonical_distinct_type | allowed | afqr / AFQR-02 | COLL-02 |
| TERM-007 | attempt | canonical_distinct_type | allowed | afqr / AFQR-02 | COLL-02 |
| TERM-008 | action | canonical_distinct_type | allowed | afqr / AFQR-03 | COLL-02 |
| TERM-009 | capability | canonical_distinct_type | allowed | afqr / AFQR-19 | COLL-02 |
| TERM-010 | opportunity | canonical_distinct_type | allowed | afqr / AFQR-03 | COLL-02 |
| TERM-011 | target | canonical_distinct_type | allowed | afqr / AFQR-19 | COLL-02 |
| TERM-012 | resolution | qualified_canonical_family | qualified_only | shared_qualified_family / R1B shared vocabulary | COLL-02 |
| TERM-013 | identity | canonical_distinct_type | allowed | afqr / AFQR-08 | COLL-03 |
| TERM-014 | owner | escalated_unresolved | reserved | unresolved_escalation / Doctrine Council | COLL-03 |
| TERM-015 | authority | escalated_unresolved | reserved | unresolved_escalation / Doctrine Council | COLL-03, COLL-08 |
| TERM-016 | agency | canonical_distinct_type | allowed | afqr / AFQR-11 | COLL-03, COLL-10 |
| TERM-017 | responsibility | escalated_unresolved | reserved | unresolved_escalation / Doctrine Council | COLL-03, COLL-10 |
| TERM-018 | claim | canonical_distinct_type | allowed | afqr / AFQR-06 | COLL-04 |
| TERM-019 | evidence | canonical_distinct_type | allowed | afqr / AFQR-06 | COLL-04 |
| TERM-020 | belief | canonical_distinct_type | allowed | afqr / AFQR-10 | COLL-04 |
| TERM-021 | knowledge | canonical_distinct_type | allowed | afqr / AFQR-10 | COLL-04 |
| TERM-022 | observation | canonical_distinct_type | allowed | afqr / AFQR-20 | COLL-04, COLL-07 |
| TERM-023 | relation | canonical_distinct_type | allowed | afqr / AFQR-09 | COLL-05 |
| TERM-024 | dependency | canonical_distinct_type | allowed | afqr / AFQR-05 | COLL-05 |
| TERM-025 | obligation | canonical_distinct_type | allowed | afqr / AFQR-09 | COLL-05 |
| TERM-026 | integrity | qualified_canonical_family | qualified_only | shared_qualified_family / R1B shared vocabulary | COLL-05, COLL-09 |
| TERM-027 | time | qualified_canonical_family | qualified_only | shared_qualified_family / R1B shared vocabulary | COLL-06 |
| TERM-028 | causality | canonical_distinct_type | allowed | afqr / AFQR-04 | COLL-06 |
| TERM-029 | process | canonical_distinct_type | allowed | afqr / AFQR-17 | COLL-06 |
| TERM-030 | signal | canonical_distinct_type | allowed | afqr / AFQR-20 | COLL-07 |
| TERM-031 | communication | canonical_distinct_type | allowed | afqr / AFQR-14 | COLL-07 |
| TERM-032 | interpretation | canonical_distinct_type | allowed | afqr / AFQR-14 | COLL-07 |
| TERM-033 | jurisdiction | canonical_distinct_type | allowed | afqr / AFQR-15 | COLL-08 |
| TERM-034 | institution | canonical_distinct_type | allowed | afqr / AFQR-15 | COLL-08 |
| TERM-035 | social state | canonical_distinct_type | allowed | afqr / AFQR-13 | COLL-08, COLL-10 |
| TERM-036 | embodiment | canonical_distinct_type | allowed | afqr / AFQR-16 | COLL-09 |
| TERM-037 | environment | canonical_distinct_type | allowed | afqr / AFQR-17 | COLL-09 |
| TERM-038 | space | canonical_distinct_type | allowed | afqr / AFQR-18 | COLL-09 |
| TERM-039 | topology | canonical_distinct_type | allowed | afqr / AFQR-18 | COLL-09 |
| TERM-040 | motivation | canonical_distinct_type | allowed | afqr / AFQR-12 | COLL-10 |
| TERM-041 | behavior | canonical_distinct_type | allowed | afqr / AFQR-12 | COLL-10 |

## Collision outcomes
| Collision | R1B status | Terms |
|---|---|---|
| COLL-01 | resolved_for_vocabulary | state, truth, transition, transaction, event |
| COLL-02 | resolved_for_vocabulary | command, attempt, action, capability, opportunity, target, resolution |
| COLL-03 | partially_resolved_with_escalation | identity, owner, authority, agency, responsibility |
| COLL-04 | resolved_for_vocabulary | claim, evidence, belief, knowledge, observation |
| COLL-05 | resolved_for_vocabulary | relation, dependency, obligation, integrity |
| COLL-06 | resolved_for_vocabulary | time, causality, process, transition |
| COLL-07 | resolved_for_vocabulary | signal, communication, interpretation, observation |
| COLL-08 | partially_resolved_with_escalation | jurisdiction, institution, authority, social state |
| COLL-09 | resolved_for_vocabulary | embodiment, integrity, environment, space, topology |
| COLL-10 | partially_resolved_with_escalation | motivation, behavior, agency, responsibility, social state |

## Qualification and aliases
Qualified-only roots are: owner, authority, integrity, time, resolution, truth, state. Their source-bounded forms are recorded in the machine artifact. No alias met the strict one-to-one evidence rule, so **accepted aliases: none**. Rejected aliases are every cross-type equality recorded per collision, including truth/state, command/action, observation/knowledge, relation/obligation, process/time, signal/interpretation, jurisdiction/social state, integrity/embodiment, and motivation/agency. The empty accepted-alias graph is direct and acyclic.

## Explicit non-equivalence and donor-family pressure
Every pair within a collision is explicitly non-equivalent. This prevents fantasy rounds, science-fiction signals, cultivation motives, class actions, point-buy capabilities, narrative tags, cyberware embodiment, psionic sensing, investigation evidence, vehicle integrity, companion agency, crafting obligations, bestiary anatomy, tables, supplements, and adventure-path cadence from silently defining universal Astra types.

## Escalations and R1C handoffs
COLL-03, COLL-08, and COLL-10 remain partially resolved with escalation. The ledger preserves unresolved owner/authority/responsibility attribution and the boundaries among jurisdiction, institution, social state, motivation, behavior, agency, and responsibility. R1C receives bounded questions for all 41 terms: establish cross-owner dependencies and invariants without settling mechanics, ordering, propagation, algorithms, or runtime representation.

## Gate posture
R1 remains incomplete because R1C, R1D, and R1E have not completed and the three doctrine escalations remain open. R1C alone is ready. R1D/R1E, R2–R6, and RT-002G remain blocked or unauthorized. Temporary evidence and all archives remain preserved; deletion is not authorized. No production import or authority is created.
