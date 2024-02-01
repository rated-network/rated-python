from __future__ import annotations

import os

import httpx

from rated.version import __version__

api_base_url: str = "https://api.rated.network"


class RatedApiError(Exception):
    def __init__(self, response: httpx.Response):
        self.status_code = response.status_code
        self.response = response
        self.request_id = response.headers.get("x-request-id")


def raise_on_4xx_5xx(response: httpx.Response):
    try:
        response.raise_for_status()
    except httpx.HTTPError:
        raise RatedApiError(response)


class Client:
    def __init__(self, api_key: str | None = None, network: str = "mainnet"):
        self.api_key = os.getenv("RATED_API_KEY", api_key)
        if not self.api_key:
            raise ValueError("Must provide a valid Rated API key")

        self.client = httpx.Client(
            base_url=api_base_url,
            headers={
                "User-Agent": f"rated-python {__version__}",
                "Authorization": f"Bearer {self.api_key}",
                "X-Rated-Network": network,
            },
            follow_redirects=True,
            event_hooks={"response": [raise_on_4xx_5xx]},
        )

    def get(self, *args, **kwargs) -> httpx.Response:
        with self.client:
            res = self.client.get(*args, **kwargs)
        return res

    def post(self, *args, **kwargs) -> httpx.Response:
        with self.client:
            res = self.client.post(*args, **kwargs)
        return res
