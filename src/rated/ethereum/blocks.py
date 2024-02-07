from __future__ import annotations

from typing import Iterator, Any, Dict

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import Block


class Blocks(APIResource):
    path = "/blocks"

    def all(
        self,
        *,
        from_slot: int | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[Block]:
        params: Dict[str, Any] = {"from": from_slot, "size": size}
        return self.client.yield_paginated_results(
            self.resource_path,
            params=params,
            cls=Block,
            follow_next=follow_next,
        )

    def by_slot(self, slot: int) -> Block:
        data = self.client.get(f"{self.resource_path}/{slot}")
        return json_to_instance(data, Block)
