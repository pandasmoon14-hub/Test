"""Bounded terminal goal wording. Parsing carries terms without authorizing steps."""

from dataclasses import asdict, dataclass
import json
import re


@dataclass(frozen=True)
class GoalCommand:
    action: str
    family: str = ""
    target: str = ""
    method: str = ""
    recipient: str = ""
    terms: tuple[str, ...] = ()
    speech: str = "attempt"

    def trace_argument(self, ordinal, count):
        return json.dumps(asdict(self), sort_keys=True)


_MODAL = re.compile(r"(?:can i|could i|may i|is there a way to|would it be possible to) (.+)")
_TERMS = re.compile(
    r"\s+(?:(?:and|but) )?(?=(?:without|leave at least|stop if|only if|unless|while|quietly|carefully)(?: |$))")
_RETURN = re.compile(
    r"(get|take|bring|return|give) (.+?) (back )?to "
    r"(the person who gave it to me|(?:its|the) giver|them)")


def parse_goal(text, *, question, followup):
    """Recognize goal descriptions and context-bound follow-ups."""
    modal = _MODAL.fullmatch(text)
    speech = "inquiry" if question or modal else "attempt"
    if modal:
        text = modal[1]
    text = re.sub(r"^(?:please |i (?:want to|would like to) |i'd like to |let me )", "", text)
    head, *terms = _TERMS.split(text)
    terms = tuple(terms)
    if head in {"why did we stop", "what stopped us", "what is left", "what remains"}:
        return GoalCommand("goal_status", speech="inquiry")
    if head in {"do that", "do it", "go ahead", "try that", "use your judgment", "you choose",
                "choose for me", "continue the plan", "carry on", "resume the plan"}:
        return GoalCommand("goal_continue", terms=terms, speech=speech)
    if followup:
        if head in {"clear the limits", "change the limits"} and speech == "attempt":
            return GoalCommand("goal_reset", terms=terms)
        if head in {"start at the last exchange", "check the last exchange first",
                    "check the last exchange", "start there"}:
            return GoalCommand("goal_continue", method="check", terms=terms, speech=speech)
        if head in {"ask the holder", "ask the holder instead", "request a handoff"}:
            return GoalCommand("goal_continue", method="ask", terms=terms, speech=speech)
        if head in {"retrieve it myself", "retrieve it by hand", "take it from the container"}:
            return GoalCommand("goal_continue", method="retrieve", terms=terms, speech=speech)
        method = re.fullmatch(r"(?:use (.+?) instead|use (.+)|(?:try |choose )?(scrub|wipe|handoff|pick up))", head)
        if method and " on " not in head:
            return GoalCommand("goal_continue", method=next(word for word in method.groups() if word),
                               terms=terms, speech=speech)
    returning = _RETURN.fullmatch(head)
    # Preserve the experienced-reference grammar and its existing concise attempt.
    if returning:
        _, target, back, recipient = returning.groups()
        if recipient == "them" and not back and returning[1] != "return":
            return None
        if recipient != "the person who gave it to me" or speech == "inquiry" or terms:
            return GoalCommand("goal_start", "return", target, recipient=recipient, terms=terms, speech=speech)
    recovery = re.fullmatch(r"(?:recover (.+)|get (.+?) back)", head)
    if recovery:
        return GoalCommand("goal_start", "recover", recovery[1] or recovery[2], terms=terms, speech=speech)
    cleaning = re.fullmatch(r"(?:get (.+?) clean|clean (.+))", head)
    if cleaning and (cleaning[1] or terms or speech == "inquiry"):
        return GoalCommand("goal_start", "clean", cleaning[1] or cleaning[2], terms=terms, speech=speech)
    return None
