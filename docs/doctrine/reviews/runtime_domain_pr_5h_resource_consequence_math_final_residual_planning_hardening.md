# RUNTIME-DOMAIN-PR-5H: Resource and Consequence Math Final Residual Planning Hardening

Artifact ID: **RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001**.

## 1. Purpose, planning-only status, mandatory sources, and precedence
PR-5H is a planning-only final residual hardening artifact. It closes the eight remaining PR-5G defects: consolidated effective contract inventory; complete CostBundle compatibility surface; exact dependency lifecycle; exact typed-result-scope cardinality and closure; simultaneous blocker precedence; universal source-literal consistency; request/result/proposal validation architecture; and factory/validator parity. It authorizes only **RUNTIME-DOMAIN-PR-5I: Resource and Consequence Math Final Residual Planning Hardening Review Gate** and keeps PR-5A unauthorized and blocked. PRs #278 and #279 were abandoned, were not merged, and are non-authoritative.

Mandatory current-main sources read: PR-5G doctrine and tests; PR-5F doctrine and tests; PR-5D doctrine and tests; PR-5B doctrine and tests; PR-5 service plan; RT002 owner specification; validation_integration.py; transaction_lifecycle.py; event_commitment.py; registry; and decision log. Precedence: PR-5H resolves only explicit PR-5G ambiguities; PR-5F overrides PR-5D only where explicit; PR-5D overrides PR-5B only where explicit; unaffected PR-5B contracts remain inherited.

## 2. Backend-first and non-implementation boundaries
The LLM is not the game engine. Reference objects are not calculations. Results are not state. Settlement proposals are not transactions. No runtime code, domain code, `src/` change, `resource_consequence_math.py`, arithmetic, affordability execution, settlement, mutation, persistence, event append, model authority, UI, conversion, sourcebook inclusion, or canon promotion is authorized. RT-002 owns this planning surface; other RT owners retain their domains.

## 3. Machine-readable effective PR-5H contract
The following YAML block is normative for PR-5H tests and future review.

