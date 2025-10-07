import httpx
from abc import ABC, abstractmethod


class ApiBase(ABC):
    def __init__(self) -> None:
        self._client = self._create_http_client()
        self._base_url = self._get_base_url()

    @abstractmethod
    def _create_http_client(self) -> httpx.Client:
        pass

    @abstractmethod
    def _get_base_url(self) -> str:
        pass
