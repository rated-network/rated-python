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


def check_for_user_agent(request: httpx.Request):
    user_agent = request.headers.get("user-agent")
    if not user_agent == f"rated-python/{__version__}":
        raise ValueError(f"User-Agent not valid: {user_agent}")


def check_for_auth_header(request: httpx.Request):
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise ValueError("Bearer token is missing")


def check_for_empty_query_params(request: httpx.Request):
    if any([not value for value in request.url.params.values()]):
        raise ValueError("Empty query parameters are not allowed")


def raise_on_4xx_5xx(response: httpx.Response):
    try:
        response.raise_for_status()
    except httpx.HTTPError:
        raise RatedApiError(response)


class Client:
    def __init__(self, api_key: str, network: str):
        """
        Initialize a client instance with an API key and a network

        Args:
            api_key: Rated API key
            network: Supported network
        """
        self.api_key = api_key
        self.network: str = network
        self.headers = httpx.Headers(
            {
                "User-Agent": f"rated-python/{__version__}",
                "Authorization": f"Bearer {self.api_key}",
                "X-Rated-Network": self.network,
            }
        )

        self.client = httpx.Client(
            base_url=api_base_url,
            follow_redirects=True,
            event_hooks={
                "request": [
                    check_for_user_agent,
                    check_for_auth_header,
                    check_for_empty_query_params,
                ],
                "response": [raise_on_4xx_5xx],
            },
        )

    def get(self, *args, **kwargs) -> Any:
        """
        Make a GET request to the Rated API

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            JSON data from the response
        """
        params = kwargs.get("params", {}).copy()
        kwargs["headers"] = self.headers
        kwargs["params"] = {k: v for k, v in params.items() if v is not None}
        response = self.client.get(*args, **kwargs)
        return response.json()

    def post(self, *args, **kwargs) -> httpx.Response:
        """
        Make a POST request to the Rated API

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Response
        """
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
        """
        Yield all results of a paginated response from the Rated API

        Args:
            url: The URL of the desired resource
            params: Query parameters for the request
            cls: Dataclass to be used to instantiate the new Python object
            follow_next: Follow next page if any and fetch its results

        Returns:
            An iterator over the results of the page
        """
        params_: Dict[str, Any] | None = params.copy() if params else None
        if params_:
            params_ = {k: v for k, v in params_.items() if v is not None}
        while True:
            response = self.client.get(url, params=params_, headers=self.headers)
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
    """
    Converts a camelCased JSON to a Python object instance

    Args:
        json_: The JSON data to convert
        cls: Dataclass to be used to instantiate the new Python object

    Returns:
        An instance of the given class
    """
    decamelized = {humps.decamelize(k): v for k, v in json_.items()}
    return cls(**decamelized)
