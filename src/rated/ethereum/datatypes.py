from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Dict, Any


@dataclass
class ValidatorMetadata:
    validator_index: int
    validator_pubkey: str
    pool: str | None = None
    dvt_network: str | None = None
    node_operators: List[str] | None = None
    deposit_addresses: List[str] | None = None
    dvt_operators: List[str] | None = None
    activation_epoch: int | None = None
    activation_eligibility_epoch: int | None = None
    exit_epoch: int | None = None
    withdrawable_epoch: int | None = None
    withdrawal_address: str | None = None


@dataclass
class ValidatorAPR:
    validator_index: int
    id_type: str
    time_window: str
    apr_type: str
    percentage: float
    percentage_consensus: float
    percentage_execution: float
    active_stake: float
    active_validators: int


@dataclass
class ValidatorEffectiveness:
    validator_index: int | None = None
    total_attestations: int | None = None
    total_unique_attestations: int | None = None
    sum_correct_head: int | None = None
    sum_correct_target: int | None = None
    avg_correctness: float | None = None
    total_attestation_assignments: int | None = None
    avg_inclusion_delay: float | None = None
    sum_inclusion_delay: float | None = None
    uptime: float | None = None
    attester_effectiveness: float | None = None
    proposed_count: int | None = None
    proposer_duties_count: int | None = None
    proposer_effectiveness: float | None = None
    slashes_collected: int | None = None
    slashes_received: int | None = None
    earnings: int | None = None
    sync_signature_count: int | None = None
    validator_effectiveness: float | None = None
    estimated_rewards: int | None = None
    estimated_penalties: int | None = None
    sum_priority_fees: int | None = None
    sum_baseline_mev: int | None = None
    sum_missed_execution_rewards: int | None = None
    sum_consensus_block_rewards: int | None = None
    sum_missed_consensus_block_rewards: int | None = None
    sum_all_rewards: int | None = None
    sum_correct_source: int | None = None
    sum_missed_sync_signatures: int | None = None
    sum_sync_committee_penalties: float | None = None
    sum_late_source_votes: int | None = None
    sum_wrong_target_votes: int | None = None
    sum_late_target_votes: int | None = None
    sum_wrong_target_penalties: float | None = None
    sum_late_target_penalties: float | None = None
    sum_missed_attestations: int | None = None
    sum_missed_attestation_penalties: float | None = None
    sum_wrong_head_votes: int | None = None
    sum_wrong_head_penalties: float | None = None
    sum_attestation_rewards: float | None = None
    sum_late_source_penalties: float | None = None
    execution_proposed_empty_count: int | None = None
    sum_missed_attestation_rewards: float | None = None
    sum_missed_sync_committee_rewards: float | None = None
    sum_externally_sourced_execution_rewards: int | None = None
    day: int | None = None
    start_day: int | None = None
    end_day: int | None = None
    start_epoch: int | None = None
    end_epoch: int | None = None
    hour: int | None = None


@dataclass
class NetworkStats:
    day: int
    avg_uptime: float
    avg_inclusion_delay: float
    avg_correctness: float
    avg_validator_effectiveness: float


