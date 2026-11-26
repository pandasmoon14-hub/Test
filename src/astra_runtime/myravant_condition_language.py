"""Parse bounded questions, evidence standards and conditional continuations."""

from dataclasses import asdict, dataclass, replace
import json
import re

from astra_runtime.myravant_input_context import reference, words


@dataclass(frozen=True)
class ConditionCommand:
    action: str = "conditional_goal"
    family: str = ""
    topic: str = ""
    site: str = ""
    expected: str = ""
    basis: str = "firsthand"
    speaker: str = ""
    worker: str = ""
    protect: str = ""
    ask: str = ""
    ask_if_needed: bool = False
    perform: bool = False
    observe: bool = False
    speech: str = "attempt"
    prohibition: bool = False
    problem: str = ""

    def trace_argument(self, ordinal, count):
        return json.dumps(asdict(self), sort_keys=True)


_ACCESS = r"(?:(?:north|south|east|west)(?:ward)? )?(?:passage|route|way|exit)"
_STATE = r"open|closed|usable|clear|blocked|fitted|finished|unassembled"
_INVESTIGATE = r"(?:find out|check|see|verify|look to see) (?:whether|if)"
_WORK = re.compile(r"ask (.+?) to (?:assemble (.+)|finish (?:it|the (?:job|next available step)))")
_CROSS = re.compile(r"(?:take me through|cross(?: the (?:passage|route))?|go through|continue through)")
_CHOICES = {
    "open": ("access", "separate"), "usable": ("access", "separate"),
    "clear": ("access", "separate"), "closed": ("access", "joined"),
    "blocked": ("access", "joined"), "fitted": ("work", "joined"),
    "finished": ("work", "joined"), "unassembled": ("work", "separate"),
}


def _question(text):
    turn = re.fullmatch(rf"(.+?) (?:is|was) (?:already |still )?({_STATE})(?: (?:at|from) (.+))?", text)
    if not turn:
        return None
    topic, state, site = turn.groups()
    family, _ = _CHOICES[state]
    if family == "access":
        edge = re.fullmatch(rf"((?:the )?{_ACCESS})(?: (?:at|from) (.+))?", topic)
        if not edge:
            return None
        topic, site = edge[1], site or edge[2]
    return family, topic, site or ""


def _test(text):
    basis, speaker = "firsthand", ""
    named = re.fullmatch(r"(.+?) (?:says|said|reports|reported) (?:that )?(.+)", text)
    direct = re.fullmatch(r"(?:i|you) (?:can )?(?:see|verify|confirm) (?:that )?(.+)", text)
    any_evidence = re.fullmatch(r"(?:the )?evidence (?:says|shows|supports) (?:that )?(.+)", text)
    if named and not any_evidence:
        basis, speaker, text = "report", named[1], named[2]
    elif direct:
        text = direct[1]
    elif any_evidence:
        basis, text = "either", any_evidence[1]
    if text in {"it still needs work", "it needs work", "it still needs fitting"}:
        return "work", "separate", basis, speaker, "", ""
    q = _question(text.replace("it is", "the passage is", 1).replace("it was", "the passage was", 1)) if re.fullmatch(
        r"it (?:is|was) (?:still )?(?:open|usable|clear|closed|blocked)", text) else _question(text)
    if q is None and re.fullmatch(r"it (?:is|was) (?:already )?(?:fitted|finished|unassembled)", text):
        state = text.split()[-1]
        return "work", _CHOICES[state][1], basis, speaker, "", ""
    if q is None:
        return None
    family, topic, site = q
    state = re.search(rf"\b(?:is|was) (?:already |still )?({_STATE})\b", text)[1]
    return family, _CHOICES[state][1], basis, speaker, topic, site


def _conditional(raw):
    if raw.startswith("if "):
        pair = re.fullmatch(r"if (.+?)\s*[,;]\s*(?:then )?(.+)", raw)
        if pair:
            return words(pair[1]), words(pair[2])
        pair = re.fullmatch(r"if (.+?) then (.+)", words(raw))
        if pair:
            return pair[1], pair[2]
        return None
    pair = re.fullmatch(r"(.+?) if (.+)", words(raw))
    return pair.groups()[::-1] if pair else None


