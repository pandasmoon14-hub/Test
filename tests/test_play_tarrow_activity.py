"""Package #563: finite NPC cross-goal work, replay and public intervention."""
from dataclasses import replace
import io
import json

import pytest

from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime.domain.persistent_world_material import placement, MaterialError, digest
from astra_runtime.myravant_activity_application import ActivityApplication
from astra_runtime.myravant_actor_activity import ActivityMethod, ActivityStage, ActivityProgram
from astra_runtime.myravant_tarrow_activity import create_activity_fixture, execute_activity_request
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_structures import create_structures_fixture
from astra_runtime.myravant_structures_application import StructuresApplication
from astra_runtime.myravant_terminal import run_terminal


def app(tmp_path=None, activity_case="standard"):
    return ActivityApplication.new(
        fixture=create_activity_fixture(activity_case=activity_case),
        checkpoint_path=tmp_path / "activity.json" if tmp_path else None)


def changed(result):
    assert result.authoritative_changed, result.message
    return result


def tick(a):
    return a.runtime_state.logical_time_state.logical_position


def test_activity_root_differs_without_rewriting_structures():
    old = create_structures_fixture()
    new = create_activity_fixture()
    assert old.provenance.fixture_version.startswith("structures-1-")
    assert new.provenance.fixture_version.startswith("activity-2-")
    assert new.provenance.fixture_version != old.provenance.fixture_version
    assert new.activity_programs[0].stages[0].options[0].kind == "cleaning"
    assert new.activity_programs[0].stages[1].options[0].kind == "assembly"
    assert new.activity_programs[0].stages[-1].options[0].kind == "recovery"
    with pytest.raises(ValueError):
        create_activity_fixture(activity_case="unbounded")
    with pytest.raises(ValueError):
        ActivityStage(())
    with pytest.raises(ValueError):
        ActivityProgram("non-work", identity("oren"),
                        (ActivityStage((ActivityMethod("recovery", "drop",
                                                      (identity("cleaning-cloth"),),
                                                      identity("work-bench")),)),) * 2)


def test_acceptance_is_zero_time_with_explicit_consent_and_no_reservation(tmp_path):
    a = app(tmp_path)
    before = tick(a)
    changed(a.request_activity("Oren Kesh", "bench upkeep"))
    assert tick(a) == before
    record = a.activity_records[0]
    assert record.status == "active" and record.task_id is None
    assert not a.participation_state.records
    assert "reserves no tools" in a.activity_status("Oren Kesh").message or tick(a) == 0
    assert not a.request_activity("Oren Kesh", "bench upkeep").authoritative_changed
    assert a.activity_records[0].activity_id == record.activity_id
    changed(a.wait())
    assert tick(a) == 1 and a.activity_records[0].task_id is not None
    assert len(a.participation_state.records) == 1
    b = ActivityApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()
    assert b.activity_records == a.activity_records


def test_real_clean_assembly_recovery_chain_and_durable_stage_boundaries(tmp_path):
    a = app(tmp_path)
    changed(a.request_activity("Oren Kesh", "bench upkeep"))
    initial = dict(a.water_state.adhered)[identity("practice-panel")]
    for _ in range(45):
        changed(a.wait())
        if a.activity_records[0].status != "active":
            break
    record = a.activity_records[0]
    assert record.status == "completed", (record, a.participation_state.records)
    assert len(record.stages_finished) == 3
    assert tuple(status for _, _, status, _ in record.stages_finished) == (
        "completed", "completed", "completed")
    assert dict(a.water_state.adhered)[identity("practice-panel")] <= initial
    assert any(c.left == identity("repair-board") and c.fastener == identity("repair-cord")
               for c in a.connections)
    p = placement(a.state.representation, identity("cleaning-cloth"))
    assert p.relation_type == "located_at" and p.object_entity_id == identity("work-bench")
    assert len(set(record.task_ids)) == len(record.task_ids)
    assert all(receipt in {c for t in a.participation_state.records for c in t.contributions}
               for _, _, _, receipt in record.stages_finished if receipt)
    b = ActivityApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()
    changed(b.wait())
    assert b.activity_records[0].status == "completed"
    assert b.activity_records[0].stages_finished == record.stages_finished


