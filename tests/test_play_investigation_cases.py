"""Case histories are owner-executed, reproducible and never regenerated on restore."""
from pathlib import Path

import pytest

from astra_runtime.myravant_investigation_cases import (
    PREHISTORIES, build_investigation_case,
)
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture


@pytest.mark.parametrize("recipe", tuple(PREHISTORIES))
def test_generated_history_is_real_repeatable_and_checkpoint_bound(recipe, tmp_path):
    outcomes = []
    for repeat in range(2):
        file = tmp_path / str(repeat) / "history.json"
        file.parent.mkdir()
        app, receipts = build_investigation_case(recipe, file)
        assert receipts and all(receipt for _, receipt in receipts)
        assert app.journal and file.exists()
        assert app.fixture.actors_version == 'investigation-neutral-1-' + recipe.removeprefix('neutral-')
        before = app.authoritative_digest()
        restored = InvestigationApplication.restore(
            fixture=create_investigation_fixture(recipe), checkpoint_path=file)
        assert restored.authoritative_digest() == before
        assert restored.journal == app.journal
        outcomes.append((before, receipts))
        with pytest.raises(ValueError, match="existing checkpoint"):
            build_investigation_case(recipe, file)
    assert outcomes[0] == outcomes[1]


def test_two_causal_resource_histories_have_distinct_winners_and_aftermath(tmp_path):
    a, _ = build_investigation_case("neutral-contended", tmp_path / "a.json")
    b, _ = build_investigation_case("neutral-reverse", tmp_path / "b.json")
    assert a.fixture.actor_order[0] != b.fixture.actor_order[0]
    assert a.authoritative_digest() != b.authoritative_digest()


def test_history_report_is_an_assertion_and_cannot_clean_a_panel(tmp_path):
    app, receipts = build_investigation_case("neutral-relay", tmp_path / "relay.json")
    panel = next(p.entity_id for p in app.fixture.object_presentations if p.name == "Panel A")
    assert dict(app.water_state.adhered)[panel] == 3
    history = app.recall_history("panel a", "residue")
    assert "received statement" in history.message and "clear" in history.message
    before = (app.authoritative_digest(), app.journal, app.evidence_state)
    for _ in range(3):
        app.compare_history("panel a", "residue")
    assert before == (app.authoritative_digest(), app.journal, app.evidence_state)
