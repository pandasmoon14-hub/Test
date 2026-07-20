# Runtime Baseline Failure Inventory

## Status

- **Inventory ID:** `RUNTIME-BASELINE-FAILURE-INVENTORY-2026-07-20`
- **Repository:** `pandasmoon14-hub/Test`
- **Baseline branch:** `main`
- **Baseline commit:** `928bb79ce00a2de749d127dcc5cb8299de788a15`
- **Baseline source:** merged RT-002F / PR #325
- **Document type:** maintenance and rehabilitation audit
- **Runtime authority:** none
- **AFQR authority:** none; this inventory records repository condition only
- **Reproduction status:** complete for the runtime and full repository suites
- **Gate R0 status:** repair and post-repair verification still open

## Purpose

This document freezes the failing repository baseline before AFQR-01–20 consolidation or further RT-series implementation.

It prevents:

1. treating pre-existing failures as regressions introduced by later consolidation;
2. repairing tests by weakening guardrails or broadening runtime authority;
3. resuming RT-002G before the repository is green;
4. confusing extraction/conversion maintenance with runtime repair.

The extraction/conversion subsystem remains disconnected from runtime. Baseline repair must not create imports, provenance links, donor identifiers, conversion metadata, or other origin-bearing paths into `astra_runtime`.

## Exact reproduction

The baseline was reproduced from a clean detached checkout of:

```text
928bb79ce00a2de749d127dcc5cb8299de788a15
```

Environment:

```yaml
operating_system: Windows
python: 3.12.10
pip: 26.1.2
pytest: 9.1.1
PyYAML: 6.0.3
installation:
  astra_runtime: editable
```

The documented setup exposed an additional maintenance gap: `requirements-dev.txt` installed PyYAML but did not install pytest. Pytest was installed separately in the isolated baseline environment. This did not cause the 47 runtime failures, but the dependency declaration must be corrected before the repository can claim a reproducible developer setup.

### Runtime suite

```text
python -m pytest tests/runtime -q --tb=short -ra
47 failed, 1443 passed
```

### Full repository suite

```text
python -m pytest -q --tb=short -ra
94 failed, 8428 passed, 12 skipped, 2 xfailed, 1 warning
```

The full-suite total is not evidence of 94 independent defects. It contains:

```yaml
direct_runtime_failures: 47
additional_top_level_failures: 47
additional_direct_stale_guardrails: 15
additional_nested_upstream_pass_through_failures: 32
```

All observed failures reduce to the same two root clusters:

1. stale and duplicated runtime-domain package allowlists;
2. a package-export namespace collision between two owner-scoped `StateVisibilityDescriptor` contracts.

No third runtime root-cause cluster was observed.

## Failure-cluster inventory

### RB-FAIL-001 — Stale runtime-domain package allowlists

- **Confidence:** reproduced
- **Runtime-suite nodes:** 15
- **Full-suite additional direct guardrail nodes:** 15
- **Affected unauthorized file set:** eight legitimate RT-001H through RT-002F modules
- **Primary classification:** `stale_allowlist_or_manifest`
- **Secondary risks:** `runtime_authority`, `import_boundary`, `AFQR_conformance`

Every failing guardrail reported the same current files as unauthorized:

```text
action_legality_service_interface_contract_skeleton.py
object_lever_event_commit_state_delta_path.py
object_lever_interaction_legality_reader.py
object_lever_replay_audit_check.py
object_lever_transaction_preview_bridge.py
projection_visibility_adapter_v0_1.py
read_only_vertical_slice_state_owner_facade.py
state_owner_interface_contract_skeleton.py
```

These files are present intentionally. The tests are stale because each historical test embeds its own snapshot of the package surface.

Correct remediation:

1. create one test-only authoritative runtime-domain manifest;
2. record each module's status and permitted authority;
3. route every current package-surface guardrail through that manifest;
4. preserve strict rejection of undeclared files;
5. remove or delegate duplicated historical allowlists;
6. ensure runtime code cannot import or use the test manifest as authority.

Prohibited remediation:

