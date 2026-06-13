from __future__ import annotations

from types import MappingProxyType

import pytest

from astra_runtime.domain.resource_consequence_math import (
    RESOURCE_MATH_OWNER_DOMAINS,
    RESOURCE_MATH_SUBJECT_ROLES,
    RESOURCE_MATH_SUBJECT_TYPES,
    VISIBILITY_POLICIES,
    InvalidResourceMathSubjectReferenceError,
    ResourceMathSubjectReference,
    create_resource_math_subject_reference,
    validate_resource_math_subject_reference,
)


def test_controlled_constants_are_frozensets_and_contain_expected_values() -> None:
    assert isinstance(RESOURCE_MATH_SUBJECT_TYPES, frozenset)
    assert "actor" in RESOURCE_MATH_SUBJECT_TYPES
    assert isinstance(RESOURCE_MATH_SUBJECT_ROLES, frozenset)
    assert "primary_subject" in RESOURCE_MATH_SUBJECT_ROLES
    assert isinstance(RESOURCE_MATH_OWNER_DOMAINS, frozenset)
    assert "RT002_resource_consequence_math" in RESOURCE_MATH_OWNER_DOMAINS
    assert isinstance(VISIBILITY_POLICIES, frozenset)
    assert "public" in VISIBILITY_POLICIES


def test_factory_creates_valid_resource_math_subject_reference() -> None:
    ref = create_resource_math_subject_reference(
        subject_binding_id="sub-1",
        subject_type="actor",
        subject_ref_id="ext-sub-1",
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
        visibility_policy="hidden",
        provenance_refs=["prov-1", "prov-2"],
        metadata={"note": "keep"},
    )
    assert isinstance(ref, ResourceMathSubjectReference)
    assert ref.subject_binding_id == "sub-1"
    assert ref.subject_type == "actor"
    assert ref.subject_ref_id == "ext-sub-1"
    assert ref.subject_role == "primary_subject"
    assert ref.owner_domain == "RT002_resource_consequence_math"
    assert ref.visibility_policy == "hidden"
    assert ref.provenance_refs == ("prov-1", "prov-2")
    assert isinstance(ref.metadata, MappingProxyType)
    assert dict(ref.metadata) == {"note": "keep"}


def test_validator_returns_true_for_valid_instance() -> None:
    ref = create_resource_math_subject_reference(
        subject_binding_id="sub-1",
        subject_type="actor",
        subject_ref_id="ext-sub-1",
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
    )
    assert validate_resource_math_subject_reference(ref) is True


def test_validator_returns_false_for_non_instance_input() -> None:
    assert validate_resource_math_subject_reference({}) is False
    assert validate_resource_math_subject_reference(None) is False
    assert validate_resource_math_subject_reference("not-a-reference") is False


def test_factory_rejects_empty_subject_binding_id() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="",
            subject_type="actor",
            subject_ref_id="ext-sub-1",
            subject_role="primary_subject",
            owner_domain="RT002_resource_consequence_math",
        )


def test_factory_rejects_invalid_subject_type() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="sub-1",
            subject_type="invalid_type",
            subject_ref_id="ext-sub-1",
            subject_role="primary_subject",
            owner_domain="RT002_resource_consequence_math",
        )


def test_factory_rejects_invalid_subject_role() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="sub-1",
            subject_type="actor",
            subject_ref_id="ext-sub-1",
            subject_role="invalid_role",
            owner_domain="RT002_resource_consequence_math",
        )


def test_factory_rejects_invalid_owner_domain() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="sub-1",
            subject_type="actor",
            subject_ref_id="ext-sub-1",
            subject_role="primary_subject",
            owner_domain="invalid_owner",
        )


def test_factory_rejects_invalid_visibility_policy() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="sub-1",
            subject_type="actor",
            subject_ref_id="ext-sub-1",
            subject_role="primary_subject",
            owner_domain="RT002_resource_consequence_math",
            visibility_policy="invalid_visibility",
        )


def test_factory_rejects_bare_string_as_provenance_refs() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="sub-1",
            subject_type="actor",
            subject_ref_id="ext-sub-1",
            subject_role="primary_subject",
            owner_domain="RT002_resource_consequence_math",
            provenance_refs="prov-1",
        )


def test_factory_rejects_empty_string_inside_provenance_refs() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="sub-1",
            subject_type="actor",
            subject_ref_id="ext-sub-1",
            subject_role="primary_subject",
            owner_domain="RT002_resource_consequence_math",
            provenance_refs=["prov-1", ""],
        )


def test_factory_rejects_callable_metadata_value() -> None:
    with pytest.raises(InvalidResourceMathSubjectReferenceError):
        create_resource_math_subject_reference(
            subject_binding_id="sub-1",
            subject_type="actor",
            subject_ref_id="ext-sub-1",
            subject_role="primary_subject",
            owner_domain="RT002_resource_consequence_math",
            metadata={"bad": lambda: None},
        )


def test_to_dict_returns_plain_dict_with_copied_values() -> None:
    ref = create_resource_math_subject_reference(
        subject_binding_id="sub-1",
        subject_type="actor",
        subject_ref_id="ext-sub-1",
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
        provenance_refs=["prov-1", "prov-2"],
        metadata={"note": "keep"},
    )
    serialized = ref.to_dict()
    assert isinstance(serialized, dict)
    assert serialized["subject_binding_id"] == "sub-1"
    assert serialized["provenance_refs"] == ["prov-1", "prov-2"]
    assert serialized["provenance_refs"] is not list(ref.provenance_refs)
    assert serialized["metadata"] == {"note": "keep"}
    assert isinstance(serialized["metadata"], dict)
    assert serialized["metadata"] is not ref.metadata


def test_metadata_mutation_does_not_affect_dataclass_or_serialization() -> None:
    original = {"nested": {"value": 1}}
    ref = create_resource_math_subject_reference(
        subject_binding_id="sub-1",
        subject_type="actor",
        subject_ref_id="ext-sub-1",
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
        metadata=original,
    )
    original["nested"]["value"] = 999
    assert dict(ref.metadata)["nested"]["value"] == 1
    serialized = ref.to_dict()
    assert serialized["metadata"]["nested"]["value"] == 1


from astra_runtime.domain.resource_consequence_math import (
    CONVERSION_POLICIES,
    InvalidResourceMathDependencyError,
    InvalidQuantitySpecificationError,
    InvalidResourceReferenceError,
    QUANTITY_NEGATIVE_VALUE_POLICIES,
    QUANTITY_REPRESENTATION_KINDS,
    RESOURCE_FAMILIES,
    RESOURCE_MATH_DEPENDENCY_TYPES,
    ROUNDING_POLICIES,
    ResourceMathDependency,
    QuantitySpecification,
    ResourceReference,
    create_resource_math_dependency,
    create_quantity_specification,
    create_resource_reference,
    validate_resource_math_dependency,
    validate_quantity_specification,
    validate_resource_reference,
)


def test_new_constants_are_frozensets() -> None:
    assert isinstance(RESOURCE_FAMILIES, frozenset)
    assert "currency_like" in RESOURCE_FAMILIES
    assert isinstance(QUANTITY_REPRESENTATION_KINDS, frozenset)
    assert "integer_exact" in QUANTITY_REPRESENTATION_KINDS
    assert isinstance(CONVERSION_POLICIES, frozenset)
    assert "no_conversion" in CONVERSION_POLICIES
    assert isinstance(ROUNDING_POLICIES, frozenset)
    assert "no_rounding" in ROUNDING_POLICIES
    assert isinstance(QUANTITY_NEGATIVE_VALUE_POLICIES, frozenset)
    assert "negative_values_forbidden" in QUANTITY_NEGATIVE_VALUE_POLICIES
    assert isinstance(RESOURCE_MATH_DEPENDENCY_TYPES, frozenset)
    assert "subject_ref" in RESOURCE_MATH_DEPENDENCY_TYPES


def test_factory_creates_valid_resource_reference() -> None:
    ref = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
        source_label="credits",
        source_aliases=["money", "funds"],
        visibility_policy="actor_visible",
        unit_ref_id="unit-credit",
        dimension_ref_id="dim-value",
        provenance_refs=["prov-1"],
        source_local=False,
        metadata={"note": "ref"},
    )
    assert isinstance(ref, ResourceReference)
    assert ref.resource_ref_id == "res-1"
    assert ref.resource_family == "currency_like"
    assert ref.source_aliases == ("money", "funds")
    assert ref.visibility_policy == "actor_visible"
    assert ref.source_local is False


def test_validator_returns_true_for_valid_resource_reference() -> None:
    ref = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    assert validate_resource_reference(ref) is True


def test_validator_returns_false_for_non_resource_reference() -> None:
    assert validate_resource_reference(None) is False
    assert validate_resource_reference("not-a-ref") is False


def test_factory_rejects_invalid_resource_family() -> None:
    with pytest.raises(InvalidResourceReferenceError):
        create_resource_reference(
            resource_ref_id="res-1",
            subject_binding_id="sub-1",
            resource_family="hit_points",
            resource_key="hp",
            owner_domain="RT002_resource_consequence_math",
        )


def test_factory_rejects_invalid_owner_domain_for_resource_reference() -> None:
    with pytest.raises(InvalidResourceReferenceError):
        create_resource_reference(
            resource_ref_id="res-1",
            subject_binding_id="sub-1",
            resource_family="currency_like",
            resource_key="credits",
            owner_domain="invalid_owner",
        )


