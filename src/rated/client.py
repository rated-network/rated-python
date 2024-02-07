from __future__ import annotations

from typing import Iterator, Type, Dict, Any

import httpx

import humps  # type: ignore

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
    def __init__(self, api_key: str, network: str):
        self.api_key = api_key
        self.network: str = network
        self.headers = httpx.Headers(
            {
                "User-Agent": f"rated-python {__version__}",
                "Authorization": f"Bearer {self.api_key}",
                "X-Rated-Network": self.network,
            }
        )

        self.client = httpx.Client(
            base_url=api_base_url,
            follow_redirects=True,
            event_hooks={"response": [raise_on_4xx_5xx]},
        )

    def get(self, *args, **kwargs) -> Any:
        kwargs["headers"] = self.headers
        response = self.client.get(*args, **kwargs)
        return response.json()

    def post(self, *args, **kwargs) -> httpx.Response:
        kwargs["headers"] = self.headers
        return self.client.post(*args, **kwargs)

    def yield_paginated_results(
        self,
        url: str,
        *,
        params: dict | None = None,
        cls: Type | None = None,
        follow_next: bool = False,
    ) -> Iterator:
        params_: Dict[str, Any] | None = params.copy() if params else None
        while True:
            response = self.client.get(url, params=params_)
            content = response.json()
            for item in content["data"]:
                if cls:
                    yield json_to_instance(item, cls)
                else:
                    yield item

            if not content["next"] or not follow_next:
                break

            url = content["next"]
            params_ = None


def json_to_instance(json_: Dict, cls: Type) -> Any:
    decamelized = {humps.decamelize(k): v for k, v in json_.items()}
    return cls(**decamelized)
