"""P1: one bounded continuing world using existing authoritative procedures.

Application inheritance is cooperative: structures/surface water/finite activity,
service commitment, investigation projection and underlying actor/time/material
owners operate on the SAME in-memory representation, clock and journal.
Neither this adapter nor a freeform interpreter owns their outcomes.
"""
from astra_runtime.myravant_activity_application import ActivityApplication
from astra_runtime.myravant_service_application import (
    ServiceApplication, SERVICE_METHODS, execute_service_locality_request,
)
from astra_runtime.myravant_investigation_application import InvestigationApplication
from astra_runtime.myravant_tarrow_investigation import (
    parse_investigation_request, execute_investigation_request,
)
from astra_runtime.myravant_tarrow_activity import execute_activity_request
from astra_runtime.myravant_shared_campaign import create_shared_campaign_fixture


class SharedCampaignApplication(ActivityApplication, ServiceApplication,
                                InvestigationApplication):
    """Opt-in, versioned intersection of existing qualified player capabilities."""

    checkpoint_format = "myravant.shared-tarrow-activity-service-investigation-journal"
    replay_methods = tuple(dict.fromkeys(
        (*ActivityApplication.replay_methods, *SERVICE_METHODS)
    ))

    @staticmethod
    def default_fixture():
        return create_shared_campaign_fixture()

    def _checkpoint_profile(self):
        return {
            "shared_binding": "tarrow-shared-1",
            "included": ("activity", "structures", "surface-water", "service",
                         "investigation", "actors", "time", "material"),
            "owners": super()._checkpoint_profile(),
        }


def execute_shared_campaign_request(application, raw):
    """Public specialty routing without duplicate execution or a new resolver."""
    if parse_investigation_request(raw) is not None:
        return execute_investigation_request(application, raw)
    serviced = execute_service_locality_request(application, raw)
    if serviced is not None:
        return serviced
    return execute_activity_request(application, raw)
