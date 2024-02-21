import http

import httpx
import pytest

from rated.ethereum.enums import (
    AprType,
    TimeWindow,
    Granularity,
    ValidatorsEffectivenessGroupBy,
)


def test_validator_apr_response_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/validators/1000/apr?aprType=backward&window=all"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "validatorIndex": 1000,
                "idType": "validator",
                "timeWindow": "all",
                "aprType": "backward",
                "percentage": 5.35,
                "percentageConsensus": 4.04,
                "percentageExecution": 1.31,
                "activeStake": 4823520000000000,
                "activeValidators": 150735,
            },
        )
    )

    apr = eth_mainnet.validator.apr(
        index_or_pubkey=1000,
        apr_type=AprType.BACKWARD,
        time_window=TimeWindow.ALL_TIME,
    )

    assert apr.apr_type == "backward"
    assert apr.validator_index == 1000
    assert apr.active_validators == 150735


def test_validator_metadata_response_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/validators/100").mock(
        return_value=httpx.Response(
            200,
            json={
                "activationEpoch": 0,
                "activationEligibilityEpoch": 0,
                "depositAddresses": ["0x74134d0c91798d720a5585364bb4be7396c5b973"],
                "dvtNetwork": None,
                "dvtOperators": [],
                "exitEpoch": None,
                "nodeOperators": [],
                "pool": None,
                "validatorIndex": 100,
                "validatorPubkey": "0xb5bc96b70df0dfcc252c9ff0d1b42cb6dc0d55f8defa474dc0a5c7e0402c241e2850fea9c582e276b638b3c2c3a5ec55",
                "withdrawableEpoch": None,
                "withdrawalAddress": "0xfff1ce616cf83327981bf61396ad0c04e0c8b771",
            },
        )
    )

    metadata = eth_mainnet.validator.metadata(index_or_pubkey=100)

    assert metadata.validator_index == 100
    assert (
        metadata.validator_pubkey
        == "0xb5bc96b70df0dfcc252c9ff0d1b42cb6dc0d55f8defa474dc0a5c7e0402c241e2850fea9c582e276b638b3c2c3a5ec55"
    )
    assert metadata.withdrawal_address == "0xfff1ce616cf83327981bf61396ad0c04e0c8b771"


def test_validator_effectiveness_dont_follow_next_page(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/validators/100/effectiveness?from=803&size=1"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "page": {
                    "filterType": "day",
                    "from": None,
                    "granularity": "day",
                    "size": 1,
                    "to": None,
                },
                "data": [
                    {
                        "attesterEffectiveness": 98.82005899705014,
                        "avgCorrectness": 0.9925925925925926,
                        "avgInclusionDelay": 1.0044444444444445,
                        "day": 803,
                        "earnings": 2958548,
                        "endDay": None,
                        "endEpoch": 180675,
                        "estimatedPenalties": -6461,
                        "estimatedRewards": 2965823,
                        "executionProposedEmptyCount": 0,
                        "proposedCount": 0,
                        "proposerDutiesCount": 0,
                        "proposerEffectiveness": None,
                        "slashesCollected": 0,
                        "slashesReceived": 0,
                        "startDay": None,
                        "startEpoch": 180899,
                        "sumAllRewards": 2958548,
                        "sumAttestationRewards": 2965823.0,
                        "sumBaselineMev": 0,
                        "sumConsensusBlockRewards": 0,
                        "sumCorrectHead": 221,
                        "sumCorrectSource": 225,
                        "sumCorrectTarget": 224,
                        "sumExternallySourcedExecutionRewards": 0,
                        "sumInclusionDelay": 226.0,
                        "sumLateSourcePenalties": 0.0,
                        "sumLateSourceVotes": 0,
                        "sumLateTargetPenalties": 0.0,
                        "sumLateTargetVotes": 0,
                        "sumMissedAttestationPenalties": 0.0,
                        "sumMissedAttestationRewards": 19233.0,
                        "sumMissedAttestations": 0,
                        "sumMissedConsensusBlockRewards": 0,
                        "sumMissedExecutionRewards": 0,
                        "sumMissedSyncCommitteeRewards": 0.0,
                        "sumMissedSyncSignatures": None,
                        "sumPriorityFees": 0,
                        "sumSyncCommitteePenalties": 0.0,
                        "sumWrongHeadPenalties": 0.0,
                        "sumWrongHeadVotes": 3,
                        "sumWrongTargetPenalties": -6461.0,
                        "sumWrongTargetVotes": 1,
                        "syncSignatureCount": 0,
                        "totalAttestationAssignments": 225,
                        "totalAttestations": 237,
                        "totalUniqueAttestations": 225,
                        "uptime": 1.0,
                        "validatorEffectiveness": 98.82005899705014,
                        "validatorIndex": 100,
                    }
                ],
                "next": "/v0/eth/validators/100/effectiveness?from=802&size=1&granularity=day&filterType=day",
                "total": 804,
            },
        )
    )

    effectiveness = eth_mainnet.validator.effectiveness(
        index_or_pubkey=100,
        from_day=803,
        size=1,
        follow_next=False,
    )

    results = list(effectiveness)

    assert len(results) == 1
    assert results[0].validator_effectiveness == 98.82005899705014
    assert results[0].validator_index == 100
    assert results[0].day == 803


