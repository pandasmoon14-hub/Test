"""Interpret terminal utterances into proposals over existing owner operations."""

from dataclasses import asdict, dataclass, replace
import json
import re

from astra_runtime.myravant_input_context import InputContext, reference, words
from astra_runtime.myravant_play_application import PlayApplicationResult


@dataclass(frozen=True)
class Intent:
    action: str
    target: str = ""
    method: str = ""
    instrument: str = ""
    person: str = ""
    facet: str = ""
    value: str = ""
    speech: str = "attempt"
    constraint: str = ""

    def trace_argument(self, ordinal, count):
        fields = {key: value for key, value in asdict(self).items() if value}
        if count > 1:
            fields["order"] = [ordinal, count]
        return json.dumps(fields, ensure_ascii=False, sort_keys=True)


# Each family parses roles independently of fixture names. Canonical requests
# still use the installed router, and grounded proposals call the same owners.
_MOVEMENT = {"go": "walk", "walk": "walk", "head": "walk", "return": "walk",
             "get": "walk", "make my way": "walk", "crawl": "crawl",
             "run": "run", "sprint": "run", "sneak": "sneak"}
_OBJECT_ACTIONS = {
    "take": "pickup", "pick up": "pickup", "grab": "pickup",
    "drop": "drop", "set down": "drop", "inspect": "inspect", "examine": "inspect",
    "check": "inspect", "look at": "inspect", "look closely at": "inspect",
    "open": "open", "unlatch": "open", "close": "close", "shut": "close",
    "untie": "untie", "unfasten": "untie",
}
_CLEANING = {"clean": "", "wash": "wash", "wipe": "wipe", "scrub": "scrub", "brush": "scrub"}
_CONDITIONS = {"wet": ("moisture", "wet"), "damp": ("moisture", "wet"),
               "dry": ("moisture", "dry"), "clean": ("residue", "clear"),
               "clear": ("residue", "clear"), "dirty": ("residue", "present"),
               "sooty": ("residue", "present")}
_PRONOUNS = {"it", "that", "this", "that one", "this one", "them"}
_PEOPLE = {"him", "her", "them", "they", "he", "she", "that person"}
_TOOL_RECALL = {"what i used earlier", "same tool"}
_POLITE = re.compile(
    r"^(?:please |i (?:want to|would like to|will|should) |i(?:'ll|'d like to) |let me )")
_QUESTION = re.compile(r"^(?:can|could|may|should|would|does|did|do|is|was|are|were|what|which|where|how|who)\b")
_CONSTRAINT = re.compile(r"\s+(without .+|only if .+|while .+|unless .+|quietly|carefully)$")
_UNSAFE = re.compile(r"^(?:do not|don't|never|no need to|imagine|suppose|if|what if|i wonder)\b")


def _head_rule(verbs):
    options = "|".join(re.escape(verb) for verb in sorted(verbs, key=len, reverse=True))
    return re.compile(rf"({options}) (.+)")


_TRAVEL = _head_rule(_MOVEMENT)
_PHYSICAL = _head_rule(_OBJECT_ACTIONS)
_CLEAN = _head_rule(_CLEANING)
_INSTRUMENT = re.compile(r"(.+?) (?:with|using) (.+)")
_WITNESS_END = r"(?: when (?:he|she|they|you) saw (?:it|that))?"
_CONDITION_WORD = "|".join(_CONDITIONS)
_TESTIMONY = re.compile(
    rf"ask (.+?) (?:if|whether) (.+?) (?:was|is|looked) ({_CONDITION_WORD}){_WITNESS_END}")
_DIRECT_TESTIMONY = re.compile(rf"did (.+?) (?:see|notice|find) (.+?) ({_CONDITION_WORD})")
_STATEMENT = re.compile(rf"tell (.+?) that (.+?) (?:is|was|looks) ({_CONDITION_WORD})")
_WITNESS_TOPIC = re.compile(r"ask (.+?) what (?:he|she|they|you) (?:saw|noticed|observed)(?: about (.+))?")
_REPORT_TOPIC = re.compile(r"ask (.+?) about (.+?) (moisture|residue|placement|assembly|trace|activity)")
_ORDERED = re.compile(r" (?:then|and(?: then)?) (?=(?:ask|tell|check|inspect|look at|take|pick up|drop|use|wipe|scrub|clean|go|head|return|open|close) )")