```yaml pr5h_effective_contract
{
  "artifact_id": "RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001",
  "future_shapes": {
    "ResourceMathSubjectReference": [
      {
        "field": "subject_binding_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "subject_type",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "subject_ref_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "subject_role",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\""
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      }
    ],
    "ResourceReference": [
      {
        "field": "resource_ref_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "subject_binding_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "resource_family",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "resource_key",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "source_label",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "source_aliases",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\""
      },
      {
        "field": "unit_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "dimension_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "source_local",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      }
    ],
    "QuantitySpecification": [
      {
        "field": "quantity_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "representation_kind",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "magnitude_text",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "source_literal",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "precision",
        "annotation": "int | None",
        "default": "None"
      },
      {
        "field": "scale",
        "annotation": "int | None",
        "default": "None"
      },
      {
        "field": "unit_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "dimension_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "conversion_policy",
        "annotation": "str",
        "default": "\"no_conversion\""
      },
      {
        "field": "rounding_policy",
        "annotation": "str",
        "default": "\"no_rounding\""
      },
      {
        "field": "negative_value_policy",
        "annotation": "str",
        "default": "\"negative_values_forbidden\""
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\""
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      }
    ],
    "ResourceMathDependency": [
      {
        "field": "dependency_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "dependency_type",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "reference_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "required",
        "annotation": "bool",
        "default": "True"
      },
      {
        "field": "satisfied",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "hidden_info_safe",
        "annotation": "bool",
        "default": "True"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      }
    ],
    "CostTerm": [
      {
        "field": "term_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "subject_binding_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "resource_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "quantity_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "value_mode",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "policy_route",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "cost_family",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "timing_policy",
        "annotation": "str",
        "default": "\"blocked_pending_validation\""
      },
      {
        "field": "outcome_policy",
        "annotation": "str",
        "default": "\"validation_blocked\""
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\""
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      }
    ],
    "CostBundle": [
      {
        "field": "bundle_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "term_ids",
        "annotation": "tuple[str, ...]",
        "default": "required"
      },
      {
        "field": "atomicity_policy",
        "annotation": "str",
        "default": "\"all_or_nothing_requested\""
      },
      {
        "field": "ordering_policy",
        "annotation": "str",
        "default": "\"unordered_terms\""
      },
      {
        "field": "partial_settlement_policy",
        "annotation": "str",
        "default": "\"no_partial_settlement\""
      },
      {
        "field": "minimum_required_terms",
        "annotation": "int | None",
        "default": "None"
      },
      {
        "field": "maximum_allowed_terms",
        "annotation": "int | None",
        "default": "None"
      },
      {
        "field": "alternative_groups",
        "annotation": "tuple[tuple[str, tuple[str, ...]], ...]",
        "default": "()"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\""
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      }
    ],
    "ConsequenceTerm": [
      {
        "field": "consequence_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "subject_binding_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "resource_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "quantity_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "value_mode",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "policy_route",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "consequence_family",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "timing_policy",
        "annotation": "str",
        "default": "\"blocked_pending_validation\""
      },
      {
        "field": "outcome_policy",
        "annotation": "str",
        "default": "\"validation_blocked\""
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\""
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      }
    ],
    "ResourceMathRequest": [
      {
        "field": "request_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "command_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "action_legality_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "subject_refs",
        "annotation": "tuple[ResourceMathSubjectReference, ...]",
        "default": "required"
      },
      {
        "field": "state_projection_ref_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "resource_refs",
        "annotation": "tuple[ResourceReference, ...]",
        "default": "()"
      },
      {
        "field": "quantity_specs",
        "annotation": "tuple[QuantitySpecification, ...]",
        "default": "()"
      },
      {
        "field": "cost_terms",
        "annotation": "tuple[CostTerm, ...]",
        "default": "()"
      },
      {
        "field": "cost_bundles",
        "annotation": "tuple[CostBundle, ...]",
        "default": "()"
      },
      {
        "field": "consequence_terms",
        "annotation": "tuple[ConsequenceTerm, ...]",
        "default": "()"
      },
      {
        "field": "dependencies",
        "annotation": "tuple[ResourceMathDependency, ...]",
        "default": "()"
      },
      {
        "field": "trace_ref_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "owner_handoff_ref_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "validation_request_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      },
      {
        "field": "calculation_executed",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "affordability_executed",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "reservation_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "settlement_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "consequence_application_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "mutation_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "state_delta_application_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "transaction_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "event_commitment_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "event_append_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "persistence_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "replay_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "rng_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "table_oracle_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "model_authority_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "live_play_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "ui_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "conversion_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "canon_promotion_authorized",
        "annotation": "bool",
        "default": "False"
      }
    ],
    "ResourceMathResult": [
      {
        "field": "result_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "request_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "stage",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "decision",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "blocking",
        "annotation": "bool",
        "default": "required"
      },
      {
        "field": "quarantined",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "escalated",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "diagnostics",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "normalized_reference_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "referenced_subject_binding_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "referenced_resource_ref_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "referenced_quantity_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "referenced_cost_term_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "referenced_cost_bundle_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "referenced_consequence_term_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "referenced_dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "dependencies",
        "annotation": "tuple[ResourceMathDependency, ...]",
        "default": "()"
      },
      {
        "field": "trace_ref_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "validation_request_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "validation_result_ref_id",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "validation_decision",
        "annotation": "str | None",
        "default": "None"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      },
      {
        "field": "calculation_executed",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "affordability_executed",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "reservation_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "settlement_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "consequence_application_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "mutation_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "state_delta_application_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "transaction_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "event_commitment_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "event_append_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "persistence_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "replay_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "rng_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "table_oracle_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "model_authority_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "live_play_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "ui_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "conversion_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "canon_promotion_authorized",
        "annotation": "bool",
        "default": "False"
      }
    ],
    "SettlementProposal": [
      {
        "field": "proposal_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "result_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "proposed_state_delta_refs",
        "annotation": "tuple[str, ...]",
        "default": "required"
      },
      {
        "field": "validation_result_ref_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "validation_decision",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "dependencies",
        "annotation": "tuple[ResourceMathDependency, ...]",
        "default": "()"
      },
      {
        "field": "trace_ref_id",
        "annotation": "str",
        "default": "required"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\""
      },
      {
        "field": "rollback_accounting_refs",
        "annotation": "tuple[str, ...]",
        "default": "()"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})"
      },
      {
        "field": "calculation_executed",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "affordability_executed",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "reservation_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "settlement_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "consequence_application_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "mutation_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "state_delta_application_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "transaction_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "event_commitment_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "event_append_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "persistence_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "replay_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "rng_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "table_oracle_execution_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "model_authority_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "live_play_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "ui_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "conversion_authorized",
        "annotation": "bool",
        "default": "False"
      },
      {
        "field": "canon_promotion_authorized",
        "annotation": "bool",
        "default": "False"
      }
    ]
  },
  "constants": {
    "RESOURCE_MATH_STAGES": [
      "resource_math_requested",
      "source_declaration_captured",
      "subject_refs_bound",
      "resource_refs_declared",
      "quantity_specs_declared",
      "terms_declared",
      "bundle_structure_declared",
      "policy_refs_declared",
      "dependency_refs_bound",
      "calculation_ready_for_review",
      "blocked_pending_validation",
      "blocked_pending_owner_handoff",
      "quarantined_for_review",
      "escalated_to_doctrine"
    ],
    "RESOURCE_MATH_DECISIONS": [
      "accepted_for_planning",
      "normalized_for_planning",
      "source_local_retained",
      "requires_validation_review",
      "requires_owner_handoff",
      "blocked_missing_dependency",
      "blocked_incompatible_policy",
      "blocked_hidden_information",
      "quarantined_for_review",
      "escalated_to_doctrine"
    ],
    "RESOURCE_FAMILIES": [
      "pooled_expendable",
      "scene_counter",
      "charge",
      "currency_like",
      "material",
      "asset_integrity",
      "vehicle_integrity",
      "time_window",
      "opportunity",
      "social_capital",
      "faction_standing",
      "clue_information",
      "risk_heat",
      "strain_corruption",
      "injury_recovery",
      "cooldown",
      "debt_obligation",
      "source_local_resource"
    ],
    "COST_FAMILIES": [
      "activation",
      "upkeep",
      "maintenance",
      "opportunity",
      "prerequisite_lock",
      "reservation_hold",
      "partial_payment",
      "substitution",
      "overcommitment",
      "debt_creation",
      "success_at_cost",
      "failure_at_cost",
      "cancellation",
      "interruption",
      "refund",
      "reversal",
      "compensation",
      "repair",
      "recovery",
      "crafting",
      "salvage",
      "requisition",
      "validation_blocked"
    ],
    "CONSEQUENCE_FAMILIES": [
      "gain",
      "loss",
      "transfer",
      "lock",
      "unlock",
      "exposure",
      "exhaustion",
      "degradation",
      "escalation",
      "cooldown",
      "debt",
      "obligation",
      "harm_pressure",
      "recovery_pressure",
      "visibility_change",
      "mission_route",
      "clue_route",
      "social_faction_change",
      "inventory_asset_change",
      "provenance_recurrence",
      "quarantine_escalation"
    ],
    "COST_TIMING_POLICIES": [
      "pay_before_resolution",
      "reserve_before_resolution",
      "pay_on_attempt",
      "pay_on_success",
      "pay_on_failure",
      "pay_on_commitment",
      "pay_over_time",
      "upkeep_interval",
      "refund_on_cancel",
      "no_refund_on_interrupt",
      "compensate_after_rollback",
      "blocked_pending_validation"
    ],
    "COST_OUTCOME_POLICIES": [
      "success",
      "failure",
      "partial_success",
      "cancelled",
      "interrupted",
      "invalid",
      "validation_blocked",
      "owner_blocked",
      "quarantined",
      "escalated",
      "rollback_required"
    ],
    "QUANTITY_REPRESENTATION_KINDS": [
      "integer_exact",
      "decimal_exact",
      "fraction_exact",
      "fixed_point_scaled",
      "source_literal_only",
      "blocked_pending_numeric_choice"
    ],
    "CONVERSION_POLICIES": [
      "no_conversion",
      "exact_conversion",
      "table_driven_conversion",
      "doctrine_approved_conversion",
      "source_local_conversion",
      "escalation_required"
    ],
    "ROUNDING_POLICIES": [
      "no_rounding",
      "round_down",
      "round_up",
      "round_nearest",
      "round_toward_zero",
      "round_away_from_zero",
      "tie_to_even",
      "tie_away_from_zero",
      "blocked_pending_rounding_choice"
    ],
    "QUANTITY_NEGATIVE_VALUE_POLICIES": [
      "negative_values_forbidden",
      "negative_values_allowed_by_source",
      "negative_values_require_owner_handoff"
    ],
    "VISIBILITY_POLICIES": [
      "public",
      "actor_visible",
      "narrator_only",
      "hidden",
      "redacted",
      "delayed_reveal",
      "derived_only"
    ],
    "RESOURCE_MATH_DEPENDENCY_TYPES": [
      "command_ref",
      "action_legality_ref",
      "state_snapshot_ref",
      "state_record_ref",
      "state_projection_ref",
      "state_delta_ref",
      "transaction_ref",
      "transaction_preview_ref",
      "event_commitment_ref",
      "event_record_ref",
      "validation_request_ref",
      "validation_result_ref",
      "runtime_trace_ref",
      "hidden_information_ref",
      "context_projection_ref",
      "provenance_ref",
      "rng_request_ref",
      "rng_result_ref",
      "table_oracle_ref",
      "table_oracle_result_ref",
      "owner_handoff_ref",
      "registry_ref",
      "decision_log_ref",
      "subject_ref",
      "unit_ref",
      "dimension_ref",
      "resource_math_request_ref",
      "resource_math_result_ref",
      "rollback_accounting_ref"
    ],
    "RESOURCE_MATH_SUBJECT_TYPES": [
      "actor",
      "command",
      "action",
      "item",
      "asset",
      "vehicle",
      "mission",
      "faction",
      "location",
      "state_record",
      "generated_content",
      "resource_owner",
      "source_local_subject",
      "unknown_pending_review"
    ],
    "RESOURCE_MATH_SUBJECT_ROLES": [
      "primary_subject",
      "payer_subject",
      "beneficiary_subject",
      "resource_owner",
      "affected_subject",
      "source_subject",
      "target_subject",
      "authority_source",
      "provenance_source"
    ],
    "RESOURCE_MATH_OWNER_DOMAINS": [
      "RT001_command_lifecycle_action_legality",
      "RT002_resource_consequence_math",
      "RT003_combat_hazard_damage_recovery",
      "RT004_ability_effect_skill_binding",
      "RT005_context_packet_hidden_information",
      "RT006_mission_reward_clue_routing",
      "RT007_social_faction_actor_knowledge",
      "RT008_generated_content_provenance_recurrence",
      "RT009_runtime_rng_table_oracle",
      "RT010_inventory_item_vehicle_asset",
      "RT011_validation_readiness_tooling",
      "RT012_d_series_promotion_boundary",
      "source_local_owner",
      "doctrine_escalation"
    ],
    "RESOURCE_TERM_VALUE_MODES": [
      "resource_quantity",
      "resource_reference_only",
      "quantity_only",
      "policy_only"
    ],
    "RESOURCE_TERM_POLICY_ROUTES": [
      "owner_handoff_required",
      "quarantine_required",
      "doctrine_escalation_required"
    ],
    "ATOMICITY_POLICIES": [
      "all_or_nothing_requested",
      "best_effort_requested",
      "ordered_partial_allowed",
      "unordered_partial_allowed",
      "alternative_exactly_one",
      "alternative_at_least_one",
      "alternative_at_most_one",
      "alternative_any",
      "invalid_mixed_atomicity",
      "blocked_pending_transaction_policy"
    ],
    "ORDERING_POLICIES": [
      "unordered_terms",
      "source_ordered_terms",
      "dependency_ordered_terms",
      "priority_ordered_terms",
      "blocked_pending_ordering_policy"
    ],
    "PARTIAL_SETTLEMENT_POLICIES": [
      "no_partial_settlement",
      "partial_settlement_allowed",
      "partial_settlement_requires_owner_review",
      "partial_settlement_requires_validation",
      "blocked_pending_settlement_policy"
    ],
    "DECLARATION_PROGRESS_STAGES": [
      "source_declaration_captured",
      "subject_refs_bound",
      "resource_refs_declared",
      "quantity_specs_declared",
      "terms_declared",
      "bundle_structure_declared",
      "policy_refs_declared",
      "dependency_refs_bound",
      "calculation_ready_for_review"
    ],
    "SOURCE_LOCAL_STAGES": [
      "source_declaration_captured",
      "resource_refs_declared",
      "terms_declared",
      "bundle_structure_declared",
      "policy_refs_declared"
    ],
    "VALIDATION_BLOCK_STAGES": [
      "blocked_pending_validation"
    ],
    "OWNER_HANDOFF_STAGES": [
      "blocked_pending_owner_handoff"
    ],
    "MISSING_DEPENDENCY_STAGES": [
      "dependency_refs_bound",
      "blocked_pending_validation",
      "blocked_pending_owner_handoff"
    ],
    "POLICY_BLOCK_STAGES": [
      "policy_refs_declared"
    ],
    "HIDDEN_INFORMATION_BLOCK_STAGES": [
      "dependency_refs_bound",
      "blocked_pending_validation"
    ],
    "QUARANTINE_STAGES": [
      "quarantined_for_review"
    ],
    "ESCALATION_STAGES": [
      "escalated_to_doctrine"
    ],
    "VALIDATION_INTEGRATION_DECISIONS": [
      "validation_ready",
      "validation_passed",
      "validation_failed",
      "validation_needs_review",
      "validation_blocked",
      "validation_not_required"
    ]
  },
  "stage_decision_matrix": {
    "accepted_for_planning": {
      "allowed_stages": [
        "resource_math_requested",
        "calculation_ready_for_review"
      ],
      "blocking": false,
      "quarantined": false,
      "escalated": false
    },
    "normalized_for_planning": {
      "allowed_stages": [
        "source_declaration_captured",
        "subject_refs_bound",
        "resource_refs_declared",
        "quantity_specs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared",
        "dependency_refs_bound",
        "calculation_ready_for_review"
      ],
      "blocking": false,
      "quarantined": false,
      "escalated": false
    },
    "source_local_retained": {
      "allowed_stages": [
        "source_declaration_captured",
        "resource_refs_declared",
        "terms_declared",
        "bundle_structure_declared",
        "policy_refs_declared"
      ],
      "blocking": false,
      "quarantined": false,
      "escalated": false
    },
    "requires_validation_review": {
      "allowed_stages": [
        "blocked_pending_validation"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false
    },
    "requires_owner_handoff": {
      "allowed_stages": [
        "blocked_pending_owner_handoff"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false
    },
    "blocked_missing_dependency": {
      "allowed_stages": [
        "dependency_refs_bound",
        "blocked_pending_validation",
        "blocked_pending_owner_handoff"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false
    },
    "blocked_incompatible_policy": {
      "allowed_stages": [
        "policy_refs_declared"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false
    },
    "blocked_hidden_information": {
      "allowed_stages": [
        "dependency_refs_bound",
        "blocked_pending_validation"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false
    },
    "quarantined_for_review": {
      "allowed_stages": [
        "quarantined_for_review"
      ],
      "blocking": true,
      "quarantined": true,
      "escalated": false
    },
    "escalated_to_doctrine": {
      "allowed_stages": [
        "escalated_to_doctrine"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": true
    }
  },
  "false_only_fields": [
    "calculation_executed",
    "affordability_executed",
    "reservation_authorized",
    "settlement_authorized",
    "consequence_application_authorized",
    "mutation_authorized",
    "state_delta_application_authorized",
    "transaction_execution_authorized",
    "event_commitment_authorized",
    "event_append_authorized",
    "persistence_authorized",
    "replay_authorized",
    "rng_execution_authorized",
    "table_oracle_execution_authorized",
    "model_authority_authorized",
    "live_play_authorized",
    "ui_authorized",
    "conversion_authorized",
    "canon_promotion_authorized"
  ],
  "typed_scope_fields": [
    "referenced_subject_binding_ids",
    "referenced_resource_ref_ids",
    "referenced_quantity_ids",
    "referenced_cost_term_ids",
    "referenced_cost_bundle_ids",
    "referenced_consequence_term_ids",
    "referenced_dependency_ids"
  ],
  "blocker_precedence": [
    "doctrine_escalation",
    "quarantine",
    "hidden_information_block",
    "missing_or_unsatisfied_required_dependency",
    "blocked_numeric_choice_or_incompatible_policy",
    "owner_handoff",
    "validation_review",
    "lawful_source_supported_negative_non_blocking",
    "no_blocker_apply_normal_compatibility_matrix"
  ],
  "dependency_lifecycle_states": {
    "A_complete_binding": "correct type/reference, required=True, satisfied=True",
    "B_incomplete_binding": "correct type/reference, required=True, satisfied=False; structurally valid but not resolution-ready; any scoped result reaching it must be blocked_missing_dependency",
    "C_missing_or_malformed_binding": "missing record, wrong type/reference, duplicate match, or required=False; aggregate invalid before result construction",
    "D_required_unsatisfied_named_dependency": "record exists, required=True, satisfied=False, named by a record or scope; forces blocked_missing_dependency when reached",
    "E_advisory_optional_unsatisfied": "required=False, satisfied=False, unbound, unnamed, and unscoped; may coexist with a non-blocking result but satisfies nothing"
  },
  "dependency_ownership": {
    "request.dependencies": "request/input references",
    "result.dependencies": "request binding, result validation, trace, and result-specific references",
    "proposal.dependencies": "result binding, validation result, state deltas, trace, rollback accounting, and proposal-specific references"
  },
  "term_value_mode_matrix": {
    "resource_quantity": {
      "resource_ref_id": "required",
      "quantity_id": "required",
      "policy_route": "None"
    },
    "resource_reference_only": {
      "resource_ref_id": "required",
      "quantity_id": "None",
      "policy_route": "None"
    },
    "quantity_only": {
      "resource_ref_id": "None",
      "quantity_id": "required",
      "policy_route": "None"
    },
    "policy_only": {
      "resource_ref_id": "None",
      "quantity_id": "None",
      "policy_route": "required RESOURCE_TERM_POLICY_ROUTES"
    }
  },
  "cost_bundle_sets": {
    "ORDERING_DECLARED_SET": [
      "unordered_terms",
      "source_ordered_terms",
      "dependency_ordered_terms",
      "priority_ordered_terms"
    ],
    "ORDERING_ORDERED_SET": [
      "source_ordered_terms",
      "dependency_ordered_terms",
      "priority_ordered_terms"
    ],
    "PARTIAL_REVIEW_SET": [
      "partial_settlement_requires_owner_review",
      "partial_settlement_requires_validation"
    ],
    "ALTERNATIVE_ATOMICITY_SET": [
      "alternative_exactly_one",
      "alternative_at_least_one",
      "alternative_at_most_one",
      "alternative_any"
    ]
  },
  "cost_bundle_matrix": [
    [
      "all_or_nothing_requested",
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement"
      ],
      "absent",
      "valid declaration, no settlement"
    ],
    [
      "all_or_nothing_requested",
      [
        "blocked_pending_ordering_policy"
      ],
      [
        "no_partial_settlement"
      ],
      "absent",
      "blocking review"
    ],
    [
      "best_effort_requested",
      "ORDERING_DECLARED_SET",
      [
        "partial_settlement_allowed"
      ],
      "absent",
      "valid declaration, no settlement"
    ],
    [
      "best_effort_requested",
      "ORDERING_DECLARED_SET",
      "PARTIAL_REVIEW_SET",
      "absent",
      "blocking review; owner or validation route follows the partial policy"
    ],
    [
      "best_effort_requested",
      [
        "blocked_pending_ordering_policy"
      ],
      [
        "partial_settlement_allowed",
        "partial_settlement_requires_owner_review",
        "partial_settlement_requires_validation",
        "blocked_pending_settlement_policy"
      ],
      "absent",
      "blocking review"
    ],
    [
      "ordered_partial_allowed",
      "ORDERING_ORDERED_SET",
      [
        "partial_settlement_allowed"
      ],
      "absent",
      "valid declaration, no settlement"
    ],
    [
      "ordered_partial_allowed",
      "ORDERING_ORDERED_SET",
      "PARTIAL_REVIEW_SET",
      "absent",
      "blocking review; owner or validation route follows the partial policy"
    ],
    [
      "ordered_partial_allowed",
      [
        "blocked_pending_ordering_policy"
      ],
      [
        "partial_settlement_allowed",
        "partial_settlement_requires_owner_review",
        "partial_settlement_requires_validation",
        "blocked_pending_settlement_policy"
      ],
      "absent",
      "blocking review"
    ],
    [
      "unordered_partial_allowed",
      [
        "unordered_terms"
      ],
      [
        "partial_settlement_allowed"
      ],
      "absent",
      "valid declaration, no settlement"
    ],
    [
      "unordered_partial_allowed",
      [
        "unordered_terms"
      ],
      "PARTIAL_REVIEW_SET",
      "absent",
      "blocking review; owner or validation route follows the partial policy"
    ],
    [
      "unordered_partial_allowed",
      [
        "blocked_pending_ordering_policy"
      ],
      [
        "partial_settlement_allowed",
        "partial_settlement_requires_owner_review",
        "partial_settlement_requires_validation",
        "blocked_pending_settlement_policy"
      ],
      "absent",
      "blocking review"
    ],
    [
      "alternative_exactly_one",
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement"
      ],
      "present and valid",
      "valid declaration, no alternative chosen"
    ],
    [
      "alternative_at_least_one",
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement"
      ],
      "present and valid",
      "valid declaration, no alternative chosen"
    ],
    [
      "alternative_at_most_one",
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement"
      ],
      "present and valid",
      "valid declaration, no alternative chosen"
    ],
    [
      "alternative_any",
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement"
      ],
      "present and valid",
      "valid declaration, no alternative chosen"
    ],
    [
      "ALTERNATIVE_ATOMICITY_SET",
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement"
      ],
      "absent",
      "invalid: alternative groups required"
    ],
    [
      "ALTERNATIVE_ATOMICITY_SET",
      "ORDERING_DECLARED_SET",
      [
        "partial_settlement_allowed",
        "partial_settlement_requires_owner_review",
        "partial_settlement_requires_validation",
        "blocked_pending_settlement_policy"
      ],
      "present or absent",
      "invalid: alternative atomicity does not use partial settlement"
    ],
    [
      "invalid_mixed_atomicity",
      "any",
      "any",
      "any",
      "invalid"
    ],
    [
      "blocked_pending_transaction_policy",
      "any",
      "any",
      "any",
      "blocking review or invalid until policy is replaced"
    ]
  ],
  "settlement_eligibility": {
    "requires": [
      "result.stage == calculation_ready_for_review",
      "result.decision in {accepted_for_planning, normalized_for_planning}",
      "validation_decision == validation_passed",
      "non-blocking",
      "non-quarantined",
      "non-escalated",
      "every scoped dependency satisfied",
      "no scoped blocker",
      "non-empty unique proposed_state_delta_refs",
      "matching required/satisfied state_delta_ref dependencies"
    ],
    "rejects": [
      "accepted_for_planning at resource_math_requested",
      "normalized_for_planning at earlier declaration stages",
      "source_local_retained",
      "blocked, handoff, review, quarantine, or escalation results",
      "event-only consequences",
      "policy-only terms"
    ]
  },
  "direct_validation_signatures": [
    "create_resource_math_result(*, request: ResourceMathRequest, ...) -> ResourceMathResult",
    "validate_resource_math_result(result: ResourceMathResult, *, request: ResourceMathRequest) -> bool",
    "create_settlement_proposal(*, request: ResourceMathRequest, result: ResourceMathResult, ...) -> SettlementProposal",
    "validate_settlement_proposal(proposal: SettlementProposal, *, request: ResourceMathRequest, result: ResourceMathResult) -> bool"
  ]
}
```

