# D04-08 — Integration Checklists and DDR Register

Status: `doctrine-draft / accepted D04 design decisions`  
Layer: D04 integration support  
Owner: doctrine architecture / review  
Purpose: capture accepted D04 decisions, validation checklists, and deferred questions for repo integration

## 1. Accepted DDR register

### D04-DDR-01 — Advancement is broader than levels

Status: accepted by user

Working answer: Astra advancement includes levels, tiers, proof, axes, Development Picks, Awakening, breakthroughs, titles, achievements, route evolution, world-state consequences, capstone, and Ascension Access.

Principle: Advancement is proof-shaped transformation, not only level gain.

### D04-DDR-02 — Level structure and tier bands

Status: accepted by user

Working answer: Tier 0 is levels 1–5, with level 5 as Mortal Threshold. Tier 1 is 5–15, Tier 2 is 16–25, and so on through Tier 10 at 95–100. Level 95 is capstone entry and levels 95–100 are hardest proof.

Principle: Level is cadence; tier is authorization.

### D04-DDR-03 — Awakening proof and route flexibility

Status: accepted by user

Working answer: Characters do not need a preplanned ascendant route. At the threshold, the system may identify lawful Awakening routes from proof but must warn that progression may formalize a contextually appropriate Path/Class/Dao route.

Principle: Awakening emerges from proof; it should not railroad.

### D04-DDR-04 — Dynamic Triadic Awakening

Status: accepted by user

Working answer: Upon gaining Awakening access, each actor should normally see three lawful potential versions of the route. These choices arise from proof clusters, contextual weight, and route/anchor/catalyst logic.

Principle: A life can imply multiple futures.

### D04-DDR-05 — Contextual proof weight

Status: accepted by user

Working answer: Proof significance depends on handling and context. A hunter killing a wolf and a baker killing wolves after family tragedy are not equivalent.

Principle: Proof is what the event means for this actor.

### D04-DDR-06 — Advancement Layer Grant Matrix

Status: accepted by user

Working answer: Different advancement layers grant different kinds of benefits. Levels grant picks, tiers grant authorization and one direct benefit, breakthroughs grant transformation, proof grants eligibility, axes grant focused progress, capstone grants final-proof outcomes.

Principle: No layer should impersonate all advancement.

### D04-DDR-07 — Advancement Safeguard Layer

Status: accepted by user

Working answer: D04 uses Legal Option Presentation, Tier Transition Impact Package, Progressive Axis Disclosure, Multi-route Capstone Proof Ladders, and Development Pick Spend Validation Gate.

Principle: Advancement should be abundant but governed.

### D04-DDR-08 — Typed Development Picks

Status: accepted by user

Working answer: Doctrine uses typed Development Picks. UI may simplify, but backend validation preserves pick type.

Principle: A level creates a lawful opportunity, not arbitrary power.

### D04-DDR-09 — Saveable picks and timing

Status: accepted by user

Working answer: Picks can be saved but remain typed and may become held, focused, stale, pressurized, converted, or source-local expired. Picks are usually spent during advancement, downtime, training, recovery, project, or threshold scenes.

Principle: Stored potential remains tied to proof.

### D04-DDR-10 — Invalid spend routing

Status: accepted by user

Working answer: Invalid spends can become pending proof, route, tier, training, structure, dangerous push, source-local only, project, or rejection.

Principle: Ambition should route into lawful work when possible.

### D04-DDR-11 — Level cadence and pick allocation

Status: accepted by user

Working answer: Ordinary levels grant one typed Development Pick. Tier packages are separate. Level 5 has threshold handling. Held picks may pressurize. Levels 95–100 use Capstone Picks.

Principle: Ordinary levels are cadence; thresholds are not ordinary increments.

### D04-DDR-12 — Tier Authorization Table

Status: accepted by user

Working answer: Tiers authorize Expression Grade, scope, axis depth, payload band, economy complexity, route complexity, external anchor scale, risk, recognition, and world-state scale. Tiers do not grant mastery.

Principle: A tier defines lawful scale.

### D04-DDR-13 — Proof Bundle Calibration

Status: accepted by user

Working answer: Astra uses structured Proof Bundles rather than proof points. Proof is usually referenced, bound, or transformed. Sufficiency bands run Trace through Capstone. Outputs are multi-state.

Principle: Proof is history and structure, not generic currency.

### D04-DDR-14 — Mixed Breakthrough Resolution

Status: accepted by user

Working answer: Safe breakthroughs usually resolve through proof and choice. Risky breakthroughs use D02 rolls, clocks, resistance, contested procedure, dangerous push, or source-local procedure.

Principle: Proof earns threshold; risk determines resolution.

### D04-DDR-15 — Expanded breakthrough response menu

Status: accepted by user

Working answer: Players can proceed, delay, stabilize, redirect, seek anchor, accept scar, externalize, resist, sever, purify, quarantine, bargain, bind, split, fuse, sacrifice, convert, revert, integrate, or push when context allows.

Principle: Breakthrough is a decision space, not a binary button.

### D04-DDR-16 — Lethal breakthrough posture

Status: accepted by user

Working answer: Lethal breakthrough outcomes require lethal-risk posture, catastrophic posture, source-local procedure, dangerous push after warning, or established pressure trail.

Principle: Danger is real but must not be arbitrary.

### D04-DDR-17 — Structured Variable Awakening Package

Status: accepted by user

Working answer: Awakening Packages have required slots but variable contents. Every package includes route identity, vector record, access vector, carrier state, starter method, Awakening Pick, ledgers, visibility change, constraints, Tier 1 authorization, and limits.

Principle: Awakening formalizes a life, not a generic class kit.

### D04-DDR-18 — Filtered Tier Direct Benefit Menu

