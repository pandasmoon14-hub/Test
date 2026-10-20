"""Pure declaration seams: no world, sensing, scheduling, or action execution."""
from dataclasses import replace
import pytest
from astra_runtime.domain import persistent_world_actor_participation as p
from astra_runtime.domain import persistent_world_actor_evidence as e


def declaration(actor="worker", task="task"):
    return p.Participation(task, actor, "player", "cleaning", "wipe", ("panel", "cloth"),
                           "workshop", "accepted", "predecessor", 2)


def accepted():
    return p.accept(p.ParticipationState(), declaration(), "command", qualified=True)


def due(state, number, outcome="blocked", **kwargs):
    return p.resolve_due(state, "worker", f"interval-{number}", 2 + number,
                         outcome=outcome, qualified=True, profile=p.ParticipationProfile("worker"), **kwargs)


def test_acceptance_requires_qualified_fresh_scoped_actor_declaration():
    original = p.ParticipationState()
    with pytest.raises(p.ParticipationRefusal):
        p.accept(original, declaration(), "command", qualified=False)
    assert original.records == ()
    state = accepted()
    with pytest.raises(p.ParticipationRefusal):
        p.accept(state, declaration(task="second"), "command", qualified=True)
    with pytest.raises(ValueError):
        p.accept(state, declaration(task="second"), "second", qualified=True)
    state = p.accept(state, declaration(actor="other", task="second"), "second", qualified=True)
    assert len(state.records) == 2


def test_three_blocked_due_intervals_withdraw_and_keep_actual_receipts():
    state = due(accepted(), 1, reason="tool unavailable")
    state = due(state, 2, reason="tool unavailable")
    assert p.selected(state, "worker").status == "blocked"
    state = due(state, 3, reason="tool unavailable")
    assert p.selected(state, "worker").status == "withdrawn"
    assert p.selected(state, "worker").contributions == ()
    with pytest.raises(p.ParticipationRefusal):
        due(state, 4, reason="tool unavailable")


def test_real_success_resets_blockage_and_completion_needs_real_receipt():
    state = due(accepted(), 1, reason="tool unavailable")
    state = due(state, 2, "contributed", receipt_id="material-receipt")
    assert p.selected(state, "worker").blocked_due == 0
    state = due(state, 3, "contributed", receipt_id="material-receipt-2", completed=True)
    assert p.selected(state, "worker").status == "completed"
    assert len(p.selected(state, "worker").contributions) == 2


def test_pause_and_not_due_do_not_age_blockage_or_reserve_resources():
    state = due(accepted(), 1, reason="tool unavailable")
    paused = p.pause(state, "worker")
    assert due(paused, 2, reason="tool unavailable") == paused
    assert p.resolve_due(state, "worker", "not-due", 4, outcome="blocked", qualified=False,
                         profile=p.ParticipationProfile("worker"), reason="unavailable") == state
    resumed = p.resume(paused, "worker", qualified=True)
    assert p.selected(resumed, "worker").blocked_due == 1


def test_predecessor_and_duplicate_interval_do_not_contribute():
    state = accepted()
    with pytest.raises(p.ParticipationRefusal):
        p.resolve_due(state, "worker", "predecessor", 3, outcome="contributed", qualified=True,
                      profile=p.ParticipationProfile("worker"), receipt_id="effect")
    state = due(state, 1, "contributed", receipt_id="effect")
    with pytest.raises(p.ParticipationRefusal):
        due(state, 1, "contributed", receipt_id="another-effect")
    with pytest.raises(p.ParticipationRefusal):
        due(state, 2, "contributed", receipt_id="effect")


@pytest.mark.parametrize("outcome,status", [("satisfied", "externally_satisfied"), ("invalidated", "withdrawn")])
def test_external_goal_or_invalid_scope_never_fabricates_contribution(outcome, status):
    state = due(accepted(), 1, outcome, reason="owner qualification")
    assert p.selected(state, "worker").status == status
    assert p.selected(state, "worker").contributions == ()


@pytest.mark.parametrize("limit", [0, -1, True, 33, 1.5])
def test_profile_requires_bounded_positive_integer(limit):
    with pytest.raises(ValueError):
        p.ParticipationProfile("worker", limit)


def event(identity="observed", actor="player", kind="witnessed", source="player", tick=3, value="wet"):
    return e.EvidenceEvent(identity, actor, kind, source, "cloth", "moisture", value,
                           tick, "receipt", "qualified-local-visual")


def test_private_history_does_not_share_witnesses_or_turn_reports_into_truth():
    state = e.record(e.EvidenceState(), event(), qualified=True)
    assert e.latest(state, "worker", "cloth", "moisture") is None
    reported = event("report", "worker", "reported", "player", 4)
    state = e.record(state, reported, qualified=True)
    result = e.latest(state, "worker", "cloth", "moisture")
    assert result.kind == "reported" and result.source_actor_id == "player"
    state = e.record(state, event("changed", tick=5, value="dry"), qualified=True)
    assert e.latest(state, "worker", "cloth", "moisture") == reported


def test_duplicate_evidence_idempotent_but_provenance_forgery_refused():
    first = event()
    state = e.record(e.EvidenceState(), first, qualified=True)
    assert e.record(state, first, qualified=True) is state
    with pytest.raises(ValueError):
        e.record(state, replace(first, value="dry"), qualified=True)
    with pytest.raises(ValueError):
        e.record(state, event("unqualified"), qualified=False)
    with pytest.raises(ValueError):
        e.record(state, event("old", tick=1), qualified=True)


def test_canonical_projection_revalidates_external_references_and_preserves_source():
    state = accepted()
    assert p.canonical_state(state)["records"][0]["eligible_after"] == "predecessor"
    with pytest.raises(ValueError):
        p.canonical_state(state, actor_ids={"worker"})
    evidence = e.record(e.EvidenceState(), event(), qualified=True)
    assert e.canonical_state(evidence)["events"][0]["qualification"] == "qualified-local-visual"
    with pytest.raises(ValueError):
        e.canonical_state(evidence, receipt_ids=set())


@pytest.mark.parametrize("change", [{"value": []}, {"source_actor_id": "other"}, {"tick": True}, {"kind": "truth"}])
def test_evidence_rejects_mutable_or_collapsed_provenance(change):
    with pytest.raises(ValueError):
        replace(event(), **change)
