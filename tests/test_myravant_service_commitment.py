"""Source-bound adversaries for issue #557's opt-in service semantic owner.

These are engineering-authored tests, not independent or human play evidence.
"""
from dataclasses import replace
from types import SimpleNamespace

import pytest

from astra_runtime import myravant_service_commitment as service
from astra_runtime.myravant_tarrow import identity


def terms(version=1):
    return service.make_terms(version=version, requester="player", performer="tali",
        beneficiary="player", target="board", tool="brush", method="scrub",
        peg="whole-peg", recipient="tali")


def task(status="active", contributions=(), *, actor="tali", task_id="task-1"):
    return SimpleNamespace(task_id=task_id, actor_id=actor,
        source_actor_id="player", kind="cleaning", method="scrub",
        participants=("board", "brush"), status=status,
        contributions=contributions)


def accepted():
    state = service.offer(service.ServiceState(), terms(), disclosure_receipt="offer-1")
    return service.decide(state, version=1, fingerprint=terms().fingerprint,
                          accept=True, decision_receipt="decision-1", task_id="task-1")


def test_offer_is_not_acceptance_reservation_or_work():
    state = service.offer(service.ServiceState(), terms(), disclosure_receipt="offer-1")
    record = service.latest(state)
    assert record.state == "offered"
    assert record.task_id is None and not record.work_receipts
    assert record.custody_receipt is None
    assert service.canonical_state(state)["history"][0]["terms"]["peg"] == "whole-peg"


def test_superseded_version_and_fingerprint_fail_closed():
    state = service.offer(service.ServiceState(), terms(), disclosure_receipt="offer-1")
    state = service.offer(state, terms(2), disclosure_receipt="offer-2")
    assert state.history[0].state == "superseded"
    with pytest.raises(ValueError, match="stale"):
        service.decide(state, version=1, fingerprint=terms().fingerprint,
                       accept=True, decision_receipt="decision", task_id="task-1")
    with pytest.raises(ValueError, match="stale"):
        service.decide(state, version=2, fingerprint=terms().fingerprint,
                       accept=True, decision_receipt="decision", task_id="task-1")
    assert service.decide(state, version=2, fingerprint=terms(2).fingerprint,
                          accept=False, decision_receipt="declined").history[-1].state == "declined"


def test_accepted_terms_not_rewritten_and_fingerprint_verified():
    with pytest.raises(ValueError, match="fingerprint"):
        replace(terms(), tool="unagreed-tool")
    with pytest.raises(ValueError, match="overwritten"):
        service.offer(accepted(), terms(2), disclosure_receipt="offer-2")


def test_third_party_or_fabricated_completion_never_qualifies():
    state = accepted()
    with pytest.raises(ValueError, match="wrong actor"):
        service.reconcile(state, task=task("completed", ("actor-work",), actor="other"),
                          receipt_ids={"actor-work"}, completion_receipt="actor-work")
    with pytest.raises(ValueError, match="missing or changed"):
        service.reconcile(state, task=task("completed", ("invented",)),
                          receipt_ids=(), completion_receipt="invented")
    with pytest.raises(ValueError, match="completion"):
        service.reconcile(state, task=task("active", ("actor-work",)),
                          receipt_ids={"actor-work"}, completion_receipt="actor-work")


def test_partial_real_work_survives_withdrawal_and_cannot_settle():
    state = service.reconcile(accepted(), task=task("active", ("work-1",)),
                              receipt_ids={"work-1"})
    assert service.latest(state).state == "partial"
    state = service.withdraw(state, receipt="withdraw-1")
    assert service.latest(state).work_receipts == ("work-1",)
    with pytest.raises(ValueError, match="qualified"):
        service.settle(state, custody_receipt="custody-1",
                       actual_object="whole-peg", giver="player", recipient="tali")


def test_completed_work_requires_matching_real_single_custody_receipt():
    state = service.reconcile(accepted(), task=task("completed", ("work-1", "work-2")),
                              receipt_ids={"work-1", "work-2"}, completion_receipt="work-2")
    assert service.latest(state).state == "eligible"
    with pytest.raises(ValueError, match="matching"):
        service.settle(state, custody_receipt="fake",
                       actual_object="other-peg", giver="player", recipient="tali")
    settled = service.settle(state, custody_receipt="custody-1",
                             actual_object="whole-peg", giver="player", recipient="tali")
    assert service.latest(settled).state == "settled"
    with pytest.raises(ValueError, match="qualified"):
        service.settle(settled, custody_receipt="custody-2",
                       actual_object="whole-peg", giver="player", recipient="tali")
    with pytest.raises(ValueError, match="missing"):
        service.canonical_state(settled,
            receipt_ids={"offer-1", "decision-1", "work-1", "work-2"})
    assert len(service.canonical_state(settled,
        receipt_ids={"offer-1", "decision-1", "work-1", "work-2", "custody-1"})["history"]) == 1


def test_service_fixture_changes_root_and_does_not_change_base_actors():
    from astra_runtime.myravant_tarrow_actors import create_actor_fixture
    base = create_actor_fixture()
    profile = create_actor_fixture(service_peg=True)
    assert base.campaign_id != profile.campaign_id
    assert identity("service-peg") not in {x.entity_id for x in base.object_presentations}
    assert identity("service-peg") in {x.entity_id for x in profile.object_presentations}
    tali = next(p for p in profile.actor_profiles if p.actor_id == identity("tali"))
    assert tali.standing_kind is None


def test_service_application_rejects_cross_profile_load():
    from astra_runtime.myravant_service_application import ServiceApplication
    from astra_runtime.myravant_tarrow_actors import create_actor_fixture
    with pytest.raises(ValueError, match="service profile"):
        ServiceApplication.new(fixture=create_actor_fixture())
    app = ServiceApplication.new()
    assert app.service_state.history == ()
    assert app.checkpoint_format == "myravant.tarrow-service-personal-commitment-journal"
