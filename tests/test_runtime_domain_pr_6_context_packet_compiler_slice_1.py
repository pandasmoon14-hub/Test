"""Focused tests for PR-6 context packet compiler Slice 1 — SingleEventNarrationPacket."""

from __future__ import annotations

from types import MappingProxyType

import pytest

from astra_runtime.domain.context_packet_compiler import (
    PACKET_KINDS,
    PACKET_PURPOSE_LABELS,
    NON_AUTHORITY_SEAL,
    ContextPacketCompilerError,
    InvalidSingleEventNarrationPacketError,
    SingleEventNarrationPacket,
    create_single_event_narration_packet,
    validate_single_event_narration_packet,
    validate_packet_kind,
)


# ── Constants ──


def test_constants_contain_three_packet_kinds() -> None:
    assert isinstance(PACKET_KINDS, frozenset)
    assert PACKET_KINDS == frozenset({
        "single_event_narration",
        "no_commit_intent",
        "visible_summary",
    })


def test_packet_purpose_labels_contains_expected_labels() -> None:
    assert isinstance(PACKET_PURPOSE_LABELS, MappingProxyType)
    assert PACKET_PURPOSE_LABELS["single_event_narration"] == (
        "visibility-safe committed-event narration input"
    )
    assert PACKET_PURPOSE_LABELS["no_commit_intent"] == (
        "uncommitted player-intent parsing input"
    )
    assert PACKET_PURPOSE_LABELS["visible_summary"] == (
        "visibility-safe committed-state summary input"
    )


def test_non_authority_seal_contains_expected_seals() -> None:
    assert isinstance(NON_AUTHORITY_SEAL, frozenset)
    assert NON_AUTHORITY_SEAL == frozenset({
        "backend_projection_not_authoritative_state",
        "no_model_authority",
        "no_hidden_information_release",
        "no_state_mutation",
        "no_event_commitment",
    })


# ── Valid creation ──


def test_factory_creates_valid_single_event_narration_packet() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-001",
        event_kind="combat_action",
        visible_fact_refs=["fact-1", "fact-2"],
        actor_refs=["actor-1"],
        target_refs=["target-1"],
        sensory_cues=["loud_explosion"],
        forbidden_claims=["actor_knows_target_hp"],
        metadata={"source": "test"},
    )
    assert isinstance(packet, SingleEventNarrationPacket)
    assert packet.packet_kind == "single_event_narration"
    assert packet.event_ref == "evt-001"
    assert packet.event_kind == "combat_action"
    assert packet.visible_fact_refs == ("fact-1", "fact-2")
    assert packet.actor_refs == ("actor-1",)
    assert packet.target_refs == ("target-1",)
    assert packet.sensory_cues == ("loud_explosion",)
    assert packet.forbidden_claims == ("actor_knows_target_hp",)
    assert packet.hidden_information_excluded is True
    assert dict(packet.metadata) == {"source": "test"}


def test_default_non_authority_seal_is_present() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-002",
        event_kind="dialogue",
        visible_fact_refs=["fact-3"],
    )
    expected_seal = tuple(sorted(NON_AUTHORITY_SEAL))
    assert packet.non_authority_seal == expected_seal


def test_custom_non_authority_seal_is_accepted() -> None:
    custom_seal = ["no_model_authority", "no_state_mutation"]
    packet = create_single_event_narration_packet(
        event_ref="evt-003",
        event_kind="exploration",
        visible_fact_refs=["fact-4"],
        non_authority_seal=custom_seal,
    )
    assert packet.non_authority_seal == ("no_model_authority", "no_state_mutation")


# ── Immutability ──


def test_packet_is_frozen() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-frozen",
        event_kind="test",
        visible_fact_refs=["fact-x"],
    )
    with pytest.raises(AttributeError):
        packet.event_ref = "changed"  # type: ignore[misc]


# ── to_dict() ──


def test_to_dict_returns_deterministic_plain_dict() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-dict",
        event_kind="test",
        visible_fact_refs=["fact-a", "fact-b"],
        actor_refs=["actor-z"],
        metadata={"key": "value"},
    )
    d = packet.to_dict()
    assert isinstance(d, dict)
    assert d["packet_kind"] == "single_event_narration"
    assert d["event_ref"] == "evt-dict"
    assert d["event_kind"] == "test"
    assert d["visible_fact_refs"] == ["fact-a", "fact-b"]
    assert d["actor_refs"] == ["actor-z"]
    assert d["target_refs"] == []
    assert d["sensory_cues"] == []
    assert d["forbidden_claims"] == []
    assert isinstance(d["non_authority_seal"], list)
    assert d["non_authority_seal"] == list(packet.non_authority_seal)
    assert d["hidden_information_excluded"] is True
    assert d["metadata"] == {"key": "value"}
    # Ensure lists are copies, not the same tuple/list
    assert d["visible_fact_refs"] is not packet.visible_fact_refs
    assert d["metadata"] is not packet.metadata


