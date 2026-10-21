"""Opt-in, actor-owned investigation projection over admitted evidence.

No query owns world truth, sensing, time, inquiry, commitment or persistence.
The only additional durable data captures an earlier speaker already disclosed
by a qualified local report, never another actor's undisclosed source chain.
"""
from dataclasses import replace

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_material_application import _transaction
from astra_runtime.domain.persistent_world_material import digest
from astra_runtime.domain import persistent_world_actor_evidence as evidence
from astra_runtime import myravant_actor_knowledge as knowledge


MAX_HISTORY = 8
DISCLOSURE_POLICY = "recipient-visible-immediate-and-one-disclosed-source-1"
QUERY_POLICY = "requester-admitted-target-and-facet-only;read-only;value-diverse-comparison-2"


def _key(value):
    return " ".join(str(value).casefold().replace("-", " ").split())


class InvestigationApplication(ActorApplication):
    """A separate journal binding. Old actor checkpoints are not converted."""

    checkpoint_format = "myravant.investigation-actor-time-material-owner-journal"

    @staticmethod
    def default_fixture():
        from astra_runtime.myravant_tarrow_investigation import create_investigation_fixture
        return create_investigation_fixture()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disclosed_relays = ()
        self._validate_transaction()

    def _checkpoint_profile(self):
        return {"actor": super()._checkpoint_profile(),
                "query_policy": QUERY_POLICY,
                "disclosure_policy": DISCLOSURE_POLICY,
                "recipe_identity": self.fixture.actors_version}

    def authoritative_digest(self):
        base = super().authoritative_digest()
        if not hasattr(self, "disclosed_relays"):
            return base
        return digest({"actor": base, "disclosed_relays": self.disclosed_relays,
                       "policy": DISCLOSURE_POLICY})

    def _capture_transaction(self):
        original = super()._capture_transaction()
        return (original, self.disclosed_relays) if hasattr(self, "disclosed_relays") else original

    def _restore_transaction(self, snapshot):
        original, self.disclosed_relays = snapshot
        super()._restore_transaction(original)

    def _validate_transaction(self):
        super()._validate_transaction()
        if not hasattr(self, "disclosed_relays"):
            return
        if type(self.disclosed_relays) is not tuple:
            raise ValueError("invalid disclosed report binding")
        seen = set()
        player = self.fixture.player_entity_id
        known_actors = {e.entity_id for e in self.state.representation.entities
                        if e.classification == "character_or_creature"}
        admitted = {e.event_id: e for e in self.evidence_state.events if e.actor_id == player}
        for entry in self.disclosed_relays:
            if (type(entry) is not tuple or len(entry) != 2
                    or any(type(x) is not str or not x for x in entry)):
                raise ValueError("invalid disclosed report entry")
            event_id, earlier_actor = entry
            record = admitted.get(event_id)
            if (event_id in seen or earlier_actor not in known_actors
                    or record is None or record.kind != "reported"
                    or record.source_actor_id == earlier_actor):
                raise ValueError("disclosed report must bind unique recipient evidence")
            seen.add(event_id)

    def _disclosed(self, event_id):
        return next((actor for key, actor in self.disclosed_relays if key == event_id), None)

    def _admitted_history(self, target_text, facet):
        # Match *only* already admitted player records. Never resolve an unknown
        # name against the whole fixture or inspect another actor's evidence.
        if facet not in knowledge.FACETS:
            return "unsupported", ()
        player = self.fixture.player_entity_id
        known = {e.target_id for e in self.evidence_state.events if e.actor_id == player}
        matches = tuple(sorted(target for target in known
                               if _key(self.fixture.entity_name(target)) == _key(target_text)))
        if len(matches) != 1:
            return ("ambiguous" if len(matches) > 1 else "unknown"), ()
        return "ok", tuple(e for e in self.evidence_state.events
                           if e.actor_id == player and e.target_id == matches[0]
                           and e.facet == facet)

    def _present_value(self, record):
        value = record.value
        if type(value) is str:
            return value
        if record.facet == "placement" and len(value) == 2:
            relationship, object_id = value
            # These identities were admitted in the historical evidence; no
            # current-world placement or visibility query occurs here.
            return relationship.replace("_", " ") + " " + self.fixture.entity_name(object_id)
        return ", ".join(value)

    def _present(self, record):
        if record.kind == "performed":
            source = "own committed action"
        elif record.kind == "witnessed":
            source = "own admitted observation"
        else:
            source = "received statement from " + self.fixture.entity_name(record.source_actor_id)
            disclosed = self._disclosed(record.event_id)
            if disclosed is not None:
                source += "; earlier speaker disclosed as " + self.fixture.entity_name(disclosed)
        markers = ("source-order " + str(record.origin_tick) + "; delivery-order " + str(record.tick)
                   if record.origin_tick is not None else "admission-order " + str(record.tick))
        return source + " [" + markers + "]: " + self._present_value(record)

    def _read_only_result(self, message):
        result = self._result(message)
        return replace(result, result_type="investigation_history",
                       authoritative_changed=False)

    def recall_history(self, target_text, facet):
        status, entries = self._admitted_history(target_text, facet)
        if status == "unsupported":
            return self._read_only_result("That topic is not admitted by this evidence profile.")
        if status == "ambiguous":
            return self._read_only_result("More than one admitted subject matches; qualify the subject.")
        if not entries:
            return self._read_only_result(
                "No player-admitted history matches that subject and topic. "
                "This does not establish that nothing occurred.")
        rows = entries[-MAX_HISTORY:]
        omitted = len(entries) - len(rows)
        header = "Retained player history, oldest to newest"
        if omitted:
            header += " (latest " + str(MAX_HISTORY) + "; " + str(omitted) + " older omitted)"
        return self._read_only_result(header + ":\n" + "\n".join(
            str(i + 1 + omitted) + ". " + self._present(entry)
            for i, entry in enumerate(rows)) +
            "\nLogical markers are ordering, not event dates or current truth.")

    def compare_history(self, target_text, facet):
        status, entries = self._admitted_history(target_text, facet)
        if status == "unsupported":
            return self._read_only_result("That topic is not admitted by this evidence profile.")
        if status == "ambiguous":
            return self._read_only_result("More than one admitted subject matches; qualify the subject.")
        if not entries:
            return self._read_only_result(
                "No player-admitted accounts match that subject and topic. "
                "Unrecorded events and undisclosed accounts remain unknown.")
        # Comparison needs historical value diversity as well as recency.
        # A flat last-N window can hide a still-retained contradictory report
        # after enough later observations. Include one earlier distinct value,
        # if any, while retaining the seven most recent reports and preserving
        # original admission-order labels. This does not inspect world truth.
        first = max(0, len(entries) - MAX_HISTORY)
        numbered = list(enumerate(entries[first:], start=first + 1))
        shown_values = {repr(event.value) for _, event in numbered}
        if first:
            omitted_distinct = next(
                ((i, event) for i, event in enumerate(entries[:first], 1)
                 if repr(event.value) not in shown_values),
                None,
            )
            if omitted_distinct is not None:
                numbered = [omitted_distinct, *numbered[1:]]
                numbered.sort(key=lambda item: item[0])
        distinct = len({repr(e.value) for _, e in numbered})
        note = ("Different retained values may describe different conditions or contexts."
                if distinct > 1 else "Displayed retained values agree; that does not certify truth.")
        truncated = (
            f" Displayed {len(numbered)} of {len(entries)} admitted records; some history is omitted."
            if len(entries) > len(numbered) else ""
        )
        return self._read_only_result("Comparison of retained player-admitted accounts:\n" +
            "\n".join(str(i) + ". " + self._present(e) for i, e in numbered) +
            "\n" + note + truncated +
            " No account is selected as true, false, guilty or conclusive.")

    def ask_report(self, actor_reference, target_reference, facet):
        # Qualification, delivery and the authoritative report remain owned by
        # the approved #548 method. Capture only what that method already displays.
        earlier = None
        try:
            speaker = self._actor(actor_reference)
            target = self.fixture.resolve_object_reference(target_reference)
            original = evidence.latest(self.evidence_state, speaker, target, facet)
            if original is not None and original.kind == "reported":
                earlier = original.source_actor_id
        except ValueError:
            pass
        result = ActorApplication.ask_report.__wrapped__(
            self, actor_reference, target_reference, facet)
        if result.authoritative_changed and earlier is not None:
            delivered = evidence.latest(self.evidence_state,
                                        self.fixture.player_entity_id, target, facet)
            if delivered is not None and delivered.kind == "reported":
                self.disclosed_relays = (*self.disclosed_relays, (delivered.event_id, earlier))
        return result


# One authoritative journal/rollback for the delivered evidence and what was
# explicitly disclosed; no query is added to replay methods or journaling.
InvestigationApplication.ask_report = _transaction(
    InvestigationApplication.ask_report, "ask_report")
