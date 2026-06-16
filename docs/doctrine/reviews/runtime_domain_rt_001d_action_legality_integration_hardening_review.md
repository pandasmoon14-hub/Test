# RUNTIME-DOMAIN-RT-001D — Action Legality Integration Hardening Review

**Date:** 2026-06-16
**Artifact ID:** RUNTIME-DOMAIN-RT-001D-ACTION-LEGALITY-INTEGRATION-HARDENING-REVIEW-001
**Follows:** RUNTIME-DOMAIN-RT-001C (action legality gate integration skeleton, merged as PR #313)
**Status:** review-only — no runtime behavior, no implementation authority

---

## 1. Purpose and scope

RT-001D is a hardening review over the merged RT-001B (PR #312) and RT-001C (PR #313) surfaces. It does not implement a real legality engine, command execution, runtime state reads, state mutation, event append/commitment, persistence/replay writes, RNG/table/oracle execution, resource/consequence math, model calls, prompt rendering, narration, live-play behavior, UI/client behavior, conversion, sourcebook inclusion, or canon promotion.

RT-001D confirms:

- The RT-001B action legality skeleton creates reference-only request/result vocabulary with frozen, keyword-only dataclasses, controlled constants, validated serializers, and false-only authority flags.
- The RT-001C action legality gate integration skeleton bridges the PR-9A through PR-9E command-path reference seam into RT-001B using inert references only, defaulting to `deferred`/`unknown` and never producing real `legal` approval.
- The boundary separations, containment rules, and non-authority constraints established by RT-001A (PR #311), RT-001B (PR #312), and RT-001C (PR #313) are intact and testable.

RT-001D authorizes no implementation behavior. It is a review-only artifact.

---

## 2. Source stack reviewed

| PR | Title | Merged as | Status |
|---|---|---|---|
| RT-001A | Action Legality Service Plan and Execution Boundary Review | PR #311 | planning/review only |
| RT-001B | Action Legality Skeleton Dataclasses, Constants, Validators, Serializers | PR #312 | skeleton only |
| RT-001C | Action Legality Gate Integration Skeleton | PR #313 | skeleton only |

All three PRs are merged to `main` as of this review.

---

## 3. Current authorized surfaces

The following surfaces exist on `main` after RT-001C:

### RT-001B surfaces (action_legality_skeleton.py)

- **Constants:** `LEGALITY_STATUSES` (7), `BLOCKER_CLASSES` (19), `SAFE_PLAYER_MESSAGES` (21), `REFERENCE_KINDS` (13), `DEPENDENCY_OWNERS` (11)
- **Dataclasses:** `ActionLegalityReference`, `ActionLegalitySubjectReference`, `ActionLegalityTargetReference`, `ActionLegalityDependencyReference`, `ActionLegalityBlocker`, `ActionLegalityBackendDetail`, `ActionLegalityVisibilityEnvelope`, `ActionLegalityRequest`, `ActionLegalityResult`, `ActionLegalityAuthorityFlags` (30 false-only flags)
- **Factories:** `make_action_legality_reference`, `make_action_legality_subject_reference`, `make_action_legality_target_reference`, `make_action_legality_dependency_reference`, `make_action_legality_blocker`, `make_action_legality_backend_detail`, `make_action_legality_visibility_envelope`, `make_action_legality_request`, `make_action_legality_result`
- **Validators:** One per dataclass
- **Error hierarchy:** Typed errors per dataclass
- **Hidden-information containment:** `_HIDDEN_INFO_SAFE_MESSAGES` subset enforced at construction

### RT-001C surfaces (action_legality_gate_integration_skeleton.py)

- **Constants:** `ACTION_LEGALITY_GATE_INTEGRATION_STAGES` (8), `ACTION_LEGALITY_GATE_ROUTES` (13), `ACTION_LEGALITY_GATE_DEFAULT_STATUSES` (2: `deferred`, `unknown`), `ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE`
- **Dataclasses:** `ActionLegalityGateInputRefs`, `ActionLegalityGateDependencyPlan`, `ActionLegalityGateIntegrationAuthorityFlags` (32 false-only flags), `ActionLegalityGateIntegrationRequest`, `ActionLegalityGateIntegrationResult`
- **Factories:** `create_action_legality_gate_input_refs`, `create_action_legality_gate_dependency_plan`, `create_action_legality_gate_integration_authority_flags`, `create_action_legality_gate_integration_request`, `create_action_legality_gate_integration_result`
- **Builders:** `build_action_legality_request_from_gate_integration`, `build_deferred_action_legality_result_from_gate_integration`, `build_unknown_action_legality_result_from_gate_integration`, `build_action_legality_gate_integration_result`
- **Serializers:** `serialize_action_legality_gate_integration_result` (backend), `serialize_action_legality_gate_integration_result_visible` (player-visible)
- **Validators:** One per dataclass plus authority flags validator

---

## 4. Current non-authority boundaries

RT-001D confirms the following are NOT authorized by any merged PR in the RT-001 series:

| Forbidden scope | Responsible RT owner | Authorized? |
|---|---|---|
| Legality evaluation engine | RT-001 (future) | No |
| Command execution | RT-001 (future) | No |
| State read service | Future state service | No |
| State mutation | Future state service | No |
| Event append / commitment | Future transaction lifecycle service | No |
| Persistence / replay writes | Future persistence service | No |
| RNG / table / oracle execution | RT-009 | No |
| Resource / consequence math execution | RT-002 | No |
| Affordability / reservation / settlement | RT-002 | No |
| Consequence application | RT-002 / RT-003 / RT-004 | No |
| Combat resolution | RT-003 | No |
| Ability / effect / skill resolution | RT-004 | No |
| Inventory mutation | RT-010 | No |
| Mission / clue / reward routing | RT-006 | No |
| Social / faction mutation | RT-007 | No |
| Context packet compilation | RT-005 | No |
| Model calls / prompt rendering / execution | Future model harness | No |
| Narration generation | Future narration service | No |
| Live-play adapter / UI / client | Future live-play gate | No |
| Conversion | Aether Forge pipeline | No |
| Sourcebook inclusion | Astra editorial process | No |
| Canon promotion | Astra Doctrine Council / RT-012 | No |

---

## 5. Confirmed invariants

### INV-001: RT-001B creates reference-only vocabulary

The RT-001B `action_legality_skeleton.py` module provides frozen, keyword-only dataclasses, controlled constant sets, factory functions, validators, and deterministic `to_dict()` serializers. It does not contain any legality evaluation engine, rule engine, command execution, state access, model call, or side-effecting function.

**Confirmed.**

### INV-002: RT-001C bridges PR-9A through PR-9E into RT-001B using inert references only

The RT-001C `action_legality_gate_integration_skeleton.py` module imports only RT-001B typed surfaces and provides bridge dataclasses that carry PR-9A (scene command execution assembly), PR-9C (command-kind routing), PR-9D (validation integration bridge), and PR-9E (transaction preview packet bridge) references as `ActionLegalityReference` instances. It does not import from, call, or depend on the builders or execution logic of PR-9A/9C/9D/9E modules.

**Confirmed.**

### INV-003: RT-001C defaults to deferred/unknown

The `ACTION_LEGALITY_GATE_DEFAULT_STATUSES` constant is `frozenset({"deferred", "unknown"})`. The `build_action_legality_gate_integration_result` builder accepts a `status_override` parameter that must be one of these two statuses. The `ActionLegalityGateIntegrationResult.__post_init__` rejects any `legality_result` whose `legality_status` is not in this set.

**Confirmed.**

### INV-004: RT-001C must not carry real legal approval

Any attempt to construct an `ActionLegalityGateIntegrationResult` with a `legality_result` that has `legality_status="legal"` raises `InvalidActionLegalityGateIntegrationResultError`. The builder function `build_action_legality_gate_integration_result` rejects `status_override="legal"` with `ActionLegalityGateIntegrationSkeletonError`. The factory function `create_action_legality_gate_integration_result` also rejects `legal` results because it delegates to the constructor.

**Confirmed.**

### INV-005: Direct constructor/factory/legal-status bypass was closed

- The `ActionLegalityGateIntegrationResult` dataclass `__post_init__` enforces `legality_result.legality_status in ACTION_LEGALITY_GATE_DEFAULT_STATUSES`.
- The builder rejects `status_override` values outside `ACTION_LEGALITY_GATE_DEFAULT_STATUSES`.
- The factory delegates to the constructor, inheriting the same gate.
- There is no alternate construction path that bypasses `__post_init__`.

**Confirmed.**

### INV-006: Player-visible serializers do not leak backend-only details

The `serialize_action_legality_gate_integration_result_visible` function returns a dict containing only: `result_id`, `request_id`, `legality_status`, `player_visible_message`, `visible_blocker_messages`, and `non_authority_note`. It does not include `backend_detail`, `backend_only_detail`, `backend_only_refs`, `trace_refs`, `dependency_plan`, `input_refs`, `affected_refs`, `doctrine_refs`, `schema_refs`, `source_local_refs`, `hidden_information_classification`, `resolution_path_summary`, `owner_route`, or `metadata`.

**Confirmed.**

### INV-007: Hidden-information blockers use generic safe messages only

RT-001B enforces that `ActionLegalityBlocker` with `blocker_class="hidden_information"` must use `player_visible_message` from `_HIDDEN_INFO_SAFE_MESSAGES`, which contains only "Not enough information to attempt this action." and "This action cannot be taken right now." These messages do not reveal the existence, nature, or type of hidden information.

**Confirmed.**

### INV-008: Authority flags remain false-only

RT-001B `ActionLegalityAuthorityFlags` (30 fields) and RT-001C `ActionLegalityGateIntegrationAuthorityFlags` (32 fields) both enforce `value is not False` rejection in `__post_init__` for every field. Any non-False value — including `True`, `1`, `0`, `None`, truthy strings — raises the corresponding error.

**Confirmed.**

### INV-009: to_dict() outputs remain deterministic and JSON-safe

All `to_dict()` methods in RT-001B and RT-001C produce dicts containing only JSON-safe types (str, int, float, bool, None, list, dict). Authority flag `to_dict()` methods hardcode all values as `False`, not reflecting user-supplied values. Metadata values are validated by `_validate_json_safe` at construction time, rejecting non-JSON-safe types (sets, custom objects, bytes, etc.).

**Confirmed.**

### INV-010: Dependency plans are references, not calls

`ActionLegalityGateDependencyPlan` holds `ActionLegalityDependencyReference` instances that declare which future owner services would be needed. These references contain `dependency_id`, `dependency_owner`, and `summary` strings. They do not import, instantiate, or call any downstream service.

**Confirmed.**

### INV-011: Guardrail allowlist expansion is recognized

RT-001C required updating the domain module allowlists in the PR-9B hardening review test file to include `action_legality_skeleton` and `action_legality_gate_integration_skeleton`. This expansion was narrow and reviewed. Future PRs must not use this as a precedent for unreviewed module additions.

**Confirmed — flagged as a risk below.**

### INV-012: No donor-family assumptions become Astra runtime law

Neither RT-001B nor RT-001C contains any donor-system-specific constants, command families, action economy terms, or rules. The blocker classes and legality statuses are system-agnostic by design. Source-local content is explicitly quarantined by the `source_local_donor_specific` blocker class, not adopted.

**Confirmed.**

### INV-013: No conversion/canon/sourcebook authority is introduced

RT-001B and RT-001C do not import, reference, or depend on any conversion pipeline, sourcebook registry, or canon promotion mechanism. Authority flags for `conversion_authorized`, `sourcebook_inclusion_authorized`, and `canon_promotion_authorized` are enforced as false-only.

**Confirmed.**

### INV-014: No live-play/model/narration authority is introduced

RT-001B and RT-001C do not import, reference, or depend on any live-play adapter, model boundary, prompt renderer, narration generator, or UI/client module. Authority flags for `model_call_authorized`, `prompt_rendering_authorized`, `prompt_execution_authorized`, `narration_generation_authorized`, `live_play_authorized`, and `ui_client_authorized` are enforced as false-only.

**Confirmed.**

---

## 6. Risk ledger

### RISK-001: Legal approval bypass risk

**Description:** A future PR could construct an `ActionLegalityResult` with `legality_status="legal"` and pass it to `ActionLegalityGateIntegrationResult` if the `__post_init__` gate were weakened or removed.

**Current mitigation:** The `ActionLegalityGateIntegrationResult.__post_init__` checks `legality_result.legality_status in ACTION_LEGALITY_GATE_DEFAULT_STATUSES` and raises on violation. The builder rejects non-default statuses.

**Residual risk:** Medium — the gate exists but is enforced only at the Python dataclass level, not at a schema or protocol level.

### RISK-002: Backend detail leakage risk

**Description:** The player-visible serializer could accidentally include backend-only fields if its implementation were changed to iterate over all `to_dict()` keys instead of whitelisting specific fields.

**Current mitigation:** `serialize_action_legality_gate_integration_result_visible` constructs its output dict from explicit field names, not from `to_dict()` output.

**Residual risk:** Low — but any future refactoring of the visible serializer must be reviewed for leakage.

### RISK-003: Hidden-information specificity risk

**Description:** A future blocker class or player-visible message could reveal the existence or nature of hidden information (e.g., "You cannot attack the invisible entity").

**Current mitigation:** RT-001B enforces `_HIDDEN_INFO_SAFE_MESSAGES` subset for `hidden_information` blockers. `SAFE_PLAYER_MESSAGES` is a controlled frozenset.

**Residual risk:** Low — but expanding `SAFE_PLAYER_MESSAGES` or `_HIDDEN_INFO_SAFE_MESSAGES` requires review.

### RISK-004: Dependency reference accidentally becoming a service call

**Description:** `ActionLegalityDependencyReference` and `ActionLegalityGateDependencyPlan` hold string references to future services. A future PR could import and call those services instead of just referencing them.

**Current mitigation:** The skeleton modules contain no imports of downstream service modules. Dependency references are string-based, not object references.

**Residual risk:** Medium — the boundary is social (code review) not structural (type system).

### RISK-005: Guardrail allowlist drift risk

**Description:** The domain module allowlists in the PR-9B hardening review test were expanded to include RT-001B and RT-001C modules. Each future skeleton module will require a similar expansion, which could become rubber-stamped rather than reviewed.

**Current mitigation:** Each expansion is explicit and tracked in the decisions log.

**Residual risk:** Medium — the allowlist pattern works but requires discipline.

### RISK-006: Metadata serialization risk

**Description:** The `_validate_json_safe` helper recursively validates metadata values at construction time. A future change could skip this validation or introduce a new field path that bypasses it.

**Current mitigation:** Both RT-001B and RT-001C apply `_safe_metadata` to all metadata fields in `__post_init__`. The `to_dict()` methods use `copy.deepcopy(dict(self.metadata))`.

**Residual risk:** Low — validation is comprehensive and structural.

### RISK-007: Authority flag bypass risk

**Description:** A future PR could add a new authority flag field with a default of `True`, or bypass the `__post_init__` loop that checks `value is not False`.

**Current mitigation:** Both `ActionLegalityAuthorityFlags.__post_init__` and `ActionLegalityGateIntegrationAuthorityFlags.__post_init__` iterate over `self.__dataclass_fields__` and reject any value that `is not False`.

**Residual risk:** Low — the loop is self-maintaining for new fields as long as defaults remain `False`.

### RISK-008: Constructor/factory divergence risk

**Description:** Factory functions could diverge from constructor behavior if they provide default values that the constructor does not validate, or if they bypass constructor validation by setting attributes directly.

**Current mitigation:** All factory functions delegate directly to their corresponding dataclass constructors. No factory uses `object.__setattr__` or bypasses `__post_init__`.

**Residual risk:** Low — but factory signatures must be reviewed when constructors change.

### RISK-009: Validator being weaker than constructor risk

**Description:** Validators (e.g., `validate_action_legality_gate_integration_result`) could accept objects that the constructor would reject, if the validator checks fewer invariants than `__post_init__`.

**Current mitigation:** Validators check type, required fields, constant membership, and delegate to sub-validators. However, validators return `bool` while constructors raise — the validator cannot check invariants that only exist as constructor-time side effects.

**Residual risk:** Medium — validators and constructors should be kept in sync but there is no structural enforcement.

### RISK-010: PR-9A/9C/9D/9E reference seam overreach

**Description:** RT-001C imports `ActionLegalityReference` typed refs that represent PR-9A scene command execution assembly, PR-9C command-kind routing, PR-9D validation integration bridge, and PR-9E transaction preview packet bridge results. A future PR could expand these refs to carry mutable state, call builders from those modules, or resolve references against live state.

**Current mitigation:** RT-001C imports only RT-001B typed surfaces. The `ActionLegalityGateInputRefs` dataclass accepts `ActionLegalityReference` instances (which are string-based, frozen, inert).

**Residual risk:** Medium — the seam is clean now but must be guarded as the reference seam matures.

### RISK-011: Future action legality engine accidentally reading state before owner service exists

**Description:** When the legality engine is implemented (RT-001E+), it will need to read actor state, target state, scene state, etc. If it attempts to read state before the corresponding state-owner services exist, it may fail silently or produce incorrect results.

**Current mitigation:** The skeleton defaults to `deferred`, which explicitly means "required upstream surface not yet available."

**Residual risk:** Medium — the deferred status is correct behavior, but the engine implementation must enforce it at the service-availability level, not just the skeleton level.

### RISK-012: Donor-specific legality assumptions leaking into runtime baseline

**Description:** A future PR implementing legality rules could embed donor-specific assumptions (e.g., D&D 5e action economy, Pathfinder spell slots, Fate aspects) as baseline Astra rules rather than quarantining them as source-local.

**Current mitigation:** RT-001A defines the `source_local_donor_specific` blocker class and quarantine status. The blocker taxonomy is system-agnostic.

**Residual risk:** Medium — requires review discipline during engine implementation.

### RISK-013: Live-play/model adapter treating skeleton statuses as final adjudication

**Description:** A future live-play adapter or model boundary could treat `deferred` or `unknown` skeleton statuses as final game decisions (e.g., "your action was denied") rather than temporary runtime-immaturity indicators.

**Current mitigation:** RT-001C includes `ACTION_LEGALITY_GATE_NON_AUTHORITY_NOTE` in every result. The player-visible message for deferred is "This action cannot be processed at this time."

**Residual risk:** Medium — the non-authority note is informational, not structurally enforced at the adapter boundary.

---

## 7. Bypass and escalation audit

### Direct constructor bypass

All RT-001B and RT-001C dataclasses are `@dataclass(frozen=True, kw_only=True)`. The `__post_init__` method runs unconditionally on construction. There is no `__init__` override. There is no `@classmethod` constructor that bypasses `__post_init__`. The `object.__setattr__` calls in `__post_init__` are used only to set validated, deep-copied values on frozen fields — not to bypass validation.

**Finding:** No bypass path found.

### Factory bypass

All factory functions delegate to constructors. No factory uses `object.__setattr__`, `type.__call__`, or `dataclasses.fields` manipulation.

**Finding:** No bypass path found.

### Legal status injection

The `ActionLegalityGateIntegrationResult` constructor rejects `legality_result.legality_status` values outside `ACTION_LEGALITY_GATE_DEFAULT_STATUSES`. The builder rejects `status_override` values outside the same set. There is no codepath that produces a `legal` `ActionLegalityGateIntegrationResult`.

**Finding:** No injection path found.

### Escalation note

If a future PR needs to allow `legal` status in the integration result, it must:
1. Add an explicit new gate class or builder function.
2. Update `ACTION_LEGALITY_GATE_DEFAULT_STATUSES` or create a new constant set.
3. Update the hardening review.
4. Pass all existing tests that assert `legal` is rejected.

---

## 8. Hidden-information containment audit

### RT-001B containment

- `ActionLegalityBlocker.__post_init__` enforces: if `blocker_class == "hidden_information"`, then `player_visible_message in _HIDDEN_INFO_SAFE_MESSAGES`.
- `_HIDDEN_INFO_SAFE_MESSAGES` contains only: "Not enough information to attempt this action." and "This action cannot be taken right now."
- These messages do not reveal entity existence, entity type, location, disposition, or any game-state fact.

### RT-001C containment

- RT-001C delegates blocker construction to RT-001B factories, which enforce the same containment rules.
- The `build_deferred_action_legality_result_from_gate_integration` and `build_unknown_action_legality_result_from_gate_integration` builders use only safe messages from `SAFE_PLAYER_MESSAGES`.
- The player-visible serializer outputs only messages that have already passed RT-001B validation.

**Finding:** Hidden-information containment is intact across both modules.

---

## 9. Player-visible message audit

### Messages used by RT-001C builders

| Builder | Message |
|---|---|
| `build_deferred_action_legality_result_from_gate_integration` | "This action cannot be processed at this time." |
| `build_unknown_action_legality_result_from_gate_integration` | "Action could not be validated." |

Both messages are members of `SAFE_PLAYER_MESSAGES`.

### Visible serializer output

`serialize_action_legality_gate_integration_result_visible` returns:
- `player_visible_message`: from `visibility_envelope.player_visible_message` or first blocker message
- `visible_blocker_messages`: from blocker `player_visible_message` values

All values are validated at construction time to be in `SAFE_PLAYER_MESSAGES`.

**Finding:** No unsafe messages can reach the player-visible serializer output.

---

## 10. Metadata / serialization audit

### JSON safety

- Both RT-001B and RT-001C apply `_validate_json_safe` recursively to all metadata at construction time.
- `_validate_json_safe` accepts: `None`, `str`, `int` (excluding `bool` subclass), `float`, `bool`, `list`/`tuple` (recursively), `dict`/`Mapping` with string keys (recursively).
- `_validate_json_safe` rejects: `set`, `frozenset`, `bytes`, custom objects, non-string dict keys.

### to_dict() determinism

- All `to_dict()` methods produce dict output using `copy.deepcopy(dict(self.metadata))` for metadata fields and deterministic list comprehensions for tuple fields.
- Authority flag `to_dict()` methods return `{field_name: False for field_name in self.__dataclass_fields__}`, hardcoding `False` regardless of field values (which must be `False` anyway due to `__post_init__`).

### Serialization round-trip safety

- `to_dict()` output can be passed to `json.dumps()` without error for any validly-constructed object.
- `serialize_action_legality_gate_integration_result` returns `result.to_dict()`.
- `serialize_action_legality_gate_integration_result_visible` constructs a whitelist dict.

**Finding:** Metadata and serialization are JSON-safe and deterministic.

---

## 11. Authority-flag audit

### RT-001B: ActionLegalityAuthorityFlags

- 30 boolean fields, all defaulting to `False`.
- `__post_init__` iterates all fields; rejects any value where `value is not False`.
- `to_dict()` returns `{field_name: False for field_name in self.__dataclass_fields__}`.
- Tested values that must be rejected: `True`, `1`, `0`, `None`, `"yes"`, `""`, `[]`.

### RT-001C: ActionLegalityGateIntegrationAuthorityFlags

- 32 boolean fields (adds `real_legality_evaluation_authorized` and `state_read_authorized`), all defaulting to `False`.
- `__post_init__` iterates all fields; rejects any value where `value is not False`.
- `to_dict()` returns `{field_name: False for field_name in self.__dataclass_fields__}`.

### Cross-module authority flag consistency

Both authority flag classes use the same pattern: iterate `__dataclass_fields__`, check `is not False`, hardcode `False` in `to_dict()`. The pattern is self-maintaining for new fields.

**Finding:** Authority flags are hardened. No truthy value can survive construction.

---

## 12. Corpus-scale donor pressure audit

### Blocker taxonomy coverage

The 19 blocker classes in `BLOCKER_CLASSES` are designed to be system-agnostic. They cover:
- Actor/target existence and reachability
- Authority/capability/permission gates
- Scene/location boundaries
- Command-kind routing and validation integration
- Resource prerequisites (existence, not affordability)
- Timing/cooldown/phase
- Hidden information
- Ambiguity/clarification
- Unsupported command families
- Source-local/donor-specific mechanics
- Doctrine and schema gaps
- Runtime owner handoff
- Policy/safety/meta-action
- Anti-authority

### Pressure scenarios

- **D&D 5e "bonus action" command:** Would be classified by PR-9C routing, then evaluated by legality. If "bonus action" is not an Astra-native action economy term, it receives `source_local_donor_specific` blocker and `quarantined` status.
- **Pathfinder "attack of opportunity" reaction:** Same path — classified, quarantined if not Astra-native.
- **Fate "compel" using fate points:** Resource prerequisite existence check (fate points are a resource category). If fate points are not an Astra resource category, `resource_prerequisite` blocker applies.
- **Shadowrun "matrix action":** If no Astra schema for matrix actions, `schema_gap` or `unsupported_command_family` blocker applies.
- **PbtA "move" trigger:** Classified by routing. If the move trigger is not mappable to an Astra command kind, `command_kind_routing` blocker or `quarantined` status.

### Donor pressure containment

No donor-specific constant, term, or assumption exists in RT-001B or RT-001C. Source-local material is quarantined by design.

**Finding:** The blocker taxonomy and quarantine mechanism handle corpus-scale pressure without donor-family leakage.

---

## 13. Future implementation readiness gates

Before any future RT-001E+ implementation PR can proceed, the following gates must be satisfied:

1. **RT-001D review accepted** — this document must be reviewed and merged.
2. **No open risk-ledger items blocking implementation** — RISK-001 through RISK-013 must be acknowledged or mitigated.
3. **Interface contract defined** — RT-001E must define the legality service interface contract (input types, output types, error types, dependency declarations) before any evaluation logic is implemented.
4. **State-owner service interface exists** — The legality engine cannot read actor/target/scene state until the state-owner service interface is defined (even as a skeleton).
5. **Downstream RT-owner service interfaces exist** — Resource math (RT-002), combat resolution (RT-003), ability resolution (RT-004), and other downstream services must have at least skeleton interfaces before legality can declare dependencies on them.
6. **Guardrail allowlist expansion reviewed** — Any new module added to the domain must update the allowlists and pass the guardrail tests.
7. **Hidden-information containment preserved** — Any new blocker class or player-visible message must be reviewed for hidden-information leakage.
8. **Authority flags extended, not bypassed** — New authority flags may be added, but existing false-only enforcement must be preserved.

---

## 14. Required sequencing for future RT-001E+

| Step | Title | Prerequisites |
|---|---|---|
| RT-001E | Action Legality Service Interface Contract Skeleton | RT-001D accepted |
| RT-001F | Action Legality Service Interface Hardening Review | RT-001E merged |
| RT-001G+ | Action Legality Evaluation Implementation (phased) | RT-001F accepted, state-owner service interface defined, downstream RT-owner interfaces defined |

RT-001E must not implement evaluation logic. It must define the interface contract only.

---

## 15. Explicitly forbidden future shortcuts

The following shortcuts are explicitly forbidden:

1. **Bypassing the legal-status gate** — No PR may weaken the `ActionLegalityGateIntegrationResult.__post_init__` check that rejects non-`deferred`/`unknown` statuses without a full hardening review.
2. **Treating deferred/unknown as legal** — No downstream service may interpret `deferred` or `unknown` as permission to proceed with execution.
3. **Expanding SAFE_PLAYER_MESSAGES without review** — New messages must be reviewed for hidden-information leakage.
4. **Adding authority flags defaulting to True** — All authority flags must default to `False` and be validated as `is not False` in `__post_init__`.
5. **Importing downstream service modules from skeleton modules** — Skeleton modules must not import state stores, transaction lifecycle, event commitment, RNG/table/oracle, resource math execution, context packet compiler execution, model boundary execution, or live-play/UI modules.
6. **Calling downstream services from dependency plans** — Dependency plans must remain string-reference-only.
7. **Embedding donor-specific rules as Astra baseline** — All donor-specific material must be quarantined via `source_local_donor_specific` blocker.
8. **Promoting conversion/canon/sourcebook from within legality** — Legality identifies but does not promote.
9. **Using model output as legality determination** — LLMs do not determine legality. The backend does.
10. **Skipping guardrail allowlist updates** — Every new domain module must be added to the allowlists and pass the guardrail tests.

---

## 16. Acceptance criteria

RT-001D is accepted when:

1. This review document exists and names RT-001A, RT-001B, and RT-001C.
2. This review document confirms RT-001D is review-only and does not authorize implementation.
3. All 14 confirmed invariants (INV-001 through INV-014) are verified.
4. All 13 risk ledger entries (RISK-001 through RISK-013) are documented.
5. The bypass and escalation audit finds no open bypass paths.
6. The hidden-information containment audit confirms containment is intact.
7. The player-visible message audit confirms no unsafe messages can reach output.
8. The metadata/serialization audit confirms JSON safety and determinism.
9. The authority-flag audit confirms false-only enforcement.
10. The corpus-scale donor pressure audit confirms no donor-family leakage.
11. The test file `tests/test_runtime_domain_rt_001d_action_legality_integration_hardening_review.py` passes.
12. Existing RT-001B and RT-001C tests still pass.
13. No implementation modules were modified.

---

## 17. Next recommended step

**RT-001E — Action Legality Service Interface Contract Skeleton**

Unless this review identifies findings that require a narrower remediation PR first, the next step is RT-001E: defining the legality service interface contract as a skeleton (input types, output types, error types, dependency declarations, no evaluation logic).

---

## Classification block

```yaml
runtime_domain_rt_001d:
  review_id: RUNTIME-DOMAIN-RT-001D-ACTION-LEGALITY-INTEGRATION-HARDENING-REVIEW-001
  artifact_type: action_legality_integration_hardening_review
  implementation_status: review_only
  derives_from:
    - RUNTIME-DOMAIN-RT-001A-ACTION-LEGALITY-SERVICE-PLAN-001
    - RUNTIME-DOMAIN-RT-001B-ACTION-LEGALITY-SKELETON-001
    - RUNTIME-DOMAIN-RT-001C-ACTION-LEGALITY-GATE-INTEGRATION-SKELETON-001
  authorizes_legality_engine: false
  authorizes_command_execution: false
  authorizes_state_mutation: false
  authorizes_event_commitment: false
  authorizes_persistence_replay: false
  authorizes_rng_table_oracle: false
  authorizes_resource_math: false
  authorizes_model_integration: false
  authorizes_narration: false
  authorizes_live_play: false
  authorizes_conversion: false
  authorizes_sourcebook_inclusion: false
  authorizes_canon_promotion: false
  confirmed_invariants: 14
  risk_ledger_entries: 13
  next_step_authorized: RT-001E action legality service interface contract skeleton
  next_step_status: pending_review
```
