from rated.base import Network
from rated.ethereum.blocks import Blocks
from rated.ethereum.operators import Operator, Operators
from rated.ethereum.p2p import P2P
from rated.ethereum.slashings import Slashings
from rated.ethereum.validators import Validator, Validators
from rated.ethereum.network import Network as NetworkMetrics
from rated.ethereum.withdrawals import Withdrawals

# supported networks
MAINNET = "mainnet"
HOLESKY = "holesky"


class Ethereum(Network):
    path = "/v0/eth"
    supported_networks = [MAINNET, HOLESKY]

    @property
    def blocks(self):
        return Blocks(self)

    @property
    def network(self):
        return NetworkMetrics(self)

    @property
    def operator(self):
        return Operator(self)

    @property
    def operators(self):
        return Operators(self)

    @property
    def p2p(self):
        return P2P(self)

    @property
    def slashings(self):
        return Slashings(self)

    @property
    def validator(self):
        return Validator(self)

    @property
    def validators(self):
        return Validators(self)

    @property
    def withdrawals(self):
        return Withdrawals(self)
