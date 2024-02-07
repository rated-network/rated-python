import http

import httpx
import pytest

from rated.ethereum.enums import IdType, TimeWindow, StakeAction, PoolType, AprType


def test_operator_metadata_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/operators/Lido?idType=pool").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "displayName": "Lido",
                "id": "Lido",
                "idType": "pool",
                "nodeOperatorCount": 36,
                "operatorTags": [
                    {
                        "idType": None,
                        "name": "pool",
                        "path": None,
                    }
                ],
            },
        )
    )

    metadata = eth_mainnet.operator.metadata("Lido", id_type=IdType.POOL)

    assert metadata.display_name == "Lido"
    assert metadata.node_operator_count == 36


def test_operator_effectiveness_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/operators/Lido/effectiveness"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "data": [
                    {
                        "avgAttesterEffectiveness": 96.70509227526074,
                        "avgCorrectness": 0.9915735769455304,
                        "avgInclusionDelay": 1.0254926730257783,
                        "avgProposerEffectiveness": 99.73661106233534,
                        "avgUptime": 0.9992134336373116,
                        "avgValidatorEffectiveness": 96.71375240728588,
                        "day": 1170,
                        "endDay": None,
                        "endEpoch": 263250,
                        "hour": None,
                        "id": "Lido",
                        "idType": "pool",
                        "networkPenetration": 0.3180371097570388,
                        "slashesCollected": 0,
                        "slashesReceived": 0,
                        "startDay": None,
                        "startEpoch": 263474,
                        "sumAllRewards": 970611986637,
                        "sumAttestationRewards": 683044232916.0,
                        "sumBaselineMev": 55282576708,
                        "sumConsensusBlockRewards": 95696726681,
                        "sumCorrectHead": 66084731,
                        "sumCorrectSource": 67533861,
                        "sumCorrectTarget": 67506270,
                        "sumEarnings": 776517385495,
                        "sumEstimatedPenalties": -1872887369,
                        "sumEstimatedRewards": 777476297623,
                        "sumExecutionProposedEmptyCount": 0,
                        "sumExternallySourcedExecutionRewards": 191310424069,
                        "sumInclusionDelay": 69333584.0,
                        "sumLateSourcePenalties": -198789920.0,
                        "sumLateSourceVotes": 77170,
                        "sumLateTargetPenalties": -344448.0,
                        "sumLateTargetVotes": 72,
                        "sumMissedAttestationPenalties": -391736000.0,
                        "sumMissedAttestationRewards": 4916329468.0,
                        "sumMissedAttestations": 53225,
                        "sumMissedConsensusBlockRewards": 259145470,
                        "sumMissedExecutionRewards": 468700606,
                        "sumMissedSyncCommitteeRewards": 781093929.0,
                        "sumMissedSyncSignatures": 36831,
                        "sumPriorityFees": 138812024434,
                        "sumProposedCount": 2280,
                        "sumProposerDutiesCount": 2286,
                        "sumSyncCommitteePenalties": -781093929.0,
                        "sumWrongHeadPenalties": 0.0,
                        "sumWrongHeadVotes": 897792,
                        "sumWrongTargetPenalties": -500923072.0,
                        "sumWrongTargetVotes": 104708,
                        "totalUniqueAttestations": 67611031,
                        "validatorCount": 300796,
                    }
                ],
                "next": "/v0/eth/operators/Lido/effectiveness?idType=pool&size=1&from=1169&granularity=day&filterType=day",
                "page": {
                    "filterType": "day",
                    "from": None,
                    "granularity": "day",
                    "size": 1,
                    "to": None,
                },
                "total": 1136,
            },
        )
    )

    effectiveness = eth_mainnet.operator.effectiveness(
        "Lido",
        size=1,
        id_type=IdType.POOL,
    )
    results = list(effectiveness)

    assert len(results) == 1
    assert results[0].validator_count == 300796
    assert results[0].avg_uptime == pytest.approx(0.9992134336373116)
    assert results[0].avg_validator_effectiveness == pytest.approx(96.71375240728588)