## 4. Consolidated field/default matrix for the ten future shapes
Exactly these ten future frozen keyword-only dataclasses are in scope; no other shape is authorized. `ResourceMathRequest` has no `stage`. `SettlementProposal` has no `request_id`. ResourceMathResult uses the seven `referenced_*` fields exactly; scope-prefixed aliases are forbidden. CostBundle preserves `atomicity_policy`, `ordering_policy`, and `partial_settlement_policy`; no `bundle_policy` replacement is authorized.

### ResourceMathSubjectReference
| field | annotation | default |
|---|---|---|
| `subject_binding_id` | `str` | `required` |
| `subject_type` | `str` | `required` |
| `subject_ref_id` | `str` | `required` |
| `subject_role` | `str` | `required` |
| `owner_domain` | `str` | `required` |
| `visibility_policy` | `str` | `"public"` |
| `provenance_refs` | `tuple[str, ...]` | `()` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |

### ResourceReference
| field | annotation | default |
|---|---|---|
| `resource_ref_id` | `str` | `required` |
| `subject_binding_id` | `str` | `required` |
| `resource_family` | `str` | `required` |
| `resource_key` | `str` | `required` |
| `source_label` | `str | None` | `None` |
| `source_aliases` | `tuple[str, ...]` | `()` |
| `owner_domain` | `str` | `required` |
| `visibility_policy` | `str` | `"public"` |
| `unit_ref_id` | `str | None` | `None` |
| `dimension_ref_id` | `str | None` | `None` |
| `provenance_refs` | `tuple[str, ...]` | `()` |
| `source_local` | `bool` | `False` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |

