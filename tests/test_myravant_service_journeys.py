"""Installed opt-in service journeys; each starts with a fresh profile-bound root."""
import pytest

from astra_runtime.myravant_service_application import ServiceApplication
from astra_runtime import myravant_service_commitment as service
from astra_runtime.myravant_tarrow import identity


def at_tali(app):
    for direction in ("south", "west"):
        result = app.move(direction)
        assert result.authoritative_changed, result.message


def offer_and_accept(app):
    at_tali(app)
    result = app.offer_service()
    assert result.authoritative_changed, result.message
    record = service.latest(app.service_state)
    result = app.respond_service(record.terms.version, record.terms.fingerprint)
    assert result.authoritative_changed, result.message
    return record.terms


@pytest.mark.parametrize("_repeat", range(2))
def test_complete_return_and_once_only_custody(_repeat, tmp_path):
    checkpoint = tmp_path / "service.json"
    app = ServiceApplication.new(checkpoint_path=checkpoint)
    terms = offer_and_accept(app)
    for _ in range(8):
        if service.latest(app.service_state).state == "eligible":
            break
        result = app.wait()
        assert result.authoritative_changed, result.message
    assert service.latest(app.service_state).state == "eligible"
    assert app.service_state.history[-1].work_receipts
    assert app.service_state.history[-1].completion_receipt
    # Explicit departure/re-entry does not invent present knowledge.
    assert app.move("east").authoritative_changed
    remote = app.service_status()
    assert "Current progress is unavailable" in remote.message
    assert app.move("west").authoritative_changed
    peg = app.pickup("Service Workshop Peg")
    assert peg.authoritative_changed, peg.message
    handoff = app.settle_service()
    assert handoff.authoritative_changed, handoff.message
    assert service.latest(app.service_state).state == "settled"
    custody_receipt = service.latest(app.service_state).custody_receipt
    repeat = app.settle_service()
    assert not repeat.authoritative_changed
    assert service.latest(app.service_state).custody_receipt == custody_receipt
    assert ServiceApplication.restore(checkpoint_path=checkpoint).authoritative_digest() == app.authoritative_digest()


@pytest.mark.parametrize("_repeat", range(2))
def test_partial_work_withdrawal_remains_unsettled(_repeat, tmp_path):
    app = ServiceApplication.new(checkpoint_path=tmp_path / "withdrawal.json")
    offer_and_accept(app)
    # A first interval may only acquire a brush; it must not grant eligibility.
    assert app.wait().authoritative_changed
    assert service.latest(app.service_state).state in {"accepted", "partial"}
    withdrawn = app.withdraw_service()
    assert withdrawn.authoritative_changed, withdrawn.message
    record = service.latest(app.service_state)
    assert record.state == "withdrawn" and record.custody_receipt is None
    assert not app.settle_service().authoritative_changed
    restored = ServiceApplication.restore(checkpoint_path=tmp_path / "withdrawal.json")
    assert restored.authoritative_digest() == app.authoritative_digest()


def test_decline_stale_and_missing_peg_never_settle(tmp_path):
    app = ServiceApplication.new(checkpoint_path=tmp_path / "declined.json")
    at_tali(app)
    assert app.offer_service().authoritative_changed
    first = service.latest(app.service_state).terms
    assert app.offer_service().authoritative_changed
    assert not app.respond_service(first.version, first.fingerprint).authoritative_changed
    current = service.latest(app.service_state).terms
    assert app.respond_service(current.version, current.fingerprint, accept=False).authoritative_changed
    assert not app.settle_service().authoritative_changed
    assert ServiceApplication.restore(checkpoint_path=tmp_path / "declined.json").authoritative_digest() == app.authoritative_digest()


def test_public_parser_isolated_to_service_profile():
    from astra_runtime.myravant_service_application import execute_service_locality_request
    app = ServiceApplication.new()
    assert not app.service_state.history
    kind, result = execute_service_locality_request(app, "offer tali service")
    assert kind == "service" and not result.authoritative_changed  # Tali is not local
    assert not app.service_state.history
    assert identity("service-peg") in {o.entity_id for o in app.fixture.object_presentations}


@pytest.mark.parametrize("_repeat", range(2))
def test_actual_brush_shortage_blocks_and_recovery_is_requalified(_repeat, tmp_path):
    """A held-away brush is not reserved by the service offer."""
    app = ServiceApplication.new(checkpoint_path=tmp_path / "shortage.json")
    offer_and_accept(app)
    taken = app.pickup("Cleaning Brush")
    assert taken.authoritative_changed, taken.message
    # The player now holds the only qualified brush. Tali cannot take it.
    assert service.latest(app.service_state).state != "eligible"
    assert service.latest(app.service_state).custody_receipt is None
    dropped = app.drop("Cleaning Brush")
    assert dropped.authoritative_changed, dropped.message
    for _ in range(8):
        if service.latest(app.service_state).state == "eligible":
            break
        assert app.wait().authoritative_changed
    assert service.latest(app.service_state).state == "eligible"
    assert ServiceApplication.restore(
        checkpoint_path=tmp_path / "shortage.json"
    ).authoritative_digest() == app.authoritative_digest()
