"""#561 opt-in structures: existing material truth, one qualified environment handoff.

The live relation graph decides what is erected. Neither an intent, model nor
this adapter owns a separate constructed-state flag or environmental stock.
"""
from dataclasses import asdict
from fractions import Fraction

from astra_runtime.domain.persistent_world_material import placement
from astra_runtime.myravant_surface_water_application import SurfaceWaterApplication
from astra_runtime.myravant_tarrow_structures import create_structures_fixture, cover_subjects


class StructuresApplication(SurfaceWaterApplication):
    checkpoint_format = "myravant.structures-actor-time-material-owner-journal"

    @staticmethod
    def default_fixture():
        return create_structures_fixture()

    def _checkpoint_profile(self):
        return {"surface": super()._checkpoint_profile(),
                "cover": asdict(self.fixture.cover_profile),
                "structures_case": self.fixture.structures_case,
                "structures_version": "relationships-and-covered-absorbents-1"}

    def _validate_transaction(self):
        super()._validate_transaction()
        profile = getattr(self.fixture, "cover_profile", None)
        if profile is not None:
            profile.validate(self.fixture)
            # Validation inspects live owner placements and connections; a
            # disconnected cover is allowed, never represented as active.
            cover_subjects(self.state.representation, self.connections, profile)

    def _exposure_rate_overrides(self, exposures):
        profile = self.fixture.cover_profile
        qualifying = cover_subjects(self.state.representation, self.connections, profile)
        if not qualifying:
            return None
        # The clock is already committed t -> t+1 here. Conditions effective
        # at the beginning of the interval were those at t, not future ones.
        beginning = self.runtime_state.logical_time_state.logical_position - 1
        rates = {place: rate for place, rate, _ in self.environment_profile.exposures}
        for due, place, rate, _ in self.environment_profile.schedule:
            if due <= beginning:
                rates[place] = rate
        overrides = {}
        for subject in qualifying:
            place = exposures[subject]
            if place is not None:
                overrides[subject] = min(profile.rate, rates[place])
        return overrides or None


def execute_structures_request(application, raw):
    from astra_runtime.myravant_surface_water_application import execute_surface_water_request
    return execute_surface_water_request(application, raw)
