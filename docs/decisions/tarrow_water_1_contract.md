# Tarrow water and cleaning — approved #544 implementation contract

Owner approval: Cam, 2026-10-17 America/Denver: “I do approve 544”. The original bounded contract is preserved in issue #544. This document records its approved implementation scope; current certification belongs to the PR/issue evidence, not to this heading.

## Player outcome and current status

A player can collect finite water, transport it, distribute it between vessels, wet a cloth, wipe or brush declared dirty surfaces, rinse tools, wring retained liquid into a vessel, and collect loose residue. Water, surface residue and tool condition remain consequential after movement, storage, leaving and restart.

Baseline: merged #543, main `8ca16b2f8104f9b2b7bc50771fce717ef725d526`, tree `acbaff4257e7392bfc774583aec578dd7a0b92d2`. Parent environmental program #540 / locality #538 / action breadth #493. Headquarters excluded.

Cam directed proceeding with the proposed combined package. This issue makes its previously unspecified primitive semantics concrete. **Contract approved for bounded implementation and draft PR preparation; merge and human-play remain separately governed.** AGENTS.md requires escalation for a new semantic primitive. Existing water imagery and static stains are not executable grants.

## Owner routing and scope

RT-010 owns asset contents and material-condition transitions; AFQR-18 retains actual placement; AFQR-19 qualifies current actor/tool/target opportunity; AFQR-20 supplies observations; AFQR-01 retains commitment. Existing custody, storage, lighting, connection and checkpoint procedures keep their owners. This is an implementation within existing semantic authorities, not a new all-owning materials service.

The new owner-local primitives are finite liquid quantity/capacity, retained moisture, removable adhered residue, and suspended residue. Their exact meaning below is authorized by the owner approval of #544. No universal physics, anatomy, potability, damage, disease, chemistry, harvesting or crafting law is adopted.

## One combined delivery

Three connected arrangements share the same profile-driven procedures:

1. Workshop washing: collect and divide water, wet cloth, clean a loose practice panel, rinse/wring and recover supplies.
2. Yard cleanup: brush a second dirty board, collect residue in a tray, bring water from the workshop and rinse the brush.
3. Recovery/logistics: use inherited support, storage and transport to stage, pack, move and later recover wet/dirty equipment without losing contents or connections.

Proposed eight new noncanonical development objects: Wash Bucket, Rinse Basin, Pouring Jug, Cleaning Cloth, Cleaning Brush, Debris Tray, Practice Panel and Sorting Board. Exact starting placements are engineering bindings inside existing workbench/tool-station positions, not claims about Tarrow resources or new geography.

The bucket starts with 12 development water units and capacity 12; basin capacity 6; jug capacity 3; cloth moisture capacity 2. Practice Panel starts with 3 adhered residue units; Sorting Board with 4. Cloth retained-residue capacity 2/removal rate 1 per wipe; brush capacity 4/rate 2 per scrub. Debris Tray capacity 7 for collected residue. All other water/residue quantities begin at zero. Values are configurable fixture examples, not native item statistics. No replenishing water source or access to the visible channel is inferred.

## State and conservation contract

1. Whole nonnegative integer water units measure only declared liquid quantities. They are not object mass, burden or general container-volume law. All quantities and capacities are explicit profile facts; unknown compatibility refuses.
2. Keep **adhered/collected residue** distinct from **residue suspended in retained liquid**. Cloth wetness is derived from its actual retained water; a wet adjective is not an independent boolean.
3. Residue quantities use exact nonnegative rational arithmetic and canonical numerator/denominator serialization. No floating drift or hidden rounding loss. Whole water units do not imply indivisible residue.
4. Water in a liquid holder is uniformly mixed for these explicitly mobile development residues. Moving q of W water units moves q/W of its suspended residue. Adhered residue remains on the source.
5. Cloth capacity bounds its retained water. Its retained adhered residue has a separate capacity; suspended residue follows the liquid. No implicit water displacement from residue volume is modeled.
6. Every committed transition conserves total water and total residue across all tracked objects. There is no deletion sink, automatic replenishment, evaporation, disappearing dirt or conversion into a generic clean flag.
7. Every fixture object retains its ordinary identity and exactly one placement. Contents/condition travel with that identity through custody, storage and qualified displacement. Cleaning does not manufacture a replacement object.
8. Profiles declare object kind, capacities, transfer/removal rates, actor qualification and allowed operation pairs. Shared reducers contain no Tarrow entity-ID branches.

## Operations and exact semantics

