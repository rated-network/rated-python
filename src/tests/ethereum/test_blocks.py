import http

import httpx
import pytest


def test_blocks_all_ok_dont_follow_next(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/blocks?size=1").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "page": {"size": 1},
                "data": [
                    {
                        "epoch": 234440,
                        "consensusSlot": 7502102,
                        "consensusBlockRoot": "\\\\x5668a71163c5ec5fcf34185deb36f0c3619a6f00a4ee0a547220f439913b6412",
                        "executionBlockNumber": 18312479,
                        "executionBlockHash": "\\\\x5b138bff063adf335b468150d91eb8c3025a02f6716e3dd4bcee42bf81bb0fe8",
                        "validatorIndex": 888078,
                        "feeRecipient": "\\\\x1f9090aae28b8a3dceadf281b0f12828e676c326",
                        "totalType0Transactions": 19,
                        "totalType2Transactions": 137,
                        "totalTransactions": 156,
                        "totalGasUsed": 11894065,
                        "baseFeePerGas": 7413818806,
                        "totalBurntFees": 88180442776786380,
                        "totalType2TxFees": 11085611875723216,
                        "totalType0TxFees": 23400203843039860,
                        "totalPriorityFees": 34485815,
                        "baselineMev": 0,
                        "executionProposerDuty": "proposed",
                        "executionRewards": 34330125,
                        "missedExecutionRewards": 0,
                        "consensusProposerDuty": "proposed",
                        "consensusRewards": 41947807,
                        "missedConsensusRewards": 0,
                        "totalRewards": 76277932,
                        "totalRewardsMissed": 0,
                        "totalType1Transactions": 0,
                        "totalType1TxFees": 0,
                        "blockTimestamp": 123242323,
                        "totalSanctionedTransactions": 0,
                        "totalPriorityFeesValidator": 34330125,
                        "relays": [
                            "bloxroute_regulated",
                            "flashbots",
                            "bloxroute_maxprofit",
                        ],
                        "blockBuilderPubkeys": [
                            "0x978a35c39c41aadbe35ea29712bccffb117cc6ebcad4d86ea463d712af1dc80131d0c650dc29ba29ef27c881f43bd587",
                            "0x978a35c39c41aadbe35ea29712bccffb117cc6ebcad4d86ea463d712af1dc80131d0c650dc29ba29ef27c881f43bd587",
                            "0x978a35c39c41aadbe35ea29712bccffb117cc6ebcad4d86ea463d712af1dc80131d0c650dc29ba29ef27c881f43bd587",
                        ],
                    }
                ],
                "next": "/v0/eth/blocks/?size=1&from=7502092",
                "total": 1,
            },
        )
    )

    blocks = eth_mainnet.blocks.all(size=1)
    results = list(blocks)

    assert len(results) == 1
    assert results[0].total_rewards == pytest.approx(76277932)
    assert results[0].total_rewards_missed == 0
    assert results[0].total_transactions == 156


def test_block_by_slot_ok(respx_mock, eth_mainnet):
    respx_mock.get("https://api.rated.network/v0/eth/blocks/7502102").mock(
        return_value=httpx.Response(
            http.HTTPStatus.OK,
            json={
                "epoch": 234440,
                "consensusSlot": 7502102,
                "consensusBlockRoot": "\\\\x5668a71163c5ec5fcf34185deb36f0c3619a6f00a4ee0a547220f439913b6412",
                "executionBlockNumber": 18312479,
                "executionBlockHash": "\\\\x5b138bff063adf335b468150d91eb8c3025a02f6716e3dd4bcee42bf81bb0fe8",
                "validatorIndex": 888078,
                "feeRecipient": "\\\\x1f9090aae28b8a3dceadf281b0f12828e676c326",
                "totalType0Transactions": 19,
                "totalType2Transactions": 137,
                "totalTransactions": 156,
                "totalGasUsed": 11894065,
                "baseFeePerGas": 7413818806,
                "totalBurntFees": 88180442776786380,
                "totalType2TxFees": 11085611875723216,
                "totalType0TxFees": 23400203843039860,
                "totalPriorityFees": 34485815,
                "baselineMev": 0,
                "executionProposerDuty": "proposed",
                "executionRewards": 34330125,
                "missedExecutionRewards": 0,
                "consensusProposerDuty": "proposed",
                "consensusRewards": 41947807,
                "missedConsensusRewards": 0,
                "totalRewards": 76277932,
                "totalRewardsMissed": 0,
                "totalType1Transactions": 0,
                "totalType1TxFees": 0,
                "blockTimestamp": "2023-10-09T11:00:47",
                "totalSanctionedTransactions": 0,
                "totalPriorityFeesValidator": 34330125,
                "relays": ["bloxroute_regulated", "flashbots", "bloxroute_maxprofit"],
                "blockBuilderPubkeys": [
                    "0x978a35c39c41aadbe35ea29712bccffb117cc6ebcad4d86ea463d712af1dc80131d0c650dc29ba29ef27c881f43bd587",
                    "0x978a35c39c41aadbe35ea29712bccffb117cc6ebcad4d86ea463d712af1dc80131d0c650dc29ba29ef27c881f43bd587",
                    "0x978a35c39c41aadbe35ea29712bccffb117cc6ebcad4d86ea463d712af1dc80131d0c650dc29ba29ef27c881f43bd587",
                ],
            },
        )
    )

    block = eth_mainnet.block.get(7502102)

    assert block.total_rewards == 76277932
    assert block.consensus_slot == 7502102
    assert len(block.block_builder_pubkeys) == 3