### QuantitySpecification
| field | annotation | default |
|---|---|---|
| `quantity_id` | `str` | `required` |
| `representation_kind` | `str` | `required` |
| `magnitude_text` | `str | None` | `None` |
| `source_literal` | `str | None` | `None` |
| `precision` | `int | None` | `None` |
| `scale` | `int | None` | `None` |
| `unit_ref_id` | `str | None` | `None` |
| `dimension_ref_id` | `str | None` | `None` |
| `conversion_policy` | `str` | `"no_conversion"` |
| `rounding_policy` | `str` | `"no_rounding"` |
| `negative_value_policy` | `str` | `"negative_values_forbidden"` |
| `visibility_policy` | `str` | `"public"` |
| `provenance_refs` | `tuple[str, ...]` | `()` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |

### ResourceMathDependency
| field | annotation | default |
|---|---|---|
| `dependency_id` | `str` | `required` |
| `dependency_type` | `str` | `required` |
| `reference_id` | `str` | `required` |
| `owner_domain` | `str` | `required` |
| `required` | `bool` | `True` |
| `satisfied` | `bool` | `False` |
| `hidden_info_safe` | `bool` | `True` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |

### CostTerm
| field | annotation | default |
|---|---|---|
| `term_id` | `str` | `required` |
| `subject_binding_id` | `str` | `required` |
| `resource_ref_id` | `str | None` | `None` |
| `quantity_id` | `str | None` | `None` |
| `value_mode` | `str` | `required` |
| `policy_route` | `str | None` | `None` |
| `cost_family` | `str` | `required` |
| `timing_policy` | `str` | `"blocked_pending_validation"` |
| `outcome_policy` | `str` | `"validation_blocked"` |
| `visibility_policy` | `str` | `"public"` |
| `owner_domain` | `str` | `required` |
| `dependency_ids` | `tuple[str, ...]` | `()` |
| `provenance_refs` | `tuple[str, ...]` | `()` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |

