"""Opt-in #559 profile: finite surface reservoirs and deliberate absorbent contact.

Neutral development objects and whole-unit rates are neither setting canon nor
universal hydrology. The old water/time/actor profiles are untouched.
"""
from dataclasses import asdict, dataclass, replace
from fractions import Fraction

from astra_runtime.domain.persistent_world_material import digest, MaterialEffect
from astra_runtime.domain.persistent_world_water_cleaning import (
    WaterCleaningAsset, WaterCleaningProfile, WaterCleaningState, validate,
    canonical_state,
)
from astra_runtime.domain.persistent_world_timed_environment import canonical_profile
from astra_runtime.myravant_tarrow import create_tarrow_fixture, identity
from astra_runtime.myravant_tarrow_water import water_layout, profile_payload
from astra_runtime.myravant_tarrow_actors import ActorFixture, create_actor_fixture
from astra_runtime.myravant_tarrow_time import AssemblyProfile


@dataclass(frozen=True)
class SurfaceFixture(ActorFixture):
    surface_policy: str = "deliberate-contact-whole-unit-1"

    @property
    def locality_help(self):
        return (
            "Surface liquids (noncanonical): pour <N> units from <carried vessel> onto "
            "<accessible surface>; scoop from <surface> into <carried vessel>; "
            "blot <surface> using <carried cloth/felt>; press <carried wet absorbent> "
            "against <accessible absorbent>; ask <willing actor> to blot "
            "<surface> using <tool>. Deliberate contact alone transfers water; "
            "moving, storage and mere adjacency do not. Partial scoop/blot/press "
            "is capacity/rate bounded; exact pours refuse overflow. Surface water "
            "does not evaporate, and no flooding, slipping or drinking is modeled.\n"
            + super().locality_help
        )