def test_factory_rejects_invalid_visibility_policy_for_resource_reference() -> None:
    with pytest.raises(InvalidResourceReferenceError):
        create_resource_reference(
            resource_ref_id="res-1",
            subject_binding_id="sub-1",
            resource_family="currency_like",
            resource_key="credits",
            owner_domain="RT002_resource_consequence_math",
            visibility_policy="everyone",
        )


def test_factory_rejects_invalid_optional_strings_for_resource_reference() -> None:
    with pytest.raises(InvalidResourceReferenceError):
        create_resource_reference(
            resource_ref_id="res-1",
            subject_binding_id="sub-1",
            resource_family="currency_like",
            resource_key="credits",
            owner_domain="RT002_resource_consequence_math",
            source_label="",
        )


def test_factory_rejects_bare_string_source_aliases() -> None:
    with pytest.raises(InvalidResourceReferenceError):
        create_resource_reference(
            resource_ref_id="res-1",
            subject_binding_id="sub-1",
            resource_family="currency_like",
            resource_key="credits",
            owner_domain="RT002_resource_consequence_math",
            source_aliases="money",
        )


def test_factory_rejects_empty_string_inside_source_aliases() -> None:
    with pytest.raises(InvalidResourceReferenceError):
        create_resource_reference(
            resource_ref_id="res-1",
            subject_binding_id="sub-1",
            resource_family="currency_like",
            resource_key="credits",
            owner_domain="RT002_resource_consequence_math",
            source_aliases=["money", ""],
        )


def test_factory_rejects_non_bool_source_local() -> None:
    with pytest.raises(InvalidResourceReferenceError):
        create_resource_reference(
            resource_ref_id="res-1",
            subject_binding_id="sub-1",
            resource_family="currency_like",
            resource_key="credits",
            owner_domain="RT002_resource_consequence_math",
            source_local="yes",
        )


def test_resource_reference_to_dict_returns_copies() -> None:
    ref = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
        source_aliases=["money"],
        metadata={"note": "ref"},
    )
    serialized = ref.to_dict()
    assert serialized["source_aliases"] == ["money"]
    assert serialized["source_aliases"] is not list(ref.source_aliases)
    assert serialized["metadata"] == {"note": "ref"}
    assert serialized["metadata"] is not ref.metadata


def test_factory_creates_valid_quantity_specification() -> None:
    qty = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="decimal_exact",
        magnitude_text="10.50",
        precision=2,
        conversion_policy="exact_conversion",
        rounding_policy="round_nearest",
        negative_value_policy="negative_values_allowed_by_source",
        visibility_policy="hidden",
        provenance_refs=["prov-1"],
        metadata={"note": "qty"},
    )
    assert isinstance(qty, QuantitySpecification)
    assert qty.quantity_id == "qty-1"
    assert qty.representation_kind == "decimal_exact"
    assert qty.precision == 2
    assert qty.conversion_policy == "exact_conversion"
    assert qty.rounding_policy == "round_nearest"
    assert qty.negative_value_policy == "negative_values_allowed_by_source"


def test_validator_returns_true_for_valid_quantity_specification() -> None:
    qty = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
        magnitude_text="5",
    )
    assert validate_quantity_specification(qty) is True


def test_validator_returns_false_for_non_quantity_specification() -> None:
    assert validate_quantity_specification({}) is False


def test_factory_rejects_invalid_representation_kind() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="float_approx",
        )


def test_factory_rejects_invalid_conversion_policy() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="integer_exact",
            conversion_policy="convert_freely",
        )


def test_factory_rejects_invalid_rounding_policy() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="integer_exact",
            rounding_policy="round_randomly",
        )


def test_factory_rejects_invalid_negative_value_policy() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="integer_exact",
            negative_value_policy="allow_anything",
        )


def test_factory_rejects_invalid_visibility_policy_for_quantity() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="integer_exact",
            visibility_policy="all_visible",
        )


def test_factory_rejects_invalid_optional_strings_for_quantity() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="integer_exact",
            magnitude_text="",
        )


def test_factory_rejects_bare_string_provenance_refs_for_quantity() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="integer_exact",
            provenance_refs="prov-1",
        )


def test_factory_rejects_empty_string_inside_provenance_refs_for_quantity() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="integer_exact",
            provenance_refs=["prov-1", ""],
        )


def test_factory_rejects_bool_precision_and_scale() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="decimal_exact",
            precision=True,
        )
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="fixed_point_scaled",
            scale=True,
        )


def test_factory_rejects_non_positive_precision_and_negative_scale() -> None:
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="decimal_exact",
            precision=0,
        )
    with pytest.raises(InvalidQuantitySpecificationError):
        create_quantity_specification(
            quantity_id="qty-1",
            representation_kind="fixed_point_scaled",
            scale=-1,
        )


def test_quantity_specification_to_dict_returns_copies() -> None:
    qty = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
        provenance_refs=["prov-1"],
        metadata={"note": "qty"},
    )
    serialized = qty.to_dict()
    assert serialized["provenance_refs"] == ["prov-1"]
    assert serialized["provenance_refs"] is not list(qty.provenance_refs)
    assert serialized["metadata"] == {"note": "qty"}
    assert serialized["metadata"] is not qty.metadata


def test_factory_creates_valid_resource_math_dependency() -> None:
    dep = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
        required=True,
        satisfied=False,
        hidden_info_safe=True,
        metadata={"note": "dep"},
    )
    assert isinstance(dep, ResourceMathDependency)
    assert dep.dependency_id == "dep-1"
    assert dep.dependency_type == "subject_ref"
    assert dep.reference_id == "ext-sub-1"
    assert dep.required is True
    assert dep.satisfied is False
    assert dep.hidden_info_safe is True


def test_validator_returns_true_for_valid_resource_math_dependency() -> None:
    dep = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="unit_ref",
        reference_id="unit-1",
        owner_domain="RT002_resource_consequence_math",
    )
    assert validate_resource_math_dependency(dep) is True


def test_validator_returns_false_for_non_dependency() -> None:
    assert validate_resource_math_dependency(None) is False
    assert validate_resource_math_dependency("dep") is False


def test_factory_rejects_invalid_dependency_type() -> None:
    with pytest.raises(InvalidResourceMathDependencyError):
        create_resource_math_dependency(
            dependency_id="dep-1",
            dependency_type="unknown_type",
            reference_id="ref-1",
            owner_domain="RT002_resource_consequence_math",
        )


def test_factory_rejects_invalid_owner_domain_for_dependency() -> None:
    with pytest.raises(InvalidResourceMathDependencyError):
        create_resource_math_dependency(
            dependency_id="dep-1",
            dependency_type="subject_ref",
            reference_id="ref-1",
            owner_domain="invalid_owner",
        )


def test_factory_rejects_non_bool_dependency_flags() -> None:
    with pytest.raises(InvalidResourceMathDependencyError):
        create_resource_math_dependency(
            dependency_id="dep-1",
            dependency_type="subject_ref",
            reference_id="ref-1",
            owner_domain="RT002_resource_consequence_math",
            required="yes",
        )
    with pytest.raises(InvalidResourceMathDependencyError):
        create_resource_math_dependency(
            dependency_id="dep-1",
            dependency_type="subject_ref",
            reference_id="ref-1",
            owner_domain="RT002_resource_consequence_math",
            satisfied="no",
        )
    with pytest.raises(InvalidResourceMathDependencyError):
        create_resource_math_dependency(
            dependency_id="dep-1",
            dependency_type="subject_ref",
            reference_id="ref-1",
            owner_domain="RT002_resource_consequence_math",
            hidden_info_safe=1,
        )


def test_resource_math_dependency_to_dict_returns_copies() -> None:
    dep = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
        metadata={"note": "dep"},
    )
    serialized = dep.to_dict()
    assert serialized["dependency_id"] == "dep-1"
    assert serialized["metadata"] == {"note": "dep"}
    assert serialized["metadata"] is not dep.metadata


def test_metadata_mutation_does_not_affect_new_shapes() -> None:
    original = {"nested": {"value": 1}}
    ref = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
        metadata=original,
    )
    qty = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
        metadata=original,
    )
    dep = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ref-1",
        owner_domain="RT002_resource_consequence_math",
        metadata=original,
    )
    original["nested"]["value"] = 999
    assert dict(ref.metadata)["nested"]["value"] == 1
    assert ref.to_dict()["metadata"]["nested"]["value"] == 1
    assert dict(qty.metadata)["nested"]["value"] == 1
    assert qty.to_dict()["metadata"]["nested"]["value"] == 1
    assert dict(dep.metadata)["nested"]["value"] == 1
    assert dep.to_dict()["metadata"]["nested"]["value"] == 1


from astra_runtime.domain.resource_consequence_math import (
    COST_FAMILIES,
    COST_OUTCOME_POLICIES,
    COST_TIMING_POLICIES,
    CONSEQUENCE_FAMILIES,
    RESOURCE_TERM_POLICY_ROUTES,
    RESOURCE_TERM_VALUE_MODES,
    ConsequenceTerm,
    CostTerm,
    InvalidConsequenceTermError,
    InvalidCostTermError,
    create_consequence_term,
    create_cost_term,
    validate_consequence_term,
    validate_cost_term,
)


