"""Configuration-only transfer to fresh identities and a neutral ring topology."""
from fractions import Fraction

import pytest

from astra_runtime import myravant_play_fixture as f
from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_tarrow_actors import ActorFixture, ActorProfile
from astra_runtime.myravant_tarrow_time import AssemblyProfile
from astra_runtime.domain.persistent_world_material import MaterialProfile, digest, placement
from astra_runtime.domain.persistent_world_water_cleaning import WaterCleaningAsset, WaterCleaningProfile, WaterCleaningState
from astra_runtime.domain.persistent_world_timed_environment import TimedEnvironmentProfile
from astra_runtime.domain import persistent_world_actor_participation as participation


def ident(key):
    return 'astra:entity:neutral-lab-' + key


def neutral_fixture(*, reverse=False, blocked_limit=3):
    """All scenario declarations are constructor inputs; no mutable runtime remap."""
    places = ('entry', 'studio', 'balcony')
    objects = ('signal', 'brush', 'panel-a', 'panel-b', 'tray', 'cloth', 'plate', 'peg', 'cord', 'bench')
    actors = ('jun', 'sol')
    edges = (('entry', 'east', 'studio'), ('studio', 'west', 'entry'),
             ('studio', 'north', 'balcony'), ('balcony', 'south', 'studio'),
             ('balcony', 'west', 'entry'), ('entry', 'north', 'balcony'))
    order = tuple(ident(k) for k in (tuple(reversed(actors)) if reverse else actors))
    campaign = 'astra:campaign:neutral-cooperation-' + digest([edges, order, blocked_limit])[:18]
    entities = tuple(f._entity(ident(k), kind) for keys, kind in (
        (places, 'place'), (objects, 'object'), ((*actors, 'visitor'), 'character_or_creature')) for k in keys)
    relations = tuple(f._located('neutral-' + k, ident(k), ident(place)) for k, place in (
        ('visitor', 'entry'), *((k, 'studio') for k in (*actors, *objects))))
    rep = f.create_persistent_world_entity_location_representation(campaign_id=campaign, entities=entities, relations=relations)
    lights = (f.create_persistent_world_object_lit_state(object_entity_id=ident('signal'), state='unlit'),)
    movement = f.create_persistent_world_movement_runtime_state(representation=rep)
    custody = f.create_persistent_world_object_custody_runtime_state(movement_state=movement)
    opened = f.create_persistent_world_object_open_close_runtime_state(custody_state=custody, object_open_states=())
    lit = f.create_persistent_world_object_lit_runtime_state(open_close_state=opened, object_lit_states=lights)
    ambient = {ident(p): 'sufficient' for p in places}
    ambient_version = f.FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION
    provenance = f.FixtureProvenanceReceipt(
        fixture_id='neutral-cooperation-laboratory', fixture_version='1', fixture_status='development-test-only',
        canon=False, default_world=False, origin_workstream='PLAY-TARROW-ACTORS-1-transfer',
        origin_merge_commit='0'*40, origin_merged_at='2026-10-19', g1_baseline_sha='0'*40,
        playable_need_refs=('configuration-transfer',), requirement_refs=('REQ-PROD-012',),
        direct_external_content_consulted_during_g1=False, originality_review_status='neutral-engineering-fixture',
        initial_state_digest=f.digest_persistent_world_entity_location_representation(rep),
        initial_world_state_digest=f.digest_persistent_world_composite_state(rep, ()),
        initial_object_lit_state_digest=f.digest_persistent_world_object_lit_states(lights),
        initial_int2_world_state_digest=f.digest_persistent_world_lit_composite_state(opened, lights),
        initial_int3_world_state_digest=f.digest_persistent_world_storage_composite_state(lit),
        ambient_visual_profile_version=ambient_version,
        ambient_visual_condition_digest=f.digest_fixture_ambient_visual_conditions(ambient))
    assets = tuple(WaterCleaningAsset(ident(k), kind, water, residue, rate) for k, kind, water, residue, rate in (
        ('brush', 'brush', 0, 8, 2), ('panel-a', 'surface', 0, 3, 0),
        ('panel-b', 'surface', 0, 3, 0), ('tray', 'tray', 0, 8, 0), ('cloth', 'absorbent', 2, 2, 1)))
    pairs = tuple(('scrub', ident(k), ident('brush')) for k in ('panel-a', 'panel-b')) + (('collect', ident('brush'), ident('tray')),)
    water_profile = WaterCleaningProfile(assets, pairs)
    initial = WaterCleaningState(tuple((a.id, 2 if a.id == ident('cloth') else 0) for a in assets),
        tuple((a.id, 3 if a.id in {ident('panel-a'), ident('panel-b')} else 0) for a in assets), tuple((a.id, 0) for a in assets))
    material = MaterialProfile(ident('visitor'), tuple((ident(k), ident('bench')) for k in ('plate', 'peg')),
        ((ident('plate'), ident('peg'), ident('cord'), 'tie'),))
    assembly = AssemblyProfile('joining frame', ident('studio'), ident('plate'), ident('peg'),
        ident('bench'), ident('bench'), ident('cord'), 'tie')
    profiles = tuple(ActorProfile(ident(actor), blocked_limit=blocked_limit, methods=('scrub',),
        cleaning_pairs=((ident(panel), ident('brush'), 'scrub'),),
        routes=tuple((ident(source), ident(target)) for source, _, target in edges),
        assembly_names=('joining frame',), standing_kind='cleaning', standing_method='scrub',
        standing_participants=(ident(panel), ident('brush')), standing_place=ident('studio'))
        for actor, panel in zip(actors, ('panel-a', 'panel-b')))
    presentations = lambda keys: tuple(f.PublicEntityPresentation(entity_id=ident(k), name=k.replace('-', ' ').title(),
        description='Neutral declared ' + k + '.') for k in keys)
    return ActorFixture(campaign_id=campaign, player_entity_id=ident('visitor'), initial_state=movement,
        initial_object_open_states=(), initial_object_lit_states=lights,
        ambient_visual_conditions=ambient, ambient_visual_profile_version=ambient_version,
        place_presentations=presentations(places), object_presentations=presentations(objects), actor_presentations=presentations(actors),
        movement_routes=tuple(f.FixtureMovementRoute(source_place_id=ident(s), direction=d, destination_place_id=ident(t)) for s, d, t in edges),
        checkpoint_qualification={'qualification_id': 'astra:evidence:neutral-checkpoint', 'semantic_owner': 'AFQR-01',
            'qualified': True, 'provenance': 'neutral transfer test', 'fixture_campaign_id': campaign}, provenance=provenance,
        fixed_object_ids=(ident('bench'),), light_source_id=ident('signal'), storage_pairs=(), stock_world_routine=False,
        specialist_routes=('material', 'water', 'timed', 'actors'), material_profile=material,
        water_profile=water_profile, water_initial=initial,
        environment_profile=TimedEnvironmentProfile((ident('cloth'),), tuple((ident(p), Fraction(1, 2), 'exposed') for p in places),
            ((4, ident('studio'), Fraction(1, 4), 'sheltered'),)), assemblies=(assembly,),
        trace_subjects=(ident('panel-a'), ident('panel-b'), ident('cloth'), ident('plate')),
        actor_profiles=profiles, actor_order=order, actors_version='neutral-actors-1')


