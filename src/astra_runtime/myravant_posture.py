"""Approved #534: profile-scoped AFQR-16 configuration, not universal anatomy.

Profiles and opportunities are explicit noncanonical fixture inputs. Changing a
configuration neither moves an entity nor advances WORLD-2. AFQR-19 consumers
must separately qualify any consequence of the recorded configuration.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from astra_runtime.kernel.command_envelope import create_command_envelope
from astra_runtime.kernel.record_identity import build_record_id
from astra_runtime.kernel.state_delta import create_state_delta_envelope
from astra_runtime.kernel.transaction_preview import create_transaction_preview


class PostureError(ValueError):
    """Unsupported profile, opportunity, stale state, or replay evidence."""


def _digest(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode()).hexdigest()


def _text(value):
    return type(value) is str and bool(value.strip())


def _sha(value):
    return type(value) is str and len(value) == 64 and all(
        c in "0123456789abcdef" for c in value
    )


@dataclass(frozen=True, kw_only=True)
class PostureProfile:
    actor_id: str
    profile_id: str
    version: int
    configurations: tuple[str, ...]
    # AFQR-19 opportunity declarations, not inferred floor/support geometry.
    places: tuple[str, ...]

    def __post_init__(self):
        if (
            not _text(self.actor_id) or not _text(self.profile_id)
            or type(self.version) is not int or self.version < 1
            or type(self.configurations) is not tuple
            or not self.configurations
            or not all(_text(x) for x in self.configurations)
            or len(set(self.configurations)) != len(self.configurations)
            or type(self.places) is not tuple or not self.places
            or not all(_text(x) for x in self.places)
            or len(set(self.places)) != len(self.places)
        ):
            raise PostureError("invalid explicit posture profile")


@dataclass(frozen=True, kw_only=True)
class PostureMovementLicense:
    source_place_id: str
    direction: str
    method: str
    profile_id: str
    version: int
    configurations: tuple[str, ...]


@dataclass(frozen=True)
class PostureEvent:
    command_id: str
    actor_id: str
    profile_id: str
    profile_version: int
    profile_digest: str
    before: str | None
    after: str
    place_id: str
    representation_digest: str
    movement_count: int
    logical_step: int
    pre_digest: str
    post_digest: str
    fingerprint: str
    preview_id: str
    receipt_id: str
    state_delta_id: str


@dataclass(frozen=True)
class PostureState:
    events: tuple[PostureEvent, ...] = ()

    def __post_init__(self):
        if type(self.events) is not tuple or any(
            type(e) is not PostureEvent for e in self.events
        ) or len({e.command_id for e in self.events}) != len(self.events):
            raise PostureError("invalid posture history")

    @property
    def configuration(self):
        return self.events[-1].after if self.events else None


def digest_posture(state):
    event = state.events[-1] if state.events else None
    return _digest({
        "owner": "AFQR-16", "revision": len(state.events),
        "actor_id": event.actor_id if event else None,
        "profile_id": event.profile_id if event else None,
        "profile_version": event.profile_version if event else None,
        "configuration": state.configuration,
    })


def digest_posture_profile(profile):
    return _digest(asdict(profile))


def execute_posture(
    *, state, profile, command_id, actor_id, configuration, place_id,
    representation_digest, movement_count, logical_step, expected_pre_digest,
):
    if type(state) is not PostureState or type(profile) is not PostureProfile:
        raise PostureError("missing posture state or profile")
    if (
        actor_id != profile.actor_id or configuration not in profile.configurations
        or place_id not in profile.places or not _sha(representation_digest)
        or type(movement_count) is not int or movement_count < 0
        or type(logical_step) is not int or logical_step < 0
        or not _text(command_id)
    ):
        raise PostureError("configuration or current opportunity is not qualified")
    for event in state.events:
        if event.command_id == command_id:
            if (
                event.actor_id, event.profile_id, event.profile_version,
                event.profile_digest, event.after, event.place_id, event.representation_digest,
                event.movement_count, event.logical_step, event.pre_digest,
            ) != (
                actor_id, profile.profile_id, profile.version, digest_posture_profile(profile), configuration,
                place_id, representation_digest, movement_count, logical_step,
                expected_pre_digest,
            ):
                raise PostureError("posture command identity reused for different intent")
            return state, event
    if command_id != f"terminal-posture-{len(state.events) + 1:06d}":
        raise PostureError("invalid posture command sequence")
    if digest_posture(state) != expected_pre_digest:
        raise PostureError("stale posture state")
    if state.events:
        previous = state.events[-1]
        if (
            previous.actor_id != actor_id
            or previous.profile_id != profile.profile_id
            or previous.profile_version != profile.version
            or previous.profile_digest != digest_posture_profile(profile)
            or previous.movement_count > movement_count
            or previous.logical_step > logical_step
        ):
            raise PostureError("posture profile or chronology changed")
    if state.configuration == configuration:
        return state, None  # truthful observation, no manufactured transition
    post_digest = _digest({
        "owner": "AFQR-16", "revision": len(state.events) + 1,
        "actor_id": actor_id, "profile_id": profile.profile_id,
        "profile_version": profile.version, "configuration": configuration,
    })
    material = dict(
        command_id=command_id, actor_id=actor_id, profile_id=profile.profile_id,
        profile_version=profile.version, profile_digest=digest_posture_profile(profile), before=state.configuration,
        after=configuration, place_id=place_id,
        representation_digest=representation_digest,
        movement_count=movement_count, logical_step=logical_step,
        pre_digest=expected_pre_digest, post_digest=post_digest,
    )
    fingerprint = _digest(material)
    token = fingerprint[:28]
    command = create_command_envelope(
        command_id=command_id, command_type="interact", source_actor_id=actor_id,
        payload={"configuration": configuration},
        metadata={"package": "PLAY-POSTURE-MOVEMENT-1", "profile": profile.profile_id,
                  "profile_version": profile.version},
    )
    preview = create_transaction_preview(
        preview_id=build_record_id("posture_preview", token), command=command,
        metadata={"semantic_owner": "AFQR-16", "mutation_performed": False},
    )
    delta = create_state_delta_envelope(
        delta_id=build_record_id("posture_delta", token),
        source_command_id=command_id, source_preview_id=preview.preview_id,
        affected_record_ids=(actor_id,), change_type="record_update",
        payload=material,
        metadata={"semantic_owner": "AFQR-16", "opportunity_owner": "AFQR-19",
                  "transition_owner": "AFQR-01"},
    )
    event = PostureEvent(
        **material, fingerprint=fingerprint, preview_id=preview.preview_id,
        receipt_id=build_record_id("posture_receipt", token), state_delta_id=delta.delta_id,
    )
    return PostureState((*state.events, event)), event


def serialize_posture(state):
    return {"owner": "AFQR-16", "version": 1,
            "events": [asdict(e) for e in state.events]}


def restore_posture(material, *, profile):
    if (
        type(material) is not dict or set(material) != {"owner", "version", "events"}
        or material["owner"] != "AFQR-16" or type(material["version"]) is not int
        or material["version"] != 1 or type(material["events"]) is not list
        or not material["events"]
    ):
        raise PostureError("invalid activated posture component")
    state = PostureState()
    for raw in material["events"]:
        if type(raw) is not dict or set(raw) != set(PostureEvent.__dataclass_fields__):
            raise PostureError("invalid posture event")
        try:
            event = PostureEvent(**raw)
            state, replayed = execute_posture(
                state=state, profile=profile, command_id=event.command_id,
                actor_id=event.actor_id, configuration=event.after, place_id=event.place_id,
                representation_digest=event.representation_digest,
                movement_count=event.movement_count, logical_step=event.logical_step,
                expected_pre_digest=digest_posture(state),
            )
        except (TypeError, ValueError) as exc:
            raise PostureError("posture history cannot replay") from exc
        if replayed is None or _digest(asdict(event)) != _digest(asdict(replayed)):
            raise PostureError("posture replay evidence differs")
    return state


# Surface words are proposals to a profile. This is not a universal body enum.
POSTURE_PHRASES = {
    "stand": "standing", "stand up": "standing", "crouch": "crouching",
    "crouch down": "crouching", "kneel": "kneeling", "kneel down": "kneeling",
    "sit": "sitting", "sit down": "sitting", "lie down": "lying",
}


def parse_posture(raw_text):
    return POSTURE_PHRASES.get(" ".join(raw_text.strip().casefold().split()))