def test_to_dict_is_deterministic_with_defaults() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-dict-2",
        event_kind="test",
        visible_fact_refs=["fact-c"],
    )
    d1 = packet.to_dict()
    d2 = packet.to_dict()
    assert d1 == d2


# ── Metadata copy and immutability ──


def test_metadata_is_defensively_copied() -> None:
    original = {"nested": {"inner": 42}}
    packet = create_single_event_narration_packet(
        event_ref="evt-meta",
        event_kind="test",
        visible_fact_refs=["fact-m"],
        metadata=original,
    )
    # Mutate original after construction
    original["nested"]["inner"] = 999
    original["extra"] = "should_not_appear"
    assert dict(packet.metadata)["nested"]["inner"] == 42
    assert "extra" not in packet.metadata


def test_metadata_is_immutable() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-meta-immutable",
        event_kind="test",
        visible_fact_refs=["fact-m2"],
        metadata={"key": "value"},
    )
    assert isinstance(packet.metadata, MappingProxyType)
    # Verify it cannot be mutated via the reference
    # (MappingProxyType raises TypeError on __setitem__)
    import types
    assert isinstance(packet.metadata, types.MappingProxyType)


# ── Invalid packet_kind rejection ──


def test_invalid_packet_kind_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            packet_kind="wrong_kind",
            event_ref="evt-bad-kind",
            event_kind="test",
            visible_fact_refs=["fact-x"],
        )


def test_empty_packet_kind_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            packet_kind="",
            event_ref="evt-empty-kind",
            event_kind="test",
            visible_fact_refs=["fact-x"],
        )


# ── hidden_information_excluded=False rejection ──


def test_hidden_information_excluded_false_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-hid",
            event_kind="test",
            visible_fact_refs=["fact-x"],
            hidden_information_excluded=False,
        )


# ── Empty event_ref rejection ──


def test_empty_event_ref_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="",
            event_kind="test",
            visible_fact_refs=["fact-x"],
        )


def test_blank_event_ref_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="   ",
            event_kind="test",
            visible_fact_refs=["fact-x"],
        )


# ── Empty event_kind rejection ──


def test_empty_event_kind_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-1",
            event_kind="",
            visible_fact_refs=["fact-x"],
        )


def test_blank_event_kind_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-1",
            event_kind="   ",
            visible_fact_refs=["fact-x"],
        )


# ── Empty visible_fact_refs rejection ──


def test_empty_visible_fact_refs_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-empty-facts",
            event_kind="test",
            visible_fact_refs=[],
        )


# ── Empty string inside tuple fields rejection ──


def test_empty_string_in_visible_fact_refs_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bad-fact",
            event_kind="test",
            visible_fact_refs=["fact-1", ""],
        )


def test_empty_string_in_actor_refs_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bad-actor",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            actor_refs=["actor-1", ""],
        )


def test_empty_string_in_target_refs_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bad-target",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            target_refs=["target-1", ""],
        )


def test_empty_string_in_sensory_cues_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bad-cue",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            sensory_cues=["cue-1", ""],
        )


def test_empty_string_in_forbidden_claims_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bad-claim",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            forbidden_claims=["claim-1", ""],
        )


def test_empty_string_in_non_authority_seal_is_rejected() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bad-seal",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            non_authority_seal=["no_model_authority", ""],
        )


# ── validate_packet_kind ──


def test_validate_packet_kind_accepts_known_kinds() -> None:
    assert validate_packet_kind("single_event_narration") is True
    assert validate_packet_kind("no_commit_intent") is True
    assert validate_packet_kind("visible_summary") is True


def test_validate_packet_kind_rejects_unknown_kind() -> None:
    with pytest.raises(ContextPacketCompilerError):
        validate_packet_kind("unknown_kind")


def test_validate_packet_kind_rejects_empty_string() -> None:
    with pytest.raises(ContextPacketCompilerError):
        validate_packet_kind("")


# ── validate_single_event_narration_packet ──


def test_validator_returns_true_for_valid_packet() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-val",
        event_kind="test",
        visible_fact_refs=["fact-v"],
    )
    assert validate_single_event_narration_packet(packet) is True