def test_validator_effectiveness_do_follow_next_page(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/validators/100/effectiveness?from=803&size=1"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "page": {
                    "filterType": "day",
                    "from": None,
                    "granularity": "day",
                    "size": 1,
                    "to": None,
                },
                "data": [
                    {
                        "attesterEffectiveness": 98.82005899705014,
                        "avgCorrectness": 0.9925925925925926,
                        "avgInclusionDelay": 1.0044444444444445,
                        "day": 803,
                        "earnings": 2958548,
                        "endDay": None,
                        "endEpoch": 180675,
                        "estimatedPenalties": -6461,
                        "estimatedRewards": 2965823,
                        "executionProposedEmptyCount": 0,
                        "proposedCount": 0,
                        "proposerDutiesCount": 0,
                        "proposerEffectiveness": None,
                        "slashesCollected": 0,
                        "slashesReceived": 0,
                        "startDay": None,
                        "startEpoch": 180899,
                        "sumAllRewards": 2958548,
                        "sumAttestationRewards": 2965823.0,
                        "sumBaselineMev": 0,
                        "sumConsensusBlockRewards": 0,
                        "sumCorrectHead": 221,
                        "sumCorrectSource": 225,
                        "sumCorrectTarget": 224,
                        "sumExternallySourcedExecutionRewards": 0,
                        "sumInclusionDelay": 226.0,
                        "sumLateSourcePenalties": 0.0,
                        "sumLateSourceVotes": 0,
                        "sumLateTargetPenalties": 0.0,
                        "sumLateTargetVotes": 0,
                        "sumMissedAttestationPenalties": 0.0,
                        "sumMissedAttestationRewards": 19233.0,
                        "sumMissedAttestations": 0,
                        "sumMissedConsensusBlockRewards": 0,
                        "sumMissedExecutionRewards": 0,
                        "sumMissedSyncCommitteeRewards": 0.0,
                        "sumMissedSyncSignatures": None,
                        "sumPriorityFees": 0,
                        "sumSyncCommitteePenalties": 0.0,
                        "sumWrongHeadPenalties": 0.0,
                        "sumWrongHeadVotes": 3,
                        "sumWrongTargetPenalties": -6461.0,
                        "sumWrongTargetVotes": 1,
                        "syncSignatureCount": 0,
                        "totalAttestationAssignments": 225,
                        "totalAttestations": 237,
                        "totalUniqueAttestations": 225,
                        "uptime": 1.0,
                        "validatorEffectiveness": 98.82005899705014,
                        "validatorIndex": 100,
                    }
                ],
                "next": "/v0/eth/validators/100/effectiveness?from=802&size=1&granularity=day&filterType=day",
                "total": 804,
            },
        )
    )
    respx_mock.get(
        "https://api.rated.network/v0/eth/validators/100/effectiveness?from=802&size=1&granularity=day&filterType=day"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "page": {
                    "filterType": "day",
                    "from": None,
                    "granularity": "day",
                    "size": 1,
                    "to": None,
                },
                "data": [
                    {
                        "attesterEffectiveness": 98.82005899705013,
                        "avgCorrectness": 0.9925925925925926,
                        "avgInclusionDelay": 1.0044444444444445,
                        "day": 802,
                        "earnings": 2958548,
                        "endDay": None,
                        "endEpoch": 180675,
                        "estimatedPenalties": -6461,
                        "estimatedRewards": 2965823,
                        "executionProposedEmptyCount": 0,
                        "proposedCount": 0,
                        "proposerDutiesCount": 0,
                        "proposerEffectiveness": None,
                        "slashesCollected": 0,
                        "slashesReceived": 0,
                        "startDay": None,
                        "startEpoch": 180899,
                        "sumAllRewards": 2958548,
                        "sumAttestationRewards": 2965823.0,
                        "sumBaselineMev": 0,
                        "sumConsensusBlockRewards": 0,
                        "sumCorrectHead": 221,
                        "sumCorrectSource": 225,
                        "sumCorrectTarget": 224,
                        "sumExternallySourcedExecutionRewards": 0,
                        "sumInclusionDelay": 226.0,
                        "sumLateSourcePenalties": 0.0,
                        "sumLateSourceVotes": 0,
                        "sumLateTargetPenalties": 0.0,
                        "sumLateTargetVotes": 0,
                        "sumMissedAttestationPenalties": 0.0,
                        "sumMissedAttestationRewards": 19233.0,
                        "sumMissedAttestations": 0,
                        "sumMissedConsensusBlockRewards": 0,
                        "sumMissedExecutionRewards": 0,
                        "sumMissedSyncCommitteeRewards": 0.0,
                        "sumMissedSyncSignatures": None,
                        "sumPriorityFees": 0,
                        "sumSyncCommitteePenalties": 0.0,
                        "sumWrongHeadPenalties": 0.0,
                        "sumWrongHeadVotes": 3,
                        "sumWrongTargetPenalties": -6461.0,
                        "sumWrongTargetVotes": 1,
                        "syncSignatureCount": 0,
                        "totalAttestationAssignments": 225,
                        "totalAttestations": 237,
                        "totalUniqueAttestations": 225,
                        "uptime": 1.0,
                        "validatorEffectiveness": 98.82005899705013,
                        "validatorIndex": 100,
                    }
                ],
                "next": None,
                "total": 804,
            },
        )
    )

    effectiveness = eth_mainnet.validator.effectiveness(
        index_or_pubkey=100,
        from_day=803,
        size=1,
        follow_next=True,
    )

    results = list(effectiveness)

    assert len(results) == 2
    assert results[0].validator_effectiveness == 98.82005899705014
    assert results[0].validator_index == 100
    assert results[0].day == 803
    assert results[1].validator_effectiveness == 98.82005899705013
    assert results[1].validator_index == 100
    assert results[1].day == 802


