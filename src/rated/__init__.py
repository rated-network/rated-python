from __future__ import annotations

import os

from rated import ethereum
from rated.client import Client


class Rated:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        if self.api_key is None:
            self.api_key = os.getenv("RATED_API_KEY")

    def ethereum(self, network: str) -> ethereum.Ethereum:
        if self.api_key is None:
            raise ValueError("Must provide an API key.")

        c = Client(api_key=self.api_key, network=network)
        return ethereum.Ethereum(c)
