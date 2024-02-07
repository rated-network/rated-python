import pytest

import rated


@pytest.fixture(scope="session")
def eth_mainnet():
    r = rated.Rated("fake_key")
    eth = r.ethereum(network=rated.ethereum.MAINNET)
    yield eth