### CostBundle
| field | annotation | default |
|---|---|---|
| `bundle_id` | `str` | `required` |
| `term_ids` | `tuple[str, ...]` | `required` |
| `atomicity_policy` | `str` | `"all_or_nothing_requested"` |
| `ordering_policy` | `str` | `"unordered_terms"` |
| `partial_settlement_policy` | `str` | `"no_partial_settlement"` |
| `minimum_required_terms` | `int | None` | `None` |
| `maximum_allowed_terms` | `int | None` | `None` |
| `alternative_groups` | `tuple[tuple[str, tuple[str, ...]], ...]` | `()` |
| `visibility_policy` | `str` | `"public"` |
| `owner_domain` | `str` | `required` |
| `dependency_ids` | `tuple[str, ...]` | `()` |
| `provenance_refs` | `tuple[str, ...]` | `()` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |

### ConsequenceTerm
| field | annotation | default |
|---|---|---|
| `consequence_id` | `str` | `required` |
| `subject_binding_id` | `str` | `required` |
| `resource_ref_id` | `str | None` | `None` |
| `quantity_id` | `str | None` | `None` |
| `value_mode` | `str` | `required` |
| `policy_route` | `str | None` | `None` |
| `consequence_family` | `str` | `required` |
| `timing_policy` | `str` | `"blocked_pending_validation"` |
| `outcome_policy` | `str` | `"validation_blocked"` |
| `visibility_policy` | `str` | `"public"` |
| `owner_domain` | `str` | `required` |
| `dependency_ids` | `tuple[str, ...]` | `()` |
| `provenance_refs` | `tuple[str, ...]` | `()` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |

### ResourceMathRequest
| field | annotation | default |
|---|---|---|
| `request_id` | `str` | `required` |
| `command_ref_id` | `str | None` | `None` |
| `action_legality_ref_id` | `str | None` | `None` |
| `subject_refs` | `tuple[ResourceMathSubjectReference, ...]` | `required` |
| `state_projection_ref_ids` | `tuple[str, ...]` | `()` |
| `resource_refs` | `tuple[ResourceReference, ...]` | `()` |
| `quantity_specs` | `tuple[QuantitySpecification, ...]` | `()` |
| `cost_terms` | `tuple[CostTerm, ...]` | `()` |
| `cost_bundles` | `tuple[CostBundle, ...]` | `()` |
| `consequence_terms` | `tuple[ConsequenceTerm, ...]` | `()` |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` |
| `trace_ref_id` | `str` | `required` |
| `provenance_refs` | `tuple[str, ...]` | `()` |
| `owner_handoff_ref_ids` | `tuple[str, ...]` | `()` |
| `validation_request_ref_id` | `str | None` | `None` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |
| `calculation_executed` | `bool` | `False` |
| `affordability_executed` | `bool` | `False` |
| `reservation_authorized` | `bool` | `False` |
| `settlement_authorized` | `bool` | `False` |
| `consequence_application_authorized` | `bool` | `False` |
| `mutation_authorized` | `bool` | `False` |
| `state_delta_application_authorized` | `bool` | `False` |
| `transaction_execution_authorized` | `bool` | `False` |
| `event_commitment_authorized` | `bool` | `False` |
| `event_append_authorized` | `bool` | `False` |
| `persistence_authorized` | `bool` | `False` |
| `replay_authorized` | `bool` | `False` |
| `rng_execution_authorized` | `bool` | `False` |
| `table_oracle_execution_authorized` | `bool` | `False` |
| `model_authority_authorized` | `bool` | `False` |
| `live_play_authorized` | `bool` | `False` |
| `ui_authorized` | `bool` | `False` |
| `conversion_authorized` | `bool` | `False` |
| `canon_promotion_authorized` | `bool` | `False` |

### ResourceMathResult
| field | annotation | default |
|---|---|---|
| `result_id` | `str` | `required` |
| `request_id` | `str` | `required` |
| `stage` | `str` | `required` |
| `decision` | `str` | `required` |
| `blocking` | `bool` | `required` |
| `quarantined` | `bool` | `False` |
| `escalated` | `bool` | `False` |
| `diagnostics` | `tuple[str, ...]` | `()` |
| `normalized_reference_ids` | `tuple[str, ...]` | `()` |
| `referenced_subject_binding_ids` | `tuple[str, ...]` | `()` |
| `referenced_resource_ref_ids` | `tuple[str, ...]` | `()` |
| `referenced_quantity_ids` | `tuple[str, ...]` | `()` |
| `referenced_cost_term_ids` | `tuple[str, ...]` | `()` |
| `referenced_cost_bundle_ids` | `tuple[str, ...]` | `()` |
| `referenced_consequence_term_ids` | `tuple[str, ...]` | `()` |
| `referenced_dependency_ids` | `tuple[str, ...]` | `()` |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` |
| `trace_ref_id` | `str` | `required` |
| `validation_request_ref_id` | `str | None` | `None` |
| `validation_result_ref_id` | `str | None` | `None` |
| `validation_decision` | `str | None` | `None` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |
| `calculation_executed` | `bool` | `False` |
| `affordability_executed` | `bool` | `False` |
| `reservation_authorized` | `bool` | `False` |
| `settlement_authorized` | `bool` | `False` |
| `consequence_application_authorized` | `bool` | `False` |
| `mutation_authorized` | `bool` | `False` |
| `state_delta_application_authorized` | `bool` | `False` |
| `transaction_execution_authorized` | `bool` | `False` |
| `event_commitment_authorized` | `bool` | `False` |
| `event_append_authorized` | `bool` | `False` |
| `persistence_authorized` | `bool` | `False` |
| `replay_authorized` | `bool` | `False` |
| `rng_execution_authorized` | `bool` | `False` |
| `table_oracle_execution_authorized` | `bool` | `False` |
| `model_authority_authorized` | `bool` | `False` |
| `live_play_authorized` | `bool` | `False` |
| `ui_authorized` | `bool` | `False` |
| `conversion_authorized` | `bool` | `False` |
| `canon_promotion_authorized` | `bool` | `False` |

