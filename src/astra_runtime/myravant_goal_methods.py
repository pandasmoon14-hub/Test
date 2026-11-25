"""Describe bounded owner operations from a player's admitted local view."""

from dataclasses import dataclass
from math import ceil

from astra_runtime.domain.persistent_world_material import placement


@dataclass(frozen=True)
class Goal:
    family: str
    target: str
    recipient: str = ""
    exchange_place: str = ""


@dataclass(frozen=True)
class Step:
    owner: str
    args: tuple[str, ...]
    destination: str = ""
    keywords: tuple[tuple[str, object], ...] = ()

    def execute(self, app):
        return getattr(app, self.owner)(*self.args, **dict(self.keywords))


@dataclass(frozen=True)
class Method:
    key: tuple[str, ...]
    description: str
    step: Step
    terms: tuple[str, ...] = ()
    next_key: tuple[str, ...] = ()


@dataclass(frozen=True)
class Options:
    methods: tuple[Method, ...] = ()
    reason: str = ""
    complete: bool = False
    investigation: Method | None = None


def carrying(context, entity):
    return any(p.entity_id == entity for p in context.fixture.public_entities_carried_by(
        context.app.state.representation, context.fixture.player_entity_id))


def _handoff_receipt(context, goal):
    player = context.fixture.player_entity_id
    for entry in reversed(context.app.handoff_state.committed_actor_object_handoff_transitions):
        receipt = entry.receipt
        if (receipt.object_entity_id == goal.target
                and player in (receipt.source_actor_entity_id, receipt.recipient_actor_entity_id)):
            return (receipt.source_actor_entity_id, receipt.recipient_actor_entity_id) == (player, goal.recipient)
    return False


def return_options(context, goal, limits):
    name = context.fixture.entity_name
    target, person = goal.target, goal.recipient
    if not carrying(context, target):
        observed = context.app._public_observation_fact(target)
        seen_elsewhere = observed is not None and observed.carrier_name != name(person)
        if not seen_elsewhere and _handoff_receipt(context, goal):
            return Options(reason=f"Your latest recorded exchange of {name(target)} was handing it to {name(person)}.",
                           complete=True)
        return Options(reason=f"You need to recover {name(target)} first. Its current location is unconfirmed by this goal.")
    if person in context.local("person"):
        step = Step("give_object", (context.owner_reference(target), context.owner_reference(person, person=True)))
        return Options((Method(("handoff",), f"hand it to {name(person)} here", step, ("hand it over",)),))
    site = goal.exchange_place
    location = name(site)
    reason = (f"You still have {name(target)}. {name(person)} is absent from your local view. "
              f"{location} is the recorded exchange site and a place to start looking.")
    if context.here == site:
        return Options(reason=reason + " You have reached that site.")
    context.local_signs()
    route = context.shortest_route(site)
    if not isinstance(route, tuple) or not route:
        return Options(reason=reason + " A unique route there is unavailable from your known directions.")
    direction, destination = route[0]
    check = Method(("check",), f"check {location} along your known route",
                   Step("move", (direction,), destination), ("start there",))
    return Options(reason=reason, investigation=check)


def recovery_options(context, goal, limits):
    app, target = context.app, goal.target
    name = context.fixture.entity_name
    if carrying(context, target):
        return Options(reason=f"You already carry {name(target)}.", complete=True)
    if target not in context.local("thing"):
        return Options(reason="Its location is currently unconfirmed. Inspect a known place or ask a local witness.")
    relation = placement(app.state.representation, target)
    obj = context.owner_reference(target)
    if relation.relation_type == "contained_by":
        container = relation.object_entity_id
        fact = app._public_observation_fact(container)
        if fact is not None and fact.open_state == "open" and name(target) in fact.visible_contents:
            return Options((Method(("retrieve",), f"retrieve it from the open {name(container)}",
                                   Step("retrieve_object", (obj, context.owner_reference(container))),
                                   ("retrieve it myself", "retrieve it by hand")),))
    if relation.relation_type == "located_at" and target not in context.fixture.fixed_object_ids:
        return Options((Method(("pick up",), "pick it up directly here",
                               Step("pickup", (obj,)), ("take it yourself",)),))
    if relation.relation_type == "carried_by" and relation.object_entity_id in context.local("person"):
        person = relation.object_entity_id
        if limits.no_asking:
            return Options(reason="Your prohibition on asking rules out the visible holder. No direct recovery is available here.")
        step = Step("request_object_from_actor", (context.owner_reference(person, person=True), obj))
        return Options((Method(("ask",), f"ask {name(person)} to hand it over, if they agree", step,
                               ("ask the holder",)),))
    return Options(reason="The current public view offers no qualified recovery method.")


