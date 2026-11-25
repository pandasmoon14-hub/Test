"""Session choices over owner actions. Physical progress is restored by those owners."""

from dataclasses import dataclass, replace
import re

from astra_runtime.myravant_goal_methods import Goal, METHODS
from astra_runtime.myravant_input_context import reference


@dataclass(frozen=True)
class Limits:
    no_asking: bool = False
    no_draw: bool = False
    reserve: tuple[str, int] | None = None
    stop_vessel: str = ""


@dataclass
class Plan:
    goal: Goal
    limits: Limits = Limits()
    unsupported: str = ""
    selected: tuple[str, ...] = ()
    committed: int = 0
    stopped: str = ""


class GoalSession:
    def __init__(self, context, result):
        self.context = context
        self.result = result
        self.active = None

    def cancel(self):
        self.active = None

    def _bind(self, command):
        c = self.context
        if command.family == "return":
            matches = c.exchange_matches(command.target, "received")
            subjects = tuple(dict.fromkeys((obj, recipient) for obj, recipient, _ in matches))
            if len(subjects) != 1:
                return None
            target, recipient = subjects[0]
            if command.recipient == "them" and c.person != recipient:
                return None
            return Goal("return", target, recipient, matches[-1][2])
        if command.family == "clean":
            profile = getattr(c.app, "water_profile", None)
            if profile is None:
                return None
            local = c.local("thing")
            known = tuple(asset.id for asset in profile.assets if asset.kind == "surface" and asset.id in local)
        else:
            history = c.history
            stores = (entry.receipt for entry in c.app.storage_state.committed_storage_transitions
                      if entry.receipt.actor_entity_id == c.fixture.player_entity_id)
            known = (*c.local("thing"), *c.seen, *(p.entity for p in history.placements("witnessed")),
                     *(p.entity for p in history.placements("reported")), *(r.object_entity_id for r in stores),
                     *(r[0] for direction in ("gave", "received") for r in history.exchanges(direction)))
        targets = c.remembered_objects(command.target, known)
        if len(targets) == 1:
            return Goal(command.family, targets[0])
        return None

    def _vessel(self, wording):
        c = self.context
        local = c.local("thing")
        vessels = tuple(asset.id for asset in c.app.water_profile.assets
                        if asset.kind == "vessel" and asset.id in local and c.app._visible(asset.id))
        matches = c.match(wording, vessels)
        return matches[0] if len(matches) == 1 else None

    def _limits(self, family, previous, terms):
        limits = previous
        for term in terms:
            if family in {"return", "recover"}:
                if term in {"without asking", "without asking anyone", "without talking to anyone",
                            "without asking the holder"}:
                    limits = replace(limits, no_asking=True)
                    continue
            if family == "clean":
                if term in {"without drawing more water", "without drawing water", "without using more water",
                            "without adding water", "without any fresh water"}:
                    limits = replace(limits, no_draw=True)
                    continue
                reserve = re.fullmatch(r"leave at least ([0-9]{1,3}) units? in (.+)", term)
                if reserve:
                    vessel = self._vessel(reserve[2])
                    value = (vessel, int(reserve[1]))
                    if vessel and (not limits.reserve or limits.reserve == value):
                        limits = replace(limits, reserve=value)
                        continue
                stop = re.fullmatch(r"stop if (?:you )?(?:need|would need|have to use) (.+)", term)
                if stop:
                    vessel = self._vessel(stop[1])
                    if vessel and (not limits.stop_vessel or limits.stop_vessel == vessel):
                        limits = replace(limits, stop_vessel=vessel)
                        continue
            return limits, term
        return limits, ""

    def _options(self, plan):
        return METHODS[plan.goal.family](self.context, plan.goal, plan.limits)

    def _summarize(self, options):
        lines = [options.reason] if options.reason else []
        if options.methods:
            lines.append("Known methods: " + "; ".join(method.description for method in options.methods) + ".")
            if len(options.methods) > 1:
                lines.append("Choose a method. Each has a different tool, source or consequence.")
        if options.investigation:
            lines.append(f"You can {options.investigation.description}. Finding the recipient is uncertain.")
        return " ".join(lines)

    def _stop(self, plan, reason, failure="goal_stopped"):
        plan.stopped = reason
        where = self.context.fixture.entity_name(self.context.here)
        return self.result(f"Stopped at {where}. {reason}", failure)

    def _selected(self, options, key):
        return next((method for method in options.methods if method.key == key), None)

    def execute(self, command):
        if command.action == "goal_status":
            plan = self.active
            if plan is None:
                yield self.result("There is no open goal. You can restate it from your recorded progress.")
            elif plan.stopped:
                yield self.result(f"{plan.committed} plan step(s) committed. {plan.stopped}")
            else:
                yield self.result(self._summarize(self._options(plan)))
            return
        plan = self.active
        if command.action == "goal_start":
            goal = self._bind(command)
            if goal is None:
                # An ungrounded new instruction cannot revive a previous plan.
                self.cancel()
                if command.recipient == "them":
                    message = "I can't identify who 'them' refers to. Name the intended recipient."
                elif command.family == "return":
                    message = "A return needs a unique recorded giver and item."
                else:
                    message = "Name one object or surface from your available observations."
                yield self.result(message, "goal_reference_unavailable")
                return
            self.context.subject = goal.target
            if goal.recipient:
                self.context.person = goal.recipient
            if plan is None or plan.goal != goal:
                plan = self.active = Plan(goal)
        if plan is None:
            yield self.result("There is no open goal. Say what you want to accomplish.", "goal_expired")
            return
        if command.action == "goal_reset":
            plan.limits, plan.unsupported = Limits(), ""
            plan.selected = ()
        if command.terms:
            plan.limits, rejected = self._limits(plan.goal.family, plan.limits, command.terms)
            plan.unsupported = rejected or plan.unsupported
        if plan.unsupported:
            yield self._stop(plan, f"I can't enforce that constraint ({plan.unsupported}). "
                                   "State a supported limit or say clear the limits.",
                             "intent_constraint_unavailable")
            return
        options = self._options(plan)
        if options.complete:
            yield self.result(f"Goal complete. {options.reason}")
            self.cancel()
            return
        if command.speech == "inquiry":
            yield self.result(self._summarize(options))
            return
        if command.action == "goal_reset":
            yield self.result(self._summarize(options))
            return
        if command.method == "check":
            yield from self._investigate(plan)
            return
        if command.method:
            term = reference(command.method)
            choices = tuple(method for method in options.methods if term in method.terms or term == method.key[0])
            if len(choices) != 1:
                message = "That method needs a more specific choice." if choices else "That method is not currently available."
                yield self._stop(plan, f"{message} {self._summarize(options)}")
                return
            plan.selected = choices[0].key
        method = self._selected(options, plan.selected) if plan.selected else None
        if method is None and not plan.selected and len(options.methods) == 1:
            method = options.methods[0]
            plan.selected = method.key
        if method is None:
            yield self._stop(plan, self._summarize(options))
            return
        yield from self._perform(plan, method)

    def _perform(self, plan, method):
        for _ in range(8):
            result = method.step.execute(self.context.app)
            if result.failure_class or not result.authoritative_changed or not result.receipt_id:
                reason = f"{result.message} The goal is still open. Choose another method or revise the situation."
                plan.stopped = reason
                yield replace(result, message=f"Stopped. {reason}",
                              failure_class=result.failure_class or "goal_step_unavailable")
                return
            plan.committed += 1
            if method.next_key:
                plan.selected = method.next_key
            yield result
            options = self._options(plan)
            if options.complete:
                self.cancel()
                yield self.result(f"Goal complete. {options.reason}")
                return
            method = self._selected(options, plan.selected)
            if method is None:
                yield self._stop(plan, self._summarize(options) + " Choose another method if one is available.")
                return
        yield self._stop(plan, "The current attempt reached its step limit. Restate the goal to continue.")

    def _investigate(self, plan):
        for _ in range(8):
            options = self._options(plan)
            if options.investigation is None:
                yield self._stop(plan, self._summarize(options) or "There is no known investigative step.")
                return
            step = options.investigation.step
            source = self.context.here
            result = step.execute(self.context.app)
            if result.failure_class or self.context.here != step.destination:
                reason = f"{result.message} The intended handoff is still open."
                plan.stopped = reason
                yield replace(result, message=f"Stopped. {reason}",
                              failure_class=result.failure_class or "goal_travel_unavailable")
                return
            self.context.note_movement(source, step.args[0])
            self.context.note_view(result.view)
            plan.committed += 1
            yield result
        yield self._stop(plan, "The current investigation reached its step limit.")