### SettlementProposal
| field | annotation | default |
|---|---|---|
| `proposal_id` | `str` | `required` |
| `result_id` | `str` | `required` |
| `proposed_state_delta_refs` | `tuple[str, ...]` | `required` |
| `validation_result_ref_id` | `str` | `required` |
| `validation_decision` | `str` | `required` |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` |
| `trace_ref_id` | `str` | `required` |
| `visibility_policy` | `str` | `"public"` |
| `rollback_accounting_refs` | `tuple[str, ...]` | `()` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` |
| `calculation_executed` | `bool` | `False` |
| `affordability_executed` | `bool` | `False` |
| `reservation_authorized` | `bool` | `False` |
| `settlement_authorized` | `bool` | `False` |
| `consequence_application_authorized` | `bool` | `False` |
| `mutation_authorized` | `bool` | `False` |
| `state_delta_application_authorized` | `bool` | `False` |
| `transaction_execution_authorized` | `bool` | `False` |
| `event_commitment_authorized` | `bool` | `False` |
| `event_append_authorized` | `bool` | `False` |
| `persistence_authorized` | `bool` | `False` |
| `replay_authorized` | `bool` | `False` |
| `rng_execution_authorized` | `bool` | `False` |
| `table_oracle_execution_authorized` | `bool` | `False` |
| `model_authority_authorized` | `bool` | `False` |
| `live_play_authorized` | `bool` | `False` |
| `ui_authorized` | `bool` | `False` |
| `conversion_authorized` | `bool` | `False` |
| `canon_promotion_authorized` | `bool` | `False` |

## 5. Controlled constants and source provenance
The constants in the YAML block restate the effective PR-5B/PR-5D/PR-5F controlled surfaces. Provenance: PR-5B supplies baseline stage, decision, resource/cost/consequence, quantity, visibility, owner, subject-type, atomicity, ordering, and partial-settlement surfaces; PR-5D adds subject roles, stage subsets, validation/result/proposal compatibility, and dependency additions; PR-5F adds subject/unit/dimension bindings, request/result/proposal dependency refinements, `RESOURCE_TERM_VALUE_MODES`, `RESOURCE_TERM_POLICY_ROUTES`, precision and source-literal corrections, and corrected CostBundle bounds. Donor-shaped resource families such as `hit_points`, `spell_slots`, `experience_points`, `fate_points`, `action_points`, and `movement_points` are intentionally absent.

## 6. Stage/decision/flag compatibility
Every allowed stage/decision/flag combination is in `stage_decision_matrix`; every unlisted pair is invalid. Quarantine and escalation are terminal planning findings only. Accepted and normalized planning are not executable, transactional, or settlement authority.

## 7. Dependency ownership and lifecycle
Dependency ownership remains separate: `request.dependencies` owns request/input references; `result.dependencies` owns request binding, result validation, trace, and result-specific references; `proposal.dependencies` owns result binding, validation result, state deltas, trace, rollback accounting, and proposal-specific references. No result self-binding is added. Lifecycle states A through E are exact in the YAML block; optional unsatisfied advisory records satisfy nothing.

