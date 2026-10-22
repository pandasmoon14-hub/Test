"""PLAY-TARROW-SERVICE-1: opt-in personal service promises (issue #557 S1-S12).

This profile-local owner records disclosed/accepted terms and verifies attribution.
It never owns work, time, custody, property title, knowledge or enforcement.
All qualified evidence is supplied by those existing owners.
"""
from dataclasses import dataclass, replace
from astra_runtime.domain.persistent_world_material import digest


def _id(value):
    return type(value) is str and bool(value.strip()) and len(value) <= 512


@dataclass(frozen=True)
class ServiceTerms:
    version: int
    requester: str
    performer: str
    beneficiary: str
    target: str
    tool: str
    method: str
    peg: str
    recipient: str
    fingerprint: str

    def __post_init__(self):
        if type(self.version) is not int or self.version < 1:
            raise ValueError("positive offer version required")
        if not all(_id(x) for x in (self.requester, self.performer, self.beneficiary,
                                    self.target, self.tool, self.method, self.peg,
                                    self.recipient, self.fingerprint)):
            raise ValueError("service identity or terms fingerprint absent")
        if self.requester == self.performer or self.recipient != self.performer:
            raise ValueError("service parties must be distinct and explicit")
        if self.fingerprint != terms_fingerprint(self):
            raise ValueError("service terms fingerprint mismatch")


def terms_fingerprint(terms):
    return digest(("service-terms-1", terms.version, terms.requester, terms.performer,
                   terms.beneficiary, terms.target, terms.tool, terms.method, terms.peg,
                   terms.recipient))


def make_terms(*, version, requester, performer, beneficiary, target, tool, method, peg, recipient):
    values = dict(version=version, requester=requester, performer=performer,
                  beneficiary=beneficiary, target=target, tool=tool, method=method,
                  peg=peg, recipient=recipient)
    return ServiceTerms(**values, fingerprint=digest(("service-terms-1", *values.values())))


@dataclass(frozen=True)
class ServiceRecord:
    terms: ServiceTerms
    offer_receipt: str
    state: str = "offered"
    decision_receipt: str | None = None
    task_id: str | None = None
    accepted_fingerprint: str | None = None
    work_receipts: tuple[str, ...] = ()
    completion_receipt: str | None = None
    custody_receipt: str | None = None
    withdrawal_receipt: str | None = None

    def __post_init__(self):
        if not _id(self.offer_receipt):
            raise ValueError("offer disclosure receipt required")
        if self.state not in {"offered", "declined", "superseded", "accepted",
                              "partial", "eligible", "withdrawn", "settled"}:
            raise ValueError("invalid service status")
        if len(set(self.work_receipts)) != len(self.work_receipts) or not all(_id(x) for x in self.work_receipts):
            raise ValueError("distinct work owner receipts required")
        if self.accepted_fingerprint is not None and self.accepted_fingerprint != self.terms.fingerprint:
            raise ValueError("accepted terms were altered")
        if self.state in {"accepted", "partial", "eligible", "withdrawn", "settled"}:
            if not all(_id(x) for x in (self.decision_receipt, self.task_id, self.accepted_fingerprint)):
                raise ValueError("accepted service lacks decision/task binding")
        if self.state in {"eligible", "settled"} and (not self.work_receipts or not _id(self.completion_receipt)):
            raise ValueError("eligibility needs attributable completed actor work")
        if self.state == "settled" and not _id(self.custody_receipt):
            raise ValueError("settlement needs real custody owner receipt")
        if self.custody_receipt is not None and self.state != "settled":
            raise ValueError("custody receipt cannot exist before settlement")
        if self.withdrawal_receipt is not None and self.state != "withdrawn":
            raise ValueError("withdrawal must be explicit")


@dataclass(frozen=True)
class ServiceState:
    history: tuple[ServiceRecord, ...] = ()

    def __post_init__(self):
        if type(self.history) is not tuple or any(type(r) is not ServiceRecord for r in self.history):
            raise ValueError("immutable service history required")
        if tuple(r.terms.version for r in self.history) != tuple(range(1, len(self.history) + 1)):
            raise ValueError("service versions must be sequential")
        if sum(r.state in {"offered", "accepted", "partial", "eligible"} for r in self.history) > 1:
            raise ValueError("only one unsettled active offer")


def latest(state):
    if not state.history:
        raise ValueError("no disclosed service offer")
    return state.history[-1]


def _replace_last(state, record):
    return ServiceState((*state.history[:-1], record))


def offer(state, terms, *, disclosure_receipt):
    if terms.version != len(state.history) + 1 or not _id(disclosure_receipt):
        raise ValueError("offer version or disclosure receipt invalid")
    history = state.history
    if history:
        old = history[-1]
        if old.state == "offered":
            history = (*history[:-1], replace(old, state="superseded"))
        elif old.state not in {"declined", "superseded", "withdrawn", "settled"}:
            raise ValueError("accepted service cannot be silently overwritten")
    return ServiceState((*history, ServiceRecord(terms, disclosure_receipt)))


