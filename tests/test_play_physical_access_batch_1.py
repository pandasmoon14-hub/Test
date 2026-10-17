"""Physical-access batch: public availability, generality and objective evidence.

Implementation-authored acceptance, not independent held-out or human play.
Neutral fixture additions explicitly license methods; they imply no physics.
"""
from dataclasses import replace
from io import StringIO
import json
import shutil
import subprocess

import pytest

from astra_runtime.domain.persistent_world_entity_location_representation import (
    LOCATED_AT_RELATION_TYPE, create_persistent_world_entity,
    create_located_at_relation, create_persistent_world_entity_location_representation,
)
from astra_runtime.domain.persistent_world_movement_integration import (
    create_persistent_world_movement_runtime_state,
    digest_persistent_world_entity_location_representation,
)
from astra_runtime import myravant_play_fixture as fixture_module
from astra_runtime.myravant_play_fixture import (
    LANTERN_ID, TOOL_CHEST_ID, WAYSTONE_ID, WORKSHOP_ID, YARD_ID, ORCHARD_PATH_ID,
    FixtureObjectDisplacementRoute, PublicEntityPresentation,
    UnknownFixturePlaceError, create_terminal_play_fixture,
)
from astra_runtime.myravant_physical_placement_goal import (
    execute_physical_placement_goal, parse_physical_placement_goal,
)
from astra_runtime.myravant_goal_method_lantern import parse_lantern_destination_goal
from astra_runtime.myravant_terminal import (
    _explicit_two_step_intent, run_terminal,
)
from astra_runtime.myravant_terminal_capabilities import execute_bounded_terminal_request
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def _place(app, target):
    return next(r.object_entity_id for r in app.state.representation.relations
                if r.subject_entity_id == target and r.relation_type == LOCATED_AT_RELATION_TYPE)


def _run(app, *commands):
    output = StringIO()
    assert run_terminal(app, input_stream=StringIO("\n".join((*commands, "exit", ""))),
                        output_stream=output,
                        specialized_router=execute_bounded_terminal_request) == 0
    return output.getvalue()


def _neutral_fixture(identity, name, *, reorder=False, source=WORKSHOP_ID):
    """Compatible new identity and explicit routes, no stock target substitution."""
    fixture = create_terminal_play_fixture()
    representation = fixture.initial_state.representation
    representation = create_persistent_world_entity_location_representation(
        campaign_id=fixture.campaign_id,
        entities=(*representation.entities,
                  create_persistent_world_entity(entity_id=identity, classification="object")),
        relations=(*representation.relations, create_located_at_relation(
            relation_id="astra:relation:neutral-start", subject_entity_id=identity,
            object_entity_id=source)),
    )
    direction, destination = ("south", YARD_ID) if source == WORKSHOP_ID else ("north", WORKSHOP_ID)
    fixture = replace(
        fixture,
        initial_state=create_persistent_world_movement_runtime_state(representation=representation),
        provenance=replace(fixture.provenance,
            initial_state_digest=digest_persistent_world_entity_location_representation(representation)),
        object_presentations=(*fixture.object_presentations,
                              PublicEntityPresentation(entity_id=identity, name=name)),
        object_displacement_routes=(*fixture.object_displacement_routes, *(
            FixtureObjectDisplacementRoute(object_entity_id=identity, source_place_id=source,
                direction=direction, destination_place_id=destination, method=method)
            for method in ("push", "slide", "drag"))),
    )
    initial_app = MyravantVSM14Application.new(fixture=fixture)
    fixture = replace(fixture, provenance=replace(fixture.provenance,
        fixture_id="physical-access-neutral-validation",
        fixture_version="test-1",
        origin_workstream="PLAY-PHYSICAL-ACCESS-BATCH-1-test",
        initial_world_state_digest=fixture_module.digest_persistent_world_composite_state(
            representation, fixture.initial_object_open_states),
        initial_int2_world_state_digest=fixture_module.digest_persistent_world_lit_composite_state(
            initial_app.object_state, fixture.initial_object_lit_states),
        initial_int3_world_state_digest=fixture_module.digest_persistent_world_storage_composite_state(
            initial_app._lit_state)))
    if reorder:
        fixture = replace(fixture,
            place_presentations=tuple(replace(p, name="Assembly Deck" if p.entity_id == WORKSHOP_ID else p.name) for p in fixture.place_presentations))
        fixture = replace(fixture,
            object_presentations=tuple(reversed(fixture.object_presentations)),
            place_presentations=tuple(reversed(fixture.place_presentations)),
            object_displacement_routes=tuple(reversed(fixture.object_displacement_routes)))
    return fixture, destination


