from __future__ import annotations

from typing import Iterator

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import (
    P2PGeographicalDistribution,
    P2PHostingProviderDistribution,
)
from rated.ethereum.enums import DistributionType


class P2P(APIResource):
    """
    Querying into aggregated stats on Ethereum's peer-to-peer networking layer
    """

    path = "/p2p"

    def geographical_distribution(
        self,
        distribution_type: DistributionType = DistributionType.PROS,
    ) -> Iterator[P2PGeographicalDistribution]:
        """
        Retrieves a list of countries and the respective share of the validator set based in those countries

        Args:
            distribution_type: The type of distribution

        Yields:
            Geographical distribution
        """
        url = f"{self.resource_path}/geographical"
        params = {"distType": distribution_type.value}
        data = self.client.get(url, params=params)
        for item in data:
            yield json_to_instance(item, P2PGeographicalDistribution)

    def hosting_provider_distribution(
        self,
        *,
        from_rank: int | None = None,
        size: int | None = None,
        distribution_type: DistributionType = DistributionType.PROS,
        follow_next: bool = False,
    ) -> Iterator[P2PHostingProviderDistribution]:
        """
        Retrieves a list of hosting providers and their respective share of the validator set

        Args:
            from_rank:
            size: Number of results included per page
            distribution_type: The type of distribution
            follow_next: Whether to follow pagination or not

        Yields:
            Hosting provider distribution
        """
        url = f"{self.resource_path}/hostingProvider"
        params = {"from": from_rank, "size": size, "distType": distribution_type.value}
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=P2PHostingProviderDistribution,
            follow_next=follow_next,
        )
