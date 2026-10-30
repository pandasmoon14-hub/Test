"""Opt-in noncanonical Tarrow shared-life fixture, not a migrated campaign.

The three specialist profiles use the same actual entities/stock and clock.
No past journals are combined and no new domain law is declared.
"""
from dataclasses import dataclass

from astra_runtime.myravant_tarrow_activity import ActivityFixture, create_activity_fixture


@dataclass(frozen=True)
class SharedCampaignFixture(ActivityFixture):
    @property
    def locality_help(self):
        return (
            "Shared local campaign: one saved world combines existing finite "
            "activities, structures, liquids, voluntary service, and inquiry. "
            "Recall <admitted subject> <facet>; compare reports about "
            "<admitted subject> <facet>. Reports are admitted history, not "
            "current truth or access to another actor's private memory. "
            "Service is one explicitly voluntary Tali profile, not an economy. "
            "Save and restore using --locality tarrow-shared. Old profiles "
            "remain separate and cannot be imported.\n" + super().locality_help
        )


def create_shared_campaign_fixture(*, activity_case="standard", structures_case="standard"):
    original = create_activity_fixture(activity_case=activity_case,
                                       structures_case=structures_case,
                                       shared_campaign=True)
    return SharedCampaignFixture(**original.__dict__)