def decide(state, *, version, fingerprint, accept, decision_receipt, task_id=None):
    old = latest(state)
    if old.state != "offered" or old.terms.version != version or old.terms.fingerprint != fingerprint:
        raise ValueError("stale or non-open offer")
    if type(accept) is not bool or not _id(decision_receipt):
        raise ValueError("explicit qualified voluntary response required")
    if accept and not _id(task_id):
        raise ValueError("acceptance must bind actual selected participation")
    record = replace(old, state="accepted" if accept else "declined",
                     decision_receipt=decision_receipt, task_id=task_id,
                     accepted_fingerprint=old.terms.fingerprint if accept else None)
    return _replace_last(state, record)


def reconcile(state, *, task, receipt_ids, completion_receipt=None):
    """Caller supplies authenticated selected actor task and committed owner receipts.

    Never infer work credit from a clean surface or from mere passage of time.
    """
    old = latest(state)
    if old.state not in {"accepted", "partial", "eligible"}:
        raise ValueError("service is not working")
    if (task.task_id != old.task_id or task.actor_id != old.terms.performer
            or task.source_actor_id != old.terms.requester or task.kind != "cleaning"
            or task.method != old.terms.method
            or task.participants != (old.terms.target, old.terms.tool)):
        raise ValueError("wrong actor, goal, tool or participation task")
    receipts = tuple(task.contributions)
    if not set(receipts) <= set(receipt_ids) or receipts[:len(old.work_receipts)] != old.work_receipts:
        raise ValueError("missing or changed physical work receipts")
    completed = task.status == "completed"
    if completed and (not receipts or completion_receipt not in receipts):
        raise ValueError("completion must be this actor's attributable contribution")
    if not completed and completion_receipt is not None:
        raise ValueError("cannot credit completion before task completion")
    if old.state == "eligible" and not completed:
        raise ValueError("completed contribution cannot be erased")
    if task.status == "withdrawn" and not completed:
        # A withdrawal receipt is supplied separately by the consent/control owner.
        return _replace_last(state, replace(old, state="partial" if receipts else "accepted",
                                            work_receipts=receipts))
    return _replace_last(state, replace(old, state="eligible" if completed else
                                       "partial" if receipts else "accepted",
                                       work_receipts=receipts,
                                       completion_receipt=completion_receipt if completed else None))


def withdraw(state, *, receipt):
    old = latest(state)
    if old.state not in {"accepted", "partial", "offered"} or not _id(receipt):
        raise ValueError("only an unsettled, incomplete voluntary service may withdraw")
    if old.state == "offered":
        return _replace_last(state, replace(old, state="declined", decision_receipt=receipt))
    return _replace_last(state, replace(old, state="withdrawn", withdrawal_receipt=receipt))


def settle(state, *, custody_receipt, actual_object, giver, recipient):
    old = latest(state)
    if old.state != "eligible":
        raise ValueError("named actor has not qualified full performance")
    if not _id(custody_receipt) or (actual_object, giver, recipient) != (
            old.terms.peg, old.terms.requester, old.terms.recipient):
        raise ValueError("no matching actual custody transfer")
    return _replace_last(state, replace(old, state="settled", custody_receipt=custody_receipt))


def canonical_state(state, *, receipt_ids=None, entity_ids=None):
    ServiceState(state.history)
    result = []
    all_receipts = set()
    for record in state.history:
        t = record.terms
        if entity_ids is not None and not {t.requester,t.performer,t.beneficiary,t.target,t.tool,t.peg,t.recipient} <= set(entity_ids):
            raise ValueError("service terms refer to unknown world identity")
        receipts = (record.offer_receipt, record.decision_receipt, *record.work_receipts,
                    record.custody_receipt, record.withdrawal_receipt)
        for receipt in receipts:
            if receipt is None:continue
            if receipt_ids is not None and receipt not in receipt_ids:
                raise ValueError("service owner evidence missing")
            if receipt in all_receipts:
                raise ValueError("service receipt reused")
            all_receipts.add(receipt)
        result.append({"terms":vars(t).copy(), "offer_receipt":record.offer_receipt,
                       "state":record.state, "decision_receipt":record.decision_receipt,
                       "task_id":record.task_id, "accepted_fingerprint":record.accepted_fingerprint,
                       "work_receipts":list(record.work_receipts),
                       "completion_receipt":record.completion_receipt,
                       "custody_receipt":record.custody_receipt,
                       "withdrawal_receipt":record.withdrawal_receipt})
    return {"history":result}
