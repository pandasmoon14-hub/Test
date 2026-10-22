"""Opt-in noncanonical #555 Tarrow transformation development fixture."""
from dataclasses import asdict, dataclass, replace
import re

from astra_runtime.myravant_tarrow import create_tarrow_fixture, identity
from astra_runtime.myravant_tarrow_water import water_layout
from astra_runtime.myravant_tarrow_actors import ActorFixture, create_actor_fixture, execute_actor_locality_request
from astra_runtime.myravant_tarrow_time import AssemblyProfile
from astra_runtime.domain.persistent_world_material import MaterialEffect, digest
from astra_runtime.domain.persistent_world_material import TransformationProfile, validate_profile


@dataclass(frozen=True)
class TransformationFixture(ActorFixture):
    transformation_profile: TransformationProfile | None = None
    transformation_actor_methods: tuple[tuple[str, tuple[str, ...]], ...] = ()

    @property
    def locality_help(self):
        return ("Transformation: start refitting <component> using <tool>; "
                "start replacing <component> with <spare>; "
                "start repurposing <component> using <tool>; "
                "ask <actor> to refit/replace/repurpose <component> using/with <resource>; "
                "work transformation; pause/resume/abandon transformation; inspect transformation. "
                "Refit and replace take two work intervals; repurpose takes one. "
                "An agreement reserves no stock, and no arbitrary repair is implied.\n"
                + super().locality_help)


def create_transformation_fixture(*, actor_order=None, spare_at="yard-tools", tool_at="yard-tools"):
    if spare_at not in {"yard-tools", "work-bench"} or tool_at not in {"yard-tools", "work-bench"}:
        raise ValueError("unsupported transformation fixture placement")
    base = create_actor_fixture()
    layout, material, _, _ = water_layout()
    additions = (
        ("barrier-spare","Barrier Spare","A declared matching whole crossbar, never free output.",spare_at),
        ("alignment-tool","Alignment Tool","A qualified hand tool for bounded component fitting.",tool_at),
    )
    layout = replace(layout,
        people=tuple((*row[:3], "work-bench" if row[0] == "oren" else
                      "yard-tools" if row[0] == "tali" else row[3]) for row in layout.people),
        objects=(*layout.objects,*additions),
        storage=(*layout.storage,*tuple((k,c) for k,_,_,_ in additions
            for c in ("coffer","basket","sorting-tray","parts-tray","document-box","guest-box","delivery-box"))),
        specialists=(*layout.specialists,"timed","actors","transformation"))
    p=TransformationProfile(identity("barrier-crossbar"),identity("barrier-spare"),
        identity("alignment-tool"),identity("barrier-board"),identity("trestle"),
        identity("repair-board"),identity("repair-cord"),identity("yard-tools"),
        identity("work-bench"))
    new_links=((p.barrier_board,p.spare,identity("barrier-cord"),"tie"),
               (p.repair_board,p.old,p.repair_cord,"tie"))
    new_effects=(
        MaterialEffect(p.barrier_place,"north","movement",
            ((p.barrier_board,p.trestle),(p.spare,p.trestle)),(new_links[0],)),
        MaterialEffect(identity("yard-sorting"),"south","movement",
            ((p.barrier_board,p.trestle),(p.spare,p.trestle)),(new_links[0],)))
    surfaces=("bench","trestle","document-box","tool-shelf","guest-bench")
    material=replace(material,
        support_pairs=(*material.support_pairs,
                       *((p.spare,identity(s)) for s in surfaces),
                       *((p.tool,identity(s)) for s in surfaces)),
        fastening_pairs=(*material.fastening_pairs,*new_links),
        effects=(*material.effects,*new_effects))
    profiles=tuple(replace(a,standing_kind=None,standing_method=None,
                           standing_participants=(),standing_place=None,
                           assembly_names=(*a.assembly_names,"restored barrier"))
                   for a in base.actor_profiles)
    order=base.actor_order if actor_order is None else actor_order
    if type(order) is not tuple or len(order)!=len(profiles) or set(order)!={a.actor_id for a in profiles}:
        raise ValueError("invalid declared actor order")
    actor_methods=((identity("tali"),("refit","replace")),(identity("oren"),("repurpose",)))
    assemblies=(*base.assemblies,AssemblyProfile("restored barrier",p.barrier_place,
                    p.barrier_board,p.spare,p.trestle,p.trestle,identity("barrier-cord"),"tie"))
    witness={"profile":asdict(p),"material":asdict(material),
             "actors":[asdict(a) for a in profiles],"order":order,
             "assemblies":[asdict(a) for a in assemblies],
             "placements":(spare_at,tool_at),"actor_methods":actor_methods,"parent":base.provenance.initial_state_digest}
    layout=replace(layout,version="transformation-1-"+digest(witness)[:16])
    root=create_tarrow_fixture(layout=layout)
    validate_profile(p,root.initial_state.representation,material)
    return TransformationFixture(**root.__dict__,material_profile=material,
        water_profile=base.water_profile,water_initial=base.water_initial,
        environment_profile=base.environment_profile,assemblies=assemblies,
        trace_subjects=base.trace_subjects,timing_version="transformation-time-1",
        actor_profiles=profiles,actor_order=order,
        actors_version="transformation-actor-1-"+digest(witness)[:16],
        transformation_profile=p,transformation_actor_methods=actor_methods)


def parse_transformation_request(raw):
    text=" ".join(raw.strip().casefold().split())
    m=re.fullmatch(r"start (refitting|replacing|repurposing) (.+?) (using|with) (.+)",text)
    if m:
        return "begin",({"refitting":"refit","replacing":"replace","repurposing":"repurpose"}[m[1]],m[2],m[4],None)
    m=re.fullmatch(r"ask (.+?) to (pause|resume|abandon) transformation",text)
    if m:return "control",(m[2],m[1])
    m=re.fullmatch(r"ask (.+?) to (refit|replace|repurpose) (.+?) (using|with) (.+)",text)
    if m:return "begin",(m[2],m[3],m[5],m[1])
    if text=="work transformation":return "work",()
    if text in {"pause transformation","resume transformation","abandon transformation"}:
        return "control",(text.split()[0],)
    if text=="inspect transformation":return "status",()
    return None


def execute_transformation_request(app,raw):
    parsed=parse_transformation_request(raw)
    if parsed is None:return execute_actor_locality_request(app,raw)
    kind,args=parsed
    result=(app.begin_transformation(*args) if kind=="begin" else
            app.contribute_transformation() if kind=="work" else
            app.control_transformation(*args) if kind=="control" else
            app.transformation_status())
    return "transformation",result
