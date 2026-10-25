"""Version-bound neutral investigation cases over existing actor/material/time owners.

This is a noncanonical fixture constructor. No generated fact is inserted into
memory or truth: prior history is obtained only through actual owner procedures.
"""
from fractions import Fraction
from dataclasses import replace

from astra_runtime import myravant_play_fixture as f
from astra_runtime.myravant_tarrow_actors import ActorFixture, ActorProfile
from astra_runtime.myravant_tarrow_time import AssemblyProfile
from astra_runtime.domain.persistent_world_material import MaterialEffect, MaterialProfile, digest, placement
from astra_runtime.domain.persistent_world_water_cleaning import WaterCleaningAsset, WaterCleaningProfile, WaterCleaningState
from astra_runtime.domain.persistent_world_timed_environment import TimedEnvironmentProfile

NEUTRAL_CASES = ('neutral-contended', 'neutral-reverse', 'neutral-relay')

def ident(key):
    return 'astra:entity:neutral-lab-' + key


def _build_neutral(*, reverse=False, blocked_limit=3, standing=True,
                   generated_case=None, generated_seed=0, generated_scale=0):
    """All scenario declarations are constructor inputs; no mutable runtime remap."""
    if generated_case is not None and generated_case not in {'access', 'resources', 'evidence'}:
        raise ValueError('unadmitted generated locality case')
    if (type(generated_scale) is not int or not 0 <= generated_scale <= 3
            or (generated_case is None and generated_scale)):
        raise ValueError('unsupported bounded generated locality scale')
    # Preserve every historical generated-worksite-1 identity at scale zero.
    token_parts = ['generated-worksite-1', generated_case, generated_seed]
    if generated_scale:
        token_parts.extend(('connected-scale-1', generated_scale))
    generated_token = (digest(token_parts)[:18] if generated_case is not None else None)
    wings = tuple(range(1, generated_scale + 1))
    uid = (ident if generated_token is None else
           lambda key: 'astra:entity:generated-worksite-' + generated_token + '-' + key)
    places = (('entry', 'studio', 'balcony') if generated_token is None else
              ('entry', 'studio', 'balcony', 'store')) + tuple(f'wing-{n}' for n in wings)
    wing_panels = tuple(f'wing-{n}-panel' for n in wings)
    wing_cloths = tuple(f'wing-{n}-cloth' for n in wings)
    wing_workers = tuple(f'wing-{n}-worker' for n in wings)
    objects = ('signal', 'brush', 'panel-a', 'panel-b', 'tray', 'cloth', 'plate', 'peg', 'cord', 'bench') + wing_panels + wing_cloths
    actors = ('jun', 'sol') + wing_workers
    edges = (('entry', 'east', 'studio'), ('studio', 'west', 'entry'),
             ('studio', 'north', 'balcony'), ('balcony', 'south', 'studio'),
             ('balcony', 'west', 'entry'), ('entry', 'north', 'balcony'))
    if generated_token is not None:
        edges = (*edges, ('entry', 'west', 'store'), ('store', 'east', 'entry'))
    # Every expansion remains one connected owner-owned representation and clock.
    # These are explicit bilateral routes, not invented teleport or catch-up law.
    wing_sources = ('studio', 'entry', 'store')
    wing_directions = (('east', 'west'), ('south', 'north'), ('west', 'east'))
    edges += tuple(edge for n in wings for edge in (
        (wing_sources[n-1], wing_directions[n-1][0], f'wing-{n}'),
        (f'wing-{n}', wing_directions[n-1][1], wing_sources[n-1])))
    order = tuple(uid(k) for k in (tuple(reversed(actors)) if reverse else actors))
    campaign = ('astra:campaign:neutral-investigation-' + digest([edges, order, blocked_limit, standing])[:18]
                if generated_token is None else
                'astra:campaign:generated-worksite-' + digest([generated_token, edges, order, standing])[:20])
    entities = tuple(f._entity(uid(k), kind) for keys, kind in (
        (places, 'place'), (objects, 'object'), ((*actors, 'visitor'), 'character_or_creature')) for k in keys)
    initial_places = {k: ('store' if generated_token is not None and k == 'tray'
                          else 'studio') for k in (*actors, *objects)}
    for n in wings:
        initial_places[f'wing-{n}-panel'] = f'wing-{n}'
        initial_places[f'wing-{n}-cloth'] = f'wing-{n}'
        initial_places[f'wing-{n}-worker'] = wing_sources[n-1]
    relations = tuple(f._located('neutral-' + k if generated_token is None else
                                  'generated-' + generated_token + '-' + k,
                                  uid(k), uid(place)) for k, place in (
        ('visitor', 'entry'), *initial_places.items()))
    rep = f.create_persistent_world_entity_location_representation(campaign_id=campaign, entities=entities, relations=relations)
    lights = (f.create_persistent_world_object_lit_state(object_entity_id=uid('signal'), state='unlit'),)
    movement = f.create_persistent_world_movement_runtime_state(representation=rep)
    custody = f.create_persistent_world_object_custody_runtime_state(movement_state=movement)
    opened = f.create_persistent_world_object_open_close_runtime_state(custody_state=custody, object_open_states=())
    lit = f.create_persistent_world_object_lit_runtime_state(open_close_state=opened, object_lit_states=lights)
    ambient = {uid(p): 'sufficient' for p in places}
    ambient_version = f.FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION
    provenance = f.FixtureProvenanceReceipt(
        fixture_id=('neutral-investigation-laboratory' if generated_token is None else 'neutral-generated-worksite'),
        fixture_version=('1' if generated_token is None else 'generated-worksite-1-' + generated_token),
        fixture_status=('development-test-only' if generated_token is None else 'noncanonical-development'),
        canon=False, default_world=False,
        origin_workstream=('PLAY-TARROW-INVESTIGATION-1' if generated_token is None else 'PLAY-TARROW-LOCALITY-GEN-1'),
        origin_merge_commit='0'*40,
        origin_merged_at=('2026-10-19' if generated_token is None else ''),
        g1_baseline_sha='0'*40,
        playable_need_refs=('configuration-transfer',), requirement_refs=('REQ-PROD-012',),
        direct_external_content_consulted_during_g1=False, originality_review_status='neutral-engineering-fixture',
        initial_state_digest=f.digest_persistent_world_entity_location_representation(rep),
        initial_world_state_digest=f.digest_persistent_world_composite_state(rep, ()),
        initial_object_lit_state_digest=f.digest_persistent_world_object_lit_states(lights),
        initial_int2_world_state_digest=f.digest_persistent_world_lit_composite_state(opened, lights),
        initial_int3_world_state_digest=f.digest_persistent_world_storage_composite_state(lit),
        ambient_visual_profile_version=ambient_version,
        ambient_visual_condition_digest=f.digest_fixture_ambient_visual_conditions(ambient))
    assets = tuple(WaterCleaningAsset(uid(k), kind, water, residue, rate) for k, kind, water, residue, rate in (
        ('brush', 'brush', 0, 8, 2), ('panel-a', 'surface', 0, 3, 0),
        ('panel-b', 'surface', 0, 3, 0), ('tray', 'tray', 0, 8, 0), ('cloth', 'absorbent', 2, 2, 1),
        *((key, 'surface', 0, 3, 0) for key in wing_panels),
        *((key, 'absorbent', 2, 2, 1) for key in wing_cloths)))
    pairs = tuple(('scrub', uid(k), uid('brush')) for k in ('panel-a', 'panel-b', *wing_panels)) + (('collect', uid('brush'), uid('tray')),)
    water_profile = WaterCleaningProfile(assets, pairs)
    cloth_ids = {uid(k) for k in ('cloth', *wing_cloths)}
    panel_ids = {uid(k) for k in ('panel-a', 'panel-b', *wing_panels)}
    initial = WaterCleaningState(tuple((a.id, 2 if a.id in cloth_ids else 0) for a in assets),
        tuple((a.id, 3 if a.id in panel_ids else 0) for a in assets), tuple((a.id, 0) for a in assets))
    material = MaterialProfile(uid('visitor'), tuple((uid(k), uid('bench')) for k in ('plate', 'peg')),
        ((uid('plate'), uid('peg'), uid('cord'), 'tie'),))
    if generated_case == 'access':
        material = replace(material, effects=(MaterialEffect(
            uid('studio'), 'north', 'movement',
            ((uid('plate'), uid('bench')), (uid('peg'), uid('bench'))),
            ((uid('plate'), uid('peg'), uid('cord'), 'tie'),)),))
    assembly = AssemblyProfile('joining frame', uid('studio'), uid('plate'), uid('peg'),
        uid('bench'), uid('bench'), uid('cord'), 'tie')
    profiles = tuple(ActorProfile(uid(actor), blocked_limit=blocked_limit, methods=('scrub',),
        cleaning_pairs=((uid(panel), uid('brush'), 'scrub'),),
        routes=tuple((uid(source), uid(target)) for source, _, target in edges),
        assembly_names=('joining frame',),
        standing_kind='cleaning' if standing and actor in {'jun', 'sol'} else None,
        standing_method='scrub' if standing and actor in {'jun', 'sol'} else None,
        standing_participants=(uid(panel), uid('brush')) if standing and actor in {'jun', 'sol'} else (),
        standing_place=uid('studio') if standing and actor in {'jun', 'sol'} else None)
        for actor, panel in zip(actors, ('panel-a', 'panel-b', *wing_panels)))
    place_names = {'entry': 'Entrance', 'studio': 'Workshop',
                   'balcony': 'Covered Yard', 'store': 'Store',
                   **{f'wing-{n}': f'Work Annex {n}' for n in wings}}
    presentations = lambda keys, place=False: tuple(f.PublicEntityPresentation(
        entity_id=uid(k),
        name=(place_names[k] if place and generated_token is not None
              else k.replace('-', ' ').title()),
        description='Neutral declared ' + k + '.') for k in keys)
    return ActorFixture(campaign_id=campaign, player_entity_id=uid('visitor'), initial_state=movement,
        initial_object_open_states=(), initial_object_lit_states=lights,
        ambient_visual_conditions=ambient, ambient_visual_profile_version=ambient_version,
        place_presentations=presentations(places, True), object_presentations=presentations(objects), actor_presentations=presentations(actors),
        movement_routes=tuple(f.FixtureMovementRoute(source_place_id=uid(s), direction=d, destination_place_id=uid(t)) for s, d, t in edges),
        checkpoint_qualification={'qualification_id': 'astra:evidence:neutral-checkpoint', 'semantic_owner': 'AFQR-01',
            'qualified': True, 'provenance': 'neutral transfer test', 'fixture_campaign_id': campaign}, provenance=provenance,
        fixed_object_ids=(uid('bench'),), light_source_id=uid('signal'), storage_pairs=(), stock_world_routine=False,
        specialist_routes=('material', 'water', 'timed', 'actors'), material_profile=material,
        water_profile=water_profile, water_initial=initial,
        environment_profile=TimedEnvironmentProfile(tuple(uid(x) for x in ('cloth', *wing_cloths)),
            tuple((uid(p), Fraction(1, 2), 'exposed') for p in places),
            ((4, uid('studio'), Fraction(1, 4), 'sheltered'),)), assemblies=(assembly,),
        trace_subjects=tuple(uid(x) for x in ('panel-a', 'panel-b', 'cloth', 'plate', *wing_panels, *wing_cloths)),
        actor_profiles=profiles, actor_order=order,
        actors_version=('investigation-neutral-1-' + ('relay' if not standing else 'reverse' if reverse else 'contended')
                        if generated_token is None else 'investigation-neutral-generated-1-' + generated_token))




def create_neutral_investigation_fixture(case='neutral-contended'):
    if type(case) is not str or case not in NEUTRAL_CASES:
        raise ValueError('unknown neutral investigation recipe')
    return _build_neutral(reverse=(case == 'neutral-reverse'),
                          blocked_limit=1 if case == 'neutral-reverse' else 3,
                          standing=(case != 'neutral-relay'))