def test_term_constants_are_frozensets() -> None:
    assert isinstance(RESOURCE_TERM_VALUE_MODES, frozenset)
    assert "resource_quantity" in RESOURCE_TERM_VALUE_MODES
    assert isinstance(RESOURCE_TERM_POLICY_ROUTES, frozenset)
    assert "owner_handoff_required" in RESOURCE_TERM_POLICY_ROUTES
    assert isinstance(COST_FAMILIES, frozenset)
    assert "activation" in COST_FAMILIES
    assert isinstance(CONSEQUENCE_FAMILIES, frozenset)
    assert "gain" in CONSEQUENCE_FAMILIES
    assert isinstance(COST_TIMING_POLICIES, frozenset)
    assert "blocked_pending_validation" in COST_TIMING_POLICIES
    assert isinstance(COST_OUTCOME_POLICIES, frozenset)
    assert "validation_blocked" in COST_OUTCOME_POLICIES


def test_factory_creates_valid_cost_term_resource_quantity() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        resource_ref_id="res-1",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
        timing_policy="pay_on_attempt",
        outcome_policy="success",
        visibility_policy="actor_visible",
        dependency_ids=["dep-1"],
        provenance_refs=["prov-1"],
        metadata={"note": "cost"},
    )
    assert isinstance(term, CostTerm)
    assert term.term_id == "term-1"
    assert term.resource_ref_id == "res-1"
    assert term.quantity_id == "qty-1"
    assert term.value_mode == "resource_quantity"
    assert term.cost_family == "activation"
    assert term.timing_policy == "pay_on_attempt"
    assert term.outcome_policy == "success"
    assert term.dependency_ids == ("dep-1",)


def test_factory_creates_valid_cost_term_policy_only() -> None:
    term = create_cost_term(
        term_id="term-2",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        cost_family="validation_blocked",
        owner_domain="RT002_resource_consequence_math",
        policy_route="quarantine_required",
    )
    assert isinstance(term, CostTerm)
    assert term.resource_ref_id is None
    assert term.quantity_id is None
    assert term.policy_route == "quarantine_required"


def test_validator_returns_true_for_valid_cost_term() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        resource_ref_id="res-1",
        value_mode="resource_reference_only",
        cost_family="opportunity",
        owner_domain="RT002_resource_consequence_math",
    )
    assert validate_cost_term(term) is True


def test_validator_returns_false_for_non_cost_term() -> None:
    assert validate_cost_term(None) is False
    assert validate_cost_term("term") is False


def test_cost_term_factory_rejects_empty_required_fields() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="",
            subject_binding_id="sub-1",
            value_mode="resource_quantity",
            resource_ref_id="res-1",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="",
            value_mode="resource_quantity",
            resource_ref_id="res-1",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_term_factory_rejects_invalid_value_mode() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="magic_cost",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_term_factory_rejects_invalid_cost_family() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="hit_points",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_term_factory_rejects_invalid_owner_domain() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="invalid_owner",
        )


def test_cost_term_factory_rejects_invalid_policy_route() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="policy_only",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            policy_route="owner_review",
        )


def test_cost_term_factory_rejects_invalid_timing_policy() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            timing_policy="pay_whenever",
        )


def test_cost_term_factory_rejects_invalid_outcome_policy() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            outcome_policy="mystery",
        )


def test_cost_term_factory_rejects_invalid_visibility_policy() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            visibility_policy="all_visible",
        )


def test_cost_term_factory_rejects_invalid_optional_strings() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="resource_reference_only",
            resource_ref_id="",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_term_factory_rejects_bare_string_dependency_ids() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            dependency_ids="dep-1",
        )


def test_cost_term_factory_rejects_empty_string_inside_dependency_ids() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            dependency_ids=["dep-1", ""],
        )


def test_cost_term_factory_rejects_bare_string_provenance_refs() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            provenance_refs="prov-1",
        )


def test_cost_term_factory_rejects_callable_metadata() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
            metadata={"bad": lambda: None},
        )


def test_cost_term_value_mode_matrix_rules() -> None:
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="resource_quantity",
            resource_ref_id="res-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="resource_reference_only",
            resource_ref_id="res-1",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            resource_ref_id="res-1",
            quantity_id="qty-1",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )
    with pytest.raises(InvalidCostTermError):
        create_cost_term(
            term_id="term-1",
            subject_binding_id="sub-1",
            value_mode="policy_only",
            cost_family="activation",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_term_to_dict_returns_copies() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        value_mode="quantity_only",
        quantity_id="qty-1",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
        dependency_ids=["dep-1"],
        provenance_refs=["prov-1"],
        metadata={"note": "cost"},
    )
    serialized = term.to_dict()
    assert serialized["dependency_ids"] == ["dep-1"]
    assert serialized["dependency_ids"] is not list(term.dependency_ids)
    assert serialized["provenance_refs"] == ["prov-1"]
    assert serialized["metadata"] == {"note": "cost"}
    assert serialized["metadata"] is not term.metadata


def test_factory_creates_valid_consequence_term() -> None:
    term = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        resource_ref_id="res-1",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
        timing_policy="pay_on_failure",
        outcome_policy="failure",
        visibility_policy="hidden",
        dependency_ids=["dep-1"],
        provenance_refs=["prov-1"],
        metadata={"note": "consequence"},
    )
    assert isinstance(term, ConsequenceTerm)
    assert term.consequence_id == "cons-1"
    assert term.consequence_family == "loss"
    assert term.value_mode == "resource_quantity"


def test_validator_returns_true_for_valid_consequence_term() -> None:
    term = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        consequence_family="visibility_change",
        owner_domain="RT002_resource_consequence_math",
        policy_route="doctrine_escalation_required",
    )
    assert validate_consequence_term(term) is True


def test_validator_returns_false_for_non_consequence_term() -> None:
    assert validate_consequence_term(None) is False
    assert validate_consequence_term("cons") is False


def test_consequence_term_factory_rejects_empty_required_fields() -> None:
    with pytest.raises(InvalidConsequenceTermError):
        create_consequence_term(
            consequence_id="",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            consequence_family="loss",
            owner_domain="RT002_resource_consequence_math",
        )


def test_consequence_term_factory_rejects_invalid_consequence_family() -> None:
    with pytest.raises(InvalidConsequenceTermError):
        create_consequence_term(
            consequence_id="cons-1",
            subject_binding_id="sub-1",
            value_mode="quantity_only",
            quantity_id="qty-1",
            consequence_family="sanity_loss",
            owner_domain="RT002_resource_consequence_math",
        )


def test_consequence_term_factory_rejects_invalid_policy_route() -> None:
    with pytest.raises(InvalidConsequenceTermError):
        create_consequence_term(
            consequence_id="cons-1",
            subject_binding_id="sub-1",
            value_mode="policy_only",
            consequence_family="exposure",
            owner_domain="RT002_resource_consequence_math",
            policy_route="hidden",
        )


def test_consequence_term_value_mode_matrix_rules() -> None:
    with pytest.raises(InvalidConsequenceTermError):
        create_consequence_term(
            consequence_id="cons-1",
            subject_binding_id="sub-1",
            value_mode="resource_quantity",
            resource_ref_id="res-1",
            consequence_family="loss",
            owner_domain="RT002_resource_consequence_math",
        )
    with pytest.raises(InvalidConsequenceTermError):
        create_consequence_term(
            consequence_id="cons-1",
            subject_binding_id="sub-1",
            value_mode="policy_only",
            consequence_family="loss",
            owner_domain="RT002_resource_consequence_math",
            resource_ref_id="res-1",
            policy_route="owner_handoff_required",
        )


def test_consequence_term_to_dict_returns_copies() -> None:
    term = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        value_mode="quantity_only",
        quantity_id="qty-1",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
        dependency_ids=["dep-1"],
        provenance_refs=["prov-1"],
        metadata={"note": "consequence"},
    )
    serialized = term.to_dict()
    assert serialized["dependency_ids"] == ["dep-1"]
    assert serialized["provenance_refs"] == ["prov-1"]
    assert serialized["metadata"] == {"note": "consequence"}
    assert serialized["metadata"] is not term.metadata


def test_new_term_metadata_mutation_is_isolated() -> None:
    original = {"nested": {"value": 1}}
    cost = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        value_mode="quantity_only",
        quantity_id="qty-1",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
        metadata=original,
    )
    cons = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        value_mode="quantity_only",
        quantity_id="qty-1",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
        metadata=original,
    )
    original["nested"]["value"] = 999
    assert dict(cost.metadata)["nested"]["value"] == 1
    assert cost.to_dict()["metadata"]["nested"]["value"] == 1
    assert dict(cons.metadata)["nested"]["value"] == 1
    assert cons.to_dict()["metadata"]["nested"]["value"] == 1


from astra_runtime.domain.resource_consequence_math import (
    ATOMICITY_POLICIES,
    COST_TIMING_POLICIES,
    ORDERING_POLICIES,
    PARTIAL_SETTLEMENT_POLICIES,
    CostBundle,
    InvalidCostBundleError,
    create_cost_bundle,
    validate_cost_bundle,
)


def test_bundle_constants_are_frozensets() -> None:
    assert isinstance(ATOMICITY_POLICIES, frozenset)
    assert "all_or_nothing_requested" in ATOMICITY_POLICIES
    assert isinstance(ORDERING_POLICIES, frozenset)
    assert "unordered_terms" in ORDERING_POLICIES
    assert isinstance(PARTIAL_SETTLEMENT_POLICIES, frozenset)
    assert "no_partial_settlement" in PARTIAL_SETTLEMENT_POLICIES
    assert isinstance(COST_TIMING_POLICIES, frozenset)