@pytest.mark.parametrize("activity_case", ["standard", "contended"])
def test_actor_order_and_intermediate_restore_are_stable(tmp_path, activity_case):
    a = app(tmp_path, activity_case)
    assert a.fixture.actor_order == ((identity("tali"), identity("oren"))
                                  if activity_case == "contended" else
                                  (identity("oren"), identity("tali")))
    changed(a.wait())
    changed(a.wait())
    saved = tick(a)
    b = ActivityApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert tick(b) == saved
    assert b.authoritative_digest() == a.authoritative_digest()
    for _ in range(3):
        changed(a.wait())
        changed(b.wait())
    assert a.authoritative_digest() == b.authoritative_digest()


def test_cancel_keeps_acknowledged_owner_prefix(tmp_path):
    a = app(tmp_path)
    changed(a.request_activity("Oren Kesh", "bench upkeep"))
    changed(a.wait())
    prefix = a.participation_state.records[-1].contributions
    position = tick(a)
    changed(a.cancel_activity("Oren Kesh"))
    assert tick(a) == position
    assert a.activity_records[0].status == "withdrawn"
    assert a.participation_state.records[-1].contributions == prefix
    for _ in range(2):
        changed(a.wait())
    assert a.activity_records[0].stages_finished == ()
    b = ActivityApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()


def test_old_structures_loader_rejects_activity_profile(tmp_path):
    a = app(tmp_path)
    changed(a.request_activity("Oren Kesh", "bench upkeep"))
    with pytest.raises(MaterialError):
        StructuresApplication.restore(fixture=create_structures_fixture(),
                                      checkpoint_path=a.checkpoint_path)


@pytest.mark.parametrize("corruption", ["profile", "journal", "last_state"])
def test_resealed_activity_checkpoint_tampering_fails(tmp_path, corruption):
    a = app(tmp_path)
    changed(a.request_activity("Oren Kesh", "bench upkeep"))
    changed(a.wait())
    envelope = json.loads(a.checkpoint_path.read_text())
    payload = envelope["payload"]
    if corruption == "profile":
        payload["profile"]["programs"][0]["actor_id"] = identity("tali")
    elif corruption == "journal":
        payload["journal"][-1]["result"]["receipt_id"] = "actor:fake"
    else:
        payload["final"] = "f" * 64
    envelope["integrity_digest"] = digest(payload)
    a.checkpoint_path.write_text(json.dumps(envelope))
    with pytest.raises(MaterialError):
        ActivityApplication.restore(fixture=a.fixture, checkpoint_path=a.checkpoint_path)


def test_installed_terminal_routes_admission_wait_and_local_status():
    a = app()
    out = io.StringIO()
    run_terminal(a, input_stream=io.StringIO(
        "help\ngo south\ngo west\nask oren kesh to undertake bench upkeep\n"
        "wait\nask oren kesh about activity\nexit\n"),
        output_stream=out, specialized_router=execute_activity_request)
    assert "Actor activities" in out.getvalue()
    assert "bench upkeep" in out.getvalue()
    assert len(a.activity_records) == 1
    assert tick(a) >= 3
    assert a.activity_records[0].task_ids


def test_private_remote_activity_status_is_not_live_state():
    a = app()
    changed(a.request_activity("Oren Kesh", "bench upkeep"))
    changed(a.wait())
    # No generic remote live window: at most a last communicated agreement.
    result = a.activity_status("Oren Kesh")
    assert not result.authoritative_changed
    assert "remote" in result.message.casefold() or "last communicated" in result.message.casefold()
