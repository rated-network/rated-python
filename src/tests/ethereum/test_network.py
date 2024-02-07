import http

import httpx
import pytest


def test_network_stats_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/network/stats").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "day": 796,
                    "avgUptime": 0.9957368996638016,
                    "avgInclusionDelay": 1.0192267929181533,
                    "avgCorrectness": 0.9908021620574459,
                    "avgValidatorEffectiveness": 97.15146353052468,
                }
            ],
        )
    )

    stats = eth_mainnet.network.stats()
    results = list(stats)

    assert len(results) == 1
    assert results[0].day == 796
    assert results[0].avg_uptime == pytest.approx(0.9957368996638016)
    assert results[0].avg_inclusion_delay == pytest.approx(1.0192267929181533)
    assert results[0].avg_correctness == pytest.approx(0.9908021620574459)
    assert results[0].avg_validator_effectiveness == pytest.approx(97.15146353052468)


def test_network_overview_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/network/overview").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "timeWindow": "all",
                    "validatorCount": 513101,
                    "validatorCountDiff": 0,
                    "medianValidatorAgeDays": 446,
                    "activeStake": 16419232000000000,
                    "activeStakeDiff": 0,
                    "avgValidatorBalance": 33989164381.593678,
                    "avgValidatorBalanceDiff": 0,
                    "consensusLayerRewardsPercentage": 71.00716294317242,
                    "priorityFeesPercentage": 17.670898689999394,
                    "baselineMevPercentage": 11.321938366828187,
                    "avgValidatorEffectiveness": 96.24882777017207,
                    "avgInclusionDelay": 1.026223700745488,
                    "avgUptime": 99.60745479648561,
                    "sumMissedSlots": 54305,
                    "missedSlotsPercentage": 0.9463495357389193,
                    "avgConsensusAprPercentage": 4.110372806103757,
                    "avgExecutionAprPercentage": 1.8784786051796751,
                    "medianConsensusAprPercentage": 3.892783165538195,
                    "medianExecutionAprPercentage": 0.6112049138020833,
                    "consensusRewardsRatio": 0.7100716294317242,
                    "executionRewardsRatio": 0.2899283705682758,
                    "avgNetworkAprPercentage": 5.988851411283433,
                    "medianNetworkAprPercentage": 4.503988079340278,
                    "avgConsensusAprGwei": 1315319298,
                    "avgExecutionAprGwei": 601113154,
                    "medianConsensusAprGwei": 1245690613,
                    "medianExecutionAprGwei": 195585572,
                    "avgNetworkAprGwei": 1916432452,
                    "medianNetworkAprGwei": 1441276185,
                    "giniCoefficient": 0.9374772860811317,
                    "clientPercentages": [
                        {"client": "Lighthouse", "percentage": 0.3744886640155385},
                        {"client": "Nimbus", "percentage": 0.025649007580706686},
                        {"client": "Teku", "percentage": 0.19682653817317683},
                        {"client": "Prysm", "percentage": 0.4004708894725073},
                        {"client": "Lodestar", "percentage": 0.0025649007580706685},
                    ],
                    "clientValidatorEffectiveness": [
                        {"client": "Lighthouse", "avgValidatorEffectiveness": 95.42},
                        {"client": "Nimbus", "avgValidatorEffectiveness": 93.4},
                        {"client": "Teku", "avgValidatorEffectiveness": 94.9},
                    ],
                    "latestEpoch": 162521,
                    "activationQueueMinutes": 838.4,
                    "activatingValidators": 787,
                    "activatingStake": 25184000000000,
                    "exitQueueMinutes": 25.6,
                    "withdrawalQueueMinutes": 47392,
                    "withdrawalProcessingQueueMinutes": 47834.2875,
                    "fullyWithdrawingValidators": 32,
                    "partiallyWithdrawingValidators": 35351,
                    "totalWithdrawingValidators": 35383,
                    "fullyWithdrawingBalance": 1024000000000,
                    "partiallyWithdrawingBalance": 1447374543384832,
                    "totalWithdrawingBalance": 39939418387645100,
                    "exitingValidators": 98,
                    "exitingStake": 3136000000000,
                }
            ],
        )
    )

    overview = eth_mainnet.network.overview()
    results = list(overview)

    assert len(results) == 1
    assert results[0].validator_count == 513101
    assert results[0].avg_uptime == pytest.approx(99.60745479648561)


def test_network_capacity_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/network/capacity").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "time_window": "all",
                    "latestEpoch": 186271,
                    "activatedValidators": 238445,
                    "activationCapacityFilled": 0.62372,
                    "exitedValidators": 955,
                    "exitCapacityFilled": 0.0025,
                    "activatedPercentage": 0.47689,
                    "exitedPercentage": 0.00191,
                    "churnLimit": 382294,
                    "activationChurnLimit": 382294,
                    "exitChurnLimit": 382294,
                }
            ],
        )
    )

    capacity = eth_mainnet.network.capacity()
    results = list(capacity)

    assert len(results) == 1
    assert results[0].activated_validators == 238445
    assert results[0].exited_validators == 955
    assert results[0].churn_limit == 382294
    assert results[0].exit_churn_limit == 382294


def test_network_capacity_pool_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/network/capacity/pool").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "time_window": "1d",
                    "stakeAction": "activation",
                    "latestEpoch": 187225,
                    "churnLimit": 12600,
                    "pool": "Lido",
                    "validatorCount": 3534,
                    "capacityFilled": 0.28048,
                    "networkCapacityRemaining": 0.41198,
                }
            ],
        )
    )

    capacity_pool = eth_mainnet.network.capacity_pool()
    results = list(capacity_pool)

    assert len(results) == 1
    assert results[0].pool == "Lido"
    assert results[0].validator_count == 3534
    assert results[0].capacity_filled == pytest.approx(0.28048)
    assert results[0].network_capacity_remaining == pytest.approx(0.41198)
