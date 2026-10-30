"""P1: existing owners in ONE real journal, not joined independent saves."""
from dataclasses import replace
import json
import subprocess
import sys

import pytest

from astra_runtime.myravant_shared_campaign import create_shared_campaign_fixture
from astra_runtime.myravant_shared_campaign_application import SharedCampaignApplication
from astra_runtime.myravant_activity_application import ActivityApplication
from astra_runtime.myravant_service_application import ServiceApplication
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow import identity
from astra_runtime.domain.persistent_world_material import MaterialError, digest, placement
from astra_runtime import myravant_service_commitment as service


def changed(outcome):
    assert outcome.authoritative_changed, outcome.message
    return outcome


def go(app, *steps):
    for step in steps:
        changed(app.move(step))


def new(tmp_path, **options):
    return SharedCampaignApplication.new(
        fixture=create_shared_campaign_fixture(**options),
        checkpoint_path=tmp_path / "shared.json")


def test_one_root_executes_personal_service_physical_work_and_history_after_restart(tmp_path):
    app = new(tmp_path)
    original_root = app.fixture.provenance.initial_state_digest
    original_campaign = app.fixture.campaign_id
    original_clock = app.runtime_state.logical_time_state.logical_position
    original_residue = dict(app.water_state.adhered)[identity("sorting-board")]

    # Tali's service is not a standing task or a free item reservation.
    go(app, "south", "west")
    changed(app.offer_service())
    terms = service.latest(app.service_state).terms
    changed(app.respond_service(terms.version, terms.fingerprint))
    premature = app.settle_service()
    assert not premature.authoritative_changed
    assert service.latest(app.service_state).custody_receipt is None
    for _ in range(12):
        if service.latest(app.service_state).state == "eligible":
            break
        changed(app.wait())
    assert service.latest(app.service_state).state == "eligible"
    assert service.latest(app.service_state).work_receipts
    assert dict(app.water_state.adhered)[identity("sorting-board")] <= original_residue

    # Exact whole-object custody is a separate voluntary action.
    changed(app.pickup("Service Workshop Peg"))
    changed(app.settle_service())
    paid = service.latest(app.service_state)
    assert paid.state == "settled" and paid.custody_receipt
    assert placement(app.state.representation, identity("service-peg")).object_entity_id == identity("tali")
    assert not app.settle_service().authoritative_changed

    # Oren's distinct finite program uses the same continuing world/clock.
    go(app, "west", "west")
    changed(app.request_activity("Oren Kesh", "bench upkeep"))
    for _ in range(45):
        changed(app.wait())
        if app.activity_records[0].status != "active":
            break
    assert app.activity_records[0].status == "completed"
    assert len(app.activity_records[0].stages_finished) == 3
    assert any(c.left == identity("repair-board") and c.fastener == identity("repair-cord")
               for c in app.connections)

    # Inquiry cannot simply read truth from the fixture, including remotely.
    changed(app.inspect("Practice Panel"))
    prior_digest = app.authoritative_digest()
    historical = app.recall_history("Practice Panel", "residue")
    comparison = app.compare_history("Practice Panel", "residue")
    assert not historical.authoritative_changed and not comparison.authoritative_changed
    assert app.authoritative_digest() == prior_digest
    assert "Retained player history" in historical.message
    assert "No account is selected as true" in comparison.message

    # Leave, advance the ONE clock, and return to a local communication route.
    go(app, "east")
    changed(app.wait())
    offsite = app.activity_status("Oren Kesh")
    assert not offsite.authoritative_changed
    assert "remote" in offsite.message.casefold() or "last communicated" in offsite.message.casefold()
    go(app, "west")
    changed(app.activity_status("Oren Kesh"))
    changed(app.save()) if False else app.save()  # save is read-only and checkpoint-bound
    resume = SharedCampaignApplication.restore(checkpoint_path=app.checkpoint_path)
    assert resume.authoritative_digest() == app.authoritative_digest()
    assert resume.fixture.campaign_id == original_campaign
    assert resume.fixture.provenance.initial_state_digest == original_root
    assert resume.runtime_state.logical_time_state.logical_position > original_clock
    assert resume.activity_records == app.activity_records
    assert resume.service_state == app.service_state
    assert resume.evidence_state == app.evidence_state
    assert resume.journal == app.journal
    changed(resume.wait())
    again = SharedCampaignApplication.restore(checkpoint_path=app.checkpoint_path)
    assert again.authoritative_digest() == resume.authoritative_digest()


