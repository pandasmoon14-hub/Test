"""Player-facing projections of existing, attributed records."""

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class RememberedPlacement:
    entity: str
    place: str
    source: str
    tick: int


class ExperiencedReferences:
    def __init__(self, app):
        self.app = app
        self.player = app.fixture.player_entity_id

    def movement(self):
        return (entry.receipt for entry in self.app.state.committed_transitions
                if entry.receipt.actor_entity_id == self.player)

    def events(self, kind, facet=None):
        state = getattr(self.app, "evidence_state", None)
        return (event for event in getattr(state, "events", ())
                if (event.actor_id, event.kind) == (self.player, kind)
                and (facet is None or facet == event.facet))

    def placements(self, kind):
        events = tuple(self.events(kind, "placement"))
        groups = defaultdict(dict)
        if kind == "witnessed":
            for event in events:
                groups[event.receipt_id][event.target_id] = event.value
        for event in events:
            relation, target = event.value
            seen = {event.target_id}
            while (relation in {"supported_by", "contained_by"} and target not in seen
                   and target in groups.get(event.receipt_id, {})):
                seen.add(target)
                relation, target = groups[event.receipt_id][target]
            if relation == "located_at":
                tick = event.tick if event.origin_tick is None else event.origin_tick
                yield RememberedPlacement(event.target_id, target, event.source_actor_id, tick)

    def exchanges(self, direction):
        incoming = direction == "received"
        receipts = self.app.handoff_state.committed_actor_object_handoff_transitions
        for entry in receipts:
            receipt = entry.receipt
            source, recipient = receipt.source_actor_entity_id, receipt.recipient_actor_entity_id
            if (recipient if incoming else source) == self.player:
                yield receipt.object_entity_id, source if incoming else recipient, receipt.place_id

    def used_tool(self):
        performed = {event.receipt_id for event in self.events("performed", "activity")
                     if event.value == "water"}
        for command in reversed(getattr(self.app, "journal", ())):
            args = command["args"]
            if (command["method"] == "water" and len(args) == 3 and args[0] in {"wipe", "scrub"}
                    and command["result"]["receipt_id"] in performed):
                return self.app.fixture.resolve_object_reference(args[2])
        return None
