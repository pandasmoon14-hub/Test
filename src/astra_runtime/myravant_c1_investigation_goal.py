"""C-1 interpreter for actor-situated witness, report, and history requests.

Only parse a bounded intent; the actor-memory owner in the playable
application qualifies sensory access and commits replayable evidence.
"""
from __future__ import annotations

import re

from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_vsm14_application import MyravantVSM14Application


def parse_actor_memory_request(raw: str) -> tuple[str, str, str | None] | None:
    text = " ".join(raw.casefold().strip().split()).rstrip("?.!")
    checks = (
        # Source-qualified investigation keeps witnessed observations distinct
        # from hearsay. Generic "last location" retains C-1 latest-lead behavior.
        (r"ask (?:the )?groundskeeper to (?:check|investigate|follow) "
         r"(?:the )?(?:last )?(?:witnessed|firsthand|observed) "
         r"(?:location|lead|trail) (?:of|for) (.+)", "follow_sighting"),
        (r"ask (?:the )?groundskeeper to (?:check|investigate|follow) "
         r"(?:the )?(?:last )?(?:reported|unverified) "
         r"(?:location|lead|trail) (?:of|for) (.+)", "follow_report"),
        (r"ask (?:the )?groundskeeper to (?:check|investigate|follow) "
         r"(?:the )?(?:last |reported )?(?:location|lead|trail) "
         r"(?:of|for) (.+)", "follow_lead"),
        (r"ask (?:the )?groundskeeper to (?:inspect|examine|look at) (.+)",
         "witness"),
        (r"ask (?:the )?groundskeeper where (?:they|he) last saw (.+)",
         "last_saw"),
        (r"ask (?:the )?groundskeeper (?:what|where) (?:they|he) "
         r"(?:heard about|was told about) (.+)", "heard"),
        (r"ask (?:the )?groundskeeper where (?:they|he) "
         r"(?:think|thinks) (.+?) (?:is|might be)", "recall"),
        (r"tell (?:the )?groundskeeper (?:that )?(.+?) "
         r"(?:is|was) (?:at|in) (?:the )?"
         r"(yard|workshop|orchard path|gatehouse)", "report"),
    )
    for pattern, kind in checks:
        match = re.fullmatch(pattern, text)
        if match is not None:
            obj = match.group(1).removeprefix("the ").strip()
            if obj:
                return (kind, obj, match.group(2) if kind == "report" else None)
    return None


def execute_actor_memory_request(
    application: MyravantVSM14Application, raw: str,
) -> PlayApplicationResult:
    parsed = parse_actor_memory_request(raw)
    if parsed is None:
        raise ValueError("not an actor memory request")
    operation, target, place = parsed
    return application.actor_memory_interaction(
        operation, target, reported_place=place,
    )