def changed(result):
    assert result.authoritative_changed, result.message
    return result


@pytest.mark.parametrize('reverse', [False, True])
@pytest.mark.parametrize('blocked_limit', [1, 3])
def test_fresh_configuration_transfers_contested_priority_policy_and_replay(tmp_path, reverse, blocked_limit):
    fixture = neutral_fixture(reverse=reverse, blocked_limit=blocked_limit)
    assert all('tarrow' not in entity.entity_id for entity in fixture.initial_state.representation.entities)
    a = ActorApplication.new(fixture=fixture, checkpoint_path=tmp_path/'neutral.json')
    winner, loser = fixture.actor_order
    changed(a.wait())
    assert placement(a.state.representation, ident('brush')).object_entity_id == winner
    assert len(participation.selected(a.participation_state, winner).contributions) == 1
    assert participation.selected(a.participation_state, loser).blocked_due == 1
    for _ in range(3): changed(a.wait())
    won = participation.selected(a.participation_state, winner)
    lost = participation.selected(a.participation_state, loser)
    assert won.status == 'completed' and len(won.contributions) == 3
    assert lost.status == 'withdrawn' and lost.blocked_due == blocked_limit
    winner_panel = won.participants[0]
    loser_panel = lost.participants[0]
    assert dict(a.water_state.adhered)[winner_panel] == 0
    assert dict(a.water_state.adhered)[loser_panel] == 3
    assert a.condition_events and dict(a.water_state.water)[ident('cloth')] == 0
    b = ActorApplication.restore(fixture=fixture, checkpoint_path=a.checkpoint_path)
    assert b.authoritative_digest() == a.authoritative_digest()
    assert b.evidence_state == a.evidence_state and b.participation_state == a.participation_state
    # Same actor goes from cleaning to a freshly declared reversible assembly.
    changed(b.move('east'))
    actor_name = fixture.entity_name(winner)
    changed(b.request_assembly(actor_name, 'joining frame'))
    b.advance_duration(kind='wait', steps=6)
    assert participation.selected(b.participation_state, winner).status == 'completed'
    assert len(b.connections) == 1
    connection = b.connections[0]
    assert (connection.left, connection.right, connection.fastener) == (ident('plate'), ident('peg'), ident('cord'))
    assert ActorApplication.restore(fixture=fixture, checkpoint_path=b.checkpoint_path).authoritative_digest() == b.authoritative_digest()
