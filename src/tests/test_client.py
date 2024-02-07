import http

import httpx
import pytest

import rated.client


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
