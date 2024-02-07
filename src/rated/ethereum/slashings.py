from __future__ import annotations

from datetime import date
from typing import Iterator, Dict, Any

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import (
    SlashingOverview,
    SlashingLeaderboard,
    SlashingCohort,
    SlashingTimeInterval,
    SlashingPenalty,
)


class Slashings(APIResource):
    path = "/slashings"

    def overview(self) -> Iterator[SlashingOverview]:
        url: str = f"{self.resource_path}/overview"
        data = self.client.get(url)
        for item in data:
            yield json_to_instance(item, SlashingOverview)

    def leaderboard(
        self,
        *,
        from_rank: int | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[SlashingLeaderboard]:
        url: str = f"{self.resource_path}/leaderboard"
        params = {"from": from_rank, "size": size}
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=SlashingLeaderboard,
            follow_next=follow_next,
        )

    def cohorts(self) -> Iterator[SlashingCohort]:
        url: str = f"{self.resource_path}/cohortAnalysis"
        data = self.client.get(url)
        for item in data:
            yield json_to_instance(item, SlashingCohort)

    def timeseries(self) -> Iterator[SlashingTimeInterval]:
        url: str = f"{self.resource_path}/timeseries"
        data = self.client.get(url)
        for item in data:
            yield json_to_instance(item, SlashingTimeInterval)

    def penalties(
        self,
        *,
        from_day: int | date | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[SlashingPenalty]:
        url: str = f"{self.resource_path}"
        from_: str | int | date | None = from_day
        if from_ is not None and isinstance(from_, date):
            from_ = from_.isoformat()
        params: Dict[str, Any] = {"from": from_, "size": size}
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=SlashingPenalty,
            follow_next=follow_next,
        )

    def for_validator(
        self,
        validator_index_or_pubkey: int | str,
    ) -> Iterator[SlashingPenalty]:
        url: str = f"{self.resource_path}/{validator_index_or_pubkey}"
        data = self.client.get(url)
        if not isinstance(data, list):
            data = [data]
        for item in data:
            yield json_to_instance(item, SlashingPenalty)
