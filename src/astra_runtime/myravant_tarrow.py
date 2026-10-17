"""Source-backed Tarrow locality with explicit, noncanonical runtime bindings.

Named source facts are preserved; added room layout, actor starting positions and
object storage licenses are development configuration, not new setting canon.
No NPC behavior, knowledge, ownership or consent is inferred from presentation.
"""
from dataclasses import dataclass, asdict
import hashlib
import json

from astra_runtime import myravant_play_fixture as f
from astra_runtime.myravant_play_application import MyravantPlayApplication, PlayApplicationResult
from astra_runtime.domain.persistent_world_entity_location_representation import (
    create_carried_by_relation, create_contained_by_relation,
)
from astra_runtime.kernel.record_identity import build_record_id

VERSION = "1"
SOURCE_REFS = ("NCD-PROD-001", "NCD-CONT-367..381", "NCD-CONT-544..566",
               "NCD-PROD-002-G", "NCD-CONT-620..629", "NCD-LSW-REWORK-001")


def identity(key):
    return build_record_id("entity", "tarrow-" + key)


@dataclass(frozen=True)
class Place:
    key: str
    name: str
    description: str
    boundary: str
    source: str


# Boundary is authored access context, not an implemented property-right system.
PLACES = (
    Place("common", "Wayhouse Common", "A dry public room shelters travelers. Messages and crossing notices concern different responsibilities.", "public interior", "NCD-CONT-368"),
    Place("yard", "Service Yard", "The packed service yard links the common, underbank walk and weir deck. Shared tools and work must coexist.", "shared exterior", "NCD-CONT-369"),
    Place("underbank", "Underbank Walk", "A damp roofed maintenance walk. Its flood marks are evidence, not a guarantee of present conditions.", "service passage", "NCD-CONT-370"),
    Place("deck", "Weir Deck", "The exposed deck overlooks the obstructed east gate. Looking at the works does not establish their internal cause.", "public service exterior", "NCD-CONT-371"),
    Place("household", "Wayhouse Household", "Domestic work and care have their own space beyond the public common. Entry requires an arrangement not yet modeled.", "private interior; no admitted entry", "NCD-LSW-REWORK-001; development layout"),
    Place("guest", "Guest Shelter", "Sheltered stopping space adjoins the common. No bed reservation or personal-property permission is implied.", "public guest interior", "NCD-CONT-368; development layout"),
    Place("workshop", "Workshop Workroom", "A work surface and sorting rack support repair work. Tools, stock, expertise and permission are separate.", "shared work interior", "NCD-PROD-002-G; development layout"),
    Place("stores", "Service Stores", "Reserved and issued materials need custody records. The stores remain outside the current public entry contract.", "controlled interior; no admitted entry", "NCD-CONT-563; development layout"),
    Place("north", "North Track Approach", "The maintained northern approach leads toward the wayhouse; the wider route network continues beyond this local binding.", "public exterior", "NCD-CONT-545; development extent"),
    Place("east", "East Bank Track", "The eastward route exists beyond the crossing. The blocked connection does not grant passage.", "exterior; crossing not admitted", "NCD-CONT-546"),
    Place("bank", "Lower Channel Bank", "A bank-side vantage looks over moving water. A bank path does not license entering the channel.", "exterior bank", "NCD-CONT-547; development access"),
    Place("reeds", "Reed Margin", "Rooted vegetation occupies the wet edge. Observation does not establish harvest rights, yields or safe footing in the water.", "exterior habitat edge", "NCD-CONT-552; development access"),
)
PEOPLE = (
    ("mira", "Mira Venn", "House Steward; coordinates guest space and scoped notices.", "common"),
    ("rho", "Rho Pell", "Carekeeper; practical guest needs remain distinct from office authority.", "guest"),
    ("oren", "Oren Kesh", "Mechanist; expertise does not confer remote knowledge.", "workshop"),
    ("tali", "Tali Ren", "Workshop Apprentice and route-survey candidate.", "yard"),
    ("kera", "Kera Doss", "Stores Keeper; custody and issue authority do not establish ownership.", "yard"),
    ("iven", "Iven Saar", "Records Keeper; records require provenance and qualified interpretation.", "common"),
    ("nala", "Nala Vey", "Route Courier; carrying a message does not imply knowledge of its contents.", "north"),
)
OBJECTS = (
    ("lamp", "Shuttered Service Lamp", "A locality service lamp. Temporary emergency use does not transfer ownership.", "common"),
    ("coffer", "Red-Lashed Parts Coffer", "A red-bound coffer holds service materials. Emergency opening concerns crossing-related need.", "yard"),
    ("post", "Floodmark Post", "Fixed water-level marks and maintenance scratches. Observation and interpretation are separate.", "underbank"),
    ("bar", "Long Pry Bar", "A practical lever; possession alone supplies neither a qualified method nor success.", "yard"),
    ("blank", "Soft-Iron Pin Blank", "Unfinished service stock; not a finished replacement part.", None),
    ("wedge", "Oak Gate Wedge", "A service wedge; no automatic bracing effect is licensed.", None),
    ("slate", "Maintenance Slate", "A partial maintenance record. Reading and interpreting its contents are not yet admitted.", None),
    ("folio", "Weatherproof Field Folio", "Your personal folio; it has no automatic mapping or truth function.", None),
    ("rack", "Sorting Rack", "A fixed sorting rack. Its hidden spaces have no public search contract yet.", "yard"),
    ("gate", "East Gate", "The east gate is visibly crooked and obstructed. Its internal cause is not revealed here.", "deck"),
)
# First six edges are source topology; following edges are explicit development
# layout. Private rooms and the blocked east connection have NO traversal edge.
EDGES = (("common", "south", "yard"), ("yard", "north", "common"),
         ("yard", "east", "underbank"), ("underbank", "west", "yard"),
         ("yard", "south", "deck"), ("deck", "north", "yard"),
         ("common", "north", "north"), ("north", "south", "common"),
         ("common", "west", "guest"), ("guest", "east", "common"),
         ("yard", "west", "workshop"), ("workshop", "east", "yard"),
         ("deck", "south", "bank"), ("bank", "north", "deck"),
         ("bank", "west", "reeds"), ("reeds", "east", "bank"))
