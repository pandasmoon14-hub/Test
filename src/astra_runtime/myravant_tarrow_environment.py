"""Environmental-depth scenario over existing place and asset procedures.

All new physical layout, contents and licenses are noncanonical development
realizations. Static descriptions never grant support, attachment, force,
wetness, repair, harvesting or hidden knowledge semantics.
"""
from dataclasses import replace

from astra_runtime.myravant_tarrow import (
    ACTIVITIES, EDGES, OBJECTS, PEOPLE, PLACES, Place, TarrowLayout,
    create_tarrow_fixture, execute_tarrow_request, identity,
)
from astra_runtime.myravant_terminal_capabilities import execute_bounded_terminal_request

# (position, area, name, description). Area is a presentation grouping only;
# current location and movement remain ordinary authoritative place state.
POSITIONS = (
    ("common-threshold", "common", "Common Threshold", "Scuffed boards cross the sheltered threshold. A shallow recess opens beside the public notice board; pale strips of wear mark the busiest footing."),
    ("notice-recess", "common", "Notice Recess", "Old fastening holes surround the notice board. A small document box sits beneath it, clear of the passage through the common."),
    ("common-shelf", "common", "Common Shelf", "A low shelf occupies the side recess. A loose cloth lies beside a pale, dust-edged outline on its surface."),
    ("yard-tools", "yard", "Yard Tool Station", "The red-bound coffer and long pry bar stand beside a scarred work trestle. The workroom entrance continues west, while the sorting bay opens to the north."),
    ("yard-sorting", "yard", "Yard Sorting Bay", "A warped sorting rack divides the bay from the tool station. A shallow lidded tray rests nearby; scrape marks overlap across the rack-facing boards."),
    ("yard-threshold", "yard", "Underbank Threshold", "The open yard narrows into a roofed walk. A stone edge and a worn side reveal the limited passage; the basket in the yard can obstruct this particular approach."),
    ("mark-position", "underbank", "Floodmark Position", "The floodmark post stands close to the damp wall. Higher scratches and dark bands are visible only when local light reaches them."),
    ("abutment-position", "underbank", "Abutment Position", "An exposed joint interrupts the streaked wall. Pale lines cross darker surface patches above the passage floor."),
    ("control-position", "deck", "Gate Control Position", "The crooked gate leaf stands beside a fixed control housing. A guide face shows rub marks, but the lifting connection disappears behind the housing."),
    ("deck-edge", "deck", "Deck Inspection Edge", "A fixed rail borders the exposed inspection edge. Moving water lies beyond, separated from the walking position by the rail and the deck edge."),
    ("guest-luggage", "guest", "Guest Belongings Bay", "A low bench stands beside an empty guest box. The shared bay leaves a clear passage between resting space and the common."),
    ("work-bench", "workshop", "Workroom Bench", "A fixed workbench occupies the recess, with a lidded parts tray and a loose wooden strip. Old scrape marks cross a visible repair patch on the work surface."),
    ("work-shelf", "workshop", "Workroom Shelf", "A fixed shelf carries scuffs and pale tool-shaped outlines. Some spaces between those outlines are empty."),
    ("north-staging", "north", "North Staging Edge", "A message rest and an empty delivery box mark a stopping position beside the maintained track. The route continues beyond the locality."),
    ("bank-edge", "bank", "Bank Observation Edge", "A darkened band crosses the exposed bank surface. The bank-side position overlooks moving water without extending into the channel."),
    ("reed-fringe", "reeds", "Reed Observation Fringe", "Rooted vegetation thickens along the wet margin. Small pieces of drift are caught between stems near the visible edge."),
)
POSITION_EDGES = (
    ("common", "east", "common-threshold"), ("common-threshold", "west", "common"),
    ("common-threshold", "east", "notice-recess"), ("notice-recess", "west", "common-threshold"),
    ("common-threshold", "north", "common-shelf"), ("common-shelf", "south", "common-threshold"),
    ("yard", "west", "yard-tools"), ("yard-tools", "east", "yard"),
    ("yard-tools", "west", "workshop"), ("workshop", "east", "yard-tools"),
    ("yard-tools", "north", "yard-sorting"), ("yard-sorting", "south", "yard-tools"),
    ("yard", "east", "yard-threshold"), ("yard-threshold", "west", "yard"),
    ("yard-threshold", "east", "underbank"), ("underbank", "west", "yard-threshold"),
    ("underbank", "east", "mark-position"), ("mark-position", "west", "underbank"),
    ("underbank", "south", "abutment-position"), ("abutment-position", "north", "underbank"),
    ("deck", "east", "control-position"), ("control-position", "west", "deck"),
    ("control-position", "south", "deck-edge"), ("deck-edge", "north", "control-position"),
    ("guest", "north", "guest-luggage"), ("guest-luggage", "south", "guest"),
    ("workshop", "west", "work-bench"), ("work-bench", "east", "workshop"),
    ("work-bench", "north", "work-shelf"), ("work-shelf", "south", "work-bench"),
    ("north", "east", "north-staging"), ("north-staging", "west", "north"),
    ("bank", "east", "bank-edge"), ("bank-edge", "west", "bank"),
    ("reeds", "north", "reed-fringe"), ("reed-fringe", "south", "reeds"),
)
FITTINGS = (
    ("threshold-frame", "Threshold Frame", "Fixed frame with a worn lower edge; opening or detaching it is not licensed.", "common-threshold"),
    ("notice-board", "Notice Board", "A fixed notice board with old fastening holes and differently weathered surface patches. No legible record text is presented here.", "notice-recess"),
    ("shelf-fitting", "Common Shelf Fitting", "A low fixed shelf with a worn front edge and a pale outline along its surface.", "common-shelf"),
    ("trestle", "Yard Work Trestle", "A fixed work trestle with overlapping scrape marks and a visibly patched surface.", "yard-tools"),
    ("threshold-stone", "Threshold Stone", "A fixed stone edge at the narrowing passage, with a worn side facing the open yard.", "yard-threshold"),
    ("abutment-joint", "Abutment Joint", "An exposed joint crossed by pale lines and darker surface streaks.", "abutment-position"),
    ("wall-streak", "Wall Streak", "A dark streak extends down the wall beside the joint. It records visible appearance rather than a current water measurement.", "abutment-position"),
    ("control-housing", "Control Housing", "A fixed housing beside the crooked gate. The lifting connection passes out of sight behind its exterior.", "control-position"),
    ("guide-face", "Gate Guide Face", "A visible guide surface bearing uneven rub marks beside the gate leaf.", "control-position"),
    ("edge-rail", "Deck Edge Rail", "A fixed rail along the inspection edge. Water is visible beyond the deck boundary.", "deck-edge"),
    ("guest-bench", "Guest Bench", "A low fixed bench with a polished front edge in the shared belongings bay.", "guest-luggage"),
    ("bench", "Workroom Bench Fitting", "A fixed workbench with old scrape marks crossing a visible repair patch.", "work-bench"),
    ("tool-shelf", "Tool Shelf", "A fixed shelf with tool-shaped outlines, small scuffs and empty spaces.", "work-shelf"),
    ("message-rest", "Message Rest", "A fixed stopping-place fitting beside the track, within reach of the delivery box.", "north-staging"),
    ("bank-mark", "Bank Water Mark", "A darkened band on the exposed bank surface beside the water.", "bank-edge"),
    ("reed-growth", "Rooted Reed Growth", "Rooted plants cluster at the wet margin, with narrow gaps between stems.", "reed-fringe"),
    ("snagged-drift", "Snagged Drift", "Small pieces of drift are caught among the rooted growth near the visible edge.", "reed-fringe"),
)
MATERIALS = (
    ("basket", "Delivery Basket", "A movable lidded delivery basket with worn sides and a close-fitting lid.", "yard"),
    ("sorting-tray", "Sorting Tray", "A shallow lidded sorting tray beside the rack, with a scuffed outer rim.", "yard-sorting"),
    ("parts-tray", "Parts Tray", "A movable lidded tray with worn edges and a fitted closure.", "work-bench"),
    ("document-box", "Document Box", "A small empty box beneath the public notice board.", "notice-recess"),
    ("guest-box", "Guest Box", "An empty box beside the shared guest bench.", "guest-luggage"),
    ("delivery-box", "Delivery Box", "An empty message box beside the track-side stopping position.", "north-staging"),
    ("cord", "Service Cord", "A loose length of service cord, gathered into a rough coil.", None),
    ("cloth", "Packing Cloth", "A folded piece of packing cloth with creased edges.", None),
    ("peg", "Wooden Peg", "A loose wooden peg with a plainly visible shaped end.", None),
    ("strip", "Wooden Strip", "A loose wooden strip resting near the parts tray.", "work-bench"),
    ("shelf-cloth", "Shelf Cloth", "A loose cloth lying beside the pale outline on the low shelf.", "common-shelf"),
)


