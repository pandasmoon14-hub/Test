# Stage 11A — Skill Check Patch v0.1

This patch incorporates a clean skill and ability check layer into the live Astra-facing packets before further production stages continue.

## Why this patch exists

The Stage 11 player chassis already had:
- D20 core resolution
- six Attributes
- three Resistances
- Paths
- Techniques

But it was too thin on ordinary trained competence:
- sneaking
- climbing
- bluffing
- tracking
- healing support
- analysis
- perception

This patch adds a stable skill system without replacing the donor-compatible Attribute-check chassis.

## Design rule

Astra keeps Attribute checks as the base engine, then layers trained skill ranks on top when formal competence matters.

Skill Checks use:

**D20 + governing Attribute modifier + Skill Rank bonus + situational modifiers**
