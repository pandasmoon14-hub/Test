"""PR-6 Slice 3 — VisibleSummaryPacket tests.

Tests cover:
* Package exports from astra_runtime.domain
* Factory creates a valid VisibleSummaryPacket
* Direct dataclass construction normalizes list fields to tuples
* Direct dataclass construction rejects bare strings for all tuple fields
* Direct construction freezes metadata with MappingProxyType
* Mutating original metadata after construction does not affect packet metadata
* Omitted/empty non_authority_seal defaults to tuple(sorted(NON_AUTHORITY_SEAL))
* Invalid packet_kind rejected
* Empty summary_ref rejected
* Empty summary_scope rejected
* Empty summary_timestamp rejected
* Empty visible_fact_refs rejected
* hidden_information_excluded=False rejected
* committed_state_only=False rejected
* Validator returns True for valid packet
* Validator rejects manually corrupted packet via object.__setattr__
* to_dict() is deterministic and contains no forbidden fields
"""

from __future__ import annotations

import copy
from types import MappingProxyType

import pytest

from astra_runtime.domain.context_packet_compiler import (
    NON_AUTHORITY_SEAL,
    InvalidVisibleSummaryPacketError,
    VisibleSummaryPacket,
    create_visible_summary_packet,
    validate_visible_summary_packet,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_valid_kwargs() -> dict:
    """Return the minimum keyword arguments for a valid VisibleSummaryPacket."""
    return {
        "summary_ref": "summary-ref-001",
        "summary_scope": "scene",
        "summary_timestamp": "2025-01-01T00:00:00Z",
        "visible_fact_refs": ["fact-1", "fact-2"],
    }


def _build_valid_packet(**overrides) -> VisibleSummaryPacket:
    """Build a valid VisibleSummaryPacket with optional field overrides."""
    kwargs = _make_valid_kwargs()
    kwargs.update(overrides)
    return create_visible_summary_packet(**kwargs)


# ---------------------------------------------------------------------------
# 1. Package exports
# ---------------------------------------------------------------------------


class TestExports:
    """Verify the public surface is accessible from astra_runtime.domain."""

    def test_error_class_exported(self) -> None:
        from astra_runtime.domain import InvalidVisibleSummaryPacketError as cls

        assert cls is InvalidVisibleSummaryPacketError

    def test_dataclass_exported(self) -> None:
        from astra_runtime.domain import VisibleSummaryPacket as cls

        assert cls is VisibleSummaryPacket

    def test_factory_exported(self) -> None:
        from astra_runtime.domain import create_visible_summary_packet as fn

        assert fn is create_visible_summary_packet

    def test_validator_exported(self) -> None:
        from astra_runtime.domain import validate_visible_summary_packet as fn

        assert fn is validate_visible_summary_packet


# ---------------------------------------------------------------------------
# 2. Factory creates a valid VisibleSummaryPacket
# ---------------------------------------------------------------------------


class TestFactoryCreation:

    def test_factory_returns_valid_packet(self) -> None:
        packet = _build_valid_packet()
        assert isinstance(packet, VisibleSummaryPacket)
        assert packet.packet_kind == "visible_summary"
        assert packet.summary_ref == "summary-ref-001"
        assert packet.summary_scope == "scene"
        assert packet.summary_timestamp == "2025-01-01T00:00:00Z"
        assert packet.visible_fact_refs == ("fact-1", "fact-2")
        assert packet.hidden_information_excluded is True
        assert packet.committed_state_only is True

    def test_factory_with_all_optional_fields(self) -> None:
        packet = _build_valid_packet(
            actor_refs=["actor-1"],
            location_refs=["loc-1"],
            faction_refs=["faction-1"],
            item_refs=["item-1"],
            condition_refs=["cond-1"],
            unresolved_visible_refs=["unresolved-1"],
            forbidden_claims=["claim-1"],
            non_authority_seal=["custom-seal"],
            metadata={"key": "value"},
        )
        assert packet.actor_refs == ("actor-1",)
        assert packet.location_refs == ("loc-1",)
        assert packet.faction_refs == ("faction-1",)
        assert packet.item_refs == ("item-1",)
        assert packet.condition_refs == ("cond-1",)
        assert packet.unresolved_visible_refs == ("unresolved-1",)
        assert packet.forbidden_claims == ("claim-1",)
        assert packet.non_authority_seal == ("custom-seal",)
        assert dict(packet.metadata) == {"key": "value"}


# ---------------------------------------------------------------------------
# 3. Direct dataclass construction normalizes list fields to tuples
# ---------------------------------------------------------------------------


class TestDirectConstructionNormalization:

    def test_lists_normalized_to_tuples(self) -> None:
        packet = VisibleSummaryPacket(
            packet_kind="visible_summary",
            summary_ref="ref-1",
            summary_scope="scene",
            summary_timestamp="2025-01-01T00:00:00Z",
            visible_fact_refs=["fact-1"],
            actor_refs=["actor-1"],
            location_refs=["loc-1"],
            faction_refs=["faction-1"],
            item_refs=["item-1"],
            condition_refs=["cond-1"],
            unresolved_visible_refs=["ur-1"],
            forbidden_claims=["fc-1"],
        )
        assert isinstance(packet.visible_fact_refs, tuple)
        assert isinstance(packet.actor_refs, tuple)
        assert isinstance(packet.location_refs, tuple)
        assert isinstance(packet.faction_refs, tuple)
        assert isinstance(packet.item_refs, tuple)
        assert isinstance(packet.condition_refs, tuple)
        assert isinstance(packet.unresolved_visible_refs, tuple)
        assert isinstance(packet.forbidden_claims, tuple)


# ---------------------------------------------------------------------------
# 4. Direct construction rejects bare strings for all tuple fields
# ---------------------------------------------------------------------------


class TestBareStringRejection:

    @pytest.mark.parametrize(
        "field_name",
        [
            "visible_fact_refs",
            "actor_refs",
            "location_refs",
            "faction_refs",
            "item_refs",
            "condition_refs",
            "unresolved_visible_refs",
            "forbidden_claims",
            "non_authority_seal",
        ],
    )
    def test_bare_string_rejected(self, field_name: str) -> None:
        base = {
            "packet_kind": "visible_summary",
            "summary_ref": "ref-1",
            "summary_scope": "scene",
            "summary_timestamp": "2025-01-01T00:00:00Z",
            "visible_fact_refs": ["fact-1"],
        }
        base[field_name] = "bare-string-value"
        with pytest.raises(InvalidVisibleSummaryPacketError, match="must not be a bare string"):
            VisibleSummaryPacket(**base)


# ---------------------------------------------------------------------------
# 5. Direct construction freezes metadata with MappingProxyType
# ---------------------------------------------------------------------------


class TestMetadataFreezing:

    def test_metadata_is_mapping_proxy(self) -> None:
        packet = _build_valid_packet(metadata={"a": 1})
        assert isinstance(packet.metadata, MappingProxyType)

    def test_metadata_deep_copied(self) -> None:
        inner = {"nested": {"deep": True}}
        packet = _build_valid_packet(metadata=inner)
        # Mutate original
        inner["nested"]["deep"] = False
        # Packet metadata should be unaffected
        assert packet.metadata["nested"]["deep"] is True


# ---------------------------------------------------------------------------
# 6. Mutating original metadata after construction does not affect packet
# ---------------------------------------------------------------------------


class TestMetadataIsolation:

    def test_mutation_after_construction_no_effect(self) -> None:
        original = {"x": [1, 2, 3]}
        packet = _build_valid_packet(metadata=original)
        original["x"].append(4)
        original["new_key"] = "new_value"
        assert packet.metadata["x"] == [1, 2, 3]
        assert "new_key" not in packet.metadata


# ---------------------------------------------------------------------------
# 7. Omitted non_authority_seal defaults to sorted NON_AUTHORITY_SEAL
# ---------------------------------------------------------------------------


class TestDefaultNonAuthoritySeal:

    def test_empty_seal_defaults_to_sorted_non_authority_seal(self) -> None:
        packet = _build_valid_packet()
        assert packet.non_authority_seal == tuple(sorted(NON_AUTHORITY_SEAL))
        assert len(packet.non_authority_seal) == len(NON_AUTHORITY_SEAL)

    def test_custom_seal_preserved(self) -> None:
        packet = _build_valid_packet(non_authority_seal=["custom-a", "custom-b"])
        assert packet.non_authority_seal == ("custom-a", "custom-b")


# ---------------------------------------------------------------------------
# 8. Invalid packet_kind rejected
# ---------------------------------------------------------------------------


class TestInvalidPacketKind:

    def test_wrong_kind_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="packet_kind"):
            _build_valid_packet(packet_kind="wrong_kind")

    def test_empty_kind_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="packet_kind"):
            _build_valid_packet(packet_kind="")


