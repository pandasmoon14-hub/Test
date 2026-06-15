from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/doctrine/reviews/runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.md"
REGISTRY = ROOT / "docs/doctrine/astra_doctrine_registry_v0_1.yaml"
DECISIONS = ROOT / "docs/decisions/current_decisions_log.md"
RESOURCE_MATH_MODULE = ROOT / "src/astra_runtime/domain/resource_consequence_math.py"
ARTIFACT_ID = "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001"
AUTHORIZED_FILES = {
    "docs/decisions/current_decisions_log.md",
    "docs/doctrine/astra_doctrine_registry_v0_1.yaml",
    "src/astra_runtime/domain/__init__.py",
    "src/astra_runtime/domain/scene_command_execution_skeleton.py",
    "tests/runtime/test_command_envelope_skeleton.py",
    "tests/runtime/test_context_projection_skeleton.py",
    "tests/runtime/test_domain_event_commitment_skeleton.py",
    "tests/runtime/test_domain_state_store_skeleton.py",
    "tests/runtime/test_domain_transaction_lifecycle_skeleton.py",
    "tests/runtime/test_domain_validation_integration_skeleton.py",
    "tests/runtime/test_event_ledger_skeleton.py",
    "tests/runtime/test_hidden_information_skeleton.py",
    "tests/runtime/test_persistence_boundary_skeleton.py",
    "tests/runtime/test_replay_audit_skeleton.py",
    "tests/runtime/test_rng_interface_skeleton.py",
    "tests/runtime/test_runtime_trace_skeleton.py",
    "tests/runtime/test_state_delta_skeleton.py",
    "tests/runtime/test_table_oracle_skeleton.py",
    "tests/runtime/test_validation_pipeline_skeleton.py",
    "tests/test_runtime_domain_pr_0_domain_service_implementation_sequencing_plan.py",
    "tests/test_runtime_domain_pr_1_command_lifecycle_action_legality_service_plan.py",
    "tests/test_runtime_domain_pr_1b_command_lifecycle_action_legality_skeleton_review.py",
    "tests/test_runtime_domain_pr_2_state_store_state_projection_service_plan.py",
    "tests/test_runtime_domain_pr_2b_state_store_state_projection_skeleton_review.py",
    "tests/test_runtime_domain_pr_3_transaction_lifecycle_event_commitment_service_plan.py",
    "tests/test_runtime_domain_pr_3b_transaction_lifecycle_event_commitment_skeleton_review.py",
    "tests/test_runtime_domain_pr_4_validation_integration_invariant_enforcement_service_plan.py",
    "tests/test_runtime_domain_pr_4b_validation_integration_invariant_enforcement_skeleton_review.py",
    "tests/test_runtime_domain_pr_4d_validation_integration_invariant_enforcement_skeleton_hardening_review.py",
    "tests/test_runtime_domain_pr_4f_validation_integration_residual_hardening_review.py",
    "tests/test_runtime_domain_pr_5_resource_consequence_math_service_plan.py",
    "tests/test_runtime_domain_pr_5c_resource_consequence_math_planning_hardening_review.py",
    "tests/test_runtime_domain_pr_5e_resource_consequence_math_final_planning_hardening_review.py",
    "tests/test_runtime_domain_pr_5g_resource_consequence_math_residual_planning_hardening_review.py",
    "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py",
    "tests/test_runtime_domain_pr_9a_scene_command_execution_skeleton.py",
    "tests/test_runtime_impl_pr_8_post_kernel_skeleton_review_domain_service_readiness_gate.py",
}
EXPECTED_SHAPES = {'ConsequenceTerm': [{'aggregate_owner': 'local aggregate identity',
                      'annotation': 'str',
                      'controlled_surface': 'none',
                      'default': 'required',
                      'external_dependency_type': 'none',
                      'field': 'consequence_id',
                      'invariant': 'local aggregate identity; unique within ResourceMathRequest.consequence_terms',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'same-request internal reference',
                      'annotation': 'str',
                      'controlled_surface': 'none',
                      'default': 'required',
                      'external_dependency_type': 'none',
                      'field': 'subject_binding_id',
                      'invariant': 'same-request reference to ResourceMathRequest.subject_refs.subject_binding_id',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5D'},
                     {'aggregate_owner': 'same-request internal reference',
                      'annotation': 'str | None',
                      'controlled_surface': 'none',
                      'default': 'None',
                      'external_dependency_type': 'none',
                      'field': 'resource_ref_id',
                      'invariant': 'None or same-request reference to '
                                   'ResourceMathRequest.resource_refs.resource_ref_id, controlled by value_mode',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'same-request internal reference',
                      'annotation': 'str | None',
                      'controlled_surface': 'none',
                      'default': 'None',
                      'external_dependency_type': 'none',
                      'field': 'quantity_id',
                      'invariant': 'None or same-request reference to ResourceMathRequest.quantity_specs.quantity_id, '
                                   'controlled by value_mode',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'local field',
                      'annotation': 'str',
                      'controlled_surface': 'RESOURCE_TERM_VALUE_MODES',
                      'default': 'required',
                      'external_dependency_type': 'none',
                      'field': 'value_mode',
                      'invariant': 'non-empty string required',
                      'replacement_artifact': 'PR-5F',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5F explicit replacement/addition'},
                     {'aggregate_owner': 'local field',
                      'annotation': 'str | None',
                      'controlled_surface': 'RESOURCE_TERM_POLICY_ROUTES',
                      'default': 'None',
                      'external_dependency_type': 'none',
                      'field': 'policy_route',
                      'invariant': 'None or non-empty string; no implicit normalization',
                      'replacement_artifact': 'PR-5F',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5F explicit replacement/addition'},
                     {'aggregate_owner': 'local field',
                      'annotation': 'str',
                      'controlled_surface': 'CONSEQUENCE_FAMILIES',
                      'default': 'required',
                      'external_dependency_type': 'none',
                      'field': 'consequence_family',
                      'invariant': 'non-empty string required',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'local field',
                      'annotation': 'str',
                      'controlled_surface': 'COST_TIMING_POLICIES',
                      'default': '"blocked_pending_validation"',
                      'external_dependency_type': 'none',
                      'field': 'timing_policy',
                      'invariant': 'non-empty when required; exact annotation/default enforced',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'local field',
                      'annotation': 'str',
                      'controlled_surface': 'COST_OUTCOME_POLICIES',
                      'default': '"validation_blocked"',
                      'external_dependency_type': 'none',
                      'field': 'outcome_policy',
                      'invariant': 'non-empty when required; exact annotation/default enforced',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'local field',
                      'annotation': 'str',
                      'controlled_surface': 'VISIBILITY_POLICIES',
                      'default': '"public"',
                      'external_dependency_type': 'none',
                      'field': 'visibility_policy',
                      'invariant': 'non-empty when required; exact annotation/default enforced',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'local field',
                      'annotation': 'str',
                      'controlled_surface': 'RESOURCE_MATH_OWNER_DOMAINS',
                      'default': 'required',
                      'external_dependency_type': 'none',
                      'field': 'owner_domain',
                      'invariant': 'non-empty string required',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                               'authority',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'same-request internal reference',
                      'annotation': 'tuple[str, ...]',
                      'controlled_surface': 'none',
                      'default': '()',
                      'external_dependency_type': 'none',
                      'field': 'dependency_ids',
                      'invariant': 'tuple of same-request dependency_id references; each resolves in '
                                   'request.dependencies',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'external dependency binding',
                      'annotation': 'tuple[str, ...]',
                      'controlled_surface': 'none',
                      'default': '()',
                      'external_dependency_type': 'provenance_ref',
                      'field': 'provenance_refs',
                      'invariant': 'tuple of provenance refs; When supplied, exactly one matching required dependency '
                                   'record is required for structural validity (correct dependency_type, correct '
                                   'reference_id, unique dependency_id, unique dependency_type/reference_id pair). '
                                   'satisfied=True is complete; satisfied=False is lifecycle State B and remains '
                                   'structurally valid but incomplete; State C cases are aggregate-invalid.',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                      'source_artifact': 'PR-5B inherited'},
                     {'aggregate_owner': 'local metadata',
                      'annotation': 'Mapping[str, object]',
                      'controlled_surface': 'none',
                      'default': 'MappingProxyType({})',
                      'external_dependency_type': 'none',
                      'field': 'metadata',
                      'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                      'replacement_artifact': 'none',
                      'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType internally',
                      'source_artifact': 'PR-5B inherited'}],
 'CostBundle': [{'aggregate_owner': 'local aggregate identity',
                 'annotation': 'str',
                 'controlled_surface': 'none',
                 'default': 'required',
                 'external_dependency_type': 'none',
                 'field': 'bundle_id',
                 'invariant': 'local aggregate identity; unique within ResourceMathRequest.cost_bundles',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'same-request internal reference',
                 'annotation': 'tuple[str, ...]',
                 'controlled_surface': 'none',
                 'default': 'required',
                 'external_dependency_type': 'none',
                 'field': 'term_ids',
                 'invariant': 'required non-empty unique tuple of same-request CostTerm.term_id references',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'str',
                 'controlled_surface': 'ATOMICITY_POLICIES',
                 'default': '"all_or_nothing_requested"',
                 'external_dependency_type': 'none',
                 'field': 'atomicity_policy',
                 'invariant': 'non-empty when required; exact annotation/default enforced',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'str',
                 'controlled_surface': 'ORDERING_POLICIES',
                 'default': '"unordered_terms"',
                 'external_dependency_type': 'none',
                 'field': 'ordering_policy',
                 'invariant': 'non-empty when required; exact annotation/default enforced',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'str',
                 'controlled_surface': 'PARTIAL_SETTLEMENT_POLICIES',
                 'default': '"no_partial_settlement"',
                 'external_dependency_type': 'none',
                 'field': 'partial_settlement_policy',
                 'invariant': 'non-empty when required; exact annotation/default enforced',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'int | None',
                 'controlled_surface': 'none',
                 'default': 'None',
                 'external_dependency_type': 'none',
                 'field': 'minimum_required_terms',
                 'invariant': 'positive non-bool int when supplied; <= len(term_ids); <= maximum when maximum supplied',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'int | None',
                 'controlled_surface': 'none',
                 'default': 'None',
                 'external_dependency_type': 'none',
                 'field': 'maximum_allowed_terms',
                 'invariant': 'positive non-bool int when supplied; <= len(term_ids); >= minimum when minimum supplied',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'tuple[tuple[str, tuple[str, ...]], ...]',
                 'controlled_surface': 'none',
                 'default': '()',
                 'external_dependency_type': 'none',
                 'field': 'alternative_groups',
                 'invariant': 'unique groups; contained non-overlapping term IDs; no alternative selection in PR-5A',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'str',
                 'controlled_surface': 'VISIBILITY_POLICIES',
                 'default': '"public"',
                 'external_dependency_type': 'none',
                 'field': 'visibility_policy',
                 'invariant': 'non-empty when required; exact annotation/default enforced',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local field',
                 'annotation': 'str',
                 'controlled_surface': 'RESOURCE_MATH_OWNER_DOMAINS',
                 'default': 'required',
                 'external_dependency_type': 'none',
                 'field': 'owner_domain',
                 'invariant': 'non-empty string required',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                          'authority',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'same-request internal reference',
                 'annotation': 'tuple[str, ...]',
                 'controlled_surface': 'none',
                 'default': '()',
                 'external_dependency_type': 'none',
                 'field': 'dependency_ids',
                 'invariant': 'tuple of same-request dependency_id references; each resolves in request.dependencies',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'external dependency binding',
                 'annotation': 'tuple[str, ...]',
                 'controlled_surface': 'none',
                 'default': '()',
                 'external_dependency_type': 'provenance_ref',
                 'field': 'provenance_refs',
                 'invariant': 'tuple of provenance refs; When supplied, exactly one matching required dependency '
                              'record is required for structural validity (correct dependency_type, correct '
                              'reference_id, unique dependency_id, unique dependency_type/reference_id pair). '
                              'satisfied=True is complete; satisfied=False is lifecycle State B and remains '
                              'structurally valid but incomplete; State C cases are aggregate-invalid.',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                 'source_artifact': 'PR-5B inherited'},
                {'aggregate_owner': 'local metadata',
                 'annotation': 'Mapping[str, object]',
                 'controlled_surface': 'none',
                 'default': 'MappingProxyType({})',
                 'external_dependency_type': 'none',
                 'field': 'metadata',
                 'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                 'replacement_artifact': 'none',
                 'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType internally',
                 'source_artifact': 'PR-5B inherited'}],
 'CostTerm': [{'aggregate_owner': 'local aggregate identity',
               'annotation': 'str',
               'controlled_surface': 'none',
               'default': 'required',
               'external_dependency_type': 'none',
               'field': 'term_id',
               'invariant': 'local aggregate identity; unique within ResourceMathRequest.cost_terms',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'same-request internal reference',
               'annotation': 'str',
               'controlled_surface': 'none',
               'default': 'required',
               'external_dependency_type': 'none',
               'field': 'subject_binding_id',
               'invariant': 'same-request reference to ResourceMathRequest.subject_refs.subject_binding_id',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5D'},
              {'aggregate_owner': 'same-request internal reference',
               'annotation': 'str | None',
               'controlled_surface': 'none',
               'default': 'None',
               'external_dependency_type': 'none',
               'field': 'resource_ref_id',
               'invariant': 'None or same-request reference to ResourceMathRequest.resource_refs.resource_ref_id, '
                            'controlled by value_mode',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'same-request internal reference',
               'annotation': 'str | None',
               'controlled_surface': 'none',
               'default': 'None',
               'external_dependency_type': 'none',
               'field': 'quantity_id',
               'invariant': 'None or same-request reference to ResourceMathRequest.quantity_specs.quantity_id, '
                            'controlled by value_mode',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'local field',
               'annotation': 'str',
               'controlled_surface': 'RESOURCE_TERM_VALUE_MODES',
               'default': 'required',
               'external_dependency_type': 'none',
               'field': 'value_mode',
               'invariant': 'non-empty string required',
               'replacement_artifact': 'PR-5F',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5F explicit replacement/addition'},
              {'aggregate_owner': 'local field',
               'annotation': 'str | None',
               'controlled_surface': 'RESOURCE_TERM_POLICY_ROUTES',
               'default': 'None',
               'external_dependency_type': 'none',
               'field': 'policy_route',
               'invariant': 'None or non-empty string; no implicit normalization',
               'replacement_artifact': 'PR-5F',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5F explicit replacement/addition'},
              {'aggregate_owner': 'local field',
               'annotation': 'str',
               'controlled_surface': 'COST_FAMILIES',
               'default': 'required',
               'external_dependency_type': 'none',
               'field': 'cost_family',
               'invariant': 'non-empty string required',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'local field',
               'annotation': 'str',
               'controlled_surface': 'COST_TIMING_POLICIES',
               'default': '"blocked_pending_validation"',
               'external_dependency_type': 'none',
               'field': 'timing_policy',
               'invariant': 'non-empty when required; exact annotation/default enforced',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'local field',
               'annotation': 'str',
               'controlled_surface': 'COST_OUTCOME_POLICIES',
               'default': '"validation_blocked"',
               'external_dependency_type': 'none',
               'field': 'outcome_policy',
               'invariant': 'non-empty when required; exact annotation/default enforced',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'local field',
               'annotation': 'str',
               'controlled_surface': 'VISIBILITY_POLICIES',
               'default': '"public"',
               'external_dependency_type': 'none',
               'field': 'visibility_policy',
               'invariant': 'non-empty when required; exact annotation/default enforced',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'local field',
               'annotation': 'str',
               'controlled_surface': 'RESOURCE_MATH_OWNER_DOMAINS',
               'default': 'required',
               'external_dependency_type': 'none',
               'field': 'owner_domain',
               'invariant': 'non-empty string required',
               'replacement_artifact': 'none',
               'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection authority',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'same-request internal reference',
               'annotation': 'tuple[str, ...]',
               'controlled_surface': 'none',
               'default': '()',
               'external_dependency_type': 'none',
               'field': 'dependency_ids',
               'invariant': 'tuple of same-request dependency_id references; each resolves in request.dependencies',
               'replacement_artifact': 'none',
               'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'external dependency binding',
               'annotation': 'tuple[str, ...]',
               'controlled_surface': 'none',
               'default': '()',
               'external_dependency_type': 'provenance_ref',
               'field': 'provenance_refs',
               'invariant': 'tuple of provenance refs; When supplied, exactly one matching required dependency record '
                            'is required for structural validity (correct dependency_type, correct reference_id, '
                            'unique dependency_id, unique dependency_type/reference_id pair). satisfied=True is '
                            'complete; satisfied=False is lifecycle State B and remains structurally valid but '
                            'incomplete; State C cases are aggregate-invalid.',
               'replacement_artifact': 'none',
               'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
               'source_artifact': 'PR-5B inherited'},
              {'aggregate_owner': 'local metadata',
               'annotation': 'Mapping[str, object]',
               'controlled_surface': 'none',
               'default': 'MappingProxyType({})',
               'external_dependency_type': 'none',
               'field': 'metadata',
               'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
               'replacement_artifact': 'none',
               'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType internally',
               'source_artifact': 'PR-5B inherited'}],
 'QuantitySpecification': [{'aggregate_owner': 'local aggregate identity',
                            'annotation': 'str',
                            'controlled_surface': 'none',
                            'default': 'required',
                            'external_dependency_type': 'none',
                            'field': 'quantity_id',
                            'invariant': 'local aggregate identity; unique within ResourceMathRequest.quantity_specs',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'str',
                            'controlled_surface': 'QUANTITY_REPRESENTATION_KINDS',
                            'default': 'required',
                            'external_dependency_type': 'none',
                            'field': 'representation_kind',
                            'invariant': 'non-empty string required',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'str | None',
                            'controlled_surface': 'none',
                            'default': 'None',
                            'external_dependency_type': 'none',
                            'field': 'magnitude_text',
                            'invariant': 'None or non-empty string; no implicit normalization',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'str | None',
                            'controlled_surface': 'none',
                            'default': 'None',
                            'external_dependency_type': 'none',
                            'field': 'source_literal',
                            'invariant': 'None or non-empty string; no implicit normalization',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'int | None',
                            'controlled_surface': 'none',
                            'default': 'None',
                            'external_dependency_type': 'none',
                            'field': 'precision',
                            'invariant': 'positive non-bool int only for decimal_exact; declaration metadata only',
                            'replacement_artifact': 'PR-5F',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5F explicit replacement/addition'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'int | None',
                            'controlled_surface': 'none',
                            'default': 'None',
                            'external_dependency_type': 'none',
                            'field': 'scale',
                            'invariant': 'non-negative non-bool int only for fixed_point_scaled',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'external dependency binding',
                            'annotation': 'str | None',
                            'controlled_surface': 'none',
                            'default': 'None',
                            'external_dependency_type': 'unit_ref',
                            'field': 'unit_ref_id',
                            'invariant': 'None or non-empty unit reference; When supplied, exactly one matching '
                                         'required dependency record is required for structural validity (correct '
                                         'dependency_type, correct reference_id, unique dependency_id, unique '
                                         'dependency_type/reference_id pair). satisfied=True is complete; '
                                         'satisfied=False is lifecycle State B and remains structurally valid but '
                                         'incomplete; State C cases are aggregate-invalid.',
                            'replacement_artifact': 'PR-5F binding-contract refinement',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'external dependency binding',
                            'annotation': 'str | None',
                            'controlled_surface': 'none',
                            'default': 'None',
                            'external_dependency_type': 'dimension_ref',
                            'field': 'dimension_ref_id',
                            'invariant': 'None or non-empty dimension reference; When supplied, exactly one matching '
                                         'required dependency record is required for structural validity (correct '
                                         'dependency_type, correct reference_id, unique dependency_id, unique '
                                         'dependency_type/reference_id pair). satisfied=True is complete; '
                                         'satisfied=False is lifecycle State B and remains structurally valid but '
                                         'incomplete; State C cases are aggregate-invalid.',
                            'replacement_artifact': 'PR-5F binding-contract refinement',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'str',
                            'controlled_surface': 'CONVERSION_POLICIES',
                            'default': '"no_conversion"',
                            'external_dependency_type': 'none',
                            'field': 'conversion_policy',
                            'invariant': 'non-empty when required; exact annotation/default enforced',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'str',
                            'controlled_surface': 'ROUNDING_POLICIES',
                            'default': '"no_rounding"',
                            'external_dependency_type': 'none',
                            'field': 'rounding_policy',
                            'invariant': 'non-empty when required; exact annotation/default enforced',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'str',
                            'controlled_surface': 'QUANTITY_NEGATIVE_VALUE_POLICIES',
                            'default': '"negative_values_forbidden"',
                            'external_dependency_type': 'none',
                            'field': 'negative_value_policy',
                            'invariant': 'non-empty when required; exact annotation/default enforced',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local field',
                            'annotation': 'str',
                            'controlled_surface': 'VISIBILITY_POLICIES',
                            'default': '"public"',
                            'external_dependency_type': 'none',
                            'field': 'visibility_policy',
                            'invariant': 'non-empty when required; exact annotation/default enforced',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                     'projection authority',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'external dependency binding',
                            'annotation': 'tuple[str, ...]',
                            'controlled_surface': 'none',
                            'default': '()',
                            'external_dependency_type': 'provenance_ref',
                            'field': 'provenance_refs',
                            'invariant': 'tuple of provenance refs; When supplied, exactly one matching required '
                                         'dependency record is required for structural validity (correct '
                                         'dependency_type, correct reference_id, unique dependency_id, unique '
                                         'dependency_type/reference_id pair). satisfied=True is complete; '
                                         'satisfied=False is lifecycle State B and remains structurally valid but '
                                         'incomplete; State C cases are aggregate-invalid.',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                            'source_artifact': 'PR-5B inherited'},
                           {'aggregate_owner': 'local metadata',
                            'annotation': 'Mapping[str, object]',
                            'controlled_surface': 'none',
                            'default': 'MappingProxyType({})',
                            'external_dependency_type': 'none',
                            'field': 'metadata',
                            'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                            'replacement_artifact': 'none',
                            'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType '
                                                     'internally',
                            'source_artifact': 'PR-5B inherited'}],
 'ResourceMathDependency': [{'aggregate_owner': 'local aggregate identity',
                             'annotation': 'str',
                             'controlled_surface': 'none',
                             'default': 'required',
                             'external_dependency_type': 'none',
                             'field': 'dependency_id',
                             'invariant': 'non-empty string; unique inside its owning dependency tuple',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                      'projection authority',
                             'source_artifact': 'PR-5B inherited'},
                            {'aggregate_owner': 'local controlled field',
                             'annotation': 'str',
                             'controlled_surface': 'RESOURCE_MATH_DEPENDENCY_TYPES',
                             'default': 'required',
                             'external_dependency_type': 'none',
                             'field': 'dependency_type',
                             'invariant': 'controlled dependency type; interprets reference_id; no dereference or '
                                          'execution',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                      'projection authority',
                             'source_artifact': 'PR-5B inherited'},
                            {'aggregate_owner': 'dependency-record external reference value',
                             'annotation': 'str',
                             'controlled_surface': 'none',
                             'default': 'required',
                             'external_dependency_type': 'none',
                             'field': 'reference_id',
                             'invariant': 'typed external-reference value interpreted according to dependency_type; '
                                          'not a same-aggregate internal reference; not resolved against '
                                          'subject/resource/quantity/term/bundle/consequence IDs unless that '
                                          'dependency type expressly represents such a reference; does not require a '
                                          'second dependency record',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                      'projection authority',
                             'source_artifact': 'PR-5B inherited'},
                            {'aggregate_owner': 'local controlled field',
                             'annotation': 'str',
                             'controlled_surface': 'RESOURCE_MATH_OWNER_DOMAINS',
                             'default': 'required',
                             'external_dependency_type': 'none',
                             'field': 'owner_domain',
                             'invariant': 'controlled owner domain for the dependency record',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                      'projection authority',
                             'source_artifact': 'PR-5B inherited'},
                            {'aggregate_owner': 'local lifecycle flag',
                             'annotation': 'bool',
                             'controlled_surface': 'none',
                             'default': 'True',
                             'external_dependency_type': 'none',
                             'field': 'required',
                             'invariant': 'bool; controls whether the dependency is mandatory; required=False cannot '
                                          'satisfy required bindings and participates in lifecycle State C or E as '
                                          'specified',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                      'projection authority',
                             'source_artifact': 'PR-5B inherited'},
                            {'aggregate_owner': 'local lifecycle flag',
                             'annotation': 'bool',
                             'controlled_surface': 'none',
                             'default': 'False',
                             'external_dependency_type': 'none',
                             'field': 'satisfied',
                             'invariant': 'bool; participates in lifecycle states A-E; required=True and '
                                          'satisfied=False is incomplete or required-unsatisfied, not malformed by '
                                          'itself',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                      'projection authority',
                             'source_artifact': 'PR-5B inherited'},
                            {'aggregate_owner': 'local hidden-information flag',
                             'annotation': 'bool',
                             'controlled_surface': 'none',
                             'default': 'True',
                             'external_dependency_type': 'none',
                             'field': 'hidden_info_safe',
                             'invariant': 'bool; False is distinct from unsatisfied; dependency-derived '
                                          'blocked_hidden_information requires the same dependency record to be '
                                          'otherwise complete (required=True and satisfied=True); required=True and '
                                          'satisfied=False with hidden_info_safe=False remains State B or State D '
                                          'missing-dependency for that same record with hidden risk retained in '
                                          'diagnostics and does not replace blocked_missing_dependency',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                      'projection authority',
                             'source_artifact': 'PR-5B inherited'},
                            {'aggregate_owner': 'local metadata',
                             'annotation': 'Mapping[str, object]',
                             'controlled_surface': 'none',
                             'default': 'MappingProxyType({})',
                             'external_dependency_type': 'none',
                             'field': 'metadata',
                             'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                             'replacement_artifact': 'none',
                             'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType '
                                                      'internally',
                             'source_artifact': 'PR-5B inherited'}],
 'ResourceMathRequest': [{'aggregate_owner': 'local aggregate identity',
                          'annotation': 'str',
                          'controlled_surface': 'none',
                          'default': 'required',
                          'external_dependency_type': 'none',
                          'field': 'request_id',
                          'invariant': 'local aggregate identity; identifies this ResourceMathRequest',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'external dependency binding',
                          'annotation': 'str | None',
                          'controlled_surface': 'none',
                          'default': 'None',
                          'external_dependency_type': 'command_ref',
                          'field': 'command_ref_id',
                          'invariant': 'None or non-empty command reference; When supplied, exactly one matching '
                                       'required dependency record is required for structural validity (correct '
                                       'dependency_type, correct reference_id, unique dependency_id, unique '
                                       'dependency_type/reference_id pair). satisfied=True is complete; '
                                       'satisfied=False is lifecycle State B and remains structurally valid but '
                                       'incomplete; State C cases are aggregate-invalid.',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'external dependency binding',
                          'annotation': 'str | None',
                          'controlled_surface': 'none',
                          'default': 'None',
                          'external_dependency_type': 'action_legality_ref',
                          'field': 'action_legality_ref_id',
                          'invariant': 'None or non-empty action-legality reference; When supplied, exactly one '
                                       'matching required dependency record is required for structural validity '
                                       '(correct dependency_type, correct reference_id, unique dependency_id, unique '
                                       'dependency_type/reference_id pair). satisfied=True is complete; '
                                       'satisfied=False is lifecycle State B and remains structurally valid but '
                                       'incomplete; State C cases are aggregate-invalid.',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'same-aggregate member collection',
                          'annotation': 'tuple[ResourceMathSubjectReference, ...]',
                          'controlled_surface': 'none',
                          'default': 'required',
                          'external_dependency_type': 'none',
                          'field': 'subject_refs',
                          'invariant': 'non-empty tuple; exactly one primary_subject; subject_binding_id values unique '
                                       'in request',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                          'source_artifact': 'PR-5D'},
                         {'aggregate_owner': 'external dependency binding',
                          'annotation': 'tuple[str, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'state_projection_ref',
                          'field': 'state_projection_ref_ids',
                          'invariant': 'tuple of state projection refs; When supplied, exactly one matching required '
                                       'dependency record is required for structural validity (correct '
                                       'dependency_type, correct reference_id, unique dependency_id, unique '
                                       'dependency_type/reference_id pair). satisfied=True is complete; '
                                       'satisfied=False is lifecycle State B and remains structurally valid but '
                                       'incomplete; State C cases are aggregate-invalid.',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'same-aggregate member collection',
                          'annotation': 'tuple[ResourceReference, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'none',
                          'field': 'resource_refs',
                          'invariant': 'tuple of ResourceReference records; resource_ref_id values unique; each '
                                       'subject_binding_id resolves in subject_refs',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'same-aggregate member collection',
                          'annotation': 'tuple[QuantitySpecification, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'none',
                          'field': 'quantity_specs',
                          'invariant': 'tuple of QuantitySpecification records; quantity_id values unique; '
                                       'lexical-only validation applies',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'same-aggregate member collection',
                          'annotation': 'tuple[CostTerm, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'none',
                          'field': 'cost_terms',
                          'invariant': 'tuple of CostTerm records; term_id values unique; internal references resolve '
                                       'in the same request',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'same-aggregate member collection',
                          'annotation': 'tuple[CostBundle, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'none',
                          'field': 'cost_bundles',
                          'invariant': 'tuple of CostBundle records; bundle_id values unique; CostBundle matrix and '
                                       'bound rules apply',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'same-aggregate member collection',
                          'annotation': 'tuple[ConsequenceTerm, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'none',
                          'field': 'consequence_terms',
                          'invariant': 'tuple of ConsequenceTerm records; consequence_id values unique; no consequence '
                                       'application',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'owned dependency tuple',
                          'annotation': 'tuple[ResourceMathDependency, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'none',
                          'field': 'dependencies',
                          'invariant': 'owns request/input external bindings; dependency_id and (dependency_type, '
                                       'reference_id) unique; lifecycle states A-E apply',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'external dependency binding',
                          'annotation': 'str',
                          'controlled_surface': 'none',
                          'default': 'required',
                          'external_dependency_type': 'runtime_trace_ref',
                          'field': 'trace_ref_id',
                          'invariant': 'required runtime trace reference; Exactly one matching required dependency '
                                       'record is required for structural validity (correct dependency_type, correct '
                                       'reference_id, unique dependency_id, unique dependency_type/reference_id pair). '
                                       'satisfied=True is complete; satisfied=False is lifecycle State B and remains '
                                       'structurally valid but incomplete; State C cases are aggregate-invalid.',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'external dependency binding',
                          'annotation': 'tuple[str, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'provenance_ref',
                          'field': 'provenance_refs',
                          'invariant': 'tuple of provenance refs; When supplied, exactly one matching required '
                                       'dependency record is required for structural validity (correct '
                                       'dependency_type, correct reference_id, unique dependency_id, unique '
                                       'dependency_type/reference_id pair). satisfied=True is complete; '
                                       'satisfied=False is lifecycle State B and remains structurally valid but '
                                       'incomplete; State C cases are aggregate-invalid.',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'external dependency binding',
                          'annotation': 'tuple[str, ...]',
                          'controlled_surface': 'none',
                          'default': '()',
                          'external_dependency_type': 'owner_handoff_ref',
                          'field': 'owner_handoff_ref_ids',
                          'invariant': 'tuple of owner handoff refs; When supplied, exactly one matching required '
                                       'dependency record is required for structural validity (correct '
                                       'dependency_type, correct reference_id, unique dependency_id, unique '
                                       'dependency_type/reference_id pair). satisfied=True is complete; '
                                       'satisfied=False is lifecycle State B and remains structurally valid but '
                                       'incomplete; State C cases are aggregate-invalid.',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'external dependency binding',
                          'annotation': 'str | None',
                          'controlled_surface': 'none',
                          'default': 'None',
                          'external_dependency_type': 'validation_request_ref',
                          'field': 'validation_request_ref_id',
                          'invariant': 'None or non-empty validation request ref; When supplied, exactly one matching '
                                       'required dependency record is required for structural validity (correct '
                                       'dependency_type, correct reference_id, unique dependency_id, unique '
                                       'dependency_type/reference_id pair). satisfied=True is complete; '
                                       'satisfied=False is lifecycle State B and remains structurally valid but '
                                       'incomplete; State C cases are aggregate-invalid.',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                   'authority',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'local metadata',
                          'annotation': 'Mapping[str, object]',
                          'controlled_surface': 'none',
                          'default': 'MappingProxyType({})',
                          'external_dependency_type': 'none',
                          'field': 'metadata',
                          'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType '
                                                   'internally',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'calculation_executed',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'affordability_executed',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'reservation_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'settlement_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'consequence_application_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'mutation_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'state_delta_application_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'transaction_execution_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'event_commitment_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'event_append_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'persistence_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'replay_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'rng_execution_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'table_oracle_execution_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'model_authority_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'live_play_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'ui_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'conversion_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'},
                         {'aggregate_owner': 'aggregate false-only authority',
                          'annotation': 'bool',
                          'controlled_surface': 'none',
                          'default': 'False',
                          'external_dependency_type': 'none',
                          'field': 'canon_promotion_authorized',
                          'invariant': 'false-only authority field; factories and validators reject True including '
                                       'manual frozen dataclasses',
                          'replacement_artifact': 'none',
                          'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                          'source_artifact': 'PR-5B inherited'}],
 'ResourceMathResult': [{'aggregate_owner': 'local aggregate identity',
                         'annotation': 'str',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'none',
                         'field': 'result_id',
                         'invariant': 'local aggregate identity; identifies this ResourceMathResult; no '
                                      'resource_math_result_ref self-binding',
                         'replacement_artifact': 'PR-5H no-self-binding correction',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'str',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'resource_math_request_ref',
                         'field': 'request_id',
                         'invariant': 'non-empty; binds the exact supplied ResourceMathRequest; Exactly one matching '
                                      'required dependency record is required for structural validity. satisfied=True '
                                      'is required for accepted_for_planning or normalized_for_planning; required=True '
                                      'and satisfied=False is lifecycle State D and is lawful only on '
                                      'blocked_missing_dependency results that scope or reach that dependency; '
                                      'missing, malformed, optional, or duplicated binding records are structurally '
                                      'invalid.',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'str',
                         'controlled_surface': 'RESOURCE_MATH_STAGES',
                         'default': 'required',
                         'external_dependency_type': 'none',
                         'field': 'stage',
                         'invariant': 'non-empty string required',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'str',
                         'controlled_surface': 'RESOURCE_MATH_DECISIONS',
                         'default': 'required',
                         'external_dependency_type': 'none',
                         'field': 'decision',
                         'invariant': 'non-empty string required',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'none',
                         'field': 'blocking',
                         'invariant': 'bool required; exact value determined by stage/decision compatibility and '
                                      'blocker precedence',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'quarantined',
                         'invariant': 'bool default False; True only for the lawful quarantined_for_review '
                                      'stage/decision pair',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'escalated',
                         'invariant': 'bool default False; True only for the lawful escalated_to_doctrine '
                                      'stage/decision pair',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local diagnostic text',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'diagnostics',
                         'invariant': 'tuple[str, ...]; diagnostics are not internal reference IDs; preserve supplied '
                                      'ordering; require non-empty strings if supplied; retain all detected blocker '
                                      'diagnostics; no same-request ID resolution',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict; no public '
                                                  'projection authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local diagnostic references',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'normalized_reference_ids',
                         'invariant': 'diagnostic-only tuple; never determines policy scope; no same-request '
                                      'resolution requirement for result policy enforcement',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'same-request internal reference',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'referenced_subject_binding_ids',
                         'invariant': 'tuple of same-request subject_binding_id references; unique non-empty IDs; '
                                      'resolves in supplied request',
                         'replacement_artifact': 'PR-5F',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5F explicit replacement/addition'},
                        {'aggregate_owner': 'same-request internal reference',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'referenced_resource_ref_ids',
                         'invariant': 'tuple of same-request resource_ref_id references; unique non-empty IDs; '
                                      'resolves in supplied request',
                         'replacement_artifact': 'PR-5F',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5F explicit replacement/addition'},
                        {'aggregate_owner': 'same-request internal reference',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'referenced_quantity_ids',
                         'invariant': 'tuple of same-request quantity_id references; unique non-empty IDs; resolves in '
                                      'supplied request',
                         'replacement_artifact': 'PR-5F',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5F explicit replacement/addition'},
                        {'aggregate_owner': 'same-request internal reference',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'referenced_cost_term_ids',
                         'invariant': 'tuple of same-request CostTerm.term_id references; unique non-empty IDs; '
                                      'resolves in supplied request',
                         'replacement_artifact': 'PR-5F',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5F explicit replacement/addition'},
                        {'aggregate_owner': 'same-request internal reference',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'referenced_cost_bundle_ids',
                         'invariant': 'tuple of same-request CostBundle.bundle_id references; unique non-empty IDs; '
                                      'resolves in supplied request',
                         'replacement_artifact': 'PR-5F',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5F explicit replacement/addition'},
                        {'aggregate_owner': 'same-request internal reference',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'referenced_consequence_term_ids',
                         'invariant': 'tuple of same-request ConsequenceTerm.consequence_id references; unique '
                                      'non-empty IDs; resolves in supplied request',
                         'replacement_artifact': 'PR-5F',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5F explicit replacement/addition'},
                        {'aggregate_owner': 'same-request internal reference',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'referenced_dependency_ids',
                         'invariant': 'tuple of same-request ResourceMathDependency.dependency_id references; unique '
                                      'non-empty IDs; resolves in supplied request; satisfied=True is required for '
                                      'accepted/normalized results; required=True satisfied=False is lifecycle State D '
                                      'and forces blocked_missing_dependency when reached; State C '
                                      'missing/malformed/optional/duplicate records are invalid',
                         'replacement_artifact': 'PR-5F',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5F explicit replacement/addition'},
                        {'aggregate_owner': 'owned dependency tuple',
                         'annotation': 'tuple[ResourceMathDependency, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'dependencies',
                         'invariant': 'owns request binding, result validation, trace, and result-specific references; '
                                      'no resource_math_result_ref self-binding; accepted/normalized results require '
                                      'all reached required dependencies satisfied; required unsatisfied reached '
                                      'dependencies are State D and lawful only for blocked_missing_dependency results',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'str',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'runtime_trace_ref',
                         'field': 'trace_ref_id',
                         'invariant': 'required runtime trace reference; Exactly one matching required dependency '
                                      'record is required for structural validity. satisfied=True is required for '
                                      'accepted_for_planning or normalized_for_planning; required=True and '
                                      'satisfied=False is lifecycle State D and is lawful only on '
                                      'blocked_missing_dependency results that scope or reach that dependency; '
                                      'missing, malformed, optional, or duplicated binding records are structurally '
                                      'invalid.',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'str | None',
                         'controlled_surface': 'none',
                         'default': 'None',
                         'external_dependency_type': 'validation_request_ref',
                         'field': 'validation_request_ref_id',
                         'invariant': 'None or non-empty validation request ref; validation co-presence rules apply; '
                                      'When supplied, exactly one matching required dependency record is required for '
                                      'structural validity. satisfied=True is required for accepted_for_planning or '
                                      'normalized_for_planning; required=True and satisfied=False is lifecycle State D '
                                      'and is lawful only on blocked_missing_dependency results that scope or reach '
                                      'that dependency; missing, malformed, optional, or duplicated binding records '
                                      'are structurally invalid.',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'str | None',
                         'controlled_surface': 'none',
                         'default': 'None',
                         'external_dependency_type': 'validation_result_ref',
                         'field': 'validation_result_ref_id',
                         'invariant': 'None or non-empty validation result ref; validation co-presence rules and '
                                      'proposal equality apply; When supplied, exactly one matching required '
                                      'dependency record is required for structural validity. satisfied=True is '
                                      'required for accepted_for_planning or normalized_for_planning; required=True '
                                      'and satisfied=False is lifecycle State D and is lawful only on '
                                      'blocked_missing_dependency results that scope or reach that dependency; '
                                      'missing, malformed, optional, or duplicated binding records are structurally '
                                      'invalid.',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'str | None',
                         'controlled_surface': 'VALIDATION_INTEGRATION_DECISIONS',
                         'default': 'None',
                         'external_dependency_type': 'none',
                         'field': 'validation_decision',
                         'invariant': 'validation decision belongs to VALIDATION_INTEGRATION_DECISIONS; co-presence '
                                      'rules apply; proposal requires validation_passed and equality with result',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local metadata',
                         'annotation': 'Mapping[str, object]',
                         'controlled_surface': 'none',
                         'default': 'MappingProxyType({})',
                         'external_dependency_type': 'none',
                         'field': 'metadata',
                         'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType '
                                                  'internally',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'calculation_executed',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'affordability_executed',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'reservation_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'settlement_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'consequence_application_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'mutation_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'state_delta_application_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'transaction_execution_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'event_commitment_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'event_append_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'persistence_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'replay_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'rng_execution_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'table_oracle_execution_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'model_authority_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'live_play_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'ui_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'conversion_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'canon_promotion_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'}],
 'ResourceMathSubjectReference': [{'aggregate_owner': 'local aggregate identity',
                                   'annotation': 'str',
                                   'controlled_surface': 'none',
                                   'default': 'required',
                                   'external_dependency_type': 'none',
                                   'field': 'subject_binding_id',
                                   'invariant': 'local aggregate identity; unique within '
                                                'ResourceMathRequest.subject_refs',
                                   'replacement_artifact': 'none',
                                   'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                            'projection authority',
                                   'source_artifact': 'PR-5D'},
                                  {'aggregate_owner': 'local field',
                                   'annotation': 'str',
                                   'controlled_surface': 'RESOURCE_MATH_SUBJECT_TYPES',
                                   'default': 'required',
                                   'external_dependency_type': 'none',
                                   'field': 'subject_type',
                                   'invariant': 'non-empty string required',
                                   'replacement_artifact': 'none',
                                   'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                            'projection authority',
                                   'source_artifact': 'PR-5D'},
                                  {'aggregate_owner': 'external dependency binding',
                                   'annotation': 'str',
                                   'controlled_surface': 'none',
                                   'default': 'required',
                                   'external_dependency_type': 'subject_ref',
                                   'field': 'subject_ref_id',
                                   'invariant': 'non-empty external/upstream subject reference; Exactly one matching '
                                                'required dependency record is required for structural validity '
                                                '(correct dependency_type, correct reference_id, unique dependency_id, '
                                                'unique dependency_type/reference_id pair). satisfied=True is '
                                                'complete; satisfied=False is lifecycle State B and remains '
                                                'structurally valid but incomplete; State C cases are '
                                                'aggregate-invalid.',
                                   'replacement_artifact': 'PR-5F binding-contract refinement',
                                   'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                            'projection authority',
                                   'source_artifact': 'PR-5D'},
                                  {'aggregate_owner': 'local field',
                                   'annotation': 'str',
                                   'controlled_surface': 'RESOURCE_MATH_SUBJECT_ROLES',
                                   'default': 'required',
                                   'external_dependency_type': 'none',
                                   'field': 'subject_role',
                                   'invariant': 'non-empty string required',
                                   'replacement_artifact': 'none',
                                   'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                            'projection authority',
                                   'source_artifact': 'PR-5D'},
                                  {'aggregate_owner': 'local field',
                                   'annotation': 'str',
                                   'controlled_surface': 'RESOURCE_MATH_OWNER_DOMAINS',
                                   'default': 'required',
                                   'external_dependency_type': 'none',
                                   'field': 'owner_domain',
                                   'invariant': 'non-empty string required',
                                   'replacement_artifact': 'none',
                                   'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                            'projection authority',
                                   'source_artifact': 'PR-5D'},
                                  {'aggregate_owner': 'local field',
                                   'annotation': 'str',
                                   'controlled_surface': 'VISIBILITY_POLICIES',
                                   'default': '"public"',
                                   'external_dependency_type': 'none',
                                   'field': 'visibility_policy',
                                   'invariant': 'non-empty when required; exact annotation/default enforced',
                                   'replacement_artifact': 'none',
                                   'serialization_posture': 'internal to_dict only; defensive scalar copy; no public '
                                                            'projection authority',
                                   'source_artifact': 'PR-5D'},
                                  {'aggregate_owner': 'external dependency binding',
                                   'annotation': 'tuple[str, ...]',
                                   'controlled_surface': 'none',
                                   'default': '()',
                                   'external_dependency_type': 'provenance_ref',
                                   'field': 'provenance_refs',
                                   'invariant': 'tuple of provenance refs; When supplied, exactly one matching '
                                                'required dependency record is required for structural validity '
                                                '(correct dependency_type, correct reference_id, unique dependency_id, '
                                                'unique dependency_type/reference_id pair). satisfied=True is '
                                                'complete; satisfied=False is lifecycle State B and remains '
                                                'structurally valid but incomplete; State C cases are '
                                                'aggregate-invalid.',
                                   'replacement_artifact': 'none',
                                   'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                                   'source_artifact': 'PR-5D'},
                                  {'aggregate_owner': 'local metadata',
                                   'annotation': 'Mapping[str, object]',
                                   'controlled_surface': 'none',
                                   'default': 'MappingProxyType({})',
                                   'external_dependency_type': 'none',
                                   'field': 'metadata',
                                   'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no '
                                                'callables',
                                   'replacement_artifact': 'none',
                                   'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType '
                                                            'internally',
                                   'source_artifact': 'PR-5D'}],
 'ResourceReference': [{'aggregate_owner': 'local aggregate identity',
                        'annotation': 'str',
                        'controlled_surface': 'none',
                        'default': 'required',
                        'external_dependency_type': 'none',
                        'field': 'resource_ref_id',
                        'invariant': 'local aggregate identity; unique within ResourceMathRequest.resource_refs',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'same-request internal reference',
                        'annotation': 'str',
                        'controlled_surface': 'none',
                        'default': 'required',
                        'external_dependency_type': 'none',
                        'field': 'subject_binding_id',
                        'invariant': 'same-request reference to ResourceMathRequest.subject_refs.subject_binding_id',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5D'},
                       {'aggregate_owner': 'local field',
                        'annotation': 'str',
                        'controlled_surface': 'RESOURCE_FAMILIES',
                        'default': 'required',
                        'external_dependency_type': 'none',
                        'field': 'resource_family',
                        'invariant': 'non-empty string required',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'local field',
                        'annotation': 'str',
                        'controlled_surface': 'none',
                        'default': 'required',
                        'external_dependency_type': 'none',
                        'field': 'resource_key',
                        'invariant': 'non-empty string required',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'local field',
                        'annotation': 'str | None',
                        'controlled_surface': 'none',
                        'default': 'None',
                        'external_dependency_type': 'none',
                        'field': 'source_label',
                        'invariant': 'None or non-empty string; no implicit normalization',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'local source-label tuple',
                        'annotation': 'tuple[str, ...]',
                        'controlled_surface': 'none',
                        'default': '()',
                        'external_dependency_type': 'none',
                        'field': 'source_aliases',
                        'invariant': 'tuple[str, ...]; aliases are source labels, not reference IDs; require non-empty '
                                     'strings if supplied; duplicates rejected only if an inherited alias contract '
                                     'explicitly requires it; no ID resolution',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'tuple copied internally; copied list in internal to_dict; no public '
                                                 'projection authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'local field',
                        'annotation': 'str',
                        'controlled_surface': 'RESOURCE_MATH_OWNER_DOMAINS',
                        'default': 'required',
                        'external_dependency_type': 'none',
                        'field': 'owner_domain',
                        'invariant': 'non-empty string required',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'local field',
                        'annotation': 'str',
                        'controlled_surface': 'VISIBILITY_POLICIES',
                        'default': '"public"',
                        'external_dependency_type': 'none',
                        'field': 'visibility_policy',
                        'invariant': 'non-empty when required; exact annotation/default enforced',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'external dependency binding',
                        'annotation': 'str | None',
                        'controlled_surface': 'none',
                        'default': 'None',
                        'external_dependency_type': 'unit_ref',
                        'field': 'unit_ref_id',
                        'invariant': 'None or non-empty unit reference; When supplied, exactly one matching required '
                                     'dependency record is required for structural validity (correct dependency_type, '
                                     'correct reference_id, unique dependency_id, unique dependency_type/reference_id '
                                     'pair). satisfied=True is complete; satisfied=False is lifecycle State B and '
                                     'remains structurally valid but incomplete; State C cases are aggregate-invalid.',
                        'replacement_artifact': 'PR-5F binding-contract refinement',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'external dependency binding',
                        'annotation': 'str | None',
                        'controlled_surface': 'none',
                        'default': 'None',
                        'external_dependency_type': 'dimension_ref',
                        'field': 'dimension_ref_id',
                        'invariant': 'None or non-empty dimension reference; When supplied, exactly one matching '
                                     'required dependency record is required for structural validity (correct '
                                     'dependency_type, correct reference_id, unique dependency_id, unique '
                                     'dependency_type/reference_id pair). satisfied=True is complete; satisfied=False '
                                     'is lifecycle State B and remains structurally valid but incomplete; State C '
                                     'cases are aggregate-invalid.',
                        'replacement_artifact': 'PR-5F binding-contract refinement',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'external dependency binding',
                        'annotation': 'tuple[str, ...]',
                        'controlled_surface': 'none',
                        'default': '()',
                        'external_dependency_type': 'provenance_ref',
                        'field': 'provenance_refs',
                        'invariant': 'tuple of provenance refs; When supplied, exactly one matching required '
                                     'dependency record is required for structural validity (correct dependency_type, '
                                     'correct reference_id, unique dependency_id, unique dependency_type/reference_id '
                                     'pair). satisfied=True is complete; satisfied=False is lifecycle State B and '
                                     'remains structurally valid but incomplete; State C cases are aggregate-invalid.',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'local field',
                        'annotation': 'bool',
                        'controlled_surface': 'none',
                        'default': 'False',
                        'external_dependency_type': 'none',
                        'field': 'source_local',
                        'invariant': 'boolean value; bool-specific validation, not a string/non-empty check',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                 'authority',
                        'source_artifact': 'PR-5B inherited'},
                       {'aggregate_owner': 'local metadata',
                        'annotation': 'Mapping[str, object]',
                        'controlled_surface': 'none',
                        'default': 'MappingProxyType({})',
                        'external_dependency_type': 'none',
                        'field': 'metadata',
                        'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                        'replacement_artifact': 'none',
                        'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType internally',
                        'source_artifact': 'PR-5B inherited'}],
 'SettlementProposal': [{'aggregate_owner': 'local aggregate identity',
                         'annotation': 'str',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'none',
                         'field': 'proposal_id',
                         'invariant': 'local aggregate identity; identifies this SettlementProposal',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'str',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'resource_math_result_ref',
                         'field': 'result_id',
                         'invariant': 'non-empty; binds the exact supplied ResourceMathResult; Exactly one matching '
                                      'required/satisfied dependency record is required; no incomplete dependency may '
                                      'enter a SettlementProposal.',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'state_delta_ref',
                         'field': 'proposed_state_delta_refs',
                         'invariant': 'required non-empty unique tuple of proposed state-delta refs; Exactly one '
                                      'matching required/satisfied dependency record is required; no incomplete '
                                      'dependency may enter a SettlementProposal.',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'str',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'validation_result_ref',
                         'field': 'validation_result_ref_id',
                         'invariant': 'non-empty validation result ref equal to supplied '
                                      'result.validation_result_ref_id; Exactly one matching required/satisfied '
                                      'dependency record is required; no incomplete dependency may enter a '
                                      'SettlementProposal.',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'str',
                         'controlled_surface': 'VALIDATION_INTEGRATION_DECISIONS',
                         'default': 'required',
                         'external_dependency_type': 'none',
                         'field': 'validation_decision',
                         'invariant': 'validation decision belongs to VALIDATION_INTEGRATION_DECISIONS; co-presence '
                                      'rules apply; proposal requires validation_passed and equality with result',
                         'replacement_artifact': 'PR-5F aggregate-validation refinement; PR-5H direct '
                                                 'request/result/proposal validation refinement',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'owned dependency tuple',
                         'annotation': 'tuple[ResourceMathDependency, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'none',
                         'field': 'dependencies',
                         'invariant': 'owns result binding, validation result, state deltas, trace, rollback '
                                      'accounting, and proposal-specific references; every required proposal '
                                      'dependency must be satisfied; incomplete dependencies are forbidden',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'str',
                         'controlled_surface': 'none',
                         'default': 'required',
                         'external_dependency_type': 'runtime_trace_ref',
                         'field': 'trace_ref_id',
                         'invariant': 'required runtime trace reference; Exactly one matching required/satisfied '
                                      'dependency record is required; no incomplete dependency may enter a '
                                      'SettlementProposal.',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local field',
                         'annotation': 'str',
                         'controlled_surface': 'VISIBILITY_POLICIES',
                         'default': '"public"',
                         'external_dependency_type': 'none',
                         'field': 'visibility_policy',
                         'invariant': 'non-empty when required; exact annotation/default enforced',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; defensive scalar copy; no public projection '
                                                  'authority',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'external dependency binding',
                         'annotation': 'tuple[str, ...]',
                         'controlled_surface': 'none',
                         'default': '()',
                         'external_dependency_type': 'rollback_accounting_ref',
                         'field': 'rollback_accounting_refs',
                         'invariant': 'tuple of rollback accounting refs when supplied; Exactly one matching '
                                      'required/satisfied dependency record is required; no incomplete dependency may '
                                      'enter a SettlementProposal.',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'tuple copied internally; copied list in internal to_dict',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'local metadata',
                         'annotation': 'Mapping[str, object]',
                         'controlled_surface': 'none',
                         'default': 'MappingProxyType({})',
                         'external_dependency_type': 'none',
                         'field': 'metadata',
                         'invariant': 'immutable defensive metadata only; copied to MappingProxyType; no callables',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'defensive dict copy in internal to_dict; MappingProxyType '
                                                  'internally',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'calculation_executed',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'affordability_executed',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'reservation_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'settlement_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'consequence_application_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'mutation_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'state_delta_application_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'transaction_execution_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'event_commitment_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'event_append_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'persistence_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'replay_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'rng_execution_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'table_oracle_execution_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'model_authority_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'live_play_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'ui_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'conversion_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'},
                        {'aggregate_owner': 'aggregate false-only authority',
                         'annotation': 'bool',
                         'controlled_surface': 'none',
                         'default': 'False',
                         'external_dependency_type': 'none',
                         'field': 'canon_promotion_authorized',
                         'invariant': 'false-only authority field; factories and validators reject True including '
                                      'manual frozen dataclasses',
                         'replacement_artifact': 'none',
                         'serialization_posture': 'internal to_dict only; preserved false; no public projection',
                         'source_artifact': 'PR-5B inherited'}]}
EXPECTED_CONSTANTS = {'ATOMICITY_POLICIES': ['all_or_nothing_requested',
                        'best_effort_requested',
                        'ordered_partial_allowed',
                        'unordered_partial_allowed',
                        'alternative_exactly_one',
                        'alternative_at_least_one',
                        'alternative_at_most_one',
                        'alternative_any',
                        'invalid_mixed_atomicity',
                        'blocked_pending_transaction_policy'],
 'CONSEQUENCE_FAMILIES': ['gain',
                          'loss',
                          'transfer',
                          'lock',
                          'unlock',
                          'exposure',
                          'exhaustion',
                          'degradation',
                          'escalation',
                          'cooldown',
                          'debt',
                          'obligation',
                          'harm_pressure',
                          'recovery_pressure',
                          'visibility_change',
                          'mission_route',
                          'clue_route',
                          'social_faction_change',
                          'inventory_asset_change',
                          'provenance_recurrence',
                          'quarantine_escalation'],
 'CONVERSION_POLICIES': ['no_conversion',
                         'exact_conversion',
                         'table_driven_conversion',
                         'doctrine_approved_conversion',
                         'source_local_conversion',
                         'escalation_required'],
 'COST_FAMILIES': ['activation',
                   'upkeep',
                   'maintenance',
                   'opportunity',
                   'prerequisite_lock',
                   'reservation_hold',
                   'partial_payment',
                   'substitution',
                   'overcommitment',
                   'debt_creation',
                   'success_at_cost',
                   'failure_at_cost',
                   'cancellation',
                   'interruption',
                   'refund',
                   'reversal',
                   'compensation',
                   'repair',
                   'recovery',
                   'crafting',
                   'salvage',
                   'requisition',
                   'validation_blocked'],
 'COST_OUTCOME_POLICIES': ['success',
                           'failure',
                           'partial_success',
                           'cancelled',
                           'interrupted',
                           'invalid',
                           'validation_blocked',
                           'owner_blocked',
                           'quarantined',
                           'escalated',
                           'rollback_required'],
 'COST_TIMING_POLICIES': ['pay_before_resolution',
                          'reserve_before_resolution',
                          'pay_on_attempt',
                          'pay_on_success',
                          'pay_on_failure',
                          'pay_on_commitment',
                          'pay_over_time',
                          'upkeep_interval',
                          'refund_on_cancel',
                          'no_refund_on_interrupt',
                          'compensate_after_rollback',
                          'blocked_pending_validation'],
 'DECLARATION_PROGRESS_STAGES': ['source_declaration_captured',
                                 'subject_refs_bound',
                                 'resource_refs_declared',
                                 'quantity_specs_declared',
                                 'terms_declared',
                                 'bundle_structure_declared',
                                 'policy_refs_declared',
                                 'dependency_refs_bound',
                                 'calculation_ready_for_review'],
 'ESCALATION_STAGES': ['escalated_to_doctrine'],
 'HIDDEN_INFORMATION_BLOCK_STAGES': ['dependency_refs_bound', 'blocked_pending_validation'],
 'MISSING_DEPENDENCY_STAGES': ['dependency_refs_bound', 'blocked_pending_validation', 'blocked_pending_owner_handoff'],
 'ORDERING_POLICIES': ['unordered_terms',
                       'source_ordered_terms',
                       'dependency_ordered_terms',
                       'priority_ordered_terms',
                       'blocked_pending_ordering_policy'],
 'OWNER_HANDOFF_STAGES': ['blocked_pending_owner_handoff'],
 'PARTIAL_SETTLEMENT_POLICIES': ['no_partial_settlement',
                                 'partial_settlement_allowed',
                                 'partial_settlement_requires_owner_review',
                                 'partial_settlement_requires_validation',
                                 'blocked_pending_settlement_policy'],
 'POLICY_BLOCK_STAGES': ['policy_refs_declared'],
 'QUANTITY_KINDS': ['count',
                    'pool_amount',
                    'delta',
                    'ratio',
                    'percentage',
                    'duration',
                    'interval',
                    'threshold',
                    'capacity',
                    'rank',
                    'tier',
                    'charge_count',
                    'currency_amount',
                    'material_amount',
                    'durability_amount',
                    'debt_amount',
                    'source_literal_quantity',
                    'unknown_pending_review'],
 'QUANTITY_NEGATIVE_VALUE_POLICIES': ['negative_values_forbidden',
                                      'negative_values_allowed_by_source',
                                      'negative_values_require_owner_handoff'],
 'QUANTITY_REPRESENTATION_KINDS': ['integer_exact',
                                   'decimal_exact',
                                   'fraction_exact',
                                   'fixed_point_scaled',
                                   'source_literal_only',
                                   'blocked_pending_numeric_choice'],
 'QUARANTINE_STAGES': ['quarantined_for_review'],
 'RESOURCE_FAMILIES': ['pooled_expendable',
                       'scene_counter',
                       'charge',
                       'currency_like',
                       'material',
                       'asset_integrity',
                       'vehicle_integrity',
                       'time_window',
                       'opportunity',
                       'social_capital',
                       'faction_standing',
                       'clue_information',
                       'risk_heat',
                       'strain_corruption',
                       'injury_recovery',
                       'cooldown',
                       'debt_obligation',
                       'source_local_resource'],
 'RESOURCE_MATH_DECISIONS': ['accepted_for_planning',
                             'normalized_for_planning',
                             'source_local_retained',
                             'requires_validation_review',
                             'requires_owner_handoff',
                             'blocked_missing_dependency',
                             'blocked_incompatible_policy',
                             'blocked_hidden_information',
                             'quarantined_for_review',
                             'escalated_to_doctrine'],
 'RESOURCE_MATH_DEPENDENCY_TYPES': ['command_ref',
                                    'action_legality_ref',
                                    'state_snapshot_ref',
                                    'state_record_ref',
                                    'state_projection_ref',
                                    'state_delta_ref',
                                    'transaction_ref',
                                    'transaction_preview_ref',
                                    'event_commitment_ref',
                                    'event_record_ref',
                                    'validation_request_ref',
                                    'validation_result_ref',
                                    'runtime_trace_ref',
                                    'hidden_information_ref',
                                    'context_projection_ref',
                                    'provenance_ref',
                                    'rng_request_ref',
                                    'rng_result_ref',
                                    'table_oracle_ref',
                                    'table_oracle_result_ref',
                                    'owner_handoff_ref',
                                    'registry_ref',
                                    'decision_log_ref',
                                    'subject_ref',
                                    'unit_ref',
                                    'dimension_ref',
                                    'resource_math_request_ref',
                                    'resource_math_result_ref',
                                    'rollback_accounting_ref'],
 'RESOURCE_MATH_OWNER_DOMAINS': ['RT001_command_lifecycle_action_legality',
                                 'RT002_resource_consequence_math',
                                 'RT003_combat_hazard_damage_recovery',
                                 'RT004_ability_effect_skill_binding',
                                 'RT005_context_packet_hidden_information',
                                 'RT006_mission_reward_clue_routing',
                                 'RT007_social_faction_actor_knowledge',
                                 'RT008_generated_content_provenance_recurrence',
                                 'RT009_runtime_rng_table_oracle',
                                 'RT010_inventory_item_vehicle_asset',
                                 'RT011_validation_readiness_tooling',
                                 'RT012_d_series_promotion_boundary',
                                 'source_local_owner',
                                 'doctrine_escalation'],
 'RESOURCE_MATH_STAGES': ['resource_math_requested',
                          'source_declaration_captured',
                          'subject_refs_bound',
                          'resource_refs_declared',
                          'quantity_specs_declared',
                          'terms_declared',
                          'bundle_structure_declared',
                          'policy_refs_declared',
                          'dependency_refs_bound',
                          'calculation_ready_for_review',
                          'blocked_pending_validation',
                          'blocked_pending_owner_handoff',
                          'quarantined_for_review',
                          'escalated_to_doctrine'],
 'RESOURCE_MATH_SUBJECT_ROLES': ['primary_subject',
                                 'payer_subject',
                                 'beneficiary_subject',
                                 'resource_owner',
                                 'affected_subject',
                                 'source_subject',
                                 'target_subject',
                                 'authority_source',
                                 'provenance_source'],
 'RESOURCE_MATH_SUBJECT_TYPES': ['actor',
                                 'command',
                                 'action',
                                 'item',
                                 'asset',
                                 'vehicle',
                                 'mission',
                                 'faction',
                                 'location',
                                 'state_record',
                                 'generated_content',
                                 'resource_owner',
                                 'source_local_subject',
                                 'unknown_pending_review'],
 'RESOURCE_TERM_POLICY_ROUTES': ['owner_handoff_required', 'quarantine_required', 'doctrine_escalation_required'],
 'RESOURCE_TERM_VALUE_MODES': ['resource_quantity', 'resource_reference_only', 'quantity_only', 'policy_only'],
 'ROUNDING_POLICIES': ['no_rounding',
                       'round_down',
                       'round_up',
                       'round_nearest',
                       'round_toward_zero',
                       'round_away_from_zero',
                       'tie_to_even',
                       'tie_away_from_zero',
                       'blocked_pending_rounding_choice'],
 'SOURCE_LOCAL_STAGES': ['source_declaration_captured',
                         'resource_refs_declared',
                         'terms_declared',
                         'bundle_structure_declared',
                         'policy_refs_declared'],
 'VALIDATION_BLOCK_STAGES': ['blocked_pending_validation'],
 'VALIDATION_INTEGRATION_DECISIONS': ['validation_ready',
                                      'validation_passed',
                                      'validation_failed',
                                      'rejected_by_missing_command_ref',
                                      'rejected_by_missing_state_ref',
                                      'rejected_by_missing_transaction_ref',
                                      'rejected_by_missing_event_commitment_ref',
                                      'rejected_by_missing_invariant_set',
                                      'rejected_by_hidden_information_risk',
                                      'rejected_by_provenance_gap',
                                      'rejected_by_schema_mismatch',
                                      'rejected_by_authority_mismatch',
                                      'rejected_by_phase_boundary',
                                      'quarantined_for_review',
                                      'escalated_to_doctrine',
                                      'unsupported_validation_scope'],
 'VISIBILITY_POLICIES': ['public',
                         'actor_visible',
                         'narrator_only',
                         'hidden',
                         'redacted',
                         'delayed_reveal',
                         'derived_only']}
EXPECTED_STAGE_MATRIX = {'accepted_for_planning': {'allowed_stages': ['resource_math_requested', 'calculation_ready_for_review'],
                           'blocking': False,
                           'escalated': False,
                           'quarantined': False},
 'blocked_hidden_information': {'allowed_stages': ['dependency_refs_bound', 'blocked_pending_validation'],
                                'blocking': True,
                                'escalated': False,
                                'quarantined': False},
 'blocked_incompatible_policy': {'allowed_stages': ['policy_refs_declared'],
                                 'blocking': True,
                                 'escalated': False,
                                 'quarantined': False},
 'blocked_missing_dependency': {'allowed_stages': ['dependency_refs_bound',
                                                   'blocked_pending_validation',
                                                   'blocked_pending_owner_handoff'],
                                'blocking': True,
                                'escalated': False,
                                'quarantined': False},
 'escalated_to_doctrine': {'allowed_stages': ['escalated_to_doctrine'],
                           'blocking': True,
                           'escalated': True,
                           'quarantined': False},
 'normalized_for_planning': {'allowed_stages': ['source_declaration_captured',
                                                'subject_refs_bound',
                                                'resource_refs_declared',
                                                'quantity_specs_declared',
                                                'terms_declared',
                                                'bundle_structure_declared',
                                                'policy_refs_declared',
                                                'dependency_refs_bound',
                                                'calculation_ready_for_review'],
                             'blocking': False,
                             'escalated': False,
                             'quarantined': False},
 'quarantined_for_review': {'allowed_stages': ['quarantined_for_review'],
                            'blocking': True,
                            'escalated': False,
                            'quarantined': True},
 'requires_owner_handoff': {'allowed_stages': ['blocked_pending_owner_handoff'],
                            'blocking': True,
                            'escalated': False,
                            'quarantined': False},
 'requires_validation_review': {'allowed_stages': ['blocked_pending_validation'],
                                'blocking': True,
                                'escalated': False,
                                'quarantined': False},
 'source_local_retained': {'allowed_stages': ['source_declaration_captured',
                                              'resource_refs_declared',
                                              'terms_declared',
                                              'bundle_structure_declared',
                                              'policy_refs_declared'],
                           'blocking': False,
                           'escalated': False,
                           'quarantined': False}}
EXPECTED_BUNDLE_SETS = {'ALTERNATIVE_ATOMICITY_SET': ['alternative_exactly_one',
                               'alternative_at_least_one',
                               'alternative_at_most_one',
                               'alternative_any'],
 'ORDERING_DECLARED_SET': ['unordered_terms',
                           'source_ordered_terms',
                           'dependency_ordered_terms',
                           'priority_ordered_terms'],
 'ORDERING_ORDERED_SET': ['source_ordered_terms', 'dependency_ordered_terms', 'priority_ordered_terms'],
 'PARTIAL_REVIEW_SET': ['partial_settlement_requires_owner_review', 'partial_settlement_requires_validation']}
EXPECTED_BUNDLE_MATRIX = [['all_or_nothing_requested',
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement'],
  'absent',
  'valid declaration, no settlement'],
 ['all_or_nothing_requested',
  ['blocked_pending_ordering_policy'],
  ['no_partial_settlement'],
  'absent',
  'blocking review'],
 ['best_effort_requested',
  'ORDERING_DECLARED_SET',
  ['partial_settlement_allowed'],
  'absent',
  'valid declaration, no settlement'],
 ['best_effort_requested',
  'ORDERING_DECLARED_SET',
  'PARTIAL_REVIEW_SET',
  'absent',
  'blocking review; owner or validation route follows the partial policy'],
 ['best_effort_requested',
  ['blocked_pending_ordering_policy'],
  ['partial_settlement_allowed',
   'partial_settlement_requires_owner_review',
   'partial_settlement_requires_validation',
   'blocked_pending_settlement_policy'],
  'absent',
  'blocking review'],
 ['ordered_partial_allowed',
  'ORDERING_ORDERED_SET',
  ['partial_settlement_allowed'],
  'absent',
  'valid declaration, no settlement'],
 ['ordered_partial_allowed',
  'ORDERING_ORDERED_SET',
  'PARTIAL_REVIEW_SET',
  'absent',
  'blocking review; owner or validation route follows the partial policy'],
 ['ordered_partial_allowed',
  ['blocked_pending_ordering_policy'],
  ['partial_settlement_allowed',
   'partial_settlement_requires_owner_review',
   'partial_settlement_requires_validation',
   'blocked_pending_settlement_policy'],
  'absent',
  'blocking review'],
 ['unordered_partial_allowed',
  ['unordered_terms'],
  ['partial_settlement_allowed'],
  'absent',
  'valid declaration, no settlement'],
 ['unordered_partial_allowed',
  ['unordered_terms'],
  'PARTIAL_REVIEW_SET',
  'absent',
  'blocking review; owner or validation route follows the partial policy'],
 ['unordered_partial_allowed',
  ['blocked_pending_ordering_policy'],
  ['partial_settlement_allowed',
   'partial_settlement_requires_owner_review',
   'partial_settlement_requires_validation',
   'blocked_pending_settlement_policy'],
  'absent',
  'blocking review'],
 ['alternative_exactly_one',
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement'],
  'present and valid',
  'valid declaration, no alternative chosen'],
 ['alternative_at_least_one',
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement'],
  'present and valid',
  'valid declaration, no alternative chosen'],
 ['alternative_at_most_one',
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement'],
  'present and valid',
  'valid declaration, no alternative chosen'],
 ['alternative_any',
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement'],
  'present and valid',
  'valid declaration, no alternative chosen'],
 ['ALTERNATIVE_ATOMICITY_SET',
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement'],
  'absent',
  'invalid: alternative groups required'],
 ['ALTERNATIVE_ATOMICITY_SET',
  'ORDERING_DECLARED_SET',
  ['partial_settlement_allowed',
   'partial_settlement_requires_owner_review',
   'partial_settlement_requires_validation',
   'blocked_pending_settlement_policy'],
  'present or absent',
  'invalid: alternatives cannot also declare partial settlement in PR-5A'],
 ['invalid_mixed_atomicity',
  'ORDERING_DECLARED_SET or { "blocked_pending_ordering_policy" }',
  ['no_partial_settlement',
   'partial_settlement_allowed',
   'partial_settlement_requires_owner_review',
   'partial_settlement_requires_validation',
   'blocked_pending_settlement_policy'],
  'present or absent',
  'invalid mixed atomicity'],
 ['blocked_pending_transaction_policy',
  'ORDERING_DECLARED_SET or { "blocked_pending_ordering_policy" }',
  ['no_partial_settlement',
   'partial_settlement_allowed',
   'partial_settlement_requires_owner_review',
   'partial_settlement_requires_validation',
   'blocked_pending_settlement_policy'],
  'present or absent',
  'blocking owner/transaction-policy review'],
 [['all_or_nothing_requested', 'best_effort_requested', 'ordered_partial_allowed', 'unordered_partial_allowed'],
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement',
   'partial_settlement_allowed',
   'partial_settlement_requires_owner_review',
   'partial_settlement_requires_validation',
   'blocked_pending_settlement_policy'],
  'overlapping groups',
  'invalid: non-alternative atomicity cannot declare alternative groups'],
 ['ALTERNATIVE_ATOMICITY_SET',
  'ORDERING_DECLARED_SET',
  ['no_partial_settlement'],
  'overlapping groups',
  'invalid unless a future explicit policy authorizes overlap']]
EXPECTED_BLOCKER_TABLE = [{'aggregate_validity_prerequisite': 'structural request valid; malformed/missing binding State C already rejected',
  'blocking': True,
  'diagnostics_rule': 'preserve lower-priority blockers in diagnostics',
  'escalated': True,
  'exact_decision': 'escalated_to_doctrine',
  'exact_stage_or_allowed_stage_set': ['escalated_to_doctrine'],
  'precedence': 1,
  'quarantined': False,
  'required_dependency': 'none unless referenced fields independently require bindings',
  'trigger': 'policy_route == doctrine_escalation_required or doctrine escalation route detected'},
 {'aggregate_validity_prerequisite': 'structural request valid; malformed/missing binding State C already rejected',
  'blocking': True,
  'diagnostics_rule': 'preserve lower-priority blockers in diagnostics',
  'escalated': False,
  'exact_decision': 'quarantined_for_review',
  'exact_stage_or_allowed_stage_set': ['quarantined_for_review'],
  'precedence': 2,
  'quarantined': True,
  'required_dependency': 'none unless referenced fields independently require bindings',
  'trigger': 'policy_route == quarantine_required or quarantine route detected'},
 {'aggregate_validity_prerequisite': 'structural request valid; the dependency record resolves; dependency-based '
                                     'hidden-information blocking requires required=True and satisfied=True',
  'blocking': True,
  'diagnostics_rule': 'preserve every simultaneous lower-priority blocker, including missing or unsatisfied '
                      'dependencies on other records',
  'escalated': False,
  'exact_decision': 'blocked_hidden_information',
  'exact_stage_or_allowed_stage_set': ['dependency_refs_bound', 'blocked_pending_validation'],
  'precedence': 3,
  'quarantined': False,
  'required_dependency': 'for a dependency-based hidden-information blocker, the scoped dependency is required=True, '
                         'satisfied=True, hidden_info_safe=False; separately referenced hidden-information evidence '
                         'uses its lawful RT-005 dependency type',
  'trigger': 'hidden_info_safe=False on a scoped dependency that is otherwise complete (required=True and '
             'satisfied=True), or another independently valid hidden-information blocker'},
 {'aggregate_validity_prerequisite': 'State C missing/malformed binding rejected before result construction',
  'blocking': True,
  'diagnostics_rule': 'record all missing/unsatisfied dependency blockers and preserve lower-priority blockers',
  'escalated': False,
  'exact_decision': 'blocked_missing_dependency',
  'exact_stage_or_allowed_stage_set': ['dependency_refs_bound',
                                       'blocked_pending_validation',
                                       'blocked_pending_owner_handoff'],
  'precedence': 4,
  'quarantined': False,
  'required_dependency': 'the reached dependency record exists with required=True and satisfied=False',
  'trigger': 'State B incomplete binding or State D required-unsatisfied named dependency reached by scope'},
 {'aggregate_validity_prerequisite': 'structural request valid; quantity/term/bundle resolves',
  'blocking': True,
  'diagnostics_rule': 'preserve lower-priority blockers in diagnostics',
  'escalated': False,
  'exact_decision': 'blocked_incompatible_policy',
  'exact_stage_or_allowed_stage_set': ['policy_refs_declared'],
  'precedence': 5,
  'quarantined': False,
  'required_dependency': 'none beyond dependencies named by scoped records',
  'trigger': 'blocked_pending_numeric_choice or incompatible policy in typed scope'},
 {'aggregate_validity_prerequisite': 'structural request valid; owner-handoff reference bindings resolve',
  'blocking': True,
  'diagnostics_rule': 'preserve lower-priority blockers in diagnostics',
  'escalated': False,
  'exact_decision': 'requires_owner_handoff',
  'exact_stage_or_allowed_stage_set': ['blocked_pending_owner_handoff'],
  'precedence': 6,
  'quarantined': False,
  'required_dependency': 'owner_handoff_ref required and satisfied for each owner handoff reference',
  'trigger': 'negative_values_require_owner_handoff or policy_route == owner_handoff_required'},
 {'aggregate_validity_prerequisite': 'structural request valid; validation request binding resolves',
  'blocking': True,
  'diagnostics_rule': 'preserve lower-priority blockers in diagnostics',
  'escalated': False,
  'exact_decision': 'requires_validation_review',
  'exact_stage_or_allowed_stage_set': ['blocked_pending_validation'],
  'precedence': 7,
  'quarantined': False,
  'required_dependency': 'validation_request_ref required and satisfied; validation_result_ref absent until result '
                         'exists',
  'trigger': 'validation review required by validation co-presence or partial-settlement validation route'},
 {'aggregate_validity_prerequisite': 'structural request valid; provenance dependencies required/satisfied',
  'blocking': False,
  'diagnostics_rule': 'diagnostic note allowed; does not block or override higher-priority blockers',
  'escalated': False,
  'exact_decision': 'non_blocking_no_decision_override',
  'exact_stage_or_allowed_stage_set': 'ordinary compatibility matrix',
  'precedence': 8,
  'quarantined': False,
  'required_dependency': 'provenance_ref required and satisfied for each provenance ref',
  'trigger': 'negative_values_allowed_by_source with valid source_literal and provenance bindings'},
 {'aggregate_validity_prerequisite': 'structural request valid and typed scope closed',
  'blocking': 'ordinary compatibility matrix',
  'diagnostics_rule': 'normal diagnostics only',
  'escalated': 'ordinary compatibility matrix',
  'exact_decision': 'ordinary compatibility matrix',
  'exact_stage_or_allowed_stage_set': 'ordinary compatibility matrix',
  'precedence': 9,
  'quarantined': 'ordinary compatibility matrix',
  'required_dependency': 'all scoped required dependencies satisfied',
  'trigger': 'no blocker detected'}]
EXPECTED_BINDING_STATE_MATRIX = [{'aggregate': 'request',
  'field_family': 'request field binding',
  'matching_record_required': 'exactly one',
  'missing_malformed_posture': 'State C aggregate-invalid before result construction',
  'permitted_result_decision': 'blocked_missing_dependency when reached if satisfied=False; otherwise ordinary matrix',
  'proposal_eligibility': 'not eligible while reached dependency is unsatisfied',
  'required_flag': 'required=True',
  'satisfied_false_posture': 'State B incomplete binding; request structurally valid but incomplete; any result '
                             'reaching it must be blocked_missing_dependency; hidden_info_safe=False on the same '
                             'record is diagnostic only and does not change the decision',
  'satisfied_true_posture': 'State A complete binding; request structurally valid and may support non-blocking result '
                            'if all other rules pass; hidden_info_safe=False on the same complete record can supply '
                            'hidden-information blocker when scoped'},
 {'aggregate': 'request',
  'field_family': 'request named dependency',
  'matching_record_required': 'record must exist when named by dependency_ids or scope',
  'missing_malformed_posture': 'State C aggregate-invalid when missing, wrong type/reference, duplicate, or '
                               'required=False for required named dependency',
  'permitted_result_decision': 'blocked_missing_dependency when reached if satisfied=False',
  'proposal_eligibility': 'not eligible while reached dependency is unsatisfied',
  'required_flag': 'required=True for required named dependency',
  'satisfied_false_posture': 'State D required-unsatisfied named dependency when named by a record or scope; '
                             'structurally present but blocks result when reached; hidden_info_safe=False on the same '
                             'record is diagnostic only and does not change the decision',
  'satisfied_true_posture': 'State A complete named dependency'},
 {'aggregate': 'result',
  'field_family': 'result request binding',
  'matching_record_required': 'exactly one resource_math_request_ref in result.dependencies',
  'missing_malformed_posture': 'State C result aggregate invalid',
  'permitted_result_decision': 'accepted/normalized require satisfied=True; satisfied=False requires '
                               'blocked_missing_dependency',
  'proposal_eligibility': 'not eligible unless satisfied=True',
  'required_flag': 'required=True',
  'satisfied_false_posture': 'State D; lawful only for blocked_missing_dependency result that scopes or reaches this '
                             'dependency',
  'satisfied_true_posture': 'complete result-to-request binding; accepted/normalized may proceed if all other rules '
                            'pass'},
 {'aggregate': 'result',
  'field_family': 'result validation/trace dependency',
  'matching_record_required': 'exactly one matching record when field supplied or required',
  'missing_malformed_posture': 'State C result aggregate invalid',
  'permitted_result_decision': 'accepted/normalized require satisfied=True; satisfied=False requires '
                               'blocked_missing_dependency',
  'proposal_eligibility': 'not eligible unless satisfied=True',
  'required_flag': 'required=True',
  'satisfied_false_posture': 'State D; lawful only for blocked_missing_dependency result that scopes or reaches this '
                             'dependency',
  'satisfied_true_posture': 'complete result-owned validation/trace dependency'},
 {'aggregate': 'result',
  'field_family': 'scoped named dependency',
  'matching_record_required': 'existing request/result dependency named by typed scope or scoped record',
  'missing_malformed_posture': 'State C aggregate invalid because scoped references must resolve',
  'permitted_result_decision': 'blocked_missing_dependency when satisfied=False; accepted/normalized require '
                               'satisfied=True',
  'proposal_eligibility': 'not eligible unless satisfied=True',
  'required_flag': 'required=True for required scoped dependency',
  'satisfied_false_posture': 'State D; forces blocked_missing_dependency when reached; hidden_info_safe=False on the '
                             'same unsatisfied record is retained diagnostically and does not replace '
                             'blocked_missing_dependency',
  'satisfied_true_posture': 'complete scoped dependency; hidden_info_safe=False on this otherwise-complete record '
                            'supplies blocked_hidden_information'},
 {'aggregate': 'request/result',
  'field_family': 'advisory optional dependency',
  'matching_record_required': 'optional advisory record may exist only when unbound, unnamed, and unscoped',
  'missing_malformed_posture': 'if used as a binding or named/scoped dependency it becomes State C invalid',
  'permitted_result_decision': 'no result decision effect when truly advisory; invalid if used as required binding',
  'proposal_eligibility': 'does not support proposal eligibility and cannot satisfy required proposal dependency',
  'required_flag': 'required=False',
  'satisfied_false_posture': 'State E advisory optional unsatisfied; may coexist with non-blocking result only when '
                             'unbound, unnamed, and unscoped; hidden_info_safe=False while genuinely State E creates '
                             'no result blocker because it is outside typed scope; satisfies nothing',
  'satisfied_true_posture': 'advisory record is not a required binding and satisfies no required field'},
 {'aggregate': 'proposal',
  'field_family': 'proposal dependency',
  'matching_record_required': 'exactly one matching record for each proposal binding/reference',
  'missing_malformed_posture': 'proposal aggregate invalid',
  'permitted_result_decision': 'proposal only follows eligible accepted/normalized result; no blocked result may '
                               'create proposal',
  'proposal_eligibility': 'eligible only when every required proposal dependency is satisfied',
  'required_flag': 'required=True',
  'satisfied_false_posture': 'incomplete dependencies are forbidden in SettlementProposal',
  'satisfied_true_posture': 'complete proposal dependency; proposal may remain eligible if all other rules pass'}]
EXPECTED_COLLISION_MATRIX = [{'blocking': True,
  'case': 'same_record_unsatisfied_and_unsafe',
  'dependency_arrangement': 'one reached dependency record has required=True, satisfied=False, hidden_info_safe=False',
  'diagnostics_retention_rule': 'retain hidden-information risk in diagnostics together with the missing-dependency '
                                'finding',
  'escalated': False,
  'exact_result_decision_or_aggregate_rejection': 'blocked_missing_dependency; not blocked_hidden_information for that '
                                                  'same record because the dependency is not otherwise satisfied',
  'governing_lifecycle_state_or_states': ['State B incomplete binding',
                                          'State D required-unsatisfied named dependency'],
  'proposal_eligibility': 'not eligible',
  'quarantined': False,
  'stage_or_allowed_stage_set': ['dependency_refs_bound',
                                 'blocked_pending_validation',
                                 'blocked_pending_owner_handoff'],
  'structural_validity': 'structurally valid only as State B request binding or State D named/scoped dependency; State '
                         'C rules still reject missing, malformed, duplicate, or optional bindings'},
 {'blocking': True,
  'case': 'separate_complete_unsafe_and_unsatisfied',
  'dependency_arrangement': 'Dependency A has required=True, satisfied=True, hidden_info_safe=False; Dependency B has '
                            'required=True, satisfied=False, hidden_info_safe=True',
  'diagnostics_retention_rule': 'retain the missing-dependency finding for Dependency B; both records remain visible '
                                'to internal validation; neither finding is discarded',
  'escalated': False,
  'exact_result_decision_or_aggregate_rejection': 'blocked_hidden_information determines result because the valid '
                                                  'hidden-information blocker is on a separate otherwise-complete '
                                                  'record and has higher precedence',
  'governing_lifecycle_state_or_states': ['A complete unsafe dependency', 'B State B or State D missing dependency'],
  'proposal_eligibility': 'not eligible',
  'quarantined': False,
  'stage_or_allowed_stage_set': ['dependency_refs_bound', 'blocked_pending_validation'],
  'structural_validity': 'both records resolve and are structurally valid; blockers occur on separate records'},
 {'blocking': True,
  'case': 'separate_complete_unsafe_and_unsatisfied_unsafe',
  'dependency_arrangement': 'Dependency A has required=True, satisfied=True, hidden_info_safe=False; Dependency B has '
                            'required=True, satisfied=False, hidden_info_safe=False',
  'diagnostics_retention_rule': 'retain hidden-information and missing-dependency findings for all records; neither '
                                'finding is discarded',
  'escalated': False,
  'exact_result_decision_or_aggregate_rejection': 'blocked_hidden_information determines result because Dependency A '
                                                  'supplies the otherwise-complete unsafe blocker; Dependency B '
                                                  'remains a missing-dependency blocker for its own record',
  'governing_lifecycle_state_or_states': ['A complete unsafe dependency',
                                          'B State B or State D missing dependency with diagnostic hidden risk'],
  'proposal_eligibility': 'not eligible',
  'quarantined': False,
  'stage_or_allowed_stage_set': ['dependency_refs_bound', 'blocked_pending_validation'],
  'structural_validity': 'both records resolve and are structurally valid when B is State B or State D; blockers occur '
                         'on separate records'},
 {'blocking': True,
  'case': 'complete_unsafe',
  'dependency_arrangement': 'one reached dependency record has required=True, satisfied=True, hidden_info_safe=False',
  'diagnostics_retention_rule': 'retain hidden-information diagnostic for the unsafe dependency',
  'escalated': False,
  'exact_result_decision_or_aggregate_rejection': 'blocked_hidden_information',
  'governing_lifecycle_state_or_states': ['State A complete binding with hidden-information risk'],
  'proposal_eligibility': 'not eligible',
  'quarantined': False,
  'stage_or_allowed_stage_set': ['dependency_refs_bound', 'blocked_pending_validation'],
  'structural_validity': 'structurally valid complete dependency'},
 {'blocking': False,
  'case': 'complete_safe',
  'dependency_arrangement': 'one reached dependency record has required=True, satisfied=True, hidden_info_safe=True',
  'diagnostics_retention_rule': 'no hidden-information diagnostic required by this dependency',
  'escalated': False,
  'exact_result_decision_or_aggregate_rejection': 'no dependency-derived hidden-information blocker',
  'governing_lifecycle_state_or_states': ['State A complete binding'],
  'proposal_eligibility': 'eligible only if all other SettlementProposal rules pass',
  'quarantined': False,
  'stage_or_allowed_stage_set': 'ordinary compatibility matrix',
  'structural_validity': 'structurally valid complete dependency'},
 {'blocking': False,
  'case': 'advisory_optional_unscoped_unsafe',
  'dependency_arrangement': 'one dependency record has required=False, satisfied=False, hidden_info_safe=False and '
                            'remains unbound, unnamed, and unscoped',
  'diagnostics_retention_rule': 'no blocker diagnostic required; internal advisory diagnostics may note unsatisfied '
                                'optional record',
  'escalated': False,
  'exact_result_decision_or_aggregate_rejection': 'no result blocker because it is outside typed scope and satisfies '
                                                  'nothing',
  'governing_lifecycle_state_or_states': ['State E advisory optional unsatisfied'],
  'proposal_eligibility': 'does not support eligibility and cannot satisfy required proposal dependency',
  'quarantined': False,
  'stage_or_allowed_stage_set': 'ordinary compatibility matrix',
  'structural_validity': 'lawful only as State E advisory optional unsatisfied outside typed scope'},
 {'blocking': 'not applicable',
  'case': 'optional_bound_named_or_scoped',
  'dependency_arrangement': 'dependency record has required=False, satisfied=False and is bound, named, or scoped '
                            'where a required dependency is expected',
  'diagnostics_retention_rule': 'report structural invalidity; do not convert to hidden-information or '
                                'missing-dependency result decision',
  'escalated': 'not applicable',
  'exact_result_decision_or_aggregate_rejection': 'aggregate rejection before result construction; not a blocked '
                                                  'result',
  'governing_lifecycle_state_or_states': ['State C missing or malformed binding'],
  'proposal_eligibility': 'not eligible',
  'quarantined': 'not applicable',
  'stage_or_allowed_stage_set': 'not applicable; no result constructed',
  'structural_validity': 'not State E; aggregate-invalid State C'}]
EXPECTED_GRAMMARS = {'blocked_pending_numeric_choice': {'exact_grammar': '^\\S(?:.*\\S)?$ plus universal source_literal character contract',
                                    'explicit_exclusions': 'no empty string, no leading/trailing whitespace, blocks '
                                                           'progression',
                                    'required_lexical_fields': ['source_literal']},
 'decimal_exact': {'exact_grammar': '^[+-]?(0|[1-9][0-9]*)\\.[0-9]+$',
                   'explicit_exclusions': 'no exponent notation, leading decimal point, trailing decimal point, '
                                          'leading zero except before `.`, or embedded separators',
                   'required_lexical_fields': ['magnitude_text']},
 'fixed_point_scaled': {'exact_grammar': 'magnitude ^[+-]?(0|[1-9][0-9]*)$; scale is an int that is not bool and is >= '
                                         '0',
                        'explicit_exclusions': 'no decimal point in magnitude, no exponent notation, no negative scale',
                        'required_lexical_fields': ['magnitude_text', 'scale']},
 'fraction_exact': {'exact_grammar': '^[+-]?(0|[1-9][0-9]*)/[1-9][0-9]*$',
                    'explicit_exclusions': 'no zero denominator, signed denominator, decimal numerator, decimal '
                                           'denominator, or mixed-number shorthand',
                    'required_lexical_fields': ['magnitude_text']},
 'integer_exact': {'exact_grammar': '^[+-]?(0|[1-9][0-9]*)$',
                   'explicit_exclusions': 'no whitespace, exponent notation, decimal point, leading zero except `0`, '
                                          'or embedded separators',
                   'required_lexical_fields': ['magnitude_text']},
 'source_literal_only': {'exact_grammar': '^\\S(?:.*\\S)?$ plus universal source_literal character contract',
                         'explicit_exclusions': 'no empty string, no leading/trailing whitespace, no evaluation',
                         'required_lexical_fields': ['source_literal']}}
EXPECTED_PUBLIC_HELPERS = ['create_resource_math_subject_reference',
 'validate_resource_math_subject_reference',
 'create_resource_reference',
 'validate_resource_reference',
 'create_quantity_specification',
 'validate_quantity_specification',
 'create_resource_math_dependency',
 'validate_resource_math_dependency',
 'create_cost_term',
 'validate_cost_term',
 'create_cost_bundle',
 'validate_cost_bundle',
 'create_consequence_term',
 'validate_consequence_term',
 'create_resource_math_request',
 'validate_resource_math_request',
 'create_resource_math_result',
 'validate_resource_math_result',
 'create_settlement_proposal',
 'validate_settlement_proposal']
EXPECTED_PRIVATE_HELPERS = ['constants/defaults',
 'subject identity',
 'internal refs',
 'external bindings',
 'dependency lifecycle',
 'typed scope',
 'blocker precedence',
 'quantity grammar',
 'source literals',
 'negative policies',
 'term modes/routes',
 'bundle matrix',
 'request/result validation',
 'proposal/request/result validation',
 'false-only fields',
 'tuple/metadata immutability',
 'internal serialization']
EXPECTED_FALSE_ONLY = ['calculation_executed',
 'affordability_executed',
 'reservation_authorized',
 'settlement_authorized',
 'consequence_application_authorized',
 'mutation_authorized',
 'state_delta_application_authorized',
 'transaction_execution_authorized',
 'event_commitment_authorized',
 'event_append_authorized',
 'persistence_authorized',
 'replay_authorized',
 'rng_execution_authorized',
 'table_oracle_execution_authorized',
 'model_authority_authorized',
 'live_play_authorized',
 'ui_authorized',
 'conversion_authorized',
 'canon_promotion_authorized']
EXPECTED_AUTHORITY_FALSE = ['runtime_code_authorized_by_this_pr',
 'domain_code_authorized_by_this_pr',
 'calculation_authorized_by_this_pr',
 'affordability_execution_authorized_by_this_pr',
 'reservation_authorized_by_this_pr',
 'settlement_authorized_by_this_pr',
 'consequence_application_authorized_by_this_pr',
 'mutation_authorized_by_this_pr',
 'state_delta_application_authorized_by_this_pr',
 'transaction_execution_authorized_by_this_pr',
 'event_commitment_authorized_by_this_pr',
 'event_append_authorized_by_this_pr',
 'persistence_authorized_by_this_pr',
 'replay_authorized_by_this_pr',
 'rng_execution_authorized_by_this_pr',
 'table_oracle_execution_authorized_by_this_pr',
 'model_authority_authorized_by_this_pr',
 'model_integration_authorized_by_this_pr',
 'live_play_authorized_by_this_pr',
 'ui_authorized_by_this_pr',
 'conversion_authorized_by_this_pr',
 'canon_promotion_authorized_by_this_pr']


def doc_text() -> str:
    return DOC.read_text()


def contract() -> dict:
    match = re.search(r"```yaml pr5h_effective_contract\n(.*?)\n```", doc_text(), re.S)
    assert match, "machine-readable PR-5H contract block is missing"
    return json.loads(match.group(1))


def shape_field_map(shape: str) -> dict[str, dict[str, str]]:
    return {item["field"]: item for item in contract()["future_shapes"][shape]}


def test_exact_ten_shape_complete_contract_matrix() -> None:
    actual = contract()["future_shapes"]
    assert actual == EXPECTED_SHAPES
    assert list(actual) == [
        "ResourceMathSubjectReference",
        "ResourceReference",
        "QuantitySpecification",
        "ResourceMathDependency",
        "CostTerm",
        "CostBundle",
        "ConsequenceTerm",
        "ResourceMathRequest",
        "ResourceMathResult",
        "SettlementProposal",
    ]
    required_keys = {
        "field",
        "annotation",
        "default",
        "controlled_surface",
        "aggregate_owner",
        "invariant",
        "external_dependency_type",
        "serialization_posture",
        "source_artifact",
        "replacement_artifact",
    }
    for fields in actual.values():
        for field in fields:
            assert set(field) == required_keys
    assert shape_field_map("QuantitySpecification")["precision"]["annotation"] == "int | None"
    assert shape_field_map("QuantitySpecification")["precision"]["replacement_artifact"] == "PR-5F"
    assert shape_field_map("ResourceReference")["unit_ref_id"]["external_dependency_type"] == "unit_ref"
    assert shape_field_map("ResourceReference")["dimension_ref_id"]["external_dependency_type"] == "dimension_ref"
    assert shape_field_map("ResourceMathSubjectReference")["subject_ref_id"]["external_dependency_type"] == "subject_ref"
    assert shape_field_map("ResourceMathResult")["result_id"]["aggregate_owner"] == "local aggregate identity"
    assert shape_field_map("ResourceMathResult")["result_id"]["external_dependency_type"] == "none"
    assert shape_field_map("ResourceMathResult")["request_id"]["external_dependency_type"] == "resource_math_request_ref"
    assert shape_field_map("SettlementProposal")["result_id"]["external_dependency_type"] == "resource_math_result_ref"
    assert shape_field_map("ResourceMathDependency")["reference_id"]["aggregate_owner"] != "same-aggregate internal reference"
    assert shape_field_map("ResourceMathResult")["diagnostics"]["aggregate_owner"] == "local diagnostic text"
    assert shape_field_map("ResourceReference")["source_aliases"]["aggregate_owner"] == "local source-label tuple"
    assert "stage" not in shape_field_map("ResourceMathRequest")
    assert "request_id" not in shape_field_map("SettlementProposal")


def test_absence_of_aliases_and_exact_typed_scope_fields() -> None:
    text = doc_text()
    forbidden_aliases = ["scoped_subject", "scoped_resource", "scoped_quantity", "scoped_cost", "scoped_bundle", "scoped_consequence", "scoped_dependency"]
    for alias in forbidden_aliases:
        assert alias not in text
    expected = [
        "referenced_subject_binding_ids",
        "referenced_resource_ref_ids",
        "referenced_quantity_ids",
        "referenced_cost_term_ids",
        "referenced_cost_bundle_ids",
        "referenced_consequence_term_ids",
        "referenced_dependency_ids",
    ]
    assert contract()["typed_scope_fields"] == expected
    result_fields = shape_field_map("ResourceMathResult")
    for field in expected:
        assert result_fields[field]["annotation"] == "tuple[str, ...]"
        assert result_fields[field]["default"] == "()"
        assert result_fields[field]["aggregate_owner"] == "same-request internal reference"


def test_all_controlled_surfaces_exact() -> None:
    assert contract()["constants"] == EXPECTED_CONSTANTS
    assert contract()["constant_provenance"]["QUANTITY_KINDS"] == {
        "origin": "PR-5B",
        "pr_5d_replacement": "none",
        "pr_5f_replacement": "none",
        "pr_5h_change": "none",
    }
    assert shape_field_map("ResourceMathSubjectReference")["subject_ref_id"]["replacement_artifact"] == "PR-5F binding-contract refinement"
    assert shape_field_map("ResourceReference")["unit_ref_id"]["replacement_artifact"] == "PR-5F binding-contract refinement"
    assert shape_field_map("ResourceReference")["dimension_ref_id"]["replacement_artifact"] == "PR-5F binding-contract refinement"
    assert shape_field_map("QuantitySpecification")["unit_ref_id"]["replacement_artifact"] == "PR-5F binding-contract refinement"
    assert shape_field_map("QuantitySpecification")["dimension_ref_id"]["replacement_artifact"] == "PR-5F binding-contract refinement"
    assert "validation_blocked" not in contract()["constants"]["RESOURCE_MATH_DECISIONS"]
    forbidden = {"hit_points", "spell_slots", "experience_points", "fate_points", "action_points", "movement_points"}
    assert not forbidden & set(contract()["constants"]["RESOURCE_FAMILIES"])


def test_exact_stage_decision_flag_matrix() -> None:
    c = contract()
    assert c["stage_decision_matrix"] == EXPECTED_STAGE_MATRIX
    stages = set(c["constants"]["RESOURCE_MATH_STAGES"])
    decisions = set(c["constants"]["RESOURCE_MATH_DECISIONS"])
    for decision, row in c["stage_decision_matrix"].items():
        assert decision in decisions
        assert set(row["allowed_stages"]) <= stages
        assert set(row) == {"allowed_stages", "blocking", "quarantined", "escalated"}
    allowed_pairs = {(decision, stage) for decision, row in c["stage_decision_matrix"].items() for stage in row["allowed_stages"]}
    all_pairs = {(decision, stage) for decision in decisions for stage in stages}
    assert ("accepted_for_planning", "blocked_pending_validation") in all_pairs - allowed_pairs
    assert ("validation_blocked", "blocked_pending_validation") not in allowed_pairs


def test_all_nineteen_false_only_fields_on_three_aggregate_shapes() -> None:
    assert contract()["false_only_fields"] == EXPECTED_FALSE_ONLY
    for shape in ["ResourceMathRequest", "ResourceMathResult", "SettlementProposal"]:
        fmap = shape_field_map(shape)
        for name in EXPECTED_FALSE_ONLY:
            assert fmap[name]["annotation"] == "bool"
            assert fmap[name]["default"] == "False"
            assert fmap[name]["aggregate_owner"] == "aggregate false-only authority"
            assert "reject True" in fmap[name]["invariant"]


def test_dependency_ownership_lifecycle_and_bindings() -> None:
    c = contract()
    assert c["dependency_ownership"] == {
        "request.dependencies": "request/input references",
        "result.dependencies": "request binding, result validation, trace, and result-specific references",
        "proposal.dependencies": "result binding, validation result, state deltas, trace, rollback accounting, and proposal-specific references",
    }
    states = c["dependency_lifecycle_states"]
    assert list(states) == [
        "A_complete_binding",
        "B_incomplete_binding",
        "C_missing_or_malformed_binding",
        "D_required_unsatisfied_named_dependency",
        "E_advisory_optional_unsatisfied",
    ]
    assert "required=True, satisfied=True" in states["A_complete_binding"]
    assert "required=True, satisfied=False" in states["B_incomplete_binding"]
    assert "required=False" in states["C_missing_or_malformed_binding"]
    assert "forces blocked_missing_dependency" in states["D_required_unsatisfied_named_dependency"]
    assert "satisfies nothing" in states["E_advisory_optional_unsatisfied"]
    assert "State C remains aggregate-invalid" in doc_text()
    assert shape_field_map("SettlementProposal")["rollback_accounting_refs"]["external_dependency_type"] == "rollback_accounting_ref"
    assert shape_field_map("SettlementProposal")["proposed_state_delta_refs"]["external_dependency_type"] == "state_delta_ref"
    dep_fields = shape_field_map("ResourceMathDependency")
    assert "mandatory" in dep_fields["required"]["invariant"]
    assert "lifecycle states A-E" in dep_fields["satisfied"]["invariant"]
    assert "False is distinct from unsatisfied" in dep_fields["hidden_info_safe"]["invariant"]


def test_typed_scope_cardinality_and_closure_rules_are_exact() -> None:
    text = doc_text()
    for phrase in [
        "Each tuple contains unique non-empty IDs",
        "every ID resolves in the supplied request",
        "combined typed scope cannot be entirely empty",
        "accepted and normalized results require at least one scoped resource, quantity, cost term, cost bundle, or consequence term",
        "subject or advisory dependency scope alone is insufficient",
        "blocked results must scope an actual blocker",
        "blocked_missing_dependency may be dependency-only",
        "bundle scope includes all contained terms",
        "term scope includes applicable quantities and dependencies",
        "all scoped references resolve even for blocked, quarantined, or escalated results",
        "normalized_reference_ids remains diagnostic only",
    ]:
        assert phrase in text


def test_exact_simultaneous_blocker_table() -> None:
    table = contract()["simultaneous_blocker_table"]
    assert table == EXPECTED_BLOCKER_TABLE
    assert [row["precedence"] for row in table] == list(range(1, 10))
    assert table[0]["trigger"].startswith("policy_route == doctrine_escalation_required")
    assert table[0]["exact_decision"] == "escalated_to_doctrine"
    assert table[1]["exact_decision"] == "quarantined_for_review"
    assert table[2]["exact_decision"] == "blocked_hidden_information"
    assert "otherwise complete" in table[2]["trigger"]
    assert "required=True and satisfied=True" in table[2]["aggregate_validity_prerequisite"]
    assert table[3]["exact_decision"] == "blocked_missing_dependency"
    assert table[4]["exact_decision"] == "blocked_incompatible_policy"
    assert table[4]["exact_stage_or_allowed_stage_set"] == ["policy_refs_declared"]
    assert table[5]["exact_decision"] == "requires_owner_handoff"
    assert "lower-priority" in doc_text() and "diagnostics" in doc_text()
    assert table[8]["diagnostics_rule"] == "normal diagnostics only"


def test_quantity_lexical_grammars_and_execution_bans_exact() -> None:
    c = contract()
    assert c["quantity_lexical_grammars"] == EXPECTED_GRAMMARS
    assert c["quantity_execution_bans"] == [
        "no Decimal",
        "no Fraction",
        "no float",
        "no exponent notation",
        "no arithmetic",
        "no comparison",
        "no conversion",
        "no rounding",
        "no affordability execution",
        "bool rejection for precision and scale",
        "precision positive and decimal_exact only",
        "scale non-negative and fixed_point_scaled only",
    ]
    assert c["quantity_lexical_grammars"]["integer_exact"]["exact_grammar"] == r"^[+-]?(0|[1-9][0-9]*)$"
    assert "source_literal character contract" in c["quantity_lexical_grammars"]["source_literal_only"]["exact_grammar"]


def test_term_value_modes_policy_routes_and_copresence_matrix() -> None:
    assert contract()["term_value_mode_matrix"] == {
        "resource_quantity": {"resource_ref_id": "required", "quantity_id": "required", "policy_route": "None"},
        "resource_reference_only": {"resource_ref_id": "required", "quantity_id": "None", "policy_route": "None"},
        "quantity_only": {"resource_ref_id": "None", "quantity_id": "required", "policy_route": "None"},
        "policy_only": {"resource_ref_id": "None", "quantity_id": "None", "policy_route": "required RESOURCE_TERM_POLICY_ROUTES"},
    }


def test_complete_costbundle_matrix_and_corrected_bounds() -> None:
    c = contract()
    assert c["cost_bundle_sets"] == EXPECTED_BUNDLE_SETS
    assert c["cost_bundle_matrix"] == EXPECTED_BUNDLE_MATRIX
    postures = [row[4] for row in c["cost_bundle_matrix"]]
    assert "invalid mixed atomicity" in postures
    assert "blocking owner/transaction-policy review" in postures
    assert "invalid: non-alternative atomicity cannot declare alternative groups" in postures
    assert "invalid unless a future explicit policy authorizes overlap" in postures
    assert c["cost_bundle_bound_corrections"] == [
        "minimum_required_terms <= len(term_ids)",
        "maximum_allowed_terms <= len(term_ids)",
        "minimum_required_terms <= maximum_allowed_terms when both supplied",
        "all_or_nothing_requested bounds both None or both equal len(term_ids)",
        "no selection or settlement execution in PR-5A",
    ]


def test_binding_state_matrix_reconciles_field_invariants() -> None:
    matrix = contract()["binding_state_matrix"]
    assert matrix == EXPECTED_BINDING_STATE_MATRIX
    rows = {(row["aggregate"], row["field_family"]): row for row in matrix}
    assert "State B incomplete binding" in rows[("request", "request field binding")]["satisfied_false_posture"]
    assert "structurally valid" in rows[("request", "request field binding")]["satisfied_false_posture"]
    assert rows[("request", "request field binding")]["missing_malformed_posture"] == "State C aggregate-invalid before result construction"
    assert "State D" in rows[("result", "scoped named dependency")]["satisfied_false_posture"]
    assert "blocked_missing_dependency" in rows[("result", "scoped named dependency")]["permitted_result_decision"]
    assert "accepted/normalized require satisfied=True" in rows[("result", "result request binding")]["permitted_result_decision"]
    assert rows[("proposal", "proposal dependency")]["satisfied_false_posture"] == "incomplete dependencies are forbidden in SettlementProposal"
    assert rows[("proposal", "proposal dependency")]["proposal_eligibility"] == "eligible only when every required proposal dependency is satisfied"


def test_external_binding_invariants_allow_structural_incomplete_states() -> None:
    subject_ref = shape_field_map("ResourceMathSubjectReference")["subject_ref_id"]["invariant"]
    unit_ref = shape_field_map("ResourceReference")["unit_ref_id"]["invariant"]
    dimension_ref = shape_field_map("ResourceReference")["dimension_ref_id"]["invariant"]
    quantity_unit = shape_field_map("QuantitySpecification")["unit_ref_id"]["invariant"]
    quantity_dimension = shape_field_map("QuantitySpecification")["dimension_ref_id"]["invariant"]
    for invariant in [subject_ref, unit_ref, dimension_ref, quantity_unit, quantity_dimension]:
        assert "satisfied=False is lifecycle State B" in invariant
        assert "structurally valid but incomplete" in invariant
        assert "required/satisfied" not in invariant
    result_request = shape_field_map("ResourceMathResult")["request_id"]["invariant"]
    result_trace = shape_field_map("ResourceMathResult")["trace_ref_id"]["invariant"]
    scoped_dependency = shape_field_map("ResourceMathResult")["referenced_dependency_ids"]["invariant"]
    for invariant in [result_request, result_trace, scoped_dependency]:
        assert "State D" in invariant
        assert "blocked_missing_dependency" in invariant
        assert "accepted/normalized" in invariant or "accepted_for_planning or normalized_for_planning" in invariant
    proposal_dependencies = shape_field_map("SettlementProposal")["dependencies"]["invariant"]
    assert "every required proposal dependency must be satisfied" in proposal_dependencies
    assert "incomplete dependencies are forbidden" in proposal_dependencies


def test_dependency_hidden_information_collision_matrix_exact_cases() -> None:
    matrix = contract()["dependency_hidden_information_collision_matrix"]
    assert matrix == EXPECTED_COLLISION_MATRIX
    rows = {row["case"]: row for row in matrix}
    same = rows["same_record_unsatisfied_and_unsafe"]
    assert same["exact_result_decision_or_aggregate_rejection"].startswith("blocked_missing_dependency")
    assert "not blocked_hidden_information" in same["exact_result_decision_or_aggregate_rejection"]
    assert same["stage_or_allowed_stage_set"] == ["dependency_refs_bound", "blocked_pending_validation", "blocked_pending_owner_handoff"]
    assert same["blocking"] is True and same["quarantined"] is False and same["escalated"] is False
    assert "hidden-information risk" in same["diagnostics_retention_rule"]
    separate = rows["separate_complete_unsafe_and_unsatisfied"]
    assert separate["exact_result_decision_or_aggregate_rejection"].startswith("blocked_hidden_information")
    assert "missing-dependency finding" in separate["diagnostics_retention_rule"]
    separate_unsafe = rows["separate_complete_unsafe_and_unsatisfied_unsafe"]
    assert separate_unsafe["exact_result_decision_or_aggregate_rejection"].startswith("blocked_hidden_information")
    assert "Dependency B remains a missing-dependency blocker" in separate_unsafe["exact_result_decision_or_aggregate_rejection"]
    complete_unsafe = rows["complete_unsafe"]
    assert complete_unsafe["exact_result_decision_or_aggregate_rejection"] == "blocked_hidden_information"
    complete_safe = rows["complete_safe"]
    assert complete_safe["exact_result_decision_or_aggregate_rejection"] == "no dependency-derived hidden-information blocker"
    assert complete_safe["blocking"] is False
    advisory = rows["advisory_optional_unscoped_unsafe"]
    assert advisory["governing_lifecycle_state_or_states"] == ["State E advisory optional unsatisfied"]
    assert advisory["exact_result_decision_or_aggregate_rejection"] == "no result blocker because it is outside typed scope and satisfies nothing"
    optional_invalid = rows["optional_bound_named_or_scoped"]
    assert optional_invalid["governing_lifecycle_state_or_states"] == ["State C missing or malformed binding"]
    assert optional_invalid["exact_result_decision_or_aggregate_rejection"] == "aggregate rejection before result construction; not a blocked result"


def test_hidden_information_collision_cross_section_consistency() -> None:
    c = contract()
    hidden_invariant = shape_field_map("ResourceMathDependency")["hidden_info_safe"]["invariant"]
    assert "otherwise complete (required=True and satisfied=True)" in hidden_invariant
    assert "required=True and satisfied=False" in hidden_invariant
    assert "does not replace blocked_missing_dependency" in hidden_invariant
    states = c["dependency_lifecycle_states"]
    assert "does not replace blocked_missing_dependency" in states["B_incomplete_binding"]
    assert "does not replace blocked_missing_dependency" in states["D_required_unsatisfied_named_dependency"]
    assert "creates no result blocker" in states["E_advisory_optional_unsatisfied"]
    binding_rows = {row["field_family"]: row for row in c["binding_state_matrix"]}
    assert "hidden_info_safe=False on the same record is diagnostic only" in binding_rows["request field binding"]["satisfied_false_posture"]
    assert "hidden_info_safe=False on this otherwise-complete record supplies blocked_hidden_information" in binding_rows["scoped named dependency"]["satisfied_true_posture"]
    hidden_row = c["simultaneous_blocker_table"][2]
    assert "otherwise complete" in hidden_row["trigger"]
    assert "required=True, satisfied=True, hidden_info_safe=False" in hidden_row["required_dependency"]
    collision_cases = {row["case"] for row in c["dependency_hidden_information_collision_matrix"]}
    assert collision_cases == {
        "same_record_unsatisfied_and_unsafe",
        "separate_complete_unsafe_and_unsatisfied",
        "separate_complete_unsafe_and_unsatisfied_unsafe",
        "complete_unsafe",
        "complete_safe",
        "advisory_optional_unscoped_unsafe",
        "optional_bound_named_or_scoped",
    }
    assert "same-record and separate-record hidden-information/missing-dependency collision matrix" in doc_text()


def test_source_literals_negative_policies_and_no_evaluation() -> None:
    text = doc_text()
    for phrase in [
        "non-empty `str`",
        "one line",
        "no leading/trailing whitespace",
        "no CR, LF, tab, NUL, Unicode `Cc`, or Unicode `Cs`",
        "ordinary Unicode text and interior spaces allowed",
        "preserve exactly",
        "no parsing, normalization, arithmetic, or evaluation",
        "including support for `negative_values_allowed_by_source`",
        "`-0`, `-0.0`, and `-0/1`",
    ]:
        assert phrase in text


def test_direct_request_result_proposal_architecture_and_eligibility() -> None:
    c = contract()
    assert c["direct_validation_signatures"] == [
        "create_resource_math_result(*, request: ResourceMathRequest, ...) -> ResourceMathResult",
        "validate_resource_math_result(result: ResourceMathResult, *, request: ResourceMathRequest) -> bool",
        "create_settlement_proposal(*, request: ResourceMathRequest, result: ResourceMathResult, ...) -> SettlementProposal",
        "validate_settlement_proposal(proposal: SettlementProposal, *, request: ResourceMathRequest, result: ResourceMathResult) -> bool",
    ]
    assert "No certificate object, repository lookup, global registry, or `already_validated` boolean" in doc_text()
    assert c["settlement_eligibility"]["requires"] == [
        "result.stage == calculation_ready_for_review",
        "result.decision in {accepted_for_planning, normalized_for_planning}",
        "validation_decision == validation_passed",
        "non-blocking",
        "non-quarantined",
        "non-escalated",
        "every scoped dependency satisfied",
        "no scoped blocker",
        "non-empty unique proposed_state_delta_refs",
        "matching required/satisfied state_delta_ref dependencies",
    ]
    assert c["settlement_eligibility"]["rejects"] == [
        "accepted_for_planning at resource_math_requested",
        "normalized_for_planning at earlier declaration stages",
        "source_local_retained",
        "blocked, handoff, review, quarantine, or escalation results",
        "event-only consequences",
        "policy-only terms",
    ]


def test_factory_validator_parity_and_private_helper_responsibilities() -> None:
    c = contract()
    assert c["public_helpers"] == EXPECTED_PUBLIC_HELPERS
    assert c["private_helper_responsibilities"] == EXPECTED_PRIVATE_HELPERS
    text = doc_text()
    for helper in EXPECTED_PUBLIC_HELPERS:
        assert helper in text
    for responsibility in EXPECTED_PRIVATE_HELPERS:
        assert responsibility in text
    for phrase in [
        "frozen keyword-only future dataclasses",
        "tuple copying",
        "MappingProxyType",
        "no callable metadata",
        "internal `to_dict()` only",
        "no `to_public_dict`",
        "defensive serialization",
        "no calculation during serialization",
        "RT-005 owns public projection and redaction",
    ]:
        assert phrase in text


def test_classification_authority_fields_match_registry_and_are_complete() -> None:
    c = contract()
    doc = doc_text()
    registry = REGISTRY.read_text()
    assert c["authority_false_fields"] == EXPECTED_AUTHORITY_FALSE
    for field in EXPECTED_AUTHORITY_FALSE:
        assert f"  {field}: false" in doc
        assert f"  {field}: false" in registry
    assert "pr_5a_authorized: false" in doc
    assert "pr_5a_blocked: true" in doc
    assert "pr_5i_is_sole_next_step: true" in doc


def test_corpus_pressure_review_is_explicit() -> None:
    text = doc_text()
    for phrase in [
        "Fantasy resources",
        "Science-fiction energy",
        "Cultivation qi",
        "Class/archetype features",
        "Profession/career economies",
        "Point-buy costs",
        "Narrative currency",
        "Cyberware/biotech capacity",
        "Psionics fatigue",
        "Horror/investigation stress",
        "Vehicles/mechs/ships",
        "Companions/summons",
        "Crafting/salvage/requisition",
        "Mission/faction/debt consequences",
        "Source-local cosmology",
        "Generated content resources",
        "Persistent campaign consequences",
    ]:
        assert phrase in text


def test_tracking_uniqueness_registry_decision_log_and_authority() -> None:
    registry = REGISTRY.read_text()
    decisions = DECISIONS.read_text()
    assert registry.startswith("registry_version: 0.1.0")
    assert registry.count(ARTIFACT_ID) == 1
    assert decisions.count(f"## {ARTIFACT_ID}") == 1
    assert registry.count("version: 0.1.90") == 1
    assert registry.count("action: runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening") == 1
    assert "planning_only" in registry
    assert "pr_5a_authorized: false" in registry
    assert "pr_5a_blocked: true" in registry
    assert "RUNTIME-DOMAIN-PR-5I" in registry
    assert "tests/test_runtime_domain_pr_5h_resource_consequence_math_final_residual_planning_hardening.py" in registry
    assert "PRs #278 and #279 were abandoned" in decisions
    assert "no implementation authority" in decisions


def test_pr_5h_registry_record_has_required_tracking_shape() -> None:
    data = yaml.safe_load(REGISTRY.read_text())
    records = [record for record in data["file_records"] if record.get("file_id") == ARTIFACT_ID]
    assert len(records) == 1
    record = records[0]
    required_keys = {
        "file_id",
        "filename",
        "proposed_path",
        "layer",
        "phase",
        "status",
        "authority_level",
        "owner",
        "purpose",
        "owns",
        "must_not_own",
        "dependencies",
        "blocked_by",
        "unlocks",
        "downstream_consumers",
        "donor_pressure_absorbed",
        "hard_refusals",
        "escalation_triggers",
        "required_tests",
        "test_status",
        "review_status",
        "promotion_requirements",
        "scale_gate_relevance",
        "broad_conversion_relevance",
        "canon_relevance",
        "runtime_relevance",
        "live_play_relevance",
        "notes",
    }
    assert required_keys <= set(record)
    for key in ["donor_pressure_absorbed", "hard_refusals", "escalation_triggers"]:
        assert isinstance(record[key], list), key
        assert record[key], key
        assert all(isinstance(item, str) and item.strip() == item and item for item in record[key])

    donor_text = "\n".join(record["donor_pressure_absorbed"]).lower()
    for phrase in [
        "fantasy",
        "science-fiction",
        "cultivation",
        "class",
        "point-buy",
        "narrative",
        "cyberware",
        "source-local cosmology",
        "persistent campaign consequences",
    ]:
        assert phrase in donor_text
    assert "not automatic astra canon" in donor_text

    hard_refusal_text = "\n".join(record["hard_refusals"]).lower()
    for phrase in [
        "no runtime or domain implementation authority",
        "no resource calculation",
        "affordability execution",
        "reservation execution",
        "settlement execution",
        "consequence application",
        "state mutation",
        "transaction execution",
        "event append",
        "event commitment",
        "persistence",
        "replay",
        "rng execution",
        "table/oracle execution",
        "model authority",
        "live-play authority",
        "ui authority",
        "conversion authorization",
        "sourcebook inclusion",
        "canon promotion",
        "no public projection",
        "no cross-owner authority capture",
    ]:
        assert phrase in hard_refusal_text

    escalation_text = "\n".join(record["escalation_triggers"]).lower()
    for phrase in [
        "cannot map into the ten-shape planning contract",
        "not owned by rt-002",
        "actual calculation",
        "hidden information",
        "rt-005",
        "combat",
        "rt-003",
        "ability",
        "rt-004",
        "mission",
        "generated-content",
        "source-local donor metaphysics",
        "external dependency owner",
        "new field",
        "doctrine or owner specifications",
        "quarantine",
    ]:
        assert phrase in escalation_text

    assert record["pr_5a_authorized"] is False
    assert record["pr_5a_blocked"] is True
    assert record["pr_5i_only_next_step"] is True
    assert record["next_step_authorized"].startswith("RUNTIME-DOMAIN-PR-5I")
    for field in EXPECTED_AUTHORITY_FALSE:
        assert record[field] is False
    record_text = "\n".join(str(value) for value in record.values()).lower()
    assert "src/astra_runtime/domain/resource_consequence_math.py" not in record_text
    assert "resource_consequence_math.py creation" in record_text
    assert "implements runtime" not in record_text


def test_resource_math_result_has_no_resource_math_result_ref_self_binding() -> None:
    result_fields = shape_field_map("ResourceMathResult")
    proposal_fields = shape_field_map("SettlementProposal")
    assert result_fields["result_id"]["external_dependency_type"] == "none"
    assert "no resource_math_result_ref self-binding" in result_fields["result_id"]["invariant"]
    assert result_fields["dependencies"]["external_dependency_type"] == "none"
    assert "no resource_math_result_ref self-binding" in result_fields["dependencies"]["invariant"]
    assert proposal_fields["result_id"]["external_dependency_type"] == "resource_math_result_ref"
    assert contract()["result_self_binding_rule"] == (
        "A ResourceMathResult never carries a resource_math_result_ref dependency for its own result_id; "
        "only a downstream SettlementProposal binds result.result_id through resource_math_result_ref."
    )


def test_git_footprint_when_base_ref_available_and_implementation_module_present() -> None:
    ref = subprocess.run(["git", "rev-parse", "--verify", "origin/main"], cwd=ROOT, text=True, capture_output=True)
    if ref.returncode == 0:
        diff = subprocess.run(["git", "diff", "--name-only", "origin/main...HEAD"], cwd=ROOT, text=True, capture_output=True, check=True)
        assert set(diff.stdout.splitlines()) == AUTHORIZED_FILES
    else:
        assert "exact four-file footprint" in doc_text()
    assert RESOURCE_MATH_MODULE.exists()