- deleting package-surface guardrails;
- using wildcard acceptance;
- marking every domain module authoritative;
- treating historical branch-specific package snapshots as permanent law.

#### Runtime-suite RB-FAIL-001 nodes

- `tests/runtime/test_command_envelope_skeleton.py::TestNoUnauthorizedModules::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_context_projection_skeleton.py::TestGuardrails::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_domain_event_commitment_skeleton.py::TestGuardrailsDomainPackage::test_domain_package_contains_only_authorized_files`
- `tests/runtime/test_domain_state_store_skeleton.py::TestGuardrailsDomainPackage::test_domain_package_contains_only_authorized_files`
- `tests/runtime/test_domain_transaction_lifecycle_skeleton.py::TestGuardrailsDomainPackage::test_domain_package_contains_only_authorized_files`
- `tests/runtime/test_domain_validation_integration_skeleton.py::TestGuardrailsDomainPackage::test_domain_package_contains_only_authorized_files`
- `tests/runtime/test_event_ledger_skeleton.py::TestNoUnauthorizedModules::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_hidden_information_skeleton.py::TestGuardrails::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_persistence_boundary_skeleton.py::TestPersistenceBoundaryGuardrails::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_replay_audit_skeleton.py::TestReplayAuditGuardrails::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_rng_interface_skeleton.py::TestNoUnauthorizedModules::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_runtime_trace_skeleton.py::TestRuntimeTraceGuardrails::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_state_delta_skeleton.py::TestNoUnauthorizedModules::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_table_oracle_skeleton.py::TestNoUnauthorizedModules::test_domain_package_contains_only_authorized_modules`
- `tests/runtime/test_validation_pipeline_skeleton.py::TestGuardrails::test_domain_package_contains_only_authorized_modules`

#### Full-suite additional direct RB-FAIL-001 nodes

- `tests/test_runtime_domain_pr_0_domain_service_implementation_sequencing_plan.py::TestRuntimeGuardrails::test_domain_package_contains_only_authorized_modules`
- `tests/test_runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.py::TestRuntimeGuardrails::test_domain_package_contains_only_authorized_modules`
- `tests/test_runtime_domain_pr_1b_command_lifecycle_action_legality_skeleton_review.py::TestRuntimeGuardrails::test_domain_package_authorized_files_only`
- `tests/test_runtime_domain_pr_2_state_store_state_projection_service_plan.py::TestDomainPackageGuardrails::test_domain_package_authorized_files_only`
- `tests/test_runtime_domain_pr_2b_state_store_state_projection_skeleton_review.py::TestRuntimeGuardrailsDomainPackage::test_domain_package_contains_only_authorized_files`
- `tests/test_runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.py::TestDomainPackageGuardrails::test_domain_package_authorized_files_only`
- `tests/test_runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.py::TestDomainPackageGuardrails::test_domain_package_contains_only_authorized_files`
- `tests/test_runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.py::TestDomainPackageGuardrails::test_domain_package_authorized_files_only`
- `tests/test_runtime_domain_pr_4b_validation_integration_invariant_enforcement_skeleton_hardening_review.py::test_current_authorized_domain_files_remain_narrow`
- `tests/test_runtime_domain_pr_4d_validation_integration_invariant_enforcement_skeleton_hardening_review.py::test_current_authorized_domain_files_remain_narrow`
- `tests/test_runtime_domain_pr_4f_validation_integration_residual_hardening_review.py::test_authorized_domain_files_remain_exactly_expected`
- `tests/test_runtime_domain_pr_5_resource_consequence_math_service_plan.py::test_authorized_domain_files_remain_exactly_expected`
- `tests/test_runtime_domain_pr_5e_resource_consequence_math_final_planning_hardening_review.py::test_scope_review_and_no_runtime_domain_file_added`
- `tests/test_runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.py::test_scope_review_and_no_runtime_domain_implementation_file_added`
- `tests/test_runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.py::TestRuntimeGuardrails::test_domain_package_contains_only_authorized_modules`

### RB-FAIL-002 — Visibility-contract namespace collision

