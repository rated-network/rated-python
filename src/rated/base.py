from typing import Sequence

from rated.client import Client


class Network:
    path: str
    supported_networks: Sequence[str]

    def __init__(self, client: Client) -> None:
        if client.network not in self.supported_networks:
            raise ValueError(f"Unknown network: '{client.network}'")
        self.client = client


class APIResource:
    path: str

    def __init__(self, network: Network) -> None:
        self.network = network

    @property
    def client(self) -> Client:
        return self.network.client

    @property
    def resource_path(self) -> str:
        return f"{self.network.path}{self.path}"
