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
    """
    Allows one to see every slashed validator in the Ethereum Beacon Chain whether individually or collectively.
    Pertinent metrics include their total penalties from being slashed,
    which epoch they were slashed, and when they will be withdrawable.
    """

    path = "/slashings"

    def overview(self) -> Iterator[SlashingOverview]:
        """
        Lists of all slashed validators, their index, pubkey, slashing epoch, withdrawable epoch,
        balance before slashing, balance before withdrawal, and the penalties incurred from getting slashed.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> slashings_overview = eth.slashings.overview()
            >>> for slashing in slashings_overview:
            >>>     print(f"{slashing.validators_slashed = }")

        Yields:
            Slashing overview
        """
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
        """
        Depending on the slashing role specified, this endpoint returns a list of entities either
        (1) according to how many times their validators have been slashed or
        (2) how many times their validators have proposed a block that included slashing report
           (i.e. letting the network know a slashing incident has occurred)

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> leaderboard = eth.slashings.leaderboard(from_rank=1)
            >>> for l in leaderboard:
            >>>     print(f"{l.id = }, {l.slashes = }, {l.validator_count = }")

        Args:
            from_rank: Start from ranking
            size: Number of results included per page
            follow_next: Whether to follow pagination or not

        Yields:
            Slashing leaderboard
        """
        url: str = f"{self.resource_path}/leaderboard"
        params = {"from": from_rank, "size": size}
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=SlashingLeaderboard,
            follow_next=follow_next,
        )

    def cohorts(self) -> Iterator[SlashingCohort]:
        """
        Retrieves the frequency of slashing incidents for validators, grouped by different operator cohort sizes,
        from solo to professional operators with more than 5,000 validator keys.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> cohorts = eth.slashings.cohorts()
            >>> for cohort in cohorts:
            >>>     print(f"{cohort.cohort = }, {cohort.last_six_months = }")

        Yield:
            Cohorts
        """
        url: str = f"{self.resource_path}/cohortAnalysis"
        data = self.client.get(url)
        for item in data:
            yield json_to_instance(item, SlashingCohort)

    def timeseries(self) -> Iterator[SlashingTimeInterval]:
        """
        Time series of slashing incidents

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> intervals = eth.slashings.timeseries()
            >>> for interval in intervals:
            >>>     print(f"{interval.month = }, {interval.validators_slashed = }")

        Yields:
            Slashing time series
        """
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
        """
        All slashed validators, their index, pubkey, slashing epoch, withdrawable epoch, balance before slashing,
        balance before withdrawal, and the penalties incurred from getting slashed

        Examples:
            >>> from datetime import date
            >>>
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> penalties = eth.slashings.penalties(from_day=date(2023, 10, 1), size=10)
            >>> for penalty in penalties:
            >>>     print(f"{penalty.validator_pubkey = }, {penalty.slashing_penalties = }")

        Args:
            from_day: Starting day
            size: Number of results included per page
            follow_next: Whether to follow pagination or not

        Yields:
            Slashing penalty

        """
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
    ) -> SlashingPenalty:
        """
        Information about a single slashed validator, queried either by the validator's index or their pubkey.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> penalties = eth.slashings.for_validator()
            >>> print(f"{penalties.slashing_epoch = }, {penalties.slashing_penalties = }")

        Args:
            validator_index_or_pubkey: Validator index or pubkey

        Returns:
            Slashing penalty
        """
        url: str = f"{self.resource_path}/{validator_index_or_pubkey}"
        data = self.client.get(url)
        return json_to_instance(data, SlashingPenalty)
