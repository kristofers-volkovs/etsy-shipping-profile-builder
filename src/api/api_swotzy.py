from api.api_base import ApiBase
import httpx
from schemas.rates import ShippingRatesReq, ShippingRatesRes
from utils import get_env
from abc import ABC, abstractmethod


class ApiSwotzyBase(ApiBase, ABC):
    def _create_http_client(self) -> httpx.Client:
        PUBLIC_KEY = get_env("PUBLIC_KEY")
        PRIVATE_KEY = get_env("PRIVATE_KEY")

        auth = httpx.BasicAuth(username=PUBLIC_KEY, password=PRIVATE_KEY)
        return httpx.Client(auth=auth)

    def _get_base_url(self) -> str:
        return "https://api.swotzy.com/public"

    @abstractmethod
    def get_rates(self, *, req: ShippingRatesReq) -> ShippingRatesRes:
        pass


class ApiSwotzy(ApiSwotzyBase):
    def get_rates(self, *, req: ShippingRatesReq) -> ShippingRatesRes:
        url = self._base_url + "/rates"
        headers = {"Accept": "application/json"}
        data = req.model_dump(mode="json")

        res = self._client.post(url, json=data, headers=headers)
        if res.status_code == 200:
            return ShippingRatesRes(**res.json())
        else:
            raise Exception(f"Failed getting rates, {res.content}")
