"""Optional PLAY-TARROW-SERVICE-1 local service application.

A personal promise is not work authority, an item reservation, property title,
or a legal claim. All material work and handoffs execute through prior owners.
"""
from dataclasses import asdict, replace

from astra_runtime.myravant_actor_application import ActorApplication
from astra_runtime.myravant_material_application import _transaction
from astra_runtime.myravant_actor_physical import execute_actor_physical
from astra_runtime.myravant_play_application import PlayApplicationResult
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_actors import create_actor_fixture
from astra_runtime.domain import persistent_world_actor_participation as participation
from astra_runtime.domain import persistent_world_service_commitment as service
from astra_runtime.domain.persistent_world_material import digest, placement

SERVICE_METHODS = ("offer_service", "respond_service", "withdraw_service",
                   "settle_service", "service_status")


class ServiceApplication(ActorApplication):
    checkpoint_format = "myravant.tarrow-service-personal-commitment-journal"
    replay_methods = (*ActorApplication.replay_methods, *SERVICE_METHODS)

    @staticmethod
    def default_fixture():
        return create_actor_fixture(service_peg=True)

    def __init__(self, **kwargs):
        if "fixture" in kwargs and identity("service-peg") not in {
                o.entity_id for o in kwargs["fixture"].object_presentations}:
            raise ValueError("service profile requires its independently existing peg")
        super().__init__(**kwargs)
        if identity("service-peg") not in {o.entity_id for o in self.fixture.object_presentations}:
            raise ValueError("service package cannot load a base actor campaign")
        self.service_state = service.ServiceState()
        self.service_communicated = ()
        self._validate_transaction()

    def _checkpoint_profile(self):
        return {"actors": super()._checkpoint_profile(),
                "service_policy": "noncanonical-single-service-consent-custody-1",
                "peg": identity("service-peg"),
                "performer": identity("tali"),
                "target": identity("sorting-board"),
                "tool": identity("cleaning-brush")}

    def authoritative_digest(self):
        base = super().authoritative_digest()
        if not hasattr(self, "service_state"):
            return base
        return digest({"actor": base, "service": service.canonical_state(self.service_state),
                       "communicated": self.service_communicated})

    def _capture_transaction(self):
        return (super()._capture_transaction(), self.service_state,
                self.service_communicated)

    def _restore_transaction(self, snapshot):
        old, self.service_state, self.service_communicated = snapshot
        super()._restore_transaction(old)

    def _validate_transaction(self):
        super()._validate_transaction()
        if not hasattr(self, "service_state"):
            return
        receipts = {e[0] for e in self.actor_events}
        receipts.update(t.receipt.receipt_id for t in self.runtime_state.logical_time_state.committed_transitions)
        receipts.update(i[4] for i in self.intervals if i[4])
        identities = {e.entity_id for e in self.state.representation.entities}
        service.canonical_state(self.service_state, receipt_ids=receipts, entity_ids=identities)
        if len(self.service_communicated) > len(self.actor_events):
            raise ValueError("unattributed service disclosures")
        for record in self.service_state.history:
            t = record.terms
            if (t.requester, t.performer, t.beneficiary, t.target, t.tool, t.method,
                    t.peg, t.recipient) != (
                        self.fixture.player_entity_id, identity("tali"),
                        self.fixture.player_entity_id, identity("sorting-board"),
                        identity("cleaning-brush"), "scrub", identity("service-peg"),
                        identity("tali")):
                raise ValueError("terms exceed this service profile")
            if record.task_id is not None:
                matched = [x for x in self.participation_state.records if x.task_id == record.task_id]
                if len(matched) != 1:
                    raise ValueError("service task attribution missing")
                task = matched[0]
                if task.contributions[:len(record.work_receipts)] != record.work_receipts:
                    raise ValueError("work history was replaced")
                if record.state in {"eligible", "settled"} and task.status != "completed":
                    raise ValueError("service completion lacks owner completion")

    def _local_service_actor(self, communication="request"):
        actor = self._actor("Tali Ren")
        self._route(actor, communication)
        return actor

    def offer_service(self):
        pre = self.authoritative_digest()
        try:
            actor = self._local_service_actor("request")
            current = self.service_state.history
            terms = service.make_terms(version=len(current) + 1,
                requester=self.fixture.player_entity_id, performer=actor,
                beneficiary=self.fixture.player_entity_id,
                target=identity("sorting-board"), tool=identity("cleaning-brush"),
                method="scrub", peg=identity("service-peg"), recipient=actor)
            receipt = self._event("service_offer", self.fixture.player_entity_id,
                                  (terms.version, terms.fingerprint))
            self.service_state = service.offer(self.service_state, terms,
                                               disclosure_receipt=receipt)
            message = ("Disclosed service offer version " + str(terms.version) +
                       ": Tali may voluntarily scrub the Sorting Board using the Cleaning Brush; "
                       "only her completed evidenced work permits an optional, later handoff of "
                       "the single Service Workshop Peg. No item or labor is reserved; "
                       "this is not title, wages or an enforceable debt. Fingerprint " +
                       terms.fingerprint + ".")
            self.service_communicated = (*self.service_communicated,
                                         (terms.version, "offered", message))
        except ValueError as exc:
            return self._result(str(exc), failure="service_offer_unavailable")
        return self._metadata_result(pre, "service_offer", actor, message)

    def respond_service(self, version, fingerprint, accept=True):
        pre = self.authoritative_digest()
        try:
            actor = self._local_service_actor("request")
            if type(version) is not int or type(fingerprint) is not str:
                raise ValueError("explicit offered version and fingerprint required")
            proposed = service.latest(self.service_state)
            if proposed.terms.version != version or proposed.terms.fingerprint != fingerprint:
                raise ValueError("stale or incompatible terms")
            if type(accept) is not bool:
                raise ValueError("explicit voluntary decision required")
            if accept:
                profile = self.actor_profile(actor)
                if not profile.willing:
                    raise ValueError("Tali declines the offer.")
                task = self._accept(actor, "cleaning", "scrub",
                                    (identity("sorting-board"), identity("cleaning-brush")),
                                    self._actor_place_id(actor), self.fixture.player_entity_id)
            else:
                task = None
            receipt = self._event("service_decision", actor, (version, fingerprint, accept))
            self.service_state = service.decide(self.service_state, version=version,
                fingerprint=fingerprint, accept=accept, decision_receipt=receipt,
                task_id=task.task_id if task else None)
            message = "Tali " + ("accepts" if accept else "declines") + (
                " the named personal service. Actual material work is still pending."
                if accept else " without work or transfer.")
            self.service_communicated = (*self.service_communicated,
                (version, self.service_state.history[-1].state, message))
        except ValueError as exc:
            return self._result(str(exc), failure="service_decision_unavailable")
        return self._metadata_result(pre, "service_decision", actor, message)

    def _interval(self, name, args=(), kwargs=None, contribution=False):
        result = super()._interval(name, args=args, kwargs=kwargs, contribution=contribution)
        if not result.authoritative_changed or not self.service_state.history:
            return result
        record = service.latest(self.service_state)
        if record.state not in {"accepted", "partial"}:
            return replace(result, post_state_digest=self.authoritative_digest())
        task = next((x for x in self.participation_state.records
                     if x.task_id == record.task_id), None)
        if task is None:
            raise ValueError("selected service work disappeared")
        receipts = {e[0] for e in self.actor_events}
        if task.status == "withdrawn":
            self.service_state = service.reconcile(self.service_state, task=task,
                                                   receipt_ids=receipts)
            receipt = self._event("service_actor_withdrawn", task.actor_id, task.task_id)
            self.service_state = service.withdraw(self.service_state, receipt=receipt)
        else:
            self.service_state = service.reconcile(self.service_state, task=task,
                receipt_ids=receipts,
                completion_receipt=task.contributions[-1] if task.status == "completed" else None)
        return replace(result, post_state_digest=self.authoritative_digest())

    def withdraw_service(self):
        pre = self.authoritative_digest()
        try:
            actor = self._local_service_actor("control")
            record = service.latest(self.service_state)
            if record.state in {"accepted", "partial"}:
                task = participation.selected(self.participation_state, actor)
                if task.task_id != record.task_id:
                    raise ValueError("service task selection has changed")
                self.participation_state = participation.withdraw(
                    self.participation_state, actor,
                    reason="performer locally accepts withdrawal")
            receipt = self._event("service_withdrawal", actor, record.terms.fingerprint)
            self.service_state = service.withdraw(self.service_state, receipt=receipt)
            message = "The voluntary service is withdrawn. Previous physical work remains."
            self.service_communicated = (*self.service_communicated,
                (record.terms.version, "withdrawn", message))
        except ValueError as exc:
            return self._result(str(exc), failure="service_withdrawal_unavailable")
        return self._metadata_result(pre, "service_withdrawal", actor, message)

    def settle_service(self):
        pre = self.authoritative_digest()
        try:
            actor = self._local_service_actor("control")
            if not self.actor_profile(actor).willing:
                raise ValueError("Tali does not currently agree to receive the peg.")
            record = service.latest(self.service_state)
            if record.state != "eligible":
                raise ValueError("Only completed attributable service is handoff-eligible.")
            peg = identity("service-peg")
            relation = placement(self.state.representation, peg)
            if (relation.relation_type, relation.object_entity_id) != (
                    "carried_by", self.fixture.player_entity_id):
                raise ValueError("Player must actually carry the existing whole peg.")
            outcome = execute_actor_physical(self, self.fixture.player_entity_id,
                                             "give", peg, actor)
            if not outcome.authoritative_changed:
                raise ValueError(outcome.message)
            self._event("service_custody_handoff", actor, peg,
                        receipt=outcome.receipt_id)
            self.service_state = service.settle(self.service_state,
                custody_receipt=outcome.receipt_id, actual_object=peg,
                giver=self.fixture.player_entity_id, recipient=actor)
            message = ("The actual peg was handed to Tali once, in custody only. "
                       "No title, wage, price or enforcement claim was created.")
            self.service_communicated = (*self.service_communicated,
                (record.terms.version, "settled", message))
        except ValueError as exc:
            return self._result(str(exc), failure="service_handoff_unavailable")
        return self._metadata_result(pre, "service_handoff", actor, message)

    def service_status(self):
        pre = self.authoritative_digest()
        if not self.service_state.history:
            return self._result("No disclosed service offer is recorded.")
        record = service.latest(self.service_state)
        try:
            actor = self._local_service_actor("status")
        except ValueError:
            if not self.service_communicated:
                return self._result("No last communicated service status is available.")
            _, status, message = self.service_communicated[-1]
            return self._result("Last communicated service status: " + status +
                                ". " + message + " Current progress is unavailable here.")
        message = ("Service version " + str(record.terms.version) + ": " + record.state +
                   "; " + str(len(record.work_receipts)) +
                   " committed performer step(s). Custody settlement: " +
                   ("recorded" if record.state == "settled" else "not recorded") + ".")
        self.service_communicated = (*self.service_communicated,
            (record.terms.version, record.state, message))
        return self._metadata_result(pre, "service_status", actor, message)


for _name in SERVICE_METHODS:
    setattr(ServiceApplication, _name,
            _transaction(getattr(ServiceApplication, _name), _name))