def test_factory_creates_valid_cost_bundle() -> None:
    bundle = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-a", "term-b"],
        atomicity_policy="best_effort_requested",
        ordering_policy="unordered_terms",
        partial_settlement_policy="partial_settlement_allowed",
        owner_domain="RT002_resource_consequence_math",
        visibility_policy="actor_visible",
        dependency_ids=["dep-1"],
        provenance_refs=["prov-1"],
        metadata={"note": "bundle"},
    )
    assert isinstance(bundle, CostBundle)
    assert bundle.bundle_id == "bundle-1"
    assert bundle.term_ids == ("term-a", "term-b")
    assert bundle.atomicity_policy == "best_effort_requested"
    assert bundle.dependency_ids == ("dep-1",)


def test_factory_creates_valid_cost_bundle_with_bounds_and_alternatives() -> None:
    bundle = create_cost_bundle(
        bundle_id="bundle-2",
        term_ids=["term-a", "term-b", "term-c"],
        atomicity_policy="alternative_exactly_one",
        ordering_policy="unordered_terms",
        minimum_required_terms=1,
        maximum_allowed_terms=2,
        alternative_groups=[
            ("group-1", ["term-a", "term-b"]),
        ],
        owner_domain="RT002_resource_consequence_math",
    )
    assert isinstance(bundle, CostBundle)
    assert bundle.minimum_required_terms == 1
    assert bundle.maximum_allowed_terms == 2
    assert bundle.alternative_groups == (("group-1", ("term-a", "term-b")),)


def test_validator_returns_true_for_valid_cost_bundle() -> None:
    bundle = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-a", "term-b"],
        owner_domain="RT002_resource_consequence_math",
    )
    assert validate_cost_bundle(bundle) is True


def test_validator_returns_false_for_non_cost_bundle() -> None:
    assert validate_cost_bundle(None) is False
    assert validate_cost_bundle("bundle") is False


def test_cost_bundle_factory_rejects_empty_bundle_id() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_empty_term_ids() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=[],
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_duplicate_term_ids() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-a"],
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_bare_string_term_ids() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids="term-a",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_empty_string_inside_term_ids() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", ""],
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_invalid_atomicity_policy() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            atomicity_policy="flexible",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_invalid_ordering_policy() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            ordering_policy="random_order",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_invalid_partial_settlement_policy() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            partial_settlement_policy="settle_freely",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_invalid_visibility_policy() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            visibility_policy="all_visible",
            owner_domain="RT002_resource_consequence_math",
        )


def test_cost_bundle_factory_rejects_invalid_owner_domain() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="invalid_owner",
        )


def test_cost_bundle_factory_rejects_bool_bounds() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            minimum_required_terms=True,
        )
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            maximum_allowed_terms=True,
        )


def test_cost_bundle_factory_rejects_non_positive_bounds() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            minimum_required_terms=0,
        )
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            maximum_allowed_terms=-1,
        )


def test_cost_bundle_factory_rejects_bounds_exceeding_term_count() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b"],
            owner_domain="RT002_resource_consequence_math",
            minimum_required_terms=3,
        )
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b"],
            owner_domain="RT002_resource_consequence_math",
            maximum_allowed_terms=3,
        )


def test_cost_bundle_factory_rejects_minimum_greater_than_maximum() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b", "term-c"],
            owner_domain="RT002_resource_consequence_math",
            minimum_required_terms=3,
            maximum_allowed_terms=2,
        )


def test_cost_bundle_factory_rejects_duplicate_alternative_group_ids() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b", "term-c", "term-d"],
            owner_domain="RT002_resource_consequence_math",
            alternative_groups=[
                ("group-1", ["term-a", "term-b"]),
                ("group-1", ["term-c", "term-d"]),
            ],
        )


def test_cost_bundle_factory_rejects_empty_alternative_group_id() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b"],
            owner_domain="RT002_resource_consequence_math",
            alternative_groups=[
                ("", ["term-a"]),
            ],
        )


def test_cost_bundle_factory_rejects_empty_alternative_group_terms() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b"],
            owner_domain="RT002_resource_consequence_math",
            alternative_groups=[
                ("group-1", []),
            ],
        )


def test_cost_bundle_factory_rejects_alternative_term_not_in_term_ids() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b"],
            owner_domain="RT002_resource_consequence_math",
            alternative_groups=[
                ("group-1", ["term-c"]),
            ],
        )


def test_cost_bundle_factory_rejects_duplicate_term_inside_alternative_group() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b"],
            owner_domain="RT002_resource_consequence_math",
            alternative_groups=[
                ("group-1", ["term-a", "term-a"]),
            ],
        )


def test_cost_bundle_factory_rejects_overlapping_alternative_groups() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a", "term-b", "term-c"],
            owner_domain="RT002_resource_consequence_math",
            alternative_groups=[
                ("group-1", ["term-a", "term-b"]),
                ("group-2", ["term-b", "term-c"]),
            ],
        )


def test_cost_bundle_factory_rejects_bare_string_dependency_ids() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            dependency_ids="dep-1",
        )


def test_cost_bundle_factory_rejects_bare_string_provenance_refs() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            provenance_refs="prov-1",
        )


def test_cost_bundle_factory_rejects_empty_string_inside_dependency_or_provenance() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            dependency_ids=["dep-1", ""],
        )
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            provenance_refs=["prov-1", ""],
        )


def test_cost_bundle_factory_rejects_callable_metadata() -> None:
    with pytest.raises(InvalidCostBundleError):
        create_cost_bundle(
            bundle_id="bundle-1",
            term_ids=["term-a"],
            owner_domain="RT002_resource_consequence_math",
            metadata={"bad": lambda: None},
        )


def test_cost_bundle_to_dict_returns_copies() -> None:
    bundle = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-a", "term-b"],
        owner_domain="RT002_resource_consequence_math",
        alternative_groups=[("group-1", ["term-a"])],
        dependency_ids=["dep-1"],
        provenance_refs=["prov-1"],
        metadata={"note": "bundle"},
    )
    serialized = bundle.to_dict()
    assert serialized["term_ids"] == ["term-a", "term-b"]
    assert serialized["term_ids"] is not list(bundle.term_ids)
    assert serialized["alternative_groups"] == [["group-1", ["term-a"]]]
    assert serialized["dependency_ids"] == ["dep-1"]
    assert serialized["provenance_refs"] == ["prov-1"]
    assert serialized["metadata"] == {"note": "bundle"}
    assert serialized["metadata"] is not bundle.metadata


def test_cost_bundle_metadata_mutation_is_isolated() -> None:
    original = {"nested": {"value": 1}}
    bundle = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-a"],
        owner_domain="RT002_resource_consequence_math",
        metadata=original,
    )
    original["nested"]["value"] = 999
    assert dict(bundle.metadata)["nested"]["value"] == 1
    assert bundle.to_dict()["metadata"]["nested"]["value"] == 1


from astra_runtime.domain.resource_consequence_math import (
    InvalidResourceMathRequestError,
    ResourceMathRequest,
    create_resource_math_request,
    validate_resource_math_request,
)


def _make_primary_subject(binding_id: str = "sub-1") -> ResourceMathSubjectReference:
    return create_resource_math_subject_reference(
        subject_binding_id=binding_id,
        subject_type="actor",
        subject_ref_id=f"ext-{binding_id}",
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
    )


def _make_minimal_request() -> ResourceMathRequest:
    return create_resource_math_request(
        request_id="req-1",
        trace_ref_id="trace-1",
        subject_refs=[_make_primary_subject()],
    )


def _make_populated_request() -> ResourceMathRequest:
    subject = _make_primary_subject()
    resource = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    quantity = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
        magnitude_text="5",
    )
    dependency = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
    )
    cost_term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        resource_ref_id="res-1",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
        dependency_ids=["dep-1"],
    )
    cost_bundle = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-1"],
        owner_domain="RT002_resource_consequence_math",
    )
    consequence = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        resource_ref_id="res-1",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
    )
    return create_resource_math_request(
        request_id="req-1",
        trace_ref_id="trace-1",
        subject_refs=[subject],
        command_ref_id="cmd-1",
        action_legality_ref_id="al-1",
        state_projection_ref_ids=["proj-1"],
        resource_refs=[resource],
        quantity_specs=[quantity],
        cost_terms=[cost_term],
        cost_bundles=[cost_bundle],
        consequence_terms=[consequence],
        dependencies=[dependency],
        provenance_refs=["prov-1"],
        owner_handoff_ref_ids=["handoff-1"],
        validation_request_ref_id="val-req-1",
        metadata={"note": "request"},
    )


def test_factory_creates_valid_minimal_resource_math_request() -> None:
    request = _make_minimal_request()
    assert isinstance(request, ResourceMathRequest)
    assert request.request_id == "req-1"
    assert request.trace_ref_id == "trace-1"
    assert len(request.subject_refs) == 1
    assert request.subject_refs[0].subject_binding_id == "sub-1"
    assert request.command_ref_id is None
    assert request.state_projection_ref_ids == ()
    assert request.resource_refs == ()


def test_factory_creates_valid_populated_resource_math_request() -> None:
    request = _make_populated_request()
    assert isinstance(request, ResourceMathRequest)
    assert request.request_id == "req-1"
    assert request.trace_ref_id == "trace-1"
    assert request.command_ref_id == "cmd-1"
    assert request.action_legality_ref_id == "al-1"
    assert request.state_projection_ref_ids == ("proj-1",)
    assert len(request.resource_refs) == 1
    assert len(request.quantity_specs) == 1
    assert len(request.cost_terms) == 1
    assert len(request.cost_bundles) == 1
    assert len(request.consequence_terms) == 1
    assert len(request.dependencies) == 1
    assert request.provenance_refs == ("prov-1",)
    assert request.owner_handoff_ref_ids == ("handoff-1",)
    assert request.validation_request_ref_id == "val-req-1"
    assert dict(request.metadata) == {"note": "request"}


