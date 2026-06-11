# RUNTIME-DOMAIN-PR-5H: Resource and Consequence Math Final Residual Planning Hardening

Artifact ID: **RUNTIME-DOMAIN-PR-5H-RESOURCE-CONSEQUENCE-MATH-FINAL-RESIDUAL-PLANNING-HARDENING-001**.

## 1. Purpose, planning-only status, mandatory sources, and precedence
PR-5H is a planning-only final residual hardening artifact with an exact four-file footprint. It closes the eight remaining PR-5G defects: consolidated effective contract inventory; complete CostBundle compatibility surface; exact dependency lifecycle; exact typed-result-scope cardinality and closure; simultaneous blocker precedence; universal source-literal consistency; request/result/proposal validation architecture; and factory/validator parity. It authorizes only **RUNTIME-DOMAIN-PR-5I: Resource and Consequence Math Final Residual Planning Hardening Review Gate** and keeps PR-5A unauthorized and blocked. PRs #278 and #279 were abandoned, were not merged, and are non-authoritative.

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
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "subject_type",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_SUBJECT_TYPES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "subject_ref_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "subject_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "subject_role",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_SUBJECT_ROLES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_OWNER_DOMAINS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\"",
        "controlled_surface": "VISIBILITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "provenance_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      }
    ],
    "ResourceReference": [
      {
        "field": "resource_ref_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "subject_binding_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "resource_family",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_FAMILIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "resource_key",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "source_label",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "source_aliases",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_OWNER_DOMAINS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\"",
        "controlled_surface": "VISIBILITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "unit_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "unit_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dimension_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "dimension_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "provenance_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "source_local",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "QuantitySpecification": [
      {
        "field": "quantity_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "representation_kind",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "QUANTITY_REPRESENTATION_KINDS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "magnitude_text",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "ASCII full-string grammar only; no Decimal, Fraction, float, arithmetic, comparison, conversion, rounding, or affordability execution",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "source_literal",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "universal one-line source literal contract; no parsing, normalization, arithmetic, or evaluation",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "precision",
        "annotation": "int | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "positive non-bool int only for decimal_exact; declaration metadata only",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "scale",
        "annotation": "int | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-negative non-bool int only for fixed_point_scaled",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "unit_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "unit_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dimension_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "dimension_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "conversion_policy",
        "annotation": "str",
        "default": "\"no_conversion\"",
        "controlled_surface": "CONVERSION_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "rounding_policy",
        "annotation": "str",
        "default": "\"no_rounding\"",
        "controlled_surface": "ROUNDING_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "negative_value_policy",
        "annotation": "str",
        "default": "\"negative_values_forbidden\"",
        "controlled_surface": "QUANTITY_NEGATIVE_VALUE_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\"",
        "controlled_surface": "VISIBILITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "provenance_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "ResourceMathDependency": [
      {
        "field": "dependency_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dependency_type",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_DEPENDENCY_TYPES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "reference_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_OWNER_DOMAINS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "required",
        "annotation": "bool",
        "default": "True",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "satisfied",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "hidden_info_safe",
        "annotation": "bool",
        "default": "True",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "CostTerm": [
      {
        "field": "term_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "subject_binding_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "resource_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "quantity_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "value_mode",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_TERM_VALUE_MODES",
        "aggregate_owner": "local field",
        "invariant": "required; co-presence matrix controls resource_ref_id, quantity_id, and policy_route",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "policy_route",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "RESOURCE_TERM_POLICY_ROUTES",
        "aggregate_owner": "local field",
        "invariant": "None unless value_mode is policy_only; policy_only requires owner_handoff_required, quarantine_required, or doctrine_escalation_required",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "cost_family",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "COST_FAMILIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "timing_policy",
        "annotation": "str",
        "default": "\"blocked_pending_validation\"",
        "controlled_surface": "COST_TIMING_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "outcome_policy",
        "annotation": "str",
        "default": "\"validation_blocked\"",
        "controlled_surface": "COST_OUTCOME_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\"",
        "controlled_surface": "VISIBILITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_OWNER_DOMAINS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "provenance_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "CostBundle": [
      {
        "field": "bundle_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "term_ids",
        "annotation": "tuple[str, ...]",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "atomicity_policy",
        "annotation": "str",
        "default": "\"all_or_nothing_requested\"",
        "controlled_surface": "ATOMICITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "ordering_policy",
        "annotation": "str",
        "default": "\"unordered_terms\"",
        "controlled_surface": "ORDERING_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "partial_settlement_policy",
        "annotation": "str",
        "default": "\"no_partial_settlement\"",
        "controlled_surface": "PARTIAL_SETTLEMENT_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "minimum_required_terms",
        "annotation": "int | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "positive non-bool int when supplied; <= len(term_ids); <= maximum when maximum supplied",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "maximum_allowed_terms",
        "annotation": "int | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "positive non-bool int when supplied; <= len(term_ids); >= minimum when minimum supplied",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "alternative_groups",
        "annotation": "tuple[tuple[str, tuple[str, ...]], ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "unique groups; contained non-overlapping term IDs; no alternative selection in PR-5A",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\"",
        "controlled_surface": "VISIBILITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_OWNER_DOMAINS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "provenance_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "ConsequenceTerm": [
      {
        "field": "consequence_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "subject_binding_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "resource_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "quantity_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "value_mode",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_TERM_VALUE_MODES",
        "aggregate_owner": "local field",
        "invariant": "required; co-presence matrix controls resource_ref_id, quantity_id, and policy_route",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "policy_route",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "RESOURCE_TERM_POLICY_ROUTES",
        "aggregate_owner": "local field",
        "invariant": "None unless value_mode is policy_only; policy_only requires owner_handoff_required, quarantine_required, or doctrine_escalation_required",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "consequence_family",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "CONSEQUENCE_FAMILIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "timing_policy",
        "annotation": "str",
        "default": "\"blocked_pending_validation\"",
        "controlled_surface": "COST_TIMING_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "outcome_policy",
        "annotation": "str",
        "default": "\"validation_blocked\"",
        "controlled_surface": "COST_OUTCOME_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\"",
        "controlled_surface": "VISIBILITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "owner_domain",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_OWNER_DOMAINS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "provenance_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "ResourceMathRequest": [
      {
        "field": "request_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "result binds exact supplied request; not a SettlementProposal field",
        "external_dependency_type": "resource_math_request_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "command_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "command_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "action_legality_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "action_legality_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "subject_refs",
        "annotation": "tuple[ResourceMathSubjectReference, ...]",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty tuple; exactly one primary_subject; subject_binding_id values unique in request",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5D",
        "replacement_artifact": "none"
      },
      {
        "field": "state_projection_ref_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "state_projection_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "resource_refs",
        "annotation": "tuple[ResourceReference, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "same-request resource_ref_id uniqueness; subject_binding_id resolves to request.subject_refs",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "quantity_specs",
        "annotation": "tuple[QuantitySpecification, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "same-request quantity_id uniqueness; lexical-only quantity validation",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "cost_terms",
        "annotation": "tuple[CostTerm, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "same-request term_id uniqueness; subject/resource/quantity/dependency references resolve",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "cost_bundles",
        "annotation": "tuple[CostBundle, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "same-request bundle_id uniqueness; bundle matrix and bound rules apply",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "consequence_terms",
        "annotation": "tuple[ConsequenceTerm, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "same-request consequence_id uniqueness; no consequence application",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dependencies",
        "annotation": "tuple[ResourceMathDependency, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "dependency_id unique; (dependency_type, reference_id) unique within owning aggregate; lifecycle states A-E apply",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "trace_ref_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "required runtime_trace_ref external binding",
        "external_dependency_type": "runtime_trace_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "provenance_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "provenance_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "owner_handoff_ref_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "owner_handoff_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "validation_request_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "validation_request_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "calculation_executed",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "affordability_executed",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "reservation_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "settlement_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "consequence_application_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "mutation_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "state_delta_application_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "transaction_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "event_commitment_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "event_append_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "persistence_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "replay_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "rng_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "table_oracle_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "model_authority_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "live_play_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "ui_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "conversion_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "canon_promotion_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "ResourceMathResult": [
      {
        "field": "result_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "proposal binds exact supplied result",
        "external_dependency_type": "resource_math_result_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "request_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "result binds exact supplied request; not a SettlementProposal field",
        "external_dependency_type": "resource_math_request_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "stage",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_STAGES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "decision",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "RESOURCE_MATH_DECISIONS",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "blocking",
        "annotation": "bool",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "quarantined",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "escalated",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "diagnostics",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "normalized_reference_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "referenced_subject_binding_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "referenced_resource_ref_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "referenced_quantity_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "referenced_cost_term_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "referenced_cost_bundle_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "referenced_consequence_term_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "referenced_dependency_ids",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "tuple copied; unique non-empty ids where references are carried",
        "external_dependency_type": "none",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5F explicit replacement/addition",
        "replacement_artifact": "PR-5F"
      },
      {
        "field": "dependencies",
        "annotation": "tuple[ResourceMathDependency, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "dependency_id unique; (dependency_type, reference_id) unique within owning aggregate; lifecycle states A-E apply",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "trace_ref_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "required runtime_trace_ref external binding",
        "external_dependency_type": "runtime_trace_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "validation_request_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "validation_request_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "validation_result_ref_id",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "validation_result_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "validation_decision",
        "annotation": "str | None",
        "default": "None",
        "controlled_surface": "VALIDATION_INTEGRATION_DECISIONS",
        "aggregate_owner": "local field",
        "invariant": "validation co-presence with validation request/result refs; proposal requires validation_passed",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "calculation_executed",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "affordability_executed",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "reservation_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "settlement_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "consequence_application_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "mutation_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "state_delta_application_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "transaction_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "event_commitment_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "event_append_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "persistence_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "replay_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "rng_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "table_oracle_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "model_authority_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "live_play_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "ui_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "conversion_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "canon_promotion_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      }
    ],
    "SettlementProposal": [
      {
        "field": "proposal_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "same-aggregate internal reference",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "result_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "proposal binds exact supplied result",
        "external_dependency_type": "resource_math_result_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "proposed_state_delta_refs",
        "annotation": "tuple[str, ...]",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "required non-empty unique tuple; each ref has required/satisfied state_delta_ref dependency",
        "external_dependency_type": "state_delta_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "validation_result_ref_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "validation_result_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "validation_decision",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "VALIDATION_INTEGRATION_DECISIONS",
        "aggregate_owner": "local field",
        "invariant": "validation co-presence with validation request/result refs; proposal requires validation_passed",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "dependencies",
        "annotation": "tuple[ResourceMathDependency, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "local field",
        "invariant": "dependency_id unique; (dependency_type, reference_id) unique within owning aggregate; lifecycle states A-E apply",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "trace_ref_id",
        "annotation": "str",
        "default": "required",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "required runtime_trace_ref external binding",
        "external_dependency_type": "runtime_trace_ref",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "visibility_policy",
        "annotation": "str",
        "default": "\"public\"",
        "controlled_surface": "VISIBILITY_POLICIES",
        "aggregate_owner": "local field",
        "invariant": "non-empty when required; exact annotation/default enforced",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; defensive scalar copy; no public projection authority",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "rollback_accounting_refs",
        "annotation": "tuple[str, ...]",
        "default": "()",
        "controlled_surface": "none",
        "aggregate_owner": "external dependency binding",
        "invariant": "tuple; each supplied ref has rollback_accounting_ref dependency",
        "external_dependency_type": "rollback_accounting_ref",
        "serialization_posture": "tuple copied internally; copied list in internal to_dict",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "metadata",
        "annotation": "Mapping[str, object]",
        "default": "MappingProxyType({})",
        "controlled_surface": "none",
        "aggregate_owner": "local metadata",
        "invariant": "defensive MappingProxyType copy; no callable metadata",
        "external_dependency_type": "none",
        "serialization_posture": "defensive dict copy in internal to_dict; MappingProxyType internally",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "calculation_executed",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "affordability_executed",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "reservation_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "settlement_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "consequence_application_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "mutation_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "state_delta_application_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "transaction_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "event_commitment_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "event_append_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "persistence_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "replay_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "rng_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "table_oracle_execution_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "model_authority_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "live_play_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "ui_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "conversion_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
      },
      {
        "field": "canon_promotion_authorized",
        "annotation": "bool",
        "default": "False",
        "controlled_surface": "none",
        "aggregate_owner": "aggregate false-only authority",
        "invariant": "false-only authority field; factories and validators reject True including manual frozen dataclasses",
        "external_dependency_type": "none",
        "serialization_posture": "internal to_dict only; preserved false; no public projection",
        "source_artifact": "PR-5B inherited",
        "replacement_artifact": "none"
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
    "QUANTITY_KINDS": [
      "count",
      "pool_amount",
      "delta",
      "ratio",
      "percentage",
      "duration",
      "interval",
      "threshold",
      "capacity",
      "rank",
      "tier",
      "charge_count",
      "currency_amount",
      "material_amount",
      "durability_amount",
      "debt_amount",
      "source_literal_quantity",
      "unknown_pending_review"
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
      "rejected_by_missing_command_ref",
      "rejected_by_missing_state_ref",
      "rejected_by_missing_transaction_ref",
      "rejected_by_missing_event_commitment_ref",
      "rejected_by_missing_invariant_set",
      "rejected_by_hidden_information_risk",
      "rejected_by_provenance_gap",
      "rejected_by_schema_mismatch",
      "rejected_by_authority_mismatch",
      "rejected_by_phase_boundary",
      "quarantined_for_review",
      "escalated_to_doctrine",
      "unsupported_validation_scope"
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
      "invalid: alternatives cannot also declare partial settlement in PR-5A"
    ],
    [
      "invalid_mixed_atomicity",
      "ORDERING_DECLARED_SET or { \"blocked_pending_ordering_policy\" }",
      [
        "no_partial_settlement",
        "partial_settlement_allowed",
        "partial_settlement_requires_owner_review",
        "partial_settlement_requires_validation",
        "blocked_pending_settlement_policy"
      ],
      "present or absent",
      "invalid mixed atomicity"
    ],
    [
      "blocked_pending_transaction_policy",
      "ORDERING_DECLARED_SET or { \"blocked_pending_ordering_policy\" }",
      [
        "no_partial_settlement",
        "partial_settlement_allowed",
        "partial_settlement_requires_owner_review",
        "partial_settlement_requires_validation",
        "blocked_pending_settlement_policy"
      ],
      "present or absent",
      "blocking owner/transaction-policy review"
    ],
    [
      [
        "all_or_nothing_requested",
        "best_effort_requested",
        "ordered_partial_allowed",
        "unordered_partial_allowed"
      ],
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement",
        "partial_settlement_allowed",
        "partial_settlement_requires_owner_review",
        "partial_settlement_requires_validation",
        "blocked_pending_settlement_policy"
      ],
      "overlapping groups",
      "invalid: non-alternative atomicity cannot declare alternative groups"
    ],
    [
      "ALTERNATIVE_ATOMICITY_SET",
      "ORDERING_DECLARED_SET",
      [
        "no_partial_settlement"
      ],
      "overlapping groups",
      "invalid unless a future explicit policy authorizes overlap"
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
  ],
  "constant_provenance": {
    "QUANTITY_KINDS": {
      "origin": "PR-5B",
      "pr_5d_replacement": "none",
      "pr_5f_replacement": "none",
      "pr_5h_change": "none"
    }
  },
  "cost_bundle_bound_corrections": [
    "minimum_required_terms <= len(term_ids)",
    "maximum_allowed_terms <= len(term_ids)",
    "minimum_required_terms <= maximum_allowed_terms when both supplied",
    "all_or_nothing_requested bounds both None or both equal len(term_ids)",
    "no selection or settlement execution in PR-5A"
  ],
  "simultaneous_blocker_table": [
    {
      "precedence": 1,
      "trigger": "policy_route == doctrine_escalation_required or doctrine escalation route detected",
      "aggregate_validity_prerequisite": "structural request valid; malformed/missing binding State C already rejected",
      "exact_decision": "escalated_to_doctrine",
      "exact_stage_or_allowed_stage_set": [
        "escalated_to_doctrine"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": true,
      "required_dependency": "none unless referenced fields independently require bindings",
      "diagnostics_rule": "preserve lower-priority blockers in diagnostics"
    },
    {
      "precedence": 2,
      "trigger": "policy_route == quarantine_required or quarantine route detected",
      "aggregate_validity_prerequisite": "structural request valid; malformed/missing binding State C already rejected",
      "exact_decision": "quarantined_for_review",
      "exact_stage_or_allowed_stage_set": [
        "quarantined_for_review"
      ],
      "blocking": true,
      "quarantined": true,
      "escalated": false,
      "required_dependency": "none unless referenced fields independently require bindings",
      "diagnostics_rule": "preserve lower-priority blockers in diagnostics"
    },
    {
      "precedence": 3,
      "trigger": "hidden_info_safe=False on a scoped dependency or hidden-information blocker",
      "aggregate_validity_prerequisite": "structural request valid; scoped dependency resolves",
      "exact_decision": "blocked_hidden_information",
      "exact_stage_or_allowed_stage_set": [
        "dependency_refs_bound",
        "blocked_pending_validation"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false,
      "required_dependency": "hidden_information_ref or context_projection_ref when external hidden-information evidence is referenced",
      "diagnostics_rule": "preserve lower-priority blockers in diagnostics"
    },
    {
      "precedence": 4,
      "trigger": "State B incomplete binding or State D required-unsatisfied named dependency reached by scope",
      "aggregate_validity_prerequisite": "State C missing/malformed binding rejected before result construction",
      "exact_decision": "blocked_missing_dependency",
      "exact_stage_or_allowed_stage_set": [
        "dependency_refs_bound",
        "blocked_pending_validation",
        "blocked_pending_owner_handoff"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false,
      "required_dependency": "the reached dependency record exists with required=True and satisfied=False",
      "diagnostics_rule": "record all missing/unsatisfied dependency blockers and preserve lower-priority blockers"
    },
    {
      "precedence": 5,
      "trigger": "blocked_pending_numeric_choice or incompatible policy in typed scope",
      "aggregate_validity_prerequisite": "structural request valid; quantity/term/bundle resolves",
      "exact_decision": "blocked_incompatible_policy",
      "exact_stage_or_allowed_stage_set": [
        "policy_refs_declared"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false,
      "required_dependency": "none beyond dependencies named by scoped records",
      "diagnostics_rule": "preserve lower-priority blockers in diagnostics"
    },
    {
      "precedence": 6,
      "trigger": "negative_values_require_owner_handoff or policy_route == owner_handoff_required",
      "aggregate_validity_prerequisite": "structural request valid; owner-handoff reference bindings resolve",
      "exact_decision": "requires_owner_handoff",
      "exact_stage_or_allowed_stage_set": [
        "blocked_pending_owner_handoff"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false,
      "required_dependency": "owner_handoff_ref required and satisfied for each owner handoff reference",
      "diagnostics_rule": "preserve lower-priority blockers in diagnostics"
    },
    {
      "precedence": 7,
      "trigger": "validation review required by validation co-presence or partial-settlement validation route",
      "aggregate_validity_prerequisite": "structural request valid; validation request binding resolves",
      "exact_decision": "requires_validation_review",
      "exact_stage_or_allowed_stage_set": [
        "blocked_pending_validation"
      ],
      "blocking": true,
      "quarantined": false,
      "escalated": false,
      "required_dependency": "validation_request_ref required and satisfied; validation_result_ref absent until result exists",
      "diagnostics_rule": "preserve lower-priority blockers in diagnostics"
    },
    {
      "precedence": 8,
      "trigger": "negative_values_allowed_by_source with valid source_literal and provenance bindings",
      "aggregate_validity_prerequisite": "structural request valid; provenance dependencies required/satisfied",
      "exact_decision": "non_blocking_no_decision_override",
      "exact_stage_or_allowed_stage_set": "ordinary compatibility matrix",
      "blocking": false,
      "quarantined": false,
      "escalated": false,
      "required_dependency": "provenance_ref required and satisfied for each provenance ref",
      "diagnostics_rule": "diagnostic note allowed; does not block or override higher-priority blockers"
    },
    {
      "precedence": 9,
      "trigger": "no blocker detected",
      "aggregate_validity_prerequisite": "structural request valid and typed scope closed",
      "exact_decision": "ordinary compatibility matrix",
      "exact_stage_or_allowed_stage_set": "ordinary compatibility matrix",
      "blocking": "ordinary compatibility matrix",
      "quarantined": "ordinary compatibility matrix",
      "escalated": "ordinary compatibility matrix",
      "required_dependency": "all scoped required dependencies satisfied",
      "diagnostics_rule": "normal diagnostics only"
    }
  ],
  "quantity_lexical_grammars": {
    "integer_exact": {
      "required_lexical_fields": [
        "magnitude_text"
      ],
      "exact_grammar": "^[+-]?(0|[1-9][0-9]*)$",
      "explicit_exclusions": "no whitespace, exponent notation, decimal point, leading zero except `0`, or embedded separators"
    },
    "decimal_exact": {
      "required_lexical_fields": [
        "magnitude_text"
      ],
      "exact_grammar": "^[+-]?(0|[1-9][0-9]*)\\.[0-9]+$",
      "explicit_exclusions": "no exponent notation, leading decimal point, trailing decimal point, leading zero except before `.`, or embedded separators"
    },
    "fraction_exact": {
      "required_lexical_fields": [
        "magnitude_text"
      ],
      "exact_grammar": "^[+-]?(0|[1-9][0-9]*)/[1-9][0-9]*$",
      "explicit_exclusions": "no zero denominator, signed denominator, decimal numerator, decimal denominator, or mixed-number shorthand"
    },
    "fixed_point_scaled": {
      "required_lexical_fields": [
        "magnitude_text",
        "scale"
      ],
      "exact_grammar": "magnitude ^[+-]?(0|[1-9][0-9]*)$; scale is an int that is not bool and is >= 0",
      "explicit_exclusions": "no decimal point in magnitude, no exponent notation, no negative scale"
    },
    "source_literal_only": {
      "required_lexical_fields": [
        "source_literal"
      ],
      "exact_grammar": "^\\S(?:.*\\S)?$ plus universal source_literal character contract",
      "explicit_exclusions": "no empty string, no leading/trailing whitespace, no evaluation"
    },
    "blocked_pending_numeric_choice": {
      "required_lexical_fields": [
        "source_literal"
      ],
      "exact_grammar": "^\\S(?:.*\\S)?$ plus universal source_literal character contract",
      "explicit_exclusions": "no empty string, no leading/trailing whitespace, blocks progression"
    }
  },
  "quantity_execution_bans": [
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
    "scale non-negative and fixed_point_scaled only"
  ],
  "public_helpers": [
    "create_resource_math_subject_reference",
    "validate_resource_math_subject_reference",
    "create_resource_reference",
    "validate_resource_reference",
    "create_quantity_specification",
    "validate_quantity_specification",
    "create_resource_math_dependency",
    "validate_resource_math_dependency",
    "create_cost_term",
    "validate_cost_term",
    "create_cost_bundle",
    "validate_cost_bundle",
    "create_consequence_term",
    "validate_consequence_term",
    "create_resource_math_request",
    "validate_resource_math_request",
    "create_resource_math_result",
    "validate_resource_math_result",
    "create_settlement_proposal",
    "validate_settlement_proposal"
  ],
  "private_helper_responsibilities": [
    "constants/defaults",
    "subject identity",
    "internal refs",
    "external bindings",
    "dependency lifecycle",
    "typed scope",
    "blocker precedence",
    "quantity grammar",
    "source literals",
    "negative policies",
    "term modes/routes",
    "bundle matrix",
    "request/result validation",
    "proposal/request/result validation",
    "false-only fields",
    "tuple/metadata immutability",
    "internal serialization"
  ],
  "authority_false_fields": [
    "runtime_code_authorized_by_this_pr",
    "domain_code_authorized_by_this_pr",
    "calculation_authorized_by_this_pr",
    "affordability_execution_authorized_by_this_pr",
    "reservation_authorized_by_this_pr",
    "settlement_authorized_by_this_pr",
    "consequence_application_authorized_by_this_pr",
    "mutation_authorized_by_this_pr",
    "state_delta_application_authorized_by_this_pr",
    "transaction_execution_authorized_by_this_pr",
    "event_commitment_authorized_by_this_pr",
    "event_append_authorized_by_this_pr",
    "persistence_authorized_by_this_pr",
    "replay_authorized_by_this_pr",
    "rng_execution_authorized_by_this_pr",
    "table_oracle_execution_authorized_by_this_pr",
    "model_authority_authorized_by_this_pr",
    "model_integration_authorized_by_this_pr",
    "live_play_authorized_by_this_pr",
    "ui_authorized_by_this_pr",
    "conversion_authorized_by_this_pr",
    "canon_promotion_authorized_by_this_pr"
  ]
}
```

## 4. Consolidated field/default matrix for the ten future shapes
Exactly these ten future frozen keyword-only dataclasses are in scope; no other shape is authorized. `ResourceMathRequest` has no `stage`. `SettlementProposal` has no `request_id`. ResourceMathResult uses the seven `referenced_*` fields exactly; scope-prefixed aliases are forbidden. CostBundle preserves `atomicity_policy`, `ordering_policy`, and `partial_settlement_policy`; no `bundle_policy` replacement is authorized. Every row is a complete future field contract and includes controlled surface, ownership, invariant, external dependency type, serialization posture, source artifact, and replacement artifact.
### ResourceMathSubjectReference
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `subject_binding_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `subject_type` | `str` | `required` | `RESOURCE_MATH_SUBJECT_TYPES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `subject_ref_id` | `str` | `required` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `subject_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `subject_role` | `str` | `required` | `RESOURCE_MATH_SUBJECT_ROLES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `owner_domain` | `str` | `required` | `RESOURCE_MATH_OWNER_DOMAINS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `provenance_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `provenance_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5D` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5D` | `none` |

### ResourceReference
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `resource_ref_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `subject_binding_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `resource_family` | `str` | `required` | `RESOURCE_FAMILIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `resource_key` | `str` | `required` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `source_label` | `str \| None` | `None` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `source_aliases` | `tuple[str, ...]` | `()` | `none` | `local field` | `tuple copied; unique non-empty ids where references are carried` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `owner_domain` | `str` | `required` | `RESOURCE_MATH_OWNER_DOMAINS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `unit_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `unit_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dimension_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `dimension_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `provenance_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `provenance_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `source_local` | `bool` | `False` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |

### QuantitySpecification
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `quantity_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `representation_kind` | `str` | `required` | `QUANTITY_REPRESENTATION_KINDS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `magnitude_text` | `str \| None` | `None` | `none` | `local field` | `ASCII full-string grammar only; no Decimal, Fraction, float, arithmetic, comparison, conversion, rounding, or affordability execution` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `source_literal` | `str \| None` | `None` | `none` | `local field` | `universal one-line source literal contract; no parsing, normalization, arithmetic, or evaluation` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `precision` | `int \| None` | `None` | `none` | `local field` | `positive non-bool int only for decimal_exact; declaration metadata only` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `scale` | `int \| None` | `None` | `none` | `local field` | `non-negative non-bool int only for fixed_point_scaled` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `unit_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `unit_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dimension_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `dimension_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `conversion_policy` | `str` | `"no_conversion"` | `CONVERSION_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `rounding_policy` | `str` | `"no_rounding"` | `ROUNDING_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `negative_value_policy` | `str` | `"negative_values_forbidden"` | `QUANTITY_NEGATIVE_VALUE_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `provenance_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `provenance_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |

### ResourceMathDependency
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `dependency_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dependency_type` | `str` | `required` | `RESOURCE_MATH_DEPENDENCY_TYPES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `reference_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `owner_domain` | `str` | `required` | `RESOURCE_MATH_OWNER_DOMAINS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `required` | `bool` | `True` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `satisfied` | `bool` | `False` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `hidden_info_safe` | `bool` | `True` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |

### CostTerm
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `term_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `subject_binding_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `resource_ref_id` | `str \| None` | `None` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `quantity_id` | `str \| None` | `None` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `value_mode` | `str` | `required` | `RESOURCE_TERM_VALUE_MODES` | `local field` | `required; co-presence matrix controls resource_ref_id, quantity_id, and policy_route` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `policy_route` | `str \| None` | `None` | `RESOURCE_TERM_POLICY_ROUTES` | `local field` | `None unless value_mode is policy_only; policy_only requires owner_handoff_required, quarantine_required, or doctrine_escalation_required` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `cost_family` | `str` | `required` | `COST_FAMILIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `timing_policy` | `str` | `"blocked_pending_validation"` | `COST_TIMING_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `outcome_policy` | `str` | `"validation_blocked"` | `COST_OUTCOME_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `owner_domain` | `str` | `required` | `RESOURCE_MATH_OWNER_DOMAINS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dependency_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `provenance_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `provenance_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |

### CostBundle
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `bundle_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `term_ids` | `tuple[str, ...]` | `required` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `atomicity_policy` | `str` | `"all_or_nothing_requested"` | `ATOMICITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `ordering_policy` | `str` | `"unordered_terms"` | `ORDERING_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `partial_settlement_policy` | `str` | `"no_partial_settlement"` | `PARTIAL_SETTLEMENT_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `minimum_required_terms` | `int \| None` | `None` | `none` | `local field` | `positive non-bool int when supplied; <= len(term_ids); <= maximum when maximum supplied` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `maximum_allowed_terms` | `int \| None` | `None` | `none` | `local field` | `positive non-bool int when supplied; <= len(term_ids); >= minimum when minimum supplied` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `alternative_groups` | `tuple[tuple[str, tuple[str, ...]], ...]` | `()` | `none` | `local field` | `unique groups; contained non-overlapping term IDs; no alternative selection in PR-5A` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `owner_domain` | `str` | `required` | `RESOURCE_MATH_OWNER_DOMAINS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dependency_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `provenance_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `provenance_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |

### ConsequenceTerm
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `consequence_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `subject_binding_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5D` | `none` |
| `resource_ref_id` | `str \| None` | `None` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `quantity_id` | `str \| None` | `None` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `value_mode` | `str` | `required` | `RESOURCE_TERM_VALUE_MODES` | `local field` | `required; co-presence matrix controls resource_ref_id, quantity_id, and policy_route` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `policy_route` | `str \| None` | `None` | `RESOURCE_TERM_POLICY_ROUTES` | `local field` | `None unless value_mode is policy_only; policy_only requires owner_handoff_required, quarantine_required, or doctrine_escalation_required` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `consequence_family` | `str` | `required` | `CONSEQUENCE_FAMILIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `timing_policy` | `str` | `"blocked_pending_validation"` | `COST_TIMING_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `outcome_policy` | `str` | `"validation_blocked"` | `COST_OUTCOME_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `owner_domain` | `str` | `required` | `RESOURCE_MATH_OWNER_DOMAINS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dependency_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `provenance_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `provenance_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |

### ResourceMathRequest
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `request_id` | `str` | `required` | `none` | `external dependency binding` | `result binds exact supplied request; not a SettlementProposal field` | `resource_math_request_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `command_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `command_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `action_legality_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `action_legality_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `subject_refs` | `tuple[ResourceMathSubjectReference, ...]` | `required` | `none` | `same-aggregate internal reference` | `non-empty tuple; exactly one primary_subject; subject_binding_id values unique in request` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5D` | `none` |
| `state_projection_ref_ids` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `state_projection_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `resource_refs` | `tuple[ResourceReference, ...]` | `()` | `none` | `same-aggregate internal reference` | `same-request resource_ref_id uniqueness; subject_binding_id resolves to request.subject_refs` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `quantity_specs` | `tuple[QuantitySpecification, ...]` | `()` | `none` | `same-aggregate internal reference` | `same-request quantity_id uniqueness; lexical-only quantity validation` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `cost_terms` | `tuple[CostTerm, ...]` | `()` | `none` | `same-aggregate internal reference` | `same-request term_id uniqueness; subject/resource/quantity/dependency references resolve` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `cost_bundles` | `tuple[CostBundle, ...]` | `()` | `none` | `same-aggregate internal reference` | `same-request bundle_id uniqueness; bundle matrix and bound rules apply` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `consequence_terms` | `tuple[ConsequenceTerm, ...]` | `()` | `none` | `same-aggregate internal reference` | `same-request consequence_id uniqueness; no consequence application` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` | `none` | `local field` | `dependency_id unique; (dependency_type, reference_id) unique within owning aggregate; lifecycle states A-E apply` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `trace_ref_id` | `str` | `required` | `none` | `external dependency binding` | `required runtime_trace_ref external binding` | `runtime_trace_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `provenance_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `provenance_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `owner_handoff_ref_ids` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple copied; unique non-empty ids where references are carried` | `owner_handoff_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `validation_request_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `validation_request_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |
| `calculation_executed` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `affordability_executed` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `reservation_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `settlement_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `consequence_application_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `mutation_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `state_delta_application_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `transaction_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `event_commitment_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `event_append_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `persistence_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `replay_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `rng_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `table_oracle_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `model_authority_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `live_play_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `ui_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `conversion_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `canon_promotion_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |

### ResourceMathResult
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `result_id` | `str` | `required` | `none` | `external dependency binding` | `proposal binds exact supplied result` | `resource_math_result_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `request_id` | `str` | `required` | `none` | `external dependency binding` | `result binds exact supplied request; not a SettlementProposal field` | `resource_math_request_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `stage` | `str` | `required` | `RESOURCE_MATH_STAGES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `decision` | `str` | `required` | `RESOURCE_MATH_DECISIONS` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `blocking` | `bool` | `required` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `quarantined` | `bool` | `False` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `escalated` | `bool` | `False` | `none` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `diagnostics` | `tuple[str, ...]` | `()` | `none` | `local field` | `tuple copied; unique non-empty ids where references are carried` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `normalized_reference_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `referenced_subject_binding_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `referenced_resource_ref_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `referenced_quantity_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `referenced_cost_term_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `referenced_cost_bundle_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `referenced_consequence_term_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `referenced_dependency_ids` | `tuple[str, ...]` | `()` | `none` | `same-aggregate internal reference` | `tuple copied; unique non-empty ids where references are carried` | `none` | `tuple copied internally; copied list in internal to_dict` | `PR-5F explicit replacement/addition` | `PR-5F` |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` | `none` | `local field` | `dependency_id unique; (dependency_type, reference_id) unique within owning aggregate; lifecycle states A-E apply` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `trace_ref_id` | `str` | `required` | `none` | `external dependency binding` | `required runtime_trace_ref external binding` | `runtime_trace_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `validation_request_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `validation_request_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `validation_result_ref_id` | `str \| None` | `None` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `validation_result_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `validation_decision` | `str \| None` | `None` | `VALIDATION_INTEGRATION_DECISIONS` | `local field` | `validation co-presence with validation request/result refs; proposal requires validation_passed` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |
| `calculation_executed` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `affordability_executed` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `reservation_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `settlement_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `consequence_application_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `mutation_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `state_delta_application_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `transaction_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `event_commitment_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `event_append_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `persistence_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `replay_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `rng_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `table_oracle_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `model_authority_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `live_play_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `ui_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `conversion_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `canon_promotion_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |

### SettlementProposal
| field | annotation | default | controlled_surface | aggregate_owner | invariant | external_dependency_type | serialization_posture | source_artifact | replacement_artifact |
|---|---|---|---|---|---|---|---|---|---|
| `proposal_id` | `str` | `required` | `none` | `same-aggregate internal reference` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `result_id` | `str` | `required` | `none` | `external dependency binding` | `proposal binds exact supplied result` | `resource_math_result_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `proposed_state_delta_refs` | `tuple[str, ...]` | `required` | `none` | `external dependency binding` | `required non-empty unique tuple; each ref has required/satisfied state_delta_ref dependency` | `state_delta_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `validation_result_ref_id` | `str` | `required` | `none` | `external dependency binding` | `non-empty when required; exact annotation/default enforced` | `validation_result_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `validation_decision` | `str` | `required` | `VALIDATION_INTEGRATION_DECISIONS` | `local field` | `validation co-presence with validation request/result refs; proposal requires validation_passed` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `dependencies` | `tuple[ResourceMathDependency, ...]` | `()` | `none` | `local field` | `dependency_id unique; (dependency_type, reference_id) unique within owning aggregate; lifecycle states A-E apply` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `trace_ref_id` | `str` | `required` | `none` | `external dependency binding` | `required runtime_trace_ref external binding` | `runtime_trace_ref` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `visibility_policy` | `str` | `"public"` | `VISIBILITY_POLICIES` | `local field` | `non-empty when required; exact annotation/default enforced` | `none` | `internal to_dict only; defensive scalar copy; no public projection authority` | `PR-5B inherited` | `none` |
| `rollback_accounting_refs` | `tuple[str, ...]` | `()` | `none` | `external dependency binding` | `tuple; each supplied ref has rollback_accounting_ref dependency` | `rollback_accounting_ref` | `tuple copied internally; copied list in internal to_dict` | `PR-5B inherited` | `none` |
| `metadata` | `Mapping[str, object]` | `MappingProxyType({})` | `none` | `local metadata` | `defensive MappingProxyType copy; no callable metadata` | `none` | `defensive dict copy in internal to_dict; MappingProxyType internally` | `PR-5B inherited` | `none` |
| `calculation_executed` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `affordability_executed` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `reservation_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `settlement_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `consequence_application_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `mutation_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `state_delta_application_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `transaction_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `event_commitment_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `event_append_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `persistence_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `replay_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `rng_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `table_oracle_execution_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `model_authority_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `live_play_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `ui_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `conversion_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |
| `canon_promotion_authorized` | `bool` | `False` | `none` | `aggregate false-only authority` | `false-only authority field; factories and validators reject True including manual frozen dataclasses` | `none` | `internal to_dict only; preserved false; no public projection` | `PR-5B inherited` | `none` |

## 5. Controlled constants and source provenance
The constants in the YAML block restate the effective PR-5B/PR-5D/PR-5F controlled surfaces. Provenance: PR-5B supplies baseline stage, decision, resource/cost/consequence, quantity kind, quantity representation, visibility, owner, subject-type, atomicity, ordering, and partial-settlement surfaces; PR-5D adds subject roles, stage subsets, validation/result/proposal compatibility, and dependency additions; PR-5F adds subject/unit/dimension bindings, request/result/proposal dependency refinements, `RESOURCE_TERM_VALUE_MODES`, `RESOURCE_TERM_POLICY_ROUTES`, precision and source-literal corrections, and corrected CostBundle bounds. `QUANTITY_KINDS` origin is PR-5B; there is no PR-5D or PR-5F replacement unless a merged artifact explicitly says otherwise; PR-5H changes it not at all. Donor-shaped resource families such as `hit_points`, `spell_slots`, `experience_points`, `fate_points`, `action_points`, and `movement_points` are intentionally absent.

## 6. Stage/decision/flag compatibility
Every allowed stage/decision/flag combination is in `stage_decision_matrix`; every unlisted pair is invalid. Quarantine and escalation are terminal planning findings only. Accepted and normalized planning are not executable, transactional, or settlement authority. `validation_blocked` belongs to validation-integration surfaces and is not a `ResourceMathResult.decision`.

## 7. Dependency ownership and lifecycle
Dependency ownership remains separate: `request.dependencies` owns request/input references; `result.dependencies` owns request binding, result validation, trace, and result-specific references; `proposal.dependencies` owns result binding, validation result, state deltas, trace, rollback accounting, and proposal-specific references. No result self-binding is added. Lifecycle states A through E are exact in the YAML block; optional unsatisfied advisory records satisfy nothing. Malformed/missing binding State C is rejected before result construction.

## 8. Typed result-scope cardinality and closure
The seven exact typed tuples are `referenced_subject_binding_ids`, `referenced_resource_ref_ids`, `referenced_quantity_ids`, `referenced_cost_term_ids`, `referenced_cost_bundle_ids`, `referenced_consequence_term_ids`, and `referenced_dependency_ids`. Each tuple contains unique non-empty IDs; every ID resolves in the supplied request; the combined typed scope cannot be entirely empty; accepted and normalized results require at least one scoped resource, quantity, cost term, cost bundle, or consequence term; subject or advisory dependency scope alone is insufficient; blocked results must scope an actual blocker; blocked_missing_dependency may be dependency-only when an existing request-level required-unsatisfied dependency is the blocker; bundle scope includes all contained terms; term scope includes applicable quantities and dependencies; all scoped references resolve even for blocked, quarantined, or escalated results; normalized_reference_ids remains diagnostic only.

## 9. Deterministic simultaneous-blocker precedence
The exact simultaneous-blocker table is machine-readable in `simultaneous_blocker_table`. It states that doctrine_escalation_required maps exactly to `escalated_to_doctrine`, quarantine_required maps exactly to `quarantined_for_review`, owner_handoff_required maps exactly to `requires_owner_handoff`, hidden_info_safe=False maps exactly to `blocked_hidden_information`, State B and State D map to `blocked_missing_dependency`, and blocked_pending_numeric_choice maps exactly to `blocked_incompatible_policy` at `policy_refs_declared`. Lower-priority blockers remain in diagnostics even when a higher-priority blocker determines the result.

## 10. Complete inherited CostBundle compatibility
The full inherited PR-5D compatibility matrix, policy sets, and only PR-5F bound corrections are in the YAML block. Bool bounds are invalid; supplied bounds are positive integers; minimum and maximum are each `<= len(term_ids)`; minimum is `<= maximum`; all-or-nothing bounds are both `None` or both equal to `len(term_ids)`; PR-5A performs no selection or settlement execution; alternative groups are unique, contained, and non-overlapping unless later explicitly authorized; every unlisted atomicity/ordering/partial-settlement combination is invalid.

## 11. Quantity and universal source-literal rules
`QuantitySpecification.precision` is exactly `int | None = None`; bool precision is invalid; positive precision is declaration metadata only for `decimal_exact`. `scale` rejects bool, is non-negative, and is allowed only for `fixed_point_scaled`. The exact PR-5D full-string ASCII lexical table is in `quantity_lexical_grammars`. PR-5A performs no Decimal, Fraction, float, exponent notation, arithmetic, comparison, conversion, rounding, or affordability execution. `source_literal` uses one universal contract wherever it appears, including support for `negative_values_allowed_by_source`: non-empty `str`; one line; no leading/trailing whitespace; no CR, LF, tab, NUL, Unicode `Cc`, or Unicode `Cs`; ordinary Unicode text and interior spaces allowed; preserve exactly; no parsing, normalization, arithmetic, or evaluation. Negative values are lexical by leading `-`, including `-0`, `-0.0`, and `-0/1`.

## 12. Direct request/result/proposal validation architecture
Future signatures are exactly represented in `direct_validation_signatures`: result creation/validation receive the exact request; proposal creation/validation receive the exact request and result. No certificate object, repository lookup, global registry, or `already_validated` boolean may replace direct aggregate validation. Validation order: structurally validate request; validate result against that exact request; verify request/result IDs and dependencies; verify typed scope, closure, blockers, and false-only fields; validate proposal against that exact result and request; verify result/proposal IDs, validation equality, eligibility, dependencies, state-delta refs, and false-only fields.

## 13. SettlementProposal eligibility
Eligibility requires calculation-ready accepted/normalized result, `validation_passed`, non-blocking, non-quarantined, non-escalated posture, every scoped dependency satisfied, no scoped blocker, non-empty unique proposed state-delta refs, and matching required/satisfied `state_delta_ref` dependencies. It rejects accepted planning at `resource_math_requested`, normalized planning at earlier declaration stages, `source_local_retained`, blocked/handoff/review/quarantine/escalation results, event-only consequences, and policy-only terms.

## 14. Factory/validator parity and serialization
Create/validate parity is required for all ten shapes through the exact helper list in `public_helpers`; no generic helper sentence substitutes for the twenty public helper names. Private helper responsibilities are exactly listed in `private_helper_responsibilities`. Factories and validators reject any true false-only field on `ResourceMathRequest`, `ResourceMathResult`, or `SettlementProposal`. Preserve frozen keyword-only future dataclasses, tuple copying, `MappingProxyType` metadata, no callable metadata, internal `to_dict()` only, no `to_public_dict`, defensive serialization, and no calculation during serialization. RT-005 owns public projection and redaction.

## 15. PR-5G closure ledger and corpus-scale owner review
| PR-5G defect | PR-5H closure |
|---|---|
| consolidated effective contract inventory | closed by one complete ten-shape field/default/ownership/dependency/serialization matrix |
| complete CostBundle compatibility surface | closed by the inherited PR-5D matrix plus only PR-5F bound corrections |
| exact dependency lifecycle | closed by states A-E and ownership split |
| exact typed-result-scope cardinality and closure | closed by seven tuple scope rules |
| simultaneous blocker precedence | closed by machine-readable precedence table |
| universal source-literal consistency | closed by one source-literal contract plus exact lexical grammars |
| request/result/proposal validation architecture | closed by direct aggregate signatures/order |
| factory/validator parity | closed by explicit helper list and private-helper responsibility list |

Corpus-pressure destinations without adopting donor law:

- Fantasy resources, costs, and consequences may be declared as typed references, quantities, source-local records, owner-handoff records, quarantine, or doctrine escalation; PR-5H does not create hit points, spell slots, fate points, or action points.
- Science-fiction energy, ammo, shields, starship, cybernetic, or logistics terms may declare resource references and quantities, or route to RT-010/RT-009/RT-002 owner handoff, quarantine, or escalation when semantics are not purely RT-002 planning.
- Cultivation qi, meridians, breakthroughs, tribulations, bottlenecks, and cosmology-specific tracks may use source-local retention, policy-only owner handoff, quarantine, or doctrine escalation rather than becoming Astra default pools.
- Class/archetype features may declare typed subject/resource/quantity references and provenance while ability semantics route to RT-004 owner handoff, quarantine, or escalation.
- Profession/career economies, jobs, wages, and occupation meters may be declared as resource/cost/consequence planning records or route to owner handoff when mission/social/inventory ownership is implicated.
- Point-buy costs may be exact lexical quantities, blocked numeric choices, validation-review records, or owner-handoff records; no arithmetic or affordability execution occurs.
- Narrative currency may be declared as source-local or quantity-bearing references, with owner handoff, quarantine, or escalation for qualitative permissions.
- Cyberware/biotech capacity, strain, and drawback consequences may declare references or quantities while hidden/biological/inventory semantics route to RT-005/RT-010 owner handoff, quarantine, or escalation.
- Psionics fatigue, backlash, focus, or qualitative powers may use source-local retention, policy-only routes, owner handoff, quarantine, or doctrine escalation.
- Horror/investigation stress, sanity, clue, corruption, doom, and hidden tracks route hidden information to RT-005, clues/missions to RT-006, and unresolved semantics to quarantine or escalation.
- Vehicles/mechs/ships may declare asset/vehicle resources and quantities, with state/inventory/vehicle mutation owned outside RT-002 and routed through owner handoff, quarantine, or escalation.
- Companions/summons may bind subjects and affected resources, but actor, social, combat, or generated-content ownership routes to the relevant RT owner through handoff, quarantine, or escalation.
- Crafting/salvage/requisition may declare materials, costs, and proposed state-delta references for future review; inventory mutation, settlement, and persistence remain unauthorized.
- Mission/faction/debt consequences may be declared as consequence terms and proposed state-delta refs only when eligible; mission/social/debt ownership routes to RT-006/RT-007/RT-002 handoff as needed.
- Source-local cosmology remains source-local, quarantined, escalated, or owner-handoff-bound unless later doctrine explicitly adopts a canonical surface.
- Generated content resources and provenance recur through RT-008 provenance bindings, source-local retention, quarantine, or doctrine escalation.
- Persistent campaign consequences remain non-mutating proposals with state-delta refs only after eligibility; persistence, transaction execution, event append, and replay remain unauthorized.

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
  reservation_authorized_by_this_pr: false
  settlement_authorized_by_this_pr: false
  consequence_application_authorized_by_this_pr: false
  mutation_authorized_by_this_pr: false
  state_delta_application_authorized_by_this_pr: false
  transaction_execution_authorized_by_this_pr: false
  event_commitment_authorized_by_this_pr: false
  event_append_authorized_by_this_pr: false
  persistence_authorized_by_this_pr: false
  replay_authorized_by_this_pr: false
  rng_execution_authorized_by_this_pr: false
  table_oracle_execution_authorized_by_this_pr: false
  model_authority_authorized_by_this_pr: false
  model_integration_authorized_by_this_pr: false
  live_play_authorized_by_this_pr: false
  ui_authorized_by_this_pr: false
  conversion_authorized_by_this_pr: false
  canon_promotion_authorized_by_this_pr: false
```