def test_validator_rejects_non_packet_value() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        validate_single_event_narration_packet("not-a-packet")


def test_validator_rejects_directly_constructed_invalid_packet_kind() -> None:
    """Direct construction with invalid packet_kind is rejected by __post_init__."""
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        SingleEventNarrationPacket(
            packet_kind="wrong",
            event_ref="evt-1",
            event_kind="test",
            visible_fact_refs=("fact-1",),
        )


# ── Package exports ──


def test_package_exports_work_from_astra_runtime_domain() -> None:
    from astra_runtime.domain import (
        PACKET_KINDS as PK,
        PACKET_PURPOSE_LABELS as PPL,
        NON_AUTHORITY_SEAL as NAS,
        ContextPacketCompilerError as CPCE,
        InvalidSingleEventNarrationPacketError as ISENPE,
        SingleEventNarrationPacket as SENP,
        create_single_event_narration_packet as CSENP,
        validate_single_event_narration_packet as VSENP,
        validate_packet_kind as VPK,
    )
    assert PK is PACKET_KINDS
    assert PPL is PACKET_PURPOSE_LABELS
    assert NAS is NON_AUTHORITY_SEAL
    assert CPCE is ContextPacketCompilerError
    assert ISENPE is InvalidSingleEventNarrationPacketError
    assert SENP is SingleEventNarrationPacket
    assert CSENP is create_single_event_narration_packet
    assert VSENP is validate_single_event_narration_packet
    assert VPK is validate_packet_kind


# ── Forbidden scope strings check ──


def test_forbidden_scope_strings_absent_from_module_source() -> None:
    """Verify forbidden-scope strings are absent from the module source.

    The module must not contain: roll, random, commit_event, mutate,
    apply_delta, persist, replay, generate_narration, to_public_dict.
    """
    import astra_runtime.domain.context_packet_compiler as mod
    import inspect

    source = inspect.getsource(mod)

    forbidden = [
        "roll",
        "random",
        "commit_event",
        "mutate",
        "apply_delta",
        "persist",
        "replay",
        "generate_narration",
        "to_public_dict",
    ]
    for token in forbidden:
        assert token not in source, (
            f"Forbidden token {token!r} found in context_packet_compiler.py source"
        )


# ── Edge cases ──


def test_factory_rejects_bare_string_as_visible_fact_refs() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bare",
            event_kind="test",
            visible_fact_refs="not-a-sequence",  # type: ignore[arg-type]
        )


def test_factory_rejects_bare_string_as_actor_refs() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bare-actor",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            actor_refs="not-a-sequence",  # type: ignore[arg-type]
        )


def test_factory_rejects_callable_metadata() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-callable-meta",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            metadata={"bad": lambda: None},
        )


def test_factory_rejects_non_mapping_metadata() -> None:
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        create_single_event_narration_packet(
            event_ref="evt-bad-meta",
            event_kind="test",
            visible_fact_refs=["fact-1"],
            metadata="not-a-mapping",  # type: ignore[arg-type]
        )


def test_tuple_defaults_are_empty() -> None:
    packet = create_single_event_narration_packet(
        event_ref="evt-defaults",
        event_kind="test",
        visible_fact_refs=["fact-d"],
    )
    assert packet.actor_refs == ()
    assert packet.target_refs == ()
    assert packet.sensory_cues == ()
    assert packet.forbidden_claims == ()


# ── Direct construction safety tests ──


def test_direct_construction_list_fields_normalize_to_tuples() -> None:
    """Direct construction with list fields normalizes them to tuples via __post_init__."""
    packet = SingleEventNarrationPacket(
        packet_kind="single_event_narration",
        event_ref="evt-direct-1",
        event_kind="test",
        visible_fact_refs=["fact-1", "fact-2"],
        actor_refs=["actor-1", "actor-2"],
        target_refs=["target-1"],
        sensory_cues=["cue-1", "cue-2"],
        forbidden_claims=["claim-1"],
    )
    assert isinstance(packet.visible_fact_refs, tuple)
    assert isinstance(packet.actor_refs, tuple)
    assert isinstance(packet.target_refs, tuple)
    assert isinstance(packet.sensory_cues, tuple)
    assert isinstance(packet.forbidden_claims, tuple)
    assert packet.visible_fact_refs == ("fact-1", "fact-2")
    assert packet.actor_refs == ("actor-1", "actor-2")