def test_validator_returns_true_for_valid_resource_math_request() -> None:
    request = _make_populated_request()
    assert validate_resource_math_request(request) is True


def test_validator_returns_false_for_non_resource_math_request() -> None:
    assert validate_resource_math_request(None) is False
    assert validate_resource_math_request("request") is False
    assert validate_resource_math_request({}) is False


def test_factory_rejects_empty_request_id() -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
        )


def test_factory_rejects_empty_trace_ref_id() -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="",
            subject_refs=[_make_primary_subject()],
        )


def test_factory_rejects_empty_subject_refs() -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[],
        )


def test_factory_rejects_bare_string_where_tuple_expected() -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs="sub-1",
        )


def test_factory_rejects_empty_string_inside_string_tuple_fields() -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            state_projection_ref_ids=["proj-1", ""],
        )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            provenance_refs=["prov-1", ""],
        )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            owner_handoff_ref_ids=["handoff-1", ""],
        )


def test_factory_rejects_non_subject_reference_inside_subject_refs() -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[{"subject_binding_id": "sub-1"}],
        )


def test_factory_rejects_duplicate_subject_binding_id() -> None:
    subject_a = create_resource_math_subject_reference(
        subject_binding_id="sub-1",
        subject_type="actor",
        subject_ref_id="ext-a",
        subject_role="primary_subject",
        owner_domain="RT002_resource_consequence_math",
    )
    subject_b = create_resource_math_subject_reference(
        subject_binding_id="sub-1",
        subject_type="item",
        subject_ref_id="ext-b",
        subject_role="affected_subject",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[subject_a, subject_b],
        )


def test_factory_rejects_zero_primary_subjects() -> None:
    subject = create_resource_math_subject_reference(
        subject_binding_id="sub-1",
        subject_type="actor",
        subject_ref_id="ext-sub-1",
        subject_role="affected_subject",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[subject],
        )


def test_factory_rejects_more_than_one_primary_subject() -> None:
    subject_a = _make_primary_subject("sub-a")
    subject_b = _make_primary_subject("sub-b")
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[subject_a, subject_b],
        )


def test_factory_rejects_unresolved_resource_ref_subject_binding_id() -> None:
    resource = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="unknown-sub",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            resource_refs=[resource],
        )


def test_factory_rejects_duplicate_resource_ref_id() -> None:
    resource_a = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    resource_b = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="scene_counter",
        resource_key="ammo",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            resource_refs=[resource_a, resource_b],
        )


def test_factory_rejects_duplicate_quantity_id() -> None:
    qty_a = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
    )
    qty_b = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="decimal_exact",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            quantity_specs=[qty_a, qty_b],
        )


def test_factory_rejects_unresolved_cost_term_subject_binding_id() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="unknown-sub",
        resource_ref_id="res-1",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
    )
    resource = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    quantity = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            resource_refs=[resource],
            quantity_specs=[quantity],
            cost_terms=[term],
        )


def test_factory_rejects_unresolved_cost_term_resource_ref_id() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        resource_ref_id="unknown-res",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
    )
    quantity = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            quantity_specs=[quantity],
            cost_terms=[term],
        )


def test_factory_rejects_unresolved_cost_term_quantity_id() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        resource_ref_id="res-1",
        quantity_id="unknown-qty",
        value_mode="resource_quantity",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
    )
    resource = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            resource_refs=[resource],
            cost_terms=[term],
        )


def test_factory_rejects_duplicate_cost_term_id() -> None:
    term_a = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        value_mode="quantity_only",
        quantity_id="qty-1",
        cost_family="activation",
        owner_domain="RT002_resource_consequence_math",
    )
    term_b = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        cost_family="validation_blocked",
        owner_domain="RT002_resource_consequence_math",
        policy_route="quarantine_required",
    )
    quantity = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            quantity_specs=[quantity],
            cost_terms=[term_a, term_b],
        )


def test_factory_rejects_unresolved_cost_bundle_term_id() -> None:
    bundle = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["unknown-term"],
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            cost_bundles=[bundle],
        )


def test_factory_rejects_duplicate_cost_bundle_id() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        cost_family="validation_blocked",
        owner_domain="RT002_resource_consequence_math",
        policy_route="quarantine_required",
    )
    bundle_a = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-1"],
        owner_domain="RT002_resource_consequence_math",
    )
    bundle_b = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-1"],
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            cost_terms=[term],
            cost_bundles=[bundle_a, bundle_b],
        )


def test_factory_rejects_unresolved_consequence_term_subject_binding_id() -> None:
    term = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="unknown-sub",
        resource_ref_id="res-1",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
    )
    resource = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    quantity = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            resource_refs=[resource],
            quantity_specs=[quantity],
            consequence_terms=[term],
        )


def test_factory_rejects_unresolved_consequence_term_resource_ref_id() -> None:
    term = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        resource_ref_id="unknown-res",
        quantity_id="qty-1",
        value_mode="resource_quantity",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
    )
    quantity = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            quantity_specs=[quantity],
            consequence_terms=[term],
        )


def test_factory_rejects_unresolved_consequence_term_quantity_id() -> None:
    term = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        resource_ref_id="res-1",
        quantity_id="unknown-qty",
        value_mode="resource_quantity",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
    )
    resource = create_resource_reference(
        resource_ref_id="res-1",
        subject_binding_id="sub-1",
        resource_family="currency_like",
        resource_key="credits",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            resource_refs=[resource],
            consequence_terms=[term],
        )


def test_factory_rejects_duplicate_consequence_id() -> None:
    term_a = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        value_mode="quantity_only",
        quantity_id="qty-1",
        consequence_family="loss",
        owner_domain="RT002_resource_consequence_math",
    )
    term_b = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        consequence_family="visibility_change",
        owner_domain="RT002_resource_consequence_math",
        policy_route="owner_handoff_required",
    )
    quantity = create_quantity_specification(
        quantity_id="qty-1",
        representation_kind="integer_exact",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            quantity_specs=[quantity],
            consequence_terms=[term_a, term_b],
        )


def test_factory_rejects_duplicate_dependency_id() -> None:
    dep_a = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-a",
        owner_domain="RT002_resource_consequence_math",
    )
    dep_b = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="unit_ref",
        reference_id="unit-1",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            dependencies=[dep_a, dep_b],
        )


def test_factory_rejects_duplicate_dependency_type_reference_pair() -> None:
    dep_a = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
    )
    dep_b = create_resource_math_dependency(
        dependency_id="dep-2",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            dependencies=[dep_a, dep_b],
        )


def test_factory_rejects_unresolved_dependency_id_in_cost_term() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        cost_family="validation_blocked",
        owner_domain="RT002_resource_consequence_math",
        policy_route="quarantine_required",
        dependency_ids=["unknown-dep"],
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            cost_terms=[term],
        )


def test_factory_rejects_unresolved_dependency_id_in_cost_bundle() -> None:
    term = create_cost_term(
        term_id="term-1",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        cost_family="validation_blocked",
        owner_domain="RT002_resource_consequence_math",
        policy_route="quarantine_required",
    )
    bundle = create_cost_bundle(
        bundle_id="bundle-1",
        term_ids=["term-1"],
        owner_domain="RT002_resource_consequence_math",
        dependency_ids=["unknown-dep"],
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            cost_terms=[term],
            cost_bundles=[bundle],
        )


def test_factory_rejects_unresolved_dependency_id_in_consequence_term() -> None:
    term = create_consequence_term(
        consequence_id="cons-1",
        subject_binding_id="sub-1",
        value_mode="policy_only",
        consequence_family="visibility_change",
        owner_domain="RT002_resource_consequence_math",
        policy_route="owner_handoff_required",
        dependency_ids=["unknown-dep"],
    )
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            consequence_terms=[term],
        )


def test_factory_rejects_callable_metadata_value() -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            metadata={"bad": lambda: None},
        )


@pytest.mark.parametrize(
    "field_name",
    [
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
        "canon_promotion_authorized",
    ],
)
def test_factory_rejects_true_false_only_authority_field(field_name: str) -> None:
    with pytest.raises(InvalidResourceMathRequestError):
        create_resource_math_request(
            request_id="req-1",
            trace_ref_id="trace-1",
            subject_refs=[_make_primary_subject()],
            **{field_name: True},
        )


def test_resource_math_request_to_dict_returns_copies_and_false_authority() -> None:
    request = _make_populated_request()
    serialized = request.to_dict()
    assert isinstance(serialized, dict)
    assert serialized["request_id"] == "req-1"
    assert serialized["trace_ref_id"] == "trace-1"
    assert isinstance(serialized["subject_refs"], list)
    assert isinstance(serialized["subject_refs"][0], dict)
    assert serialized["subject_refs"] is not list(request.subject_refs)
    assert serialized["resource_refs"][0]["resource_ref_id"] == "res-1"
    assert serialized["state_projection_ref_ids"] == ["proj-1"]
    assert serialized["state_projection_ref_ids"] is not list(request.state_projection_ref_ids)
    assert serialized["provenance_refs"] == ["prov-1"]
    assert serialized["owner_handoff_ref_ids"] == ["handoff-1"]
    assert serialized["metadata"] == {"note": "request"}
    assert isinstance(serialized["metadata"], dict)
    assert serialized["metadata"] is not request.metadata
    assert not isinstance(serialized["metadata"], MappingProxyType)
    for field_name in [
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
        "canon_promotion_authorized",
    ]:
        assert field_name in serialized
        assert serialized[field_name] is False