# ---------------------------------------------------------------------------
# 9. Empty summary_ref rejected
# ---------------------------------------------------------------------------


class TestEmptySummaryRef:

    def test_empty_summary_ref_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="summary_ref"):
            _build_valid_packet(summary_ref="")


# ---------------------------------------------------------------------------
# 10. Empty summary_scope rejected
# ---------------------------------------------------------------------------


class TestEmptySummaryScope:

    def test_empty_summary_scope_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="summary_scope"):
            _build_valid_packet(summary_scope="")


# ---------------------------------------------------------------------------
# 11. Empty summary_timestamp rejected
# ---------------------------------------------------------------------------


class TestEmptySummaryTimestamp:

    def test_empty_summary_timestamp_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="summary_timestamp"):
            _build_valid_packet(summary_timestamp="")


# ---------------------------------------------------------------------------
# 12. Empty visible_fact_refs rejected
# ---------------------------------------------------------------------------


class TestEmptyVisibleFactRefs:

    def test_empty_visible_fact_refs_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="visible_fact_refs"):
            _build_valid_packet(visible_fact_refs=[])


# ---------------------------------------------------------------------------
# 13. hidden_information_excluded=False rejected
# ---------------------------------------------------------------------------


class TestHiddenInformationExcluded:

    def test_false_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="hidden_information_excluded"):
            _build_valid_packet(hidden_information_excluded=False)


