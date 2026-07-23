"""Tests for deterministic RNG interface skeleton — RUNTIME-IMPL-PR-4."""

from tests.runtime_domain_package_manifest import (
    AUTHORIZED_RUNTIME_DOMAIN_ENTRIES,
    AUTHORIZED_RUNTIME_DOMAIN_FILES,
)

import os
import random

import pytest

from astra_runtime.kernel.rng_interface import (
    InvalidRNGInvocationError,
    InvalidRNGResultError,
    RNGInvocation,
    RNGResult,
    create_rng_invocation,
    create_rng_result,
    deterministic_int,
    validate_rng_invocation,
    validate_rng_result,
)


class TestCreateRNGInvocation:
    def test_valid_creation(self):
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20)
        assert isinstance(inv, RNGInvocation)

    def test_preserves_rng_id(self):
        inv = create_rng_invocation("rng-42", "seed-a", "attack_roll", 1, 20)
        assert inv.rng_id == "rng-42"

    def test_preserves_seed(self):
        inv = create_rng_invocation("rng-1", "my-seed", "attack_roll", 1, 20)
        assert inv.seed == "my-seed"

    def test_preserves_purpose(self):
        inv = create_rng_invocation("rng-1", "seed-a", "damage_roll", 1, 6)
        assert inv.purpose == "damage_roll"

    def test_preserves_range_min(self):
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 3, 18)
        assert inv.range_min == 3

    def test_preserves_range_max(self):
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 100)
        assert inv.range_max == 100

    def test_rejects_empty_rng_id(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("", "seed-a", "attack_roll", 1, 20)

    def test_rejects_whitespace_rng_id(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("   ", "seed-a", "attack_roll", 1, 20)

    def test_rejects_empty_seed(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "", "attack_roll", 1, 20)

    def test_rejects_empty_purpose(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "seed-a", "", 1, 20)

    def test_rejects_non_int_range_min(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "seed-a", "attack_roll", 1.5, 20)

    def test_rejects_non_int_range_max(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20.0)

    def test_rejects_bool_range_min(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "seed-a", "attack_roll", True, 20)

    def test_rejects_bool_range_max(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, False)

    def test_rejects_range_min_greater_than_max(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "seed-a", "attack_roll", 20, 1)

    def test_range_min_equals_max_accepted(self):
        inv = create_rng_invocation("rng-1", "seed-a", "fixed", 5, 5)
        assert inv.range_min == 5
        assert inv.range_max == 5

    def test_metadata_defaults_to_empty_mapping(self):
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20)
        assert dict(inv.metadata) == {}

    def test_metadata_copy_safe(self):
        original = {"context": "combat"}
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20, metadata=original)
        original["context"] = "changed"
        assert inv.metadata["context"] == "combat"

    def test_metadata_nested_copy_safe(self):
        original = {"ctx": {"k": "v"}}
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20, metadata=original)
        original["ctx"]["k"] = "changed"
        assert inv.metadata["ctx"]["k"] == "v"

    def test_reject_non_mapping_metadata(self):
        with pytest.raises(InvalidRNGInvocationError):
            create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20, metadata="bad")


class TestRNGInvocationToDict:
    def test_to_dict_returns_dict(self):
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20)
        result = inv.to_dict()
        assert isinstance(result, dict)
        assert result["rng_id"] == "rng-1"
        assert result["seed"] == "seed-a"
        assert result["purpose"] == "attack_roll"
        assert result["range_min"] == 1
        assert result["range_max"] == 20

    def test_to_dict_returns_deep_copy(self):
        inv = create_rng_invocation(
            "rng-1", "seed-a", "attack_roll", 1, 20,
            metadata={"nested": {"b": 2}},
        )
        result = inv.to_dict()
        result["metadata"]["nested"]["b"] = 999
        assert inv.metadata["nested"]["b"] == 2


class TestValidateRNGInvocation:
    def test_valid_invocation_accepted(self):
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20)
        assert validate_rng_invocation(inv) is True

    def test_invalid_object_rejected(self):
        assert validate_rng_invocation("not-an-invocation") is False

    def test_none_rejected(self):
        assert validate_rng_invocation(None) is False

    def test_dict_rejected(self):
        assert validate_rng_invocation({"rng_id": "rng-1"}) is False