def test_resource_math_request_metadata_mutation_is_isolated() -> None:
    original = {"nested": {"value": 1}}
    request = create_resource_math_request(
        request_id="req-1",
        trace_ref_id="trace-1",
        subject_refs=[_make_primary_subject()],
        metadata=original,
    )
    original["nested"]["value"] = 999
    assert dict(request.metadata)["nested"]["value"] == 1
    assert request.to_dict()["metadata"]["nested"]["value"] == 1


from dataclasses import replace

from astra_runtime.domain.resource_consequence_math import (
    RESOURCE_MATH_DECISIONS,
    RESOURCE_MATH_STAGES,
    VALIDATION_INTEGRATION_DECISIONS,
    InvalidResourceMathResultError,
    ResourceMathResult,
    create_resource_math_result,
    validate_resource_math_result,
)


def _make_minimal_result(
    request: ResourceMathRequest | None = None,
) -> ResourceMathResult:
    return create_resource_math_result(
        result_id="res-1",
        request_id=request.request_id if request is not None else "req-1",
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        trace_ref_id="trace-1",
    )


def _make_populated_result(
    request: ResourceMathRequest | None = None,
) -> ResourceMathResult:
    dependency = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
    )
    return create_resource_math_result(
        result_id="res-1",
        request_id=request.request_id if request is not None else "req-1",
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        trace_ref_id="trace-1",
        diagnostics=["diag-1"],
        normalized_reference_ids=["norm-1"],
        referenced_subject_binding_ids=["sub-1"],
        referenced_resource_ref_ids=["res-1"],
        referenced_quantity_ids=["qty-1"],
        referenced_cost_term_ids=["term-1"],
        referenced_cost_bundle_ids=["bundle-1"],
        referenced_consequence_term_ids=["cons-1"],
        referenced_dependency_ids=["dep-1"],
        dependencies=[dependency],
        validation_request_ref_id="val-req-1",
        validation_result_ref_id="val-res-1",
        validation_decision="validation_passed",
        metadata={"note": "result"},
    )


def test_result_constants_are_frozensets() -> None:
    assert isinstance(RESOURCE_MATH_STAGES, frozenset)
    assert "calculation_ready_for_review" in RESOURCE_MATH_STAGES
    assert isinstance(RESOURCE_MATH_DECISIONS, frozenset)
    assert "accepted_for_planning" in RESOURCE_MATH_DECISIONS
    assert isinstance(VALIDATION_INTEGRATION_DECISIONS, frozenset)
    assert "validation_passed" in VALIDATION_INTEGRATION_DECISIONS


def test_factory_creates_valid_minimal_resource_math_result() -> None:
    result = _make_minimal_result()
    assert isinstance(result, ResourceMathResult)
    assert result.result_id == "res-1"
    assert result.request_id == "req-1"
    assert result.stage == "calculation_ready_for_review"
    assert result.decision == "accepted_for_planning"
    assert result.blocking is False
    assert result.trace_ref_id == "trace-1"
    assert result.quarantined is False
    assert result.escalated is False


def test_factory_creates_valid_populated_resource_math_result() -> None:
    result = _make_populated_result()
    assert isinstance(result, ResourceMathResult)
    assert result.diagnostics == ("diag-1",)
    assert result.normalized_reference_ids == ("norm-1",)
    assert result.referenced_subject_binding_ids == ("sub-1",)
    assert result.referenced_resource_ref_ids == ("res-1",)
    assert result.referenced_quantity_ids == ("qty-1",)
    assert result.referenced_cost_term_ids == ("term-1",)
    assert result.referenced_cost_bundle_ids == ("bundle-1",)
    assert result.referenced_consequence_term_ids == ("cons-1",)
    assert result.referenced_dependency_ids == ("dep-1",)
    assert len(result.dependencies) == 1
    assert result.validation_request_ref_id == "val-req-1"
    assert result.validation_result_ref_id == "val-res-1"
    assert result.validation_decision == "validation_passed"
    assert dict(result.metadata) == {"note": "result"}


def test_validator_returns_true_for_valid_resource_math_result() -> None:
    result = _make_populated_result()
    assert validate_resource_math_result(result) is True


def test_validator_returns_false_for_non_resource_math_result() -> None:
    assert validate_resource_math_result(None) is False
    assert validate_resource_math_result("result") is False
    assert validate_resource_math_result({}) is False


def test_factory_rejects_empty_result_id() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
        )


def test_factory_rejects_empty_request_id() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
        )


def test_factory_rejects_empty_trace_ref_id() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="",
        )


def test_factory_rejects_invalid_stage() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="unknown_stage",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
        )


def test_factory_rejects_invalid_decision() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="unknown_decision",
            blocking=False,
            trace_ref_id="trace-1",
        )


@pytest.mark.parametrize(
    "stage,decision",
    [
        ("calculation_ready_for_review", "requires_validation_review"),
        ("resource_math_requested", "normalized_for_planning"),
        ("blocked_pending_validation", "accepted_for_planning"),
        ("terms_declared", "blocked_incompatible_policy"),
    ],
)
def test_factory_rejects_invalid_stage_decision_pair(stage: str, decision: str) -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage=stage,
            decision=decision,
            blocking=True,
            trace_ref_id="trace-1",
        )


def test_factory_rejects_non_bool_blocking() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking="no",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_non_bool_quarantined() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            quarantined=1,
        )


def test_factory_rejects_non_bool_escalated() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            escalated="yes",
        )


def test_factory_rejects_invalid_quarantine_flag_pairing() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            quarantined=True,
        )
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="quarantined_for_review",
            decision="quarantined_for_review",
            blocking=True,
            trace_ref_id="trace-1",
            quarantined=False,
        )


def test_factory_rejects_invalid_escalation_flag_pairing() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            escalated=True,
        )
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="escalated_to_doctrine",
            decision="escalated_to_doctrine",
            blocking=True,
            trace_ref_id="trace-1",
            escalated=False,
        )


def test_factory_rejects_bare_string_passed_to_tuple_fields() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            diagnostics="diag-1",
        )
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            referenced_subject_binding_ids="sub-1",
        )


def test_factory_rejects_empty_string_inside_tuple_fields() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            diagnostics=["diag-1", ""],
        )
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            referenced_resource_ref_ids=["res-1", ""],
        )


def test_factory_rejects_duplicate_values_in_typed_scope_tuples() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            referenced_quantity_ids=["qty-1", "qty-1"],
        )


def test_factory_rejects_non_dependency_inside_dependencies() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            dependencies=[{"dependency_id": "dep-1"}],
        )


def test_factory_rejects_duplicate_dependency_id_in_result() -> None:
    dep_a = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-a",
        owner_domain="RT002_resource_consequence_math",
    )
    dep_b = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="unit_ref",
        reference_id="unit-1",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            dependencies=[dep_a, dep_b],
        )


def test_factory_rejects_duplicate_dependency_type_reference_pair_in_result() -> None:
    dep_a = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
    )
    dep_b = create_resource_math_dependency(
        dependency_id="dep-2",
        dependency_type="subject_ref",
        reference_id="ext-sub-1",
        owner_domain="RT002_resource_consequence_math",
    )
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            dependencies=[dep_a, dep_b],
        )


def test_factory_rejects_empty_optional_validation_refs() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            validation_request_ref_id="",
        )
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            validation_result_ref_id="",
        )


def test_factory_rejects_invalid_validation_decision() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            validation_decision="unknown_validation",
        )


def test_factory_rejects_callable_metadata_value_for_result() -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            metadata={"bad": lambda: None},
        )


@pytest.mark.parametrize(
    "field_name",
    [
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
        "canon_promotion_authorized",
    ],
)
def test_factory_rejects_true_false_only_authority_field_for_result(
    field_name: str,
) -> None:
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="req-1",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            **{field_name: True},
        )


def test_factory_accepts_valid_result_with_matching_request() -> None:
    request = _make_populated_request()
    result = _make_populated_result(request=request)
    assert validate_resource_math_result(result, request=request) is True


def test_factory_rejects_mismatched_request_id() -> None:
    request = _make_populated_request()
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id="different-req",
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            referenced_subject_binding_ids=["sub-1"],
            request=request,
        )


@pytest.mark.parametrize(
    "field_name,values",
    [
        ("referenced_subject_binding_ids", ["unknown-sub"]),
        ("referenced_resource_ref_ids", ["unknown-res"]),
        ("referenced_quantity_ids", ["unknown-qty"]),
        ("referenced_cost_term_ids", ["unknown-term"]),
        ("referenced_cost_bundle_ids", ["unknown-bundle"]),
        ("referenced_consequence_term_ids", ["unknown-cons"]),
        ("referenced_dependency_ids", ["unknown-dep"]),
    ],
)
def test_factory_rejects_unresolved_referenced_id_with_request(
    field_name: str,
    values: list[str],
) -> None:
    request = _make_populated_request()
    kwargs: dict[str, object] = {field_name: values}
    with pytest.raises(InvalidResourceMathResultError):
        create_resource_math_result(
            result_id="res-1",
            request_id=request.request_id,
            stage="calculation_ready_for_review",
            decision="accepted_for_planning",
            blocking=False,
            trace_ref_id="trace-1",
            request=request,
            **kwargs,
        )