Status: accepted by user

Working answer: Tier transitions generate one legal Direct Tier Benefit from filtered categories. Tier 0→1 uses Awakening Package. Tier 9→10 uses Capstone Procedure. Pending Tier Benefits are allowed. Benefits are narrow/moderate by default.

Principle: Tier transitions visibly matter without becoming feature tables.

### D04-DDR-19 — Capstone Band Procedure

Status: accepted by user

Working answer: Levels 95–100 are special capstone levels with functions: Threshold Entry, Axis Consolidation, Contradiction/Cost Confrontation, World/Domain/Recognition Proof, Final Integration/Irreversible Choice, Final Capstone Resolution.

Principle: Capstone is final proof, not more levels.

### D04-DDR-20 — Level 100 Ascension Access

Status: accepted by user / reserved for expansion

Working answer: Level 100 can grant Ascension Access, but Ascension is not automatic. An entity may attempt, delay, suppress, refuse, externalize, redirect, or transform Ascension.

Principle: Level 100 opens a profound choice, not mandatory exile.

### D04-DDR-21 — D02-to-D04 mapping

Status: accepted by user

Working answer: D02 lanes map into breakthrough outcomes. Natural 20 is best lawful result. Natural 1 is worst lawful failure within posture. Margin -4 to -7 is flat failure with consequence.

Principle: Randomness can shape dangerous transformation but cannot replace proof, route, tier, or lawful action vectors.

## 2. Integration checklist

Before merging D04 into the repo, check:

- [ ] Every file has status, layer, owner, scope, and dependencies.
- [ ] No file claims canon status.
- [ ] No file defines final runtime implementation.
- [ ] No file imports donor terms as Astra law.
- [ ] D04 references D02 for resolution rather than redefining d20.
- [ ] D04 references D03 for Power Economy and Expression math.
- [ ] D04 references D05 for skills/professions/research/training.
- [ ] D04 references D06 for Path/Class/Dao/domain mechanics.
- [ ] D04 references D07 for harm/death/recovery details.
- [ ] D04 references D08 for actor-state transformations.
- [ ] D04 references D09 for items/relics/platforms/external anchors.
- [ ] D04 references D10 for factions/world-state/territory/recognition.
- [ ] D04 distinguishes proof from XP.
- [ ] D04 distinguishes level from tier.
- [ ] D04 distinguishes tier authorization from mastery.
- [ ] D04 distinguishes Development Pick from Direct Tier Benefit.
- [ ] D04 distinguishes Awakening from normal tier transition.
- [ ] D04 distinguishes Capstone from Ascension.
- [ ] D04 has lawful attempt vector protection.
- [ ] D04 has lethal-risk posture protection.
- [ ] D04 has source-local handling.

## 3. Suggested minimum tests

### 3.1 Mundane Tier 0 test

Input: level 4 blacksmith with 100 sword proof and no Power Economy.

Expected: craft/profession axis visible; possible title seed; no automatic supernatural Expression; route seed possible; Development Pick legal options filtered.

### 3.2 Awakening test

Input: level 5 fisherman with planetary largest-fish desire and proof.

Expected: Awakening warning; Dynamic Triadic Awakening options; Catalyst/Route/Anchor identified; Structured Variable Awakening Package after selection.

### 3.3 Multiple proof cluster test

Input: actor is both fisher and baker with strong proof in each.

Expected: proof clusters distributed; triadic options do not collapse into one route; fusion or parallel route option possible if lawful.

### 3.4 Invalid Expression test

Input: low-level mundane actor declares instant-kill spoken word with no sound/compulsion/relic/entity/action vector.

Expected: no breakthrough/Expression roll; route to project/research/route-seeking or impossible action; if actor forces self-harm, dangerous action only with warning.

### 3.5 Development Pick validation test

Input: player tries to spend Skill Pick on unrelated high-grade Expression.

Expected: blocked or pending route/proof/tier/training; possible project if coherent; no direct authorization.

### 3.6 Tier authorization test

Input: Tier 5 actor requests world-scale effect.

Expected: tier scope check identifies ceiling issue; if unsupported, pending tier/proof/capstone/world-state route; natural 20 cannot bypass.

### 3.7 Breakthrough failure test

Input: dangerous push with lethal-risk warning accepted, then natural 1.

Expected: worst lawful failure within catastrophic posture; D07 handoff for lethal/crippling/unmaking; committed state delta.

### 3.8 Safe breakthrough test

Input: stable proof-supported profession breakthrough with no risk.

Expected: no random roll required; formal or choice-gated resolution; payload and proof binding recorded.

### 3.9 Capstone noncombat test

Input: level 95 healer/crafter with capstone-grade proof.

Expected: Capstone Band Procedure available; Capstone Proof Lanes include profession/service/world consequence; not forced into combat route.

### 3.10 Ascension Access test

Input: level 100 actor completes Final Capstone Resolution.

Expected: Ascension Access may become eligible; actor may attempt, delay, suppress, refuse, externalize, redirect, or remain; no mandatory departure.

## 4. Deferred questions

D04 deliberately defers final D02 outcome names, exact numeric Expression Grade ceilings, exact scope/range/duration/target-count values, exact Power Economy math, exact carrier burden formula, exact skill rank names, exact Path/Class/Dao features, exact breakthrough harm tables, exact corruption/purification mechanics, exact capstone failure tables, exact Ascension Access procedure, post-Ascension play loop, and final sourcebook prose.

## 5. Recommended next design stage

After D04, proceed to D05: Skills, Competencies, Professions, Knowledge, Training, Research, and Synthesis.

D05 is needed because D04 now relies on skills/professions/training/research for proof generation, Development Pick validation, axis progress, assessment relevance, project conversion, Awakening support, and capstone proof.