def test_validators_metadata_response_ok_dont_follow_next(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/validators").mock(
        return_value=httpx.Response(
            200,
            json={
                "page": {"from": 0, "size": 3},
                "total": 11,
                "data": [
                    {
                        "validatorIndex": 1,
                        "validatorPubkey": "0xb44440543ceef8d77e065c70da15f7b731e56db5457571c465f025e032bbcd263a0990c8749b4ca6ff20d77004466666",
                        "pool": "",
                        "dvtNetwork": "",
                        "nodeOperators": [],
                        "depositAddresses": [
                            "0xc34eb7e3f34e54646d7cd140bb7c20a466b3e852"
                        ],
                        "dvtOperators": [],
                        "activationEpoch": 169000,
                        "activationEligibilityEpoch": 171000,
                        "exitEpoch": 172000,
                        "withdrawableEpoch": 172256,
                        "withdrawalAddress": "0x0d369bb49efa5100fd3b86a9f828c55da04d2d50",
                    },
                    {
                        "validatorIndex": 4,
                        "validatorPubkey": "0xa62420543ceef8d77e065c70da15f7b731e56db5457571c465f025e032bbcd263a0990c8749b4ca6ff20d77004454b51",
                        "pool": "",
                        "dvtNetwork": "",
                        "nodeOperators": [],
                        "depositAddresses": [
                            "0xc34eb7e3f34e54646d7cd140bb7c20a466b3e852"
                        ],
                        "dvtOperators": [],
                        "activationEpoch": 169000,
                        "activationEligibilityEpoch": 171000,
                        "exitEpoch": 172000,
                        "withdrawableEpoch": 172256,
                        "withdrawalAddress": "0x0d369bb49efa5100fd3b86a9f828c55da04d2d50",
                    },
                    {
                        "validatorIndex": 10,
                        "validatorPubkey": "0xc55540543ceef8dccc065c70da15f7b731e56db5457571c465f0254442bbcd263a0111c8749b4ca6ff20d77004466777",
                        "pool": "",
                        "dvtNetwork": "",
                        "nodeOperators": [],
                        "depositAddresses": [
                            "0xc34eb7e3f34e54646d7cd140bb7c20a466b3e852"
                        ],
                        "dvtOperators": [],
                        "activationEpoch": 169000,
                        "activationEligibilityEpoch": 171000,
                        "exitEpoch": 172000,
                        "withdrawableEpoch": 172256,
                        "withdrawalAddress": "0x0d369bb49efa5100fd3b86a9f828c55da04d2d50",
                    },
                ],
                "next": "/v0/eth/validators?from=11&size=3&operatorsIds=&idType=",
            },
        )
    )

    metadata = eth_mainnet.validators.metadata(size=3)
    results = list(metadata)

    assert len(results) == 3
    assert results[0].validator_index == 1
    assert results[1].validator_index == 4
    assert results[2].validator_index == 10


