from typing import Sequence

from rated.client import Client


class Network:
    """A supported network you can access with the Rated API"""

    path: str
    supported_networks: Sequence[str]

    def __init__(self, client: Client) -> None:
        """
        Initialize the client to access this network

        Args:
            client: HTTP Client to use for requests

        Raises:
             ValueError: If the client is not supported
        """
        if client.network not in self.supported_networks:
            raise ValueError(f"Unknown network: '{client.network}'")
        self.client = client


class APIResource:
    """An API resource you can consume from the Rated API"""

    path: str

    def __init__(self, network: Network) -> None:
        """
        Initialize the API resource for the given network

        Args:
            network: The network to consume
        """
        self.network = network

    @property
    def client(self) -> Client:
        """Get a Client object ready to access the network"""
        return self.network.client

    @property
    def resource_path(self) -> str:
        """Full path to the API resource"""
        return f"{self.network.path}{self.path}"
