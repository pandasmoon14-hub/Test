# D17-09 — Integration Checklists, DDR Register, and Acceptance Criteria

> Doctrine status: D17 doctrine pack draft for Astra Ascension.
> Schema status: record shapes are **not final schema**; they are doctrine-facing / conversion-facing controls. Runtime Gate B or later schema doctrine may replace or formalize them.
> Research note: the supplied economy/acquisition/inventory/reward/requisition analysis is used as non-final research pressure and guardrail material, not canon terminology by default.


## Integration checklist
D17 is integrated only when all are true:
```text
Value is classified by form, access channel, scarcity, legality, ownership/custody, and burden.
Acquisition and exchange do not assume price equals access.
Reward, loot, salvage, bounty, faction grants, requisition grants, Project outputs, crafting outputs, and source-local value-entry do not imply automatic ownership or power.
Custody and ownership are separate.
Inventory is represented as burden, access, storage, custody, visibility, maintenance, decay, and transport pressure.
No universal slot, weight, bulk, encumbrance, spatial storage, cargo, or post-scarcity storage law is created.
Requisition, upkeep, maintenance, consumption, taxes, dues, debt, fuel, ammo, decay, confiscation, cultivation consumption, and source-local sinks are supported without becoming universal.
Anti-poverty-trap review is required for severe sink/upkeep/requisition pressure.
Donor economy systems are mapped by function, not label.
Bounded source-local value systems are preserved where appropriate.
Unsupported value constructs are quarantined.
Repeated or high-impact missing doctrine is escalated.
Owner-file handoffs are explicit.
```

## Owner-file handoff checklist
```text
D03 — resource pools, charges, overdraw, recharge, resource-side instability.
D04 — advancement gates, breakthroughs, progression proof, advancement-adjacent costs.
D05 — methods used to acquire, appraise, negotiate, craft, salvage, conceal, or transport.
D06 — Techniques, domains, power expression, ritual/power consumption.
D07 — harm, contamination, exposure, corruption, injury, condition consequences.
D08 — actor body/substrate, companion burden, bound actor implications.
D09 — object, item, material, relic, implant, vehicle, ship, platform, container, cargo, module, tool state.
D10 — world-state, law records, market facts, scarcity, hidden truth, public belief, rumor, regional economy.
D11 — presentation, hidden-state boundaries, misinformation, player-facing summary.
D12 — scene timing, quick access timing, action cadence, immediate use attempts.
D13 — Projects for crafting, salvage, repair, maintenance, acquisition, storage, transport, resource gathering.
D14 — travel, discovery, site-entry, route access, transport pressure.
D15 — claims, obligations, enforcement, faction stores, licenses, requisition authority, law operations, domain control.
D16 — encounter reward pressure, loot triggers, salvage triggers, opposition-related value.
D18 — campaign economy, settlement/domain income, seasonal scarcity, inflation/collapse, state aging, long-horizon reward pacing.
```

## Anti-drift rules
```text
Do not treat money as the default form of value.
Do not treat price as access.
Do not treat possession as ownership.
Do not treat rarity as final value.
Do not treat loot as lawful property by default.
Do not treat salvage as free wealth.
Do not treat reward as automatic power.
Do not treat requisition as free supply.
Do not treat post-scarcity as no-scarcity.
Do not treat inventory as default slots, weight, bulk, or encumbrance.
Do not treat containers, magic bags, spatial rings, cargo holds, banks, or pattern libraries as burden-erasure devices unless an owner file or source-local rule supports it.
Do not import donor shop lists, price tables, wealth-by-level, treasure parcels, loot tables, reward schedules, contribution charts, or currency systems as Astra law.
Do not let D17 become D09 item-state, D10 market-state/world-state, D13 Project procedure, D15 institutional enforcement, D16 reward-trigger construction, or D18 campaign economy doctrine.
Do not let source-local economy systems become Astra law through repetition alone.
```