| Operation | Qualification | Authoritative effect |
| --- | --- | --- |
| Pour q units from A into B | q is a positive integer; declared vessel pair; source has q; destination has capacity | Transfer exactly q water plus proportional suspended residue; adhered residue remains |
| Fill B from A | Declared source/recipient vessels; both accessible | Transfer min(source water, free destination capacity), stated explicitly in result; zero transfer refuses |
| Empty A into B | Declared vessel pair; B can hold every source water unit | Transfer all water and suspended residue; overflow refuses before mutation |
| Soak cloth from A | Qualified carried absorbent tool; source has water; tool has free moisture capacity | Transfer one development water unit and its proportional suspended residue into cloth |
| Wipe surface using cloth | Qualified surface and carried wet cloth; compatible removable residue; tool capacity | Transfer min(surface adhered residue, cloth free adhered capacity, declared rate) to cloth adhered residue |
| Scrub surface using brush | Qualified surface and carried brush; compatible residue; tool capacity | Transfer bounded adhered residue to brush; no water or wetness required by this dry method |
| Rinse tool in basin | Qualified vessel containing at least one water unit; compatible cloth/brush | Release removable adhered residue into the bath. For absorbent tools, mix bath and retained liquid, then redistribute suspended residue uniformly while preserving each participant's water quantity |
| Wring cloth into B | Qualified carried absorbent tool with water; B has sufficient free capacity | Transfer all retained water and its suspended residue; **adhered residue stays on the cloth** |
| Collect residue from tool into tray | Qualified dry-residue receiving tray with capacity | Transfer all tool adhered residue into the tray; overflow refuses, retained/suspended liquid is unchanged |

Rinse may reduce suspended residue remaining in a cloth when used with fresh water; it never promises a perfectly clean cloth from dirty wash water. Repeating an already-zero-effect operation refuses without an event. Methods cannot silently substitute for one another: dry wiping, pouring a brush, wringing a vessel, or generic “clean” without a clear method cannot become an unrelated success.

Tool capacities, kinds and removal rates are explicit neutral profiles. No solvent, stain, embedded grime, filtration, settling, sterilization or drinkability inference. The first package models only compatible mechanically removable development residue.

## Access, motion and observation

- Resolve participants for the selected actor at execution. Both must be currently accessible and at the actual local position; same building labels and remembered names do not grant reach.
- Pour/empty/wring require source control through carried custody; cleaning/soaking/rinsing require a qualified carried tool. Receiver/surface may be directly placed or supported where expressly admitted. Actor opportunity is profile-based; no universal hand count, anatomy, strength or skill is inferred.
- Closed containment blocks interior access. A reachable exterior surface remains distinct. Existing support/connection movement constraints remain; no group-motion exception is introduced.
- Visible wet/dirty state and accessible vessel contents may be inspected, including actual quantities under explicit development observation profiles. Hidden contents and remote state cannot leak through help, inspection or different refusal wording.
- Held tools and vessels can travel and enter admitted storage without losing water/residue. No universal spill, tipping, breakage, load or closed-liquid-container rule is inferred.
- Cleaning a development surface removes tracked removable residue only. It does not erase authored scratches, historical wear, writing, damage or memories.
- No passive drying, wet transfer to arbitrary neighbors, time-based work, action costs or broader NPC routine is silently introduced. Such extensions require their own causal contracts.

## Public integration and persistence

Provide a separate opt-in `tarrow-water` binding extending material preview capabilities. Existing `tarrow`, `tarrow-depth`, `tarrow-material`, default fixture and old checkpoints keep their meanings.

Public single-step and exactly-two-step input share pure classification and the same execution route. Preserve amount, method and all participants/modifiers. Unsupported modifiers or extra steps must not simplify into success; compound execution requalifies and durably stops after the first failed step.

Each transition has current opportunity evidence and command/preview/delta/receipt identities with combined pre/post digests. New quantities and both residue compartments participate in the authoritative digest. Refusal leaves all world state unchanged.

The new versioned checkpoint binding contains root/profile witnesses and a chronological journal of every material, water and retained-owner transition. Restore reconstructs from the declared root and re-executes qualified operations, checking receipts, chronology and final combined state; a resealed final snapshot is not trusted. Old bindings reject the new envelope rather than silently interpreting it.

Extend the existing transaction boundary so every relevant state family rolls back together on failed persistence; no successful acknowledgement precedes durability, and further mutation halts after an uncertain write until validated restart. Deliberate repeats are new attempts; restored journal entries preserve their original command identities. No new network retry protocol or distributed event-store claim.

## Combined acceptance

- Three installed arrangements repeated with intermediate restart, objective checks and complete trace/digest joins.
- Water and residue conservation on exact transfer, partial fill, saturated tool, dirty-water rinse, wring, collection, movement, storage and restore.
- Demonstrate dirty-water cross-transfer: splitting/pouring wash water cannot make all receivers clean; wringing cannot remove adhered residue.
- Opposite preconditions, self-transfer, invalid/negative/fractional/bool amounts, empty/full sources/receivers, ambiguity, dark/remote/closed participants and stale opportunity.
- Method fidelity and direct/two-step receipt parity; failed later steps preserve earlier durable changes.
- Checkpoint root/profile/quantity/residue/receipt/chronology forgery and write failures before/after replacement.
- Different capacities, identities, starting states and allowed pairs operate through configuration alone; no per-goal success flags.
- Isolated mutations must demonstrate conservation, capacity, residue-compartment, access and replay checks detect defects with passing controls.
- Focused old-owner and locality regressions; full local suite and exact-head Linux/Windows CI before certification.
- Engineering-authored evidence is separate from blind/human acceptance. Parent milestones remain open.


## Continuing development

See [water_domain_expansion_register.md](water_domain_expansion_register.md) for current domain limits, concrete reopening triggers, dependency order and extension acceptance. Revisit affected rows whenever another package touches liquids, exposure, time, terrain, infrastructure, living beings or extraordinary effects. The register tracks future work; it is not approval to implement those extensions.