- **Confidence:** reproduced
- **Runtime-suite nodes:** 32
- **Primary classification:** `signature_drift`
- **Secondary risks:** `hidden_information`, `state_ownership`, `import_boundary`, `AFQR_conformance`

The failing tests call:

```text
create_state_visibility_descriptor(..., hidden_info_safe=...)
```

but receive the package-level factory exported for the later RT-001H owner-interface contract, whose signature does not include `hidden_info_safe`.

The repository contains two intentionally distinct contracts:

```text
astra_runtime.domain.state_store.StateVisibilityDescriptor
astra_runtime.domain.state_owner_interface_contract_skeleton.StateVisibilityDescriptor
```

The state-store contract includes `hidden_info_safe`. The RT-001H owner-interface contract uses policy and redaction fields instead. Package-level wildcard exports allow the later identically named symbols to shadow the state-store symbols expected by the older test.

Correct remediation:

1. import both contracts from their defining modules;
2. preserve their distinct semantics;
3. add a regression proving they are not interchangeable;
4. avoid adding `hidden_info_safe` to the RT-001H contract;
5. avoid treating a caller-provided boolean as universal proof of hidden-information safety;
6. later replace ambiguous package-level names with explicit aliases or a controlled compatibility/deprecation policy.

#### Runtime-suite RB-FAIL-002 nodes

- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordCategories::test_unsupported_category_rejected`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateAuthorityLevels::test_unsupported_level_rejected`
- `tests/runtime/test_domain_state_store_skeleton.py::TestVisibilityTiers::test_all_visibility_tiers_accepted[backend_hidden]`
- `tests/runtime/test_domain_state_store_skeleton.py::TestVisibilityTiers::test_all_visibility_tiers_accepted[gm_visible]`
- `tests/runtime/test_domain_state_store_skeleton.py::TestVisibilityTiers::test_all_visibility_tiers_accepted[actor_visible]`
- `tests/runtime/test_domain_state_store_skeleton.py::TestVisibilityTiers::test_all_visibility_tiers_accepted[player_visible]`
- `tests/runtime/test_domain_state_store_skeleton.py::TestVisibilityTiers::test_all_visibility_tiers_accepted[public]`
- `tests/runtime/test_domain_state_store_skeleton.py::TestVisibilityTiers::test_all_visibility_tiers_accepted[redacted]`
- `tests/runtime/test_domain_state_store_skeleton.py::TestVisibilityTiers::test_unsupported_visibility_tier_rejected`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_valid_creation`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_invalid_id_rejected`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_non_bool_hidden_info_safe_rejected`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_non_bool_player_visible_rejected`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_metadata_defaults_empty`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_metadata_deep_copy_safe`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_to_dict_returns_copy`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_frozen`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateVisibilityDescriptor::test_validate_accepts_valid`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_valid_creation`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_optional_ids_accept_none`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_optional_ids_reject_empty_string`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_invalid_visibility_type_rejected`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_metadata_defaults_empty`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_metadata_deep_copy_safe`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_to_dict_returns_copy`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_frozen`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateRecordRef::test_validate_accepts_valid`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateStoreService::test_service_create_record_ref`
- `tests/runtime/test_domain_state_store_skeleton.py::TestStateStoreService::test_service_validate_record_ref`
- `tests/runtime/test_domain_state_store_skeleton.py::TestValidatorParityStateStore::test_validate_record_ref_rejects_empty_schema_id`
- `tests/runtime/test_domain_state_store_skeleton.py::TestValidatorParityStateStore::test_validate_record_ref_rejects_empty_source_event_id`
- `tests/runtime/test_domain_state_store_skeleton.py::TestValidatorParityStateStore::test_validate_record_ref_accepts_all_none_optionals`

### RB-FAIL-003 — Historical pass-through amplification

- **Confidence:** reproduced
- **Full-suite nodes:** 32
- **Primary classification:** `test_infrastructure_fragility`
- **Secondary risks:** `runtime_authority`, `import_boundary`

Many later review tests execute earlier test files as subprocess or pass-through checks. Once an earlier package-surface or state-store test fails, the same root failure is counted again in several historical review layers.

These 32 nodes are not new production defects. They are an amplification mechanism that makes the full-suite failure count appear larger and couples current repository health to stale branch-specific snapshots.

Correct remediation:

1. repair the two root clusters first;
2. rerun the full suite;
3. retain pass-through tests only where they protect a current invariant not already covered by direct tests;
4. migrate repeated current-state package assertions to shared infrastructure;
5. address remaining helper and subprocess fragility under issue #128.

#### Full-suite RB-FAIL-003 nodes

- `tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py::TestExistingTestsStillPass::test_rt001b_tests_pass`
- `tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py::TestExistingTestsStillPass::test_rt001c_tests_pass`
- `tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py::TestExistingTestsStillPass::test_rt001d_tests_pass`
- `tests/test_runtime_domain_rt_001f_action_legality_service_interface_contract_hardening_review.py::TestExistingTestsStillPass::test_rt001e_tests_pass`
- `tests/test_runtime_domain_rt_001g_state_owner_interface_prerequisite_review.py::TestExistingTestsStillPass::test_rt001b_tests_pass`
- `tests/test_runtime_domain_rt_001g_state_owner_interface_prerequisite_review.py::TestExistingTestsStillPass::test_rt001c_tests_pass`
- `tests/test_runtime_domain_rt_001g_state_owner_interface_prerequisite_review.py::TestExistingTestsStillPass::test_rt001d_tests_pass`
- `tests/test_runtime_domain_rt_001g_state_owner_interface_prerequisite_review.py::TestExistingTestsStillPass::test_rt001e_tests_pass`
- `tests/test_runtime_domain_rt_001g_state_owner_interface_prerequisite_review.py::TestExistingTestsStillPass::test_rt001f_tests_pass`
- `tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py::TestExistingTestsStillPass::test_rt001b_tests_pass`
- `tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py::TestExistingTestsStillPass::test_rt001c_tests_pass`
- `tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py::TestExistingTestsStillPass::test_rt001d_tests_pass`
- `tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py::TestExistingTestsStillPass::test_rt001e_tests_pass`
- `tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py::TestExistingTestsStillPass::test_rt001f_tests_pass`
- `tests/test_runtime_domain_rt_001h_state_owner_interface_contract_skeleton.py::TestExistingTestsStillPass::test_rt001g_tests_pass`
- `tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py::TestRt001hTestsPass::test_rt001h_tests_pass`
- `tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py::TestEarlierRtTestsPass::test_rt001b_tests_pass`
- `tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py::TestEarlierRtTestsPass::test_rt001c_tests_pass`
- `tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py::TestEarlierRtTestsPass::test_rt001d_tests_pass_excluding_branch_guardrail`
- `tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py::TestEarlierRtTestsPass::test_rt001e_tests_pass`
- `tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py::TestEarlierRtTestsPass::test_rt001f_tests_pass_excluding_branch_guardrail`
- `tests/test_runtime_domain_rt_001i_state_owner_interface_contract_hardening_review.py::TestEarlierRtTestsPass::test_rt001g_tests_pass_excluding_branch_guardrail`
- `tests/test_runtime_domain_rt_002a_read_only_vertical_slice_state_owner_facade.py::TestRt001hTestsPass::test_rt001h_tests_pass`
- `tests/test_runtime_domain_rt_002a_read_only_vertical_slice_state_owner_facade.py::TestRt001iTestsPass::test_rt001i_tests_pass`
- `tests/test_runtime_domain_rt_002a_read_only_vertical_slice_state_owner_facade.py::TestPr9SeamTestsPass::test_pr9a_through_pr9e_tests_pass`
- `tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py::TestUpstreamPassThrough::test_rt002a_tests_pass`
- `tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py::TestUpstreamPassThrough::test_rt001h_tests_pass`
- `tests/test_runtime_domain_rt_002b_projection_visibility_adapter_v0_1.py::TestUpstreamPassThrough::test_rt001i_tests_pass`
- `tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py::TestUpstreamPassThrough::test_rt002b_tests_pass`
- `tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py::TestUpstreamPassThrough::test_rt002a_tests_pass`
- `tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py::TestUpstreamPassThrough::test_rt001h_tests_pass`
- `tests/test_runtime_domain_rt_002c_object_lever_interaction_legality_reader.py::TestUpstreamPassThrough::test_rt001i_tests_pass`

## Dependency declaration gap

### RB-DEBT-001 — Pytest absent from `requirements-dev.txt`

- **Classification:** `test_environment_defect`
- **Runtime failure contribution:** none after manual pytest installation
- **Observed behavior:** following the documented development install produced `ModuleNotFoundError: No module named 'pytest'`
- **Required repair:** declare pytest in the development/test dependency source and add a setup smoke check
- **Scope:** permitted in the green-baseline repair PR because it is necessary for reproducible verification

## Failure distribution

```yaml
runtime_suite:
  stale_allowlist_or_manifest: 15
  visibility_contract_namespace_collision: 32
  total: 47

