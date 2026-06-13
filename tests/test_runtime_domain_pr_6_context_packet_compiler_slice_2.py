"""Focused tests for PR-6 context packet compiler Slice 2 — NoCommitIntentPacket."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from astra_runtime.domain.context_packet_compiler import (
    InvalidNoCommitIntentPacketError,
    NoCommitIntentPacket,
    create_no_commit_intent_packet,
    validate_no_commit_intent_packet,
)


# ── Helpers ──


def _minimal_kwargs(**overrides) -> dict:
    """Return minimal valid kwargs for create_no_commit_intent_packet."""
    base = {
        "intent_ref": "intent-001",
        "actor_ref": "actor-001",
        "proposed_action_kind": "move",
        "intent_timestamp": "2025-01-01T00:00:00Z",
    }
    base.update(overrides)
    return base


def _valid_packet(**overrides) -> NoCommitIntentPacket:
    """Build a valid NoCommitIntentPacket via factory."""
    kwargs = _minimal_kwargs(**overrides)
    return create_no_commit_intent_packet(**kwargs)


# ── Package exports ──


def test_package_exports_from_domain() -> None:
    from astra_runtime.domain import (
        InvalidNoCommitIntentPacketError,
        NoCommitIntentPacket,
        create_no_commit_intent_packet,
        validate_no_commit_intent_packet,
    )

    assert InvalidNoCommitIntentPacketError is not None
    assert NoCommitIntentPacket is not None
    assert create_no_commit_intent_packet is not None
    assert validate_no_commit_intent_packet is not None


# ── Factory creates valid packet ──


def test_factory_creates_valid_packet() -> None:
    pkt = _valid_packet()
    assert isinstance(pkt, NoCommitIntentPacket)
    assert pkt.packet_kind == "no_commit_intent"
    assert pkt.intent_ref == "intent-001"
    assert pkt.actor_ref == "actor-001"
    assert pkt.proposed_action_kind == "move"
    assert pkt.intent_timestamp == "2025-01-01T00:00:00Z"


def test_factory_defaults() -> None:
    pkt = _valid_packet()
    assert pkt.target_refs == ()
    assert pkt.declared_resource_refs == ()
    assert pkt.declared_cost_refs == ()
    assert pkt.visible_context_refs == ()
    assert pkt.confirmation_required is True
    assert pkt.hidden_information_excluded is True
    assert pkt.no_commit_marker is True
    assert isinstance(pkt.non_authority_seal, tuple)
    assert len(pkt.non_authority_seal) > 0
    assert isinstance(pkt.metadata, MappingProxyType)


# ── Direct dataclass construction normalizes list fields to tuples ──


def test_direct_construction_normalizes_lists_to_tuples() -> None:
    pkt = NoCommitIntentPacket(
        packet_kind="no_commit_intent",
        intent_ref="i1",
        actor_ref="a1",
        proposed_action_kind="attack",
        intent_timestamp="2025-01-01T00:00:00Z",
        target_refs=["t1", "t2"],
        declared_resource_refs=["r1"],
        declared_cost_refs=["c1"],
        visible_context_refs=["v1"],
    )
    assert isinstance(pkt.target_refs, tuple)
    assert pkt.target_refs == ("t1", "t2")
    assert isinstance(pkt.declared_resource_refs, tuple)
    assert pkt.declared_resource_refs == ("r1",)
    assert isinstance(pkt.declared_cost_refs, tuple)
    assert pkt.declared_cost_refs == ("c1",)
    assert isinstance(pkt.visible_context_refs, tuple)
    assert pkt.visible_context_refs == ("v1",)


# ── Direct construction rejects bare strings for all tuple fields ──


@pytest.mark.parametrize(
    "field_name",
    [
        "target_refs",
        "declared_resource_refs",
        "declared_cost_refs",
        "visible_context_refs",
    ],
)
def test_direct_construction_rejects_bare_string(field_name: str) -> None:
    kwargs = {
        "packet_kind": "no_commit_intent",
        "intent_ref": "i1",
        "actor_ref": "a1",
        "proposed_action_kind": "attack",
        "intent_timestamp": "2025-01-01T00:00:00Z",
        field_name: "bare_string_value",
    }
    with pytest.raises(InvalidNoCommitIntentPacketError, match="bare string"):
        NoCommitIntentPacket(**kwargs)


def test_direct_construction_rejects_bare_string_non_authority_seal() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="bare string"):
        NoCommitIntentPacket(
            packet_kind="no_commit_intent",
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
            non_authority_seal="bare_string_value",
        )


# ── Direct construction freezes metadata with MappingProxyType ──


def test_direct_construction_freezes_metadata() -> None:
    pkt = NoCommitIntentPacket(
        packet_kind="no_commit_intent",
        intent_ref="i1",
        actor_ref="a1",
        proposed_action_kind="attack",
        intent_timestamp="2025-01-01T00:00:00Z",
        metadata={"key": "value", "nested": [1, 2, 3]},
    )
    assert isinstance(pkt.metadata, MappingProxyType)


def test_mutating_original_metadata_does_not_affect_packet() -> None:
    original = {"key": "value", "nested": [1, 2]}
    pkt = NoCommitIntentPacket(
        packet_kind="no_commit_intent",
        intent_ref="i1",
        actor_ref="a1",
        proposed_action_kind="attack",
        intent_timestamp="2025-01-01T00:00:00Z",
        metadata=original,
    )
    # Mutate original
    original["key"] = "changed"
    original["nested"].append(3)
    original["new_key"] = "new"
    # Packet metadata must be unaffected
    assert pkt.metadata["key"] == "value"
    assert list(pkt.metadata["nested"]) == [1, 2]
    assert "new_key" not in pkt.metadata


# ── non_authority_seal defaults ──


def test_empty_non_authority_seal_defaults_to_sorted_seal() -> None:
    pkt = NoCommitIntentPacket(
        packet_kind="no_commit_intent",
        intent_ref="i1",
        actor_ref="a1",
        proposed_action_kind="attack",
        intent_timestamp="2025-01-01T00:00:00Z",
    )
    assert len(pkt.non_authority_seal) > 0
    assert pkt.non_authority_seal == tuple(sorted({
        "backend_projection_not_authoritative_state",
        "no_model_authority",
        "no_hidden_information_release",
        "no_state_mutation",
        "no_event_commitment",
    }))


def test_omitted_non_authority_seal_defaults_to_sorted_seal() -> None:
    pkt = _valid_packet()
    from astra_runtime.domain.context_packet_compiler import NON_AUTHORITY_SEAL
    assert pkt.non_authority_seal == tuple(sorted(NON_AUTHORITY_SEAL))


# ── Invalid packet_kind rejected ──


def test_invalid_packet_kind_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="packet_kind"):
        create_no_commit_intent_packet(
            packet_kind="wrong_kind",
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
        )


def test_empty_packet_kind_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="packet_kind"):
        create_no_commit_intent_packet(
            packet_kind="",
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
        )


# ── Empty required string fields rejected ──


def test_empty_intent_ref_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="intent_ref"):
        create_no_commit_intent_packet(
            intent_ref="",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
        )


def test_empty_actor_ref_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="actor_ref"):
        create_no_commit_intent_packet(
            intent_ref="i1",
            actor_ref="",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
        )


def test_empty_proposed_action_kind_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="proposed_action_kind"):
        create_no_commit_intent_packet(
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="",
            intent_timestamp="2025-01-01T00:00:00Z",
        )


def test_empty_intent_timestamp_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="intent_timestamp"):
        create_no_commit_intent_packet(
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="",
        )


# ── confirmation_required must be bool ──


def test_confirmation_required_must_be_bool() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="confirmation_required"):
        create_no_commit_intent_packet(
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
            confirmation_required="yes",
        )


# ── hidden_information_excluded=False rejected ──


def test_hidden_information_excluded_false_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="hidden_information_excluded"):
        create_no_commit_intent_packet(
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
            hidden_information_excluded=False,
        )


# ── no_commit_marker=False rejected ──


def test_no_commit_marker_false_rejected() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="no_commit_marker"):
        create_no_commit_intent_packet(
            intent_ref="i1",
            actor_ref="a1",
            proposed_action_kind="attack",
            intent_timestamp="2025-01-01T00:00:00Z",
            no_commit_marker=False,
        )


# ── Validator tests ──


def test_validator_returns_true_for_valid_packet() -> None:
    pkt = _valid_packet()
    assert validate_no_commit_intent_packet(pkt) is True


def test_validator_rejects_non_packet() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="instance"):
        validate_no_commit_intent_packet("not a packet")


def test_validator_rejects_non_instance() -> None:
    with pytest.raises(InvalidNoCommitIntentPacketError, match="instance"):
        validate_no_commit_intent_packet({"packet_kind": "no_commit_intent"})


def test_validator_rejects_corrupted_packet_kind() -> None:
    pkt = _valid_packet()
    object.__setattr__(pkt, "packet_kind", "wrong_kind")
    with pytest.raises(InvalidNoCommitIntentPacketError, match="packet_kind"):
        validate_no_commit_intent_packet(pkt)


def test_validator_rejects_corrupted_intent_ref() -> None:
    pkt = _valid_packet()
    object.__setattr__(pkt, "intent_ref", "")
    with pytest.raises(InvalidNoCommitIntentPacketError, match="intent_ref"):
        validate_no_commit_intent_packet(pkt)


def test_validator_rejects_corrupted_actor_ref() -> None:
    pkt = _valid_packet()
    object.__setattr__(pkt, "actor_ref", "")
    with pytest.raises(InvalidNoCommitIntentPacketError, match="actor_ref"):
        validate_no_commit_intent_packet(pkt)


def test_validator_rejects_corrupted_hidden_information_excluded() -> None:
    pkt = _valid_packet()
    object.__setattr__(pkt, "hidden_information_excluded", False)
    with pytest.raises(InvalidNoCommitIntentPacketError, match="hidden_information_excluded"):
        validate_no_commit_intent_packet(pkt)


def test_validator_rejects_corrupted_no_commit_marker() -> None:
    pkt = _valid_packet()
    object.__setattr__(pkt, "no_commit_marker", False)
    with pytest.raises(InvalidNoCommitIntentPacketError, match="no_commit_marker"):
        validate_no_commit_intent_packet(pkt)


def test_validator_rejects_corrupted_non_authority_seal() -> None:
    pkt = _valid_packet()
    object.__setattr__(pkt, "non_authority_seal", ())
    with pytest.raises(InvalidNoCommitIntentPacketError, match="non_authority_seal"):
        validate_no_commit_intent_packet(pkt)


def test_validator_rejects_corrupted_metadata_type() -> None:
    pkt = _valid_packet()
    object.__setattr__(pkt, "metadata", {"not": "frozen"})
    with pytest.raises(InvalidNoCommitIntentPacketError, match="MappingProxyType"):
        validate_no_commit_intent_packet(pkt)


# ── to_dict() tests ──


FORBIDDEN_TO_DICT_KEYS = {
    "event_ref",
    "event_commitment",
    "committed_event",
    "state_delta",
    "mutation",
    "roll_result",
    "rng_result",
    "narration_output",
    "hidden_fact",
}


def test_to_dict_is_deterministic() -> None:
    pkt = _valid_packet()
    d1 = pkt.to_dict()
    d2 = pkt.to_dict()
    assert d1 == d2


def test_to_dict_contains_expected_fields() -> None:
    pkt = _valid_packet()
    d = pkt.to_dict()
    assert d["packet_kind"] == "no_commit_intent"
    assert d["intent_ref"] == "intent-001"
    assert d["actor_ref"] == "actor-001"
    assert d["proposed_action_kind"] == "move"
    assert d["intent_timestamp"] == "2025-01-01T00:00:00Z"
    assert d["confirmation_required"] is True
    assert d["hidden_information_excluded"] is True
    assert d["no_commit_marker"] is True
    assert isinstance(d["target_refs"], list)
    assert isinstance(d["declared_resource_refs"], list)
    assert isinstance(d["declared_cost_refs"], list)
    assert isinstance(d["visible_context_refs"], list)
    assert isinstance(d["non_authority_seal"], list)
    assert isinstance(d["metadata"], dict)


def test_to_dict_contains_no_forbidden_commit_or_state_fields() -> None:
    pkt = _valid_packet()
    d = pkt.to_dict()
    for key in FORBIDDEN_TO_DICT_KEYS:
        assert key not in d, f"forbidden key {key!r} must not appear in to_dict()"


def test_to_dict_forbidden_strings_not_in_keys() -> None:
    pkt = _valid_packet()
    d = pkt.to_dict()
    forbidden_keys = {
        "event_commitment",
        "committed_event",
        "state_delta",
        "mutation",
        "roll_result",
        "rng_result",
        "narration_output",
        "hidden_fact",
    }
    for key in forbidden_keys:
        assert key not in d, (
            f"forbidden key {key!r} must not appear in to_dict()"
        )


def test_to_dict_metadata_is_deep_copied() -> None:
    pkt = _valid_packet(metadata={"key": "value"})
    d = pkt.to_dict()
    d["metadata"]["key"] = "mutated"
    assert pkt.metadata["key"] == "value"


# ── Frozen dataclass immutability ──


def test_frozen_dataclass_rejects_attribute_set() -> None:
    pkt = _valid_packet()
    with pytest.raises(AttributeError):
        pkt.intent_ref = "new-intent"  # type: ignore[misc]
