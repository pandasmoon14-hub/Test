"""Carry a question and its evidence standard through existing goal steps."""

from dataclasses import dataclass, replace

from astra_runtime.myravant_condition_methods import (
    bind_subjects, continuation_step, currently_observed, observation_step,
    player_reports, player_witness, report_steps,
)
from astra_runtime.myravant_goal_methods import Step
from astra_runtime.myravant_input_context import reference


@dataclass
class Question:
    subject: object
    last: str = ""
    prohibition: bool = False
    protect: str = ""


class ConditionSession:
    def __init__(self, context, result, step):
        self.context = context
        self.result = result
        self.step = step
        self.active = None

    def _describe(self, subject, account):
        event = account.event
        tick = event.tick if event.origin_tick is None else event.origin_tick
        word = subject.word(account.state)
        if event.kind == "witnessed":
            return f"You saw that the {subject.label} was {word} at step {tick}."
        name = self.context.fixture.entity_name(event.source_actor_id)
        return f"{name} reported that the {subject.label} was {word} at step {tick}."

    def _people(self):
        c = self.context
        local = c.local("person")
        return tuple(p.actor_id for p in c.fixture.actor_profiles if p.actor_id in local)

    def _choose(self, wording, options):
        if reference(wording) in {"someone", "worker", "a worker", "person", "a person"}:
            return options
        return tuple(self.context.match(wording, options))

    def _names(self, people):
        return ", ".join(self.context.fixture.entity_name(person) for person in people)

    def _stop(self, plan, message):
        plan.last = message
        return self.result(message, "condition_stopped")

    def _check(self, subject):
        # Project the actual condition only inside the actor's sensing scope.
        if currently_observed(self.context, subject) is None:
            return None, None
        before = len(self.context.app.evidence_state.events)
        result = self.step(observation_step(self.context, subject))
        if result.failure_class:
            return result, None
        return result, player_witness(self.context, subject, self.context.app.evidence_state.events[before:])

    def _visit(self, plan, command):
        c = self.context
        places = c.destinations(command.site)
        if places != [plan.subject.place]:
            yield self._stop(plan, "That is outside the documented inspection position for this question.")
            return
        route = c.shortest_route(plan.subject.place)
        if not isinstance(route, tuple) or len(route) > 8:
            yield self._stop(plan, "Choose a bounded route you know to the inspection position.")
            return
        if command.speech == "inquiry":
            yield self.result("You can follow your known route to the inspection position. Arrival will still need a check.")
            return
        for direction, destination in route:
            result = self.step(Step("move", (direction,), keywords=(("method", "walk"),), destination=destination))
            if result.failure_class or c.here != destination:
                message = f"{result.message} The condition and consequent remain open."
                plan.last = message
                yield replace(result, message=message, failure_class=result.failure_class or "condition_travel_stopped")
                return
            yield result
        yield from self.execute(replace(command, action="condition_recheck", observe=True))

    def execute(self, command):
        c, plan = self.context, self.active
        if command.action == "condition_status":
            yield self.result(plan.last if plan and plan.last else "There is no retained account in this conversation.")
            return
        if command.problem:
            yield self.result(command.problem, "condition_unsupported")
            return
        if command.action == "condition_visit":
            if plan is None:
                yield self.result("Restate the question and its limits before continuing.", "condition_unknown")
                return
            yield from self._visit(plan, command)
            return
        if command.action == "condition_recheck":
            if plan is None:
                yield self.result("Restate the question before continuing.", "condition_unknown")
                return
        else:
            topic = command.topic or (plan.subject.label if plan and plan.subject.family == command.family else "")
            use_previous = (plan is not None and plan.subject.family == command.family and not command.site
                            and reference(topic) in {"", "passage", reference(plan.subject.label)})
            matches = (plan.subject,) if use_previous else bind_subjects(c, command.family, topic, command.site)
            if len(matches) != 1:
                if matches:
                    detail = "Choose one known position or direction. " + ", ".join(s.label for s in matches) + "."
                else:
                    detail = ("The condition is still unknown. Name a documented passage or "
                              "visible assembly and its known inspection position.")
                yield self.result(detail, "condition_reference_unavailable")
                return
            if plan is None or plan.subject != matches[0]:
                plan = Question(matches[0])
        subject = plan.subject
        revision = command.action == "condition_recheck" and bool(command.ask)
        prohibition = command.prohibition or (plan.prohibition and not revision)
        if command.protect and plan.protect and reference(command.protect) != reference(plan.protect):
            yield self._stop(plan, "That would replace a placement limit. Cancel the question and restate the complete scope.")
            return
        protected_text = command.protect or plan.protect
        command = replace(command, prohibition=prohibition, protect=protected_text)
        if command.protect and subject.family != "work":
            yield self._stop(plan, "That placement limit cannot be guaranteed for this action.")
            return

        if command.speech == "inquiry":
            where = c.fixture.entity_name(subject.place)
            yield self.result(f"You can check the {subject.label} at {where}. "
                              "A reachable witness can give a dated account. This preview spends no time.")
            return

        self.active = plan
        plan.prohibition, plan.protect = prohibition, protected_text
        if command.ask and prohibition and not command.observe:
            yield self._stop(plan, "The prohibition on asking is active. No one was contacted.")
            return

        # A report standard uses the player's scoped delivered records. The
        # continuation never checks the witness's private history itself.
        reports = player_reports(c, subject)
        firsthand = None
        if (command.observe or (command.perform and command.basis in {"firsthand", "either"})):
            result, firsthand = self._check(subject)
            if result is not None:
                if firsthand is None:
                    plan.last = "The personal check did not establish the condition. No consequent was attempted."
                    yield replace(result, message=f"{result.message} {plan.last}",
                                  view=None, failure_class=result.failure_class or "condition_unknown")
                    return
                plan.last = self._describe(subject, firsthand)
                yield replace(result, message=plan.last, view=None)

        if command.ask and not command.prohibition and (not command.ask_if_needed or firsthand is None):
            choices = self._choose(command.ask, self._people())
            if len(choices) != 1:
                yield self._stop(plan, f"Choose whom to ask. {self._names(choices)}." if choices else
                                 "No qualified person is reachable here. The condition is still unknown.")
                return
            speaker = choices[0]
            steps = report_steps(c, subject, speaker)
            for index, step in enumerate(steps):
                result = self.step(step)
                if result.failure_class or not result.authoritative_changed:
                    plan.last = f"{result.message} The condition is still unknown from this account."
                    yield replace(result, message=plan.last, view=None,
                                  failure_class=result.failure_class or "condition_unknown")
                    return
                if index < len(steps) - 1:
                    yield result
                    continue
                reports = player_reports(c, subject)
                supplied = player_reports(c, subject, speaker)
                if not supplied:
                    plan.last = "This witness has no single observation that settles the whole condition."
                else:
                    plan.last = self._describe(subject, supplied[0]) + " This describes the earlier observation."
                yield replace(result, message=plan.last, view=None)

        if not command.perform:
            if firsthand is None and not command.ask:
                yield self._stop(plan, "The condition is still unknown from here. "
                                 "Check from the documented position or ask a reachable witness.")
            return

        chosen = firsthand
        if command.basis == "report":
            speakers = tuple(e.event.source_actor_id for e in reports)
            people = self._choose(command.speaker, speakers)
            chosen = next((e for e in reports if e.event.source_actor_id == people[0]), None) if len(people) == 1 else None
        elif command.basis == "either":
            relevant = (*((firsthand,) if firsthand else ()), *reports)
            if len({e.state for e in relevant}) > 1:
                accounts = " ".join(self._describe(subject, e) for e in relevant)
                yield self._stop(plan, f"{accounts} These accounts differ. Choose which evidence standard to require.")
                return
            # A generic evidence clause still needs a qualified present view.
            # A historical account can authorize action only when named.
        if chosen is None:
            history = " ".join(self._describe(subject, event) for event in reports)
            reason = "The required evidence is still unknown. No consequent was attempted."
            yield self._stop(plan, f"{history} {reason}".strip())
            return
        if command.basis == "report":
            plan.last = self._describe(subject, chosen) + " Proceeding under the named account condition."
            yield self.result(plan.last)
        if chosen.state != command.expected:
            other = " ".join(self._describe(subject, e) for e in reports if e.state != chosen.state)
            yield self._stop(plan, f"{self._describe(subject, chosen)} {other} The condition was false. No consequent was attempted."
                             .replace("  ", " "))
            return

        worker, protected = "", ""
        if subject.family == "work":
            if command.prohibition:
                yield self._stop(plan, "The prohibition on asking prevents the work request. No new agreement was made.")
                return
            people = self._choose(command.worker, self._people())
            if len(people) != 1:
                yield self._stop(plan, f"Choose an available worker. {self._names(people)}." if people else
                                 "The worker is not reachable here. No new agreement was made.")
                return
            worker = people[0]
            if command.protect:
                matches = c.match(command.protect, c.local("thing"))
                if len(matches) != 1:
                    yield self._stop(plan, "I can't identify one visible part to leave in place.")
                    return
                protected = matches[0]
        try:
            step = continuation_step(c, subject, worker, protected)
        except ValueError as exc:
            yield self._stop(plan, str(exc))
            return
        # Personal authorization is conditional on live opportunity. A dated
        # report can license an attempt, but the action owner still requalifies.
        if command.basis != "report" and currently_observed(c, subject) != chosen.state:
            yield self._stop(plan, "The condition changed before the next action. Check again.")
            return
        result = self.step(step)
        if result.failure_class or not result.authoritative_changed:
            learned = self._describe(subject, chosen)
            next_action = "Crossing is still pending." if subject.family == "access" else "No new agreement was made."
            plan.last = f"{learned} {result.message} {next_action}"
            yield replace(result, message=plan.last, view=None,
                          failure_class=result.failure_class or "condition_stopped")
            return
        action = "You crossed." if subject.family == "access" else "The worker accepted. Physical work is still pending."
        plan.last = f"{self._describe(subject, chosen)} {action}"
        yield result