@pytest.mark.parametrize("identity,name", [
    ("astra:entity:neutral-crate", "Painted Crate"),
    ("astra:entity:neutral-sled", "Validation Sled"),
])
@pytest.mark.parametrize("method", ["push", "slide", "drag"])
@pytest.mark.parametrize("source,reorder", [(WORKSHOP_ID, False), (YARD_ID, True)])
def test_new_identity_methods_and_arrangements_use_real_public_routes_and_restore(
    tmp_path, identity, name, method, source, reorder,
):
    fixture, destination = _neutral_fixture(identity, name, reorder=reorder, source=source)
    checkpoint = tmp_path / "neutral.json"
    app = MyravantVSM14Application.new(fixture=fixture, checkpoint_path=checkpoint)
    if source == YARD_ID:
        assert app.move("south").authoritative_changed
    place_name = fixture.entity_name(destination)
    query = f"get {name} to {place_name}"
    before = app.authoritative_digest()
    advice = execute_bounded_terminal_request(app, query)
    assert advice[0] == "physical_placement_goal"
    assert advice[1].pre_state_digest == advice[1].post_state_digest == before
    assert method in advice[1].message
    text = _run(app, f"{query} by {method}")
    assert f"You {method} the {name}" in text
    assert _place(app, identity) == destination
    assert app.displacement_state.committed_object_displacement_transitions[-1].receipt.method == method
    assert app.save().checkpoint_digest
    restored = MyravantVSM14Application.restore(checkpoint_path=checkpoint, fixture=fixture)
    assert restored.authoritative_digest() == app.authoritative_digest()
    assert _place(restored, identity) == destination
    # Stale name/old route does not license a second movement or leak advice.
    prior = restored.authoritative_digest()
    refused = execute_bounded_terminal_request(restored, query)[1]
    assert refused.failure_class == "physical_goal_local_evidence_unavailable"
    assert restored.authoritative_digest() == prior


@pytest.mark.parametrize("modifier", ["pulling", "pulling it", "rotating", "quietly sliding", "sliding without opening it", "pushing waystone north"])
def test_material_methods_are_never_silently_rewritten(modifier):
    app = MyravantVSM14Application.new()
    assert app.move("south").authoritative_changed
    before = app.authoritative_digest()
    result = execute_physical_placement_goal(app, f"get chest to workshop by {modifier}")
    assert result.failure_class == "physical_goal_method_unqualified"
    assert result.receipt_id is None
    assert result.pre_state_digest == result.post_state_digest == before
    assert app.authoritative_digest() == before


@pytest.mark.parametrize("raw", [
    "get lantern to yard by sliding and wait",
    "get lantern to yard while going south",
    "get lantern to yard without making noise",
    "get that to yard by sliding",
    "get lantern to yard by sliding then invent wings",
    "get lantern to yard by sliding then go south then wait",
])
def test_ambiguous_or_unbounded_input_never_mutates(raw):
    app = MyravantVSM14Application.new()
    before = app.authoritative_digest()
    _run(app, raw)
    assert app.authoritative_digest() == before