def test_busy_actor_and_withheld_tool_change_next_interval_without_fabrication(tmp_path):
    app = new(tmp_path)
    go(app, "south", "west")
    changed(app.offer_service())
    terms = service.latest(app.service_state).terms
    changed(app.respond_service(terms.version, terms.fingerprint))
    # Prevent the NPC from obtaining the only qualified tool.
    changed(app.pickup("Cleaning Brush"))
    for _ in range(3):
        changed(app.wait())
    assert service.latest(app.service_state).state != "eligible"
    assert service.latest(app.service_state).custody_receipt is None
    before = app.authoritative_digest()
    assert not app.settle_service().authoritative_changed
    assert app.authoritative_digest() == before
    paused = SharedCampaignApplication.restore(checkpoint_path=app.checkpoint_path)
    assert paused.authoritative_digest() == before
    changed(paused.drop("Cleaning Brush"))
    for _ in range(12):
        if service.latest(paused.service_state).state == "eligible":
            break
        changed(paused.wait())
    assert service.latest(paused.service_state).state == "eligible"
    assert SharedCampaignApplication.restore(
        checkpoint_path=app.checkpoint_path).authoritative_digest() == paused.authoritative_digest()


def test_opt_in_root_does_not_convert_old_profiles_or_trust_forged_witness(tmp_path):
    shared = new(tmp_path)
    first = shared.fixture
    activity = ActivityApplication.default_fixture()
    service_root = ServiceApplication.default_fixture()
    investigation = InvestigationApplication.default_fixture()
    assert first.provenance.fixture_version.startswith("shared-campaign-1-")
    assert first.campaign_id not in {activity.campaign_id, service_root.campaign_id,
                                     investigation.campaign_id}
    assert identity("service-peg") not in {o.entity_id for o in activity.object_presentations}
    changed(shared.move("south"))
    with pytest.raises(MaterialError):
        ActivityApplication.restore(checkpoint_path=shared.checkpoint_path)
    with pytest.raises(MaterialError):
        ServiceApplication.restore(checkpoint_path=shared.checkpoint_path)
    with pytest.raises(MaterialError):
        InvestigationApplication.restore(checkpoint_path=shared.checkpoint_path)

    blob = json.loads(shared.checkpoint_path.read_text())
    blob["payload"]["profile"]["shared_binding"] = "fake-other-root"
    blob["integrity_digest"] = digest(blob["payload"])
    shared.checkpoint_path.write_text(json.dumps(blob))
    with pytest.raises(MaterialError):
        SharedCampaignApplication.restore(checkpoint_path=shared.checkpoint_path)


def test_alternative_activity_root_preserves_separate_root_and_replay(tmp_path):
    standard = create_shared_campaign_fixture()
    contended = create_shared_campaign_fixture(activity_case="contended",
                                                structures_case="cross-workshop")
    assert standard.campaign_id != contended.campaign_id
    app = SharedCampaignApplication.new(fixture=contended,
                                        checkpoint_path=tmp_path / "variant.json")
    changed(app.wait())
    restored = SharedCampaignApplication.restore(
        checkpoint_path=app.checkpoint_path, fixture=contended)
    assert restored.authoritative_digest() == app.authoritative_digest()
    with pytest.raises(MaterialError):
        SharedCampaignApplication.restore(checkpoint_path=app.checkpoint_path)


def test_public_two_sessions_share_activity_service_and_investigation_routes(tmp_path):
    checkpoint = tmp_path / "one-world.json"
    base = [sys.executable, "-m", "astra_runtime.myravant_terminal",
            "--locality", "tarrow-shared"]
    first = subprocess.run([*base, "--checkpoint", str(checkpoint)],
        input="help\ngo south\ngo west\noffer tali service\n"
              "ask tali about service\nsave\nexit\n",
        text=True, capture_output=True, timeout=120)
    assert first.returncode == 0, (first.stdout, first.stderr)
    assert checkpoint.exists()
    assert "Fingerprint" in first.stdout
    assert "Shared local campaign" in first.stdout
    second = subprocess.run([*base, "--load", str(checkpoint)],
        input="go west\ngo west\nask oren kesh to undertake bench upkeep\n"
              "wait\ninspect practice panel\nrecall practice panel residue\n"
              "compare reports about practice panel residue\nsave\nexit\n",
        text=True, capture_output=True, timeout=120)
    assert second.returncode == 0, (second.stdout, second.stderr)
    assert "bench upkeep" in second.stdout
    assert "Retained player history" in second.stdout
    assert "Comparison of retained" in second.stdout
    restored = SharedCampaignApplication.restore(checkpoint_path=checkpoint)
    assert restored.service_state.history
    assert restored.activity_records
    assert restored.journal