full_suite:
  direct_runtime_failures: 47
  additional_direct_stale_guardrails: 15
  nested_upstream_pass_through_failures: 32
  total: 94
```

## Remediation order

### Phase 1 — Capture

Complete.

- exact baseline reproduced;
- all 47 runtime node IDs captured;
- full suite reproduced;
- all 94 full-suite node IDs classified;
- no third root cluster observed.

### Phase 2 — Repair shared package-surface infrastructure

1. centralize the exact current runtime-domain file manifest;
2. classify fixture-only and narrow-reference modules;
3. update all 15 runtime guardrails;
4. update all 15 direct top-level guardrails;
5. preserve strict undeclared-file rejection;
6. add manifest consistency and runtime-import prohibition tests.

### Phase 3 — Resolve visibility-contract ownership

1. use owner-module imports in state-store tests;
2. add explicit aliases for tests where both descriptors are needed;
3. add positive, negative, and misuse tests;
4. preserve the RT-001H policy/redaction contract;
5. do not widen either production contract solely to make imports convenient.

### Phase 4 — Reproducible test setup

1. add pytest to the development dependency declaration;
2. verify a clean Python 3.12 environment can install and collect tests;
3. document the exact commands.

### Phase 5 — Verify

Run:

```text
python -m pytest -q tests/runtime
python -m pytest -q
```

The target is:

```text
runtime: 0 unexpected failures
full: 0 unexpected failures
```

Expected failures remain permitted only when narrow, documented, and unrelated to the runtime-baseline repair.

## Gate R0 exit criteria

- [x] exact runtime failure inventory captured;
- [x] every runtime failure classified;
- [x] full-suite amplification inventory captured;
- [x] environment and dependency versions captured;
- [ ] authoritative test-only domain manifest fully adopted;
- [ ] duplicated allowlists removed or delegated;
- [ ] visibility contract ownership explicit in all affected tests;
- [ ] pytest declared by repository development dependencies;
- [ ] runtime suite has zero unexpected failures;
- [ ] full suite has zero unexpected failures;
- [ ] no guardrail weakened;
- [ ] no extraction/conversion dependency introduced into runtime;
- [ ] no RT-002G behavior implemented.

## Current PR disposition

### PR #327

This inventory is now complete enough to merge after review. It changes documentation only and freezes the exact pre-repair baseline.

### PR #328

PR #328 must not merge in its current form. It repairs the state-store import collision and introduces a shared manifest, but it updates only one of the 15 failing runtime allowlists and does not address the 15 direct top-level stale guardrails, 32 pass-through failures, or missing pytest development dependency.

PR #328 should be revised or replaced so its scope matches this reproduced inventory, then validated locally before merge.

## Next implementation PR boundary

The green-baseline repair may include only:

- the shared test-only runtime-domain manifest;
- migration of all current package-surface guardrails;
- the state-store visibility-contract import correction;
- explicit descriptor-ownership regression tests;
- pytest development dependency correction;
- before/after test evidence.

It must not include:

- AFQR-01–20 consolidation;
- Batch doctrine rewrites;
- new RT functionality;
- RT-002G;
- extraction or conversion changes;
- canon promotion;
- model-facing behavior.