def environment_layout():
    # Split coarse edges into explicit nearby positions without inventing a
    # metric, movement cost, body profile or new semantic location relation.
    replaced = {("yard", "west", "workshop"), ("workshop", "east", "yard"),
                ("yard", "east", "underbank"), ("underbank", "west", "yard")}
    edges = tuple(e for e in EDGES if e not in replaced) + POSITION_EDGES
    places = PLACES + tuple(Place(k, name, description, "local position", "noncanonical environmental development binding")
                            for k,area,name,description in POSITIONS)
    # Local route names aid discovery without granting remote interaction.
    names = {p.key:p.name for p in places}
    places = tuple(replace(p, description=p.description + (" Nearby positions: " + "; ".join(
        f"{names[b]} ({d})" for a,d,b in edges if a == p.key) + "." if any(a == p.key for a,d,b in edges) else "")) for p in places)
    relocations = {"coffer":"yard-tools", "bar":"yard-tools", "rack":"yard-sorting",
                   "post":"mark-position", "gate":"control-position"}
    objects = tuple((k,n,d,relocations.get(k,place)) for k,n,d,place in OBJECTS) + FITTINGS + MATERIALS
    containers = ("basket", "sorting-tray", "parts-tray", "document-box", "guest-box", "delivery-box")
    portable = ("lamp", "wedge", "slate", "folio", "cord", "cloth", "peg", "strip", "shelf-cloth")
    # The hidden blank deliberately has no new publicly discoverable route.
    base = TarrowLayout()
    routes = (
        ("basket", "yard", "west", "yard-tools", "push", "closed"),
        ("basket", "yard", "west", "yard-tools", "slide", "closed"),
        ("basket", "yard-tools", "east", "yard", "push", "closed"),
        ("basket", "yard-tools", "east", "yard", "slide", "closed"),
        ("parts-tray", "work-bench", "east", "workshop", "push", "closed"),
        ("parts-tray", "workshop", "west", "work-bench", "push", "closed"),
        ("sorting-tray", "yard-sorting", "south", "yard-tools", "slide", "closed"),
        ("sorting-tray", "yard-tools", "north", "yard-sorting", "slide", "closed"),
    )
    return replace(base, version="environment-1", places=places, objects=objects, edges=edges,
        fixed=base.fixed + tuple(k for k,_,_,_ in FITTINGS),
        contained=base.contained + (("cord","basket"), ("cloth","basket"), ("peg","parts-tray")),
        storage=base.storage + tuple((k,c) for c in containers for k in portable),
        open_states=base.open_states + tuple((c,"closed") for c in containers),
        dark=("underbank", "mark-position", "abutment-position"),
        displacement=routes, obstructions=(("yard","east","basket","yard"),),
        sightlines=tuple((a,d,b) for a,d,b in POSITION_EDGES),
        positions=tuple((k,area) for k,area,_,_ in POSITIONS),
        specialists=("physical_placement_goal",))


def create_environment_fixture():
    return create_tarrow_fixture(layout=environment_layout())


def execute_environment_request(application, raw_text):
    context = execute_tarrow_request(application, raw_text)
    if context is not None:
        return context
    return execute_bounded_terminal_request(application, raw_text)