## Research-derived guardrail register
```text
inflation_risk — value faucets exceed sink/burden review.
poverty_trap_risk — sinks/upkeep create unrecoverable resource collapse.
hoarding_risk — inventory/storage permits lossless accumulation.
reward_collapse_risk — rewards lose value because economy or sinks are miscalibrated.
inventory_paralysis_risk — burden creates excessive bookkeeping or lost-loot anxiety.
grind_wall_risk — scarcity blocks progression without alternate access.
uncontrolled_salvage_risk — salvage becomes free or unbounded wealth.
post_scarcity_erasure_risk — fabrication or storage erases scarcity and access pressure.
donor_value_law_leakage_risk — donor price/currency/slot/reward/sink logic becomes Astra law.
```

## DDR register
### D17-DDR-001 — Value is broader than money
Decision: D17 treats value as currency, barter, material, service, labor, favor, debt, license, permit, access, claim, storage, transport, requisition authority, cultivation resource, source-local value, and more.
Rationale: Corpus-scale conversion requires fantasy, sci-fi, cultivation, requisition, barter, and abstract wealth compatibility.
Control: Records require value form and access channel.

### D17-DDR-002 — Access is not price
Decision: Price is only one possible friction. Availability, permission, legality, custody, scarcity, standing, license, and owner support matter.
Control: Availability outcomes and acquisition records prevent shop-list drift.

### D17-DDR-003 — Inventory is burden/access/custody
Decision: D17 does not define default slots, weight, bulk, or encumbrance.
Control: Inventory/Burden Record captures many burden types without final schema.

### D17-DDR-004 — Reward, loot, and salvage are value-entry
Decision: Rewards, loot, salvage, bounties, faction grants, requisition grants, Project outputs, and crafting outputs are value-entry, not automatic power or ownership.
Control: Value Entry and Ownership/Custody Records require authority, eligibility, burden, and claim state.

### D17-DDR-005 — Requisition and sinks are first-class but not universal
Decision: D17 supports taxes, upkeep, fuel, ammo, repair, debt, dues, contribution, consumption, confiscation, decay, requisition, and source-local sinks without universalizing bookkeeping.
Control: Sink/Requisition/Upkeep Record and anti-poverty-trap guardrail.

### D17-DDR-006 — Donor value systems map by function
Decision: Donor price lists, loot tables, reward schedules, wealth ratings, inventory rules, fuel rules, contribution charts, requisition lists, and sink formulas are evidence only.
Control: Functional donor value mapping ladder and rejected-import notes.

## Acceptance criteria
D17 is accepted if it can:
```text
Classify value by form, access channel, scarcity, legality, ownership/custody, and burden.
Handle acquisition and exchange without assuming price equals access.
Handle reward, loot, salvage, bounty, faction grant, requisition grant, project output, crafting output, and source-local value-entry without automatic ownership or power.
Distinguish custody from ownership.
Represent inventory as burden, access, storage, custody, visibility, maintenance, decay, and transport pressure.
Support multiple burden types without universal slots, weight, or encumbrance.
Support requisition, upkeep, maintenance, consumption, taxes, dues, debt, fuel, ammo, decay, confiscation, cultivation consumption, and source-local sinks without making any universal.
Prevent unrecoverable resource collapse unless explicit high-risk support exists.
Map donor economy systems by function, not label.
Preserve bounded source-local value systems.
Quarantine unsupported value constructs.
Escalate repeated or high-impact missing doctrine.
Route object, world, project, faction, opposition, reward, and campaign effects to owner files without stealing ownership.
```

## Risk fixes embedded
This control file confirms the D17 pre-generation risk audit has been embedded across the pack: money-collapse risk, price-as-access risk, possession-as-ownership risk, free-salvage risk, reward-as-power risk, inventory-default risk, burden-erasure storage risk, post-scarcity no-scarcity risk, free-requisition risk, poverty-trap risk, universal-sink risk, debt-as-money risk, cultivation-resource-as-advancement-currency risk, D10/D09/D13/D15/D18 ownership theft risk, source-local generalization risk, and record-shape final-schema risk.
