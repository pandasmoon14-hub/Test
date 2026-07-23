# AFQR-03 - Action Representation, Capability, Affordance, Method Selection, and Bounded Plans

**Selected architecture:** Typed Action Gateway with Registered Semantics, Capability-Affordance Composition, and Bounded Plan Verification  
**Ratification status:** `ratified_architecture_not_implementation_authority`  
**Repository baseline:** `main@928bb79ce00a2de749d127dcc5cb8299de788a15`

## Owned question
Defines how freeform player language becomes a lawful backend action without a universal effect soup, generic freeform commands, or model-invented methods.

## Central law
> The backend executes only registered action semantics. A lawful action route exists only where a registered method, actor capability, target or environment affordance, and applicable constraints compose successfully. The model may propose a route but cannot invent one. Multi-step plans must be bounded, typed, and verified before execution.

## Universal components
- Action-definition and action-method registry.
- Typed verb, target, instrument, posture, and declared-purpose fields.
- Capability requirements distinct from permission and access.
- Affordance declarations owned by target or environment domains.
- Registered interfaces and bridge handoffs for cross-domain action methods.
- Legality preview and cost/risk quotation.
- Bounded plan graph with step count, branch count, and verification limits.
- Material-alternative detection and player confirmation.
- Source-local method containment.
- Visibility-safe blocker and alternative projection.

## Core contracts
- `ActionDefinition`
- `ActionMethodDefinition`
- `CapabilityRequirement`
- `AffordanceDeclaration`
- `ActionRouteCandidate`
- `ActionLegalityPreview`
- `BoundedPlan`
- `PlanVerificationReceipt`
- `MaterialAlternativeNotice`
- `ActionGatewayHandoff`

## Determination or execution pipeline
1. interpret intended outcome
2. identify registered action families
3. resolve candidate methods
4. compose actor capabilities with target and environment affordances
5. invoke AFQR-05 bridges when required
6. quote visible costs and risks
7. verify any bounded plan
8. obtain confirmation for material alternatives
9. compile one immutable AFQR-02 command

## Ratified constraints and amendments
- Competency, capability, permission, access, equipment, and affordance remain distinct.
- A target being physically reachable does not imply a legal or supported action method.
- An ability name or donor verb does not authenticate runtime semantics.
- Generic metadata cannot carry executable effects.
- Plans cannot contain unbounded search, recursion, or autonomous objective optimization.
- The gateway may return no lawful route without fabricating one.
- A changed method with different cost, risk, timing, target, or consequence is a material alternative.

## Guarantees
- Registered action semantics.
- No model-invented backend method.
- Capability-affordance separation.
- Bounded multi-step planning.
- Visibility-safe legal alternatives.

## Non-guarantees
- Every fictional action is currently implemented.
- Capability implies permission.
- Affordance implies success.
- A plan reserves resources or commits consequences.

## Required non-mutating prototype
A non-mutating action-route resolver for direct, unavailable, source-local, cross-domain, and multi-step actions, including material-alternative confirmation and no-lawful-route outcomes.

## Required artifacts
- AFQR-03 ADR
- action and method registry schemas
- capability and affordance contracts
- legality preview schema
- bounded-plan verifier
- source-local route certification pack

## Blocked work
- generic freeform executable commands
- universal effect records
- unbounded autonomous planning
- silent method substitution

## Work unlocked
- AFQR-05 cross-system route discovery
- AFQR-02 command compilation
- runtime action legality readers

## Cross-question handoff
AFQR-03 selects and verifies the action route; later AFQRs determine timing, claims, quantities, identity, and dependencies.

## Authority posture
This ADR is architectural doctrine. It does not create runtime state, authorize mutation, promote donor content to canon, or permit model adjudication.