def _water_step(*args):
    return Step("water", args, keywords=(("amount", None),))


def cleaning_options(context, goal, limits):
    app = context.app
    profile = getattr(app, "water_profile", None)
    if profile is None:
        return Options(reason="This locality has no qualified cleaning method.")
    target = goal.target
    local = set(context.local("thing"))
    if target not in local or not app._visible(target):
        return Options(reason="The work surface is no longer observable here.")
    name = context.fixture.entity_name
    assets = {asset.id: asset for asset in profile.assets}
    water, residue = dict(app.water_state.water), dict(app.water_state.adhered)
    remaining = residue[target]
    if remaining == 0:
        return Options(reason=f"{name(target)} has no removable residue.", complete=True)
    methods, blocks = [], []
    visible_reachable = {obj for obj in local & assets.keys() if app._visible(obj)
                         and placement(app.state.representation, obj).relation_type
                         in {"located_at", "carried_by", "supported_by"}}
    if target not in visible_reachable:
        return Options(reason="The panel remains inaccessible for work.")
    if limits.reserve and limits.reserve[0] not in visible_reachable:
        return Options(reason="The reserve vessel is no longer observable and reachable.")
    if limits.reserve and water[limits.reserve[0]] < limits.reserve[1]:
        return Options(reason=f"The vessel is already below your reserve of {limits.reserve[1]} unit(s).")
    for verb, surface, tool in profile.allowed_pairs:
        if surface != target or verb not in {"wipe", "scrub"} or tool not in visible_reachable:
            continue
        # Preparation may pick up a loose visible tool. It never searches a holder,
        # lifts a fixed object, or takes a tool off another support as a shortcut.
        held = carrying(context, tool)
        if not held and (placement(app.state.representation, tool).relation_type != "located_at"
                         or tool in context.fixture.fixed_object_ids):
            continue
        asset = assets[tool]
        capacity = asset.residue_capacity - residue[tool]
        if capacity <= 0 or asset.transfer_rate <= 0:
            blocks.append(f"{name(tool)} has no free residue capacity")
            continue
        target_ref, tool_ref = (context.owner_reference(obj) for obj in (target, tool))
        prep = None if held else Step("pickup", (tool_ref,))
        amount = min(remaining, capacity)
        strokes = ceil(amount / asset.transfer_rate)
        scope = (f"up to {amount} of {remaining} residue unit(s) in {strokes} stroke(s)"
                 + (f", first pick up {name(tool)}" if prep else ""))
        description = f"{verb} with {name(tool)} ({scope})"
        base = (verb, tool)
        aliases = (verb, name(tool).casefold(), "brush" if verb == "scrub" else "cloth")
        if verb == "scrub" or water[tool] > 0:
            step = prep or _water_step(verb, target_ref, tool_ref)
            methods.append(Method(base, description + " with no new water draw", step, aliases))
            continue
        if limits.no_draw:
            blocks.append(f"{name(tool)} is dry and drawing more water is prohibited")
            continue
        for op, source, destination in profile.allowed_pairs:
            if op != "soak" or destination != tool or source not in visible_reachable or not water[source]:
                continue
            if source == limits.stop_vessel:
                blocks.append(f"Stop before using {name(source)}")
                continue
            if limits.reserve and source == limits.reserve[0] and water[source] <= limits.reserve[1]:
                blocks.append(f"Leave the reserve of {limits.reserve[1]} unit(s) in {name(source)}")
                continue
            step = prep or _water_step("soak", context.owner_reference(source), tool_ref)
            methods.append(Method((*base, source), description + f", draw one unit from {name(source)}",
                                  step, (*aliases, name(source).casefold()), base if prep is None else ()))
        if not any(method.key[:2] == base for method in methods):
            blocks.append(f"{name(tool)} needs a qualified water source")
    reason = f"{name(target)} still has {remaining} removable residue unit(s)."
    if blocks:
        reason += " " + ". ".join(dict.fromkeys(blocks)) + "."
    return Options(tuple(methods), reason)


METHODS = {"return": return_options, "recover": recovery_options, "clean": cleaning_options}