def _cleaning(text, person=""):
    action = "work" if person else "clean"
    use = re.fullmatch(r"use (.+?) on (.+)", text)
    if use:
        return Intent(action, target=use[2], instrument=use[1], person=person)
    method_suffix = re.fullmatch(r"(.+) by (wiping|scrubbing)", text)
    match = _CLEAN.fullmatch(method_suffix[1] if method_suffix else text)
    if not match:
        return None
    verb, target = match.groups()
    instrument = _INSTRUMENT.fullmatch(target)
    if instrument:
        target, tool = instrument.groups()
    else:
        tool = ""
    method = _CLEANING[verb]
    if method_suffix:
        suffix = {"wiping": "wipe", "scrubbing": "scrub"}[method_suffix[2]]
        method = method if method not in {"", suffix} else suffix
        if method != suffix:
            return Intent(action, target, method, tool, person, constraint=method_suffix[2])
    return Intent(action, target, method, tool, person)


def _proposal(text):
    constraint = _CONSTRAINT.search(text)
    if constraint:
        proposal = _unqualified_proposal(text[:constraint.start()])
        return replace(proposal, constraint=constraint[1]) if proposal else None
    return _unqualified_proposal(text)


def _unqualified_proposal(text):
    if re.fullmatch(r"(?:which way|how (?:do|can) i (?:get|go)) back", text):
        return Intent("travel", "back", speech="inquiry")
    if text in {"where can i go", "what ways out are there", "where do these exits lead"}:
        return Intent("guide", speech="inquiry")
    feasibility = re.fullmatch(r"(?:can|could|may) i (.+)", text)
    if feasibility:
        candidate = _proposal(feasibility[1])
        return replace(candidate, speech="inquiry") if candidate else Intent("unknown_question", speech="inquiry")
    for pattern, action, speech in (
        (_TESTIMONY, "report", "inquiry"), (_DIRECT_TESTIMONY, "report", "inquiry"),
        (_STATEMENT, "statement", "statement"),
    ):
        match = pattern.fullmatch(text)
        if match:
            person, target, condition = match.groups()
            facet, value = _CONDITIONS[condition]
            return Intent(action, target, person=person, facet=facet, value=value, speech=speech)
    witness = _WITNESS_TOPIC.fullmatch(text)
    if witness:
        return Intent("report", witness[2] or "it", person=witness[1], speech="inquiry")
    report = _REPORT_TOPIC.fullmatch(text)
    if report:
        return Intent("report", report[2], person=report[1], facet=report[3], speech="inquiry")
    condition = re.fullmatch(rf"(?:is|was) (.+?) (?:still )?({_CONDITION_WORD})", text)
    if condition and text.startswith("is "):
        return Intent("condition", condition[1], facet=_CONDITIONS[condition[2]][0], speech="inquiry")
    work = re.fullmatch(r"(?:ask (.+?) to|(?:have|get) (.+?) to|have (.+?)) (.+)", text)
    if work:
        person = next(item for item in work.groups()[:3] if item is not None)
        clause = work[4]
        switch = re.fullmatch(r"use (.+?) instead", clause)
        if switch:
            return Intent("work", instrument=switch[1], person=person, speech="request")
        intent = _cleaning(clause, person)
        if intent:
            return replace(intent, speech="request")
    handoff = re.fullmatch(r"ask (.+?) for (.+)", text)
    if handoff:
        return Intent("request_object", handoff[2], person=handoff[1], speech="request")
    if _QUESTION.match(text):
        return None
    travel = _TRAVEL.fullmatch(text)
    if travel:
        verb, target = travel.groups()
        if verb in {"get", "run", "sprint", "sneak"} and not re.match(r"^(?:back|to|there)\b", target):
            return None
        target = re.sub(r"^(?:back (?:to |into )?|(?:over )?to |towards? |into )", "", target) or "back"
        return Intent("travel", target, method=_MOVEMENT[verb])
    cleaning = _cleaning(text)
    if cleaning:
        return cleaning
    put = re.fullmatch(r"(?:put|set|place) (.+?) (in|inside|into|on|onto) (.+)", text)
    if put:
        return Intent("place", put[1], "store" if put[2] in {"in", "inside", "into"} else "put_on",
                      put[3])
    object_action = _PHYSICAL.fullmatch(text)
    if object_action:
        verb, target = object_action.groups()
        if verb == "check" and target.startswith(("if ", "whether ", "how ", "why ")):
            return None
        return Intent(_OBJECT_ACTIONS[verb], target)
    return None


class Clarification(ValueError):
    def __init__(self, field, message):
        super().__init__(message)
        self.field = field


