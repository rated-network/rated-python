from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterator, List

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import (
    Operator as OperatorType,
    OperatorEffectiveness,
    ClientPercentage,
    RelayerPercentage,
    OperatorApr,
    OperatorSummary,
    OperatorStakeMovement,
    Percentile,
)
from rated.ethereum.enums import (
    IdType,
    Granularity,
    FilterType,
    TimeWindow,
    AprType,
    StakeAction,
    PoolType,
)


class Operator(APIResource):
    path = "/operators"

    def metadata(self, operator_id, *, id_type: IdType = IdType.NONE) -> OperatorType:
        url: str = f"{self.resource_path}/{operator_id}"
        params: Dict[str, Any] = {"idType": id_type.value}
        operator = self.client.get(url, params=params)
        return json_to_instance(operator, OperatorType)

    def effectiveness(
        self,
        operator_id,
        *,
        id_type: IdType = IdType.NONE,
        from_day: int | date | None = None,
        size: int | None = None,
        granularity: Granularity = Granularity.DAY,
        filter_type: FilterType = FilterType.DAY,
        include: List[str] | None = None,
        follow_next: bool = False,
    ) -> Iterator[OperatorEffectiveness]:
        url: str = f"{self.resource_path}/{operator_id}/effectiveness"
        params: Dict[str, Any] = {
            "idType": id_type.value,
            "from": from_day,
            "size": size,
            "granularity": granularity.value,
            "filterType": filter_type.value,
            "include": include,
        }
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=OperatorEffectiveness,
            follow_next=follow_next,
        )

    def clients(
        self,
        operator_id,
        *,
        id_type: IdType = IdType.NONE,
    ) -> Iterator[ClientPercentage]:
        url: str = f"{self.resource_path}/{operator_id}/clients"
        params: Dict[str, Any] = {"idType": id_type.value}
        data = self.client.get(url, params=params)
        for item in data:
            yield json_to_instance(item, ClientPercentage)

    def relayers(
        self,
        operator_id,
        *,
        id_type: IdType = IdType.NONE,
        time_window: TimeWindow = TimeWindow.THIRTY_DAYS,
    ) -> Iterator[RelayerPercentage]:
        url: str = f"{self.resource_path}/{operator_id}/relayers"
        params: Dict[str, Any] = {"idType": id_type.value, "window": time_window.value}
        data = self.client.get(url, params=params)
        for item in data:
            yield json_to_instance(item, RelayerPercentage)

    def apr(
        self,
        operator_id,
        *,
        id_type: IdType = IdType.NONE,
        time_window: TimeWindow,
        apr_type: AprType = AprType.BACKWARD,
    ) -> OperatorApr:
        url: str = f"{self.resource_path}/{operator_id}/apr"
        params: Dict[str, Any] = {
            "idType": id_type.value,
            "window": time_window.value,
            "aprType": apr_type.value,
        }
        data = self.client.get(url, params=params)
        return json_to_instance(data, OperatorApr)

    def summary(
        self,
        operator_id,
        *,
        id_type: IdType = IdType.NONE,
        time_window: TimeWindow,
    ) -> OperatorSummary:
        url: str = f"{self.resource_path}/{operator_id}/summary"
        params: Dict[str, Any] = {
            "idType": id_type.value,
            "window": time_window.value,
        }
        data = self.client.get(url, params=params)
        return json_to_instance(data, OperatorSummary)

    def stake_movement(
        self,
        operator_id,
        *,
        id_type: IdType = IdType.NONE,
        stake_action: StakeAction = StakeAction.ACTIVATION,
        time_window: TimeWindow,
    ) -> Iterator[OperatorStakeMovement]:
        url: str = f"{self.resource_path}/{operator_id}/stakeMovement"
        params: Dict[str, Any] = {
            "idType": id_type.value,
            "stakeAction": stake_action.value,
            "window": time_window.value,
        }
        data = self.client.get(url, params=params)
        for item in data:
            yield json_to_instance(item, OperatorStakeMovement)


class Operators(APIResource):
    path = "/operators"

    def percentiles(
        self,
        *,
        id_type: IdType = IdType.NONE,
        time_window: TimeWindow,
    ) -> Iterator[Percentile]:
        url: str = f"{self.resource_path}/percentiles"
        params: Dict[str, Any] = {
            "idType": id_type.value,
            "window": time_window.value,
        }
        data = self.client.get(url, params=params)
        for item in data:
            yield json_to_instance(item, Percentile)

    def summaries(
        self,
        *,
        time_window: TimeWindow,
        pool_type: PoolType = PoolType.ALL,
        id_type: IdType = IdType.DEPOSIT_ADDRESS,
        parent_id: str | None = None,
        from_day: int | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[OperatorSummary]:
        url: str = f"{self.resource_path}"
        params: Dict[str, Any] = {
            "poolType": pool_type.value,
            "idType": id_type.value,
            "parentId": parent_id,
            "window": time_window.value,
            "from": from_day,
            "size": size,
        }
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=OperatorSummary,
            follow_next=follow_next,
        )