# ---------------------------------------------------------------------------
# 14. committed_state_only=False rejected
# ---------------------------------------------------------------------------


class TestCommittedStateOnly:

    def test_false_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="committed_state_only"):
            _build_valid_packet(committed_state_only=False)


# ---------------------------------------------------------------------------
# 15. Validator returns True for valid packet
# ---------------------------------------------------------------------------


class TestValidatorPositive:

    def test_valid_packet_passes_validation(self) -> None:
        packet = _build_valid_packet()
        assert validate_visible_summary_packet(packet) is True


# ---------------------------------------------------------------------------
# 16. Validator rejects manually corrupted packet
# ---------------------------------------------------------------------------


class TestValidatorCorruption:

    def test_corrupted_packet_kind_rejected(self) -> None:
        packet = _build_valid_packet()
        object.__setattr__(packet, "packet_kind", "corrupted_kind")
        with pytest.raises(InvalidVisibleSummaryPacketError, match="packet_kind"):
            validate_visible_summary_packet(packet)

    def test_corrupted_visible_fact_refs_rejected(self) -> None:
        packet = _build_valid_packet()
        object.__setattr__(packet, "visible_fact_refs", ())
        with pytest.raises(InvalidVisibleSummaryPacketError, match="visible_fact_refs"):
            validate_visible_summary_packet(packet)

    def test_corrupted_hidden_information_excluded_rejected(self) -> None:
        packet = _build_valid_packet()
        object.__setattr__(packet, "hidden_information_excluded", False)
        with pytest.raises(InvalidVisibleSummaryPacketError, match="hidden_information_excluded"):
            validate_visible_summary_packet(packet)

    def test_corrupted_committed_state_only_rejected(self) -> None:
        packet = _build_valid_packet()
        object.__setattr__(packet, "committed_state_only", False)
        with pytest.raises(InvalidVisibleSummaryPacketError, match="committed_state_only"):
            validate_visible_summary_packet(packet)

    def test_corrupted_metadata_type_rejected(self) -> None:
        packet = _build_valid_packet()
        object.__setattr__(packet, "metadata", {"not": "frozen"})
        with pytest.raises(InvalidVisibleSummaryPacketError, match="metadata"):
            validate_visible_summary_packet(packet)

    def test_non_instance_rejected(self) -> None:
        with pytest.raises(InvalidVisibleSummaryPacketError, match="must be a VisibleSummaryPacket"):
            validate_visible_summary_packet("not_a_packet")


