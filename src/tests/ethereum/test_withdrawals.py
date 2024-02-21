import http

import httpx


def test_withdrawals_by_operator_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/withdrawals/predicted/operators/Lido?size=2"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "data": [
                    {
                        "id": "Lido",
                        "idType": "pool",
                        "validatorIndex": 1055600,
                        "withdrawableAmount": 17626052,
                        "withdrawalEpoch": 263530,
                        "withdrawalSlot": 8432960,
                        "withdrawalType": "partial",
                    },
                    {
                        "id": "Lido",
                        "idType": "pool",
                        "validatorIndex": 1055601,
                        "withdrawableAmount": 17641057,
                        "withdrawalEpoch": 263530,
                        "withdrawalSlot": 8432961,
                        "withdrawalType": "partial",
                    },
                ],
                "next": "/v0/eth/withdrawals/predicted/operators/Lido?size=2&from=8432959",
                "page": {
                    "filterType": None,
                    "from": None,
                    "granularity": None,
                    "size": 2,
                    "to": None,
                },
                "total": 300473,
            },
        )
    )

    withdrawals = eth_mainnet.withdrawals.by_operator("Lido", size=2)
    results = list(withdrawals)

    assert len(results) == 2
    assert results[0].validator_index == 1055600
    assert results[0].withdrawal_type == "partial"
    assert results[0].withdrawal_epoch == 263530
    assert results[1].validator_index == 1055601
    assert results[1].withdrawal_type == "partial"
    assert results[1].withdrawal_epoch == 263530


def test_withdrawals_by_slot_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/withdrawals/predicted/slot/8432961"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "id": "Ebunker",
                    "idType": "nodeOperator",
                    "validatorIndex": 1055616,
                    "withdrawableAmount": 60491748,
                    "withdrawalEpoch": 263530,
                    "withdrawalSlot": 8432961,
                    "withdrawalType": "partial",
                },
                {
                    "id": "0xf82ac5937a20dc862f9bc0668779031e06000f17",
                    "idType": "depositAddress",
                    "validatorIndex": 1055616,
                    "withdrawableAmount": 60491748,
                    "withdrawalEpoch": 263530,
                    "withdrawalSlot": 8432961,
                    "withdrawalType": "partial",
                },
            ],
        )
    )

    withdrawals = eth_mainnet.withdrawals.by_slot(8432961)
    results = list(withdrawals)

    assert len(results) == 2
    assert results[0].id == "Ebunker"
    assert results[0].validator_index == 1055616
    assert results[0].withdrawable_amount == 60491748
    assert results[1].id == "0xf82ac5937a20dc862f9bc0668779031e06000f17"
    assert results[1].validator_index == 1055616
    assert results[1].withdrawable_amount == 60491748