def create_surface_fixture(*, reverse_order=False, shared_workbench=False, structure_case=None):
    if type(shared_workbench) is not bool:
        raise ValueError("surface actor-position variant must be explicit")
    if type(reverse_order) is not bool:
        raise ValueError("surface actor-order variant must be explicit")
    if structure_case is not None and structure_case not in ('standard', 'cross-workshop'):
        raise ValueError('unqualified structures configuration')
    base = create_actor_fixture()
    layout, material, water_profile, initial = water_layout()
    felt = identity("packing-felt")
    surfaces = (identity("practice-panel"), identity("sorting-board"))
    cloth = identity("cleaning-cloth")
    vessels = (identity("wash-bucket"), identity("rinse-basin"), identity("pouring-jug"))
    supports = ("bench", "trestle", "document-box", "tool-shelf", "guest-bench")
    containers = ("coffer", "basket", "sorting-tray", "parts-tray",
                  "document-box", "guest-box", "delivery-box")

    assets = tuple(
        replace(a, water_capacity=(3 if a.id == surfaces[0] else 2),
                transfer_rate=Fraction(2))
        if a.id in surfaces else a for a in water_profile.assets
    ) + (WaterCleaningAsset(felt, "absorbent", 3, Fraction(2), Fraction(2)),)
    pairs = list(water_profile.allowed_pairs)
    pairs += [("spill", vessel, surface) for vessel in vessels for surface in surfaces]
    pairs += [("scoop", surface, vessel) for surface in surfaces for vessel in vessels]
    pairs += [("blot", surface, tool) for surface in surfaces for tool in (cloth, felt)]
    pairs += [("press", cloth, felt), ("press", felt, cloth)]
    pairs += [("wring", felt, vessel) for vessel in vessels]
    pairs += [("soak", vessel, felt) for vessel in vessels]
    pairs += [("rinse", felt, vessel) for vessel in vessels]
    pairs += [("collect", felt, identity("debris-tray"))]
    profile = WaterCleaningProfile(assets, tuple(pairs))
    water = WaterCleaningState(
        (*initial.water, (felt, 0)), (*initial.adhered, (felt, Fraction(0))),
        (*initial.suspended, (felt, Fraction(0)))
    )
    validate(water, profile)

    environment = replace(base.environment_profile,
                          absorbents=(*base.environment_profile.absorbents, felt))
    blot_pairs = tuple((s, t, "blot") for s in surfaces for t in (cloth, felt))
    actors = tuple(
        replace(p, methods=(*p.methods, "blot"),
                cleaning_pairs=(*p.cleaning_pairs, *blot_pairs),
                standing_kind=None, standing_method=None,
                standing_participants=(), standing_place=None)
        for p in base.actor_profiles
    )
    order = tuple(reversed(base.actor_order)) if reverse_order else base.actor_order
    material = replace(material, support_pairs=(
        *material.support_pairs, *((felt, identity(s)) for s in supports)
    ))
    layout = replace(
        layout,
        people=tuple((*row[:3],
                      "work-bench" if row[0] == "oren" else
                      ("work-bench" if shared_workbench else "yard-tools") if row[0] == "tali" else row[3])
                     for row in layout.people),
        objects=(*layout.objects,
                 ("packing-felt", "Packing Felt",
                  "One development absorbent with 3 retained-water units of capacity.",
                  "work-bench")),
        storage=(*layout.storage, *(( "packing-felt", c) for c in containers)),
        specialists=(*layout.specialists, "timed", "actors", "surface-water")
    )
    # Option A #561: reuse the exact surface-water and actor owner binding for
    # one NEW opt-in configuration only. Earlier surface roots are unchanged.
    assemblies = base.assemblies
    if structure_case is not None:
        # This NEW versioned preview retains the aired-to-sheltered schedule
        # at a later committed boundary, leaving genuine exposure contrast for
        # a constructed cover before the ambient change. Old profiles keep t12.
        environment = replace(environment, schedule=((24, identity('yard-tools'),
                                                       Fraction(1, 4), 'sheltered'),))
        panel, cord = identity('work-panel'), identity('work-cord')
        cover, cover_tie = identity('cover-cloth'), identity('cover-tie')
        crossbar, trestle = identity('barrier-crossbar'), identity('trestle')
        board, box = identity('notice-board'), identity('document-box')
        station = identity('yard-tools')
        barrier_link = (panel, crossbar, cord, 'tie')
        screen_link = (panel, board, cord, 'tie')
        cover_link = (cover, crossbar, cover_tie, 'tie')
        barrier_support = ((panel, trestle), (crossbar, trestle))
        barrier_routes = (('yard-tools', 'north'), ('yard-sorting', 'south')) if structure_case == 'standard' else (('yard-tools', 'west'), ('workshop', 'east'))
        material = replace(material,
            support_pairs=(*material.support_pairs, (panel, trestle), (panel, box), (cover, trestle)),
            fastening_pairs=(*material.fastening_pairs, barrier_link, screen_link, cover_link),
            effects=(*material.effects,
                *(MaterialEffect(identity(site), direction, 'movement', barrier_support, (barrier_link,)) for site, direction in barrier_routes),
                MaterialEffect(identity('common-threshold'), 'east', 'sight', ((panel, box),), (screen_link,))))
        assemblies = (*assemblies,
            AssemblyProfile('work partition', station, panel, crossbar, trestle, trestle, cord, 'tie'),
            AssemblyProfile('work screen', identity('notice-recess'), panel, board, box, None, cord, 'tie'),
            AssemblyProfile('drying cover', station, cover, crossbar, trestle, trestle, cover_tie, 'tie'))
        actors = tuple(replace(a, assembly_names=(*a.assembly_names, 'work partition', 'work screen', 'drying cover')) for a in actors)
        new_objects = (
            ('work-panel', 'Work Panel', 'A whole portable development panel with declared arrangement-specific effects.', 'yard-tools'),
            ('work-cord', 'Work Cord', 'A whole reusable cord for one connection at a time.', 'yard-tools'),
            ('cover-cloth', 'Cover Cloth', 'A separate whole opaque cloth for a qualified drying cover.', 'yard-tools'),
            ('cover-tie', 'Cover Tie', 'A whole reusable cover fastener.', 'yard-tools'))
        layout = replace(layout, objects=(*layout.objects, *new_objects),
            storage=(*layout.storage, *((row[0], destination) for row in new_objects for destination in containers)),
            specialists=(*layout.specialists, 'structures'))

    witness = {
        "old_water_root": layout.version, "material": asdict(material),
        "water": profile_payload(profile), "initial": canonical_state(water),
        "environment": canonical_profile(environment),
        "actors": [asdict(x) for x in actors], "order": order,
        "shared_workbench": shared_workbench, "people": layout.people,
        "assemblies": [asdict(x) for x in assemblies],
        "policy": "deliberate-contact-whole-unit-1"
    }
    if structure_case is not None:
        witness["structure_case"] = structure_case
    layout = replace(layout, version=("structures-1-" if structure_case is not None else "surface-water-1-")+digest(witness)[:16])
    root = create_tarrow_fixture(layout=layout)
    return SurfaceFixture(
        **root.__dict__, material_profile=material, water_profile=profile,
        water_initial=water, environment_profile=environment,
        assemblies=assemblies,
        trace_subjects=(*base.trace_subjects, felt),
        timing_version=base.timing_version,
        actor_profiles=actors, actor_order=order, actors_version="surface-actors-1"
    )