# ---------------------------------------------------------------------------
# 17. to_dict() is deterministic and contains no forbidden fields
# ---------------------------------------------------------------------------


FORBIDDEN_STRINGS = [
    "hidden_fact",
    "hidden_information",
    "secret",
    "unrevealed",
    "event_commitment",
    "commit_event",
    "state_delta",
    "mutation",
    "roll_result",
    "rng_result",
    "narration_output",
    "model_output",
]


FORBIDDEN_DICT_KEYS = [
    "hidden_fact",
    "hidden_information",
    "secret",
    "unrevealed",
    "event_commitment",
    "commit_event",
    "state_delta",
    "mutation",
    "roll_result",
    "rng_result",
    "narration_output",
    "model_output",
]


class TestToDict:

    def test_to_dict_deterministic(self) -> None:
        packet = _build_valid_packet(metadata={"key": "value"})
        d1 = packet.to_dict()
        d2 = packet.to_dict()
        assert d1 == d2
        assert d1 is not d2

    def test_to_dict_expected_keys(self) -> None:
        packet = _build_valid_packet()
        d = packet.to_dict()
        expected_keys = {
            "packet_kind",
            "summary_ref",
            "summary_scope",
            "summary_timestamp",
            "visible_fact_refs",
            "actor_refs",
            "location_refs",
            "faction_refs",
            "item_refs",
            "condition_refs",
            "unresolved_visible_refs",
            "forbidden_claims",
            "hidden_information_excluded",
            "committed_state_only",
            "non_authority_seal",
            "metadata",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_no_forbidden_keys(self) -> None:
        """No dict key must match a forbidden authority/commit/mutation field."""
        packet = _build_valid_packet()
        d = packet.to_dict()
        for forbidden in FORBIDDEN_DICT_KEYS:
            assert forbidden not in d.keys(), (
                f"to_dict() must not contain forbidden key {forbidden!r}"
            )

    def test_to_dict_no_hidden_or_commit_values_in_dict(self) -> None:
        """Serialized value strings must not carry forbidden authority tokens.

        Some forbidden strings are substrings of negated safety-seal values
        (e.g. ``no_event_commitment``). Those are safety markers, not leaked
        authority; they are excluded from the substring check.
        """
        packet = _build_valid_packet()
        d = packet.to_dict()
        serialized = str(d)
        # Strings that are substrings of safety-seal values are excluded.
        _seal_substrings = {"hidden_information", "event_commitment", "mutation"}
        for forbidden in FORBIDDEN_STRINGS:
            if forbidden in _seal_substrings:
                continue
            assert forbidden not in serialized, (
                f"to_dict() serialized output must not contain {forbidden!r}"
            )

    def test_to_dict_metadata_is_plain_dict(self) -> None:
        packet = _build_valid_packet(metadata={"nested": {"a": 1}})
        d = packet.to_dict()
        assert isinstance(d["metadata"], dict)
        # Verify deep copy — mutating serialized metadata should not affect packet
        d["metadata"]["nested"]["a"] = 999
        assert packet.metadata["nested"]["a"] == 1

    def test_to_dict_tuple_fields_are_lists(self) -> None:
        packet = _build_valid_packet(
            actor_refs=["a1"],
            location_refs=["l1"],
            faction_refs=["f1"],
            item_refs=["i1"],
            condition_refs=["c1"],
            unresolved_visible_refs=["u1"],
            forbidden_claims=["fc1"],
        )
        d = packet.to_dict()
        for key in (
            "visible_fact_refs",
            "actor_refs",
            "location_refs",
            "faction_refs",
            "item_refs",
            "condition_refs",
            "unresolved_visible_refs",
            "forbidden_claims",
            "non_authority_seal",
        ):
            assert isinstance(d[key], list), f"{key} should be a list in to_dict()"