class ReferenceUnavailable(ValueError):
    pass


class IntentSession:
    def __init__(self, application):
        self.app = application
        self.context = InputContext(application)
        self.pending = None
        self.facet = ""

    def offer(self, raw, parsed):
        original = raw.strip()
        text = words(original)
        if not text:
            return None
        if original.startswith(('"', "'", "“", "‘", ">")) or _UNSAFE.match(text):
            self.pending = None
            return (Intent("non_attempt", speech="non_attempt"),)
        if text in {"actually leave it", "leave it", "never mind", "forget it", "cancel that"}:
            self.pending = None
            return (Intent("cancel", speech="correction"),)
        if self.pending:
            reply = re.fullmatch(r"(?:no |actually |i meant |with |using )(.+)", text)
            if (reply is None and parsed.action in {"unsupported", "ambiguous", "uninterpretable"}
                    and _proposal(text) is None and len(text.split()) <= 5 and not _QUESTION.match(text)):
                reply = re.fullmatch(r"(.+)", text)
            if reply:
                proposal, field, place = self.pending
                self.pending = None
                if place != self.context.here:
                    return (Intent("expired", speech="correction"),)
                return (replace(proposal, **{field: reply[1]}),)
            self.pending = None
        if re.match(r"^(?:no |actually |i meant |with |using )", text) and _proposal(text) is None:
            return (Intent("expired", speech="correction"),)

        polite = _POLITE.match(text)
        body = text[polite.end():] if polite else text
        if _UNSAFE.match(body):
            return (Intent("non_attempt", speech="non_attempt"),)
        pieces = _ORDERED.split(body)
        if len(pieces) > 1:
            if original.endswith("?"):
                return (Intent("unknown_question", speech="inquiry"),)
            proposed = tuple(_proposal(piece) for piece in pieces)
            if (len(pieces) == 2 and all(proposed) and proposed[0].action == "travel"
                    and proposed[0].speech == "attempt" and not _QUESTION.match(body)):
                if not polite and reference(proposed[0].target) in {"north", "south", "east", "west"}:
                    return None
                return proposed
            if polite or any(_UNSAFE.match(piece) for piece in pieces):
                return (Intent("sequence_unavailable", speech="attempt"),)
            return None

        if (not polite and not original.endswith("?") and parsed.action == "ambiguous"
                and self.context.subject is None and self.context.person is None):
            return None
        if not polite and parsed.failure_class == "unsupported_compound_intent_sequencing":
            return None

        proposal = _proposal(body)
        if proposal is None:
            if original.endswith("?") or _QUESTION.match(body):
                from astra_runtime.myravant_goal_method_lantern import parse_lantern_destination_goal
                goal = parse_lantern_destination_goal(raw)
                if goal is not None:
                    if goal.method is None:  # The retained owner path offers advice only.
                        return None
                    return (Intent("unknown_question", speech="inquiry"),)
            if original.endswith("?"):
                from astra_runtime.myravant_situated_inquiry import parse_situated_inquiry
                if parse_situated_inquiry(raw).parsed:
                    return None
                return (Intent("unknown_question", speech="inquiry"),)
            return None
        if original.endswith("?") and proposal.speech != "inquiry":
            return (replace(proposal, speech="inquiry"),)
        if (not polite and proposal.constraint.startswith("while ")
                and reference(proposal.target) in {"north", "south", "east", "west"}):
            return None
        if parsed.action == "inspect_self" and not polite:
            return None
        if polite or proposal.constraint:
            return (proposal,)
        from astra_runtime.myravant_terminal_capabilities import classify_bounded_terminal_request
        legacy = classify_bounded_terminal_request(raw, fixture=self.app.fixture)
        if legacy is not None and legacy not in {"water", "material"}:
            return None
        if original.endswith((".", "!")):
            return (proposal,)
        if self._legacy_form(body, parsed, proposal):
            return None
        return (proposal,)

    def _legacy_form(self, text, parsed, proposal):
        # Exact established commands keep their dispatcher, including prior
        # fixture aliases and failure classes. Descriptions use qualified lookup.
        if proposal.action == "travel":
            return parsed.action in {"move", "move_crawl"}
        if proposal.action == "request_object":
            return all(self._exact(value, kind) for value, kind in (
                (proposal.target, "thing"), (proposal.person, "person")))
        if proposal.action == "statement":
            return " residue is " in text or " moisture is " in text
        if proposal.action == "report" and _REPORT_TOPIC.fullmatch(text):
            return self._exact(proposal.target, "thing") and self._exact(proposal.person, "person")
        if proposal.action == "work" and text.startswith("ask ") and " to clean " in text:
            return (self._exact(proposal.target, "thing") and self._exact(proposal.person, "person")
                    and (not proposal.instrument or self._exact(proposal.instrument, "thing")))
        if proposal.action == "place":
            return all(self._exact(value, "thing") for value in (proposal.target, proposal.instrument))
        if proposal.action == "clean":
            return (text.startswith(("wipe ", "scrub ")) and bool(proposal.instrument)
                    and all(self._exact(value, "thing") for value in (proposal.target, proposal.instrument)))
        if proposal.action == "untie":
            return self._exact(proposal.target, "thing")
        if proposal.action in _OBJECT_ACTIONS.values() and parsed.action == proposal.action:
            return self._exact(proposal.target, "thing") or (
                proposal.action == "inspect" and self._exact(proposal.target, "person"))
        return False

    def _exact(self, value, kind):
        # Existing owner target forms include admitted internal labels and
        # pronoun-free unique short forms. Never surface hidden matches.
        context = self.context
        local = context.local(kind)
        term = reference(value)
        if (term in _PRONOUNS | _PEOPLE | _TOOL_RECALL or re.match(r"^(?:other|front|rear|wet|dry|damp) ", term)
                or any(term == reference(alias) for entity in local
                       for alias in context.aliases.get(entity, ()))):
            return False
        candidates = context.match(value, local)
        if not candidates:
            return True  # Preserve the qualified refusal of an exact command.
        if len(candidates) != 1:
            return False
        resolve = (context.fixture.resolve_actor_reference if kind == "person"
                   else context.fixture.resolve_object_reference)
        try:
            return resolve(term) == candidates[0]
        except ValueError:
            return False

    def notice(self, parsed, result, source, route=None):
        if result.failure_class:
            return
        context = self.context
        context.note_view(result.view)
        direction = parsed.argument if parsed.action in {"move", "move_crawl"} else None
        context.note_movement(source, direction)
        if parsed.action in {"inspect", "pickup", "drop", "open", "close"} and parsed.argument:
            entries = context.local("thing")
            matches = context.match(parsed.argument, entries)
            if len(matches) == 1:
                context.subject = matches[0]
                if parsed.action == "inspect":
                    context.seen.setdefault(matches[0], set()).add(context.here)
            elif parsed.action == "inspect":
                people = context.match(parsed.argument, context.local("person"))
                if len(people) == 1:
                    context.person = people[0]
        if route == "actors":
            from astra_runtime.myravant_tarrow_actors import parse_actor_request
            parsed_request = parse_actor_request(parsed.raw_text)
            if parsed_request:
                action, args = parsed_request
                actors = context.match(args[0], context.local("person"))
                if len(actors) == 1:
                    context.person = actors[0]
                if action in {"report", "cleaning"}:
                    objects = context.match(args[1], context.local("thing"))
                    if len(objects) == 1:
                        context.subject = objects[0]
                        if action == "cleaning":
                            context.work_target = objects[0]
                        else:
                            self.facet = args[2]
        if route == "water":
            from astra_runtime.myravant_water_application import parse_water
            attempt = parse_water(parsed.raw_text)
            if attempt:
                operation, participants, _ = attempt
                if operation in {"wipe", "scrub"}:
                    for text, field in zip(participants, ("subject", "tool")):
                        matches = context.match(text, context.local("thing"))
                        if len(matches) == 1:
                            setattr(context, field, matches[0])

    def _result(self, message, failure=None):
        digest = self.app.authoritative_digest()
        return PlayApplicationResult(result_type="player_intention", message=message,
                                     authoritative_changed=False, pre_state_digest=digest,
                                     post_state_digest=digest, failure_class=failure)

    def _resolve(self, phrase, options, field, *, remembered=None):
        context = self.context
        term = reference(phrase)
        if term in _PRONOUNS | _PEOPLE | _TOOL_RECALL | {"one"}:
            candidates = [remembered] if remembered in options else []
            if remembered is not None and not candidates:
                raise ReferenceUnavailable("The earlier reference can't be identified in the current situation.")
        elif term.startswith("other ") or term == "other one":
            head = term.removeprefix("other ")
            if head == "one" and remembered in options:
                labels = context.names(remembered)
                head = next((reference(name).split()[-1] for name in labels[1:]),
                            reference(labels[0]).split()[-1])
            candidates = [item for item in context.match(head, options) if item != remembered]
            if remembered not in options:
                candidates = []
        else:
            if term.endswith(" one"):
                phrase = term.removesuffix(" one")
            candidates = context.match(phrase, options)
        if len(candidates) == 1:
            return candidates[0]
        label = {"target": "object", "instrument": "tool or support", "person": "person"}[field]
        if candidates:
            names = ", ".join(self.app.fixture.entity_name(item) for item in candidates)
            raise Clarification(field, f"Which {label} do you mean? {names}.")
        if term in _PRONOUNS | _PEOPLE | _TOOL_RECALL | {"", "one"} or term.startswith("other "):
            raise Clarification(field, f"Which {label} here do you mean?")
        raise ReferenceUnavailable(f"I can't identify that {label} in the current situation.")

    def _travel(self, proposal):
        context = self.context
        if proposal.speech == "attempt" and proposal.method not in {"walk", "crawl"}:
            yield self._result(f"The requested travel method ({proposal.method}) is unavailable here.",
                               "intent_missing_mechanic")
            return
        targets = context.destinations(proposal.target)
        if len(targets) != 1:
            names = ", ".join(context.fixture.entity_name(item) for item in targets)
            message = f"Which destination do you mean? {names}." if targets else (
                "I can't identify a known destination from that description. " + context.route_labels())
            raise Clarification("target", message.rstrip())
        target = targets[0]
        route = context.shortest_route(target)
        if isinstance(route, list):
            first = ", ".join(dict.fromkeys(context.fixture.entity_name(path[0][1]) for path in route))
            yield self._result(f"Which way would you like to take? Known routes start toward {first}.",
                               "intent_route_choice")
            return
        if route is None:
            yield self._result("You have no known route from here to that destination.", "intent_route_unknown")
            return
        name = context.fixture.entity_name(target)
        if proposal.speech == "inquiry":
            via = ", ".join(context.fixture.entity_name(place) for _, place in route)
            yield self._result(f"Known way to {name}: {via}." if via else f"You are already at {name}.")
            return
        if not route:
            yield self._result(f"You are already at {name}.")
            return
        start = context.here
        for direction, destination in route:
            source = context.here
            result = self.app.move(direction, method=proposal.method)
            context.note_movement(source, direction)
            if result.failure_class or context.here != destination:
                reason = result.message if result.failure_class else "Your position changed unexpectedly."
                yield replace(result, message=f"Travel stopped at {context.fixture.entity_name(context.here)}. {reason}",
                              failure_class=result.failure_class or "intent_travel_interrupted", view=None)
                return
            yield result
        context.previous_place = start

    def _clean(self, proposal, person):
        context = self.context
        fixture = context.fixture
        water_profile = getattr(fixture, "water_profile", None)
        if water_profile is None:
            return self._result("Cleaning has no implemented method in this locality.", "intent_missing_mechanic")
        pairs = [(method, target, tool) for method, target, tool in water_profile.allowed_pairs
                 if method in {"wipe", "scrub"}]
        local = context.local("thing")
        surfaces = tuple(dict.fromkeys(target for _, target, _ in pairs if target in local))
        subject = proposal.target or "it"
        previous = context.work_target if not proposal.target else context.subject
        target = self._resolve(subject, surfaces, "target", remembered=previous)
        proposed_tool = None
        if proposal.instrument:
            wording = reference(proposal.instrument)
            condition = re.fullmatch(r"(damp|wet|dry) (.+)", wording)
            proposed_tool = self._resolve(condition[2] if condition else wording, local, "instrument",
                                          remembered=context.tool)
            if condition:
                current = dict(self.app.water_state.water).get(proposed_tool)
                if current is None or bool(current) != (condition[1] != "dry"):
                    return self._result("The referenced tool does not have the stated moisture condition here.",
                                        "intent_context_blocked")
        candidates = [(method, tool) for method, surface, tool in pairs
                      if surface == target and tool in local
                      and (not proposal.method or proposal.method == method)
                      and (proposed_tool is None or tool == proposed_tool)]
        if not candidates:
            return self._result("That method and tool are not available for this surface here.",
                                "intent_context_blocked")
        if len(candidates) > 1:
            verbs = {"scrub": "scrubbing", "wipe": "wiping"}
            names = ", ".join(f"{fixture.entity_name(tool)} for {verbs[method]}" for method, tool in candidates)
            raise Clarification("instrument", f"Which tool would you like to use? {names}.")
        method, tool = candidates[0]
        target_name, tool_name = (context.owner_reference(entity) for entity in (target, tool))
        result = (self.app.request_cleaning(context.owner_reference(person, person=True), target_name,
                                            tool_reference=tool_name, method=method)
                  if person else self.app.water(method, target_name, tool_name, amount=None))
        if not result.failure_class:
            context.subject, context.tool = target, tool
            if person:
                context.work_target = target
        return result

    def execute(self, proposal):
        context = self.context
        action = proposal.action
        try:
            if proposal.constraint:
                yield self._result(f"I can't guarantee that constraint here ({proposal.constraint}).",
                                   "intent_constraint_unavailable")
                return
            if action == "travel":
                yield from self._travel(proposal)
                return
            if action == "guide":
                yield self._result(context.route_labels() or "There are no readable exit signs here.")
                return
            if action in {"non_attempt", "cancel", "expired", "sequence_unavailable", "unknown_question"}:
                messages = {
                    "non_attempt": "I treated that as a statement, quotation, negation or hypothetical.",
                    "cancel": "The unfinished request is set aside.",
                    "expired": "There is no current question to answer. Say what you want to do here.",
                    "sequence_unavailable": "I couldn't establish the order of those actions. Try one at a time.",
                    "unknown_question": "I couldn't interpret what you were asking.",
                }
                failure = None if action in {"cancel", "non_attempt"} else "intent_" + action
                yield self._result(messages[action], failure)
                return
            if proposal.speech == "inquiry" and action not in {"report", "condition"}:
                yield self._result("I heard a question. This action's feasibility cannot be checked in that form.",
                                   "intent_feasibility_unavailable")
                return
            person = (self._resolve(proposal.person, context.local("person"), "person",
                                    remembered=context.person) if proposal.person else None)
            if action in {"clean", "work"}:
                if person and not hasattr(self.app, "request_cleaning"):
                    yield self._result("There is no work agreement procedure here.", "intent_missing_mechanic")
                else:
                    result = self._clean(proposal, person)
                    if person and not result.failure_class:
                        context.person = person
                    yield result
                return
            entries = context.local("thing")
            if action == "inspect":
                entries += context.local("person")
            target = self._resolve(proposal.target, entries, "target", remembered=context.subject)
            inspecting_person = action == "inspect" and target in context.local("person")
            name = context.owner_reference(target, person=inspecting_person)
            if action in {"report", "statement"}:
                owner = getattr(self.app, "ask_report" if action == "report" else "tell_actor", None)
                if owner is None:
                    yield self._result("This locality has no qualified procedure for that kind of conversation.",
                                       "intent_missing_mechanic")
                    return
                facet = proposal.facet or self.facet
                if not facet:
                    raise Clarification("facet", "What did you want to ask about: moisture, residue, or activity?")
                args = (context.owner_reference(person, person=True), name, facet)
                result = owner(*args) if action == "report" else owner(*args, proposal.value)
                if not result.failure_class:
                    self.facet = facet
            elif action == "request_object":
                result = self.app.request_object_from_actor(context.owner_reference(person, person=True), name)
            elif action == "place":
                base = self._resolve(proposal.instrument, entries, "instrument", remembered=context.tool)
                base_name = context.owner_reference(base)
                if proposal.method == "store":
                    result = self.app.store_object(object_reference=name, container_reference=base_name)
                elif hasattr(self.app, "material"):
                    result = self.app.material("put_on", name, base_name)
                else:
                    result = self._result("Placing objects on supports has no implemented method here.",
                                          "intent_missing_mechanic")
            elif action == "untie":
                owner = getattr(self.app, "material", None)
                result = (owner("untie", name) if owner else
                          self._result("This locality has no qualified untying method.", "intent_missing_mechanic"))
            else:
                method = {"open": "open_object", "close": "close_object", "condition": "inspect"}.get(action, action)
                result = getattr(self.app, method)(name)
            if not result.failure_class:
                if target in context.local("person"):
                    context.person = target
                else:
                    context.subject = target
                    if action in {"inspect", "condition"}:
                        context.seen.setdefault(target, set()).add(context.here)
                        if proposal.facet:
                            self.facet = proposal.facet
                if person:
                    context.person = person
            yield result
        except Clarification as exc:
            self.pending = (proposal, exc.field, context.here)
            yield self._result(str(exc), "intent_clarification")
        except ReferenceUnavailable as exc:
            yield self._result(str(exc), "intent_context_blocked")
