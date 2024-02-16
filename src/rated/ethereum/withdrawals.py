from __future__ import annotations

from datetime import date
from typing import Iterator, Dict, Any

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import Withdrawal


class Withdrawals(APIResource):
    """Offers a view into the future, relating to when a set of withdrawals are expected to land"""

    path = "/withdrawals"

    def by_operator(
        self,
        operator_id: str,
        *,
        from_day: int | date | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[Withdrawal]:
        """
        Retrieve information about the expectation of a withdrawal fulfilment, on a per validator index level

        Args:
            operator_id: The name of the entity in question
            from_day: Starting day
            size: Number of results included per page
            follow_next: Whether to follow pagination or not

        Yields:
            Withdrawal
        """
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
        """
        Returns all the validators that are expected to withdraw by slot

        Args:
            slot: Withdrawal slot number

        Yields:
            Withdrawal
        """
        url: str = f"{self.resource_path}/predicted/slot/{slot}"
        data = self.client.get(url)
        for item in data:
            yield json_to_instance(item, Withdrawal)
