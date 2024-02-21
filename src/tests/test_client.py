import http

import httpx
import pytest

import rated.client
from rated.version import __version__


def test_set_api_key(respx_mock):
    rated.client.api_base_url = "https://foo.bar"
    respx_mock.get("https://foo.bar/v0/health").mock(return_value=httpx.Response(204))
    c = rated.client.Client("fake_api_key", network="foobar")

    assert c.headers.get("Authorization") == "Bearer fake_api_key"


@pytest.mark.parametrize(
    "failure_status_code",
    [
        http.HTTPStatus.INTERNAL_SERVER_ERROR,
        http.HTTPStatus.BAD_REQUEST,
        http.HTTPStatus.UNAUTHORIZED,
        http.HTTPStatus.FORBIDDEN,
    ],
)
def test_rated_api_error_raised_on_unsuccessful_responses(
    respx_mock,
    failure_status_code,
):
    rated.client.api_base_url = "https://foo.bar"
    respx_mock.get("https://foo.bar/v0/health").mock(
        side_effect=httpx.Response(failure_status_code)
    )
    c = rated.client.Client("fake_api_key", network="foobar")
    with pytest.raises(rated.client.RatedApiError):
        c.get("/v0/health")


def test_get_sends_headers(respx_mock):
    rated.client.api_base_url = "https://foo.bar"
    respx_mock.get("https://foo.bar/v0/health").mock(side_effect=httpx.Response(502))
    c = rated.client.Client("fake_api_key", network="foobar")

    try:
        c.get("https://foo.bar/v0/health")
    except rated.client.RatedApiError as exc:
        request = exc.response.request
        assert request.headers.get("Authorization") == "Bearer fake_api_key"
        assert request.headers.get("User-Agent") == "rated-python/0.0.1"


def test_post_sends_headers(respx_mock):
    rated.client.api_base_url = "https://foo.bar"
    respx_mock.post("https://foo.bar/v0/health").mock(side_effect=httpx.Response(502))
    c = rated.client.Client("fake_api_key", network="foobar")

    try:
        c.post("https://foo.bar/v0/health", json={"foo": "bar"})
    except rated.client.RatedApiError as exc:
        request = exc.response.request
        assert request.headers.get("Authorization") == "Bearer fake_api_key"
        assert request.headers.get("User-Agent") == "rated-python/0.0.1"


@pytest.mark.parametrize(
    "headers, exc_message",
    [
        (
            {"Authorization": "Token X", "User-Agent": f"rated-python/{__version__}"},
            "Bearer token is missing",
        ),
        ({"User-Agent": f"rated-python/{__version__}"}, "Bearer token is missing"),
        (
            {"Authorization": "Bearer Y"},
            f"User-Agent not valid: python-httpx/{httpx.__version__}",
        ),
    ],
    ids=[
        "missing-bearer-token",
        "missing-authorization-header",
        "missing-user-agent",
    ],
)
def test_client_raises_on_missing_headers(respx_mock, headers, exc_message):
    rated.client.api_base_url = "https://foo.bar"
    respx_mock.get("https://foo.bar/v0/health").mock(return_value=httpx.Response(204))
    c = rated.client.Client("fake_api_key", network="foobar")

    with pytest.raises(ValueError) as exc_info:
        c.client.get("https://foo.bar/v0/health", headers=headers)

    assert str(exc_info.value) == exc_message
