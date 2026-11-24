"""Session-local references from signs, lawful sightings and the player's travel."""

from collections import deque
import re


def words(text):
    return " ".join(re.findall(r"[\w']+", text.casefold().replace("’", "'")))


def reference(text):
    return re.sub(r"^(?:the|a|an|my) ", "", words(text))


class InputContext:
    def __init__(self, application):
        self.app = application
        self.fixture = application.fixture
        self.aliases = dict(self.fixture.public_input_aliases)
        self.routes = {}
        self.seen = {}
        self.previous_place = None
        self.subject = None
        self.person = None
        self.tool = None
        self.work_target = None

    @property
    def here(self):
        return self.app.current_place_id()

    def names(self, entity):
        return (self.fixture.entity_name(entity), *self.aliases.get(entity, ()))

    def owner_reference(self, entity, *, person=False):
        """Preserve the grounded identity when a label collides elsewhere."""
        label = self.fixture.entity_name(entity).casefold()
        resolve = (self.fixture.resolve_actor_reference if person
                   else self.fixture.resolve_object_reference)
        try:
            if resolve(label) == entity:
                return label
        except ValueError:
            pass
        # The existing owner resolver accepts fixture identity suffixes. The
        # referent is already audience-qualified before reaching this method.
        return entity.rsplit(":", 1)[-1]

    def match(self, phrase, entries):
        term = reference(phrase)
        labels = [(entity, reference(label)) for entity in entries for label in self.names(entity)]
        full = list(dict.fromkeys(entity for entity, label in labels if term == label))
        if full:
            return full
        if len(term) < 2:
            return []
        return list(dict.fromkeys(
            entity for entity, label in labels
            if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", label)
        ))

    def local(self, kind):
        presentations = (self.fixture.actor_presentations if kind == "person"
                         else self.fixture.object_presentations)
        candidates = []
        for presentation in presentations:
            entity = presentation.entity_id
            fact = self.app._public_observation_fact(entity)
            material_visible = kind == "thing" and getattr(self.app, "_visible", lambda _: False)(entity)
            if fact is not None or material_visible:
                candidates.append(entity)
        if kind == "thing":
            # Carrying is independently public in the existing location view,
            # including possessions that are identifiable without visual access.
            carried = self.fixture.public_entities_carried_by(
                self.app.state.representation, self.fixture.player_entity_id)
            candidates.extend(p.entity_id for p in carried if p.entity_id not in candidates)
        return tuple(candidates)

    def note_view(self, view):
        for fact in getattr(view, "observation_facts", ()):
            if fact.entity_kind == "object":
                self.seen.setdefault(fact.entity_id, set()).add(view.place_id)
        direction = getattr(view, "direction", None)
        if direction is None or not hasattr(view, "target_place_id"):
            return
        for edge in self.fixture.movement_routes:
            if (edge.source_place_id, edge.direction, edge.destination_place_id) == (
                    view.source_place_id, direction, view.target_place_id):
                self.routes[(edge.source_place_id, direction)] = edge.destination_place_id
                break

    def note_movement(self, source, direction):
        if source == self.here:
            return
        self.previous_place = source
        if direction is not None:
            self.routes[(source, direction)] = self.here

    def local_signs(self):
        here = self.here
        if (self.fixture.ambient_visual_condition_for(here) != "sufficient"
                and not self.app._bounded_local_light_available()):
            return ()
        signs = set(self.fixture.signposted_routes)
        destinations = []
        for edge in self.fixture.movement_routes:
            key = (edge.source_place_id, edge.direction)
            if key[0] == here and key in signs:
                self.routes[key] = edge.destination_place_id
                destinations.append(edge.destination_place_id)
        return tuple(dict.fromkeys(destinations))

    def route_labels(self):
        labels = [self.fixture.entity_name(entity) for entity in self.local_signs()]
        return "Signs here point to " + ", ".join(labels) + "." if labels else ""

    def destinations(self, phrase):
        self.local_signs()
        term = reference(phrase)
        if term in {"back", "where i came from", "where we came from", "last room", "previous room"}:
            return [self.previous_place] if self.previous_place else []
        named = tuple(dict.fromkeys((self.here, *(place for place, _ in self.routes), *self.routes.values())))
        landmark = re.fullmatch(r"(?:room|place) (?:with|where i saw) (.+)", term)
        if landmark:
            objects = self.match(landmark[1], tuple(self.seen))
            return [place for place in named if any(place in self.seen[obj] for obj in objects)]
        return self.match(term, named)

    def shortest_route(self, target):
        """Return a unique shortest known path or signal a real choice."""
        start = self.here
        if target == start:
            return ()
        edges = {}
        for (source, direction), destination in self.routes.items():
            edges.setdefault(source, []).append((direction, destination))
        depth = {start: 0}
        paths = {start: [()]}
        queue = deque([start])
        while queue:
            place = queue.popleft()
            if target in depth and depth[place] >= depth[target]:
                break
            for direction, next_place in edges.get(place, ()):
                distance = depth[place] + 1
                if next_place not in depth:
                    depth[next_place] = distance
                    paths[next_place] = []
                    queue.append(next_place)
                if depth[next_place] == distance and len(paths[next_place]) < 2:
                    for path in paths[place]:
                        paths[next_place].append((*path, (direction, next_place)))
                        if len(paths[next_place]) == 2:
                            break
        known = paths.get(target, [])
        if len(known) > 1:
            return known
        return known[0] if known else None