def test_reference_ambiguity_never_selects_a_place_or_object():
    fixture = create_terminal_play_fixture()
    places = tuple(replace(p, name="Shared Hall" if p.entity_id in {YARD_ID, WORKSHOP_ID} else p.name)
                   for p in fixture.place_presentations)
    variant = replace(fixture, place_presentations=places)
    with pytest.raises(UnknownFixturePlaceError):
        variant.resolve_place_reference("shared")
    assert parse_physical_placement_goal("get lantern to shared by sliding", fixture=variant) is None
    objects = tuple(replace(p, name="Shared Box" if p.entity_id in {LANTERN_ID, TOOL_CHEST_ID} else p.name)
                    for p in fixture.object_presentations)
    variant = replace(fixture, object_presentations=objects)
    assert parse_physical_placement_goal("get shared box to yard by sliding", fixture=variant) is None


def test_custody_filters_methods_and_real_throw_replaces_ground_placement(tmp_path):
    # Generic goals can qualify any declared object; the public Lantern ->
    # Orchard adapter retains its prior precedence and voluntary NPC route.
    app = MyravantVSM14Application.new(checkpoint_path=tmp_path / "custody.json")
    _run(app, "get lantern to yard by sliding then go south")
    assert _place(app, LANTERN_ID) == YARD_ID
    assert app.current_place_id() == YARD_ID
    assert app.pickup("lantern").authoritative_changed
    result = execute_physical_placement_goal(app, "get lantern to orchard")
    assert "throw east" in result.message and "push east" not in result.message
    prior = app.authoritative_digest()
    no_push = execute_physical_placement_goal(app, "get lantern to orchard by pushing")
    assert no_push.failure_class and app.authoritative_digest() == prior
    moved = execute_physical_placement_goal(app, "get lantern to orchard by throwing")
    assert moved.authoritative_changed and moved.receipt_id
    assert _place(app, LANTERN_ID) == ORCHARD_PATH_ID
    app.save()
    restored = MyravantVSM14Application.restore(checkpoint_path=app.checkpoint_path)
    assert restored.authoritative_digest() == app.authoritative_digest()


def test_recognizer_collision_retains_standalone_precedence_in_sequence():
    app = MyravantVSM14Application.new()
    for raw in ("get lantern to orchard", "get lantern to orchard by throwing",
                "get lantern to orchard by asking groundskeeper"):
        assert parse_lantern_destination_goal(raw) is not None
        assert parse_physical_placement_goal(raw, fixture=app.fixture) is not None
        planned = _explicit_two_step_intent(raw + " then look", fixture=app.fixture)
        assert planned[0].action == "destination_goal_method"
        assert execute_bounded_terminal_request(app, raw)[0] == "destination_goal_method"


