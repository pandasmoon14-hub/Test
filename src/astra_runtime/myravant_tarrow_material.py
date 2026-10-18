"""Tarrow material preview: noncanonical arrangements within existing areas.

Source-backed identities remain inherited; new boards, cords and fittings are
explicit engineering bindings, not native canon or inferred service resources.
"""
from dataclasses import dataclass, replace
from astra_runtime.myravant_tarrow import TarrowFixture, create_tarrow_fixture, identity
from astra_runtime.myravant_tarrow_environment import environment_layout, execute_environment_request
from astra_runtime.domain.persistent_world_material import MaterialProfile, MaterialEffect, digest


@dataclass(frozen=True)
class MaterialFixture(TarrowFixture):
    material_profile: MaterialProfile | None = None

    @property
    def locality_help(self):
        return ('Material arrangements: put <object> on <surface>; lift <object> from <surface>; '
                'tie/fasten <left> to <right> using <fastener>; untie/unfasten <fastener>.\n'
                'Workshop: Repair Board and Repair Peg on Workroom Bench, joined using Repair Cord (tie).\n'
                'Passage: Barrier Board and Barrier Crossbar on Yard Work Trestle, joined using Barrier Cord (tie); blocks the sorting-bay passage.\n'
                'Screen: Screen Cloth on Document Box, joined to Notice Board using Screen Cord (tie); blocks the threshold sightline, not movement. Screen Tie (fasten) is an independent optional connection.\n'
                'Lift supported objects before carrying/storing them; disconnect attached components before moving them. '
                'Components and whole fasteners can be recovered. No force, load, cutting or repair is inferred.\n'+super().locality_help)


def material_layout():
    layout=environment_layout()
    additions=(
        ('repair-board','Repair Board','A loose board for the declared reversible workshop arrangement.','work-bench'),
        ('repair-peg','Repair Peg','A loose shaped piece for the declared workshop connection.','work-bench'),
        ('repair-cord','Repair Cord','A whole reusable tying cord.','work-bench'),
        ('barrier-board','Barrier Board','A loose barrier panel for the sorting-bay entrance.','yard-tools'),
        ('barrier-crossbar','Barrier Crossbar','A loose crossbar for the declared barrier connection.','yard-tools'),
        ('barrier-cord','Barrier Cord','A whole reusable tying cord for the barrier.','yard-tools'),
        ('screen-cloth','Screen Cloth','An opaque loose cloth for the declared removable screen.','notice-recess'),
        ('screen-cord','Screen Cord','A whole reusable tying cord for the screen.','notice-recess'),
        ('screen-tie','Screen Tie','A reusable fastening strap, distinct from a tying cord.','notice-recess'),
    )
    surfaces=('bench','trestle','document-box','tool-shelf','guest-bench')
    portable=tuple(k for k,_,_,_ in additions)+('cord','cloth','peg','strip','shelf-cloth','lamp','folio')
    supports=tuple((identity(k),identity(s)) for k in portable for s in surfaces)
    links=tuple(tuple(identity(k) for k in row[:3])+(row[3],) for row in (
        ('repair-board','repair-peg','repair-cord','tie'),
        ('barrier-board','barrier-crossbar','barrier-cord','tie'),
        ('screen-cloth','notice-board','screen-cord','tie'),
        ('screen-cloth','notice-board','screen-tie','fasten'),
    ))
    barrier_supports=((identity('barrier-board'),identity('trestle')),(identity('barrier-crossbar'),identity('trestle')))
    profile=MaterialProfile(actor_id=identity('wayfarer'),support_pairs=supports,fastening_pairs=links,effects=(
        MaterialEffect(identity('yard-tools'),'north','movement',barrier_supports,(links[1],)),
        MaterialEffect(identity('yard-sorting'),'south','movement',barrier_supports,(links[1],)),
        MaterialEffect(identity('common-threshold'),'east','sight',((identity('screen-cloth'),identity('document-box')),),(links[2],)),
    ))
    # Include every qualification/effect in the binding identity. V1/depth saves
    # remain separate and cannot silently acquire new relationships.
    from dataclasses import asdict
    version='material-1-'+digest(asdict(profile))[:16]
    containers=('coffer','basket','sorting-tray','parts-tray','document-box','guest-box','delivery-box')
    layout=replace(layout,version=version,objects=layout.objects+additions,
        storage=layout.storage+tuple((k,c) for k,_,_,_ in additions for c in containers),
        specialists=(*layout.specialists,'material'))
    return layout, profile


def create_material_fixture():
    layout, profile = material_layout()
    fixture=create_tarrow_fixture(layout=layout)
    result=MaterialFixture(**fixture.__dict__,material_profile=profile)
    profile.validate(result.initial_state.representation)
    return result


def execute_material_locality_request(application,raw):
    from astra_runtime.myravant_material_application import execute_material_request
    return execute_material_request(application,raw) or execute_environment_request(application,raw)
