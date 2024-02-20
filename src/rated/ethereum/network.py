from typing import Iterator, Dict, Any

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import (
    NetworkStats,
    NetworkOverview,
    NetworkChurnCapacity,
    NetworkChurnCapacityPool,
)
from rated.ethereum.enums import StakeAction, TimeWindow


class Network(APIResource):
    """
    Network allows querying into a collection of statistics that provide an overview of the whole network in historical
    states, which can be as recent as the last 24h.
    """

    path = "/network"

    def stats(self) -> Iterator[NetworkStats]:
        """
        Summarizes key performance statistics for all the whole network, for the current calendar day.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> network_stats = eth.network.stats()
            >>> for stat in network_stats:
            >>>     print(f"{stat.avg_uptime = }")

        Yields:
            Network performance stats
        """
        data = self.client.get(f"{self.resource_path}/stats")
        for item in data:
            yield json_to_instance(item, NetworkStats)

    def overview(self) -> Iterator[NetworkOverview]:
        """
        Summarizes key statistics for the whole network.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> overview = eth.network.overview()
            >>> for values in overview:
            >>>     print(f"{values.activating_validators = }")

        Yields:
            Statistics summary
        """
        data = self.client.get(f"{self.resource_path}/overview")
        for item in data:
            yield json_to_instance(item, NetworkOverview)

    def capacity(self) -> Iterator[NetworkChurnCapacity]:
        """
        Summarizes activations and exits for all the whole network.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> capacity = eth.network.capacity()
            >>> for cap in capacity:
            >>>     print(f"{cap.churn_limit = }")

        Yields:
            Activations and exits summary
        """
        data = self.client.get(f"{self.resource_path}/capacity")
        for item in data:
            yield json_to_instance(item, NetworkChurnCapacity)

    def capacity_pool(
        self,
        *,
        stake_action: StakeAction = StakeAction.ACTIVATION,
        time_window: TimeWindow = TimeWindow.ONE_DAY,
    ) -> Iterator[NetworkChurnCapacityPool]:
        """
        Summarizes activations and exits, broken down by staking pool.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> capacity_pool = eth.network.capacity_pool(time_window=TimeWindow.THIRTY_DAYS)
            >>> for cap in capacity_pool:
            >>>     print(f"{cap.churn_limit = }")

        Args:
            stake_action: Direction of flow. This can be either of activation or exit.
            time_window: The time window of aggregation. You might ask for 1d, 7d, 30d or All-time data

        Yields:
            An iterator over all results
        """
        params: Dict[str, Any] = {
            "stakeAction": stake_action.value,
            "window": time_window.value,
        }
        data = self.client.get(f"{self.resource_path}/capacity/pool", params=params)
        for item in data:
            yield json_to_instance(item, NetworkChurnCapacityPool)