## 8. Typed result-scope cardinality and closure
The seven exact typed tuples are `referenced_subject_binding_ids`, `referenced_resource_ref_ids`, `referenced_quantity_ids`, `referenced_cost_term_ids`, `referenced_cost_bundle_ids`, `referenced_consequence_term_ids`, and `referenced_dependency_ids`. Each tuple contains unique non-empty IDs; every ID resolves in the supplied request; the combined typed scope cannot be entirely empty; accepted and normalized results require at least one scoped resource, quantity, cost term, cost bundle, or consequence term; subject or advisory dependency scope alone is insufficient; blocked results must scope an actual blocker; blocked_missing_dependency may be dependency-only when an existing request-level required-unsatisfied dependency is the blocker; bundle scope includes all contained terms; term scope includes applicable quantities and dependencies; all scoped references resolve even for blocked, quarantined, or escalated results; normalized_reference_ids remains diagnostic only.

## 9. Deterministic simultaneous-blocker precedence
After structural request validation, PR-5A must apply this precedence: doctrine escalation; quarantine; hidden-information block; missing or unsatisfied required dependency; blocked numeric choice or incompatible policy; owner handoff; validation review; lawful source-supported negative is non-blocking; no blocker applies the normal compatibility matrix. Preserve every detected blocker in diagnostics even when a higher-priority blocker determines the result.

## 10. Complete inherited CostBundle compatibility
The full inherited compatibility matrix, policy sets, and PR-5F bound corrections are in the YAML block. Bool bounds are invalid; supplied bounds are positive integers; minimum and maximum are each `<= len(term_ids)`; minimum is `<= maximum`; all-or-nothing bounds are both `None` or both equal to `len(term_ids)`; PR-5A performs no term selection or alternative selection; alternative groups are unique, contained, and non-overlapping; every unlisted atomicity/ordering/partial-settlement combination is invalid.

## 11. Quantity and universal source-literal rules
`QuantitySpecification.precision` is exactly `int | None = None`; bool precision is invalid; positive precision is declaration metadata only for `decimal_exact`. `source_literal` uses one universal contract wherever it appears, including support for `negative_values_allowed_by_source`: non-empty `str`; one line; no leading/trailing whitespace; no CR, LF, tab, NUL, Unicode `Cc`, or Unicode `Cs`; ordinary Unicode text and interior spaces allowed; preserve exactly; no parsing, normalization, arithmetic, or evaluation. Negative values are lexical by leading `-`, including `-0`, `-0.0`, and `-0/1`.

## 12. Direct request/result/proposal validation architecture
Future signatures are exactly represented in `direct_validation_signatures`: result creation/validation receive the exact request; proposal creation/validation receive the exact request and result. No certificate object, repository lookup, global registry, or `already_validated` boolean may replace direct aggregate validation. Validation order: structurally validate request; validate result against that exact request; verify request/result IDs and dependencies; verify typed scope, closure, blockers, and false-only fields; validate proposal against that exact result and request; verify result/proposal IDs, validation equality, eligibility, dependencies, state-delta refs, and false-only fields.

## 13. SettlementProposal eligibility
Eligibility requires calculation-ready accepted/normalized result, `validation_passed`, non-blocking, non-quarantined, non-escalated posture, every scoped dependency satisfied, no scoped blocker, non-empty unique proposed state-delta refs, and matching required/satisfied `state_delta_ref` dependencies. It rejects accepted planning at `resource_math_requested`, normalized planning at earlier declaration stages, `source_local_retained`, blocked/handoff/review/quarantine/escalation results, event-only consequences, and policy-only terms.

## 14. Factory/validator parity and serialization
Create/validate parity is required for all ten shapes, with identical treatment of manually constructed frozen dataclasses. Factories and validators reject any true false-only field on `ResourceMathRequest`, `ResourceMathResult`, or `SettlementProposal`. Preserve frozen keyword-only future dataclasses, tuple copying, `MappingProxyType` metadata, no callable metadata, internal `to_dict()` only, no `to_public_dict`, defensive serialization, and no calculation during serialization. RT-005 owns public projection and redaction.

## 15. PR-5G closure ledger and corpus-scale owner review
| PR-5G defect | PR-5H closure |
|---|---|
| consolidated effective contract inventory | closed by one ten-shape field/default matrix |
| complete CostBundle compatibility surface | closed by inherited matrix plus PR-5F bounds |
| exact dependency lifecycle | closed by states A-E and ownership split |
| exact typed-result-scope cardinality and closure | closed by seven tuple scope rules |
| simultaneous blocker precedence | closed by deterministic precedence |
| universal source-literal consistency | closed by one source-literal contract |
| request/result/proposal validation architecture | closed by direct aggregate signatures/order |
| factory/validator parity | closed by parity and serialization requirements |

Corpus-scale review remains planning-only: 200-400 donor sources can be represented by typed references, source-local retention, owner handoff, quarantine, escalation, and validation review without turning donor terms into Astra defaults or granting resource math implementation authority.

## 16. PR-5I-only gate classification
```yaml
runtime_domain_pr_5h_classification:
  artifact_type: final_residual_planning_hardening
  planning_only: true
  rt_002_ownership: true
  closes_pr_5g_defects: true
  pr_5a_authorized: false
  pr_5a_blocked: true
  pr_5i_is_sole_next_step: true
  next_step_authorized: RUNTIME-DOMAIN-PR-5I resource and consequence math final residual planning hardening review gate
  next_step_status: review_gate_only
  runtime_code_authorized_by_this_pr: false
  domain_code_authorized_by_this_pr: false
  calculation_authorized_by_this_pr: false
  affordability_execution_authorized_by_this_pr: false
  consequence_application_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  state_mutation_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
```
