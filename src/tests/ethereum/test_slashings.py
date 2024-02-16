import http

import httpx
import pytest


def test_slashings_overview_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/slashings/overview").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "currentSlashingPenaltyGwei": 1064505495,
                    "discreteSlashingEvents": 109,
                    "largestSlashingIncident": 77,
                    "prosRatio": 0.67554,
                    "slashingPenaltiesAllRewardsRatio": 0.00016,
                    "slashingPenaltiesStakeRatio": 1e-05,
                    "slashingSlotsRatio": 3.8817596831333945e-05,
                    "solosRatio": 0.32446,
                    "timeWindow": "all",
                    "validatorsSlashed": 413,
                }
            ],
        )
    )

    overview = eth_mainnet.slashings.overview()
    results = list(overview)

    assert len(results) == 1
    assert results[0].validators_slashed == 413
    assert results[0].current_slashing_penalty_gwei == 1064505495
    assert results[0].pros_ratio == pytest.approx(0.67554)
    assert results[0].solos_ratio == pytest.approx(0.32446)


def test_slashings_leaderboard_ok(respx_mock, eth_mainnet):
    respx_mock.get(
        "https://api.rated.network/v0/eth/slashings/leaderboard?from=&size=1"
    ).mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "data": [
                    {
                        "id": "Bitcoin Suisse",
                        "idType": "pool",
                        "medianSlashedMonth": "Nov 2023",
                        "slasherPedigree": "NA",
                        "slashes": 99,
                        "slashingRole": "slashed",
                        "validatorCount": 14564,
                    }
                ],
                "next": "/v0/eth/slashings/leaderboard?size=1&from=1",
                "page": {"fromRank": 0, "size": 1, "toRank": None},
                "total": 125,
            },
        )
    )

    leaderboard = eth_mainnet.slashings.leaderboard(size=1)
    results = list(leaderboard)

    assert len(results) == 1
    assert results[0].id == "Bitcoin Suisse"
    assert results[0].slashes == 99
    assert results[0].validator_count == 14564


def test_slashings_cohorts_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/slashings/cohortAnalysis").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {
                    "allTime": 17,
                    "cohort": "pros_between_100_to_1k",
                    "lastSixMonths": 0,
                    "pastTwoYears": 0,
                    "pastYear": 0,
                },
                {
                    "allTime": 21,
                    "cohort": "pros_between_10_to_100",
                    "lastSixMonths": 14,
                    "pastTwoYears": 18,
                    "pastYear": 18,
                },
                {
                    "allTime": 150,
                    "cohort": "solos",
                    "lastSixMonths": 14,
                    "pastTwoYears": 94,
                    "pastYear": 40,
                },
                {
                    "allTime": 20,
                    "cohort": "pros_between_1k_to_5k",
                    "lastSixMonths": 20,
                    "pastTwoYears": 20,
                    "pastYear": 20,
                },
                {
                    "allTime": 205,
                    "cohort": "pros_more_than_5k",
                    "lastSixMonths": 100,
                    "pastTwoYears": 112,
                    "pastYear": 112,
                },
            ],
        )
    )

    cohorts = eth_mainnet.slashings.cohorts()
    results = list(cohorts)

    assert len(results) == 5
    assert results[0].all_time == 17
    assert results[0].cohort == "pros_between_100_to_1k"


def test_slashings_timeseries_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/slashings/timeseries").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json=[
                {"month": "2020-12-01", "validatorsSlashed": 32},
                {"month": "2021-01-01", "validatorsSlashed": 7},
                {"month": "2021-02-01", "validatorsSlashed": 93},
            ],
        )
    )

    timeseries = eth_mainnet.slashings.timeseries()
    results = list(timeseries)

    assert len(results) == 3
    assert results[0].validators_slashed == 32
    assert results[0].month == "2020-12-01"


def test_slashings_penalties_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/slashings?from=&size=2").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "data": [
                    {
                        "balanceBeforeSlashing": 32014860472,
                        "balanceBeforeWithdrawal": 31408009071,
                        "slashingEpoch": 208,
                        "slashingPenalties": 606851401,
                        "validatorIndex": 20075,
                        "validatorPubkey": "0xb02c42a2cda10f06441597ba87e87a47c187cd70e2b415bef8dc890669efe223f551a2c91c3d63a5779857d3073bf288",
                        "withdrawableEpoch": 8400,
                    },
                    {
                        "balanceBeforeSlashing": 32035870245,
                        "balanceBeforeWithdrawal": 31433401729,
                        "slashingEpoch": 534,
                        "slashingPenalties": 602468516,
                        "validatorIndex": 4259,
                        "validatorPubkey": "0xad1b82729a1afb2a827a27ce16705fb7eeb59bb9e66eeabc8d40b0c40ab2181ae1e173fb85370c21052d5b10fee1916c",
                        "withdrawableEpoch": 8726,
                    },
                ],
                "next": "/v0/eth/slashings?size=2&from=207",
                "page": {
                    "filterType": None,
                    "from": None,
                    "granularity": None,
                    "size": 2,
                    "to": None,
                },
                "total": 413,
            },
        )
    )

    penalties = eth_mainnet.slashings.penalties(size=2)
    results = list(penalties)

    assert len(results) == 2
    assert results[0].validator_index == 20075
    assert results[0].slashing_epoch == 208
    assert results[0].slashing_penalties == 606851401
    assert results[1].validator_index == 4259
    assert results[1].slashing_epoch == 534
    assert results[1].slashing_penalties == 602468516


def test_slashings_for_validator_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/slashings/20075").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "balanceBeforeSlashing": 32014860472,
                "balanceBeforeWithdrawal": 31408009071,
                "slashingEpoch": 208,
                "slashingPenalties": 606851401,
                "validatorIndex": 20075,
                "validatorPubkey": "0xb02c42a2cda10f06441597ba87e87a47c187cd70e2b415bef8dc890669efe223f551a2c91c3d63a5779857d3073bf288",
                "withdrawableEpoch": 8400,
            },
        )
    )

    penalty = eth_mainnet.slashings.for_validator(20075)

    assert penalty.validator_index == 20075
    assert penalty.slashing_epoch == 208
    assert penalty.slashing_penalties == 606851401