@dataclass
class NetworkOverview:
    time_window: str
    validator_count: int
    sum_missed_slots: int
    missed_slots_percentage: float
    active_stake: int
    median_validator_age_days: int
    avg_validator_balance: float
    gini_coefficient: float
    client_percentages: List[Dict]
    latest_epoch: int
    activation_queue_minutes: float
    activating_validators: int
    activating_stake: int
    exit_queue_minutes: float
    withdrawal_queue_minutes: float
    withdrawal_processing_queue_minutes: float
    fully_withdrawing_validators: int
    partially_withdrawing_validators: int
    total_withdrawing_validators: int
    fully_withdrawing_balance: int
    partially_withdrawing_balance: int
    total_withdrawing_balance: int
    exiting_validators: int
    validator_count_diff: int | None = None
    active_stake_diff: int | None = None
    avg_validator_balance_diff: float | None = None
    consensus_layer_rewards_percentage: float | None = None
    priority_fees_percentage: float | None = None
    baseline_mev_percentage: float | None = None
    avg_validator_effectiveness: float | None = None
    avg_inclusion_delay: float | None = None
    avg_uptime: float | None = None
    avg_consensus_apr_percentage: float | None = None
    avg_execution_apr_percentage: float | None = None
    median_consensus_apr_percentage: float | None = None
    median_execution_apr_percentage: float | None = None
    consensus_rewards_ratio: float | None = None
    execution_rewards_ratio: float | None = None
    avg_network_apr_percentage: float | None = None
    median_network_apr_percentage: float | None = None
    avg_consensus_apr_gwei: int | None = None
    avg_execution_apr_gwei: int | None = None
    median_consensus_apr_gwei: int | None = None
    median_execution_apr_gwei: int | None = None
    avg_network_apr_gwei: int | None = None
    median_network_apr_gwei: int | None = None
    client_validator_effectiveness: List[Dict] | None = None
    exiting_stake: int | None = None


@dataclass
class NetworkChurnCapacity:
    time_window: str
    latest_epoch: int
    activated_validators: int
    activation_capacity_filled: float
    exited_validators: int
    exit_capacity_filled: float
    activated_percentage: float
    exited_percentage: float
    churn_limit: int
    activation_churn_limit: int
    exit_churn_limit: int


@dataclass
class NetworkChurnCapacityPool:
    time_window: str
    stake_action: str
    latest_epoch: int
    churn_limit: int
    pool: str
    validator_count: int
    capacity_filled: float
    network_capacity_remaining: float


@dataclass
class Block:
    epoch: int
    consensus_slot: int
    validator_index: int
    relays: List[str]
    block_builder_pubkeys: List[str]
    execution_proposer_duty: str
    consensus_proposer_duty: str
    consensus_block_root: str | None = None
    execution_block_number: int | None = None
    execution_block_hash: str | None = None
    fee_recipient: str | None = None
    total_type0_transactions: int | None = None
    total_type2_transactions: int | None = None
    total_transactions: int | None = None
    total_gas_used: int | None = None
    base_fee_per_gas: int | None = None
    total_burnt_fees: int | None = None
    total_type2_tx_fees: int | None = None
    total_type0_tx_fees: int | None = None
    total_priority_fees: int | None = None
    baseline_mev: int | None = None
    execution_rewards: int | None = None
    missed_execution_rewards: int | None = None
    consensus_rewards: int | None = None
    missed_consensus_rewards: float | None = None
    total_rewards: int | None = None
    total_rewards_missed: float | None = None
    total_type1_transactions: int | None = None
    total_type1_tx_fees: int | None = None
    block_timestamp: datetime | None = None
    total_sanctioned_transactions: int | None = None
    total_priority_fees_validator: int | None = None
    total_type3_transactions: int | None = None
    total_type3_tx_fees: int | None = None


@dataclass
class Withdrawal:
    validator_index: int
    withdrawal_type: str
    withdrawable_amount: int
    id: str
    id_type: str
    withdrawal_slot: int
    withdrawal_epoch: int


@dataclass
class P2PGeographicalDistribution:
    country: str
    country_code: str
    validator_share: float
    dist_type: str


@dataclass
class P2PHostingProviderDistribution:
    hosting_provider: str
    validator_share: float
    dist_type: str


@dataclass
class SlashingOverview:
    time_window: str
    validators_slashed: int
    discrete_slashing_events: int
    largest_slashing_incident: int
    current_slashing_penalty_gwei: int
    slashing_slots_ratio: float
    solos_ratio: float
    pros_ratio: float
    slashing_penalties_all_rewards_ratio: float
    slashing_penalties_stake_ratio: float


@dataclass
class SlashingLeaderboard:
    id: str
    id_type: str
    slashes: int
    median_slashed_month: str
    slasher_pedigree: str
    slashing_role: str
    validator_count: int


