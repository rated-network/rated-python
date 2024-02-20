from __future__ import annotations

from typing import Iterator, Any, Dict

from rated.base import APIResource
from rated.client import json_to_instance
from rated.ethereum.datatypes import Block as EthBlock


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
    ) -> Iterator[EthBlock]:
        """
        Get all blocks

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> blocks = eth.blocks.all(from_slot=500, size=10)
            >>> for block in blocks:
            >>>     print(f"{block.total_rewards = }")

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
            cls=EthBlock,
            follow_next=follow_next,
        )


class Block(APIResource):
    path = "/blocks"

    def get(self, slot: int) -> EthBlock:
        """
        Get a block by consensus slot number

        Examples:
            >>> from rated import Rated
            >>> from rated.ethereum import MAINNET
            >>>
            >>> RATED_KEY = "ey..."
            >>> r = Rated(RATED_KEY)
            >>> eth = r.ethereum(network=MAINNET)
            >>> block = eth.blocks.get(500)
            >>> print(f"{block.total_rewards = }")

        Args:
            slot: Consensus slot number

        Returns:
            A single block
        """
        data = self.client.get(f"{self.resource_path}/{slot}")
        return json_to_instance(data, EthBlock)
