"""Player-help discoverability regression: clear topics without gameplay authority."""
from __future__ import annotations

from io import StringIO
import subprocess
import sys

import pytest

from astra_runtime.myravant_terminal import (
    _HELP_TOPICS, _write_help, parse_terminal_command, run_terminal,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application
from astra_runtime.myravant_terminal_capabilities import execute_bounded_terminal_request


def test_plain_help_is_short_and_player_facing_not_an_internal_doctrine_dump():
    out = StringIO()
    result = _write_help(out)
    assert result == out.getvalue()
    assert result.startswith("Commands:")
    assert len(result) < 600
    for topic in ("travel", "senses", "objects", "people", "work", "inquiry", "session"):
        assert "help " + topic in result
    for package_label in ("B-2a", "B-2b", "C-1", "C-2", "C-3", "D-1", "E-1", "E-2", "BREADTH-1", "VSM-"):
        assert package_label not in result


@pytest.mark.parametrize(
    "utterance,topic",
    [
        ("help", None),
        ("?", None),
        ("help travel", "travel"),
        ("HELP SENSES", "senses"),
        ("help objects", "objects"),
        ("help people", "people"),
        ("help work", "work"),
        ("help inquiry", "inquiry"),
        ("help session", "session"),
        ("help movement", "movement"),
        ("help items", "items"),
        ("help investigation", "investigation"),
        ("help all", "all"),
        ("help unknown", "unknown"),
    ],
)
def test_help_topic_parser_does_not_misroute_actual_gameplay(utterance, topic):
    parsed = parse_terminal_command(utterance)
    assert parsed.action == "help"
    assert parsed.argument == topic


def test_each_topic_keeps_mechanical_discoverability_without_internal_codes():
    assert set(_HELP_TOPICS) == {
        "travel", "senses", "objects", "people", "work", "inquiry", "session",
    }
    for topic in _HELP_TOPICS:
        out = StringIO()
        visible = _write_help(out, topic)
        assert visible == out.getvalue()
        assert 50 < len(visible) < 1800
        assert not any(
            token in visible
            for token in ("B-2a", "B-2b", "C-1", "C-2", "C-3", "D-1", "E-1", "E-2", "BREADTH-1", "VSM-")
        )
    assert "obstruction" in _write_help(StringIO(), "travel")
    assert "poor light" in _write_help(StringIO(), "senses")
    assert "drag waystone west" in _write_help(StringIO(), "objects")
    assert "follow me" in _write_help(StringIO(), "people")
    assert "waystone" in _write_help(StringIO(), "work")
    assert "last witnessed" in _write_help(StringIO(), "inquiry")
    assert "--load" in _write_help(StringIO(), "session")


def test_help_alias_and_unrecognized_topic_are_read_only_and_actionable():
    assert _write_help(StringIO(), "movement") == _write_help(StringIO(), "travel")
    assert _write_help(StringIO(), "investigation") == _write_help(StringIO(), "inquiry")
    for unknown in ("missing", "north", "lantern"):
        result = _write_help(StringIO(), unknown)
        assert "No help topic" in result
        assert "Choose travel" in result


def test_all_topics_is_opt_in_and_does_not_change_default_length():
    summary = _write_help(StringIO())
    all_text = _write_help(StringIO(), "all")
    assert all_text.startswith(summary)
    assert all("help " + topic in summary for topic in _HELP_TOPICS)
    assert all(topic_text in all_text for topic_text in _HELP_TOPICS.values())
    assert len(all_text) > len(summary)


def test_installed_terminal_help_topics_do_not_advance_time_or_make_checkpoint(tmp_path):
    checkpoint = tmp_path / "help-only.json"
    result = subprocess.run(
        [
            sys.executable, "-m", "astra_runtime.myravant_terminal",
            "--checkpoint", str(checkpoint),
        ],
        input="help\nhelp work\nhelp inquiry\nhelp anything\nexit\n",
        text=True, capture_output=True, timeout=90,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert "Explore: help travel" in result.stdout
    assert "Ongoing work and consequences" in result.stdout
    assert "Learning from another person" in result.stdout
    assert "No help topic named 'anything'" in result.stdout
    assert "B-2a" not in result.stdout
    assert not checkpoint.exists()


def test_help_does_not_change_live_world_or_prevent_actual_play():
    app = MyravantVSM14Application.new()
    pre_digest = app.authoritative_digest()
    out = StringIO()
    result = run_terminal(
        app,
        input_stream=StringIO("help\nhelp objects\ngo south\nhelp travel\nwait\nexit\n"),
        output_stream=out,
        specialized_router=execute_bounded_terminal_request,
    )
    assert result == 0
    visible = out.getvalue()
    assert "Handling objects" in visible
    assert "Travel and time" in visible
    assert "Time passes." in visible
    assert app.current_place_id() != app.fixture.initial_state.representation.relations[0].object_entity_id
    assert app.runtime_state.logical_time_state.logical_position == 1
    assert app.authoritative_digest() != pre_digest
