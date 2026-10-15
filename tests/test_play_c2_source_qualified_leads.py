"""C-2: the same actor's sighting and testimony suggest different lawful routes.

Historical evidence selects a candidate destination; it never owns physical
movement or silently asserts that an object remains at its old location.
"""
from __future__ import annotations

import subprocess
import sys

from astra_runtime.myravant_actor_situated_knowledge import (
    digest_actor_knowledge,
)
from astra_runtime.myravant_c1_investigation_goal import parse_actor_memory_request
from astra_runtime.myravant_play_fixture import (
    GATEHOUSE_ID, GROUNDSKEEPER_ID, TOOL_CHEST_ID, YARD_ID,
)
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _meet_in_yard(app: MyravantVSM14Application) -> None:
    assert app.move("south").authoritative_changed
    assert app.wait().authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def _record_disagreeing_leads(app: MyravantVSM14Application) -> None:
    _meet_in_yard(app)
    assert app.actor_memory_interaction(
        "witness", "chest",
    ).authoritative_changed
    assert app.actor_memory_interaction(
        "report", "chest", reported_place="gatehouse",
    ).authoritative_changed


def _chest_still_in_yard(app: MyravantVSM14Application) -> bool:
    return any(
        rel.relation_type == "located_at"
        and rel.subject_entity_id == TOOL_CHEST_ID
        and rel.object_entity_id == YARD_ID
        for rel in app.state.representation.relations
    )


def test_source_qualified_leads_have_distinct_real_consequences(tmp_path):
    checkpoint = tmp_path / "c2-leads.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _record_disagreeing_leads(app)
    remembered = digest_actor_knowledge(app.knowledge_state)
    original_world = app.representation_digest()
    assert _chest_still_in_yard(app)

    # Firsthand observation points to the current Yard, so no movement can
    # be claimed. The same agent's attributed report proposes Gatehouse.
    already_here = app.actor_memory_interaction("follow_sighting", "chest")
    assert not already_here.authoritative_changed
    assert "already at" in already_here.message
    assert app.representation_digest() == original_world
    reported = app.actor_memory_interaction("follow_report", "chest")
    assert reported.authoritative_changed
    assert reported.receipt_id and reported.command_id
    assert "reported lead" in reported.message
    assert "does not establish" in reported.message
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert _chest_still_in_yard(app)

    # The original observation is still independently addressable after the
    # newer report and remains so across a full v7 checkpoint restoration.
    assert digest_actor_knowledge(app.knowledge_state) == remembered
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    # Dialogue remains co-present only: after the false lead, the player
    # must actually travel to Gatehouse before consulting the Groundskeeper.
    absent = restored.actor_memory_interaction("last_saw", "chest")
    assert absent.failure_class == "actor_knowledge_actor_not_local"
    assert restored.move("south").authoritative_changed
    assert "Yard" in restored.actor_memory_interaction(
        "last_saw", "chest",
    ).message
    assert "Gatehouse" in restored.actor_memory_interaction(
        "heard", "chest",
    ).message

    witnessed = restored.actor_memory_interaction("follow_sighting", "chest")
    assert witnessed.authoritative_changed
    assert witnessed.receipt_id and witnessed.command_id
    assert "witnessed lead" in witnessed.message
    assert restored.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert _chest_still_in_yard(restored)
    assert digest_actor_knowledge(restored.knowledge_state) == remembered
    restored.save()
    again = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert again.authoritative_digest() == restored.authoritative_digest()
    assert again.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID


def test_stale_observation_and_false_report_both_remain_fallible(tmp_path):
    checkpoint = tmp_path / "c2-stale.json"
    app = MyravantVSM14Application.new(checkpoint_path=checkpoint)
    _meet_in_yard(app)
    assert app.actor_memory_interaction("witness", "chest").authoritative_changed
    # Actual chest is now in a *third* place, distinct from both prior
    # firsthand observation (Yard) and later unverified report (Gatehouse).
    assert app.displace_object(
        "chest", "north", method="push",
    ).authoritative_changed
    assert app.actor_memory_interaction(
        "report", "chest", reported_place="gatehouse",
    ).authoritative_changed
    assert app.actor_memory_interaction("follow_report", "chest").authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert app.move("south").authoritative_changed
    before = app.representation_digest()

    # The actor acts on a lawful but outdated observation. The response must
    # not claim to discover the object's actual Workshop placement.
    stale = app.actor_memory_interaction("follow_sighting", "chest")
    assert stale.authoritative_changed
    assert app.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert "witnessed lead" in stale.message
    assert "Workshop" not in stale.message
    assert "does not establish" in stale.message
    assert app.representation_digest() != before
    assert not _chest_still_in_yard(app)
    assert len(app.knowledge_state.events) == 2
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert not _chest_still_in_yard(restored)


