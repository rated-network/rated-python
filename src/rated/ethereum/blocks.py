from __future__ import annotations

from typing import Iterator, Any, Dict

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import Block


class Blocks(APIResource):
    """
    Blocks allows one to dig into the individual slots and blocks in Ethereum since the Merge.
    Metrics include validator rewards from the consensus and execution layers, MEV data, and missed reward estimates.
    """

    path = "/blocks"

    def all(
        self,
        *,
        from_slot: int | None = None,
        size: int | None = None,
        follow_next: bool = False,
    ) -> Iterator[Block]:
        """
        Get all blocks

        Args:
            from_slot: Start slot
            size: Number of results included per page
            follow_next: Whether to follow pagination or not

        Yields:
            An iterator over all blocks
        """
        params: Dict[str, Any] = {"from": from_slot, "size": size}
        return self.client.yield_paginated_results(
            self.resource_path,
            params=params,
            cls=Block,
            follow_next=follow_next,
        )

    def by_slot(self, slot: int) -> Block:
        """
        Get a block by consensus slot number

        Args:
            slot: Consensus slot number

        Returns:
            A single block
        """
        data = self.client.get(f"{self.resource_path}/{slot}")
        return json_to_instance(data, Block)