@pytest.mark.parametrize(
    "field_name,values",
    [
        ("referenced_subject_binding_ids", ("unknown-sub",)),
        ("referenced_resource_ref_ids", ("unknown-res",)),
        ("referenced_quantity_ids", ("unknown-qty",)),
        ("referenced_cost_term_ids", ("unknown-term",)),
        ("referenced_cost_bundle_ids", ("unknown-bundle",)),
        ("referenced_consequence_term_ids", ("unknown-cons",)),
        ("referenced_dependency_ids", ("unknown-dep",)),
    ],
)
def test_validator_rejects_unresolved_referenced_id_with_request(
    field_name: str,
    values: tuple[str, ...],
) -> None:
    request = _make_populated_request()
    result = create_resource_math_result(
        result_id="res-1",
        request_id=request.request_id,
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        trace_ref_id="trace-1",
    )
    unresolved_result = replace(result, **{field_name: values})
    assert validate_resource_math_result(unresolved_result, request=request) is False


def test_resource_math_result_to_dict_returns_copies_and_false_authority() -> None:
    result = _make_populated_result()
    serialized = result.to_dict()
    assert isinstance(serialized, dict)
    assert serialized["result_id"] == "res-1"
    assert serialized["request_id"] == "req-1"
    assert serialized["stage"] == "calculation_ready_for_review"
    assert serialized["decision"] == "accepted_for_planning"
    assert serialized["blocking"] is False
    assert isinstance(serialized["dependencies"], list)
    assert isinstance(serialized["dependencies"][0], dict)
    assert serialized["diagnostics"] == ["diag-1"]
    assert serialized["referenced_quantity_ids"] == ["qty-1"]
    assert serialized["referenced_quantity_ids"] is not list(result.referenced_quantity_ids)
    assert serialized["metadata"] == {"note": "result"}
    assert isinstance(serialized["metadata"], dict)
    assert serialized["metadata"] is not result.metadata
    assert not isinstance(serialized["metadata"], MappingProxyType)
    for field_name in [
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
        "canon_promotion_authorized",
    ]:
        assert field_name in serialized
        assert serialized[field_name] is False


def test_resource_math_result_metadata_mutation_is_isolated() -> None:
    original = {"nested": {"value": 1}}
    result = create_resource_math_result(
        result_id="res-1",
        request_id="req-1",
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        trace_ref_id="trace-1",
        metadata=original,
    )
    original["nested"]["value"] = 999
    assert dict(result.metadata)["nested"]["value"] == 1
    assert result.to_dict()["metadata"]["nested"]["value"] == 1


from astra_runtime.domain.resource_consequence_math import (
    InvalidSettlementProposalError,
    SettlementProposal,
    create_settlement_proposal,
    validate_settlement_proposal,
)


def _make_passing_result() -> ResourceMathResult:
    return create_resource_math_result(
        result_id="res-1",
        request_id="req-1",
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        trace_ref_id="trace-1",
        validation_result_ref_id="val-res-1",
        validation_decision="validation_passed",
    )


def _make_minimal_proposal(
    result: ResourceMathResult | None = None,
) -> SettlementProposal:
    return create_settlement_proposal(
        proposal_id="prop-1",
        result_id=result.result_id if result is not None else "res-1",
        proposed_state_delta_refs=["delta-1"],
        validation_result_ref_id=result.validation_result_ref_id
        if result is not None
        else "val-res-1",
        validation_decision="validation_passed",
        trace_ref_id="trace-1",
    )


def _make_populated_proposal(
    result: ResourceMathResult | None = None,
) -> SettlementProposal:
    dependency = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="state_delta_ref",
        reference_id="delta-1",
        owner_domain="RT002_resource_consequence_math",
        required=True,
        satisfied=True,
    )
    return create_settlement_proposal(
        proposal_id="prop-1",
        result_id=result.result_id if result is not None else "res-1",
        proposed_state_delta_refs=["delta-1", "delta-2"],
        validation_result_ref_id=result.validation_result_ref_id
        if result is not None
        else "val-res-1",
        validation_decision="validation_passed",
        trace_ref_id="trace-1",
        dependencies=[dependency],
        visibility_policy="actor_visible",
        rollback_accounting_refs=["rb-1"],
        metadata={"note": "proposal"},
    )


def test_factory_creates_valid_minimal_settlement_proposal() -> None:
    proposal = _make_minimal_proposal()
    assert isinstance(proposal, SettlementProposal)
    assert proposal.proposal_id == "prop-1"
    assert proposal.result_id == "res-1"
    assert proposal.proposed_state_delta_refs == ("delta-1",)
    assert proposal.validation_result_ref_id == "val-res-1"
    assert proposal.validation_decision == "validation_passed"
    assert proposal.trace_ref_id == "trace-1"
    assert proposal.dependencies == ()
    assert proposal.visibility_policy == "public"
    assert proposal.rollback_accounting_refs == ()


def test_factory_creates_valid_populated_settlement_proposal() -> None:
    proposal = _make_populated_proposal()
    assert isinstance(proposal, SettlementProposal)
    assert proposal.proposed_state_delta_refs == ("delta-1", "delta-2")
    assert len(proposal.dependencies) == 1
    assert proposal.dependencies[0].satisfied is True
    assert proposal.visibility_policy == "actor_visible"
    assert proposal.rollback_accounting_refs == ("rb-1",)
    assert dict(proposal.metadata) == {"note": "proposal"}


def test_validator_returns_true_for_valid_settlement_proposal() -> None:
    proposal = _make_populated_proposal()
    assert validate_settlement_proposal(proposal) is True


def test_validator_returns_false_for_non_settlement_proposal() -> None:
    assert validate_settlement_proposal(None) is False
    assert validate_settlement_proposal("proposal") is False
    assert validate_settlement_proposal({}) is False


def test_factory_rejects_empty_proposal_id() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_empty_result_id() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_empty_validation_result_ref_id() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_empty_trace_ref_id() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="",
        )


def test_factory_rejects_empty_proposed_state_delta_refs() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=[],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_bare_string_proposed_state_delta_refs() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs="delta-1",
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_empty_string_inside_proposed_state_delta_refs() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1", ""],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_duplicate_proposed_state_delta_refs() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1", "delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_invalid_validation_decision() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="unknown",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_validation_decision_not_passed() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_failed",
            trace_ref_id="trace-1",
        )


def test_factory_rejects_non_dependency_inside_dependencies() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            dependencies=[{"dependency_id": "dep-1"}],
        )


def test_factory_rejects_required_dependency_not_satisfied() -> None:
    dependency = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="state_delta_ref",
        reference_id="delta-1",
        owner_domain="RT002_resource_consequence_math",
        required=True,
        satisfied=False,
    )
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            dependencies=[dependency],
        )


def test_factory_rejects_duplicate_dependency_id_in_proposal() -> None:
    dep_a = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="state_delta_ref",
        reference_id="delta-a",
        owner_domain="RT002_resource_consequence_math",
        required=True,
        satisfied=True,
    )
    dep_b = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="state_delta_ref",
        reference_id="delta-b",
        owner_domain="RT002_resource_consequence_math",
        required=True,
        satisfied=True,
    )
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            dependencies=[dep_a, dep_b],
        )


def test_factory_rejects_duplicate_dependency_pair_in_proposal() -> None:
    dep_a = create_resource_math_dependency(
        dependency_id="dep-1",
        dependency_type="state_delta_ref",
        reference_id="delta-1",
        owner_domain="RT002_resource_consequence_math",
        required=True,
        satisfied=True,
    )
    dep_b = create_resource_math_dependency(
        dependency_id="dep-2",
        dependency_type="state_delta_ref",
        reference_id="delta-1",
        owner_domain="RT002_resource_consequence_math",
        required=True,
        satisfied=True,
    )
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            dependencies=[dep_a, dep_b],
        )


def test_factory_rejects_invalid_visibility_policy() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            visibility_policy="all_visible",
        )


def test_factory_rejects_bare_string_rollback_accounting_refs() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            rollback_accounting_refs="rb-1",
        )


def test_factory_rejects_empty_string_inside_rollback_accounting_refs() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            rollback_accounting_refs=["rb-1", ""],
        )


def test_factory_rejects_callable_metadata_value_for_proposal() -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            metadata={"bad": lambda: None},
        )


@pytest.mark.parametrize(
    "field_name",
    [
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
        "canon_promotion_authorized",
    ],
)
def test_factory_rejects_true_false_only_authority_field_for_proposal(
    field_name: str,
) -> None:
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="res-1",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="val-res-1",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            **{field_name: True},
        )


def test_factory_accepts_valid_proposal_with_matching_result() -> None:
    result = _make_passing_result()
    proposal = _make_minimal_proposal(result=result)
    assert validate_settlement_proposal(proposal, result=result) is True


def test_factory_rejects_mismatched_result_id() -> None:
    result = _make_passing_result()
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id="different-res",
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id=result.validation_result_ref_id,
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            result=result,
        )


def test_factory_rejects_mismatched_validation_result_ref_id() -> None:
    result = _make_passing_result()
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id=result.result_id,
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id="different-val-res",
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            result=result,
        )


def test_factory_rejects_mismatched_validation_decision() -> None:
    result = create_resource_math_result(
        result_id="res-1",
        request_id="req-1",
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        trace_ref_id="trace-1",
        validation_result_ref_id="val-res-1",
        validation_decision="validation_failed",
    )
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id=result.result_id,
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id=result.validation_result_ref_id,
            validation_decision="validation_passed",
            trace_ref_id="trace-1",
            result=result,
        )


