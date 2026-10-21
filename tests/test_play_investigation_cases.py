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



@pytest.mark.parametrize("recipe", tuple(PREHISTORIES))
def test_public_fresh_start_prepares_lawful_history_and_replay(recipe, tmp_path):
    import subprocess
    import sys

    path = tmp_path / (recipe + ".json")
    args = [sys.executable, "-m", "astra_runtime.myravant_terminal",
            "--locality", "tarrow-investigation", "--investigation-case", recipe,
            "--prepare-investigation", "--checkpoint", str(path)]
    result = subprocess.run(
        args, input="recall panel a residue\nsave\nexit\n",
        text=True, capture_output=True, timeout=90,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert "circumstance prepared through committed world actions" in result.stdout
    assert path.exists()
    fixture = create_investigation_fixture(recipe)
    restored = InvestigationApplication.restore(fixture=fixture, checkpoint_path=path)
    assert len(restored.journal) >= len(PREHISTORIES[recipe])
    assert all(e["result"]["receipt_id"] for e in restored.journal[:len(PREHISTORIES[recipe])])
    if recipe == "neutral-relay":
        assert "earlier speaker disclosed as Traveler" in result.stdout
        assert len(restored.disclosed_relays) == 1
    else:
        from astra_runtime.domain.persistent_world_material import placement
        brush = next(p.entity_id for p in fixture.object_presentations if p.name == "Brush")
        assert placement(restored.state.representation, brush).object_entity_id == fixture.actor_order[0]

    # Opening a resumed actor session legitimately performs a qualified
    # initial look, admitting new evidence. Only that operation may extend
    # the acknowledged prefix; recall and save are read-only by contract.
    before_journal = restored.journal
    before_time = restored.runtime_state.logical_time_state.logical_position
    before_water = restored.water_state
    before_connections = restored.connections
    before_relays = restored.disclosed_relays
    replay = subprocess.run(
        [sys.executable, "-m", "astra_runtime.myravant_terminal",
         "--locality", "tarrow-investigation", "--investigation-case", recipe,
         "--load", str(path), "--checkpoint", str(path)],
        input="recall panel a residue\nsave\nexit\n",
        text=True, capture_output=True, timeout=90,
    )
    assert replay.returncode == 0, (replay.stdout, replay.stderr)
    assert "circumstance prepared through committed world actions" not in replay.stdout
    after_replay = InvestigationApplication.restore(fixture=fixture, checkpoint_path=path)
    assert after_replay.journal[:len(before_journal)] == before_journal
    new_entries = after_replay.journal[len(before_journal):]
    assert new_entries and all(entry["method"] == "look" for entry in new_entries)
    assert after_replay.runtime_state.logical_time_state.logical_position == before_time
    assert after_replay.water_state == before_water
    assert after_replay.connections == before_connections
    assert after_replay.disclosed_relays == before_relays
    # Refused *preparation* cannot rewrite any acknowledged save bytes.
    settled_bytes = path.read_bytes()
    denied = subprocess.run(args, input="exit\n", text=True, capture_output=True, timeout=90)
    assert denied.returncode == 2 and "existing checkpoint" in denied.stderr
    assert path.read_bytes() == settled_bytes


@pytest.mark.parametrize("extra", [
    ("--load", "existing.json"),
    (),
])
def test_prepared_start_rejects_ambiguous_or_absent_checkpoint(extra, tmp_path):
    import subprocess
    import sys

    args = [sys.executable, "-m", "astra_runtime.myravant_terminal",
            "--locality", "tarrow-investigation",
            "--investigation-case", "neutral-relay", "--prepare-investigation",
            *extra]
    if extra:
        args += ["--checkpoint", str(tmp_path / "not-created.json")]
    result = subprocess.run(args, input="exit\n",
                            text=True, capture_output=True, timeout=90)
    assert result.returncode == 2
    assert "requires --locality tarrow-investigation" in result.stderr
    assert not (tmp_path / "not-created.json").exists()


@pytest.mark.parametrize("locality,recipe", [
    ("tarrow-investigation", "cleanup"),
    ("tarrow-actors", "neutral-contended"),
])
def test_preparation_cannot_mutate_unrelated_profile(locality, recipe, tmp_path):
    import subprocess
    import sys

    save = tmp_path / "forbidden.json"
    result = subprocess.run(
        [sys.executable, "-m", "astra_runtime.myravant_terminal",
         "--locality", locality, "--investigation-case", recipe,
         "--prepare-investigation", "--checkpoint", str(save)],
        input="exit\n", text=True, capture_output=True, timeout=90,
    )
    assert result.returncode == 2
    assert not save.exists()
