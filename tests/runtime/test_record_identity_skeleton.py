"""Tests for record identity skeleton — RUNTIME-IMPL-PR-1."""

import pytest

from astra_runtime.kernel.record_identity import (
    InvalidRecordIdError,
    RecordId,
    build_record_id,
    is_valid_record_id,
    parse_record_id,
)


class TestBuildRecordId:
    def test_build_valid_id(self):
        result = build_record_id("creature", "goblin-01")
        assert result == "astra:creature:goblin-01"

    def test_build_with_underscores(self):
        result = build_record_id("magic_item", "staff_of_power")
        assert result == "astra:magic_item:staff_of_power"

    def test_build_with_digits(self):
        result = build_record_id("npc", "guard-42")
        assert result == "astra:npc:guard-42"

    def test_deterministic_output(self):
        a = build_record_id("creature", "goblin-01")
        b = build_record_id("creature", "goblin-01")
        assert a == b

    def test_reject_empty_type(self):
        with pytest.raises(InvalidRecordIdError):
            build_record_id("", "local-id")

    def test_reject_empty_local_id(self):
        with pytest.raises(InvalidRecordIdError):
            build_record_id("creature", "")

    def test_reject_whitespace_only_type(self):
        with pytest.raises(InvalidRecordIdError):
            build_record_id("   ", "local-id")

    def test_reject_whitespace_only_local_id(self):
        with pytest.raises(InvalidRecordIdError):
            build_record_id("creature", "   ")

    def test_reject_uppercase_type(self):
        with pytest.raises(InvalidRecordIdError):
            build_record_id("Creature", "goblin")

    def test_reject_spaces_in_type(self):
        with pytest.raises(InvalidRecordIdError):
            build_record_id("magic item", "staff")

    def test_reject_special_chars_in_local_id(self):
        with pytest.raises(InvalidRecordIdError):
            build_record_id("creature", "goblin@cave")


class TestParseRecordId:
    def test_parse_valid_id(self):
        result = parse_record_id("astra:creature:goblin-01")
        assert isinstance(result, RecordId)
        assert result.record_type == "creature"
        assert result.local_id == "goblin-01"

    def test_parse_full_id_property(self):
        result = parse_record_id("astra:item:sword-01")
        assert result.full_id == "astra:item:sword-01"

    def test_reject_empty_string(self):
        with pytest.raises(InvalidRecordIdError):
            parse_record_id("")

    def test_reject_whitespace_only(self):
        with pytest.raises(InvalidRecordIdError):
            parse_record_id("   ")

    def test_reject_missing_prefix(self):
        with pytest.raises(InvalidRecordIdError):
            parse_record_id("creature:goblin-01")

    def test_reject_wrong_prefix(self):
        with pytest.raises(InvalidRecordIdError):
            parse_record_id("other:creature:goblin-01")

    def test_reject_too_few_segments(self):
        with pytest.raises(InvalidRecordIdError):
            parse_record_id("astra:creature")

    def test_reject_uppercase_in_id(self):
        with pytest.raises(InvalidRecordIdError):
            parse_record_id("astra:Creature:goblin")


class TestIsValidRecordId:
    def test_valid_id_returns_true(self):
        assert is_valid_record_id("astra:creature:goblin-01") is True

    def test_invalid_id_returns_false(self):
        assert is_valid_record_id("bad-format") is False

    def test_empty_string_returns_false(self):
        assert is_valid_record_id("") is False

    def test_none_returns_false(self):
        assert is_valid_record_id(None) is False


class TestNoRandomOrPersistentAllocation:
    def test_build_is_purely_deterministic(self):
        results = {build_record_id("creature", "test") for _ in range(100)}
        assert len(results) == 1