class TestCreateRNGResult:
    def test_valid_creation(self):
        res = create_rng_result("rng-1", "seed-a", 15, 1, 20)
        assert isinstance(res, RNGResult)

    def test_preserves_fields(self):
        res = create_rng_result("rng-1", "seed-a", 15, 1, 20)
        assert res.rng_id == "rng-1"
        assert res.seed == "seed-a"
        assert res.value == 15
        assert res.range_min == 1
        assert res.range_max == 20

    def test_rejects_value_below_range(self):
        with pytest.raises(InvalidRNGResultError):
            create_rng_result("rng-1", "seed-a", 0, 1, 20)

    def test_rejects_value_above_range(self):
        with pytest.raises(InvalidRNGResultError):
            create_rng_result("rng-1", "seed-a", 21, 1, 20)

    def test_rejects_bool_value(self):
        with pytest.raises(InvalidRNGResultError):
            create_rng_result("rng-1", "seed-a", True, 0, 1)

    def test_boundary_value_min_accepted(self):
        res = create_rng_result("rng-1", "seed-a", 1, 1, 20)
        assert res.value == 1

    def test_boundary_value_max_accepted(self):
        res = create_rng_result("rng-1", "seed-a", 20, 1, 20)
        assert res.value == 20

    def test_metadata_defaults_to_empty(self):
        res = create_rng_result("rng-1", "seed-a", 5, 1, 10)
        assert dict(res.metadata) == {}

    def test_to_dict_returns_deep_copy(self):
        res = create_rng_result(
            "rng-1", "seed-a", 5, 1, 10,
            metadata={"nested": {"x": 1}},
        )
        d = res.to_dict()
        d["metadata"]["nested"]["x"] = 999
        assert res.metadata["nested"]["x"] == 1


class TestValidateRNGResult:
    def test_valid_result_accepted(self):
        res = create_rng_result("rng-1", "seed-a", 10, 1, 20)
        assert validate_rng_result(res) is True

    def test_invalid_object_rejected(self):
        assert validate_rng_result("not-a-result") is False


class TestRNGInvocationImmutability:
    def test_frozen_dataclass(self):
        inv = create_rng_invocation("rng-1", "seed-a", "attack_roll", 1, 20)
        with pytest.raises(AttributeError):
            inv.rng_id = "changed"


class TestDeterministicInt:
    def test_same_seed_same_result(self):
        a = deterministic_int("test-seed", 1, 100)
        b = deterministic_int("test-seed", 1, 100)
        assert a == b

    def test_within_inclusive_range(self):
        for seed in ["alpha", "beta", "gamma", "delta", "epsilon"]:
            val = deterministic_int(seed, 1, 20)
            assert 1 <= val <= 20

    def test_different_seeds_can_differ(self):
        results = {deterministic_int(f"seed-{i}", 1, 1000) for i in range(20)}
        assert len(results) > 1

    def test_does_not_mutate_global_random_state(self):
        random.seed(12345)
        before = random.random()
        random.seed(12345)
        deterministic_int("test-seed", 1, 100)
        after = random.random()
        assert before == after

    def test_single_value_range(self):
        val = deterministic_int("any-seed", 7, 7)
        assert val == 7


class TestNoUnauthorizedRNGMethods:
    """RNG interface must not contain session/store/persist/replay/dice methods."""

    def test_no_session_store_replay(self):
        inv = create_rng_invocation("rng-1", "seed-a", "test", 1, 6)
        for attr in ["session", "store", "persist", "replay", "hash", "save", "append"]:
            assert not hasattr(inv, attr)

    def test_no_dice_expression_parser(self):
        import astra_runtime.kernel.rng_interface as mod
        for attr in ["parse_dice", "roll_dice", "DiceExpression", "dice_expression"]:
            assert not hasattr(mod, attr)


class TestNoUnauthorizedModules:
    """Guardrail tests — future modules must not exist yet."""

    KERNEL_DIR = os.path.join(
        os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "kernel"
    )

    def test_domain_package_contains_only_authorized_modules(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "domain"
        )
        assert os.path.isdir(path), "Domain package should exist after PR-1A"
        allowed = set(AUTHORIZED_RUNTIME_DOMAIN_ENTRIES)
        actual = set(os.listdir(path))
        unauthorized = actual - allowed
        assert not unauthorized, f"Unauthorized domain modules: {unauthorized}"

    def test_no_model_integration_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "model"
        )
        assert not os.path.isdir(path), "Unauthorized model integration package exists"

    def test_no_prompt_template_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "prompts"
        )
        assert not os.path.isdir(path), "Unauthorized prompt template package exists"

    def test_no_live_play_adapter_package(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "astra_runtime", "live_play"
        )
        assert not os.path.isdir(path), "Unauthorized live-play adapter package exists"