def test_factory_rejects_result_whose_validation_decision_is_not_passed() -> None:
    result = create_resource_math_result(
        result_id="res-1",
        request_id="req-1",
        stage="calculation_ready_for_review",
        decision="accepted_for_planning",
        blocking=False,
        trace_ref_id="trace-1",
        validation_result_ref_id="val-res-1",
        validation_decision="validation_failed",
    )
    with pytest.raises(InvalidSettlementProposalError):
        create_settlement_proposal(
            proposal_id="prop-1",
            result_id=result.result_id,
            proposed_state_delta_refs=["delta-1"],
            validation_result_ref_id=result.validation_result_ref_id,
            validation_decision=result.validation_decision,
            trace_ref_id="trace-1",
            result=result,
        )


def test_settlement_proposal_to_dict_returns_copies_and_false_authority() -> None:
    proposal = _make_populated_proposal()
    serialized = proposal.to_dict()
    assert isinstance(serialized, dict)
    assert serialized["proposal_id"] == "prop-1"
    assert serialized["result_id"] == "res-1"
    assert serialized["proposed_state_delta_refs"] == ["delta-1", "delta-2"]
    assert serialized["proposed_state_delta_refs"] is not list(
        proposal.proposed_state_delta_refs
    )
    assert serialized["validation_result_ref_id"] == "val-res-1"
    assert serialized["validation_decision"] == "validation_passed"
    assert serialized["trace_ref_id"] == "trace-1"
    assert isinstance(serialized["dependencies"], list)
    assert isinstance(serialized["dependencies"][0], dict)
    assert serialized["rollback_accounting_refs"] == ["rb-1"]
    assert serialized["metadata"] == {"note": "proposal"}
    assert isinstance(serialized["metadata"], dict)
    assert serialized["metadata"] is not proposal.metadata
    assert not isinstance(serialized["metadata"], MappingProxyType)
    assert "request_id" not in serialized
    for field_name in [
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
        "canon_promotion_authorized",
    ]:
        assert field_name in serialized
        assert serialized[field_name] is False


def test_settlement_proposal_has_no_request_id_field() -> None:
    proposal = _make_minimal_proposal()
    assert not hasattr(proposal, "request_id")


def test_settlement_proposal_metadata_mutation_is_isolated() -> None:
    original = {"nested": {"value": 1}}
    proposal = create_settlement_proposal(
        proposal_id="prop-1",
        result_id="res-1",
        proposed_state_delta_refs=["delta-1"],
        validation_result_ref_id="val-res-1",
        validation_decision="validation_passed",
        trace_ref_id="trace-1",
        metadata=original,
    )
    original["nested"]["value"] = 999
    assert dict(proposal.metadata)["nested"]["value"] == 1
    assert proposal.to_dict()["metadata"]["nested"]["value"] == 1


import astra_runtime.domain as domain_package
from astra_runtime.domain import (
    ATOMICITY_POLICIES,
    CONSEQUENCE_FAMILIES,
    CONVERSION_POLICIES,
    COST_FAMILIES,
    COST_OUTCOME_POLICIES,
    COST_TIMING_POLICIES,
    CostBundle,
    CostTerm,
    ConsequenceTerm,
    InvalidCostBundleError,
    InvalidCostTermError,
    InvalidConsequenceTermError,
    InvalidQuantitySpecificationError,
    InvalidResourceMathDependencyError,
    InvalidResourceMathRequestError,
    InvalidResourceMathResultError,
    InvalidResourceMathSubjectReferenceError,
    InvalidResourceReferenceError,
    InvalidSettlementProposalError,
    ORDERING_POLICIES,
    PARTIAL_SETTLEMENT_POLICIES,
    QUANTITY_NEGATIVE_VALUE_POLICIES,
    QUANTITY_REPRESENTATION_KINDS,
    QuantitySpecification,
    RESOURCE_FAMILIES,
    RESOURCE_MATH_DECISIONS,
    RESOURCE_MATH_DEPENDENCY_TYPES,
    RESOURCE_MATH_OWNER_DOMAINS,
    RESOURCE_MATH_STAGES,
    RESOURCE_MATH_SUBJECT_ROLES,
    RESOURCE_MATH_SUBJECT_TYPES,
    RESOURCE_TERM_POLICY_ROUTES,
    RESOURCE_TERM_VALUE_MODES,
    ROUNDING_POLICIES,
    ResourceMathDependency,
    ResourceMathError,
    ResourceMathRequest,
    ResourceMathResult,
    ResourceMathSubjectReference,
    ResourceReference,
    SettlementProposal,
    VALIDATION_INTEGRATION_DECISIONS,
    VISIBILITY_POLICIES,
    create_cost_bundle,
    create_cost_term,
    create_consequence_term,
    create_quantity_specification,
    create_resource_math_dependency,
    create_resource_math_request,
    create_resource_math_result,
    create_resource_math_subject_reference,
    create_resource_reference,
    create_settlement_proposal,
    validate_cost_bundle,
    validate_cost_term,
    validate_consequence_term,
    validate_quantity_specification,
    validate_resource_math_dependency,
    validate_resource_math_request,
    validate_resource_math_result,
    validate_resource_math_subject_reference,
    validate_resource_reference,
    validate_settlement_proposal,
)


def test_domain_package_exports_all_ten_dataclasses() -> None:
    assert ResourceMathSubjectReference is domain_package.ResourceMathSubjectReference
    assert ResourceReference is domain_package.ResourceReference
    assert QuantitySpecification is domain_package.QuantitySpecification
    assert ResourceMathDependency is domain_package.ResourceMathDependency
    assert CostTerm is domain_package.CostTerm
    assert ConsequenceTerm is domain_package.ConsequenceTerm
    assert CostBundle is domain_package.CostBundle
    assert ResourceMathRequest is domain_package.ResourceMathRequest
    assert ResourceMathResult is domain_package.ResourceMathResult
    assert SettlementProposal is domain_package.SettlementProposal


def test_domain_package_exports_all_factories() -> None:
    assert callable(create_resource_math_subject_reference)
    assert callable(create_resource_reference)
    assert callable(create_quantity_specification)
    assert callable(create_resource_math_dependency)
    assert callable(create_cost_term)
    assert callable(create_consequence_term)
    assert callable(create_cost_bundle)
    assert callable(create_resource_math_request)
    assert callable(create_resource_math_result)
    assert callable(create_settlement_proposal)


def test_domain_package_exports_all_validators() -> None:
    assert callable(validate_resource_math_subject_reference)
    assert callable(validate_resource_reference)
    assert callable(validate_quantity_specification)
    assert callable(validate_resource_math_dependency)
    assert callable(validate_cost_term)
    assert callable(validate_consequence_term)
    assert callable(validate_cost_bundle)
    assert callable(validate_resource_math_request)
    assert callable(validate_resource_math_result)
    assert callable(validate_settlement_proposal)


def test_domain_package_exports_all_exceptions() -> None:
    assert issubclass(ResourceMathError, Exception)
    assert issubclass(InvalidResourceMathSubjectReferenceError, ResourceMathError)
    assert issubclass(InvalidResourceReferenceError, ResourceMathError)
    assert issubclass(InvalidQuantitySpecificationError, ResourceMathError)
    assert issubclass(InvalidResourceMathDependencyError, ResourceMathError)
    assert issubclass(InvalidCostTermError, ResourceMathError)
    assert issubclass(InvalidConsequenceTermError, ResourceMathError)
    assert issubclass(InvalidCostBundleError, ResourceMathError)
    assert issubclass(InvalidResourceMathRequestError, ResourceMathError)
    assert issubclass(InvalidResourceMathResultError, ResourceMathError)
    assert issubclass(InvalidSettlementProposalError, ResourceMathError)


def test_domain_package_exports_public_controlled_constants() -> None:
    constants = [
        RESOURCE_MATH_STAGES,
        RESOURCE_MATH_DECISIONS,
        RESOURCE_FAMILIES,
        COST_FAMILIES,
        CONSEQUENCE_FAMILIES,
        COST_TIMING_POLICIES,
        COST_OUTCOME_POLICIES,
        QUANTITY_REPRESENTATION_KINDS,
        CONVERSION_POLICIES,
        ROUNDING_POLICIES,
        QUANTITY_NEGATIVE_VALUE_POLICIES,
        VISIBILITY_POLICIES,
        RESOURCE_MATH_DEPENDENCY_TYPES,
        RESOURCE_MATH_SUBJECT_TYPES,
        RESOURCE_MATH_SUBJECT_ROLES,
        RESOURCE_MATH_OWNER_DOMAINS,
        RESOURCE_TERM_VALUE_MODES,
        RESOURCE_TERM_POLICY_ROUTES,
        ATOMICITY_POLICIES,
        ORDERING_POLICIES,
        PARTIAL_SETTLEMENT_POLICIES,
        VALIDATION_INTEGRATION_DECISIONS,
    ]
    for const in constants:
        assert isinstance(const, frozenset)
    assert "validation_passed" in VALIDATION_INTEGRATION_DECISIONS
    assert "accepted_for_planning" in RESOURCE_MATH_DECISIONS
    assert "actor" in RESOURCE_MATH_SUBJECT_TYPES


def test_domain_package_all_excludes_private_helpers() -> None:
    assert hasattr(domain_package, "__all__")
    for name in domain_package.__all__:
        assert not name.startswith("_"), f"{name!r} should not be exported"
    assert "_validate_non_empty_string" not in domain_package.__all__
    assert "_RESOURCE_MATH_FALSE_ONLY_AUTHORITY_FIELDS" not in domain_package.__all__
    assert "_STAGE_DECISION_MATRIX" not in domain_package.__all__
