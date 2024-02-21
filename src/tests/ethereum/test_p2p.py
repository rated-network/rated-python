import http

import httpx
import pytest


def test_p2p_geographical_distribution_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/p2p/geographical?distType=pros"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "country": "United States of America",
                    "countryCode": "US",
                    "distType": "pros",
                    "validatorShare": 0.25749,
                },
                {
                    "country": "Germany",
                    "countryCode": "DE",
                    "distType": "pros",
                    "validatorShare": 0.11901,
                },
                {
                    "country": "United Kingdom of Great Britain and Northern Ireland",
                    "countryCode": "GB",
                    "distType": "pros",
                    "validatorShare": 0.07733,
                },
                {
                    "country": "Singapore",
                    "countryCode": "SG",
                    "distType": "pros",
                    "validatorShare": 0.07289,
                },
                {
                    "country": "Hong Kong",
                    "countryCode": "HK",
                    "distType": "pros",
                    "validatorShare": 0.06539,
                },
            ],
        )
    )

    distribution = eth_mainnet.p2p.geographical_distribution()
    results = list(distribution)

    assert len(results) == 5
    assert results[0].country_code == "US"
    assert results[0].validator_share == pytest.approx(0.25749)
    assert results[4].country_code == "HK"
    assert results[4].validator_share == pytest.approx(0.06539)


def test_p2p_hosting_provider_distribution_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/p2p/hostingProvider?size=2&distType=pros"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "data": [
                    {
                        "distType": "pros",
                        "hostingProvider": "AWS",
                        "validatorShare": 0.22274,
                    },
                    {
                        "distType": "pros",
                        "hostingProvider": "Google Cloud",
                        "validatorShare": 0.13464,
                    },
                ],
                "next": "/v0/eth/p2p/hostingProvider?size=2&from=2",
                "page": {"fromRank": 0, "size": 2, "toRank": None},
                "total": 303,
            },
        )
    )

    distribution = eth_mainnet.p2p.hosting_provider_distribution(size=2)
    results = list(distribution)

    assert len(results) == 2
    assert results[0].hosting_provider == "AWS"
    assert results[0].validator_share == pytest.approx(0.22274)
    assert results[1].hosting_provider == "Google Cloud"
    assert results[1].validator_share == pytest.approx(0.13464)
