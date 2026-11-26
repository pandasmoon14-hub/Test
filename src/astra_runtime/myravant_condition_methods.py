"""Bind passage and construction questions to existing observations and actions."""

from dataclasses import dataclass
import re

from astra_runtime import myravant_actor_knowledge as knowledge
from astra_runtime.domain.persistent_world_actor_evidence import EvidenceState
from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_goal_methods import Step
from astra_runtime.myravant_input_context import reference


@dataclass(frozen=True)
class Subject:
    family: str
    assemblies: tuple
    label: str
    direction: str = ""
    destination: str = ""

    @property
    def assembly(self):
        return self.assemblies[0]

    @property
    def place(self):
        return self.assembly.place

    def word(self, value):
        if self.family == "access":
            return "closed" if value == "joined" else "open"
        return "fitted" if value == "joined" else "unfinished"


def bind_subjects(context, family, phrase, site):
    """Find only public, already known edges and locally visible assembly anchors."""
    app, fixture = context.app, context.fixture
    if not hasattr(app, "evidence_state"):
        return ()
    context.local_signs()
    places = context.destinations(site) if site else [context.here]
    if len(places) != 1:
        return ()
    here = places[0]
    assemblies = [a for a in fixture.assemblies
                  if a.place == here and a.support_left in fixture.fixed_object_ids
                  and a.support_right in {None, a.support_left}
                  and (site or app._visible(a.support_left))]
    if family == "work":
        term = reference(phrase)
        return tuple(Subject(family, (a,), a.name) for a in assemblies
                     if here == context.here and app._visible(a.left)
                     and (term == a.name or term == reference(fixture.entity_name(a.left))))
    target = re.fullmatch(r"(?:(north|south|west|east)(?:ward)? )?(?:passage|route|way|exit)", reference(phrase))
    if not target:
        return ()
    options = []
    for (place, direction), destination in context.routes.items():
        if place != here or (target[1] and target[1] != direction):
            continue
        effects = [e for e in fixture.material_profile.effects
                   if (e.source, e.direction, e.kind) == (place, direction, "movement")]
        bound = []
        for effect in effects:
            matching = tuple(a for a in assemblies if _explains(a, effect))
            if len(matching) == 1:
                bound.append(matching[0])
        if effects and len(bound) == len(effects):
            options.append(Subject(family, tuple(bound), direction + " passage", direction, destination))
    return tuple(options)


def _explains(assembly, effect):
    a = assembly
    supports = {(child, support) for child, support in
                ((a.left, a.support_left), (a.right, a.support_right)) if support}
    return (set(effect.supports) == supports
            and effect.connections == ((a.left, a.right, a.fastener, a.method),))


@dataclass(frozen=True)
class Account:
    event: object
    state: str


def _account(events, count):
    joined = [event for event in events if event.value[1] == "joined"]
    if joined:
        return Account(max(joined, key=lambda e: e.origin_tick if e.origin_tick is not None else e.tick), "joined")
    origins = {event.qualification.rsplit("|", 1)[-1] if event.kind == "reported" else event.receipt_id
               for event in events}
    if len(events) == count and len(origins) == 1:
        return Account(events[0], "separate")
    return None


def currently_observed(context, subject):
    observed = [knowledge.observed_assembly(context.app, context.fixture.player_entity_id, a, a.support_left)
                for a in subject.assemblies]
    if any(value and value[1] == "joined" for value in observed):
        return "joined"
    return "separate" if all(observed) else None


def player_witness(context, subject, new_events):
    observed = EvidenceState(new_events)
    events = [knowledge.report_source(observed, context.fixture.player_entity_id,
                                      a.left, "assembly", kind="witnessed",
                                      scope=(a.name, a.support_left, a.place)) for a in subject.assemblies]
    return _account(tuple(e for e in events if e is not None), len(events))


def player_reports(context, subject, speaker=None):
    reports = {}
    topics = {(a.left, a.name) for a in subject.assemblies}
    prefix = "qualified-local-delivery-at:" + subject.place + "|"
    for event in context.history.events("reported", "assembly"):
        if (event.qualification.startswith(prefix)
                and (event.target_id, event.value[0]) in topics
                and (speaker is None or event.source_actor_id == speaker)):
            reports.setdefault(event.source_actor_id, {})[(event.target_id, event.value[0])] = event
    accounts = tuple(_account(tuple(events.values()), len(topics)) for events in reports.values())
    return tuple(account for account in accounts if account is not None)


def observation_step(context, subject):
    return Step("inspect", (context.owner_reference(subject.assembly.left),))


def report_steps(context, subject, speaker):
    return tuple(Step("ask_report", (context.owner_reference(speaker, person=True),
                                     context.owner_reference(a.left), "assembly"),
                      keywords=(("kind", "witnessed"), ("assembly_scope", a.name)))
                 for a in subject.assemblies)


def continuation_step(context, subject, worker, protected):
    if subject.family == "access":
        if context.here != subject.place:
            raise ValueError("Go to the known inspection position before attempting that passage.")
        return Step("move", (subject.direction,), keywords=(("method", "walk"),),
                    destination=subject.destination)
    a = subject.assembly
    if protected:
        scoped = {a.left, a.right, a.fastener, a.support_left, a.support_right}
        if (protected in scoped or not context.app._visible(protected)
                or (placement(context.app.state.representation, protected).relation_type,
                    placement(context.app.state.representation, protected).object_entity_id)
                != ("located_at", context.here)):
            raise ValueError("I can't guarantee that placement with the assembly scope you selected.")
    return Step("request_assembly", (context.owner_reference(worker, person=True), a.name))