def test_missing_source_is_unknown_not_replaced_with_other_or_world_truth():
    sight_only = MyravantVSM14Application.new()
    _meet_in_yard(sight_only)
    assert sight_only.actor_memory_interaction(
        "witness", "chest",
    ).authoritative_changed
    pre = sight_only.authoritative_digest()
    unknown_report = sight_only.actor_memory_interaction("follow_report", "chest")
    assert unknown_report.failure_class == "actor_knowledge_unknown"
    assert "report" in unknown_report.message
    assert "Gatehouse" not in unknown_report.message
    assert sight_only.authoritative_digest() == pre

    report_only = MyravantVSM14Application.new()
    _meet_in_yard(report_only)
    assert report_only.actor_memory_interaction(
        "report", "chest", reported_place="gatehouse",
    ).authoritative_changed
    pre = report_only.authoritative_digest()
    unknown_sighting = report_only.actor_memory_interaction(
        "follow_sighting", "chest",
    )
    assert unknown_sighting.failure_class == "actor_knowledge_unknown"
    assert "sighting" in unknown_sighting.message
    assert "Yard" not in unknown_sighting.message
    assert report_only.authoritative_digest() == pre

    # The original C-1 latest-lead request still uses the available report.
    default = report_only.actor_memory_interaction("follow_lead", "chest")
    assert default.authoritative_changed
    assert "reported lead" in default.message


def test_remote_actor_refusal_does_not_disclose_leads():
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    for operation in ("follow_sighting", "follow_report"):
        denied = app.actor_memory_interaction(operation, "chest")
        assert denied.failure_class == "actor_knowledge_actor_not_local"
        assert not denied.authoritative_changed
        assert "Yard" not in denied.message
        assert "Gatehouse" not in denied.message
    assert app.authoritative_digest() == before


def test_c2_interpreter_preserves_adjacent_parsers_and_legacy_intent():
    assert parse_actor_memory_request(
        "ask groundskeeper to investigate last witnessed location of chest"
    ) == ("follow_sighting", "chest", None)
    assert parse_actor_memory_request(
        "ask the groundskeeper to check the last firsthand lead for lantern"
    ) == ("follow_sighting", "lantern", None)
    assert parse_actor_memory_request(
        "ask groundskeeper to follow the observed trail of chest"
    ) == ("follow_sighting", "chest", None)
    assert parse_actor_memory_request(
        "ask groundskeeper to investigate last reported location of chest"
    ) == ("follow_report", "chest", None)
    assert parse_actor_memory_request(
        "ask groundskeeper to follow the unverified lead for chest"
    ) == ("follow_report", "chest", None)
    assert parse_actor_memory_request(
        "ask groundskeeper to investigate the last location of chest"
    ) == ("follow_lead", "chest", None)
    for other in (
        "ask groundskeeper for chest",
        "ask groundskeeper to follow me",
        "ask groundskeeper to go to yard",
        "ask council for a charter",
    ):
        assert parse_actor_memory_request(other) is None


def test_installed_sessions_durably_ack_selected_source_and_resume(tmp_path):
    checkpoint = tmp_path / "terminal-c2.json"

    def run(commands, *flags):
        return subprocess.run(
            [sys.executable, "-m", "astra_runtime.myravant_terminal", *flags],
            input="\n".join((*commands, "exit", "")),
            text=True, capture_output=True, timeout=80,
        )

    first = run((
        "go south",
        "wait",
        "ask groundskeeper to inspect chest",
        "tell groundskeeper chest is at gatehouse",
        "ask groundskeeper to investigate last witnessed location of chest",
        "ask groundskeeper to investigate last reported location of chest",
    ), "--checkpoint", str(checkpoint))
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert "already at" in first.stdout
    assert "Following the reported lead" in first.stdout
    stored = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert stored.entity_place_id(GROUNDSKEEPER_ID) == GATEHOUSE_ID
    assert len(stored.knowledge_state.events) == 2

    second = run((
        "go south",
        "ask groundskeeper to investigate last witnessed location of chest",
    ), "--load", str(checkpoint))
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "Following the witnessed lead" in second.stdout
    final = MyravantVSM14Application.restore(checkpoint_path=checkpoint)
    assert final.entity_place_id(GROUNDSKEEPER_ID) == YARD_ID
    assert len(final.knowledge_state.events) == 2
    assert _chest_still_in_yard(final)
