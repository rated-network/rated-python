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
        validator = self.client.get(f"{self.resource_path}/{index_or_pubkey}")
        return json_to_instance(validator, ValidatorMetadata)

    def apr(
        self,
        index_or_pubkey: int | str,
        *,
        apr_type: AprType = AprType.BACKWARD,
        time_window: TimeWindow = TimeWindow.ONE_DAY,
    ) -> ValidatorAPR:
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
        from_: int = 0,
        size: int = 100,
        operators_ids: List[str] | None = None,
        withdrawal_address: str | None = None,
        id_type: IdType = IdType.NODE_OPERATOR,
        follow_next: bool = False,
    ) -> Iterator[ValidatorMetadata]:
        url = f"{self.resource_path}"
        params: Dict[str, Any] = {
            "from": from_,
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
        url = "/v0/selfReports/validators"
        data = {"validators": validators, "poolTag": pool_tag}
        res = self.client.post(url, json=data)
        count = len(res.json()["validators"])
        return count