@dataclass
class SlashingCohort:
    cohort: str
    last_six_months: int
    past_year: int
    past_two_years: int
    all_time: int


@dataclass
class SlashingTimeInterval:
    month: date
    validators_slashed: int


@dataclass
class SlashingPenalty:
    validator_index: int
    validator_pubkey: str
    slashing_epoch: int
    withdrawable_epoch: int
    balance_before_slashing: int
    balance_before_withdrawal: int
    slashing_penalties: int


@dataclass
class Operator:
    id: str
    id_type: str
    display_name: str
    operator_tags: List[Dict[str, Any]]
    node_operator_count: int | None = None


@dataclass
class OperatorEffectiveness:
    id: str
    id_type: str
    validator_count: int | None = None
    avg_inclusion_delay: float | None = None
    avg_uptime: float | None = None
    avg_correctness: float | None = None
    avg_proposer_effectiveness: float | None = None
    avg_validator_effectiveness: float | None = None
    total_unique_attestations: int | None = None
    sum_correct_head: int | None = None
    sum_correct_target: int | None = None
    sum_inclusion_delay: float | None = None
    sum_proposed_count: int | None = None
    sum_proposer_duties_count: int | None = None
    slashes_collected: int | None = None
    slashes_received: int | None = None
    sum_earnings: int | None = None
    sum_estimated_rewards: int | None = None
    sum_estimated_penalties: int | None = None
    network_penetration: float | None = None
    sum_priority_fees: int | None = None
    sum_baseline_mev: int | None = None
    sum_missed_execution_rewards: int | None = None
    sum_consensus_block_rewards: int | None = None
    sum_missed_consensus_block_rewards: int | None = None
    sum_all_rewards: int | None = None
    sum_correct_source: int | None = None
    avg_attester_effectiveness: float | None = None
    sum_missed_sync_signatures: int | None = None
    sum_sync_committee_penalties: float | None = None
    sum_late_source_votes: int | None = None
    sum_wrong_target_votes: int | None = None
    sum_late_target_votes: int | None = None
    sum_wrong_target_penalties: float | None = None
    sum_late_target_penalties: float | None = None
    sum_missed_attestations: int | None = None
    sum_missed_attestation_penalties: float | None = None
    sum_wrong_head_votes: int | None = None
    sum_wrong_head_penalties: float | None = None
    sum_attestation_rewards: float | None = None
    sum_late_source_penalties: float | None = None
    sum_execution_proposed_empty_count: int | None = None
    sum_missed_attestation_rewards: float | None = None
    sum_missed_sync_committee_rewards: float | None = None
    sum_externally_sourced_execution_rewards: int | None = None
    day: int | None = None
    start_day: int | None = None
    end_day: int | None = None
    end_epoch: int | None = None
    start_epoch: int | None = None
    hour: int | None = None


@dataclass
class ClientPercentage:
    client: str
    percentage: float


@dataclass
class RelayerPercentage:
    relayer: str
    percentage: float


@dataclass
class OperatorApr:
    id: str
    id_type: str
    time_window: str
    apr_type: str
    percentage: float
    percentage_consensus: float
    percentage_execution: float
    active_stake: float
    active_validators: int


@dataclass
class OperatorSummary:
    id: str
    id_type: str
    time_window: str
    validator_count: int
    avg_correctness: float
    avg_uptime: float
    avg_validator_effectiveness: float
    client_percentages: List[Dict[str, Any]]
    relayer_percentages: List[Dict[str, Any]]
    operator_tags: List[Dict[str, Any]]
    network_penetration: float | None = None
    avg_inclusion_delay: float | None = None
    node_operator_count: int | None = None
    display_name: str | None = None
    apr_percentage: str | None = None


@dataclass
class OperatorStakeMovement:
    time_window: str
    id: str
    id_type: str
    stake_action: str
    validator_count: int
    avg_epochs_to_action: int
    avg_minutes_to_action: float
    amount_gwei: int | None = None


@dataclass
class Percentile:
    time_window: str
    rank: int
    value: float
