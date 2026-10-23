"""Approved #561: reusable noncanonical work partitions, screens, and cover.

No new structure state: material support and connection records remain the
authority. Environmental drying consumes a qualified, current material handoff.
The profile is a local fixture contract, not general weather/load/roof physics.
"""
from dataclasses import asdict, dataclass
from fractions import Fraction

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_tarrow import identity
from astra_runtime.myravant_tarrow_surface_water import SurfaceFixture, create_surface_fixture


@dataclass(frozen=True)
class CoverExposure:
    cover: str
    anchor: str
    fastener: str
    support: str
    absorbents: tuple[str, ...]
    rate: Fraction = Fraction(1, 4)
    method: str = "tie"

    def validate(self, fixture):
        material = fixture.material_profile
        objects = {p.entity_id for p in fixture.object_presentations}
        if (len({self.cover, self.anchor, self.fastener, self.support}) != 4
                or not {self.cover, self.anchor, self.fastener, self.support} <= objects
                or not self.absorbents or len(set(self.absorbents)) != len(self.absorbents)
                or not set(self.absorbents) <= set(fixture.environment_profile.absorbents)
                or type(self.rate) is not Fraction or self.rate != Fraction(1, 4)
                or self.method != "tie"
                or (self.cover, self.support) not in material.support_pairs
                or (self.anchor, self.support) not in material.support_pairs
                or (self.cover, self.anchor, self.fastener, self.method) not in material.fastening_pairs
                or any((subject, self.support) not in material.support_pairs for subject in self.absorbents)):
            raise ValueError("invalid qualified cover material/exposure declaration")


@dataclass(frozen=True)
class StructuresFixture(SurfaceFixture):
    cover_profile: CoverExposure | None = None
    structures_case: str = "standard"

    @property
    def locality_help(self):
        return ("Configurable structures (development profile): assemble a work partition "
                "using Work Panel, Barrier Crossbar and Work Cord on Yard Work Trestle; "
                "untie, lift and reuse the SAME panel and cord for a work screen at "
                "Document Box and Notice Board. These arrangements separately affect "
                "declared passage and sightline. A different Cover Cloth and Cover Tie "
                "can make a qualified drying cover over the trestle when tied to the "
                "supported crossbar. Only declared absorbents supported there dry at "
                "the 1/4 interval cover rate; no load, roof, rain, sealing, force or "
                "ambient water behavior is implied. 'Start assembling work partition', "
                "'start assembling work screen' and 'start assembling drying cover' "
                "create optional multi-step work intentions; each step still requires "
                "real component access.\n" + super().locality_help)


def cover_subjects(representation, connections, profile):
    """Return ONLY actual supported absorbents under a live whole-part cover."""
    if (placement(representation, profile.cover).relation_type != "supported_by"
            or placement(representation, profile.cover).object_entity_id != profile.support
            or placement(representation, profile.anchor).relation_type != "supported_by"
            or placement(representation, profile.anchor).object_entity_id != profile.support
            or not any((c.left, c.right, c.fastener, c.method)
                       == (profile.cover, profile.anchor, profile.fastener, profile.method)
                       for c in connections)):
        return ()
    return tuple(subject for subject in profile.absorbents
                 if placement(representation, subject).relation_type == "supported_by"
                 and placement(representation, subject).object_entity_id == profile.support)


def create_structures_fixture(*, structures_case="standard"):
    if type(structures_case) is not str or structures_case not in {"standard", "cross-workshop"}:
        raise ValueError("unknown declared structure configuration")
    parent = create_surface_fixture(structure_case=structures_case)
    cover = CoverExposure(identity("cover-cloth"), identity("barrier-crossbar"),
                          identity("cover-tie"), identity("trestle"),
                          (identity("cleaning-cloth"), identity("packing-felt")))
    result = StructuresFixture(**parent.__dict__, cover_profile=cover,
                               structures_case=structures_case)
    cover.validate(result)
    return result


def execute_structures_request(application, raw):
    from astra_runtime.myravant_surface_water_application import execute_surface_water_request
    return execute_surface_water_request(application, raw)