def test_operator_clients_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/operators/Lido/clients?idType=pool"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {"client": "Nimbus", "percentage": 0.07673449918745182},
                {"client": "Teku", "percentage": 0.2458277175992945},
                {"client": "Lodestar", "percentage": 0.03457073606327338},
                {"client": "Prysm", "percentage": 0.33916815032973374},
                {"client": "Lighthouse", "percentage": 0.3036988968202466},
            ],
        )
    )

    clients = eth_mainnet.operator.clients("Lido", id_type=IdType.POOL)
    results = list(clients)

    assert len(results) == 5
    assert results[0].client == "Nimbus"
    assert results[0].percentage == pytest.approx(0.07673449918745182)
    assert results[4].client == "Lighthouse"
    assert results[4].percentage == pytest.approx(0.3036988968202466)


def test_operator_relayers_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/operators/Lido/relayers?idType=pool&window=30d"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {"percentage": 0.10582940258959277, "relayer": "flashbots"},
                {"percentage": 0.25825456185518575, "relayer": "ultra_sound_money"},
            ],
        )
    )

    relayers = eth_mainnet.operator.relayers(
        "Lido",
        id_type=IdType.POOL,
        time_window=TimeWindow.THIRTY_DAYS,
    )
    results = list(relayers)

    assert len(results) == 2
    assert results[0].relayer == "flashbots"
    assert results[0].percentage == pytest.approx(0.10582940258959277)
    assert results[1].relayer == "ultra_sound_money"
    assert results[1].percentage == pytest.approx(0.25825456185518575)


def test_operator_apr_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/operators/Lido/apr?idType=pool&window=7d&aprType=backward"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "activeStake": 9453792000000000.0,
                "activeValidators": 295431,
                "aprType": "backward",
                "id": "Lido",
                "idType": "pool",
                "percentage": 4.07,
                "percentageConsensus": 2.97,
                "percentageExecution": 1.1,
                "timeWindow": "7d",
            },
        )
    )

    apr = eth_mainnet.operator.apr(
        "Lido",
        id_type=IdType.POOL,
        time_window=TimeWindow.SEVEN_DAYS,
        apr_type=AprType.BACKWARD,
    )

    assert apr.active_stake == pytest.approx(9453792000000000.0)
    assert apr.active_validators == 295431
    assert apr.percentage == pytest.approx(4.07)


def test_operator_summary_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/operators/Lido/summary?idType=pool&window=7d"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "aprPercentage": 4.07,
                "avgCorrectness": 0.9921541927979295,
                "avgInclusionDelay": 1.0219224318884224,
                "avgUptime": 0.9993176602148433,
                "avgValidatorEffectiveness": 97.10250590328032,
                "clientPercentages": [
                    {"client": "Nimbus", "percentage": 0.07673449918745182},
                    {"client": "Lodestar", "percentage": 0.03457073606327338},
                    {"client": "Prysm", "percentage": 0.33916815032973374},
                    {"client": "Lighthouse", "percentage": 0.3036988968202466},
                    {"client": "Teku", "percentage": 0.2458277175992945},
                ],
                "displayName": "Lido",
                "id": "Lido",
                "idType": "pool",
                "networkPenetration": 0.3180371097570388,
                "nodeOperatorCount": 36,
                "operatorTags": [{"idType": None, "name": "pool", "path": None}],
                "relayerPercentages": [
                    {
                        "percentage": 0.1928463517210404,
                        "relayer": "bloxroute_regulated",
                    },
                    {"percentage": 0.05814380792944347, "relayer": "no_mev_boost"},
                    {"percentage": 0.0007349638642766731, "relayer": "edennetwork"},
                    {"percentage": 0.282920256420726, "relayer": "ultra_sound_money"},
                    {"percentage": 0.034012494385692704, "relayer": "aestus"},
                    {"percentage": 0.001796578334898534, "relayer": "manifold"},
                    {
                        "percentage": 0.2295537136090809,
                        "relayer": "bloxroute_maxprofit",
                    },
                    {"percentage": 0.0927687722020334, "relayer": "flashbots"},
                    {"percentage": 0.10722306153280797, "relayer": "agnostic"},
                ],
                "timeWindow": "7d",
                "validatorCount": 300796,
            },
        )
    )

    summary = eth_mainnet.operator.summary(
        "Lido",
        id_type=IdType.POOL,
        time_window=TimeWindow.SEVEN_DAYS,
    )

    assert summary.display_name == "Lido"
    assert summary.avg_validator_effectiveness == pytest.approx(97.10250590328032)
    assert summary.network_penetration == pytest.approx(0.3180371097570388)