ACTIVITIES = (
    ("Traveler reception", "common / guest", "Mira and Rho", "lodging capacity, consent and guest arrangements are not executable yet"),
    ("Repair and tool stewardship", "yard / workshop", "Oren and Tali", "work, part fitting and gate repair require qualified contracts"),
    ("Stock issue and return", "yard / stores", "Kera", "reservations, ownership and stock quantities are not simulated yet"),
    ("Record and message handling", "common / northern approach", "Iven and Nala", "testimony, record access and courier schedules are not simulated yet"),
    ("Environmental inspection", "underbank / deck / bank", "no automatic assignee", "runoff, drift and harvesting do not advance automatically"),
)


class TarrowFixture(f.MyravantPlayFixture):
    @property
    def locality_help(self):
        return ("Tarrow Reach: look; inspect <visible name>; inspect self; go north/south/east/west; "
                "take/drop <object>; open/close <coffer>; light/extinguish <lamp>; "
                "put <object> in <coffer>; retrieve <object> from <coffer>; wait; save; exit.\n"
                "Use locality, community, or activities for public context. Exactly two supported "
                "steps may be joined with 'then'. Private access, gate repair, autonomous NPC "
                "routines, dialogue and posture for an unspecified body are not yet qualified.")


def create_tarrow_fixture():
    player = identity("wayfarer")
    binding = {"version": VERSION, "places": [asdict(p) for p in PLACES],
               "people": PEOPLE, "objects": OBJECTS, "edges": EDGES,
               "sources": SOURCE_REFS, "activities": ACTIVITIES,
               "fixed": ("post", "rack", "gate"),
               "storage": ("lamp", "blank", "wedge", "slate", "folio"),
               "initial_containment": (("wedge", "coffer"), ("slate", "coffer"), ("blank", "rack")),
               "initial_carry": ("folio", "wayfarer"), "initial_player_place": "common",
               "dark": ("underbank",), "stock_world_routine": False, "specialist_routes": ()}
    binding_digest = hashlib.sha256(json.dumps(binding, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    campaign = build_record_id("campaign", "tarrow-locality-v" + VERSION + "-" + binding_digest[:20])
    presentations = lambda rows: tuple(f.PublicEntityPresentation(entity_id=identity(r[0]), name=r[1], description=r[2]) for r in rows)
    places = presentations(tuple((p.key, p.name, p.description) for p in PLACES))
    objects = presentations(OBJECTS)
    actors = presentations(PEOPLE)
    entities = tuple(f._entity(p.entity_id, kind) for rows, kind in (
        (places, "place"), (objects, "object"), (actors, "character_or_creature")) for p in rows) + (f._entity(player, "character_or_creature"),)
    relations = [f._located("tarrow-player", player, identity("common"))]
    relations += [f._located("tarrow-place-" + key, identity(key), identity(place)) for key, _, _, place in OBJECTS + PEOPLE if place]
    for key, container in (("wedge", "coffer"), ("slate", "coffer"), ("blank", "rack")):
        relations.append(create_contained_by_relation(relation_id=build_record_id("relation", "tarrow-contained-" + key), subject_entity_id=identity(key), object_entity_id=identity(container)))
    relations.append(create_carried_by_relation(relation_id=build_record_id("relation", "tarrow-folio"), subject_entity_id=identity("folio"), object_entity_id=player))
    rep = f.create_persistent_world_entity_location_representation(campaign_id=campaign, entities=entities, relations=tuple(relations))
    opens = (f.create_persistent_world_object_open_state(object_entity_id=identity("coffer"), state="closed"),)
    lights = (f.create_persistent_world_object_lit_state(object_entity_id=identity("lamp"), state="unlit"),)
    custody = f.create_persistent_world_object_custody_runtime_state(movement_state=f.create_persistent_world_movement_runtime_state(representation=rep))
    opened = f.create_persistent_world_object_open_close_runtime_state(custody_state=custody, object_open_states=opens)
    lit = f.create_persistent_world_object_lit_runtime_state(open_close_state=opened, object_lit_states=lights)
    ambient = {p.entity_id: "insufficient" if p.entity_id == identity("underbank") else "sufficient" for p in places}
    provenance = f.FixtureProvenanceReceipt(
        fixture_id="myravant-tarrow-locality", fixture_version=VERSION,
        fixture_status="canon_sources_with_development_bindings", canon=False, default_world=False,
        origin_workstream="PLAY-TARROW-REACH-1", origin_merge_commit="163721ca06ec4c6df2618f96520ea8ab3a4a9d1e",
        origin_merged_at="2026-10-17", g1_baseline_sha="163721ca06ec4c6df2618f96520ea8ab3a4a9d1e",
        playable_need_refs=SOURCE_REFS, requirement_refs=("REQ-PROD-002", "REQ-PROD-012", "REQ-PROD-013"),
        direct_external_content_consulted_during_g1=False, originality_review_status="native_sources_explicit_development_layout",
        initial_state_digest=f.digest_persistent_world_entity_location_representation(rep),
        initial_world_state_digest=f.digest_persistent_world_composite_state(rep, opens),
        initial_object_lit_state_digest=f.digest_persistent_world_object_lit_states(lights),
        initial_int2_world_state_digest=f.digest_persistent_world_lit_composite_state(opened, lights),
        initial_int3_world_state_digest=f.digest_persistent_world_storage_composite_state(lit),
        ambient_visual_profile_version=f.FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION,
        ambient_visual_condition_digest=f.digest_fixture_ambient_visual_conditions(ambient),
    )
    return TarrowFixture(
        campaign_id=campaign, player_entity_id=player, initial_state=custody.movement_state,
        initial_object_open_states=opens, initial_object_lit_states=lights,
        ambient_visual_conditions=ambient, ambient_visual_profile_version=f.FIXTURE_AMBIENT_VISUAL_PROFILE_VERSION,
        place_presentations=places, object_presentations=objects, actor_presentations=actors,
        movement_routes=tuple(f.FixtureMovementRoute(source_place_id=identity(a), direction=d, destination_place_id=identity(b)) for a,d,b in EDGES),
        checkpoint_qualification={"qualification_id": build_record_id("evidence", "tarrow-checkpoint-v" + VERSION), "semantic_owner": "AFQR-01", "qualified": True, "provenance": "owner-approved Tarrow development binding", "fixture_campaign_id": campaign},
        provenance=provenance, fixed_object_ids=tuple(identity(k) for k in ("post", "rack", "gate")),
        light_source_id=identity("lamp"), stock_world_routine=False, specialist_routes=(),
        storage_pairs=tuple((identity(k), identity("coffer")) for k in ("lamp", "blank", "wedge", "slate", "folio")),
    )


def execute_tarrow_request(application: MyravantPlayApplication, raw_text: str):
    query = " ".join(raw_text.casefold().strip().split())
    if query not in {"locality", "community", "activities"}:
        return None
    if query == "locality":
        text = ("Tarrow Weir lies within Tarrow Reach. Public routes connect the common, yard, underbank and deck "
                "with this development binding's guest shelter, workroom, northern approach and bank edge. "
                "The east crossing is blocked; household and stores entry require contracts not yet admitted. "
                "Room layout and starting positions are development configuration, not additional canon.")
    elif query == "community":
        text = "\n".join(name + ": " + role for _, name, role, _ in PEOPLE)
        text += "\nThese public roles do not establish current location, private knowledge, consent or autonomous schedules."
    else:
        text = "\n".join(f"{name}: {place}; {people}. Pending: {limit}." for name,place,people,limit in ACTIVITIES)
    digest = application.authoritative_digest()
    return "locality_context", PlayApplicationResult(result_type="locality_context", message=text, authoritative_changed=False, pre_state_digest=digest, post_state_digest=digest)