def test_validators_effectiveness_ok_dont_follow_next(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/validators/effectiveness?indices=100&indices=101&filterType=day&size=1&granularity=month&groupBy=timeWindow"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "attesterEffectiveness": 98.46868397067385,
                        "avgCorrectness": 0.9951851851851852,
                        "avgInclusionDelay": 1.0107407407407407,
                        "day": 803,
                        "earnings": 35804991,
                        "endDay": 792,
                        "endEpoch": 178200,
                        "estimatedPenalties": -22921,
                        "estimatedRewards": 35849013,
                        "executionProposedEmptyCount": 0,
                        "proposedCount": 0,
                        "proposerDutiesCount": 0,
                        "slashesCollected": 0,
                        "slashesReceived": 0,
                        "startDay": 803,
                        "startEpoch": 180899,
                        "sumAllRewards": 35804991,
                        "sumAttestationRewards": 35849013,
                        "sumBaselineMev": 0,
                        "sumConsensusBlockRewards": 0,
                        "sumCorrectHead": 2665,
                        "sumCorrectSource": 2699,
                        "sumCorrectTarget": 2697,
                        "sumExternallySourcedExecutionRewards": 0,
                        "sumInclusionDelay": 2729,
                        "sumLateSourcePenalties": -3486,
                        "sumLateSourceVotes": 1,
                        "sumLateTargetPenalties": 0,
                        "sumLateTargetVotes": 0,
                        "sumMissedAttestationPenalties": 0,
                        "sumMissedAttestationRewards": 137813,
                        "sumMissedAttestations": 0,
                        "sumMissedConsensusBlockRewards": 0,
                        "sumMissedExecutionRewards": 0,
                        "sumMissedSyncCommitteeRewards": 0,
                        "sumPriorityFees": 0,
                        "sumSyncCommitteePenalties": 0,
                        "sumWrongHeadPenalties": 0,
                        "sumWrongHeadVotes": 21,
                        "sumWrongTargetPenalties": -19435,
                        "sumWrongTargetVotes": 3,
                        "syncSignatureCount": 0,
                        "totalAttestationAssignments": 2700,
                        "totalAttestations": 2919,
                        "totalUniqueAttestations": 2700,
                        "uptime": 1,
                        "validatorEffectiveness": 98.46868397067385,
                    }
                ],
                "next": "/v0/eth/validators/effectiveness?indices=100&indices=101&groupBy=timeWindow&granularity=month&size=1&from=791&filterType=day",
                "page": {"filterType": "day", "granularity": "month", "size": 1},
                "total": 27,
            },
        )
    )
    effectiveness = eth_mainnet.validators.effectiveness(
        indices=[100, 101],
        group_by=ValidatorsEffectivenessGroupBy.TIME,
        granularity=Granularity.MONTH,
        size=1,
    )
    results = list(effectiveness)

    assert len(results) == 1
    assert results[0].validator_effectiveness == pytest.approx(98.46868397067385)


def test_validator_self_report_ok(respx_mock, eth_mainnet):
    respx_mock.post("https://api.rated.network/v0/selfReports/validators").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "operatorName": "Ratooor",
                "validators": [
                    "0x111135d53832d108e9015295802aa49834efa6c7e5cfd2be02f2f3f5aaba13c07230cb89ba66bd04e2703499542aa153"
                ],
                "network": "mainnet",
                "poolTag": None,
            },
        )
    )

    result = eth_mainnet.validators.report(
        [
            "0x111135d53832d108e9015295802aa49834efa6c7e5cfd2be02f2f3f5aaba13c07230cb89ba66bd04e2703499542aa153"
        ]
    )

    assert result == 1
