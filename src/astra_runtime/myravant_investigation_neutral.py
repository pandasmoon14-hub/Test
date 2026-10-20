"""Version-bound neutral investigation cases over existing actor/material/time owners.

This is a noncanonical fixture constructor. No generated fact is inserted into
memory or truth: prior history is obtained only through actual owner procedures.
"""
from fractions import Fraction

from astra_runtime import myravant_play_fixture as f
from astra_runtime.myravant_tarrow_actors import ActorFixture, ActorProfile
from astra_runtime.myravant_tarrow_time import AssemblyProfile
from astra_runtime.domain.persistent_world_material import MaterialProfile, digest, placement
from astra_runtime.domain.persistent_world_water_cleaning import WaterCleaningAsset, WaterCleaningProfile, WaterCleaningState
from astra_runtime.domain.persistent_world_timed_environment import TimedEnvironmentProfile

NEUTRAL_CASES = ('neutral-contended', 'neutral-reverse', 'neutral-relay')

def ident(key):
    return 'astra:entity:neutral-lab-' + key


def _build_neutral(*, reverse=False, blocked_limit=3, standing=True):
    """All scenario declarations are constructor inputs; no mutable runtime remap."""
    places = ('entry', 'studio', 'balcony')
    objects = ('signal', 'brush', 'panel-a', 'panel-b', 'tray', 'cloth', 'plate', 'peg', 'cord', 'bench')
    actors = ('jun', 'sol')
    edges = (('entry', 'east', 'studio'), ('studio', 'west', 'entry'),
             ('studio', 'north', 'balcony'), ('balcony', 'south', 'studio'),
             ('balcony', 'west', 'entry'), ('entry', 'north', 'balcony'))
    order = tuple(ident(k) for k in (tuple(reversed(actors)) if reverse else actors))
    campaign = 'astra:campaign:neutral-investigation-' + digest([edges, order, blocked_limit, standing])[:18]
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
        fixture_id='neutral-investigation-laboratory', fixture_version='1', fixture_status='development-test-only',
        canon=False, default_world=False, origin_workstream='PLAY-TARROW-INVESTIGATION-1',
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
        assembly_names=('joining frame',), standing_kind='cleaning' if standing else None, standing_method='scrub' if standing else None,
        standing_participants=(ident(panel), ident('brush')) if standing else (), standing_place=ident('studio') if standing else None)
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
        actor_profiles=profiles, actor_order=order, actors_version='investigation-neutral-1-' + ('relay' if not standing else 'reverse' if reverse else 'contended'))




def create_neutral_investigation_fixture(case='neutral-contended'):
    if type(case) is not str or case not in NEUTRAL_CASES:
        raise ValueError('unknown neutral investigation recipe')
    return _build_neutral(reverse=(case == 'neutral-reverse'),
                          blocked_limit=1 if case == 'neutral-reverse' else 3,
                          standing=(case != 'neutral-relay'))