def _installed(tmp_path, name, commands, *, resume=False):
    launcher = shutil.which("myravant-play")
    assert launcher, "installed public launcher required"
    save = tmp_path / f"{name}.json"
    trace = tmp_path / f"{name}-{'resume' if resume else 'first'}.jsonl"
    args = [launcher, "--checkpoint", str(save), "--trace", str(trace), "--repository-sha", "b" * 40]
    if resume:
        args.extend(["--load", str(save)])
    result = subprocess.run(args, input="\n".join((*commands, "save", "exit", "")),
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, (result.stdout, result.stderr)
    rows = [json.loads(line) for line in trace.read_text().splitlines()]
    assert rows[-1]["evidence_complete"]
    return [r for r in rows if r["record_type"] == "interaction"], MyravantVSM14Application.restore(checkpoint_path=save)


@pytest.mark.parametrize("method", ["pushing", "sliding"])
def test_installed_multiple_approaches_to_persistent_access_goal(tmp_path, method):
    # Dark contact -> actual obstruction -> choice: bypass vs clear -> return.
    rows, app = _installed(tmp_path, method, (
        "go south", "go east", "feel for waystone then get waystone to yard by dragging",
        "go west", "go east", "crawl east", "go west", "save",
    ))
    assert _place(app, WAYSTONE_ID) == YARD_ID
    assert app.current_place_id() == YARD_ID
    assert any(r["failure_class"] == "movement_opportunity_obstructed" for r in rows)
    rows2, restored = _installed(tmp_path, method, (
        f"get waystone to workshop by {method} then go east", "wait", "go west", "go east",
    ), resume=True)
    assert restored.current_place_id() == ORCHARD_PATH_ID
    assert _place(restored, WAYSTONE_ID) == WORKSHOP_ID
    chosen = next(r for r in rows2 if r["parsed_action"] == "sequence_1_physical_placement_goal")
    assert chosen["receipt_id"] and chosen["authoritative_changed"]
    assert chosen["post_state_digest"] == rows2[1]["pre_state_digest"]
    assert rows2[1]["parsed_action"] == "sequence_2_move"


def test_installed_goal_sequence_partial_completion_and_no_hidden_plan(tmp_path):
    rows, app = _installed(tmp_path, "partial", (
        "get lantern to yard by sliding then get lantern to orchard by throwing",
    ))
    seq = [r for r in rows if r["parsed_action"].startswith("sequence_")]
    assert len(seq) == 2
    assert seq[0]["authoritative_changed"] and seq[0]["receipt_id"]
    assert seq[1]["failure_class"] and not seq[1]["authoritative_changed"]
    assert seq[0]["post_state_digest"] == seq[1]["pre_state_digest"] == seq[1]["post_state_digest"]
    assert _place(app, LANTERN_ID) == YARD_ID
    assert app.current_place_id() == WORKSHOP_ID
    rows2, app2 = _installed(tmp_path, "failed-first", (
        "get chest to workshop by dragging then go south",
    ))
    assert len([r for r in rows2 if r["parsed_action"].startswith("sequence_")]) == 1
    assert app2.current_place_id() == WORKSHOP_ID


@pytest.mark.parametrize("method", ["push", "slide", "drag", "throw"])
def test_destination_and_directional_routes_have_identical_owner_receipts(method):
    identity, name = "astra:entity:neutral-crate", "Painted Crate"
    fixture, _ = _neutral_fixture(identity, name)
    if method == "throw":
        fixture = replace(fixture, object_displacement_routes=(*fixture.object_displacement_routes,
            FixtureObjectDisplacementRoute(object_entity_id=identity, source_place_id=WORKSHOP_ID,
                direction="south", destination_place_id=YARD_ID, method="throw")))
    apps = [MyravantVSM14Application.new(fixture=fixture) for _ in range(2)]
    if method == "throw":
        for app in apps:
            assert app.pickup(name).authoritative_changed
        advice = execute_physical_placement_goal(apps[0], "get painted crate to yard")
        assert "throw south" in advice.message and "push south" not in advice.message
    goal = execute_physical_placement_goal(apps[0], f"get painted crate to yard by {method}")
    direct = apps[1].displace_object(name, "south", method=method)
    assert goal.authoritative_changed and direct.authoritative_changed
    assert goal.receipt_id == direct.receipt_id
    assert goal.command_fingerprint == direct.command_fingerprint
    assert apps[0].authoritative_digest() == apps[1].authoritative_digest()


def test_two_step_uses_runtime_fixture_references_for_added_targets():
    fixture, _ = _neutral_fixture("astra:entity:neutral-sled", "Validation Sled")
    app = MyravantVSM14Application.new(fixture=fixture)
    output = _run(app, "get validation sled to yard by sliding then go south")
    assert "You slide the Validation Sled south." in output
    assert app.current_place_id() == YARD_ID
    assert _place(app, "astra:entity:neutral-sled") == YARD_ID


def test_destination_with_two_licensed_directions_requires_choice():
    fixture, _ = _neutral_fixture("astra:entity:neutral-crate", "Painted Crate")
    fixture = replace(fixture, object_displacement_routes=(*fixture.object_displacement_routes,
        FixtureObjectDisplacementRoute(object_entity_id="astra:entity:neutral-crate",
            source_place_id=WORKSHOP_ID, direction="east", destination_place_id=YARD_ID,
            method="slide")))
    app = MyravantVSM14Application.new(fixture=fixture)
    before = app.authoritative_digest()
    result = execute_physical_placement_goal(app, "get painted crate to yard by sliding")
    assert result.failure_class == "physical_goal_route_unavailable"
    assert result.receipt_id is None and app.authoritative_digest() == before