def parse_condition(raw, *, active):
    stripped = raw.strip().casefold().replace("’", "'")
    if not stripped or stripped.startswith(("'", '"', "“", "‘", ">")):
        return None
    text = words(stripped)
    if text in {"whose account was that", "who saw that", "what did we learn"} or (
            active and text in {"why did we stop", "what stopped us"}):
        return ConditionCommand(action="condition_status", speech="inquiry")
    if active and text in {"check it yourself instead", "check it yourself", "check for yourself", "look for yourself"}:
        return ConditionCommand(action="condition_recheck", observe=True)
    other = re.fullmatch(r"ask (.+?) instead", text)
    if active and other:
        return ConditionCommand(action="condition_recheck", ask=other[1],
                                speech="inquiry" if stripped.endswith("?") else "attempt")
    from_site = re.fullmatch(r"check (?:it )?from (.+)", text)
    if active and from_site:
        return ConditionCommand(action="condition_visit", site=from_site[1],
                                speech="inquiry" if stripped.endswith("?") else "attempt")

    speech = "inquiry" if stripped.endswith("?") else "attempt"
    stripped = re.sub(r"^(?:could i|can i|may i|could we|can we|could you|can you|how could i) ", "", stripped)
    if stripped != raw.strip().casefold().replace("’", "'"):
        speech = "inquiry"
    stripped = re.sub(r"^(?:please |actually |instead )", "", stripped)
    chunks = re.split(r"[.!?;]+\s*", stripped)
    if len(chunks) > 8:
        return None
    plan = ConditionCommand(speech=speech)
    recognized = False
    unparsed = []
    for chunk in filter(None, chunks):
        ban = re.fullmatch(r"(.+?) without (?:asking anyone|talking to anyone)", chunk)
        if ban:
            plan = replace(plan, prohibition=True)
            chunk = ban[1]
        plain = words(chunk).replace("it's", "it is")
        conditioned = _conditional(chunk.replace("it's", "it is"))
        if conditioned:
            test, consequence = conditioned
            suffix = re.fullmatch(r"(.+?) without (?:asking anyone|talking to anyone)", consequence)
            if suffix:
                consequence = suffix[1]
                plan = replace(plan, prohibition=True)
            work = _WORK.fullmatch(consequence)
            cross = _CROSS.fullmatch(consequence)
            outcome = _test(test) if work or cross else None
            if outcome:
                family, expected, basis, speaker, topic, site = outcome
                if plan.perform or (family == "work") != bool(work) or (plan.family and plan.family != family):
                    return ConditionCommand(problem="Keep one scoped condition and consequent in an instruction.")
                requested = (work[2] if work else None) or ""
                topics = [reference(x) for x in (plan.topic, requested, topic) if x and reference(x) != "passage"]
                if len(set(topics)) > 1:
                    return ConditionCommand(problem="The question and action name different targets.")
                if plan.site and site and reference(plan.site) != reference(site):
                    return ConditionCommand(problem="Use the same inspection position throughout the instruction.")
                plan = replace(plan, family=family, topic=requested or plan.topic or topic,
                               site=site or plan.site, expected=expected, basis=basis, speaker=speaker,
                               worker=work[1] if work else "", perform=True)
                recognized = True
                continue
        inquiry = re.fullmatch(rf"{_INVESTIGATE} (.+)", plain)
        account = re.fullmatch(r"ask (.+?) (?:whether|if) (.+)", plain)
        q = _question(inquiry[1]) if inquiry else _question(account[2]) if account else None
        if q:
            family, topic, site = q
            if plan.family and (plan.family != family or
                                (plan.topic and reference(plan.topic) != reference(topic)
                                 and "passage" not in {reference(plan.topic), reference(topic)})):
                return ConditionCommand(problem="The question and action need to refer to the same target.")
            if plan.site and site and reference(plan.site) != reference(site):
                return ConditionCommand(problem="Use the same inspection position throughout the instruction.")
            topic = plan.topic if plan.topic and reference(topic) == "passage" else topic
            if account and plan.ask and not plan.ask_if_needed and reference(plan.ask) != reference(account[1]):
                return ConditionCommand(problem="Choose one witness for this instruction.")
            plan = replace(plan, family=family, topic=topic, site=site or plan.site,
                           observe=plan.observe or bool(inquiry), ask=account[1] if account else plan.ask,
                           ask_if_needed=not account and plan.ask_if_needed)
            recognized = True
        elif re.fullmatch(r"ask (?:someone|a person|a witness)(?: who saw it)?(?: if you need to)?", plain):
            if not plan.ask:
                plan = replace(plan, ask="someone", ask_if_needed=plain.endswith(" if you need to"))
        elif re.fullmatch(r"ask (.+?) if you need to", plain):
            if not plan.ask:
                plan = replace(plan, ask=re.fullmatch(r"ask (.+?) if you need to", plain)[1], ask_if_needed=True)
        elif plain in {"otherwise stop", "otherwise stop there", "if not stop"}:
            pass
        elif plain in {"without asking anyone", "without talking to anyone", "do not ask anyone"}:
            plan = replace(plan, prohibition=True)
        elif re.fullmatch(r"(?:leave|keep) (.+?) (?:where it is|in place)", plain):
            part = re.fullmatch(r"(?:leave|keep) (.+?) (?:where it is|in place)", plain)[1]
            if plan.protect and reference(part) != reference(plan.protect):
                return ConditionCommand(problem="Only one protected placement can be checked in this instruction.")
            plan = replace(plan, protect=part)
        else:
            unparsed.append(plain)
    if not recognized:
        return None
    if unparsed:
        return replace(plan, problem="I couldn't ground every clause. Restate the question, condition and next action.")
    if plan.ask and plan.prohibition:
        return replace(plan, problem="The instruction both permits and prohibits asking.")
    return plan
