from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterator

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
    """Querying into pre-materialized operator groupings."""

    path = "/operators"

    def metadata(
        self,
        operator_id: str,
        *,
        id_type: IdType = IdType.NONE,
    ) -> OperatorType:
        """
        Retrieve profile information on specific operators.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> op = eth.operator.metadata("Lido")
            >>> print(f"{op.node_operator_count = }")

        Args:
            operator_id: The name of the entity in question
            id_type: The type of entity class

        Returns:
            Operator metadata.
        """
        url: str = f"{self.resource_path}/{operator_id}"
        params: Dict[str, Any] = {"idType": id_type.value}
        operator = self.client.get(url, params=params)
        return json_to_instance(operator, OperatorType)

    def effectiveness(
        self,
        operator_id: str,
        *,
        id_type: IdType = IdType.NONE,
        from_day: int | date | None = None,
        size: int | None = None,
        granularity: Granularity = Granularity.DAY,
        filter_type: FilterType = FilterType.DAY,
        follow_next: bool = False,
    ) -> Iterator[OperatorEffectiveness]:
        """
        Historical performance of a single operator.
        This includes rewards (aggregate and granular), performance (effectiveness and its components),
        slashing history and much more.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> effectiveness = eth.operator.effectiveness("Lido", from_day=795, size=10)
            >>> for eff in effectiveness:
            >>>     print(f"{eff.avg_validator_effectiveness = }, {eff.day = }")

        Args:
            operator_id: The name of the entity in question
            id_type: The type of entity class
            from_day: Start day
            size: Number of results included per page
            granularity:T he size of time increments you are looking to query
            filter_type: Hour, day and datetime
            follow_next: Whether to follow pagination or not

        Yields:
            Operator Effectiveness
        """
        url: str = f"{self.resource_path}/{operator_id}/effectiveness"
        params: Dict[str, Any] = {
            "idType": id_type.value,
            "from": from_day,
            "size": size,
            "granularity": granularity.value,
            "filterType": filter_type.value,
        }
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=OperatorEffectiveness,
            follow_next=follow_next,
        )

    def clients(
        self,
        operator_id: str,
        *,
        id_type: IdType = IdType.NONE,
    ) -> Iterator[ClientPercentage]:
        """
        Consensus client distribution

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> clients = eth.operator.clients("Lido")
            >>> for c in clients:
            >>>     print(f"{c.client = }, {c.percentage = }%")

        Args:
            operator_id: The name of the entity in question
            id_type: The type of entity class

        Yields:
            Clients percentages
        """
        url: str = f"{self.resource_path}/{operator_id}/clients"
        params: Dict[str, Any] = {"idType": id_type.value}
        data = self.client.get(url, params=params)
        for item in data:
            yield json_to_instance(item, ClientPercentage)

    def relayers(
        self,
        operator_id: str,
        *,
        id_type: IdType = IdType.NONE,
        time_window: TimeWindow = TimeWindow.THIRTY_DAYS,
    ) -> Iterator[RelayerPercentage]:
        """
        Get information relating to an entity's historical distribution of relays they have procured blocks from.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> relayers = eth.operator.relayers("Lido", time_window=TimeWindow.ALL_TIME)
            >>> for r in relayers:
            >>>     print(f"{r.relayer = }, {r.percentage = }%")

        Args:
            operator_id: The name of the entity in question
            id_type: The type of entity class
            time_window: The time window of aggregation

        Yields:
            Relayer Percentages
        """
        url: str = f"{self.resource_path}/{operator_id}/relayers"
        params: Dict[str, Any] = {"idType": id_type.value, "window": time_window.value}
        data = self.client.get(url, params=params)
        for item in data:
            yield json_to_instance(item, RelayerPercentage)

    def apr(
        self,
        operator_id: str,
        *,
        id_type: IdType = IdType.NONE,
        time_window: TimeWindow,
        apr_type: AprType = AprType.BACKWARD,
    ) -> OperatorApr:
        """
        Retrieve historical data on the returns any of the entities supported have recorded.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> apr = eth.operator.apr("Lido", time_window=TimeWindow.ALL_TIME)
            >>> print(f"{apr.percentage = }%")

        Args:
            operator_id: The name of the entity in question
            id_type: The type of entity class
            time_window: The time window of aggregation
            apr_type: Direction of flow

        Returns:
            Entity APR %
        """
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
        operator_id: str,
        *,
        id_type: IdType = IdType.NONE,
        time_window: TimeWindow,
    ) -> OperatorSummary:
        """
        Retrieve summary statistics for a specific operator

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> summary = eth.operator.summary("Lido", time_window=TimeWindow.SEVEN_DAYS)
            >>> print(f"{summary.avg_uptime = }%")

        Args:
            operator_id: The name of the entity in question
            id_type: The type of entity class
            time_window: The time window of aggregation

        Returns:
            Operator summary
        """
        url: str = f"{self.resource_path}/{operator_id}/summary"
        params: Dict[str, Any] = {
            "idType": id_type.value,
            "window": time_window.value,
        }
        data = self.client.get(url, params=params)
        return json_to_instance(data, OperatorSummary)

    def stake_movement(
        self,
        operator_id: str,
        *,
        id_type: IdType = IdType.NONE,
        stake_action: StakeAction = StakeAction.ACTIVATION,
        time_window: TimeWindow,
    ) -> Iterator[OperatorStakeMovement]:
        """
        Retrieve data on the activation and exit activity of a specific pre-materialized view
        (e.g. operator, deposit address, etc.)

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> stake_movement = eth.operator.stake_movement("Lido", time_window=TimeWindow.THIRTY_DAYS)
            >>> for mov in stake_movement:
            >>>     print(f"{mov.amount_gwei = }")

        Args:
            operator_id: The name of the entity in question
            id_type: The type of entity class
            stake_action: Direction of flow
            time_window: The time window of aggregation

        Yields:
            Activations and withdrawals state and status

        """
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
        """
        Retrieve data of entities with their respective percentile rank score, according to their effectiveness rating.

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> percentiles = eth.operators.percentiles(time_window=TimeWindow.SEVEN_DAYS)
            >>> for percentile in percentiles:
            >>>     print(f"{percentile.rank = }, {percentile.value = }")

        Args:
            id_type: The type of entity class
            time_window: The time window of aggregation

        Yields:
            Percentiles

        See Also:
            https://docs.rated.network/methodologies/ethereum-beacon-chain/rating-percentiles

        """
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
        """
        Summarizes statistics for all the operators Rated has pre-materialized views on

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> summaries = eth.operators.summaries(time_window=TimeWindow.ALL_TIME, from_day=795, size=10)
            >>> for summary in summaries:
            >>>     print(f"{summary.avg_uptime = }")

        Args:
            time_window: The time window of aggregation
            pool_type: Type of Pool
            id_type: The type of entity class
            parent_id: Specifying a pool or node operator so that the response is focused on the Pool Shares of said entity
            from_day: Start day
            size: Number of results included per page
            follow_next: Whether to follow pagination or not

        Yields:

        """
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
