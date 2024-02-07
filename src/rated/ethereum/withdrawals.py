from __future__ import annotations

from datetime import date
from typing import Iterator, Dict, Any

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import Withdrawal


class Withdrawals(APIResource):
    path = "/withdrawals"

    def by_operator(
        self,
        operator_id: str,
        *,
        from_day: int | date | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[Withdrawal]:
        url: str = f"{self.resource_path}/predicted/operators/{operator_id}"
        from_: str | int | date | None = from_day
        if from_ is not None and isinstance(from_, date):
            from_ = from_.isoformat()

        params: Dict[str, Any] = {"from": from_, "size": size}
        return self.client.yield_paginated_results(
            url,
            params=params,
            cls=Withdrawal,
            follow_next=follow_next,
        )

    def by_slot(self, slot: int) -> Iterator[Withdrawal]:
        url: str = f"{self.resource_path}/predicted/slot/{slot}"
        data = self.client.get(url)
        for item in data:
            yield json_to_instance(item, Withdrawal)
