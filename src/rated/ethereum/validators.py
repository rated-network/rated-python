from __future__ import annotations

from datetime import date
from typing import Iterator, Dict, Any, List, Sequence, Union

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import (
    ValidatorAPR,
    ValidatorMetadata,
    ValidatorEffectiveness,
)
from rated.ethereum.enums import (
    AprType,
    TimeWindow,
    IdType,
    FilterType,
    Granularity,
    ValidatorsEffectivenessGroupBy,
)


class Validator(APIResource):
    path = "/validators"

    def metadata(self, index_or_pubkey: int | str) -> ValidatorMetadata:
        """
        Reverse lookup into the entity-to-validator index mappings that live in the RatedDB

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> metadata = eth.validator.metadata(560000)
            >>> print(f"{metadata.validator_pubkey = }, {metadata.deposit_addresses = }")

        Args:
            index_or_pubkey: Validator index or pubkey

        Returns:
            Metadata about the validator
        """
        validator = self.client.get(f"{self.resource_path}/{index_or_pubkey}")
        return json_to_instance(validator, ValidatorMetadata)

    def apr(
        self,
        index_or_pubkey: int | str,
        *,
        apr_type: AprType = AprType.BACKWARD,
        time_window: TimeWindow = TimeWindow.ONE_DAY,
    ) -> ValidatorAPR:
        """
        Historical data on the returns of a validator index

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> validator_apr = eth.validator.apr(560000, time_window=TimeWindow.THIRTY_DAYS)
            >>> print(f"{validator_apr.validator_index = }, {validator_apr.percentage = }%")

        Args:
            index_or_pubkey: Validator index or pubkey
            apr_type: Direction of flow
            time_window: The time window of aggregation

        Returns:
            APR %
        """
        params = {"aprType": apr_type.value, "window": time_window.value}
        apr = self.client.get(
            f"{self.resource_path}/{index_or_pubkey}/apr",
            params=params,
        )
        return json_to_instance(apr, ValidatorAPR)

    def effectiveness(
        self,
        index_or_pubkey: int | str,
        *,
        from_day: int | date | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[ValidatorEffectiveness]:
        """
        Historical performance of a single validator index

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> effectiveness = eth.validator.effectiveness(560000, from_day=795)
            >>> for eff in effectiveness:
            >>>     print(f"{eff.validator_index = }, {eff.validator_effectiveness = }")

        Args:
            index_or_pubkey: Validator index or pubkey
            from_day: Starting day
            size: Number of results included per page
            follow_next: Whether to follow pagination or not

        Yields:
            Effectiveness metrics
        """
        from_: str | int | date | None = from_day
        if from_ is not None and isinstance(from_, date):
            from_ = from_.isoformat()

        params: Dict[str, Any] = {"from": from_, "size": size}
        url = f"{self.resource_path}/{index_or_pubkey}/effectiveness"
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=ValidatorEffectiveness,
            follow_next=follow_next,
        )


class Validators(APIResource):
    path = "/validators"

    def metadata(
        self,
        *,
        from_index: int = 0,
        size: int = 100,
        operators_ids: List[str] | None = None,
        withdrawal_address: str | None = None,
        id_type: IdType = IdType.NODE_OPERATOR,
        follow_next: bool = False,
    ) -> Iterator[ValidatorMetadata]:
        """
        Allows users to request metadata for a group of validators that map to the same operator or pool

        Args:
            from_index: Starting validator index
            size: Number of results included per page
            operators_ids: An array of entities names you want to filter by
            withdrawal_address: Filter by the withdrawal address
            id_type: The type of entity class you would like to filter by
            follow_next: Whether to follow pagination or not

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> metadata = eth.validators.metadata(operators_ids=["Lido", "Kiln"])
            >>> for m in metadata:
            >>>     print(f"{m.validator_pubkey = }, {m.deposit_addresses = }, {m.node_operators = }")

        Yields:
            Validator metadata
        """
        url = f"{self.resource_path}"
        params: Dict[str, Any] = {
            "from": from_index,
            "size": size,
            "operators_ids": operators_ids,
            "withdrawal_address": withdrawal_address,
            "id_type": id_type.value,
        }
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=ValidatorMetadata,
            follow_next=follow_next,
        )

    def effectiveness(
        self,
        *,
        pubkeys: List[str] | None = None,
        indices: List[int] | None = None,
        from_day: int | date | None = None,
        to_day: Union[int, date] | None = None,
        filter_type: FilterType = FilterType.DAY,
        size: int = 10,
        granularity: Granularity = Granularity.NONE,
        group_by: ValidatorsEffectivenessGroupBy = ValidatorsEffectivenessGroupBy.VALIDATOR,
        follow_next: bool = False,
    ) -> Iterator[ValidatorEffectiveness]:
        """
        Enables the aggregation of all the metrics that live under Validators across an arbitrary number of validator
        indices or pubkeys

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> effectiveness = eth.validators.effectiveness(indices=[500, 501, 502], from_day=795)
            >>> for eff in effectiveness:
            >>>     print(f"{eff.validator_index = }, {eff.validator_effectiveness = }")

        Args:
            pubkeys: Array of pubkeys
            indices: Array of indices
            from_day: Start day
            to_day: End day
            filter_type: Type of filter to apply to from
            size: Number of results included per page
            granularity: The size of time increments you are looking to query
            group_by: Time window or validator; we either group by validator index or across time
            follow_next: Whether to follow pagination or not

        Yields:
            Effectiveness metrics
        """
        from_: str | int | date | None = from_day
        if from_ is not None and isinstance(from_, date):
            from_ = from_.isoformat()

        to_: str | int | date | None = to_day
        if to_ is not None and isinstance(to_, date):
            to_ = to_.isoformat()

        if not pubkeys and not indices:
            raise ValueError("Either pubkeys or indices must be specified")

        if pubkeys and indices:
            raise ValueError("Cannot specify both pubkeys and indices")

        params: Dict[str, Any] = {
            "pubkeys": pubkeys,
            "indices": indices,
            "from": from_,
            "to": to_,
            "filterType": filter_type.value,
            "size": size,
            "granularity": granularity.value,
            "groupBy": group_by.value,
        }
        url = f"{self.resource_path}/effectiveness"
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=ValidatorEffectiveness,
            follow_next=follow_next,
        )

    def report(self, validators: Sequence[str], *, pool_tag: str | None = None) -> int:
        """
        Gateway for node operators to "upload" their sets

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> validator_count = eth.validators.report(["0x...", "0x...", ...], pool_tag="ACME")

        Args:
            validators: Array of validator pubkeys associated with the node operator
            pool_tag: Pool name as they appear in the Rated Explorer

        Returns:
            Number of accepted validators
        """
        url = "/v0/selfReports/validators"
        data = {"validators": validators, "poolTag": pool_tag}
        res = self.client.post(url, json=data)
        count = len(res.json()["validators"])
        return count
