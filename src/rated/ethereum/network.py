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
    path = "/network"

    def stats(self) -> Iterator[NetworkStats]:
        data = self.client.get(f"{self.resource_path}/stats")
        for item in data:
            yield json_to_instance(item, NetworkStats)

    def overview(self) -> Iterator[NetworkOverview]:
        data = self.client.get(f"{self.resource_path}/overview")
        for item in data:
            yield json_to_instance(item, NetworkOverview)

    def capacity(self) -> Iterator[NetworkChurnCapacity]:
        data = self.client.get(f"{self.resource_path}/capacity")
        for item in data:
            yield json_to_instance(item, NetworkChurnCapacity)

    def capacity_pool(
        self,
        stake_action: StakeAction = StakeAction.ACTIVATION,
        time_window: TimeWindow = TimeWindow.ONE_DAY,
    ) -> Iterator[NetworkChurnCapacityPool]:
        params: Dict[str, Any] = {
            "stakeAction": stake_action.value,
            "window": time_window.value,
        }
        data = self.client.get(f"{self.resource_path}/capacity/pool", params=params)
        for item in data:
            yield json_to_instance(item, NetworkChurnCapacityPool)