def test_direct_construction_dict_metadata_converts_to_mapping_proxy_type() -> None:
    """Direct construction with plain dict metadata converts to MappingProxyType."""
    packet = SingleEventNarrationPacket(
        packet_kind="single_event_narration",
        event_ref="evt-direct-meta",
        event_kind="test",
        visible_fact_refs=["fact-1"],
        metadata={"key": "value", "nested": {"inner": 42}},
    )
    assert isinstance(packet.metadata, MappingProxyType)


def test_direct_construction_metadata_mutation_does_not_affect_packet() -> None:
    """Mutation of the original metadata dict after direct construction does not affect packet."""
    original = {"key": "original", "nested": {"inner": 1}}
    packet = SingleEventNarrationPacket(
        packet_kind="single_event_narration",
        event_ref="evt-direct-mut",
        event_kind="test",
        visible_fact_refs=["fact-1"],
        metadata=original,
    )
    # Mutate the original dict
    original["key"] = "mutated"
    original["nested"]["inner"] = 999
    original["new_key"] = "injected"
    # Packet should be unaffected
    assert packet.metadata["key"] == "original"
    assert packet.metadata["nested"]["inner"] == 1
    assert "new_key" not in packet.metadata


def test_direct_construction_omitted_non_authority_seal_defaults() -> None:
    """Direct construction with omitted/empty non_authority_seal defaults to sorted NON_AUTHORITY_SEAL."""
    packet = SingleEventNarrationPacket(
        packet_kind="single_event_narration",
        event_ref="evt-direct-seal",
        event_kind="test",
        visible_fact_refs=["fact-1"],
    )
    expected_seal = tuple(sorted(NON_AUTHORITY_SEAL))
    assert packet.non_authority_seal == expected_seal
    assert len(packet.non_authority_seal) == 5


def test_direct_construction_invalid_packet_kind_raises() -> None:
    """Direct construction with invalid packet_kind raises InvalidSingleEventNarrationPacketError."""
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        SingleEventNarrationPacket(
            packet_kind="wrong_kind",
            event_ref="evt-direct-bad-kind",
            event_kind="test",
            visible_fact_refs=("fact-1",),
        )


def test_direct_construction_hidden_information_excluded_false_raises() -> None:
    """Direct construction with hidden_information_excluded=False raises."""
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        SingleEventNarrationPacket(
            packet_kind="single_event_narration",
            event_ref="evt-direct-hid",
            event_kind="test",
            visible_fact_refs=("fact-1",),
            hidden_information_excluded=False,
        )


def test_direct_construction_empty_event_ref_raises() -> None:
    """Direct construction with empty event_ref raises."""
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        SingleEventNarrationPacket(
            packet_kind="single_event_narration",
            event_ref="",
            event_kind="test",
            visible_fact_refs=("fact-1",),
        )


def test_direct_construction_empty_visible_fact_refs_raises() -> None:
    """Direct construction with empty visible_fact_refs raises."""
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        SingleEventNarrationPacket(
            packet_kind="single_event_narration",
            event_ref="evt-direct-empty-vis",
            event_kind="test",
            visible_fact_refs=(),
        )


def test_validator_rejects_object_setattr_corrupted_packet() -> None:
    """Validator rejects a packet corrupted via object.__setattr__ after construction."""
    packet = create_single_event_narration_packet(
        event_ref="evt-validate-corrupt",
        event_kind="test",
        visible_fact_refs=["fact-1"],
    )
    # Corrupt the packet_kind via object.__setattr__
    object.__setattr__(packet, "packet_kind", "corrupted")
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        validate_single_event_narration_packet(packet)


def test_validator_rejects_empty_non_authority_seal() -> None:
    """Validator rejects a packet with empty non_authority_seal."""
    packet = create_single_event_narration_packet(
        event_ref="evt-validate-empty-seal",
        event_kind="test",
        visible_fact_refs=["fact-1"],
    )
    # Corrupt non_authority_seal via object.__setattr__
    object.__setattr__(packet, "non_authority_seal", ())
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        validate_single_event_narration_packet(packet)


def test_validator_rejects_non_mapping_proxy_metadata() -> None:
    """Validator rejects a packet whose metadata is not MappingProxyType."""
    packet = create_single_event_narration_packet(
        event_ref="evt-validate-bad-meta",
        event_kind="test",
        visible_fact_refs=["fact-1"],
    )
    # Corrupt metadata via object.__setattr__
    object.__setattr__(packet, "metadata", {"bad": "plain_dict"})
    with pytest.raises(InvalidSingleEventNarrationPacketError):
        validate_single_event_narration_packet(packet)