def test_operator_stake_movement_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/operators/Lido/stakeMovement?idType=pool&stakeAction=activation&window=7d"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "amountGwei": 173920000000000,
                    "avgEpochsToAction": 0,
                    "avgMinutesToAction": 0.0,
                    "id": "Lido",
                    "idType": "pool",
                    "stakeAction": "activation",
                    "timeWindow": "7d",
                    "validatorCount": 5435,
                }
            ],
        )
    )

    stake_movement = eth_mainnet.operator.stake_movement(
        "Lido",
        id_type=IdType.POOL,
        time_window=TimeWindow.SEVEN_DAYS,
        stake_action=StakeAction.ACTIVATION,
    )
    results = list(stake_movement)

    assert len(results) == 1
    assert results[0].validator_count == 5435
    assert results[0].amount_gwei == 173920000000000


def test_operators_percentiles_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/operators/percentiles?idType=pool&window=7d"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {"rank": 0, "timeWindow": "7d", "value": 66.62489785231287},
                {"rank": 1, "timeWindow": "7d", "value": 66.62489785231287},
                {"rank": 2, "timeWindow": "7d", "value": 66.62489785231287},
                {"rank": 3, "timeWindow": "7d", "value": 85.37287684631578},
                {"rank": 4, "timeWindow": "7d", "value": 85.37287684631578},
            ],
        )
    )

    percentiles = eth_mainnet.operators.percentiles(
        id_type=IdType.POOL,
        time_window=TimeWindow.SEVEN_DAYS,
    )
    results = list(percentiles)

    assert len(results) == 5
    assert results[0].rank == 0
    assert results[0].value == pytest.approx(66.62489785231287)
    assert results[4].rank == 4
    assert results[4].value == pytest.approx(85.37287684631578)


def test_operators_summaries_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/operators").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "data": [
                    {
                        "aprPercentage": 4.02,
                        "avgCorrectness": 0.992189223948043,
                        "avgInclusionDelay": 1.0218233708560729,
                        "avgUptime": 0.9993308928973733,
                        "avgValidatorEffectiveness": 97.11748772553577,
                        "clientPercentages": [
                            {"client": "Lodestar", "percentage": 0.04080870061163884},
                            {"client": "Prysm", "percentage": 0.31096557646796597},
                            {"client": "Nimbus", "percentage": 0.08998892101140021},
                            {"client": "Teku", "percentage": 0.25362361594587685},
                            {"client": "Lighthouse", "percentage": 0.3046131859631181},
                        ],
                        "displayName": "0xf82ac5937a20dc862f9bc0668779031e06000f17",
                        "id": "0xf82ac5937a20dc862f9bc0668779031e06000f17",
                        "idType": "depositAddress",
                        "networkPenetration": 0.2756513344942688,
                        "nodeOperatorCount": None,
                        "operatorTags": [],
                        "relayerPercentages": [
                            {
                                "percentage": 0.0007036307345904869,
                                "relayer": "edennetwork",
                            },
                            {
                                "percentage": 0.1995496763298621,
                                "relayer": "bloxroute_regulated",
                            },
                            {"percentage": 0.09264471338774745, "relayer": "flashbots"},
                            {
                                "percentage": 0.06454639271976734,
                                "relayer": "no_mev_boost",
                            },
                            {
                                "percentage": 0.0018763486255746317,
                                "relayer": "manifold",
                            },
                            {
                                "percentage": 0.2679425837320574,
                                "relayer": "ultra_sound_money",
                            },
                            {"percentage": 0.03316446195703162, "relayer": "aestus"},
                            {
                                "percentage": 0.235059574068862,
                                "relayer": "bloxroute_maxprofit",
                            },
                            {"percentage": 0.10451261844450699, "relayer": "agnostic"},
                        ],
                        "timeWindow": "7d",
                        "validatorCount": 260708,
                    }
                ],
                "next": "/v0/eth/operators?window=7d&from=1&size=1&idType=depositAddress",
                "page": {
                    "filterType": None,
                    "from": None,
                    "granularity": None,
                    "size": 1,
                    "to": None,
                },
                "total": 109982,
            },
        )
    )

    summaries = eth_mainnet.operators.summaries(
        time_window=TimeWindow.SEVEN_DAYS,
        pool_type=PoolType.ALL,
        size=1,
    )
    results = list(summaries)

    assert len(results) == 1
    assert results[0].display_name == "0xf82ac5937a20dc862f9bc0668779031e06000f17"
    assert results[0].validator_count == 260708
    assert results[0].network_penetration == pytest.approx(0.2756513344942688)
