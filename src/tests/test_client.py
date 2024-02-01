import httpx

import rated.client


def test_set_api_key(respx_mock):
    respx_mock.get("https://foo.bar/v0/health").mock(return_value=httpx.Response(204))
    rated.client.api_base_url = "https://foo.bar"
    c = rated.client.Client("fake_api_key")
    res = c.get("/v0/health")

    assert res.request.headers["Authorization"] == "Bearer fake_api_key"


def test_set_network(respx_mock):
    respx_mock.get("https://foo.bar/v0/health").mock(return_value=httpx.Response(204))
    rated.client.api_base_url = "https://foo.bar"
    c = rated.client.Client("fake_api_key", "fakenet")
    res = c.get("/v0/health")

    assert res.request.headers["X-Rated-Network"] == "fakenet"
