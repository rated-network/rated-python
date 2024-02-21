from enum import Enum


class StakeAction(str, Enum):
    ACTIVATION = "activation"
    EXIT = "exit"


class TimeWindow(str, Enum):
    ONE_DAY = "1d"
    SEVEN_DAYS = "7d"
    THIRTY_DAYS = "30d"
    ALL_TIME = "all"


class IdType(str, Enum):
    DEPOSIT_ADDRESS = "depositAddress"
    WITHDRAWAL_ADDRESS = "withdrawalAddress"
    NODE_OPERATOR = "nodeOperator"
    POOL = "pool"
    POOL_SHARE = "poolShare"


class Granularity(str, Enum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    ALL_TIME = "all"


class FilterType(str, Enum):
    HOUR = "hour"
    DAY = "day"
    DATETIME = "datetime"


class AprType(str, Enum):
    BACKWARD = "backward"
    FORWARD = "forward"


class PoolType(str, Enum):
    ALL = "all"
    CEX = "cex"
    LST = "lst"


class DistributionType(str, Enum):
    ALL = "all"
    PROS = "pros"


class ValidatorsEffectivenessGroupBy(str, Enum):
    TIME = "timeWindow"
    VALIDATOR = "validator"
